# Recommendation — local live Tanglish dictation on an RTX 3050 6 GB

Date: 2026-09-24. Hard constraint: everything local on the laptop GPU; no APIs, no paid or cloud models.

Evidence: `research.md` (full dump), `research/` (organised by topic), `research/candidates/candidates.json` (the evidence cards Jev judged), `research/jev/` (Jev script, raw answers, ranking).

## 1. How the choice was made

1. Seven research streams plus retries collected evidence from Hugging Face, GitHub, arXiv, YouTube, Reddit (agent-reach OpenCLI) and X (tw.sh).
2. Every speech-recognition candidate got an evidence card containing only sourced facts, negatives included.
3. TypeSafe **Jev** (`jev-1.13.0`) judged each card against the requirements using 6 **Score** questions, 3 **Noul** gates and 1 global **Choice** (`research/jev/run_jev.py`).
4. Two deliberate controls tested Jev: a cloud API (Sarvam) and a model without Tamil (Qwen3-ASR). Jev blocked both (cloud p = 0.99; Tamil p = 0.03), so the judgments discriminate on the constraints.

## 2. The five options (Jev ranking, local-only candidates)

Weighted total uses the asserted weights in `run_jev.py`: accuracy 0.30, code-mix 0.20, live 0.15, fits-6GB 0.15, independent validation 0.12, Windows 0.08.

| Rank | Option | Jev weighted | Equal-weight rank | Tamil accuracy evidence | English words | Live behaviour |
|---|---|---|---|---|---|---|
| **1 — DEFAULT** | **Indic-Transcribe-flex** (bodhan-ai), mixed-script mode | **0.701** | 3 | Voice of India Tamil WER **10.8** (developer-reported) | **Latin script** (mixed mode) | Phrase by phrase at pauses |
| 2 | AI4Bharat IndicConformer-600M multilingual | 0.646 | 2 | Voice of India Tamil OIWER **19.9** (**independent paper**); local Tamil pipeline demonstrated on YouTube (WSL2) | Tamil script | Phrase by phrase |
| 3 | Indic-Transcribe-core (bodhan-ai) | 0.625 | 4 | Voice of India Tamil WER **9.0** (developer-reported) | Tamil script only | Phrase by phrase |
| 4 | Whisper large-v3-turbo + faster-whisper + whisper_streaming | 0.559 | **1** | No conversational Tamil number; large-v2 FLEURS 17.5 (clean speech); YouTube: CPU-only mixed-phrase test self-rated "90%" | Undocumented; maintainer: "doesn't support code-switching inputs very well" | **Word by word** (LocalAgreement) |
| 5 | vasista22/whisper-tamil-medium | 0.456 | 5 | FLEURS 6.97 / Common Voice 6.5 (clean read speech only) | Undocumented, Tamil-only fine-tune | Word by word via LocalAgreement |

Jev's global Choice for the default model: **Indic-Transcribe-flex, p = 0.66** (Whisper-turbo 0.19, IndicConformer 0.15, all others 0.00), confidence 0.61. This is run 2, after adding the YouTube evidence from `research/youtube/youtube_summaries.md`. Run 1 (before YouTube) had the same default, with p = 0.68, and ranked Indic-Transcribe-core above IndicConformer; its output is kept in `research/jev/jev_ranking_run1.md`.

YouTube findings that affect setup (from `research/youtube/youtube_summaries.md`):
- No video demonstrates live local Tamil dictation, reports VRAM, or shows how English words inside Tamil are written.
- The IndicConformer demos ran under WSL2, because native Windows CUDA was unstable, and needed pinned old versions of `transformers`, `onnxruntime` and related packages.

Excluded by Jev's gates or ranking: Gemma 3n E4B (Tamil WER 37.9 on Voice of India; Tamil audio support not documented), Meta Omnilingual 1B (Tamil 49.0), IndicConformer Tamil-only 120M (Linux-oriented NeMo fork), Sarvam (cloud), Qwen3-ASR (no Tamil).

### What the ranking does and does not prove

- **The ranking flips with the weights.** With equal weights Whisper-turbo is first and Indic-Transcribe-flex third. The default wins because accuracy on conversational Tamil and English-in-Latin-script were weighted highest — those are the two things you asked for. If you value "proven by the community" and "word-by-word streaming" above accuracy, Whisper-turbo is the pick.
- **The default's accuracy is unverified by anyone independent.** Jev scored its independent validation **0.00**. All its numbers come from the developer's own card (Bodhan is an AI4Bharat spin-off; the Voice of India benchmark is also AI4Bharat's). No Reddit, X or YouTube user has reported on it yet — it was released in August 2026.
- **Its VRAM on your GPU is unknown.** Jev gave "fits 6 GB" only 0.64, with low confidence (0.48). The weights are about 2.4 GB in fp16 by arithmetic; the only published memory figure (9.2 GiB) is for batch-8 long-form decoding.
- **Consequence:** the default is provisional until the bake-off in section 5 measures word error rate on your voice, VRAM and latency on your laptop. The fallback, if it fails, is option 2 (IndicConformer), the best independently validated local model.

## 3. How live Markdown editing works

### What you see

Open `notes/<session>.md` in **VS Code with Markdown Preview side by side** (`Ctrl+K V`), or in **Obsidian**. Both re-render automatically when the file changes on disk, so no plugin is needed. You speak and the preview updates. A short "listening / pending" line at the bottom shows the phrase currently being transcribed.

### Pipeline (all local, one process, separate threads)

```text
mic (16 kHz mono, sounddevice)
  -> Silero VAD on CPU: cut the audio when you pause for ~400 ms (maximum 25 s per piece;
     the model is trained on clips up to 30 s)
  -> ASR worker on GPU: Indic-Transcribe-flex, mode="mixed", lang="ta"
       output example:  "நாளைக்கு client meeting 3 மணிக்கு fix பண்ணு"
  -> router:
       - starts with the command word ("command" / "கமாண்ட்")  -> command path
       - otherwise                                              -> dictation path
  -> organiser (local text model):
       dictation -> which section it belongs to (existing or new), cleaned text
       command   -> one edit operation from a fixed JSON schema, e.g.
                    {"op":"make_bullets","target":"last_paragraph"}
                    {"op":"move","what":"last_paragraph","to_section":"Action items"}
                    {"op":"new_section","title":"Meeting notes"}
                    {"op":"undo"}
  -> document model (in memory: sections -> blocks) -> render Markdown
  -> atomic write (temp file + os.replace) so the viewer never shows a half-written file
  -> clarification queue -> text-to-speech -> speaker (asked at your next pause)
```

Design rules that make it seamless and safe:

- **The program is the only writer.** Edits are structured operations applied by code, never free-form text written by the model, so a model mistake cannot corrupt the file. Every operation is undoable ("undo" / "அதை cancel பண்ணு").
- **A spoken command word separates commands from dictation.** Without it, "move this to action items" would be typed into the document. This is a deterministic check, not a model guess.
- **Pushback, asked at pauses and not mid-sentence.** The assistant asks when:
  - (a) the organiser can't decide where something goes;
  - (b) a number or date contradicts an earlier one;
  - (c) a command is destructive ("delete that section? it has 12 items");
  - (d) the speech model is unsure of a word.

  Trigger (d) needs a per-word confidence value. Jev rated the default model's confidence output as **undocumented (p = 0.19)**; IndicConformer's CTC output supports it (p = 0.76). If the default model doesn't expose token probabilities, trigger (d) will be built by re-checking low-agreement phrases, and that is to be decided in the bake-off.
- **Live feel:** text appears phrase by phrase, after each pause, not word by word. That is inherent to options 1–3, which do not stream. Estimated delay is the pause length (~0.4 s) plus decode time on the RTX 3050, which is **not yet measured**. If phrase-by-phrase feels too slow, option 4 (Whisper-turbo with LocalAgreement) is the word-by-word alternative, at the cost of weaker Tamil and code-mix accuracy.

### GPU memory budget (estimates, to be measured)

| Component | Model | Estimate | Basis |
|---|---|---|---|
| Speech recognition | Indic-Transcribe-flex fp16 | ~2.4 GB weights + activations | 1.2 B parameters × 2 bytes |
| Organiser | a 2 B text model, 4-bit GGUF (e.g. `Timegravity/tamil-lm-2b-instruct`, 1.3 GB) | ~1.5 GB | file size from its card |
| Voice replies | `ai4bharat/indic-parler-tts` (Apache-2.0, Tamil) | ~1.2 GB fp16, or CPU | 2.4 GB checkpoint |
| CUDA context | — | ~0.4 GB | typical per process |

The total of about 5.5 GB is too close to 6 GB to trust from arithmetic. The bake-off measures it. If it doesn't fit, text-to-speech moves to the CPU, since it only speaks occasionally.

The organiser and text-to-speech choices have **not** been through Jev yet. Only the speech model was ranked. They are the next Jev round, using the same method.

## 4. What you need to do

1. Accept the licence terms on Hugging Face for `bodhan-ai/indic-transcribe-flex`, `bodhan-ai/indic-transcribe-core` and `ai4bharat/indic-conformer-600m-multilingual`. They are gated, and I will not accept terms on your behalf.
2. Record 3–5 clips of how you normally speak (Tanglish, including a few commands) with the laptop microphone. Save them as `samples/*.wav` and write down exactly what you said in `samples/*.txt`.

## 5. Next step: the bake-off, which decides the default for real

For options 1, 3 and 4, on your recordings and your GPU, measure:
- word error rate, with English words in Latin script;
- peak VRAM;
- time from the end of a phrase to text appearing in the file.

The default stays Indic-Transcribe-flex only if it beats IndicConformer on your voice and fits in memory alongside the organiser.
