"""Genera el informe Word del Lab 5 «Service Worker» (estilo UMB, APA 7).

Usa el constructor UMB del equipo (estilos reales de TallerBI.docx), las figuras de figuras/ (recortes de capturas reales de Chrome DevTools y
Visual Studio Code) y el contenido de contenido.py. Uso: py generar_informe.py  ->  Lab5_ServiceWorker_Grupo6.docx
"""
from __future__ import annotations

import sys

import contenido as c
from constructor import Documento  # noqa: E402  (la ruta la agrega contenido)

sys.stdout.reconfigure(encoding="utf-8")

TITULO = "Service Worker: caché, modo sin conexión y estrategias de red"
SUBTITULO = "Informe de laboratorio. Guía n.º 5"
AUTORES = ("Rodríguez Ángel, Santiago", "Olaya Rojas, Santiago")
SALIDA = c.AQUI / "Lab5_ServiceWorker_Grupo6.docx"


def portada(doc: Documento) -> None:
    doc.fijar_propiedades(f"{TITULO}: {SUBTITULO}", AUTORES)
    doc.portada_logo(3.0)
    doc.portada_linea()
    doc.portada_linea(TITULO, negrita=True)
    doc.portada_linea(SUBTITULO)
    doc.portada_linea()
    for linea in (*AUTORES, "Universidad Manuela Beltrán", "Ingeniería de Software", "Facultad de Ingeniería",
                  "Nuevas Tecnologías del Desarrollo", "Grupo 6", "Bogotá, Colombia", "2026"):
        doc.portada_linea(linea)
    doc.salto_pagina()


def listas(doc: Documento) -> None:
    doc.rotulo_centrado("Tabla de contenido")
    doc.campo_toc('TOC \\o "1-3" \\h \\z \\u')
    doc.rotulo_centrado("Lista de tablas", salto_antes=True)
    doc.campo_toc('TOC \\h \\z \\t "TITULO TABLA,1"')
    doc.rotulo_centrado("Lista de figuras", salto_antes=True)
    doc.campo_toc('TOC \\h \\z \\t "TITULO FIGURA,1"')


def construir(doc: Documento) -> None:
    portada(doc)
    listas(doc)
    c.introduccion(doc)
    c.marco_conceptual(doc)
    c.entorno(doc)
    c.paso1(doc)
    c.paso2(doc)
    c.paso3(doc)
    c.paso4(doc)
    c.actualizacion(doc)
    c.desafio(doc)
    c.reflexion(doc)
    c.conclusiones(doc)
    c.referencias(doc)


if __name__ == "__main__":
    c.verificar_datos()
    previo = Documento(estricto=False)          # pasada 1: solo registra la numeración (referencias hacia adelante)
    construir(previo)
    doc = Documento(etiquetas=previo.etiquetas, estricto=True)
    construir(doc)
    doc.guardar(SALIDA)
    print(f"docx generado: {SALIDA} | tablas={previo.n_tabla} | figuras={previo.n_figura}")
