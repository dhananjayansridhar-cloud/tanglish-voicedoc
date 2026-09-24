"""Desktop ease-of-use: global hotkey, status overlay, spoken questions, sounds, typing at the cursor, custom dictionary."""
from __future__ import annotations

import queue
import re
import threading
from collections.abc import Callable


# ---------- custom dictionary ----------

def apply_replacements(text: str, replacements: dict[str, str]) -> str:
    """Whole-word, case-insensitive replacements, longest key first (so 'deep gram' wins over 'deep')."""
    for wrong in sorted(replacements, key=len, reverse=True):
        text = re.sub(rf"(?<!\w){re.escape(wrong)}(?!\w)", replacements[wrong], text, flags=re.IGNORECASE)
    return text


# ---------- listening state shared by hotkey, overlay, speaker and audio ----------

class ListenState:
    def __init__(self, listening: bool) -> None:
        self.listening = threading.Event()
        if listening:
            self.listening.set()
        self.muted = threading.Event()  # set while the assistant is speaking, so the mic does not hear it

    def accepts_audio(self) -> bool:
        return self.listening.is_set() and not self.muted.is_set()


def _pynput_combo(hotkey: str) -> str:
    """'ctrl+shift+space' -> '<ctrl>+<shift>+<space>' (pynput GlobalHotKeys syntax)."""
    parts = [p.strip().lower() for p in hotkey.split("+") if p.strip()]
    return "+".join(p if len(p) == 1 else f"<{p}>" for p in parts)


class Hotkey:
    """toggle: press once to pause/resume. hold: listen only while the combination is held."""

    def __init__(self, hotkey: str, mode: str, state: ListenState, on_change: Callable[[bool], None]) -> None:
        from pynput import keyboard

        self._kb, self.state, self.on_change, self.mode = keyboard, state, on_change, mode
        combo = _pynput_combo(hotkey)
        if mode == "toggle":
            self._listener = keyboard.GlobalHotKeys({combo: self._toggle})
        else:
            self._hk = keyboard.HotKey(keyboard.HotKey.parse(combo), self._pressed)
            self._held = False
            self._listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)

    def _toggle(self) -> None:
        if self.state.listening.is_set():
            self.state.listening.clear()
        else:
            self.state.listening.set()
        self.on_change(self.state.listening.is_set())

    def _pressed(self) -> None:
        if not self._held:
            self._held = True
            self.state.listening.set()
            self.on_change(True)

    def _on_press(self, key) -> None:  # noqa: ANN001 - pynput key object
        self._hk.press(self._listener.canonical(key))

    def _on_release(self, key) -> None:  # noqa: ANN001
        self._hk.release(self._listener.canonical(key))
        if self._held:
            self._held = False
            self.state.listening.clear()
            self.on_change(False)

    def start(self) -> None:
        self._listener.start()

    def stop(self) -> None:
        self._listener.stop()


# ---------- sounds ----------

def beep(on: bool, enabled: bool) -> None:
    if not enabled:
        return
    import winsound

    threading.Thread(target=winsound.Beep, args=((880, 90) if on else (440, 90)), daemon=True).start()


# ---------- spoken questions (Windows SAPI via pyttsx3; any installed SAPI voice works) ----------

class Speaker:
    """Owns the pyttsx3 engine on one thread (it is not thread-safe) and mutes the mic while talking."""

    def __init__(self, state: ListenState, voice: str | None, rate: int) -> None:
        self.state = state
        self._q: queue.Queue[str | None] = queue.Queue()
        self._ready = threading.Event()
        self.voice_name: str | None = None
        self._error: Exception | None = None
        threading.Thread(target=self._run, args=(voice, rate), daemon=True).start()
        self._ready.wait(10)
        if self._error:
            raise self._error

    def _run(self, voice: str | None, rate: int) -> None:
        try:
            import pyttsx3

            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            if voice:
                match = [v for v in voices if voice.lower() in v.name.lower()]
                if not match:
                    raise ValueError(f"no Windows voice matching {voice!r}; installed: {[v.name for v in voices]}")
                engine.setProperty("voice", match[0].id)
            else:
                # Prefer neural voices (e.g. Narrator voices exposed by NaturalVoiceSAPIAdapter), English first.
                ranked = sorted(voices, key=lambda v: ("natural" not in v.name.lower(), "english" not in v.name.lower()))
                if ranked:
                    engine.setProperty("voice", ranked[0].id)
            engine.setProperty("rate", rate)
            self.voice_name = next((v.name for v in voices if v.id == engine.getProperty("voice")), None)
        except Exception as exc:  # noqa: BLE001 - surfaced to the caller of __init__
            self._error = exc
            self._ready.set()
            return
        self._ready.set()
        while (text := self._q.get()) is not None:
            self.state.muted.set()
            try:
                engine.say(text)
                engine.runAndWait()
            finally:
                threading.Timer(0.3, self.state.muted.clear).start()  # let the room echo die down

    def say(self, text: str) -> None:
        self._q.put(text)

    def close(self) -> None:
        self._q.put(None)


# ---------- typing at the cursor (cursor mode) ----------

_SHELL_CLASSES = {"Shell_TrayWnd", "Shell_SecondaryTrayWnd", "NotifyIconOverflowWindow",
                  "TopLevelWindowForOverflowXamlIsland", "Progman", "WorkerW"}


class FocusTracker:
    """Remembers the last real app window the user worked in, ignoring the taskbar/tray and our own windows.

    Clicking the tray icon makes the taskbar the foreground window; without this, typed text would go nowhere.
    """

    def __init__(self) -> None:
        import ctypes
        import os
        from ctypes import wintypes

        self._u32 = ctypes.windll.user32
        self._wintypes, self._ctypes = wintypes, ctypes
        self._pid = os.getpid()
        self.last: int | None = None
        threading.Thread(target=self._run, daemon=True).start()

    def _is_app_window(self, hwnd: int) -> bool:
        if not hwnd:
            return False
        pid = self._wintypes.DWORD()
        self._u32.GetWindowThreadProcessId(hwnd, self._ctypes.byref(pid))
        if pid.value == self._pid:
            return False
        buf = self._ctypes.create_unicode_buffer(256)
        self._u32.GetClassNameW(hwnd, buf, 256)
        return buf.value not in _SHELL_CLASSES

    def _run(self) -> None:
        import time

        while True:
            hwnd = self._u32.GetForegroundWindow()
            if self._is_app_window(hwnd):
                self.last = hwnd
            time.sleep(0.15)

    def ensure_target(self) -> None:
        """If focus is on the taskbar/tray or our own window, give it back to the user's last app."""
        import time

        fg = self._u32.GetForegroundWindow()
        if not self._is_app_window(fg) and self.last and self._u32.IsWindow(self.last):
            self._u32.SetForegroundWindow(self.last)
            time.sleep(0.08)


class CursorTyper:
    """Types into whatever window has focus. Uses key events, so the user's clipboard is never touched."""

    def __init__(self, focus: FocusTracker | None = None) -> None:
        from pynput.keyboard import Controller, Key

        self._kb, self._Key = Controller(), Key
        self.focus = focus
        self.history: list[str] = []  # what we typed, so "scratch that" can remove exactly the last phrase

    def _target(self) -> None:
        if self.focus:
            self.focus.ensure_target()

    def type(self, text: str) -> None:
        self._target()
        self._kb.type(text)
        self.history.append(text)

    def newline(self, n: int = 1) -> None:
        self._target()
        for _ in range(n):
            self._kb.tap(self._Key.enter)
        self.history.append("\n" * n)

    def scratch_last(self) -> bool:
        if not self.history:
            return False
        self._target()
        for _ in range(len(self.history.pop())):
            self._kb.tap(self._Key.backspace)
        return True

    def undo_key(self) -> None:
        self._target()
        with self._kb.pressed(self._Key.ctrl):
            self._kb.tap("z")


# ---------- system tray ----------

def _tray_image(color: str):  # noqa: ANN202 - PIL image
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((20, 6, 44, 40), radius=12, fill=color)      # microphone head
    d.arc((12, 22, 52, 50), start=0, end=180, fill=color, width=5)   # holder
    d.line((32, 50, 32, 58), fill=color, width=5)
    d.line((22, 58, 42, 58), fill=color, width=5)
    return img


class Tray:
    """System-tray icon: the app lives here; the status window is optional."""

    def __init__(self, app) -> None:  # noqa: ANN001 - voicedoc.app.App
        import pystray

        self.app = app
        self._icons = {True: _tray_image("#1e8e3e"), False: _tray_image("#8a8a8a")}
        menu = pystray.Menu(
            pystray.MenuItem(lambda _: "Pause listening" if app.state.listening.is_set() else "Start listening",
                             lambda: app.toggle_listening(), default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Write to today's note", lambda: app.set_output("file"),
                             checked=lambda _: app.s.output == "file", radio=True),
            pystray.MenuItem("Type at cursor (any app)", lambda: app.set_output("cursor"),
                             checked=lambda _: app.s.output == "cursor", radio=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Microphone", pystray.Menu(lambda: self._mic_items())),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Show status window", lambda: app.show_status()),
            pystray.MenuItem("History…", lambda: app.show_history()),
            pystray.MenuItem("Help…", lambda: app.show_help()),
            pystray.MenuItem("Open notes", lambda: app.open_notes()),
            pystray.MenuItem("Settings…", lambda: app.open_settings()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", lambda: app.quit()),
        )
        self.icon = pystray.Icon("voicedoc", self._icons[app.state.listening.is_set()], "voicedoc", menu)
        self._stop = threading.Event()

    def _mic_items(self):  # noqa: ANN202 - generator of pystray.MenuItem
        import pystray

        from .audio import list_input_devices

        app = self.app

        def item(label: str, value: str):  # noqa: ANN202
            return pystray.MenuItem(label, lambda: app.set_mic(value),
                                    checked=lambda _: (app.s.mic or "communications") == value, radio=True)

        yield item("Follow Windows communications device (headsets)", "communications")
        yield item("Follow Windows default device", "default")
        yield pystray.Menu.SEPARATOR
        try:
            names = list_input_devices()
        except Exception:  # noqa: BLE001 - audio library busy; show the fixed choices only
            names = []
        for n in names:
            yield item(n, n)

    @property
    def title(self) -> str:
        return self.icon.title

    @title.setter
    def title(self, value: str) -> None:
        self.icon.title = value
        self.icon.icon = self._icons[self.app.state.listening.is_set()]

    def start(self) -> None:
        self.icon.run_detached()

    def stop(self) -> None:
        self.icon.stop()


# ---------- help window ----------

HELP_TEXT = """VOICEDOC — speak Tamil / Tanglish, get English text, live.

GETTING STARTED
  VoiceDoc waits in the system tray (microphone icon near the clock; if hidden, click the ^ arrow and
  drag it onto the taskbar). Grey = paused, green = listening.
  1. Click into the app you want to type in (Notepad++, VS Code, Word…).
  2. LEFT-CLICK the mic icon (or press {hotkey}) — beep, icon turns green: speak.
     Each phrase appears in English about 1–3 s after you pause, where your cursor is.
  3. Click the mic icon again (or {hotkey}) to stop.
  Right-click the icon for everything else (mode, history, help, settings, quit).

TWO WAYS TO GET YOUR TEXT  (right-click the tray icon to switch)
  • Write to today's note — everything goes into {note}
      Open it in VS Code and press Ctrl+K V for a live preview (Notepad++ also refreshes; classic Notepad does not).
      Voice commands can organise the note (see below).
  • Type at cursor (any app) — click into Notepad++, VS Code, Word, a browser… and speak.
      The English text is typed where your cursor is. Your clipboard is never touched.

VOICE COMMANDS — always start with the word "command" (or கமாண்ட்)
  In today's note:
    command new section Meeting notes         → new heading; next dictation goes there
    command budget section-ku po               → continue writing under "Budget"
    command idha action items-ku move pannu    → move the last paragraph to "Action items"
    command last paragraph-a bullet points-a maathu → turn it into a bullet list
    command rename Budjet to Budget
    command andha section-a delete pannu       → asks you to confirm: say "yes" / "ஆமா" or "no" / "வேண்டாம்"
    command scratch that   /   command undo    → instant, removes the last change
  While typing at the cursor:
    command new line · command new paragraph · command bullet · command heading
    command scratch that (deletes what was just typed) · command undo (Ctrl+Z)

WHEN IT ASKS YOU SOMETHING
  If a command is unclear it asks a short question (on screen, and aloud).
  Your next sentence is taken as the answer. Say "cancel" / "வேண்டாம்" to drop it.

YOUR DATA
  • Original Tamil of every phrase: {transcript}
  • Audio of every phrase: {audio}  (play it from History…)
  • History…  (tray) shows recent phrases with Tamil + English, Copy and Play buttons.
  • If you edit the note by hand while it runs, your edits are kept. If they can't be merged,
    listening pauses and the status window tells you why — nothing is overwritten.

SETTINGS  (tray → Settings… opens voicedoc.json; restart after editing)
  hotkey / hotkey_mode ("toggle" or "hold")   voice (e.g. "Zira", or any installed Windows voice)
  replacements: fix recurring words, e.g. {{"diarrhegation": "diarization"}}
  min_silence_ms: pause length that ends a phrase (default 400)   max_phrase_s: longest phrase (12)
  output: "file" or "cursor" (start-up mode)   speak_questions / sounds / save_audio: true or false

BETTER VOICE FOR SPOKEN QUESTIONS
  Install NaturalVoiceSAPIAdapter (github.com/gexgd0419/NaturalVoiceSAPIAdapter) with its online
  voices unticked; its natural Narrator voices are picked automatically on next start.

Everything runs on this laptop. Nothing is sent to the internet.
"""


def open_help_window(root, s, note_path) -> None:  # noqa: ANN001 - tk root, Settings, Path
    import tkinter as tk

    win = tk.Toplevel(root)
    win.title("voicedoc — help")
    win.geometry("820x640")
    txt = tk.Text(win, wrap="word", font=("Consolas", 10), padx=12, pady=10)
    sb = tk.Scrollbar(win, command=txt.yview)
    txt.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    txt.pack(side="left", fill="both", expand=True)
    txt.insert("1.0", HELP_TEXT.format(
        hotkey=s.hotkey.title(), note=note_path,
        transcript=note_path.with_name(note_path.stem + ".transcript.md").name,
        audio=note_path.with_name(note_path.stem + ".audio").name + "\\"))
    txt.configure(state="disabled")
    win.lift()


# ---------- history window ----------

def open_history_window(root, history: list) -> None:  # noqa: ANN001 - tk root, list[HistoryEntry]
    """Recent phrases with the original Tamil, the English written, copy buttons and audio playback."""
    import tkinter as tk
    import winsound

    win = tk.Toplevel(root)
    win.title("voicedoc — history")
    win.geometry("760x460")
    win.attributes("-topmost", True)
    lb = tk.Listbox(win, font=("Segoe UI", 10), activestyle="none")
    lb.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
    side = tk.Frame(win)
    side.pack(side="right", fill="y", padx=8, pady=8)
    detail = tk.Text(side, width=44, height=16, wrap="word", font=("Segoe UI", 10))
    detail.pack()
    entries: list = []

    def refresh() -> None:
        entries[:] = list(reversed(history))
        lb.delete(0, "end")
        for e in entries:
            lb.insert("end", f"{e.time}  {(e.written or '[command] ' + e.spoken)[:90]}")

    def selected():  # noqa: ANN202
        sel = lb.curselection()
        return entries[sel[0]] if sel else None

    def on_select(_event=None) -> None:  # noqa: ANN001
        e = selected()
        detail.delete("1.0", "end")
        if e:
            detail.insert("end", f"Heard ({e.time}):\n{e.spoken}\n\nWritten:\n{e.written or '(command, nothing written)'}")

    def copy(which: str) -> None:
        e = selected()
        if e:
            win.clipboard_clear()
            win.clipboard_append((e.written if which == "en" else e.spoken) or "")

    def play() -> None:
        e = selected()
        if e and e.audio and e.audio.exists():
            winsound.PlaySound(str(e.audio), winsound.SND_FILENAME | winsound.SND_ASYNC)

    lb.bind("<<ListboxSelect>>", on_select)
    for label, cmd in (("Copy English", lambda: copy("en")), ("Copy Tamil", lambda: copy("ta")),
                       ("Play audio", play), ("Refresh", refresh)):
        tk.Button(side, text=label, command=cmd, width=18).pack(pady=2)
    refresh()


# ---------- status overlay ----------

class Overlay:
    """Small always-on-top window. Must be created and run on the main thread (tkinter requirement)."""

    COLORS = {"listening": "#1e8e3e", "paused": "#6b6b6b", "transcribing": "#b06000",
              "question": "#1a55c4", "error": "#c5221f", "loading": "#6b6b6b"}

    def __init__(self, on_close: Callable[[], None]) -> None:
        import tkinter as tk

        self._tk = tk
        self.root = tk.Tk()
        self.root.title("voicedoc")
        self.root.attributes("-topmost", True)
        self.root.geometry("+20+20")
        self.root.resizable(False, False)
        self.state_lbl = tk.Label(self.root, text="loading…", fg="white", bg=self.COLORS["loading"],
                                  font=("Segoe UI", 11, "bold"), width=34, anchor="w", padx=8, pady=4)
        self.state_lbl.pack(fill="x")
        self.text_lbl = tk.Label(self.root, text="", font=("Segoe UI", 10), width=48, anchor="w",
                                 justify="left", wraplength=420, padx=8, pady=4)
        self.text_lbl.pack(fill="x")
        self._q: queue.Queue[tuple[str, str]] = queue.Queue()
        self.root.protocol("WM_DELETE_WINDOW", on_close)
        self.root.after(100, self._poll)

    def show(self, state: str, detail: str = "") -> None:
        """Thread-safe: queues an update for the Tk thread."""
        self._q.put((state, detail))

    def _poll(self) -> None:
        try:
            while True:
                state, detail = self._q.get_nowait()
                self.state_lbl.config(text=state if state not in self.COLORS else f"● {state}",
                                      bg=self.COLORS.get(state, "#333333"))
                self.text_lbl.config(text=detail[:300])
        except queue.Empty:
            pass
        self.root.after(100, self._poll)

    def run(self) -> None:
        self.root.mainloop()

    def close(self) -> None:
        self.root.after(0, self.root.destroy)
