"""Turns a spoken command into one document edit (or a clarifying question) using a local Ollama model."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from .document import Document, DocumentError, Op, Paragraph, parse_op

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

OP_NAMES = ["append_text", "new_section", "go_to_section", "move_last", "make_bullets",
            "rename_section", "delete_last", "delete_section", "undo"]

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["edit", "clarify"]},
        "question": {"type": "string"},
        "op": {
            "type": "object",
            "properties": {
                "op": {"type": "string", "enum": OP_NAMES},
                "text": {"type": "string"},
                "title": {"type": "string"},
                "to_section": {"type": "string"},
                "scope": {"type": "string", "enum": ["last", "section"]},
                "old": {"type": "string"},
                "new": {"type": "string"},
            },
            "required": ["op"],
        },
    },
    "required": ["action"],
}

SYSTEM_PROMPT = """You control a Markdown notes document by voice. The user speaks colloquial Tamil mixed with English (Tanglish). You receive ONE spoken command and must return ONE edit operation as JSON, or ask ONE short clarifying question.

Operations (field "op"):
- new_section {title}: create a section (or switch to it if it exists) and make it current.
- go_to_section {title}: make an existing section current; later dictation goes there.
- move_last {to_section}: move the last paragraph or list of the current section to another section (created if missing).
- make_bullets {scope}: scope "last" turns the last paragraph into a bullet list; scope "section" turns all paragraphs of the current section into one bullet list.
- rename_section {old, new}
- delete_last: delete the last paragraph or list of the current section.
- delete_section {title}
- undo: undo the previous edit.
- append_text {text}: add a paragraph with exactly this text (only when the user dictates text inside a command).

Rules:
- Section titles: short, in the language the user used, matching an existing section title exactly when the user refers to one.
- If the command is ambiguous (for example it could mean two different sections, or you cannot tell which operation is meant), return {"action": "clarify", "question": "..."} and ask in the same Tanglish style the user spoke, in one short sentence.
- Never invent content. Never return more than one operation.

Examples:
command: "meeting notes nu oru new section podu" -> {"action":"edit","op":{"op":"new_section","title":"Meeting notes"}}
command: "idha action items-ku move pannu" -> {"action":"edit","op":{"op":"move_last","to_section":"Action items"}}
command: "last paragraph-a bullet points-a maathu" -> {"action":"edit","op":{"op":"make_bullets","scope":"last"}}
command: "அதை undo பண்ணு" -> {"action":"edit","op":{"op":"undo"}}
command: "andha section-a delete pannu" with sections Notes, Budget, Travel and current Notes -> {"action":"clarify","question":"Endha section delete pannanum — Budget-a Travel-a?"}
"""


class OrganizerError(RuntimeError):
    """The local model could not be reached or returned something unusable."""


@dataclass(frozen=True)
class Decision:
    op: Op | None
    question: str | None


def _state(doc: Document) -> dict:
    cur = doc.find(doc.current)
    last = None
    if cur and cur.blocks:
        b = cur.blocks[-1]
        last = b.text if isinstance(b, Paragraph) else "; ".join(b.items)
    return {"sections": doc.outline(), "current_section": doc.current, "last_block_of_current": last}


class Organizer:
    def __init__(self, model: str, timeout_s: float = 120.0) -> None:
        self.model = model
        self.timeout_s = timeout_s

    def decide(self, doc: Document, command: str, earlier: list[tuple[str, str]] | None = None) -> Decision:
        """`earlier` holds (question, answer) pairs from a clarification exchange about this same command."""
        user = {"document": _state(doc), "command": command}
        if earlier:
            user["clarifications"] = [{"you_asked": q, "user_answered": a} for q, a in earlier]
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT},
                         {"role": "user", "content": json.dumps(user, ensure_ascii=False)}],
            "format": RESPONSE_SCHEMA,
            "stream": False,
            "think": False,
            # num_gpu 0 keeps the model on CPU: the 6 GB GPU is reserved for speech recognition + translation.
            "options": {"temperature": 0, "num_gpu": 0},
        }
        req = urllib.request.Request(OLLAMA_URL, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise OrganizerError(f"cannot reach Ollama at {OLLAMA_URL} ({exc.reason}); is Ollama running and is '{self.model}' pulled?") from exc
        content = payload.get("message", {}).get("content", "")
        try:
            out = json.loads(content)
        except json.JSONDecodeError as exc:
            raise OrganizerError(f"model returned non-JSON: {content[:200]!r}") from exc
        if out.get("action") == "clarify":
            q = (out.get("question") or "").strip()
            if not q:
                raise OrganizerError("model asked to clarify but gave no question")
            return Decision(None, q)
        try:
            return Decision(parse_op(out.get("op") or {}), None)
        except DocumentError as exc:
            raise OrganizerError(f"model returned an invalid operation: {exc}") from exc
