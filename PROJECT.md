# VoiceDoc — project state

Status (2026-09-24): **v0.2, desktop app working on the target laptop.** A tray app speaks Tamil/Tanglish in and
writes English out, live, fully local. User guide: `README.md`. Model selection evidence: `RECOMMENDATION.md`,
`research/`, `research.md`.

## Architecture

```text
mic (Windows communications/default device, followed live; audio.Microphone)
 └► Silero VAD on CPU: phrase ends at 400 ms pause or 12 s          audio.PhraseSegmenter (gated by pause/mute)
     └► Indic-Transcribe-flex, lang=ta, mode=mixed, GPU bf16          asr.Transcriber
         └► IndicTrans2 indic-en-dist-200M, GPU fp16, beam 5           translate.Translator (+ custom replacements)
             ├► cursor mode: pynput types at the cursor               app.CursorController, desktop.CursorTyper
             │   (focus handed back to the last real app window)       desktop.FocusTracker
             └► note mode: router → dictation append / "command …"    app.Controller, router, organizer (Ollama CPU)
                 → typed edit ops, undo, confirm-on-delete            document.Document
                 → external-edit guard → atomic .md write             Controller._sync_from_disk, write_atomic
tray (pystray) + hotkey (pynput) + status/history/help windows (tkinter) + spoken questions (pyttsx3/SAPI)
VoiceDoc.exe = PyInstaller launcher → .venv\Scripts\pythonw.exe -m voicedoc (single instance via named mutex)
```

## Decisions and the evidence behind them

| Decision | Evidence |
|---|---|
| ASR = `bodhan-ai/indic-transcribe-flex`, mixed script | Jev rank 1 (weighted 0.701, Choice p = 0.66); Voice of India Tamil WER 10.8 (developer-reported); the only local model with a Tamil-script + Latin-English output mode |
| Mixed (not native) script as translator input | test bed: native input produced "Deep Gram", "Poitur" and a 40× repetition loop; mixed did not |
| MT = IndicTrans2 200M | the only candidate that fits next to the ASR in 6 GB (1B ≈ 2 GB fp16 is pending licence access; bodhan indic-translate is 7.9 B) |
| Dictation never goes through the LLM | the organiser runs on CPU (GPU reserved); a call per phrase would lag the live text |
| The LLM can only choose from a fixed JSON edit-op schema | a model error cannot corrupt the file; every op is undoable |
| Max phrase 12 s (was 25 s) | bench: median latency 2.02 → 1.31 s, CER 13.0 → 12.1% |
| Follow the Windows *communications* capture device | the user's Bluetooth headset was the communications default while the laptop array was the console default |
| Type with key events, not clipboard paste | never clobbers the user's clipboard; no restore race |
| Cursor mode + paused at start-up, Startup shortcut | user request: "one click on the mic icon should listen and start typing" |

Ease-of-use features were chosen from what mature dictation apps share (Handy, OpenWhispr, VoiceInk, whisper-writer,
Buzz; `research/04_github_practitioners/research_dictation_app_ux.md`): global hotkey with toggle/hold, tray,
status overlay, custom dictionary, history, settings file, saved audio, start/stop sounds.

## Measured on this laptop (RTX 3050 6 GB)

Test bed = 5 Tamil YouTube Shorts (`samples/testbed.txt` → `samples/testbed_report.md`). Reference = YouTube's own
Tamil auto-captions (another ASR system), so CER is agreement, not accuracy.

| Clip | Kind | CER vs captions | ASR median | MT median |
|---|---|---|---|---|
| jOT8eHwlXHQ | fast tech talk, 1 speaker | 12.1% | 1.13 s | 0.64 s |
| upVmMFjZGQ0 | film interview, idioms | 11.8% | 1.32 s | 0.89 s |
| zm_obU5n8B0 | comedy, several speakers, music | n/a (captions unusable) | 0.39 s | 0.32 s |
| wG6xp3AmNaM | reminiscence | 19.7% | 0.41 s | 0.26 s |
| 8xgD-2qYdr0 | street interview, heavy code-mix | 31.3% | 0.95 s | 0.54 s |

- Peak PyTorch VRAM with ASR + MT: **2.77 GB**. ASR model load ~16 s, MT ~5 s.
- Speaker → air → laptop-mic end-to-end run (upVmMFjZGQ0): each phrase landed in the note during playback.
- The user's own voice (laptop mic): "இன்னைக்கு நான் எங்கே போய் சாப்பிட்றது?" → "Where am I going to eat today?".
- **Weakest step = translation**: slang and names fail ("பொண்டாட்டி" → "Ponti", "பாட்டில்" (in the song) → "bottle",
  "அன்பே சிவம்" → "dear Shiva").

## Known limits / next

- Phrase-by-phrase, not word-by-word (the default model does not stream; "lite" streaming variant is unreleased).
- No per-word "did you say X?" confidence: the ASR does not expose token probabilities.
- No speaker labels; the ASR card states single-speaker training (overlapping speech degrades).
- Bluetooth headset mic runs in hands-free mode (16/8 kHz); accuracy on it is not yet measured.
- Organiser (`qwen3:4b`, CPU) latency and Tanglish command accuracy not yet measured on real commands.
- Next: IndicTrans2-1B comparison (licence pending, HTTP 403 for account dhansrid); portable installer for other PCs;
  user-chosen extras (voice-added dictionary words, clean-up pass, Tamil TTS, natural Windows voices).

## Environment notes

- Python 3.10.11 venv `.venv`; `transformers>=4.56,<5` (IndicTransToolkit breaks on v5; Indic-Transcribe needs
  `dtype=`); IndicTrans2 remote code needs `use_cache=False` on transformers 4.57.
- pip cache/temp redirected to `.cache/` (C: was full). HF token belongs to account **dhansrid**.
- Ollama must run with `qwen3:4b`; requests force `num_gpu: 0` so it stays off the GPU.
