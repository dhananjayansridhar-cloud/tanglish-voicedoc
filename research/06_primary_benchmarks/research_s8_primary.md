## S8 — Primary-source extractions done directly (arXiv MCP + hf CLI), verbatim

### S8.1 Whisper paper (arXiv:2212.04356v1), Appendix D — Tamil WER (%)

Only up to large-v2 is in the paper; large-v3 / turbo Tamil numbers are NOT in this paper.

| Model | Common Voice 9 Tamil (Table 11) | FLEURS Tamil (Table 13) |
|---|---|---|
| Whisper tiny | 105.7 | 99.9 |
| Whisper base | 49.5 | 58.7 |
| Whisper small | 28.7 | 35.2 |
| Whisper medium | 19.6 | 23.1 |
| Whisper large | 17.6 | 20.6 |
| Whisper large-v2 | 16.1 | 17.5 |

Also Table 14 (BLEU, FLEURS speech translation) Tamil: tiny 0.2, base 0.4, small 2.1, medium 7.0, large 8.5, large-v2 9.2. Table 15 (BLEU CoVoST2) Tamil: tiny 0.1, base 0.4, small 1.7, medium 2.9, large 3.7, large-v2 4.2.

### S8.2 Voice of India benchmark (arXiv:2604.19151; AI4Bharat / IIT Madras + Josh Talks)

Abstract (verbatim): "Existing Indic ASR benchmarks often use scripted, clean speech and leaderboard driven evaluation that encourages dataset specific overfitting. In addition, strict single reference WER penalizes natural spelling variation in Indian languages, including non standardized spellings of code-mixed English origin words. To address these limitations, we introduce Voice of India, a closed source benchmark built from unscripted telephonic conversations covering 15 major Indian languages across 139 regional clusters. The dataset contains 306230 utterances, totaling 536 hours of speech from 36691 speakers with transcripts accounting for spelling variations."

Tamil subset (Table 1): 53.4 h, 37 districts, 32.6K utterances, 4434 speakers.

Metric: "Orthographically-Informed Word Error Rate (OIWER) … accounts for permissible spelling variation between hypothesis and reference". "All models are evaluated using their default inference configurations."

Table 2(a), verbatim:

| Model | as | bn | bho | gu | hi | hne | ka | mai | ml | mr | or | pa | **ta** | te | ur |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ElevenLabs Scribe v2 | 15.6 | 10 | 23.5 | 21.2 | 7.7 | 20.3 | 19.2 | - | 23 | 12.9 | 20.7 | 15.6 | **20.4** | 23 | 25.5 |
| Amazon Transcribe | - | 9.1 | 36 | 17.7 | 6.8 | 32.9 | 18.6 | - | 28.2 | 11.3 | 17.9 | 15.9 | **19.3** | 19.7 | - |
| AssemblyAI Universal | 104.8 | 103.8 | 46.1 | 101.8 | 19.3 | 43.6 | 89 | - | 107.5 | 87.6 | - | 101 | **57.4** | 105 | 31.9 |
| Deepgram Nova 3 | - | 28.9 | 45.8 | - | 13 | 42.4 | 53.7 | - | - | 43.7 | - | - | **67.8** | 43.1 | - |
| Gemini 3 Pro | 20.1 | 8.5 | 18.4 | 15.8 | 6 | 17.2 | 19.9 | 25.6 | 21.7 | 10.7 | 20.9 | 14.4 | **15.7** | 21.9 | 9.1 |
| Gemini 3 Flash | 26.9 | 12.6 | 22.6 | 22.5 | 8.3 | 23.9 | 22.2 | 30.8 | 27.1 | 16 | 26.1 | 19.4 | **19.9** | 27.9 | 11.9 |
| GPT-4o Transcribe | 94.7 | 44.9 | 49 | 98.2 | 33.9 | 45.2 | 84.2 | 60.4 | 97 | 55.6 | 72.5 | 70.1 | **64.2** | 69.3 | 35.4 |
| GPT-4o Mini Transcribe | 37.6 | 21.1 | 49.1 | 295.9 | 19.6 | 44.6 | 97.5 | 45.6 | 167.8 | 30.7 | 42.1 | 37.9 | **51.9** | 81.2 | 52 |
| Indic Conformer (open) | 14.3 | 10.7 | 35.4 | 18 | 8.2 | 31.6 | 21.4 | 24.7 | 26 | 13.1 | 14.4 | 14.9 | **19.9** | 23.7 | 8.1 |
| Microsoft Speech-to-Text | - | 25.4 | 38.1 | - | 11.4 | 34.5 | - | - | 40.9 | 31.9 | - | - | **28** | - | 25.2 |
| OmniASR LLM 1B (open) | 29.2 | 29.7 | 32.8 | 38.9 | 14.9 | 27.3 | 45.7 | 47.7 | 58.4 | 31.2 | 89.8 | 36.5 | **49** | 57.3 | 17.2 |
| OmniASR LLM 7B (open) | 25.3 | 22.8 | 31.4 | 34.1 | 13.7 | 26.3 | 39.2 | 48.2 | 52 | 26.3 | 72.6 | 33.3 | **43.1** | 50.7 | 16 |
| Sarvam Audio | 12.7 | 6.1 | 20.9 | 12.8 | 5 | 17.6 | 16.3 | 24.8 | 18.9 | 9.4 | 14 | 11.2 | **14.2** | 18.2 | 7 |
| Saarika 2.5 | - | 8.2 | 29.6 | 14 | 6.2 | 26 | 16.4 | - | 18.9 | 10 | 15.1 | 12.5 | **14.9** | 18.9 | - |

Other verbatim passages:
- "most models exceed a WER of 20 (highlighted in red), a threshold often associated with practical usability … Sarvam Audio achieves the lowest WER in 13 of 15 languages, followed by Saarika 2.5 and Gemini 3 Pro. Indic Conformer and ElevenLabs Scribe v2 show moderate performance".
- "Tier I: Top-performing systems (Ranks 1–6, WER ≤ 20%). Tier I models (Sarvam-Audio, Gemini-3-Pro, IndicConformer) largely solve general multilingual transcription but … models fail catastrophically for out-of-region migrants (e.g., Chattisgarhi speakers in Tamil Nadu face WERs of 55%-65%)."
- "Tier III … Deepgram Nova-3 and OmniASR yield elevated error rates in Tamil (WER: 67.8%) …"
- "models that achieve strong WER on FLEURS often perform substantially worse on our benchmark, particularly for morphologically richer languages."
- "Speaking rate exhibits a U-shaped pattern, with Indic Conformer WER peaking at 27.57% (slow) and 27.53% (very fast) versus 24.75% at moderate speeds. Short utterances are most affected due to limited semantic context".
- Reference transcripts: "Initial transcripts were generated using internally fine-tuned Whisper models for 11 languages and the Indic Conformer model for Assamese, Odia, Urdu, and Maithili", then native-speaker verification and "six rounds of cross-validation".
- "Raw recordings were segmented into utterances using WebRTC VAD".
- Open-source OpenAI Whisper checkpoints were NOT among the 14 evaluated systems. "OmniASR" = Meta Omnilingual ASR, which exists (S6 wrongly reported it as non-existent).

### S8.3 Vistaar (arXiv:2305.15386) and "IndicVoices"
- Vistaar: a text search for "Tamil" returned only dataset descriptions (IISc-MILE: "read speech recorded in a clean, noise-free environment … Tamil and Kannada data were recorded from 531 and 915 native speakers") and references. The per-language WER table did not surface — NOT COVERED.
- arXiv:2409.05356, which S6 recorded as "IndicVoices", is actually "IndicVoices-R: Unlocking a Massive Multilingual Multi-speaker Speech Corpus for Scaling Indian TTS" — a TTS corpus paper. S6 mis-identified it; the IndicVoices ASR paper was not retrieved.

### S8.4 IndicConformer model cards (downloaded via logged-in `hf` CLI; full text in the S6 section)
- `ai4bharat/indic-conformer-600m-multilingual`: MIT; "Multilingual Conformer-based Hybrid CTC + RNNT ASR model"; 600M; IN-22 incl. Tamil (`ta`); runs via `transformers` `AutoModel.from_pretrained(..., trust_remote_code=True)` with `onnxruntime-gpu==1.20.1`; call `model(wav, "ta", "ctc"|"rnnt")`; 16 kHz mono. No streaming mentioned. No WER in the card.
- `ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large`: MIT; Tamil-only; "conformer-Large model, consisting of 120M parameters … 17 conformer blocks with 512 as the model dimension"; requires the AI4Bharat NeMo fork (`nemo-v2` branch, `bash reinstall.sh`, a Linux-oriented script). No streaming mentioned, no WER in the card.
- Which IndicConformer variant Voice of India evaluated is not stated in the extracted text (cited as "[31]").

### S8.5 X/Twitter spot check via tw.sh (my own test query, verbatim first hit)
- @justkarangupta, 2026-08-03, 26 likes: "Built Aria: realtime multilingual voice assistant. … Recognition on Groq Whisper, replies from LLaMA 3.3 70B, speech out through Microsoft Edge TTS, free tiers end to end. … detect speech → think → speak, usually in a few seconds, with barge-in so the agent yields when you talk. … Automatic speech detection (Silero VAD, no push-to-talk) - 15 languages (English, Hindi, Spanish, French, Japanese, Tamil, and more) … LiveKit Agents · Groq Whisper + LLaMA 3.3 70B · Microsoft Edge TTS · Silero VAD". (Builder showcase; no Tamil accuracy data.)
