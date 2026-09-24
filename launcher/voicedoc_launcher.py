"""VoiceDoc.exe: starts the tray app from this project's virtual environment, without a console window.

Built with scripts/build_app.ps1 (PyInstaller). The exe must sit in the project root, next to .venv/ and voicedoc/,
so the 5 GB of models and the CUDA PyTorch install are used in place instead of being copied into the exe.
"""
import ctypes
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent
if not (ROOT / "voicedoc").is_dir():  # running from launcher/ during development
    ROOT = ROOT.parent
PYTHONW = ROOT / ".venv" / "Scripts" / "pythonw.exe"


def message(text: str, error: bool = False) -> None:
    ctypes.windll.user32.MessageBoxW(None, text, "VoiceDoc", 0x10 if error else 0x40)


def main() -> None:
    if not PYTHONW.exists():
        message(f"Cannot find {PYTHONW}.\nVoiceDoc.exe must stay in the VoiceRecognition project folder.", error=True)
        return
    subprocess.Popen([str(PYTHONW), "-m", "voicedoc", *sys.argv[1:]], cwd=str(ROOT),
                     creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
                     close_fds=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})


if __name__ == "__main__":
    main()
