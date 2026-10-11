"""Regenera las cuatro láminas de ampliación; las fotografías se conservan tal cual."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIRECTORY = Path(__file__).resolve().parent


def main() -> None:
    for name in ("DejaVuSans.ttf", "Arial.ttf", "LiberationSans-Regular.ttf"):
        try:
            font = ImageFont.truetype(name, 24)
            title = ImageFont.truetype(name, 34)
            small = ImageFont.truetype(name, 20)
            break
        except OSError:
            continue
    else:
        raise RuntimeError("Se necesita DejaVu Sans, Arial o Liberation Sans.")

    def canvas(text: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        image = Image.new("RGB", (1000, 640), "white")
        draw = ImageDraw.Draw(image)
        draw.text((40, 30), text, font=title, fill="#172554")
        return image, draw

    def arrow(draw: ImageDraw.ImageDraw, start: tuple, end: tuple) -> None:
        draw.line([start, end], fill="#334155", width=4)
        direction = 1 if end[0] > start[0] else -1
        draw.polygon(
            [end, (end[0] - direction * 12, end[1] - 7), (end[0] - direction * 12, end[1] + 7)],
            fill="#334155",
        )

    image, draw = canvas("Cambios de estado del agua")
    for x, label, color in [
        (50, "Sólido", "#dbeafe"),
        (390, "Líquido", "#bfdbfe"),
        (730, "Gas", "#93c5fd"),
    ]:
        draw.rounded_rectangle((x, 250, x + 220, 370), radius=12, fill=color)
        draw.text((x + 110, 310), label, anchor="mm", font=font, fill="#172554")
    for x, forward, reverse in [
        (270, "Fusión", "Solidificación"),
        (610, "Evaporación", "Condensación"),
    ]:
        arrow(draw, (x + 5, 270), (x + 115, 270))
        arrow(draw, (x + 115, 350), (x + 5, 350))
        draw.text((x + 60, 220), forward, anchor="mm", font=small, fill="#172554")
        draw.text((x + 60, 405), reverse, anchor="mm", font=small, fill="#172554")
    draw.text(
        (40, 530), "Las flechas indican el sentido de cada cambio.", font=font, fill="#334155"
    )
    image.save(DIRECTORY / "estados_agua.png")
    image.close()

    image, draw = canvas("Una cadena alimentaria")
    for x, label in [(40, "Pasto"), (280, "Saltamontes"), (520, "Rana"), (760, "Serpiente")]:
        draw.rounded_rectangle(
            (x, 250, x + 190, 360), radius=12, fill="#dcfce7", outline="#15803d", width=3
        )
        draw.text((x + 95, 305), label, anchor="mm", font=font, fill="#14532d")
        if x < 760:
            arrow(draw, (x + 200, 305), (x + 230, 305))
    draw.text(
        (40, 455),
        "Cada flecha va del alimento al organismo que lo consume.",
        font=font,
        fill="#334155",
    )
    image.save(DIRECTORY / "cadena_alimentaria.png")
    image.close()

    image, draw = canvas("Temperatura registrada a las 12:00")
    draw.text((75, 100), "Temperatura (grados Celsius)", font=small, fill="#334155")
    for value in range(16, 27, 2):
        y = 500 - (value - 16) * 30
        draw.line([(130, y), (930, y)], fill="#d1d5db", width=1)
        draw.text((90, y), str(value), anchor="mm", font=small, fill="#334155")
    draw.line([(130, 170), (130, 500), (930, 500)], fill="#334155", width=3)
    values = [18, 21, 19, 24, 22]
    points = [(180 + index * 170, 500 - (value - 16) * 30) for index, value in enumerate(values)]
    draw.line(points, fill="#2563eb", width=4)
    for (x, y), value, day in zip(points, values, ["Lun", "Mar", "Mié", "Jue", "Vie"], strict=True):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill="#2563eb")
        draw.text((x, y - 25), str(value), anchor="mm", font=font, fill="#172554")
        draw.text((x, 530), day, anchor="mm", font=font, fill="#334155")
    draw.text((820, 585), "Día", font=font, fill="#334155")
    draw.text(
        (40, 585),
        "Datos ficticios para practicar la lectura de gráficas.",
        font=small,
        fill="#475569",
    )
    image.save(DIRECTORY / "temperaturas.png")
    image.close()

    image, draw = canvas("Cómo llegan a la escuela 20 estudiantes")
    start = -90
    for fraction, color in [(0.5, "#2563eb"), (0.3, "#16a34a"), (0.2, "#f97316")]:
        end = start + 360 * fraction
        draw.pieslice(
            (60, 150, 490, 580), start=start, end=end, fill=color, outline="white", width=4
        )
        start = end
    for y, label, color in [
        (220, "A pie: 10 estudiantes (50 %)", "#2563eb"),
        (310, "Bicicleta: 6 estudiantes (30 %)", "#16a34a"),
        (400, "Automóvil: 4 estudiantes (20 %)", "#f97316"),
    ]:
        draw.rectangle((535, y, 560, y + 25), fill=color)
        draw.text((580, y), label, font=font, fill="#172554")
    draw.text((535, 510), "Datos ficticios para uso educativo.", font=small, fill="#475569")
    image.save(DIRECTORY / "transporte.png")
    image.close()


if __name__ == "__main__":
    main()
