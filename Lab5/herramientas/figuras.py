"""Prepara las figuras del informe a partir de las capturas reales (evidencia/ y evidencia/vscode/figuras/).

Solo se recortan, se apilan y se enmarcan: no se retoca el contenido. Los recortes quitan el espacio vacío de los paneles de DevTools; cuando
la franja inferior importa (el total de entradas del caché, el resumen del panel Network) se agrega como una pieza aparte con un
pequeño hueco blanco, y la nota de cada figura lo dice. Salida: figuras/*.png.  Uso: py figuras.py
"""
from __future__ import annotations

import pathlib
import shutil
import sys

from PIL import Image, ImageOps

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = pathlib.Path(__file__).resolve().parent.parent
EVIDENCIA = RAIZ / "evidencia"
CODIGO = EVIDENCIA / "vscode" / "figuras"
SALIDA = RAIZ / "figuras"
MARCO = 2
COLOR_MARCO = (191, 191, 191)
HUECO = 10

ANCHO_DEVTOOLS = 1720                               # px de las capturas de DevTools (860 px CSS al doble de densidad)
BARRA_INFERIOR = (0, 1440, ANCHO_DEVTOOLS, 1500)    # franja «Total entries» / resumen del panel Network
ANCHO_APP = 1600                                    # px de las capturas de la app (800 px CSS al doble de densidad)
ALTO_APP = 860                                      # la página de la app termina antes


def abrir(ruta: pathlib.Path) -> Image.Image:
    return Image.open(ruta).convert("RGB")


def recorte(ruta: pathlib.Path, caja: tuple[int, int, int, int]) -> Image.Image:
    return abrir(ruta).crop(caja)


def enmarcar(imagen: Image.Image) -> Image.Image:
    return ImageOps.expand(imagen, border=MARCO, fill=COLOR_MARCO)


def apilar(piezas: list[Image.Image], hueco: int = HUECO) -> Image.Image:
    piezas = [enmarcar(p) for p in piezas]
    ancho = max(p.width for p in piezas)
    alto = sum(p.height for p in piezas) + hueco * (len(piezas) - 1)
    lienzo = Image.new("RGB", (ancho, alto), "white")
    y = 0
    for p in piezas:
        lienzo.paste(p, (0, y))
        y += p.height + hueco
    return lienzo


def guardar(nombre: str, imagen: Image.Image) -> None:
    imagen.save(SALIDA / nombre)
    print(f"{nombre}: {imagen.width}x{imagen.height}")


def devtools(nombre_origen: str, alto: int, con_barra: bool = False) -> Image.Image:
    ruta = EVIDENCIA / nombre_origen
    piezas = [recorte(ruta, (0, 0, ANCHO_DEVTOOLS, alto))]
    if con_barra:
        piezas.append(recorte(ruta, BARRA_INFERIOR))
    return apilar(piezas, hueco=0) if len(piezas) == 1 else apilar_union(piezas)


def apilar_union(piezas: list[Image.Image]) -> Image.Image:
    """Une un recorte y su franja inferior en una sola imagen enmarcada, separados por un hueco blanco."""
    ancho = max(p.width for p in piezas)
    alto = sum(p.height for p in piezas) + HUECO * (len(piezas) - 1)
    lienzo = Image.new("RGB", (ancho, alto), "white")
    y = 0
    for p in piezas:
        lienzo.paste(p, (0, y))
        y += p.height + HUECO
    return enmarcar(lienzo)


def app(nombre_origen: str) -> Image.Image:
    return recorte(EVIDENCIA / nombre_origen, (0, 0, ANCHO_APP, ALTO_APP))


def main() -> None:
    SALIDA.mkdir(exist_ok=True)
    # capturas de VS Code (ya recortadas y enmarcadas por componer_capturas.py)
    for origen in sorted(CODIGO.glob("*.png")):
        shutil.copy(origen, SALIDA / f"vscode_{origen.name}")
        print(f"vscode_{origen.name}")
    # paneles de Chrome DevTools
    guardar("devtools_service_worker.png", devtools("01_devtools_service_worker.png", 950))
    guardar("devtools_consola.png", devtools("02_devtools_consola.png", 300))
    guardar("devtools_cache_v1.png", devtools("03_devtools_cache_storage.png", 700, con_barra=True))
    guardar("devtools_offline_casilla.png", devtools("04_devtools_offline_activado.png", 500))
    guardar("devtools_network_offline.png", devtools("06_devtools_network_sin_conexion.png", 700, con_barra=True))
    guardar("devtools_version_en_espera.png", devtools("08_devtools_version_en_espera.png", 1020))
    guardar("devtools_cache_v2.png", devtools("09_devtools_cache_actualizado.png", 700, con_barra=True))
    # la app
    guardar("app_sin_conexion.png", apilar([app("05_app_sin_conexion.png"), app("07_app_sin_conexion_con_entrega.png")]))
    guardar("comparacion_servidor_actualizado.png",
            apilar([app("10_cache_first_con_servidor_actualizado.png"), app("11_network_first_con_servidor_actualizado.png")]))
    guardar("comparacion_sin_servidor.png",
            apilar([app("10_cache_first_sin_servidor.png"), app("11_network_first_sin_servidor.png")]))


if __name__ == "__main__":
    main()
