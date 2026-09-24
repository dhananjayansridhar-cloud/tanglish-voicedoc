# Research Log — Live Tanglish Voice-to-Document Assistant

Started 2026-09-24. Hardware: RTX 3050 Laptop GPU 6144 MiB, driver 610.88, Windows 11, Python 3.10.11 (`.venv`).

This file contains **every** research output verbatim (Part 2), plus the verification notes I made while reviewing them (Part 1). Nothing has been removed, including weak, contradictory or unverified material. Raw sources were collected by fetcher agents instructed to quote verbatim and write `NOT COVERED` for gaps; their files are appended unedited. Where I found a fetcher error, it is flagged in Part 1, not silently corrected in Part 2.

## Requirements as stated by the user (verbatim, in order)

1. "I want a Voice recognition model which can convert my colloqial Tamil+ Indian English speech in to a live document with auto organizing and formatting ability which organized my data as per my command... Ideally I would prefer a single model which can understand colloquial tamil(which obviously have mix of english words in it, which we call as tanglish)."
2. "you have huggingface and github access do a proper research and come back"
3. "But it should do the job and not simply fit inside but cant do it efficiently. It should be proven and also discussed well in youtube channels"
4. "Not just youtube channels also in reddit and twitter."
5. "I should be able to do live dictation and update the document alive..not offline or pre-recorded!"
6. "If possible if there is a voice based reply option.to have a converation..that'll be ideal so if there are any doubts they can be clarified"
7. "instead of blindly wriing what i simply say without pushback or clarification"
8. "write all your research data in reseach.md fully without misisn ANYTHING, whether good or bad"

## Selection criteria derived from the requirements

| # | Criterion | Source requirement |
|---|---|---|
| C1 | Published Tamil WER/CER on a named dataset | 3 |
| C2 | Practitioner confirmation on colloquial / code-switched Tamil | 3, 4 |
| C3 | Independent community discussion (YouTube, Reddit, X) | 3, 4 |
| C4 | Real-time on RTX 3050 6 GB alongside the other models (measured, not estimated) | 3 |
| C5 | Streaming / live partial output, ~1–2 s latency | 5 |
| C6 | Per-token/word confidence available (needed to ask "did you say X?") | 7 |
| C7 | Tamil/Tanglish TTS + turn-taking for spoken clarification | 6 |
| C8 | Reasoning model with genuine colloquial-Tamil understanding | 7 |

## Research streams

| Stream | File (appended below) | Status |
|---|---|---|
| S1 Hugging Face ASR survey | `research_asr_hf.md` | done |
| S2 GitHub / forum practitioners + streaming projects | `research_practitioner.md` | done |
| S3 Local LLMs + audio-LLMs ("single model") | `research_llm.md` | done |
| S4 YouTube | `research_youtube.md` | running |
| S5 Reddit + X/Twitter | `research_social.md` | running |
| S6 Verification: gated cards, Vistaar, Whisper Tamil WER, IndicVoices, Sarvam, Omnilingual, leaderboards | `research_verify.md` | running |
| S7 Tamil TTS + voice-agent frameworks | `research_tts_agent.md` | running |

---

# Part 1 — Verification notes (my review of the raw material)

### On S1 (Hugging Face ASR survey)
- **Gap, fetcher error:** Whisper large-v3 / turbo / small / medium have `Tamil WER: NOT COVERED`. OpenAI did publish per-language FLEURS WER (paper appendix / repo plot). Missing because the fetcher only read model cards. Re-requested in S6.
- **Gap, access:** Both AI4Bharat IndicConformer cards were gated (auth error). The HF CLI on this machine is logged in; re-requested in S6.
- **Unverified estimates:** Every `VRAM Requirement` line in S1 is the fetcher's own estimate ("estimated 1.5-3GB"), not a sourced figure. Do not treat as evidence; C4 will be measured.
- **Unsupported claim:** "Streaming Support: Yes" for Whisper models rests on `chunk_length_s=30` (chunked long-form batch inference), which is **not** live streaming. Whisper has no native streaming; live use requires external chunking (e.g. ufal/whisper_streaming LocalAgreement, see S2 B1).
- **Unsupported claim:** vasista22 "Streaming Support: Yes, supports whisper-jax" — whisper-jax is batch acceleration, not streaming.
- **Solid finding:** `vasista22/whisper-tamil-medium` card states FLEURS ta_in test WER 6.97 and Common Voice 11 ta test WER 6.5. These are read/prompted speech sets, not colloquial or code-switched.
- **Solid finding:** Qwen3-ASR (0.6B/1.7B) language list does not include Tamil → excluded despite native streaming.
- **Solid finding (negative):** no HF model card examined reports Tamil–English code-switched WER.

### On S2 (practitioner survey)
- **Fetcher inference flagged:** B13 HeySpeaky "Notable: Designed specifically to handle language-switching mid-dictation (English-Tamil code-switching scenario)." The quoted repo description says only "survives switching language mid-sentence"; **Tamil is not mentioned in the quote.** 5 stars. Treat as unproven for Tamil.
- **Attribution to check:** A2 — the final line ("Whisper commits to a single language token per 30-second audio window…") is not marked as the maintainer's words and may be a paraphrase; the maintainer line "Whisper doesn't support code-switching inputs very well" is the load-bearing quote. The date is Unknown.
- **Strong, design-relevant:** A3 (faster-whisper issue #1476, 2026-09-10): with `multilingual=True`, a window can be decoded in the previous window's language unless `condition_on_previous_text=False`. Directly relevant to Tanglish, where the language flips inside a sentence.
- **Strong:** A7 (a Tamil developer, 2025-12-04) chose to route Tamil away from Whisper to `ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large` via NeMo because "Whisper's accuracy is not as good". Single practitioner, no numbers.
- **Vendor claim (not independent):** A9 Sarvam "Streaming speech recognition for 22 Indian languages… code-mixed support". Cloud API.
- **Hallucination evidence:** A4/A5 — Whisper large-v3 non-empty output for 40.3% of non-speech inputs (research paper). Implies a VAD gate is mandatory for live dictation.

### On S3 (local LLMs + audio-LLMs)
- **Fetcher broke the no-ranking instruction:** its summary labels Sarvam-1 "BEST FIT" and proposes an architecture. That is the fetcher's opinion, not evidence; disregarded for decision-making, kept in the raw file.
- **Likely false negative:** "Phi-4-Mini (does not exist as separate product)". Microsoft publishes `microsoft/Phi-4-mini-instruct` and `microsoft/Phi-4-multimodal-instruct` (audio input). To be verified directly before the final pick.
- **Omission:** Gemma 3n (E2B/E4B, audio input) was in the brief but is not in the summary's model list. To be checked.
- **Contradiction to resolve:** summary says Sarvam-1 has a "non-commercial license" and is "instruction-capable"; Sarvam-1 was released as a base model. Check the card text in the raw file.
- **Finding (negative, as reported):** Voxtral Mini 3B / 4B-Realtime, Granite Speech 4.1-2B, Sarvam Shuka-1 do not list Tamil for audio input. Qwen2.5-Omni-3B Tamil audio support NOT COVERED.
- **Gap:** no Tamil benchmark numbers for any LLM; no GGUF file sizes; no Ollama 6 GB offload data.

### On S4 (YouTube)
- **Weak collection:** 54 video IDs found via yt-dlp, but the file contains titles/metadata only — no presenter verdicts, no accuracy observations, no comments. The 5 transcripts were downloaded but not read by the fetcher. Tamil-language queries were skipped ("NOT TESTED"). The "Key Findings" list in the raw file is the fetcher's own interpretation of titles, not evidence.
- **Remediation:** stream S4b (`research_youtube_quotes.md`) extracts verbatim verdicts from transcripts, descriptions and top comments, and runs the Tamil-language queries.
- **Signal from titles alone (weak):** community activity exists for faster-whisper realtime (uimBp3c3Koo, 31k views), IndicConformer pipelines (Sudheendra S G, 2026-05), Sarvam voice agents in Tamil (AI with Thiru, 2026-03), Indic Parler-TTS local install with Tamil (Fahd Mirza, 2024-12), a Tamil "listen, think & speak" Python assistant (Karthik's Show, 2026-07). View counts are small (50–31k): Tamil local-ASR is **not** a heavily reviewed topic on YouTube.

### On S5 (Reddit + X/Twitter)
- **Coverage failure:** Reddit 0 entries (all access blocked). X full posts blocked (HTTP 402); quotes are search-result snippets only. Remediation: stream S5b (`research_social_retry.md`) via Reddit JSON / PullPush / xcancel / syndication endpoints.
- **Vendor-dominated:** fetcher reports ~60% of X entries are vendor announcements; only 1 independent user report, and it is about Kannada, not Tamil.
- **Most important lead:** "Voice of India" benchmark (AI4Bharat/IIT Madras + Josh Talks, Feb 2026) — "measures how well AI models understand real-world Indian speech across languages, accents, code-switching, and noisy conditions." This is the only evaluation found so far that targets code-switched real-world speech. Its Tamil numbers are requested in S6 task 7.
- **Leads to verify:** Sarvam Saaras V3 (May 2026) vendor claim "particularly for mixed-language and noisy speech" — API product. SraVaani 1.0 (IISc SPIRE Lab + ARTPARK + Google, Aug 2026, 65 Indian languages) — Tamil not explicitly named in the quote; open-weights status unknown.

(Notes for S6, S7 and the retry streams are added as they complete.)

---

# Part 2 — Raw research files (verbatim, unedited)



---

## S1 raw file: `research_asr_hf.md` (498 lines, verbatim)

# ASR Models for Tamil + English Code-Switching (Tanglish)
## Research Date: 2026-09-24
### Target: RTX 3050 Laptop GPU (6GB VRAM), Windows, Python 3.10

---

## OpenAI Whisper Series

### openai/whisper-large-v3
- **HF Repo ID:** openai/whisper-large-v3
- **Parameters:** 1,550 M
- **License:** MIT
- **Last Modified:** 2024-08-12
- **Downloads:** 4,700,322
- **Languages:** 99 languages including Tamil (ta)
- **Tamil WER:** NOT COVERED (model card does not specify Tamil-specific WER metrics)
- **Code-switched Tamil-English:** NOT COVERED (no mention of code-switching support in README)
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** Yes, supports chunked algorithm with 30-second optimal chunk length
  - Source: https://huggingface.co/openai/whisper-large-v3/raw/main/README.md "chunk_length_s=30 parameter"
- **Runtime:** transformers, pytorch, jax, safetensors
- **VRAM Requirement:** NOT COVERED (estimated 3-6GB based on 1.5B params with fp16)
- **Notes:** Multilingual model trained on ~99 languages. Updated October 2024.

### openai/whisper-large-v3-turbo
- **HF Repo ID:** openai/whisper-large-v3-turbo
- **Parameters:** 1,550 M (optimized/distilled version)
- **License:** Apache 2.0 / MIT
- **Last Modified:** 2024-10-04
- **Downloads:** 6,530,592
- **Languages:** 99+ languages including Tamil (ta)
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** Yes, optimized for faster inference
- **Runtime:** transformers, safetensors
- **VRAM Requirement:** NOT COVERED (smaller than large-v3, estimated 2.5-5GB with fp16)
- **Notes:** Turbo variant designed for speed. Most downloaded Whisper model (6.5M).

### openai/whisper-small
- **HF Repo ID:** openai/whisper-small
- **Parameters:** 244 M
- **License:** MIT
- **Last Modified:** 2024-02-29
- **Downloads:** 2,950,422
- **Languages:** 99 languages including Tamil (ta)
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** Yes
- **Runtime:** transformers, pytorch, tf, jax, safetensors
- **VRAM Requirement:** NOT COVERED (estimated 0.5-1.5GB with fp16)
- **Notes:** Smaller model suitable for resource-constrained environments.

### openai/whisper-medium
- **HF Repo ID:** openai/whisper-medium
- **Parameters:** 769 M
- **License:** MIT
- **Last Modified:** 2024-02-29
- **Downloads:** 302,910
- **Languages:** 99 languages including Tamil (ta)
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** Yes
- **Runtime:** transformers, pytorch, tf, jax, safetensors
- **VRAM Requirement:** NOT COVERED (estimated 1.5-3GB with fp16)
- **Notes:** Medium-sized model, balance between quality and resource usage.

---

## Tamil-Specific Whisper Fine-tunes

### vasista22/whisper-tamil-medium
- **HF Repo ID:** vasista22/whisper-tamil-medium
- **Parameters:** 769 M (from openai/whisper-medium)
- **License:** Apache 2.0
- **Last Modified:** NOT COVERED
- **Downloads:** 776
- **Languages:** Tamil (ta)
- **Tamil WER:**
  - google/fleurs (ta_in, test): **6.97%** (exact quote from model card)
    - Source: https://huggingface.co/vasista22/whisper-tamil-medium/raw/main/README.md
  - mozilla-foundation/common_voice_11_0 (ta, test): **6.5%** (exact quote from model card)
    - Source: https://huggingface.co/vasista22/whisper-tamil-medium/raw/main/README.md
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** Yes, supports whisper-jax for faster inference
  - Source: model card mentions "faster inference using whisper-jax"
- **Runtime:** transformers, whisper-jax (optional for acceleration)
- **VRAM Requirement:** NOT COVERED (estimated 1.5-3GB with fp16, same as base model)
- **Training Data:** IISc-MILE, ULCA ASR Corpus, Shrutilipi, Microsoft Speech Corpus (Indian Languages), Google Fleurs, Babel
  - Source: https://huggingface.co/vasista22/whisper-tamil-medium/raw/main/README.md
- **Notes:** Fine-tuned on multiple public Tamil ASR datasets. Strong WER numbers. Most relevant baseline for Tamil.

### vasista22/whisper-tamil-small
- **HF Repo ID:** vasista22/whisper-tamil-small
- **Parameters:** 244 M (from openai/whisper-small)
- **License:** Apache 2.0
- **Last Modified:** NOT COVERED
- **Downloads:** 151,305
- **Languages:** Tamil (ta)
- **Tamil WER:** NOT COVERED (no metrics published in model card)
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** Yes, supports whisper-jax
- **Runtime:** transformers, whisper-jax
- **VRAM Requirement:** NOT COVERED (estimated 0.5-1.5GB with fp16)
- **Notes:** Smaller variant of Tamil fine-tune. Higher downloads than medium variant (151k vs 776).

### vasista22/whisper-tamil-large-v2
- **HF Repo ID:** vasista22/whisper-tamil-large-v2
- **Parameters:** 1,550 M (from openai/whisper-large-v2)
- **License:** Apache 2.0
- **Last Modified:** NOT COVERED
- **Downloads:** 664
- **Languages:** Tamil (ta)
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** Yes
- **Runtime:** transformers
- **VRAM Requirement:** NOT COVERED (estimated 3-6GB with fp16)
- **Notes:** Largest Tamil fine-tune variant. Fewer downloads than smaller variants.

---

## Harveenchadha Vakyansh Series

### Harveenchadha/vakyansh-wav2vec2-tamil-tam-250
- **HF Repo ID:** Harveenchadha/vakyansh-wav2vec2-tamil-tam-250
- **Parameters:** 300 M (CLSRIL-23 base model)
- **License:** MIT
- **Last Modified:** NOT COVERED
- **Downloads:** 1,370,172 (highest among all Tamil models)
- **Languages:** Tamil (ta)
- **Tamil WER:**
  - Common Voice ta (test): **53.64%** (exact quote from model card)
    - Source: https://huggingface.co/Harveenchadha/vakyansh-wav2vec2-tamil-tam-250/raw/main/README.md
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** NOT COVERED
- **Runtime:** transformers (Wav2Vec2ForCTC)
- **VRAM Requirement:** NOT COVERED (estimated 0.8-2GB with fp16)
- **Training Data:** 4,200 hours of Hindi labelled data (NOT public domain as of model publish date)
  - Source: model card states "trained on 4200 hours of Hindi Labelled Data"
- **Notes:** 
  - "Note: The result from this model is without a language model so you may witness a higher WER in some cases." (exact quote)
  - Based on multilingual CLSRIL-23 model
  - WITHOUT language model, WER is much higher than Whisper fine-tunes
  - Most downloaded Tamil ASR model overall

---

## Meta MMS (Massively Multilingual Speech)

### facebook/mms-1b-all
- **HF Repo ID:** facebook/mms-1b-all
- **Parameters:** 1,000 M (1B)
- **License:** CC-BY-NC-4.0
- **Last Modified:** NOT COVERED
- **Downloads:** 299,178
- **Languages:** 1,107 languages including Tamil (ta)
  - Source: https://huggingface.co/facebook/mms-1b-all/raw/main/README.md "fine-tuned...on 1162 languages"
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** Adapter-based architecture switches language via `set_target_lang("tam")` and `load_adapter("tam")`
  - Source: model card shows example "processor.tokenizer.set_target_lang("fra")" for language switching
- **Streaming Support:** NOT COVERED
- **Runtime:** transformers (Wav2Vec2ForCTC with adapter architecture)
- **VRAM Requirement:** NOT COVERED (estimated 2-4GB with fp16 for single language adapter)
- **Dataset Evaluation:** google/fleurs
  - Source: README lists fleurs in metrics tag
- **Notes:** 
  - Adapter-based: same 1B base model, language-specific adapters loaded per language
  - Requires `transformers >= 4.30`
  - Tamil adapter available as "tam" language code

---

## AI4Bharat IndicConformer Series

### ai4bharat/indic-conformer-600m-multilingual
- **HF Repo ID:** ai4bharat/indic-conformer-600m-multilingual
- **Parameters:** 600 M
- **License:** NOT COVERED (model is gated/restricted access)
- **Last Modified:** NOT COVERED
- **Downloads:** 522,592
- **Languages:** Indic languages (Tamil included)
- **Tamil WER:** NOT COVERED (restricted model, README inaccessible: "Access to model...is restricted. You must have access to it and be authenticated")
  - Source: Attempted fetch https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual/raw/main/README.md returned auth error
- **Code-switched Tamil-English:** NOT COVERED (gated model)
- **Output Script Behavior:** NOT COVERED (gated model)
- **Streaming Support:** NOT COVERED
- **Runtime:** NOT COVERED (likely NeMo-based)
- **VRAM Requirement:** NOT COVERED (estimated 1.5-2.5GB with fp16 based on 600M params)
- **Notes:** 
  - Gated model requiring explicit access approval
  - Trained on Indic Speech datasets
  - IndicConformer architecture (NVIDIA/AI4Bharat collaboration)

### ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large
- **HF Repo ID:** ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large
- **Parameters:** NOT COVERED
- **License:** NOT COVERED
- **Last Modified:** NOT COVERED
- **Downloads:** 470
- **Languages:** Tamil (ta) only
- **Tamil WER:** NOT COVERED (gated/restricted access)
- **Code-switched Tamil-English:** NOT COVERED (gated model)
- **Output Script Behavior:** NOT COVERED (gated model)
- **Streaming Support:** NOT COVERED
- **Runtime:** NOT COVERED (likely NeMo-based, hybrid CTC/RNN-T architecture)
- **VRAM Requirement:** NOT COVERED
- **Notes:** 
  - Model card inaccessible: "Access to model...is restricted. You must have access to it and be authenticated"
  - Hybrid CTC/RNN-T decoding strategy
  - Gated model (requires request for access)

### ai4bharat/indic-seamless
- **HF Repo ID:** ai4bharat/indic-seamless
- **Parameters:** NOT COVERED
- **License:** NOT COVERED
- **Last Modified:** NOT COVERED
- **Downloads:** 12,045
- **Languages:** Indic languages (Tamil included)
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** NOT COVERED
- **Runtime:** NOT COVERED (likely SeamlessM4T-based)
- **VRAM Requirement:** NOT COVERED
- **Notes:** AI4Bharat adaptation of Seamless architecture for Indic languages

---

## Meta SeamlessM4T Series

### facebook/seamless-m4t-v2-large
- **HF Repo ID:** facebook/seamless-m4t-v2-large
- **Parameters:** 2,300 M (2.3B)
- **License:** CC-BY-NC-4.0
- **Last Modified:** NOT COVERED
- **Downloads:** 304,813
- **Languages:** 101 languages for speech input including Tamil (ta)
  - Exact quote from README: "🎤 101 languages for speech input" and Tamil listed in language tags
  - Source: https://huggingface.co/facebook/seamless-m4t-v2-large/raw/main/README.md
- **Tamil WER:** NOT COVERED (model card provides only general metrics links, not language-specific WER)
  - Metrics available at: https://dl.fbaipublicfiles.com/seamless/metrics/seamlessM4T_large_v2.zip (not human-readable in README)
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** Multilingual output; can generate speech or text in 96 target languages
  - Source: "💬 96 Languages for text input/output" and "🔊 35 languages for speech output"
- **Streaming Support:** NOT COVERED (designed for speech-to-speech, speech-to-text, text-to-speech translation)
- **Runtime:** transformers (SeamlessM4Tv2Model)
- **VRAM Requirement:** NOT COVERED (estimated 5-9GB with fp16 for 2.3B params)
- **Training Data:** Evaluated on FLEURS, CoVoST2, CVSS-C datasets
  - Source: "evaluation data ids for FLEURS, CoVoST2 and CVSS-C can be found here"
- **Novel Architecture:** UnitY2 with hierarchical character-to-unit upsampling and non-autoregressive text-to-unit decoding
  - Source: README describes "*Unity2* architecture...improves over SeamlessM4T v1 in quality and inference speed"
- **Notes:** 
  - Multitask model (S2ST, S2TT, T2ST, T2TT, ASR in one model)
  - Improved over v1 in quality and inference speed
  - Commercial license (CC-BY-NC-4.0, non-commercial only)

---

## Qwen3 ASR Series

### Qwen/Qwen3-ASR-1.7B
- **HF Repo ID:** Qwen/Qwen3-ASR-1.7B
- **Parameters:** 1,700 M (1.7B)
- **License:** Apache 2.0
- **Last Modified:** NOT COVERED
- **Downloads:** 2,044,581
- **Languages:** 30 languages + 22 Chinese dialects claimed
  - Exact quote: "support language identification and ASR for 30 languages and 22 Chinese dialects, so as to English accents from multiple countries and regions"
  - Supported languages listed: Chinese, English, Cantonese, Arabic, German, French, Spanish, Portuguese, Indonesian, Italian, Korean, Russian, Thai, Vietnamese, Japanese, Turkish, Hindi, Malay, Dutch, Swedish, Danish, Finnish, Polish, Czech, Filipino, Persian, Greek, Hungarian, Macedonian, Romanian
  - Source: https://huggingface.co/Qwen/Qwen3-ASR-1.7B/raw/main/README.md
  - **Tamil status: NOT EXPLICITLY MENTIONED** in language list (NOT COVERED)
- **Tamil WER:** NOT COVERED (no Tamil evaluation, Tamil not in supported language list)
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** Generates UTF-8 text output with language identification
  - Source: Code example shows `results[0].language` and `results[0].text`
- **Streaming Support:** Yes, unified streaming and offline inference with single model
  - Exact quote: "support streaming / offline unified inference with single model"
  - Source: README features section
- **Runtime:** Transformers backend (primary), vLLM backend (optional for faster inference)
- **VRAM Requirement:** NOT COVERED explicitly; README recommends FlashAttention 2 for "reduce GPU memory usage"
- **Timestamp Support:** Yes, via Qwen3-ForcedAligner-0.6B
  - Source: README mentions forced alignment support
- **Performance:** "achieves strong performance on both open-sourced and internal benchmarks"
  - Source: README, no specific WER numbers provided
- **Notes:** 
  - Does NOT support Tamil (not in language list)
  - FlashAttention 2 recommended for reducing VRAM
  - Batch inference support via vLLM backend
  - New Qwen3-Omni foundation model underlying architecture

### Qwen/Qwen3-ASR-0.6B
- **HF Repo ID:** Qwen/Qwen3-ASR-0.6B
- **Parameters:** 600 M
- **License:** Apache 2.0
- **Last Modified:** NOT COVERED
- **Downloads:** 583,906
- **Languages:** 30 languages + 22 Chinese dialects (same as 1.7B model)
  - **Tamil status: NOT COVERED (NOT in supported languages)**
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** Same as 1.7B (language identification + transcription)
- **Streaming Support:** Yes, unified streaming and offline
- **Runtime:** Transformers, vLLM optional
- **VRAM Requirement:** NOT COVERED (estimated 0.8-2GB with fp16, lighter than 1.7B)
- **Performance:** "reaches 2000 times throughput at a concurrency of 128" (efficiency-focused)
  - Source: README
- **Notes:** 
  - Does NOT support Tamil
  - Efficiency-optimized version of 1.7B
  - Lower throughput target than 1.7B but uses less VRAM

---

## Additional Wav2Vec2-based Tamil Models

### Amrrs/wav2vec2-large-xlsr-53-tamil
- **HF Repo ID:** Amrrs/wav2vec2-large-xlsr-53-tamil
- **Parameters:** NOT COVERED (XLSR-53 base ~300M)
- **License:** NOT COVERED
- **Last Modified:** NOT COVERED
- **Downloads:** 2,951
- **Languages:** Tamil (ta)
- **Tamil WER:** NOT COVERED
- **Code-switched Tamil-English:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** NOT COVERED
- **Runtime:** transformers (Wav2Vec2ForCTC)
- **VRAM Requirement:** NOT COVERED (estimated 0.8-1.5GB)
- **Notes:** XLSR-53 multilingual model fine-tuned for Tamil

### Anujgr8/wav2vec2-base-Tamil-large
- **HF Repo ID:** Anujgr8/wav2vec2-base-Tamil-large
- **Parameters:** NOT COVERED
- **License:** NOT COVERED
- **Last Modified:** NOT COVERED
- **Downloads:** 1,195
- **Languages:** Tamil (ta)
- **Tamil WER:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** NOT COVERED
- **Runtime:** transformers (Wav2Vec2ForCTC)
- **VRAM Requirement:** NOT COVERED
- **Notes:** Community-contributed Tamil model

### nikhil6041/wav2vec2-large-xlsr-tamil-commonvoice
- **HF Repo ID:** nikhil6041/wav2vec2-large-xlsr-tamil-commonvoice
- **Parameters:** NOT COVERED
- **License:** NOT COVERED
- **Last Modified:** NOT COVERED
- **Downloads:** 698
- **Languages:** Tamil (ta)
- **Tamil WER:** NOT COVERED
- **Output Script Behavior:** NOT COVERED
- **Streaming Support:** NOT COVERED
- **Runtime:** transformers (Wav2Vec2ForCTC)
- **VRAM Requirement:** NOT COVERED
- **Notes:** Fine-tuned on Common Voice Tamil dataset

---

## Code-Switching Research Summary

### Search Results for Tamil-English Code-Switching ASR

**Status:** Code-switching specific models were NOT FOUND in Hugging Face search results for Tamil-English mixed speech.

**Findings:**
- No published models explicitly labeled as "code-switching" or "Tanglish" on Hugging Face
- Major multilingual models (Whisper, MMS, SeamlessM4T) claim to support Tamil but do NOT publish code-switched evaluation metrics
- Whisper fine-tunes for Tamil (vasista22 series) trained on standard datasets WITHOUT explicit code-switching labels
- AI4Bharat IndicConformer models are gated; code-switching support status NOT COVERED

**Research Gap:** 
Code-switching performance for Tamil-English mixed speech is NOT documented in any of the model cards examined.
No baseline WER/CER numbers available for Tamil-English code-switched audio on publicly available ASR models as of 2026-09-24.

---

## VRAM Feasibility Analysis for RTX 3050 (6GB)

### Viable for RTX 3050 with 6GB VRAM (estimated):
- ✓ **openai/whisper-small** (244M params): ~1GB model + ~0.5GB inference = ~1.5GB total
- ✓ **vasista22/whisper-tamil-small** (244M params): ~1GB model + ~0.5GB inference = ~1.5GB total
- ✓ **Harveenchadha/vakyansh-wav2vec2-tamil-tam-250** (300M params): ~1GB model + ~0.5GB inference = ~1.5GB total
- ✓ **openai/whisper-medium** (769M params): ~2GB model + ~1GB inference = ~3GB total (marginal)
- ✓ **vasista22/whisper-tamil-medium** (769M params): ~2GB model + ~1GB inference = ~3GB total (marginal)
- ✓ **Qwen/Qwen3-ASR-0.6B** (600M params): ~1.2GB model + ~0.8GB inference = ~2GB total
- ✓ **ai4bharat/indic-conformer-600m-multilingual** (600M params, estimated): ~1.2GB + ~0.8GB = ~2GB (needs access)

### NOT Viable for RTX 3050 with 6GB VRAM:
- ✗ **openai/whisper-large-v3** (1.55B params): ~4GB model + ~2GB inference = ~6GB+ (at or over limit)
- ✗ **openai/whisper-large-v3-turbo** (1.55B params, optimized): ~3.5GB model + ~2GB inference = ~5.5GB (tight fit, risky)
- ✗ **openai/whisper-medium** (1.55B): same as above
- ✗ **vasista22/whisper-tamil-large-v2** (1.55B params): ~4GB model + ~2GB inference = ~6GB+ (at or over limit)
- ✗ **facebook/mms-1b-all** (1B params): ~3GB model + ~1.5GB inference = ~4.5GB (possibly viable with quantization)
- ✗ **Qwen/Qwen3-ASR-1.7B** (1.7B params): ~4.5GB model + ~2GB inference = ~6.5GB+ (over limit)
- ✗ **facebook/seamless-m4t-v2-large** (2.3B params): ~6GB model + ~2GB inference = ~8GB+ (far over limit)

---

## Compilation Status

**Models researched:** 20+
**Models with published Tamil WER:** 2
  - vasista22/whisper-tamil-medium: 6.97% (FLEURS), 6.5% (Common Voice)
  - Harveenchadha/vakyansh-wav2vec2-tamil-tam-250: 53.64% (Common Voice, no LM)

**Models with code-switching evaluation:** 0

**Gated/Restricted models preventing full analysis:** 2
  - ai4bharat/indic-conformer-600m-multilingual
  - ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large

**Models explicitly supporting Tamil:** 11
  - openai/whisper-* series (5 models)
  - vasista22/whisper-tamil-* (3 models)
  - facebook/mms-1b-all
  - facebook/seamless-m4t-v2-large
  - Harveenchadha/vakyansh-wav2vec2-tamil-tam-250

**Models NOT supporting Tamil:** 2
  - Qwen/Qwen3-ASR-1.7B
  - Qwen/Qwen3-ASR-0.6B

---

## Candidates Not Found / Unable to Access

1. **Sarvam AI speech models** (sarvamai/saarika, sarvamai/saaras, sarvamai/shuka)
   - Status: Text-generation and audio-text-to-text models found, NOT standalone ASR models
   - Sarvam AI appears to focus on multilingual LLMs and multimodal models, not dedicated ASR

2. **NVIDIA NeMo/Parakeet with Tamil support**
   - Status: Only English variants found on HF (parakeet_tdt_ctc, parakeet_tdt_transducer)
   - Tamil variant, if it exists, not published to public HF

3. **Explicit Tamil-English code-switching ASR datasets or models**
   - Status: NOT FOUND on Hugging Face
   - No public models trained specifically on code-switched Tamil-English audio

4. **IndicWhisper / IndicVaspthaar variants**
   - Status: NOT FOUND on current Hugging Face (may be in private/gated repos or published only on other platforms)

5. **Gemma 3n / Voxtral / Phi-4-multimodal audio-LLM with Tamil**
   - Status: NOT FOUND as ASR-specific models
   - Gemma 3 / Phi models are text-centric; Tamil audio support NOT documented

---

## Key Findings Summary

1. **Best Published Tamil WER baselines:**
   - vasista22/whisper-tamil-medium: 6.97% FLEURS, 6.5% Common Voice (RECOMMENDED BASELINE)
   - Harveenchadha/vakyansh: 53.64% Common Voice (no language model)

2. **RTX 3050 (6GB VRAM) Recommended Models:**
   - **Primary choice:** vasista22/whisper-tamil-small (244M, ~1.5GB total)
   - **Larger option:** vasista22/whisper-tamil-medium (769M, ~3GB total, marginal fit)
   - **Backup lightweight:** Qwen/Qwen3-ASR-0.6B if Tamil not required (600M, ~2GB) — but Tamil NOT supported
   - **Very lightweight:** Harveenchadha/vakyansh-wav2vec2-tamil-tam-250 (300M, ~1.5GB) — poor WER without LM

3. **Code-switching support:** NONE DOCUMENTED
   - No model evaluated on Tamil-English code-switched speech
   - Multilingual models may handle code-switching implicitly, but no published metrics
   - Recommend empirical testing on local Tamil-English audio corpus

4. **License considerations for deployment:**
   - Apache 2.0: vasista22 models, Qwen3, MMS-1b-all OK for commercial use
   - CC-BY-NC-4.0: SeamlessM4T, MMS (non-commercial only)
   - MIT: Vakyansh, Whisper (openai variants)

---

## Data Collection Methodology

**Search tools used:**
- Hugging Face API: `https://huggingface.co/api/models?search=<query>&filter=automatic-speech-recognition`
- Direct model card fetches via: `https://huggingface.co/<repo>/raw/main/README.md`
- Metadata from HF API JSON responses (downloads, lastModified, tags, languages)

**Scope limitations:**
- Search limited to models published on Hugging Face Hub (public or gated)
- Code-switching research limited to model card documentation (NOT comprehensive academic literature search)
- Some gated models could not be accessed; their specs marked NOT COVERED
- Model parameter counts estimated from published repo metadata; some unavailable in README

**Date:** 2026-09-24

---



---

## S2 raw file: `research_practitioner.md` (494 lines, verbatim)

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



---

## S3 raw file: `research_llm.md` (568 lines, verbatim)

# Small LLM Research: Tamil/Tanglish ASR + Formatting on RTX 3050 (6GB VRAM)

**Research Date:** 2026-09-24  
**Target:** Instruction LLMs (1-8B, quantized ~3-4 GB VRAM) + single audio model candidates for Tamil/Tanglish dictation + formatting  
**Constraint:** RTX 3050 laptop GPU, 6 GB VRAM; ASR ~1-3 GB, text model ~3-4 GB

---

## Section 1: Small Instruction LLMs (1-8B) with Tamil/Indic Support

### 1.1 Sarvam-1

**HuggingFace URL:** https://huggingface.co/sarvamai/sarvam-1  
**API Metadata:** https://huggingface.co/api/models/sarvamai/sarvam-1

| Field | Value |
|-------|-------|
| **Model ID** | sarvamai/sarvam-1 |
| **Parameters** | 2 billion |
| **Architecture** | Llama (LlamaForCausalLM) |
| **Languages Supported** | bn, en, gu, hi, kn, ml, mr, or, pa, **ta** (Tamil), te |
| **Release Date** | 2024-10-23 |
| **Downloads** | 9,209 |
| **License** | Sarvam non-commercial license |
| **Library** | transformers, safetensors |
| **Instruction Capability** | Text-generation model, non-chat by default (requires fine-tuning for chat) |
| **Tamil Benchmark** | NOT COVERED |
| **GGUF Availability** | Quantized versions: mradermacher/sarvam-1-i1-GGUF exists (https://huggingface.co/mradermacher/sarvam-1-i1-GGUF) |
| **GGUF Quantization Types** | Multiple .gguf files listed, sizes NOT COVERED in accessible repos |
| **Notes** | Trained on ~4 trillion tokens (2T high-quality Indic); 4-6x faster inference than larger models; fertility rates 1.4-2.1 across supported languages (2-4x more efficient than existing multilingual models) |

**Source:** Model card README at https://huggingface.co/sarvamai/sarvam-1/raw/main/README.md quotes: "Sarvam-1 is a 2-billion parameter language model specifically optimized for Indian languages...achieves fertility rates of 1.4-2.1 across all supported languages, 2-4x more efficient than existing multilingual models."

---

### 1.2 Sarvam-M (Mistral-Small-based)

**HuggingFace URL:** https://huggingface.co/sarvamai/sarvam-m  
**API Metadata:** https://huggingface.co/api/models/sarvamai/sarvam-m

| Field | Value |
|-------|-------|
| **Model ID** | sarvamai/sarvam-m |
| **Parameters** | ~24 billion (Mistral-Small-3.1-24B-Base-2503 base) |
| **Architecture** | Mistral |
| **Languages Supported** | en, bn, hi, kn, gu, mr, ml, or, pa, **ta** (Tamil), te |
| **Release Date** | 2025-05-20 |
| **Downloads** | 2,751 |
| **License** | Apache 2.0 |
| **Base Model** | mistralai/Mistral-Small-3.1-24B-Base-2503 (fine-tuned) |
| **GGUF Availability** | bartowski/sarvamai_sarvam-m-GGUF (https://huggingface.co/bartowski/sarvamai_sarvam-m-GGUF) |
| **Quantized Size** | NOT COVERED |
| **Notes** | Too large for 3-4 GB VRAM constraint; listed for completeness. Text-generation-inference compatible. |

**Source:** HF API query for "sarvam" models, dated 2025-05-20 (https://huggingface.co/api/models?search=sarvam&sort=downloads&limit=20)

---

### 1.3 Qwen3-4B-Tamil-16bit-Instruct

**HuggingFace URL:** https://huggingface.co/sabaridsnfuji/Qwen3-4B-tamil-16bit-Instruct  
**API Metadata:** https://huggingface.co/api/models/sabaridsnfuji/Qwen3-4B-tamil-16bit-Instruct

| Field | Value |
|-------|-------|
| **Model ID** | sabaridsnfuji/Qwen3-4B-tamil-16bit-Instruct |
| **Parameters** | 4 billion |
| **Architecture** | Qwen3 (Qwen3ForCausalLM) |
| **Languages Supported** | en, **ta** (Tamil explicitly mentioned in model name) |
| **Release Date** | 2025-11-02 |
| **Downloads** | 16 |
| **License** | Apache 2.0 |
| **Instruction Capability** | Instruction-tuning (Instruct suffix) |
| **GGUF Availability** | mradermacher/Qwen3-4B-tamil-16bit-Instruct-i1-GGUF (https://huggingface.co/mradermacher/Qwen3-4B-tamil-16bit-Instruct-i1-GGUF) |
| **GGUF Downloads** | 863 |
| **GGUF File Sizes** | NOT COVERED |
| **Notes** | Recent (Nov 2025), fine-tuned for Tamil; limited download count suggests small community. Instruction-tuned for chat/formatting tasks. |

**Source:** HF API query result, metadata extracted from sabaridsnfuji/Qwen3-4B-tamil-16bit-Instruct JSON

---

### 1.4 Navarasa Indic-Gemma-2B (Telugu-LLM-Labs)

**HuggingFace URL:** https://huggingface.co/Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa  
**API Metadata:** https://huggingface.co/api/models?search=Navarasa+indic

| Field | Value |
|-------|-------|
| **Model ID** | Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa |
| **Parameters** | 2 billion (Gemma-2B base) |
| **Architecture** | Gemma |
| **Languages Supported** | te, en, **ta** (Tamil), ml, hi, kn, gu, bn, pa, or |
| **Release Date** | 2024-03-04 |
| **Downloads** | 0 (research model) |
| **License** | Other (non-commercial likely) |
| **Instruction Capability** | Supervised fine-tuning (SFT) on Indic datasets including Tamil Alpaca |
| **Training Datasets** | Tamil Alpaca dataset (abhinand/tamil-alpaca), Samvaad (Hindi), Telugu data, Malayalam Alpaca, Gujarati Alpaca, Punjabi Alpaca, Bengali Alpaca, Odia Alpaca |
| **Quantized Sizes** | NOT COVERED |
| **GGUF Availability** | NOT COVERED |
| **Notes** | Purpose-built for Indic languages; 2B size fits VRAM; training data explicitly includes Tamil; no commercial license clear. |

**Source:** HF API query for "Navarasa+indic", model card tags show training datasets

---

### 1.5 Krutrim-2-Instruct

**HuggingFace URL:** https://huggingface.co/krutrim-ai-labs/Krutrim-2-instruct  
**API Metadata:** https://huggingface.co/api/models?search=Krutrim

| Field | Value |
|-------|-------|
| **Model ID** | krutrim-ai-labs/Krutrim-2-instruct |
| **Parameters** | NOT COVERED in metadata |
| **Architecture** | Mistral |
| **Languages Supported** | en, hi, bn, mr, te, **ta** (Tamil), kn, ml, gu, as, pa, sa, ur |
| **Release Date** | 2025-02-02 |
| **Downloads** | 439 |
| **License** | Other (proprietary, non-commercial likely) |
| **Instruction Capability** | Instruct-tuned |
| **Quantized Sizes** | NOT COVERED |
| **GGUF Availability** | NOT COVERED |
| **Notes** | Indian company (Krutrim AI Labs); broad Indic language support including Tamil; recent (Feb 2025). Parameter count not stated; likely larger than 4B based on architecture hints. |

**Source:** HF API query for Krutrim models, 2025-02-02 metadata

---

### 1.6 Tamil-Mistral-7B-Instruct-v0.1

**HuggingFace URL:** https://huggingface.co/Hemanth-thunder/Tamil-Mistral-7B-Instruct-v0.1  
**GGUF URL:** https://huggingface.co/mradermacher/Tamil-Mistral-7B-Instruct-v0.1-i1-GGUF

| Field | Value |
|-------|-------|
| **Model ID** | Hemanth-thunder/Tamil-Mistral-7B-Instruct-v0.1 |
| **Parameters** | 7 billion |
| **Architecture** | Mistral |
| **Languages Supported** | **Tamil (ta)** + English (likely) |
| **Release Date** | 2024 (exact date NOT COVERED) |
| **License** | Apache 2.0 |
| **Instruction Capability** | Instruct-tuned (Instruction Tuning suffix) |
| **Training Data** | Tamil Open Instruct v1 (Hemanth-thunder/tamil-open-instruct-v1 dataset); DPO, RLHF, synthetic data distillation, function calling, JSON mode |
| **GGUF Quantization Available** | mradermacher/Tamil-Mistral-7B-Instruct-v0.1-i1-GGUF |
| **GGUF Downloads** | 793 |
| **GGUF File Sizes** | NOT COVERED (repo tree query returned no output) |
| **Quantization Methods** | imatrix quantization claimed |
| **Notes** | 7B exceeds 3-4 GB VRAM budget in FP32; quantization required. Function-calling and JSON mode support useful for formatting. |

**Source:** HF API query, mradermacher GGUF repository

---

### 1.7 Gemma-3-4B-IT (Google)

**HuggingFace URL:** https://huggingface.co/google/gemma-3-4b-it  
**Note:** Access restricted; metadata from HF API query only.

| Field | Value |
|-------|-------|
| **Model ID** | google/gemma-3-4b-it |
| **Parameters** | 4 billion |
| **Architecture** | Gemma-3 |
| **Languages Supported** | English (model card access restricted; likely English-only based on Gemma line) |
| **Release Date** | 2025-02-20 |
| **Downloads** | 1,682,829 |
| **License** | Gemma |
| **Pipeline Tag** | image-text-to-text (multimodal) |
| **Library** | transformers, safetensors |
| **Instruction Capability** | Instruction-tuned (IT suffix) |
| **GGUF Availability** | NOT COVERED |
| **Tamil Support** | NOT COVERED (model card access restricted) |
| **Notes** | Multimodal (image + text input); high download count; language support NOT COVERED due to access restriction. English-only likely, no Tamil evidence. |

**Source:** HF API query for "gemma+3" models, 2025-02-20 metadata. Model card README requires authentication.

---

### 1.8 Phi-4 (Microsoft)

**HuggingFace URL:** https://huggingface.co/microsoft/phi-4  
**API Metadata:** https://huggingface.co/api/models/microsoft/phi-4

| Field | Value |
|-------|-------|
| **Model ID** | microsoft/phi-4 |
| **Parameters** | ~14 billion (estimated; exact param count NOT COVERED) |
| **Architecture** | Phi-3 |
| **Languages Supported** | English only (en tag) |
| **Release Date** | 2025-12-08 (last modified) |
| **Downloads** | 621,463 |
| **License** | MIT |
| **Library** | transformers, safetensors |
| **Instruction Capability** | Chat/conversational instruction-tuned |
| **GGUF Availability** | NOT COVERED |
| **Tamil Support** | No Tamil support claimed |
| **Notes** | English-only; too large (~14B) for 3-4 GB VRAM without aggressive quantization; MIT license permissive. |

**Source:** HF API query, microsoft/phi-4 JSON metadata

---

## Section 2: Single-Model Audio Input LLMs (ASR + Formatting in One Pass)

### 2.1 Qwen2.5-Omni-3B (Audio + Text Input, Streaming Audio Output)

**HuggingFace URL:** https://huggingface.co/Qwen/Qwen2.5-Omni-3B  
**API Metadata:** https://huggingface.co/api/models/Qwen/Qwen2.5-Omni-3B

| Field | Value |
|-------|-------|
| **Model ID** | Qwen/Qwen2.5-Omni-3B |
| **Parameters** | 3 billion |
| **Architecture** | Qwen2.5-Omni (Thinker-Talker, end-to-end multimodal) |
| **Input Modalities** | Text, images, audio, video |
| **Output Modalities** | Text, natural speech (streaming) |
| **Audio Languages Supported** | NOT COVERED in README excerpt (languages not listed for audio specifically) |
| **Tamil ASR Support** | NOT COVERED |
| **Release Date** | 2025-04-30 (HF upload date) |
| **Downloads** | 329,421 |
| **License** | Qwen Research License (proprietary) |
| **Library** | transformers, safetensors |
| **GGUF Availability** | unsloth/Qwen2.5-Omni-7B-GGUF (7B version exists; 3B GGUF NOT COVERED) |
| **Streaming Support** | Yes; explicitly designed for real-time interactions |
| **Quantized Sizes** | NOT COVERED |
| **Benchmarks** | OmniBench (speech, sound events, music); Common Voice; CoVoST2 (translation); MMAU (audio understanding); Seed-tts-eval (speech generation) |
| **Notes** | Novel Thinker-Talker architecture; end-to-end any-to-any; streaming speech output (not just text). Audio input language support NOT COVERED in accessible documentation. |

**Source:** HF model card README at https://huggingface.co/Qwen/Qwen2.5-Omni-3B/raw/main/README.md

---

### 2.2 Qwen2.5-Omni-7B (Larger Audio Model)

**HuggingFace URL:** https://huggingface.co/Qwen/Qwen2.5-Omni-7B  

| Field | Value |
|-------|-------|
| **Model ID** | Qwen/Qwen2.5-Omni-7B |
| **Parameters** | 7 billion |
| **Architecture** | Qwen2.5-Omni (same as 3B variant) |
| **Input Modalities** | Text, images, audio, video |
| **Output Modalities** | Text, natural speech (streaming) |
| **Audio Languages Supported** | NOT COVERED |
| **Tamil ASR Support** | NOT COVERED |
| **Release Date** | 2025-03-22 |
| **Downloads** | 332,236 |
| **License** | Qwen Research License |
| **GGUF Availability** | unsloth/Qwen2.5-Omni-7B-GGUF (https://huggingface.co/unsloth/Qwen2.5-Omni-7B-GGUF) |
| **GGUF Downloads** | 18,967 |
| **Streaming Support** | Yes |
| **VRAM Footprint** | 7B likely exceeds 3-4 GB in FP32; quantization required |
| **Notes** | 7B version more capable than 3B but larger VRAM burden; GGUF available; language support for audio NOT COVERED. |

**Source:** HF API query for Qwen Omni models

---

### 2.3 Qwen3-Omni-30B-A3B-Instruct (Large Audio Model)

**HuggingFace URL:** https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct  

| Field | Value |
|-------|-------|
| **Model ID** | Qwen/Qwen3-Omni-30B-A3B-Instruct |
| **Parameters** | 30 billion (MOE with adaptive sparse) |
| **Architecture** | Qwen3-Omni MOE |
| **Input Modalities** | Text, images, audio, video |
| **Output Modalities** | Text, audio |
| **Audio Languages** | NOT COVERED |
| **Tamil Support** | NOT COVERED |
| **Release Date** | 2025-09-20 |
| **Downloads** | 638,761 |
| **License** | Qwen Research License |
| **GGUF Availability** | TrevorJS/Qwen3-Omni-30B-A3B-GGUF exists (https://huggingface.co/TrevorJS/Qwen3-Omni-30B-A3B-GGUF), downloads 470 |
| **Trending Score** | 6 (high) |
| **VRAM Footprint** | Likely 12-20+ GB full precision; beyond 6GB constraint even quantized |
| **Notes** | Cutting-edge (Sep 2025); MOE enables dynamic inference cost; too large for this project's VRAM budget. Audio language support NOT COVERED. |

**Source:** HF API query, https://huggingface.co/api/models?search=qwen+omni

---

### 2.4 Voxtral-Mini-4B-Realtime-2602 (Mistral Speech ASR)

**HuggingFace URL:** https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602  
**API Metadata:** https://huggingface.co/api/models/mistralai/Voxtral-Mini-4B-Realtime-2602

| Field | Value |
|-------|-------|
| **Model ID** | mistralai/Voxtral-Mini-4B-Realtime-2602 |
| **Parameters** | 4 billion (based on Mini-4B naming) |
| **Base Model** | mistralai/Ministral-3-3B-Base-2512 (fine-tuned) |
| **Architecture** | VoxtralRealtimeForConditionalGeneration |
| **Pipeline Task** | automatic-speech-recognition (ASR) |
| **Input Languages (Audio)** | en, fr, es, de, ru, zh, ja, it, pt, nl, ar, hi, ko |
| **Tamil ASR Support** | No Tamil in language list |
| **Output** | Text (ASR transcription) |
| **Release Date** | 2026-01-21 |
| **Downloads** | 1,736,439 |
| **License** | Apache 2.0 |
| **Streaming Support** | Realtime (model name suffix) |
| **GGUF Availability** | NOT COVERED |
| **Real-time Capability** | Designed for "fully real-time interactions, supporting chunked input and immediate output" |
| **Notes** | **NO Tamil support** (Hindi is supported, not Tamil). ASR-only (no formatting); text model would be needed separately. Mistral's latest speech model. |

**Source:** HF API metadata, https://huggingface.co/api/models/mistralai/Voxtral-Mini-4B-Realtime-2602; quote from release notes.

---

### 2.5 Voxtral-Mini-3B-2507 (Older Voxtral ASR)

**HuggingFace URL:** https://huggingface.co/mistralai/Voxtral-Mini-3B-2507  
**API Metadata:** https://huggingface.co/api/models/mistralai/Voxtral-Mini-3B-2507

| Field | Value |
|-------|-------|
| **Model ID** | mistralai/Voxtral-Mini-3B-2507 |
| **Parameters** | 3 billion |
| **Architecture** | VoxtralForConditionalGeneration |
| **Pipeline Task** | audio-text-to-text |
| **Input Languages** | en, fr, de, es, it, pt, nl, hi |
| **Tamil ASR Support** | No Tamil in language list |
| **Release Date** | 2025-07-01 |
| **Downloads** | 289,250 |
| **License** | Apache 2.0 |
| **GGUF Availability** | bartowski/mistralai_Voxtral-Mini-3B-2507-GGUF (https://huggingface.co/bartowski/mistralai_Voxtral-Mini-3B-2507-GGUF), downloads 4,288 |
| **GGUF File Sizes** | NOT COVERED |
| **Streaming Support** | NOT COVERED |
| **Notes** | Older model (Jul 2025); same language limitation: **NO Tamil**. Smaller (3B) than Realtime variant. |

**Source:** HF API query, https://huggingface.co/api/models?search=voxtral+mistral

---

### 2.6 Sarvam Shuka-1 (Audio + Text, Limited Languages)

**HuggingFace URL:** https://huggingface.co/sarvamai/shuka-1  
**API Metadata:** https://huggingface.co/api/models?search=sarvam+shuka

| Field | Value |
|-------|-------|
| **Model ID** | sarvamai/shuka-1 |
| **Parameters** | NOT COVERED |
| **Architecture** | Shuka (feature-extraction audio-text-to-text) |
| **Pipeline Task** | audio-text-to-text |
| **Input Languages** | en, hi |
| **Tamil ASR Support** | No Tamil listed |
| **Release Date** | 2024-08-08 |
| **Downloads** | 327 |
| **License** | Llama3 |
| **Notes** | **NO Tamil support** (Hindi present, Tamil absent). Limited language support; low download count; from Sarvam AI. |

**Source:** HF API query for "sarvam+shuka" models

---

### 2.7 IBM Granite Speech 4.1-2B-Plus (Multilingual ASR)

**HuggingFace URL:** https://huggingface.co/ibm-granite/granite-speech-4.1-2b-plus  
**API Metadata:** https://huggingface.co/api/models?search=granite+speech

| Field | Value |
|-------|-------|
| **Model ID** | ibm-granite/granite-speech-4.1-2b-plus |
| **Parameters** | 2 billion |
| **Architecture** | Granite Speech (tuned on Granite-4.0-1b-base) |
| **Pipeline Task** | automatic-speech-recognition |
| **Input Languages** | en, fr, de, es, pt |
| **Tamil ASR Support** | No Tamil listed |
| **Release Date** | 2026-04-16 |
| **Downloads** | 123,799 |
| **License** | Apache 2.0 |
| **Streaming Support** | NOT COVERED |
| **GGUF Availability** | NOT COVERED |
| **Notes** | **NO Tamil support**. European languages focus (en, fr, de, es, pt). Small 2B model fits VRAM, but ASR-only; no formatting capability. |

**Source:** HF API query for "granite+speech" models

---

## Section 3: Ollama & llama.cpp CUDA/Windows Constraints

### 3.1 llama.cpp CUDA Support (GitHub)

**Repository:** https://github.com/ggerganov/llama.cpp  
**Raw README:** https://raw.githubusercontent.com/ggerganov/llama.cpp/master/README.md (404 Not Found)

| Feature | Status/Details |
|---------|---|
| **CUDA Support** | Native custom CUDA kernels for NVIDIA GPUs |
| **Quantization Support** | 1.5-bit, 2-bit, 3-bit, 4-bit, 5-bit, 6-bit, 8-bit integer quantization |
| **Memory Reduction** | Quantization reduces memory footprint for "faster inference and reduced memory use" |
| **CPU+GPU Hybrid** | "CPU+GPU hybrid inference to partially accelerate models larger than total VRAM capacity" |
| **Layer Offloading** | Supported; allows models to overflow to CPU RAM when VRAM is exceeded |
| **VRAM Constraint Workaround** | Hybrid processing enables layer-by-layer offloading |
| **Installation** | https://llama.app; pre-built binaries; Docker; build from source |
| **API Server** | OpenAI-compatible API server available |
| **Documentation** | Covers building, Docker, multi-GPU, performance optimization |
| **Windows Support** | NOT COVERED in accessible documentation |

**Source:** WebFetch from https://github.com/ggerganov/llama.cpp, quoted: "Custom CUDA kernels...CPU+GPU hybrid inference to partially accelerate models larger than the total VRAM capacity."

---

### 3.2 Ollama Documentation (URL Redirect Chain)

**Primary URL:** https://ollama.ai/docs → 301 redirect  
**Intermediate URL:** https://ollama.com/docs → 303 redirect  
**Final URL:** https://docs.ollama.com/ (landing page; technical specs NOT COVERED)

| Feature | Status/Details |
|---------|---|
| **GPU Support** | NVIDIA CUDA (implied; NOT COVERED in accessible docs) |
| **VRAM Management** | NOT COVERED |
| **Layer Offloading** | NOT COVERED |
| **Context Size Limits** | NOT COVERED |
| **Windows Support** | NOT COVERED |
| **Quantization** | NOT COVERED |
| **Documentation Index** | Exists but detailed specs require deeper navigation |

**Notes:** Ollama documentation landing page does not surface VRAM, context, or offloading details in index view. Full documentation exists but requires specific navigation to find technical constraints.

**Source:** WebFetch attempted at https://docs.ollama.com/ (landing page only); detailed specs NOT accessible via homepage.

---

## Section 4: Tamil ASR Models (for Baseline Reference)

**Note:** These are ASR-only, not instruction LLMs or audio-in LLMs, but listed for completeness.

### 4.1 Whisper-Tamil-Small (Vasista22)

**HuggingFace URL:** https://huggingface.co/vasista22/whisper-tamil-small  
**API Metadata:** https://huggingface.co/api/models?search=tamil

| Field | Value |
|-------|-------|
| **Model ID** | vasista22/whisper-tamil-small |
| **Parameters** | Small (relative to Whisper base/medium) |
| **Architecture** | Whisper (OpenAI) |
| **Pipeline** | automatic-speech-recognition |
| **Language** | Tamil (ta) |
| **Release Date** | 2023-01-01 |
| **Downloads** | 151,305 |
| **License** | Apache 2.0 |
| **Use Case** | ASR baseline for Tamil speech recognition |

**Source:** HF API search for "tamil" models

---

### 4.2 Vakyansh-Wav2Vec2-Tamil (Harveenchadha)

**HuggingFace URL:** https://huggingface.co/Harveenchadha/vakyansh-wav2vec2-tamil-tam-250  

| Field | Value |
|-------|-------|
| **Model ID** | Harveenchadha/vakyansh-wav2vec2-tamil-tam-250 |
| **Architecture** | Wav2Vec2 |
| **Pipeline** | automatic-speech-recognition |
| **Language** | Tamil (ta) |
| **Release Date** | 2022-03-02 |
| **Downloads** | 1,370,172 (highest for Tamil ASR) |
| **License** | MIT |
| **WER Benchmark** | NOT COVERED |

**Source:** HF API search result; highest-download Tamil ASR model

---

### 4.3 AI4Bharat Indic-Conformer-600M (Multilingual ASR)

**HuggingFace URL:** https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual  

| Field | Value |
|-------|-------|
| **Model ID** | ai4bharat/indic-conformer-600m-multilingual |
| **Parameters** | 600 million |
| **Architecture** | Conformer (ONNX format) |
| **Pipeline** | automatic-speech-recognition |
| **Languages** | Multilingual Indic languages (Tamil likely included; exact list NOT COVERED) |
| **Release Date** | 2025-03-15 |
| **Downloads** | 522,592 |
| **License** | MIT |
| **Streaming Support** | NOT COVERED |
| **VRAM Footprint** | 600M likely < 1 GB; suitable for low-VRAM setups |

**Source:** HF API query for AI4Bharat models

---

## Section 5: Tamil Text-to-Speech (Not Primary, But Noted)

### 5.1 AI4Bharat IndicF5 (Multilingual TTS)

**HuggingFace URL:** https://huggingface.co/ai4bharat/IndicF5  

| Field | Value |
|-------|-------|
| **Model ID** | ai4bharat/IndicF5 |
| **Architecture** | Inf5 (proprietary) |
| **Pipeline** | text-to-speech |
| **Languages** | as, bn, gu, mr, hi, kn, ml, or, pa, **ta** (Tamil), te |
| **Use Case** | Output formatting (after ASR + text generation, can speak back formatted document) |
| **Release Date** | 2025-03-11 |
| **Downloads** | 31,246 |
| **License** | MIT |

**Source:** HF API query for "AI4Bharat" models

---

## Section 6: Summary Table — Candidates Ranked by Suitability

| Model | Params | Architecture | Tamil Support | Type | Quantized Size | Fit (3-4GB) | Notes |
|-------|--------|--------------|---|---|---|---|
| **Sarvam-1** | 2B | Llama | **YES (ta)** | Instruction LLM | ~600MB-1.2GB (Q4) | **YES** | Best for Tamil instruction following; fits easily in 3-4GB |
| **Qwen3-4B-Tamil** | 4B | Qwen3 | **YES (ta)** | Instruction LLM | ~1.5-2.5GB (Q4) | **YES (tight)** | Tamil-specific fine-tune; instruction-capable |
| **Navarasa Indic-Gemma-2B** | 2B | Gemma | **YES (ta)** | Instruction LLM (SFT) | ~600MB-1.2GB (Q4) | **YES** | Research model; Indic training data; no commercial license clear |
| **Krutrim-2-Instruct** | Unknown | Mistral | **YES (ta)** | Instruction LLM | Unknown | TBD | Proprietary license; parameter count not disclosed |
| **Tamil-Mistral-7B-Instruct** | 7B | Mistral | **YES (ta)** | Instruction LLM | ~2-3GB (Q4-Q5) | **Marginal** | Fits in 3-4GB with Q4-Q5; function-calling + JSON mode |
| **Gemma-3-4B-IT** | 4B | Gemma | TBD (restricted) | Instruction LLM | Unknown | TBD | Access restricted; likely English-only; multimodal |
| **Qwen2.5-Omni-3B** | 3B | Omni (Thinker-Talker) | **NOT COVERED** | Audio input + text output | Unknown | TBD | Single model ASR+formatting; Tamil support NOT documented |
| **Voxtral-Mini-4B** | 4B | Voxtral | **NO Tamil** | ASR only | Unknown | TBD | Real-time ASR; no Tamil; separate text model needed |
| **Voxtral-Mini-3B** | 3B | Voxtral | **NO Tamil** | ASR only | ~1.5-2GB (GGUF Q4) | **YES** | No Tamil; GGUF available; ASR-only |
| **Sarvam Shuka-1** | Unknown | Shuka | **NO Tamil** | Audio-text | Unknown | TBD | Hindi only; no Tamil support |
| **Granite Speech 4.1-2B-Plus** | 2B | Granite | **NO Tamil** | ASR only | Unknown | TBD | European languages; no Tamil |

---

## Section 7: Not Found / Candidates Without Sufficient Data

| Model Name | Search Strategy | Result |
|------------|---|---|
| **Phi-4-Mini** | HF search "phi+small", explicit search for Phi-4 multimodal | NOT FOUND (Phi-4 is ~14B base model only; no "mini" variant found) |
| **Sarvam-Translate** | HF API query "sarvam" | FOUND: sarvamai/sarvam-translate (4B Gemma-3-4b-it base), but translation model (not instruction/formatting LLM) |
| **Llama-3.2-3B Tamil** | HF search "Llama+3.2+small", "tamil" | NOT FOUND (Llama-3.2-3B exists but no Tamil-specific variant in top results) |
| **Granite Speech 8B** | HF search "granite+speech" | FOUND but >2B; exceeds typical 3-4GB budget without aggressive quantization |
| **Ollama GPU layer offload exact constraints** | WebFetch docs.ollama.com | DOCS LANDING PAGE ONLY; technical specs NOT COVERED in accessible pages |
| **llama.cpp Windows CUDA setup guide** | WebFetch raw GitHub URL | 404 Not Found; README not on main branch |

---

## Appendix: Research Gaps (Explicitly Marked NOT COVERED)

1. **Tamil/Indic benchmarks for small models**: No published WER, BLEU, or instruction-following accuracy for Sarvam-1, Qwen3-4B-Tamil, or Navarasa on Tamil tasks. Quote from source: "NOT COVERED."

2. **Exact GGUF quantization file sizes**: HF API repo tree queries returned empty output or truncated results. GGUF repositories exist (e.g., mradermacher/sarvam-1-i1-GGUF) but file sizes not accessible via curl.

3. **Ollama/llama.cpp CUDA + Windows specifics**: Docs landing page does not expose VRAM offload mechanics, context-size limits, or Windows driver/DLL requirements. Deeper docs pages likely exist but require navigation.

4. **Single-model audio-in LLM Tamil support**: Qwen2.5-Omni README does not list audio input languages. Inference against Tamil speech NOT TESTED; only documented for English.

5. **Function-calling and JSON-mode support**: Not confirmed for Sarvam-1, Navarasa, or Krutrim models; inferred from model architecture but NOT EXPLICITLY STATED in accessible model cards.

6. **Streaming output support**: Ollama integration with small quantized models for streaming text/audio output NOT COVERED in accessible documentation.

---

## File Metadata

**Research Date:** 2026-09-24  
**Sources:** HuggingFace Hub (API + model cards), GitHub (llama.cpp), Ollama docs landing page  
**Verbatim Quotes:** All factual claims backed by URL + direct extraction from model metadata JSON or README files.  
**Gaps:** Marked "NOT COVERED" where sources do not state information.



---

## S4 raw file: `research_youtube.md` (verbatim)

﻿# YouTube Research: Tamil and Tanglish Speech-to-Text (2024-2026)

**Research Date:** 2026-09-24
**Search Tool:** yt-dlp (C:\Users\DJ\.local\bin\yt-dlp.exe)
**Scope:** Colloquial Tamil, Tanglish code-switched, local GPU models
**Total Unique Videos:** 54
**Videos Analyzed:** 14
**Transcripts Retrieved:** 5

---

## Search Results

| Query | Results |
|-------|---------|
| whisper tamil speech to text | 10 |
| tamil speech recognition ai | 10 |
| tanglish transcription demo | 10 |
| IndicConformer tamil demo | 6 |
| IndicWhisper tamil speech | 3 |
| faster-whisper tamil | 10 |
| sarvam ai tamil voice | 10 |
| AI4Bharat tamil voice recognition | 10 |

**Total: 54 unique videos across 8 search queries**

---

## Models Identified

| Model | Videos | Status |
|-------|--------|--------|
| OpenAI Whisper / faster-whisper | 10+ | Local GPU capable |
| AI4Bharat IndicConformer | 7+ | Multi-language, Tamil included |
| Sarvam AI | 8+ | Sovereign Indian AI, 2026 active |
| IndicWav2Vec | 3+ | AI4Bharat ASR model |
| Indic Parler-TTS | 2+ | Local TTS installation |
| Custom Python/LiveKit stacks | 3+ | Voice assistants |

---

## Videos Analyzed (14 total)

### 1. How to Install Whisper AI - Complete Tutorial | Tamil Audio to Text | Ep. 12 #RTR #ai #transcription

- **URL:** https://www.youtube.com/watch?v=PKHA92gusTM
- **Channel:** RTR Unfiltered
- **Date:** 20250418
- **Views:** 1281
- **Duration:** 1020s

### 2. Convert speech to text in realtime without delay | using faster-whisper module

- **URL:** https://www.youtube.com/watch?v=uimBp3c3Koo
- **Channel:** KARTIS
- **Date:** 20250429
- **Views:** 31236
- **Duration:** 456s

### 3. Speech-to-Text Model Demo - AI4Bharat

- **URL:** https://www.youtube.com/watch?v=xgBKvpiiYrI
- **Channel:** AI4Bharat
- **Date:** 20221217
- **Views:** 2931
- **Duration:** 99s

### 4. Sarvam AI | Real Time Voice Agent Exploring Video Tamil

- **URL:** https://www.youtube.com/watch?v=6od8EtAXm3M
- **Channel:** AI with Thiru
- **Date:** 20260309
- **Views:** 5915
- **Duration:** 533s

### 5. Indic Parler-TTS - Install Locally - Test with Hindi, Urdu, Tamil and Other Languages

- **URL:** https://www.youtube.com/watch?v=X1GK4iSNQJU
- **Channel:** Fahd Mirza
- **Date:** 20241204
- **Views:** 8329
- **Duration:** 790s

### 6. 37 Indian Language Speech to Text Pipeline | AI4Bharat IndicConformer ASR with JSON  SRT

- **URL:** https://www.youtube.com/watch?v=70Nrt_FpHz4
- **Channel:** Sudheendra S G
- **Date:** 20260524
- **Views:** 431
- **Duration:** 1596s

### 7. 38 AI4Bharat Indic Conformer Tutorial

- **URL:** https://www.youtube.com/watch?v=7yWXkWvqSrA
- **Channel:** Sudheendra S G
- **Date:** 20260524
- **Views:** 377
- **Duration:** 448s

### 8. Build an AI Voice Assistant with Python | Listen, Think & Speak | Tamil | Karthik's Show

- **URL:** https://www.youtube.com/watch?v=V3tmtEM_uhk
- **Channel:** Karthik's Show
- **Date:** 20260724
- **Views:** 2547
- **Duration:** 1332s

### 9. Automatic  Speech  Recognition in Tamil | Thenkachi ko swaminathan inspired recreation.

- **URL:** https://www.youtube.com/watch?v=hoA-xO3Zzio
- **Channel:** Tech Thuli
- **Date:** 20260310
- **Views:** 92
- **Duration:** 340s

### 10. Automatic Speech Recognition system for Indian Languages “IndicWav2Vec”

- **URL:** https://www.youtube.com/watch?v=cmy2zf6CuH4
- **Channel:** AI4Bharat
- **Date:** 20220822
- **Views:** 5345
- **Duration:** 925s

### 11. How to Build Your Own JARVIS AI Agent 100% Free! | LiveKit Tutorial #tamil

- **URL:** https://www.youtube.com/watch?v=xHvWsePTs3I
- **Channel:** Echo Mind
- **Date:** 20250817
- **Views:** 11340
- **Duration:** 794s

### 12. AI in Tamil 🚀 Sarvam AI | Language No Bar | Photoshop + DaVinci Resolve Edit 🔥 மொழி ஒரு தடையல்ல

- **URL:** https://www.youtube.com/watch?v=3eE4ZdnPNZU
- **Channel:** Salavadi Eswaran
- **Date:** 20260221
- **Views:** 17517
- **Duration:** 920s

### 13. Sarvam AI Text to Speech in Action | Best AI Tamil Voice Generator (AI Tamil)

- **URL:** https://www.youtube.com/watch?v=y38bxfAX6Rg
- **Channel:** Tutusfunny tamil
- **Date:** 20260706
- **Views:** 195
- **Duration:** 531s

### 14. This AI Voice Generator Speaks 11 Indian Languages (@SarvamAI  )

- **URL:** https://www.youtube.com/watch?v=lnCTn6q6thE
- **Channel:** Media Meets AI
- **Date:** 20260727
- **Views:** 50
- **Duration:** 65s

---

## Transcripts Retrieved

Successfully downloaded 5 subtitle files:

- 70Nrt_FpHz4.en.vtt (198.6KB)
- 7yWXkWvqSrA.en.vtt (48.9KB)
- uimBp3c3Koo.en.vtt (73.9KB)
- V3tmtEM_uhk.en.vtt (37.9KB)
- xgBKvpiiYrI.en.vtt (6.4KB)

---

## All Video IDs (54 total)

04BSgrzOBVk, 3eE4ZdnPNZU, 4t_coQGUbOo, 56_lZDOwSKo, 6altVgTOf9s

6od8EtAXm3M, 6VheRwdQQ78, 70Nrt_FpHz4, 7yWXkWvqSrA, 86GzmsPcUgw

ABFqbY_rmEk, anplUNnkM68, BMe9QFU2GSY, bOW8tV15rBs, CCkoqOKKjcA

cfWG0KmNzso, cmy2zf6CuH4, D0p2zIGOskM, dg_TWk8Zfjk, ezdIOLbUSWg

f7md4IS4qXQ, FGeYswHAn5g, fyifKHq8XaY, GEpqRST7Oj0, GmRG59OD26U

HbY51mVKrcE, hoA-xO3Zzio, I1o8QO7PU2U, I3TCBVBdqLo, JsSFHsO65uY

KFuSJiqEm4E, lnCTn6q6thE, lpSahBCcgqc, mALoIKrK_ms, MRz4et4Sd0c

-nCWBM4aE64, orTVWvbMk6s, PKHA92gusTM, R5bfClvmmqc, Ra3brxxNX4s

SiEXBVudlJw, Tj8qOxZT06M, tQtlHZNlYxw, Tw7hLBMA1Pk, U9Cs9gwNZOY

uimBp3c3Koo, uLFfTNPTM9I, Upl7q8GP-xA, V3tmtEM_uhk, X1GK4iSNQJU

xgBKvpiiYrI, xHvWsePTs3I, xJTFY5t9nQA, y38bxfAX6Rg

---

## Search Tools Evaluation

| Tool | Status | Effectiveness |
|------|--------|----------------|
| yt-dlp | WORKING | Highly effective - 54 videos found, transcripts retrieved |
| agent-reach | NOT FOUND | Would have provided forum/Reddit context |
| WebSearch/WebFetch | Available | Not needed - yt-dlp sufficient |
| Tamil queries | NOT TESTED | Would likely yield additional results |

---

## Key Findings

1. **Sarvam AI Surge (2026):** Heavy recent activity in Tamil voice agents and TTS
2. **AI4Bharat Mature:** IndicConformer established with tutorials and demos
3. **Whisper + Optimization:** faster-whisper widely demonstrated for local, real-time use
4. **Limited Tanglish Focus:** Most code-switching appears in voice assistant demos
5. **Local GPU Deployment:** Multiple videos show offline setup options
6. **Active Tamil Tech Community:** Strong 2025-2026 content creation



### S4 fetcher hand-back message (verbatim)

> Videos Logged: 54 unique (14 with full metadata). Count by Model/Service: OpenAI Whisper / faster-whisper: 10+ videos; AI4Bharat IndicConformer: 7+; Sarvam AI: 8+; IndicWav2Vec: 3+; Indic Parler-TTS: 2+; Custom Python/LiveKit stacks: 3+. Transcripts Retrieved: 5 files (VTT format, en + ta). Search tools: yt-dlp WORKING (54 videos found across 8 queries); agent-reach NOT FOUND (not on PATH); WebSearch/WebFetch available but not needed; Tamil-language queries NOT TESTED (English queries sufficient).


### S4 supporting file: `unique_video_ids.txt` (verbatim)

```
﻿04BSgrzOBVk
3eE4ZdnPNZU
4t_coQGUbOo
56_lZDOwSKo
6altVgTOf9s
6od8EtAXm3M
6VheRwdQQ78
70Nrt_FpHz4
7yWXkWvqSrA
86GzmsPcUgw
ABFqbY_rmEk
anplUNnkM68
BMe9QFU2GSY
bOW8tV15rBs
CCkoqOKKjcA
cfWG0KmNzso
cmy2zf6CuH4
D0p2zIGOskM
dg_TWk8Zfjk
ezdIOLbUSWg
f7md4IS4qXQ
FGeYswHAn5g
fyifKHq8XaY
GEpqRST7Oj0
GmRG59OD26U
HbY51mVKrcE
hoA-xO3Zzio
I1o8QO7PU2U
I3TCBVBdqLo
JsSFHsO65uY
KFuSJiqEm4E
lnCTn6q6thE
lpSahBCcgqc
mALoIKrK_ms
MRz4et4Sd0c
-nCWBM4aE64
orTVWvbMk6s
PKHA92gusTM
R5bfClvmmqc
Ra3brxxNX4s
SiEXBVudlJw
Tj8qOxZT06M
tQtlHZNlYxw
Tw7hLBMA1Pk
U9Cs9gwNZOY
uimBp3c3Koo
uLFfTNPTM9I
Upl7q8GP-xA
V3tmtEM_uhk
X1GK4iSNQJU
xgBKvpiiYrI
xHvWsePTs3I
xJTFY5t9nQA
y38bxfAX6Rg

```


### S4 supporting file: `yt_search_AI4Bharat_tamil_voice_recognition.csv` (verbatim)

```
﻿{"id":"xgBKvpiiYrI","title":"Speech-to-Text Model Demo - AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":2931,"duration":99}
{"id":"cmy2zf6CuH4","title":"Automatic Speech Recognition system for Indian Languages “IndicWav2Vec”","channel":"AI4Bharat","upload_date":null,"view_count":5345,"duration":926}
{"id":"JsSFHsO65uY","title":"Kathbath Demo | Speech Collection | AI4Bharat | IIT Madras","channel":"AI4Bharat","upload_date":null,"view_count":1735,"duration":65}
{"id":"6VheRwdQQ78","title":"Speech-to-Text Model Demo - AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":894,"duration":118}
{"id":"SiEXBVudlJw","title":"Text-to-Speech Model Demo AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":2128,"duration":101}
{"id":"KFuSJiqEm4E","title":"Text-to-Speech Model Demo - AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":1327,"duration":87}
{"id":"70Nrt_FpHz4","title":"37 Indian Language Speech to Text Pipeline | AI4Bharat IndicConformer ASR with JSON  SRT","channel":"Sudheendra S G","upload_date":null,"view_count":431,"duration":1597}
{"id":"cfWG0KmNzso","title":"Transliteration Model Demo   AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":822,"duration":73}
{"id":"I3TCBVBdqLo","title":"Transliteration Model Demo AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":810,"duration":74}
{"id":"7yWXkWvqSrA","title":"38 AI4Bharat Indic Conformer Tutorial","channel":"Sudheendra S G","upload_date":null,"view_count":376,"duration":448}

```


### S4 supporting file: `yt_search_IndicConformer_tamil_demo.csv` (verbatim)

```
﻿{"id":"X1GK4iSNQJU","title":"Indic Parler-TTS - Install Locally - Test with Hindi, Urdu, Tamil and Other Languages","channel":"Fahd Mirza","upload_date":null,"view_count":8328,"duration":791}
{"id":"xgBKvpiiYrI","title":"Speech-to-Text Model Demo - AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":2931,"duration":99}
{"id":"cfWG0KmNzso","title":"Transliteration Model Demo   AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":822,"duration":73}
{"id":"tQtlHZNlYxw","title":"Translation Model Demo AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":892,"duration":72}
{"id":"uimBp3c3Koo","title":"Convert speech to text in realtime without delay | using faster-whisper module","channel":"KARTIS","upload_date":null,"view_count":31237,"duration":456}
{"id":"ezdIOLbUSWg","title":"Fine Tuning LLM Explained Simply","channel":"codebasics","upload_date":null,"view_count":64452,"duration":406}

```


### S4 supporting file: `yt_search_IndicWhisper_tamil_speech.csv` (verbatim)

```
﻿{"id":"X1GK4iSNQJU","title":"Indic Parler-TTS - Install Locally - Test with Hindi, Urdu, Tamil and Other Languages","channel":"Fahd Mirza","upload_date":null,"view_count":8328,"duration":791}
{"id":"anplUNnkM68","title":"Fine tuning Whisper for Speech Transcription","channel":"Trelis Research","upload_date":null,"view_count":62768,"duration":2966}
{"id":"xgBKvpiiYrI","title":"Speech-to-Text Model Demo - AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":2931,"duration":99}

```


### S4 supporting file: `yt_search_faster-whisper_tamil.csv` (verbatim)

```
﻿{"id":"uimBp3c3Koo","title":"Convert speech to text in realtime without delay | using faster-whisper module","channel":"KARTIS","upload_date":null,"view_count":31237,"duration":456}
{"id":"lpSahBCcgqc","title":"நினைத்ததை துரிதமாக அடைந்திட இதை செய்யுங்கள் | Whisper Method | Fast and Reliable | ND","channel":"Nithilan Dhandapani Podcast","upload_date":null,"view_count":20034,"duration":986}
{"id":"xJTFY5t9nQA","title":"பைத்தானைப் பயன்படுத்தி CPU-வில் வேகமான விஸ்பர் | வேகமான ஆஃப்லைன் டிரான்ஸ்கிரிப்ஷன் பயிற்சி","channel":"Stef from Samayas","upload_date":null,"view_count":1523,"duration":1045}
{"id":"R5bfClvmmqc","title":"Whisper Large V3 Turbo | Tested","channel":"David Hamner","upload_date":null,"view_count":11802,"duration":100}
{"id":"dg_TWk8Zfjk","title":"How to Use OpenAI\u0027s Whisper for Perfect Transcriptions (Speech to Text)","channel":"Teacher\u0027s Tech","upload_date":null,"view_count":139837,"duration":494}
{"id":"ABFqbY_rmEk","title":"How to Install \u0026 Use Whisper AI Voice to Text","channel":"Kevin Stratvert","upload_date":null,"view_count":797187,"duration":764}
{"id":"anplUNnkM68","title":"Fine tuning Whisper for Speech Transcription","channel":"Trelis Research","upload_date":null,"view_count":62768,"duration":2966}
{"id":"Tj8qOxZT06M","title":"Death Whisper Movie Explanation In Tamil | Tamil Voice Over | Mr Tamizhan | Movie Story \u0026 Review","channel":"kathai kalam","upload_date":null,"view_count":161,"duration":78}
{"id":"f7md4IS4qXQ","title":"They Will CALL You INSTANTLY After Listening To This Meditation | 5 Minutes","channel":"Law of Attraction Solutions","upload_date":null,"view_count":1309434,"duration":387}
{"id":"MRz4et4Sd0c","title":"24 Hours Whisper Method | अपनी Wish को Fast Manifest करने का सबसे Powerful तरीका!!!!","channel":"universaltruth1111","upload_date":null,"view_count":38093,"duration":818}

```


### S4 supporting file: `yt_search_sarvam_ai_tamil_voice.csv` (verbatim)

```
﻿{"id":"6od8EtAXm3M","title":"Sarvam AI | Real Time Voice Agent Exploring Video Tamil","channel":"AI with Thiru","upload_date":null,"view_count":5915,"duration":534}
{"id":"3eE4ZdnPNZU","title":"AI in Tamil 🚀 Sarvam AI | Language No Bar | Photoshop + DaVinci Resolve Edit 🔥 மொழி ஒரு தடையல்ல","channel":"Salavadi Eswaran","upload_date":null,"view_count":17517,"duration":920}
{"id":"04BSgrzOBVk","title":"Are We Using AI… Or Is AI Using Us? | Sarvam AI Founder Pratyush Kumar | Gobinath","channel":"Gobinath","upload_date":null,"view_count":187868,"duration":4346}
{"id":"y38bxfAX6Rg","title":"Sarvam AI Text to Speech in Action | Best AI Tamil Voice Generator (AI Tamil)","channel":"Tutusfunny tamil","upload_date":null,"view_count":194,"duration":531}
{"id":"-nCWBM4aE64","title":"How to Create Realistic AI Voice in Tamil | Free AI Voice Generator YouTube \u0026 Reels","channel":"SSK Decode ","upload_date":null,"view_count":47187,"duration":305}
{"id":"lnCTn6q6thE","title":"This AI Voice Generator Speaks 11 Indian Languages (@SarvamAI  )","channel":"Media Meets AI","upload_date":null,"view_count":50,"duration":66}
{"id":"I1o8QO7PU2U","title":"Sarvam AI Tutorial for Beginners (India’s Sovereign AI) | Ansh Mehra","channel":"The Cutting Edge School","upload_date":null,"view_count":82660,"duration":695}
{"id":"D0p2zIGOskM","title":"Sarvam AI Explained | India’s Own AI Model for Indian Languages | Tamil","channel":"Kishorelytics","upload_date":null,"view_count":95,"duration":921}
{"id":"4t_coQGUbOo","title":"HeyKoala AI selected for Sarvam AI Startup Program","channel":"HeyKoala AI","upload_date":null,"view_count":129,"duration":30}
{"id":"uLFfTNPTM9I","title":"இந்தியாவின் சொந்த AI! | Sarvam AI Explained in Tamil #SarvamAI #ArtificialIntelligence #MadeInIndia","channel":"Infostream","upload_date":null,"view_count":46,"duration":241}

```


### S4 supporting file: `yt_search_tamil_speech_recognition_ai.csv` (verbatim)

```
﻿{"id":"V3tmtEM_uhk","title":"Build an AI Voice Assistant with Python | Listen, Think \u0026 Speak | Tamil | Karthik\u0027s Show","channel":"Karthik\u0027s Show","upload_date":null,"view_count":2550,"duration":1332}
{"id":"Upl7q8GP-xA","title":"Voice Recognition Technology | Explained | Learn It in English","channel":"Learn It In Tamil","upload_date":null,"view_count":6166,"duration":182}
{"id":"6od8EtAXm3M","title":"Sarvam AI | Real Time Voice Agent Exploring Video Tamil","channel":"AI with Thiru","upload_date":null,"view_count":5915,"duration":534}
{"id":"xHvWsePTs3I","title":"How to Build Your Own JARVIS AI Agent 100% Free! | LiveKit Tutorial #tamil","channel":"Echo Mind","upload_date":null,"view_count":11339,"duration":795}
{"id":"hoA-xO3Zzio","title":"Automatic  Speech  Recognition in Tamil | Thenkachi ko swaminathan inspired recreation.","channel":"Tech Thuli","upload_date":null,"view_count":92,"duration":340}
{"id":"56_lZDOwSKo","title":"Automatic Speech Recognition: An Overview","channel":"Tamil Internet Conferences","upload_date":null,"view_count":11499,"duration":4154}
{"id":"6altVgTOf9s","title":"How Does Speech Recognition Work? Learn about Speech to Text, Voice Recognition and Speech Synthesis","channel":"Acadaimy","upload_date":null,"view_count":130452,"duration":384}
{"id":"PKHA92gusTM","title":"How to Install Whisper AI - Complete Tutorial | Tamil Audio to Text | Ep. 12 #RTR #ai #transcription","channel":"RTR Unfiltered","upload_date":null,"view_count":1280,"duration":1020}
{"id":"Tw7hLBMA1Pk","title":"Tamil Voice Typing 🔥 How to use on iPhone and iPad?","channel":"iRobinPro","upload_date":null,"view_count":90275,"duration":300}
{"id":"FGeYswHAn5g","title":"SPEECH RECOGNITION-Artificial Intelligence-NLP-20A05502T-unit-4-Natural Language for Communication","channel":"D Sumathi","upload_date":null,"view_count":9220,"duration":1143}

```


### S4 supporting file: `yt_search_tanglish_transcription_demo.csv` (verbatim)

```
﻿{"id":"Tw7hLBMA1Pk","title":"Tamil Voice Typing 🔥 How to use on iPhone and iPad?","channel":"iRobinPro","upload_date":null,"view_count":90275,"duration":300}
{"id":"GmRG59OD26U","title":"Tamil Transcription 8k Training Part 1","channel":"Data Mining","upload_date":null,"view_count":67,"duration":1280}
{"id":"PKHA92gusTM","title":"How to Install Whisper AI - Complete Tutorial | Tamil Audio to Text | Ep. 12 #RTR #ai #transcription","channel":"RTR Unfiltered","upload_date":null,"view_count":1280,"duration":1020}
{"id":"BMe9QFU2GSY","title":"How to Use Google Gemini to Automatically Transcribe Audio or Video to Text Transcripts","channel":"AI Mastery","upload_date":null,"view_count":17768,"duration":184}
{"id":"GEpqRST7Oj0","title":"How to Teach Phonetics Using Flashcards |Demo","channel":"Tlm with KeeMoh","upload_date":null,"view_count":10,"duration":125}
{"id":"Ra3brxxNX4s","title":"How to Use ChatGPT as a Language Translation Tool","channel":"Keywords Everywhere","upload_date":null,"view_count":88219,"duration":346}
{"id":"U9Cs9gwNZOY","title":"Translator from Tamil to English and from English to Tamil how to just Vice Sounds Use and Type easy","channel":"Lot Of Technology","upload_date":null,"view_count":92,"duration":244}
{"id":"orTVWvbMk6s","title":"12th Zoology | CH 5 Transcription \u0026 Translation | State Board | Asha Ma\u0027am","channel":"Vedantu 11th 12th State Board NEET Tamil","upload_date":null,"view_count":4067,"duration":2963}
{"id":"mALoIKrK_ms","title":"How to Type Tamil easy in Smartphone | Direct typing Tanglish | Google Indic Keyboard","channel":"Tech Ajith","upload_date":null,"view_count":240,"duration":156}
{"id":"CCkoqOKKjcA","title":"Live transcribe.. Tutorial video.. / voice to text converter /easy voice to text","channel":"SCI-TECH MEDIA","upload_date":null,"view_count":161,"duration":410}

```


### S4 supporting file: `yt_search_whisper_tamil_speech_to_text.csv` (verbatim)

```
﻿{"id":"PKHA92gusTM","title":"How to Install Whisper AI - Complete Tutorial | Tamil Audio to Text | Ep. 12 #RTR #ai #transcription","channel":"RTR Unfiltered","upload_date":null,"view_count":1280,"duration":1020}
{"id":"HbY51mVKrcE","title":"OpenAI Whisper Demo: Convert Speech to Text in Python","channel":"Rob Mulla","upload_date":null,"view_count":164870,"duration":299}
{"id":"uimBp3c3Koo","title":"Convert speech to text in realtime without delay | using faster-whisper module","channel":"KARTIS","upload_date":null,"view_count":31237,"duration":456}
{"id":"dg_TWk8Zfjk","title":"How to Use OpenAI\u0027s Whisper for Perfect Transcriptions (Speech to Text)","channel":"Teacher\u0027s Tech","upload_date":null,"view_count":139837,"duration":494}
{"id":"fyifKHq8XaY","title":"How to Use Wispr Flow - The Best Voice to Text App (FULL GUIDE)","channel":"Alec Wilcock","upload_date":null,"view_count":106886,"duration":649}
{"id":"ABFqbY_rmEk","title":"How to Install \u0026 Use Whisper AI Voice to Text","channel":"Kevin Stratvert","upload_date":null,"view_count":797187,"duration":764}
{"id":"bOW8tV15rBs","title":"Voice to Text Typing - Best Free Tool in Tamil Typing | Speech to Text Typing | Easy Tamil Typing","channel":"Alpha6 Learning Tamil","upload_date":null,"view_count":1880,"duration":276}
{"id":"V3tmtEM_uhk","title":"Build an AI Voice Assistant with Python | Listen, Think \u0026 Speak | Tamil | Karthik\u0027s Show","channel":"Karthik\u0027s Show","upload_date":null,"view_count":2550,"duration":1332}
{"id":"86GzmsPcUgw","title":"Whisper OpenAI Unveiled Tamil AI for Hackers  Artificial Intelligence More Dangerous than Phishing","channel":"Scholarly Thugs","upload_date":null,"view_count":217,"duration":473}
{"id":"xgBKvpiiYrI","title":"Speech-to-Text Model Demo - AI4Bharat","channel":"AI4Bharat","upload_date":null,"view_count":2931,"duration":99}

```


### S4 supporting file: `video_metadata.json` (verbatim)

```
﻿[
    {
        "id":  "PKHA92gusTM",
        "url":  "https://www.youtube.com/watch?v=PKHA92gusTM",
        "title":  "How to Install Whisper AI - Complete Tutorial | Tamil Audio to Text | Ep. 12 #RTR #ai #transcription",
        "channel":  "RTR Unfiltered",
        "upload_date":  "20250418",
        "view_count":  1281,
        "duration":  1020,
        "description":  "Curious about AI and how it’s shaping the future of technology? In this tech tutorial, we dive into the world of artificial intelligence, voice recognition, and speech to text using open source tools. Whether you\u0027re a tech enthusiast, student, or just starting your journey in computer science basics, this beginner tutorial is packed with trending tech insights and hands-on learning. Discover how to install powerful AI tools on your own system and unlock the potential of productivity tools through digital transformation. Perfect for those who want to learn technology, explore programming tutorials, and stay ahead in tech trends.\n\nWhisper AI: https://openai.com/index/whisper/\nCodebase: https://github.com/RTR95/whisperAI\nPython: https://www.python.org/downloads/\nPyTorch: https://pytorch.org/\n\n**Follow RTR Unfiltered on **\nInstagram - https://www.instagram.com/rtr.unfiltered/\nSpotify - https://open.spotify.com/show/77klNnKp8DBEoJLqf1QXbY\nApple Podcasts - https://podcasts.apple.com/us/podcast/rtr-unfiltered/id1805635024\nPrime Music - https://music.amazon.in/podcasts/dfbde888-4937-4a64-9232-cbbb169473bb/rtr-unfiltered\n*****\n\nStuffs \u0026 Things: \nCamera: Nothing Phone (2) https://amzn.to/3HhUSpd\nMic: Maono Dynamic Gaming Mic with RGB Light - PD100X https://amzn.to/4jtKNmo\nKey Light: Kreo Slab Key Light https://amzn.to/3Z7GYfG\nHeadphones: Sony WH-CH520 Wireless BT https://amzn.to/44YoVw6\niPod Classic: Apple iPod Classic Video 5th Generation\nEditing: Magix Vegas Pro 22\n\n00:00 - CHECK\n00:03 - Intro\n01:06 - Title\n01:15 - AI for Everyone\n01:42 - Spoiler\n01:56 - Tool Reveal\n02:56 - READ THE MANUAL!!!\n03:32 - Example/Test\n04:03 - Benefits of Whisper\n04:27 - Prerequisites\n04:50 - 0. Love for Open-Source\n05:23 - 1. Python Installation\n06:20 - 2. PyTorch Setup\n07:30 - 3. TikToken Installation\n07:43 - 4. Whisper AI installation\n08:31 - 5a. FFMpeg Installation\n09:05 - 5b. Rust Setup\n09:26 - Whisper AI Models\n10:26 - Test Audio Capturing\n11:03 - Whisper Initialization\n11:57 - Whisper in Action!\n12:10 - Results\n13:06 - Hidden Features of Whisper AI\n14:26 - End of the Demo\n16:00 - Outro\n16:22 - Karuthu Section\n\n#AITutorial #LearnAI #TechForBeginners #FutureOfTech #MachineLearning #VoiceToText #ArtificialIntelligence #TechExplained #CodingMadeEasy #OpenSourceTools #TechEducation #NextGenTech #AIForEveryone"
    },
    {
        "id":  "uimBp3c3Koo",
        "url":  "https://www.youtube.com/watch?v=uimBp3c3Koo",
        "title":  "Convert speech to text in realtime without delay | using faster-whisper module",
        "channel":  "KARTIS",
        "upload_date":  "20250429",
        "view_count":  31236,
        "duration":  456,
        "description":  "In this tutorial, you\u0027ll learn how to use the Faster-Whisper module in Python to achieve real-time audio transcription with high accuracy and low latency. Faster-Whisper is a fast and lightweight implementation of OpenAI\u0027s Whisper ASR model, optimized for performance on both CPU and GPU.\n\nWe’ll walk through:\n\nInstalling and setting up Faster-Whisper\nCapturing real-time audio input\nProcessing and transcribing speech on the fly\nTips for improving speed and accuracy\nWhether you\u0027re building a voice assistant, live captioning tool, or speech analytics app, this tutorial will give you a solid foundation for integrating real-time speech-to-text in your Python projects.\n\n\nGithub Repo:\nhttps://github.com/SYSTRAN/faster-whisper\n\nTools Used:\nPython\nFaster-Whisper\nPyAudio / sounddevice\nOptional: GPU support for better performance\nSubscribe for more tutorials on AI, machine learning, and real-time systems!\n\n\n\nMake sure you subscribe for latest updates and announcements from our channel\n\nABOUT MY CHANNEL\nThis channel is about General contents that are likely to be Informative. We will cover more common Topics which will be More Innovative in Daily needs.\n\nFOLLOW ME ON SOCIAL\nFollow me in Instagram: https://www.instagram.com/kartis_official/\nFacebook Page: https://www.facebook.com/Kartis-101340512507864/\n\nTimeline:\n\n\nollama,home assistant,ollama tutorial,ollama home assistant,home assistant ollama,home assistant voice,ollama voice assistant,ai assistant with ollama,llama 3,assistant,llama 3 home assistant,ollama llm,home assistant voice ollama,ai assistant,ollama code assistant tutorial,llama3,ollama ai,ollama api,ollama server,how to install ollama,local ollama,ollama python,llama,ollama llama,llama 2,run ollama locally,local ai assistant, \njarvis technology,tony stark,artificial intelligence,AI,future technology,how to create a bot,how to create ai,machine learning,deep learning,avengers jarvis,tony stark techology,tony stark computer,make your pc like tony stark jarvis artificial intelligence,advanced programming,iron man technology,iron man jarvis,iron man\u0027s AI,jarvis tutorial,project jarvis,ui development,ui/ux designing,gui for jarvis,user interface,graphical user interface,jarvis, jarvis technology,jarvis,tony stark,artificial intelligence,AI,future technology,i created jarvis,how to create a bot,how to create a tool,how to create ai,machine learning,deep learning,avengers jarvis,tony stark techology,tony stark computer,make your pc like tony stark jarvis artificial intelligence,real life , jarvis technology,jarvis,tony stark,artificial intelligence,AI,future technology,i created jarvis,how to create a bot,how to create a tool,how to create ai,machine learning,deep learning,avengers jarvis,tony stark techology,tony stark computer,make your pc like tony stark jarvis artificial intelligence,real life robots,programming,advanced programming,iron man technology,iron man jarvis,iron man\u0027s AI,jarvis tutorial,project jarvis,programming tutorialrobots,programming,advanced programming,iron man technology,iron man jarvis,iron man\u0027s AI,jarvis tutorial,project jarvis,programming tutorial, #jarvisproject #tonystarktechnology #ironmantechnology #futuretech \ntony stark,how to create jarvis,real life tony stark,how to create my own jarvis,tony stark in real life,tony stark computer,tony starks robot,jarvis tony stark,tony stark jarvis,tony stark smart home,tony stark kills thanos,created,stark industries,make your pc like tony stark jarvis artificial intelligence,real life stark industries,stark industries in real life,tony,stark industries robot,tonystark,arc reactor,iron man arc reactor, artificial intelligence,what is artificial intelligence,artificial general intelligence,artificial intelligence explained,future artificial intelligence,artificial intelligence future,artificial intelligence edureka,artificial super intelligence,artificial intelligence tutorial,smartest artificial intelligence,artificial intelligence applications,artificial intelligence for beginners,artificial intelligence tutorial for beginners,learn artificial intelligence, iron man,iron man 2,real iron man suit,real life iron man,iron man armor"
    },
    {
        "id":  "xgBKvpiiYrI",
        "url":  "https://www.youtube.com/watch?v=xgBKvpiiYrI",
        "title":  "Speech-to-Text Model Demo - AI4Bharat",
        "channel":  "AI4Bharat",
        "upload_date":  "20221217",
        "view_count":  2931,
        "duration":  99,
        "description":  "Please try our model at - https://models.ai4bharat.org/#/asr\nSupported Languages -\nBangla, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Nepali, Oriya, Panjabi, Sanskrit, Sinhala, Tamil, Telugu, Urdu"
    },
    {
        "id":  "6od8EtAXm3M",
        "url":  "https://www.youtube.com/watch?v=6od8EtAXm3M",
        "title":  "Sarvam AI | Real Time Voice Agent Exploring Video Tamil",
        "channel":  "AI with Thiru",
        "upload_date":  "20260309",
        "view_count":  5915,
        "duration":  533,
        "description":  "In this video, we explore Sarvam AI’s Realtime Voice Agent and how developers can build AI systems that talk to users like a human. You’ll learn how realtime voice agents work, the architecture behind them, and how they combine speech recognition, LLM reasoning, and text-to-speech to create truly interactive AI experiences.\n\nTo learn Gen AI, AI Agents, Agentic AI, AI Automation and Microsaas Building, Join GEN AI Architect Community Now: https://my-url.in/youtube_architects_show_interest\n\nMachine Learning Book: https://topmate.io/thirumurugan_r/1919355\n\nInstagram: https://www.instagram.com/ai_with_thiru?igsh=MWkzeWdsOXU4c3o0Ng==\n\n1:1 Mentorship : https://topmate.io/thirumurugan_r/\n\nIf you found this useful, SMASH that Like button and \nSubscribe — I post weekly videos on AI tools, Claude, \nand cutting-edge developer workflows.\n\nThis is part of the Agentic AI series on AI with Thiru — Subscribe for tutorials, demos, and real-world GenAI use cases in Tamil + English!\n\nsarvam ai, sarvam ai voice agent, realtime voice ai, voice ai agents, ai voice assistant, realtime ai agents, ai voice bot, speech to speech ai, voice interface ai, ai voice technology, build voice ai agent, ai voice architecture, llm voice agent, ai developer tools, conversational ai, speech to text ai, text to speech ai, voice ai tutorial, ai engineering, ai agents\n\n#AI #VoiceAI #AIAgents #SarvamAI #RealtimeAI #AIDevelopment #MachineLearning #ConversationalAI #SpeechToText #TextToSpeech #AIVoiceAgent #AIEngineering #ArtificialIntelligence #LLM #TechYouTube"
    },
    {
        "id":  "X1GK4iSNQJU",
        "url":  "https://www.youtube.com/watch?v=X1GK4iSNQJU",
        "title":  "Indic Parler-TTS - Install Locally - Test with Hindi, Urdu, Tamil and Other Languages",
        "channel":  "Fahd Mirza",
        "upload_date":  "20241204",
        "view_count":  8329,
        "duration":  790,
        "description":  "This video shows how to locally install Indic Parler-TTS which can officially speak in 20 Indic languages.\n\n🔥 Get 50% Discount on any A6000 or A5000 GPU rental, use following link and coupon:\n\nhttps://bit.ly/fahd-mirza\nCoupon code: FahdMirza\n\n🔥 Buy Me a Coffee to support the channel: https://ko-fi.com/fahdmirza\n\n#indiai #ai4bharat #indicparlertts #indicparlartts\n\nPLEASE FOLLOW ME: \n▶ LinkedIn:  https://www.linkedin.com/in/fahdmirza/\n▶ YouTube: https://www.youtube.com/@fahdmirza\n▶ Blog: https://www.fahdmirza.com\n\nRELATED VIDEOS:\n\n▶ Code https://www.fahdmirza.com/2024/12/install-indic-parler-tts-model-locally.html\n▶ Resource https://huggingface.co/ai4bharat/indic-parler-tts\n\nAll rights reserved © Fahd Mirza"
    },
    {
        "id":  "70Nrt_FpHz4",
        "url":  "https://www.youtube.com/watch?v=70Nrt_FpHz4",
        "title":  "37 Indian Language Speech to Text Pipeline | AI4Bharat IndicConformer ASR with JSON  SRT",
        "channel":  "Sudheendra S G",
        "upload_date":  "20260524",
        "view_count":  431,
        "duration":  1596,
        "description":  "00:00 Introduction to Session 37: Indian Regional Language Pipeline\n01:46 Downloading Session Files and Sample Videos\n03:04 Preparing Scripts and Opening Anaconda Prompt\n04:04 Checking audio-asr Environment and CUDA Support\n04:50 Extracting Audio Tracks with FFmpeg\n06:58 Preparing Hindi, Kannada, and Tamil WAV Files\n07:32 Introduction to AI4Bharat IndicConformer\n08:25 Accepting Hugging Face Model Access\n08:53 Switching to WSL2 for Indic ASR\n09:41 Checking Conda, Mamba, and Hugging Face Cache Paths\n10:03 Creating audio-indic-asr Conda Environment\n10:47 Upgrading pip and Setup Tools\n11:08 Checking NVIDIA GPU Access in WSL2\n11:31 Installing PyTorch with CUDA 12.8\n12:20 Testing PyTorch GPU Detection\n13:06 Installing Compatible Transformers and Tokenizers\n14:01 Installing ONNX Runtime Dependencies\n15:00 Installing Audio Utility Packages\n15:22 Logging into Hugging Face\n16:47 Installing and Testing TorchCodec\n17:22 Installing FFmpeg in WSL2\n18:00 Why Silence-Aware Audio Chunking Is Needed\n19:10 Reviewing the Indian Language Transcription Script\n20:00 Understanding Language Codes and Model Options\n20:39 Running the Script with Input, Language, and Chunk Parameters\n23:00 Fixing WSL2 Path Issues\n23:20 Running Hindi Transcription\n24:00 Reviewing JSON, TXT, and SRT Outputs\n24:30 Running Kannada Transcription\n25:12 Running Tamil Transcription\n26:00 Final Output Review and Next Session Preview\n\nFor free resources and course materials visit the below patreon page\n\nhttps://www.patreon.com/posts/151488430\n\nIn this session, we build a local Indian regional language speech-to-text pipeline using AI4Bharat IndicConformer ASR.\n\nInstead of starting from English content, this workflow works directly with Indian language videos and audio files. We take source speech in languages like Hindi, Kannada, Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Urdu and other supported Indian languages, then convert them into structured transcript outputs.\n\nIn this tutorial, you will learn how to:\n\n✅ Extract audio from video using FFmpeg\n✅ Prepare 16 kHz mono WAV files for ASR\n✅ Set up a WSL2-based AI environment\n✅ Create and activate a Conda environment for Indic ASR\n✅ Install PyTorch with CUDA support\n✅ Install Transformers, ONNX Runtime, FFmpeg and required audio packages\n✅ Use AI4Bharat IndicConformer for Indian-language transcription\n✅ Run a parameter-based Python transcription script\n✅ Generate JSON, TXT and SRT subtitle files\n✅ Use silence-aware chunking to avoid cutting words and sentences\n✅ Transcribe Hindi, Kannada and Tamil sample videos\n✅ Prepare output files for future translation and dubbing workflows\n\nThis pipeline is useful for educators, content creators, AI filmmakers, dubbing workflows, regional language documentation, LMS content preparation, subtitle generation and multilingual media automation.\n\nThe generated outputs include:\n\n1. JSON segment file  \n2. Plain text transcript  \n3. SRT subtitle file  \n\nThe JSON file is especially important because it stores the transcript with structured timing information, making it useful for translation, TTS, dubbing, subtitles and future AI workflows.\n\nTools and technologies used:\n\n- AI4Bharat IndicConformer\n- WSL2 Ubuntu\n- Conda / Mamba\n- PyTorch CUDA\n- Hugging Face\n- FFmpeg\n- ONNX Runtime\n- Python\n- Silence-aware audio chunking\n- JSON, TXT and SRT generation\n\nThis is part of our local AI Film Studio and multilingual Indian language workflow series.\n\n#AI4Bharat #IndicConformer #SpeechToText #IndianLanguages #HindiASR #KannadaASR #TamilASR #TeluguASR #WSL2 #PyTorch #FFmpeg #HuggingFace #Python #Subtitles #SRT #AIWorkflow #LocalAI #AIFilmStudio #RegionalLanguages #MultilingualAI"
    },
    {
        "id":  "7yWXkWvqSrA",
        "url":  "https://www.youtube.com/watch?v=7yWXkWvqSrA",
        "title":  "38 AI4Bharat Indic Conformer Tutorial",
        "channel":  "Sudheendra S G",
        "upload_date":  "20260524",
        "view_count":  377,
        "duration":  448,
        "description":  "00:00 - Why Indian Language ASR Needs a Specialized Pipeline\n00:38 - Preparing Video Audio with FFmpeg\n01:18 - Setting Up WSL2, CUDA \u0026 Python Environment\n02:06 - Accessing AI4Bharat Indic Conformer on Hugging Face\n02:47 - Fixing Windows-to-Linux Path Issues\n03:10 - Silence-Aware Audio Chunking\n03:36 - Running Transcription for Hindi, Kannada \u0026 Tamil\n04:20 - Reviewing JSON, TXT \u0026 SRT Outputs\n04:55 - Final Result: Local Indian Language Transcription Pipeline\n\nFor free resources and course materials visit the below patreon page\n\nhttps://www.patreon.com/posts/151488430\n\nIn this video, we build a local Indian language speech-to-text pipeline using AI4Bharat’s Indic Conformer model.\n\nMost standard English transcription tools struggle with Indian regional languages like Hindi, Kannada, and Tamil. They often produce broken words, incorrect accents, or hallucinated text. So in this workflow, we use a specialized Indic ASR model designed for Indian speech.\n\nYou will see how to prepare video audio using FFmpeg, convert it into the required 16 kHz mono WAV format, set up a stable WSL2 Linux environment, install CUDA-compatible PyTorch dependencies, access the AI4Bharat Indic Conformer model from Hugging Face, and run a reusable transcription script.\n\nThe pipeline outputs three useful files:\n\n1. Structured JSON segments with timestamps\n2. Plain text transcript\n3. Ready-to-use SRT subtitle file\n\nWe also cover important practical issues like Windows-to-Linux path conversion, Hugging Face authentication, avoiding TorchCodec conflicts, and silence-aware chunking so words are not split in the middle.\n\nThis forms the base layer for future AI workflows like translation, multilingual dubbing, subtitle generation, and local Indian language automation.\n\nTopics covered:\n- AI4Bharat Indic Conformer\n- Indian language ASR\n- Hindi, Kannada, and Tamil transcription\n- FFmpeg audio extraction\n- WSL2 setup\n- CUDA PyTorch installation\n- Hugging Face model access\n- JSON, TXT, and SRT output generation\n- Silence-aware audio chunking\n\n#AI4Bharat #IndicConformer #IndianLanguages #SpeechToText #ASR #HindiASR #KannadaASR #TamilASR #WSL2 #CUDA #FFmpeg #LocalAI #OpenSourceAI #IndianAI"
    },
    {
        "id":  "V3tmtEM_uhk",
        "url":  "https://www.youtube.com/watch?v=V3tmtEM_uhk",
        "title":  "Build an AI Voice Assistant with Python | Listen, Think \u0026 Speak | Tamil | Karthik\u0027s Show",
        "channel":  "Karthik\u0027s Show",
        "upload_date":  "20260724",
        "view_count":  2547,
        "duration":  1332,
        "description":  "Build your own AI Voice Assistant using Python in this beginner-friendly Tamil tutorial.\n\nIn this project, we create an application that can:\n\n🎙️ Listen to a spoken question\n📝 Convert speech into text using Whisper\n🤖 Generate an AI response using Groq\n🔊 Convert the answer back into speech using gTTS\n🧪 Use GitHub Copilot as a software tester to review failure scenarios and improve reliability\n\nThis project is part of the AI Projects Series on Karthik’s Show, where we build practical AI applications step by step. \n\nAI Projects Series playlist:  https://www.youtube.com/playlist?list=PLE1SJVkd0yXo\n\nWhat you will learn\n\n* How to capture microphone input in Streamlit\n* How speech-to-text works\n* How to use Groq Whisper for transcription\n* How to send the transcribed question to an LLM\n* How to convert AI text into spoken audio\n* How to validate empty responses\n* How to use GitHub Copilot for code review and testing\n\nTimestamps:\n00:00 Intro and demo\n00:54 Project setup\n03:35 Build the Voice Assistant\n14:13 GitHub Copilot review\n18:23 Final demo and recap\n19:29 Next project preview\n\nTools used\n\n* Python\n* Streamlit\n* Groq\n* Whisper\n* gTTS\n* GitHub Copilot\n* VS Code\n\nThe complete source code and prompt templates are available in the GitHub repository below:\n\n🔗 GitHub: https://github.com/KarthiksShow/ai-voice-assistant\nGroq API Link: https://console.groq.com/docs/models\n\nWatch the previous projects in this AI Projects Series and follow along as we move from beginner to intermediate-level AI applications.\n\nIf this video helps you, like the video, share it, and subscribe to Karthik’s Show for more beginner-friendly AI and Python tutorials in Tamil.\n\nCheck \u0027Python Programming for Beginners\u0027 Tamil course at https://www.karthiksshow.com/courses/Python-Programming-for-Beginners-638dbf0ce4b09464540754a9. \n\nCheck \u0027Python Programming for Machine Learning\u0027 Tamil course at https://www.karthiksshow.com/courses/Python-Programming-for-Machine-Learning-649d29ace4b0834a0c48cee3\n\nCheck \"Python Programming Package\" at https://www.karthiksshow.com/courses/Python-Programming-Package-64f2c028e4b039bbd3fe6bf5\n\n#AIVoiceAssistant #PythonProject #ArtificialIntelligence #Streamlit #Groq #WhisperAI #GitHubCopilot #TamilTutorial #AIProjects #KarthiksShow"
    },
    {
        "id":  "hoA-xO3Zzio",
        "url":  "https://www.youtube.com/watch?v=hoA-xO3Zzio",
        "title":  "Automatic  Speech  Recognition in Tamil | Thenkachi ko swaminathan inspired recreation.",
        "channel":  "Tech Thuli",
        "upload_date":  "20260310",
        "view_count":  92,
        "duration":  340,
        "description":  "We all loved and enjoyed Thenkachi ko Swamination Radio stories. So we tried recreating his way of story telling for teaching AI and tech to common people"
    }
]

```


### S4 supporting file: `additional_video_metadata.json` (verbatim)

```
﻿[
    {
        "id":  "cmy2zf6CuH4",
        "url":  "https://www.youtube.com/watch?v=cmy2zf6CuH4",
        "title":  "Automatic Speech Recognition system for Indian Languages “IndicWav2Vec”",
        "channel":  "AI4Bharat",
        "upload_date":  "20220822",
        "view_count":  5345,
        "duration":  925,
        "description":  ""
    },
    {
        "id":  "xHvWsePTs3I",
        "url":  "https://www.youtube.com/watch?v=xHvWsePTs3I",
        "title":  "How to Build Your Own JARVIS AI Agent 100% Free! | LiveKit Tutorial #tamil",
        "channel":  "Echo Mind",
        "upload_date":  "20250817",
        "view_count":  11340,
        "duration":  794,
        "description":  "#JARVIS #Gemini #IronMan\n🚀 Build Your Own JARVIS AI Agent – 100% Free!\n\nAll in one epic tutorial – and it\u0027s completely FREE.\n\nCODE  \nhttps://github.com/jeshinjs/Jarvis_v1\n\nIn this video, I’ll show you how to create your very own AI Voice Agent using LiveKit and other free tools. This isn’t just a basic chatbot – this JARVIS-like agent is super responsive, intelligent, and packed with powerful features:\n\n✅ Real-time voice \u0026 text conversation\n✅ Camera vision integration\n✅ Web search capabilities\n✅ Weather-checking tool\n\nWhether you\u0027re a beginner or an AI enthusiast, this step-by-step guide will walk you through everything you need to build and deploy your personal assistant – no paid APIs or expensive tools required.\n\n🔧 Tech stack: LiveKit, Open Source Tools, Custom Python Scripting\n📲 Final product: Fully functional AI assistant running on your Phone, on your PC and in your Browser!\n#AI #JARVIS #LiveKit #VoiceAgent #Gemini #FreeAI #OpenSource #AndroidApp #AITutorial #ArtificialIntelligence #PythonTutorial #IronMan"
    },
    {
        "id":  "3eE4ZdnPNZU",
        "url":  "https://www.youtube.com/watch?v=3eE4ZdnPNZU",
        "title":  "AI in Tamil 🚀 Sarvam AI | Language No Bar | Photoshop + DaVinci Resolve Edit 🔥 மொழி ஒரு தடையல்ல",
        "channel":  "Salavadi Eswaran",
        "upload_date":  "20260221",
        "view_count":  17517,
        "duration":  920,
        "description":  "Sarvam AI – மொழி ஒரு தடையல்ல | Language No Bar 🌍\n\nIn this video, I explain how AI is breaking language barriers and empowering Tamil creators worldwide.\n\nThrough Sarvam AI, we explore how technology makes the world accessible in any language. Whether you are a Tamil content creator, student, or tech enthusiast, this video shows how AI is transforming communication.\n#SarvamAI\n#TamilAI\n#LanguageNoBar\n#மொழிஒருதடையல்ல\n#AITamil\n#AIforCreators\n#TamilTech\n#PhotoshopEditing\n#DaVinciResolve\n#ThumbnailDesign\n#YouTubeGrowth\n#ContentCreatorTamil\n#BharathiColours\n#ArtificialIntelligence\n#TamilYouTuber"
    },
    {
        "id":  "y38bxfAX6Rg",
        "url":  "https://www.youtube.com/watch?v=y38bxfAX6Rg",
        "title":  "Sarvam AI Text to Speech in Action | Best AI Tamil Voice Generator (AI Tamil)",
        "channel":  "Tutusfunny tamil",
        "upload_date":  "20260706",
        "view_count":  195,
        "duration":  531,
        "description":  "Want to experience the power of next-gen AI voice technology? In this video, I will show you Sarvam AI Text to Speech in action and how it is changing the way we use AI Tamil voice systems.\n\nIf you are interested in building smart voice assistants, this tutorial will help you understand everything step by step. We will also explore Sarvam AI and its powerful features for creating realistic AI voices.\n\n🤖 In this video you will learn:\n✔ What is Sarvam AI\n✔ How Sarvam AI Text to Speech works\n✔ Real demo of AI Tamil voice output\n✔ How to set up voice AI agent on Sarvam\n✔ Step-by-step guide for beginners\n\n💡 If you are searching for how to set up voice AI agent on Sarvam, this video is perfect for you. I have explained everything in a simple and practical way so anyone can follow easily.\n\n🔥 Whether you are a developer, content creator, or AI enthusiast, Sarvam AI can help you create powerful voice-based applications with ease.\n\n📌 Don’t forget to LIKE 👍, SHARE 🔁, and SUBSCRIBE 🔔 for more AI Tamil tutorials and tech updates!\n\n#SarvamAI #SarvamAITextToSpeech #VoiceAIAgent #AIAgentSetup #HowToSetUpVoiceAIAgentOnSarvam #AI #AITamil #TextToSpeech #AIVoice #TechTutorial #AITutorial #ArtificialIntelligence"
    },
    {
        "id":  "lnCTn6q6thE",
        "url":  "https://www.youtube.com/watch?v=lnCTn6q6thE",
        "title":  "This AI Voice Generator Speaks 11 Indian Languages (@SarvamAI  )",
        "channel":  "Media Meets AI",
        "upload_date":  "20260727",
        "view_count":  50,
        "duration":  65,
        "description":  "Looking for a free AI voice generator that actually sounds natural in Hindi, Tamil, Telugu, and other Indian languages? Meet @SarvamAI , an Indian startup solving AI voice cloning and text to speech for India specifically, not bolted onto an English model like most global tools.\n\nPaste a script, pick a voice, get broadcast ready narration in seconds — names pronounced right, natural Hindi-English code switching included.\n\nThis isn\u0027t about replacing voice artists. It\u0027s about the regional content that never got made because there wasn\u0027t budget for separate artists in every language finally getting a shot.\n\nPart of a series breaking down the AI tools quietly changing how media and entertainment gets made. Follow for more on AI voice generators, AI in media, and where video tech is headed next.\n\n\n#AIVoiceGenerator #AIVoiceCloning #TextToSpeech #SarvamAI #AITools #AIinMedia #IndianLanguages #Dubbing #MediaTech #ArtificialIntelligence\n\n\nInterested in AI for video workflows?\n\nCheck out Decouple AI, the platform I\u0027m building to automate livestream and video clipping, editing, and publishing for broadcasters, media teams, and creators.\n\nhttps://decouple.live/"
    }
]

```


### S4 transcript `70Nrt_FpHz4.en.vtt` (auto-captions; timestamps and rolling-caption duplicates removed; full VTT in research_raw/transcripts/)

Hello and welcome to our 37th session. In the previous session, we completed the first part of our multilingual AI workflows, where we started with English content and translated it into Indian 
regional languages. In this session, instead of starting from English, we are working directly with Indian regional languages and video content. That means the source speech itself can be in 
languages like Hindi, Kannada, Telugu, Tamil, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Urdu or any supported Indian languages. The first step in this process is transcription. We use one 
common transcription script where the input file and source language are passed as parameters. For example, the same script can transcribe a Hindi video, a Kannada video, a Tamil lecture or a Telugu 
speech just by changing the language code in the command. The script then generates three important output files: a JSON segment file, a plain text transcript and an SRT subtitle file. The JSON file 
is especially important because it stores the transcript in structured segments along with start and end timing. So, from one Indian language audio or video file, we can get machine-readable, 
human-readable and subtitle-ready output. In this phase, our focus is very clear. Take Indian regional language audio or video, transcribe into JSON, text and SRT file. We build a reusable Indian 
multilingual media pipeline. One that can listen to Indian language content, convert it into structured texts and subtitles, and then transform it into another Indian language for education, dubbing, 
training videos, documentation and regional content creation. I have already provided you with some Python scripts for this particular session. And to get these Python scripts and also sample 
different language videos, you can come into YouTube video page or in the e-learning page, scroll down and in the description click on more. And if you scroll down, you have a Patreon link here. 
Click on this Patreon link. This will bring you to the AI Filming Studio Patreon page. Scroll down and you are provided with 37 Indian regional languages translate.zip file. Click on this file to 
download it. Once the file is downloaded, come to the downloads folder, select this zip file, click extract all and click the extract button. Now, inside you can see three MP4 files. One is a Tamil 
video sample, another is Hindi and another is Kannada. You can select all these three files, right click and copy it. Come back to your PC D AI Studio audio folder. And in input, there is a folder 
called video. So, right click and paste these three videos. Coming back to the extracted folder, I have provided you with another two scripts. Select these two scripts, right click, copy it. Come 
back to D AI Studio audio and in script in phase four, right click and paste it. As we have already explored in our previous session, our first job is to extract only the audio track from all these 
video files. First, we are going to launch our Anaconda prompt because in this phase, we are going to run pipeline through our Windows platform. I will to search and type Anaconda and open it run as 
administrator. But, we are right now in the base environment. So, to see the list of all the environment, type conda env list. First step, environment that we are going to use here is this audio ASR 
environment. Type conda activate audio-asr and press enter. Let us first check whether this environment is running correctly for C translate to the AI studio audio scripts. I had already provided you 
a script check underscore C translate to dot py. This file is also present in our Patreon page also. I have to use this file through this path. We'll select this path, right click and copy it. Come 
back to Anaconda prompt, type Python space, press control V to paste the path, add backslash check underscore C translate to dot py. And if I press enter, you can see version number you are seeing. 
And if it shows CUDA devices equals one, then the CUDA device is correctly recognized. Now, our first job is to separate the audio track. Our source video files are in D AI studio audio and in the 
input, you have a folder called video. And here we have our actual videos. First, I have to take this video and separate the audio track. To do this, I will come back to my Anaconda prompt and I'm 
now going to use my FFmpeg command. The command is FFmpeg followed by hyphen Y hyphen I means the input source. The input source is D colon backslash AI studio backslash audio backslash input 
backslash video. And in this folder, separate the audio will be Hindi video sample. So, I will type this file name. Hindi underscore video underscore sample.mp4. This is my source file. Paste that 
hyphen VN. This is going to extract only the audio track. Then hyphen AC one make the track mono. Then hyphen AR type 16,000. Press space, give the output path. where I want to save this extracted 
audio file. D colon backward slash AI studio backward slash audio backward slash output backward slash. If I come to my folder, I want it in audio output. I want to create one folder here, audio 
tracks. So, I will come back, add audio tracks. I'm going to call this file Hindi underscore video underscore sample. Add a period and the format will be a wave format. If I press enter, the audio 
track will now be separated. To test it, if I come back to the explorer and in audio output audio tracks, Hindi video sample.wav. Double click and play it. You are getting the Hindi track. So, I will 
just press the up arrow to get the previous command. I will press the left arrow and I will first come into the input file name. I'm going to delete this old name, take Kannada underscore video 
underscore sample. In the output track, I'm now going to call this Kannada video sample. I will press enter to come to the end of the command and if I press enter and if I come back the audio output 
audio tracks, you are seeing the Kannada video sample. Press up arrow. I will move back with my left arrow and instead of Kannada here, Tamil video sample in the source name. And similarly in the 
output name also, replace this as Tamil video sample. Press enter to come to the end of the command and press enter. In audio output side audio tracks, I have all the three tracks. I will come to 
output and I will drag English 16K also into my audio tracks folder. So, for Indian languages, we are now going to again make use of another AI for Bharat model. Now, the model we are going to use is 
Indic Conformer. So in Google if you type Indic Conformer and press enter, you can see the first link here, Indic Conformer. And if I click on this link, you can come into the Hugging Face. You have 
various model available for Indic Conformer. You have one main model for all the languages. For every language, there is a separate model available here. In this session, we are going to use this 
common model, AI for Bharat Indic Conformer. And if I click on this model, I have to log in into my Hugging Face account. I have already logged in and click on agree and assess repository. You have 
to provide your contact information to use this model. So I will click on agree. So I will now close my browser. For this Indic for Bharat model, we are going to use the Linux platform instead of the 
Windows platform. I have already shown you how to install WSL2. Search, type WSL, click on run as administrator. So you are now in the Linux WSL2 format. In our previous session, we have already 
installed Conda and Mamba. Type Conda two hyphen version. And if you see the version number, it means that Conda has been installed. Call Conda ENV list and press enter. We have already created one 
environment, Indic Translate, which we used it in our previous session. I will type Conda config two hyphen show and I want it to show my environment, I press enter, it should be in home Satwik AI 
Studio Conda environment. I will press up arrow to assess my previous command. And in instead of ENVS_DIRS, I will type PKGS_DIRS. Press enter. You can see this path is also set to this conda 
package. I type echo dollar HF underscore. If I press enter, see it is set to my AI studio models hugging face. We have already done it in our previous session. And if you doesn't know how to do 
these settings, you can refer our previous session where we created this Indic hyphen translate environment. I'm going to now create a new environment. I will use the command mamba create hyphen n 
the name of my environment. It is audio hyphen Indic hyphen ASR. The Python version Python equal 3.10. I will add hyphen y. And if I press enter, now a new environment will be created. I have to 
activate my environment. So, I will type conda activate the name of my environment audio hyphen Indic hyphen ASR. If you see this audio Indic ASR in the bracket before my prompt, it means that I am 
in this new environment. Let us start preparing our environment ready for our model. The first step is to install some of the dependency tool. Type Python hyphen m pip install two hyphen upgrade pip 
space setup tools and then space v. And if I press enter, so the pip will be upgraded to the latest version. Let us check whether my Nvidia card is accessed in this environment. So, for that I will 
type Nvidia hyphen SMI. And if I press enter, if you see the driver version, the name of your card and the RAM, it means that Nvidia card is correctly recognized in this environment. We are going to 
start torch installation. Now, coming into the prompt, I will call pip install first star, then torch vision torch audio. We are going to install this by a new address. So, I will add two hyphen, 
index hyphen URL. The address of the URL is https: {forward slash} two {forward slash} download.pytorch.org {forward slash} whl {forward slash} cu128 version. Because the latest 130 version, some 
drivers will not be correctly assessed in this current model. If I press enter, now the installation of torch, torch vision, and torch audio, it is going to download and install it. Once we have 
completed the installation of torch, we have to check whether this installation is correctly recognizing the GPU. So, to test it, if you come into explorer, D drive, AI studio, audio scripts, I have 
already provided you with this check_torch_gpu.py file. So, to assess this file, now I have to use this path and this file name. Come back to my Linux prompt, type python space the path of my file. I 
will add forward slash because it is Linux. I have to use mnt {forward slash} d, then my path, AI studio {forward slash} audio {forward slash} script {forward slash} the name of my file, which is 
check_torch_gpu.py. And if I press enter, it is going to test. And if you see this CUDA count as one and the name of your card, it means that torch has been successfully installed. I have to install 
a few more dependencies. I have to install the transformers, and I should not install the latest transformer version. It is not compatible as of now. So, I have to install a little older version. So, 
I will type pip install and add an inverted comma transformers I have to add two equal signs, then 4.4 4.40. 2 and end the inverted comma. And if I press enter, this 4.40.2 version transformer will 
be installed. I have to install tokenizer, that too of a specific version. So, I will type pip space install, again inverted comma, tokenizers, two equal sign. Version number is 0.19.1. End the 
inverted comma. If I press enter, even this installation is done correctly. Next, I will type pip install, install, add inverted comma, onnx runtime, two equal sign. The version number is 1.20.1. End 
the inverted comma and press the enter. So, this installation is going to happen. Next, type pip install, inverted comma, onnx, two equal sign, and the version number is 1.20.1. End the inverted 
comma and press enter. So, this version will now be installed. I should next install pip install, again add inverted comma and onnx runtime, two equal sign, 1.20. 1. Close it with inverted comma and 
press the enter button. I have to also install a few more dependencies. pip install pydub space SRT space tqdm space soundfile space ffmpeg-python. That is the Python version of ffmpeg. Press enter. 
This will also be now installed. We have to log in into hugging face to download the model. Just like last time, I will type I will type pip install {inverted comma} hugging face {hyphen} hub add two 
equal signs version is 0.23.5 and end it with {inverted comma} because the latest version is not compatible with this AI for Bharat model. So, I'm installing a older version of hugging face hub and 
now if I press enter, hugging face hub will be installed. I have to authenticate my account. So, I will type hugging face {hyphen} cli login to {hyphen} token. In the previous session, I had shown 
you how you can go into your hugging face login and if you click on your user icon, you have access token, create your token. So, this token is already created by us. I have saved it in a text 
document. So, I will close this and this text document is in D AI studio in this hugging face AI Bharat access token text file. I will double click to open it. Press control A to select this entire 
token, right click and copy. I will come into my WSL2 command window and if I right click, it will be pasted. Press right arrow and then press enter and now the authentication will be done and to 
test whether the authentication is done correctly, I will type hugging face {hyphen} cli who am I and you should see your name. If it appears, then you have logged in correctly. I will install torch 
product. So, I will add pip install. For safer side, I will add two {hyphen} no {hyphen} cache {hyphen} dir. So, I will add torch product and press enter. Torch product will be downloaded and 
installed. Now if I type pip show torch product and press enter, You can see that torch Kodak version 0.13 is correctly installed. Now, during installation, we had installed FFmpeg Python, but if we 
had not installed FFmpeg, type conda install {hyphen} c take it through the channel conda four. Type FFmpeg {hyphen} y and press enter. FFmpeg will be downloaded and installed. Type FFmpeg {hyphen} 
version and press enter. I should see the version number of FFmpeg. I should also see that my torch Kodak is running, right? Type Python {hyphen} c inverted comma, I will add a command import torch 
Kodak and end it with inverted comma. And if I press enter, if you doesn't get any error, it means that the torch Kodak is getting imported correctly. Now, unlike faster whisper, AI4Bharat does not 
chunk audio file into 10 seconds or 20 seconds clips automatically. We have to manually write a Python script to chunk our entire audio. I am feeding it with a 5 minutes audio means it should divide 
it into 10 10 seconds clip and from that 10 second clip, it has to do the transcription. One issue here is if you cut an audio exactly at 10 second, a sentence may be half cut, a word might be cut 
and that will be an issue in translation. We have to test at the 10th second, the sentence has not completed. It has to move a little forward or backward and close the sentence. How do you know that 
a sentence is completed in an audio? You will have a small gap of silence. So, I have to detect the silence and based on the silence, it has to cut the audio. Don't worry, this complicated process I 
have already implemented in my script and I have provided you the script. In free time, you can open the script and you can study how exactly it is done. Come into the AI Studio audio scripts phase 
four. I have already provided you with three transcribe any language.py file. If you right click and open it in Visual Studio Code, this file we have already downloaded at the start of this session 
from the Patreon page. If you scroll down, in this case you can see the language code for all the Indian language. You even have Sanskrit. If I move down, you have models. In case of this AI for 
Bharat, there is a separate model for Hindi, Kannada, Tamil, Telugu, Bengali. They have used separate models. The default model is good enough for all the languages. We are going to use this default 
model. Then if you scroll down, you have the various parameters that you have to apply for this Python script. First is the input. Let us start adding these parameters. I will come into my WSL 2 
command prompt. Type Python and the path to the script is we are in Linux. I have to add forward slash mount mnt forward/d/aistudio forward/audio forward/scripts forward/phase four forward/ the name 
of the file is three underscore transcribe underscore any underscore language.py. Press space. I have to give it a few parameters. The first parameter is my input file. So, I will add two hyphen 
input. I will add a space. Your input file is in DAI Studio audio output audio track. From the video track, we have separated the audio track using FFmpeg and you see this file. So, I will come back 
to my command now. forward/mnt forward/aistudio forward/output forward {slash} audio tracks. Forward {slash} name of the file is Hindi underscore video underscore sample.wav. I will come back to my 
code now. The language I will come back to my code type two hyphen language. I will type h i because this is Hindi audio. Space, come back to Visual Studio Code. The next parameter is model. I will 
set this to auto. The default value if it is set to auto, then I need not add this parameter model. You have decoder set to CTC. I will leave it as it is. Device is set to CUDA. I will leave it as it 
is. Chunk seconds is set to 20 seconds. 20 seconds is too large. I want this duration to be 10 seconds. I will come back to WSL2. I will add two hyphen chunk hyphen seconds and I will set it to 10. 
Press space. Now come back to Visual Studio Code. Split mode silence. I will leave it as it is. Overlap seconds. I will leave it as it is. Mini silence length 400 milliseconds. I will leave it as it 
is. Silence trash is set to 40. I will leave it as it is. Seek window 2500. I will leave it as it is. Mini chunk seconds is set to 3 seconds. I will leave it as it is. Sample rate is set to 16,000. I 
will leave it as it is. And now the output directory here I have already set it to output transcript. If I want a default folder, I can just set the path here. Working directory means when our audio 
is split into 10 10 seconds clip, it is temporarily stored in this folder. Created a new folder Indic underscore ASR underscore working output. I leave all other options as it is. There are no 
changes. Now I will come back to my WSL2 command. If I press enter, it is showing me an error because I have not given the input file path correctly. Press up arrow to come to my previous command. 
Left arrow and I will come here. I forgot to add D here. Mount, I will add forward slash D. So, I have missed this D. I will press N to come to the end of the line and if I press enter, chunking 
first takes place and after the chunking is over, then the transcription starts. See the See the transcription is happening. Wait for the full transcription to be over. If you come into folder D A 
Studio audio output. It has created a new folder in the underscore ASR underscore work. If you open it, you have Hindi video sample and here it will store the good file and if you come to output 
transcripts, a new folder Hindi is created. If you double click it, first I have the JSON file. If I right click and open it in Visual Studio Code, it is precisely translated. First is it is up to 
10.82 second, 10.8 to 21.34. But see, it is going to end the sentence correctly. When the chunking is done, it is correctly going to chunk at the end of the sentence. It will not abruptly cut at 10 
second or 20 second. Giving this script to you, so using this you need not worry about this abrupt cutting of sentences. Now, I will close this file, come back here to my folder. You have the 
subtitles and transcript file also and similarly, if I want to do Kannada transcription, I will come back to WSL 2, press up arrow to come into the previous command and I will leave everything as it 
is and I have to only change the input track. So, instead of Hindi video sample, I will delete this name. I will press delete to delete this I and I will [clears throat] type Kannada video sample 
now. And one more thing here, I have to change language. Here, I have set it to HI. If you come into your script, you move up, the code for Kannada here is KN. So, I will come back here and type the 
code KN. Press enter to come to the end of the line. If I press enter, now the entire translation is now going to happen in Kannada. The quality of this translation is very good Indian language. Now, 
similarly, I want to translate another file in Tamil. Press up arrow key. I will move my left key. I will delete this Kannada and I will type Tamil. Now, I will come in to language and in the 
language code, coming into my transcript for Tamil, the code is TA. I will delete KN and type TA. Press enter to come to the end of the line and press enter. The Tamil audio file will be taken. It 
will be chunked into 10 seconds where you have the silence. You can see the entire file is translated into Tamil. If you come into your folder, D audio output transcripts, you have three folders 
here. One for Hindi, one for Kannada, one for Tamil. And using the same system, you can translate it from Sanskrit audio, you can translate it from Punjabi audio. It is going to generate these three 
files. And if you open the text file and see it, you will have the precise translations. With this, you have been exposed to this new model, which is developed by AI for Bharat, which is called as 
Indic Conformer. And we have learned about how to use this Indic Conformer to convert our audio into a transcripted file. To translate this, we are going to do this in our next session. 


### S4 transcript `7yWXkWvqSrA.en.vtt` (auto-captions; timestamps and rolling-caption duplicates removed; full VTT in research_raw/transcripts/)

Standard English transcription tools struggle with Indian regional languages. Feed them Hindi or Tamil and you often get broken accents and strange hallucinated text. To get accurate results, we use 
a specialized engine. This AI for Bharat's Indic Conformer model is built specifically to handle the unique phonetics of regional Indian speech. Our goal today is to build a reusable local pipeline 
that takes raw Indian language video and outputs three distant files. This a structured JSON segment file, a plain text transcript, and a ready-to-use SRT subtitle track. To follow along, you need a 
Windows PC equipped with an Nvidia GPU, the Windows Subsystem for Linux or WSL2 installed, and the provided Python scripts downloaded to your working directory. Getting machine-readable text out of 
regional speech is the crucial first step. Without this reliable base layer, any automated translation or dubbing platform will fail. So, we start the preparation phase in Windows. Open your Windows 
search bar, type Anaconda, and run the Anaconda command prompt as an administrator. Before we run the AI model, we extract the raw audio track from our video file using FFmpeg. This terminal visual 
shows the strict input requirements of the AI for Bharat model. For it, pass three specific flags to FFmpeg. VN to strip away the video entirely, AC1 to force a single mono audio channel, and a 
16,000 reals to lock the sample rate exactly at 16 kilohertz. Run the command, then navigate to your output folder. You will find a clean isolated baby file that plays back the original regional 
speech perfectly. Forcing the audio into this precise 16 kilohertz mono format before doing anything else removes the vast majority of processing errors you would otherwise encounter during 
transcription. Now we leave Windows behind. Open your WSL2 Linux terminal. We execute the processing phase in Linux because AI models and CUDA dependencies are significantly more stable here. Staying 
in WSL2 prevents the missing BL errors that frequently crash these pipelines on native Windows. Use Mamba or Conda to create a new isolated environment specifically for this project and explicitly 
lock the Python version to 3.10. Activate the environment, then install PyTorch using the CUDA 12.8 index. The absolute latest versions are not always compatible, so we carefully install older 
verified versions of both the Transformers library and ONNX runtime alongside it. Finally, manually uninstall the torch codec package. It frequently causes fatal shared library conflicts with FFmpeg 
during runtime when we already have reliable audio extraction in place. By strictly controlling these software versions within an isolated Linux subsystem, we guarantee that the open-source AI tools 
communicate flawlessly with your underlying Nvidia hardware. Next, we require access to the model itself. Open your browser and navigate to the Hugging Face repository for AI for Bharots in Indic 
Conformer. You cannot download these models anonymously. You must log in, review the author's terms, and explicitly agree to request access. Once approved, go to your Hugging Face account settings, 
generate a new user access token, and copy it to your clipboard. Head back to your WSL2 terminal and run the Hugging Face CLI login command. Paste your token when prompted to verify your identity 
locally. Even when running open source code entirely on your own local hardware, these authenticated cloud handshakes are standard practice to protect proprietary model weights from unauthorized 
distribution. Before executing the final script, we must avoid a common syntax error. You cannot paste a standard Windows file paths into a Linux terminal. Windows uses drive letters like D: 
/AIStudio. Linux requires mounted directories. You must rewrite that path to read /mount/D/AIStudio. Large audio files also need to be broken down or chunked so the model can process them without 
running out of memory. If you blindly cut the audio every 10 seconds, you risk slicing a word right in half. Our script avoids this using silence-aware chunking. Instead of a hard cut, it searches 
for a natural acoustic pause, making the split there. Respecting these natural boundaries ensures the translation engine receives complete syllables, keeping it from guessing and generating incorrect 
words. We are ready to run. Fully call our main Python script and point the input path to the Hindi wave file we prepared earlier. We pass a few parameters setting the target language code to HI for 
Hindi and leaving the model selection on auto so it utilizes the main multilingual engine. Hit enter and let it process. Once it finishes, press the up arrow to recall the command. Change the input 
path to your Kannada audio file, swap the language code to KN and run it again. You can do the exact same thing with the Tamil code TA. A properly engineered AI environment abstracts linguistic 
complexity. Switching between vastly different regional dialects requires nothing more than changing a single two-letter variable. Open your standard Windows File Explorer and check the project 
output directory. You'll see a new set of folders organized automatically by language. This layout shows the output JSON segment file. It pairs the transcribed regional text with precise start and 
end timing data along with a firm language identifier tag. Alongside the JSON, the script generated a fully synchronized SRT captions. So we took unstructured regional video and successfully 
converted the speech into perfect time machine readable JSON data. That structured text bridges the gap giving us the exact foundation required to begin fully automated cross language dubbing. 


### S4 transcript `V3tmtEM_uhk.en.vtt` (auto-captions; timestamps and rolling-caption duplicates removed; full VTT in research_raw/transcripts/)

Hello friends, welcome. What is a neural network? A neural network is a computer system that works like the human brain. [music] Welcome back. Beginner level projects, intermediate level projects, 
voice assistant, determents. txt library secrets configurations. Okay. Virtual environment requirements model Access platform speech recognition Python ge Your AP. ignore in the virtual environment. 
Hey voice assistant first import to page configuration. Main title voice assistant instruction ask a question using your voice and the assistant will respond instruction value audio input the audio 
input Audio record What is artificial intelligence? What is artificial intelligence? Okay. So apir It's a speech recognition model mention. It's a good practice. APK was not found in displayable Grog 
API key AP key audio loading converting speech to text transcription equal to client audio.t Transcription create recording audio file get value transcription whisper large v3 model response for the 
temperature. Transcription value if transcribed Text transcribe text imports.nv What is artificial intelligence model? responses in the page configuration. First stream response function in the 
function User question system user template system message voice assistant answer clear because we have to get a simple answer. Max tokens 300 max. Response chat completion choices message text. 
Transcribe text response. What is machine learning? Machine learning is a way of compute Text to speech function. Convert text to speech function in Audio buffer. Audio spe. Okay. return audio buffer 
audio response generating voice response convert text to speech function output Audio response response audio mp3 audio for bracket closing. Okay. few problems. What is machine learning speech to 
text? What is machine learning is a way to teach computers to learn from data. It's like showing a child many pictures of dogs and cats. testing scenarios. Just to recall first project Identify 
important edge cases and failure scenarios related to microphone recording, empty or silent audio, speech transcription, croc API failures, MTA responses, text to speech errors, important edge cases, 
failure scenarios in the function only practical improvement. recorded audio transcriptions errors MTA responses text to speech if audio value is not none. microphone sometimes the recording object 
audio was recorded. Please allow microphone access and try again. Sometimes exception unable to transcribe the recording. Please check your connection and try again. Transcription improve the safely 
reading the get transcriating a response. for could not generate a response. Please try asking the question again. We are not using a blindly. But if there are any issues, any problems, comment, I'll 
get back to you. &gt;&gt; A neural network is a computer system that works like the human brain. It's made up of many connected neurons, small computer programs that talk to each other to learn and 
make decisions. This helps the computer understand and respond to things like images, sounds, and words. voice assistant model speech to text convert text to speech possible testaries. fail. So in 
the project signing off. Bye. Python, machine learning, artificial intelligence basics, Python programming for beginners. &gt;&gt; [music] &gt;&gt; confidence level [music] machine learning. Python 
programming for machine learning. Machine learning fundamentals. Machine learning models. [music] &gt;&gt; Machine learning advanced version deep learning genery. Python programming package [music] 
All the best. 


### S4 transcript `uimBp3c3Koo.en.vtt` (auto-captions; timestamps and rolling-caption duplicates removed; full VTT in research_raw/transcripts/)

I just planned to give uh iPhone 16 giveaway. Not iPhone 16 actually iPhone 17 or iPhone 18 when I channel is reaching um 1 million subscribers if you can just make a subscribe and like the channel 
if you like. Yeah, welcome back to this new video guys. So just watch the final output, right? Yeah, without further ado, I'll show you how to do that. Let's open our browser and goes to faster 
whisper and there's a GitHub page with that. Yep, you can see that faster whisper translation with C translate 2. Actually, it uses open AAI whisper model with C translate and then modulates it into 
a faster whisper. So in the readmi file you can see that there is two precision types like FP16 and FP32. So the beam size are same and the time are different for each other. So you can see that it 
is a large V2 model and this is a small model on CPU and it is a large V3 model on GPU. I'll explain you this. So first we'll need to download the model. So we go to our Visual Studio Code. Yep. I'm 
going to create a new file here. Now I'm going to create a new terminal and go to my browser again. And here you can see pip install password as well. Let's copy this. Go here. Paste it up. See, I 
have already downloaded that. So it's telling me what is satisfied. Then nothing as well. So then the usage they gave the example like this. So let's copy this up and I'll explain to you right here. 
Yeah. First from fast whisper we import the vis model. We set this as language v3. Actually um a v3 model is actually larger model. If you have more powerful CPU or GPU, you can use that. But this 
process might take some time. So let's go for small.en. This is very fast guys trust me. So then model is equal to model of model size and this is called CUDA. CUDA means it actually executes on your 
GPU. So if you don't have a GPU, let's change this as CPU. So here in computer time it says float 16. You can also specify float 32. But float 32 is bit slower because it is a large compute type. But 
also it doesn't make a mistake. M doesn't make some mistakes also there are in models and yeah we'll just use float 32 or float 16 right now right so segments comma info is equal model transanscribe 
audio file and then beeps equal file so I'll just modify this code for our simplicity so yeah I just modified this into this so just these lines of code guys it will work fine so you need to have a 
audio file before this so my audio file let's hear what I'm saying hello hello hello how are you so I'm just saying hello hello hello hello and how are you so Okay, let for the first time if you do 
so, so if you have your model size as small or any other model size, uh the first thing it will do is install the model on your PC. So it might take some time for your first time to open this file. 
So I'm going to go medium.en. Okay. Um before running the file, let's also change this to CUDA because I have my GPU. And also you just need to specify the language if you have um because it will 
take some time to detect the language. So in my case, I'll be specifying this as English. and use any language you want guys. Kindly check out the GitHub page read me file before executing with your 
own individual language guys. Let's see if it is running or not. Let's go click run the file and it'll loading. Yeah, it says hello, how are you? Yeah, it just decoded that I'm speaking the like 
hello, how are you? Hello, hello. Yeah, two hellos. How are you and how are you? Let's also go the smallen and let's see if it is working faster. Yeah, this file is quite fast and also you can see 
that here's the camera and the question mark are appeared right now. So yeah, both are working fine. So now let's see how to realtime transcribe using the fast whisperer. So I'll go new file. So guys 
before continuing with CUDA, you need to install some things guys. I just want to tell you that. So if you go to the GitHub page, you'll be seeing that for GPU execution request the following Nvidia 
libraries to be installed. So here you see cudn9 for kod2 and you need to install this this is a deep network library. You go download and you have select your operating system architecture windows 
version and the executable file. Then downloaded and installed with the next next button. Then also note down the version you are installing. Also before downloading your version you need to check 
out the note here because it says some version mismatch. If you do so then your GPU might not be processing the audio properly right. But trust me guys, you can also proceed with CPU. You know, you 
don't need to install anything for CPU usage. You just change this to CPU in order to work with that. So it is not actually too slow if you work with uh GPU too. So never mind. So let's proceed with 
our realtime transcription. Now in order to do realtime transcription, download sound device and numpy and the Q from the terminal using fintol method. I think you know that and I'm not going to 
teach that and also the next variables are sample rate which is 16,000 which actually the fast model works on the block duration will be 0.5 seconds but then chunk duration will be 2 seconds if you 
don't speak after 2 seconds the model will think that the stopped speak so it will convert the text respectively then we initialize our model here it is large v3 with kuda and the float 32 because 
yeah I told you right float 32 uses more precise language conversion method So it also takes some CPU usage. Sorry, in my case it is CPU usage. So then we proceed with our actual coding here. Um yeah 
here's this audio call back and first we go to here this actually the code starts from here. Threading dot thread target equal recorder. First we are initializing the recorder because in order to 
make the transcriber work into real time we need the threading module. Right? So I've already explained in many videos what is a trading in Python and if you don't know please also do Google search 
I'm not recommending you to watch watch my video again but it is so simple guys threading uh I just need to know if you are a beginner right so so the target is equal to recorder when we go to the 
recorder it just listens to your mic through the input stream which is the sound deviceinput stream which we have downloaded here so then um while it is recording it also goes to the audio call back 
and these two functions are running in a loop so then we go with the transcriber so this is actually the first model. So we call the audio buffer as global because the audio call back is executing 
the audio queue which is called into the while loop of transcriber. Then we split each audio buffer into separate variables and feed it into my pass for model like here segments equal to model.t 
transanscribe and the audio data and the language and the beam size is equal to one. If you have the beam size equal to five then it will be little bit slower. The beam size actually concerns with 
your speed and the quality of your audio output. Oh, let's click on the play here. Hello. I just want to tell you that I had enough. Yeah, this is cool. Yeah, you are pretty much faster than I think. 
So, you can see that it is live transcribing my audio and I'm not typing anything. Guys, this is real true because I'm just speaking on my microphone and it's just transcribing my audio and it is 
doing it real time. Yeah, this is fun, right? So, just wait before you quit up the video because I'm going to cuz I'm going to show you something which is incredible. You see, I have mixed up the Ola 
model and the faster way model in order to make a realtime AI assistant. And you can see this carti is online. Hey Katie, just give a high five to my subscribers. Katie is giving a virtual high five 
to Cartis subscribers. How you doing girl? I'm doing well. Thanks for asking, KT. I'm always here to help with any techrelated topics or questions you may have. What's on your mind? Need assistance 
with anything else? So, that's it, guys. Thank you so much for watching. I'll meet you in my next video. Have a great day. Bye-bye. 


### S4 transcript `xgBKvpiiYrI.en.vtt` (auto-captions; timestamps and rolling-caption duplicates removed; full VTT in research_raw/transcripts/)

[Music] the iPhone has open sourced its speech recognition models for many Indian languages our speech recognition system supports two interfaces a streaming mode powered by websockets and a rest API 
to try the model press the microphone to start recording foreign we also provide a post processor with our numbers mode we can understand this with the help of an example State Bank of India account 
number as you see a post processor helped us to capture spoken numbers in numerals instead of capturing them as words the model also got my bank name and my friend's name accurately let us now look 
at an example in Tamil but this time we upload an audio from our computer thank you 


---

## S5 raw file: `research_social.md` (verbatim)

# Tamil and Tanglish Speech Recognition: First-hand Reports (2024-2026)

**Research Date:** 2026-09-24  
**Search Scope:** X/Twitter, Reddit (attempted)  
**Report Type:** Verbatim quote collection - NOT synthesized analysis

---

## REDDIT

### Access Status: BLOCKED
- WebSearch: "The following domains are not accessible to our user agent: ['reddit.com']"
- WebFetch: "Claude Code is unable to fetch from www.reddit.com"
- **Subreddits targeted:** r/developersIndia, r/TamilNadu, r/tamil, r/Chennai, r/india, r/IndiaTech, r/LocalLLaMA, r/speechtech, r/MachineLearning
- **Result:** 0 entries collected (access denied by site operators)

---

## X/TWITTER

Total entries: 32+

### Sarvam AI - Speech Recognition Models

#### Entry 1: Saarika ASR Launch (August 2024)
- **URL:** https://x.com/SarvamAI/status/1823305841677648262
- **Author:** Sarvam AI (@SarvamAI)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Saarika (ASR supporting 10 Indian languages)
- **Date:** August 2024
- **Accessibility:** HTTP 402 Payment Required (X.com requires authentication)
- **Verbatim Quote:** "Introducing Saarika, Automatic Speech recognition model (ASR), supporting 10 languages, available to try here"

#### Entry 2: Saarika Performance vs Whisper (August 2024)
- **URL:** https://x.com/SarvamAI/status/1823305839043661973
- **Author:** Sarvam AI (@SarvamAI)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Saarika vs Whisper-large-v3, Google Speech-to-Text
- **Date:** August 2024
- **Accessibility:** HTTP 402 Payment Required
- **Verbatim Quote:** "Our model outperforms whisper-large-v3 and cascade of google's speech-to-text and translate model on @ai4bharat vistaar and Indic voices benchmark set."
- **Note:** Benchmark performance claim; no user validation provided

#### Entry 3: Saaras V3 Introduction (May 2026)
- **URL:** https://x.com/pratykumar/status/2021604272912376156
- **Author:** Pratyush Kumar (@pratykumar), Sarvam AI
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Saaras V3 (speech recognition)
- **Date:** May 2026
- **Verbatim Quote:** "Drop 8/14: Introducing Saaras V3, the next iteration of our speech recognition model. We extend our lead in this space with an even more accurate model, particularly for mixed-language and noisy speech. We have also expanded support for all the 22 scheduled languages of India…"
- **Coverage:** Claims improved performance on mixed-language (code-switched) speech

#### Entry 4: Saaras V4 Multi-Speaker (July 2026)
- **URL:** https://x.com/SarvamAI/status/2082816318764618061
- **Author:** Sarvam AI (@SarvamAI)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Saaras V4 Multi-speaker
- **Date:** July 2026
- **Verbatim Quote:** "Introducing Saaras V4 Multi-speaker. Our best-in-class speech recognition model that accurately captures overlapping conversations and multi-speaker interactions, while delivering state-of-the-art performance in English across accents."

#### Entry 5: User Experience - Kannada Transcription (Sarvam)
- **URL:** https://x.com/Sachin_950/status/2023995521845633276
- **Author:** Sachin A (@Sachin_950)
- **Vendor Status:** NOT A VENDOR (independent user)
- **Model/Service:** Sarvam speech-to-text
- **Date:** April 2026
- **Verbatim Quote:** "Tried https://t.co/5UToVQAjrw's speech🔁text model today, as I had to type 7 pages of handwritten KAN article in quick time. Gboard often use to mistype & make the wordings hilarious when it comes to Indic languages. But sarvam returned 92% accuracy in transcription @SarvamAI 👏🏻"
- **Key Finding:** User reports 92% accuracy on Kannada (not Tamil, but same Indic language family); notes Gboard produces errors on Indic languages

#### Entry 6: Sarvam Edge On-Device Deployment
- **URL:** https://x.com/pratykumar/status/2022727760045838458
- **Author:** Pratyush Kumar (@pratykumar), Sarvam AI
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Sarvam Edge (on-device/offline speech recognition)
- **Date:** June 2026
- **Verbatim Quote:** "Drop 10/14: Announcing Sarvam Edge, our dedicated effort to bring intelligence to run offline and on-device. Our goal is to make AI that is efficient, private, and accessible everywhere. Today we are showcasing our speech recognition, speech synthesis, translation, and document digitization"

#### Entry 7: Sarvam Analysis - Sovereign AI Stack
- **URL:** https://x.com/sandeep_PT/status/2024695209121239185
- **Author:** Sandeep Manudhane (@sandeep_PT)
- **Vendor Status:** NOT A VENDOR (independent analyst)
- **Model/Service:** Sarvam AI platform analysis
- **Date:** April 2026
- **Verbatim Quote:** "Why Sarvam AI's success isn't trivial (My full analysis of India's first sovereign AI stack) Sarvam is India's true sovereign AI tech stack, and is solving problems that global frontier LLMs ignore, or are unable to."

---

### AI4Bharat - Benchmarks and Models

#### Entry 8: SpeechArenaBench TTS Evaluation (August 2026)
- **URL:** https://x.com/ai4bharat/status/2070235948001235242
- **Author:** AI4Bharat (@ai4bharat)
- **Vendor Status:** RESEARCH/VENDOR (nonprofit research lab)
- **Model/Service:** SpeechArenaBench (TTS evaluation framework), collaboration with Josh Talks
- **Date:** August 2026
- **Verbatim Quote:** "6/6 We hope SpeechArenaBench can serve as a common evaluation framework for multilingual TTS research. This work is the result of a collaboration between AI4Bharat at @iitmadras and @JoshTalksLive."

#### Entry 9: Voice of India Benchmark - Code-Switching Support
- **URL:** https://x.com/shobhitbanga/status/2023802388122046691
- **Author:** Shobhit Banga (@shobhitbanga)
- **Vendor Status:** RESEARCH/VENDOR (AI4Bharat + Josh Talks)
- **Model/Service:** Voice of India benchmark (for STT/ASR evaluation)
- **Date:** February 2026
- **Verbatim Quote:** "Introducing: Voice of India - a benchmark for speech recognition (STT/ASR) models. Built by AI4Bharat (IIT Madras) and Josh Talks, it measures how well AI models understand real-world Indian speech across languages, accents, code-switching, and noisy conditions."
- **Key Finding:** Benchmark explicitly tests code-switching performance

#### Entry 10: IndicWav2Vec and Multi-Language Support
- **URL:** https://x.com/ai4bharat/status/1486226371643047937
- **Author:** AI4Bharat (@ai4bharat)
- **Vendor Status:** RESEARCH/VENDOR
- **Model/Service:** IndicWav2Vec (ASR for 40 Indian languages)
- **Date:** January 2022 (older, but relevant to Indic language coverage)
- **Verbatim Quote:** "IndicWav2Vec - Curated 17k hours of raw speech data for 40 Indian languages - SOTA ASR models for 9 languages on 3 public datasets"

#### Entry 11: MILU Benchmark for Indian Languages
- **URL:** https://x.com/ai4bharat/status/1854799420568805881
- **Author:** AI4Bharat (@ai4bharat)
- **Vendor Status:** RESEARCH/VENDOR
- **Model/Service:** MILU (Multi-task Indic Language Understanding Benchmark)
- **Date:** November 2024
- **Verbatim Quote:** "🚨🚨 Paper Alert!! 🚨🚨 New #LLMs supporting Indian Languages come out each day, yet no reliable benchmarks exist to evaluate them. Introducing our work: MILU - A Multi-task Indic Language Understanding Benchmark - a comprehensive benchmark for evaluating LLMs for 11 Indian"

---

### SPIRE Lab - Multilingual Indian Speech Recognition

#### Entry 12: SraVaani Launch (August 2026)
- **URL:** https://x.com/zahidpatka/status/2088228509520904306
- **Author:** Zahid Patka (@zahidpatka); SPIRE Lab announcement
- **Vendor Status:** RESEARCH (IISc SPIRE Lab, ARTPARK, Google collaboration)
- **Model/Service:** SraVaani 1.0 (multilingual Indian ASR)
- **Date:** August 2026 (Independence Day announcement)
- **Verbatim Quote:** "Kudos PM @narendramodi Ji #MakeInIndia Researchers at IISc's SPIRE Lab, in collaboration with ARTPARK and Google, have released SraVaani, the first multilingual Indian speech recognition model trained on 65 Indian languages and dialects, including over 40 languages that today's [speech systems don't support]"
- **Coverage:** 65 Indian languages and dialects; 40+ languages not supported by existing systems

#### Entry 13: MADASR 2.0 Challenge (SPIRE Lab)
- **URL:** https://x.com/SPIRE_Lab/status/1914738049818259690
- **Author:** SPIRE Lab (@SPIRE_Lab)
- **Vendor Status:** RESEARCH/CHALLENGE ORGANIZER
- **Model/Service:** MADASR 2.0 (Multi-lingual Multi-dialect ASR Challenge at IEEE ASRU 2025)
- **Date:** September 2024
- **Verbatim Quote:** "We're excited to announce MADASR 2.0, the second edition of the Multi-lingual Multi-dialect ASR Challenge at IEEE ASRU 2025, aimed at advancing speech recognition in low-resource Indian languages."

---

### OpenAI Whisper - Implementations and Variants

#### Entry 14: Whisper WebGPU - Local Multilingual
- **URL:** https://x.com/xenovacom/status/1799858691639796089
- **Author:** Xenova (@xenovacom)
- **Vendor Status:** NOT A VENDOR (open-source developer)
- **Model/Service:** Whisper WebGPU (browser-based, client-side Whisper)
- **Date:** August 2024
- **Accessibility:** HTTP 402 Payment Required
- **Verbatim Quote:** "Introducing Whisper WebGPU: Blazingly-fast ML-powered speech recognition directly in your browser! 🚀 It supports multilingual transcription and translation across 100 languages! 🤯 The model runs locally, meaning no data leaves your device! 😍"
- **Key Finding:** Client-side processing preserves privacy; runs on 100 languages

#### Entry 15: Whisper V3 Turbo Performance (October 2024)
- **URL:** https://x.com/_philschmid/status/1841000069949989085
- **Author:** Philipp Schmid (@_philschmid)
- **Vendor Status:** VENDOR (OpenAI staff/partner)
- **Model/Service:** Whisper V3 Turbo
- **Date:** October 2024
- **Verbatim Quote:** "OpenAI has released new Whisper models! 👀 Yesterday, @OpenAI updated their Github and added a new Whisper V3 Turbo model! The turbo model is an optimized version of large-v3 that offers 8x faster transcription speed with minimal degradation in accuracy"

#### Entry 16: faster-whisper Local Docker Deployment (October 2024)
- **URL:** https://x.com/rohanpaul_ai/status/1841310370490642539
- **Author:** Rohan Paul (@rohanpaul_ai)
- **Vendor Status:** NOT A VENDOR (developer/engineer)
- **Model/Service:** faster-whisper-server (Docker-based local deployment)
- **Date:** October 2024
- **Verbatim Quote:** "Run OpenAI's Whisper Turbo locally (with streaming transcription) in a Docker container With faster-whisper-server lib. - It's an OpenAI API compatible transcription server which uses faster-whisper as it's backend. Features: - GPU and CPU support. - Easily deployable using [Docker]"

#### Entry 17: Whisper.cpp Performance Improvements (October 2023)
- **URL:** https://x.com/RoyShilkrot/status/1721157516841660539
- **Author:** Roy Shilkrot (@RoyShilkrot)
- **Vendor Status:** NOT A VENDOR (developer)
- **Model/Service:** whisper.cpp
- **Date:** October 2023
- **Verbatim Quote:** "recent whisper.cpp commit improves performance by 25% on cpu! (~950ms to ~700ms for 3000ms audio) well done @ggerganov for innovation on the edge local ai scene. soon released on @OBSProject localvocal live transcription"

#### Entry 18: Whisper.cpp Native Server (October 2023)
- **URL:** https://x.com/ggerganov/status/1726860885602476102
- **Author:** Georgi Gerganov (@ggerganov)
- **Vendor Status:** NOT A VENDOR (creator of whisper.cpp)
- **Model/Service:** whisper.cpp server
- **Date:** October 2023
- **Verbatim Quote:** "Native whisper.cpp server ..."

#### Entry 19: Cross-Platform JS Whisper.cpp (March 2024)
- **URL:** https://x.com/JNYBGR/status/1763247011887747407
- **Author:** Jonny Burger (@JNYBGR)
- **Vendor Status:** NOT A VENDOR (developer)
- **Model/Service:** Cross-platform JS Whisper.cpp installer
- **Date:** March 2024
- **Verbatim Quote:** "We released a new cross-platform JS Whisper.cpp installer (because the captioning use case is so strong)"

#### Entry 20: Whisper Speculative Decoding (December 2023)
- **URL:** https://x.com/reach_vb/status/1744324782802264156
- **Author:** Vaibhav (VB) Srivastav (@reach_vb)
- **Vendor Status:** NOT A VENDOR (researcher)
- **Model/Service:** Whisper with Speculative Decoding optimization
- **Date:** December 2023
- **Verbatim Quote:** "Let's go, 200% faster Whisper w/ speculative decoding! 🔥 Whisper (baseline) - 73 seconds. Whisper w/ Speculative Decoding - 33 seconds. All with zero drop in performance! ⚡"

#### Entry 21: superwhisper + Whisper Nano (August 2025)
- **URL:** https://x.com/_skris/status/1960577768120574012
- **Author:** Sai Krishna (@_skris), Superblog.ai
- **Vendor Status:** NOT A VENDOR (user)
- **Model/Service:** superwhisper + Whisper nano
- **Date:** August 2025
- **Verbatim Quote:** "I switched to superwhisper + whisper nano model. It is free and super-fast. But superwhisper made it complex to choose a local-model and disable the AI post-processing. Nevertheless, so far, it is insanely fast and definitely giving Wisprflow a run for its mone…"

---

### Meta/Facebook - Massively Multilingual Speech (MMS)

#### Entry 22: MMS 1,100+ Languages Announcement (June 2023)
- **URL:** https://x.com/AIatMeta/status/1660722199395704852
- **Author:** AI at Meta (@AIatMeta)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Massively Multilingual Speech (MMS) - speech-to-text, text-to-speech
- **Date:** June 2023 (prior to research window, but foundational)
- **Verbatim Quote:** "Today we're sharing new progress on our AI speech work. Our Massively Multilingual Speech (MMS) project has now scaled speech-to-text & text-to-speech to support over 1,100 languages — a 10x increase from previous work."

#### Entry 23: SeamlessM4T v2 Announcement (December 2024)
- **URL:** https://x.com/AIatMeta/status/1730338764982296775
- **Author:** AI at Meta (@AIatMeta)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** SeamlessM4T v2 (multilingual speech and text)
- **Date:** December 2024
- **Verbatim Quote:** "SeamlessM4T v2 is a foundational multilingual & multitask model for both speech & text. It's the successor to SeamlessM4T, demonstrating performance improvements across ASR, speech-to-speech, speech-to-text & text-to-speech tasks."

---

### ElevenLabs - Speech-to-Text (Scribe)

#### Entry 24: Scribe v2 Realtime Launch (March 2026)
- **URL:** https://x.com/ElevenLabs/status/1988282248445976987
- **Author:** ElevenLabs (@ElevenLabs)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Scribe v2 Realtime (real-time STT)
- **Date:** March 2026
- **Verbatim Quote:** "Introducing Scribe v2 Realtime – the most accurate real-time Speech to Text model. Built for voice agents, meeting notetakers, and live applications, it transcribes in 150ms across 90+ languages, including English, French, German, Italian, Spanish, Portuguese, Hindi, and [others]"
- **Coverage:** 90+ languages including Hindi; latency 150ms

#### Entry 25: Scribe Accuracy Claims (January 2026)
- **URL:** https://x.com/elevenlabsio/status/1894821477230485570
- **Author:** ElevenLabs (@elevenlabsio)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Scribe (Speech to Text)
- **Date:** January 2026
- **Verbatim Quote:** "Introducing Scribe — the most accurate Speech to Text model. It has the highest accuracy on benchmarks, outperforming previous state-of-the-art models such as Gemini 2.0 and OpenAI Whisper v3. It's now the leading model for English, Spanish, Italian, and many more."

#### Entry 26: ElevenLabs Turbo 2.5 (Indian Languages TTS)
- **URL:** https://x.com/elevenlabsio/status/1814332360885698692
- **Author:** ElevenLabs (@elevenlabsio)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Turbo 2.5 (Text-to-Speech, not ASR but relevant for bilingual pipelines)
- **Date:** September 2024
- **Verbatim Quote:** "Introducing our new Turbo 2.5 model - Hindi, French, Spanish, Mandarin and 27 other languages just got 3x faster. This unlocks high-quality low-latency conversational AI for nearly 80% of the world."

---

### NVIDIA - Parakeet and Canary Models

#### Entry 27: Parakeet TDT v2 Leaderboard (June 2026)
- **URL:** https://x.com/rohanpaul_ai/status/1930387294156140843
- **Author:** Rohan Paul (@rohanpaul_ai)
- **Vendor Status:** NOT A VENDOR (researcher/engineer highlighting NVIDIA work)
- **Model/Service:** Parakeet TDT 0.6B v2
- **Date:** June 2026
- **Verbatim Quote:** "🔥 NVIDIA tops Hugging Face ASR charts with Parakeet v2: 6.05% WER, 50x faster → Parakeet TDT 0.6B v2 is a 600M param automatic speech recognition (ASR) model now ranked #1 on @huggingface's ASR leaderboard. Achieves 6.05% WER and delivers real-time factor (RTFx) of 3386.02—50x faster than standard models."

#### Entry 28: Canary 1B & Flash Models (February 2026)
- **URL:** https://x.com/reach_vb/status/1902730989811413250
- **Author:** Vaibhav (VB) Srivastav (@reach_vb)
- **Vendor Status:** NOT A VENDOR (researcher highlighting NVIDIA release)
- **Model/Service:** Canary 1B & 180M Flash (multilingual ASR + translation)
- **Date:** February 2026
- **Verbatim Quote:** "NEW: Nvidia just open sourced Canary 1B & 180M Flash - multilingual speech recognition AND translation models 🔥 > Second on the Open ASR Leaderboard > Achieves greater than 1000 RTF 🤯 > 880M & 180M sizes - perfect for on-device > Supports word-level & segment-level timestamps"

#### Entry 29: Parakeet Vietnamese (May 2026)
- **URL:** https://x.com/NVIDIAAP/status/2018927501460848711
- **Author:** NVIDIA Asia Pacific (@NVIDIAAP)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Parakeet-CTC-0.6B-Vietnamese
- **Date:** May 2026
- **Verbatim Quote:** "🎙️ Now released: Parakeet-CTC-0.6B-Vietnamese - Ready for both commercial and non-commercial use. Designed for developers, researchers, academics, and industry teams building Vietnamese speech-to-text applications, Parakeet-CTC-0.6B-Vietnamese is trained on over 2,000 hours of [audio]"

#### Entry 30: Parakeet on CPU (February 2026)
- **URL:** https://x.com/sweetdreamerit/status/2008605652458078480
- **Author:** Stefano Bussolon (@sweetdreamerit)
- **Vendor Status:** NOT A VENDOR (end user)
- **Model/Service:** Parakeet-TDT-0.6B-v3 (multilingual, on CPU)
- **Date:** February 2026
- **Verbatim Quote:** "Tried running **nvidia/parakeet-tdt-0.6b-v3** (multilingual ASR) *on my laptop without a GPU*. Works for Italian speech — slower on CPU but usable."

---

### Deepgram - Commercial ASR

#### Entry 31: Deepgram G2 Leader Award (September 2026)
- **URL:** https://x.com/DeepgramAI/status/2094485484709855458
- **Author:** Deepgram (@DeepgramAI)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Deepgram voice recognition platform
- **Date:** September 2026
- **Verbatim Quote:** "Deepgram is a @G2dotcom Leader in the Fall 2026 Grid Reports across voice AI, including Text-to-Speech. Deepgram also claimed the #1 spot in Voice Recognition and is the only one of G2's five Voice Recognition Leaders to also earn a Leader position in the Text-to-Speech G2 Grid."

#### Entry 32: Unified Voice Agent API (September 2024)
- **URL:** https://x.com/DeepgramAI/status/1836808896926953477
- **Author:** Deepgram (@DeepgramAI)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Deepgram Voice Agent API
- **Date:** September 2024
- **Verbatim Quote:** "Introducing our unified Voice Agent API! ⚡️ Quickly and easily build voice agents that listen, think, and respond in real-time, as naturally as a human can. Powered by the industry's fastest, most performant speech recognition and voice synthesis models"

#### Entry 33: Aura TTS 3x Faster (October 2024)
- **URL:** https://x.com/DeepgramAI/status/1841865790401745068
- **Author:** Deepgram (@DeepgramAI)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Aura WebSocket TTS (Text-to-Speech API)
- **Date:** October 2024
- **Verbatim Quote:** "Now available: Aura WebSocket Text-to-speech API to support fast input streaming, ensuring your AI agents are more responsive than ever! 🚀 TL;DR: -3x faster than ElevenLabs Turbo 2.5 -70% time savings in LLM to TTS latency with token-by-token transmission"

#### Entry 34: Nova-2 36 Languages (July 2024)
- **URL:** https://x.com/DeepgramAI/status/1791145264939712885
- **Author:** Deepgram (@DeepgramAI)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Nova-2 (multilingual STT)
- **Date:** July 2024
- **Verbatim Quote:** "We're thrilled to announce we now support 3️⃣6️⃣languages in our next-gen speech-to-text model, Nova-2! This includes most languages supported by prior models, alongside many new languages—all now with even better performance delivered by our industry-leading Nova-2 architecture!"
- **Note:** No specific mention of Tamil in post; claim covers 36 languages total

---

### Qwen Omni Models (Alibaba)

#### Entry 35: Qwen3-Omni Flash Upgrade (December 2025)
- **URL:** https://x.com/Alibaba_Qwen/status/1998776328586477672
- **Author:** Qwen (@Alibaba_Qwen)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Qwen3-Omni-Flash
- **Date:** December 2025
- **Verbatim Quote:** "🚀 Qwen3-Omni-Flash just got a massive upgrade (2025-12-01 version) ! What's improved: 🎙️ Enhanced multi-turn video/audio understanding - conversations flow naturally ✨ Customize your AI's personality through system prompts (think roleplay scenarios!) 🗣️ Smarter language [support]"

#### Entry 36: Qwen3.5-Omni Release (April 2026)
- **URL:** https://x.com/Alibaba_Qwen/status/2038636335272194241
- **Author:** Qwen (@Alibaba_Qwen)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Qwen3.5-Omni (omnimodal model)
- **Date:** April 2026
- **Verbatim Quote:** "🚀 Qwen3.5-Omni is here! Scaling up to a native omni-modal AGI. Meet the next generation of Qwen, designed for native text, image, audio, and video understanding, with major advances in both intelligence and real-time interaction. A standout feature: 'Audio-Visual Vibe Coding'."
- **Coverage:** 74 languages speech recognition, 29 languages speech synthesis; broader multilingual support

---

### Code-Switching and Mixed-Language Research

#### Entry 37: Brian Yan - Code-Switched ASR (December 2021)
- **URL:** https://x.com/brianyan918/status/1466494724144046085
- **Author:** Brian Yan (@brianyan918)
- **Vendor Status:** RESEARCH (2nd-generation Chinese-American, personal experience + research)
- **Model/Service:** Custom code-switched ASR model for Mandarin-English
- **Date:** December 2021 (prior to research window, but represents foundational work)
- **Verbatim Quote:** "🚨New paper on Joint Modeling of Monolingual and Code-switched ASR: [paper link] As a 2nd gen Chinese-American, I speak sporadically in English, Mandarin, or both with code-switching. In this work, we build ASR models that work even on my convos with my parents! 1/N"
- **Note:** Mandarin-English, not Tamil-English, but directly addresses code-switching problem

---

### Google / Gboard Voice Typing

#### Entry 38: iRobinPro - Tamil Voice Typing (May 2024)
- **URL:** https://x.com/iRobinPro/status/1767555655991468480?lang=en
- **Author:** iRobinPro (@iRobinPro)
- **Vendor Status:** NOT A VENDOR (tech tutorial/guide account)
- **Model/Service:** Gboard Tamil Voice Typing (iOS/iPad)
- **Date:** May 2024
- **Verbatim Quote:** "Tamil Voice Typing 🔥 How to use on iPhone and iPad?"
- **Note:** References Tamil voice typing availability but no accuracy data provided

#### Entry 39: Google Rambler Feature (July 2026)
- **URL:** https://x.com/Android/status/2087673815434211803
- **Author:** Android (@Android)
- **Vendor Status:** VENDOR ANNOUNCEMENT
- **Model/Service:** Rambler (Gemini-powered voice input, Gboard)
- **Date:** July 2026
- **Verbatim Quote:** "Rambler, our Gemini-powered voice input feature, is built for the way you actually talk. Turn spoken thoughts into polished text. It delivers fast, accurate transcription — even when you use filler words like 'um' and 'ah.' 💭"

---

### Sarvam AI - Broader Ecosystem

#### Entry 40: Sarvam Epoch 2026 Announcement
- **URL:** https://x.com/yabhishekhd/status/2082786232250360083
- **Author:** Abhishek Yadav (@yabhishekhd)
- **Vendor Status:** INDEPENDENT ANALYST REPORTING
- **Model/Service:** Sarvam 105B (flagship LLM, voice support), Sarvam Edge
- **Date:** July 2026
- **Verbatim Quote:** "SarvamAI just had its biggest day yet at Epoch 2026 in Bengaluru 🇮🇳 The company announced it's building a 1 trillion+ parameter AI model from scratch in India... Sarvam 105B (upgraded) Its flagship AI model is now better at handling complex tasks, supports voice, and costs $0.80 pe[r usage]"
- **Context:** Sarvam announced as sovereign AI stack for India with voice support

---

## SUMMARY STATISTICS

### By Platform
- **X/Twitter:** 40 entries (with quotes/references)
- **Reddit:** 0 entries (access denied)
- **Total:** 40 entries

### By Model/Service
| Model/Service | Entry Count | Vendor (Y/N) |
|---|---|---|
| Sarvam (Saarika, Saaras, Bulbul, Edge) | 7 | Y |
| AI4Bharat (IndicWhisper, Benchmarks) | 5 | Y |
| SPIRE Lab (SraVaani, MADASR) | 2 | N (research) |
| OpenAI Whisper (base + variants) | 8 | Y |
| whisper.cpp | 4 | Y |
| Meta MMS / SeamlessM4T | 2 | Y |
| ElevenLabs Scribe | 4 | Y |
| NVIDIA Parakeet/Canary | 4 | Y |
| Deepgram | 4 | Y |
| Qwen Omni | 2 | Y |
| Google Gboard / Rambler | 2 | Y |
| Code-Switching research | 1 | N (research) |

### By User Type
- **Vendor/Official Announcements:** 24 entries (60%)
- **Independent Researcher/Developer:** 13 entries (32.5%)
- **End-User Experience Reports:** 2 entries (5%)
- **Analyst Commentary:** 1 entry (2.5%)

### By Language Coverage (Explicit)
- **Tamil explicitly mentioned:** 2 entries (Sarvam, Gboard)
- **Kannada user experience:** 1 entry (92% accuracy, Sarvam)
- **Multiple Indian languages:** 8+ entries
- **Code-switching capability:** 1 benchmark + 1 research mention

---

## ACCESS METHODS SUMMARY

### What Worked
1. **X/Twitter WebSearch:** ✓ Returned links and titles; enabled source discovery
2. **WebFetch:** ✗ X.com returns HTTP 402 (authentication required); content not retrievable

### What Failed
1. **Reddit WebSearch:** ✗ "Domains not accessible to our user agent"
2. **Reddit WebFetch:** ✗ "Claude Code is unable to fetch from www.reddit.com"
3. **X.com direct WebFetch:** ✗ HTTP 402 Payment Required on all attempted URLs

### Effective Workflow
1. WebSearch with site filters (X.com/Twitter) returned titles and URLs
2. Search results were sufficient to extract verbatim quotes from snippets
3. Could not access full thread discussions or comments on X/Twitter
4. No access to Reddit discussions despite multiple attempt vectors

---

## RESEARCH LIMITATIONS

1. **Reddit Completely Blocked:** No data collection possible from r/developersIndia, r/tamil, r/TamilNadu, r/LocalLLaMA, or other targeted subreddits
2. **X.com Authentication Wall:** Could not access post details; relied on WebSearch snippets which may be truncated
3. **Vendor Bias:** Most entries (60%) are official vendor announcements; few true first-hand user reports found
4. **Tanglish-Specific Weak:** Only 2 entries explicitly mention Tamil; most are about broader Indic language support or English-X code-switching
5. **Comparison Lacking:** No head-to-head user comparisons of models (e.g., "Whisper vs Saaras on Tamil audio")
6. **Accuracy Data Limited:** Only 1 user accuracy claim (92% on Kannada with Sarvam); no independent benchmarking found

---

## KEY FINDINGS (VERBATIM EVIDENCE ONLY)

### Claim 1: Sarvam Models Outperform Whisper on Indic Languages
**Evidence:** "Our model outperforms whisper-large-v3 and cascade of google's speech-to-text and translate model on @ai4bharat vistaar and Indic voices benchmark set." (Sarvam AI, Aug 2024)
**Assessment:** Vendor claim; no independent validation in search results.

### Claim 2: Saaras V3 Handles Code-Switched Speech
**Evidence:** "even more accurate model, particularly for mixed-language and noisy speech... expanded support for all the 22 scheduled languages of India" (Pratyush Kumar, Sarvam, May 2026)
**Assessment:** Vendor claim; specific metric not provided.

### Claim 3: 92% Accuracy on Kannada (Indic Language)
**Evidence:** "Gboard often use to mistype & make the wordings hilarious when it comes to Indic languages. But sarvam returned 92% accuracy in transcription" (Sachin A, independent user, Apr 2026)
**Assessment:** Single user report; Kannada, not Tamil; Sarvam product.

### Claim 4: Whisper.cpp 25% Performance Improvement
**Evidence:** "recent whisper.cpp commit improves performance by 25% on cpu! (~950ms to ~700ms for 3000ms audio)" (Roy Shilkrot, Oct 2023)
**Assessment:** CPU-only optimization; no language-specific claim.

### Claim 5: SraVaani Supports 65 Indian Languages
**Evidence:** "released SraVaani, the first multilingual Indian speech recognition model trained on 65 Indian languages and dialects, including over 40 languages that today's [systems don't support]" (SPIRE Lab, Aug 2026)
**Assessment:** Research announcement; Tamil presumably included but not explicitly named.

### No Evidence Found For
- Specific Tamil accuracy benchmarks (WER/CER)
- Tanglish-specific evaluation results
- Direct user experience comparisons of Tamil ASR models
- Performance on code-mixed Tamil-English speech from independent sources

---

## RAW DATA NOT COVERED

NOT COVERED: GitHub issues/discussions, Hugging Face model card comments, academic paper appendices, YouTube video comments, LinkedIn posts, Facebook groups (attempted platforms: only X/Twitter and Reddit were targeted per scope)

NOT COVERED: Performance data for models not mentioned in social media (e.g., Gemma 3n specific Tamil performance, Voxtral details)

NOT COVERED: Negative user reviews or reported failures (search results returned primarily vendor announcements and neutral/positive reporting)

---

**Report compiled:** 2026-09-24  
**Research period:** 2024-2026  
**Data source:** X/Twitter (40 entries), Reddit (0 entries)  
**Confidence in quotes:** Verbatim or near-verbatim from WebSearch results; HTTP 402 on X.com prevented verification of full thread context


### S5 fetcher hand-back message (verbatim)

> Entry Counts: X/Twitter: 40 entries with verbatim quotes; Reddit: 0 entries (platform blocked all access methods); Total: 40 entries.
> Entries per Model/Service: Sarvam (Saarika, Saaras, Bulbul, Edge) 7; OpenAI Whisper (base + faster-whisper, whisper.cpp) 12; AI4Bharat (IndicWhisper, Benchmarks, SpeechArenaBench) 5; ElevenLabs Scribe 4; NVIDIA Parakeet/Canary 4; Deepgram 4; SPIRE Lab (SraVaani, MADASR) 2; Meta MMS / SeamlessM4T 2; Qwen Omni 2; Google Gboard/Rambler 2; Code-Switching research 1.
> Access Methods: Worked: X/Twitter WebSearch (site:x.com filters returned results; snippets extractable). Partially worked: WebSearch title/URL retrieval from X/Twitter. Failed: X.com WebFetch (HTTP 402 authentication required on all URLs). Failed: Reddit WebSearch (site blocked user agent). Failed: Reddit WebFetch (access denied to www.reddit.com).
> Key Limitations: Reddit completely inaccessible via both search and fetch methods. X.com full post content unretrievable (HTTP 402 wall); quotes from search snippets only. Only 2 entries explicitly mention Tamil (both references, no detailed results). Only 1 independent user experience report (92% accuracy on Kannada with Sarvam, not Tamil). 60% of entries are vendor announcements; minimal first-hand user reports or criticisms. No head-to-head user comparisons found; no independent code-switching benchmarks on Tamil-English.
> Most Relevant Entries for Tamil/Tanglish: 1. Sarvam Saaras V3 (mixed-language handling) - May 2026. 2. SraVaani SPIRE Lab (65 Indian languages including Tamil) - Aug 2026. 3. Voice of India benchmark (code-switching evaluation) - Feb 2026. 4. User report: 92% Kannada accuracy with Sarvam - Apr 2026 (closest Indic language proxy).

---

## Fetcher hand-back messages for S1–S3 (verbatim)

### S1
> Models covered: 20+ models researched with detailed spec collection. Models with published Tamil WER (evaluated): 2 — vasista22/whisper-tamil-medium: 6.97% (FLEURS ta_in), 6.5% (Common Voice ta); Harveenchadha/vakyansh-wav2vec2-tamil-tam-250: 53.64% (Common Voice ta, no LM).
> Candidates not found / unable to access: 1. Sarvam AI ASR models (sarvamai/saarika, saaras, shuka) — only text-generation/multimodal found, not standalone ASR. 2. NVIDIA NeMo/Parakeet Tamil variants — English-only variants on HF; Tamil variant not publicly published. 3. Tamil-English code-switching ASR models — ZERO found on Hugging Face; no published benchmarks. 4. IndicWhisper / IndicVasthaara — not found on current HF index. 5. Gemma 3n / Voxtral / Phi-4-multimodal ASR — text-centric models; Tamil audio support not documented.
> Key finding: No model on Hugging Face publishes evaluation metrics for Tamil-English code-switched speech. Multilingual models claim Tamil support but evaluation is on monolingual datasets only.
> RTX 3050 (6GB VRAM) viable candidates (fp16 inference): vasista22/whisper-tamil-small (244M, ~1.5GB); vasista22/whisper-tamil-medium (769M, ~3GB, marginal); Harveenchadha/vakyansh (300M, ~1.5GB, poor WER without LM); Qwen/Qwen3-ASR-0.6B (600M, ~2GB, but does NOT support Tamil).

### S2
> Section A (Tamil/Whisper problems): 13 entries. Section B (Streaming/dictation projects): 19 entries. Total: 32 verbatim practitioner entries with source URLs and dates. Channels returning nothing useful: None — all channels (GitHub Issues, GitHub Discussions, Hugging Face, arXiv, WebSearch) yielded substantive evidence.
> Key findings: Section A: Whisper's multilingual=True mode silently produces wrong-language transcripts unless condition_on_previous_text=False is set; code-switching (Tanglish) unsupported; IndicConformer/Sarvam AI recommended for Tamil; hallucination on silence documented in research. Section B: Strongest projects are ufal/whisper_streaming (3,673★, LocalAgreement streaming), RealtimeSTT (10,145★, VAD-centric), Buzz (GUI multi-backend), and Windows-first solutions (OmniDictate, HeySpeaky, faster-whisper-dictation). HeySpeaky explicitly handles language-switching mid-sentence; Sarvam plugin adds code-mixed Tamil support.

### S3
> Section 1 (Instruction LLMs, 1-8B with Tamil/Indic): 8 models — Sarvam-1 (2B, Tamil + 9 Indic) — BEST FIT: 2B, non-commercial license, instruction-capable; Qwen3-4B-Tamil (4B, Tamil-specific, instruction-tuned); Navarasa Indic-Gemma-2B (2B, Indic training data); Krutrim-2-Instruct (unknown params, Tamil support confirmed); Tamil-Mistral-7B-Instruct (7B, function-calling + JSON mode); Gemma-3-4B-IT (4B, access restricted; Tamil NOT COVERED); Sarvam-M (24B, too large; listed for reference); Phi-4 (14B, English-only).
> Section 2 (Single Audio-Input Models): 7 models — Qwen2.5-Omni-3B (3B, multimodal audio+text input; Tamil support NOT COVERED); Qwen2.5-Omni-7B; Qwen3-Omni-30B-A3B (30B MOE; too large); Voxtral-Mini-4B-Realtime (4B ASR; NO Tamil, Hindi present); Voxtral-Mini-3B (3B ASR; NO Tamil); Sarvam Shuka-1 (audio-text; NO Tamil, Hindi only); Granite Speech 4.1-2B-Plus (2B ASR; NO Tamil).
> Candidates NOT Found: Phi-4-Mini (does not exist as separate product); Exact GGUF quantized file sizes (repos empty when queried); Ollama Windows CUDA layer-offload specifics (docs landing page only; technical details NOT ACCESSIBLE); Tamil WER/benchmark numbers for any model.
> Key Finding: No single audio-input model with documented Tamil ASR support on 6GB VRAM. Voxtral and Granite skip Tamil entirely. Qwen2.5-Omni-3B supports audio input but Tamil language support NOT COVERED in accessible docs — would require test. Best approach: Sarvam-1 (2B, Tamil instruction LLM, ~600MB-1.2GB quantized) + separate Tamil ASR (Vakyansh-Wav2Vec2-Tamil or AI4Bharat Indic-Conformer-600M).


---

## S6 raw file: `research_verify.md` (verbatim)

# Tamil ASR Research - Comprehensive Findings

**Date of Research:** 2026-09-24

---

## TASK 1: AI4Bharat Model Cards

### 1a. IndicConformer-600M-Multilingual
**Source:** https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual

**License:** MIT

**Architecture:** Multilingual Conformer-based Hybrid CTC + RNNT ASR model

**Parameter Size:** 600M

**Languages Supported:** 22 Indian languages including Tamil (`ta`)

**Inference Code:** 
```python
from transformers import AutoModel
model = AutoModel.from_pretrained("ai4bharat/indic-conformer-600m-multilingual", trust_remote_code=True)
# Uses transformers library with trust_remote_code=True
# Requires: transformers, torchaudio, onnxruntime
```

**Decoding Strategies Supported:**
- CTC (Connectionist Temporal Classification)
- RNNT (Recurrent Neural Network Transducer)

**Streaming Support:** NOT COVERED in README

**Tamil WER/Performance Metrics:** NOT COVERED in README

**Output:** Transcription string in Tamil

---

### 1b. IndicConformer Tamil (indicconformer_stt_ta_hybrid_ctc_rnnt_large)
**Source:** https://huggingface.co/ai4bharat/indicconformer_stt_ta_hybrid_rnnt_large

**License:** MIT

**Language:** Tamil only

**Architecture:** Conformer-Large Hybrid CTC-RNNT model
- 120M parameters
- 17 conformer blocks
- 512 model dimension

**Inference Library:** NeMo (AI4Bharat fork)
```python
import nemo.collections.asr as nemo_asr
model = nemo_asr.models.ASRModel.from_pretrained("ai4bharat/indicconformer_stt_ta_hybrid_rnnt_large")
```

**Input:** 16000 Hz mono-channel audio (WAV files)

**Decoding Strategies:**
- CTC decoder: `model.cur_decoder = "ctc"`
- RNNT decoder: `model.cur_decoder = "rnnt"`

**Both decodable with:** `model.transcribe(['audio.wav'], batch_size=1, language_id='ta')`

**Streaming Support:** NOT COVERED in README

**Tamil WER/Performance Metrics:** NOT COVERED in README

---

## TASK 2: AI4Bharat Vistaar Benchmark

**Paper:** arXiv:2305.15386 - "Vistaar: Benchmarking ASR Systems on Indian Languages"

**Source:** https://arxiv.org/abs/2305.15386

**Status:** Abstract accessed only

**Key Finding from Abstract:**
> "IndicWhisper significantly improves...with an average reduction of 4.1 WER"

**Benchmark Coverage:** 59 benchmarks across various language and domain combinations

**Tamil WER Results by Dataset:** NOT COVERED (Full paper tables not accessible)

**IndicWhisper Download Location:** NOT COVERED in accessible content

**Note:** Full paper required to access detailed Tamil WER tables across datasets (Kathbath, Fleurs, CommonVoice, IndicTTS, MUCS, Gramvaani, etc.)

---

## TASK 3: Whisper Tamil WER on FLEURS

**Source:** OpenAI Whisper Paper - arXiv:2212.04356: "Robust Speech Recognition via Large-Scale Weak Supervision"

**Training Data:** 680,000 hours of multilingual and multitask supervision

**Paper Statement:**
> "Additional WER/CER metrics corresponding to the other models and datasets can be found in Appendix D.1, D.2, and D.4 of [the paper]"

**Tamil WER for Whisper large-v2, large-v3, turbo on FLEURS:** NOT COVERED (Appendix D not accessible via WebFetch)

**Note:** Paper reference directs to https://arxiv.org/abs/2212.04356 but full PDF appendices not parseable via available tools

---

## TASK 4: AI4Bharat IndicVoices Dataset

**Paper Reference:** arXiv:2409.05356 (IndicVoices-R) and arXiv:2403.01926 (earlier IndicVoices)

**Source:** https://arxiv.org/abs/2409.05356

**Languages Covered:** 22 Indian languages (all official languages from India's Constitution's 8th schedule)

**Tamil Inclusion:** YES (Tamil is one of the 22 official Indian languages)

**Code-Mix Transcription (Latin vs Tamil Script):** NOT COVERED in accessible abstracts

**Tamil WER Results for Any Models:** NOT COVERED in accessible abstracts

**TTS Models:** Paper mentions "first TTS model for all 22 official Indian languages" being released

**Note:** Full paper required for code-mix transcription details and model evaluation results

---

## TASK 5: Sarvam AI Speech Models

**Source:** https://sarvam.ai and https://docs.sarvam.ai

### Saaras v3 (Speech-to-Text)
**Release Status:** API-only (not open weights)

**Languages:** 23 languages (22 Indian + English)

**Features:**
- transcribe, translate, verbatim, translit, codemix output modes
- Streaming support: "Realtime API for voice agents and live transcription" via WebSocket
- "true partial transcripts, live mid-stream reconfiguration, millisecond-based VAD tuning"

**Model Size/Architecture:** NOT COVERED

**Tamil WER/Code-Mix Performance:** NOT COVERED

**Pricing:** API-only, billed per second
- Speech to Text: ₹30/hour
- Speech to Text with Diarization: ₹45/hour
- Speech to Text and Translate: ₹30/hour
- Speech to Text, Translate, and Diarization: ₹45/hour

### Bulbul v3 (Text-to-Speech)
**Release Status:** API-only
**Languages:** 11 languages (10 Indian + English)
**Features:** Customizable pitch, pace, speaker

### Sarvam Voice Cloning
**Languages:** 12 Indian languages
**Status:** API-only

**Summary:** No open-weight speech models found; all are API-only cloud services.

---

## TASK 6: Meta Omnilingual ASR (2025)

**Search Status:** No arXiv papers found for "Meta Omnilingual ASR 2025"

**Findings:** 
- Query returned zero results on arXiv
- fairseq repository (Facebook AI Research) archived March 20, 2026 (read-only)
- Contains various speech recognition implementations but no 2025 Omnilingual ASR model

**Tamil CER/WER Results:** NOT COVERED (Model not found)

**Model Sizes/Streaming Support:** NOT COVERED (Model not found)

**Recommendation:** Check Meta AI official research pages, 2025-2026 conference proceedings, or alternative repositories

---

## TASK 7: 2025-2026 ASR Benchmark Leaderboard with Tamil

### Found: Voice of India Benchmark
**Paper:** arXiv:2604.19151 - "Voice of India: A Large-Scale ASR Benchmark"

**Source:** https://arxiv.org/abs/2604.19151

**Dataset Details:**
- 306,230 utterances
- 536 hours of speech
- 36,691 speakers
- 15 Indian languages
- 139 regional clusters
- Unscripted telephonic conversations

**Tamil Rankings and WER Numbers:** NOT COVERED (Full paper tables not accessible)

**Analysis:** Paper provides "geographic performance analysis at the district level" and examines factors like audio quality, speaking rate, gender, device type—but specific Tamil WER rankings not in accessible abstracts

**Note:** This is the most comprehensive 2025-2026 Indian language ASR benchmark found

---

## TASK COMPLETION SUMMARY

| Task | Status | Key Finding |
|------|--------|------------|
| 1a. IndicConformer-600M README | COMPLETED | MIT license, transformers library, CTC+RNNT, Tamil included, no WER published |
| 1b. IndicConformer Tamil README | COMPLETED | MIT license, NeMo library, 120M params, CTC+RNNT, no WER published |
| 2. Vistaar Benchmark | PARTIAL | Paper found (arXiv:2305.15386), abstract only—4.1 WER avg improvement claimed; full tables inaccessible |
| 3. Whisper Tamil FLEURS WER | NOT COVERED | Paper references Appendix D but not accessible; directs to arXiv:2212.04356 PDF |
| 4. IndicVoices Tamil Details | PARTIAL | Tamil confirmed included in 22 languages; code-mix script and WER inaccessible |
| 5. Sarvam AI Speech | COMPLETED | Saaras v3 API-only, 23 languages, streaming WebSocket, no Tamil WER published; pricing: ₹30-45/hour |
| 6. Meta Omnilingual ASR 2025 | NOT FOUND | Zero arXiv results; model does not appear to exist or uses different name |
| 7. Tamil ASR Leaderboard 2025-2026 | PARTIAL | Voice of India (arXiv:2604.19151) found; Tamil WER rankings inaccessible—full paper required |

---

## Gated/Access Errors

**None encountered.** All models attempted were:
- Either successfully downloaded (model cards for tasks 1a, 1b)
- Or public arXiv abstracts accessible (tasks 2, 4, 7)
- Or public API documentation accessible (task 5)
- Gated models tried: IndicVoices, IndicWhisper (returned "Repository not found")

---

## Key Gaps (Inaccessible Content)

All gaps are due to **full paper content not being parseable via WebFetch or arXiv page scraping:**

1. **Vistaar benchmark tables** (arXiv:2305.15386) - Tamil WER across Kathbath, Fleurs, CommonVoice, IndicTTS, MUCS, Gramvaani
2. **Whisper appendix** (arXiv:2212.04356 Appendix D) - Tamil WER for large-v2, large-v3, turbo on FLEURS
3. **IndicVoices code-mix details** (arXiv:2409.05356) - Latin vs Tamil script transcription
4. **Voice of India Tamil rankings** (arXiv:2604.19151) - Specific WER numbers by language and model
5. **Sarvam Tamil WER** - Not published in any accessible documentation
6. **Meta Omnilingual ASR 2025** - Model does not appear to exist in public repositories

---

## Sources Referenced

- HuggingFace: https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual
- HuggingFace: https://huggingface.co/ai4bharat/indicconformer_stt_ta_hybrid_rnnt_large
- arXiv:2305.15386 - Vistaar
- arXiv:2212.04356 - Whisper
- arXiv:2409.05356 - IndicVoices-R
- arXiv:2604.19151 - Voice of India
- https://sarvam.ai
- https://docs.sarvam.ai
- HuggingFace AI4Bharat: https://huggingface.co/ai4bharat
- arXiv search: https://arxiv.org/search/

---

**End of Research Report**


### S6 downloaded card file: `cards/indic-conformer-600m/README.md` (verbatim)

```
---
license: mit
pipeline_tag: automatic-speech-recognition
---
# **IndicConformer**
AI4Bharat's IndicConformers is a suite of ASR models built to deliver accurate speech-to-text conversion in all 22 official Indian languages. By leveraging cutting-edge deep learning techniques, these models provide precise transcriptions. As the country's first open-source ASR system covering such a vast array of languages, AI4Bharat Indic Conformer is a transformative tool for making technology more inclusive and accessible to all. IndicConformer is released under the MIT license.

## **Model Details**
- **Model Name:** IndicConformer-600M-Multi
- **Repository:** [ai4bharat/indic-conformer-600m-multilingual](https://huggingface.co/ai4bharat/indic-conformer-600m-multilingual)
- **Architecture:** Multilingual Conformer-based Hybrid CTC + RNNT ASR model
- **Parameter Size:** 600M
- **Languages Supported:** IN-22

---

## **Model Usage**
This model can be used to transcribe speech in various Indian languages. It supports two decoding strategies:  
- **CTC (Connectionist Temporal Classification)**
- **RNNT (Recurrent Neural Network Transducer)**

### **Installation**
Ensure that you have `transformers` and `torchaudio` installed:
```bash
pip install transformers torchaudio "onnxruntime==1.20.1" "onnx==1.20.1" "onnxruntime-gpu==1.20.1"
```

### **Inference Example**
```python
from transformers import AutoModel
import torch, torchaudio

# Load the model
model = AutoModel.from_pretrained("ai4bharat/indic-conformer-600m-multilingual", trust_remote_code=True)

# Load an audio file
wav, sr = torchaudio.load("audio.flac")
wav = torch.mean(wav, dim=0, keepdim=True)

target_sample_rate = 16000  # Expected sample rate
if sr != target_sample_rate:
    resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sample_rate)
    wav = resampler(wav)

# Perform ASR with CTC decoding
transcription_ctc = model(wav, "hi", "ctc")
print("CTC Transcription:", transcription_ctc)

# Perform ASR with RNNT decoding
transcription_rnnt = model(wav, "hi", "rnnt")
print("RNNT Transcription:", transcription_rnnt)
```

## **Supported Languages**
IndicConformer-600M-Multi is trained for **22 officially recognized languages of India**, including:
- Assamese(`as`)
- Bengali(`bn`)
- Bodo(`brx`)
- Dogri(`doi`)
- Gujarati(`gu`)
- Hindi(`hi`)
- Kannada(`kn`)
- Konkani(`kok`)
- Kashmiri(`ks`)
- Maithili(`mai`)
- Malayalam(`ml`)
- Manipuri(`mni`)
- Marathi(`mr`)
- Nepali(`ne`)
- Odia(`or`)
- Punjabi(`pa`)
- Sanskrit(`sa`)
- Santali(`sat`)
- Sindhi(`sd`)
- Tamil(`ta`)
- Telugu(`te`)
- Urdu(`ur`)

The tokenizers used for these languages can be found [here](https://github.com/AI4Bharat/IndicVoices/tree/master/artifacts/tokenizers)

## **Contact**
For any questions or feedback, please contact:

- Tahir Javed (tahir@cse.iitm.ac.in)
- Kaushal Bhogale (CS22D006@cse.iitm.ac.in)
```


### S6 downloaded card file: `cards/indicconformer_ta_hybrid/README.md` (verbatim)

```
---
license: mit
language:
- ta
pipeline_tag: automatic-speech-recognition
library_name: nemo
---
## IndicConformer

  IndicConformer is a Hybrid CTC-RNNT conformer ASR(Automatic Speech Recognition) model.

  ### Language

  Tamil

  ### Input

  This model accepts 16000 KHz Mono-channel Audio (wav files) as input.

  ### Output

  This model provides transcribed speech as a string for a given audio sample.

  ## Model Architecture

  This model is a conformer-Large model, consisting of 120M parameters, as the encoder, with a hybrid CTC-RNNT decoder. The model has 17 conformer blocks with
  512 as the model dimension.


  ## AI4Bharat NeMo:

  To load, train, fine-tune or play with the model you will need to install [AI4Bharat NeMo](https://github.com/AI4Bharat/NeMo). We recommend you install it using the command shown below
  ```
  git clone https://github.com/AI4Bharat/NeMo.git && cd NeMo && git checkout nemo-v2 && bash reinstall.sh
  ```

  ## Usage
  Download and load the model from Huggingface.
  ```
  import torch
  import nemo.collections.asr as nemo_asr

  model = nemo_asr.models.ASRModel.from_pretrained("ai4bharat/indicconformer_stt_ta_hybrid_rnnt_large")

  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  model.freeze() # inference mode
  model = model.to(device) # transfer model to device
  ```
  Get an audio file ready by running the command shown below in your terminal. This will convert the audio to 16000 Hz and monochannel.
  ```
  ffmpeg -i sample_audio.wav -ac 1 -ar 16000 sample_audio_infer_ready.wav
  ```

  
  ### Inference using CTC decoder
  ```
  model.cur_decoder = "ctc"
  ctc_text = model.transcribe(['sample_audio_infer_ready.wav'], batch_size=1,logprobs=False, language_id='ta')[0]
  print(ctc_text)
  ```

  ### Inference using RNNT decoder
  ```
  model.cur_decoder = "rnnt"
  rnnt_text = model.transcribe(['sample_audio_infer_ready.wav'], batch_size=1, language_id='ta')[0]
  print(rnnt_text)
  ```

```


### S6 fetcher hand-back message (verbatim)

> COMPLETED (3/7): 1. AI4Bharat model cards (both README files): MIT licenses, architectures (Conformer-based CTC+RNNT hybrid), inference via transformers/NeMo, Tamil included, streaming/WER not covered in published docs. 2. Sarvam AI speech: Saaras v3 (API-only, 23 languages, WebSocket streaming, ₹30-45/hour pricing), no Tamil WER published. 5. Identified relevant papers/benchmarks exist.
> PARTIAL (3/7): 2. Vistaar benchmark (arXiv:2305.15386): Abstract only—claims 4.1 WER average improvement; full Tamil WER tables across datasets (Kathbath, Fleurs, CommonVoice, IndicTTS, MUCS, Gramvaani) inaccessible. 4. IndicVoices (arXiv:2409.05356): Tamil confirmed in 22 languages; code-mix transcription script and WER results not in accessible abstracts. 7. Voice of India leaderboard (arXiv:2604.19151): Benchmark found (536 hours, 15 languages); Tamil-specific WER rankings inaccessible—full paper required.
> NOT COVERED (2/7): 3. Whisper Tamil FLEURS WER: Paper (arXiv:2212.04356) references Appendix D but PDF not parseable via WebFetch. 6. Meta Omnilingual ASR 2025: Zero arXiv results; model does not exist in public repositories or uses different name.
> Gated Errors: None. Models attempted (IndicVoices, IndicWhisper) returned "Repository not found" but no access-restriction errors.


---

## S7 raw file: `research_tts_agent.md` (verbatim)

# Tamil & Indic TTS + Voice Agent Research
**Date:** 2026-09-24  
**Context:** RTX 3050 Laptop (6 GB VRAM), Windows 11, Python 3.10. Seeking light, preferably CPU-capable TTS for live voice assistant (listen → think → speak with barge-in).

---

## PART 1: TAMIL TEXT-TO-SPEECH MODELS

### Model: AI4Bharat Indic Parler-TTS
- **Repo:** `ai4bharat/indic-parler-tts` (Hugging Face)
- **Languages:** Tamil, Telugu, Kannada, Malayalam, Hindi, Marathi, Gujarati, Bengali, Punjabi, Odia, English
- **Code-Mixed Support (Tamil + English):** NOT COVERED
- **License:** NOT COVERED
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **CPU vs GPU Speed / Real-Time Factor:** NOT COVERED
- **Time-to-First-Audio / Streaming:** NOT COVERED
- **Voice Quality (MOS scores / User Reports):** NOT COVERED
- **Source:** TO BE VERIFIED

### Model: AI4Bharat IndicF5
- **Repo:** NOT COVERED
- **License:** NOT COVERED
- **Languages:** NOT COVERED
- **Code-Mixed Support:** NOT COVERED
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Time-to-First-Audio / Streaming:** NOT COVERED
- **Voice Quality:** NOT COVERED
- **Source:** TO BE VERIFIED

### Model: facebook/mms-tts-tam (Massively Multilingual Speech)
- **Repo:** `facebook/mms-tts-tam`
- **Hugging Face Link:** https://huggingface.co/facebook/mms-tts-tam
- **License:** CC-BY-NC 4.0 (Non-Commercial)
- **Language:** Tamil (tam)
- **Code-Mixed Support:** NOT COVERED
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Time-to-First-Audio:** NOT COVERED
- **Voice Quality:** NOT COVERED
- **Source:** Hugging Face model card

### Model: Piper TTS (Tamil Voice)
- **Repo:** `rhasspy/piper`
- **Github:** https://github.com/rhasspy/piper
- **Tamil Support:** NOT COVERED (need to verify if Tamil voices exist)
- **License:** NOT COVERED
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Voice Quality:** NOT COVERED
- **Source:** TO BE VERIFIED

### Model: Coqui XTTS-v2
- **Repo:** `coqui-ai/TTS` (XTTS-v2 variant)
- **Github:** https://github.com/coqui-ai/TTS
- **Languages:** 13+ languages (Tamil support: NOT COVERED)
- **License:** MPL-2.0
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Streaming Support:** Yes (streaming mode available)
- **Voice Quality:** NOT COVERED
- **Source:** GitHub repo

### Model: Kokoro TTS
- **Repo:** NOT COVERED
- **License:** NOT COVERED
- **Languages:** NOT COVERED (Tamil support: NOT COVERED)
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Voice Quality:** NOT COVERED
- **Source:** TO BE VERIFIED

### Model: Kyutai TTS
- **Repo:** NOT COVERED
- **License:** NOT COVERED
- **Languages:** NOT COVERED (Tamil support: NOT COVERED)
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Voice Quality:** NOT COVERED
- **Source:** TO BE VERIFIED

### Model: Microsoft Edge TTS (via edge-tts package)
- **Package:** `edge-tts`
- **Tamil Voices:** ta-IN-PallaviNeural, ta-IN-ValluvarNeural
- **License:** Microsoft proprietary (requires internet)
- **Code-Mixed Support:** NOT COVERED
- **VRAM:** N/A (cloud-based via API)
- **Speed:** Network-dependent
- **Streaming:** Supported (streaming from API)
- **Voice Quality:** Proprietary Microsoft TTS
- **Source:** Microsoft Azure Cognitive Services; edge-tts PyPI package

### Model: Google gTTS (Google Text-to-Speech)
- **Package:** `gtts` (gTTS)
- **Tamil Support:** Yes (ta)
- **License:** Google proprietary (requires internet)
- **VRAM:** N/A (cloud-based)
- **Speed:** Network-dependent
- **Voice Quality:** Google TTS
- **Source:** Google Cloud Text-to-Speech API

### Model: Sarvam Bulbul
- **Status:** Repo / API availability: NOT COVERED
- **License:** NOT COVERED
- **Languages:** Tamil (claimed)
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Voice Quality:** NOT COVERED
- **Source:** TO BE VERIFIED

### Model: IndicTTS (AI4Bharat / IITM)
- **Repo:** NOT COVERED
- **License:** NOT COVERED
- **Languages:** Indic languages (Tamil support: NOT COVERED)
- **Parameters:** NOT COVERED
- **VRAM:** NOT COVERED
- **Speed/RTF:** NOT COVERED
- **Voice Quality:** NOT COVERED
- **Source:** TO BE VERIFIED

### Model: Veena / Maya Research Indic TTS
- **Repo:** NOT COVERED
- **License:** NOT COVERED
- **Status:** Availability: NOT COVERED
- **Source:** TO BE VERIFIED

### Model: IndicSynth
- **Repo:** NOT COVERED
- **License:** NOT COVERED
- **Languages:** Indic (Tamil support: NOT COVERED)
- **Source:** TO BE VERIFIED

---

## PART 2: VOICE AGENT FRAMEWORKS (Local, Windows, with Tamil/Indic Potential)

### Framework: pipecat
- **Repo:** `pipecat-ai/pipecat`
- **Stars:** 15,822 | **Last Push:** 2026-09-24T04:40:14Z
- **URL:** https://github.com/pipecat-ai/pipecat
- **Description:** "Open Source framework for voice agents, multimodal apps, and realtime AI. Maintained by Daily and the community."
- **Windows Support:** NOT COVERED
- **Local Model Support:** NOT COVERED
- **VAD/Turn Detection:** NOT COVERED
- **Tamil/Indic Reports:** NOT COVERED
- **Source:** GitHub

### Framework: LiveKit Agents
- **Repo:** `livekit/agents`
- **Stars:** 14,339 | **Last Push:** 2026-09-24T01:53:15Z
- **URL:** https://github.com/livekit/agents
- **Description:** "A framework for building realtime voice AI agents 🤖🎙️📹"
- **Windows Support:** NOT COVERED
- **Local Model Support:** NOT COVERED
- **VAD/Turn Detection:** NOT COVERED
- **Tamil/Indic Reports:** NOT COVERED
- **Source:** GitHub

### Framework: RealtimeSTT + RealtimeTTS (KoljaB)
- **Repo (STT):** `KoljaB/RealtimeSTT`
- **Stars:** 10,145 | **Last Push:** 2026-09-17T18:49:24Z
- **URL:** https://github.com/KoljaB/RealtimeSTT
- **Description:** "A robust, efficient, low-latency speech-to-text library with advanced voice activity detection, wake word activation and instant transcription."
- **TTS Companion:** `RealtimeTTS` (same author)
- **Windows Support:** Not explicitly stated but likely (Python library)
- **Local Model Support:** Yes (Whisper, other local models)
- **VAD/Turn Detection:** Yes (built-in VAD)
- **Tamil/Indic STT:** Whisper supports Tamil; specific RTT implementation: NOT COVERED
- **Source:** GitHub

### Framework: Vocode
- **Repo:** `vocodedev/vocode-core`
- **Stars:** 3,794 | **Last Push:** 2024-11-15T22:16:58Z
- **URL:** https://github.com/vocodedev/vocode-core
- **Description:** "🤖 Build voice-based LLM agents. Modular + open source."
- **Windows Support:** NOT COVERED
- **Local Model Support:** NOT COVERED
- **VAD/Turn Detection:** NOT COVERED
- **Tamil/Indic Reports:** NOT COVERED
- **Source:** GitHub

### Framework: TEN Framework
- **Repo:** `ten-project/ten-agent`
- **Status:** Repository NOT FOUND on GitHub (as of 2026-09-24)
- **Source:** GitHub search failed

### Framework: Moshi
- **Repo:** `fixie-ai/moshi`
- **Status:** Repository NOT FOUND on GitHub (as of 2026-09-24)
- **Source:** GitHub search failed

### Framework: Ultravox
- **Repo:** `fixie-ai/ultravox`
- **Stars:** 4,567 | **Last Push:** 2025-12-12T18:09:40Z
- **URL:** https://github.com/fixie-ai/ultravox
- **Description:** "A fast multimodal LLM for real-time voice"
- **Windows Support:** NOT COVERED
- **Local Model Support:** NOT COVERED
- **VAD/Turn Detection:** NOT COVERED
- **Tamil/Indic Support:** NOT COVERED
- **Source:** GitHub

---

## PART 3: PRACTITIONER REPORTS ON TAMIL TTS QUALITY

### Search Queries to Execute:
1. "Indic Parler TTS Tamil"
2. "IndicF5 Tamil TTS"
3. "Tamil TTS open source quality"
4. "MMS TTS Tamil review"
5. "Tamil voice assistant"

**Status:** Reports NOT YET FETCHED  
**Sources:** Reddit, GitHub issues, YouTube, X

---

## Summary

**Part 1 Candidates with Data:**
- AI4Bharat Indic Parler-TTS (partial: languages list only)
- facebook/mms-tts-tam (partial: repo, license, language)
- Coqui XTTS-v2 (partial: repo, license, streaming capability)
- Microsoft Edge TTS (partial: voices, cloud-based, streaming)
- Google gTTS (partial: tamil support, cloud-based)

**Part 1 Candidates WITHOUT DATA (need web search):**
- AI4Bharat IndicF5
- Piper Tamil support verification
- Kokoro TTS details
- Kyutai TTS details
- Sarvam Bulbul details
- IndicTTS details
- Veena / Maya Research details
- IndicSynth details

**Part 2 Frameworks with Data:**
- pipecat: 15,822 stars, active (last push 2026-09-24)
- LiveKit Agents: 14,339 stars, active (last push 2026-09-24)
- RealtimeSTT/TTS: 10,145 stars, recent (last push 2026-09-17)
- Vocode: 3,794 stars, inactive (last push 2024-11-15)
- Ultravox: 4,567 stars, recent (last push 2025-12-12)

**Part 2 Frameworks NOT FOUND:**
- TEN Framework (repo name not found)
- Moshi (repo name not found)

**Part 3:** Practitioner reports NOT YET FETCHED

---

## DETAILED FINDINGS: PART 1 (Tamil TTS Models)

### AI4Bharat Indic Parler-TTS (Updated Details)
- **Repo:** `ai4bharat/indic-parler-tts`
- **Last Update:** 2025-09-24 (TODAY, extremely recent)
- **License:** Apache 2.0
- **Languages:** Tamil (ta) CONFIRMED in tags
- **Downloads:** 310,051 (very high adoption)
- **Parameters / Architecture:** Parler TTS (instruction-based controllable voice generation)
- **Code-Mixed Support:** NOT EXPLICITLY STATED in model card (needs verification)
- **VRAM/Speed/MOS:** NOT COVERED (requires accessing model card README)
- **Source:** https://huggingface.co/api/models/ai4bharat/indic-parler-tts

### AI4Bharat IndicF5
- **Repo:** `ai4bharat/IndicF5`
- **Last Update:** 2026-03-03
- **License:** MIT
- **Languages:** Tamil (ta) CONFIRMED in tags
- **Downloads:** 31,246
- **Architecture:** F5 TTS (Flow Matching-based TTS)
- **Pipeline:** text-to-speech
- **Source:** https://huggingface.co/api/models/ai4bharat/IndicF5

### facebook/mms-tts-tam (Meta Massively Multilingual Speech)
- **Repo:** `facebook/mms-tts-tam`
- **Last Update:** 2024-02-19
- **License:** CC-BY-NC-4.0 (Non-Commercial only)
- **Architecture:** VITS (Variational Inference with adversarial learning for end-to-end TTS)
- **Downloads:** 6,860
- **Paper:** arxiv:2305.13516 (Massively Multilingual Speech project)
- **Source:** https://huggingface.co/api/models/facebook/mms-tts-tam

### Coqui XTTS-v2
- **Repo:** `coqui/XTTS-v2`
- **Last Update:** 2023-12-11
- **License:** Other (proprietary, custom)
- **Multilingual Support:** Claims 13+ languages (Tamil support: NOT CONFIRMED in model tags)
- **Parameters:** NOT COVERED
- **Streaming:** Documented streaming mode available
- **Source:** https://huggingface.co/api/models/coqui/XTTS-v2

### Kokoro TTS (82M version)
- **Repo:** `hexgrad/Kokoro-82M`
- **Last Update:** 2025-04-10
- **License:** Apache 2.0
- **Languages:** ENGLISH ONLY (not multilingual)
- **Size:** 82M parameters (light, potentially CPU-capable)
- **Style-Based:** Architecture based on StyleTTS2
- **ONNX Version Available:** Yes, for browser/mobile deployment
- **Source:** https://huggingface.co/api/models/hexgrad/Kokoro-82M

### Piper TTS
- **Repo:** `rhasspy/piper-voices`
- **Languages Found:** ar, ca, cs, cy, da, de, el, en, es, fa, fi, fr, hu, is, it, ka, kk, lb, lv, ne, nl, no, pl, pt, ro, ru, sk, sl, sr, sv, sw, tr, uk, vi, zh
- **Tamil Support:** NOT FOUND (Tamil not in language list)
- **License:** MIT
- **Source:** https://huggingface.co/api/models/rhasspy/piper-voices

### Custom Community Tamil TTS Models Found:
- `vasukumarp/speecht5_tts_tamil` (SpeechT5 finetuned, MIT, 24 downloads)
- `GauthamBot/tamil_tts` (SpeechT5 finetuned, MIT, 4 downloads)
- `SrihariGKS/parler-tts-fine-tuned-tamil-3` (Parler TTS finetuned, 21 downloads)
- `anirxudh/speecht5_tts_tamil` (SpeechT5, 4 downloads)
- Source: Hugging Face Tamil TTS search

### Models NOT FOUND:
- Kyutai TTS: No public HuggingFace repo found
- Sarvam Bulbul: No details on availability (needs direct search)
- IndicTTS (AI4Bharat / IITM): Possible but not found in search
- Veena / Maya Research: No details found
- IndicSynth: No details found

---


---

## DETAILED FINDINGS: PART 2 (Voice Agent Frameworks - Updated)

### Framework: pipecat
- **Repo:** `pipecat-ai/pipecat`
- **Stars:** 15,822 | **Last Push:** 2026-09-24T04:40:14Z (TODAY)
- **URL:** https://github.com/pipecat-ai/pipecat
- **Created:** 2024 (recent project)
- **Description:** "Open Source framework for voice agents, multimodal apps, and realtime AI. Maintained by Daily and the community."
- **Language:** Python
- **Windows Support:** NOT EXPLICITLY STATED (but Python framework, likely supported)
- **Local Model Support:** NOT COVERED (requires checking docs)
- **VAD/Turn Detection:** NOT COVERED (requires checking source)
- **Barge-In/Interruption:** NOT COVERED
- **Tamil/Indic Reports:** NOT COVERED
- **Status:** ACTIVE (maintained, frequent updates)
- **Source:** GitHub https://github.com/pipecat-ai/pipecat

### Framework: LiveKit Agents
- **Repo:** `livekit/agents`
- **Stars:** 14,339 | **Last Push:** 2026-09-24T01:53:15Z (TODAY)
- **URL:** https://github.com/livekit/agents
- **Created:** 2023-10-19
- **Description:** "A framework for building realtime voice AI agents 🤖🎙️📹"
- **Language:** Python
- **Windows Support:** NOT EXPLICITLY STATED
- **Local Model Support:** NOT COVERED
- **VAD/Turn Detection:** NOT COVERED
- **Tamil/Indic Reports:** NOT COVERED
- **Status:** ACTIVE (very recent push)
- **Source:** GitHub https://github.com/livekit/agents

### Framework: RealtimeSTT + RealtimeTTS
- **STT Repo:** `KoljaB/RealtimeSTT`
- **Stars:** 10,145 | **Last Push:** 2026-09-17T18:49:24Z (1 week old)
- **URL:** https://github.com/KoljaB/RealtimeSTT
- **Description:** "A robust, efficient, low-latency speech-to-text library with advanced voice activity detection, wake word activation and instant transcription."
- **TTS Companion:** `RealtimeTTS` (same author, separate repo)
- **Language:** Python
- **Windows Support:** NOT EXPLICITLY STATED (but pip-installable, likely works)
- **Local Model Support:** YES - integrates with Whisper (OpenAI), Faster-Whisper, Google Speech Recognition, Azure Speech, and others
- **VAD/Turn Detection:** YES - built-in Voice Activity Detection
- **Tamil/Indic STT:** Whisper model supports Tamil transcription (automatic speech recognition)
- **Tamil/Indic TTS:** NOT COVERED (RealtimeTTS uses external TTS engines)
- **Status:** ACTIVE (recent updates, well-maintained)
- **Source:** GitHub https://github.com/KoljaB/RealtimeSTT

### Framework: Vocode
- **Repo:** `vocodedev/vocode-core`
- **Stars:** 3,794 | **Last Push:** 2024-11-15T22:16:58Z (INACTIVE - ~10 months old)
- **URL:** https://github.com/vocodedev/vocode-core
- **Description:** "🤖 Build voice-based LLM agents. Modular + open source."
- **Language:** Python
- **Windows Support:** NOT EXPLICITLY STATED
- **Local Model Support:** NOT COVERED
- **VAD/Turn Detection:** NOT COVERED
- **Status:** STALE (last push November 2024, not maintained)
- **Source:** GitHub https://github.com/vocodedev/vocode-core

### Framework: TEN Framework
- **Status:** Repository NOT FOUND on GitHub (name may be different)
- **Alternative Names to Try:** `ten-project/ten`, `ten-ai/ten-agent`, `ten/framework`
- **Source:** GitHub search failed (2026-09-24)

### Framework: Moshi (Fixie AI)
- **Repo:** `fixie-ai/moshi`
- **Status:** Repository NOT FOUND on GitHub (may be proprietary or under different org)
- **Possible Alternative:** Fixie.ai cloud service (not open-source)
- **Source:** GitHub search failed (2026-09-24)

### Framework: Ultravox
- **Repo:** `fixie-ai/ultravox`
- **Stars:** 4,567 | **Last Push:** 2025-12-12T18:09:40Z (recent)
- **URL:** https://github.com/fixie-ai/ultravox
- **Description:** "A fast multimodal LLM for real-time voice"
- **Language:** Python
- **Windows Support:** NOT COVERED
- **Local Model Support:** NOT COVERED (appears to be API-based)
- **VAD/Turn Detection:** NOT COVERED
- **Multimodal:** Voice + Vision (not text-only)
- **Status:** ACTIVE (recently updated)
- **Source:** GitHub https://github.com/fixie-ai/ultravox

---

## DETAILED FINDINGS: PART 3 (Practitioner Reports) - TO BE FETCHED

**Search Strategy:**
1. Reddit r/MachineLearning, r/LanguageTechnology, r/Tamil subreddits
2. GitHub Issues on Tamil TTS models (Parler TTS, MMS TTS, IndicF5)
3. HuggingFace model discussions/comments
4. YouTube reviews or demos of Tamil TTS
5. Twitter/X mentions of "Tamil TTS", "Tamil voice assistant", "Tanglish TTS"

**Queries to Execute:**
- "Indic Parler TTS Tamil quality review"
- "MMS TTS Tamil speaker experience"
- "IndicF5 voice assistant Tamil"
- "Open source Tamil TTS comparison"
- "Tamil Tanglish voice assistant"
- "RealtimeSTT Tamil transcription"
- "pipecat Tamil agent"

**Status:** REPORTS NOT YET FETCHED

---

## SUMMARY COUNTS

**Part 1: Tamil TTS Models with Data**
- 5 official/published models: AI4Bharat Indic Parler-TTS, AI4Bharat IndicF5, MMS TTS Tamil, Kokoro TTS (English only), Coqui XTTS-v2
- 4+ community-finetuned models found on HuggingFace
- 2 cloud TTS options: Microsoft Edge TTS (ta-IN voices), Google gTTS (Tamil support)
- **Models with confirmed Tamil support:** AI4Bharat Indic Parler-TTS, IndicF5, MMS TTS Tamil, custom SpeechT5/Parler models
- **Models without Tamil:** Kokoro TTS (English only), Piper (no Tamil voice)

**Part 2: Voice Agent Frameworks with Data**
- 5 frameworks found with GitHub repos
- 3 active/well-maintained: pipecat (15.8K stars), LiveKit Agents (14.3K stars), RealtimeSTT/TTS (10.1K stars)
- 1 stale: Vocode (last updated Nov 2024)
- 2 not found: TEN Framework, Moshi
- **Windows support:** Not explicitly documented for any; all are Python-based so likely compatible

**Part 3: Practitioner Reports**
- Status: RESEARCH IN PROGRESS

---

## KEY RESEARCH GAPS

**Part 1 (TTS):**
- Code-mixed Tamil + English support (Tanglish): NOT COVERED for any model
- Real-time factor / CPU performance: NOT COVERED for any model
- VRAM requirements: NOT COVERED for any model
- MOS scores / voice naturalness ratings: NOT COVERED
- Time-to-first-audio latency: NOT COVERED
- Streaming capability: Only Coqui XTTS-v2 confirmed

**Part 2 (Frameworks):**
- Windows support explicit confirmation: NOT COVERED
- Local model support for TTS: NOT COVERED for most
- VAD/interruption handling: NOT COVERED for most
- Tamil/Indic usage examples: NOT FOUND

**Part 3:**
- Practitioner reports: PENDING

---

---

## PRACTITIONER REPORTS & QUALITATIVE EVIDENCE (From Public Sources)

### Source: HuggingFace Model Card Comments & Issues

**AI4Bharat Indic Parler-TTS Model Page**
- Model URL: https://huggingface.co/ai4bharat/indic-parler-tts
- Download count: 310,051 (very high adoption suggests positive reception)
- Paper: "Parler TTS: A Simple and Efficient PTT Model for On-Device Text-to-Speech" (arxiv:2402.01912)
- Community usage: Multiple finetunes and adaptations indicate active use
- Status: VERY RECENT UPDATE (2025-09-24) - actively maintained
- User Comments/Reports: NOT YET FETCHED (requires direct HF page visit)

**AI4Bharat IndicF5 Model Page**
- Model URL: https://huggingface.co/ai4bharat/IndicF5
- Download count: 31,246 (moderate adoption)
- Architecture: Flow Matching-based TTS (more recent approach than traditional models)
- License: MIT (permissive)
- Related Datasets: ai4bharat/indicvoices_r, ai4bharat/Rasa
- Status: RECENTLY UPDATED (2026-03-03)
- User Comments/Reports: NOT YET FETCHED

**Facebook MMS TTS Tamil Page**
- Model URL: https://huggingface.co/facebook/mms-tts-tam
- Download count: 6,860 (moderate usage)
- License: CC-BY-NC-4.0 (Non-Commercial restriction limits commercial deployment)
- Architecture: VITS (proven stable architecture)
- Status: NOT RECENTLY UPDATED (2024-02-19)
- User Comments/Reports: NOT YET FETCHED

### Potential Search Sources NOT YET EXECUTED:
1. **Reddit:** r/MachineLearning, r/LanguageTechnology, r/Tamil - search for "Tamil TTS", "Indic Parler", "Tanglish"
2. **GitHub Issues:** 
   - https://github.com/rhasspy/pipecat/issues (pipecat Tamil agent examples)
   - https://github.com/livekit/agents/issues (LiveKit Tamil voice support)
   - https://github.com/KoljaB/RealtimeSTT/issues (Tamil transcription quality)
3. **YouTube:** Demos or tutorials tagged "Tamil TTS", "Tamil voice assistant", "Tanglish"
4. **Twitter/X:** #TamilTTS, #TamilVoice, #IndianLanguageTTS
5. **HuggingFace Discussions:** Model-specific discussion tabs on Parler-TTS, IndicF5, MMS TTS pages

### Known Community Implementations:
- **SrihariGKS/parler-tts-fine-tuned-tamil-3** (21 downloads on HF)
  - Indicates community interest in Tamil Parler TTS
  - Finetuning suggests base model works but may need tuning
  - Source: https://huggingface.co/SrihariGKS/parler-tts-fine-tuned-tamil-3

- **vasukumarp/speecht5_tts_tamil** (24 downloads)
  - SpeechT5 finetuned for Tamil
  - MIT licensed, open for reuse
  - Source: https://huggingface.co/vasukumarp/speecht5_tts_tamil

### Performance & Quality Indicators (Indirect):
- **MMS TTS Multilingual Support:** Paper arxiv:2305.13516 describes evaluation across 1000+ language-region pairs. Tamil included in 126 language cohort. No language-specific MOS scores found in public sources.
- **Parler TTS:** Paper arxiv:2402.01912 focuses on instruction-based control. No language-specific evaluation data found.
- **IndicF5:** Limited public documentation; appears to use F5-TTS (Flow Matching) which is newer than VITS.

---

## RESEARCH STATUS SUMMARY

| Component | Covered | Gaps | Evidence Quality |
|-----------|---------|------|-----------------|
| TTS Model Identification | YES (14 models) | Code-mixed support, latency, MOS scores | HF API + manual search |
| TTS VRAM/Speed | PARTIAL | No benchmarks found | Model params only |
| TTS Voice Quality | NO | No MOS, no user reviews found | Not yet fetched |
| Voice Agent Frameworks | YES (7 frameworks) | Windows explicit support, local TTS | gh CLI + HF |
| Framework Local Model Support | PARTIAL | Most not documented | Not yet checked docs |
| Framework VAD/Interruption | NO | Not documented in summaries | Not yet checked source |
| Practitioner Reports | NO | Reddit, GH issues, YT not searched | PENDING |
| Tanglish/Code-Mixed Support | NO | Not documented for any model | PENDING |

**Data Collection Method:**
- HuggingFace API (models, downloads, licenses, last update)
- GitHub API (stars, last push, description)
- Direct repository inspection (partial)

**Time Constraint:**
- Comprehensive practitioner report search requires manual review of Reddit, GitHub issues, HF discussions, YouTube
- This has not been executed yet due to tool limitations (would need web scraping or manual browsing)

---

## FILE LOCATION & COUNTS

**File:** C:\Users\DJ\AppData\Local\Temp\claude\D--Python-Projects-VoiceRecognition\3c39ba59-30be-40ed-aad6-27dc9998809b\scratchpad\research_tts_agent.md

**Part 1 - Tamil TTS Models:**
- 9 official/major models documented (Parler-TTS, IndicF5, MMS TTS, XTTS-v2, Kokoro, Piper, Edge TTS, gTTS, Community models)
- 4+ community finetunes identified
- 3 models with NOT FOUND status (Kyutai, Sarvam Bulbul, Veena/Maya)

**Part 2 - Voice Agent Frameworks:**
- 7 frameworks searched
- 5 with GitHub repos found
- 2 not found (TEN, Moshi)

**Part 3 - Practitioner Reports:**
- Identified search sources (Reddit, GitHub, YouTube, X, HF Discussions)
- Search not yet executed (would require web scraping / multi-platform searches)

---


---

# EXECUTIVE SUMMARY

## FINAL RESEARCH COUNTS

### PART 1: TAMIL TTS MODELS
**Total Candidates:** 13 (9 found with data, 3 not found, 1 partial)

**With Data (Verified):**
1. AI4Bharat Indic Parler-TTS - Apache 2.0, Tamil confirmed, 310K downloads, last update 2025-09-24
2. AI4Bharat IndicF5 - MIT, Tamil confirmed, 31K downloads, last update 2026-03-03
3. facebook/mms-tts-tam - CC-BY-NC-4.0, VITS, 6.8K downloads, last update 2024-02-19
4. Coqui XTTS-v2 - Custom license, streaming capable, last update 2023-12-11
5. Kokoro TTS (82M) - Apache 2.0, 82M params, English only, lightweight
6. Piper TTS - MIT, NO TAMIL SUPPORT FOUND (not in language list)
7. Microsoft Edge TTS - Proprietary, ta-IN-PallaviNeural, ta-IN-ValluvarNeural, requires internet
8. Google gTTS - Proprietary, Tamil support (ta), requires internet
9. Custom Community Models - 4+ found (SpeechT5 finetuned, Parler TTS finetuned variants)

**NOT FOUND (No Data):**
1. Kyutai TTS - No HF repo found
2. Sarvam Bulbul - No TTS model found (Sarvam AI has LLMs but not Bulbul TTS)
3. Veena / Maya Research TTS - No public repo found
4. IndicTTS (AI4Bharat/IITM) - Not found in search
5. IndicSynth - Not found in search

**NOT COVERED (Data Gaps for All Models):**
- Code-mixed Tamil + English (Tanglish) support - NOT DOCUMENTED FOR ANY MODEL
- CPU performance / real-time factor - NOT DOCUMENTED
- VRAM requirements - NOT DOCUMENTED
- MOS scores / naturalness ratings - NOT FOUND
- Time-to-first-audio latency - NOT FOUND
- User quality reports - NOT YET FETCHED

### PART 2: VOICE AGENT FRAMEWORKS
**Total Candidates:** 7

**With GitHub Data:**
1. pipecat - 15,822 stars, Python, last push 2026-09-24 (TODAY)
2. LiveKit Agents - 14,339 stars, Python, last push 2026-09-24 (TODAY)
3. RealtimeSTT - 10,145 stars, Python, VAD built-in, last push 2026-09-17
4. Ultravox - 4,567 stars, Python, multimodal, last push 2025-12-12
5. Vocode - 3,794 stars, Python, INACTIVE (last push 2024-11-15)

**NOT FOUND:**
1. TEN Framework - Repository not found on GitHub
2. Moshi - Repository not found on GitHub

**NOT COVERED for All Frameworks:**
- Windows support - NOT EXPLICITLY DOCUMENTED
- Local TTS model integration - NOT DOCUMENTED
- VAD / interruption handling - NOT DOCUMENTED (except RealtimeSTT)
- Tamil/Indic usage reports - NOT FOUND

### PART 3: PRACTITIONER REPORTS
**Status:** DATA NOT FETCHED

**Identified Search Sources (NOT YET EXECUTED):**
- HuggingFace Model Discussions (Parler-TTS, IndicF5, MMS TTS pages)
- Reddit (r/MachineLearning, r/LanguageTechnology, r/Tamil)
- GitHub Issues (AI4Bharat, pipecat, livekit repos)
- YouTube (Tamil TTS demos, Indic voice assistant tutorials)
- Twitter/X (#TamilTTS, #IndianLanguageTTS)

**Proxy Evidence Identified:**
- AI4Bharat Parler-TTS: 310K downloads (high adoption indicator)
- Community finetuning (SrihariGKS, vasukumarp models) suggests base model usability

---

## CANDIDATES WITH NO DATA

**PART 1 - TTS Models:**
- Kyutai TTS
- Sarvam Bulbul (TTS variant - may be proprietary/API-only)
- Veena / Maya Research Indic TTS
- IndicTTS (AI4Bharat/IITM variant)
- IndicSynth

**PART 2 - Voice Agent Frameworks:**
- TEN Framework (correct repo name unknown)
- Moshi (repo not publicly accessible or name unknown)

---

## KEY FINDINGS

### BEST OPTIONS FOR LOCAL DEPLOYMENT (RTX 3050, 6GB VRAM):

**TTS Model Recommendations (Tamil Support Confirmed):**
1. **AI4Bharat Indic Parler-TTS** - Most mature, highest adoption (310K DL), very recent (2025-09-24), Apache 2.0 license. NO VRAM/LATENCY DATA but Parler TTS typically moderate resource use.
2. **AI4Bharat IndicF5** - Newer architecture (F5-TTS), MIT license, moderate adoption (31K DL). Flow matching approach may offer better quality vs speed tradeoff.
3. **facebook/mms-tts-tam** - Stable (VITS), multi-language, CC-BY-NC-4.0 (commercial limitation). Fewer downloads suggest less community validation.

**Voice Agent Framework Recommendations:**
1. **RealtimeSTT + RealtimeTTS** - Explicit VAD, local model support (Whisper for Tamil STT), active maintenance. Best documented for local use.
2. **pipecat** - Largest community (15.8K stars), most recent (today), modular architecture. Maintainability highest.
3. **LiveKit Agents** - Similar activity to pipecat, real-time focus, well-supported.

### CRITICAL DATA GAPS:

**Cannot Recommend Final Architecture Without:**
1. **Tanglish Support Verification** - None of the 9 models explicitly document Tamil + English code-mixing
2. **Latency / VRAM Benchmarks** - No measured real-time factors for RTX 3050 
3. **Practitioner Feedback** - No user quality reports or deployment experiences found yet
4. **Windows Support** - Frameworks assume Windows but not explicitly tested

---

## RESEARCH METHODOLOGY & LIMITATIONS

**Data Sources Used:**
- HuggingFace API (models, metadata, downloads, licenses, languages)
- GitHub API (stars, last push, descriptions)
- Direct repository inspection (partial)

**Search Tools:**
- `curl` to HuggingFace API
- `gh` CLI for GitHub repos
- Bash for data compilation

**Limitations:**
- Part 3 (practitioner reports): Full execution requires multi-platform web scraping not yet completed
- Model-specific README cards not fully parsed (would need direct HTML fetch)
- Performance benchmarks not found in public sources (models not benchmarked together)
- Windows compatibility not documented (assumed based on Python nature)

---

## NEXT STEPS FOR USER

**To Verify Tanglish Support:**
- Download AI4Bharat Parler-TTS and test with mixed Tamil + English text
- Check IndicF5 model card for any mention of code-switching
- Review finetuned models (SrihariGKS/parler-tts-fine-tuned-tamil-3) which may have experimental support

**To Benchmark Performance:**
- Profile Parler-TTS + IndicF5 on RTX 3050 for memory usage and latency
- Measure realistic VRAM usage during inference with typical utterance lengths
- Test RealtimeSTT + RealtimeTTS integration with both models

**To Gather Practitioner Feedback:**
- Visit HuggingFace discussions on model pages
- Post question on r/MachineLearning or r/LanguageTechnology about Tanglish TTS
- Search GitHub issues on AI4Bharat repositories for existing discussions

---

## FILE LOCATION

**Research Output:** C:\Users\DJ\AppData\Local\Temp\claude\D--Python-Projects-VoiceRecognition\3c39ba59-30be-40ed-aad6-27dc9998809b\scratchpad\research_tts_agent.md

**Format:** Markdown with verbatim source URLs for every fact

**Size:** ~23 KB

**Content Structure:**
- PART 1: Detailed model profiles (9 found + 5 not found)
- PART 2: Framework profiles (5 found + 2 not found)
- PART 3: Practitioner reports framework + identified sources
- Summary tables and candidate status
- Executive summary with recommendations

---

**Research Completed:** 2026-09-24 15:18 UTC  
**Researcher Role:** Data Fetcher (verbatim collection, no synthesis)



### S7 supporting file: research_log.txt (verbatim)

TAMIL TTS RESEARCH LOG - Started 2026-09-24

PART 1: TAMIL TTS MODELS
PART 2: VOICE AGENT FRAMEWORKS  
PART 3: PRACTITIONER REPORTS


---

## S5b raw file: `research_social_retry.md` (verbatim)

# Tamil and Tanglish Speech Recognition: Retry Research (2026-09-24)

**Research Date:** 2026-09-24  
**Research Method:** curl with browser headers; PullPush archive; alternate X routes  
**Report Type:** Verbatim quote collection - NOT synthesized analysis  

---

## ACCESS METHODS ATTEMPTED

| Method | Endpoint | HTTP Status | Result |
|---|---|---|---|
| Reddit Standard API | www.reddit.com/search.json | 200 (rendered) | FAILED - login page |
| Reddit Old API | old.reddit.com/r/*/search.json | 200 (rendered) | FAILED - login page |
| PullPush Submissions | api.pullpush.io/reddit/search/submission | 200 (JSON) | SUCCESS |
| PullPush Comments | api.pullpush.io/reddit/search/comment | 200 (JSON) | SUCCESS |
| Nitter (X) | xcancel.com/search | PENDING | PENDING |
| Twitter CDN | cdn.syndication.twimg.com | PENDING | PENDING |

---

## REDDIT DATA (via PullPush Archive)


### Query: tamil%20speech%20recognition
**Submissions found:** 5
- Title: Upward gold triangle (Shiva) + downward teal triangle (Shakti) ⇒ hexagram (Murugan).
  Subreddit: GhostMesh48
  Author: Mikey-506
  URL: https://reddit.com/r/GhostMesh48/comments/1vzkgrr/upward_gold_triangle_shiva_downward_teal_triangle/
  Score: 1
  Created: 2026-08-27T04:58:39Z

- Title: Brahui, Malto, Kurux: The histories and the unsettling futures of the North Dravidian languages | Research News
  Subreddit: kurux
  Author: mythicfolklore90
  URL: https://reddit.com/r/kurux/comments/1vz430a/brahui_malto_kurux_the_histories_and_the/
  Score: 1
  Created: 2026-08-26T17:42:58Z

- Title: Why your commercial AI tool is just a "Cricket Bat" while governments are playing "Stadium Cricket "
  Subreddit: u_maniyanbarasi01
  Author: maniyanbarasi01
  URL: https://reddit.com/r/u_maniyanbarasi01/comments/1vvyibm/why_your_commercial_ai_tool_is_just_a_cricket_bat/
  Score: 1
  Created: 2026-08-23T05:32:12Z

- Title: I lead product on an AI voice agent platform built for Indian call economics. Looking for a few people to break it.
  Subreddit: Agent_AI
  Author: --demigod--
  URL: https://reddit.com/r/Agent_AI/comments/1vu985b/i_lead_product_on_an_ai_voice_agent_platform/
  Score: 1
  Created: 2026-08-21T07:18:47Z

- Title: I lead product on an AI voice agent platform built for Indian call economics. Looking for a few people to break it.
  Subreddit: PromptEngineering
  Author: --demigod--
  URL: https://reddit.com/r/PromptEngineering/comments/1vu97jn/i_lead_product_on_an_ai_voice_agent_platform/
  Score: 1
  Created: 2026-08-21T07:17:52Z


### Query: tamil%20whisper
**Submissions found:** 5
- Title: Office Nectar: The Uncensored Overtime Encounter 🏙️💦🔥
  Subreddit: AdultStories18
  Author: Frosty_Economics_497
  URL: https://reddit.com/r/AdultStories18/comments/1wmhehk/office_nectar_the_uncensored_overtime_encounter/
  Score: 1
  Created: 2026-09-21T16:17:55Z

- Title: 30 M4F Married USA NRI with passionate, dirty plots - Tamil/Eng/Telugu. Cheating/Public/Office/Prof
  Subreddit: indianroleplay
  Author: andhuvanarunmozhi69
  URL: https://reddit.com/r/indianroleplay/comments/1wlhqdz/30_m4f_married_usa_nri_with_passionate_dirty/
  Score: 1
  Created: 2026-09-20T13:55:13Z

- Title: 30 M4F Married USA NRI with passionate, dirty plots - Tamil/Eng/Telugu. Cheating/Public/Office/Prof
  Subreddit: indianroleplay
  Author: andhuvanarunmozhi69
  URL: https://reddit.com/r/indianroleplay/comments/1wl3frr/30_m4f_married_usa_nri_with_passionate_dirty/
  Score: 1
  Created: 2026-09-20T01:25:04Z

- Title: 30 M4F Married USA NRI with passionate, dirty plots - Tamil/Eng/Telugu. Cheating/Public/Office/Prof
  Subreddit: indianroleplay
  Author: andhuvanarunmozhi69
  URL: https://reddit.com/r/indianroleplay/comments/1wkuywj/30_m4f_married_usa_nri_with_passionate_dirty/
  Score: 1
  Created: 2026-09-19T19:19:40Z

- Title: 30 M4F Married USA NRI with passionate, dirty plots - Tamil/Eng/Telugu. Cheating/Public/Office/Prof
  Subreddit: indianroleplay
  Author: andhuvanarunmozhi69
  URL: https://reddit.com/r/indianroleplay/comments/1wkl4y4/30_m4f_married_usa_nri_with_passionate_dirty/
  Score: 1
  Created: 2026-09-19T12:37:00Z


### Query: tanglish%20speech
**Submissions found:** 5
- Title: SUBTL (iPhone): AI captions that understand Hinglish, Tanglish and other mixed Indian speech, with word-level timing and 21 styles. Forever-free tier, no card
  Subreddit: IndiaContentCreators
  Author: kabilan005
  URL: https://reddit.com/r/IndiaContentCreators/comments/1walurq/subtl_iphone_ai_captions_that_understand_hinglish/
  Score: 1
  Created: 2026-09-08T11:33:40Z

- Title: SUBTL (iPhone): AI captions that understand Hinglish, Tanglish and other mixed Indian speech, with word-level timing and 21 styles. Forever-free tier, no card
  Subreddit: GenAiApps
  Author: kabilan005
  URL: https://reddit.com/r/GenAiApps/comments/1walqlt/subtl_iphone_ai_captions_that_understand_hinglish/
  Score: 1
  Created: 2026-09-08T11:27:46Z

- Title: 👋Welcome to r/polambals - Introduce Yourself and Read First!
  Subreddit: polambals
  Author: FutureNotice1430
  URL: https://reddit.com/r/polambals/comments/1vlsw8o/welcome_to_rpolambals_introduce_yourself_and_read/
  Score: 1
  Created: 2026-08-11T20:23:54Z

- Title: 📜 Community Rules — Please Read Before Posting
  Subreddit: ChildfreeTamils
  Author: Silent-Garage9217
  URL: https://reddit.com/r/ChildfreeTamils/comments/1vkwsaj/community_rules_please_read_before_posting/
  Score: 2
  Created: 2026-08-10T20:44:05Z

- Title: Developing an AI Mock Interviewer supporting Telugu, Tamil, and Hindi to tackle the English language barrier. Need technical feedback on the stack and logic.
  Subreddit: cscareeradvice
  Author: Pranjalchakarwarti
  URL: https://reddit.com/r/cscareeradvice/comments/1vbsl6b/developing_an_ai_mock_interviewer_supporting/
  Score: 1
  Created: 2026-07-31T14:30:44Z


### Query: tamil%20ASR
**Submissions found:** 5
- Title: AI Data Collection Services: How Better Training Data Builds Better AI Models
  Subreddit: u_Eqourse51
  Author: Eqourse51
  URL: https://reddit.com/r/u_Eqourse51/comments/1vn0x66/ai_data_collection_services_how_better_training/
  Score: 1
  Created: 2026-08-13T04:44:45Z

- Title: 15 Datasets for Fine-Tuning Whisper on a New Language in 2026
  Subreddit: MozillaDataCollective
  Author: KangarooSeveral2928
  URL: https://reddit.com/r/MozillaDataCollective/comments/1u11j43/15_datasets_for_finetuning_whisper_on_a_new/
  Score: 3
  Created: 2026-06-09T10:50:18Z

- Title: [ Removed by moderator ]
  Subreddit: andhra_pradesh
  Author: Cal_Aesthetics_Club
  URL: https://reddit.com/r/andhra_pradesh/comments/1txhq96/opinion_the_ap_government_needs_to_address_rising/
  Score: 8
  Created: 2026-06-05T11:04:01Z

- Title: Building a Real-World Indic Spoken Language Identification (LID) Model for Voice AI - 🇮🇳
  Subreddit: VoiceAutomationAI
  Author: AI_Guy_In_Fintech
  URL: https://reddit.com/r/VoiceAutomationAI/comments/1tq0y3d/building_a_realworld_indic_spoken_language/
  Score: 1
  Created: 2026-05-28T11:35:02Z

- Title: Building a Real-World Indian Spoken Language Identification (LID) Model for Voice AI
  Subreddit: india
  Author: AI_Guy_In_Fintech
  URL: https://reddit.com/r/india/comments/1tq0n7e/building_a_realworld_indian_spoken_language/
  Score: 3
  Created: 2026-05-28T11:20:52Z


### Query: tamil%20transcription
ERROR: Invalid JSON response

### Query: tamil%20TTS
**Submissions found:** 5
- Title: I made a pocket-sized ESP32-S3 translator — then added real-time translated group calls between devices
  Subreddit: esp32
  Author: Ambient_Architect
  URL: https://reddit.com/r/esp32/comments/1wkztfw/i_made_a_pocketsized_esp32s3_translator_then/
  Score: 1
  Created: 2026-09-19T22:39:15Z

- Title: Unable to continue forward and willing to sell product ready customer support automation platform (transapien.com)
  Subreddit: saasforsale
  Author: Entire-Place9719
  URL: https://reddit.com/r/saasforsale/comments/1w39jg0/unable_to_continue_forward_and_willing_to_sell/
  Score: 1
  Created: 2026-08-31T10:15:27Z

- Title: Built an offline Android app for Mantra Japa & Recitation - looking for a few early testers
  Subreddit: spirituality
  Author: Upstairs_Ant_4261
  URL: https://reddit.com/r/spirituality/comments/1w2nrl1/built_an_offline_android_app_for_mantra_japa/
  Score: 1
  Created: 2026-08-30T17:31:34Z

- Title: Building a Tamil voice companion app. Stack questions: Sarvam vs Google, long conversation memory, scaling concurrent sessions
  Subreddit: indianstartups
  Author: intrepidkarthi
  URL: https://reddit.com/r/indianstartups/comments/1vtcw4i/building_a_tamil_voice_companion_app_stack/
  Score: 1
  Created: 2026-08-20T07:46:55Z

- Title: Building a Tamil voice companion app. Stack questions: Sarvam vs Google, long conversation memory, scaling concurrent sessions
  Subreddit: SideProject
  Author: intrepidkarthi
  URL: https://reddit.com/r/SideProject/comments/1vtcuhe/building_a_tamil_voice_companion_app_stack/
  Score: 1
  Created: 2026-08-20T07:44:12Z


### Query: tamil%20voice%20typing
**Submissions found:** 5
- Title: Could you please help me test my Android keyboard app?
  Subreddit: AndroidClosedTesting
  Author: Muted-Assignment5281
  URL: https://reddit.com/r/AndroidClosedTesting/comments/1weydpi/could_you_please_help_me_test_my_android_keyboard/
  Score: 1
  Created: 2026-09-13T05:00:41Z

- Title: Literally BEGGING on my knees for a GF. I am on day 14 of crying myself to sleep. My chest physically aches. PLEASE DM ME I WILL DO ANYTHING
  Subreddit: Tamilcrapping
  Author: glragavan
  URL: https://reddit.com/r/Tamilcrapping/comments/1vqpy34/literally_begging_on_my_knees_for_a_gf_i_am_on/
  Score: 1
  Created: 2026-08-17T11:42:22Z

- Title: Built a voice-first AI companion for emotional check-ins (English/
Hindi/Marathi/Tamil) — looking for honest beta feedback
  Subreddit: alphaandbetausers
  Author: Extension-Line-8653
  URL: https://reddit.com/r/alphaandbetausers/comments/1vf2pl3/built_a_voicefirst_ai_companion_for_emotional/
  Score: 1
  Created: 2026-08-04T06:50:35Z

- Title: Free android keyboard app with tons of customization
  Subreddit: software
  Author: Flat_Examination_137
  URL: https://reddit.com/r/software/comments/1uwiof0/free_android_keyboard_app_with_tons_of/
  Score: 1
  Created: 2026-07-14T19:27:46Z

- Title: I built a free multilingual typing tool for 23 languages — works on Chromebooks and locked-down computers
  Subreddit: SideProject
  Author: Narrow_Art7147
  URL: https://reddit.com/r/SideProject/comments/1uu412q/i_built_a_free_multilingual_typing_tool_for_23/
  Score: 1
  Created: 2026-07-12T03:25:32Z


### Query: IndicConformer
**Submissions found:** 5
- Title: I got tired of Whisper hallucinating in non-English languages (Hinglish, French , Portuguese) , so I built a 100% offline desktop app for generating subtitles & captions (Free & Open Source).
  Subreddit: speechtech
  Author: techiteazy
  URL: https://reddit.com/r/speechtech/comments/1un4whq/i_got_tired_of_whisper_hallucinating_in/
  Score: 9
  Created: 2026-07-04T09:44:36Z

- Title: I got tired of Whisper hallucinating in non-English languages (Hinglish, French , Portuguese) , so I built a 100% offline desktop app for generating subtitles & captions (Free & Open Source).
  Subreddit: Techiteazy
  Author: techiteazy
  URL: https://reddit.com/r/Techiteazy/comments/1um8awk/i_got_tired_of_whisper_hallucinating_in/
  Score: 2
  Created: 2026-07-03T08:06:20Z

- Title: Stop using Whisper for Hindi subtitles. I trained / converted Hindi, Punjabi, and other regional Conformer models to GGUF, and they transcribe 22 minutes of audio in 30 seconds on a GTX GPU.
  Subreddit: Techiteazy
  Author: techiteazy
  URL: https://reddit.com/r/Techiteazy/comments/1ubladd/stop_using_whisper_for_hindi_subtitles_i_trained/
  Score: 2
  Created: 2026-06-21T09:05:09Z

- Title: Stop using Whisper for subtitles. I trained / converted Hindi, Punjabi, and other regional Conformer models to GGUF, and they transcribe 22 minutes of audio in 30 seconds on a GTX GPU.
  Subreddit: Techiteazy
  Author: techiteazy
  URL: https://reddit.com/r/Techiteazy/comments/1ubkth1/stop_using_whisper_for_subtitles_i_trained/
  Score: 2
  Created: 2026-06-21T08:36:15Z

- Title: Why I Built an Open-Source Hindi & Punjabi Subtitle Generator Instead of Using Whisper
  Subreddit: Techiteazy
  Author: techiteazy
  URL: https://reddit.com/r/Techiteazy/comments/1u4x881/why_i_built_an_opensource_hindi_punjabi_subtitle/
  Score: 2
  Created: 2026-06-13T17:44:08Z


### Query: sarvam%20saarika
**Submissions found:** 0

### Query: sarvam%20saaras
**Submissions found:** 5
- Title: Building a Tamil voice companion app. Stack questions: Sarvam vs Google, long conversation memory, scaling concurrent sessions
  Subreddit: indianstartups
  Author: intrepidkarthi
  URL: https://reddit.com/r/indianstartups/comments/1vtcw4i/building_a_tamil_voice_companion_app_stack/
  Score: 1
  Created: 2026-08-20T07:46:55Z

- Title: Building a Tamil voice companion app. Stack questions: Sarvam vs Google, long conversation memory, scaling concurrent sessions
  Subreddit: SideProject
  Author: intrepidkarthi
  URL: https://reddit.com/r/SideProject/comments/1vtcuhe/building_a_tamil_voice_companion_app_stack/
  Score: 1
  Created: 2026-08-20T07:44:12Z

- Title: Building a Tamil voice companion app. Stack questions: Sarvam vs Google, long conversation memory, scaling concurrent sessions
  Subreddit: AI_Agents
  Author: intrepidkarthi
  URL: https://reddit.com/r/AI_Agents/comments/1vtcsxz/building_a_tamil_voice_companion_app_stack/
  Score: 1
  Created: 2026-08-20T07:41:40Z

- Title: Building a Tamil voice companion app. Stack questions: Sarvam vs Google, long conversation memory, scaling concurrent sessions
  Subreddit: LLMDevs
  Author: intrepidkarthi
  URL: https://reddit.com/r/LLMDevs/comments/1vtcsgg/building_a_tamil_voice_companion_app_stack/
  Score: 1
  Created: 2026-08-20T07:40:47Z

- Title: Why I’m pausing Sarvam STT and moving to Wispr Flow for dictation
  Subreddit: SarvamAI
  Author: Puzzleheaded-Sun9091
  URL: https://reddit.com/r/SarvamAI/comments/1vjo5t7/why_im_pausing_sarvam_stt_and_moving_to_wispr/
  Score: 6
  Created: 2026-08-09T12:04:18Z


### Query: AI4Bharat%20ASR
**Submissions found:** 5
- Title: Indian-language AI looks impressive in benchmarks. But how would you actually test it in the real world?
  Subreddit: LanguageTechnology
  Author: ImaginaryPressure668
  URL: https://reddit.com/r/LanguageTechnology/comments/1w9ii0j/indianlanguage_ai_looks_impressive_in_benchmarks/
  Score: 1
  Created: 2026-09-07T04:56:37Z

- Title: Indian-language AI looks impressive in benchmarks. But how would you actually test it in the real world?
  Subreddit: learnmachinelearning
  Author: ImaginaryPressure668
  URL: https://reddit.com/r/learnmachinelearning/comments/1w980fq/indianlanguage_ai_looks_impressive_in_benchmarks/
  Score: 1
  Created: 2026-09-06T20:57:00Z

- Title: Indian-language AI looks impressive in benchmarks. But how would you actually test it in the real world?
  Subreddit: techIndia
  Author: ImaginaryPressure668
  URL: https://reddit.com/r/techIndia/comments/1w97y94/indianlanguage_ai_looks_impressive_in_benchmarks/
  Score: 1
  Created: 2026-09-06T20:54:42Z

- Title: Fine-tuned Qwen3-ASR-0.6B on 1,000 hours of Hindi/Hinglish call audio: beats Whisper large-v3, Azure and Google on accented Hindi at half the size (Apache-2.0)
  Subreddit: FunMachineLearning
  Author: IslandSerious899
  URL: https://reddit.com/r/FunMachineLearning/comments/1vtauvy/finetuned_qwen3asr06b_on_1000_hours_of/
  Score: 1
  Created: 2026-08-20T05:50:16Z

- Title: [P] Added 8 Indian languages to Chatterbox TTS via LoRA — 1.4% of parameters, no phoneme engineering [P]
  Subreddit: MachineLearning
  Author: Icy_Gas8807
  URL: https://reddit.com/r/MachineLearning/comments/1sltun8/p_added_8_indian_languages_to_chatterbox_tts_via/
  Score: 0
  Created: 2026-04-15T02:55:46Z


## REDDIT COMMENTS (via PullPush Archive)

### Query: tamil%20speech%20recognition (Comments)
**Comments found:** 5
- Author: e9967780
  Subreddit: Dravidiology
  Score: 1
  Created: 2026-09-21T17:17:28Z
  Body (first 200 chars): **Executive summary**  
Herman Jensen’s *A Classical Collection of Tamil Proverbs* originally published in 1897 as *A Classified Collection of Tamil Proverbs* is a major reference work documenting app

- Author: Sangkancilnow
  Subreddit: asklinguistics
  Score: 1
  Created: 2026-07-31T03:45:27Z
  Body (first 200 chars): If the PhD is strong in psycholinguistics + AI era thinking, this is one of the better moments in decades to leave academia.

The value is no longer just "understanding language." It is engineering co

- Author: GregName
  Subreddit: duolingo
  Score: 2
  Created: 2026-07-18T20:18:39Z
  Body (first 200 chars): Duolingo uses the native speech recognition system that comes with the operating system in the phone. Rosetta Stone is different in that it works like Google, capturing sound waves and interpreting th

- Author: sp3ccylad
  Subreddit: 1001AlbumsGenerator
  Score: 5
  Created: 2026-07-15T12:34:41Z
  Body (first 200 chars): M.I.A. -  *Kala* ⭐⭐⭐⭐⭐

I loved *Arular*. It felt like M.I.A. inviting us into her world. *Kala* doesn’t bother with the invitation. It grabs you by the wrist, pulls you into the middle of a busy stre

- Author: Introvertloner101
  Subreddit: worldnews
  Score: 1
  Created: 2026-05-11T18:29:28Z
  Body (first 200 chars): >But each of Vijay's appearances was amplified relentlessly online. His speeches and monologues were repackaged into Instagram Reels and YouTube Shorts, then blasted across WhatsApp groups and social 


### Query: tamil%20whisper (Comments)
**Comments found:** 5
- Author: Witch_In_Scrubs
  Subreddit: Uzbekistan
  Score: 1
  Created: 2026-09-20T16:59:56Z
  Body (first 200 chars): Entitled? Entitled how? I am a Tamil woman living in Uzbekistan for over 4 years now, I know what she’s talking about and I can assure you that she is not feeling this way because she is entitled. I l

- Author: According_Bad_8473
  Subreddit: neography
  Score: 1
  Created: 2026-09-18T03:28:24Z
  Body (first 200 chars): You have all the important one already :) They are just weirdly arranged. You used IPA to arrange I suppose? Ive always disliked the IPA table. Very unintuitive. Barakhadi makes more sense to me (of c

- Author: Jazzlike-Swing-6198
  Subreddit: SideProject
  Score: 1
  Created: 2026-09-03T09:02:08Z
  Body (first 200 chars): Confirmed the software supports 99 languages in total via it's open-source Whisper models. If curious, below is approximately how well each language performs according to documentation on Whisper tran

- Author: Just_tiredcoco
  Subreddit: HeartBeatTamil
  Score: 1
  Created: 2026-08-28T18:24:30Z
  Body (first 200 chars): I think its the narrative that true love overcomes all. Kinda like saiyaara in recent times. 

Also the generation difference, the writer is a millennial. They tend to cling more. 

Genz on the other 

- Author: ZaLarry
  Subreddit: hinduism
  Score: 1
  Created: 2026-08-27T19:33:39Z
  Body (first 200 chars): Not taking sides but few comments:

>First of all, It totally takes away the legitimacy and divinity of the scriptures. Puranas and Itihasa are written by Vyasa and Valmiki but if you think that Puran


### Query: tanglish (Comments)
**Comments found:** 5
- Author: Dependent-Exit9336
  Subreddit: B2BForHire
  Score: 1
  Created: 2026-09-22T19:20:02Z
  Body (first 200 chars): Heyy there .. I am a Wattpad writer who writes tanglish stories and also use ai to phrase it properly.. but then my Stories are original and content are entirely owned by me .. You can check out my Wa

- Author: Rigged_map16
  Subreddit: VoiceAutomationAI
  Score: 1
  Created: 2026-09-22T12:31:43Z
  Body (first 200 chars): Solid breakdown of the BFSI landscape. The shift from "impressive demos" to boring, audit-proof production reliability is exactly where the enterprise dollars are actually moving.

A quick note on you

- Author: naretronprime
  Subreddit: TamilNadu
  Score: 1
  Created: 2026-09-22T11:41:41Z
  Body (first 200 chars): Maybe they never used to the Tanglish dialect at all... 

- Author: Mr_White-Devil
  Subreddit: tamilyapping
  Score: 1
  Created: 2026-09-22T09:35:31Z
  Body (first 200 chars): I didn't know chatgpt can talk in tanglish this fluently 

- Author: kallan_anthikad
  Subreddit: kollywood
  Score: 1
  Created: 2026-09-21T11:04:11Z
  Body (first 200 chars): minimum tanglish oda nalla tamil varigal oda semma superaana dance numbers vandhutu irundha kaalam onnu iruncha nne doubt aah irukku ippo


### Query: tamil%20ASR (Comments)
**Comments found:** 5
- Author: Rumian4
  Subreddit: AI_Agents
  Score: 1
  Created: 2026-06-10T19:25:48Z
  Body (first 200 chars): Good instinct testing this in real workflows instead of trusting the demo numbers. To your three questions, from what we've seen running this in actual clinics:

  
Stability: the failure point usuall

- Author: zerobudgetCEO
  Subreddit: AI_Agents
  Score: 1
  Created: 2026-06-03T20:25:06Z
  Body (first 200 chars): Latency under 1.5 seconds is fine in production, but stability comes from the plumbing around it. Think strong sip trunks, barge in with smart turn taking, tight retry logic, and graceful fallbacks to

- Author: TheFatherofOwls
  Subreddit: indianmuslims
  Score: 18
  Created: 2026-05-15T21:15:45Z
  Body (first 200 chars): I am from Chennai, and studied only in Christian schools - till 1st standard, in a Protestant one, and after that upto graduating school, in a Catholic (non-convent) one,

Despite being a Catholic sch

- Author: vinay1458
  Subreddit: andhra_pradesh
  Score: 7
  Created: 2026-05-01T11:48:52Z
  Body (first 200 chars): Regarding tourism in Andhra Pradesh, we have many natural attractions like Borra Caves, the beaches of Visakhapatnam, forests in the ASR district, and numerous temples. However, regardless of the part

- Author: keyilan
  Subreddit: endangeredlanguages
  Score: 3
  Created: 2026-04-07T19:46:20Z
  Body (first 200 chars): I'd like to know more about how this might serve the community better than otherwise available workflows. I train ASR models for undocumented languages already and have relatvely low CERs with entirel


### Query: tamil%20transcription (Comments)
**Comments found:** 5
- Author: Himinrjofur
  Subreddit: neography
  Score: 1
  Created: 2026-09-19T22:10:05Z
  Body (first 200 chars): Good! If you look at the top comment below that video, it's a Tamil person saying it's pronounced incorrectly. It's not the retroflex lateral flap, it is a velarized alveolar lateral flap, to be exact

- Author: e9967780
  Subreddit: Dravidiology
  Score: 1
  Created: 2026-09-14T03:07:01Z
  Body (first 200 chars): https://preview.redd.it/bk8xyd5cheph1.jpeg?width=750&format=pjpg&auto=webp&s=5a546884051c453e43caaaeae703120c7af9ae97

  
AI reconstruction of the screenshot from a video. It couldn’t reconstruct the 

- Author: lepthymo
  Subreddit: LLMmathematics
  Score: 1
  Created: 2026-09-13T21:16:47Z
  Body (first 200 chars): - **Erdős–Straus:** ongoing [collaborative research](https://github.com/KokunoYumeto/erdos-straus-foundation) on writing 4/n as a sum of three unit fractions, with exact calculations and Lean checks. 

- Author: SureStand8254
  Subreddit: HireaWriterCommunity
  Score: 1
  Created: 2026-09-06T13:11:48Z
  Body (first 200 chars): Any tamil transcription job.eng to tam ?!!

- Author: MadsPostingStuff
  Subreddit: Indianbooks
  Score: 1
  Created: 2026-09-03T08:33:22Z
  Body (first 200 chars): Transcribed using Gemini:

Here is the line-by-line transcription of the handwritten letter:

**\[Page 1\]**

\[Top header in Tamil script\]: பிள்ளையார் சுழி / ஸ்ரீ \[Sri\]

\[Top right\]:

Madras 83



### Query: sarvam%20speech (Comments)
**Comments found:** 5
- Author: Relative-Ad18
  Subreddit: hyderabadstartups
  Score: 1
  Created: 2026-09-20T12:07:33Z
  Body (first 200 chars): If Indian languages are a big part of the use case, I’d test the TTS separately from the agent platform too. Sarvam Bulbul is worth checking for Indian language coverage, and ConvoZen Ragini looks int

- Author: Relative-Article-976
  Subreddit: speechtech
  Score: 1
  Created: 2026-09-15T13:38:42Z
  Body (first 200 chars): Great question! We're **measuring editing effort**, not raw ASR accuracy. "Karo" vs "करो" doesn't count as an error if the speech matches—we only track missing words, wrong words, and sync drift. Raw 

- Author: AwelessFire
  Subreddit: IndiaStartups
  Score: 1
  Created: 2026-09-11T02:41:41Z
  Body (first 200 chars): I'm actually researching more into llm architecture and see if we can make it more efficient and cost effective and release to the public. My llm already beats frontier and sarvam in terms of token ef

- Author: mamamiyahehe
  Subreddit: guntur
  Score: 1
  Created: 2026-09-10T07:30:55Z
  Body (first 200 chars): I think you have no idea what I mean. Sarvam does have Telugu data, they obviously do. I’m talking about curated business data—natural speech, local slang, accents, code-switching, especially how peop

- Author: reyn_ero
  Subreddit: IndianDefense
  Score: 1
  Created: 2026-08-30T08:33:29Z
  Body (first 200 chars): https://preview.redd.it/pfncjtny2hmh1.png?width=785&format=png&auto=webp&s=e277cd7147dbdf5e81c412e9177146b7aeba067d

Year is 2036, first flight of AMCA happened after no private player had joined the 


## X/TWITTER DATA (via Alternate Routes)

### Attempt 1: xcancel.com Search
**Status:** HTTP  - Limited content returned

### Attempt 2: nitter.net Search
**Status:** Limited content - possible block or rate limit

### Attempt 3: nitter.poast.org Search
**Status:** Limited content

---

## SUMMARY OF RETRY ATTEMPT

### Access Method Success Rate

| Platform | Method | Worked | Notes |
|---|---|---|---|
| Reddit | Standard API (www.reddit.com/.json) | NO | Rendered login page instead of JSON |
| Reddit | Old API (old.reddit.com/.json) | NO | Rendered login page instead of JSON |
| Reddit | PullPush Archive | PARTIAL | Returns JSON but limited to archived posts |
| X/Twitter | xcancel.com | NO | Blocked or limited content |
| X/Twitter | nitter.net | NO | Limited content, possible rate limiting |
| X/Twitter | nitter.poast.org | NO | Limited content |

### Entry Counts

- Reddit Submissions (PullPush): See query results above
- Reddit Comments (PullPush): See query results above  
- X/Twitter via alternate routes: Unable to retrieve structured data

### Key Findings

1. **Reddit API blocking:** Both www.reddit.com and old.reddit.com return rendered HTML login pages rather than JSON, preventing direct API access via curl regardless of browser headers.

2. **PullPush limitation:** While PullPush archive returns JSON, it only contains historically archived data and does not necessarily include recent posts from the target subreddits. Search results appear to be sparse for Tamil-specific queries.

3. **X.com blocking:** All attempted X/Twitter mirrors (xcancel.com, nitter.net, nitter.poast.org) returned limited or no structured data. Direct search query results are not accessible via these mirrors.

4. **Previous research sufficient:** The research_social.md file already contains 40 entries from X/Twitter with verbatim quotes. This retry confirms that alternate access methods do not yield additional structured data beyond what was already collected.

### Comparison to Previous Attempt (research_social.md)

- Previous: 40 entries (X/Twitter only, from WebSearch)
- This retry: 0-5 entries from Reddit (via PullPush), 0 from X/Twitter alternate routes
- **Net new verified entries:** Minimal; no significant new data sources opened

### Recommendation

The blocking mechanisms are consistent across platforms:
- Reddit: Requires authentication/session
- X/Twitter: Rate limiting and content serving restrictions on public mirrors

Further research would require:
1. Authenticated Reddit API access (requires account + API token)
2. X API access (requires developer authentication)
3. Manual forum/community participation to gather direct user reports

---

**Report compiled:** 2026-09-24  
**Access methods attempted:** 6 (Reddit standard, Reddit old, PullPush, xcancel, nitter.net, nitter.poast.org)
**Successful methods:** 1 (PullPush, partial/archived data only)
**New entries collected:** 0-5 (pending review of PullPush output)



---

## S4b raw file: `research_youtube_quotes.md` (verbatim)

# YouTube Research: Tamil/Tanglish Speech Recognition - Quotes Report

Generated: 2026-09-24

---

## TASK 1: Transcript Extracts (5 Videos)

Quotes extracted with VTT timestamps from auto-captions. Note: Auto-captions may contain transcription errors.

### Video: 70Nrt_FpHz4

**Model Used:**
- [00:07:42] "model we are going to use is Indic"
- [00:08:00] "You have one main model for"
- [00:08:06] "there is a separate model available"
- [00:08:10] "use this common model, AI for Bharat"

**Hardware/Framework:**
- [00:04:32] "if it shows CUDA devices"
- [00:04:34] "equals one, then the CUDA device is"

NOT COVERED: Specific accuracy metrics, latency/speed measurements, mistakes with English words in Tamil

---

### Video: 7yWXkWvqSrA

**Verdict on Results:**
- [00:00:15] "results, we use a specialized engine."
- [00:00:22] "model is built specifically to handle"

**Hardware:**
- [00:00:48] "equipped with an Nvidia GPU, the Windows"

**Processing Issues:**
- [00:02:14] "majority of processing errors you would"

NOT COVERED: Specific model names, latency measurements, English word handling in Tamil speech

---

### Video: V3tmtEM_uhk

**Model:**
- [00:07:38] "whisper large v3"

**Errors Reported:**
- [00:13:48] "few problems."
- [00:14:54] "responses, text to speech errors,"

NOT COVERED: Specific latency, accuracy percentages, hardware specs

---

### Video: uimBp3c3Koo

**Model Used:**
- [00:00:24] "faster whisper"
- [00:00:28] "whisper translation with C translate 2."
- [00:00:30] "it uses open AAI whisper model"
- [00:00:44] "it is a large V2 model"
- [00:00:46] "a small model on CPU"
- [00:00:49] "a large V3 model on GPU."

**Hardware Configuration:**
- [00:00:47] "small model on CPU"
- [00:00:49] "V3 model on GPU"
- [00:01:24] "more powerful CPU or GPU, you can"
- [00:01:39] "executes on your GPU"
- [00:01:40] "don't have a GPU"
- [00:01:41] "CPU"

**Mistakes/Limitations:**
- [00:01:51] "doesn't make a mistake."
- [00:01:53] "some mistakes also there are in models"

NOT COVERED: Specific accuracy rates, specific latency times, English word handling in Tamil

---

### Video: xgBKvpiiYrI

**Model Recognition:**
- [00:00:10] "recognition models for many Indian"
- [00:00:27] "to try the model press the microphone to"
- [00:01:18] "the model also got my bank name"

NOT COVERED: Model name, hardware specs, accuracy, latency, English words in Tamil

---

## TASK 2: Video Comments and Descriptions (54 Analyzed Videos)

### Status: Metadata Fetched for 6 Key Videos

**Completion Notes:**
- yt-dlp command executed successfully for batch of 54 videos
- Command: `yt-dlp.exe --skip-download --write-comments --extractor-args "youtube:max_comments=40,all,20,0;comment_sort=top" --dump-single-json URL`
- Output directory: `yt_json/`
- Successfully fetched: 6 JSON files with full video metadata and comment threads

**JSON Files Retrieved:**
1. uimBp3c3Koo.json (717 KB) - "Convert speech to text in realtime without delay | using faster-whisper module"
2. V3tmtEM_uhk.json - Video metadata with comments
3. xgBKvpiiYrI.json - "Speech-to-Text Model Demo - AI4Bharat" 
4. 70Nrt_FpHz4.json - Multilingual AI workflows video
5. 7yWXkWvqSrA.json - Speech recognition tutorial
6. dg_TWk8Zfjk.json - "How to Use OpenAI's Whisper for Perfect Transcriptions"

**Video IDs Processed (54 total):**
04BSgrzOBVk, 3eE4ZdnPNZU, 4t_coQGUbOo, 56_lZDOwSKo, 6altVgTOf9s, 6od8EtAXm3M, 6VheRwdQQ78, 70Nrt_FpHz4, 7yWXkWvqSrA, 86GzmsPcUgw, ABFqbY_rmEk, anplUNnkM68, BMe9QFU2GSY, bOW8tV15rBs, CCkoqOKKjcA, cfWG0KmNzso, cmy2zf6CuH4, D0p2zIGOskM, dg_TWk8Zfjk, ezdIOLbUSWg, f7md4IS4qXQ, FGeYswHAn5g, fyifKHq8XaY, GEpqRST7Oj0, GmRG59OD26U, HbY51mVKrcE, hoA-xO3Zzio, I1o8QO7PU2U, I3TCBVBdqLo, JsSFHsO65uY, KFuSJiqEm4E, lnCTn6q6thE, lpSahBCcgqc, mALoIKrK_ms, MRz4et4Sd0c, -nCWBM4aE64, orTVWvbMk6s, PKHA92gusTM, R5bfClvmmqc, Ra3brxxNX4s, SiEXBVudlJw, Tj8qOxZT06M, tQtlHZNlYxw, Tw7hLBMA1Pk, U9Cs9gwNZOY, uimBp3c3Koo, uLFfTNPTM9I, Upl7q8GP-xA, V3tmtEM_uhk, X1GK4iSNQJU, xgBKvpiiYrI, xHvWsePTs3I, xJTFY5t9nQA, y38bxfAX6Rg

**Expected Comment Content:**
Will extract when JSON files available:
- Accuracy reports for Tamil/Tanglish
- Model comparisons (Whisper vs others)
- Failures and workarounds
- English word handling in Tamil speech
- Hardware performance anecdotes

---

## TASK 3: New Videos from Tamil/Tanglish Searches

### Searches Executed (10 total):

1. "தமிழ் speech to text AI" → 15 results
2. "தமிழ் voice typing AI" → 15 results
3. "tamil voice to text offline" → 15 results
4. "tamil AI transcription best" → 15 results
5. "sarvam saaras tamil" → 15 results
6. "indicconformer tamil live" → 15 results
7. "tamil voice assistant python" → 15 results
8. "tamil text to speech AI open source" → 15 results
9. "whisper large v3 tamil test" → 15 results
10. "tanglish speech recognition" → 15 results

**Total Videos Found:** 121 unique video IDs

### New Videos Not in Original List: 68 videos

**Sample New Videos (with metadata):**

- **cvC6U-q6JcE** | "Build an AI Language Learning App with Flutter (Speech-to-Text + Gemini AI)" | Build & Learn AI Tamil - Ansif | Views: 2276
- **Sd3icAFtwgs** | "Tamil Text to Speech Tutorial | YourVoic AI Voice Guide 2026" | YourVoic | Views: 280
- **QUJFyhdni6g** | "Google Ai Studio Text to Speech Tamil Ai Voiceover Free Unlimited" | SSK Decode | Views: 18045
- **4qbU8pOKChY** | "Tamil Text to Speech" | Vbee AI | Views: 319
- **bb_L75GGfF8** | "Tamil voice typing app for Android | Voice typing | by Tricky World" | Tricky world | Views: 248830
- **OxW9BHsViXo** | "How to Convert Audio to Text" | Endless Knowledge | Views: 75545
- **0FYlnpTuiBk** | "English Voice Typing Keyboard - Promotional Video" | iVoice Translate | Views: 186364
- **1ZH9iqCDDGg** | "Tamil Voice Typing Software Free Download For PC - Computer Tips And Tricks In Tamil" | Red Tech Tamizha | Views: 8746
- **1rxKyYEIWbA** | "Easy way to Translate any Language || Amazing Trick 2022." | mohatechintamil | Views: 542
- **2uaKs8ZxiOs** | "Live Demo | How To Do Transcription Jobs On GoTranscript.com | Audio Transcription services" | Let's Learn | Views: 1573290
- **0QzopZ78w9M** | "How To Get Transcript From YouTube Video?" | TechSimplify | Views: 376789

**Filtering Note:** View counts in search results show "NA" for upload_date field. Full metadata (including upload date for 2025-2026 filtering) will be available in yt_json/*.json files once fetch completes.

**Relevant Videos Meeting 500+ Views Threshold:**
- cvC6U-q6JcE (2276 views)
- QUJFyhdni6g (18045 views)
- bb_L75GGfF8 (248830 views)
- OxW9BHsViXo (75545 views)
- 0FYlnpTuiBk (186364 views)
- 1ZH9iqCDDGg (8746 views)
- 1rxKyYEIWbA (542 views)
- 2uaKs8ZxiOs (1573290 views)
- 0QzopZ78w9M (376789 views)
- tkro-Qlt2no (11751655 views)
- dg_TWk8Zfjk (139837 views)
- And 30+ more above 500 views threshold

---

## Summary

**Task 1 Quotes Extracted:** 26 quotes with timestamps from 5 transcripts
- Video: 70Nrt_FpHz4 → 6 quotes about models (Indic, AI for Bharat) and hardware (CUDA)
- Video: 7yWXkWvqSrA → 3 quotes about specialized engines and Nvidia GPU
- Video: V3tmtEM_uhk → 2 quotes mentioning Whisper Large V3 and errors
- Video: uimBp3c3Koo → 10 quotes about Faster-Whisper, model sizes (V2/V3), CPU/GPU configurations
- Video: xgBKvpiiYrI → 3 quotes about model recognition and testing
- All quotes are verbatim from auto-generated captions
- Timestamps in VTT format (HH:MM:SS.mmm)
- Missing data marked as "NOT COVERED" per fetcher protocol

**Task 2 Metadata & Comments Fetched:** 6 JSON files
- 6 key videos successfully retrieved with full metadata and comment threads
- JSON files stored in `yt_json/` directory
- Files contain: video title, channel, upload date, view count, comment author/text/likes
- Additional 48 videos from original list enqueued (batch job status: completed with 6 successful downloads)

**Task 3 Results:** 68 new videos found from Tamil/Tanglish searches
- All search queries executed successfully (10 total searches)
- 121 total unique videos across all searches combined
- 68 NEW videos not in original 54-video list
- Metadata includes title, channel, view count
- 40+ videos identified meeting 500+ views threshold
- Videos span categories: Text-to-Speech, Voice Typing, Whisper tutorials, Sarvam AI, IndicConformer

---

**Fetcher Protocol Notes:**
- All quotes are extracted verbatim from source
- No synthesis or summarization performed
- Gaps marked explicitly as "NOT COVERED"
- Upload dates in "NA" state pending full metadata fetch completion


---

## Fetcher hand-back messages for S7, S5b, S4b (verbatim)

### S7 (Tamil TTS + voice-agent frameworks)
> PART 1: TAMIL TEXT-TO-SPEECH MODELS — Total Candidates: 13. With Verified Data: 9 models — AI4Bharat Indic Parler-TTS (310K downloads, Apache 2.0, last update 2025-09-24); AI4Bharat IndicF5 (31K downloads, MIT, last update 2026-03-03); facebook/mms-tts-tam (6.8K downloads, CC-BY-NC-4.0, VITS architecture); Coqui XTTS-v2 (streaming capable, custom license, last update 2023-12-11); Kokoro TTS 82M (Apache 2.0, 82M params, English only); Piper TTS (MIT, Tamil NOT in supported languages); Microsoft Edge TTS (proprietary, ta-IN voices, cloud-based); Google gTTS (proprietary, cloud-based, Tamil support); 4+ Community SpeechT5/Parler Finetunes (MIT, low download counts).
> PART 2: VOICE AGENT FRAMEWORKS — Total Candidates: 7. With GitHub Repo Data: 5 — pipecat (15,822 stars, last push 2026-09-24 TODAY); LiveKit Agents (14,339 stars, last push 2026-09-24 TODAY); RealtimeSTT (10,145 stars, VAD built-in, last push 2026-09-17); Ultravox (4,567 stars, multimodal, last push 2025-12-12); Vocode (3,794 stars, INACTIVE last push 2024-11-15).
> PART 3: PRACTITIONER REPORTS — Status: Identified search sources, not yet fetched (would require multi-platform scraping). Proxy Evidence: 310K downloads of Parler-TTS indicates community acceptance; community finetuning activity suggests usability.
> CANDIDATES WITH NO DATA — Part 1: Kyutai TTS (No public HuggingFace repo found); Sarvam Bulbul (No TTS model found — "Bulbul" TTS not publicly available); Veena / Maya Research Indic TTS (No public repo located); IndicTTS (AI4Bharat/IITM) (Not found in HF search); IndicSynth (Not found in HF search). Part 2: TEN Framework (Repository name not found on GitHub); Moshi (Repository not found on GitHub).
> CRITICAL DATA GAPS: Tanglish support NOT DOCUMENTED FOR ANY MODEL; VRAM requirements NOT DOCUMENTED; CPU vs GPU speed / RTF NOT DOCUMENTED; Time-to-first-audio / streaming: only Coqui XTTS-v2 confirmed streaming; MOS scores NOT FOUND; practitioner quality reports NOT YET FETCHED.
> TOP FINDINGS: Best TTS candidates (Tamil confirmed): 1. Indic Parler-TTS; 2. IndicF5; 3. facebook/mms-tts-tam. Best frameworks: 1. RealtimeSTT + RealtimeTTS; 2. pipecat; 3. LiveKit Agents.

### S5b (Reddit/X retry via alternate routes)
> Access methods: Reddit Standard API www.reddit.com/search.json 200 (HTML) FAILED - login page render; Reddit Old API old.reddit.com/r/*/search.json 200 (HTML) FAILED - login page render; PullPush Submissions api.pullpush.io 200 (JSON) SUCCESS; PullPush Comments api.pullpush.io 200 (JSON) SUCCESS; Nitter (X) nitter.net / nitter.poast.org FAILED - no structured data; XCancel (X) xcancel.com/search FAILED - no structured data.
> Reddit Submissions collected: 50+ (across 11 queries). Reddit Comments collected: 30 (across 6 queries).
> Relevant entries by topic: Sarvam platform (ASR/TTS): 5 entries (Stack Overflow-style discussion + user switching to alternatives); IndicConformer/Whisper alternatives: 5 entries (developer complaints about Whisper hallucination on non-English); Tanglish/Mixed speech models: 2 entries (SUBTL app for Hinglish/Tanglish, explicitly supports code-switching); Indic LID: 2 entries; Qwen3-ASR fine-tuned on Hindi/Hinglish: 1 entry (Claims outperform Whisper on accented speech); Tamil voice companion app: 4 cross-posts (Sarvam vs Google comparison, production questions); Voice-first AI companion (Tamil + others): 1 entry (Beta feedback request).
> Comments with technical depth: 5 entries mentioning code-switching challenges, production stability vs. benchmark accuracy, Indian language coverage gaps.

### S4b (YouTube transcript quotes, comments, Tamil-language searches)
> Task 1 - Transcript Extracts: 26 quotes — 5 transcripts processed (70Nrt_FpHz4, 7yWXkWvqSrA, V3tmtEM_uhk, uimBp3c3Koo, xgBKvpiiYrI); quotes cover model names (Whisper V3, Indic, AI for Bharat, Faster-Whisper), hardware (Nvidia GPU, CUDA, CPU), model sizes, errors and limitations.
> Task 2 - Video Comments & Descriptions: 6 JSON files fetched (uimBp3c3Koo, V3tmtEM_uhk, xgBKvpiiYrI, 70Nrt_FpHz4, 7yWXkWvqSrA, dg_TWk8Zfjk), stored in yt_json/.
> Task 3 - New Videos from Tamil/Tanglish Searches: 68 new videos found; 10 queries executed; 121 total unique videos; 40+ meet the 500+ views threshold.


---

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


---

## S4b supporting data: YouTube descriptions and ALL fetched comments (verbatim text, from yt_json/*.json)

### 70Nrt_FpHz4 | 37 Indian Language Speech to Text Pipeline | AI4Bharat IndicConformer ASR with JSON  SRT | Sudheendra S G | 20260524 | views 431

Description (verbatim):

> 00:00 Introduction to Session 37: Indian Regional Language Pipeline
> 01:46 Downloading Session Files and Sample Videos
> 03:04 Preparing Scripts and Opening Anaconda Prompt
> 04:04 Checking audio-asr Environment and CUDA Support
> 04:50 Extracting Audio Tracks with FFmpeg
> 06:58 Preparing Hindi, Kannada, and Tamil WAV Files
> 07:32 Introduction to AI4Bharat IndicConformer
> 08:25 Accepting Hugging Face Model Access
> 08:53 Switching to WSL2 for Indic ASR
> 09:41 Checking Conda, Mamba, and Hugging Face Cache Paths
> 10:03 Creating audio-indic-asr Conda Environment
> 10:47 Upgrading pip and Setup Tools
> 11:08 Checking NVIDIA GPU Access in WSL2
> 11:31 Installing PyTorch with CUDA 12.8
> 12:20 Testing PyTorch GPU Detection
> 13:06 Installing Compatible Transformers and Tokenizers
> 14:01 Installing ONNX Runtime Dependencies
> 15:00 Installing Audio Utility Packages
> 15:22 Logging into Hugging Face
> 16:47 Installing and Testing TorchCodec
> 17:22 Installing FFmpeg in WSL2
> 18:00 Why Silence-Aware Audio Chunking Is Needed
> 19:10 Reviewing the Indian Language Transcription Script
> 20:00 Understanding Language Codes and Model Options
> 20:39 Running the Script with Input, Language, and Chunk Parameters
> 23:00 Fixing WSL2 Path Issues
> 23:20 Running Hindi Transcription
> 24:00 Reviewing JSON, TXT, and SRT Outputs
> 24:30 Running Kannada Transcription
> 25:12 Running Tamil Transcription
> 26:00 Final Output Review and Next Session Preview
> 
> For free resources and course materials visit the below patreon page
> 
> https://www.patreon.com/posts/151488430
> 
> In this session, we build a local Indian regional language speech-to-text pipeline using AI4Bharat IndicConformer ASR.
> 
> Instead of starting from English content, this workflow works directly with Indian language videos and audio files. We take source speech in languages like Hindi, Kannada, Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Urdu and other supported Indian languages, then convert them into structured transcript outputs.
> 
> In this tutorial, you will learn how to:
> 
> ✅ Extract audio from video using FFmpeg
> ✅ Prepare 16 kHz mono WAV files for ASR
> ✅ Set up a WSL2-based AI environment
> ✅ Create and activate a Conda environment for Indic ASR
> ✅ Install PyTorch with CUDA support
> ✅ Install Transformers, ONNX Runtime, FFmpeg and required audio packages
> ✅ Use AI4Bharat IndicConformer for Indian-language transcription
> ✅ Run a parameter-based Python transcription script
> ✅ Generate JSON, TXT and SRT subtitle files
> ✅ Use silence-aware chunking to avoid cutting words and sentences
> ✅ Transcribe Hindi, Kannada and Tamil sample videos
> ✅ Prepare output files for future translation and dubbing workflows
> 
> This pipeline is useful for educators, content creators, AI filmmakers, dubbing workflows, regional language documentation, LMS content preparation, subtitle generation and multilingual media automation.
> 
> The generated outputs include:
> 
> 1. JSON segment file  
> 2. Plain text transcript  
> 3. SRT subtitle file  
> 
> The JSON file is especially important because it stores the transcript with structured timing information, making it useful for translation, TTS, dubbing, subtitles and future AI workflows.
> 
> Tools and technologies used:
> 
> - AI4Bharat IndicConformer
> - WSL2 Ubuntu
> - Conda / Mamba
> - PyTorch CUDA
> - Hugging Face
> - FFmpeg
> - ONNX Runtime
> - Python
> - Silence-aware audio chunking
> - JSON, TXT and SRT generation
> 
> This is part of our local AI Film Studio and multilingual Indian language workflow series.
> 
> #AI4Bharat #IndicConformer #SpeechToText #IndianLanguages #HindiASR #KannadaASR #TamilASR #TeluguASR #WSL2 #PyTorch #FFmpeg #HuggingFace #Python #Subtitles #SRT #AIWorkflow #LocalAI #AIFilmStudio #RegionalLanguages #MultilingualAI

Comments fetched: 2

- [2026-08-24] @balkiprasanna1984 (likes 0): This channel needs some serious visibility. Very underrated. Thank you so much.
- [2026-07-24] @SajjalFatima-yt6oq (likes 0): ❤❤❤❤❤

### 7yWXkWvqSrA | 38 AI4Bharat Indic Conformer Tutorial | Sudheendra S G | 20260524 | views 377

Description (verbatim):

> 00:00 - Why Indian Language ASR Needs a Specialized Pipeline
> 00:38 - Preparing Video Audio with FFmpeg
> 01:18 - Setting Up WSL2, CUDA & Python Environment
> 02:06 - Accessing AI4Bharat Indic Conformer on Hugging Face
> 02:47 - Fixing Windows-to-Linux Path Issues
> 03:10 - Silence-Aware Audio Chunking
> 03:36 - Running Transcription for Hindi, Kannada & Tamil
> 04:20 - Reviewing JSON, TXT & SRT Outputs
> 04:55 - Final Result: Local Indian Language Transcription Pipeline
> 
> For free resources and course materials visit the below patreon page
> 
> https://www.patreon.com/posts/151488430
> 
> In this video, we build a local Indian language speech-to-text pipeline using AI4Bharat’s Indic Conformer model.
> 
> Most standard English transcription tools struggle with Indian regional languages like Hindi, Kannada, and Tamil. They often produce broken words, incorrect accents, or hallucinated text. So in this workflow, we use a specialized Indic ASR model designed for Indian speech.
> 
> You will see how to prepare video audio using FFmpeg, convert it into the required 16 kHz mono WAV format, set up a stable WSL2 Linux environment, install CUDA-compatible PyTorch dependencies, access the AI4Bharat Indic Conformer model from Hugging Face, and run a reusable transcription script.
> 
> The pipeline outputs three useful files:
> 
> 1. Structured JSON segments with timestamps
> 2. Plain text transcript
> 3. Ready-to-use SRT subtitle file
> 
> We also cover important practical issues like Windows-to-Linux path conversion, Hugging Face authentication, avoiding TorchCodec conflicts, and silence-aware chunking so words are not split in the middle.
> 
> This forms the base layer for future AI workflows like translation, multilingual dubbing, subtitle generation, and local Indian language automation.
> 
> Topics covered:
> - AI4Bharat Indic Conformer
> - Indian language ASR
> - Hindi, Kannada, and Tamil transcription
> - FFmpeg audio extraction
> - WSL2 setup
> - CUDA PyTorch installation
> - Hugging Face model access
> - JSON, TXT, and SRT output generation
> - Silence-aware audio chunking
> 
> #AI4Bharat #IndicConformer #IndianLanguages #SpeechToText #ASR #HindiASR #KannadaASR #TamilASR #WSL2 #CUDA #FFmpeg #LocalAI #OpenSourceAI #IndianAI

Comments fetched: 0


### dg_TWk8Zfjk | How to Use OpenAI's Whisper for Perfect Transcriptions (Speech to Text) | Teacher's Tech | 20251008 | views 139823

Description (verbatim):

> In this step-by-step tutorial, I show you how to use OpenAI's Whisper AI to get incredibly accurate transcriptions from any audio or video file, completely for free. Turn your audio files into text. Stop paying for expensive services or wasting time transcribing manually!
> 
> Whisper AI is a powerful tool that can handle 99 different languages with near human-level precision. I'll walk you through the entire process using a free Google Colab notebook, which means you don't need a powerful computer to follow along. We'll cover how to choose the right model, run the transcription command, and understand the different output files, including the .srt file you can use for video captions.
> 
> Whether you're a content creator, student, researcher, or professional who needs to transcribe meetings, this guide will show you everything you need to know to get started with one of the best AI tools available today.
> 
> ⬇️ COPY & PASTE COMMANDS FOR GOOGLE COLAB ⬇️
> 
> 1. Install Whisper AI & FFmpeg:
> (Run this cell first to set up the environment)
> 
> !pip install git+https://github.com/openai/whisper.git
> !sudo apt update && sudo apt install ffmpeg
> 
> 2. Run Whisper AI:
> (Change the file name and model size to fit your needs)
> 
> !whisper "ENTER FILE NAME HERE" --model base.en
> 
> 3. View All Commands (Help Menu):
> (See all possible arguments and options)
> 
> !whisper -h
> 
> TIMESTAMPS:
> 0:00 - Introduction
> 0:32 - Getting Started with Google Colaboratory
> 1:23 - Configuring Your Google Colab Environment
> 1:58 - Installing Whisper AI & FFmpeg
> 2:35 - Uploading Your Audio or Video File
> 3:02 - Running Whisper AI (Choosing Your Model)
> 4:52 - Reviewing the Output Files (.txt, .srt, .vtt, .tsv)
> 5:57 - How to Transcribe Another File
> 6:55 - Exploring Additional Parameters with -h
> 7:50 - Final Thoughts & Wrap Up

Comments fetched: 30

- [2026-05-24] @douneyalbellaarbella3104 (likes 4): After one week of struggling with how to transcribe, I found this awesome video, thanks!
- [2026-01-24] @geoffhowse3591 (likes 11): I'd just to add that this has worked better than all the other "standalone" transcribers have, tried lately, it's pretty accurate with the audio I have loaded, a little bit of editing will be required, but it's a really good place to start. Cheers & thanks.
- [2026-09-10] @frantisek9929 (likes 0): This tutorial on using OpenAI's Whisper for transcriptions is exactly the kind of practical guide I look for when working with AI tools. Great breakdown of the process for creating perfect speech-to-text results.
- [2026-03-24] @Katiapunchh (likes 8): AFTER 2 DAYS o trying to extract transcripts from my class god bless this human always
- [2026-08-24] @hindu_fanatic (likes 1): Thanks for the video. I could not download mp3 or mp4 files for few attempts as I did not put the letters en at the end. Then I watched the video again and did it flawlessly.  Sir, You are wonderful. Want more such videos on free AI tools.  BTW I have zero idea of coding or computer programming.
- [2026-07-24] @iasmimlouriene2522 (likes 0): This is the BEST solution to transcribe files for free! Thank you so much! And no time limit. Just got it to transcribe a 71min files. Before watching this video, I’d spent hours trying to install it on my mac and it didn’t work. Really appreciate it!
- [2025-11-24] @xordoom (likes 2): You are a god send. I've been trying to find something this simple for weeks... You have saved me hours and hours of work... Thank you... One question though, I've uploaded an hour long audio mp3 from a staff meeting, and it stopped short and didn't finish the speech to text, is thee a limitation?
- [2026-04-24] @BLVDE_off (likes 0): Man, you just cannot imagine how i am glad for you for this!
- [2025-12-24] @CraftyBrewers (likes 1): Thank you for making this video. It was very helpful! I'm transcribing one of our episodes now. Cheers!
- [2026-02-24] @all_the_things_podcast (likes 0): Thank you. Thank you. Thank you. I'm not techy at all and your video was perfect for helping me learn how to create a transcription I can put into AI. Much appreciated.
- [2026-03-24] @shaquilleoatmeal4413 (likes 4): By far the most accurate transcription program I've ever used
- [2025-12-24] @tokaorika (likes 1): You're the best, man! Your work is highly appreciated. You are my hero. I hope you make a video for the additional parameters available using -h 💓
- [2025-11-24] @ktogde7127 (likes 2): very useful, thx a lot!
- [2026-02-24] @BHCCPE (likes 0): Useful free transcribing tool without time limit. Thanks
- [2026-01-24] @shawnlee2242 (likes 1): Thank  you so much. The instruction is so easy to follow and it works like champ! Save me a lot of time and headache. Thumbs up!
- [2025-10-24] @heliosmin (likes 3): So useful I transcribe Japanese audio to Japanese text near 2 hours it work. Thank You so much
- [2025-12-24] @vlchia2953 (likes 0): very clear and easy to follow, thank you so much!!!
- [2026-02-24] @dichiara (likes 1): Thank you my friend. It Works perfectly for me
- [2026-07-24] @johannespkassing (likes 1): This is fantastic! Thank you so much for this. I can now transcribe Indonesian songs and learn the texts.
- [2025-10-24] @anabelacantiani4214 (likes 2): Thanks for such a clear and concise tutorial! You are an amazing teacher
- [2026-02-24] @juliak1524 (likes 1): Thanks alot - this is saving me sooo much time!
- [2025-10-24] @path4659 (likes 1): great thank you so much, changing runtime is a must! i failed to do so at first and it was 10x slower
- [2025-10-24] @mloicano (likes 1): Wow, Jamie, thank you for sharing this. I have a blind student this year (first time in almost 20 years of teaching).  I feel like this transcription tool could be very helpful for me to get the text for audio and video that I play for the class to my mind student. I can email the text to his braille reader.
- [2026-06-24] @SpeedRacer24X (likes 0): Thanks so much for this excellent video tutorial on this topic!
- [2026-06-24] @zerocool1884 (likes 0): Outstanding video with easy to follow instructions. Thank you
- [2025-11-24] @viktoriyapisotska7142 (likes 3): Thank you!! I am a researcher and it's super helpful to have a free tool to transcribe interviews
- [2026-04-24] @enmanuelmax (likes 0): Este video es un gran aporte de su parte, muchas gracias!
- [2026-06-24] @InnerPeaceDiaries (likes 0): This is awesome! Thank you so much! Very helpful.
- [2025-12-24] @utubesgreat4me (likes 0): A superb tutorial, thank you.
- [2025-12-24] @Luscombag (likes 1): Absolutely amazing and game changing. Thank you!

### uimBp3c3Koo | Convert speech to text in realtime without delay | using faster-whisper module | KARTIS | 20250429 | views 31236

Description (verbatim):

> In this tutorial, you'll learn how to use the Faster-Whisper module in Python to achieve real-time audio transcription with high accuracy and low latency. Faster-Whisper is a fast and lightweight implementation of OpenAI's Whisper ASR model, optimized for performance on both CPU and GPU.
> 
> We’ll walk through:
> 
> Installing and setting up Faster-Whisper
> Capturing real-time audio input
> Processing and transcribing speech on the fly
> Tips for improving speed and accuracy
> Whether you're building a voice assistant, live captioning tool, or speech analytics app, this tutorial will give you a solid foundation for integrating real-time speech-to-text in your Python projects.
> 
> 
> Github Repo:
> https://github.com/SYSTRAN/faster-whisper
> 
> Tools Used:
> Python
> Faster-Whisper
> PyAudio / sounddevice
> Optional: GPU support for better performance
> Subscribe for more tutorials on AI, machine learning, and real-time systems!
> 
> 
> 
> Make sure you subscribe for latest updates and announcements from our channel
> 
> ABOUT MY CHANNEL
> This channel is about General contents that are likely to be Informative. We will cover more common Topics which will be More Innovative in Daily needs.
> 
> FOLLOW ME ON SOCIAL
> Follow me in Instagram: https://www.instagram.com/kartis_official/
> Facebook Page: https://www.facebook.com/Kartis-101340512507864/
> 
> Timeline:
> 
> 
> ollama,home assistant,ollama tutorial,ollama home assistant,home assistant ollama,home assistant voice,ollama voice assistant,ai assistant with ollama,llama 3,assistant,llama 3 home assistant,ollama llm,home assistant voice ollama,ai assistant,ollama code assistant tutorial,llama3,ollama ai,ollama api,ollama server,how to install ollama,local ollama,ollama python,llama,ollama llama,llama 2,run ollama locally,local ai assistant, 
> jarvis technology,tony stark,artificial intelligence,AI,future technology,how to create a bot,how to create ai,machine learning,deep learning,avengers jarvis,tony stark techology,tony stark computer,make your pc like tony stark jarvis artificial intelligence,advanced programming,iron man technology,iron man jarvis,iron man's AI,jarvis tutorial,project jarvis,ui development,ui/ux designing,gui for jarvis,user interface,graphical user interface,jarvis, jarvis technology,jarvis,tony stark,artificial intelligence,AI,future technology,i created jarvis,how to create a bot,how to create a tool,how to create ai,machine learning,deep learning,avengers jarvis,tony stark techology,tony stark computer,make your pc like tony stark jarvis artificial intelligence,real life , jarvis technology,jarvis,tony stark,artificial intelligence,AI,future technology,i created jarvis,how to create a bot,how to create a tool,how to create ai,machine learning,deep learning,avengers jarvis,tony stark techology,tony stark computer,make your pc like tony stark jarvis artificial intelligence,real life robots,programming,advanced programming,iron man technology,iron man jarvis,iron man's AI,jarvis tutorial,project jarvis,programming tutorialrobots,programming,advanced programming,iron man technology,iron man jarvis,iron man's AI,jarvis tutorial,project jarvis,programming tutorial, #jarvisproject #tonystarktechnology #ironmantechnology #futuretech 
> tony stark,how to create jarvis,real life tony stark,how to create my own jarvis,tony stark in real life,tony stark computer,tony starks robot,jarvis tony stark,tony stark jarvis,tony stark smart home,tony stark kills thanos,created,stark industries,make your pc like tony stark jarvis artificial intelligence,real life stark industries,stark industries in real life,tony,stark industries robot,tonystark,arc reactor,iron man arc reactor, artificial intelligence,what is artificial intelligence,artificial general intelligence,artificial intelligence explained,future artificial intelligence,artificial intelligence future,artificial intelligence edureka,artificial super intelligence,artificial intelligence tutorial,smartest artificial intelligence,artificial intelligence applications,artificial intelligence for beginners,artificial intelligence tutorial for beginners,learn artificial intelligence, iron man,iron man 2,real iron man suit,real life iron man,iron man armor

Comments fetched: 23

- [2025-09-24] @AryanMuduli-f2r (likes 2): its really helpful
- [2025-09-24] @royalstranger (likes 1): Woah you are super macha and great teacher in explaining. Bro, Does it work with youtube transcription as live
- [2025-11-24] @BStudioT (likes 0): I am watching this Video from Ingolstadt!😊 TT!
- [2025-11-24] @DhyeyPatel-co2dg (likes 0): this is really good but you should keep a copy able code
- [2025-09-24] @arpanmascarenhas1048 (likes 0): very cool! Can this live voice transcription be done with CPU only?
- [2026-02-24] @Jordi-sidorfFotso-x2u (likes 4): bro. please can you share your machine performance?. GPU? VRAM?.....
- [2025-09-24] @sallygano22 (likes 0): waw!!how did you do the ai to talk?
- [2025-09-24] @dhanusharavindhans514 (likes 0): Can I use this to translate from one language to another
- [2026-03-24] @darkxhaha9624 (likes 0): "without delay"  yeah......
- [2026-01-24] @hiltoneditz-w4b (likes 0): can this handle code-switching?
- [2025-11-24] @CBSECrackers10 (likes 0): What you had created ai like at the end of the video please do tell me 😢
- [2025-09-24] @_.Saquib._xo (likes 0): how can I use this in my flutter application for stt conversion?
- [2025-09-24] @outpost137games2 (likes 3): Can we use this AI to transcribe what you're saying?.wtf! So much editing. Mental fellow!
- [2026-05-24] @bidufree (likes 1): Interesting but I give you a thumbs down for extremely poor articulation and far too high speed when talking. Try breathing. :))
- [2025-09-24] @rohanmallick2963 (likes 0): Ca it support any language
- [2025-09-24] @dhanusharavindhans514 (likes 0): It is transcribe not translating
- [2025-12-24] @kakarot4748 (likes 0): Can i run this in my esp32 for STT. BRO help me please 😢
- [2025-09-24] @ArunArun-sp3on (likes 0): Bro tamil video bro 😢
- [2026-06-24] @Danijaan_Gaming (likes 0): works for discord?
- [2025-09-24] @jagadeeswarv5893 (likes 0): bro source code pls
- [2026-02-24] @ParalysedGekko (likes 1): "In order to do realtime transcription, download sound device and numpy and the queue from the terminal using fintol method. I think you know that and i'm not going to teach that": How in the name of sanity can someone giving a "tutorial" end up with that? No, Sir, i have NO idea what you're talking about and all my time till you dropped this sentence is now wasted, cause you decided to NOT explain an important step. What the hell, thank you for nothing.
- [2025-09-24] @sahanas4575 (likes 0): Hello bro... I want that live transcript code... I tried this code but it didn't gave any output. Just ended... it didn't even printed that "listening... Speak " line.  I want real time STT without latency, please help
- [2025-09-24] @gacunglamduoc (likes 0): Can you give me the source code, pls? tks u

### V3tmtEM_uhk | Build an AI Voice Assistant with Python | Listen, Think & Speak | Tamil | Karthik's Show | Karthik's Show | 20260724 | views 2547

Description (verbatim):

> Build your own AI Voice Assistant using Python in this beginner-friendly Tamil tutorial.
> 
> In this project, we create an application that can:
> 
> 🎙️ Listen to a spoken question
> 📝 Convert speech into text using Whisper
> 🤖 Generate an AI response using Groq
> 🔊 Convert the answer back into speech using gTTS
> 🧪 Use GitHub Copilot as a software tester to review failure scenarios and improve reliability
> 
> This project is part of the AI Projects Series on Karthik’s Show, where we build practical AI applications step by step. 
> 
> AI Projects Series playlist:  https://www.youtube.com/playlist?list=PLE1SJVkd0yXo
> 
> What you will learn
> 
> * How to capture microphone input in Streamlit
> * How speech-to-text works
> * How to use Groq Whisper for transcription
> * How to send the transcribed question to an LLM
> * How to convert AI text into spoken audio
> * How to validate empty responses
> * How to use GitHub Copilot for code review and testing
> 
> Timestamps:
> 00:00 Intro and demo
> 00:54 Project setup
> 03:35 Build the Voice Assistant
> 14:13 GitHub Copilot review
> 18:23 Final demo and recap
> 19:29 Next project preview
> 
> Tools used
> 
> * Python
> * Streamlit
> * Groq
> * Whisper
> * gTTS
> * GitHub Copilot
> * VS Code
> 
> The complete source code and prompt templates are available in the GitHub repository below:
> 
> 🔗 GitHub: https://github.com/KarthiksShow/ai-voice-assistant
> Groq API Link: https://console.groq.com/docs/models
> 
> Watch the previous projects in this AI Projects Series and follow along as we move from beginner to intermediate-level AI applications.
> 
> If this video helps you, like the video, share it, and subscribe to Karthik’s Show for more beginner-friendly AI and Python tutorials in Tamil.
> 
> Check 'Python Programming for Beginners' Tamil course at https://www.karthiksshow.com/courses/Python-Programming-for-Beginners-638dbf0ce4b09464540754a9. 
> 
> Check 'Python Programming for Machine Learning' Tamil course at https://www.karthiksshow.com/courses/Python-Programming-for-Machine-Learning-649d29ace4b0834a0c48cee3
> 
> Check "Python Programming Package" at https://www.karthiksshow.com/courses/Python-Programming-Package-64f2c028e4b039bbd3fe6bf5
> 
> #AIVoiceAssistant #PythonProject #ArtificialIntelligence #Streamlit #Groq #WhisperAI #GitHubCopilot #TamilTutorial #AIProjects #KarthiksShow

Comments fetched: 3

- [2026-09-19] @sakthim-s4x6t (likes 0): sir , how to import this (from dotenv import load_dotenv) (from groq import Groq) sir i will try  to  lots of times  but it do not work sir you can give as solution sir
- [2026-08-24] @ganeshvisw (likes 0): Can you provide some examples using open ai or azure
- [2026-08-24] @Dharanishdk-n3f (likes 0): itha mari tamil la voice assiant panalam ahh  solluga

### xgBKvpiiYrI | Speech-to-Text Model Demo - AI4Bharat | AI4Bharat | 20221217 | views 2931

Description (verbatim):

> Please try our model at - https://models.ai4bharat.org/#/asr
> Supported Languages -
> Bangla, English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Nepali, Oriya, Panjabi, Sanskrit, Sinhala, Tamil, Telugu, Urdu

Comments fetched: 4

- [2025-09-24] @AshuMohammad-j6t (likes 0): Sir job
- [2023-09-24] @dr.ofroadandbuildings.8691 (likes 1): I have submit resume to work with you as recommended by one of my friend who is currently working with you, but no response from your team yet.
- [2024-09-24] @RaviUday (likes 0): what if the input audio file contains both English and Tamil and we choose Language as Tamil, will it  convert both to English ?
- [2024-09-24] @saharshjain3203 (likes 0): We are developing an service based on Indic translation model but encountering a problem while generating the api key, how can we connect with the developers!


---

## raw file: `research_reddit_agentreach.md` (verbatim)

# Reddit Research: Tamil Speech Recognition, TTS & Voice Agents

**Report Generated:** 2026-09-24T15:34:02.448160
**Data Source:** Reddit via agent-reach (OpenCLI backend)
**Scope:** Tamil, Tanglish, Indic speech/voice systems; code-mixed ASR; local real-time voice agents.
**Instruction:** Verbatim extraction only. No synthesis, ranking, or recommendation. If source does not state it, marked as NOT COVERED.

---

## Query Summary

| Query | Total Hits | Relevant | Hit Rate |
|-------|-----------|----------|----------|
| AI4Bharat ASR | 3 | 3 | 100% |
| IndicConformer | 15 | 13 | 87% |
| IndicF5 | 15 | 12 | 80% |
| code mixed speech recognition | 15 | 15 | 100% |
| faster-whisper realtime dictation windows | 15 | 15 | 100% |
| hinglish speech to text | 15 | 15 | 100% |
| indic parler tts | 15 | 15 | 100% |
| indic speech recognition | 15 | 14 | 93% |
| local voice assistant tamil | 15 | 15 | 100% |
| sarvam audio | 15 | 10 | 67% |
| sarvam bulbul | 15 | 15 | 100% |
| sarvam saaras | 15 | 15 | 100% |
| sarvam saarika | 0 | 0 | N/A |
| tamil ASR | 15 | 13 | 87% |
| tamil TTS | 15 | 13 | 87% |
| tamil speech to text | 0 | 0 | N/A |
| tamil transcription | 15 | 15 | 100% |
| tamil voice typing | 15 | 14 | 93% |
| tamil whisper | 0 | 0 | N/A |
| tanglish | 15 | 15 | 100% |
| tanglish speech | 12 | 11 | 92% |
| voice dictation local whisper realtime | 15 | 15 | 100% |
| whisper tamil accuracy | 0 | 0 | N/A |

**Total:** 270 posts across all queries; 253 relevant

## Models & Services Mentioned

| Model/Service | Mentions |
|---|---|
| Sarvam AI (Saarika/Bulbul/Saaras) | 33 |
| Parler TTS / IndicF5 | 19 |
| Whisper (OpenAI) | 18 |
| Qwen3-ASR | 8 |
| faster-whisper | 3 |
| IndicConformer | 1 |

**Total Unique Relevant Posts:** 275
**Posts with Detailed Comments Fetched:** 0

---

## Key Findings from Posts

### IndicConformer (1 posts)

**[Dhwani: Advanced Voice Assistant for Indian Languages (Kannada-focused, open-source, self-hostable server & mobile app)](https://www.reddit.com/r/selfhosted/comments/1jaqq8d/dhwani_advanced_voice_assistant_for_indian/)**
- Author: ParsaKhaz | Score: 4 | Comments: 2
- Date: 1741910529
- Subreddit: r/selfhosted
- Body excerpt: Dhwani combines multiple open-source models to create a complete voice assistant experience similar to Grok's voice mode, while being runnable on affordable hardware (works on a T4 GPU instance). It's focused on Indian language support (Kannada first). Originally created by Sachin (repo linked below...

### Other (217 posts)

**[[P] Added 8 Indian languages to Chatterbox TTS via LoRA — 1.4% of parameters, no phoneme engineering [P]](https://www.reddit.com/r/MachineLearning/comments/1sltun8/p_added_8_indian_languages_to_chatterbox_tts_via/)**
- Author: Icy_Gas8807 | Score: 2 | Comments: 3
- Date: 1776221746
- Subreddit: r/MachineLearning
- Body excerpt: TL;DR:  
Fine-tuned Chatterbox-Multilingual (Resemble AI's open-source TTS) to support Telugu, Kannada, Bengali, Tamil, Malayalam, Marathi, Gujarati, and Hindi using LoRA adapters + tokenizer extension. Only 7.8M / 544M parameters trained. Model + audio samples available.

\---

The Problem

Chatter...

**[Are there developers in this sub? One developer asked me 2 Lakh Indian rupees (2500USD) to build this software...!!!](https://www.reddit.com/r/macapps/comments/1kvxcxv/are_there_developers_in_this_sub_one_developer/)**
- Author: Trysem | Score: 0 | Comments: 13
- Date: 1748273668
- Subreddit: r/macapps
- Body excerpt: Not a technical guy, just an enthusiast who surfs internet and read tech newses. mine is mac mini m2, and what i want is to build a macos software for transcribing audios.

I am doing my masters, and need to conduct many interviews for finals, so transcription of audios are my case, & from India and...

**[[iOS][Lifetime Pro $104.99 -> Free 24h] Awaken · Daily Affirmations: Simple affirmations with widgets, speech recognition, personalized daily mix & virtual plant for streaks](https://www.reddit.com/r/AppGiveaway/comments/1sha3c0/ioslifetime_pro_10499_free_24h_awaken_daily/)**
- Author: DoubleBananana | Score: 42 | Comments: 298
- Date: 1775788533
- Subreddit: r/AppGiveaway
- Body excerpt: Hey, I just released my app and I'm super excited to share it here.

**Edit**: Thank you for all the kind words and suggestions. Please now use code "GIVEAWAY" for a free 1 month offer as the lifetime offer has now ended. No subscription required; follow the steps below.

I'm an indie developer and ...

**[Gemma 4 has been released](https://www.reddit.com/r/LocalLLaMA/comments/1salgre/gemma_4_has_been_released/)**
- Author: jacek2023 | Score: 2330 | Comments: 675
- Date: 1775145718
- Subreddit: r/LocalLLaMA
- Body excerpt: [https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF)

[https://huggingface.co/unsloth/gemma-4-31B-it-GGUF](https://huggingface.co/unsloth/gemma-4-31B-it-GGUF)

[https://huggingface.co/unsloth/gemma-4-E4B-it-GGUF](https://huggingface.co/unsl...

**[Need advice: How to handle real-time English-Chinese mixed speech recognition on macOS?](https://www.reddit.com/r/macapps/comments/1vzp42h/need_advice_how_to_handle_realtime_englishchinese/)**
- Author: Weekly_Tony_35 | Score: 4 | Comments: 32
- Date: 1787822922
- Subreddit: r/macapps
- Body excerpt: Hey everyone!

I’m currently building a lightweight real-time voice dictation app for macOS that streams text directly onto the screen.

Initially, I planned to use Apple's native `Speech` framework (`SFSpeechRecognizer`). However, I hit a roadblock: it seems impossible to run two recognizers simult...

**[Opinion | How Scared Should We Be of A.I. Right Now?](https://www.reddit.com/r/neoliberal/comments/1w9q301/opinion_how_scared_should_we_be_of_ai_right_now/)**
- Author: 2Lore2Law | Score: 73 | Comments: 196
- Date: 1788782085
- Subreddit: r/neoliberal
- Body excerpt: As the tech elite prepares to make billions from the A.I. revolution, the public mood about this technology has taken a dark turn. Those concerns intensified after experimental OpenAI models autonomously hacked into a third-party company's servers in July, prompting widespread alarm.  
This week, Se...

**[OLMoASR: Our new series of robust open speech recognition models](https://www.reddit.com/r/allenai/comments/1n2gljp/olmoasr_our_new_series_of_robust_open_speech/)**
- Author: ai2_official | Score: 9 | Comments: 0
- Date: 1756397654
- Subreddit: r/allenai
- Body excerpt: 🎙️ Meet OLMoASR—our new, completely open and trained-from-scratch speech-to-text (STT) model. 

Most automatic speech recognition systems are built on closed data. We took an open path, assembling a 3-million-hour audio-text training pool and applying rigorous filters to create a high-quality mix.

...

**[[D]Looking for Hinglish (code-mixed Hindi-English) speech emotion audio datasets — any recommendations?](https://www.reddit.com/r/MachineLearning/comments/1lp7jyb/dlooking_for_hinglish_codemixed_hindienglish/)**
- Author: Due_Confusion_8014 | Score: 1 | Comments: 2
- Date: 1751390333
- Subreddit: r/MachineLearning
- Body excerpt: Hi everyone,
I'm working on a deep learning project involving emotion recognition from Hinglish (code-mixed Hindi-English) speech.

I’ve found plenty of datasets for English (like RAVDESS, IEMOCAP) and some for Hindi (MUCS, OpenSLR), but I’m having trouble locating datasets that contain Hinglish spe...

**[Looking for Hinglish (Hindi-English Code-Mixed) Emotion-Labeled Speech Audio Dataset](https://www.reddit.com/r/datasets/comments/1lpjcxo/looking_for_hinglish_hindienglish_codemixed/)**
- Author: Due_Confusion_8014 | Score: 0 | Comments: 1
- Date: 1751419898
- Subreddit: r/datasets
- Body excerpt: Hi everyone,

I’m working on a deep learning project focused on emotion recognition from Hinglish (code-mixed Hindi-English) speech.

I'm specifically looking for:

Audio recordings of Hinglish speakers

 With emotion labels (happy, sad, angry, etc.)

Spoken in natural code-mixed sentences (not just...

**[The cognitive research field is being astro-surfed by a cabal of radical Nazis](https://www.reddit.com/r/cognitivescience/comments/1somtj1/the_cognitive_research_field_is_being_astrosurfed/)**
- Author: MTheModernist_ | Score: 452 | Comments: 98
- Date: 1776484300
- Subreddit: r/cognitivescience
- Body excerpt: **Edit: typo in the title. It’s astroturf. Reddit doesn’t let you edit titles.** 

**Astroturf: Astroturfing is a coordinated campaign designed to mimic a genuine organic growth of a**  
**movement or train of thought, when it’s actually an artificial and orchestrated effort by a hidden corp/politic...

### Qwen3-ASR (8 posts)

**[Fine-tuned Qwen3-ASR-0.6B on 1,000 hours of Hindi/Hinglish call audio: beats Whisper large-v3, Azure and Google on accented Hindi at half the size (Apache-2.0)](https://www.reddit.com/r/FunMachineLearning/comments/1vtauvy/finetuned_qwen3asr06b_on_1000_hours_of/)**
- Author: IslandSerious899 | Score: 6 | Comments: 1
- Date: 1787205016
- Subreddit: r/FunMachineLearning
- Body excerpt: Weights: [https://huggingface.co/tryorato](https://huggingface.co/tryorato)

We build voice agents for Indian and Gulf businesses, and every off-the-shelf ASR fell apart on real calls: accented Hindi, constant Hindi-English code-switching, noisy lines. So we fine-tuned Qwen3-ASR-0.6B on roughly 1,00...

**[[macOS] OpenVox - Local AI voice studio with 3 SOTA TTS models. No cloud. [Lifetime]](https://www.reddit.com/r/tts/comments/1rymr0u/macos_openvox_local_ai_voice_studio_with_3_sota/)**
- Author: ritzynitz | Score: 1 | Comments: 0
- Date: 1773981119
- Subreddit: r/tts
- Body excerpt: Problem: Most TTS tools lock you into one model, and usually a cloud API.

Solution: OpenVox is a local AI voice studio for Mac with multiple SOTA models you can switch between. No cloud, no accounts, everything runs on-device.

Core idea: multiple SOTA models

• Qwen3 TTS → top-tier quality + voice...

**[February so far in AI… in just 19 days  👇](https://www.reddit.com/r/AIAgentsInAction/comments/1r9ymco/february_so_far_in_ai_in_just_19_days/)**
- Author: Worldly_Ad_2410 | Score: 209 | Comments: 30
- Date: 1771601907
- Subreddit: r/AIAgentsInAction
- Body excerpt: Feb 19-20 – Gemini 3.1 Pro  
better coding, stronger agents, longer context  
  
Feb 18 – Google Lyria 3  
AI that turns text, pics, or video into 30-second music tracks with lyrics  
  
Feb 18 – Sarvam 105B AI LLM (India)  
big open model focused on indian languages and use cases  
  
Feb 17 – Clau...

**[JEV almost dead: CLM vs JEV](https://www.reddit.com/r/LocalLLaMA/comments/1wouby6/jev_almost_dead_clm_vs_jev/)**
- Author: R_Duncan | Score: 0 | Comments: 54
- Date: 1790232015
- Subreddit: r/LocalLLaMA
- Body excerpt: Original post: [https://www.reddit.com/r/LocalLLaMA/comments/1woscea/contrastive\_language\_models/](https://www.reddit.com/r/LocalLLaMA/comments/1woscea/contrastive_language_models/)

(sorry I felt it wasn't giving CLM the highlight it deserves)

  
What it is: a new projection head for Qwen3-8B.

...

**[My foray into local ai. Two BC-250 ex mining apus running Qwen3.6-35B-A3B Q4_K_M at 60 tok/s with 64k context](https://www.reddit.com/r/LocalLLaMA/comments/1wou3gr/my_foray_into_local_ai_two_bc250_ex_mining_apus/)**
- Author: Ok-Breadfruit-3523 | Score: 0 | Comments: 12
- Date: 1790231159
- Subreddit: r/LocalLLaMA
- Body excerpt: These boards cost me $115 each and I have them connected using llama.cpp with Vulkan and RPC on Bazzite. The boards have roughly 27GB of combined GPU memory and communicate over 1gb Ethernet. For around $300 including psu I’m loving the performance. I have a few more and want to see what 6 looks lik...

**[Qwen 3.8 Flash Next q4_k_m, 130k context, q8 cache on 16GB VRAM ann 64GB RAM, 15-20 t/s on 4080](https://www.reddit.com/r/LocalLLaMA/comments/1wom3fe/qwen_38_flash_next_q4_k_m_130k_context_q8_cache/)**
- Author: AvidCyclist250 | Score: 0 | Comments: 39
- Date: 1790207201
- Subreddit: r/LocalLLaMA
- Body excerpt: Thought it's about time to share after testing for a week. You need four things most people miss: the right quant, the right model, the right branch, and the right cache flags. 

https://github.com/dtm-beep/qwen38-flash-next-mtp-16gb    

TLDR: AtomicChat AD-4.27bpw Q4_K_M target + the shared Unslot...

**[Qwen FN vs 27B --- Think I'm saturated.](https://www.reddit.com/r/LocalLLaMA/comments/1woi2ho/qwen_fn_vs_27b_think_im_saturated/)**
- Author: OvertaxedOne | Score: 0 | Comments: 63
- Date: 1790197139
- Subreddit: r/LocalLLaMA
- Body excerpt: Got QFN up and running on our Strix box this past weekend and have been running on it for a few days now.   Big thank you/shout out to the Halogen team, it's running fantastic on the Strix, this is clearly "the setup" right now for this hardware with this model, really impressive performance for suc...

**[Stress-test Qwen3-TTS and VoxCPM2 in real-world scenarios and uncover reliability failures](https://www.reddit.com/r/speechtech/comments/1wmg8pn/stresstest_qwen3tts_and_voxcpm2_in_realworld/)**
- Author: nshmyrev | Score: 0 | Comments: 1
- Date: 1790005004
- Subreddit: r/speechtech
- Body excerpt: ...

### Sarvam AI (33 posts)

**[Sarvam is building a full-stack AI platform optimised for 22 Indian languages, code-mixed text and speech, Indian governance and enterprise use cases, and population-scale deployment, areas where global models still leave a large gap.](https://www.reddit.com/r/ShareBazarIndia/comments/1r2nzbg/sarvam_is_building_a_fullstack_ai_platform/)**
- Author: InsuranceLess8872 | Score: 9 | Comments: 0
- Date: 1770884477
- Subreddit: r/ShareBazarIndia
- Body excerpt: ...

**[Anyone testing Indian TTS (Text to Speech) models on actual phone calls?](https://www.reddit.com/r/AI_India/comments/1wbdmfg/anyone_testing_indian_tts_text_to_speech_models/)**
- Author: nandani_bhatti12 | Score: 16 | Comments: 12
- Date: 1788935294
- Subreddit: r/AI_India
- Body excerpt: I’ve been testing sarvam bulbul and convozen ragini for a Hinglish voice agent.

Both sound good in demos, but real calls are a different story.

The issues I keep noticing are small things, weird pauses, English words suddenly sounding inserted into Hindi, names or numbers breaking the flow, and th...

**[My interview experience with @SarvamAI for ML engineer role.](https://www.reddit.com/r/developersIndia/comments/1u4uf70/my_interview_experience_with_sarvamai_for_ml/)**
- Author: Aggravating-Ant-8234 | Score: 1888 | Comments: 254
- Date: 1781365919
- Subreddit: r/developersIndia
- Body excerpt: This was during campus placements-dec'24 (freshers take notes).  
CTC : 84 LPA (including esops)

Disclaimer : No DSA was asked

To get an interview call, we had to build a VAD (Voice Activity Detector) from scratch in 2.5 hours on-site (with proctorship), although we were allowed any tool we could ...

**[India is winning Audio Benchmark using Sarvam model](https://www.reddit.com/r/AajMaineJana_Video/comments/1r6zdfh/india_is_winning_audio_benchmark_using_sarvam/)**
- Author: Haunting_Pizza7642 | Score: 48 | Comments: 3
- Date: 1771312349
- Subreddit: r/AajMaineJana_Video
- Body excerpt: Looks like Indian AI models are winning the Audio race will they be able to build BPO replacement AI....

**[Attended the AI Impact Summit today — and I’m genuinely blown away.](https://www.reddit.com/r/indianstartups/comments/1r8bvxm/attended_the_ai_impact_summit_today_and_im/)**
- Author: gaut90 | Score: 296 | Comments: 60
- Date: 1771441142
- Subreddit: r/indianstartups
- Body excerpt: 

Here are 5 Made-in-India AI innovations that completely impressed me (reordered):

1. **Sarvam Kaze**: Stylish AI-powered smart glasses built in India that “see” what you see. They don’t just record — they interpret and explain your surroundings in your local language through bone-conduction audio...

**[February so far in AI… in just 19 days  👇](https://www.reddit.com/r/AIAgentsInAction/comments/1r9ymco/february_so_far_in_ai_in_just_19_days/)**
- Author: Worldly_Ad_2410 | Score: 209 | Comments: 30
- Date: 1771601907
- Subreddit: r/AIAgentsInAction
- Body excerpt: Feb 19-20 – Gemini 3.1 Pro  
better coding, stronger agents, longer context  
  
Feb 18 – Google Lyria 3  
AI that turns text, pics, or video into 30-second music tracks with lyrics  
  
Feb 18 – Sarvam 105B AI LLM (India)  
big open model focused on indian languages and use cases  
  
Feb 17 – Clau...

**[India has launched 5 LLMs this week. • Sarvam (Bengaluru) • Gnani (Bengaluru) • BharatGen (Mumbai) • Fractal (Mumbai/SF) • Tech Mahindra (Pune)](https://www.reddit.com/r/IndiaPulse_/comments/1rai3u8/india_has_launched_5_llms_this_week_sarvam/)**
- Author: wryes | Score: 138 | Comments: 27
- Date: 1771649523
- Subreddit: r/IndiaPulse_
- Body excerpt: ...

**[What Actually Powers Sub 200ms Multilingual Voice AI? It Is Not Just GPUs](https://www.reddit.com/r/VoiceAutomationAI/comments/1w0prae/what_actually_powers_sub_200ms_multilingual_voice/)**
- Author: Aryanlabs | Score: 5 | Comments: 6
- Date: 1787921561
- Subreddit: r/VoiceAutomationAI
- Body excerpt: Everyone assumes low latency voice AI is a GPU shopping problem. Buy more H100s, latency drops, done.

It is not that simple.

We looked at how Sarvam AI and Cartesia actually get to sub 200ms round trips across multiple languages, and the pattern was the same both times. The real gains came from re...

**[tamil voice agents](https://www.reddit.com/r/tamilyapping/comments/1vd5tuv/tamil_voice_agents/)**
- Author: shxdowtamer | Score: 4 | Comments: 4
- Date: 1785637669
- Subreddit: r/tamilyapping
- Body excerpt: summah scroll pannitu irukkum bothu oru startup pathi paarthen "foish audio" ivanga voice ai startup company , ivangalta irukka voice agent , normal sarvam ai agent vida tamil nalla pesuthu:  
  
[https://fish.audio/m/704e6e11b64d4f5ca484256d349fd041](https://fish.audio/m/704e6e11b64d4f5ca484256d349...

**[I built an AI cricket commentator that watches ball-by-ball data and generates natural commentary in Indian languages — powered by Sarvam Bulbul v3.](https://www.reddit.com/r/AI_India/comments/1r0yr4d/i_built_an_ai_cricket_commentator_that_watches/)**
- Author: DragonishDark | Score: 64 | Comments: 31
- Date: 1770724516
- Subreddit: r/AI_India
- Body excerpt: ...

### Whisper (OpenAI) (18 posts)

**[Fine-tuned Qwen3-ASR-0.6B on 1,000 hours of Hindi/Hinglish call audio: beats Whisper large-v3, Azure and Google on accented Hindi at half the size (Apache-2.0)](https://www.reddit.com/r/FunMachineLearning/comments/1vtauvy/finetuned_qwen3asr06b_on_1000_hours_of/)**
- Author: IslandSerious899 | Score: 6 | Comments: 1
- Date: 1787205016
- Subreddit: r/FunMachineLearning
- Body excerpt: Weights: [https://huggingface.co/tryorato](https://huggingface.co/tryorato)

We build voice agents for Indian and Gulf businesses, and every off-the-shelf ASR fell apart on real calls: accented Hindi, constant Hindi-English code-switching, noisy lines. So we fine-tuned Qwen3-ASR-0.6B on roughly 1,00...

**[[Electron] Earheart - private, hotkey-driven voice dictation for Windows/macOS/Linux that runs fully on-device](https://www.reddit.com/r/coolgithubprojects/comments/1ug4c4z/electron_earheart_private_hotkeydriven_voice/)**
- Author: hydrarulz | Score: 3 | Comments: 0
- Date: 1782473823
- Subreddit: r/coolgithubprojects
- Body excerpt: I built Earheart because I wanted Whisper-style voice dictation that doesn't ship my audio to anyone's cloud and doesn't make me set up Python or an account first.

You press a global hotkey (`Ctrl/Cmd+Shift+Space`), speak, press again, and the transcribed text gets pasted straight into whatever app...

**[MangoChat — free, open-source, ultra-lightweight voice dictation built for Windows](https://www.reddit.com/r/VibeCodeDevs/comments/1r9jgf2/mangochat_free_opensource_ultralightweight_voice/)**
- Author: bcrawl | Score: 2 | Comments: 3
- Date: 1771555269
- Subreddit: r/VibeCodeDevs
- Body excerpt:  Hey All - Introducing MangoChat. 

We know voice dictation apps suck for Windows or cost too much. Not everyone has MacOS. Windows users need this functionality for the current Agentic AI development.

I noticed that Deepgram and Assembly AI currently give out $250 free credits without even needing...

**[TranscriptionSuite - A fully local, private & open source audio transcription for Linux, Windows & macOS](https://www.reddit.com/r/LocalLLaMA/comments/1r9y6s8/transcriptionsuite_a_fully_local_private_open/)**
- Author: TwilightEncoder | Score: 184 | Comments: 114
- Date: 1771600944
- Subreddit: r/LocalLLaMA
- Body excerpt: **EDIT**: Update post [here](https://www.reddit.com/r/LocalLLaMA/comments/1rmdvdk/transcriptionsuite_my_fully_local_private_open/).

---

Hi! This is a short presentation for my hobby project, [TranscriptionSuite](https://github.com/homelab-00/TranscriptionSuite).


**TL;DR** A fully local & private...

**[I ported my local voice dictation tool to Linux — Wayland-native, faster-whisper, AppImage available](https://www.reddit.com/r/linux/comments/1s6xs0g/i_ported_my_local_voice_dictation_tool_to_linux/)**
- Author: raww2222 | Score: 291 | Comments: 115
- Date: 1774797375
- Subreddit: r/linux
- Body excerpt: I've been building VoiceFlow for a few months now. It runs Whisper locally for voice dictation. Audio stays on your machine, no network calls, no accounts.

It started on Windows back in December and picked up around 270 stars on GitHub. Enough people asked about Linux that I finally sat down and ma...

**[VoxScribe — free, open-source, offline voice dictation for Windows](https://www.reddit.com/r/software/comments/1w4i2kh/voxscribe_free_opensource_offline_voice_dictation/)**
- Author: Strong-Leg-9636 | Score: 7 | Comments: 17
- Date: 1788282331
- Subreddit: r/software
- Body excerpt: Hold a hotkey, talk, release — the text gets typed into whatever app you're focused in. Runs speech-to-text locally (faster-whisper), so there's no subscription and no cloud upload. MIT licensed.

GitHub: [https://github.com/ahmedhmam1994/voxscribe-ai-voice-dictation](https://github.com/ahmedhmam199...

**[[Promotion] Substitute Gboard dictation with modern offline speech to text models](https://www.reddit.com/r/HowToMen/comments/1rzykmr/promotion_substitute_gboard_dictation_with_modern/)**
- Author: WhisperianCookie | Score: 28 | Comments: 44
- Date: 1774116991
- Subreddit: r/HowToMen
- Body excerpt: Hi everyone, we built a speech to text app for Android named Whisperian that works alongside Gboard and acts as a more configurable alternative to Google dictation / Wisprflow.

I posted it last month, but figured I'd post again since now we also added local models support so that the app can work w...

**[Any free Windows app that converts Hindi speech to English text typing? or Hinglish ?](https://www.reddit.com/r/windowsapps/comments/1q5hf4n/any_free_windows_app_that_converts_hindi_speech/)**
- Author: gaurav_9372 | Score: 2 | Comments: 3
- Date: 1767702963
- Subreddit: r/windowsapps
- Body excerpt: I’m looking for a free Hindi voice to English typing tool for Windows.

**What I need**

1. Speak in Hindi and have it typed in English (translated) within seconds.
2. Should work system-wide in apps like Teams, browser text fields, WhatsApp, etc.
3. Option to type in Hinglish too when needed (not H...

**[Any free Windows app that converts Hindi speech to English text typing? or Hinglish ?](https://www.reddit.com/r/TextToSpeech/comments/1q5hdug/any_free_windows_app_that_converts_hindi_speech/)**
- Author: gaurav_9372 | Score: 0 | Comments: 1
- Date: 1767702860
- Subreddit: r/TextToSpeech
- Body excerpt: I’m looking for a free Hindi voice to English typing tool for Windows.

**What I need**

1. Speak in Hindi and have it typed in English (translated) within seconds.
2. Should work system-wide in apps like Teams, browser text fields, WhatsApp, etc.
3. Option to type in Hinglish too when needed (not H...

**[Launched Vaani today: an Indic TTS API that returns word-by-word timestamps](https://www.reddit.com/r/StartupSoloFounder/comments/1wngt61/launched_vaani_today_an_indic_tts_api_that/)**
- Author: Temporary_Water_7579 | Score: 3 | Comments: 0
- Date: 1790099914
- Subreddit: r/StartupSoloFounder
- Body excerpt: Hello there,



Here’s a quick update on the tech stack – Vaani was launched today. 🎉



Vaani is a text-to-speech engine for Indian languages, specifically Hindi, and different from the usual TTS APIs, it delivers the word-level timestamps along with the audio stream – a structured JSON containing ...


---

## Raw Data Archive

**Raw YAML search results:** `reddit_raw/search_*.yaml` (43 files)
**Extracted posts (JSON):** `relevant_posts.json` (275 posts)
**Detailed posts with comments (JSON):** `detailed_posts.json` (0 posts)

**Note:** This report is a **transport layer only**. It presents evidence verbatim. For synthesis, ranking, and architectural recommendations, refer to frontier-model analysis.


---

## raw file: `research_x_agentreach.md` (verbatim)

# Tamil Voice Recognition & TTS Research - X/Twitter Data

**Research Date:** 2026-09-24  
**Search Tool:** X/Twitter wrapper  
**Total Searches:** 13  
**Independent Posts:** ~89  
**Vendor/Employee Posts:** ~24

## Search Query Summary

| Query | Hit Count | Relevant Count | Exit Code | Status |
|-------|-----------|-----------------|-----------|---------|
| tamil speech recognition | 16 | 14 | 0 | Success |
| tamil speech to text | 15 | 13 | 0 | Success |
| tamil ASR | 15 | 7 | 0 | Success (mixed results) |
| tanglish | 16 | 10 | 0 | Success |
| tamil TTS | 20 | 18 | 0 | Success |
| sarvam bulbul tamil | 30+ | 28 | 0 | Success (large) |
| whisper tamil | 16 | 10 | 0 | Success |
| AI4Bharat | 15 | 15 | 0 | Success (all relevant) |
| SarvamAI | 15 | 15 | 0 | Success (all relevant) |
| IndicConformer | 0 | 0 | 143 | TIMEOUT |
| indic voice | 20 | 18 | 0 | Success |
| code mixed ASR | 20 | 16 | 0 | Success |
| tamil voice assistant | 20 | 18 | 0 | Success |

---

## Key Findings by Model/Service

### Count Summary by Provider/Model

**Vendor Posts:**
- Sarvam AI: 12 entries
- AI4Bharat/Bodhan AI: 10 entries
- OpenAI: 3 entries
- ElevenLabs: 3 entries
- Cartesia (Sonic): 2 entries
- Google Gemini: 2 entries
- Others: 2 entries

**Independent Posts:**
- Whisper general use: 8 entries
- Sarvam Bulbul v3/v4: 6 entries
- Indic-Speak: 5 entries
- Code-mixed speech/Tanglish: 8 entries
- Cartesia Sonic 3: 3 entries
- Custom voice agents: 12 entries
- IndicVoices/Svara/other models: 7 entries
- Accuracy comparisons: 9 entries

---

## Detailed Research Entries

### 1. Sarvam AI Voice Models

**VENDOR: Sarvam Bulbul v3 TTS Ranking**
- URL: https://x.com/i/status/2097689651603746988
- Author: SuryaS_1729
- Date: 2026-09-16
- Likes: 89
- Model: Bulbul v3 TTS
- Verbatim: "Bulbul v3 is still pretty usable, especially for conversational AI calling and customer servie. However, the voice clarity needs to improve for audiobooks and storytelling. The female Telugu voices fail pretty badly. If you're using v3, I'd go with Shubh. It sounds noticeably robotic/telephonic than Cartesia, but this is still the best option I've found from an Indian provider."
- Key Points: Ranked #2 for South Indian, acceptable for customer service, clarity issues for storytelling, Shubh voice recommended

**VENDOR: Sarvam Saaras v3 - BRIDGE ASR 2.0 Score**
- URL: https://x.com/i/status/2100578768272150909
- Author: thehypedotnews
- Date: 2026-09-17
- Model: Sarvam Saaras v3 ASR
- Benchmark Score: 0.787 (Humyn score, 4th of 23 globally)
- Rank Above: Gemini 3 Pro (0.798), Gemini 2.5 Pro (0.780)
- Rank Below: ElevenLabs Scribe v2 (0.876), Gemini 3 Flash (0.808)
- Test Conditions: 23 models on 23 languages with code-switching, overlap, interruptions
- Verbatim: "silence breaks these models harder than speed"

**VENDOR: Sarvam API Usage Cost**
- URL: https://x.com/i/status/2101976048976134359
- Author: TughlaqBinMohd
- Date: 2026-09-21
- Service: Sarvam TTS API
- Monthly Cost: ₹500 for Tamil TTS

**VENDOR: Sarvam Series B Funding**
- URL: https://x.com/i/status/2066560409444983210
- Author: KanikaBK
- Date: 2026-06-15
- Funding: $234M Series B at $1.5B valuation
- Coverage: 22 Indian languages, sovereign AI stack

---

### 2. AI4Bharat / Bodhan AI Voice Models

**VENDOR: Indic-Speak TTS - Sept 2026**
- URL: https://x.com/i/status/2094742553543541162
- Author: MiteshKhapra
- Date: 2026-09-01
- Model: Indic-Speak 4B params, 23 languages including Tamil
- Verbatim: "Indic-Speak: 4B params, 23 languages, one model. Also handles code-mixed speech naturally, gets PAN/Aadhaar/currency right, and reads a full Tamil audiobook chapter without losing the thread. Multi-speaker podcast style generation in single pass."
- Key: Code-mixed speech, audiobook-ready, multi-speaker generation in one pass

**VENDOR: Indic-Transcribe ASR - Aug 2026**
- URL: https://x.com/i/status/2089322239305175350
- Author: MiteshKhapra
- Date: 2026-08-17
- Model: Indic-Transcribe 1.2B params, 26 languages + English
- Verbatim: "India is a voice-first nation: countless languages, scripts, and accents. Introducing Indic-Transcribe: built to understand India as she actually speaks."
- Scope: 26 Indian languages, designed for native speech patterns

**VENDOR: Indic-Parler TTS - Dec 2024**
- URL: https://x.com/i/status/1865266632995803290
- Author: Marktechpost
- Date: 2024-12-07
- Model: Indic-Parler-TTS, 21 languages including Tamil
- Verbatim: "Supporting 21 languages, including Hindi, Bengali, Tamil, Telugu, and Marathi, alongside English, built on a robust dataset of over 1,800 hours of speech data. It offers 69 unique voices with emotion rendering, accent flexibility for Indian English, and customizable attributes like pitch, speaking rate, background noise, and reverberation."
- Dataset: 1,800+ hours, 69 voices, emotion support

---

### 3. Tanglish & Code-Mixed Speech

**Independent: Tanglish Detection Failure - Grok Feedback**
- URL: https://x.com/i/status/2100675671328460814
- Author: grok
- Date: 2026-09-17
- Issue: Tanglish script detection failed
- Verbatim: "Feedback on the Tanglish detection failure is noted and tagged correctly for the training pipeline. Improvements to mixed-script and lower-resource language handling are ongoing."
- Status: Acknowledged gap, in training pipeline

**Independent: Tamil-LM-2B for Tanglish Translation**
- URL: https://x.com/i/status/2099506205932798414
- Author: VigneshAnguraj
- Date: 2026-09-14
- Model: tamil-lm-2b (2B parameters, 1.3GB, local only)
- Verbatim: "Where it is strong is translation. Tamil to English, English to Tamil, and everyday Tamil and Tanglish. Against models built by the frontier labs, it beats their 120 billion parameter open model, sixty times its size, on all four Tamil translation directions in our benchmark."
- Scope: Tanglish translation focus, phone-only, no internet required

**Independent: Code-Mixed TTS - Rumik Silk Mulberry 1.5**
- URL: https://x.com/i/status/2067608358551695632
- Author: VaibhavSisinty
- Date: 2026-06-18
- Model: Silk Mulberry 1.5
- Latency: 162 milliseconds
- Cost: ₹0.40 per minute
- Verbatim: "Handles Hinglish, Tanglish, Manglish the way Indians actually speak. Not robotic translations. Real code-switching with natural tone, pauses, and emotions."

---

### 4. Whisper / OpenAI Speech Recognition

**Independent: Whisper Tamil Performance Leader**
- URL: https://x.com/i/status/1573904544978718720
- Author: krishashok
- Date: 2022-09-25
- Model: Whisper
- Verbatim: "Interesting to see that Tamil is the best-performing Indian language on Whisper (WER is word error rate)"
- Finding: Tamil ranks highest among Indian languages

**Independent: Whisper Telugu/Kannada Failure**
- URL: https://x.com/i/status/2034178974012633206
- Author: r4plh
- Date: 2026-03-18
- Issue: Whisper fine-tunes fail on Telugu and Kannada
- Verbatim: "Whisper fine-tunes for Hindi and Tamil? Worked. Telugu? Hallucinated text. Kannada? Output in the wrong script entirely. The model just hasn't seen enough data in these languages to produce stable output."
- Finding: Tamil/Hindi work; Telugu/Kannada hallucinate or output wrong script

**Independent: Streaming ASR Text Correction Problem**
- URL: https://x.com/i/status/2102009238667079914
- Author: AriaWestcott
- Date: 2026-09-21
- Issue: Streaming ASR text corrections break voice agent state
- Verbatim: "Streaming ASR has a problem nobody shows in demos. the text you already read? it can just… stop being true. you saw 'book a table.' two seconds later it says something else. for a voice agent consuming that text? broken state."
- Impact: Voice agents consume corrected text causing errors

---

### 5. Code-Mixed Speech Recognition

**Independent: BRIDGE ASR 2.0 Benchmark**
- URL: https://x.com/i/status/2100539424073539769
- Author: humynlabs
- Date: 2026-09-17
- Likes: 332
- Benchmark: 23 models across 23 languages
- Verbatim: "The only global independent ASR benchmark evaluating 23 models for real-world deployment across a 6-metric stack. Tested across 23 languages on real dual-speaker overlap, interruptions, code-switching, and conversations."
- Test Conditions: Real overlap, interruptions, code-switching
- Dataset: Public, with golden transcripts and eval scripts

**Independent: Voice Isolation Impact**
- URL: https://x.com/i/status/2102774409123815731
- Author: Ulobex
- Date: 2026-09-23
- Study: Krisp voice isolation impact
- Verbatim: "Across 265 real recordings, voice isolation brought word error rate down from 23.3% to 6.2% across 11 speech-to-text configurations."
- Improvement: 3.8x WER reduction
- Dataset: Public on Hugging Face

**Independent: Audio8-ASR-0.1B - Compact Code-Mixed**
- URL: https://x.com/i/status/2085321310067134527
- Author: SamuelZengML
- Date: 2026-08-06
- Model: Audio8-ASR-0.1B
- Capabilities: Rap, fast dialogue, mixed-language, multi-speaker, on-device
- Size: 100M parameters (ternary quantized)

---

### 6. Aria - Multilingual Tamil Voice Assistant

**Independent: Aria Voice Agent**
- URL: https://x.com/i/status/2084255591430795456
- Author: justkarangupta
- Date: 2026-08-03
- Service: Aria (realtime multilingual voice assistant)
- Languages: 15 (English, Hindi, Spanish, French, Japanese, Tamil, more)
- Stack: Groq Whisper + LLaMA 3.3 70B, Microsoft Edge TTS, Silero VAD
- Latency: "usually in a few seconds"
- Features: Automatic speech detection, realtime two-way WebRTC, barge-in
- Availability: Free tiers end-to-end

---

### 7. Accuracy & Performance Comparisons

**Independent: Sonic 3.6 vs Sarvam Bulbul v3 vs IndicSpeak**
- URL: https://x.com/i/status/2097689651603746988
- Author: SuryaS_1729
- Ranking for South Indian: #1 Sonic 3.6, #2 Bulbul v3, #3 IndicSpeak
- Sonic Verbatim: "By far my favorite. Sonic is the best combination of speed, diction and voice quality. There's a weird underlying noise/artifact in almost every other TTS I tried, which Sonic doesn't seem to have."
- Bulbul Issue: Female Telugu voices "fail pretty badly"
- IndicSpeak: Best on cost, but traditional-sounding voices

---

### 8. Hardware & Performance

**Independent: Svanita-0.6b - CPU ASR**
- URL: https://x.com/i/status/2101201091136507972
- Author: prasadvittaldev
- Date: 2026-09-19
- Model: Svanita-0.6b
- Performance: 3s audio → 0.28s on CPU (11x real-time)
- Feature: True code-switching, GPU-free
- Focus: Live Indic voice AI

**Independent: Rumik Latency**
- URL: https://x.com/i/status/2067608358551695632
- Latency: 162ms for code-mixed TTS

---

### 9. Tokenization Efficiency

**Independent: Tokenizer Tax for Tamil**
- URL: https://x.com/i/status/2102984395309375675
- Author: chirag
- Date: 2026-09-24
- Finding: "Tamil is 0.25 tokens/char on Gemma 4 and 2.16 on LFM2.5"
- Impact: Tokenization cost varies 8.6x across models; affects context window sizing

---

### 10. Failures & Edge Cases

**Independent: AssemblyAI Malayalam Failure**
- URL: https://x.com/i/status/2101909310028820609
- Author: JachinJVictor
- Date: 2026-09-21
- Issue: AssemblyAI "mostly tamil script, one sentence repeated twelve times"
- Finding: Severe repetition and script detection failure

**Independent: VocaMac Hinglish Local**
- URL: https://x.com/i/status/2102876650610528400
- Author: itsKanishkP
- Date: 2026-09-23
- Model: VocaMac v1.0.0 (Hinglish only, NOT Tamil)
- Verbatim: "Speak in English, Hindi, or mix both. It detects it automatically. Speak Hindi → get Hinglish (Roman English). And the best part: it runs completely locally on your Mac. No cloud. No API."
- Scope: Hinglish-only (no Tamil), local-only

---

## Summary Statistics

**Total Entries Collected:** ~113  
**Independent Posts:** ~89  
**Vendor Posts:** ~24  

**Models/Services Covered:**
- Sarvam (Bulbul v3, Saaras v3): 12 entries
- AI4Bharat/Bodhan (Indic-Speak, Indic-Transcribe, Indic-Parler): 10 entries
- Cartesia Sonic 3.x: 5 entries
- OpenAI Whisper: 8 entries
- Custom/OSS (Tamil-LM, Svanita, Audio8, Aria): 15 entries
- Benchmark/Comparison: 9 entries
- Error cases: 4 entries
- Infrastructure/Voice agents: 12 entries
- Other vendors (ElevenLabs, Google, Rumik): 8 entries

**Key Accuracy Metrics:**
- Sarvam Saaras v3 (BRIDGE ASR): 0.787
- ElevenLabs Scribe v2 (BRIDGE ASR): 0.876 (best)
- Gemini 3 Flash (BRIDGE ASR): 0.808
- Voice isolation WER improvement: 23.3% → 6.2%
- Tamil on Whisper: Best Indian language performance

**Performance Benchmarks:**
- Svanita-0.6b: 11x real-time on CPU
- Rumik Latency: 162ms
- Aria Latency: "a few seconds"
- Cartesia Sonic 3: "very low latency" (exact figure NOT COVERED)

**Critical Issues Found:**
- Whisper Telugu/Kannada hallucination and script failure
- Streaming ASR text correction causing voice agent state errors
- Sarvam Bulbul female Telugu voices fail
- Grok Tanglish detection still in training pipeline
- AssemblyAI Malayalam severe repetition

**Positive Findings:**
- Tamil outperforms other Indic languages on Whisper
- Code-mixed TTS at natural latency and low cost (Rumik)
- CPU-only ASR with code-switching support (Svanita)
- Tamil-LM beats 120B models on Tamil translation
- AI4Bharat supports full audiobook narration in Tamil
- Voice isolation provides 3.8x WER improvement

---

## Data Collection Notes

- All entries sourced verbatim from X/Twitter  
- VENDOR tags mark official company/employee posts
- One search timeout (IndicConformer) - not retried
- Benchmarks from independent sources where possible (Humyn Labs, Krisp)
- NOT COVERED indicates field not mentioned in source material
- All URLs, authors, dates verified from search results
- Likes counts captured as-is from X/Twitter API response


---

## S9 raw file: `research_leads_verify.md` (verbatim)

# Voice Recognition Model Research — Verification Results

**Date:** 2026-09-24
**Researcher:** Claude Haiku 4.5
**Method:** HuggingFace API + Model Card inspection

---

## Lead 1: AI4Bharat "Indic-Transcribe" (ASR, 1.2B)

**HF Repo:** bodhan-ai/indic-transcribe-flex, bodhan-ai/indic-transcribe-core
**URL:** https://huggingface.co/bodhan-ai/indic-transcribe-flex

**Weights:** OPEN-WEIGHTS (safetensors downloadable)
**License:** Bodhan_AI_Open_Model_License + indic-open-license (custom open)
**Params:** 1.2B (FastConformer encoder + TDT decoder, based on nvidia/canary-1b-v2)
**File Size:** ~2.2GB safetensors

**Tamil Support:** YES
- Language tags include: ta (Tamil)
- Full support: as, bn, brx, doi, gu, hi, kn, ks, kok, mai, ml, mni, mr, ne, or, pa, sa, sat, sd, ta, te, ur

**Code-Mixing:** YES
- Tags: code-switching, code-mixing
- Long-form inference provided

**Tamil WER/CER Benchmarks:** NOT COVERED (README gated, cannot access detailed metrics)

**Runtime:** NeMo (.nemo), Transformers (safetensors), ONNX (community variants)
**VRAM:** ~4-6GB GPU typical, depends on batch size
**Windows:** Yes (PyTorch/Transformers stack + ONNX Runtime)

---

## Lead 2: AI4Bharat "Indic-Speak" (TTS, 4B)

**HF Repo:** bodhan-ai/indic-speak
**URL:** https://huggingface.co/bodhan-ai/indic-speak

**Weights:** OPEN-WEIGHTS (safetensors downloadable)
**License:** Bodhan_AI_Open_Model_License + indic-open-license
**Params:** 3.2B (based on Llama-3.2-3B)
**File Size:** ~6.4GB full FP32; ~3.2GB quantized (4-bit MLX)

**Tamil Support:** YES
- Language tags: ta (Tamil) included
- Full support: en, hi, bn, mr, te, ta, gu, kn, ml, or, pa, as, ur, brx, doi, kok, ks, mai, ne, mni, sa, sat, sd

**Code-Mixing:** YES
- Tags: code-switching, code-mixing

**Quality Metrics (MOS/Numbers):** NOT COVERED (README gated)

**Runtime:** Transformers (text-generation), Vocos vocoder (PyTorch)
**Quantized Variants:** MLX (4-bit, 6-bit, 8-bit for Apple Silicon); GGUF via llama.cpp
**VRAM:** Full: ~13GB; 4-bit: ~3.2GB
**Windows:** Yes (Transformers) + GGUF (llama.cpp native binary available)

---

## Lead 3: Svanita-0.6b (ASR, code-switching, CPU 11x)

**HF Repo:** prasadvittaldev/svanita-0.6b
**URL:** https://huggingface.co/prasadvittaldev/svanita-0.6b

**Weights:** OPEN-WEIGHTS (safetensors)
**License:** CC-BY-4.0
**Params:** 622M (encoder 609M + decoder+joint 13M)
**File Size:** ~1.2GB

**Tamil Support:** NO
- Supported languages (from README): Telugu and Hindi only
- QUOTE: "This release (v0.2) covers Telugu and Hindi in one checkpoint. More Indian languages follow on the same recipe."
- No Tamil language support in this version

**Code-Mixing:** YES (Telugu-English, Hindi-English)
- QUOTE: "Svanita transcribes the local language and the English mixed into it in one transcript — native script for the native words, Latin script for the English ones"
- Example: "OK home loan కావాలి అంటే మీకు ఎంత కావాలి"

**CPU Speed (11x Real-time):** YES, VERIFIED
- QUOTE: "a 3.6-second reply is transcribed in about 0.33 seconds"
- Measured: 3600ms / 326ms = ~11x real-time on 8 CPU threads
- CPU-only, no GPU required

**Telugu Benchmarks (Published):** YES
- IndicVoices Telugu (conversational, 1,499 clips, 153 speakers):
  - WER (either script): 37.7
  - WER (Latin required): 38.0
  - CER: 17.0
  - English retained in Latin: 74%
- Kathbath Telugu (read speech): WER ~24.5, CER ~14.2

**Runtime:** Transformers (ParakeetForTDT), CPU inference script included
**Base Model:** nvidia/parakeet-tdt-0.6b-v3
**VRAM:** CPU-only (2-3GB RAM sufficient)
**Windows:** Yes (Python + transformers + torch cross-platform)

---

## Lead 4: tamil-lm-2b (LLM, not ASR)

**HF Repo:** Timegravity/tamil-lm-2b-instruct, Timegravity/tamil-lm-2b-base
**URL:** https://huggingface.co/Timegravity/tamil-lm-2b-instruct

**Weights:** OPEN-WEIGHTS (safetensors)
**License:** Apache-2.0
**Params:** 2B (Qwen3.5-2B base)
**File Size:** ~4.2GB full; ~1.3GB GGUF quantized

**Type:** TEXT-GENERATION LLM, NOT ASR
- Pipeline: image-text-to-text (multimodal)
- NOT suitable for speech recognition tasks
- Can be used for Tamil text understanding/generation only

**Tamil/Tanglish Support:** YES (text level)
- Language tags: ta, en
- Trained on Tamil and Tamil-English text

**Runtime:** Transformers, GGUF (llama.cpp compatible)
**VRAM:** 4-8GB GPU or 16GB CPU
**Windows:** Yes

---

## Lead 5: Audio8-ASR-0.1B

**HF Repo:** Edge0/Audio8-ASR-0.1B
**URL:** https://huggingface.co/Edge0/Audio8-ASR-0.1B

**Weights:** OPEN-WEIGHTS (safetensors)
**License:** CC-BY-NC-4.0 (Non-Commercial)
**Params:** 0.1B
**File Size:** ~120MB

**Tamil Support:** NO
- Language tags: en, zh, fr, ja, yue, de, ko ONLY
- No South Asian languages included
- NOT Tamil-capable

**Runtime:** Transformers (custom Audio8 code), ONNX Runtime available
**Variants:** iOS CoreML, ONNX, transformers
**VRAM:** 512MB-2GB
**Windows:** Yes (Transformers + ONNX Runtime)

---

## Lead 6: AI4Bharat IndicF5 (TTS)

**HF Repo:** ai4bharat/IndicF5
**URL:** https://huggingface.co/ai4bharat/IndicF5

**Weights:** OPEN-WEIGHTS (safetensors)
**License:** MIT

**Tamil Support:** YES
- Tags: as, bn, gu, mr, hi, kn, ml, or, pa, ta, te
- Tamil explicitly included

**Code-Mixing:** NOT COVERED (README details inaccessible)

**Quality Metrics:** NOT COVERED (README gated)

---

## Lead 6b: AI4Bharat indic-parler-tts

**HF Repo:** ai4bharat/indic-parler-tts
**URL:** https://huggingface.co/ai4bharat/indic-parler-tts

**Weights:** OPEN-WEIGHTS (safetensors)
**License:** Apache-2.0
**File Size:** ~2.4GB

**Tamil Support:** YES
- Language tags: en, as, bn, gu, hi, kn, ks, or, ml, mr, ne, pa, sa, sd, ta, te, ur, om
- Tamil included

**Runtime:** Transformers (Parler-TTS, speaker/prosody control)
**VRAM:** Full: ~8GB GPU or 16GB CPU
**Windows:** Yes

---

## Lead 7: Microsoft Phi-4-multimodal-instruct

**HF Repo:** microsoft/Phi-4-multimodal-instruct
**URL:** https://huggingface.co/microsoft/Phi-4-multimodal-instruct

**Weights:** OPEN-WEIGHTS (safetensors)
**License:** MIT
**Params:** 12B (multimodal: vision + audio + text)
**File Size:** ~24GB

**Audio/Speech Languages Supported:** ar, zh, cs, da, nl, en, fi, fr, de, he, hu, it, ja, ko, no, pl, pt, ru, es, sv, th, tr, uk
**Tamil for Audio/Speech:** NO
- Tamil NOT listed in audio language support
- https://huggingface.co/microsoft/Phi-4-multimodal-instruct (tags show no Tamil)

**Speech Tasks:** Supports ASR, speech-summarization, speech-translation
- But NOT for Tamil audio

**Runtime:** Transformers (custom phi4mm), ONNX Runtime
**VRAM:** 24GB+ or quantized variants
**Windows:** Yes (Transformers + ONNX)

---

## Lead 7b: Google Gemma-3n-E4B-it

**HF Repo:** google/gemma-3n-E4B-it
**URL:** https://huggingface.co/google/gemma-3n-E4B-it

**Weights:** GATED / MANUAL (requires approval/access request)
- NOT freely downloadable without manual approval from Google

**License:** Gemma (research/commercial restrictions apply)
**Params:** 4B (multimodal: image + audio + text)
**File Size:** ~8GB

**Audio/Speech Language Support:** NOT COVERED
- Public card does not detail which languages are supported for audio/speech input
- Gemma languages typically: broad multilingual, but Tamil coverage unknown

**Gating Status:** MANUAL (user must request access)
- https://huggingface.co/google/gemma-3n-E4B-it (gated="manual")

---

## Lead 8: HumynLabs "BRIDGE ASR 2.0" Benchmark

**Public Leaderboard:** NOT FOUND
- Standard searches for "BRIDGE ASR 2.0 leaderboard" or "HumynLabs benchmark" did not return indexed HuggingFace resource
- X post reference provided (2026-09-22 estimated) but specific benchmark URL not accessible

**Tamil Benchmarks in Related Work:**
- NOT COVERED — BRIDGE ASR 2.0 specific Tamil rows not located

**Alternative Sources Found:**
- Svanita paper includes IndicConformer benchmarks on IndicVoices (Telugu: WER 27.4)
- Open ASR Leaderboard exists but BRIDGE ASR 2.0 specific page not found

---

## Summary

| Lead | Repo | Weights | Tamil | Benchmarks |
|---|---|---|---|---|
| 1. Indic-Transcribe | bodhan-ai/* | **OPEN** | YES | Gated |
| 2. Indic-Speak | bodhan-ai/indic-speak | **OPEN** | YES | Gated |
| 3. Svanita-0.6b | prasadvittaldev/* | **OPEN** | NO | Telugu: 37.7 WER |
| 4. tamil-lm-2b | Timegravity/* | **OPEN** | YES (text) | N/A (LLM) |
| 5. Audio8-ASR-0.1B | Edge0/* | **OPEN** | NO | NOT COVERED |
| 6. IndicF5 | ai4bharat/IndicF5 | **OPEN** | YES | Gated |
| 6b. indic-parler-tts | ai4bharat/* | **OPEN** | YES | Gated |
| 7. Phi-4-multimodal | microsoft/* | **OPEN** | NO | NOT COVERED |
| 7b. Gemma-3n-E4B-it | google/gemma-3n-E4B-it | **GATED** | Unknown | N/A |
| 8. BRIDGE ASR 2.0 | NOT FOUND | N/A | N/A | NOT FOUND |


### S9 downloaded card: `indic-transcribe-flex/README.md` (verbatim)

---
extra_gated_prompt: "Please provide your details and agree to the [LICENSE](https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License.md) [[simpler version](https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License_Deed.md)] to request access."
extra_gated_fields:
  Company / Organization: text
  Country: country
  Intended Use Case:
    type: select
    options:
      - Research
      - Commercial
      - Education
      - label: Other
        value: other
  I agree to the license terms: checkbox
license: other
language:
- en
- as
- bn
- brx
- doi
- gu
- hi
- kn
- ks
- kok
- mai
- ml
- mni
- mr
- ne
- or
- pa
- sa
- sat
- sd
- ta
- te
- ur
- bho
- hne
- bgc
- bhb
library_name: nemo
pipeline_tag: automatic-speech-recognition
base_model: nvidia/canary-1b-v2
tags:
- automatic-speech-recognition
- speech
- audio
- asr
- multilingual
- indic
- code-switching
- code-mixing
- romanization
- transliteration
- language-identification
- nemo
- canary
- fastconformer
metrics:
- wer
- cer
---

<div align="center">
  <img src="banner.png" alt="Indic-Transcribe Flex">
</div>

<h1 id="indic-transcribe-flex" style="color:#FFD21E;">Indic-Transcribe-flex</h1>

<div align="center">

[![Model Arch](https://img.shields.io/badge/Model_Arch-FastConformer--Transformer-C1440E?style=flat#model-badge)](#model-architecture)
[![Params](https://img.shields.io/badge/Params-1.2B-C1440E?style=flat#model-badge)](#model-architecture)
[![Languages](https://img.shields.io/badge/Languages-27-C1440E?style=flat#model-badge)](#supported-languages)
[![Language](https://img.shields.io/badge/Language-Multilingual-C1440E?style=flat#model-badge)](#supported-languages)
[![License](https://img.shields.io/badge/License-Indic%20Open%20Model%20License%20v1.0-C1440E?style=flat#model-badge)](#license--terms-of-use)


</div>

**Multilingual speech recognition for 27 Indian languages with native-script, mixed-script, and romanized output.**

<div align="center">
  <img src="model-diagram.png" alt="Indic-Transcribe: 27 languages in, all output features out" width="860">
</div>

**Quick links**:  [Blog](bodhan.ai/research/blogs/indic-transcribe) · [Demo](https://youtu.be/5GuSEcs4ucc?si=xNhlzdFBWaIEW2fl) · [Try it out](bodhan.ai/developers/indic-transcribe) . [Github](https://github.com/Bodhan-AI/bodhan_genai)

**Indic-Transcribe-Flex** is a multilingual Automatic Speech Recognition (ASR) model built for **27 Indian languages**. It is trained to be robust and general-purpose: it handles the full diversity of Indian accents and holds up in noisy real-world conditions, from crowded markets to call-centre floors, with strong coverage in the domains where Indian voice products are actually built: education, agriculture, and healthcare.

Unlike traditional ASR systems that return only a native-script transcript, Indic-Transcribe offers **three transcription modes**: native script, romanized text, or true code-mixed output so you can match the output to what your product expects.

---

<h2 id="why-choose-indic-transcribe" style="color:#FFD21E;">Why Choose Indic-Transcribe?</h2>

- 🔀 **Code-mixing, natively.** Indians rarely speak one language at a time. Indic-Transcribe transcribes Hinglish and other mixed speech as it is actually spoken, instead of forcing it into a single language.
- 📝 **Three transcription modes.** *Native script* for fully native output; *mixed script* for native words in native script with English and numerals in Latin; *romanized* for everything in Latin script.
- 🏥 **Domain coverage where it matters.** Deep vocabulary in education, agriculture, and healthcare.
- 🌐 **Language identification built in.** Use the model directly as a language-ID system, or let it auto-detect the language and then transcribe.
---

<h2 id="supported-languages" style="color:#FFD21E;">Supported Languages</h2>

The model covers **27 languages** across four groups:

| Group | Languages |
| --- | --- |
| **Indian-accented English** | English benchmarked across speakers from 19 states |
| **22 constitutionally recognised languages** | Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu |
| **Hindi dialects** | Chhattisgarhi, Haryanvi |
| **Extremely low-resource** | Bhili, Bhojpuri |

See [Supported Language Codes](#supported-language-codes) for the code to pass at inference time.

<h3 style="color:#FFD21E;">The three transcription modes</h3>

The same utterance, three renderings:

| Mode | Output |
| --- | --- |
| Native script | `मैंने कल पांच बजे तीन फाइल्स अपलोड कीं` |
| Mixed script | `मैंने कल 5 बजे 3 files upload कीं` |
| Romanized | `maine kal 5 baje 3 files upload kin` |

---

<h2 id="model-architecture" style="color:#FFD21E;">Model Architecture</h2>

**Architecture Type:** NVIDIA Canary: FastConformer encoder with a Transformer decoder.

Indic-Transcribe-Flex is built on the [nvidia/canary-1b-v2](https://huggingface.co/nvidia/canary-1b-v2) architecture. The FastConformer encoder produces acoustic representations that the Transformer decoder converts into text, with task tokens selecting the transcription mode and target language.

|  |  |
| --- | --- |
| **Model name** | Indic-Transcribe-Flex |
| **Task** | Speech-to-Text (Automatic Speech Recognition) |
| **Base model** | [nvidia/canary-1b-v2](https://huggingface.co/nvidia/canary-1b-v2) |
| **Total parameters** | 1.2B |
| **Encoder** | FastConformer: 32 layers, 811M params, 1024 hidden dim, 8 attention heads, conv kernel 9 |
| **Decoder** | Transformer: 24 layers, 419M params, 1024 hidden size, 8 attention heads |
| **Vocabulary** | 7,152 tokens (1,152 special / task + 6,000 multilingual) |
| **Sub-word algorithm** | BPE (byte fallback disabled) |
| **Precision** | fp16 |
| **Checkpoint size** | 4.6 GB |


---

<h2 id="results-at-a-glance" style="color:#FFD21E;">Results at a Glance</h2>

Results below are from the **Voice of India** benchmark. ASR performance is measured using Word Error Rate (WER); **lower is better**. Best score per column is in **bold**.

| Model | Average | Assamese | Bhojpuri | Bengali | Gujarati | Hindi | Chhattisgarhi | Kannada | Maithili | Malayalam | Marathi | Odia | Punjabi | Tamil | Telugu | Urdu |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Indic-Transcribe-core** | 8.7 | 8.2 | 13.3 | 4.3 | 9.2 | 3.5 | 13.6 | 7.4 | 11.3 | 11.5 | 5.7 | 8.7 | 8.3 | 9.0 | 11.4 | 5.0 |
| Saaras V3 | 10.7 | 9.1 | 17.9 | 5.2 | 9.7 | 3.8 | 14.0 | 8.8 | 14.2 | 12.2 | 6.5 | 11.1 | 8.6 | 9.1 | 13.5 | 7.5 |
| **Indic-Transcribe-flex** | 11.3 | 9.6 | 18.5 | 5.0 | 10.8 | 4.1 | 13.6 | 9.7 | 15.1 | 13.7 | 6.6 | 10.2 | 9.5 | 10.8 | 13.1 | 5.6 |
| Indic Conformer | 17.8 | 13.1 | 30.3 | 9.5 | 16.3 | 6.5 | 24.5 | 16.3 | 16.3 | 28.2 | 11.6 | 13.1 | 19.1 | 16.2 | 20.0 | 8.0 |
| Gemini 3 Pro | 21.1 | 23.7 | 24.1 | 10.3 | 18.1 | 9.3 | 19.6 | 20.1 | 27.2 | 21.0 | 14.0 | 25.7 | 19.3 | 15.5 | 24.6 | 10.6 |
| Gemini 3 Flash | 23.1 | 25.0 | 20.2 | 11.1 | 20.3 | 7.1 | 21.7 | 18.5 | 28.0 | 30.1 | 14.2 | 23.3 | 23.2 | 17.3 | 25.5 | 11.0 |
| Gemma E4B | 36.1 | 45.0 | 27.0 | 19.6 | 27.3 | 9.1 | 24.0 | 31.0 | 36.7 | 44.4 | 24.4 | 44.4 | 23.4 | 37.9 | 41.6 | 14.2 |
| OmniASR LLM 7B | 44.5 | 23.9 | 26.3 | 20.9 | 32.0 | 9.6 | 20.7 | 35.0 | 44.6 | 48.8 | 24.5 | 72.3 | 31.7 | 40.6 | 48.7 | 14.8 |
| OmniASR CTC 7B | 62.5 | 33.3 | 39.2 | 43.5 | 62.5 | 20.7 | 33.4 | 50.0 | 51.6 | 61.3 | 33.6 | 90.2 | 80.7 | 58.3 | 62.1 | 89.3 |

Indic-Transcribe Flex offers support for more transcription modes and languages. Do check out [Indic-Transcribe Core](https://huggingface.co/bodhan-ai/indic-transcribe-core) for better accuracy.

<!-- ---

<h2 id="throughput--efficiency" style="color:#FFD21E;">Throughput & Efficiency</h2>

Measured on a single NVIDIA H100, fp16.

| Metric | Indic-Transcribe-Flex | Indic-Transcribe-lite |
| --- | :---: | :---: |
| Latency | 100 ms | 30 ms |
| RTFx | 500 | 1000 |
| Peak GPU memory | *TBD* | *TBD* |
| Checkpoint size | 4.6 GB | *TBD* |

> RTFx is the inverse real-time factor: RTFx 500 means one hour of audio is transcribed in ~7.2 seconds. -->

---

<h2 id="how-to-use-this-model" style="color:#FFD21E;">How to Use this Model</h2>

<h3 style="color:#FFD21E;">Installation</h3>

```bash
pip install torch torchaudio transformers sentencepiece soundfile
```

The model code ships inside this repository, so there is nothing else to install — no NeMo,
no other toolkit.

<details>
<summary>Conda environment (recommended for reproducibility)</summary>

```bash
conda create -n indic-transcribe python=3.10 -y
conda activate indic-transcribe
pip install torch torchaudio transformers sentencepiece soundfile
```

</details>

<h3 style="color:#FFD21E;">Input audio requirements</h3>

|  |  |
| --- | --- |
| Sample rate | 16 kHz (resampled automatically if it differs) |
| Channels | Mono |
| Formats | `.wav`, `.flac`, `.mp3` |
| Speakers | Single speaker — see [Limitations](#limitations) |

```bash
# Convert anything to the expected format
ffmpeg -i input.mp3 -ac 1 -ar 16000 -c:a pcm_s16le audio.wav
```

<h3 style="color:#FFD21E;">Basic inference</h3>

```python
# Gated model: accept the terms on this page, then run `hf auth login` once (older installs: `huggingface-cli login`).
import sys
from huggingface_hub import snapshot_download

model_dir = snapshot_download("bodhan-ai/Indic-Transcribe-Flex")
sys.path.insert(0, model_dir)          # the model code ships inside the download

from indic_transcribe import IndicTranscribe
asr = IndicTranscribe.from_pretrained(model_dir)
print(asr("audio.wav", lang="hi"))
```

<h3 style="color:#FFD21E;">The three transcription modes</h3>

The same audio, three outputs. Pick the mode that matches what your downstream system expects.

**Native script**: everything in the language's own script. Recommended for production.

```python
print(asr("audio.wav", lang="hi", mode="native"))
# मैंने कल पांच बजे तीन फाइलें अपलोड कीं
```

**Mixed script (ITN)**: native words in native script; English words and numerals in Latin. Inverse text normalization turns spoken numbers into digits. Recommended if you want formatted and normalized output.

```python
print(asr("audio.wav", lang="hi", mode="mixed"))
# मैंने कल 5 बजे 3 files upload कीं
```

**Romanized**: everything transliterated into Latin script. Useful for search indexing, keyword spotting, and Latin-only UIs.

```python
print(asr("audio.wav", lang="hi", mode="romanized"))
# maine kal 5 baje 3 files upload kin
```

<h3 style="color:#FFD21E;">Automatic language ID + transcription</h3>

When you don't know the language ahead of time, omit `lang`. The model first identifies it, then transcribes at the cost of one decoder step, without requiring a second encoder pass.

```python
text, lid = asr.transcribe("unknown_language.wav", return_lid=True)
print(lid["lang"])   # e.g. "ta"
print(text)
```

A language you supply always wins; identification only fills a gap. `return_lid=True` also
works when you *did* supply one, so a disagreement between your metadata and the model stays
visible instead of silent:

```python
text, lid = asr.transcribe("audio.wav", lang="hi", return_lid=True)
# lid == {"lang": "hi", "source": "explicit", "topk": [("hi", 0.9999), ("ur", 0.0001), ...]}
```

<h3 style="color:#FFD21E;">Language identification only</h3>

To use the model purely as a language-ID system, read the predicted language and discard the transcript.

```python
for path in ["a.wav", "b.wav", "c.wav"]:
    print(path, asr.identify(path))
    # [('ta', 0.9812), ('ml', 0.0104), ('kn', 0.0031), ...]
```

`identify` returns the ranked distribution rather than a single string, because for the
confusable pairs the top-1 alone hides how close the decision was. Accuracy is uneven:
`ml`/`ta` 0.98 and `kn`/`bn` 0.96, against `bho` 0.05, `hi` 0.26, `mai` 0.36 and `ur` 0.49,
each absorbed by a close neighbour. If you have a language label, pass it.



<h3 style="color:#FFD21E;">Long audio</h3>

`asr(...)` decodes a file in one pass and refuses audio longer than 45 s. That limit is
deliberate: the model trains on clips of up to 30 s, and a single pass over long audio
collapses into repetition rather than degrading gracefully. For long audio, use the chunked
helper that ships with the model. It cuts the audio at natural pauses (or at exactly 30 s
when there is none) into pieces of at most 30 s, transcribes each, and joins the text:

```python
from long_form import transcribe_long

print(transcribe_long(asr, "long_audio.wav", lang="hi"))
```

Omit `lang` and the language is identified once, from samples across the whole file.
Pass it whenever you know it — it is faster and avoids a wrong guess.

Output modes work the same way on long audio — pass `mode="mixed"` or `mode="romanized"` to `transcribe_long`.

How the long-audio path works:

```text
audio (.wav / .flac / .mp3, any sample rate, mono or stereo)
  │  load → mono → 16 kHz
  ▼
lang given? ── no ──► identify it (long files: 3 × 20 s windows across the file)
  │
  ▼
≤ 30 s? ── yes ──► decode in one pass ───────────────────────────┐
  │ no                                                           │
  ▼                                                              │
split at pauses                                                  │
  • pause = ≥ 250 ms at least 25 dB below the file's peak        │
  • cut in the middle of the pause nearest 25 s                  │
  • no pause within 30 s → cut at exactly 30 s                   │
  ▼                                                              │
decode each piece (every piece ≤ 30 s)                           │
  • output looping? → split that piece at a pause, decode again  │
  • still looping?  → collapse the repeated phrase               │
  ▼                                                              │
join the pieces ─────────────────────────────────────────────────┴──► transcript
```

Pieces are kept as long as possible because every cut costs a little accuracy — the words
at a cut are the ones most likely to be wrong — and 30 s is the longest input the model
was trained on.

<h3 style="color:#FFD21E;">Command line</h3>

`inference.py` ships with the model and wraps the same calls. It picks the whole-file or
chunked path by duration, and identifies the language when `--lang` is omitted.

```bash
MODEL_DIR=$(python -c 'from huggingface_hub import snapshot_download; print(snapshot_download("bodhan-ai/Indic-Transcribe-Flex"))')

python "$MODEL_DIR/inference.py" audio.wav --lang hi
python "$MODEL_DIR/inference.py" long_call.wav --show-lang      # no --lang: identify it, and print it
python "$MODEL_DIR/inference.py" *.wav --lang ta                # several files
python "$MODEL_DIR/inference.py" audio.wav --lang hi --mode romanized
```

<h2 style="color:#FFD21E;">NeMo checkpoint</h2>

`nemo/` holds the same model as an NVIDIA NeMo checkpoint, for pipelines already built on NeMo.
Its config names the tokenizer class the model was trained with, which is not part of a stock
NeMo install, so `load_nemo` registers the copy that ships beside it before restoring:

```python
import sys
from huggingface_hub import snapshot_download

model_dir = snapshot_download("bodhan-ai/indic-transcribe-flex")
sys.path.insert(0, f"{model_dir}/nemo")      # the loader ships inside the download

from load_nemo import load_nemo_model
model = load_nemo_model(model_dir)
print(model.transcribe(["audio.wav"], source_lang="hi", target_lang="hi", pnc="yes")[0].text)
```

Nothing inside NeMo is modified, and the loader finds the checkpoint next to itself. If you
would rather not add anything to `sys.path`, copy `nemo/canary_multilingual_tokenizer.py` into
your NeMo install beside `canary_tokenizer.py` and `restore_from` the `.nemo` directly.

**Give it a language.** Pass any of the codes in *Full list of language codes* below as both
`source_lang` and `target_lang`:

```text
as  bho  bn  brx  doi  en  gu  hi  kn  kok  ks  mai  ml  mni
mr  ne  or  pa  sa  sat  sd  ta  te  ur
```

The checkpoint keeps one shared sub-tokenizer for all of them, and the class above routes every
code to it. Without it, stock NeMo raises `RuntimeError: Unsupported language: 'ml'`.

The NeMo path writes each language in its native script. The mixed and romanized modes are
available through the Hugging Face model above (`mode="mixed"` / `mode="romanized"`).

<h3 style="color:#FFD21E;">Command line</h3>

```bash
pip install "nemo_toolkit[asr]"

MODEL_DIR=$(python -c 'from huggingface_hub import snapshot_download; print(snapshot_download("bodhan-ai/indic-transcribe-flex"))')

python "$MODEL_DIR/nemo/test_nemo.py" audio.wav hi          # check the install
python "$MODEL_DIR/nemo/inference_nemo.py" audio.wav --lang hi
python "$MODEL_DIR/nemo/inference_nemo.py" long_call.wav --lang ta   # chunked automatically
python "$MODEL_DIR/nemo/inference_nemo.py" *.wav --lang bn --batch-size 8
```

<h3 style="color:#FFD21E;">Long audio</h3>

Audio over 30 s is cut at natural pauses into pieces of at most 30 s and decoded piece by
piece -- the same splitter, cap and repetition guard the Hugging Face model uses, so both
paths cut audio identically. `inference_nemo.py` does it automatically; in code:

```python
from long_form_nemo import transcribe_long_nemo

print(transcribe_long_nemo(model, "long_audio.wav", lang="hi", batch_size=8))
```

Batching the pieces makes this path the faster one for long audio: a 10-minute file takes
8 s at `batch_size=8` against 24 s at 1, and an hour of audio runs in 48 s (77x realtime,
9.2 GiB of GPU memory). Pass `lang` -- this path has no language identification of its own,
and a wrong language gives you the wrong script rather than an error.

---

<h2 id="inputs" style="color:#FFD21E;">Input(s)</h2>

| Field | Details |
| :--- | :--- |
| **Input Type(s)** | Audio, Language ID |
| **Input Format(s)** | `.wav`, `.flac`, `.mp3`; string language code |
| **Input Parameters** | One-dimensional (1D) audio; one-dimensional (1D) language ID |
| **Other Properties** | 16 kHz mono; audio is resampled automatically if it differs. Single speaker. |

---

<h2 id="output" style="color:#FFD21E;">Output</h2>

| Field | Details |
| :--- | :--- |
| **Output Type(s)** | Text string in the input language |
| **Output Format(s)** | String |
| **Output Parameters** | One-dimensional (1D) |
| **Other Properties** | Selectable native-script, mixed-script, or romanized rendering; optional detected-language tag. |

---

<h2 id="supported-language-codes" style="color:#FFD21E;">Supported Language Codes</h2>

Pass these to `source_lang`. Use `"auto"` for automatic language identification.

| Example | Value |
| --- | --- |
| Hindi | `source_lang="hi"` |
| Tamil | `source_lang="ta"` |
| Bengali | `source_lang="bn"` |
| Indian English | `source_lang="en"` |
| Auto-detect | `source_lang="auto"` |

All 27 languages use standard ISO 639-1 / 639-3 codes (also listed in the `language:` field at the top of this card).

<details>
<summary>Full list of language codes (27)</summary>

| Language | Code | Script | Group |
| --- | --- | --- | --- |
| English (Indian) | `en` | Latin | Indian-accented English |
| Assamese | `as` | Bengali–Assamese | Scheduled |
| Bengali | `bn` | Bengali | Scheduled |
| Bodo | `brx` | Devanagari | Scheduled |
| Dogri | `doi` | Devanagari | Scheduled |
| Gujarati | `gu` | Gujarati | Scheduled |
| Hindi | `hi` | Devanagari | Scheduled |
| Kannada | `kn` | Kannada | Scheduled |
| Kashmiri | `ks` | Perso-Arabic / Devanagari | Scheduled |
| Konkani | `kok` | Devanagari | Scheduled |
| Maithili | `mai` | Devanagari | Scheduled |
| Malayalam | `ml` | Malayalam | Scheduled |
| Manipuri | `mni` | Bengali / Meetei Mayek | Scheduled |
| Marathi | `mr` | Devanagari | Scheduled |
| Nepali | `ne` | Devanagari | Scheduled |
| Odia | `or` | Odia | Scheduled |
| Punjabi | `pa` | Gurmukhi | Scheduled |
| Sanskrit | `sa` | Devanagari | Scheduled |
| Santali | `sat` | Ol Chiki | Scheduled |
| Sindhi | `sd` | Perso-Arabic / Devanagari | Scheduled |
| Tamil | `ta` | Tamil | Scheduled |
| Telugu | `te` | Telugu | Scheduled |
| Urdu | `ur` | Perso-Arabic | Scheduled |
| Bhojpuri | `bho` | Devanagari | Hindi dialect |
| Chhattisgarhi | `hne` | Devanagari | Hindi dialect |
| Haryanvi | `bgc` | Devanagari | Hindi dialect |
| Bhili | `bhb` | Devanagari | Low resource |

</details>

---

<h2 id="limitations" style="color:#FFD21E;">Limitations</h2>

- **Single-speaker audio.** The model is trained for single-speaker recordings. For multi-speaker scenarios, pair it with a diarization module and transcribe each speaker turn separately.
- **Mixed-script (ITN) mode can be wrong.** Inverse text normalization is genuinely ambiguous in places, so mixed-script mode will occasionally get it wrong. For production, native-script mode is recommended, applying your own ITN downstream if you need it.
- **Romanization is not standardized.** There is no single canonical romanization for most Indian languages. Romanized output follows the model's learned convention, which may not match your existing transliteration scheme.
- **Streaming is not available in `pro`.** Use Indic-Transcribe-lite for real-time use.
- **Low-resource languages are weaker.** Bhili in particular has very little training data. Check the per-language numbers in [Results at a Glance](#results-at-a-glance) before committing to a language.
- **Noise robustness has limits.** Heavily overlapped speech, far-field audio, and very low-SNR recordings will still degrade quality.

---

<h2 id="license--terms-of-use" style="color:#FFD21E;">License / Terms of Use</h2>

Released under [Indic Open Model License v1.0](Bodhan_AI_Open_Model_License.md).

The base model, [nvidia/canary-1b-v2](https://huggingface.co/nvidia/canary-1b-v2), carries its own license terms — ensure your use complies with both.

---

*If you find the license difficult to understand, here is a plain-language guide to the Indic Open Model License.*

Broad, no-cost access for research, government, nonprofit, and commercial use — with a few conditions attached.

> **This deed is a human-readable summary of the license, not a substitute for it.** Where the two disagree, the full **Indic Open Model License** governs.

---

## You're free to

No cost, no royalty, worldwide — for research, government, nonprofit, and commercial use, at any scale.

- ✅ **Run it** — for inference, in a product, in research, however you like.
- ✅ **Change it** — fine-tune, distill, quantize, merge, or otherwise build on it.
- ✅ **Self-host it** — power your own product or service with it, commercial or not.
- ✅ **Share it** — pass on copies of the model or your own version of it.

---

## As long as you

Five conditions cover almost everything. The rest of the license is these, spelled out in legal detail.

### 1. Give credit

Wherever you ship the model or a derivative to anyone else, say where it came from — and don't strip out existing notices.

```
"Built with [Model Name] from Bodhan AI / AI4Bharat."
```

### 2. Pass it on the same way

If you give your fine-tuned or derived version to anyone else — hand it over, or run it as a service for them — it carries this exact license. You can't relicense it on different terms.

### 3. Ask before hosting it for others

Self-hosting is free. But if you're going to run it as an API or hosted service that *other people or companies* call directly, that needs Bodhan AI's written sign-off first — unless you're a nonprofit, government, or academic user, or you publicly release an equally capable open version within 90 days.

### 4. Don't use it to cause harm

No exceptions — not even for nonprofit or research use. That means no:

- child sexual abuse material, or content that sexualizes minors
- weapons development, including chemical, biological, radiological, or nuclear
- mass surveillance or social-scoring systems
- disinformation campaigns, including election manipulation
- automated decisions that affect someone's legal rights without human oversight
- deepfakes or voice clones of real people without their consent
- robocalls, auto-dialers, or voice-phishing scams
- AI companion products designed to simulate romance or foster emotional dependency

### 5. Talk to us if your product gets huge

If your product, built for your own use rather than hosting for others, crosses either threshold, you will need a separate commercial license. This does not apply to nonprofit, government, or academic users.

| Threshold | |
|---|---|
| **500M+** | monthly active users |
| | *or* |
| **$250M+** | annual revenue |

---

## Good to know

- **No warranty.** The model is provided as-is. It isn't tested or certified for safety-critical use — medical, aviation, nuclear, or similar so test thoroughly before relying on it in high-stakes settings.
- **You handle your own compliance.** Export controls, sanctions, and data-protection law (including India's DPDP Act, where it applies) are on you, not Bodhan AI.
- **This deed doesn't replace the license.** It leaves out most of the legal detail — termination, dispute resolution, confidentiality, and more all live in the full text. Read that before you rely on anything here.

---

<h2 id="use-case" style="color:#FFD21E;">Use Case</h2>

Transcription of multilingual and code-mixed Indian-language audio, including native-script, mixed-script, and romanized output, plus language identification.

---

<h2 id="deployment-geography" style="color:#FFD21E;">Deployment Geography</h2>

Global

---

<h2 id="citation" style="color:#FFD21E;">Citation</h2>

```bibtex
@misc{indictranscribe2026,
  title  = {Indic-Transcribe: Built for the way India actually speaks},
  author = {Bodhan AI, AI4Bharat},
  year   = {2026},
  url    = {https://bodhan.ai/research/blogs/indic-transcribe}
}
```

---

<h2 id="ethical-considerations" style="color:#FFD21E;">Ethical Considerations</h2>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Developers should work with their team to ensure this model meets requirements for the relevant industry and use case, and addresses unforeseen product misuse.

### S9 downloaded card: `indic-transcribe-core/README.md` (verbatim)

---
extra_gated_prompt: "Please provide your details and agree to the [LICENSE](https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License.md) [[simpler version](https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License_Deed.md)] to request access."
extra_gated_fields:
  Company / Organization: text
  Country: country
  Intended Use Case:
    type: select
    options:
      - Research
      - Commercial
      - Education
      - label: Other
        value: other
  I agree to the license terms: checkbox
language:
- en
- as
- bn
- brx
- doi
- gu
- hi
- kn
- ks
- kok
- mai
- ml
- mni
- mr
- ne
- or
- pa
- sa
- sat
- sd
- ta
- te
- ur
- bho
- bhb
library_name: transformers
pipeline_tag: automatic-speech-recognition
base_model: nvidia/canary-1b-v2
tags:
- automatic-speech-recognition
- speech
- audio
- asr
- multilingual
- indic
- code-switching
- code-mixing
- language-identification
- canary
- fastconformer
metrics:
- wer
- cer
license: other
---

<div align="center">
  <img src="banner.png" alt="Indic-Transcribe-core Banner">
</div>

<h1 id="indic-transcribe-core" style="color:#FFD21E;">Indic-Transcribe-core</h1>

<div align="center">

[![Model Arch](https://img.shields.io/badge/Model_Arch-FastConformer--Transformer-C1440E?style=flat#model-badge)](#model-architecture)
[![Params](https://img.shields.io/badge/Params-1.2B-C1440E?style=flat#model-badge)](#model-architecture)
[![Languages](https://img.shields.io/badge/Languages-25-C1440E?style=flat#model-badge)](#supported-languages)
[![Language](https://img.shields.io/badge/Language-Multilingual-C1440E?style=flat#model-badge)](#supported-languages)
[![License](https://img.shields.io/badge/License-Indic%20Open%20Model%20License%20v1.0-C1440E?style=flat#model-badge)](#license--terms-of-use)


</div>

**Multilingual speech recognition for 25 Indian languages, in each language's native script.**

**Indic-Transcribe-core** is a multilingual Automatic Speech Recognition (ASR) model built for **25 Indian languages**. It is trained to be robust and general purpose: it handles the full diversity of Indian accents and holds up in noisy real-world conditions, from crowded markets to call-center floors, with strong coverage in the domains where Indian voice products are actually built — education, agriculture, and healthcare.

The model transcribes into the native script of the language being spoken, and can identify the language on its own when you don't know it in advance.

This model is ready for commercial use.

---

<h2 id="why-choose-indic-transcribe" style="color:#FFD21E;">Why Choose Indic-Transcribe-core?</h2>

- 🔀 **Code-mixing, natively.** Indians rarely speak one language at a time. Indic-Transcribe-core transcribes Hinglish and other mixed speech as it is actually spoken, instead of forcing it into a single language.
- 🌐 **Language identification built in.** Use the model directly as a language-ID system, or let it auto-detect the language and then transcribe — at the cost of one decoder step, not a second encoder pass.
- 🏥 **Domain coverage where it matters.** Deep vocabulary in education, agriculture, and healthcare.

---

<h2 id="supported-languages" style="color:#FFD21E;">Supported Languages</h2>

The model covers **25 languages** across four groups:

| Group | Languages |
| --- | --- |
| **Indian-accented English** | English |
| **22 constitutionally recognised languages** | Assamese, Bengali, Bodo, Dogri, Gujarati, Hindi, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, Odia, Punjabi, Sanskrit, Santali, Sindhi, Tamil, Telugu, Urdu |
| **Hindi dialect** | Bhojpuri |
| **Low resource** | Bhili |

---

<h2 id="model-architecture" style="color:#FFD21E;">Model Architecture</h2>

**Architecture Type:** NVIDIA Canary: FastConformer encoder with a Transformer decoder.

Indic-Transcribe-core is built on the [nvidia/canary-1b-v2](https://huggingface.co/nvidia/canary-1b-v2) architecture. The FastConformer encoder produces acoustic representations that the Transformer decoder converts into text, with task tokens selecting the target language.

|  |  |
| --- | --- |
| **Model name** | Indic-Transcribe-core |
| **Task** | Speech-to-Text (Automatic Speech Recognition) |
| **Base model** | [nvidia/canary-1b-v2](https://huggingface.co/nvidia/canary-1b-v2) |
| **Total parameters** | 1.2B |
| **Encoder** | FastConformer: 32 layers, 811M params, 1024 hidden dim, 8 attention heads, conv kernel 9 |
| **Decoder** | Transformer: 24 layers, 419M params, 1024 hidden size, 8 attention heads |
| **Vocabulary** | 7,152 tokens (1,152 special / task + 6,000 multilingual) |
| **Sub-word algorithm** | BPE (byte fallback disabled) |
| **Precision** | fp32 on disk, bf16 at inference |
| **Checkpoint size** | 4.6 GB |

<h3 style="color:#FFD21E;">Capabilities</h3>

| Feature | Indic-Transcribe-core |
| --- | :---: |
| Languages | 25 |
| Code-mixed audio | ✅ |
| Transcription output | Native script |
| Automatic language ID | ✅ |

---

<h2 id="results-at-a-glance" style="color:#FFD21E;">Results at a Glance</h2>

Accuracy is reported as **OIWER** — an orthographically-informed word error rate that accepts documented spelling and transliteration variants as correct, scored against multi-reference transcripts. **Lower is better.**

<h3 style="color:#FFD21E;">Voice of India benchmark</h3>

| Model | Average | Assamese | Bhojpuri | Bengali | Gujarati | Hindi | Chhattisgarhi | Kannada | Maithili | Malayalam | Marathi | Odia | Punjabi | Tamil | Telugu | Urdu |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Indic-Transcribe-core** | 8.7 | 8.2 | 13.3 | 4.3 | 9.2 | 3.5 | 13.6 | 7.4 | 11.3 | 11.5 | 5.7 | 8.7 | 8.3 | 9.0 | 11.4 | 5.0 |
| Saaras V3 | 10.7 | 9.1 | 17.9 | 5.2 | 9.7 | 3.8 | 14.0 | 8.8 | 14.2 | 12.2 | 6.5 | 11.1 | 8.6 | 9.1 | 13.5 | 7.5 |
| **Indic-Transcribe-flex** | 11.3 | 9.6 | 18.5 | 5.0 | 10.8 | 4.1 | 13.6 | 9.7 | 15.1 | 13.7 | 6.6 | 10.2 | 9.5 | 10.8 | 13.1 | 5.6 |
| Indic Conformer | 17.8 | 13.1 | 30.3 | 9.5 | 16.3 | 6.5 | 24.5 | 16.3 | 16.3 | 28.2 | 11.6 | 13.1 | 19.1 | 16.2 | 20.0 | 8.0 |
| Gemini 3 Pro | 21.1 | 23.7 | 24.1 | 10.3 | 18.1 | 9.3 | 19.6 | 20.1 | 27.2 | 21.0 | 14.0 | 25.7 | 19.3 | 15.5 | 24.6 | 10.6 |
| Gemini 3 Flash | 23.1 | 25.0 | 20.2 | 11.1 | 20.3 | 7.1 | 21.7 | 18.5 | 28.0 | 30.1 | 14.2 | 23.3 | 23.2 | 17.3 | 25.5 | 11.0 |
| Gemma E4B | 36.1 | 45.0 | 27.0 | 19.6 | 27.3 | 9.1 | 24.0 | 31.0 | 36.7 | 44.4 | 24.4 | 44.4 | 23.4 | 37.9 | 41.6 | 14.2 |
| OmniASR LLM 7B | 44.5 | 23.9 | 26.3 | 20.9 | 32.0 | 9.6 | 20.7 | 35.0 | 44.6 | 48.8 | 24.5 | 72.3 | 31.7 | 40.6 | 48.7 | 14.8 |
| OmniASR CTC 7B | 62.5 | 33.3 | 39.2 | 43.5 | 62.5 | 20.7 | 33.4 | 50.0 | 51.6 | 61.3 | 33.6 | 90.2 | 80.7 | 58.3 | 62.1 | 89.3 |

Indic-Transcribe Core offers better accuracy. Do check out [Indic-Transcribe Flex](https://huggingface.co/bodhan-ai/indic-transcribe-flex) for support for more transcription modes and languages. 

---


<h2 id="how-to-use-this-model" style="color:#FFD21E;">How to Use this Model</h2>

<h3 style="color:#FFD21E;">Installation</h3>

```bash
pip install torch torchaudio transformers sentencepiece soundfile
```

The model code ships inside this repository, so there is nothing else to install — no NeMo,
no other toolkit.

<details>
<summary>Conda environment (recommended for reproducibility)</summary>

```bash
conda create -n indic-transcribe python=3.10 -y
conda activate indic-transcribe
pip install torch torchaudio transformers sentencepiece soundfile
```

</details>

<h3 style="color:#FFD21E;">Input audio requirements</h3>

|  |  |
| --- | --- |
| Sample rate | 16 kHz (resampled automatically if it differs) |
| Channels | Mono |
| Formats | `.wav`, `.flac`, `.mp3` |
| Speakers | Single speaker — see [Limitations](#limitations) |

```bash
# Convert anything to the expected format
ffmpeg -i input.mp3 -ac 1 -ar 16000 -c:a pcm_s16le audio.wav
```

<h3 style="color:#FFD21E;">Basic inference</h3>

```python
# Gated model: accept the terms on this page, then run `hf auth login` once (older installs: `huggingface-cli login`).
import sys
from huggingface_hub import snapshot_download

model_dir = snapshot_download("bodhan-ai/indic-transcribe-core")
sys.path.insert(0, model_dir)          # the model code ships inside the download

from indic_transcribe import IndicTranscribe
asr = IndicTranscribe.from_pretrained(model_dir)
print(asr("audio.wav", lang="hi"))
# मैंने कल पांच बजे तीन फाइलें अपलोड कीं
```

Output is always in the native script of the language being transcribed.

<h3 style="color:#FFD21E;">Automatic language ID + transcription</h3>

When you don't know the language ahead of time, omit `lang`. The model identifies it first,
then transcribes — at the cost of one decoder step, not a second encoder pass.

```python
text, lid = asr.transcribe("unknown_language.wav", return_lid=True)
print(lid["lang"])   # e.g. "ta"
print(text)
```

A language you supply always wins; identification only fills a gap. `return_lid=True` also
works when you *did* supply one, so a disagreement between your metadata and the model stays
visible instead of silent:

```python
text, lid = asr.transcribe("audio.wav", lang="hi", return_lid=True)
# lid == {"lang": "hi", "source": "explicit", "topk": [("hi", 0.9999), ("ur", 0.0001), ...]}
```

<h3 style="color:#FFD21E;">Language identification only</h3>

To use the model purely as a language-ID system, read the predicted language and discard the transcript.

```python
for path in ["a.wav", "b.wav", "c.wav"]:
    print(path, asr.identify(path))
    # [('ta', 0.9812), ('ml', 0.0104), ('kn', 0.0031), ...]
```

`identify` returns the ranked distribution rather than a single string, because for the
confusable pairs the top-1 alone hides how close the decision was. Accuracy is uneven across
languages — the Hindi-belt languages in particular are often absorbed by Hindi. If you have a
language label, pass it.

You can narrow the candidate set when you know your traffic:

```python
from indic_transcribe import RECOMMENDED_LANGS

asr.identify("audio.wav", allowed_langs=RECOMMENDED_LANGS)
```

This is a hard filter — audio in an excluded language is silently reassigned to the nearest
permitted one rather than flagged.

<h3 style="color:#FFD21E;">Long audio</h3>

`asr(...)` decodes a file in one pass and refuses audio longer than 45 s. That limit is
deliberate: the model trains on clips of up to 30 s, and a single pass over long audio
collapses into repetition rather than degrading gracefully. For long audio, use the chunked
helper that ships with the model. It cuts the audio at natural pauses (or at exactly 30 s
when there is none) into pieces of at most 30 s, transcribes each, and joins the text:

```python
from long_form import transcribe_long

print(transcribe_long(asr, "long_audio.wav", lang="hi"))
```

Omit `lang` and the language is identified once, from samples across the whole file.
Pass it whenever you know it — it is faster and avoids a wrong guess.

How the long-audio path works:

```text
audio (.wav / .flac / .mp3, any sample rate, mono or stereo)
  │  load → mono → 16 kHz
  ▼
lang given? ── no ──► identify it (long files: 3 × 20 s windows across the file)
  │
  ▼
≤ 30 s? ── yes ──► decode in one pass ───────────────────────────┐
  │ no                                                           │
  ▼                                                              │
split at pauses                                                  │
  • pause = ≥ 250 ms at least 25 dB below the file's peak        │
  • cut in the middle of the pause nearest 25 s                  │
  • no pause within 30 s → cut at exactly 30 s                   │
  ▼                                                              │
decode each piece (every piece ≤ 30 s)                           │
  • output looping? → split that piece at a pause, decode again  │
  • still looping?  → collapse the repeated phrase               │
  ▼                                                              │
join the pieces ─────────────────────────────────────────────────┴──► transcript
```

Pieces are kept as long as possible because every cut costs a little accuracy — the words
at a cut are the ones most likely to be wrong — and 30 s is the longest input the model
was trained on.

<h3 style="color:#FFD21E;">Command line</h3>

`inference.py` ships with the model and wraps the same calls. It picks the whole-file or
chunked path by duration, and identifies the language when `--lang` is omitted.

```bash
MODEL_DIR=$(python -c 'from huggingface_hub import snapshot_download; print(snapshot_download("bodhan-ai/indic-transcribe-core"))')

python "$MODEL_DIR/inference.py" audio.wav --lang hi
python "$MODEL_DIR/inference.py" long_call.wav --show-lang      # no --lang: identify it, and print it
python "$MODEL_DIR/inference.py" *.wav --lang ta                # several files
```

<h2 style="color:#FFD21E;">NeMo checkpoint</h2>

`nemo/` holds the same model as an NVIDIA NeMo checkpoint, for pipelines already built on NeMo.
Its config names the tokenizer class the model was trained with, which is not part of a stock
NeMo install, so `load_nemo` registers the copy that ships beside it before restoring:

```python
import sys
from huggingface_hub import snapshot_download

model_dir = snapshot_download("bodhan-ai/indic-transcribe-core")
sys.path.insert(0, f"{model_dir}/nemo")      # the loader ships inside the download

from load_nemo import load_nemo_model
model = load_nemo_model(model_dir)
print(model.transcribe(["audio.wav"], source_lang="hi", target_lang="hi", pnc="yes")[0].text)
```

Nothing inside NeMo is modified, and the loader finds the checkpoint next to itself. If you
would rather not add anything to `sys.path`, copy `nemo/canary_multilingual_tokenizer.py` into
your NeMo install beside `canary_tokenizer.py` and `restore_from` the `.nemo` directly.

**Give it a language.** Pass any of the codes in *Full list of language codes* below as both
`source_lang` and `target_lang`:

```text
as  bho  bn  brx  doi  en  gu  hi  kn  kok  ks  mai  ml  mni
mr  ne  or  pa  sa  sat  sd  ta  te  ur
```

The checkpoint keeps one shared sub-tokenizer for all of them, and the class above routes every
code to it. Without it, stock NeMo raises `RuntimeError: Unsupported language: 'ml'`. This
checkpoint writes each language in its native script.

<h3 style="color:#FFD21E;">Command line</h3>

```bash
pip install "nemo_toolkit[asr]"

MODEL_DIR=$(python -c 'from huggingface_hub import snapshot_download; print(snapshot_download("bodhan-ai/indic-transcribe-core"))')

python "$MODEL_DIR/nemo/test_nemo.py" audio.wav hi          # check the install
python "$MODEL_DIR/nemo/inference_nemo.py" audio.wav --lang hi
python "$MODEL_DIR/nemo/inference_nemo.py" long_call.wav --lang ta   # chunked automatically
python "$MODEL_DIR/nemo/inference_nemo.py" *.wav --lang bn --batch-size 8
```

<h3 style="color:#FFD21E;">Long audio</h3>

Audio over 30 s is cut at natural pauses into pieces of at most 30 s and decoded piece by
piece -- the same splitter, cap and repetition guard the Hugging Face model uses, so both
paths cut audio identically. `inference_nemo.py` does it automatically; in code:

```python
from long_form_nemo import transcribe_long_nemo

print(transcribe_long_nemo(model, "long_audio.wav", lang="hi", batch_size=8))
```

Batching the pieces makes this path the faster one for long audio: a 10-minute file takes
8 s at `batch_size=8` against 24 s at 1, and an hour of audio runs in 48 s (77x realtime,
9.2 GiB of GPU memory). Pass `lang` -- this path has no language identification of its own,
and a wrong language gives you the wrong script rather than an error.

---

<h2 id="inputs" style="color:#FFD21E;">Input(s)</h2>

| Field | Details |
| :--- | :--- |
| **Input Type(s)** | Audio, Language ID |
| **Input Format(s)** | `.wav`, `.flac`, `.mp3`; string language code |
| **Input Parameters** | One-dimensional (1D) audio; one-dimensional (1D) language ID |
| **Other Properties** | 16 kHz mono; audio is resampled automatically if it differs. Single speaker. |

---

<h2 id="output" style="color:#FFD21E;">Output</h2>

| Field | Details |
| :--- | :--- |
| **Output Type(s)** | Text string in the input language |
| **Output Format(s)** | String |
| **Output Parameters** | One-dimensional (1D) |
| **Other Properties** | Native-script rendering; optional detected-language tag. |

---


<h2 id="supported-language-codes" style="color:#FFD21E;">Supported Language Codes</h2>

Pass these to `lang`. Omit `lang` for automatic language identification.

| Example | Value |
| --- | --- |
| Hindi | `lang="hi"` |
| Tamil | `lang="ta"` |
| Bengali | `lang="bn"` |
| Indian English | `lang="en"` |
| Auto-detect | omit `lang` |

All 25 languages use standard ISO 639-1 / 639-3 codes (also listed in the `language:` field at the top of this card).

<details>
<summary>Full list of language codes (25)</summary>

| Language | Code | Script | Group |
| --- | --- | --- | --- |
| English (Indian) | `en` | Latin | Indian-accented English |
| Assamese | `as` | Bengali–Assamese | Scheduled |
| Bengali | `bn` | Bengali | Scheduled |
| Bodo | `brx` | Devanagari | Scheduled |
| Dogri | `doi` | Devanagari | Scheduled |
| Gujarati | `gu` | Gujarati | Scheduled |
| Hindi | `hi` | Devanagari | Scheduled |
| Kannada | `kn` | Kannada | Scheduled |
| Kashmiri | `ks` | Perso-Arabic / Devanagari | Scheduled |
| Konkani | `kok` | Devanagari | Scheduled |
| Maithili | `mai` | Devanagari | Scheduled |
| Malayalam | `ml` | Malayalam | Scheduled |
| Manipuri | `mni` | Bengali / Meetei Mayek | Scheduled |
| Marathi | `mr` | Devanagari | Scheduled |
| Nepali | `ne` | Devanagari | Scheduled |
| Odia | `or` | Odia | Scheduled |
| Punjabi | `pa` | Gurmukhi | Scheduled |
| Sanskrit | `sa` | Devanagari | Scheduled |
| Santali | `sat` | Ol Chiki | Scheduled |
| Sindhi | `sd` | Perso-Arabic / Devanagari | Scheduled |
| Tamil | `ta` | Tamil | Scheduled |
| Telugu | `te` | Telugu | Scheduled |
| Urdu | `ur` | Perso-Arabic | Scheduled |
| Bhojpuri | `bho` | Devanagari | Hindi dialect |
| Bhili | `bhb` | Devanagari | Low resource |

</details>

---

<h2 id="limitations" style="color:#FFD21E;">Limitations</h2>

- **Native script only.** This model transcribes into the language's own script. It does not produce mixed-script/ITN or romanized output — spoken numbers stay as words, and English words inside Indic speech are rendered in the native script. Apply your own inverse text normalization or transliteration downstream if you need it.
- **Single-speaker audio.** The model is trained for single-speaker recordings. For multi-speaker scenarios, pair it with a diarization module and transcribe each speaker turn separately.
- **Automatic language ID is uneven — do not rely on it for Hindi-belt languages.** Accuracy varies widely by language, and Bhojpuri, Maithili and Urdu are absorbed by Hindi far too often to be trusted. Pass `lang` explicitly whenever you have it.

---

<h2 id="license--terms-of-use" style="color:#FFD21E;">License / Terms of Use</h2>

Released under [Indic Open Model License v1.0](Bodhan_AI_Open_Model_License.md).

The base model, [nvidia/canary-1b-v2](https://huggingface.co/nvidia/canary-1b-v2), carries its own license terms — ensure your use complies with both.

*If you find the license difficult to understand, here is a plain-language guide to the Indic Open Model License.*

Broad, no-cost access for research, government, nonprofit, and commercial use — with a few conditions attached.

> **This deed is a human-readable summary of the license, not a substitute for it.** Where the two disagree, the full **Indic Open Model License** governs.

---

## You're free to

No cost, no royalty, worldwide — for research, government, nonprofit, and commercial use, at any scale.

- ✅ **Run it** — for inference, in a product, in research, however you like.
- ✅ **Change it** — fine-tune, distill, quantize, merge, or otherwise build on it.
- ✅ **Self-host it** — power your own product or service with it, commercial or not.
- ✅ **Share it** — pass on copies of the model or your own version of it.

---

## As long as you

Five conditions cover almost everything. The rest of the license is these, spelled out in legal detail.

### 1. Give credit

Wherever you ship the model or a derivative to anyone else, say where it came from — and don't strip out existing notices.

```
"Built with [Model Name] from Bodhan AI / AI4Bharat."
```

### 2. Pass it on the same way

If you give your fine-tuned or derived version to anyone else — hand it over, or run it as a service for them — it carries this exact license. You can't relicense it on different terms.

### 3. Ask before hosting it for others

Self-hosting is free. But if you're going to run it as an API or hosted service that *other people or companies* call directly, that needs Bodhan AI's written sign-off first — unless you're a nonprofit, government, or academic user, or you publicly release an equally capable open version within 90 days.

### 4. Don't use it to cause harm

No exceptions — not even for nonprofit or research use. That means no:

- child sexual abuse material, or content that sexualizes minors
- weapons development, including chemical, biological, radiological, or nuclear
- mass surveillance or social-scoring systems
- disinformation campaigns, including election manipulation
- automated decisions that affect someone's legal rights without human oversight
- deepfakes or voice clones of real people without their consent
- robocalls, auto-dialers, or voice-phishing scams
- AI companion products designed to simulate romance or foster emotional dependency

### 5. Talk to us if your product gets huge

If your own product built on this — not through hosting it for others, that's covered above — crosses either threshold, you'll need a separate commercial license. Doesn't apply to nonprofit, government, or academic users.

| Threshold | |
|---|---|
| **500M+** | monthly active users |
| | *or* |
| **$250M+** | annual revenue |

---

## Good to know

- **No warranty.** The model is provided as-is. It isn't tested or certified for safety-critical use — medical, aviation, nuclear, or similar — so test thoroughly before relying on it in high-stakes settings.
- **You handle your own compliance.** Export controls, sanctions, and data-protection law (including India's DPDP Act, where it applies) are on you, not Bodhan AI.
- **This deed doesn't replace the license.** It leaves out most of the legal detail — termination, dispute resolution, confidentiality, and more all live in the full text. Read that before you rely on anything here.

---

<h2 id="use-case" style="color:#FFD21E;">Use Case</h2>

Native-script transcription of multilingual and code-mixed Indian-language audio, plus language identification.

---

<h2 id="deployment-geography" style="color:#FFD21E;">Deployment Geography</h2>

Global

---

<h2 id="citation" style="color:#FFD21E;">Citation</h2>

```bibtex
@misc{indictranscribe2026,
  title  = {Indic-Transcribe: Built for the way India actually speaks},
  author = {Bodhan AI, AI4Bharat},
  year   = {2026},
  url    = {https://bodhan.ai/research/blogs/indic-transcribe}
}
```

---

<h2 id="ethical-considerations" style="color:#FFD21E;">Ethical Considerations</h2>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Developers should work with their team to ensure this model meets requirements for the relevant industry and use case, and addresses unforeseen product misuse.

### S9 downloaded card: `indic-speak/README.md` (verbatim)

---
extra_gated_prompt: "Please provide your details and agree to the [LICENSE](https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License.md) [[simpler version](https://github.com/Bodhan-AI/bodhan-model-info/blob/main/licenses/indic-open-model-license/v1/Indic_Open_Model_License_Deed.md)] to request access."
extra_gated_fields:
  Company / Organization: text
  Country: country
  Intended Use Case:
    type: select
    options:
      - Research
      - Commercial
      - Education
      - label: Other
        value: other
  I agree to the license terms: checkbox
base_model: meta-llama/Llama-3.2-3B
language:
- en
- hi
- bn
- mr
- te
- ta
- gu
- kn
- ml
- or
- pa
- as
- ur
- brx
- doi
- kok
- ks
- mai
- ne
- mni
- sa
- sat
- sd
library_name: transformers
pipeline_tag: text-to-speech
tags:
- text-to-speech
- tts
- speech
- audio
- indic
- multilingual
- code-switching
- code-mixing
- stem
- education
- indic-speak
metrics:
- wer
- cer
- mos
license: other
---

<div align="center">
  <img src="banner.png" alt="Indic-Speak banner">
</div>

<div align="center">

[![Task](https://img.shields.io/badge/Task-Text--to--Speech-C1440E?style=flat#model-badge)](#what-is-indic-speak)
[![Languages](https://img.shields.io/badge/Languages-23-C1440E?style=flat#model-badge)](#languages-supported)
[![Language](https://img.shields.io/badge/Language-Multilingual-C1440E?style=flat#model-badge)](#languages-supported)
[![Latency](https://img.shields.io/badge/Latency-~200ms-C1440E?style=flat#model-badge)](#quality--performance)
[![License](https://img.shields.io/badge/License-Indic%20Open%20Model%20License%20v1.0-C1440E?style=flat#model-badge)](#license--terms-of-use)

</div>

**Natural-sounding text-to-speech for 22 Indian languages and English — built for the classroom first.**

---

<h2 id="what-is-indic-speak" style="color:#C1440E;">What is Indic-Speak?</h2>

Indic-Speak turns written text into natural-sounding speech across 22 Indian languages and English. It is a general-purpose voice engine — you can use it for an app, a helpline, an audiobook, or anything else that needs to talk. But it was built with one audience in mind first: students.

Most of the effort went into two problems that matter enormously in Indian education and that almost every other voice system handles badly — reading STEM content correctly, and reading sentences that mix an Indian language with English. The result is a voice that sounds like a teacher explaining something, rather than a machine reading a list. That difference is subtle in a single sentence and very obvious across a ten-minute lesson.

---

<h2 id="key-features" style="color:#C1440E;">Key Features</h2>

<h3 style="color:#C1440E;">Built for students first</h3>

- **STEM content that is actually correct.** Equations, units, fractions, exponents, and chemical formulae are read the way a teacher reads them in a classroom.
- **Code-mixed speech, read naturally.** Indian teaching is rarely in one language; Indic-Speak reads mixed sentences in one continuous voice.
- **Paced for comprehension.** The default delivery is explanatory and unhurried rather than brisk and announcement-like.

<h3 style="color:#C1440E;">Capabilities and use cases</h3>

Indic-Speak provides several voices per production language, spanning gender, age, and region. English terms, acronyms, and numerals sitting inside an Indic sentence are read in the surrounding voice and accent. Beyond education, the engine serves:

- **Audiobooks and long-form narration.** Quality and pacing stay consistent across chapter-length material.
- **Apps and product voice.** Notifications, walkthroughs, and in-app guidance.
- **Conversational agents and helplines.** Fast response times for back-and-forth conversation.
- **Accessibility.** Screen reading for users who cannot or prefer not to read.

<h3 style="color:#C1440E;">Voices and data integrity</h3>

- **Professionally recorded voices.** Every voice comes from a contracted voice artist who consented to its use.
- **Curriculum-aligned content.** Training material spans mathematics, science, and technical explanation.

---

<h2 id="quality--performance" style="color:#C1440E;">Quality &amp; Performance</h2>

| Measure | What it tells you | Result |
| --- | --- | --- |
| Intelligibility (WER / CER) | How reliably a listener can make out every word | 26.49 / 17.86 |
| Voice consistency | Whether the voice stays the same across a long passage | 96.47 ± 1.64 |
| Overall quality (NORESQA MOS) | A standard automated quality score | 4.46 ± 0.26 |
| Response time | Delay before audio starts | ~200 ms |

> For WER / CER, lower is better. For voice consistency and MOS, higher is better.

---

<h2 id="languages-supported" style="color:#C1440E;">Languages Supported</h2>

| Tier | Languages |
| --- | --- |
| **Production (13)** | English, Hindi, Bengali, Marathi, Telugu, Tamil, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamese, Urdu |
| **Preview (10)** | Bodo, Dogri, Konkani, Kashmiri, Maithili, Nepali, Manipuri, Sanskrit, Santali, Sindhi |

<details>
<summary>Language codes</summary>

| Language | Code | Tier |
| --- | --- | --- |
| English | `en` | Production |
| Hindi | `hi` | Production |
| Bengali | `bn` | Production |
| Marathi | `mr` | Production |
| Telugu | `te` | Production |
| Tamil | `ta` | Production |
| Gujarati | `gu` | Production |
| Kannada | `kn` | Production |
| Malayalam | `ml` | Production |
| Odia | `or` | Production |
| Punjabi | `pa` | Production |
| Assamese | `as` | Production |
| Urdu | `ur` | Production |
| Bodo | `brx` | Preview |
| Dogri | `doi` | Preview |
| Konkani | `kok` | Preview |
| Kashmiri | `ks` | Preview |
| Maithili | `mai` | Preview |
| Nepali | `ne` | Preview |
| Manipuri | `mni` | Preview |
| Sanskrit | `sa` | Preview |
| Santali | `sat` | Preview |
| Sindhi | `sd` | Preview |

</details>

---

<h2 id="how-to-use" style="color:#C1440E;">How to Use</h2>

```
pip install "transformers>=5" torch snac soundfile
```

<h3 style="color:#C1440E;">In a script</h3>

```python
from inference import TTS

tts = TTS("bodhan-ai/indic-speak-preview-v2")   # or a local dir; loads once
wav = tts("प्रकाश की चाल लगभग तीन लाख किलोमीटर प्रति सेकंड होती है।", speaker="Amit")
tts.save("output.wav", wav)                  # float32 numpy @ 24 kHz
```

```python
wav = tts(text, speaker="Amit", style="ANGER",
          temperature=0.6, top_p=0.9, top_k=50,
          max_new_tokens=2520, seed=None, stock=False)
```

<h3 style="color:#C1440E;">From the command line</h3>

```
python inference.py --text "..." --speaker Amit --style ANGER
```

<h3 style="color:#C1440E;">Voices</h3>

`speaker` must be a name the model saw in training — an unseen name does not error, it just
gives an averaged, worse voice.

<details>
<summary>All 95 voices by language</summary>

| Language | Code | N | Speakers |
|---|---|---|---|
| Assamese | `as` | 2 | `Ankur`, `Prastuti` |
| Bengali | `bn` | 2 | `Ishita`, `Sourav` |
| Bhili | `bhb` | 7 | `Bhima`, `Dhulji`, `Govind`, `Jhamku`, `Kanku`, `Sarju`, `Tantya` |
| Bodo | `brx` | 2 | `Gwrbw`, `Sansuma` |
| Dogri | `doi` | 2 | `Preeti`, `Sham` |
| English | `en` | 44 | `Adarsh`, `Akash`, `Amit`, `Anagha`, `Anitha`, `Anjali`, `Ankur`, `Arun`, `Aryaman`, `Bharati`, `Chaoba`, `Chinmay`, `Deepika`, `Dhara`, `Gwrbw`, `Ishfaq`, `Ishita`, `Itishree`, `Kaur`, `Kavya`, `Kiran`, `Lakshmi`, `Madhukar`, `Manpreet`, `Moomal`, `Parth`, `Phulmani`, `Prastuti`, `Preeti`, `Rano`, `Saba`, `Sagar`, `Sandeep`, `Sansuma`, `Sham`, `Sibu`, `Sourav`, `Sravani`, `Srijana`, `Thoibi`, `Vaidehi`, `Vamsi`, `Zaid`, `Zoon` |
| Gujarati | `gu` | 2 | `Dhara`, `Parth` |
| Hindi | `hi` | 2 | `Amit`, `Kavya` |
| Kannada | `kn` | 2 | `Adarsh`, `Deepika` |
| Kashmiri | `ks` | 2 | `Ishfaq`, `Zoon` |
| Konkani | `kok` | 2 | `Anjali`, `Sandeep` |
| Maithili | `mai` | 2 | `Madhukar`, `Vaidehi` |
| Malayalam | `ml` | 2 | `Kiran`, `Lakshmi` |
| Manipuri | `mni` | 2 | `Chaoba`, `Thoibi` |
| Marathi | `mr` | 2 | `Anagha`, `Chinmay` |
| Nepali | `ne` | 2 | `Sagar`, `Srijana` |
| Odia | `or` | 2 | `Akash`, `Itishree` |
| Punjabi | `pa` | 2 | `Kaur`, `Manpreet` |
| Sanskrit | `sa` | 2 | `Aryaman`, `Bharati` |
| Santali | `sat` | 2 | `Phulmani`, `Sibu` |
| Sindhi | `sd` | 2 | `Moomal`, `Rano` |
| Tamil | `ta` | 2 | `Anitha`, `Arun` |
| Telugu | `te` | 2 | `Sravani`, `Vamsi` |
| Urdu | `ur` | 2 | `Saba`, `Zaid` |

Most languages have one male and one female voice. The English list is largely the same
artists recording English, so a name like `Amit` or `Kavya` serves both its own language
and English — which is what makes code-mixed text work.

</details>

<details>
<summary>Technical details — pipeline, prompt format, files</summary>

```
text -> prompt -> LM -> SNAC codes -> quantizer.from_codes -> z_q [B,768,L] -> Vocos -> 24 kHz
```

A Llama-3.2-3B speech LM emits SNAC audio codes; a fine-tuned Vocos decoder converts them to
waveform. SNAC is pulled from `hubertsiuzdak/snac_24khz`, but only its **quantizer**
(0.56 MB of 79 MB) is used — Vocos replaces SNAC's decoder entirely, and SNAC's encoder is unused.

Prompt (both metadata blocks optional):

```
<|start_of_human|><|begin_of_text|><|speaker>Amit<speaker|>\n<|style>ANGER<style|>\n{text}<|eot_id|><|end_of_human|><|start_of_ai|><|start_of_speech|>
```

`style` is free text. Two forms appear in training: uppercase emotion labels (`ANGER`,
`FEAR`, … 17 in total) and descriptive phrases such as `happiness, speaking with a strong
texan accent`.

| File | |
|---|---|
| `model.safetensors` | LM, 3.78 B params, bf16, vocab 156960 |
| `tokenizer.json` | Llama-3 base + speech control + SNAC + non-verbal tokens |
| `vocos/best.pt` | Vocos decoder `vocos_dec_v9_gen`, step 200k (EMA weights under `ema`, live under `vocos`; the loader uses `ema`) |
| `vocos/model.py` | decoder architecture (ConvNeXt-1D + iSTFT head) |
| `vocos/load.py` | standalone decoder loader |
| `inference.py` | `TTS` class + CLI |

Requires **transformers v5** (`tokenizer_class: TokenizersBackend`).

</details>

---

<h2 id="limitations" style="color:#C1440E;">Limitations</h2>

- **Style control is preview-quality.** A `style` field exists and responds to emotion labels and descriptive phrases, but it is not yet consistent enough to rely on.
- **No sound effects.** No laughter, sighs, or breaths.
- **No voice cloning.** Voices come from the library only.
- **Content-specific performance.** Best on explanatory content; unusual words may be mispronounced, and very complex equations may need help.

---

<h2 id="license--terms-of-use" style="color:#C1440E;">License / Terms of Use</h2>

Released under [Indic Open Model License v1.0](Bodhan_AI_Open_Model_License.md).

The base model is [`Llama-3.2-3B`](https://huggingface.co/meta-llama/Llama-3.2-3B), and this system also uses the [`SNAC`](https://github.com/hubertsiuzdak/snac) Quantizer and a finetuned [`Vocos`](https://github.com/gemelo-ai/vocos) decoder. You should confirm that your use of this model conforms the terms of use and license of these upstream models/components also.

---

*If you find the license difficult to understand, here is a plain-language guide to the Indic Open Model License.*

Broad, no-cost access for research, government, nonprofit, and commercial use — with a few conditions attached.

> **This deed is a human-readable summary of the license, not a substitute for it.** Where the two disagree, the full **Indic Open Model License** governs.

---

## You're free to

No cost, no royalty, worldwide — for research, government, nonprofit, and commercial use, at any scale.

- ✅ **Run it** — for inference, in a product, in research, however you like.
- ✅ **Change it** — fine-tune, distill, quantize, merge, or otherwise build on it.
- ✅ **Self-host it** — power your own product or service with it, commercial or not.
- ✅ **Share it** — pass on copies of the model or your own version of it.

---

## As long as you

Five conditions cover almost everything. The rest of the license is these, spelled out in legal detail.

### 1. Give credit

Wherever you ship the model or a derivative to anyone else, say where it came from — and don't strip out existing notices.

```
"Built with [Model Name] from Bodhan AI / AI4Bharat."
```

### 2. Pass it on the same way

If you give your fine-tuned or derived version to anyone else — hand it over, or run it as a service for them — it carries this exact license. You can't relicense it on different terms.

### 3. Ask before hosting it for others

Self-hosting is free. But if you're going to run it as an API or hosted service that *other people or companies* call directly, that needs Bodhan AI's written sign-off first — unless you're a nonprofit, government, or academic user, or you publicly release an equally capable open version within 90 days.

### 4. Don't use it to cause harm

No exceptions — not even for nonprofit or research use. That means no:

- child sexual abuse material, or content that sexualizes minors
- weapons development, including chemical, biological, radiological, or nuclear
- mass surveillance or social-scoring systems
- disinformation campaigns, including election manipulation
- automated decisions that affect someone's legal rights without human oversight
- deepfakes or voice clones of real people without their consent
- robocalls, auto-dialers, or voice-phishing scams
- AI companion products designed to simulate romance or foster emotional dependency

### 5. Talk to us if your product gets huge

If your own product built on this — not through hosting it for others, that's covered above — crosses either threshold, you'll need a separate commercial license. Doesn't apply to nonprofit, government, or academic users.

| Threshold | |
|---|---|
| **500M+** | monthly active users |
| | *or* |
| **$250M+** | annual revenue |


---

<h2 id="use-case" style="color:#C1440E;">Use Case</h2>

Text-to-speech for education (STEM and code-mixed lessons), audiobooks and long-form narration, in-app product voice, conversational agents and helplines, and accessibility / screen reading.

---

<h2 id="citation" style="color:#C1440E;">Citation</h2>

```bibtex
@misc{indicspeak2026,
  title  = {Indic-Speak: Text-to-Speech for 22 Indian Languages and English},
  author = {Bodhan AI and AI4Bharat},
  year   = {2026},
  url    = {https://huggingface.co/bodhan-ai/indic-speak-preview-v2}
}
```

---

<h2 id="ethical-considerations" style="color:#C1440E;">Ethical Considerations</h2>

All voices are recorded by consenting, contracted artists, and the model does not support voice cloning. Developers integrating Indic-Speak should test with use-case-specific content to ensure pronunciation and pacing meet their requirements, and should disclose synthetic speech to end users where appropriate.

---

## S10 Jev evaluation — evidence cards judged (verbatim `research/candidates/candidates.json`)

```json
[
  {
    "id": "C1",
    "name": "Indic-Transcribe-flex (bodhan-ai/indic-transcribe-flex), mixed-script mode",
    "type": "speech recognition model, 1.2B parameters, FastConformer encoder + Transformer decoder, based on nvidia/canary-1b-v2",
    "runs_where": "Local. Open weights, gated: must accept the Indic Open Model License on Hugging Face. Checkpoint 4.6 GB; fp16 weights about 2.4 GB by arithmetic (1.2B x 2 bytes).",
    "evidence": [
      "Voice of India benchmark (unscripted telephonic conversational speech), Tamil WER 10.8 as reported on the model card; the same card reports Indic Conformer 16.2, Gemini 3 Pro 15.5, Saaras V3 9.1. Source: bodhan-ai/indic-transcribe-flex README. This is the developer's own report, not an independent evaluation.",
      "Card: 'Three transcription modes: Native script; Mixed script for native words in native script with English and numerals in Latin; Romanized for everything in Latin script.' Example given: 'मैंने कल 5 बजे 3 files upload कीं'.",
      "Card: 'Code-mixing, natively. Indians rarely speak one language at a time. Indic-Transcribe transcribes Hinglish and other mixed speech as it is actually spoken.' Tags include code-switching, code-mixing, romanization, transliteration.",
      "Card limitation: 'Mixed-script (ITN) mode can be wrong. Inverse text normalization is genuinely ambiguous in places, so mixed-script mode will occasionally get it wrong.'",
      "Card limitation: 'Streaming is not available in pro. Use Indic-Transcribe-lite for real-time use.' Indic-Transcribe-lite is not published in the bodhan-ai Hugging Face organisation (models listed: indic-transcribe-flex, indic-transcribe-core, indic-speak, indic-ocr, indic-translate).",
      "Card: single-pass decoding refuses audio longer than 45 s; model trained on clips up to 30 s; a long-form helper splits audio at pauses of at least 250 ms. Latency on an H100 is listed as 100 ms per request (in a commented-out section).",
      "Card: 'an hour of audio runs in 48 s (77x realtime, 9.2 GiB of GPU memory)' on the NeMo path at batch size 8. VRAM at batch size 1 on a 6 GB laptop GPU is NOT measured.",
      "Card: built-in language identification; for Tamil the language-ID accuracy is listed as 0.98.",
      "Released August 2026 (announced by Mitesh Khapra, AI4Bharat, on X, 2026-08-17). No independent practitioner reports, Reddit threads, or YouTube demos of this model were found.",
      "Runtime: Hugging Face path with code shipped in the repository (pip install torch torchaudio transformers sentencepiece soundfile); a NeMo path is also provided. Windows use is not explicitly documented."
    ],
    "unknowns": "Actual VRAM and latency on an RTX 3050 6 GB; whether per-token confidence is exposed; independent accuracy."
  },
  {
    "id": "C2",
    "name": "Indic-Transcribe-core (bodhan-ai/indic-transcribe-core), native-script output",
    "type": "speech recognition model, 1.2B parameters, based on nvidia/canary-1b-v2",
    "runs_where": "Local. Open weights, gated with the Indic Open Model License. Same size class as C1 (about 2.4 GB fp16 weights by arithmetic).",
    "evidence": [
      "Voice of India benchmark Tamil WER 9.0 as reported on the model card (best Tamil number in that table; Saaras V3 9.1, Indic-Transcribe-flex 10.8, Indic Conformer 16.2). Metric described as OIWER, which accepts documented spelling and transliteration variants. Developer's own report.",
      "Card: 'The model transcribes into the native script of the language being spoken' — no mixed-script or romanized mode (those are only in flex). English words spoken inside Tamil would therefore be written in Tamil script.",
      "Card: 'Code-mixed audio: yes'; 'Code-mixing, natively.'",
      "Card: 'The model code ships inside this repository, so there is nothing else to install — no NeMo'.",
      "Same 30 s training-clip limit and pause-based long-form splitter as C1; no streaming.",
      "No independent practitioner reports, Reddit threads, or YouTube demos found (released August 2026)."
    ],
    "unknowns": "VRAM and latency on RTX 3050; confidence output; independent accuracy."
  },
  {
    "id": "C3",
    "name": "AI4Bharat IndicConformer-600M multilingual (ai4bharat/indic-conformer-600m-multilingual)",
    "type": "speech recognition model, 600M parameters, Conformer with hybrid CTC + RNNT decoders",
    "runs_where": "Local. MIT license, gated access. Runs through transformers trust_remote_code with onnxruntime-gpu 1.20.1. fp16 weights about 1.2 GB by arithmetic.",
    "evidence": [
      "Voice of India paper (arXiv 2604.19151, AI4Bharat/IIT Madras + Josh Talks, independent of Bodhan): Tamil OIWER 19.9, best open-source model evaluated; cloud systems Sarvam Audio 14.2, Saarika 2.5 14.9, Gemini 3 Pro 15.7. Paper places IndicConformer in 'Tier I: Top-performing systems (WER <= 20%)'.",
      "Voice of India paper: 'Indic Conformer WER peaking at 27.57% (slow) and 27.53% (very fast) versus 24.75% at moderate speeds' (cross-lingual average).",
      "GitHub practitioner (gnanaprakash2918/AI-Media-Indexer issue #3, 2025-12-04): 'For Tamil, Whisper's accuracy is not as good as AI4Bharat's IndicConformer models' — chose to route Tamil to IndicConformer.",
      "Model card: supports CTC and RNNT decoding, 22 Indian languages including Tamil; no streaming mentioned; no WER in the card.",
      "CTC decoding produces per-frame probabilities that can be turned into word confidence (standard property of CTC; not documented in the card).",
      "Output is native Tamil script; English words spoken inside Tamil come out transliterated in Tamil script (Voice of India paper notes 'non standardized native script renderings of English origin words in code mixed spontaneous speech').",
      "YouTube: tutorials by Sudheendra S G (2026-05, IndicConformer pipeline with JSON/SRT output, 431 and 377 views); AI4Bharat demo video (2022). About 520k downloads on Hugging Face."
    ],
    "unknowns": "Latency on RTX 3050; Windows-specific issues with the ONNX remote code."
  },
  {
    "id": "C4",
    "name": "OpenAI Whisper large-v3-turbo via faster-whisper (CTranslate2) + ufal/whisper_streaming LocalAgreement",
    "type": "speech recognition model, 809M parameters, encoder-decoder, 99 languages",
    "runs_where": "Local. MIT license, no gating. fp16 weights about 1.6 GB by arithmetic; faster-whisper supports int8.",
    "evidence": [
      "Whisper paper (arXiv 2212.04356) Tamil WER for large-v2: Common Voice 9 16.1, FLEURS 17.5 (clean read speech). No published Tamil WER for large-v3 or turbo was found. Open-source Whisper was not evaluated on the Voice of India conversational benchmark.",
      "OpenAI maintainer on github.com/openai/whisper discussion 2009: 'Whisper doesn't support code-switching inputs very well.'",
      "faster-whisper issue 1476 (2026-09-10): with multilingual=True a window can be decoded in the previous window's language unless condition_on_previous_text=False — 'the default configuration of multilingual=True does not produce a multilingual transcript.'",
      "Research cited in practitioner survey: Whisper large-v3 produces non-empty transcriptions for 40.3% of non-speech inputs (hallucination on silence); a voice-activity gate is required.",
      "Streaming: ufal/whisper_streaming (3,673 stars) uses LocalAgreement — 'emit the transcripts that are confirmed by 2 iterations'. RealtimeSTT (10,145 stars) is VAD-centric. Word-level partial output while speaking is available.",
      "X post (r4plh, 2026-03-18): 'Whisper fine-tunes for Hindi and Tamil? Worked. Telugu? Hallucinated text. Kannada? Output in the wrong script entirely.' X post (krishashok, 2022): 'Tamil is the best-performing Indian language on Whisper'.",
      "YouTube: faster-whisper realtime tutorial (KARTIS, 31k views) shows large-v3 on GPU; a Tamil voice-assistant build (Karthik's Show, 2026-07, 2.5k views) uses Whisper large-v3 and mentions 'few problems'.",
      "Widely installed on Windows (faster-whisper, whisper-writer, Buzz, OmniDictate)."
    ],
    "unknowns": "Turbo's Tamil accuracy on colloquial speech; whether English words come out in Latin or Tamil script on Tanglish."
  },
  {
    "id": "C5",
    "name": "vasista22/whisper-tamil-medium (Tamil fine-tune of Whisper medium) via faster-whisper conversion",
    "type": "speech recognition model, 769M parameters, Tamil-only fine-tune",
    "runs_where": "Local. Apache-2.0, no gating. fp16 weights about 1.5 GB by arithmetic; needs conversion to CTranslate2 for faster-whisper.",
    "evidence": [
      "Model card: FLEURS ta_in test WER 6.97; Common Voice 11 ta test WER 6.5. Both are read or prompted speech, not colloquial or code-switched.",
      "Training data per card: IISc-MILE, ULCA, Shrutilipi, Microsoft Speech Corpus (Indian Languages), Google FLEURS, Babel — mostly clean or read speech.",
      "776 downloads for medium; the small variant (vasista22/whisper-tamil-small) has about 151k downloads but no published WER.",
      "Inherits Whisper behaviour: no native streaming (needs LocalAgreement or VAD chunking), hallucination on silence, single-language decoding per window.",
      "No code-switching evaluation; fine-tuned only on Tamil, so English words are likely forced into Tamil script (not documented).",
      "Not evaluated on Voice of India. No Reddit or YouTube reports specific to this checkpoint were found."
    ],
    "unknowns": "Accuracy on colloquial Tanglish; behaviour on English words."
  },
  {
    "id": "C6",
    "name": "Google Gemma 3n E4B (audio-input LLM) as a single model for transcription and formatting",
    "type": "multimodal LLM with audio input, about 4B effective parameters",
    "runs_where": "Local. Gated with manual approval; Gemma license. About 8 GB download; would need 4-bit quantisation to fit in 6 GB.",
    "evidence": [
      "Indic-Transcribe-flex card, Voice of India table: Gemma E4B Tamil WER 37.9 (average 36.1).",
      "Public model card does not list which languages are supported for audio input (lead verification found NOT COVERED).",
      "Would be a single model for both hearing and organising, which the user prefers, but no Tamil ASR demo or practitioner report was found.",
      "GitHub Next localjev study: Gemma 4 E4B accuracy fell from 50.0% to 12.5% when 2,048 unrelated words were added to the input (distraction sensitivity for a small model).",
      "No streaming speech recognition; audio is processed in clips."
    ],
    "unknowns": "Whether Tamil audio is officially supported; VRAM when quantised."
  },
  {
    "id": "C7",
    "name": "Meta Omnilingual ASR LLM 1B",
    "type": "speech recognition model, 1B parameters, 1,600+ languages",
    "runs_where": "Local. Open weights. About 2 GB fp16 by arithmetic.",
    "evidence": [
      "Voice of India paper: OmniASR LLM 1B Tamil OIWER 49.0; OmniASR LLM 7B 43.1. Paper Tier III: 'Deepgram Nova-3 and OmniASR yield elevated error rates in Tamil'.",
      "Indic-Transcribe card table: OmniASR LLM 7B Tamil 40.6; OmniASR CTC 7B Tamil 58.3.",
      "No Tamil practitioner reports found."
    ],
    "unknowns": "Streaming support; Windows install."
  },
  {
    "id": "C8",
    "name": "AI4Bharat IndicConformer Tamil-only large (ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large)",
    "type": "speech recognition model, 120M parameters, Conformer-Large hybrid CTC-RNNT, Tamil only",
    "runs_where": "Local. MIT license, gated. Very small (about 0.25 GB fp16).",
    "evidence": [
      "Model card: '17 conformer blocks with 512 as the model dimension', Tamil only, 16 kHz mono input.",
      "Requires the AI4Bharat NeMo fork: 'git clone https://github.com/AI4Bharat/NeMo.git && cd NeMo && git checkout nemo-v2 && bash reinstall.sh' (a bash script; Windows support not documented).",
      "No WER in the card; not separately evaluated on Voice of India (the paper's Indic Conformer entry is not identified by checkpoint).",
      "GitHub practitioner (AI-Media-Indexer issue #3) recommended this exact checkpoint for Tamil via NeMo.",
      "No streaming mentioned. Native-script output."
    ],
    "unknowns": "Accuracy; Windows install feasibility."
  },
  {
    "id": "C9",
    "name": "CONTROL: Sarvam Audio / Saarika cloud speech-to-text API",
    "type": "cloud API service",
    "runs_where": "Cloud only. Paid per hour of audio (about Rs 30-45 per hour per Sarvam pricing). Audio is sent to Sarvam servers over the internet.",
    "evidence": [
      "Voice of India paper: Sarvam Audio Tamil OIWER 14.2 (best), Saarika 2.5 14.9.",
      "Sarvam site: 'Streaming speech recognition for 22 Indian languages with low-latency decoding and code-mixed support.' WebSocket streaming API.",
      "Weights are not available for download."
    ],
    "unknowns": "None relevant: it cannot run locally."
  },
  {
    "id": "C10",
    "name": "CONTROL: Qwen3-ASR-0.6B",
    "type": "speech recognition model, 600M parameters",
    "runs_where": "Local. Apache-2.0.",
    "evidence": [
      "Model card language list (30 languages + 22 Chinese dialects): Chinese, English, Cantonese, Arabic, German, French, Spanish, Portuguese, Indonesian, Italian, Korean, Russian, Thai, Vietnamese, Japanese, Turkish, Hindi, Malay, Dutch, Swedish, Danish, Finnish, Polish, Czech, Filipino, Persian, Greek, Hungarian, Macedonian, Romanian. Tamil is not listed.",
      "Card: 'support streaming / offline unified inference with single model'.",
      "Reddit (r/FunMachineLearning): a Hindi/Hinglish fine-tune on 1,000 hours of call audio 'beats Whisper large-v3, Azure and Google on accented Hindi' — no Tamil version exists."
    ],
    "unknowns": "None relevant: Tamil unsupported."
  }
]

```

# Jev ranking of speech-recognition candidates

Model: `jev-1.13.0`. Generated by `run_jev.py` from `../candidates/candidates.json`. Raw answers: `jev_raw.json`.

Scores are Jev Score outputs normalised to 0-1 (score / top level). Weighted total uses the ASSERTED policy weights in `run_jev.py`; the equal-weight rank is shown as a sensitivity check. A candidate is BLOCKED if Jev's Noul says it needs the cloud (p > 0.5) or does not support Tamil (p < 0.5).

| Rank | ID | Candidate | Tamil acc | Code-mix | Live | Fits 6GB | Indep. valid. | Windows | Weighted | Equal-wt rank | Cloud p | Tamil p | Conf-signal p | Blocked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C1 | Indic-Transcribe-flex (bodhan-ai/indic-transcribe-flex), mixed-script mode | 1.00 | 0.97 | 0.49 | 0.64 | 0.00 | 0.49 | **0.704** | 3 | 0.09 | 0.94 | 0.19 | - |
| 2 | C2 | Indic-Transcribe-core (bodhan-ai/indic-transcribe-core), native-script output | 0.94 | 0.50 | 0.48 | 0.88 | 0.01 | 0.48 | **0.625** | 4 | 0.07 | 0.95 | 0.17 | - |
| 3 | C3 | AI4Bharat IndicConformer-600M multilingual (ai4bharat/indic-conformer-600m-multilingual) | 0.66 | 0.50 | 0.27 | 0.92 | 0.86 | 0.50 | **0.621** | 2 | 0.07 | 0.97 | 0.76 | - |
| 4 | C4 | OpenAI Whisper large-v3-turbo via faster-whisper (CTranslate2) + ufal/whisper_streaming LocalAgreement | 0.37 | 0.08 | 1.00 | 0.92 | 0.55 | 0.95 | **0.556** | 1 | 0.03 | 0.84 | 0.42 | - |
| 5 | C5 | vasista22/whisper-tamil-medium (Tamil fine-tune of Whisper medium) via faster-whisper conversion | 0.34 | 0.24 | 0.49 | 0.93 | 0.43 | 0.51 | **0.454** | 5 | 0.04 | 0.86 | 0.40 | - |
| 6 | C7 | Meta Omnilingual ASR LLM 1B | 0.34 | 0.15 | 0.25 | 0.96 | 0.49 | 0.34 | **0.399** | 6 | 0.04 | 0.82 | 0.19 | - |
| 7 | C8 | AI4Bharat IndicConformer Tamil-only large (ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large) | 0.08 | 0.04 | 0.33 | 0.98 | 0.48 | 0.04 | **0.288** | 7 | 0.04 | 0.94 | 0.24 | - |
| 8 | C9 | CONTROL: Sarvam Audio / Saarika cloud speech-to-text API | 0.93 | 0.48 | 0.97 | 0.00 | 0.50 | 0.18 | **0.596** | 8 | 0.99 | 0.94 | 0.25 | cloud p=0.99 |
| 9 | C6 | Google Gemma 3n E4B (audio-input LLM) as a single model for transcription and formatting | 0.24 | 0.09 | 0.40 | 0.49 | 0.47 | 0.49 | **0.318** | 9 | 0.13 | 0.37 | 0.14 | no Tamil p=0.37 |
| 10 | C10 | CONTROL: Qwen3-ASR-0.6B | 0.00 | 0.01 | 0.72 | 0.86 | 0.00 | 0.47 | **0.279** | 10 | 0.05 | 0.03 | 0.23 | no Tamil p=0.03 |

## Jev confidence per Score (distribution concentration, 0-1)

| ID | tamil_accuracy | code_mixed_output | live_updates | fits_6gb | independent_validation | windows_setup |
|---|---|---|---|---|---|---|
| C1 | 1.00 | 0.93 | 0.96 | 0.48 | 0.99 | 0.99 |
| C2 | 0.82 | 0.99 | 0.95 | 0.62 | 0.98 | 0.96 |
| C3 | 0.97 | 0.99 | 0.20 | 0.75 | 0.59 | 1.00 |
| C4 | 0.90 | 0.76 | 0.99 | 0.75 | 0.87 | 0.86 |
| C5 | 0.99 | 0.28 | 0.96 | 0.79 | 0.78 | 0.99 |
| C7 | 0.99 | 0.55 | 0.25 | 0.89 | 0.96 | 0.50 |
| C8 | 0.77 | 0.89 | 0.24 | 0.94 | 0.94 | 0.87 |
| C9 | 0.78 | 0.78 | 0.93 | 1.00 | 0.96 | 0.46 |
| C6 | 0.72 | 0.74 | 0.70 | 0.67 | 0.87 | 0.97 |
| C10 | 1.00 | 0.96 | 0.17 | 0.59 | 1.00 | 0.21 |

## Jev global Choice: default model

Choice: **C1**, confidence 0.63

| Option | Probability |
|---|---|
| C1 Indic-Transcribe-flex (bodhan-ai/indic-transcribe-flex), mixed-script mode | 0.680 |
| C4 OpenAI Whisper large-v3-turbo via faster-whisper (CTranslate2) + ufal/whisper_streaming LocalAgreement | 0.170 |
| C3 AI4Bharat IndicConformer-600M multilingual (ai4bharat/indic-conformer-600m-multilingual) | 0.150 |
| C5 vasista22/whisper-tamil-medium (Tamil fine-tune of Whisper medium) via faster-whisper conversion | 0.000 |
| C9 CONTROL: Sarvam Audio / Saarika cloud speech-to-text API | 0.000 |
| C10 CONTROL: Qwen3-ASR-0.6B | 0.000 |
| C8 AI4Bharat IndicConformer Tamil-only large (ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large) | 0.000 |
| C6 Google Gemma 3n E4B (audio-input LLM) as a single model for transcription and formatting | 0.000 |
| C7 Meta Omnilingual ASR LLM 1B | 0.000 |
| C2 Indic-Transcribe-core (bodhan-ai/indic-transcribe-core), native-script output | 0.000 |


---

## S11 YouTube deep summaries (verbatim `research/youtube/youtube_summaries.md`)

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


---

## S12 Jev run 2 (after adding YouTube evidence to cards)

# Jev ranking of speech-recognition candidates

Model: `jev-1.13.0`. Generated by `run_jev.py` from `../candidates/candidates.json`. Raw answers: `jev_raw.json`.

Scores are Jev Score outputs normalised to 0-1 (score / top level). Weighted total uses the ASSERTED policy weights in `run_jev.py`; the equal-weight rank is shown as a sensitivity check. A candidate is BLOCKED if Jev's Noul says it needs the cloud (p > 0.5) or does not support Tamil (p < 0.5).

| Rank | ID | Candidate | Tamil acc | Code-mix | Live | Fits 6GB | Indep. valid. | Windows | Weighted | Equal-wt rank | Cloud p | Tamil p | Conf-signal p | Blocked |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C1 | Indic-Transcribe-flex (bodhan-ai/indic-transcribe-flex), mixed-script mode | 1.00 | 0.98 | 0.49 | 0.60 | 0.01 | 0.49 | **0.701** | 3 | 0.08 | 0.93 | 0.20 | - |
| 2 | C3 | AI4Bharat IndicConformer-600M multilingual (ai4bharat/indic-conformer-600m-multilingual) | 0.67 | 0.50 | 0.44 | 0.93 | 0.87 | 0.46 | **0.646** | 2 | 0.08 | 0.96 | 0.75 | - |
| 3 | C2 | Indic-Transcribe-core (bodhan-ai/indic-transcribe-core), native-script output | 0.94 | 0.49 | 0.47 | 0.89 | 0.01 | 0.49 | **0.625** | 4 | 0.05 | 0.95 | 0.16 | - |
| 4 | C4 | OpenAI Whisper large-v3-turbo via faster-whisper (CTranslate2) + ufal/whisper_streaming LocalAgreement | 0.36 | 0.11 | 1.00 | 0.92 | 0.54 | 0.96 | **0.559** | 1 | 0.03 | 0.81 | 0.46 | - |
| 5 | C5 | vasista22/whisper-tamil-medium (Tamil fine-tune of Whisper medium) via faster-whisper conversion | 0.33 | 0.26 | 0.49 | 0.92 | 0.43 | 0.51 | **0.456** | 5 | 0.03 | 0.87 | 0.38 | - |
| 6 | C7 | Meta Omnilingual ASR LLM 1B | 0.34 | 0.15 | 0.24 | 0.95 | 0.49 | 0.35 | **0.397** | 6 | 0.05 | 0.82 | 0.19 | - |
| 7 | C8 | AI4Bharat IndicConformer Tamil-only large (ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large) | 0.09 | 0.05 | 0.33 | 0.98 | 0.48 | 0.04 | **0.293** | 7 | 0.04 | 0.94 | 0.27 | - |
| 8 | C9 | CONTROL: Sarvam Audio / Saarika cloud speech-to-text API | 0.91 | 0.49 | 0.96 | 0.00 | 0.51 | 0.17 | **0.590** | 8 | 0.99 | 0.94 | 0.26 | cloud p=0.99 |
| 9 | C6 | Google Gemma 3n E4B (audio-input LLM) as a single model for transcription and formatting | 0.26 | 0.07 | 0.40 | 0.49 | 0.46 | 0.49 | **0.319** | 9 | 0.12 | 0.38 | 0.14 | no Tamil p=0.38 |
| 10 | C10 | CONTROL: Qwen3-ASR-0.6B | 0.00 | 0.02 | 0.79 | 0.88 | 0.00 | 0.43 | **0.289** | 10 | 0.05 | 0.03 | 0.23 | no Tamil p=0.03 |

## Jev confidence per Score (distribution concentration, 0-1)

| ID | tamil_accuracy | code_mixed_output | live_updates | fits_6gb | independent_validation | windows_setup |
|---|---|---|---|---|---|---|
| C1 | 1.00 | 0.95 | 0.96 | 0.58 | 0.98 | 0.99 |
| C3 | 0.97 | 0.99 | 0.81 | 0.77 | 0.61 | 0.87 |
| C2 | 0.81 | 0.99 | 0.92 | 0.66 | 0.96 | 0.96 |
| C4 | 0.91 | 0.67 | 0.99 | 0.75 | 0.87 | 0.88 |
| C5 | 0.99 | 0.28 | 0.97 | 0.74 | 0.80 | 0.98 |
| C7 | 0.99 | 0.54 | 0.27 | 0.85 | 0.95 | 0.52 |
| C8 | 0.74 | 0.85 | 0.21 | 0.94 | 0.95 | 0.89 |
| C9 | 0.73 | 0.79 | 0.90 | 1.00 | 0.95 | 0.49 |
| C6 | 0.76 | 0.78 | 0.68 | 0.66 | 0.86 | 0.97 |
| C10 | 1.00 | 0.94 | 0.37 | 0.64 | 1.00 | 0.14 |

## Jev global Choice: default model

Choice: **C1**, confidence 0.61

| Option | Probability |
|---|---|
| C1 Indic-Transcribe-flex (bodhan-ai/indic-transcribe-flex), mixed-script mode | 0.660 |
| C4 OpenAI Whisper large-v3-turbo via faster-whisper (CTranslate2) + ufal/whisper_streaming LocalAgreement | 0.190 |
| C3 AI4Bharat IndicConformer-600M multilingual (ai4bharat/indic-conformer-600m-multilingual) | 0.150 |
| C6 Google Gemma 3n E4B (audio-input LLM) as a single model for transcription and formatting | 0.000 |
| C2 Indic-Transcribe-core (bodhan-ai/indic-transcribe-core), native-script output | 0.000 |
| C10 CONTROL: Qwen3-ASR-0.6B | 0.000 |
| C9 CONTROL: Sarvam Audio / Saarika cloud speech-to-text API | 0.000 |
| C5 vasista22/whisper-tamil-medium (Tamil fine-tune of Whisper medium) via faster-whisper conversion | 0.000 |
| C7 Meta Omnilingual ASR LLM 1B | 0.000 |
| C8 AI4Bharat IndicConformer Tamil-only large (ai4bharat/indicconformer_stt_ta_hybrid_ctc_rnnt_large) | 0.000 |


---

## S13 raw file: `research_voice_editors.md` (verbatim)

Reviewer note: the table marks coleam00/obsidian-voice-agent "Local: Yes", but its own description says "Real-time voice chat powered by OpenAI Realtime API" — it is cloud-dependent.

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
