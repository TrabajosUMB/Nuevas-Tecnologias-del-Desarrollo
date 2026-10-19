"""Arma el entregable Lab5_ServiceWorker_Grupo6.zip: proyecto, informe (docx y pdf), evidencia real y scripts para repetir las pruebas.

Uso: py empaquetar.py   ->  Lab5_ServiceWorker_Grupo6.zip (junto a la carpeta proyecto)
"""
from __future__ import annotations

import pathlib
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
RAIZ = pathlib.Path(__file__).resolve().parent.parent
RAIZ_ZIP = "Lab5_ServiceWorker_Grupo6"
SALIDA = RAIZ / f"{RAIZ_ZIP}.zip"
SCRIPTS = ("ejecutar_laboratorio.mjs", "cdp_lib.mjs", "servidor.py", "lanzar_chrome.ps1", "generar_iconos.py")


def archivos() -> list[tuple[pathlib.Path, str]]:
    lista: list[tuple[pathlib.Path, str]] = []
    for ruta in sorted((RAIZ / "proyecto").rglob("*")):
        if ruta.is_file():
            lista.append((ruta, f"proyecto/{ruta.relative_to(RAIZ / 'proyecto').as_posix()}"))
    for nombre in (f"{RAIZ_ZIP}.docx", f"{RAIZ_ZIP}.pdf"):
        lista.append((RAIZ / nombre, nombre))
    for ruta in sorted((RAIZ / "evidencia").iterdir()):
        if ruta.is_file():
            lista.append((ruta, f"evidencia/{ruta.name}"))
    for nombre in SCRIPTS:
        lista.append((RAIZ / "herramientas" / nombre, f"herramientas/{nombre}"))
    return lista


def main() -> None:
    entradas = archivos()
    faltan = [str(r) for r, _ in entradas if not r.exists()]
    if faltan:
        raise SystemExit(f"faltan archivos: {faltan}")
    with zipfile.ZipFile(SALIDA, "w", zipfile.ZIP_DEFLATED) as z:
        for ruta, destino in entradas:
            z.write(ruta, f"{RAIZ_ZIP}/{destino}")
    with zipfile.ZipFile(SALIDA) as z:
        assert z.testzip() is None
        nombres = z.namelist()
    print(f"{SALIDA.name}: {len(nombres)} archivos, {SALIDA.stat().st_size // 1024} KB")
    for n in nombres:
        print("  ", n)


if __name__ == "__main__":
    main()
