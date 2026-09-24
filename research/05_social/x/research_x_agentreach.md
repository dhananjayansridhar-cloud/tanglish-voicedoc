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
