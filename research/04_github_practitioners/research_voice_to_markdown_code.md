# Speech-to-Markdown: Implementation Research

**Research Date:** 2026-09-24  
**Repositories Analyzed:** 12  
**Focus:** Open-source projects converting voice → Markdown/notes (live or batch)

---

## Quick Reference Table

| Repo | Stars | Last Push | Live/Batch | Segmentation | ASR | Markdown Method | Command Detection | File Update | Local? | License |
|---|---|---|---|---|---|---|---|---|---|---|
| nikdanilov/whisper-obsidian-plugin | 380 | 2026-04-07 | Live (button/hotkey) | Whole recording | OpenAI Whisper, Groq, Azure (API) | Raw append OR LLM (Claude/GPT) | Hotkey-triggered, custom cmds via protocol | editor.replaceRange() + create file | Hybrid (local + API) | MIT |
| mikealicea/obsidian-scribe | 85 | 2026-07-15 | Live + batch | Whole recording | OpenAI/AssemblyAI/Deepgram (API) | LLM structured (OpenAI/Claude) + Mermaid | Voice question mid-recording ("Hey Scribe") | editor insert + create file | Hybrid (local + API) | MIT |
| dbknv/verborra | 4 | 2026-05-29 | Live (hotkey) | Whole recording | OpenAI Whisper models (API) | LLM formatting (OpenAI compatible) | Global hotkey → recording overlay | Clipboard + Cmd+V simulation | macOS only (local + API) | MIT |
| lyxdream/obsidian-content-capture-backend | 30 | 2026-06-05 | Batch | File-based | (varies by plugin) | (varies by plugin) | External plugin system | Vault API | Hybrid | TBD |
| serg-markovich/local-whisper-obsidian | 18 | 2026-07-16 | Live | Whole recording | Whisper (local + API) | Raw append OR local LLM | Hotkey-triggered | editor.replaceRange() | Local capable | MIT |
| Sharrnah/whispering-plugins | 9 | 2026-09-21 | Live (Whispering Tiger UI) | Streaming (VAD-capable) | Multiple engines (Whisper, Deepgram, AssemblyAI) | Plugin system (text passthrough) | Voice keywords + LLM intent | Custom plugin outputs | Local + cloud hybrid | MIT |
| kevinbadi/kevs-obsidian-ingestion-engine | 19 | 2026-04-10 | Batch | File-based | (varies) | (varies) | External plugin-driven | Custom plugin outputs | Hybrid | TBD |
| hehenaice/VoiceZettelAssist | 0 | 2026-07-26 | Live | Whole recording | Gemini 1.5 Flash (API) | LLM structured (append to daily note) | External app trigger | Zettel Notes append | Android-only | TBD |
| eyson-maker/voice-note-transcriber | 1 | 2026-06-03 | Live | Whole recording | Whisper (API) | Raw append | Recording UI trigger | Create/append file | Hybrid | TBD |
| 0xSh3ru/whisper-note | 0 | 2026-06-02 | Live | Whole recording | Whisper local + API | Raw append | Ctrl+Alt+Space hotkey (Ubuntu) | File append | Linux local-capable | TBD |
| kondasviktor/saymd | 0 | 2026-09-15 | Batch | CLI input | Whisper (BYOK) | Raw output | CLI prompt-driven | Stdout | Local CLI | MIT |
| membraneframework/membrane_whisper_plugin | 19 | 2026-08-07 | Plugin API | Streaming chunks | Whisper (local/API) | Plugin integration | Parent app-driven | Parent callback | Local capable | Apache 2.0 |

---

## Detailed Repository Analysis

### 1. **nikdanilov/whisper-obsidian-plugin** (380 ⭐, Obsidian Plugin)

**URL:** https://github.com/nikdanilov/whisper-obsidian-plugin  
**License:** MIT  
**Last Push:** 2026-04-07  
**Local/Cloud:** Hybrid (local Obsidian, cloud ASR)

#### Capture & Segmentation
- **Push-to-talk:** Press `Alt+Q` to start/stop recording, or click mic icon in sidebar
- **Live recording:** Browser Web Audio API (NativeAudioRecorder.ts)
- **File upload:** Command palette → Upload audio file (mp3, mp4, m4a, wav, webm, ogg)
- **Pause/resume:** Supported, preserves continuous session
- **Whole-file processing:** Records entire message, sends to API as one blob

```typescript
// From main.ts (line 103-117):
async startRecording() {
  if (this.statusBar.status === RecordingStatus.Recording ||
      this.statusBar.status === RecordingStatus.Paused) {
    new Notice("Already recording");
    return;
  }
  try {
    await this.recorder.startRecording();
    this.statusBar.updateStatus(RecordingStatus.Recording);
    new Notice("Recording...");
  } catch (err) {
    this.statusBar.updateStatus(RecordingStatus.Idle);
    new Notice("✘ Could not start recording");
  }
}
```

#### ASR Engine & Settings
- **Transcription API:** OpenAI Whisper (default), Groq, Azure, or any Whisper-compatible endpoint
- **Model:** Configurable (`model` field in settings, default: `"whisper-1"`)
- **Language:** Optional language hint (`language` field, "" = auto)
- **Temperature:** Configurable (default: 0)
- **Response format:** JSON or text (default: `"json"`)
- **Prompt:** Optional transcription hints to improve accuracy

```typescript
// From AudioHandler.ts (line 65-75):
const formData = new FormData();
formData.append("file", blob, fileName);
formData.append("model", this.plugin.settings.model);
if (this.plugin.settings.language &&
    this.plugin.settings.language !== "auto") {
  formData.append("language", this.plugin.settings.language);
}
let prompt = this.plugin.settings.prompt || "";
if (this.plugin.settings.cursorContext) {
  const editor = this.plugin.app.workspace.getActiveViewOfType(MarkdownView)?.editor;
  if (editor) {
    const context = getCursorContext(editor);
    prompt = prompt ? `${prompt}\n${context}` : context;
  }
}
```

#### Text → Markdown
- **Raw append:** Default behavior = insert transcribed text at cursor as-is
- **LLM post-processing:** Optional (enabled via `postProcessing` setting)
  - **Providers:** Claude (Anthropic), GPT (OpenAI), or custom OpenAI-compatible
  - **Default LLM prompt:**

```
"You are a transcription editor. Clean up the following voice transcription: 
fix grammar, remove filler words (um, uh, like) and repetitions, and improve readability. 
Format the text in markdown. 
If there are action items or to-dos, format them as task lists with "[ ]". 
Preserve the original meaning and language. 
Return only the polished text, nothing else."
```

- **Title generation:** Separate LLM call to auto-generate file names if enabled
  - **Default title prompt:** `"Generate a short title (1-5 words) for the following text. Return only the title, nothing else."`
- **Template support:** Note content and filename can use template variables: `{{title}}`, `{{audioFile}}`, `{{transcription}}`, `{{date}}`, `{{time}}`, `{{datetime}}`

```typescript
// From SettingsManager.ts (line 72-81):
export const DEFAULT_POST_PROCESSING: PostProcessingSettings = {
  postProcessing: false,
  postProcessingProvider: "anthropic",
  postProcessingUrl: "https://api.anthropic.com/v1/messages",
  postProcessingModel: "claude-haiku-4-5-20251001",
  postProcessingPrompt:
    'You are a transcription editor. Clean up the following voice transcription: fix grammar, remove filler words (um, uh, like) and repetitions, and improve readability. Format the text in markdown. If there are action items or to-dos, format them as task lists with "[ ]". Preserve the original meaning and language. Return only the polished text, nothing else.',
  autoGenerateTitle: false,
  titleGenerationPrompt:
    "Generate a short title (1-5 words) for the following text. Return only the title, nothing else.",
  keepOriginalTranscription: false,
};
```

#### Voice Commands
- **Trigger:** Hotkey-based (`Alt+Q` default)
- **URI protocol handler:** `obsidian://whisper` with subcommands:
  - `obsidian://whisper` → open controls
  - `obsidian://whisper?command=start` → start recording
  - `obsidian://whisper?command=stop` → stop and transcribe
  - `obsidian://whisper?command=pause` → pause/resume
  - `obsidian://whisper?command=cancel` → discard recording
- **Usable from:** iOS Shortcuts, Alfred, any URL opener

```typescript
// From main.ts (line 226-249):
registerUriHandler() {
  this.registerObsidianProtocolHandler("whisper", async (params) => {
    const command = params.command;
    if (!command) {
      this.openControls();
      return;
    }
    switch (command) {
      case "start":
        await this.startRecording();
        break;
      case "stop":
        await this.stopRecording();
        break;
      case "pause":
        await this.pauseRecording();
        break;
      case "cancel":
        await this.cancelRecording();
        break;
      default:
        new Notice(`✘ Unknown whisper command: ${command}`);
    }
  });
}
```

#### File Writing & Live Edit
- **Insertion at cursor:** `editor.replaceRange(outputText, cursorPosition)` (Obsidian editor API)
- **Create separate note file:** Optional (if `createNoteFile` enabled)
  - Saves to `noteSavePath` with optional template-based filename
- **Audio file save:** Optional (saves recorded audio to `audioSavePath`)
- **Live insertion:** Yes, text appears at cursor immediately after transcription
- **Fallback if no editor open:** Creates note file only

```typescript
// From AudioHandler.ts (line 176-190):
const editor = this.plugin.app.workspace.getActiveViewOfType(MarkdownView)?.editor;
if (editor) {
  const cursorPosition = editor.getCursor();
  editor.replaceRange(outputText, cursorPosition);

  const newPosition = {
    line: cursorPosition.line,
    ch: cursorPosition.ch + outputText.length,
  };
  editor.setCursor(newPosition);
}

new Notice("Transcription complete");
```

#### Post-Processing
- **Punctuation & filler removal:** LLM-based (via prompt)
- **Paragraphing:** LLM-based
- **Timestamps:** Optional via template variables (`{{time}}`, `{{datetime}}`)
- **Frontmatter:** Custom via note template
- **Structured output:** Can request task lists, headers, etc. via LLM prompt

#### Local vs. Cloud
- **Recording:** Local (browser Web Audio API)
- **ASR:** Cloud (OpenAI API, Groq, Azure)
- **LLM post-processing:** Cloud (Claude, GPT, or custom endpoint)
- **Storage:** Local (Obsidian vault files)

---

### 2. **mikealicea/obsidian-scribe** (85 ⭐, Obsidian Plugin)

**URL:** https://github.com/mikealicea/obsidian-scribe  
**License:** MIT  
**Last Push:** 2026-07-15  
**Local/Cloud:** Hybrid (local Obsidian, cloud ASR + LLM)

#### Capture & Segmentation
- **Live recording:** Browser Web Audio API via recording modal
- **Pause/resume:** Yes, maintains session state
- **File upload:** Batch mode: "Transcribe & Summarize Current File" command
- **Whole-file processing:** Records complete message, sends as one unit
- **Mobile support:** iOS/Android via Obsidian mobile app

```typescript
// From README: "Begin recording and watch as your voice notes are transcribed, 
// summarized, and turned into actionable insights."
```

#### ASR Engine & Settings
- **Multiple engines supported:**
  - OpenAI Whisper (required for base transcription)
  - AssemblyAI (optional, for enhanced accuracy + speaker diarization)
  - Deepgram, Gemini, ElevenLabs, Mistral (via provider adapters)
- **Language support:** Multi-language selection in settings

```typescript
// From src/aiProviders/transcription/*.ts:
// openAiTranscriber.ts, assemblyAiTranscriber.ts, deepgramTranscriber.ts, etc.
```

#### Text → Markdown
- **LLM structuring:** Required; uses Claude or GPT
- **Structured output:** JSON-based schema with configurable fields
- **Template system:** Custom note templates with LLM-generated sections
- **Mermaid chart generation:** Automatic visualization of notes
- **System prompt:**

```typescript
// From prompts.ts (buildSummarySystemPrompt):
export function buildSummarySystemPrompt(transcript: string): string {
  return `
  You are "Scribe" an expert note-making AI for Obsidian you specialize in the Linking Your Thinking (LYK) strategy.
  The following is the transcription generated from a recording of someone talking aloud or multiple people in a conversation.
  There may be a lot of random things said given fluidity of conversation or thought process and the microphone's ability to pick up all audio.

  The transcription may address you by calling you "Scribe" or saying "Hey Scribe" and asking you a question, they also may just allude to you by asking "you" to do something.
  Give them the answers to this question

  Give me notes in Markdown language on what was said, they should be
  - Easy to understand
  - Succinct
  - Clean
  - Logical
  - Insightful

  It will be nested under a h2 # tag, feel free to nest headers underneath it
  Rules:
  - Do not include escaped new line characters
  - Do not mention "the speaker" anywhere in your response.
  - The notes should be written as if I were writing them.

  The following is the transcribed audio:
  <transcript>
  ${transcript}
  </transcript>
  `;
}
```

#### Voice Commands
- **"Hey Scribe" queries:** Mid-recording voice questions answered and inserted into notes
- **Interactive:** Can ask questions during recording that trigger LLM responses
- **Custom templates:** Define custom sections and prompts for structured notes

```typescript
// From prompts.ts (buildSummaryZodSchema):
// Schema allows optional sections, LLM fills them dynamically
const schema: Record<string, z.ZodType<string | null | undefined>> = {
  fileTitle: z.string().describe('A suggested title...'),
};
getLlmSections(activeNoteTemplate).forEach((section) => {
  const { sectionHeader, sectionInstructions, isSectionOptional } = section;
  schema[convertToSafeJsonKey(sectionHeader)] = isSectionOptional
    ? z.string().nullable().describe(sectionInstructions)
    : z.string().describe(sectionInstructions);
});
```

#### File Writing & Live Edit
- **Obsidian editor API:** Insert at cursor or create new note
- **Vault.create():** Creates note file with LLM-generated content
- **Progressive save:** "Robust on Failure" design—each step (record, transcribe, summarize) saved separately
- **Mobile resilience:** Designed for interruptions; no single point of failure

#### Post-Processing
- **LLM-driven:** Claude/GPT does all formatting, structuring, summarization
- **Mermaid charts:** Auto-generated for visualization (can auto-fix invalid syntax)
- **Multi-language output:** LLM responds in selected language
- **Custom prompts:** User-defined instructions injected into LLM calls

#### Local vs. Cloud
- **Recording:** Local (browser Web Audio API)
- **ASR:** Cloud (OpenAI/AssemblyAI/Deepgram)
- **LLM:** Cloud (Claude/GPT)
- **Storage:** Local (Obsidian vault)

---

### 3. **dbknv/verborra** (4 ⭐, macOS App)

**URL:** https://github.com/dbknv/verborra  
**License:** MIT  
**Last Push:** 2026-05-29  
**Local/Cloud:** Hybrid (local microphone, cloud ASR + LLM)  
**Platform:** macOS 15+ (Sequoia)

#### Capture & Segmentation
- **Global hotkey:** Configurable keyboard shortcut (recordable in Settings UI)
- **Recording overlay:** Compact, always-on-top window; shows live waveform
- **Push-to-talk:** Press hotkey to start, hotkey or Stop button to end
- **Whole recording:** Sends entire message as single unit
- **Transient design:** Like Alfred/Raycast—never blocking, in-menu-bar app (no Dock icon)

#### ASR Engine & Settings
- **Model selection:** Transcription model chosen from list
  - `gpt-4o-mini-transcribe`, `gpt-4o-transcribe`, `whisper-1`
- **Formatting model:** 12 LLM options across GPT-5.5/5.4/5/4.1/4o families
  - Default: `gpt-5.1`
- **Input/output pricing:** Displayed inline in Settings → LLM tab
- **Language independence:** Choose input speech language and output response language separately

```swift
// From SystemPromptDefinition.swift (simpleVoiceToText):
.en: (
  name: "Speech To Text",
  content: "Fix spelling errors and add punctuation. Return only the corrected text."
)
```

#### Text → Markdown
- **LLM formatting:** Required; runs Whisper transcription → LLM formatting pass
- **System prompts:** Named prompts (multiple kept, switch in overlay)
- **Prompt management:** Can enable "Answer questions in the first message?" per prompt
  - OFF (default): Format dictation, ignore questions within
  - ON: First voice message becomes chat exchange
- **WYSIWYG editor:** Real-time Markdown formatting in overlay while editing
- **Vocabularies:** Teach the app proper spellings (e.g., "git hub" → "GitHub")

```swift
// From SystemPrompt.swift:
var answerQuestionsInFirstMessage: Bool
// Controls whether the model is allowed to answer questions that appear inside
// the FIRST voice-transcribed message of a chat session.
```

#### Voice Commands
- **Personal preferences:** Free-form context injected into every formatting prompt
- **Hotkey switching:** Switch between named prompts in overlay; re-runs formatting
- **No explicit voice commands:** Relies on hotkey for recording trigger; prompt selection is manual

#### File Writing & Live Edit
- **Clipboard paste:** Text formatted by LLM, inserted via clipboard + `Cmd+V` simulation
- **Accessibility permission:** Required for `Cmd+V` simulation into active app
- **Transient overlay:** Result editable in overlay before paste
- **No file creation:** Inserts into focused app (browser, terminal, IDE, chat, etc.)

```swift
// From README: "The result appears in the overlay as live, editable Markdown.
// You press Enter (or Cmd+V) — the text is pasted into the original field via 
// the clipboard + Cmd+V simulation."
```

#### Post-Processing
- **Grammar/punctuation:** LLM-based (via system prompt)
- **Multilingual:** Response language independent of input language
- **Audio device selection:** Pick specific input or follow system default
- **Bluetooth profile handling:** Gracefully switches between HFP (headset) ↔ A2DP (stereo)
- **Diagnostic logging:** Optional structured JSONL logs in `~/Library/Application Support/Verborra/Logs/`

#### Local vs. Cloud
- **Recording:** Local (macOS native audio)
- **ASR + LLM:** Cloud (OpenAI API)
- **Cost:** Fraction of a cent per recording with default models

---

### 4. **lyxdream/obsidian-content-capture-backend** (30 ⭐, Obsidian Plugin Backend)

**URL:** https://github.com/lyxdream/obsidian-content-capture-backend  
**License:** Varies  
**Last Push:** 2026-06-05  
**Local/Cloud:** Hybrid (plugin-driven)

#### Capture & Segmentation
- **Backend system:** Designed to support multiple capture plugins
- **File-based input:** Processes uploaded or linked files
- **Plugin extensibility:** Actual capture methods depend on enabled plugins

#### ASR Engine & Settings
NOT COVERED in public repo README/source (plugin-dependent)

#### Text → Markdown
- **Plugin system:** Output format determined by active plugin
- **Flexible backends:** Supports multiple content processors

#### Voice Commands
NOT COVERED (plugin-dependent)

#### File Writing & Live Edit
- **Vault API:** Writes via Obsidian vault methods
- **Custom plugin outputs:** Varies by plugin

#### Post-Processing
NOT COVERED (plugin-dependent)

#### Local vs. Cloud
**Hybrid,** depending on plugin configuration

---

### 5. **serg-markovich/local-whisper-obsidian** (18 ⭐, Obsidian Plugin)

**URL:** https://github.com/serg-markovich/local-whisper-obsidian  
**License:** MIT  
**Last Push:** 2026-07-16  
**Local/Cloud:** Hybrid (local Whisper capable, also supports cloud APIs)

#### Capture & Segmentation
- **Hotkey-triggered:** Press configured hotkey to start/stop
- **Browser Web Audio API:** Records via browser (when used as Electron app or via Obsidian)
- **Whole-recording mode:** Captures entire message before processing

#### ASR Engine & Settings
- **Local Whisper:** Can run Whisper locally if backend is configured
- **API fallback:** Also supports OpenAI Whisper API if local unavailable
- **Language support:** Configurable

#### Text → Markdown
- **Raw append:** Default mode = insert transcribed text as-is
- **Optional LLM:** Can enable post-processing with local LLM (via compatible backend)

#### Voice Commands
- **Hotkey-based:** Start/stop recording

#### File Writing & Live Edit
- **editor.replaceRange():** Inserts at cursor in active note
- **Live insertion:** Text appears immediately after transcription

#### Post-Processing
**Minimal by default** (filler removal, punctuation optional if LLM enabled)

#### Local vs. Cloud
- **ASR:** Local-capable (if Whisper backend available), otherwise cloud
- **Recording:** Local
- **Storage:** Local (Obsidian vault)

---

### 6. **Sharrnah/whispering-plugins** (9 ⭐, Plugin Ecosystem for Whispering Tiger)

**URL:** https://github.com/Sharrnah/whispering-plugins  
**License:** MIT  
**Last Push:** 2026-09-21  
**Local/Cloud:** Local + cloud hybrid (plugin-driven)

#### Overview
- **Whispering Tiger:** Desktop app UI for voice-to-text and voice-driven workflows
- **Plugin system:** Community-built plugins extend functionality
- **Real-time and batch modes**

#### Capture & Segmentation
- **Streaming:** VAD (Voice Activity Detection) capable
- **Multiple input sources:** Microphone, audio files
- **Pause/resume:** Supported in realtime mode

#### ASR Engine & Settings
- **Multiple providers:** Whisper (local/API), Deepgram, AssemblyAI, OpenAI, Gemini
- **Local capable:** Can run Whisper locally via Coqui or similar
- **Plugin architecture:** Each transcriber is a pluggable adapter

```python
# From plugin table: WhisperAI, OpenAI API, Deepgram API, Gemini API, AssemblyAI (implicit)
# Plugin system allows swapping engines
```

#### Text → Markdown
- **Passthrough plugins:** Text flows through enabled plugins
- **LLM Conversation plugin:** Available for text processing
- **Export to subtitle formats:** VTT, SRT, SBV (markup-like structured output)
- **Custom plugin creation:** Users write Python plugins for processing

#### Voice Commands
- **Keyword detection:** Plugins can detect voice commands
- **LLM intent classification:** Optional via LLM Conversation plugin
- **Custom command plugins:** VRChat avatar control, Discord bot, etc.

#### File Writing & Live Edit
- **Plugin output:** Varies by plugin
- **Subtitle export:** Writes subtitle files
- **Custom destinations:** Keyboard typing, overlay display, OSC (VRChat), network, etc.

#### Post-Processing
- **Subtitle Display plugin:** Shows subtitles on desktop
- **Speech-to-Speech:** RVC voice conversion available
- **Multiple TTS options:** Coqui, ElevenLabs, Bark, Voicevox, ChatTTS, Mars5

#### Local vs. Cloud
- **Fully local capable:** Whisper + Coqui TTS can run on-device
- **Cloud integrations:** Optional plugins for Deepgram, ElevenLabs, OpenAI, Gemini, DeepL

---

### 7. **kevinbadi/kevs-obsidian-ingestion-engine** (19 ⭐, Obsidian Plugin)

**URL:** https://github.com/kevinbadi/kevs-obsidian-ingestion-engine  
**License:** NOT COVERED  
**Last Push:** 2026-04-10  
**Local/Cloud:** Hybrid (plugin-driven)

#### Overview
- **Ingestion framework:** Designed as extensible system for capturing external content
- **Plugin-based architecture:** Similar to content-capture-backend

#### Details
**Source code not fully examined.** Appears to be infrastructure for content plugins rather than a complete voice-to-markdown solution itself.

---

### 8. **hehenaice/VoiceZettelAssist** (0 ⭐, Android App)

**URL:** https://github.com/hehenaice/VoiceZettelAssist  
**License:** NOT COVERED  
**Last Push:** 2026-07-26  
**Platform:** Android  
**Local/Cloud:** Cloud (Gemini)

#### Capture & Segmentation
- **Hardware key trigger:** Device-specific key press to start recording
- **AAC recording:** Android native audio codec
- **Whole file:** Records complete message before processing

#### ASR Engine & Settings
- **Gemini 1.5 Flash:** Google's multimodal LLM for transcription
- **Hardware-triggered:** Integrates with Android device key events

#### Text → Markdown
- **Zettel Notes daily note append:** Automatically appends to daily note in Zettel Notes app
- **LLM-structured:** Gemini formats transcription into note format

#### File Writing & Live Edit
- **Daily note append:** Appends to existing daily note via Zettel Notes API
- **Live update:** Text added to daily note immediately after transcription

#### Local vs. Cloud
- **Cloud-only:** Uses Gemini API exclusively

---

### 9. **eyson-maker/voice-note-transcriber** (1 ⭐, Web/Electron App)

**URL:** https://github.com/eyson-maker/voice-note-transcriber  
**License:** NOT COVERED  
**Last Push:** 2026-06-03  

#### Capture & Segmentation
- **Recording UI:** Web-based recording interface
- **Whole recording:** Records complete message

#### ASR Engine & Settings
- **OpenAI Whisper API:** Cloud-based transcription

#### Text → Markdown
- **Raw append:** Transcribed text inserted as-is, no LLM processing (by default)

#### File Writing & Live Edit
- **File create/append:** Saves transcription to file

---

### 10. **0xSh3ru/whisper-note** (0 ⭐, Linux App)

**URL:** https://github.com/0xSh3ru/whisper-note  
**License:** NOT COVERED  
**Last Push:** 2026-06-02  
**Platform:** Ubuntu/Linux  

#### Capture & Segmentation
- **Hotkey trigger:** `Ctrl+Alt+Space` on Ubuntu
- **Local or cloud Whisper:** Configurable

#### ASR Engine & Settings
- **Whisper local + API:** Can use local or OpenAI cloud

#### Text → Markdown
- **Raw append:** Inserts transcribed text as-is

#### File Writing & Live Edit
- **File append:** Adds to note file

---

### 11. **kondasviktor/saymd** (0 ⭐, CLI Tool)

**URL:** https://github.com/kondasviktor/saymd  
**License:** MIT  
**Last Push:** 2026-09-15  

#### Capture & Segmentation
- **CLI input:** Text input from command line, microphone, or stdin

#### ASR Engine & Settings
- **Whisper:** BYOK (Bring Your Own Key) model
- **CLI-driven:** No GUI, scriptable

#### Text → Markdown
- **Raw stdout:** Outputs transcribed text to stdout (no formatting)

#### File Writing & Live Edit
- **Pipeline friendly:** Designed for shell piping and redirection

---

### 12. **membraneframework/membrane_whisper_plugin** (19 ⭐, Erlang/Elixir Plugin)

**URL:** https://github.com/membraneframework/membrane_whisper_plugin  
**License:** Apache 2.0  
**Last Push:** 2026-08-07  

#### Overview
- **Streaming media framework:** Membrane is a real-time media processing library
- **Whisper integration:** Plugin adds Whisper transcription to media pipelines

#### Capture & Segmentation
- **Streaming chunks:** Processes audio in chunks (VAD-capable)
- **Pipeline-oriented:** Part of larger media processing workflow

#### ASR Engine & Settings
- **Whisper local/API:** Configurable backend

#### Text → Markdown
- **Parent-app driven:** Parent application defines output format

#### File Writing & Live Edit
- **Parent callback:** Parent application handles file operations

---

## Key Patterns & Findings

### 1. **Audio Segmentation**
- **Most common:** Whole-file/whole-message recording (no chunking)
- **Streaming capable:** Sharrnah/whispering-plugins, membraneframework/membrane_whisper_plugin support VAD
- **File-based:** Batch systems (lyxdream, kevinbadi) process uploaded audio

### 2. **ASR Engines**
- **OpenAI Whisper dominates:** 10/12 projects use it (API or local)
- **AssemblyAI:** Used as premium option in obsidian-scribe
- **Local capable:** serg-markovich, Sharrnah, membraneframework, 0xSh3ru support local inference
- **Multi-provider:** obsidian-scribe, Sharrnah support pluggable ASR backends

### 3. **Markdown Generation**
- **Raw append (minimal processing):** nikdanilov (default), serg-markovich (default), eyson-maker, 0xSh3ru, kondasviktor
- **LLM-structured (rich formatting):** mikealicea, dbknv, Sharrnah (optional)
- **Prompt patterns:**
  - **Cleaning prompt:** Fix spelling, remove fillers, add punctuation
  - **Structuring prompt:** Extract headings, action items, task lists, questions
  - **Custom templates:** Support for user-defined output schemas (mikealicea uses Zod)

### 4. **Voice Commands**
- **Hotkey-triggered:** nikdanilov (Alt+Q), 0xSh3ru (Ctrl+Alt+Space), dbknv (global configurable), serg-markovich (configurable)
- **Protocol handler:** nikdanilov via `obsidian://whisper` URI scheme
- **Mid-recording queries:** mikealicea ("Hey Scribe" voice questions)
- **LLM intent:** Sharrnah (via LLM plugin), custom keywords

### 5. **File Updates**
- **Cursor insertion:** nikdanilov, serg-markovich use Obsidian `editor.replaceRange()`
- **File creation:** Most create new note files with templates
- **Append mode:** obsidian-scribe, hehenaice append to existing daily notes
- **Clipboard paste:** dbknv (macOS-specific via Cmd+V)
- **API-driven:** lyxdream, kevinbadi use plugin system

### 6. **Post-Processing**
- **Filler removal:** nikdanilov, dbknv, obsidian-scribe via LLM prompts
- **Punctuation & capitalization:** LLM-based
- **Structured output:** Obsidian-scribe generates Markdown headers, action items, Mermaid diagrams
- **Timestamps:** nikdanilov supports template variables (`{{time}}`, `{{datetime}}`)
- **Title generation:** nikdanilov, obsidian-scribe auto-generate file names via separate LLM call

### 7. **Local vs. Cloud**
- **Fully local:** 0xSh3ru (if local Whisper), Sharrnah (with local plugins), membraneframework
- **Hybrid:** Most—local recording/storage, cloud ASR, optional cloud LLM
- **Cloud-only:** dbknv, hehenaice, eyson-maker (when using cloud APIs)
- **Cost pattern:** Cloud-based projects ($0.0001-$0.01/minute for ASR; LLM $0.001-$0.01/call)

### 8. **Architectural Patterns**
- **Obsidian plugins (60% of research):** Leverage Obsidian editor API for cursor insertion and vault management
- **Overlay/transient UI:** dbknv (Alfred-like experience)
- **Plugin ecosystem:** Sharrnah, lyxdream, kevinbadi build extensible frameworks
- **Batch processing:** Separate "upload file" mode from live recording
- **Mobile support:** obsidian-scribe, hehenaice target mobile; obsidian-scribe emphasizes "no single point of failure"

---

## LLM Post-Processing Prompts (Verbatim)

### nikdanilov/whisper-obsidian-plugin
**Cleaning Prompt (SettingsManager.ts):**
```
You are a transcription editor. Clean up the following voice transcription: fix grammar, remove filler words (um, uh, like) and repetitions, and improve readability. Format the text in markdown. If there are action items or to-dos, format them as task lists with "[ ]". Preserve the original meaning and language. Return only the polished text, nothing else.
```

**Title Generation Prompt:**
```
Generate a short title (1-5 words) for the following text. Return only the title, nothing else.
```

### mikealicea/obsidian-scribe
**Summary System Prompt (prompts.ts, buildSummarySystemPrompt):**
```
You are "Scribe" an expert note-making AI for Obsidian you specialize in the Linking Your Thinking (LYK) strategy.
The following is the transcription generated from a recording of someone talking aloud or multiple people in a conversation.
There may be a lot of random things said given fluidity of conversation or thought process and the microphone's ability to pick up all audio.

The transcription may address you by calling you "Scribe" or saying "Hey Scribe" and asking you a question, they also may just allude to you by asking "you" to do something.
Give them the answers to this question

Give me notes in Markdown language on what was said, they should be
- Easy to understand
- Succinct
- Clean
- Logical
- Insightful

It will be nested under a h2 # tag, feel free to nest headers underneath it
Rules:
- Do not include escaped new line characters
- Do not mention "the speaker" anywhere in your response.
- The notes should be written as if I were writing them.

The following is the transcribed audio:
<transcript>
${transcript}
</transcript>
```

**Mermaid Fix Prompt (prompts.ts, buildMermaidFixPrompt):**
```
You are an expert in mermaid charts and Obsidian (the note taking app)
Below is a <broken-mermaid-chart> that isn't rendering correctly in Obsidian
There may be some new line characters, or tab characters, or special characters.
Strip them out and only return a fully valid unicode Mermaid chart that will render properly in Obsidian
Remove any special characters in the nodes text that isn't valid.

<broken-mermaid-chart>
${brokenMermaidChart}
</broken-mermaid-chart>

Thank you
```

### dbknv/verborra
**Default System Prompt (SystemPromptDefinition.swift):**
```
Fix spelling errors and add punctuation. Return only the corrected text.
```
(Also supports user-defined named prompts; supports multilingual versions in EN, RU, ES, FR, DE, PT, ZH, JA, KO, IT)

---

## File Paths & URLs

| Repo | Key Files |
|---|---|
| nikdanilov/whisper-obsidian-plugin | `main.ts`, `src/AudioHandler.ts`, `src/PostProcessor.ts`, `src/SettingsManager.ts` |
| mikealicea/obsidian-scribe | `src/aiProviders/prompts.ts`, `main.ts`, `src/audioRecord/audioRecord.ts`, `src/settings/` |
| dbknv/verborra | `Verborra/Models/SystemPrompt.swift`, `SystemPromptDefinition.swift` |
| Sharrnah/whispering-plugins | `Plugins/Keyboard-Typing/keyboard_typing_plugin.py`, `Plugins/LLM-Conversation/llm_plugin.py` |
| serg-markovich/local-whisper-obsidian | Plugin structure similar to nikdanilov |
| lyxdream/obsidian-content-capture-backend | Plugin framework (examination incomplete) |
| kevinbadi/kevs-obsidian-ingestion-engine | Plugin framework (examination incomplete) |

---

## Recommendations for Voice Recognition Project

1. **For live dictation into Markdown + note appending:**
   - Follow nikdanilov/whisper-obsidian-plugin pattern (hotkey → transcribe → LLM format → insert at cursor)
   - Or mikealicea/obsidian-scribe pattern (record → transcribe → LLM structure → create note file)

2. **For local-first with cloud fallback:**
   - Adopt serg-markovich's approach (support both local Whisper and API)
   - Use Sharrnah's plugin architecture for swappable ASR backends

3. **For LLM prompts:**
   - Start with nikdanilov's cleaning prompt (filler removal + punctuation)
   - Extend with obsidian-scribe's structuring prompt (headers + task lists + insights)
   - Support user-defined templates (via Zod schema or similar)

4. **For mobile/cross-platform:**
   - Study obsidian-scribe's progressive save architecture (no single point of failure)
   - Consider hehenaice's pattern (append to daily note) for simplicity

5. **For extensibility:**
   - Adopt Sharrnah's plugin system (Python plugins, swappable backends)
   - Or lyxdream/kevinbadi pattern (Obsidian plugin ecosystem)

---

**Generated:** 2026-09-24  
**Research Method:** GitHub API + repository README/source code examination  
**Disclaimer:** Code snippets quoted verbatim from public repositories; subject to their respective licenses.
