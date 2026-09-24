"""Rank speech-recognition candidates with TypeSafe Jev over the evidence cards."""
import json
import pathlib
import time

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

HERE = pathlib.Path(__file__).parent
CARDS = json.loads((HERE.parent / "candidates" / "candidates.json").read_text(encoding="utf-8"))

REQUIREMENTS = {
    "goal": "Live dictation of colloquial Tamil mixed with Indian English (Tanglish) into a Markdown document that updates while the user speaks, reorganises itself on spoken commands, and asks the user clarifying questions by voice when speech or intent is unclear.",
    "hard_constraints": [
        "Everything runs locally on a laptop with an NVIDIA RTX 3050 Laptop GPU with 6 GB VRAM, Windows 11, Python 3.10.",
        "No cloud APIs, no paid services, no internet-hosted models at run time.",
        "The speech model must share the 6 GB with a local text model (for organising) and a local text-to-speech model (for voice replies).",
    ],
    "what_good_output_looks_like": "Tamil words in Tamil script, English words in Latin script, as the user actually spoke them.",
}

QUESTIONS = {
    "tamil_accuracy": Score(
        instructions="Using only the evidence in `candidate`, how accurately does this option transcribe real, unscripted, conversational Tamil speech?",
        criteria=[
            "Tamil is not supported, or there is no evidence at all about Tamil accuracy.",
            "Tamil is supported but the only evidence is on clean read speech, or the reported error rate on unscripted conversational Tamil is above 30 percent.",
            "The reported word error rate on unscripted conversational Tamil is between 15 and 30 percent.",
            "The reported word error rate on unscripted conversational Tamil is below 15 percent.",
        ],
    ),
    "code_mixed_output": Score(
        instructions="Using only the evidence in `candidate`, how well does this option handle English words spoken inside Tamil sentences, compared with `requirements.what_good_output_looks_like`?",
        criteria=[
            "No evidence of code-mixing support, or evidence that mixed speech is forced into one language or mis-transcribed.",
            "Code-mixed speech is handled, but English words come out transliterated into Tamil script, or the behaviour is undocumented.",
            "An explicit documented mode outputs Tamil words in Tamil script and English words in Latin script.",
        ],
    ),
    "live_updates": Score(
        instructions="Using only the evidence in `candidate`, how well can this option update a document live while the user is speaking?",
        criteria=[
            "Only suited to processing finished recordings or long files in batch.",
            "Can transcribe each phrase after the user pauses, by cutting audio at pauses, so text appears phrase by phrase.",
            "Supports streaming output with partial words appearing while the user is still speaking.",
        ],
    ),
    "fits_6gb": Score(
        instructions="Using only the evidence in `candidate` and `requirements.hard_constraints`, how well does this option fit on the 6 GB laptop GPU alongside a local text model and a local text-to-speech model?",
        criteria=[
            "Cannot run locally, or needs more than 6 GB of GPU memory by itself.",
            "Fits in 6 GB by itself but would leave little room (under about 2 GB) for the other two models, or its memory use is unknown and plausibly large.",
            "Small enough (about 2.5 GB or less for its weights) to leave room for a text model and a text-to-speech model.",
        ],
    ),
    "independent_validation": Score(
        instructions="Using only the evidence in `candidate`, how much independent validation exists for its Tamil performance, beyond the developer's own claims?",
        criteria=[
            "No evidence of Tamil use at all, or only the developer's own claims.",
            "An independent benchmark or at least one independent practitioner report on Tamil exists.",
            "An independent benchmark on conversational Tamil plus independent practitioner or community reports exist.",
        ],
    ),
    "windows_setup": Score(
        instructions="Using only the evidence in `candidate`, how easy is this option to install and run on Windows 11 with Python?",
        criteria=[
            "Requires Linux-only build scripts, a custom fork, or cannot be downloaded.",
            "Installable with Python on Windows but needs gated access, custom remote code, or conversion steps.",
            "Plain pip-installable with widely documented Windows use.",
        ],
    ),
    "requires_cloud": Noul(
        instructions="Does using this option require sending audio or text to a cloud API, an internet-hosted model, or a paid service at run time?",
    ),
    "supports_tamil": Noul(
        instructions="According to the evidence in `candidate`, does this option support transcribing Tamil speech?",
    ),
    "confidence_signal": Noul(
        instructions="Does the evidence in `candidate` indicate that this option can provide per-word or per-segment confidence or probabilities that software could use to ask the user to confirm an unclear word?",
    ),
}

# Policy settings (ASSERTED, not swept): relative importance of each Score dimension.
WEIGHTS = {
    "tamil_accuracy": 0.30,
    "code_mixed_output": 0.20,
    "live_updates": 0.15,
    "fits_6gb": 0.15,
    "independent_validation": 0.12,
    "windows_setup": 0.08,
}
LEVELS = {"tamil_accuracy": 3, "code_mixed_output": 2, "live_updates": 2, "fits_6gb": 2,
          "independent_validation": 2, "windows_setup": 2}


def call(client: TypeSafeClient, state: dict, questions: dict):
    for attempt in range(5):
        try:
            return client.system_one(state=state, questions=questions, timeout=60.0)
        except Exception as exc:  # noqa: BLE001 - retried then re-raised
            if attempt == 4:
                raise
            print(f"  retry {attempt + 1} after error: {type(exc).__name__}: {exc}")
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def main() -> None:
    raw: dict = {"model": None, "per_candidate": {}, "default_choice": None}
    rows = []
    with TypeSafeClient() as client:
        for card in CARDS:
            print(f"Judging {card['id']} {card['name'][:60]}")
            resp = call(client, {"requirements": REQUIREMENTS, "candidate": card}, QUESTIONS)
            dumped = resp.model_dump(mode="json")
            raw["model"] = dumped.get("model")
            raw["per_candidate"][card["id"]] = dumped
            ans = dumped["answers"]
            norm = {k: ans[k]["score"] / LEVELS[k] for k in WEIGHTS}
            weighted = sum(WEIGHTS[k] * norm[k] for k in WEIGHTS)
            equal = sum(norm.values()) / len(norm)
            blocked = []
            if ans["requires_cloud"]["noul"] > 0.5:
                blocked.append(f"cloud p={ans['requires_cloud']['noul']:.2f}")
            if ans["supports_tamil"]["noul"] < 0.5:
                blocked.append(f"no Tamil p={ans['supports_tamil']['noul']:.2f}")
            rows.append({"id": card["id"], "name": card["name"], "norm": norm,
                         "conf": {k: ans[k]["confidence"] for k in WEIGHTS},
                         "weighted": weighted, "equal": equal,
                         "cloud": ans["requires_cloud"]["noul"], "tamil": ans["supports_tamil"]["noul"],
                         "confidence_signal": ans["confidence_signal"]["noul"], "blocked": blocked})

        options = {c["id"]: f"{c['name']}" for c in CARDS}
        print("Asking the global default-model Choice")
        resp = call(client, {"requirements": REQUIREMENTS, "candidates": CARDS}, {
            "default_model": Choice(
                instructions="Which single option in `candidates` should be the default speech recognition model for this project, given `requirements` and all hard constraints?",
                criteria=options,
            ),
        })
        raw["default_choice"] = resp.model_dump(mode="json")

    (HERE / "jev_raw.json").write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")

    ranked = sorted(rows, key=lambda r: (bool(r["blocked"]), -r["weighted"]))
    eq_rank = {r["id"]: i + 1 for i, r in enumerate(sorted(rows, key=lambda r: (bool(r["blocked"]), -r["equal"])))}
    choice = raw["default_choice"]["answers"]["default_model"]
    lines = [
        "# Jev ranking of speech-recognition candidates",
        "",
        f"Model: `{raw['model']}`. Generated by `run_jev.py` from `../candidates/candidates.json`. Raw answers: `jev_raw.json`.",
        "",
        "Scores are Jev Score outputs normalised to 0-1 (score / top level). Weighted total uses the ASSERTED policy weights in `run_jev.py`; the equal-weight rank is shown as a sensitivity check. A candidate is BLOCKED if Jev's Noul says it needs the cloud (p > 0.5) or does not support Tamil (p < 0.5).",
        "",
        "| Rank | ID | Candidate | Tamil acc | Code-mix | Live | Fits 6GB | Indep. valid. | Windows | Weighted | Equal-wt rank | Cloud p | Tamil p | Conf-signal p | Blocked |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(ranked, 1):
        n = r["norm"]
        lines.append(
            f"| {i} | {r['id']} | {r['name']} | {n['tamil_accuracy']:.2f} | {n['code_mixed_output']:.2f} | {n['live_updates']:.2f} | "
            f"{n['fits_6gb']:.2f} | {n['independent_validation']:.2f} | {n['windows_setup']:.2f} | **{r['weighted']:.3f}** | {eq_rank[r['id']]} | "
            f"{r['cloud']:.2f} | {r['tamil']:.2f} | {r['confidence_signal']:.2f} | {'; '.join(r['blocked']) or '-'} |"
        )
    lines += ["", "## Jev confidence per Score (distribution concentration, 0-1)", "",
              "| ID | " + " | ".join(WEIGHTS) + " |", "|---|" + "---|" * len(WEIGHTS)]
    for r in ranked:
        lines.append(f"| {r['id']} | " + " | ".join(f"{r['conf'][k]:.2f}" for k in WEIGHTS) + " |")
    lines += ["", "## Jev global Choice: default model", "",
              f"Choice: **{choice['choice']}**, confidence {choice['confidence']:.2f}", "",
              "| Option | Probability |", "|---|---|"]
    for k, p in sorted(choice["probabilities"].items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} {options[k]} | {p:.3f} |")
    (HERE / "jev_ranking.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
