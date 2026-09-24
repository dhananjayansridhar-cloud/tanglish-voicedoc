# VoiceDoc

**Speak colloquial Tamil / Tanglish, get English text, live, fully offline.**

VoiceDoc sits in the Windows system tray. Click the mic icon (or press **Ctrl+Shift+Space**), talk, and the English
translation of each phrase appears a second or two after you pause. The text goes either **where your cursor is**
(Notepad++, VS Code, Word, a browser…) or into **today's Markdown note**, which you can reorganise by voice.

Everything runs on your own laptop GPU. Nothing is sent to the internet; there are no API keys or paid services.

```text
your voice ──► pause detection ──► Tamil/Tanglish speech recognition ──► Tamil→English translation ──► your text
               (Silero VAD, CPU)    (Indic-Transcribe-flex, GPU)           (IndicTrans2, GPU)
```

## Requirements

| | |
|---|---|
| OS | Windows 10/11 |
| GPU | NVIDIA with ≥ 6 GB VRAM (tested: RTX 3050 Laptop 6 GB; uses ~2.8 GB peak) |
| RAM | 16 GB (keep ~6 GB free while dictating) |
| Disk | ~10 GB (models ~5.5 GB + PyTorch ~3 GB) |
| Software | Python 3.10, [Ollama](https://ollama.com/download/windows) (for voice commands in note mode) |
| Hugging Face | a free account that has accepted the licences of the gated models below |

## Setup (once)

```powershell
# 1. virtual environment + CUDA PyTorch
py -3.10 -m venv .venv
.venv\Scripts\python.exe -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu126
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2. models (accept the licence on each model page first, then log in)
hf auth login
hf download bodhan-ai/indic-transcribe-flex --local-dir models/indic-transcribe-flex --exclude "nemo/*"
#    ai4bharat/indictrans2-indic-en-dist-200M downloads automatically on first run (licence must be accepted)

# 3. organiser model for voice commands
ollama pull qwen3:4b

# 4. build the app: VoiceDoc.exe + desktop/Start-menu shortcuts (+ -Startup to launch with Windows)
powershell -ExecutionPolicy Bypass -File scripts\build_app.ps1 -Startup
```

Gated model pages to accept: [indic-transcribe-flex](https://huggingface.co/bodhan-ai/indic-transcribe-flex),
[indictrans2-indic-en-dist-200M](https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M).

## Daily use

1. Start **VoiceDoc** (desktop icon, Start menu, or automatically with Windows). It loads for ~25 s, then waits in
   the tray. **Grey mic = paused, green mic = listening.** If you don't see it, click the **^** by the clock and drag
   the mic onto the taskbar.
2. Click into the app you want to type in.
3. **Left-click the mic icon** (or **Ctrl+Shift+Space**): beep, icon turns green. Speak naturally, with short pauses.
4. Click again to stop.

Right-click the mic icon for everything else:

| Menu item | What it does |
|---|---|
| Start / Pause listening | same as a left-click |
| Write to today's note | text goes to `notes/YYYY-MM-DD.md` (open it in VS Code, `Ctrl+K V` for live preview) |
| Type at cursor (any app) | text is typed where your cursor is; your clipboard is never touched |
| Microphone | follow the Windows communications device (headsets), the default device, or pick one |
| Show status window | small always-on-top window showing what it is doing and the last sentence |
| History… | recent phrases with the original Tamil, the English, Copy and Play-audio buttons |
| Help… | full in-app help |
| Settings… | opens `voicedoc.json` (restart after editing) |

## Voice commands

Always start with the word **"command"** (or **கமாண்ட்**). Everything else is dictation.

**Type-at-cursor mode**

| Say | Effect |
|---|---|
| command new line / command new paragraph | Enter / Enter Enter |
| command bullet / command heading | types `- ` / `## ` |
| command scratch that | deletes exactly the phrase it just typed |
| command undo | sends Ctrl+Z |

**Note mode** (a local model on CPU interprets these; the first command after start-up takes longer)

| Say | Effect |
|---|---|
| command new section Meeting notes | new `##` section; next dictation goes there |
| command budget section-ku po | continue writing under "Budget" |
| command idha action items-ku move pannu | move the last paragraph to "Action items" |
| command last paragraph-a bullet points-a maathu | turn it into a bullet list |
| command rename Budjet to Budget | rename a section |
| command andha section-a delete pannu | asks to confirm aloud: answer "yes" / "ஆமா" or "no" / "வேண்டாம்" |
| command scratch that / command undo | instant undo of the last change |

If a command is unclear, VoiceDoc asks a short question on screen and aloud; your next sentence is the answer.

## Your data

All under `notes/` (never uploaded, never committed to git):

- `YYYY-MM-DD.md`: today's note (English)
- `YYYY-MM-DD.transcript.md`: every phrase as heard (Tamil) → as written (English), with a link to its audio
- `YYYY-MM-DD.audio/`: the audio of every phrase (turn off with `"save_audio": false`)
- `voicedoc.log`: errors and start-up messages

If you edit the note by hand while VoiceDoc runs, your edits are kept. If they use structure VoiceDoc can't merge
(tables, `###` headings), it pauses instead of overwriting.

## Settings (`voicedoc.json`)

| Key | Default | Meaning |
|---|---|---|
| `output` | `"cursor"` | start-up mode: `"cursor"` or `"file"` |
| `start_listening` | `false` | listen immediately at start-up |
| `hotkey`, `hotkey_mode` | `"ctrl+shift+space"`, `"toggle"` | `"hold"` = push-to-talk |
| `mic` | `"communications"` | `"communications"`, `"default"`, or part of a device name |
| `min_silence_ms`, `max_phrase_s` | `400`, `12` | pause that ends a phrase; longest phrase before text is forced out |
| `replacements` | `{}` | fix recurring words, e.g. `{"diarrhegation": "diarization"}` |
| `translate` | `true` | `false` writes the Tamil transcript instead of English |
| `speak_questions`, `voice`, `voice_rate` | `true`, `null`, `185` | spoken questions via Windows voices (`"Zira"`, …) |
| `sounds`, `save_audio`, `overlay` | `true`, `true`, `false` | beeps, per-phrase audio, status window at start-up |
| `use_llm`, `llm` | `true`, `"qwen3:4b"` | note-mode command interpreter (Ollama, CPU) |

A malformed file is reported with the line and column, never silently replaced.

**Nicer voice for spoken questions:** install [NaturalVoiceSAPIAdapter](https://github.com/gexgd0419/NaturalVoiceSAPIAdapter)
with its online voices unticked; its natural Narrator voices are chosen automatically. (It is an unofficial workaround
that a Windows update can break.)

## Troubleshooting

| Symptom | Fix |
|---|---|
| Nothing is typed | click into the target app first; the text goes to the last app you used before clicking the mic |
| Wrong microphone | right-click → Microphone; for headsets use "Follow Windows communications device" |
| "already running" | VoiceDoc is in the tray; right-click → Quit before starting another |
| Out of memory at start-up | close Chrome/Teams/HDevelop; VoiceDoc needs ~6 GB free RAM while loading |
| Command does nothing in note mode | is Ollama running? `ollama list` must show `qwen3:4b` |
| Anything else | `notes/voicedoc.log` |

## Accuracy: what to expect

Measured on five Tamil YouTube Shorts (`samples/testbed.txt`, `scripts/testbed.py`): Tamil transcription
**~12–20% character difference** from YouTube's own captions, **~1.3–2.5 s** from end of phrase to text on an RTX 3050.
English words, names and numbers inside Tamil come through well. The **translation is the weak step**: plain
speech translates well, while idioms, slang and film titles are often wrong. The original Tamil is always kept in the
transcript. Details: `PROJECT.md`, `samples/testbed_report.md`.

## For developers

```powershell
.venv\Scripts\python.exe -m pytest -q                              # 29 tests
.venv\Scripts\python.exe -m voicedoc notes\test.md --console       # run with console logging
.venv\Scripts\python.exe -m voicedoc notes\test.md --text          # type utterances instead of speaking
.venv\Scripts\python.exe scripts\testbed.py                        # accuracy/latency test bed on YouTube clips
```

Code map: `voicedoc/app.py` (controllers, tray app), `audio.py` (mic + VAD), `asr.py`, `translate.py`,
`document.py` (Markdown model + edit ops), `router.py`, `organizer.py` (Ollama), `desktop.py` (tray, hotkey,
overlay, typing, voice), `settings.py`. Research and model selection: `RECOMMENDATION.md`, `research/`.

## Licences

Code: yours. Models keep their own licences: Indic-Transcribe (Indic Open Model License, attribution; ask Bodhan
before hosting it for others), IndicTrans2 (MIT), Silero VAD (MIT), Qwen3 (Apache-2.0).
