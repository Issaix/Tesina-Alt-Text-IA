"""Captioning local en CPU, seguido de traducción al español."""

import os
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from transformers import (
        BlipForConditionalGeneration,
        BlipProcessor,
        MarianMTModel,
        MarianTokenizer,
    )

CAPTION_MODEL = "Salesforce/blip-image-captioning-base"
CAPTION_REVISION = "82a37760796d32b1411fe092ab5d4e227313294b"
TRANSLATION_MODEL = "Helsinki-NLP/opus-mt-en-es"
TRANSLATION_REVISION = "5bc4493d463cf000c1f0b50f8d56886a392ed4ab"
DEFAULT_CACHE = Path(__file__).resolve().parents[1] / ".cache" / "models"


class ModelBusyError(RuntimeError):
    """El proceso ya está atendiendo otra imagen."""


@dataclass(frozen=True)
class LoadedModels:
    processor: "BlipProcessor"
    captioner: "BlipForConditionalGeneration"
    tokenizer: "MarianTokenizer"
    translator: "MarianMTModel"


class CaptioningService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._models: LoadedModels | None = None

    def _load(self) -> LoadedModels:
        """Carga ambos modelos bajo el bloqueo de describe; permite reintentar si falla."""
        if self._models is not None:
            return self._models
        # Importación diferida: /health y las validaciones no necesitan pesos.
        from huggingface_hub import snapshot_download
        from transformers import (
            BlipForConditionalGeneration,
            BlipProcessor,
            MarianMTModel,
            MarianTokenizer,
        )

        cache = Path(os.environ.get("MODEL_CACHE_DIR", str(DEFAULT_CACHE))).expanduser()
        offline = os.environ.get("HF_HUB_OFFLINE", "").strip().upper() in {"1", "ON", "YES", "TRUE"}
        common = {"cache_dir": cache, "local_files_only": offline}
        # Descargar solo los archivos de inferencia y cargar desde disco evita
        # conversiones remotas automáticas de Transformers en segundo plano.
        caption_path = snapshot_download(
            CAPTION_MODEL,
            revision=CAPTION_REVISION,
            allow_patterns=["*.json", "*.txt", "pytorch_model.bin"],
            **common,
        )
        translation_path = snapshot_download(
            TRANSLATION_MODEL,
            revision=TRANSLATION_REVISION,
            allow_patterns=["*.json", "*.spm", "pytorch_model.bin"],
            **common,
        )
        processor = BlipProcessor.from_pretrained(
            caption_path,
            use_fast=False,
            local_files_only=True,
        )
        captioner = BlipForConditionalGeneration.from_pretrained(
            caption_path,
            use_safetensors=False,
            local_files_only=True,
        ).eval()
        tokenizer = MarianTokenizer.from_pretrained(
            translation_path,
            local_files_only=True,
        )
        translator = MarianMTModel.from_pretrained(
            translation_path,
            use_safetensors=False,
            local_files_only=True,
        ).eval()
        self._models = LoadedModels(processor, captioner, tokenizer, translator)
        return self._models

    def describe(self, image: Image.Image) -> str:
        """Genera y traduce una descripción sin modificar ni cerrar la imagen recibida."""
        # Un único trabajo por proceso evita inferencias concurrentes costosas.
        if not self._lock.acquire(blocking=False):
            raise ModelBusyError("El modelo está ocupado.")
        try:
            import torch

            models = self._load()
            with torch.inference_mode():
                inputs = models.processor(images=image, return_tensors="pt")
                tokens = models.captioner.generate(
                    **inputs,
                    max_new_tokens=60,
                    do_sample=False,
                    num_beams=3,
                    no_repeat_ngram_size=3,
                )
                english = models.processor.decode(tokens[0], skip_special_tokens=True).strip()
                if not english:
                    raise RuntimeError("El modelo devolvió una descripción vacía.")
                inputs = models.tokenizer(english, return_tensors="pt", truncation=True)
                tokens = models.translator.generate(
                    **inputs,
                    max_new_tokens=100,
                    do_sample=False,
                    num_beams=3,
                    no_repeat_ngram_size=3,
                )
                spanish = models.tokenizer.decode(tokens[0], skip_special_tokens=True).strip()
                if not spanish:
                    raise RuntimeError("La traducción está vacía.")
                return spanish
        finally:
            self._lock.release()


service = CaptioningService()


def get_captioning_service() -> CaptioningService:
    return service
