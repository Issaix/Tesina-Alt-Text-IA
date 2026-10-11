"""Regenera diez láminas educativas de matemáticas, ciencias y estadística."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIRECTORY = Path(__file__).resolve().parent
INK = "#172554"
BLUE = "#2563eb"
GREEN = "#15803d"


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

    def canvas(text: str, *, data: bool = False) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        image = Image.new("RGB", (1000, 640), "white")
        draw = ImageDraw.Draw(image)
        draw.text((40, 30), text, font=title, fill=INK)
        if data:
            draw.text((40, 600), "Datos ficticios para uso educativo.", font=small, fill=INK)
        return image, draw

    def save(image: Image.Image, name: str) -> None:
        image.save(DIRECTORY / name)
        image.close()

    image, draw = canvas("Fracciones equivalentes")
    for y, parts, selected, label in [(190, 2, 1, "1/2"), (370, 4, 2, "2/4")]:
        for index in range(parts):
            x = 130 + index * 600 // parts
            draw.rectangle(
                (x, y, x + 600 // parts, y + 100),
                fill="#93c5fd" if index < selected else "white",
                outline=INK,
                width=3,
            )
        draw.text((800, y + 50), label, anchor="mm", font=title, fill=INK)
    draw.text((130, 540), "La misma porción: 1/2 = 2/4", font=font, fill=INK)
    save(image, "fracciones.png")

    image, draw = canvas("Puntos en el plano cartesiano")
    for value in range(-3, 4):
        x, y = 500 + value * 65, 325 - value * 65
        draw.line((305, y, 695, y), fill="#d1d5db")
        draw.line((x, 130, x, 520), fill="#d1d5db")
        if value:
            draw.text((x, 343), str(value), anchor="mm", font=small, fill=INK)
            draw.text((478, y), str(value), anchor="mm", font=small, fill=INK)
    draw.line((280, 325, 730, 325), fill=INK, width=3)
    draw.line((500, 105, 500, 545), fill=INK, width=3)
    draw.text((745, 315), "x", font=font, fill=INK)
    draw.text((510, 95), "y", font=font, fill=INK)
    draw.text((480, 343), "0", anchor="mm", font=small, fill=INK)
    for a, b, label in [(2, 1, "A (2, 1)"), (-2, 2, "B (-2, 2)"), (-1, -2, "C (-1, -2)")]:
        x, y = 500 + a * 65, 325 - b * 65
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=BLUE)
        label_position = (x - 155, y + 15) if a == -1 else (x + 12, y - 30)
        draw.text(label_position, label, font=font, fill=INK)
    save(image, "coordenadas.png")

    image, draw = canvas("Circuito eléctrico cerrado")
    draw.line([(200, 270), (200, 170), (440, 170)], fill=INK, width=4)
    draw.line([(560, 170), (800, 170), (800, 290)], fill=INK, width=4)
    draw.line([(800, 390), (800, 490), (200, 490), (200, 330)], fill=INK, width=4)
    draw.line((150, 270, 250, 270), fill=INK, width=5)
    draw.line((170, 330, 230, 330), fill=INK, width=5)
    draw.text((65, 290), "Pila", font=font, fill=INK)
    draw.text((265, 255), "+", font=font, fill=INK)
    draw.text((245, 315), "-", font=font, fill=INK)
    draw.line((440, 170, 560, 170), fill=GREEN, width=5)
    for x in (440, 560):
        draw.ellipse((x - 6, 164, x + 6, 176), fill=INK)
    draw.text((500, 115), "Interruptor cerrado", anchor="mm", font=font, fill=INK)
    draw.ellipse((750, 290, 850, 390), fill="#fef08a", outline=INK, width=4)
    draw.line((765, 305, 835, 375), fill=INK, width=3)
    draw.line((765, 375, 835, 305), fill=INK, width=3)
    draw.text((865, 340), "Lámpara", anchor="lm", font=font, fill=INK)
    draw.text((250, 545), "Un solo recorrido, sin interrupciones.", font=font, fill=INK)
    save(image, "circuito.png")

    image, draw = canvas("Clasificación de triángulos por sus lados")
    for x, label, detail, points in [
        (170, "Equilátero", "Tres lados iguales", [(70, 390), (270, 390), (170, 217)]),
        (500, "Isósceles", "Solo dos lados iguales", [(420, 390), (580, 390), (500, 190)]),
        (830, "Escaleno", "Tres lados diferentes", [(710, 390), (930, 390), (760, 210)]),
    ]:
        draw.polygon(points, fill="#dbeafe", outline=INK, width=3)
        draw.text((x, 450), label, anchor="mm", font=font, fill=INK)
        draw.text((x, 495), detail, anchor="mm", font=small, fill=INK)
    draw.text((40, 560), "Aquí se separa el equilátero del isósceles.", font=small, fill=INK)
    save(image, "tipos_triangulos.png")

    image, draw = canvas("Área y perímetro de un rectángulo")
    draw.rectangle((240, 190, 720, 430), fill="#dcfce7", outline=INK, width=4)
    draw.text((480, 150), "8 cm", anchor="mm", font=font, fill=INK)
    draw.text((790, 310), "4 cm", anchor="mm", font=font, fill=INK)
    draw.text((240, 480), "Área: 8 x 4 = 32 cm cuadrados", font=font, fill=INK)
    draw.text((240, 525), "Perímetro: 8 + 4 + 8 + 4 = 24 cm", font=font, fill=INK)
    save(image, "rectangulo.png")

    image, draw = canvas("Ciclo de vida de una mariposa")
    boxes = [(130, 160, "Huevo"), (640, 160, "Larva"), (640, 410, "Pupa"), (130, 410, "Adulto")]
    for x, y, label in boxes:
        draw.rounded_rectangle(
            (x, y, x + 230, y + 90), radius=12, fill="#dcfce7", outline=GREEN, width=3
        )
        draw.text((x + 115, y + 45), label, anchor="mm", font=font, fill=INK)
    for start, end in [
        ((370, 205), (625, 205)),
        ((755, 265), (755, 395)),
        ((625, 455), (375, 455)),
        ((245, 395), (245, 265)),
    ]:
        draw.line([start, end], fill=INK, width=4)
        dx = (end[0] > start[0]) - (end[0] < start[0])
        dy = (end[1] > start[1]) - (end[1] < start[1])
        x, y = end
        draw.polygon(
            [
                (x, y),
                (x - 14 * dx + 7 * dy, y - 14 * dy - 7 * dx),
                (x - 14 * dx - 7 * dy, y - 14 * dy + 7 * dx),
            ],
            fill=INK,
        )
    draw.text((40, 555), "Las flechas siguen las etapas y vuelven al huevo.", font=font, fill=INK)
    save(image, "ciclo_mariposa.png")

    image, draw = canvas("Precipitación mensual", data=True)
    draw.text((120, 100), "Precipitación (mm)", font=small, fill=INK)
    for value in range(0, 81, 20):
        y = 490 - value * 4
        draw.line((150, y, 920, y), fill="#d1d5db")
        draw.text((110, y), str(value), anchor="mm", font=small, fill=INK)
    for x, label, value in [
        (230, "Enero", 20),
        (430, "Febrero", 0),
        (630, "Marzo", 60),
        (830, "Abril", 40),
    ]:
        y = 490 - value * 4
        if value:
            draw.rectangle((x - 50, y, x + 50, 490), fill=BLUE)
        draw.text((x, y - 22), str(value), anchor="mm", font=font, fill=INK)
        draw.text((x, 525), label, anchor="mm", font=font, fill=INK)
    draw.line((150, 160, 150, 490, 920, 490), fill=INK, width=3)
    draw.text((860, 560), "Mes", font=small, fill=INK)
    save(image, "precipitacion.png")

    image, draw = canvas("Residuos recolectados para reciclar", data=True)
    for value in range(0, 9, 2):
        x = 250 + value * 75
        draw.line((x, 160, x, 460), fill="#d1d5db")
        draw.text((x, 490), str(value), anchor="mm", font=small, fill=INK)
    for y, label, value in [(210, "Papel", 8), (310, "Vidrio", 5), (410, "Plástico", 3)]:
        draw.text((210, y), label, anchor="rm", font=font, fill=INK)
        draw.rectangle((250, y - 25, 250 + value * 75, y + 25), fill=GREEN)
        draw.text((270 + value * 75, y), str(value), anchor="lm", font=font, fill=INK)
    draw.line((250, 160, 250, 460, 900, 460), fill=INK, width=3)
    draw.text((410, 540), "Masa recolectada (kg)", font=font, fill=INK)
    save(image, "reciclaje.png")

    image, draw = canvas("Temperatura durante una madrugada", data=True)
    draw.text((110, 100), "Temperatura (grados Celsius)", font=small, fill=INK)
    for value in range(-4, 5, 2):
        y = 330 - value * 40
        draw.line((160, y, 920, y), fill=INK if value == 0 else "#d1d5db", width=2)
        draw.text((120, y), str(value), anchor="mm", font=small, fill=INK)
    points = [(220 + i * 200, 330 - v * 40) for i, v in enumerate([2, -2, -4, 0])]
    draw.line(points, fill=BLUE, width=4)
    for (x, y), value, hour in zip(
        points, [2, -2, -4, 0], ["00:00", "02:00", "04:00", "06:00"], strict=True
    ):
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=BLUE)
        draw.text((x, y - 25), str(value), anchor="mm", font=font, fill=INK)
        draw.text((x, 535), hour, anchor="mm", font=font, fill=INK)
    draw.text((865, 570), "Hora", font=small, fill=INK)
    save(image, "temperaturas_negativas.png")

    image, draw = canvas("Altura de cinco plantas", data=True)
    draw.text((80, 100), "Altura (cm)", font=small, fill=INK)
    for value in range(0, 21, 5):
        y = 500 - value * 16
        draw.line((160, y, 920, y), fill="#d1d5db")
        draw.text((120, y), str(value), anchor="mm", font=small, fill=INK)
    draw.line((160, 165, 160, 500, 920, 500), fill=INK, width=3)
    for hours, height in [(1, 5), (2, 9), (3, 8), (4, 14), (5, 17)]:
        x, y = 160 + hours * 140, 500 - height * 16
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=GREEN)
        draw.text((x, y - 25), str(height), anchor="mm", font=font, fill=INK)
    for hours in range(6):
        draw.text((160 + hours * 140, 530), str(hours), anchor="mm", font=small, fill=INK)
    draw.text((310, 565), "Exposición diaria a la luz (horas)", font=font, fill=INK)
    save(image, "dispersion_plantas.png")


if __name__ == "__main__":
    main()
