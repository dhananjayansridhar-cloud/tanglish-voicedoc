# Research index

Everything collected on 2026-09-24, organised by topic. Nothing was removed. `../research.md` is the single-file dump, with my verification notes in its Part 1. `../research_raw/` holds every raw artefact unchanged.

| Folder | Contents | Main takeaways |
|---|---|---|
| `01_asr_models/` | Hugging Face survey, verification pass, new-lead verification, downloaded model cards (IndicConformer, Indic-Transcribe flex/core, Indic-Speak) | Indic-Transcribe-flex/core are the only local models with a mixed-script (Tanglish) mode and a conversational-Tamil number (developer-reported) |
| `02_llm_organizer/` | Small local LLMs and audio-LLMs | No audio-LLM has proven Tamil ASR; Gemma E4B scores 37.9 Tamil WER on Voice of India |
| `03_tts_and_voice_agents/` | Tamil TTS models, voice-agent frameworks | Indic Parler-TTS, IndicF5 and Indic-Speak support Tamil; pipecat, LiveKit and RealtimeSTT are the active frameworks |
| `04_github_practitioners/` | GitHub issues and discussions, streaming and dictation projects | Whisper code-switching weakness (maintainer quote); faster-whisper multilingual bug #1476; a practitioner routed Tamil to IndicConformer |
| `05_social/reddit/` | PullPush retry and agent-reach OpenCLI collection (275 posts, no comment threads) | Little Tamil ASR discussion on Reddit; Qwen3-ASR Hinglish fine-tune; a Tamil voice-agent thread |
| `05_social/x/` | WebSearch snippets and tw.sh collection (~113 entries) | Indic-Transcribe launch, Whisper Tamil works but Telugu/Kannada fail, the streaming text-revision problem |
| `06_primary_benchmarks/` | Whisper paper Tamil tables, Voice of India full Table 2(a), model-card facts | IndicConformer 19.9 is the best independently measured open model on conversational Tamil |
| `youtube/` | Transcripts, metadata and comments, and `youtube_summaries.md` | see `youtube/youtube_summaries.md` |
| `candidates/` | `candidates.json`: the evidence cards Jev judged | 10 cards: 8 local candidates and 2 controls |
| `jev/` | `run_jev.py`, `jev_raw.json`, `jev_ranking.md` | Default: Indic-Transcribe-flex (weighted 0.704; global Choice p = 0.68) |
| `research_handbacks_s4b_s5b_s7.md` | Verbatim hand-back messages from fetcher agents | — |

Decision document: `../RECOMMENDATION.md`.
