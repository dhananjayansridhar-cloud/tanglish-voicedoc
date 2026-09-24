"""Live Tanglish dictation -> English, into a Markdown file (file mode) or at the cursor in any app (cursor mode).

mic -> Silero VAD phrases -> Indic-Transcribe-flex (mixed script) -> IndicTrans2 Tamil->English
    -> file mode: router/organiser -> typed document edits -> atomic .md write
    -> cursor mode: typed at the cursor, with a small fixed command set
Runs from the system tray; an optional always-on-top status window shows what it is doing.
"""
from __future__ import annotations

import argparse
import os
import queue
import shutil
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Protocol

from .document import DESTRUCTIVE, AppendText, Document, DocumentError, Op, Undo, write_atomic
from .organizer import Decision, OrganizerError
from .router import is_fast_undo, is_no, is_yes, route

ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = ROOT / "notes"
MAX_CLARIFY_ROUNDS = 2


class Decider(Protocol):
    def decide(self, doc: Document, command: str, earlier: list[tuple[str, str]] | None = None) -> Decision: ...


class ExternalEditError(RuntimeError):
    """The .md file was changed outside the program in a way it cannot safely merge."""


@dataclass
class _Clarifying:
    command: str
    question: str
    qa: list[tuple[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class HistoryEntry:
    time: str
    spoken: str            # what the speech model heard (Tamil/Tanglish)
    written: str | None    # what went into the document (English), None for commands
    audio: Path | None


HISTORY: list[HistoryEntry] = []   # this session's phrases, newest last; read by the history window
HISTORY_MAX = 500


def _log_line(path: Path, spoken: str, written: str | None, audio: Path | None = None) -> None:
    HISTORY.append(HistoryEntry(f"{datetime.now():%H:%M:%S}", spoken, written, audio))
    del HISTORY[:-HISTORY_MAX]
    line = f"- `{datetime.now():%H:%M:%S}` {spoken}"
    if written is not None:
        line += f"  \n  → {written}"
    if audio is not None:
        line += f"  \n  🎙 [{audio.name}]({audio.parent.name}/{audio.name})"
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")


class Controller:
    """File mode: applies each utterance to the document and keeps the .md file in sync."""

    def __init__(self, doc: Document, path: Path, organizer: Decider | None,
                 translate: Callable[[str], str] | None = None,
                 on_question: Callable[[str], None] | None = None) -> None:
        self.doc, self.path, self.organizer, self.translate = doc, path, organizer, translate
        self.on_question = on_question
        self.transcript_path = path.with_name(path.stem + ".transcript.md")
        self._confirm: Op | None = None
        self._clarify: _Clarifying | None = None
        self._lock = threading.Lock()
        self._last_written: str | None = None
        self.pending_audio: Path | None = None  # set by the pipeline so the transcript links the phrase's audio

    # ---- file sync with external-edit guard ----
    def _sync_from_disk(self) -> None:
        """If someone edited the file since our last write, adopt their edits instead of overwriting them."""
        if self._last_written is None or not self.path.exists():
            return
        on_disk = self.path.read_text(encoding="utf-8")
        if on_disk == self._last_written:
            return
        try:
            edited = Document.from_markdown(on_disk)
        except DocumentError as exc:
            raise ExternalEditError(
                f"{self.path.name} was edited outside the program and can't be merged ({exc}). "
                "Listening is paused; undo that edit or keep only '#', '##', paragraphs and '- ' bullets, then resume.") from exc
        edited.pending_question = self.doc.pending_question
        if self.doc.find(self.doc.current) and edited.find(self.doc.current):
            edited.current = self.doc.current
        self.doc.sections, self.doc.current, self.doc.title = edited.sections, edited.current, edited.title
        self._last_written = on_disk  # adopted: the next save must not re-read this version and drop new edits

    def save(self, status: str | None = None) -> None:
        with self._lock:
            self._sync_from_disk()
            text = self.doc.render(status)
            write_atomic(self.path, text)
            self._last_written = text

    def handle(self, text: str) -> str:
        """Process one utterance; returns a one-line log message."""
        text = text.strip()
        audio, self.pending_audio = self.pending_audio, None
        if not text:
            return "(empty)"
        if self._confirm is not None:
            return self._answer_confirm(text)
        if self._clarify is not None:
            return self._answer_clarify(text)
        r = route(text)
        if r.kind == "dictation":
            written = self.translate(r.text) if self.translate else r.text
            _log_line(self.transcript_path, r.text, written if self.translate else None, audio)
            if not written:
                return f"! translation returned nothing for: {r.text}"
            return self._apply(AppendText(written), f"+ {written}")
        _log_line(self.transcript_path, f"**command:** {r.text}", None, audio)
        if not r.text:
            return self._ask("Which command? For example: command new section Budget.")
        if is_fast_undo(r.text):
            return self._apply(Undo(), "* undo")
        return self._run_command(r.text, [])

    # ---- internals ----
    def _apply(self, op: Op, log: str) -> str:
        with self._lock:
            self._sync_from_disk()
            try:
                self.doc.apply(op)
            except DocumentError as exc:
                self.doc.pending_question = None
                err = str(exc)
            else:
                self.doc.pending_question = None
                err = None
        self.save(f"Could not apply: {err}" if err else None)
        return f"! {err}" if err else log

    def _ask(self, question: str) -> str:
        self.doc.pending_question = question
        self.save()
        if self.on_question:
            self.on_question(question)
        return f"? {question}"

    def _run_command(self, command: str, qa: list[tuple[str, str]]) -> str:
        if self.organizer is None:
            self.save("Organizer is off (use_llm is false); only 'scratch that' / 'undo' work.")
            return "! organizer off"
        t0 = time.perf_counter()
        try:
            d = self.organizer.decide(self.doc, command, qa or None)
        except OrganizerError as exc:
            self._clarify = None
            self.save(f"Organizer error: {exc}")
            return f"! organizer error: {exc}"
        dt = time.perf_counter() - t0
        if d.question:
            if len(qa) >= MAX_CLARIFY_ROUNDS:
                self._clarify = None
                self.save("Could not understand the command after two questions; please rephrase it.")
                return f"! gave up on: {command}"
            self._clarify = _Clarifying(command, d.question, qa)
            return self._ask(d.question) + f"  [{dt:.1f}s]"
        assert d.op is not None
        self._clarify = None
        if isinstance(d.op, DESTRUCTIVE):
            try:
                summary = self.doc.describe(d.op)
            except DocumentError as exc:
                self.save(f"Could not apply: {exc}")
                return f"! {exc}"
            self._confirm = d.op
            return self._ask(f"Confirm: {summary}? Say yes or no.") + f"  [{dt:.1f}s]"
        return self._apply(d.op, f"* {d.op}  [{dt:.1f}s]")

    def _answer_confirm(self, text: str) -> str:
        op = self._confirm
        assert op is not None
        if is_yes(text):
            self._confirm = None
            return self._apply(op, f"* confirmed {op}")
        if is_no(text):
            self._confirm = None
            self.doc.pending_question = None
            self.save("Cancelled.")
            return "- cancelled"
        return self._ask(f"{self.doc.pending_question}  Please say yes or no.")

    def _answer_clarify(self, text: str) -> str:
        c = self._clarify
        assert c is not None
        if is_no(text):
            self._clarify = None
            self.doc.pending_question = None
            self.save("Cancelled.")
            return "- cancelled"
        return self._run_command(c.command, c.qa + [(c.question, text)])


class CursorController:
    """Cursor mode: types English at the cursor of whatever app has focus. Fixed, instant commands only."""

    COMMANDS = {
        "new line": "newline", "next line": "newline", "புது லைன்": "newline",
        "new paragraph": "paragraph", "next paragraph": "paragraph", "புது பாரா": "paragraph",
        "scratch that": "scratch", "delete that": "scratch", "அதை அழி": "scratch",
        "undo": "undo", "undo pannu": "undo", "undo பண்ணு": "undo",
        "bullet": "bullet", "heading": "heading",
    }

    def __init__(self, typer, translate: Callable[[str], str] | None, transcript_path: Path) -> None:  # noqa: ANN001
        self.typer, self.translate, self.transcript_path = typer, translate, transcript_path
        self.pending_audio: Path | None = None

    def handle(self, text: str) -> str:
        text = text.strip()
        audio, self.pending_audio = self.pending_audio, None
        if not text:
            return "(empty)"
        r = route(text)
        if r.kind == "command":
            _log_line(self.transcript_path, f"**command:** {r.text}", None, audio)
            action = self.COMMANDS.get(r.text.strip(" .,!?").casefold())
            if action == "newline":
                self.typer.newline(1)
            elif action == "paragraph":
                self.typer.newline(2)
            elif action == "scratch":
                return "* scratched" if self.typer.scratch_last() else "! nothing to scratch"
            elif action == "undo":
                self.typer.undo_key()
            elif action == "bullet":
                self.typer.type("- ")
            elif action == "heading":
                self.typer.type("## ")
            else:
                return f"! unknown cursor-mode command '{r.text}' (try: new line, new paragraph, scratch that, undo, bullet, heading)"
            return f"* {action}"
        written = self.translate(r.text) if self.translate else r.text
        _log_line(self.transcript_path, r.text, written if self.translate else None, audio)
        if not written:
            return f"! translation returned nothing for: {r.text}"
        self.typer.type(written.rstrip() + " ")
        return f"+ {written}"


def _load_or_create(path: Path, title: str, resume: bool) -> Document:
    if not path.exists():
        return Document(title)
    if not resume:
        sys.exit(f"{path} already exists. Use --resume to continue it (a .bak copy is made first), or pick a new file name.")
    doc = Document.from_markdown(path.read_text(encoding="utf-8"))
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)
    print(f"Resumed {path} (backup: {backup})")
    return doc


def _make_translate(translator, replacements: dict[str, str]) -> Callable[[str], str]:  # noqa: ANN001
    from .desktop import apply_replacements

    def fn(s: str) -> str:
        out = translator(s)[0] if translator else s
        return apply_replacements(out, replacements) if replacements else out
    return fn


_MUTEX_HANDLE = None


def _single_instance() -> bool:
    """Two tray copies would fight over the microphone and GPU; the second launch just says so and exits."""
    global _MUTEX_HANDLE
    import ctypes

    ERROR_ALREADY_EXISTS = 183
    _MUTEX_HANDLE = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\VoiceDocTrayApp")
    if ctypes.windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        ctypes.windll.user32.MessageBoxW(
            None, "VoiceDoc is already running.\nLook for the microphone icon in the system tray (near the clock).",
            "VoiceDoc", 0x40)
        return False
    return True


def main(argv: list[str] | None = None) -> None:
    from . import settings as settings_mod

    ap = argparse.ArgumentParser(prog="voicedoc", description="Live Tanglish dictation into English Markdown.")
    ap.add_argument("file", type=Path, nargs="?", default=None,
                    help="Markdown file (default: today's note, notes/YYYY-MM-DD.md, resumed if it exists)")
    ap.add_argument("--settings", type=Path, default=settings_mod.DEFAULT_PATH, help="settings JSON file")
    ap.add_argument("--resume", action="store_true", help="continue an existing file this program wrote")
    ap.add_argument("--cursor", action="store_true", help="type at the cursor in any app instead of writing a file")
    ap.add_argument("--text", action="store_true", help="type utterances in the console (no mic/ASR); for testing")
    ap.add_argument("--console", action="store_true", help="no tray/overlay; log to the console")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--no-translate", action="store_true")
    args = ap.parse_args(argv)

    first_run = not args.settings.exists()
    s = settings_mod.load(args.settings)
    if args.cursor:
        s.output = "cursor"
    if args.no_llm:
        s.use_llm = False
    if args.no_translate:
        s.translate = False

    if args.file is None:
        args.file = NOTES_DIR / f"{datetime.now():%Y-%m-%d}.md"
        args.resume = True  # one-click launch: keep appending to today's note
    NOTES_DIR.mkdir(exist_ok=True)

    if not (args.console or args.text) and not _single_instance():
        return
    app = App(s, args)
    app.show_help_on_start = first_run
    if args.console or args.text:
        app.run_console()
    else:
        # Launched by pythonw (no console): sys.stdout/stderr are None, which breaks progress bars and hides
        # tracebacks. Send both to a log file next to the notes.
        if sys.stderr is None or sys.stdout is None:
            log = (NOTES_DIR / "voicedoc.log").open("a", encoding="utf-8", buffering=1)
            log.write(f"\n=== start {datetime.now():%Y-%m-%d %H:%M:%S} ===\n")
            sys.stdout = sys.stderr = log
        app.run_desktop()


class App:
    def __init__(self, s, args) -> None:  # noqa: ANN001
        from .desktop import ListenState

        self.s, self.args = s, args
        self.state = ListenState(listening=s.start_listening)
        self.stop = threading.Event()
        self.overlay = None
        self.tray = None
        self.speaker = None
        self.ctl: Controller | CursorController | None = None
        self._file_ctl: Controller | None = None
        self._focus = None  # desktop.FocusTracker, created on first switch to cursor mode
        self.mic = None     # audio.Microphone once the pipeline is running
        self._translate_fn: Callable[[str], str] | None = None
        self.last_text = ""
        self.show_help_on_start = False

    # ---- status fan-out (console, overlay, tray tooltip) ----
    def status(self, state: str, detail: str = "") -> None:
        if detail:
            self.last_text = detail
        if self.args.console or self.args.text:
            print(f"[{state}] {detail}" if detail else f"[{state}]")
        if self.overlay:
            self.overlay.show(state, detail or self.last_text)
        if self.tray:
            self.tray.title = f"voicedoc — {state}"[:120]

    def _question(self, q: str) -> None:
        self.status("question", q)
        if self.overlay and self.s.output == "file":  # in cursor mode, never steal focus from the user's editor
            self.overlay.root.after(0, self.overlay.root.deiconify)
        if self.speaker:
            self.speaker.say(q)

    # ---- model + controller setup (worker thread) ----
    def _setup(self) -> None:
        s, args = self.s, self.args
        translator = None
        if s.translate:
            self.status("loading", "Tamil→English translator…")
            from .translate import Translator

            translator = Translator(model_name=s.mt_model)
        translate_fn = _make_translate(translator, s.replacements) if (translator or s.replacements) else None
        if s.speak_questions:
            from .desktop import Speaker

            try:
                self.speaker = Speaker(self.state, s.voice, s.voice_rate)
            except Exception as exc:  # noqa: BLE001 - voice replies are optional; report and continue
                self.status("error", f"voice replies off: {exc}")
        self._translate_fn = translate_fn
        self.set_output(s.output)

    def set_output(self, mode: str) -> None:
        """Switch between writing today's note and typing at the cursor; safe while running."""
        s, args = self.s, self.args
        if mode == "cursor":
            from .desktop import CursorTyper, FocusTracker

            if self._focus is None:
                self._focus = FocusTracker()
            log = NOTES_DIR / f"{datetime.now():%Y-%m-%d}.cursor.transcript.md"
            self.ctl = CursorController(CursorTyper(self._focus), self._translate_fn, log)
        else:
            if self._file_ctl is None:
                from .organizer import Organizer

                doc = _load_or_create(args.file, args.file.stem, args.resume or args.file.exists())
                self._file_ctl = Controller(doc, args.file, Organizer(s.llm) if s.use_llm else None,
                                            self._translate_fn, self._question)
                self._file_ctl.save()
            self.ctl = self._file_ctl
        s.output = mode
        where = "the window under your cursor (click into Notepad++, VS Code, …)" if mode == "cursor" else args.file.name
        self.status("listening" if self.state.listening.is_set() else "paused", f"Output: {where}")

    def _audio_dir(self) -> Path:
        base = self.args.file if self.s.output == "file" else NOTES_DIR / f"{datetime.now():%Y-%m-%d}.cursor.md"
        d = base.with_name(base.stem + ".audio")
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _pipeline(self) -> None:
        """Worker thread: load models, then mic -> VAD -> ASR -> controller until stop."""
        try:
            self._setup()
            if self.args.text:
                return
            from .asr import Transcriber
            from .audio import Microphone, PhraseSegmenter, VadConfig, run_segmenter

            self.status("loading", "speech model (Indic-Transcribe-flex)…")
            asr = Transcriber(mode=self.s.asr_mode)
            phrases: queue.Queue = queue.Queue()
            seg = PhraseSegmenter(VadConfig(min_silence_ms=self.s.min_silence_ms, max_phrase_s=self.s.max_phrase_s),
                                  on_phrase=phrases.put, on_speech_start=lambda: self.status("listening", "hearing you…"),
                                  gate=self.state.accepts_audio)
            with Microphone(self.s.mic, on_change=lambda name: self.status(
                    "listening" if self.state.listening.is_set() else "paused", f"Microphone: {name}")) as mic:
                self.mic = mic
                threading.Thread(target=run_segmenter, args=(mic, seg, self.stop), daemon=True).start()
                self._announce_listening()
                while not self.stop.is_set():
                    try:
                        audio = phrases.get(timeout=0.5)
                    except queue.Empty:
                        continue
                    self.status("transcribing", "")
                    audio_path = None
                    if self.s.save_audio:
                        import soundfile as sf

                        audio_path = self._audio_dir() / (f"{datetime.now():%H%M%S_%f}"[:-3] + ".wav")
                        sf.write(audio_path, audio, 16000)
                    text, dt = asr(audio)
                    self.ctl.pending_audio = audio_path
                    try:
                        msg = self.ctl.handle(text) if text else "(no speech recognised)"
                    except ExternalEditError as exc:
                        self.state.listening.clear()
                        self.status("error", str(exc))
                        if self.speaker:
                            self.speaker.say("The file was edited outside the program. I paused listening.")
                        continue
                    _, peak = asr.gpu_memory_mb()
                    if self.args.console:
                        print(f"[{len(audio) / 16000:4.1f}s audio | asr {dt:.2f}s | peak {peak:.0f} MiB] {msg}")
                    if not msg.startswith("?"):
                        self._announce_listening(msg)
        except Exception as exc:  # noqa: BLE001 - shown to the user in the tray/overlay, then re-raised in console
            self.status("error", f"{type(exc).__name__}: {exc}")
            if self.args.console:
                raise

    def _announce_listening(self, detail: str = "") -> None:
        if self.state.listening.is_set():
            self.status("listening", detail or f"Speak. {self.s.hotkey} pauses.")
        else:
            self.status("paused", detail or f"Press {self.s.hotkey} to listen.")

    def _on_hotkey(self, listening: bool) -> None:
        from .desktop import beep

        beep(listening, self.s.sounds)
        self._announce_listening()

    # ---- runners ----
    def run_console(self) -> None:
        if self.args.text:
            self._setup()
            print("Type an utterance per line (start with 'command' for edits). Ctrl+Z then Enter to quit.")
            for line in sys.stdin:
                print(self.ctl.handle(line))
            return
        from .desktop import Hotkey

        hk = Hotkey(self.s.hotkey, self.s.hotkey_mode, self.state, self._on_hotkey)
        hk.start()
        worker = threading.Thread(target=self._pipeline, daemon=True)
        worker.start()
        try:
            while worker.is_alive():
                worker.join(0.5)
        except KeyboardInterrupt:
            print("\nStopping.")
        finally:
            self.stop.set()
            hk.stop()

    def run_desktop(self) -> None:
        from .desktop import Hotkey, Overlay, Tray

        self.overlay = Overlay(on_close=lambda: self.overlay.root.withdraw())  # closing the window only hides it
        if not self.s.overlay:
            self.overlay.root.withdraw()
        self.tray = Tray(self)
        self.tray.start()
        if self.show_help_on_start:
            self.show_help()
        hk = Hotkey(self.s.hotkey, self.s.hotkey_mode, self.state, self._on_hotkey)
        hk.start()
        threading.Thread(target=self._pipeline, daemon=True).start()
        try:
            self.overlay.run()
        finally:
            self.stop.set()
            hk.stop()
            if self.speaker:
                self.speaker.close()
            self.tray.stop()

    # ---- tray actions ----
    def toggle_listening(self) -> None:
        if self.state.listening.is_set():
            self.state.listening.clear()
        else:
            self.state.listening.set()
        self._on_hotkey(self.state.listening.is_set())

    def open_notes(self) -> None:
        target = self.args.file if self.s.output == "file" else NOTES_DIR
        os.startfile(target)  # noqa: S606 - opens the user's own file with its default app

    def open_settings(self) -> None:
        os.startfile(self.args.settings)  # noqa: S606

    def show_status(self) -> None:
        if self.overlay:
            self.overlay.root.after(0, self.overlay.root.deiconify)

    def set_mic(self, mic: str) -> None:
        self.s.mic = mic
        if self.mic is not None:
            try:
                self.mic.switch(mic)
            except Exception as exc:  # noqa: BLE001 - shown to the user; the watcher retries
                self.status("error", f"microphone: {exc}")

    def show_help(self) -> None:
        if self.overlay:
            from .desktop import open_help_window

            self.overlay.root.after(0, lambda: open_help_window(self.overlay.root, self.s, self.args.file))

    def show_history(self) -> None:
        if self.overlay:
            from .desktop import open_history_window

            self.overlay.root.after(0, lambda: open_history_window(self.overlay.root, HISTORY))

    def quit(self) -> None:
        self.stop.set()
        if self.overlay:
            self.overlay.close()
