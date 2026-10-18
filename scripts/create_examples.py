"""Comprueba el set de la línea A y descarga únicamente las imágenes que falten."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "examples" / "educational"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DIRECTORY / "manifest.json")
    args = parser.parse_args()
    directory = args.manifest.resolve().parent
    records = json.loads(args.manifest.read_text(encoding="utf-8"))
    for item in records:
        path = (directory / item["file"]).resolve()
        if not path.is_relative_to(directory):
            raise ValueError("La imagen debe estar dentro del conjunto educativo.")
        complementary = item.get("scope") == "complementario_limitaciones"
        allowed = {"diagrama", "gráfica"} if complementary else {"fotografía", "ilustración"}
        if item["type"] not in allowed:
            raise ValueError("El tipo de imagen no corresponde al alcance declarado.")
        if path.exists():
            data = path.read_bytes()
        elif complementary:
            raise FileNotFoundError(
                f"Falta {path.name}. Recupera la lámina original del repositorio del proyecto."
            )
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
