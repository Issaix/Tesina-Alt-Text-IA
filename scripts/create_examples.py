"""Crea cuatro láminas educativas originales y reproducibles para el Sprint 1."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "examples" / "educational"


def main() -> None:
    DIRECTORY.mkdir(parents=True, exist_ok=True)
    # La fuente predeterminada de Pillow no incluye todas las vocales acentuadas.
    for name in ("DejaVuSans.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"):
        try:
            font = ImageFont.truetype(name, 24)
            title = ImageFont.truetype(name, 32)
            break
        except OSError:
            continue
    else:
        raise RuntimeError(
            "Instala DejaVu Sans, Arial o Liberation Sans para regenerar las láminas."
        )
    records: list[dict[str, str]] = []

    def canvas(name: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        image = Image.new("RGB", (800, 600), "white")
        draw = ImageDraw.Draw(image)
        draw.text((30, 25), name, fill="#172554", font=title)
        return image, draw

    def save(image: Image.Image, filename: str, subject: str, expected: str) -> None:
        try:
            image.save(DIRECTORY / filename)
        finally:
            image.close()
        records.append(
            {
                "file": filename,
                "subject": subject,
                "reference": expected,
                "source": "Ilustración original generada por scripts/create_examples.py",
            }
        )

    image, draw = canvas("Geometría: triángulo rectángulo")
    draw.polygon([(200, 150), (200, 450), (600, 450)], fill="#bae6fd", outline="#075985", width=6)
    draw.line([(200, 415), (235, 415), (235, 450)], fill="#075985", width=3)
    for position, text in [((135, 295), "3 cm"), ((350, 475), "4 cm"), ((420, 270), "5 cm")]:
        draw.text(position, text, fill="black", font=font)
    save(
        image,
        "triangulo.png",
        "Geometría",
        "Triángulo rectángulo con catetos de 3 y 4 cm e hipotenusa de 5 cm.",
    )

    image, draw = canvas("Libros leídos por grupo")
    draw.line([(120, 115), (120, 490), (730, 490)], fill="black", width=4)
    for value in range(0, 11, 2):
        y = 490 - value * 32
        draw.line([(120, y), (730, y)], fill="#d1d5db", width=1)
        draw.text((70, y - 13), str(value), fill="black", font=font)
    for x, value, label, color in [
        (190, 4, "A", "#2563eb"),
        (360, 7, "B", "#16a34a"),
        (530, 10, "C", "#f97316"),
    ]:
        draw.rectangle((x, 490 - value * 32, x + 95, 490), fill=color)
        draw.text((x + 32, 505), label, fill="black", font=font)
    save(
        image,
        "barras.jpg",
        "Estadística",
        "Gráfico de barras: grupos A, B y C leyeron 4, 7 y 10 libros, respectivamente.",
    )

    image, draw = canvas("Astronomía: Sol, Tierra y Luna")
    draw.ellipse((70, 220, 280, 430), fill="#facc15", outline="#eab308", width=5)
    draw.ellipse((440, 265, 560, 385), fill="#2563eb")
    draw.polygon(
        [(475, 275), (520, 285), (540, 330), (505, 340), (488, 375), (460, 335)], fill="#22c55e"
    )
    draw.ellipse((660, 300, 710, 350), fill="#9ca3af")
    for x, label in [(150, "Sol"), (465, "Tierra"), (655, "Luna")]:
        draw.text((x, 450), label, fill="black", font=font)
    draw.text((160, 530), "Esquema ilustrativo, sin escala real", fill="#475569", font=font)
    save(
        image,
        "astronomia.jpeg",
        "Astronomía",
        "Esquema sin escala del Sol amarillo, la Tierra azul y verde y la Luna gris.",
    )

    image, draw = canvas("Biología: partes de una planta")
    draw.line([(400, 220), (400, 460)], fill="#15803d", width=14)
    draw.ellipse((280, 295, 395, 345), fill="#22c55e")
    draw.ellipse((405, 350, 520, 400), fill="#16a34a")
    for box in [
        (355, 120, 405, 195),
        (395, 120, 445, 195),
        (330, 170, 405, 220),
        (395, 170, 470, 220),
        (365, 200, 435, 260),
    ]:
        draw.ellipse(box, fill="#f472b6")
    draw.ellipse((370, 165, 430, 225), fill="#facc15")
    draw.line([(140, 460), (660, 460)], fill="#92400e", width=5)
    for end in [(330, 550), (385, 565), (455, 555)]:
        draw.line([(400, 460), end], fill="#92400e", width=6)
    for position, label in [
        ((535, 180), "Flor"),
        ((555, 355), "Hoja"),
        ((245, 400), "Tallo"),
        ((490, 520), "Raíz"),
    ]:
        draw.text(position, label, fill="black", font=font)
    save(
        image,
        "planta.png",
        "Biología",
        "Planta con flor rosa y amarilla, hojas verdes, tallo y raíces; partes rotuladas.",
    )
    manifest_path = DIRECTORY / "manifest.json"
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        # Las referencias revisadas y las imágenes añadidas pertenecen al conjunto,
        # aunque este generador solo dibuje las cuatro láminas originales.
        known_files = {record["file"] for record in existing}
        records = existing + [record for record in records if record["file"] not in known_files]
    manifest_path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"4 láminas regeneradas en {DIRECTORY}")


if __name__ == "__main__":
    main()
