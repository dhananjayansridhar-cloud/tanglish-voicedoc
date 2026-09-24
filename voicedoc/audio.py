"""Microphone capture and pause-based segmentation with Silero VAD (runs on CPU)."""
from __future__ import annotations

import queue
import threading
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

SAMPLE_RATE = 16_000
CHUNK = 512  # Silero VAD's required window at 16 kHz (32 ms)
CHUNK_MS = CHUNK * 1000 // SAMPLE_RATE


@dataclass
class VadConfig:
    start_threshold: float = 0.5   # speech probability that opens a phrase
    end_threshold: float = 0.35    # below this counts as silence
    min_silence_ms: int = 400      # pause that closes a phrase
    min_speech_ms: int = 250       # shorter bursts (clicks, coughs) are dropped
    max_phrase_s: float = 12.0     # forces an update during non-stop speech; bench: 25 s cuts made text appear only every 25 s
    pre_roll_ms: int = 300         # audio kept from before speech was detected


class PhraseSegmenter:
    """Feeds 512-sample chunks through Silero VAD and emits one array per spoken phrase."""

    def __init__(self, cfg: VadConfig, on_phrase: Callable[[np.ndarray], None],
                 on_speech_start: Callable[[], None] | None = None,
                 gate: Callable[[], bool] | None = None) -> None:
        self.gate = gate  # False while paused or while the assistant is speaking: audio is discarded
        import torch
        from silero_vad import load_silero_vad

        torch.set_num_threads(1)
        self._torch = torch
        self.model = load_silero_vad()
        self.cfg = cfg
        self.on_phrase, self.on_speech_start = on_phrase, on_speech_start
        self._pre = deque(maxlen=max(1, cfg.pre_roll_ms // CHUNK_MS))
        self._buf: list[np.ndarray] = []
        self._silence_ms = 0
        self._speech_ms = 0

    def feed(self, chunk: np.ndarray) -> None:
        if self.gate is not None and not self.gate():
            if self._buf:  # paused mid-phrase: drop it rather than emit half a sentence
                self._buf, self._silence_ms, self._speech_ms = [], 0, 0
                self.model.reset_states()
            self._pre.clear()
            return
        with self._torch.inference_mode():
            p = float(self.model(self._torch.from_numpy(chunk), SAMPLE_RATE).item())
        if not self._buf:
            if p >= self.cfg.start_threshold:
                self._buf = list(self._pre) + [chunk]
                self._speech_ms, self._silence_ms = CHUNK_MS, 0
                if self.on_speech_start:
                    self.on_speech_start()
            else:
                self._pre.append(chunk)
            return
        self._buf.append(chunk)
        if p < self.cfg.end_threshold:
            self._silence_ms += CHUNK_MS
        else:
            self._silence_ms = 0
            self._speech_ms += CHUNK_MS
        total_s = len(self._buf) * CHUNK / SAMPLE_RATE
        if self._silence_ms >= self.cfg.min_silence_ms or total_s >= self.cfg.max_phrase_s:
            self._close()

    def _close(self) -> None:
        audio = np.concatenate(self._buf)
        keep = self._speech_ms >= self.cfg.min_speech_ms
        self._buf, self._silence_ms, self._speech_ms = [], 0, 0
        self._pre.clear()
        self.model.reset_states()
        if keep:
            self.on_phrase(audio)


def windows_default_capture(role: str) -> tuple[str, str] | None:
    """(endpoint id, friendly name) of the Windows default recording device for role 'default' or 'communications'."""
    import comtypes
    from pycaw.api.mmdeviceapi import IMMDeviceEnumerator
    from pycaw.constants import CLSID_MMDeviceEnumerator, EDataFlow, ERole
    from pycaw.pycaw import AudioUtilities

    comtypes.CoInitialize()
    try:
        en = comtypes.CoCreateInstance(CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, comtypes.CLSCTX_INPROC_SERVER)
        r = ERole.eCommunications if role == "communications" else ERole.eConsole
        dev = en.GetDefaultAudioEndpoint(EDataFlow.eCapture.value, r.value)
        return dev.GetId(), AudioUtilities.CreateDevice(dev).FriendlyName
    except comtypes.COMError:
        return None  # no recording device at all
    finally:
        comtypes.CoUninitialize()


def list_input_devices() -> list[str]:
    """Friendly names of MME input devices (MME resamples to 16 kHz for us; WASAPI shared mode would not)."""
    import sounddevice as sd

    mme = next(i for i, h in enumerate(sd.query_hostapis()) if h["name"] == "MME")
    return [d["name"] for d in sd.query_devices() if d["hostapi"] == mme and d["max_input_channels"] > 0
            and "Sound Mapper" not in d["name"]]


def _portaudio_index(friendly: str) -> int | None:
    """MME truncates names to 31 chars, so match the Windows friendly name by prefix."""
    import sounddevice as sd

    mme = next(i for i, h in enumerate(sd.query_hostapis()) if h["name"] == "MME")
    for i, d in enumerate(sd.query_devices()):
        if d["hostapi"] == mme and d["max_input_channels"] > 0 and friendly.startswith(d["name"].strip()):
            return i
    return None


class Microphone:
    """Pushes 512-sample float32 chunks into a queue and follows the chosen Windows recording device.

    mic = "communications" (Windows default communications device, what headsets get), "default", or a device-name
    substring. When Windows switches the device (headset connected, unplugged…) the stream is reopened on the new one.
    """

    POLL_S = 2.0

    def __init__(self, mic: str | None = "communications", on_change: Callable[[str], None] | None = None) -> None:
        self.q: queue.Queue[np.ndarray] = queue.Queue()
        self.mic = mic or "communications"
        self.on_change = on_change
        self.overflows = 0
        self.device_name = "?"
        self._stream = None
        self._key: str | None = None
        self._lock = threading.Lock()
        self._stop = threading.Event()

    def _callback(self, indata, frames, time_info, status) -> None:  # noqa: ANN001 - sounddevice signature
        if status.input_overflow:
            self.overflows += 1
        self.q.put(indata[:, 0].copy())

    def _resolve(self) -> tuple[str, str]:
        """(key identifying the target device, its friendly name)."""
        if self.mic in ("communications", "default"):
            found = windows_default_capture(self.mic)
            if found is None:
                raise RuntimeError("Windows reports no recording device. Connect a microphone or headset.")
            return found
        matches = [n for n in list_input_devices() if self.mic.lower() in n.lower()]
        if not matches:
            raise RuntimeError(f"no microphone matching {self.mic!r}; available: {list_input_devices()}")
        return matches[0], matches[0]

    def _open(self) -> None:
        import sounddevice as sd

        key, friendly = self._resolve()
        # PortAudio lists devices once per initialisation; re-initialise so a newly connected headset is visible.
        sd._terminate()
        sd._initialize()
        idx = _portaudio_index(friendly)
        if idx is None:
            raise RuntimeError(f"Windows device {friendly!r} is not visible to the audio library yet")
        self._stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32",
                                      blocksize=CHUNK, device=idx, callback=self._callback)
        self._stream.start()
        self._key, self.device_name = key, friendly
        if self.on_change:
            self.on_change(friendly)

    def _close_stream(self) -> None:
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            finally:
                self._stream = None

    def _watch(self) -> None:
        import time

        while not self._stop.wait(self.POLL_S):
            try:
                key, _ = self._resolve()
                dead = self._stream is None or not self._stream.active
                if key != self._key or dead:
                    with self._lock:
                        self._close_stream()
                        self._open()
            except Exception as exc:  # noqa: BLE001 - device churn is expected; report and retry next poll
                if self.on_change:
                    self.on_change(f"microphone unavailable: {exc}")
                time.sleep(self.POLL_S)

    def switch(self, mic: str) -> None:
        """Change the target ('communications', 'default' or a device name) and reopen immediately."""
        self.mic = mic
        with self._lock:
            self._close_stream()
            self._open()

    def __enter__(self) -> "Microphone":
        with self._lock:
            self._open()
        threading.Thread(target=self._watch, daemon=True).start()
        return self

    def __exit__(self, *exc) -> None:
        self._stop.set()
        with self._lock:
            self._close_stream()


def run_segmenter(mic: Microphone, seg: PhraseSegmenter, stop: threading.Event) -> None:
    while not stop.is_set():
        try:
            chunk = mic.q.get(timeout=0.2)
        except queue.Empty:
            continue
        seg.feed(chunk)
