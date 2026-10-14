"""Figuras del informe del Lab 3 (Solidity y contratos). Paleta formal azul/gris, tipografía serif.

Las figuras 2 a 7 son recortes de las capturas reales de Remix guardadas en evidencia/ (sin retocar el contenido); la figura 1 es el
diagrama de estados del contrato propuesto para el caso universitario. Uso: py figuras.py
"""
from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.stdout.reconfigure(encoding="utf-8")

AQUI = pathlib.Path(__file__).resolve().parent.parent
EVID = AQUI / "evidencia"
SALIDA = AQUI / "figuras"
AZUL, AZUL_M, AZUL_C, AZUL_P = "#1F497D", "#4F6F9A", "#B8CCE4", "#DBE5F1"
GRIS, GRIS_L, GRIS_T, NEGRO = "#F2F2F2", "#BFBFBF", "#595959", "#000000"
ANCHO_IN = 6.5

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 9, "axes.unicode_minus": False})

# Recortes (x0, y0, x1, y1) en píxeles de la captura completa de 1440 x 900.
PANEL_FUNCIONES = (60, 675, 395, 835)       # funciones contador / mensaje / obtenerContador del contrato desplegado
EDITOR_Y_PANEL = (0, 45, 960, 765)          # panel del compilador + código
FILA_CONSOLA = (432, 0, 1330, 0)            # ancho de una fila de la consola (el alto cambia por captura)


def _guardar(fig, nombre: str) -> pathlib.Path:
    SALIDA.mkdir(exist_ok=True)
    ruta = SALIDA / nombre
    fig.savefig(ruta, dpi=300, facecolor="white")
    plt.close(fig)
    return ruta


def _recorte(captura: str, caja: tuple[int, int, int, int]):
    x0, y0, x1, y1 = caja
    return mpimg.imread(EVID / captura)[y0:y1, x0:x1]


def _marco(ax, titulo: str | None = None) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for lado in ax.spines.values():
        lado.set_edgecolor(GRIS_L)
        lado.set_linewidth(0.9)
    if titulo:
        ax.set_title(titulo, fontsize=8.5, pad=3)


def _tamano(caja: tuple[int, int, int, int]) -> tuple[int, int]:
    return caja[2] - caja[0], caja[3] - caja[1]


# --------------------------------------------------------------------------- Figura 1: estados del contrato propuesto
def fig_estados() -> pathlib.Path:
    fig, ax = plt.subplots(figsize=(ANCHO_IN, 2.9), dpi=300)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis("off")

    def caja(x, y, w, h, titulo, sub, fc="white", ec=AZUL, tc=NEGRO):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=1.2))
        ax.text(x + w / 2, y + h / 2 + 2.4, titulo, ha="center", va="center", fontsize=9.5, fontweight="bold", color=tc, family="monospace")
        ax.text(x + w / 2, y + h / 2 - 2.6, sub, ha="center", va="center", fontsize=8, color=tc, linespacing=1.15)

    def flecha(p1, p2, texto, dx=0.0, dy=3.2):
        ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color=GRIS_T, lw=1.2, mutation_scale=10, shrinkA=0, shrinkB=0))
        ax.text((p1[0] + p2[0]) / 2 + dx, (p1[1] + p2[1]) / 2 + dy, texto, ha="center", va="center", fontsize=8, style="italic",
                color=GRIS_T, linespacing=1.15)

    caja(2, 20, 20, 16, "Abierta", "acepta evidencias\nhasta la fecha límite", fc=AZUL_P, ec=AZUL_C)
    caja(40, 31, 22, 16, "Completa", "nota 5,0 registrada\npor el contrato", fc=AZUL, ec=AZUL, tc="white")
    caja(40, 3, 22, 16, "Vencida", "sin nota automática;\ndecide el docente", fc=GRIS, ec=GRIS_L)
    caja(78, 31, 20, 16, "Anulada", "el docente revierte\nla nota con motivo", fc="white", ec=AZUL)
    flecha((22, 31), (40, 39), "las N evidencias\nllegan a tiempo", dx=-3.5, dy=5.4)
    flecha((22, 24), (40, 12), "pasa la fecha límite\nsin completarlas", dx=-3.5, dy=-5.8)
    flecha((62, 39), (78, 39), "docente anula dentro\ndel plazo de revisión", dy=5.6)
    ax.text(82, 12, "Cada transición ocurre cuando alguien llama\nal contrato: no tiene reloj propio.", ha="center", va="center",
            fontsize=8, color=NEGRO, linespacing=1.2,
            bbox=dict(boxstyle="round,pad=0.5", fc=GRIS, ec=GRIS_L, lw=0.8))
    return _guardar(fig, "fig1_estados_contrato_universitario.png")


# --------------------------------------------------------------------------- Figura 2 y 5: compilación (original y modificado)
def fig_compilacion(captura: str, nombre: str) -> pathlib.Path:
    w, h = _tamano(EDITOR_Y_PANEL)
    fig, ax = plt.subplots(figsize=(ANCHO_IN, ANCHO_IN * h / w), dpi=300)
    fig.subplots_adjust(left=0.003, right=0.997, top=0.997, bottom=0.003)
    ax.imshow(_recorte(captura, EDITOR_Y_PANEL))
    _marco(ax)
    return _guardar(fig, nombre)


# --------------------------------------------------------------------------- Figura 3: contrato original funcionando (2 x 2)
def fig_original() -> pathlib.Path:
    paneles = (("a) mensaje() tras el despliegue", "04a_mensaje_inicial.png"),
               ("b) contador() tras el despliegue", "04b_contador_inicial.png"),
               ("c) contador() tras cambiarMensaje", "04d_contador_tras_cambio.png"),
               ("d) mensaje() tras cambiarMensaje", "04e_mensaje_tras_cambio.png"))
    w, h = _tamano(PANEL_FUNCIONES)
    fig, axs = plt.subplots(2, 2, figsize=(ANCHO_IN, ANCHO_IN * (2 * h + 40) / (2 * w + 20)), dpi=300)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.94, bottom=0.005, wspace=0.03, hspace=0.20)
    for ax, (titulo, captura) in zip(axs.flat, paneles):
        ax.imshow(_recorte(captura, PANEL_FUNCIONES))
        _marco(ax, titulo)
    return _guardar(fig, "fig3_contrato_original_funcionando.png")


# --------------------------------------------------------------------------- Figura 4: transacciones en la consola
def fig_consola() -> pathlib.Path:
    filas = (("a) Despliegue del contrato original (constructor)", "04_despliegue_original.png", (432, 768, 1330, 814)),
             ("b) cambiarMensaje (escritura)", "04c_transaccion_cambiarMensaje.png", (432, 762, 1330, 812)),
             ("c) establecerPrecio, en el contrato modificado (escritura)", "05b_transaccion_establecerPrecio.png", (432, 762, 1330, 812)))
    alturas = [f[2][3] - f[2][1] for f in filas]
    ancho = filas[0][2][2] - filas[0][2][0]
    total = sum(alturas) + 3 * 34
    fig, axs = plt.subplots(3, 1, figsize=(ANCHO_IN, ANCHO_IN * total / ancho), dpi=300, gridspec_kw={"height_ratios": [a + 20 for a in alturas]})
    fig.subplots_adjust(left=0.005, right=0.995, top=0.93, bottom=0.005, hspace=0.55)
    for ax, (titulo, captura, caja) in zip(axs, filas):
        ax.imshow(_recorte(captura, caja))
        _marco(ax, titulo)
    return _guardar(fig, "fig4_transacciones_consola.png")


# --------------------------------------------------------------------------- Figura 6: contrato modificado funcionando (1 x 2)
def fig_modificado() -> pathlib.Path:
    paneles = (("a) establecerPrecio(1000000)", "05b_transaccion_establecerPrecio.png", (60, 480, 395, 870)),
               ("b) precio() devuelve el valor guardado", "05c_precio_leido.png", (60, 305, 395, 695)))
    w, h = 335, 390
    fig, axs = plt.subplots(1, 2, figsize=(ANCHO_IN * 0.78, ANCHO_IN * 0.78 * (h + 22) / (2 * w + 12)), dpi=300)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.93, bottom=0.005, wspace=0.04)
    for ax, (titulo, captura, caja) in zip(axs, paneles):
        ax.imshow(_recorte(captura, caja))
        _marco(ax, titulo)
    return _guardar(fig, "fig6_contrato_modificado_funcionando.png")


# --------------------------------------------------------------------------- Figura 7: gas de una escritura y de una lectura
def fig_gas() -> pathlib.Path:
    paneles = (("a) Transacción cambiarMensaje (escritura)", "06a_gas_transaccion_cambiarMensaje.png", (436, 130, 1220, 430)),
               ("b) Llamada contador() (lectura)", "06b_gas_llamada_contador.png", (436, 185, 1220, 520)))
    alturas = [p[2][3] - p[2][1] for p in paneles]
    fig, axs = plt.subplots(2, 1, figsize=(ANCHO_IN, ANCHO_IN * (sum(alturas) + 70) / 784), dpi=300, gridspec_kw={"height_ratios": alturas})
    fig.subplots_adjust(left=0.005, right=0.995, top=0.95, bottom=0.005, hspace=0.18)
    for ax, (titulo, captura, caja) in zip(axs, paneles):
        ax.imshow(_recorte(captura, caja))
        _marco(ax, titulo)
    return _guardar(fig, "fig7_gas_escritura_vs_lectura.png")


def generar_todas() -> list[pathlib.Path]:
    return [fig_estados(), fig_compilacion("03_compilacion_original.png", "fig2_compilacion_original.png"), fig_original(),
            fig_consola(), fig_compilacion("05a_modificado_compilado.png", "fig5_compilacion_modificado.png"), fig_modificado(), fig_gas()]


if __name__ == "__main__":
    for ruta in generar_todas():
        print(ruta)
