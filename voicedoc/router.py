"""Deterministic split between dictation and spoken commands, plus yes/no answers."""
from __future__ import annotations

import re
from dataclasses import dataclass

# The spoken command word, as the speech model may write it in mixed-script or native mode.
COMMAND_WORDS = ("command", "commands", "கமாண்ட்", "கமாண்டு", "கமான்ட்", "கமாண்ட")

YES_WORDS = ("yes", "yeah", "ok", "okay", "sure", "confirm", "ஆமா", "ஆமாம்", "ஆம்", "சரி", "sari", "seri", "pannu", "பண்ணு")
NO_WORDS = ("no", "nope", "cancel", "stop", "வேண்டாம்", "வேணாம்", "இல்லை", "இல்ல", "venam", "vendam", "illa")

_EDGE_PUNCT = " \t\r\n.,!?;:'\"-–—।"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip(_EDGE_PUNCT).casefold()


@dataclass(frozen=True)
class Routed:
    kind: str  # "dictation" | "command"
    text: str


def route(text: str) -> Routed:
    norm = _norm(text)
    for word in COMMAND_WORDS:
        if norm == word or norm.startswith(word + " ") or norm.startswith(word + ","):
            rest = text.strip(_EDGE_PUNCT)[len(word):].strip(_EDGE_PUNCT)
            return Routed("command", rest)
    return Routed("dictation", text.strip())


FAST_UNDO = ("undo", "undo pannu", "undo பண்ணு", "அதை undo பண்ணு", "scratch that", "cancel that", "அன்டு", "அன்டூ")


def is_fast_undo(command_text: str) -> bool:
    """Commands handled without the organiser model, so they are instant."""
    return _norm(command_text) in FAST_UNDO


def _first_word(text: str) -> str:
    norm = _norm(text)
    return norm.split(" ", 1)[0].strip(_EDGE_PUNCT) if norm else ""


def is_yes(text: str) -> bool:
    return _first_word(text) in YES_WORDS


def is_no(text: str) -> bool:
    return _first_word(text) in NO_WORDS
