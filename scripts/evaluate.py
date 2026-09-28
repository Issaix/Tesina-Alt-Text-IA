"""Prueba las imágenes educativas por HTTP y guarda las respuestas del servicio."""

import argparse
import hashlib
import json
import mimetypes
import time
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

from app.captioning import (
    CAPTION_MODEL,
    CAPTION_REVISION,
    TRANSLATION_MODEL,
    TRANSLATION_REVISION,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / ".cache" / "evaluation.json"


def evaluate_image(client: httpx.Client, path: Path, metadata: dict[str, str]) -> dict[str, Any]:
    """Registra también los fallos para no perder los resultados de las otras imágenes."""
    result: dict[str, Any] = {
        **metadata,
        "sha256": None,
        "status_code": None,
        "response": None,
        "passed": False,
    }
    started = time.perf_counter()
    try:
        data = path.read_bytes()
        result["sha256"] = hashlib.sha256(data).hexdigest()
        response = client.post(
            "/describe",
            files={"image": (path.name, data, mimetypes.guess_type(path)[0])},
        )
        result["status_code"] = response.status_code
        try:
            body = response.json()
        except ValueError:
            result["error"] = "El servidor no devolvió una respuesta JSON."
        else:
            result["response"] = body
            result["passed"] = (
                response.status_code == 200
                and isinstance(body, dict)
                and set(body) == {"description"}
                and isinstance(body["description"], str)
                and bool(body["description"].strip())
            )
            if not result["passed"]:
                result["error"] = "La respuesta no cumple el contrato de descripción."
    except (OSError, httpx.HTTPError) as exc:
        result["error"] = f"No se pudo completar la petición: {exc}"
    result["seconds"] = round(time.perf_counter() - started, 3)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    directory = ROOT / "examples" / "educational"
    try:
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"No se pudo leer el manifiesto de imágenes: {exc}\n")
    if not isinstance(manifest, list) or not manifest:
        parser.error("El manifiesto debe contener al menos una imagen.")
    for item in manifest:
        if not isinstance(item, dict) or not isinstance(item.get("file"), str):
            parser.error("Cada entrada del manifiesto debe incluir un nombre de archivo.")
        if not (directory / item["file"]).resolve().is_relative_to(directory.resolve()):
            parser.error("Las imágenes deben estar dentro de examples/educational.")

    results = []
    with httpx.Client(base_url=args.base_url, timeout=600) as client:
        for item in manifest:
            result = evaluate_image(client, directory / item["file"], item)
            results.append(result)
            message = result["response"]["description"] if result["passed"] else result["error"]
            print(f"{item['file']}: {message}", flush=True)
    report = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "caption_model": CAPTION_MODEL,
        "caption_revision": CAPTION_REVISION,
        "translation_model": TRANSLATION_MODEL,
        "translation_revision": TRANSLATION_REVISION,
        "transport": "HTTP multipart/form-data",
        "device": "cpu",
        "results": results,
    }
    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        parser.exit(1, f"No se pudo guardar el informe: {exc}\n")
    passed = sum(item["passed"] for item in results)
    print(f"{passed} de {len(results)} peticiones correctas. Informe: {args.output}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
