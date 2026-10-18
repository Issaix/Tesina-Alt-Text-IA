"""Comprueba el set de la línea A y descarga únicamente las imágenes que falten."""

import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "examples" / "educational"


def main() -> None:
    records = json.loads((DIRECTORY / "manifest.json").read_text(encoding="utf-8"))
    for item in records:
        path = (DIRECTORY / item["file"]).resolve()
        if not path.is_relative_to(DIRECTORY.resolve()):
            raise ValueError("La imagen debe estar dentro del conjunto educativo.")
        if item["type"] not in {"fotografía", "ilustración"}:
            raise ValueError("El conjunto solo admite fotografías e ilustraciones generales.")
        if path.exists():
            data = path.read_bytes()
        else:
            with urlopen(item["source_url"], timeout=60) as response:
                data = response.read()
        if hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(
                f"El hash de {item['file']} no coincide; no se sobrescribió el archivo."
            )
        if not path.exists():
            path.write_bytes(data)
            print(f"Restaurada: {item['file']}")
    print(f"{len(records)} imágenes verificadas.")


if __name__ == "__main__":
    main()
