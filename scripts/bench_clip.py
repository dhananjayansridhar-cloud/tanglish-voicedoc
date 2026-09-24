"""Replay a recorded clip through the live pipeline (VAD -> ASR -> translation) and report quality, latency and VRAM.

Usage: python scripts/bench_clip.py samples/yt/jOT8eHwlXHQ.wav [--ref samples/yt/jOT8eHwlXHQ.ref_youtube_auto_ta.txt]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from voicedoc.asr import Transcriber  # noqa: E402
from voicedoc.audio import CHUNK, SAMPLE_RATE, PhraseSegmenter, VadConfig  # noqa: E402
from voicedoc.translate import Translator  # noqa: E402


def cer(hyp: str, ref: str) -> float:
    """Character error rate, whitespace ignored (Levenshtein distance / reference length)."""
    h, r = "".join(hyp.split()), "".join(ref.split())
    prev = list(range(len(r) + 1))
    for i, hc in enumerate(h, 1):
        cur = [i] + [0] * len(r)
        for j, rc in enumerate(r, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (hc != rc))
        prev = cur
    return prev[-1] / max(1, len(r))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("wav", type=Path)
    ap.add_argument("--ref", type=Path, default=None, help="reference transcript (native Tamil script)")
    ap.add_argument("--min-silence-ms", type=int, default=400)
    ap.add_argument("--no-translate", action="store_true", help="benchmark speech recognition only")
    args = ap.parse_args()

    audio, sr = sf.read(args.wav, dtype="float32", always_2d=True)
    audio = audio.mean(axis=1)
    if sr != SAMPLE_RATE:
        sys.exit(f"{args.wav} is {sr} Hz; convert to 16 kHz mono first (ffmpeg -ar 16000 -ac 1)")

    phrases: list[tuple[float, np.ndarray]] = []
    pos = [0]
    seg = PhraseSegmenter(VadConfig(min_silence_ms=args.min_silence_ms),
                          on_phrase=lambda a: phrases.append((pos[0] / SAMPLE_RATE, a)))
    for i in range(0, len(audio) - CHUNK + 1, CHUNK):
        pos[0] = i + CHUNK
        seg.feed(audio[i:i + CHUNK])
    print(f"{len(audio) / SAMPLE_RATE:.1f}s audio -> {len(phrases)} phrases")

    import torch
    t0 = time.perf_counter()
    asr = Transcriber(mode="native")
    t_asr_load = time.perf_counter() - t0
    after_asr = torch.cuda.memory_allocated() / 2**20
    t0 = time.perf_counter()
    mt = (lambda s: ("", 0.0)) if args.no_translate else Translator(device=str(asr.device))
    t_mt_load = time.perf_counter() - t0
    after_mt = torch.cuda.memory_allocated() / 2**20
    torch.cuda.reset_peak_memory_stats()

    rows, natives = [], []
    for end_s, a in phrases:
        asr.mode = "native"
        nat, t_nat = asr(a)
        asr.mode = "mixed"
        mix, t_mix = asr(a)
        en_nat, t_en_nat = mt(nat) if nat else ("", 0.0)
        en_mix, t_en_mix = mt(mix) if mix else ("", 0.0)
        natives.append(nat)
        rows.append((end_s, len(a) / SAMPLE_RATE, nat, t_nat, mix, t_mix, en_nat, t_en_nat, en_mix, t_en_mix))
        print(f"[{end_s:6.1f}s | {len(a) / SAMPLE_RATE:4.1f}s] asr {t_nat:.2f}s  mt {t_en_nat:.2f}s  -> {en_nat}")
    peak = torch.cuda.max_memory_allocated() / 2**20

    out = [f"# Bench: `{args.wav.name}`", "",
           f"- Audio {len(audio) / SAMPLE_RATE:.1f} s, {len(phrases)} phrases (VAD min silence {args.min_silence_ms} ms)",
           f"- ASR load {t_asr_load:.1f} s, {after_asr:.0f} MiB allocated; translator load {t_mt_load:.1f} s, total {after_mt:.0f} MiB",
           f"- Peak PyTorch GPU memory while running: {peak:.0f} MiB (excludes CUDA context, about 300-500 MiB)",
           f"- GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}", ""]
    lat = [r[3] + r[7] for r in rows]
    if lat:
        out.append(f"- Phrase latency after the pause (ASR native + translation): median {np.median(lat):.2f} s, max {max(lat):.2f} s")
    if args.ref and args.ref.is_file():
        ref = args.ref.read_text(encoding="utf-8")
        out.append(f"- CER, native-script ASR vs `{args.ref.name}`: **{cer(' '.join(natives), ref):.1%}** "
                   "(the reference is YouTube's own auto-caption, i.e. another ASR system, not a human transcript)")
    out += ["", "| end (s) | len (s) | ASR native | ASR mixed | English (from native) | English (from mixed) | asr s | mt s |",
            "|---|---|---|---|---|---|---|---|"]
    for end_s, ln, nat, t_nat, mix, t_mix, en_nat, t_en_nat, en_mix, t_en_mix in rows:
        out.append(f"| {end_s:.1f} | {ln:.1f} | {nat} | {mix} | {en_nat} | {en_mix} | {t_nat:.2f} | {t_en_nat:.2f} |")
    report = args.wav.with_suffix(".bench.md")
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
