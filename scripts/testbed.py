"""Test bed: download every clip in samples/testbed.txt, run VAD -> ASR (mixed) -> translation, write one report.

Usage: python scripts/testbed.py [--mt ai4bharat/indictrans2-indic-en-dist-200M ai4bharat/indictrans2-indic-en-1B]
Output: samples/testbed_report.md (plus per-clip audio and YouTube Tamil auto-captions in samples/yt/).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from bench_clip import cer  # noqa: E402
from voicedoc.asr import Transcriber  # noqa: E402
from voicedoc.audio import CHUNK, SAMPLE_RATE, PhraseSegmenter, VadConfig  # noqa: E402
from voicedoc.translate import MODEL_NAME, Translator  # noqa: E402

YT = ROOT / "samples" / "yt"
YTDLP = Path.home() / ".local" / "bin" / "yt-dlp.exe"
_VTT_SKIP = re.compile(r"^(WEBVTT|Kind:|Language:|\d{2}:\d{2}:\d{2}\.\d{3} -->|\s*$)")


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def fetch(url: str) -> tuple[str, Path, Path | None, str]:
    """Returns (video id, 16 kHz wav, reference caption text file or None, title)."""
    info = _run([str(YTDLP), "--print", "%(id)s|%(title)s", "--skip-download", url]).stdout.strip().splitlines()
    if not info:
        raise RuntimeError(f"yt-dlp could not read {url}")
    vid, title = info[-1].split("|", 1)
    wav = YT / f"{vid}.wav"
    if not wav.exists():
        r = _run([str(YTDLP), "-x", "--audio-format", "wav", "--postprocessor-args", "ffmpeg:-ar 16000 -ac 1",
                  "-o", str(YT / "%(id)s.%(ext)s"), url])
        if not wav.exists():
            raise RuntimeError(f"audio download failed for {url}: {r.stderr[-300:]}")
    ref = YT / f"{vid}.ref_youtube_auto_ta.txt"
    vtt = YT / f"{vid}.ta.vtt"
    for attempt in range(4):  # YouTube answers caption requests with HTTP 429 when hit repeatedly
        if vtt.exists():
            break
        _run([str(YTDLP), "--skip-download", "--write-auto-subs", "--sub-langs", "ta", "--sub-format", "vtt",
              "-o", str(YT / "%(id)s.%(ext)s"), url])
        if not vtt.exists():
            time.sleep(10 * (attempt + 1))
    if vtt.exists() and not ref.exists():
        seen, words = set(), []
        for line in vtt.read_text(encoding="utf-8").splitlines():
            if _VTT_SKIP.match(line):
                continue
            line = re.sub(r"<[^>]+>", "", line)
            if line not in seen:
                seen.add(line)
                words.append(line)
        ref.write_text(" ".join(words), encoding="utf-8")
    return vid, wav, (ref if ref.exists() else None), title


def phrases_of(wav: Path) -> tuple[float, list[tuple[float, np.ndarray]]]:
    audio, sr = sf.read(wav, dtype="float32", always_2d=True)
    audio = audio.mean(axis=1)
    if sr != SAMPLE_RATE:
        raise RuntimeError(f"{wav} is {sr} Hz, expected 16 kHz")
    out: list[tuple[float, np.ndarray]] = []
    pos = [0]
    seg = PhraseSegmenter(VadConfig(), on_phrase=lambda a: out.append((pos[0] / SAMPLE_RATE, a)))
    for i in range(0, len(audio) - CHUNK + 1, CHUNK):
        pos[0] = i + CHUNK
        seg.feed(audio[i:i + CHUNK])
    return len(audio) / SAMPLE_RATE, out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mt", nargs="+", default=[MODEL_NAME], help="translation model(s) to compare")
    args = ap.parse_args()

    lines = [ln.split("|", 1) for ln in (ROOT / "samples" / "testbed.txt").read_text(encoding="utf-8").splitlines()
             if ln.strip() and not ln.startswith("#")]
    clips = []
    for parts in lines:
        url, note = parts[0].strip(), (parts[1].strip() if len(parts) > 1 else "")
        try:
            vid, wav, ref, title = fetch(url)
        except RuntimeError as exc:
            print(f"SKIP {url}: {exc}")
            continue
        dur, phrases = phrases_of(wav)
        clips.append({"url": url, "note": note, "vid": vid, "title": title, "ref": ref, "dur": dur, "phrases": phrases})
        print(f"{vid}: {dur:.1f}s, {len(phrases)} phrases, captions: {'yes' if ref else 'NO (429 or none)'}")

    import torch
    asr = Transcriber(mode="mixed")
    for c in clips:
        c["asr"] = []
        for end_s, a in c["phrases"]:
            asr.mode = "mixed"
            mix, t_mix = asr(a)
            asr.mode = "native"
            nat, _ = asr(a)
            c["asr"].append((end_s, len(a) / SAMPLE_RATE, mix, nat, t_mix))

    results: dict[str, dict[str, list[tuple[str, float]]]] = {}
    peaks: dict[str, float] = {}
    for name in args.mt:
        torch.cuda.reset_peak_memory_stats()
        try:
            mt = Translator(device=str(asr.device), model_name=name)
        except OSError as exc:
            print(f"SKIP translator {name}: {str(exc).splitlines()[0]}")
            continue
        results[name] = {c["vid"]: [mt(mix) if mix else ("", 0.0) for _, _, mix, _, _ in c["asr"]] for c in clips}
        peaks[name] = torch.cuda.max_memory_allocated() / 2**20
        del mt
        torch.cuda.empty_cache()

    out = ["# Test bed report", "", f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `scripts/testbed.py`. "
           "ASR: Indic-Transcribe-flex, mixed script. Reference = YouTube Tamil auto-captions (another ASR system, "
           "not a human transcript), so CER is agreement, not accuracy.", "",
           f"GPU: {torch.cuda.get_device_name(0)}. Peak PyTorch VRAM with ASR + translator: "
           + ", ".join(f"`{n.split('/')[-1]}` {p:.0f} MiB" for n, p in peaks.items()), "",
           "| Clip | Note | Length | Phrases | Native CER vs captions | ASR median s | " +
           " | ".join(f"MT median s ({n.split('/')[-1]})" for n in results) + " |",
           "|---|---|---|---|---|---|" + "---|" * len(results)]
    for c in clips:
        nat_all = " ".join(r[3] for r in c["asr"])
        c_cer = f"{cer(nat_all, c['ref'].read_text(encoding='utf-8')):.1%}" if c["ref"] else "no captions"
        asr_med = np.median([r[4] for r in c["asr"]]) if c["asr"] else 0.0
        mts = " | ".join(f"{np.median([t for _, t in results[n][c['vid']]]):.2f}" if c["asr"] else "-" for n in results)
        out.append(f"| [{c['vid']}]({c['url']}) | {c['note']} | {c['dur']:.0f}s | {len(c['phrases'])} | {c_cer} | "
                   f"{asr_med:.2f} | {mts} |")
    for c in clips:
        out += ["", f"## {c['vid']} — {c['title']}", "", f"{c['note']}", "",
                "| end s | ASR (mixed) | " + " | ".join(f"English ({n.split('/')[-1]})" for n in results) + " |",
                "|---|---|" + "---|" * len(results)]
        for i, (end_s, _, mix, _, _) in enumerate(c["asr"]):
            ens = " | ".join(results[n][c["vid"]][i][0] for n in results)
            out.append(f"| {end_s:.1f} | {mix} | {ens} |")
    report = ROOT / "samples" / "testbed_report.md"
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
