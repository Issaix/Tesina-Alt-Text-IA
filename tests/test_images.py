from io import BytesIO

import pytest
from PIL import Image

from app.images import decode_image


@pytest.mark.parametrize(
    "mode,fmt,filename", [("L", "PNG", "gray.png"), ("CMYK", "JPEG", "print.jpg")]
)
def test_opaque_images_are_converted_to_rgb(mode, fmt, filename):
    buffer = BytesIO()
    with Image.new(mode, (10, 20)) as source:
        source.save(buffer, format=fmt)
    with decode_image(buffer.getvalue(), filename) as decoded:
        assert decoded.mode == "RGB"
        assert decoded.size == (10, 20)
        assert decoded.getpixel((0, 0)) is not None


def test_palette_transparency_is_composited_on_white():
    buffer = BytesIO()
    with Image.new("P", (2, 1)) as source:
        source.putpalette([0, 0, 0, 255, 0, 0] + [0] * 762)
        source.putdata([0, 1])
        source.save(buffer, format="PNG", transparency=0)
    with decode_image(buffer.getvalue(), "palette.png") as decoded:
        assert decoded.getpixel((0, 0)) == (255, 255, 255)
        assert decoded.getpixel((1, 0)) == (255, 0, 0)
