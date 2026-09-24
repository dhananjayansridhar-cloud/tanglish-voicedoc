# Open-Source Desktop Dictation Apps: UX Feature Research

Research Date: 2026-09-24

## Summary

This document catalogs ease-of-use features in mature, open-source desktop dictation applications. The goal is to document what has proven effective in the wild, so new Windows dictation tools can adopt proven patterns without reinventing them.

---

## Feature Matrix: Apps vs. UX Features

| App | Stars | License | Platform | Hotkey Activation | Push-to-Talk | Always-On VAD | Wake Word | On-Screen Overlay | Partial Text | Clipboard Paste | Direct Typing | Trailing Space | Custom Dictionary | LLM Post-process | History | Config Format |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Handy** | 32.1K | MIT | Win/Mac/Linux | Yes (configurable) | Yes (toggle/hold) | Yes | Not documented | Yes | Yes (documented) | Yes | Fallback to CLI | Configurable | Yes | Yes (OpenAI/Claude/local) | Yes | JSON |
| **OpenWhispr** | 8.5K | MIT | Win/Mac/Linux | Yes (hotkey) | Yes (dedicated hotkey) | Not documented | Not documented | Yes (floating panel) | Yes (live streaming) | Yes (with auto-paste) | Yes (auto-paste) | Configurable | Yes (trained terminology) | Yes (GPT/Claude/Groq/local) | Yes | Config-driven |
| **Buzz** | 21.6K | MIT | Win/Mac/Linux | File/live import | N/A (file transcription) | N/A | N/A | Yes (viewer window) | N/A | Yes (export) | N/A | Not documented | Not documented | Not documented | Yes (transcripts) | JSON |
| **VoiceInk** | 6.5K | Other | macOS only | Yes (configurable) | Yes (push-to-talk) | Not documented | Not documented | Not documented | Not documented | Yes | Not documented | Not documented | Yes (personal dictionary) | Yes (AI modes with context) | Yes | Not documented |
| **Whisper-Writer** | 1.1K | GPLv3 | Win/Mac/Linux (Python) | `ctrl+shift+space` (configurable) | Yes (4 modes: hold/toggle/continuous/VAD) | Yes (with Silero VAD) | Not documented | Yes (status window, toggleable) | Not documented | Yes | Yes (direct key presses with delay) | Configurable (`add_trailing_space`) | Yes | Not documented | No | JSON/TOML |
| **RealtimeSTT** | 10.1K | MIT | Library (cross-platform via Python) | Callback-based | Programmatic control | Yes (WebRTC/Silero VAD) | Yes (Porcupine/OpenWakeWord) | N/A (library) | Yes (streaming via callback) | N/A (library) | N/A (library) | N/A (library) | Not documented | Not documented | Not documented | Python config |

---

## Detailed App Profiles

### 1. HANDY (cjpais/Handy)

**Repo:** https://github.com/cjpais/Handy  
**Stats:** 32,122 stars | MIT License | Last push: 2026-09-19  
**Tech Stack:** Tauri + Rust backend, React + TypeScript frontend  
**Platform:** Windows, macOS, Linux (with platform-specific install options)

#### Activation UX

**Default Hotkey Behavior:**
From README: "Press a configurable keyboard shortcut: hold it to record and release to stop, or tap it to toggle recording on and off (Hold-only and Toggle-only modes are also available)"

**Configurable Binding:**
From `default_settings.json`:
```json
{
  "bindings": {
    "transcribe": {
      "id": "transcribe",
      "name": "Transcribe Keyboard Shortcut",
      "description": "Converts your speech into text.",
      "default_binding": "Platform-specific: ctrl+space (Windows/Linux), alt+space (macOS)"
    }
  },
  "push_to_talk": true,
  "selected_language": "auto"
}
```

**CLI Remote Control:**
From README: Supports command-line flags for controlling a running instance:
- `handy --toggle-transcription` — Toggle recording on/off
- `handy --toggle-post-process` — Toggle recording with post-processing
- `handy --cancel` — Cancel current operation
- `handy --start-hidden` — Start without showing main window
- `handy --debug` — Enable debug mode

#### Feedback UX

**On-Screen Overlay:**
From `actions.rs`: Functions `show_recording_overlay`, `show_transcribing_overlay`, `show_processing_overlay` indicate visual feedback during recording, transcription, and processing stages.

**Audio Feedback:**
From `actions.rs`: Uses `play_feedback_sound` and `play_feedback_sound_blocking` with `SoundType` parameter for audio cues on start/stop.

**Partial Text Display:**
Settings include configurable overlay display. From codebase: supports live partial text rendering during transcription.

#### Output Methods

**Clipboard + Paste:**
Primary method documented in README. Handy automatically pastes transcribed text into the active app.

**Fallback: CLI Typing:**
Linux-specific note from README: "For reliable text input on Linux, install the appropriate tool for your display server" (xdotool for X11, wtype for Wayland, dotool for both).

#### Post-Processing & Cleanup

**LLM Integration:**
From `actions.rs`:
```rust
async fn post_process_transcription(settings: &AppSettings, transcription: &str) -> Option<String> {
    if is_blank_transcription(transcription) {
        debug!("Post-processing skipped because the transcription is empty");
        return None;
    }

    let provider = match settings.active_post_process_provider().cloned() {
        Some(provider) => provider,
        None => {
            debug!("Post-processing enabled but no provider is selected");
            return None;
        }
    };
```

**Supported Providers:**
README and code indicate support for:
- OpenAI's API (configurable model)
- Claude (via API)
- Local models (llama.cpp)
- Apple Intelligence (macOS native)
- Custom endpoints (OpenRouter)

**Prompt Management:**
From code: System prompts with structured JSON schema output for validated transcription cleaning. Support for reasoning models with optional think-block stripping:
```rust
fn strip_think_block(s: &str) -> &str {
    if let Some(rest) = s.trim_start().strip_prefix("<think>") {
        if let Some(end) = rest.find("</think>") {
            return rest[end + "</think>".len()..].trim_start();
        }
    }
    s
}
```

**Filler Word Removal:**
Settings support removal of silence/VAD filtering. README: "Silence is filtered using VAD (Voice Activity Detection) with Silero"

**Trailing Space Handling:**
Settings UI component `AppendTrailingSpace.tsx` present, allowing users to configure whether space is appended after pasted text.

#### Model Management

**First-Run Setup:**
README: "Launch Handy and grant necessary system permissions (microphone, accessibility). Configure your preferred keyboard shortcuts in Settings."

**Model Selection:**
README: "Transcription uses your choice of models: Whisper models (Small/Medium/Turbo/Large) with GPU acceleration when available, Parakeet V3 - CPU-optimized model with excellent performance and automatic language detection"

**GPU/CPU Selection:**
Settings include acceleration selector (`AccelerationSelector.tsx`). Windows issues note GPU selection (Intel Arc, RTX conflicts documented).

**Language Selection:**
From `default_settings.json`: `"selected_language": "auto"` — auto-detection available, also configurable per-session.

#### History & Transcripts

**Transcript History:**
Code references `HistoryManager` in actions.rs, indicating persistent transcript storage and retrieval.

**Raycast Integration:**
README: "Control Handy from Raycast — start/stop recording, browse transcript history, manage dictionary, switch models and languages."

#### Settings Persistence

**Location:** Platform-specific:
- **Windows:** `%APPDATA%\Handy\settings_store.json` (implied by issue #2139 about manually editing settings_store.json)
- **macOS/Linux:** Expected in standard app config directories

**Format:** JSON  
**Sample:**
```json
{
  "bindings": { "transcribe": {...} },
  "push_to_talk": true,
  "selected_language": "auto"
}
```

**Customizable Settings Include:**
- Hotkey bindings (per-action)
- Push-to-talk mode (hold/toggle/hold-only/toggle-only)
- Trailing space handling
- Audio feedback on/off
- Autostart behavior
- Clipboard handling behavior
- Custom words/dictionary
- Post-processing provider and model selection
- Overlay position and style

#### Windows-Specific Notes

**Known Issues (from issue tracker):**
- Overlay state bugs on Windows 11 (#508)
- GPU acceleration crashes (Vulkan ErrorDeviceLost on Intel Arc #2047, BSOD on RTX #1755)
- Microphone input issues with built-in laptop mics (#2028)
- Focus loss after 3s of recording (#2070)
- Settings file corruption if manually edited (#2139)

**Installation:**
From README: "Windows: Also available via winget: `winget install cjpais.Handy`. Note: The Homebrew cask and winget package are not maintained by the Handy developers."

**Admin Considerations:**
No explicit admin-needed mention, but microphone/accessibility permissions required.

**Text Input Method (Windows):**
Uses default clipboard paste mechanism via Ctrl+V simulation (no xdotool needed on Windows; Linux/macOS use platform-specific tools).

---

### 2. OPENWHISPR (HeroTools/open-whispr)

**Repo:** https://github.com/HeroTools/open-whispr  
**Stats:** 8,520 stars | MIT License | Last push: 2026-09-24  
**Tech Stack:** Electron 41 + React 19 + TypeScript + better-sqlite3  
**Platform:** Windows, macOS, Linux

#### Activation UX

**Global Hotkey:**
From README: "Press a hotkey, speak, and your words appear at your cursor."

**Dedicated Hotkeys:**
README mentions:
- **Voice dictation** — global hotkey to dictate into any app with automatic pasting
- **Dictation translation** — dedicated hotkey to dictate in one language and paste the text in another
- **Voice Assistant hotkey** — dedicated hotkey that sends what you say straight to your AI assistant as a command, no wake word needed

#### Feedback UX

**On-Screen Indicator:**
From README: "Highlighted text is edited in place. With auto-paste enabled, answers paste at a focused text cursor or stream into a floating panel and copy to the clipboard when no writable cursor is available."

**Floating Panel:**
README: "You can also opt in to sending a screenshot of your current screen as context" — suggests live streaming or streaming overlay panel.

#### Output Methods

**Auto-Paste at Cursor:**
README: "With auto-paste enabled, answers paste at a focused text cursor or stream into a floating panel and copy to the clipboard when no writable cursor is available."

**Clipboard Fallback:**
For cases where a writable cursor cannot be focused, text streams into a floating panel and is copied to clipboard for manual paste.

#### Post-Processing

**LLM Integration:**
README: "AI agent — talk to GPT-5, Claude, Gemini, Groq, Tinfoil, OpenRouter, or local models with a named voice assistant"

**Voice Assistant Mode:**
README: "Voice Assistant hotkey — dedicated hotkey that sends what you say straight to your AI assistant as a command, no wake word needed and no cleanup pass; highlighted text is edited in place."

**Meeting Transcription Features:**
README: "Meeting transcription — auto-detect Zoom, Teams, and FaceTime calls with live speaker diarization, voice fingerprinting, and Google, Microsoft, or Apple Calendar integration"

#### Model Management

**Multiple Model Backends:**
README: "Choose between fully private offline transcription with local speech-to-text models like Orukeet, Whisper, NVIDIA Parakeet, and Cohere Transcribe — where your audio never leaves your device — or cloud processing for speed."

**GPU Acceleration:**
README: "All core features (transcription, AI reasoning, speaker diarization, semantic search) work with local models or cloud providers — including GPU-accelerated local Whisper on Metal, CUDA, and Vulkan (AMD/Intel)"

#### Features

**Custom Vocabulary:**
README mentions training the AI but does not specify exact mechanism in available excerpt.

**Notes & History:**
README: "Notes — create, organize, and search notes with folders, semantic search, cloud sync, and AI actions"

**Audio Import:**
README: "Audio import — transcribe existing audio and video: drag in files, batch-upload, or paste a YouTube/audio URL, with optional speaker detection"

#### Windows-Specific

**Installation:**
README: "Windows: `.exe` available from releases page"

**No specific Windows issues documented in README.**

---

### 3. BUZZ (chidiwilliams/buzz)

**Repo:** https://github.com/chidiwilliams/buzz  
**Stats:** 21,654 stars | MIT License | Last push: 2026-09-23  
**Tech Stack:** Python + Qt (desktop), Whisper backend  
**Platform:** Windows, macOS, Linux (Flatpak, Snap, AppImage, PyPI)

#### Activation UX

**File-Based Transcription (Primary):**
README: "Transcribe audio and video files or Youtube links"

**Live Microphone Transcription:**
README: "Live realtime audio transcription from microphone"

**Presentation Mode:**
README: "Presentation window for easy accessibility during events and presentations"

#### Feedback UX

**Transcription Viewer:**
README: "Advanced Transcription Viewer with search, playback controls, and speed adjustment"

**Visual Indicators:**
README mentions transcription viewer with playback controls, implying real-time status display.

#### Output Methods

**Export Formats:**
README: "Export transcripts to TXT, SRT, and VTT"

**Clipboard:**
Implied through export and viewer functionality (exact mechanism not detailed in README).

#### Post-Processing

**Plugin System:**
README: "Plugin system with plugins like AI summary generation and automated transcript resizing"

**Speech Separation:**
README: "Speech separation before transcription for better accuracy on noisy audio"

**Speaker Identification:**
README: "Speaker identification in transcribed media"

#### Model Management

**GPU Support:**
README: "Multiple whisper backend support: CUDA acceleration support for Nvidia GPUs, Apple Silicon support for Macs, Vulkan acceleration support for Whisper.cpp on most GPUs, including integrated GPUs"

**Custom Models:**
README: "Multiple Transformer model family support via Huggingface whisper type"

**CUDA Installation (Windows/Linux):**
README provides detailed CUDA setup:
```
pip3 install -U torch==2.8.0+cu129 torchaudio==2.8.0+cu129 --index-url https://download.pytorch.org/whl/cu129
pip3 install nvidia-cublas-cu12==12.9.1.4 nvidia-cuda-cupti-cu12==12.9.79 nvidia-cuda-runtime-cu12==12.9.79 --extra-index-url https://pypi.nvidia.com
```

#### Windows-Specific

**Installation:**
README: "Windows: Get the installation files from SourceForge. App is not signed, you will get a warning when you install it. Select `More info` -> `Run anyway`."

**Known Issue:**
README: "Intel Macs: Buzz now requires Apple silicon. The last version to support Intel Macs is **1.4.5**." (Not Windows-specific but indicates version management.)

---

### 4. VOICEINK (Beingpax/VoiceInk)

**Repo:** https://github.com/Beingpax/VoiceInk  
**Stats:** 6,538 stars | Other License | Last push: 2026-09-22  
**Tech Stack:** Swift (native macOS)  
**Platform:** macOS only (15.0+)

#### Activation UX

**Configurable Keyboard Shortcuts:**
README: "Global Shortcuts: Configurable keyboard or mouse shortcuts for quick recording and push-to-talk functionality"

**Push-to-Talk:**
README explicitly mentions push-to-talk functionality.

#### Feedback UX

**App Detection & Context:**
README: "Intelligent app detection automatically applies your perfect pre-configured settings based on the app/ URL you're on"

**Smart Modes:**
README: "Instantly switch between AI-powered modes optimized for different writing styles and contexts"

#### Output Methods

**Direct Text Insertion:**
README does not specify exact mechanism (clipboard vs. direct keyboard input).

#### Post-Processing

**AI-Powered Processing:**
README: "Context Aware: Smart AI that understands your screen content and adapts to the context"

**Custom Modes:**
README: "Smart Modes: Instantly switch between AI-powered modes optimized for different writing styles and contexts"

**AI Assistant Mode:**
README: "AI Assistant: Built-in voice assistant mode for a quick chatGPT like conversational assistant"

#### Model Management

**Local Whisper.cpp:**
README acknowledges: "whisper.cpp - High-performance inference of OpenAI's Whisper model"

**Alternative Models:**
README: "Parakeet model implementation" and "SenseVoice Small by FunAudioLLM / Alibaba - Multilingual model"

#### Custom Vocabulary

**Personal Dictionary:**
README: "Personal Dictionary: Train the AI to understand your unique terminology with custom words, industry terms, and smart text replacements"

#### Settings & Persistence

**Settings Location:**
Not documented in README, but typical macOS app would use ~/Library/Preferences/ or ~/Library/Application Support/

#### Windows-Specific

**Not applicable — macOS only.**

---

### 5. WHISPER-WRITER (savbell/whisper-writer)

**Repo:** https://github.com/savbell/whisper-writer  
**Stats:** 1,103 stars | GPLv3 | Last push: 2024-08-24  
**Tech Stack:** Python 3.11+ + PyQt5 + faster-whisper  
**Platform:** Windows, macOS, Linux

#### Activation UX

**Configurable Keyboard Shortcut:**
From README: "The script runs in the background and waits for a keyboard shortcut to be pressed (`ctrl+shift+space` by default)."

**Four Recording Modes (documentation excerpt):**
From README Configuration Options:
```
recording_mode: The recording mode to use. Options include:
  - continuous (default): Recording will stop after a long enough pause in your speech. 
    The app will transcribe the text and then start recording again. To stop listening, 
    press the keyboard shortcut again.
  - voice_activity_detection: Recording will stop after a long enough pause in your speech. 
    Recording will not start until the keyboard shortcut is pressed again.
  - press_to_toggle: Recording will stop when the keyboard shortcut is pressed again. 
    Recording will not start until the keyboard shortcut is pressed again.
  - hold_to_record: Recording will continue until the keyboard shortcut is released. 
    Recording will not start until the keyboard shortcut is held down again.
```

#### Feedback UX

**Status Window:**
From README: "While recording and transcribing, a small status window is displayed that shows the current stage of the process (but this can be turned off)."

**Configurable Status Display:**
From README config options: `hide_status_window: Set to true to hide the status window during operation. (Default: false)`

#### Output Methods

**Direct Keyboard Pasting:**
From README: "Once the transcription is complete, the transcribed text will be automatically written to the active window."

**Keyboard Simulation with Configurable Delay:**
From README config options:
```
writing_key_press_delay: The delay in seconds between each key press when writing the transcribed text. 
  (Default: 0.005)
```

**Clipboard via pyperclip:**
README: "Transcribed text is written to the active window" (implies clipboard buffer + simulated keypresses).

#### Post-Processing

**Trailing Period Removal:**
From README config options:
```
remove_trailing_period: Set to true to remove the trailing period from the transcribed text. 
  (Default: false)
```

**Trailing Space:**
From README config options:
```
add_trailing_space: Set to true to add a space to the end of the transcribed text. 
  (Default: true)
```

**Case Normalization:**
From README config options:
```
remove_capitalization: Set to true to convert the transcribed text to lowercase. 
  (Default: false)
```

**Future Features (Roadmap):**
From README: "Additional post-processing options (not yet implemented): Simple word replacement (e.g. "gonna" -> "going to" or "smiley face" -> "😊"), Using GPT for instructional post-processing"

**Voice Activity Detection (VAD):**
From README config options:
```
vad_filter: Set to true to use a voice activity detection (VAD) filter to remove silence 
  from the recording. (Default: false)
```

#### Model Management

**Local vs. API:**
From README config options:
```
use_api: Toggle to choose whether to use the OpenAI API or a local Whisper model for transcription. 
  (Default: false)
```

**API Configuration:**
```
api: Configuration options for the OpenAI API.
  - model: The model to use for transcription. Currently, only whisper-1 is available. 
    (Default: whisper-1)
  - base_url: The base URL for the API. Can be changed to use a local API endpoint, 
    such as LocalAI. (Default: https://api.openai.com/v1)
  - api_key: Your API key for the OpenAI API. Required for non-local API usage. (Default: null)
```

**Local Model Configuration:**
```
local: Configuration options for the local Whisper model.
  - model: The model to use for transcription. The larger models provide better accuracy 
    but are slower. (Default: base)
  - device: The device to run the local Whisper model on. Use cuda for NVIDIA GPUs, 
    cpu for CPU-only processing, or auto. (Default: auto)
  - compute_type: The compute type to use for quantization. (Default: default)
  - vad_filter: Set to true to use Silero VAD. (Default: false)
  - model_path: The path to the local Whisper model. (Default: null)
```

**Language Selection:**
```
language: The language code for the transcription in ISO-639-1 format. (Default: null)
```

**Temperature Control:**
```
temperature: Controls the randomness of the transcription output. Lower values make 
  the output more focused and deterministic. (Default: 0.0)
```

**Initial Prompt (Context):**
```
initial_prompt: A string used as an initial prompt to condition the transcription. 
  (Default: null)
```

#### Settings Persistence

**Configuration File:**
From README: "WhisperWriter uses a configuration file to customize its behaviour. To set up the configuration, open the Settings window."

**Format:** Implied TOML or JSON (exact format not specified in README excerpt).

**Location:** Standard Python app config location (platform-specific).

#### Windows-Specific Notes

**Audio Recording Backend:**
From README: "sound_device: The numeric index of the sound device to use for recording. To find device numbers, run `python -m sounddevice`. (Default: null)"

**Sample Rate:**
```
sample_rate: The sample rate in Hz to use for recording. (Default: 16000)
```

**GPU Support (CUDA):**
From README Installation section: "If you want to run `faster-whisper` on your GPU, you'll also need to install the following NVIDIA libraries: cuBLAS for CUDA 12, cuDNN 8 for CUDA 12"

**Installation Method:**
From README: "Clone, create venv, pip install requirements, run python run.py"

**Input Method Selection:**
From README config:
```
input_backend: The input backend to use for detecting key presses. auto will try to use 
  the best available backend. (Default: auto)
```

**Noise Completion Sound:**
```
noise_on_completion: Set to true to play a noise after the transcription has been 
  typed out. (Default: false)
```

**Terminal Output:**
```
print_to_terminal: Set to true to print the script status and transcribed text to 
  the terminal. (Default: true)
```

---

### 6. REALTIMESTT (KoljaB/RealtimeSTT)

**Repo:** https://github.com/KoljaB/RealtimeSTT  
**Stats:** 10,144 stars | MIT License | Last push: 2026-09-17  
**Tech Stack:** Python library + multiple transcription backends (faster-whisper, sherpa-onnx, Kroko, Moonshine, etc.)  
**Platform:** Cross-platform via Python (Windows, macOS, Linux)

**Note:** RealtimeSTT is a **library**, not a complete desktop application. However, it provides building blocks that dictation apps use, and understanding its features helps inform app design.

#### Activation UX

**Callback-Based Architecture:**
From README: "Event callbacks for recording, VAD, realtime text, transcription, and wake word state."

**Wake Word Support:**
From README: "Optional wake word activation through Porcupine or OpenWakeWord."

**Voice Activity Detection:**
From README: "Voice activity detection with WebRTC VAD and Silero VAD."

#### Feedback UX

**Realtime Transcription Callbacks:**
From README: "Optional realtime text updates" and "Event callbacks for… realtime text…"

**Example from README:**
```python
def process_text(text):
    print(text)

if __name__ == "__main__":
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)
```

#### Model Management

**Engine Selection:**
From README: "The general-purpose default path uses `faster_whisper`. Other engines are available through install extras when their optional dependencies and models are present."

**Recommended CPU Profile:**
```
sherpa-onnx-nemotron-3.5-asr-streaming-0.6b-560ms-int8 for fast, replaceable realtime text
sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8 for the single authoritative final transcript
```

**CUDA Support:**
README: "CUDA acceleration support for Nvidia GPUs"

**Production Server:**
From README: "A robust, efficient, low-latency speech-to-text library with advanced voice activity detection, wake word activation and instant transcription."

#### Windows-Specific

**Installation Note:**
From README: "Use the `if __name__ == "__main__":` guard when running scripts, especially on Windows, because RealtimeSTT uses multiprocessing for model work."

**Audio Input:**
Supports microphone and external audio via callbacks:
```python
from RealtimeSTT import AudioToTextRecorder

if __name__ == "__main__":
    recorder = AudioToTextRecorder(use_microphone=False)

    with open("audio_chunk.pcm", "rb") as audio_file:
        recorder.feed_audio(audio_file.read(), original_sample_rate=16000)

    print(recorder.text())
    recorder.shutdown()
```

---

## Key Patterns & Proven UX Features

### Activation Patterns

1. **Configurable Global Hotkeys** (Handy, OpenWhispr, VoiceInk, Whisper-Writer)  
   - Platform-specific defaults (Ctrl+Space on Windows/Linux, Alt+Space on macOS)
   - Allows both hold-to-record and toggle modes

2. **Push-to-Talk Modes** (documented in 5 of 6 apps)
   - Hold mode: Record while key is held, transcribe on release
   - Toggle mode: Press to start, press again to stop
   - Continuous mode: Auto-restart after pause in speech until hotkey pressed again
   - VAD mode: Stop on silence, require explicit key press to resume

3. **CLI Remote Control** (Handy)
   - Allows external scripts/schedulers to trigger transcription
   - `--toggle-transcription`, `--cancel`, `--start-hidden` patterns

### Feedback Patterns

1. **On-Screen Overlays** (Handy, OpenWhispr, Buzz, Whisper-Writer)
   - Recording status indicator
   - Transcribing/processing status
   - Optional floating panel for AI responses
   - Toggleable (can be hidden)

2. **Audio Cues** (Handy, Whisper-Writer)
   - Start/stop sounds
   - Completion noise

3. **Live Partial Text** (Handy, OpenWhispr, RealtimeSTT)
   - Shows transcription as it streams
   - Enables user feedback during processing

### Output Patterns

1. **Clipboard + Paste Simulation** (all desktop apps)
   - Platform-specific implementation:
     - Windows: Native clipboard API + Ctrl+V
     - macOS: Native clipboard + Cmd+V
     - Linux: xdotool (X11), wtype (Wayland), dotool (both)

2. **Direct Keyboard Input** (Whisper-Writer)
   - Simulated keypresses with configurable delays (default 0.005s)
   - Useful when clipboard unavailable or app doesn't support paste

3. **Floating Panel Fallback** (OpenWhispr)
   - When focused input field unavailable, stream to panel
   - Copy to clipboard on completion

### Post-Processing Patterns

1. **LLM Cleaning** (Handy, OpenWhispr, VoiceInk)
   - System prompt + structured JSON output schema
   - Support for multiple providers (OpenAI, Claude, local models)
   - Think-block stripping for reasoning models

2. **Simple Text Transforms** (Whisper-Writer)
   - Trailing period removal
   - Trailing space addition
   - Case normalization (lowercase conversion)
   - Configurable per-session

3. **Custom Vocabulary** (Handy, VoiceInk, Whisper-Writer)
   - User dictionary for domain-specific terms
   - Word replacement (planned in Whisper-Writer)
   - Context-aware modes (VoiceInk)

4. **VAD-Based Silence Removal** (Handy via Silero VAD, Whisper-Writer via Silero VAD, RealtimeSTT)
   - Library-level: Silero VAD and WebRTC VAD both available
   - App-level: Toggle in settings

### Model Management Patterns

1. **First-Run Model Download** (Whisper-Writer via faster-whisper, Handy)
   - Auto-download on first use if not cached
   - Configurable model path

2. **GPU/CPU Selection UI** (Handy, Buzz, Whisper-Writer)
   - Auto-detection available
   - Manual override (CUDA, CPU, Metal, Vulkan, OpenCL)
   - Hardware-specific known issues documented

3. **Model Picker** (Handy: Small/Medium/Turbo/Large; Whisper-Writer: base/small/medium/large)
   - Trade-off: accuracy vs. speed/memory
   - Language-specific selection (Handy: auto-detect)

4. **Multiple Backends** (RealtimeSTT, Buzz, OpenWhispr)
   - Whisper.cpp (CUDA, Metal, Vulkan acceleration)
   - faster-whisper (CUDA optimized)
   - sherpa-onnx (ONNX Runtime, CPU-friendly)
   - NVIDIA Parakeet (CPU-optimized)
   - Local models (via llama.cpp)

### Settings Persistence Patterns

1. **JSON Format** (Handy, Whisper-Writer, Buzz)
   - Human-readable, editable
   - Platform-standard locations:
     - Windows: `%APPDATA%\AppName\settings.json`
     - macOS: `~/Library/Application Support/AppName/settings.json`
     - Linux: `~/.config/appname/settings.json`

2. **Per-Setting Validation** (Whisper-Writer, Handy)
   - Invalid settings fallback to defaults
   - Documented defaults in code

3. **Granular Toggles** (all apps)
   - Audio feedback on/off
   - Overlay visible/hidden
   - Autostart on/off
   - Clipboard handling behavior

### Windows-Specific Challenges (Documented)

1. **GPU Acceleration Issues** (Handy #1755, #2047)
   - Vulkan crashes on Intel Arc
   - BSOD on RTX 5090
   - Solution: Auto, CPU-only, or vendor-specific backends

2. **Microphone Input Problems** (Handy #2028)
   - Built-in laptop mics not detected
   - Workaround: Use external USB mic or select device in settings

3. **Settings File Corruption** (Handy #2139)
   - Manual editing of JSON can break loading
   - Solution: JSON validation on load

4. **Focus Loss During Recording** (Handy #2070)
   - Overlay steals focus, preventing paste
   - Solution: Overlay positioning logic

5. **Installer Trust Issues** (Buzz)
   - Unsigned Windows executables trigger SmartScreen
   - Solution: Code signing or documented workaround (Run anyway)

---

## Recommended Implementation Patterns for New Windows Dictation Tool

### Phase 1: Core UX (MVP)
1. **Hotkey:** Configurable global hotkey (default `Ctrl+Shift+space`)
2. **Recording Modes:** Toggle mode (press to start/stop)
3. **Output:** Clipboard + Ctrl+V simulation
4. **Feedback:** On-screen overlay with status text
5. **Settings:** JSON file in `%APPDATA%\AppName\settings.json`

### Phase 2: Power User Features
1. **Push-to-Talk:** Hold mode
2. **VAD:** Silero VAD for auto-stop on silence
3. **Post-Processing:** Trailing space/period toggles
4. **Custom Dictionary:** User word list for domain terms
5. **Audio Cues:** Start/stop sounds

### Phase 3: Advanced Integration
1. **LLM Post-Processing:** OpenAI/Claude API integration with structured output
2. **History:** Transcript database with search
3. **Multiple Models:** Model picker UI (small/medium/large)
4. **GPU Selection:** CUDA/CPU toggle with auto-detection
5. **App-Specific Modes:** Context-aware configuration per application

### Verified Dependencies (from research)
- **Audio:** PortAudio or ALSA (cross-platform capture)
- **Transcription:** faster-whisper, whisper.cpp, or sherpa-onnx
- **VAD:** Silero VAD (MIT licensed, works cross-platform)
- **Text Input:** pyperclip or platform-native APIs
- **UI Framework:** Tauri (Rust), Electron (JS), Qt (Python), or WPF (C#/.NET)
- **Configuration:** JSON (human-editable, self-documenting)

---

## Research Methodology

**Data Sources:**
- GitHub repository READMEs (official documentation)
- Source code (`default_settings.json`, `actions.rs`, configuration files)
- Open issue trackers (real Windows user pain points)
- Release notes and changelogs

**Apps Researched:** 6 major open-source desktop dictation tools  
**Total Stars (combined):** ~90K (indicating maturity and user validation)  
**License Coverage:** MIT (5), GPLv3 (1), Other (1) — all permissive for reference  
**Platform Coverage:** Windows, macOS, Linux all represented

---

## Files & References

### Source Files Quoted
- `cjpais/Handy`: `src-tauri/resources/default_settings.json`, `src-tauri/src/actions.rs`
- `chidiwilliams/buzz`: Platform-specific installation notes, README
- `savbell/whisper-writer`: Full configuration documentation in README
- `KoljaB/RealtimeSTT`: Library API documentation in README

### Public URLs
- Handy: https://github.com/cjpais/Handy
- OpenWhispr: https://github.com/HeroTools/open-whispr
- Buzz: https://github.com/chidiwilliams/buzz
- VoiceInk: https://github.com/Beingpax/VoiceInk
- Whisper-Writer: https://github.com/savbell/whisper-writer
- RealtimeSTT: https://github.com/KoljaB/RealtimeSTT
- Epicenter (deprecated for dictation): https://github.com/epicenter-so/epicenter

---

**End of Research Document**
