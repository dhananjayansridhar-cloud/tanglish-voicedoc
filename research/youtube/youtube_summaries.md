# YouTube Research: Tamil / Tanglish Speech Recognition & TTS for Local Live Dictation

Compiled 2026-09-24. Built from auto-generated caption transcripts (VTT), video metadata, and
viewer comments fetched with `yt-dlp`. Project constraint under evaluation: **fully local,
RTX 3050 Laptop GPU (6 GB VRAM), Windows 11, no cloud/paid APIs**, for live Tamil/Tanglish
dictation into a self-organizing Markdown document.

**IMPORTANT CAVEAT ON SOURCE QUALITY:** All transcripts below come from YouTube's auto-generated
captions (or auto-translated captions). Auto-captions of Tamil or Tamil-English mixed speech are
frequently garbled, fragmentary, or wrong — this is flagged per video below. Where a caption
reads as nonsensical word salad, that is the auto-caption failing, not necessarily the video's
content failing. Quotes are quoted verbatim from the caption text (spelling/grammar as captured),
with `mm:ss` markers from the cleaned transcript.

Cleaned transcripts and raw VTT files: `research/youtube/transcripts/`
Raw metadata + comment JSON: `research/youtube/metadata/`

---

## Videos summarised: 14
## Videos skipped (off-topic or explicitly excluded): 1 explicitly reviewed + candidate lists noted below

---

# PART A — Videos WITH transcript evidence (10)

## 1. 37 Indian Language Speech to Text Pipeline | AI4Bharat IndicConformer ASR with JSON SRT

- **URL:** https://www.youtube.com/watch?v=70Nrt_FpHz4
- **Channel:** Sudheendra S G | **Upload date:** 2026-05-24 | **Views:** 431 | **Duration:** 1596 s (26:36)
- **Caption:** English (`en-IN`), auto-generated (`automatic_captions`), also listed under `subtitles` (creator-uploaded/auto — same track)
- **LOCAL/CLOUD:** **LOCAL.** Runs entirely on the presenter's own Windows PC + WSL2, no API calls to a third-party service (HuggingFace login is only for model-weight download gating).
- **Models/tools shown:** AI4Bharat **IndicConformer** (Hugging Face, "AI4Bharat Indic Conformer" common multilingual checkpoint, plus per-language checkpoints exist but not used here), FFmpeg (audio extraction), Conda/Mamba envs, PyTorch (cu128 index), transformers==4.40.2, tokenizers==0.19.1, onnx==1.20.1, onnxruntime==1.20.1, huggingface-hub==0.23.5, a custom `3_transcribe_any_language.py` script with silence-aware chunking.
- **Hardware/GPU:** Windows host + WSL2 (Linux) for the AI4Bharat step (author states CUDA/AI dependencies "significantly more stable" in WSL2 than native Windows — see companion video #2). GPU is only confirmed generically via `nvidia-smi` and a `check_torch_gpu.py` script reporting `CUDA count == 1`; **no specific GPU model or VRAM figure is stated.**
- **What was demonstrated (step by step):**
  1. [00:00–02:01] Session recap: pipeline transcribes Hindi/Kannada/Tamil/etc. audio into JSON + TXT + SRT.
  2. [02:01–03:38] Download sample Tamil/Hindi/Kannada MP4s + scripts from a Patreon page; open Anaconda Prompt; `conda env list`; `conda activate audio-asr`.
  3. [03:38–07:18] Run `check_C_translate2.py` — [04:32] *"if it shows CUDA devices"* / [04:34] *"equals one, then the CUDA device is"* [correctly recognized]. Extract mono 16 kHz WAV per-language with FFmpeg (`-vn -ac 1 -ar 16000`) for Hindi, Kannada, Tamil separately.
  4. [07:18–08:52] Switch to WSL2 for the AI4Bharat step; find IndicConformer on Hugging Face, log in, "agree and access repository."
  5. [08:52–16:48] Create a new `audio-indic-asr` conda env (Python 3.10), install torch/torchvision/torchaudio from the `cu128` PyTorch index, `nvidia-smi` check, pin `transformers==4.40.2`, `tokenizers==0.19.1`, `onnxruntime==1.20.1`, `onnx==1.20.1`, `pydub`, `srt`, `tqdm`, `soundfile`, `ffmpeg-python`; pin `huggingface-hub==0.23.5` (states the *latest* hub version is "not compatible" with this model); `huggingface-cli login --token`.
  6. [16:48–19:25] Install `torchcodec`; explains **manual silence-aware chunking** is required because *"unlike faster whisper, AI4Bharat does not chunk audio file into 10 seconds or 20 seconds clips automatically"* [17:52] — a custom script detects silence gaps so chunk boundaries don't cut mid-word/mid-sentence.
  7. [19:25–26:10] Runs `3_transcribe_any_language.py --input <wav> --language hi|kn|ta --chunk-seconds 10 --decoder ctc --device cuda ...` for Hindi, then re-runs with `--language kn` (Kannada) and `--language ta` (Tamil) by editing the previous command in place. Output: per-language folders each with JSON (segments + start/end timestamps), TXT, SRT.
- **OBSERVED RESULTS:**
  - No numeric accuracy, WER, or latency figures given anywhere in this video.
  - [23:33] *"if you come into folder D A Studio audio output... first I have the JSON file... it is precisely translated"* and [24:04] *"it is correctly going to chunk at the end of the sentence... using this you need not worry about this abrupt cutting of sentences"* — a qualitative claim of good sentence-boundary behavior, not a measured accuracy.
  - [25:09] *"The quality of this translation is very good Indian language"* — subjective verdict, no specifics.
  - No English-in-Tamil (code-switch) test performed; the Tamil sample is presumably monolingual Tamil.
  - No error/hallucination is shown on screen in this video (contrast with the companion video #2 below, which explicitly names hallucination as the problem IndicConformer solves).
  - This is a **batch/offline transcription pipeline** (feed a finished video/audio file → get JSON/TXT/SRT), **not live/streaming dictation.**
- **Pitfalls / workarounds mentioned:**
  - Must pin old versions of `transformers`, `tokenizers`, `onnxruntime`, `onnx`, and `huggingface-hub` — "the latest version is not compatible with this AI for Bharat model."
  - Windows paths must be manually rewritten for WSL2 (`D:\AIStudio` → `/mnt/d/AIStudio`) — presenter hits this exact error live at [22:31]–[23:03] (forgot the leading `/mnt/d`).
  - IndicConformer requires gated Hugging Face access (must "agree and access repository", provide contact info).
  - No automatic chunking — must implement silence-aware chunking manually or risk cutting words mid-sentence.
- **Relevant viewer comments (from metadata JSON):**
  - *"This channel needs some serious visibility. Very underrated. Thank you so much."* — @balkiprasanna1984 (0 likes; channel has only 2 comments total).
- **Relevance to this project:** Proves a working **LOCAL, offline** IndicConformer pipeline exists for Tamil on a Windows+WSL2 machine, with concrete install steps and version pins — directly reusable as a batch-ASR reference, but it is **not live/streaming** and gives **no VRAM or 3050-class hardware confirmation**, no Tanglish/code-switch test, and no accuracy numbers.
- **Evidence grade:** **DEMONSTRATED ON SCREEN** (install + run shown), but no numeric results — accuracy/verdict is CLAIMED VERBALLY only.

---

## 2. 38 AI4Bharat Indic Conformer Tutorial

- **URL:** https://www.youtube.com/watch?v=7yWXkWvqSrA
- **Channel:** Sudheendra S G | **Upload date:** 2026-05-24 | **Views:** 377 | **Duration:** 448 s (7:28)
- **Caption:** English, auto-generated
- **LOCAL/CLOUD:** **LOCAL** (companion/condensed recap of video #1, same WSL2 pipeline)
- **Models/tools shown:** AI4Bharat IndicConformer (same as above), FFmpeg, WSL2, Conda/Mamba, PyTorch cu128, pinned Transformers/ONNX-Runtime versions, Hugging Face CLI login.
- **Hardware/GPU:** *"a Windows PC equipped with an Nvidia GPU, the Windows Subsystem for Linux or WSL2"* [00:33] — again no specific GPU model or VRAM figure.
- **What was demonstrated:** A tighter, voiceover-style recap of the same pipeline as video #1: FFmpeg extraction → WSL2 env setup → CUDA 12.8 PyTorch → pinned deps → silence-aware chunking → run for Hindi/Kannada/Tamil by swapping the two-letter language code → JSON/TXT/SRT output.
- **OBSERVED RESULTS:**
  - [00:00] *"Standard English transcription tools struggle with Indian regional languages. Feed them Hindi or Tamil and you often get broken accents and strange hallucinated text."* — this is the key line: a generic (implicitly Whisper-class) ASR **hallucinates** on Tamil/Hindi input, which is the stated motivation for using IndicConformer instead.
  - [00:22] *"This AI for Bharat's Indic Conformer model is built specifically to handle the unique phonetics of regional Indian speech."*
  - [02:08] *"Forcing the audio into this precise 16 kilohertz mono format before doing anything else removes the vast majority of processing errors you would otherwise encounter during transcription."*
  - [02:39] *"Staying in WSL2 prevents the missing BL errors that frequently crash these pipelines on native Windows."* (i.e., native-Windows CUDA/library errors are a known failure mode, not shown on screen here but stated as the reason for the WSL2 detour.)
  - [05:15] Chunking rationale repeated: *"If you blindly cut the audio every 10 seconds, you risk slicing a word right in half... silence-aware chunking... searches for a natural acoustic pause."*
  - No numeric accuracy, latency, or VRAM figures. No live/real-time claim — this is explicitly a batch pipeline for producing JSON/SRT for later dubbing.
- **Pitfalls / workarounds:** Same as video #1 (version pinning, WSL2 path rewriting, manual `torchcodec` uninstall to avoid "fatal shared library conflicts with FFmpeg").
- **Relevant viewer comments:** None (0 comments on this video per metadata).
- **Relevance to this project:** The single strongest **on-screen-adjacent evidence in this whole set that a general ASR model hallucinates on Tamil**, and that IndicConformer is positioned as the fix — but this is a narrated/scripted recap, not a live demo with a visible transcript comparison. Still batch, not live.
- **Evidence grade:** **CLAIMED VERBALLY** (hallucination claim, chunking benefits) — the pipeline mechanics themselves are DEMONSTRATED ON SCREEN in the companion video #1.

---

## 3. Convert speech to text in realtime without delay | using faster-whisper module

- **URL:** https://www.youtube.com/watch?v=uimBp3c3Koo
- **Channel:** KARTIS | **Upload date:** 2025-04-29 | **Views:** 31,236 | **Duration:** 456 s (7:36)
- **Caption:** English, auto-generated
- **LOCAL/CLOUD:** **LOCAL** (faster-whisper runs on the presenter's own machine; no API key used for ASR — a separate "Ollama" LLM is bolted on at the end for a voice-assistant demo, also local).
- **Models/tools shown:** **faster-whisper** (CTranslate2-based reimplementation of OpenAI Whisper), tested with `large-v2`/`large-v3`/`small.en`/`medium.en`; `sounddevice`, `numpy`, `queue` for real-time mic capture; Python `threading` for concurrent record+transcribe; Ollama for the bonus voice-assistant demo.
- **Hardware/GPU:** Presenter states GPU vs CPU is a config toggle (`device="cuda"` vs `"cpu"`) but **never states which physical GPU or how much VRAM** he is using. [00:47]/[00:49] he describes running "a small model on CPU" and "a large V3 model on GPU" as two options, not what he personally has.
- **What was demonstrated, step by step:**
  1. [00:00] Opens faster-whisper GitHub README (CTranslate2 backend), notes FP16 vs FP32 precision options and speed tradeoffs.
  2. [00:30] `pip install faster-whisper`; writes a minimal script: `WhisperModel(model_size, device="cuda", compute_type="float16")`.
  3. [01:33]–[02:35] Tests `small.en` then `medium.en` on a pre-recorded "hello hello hello, how are you" clip — transcribes correctly (see quote below).
  4. [03:07]–[04:10] Explains GPU path requires installing NVIDIA **cuDNN 9** for CTranslate2 (links out to NVIDIA's site, warns of version mismatches causing GPU failures) but says CPU works with zero extra installs and "is not actually too slow."
  5. [04:10]–[06:44] Builds the **real-time** loop: `sounddevice` input stream in a background thread feeding an audio queue; `sample_rate=16000`; `block_duration=0.5s`; `chunk_duration=2s` (i.e., ~2 s of silence is treated as end-of-utterance); `model.transcribe(audio_data, language=..., beam_size=1)`; live captioning of his own speech is shown on screen.
  6. [06:44]–[07:21] Bonus: wires faster-whisper's live transcript into an Ollama LLM to build a toy real-time "AI assistant" ("Katie") that responds to spoken prompts.
- **OBSERVED RESULTS:**
  - [01:51] *"doesn't make a mistake."* / [01:53] *"some mistakes also there are in models"* — presenter acknowledges float32 vs float16 tradeoff affects mistake rate but gives no numbers.
  - [06:14] *"the beam size actually concerns with your speed and the quality of your audio output"* — beam_size=1 chosen for speed in the real-time path (accuracy/latency tradeoff named, not quantified).
  - [06:29]–[06:44] *"you can see that it is live transcribing my audio and I'm not typing anything... this is real true because I'm just speaking on my microphone and it's just transcribing my audio and it is doing it real time."* — real-time low-latency captioning **demonstrated on screen**, but only for English speech, no Tamil/Tanglish tested anywhere in this video.
  - No WER/accuracy percentage, no explicit latency-in-milliseconds figure (only qualitative "quite fast").
  - No Tamil, Indic, or code-switched audio is used at any point — this is a **generic English faster-whisper real-time demo**, useful only as an architecture reference (mic → queue → thread → chunked transcribe → text), not as Tamil evidence.
- **Pitfalls / workarounds mentioned:**
  - GPU path needs matching cuDNN 9 version or "your GPU might not be processing the audio properly."
  - `chunk_duration=2` seconds silence-triggered cutoff is a simple heuristic, not silence/VAD-aware in a sophisticated sense.
- **Relevant viewer comments:**
  - *"bro. please can you share your machine performance?. GPU? VRAM?....."* — @Jordi-sidorfFotso-x2u (4 likes) — **exactly the question this research needs, and it goes unanswered in the video/comments.**
  - *"Woah you are super macha and great teacher in explaining. Bro, Does it work with youtube transcription as live"* — @royalstranger (1 like).
  - *"'In order to do realtime transcription, download sound device and numpy and the queue from the terminal using fintol method. I think you know that and i'm not going to teach that': How in the name of sanity can someone giving a 'tutorial' end up with that? No, Sir, i have NO idea what you're talking"* — @ParalysedGekko (1 like) — a legitimate complaint that key real-time plumbing (the `pip install` commands, thread wiring) is skipped/assumed.
- **Relevance to this project:** The **clearest architecture template found for a live local dictation loop** (mic stream → thread → chunked faster-whisper transcribe → text), and confirms faster-whisper auto-chunks (unlike IndicConformer above, which needed a manual chunker). But it is 100% English, never tests Tamil, and — critically — a top comment asking about GPU/VRAM goes unanswered, so **no hardware-sizing evidence** comes from this video.
- **Evidence grade:** **DEMONSTRATED ON SCREEN** (real-time English loop working) / **NOT SHOWN** (Tamil, VRAM, GPU model, accuracy numbers).

---

## 4. Build an AI Voice Assistant with Python | Listen, Think & Speak | Tamil | Karthik's Show

- **URL:** https://www.youtube.com/watch?v=V3tmtEM_uhk
- **Channel:** Karthik's Show | **Upload date:** 2026-07-24 | **Views:** 2,547 | **Duration:** 1332 s (22:12)
- **Caption:** English, auto-generated — **caption quality is poor/fragmentary throughout** (see caveat below).
- **LOCAL/CLOUD:** **CLOUD.** Uses the **Groq API** for both speech-to-text and the chat/LLM step (`client.audio.transcriptions.create(...)`, later `response = chat completion`), i.e. Whisper-large-v3 **hosted on Groq's cloud**, not local inference. Also implies a separate TTS API call. Not a local-6GB-VRAM solution as built, despite being a "Tamil" voice-assistant tutorial.
- **Models/tools shown:** **Whisper large-v3** (via Groq API) [07:38] *"whisper large v3"*, Streamlit-style page/UI code, `python-dotenv` for API keys, a TTS function (`text_to_speech`) returning an audio buffer, and general prompt/response scaffolding for a Q&A voice assistant ("What is a neural network?", "What is machine learning?").
- **Hardware/GPU:** Not applicable — inference happens on Groq's servers, not the presenter's machine.
- **What was demonstrated (as far as legible):**
  1. Project scaffolding: virtual environment, `requirements.txt`, secrets/config file, API key handling ([Groq API key] and TTS key).
  2. A Streamlit-like page titled "voice assistant" with an audio-record input widget.
  3. [06:59]–[07:37] `transcription = client.audio.transcriptions.create(file=recorded_audio, model="whisper-large-v3", temperature=...)` — records mic audio, sends to Groq, gets back `transcription.text`.
  4. [08:47]–[10:35] Feeds the transcribed text into a chat-completion call (system prompt = "voice assistant", user template, `max_tokens=300`) to generate an answer.
  5. [11:44]–[13:24] Converts the answer back to speech via a `text_to_speech` function returning an `audio_buffer`, played back to the user.
  6. [14:43]–[18:07] Explicitly walks through **edge-case handling**: empty/silent audio, Groq API failures, malformed transcription, TTS errors — presenter deliberately tests "What is a neural network?" and "What is machine learning?" end-to-end and shows the assistant answering correctly both times.
- **OBSERVED RESULTS:**
  - [13:48] *"few problems."* and [14:54] *"responses, text to speech errors,"* — presenter acknowledges failure modes exist (garbled captions make the exact wording unrecoverable) and the following section [14:43]–[18:07] is explicitly about handling "microphone failure, empty or silent audio, speech transcription, Groq API failures, ... responses, text to speech errors."
  - No accuracy percentage, no latency figure, no explicit statement of how English words inside Tamil speech are rendered (Latin vs Tamil script) — **this specific, important question is NOT COVERED** in the legible caption text, despite the video being labeled "Tamil."
  - **Caption reliability warning:** long stretches of this transcript are single disconnected words/fragments ("Okay. Onboarding. txt library secrets configurations." etc.) — the video is very likely narrated substantially in Tamil or Tanglish and YouTube's English auto-captioner is failing to capture most of the spoken content, rendering only isolated English technical terms it recognizes. **Treat any claim about this video's actual Tamil-handling quality as unverifiable from this transcript; only the code/architecture is legible.**
- **Pitfalls / workarounds mentioned:** Explicit edge-case list: mic access denial, empty/silent recordings, Groq API failure, malformed/empty transcription, TTS failure — all called out as things to defensively code around.
- **Relevant viewer comments:**
  - *"sir , how to import this (from dotenv import load_dotenv) (from groq import Groq) sir i will try to lots of times but it do not work sir you can give as solution sir"* — @sakthim-s4x6t (0 likes) — confirms viewers hit basic import/setup failures even for this cloud-based approach.
  - *"Can you provide some examples using open ai or azure"* — @ganeshvisw (0 likes) — viewer wants alternative cloud backends, reinforcing that neither presenter nor audience is thinking "local."
  - *"itha mari tamil la voice assiant panalam ahh solluga"* [Tanglish: "can you tell us how to build a voice assistant like this in Tamil?"] — @Dharanishdk-n3f (0 likes) — a genuine ask for a **Tamil-language** version of this assistant, unanswered in the visible comments, implying the demo itself may be mostly in English despite the "Tamil" title tag.
- **Relevance to this project:** Useful only as an **architecture reference** for a record→transcribe→LLM→TTS voice-assistant loop with explicit edge-case handling — but it is **CLOUD (Groq)**, not local, and does **not** demonstrably prove Tamil/Tanglish transcription quality because the auto-captions themselves are too garbled to verify. Disproves nothing about local feasibility; simply provides no local evidence either way.
- **Evidence grade:** **NOT SHOWN** for Tamil-handling quality (captions unreadable); **DEMONSTRATED ON SCREEN** for the cloud record→transcribe→LLM→TTS architecture and edge-case list.

---

## 5. Speech-to-Text Model Demo - AI4Bharat

- **URL:** https://www.youtube.com/watch?v=xgBKvpiiYrI
- **Channel:** AI4Bharat (official) | **Upload date:** 2022-12-17 | **Views:** 2,931 | **Duration:** 99 s (1:39)
- **Caption:** English, auto-generated
- **LOCAL/CLOUD:** **CLOUD demo of the underlying models** (demoed via `models.ai4bharat.org/#/asr`, a hosted REST/WebSocket API), but the **same underlying model family (IndicConformer/earlier AI4Bharat ASR) is separately shown running fully local** in videos #1–#2 above.
- **Models/tools shown:** AI4Bharat's hosted ASR demo — *"a streaming mode powered by websockets and a rest API"* [00:10]. Includes a **post-processor for numbers** (converts spoken digits to numerals) and named-entity handling (bank names, personal names).
- **Hardware/GPU:** Not applicable (cloud demo site; server-side hardware not disclosed).
- **What was demonstrated:**
  1. [00:02]–[00:33] Introduces the demo site: microphone button starts live streaming recognition via WebSocket, or REST for file upload.
  2. [00:33]–[01:10] Example: speaks a bank account number; the post-processor renders it as digits/numerals rather than spelled-out words.
  3. [01:10]–end] *"the model also got my bank name and my friend's name accurately"* [01:18] — named entities recognized correctly in the (English) example.
  4. [01:23]–end] Switches to a **Tamil** example, uploading a pre-recorded Tamil audio file from the computer (cuts off — video ends right as the Tamil example begins; **no Tamil transcription output is actually shown on screen** in the available caption/video length).
- **OBSERVED RESULTS:**
  - Numbers/entities work well for the English example shown.
  - **The Tamil portion is announced but the actual Tamil transcription result is not captured/shown before the video ends** — this is a teaser/incomplete demo as far as the available recording goes.
  - No accuracy %, no latency figure, no VRAM/hardware info (irrelevant — cloud demo).
- **Pitfalls/workarounds:** None discussed.
- **Relevant viewer comments:**
  - *"what if the input audio file contains both English and Tamil and we choose Language as Tamil, will it convert both to English?"* — @RaviUday (0 likes) — **this is precisely the Tanglish/code-switch question this whole project cares about, and it is unanswered by AI4Bharat or anyone else in the comments.**
  - *"We are developing an service based on Indic translation model but encountering a problem while generating the api key, how can we connect with the developers!"* — @saharshjain3203 (0 likes) — signals friction even in AI4Bharat's own hosted API onboarding.
- **Relevance to this project:** Confirms AI4Bharat's ASR family supports **streaming** (WebSocket) recognition architecturally and has a numeral/entity post-processor — both useful design patterns for a live-dictation tool — but the **Tamil demo itself is never actually shown completing**, and the most relevant viewer question (code-switched Tamil+English input) is left open. Combined with videos #1–#2, this establishes IndicConformer/AI4Bharat models *can* run locally and *can* stream, but no video in this set shows a streaming local Tamil transcription with visible output.
- **Evidence grade:** **DEMONSTRATED ON SCREEN** (English number/name post-processing, streaming architecture); **NOT SHOWN** (actual Tamil output, code-switch behavior).

---

## 6. Automatic Speech Recognition system for Indian Languages "IndicWav2Vec"

- **URL:** https://www.youtube.com/watch?v=cmy2zf6CuH4
- **Channel:** AI4Bharat (official) | **Upload date:** 2022-08-22 | **Views:** 5,345 | **Duration:** 925 s (15:25)
- **Caption:** English, auto-generated
- **LOCAL/CLOUD:** **LOCAL-capable** — this is a **research talk**, not a live demo. The presenter (an AI4Bharat PhD researcher) describes an **open-sourced, downloadable checkpoint** (wav2vec2.0-style self-supervised pretraining + CTC fine-tuning), explicitly contrasted with closed-source cloud models like Google's: [01:39] *"even though there are some models which are available in indian languages... google does host some of these models but the problem is that those are closed source... we don't have access to the model."*
- **Models/tools shown:** **IndicWav2Vec** — wav2vec 2.0 architecture, self-supervised pretraining on ~17,000 hours of unlabeled Indic audio (sourced from YouTube and All India Radio/AIR, roughly 6,000+11,000 hours respectively per [05:16]–[05:48]), fine-tuned with CTC + an external language model for error correction/rescoring, covering **40 languages** for pretraining and **9 languages with state-of-the-art results** at publication (covers up to 22 target languages including Tamil per AI4Bharat's broader IndicASR project, though this talk does not show a live Tamil test).
- **Hardware/GPU:** [11:22] *"this model particularly took 24 gpus for three days to train"* — this is a **training-time** figure for the original model, not an inference/VRAM figure for a laptop deployment. **No inference VRAM figure given.**
- **What was demonstrated:** This is a **slide/talk presentation**, not a live coding or on-screen inference demo. Covers: why Indian-language ASR is data-poor vs English; traditional (feature extractor → acoustic model → pronunciation model → language model) pipeline vs modern end-to-end self-supervised approach; wav2vec2.0 pretraining mechanics (convolutional encoder → quantizer → contrastive task); benchmark bar charts showing fine-tuned+pretrained models beat from-scratch baselines, and a language model further reducing "grammatical mistakes" and "spelling mistakes."
- **OBSERVED RESULTS:**
  - [07:51]–[08:22] The language model stage explicitly exists to fix *"spelling errors and the mistakes that the model can potentially make"* from the acoustic-only stage, and to fix *"incomplete sentences"* — i.e., the raw wav2vec2/CTC output has known spelling/grammar mistakes that require an LM pass to clean up.
  - Benchmark charts are described (pretrained fine-tuned models, red bars, beat from-scratch blue bars; LM further improves via yellow bars for large-corpus LM) but **no specific numeric WER/CER values are captured in the caption text** — the presenter references "two tables" on-screen that the caption does not transcribe as numbers.
  - No Tamil-specific test run in this talk; Tamil is one of the target languages in AI4Bharat's broader project but not demonstrated here individually.
  - [12:32]–[13:03] Notes downstream applications explicitly include *"smart personal assistants"* and forming a *"stepping stone for speech to speech translation... real-time translations."*
- **Pitfalls/workarounds:** Per-language fine-tuning is expensive to deploy (*"you should be having 20 instances of the same model running across 20 machines"* [13:34]) — motivates ongoing work (at time of talk) toward a single multilingual model and lightweight "adapters" for domain specificity instead of full per-language deployments.
- **Relevant viewer comments:** None captured (research-talk video, low comment engagement).
- **Relevance to this project:** Background/provenance for the AI4Bharat model family used locally in videos #1–#2 (IndicConformer is a later evolution of this IndicWav2Vec line). Confirms the checkpoints are genuinely open-sourced and self-hostable, and confirms the honest limitation that raw acoustic-model output needs LM correction for spelling/grammar. Gives **no inference-time VRAM/latency numbers** — the "24 GPUs for 3 days" figure is training cost, **not** relevant to a 6 GB laptop inference budget, and should not be conflated with inference requirements.
- **Evidence grade:** **CLAIMED VERBALLY** throughout (a research talk with described-but-not-numerically-transcribed benchmark charts); no live inference shown.

---

## 7. How to Build Your Own JARVIS AI Agent 100% Free! | LiveKit Tutorial #tamil

- **URL:** https://www.youtube.com/watch?v=xHvWsePTs3I
- **Channel:** Echo Mind | **Upload date:** 2025-08-17 | **Views:** 11,353 | **Duration:** 794 s (13:14)
- **Caption:** English, auto-generated
- **LOCAL/CLOUD:** **CLOUD.** Despite "100% Free" in the title, the pipeline uses **LiveKit's hosted voice-AI stack** plus an **OpenAI API key** [02:05] *"open API key"* for the LLM/agent brain — this is a cloud-orchestrated agent (LiveKit Cloud project, WebSocket URL + secret key [04:15]–[04:54]), not a local pipeline. "Free" appears to refer to the LiveKit free tier, not to running without external services.
- **Models/tools shown:** LiveKit Agents framework/Voice AI quick-start, an OpenAI-backed conversational agent named "Friday" (the presenter addresses it as "Jarvis"/calls the assistant "boss"-responsive), `agent.py` console-mode run.
- **Hardware/GPU:** Not applicable (cloud-hosted agent).
- **What was demonstrated:**
  1. Sign-up/setup on LiveKit's official site, agent + model selection, "voice AI quick start," Python <10-minute self-host setup.
  2. Create a new LiveKit project, configure WebSocket URL + secret key, add OpenAI API key.
  3. [07:21]–[08:05] Run `python agent.py console` and converse live.
  4. [08:05]–[12:04] Live conversation demo, mixed Tanglish framing ("boss" address is a Tamil-cinema-influenced convention) — sample exchange: *"Uh, who you speak in English? Right away, boss. Should I switch to English for this conversation? Yes, of course. Go ahead. Understood. I will now respond in English."* — i.e. the presenter explicitly asks the agent to switch language mid-conversation and it complies (in the visible/legible English side of the exchange).
  5. The agent momentarily misidentifies itself: *"I apologize boss. There seems to be a misunderstanding. I am Friday, your personal assistant, not Gemini."* [09:11] — a minor identity/hallucination glitch during the live demo.
- **OBSERVED RESULTS:**
  - Language-switching mid-conversation works (agent acknowledges and switches to English on request) — but because this is voiced through an **OpenAI cloud LLM+STT/TTS stack**, it says nothing about local Tamil ASR feasibility.
  - No accuracy, latency, or hardware figures (not applicable — cloud).
  - One visible **hallucination/identity confusion** moment (agent calls itself unprompted-adjacent wrong name before correcting) — worth noting as a general LLM-agent failure mode independent of ASR.
- **Pitfalls/workarounds:** None specific to ASR; general LiveKit account/project setup friction implied by the step count.
- **Relevant viewer comments:** Not separately fetched for this video (added mid-research as a supplementary on-topic pick; no yt_json metadata file was fetched for it — see gaps below).
- **Relevance to this project:** Shows a **cloud** voice-agent architecture with mid-conversation language switching and "boss"-style Tanglish framing, but is **not evidence for local Tamil ASR** at all — it is included only as a reference architecture for command-driven language-switching UX, which is directly relevant to the "auto-organizes on spoken commands" requirement, but implemented via cloud APIs, not local models.
- **Evidence grade:** **DEMONSTRATED ON SCREEN** (cloud agent + language-switch UX); **NOT APPLICABLE** to local ASR question.

---

## 8. AI in Tamil — Sarvam AI | Language No Bar (மொழி ஒரு தடையல்ல)

- **URL:** https://www.youtube.com/watch?v=3eE4ZdnPNZU
- **Channel:** Salavadi Eswaran | **Upload date:** 2026-02-21 | **Views:** 17,518 | **Duration:** 920 s (15:20)
- **Caption:** English (auto-generated) **and** Tamil (`ta`, auto-generated) both downloaded; English captions used for this summary.
- **LOCAL/CLOUD:** **CLOUD.** Sarvam AI is explicitly a hosted Indian AI platform/API (the presenter navigates its web platform: text-to-speech, speech-to-text, translate-text-to-speech tabs). No local install shown.
- **Models/tools shown:** **Sarvam AI** web platform — Speech-to-Text, Text-to-Speech ("male and female voice," "advanced voice" models), Translate, and an OCR ("optical character recognition," handwriting/newspaper) feature.
- **Hardware/GPU:** Not applicable (cloud platform).
- **What was demonstrated:** A guided tour of Sarvam AI's dashboard: switching between TTS/STT/Translate tabs, selecting a voice, starting a recording, uploading a YouTuber-style script for "dubbing," and a separate OCR panel for scanning handwritten/newspaper text and translating it.
- **OBSERVED RESULTS:**
  - **Caption reliability warning:** the English auto-caption for this video is extremely fragmentary — most cues are single disconnected words ("multi-billion dollar", "Deep sea deep.", "for", "[snorts]") rather than coherent sentences. This strongly suggests the presenter is speaking largely in Tamil (or heavy Tanglish) and the English auto-captioner is failing to capture it, catching only isolated recognizable words. **No reliable accuracy, error, or verdict quote can be extracted from the English captions of this video** — this is flagged rather than guessed at. The Tamil-language caption track (`3eE4ZdnPNZU.ta.vtt`, saved alongside) was downloaded but not deeply reviewed for this summary; a Tamil-literate reviewer could extract more from it.
  - No numeric accuracy, latency, or hardware data recoverable.
- **Pitfalls/workarounds:** None recoverable from legible captions.
- **Relevant viewer comments:** Not separately fetched (supplementary pick; no yt_json file for this video id — see gaps below).
- **Relevance to this project:** Demonstrates Sarvam AI's breadth (STT/TTS/Translate/OCR, all in Tamil) as a **CLOUD** reference point only — cannot be used under the local/6 GB constraint. Its value here is mainly as a pointer that a Tamil-fluent human reviewer should re-check the `.ta.vtt` Tamil caption track directly, since the English auto-caption track is unusable for extracting claims.
- **Evidence grade:** **NOT SHOWN** (captions too garbled to confirm any specific claim about Sarvam's Tamil quality).

---

## 9. This AI Voice Generator Speaks 11 Indian Languages (@SarvamAI)

- **URL:** https://www.youtube.com/watch?v=lnCTn6q6thE
- **Channel:** Media Meets AI | **Upload date:** 2026-07-27 | **Views:** 50 | **Duration:** 65 s (1:05)
- **Caption:** English, auto-generated (clean/legible — this is a scripted voiceover, not live speech)
- **LOCAL/CLOUD:** **CLOUD.** Sarvam AI is again the subject; this is a short marketing/explainer clip, not a hands-on demo.
- **Models/tools shown:** Sarvam AI's narration/TTS product (paste-script → pick-voice → get narration).
- **Hardware/GPU:** Not applicable.
- **What was demonstrated:** No hands-on demo at all — this is narrated marketing copy over presumably stock/product footage. No screen-recorded usage.
- **OBSERVED RESULTS / claims (verbatim, unverified):**
  - [00:00] *"An Indian startup built an AI voice that speaks 11 Indian languages fluently, including the Hindi-English mix people actually talk in. It's called Sarvam AI... Names pronounced right, code-switching handled natively, because it was built on Indian speech from day one. Not bolted onto an English model like most global tools."*
  - This is the **only source in this whole set that explicitly claims "code-switching handled natively"** for an Indian-language voice product — but it is a marketing claim with **zero on-screen demonstration**, no Tamil-specific example, and no independent verification.
- **Pitfalls/workarounds:** None (no demo).
- **Relevant viewer comments:** Not separately fetched (supplementary pick; low-view video, no yt_json file — see gaps below).
- **Relevance to this project:** Surfaces the *claim* that Sarvam AI handles Hindi-English code-switching natively — directly relevant to the Tanglish requirement — but as a **pure marketing claim with no demonstration**, it must not be treated as evidence of actual behavior, and it is about TTS/voice generation, not ASR/dictation anyway.
- **Evidence grade:** **CLAIMED VERBALLY** (marketing copy only) — **NOT SHOWN** on screen.

---

## 10. How to Install Whisper AI - Complete Tutorial | Tamil Audio to Text | Ep. 12

- **URL:** https://www.youtube.com/watch?v=PKHA92gusTM
- **Channel:** RTR Unfiltered | **Upload date:** 2025-04-18 | **Views:** 1,281 | **Duration:** 1020 s (17:00)
- **Caption:** English (`en`) **and** Tamil (`ta`/`ta-orig`) auto-generated captions both downloaded. **The English caption track reads as a machine-translated-from-Tamil transcript** (unusual phrasing consistent with YouTube auto-translating Tamil audio into English, not native English captioning) — flagged rather than treated as a clean native-English transcript.
- **LOCAL/CLOUD:** **LOCAL.** OpenAI's original **`whisper` pip package** (`pip install -U openai-whisper`) installed and run entirely on the presenter's own **CPU** (explicitly: *"I don't have any gpu. I use AMD1 so I got this model going to select cpu."* [07:02]) — i.e., this is a **CPU-only** run, not GPU-accelerated, and not on an NVIDIA card at all.
- **Models/tools shown:** OpenAI Whisper (official package, not faster-whisper), Python 3.9–3.11 compatibility window stated explicitly [05:25], PyTorch (CPU build), `tiktoken`, FFmpeg, Rust (`pip install setuptools-rust` dependency), all six standard Whisper sizes (tiny/base/small/medium/large/turbo) — presenter uses **`turbo`** and **`large`** for the live test.
- **Hardware/GPU:** **CPU-only, AMD system** — explicitly no NVIDIA GPU. Large model download noted as **"7 to 8 GB"** [11:38] (disk size, not VRAM — relevant context since the project's constraint is 6 GB VRAM and a `large` Whisper checkpoint alone is close to/over that budget before any KV-cache/activation overhead).
- **What was demonstrated, step by step:**
  1. [01:42]–[05:25] Explains this is an instructional/local-AI-tools series; goes to openai/whisper GitHub, reads Security & Privacy section, recommends users read privacy policy before local install.
  2. [04:23]–[07:02] Installs Python 3.11, PyTorch (CPU-only build: *"I don't have any gpu... select cpu"*), `pip install -U openai-whisper` (clones/installs from GitHub), FFmpeg (via Chocolatey/Scoop), Rust + `setuptools-rust` (needed as a Whisper dependency).
  3. [09:36]–[10:07] Explains the six model sizes and the general accuracy/speed/resource tradeoff (*"Higher the number is kind of more data intensive and more resource intensive at the same time more accurate"*), notes not everyone can run `large` — depends on GPU/CPU power.
  4. [10:07]–[12:40] Records a **live test audio sample deliberately mixing English and Tamil**: [12:24] *"why then did I purposefully speak only English and Tamil? To show you a demo of how it delivers to you."* Runs `whisper <file> --model turbo` then a second pass with `--model large` via CPU.
  5. [12:40]–[14:12] Reviews the generated **JSON output**: confirms it includes per-segment `start`, `end`, `text`, and a detected **`language: Tamil`** field; also reviews the generated `.srt` and `.tsv` (tab-separated) outputs.
- **OBSERVED RESULTS:**
  - [12:24]–[12:40] *"test 123, this is sample audio for RTR Unbuilder Episode 12, I don't know what this is, okay, I think it's correct, okay, it's not bad"* — presenter's real-time reaction to the transcription of his own mixed English+Tamil test phrase.
  - [12:40] **Self-rated accuracy: *"even say that I would give it a 90% mark."*** — explicitly a **subjective, unverified self-assessment**, not a measured WER, and confounded by an acknowledged noisy recording setup (*"I'm using this same mic to record this video... there is some noise issue in the background"* [12:40]).
  - Confirms the model **auto-detects the spoken language and tags the JSON output `language: Tamil`** even in a mixed English+Tamil utterance — direct, on-screen evidence that OpenAI Whisper's language-ID reports "Tamil" for code-switched Tamil-dominant speech, though the video does **not** show or discuss whether the *English* words inside that Tamil speech are rendered in Latin script or transliterated into Tamil script (**NOT COVERED** — this exact, critical question for the project is not addressed).
  - [14:22]–[14:43] Presenter states CPU-only ("laptop... run on CPU mode") works for this use case, but recommends an NVIDIA GPU for "larger audio samples" and "more powerful and more accurate" runs, while noting NVIDIA GPUs are "expensive."
  - No explicit latency/real-time-factor number given — this is explicitly framed as **offline/batch** transcription of a short pre-recorded sample, not live/streaming.
- **Pitfalls/workarounds mentioned:**
  - Whisper requires Python 3.9.9–3.11.x, not the latest Python.
  - Requires Rust toolchain (`setuptools-rust`) as a build dependency — an easy-to-miss requirement.
  - Background mic noise degrades transcription quality (acknowledged directly).
  - `large` model is ~7–8 GB to download/cache.
- **Relevant viewer comments:** No comments were fetched for this specific video (not in the original yt_json batch — see gaps below).
- **Relevance to this project:** **The single most directly relevant "does it work on Tamil/Tanglish" data point found in this entire set.** It is the only video that (a) deliberately constructs a mixed English+Tamil test utterance, (b) runs a locally installed Whisper-family model against it, and (c) reports back a result — even though that result is only a self-rated "90%" with no ground-truth WER, on a noisy mic, on CPU only (not GPU/VRAM-relevant), and with the English-vs-Tamil-script rendering question left unanswered.
- **Evidence grade:** **DEMONSTRATED ON SCREEN** for install + mixed-language run + JSON language-ID output; **CLAIMED VERBALLY** (not measured) for the "90%" accuracy figure; **NOT SHOWN** for VRAM/GPU behavior (this run is CPU-only) and for English-script-vs-Tamil-script rendering of code-switched words.

---

# PART B — On-topic videos identified but WITHOUT usable transcript (4)

`yt-dlp` returned repeated `HTTP Error 429: Too Many Requests` for these four caption downloads even after retries with backoff; only title/channel/date/views/duration metadata (via `--print`) could be retrieved. They are listed here per the task's "still worth listing" guidance, with grade **NOT SHOWN** throughout.

### 11. Sarvam AI | Real Time Voice Agent Exploring Video Tamil
- **URL:** https://www.youtube.com/watch?v=6od8EtAXm3M | **Channel:** AI with Thiru | **Date:** 2026-03-09 | **Views:** 5,915 | **Duration:** 533 s
- **LOCAL/CLOUD:** **CLOUD** (Sarvam AI, per title/channel context).
- **Relevance:** Title suggests a real-time Tamil voice agent demo on Sarvam's cloud platform — would be directly relevant as a CLOUD reference point for real-time Tamil ASR latency/quality if captions become available later. **Evidence grade: NOT SHOWN** (no transcript retrieved).

### 12. Indic Parler-TTS - Install Locally - Test with Hindi, Urdu, Tamil and Other Languages
- **URL:** https://www.youtube.com/watch?v=X1GK4iSNQJU | **Channel:** Fahd Mirza | **Date:** 2024-12-04 | **Views:** 8,329 | **Duration:** 790 s
- **LOCAL/CLOUD:** **LOCAL** (title explicitly states local install) — **Indic Parler-TTS**, a locally-installable Tamil-capable TTS model. This is potentially important for the "assistant asking clarifying questions by voice" requirement (local Tamil TTS), but no transcript could be retrieved (429 errors persisted across three retry attempts). **Evidence grade: NOT SHOWN** — flagged as a priority for manual follow-up given the title directly matches a project need (local Tamil TTS).

### 13. Automatic Speech Recognition in Tamil | Thenkachi ko swaminathan inspired recreation
- **URL:** https://www.youtube.com/watch?v=hoA-xO3Zzio | **Channel:** Tech Thuli | **Date:** 2026-03-10 | **Views:** 92 | **Duration:** 340 s
- **LOCAL/CLOUD:** Unknown (no transcript). Low view count.
- **Relevance:** Title suggests a Tamil ASR demo; unverifiable. **Evidence grade: NOT SHOWN.**

### 14. Sarvam AI Text to Speech in Action | Best AI Tamil Voice Generator
- **URL:** https://www.youtube.com/watch?v=y38bxfAX6Rg | **Channel:** Tutusfunny tamil | **Date:** 2026-07-06 | **Views:** 195 | **Duration:** 531 s
- **LOCAL/CLOUD:** **CLOUD** (Sarvam AI).
- **Relevance:** Another Sarvam Tamil TTS demo; unverifiable without transcript. **Evidence grade: NOT SHOWN.**

---

# PART C — Explicitly SKIPPED (off-topic) videos

### How to Use OpenAI's Whisper for Perfect Transcriptions (Speech to Text)
- **URL:** https://www.youtube.com/watch?v=dg_TWk8Zfjk | **Channel:** Teacher's Tech | **Date:** 2025-10-08 | **Views:** 139,823 | **Duration:** 493 s
- **Reason skipped:** Generic English-only Whisper transcription tutorial with no Tamil/Indic content anywhere in the title, description, or (spot-checked) comments — matches the task's explicit "generic transcription jobs" skip criterion. It was fetched into `yt_json/` early in the research process (before this filtering pass) and its metadata/comments are retained in `metadata/dg_TWk8Zfjk.json` for completeness, but it is **not summarised** as a project-relevant video. Its top comments ("most accurate transcription program I've ever used," "worked better than all the other standalone transcribers") are generic praise with no Indic-language relevance.

### Other candidates noted in the original 54-video and 68-video candidate lists but not pursued (one-line reasons, from `research_youtube.md` / `research_youtube_quotes.md`):
- **bb_L75GGfF8** "Tamil voice typing app for Android" (248,830 views) — Android phone-keyboard voice-typing app promo, not an ASR model/technique demo; matches "phone keyboard promos" skip criterion.
- **OxW9BHsViXo** "How to Convert Audio to Text" — generic transcription-service walkthrough, no Indic focus.
- **0FYlnpTuiBk** "English Voice Typing Keyboard - Promotional Video" — English-only keyboard promo.
- **2uaKs8ZxiOs** "Live Demo | How To Do Transcription Jobs On GoTranscript.com" — a transcription *job/gig-work* tutorial, not an ASR technology demo; matches "generic transcription jobs" skip criterion.
- **0QzopZ78w9M** "How To Get Transcript From YouTube Video?" — YouTube-transcript-extraction trick, matches explicit skip criterion.
- **1rxKyYEIWbA** "Easy way to Translate any Language" — generic translation trick video, not ASR/TTS specific.
- **QUJFyhdni6g** "Google Ai Studio Text to Speech Tamil Ai Voiceover Free Unlimited" — **on-topic but CLOUD (Google AI Studio)** and not pursued for transcript download in this pass given the extra-download cap and higher priority given to LOCAL-labeled and higher-signal candidates; noted here as a gap (see final section).
- **cvC6U-q6JcE** "Build an AI Language Learning App with Flutter (Speech-to-Text + Gemini AI)" — on-topic-adjacent (uses cloud Speech-to-Text + Gemini) but is an app-building tutorial where ASR is incidental, not the focus; deprioritized versus the 9 videos actually pursued.
- The remaining ~60 unreviewed IDs from the 54-video and 68-video candidate lists (full IDs in `unique_video_ids.txt` and inline in `research_youtube_quotes.md`) were **not individually triaged** in this pass beyond the keyword/title screening already recorded in the prior research files — this is an explicit scope limitation, not a claim that they are all off-topic.

---

# PART D — Cross-video synthesis

## Which models were actually DEMONSTRATED working on Tamil (on screen, with visible output)?

| Model | Video(s) | What was actually shown | Local? |
|---|---|---|---|
| **AI4Bharat IndicConformer** | #1 (70Nrt_FpHz4), #2 (7yWXkWvqSrA) | Full local install + batch transcription of a Tamil MP4 sample → JSON/TXT/SRT, on WSL2. No accuracy % shown, but pipeline runs end-to-end and output files are opened on screen. | **Yes — LOCAL** |
| **OpenAI Whisper (`large`/`turbo`, official package)** | #10 (PKHA92gusTM) | Local CPU-only run on a deliberately mixed English+Tamil test phrase; JSON output correctly tags `language: Tamil`; presenter self-rates "90%" (unverified, noisy mic). | **Yes — LOCAL (CPU only, not GPU-tested)** |
| **AI4Bharat hosted ASR (WebSocket/REST demo)** | #5 (xgBKvpiiYrI) | English number/name post-processing shown working; **Tamil example is announced but the actual Tamil output is never shown before the clip ends.** | Cloud demo (model itself is open/self-hostable per #1/#2) |
| **faster-whisper** | #3 (uimBp3c3Koo) | Real-time **English** transcription shown working smoothly; **never tested on Tamil at all** in this video. | Yes — LOCAL, but no Tamil evidence |
| **Groq-hosted Whisper large-v3** | #4 (V3tmtEM_uhk) | Used in a "Tamil" voice-assistant, but captions too garbled to confirm actual Tamil transcription quality. | Cloud, unverifiable |
| **Sarvam AI (STT/TTS)** | #8, #9, #11(NOT SHOWN), #14(NOT SHOWN) | Claims of Tamil + code-switch support; one platform tour with unreadable captions, one pure marketing claim with no demo, two videos with no transcript at all. | Cloud, unverified |
| **IndicWav2Vec** | #6 (cmy2zf6CuH4) | Research talk describing the method and open-sourced checkpoint; no live Tamil inference run shown. | Local-capable, not demonstrated live |

**No video in this set shows a real-time/streaming local Tamil or Tanglish transcription with a visible, legible result.** The closest approaches are: (a) IndicConformer's local *batch* Tamil pipeline (not live), and (b) Whisper's local *offline* mixed-language test (not live/streaming, CPU-only, self-rated not measured).

## Which models/approaches FAILED or showed problems on Tamil/Indic input?

- **Generic/English-tuned transcription tools** are explicitly named (video #2, [00:00]) as producing **"broken accents and strange hallucinated text"** on Hindi/Tamil input — the stated reason AI4Bharat built IndicConformer. This is a **verbal claim**, not shown side-by-side on screen.
- **Raw wav2vec2/CTC acoustic-model output** (video #6) is explicitly stated to contain **spelling and grammar mistakes** and **incomplete sentences** that require a separate language-model rescoring pass to clean up — an architecture-level admission that acoustic-only Indic ASR is imperfect out of the box.
- **AI4Bharat's own IndicConformer pipeline has no automatic chunking** (video #1, [17:52]) — naive fixed-interval chunking risks cutting words/sentences mid-way, requiring a custom silence-aware chunker to work around.
- **A LiveKit/OpenAI cloud agent** (video #7) showed one live identity-hallucination glitch (misnaming itself) during an otherwise working language-switch demo — a general LLM-agent failure mode, not ASR-specific.
- **Whisper's mixed English+Tamil result** (video #10) was only self-rated ("90%," unverified) on a noisy mic, with the specific question of *how English words are rendered inside Tamil output* left completely unaddressed.

## Recurring pitfalls / install problems across videos

1. **Dependency version pinning is brittle and load-bearing** for AI4Bharat models — must downgrade `transformers`, `tokenizers`, `onnxruntime`, `onnx`, and `huggingface-hub` to specific older versions or installation/runtime breaks (videos #1, #2).
2. **Windows-native CUDA/library instability** pushes creators toward **WSL2** for AI4Bharat-style pipelines specifically to avoid "missing BL errors" and general instability (videos #1, #2) — a real added-complexity tax for a Windows 11 target environment.
3. **Windows-vs-Linux path syntax** is an easy, actually-hit mistake (`D:\...` vs `/mnt/d/...`) when bridging WSL2 pipelines (video #1, hit live on screen).
4. **GPU driver/library mismatches** (cuDNN version for faster-whisper's CTranslate2 backend) are called out as a real failure risk (video #3).
5. **Gated model access** (Hugging Face "agree and access repository" + token) adds friction to every AI4Bharat/Indic-Conformer setup (videos #1, #2).
6. **Real-time plumbing is glossed over** in at least one popular tutorial (video #3; a viewer complains the actual `pip install`/threading wiring is skipped) — a caution that "it works in the video" does not always mean the steps are fully reproducible from the video alone.
7. **No video in this set reports a concrete VRAM number**, and the one direct viewer question asking for GPU/VRAM specs (video #3 comments) goes **unanswered**.

## What NO video showed (explicit gaps — do not guess past these)

- **No video demonstrates live/streaming Tamil or Tanglish dictation on a 6 GB-class consumer GPU (RTX 3050 or equivalent).** This is the project's core requirement, and it is simply not covered anywhere in this video set.
- **No video reports a VRAM figure for running IndicConformer, IndicWav2Vec, or Whisper large/turbo on Tamil audio.** The only GPU-adjacent figures found are (a) a training-time "24 GPUs for 3 days" for IndicWav2Vec's original training (not inference-relevant), and (b) Whisper's `large` model disk-download size of "7 to 8 GB" (not a VRAM figure).
- **No video shows or discusses how English words embedded in Tamil speech are rendered** — Latin script vs. transliterated Tamil script vs. dropped/mangled — despite this being asked directly by a viewer (video #5 comments) and being central to the project's "Tanglish" requirement. This is the single clearest, most consequential gap.
- **No video reports a measured WER/CER or latency-in-milliseconds figure for Tamil or Tanglish input on any model.** All "accuracy" statements found are subjective ("90% mark," "very good quality," "quite fast") rather than measured.
- **No video demonstrates a fully local, offline voice-assistant loop (ASR → LLM → TTS) that is simultaneously (a) Tamil/Tanglish-capable and (b) running without any cloud API call.** The closest local-only pieces are IndicConformer's batch ASR (videos #1/#2, no LLM/TTS attached) and Whisper's offline CPU test (video #10, no LLM/TTS attached); every voice-*assistant* demo found (videos #4, #7) relies on a cloud LLM/TTS backend.
- **Indic Parler-TTS**, the one video title found that explicitly promises a local Tamil TTS install/test (video #12, X1GK4iSNQJU), could not be retrieved in this pass due to persistent rate-limiting — this is a priority follow-up, not a finding that it doesn't work.
- Auto-captions of Tamil and Tanglish speech in this dataset were **frequently unusable** (videos #4, #8) — several presenters clearly speak substantially in Tamil, and YouTube's English auto-captioner returns disconnected word fragments rather than sentences. Any future research pass should prioritize the **Tamil-language (`ta`) caption tracks** (downloaded alongside for videos #3-supplementary set: PKHA92gusTM, 3eE4ZdnPNZU) and have a Tamil-literate reviewer read them directly, since the English machine captions/translations are not reliable enough to support claims for those videos.

---

*End of report. 14 videos summarised (10 with usable transcript evidence in Part A, 4 metadata-only in Part B), 1 video explicitly skipped with reason in Part C plus ~9 additional skip notes for candidates seen only in the prior research-file lists.*
