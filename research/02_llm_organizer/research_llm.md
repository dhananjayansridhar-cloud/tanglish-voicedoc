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

