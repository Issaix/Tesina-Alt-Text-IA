"""Validación y normalización de imágenes antes de la inferencia."""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
FORMATS = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG"}
MIME_TYPES = {"JPEG": "image/jpeg", "PNG": "image/png"}


class ImageValidationError(ValueError):
    """Indica por qué una imagen no se puede procesar."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def decode_image(data: bytes, filename: str, content_type: str | None = None) -> Image.Image:
    """Valida los bytes y devuelve una imagen RGB que el llamador debe cerrar."""
    if not data:
        raise ImageValidationError(400, "La imagen está vacía.")
    if len(data) > MAX_IMAGE_BYTES:
        raise ImageValidationError(413, "La imagen supera el límite de 10 MiB.")
    expected = FORMATS.get(Path(filename).suffix.lower())
    if expected is None:
        raise ImageValidationError(415, "Solo se aceptan archivos JPG, JPEG y PNG.")
    if content_type not in (MIME_TYPES[expected], "application/octet-stream", None):
        raise ImageValidationError(415, "El tipo de contenido no coincide con la extensión.")
    try:
        with Image.open(BytesIO(data)) as source:
            if source.format != expected:
                raise ImageValidationError(415, "El formato real no coincide con la extensión.")
            if source.width * source.height > MAX_IMAGE_PIXELS:
                raise ImageValidationError(413, "La imagen supera el límite de 20 megapíxeles.")
            if getattr(source, "n_frames", 1) != 1:
                raise ImageValidationError(415, "Solo se aceptan imágenes estáticas.")
            source.verify()
        with Image.open(BytesIO(data)) as source:
            source.load()
            with ImageOps.exif_transpose(source) as oriented:
                # Las imágenes opacas no necesitan las copias RGBA de la composición.
                if "A" not in oriented.getbands() and "transparency" not in oriented.info:
                    return oriented.convert("RGB")
                with (
                    oriented.convert("RGBA") as normalized,
                    Image.new("RGBA", normalized.size, "white") as background,
                    Image.alpha_composite(background, normalized) as composed,
                ):
                    return composed.convert("RGB")
    except ImageValidationError:
        raise
    except Image.DecompressionBombError as exc:
        raise ImageValidationError(413, "La imagen tiene demasiados píxeles.") from exc
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        raise ImageValidationError(
            400, "El archivo no es una imagen válida o está dañado."
        ) from exc
