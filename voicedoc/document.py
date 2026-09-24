"""In-memory Markdown document, the edit operations that change it, and atomic file output."""
from __future__ import annotations

import copy
import os
import re
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union

DEFAULT_SECTION = "Notes"
UNDO_DEPTH = 50


@dataclass
class Paragraph:
    text: str


@dataclass
class Bullets:
    items: list[str]


Block = Union[Paragraph, Bullets]


@dataclass
class Section:
    title: str
    blocks: list[Block] = field(default_factory=list)


class DocumentError(ValueError):
    """An edit that cannot be applied, with a message meant for the user."""


# ---------- edit operations ----------

@dataclass(frozen=True)
class AppendText:
    text: str


@dataclass(frozen=True)
class NewSection:
    title: str


@dataclass(frozen=True)
class GoToSection:
    title: str


@dataclass(frozen=True)
class MoveLast:
    to_section: str


@dataclass(frozen=True)
class MakeBullets:
    scope: str  # "last" = last paragraph split into sentences; "section" = every paragraph of the current section


@dataclass(frozen=True)
class RenameSection:
    old: str
    new: str


@dataclass(frozen=True)
class DeleteLast:
    pass


@dataclass(frozen=True)
class DeleteSection:
    title: str


@dataclass(frozen=True)
class Undo:
    pass


Op = Union[AppendText, NewSection, GoToSection, MoveLast, MakeBullets, RenameSection, DeleteLast, DeleteSection, Undo]

DESTRUCTIVE = (DeleteLast, DeleteSection)


def _req_str(d: dict, key: str) -> str:
    v = d.get(key)
    if not isinstance(v, str) or not v.strip():
        raise DocumentError(f"operation '{d.get('op')}' needs a non-empty '{key}'")
    return v.strip()


def parse_op(d: dict) -> Op:
    """Build a typed operation from the organiser's JSON output; rejects anything malformed."""
    kind = d.get("op")
    if kind == "append_text":
        return AppendText(_req_str(d, "text"))
    if kind == "new_section":
        return NewSection(_req_str(d, "title"))
    if kind == "go_to_section":
        return GoToSection(_req_str(d, "title"))
    if kind == "move_last":
        return MoveLast(_req_str(d, "to_section"))
    if kind == "make_bullets":
        scope = d.get("scope", "last")
        if scope not in ("last", "section"):
            raise DocumentError("make_bullets scope must be 'last' or 'section'")
        return MakeBullets(scope)
    if kind == "rename_section":
        return RenameSection(_req_str(d, "old"), _req_str(d, "new"))
    if kind == "delete_last":
        return DeleteLast()
    if kind == "delete_section":
        return DeleteSection(_req_str(d, "title"))
    if kind == "undo":
        return Undo()
    raise DocumentError(f"unknown operation: {kind!r}")


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?।])\s+")


def _split_sentences(text: str) -> list[str]:
    parts = [p.strip() for p in _SENTENCE_SPLIT.split(text) if p.strip()]
    return parts or [text.strip()]


CURRENT_MARKER = " ✎"


class Document:
    def __init__(self, title: str) -> None:
        self.title = title
        self.sections: list[Section] = [Section(DEFAULT_SECTION)]
        self.current = DEFAULT_SECTION
        self.pending_question: str | None = None
        self._history: list[tuple[list[Section], str]] = []

    @classmethod
    def from_markdown(cls, text: str) -> "Document":
        """Read back a file this program wrote. Raises on structure it would not preserve."""
        doc = cls("Notes")
        doc.sections = []
        body = text.split("\n---\n> ", 1)[0]  # drop the status/question footer
        cur: Section | None = None
        para: list[str] = []

        def flush() -> None:
            if para and cur is not None:
                cur.blocks.append(Paragraph(" ".join(para)))
            para.clear()

        prev_bullet = False
        for n, raw in enumerate(body.splitlines(), 1):
            line = raw.rstrip()
            is_bullet = line.startswith("- ")
            if line.startswith("# ") and cur is None and not doc.sections:
                doc.title = line[2:].strip()
            elif line.startswith("## "):
                flush()
                title = line[3:]
                if title.endswith(CURRENT_MARKER):
                    title = title[: -len(CURRENT_MARKER)]
                    doc.current = title.strip()
                cur = Section(title.strip())
                doc.sections.append(cur)
            elif line.startswith("#"):
                raise DocumentError(f"line {n}: heading level other than # / ## is not supported: {line[:60]!r}")
            elif is_bullet:
                flush()
                if cur is None:
                    raise DocumentError(f"line {n}: bullet before any '## ' section")
                if prev_bullet and cur.blocks and isinstance(cur.blocks[-1], Bullets):
                    cur.blocks[-1].items.append(line[2:].strip())
                else:
                    cur.blocks.append(Bullets([line[2:].strip()]))
            elif not line.strip():
                flush()
            else:
                if cur is None:
                    raise DocumentError(f"line {n}: text before any '## ' section: {line[:60]!r}")
                para.append(line.strip())
            prev_bullet = is_bullet
        flush()
        if not doc.sections:
            doc.sections = [Section(DEFAULT_SECTION)]
        if doc.find(doc.current) is None:
            doc.current = doc.sections[-1].title
        return doc

    # ---- queries ----
    def outline(self) -> list[str]:
        return [s.title for s in self.sections]

    def find(self, title: str) -> Section | None:
        key = title.strip().casefold()
        for s in self.sections:
            if s.title.casefold() == key:
                return s
        return None

    def _require(self, title: str) -> Section:
        s = self.find(title)
        if s is None:
            raise DocumentError(f"no section named '{title}' (sections: {', '.join(self.outline())})")
        return s

    def describe(self, op: Op) -> str:
        """Human-readable summary, used when asking the user to confirm a destructive edit."""
        if isinstance(op, DeleteLast):
            sec = self._require(self.current)
            if not sec.blocks:
                return f"delete the last block of '{sec.title}' (it is empty)"
            last = sec.blocks[-1]
            preview = last.text if isinstance(last, Paragraph) else "; ".join(last.items)
            return f"delete the last block of '{sec.title}': \"{preview[:80]}\""
        if isinstance(op, DeleteSection):
            sec = self._require(op.title)
            n = sum(1 if isinstance(b, Paragraph) else len(b.items) for b in sec.blocks)
            return f"delete section '{sec.title}' with {n} item(s)"
        return type(op).__name__

    # ---- mutation ----
    def apply(self, op: Op) -> None:
        if isinstance(op, Undo):
            if not self._history:
                raise DocumentError("nothing to undo")
            self.sections, self.current = self._history.pop()
            return
        snapshot = (copy.deepcopy(self.sections), self.current)
        self._apply(op)
        self._history.append(snapshot)
        del self._history[:-UNDO_DEPTH]

    def _apply(self, op: Op) -> None:
        if isinstance(op, AppendText):
            self._require(self.current).blocks.append(Paragraph(op.text.strip()))
        elif isinstance(op, NewSection):
            if self.find(op.title) is None:
                self.sections.append(Section(op.title.strip()))
            self.current = self._require(op.title).title
        elif isinstance(op, GoToSection):
            self.current = self._require(op.title).title
        elif isinstance(op, MoveLast):
            src = self._require(self.current)
            if not src.blocks:
                raise DocumentError(f"section '{src.title}' is empty, nothing to move")
            dst = self.find(op.to_section)
            if dst is None:
                dst = Section(op.to_section.strip())
                self.sections.append(dst)
            if dst is src:
                raise DocumentError(f"'{src.title}' is already the current section")
            dst.blocks.append(src.blocks.pop())
        elif isinstance(op, MakeBullets):
            sec = self._require(self.current)
            if op.scope == "last":
                idx = next((i for i in range(len(sec.blocks) - 1, -1, -1) if isinstance(sec.blocks[i], Paragraph)), None)
                if idx is None:
                    raise DocumentError(f"no paragraph in '{sec.title}' to turn into bullets")
                para = sec.blocks[idx]
                assert isinstance(para, Paragraph)
                sec.blocks[idx] = Bullets(_split_sentences(para.text))
            else:
                items = [b.text for b in sec.blocks if isinstance(b, Paragraph)]
                if not items:
                    raise DocumentError(f"no paragraphs in '{sec.title}' to turn into bullets")
                kept = [b for b in sec.blocks if isinstance(b, Bullets)]
                sec.blocks = kept + [Bullets(items)]
        elif isinstance(op, RenameSection):
            sec = self._require(op.old)
            if self.find(op.new) is not None and self.find(op.new) is not sec:
                raise DocumentError(f"a section named '{op.new}' already exists")
            if self.current == sec.title:
                self.current = op.new.strip()
            sec.title = op.new.strip()
        elif isinstance(op, DeleteLast):
            sec = self._require(self.current)
            if not sec.blocks:
                raise DocumentError(f"section '{sec.title}' is already empty")
            sec.blocks.pop()
        elif isinstance(op, DeleteSection):
            sec = self._require(op.title)
            self.sections.remove(sec)
            if not self.sections:
                self.sections.append(Section(DEFAULT_SECTION))
            if self.find(self.current) is None:
                self.current = self.sections[-1].title
        else:
            raise DocumentError(f"unsupported operation {op!r}")

    # ---- output ----
    def render(self, status: str | None = None) -> str:
        out = [f"# {self.title}", ""]
        for s in self.sections:
            if not s.blocks and s.title == DEFAULT_SECTION and len(self.sections) > 1:
                continue
            marker = CURRENT_MARKER if s.title == self.current else ""
            out += [f"## {s.title}{marker}", ""]
            for b in s.blocks:
                if isinstance(b, Paragraph):
                    out += [b.text, ""]
                else:
                    out += [f"- {item}" for item in b.items] + [""]
        if self.pending_question or status:
            out.append("---")
            if self.pending_question:
                out.append(f"> **Question:** {self.pending_question}")
            if status:
                out.append(f"> _{status}_")
            out.append("")
        return "\n".join(out)


def write_atomic(path: Path, text: str) -> None:
    """Write via a temp file + os.replace so a viewer never reads a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    for attempt in range(5):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            # Windows: another process (editor, antivirus) briefly holds the target open.
            if attempt == 4:
                os.unlink(tmp)
                raise
            time.sleep(0.05 * (attempt + 1))
