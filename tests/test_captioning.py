import pytest
from PIL import Image

from app.captioning import CaptioningService, ModelBusyError


def test_busy_model_rejects_a_second_request():
    service = CaptioningService()
    with Image.new("RGB", (8, 8)) as image, service._lock, pytest.raises(ModelBusyError):
        service.describe(image)


def test_failed_load_releases_lock_for_retry(monkeypatch):
    service = CaptioningService()
    attempts = []

    def fail():
        attempts.append(True)
        raise OSError("Model unavailable")

    monkeypatch.setattr(service, "_load", fail)
    with Image.new("RGB", (8, 8)) as image:
        for _ in range(2):
            with pytest.raises(OSError):
                service.describe(image)
    assert len(attempts) == 2
