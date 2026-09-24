from pathlib import Path

import pytest

from voicedoc.app import Controller
from voicedoc.document import (AppendText, Bullets, DeleteSection, Document, DocumentError, MakeBullets, MoveLast,
                               NewSection, Paragraph, RenameSection, Undo, parse_op, write_atomic)
from voicedoc.organizer import Decision
from voicedoc.router import is_no, is_yes, route


# ---------- document ----------

def test_dictation_goes_to_current_section_and_renders():
    d = Document("Day")
    d.apply(AppendText("நாளைக்கு client meeting 3 மணிக்கு"))
    d.apply(NewSection("Action items"))
    d.apply(AppendText("invoice anuppu"))
    md = d.render()
    assert md.startswith("# Day\n")
    assert "## Notes\n\nநாளைக்கு client meeting 3 மணிக்கு" in md
    assert "## Action items ✎\n\ninvoice anuppu" in md


def test_move_last_creates_target_and_undo_restores():
    d = Document("Day")
    d.apply(AppendText("one"))
    d.apply(AppendText("two"))
    d.apply(MoveLast("Later"))
    assert [b.text for b in d.find("Notes").blocks] == ["one"]
    assert [b.text for b in d.find("Later").blocks] == ["two"]
    d.apply(Undo())
    assert d.find("Later") is None
    assert [b.text for b in d.find("Notes").blocks] == ["one", "two"]


def test_make_bullets_last_splits_sentences():
    d = Document("Day")
    d.apply(AppendText("Milk vaanganum. Bread vaanganum. Eggs."))
    d.apply(MakeBullets("last"))
    assert d.find("Notes").blocks == [Bullets(["Milk vaanganum.", "Bread vaanganum.", "Eggs."])]


def test_make_bullets_section_merges_paragraphs():
    d = Document("Day")
    for t in ("a", "b", "c"):
        d.apply(AppendText(t))
    d.apply(MakeBullets("section"))
    assert d.find("Notes").blocks == [Bullets(["a", "b", "c"])]


def test_errors_do_not_change_document_or_history():
    d = Document("Day")
    with pytest.raises(DocumentError):
        d.apply(MoveLast("X"))  # empty section
    with pytest.raises(DocumentError):
        d.apply(Undo())  # the failed op left no history entry


def test_rename_keeps_current_pointer():
    d = Document("Day")
    d.apply(NewSection("Budjet"))
    d.apply(RenameSection("budjet", "Budget"))
    assert d.current == "Budget"


def test_describe_destructive_counts_items():
    d = Document("Day")
    d.apply(NewSection("Travel"))
    d.apply(AppendText("x"))
    d.apply(AppendText("y"))
    assert "2 item(s)" in d.describe(DeleteSection("travel"))


def test_parse_op_rejects_malformed():
    assert parse_op({"op": "new_section", "title": " Budget "}) == NewSection("Budget")
    for bad in ({"op": "new_section"}, {"op": "explode"}, {"op": "make_bullets", "scope": "all"}):
        with pytest.raises(DocumentError):
            parse_op(bad)


def test_markdown_round_trip():
    d = Document("Day")
    d.apply(AppendText("p1"))
    d.apply(NewSection("List"))
    d.apply(AppendText("a. b."))
    d.apply(MakeBullets("last"))
    d.apply(AppendText("tail"))
    d.pending_question = "Which one?"
    back = Document.from_markdown(d.render(status="listening…"))
    assert back.title == "Day"
    assert back.current == "List"
    assert back.find("Notes").blocks == [Paragraph("p1")]
    assert back.find("List").blocks == [Bullets(["a.", "b."]), Paragraph("tail")]


def test_from_markdown_refuses_unsupported_structure():
    with pytest.raises(DocumentError):
        Document.from_markdown("# T\n\n## A\n\n### deeper\n")


def test_write_atomic(tmp_path: Path):
    p = tmp_path / "sub" / "n.md"
    write_atomic(p, "one")
    write_atomic(p, "two")
    assert p.read_text(encoding="utf-8") == "two"
    assert [f.name for f in p.parent.iterdir()] == ["n.md"]


# ---------- router ----------

@pytest.mark.parametrize("text,kind,rest", [
    ("command new section Budget", "command", "new section Budget"),
    ("Command, idha move pannu.", "command", "idha move pannu"),
    ("கமாண்ட் undo பண்ணு", "command", "undo பண்ணு"),
    ("commander vandhaar", "dictation", "commander vandhaar"),
    ("naan command panna maaten", "dictation", "naan command panna maaten"),
])
def test_route(text, kind, rest):
    r = route(text)
    assert (r.kind, r.text) == (kind, rest)


def test_yes_no():
    assert is_yes("Yes.") and is_yes("சரி போடு") and is_yes("ok")
    assert is_no("வேண்டாம்") and is_no("No, leave it") and not is_yes("no")


# ---------- controller ----------

class FakeOrganizer:
    def __init__(self, *decisions: Decision) -> None:
        self.decisions = list(decisions)
        self.calls: list[tuple[str, object]] = []

    def decide(self, doc, command, earlier=None):
        self.calls.append((command, earlier))
        return self.decisions.pop(0)


def _ctl(tmp_path, *decisions):
    return Controller(Document("T"), tmp_path / "n.md", FakeOrganizer(*decisions))


def test_dictation_is_written_live(tmp_path):
    c = _ctl(tmp_path)
    c.handle("first line")
    assert "first line" in (tmp_path / "n.md").read_text(encoding="utf-8")


def test_destructive_command_needs_confirmation(tmp_path):
    c = _ctl(tmp_path, Decision(DeleteSection("Notes"), None))
    c.handle("keep me")
    msg = c.handle("command Notes section-a delete pannu")
    assert msg.startswith("? Confirm: delete section 'Notes' with 1 item(s)")
    assert "**Question:** Confirm" in (tmp_path / "n.md").read_text(encoding="utf-8")
    assert "keep me" in c.doc.render()
    c.handle("maybe")                     # neither yes nor no -> asks again, nothing applied
    assert "keep me" in c.doc.render()
    c.handle("no")
    assert "keep me" in c.doc.render() and c.doc.pending_question is None


def test_destructive_command_applies_on_yes(tmp_path):
    c = _ctl(tmp_path, Decision(DeleteSection("Notes"), None))
    c.handle("gone soon")
    c.handle("command delete Notes")
    c.handle("ஆமா")
    assert "gone soon" not in c.doc.render()


def test_clarification_round_trip(tmp_path):
    org = FakeOrganizer(Decision(None, "Budget-a Travel-a?"), Decision(MoveLast("Travel"), None))
    c = Controller(Document("T"), tmp_path / "n.md", org)
    c.handle("ticket book pannanum")
    assert c.handle("command idha andha section-ku move pannu").startswith("? Budget-a Travel-a?")
    c.handle("Travel")
    assert org.calls[1] == ("idha andha section-ku move pannu", [("Budget-a Travel-a?", "Travel")])
    assert [b.text for b in c.doc.find("Travel").blocks] == ["ticket book pannanum"]
    assert c.doc.pending_question is None


def test_dictation_is_translated_and_original_logged(tmp_path):
    c = Controller(Document("T"), tmp_path / "n.md", FakeOrganizer(), translate=lambda s: "Meeting tomorrow at 3")
    c.handle("நாளைக்கு 3 மணிக்கு மீட்டிங்")
    md = (tmp_path / "n.md").read_text(encoding="utf-8")
    log = (tmp_path / "n.transcript.md").read_text(encoding="utf-8")
    assert "Meeting tomorrow at 3" in md and "மீட்டிங்" not in md
    assert "நாளைக்கு 3 மணிக்கு மீட்டிங்" in log and "Meeting tomorrow at 3" in log


def test_fast_undo_skips_the_model(tmp_path):
    org = FakeOrganizer()
    c = Controller(Document("T"), tmp_path / "n.md", org)
    c.handle("oops")
    assert c.handle("command scratch that") == "* undo"
    assert org.calls == [] and "oops" not in c.doc.render()


def test_external_edit_is_adopted_not_overwritten(tmp_path):
    c = Controller(Document("T"), tmp_path / "n.md", FakeOrganizer())
    c.handle("first")
    p = tmp_path / "n.md"
    p.write_text(p.read_text(encoding="utf-8").replace("first", "first, fixed by hand"), encoding="utf-8")
    c.handle("second")
    md = p.read_text(encoding="utf-8")
    assert "first, fixed by hand" in md and "second" in md


def test_unmergeable_external_edit_stops_writing(tmp_path):
    from voicedoc.app import ExternalEditError

    c = Controller(Document("T"), tmp_path / "n.md", FakeOrganizer())
    c.handle("first")
    p = tmp_path / "n.md"
    p.write_text(p.read_text(encoding="utf-8") + "\n### my own heading\n", encoding="utf-8")
    with pytest.raises(ExternalEditError):
        c.handle("second")
    assert "### my own heading" in p.read_text(encoding="utf-8")  # user's edit survives


def test_replacements_whole_word_case_insensitive():
    from voicedoc.desktop import apply_replacements

    r = {"diarrhegation": "diarization", "deep gram": "Deepgram"}
    assert apply_replacements("Accuracy, Diarrhegation and deep gram.", r) == "Accuracy, diarization and Deepgram."
    assert apply_replacements("deep grammar", r) == "deep grammar"


def test_settings_roundtrip_and_validation(tmp_path):
    from voicedoc import settings as st

    p = tmp_path / "s.json"
    s = st.load(p)                       # missing -> defaults written
    assert p.exists() and s.hotkey == "ctrl+shift+space"
    p.write_text('{"hotkey_mode": "sometimes"}', encoding="utf-8")
    with pytest.raises(ValueError, match="hotkey_mode"):
        st.load(p)
    p.write_text('{"hotkey": "ctrl+alt+d",}', encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        st.load(p)
    p.write_text('{"hotkee": "x"}', encoding="utf-8")
    with pytest.raises(ValueError, match="unknown setting"):
        st.load(p)


class FakeTyper:
    def __init__(self):
        self.out = ""
        self.history = []

    def type(self, t):
        self.out += t
        self.history.append(t)

    def newline(self, n=1):
        self.out += "\n" * n
        self.history.append("\n" * n)

    def scratch_last(self):
        if not self.history:
            return False
        self.out = self.out[: -len(self.history.pop())]
        return True

    def undo_key(self):
        self.out += "<ctrl+z>"


def test_cursor_mode_types_english_and_handles_commands(tmp_path):
    from voicedoc.app import CursorController

    t = FakeTyper()
    c = CursorController(t, lambda s: "Hello there", tmp_path / "log.md")
    c.handle("வணக்கம்")
    c.handle("command new paragraph")
    c.handle("வணக்கம்")
    c.handle("command scratch that")
    assert t.out == "Hello there \n\n"
    assert c.handle("command dance").startswith("! unknown")


def test_clarification_gives_up_after_two_rounds(tmp_path):
    q = Decision(None, "Which?")
    c = _ctl(tmp_path, q, q, q)
    c.handle("command do the thing")
    c.handle("that one")
    msg = c.handle("the other one")
    assert msg.startswith("! gave up")
    assert c.handle("back to dictation").startswith("+ ")
