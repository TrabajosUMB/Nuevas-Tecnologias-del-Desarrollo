"""Compone las figuras de código del informe a partir de las capturas reales de VS Code (evidencia/vscode/*.png y *_meta.json).

El código largo se parte en un renglón en blanco para que cada figura quepa en una página con letra legible. No se retoca el contenido de las
capturas: solo se recortan y se enmarcan. Salida: evidencia/vscode/figuras/<id>_<n>.png y manifiesto.json.
Uso: py componer_capturas.py
"""
from __future__ import annotations

import json
import pathlib
import sys

from PIL import Image, ImageOps

sys.stdout.reconfigure(encoding="utf-8")
AQUI = pathlib.Path(__file__).resolve().parent
ENTRADA = AQUI.parent / "evidencia" / "vscode"
SALIDA = ENTRADA / "figuras"
MAX_PARTE = 1500                # alto máximo (px) de una parte de código; con 1334 px de ancho cabe en 6,1 pulgadas de ancho y 6,9 de alto
MARCO = 2
COLOR_MARCO = (191, 191, 191)
CAPTURAS = ["service_worker_cache_first", "service_worker_network_first", "registro_en_app"]


def enmarcar(imagen: Image.Image) -> Image.Image:
    return ImageOps.expand(imagen.convert("RGB"), border=MARCO, fill=COLOR_MARCO)


def partir(imagen: Image.Image, meta: dict) -> list[tuple[Image.Image, int, int]]:
    """Devuelve [(imagen, primera línea, última línea)] cortando siempre después de un renglón en blanco."""
    escala = imagen.width / meta["anchoRecorte"]                         # px de la imagen por píxel CSS (incluye el factor de pantalla de Windows)
    lineas = meta["lineas"]
    fondos = [(l["top"] + l["alto"]) * escala for l in lineas]            # borde inferior de cada línea, en px
    ultimo = int(fondos[-1]) + 6                                          # se descarta el espacio vacío bajo la última línea
    imagen = imagen.crop((0, 0, imagen.width, min(imagen.height, ultimo)))
    if imagen.height <= MAX_PARTE:
        return [(imagen, 1, len(lineas))]
    partes, inicio_y, primera = [], 0.0, 0
    while True:
        if imagen.height - inicio_y <= MAX_PARTE:
            partes.append((imagen.crop((0, int(inicio_y), imagen.width, imagen.height)), primera + 1, len(lineas)))
            return partes
        candidatos = [k for k in range(primera, len(lineas) - 1)
                      if lineas[k]["texto"].strip() == "" and MAX_PARTE * 0.45 < fondos[k] - inicio_y <= MAX_PARTE]
        if not candidatos:
            raise SystemExit(f"{meta['archivo']}: no hay un renglón en blanco donde cortar")
        k = candidatos[-1]
        corte = int(fondos[k]) + 1
        partes.append((imagen.crop((0, int(inicio_y), imagen.width, corte)), primera + 1, k + 1))
        inicio_y, primera = float(corte), k + 1


def main() -> None:
    SALIDA.mkdir(exist_ok=True)
    manifiesto: dict[str, list[dict]] = {}
    for cid in CAPTURAS:
        imagen = Image.open(ENTRADA / f"{cid}.png")
        meta = json.loads((ENTRADA / f"{cid}_meta.json").read_text(encoding="utf-8"))
        manifiesto[cid] = []
        for n, (parte, ini, fin) in enumerate(partir(imagen, meta), 1):
            figura = enmarcar(parte)
            nombre = f"{cid}_{n}.png"
            figura.save(SALIDA / nombre)
            manifiesto[cid].append({"archivo": nombre, "parte": n, "lineas": [ini, fin], "alto_px": figura.height, "ancho_px": figura.width,
                                    "archivo_fuente": meta["archivo"]})
        print(cid, [(m["archivo"], m["lineas"], m["alto_px"]) for m in manifiesto[cid]])
    estructura = enmarcar(Image.open(ENTRADA / "estructura_proyecto.png"))
    estructura.save(SALIDA / "estructura_proyecto.png")
    manifiesto["estructura_proyecto"] = [{"archivo": "estructura_proyecto.png", "parte": 1, "lineas": None,
                                          "alto_px": estructura.height, "ancho_px": estructura.width}]
    (SALIDA / "manifiesto.json").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
