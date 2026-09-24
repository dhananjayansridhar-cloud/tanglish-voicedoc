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