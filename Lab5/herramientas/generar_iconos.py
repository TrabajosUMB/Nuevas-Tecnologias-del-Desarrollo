"""Genera los íconos de la PWA (icons/icon-192.png e icons/icon-512.png): una hoja de agenda con una marca de verificación, en azul UMB.

Se dibuja a 4x y se reduce para suavizar los bordes. Uso: py generar_iconos.py
"""
from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw

AZUL = (31, 73, 125)
AZUL_CLARO = (219, 229, 241)
BLANCO = (255, 255, 255)
SALIDA = pathlib.Path(__file__).resolve().parent.parent / "proyecto" / "icons"


def dibujar(lado: int) -> Image.Image:
    g = lado * 4                                              # lienzo de trabajo ampliado
    imagen = Image.new("RGBA", (g, g), AZUL + (255,))
    d = ImageDraw.Draw(imagen)
    margen = g * 0.20
    hoja = (margen, margen * 1.15, g - margen, g - margen * 0.9)
    d.rounded_rectangle(hoja, radius=g * 0.07, fill=BLANCO)
    franja = (hoja[0], hoja[1], hoja[2], hoja[1] + g * 0.16)
    d.rounded_rectangle(franja, radius=g * 0.07, fill=AZUL_CLARO)
    d.rectangle((franja[0], franja[1] + g * 0.08, franja[2], franja[3]), fill=AZUL_CLARO)
    for fraccion in (0.34, 0.66):                             # argollas de la agenda
        x = hoja[0] + (hoja[2] - hoja[0]) * fraccion
        d.rounded_rectangle((x - g * 0.018, hoja[1] - g * 0.05, x + g * 0.018, hoja[1] + g * 0.08), radius=g * 0.018, fill=AZUL)
    # marca de verificación
    cx, cy = (hoja[0] + hoja[2]) / 2, (hoja[1] + hoja[3]) / 2 + g * 0.07
    puntos = [(cx - g * 0.15, cy), (cx - g * 0.04, cy + g * 0.11), (cx + g * 0.17, cy - g * 0.12)]
    d.line(puntos, fill=AZUL, width=int(g * 0.055), joint="curve")
    for x, y in (puntos[0], puntos[2]):
        r = g * 0.0275
        d.ellipse((x - r, y - r, x + r, y + r), fill=AZUL)
    return imagen.resize((lado, lado), Image.LANCZOS)


if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    for lado in (192, 512):
        ruta = SALIDA / f"icon-{lado}.png"
        dibujar(lado).save(ruta)
        print(ruta, Image.open(ruta).size)
