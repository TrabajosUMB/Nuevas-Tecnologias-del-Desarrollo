"""Figuras del informe «Agentes inteligentes de IA» (matplotlib, paleta formal azul/gris, tipografía serif).

Cada función dibuja una figura y la guarda en figuras/. Las cifras de la figura 6 son las publicadas por
Agent Arena (arena.ai/leaderboard/agent) el 30 de septiembre de 2026, categoría General.
"""
from __future__ import annotations

import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle

sys.stdout.reconfigure(encoding="utf-8")

SALIDA = pathlib.Path(__file__).parent / "figuras"
AZUL, AZUL_M, AZUL_C, AZUL_P = "#1F497D", "#4F6F9A", "#B8CCE4", "#DBE5F1"
GRIS, GRIS_L, GRIS_T, NEGRO = "#F2F2F2", "#BFBFBF", "#595959", "#000000"
ANCHO_IN = 6.5

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 9,
    "axes.unicode_minus": False,
})


def _lienzo(alto_in: float, xmax: float = 100, ymax: float = 50):
    fig, ax = plt.subplots(figsize=(ANCHO_IN, alto_in), dpi=300)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    return fig, ax


def _caja(ax, x, y, w, h, texto, fc="white", ec=AZUL, tc=NEGRO, size=8.5, negrita_primera=True, ls="-", lw=1.1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=lw, ls=ls))
    lineas = texto.split("\n")
    n = len(lineas)
    paso = min(h / (n + 0.6), size * 0.36)
    y0 = y + h / 2 + (n - 1) * paso / 2
    for i, linea in enumerate(lineas):
        ax.text(x + w / 2, y0 - i * paso, linea, ha="center", va="center", color=tc, fontsize=size if i == 0 else size - 0.8,
                fontweight="bold" if (i == 0 and negrita_primera) else "normal")


def _flecha(ax, p1, p2, color=GRIS_T, lw=1.2, estilo="-|>", ls="-", conexion="arc3,rad=0"):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle=estilo, color=color, lw=lw, ls=ls,
                                                      shrinkA=0, shrinkB=0, connectionstyle=conexion, mutation_scale=9))


def _guardar(fig, nombre: str) -> pathlib.Path:
    SALIDA.mkdir(exist_ok=True)
    ruta = SALIDA / nombre
    fig.savefig(ruta, dpi=300, facecolor="white")
    plt.close(fig)
    return ruta


# --------------------------------------------------------------------------- Figura 1: ciclo del agente
def fig_ciclo() -> pathlib.Path:
    fig, ax = _lienzo(3.2, ymax=50)
    _caja(ax, 4, 20, 24, 14, "Percibe\nlee datos del entorno", fc="white")
    _caja(ax, 38, 20, 24, 14, "Decide\nrazona, recuerda y planifica", fc=AZUL, ec=AZUL, tc="white")
    _caja(ax, 72, 20, 24, 14, "Actúa\nusa herramientas y ejecuta", fc="white")
    _caja(ax, 30, 41, 40, 7, "Objetivo y reglas definidos por personas", fc=GRIS, ec=GRIS_L, size=8, negrita_primera=False)
    _caja(ax, 25, 2, 50, 8, "Entorno: usuarios, datos y sistemas", fc=AZUL_P, ec=AZUL_C, size=8.5, negrita_primera=False)
    _flecha(ax, (28, 27), (38, 27))
    _flecha(ax, (62, 27), (72, 27))
    _flecha(ax, (50, 41), (50, 34))
    # retroalimentación: Actúa -> Entorno -> Percibe
    ax.plot([84, 84], [20, 6], color=GRIS_T, lw=1.2)
    _flecha(ax, (84, 6), (75, 6))
    ax.plot([25, 16], [6, 6], color=GRIS_T, lw=1.2)
    _flecha(ax, (16, 6), (16, 20))
    ax.text(88, 12.5, "la acción cambia\nel entorno", fontsize=7.5, color=GRIS_T, ha="left", va="center", style="italic")
    ax.text(12, 13, "nueva\npercepción", fontsize=7.5, color=GRIS_T, ha="right", va="center", style="italic")
    return _guardar(fig, "fig1_ciclo.png")


# --------------------------------------------------------------------------- Figura 2: anatomía
def fig_anatomia() -> pathlib.Path:
    fig, ax = _lienzo(3.9, ymax=60)
    ax.add_patch(FancyBboxPatch((1, 1), 98, 58, boxstyle="round,pad=0,rounding_size=1.5", fc="none", ec=GRIS_T, lw=1, ls=(0, (4, 3))))
    ax.text(3, 59, " Orquestación, límites de seguridad y supervisión humana ", fontsize=8, style="italic", color=GRIS_T,
            ha="left", va="center", bbox=dict(fc="white", ec="none", pad=1.5))
    _caja(ax, 4, 36, 22, 14, "Entrada\nobjetivo y contexto\ndel usuario")
    _caja(ax, 34, 36, 32, 14, "Núcleo: LLM\nmodelo de lenguaje\nrazona, decide y orquesta", fc=AZUL, ec=AZUL, tc="white")
    _caja(ax, 74, 36, 22, 14, "Salida\nrespuesta o acción\nregistrada")
    _flecha(ax, (26, 43), (34, 43))
    _flecha(ax, (66, 43), (74, 43))
    # el núcleo consulta y usa
    ax.plot([50, 50], [36, 30], color=GRIS_T, lw=1.2)
    ax.plot([19, 81], [30, 30], color=GRIS_T, lw=1.2)
    ax.text(48.4, 33, "consulta y usa", fontsize=7.5, style="italic", color=GRIS_T, ha="right", va="center")
    for cx, texto in ((19, "Planificación\ndescompone la meta\ny reordena los pasos"),
                      (50, "Memoria\ninteracciones y\nsoluciones previas"),
                      (81, "Herramientas\nAPIs, bases de datos,\nbúsqueda web, otros agentes")):
        _flecha(ax, (cx, 30), (cx, 24), estilo="<|-|>")
        _caja(ax, cx - 14, 6, 28, 18, texto, fc=AZUL_P, ec=AZUL_C, size=8)
    return _guardar(fig, "fig2_anatomia.png")


# --------------------------------------------------------------------------- Figura 3: patrones
def fig_patrones() -> pathlib.Path:
    fig, axs = plt.subplots(1, 4, figsize=(ANCHO_IN, 1.9), dpi=300)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02, wspace=0.08)
    titulos = ("Agente único", "Vertical", "Horizontal", "Híbrida")
    for ax, titulo in zip(axs, titulos):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(5, 0.3, titulo, ha="center", va="center", fontsize=9, fontweight="bold")

    def nodo(ax, x, y, lider=False, r=0.62):
        ax.add_patch(Circle((x, y), r, fc=AZUL if lider else "white", ec=AZUL if lider else NEGRO, lw=1.2, zorder=3))

    def linea(ax, a, b, ls="-"):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=GRIS_T, lw=1.1, ls=ls, zorder=1)

    # único
    a = axs[0]
    nodo(a, 5, 4.6, r=0.9)
    a.add_patch(Circle((5, 4.6), 0.28, fc=AZUL, ec=AZUL, zorder=4))
    _flecha(a, (0.8, 4.6), (4.0, 4.6))
    _flecha(a, (6.0, 4.6), (9.2, 4.6))
    # vertical
    a = axs[1]
    jefe, hijos = (5, 6.4), [(1.8, 3), (5, 3), (8.2, 3)]
    for h in hijos:
        linea(a, jefe, h)
    nodo(a, *jefe, lider=True)
    for h in hijos:
        nodo(a, *h)
    # horizontal
    a = axs[2]
    pts = [(2, 6.2), (8, 6.2), (2, 2.6), (8, 2.6)]
    for i in range(4):
        for j in range(i + 1, 4):
            linea(a, pts[i], pts[j])
    for p in pts:
        nodo(a, *p)
    # híbrida
    a = axs[3]
    for h in hijos:
        linea(a, jefe, h)
    linea(a, hijos[0], hijos[1], ls=(0, (3, 2)))
    linea(a, hijos[1], hijos[2], ls=(0, (3, 2)))
    nodo(a, *jefe, lider=True)
    for h in hijos:
        nodo(a, *h)
    return _guardar(fig, "fig3_patrones.png")


# --------------------------------------------------------------------------- Figura 4: escalera de tipos
def fig_escalera() -> pathlib.Path:
    fig, ax = _lienzo(3.4, ymax=50)
    nombres = ("Reflejo\nsimple", "Reflejo basado\nen modelo", "Basado en\nobjetivos", "Basado en\nutilidad", "De\naprendizaje")
    notas = ("reglas condición-acción", "memoria y modelo\ndel mundo", "planifica para\nuna meta", "maximiza el\nbeneficio esperado", "mejora con la\nexperiencia")
    colores = ("#E1E4E8", "#C2C8D0", "#98A4B4", AZUL_M, AZUL)
    ancho, sep = 17.5, 1.6
    for i, (nombre, nota, color) in enumerate(zip(nombres, notas, colores)):
        x = 3 + i * (ancho + sep)
        alto = 15 + i * 5
        ax.add_patch(Rectangle((x, 8), ancho, alto, fc=color, ec="none"))
        claro = i >= 3
        tc = "white" if claro else NEGRO
        ax.text(x + 1.2, 8 + alto - 1.6, f"{i + 1}", fontsize=8, family="monospace", color=tc, va="top")
        ax.text(x + ancho / 2, 8 + alto - 5.5, nombre, fontsize=8.5, fontweight="bold", color=tc, ha="center", va="top", linespacing=1.15)
        ax.text(x + ancho / 2, 8 + 2.4, nota, fontsize=7.3, color=tc, ha="center", va="bottom", linespacing=1.15)
    _flecha(ax, (3, 4.5), (97, 4.5), color=GRIS_T)
    ax.text(50, 1.8, "Mayor capacidad de razonamiento y adaptación", fontsize=8, style="italic", color=GRIS_T, ha="center")
    ax.text(3, 47.5, "Los sistemas multiagente pueden combinar los cinco tipos.", fontsize=8, style="italic", color=GRIS_T, ha="left")
    return _guardar(fig, "fig4_escalera.png")


# --------------------------------------------------------------------------- Figura 5: flujo Dynamiq
def fig_dynamiq() -> pathlib.Path:
    fig, ax = _lienzo(2.9, ymax=48)
    _caja(ax, 1, 17, 17, 14, "Consulta\nlegal\nentrante", size=8.5)
    _caja(ax, 25, 17, 19, 14, "Clasificador\nIBM Granite\nde bajo costo", size=8.5)
    _caja(ax, 52, 31, 22, 12, "Caso simple\nno se escala al\nagente más capaz", fc=GRIS, ec=GRIS_L, size=8, ls=(0, (4, 3)))
    _caja(ax, 52, 5, 22, 14, "Agente de\ninvestigación\nmás capaz", fc=AZUL, ec=AZUL, tc="white", size=8.5)
    _caja(ax, 81, 17, 18, 14, "Respuesta\nauditable", size=8.5)
    _flecha(ax, (18, 24), (25, 24))
    # codos dibujados a mano: segmentos rectos y una flecha final horizontal
    for xs, ys in (([44, 48, 48], [27, 27, 37]), ([44, 48, 48], [21, 21, 12]), ([74, 77.5, 77.5], [12, 12, 22])):
        ax.plot(xs, ys, color=GRIS_T, lw=1.2)
    _flecha(ax, (48, 37), (52, 37))
    _flecha(ax, (48, 12), (52, 12))
    _flecha(ax, (77.5, 22), (81, 22))
    ax.text(46.5, 39.5, "sencilla", fontsize=7.5, style="italic", color=GRIS_T, ha="center")
    ax.text(46.5, 8.5, "compleja", fontsize=7.5, style="italic", color=GRIS_T, ha="center")
    return _guardar(fig, "fig5_dynamiq.png")


# --------------------------------------------------------------------------- Figura 6: Agent Arena
ARENA = (  # modelo, laboratorio, mejora neta, margen ±, rango posible, USD/tarea (P50)
    ("Claude Fable 5.1 (Max)", "Anthropic", 14.55, 1.92, "1–4", 4.16),
    ("Claude Opus 5.5 (High)", "Anthropic", 13.78, 2.24, "1–4", 1.56),
    ("GPT 6 Astra (Max)", "OpenAI", 12.18, 2.28, "1–7", 2.91),
    ("GPT 6 Sol (Max)", "OpenAI", 10.65, 2.57, "1–10", 0.92),
    ("Claude Opus 5 (High)", "Anthropic", 8.76, 1.50, "3–10", 2.52),
    ("Claude Opus 5 (Max)", "Anthropic", 8.55, 1.57, "3–10", 3.60),
    ("Claude Fable 5 (High)", "Anthropic", 8.37, 1.30, "4–10", 2.01),
    ("Gemini 4 Argon (High)", "Google", 7.92, 3.24, "3–15", 0.62),
    ("GPT 5.6 Sol (xHigh)", "OpenAI", 7.05, 1.38, "4–11", 1.05),
    ("Claude Opus 4.8 (High)", "Anthropic", 6.92, 1.38, "4–11", 1.36),
)


def fig_arena() -> pathlib.Path:
    fig, ax = plt.subplots(figsize=(ANCHO_IN, 4.1), dpi=300)
    fig.subplots_adjust(left=0.29, right=0.76, top=0.93, bottom=0.12)
    n = len(ARENA)
    for i, (modelo, lab, valor, margen, _rango, costo) in enumerate(ARENA):
        y = n - 1 - i
        ax.barh(y, valor, height=0.55, color="#E1E4E8", zorder=1)
        ax.errorbar(valor, y, xerr=margen, fmt="o", color=AZUL, ecolor=AZUL, elinewidth=1.4, capsize=3, capthick=1.4, ms=5.5, zorder=3)
        ax.text(-0.025, y + 0.1, modelo, ha="right", va="center", fontsize=8, fontweight="bold", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.text(-0.025, y - 0.25, lab, ha="right", va="center", fontsize=7, color=GRIS_T, transform=ax.get_yaxis_transform(), clip_on=False)
        ax.text(1.03, y, f"{valor:.2f} %".replace(".", ","), ha="left", va="center", fontsize=8, transform=ax.get_yaxis_transform(), clip_on=False)
        ax.text(1.28, y, f"{costo:.2f}".replace(".", ","), ha="left", va="center", fontsize=8, transform=ax.get_yaxis_transform(), clip_on=False)
    ax.set_xlim(0, 18)
    ax.set_ylim(-0.7, n - 0.3)
    ax.set_yticks([])
    ax.set_xticks([0, 5, 10, 15])
    ax.set_xticklabels(["0", "5", "10", "15 %"])
    ax.tick_params(axis="x", labelsize=8, colors=GRIS_T, length=3)
    ax.grid(axis="x", color=GRIS_L, lw=0.6, zorder=0)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color(GRIS_L)
    ax.set_xlabel("Mejora neta, con su margen de error (±)", fontsize=8.5, labelpad=4)
    ax.text(1.03, n - 0.35, "Mejora neta", ha="left", va="bottom", fontsize=7.5, color=GRIS_T, transform=ax.get_yaxis_transform())
    ax.text(1.28, n - 0.35, "USD/tarea", ha="left", va="bottom", fontsize=7.5, color=GRIS_T, transform=ax.get_yaxis_transform())
    return _guardar(fig, "fig6_arena.png")


def generar_todas() -> list[pathlib.Path]:
    return [fig_ciclo(), fig_anatomia(), fig_patrones(), fig_escalera(), fig_dynamiq(), fig_arena()]


if __name__ == "__main__":
    for ruta in generar_todas():
        print("figura:", ruta)
