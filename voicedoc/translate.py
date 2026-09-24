"""Tamil -> English translation of each dictated phrase with IndicTrans2 (distilled 200M)."""
from __future__ import annotations

import time

MODEL_NAME = "ai4bharat/indictrans2-indic-en-dist-200M"
SRC_LANG, TGT_LANG = "tam_Taml", "eng_Latn"


class Translator:
    def __init__(self, device: str | None = None, num_beams: int = 5, model_name: str = MODEL_NAME) -> None:
        import torch
        from IndicTransToolkit.processor import IndicProcessor
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self._torch = torch
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        dtype = torch.float16 if self.device.startswith("cuda") else torch.float32
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name, trust_remote_code=True, torch_dtype=dtype).to(self.device).eval()
        self.ip = IndicProcessor(inference=True)
        self.num_beams = num_beams

    def __call__(self, text: str) -> tuple[str, float]:
        """Returns (English text, seconds spent)."""
        t0 = time.perf_counter()
        batch = self.ip.preprocess_batch([text], src_lang=SRC_LANG, tgt_lang=TGT_LANG)
        inputs = self.tokenizer(batch, truncation=True, padding="longest", return_tensors="pt",
                                return_attention_mask=True).to(self.device)
        with self._torch.inference_mode():
            # use_cache=False: the model's remote code (modeling_indictrans.py:1360) crashes on the
            # cache objects that transformers 4.5x passes ('NoneType' object has no attribute 'shape').
            # Loop guard: a native-script phrase once decoded "more to be done," ~40 times (bench, clip jOT8eHwlXHQ).
            max_new = min(256, int(inputs["input_ids"].shape[1] * 2) + 16)
            out = self.model.generate(**inputs, use_cache=False, min_length=0, max_new_tokens=max_new,
                                      num_beams=self.num_beams, num_return_sequences=1,
                                      no_repeat_ngram_size=4, repetition_penalty=1.1)
        decoded = self.tokenizer.batch_decode(out, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        english = self.ip.postprocess_batch(decoded, lang=TGT_LANG)[0].strip()
        return english, time.perf_counter() - t0
