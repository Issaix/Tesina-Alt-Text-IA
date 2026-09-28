"""Descarga los pesos y realiza una inferencia; no inicia la API."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

from app.captioning import CaptioningService
from app.images import MAX_IMAGE_BYTES, decode_image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--image", type=Path, help="Imagen local opcional para la primera inferencia"
    )
    args = parser.parse_args()
    if args.image:
        with args.image.open("rb") as source:
            image = decode_image(source.read(MAX_IMAGE_BYTES + 1), args.image.name)
    else:
        image = Image.new("RGB", (640, 480), "white")
        draw = ImageDraw.Draw(image)
        draw.rectangle((160, 100, 480, 380), fill="blue")
    try:
        print(json.dumps({"description": CaptioningService().describe(image)}, ensure_ascii=False))
    finally:
        image.close()


if __name__ == "__main__":
    main()
