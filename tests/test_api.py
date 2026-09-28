from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from threading import Event

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app import images
from app.captioning import ModelBusyError, get_captioning_service
from app.main import create_app


def image_bytes(fmt="PNG", mode="RGB", size=(20, 10), **kwargs):
    buffer = BytesIO()
    with Image.new(mode, size) as image:
        image.save(buffer, format=fmt, **kwargs)
    return buffer.getvalue()


class FakeCaptioner:
    def __init__(self):
        self.calls = []
        self.error = None
        self.output = "Un triángulo azul."

    def describe(self, image):
        self.calls.append((image.mode, image.size, image.getpixel((0, 0))))
        if self.error:
            raise self.error
        return self.output


@pytest.fixture
def api():
    app = create_app()
    fake = FakeCaptioner()
    app.dependency_overrides[get_captioning_service] = lambda: fake
    try:
        with TestClient(app) as client:
            yield client, fake
    finally:
        app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "name,fmt,mime",
    [
        ("a.jpg", "JPEG", "image/jpeg"),
        ("a.JPEG", "JPEG", "image/jpeg"),
        ("a.png", "PNG", "image/png"),
        ("a.png", "PNG", "application/octet-stream"),
    ],
)
def test_valid_image_returns_exact_contract(api, name, fmt, mime):
    client, fake = api
    response = client.post("/describe", files={"image": (name, image_bytes(fmt), mime)})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"description": "Un triángulo azul."}
    assert len(fake.calls) == 1
    assert fake.calls[0][:2] == ("RGB", (20, 10))


@pytest.mark.parametrize(
    "name,data,mime,status",
    [
        ("empty.png", b"", "image/png", 400),
        ("fake.png", b"not an image", "image/png", 400),
        ("a.gif", image_bytes("GIF"), "image/gif", 415),
        ("a.png", image_bytes("GIF"), "image/png", 415),
        ("a.jpg", image_bytes("PNG"), "image/jpeg", 415),
        ("a.png", image_bytes(), "text/plain", 415),
        ("a", image_bytes(), "image/png", 415),
        ("broken.png", image_bytes()[:-12], "image/png", 400),
        ("broken.jpg", image_bytes("JPEG")[:-30], "image/jpeg", 400),
    ],
)
def test_invalid_input_never_calls_model(api, name, data, mime, status):
    client, fake = api
    response = client.post("/describe", files={"image": (name, data, mime)})
    assert response.status_code == status, response.text
    assert isinstance(response.json()["detail"], str)
    assert not fake.calls


def test_missing_image(api):
    client, fake = api
    assert client.post("/describe").status_code == 422
    assert client.post("/describe", json={"image": "base64"}).status_code == 422
    assert not fake.calls


@pytest.mark.parametrize("limit", ["bytes", "pixels"])
def test_limits(api, monkeypatch, limit):
    client, fake = api
    monkeypatch.setattr(images, "MAX_IMAGE_BYTES" if limit == "bytes" else "MAX_IMAGE_PIXELS", 100)
    response = client.post(
        "/describe", files={"image": ("a.png", image_bytes(size=(100, 100)), "image/png")}
    )
    assert response.status_code == 413
    assert not fake.calls


def test_animated_png_is_rejected(api):
    client, fake = api
    buffer = BytesIO()
    with Image.new("RGB", (10, 10), "red") as first, Image.new("RGB", (10, 10), "blue") as second:
        first.save(buffer, format="PNG", save_all=True, append_images=[second], duration=100)
    assert (
        client.post(
            "/describe", files={"image": ("animated.png", buffer.getvalue(), "image/png")}
        ).status_code
        == 415
    )
    assert not fake.calls


def test_transparency_has_white_background(api):
    client, fake = api
    response = client.post(
        "/describe", files={"image": ("alpha.png", image_bytes(mode="RGBA"), "image/png")}
    )
    assert response.status_code == 200
    assert fake.calls[0][2] == (255, 255, 255)


def test_exif_orientation(api):
    client, fake = api
    exif = Image.Exif()
    exif[274] = 6
    response = client.post(
        "/describe", files={"image": ("rotated.jpg", image_bytes("JPEG", exif=exif), "image/jpeg")}
    )
    assert response.status_code == 200
    assert fake.calls[0][1] == (10, 20)


@pytest.mark.parametrize("error", [OSError("sensitive local path"), ModelBusyError("busy")])
def test_model_errors_are_controlled(api, error):
    client, fake = api
    fake.error = error
    response = client.post("/describe", files={"image": ("a.png", image_bytes(), "image/png")})
    assert response.status_code == 503
    assert "sensitive" not in response.text
    if isinstance(error, ModelBusyError):
        assert response.headers["retry-after"] == "5"


def test_empty_model_output_is_not_a_success(api):
    client, fake = api
    fake.output = " "
    assert (
        client.post("/describe", files={"image": ("a.png", image_bytes(), "image/png")}).status_code
        == 503
    )


@pytest.mark.parametrize("stage", ["decode", "inference"])
def test_health_remains_responsive_during_processing(api, monkeypatch, stage):
    client, fake = api
    started, release = Event(), Event()

    decode_image = images.decode_image

    def slow(*args):
        started.set()
        assert release.wait(10)
        if stage == "decode":
            return decode_image(*args)
        return "Una planta."

    if stage == "decode":
        monkeypatch.setattr(images, "decode_image", slow)
    else:
        monkeypatch.setattr(fake, "describe", slow)
    with ThreadPoolExecutor() as pool:
        future = pool.submit(
            client.post, "/describe", files={"image": ("a.png", image_bytes(), "image/png")}
        )
        try:
            assert started.wait(5)
            assert client.get("/health").json() == {
                "status": "ok",
                "service": "alt-text",
                "version": "0.1.0",
            }
        finally:
            release.set()
        assert future.result().status_code == 200


def test_openapi_contract(api):
    client, _ = api
    schema = client.get("/openapi.json").json()
    operation = schema["paths"]["/describe"]["post"]
    assert "multipart/form-data" in operation["requestBody"]["content"]
    assert operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"].endswith(
        "/DescriptionResponse"
    )
    assert set(operation["responses"]) >= {"200", "400", "413", "415", "422", "503"}
