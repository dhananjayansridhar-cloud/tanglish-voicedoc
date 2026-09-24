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

