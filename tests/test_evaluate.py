import json

import httpx
import pytest

from scripts import evaluate


@pytest.mark.parametrize(
    "status,body,passed",
    [
        (200, {"description": "Una planta."}, True),
        (200, {"description": " "}, False),
        (200, {"description": 123}, False),
        (200, {"description": "Una planta.", "extra": True}, False),
        (503, {"detail": "Modelo ocupado."}, False),
    ],
)
def test_response_contract(tmp_path, status, body, passed):
    path = tmp_path / "image.png"
    path.write_bytes(b"example")
    transport = httpx.MockTransport(lambda request: httpx.Response(status, json=body))
    with httpx.Client(transport=transport, base_url="http://test") as client:
        result = evaluate.evaluate_image(client, path, {"file": path.name})
    assert result["passed"] is passed
    assert result["response"] == body
    assert result["status_code"] == status


def test_failed_requests_do_not_lose_the_report(tmp_path, monkeypatch):
    calls = []

    def handle(request):
        calls.append(request)
        if len(calls) == 1:
            raise httpx.ReadTimeout("Tiempo de espera agotado", request=request)
        if len(calls) == 2:
            return httpx.Response(502, text="<html>Error del servidor</html>")
        return httpx.Response(200, json={"description": "Una imagen educativa."})

    client_type = httpx.Client
    monkeypatch.setattr(
        evaluate.httpx,
        "Client",
        lambda **kwargs: client_type(transport=httpx.MockTransport(handle), **kwargs),
    )
    output = tmp_path / "results.json"
    assert evaluate.main(["--base-url", "http://test", "--output", str(output)]) == 1
    results = json.loads(output.read_text(encoding="utf-8"))["results"]
    assert len(results) == 4
    assert [item["passed"] for item in results] == [False, False, True, True]
    assert results[0]["status_code"] is None
    assert results[1]["status_code"] == 502
    assert "JSON" in results[1]["error"]


def test_missing_image_is_recorded(tmp_path):
    with httpx.Client(base_url="http://test") as client:
        result = evaluate.evaluate_image(client, tmp_path / "missing.png", {"file": "missing.png"})
    assert not result["passed"]
    assert result["sha256"] is None
    assert result["status_code"] is None
