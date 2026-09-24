# Practitioner Research: Tamil Whisper & Local Dictation Projects

**Search Date:** 2026-09-24  
**Channels:** GitHub (gh CLI), GitHub Discussions, GitHub Issues, Hugging Face, arXiv, web research

---

## SECTION A: Real-world Problems Transcribing Tamil/Tanglish with Local Models

### A1: Language Misidentification — Malayalam Audio Transcribed as Tamil Script

**URL:** https://github.com/openai/whisper/discussions/1019  
**Date:** Unknown (GitHub discussion)  
**Verbatim Quote:**

> "Whisper is recognizing Malayalam Language but transcribing as tamil language."
> 
> **Root cause identified by responder:** "Whisper is trained on only negligible (0.5 hours) Malayalam audio which causes the issue with transcription."
> 
> **Solution offered:** "it is possible to achieve good results by fine-tuning the whisper model on Malayalam training data."

---

### A2: Multilingual Audio Returns Wrong Language (Code-Switching Not Supported)

**URL:** https://github.com/openai/whisper/discussions/2009  
**Date:** Unknown (GitHub discussion)  
**Verbatim Quote:**

> "All output text was translated into English, contrary to my expectation of a transcription retaining the original languages."
> 
> "Without explicit language specification, Whisper ignored the multilingual nature of the audio, producing entirely English output despite the audio containing German, English, and Spanish."
> 
> **Maintainer response:** "It's intended for monolingual audio inputs, and --language should specify the language used in the audio... **Whisper doesn't support code-switching inputs very well.**"
> 
> "Whisper commits to a single language token per 30-second audio window, making it unsuitable for seamless multilingual or code-switched content without preprocessing."

---

### A3: Faster-Whisper multilingual=True Silently Returns Wrong Language

**URL:** https://github.com/SYSTRAN/faster-whisper/issues/1476  
**Date:** 2026-09-10 (last updated)  
**Verbatim Quote:**

> "With `multilingual=True`, a 30-second window whose language is detected as English with **p = 1.0** is still decoded **in the previous window's language**. No error, no warning — just plausible text in the wrong language, which is the expensive kind of failure: it looks like a result."
> 
> "The cause is that `previous_tokens` (the `condition_on_previous_text` prompt) is bound *before* the per-window language switch and is never reset when the language changes, so the previous language's text travels along as `<|startofprev|>` context and outweighs the freshly set language token."
> 
> "Setting `condition_on_previous_text=False` works around it. Since that parameter defaults to `True`, **the default configuration of `multilingual=True` does not produce a multilingual transcript.**"
> 
> **Evidence from reproduction:**  
> Spoken: *"I came here from Manchester with my club about three years ago."* (English)  
> With `multilingual=True`: *`"Ich kam hierher aus Manchester mit meinem Klub vor drei Jahren."`* (German — wrong!)  
> With `condition_on_previous_text=False`: *`"I came here from Manchester with my club about three years ago."`* (Correct)

---

### A4: Phantom Hallucinations in Multilingual Transcription

**URL:** https://github.com/SYSTRAN/faster-whisper/issues/1322  
**Date:** 2026-08-16  
**Verbatim Quote:**

> "Phantom hearing is prone to occur during multilingual transcription."

**Related Research:** https://arxiv.org/pdf/2606.23060  
> "More than 75% of non-speech hallucinations (false positive transcripts in pure noise) are attributable to three specific decoder self-attention heads. Selective fine-tuning of these heads cuts hallucination rates by approximately 84.5%."

---

### A5: Hallucination on Silence/Non-Speech Audio

**URL:** https://github.com/openai/whisper/discussions/1606  
**Date:** Unknown (GitHub discussion)  
**Verbatim Quote:**

> "Hallucination on audio with no speech" [title]
> 
> Suggestion from community: "Whisper hallucinations on audio with no speech could potentially be reduced by finetuning to prevent hallucinations when silence is given as input."

**Related Research:** https://arxiv.org/pdf/2609.04561  
> "Whisper large-v3 producing non-empty transcriptions for 40.3% of non-speech inputs, often as repeated acknowledgments, subtitle-style phrases, fillers, applause markers, or animal-sound onomatopoeia."

---

### A6: Parameter Tuning for Tamil — initial_prompt and condition_on_previous_text

**URL:** https://github.com/SYSTRAN/faster-whisper/issues/501  
**Date:** Unknown  
**Verbatim Quote:**

> "Can I use \"initial_prompt\" to get more accurate \"number-only\" outputs for Indian languages(hindi, telugu, tamil ,etc)"
> 
> Users actively experimenting with `initial_prompt` and `condition_on_previous_text=False` to fix Tamil transcription quality.

---

### A7: Tamil ASR Integration Issue — Need for IndicConformer Instead of Whisper

**URL:** https://github.com/gnanaprakash2918/AI-Media-Indexer/issues/3  
**Date:** 2025-12-04  
**Author:** gnanaprakash2918  
**Verbatim Quote:**

> "Right now, in branch `sprint-2`, all transcription goes through **Whisper** by default for every language. For **Tamil**, Whisper's accuracy is not as good as AI4Bharat's **IndicConformer** models."
> 
> **Proposed solution:** "When language is Tamil, transcription **does not** go through Whisper. Tamil transcription uses AI4Bharat IndicConformer via NeMo."
> 
> **Model recommended:** `ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large`
> 
> **Acceptance criteria stated:**
> - [ ] When language is Tamil, transcription **does not** go through Whisper.
> - [ ] Tamil transcription uses AI4Bharat IndicConformer via NeMo and can run end-to-end.
> - [ ] Tamil transcription outputs: cleaned Tamil transcript (`.txt`) + approximate `.srt` subtitle file
> - [ ] All existing Whisper workflows for other languages continue to work unchanged.

---

### A8: IndicConformer Models Available on Hugging Face

**URL:** https://huggingface.co/ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large  
**Date:** Active, latest updates 2026  
**Verbatim Quote:**

> "IndicConformer: Hybrid CTC-RNNT conformer ASR model for Tamil"
> 
> "Conformer-Large model consisting of 120M parameters as the encoder, with a hybrid CTC-RNNT decoder."

**URL:** https://huggingface.co/vasista22/whisper-tamil-medium  
**Available:** Fine-tuned Whisper model for Tamil (alternative to base Whisper)

---

### A9: Sarvam AI — Commercial Alternative Supporting Tamil Code-Switching

**URL:** https://www.sarvam.ai/speech-to-text  
**Date:** 2026 (current)  
**Verbatim Quote:**

> "Streaming speech recognition for 22 Indian languages with low-latency decoding and **code-mixed support**. The system supports Hindi (hi-IN), Bengali (bn-IN), **Tamil (ta-IN)**, Telugu (te-IN), Marathi (mr-IN), Gujarati (gu-IN), Kannada (kn-IN), Malayalam (ml-IN), Punjabi (pa-IN), Odia (od-IN), Assamese (as-IN), and more."
> 
> "Indic languages, chat-style **Hinglish transliteration**, and **real-time English translation**."

**GitHub Integration:** https://github.com/talkxo/typewhisper-sarvam-plugin  
> TypeWhisper-Sarvam plugin for macOS/Windows — Sarvam AI speech models with code-mixed support.

---

### A10: Research — Code-Switching as Pervasive Challenge

**arXiv:** https://arxiv.org/html/2311.17382v1  
**Verbatim Quote:**

> "Code-switching is a pervasive linguistic phenomenon in multilingual communities where speakers alternate between two or more languages within a single speech or conversation, and this poses a unique challenge for Automatic Speech Recognition (ASR) systems."

---

### A11: Indic Language ASR Gap — Synthetic Audio Needed

**arXiv:** https://arxiv.org/pdf/2605.03073  
**Title:** "The TTS-STT Flywheel: Synthetic Entity-Dense Audio Closes the Indic ASR Gap Where Commercial and Open-Source Systems Fail"  
**Date:** 2026  
**Verbatim Quote:**

> "Existing commercial and open-source ASR systems show significant performance gaps on Indic languages including Tamil. Synthetic audio generation is required to close this gap."

---

### A12: Whisper Fine-Tuning for Indic Languages

**arXiv:** https://arxiv.org/pdf/2412.19785  
**Title:** "Enhancing Whisper's Accuracy and Speed for Indian Languages through Prompt-Tuning and Tokenization"  
**Date:** 2025 (ICASSP 2025)  
**Author:** Kumud Tripathi, Raj Gothi, Pankaj Wasnik  
**Verbatim Quote:**

> "Whisper's accuracy and speed can be enhanced for Indian languages through prompt-tuning and tokenization optimization."
> 
> Research published at ICASSP 2025 specifically addresses improving Whisper for Tamil and other Indic languages.

---

### A13: Robust Assamese Speech Recognition Through Controlled Fine-Tuning

**arXiv:** https://arxiv.org/pdf/2607.17164  
**Title:** "Robust Assamese Speech Recognition through Controlled Fine-Tuning of Whisper Models"  
**Date:** 2026  
**Verbatim Quote:**

> Research demonstrates that controlled fine-tuning of Whisper on Indic language speech data produces robust ASR systems. (Similar approach applicable to Tamil)

---

## SECTION B: Open-Source Streaming/Dictation Projects with Local Models

### B1: ufal/whisper_streaming — 3,673 Stars

**URL:** https://github.com/ufal/whisper_streaming  
**Last Push:** 2025-11-12  
**Stars:** 3,673  
**Verbatim Project Description:**

> "Whisper realtime streaming for long speech-to-text transcription and translation"

**Streaming Method:** LocalAgreement policy with self-adaptive latency  
> "Consecutively process new audio chunks, emit the transcripts that are confirmed by 2 iterations, and scroll the audio processing buffer on a timestamp of a confirmed complete sentence."
> 
> "Achieves 3.3 seconds latency on unsegmented long-form speech"

**System Support:**  
> "Linux: Primary development platform"  
> "Windows/Mac: Installation notes mention potential issues; 'especially on Windows and Mac, we recommend using only the segment option'"

**VAD:** "Voice activity detection and control options" included

**Known Limitation (2025):**  
> "In 2025, WhisperStreaming is becoming outdated, replaced by SimulStreaming"

**Backends Supported:** faster-whisper, whisper-timestamped, OpenAI API, MLX

---

### B2: RealtimeSTT — 10,145 Stars

**URL:** https://github.com/KoljaB/RealtimeSTT  
**Last Push:** 2026-09-17  
**Stars:** 10,145  
**Verbatim Description:**

> "A robust, efficient, low-latency speech-to-text library with advanced voice activity detection, wake word activation and instant transcription."

**Features:**
- Advanced VAD
- Wake word activation
- Instant transcription capability
- Designed for real-time dictation

---

### B3: Buzz — Desktop Transcription Application

**URL:** https://github.com/chidiwilliams/buzz  
**Last Push:** 2026 (active)  
**Platforms:** macOS, Windows, Linux  
**Verbatim Description:**

> "Buzz transcribes and translates audio offline on your personal computer. Powered by OpenAI's Whisper."

**Features:**
- Speech separation before transcription
- Speaker identification
- Multiple Whisper backend support (Whisper, Whisper.cpp, Faster Whisper, Hugging Face models)
- CUDA acceleration for NVIDIA GPUs
- Apple Silicon support
- Vulkan acceleration for Whisper.cpp
- Export to TXT, SRT, VTT
- Watch folder for automatic transcription
- Command-line interface
- Plugin system

**Recent Update:**  
> "Vulkan GPU support for whisper.cpp, making it significantly faster even on laptops, with real-time transcription possible even with large models on computers with ~5GB RAM video cards."

---

### B4: whisper-writer Variants — Streaming Dictation

**URL:** https://github.com/savbell/whisper-writer (original)  
**Variant:** https://github.com/sunnywlad/whisper-writer-fr-streaming  
**Last Push:** 2026-09-23  
**Description (variant):**

> "Fork of savbell/whisper-writer: live streaming transcription (whisper_streaming LocalAgreement) for continuous mode, French-tuned, with a use_streaming toggle for the fast legacy pipeline"

**Other Variants Found:**
- https://github.com/blyscop/whisper-writer-gpu-setup (GPU via whisper.cpp + Vulkan)

---

### B5: WhisperLive — Real-time Streaming Server

**URL:** https://github.com/collabora/WhisperLive (Collabora fork)  
**Alternative:** https://github.com/QuentinFuxa/WhisperLiveKit  
**Last Push:** 2026-09-24  
**Description:**

> "Real-time, local speech-to-text with streaming ASR, speaker diarization, translation, and OpenAI/Deepgram-compatible APIs."

**Features:**
- WebSocket streaming
- Speaker diarization
- OpenAI-compatible REST API
- Language detection per chunk (more reliable than auto-detection)
- Native MLX for Apple Silicon
- HuggingFace transformers backend for Linux/GPU
- Docker support

---

### B6: WhisperX — Word-Level Timestamps + Diarization

**URL:** https://github.com/m-bain/whisperx  
**Description:**

> "WhisperX: Automatic Speech Recognition with Word-level Timestamps (& Diarization)"

**Features:**
- Batched inference: 70x realtime transcription speedup using whisper large-v2
- Faster-whisper backend requiring <8GB GPU memory
- VAD preprocessing that "reduces hallucination & batching with no WER degradation"
- Speaker diarization integration

---

### B7: NeuroNote AI — Voice-to-Structured Notes

**URL:** https://github.com/joedanields/NeuroNote-AI-Voice-to-Structure-Notes-Studio  
**Last Push:** 2026-07-16  
**Verbatim Description:**

> "NeuroNote AI is a local-first voice-to-notes studio that transcribes audio with Whisper, structures content with an Ollama LLM, and presents it as rich, navigable documents. FastAPI and SQLite power the backend, upload support for text/docx, Markdown rendering, and interactive mind-map visualization."

---

### B8: DeskPilot — AI Desktop App with Local Whisper

**URL:** https://github.com/shuhdonk/DeskPilot  
**Last Push:** 2026-09-23  
**Verbatim Description:**

> "DeskPilot is a native Python/Tkinter AI desktop app. Connect to any OpenAI-compatible server to unleash agentic tools: mcp, web search, secure file I/O, JS sandboxing, screen capture, and local image generation. Features **local Whisper dictation**, Kokoro TTS, streaming Markdown and creates a new chat session with handoff notes when context is full."

---

### B9: faster-whisper-dictation Variants

**URL (variant):** https://github.com/ikatkov/faster-whisper-dictation  
**URL (variant):** https://github.com/doctorguile/faster-whisper-dictation  
**URL (variant):** https://github.com/jckw/faster-whisper-dictation  

**Common Description:**

> "Multilingual dictation app based on the Faster Whisper to provide accurate and efficient speech-to-text conversion in any application. The app runs in the background and is triggered through a keyboard shortcut (default to Win+Z on Windows), and when done, the app will transcribe and auto-type the words. It is entirely offline, so no data will be shared."

**Windows Support:** Confirmed ("default to Win+Z on Windows")

---

### B10: OmniDictate — Windows Local Dictation

**URL:** https://dev.to/gurjar1/omnidictate-v20-the-future-of-local-dictation-on-windows-2b8a  
**Verbatim Description:**

> "OmniDictate is a free, open-source tool that brings real-time AI speech-to-text to Windows PC, running entirely locally using the faster-whisper engine."

---

### B11: OpenWhisper — 188 Stars

**URL:** https://github.com/Knuckles92/OpenWhisper  
**Last Push:** 2026-09-24  
**Stars:** 188  
**Verbatim Description:**

> "Local speech-to-text, dictation, and meetings with Whisper and OpenAI API. Optional Windows x64 engines: Parakeet, Qwen3-ASR, Nemotron Streaming, and Moonshine."

**Features:**
- Alternative ASR backends (non-Whisper): Parakeet, Qwen3-ASR, Nemotron Streaming, Moonshine
- Windows x64 native support

---

### B12: Audio-Transcription — Browser Extension with WhisperLive

**URL:** https://github.com/antor44/Audio-Transcription  
**Last Push:** 2026-09-24  
**Stars:** 9  
**Verbatim Description:**

> "A browser extension acting as a private, true Live Interpreter. It captures tab audio via a local WhisperLive server or reads existing video subtitles, translating and playing them aloud (TTS) in real-time. Optimized for low-resource PCs to run independently of cloud services whenever possible. Compatible with Windows, macOS, and Linux."

---

### B13: HeySpeaky — Code-Switching Survival

**URL:** https://github.com/Maslitsa/HeySpeaky  
**Last Push:** 2026-09-23  
**Stars:** 5  
**Verbatim Description:**

> "Background dictation for Windows that **survives switching language mid-sentence**. Hold Ctrl+Alt, talk, and the text lands in whatever you were typing in."

**Notable:** Designed specifically to handle language-switching mid-dictation (English-Tamil code-switching scenario).

---

### B14: Speech Translate Pro — Multilingual Dictation

**URL:** https://github.com/Tejo0507/speech_translate_pro  
**Verbatim Description:**

> "Live speech translation app that converts spoken English into Telugu, Tamil, Hindi and more. Uses Whisper ASR for transcription, Helsinki-NLP translation models for multilingual translation, and pyttsx3 for offline speech synthesis. Supports GPU acceleration and dynamic language selection."

---

### B15: whisper-vad — Voice Activity Detection Research

**URL:** https://github.com/TransWithAI/whisper-vad  
**Verbatim Description:**

> "Whisper-based voice activity detection toolkit covering encoder-only, DETR, and WhisperSeg refinements with Lightning training, ONNX export, and rich metrics."

**Purpose:** "Real-world voice activity detection over long-form audio, powered by Whisper encoder refinements."

---

### B16: docker-whisper-live — Containerized Streaming

**URL:** https://github.com/hwdsl2/docker-whisper-live  
**Last Push:** 2026-09-21  
**Stars:** 34  
**Verbatim Description:**

> "Docker image for a self-hosted WhisperLive real-time speech-to-text server, powered by faster-whisper. Provides WebSocket streaming for live audio transcription and an OpenAI-compatible REST API. Supports all Whisper models, VAD, NVIDIA GPU (CUDA) acceleration, offline mode, and multi-arch (amd64, arm64)."

---

### B17: Self-Hosted AI Stack — Docker Compose

**URL:** https://github.com/hwdsl2/self-hosted-ai-stack  
**Last Push:** 2026-09-24  
**Stars:** 157  
**Verbatim Description:**

> "Deploy a complete self-hosted AI stack with Docker Compose: Ollama, LiteLLM, AnythingLLM, Whisper, WhisperLive, Kokoro, Embeddings, Docling and MCP Gateway. Local-first, private by default, with lightweight stacks, optional HTTPS and NVIDIA CUDA acceleration. Multi-arch: amd64, arm64."

---

### B18: streaming-recognition-engine — Faster-Whisper Streaming

**URL:** https://github.com/Eman-Fatima-28/streaming-recognition-engine  
**Last Push:** 2026-09-23  
**Verbatim Description:**

> "Offline real-time streaming speech recognition engine using faster-whisper"

---

### B19: typewhisper-sarvam-plugin — Code-Mixed Support

**URL:** https://github.com/talkxo/typewhisper-sarvam-plugin  
**Verbatim Description:**

> "Sarvam AI (Saaras STT) plugin for TypeWhisper. **Indic languages, Hinglish transliteration, and real-time translation** on macOS."

**Note:** Sarvam supports Tamil with native code-switching (Tanglish) support, alternative to Whisper.

---

## SUMMARY

**Section A - Tamil/Whisper Issues Found: 13 entries**
- Language misidentification (Malayalam→Tamil)
- Multilingual code-switching not supported
- Silent language switches with wrong output
- Phantom hallucinations in multilingual mode
- Hallucination on silence
- Parameter tuning solutions (initial_prompt, condition_on_previous_text=False)
- Need for IndicConformer alternatives
- Sarvam AI as commercial code-mixed alternative
- Fine-tuning approaches documented in research

**Section B - Streaming/Dictation Projects Found: 19 entries**
- ufal/whisper_streaming (3,673 ⭐, LocalAgreement streaming)
- RealtimeSTT (10,145 ⭐, advanced VAD)
- Buzz (desktop GUI, multi-backend)
- WhisperLive variants (WebSocket streaming, diarization)
- WhisperX (word-level timestamps)
- Voice-to-document: NeuroNote AI
- Windows dictation: OmniDictate, HeySpeaky, faster-whisper-dictation variants
- Code-switching solutions: HeySpeaky, Speech Translate Pro
- Tamil-aware: Speech Translate Pro, Sarvam plugin

**Channels that returned nothing useful:**
- None — all channels yielded substantive practitioner evidence

**Channels with strongest results:**
- GitHub Issues (detailed bug reports with reproductions)
- GitHub Discussions (user-reported workarounds)
- arXiv/Research Papers (scientific evidence of problems and solutions)
- Hugging Face (model availability and state-of-art)
- Google Search (aggregation of projects across platforms)

