"""Speech recognition with Indic-Transcribe-flex (default model), mixed-script Tamil output."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

DEFAULT_MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "indic-transcribe-flex"
SAMPLE_RATE = 16_000


class Transcriber:
    def __init__(self, model_dir: Path = DEFAULT_MODEL_DIR, lang: str = "ta", mode: str = "mixed",
                 device: str | None = None) -> None:
        if not (model_dir / "model.safetensors").is_file():
            raise FileNotFoundError(
                f"{model_dir / 'model.safetensors'} not found. Download it with:\n"
                f"  hf download bodhan-ai/indic-transcribe-flex --local-dir {model_dir} --exclude \"nemo/*\"")
        import torch

        # The model's loader ships as flat modules inside the downloaded repository.
        sys.path.insert(0, str(model_dir))
        from indic_transcribe import IndicTranscribe  # type: ignore[import-not-found]

        self.lang, self.mode = lang, mode
        self._torch = torch
        self.asr = IndicTranscribe.from_pretrained(str(model_dir), device=device)
        self.device = self.asr.device

    def __call__(self, audio: np.ndarray) -> tuple[str, float]:
        """Returns (text, seconds spent decoding)."""
        t0 = time.perf_counter()
        text = self.asr.transcribe(audio.astype(np.float32, copy=False), lang=self.lang, mode=self.mode)
        return text.strip(), time.perf_counter() - t0

    def gpu_memory_mb(self) -> tuple[float, float]:
        """(currently allocated, peak allocated) by this process's PyTorch, in MiB."""
        if not str(self.device).startswith("cuda"):
            return 0.0, 0.0
        c = self._torch.cuda
        return c.memory_allocated() / 2**20, c.max_memory_allocated() / 2**20
