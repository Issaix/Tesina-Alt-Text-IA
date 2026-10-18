import hashlib
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
    # Esta prueba usa cuatro casos propios, independientemente del conjunto educativo.
    directory = tmp_path / "examples" / "educational"
    directory.mkdir(parents=True)
    manifest = [{"file": f"image-{index}.png"} for index in range(4)]
    for item in manifest:
        (directory / item["file"]).write_bytes(b"example")
    (directory / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(evaluate, "ROOT", tmp_path)
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


@pytest.mark.parametrize(
    "values,critical,decision",
    [
        ([2, 2, 2, 2, 2], "", "apta"),
        ([2, 1, 2, 2, 1], "", "apta"),
        ([2, 2, 1, 2, 2], "", "requiere_revision"),
        ([2, 0, 2, 2, 2], "", "requiere_revision"),
        ([1, 0, 0, 2, 2], "", "no_apta"),
        ([2, 2, 2, 2, 2], "Cifra inventada", "no_apta"),
    ],
)
def test_rubric_decisions(values, critical, decision):
    scores = dict(zip(evaluate.CRITERIA, values, strict=True))
    assert evaluate.quality_result(scores, critical) == decision


@pytest.mark.parametrize("value", [True, -1, 3, 1.5, "2", None])
def test_invalid_scores_are_rejected(value):
    scores = dict.fromkeys(evaluate.CRITERIA, 2)
    scores["essential"] = value
    with pytest.raises(ValueError):
        evaluate.quality_result(scores, "")


def review_fixture():
    return {
        "file": "image.png",
        "sha256": "image-hash",
        "description_sha256": evaluate.description_hash("Una planta."),
        "scores": dict.fromkeys(evaluate.CRITERIA, 2),
        "critical_error": "",
        "reviewer": "Revisor de prueba",
        "reviewed_at": "2026-10-17",
        "notes": "Conserva los contenidos requeridos en esta prueba.",
        "correction": "Ninguna.",
    }


def result_fixture():
    return {
        "file": "image.png",
        "sha256": "image-hash",
        "passed": True,
        "response": {"description": "Una planta."},
    }


@pytest.mark.parametrize("field", ["sha256", "description_sha256"])
def test_stale_reviews_are_rejected(field):
    review = review_fixture()
    review[field] = "different"
    with pytest.raises(ValueError, match="no corresponde"):
        evaluate.apply_reviews([result_fixture()], [review])


def test_http_success_is_not_quality_approval():
    results = [result_fixture()]
    evaluate.apply_reviews(results, [])
    assert results[0]["quality"]["status"] == "pending"
    summary = evaluate.summarize(results)
    assert summary["http_passed"] == 1
    assert summary["reviewed"] == 0
    assert summary["decisions"]["apta"] == 0
    assert summary["mean_score"] is None


def test_saved_run_can_be_reviewed_without_http(tmp_path, monkeypatch):
    source = tmp_path / "raw.json"
    source.write_text(json.dumps({"timestamp_utc": "original", "results": [result_fixture()]}))
    reviews = tmp_path / "reviews.json"
    reviews.write_text(json.dumps([review_fixture()]))
    monkeypatch.setattr(evaluate.httpx, "Client", lambda **kwargs: pytest.fail("Unexpected HTTP"))
    output = tmp_path / "reviewed.json"
    assert (
        evaluate.main(["--input", str(source), "--reviews", str(reviews), "--output", str(output)])
        == 0
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["timestamp_utc"] == "original"
    assert report["summary"]["decisions"]["apta"] == 1
    assert output.with_suffix(".md").is_file()
    assert "quality" not in json.loads(source.read_text())["results"][0]


def test_datasets_respect_project_scope():
    directory = evaluate.ROOT / "examples" / "educational"
    main = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    assert len(main) == 20
    assert sum(item["type"] == "fotografía" for item in main) == 10
    assert sum(item["type"] == "ilustración" for item in main) == 10
    assert {item["scope"] for item in main} == {"principal_linea_a"}
    assert len({item["file"] for item in main}) == len({item["sha256"] for item in main}) == 20
    images = {p.name for p in directory.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}}
    assert images == {item["file"] for item in main}
    for item in main:
        assert hashlib.sha256((directory / item["file"]).read_bytes()).hexdigest() == item["sha256"]
        assert all(
            item.get(key)
            for key in ("reference", "context", "required_content", "source_url", "license")
        )


def test_diagrams_are_rejected_before_http(tmp_path, monkeypatch):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps([{"file": "diagram.png", "type": "diagrama"}]))
    monkeypatch.setattr(evaluate.httpx, "Client", lambda **kwargs: pytest.fail("Unexpected HTTP"))
    with pytest.raises(SystemExit) as exc:
        evaluate.main(["--manifest", str(manifest)])
    assert exc.value.code == 2


def test_mixed_scopes_are_rejected_before_http(tmp_path, monkeypatch):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            [
                {"file": "a.png", "scope": "principal_linea_a"},
                {"file": "b.png", "scope": "exploratorio_fuera_de_alcance"},
            ]
        )
    )
    monkeypatch.setattr(evaluate.httpx, "Client", lambda **kwargs: pytest.fail("Unexpected HTTP"))
    with pytest.raises(SystemExit) as exc:
        evaluate.main(["--manifest", str(manifest)])
    assert exc.value.code == 2


def test_failed_request_cannot_receive_quality_score():
    result = result_fixture()
    result["passed"] = False
    with pytest.raises(ValueError, match="petición fallida"):
        evaluate.apply_reviews([result], [review_fixture()])


def test_duplicate_and_unknown_reviews_are_rejected():
    review = review_fixture()
    with pytest.raises(ValueError, match="duplicada"):
        evaluate.apply_reviews([result_fixture()], [review, review])
    review["file"] = "other.png"
    with pytest.raises(ValueError, match="ajenos"):
        evaluate.apply_reviews([result_fixture()], [review])


def test_summary_keeps_pending_and_http_failure_separate():
    good, pending, failed = result_fixture(), result_fixture(), result_fixture()
    pending["file"], failed["file"] = "pending.png", "failed.png"
    failed["passed"] = False
    results = [good, pending, failed]
    evaluate.apply_reviews(results, [review_fixture()])
    summary = evaluate.summarize(results)
    assert summary["images"] == 3
    assert summary["http_passed"] == 2
    assert summary["reviewed"] == summary["pending"] == summary["not_evaluated"] == 1
    assert summary["mean_score"] == 10
