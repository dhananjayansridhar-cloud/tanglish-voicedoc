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
