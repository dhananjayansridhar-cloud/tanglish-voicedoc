"""User settings, persisted as JSON (voicedoc.json). Command-line flags override them for one run."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "voicedoc.json"


@dataclass
class Settings:
    output: str = "file"               # "file": program owns a .md file; "cursor": type at the cursor in any app
    hotkey: str = "ctrl+shift+space"   # toggles listening (or hold-to-talk, see hotkey_mode)
    hotkey_mode: str = "toggle"        # "toggle" or "hold"
    start_listening: bool = True
    min_silence_ms: int = 400
    max_phrase_s: float = 12.0
    asr_mode: str = "mixed"
    translate: bool = True
    mt_model: str = "ai4bharat/indictrans2-indic-en-dist-200M"
    use_llm: bool = True
    llm: str = "qwen3:4b"
    mic: str | None = "communications"  # "communications" (headsets), "default", or part of a device name
    save_audio: bool = True
    sounds: bool = True
    speak_questions: bool = True
    voice: str | None = None           # substring of a Windows voice name, e.g. "Zira"; None = system default
    voice_rate: int = 185
    overlay: bool = True
    replacements: dict[str, str] = field(default_factory=dict)  # custom dictionary: wrong -> right (whole words)

    def validate(self) -> None:
        checks = [
            (self.output in ("file", "cursor"), "output must be 'file' or 'cursor'"),
            (self.hotkey_mode in ("toggle", "hold"), "hotkey_mode must be 'toggle' or 'hold'"),
            (self.asr_mode in ("mixed", "native"), "asr_mode must be 'mixed' or 'native'"),
            (100 <= self.min_silence_ms <= 3000, "min_silence_ms must be 100..3000"),
            (2.0 <= self.max_phrase_s <= 30.0, "max_phrase_s must be 2..30 (the model trains on <=30 s clips)"),
            (all(isinstance(k, str) and isinstance(v, str) and k.strip() for k, v in self.replacements.items()),
             "replacements must map non-empty strings to strings"),
        ]
        bad = [msg for ok, msg in checks if not ok]
        if bad:
            raise ValueError("invalid settings: " + "; ".join(bad))


def load(path: Path = DEFAULT_PATH) -> Settings:
    """Missing file -> defaults written out for the user to edit. Broken file -> clear error, never silent defaults."""
    if not path.exists():
        s = Settings()
        save(s, path)
        return s
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON (line {exc.lineno}, column {exc.colno}): {exc.msg}") from exc
    known = {f.name for f in fields(Settings)}
    unknown = sorted(set(raw) - known)
    if unknown:
        raise ValueError(f"{path}: unknown setting(s) {unknown}; valid: {sorted(known)}")
    s = Settings(**raw)
    s.validate()
    return s


def save(s: Settings, path: Path = DEFAULT_PATH) -> None:
    path.write_text(json.dumps(asdict(s), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
