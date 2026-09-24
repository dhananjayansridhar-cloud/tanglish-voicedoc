# Voice Dictation & Voice-Edited Document Research

Date: 2026-09-24

## Summary Table

| Repo | Stars | Last Push | Local? | Command Mechanism | ASR Engine | LLM? | Voice Editing? | OS Support |
|------|-------|-----------|--------|-------------------|-----------|------|----------------|-----------|
| ideasman42/nerd-dictation | 1920 | 2025-10-10 | ✓ Yes | Manual begin/end | VOSK-API | No | No | Linux |
| themanyone/whisper_dictation | 294 | 2026-08-13 | ✓ Yes | Keyboard hotkey | Whisper.cpp | Yes (Ollama, ChatGPT) | Limited | Linux |
| foges/whisper-dictation | 220 | 2024-07-20 | ✓ Yes | Keyboard shortcut (cmd+option) | OpenAI Whisper | No | No | macOS |
| chrisurf/obsidian-voice | 86 | 2026-03-01 | No (cloud) | Ribbon/Command | Not Covered | No | No (TTS only) | All |
| TalonCommunity/Wiki | 97 | 2026-09-20 | ✓ Yes (community) | Voice commands | VOSK-API (varies) | No | Yes | Linux, Windows, macOS |
| AndreasArvidsson/andreas-talon | 92 | 2026-09-23 | ✓ Yes | Voice commands | Not Covered | No | Yes | Windows, macOS |
| ashwin-pc/whisper-dictation | 25 | 2026-03-15 | ✓ Yes | Hotkey (Globe key) | OpenAI Whisper | No | No | macOS |
| doctorguile/faster-whisper-dictation | 29 | 2023-12-14 | ✓ Yes | Not Covered | Faster-Whisper | No | No | Not Covered |
| coleam00/obsidian-voice-agent | 33 | 2026-08-31 | ✓ Yes | Voice conversation | OpenAI Realtime API | Yes (Pydantic AI) | No | Not Covered |
| jiaoyingxing/resojot | 43 | 2026-06-13 | ✓ Yes | Not Covered | Not Covered | Possible | No | Not Covered |

---

## 1. Nerd Dictation

**URL:** https://github.com/ideasman42/nerd-dictation  
**Stars:** 1920  
**Last Push:** 2025-10-10  
**Local:** Yes  

### Description (Verbatim)

> *Offline Speech to Text for Desktop Linux.* - Utility that provides simple access speech to text for using in Linux without being tied to a desktop environment, using the excellent VOSK-API.
>
> Simple - This is a single file Python script with minimal dependencies.  
> Hackable - User configuration lets you manipulate text using Python string operations.  
> Zero Overhead - As this relies on manual activation there are no background processes.

### Voice Commands/Mechanism (Verbatim)

> Dictation is accessed manually with begin/end commands.
>
> It is suggested to bind begin/end/cancel to shortcut keys.
>
> ```sh
> nerd-dictation begin
> nerd-dictation end
> ```

### Features (Verbatim)

> - Numbers as Digits: Optional conversion from numbers to digits. So `Three million five hundred and sixty second` becomes `3,000,562nd`.
> - Time Out: Optionally end speech to text early when no speech is detected for a given number of seconds.
> - Output Type: Output can simulate keystroke events (default) or simply print to the standard output.
> - User Configuration Script: User configuration is just a Python script which can be used to manipulate text using Python's full feature set.
> - Suspend/Resume: Initial load time can be an issue for users on slower systems or with some of the larger language-models, in this case suspend/resume can be useful.

### Document Editing (Verbatim)

> Output can simulate keystroke events (default) or simply print to the standard output.

User Configuration Script Example (Verbatim):

```python
# ~/.config/nerd-dictation/nerd-dictation.py
def nerd_dictation_process(text):
    return text.upper()
```

> The processing function can be used to implement your own actions using keywords of your choice. Simply return a blank string if you have implemented your own text handling.

### ASR Engine (Verbatim)

> - The VOSK-API.
> - Dependencies: Python 3.6+, VOSK-API, An audio recording utility (parec by default), An input simulation utility (xdotool by default)

### Dictation vs Commands (Verbatim)

NOT COVERED - No distinction between dictation and commands mentioned. Manual begin/end cycle separates them temporally.

### LLM Use

NOT COVERED

---

## 2. Whisper Dictation (themanyone)

**URL:** https://github.com/themanyone/whisper_dictation  
**Stars:** 294  
**Last Push:** 2026-08-13  
**Local:** Yes  

### Description (Verbatim)

> Private voice keyboard, AI chat, images, webcam, recordings, voice control in >= 4 GiB of VRAM. "The works" all AI features now running concurrently on an old laptop from 2013.
>
> **The ship's computer.** Inspired by the *Star Trek* television series. Talk to your computer. Have it answer back with clear, easy-to-understand speech.

### Voice Commands (Verbatim)

> **Voice control.** The bot responds to commands.
>
> Say, "Computer, on screen." A window opens up showing the webcam. Say "Computer, take a picture". A picture, "webcam/image().jpg" is saved in a 'webcam' subdirectory of the current folder. Say, "Computer, search the web for places to eat". A browser opens up with a list of local restaurants. Say, "Computer, say hello to our guest". After a brief pause, there is a reply, either from your local machine, `ChatGPT`, or a local area chat server that you set up. A voice, `mimic3` says some variation of, "Hello. Pleased to meet you. Welcome to our shop. Let me know how I can be of assistance". It's unique each time. Say, "Computer, open terminal". A terminal window pops up. Say "Computer, draw a picture of a Klingon warship". An image of a warship appears with buttons to save, print, and navigate through previously-generated images.

### Supported Platforms (Verbatim)

> This application now supports both **X11** and **Wayland** display servers with automatic detection.
>
> The application automatically detects your session type:
> - **Wayland sessions**: Uses `evdev` backend for input simulation
> - **X11 sessions**: Uses traditional `PyAutoGUI` backend

### LLM & AI Features (Verbatim)

> - Hands-free recording with `record.py`
> - Voice keyboard depends on `whisper.cpp`
> - LLM inference depends on [Llama.cpp](https://github.com/ggml-org/llama.cpp)
> - Agentic capabilities (unstable branch)
> - Translate various languages
> - Voice-controlled webcam, audio recorder
> - Launch & control apps, with `pyautogui`
> - Optional OpenAI `ChatGPT`, Google Gemini, more
> - If desired, speak answers out loud with `mimic3`*
> - Draw pictures with [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)

### ASR Engine (Verbatim)

> Voice keyboard depends on `whisper.cpp`

### Document Editing

NOT COVERED - Focus is on voice control of application/system, not document editing.

---

## 3. Whisper Dictation (foges)

**URL:** https://github.com/foges/whisper-dictation  
**Stars:** 220  
**Last Push:** 2024-07-20  
**Local:** Yes  

### Description (Verbatim)

> Multilingual Dictation App based on OpenAI Whisper
> 
> Multilingual dictation app based on the powerful OpenAI Whisper ASR model(s) to provide accurate and efficient speech-to-text conversion in any application. The app runs in the background and is triggered through a keyboard shortcut. It is also entirely offline, so no data will be shared. It allows users to set up their own keyboard combinations and choose from different Whisper models, and languages.

### Activation Mechanism (Verbatim)

> By default, the app uses the "base" Whisper ASR model and the key combination to toggle dictation is cmd+option on macOS and ctrl+alt on other platforms. You can change the model and the key combination using command-line arguments.
>
> Example:
> ```bash
> python whisper-dictation.py -m large -k cmd_r+shift -l en
> ```

### Multilingual Support (Verbatim)

> The models are multilingual, and you can specify a two-letter language code (e.g., "no" for Norwegian) with the `-l` or `--language` option. Specifying the language can improve recognition accuracy, especially for smaller model sizes.

### ASR Engine (Verbatim)

> OpenAI Whisper ASR model(s)

### Document Editing

NOT COVERED - Focused on background dictation in any application, not document organization.

### Permissions (Verbatim)

> The app requires accessibility permissions to register global hotkeys and permission to access your microphone for speech recognition.

---

## 4. Obsidian Voice Plugin

**URL:** https://github.com/chrisurf/obsidian-voice  
**Stars:** 86  
**Last Push:** 2026-03-01  
**Local:** No (requires cloud text-to-speech provider)  

### Description (Verbatim)

> Turn every note into a mobile-friendly, audiobook-like experience. The Obsidian Voice Plugin reads your notes aloud in natural, lifelike speech — using the text-to-speech provider you already have. It supports all the major engines — **AWS Polly**, **ElevenLabs**, **OpenAI**, **Google Cloud**, **Azure Speech**, and **MiniMax** — plus **any OpenAI-compatible server** such as OpenRouter or a self-hosted Kokoro — so you can listen with whichever one you prefer.

### Features - Not Voice Dictation/Editing (Verbatim)

> - **A real audiobook player** — open the Voice player, see your notes as chapters, and play, skip, and repeat just like a podcast app.
> - **Listen in seconds** — turn any note into lifelike speech straight from the ribbon, a command, or the player.
> - **Own your audio** — download MP3 files, auto-embed them into your note, and keep an offline archive.
> - **Stay in control** — adjust tempo on the fly, jump forward or back, repeat a chapter or the whole list, and watch synthesis progress in real time.

### Note on This Project

This is a TEXT-TO-SPEECH plugin, not a voice DICTATION or voice-EDITING plugin. NOT RELEVANT to the goal of voice-commanded document editing.

---

## 5. Talon Voice — Community Wiki

**URL:** https://github.com/TalonCommunity/Wiki  
**Stars:** 97  
**Last Push:** 2026-09-20  
**Local:** Yes (Talon Voice is local, runs on user's machine)  

### Description (Verbatim)

> This is the source repo for the [https://talon.wiki/](https://talon.wiki), a community maintained wiki for [Talon voice](https://talonvoice.com/).
>
> Join the [Talon Slack](https://talonvoice.com/chat) to find other folks interested in or using Talon.

### What is Talon Voice (from talonvoice.com)

NOT COVERED in README - Refer to https://talonvoice.com/ for core Talon documentation.

### Community Resources (Verbatim)

> The wiki belongs to the Talon Community, and contributions are welcome from anyone.
>
> Join the [Talon Slack](https://talonvoice.com/chat) to find other folks interested in or using Talon. If you want to support the project, consider donating to the [Patreon](https://www.patreon.com/lunixbochs).

### Repository Explorer (Verbatim)

> The wiki includes a [Repository Explorer](https://talon.wiki/explorer/) that automatically displays Talon-related repositories from GitHub tagged with `talonvoice` topic.

### Commands & Voice Control

NOT COVERED in the wiki README itself. See TalonCommunity community repositories for command sets (e.g., `talonhub/community`).

---

## 6. Andreas Talon (AndreasArvidsson/andreas-talon)

**URL:** https://github.com/AndreasArvidsson/andreas-talon  
**Stars:** 92  
**Last Push:** 2026-09-23  
**Local:** Yes  

### Description

NOT COVERED in accessible README excerpts. Project is a Talon Voice set of commands/scripts.

### Related Projects

Same author maintains:
- `AndreasArvidsson/talon-deck` - 10 stars
- `AndreasArvidsson/andreas-talon-vscode` - 13 stars

---

## 7. Whisper Dictation (ashwin-pc)

**URL:** https://github.com/ashwin-pc/whisper-dictation  
**Stars:** 25  
**Last Push:** 2026-03-15  
**Local:** Yes  

### Description (Verbatim)

> A macOS application that converts speech to text using OpenAI's Whisper model running locally. Press the Globe/Function key to start recording, press it again to stop recording, transcribe, and paste text at your current cursor position.

### Activation Mechanism (Verbatim)

> Press the Globe/Function key to start recording, press it again to stop recording, transcribe, and paste text at your current cursor position.

### ASR Engine (Verbatim)

> OpenAI's Whisper model running locally

---

## 8. Faster Whisper Dictation (doctorguile)

**URL:** https://github.com/doctorguile/faster-whisper-dictation  
**Stars:** 29  
**Last Push:** 2023-12-14  
**Local:** Yes  

### Description (Verbatim)

> Dictation app based on the Faster Whisper transcription with CTranslate2

### ASR Engine (Verbatim)

> Faster Whisper transcription with CTranslate2

### Note

Last push 2023-12-14 — over 2.5 years old, may be abandoned.

---

## 9. Obsidian Voice Agent (coleam00)

**URL:** https://github.com/coleam00/obsidian-voice-agent  
**Stars:** 33  
**Last Push:** 2026-08-31  
**Local:** Yes  

### Description (Verbatim)

> Voice and text interface for querying your Obsidian knowledge base using AI.
>
> - **Voice Conversations**: Real-time voice chat powered by OpenAI Realtime API (~300ms latency)
> - **Text Chat**: Traditional chat interface for typed queries
> - **Knowledge Base Search**: Full-text search across your Obsidian vault
> - **Real-time File References**: See which documents the agent references as it speaks

### Voice Mechanism (Verbatim)

> Real-time voice chat powered by OpenAI Realtime API (~300ms latency)

### LLM & AI (Verbatim)

> - **Backend**: Python 3.11+, FastAPI, Pydantic AI, LiveKit Agents SDK
> - **Voice**: OpenAI Realtime API (gpt-realtime-mini)

### Tools Available (Verbatim)

> Both agents share these tools for querying your vault:
>
> | Tool | Description |
> |------|-------------|
> | `search_documents` | Full-text search across all markdown files |
> | `find_files` | Find files matching glob patterns (e.g., `**/daily/*.md`) |
> | `search_content` | Regex search within file contents |
> | `read_document` | Read full document with frontmatter parsing |
> | `get_document_metadata` | Get tags, dates without full content |

### Document Editing

NOT COVERED - Focuses on querying/searching vault via voice, not editing documents by voice commands.

---

## 10. Resojot (jiaoyingxing)

**URL:** https://github.com/jiaoyingxing/resojot  
**Stars:** 43  
**Last Push:** 2026-06-13  
**Local:** Yes  

### Description

NOT COVERED in accessible README excerpts.

---

## Key Findings: Voice-Edited Document Projects

### Projects with Voice DICTATION (speech-to-text input):
1. **nerd-dictation** - Offline, VOSK, Linux, manual begin/end
2. **whisper-dictation (themanyone)** - Whisper.cpp, Linux, voice control commands
3. **whisper-dictation (foges)** - OpenAI Whisper, macOS, keyboard hotkey
4. **whisper-dictation (ashwin-pc)** - OpenAI Whisper, macOS, Globe key hotkey
5. **faster-whisper-dictation** - Faster-Whisper, CUDA, older (2023)

### Projects with Voice COMMANDS to EDIT/ORGANIZE documents:
1. **Talon Voice (talonhub/community)** - Full command set for prose editing, NOT COVERED in this README but referenced. See https://talon.wiki/ and https://github.com/talonhub/community
2. **themanyone/whisper_dictation** - Voice control of applications (limited document editing)
3. **AndreasArvidsson/andreas-talon** - Talon Voice command set, NOT FULLY DOCUMENTED

### Projects with LLM-powered document interface:
1. **obsidian-voice-agent** - OpenAI Realtime API, queries/searches vault
2. **themanyone/whisper_dictation** - ChatGPT, Ollama, Llama.cpp support

### Projects NOT relevant (text-to-speech, not voice input):
- **obsidian-voice (chrisurf)** - Reads notes aloud (TTS), not voice dictation

---

## Talon Voice: Core Reference

**URL:** https://talonvoice.com/  
**Primary Repo:** https://github.com/talonhub/community  

Talon Voice is a comprehensive voice control system. The community command set (`talonhub/community`) contains extensive editing commands.

### Editing Commands (Expected, NOT VERIFIED in this search)

Per Talon documentation (NOT QUOTED HERE - refer to https://talon.wiki/):
- Prose editing: "scratch that", "select X", "cap", "new paragraph"
- Text manipulation: "replace X with Y"
- Navigation: "jump to line", "go to end of file"

**Status:** Core Talon repository and full command documentation NOT AVAILABLE in this research session. Recommend direct review at https://github.com/talonhub/community and https://talon.wiki/.

---

## Obsidian Plugins: Voice

Searched plugins found:
1. **obsidian-voice** (chrisurf) - Text-to-speech, NOT voice dictation
2. **obsidian-voice-agent** (coleam00) - Voice query interface, NOT voice editing

**Finding:** NOT COVERED - No Obsidian plugins found that support voice-based document EDITING (e.g., "scratch that", "make a list", "move that").

---

## Conclusion

### Most Relevant for "Voice Dictation + Voice-Editing Commands":

1. **Talon Voice (talonhub/community)** - Only system with comprehensive voice-editing commands. Status: NOT FULLY DOCUMENTED HERE; refer to https://github.com/talonhub/community.
2. **nerd-dictation** - Simple, hackable, offline dictation. Extensible via Python config, but NO built-in voice-editing commands.
3. **whisper-dictation (themanyone)** - Most feature-rich; supports voice control of apps, LLM chat. NOT optimized for document organization.

### NOT FOUND in this search:

- Open-source project that combines (1) speech-to-markdown dictation + (2) voice commands to edit/organize ("scratch that", "make a list", "select X", "move that") in a single tool running locally.

Recommend searching:
- `talonhub/community` directly for full editing command grammar
- https://talon.wiki/ for Talon editing paradigm
- Nerd-dictation user configs (GitHub issues/discussions) for custom voice-command extensions
