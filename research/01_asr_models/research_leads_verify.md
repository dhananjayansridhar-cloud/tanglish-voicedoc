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
