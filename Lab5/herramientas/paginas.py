"""Renderiza un PDF en hojas de dos páginas (PNG) para revisarlo a ojo. Uso: py paginas.py documento.pdf carpeta_salida [dpi]"""
from __future__ import annotations

import pathlib
import sys

import pymupdf
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")


def main(pdf: str, salida: str, dpi: int = 85) -> None:
    destino = pathlib.Path(salida)
    destino.mkdir(parents=True, exist_ok=True)
    for viejo in destino.glob("hoja_*.png"):
        viejo.unlink()
    with pymupdf.open(pdf) as doc:
        imagenes = []
        for pagina in doc:
            pix = pagina.get_pixmap(dpi=dpi)
            imagenes.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    for i in range(0, len(imagenes), 2):
        par = imagenes[i:i + 2]
        hoja = Image.new("RGB", (sum(p.width for p in par) + 8 * (len(par) - 1), par[0].height), (110, 110, 110))
        x = 0
        for p in par:
            hoja.paste(p, (x, 0))
            x += p.width + 8
        hoja.save(destino / f"hoja_{i // 2:02d}_p{i + 1}-{i + len(par)}.png")
    print(f"{len(imagenes)} páginas -> {destino}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 85)
