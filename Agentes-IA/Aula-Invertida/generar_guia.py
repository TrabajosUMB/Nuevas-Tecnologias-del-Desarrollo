"""Genera la guía de aula invertida diligenciada «Agentes inteligentes de IA» (estilo UMB, APA 7).

Parte A: respuestas individuales de Santiago Rodríguez Ángel (sector Finanzas). Parte B: pre-diseño del equipo con Santiago Olaya Rojas.
Uso: py generar_guia.py  ->  Guia_AulaInvertida_AgentesIA_Rodriguez.docx
"""
from __future__ import annotations

import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import guia_parte_a as A  # noqa: E402
from constructor import Documento  # noqa: E402
from corregir_docx import agregar_referencia, crear_estilo_codigo  # noqa: E402

TITULO = "Guía de aula invertida"
SUBTITULO = "Agentes inteligentes de IA"
AUTOR = "Rodríguez Ángel, Santiago"
EQUIPO = "Rodríguez Ángel, Santiago y Olaya Rojas, Santiago"
SALIDA = AQUI / "Guia_AulaInvertida_AgentesIA_Rodriguez.docx"
NB = "s. f."  # «s. f.» sin salto de línea


def portada(doc: Documento) -> None:
    doc.fijar_propiedades(f"{TITULO}: {SUBTITULO}", AUTOR)
    doc.portada_logo(3.0)
    doc.portada_linea()
    doc.portada_linea(TITULO, negrita=True)
    doc.portada_linea(SUBTITULO)
    doc.portada_linea()
    for linea in (AUTOR, "Universidad Manuela Beltrán", "Ingeniería de Software", "Facultad de Ingeniería",
                  "Nuevas Tecnologías del Desarrollo", "Bogotá, Colombia", "2026"):
        doc.portada_linea(linea)
    doc.salto_pagina()


def listas(doc: Documento) -> None:
    doc.rotulo_centrado("Tabla de contenido")
    doc.campo_toc('TOC \\o "1-3" \\h \\z \\u')
    doc.rotulo_centrado("Lista de tablas", salto_antes=True)
    doc.campo_toc('TOC \\h \\z \\t "TITULO TABLA,1"')
    doc.rotulo_centrado("Lista de figuras", salto_antes=True)
    doc.campo_toc('TOC \\h \\z \\t "TITULO FIGURA,1"')


def identificacion(doc: Documento) -> None:
    doc.titulo(1, "Datos de identificación", salto_antes=True)
    doc.parrafo(
        "Esta guía corresponde a la preparación de la sesión presencial de 3 horas de la asignatura Nuevas Tecnologías del Desarrollo. La Parte A "
        "(actividades A1 a A5) se desarrolló de forma individual, con el sector Finanzas; la Parte B (actividad B1) se coordinó en equipo. La "
        "{T:identificacion} registra los datos de identificación.")
    A.tabla_umb(doc, "identificacion", "Datos de identificación de la guía", ["Campo", "Información"], [
        ("Nombre completo", AUTOR),
        ("Equipo / grupo", EQUIPO),
        ("Sector asignado", "Finanzas"),
        ("Fecha de entrega", "Antes de la sesión presencial. Clase del: ____________________"),
    ], [1.8, 4.7], nota="Elaboración propia.")


# --------------------------------------------------------------------------- Parte B
def parte_b(doc: Documento) -> None:
    doc.titulo(1, "Parte B. Actividad en equipo")
    doc.titulo(2, "Actividad B1. Pre-diseño del agente en equipo: blueprint inicial")
    doc.parrafo(
        "<b>Enunciado.</b> Antes de llegar a clase, el equipo debe tener claridad sobre qué agente van a diseñar y construir. Completen juntos "
        "el siguiente canvas preliminar. El equipo está integrado por Rodríguez Ángel, Santiago y Olaya Rojas, Santiago, ambos con el sector Finanzas.")
    doc.titulo(3, "Paso 1. Elección del agente")
    doc.parrafo("<b>Respuesta.</b> La {T:eleccion} registra la decisión del equipo.")
    A.tabla_umb(doc, "eleccion", "Elección del agente que diseñará el equipo", ["Aspecto", "Decisión"], [
        ("Nombre del agente que van a diseñar", "Guardián Antifraude."),
        ("Sector elegido (salud / finanzas / educación / comercio)", "Finanzas."),
        ("¿Por qué eligieron este agente?",
         "El fraude digital es un problema frecuente y de alto impacto para los clientes de un banco. Permite aplicar los conceptos de la guía "
         "(percepción, razonamiento, herramientas y límites éticos), se puede construir y probar en la sesión solo con prompting y escenarios "
         "simulados, sin datos reales, y se relaciona con el caso de detección de fraude analizado en la Actividad A2."),
        ("¿Tomaron como base alguno investigado? ¿Cuál?",
         "Sí. Se tomó como base a Erica, de Bank of America (Actividad A3), en la orientación proactiva y personalizada y en la derivación a "
         "especialistas humanos. Agente investigado por Olaya Rojas, Santiago: ____________________."),
    ], [2.0, 4.5], tam=9.5, nota="Elaboración propia.")
    doc.titulo(3, "Paso 2. Canvas del agente (pre-diseño)")
    doc.parrafo("<b>Respuesta.</b> La {T:canvas} presenta el pre-diseño del agente, que se refinará y ampliará en la sesión.")
    A.tabla_umb(doc, "canvas", "Canvas preliminar del agente «Guardián Antifraude»", ["Elemento", "Pre-diseño"], [
        ("Objetivo principal del agente",
         "Ayudar a clientes de un banco a reconocer posibles fraudes (phishing, smishing, vishing y suplantación) y a actuar de forma segura, "
         "escalando a una persona cuando el riesgo sea alto."),
        ("Entorno y datos que percibe (entradas)",
         "En el taller: texto que el usuario pega (mensajes, correos, enlaces sin abrir, descripción de una transacción o de una llamada) y un "
         "contexto simulado del cliente. En producción: eventos de transacciones, dispositivo, ubicación, historial y listas de comercios y "
         "enlaces maliciosos."),
        ("Modelo de razonamiento (¿cómo decide?)",
         "Agente deliberativo con rasgos de aprendizaje: evalúa señales (urgencia, enlaces acortados, petición de claves, montos inusuales) con una "
         "lista de verificación, asigna un nivel de sospecha (bajo, medio o alto) y decide la recomendación. Sigue el ciclo pensar, actuar y "
         "observar de ReAct cuando usa herramientas y se ajusta con la retroalimentación del evaluador."),
        ("Herramientas necesarias (API, bases de datos, sensores)",
         "En el taller: base de conocimiento de patrones de fraude en el prompt o como archivo adjunto, lista de verificación de señales y plantilla "
         "de respuesta. En producción: API de transacciones, motor de reglas, servicio de reputación de enlaces, base de casos confirmados y canal "
         "de escalamiento a analistas."),
        ("Acciones y salidas (¿qué hace?)",
         "Entrega el nivel de sospecha, las señales detectadas, los pasos inmediatos (no abrir el enlace, bloquear la tarjeta, llamar a la línea "
         "oficial) y cómo verificar por un canal oficial. En riesgo alto, deriva a un analista humano."),
        ("Restricciones éticas (¿qué NO debe hacer?)",
         "No pide ni guarda claves, PIN, CVV, códigos OTP ni datos completos de tarjetas o documentos; no afirma con certeza si algo es fraude; no da "
         "asesoría de inversión ni ayuda a cometer fraude; informa que es un sistema automatizado y minimiza los datos que usa."),
        ("Métricas de éxito (¿cómo sabemos que funciona?)",
         "Porcentaje de casos de prueba con el nivel de sospecha esperado (meta de al menos 90 % en los escenarios del taller); tasas de falsos "
         "positivos y falsos negativos; ninguna solicitud de datos sensibles por parte del agente; porcentaje de respuestas que incluyen un canal "
         "oficial de verificación; y claridad de las respuestas según la rúbrica del evaluador."),
    ], [1.9, 4.6], tam=9.5, nota="Elaboración propia. Las metas numéricas son una propuesta inicial del equipo.")
    doc.titulo(3, "Paso 3. Roles del equipo para la sesión")
    doc.parrafo(
        "<b>Respuesta.</b> Con dos integrantes, cada uno asume dos roles, que pueden rotar durante la sesión. La {T:roles} muestra la asignación.")
    A.tabla_umb(doc, "roles", "Roles del equipo para la sesión presencial", ["Rol", "Responsabilidad", "Integrante asignado"], [
        ("Líder / coordinador", "Coordina los tiempos y modera las decisiones del equipo.", "Rodríguez Ángel, Santiago"),
        ("Diseñador", "Documenta el canvas y el flujo del agente.", "Olaya Rojas, Santiago"),
        ("Prompt engineer", "Escribe y prueba el system prompt en la IA.", "Rodríguez Ángel, Santiago"),
        ("Evaluador", "Aplica la rúbrica y documenta los resultados.", "Olaya Rojas, Santiago"),
    ], [1.5, 3.0, 2.0], nota="Elaboración propia.")
    doc.titulo(3, "Paso 4. Preguntas que llevan a la sesión")
    doc.parrafo("<b>Respuesta.</b> El equipo llevará tres dudas técnicas para resolver con el docente.")
    doc.parrafo(
        "<b>Pregunta 1.</b> ¿Cómo evaluar de forma objetiva a un agente cuyas respuestas no son siempre iguales ante la misma entrada? ¿Cuántas "
        "repeticiones por caso de prueba y qué criterios se recomiendan?")
    doc.parrafo(
        "<b>Pregunta 2.</b> ¿Cómo evitar que el system prompt sea ignorado o manipulado (inyección de prompt) cuando el usuario escribe "
        "instrucciones contradictorias, y qué pruebas conviene incluir para comprobarlo?")
    doc.parrafo(
        "<b>Pregunta 3.</b> ¿Hasta dónde puede llegar un agente de orientación sobre fraude sin convertirse en asesoría financiera personalizada, "
        "y cómo se documenta ese límite para el usuario?")


# --------------------------------------------------------------------------- Rúbrica y referencias
def rubrica(doc: Documento) -> None:
    doc.titulo(1, "Rúbrica de evaluación", salto_antes=True)
    doc.parrafo("El docente evaluará esta guía al inicio de la sesión; la calificación forma parte de la nota del taller ({T:rubrica}).")
    A.tabla_umb(doc, "rubrica", "Rúbrica de evaluación de la guía de aula invertida",
                ["Criterio", "Excelente (4)", "Bueno (3)", "Regular (2)", "Insuficiente (1)", "Pts."], [
        ("A1. Comprensión conceptual", "Definición propia, tabla completa con ejemplos originales, diagrama detallado",
         "Definición correcta, tabla con algunos ejemplos propios, diagrama básico",
         "Definición copiada o imprecisa, tabla incompleta, sin diagrama", "No realizada o incoherente", ""),
        ("A2. Tipos de agentes", "Tabla completa con análisis claro, argumentación sólida del tipo para fraudes",
         "Tabla mayormente completa, argumentación con algunos vacíos", "Tabla incompleta, argumentación superficial", "No realizada", ""),
        ("A3. Investigación de caso real", "Ficha completa con fuentes, análisis crítico profundo de ética y mejoras",
         "Ficha completa, análisis ético básico pero coherente", "Ficha incompleta, análisis superficial sin argumentos", "No realizada o sin fuentes", ""),
        ("A4. Reflexión ética", "Reflexión profunda con posiciones claras, aplica conceptos de clase y regulación",
         "Reflexión adecuada con algunos argumentos sólidos", "Reflexión superficial, no aplica conceptos de clase", "No realizada o fuera de tema", ""),
        ("A5. Prompting técnico", "Errores identificados, system prompt excelente, 5 casos borde completos",
         "Errores identificados, buen system prompt, casos borde básicos", "Errores parcialmente identificados, prompt incompleto", "No realizada", ""),
        ("B1. Pre-diseño en equipo", "Canvas completo, roles claros, preguntas relevantes y bien formuladas",
         "Canvas mayormente completo, roles asignados, preguntas básicas", "Canvas incompleto, roles no claros, pocas preguntas",
         "No realizada o sin evidencia de trabajo en equipo", ""),
        ("Total", "", "", "", "", "/ 24"),
    ], [1.15, 1.45, 1.3, 1.25, 1.0, 0.45], alinear=["l", "l", "l", "l", "l", "c"], tam=8.5,
        nota="Rúbrica del docente de la asignatura; la columna de puntos queda en blanco para su calificación.")
    doc.parrafo("Calificación total de la guía: _____ / 24 puntos; equivale a: _____ / 5.0.")


def referencias(doc: Documento) -> None:
    doc.titulo(1, "Referencias", salto_antes=True)
    bofa = "https://newsroom.bankofamerica.com/content/newsroom/press-releases/"
    refs = (
        [("Bank of America. (2025, 20 de agosto). ", False),
         ("A decade of AI innovation: BofA's virtual assistant Erica surpasses 3 billion client interactions", True),
         (f" [Comunicado de prensa]. {bofa}2025/08/a-decade-of-ai-innovation--bofa-s-virtual-assistant-erica-surpas.html", False)],
        [("Bank of America. (2026, 10 de marzo). ", False), ("BofA AI and digital innovations fuel 30 billion client interactions", True),
         (f" [Comunicado de prensa]. {bofa}2026/03/bofa-ai-and-digital-innovations-fuel-30-billion-client-interacti.html", False)],
        [("Congreso de la República de Colombia. (2008, 31 de diciembre). ", False),
         ("Ley 1266 de 2008, por la cual se dictan las disposiciones generales del hábeas data y se regula el manejo de la información contenida en "
          "bases de datos personales, en especial la financiera, crediticia, comercial, de servicios y la proveniente de terceros países y se dictan "
          "otras disposiciones", True),
         (". https://www.secretariasenado.gov.co/senado/basedoc/ley_1266_2008.html", False)],
        [("Congreso de la República de Colombia. (2012, 17 de octubre). ", False),
         ("Ley 1581 de 2012, por la cual se dictan disposiciones generales para la protección de datos personales", True),
         (". https://www.secretariasenado.gov.co/senado/basedoc/ley_1581_2012.html", False)],
        [(f"Future of Life Institute. ({NB}-a). ", False), ("Article 14: Human oversight", True),
         (". EU Artificial Intelligence Act. https://artificialintelligenceact.eu/article/14/", False)],
        [(f"Future of Life Institute. ({NB}-b). ", False), ("Article 26: Obligations of deployers of high-risk AI systems", True),
         (". EU Artificial Intelligence Act. https://artificialintelligenceact.eu/article/26/", False)],
        [(f"Future of Life Institute. ({NB}-c). ", False), ("Article 6: Classification rules for high-risk AI systems", True),
         (". EU Artificial Intelligence Act. https://artificialintelligenceact.eu/article/6/", False)],
        [(f"Gutowska, A. ({NB}). ", False), ("What are AI agents?", True), (" IBM Think. https://www.ibm.com/think/topics/ai-agents", False)],
        [(f"IBM. ({NB}-a). ", False), ("Types of AI agents", True), (". IBM Think. https://www.ibm.com/think/topics/ai-agent-types", False)],
        [(f"IBM. ({NB}-b). ", False), ("What is agentic architecture?", True), (" IBM Think. https://www.ibm.com/think/topics/agentic-architecture", False)],
        [(f"Intersoft Consulting. ({NB}-a). ", False), ("Art. 22 GDPR: Automated individual decision-making, including profiling", True),
         (". General Data Protection Regulation (GDPR). https://gdpr-info.eu/art-22-gdpr/", False)],
        [(f"Intersoft Consulting. ({NB}-b). ", False), ("Art. 9 GDPR: Processing of special categories of personal data", True),
         (". General Data Protection Regulation (GDPR). https://gdpr-info.eu/art-9-gdpr/", False)],
        [("Russell, S., y Norvig, P. (2021). ", False), ("Artificial intelligence: A modern approach", True), (" (4.ª ed.). Pearson.", False)],
    )
    for partes in refs:
        agregar_referencia(doc.d, partes)


def construir(doc: Documento) -> None:
    crear_estilo_codigo(doc.d)
    portada(doc)
    listas(doc)
    identificacion(doc)
    A.actividad_a1(doc)
    A.actividad_a2(doc)
    A.actividad_a3(doc)
    A.actividad_a4(doc)
    A.actividad_a5(doc)
    parte_b(doc)
    rubrica(doc)
    referencias(doc)


if __name__ == "__main__":
    previo = Documento(estricto=False)          # pasada 1: registra la numeración (referencias hacia adelante)
    construir(previo)
    doc = Documento(etiquetas=previo.etiquetas, estricto=True)
    construir(doc)
    doc.guardar(SALIDA)
    print(f"docx generado: {SALIDA} | tablas={previo.n_tabla} | figuras={previo.n_figura}")
