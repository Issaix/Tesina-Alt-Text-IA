"""Prueba las imágenes educativas por HTTP y guarda las respuestas del servicio."""

import argparse
import hashlib
import json
import mimetypes
import platform
import time
from collections.abc import Sequence
from datetime import UTC, datetime
from importlib.metadata import version
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
DATASET_TYPES = {
    "principal_linea_a": {"fotografía", "ilustración"},
    "complementario_limitaciones": {"diagrama", "gráfica"},
}
CRITERIA = ("identification", "context", "essential", "fidelity", "clarity")
CRITERIA_LABELS = ("Identificación", "Contexto", "Información esencial", "Fidelidad", "Claridad")
STATUS_LABELS = {
    "pending": "Pendiente",
    "not_evaluated": "Sin evaluar (fallo HTTP)",
    "reviewed": "Revisada",
    "apta": "Apta",
    "requiere_revision": "Requiere revisión",
    "no_apta": "No apta",
}


def description_hash(description: str) -> str:
    return hashlib.sha256(description.encode("utf-8")).hexdigest()


def quality_result(scores: dict[str, int], critical_error: str) -> str:
    """Aplica las reglas de la rúbrica, no una similitud literal de textos."""
    if (
        not isinstance(scores, dict)
        or set(scores) != set(CRITERIA)
        or any(type(value) is not int or value not in (0, 1, 2) for value in scores.values())
    ):
        raise ValueError("La revisión debe puntuar los cinco criterios de 0 a 2.")
    total = sum(scores.values())
    if critical_error or total <= 5:
        return "no_apta"
    if (
        total >= 8
        and all(scores[key] == 2 for key in ("identification", "essential", "fidelity"))
        and scores["context"] >= 1
        and scores["clarity"] >= 1
    ):
        return "apta"
    return "requiere_revision"


def apply_reviews(results: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> None:
    """Vincula cada juicio con la imagen y salida exactas que se revisaron."""
    by_file = {}
    if not results or len({item["file"] for item in results}) != len(results):
        raise ValueError("El informe debe contener imágenes únicas y no estar vacío.")
    if len({item.get("scope", "unspecified") for item in results}) > 1:
        raise ValueError("No se pueden mezclar alcances en un informe.")
    for review in reviews:
        name = review["file"]
        if name in by_file:
            raise ValueError(f"Revisión duplicada: {name}")
        by_file[name] = review
    if set(by_file) - {item["file"] for item in results}:
        raise ValueError("Hay revisiones de archivos ajenos a esta ejecución.")
    for item in results:
        item["quality"] = {"status": "pending" if item["passed"] else "not_evaluated"}
        review = by_file.get(item["file"])
        if review is None:
            continue
        if not item["passed"]:
            raise ValueError(f"No se puede puntuar una petición fallida: {item['file']}")
        if review["sha256"] != item["sha256"] or review["description_sha256"] != description_hash(
            item["response"]["description"]
        ):
            raise ValueError(f"La revisión no corresponde a la imagen o salida: {item['file']}")
        for field in ("reviewer", "reviewed_at", "notes", "correction"):
            if not isinstance(review.get(field), str) or not review[field].strip():
                raise ValueError(f"Falta {field} en la revisión de {item['file']}")
        if not isinstance(review["critical_error"], str):
            raise ValueError("critical_error debe ser texto; vacío si no existe.")
        decision = quality_result(review["scores"], review["critical_error"])
        item["quality"] = {
            **review,
            "status": "reviewed",
            "total": sum(review["scores"].values()),
            "decision": decision,
        }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    reviewed = [item["quality"] for item in results if item["quality"]["status"] == "reviewed"]
    return {
        "images": len(results),
        "http_passed": sum(item["passed"] for item in results),
        "reviewed": len(reviewed),
        "pending": sum(item["quality"]["status"] == "pending" for item in results),
        "not_evaluated": sum(not item["passed"] for item in results),
        "decisions": {
            decision: sum(item["decision"] == decision for item in reviewed)
            for decision in ("apta", "requiere_revision", "no_apta")
        },
        "mean_score": round(sum(item["total"] for item in reviewed) / len(reviewed), 2)
        if reviewed
        else None,
        "critical_errors": sum(bool(item["critical_error"]) for item in reviewed),
        "mean_by_criterion": {
            key: round(sum(item["scores"][key] for item in reviewed) / len(reviewed), 2)
            if reviewed
            else None
            for key in CRITERIA
        },
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Evaluación de descripciones educativas",
        "",
        f"Ejecución HTTP: {report['timestamp_utc']}",
        "",
        f"Alcance: {report.get('scope', 'No registrado en el informe original.')}",
        "",
        report.get("evidence_note", ""),
        "",
        "`passed` comprueba el contrato HTTP; no acredita calidad educativa. "
        "Las puntuaciones siguen la rúbrica y son preliminares, pendientes de validación.",
        "",
        "| Tipo | Imágenes | HTTP | Revisadas | Aptas | Revisión | No aptas | Media / 10 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for kind, summary in report["by_type"].items():
        decisions = summary["decisions"]
        lines.append(
            f"| {kind} | {summary['images']} | {summary['http_passed']} | {summary['reviewed']} "
            f"| {decisions['apta']} | {decisions['requiere_revision']} | {decisions['no_apta']} "
            f"| {summary['mean_score'] if summary['mean_score'] is not None else '—'} |"
        )
    lines.extend(
        [
            "",
            f"Revisiones con error crítico: {report['summary']['critical_errors']}.",
            "",
            "| Criterio | Media / 2 |",
            "|---|---:|",
        ]
    )
    for key, label in zip(CRITERIA, CRITERIA_LABELS, strict=True):
        value = report["summary"]["mean_by_criterion"][key]
        lines.append(f"| {label} | {value if value is not None else '—'} |")
    for item in report["results"]:
        quality = item["quality"]
        lines.extend(
            [
                "",
                f"## {item['file']}",
                "",
                f"**Contexto:** {item.get('context', 'Sin contexto registrado.')}",
                "",
                f"**Referencia:** {item.get('reference', 'Sin referencia registrada.')}",
                "",
                f"**Contenido obligatorio:** {item.get('required_content', 'No registrado.')}",
                "",
                "**Salida:** "
                + (item["response"]["description"] if item["passed"] else item["error"]),
                "",
                f"**Revisión:** {STATUS_LABELS[quality['status']]}",
            ]
        )
        if quality["status"] == "reviewed":
            scores = "; ".join(
                f"{label}: {quality['scores'][key]}"
                for key, label in zip(CRITERIA, CRITERIA_LABELS, strict=True)
            )
            lines.extend(
                [
                    f"**Puntuaciones:** {scores}. Total: {quality['total']}/10.",
                    "",
                    f"**Resultado:** {STATUS_LABELS[quality['decision']]}. {quality['notes']}",
                    "",
                    f"**Error crítico:** {quality['critical_error'] or 'Ninguno identificado.'}",
                    "",
                    f"**Corrección:** {quality['correction']}",
                ]
            )
    return "\n".join(lines) + "\n"


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
    parser.add_argument("--input", type=Path, help="Revisar un informe guardado sin repetir HTTP.")
    parser.add_argument("--reviews", type=Path, help="JSON con revisiones y hashes de las salidas.")
    parser.add_argument(
        "--manifest", type=Path, help="Manifiesto principal o complementario, sin mezclar alcances."
    )
    args = parser.parse_args(argv)
    if args.input:
        try:
            report = json.loads(args.input.read_text(encoding="utf-8"))
            return save_report(report, args, parser)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            parser.exit(1, f"No se pudo revisar el informe: {exc}\n")
    manifest_path = args.manifest or ROOT / "examples" / "educational" / "manifest.json"
    directory = manifest_path.resolve().parent
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"No se pudo leer el manifiesto de imágenes: {exc}\n")
    if not isinstance(manifest, list) or not manifest:
        parser.error("El manifiesto debe contener al menos una imagen.")
    for item in manifest:
        if not isinstance(item, dict) or not isinstance(item.get("file"), str):
            parser.error("Cada entrada del manifiesto debe incluir un nombre de archivo.")
        kind, scope = item.get("type"), item.get("scope", "unspecified")
        allowed = DATASET_TYPES.get(scope, {"fotografía", "ilustración"})
        if kind is not None and kind not in allowed:
            parser.error("El tipo de imagen no corresponde al alcance declarado en el manifiesto.")
        if not (directory / item["file"]).resolve().is_relative_to(directory.resolve()):
            parser.error("Las imágenes deben estar dentro de la carpeta del manifiesto.")
    scopes = {item.get("scope", "unspecified") for item in manifest}
    if len(scopes) != 1:
        parser.error("No mezcles alcances distintos en un mismo informe.")

    results = []
    with httpx.Client(base_url=args.base_url, timeout=600) as client:
        for item in manifest:
            result = evaluate_image(client, directory / item["file"], item)
            results.append(result)
            message = result["response"]["description"] if result["passed"] else result["error"]
            print(f"{item['file']}: {message}", flush=True)
    report = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "scope": next(iter(scopes)),
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "base_url": args.base_url,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "libraries": {
            name: version(name)
            for name in ("torch", "transformers", "huggingface-hub", "Pillow", "httpx")
        },
        "captioning_code_sha256": hashlib.sha256(
            (Path(__file__).resolve().parents[1] / "app" / "captioning.py").read_bytes()
        ).hexdigest(),
        "model_metadata_source": "Configuración del código local; no consultada al servidor.",
        "caption_model": CAPTION_MODEL,
        "caption_revision": CAPTION_REVISION,
        "translation_model": TRANSLATION_MODEL,
        "translation_revision": TRANSLATION_REVISION,
        "transport": "HTTP multipart/form-data",
        "device": "cpu",
        "results": results,
    }
    return save_report(report, args, parser)


def save_report(report: dict[str, Any], args: argparse.Namespace, parser: Any) -> int:
    results = report["results"]
    try:
        reviews = (
            json.loads(args.reviews.read_text(encoding="utf-8"))
            if args.reviews
            else [
                item["quality"]
                for item in results
                if item.get("quality", {}).get("status") == "reviewed"
            ]
        )
        if not isinstance(reviews, list):
            raise ValueError("El archivo de revisiones debe ser una lista.")
        apply_reviews(results, reviews)
        report["summary"] = summarize(results)
        report["by_type"] = {
            kind: summarize([item for item in results if item.get("type", "sin_tipo") == kind])
            for kind in sorted({item.get("type", "sin_tipo") for item in results})
        }
        report["review_report_utc"] = datetime.now(UTC).isoformat()
        current_rubric = hashlib.sha256(
            (Path(__file__).resolve().parents[1] / "docs" / "rubrica-alt-text.md").read_bytes()
        ).hexdigest()
        # Reprocesar respuestas no cambia la rúbrica con la que se puntuaron.
        if args.reviews or "rubric_sha256" not in report:
            report["rubric_sha256"] = current_rubric
            report["rubric_source"] = "docs/rubrica-alt-text.md"
        report["current_rubric_sha256"] = current_rubric
        if args.output.suffix.lower() != ".json":
            raise ValueError("El informe de salida debe tener extensión .json.")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        args.output.with_suffix(".md").write_text(markdown_report(report), encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"No se pudo guardar el informe: {exc}\n")
    passed = sum(item["passed"] for item in results)
    print(f"{passed} de {len(results)} peticiones correctas. Informe: {args.output}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
