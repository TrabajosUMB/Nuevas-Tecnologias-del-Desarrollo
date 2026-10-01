"""Genera el informe Word «Agentes inteligentes de inteligencia artificial» (estilo UMB, APA 7).

Documento de apoyo a la presentación Presentacion_Agentes_Inteligentes.html. Usa el constructor UMB del equipo
(estilos reales de TallerBI.docx). Uso: py generar_informe.py  ->  Informe_Agentes_Inteligentes_IA.docx
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, r"C:\Users\cuent\Documents\Universidad\Katherin\2026-02\Sistemas Transaccionales\herramientas_doc\build")
sys.path.insert(0, r"C:\Users\cuent\.claude\skills\umb-documento\references")
sys.stdout.reconfigure(encoding="utf-8")

from constructor import Documento  # noqa: E402
from corregir_docx import agregar_referencia, cabecera_azul  # noqa: E402

import figuras  # noqa: E402

AQUI = pathlib.Path(__file__).parent
FIG = AQUI / "figuras"
TITULO = "Agentes inteligentes de inteligencia artificial"
SUBTITULO = "Informe de la presentación"
AUTORES = ("Rodríguez Ángel, Santiago", "Olaya Rojas, Santiago")
SALIDA = AQUI / "Informe_Agentes_Inteligentes_IA.docx"


def tabla_umb(doc: Documento, *args, **kwargs):
    """Tabla APA con encabezado azul UMB."""
    t = doc.tabla(*args, **kwargs)
    cabecera_azul(t)
    return t


# --------------------------------------------------------------------------- portada e índices
def portada(doc: Documento) -> None:
    doc.fijar_propiedades(f"{TITULO}: {SUBTITULO}", AUTORES)
    doc.portada_logo(3.0)
    doc.portada_linea()
    doc.portada_linea(TITULO, negrita=True)
    doc.portada_linea(SUBTITULO)
    doc.portada_linea()
    for linea in (*AUTORES, "Universidad Manuela Beltrán", "Ingeniería de Software", "Facultad de Ingeniería",
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


def introduccion(doc: Documento) -> None:
    doc.titulo(1, "Introducción", salto_antes=True)
    doc.parrafo(
        "Los agentes inteligentes de inteligencia artificial (IA) pasaron de ser un concepto de la investigación académica a una herramienta "
        "que organizaciones de distintos sectores emplean para automatizar tareas complejas. A diferencia de un modelo de lenguaje que solo "
        "responde a una consulta, un agente puede planificar, usar herramientas externas y corregir su propio plan para alcanzar un objetivo "
        "(Gutowska, s.\u00a0f.).")
    doc.parrafo(
        "Este documento recoge y amplía el contenido de la presentación «Agentes inteligentes de IA», elaborada para la asignatura Nuevas "
        "Tecnologías del Desarrollo. Se organiza en seis bloques: qué es un agente inteligente, principios clave, arquitectura, tipos de "
        "agentes, aplicaciones reales y un ejemplo. El apoyo principal es la documentación divulgativa de IBM (Gutowska, s.\u00a0f.; IBM, s.\u00a0f.-a, "
        "s.\u00a0f.-b, s.\u00a0f.-c), complementada con la definición clásica de agente de Russell y Norvig (2021) y con los datos del ranking Agent Arena "
        "(Arena, 2026).")
    doc.parrafo(
        "Conviene precisar el alcance. Las cifras de resultados de la sección 5 son las que publica IBM y no fueron verificadas de forma "
        "independiente. Los datos del ranking de la sección 6 corresponden al 30 de septiembre de 2026 y cambian a medida que se registran "
        "nuevas sesiones. Las lecturas que no provienen de las fuentes se identifican como interpretación de los autores.")


# --------------------------------------------------------------------------- 1. Qué es un agente inteligente
def seccion1(doc: Documento) -> None:
    doc.titulo(1, "1. ¿Qué es un agente inteligente?")
    doc.titulo(2, "1.1 Definición")
    doc.parrafo(
        "Un agente de IA es, según IBM, un sistema que realiza tareas de forma autónoma al diseñar flujos de trabajo con las herramientas "
        "disponibles (Gutowska, s.\u00a0f.). La definición se alinea con la tradición clásica del área, en la que un agente es todo aquello que "
        "percibe su entorno mediante sensores y actúa sobre él mediante actuadores (Russell y Norvig, 2021). En ambos casos el elemento "
        "central es un ciclo: el agente percibe, decide y actúa, y el resultado de su acción modifica el entorno y produce una nueva "
        "percepción ({F:ciclo}).")
    doc.figura("ciclo", "Ciclo de un agente inteligente", FIG / "fig1_ciclo.png",
               nota="Elaboración propia con base en Gutowska (s.\u00a0f.) y Russell y Norvig (2021).")
    doc.parrafo(
        "En los agentes actuales ese ciclo se apoya en un modelo de lenguaje de gran tamaño (LLM, por sus siglas en inglés). Un LLM "
        "tradicional, como los modelos Granite de IBM, genera sus respuestas a partir de los datos con los que fue entrenado y queda limitado "
        "por ese conocimiento. El agente, en cambio, emplea la llamada de herramientas en segundo plano para obtener información actualizada, "
        "optimizar flujos de trabajo y crear subtareas de forma autónoma (Gutowska, s.\u00a0f.).")
    doc.parrafo(
        "La autonomía del agente no es absoluta. Requiere metas y reglas definidas por personas, y su comportamiento depende de tres "
        "influencias: el equipo que diseña y entrena el sistema, el equipo que lo despliega y da acceso a los usuarios, y el usuario que "
        "fija los objetivos y establece las herramientas disponibles (Gutowska, s.\u00a0f.).")
    doc.titulo(2, "1.2 Agente frente a chatbot no agéntico")
    doc.parrafo(
        "Los chatbots de IA emplean técnicas de procesamiento de lenguaje natural para entender las preguntas del usuario y automatizar las "
        "respuestas. IBM precisa que el chatbot es una modalidad de interacción, mientras que la agencia es un marco tecnológico; por eso un "
        "chatbot puede ser agéntico o no serlo (Gutowska, s.\u00a0f.). La {T:chatbot} contrasta ambos casos.")
    tabla_umb(doc, "chatbot", "Chatbot no agéntico frente a agente de IA", ["Capacidad", "Chatbot no agéntico", "Agente de IA"], [
        ("Herramientas", "No dispone de herramientas.", "Llama APIs, bases de datos, búsquedas web y otros agentes."),
        ("Memoria", "No conserva lo aprendido.", "Guarda interacciones pasadas y se adapta al usuario."),
        ("Razonamiento y planificación", "Solo alcanza objetivos de corto plazo y no planifica.", "Descompone la meta en subtareas y corrige su plan."),
        ("Autonomía", "Necesita entrada continua del usuario.", "Completa tareas complejas sin intervención continua."),
        ("Aprendizaje", "No aprende de sus errores.", "Refina sus respuestas con retroalimentación."),
    ], [1.5, 2.4, 2.6], nota="Elaboración propia con base en Gutowska (s.\u00a0f.).", negrita_primera_col=True, sombrear_primera_col=True)
    doc.parrafo(
        "IBM señala que los chatbots no agénticos responden bien a consultas comunes, pero rinden mal con preguntas propias del usuario y de "
        "sus datos, y que no aprenden de sus errores porque no tienen memoria (Gutowska, s.\u00a0f.).")


# --------------------------------------------------------------------------- 2. Principios clave
def seccion2(doc: Documento) -> None:
    doc.titulo(1, "2. Principios clave")
    doc.titulo(2, "2.1 Funcionamiento en tres etapas")
    doc.parrafo("IBM describe el funcionamiento de un agente en tres etapas (Gutowska, s.\u00a0f.).")
    doc.parrafo(
        "<b>Inicialización de objetivos y planificación.</b> Aunque decide con autonomía, el agente parte de metas y reglas que definen las "
        "personas. Con ellas y con las herramientas disponibles realiza una descomposición de tareas: arma un plan de tareas y subtareas para "
        "alcanzar el objetivo complejo. En tareas simples la planificación no es necesaria, y el agente puede reflexionar sobre sus "
        "respuestas y mejorarlas sin planificar los pasos siguientes.")
    doc.parrafo(
        "<b>Razonamiento con herramientas.</b> Como el agente no tiene todo el conocimiento que necesita, acude a conjuntos de datos externos, "
        "búsquedas web, interfaces de programación (API) e incluso otros agentes. Cuando obtiene la información faltante, actualiza su base de "
        "conocimiento y razona de nuevo: reevalúa de forma continua su plan y se autocorrige, lo que permite decisiones más informadas y "
        "adaptativas.")
    doc.parrafo(
        "<b>Aprendizaje y reflexión.</b> El agente usa mecanismos de retroalimentación, como otros agentes o la intervención humana "
        "(human-in-the-loop), para mejorar la precisión de sus respuestas. Este proceso se conoce como refinamiento iterativo, y el agente puede "
        "guardar en una base de conocimiento las soluciones a obstáculos anteriores para no repetir errores.")
    doc.parrafo(
        "Como ilustración, IBM plantea a un usuario que pide predecir qué semana del próximo año tendrá el mejor clima para surfear en "
        "Grecia. El agente no puede resolverlo solo con su conocimiento interno: consulta una base de datos con reportes diarios del clima de "
        "los últimos años y luego se comunica con un agente especializado en surf, que le indica que las mareas altas y el clima soleado con "
        "poca lluvia son las mejores condiciones. Con esa información identifica patrones y presenta su predicción; después almacena lo "
        "aprendido junto con la retroalimentación del usuario (Gutowska, s.\u00a0f.).")
    doc.titulo(2, "2.2 Seis capacidades que sostienen al agente")
    doc.parrafo(
        "A partir de la descripción de IBM es posible sintetizar seis capacidades que sostienen el comportamiento de un agente ({T:capacidades}). "
        "Se trata de una síntesis de los autores y no de una lista textual de la fuente.")
    tabla_umb(doc, "capacidades", "Capacidades que sostienen el comportamiento de un agente", ["Capacidad", "Qué significa", "Fundamento en IBM"], [
        ("Autonomía", "Decide y actúa sin supervisión constante, con metas y reglas definidas por personas.",
         "Los agentes son autónomos en su toma de decisiones, pero requieren metas y reglas humanas."),
        ("Percepción", "Basa sus acciones en la información que percibe del entorno y de sus herramientas.",
         "Las acciones del agente se basan en la información que percibe."),
        ("Razonamiento", "Evalúa lo que sabe, detecta lo que le falta y elige la siguiente acción.",
         "Razonamiento agéntico: reevalúa su plan y se autocorrige."),
        ("Planificación", "Descompone objetivos complejos en tareas y subtareas y ajusta el plan.",
         "Descomposición de tareas en un plan de tareas y subtareas."),
        ("Memoria", "Guarda interacciones y soluciones previas para personalizar y no repetir errores.",
         "Almacena interacciones pasadas y soluciones a obstáculos anteriores."),
        ("Uso de herramientas", "Accede a datos actualizados mediante APIs, búsquedas y otros agentes.",
         "Llamada de herramientas en segundo plano, sin intervención humana."),
    ], [1.3, 2.9, 2.3], nota="Síntesis de los autores a partir de Gutowska (s.\u00a0f.) e IBM (s.\u00a0f.-c).", negrita_primera_col=True, sombrear_primera_col=True)
    doc.titulo(2, "2.3 Paradigmas de razonamiento: ReAct y ReWOO")
    doc.parrafo(
        "IBM aclara que no existe una arquitectura estándar única para construir agentes: hay varios paradigmas para resolver problemas de "
        "varios pasos (Gutowska, s.\u00a0f.). Dos de los más conocidos son ReAct y ReWOO ({T:razonamiento}).")
    doc.parrafo(
        "En el paradigma ReAct (reasoning and action) se instruye al agente para que piense y planifique después de cada acción y de cada "
        "respuesta de una herramienta, y así decida cuál usar a continuación. Estos ciclos, llamados «pensar, actuar, observar» (Think-Act-Observe), "
        "resuelven el problema paso a paso y mejoran las respuestas de forma iterativa. Mediante la estructura del prompt puede pedirse al "
        "agente que razone con calma y muestre cada pensamiento, lo que da visibilidad sobre cómo formula su respuesta (Gutowska, s.\u00a0f.).")
    doc.parrafo(
        "ReWOO (reasoning without observation) elimina la dependencia de los resultados de las herramientas para planificar. El agente "
        "anticipa desde el inicio qué herramientas usará, lo que evita usos redundantes y permite que la persona confirme el plan antes de "
        "ejecutarlo. Su flujo tiene tres módulos: planificación, recolección de las salidas de las herramientas y combinación del plan con "
        "esas salidas para formular la respuesta. Planificar por adelantado puede reducir de forma importante el uso de tokens, la complejidad "
        "computacional y las consecuencias de un fallo intermedio de una herramienta (Gutowska, s.\u00a0f.).")
    tabla_umb(doc, "razonamiento", "Comparación entre los paradigmas ReAct y ReWOO", ["Aspecto", "ReAct", "ReWOO"], [
        ("Ciclo", "Pensar, actuar y observar, en bucle.", "Planificar, llamar herramientas y responder."),
        ("Cuándo planifica", "Después de cada acción y de cada respuesta de una herramienta.", "Una sola vez, al inicio."),
        ("Dependencia de las salidas de las herramientas", "Alta: cada resultado orienta el paso siguiente.", "Ninguna para planificar: anticipa las herramientas que usará."),
        ("Ventaja señalada", "Resolución paso a paso y mejora iterativa.", "Menor uso de tokens y de complejidad; evita usos redundantes."),
        ("Control humano", "Puede mostrarse cada pensamiento del agente.", "La persona puede confirmar el plan antes de la ejecución."),
    ], [1.7, 2.4, 2.4], nota="Elaboración propia con base en Gutowska (s.\u00a0f.).", negrita_primera_col=True, sombrear_primera_col=True)


# --------------------------------------------------------------------------- 3. Arquitectura
def seccion3(doc: Documento) -> None:
    doc.titulo(1, "3. Arquitectura de los agentes de IA")
    doc.titulo(2, "3.1 Anatomía de un agente")
    doc.parrafo(
        "IBM define la arquitectura agéntica como la estructura y el diseño de los marcos de trabajo de IA agéntica: la que moldea el espacio "
        "virtual y la estructura del flujo de trabajo para automatizar los modelos de IA dentro de un sistema agéntico (IBM, s.\u00a0f.-c). Su "
        "propósito es dar una estructura a un LLM para que automatice agentes capaces de completar tareas complejas. Esa arquitectura debe "
        "incluir componentes que atiendan los cuatro factores de la agencia: intencionalidad (planificación), previsión, autorreactividad y "
        "autorreflexión, que permiten al agente fijar metas, planificar, monitorear su desempeño y reflexionar para alcanzarlas (IBM, s.\u00a0f.-c).")
    doc.parrafo(
        "La {F:anatomia} resume los componentes. El núcleo es el LLM, que razona y decide. En torno a él, la planificación descompone la meta, "
        "la memoria conserva interacciones y soluciones previas, y las herramientas dan acceso a APIs, bases de datos, búsqueda web y otros "
        "agentes. El conjunto opera dentro de una capa de orquestación, que gestiona el comportamiento de los agentes, y de límites de "
        "seguridad y supervisión humana, que IBM recomienda para las acciones de alto impacto (Gutowska, s.\u00a0f.; IBM, s.\u00a0f.-c).")
    doc.figura("anatomia", "Componentes de un agente de IA", FIG / "fig2_anatomia.png",
               nota="Esquema elaborado por los autores con base en IBM (s.\u00a0f.-c) y Gutowska (s.\u00a0f.).")
    doc.titulo(2, "3.2 Patrones de arquitectura")
    doc.parrafo(
        "IBM distingue los sistemas de un solo agente de los multiagente y, dentro de estos últimos, tres patrones de organización: vertical, "
        "horizontal e híbrido (IBM, s.\u00a0f.-c). La {F:patrones} los representa y la {T:patrones} resume sus características.")
    doc.parrafo(
        "En la arquitectura de agente único, una sola entidad autónoma toma decisiones centralizadas en su entorno. Es más simple, predecible, "
        "rápida y económica, pero tiene escalabilidad limitada, porque puede convertirse en un cuello de botella, y es rígida ante tareas que "
        "exigen varios pasos o coordinación entre dominios (IBM, s.\u00a0f.-c).")
    doc.parrafo(
        "Las arquitecturas multiagente, en cambio, hacen que cada agente se especialice en un dominio y colabore con los demás para resolver "
        "problemas complejos. Un agente puede usar procesamiento de lenguaje natural, otro visión por computador y otro generación aumentada "
        "por recuperación (RAG), lo que las hace más flexibles. Entre los marcos para construirlas, IBM menciona crewAI, un marco en Python "
        "que opera sobre LangChain, y MetaGPT, de DeepWisdom, que sigue un flujo estructurado guiado por procedimientos operativos estándar "
        "(IBM, s.\u00a0f.-c).")
    doc.figura("patrones", "Patrones de organización de los agentes", FIG / "fig3_patrones.png",
               nota="Representación simplificada elaborada por los autores con base en IBM (s.\u00a0f.-c). El nodo azul indica al agente líder.")
    tabla_umb(doc, "patrones", "Patrones de arquitectura de agentes", ["Patrón", "Estructura", "Fortalezas", "Limitaciones", "Ideal para"], [
        ("Agente único", "Una sola entidad autónoma decide de forma centralizada.", "Simple, predecible, rápido y económico.",
         "Poca escalabilidad; rígido y limitado a un dominio.", "Chatbots simples y sistemas de recomendación."),
        ("Vertical", "Un agente líder supervisa las subtareas y los demás le reportan.", "Eficiente en flujos secuenciales; responsabilidad clara.",
         "Cuello de botella y punto único de falla.", "Flujos con aprobaciones en varios pasos; generación de documentos."),
        ("Horizontal", "Agentes pares colaboran sin jerarquía y deciden en grupo.", "Resolución dinámica de problemas y procesamiento en paralelo.",
         "Coordinación compleja y decisiones más lentas.", "Lluvia de ideas y problemas interdisciplinarios."),
        ("Híbrida", "Combina liderazgo estructurado con colaboración; el liderazgo cambia según la tarea.", "Versatilidad y adaptabilidad.",
         "Mayor complejidad y exigencia de recursos.", "Planeación estratégica y procesos dinámicos."),
    ], [0.9, 1.7, 1.45, 1.35, 1.4], tam=9, nota="Elaboración propia con base en IBM (s.\u00a0f.-c).", negrita_primera_col=True, sombrear_primera_col=True)
    doc.titulo(2, "3.3 Marcos según la forma de razonar")
    doc.parrafo(
        "Además de la organización de los agentes, IBM describe marcos agénticos según la forma en que razonan (IBM, s.\u00a0f.-c). La "
        "<b>arquitectura reactiva</b> asocia cada situación directamente con una acción: decide a partir de estímulos inmediatos del entorno, "
        "sin memoria ni capacidad de predicción, por lo que no aprende del pasado ni planifica el futuro. La <b>arquitectura deliberativa</b> "
        "decide con base en razonamiento, planificación y modelos internos del mundo; a diferencia de la reactiva, analiza el entorno, predice "
        "resultados y elige antes de actuar. La <b>arquitectura cognitiva</b> imita el pensamiento, el razonamiento, el aprendizaje y la toma "
        "de decisiones humanos mediante módulos de percepción, memoria, razonamiento y adaptación; IBM la considera el tipo más avanzado, "
        "capaz de operar en entornos complejos e inciertos y de mejorar con el tiempo.")
    doc.parrafo(
        "Un ejemplo de arquitectura cognitiva es el modelo BDI (belief-desire-intention), que representa la decisión racional con tres "
        "elementos: las creencias, que son el conocimiento que el agente tiene del mundo («la puerta está cerrada»); los deseos, que son sus "
        "objetivos de alto nivel («quiero entrar al cuarto»); y las intenciones, que son el curso de acción con el que se compromete («abriré "
        "la puerta») (IBM, s.\u00a0f.-c).")


# --------------------------------------------------------------------------- 4. Tipos de agentes
def seccion4(doc: Documento) -> None:
    doc.titulo(1, "4. Tipos de agentes")
    doc.titulo(2, "4.1 Los cinco tipos")
    doc.parrafo(
        "IBM clasifica los agentes en cinco tipos, del más simple al más avanzado (Gutowska, s.\u00a0f.; IBM, s.\u00a0f.-b). Un agente simple puede ser "
        "preferible para objetivos sencillos, porque evita una complejidad computacional innecesaria (Gutowska, s.\u00a0f.). La {F:escalera} ilustra "
        "la progresión y la {T:tipos} resume cada tipo.")
    doc.figura("escalera", "Los cinco tipos de agentes, de lo simple a lo avanzado", FIG / "fig4_escalera.png",
               nota="Elaboración propia con base en IBM (s.\u00a0f.-b) y Gutowska (s.\u00a0f.).")
    tabla_umb(doc, "tipos", "Características de los cinco tipos de agentes", ["Tipo", "Cómo decide", "Ejemplo", "Limitación"], [
        ("1. Reflejo simple", "Aplica reglas condición-acción predefinidas a la percepción actual; no guarda memoria.",
         "Termostato que enciende la calefacción cuando la temperatura baja de un umbral.",
         "Falla en escenarios dinámicos o complejos y puede repetir los mismos errores."),
        ("2. Reflejo basado en modelo", "Mantiene un modelo interno del mundo que actualiza con cada percepción y lo usa junto con sus reglas.",
         "Aspiradora robot que esquiva muebles y recuerda las áreas ya limpiadas.",
         "Carece de razonamiento o aprendizaje avanzados para problemas complejos."),
        ("3. Basado en objetivos", "Tiene una meta y usa planificación y razonamiento para elegir las acciones que lo acercan a ella.",
         "Sistema de navegación que recomienda la ruta más rápida al destino.",
         "Complejidad limitada: suele apoyarse en estrategias o árboles de decisión preprogramados."),
        ("4. Basado en utilidad", "Asigna un valor de utilidad a cada resultado posible y elige la acción que maximiza el beneficio esperado.",
         "Vehículo autónomo que equilibra velocidad, eficiencia de combustible y seguridad.",
         "Es difícil crear funciones de utilidad precisas y confiables."),
        ("5. De aprendizaje", "Incorpora experiencias nuevas a su conocimiento de forma autónoma; puede razonar por objetivos o por utilidad.",
         "Recomendaciones personalizadas en sitios de comercio electrónico.",
         "Su mejora depende de la retroalimentación que recibe del entorno."),
    ], [1.15, 2.0, 1.75, 1.6], tam=9.5, nota="Elaboración propia con base en IBM (s.\u00a0f.-b) y Gutowska (s.\u00a0f.). La limitación del agente de aprendizaje es una "
                                              "deducción de los autores a partir de su definición.", negrita_primera_col=True, sombrear_primera_col=True)
    doc.parrafo(
        "Los agentes de aprendizaje se componen de cuatro elementos: el elemento de aprendizaje, que mejora el conocimiento a partir de la "
        "experiencia; el crítico, que indica si la calidad de las respuestas cumple el estándar; el elemento de desempeño, que selecciona las "
        "acciones; y el generador de problemas, que propone acciones exploratorias (Gutowska, s.\u00a0f.; IBM, s.\u00a0f.-b). En el aprendizaje por "
        "refuerzo, por ejemplo, el agente prueba estrategias y recibe recompensas por las acciones correctas.")
    doc.titulo(2, "4.2 Sistemas multiagente y jerárquicos")
    doc.parrafo(
        "A medida que los sistemas de IA se vuelven más complejos aparecen los agentes jerárquicos, diseñados para dividir problemas complejos "
        "en subtareas manejables: los agentes de nivel superior se ocupan de los objetivos generales y los de nivel inferior, de tareas "
        "específicas. Los cinco tipos pueden desplegarse juntos en un sistema multiagente, de modo que cada agente se encargue de la parte de "
        "la tarea que mejor maneja, y una orquestación que integre los distintos tipos puede producir un sistema muy inteligente y adaptativo "
        "(IBM, s.\u00a0f.-b). IBM lo ejemplifica con una fábrica inteligente, donde agentes reflejo se encargan de la automatización básica "
        "respondiendo con reglas predefinidas a las entradas de los sensores.")
    doc.parrafo(
        "Los marcos multiagente tienden a superar a los agentes individuales, porque cuantos más planes de acción tiene disponibles un agente, "
        "más aprendizaje y reflexión ocurren (Gutowska, s.\u00a0f.). Sin embargo, los sistemas construidos sobre un mismo modelo base pueden "
        "compartir debilidades que provoquen fallas en todos los agentes (Gutowska, s.\u00a0f.), aspecto que se retoma en la sección 5.3.")


# --------------------------------------------------------------------------- 5. Aplicaciones reales
def seccion5(doc: Documento) -> None:
    doc.titulo(1, "5. Aplicaciones reales")
    doc.titulo(2, "5.1 Sectores de aplicación")
    doc.parrafo(
        "IBM documenta el uso de agentes en numerosos sectores ({T:sectores}). Los agentes de los sectores financiero y de cadena de suministro "
        "requieren, además, medidas de seguridad que protejan la privacidad de los datos (Gutowska, s.\u00a0f.).")
    tabla_umb(doc, "sectores", "Aplicaciones de los agentes de IA por sector", ["Sector", "Qué hacen los agentes"], [
        ("Atención al cliente", "Asistentes virtuales integrados en sitios web y aplicaciones; también simulan entrevistas y brindan apoyo en salud mental."),
        ("Salud", "Sistemas multiagente que planifican tratamientos de pacientes en urgencias y gestionan procesos con medicamentos."),
        ("Finanzas", "Detectan fraude de forma continua, vigilan el cumplimiento normativo y apoyan el análisis de préstamos."),
        ("Respuesta a emergencias", "Tras un desastre natural, identifican en redes sociales a quienes necesitan rescate y mapean su ubicación."),
        ("Energía", "Gestionan la red de forma inteligente y predicen el mantenimiento; equilibran oferta y demanda en tiempo real."),
        ("Desarrollo de software", "Recorren el ciclo completo: especificación, implementación e iteración con mínima intervención."),
        ("Recursos humanos", "Responden preguntas frecuentes de los empleados, gestionan solicitudes de permisos y apoyan el cumplimiento."),
    ], [1.6, 4.9], nota="Elaboración propia con base en IBM (s.\u00a0f.-a) y Gutowska (s.\u00a0f.).", negrita_primera_col=True, sombrear_primera_col=True)
    doc.titulo(2, "5.2 Resultados medibles")
    doc.parrafo(
        "IBM reporta resultados cuantificados de algunos de estos usos ({T:resultados}). Se trata de casos propios de IBM o de sus clientes, "
        "por lo que no deben generalizarse sin considerar las condiciones de cada organización.")
    tabla_umb(doc, "resultados", "Resultados reportados por IBM sobre el uso de agentes", ["Caso", "Resultado reportado", "Descripción"], [
        ("Dynamiq con IBM watsonx Orchestrate", "Revisión de contratos: de 90 a 45 minutos.", "Asistente legal multiagente para una aseguradora (sección 6.1)."),
        ("IBM Bob", "+45 % de productividad en desarrolladores.", "Socio de programación («coding partner») usado por 10.000 desarrolladores de IBM en software, consultoría e infraestructura."),
        ("IBM AskHR", "Más de 80 solicitudes de recursos humanos automatizadas por completo.", "Agente de recursos humanos de IBM."),
        ("Pilotos en instituciones financieras", "30.000 días laborales ahorrados (estimado) y +20 % a 59 % de productividad.",
         "Mejora en tareas administrativas, documentación y análisis preliminar; cifras del Foro Económico Mundial citadas por IBM."),
    ], [1.6, 2.3, 2.6], nota="Cifras publicadas por IBM (Gutowska, s.\u00a0f.; IBM, s.\u00a0f.-a); no fueron verificadas de forma independiente.",
        negrita_primera_col=True, sombrear_primera_col=True)
    doc.titulo(2, "5.3 Beneficios, riesgos y buenas prácticas")
    doc.parrafo(
        "IBM destaca tres beneficios: la automatización de tareas complejas de forma rápida, económica y a escala; un mayor desempeño de los "
        "marcos multiagente frente a los agentes individuales; y respuestas más completas, precisas y personalizadas que las de los modelos "
        "tradicionales (Gutowska, s.\u00a0f.). Al mismo tiempo advierte riesgos y limitaciones ({T:riesgos}).")
    tabla_umb(doc, "riesgos", "Riesgos y limitaciones de los agentes de IA", ["Riesgo", "Descripción"], [
        ("Dependencias multiagente", "Los agentes construidos sobre el mismo modelo base comparten debilidades y pueden fallar juntos o ser vulnerables a ataques."),
        ("Bucles infinitos", "Un agente que no logra un plan completo ni reflexiona sobre sus hallazgos puede llamar repetidamente a las mismas herramientas."),
        ("Complejidad computacional", "Construir agentes desde cero consume tiempo y recursos, y algunas tareas pueden tardar varios días."),
        ("Privacidad de datos", "Integrar agentes con procesos de negocio sin supervisión ni límites puede generar graves problemas de seguridad."),
    ], [1.7, 4.8], nota="Elaboración propia con base en Gutowska (s.\u00a0f.).", negrita_primera_col=True, sombrear_primera_col=True)
    doc.parrafo("Para mitigarlos, IBM propone cuatro buenas prácticas ({T:practicas}).")
    tabla_umb(doc, "practicas", "Buenas prácticas para el uso de agentes de IA", ["Práctica", "Descripción"], [
        ("Registros de actividad", "Una bitácora de las herramientas y agentes usados da transparencia, permite descubrir errores y genera confianza."),
        ("Interrupción", "Permitir detener la secuencia de acciones, con criterio: algunas terminaciones causan más daño que beneficio, por ejemplo en una emergencia con riesgo de vida."),
        ("Identificadores únicos", "Permiten rastrear quién desarrolló, desplegó y usó al agente, lo que añade una capa de responsabilidad."),
        ("Supervisión humana", "Exigir aprobación humana antes de acciones de alto impacto, como el envío masivo de correos o las operaciones financieras."),
    ], [1.7, 4.8], nota="Elaboración propia con base en Gutowska (s.\u00a0f.).", negrita_primera_col=True, sombrear_primera_col=True)


# --------------------------------------------------------------------------- 6. Ejemplo
ARENA_FILAS = [
    ("1", "Claude Fable 5.1 (Max) · Anthropic", "14,55 %", "±1,92", "1–4", "4,16"),
    ("2", "Claude Opus 5.5 (High) · Anthropic", "13,78 %", "±2,24", "1–4", "1,56"),
    ("3", "GPT 6 Astra (Max) · OpenAI", "12,18 %", "±2,28", "1–7", "2,91"),
    ("4", "GPT 6 Sol (Max) · OpenAI", "10,65 %", "±2,57", "1–10", "0,92"),
    ("5", "Claude Opus 5 (High) · Anthropic", "8,76 %", "±1,50", "3–10", "2,52"),
    ("6", "Claude Opus 5 (Max) · Anthropic", "8,55 %", "±1,57", "3–10", "3,60"),
    ("7", "Claude Fable 5 (High) · Anthropic", "8,37 %", "±1,30", "4–10", "2,01"),
    ("8", "Gemini 4 Argon (High) · Google", "7,92 %", "±3,24", "3–15", "0,62"),
    ("9", "GPT 5.6 Sol (xHigh) · OpenAI", "7,05 %", "±1,38", "4–11", "1,05"),
    ("10", "Claude Opus 4.8 (High) · Anthropic", "6,92 %", "±1,38", "4–11", "1,36"),
]


def seccion6(doc: Documento) -> None:
    doc.titulo(1, "6. Ejemplo")
    doc.titulo(2, "6.1 Asistente legal multiagente de Dynamiq con IBM")
    doc.parrafo(
        "IBM presenta el caso de Dynamiq, que construyó un asistente de investigación legal multiagente para una importante aseguradora usando "
        "IBM watsonx Orchestrate. El sistema enruta las consultas legales entrantes primero por un clasificador de bajo costo, basado en un "
        "modelo IBM Granite, y escala únicamente los casos complejos a un agente de investigación más capaz. Ese enrutamiento inteligente "
        "entre agentes especializados redujo el tiempo de revisión de contratos de 90 a 45 minutos y mantuvo cada decisión auditable y con "
        "costo controlado (Gutowska, s.\u00a0f.) ({F:dynamiq}).")
    doc.parrafo(
        "El caso ilustra varios conceptos de este documento. Es un sistema multiagente en el que un nivel delega en otro, de forma similar al "
        "patrón vertical de la sección 3.2; usa un modelo de bajo costo para decidir qué agente debe intervenir, lo que muestra el valor de "
        "la orquestación; y conserva la trazabilidad de las decisiones, una de las buenas prácticas de la sección 5.3. Esta lectura es "
        "interpretación de los autores y no una afirmación de IBM.")
    doc.figura("dynamiq", "Flujo del asistente legal multiagente de Dynamiq", FIG / "fig5_dynamiq.png",
               nota="Esquema elaborado por los autores con base en la descripción de Gutowska (s.\u00a0f.). La fuente no detalla qué ocurre con los casos simples.")
    doc.titulo(2, "6.2 Evaluación de agentes: Agent Arena")
    doc.parrafo(
        "Agent Arena es un ranking dinámico de modelos según qué tan bien orquestan herramientas en tareas agénticas reales, con base en señales "
        "como la fiabilidad de las herramientas, la finalización de tareas y la dirigibilidad (steerability) (Arena, 2026). Al 30 de "
        "septiembre de 2026, la categoría General registraba 2.001.328 sesiones y 46 modelos. El ranking ordena los modelos por «mejora "
        "neta» (net improvement) y publica, para cada uno, un margen de error (±) y el rango de posiciones posibles. La {F:arena} y la {T:arena} "
        "muestran los diez primeros.")
    doc.figura("arena", "Diez primeros modelos de Agent Arena por mejora neta", FIG / "fig6_arena.png",
               nota="Elaboración propia con datos de Arena (2026), categoría General, consultados el 30 de septiembre de 2026. La barra y el punto "
                    "indican la mejora neta; la línea, su margen de error (±); USD/tarea es el costo mediano (P50).")
    tabla_umb(doc, "arena", "Diez primeros modelos de Agent Arena (categoría General)",
              ["Pos.", "Modelo · laboratorio", "Mejora neta", "Margen (±)", "Rango posible", "USD/tarea"], ARENA_FILAS,
              [0.5, 2.6, 0.9, 0.8, 0.9, 0.8], alinear=["c", "l", "c", "c", "c", "c"], tam=9.5,
              nota="Datos de Arena (2026), consultados el 30 de septiembre de 2026. Rango posible: posiciones que la página considera posibles para cada modelo. "
                   "USD/tarea: costo mediano por tarea (P50).")
    doc.parrafo(
        "Tres observaciones se desprenden de estos datos. Primero, los márgenes de error de los cuatro primeros modelos se traslapan y la "
        "propia página publica rangos de posición que van de «1 a 4» hasta «1 a 10»; por tanto, la diferencia entre ellos no es concluyente. Segundo, el "
        "desempeño y el costo no van de la mano: GPT 6 Sol (Max) obtiene una mejora neta de 10,65 % con un costo mediano de USD 0,92 por "
        "tarea, mientras que Claude Fable 5.1 (Max) obtiene 14,55 % con USD 4,16. Tercero, el costo mediano por tarea de los diez primeros "
        "va de USD 0,62 a USD 4,16.")
    doc.parrafo(
        "Además de la mejora neta, la página destaca cinco señales de desempeño, cada una con un modelo líder ({T:senales}). Estas señales se "
        "relacionan con los principios de la sección 2: el éxito confirmado, con el cumplimiento del objetivo; la dirigibilidad, con la "
        "supervisión humana; la recuperación ante fallos, con la autocorrección del plan; y la alucinación de herramientas, con el uso "
        "correcto de las herramientas. Esta correspondencia es una lectura de los autores.")
    tabla_umb(doc, "senales", "Señales de desempeño de Agent Arena y modelo que destaca cada una",
              ["Señal", "Qué mide", "Modelo que destaca", "Valor"], [
        ("Éxito confirmado (Confirmed Success)", "Con qué frecuencia el modelo logra que el usuario confirme que la tarea terminó.", "Claude Fable 5.1 (Max)", "17,46 %"),
        ("Elogio frente a queja (Praise vs Complaint)", "Respuestas positivas de los usuarios en relación con las negativas.", "GPT 6 Astra (Max)", "34,70 %"),
        ("Dirigibilidad (Steerability)", "Qué tan bien incorpora las correcciones del usuario.", "Gemini 4 Argon (High)", "15,88 %"),
        ("Recuperación ante fallos (Bash Recovery)", "Se recupera de comandos fallidos con el menor número de pasos.", "Claude Opus 5 (Max)", "13,05 %"),
        ("Alucinación de herramientas (Tool Hallucination)", "Probabilidad de inventar herramientas que no tiene; menos es mejor.", "GPT 5.6 Terra (xHigh)", "0,32 %"),
    ], [1.7, 2.3, 1.7, 0.8], alinear=["l", "l", "l", "c"], tam=9.5,
              nota="Datos de Arena (2026), consultados el 30 de septiembre de 2026. «Modelo que destaca» es el que la propia página señala como líder de "
                   "cada señal; en alucinación de herramientas, casi todos los diez primeros rondan 0,3 %.",
              negrita_primera_col=True, sombrear_primera_col=True)
    doc.parrafo(
        "Estos datos son una fotografía de un momento: el ranking se actualiza de forma continua y los modelos cambian de versión, por lo que "
        "las posiciones pueden variar en pocos días.")


# --------------------------------------------------------------------------- conclusiones y referencias
def conclusiones(doc: Documento) -> None:
    doc.titulo(1, "Conclusiones")
    doc.parrafo(
        "Un agente inteligente percibe su entorno, razona, planifica y actúa de forma autónoma para cumplir un objetivo definido por personas. "
        "Lo distinguen de un chatbot no agéntico el uso de herramientas, la memoria y la planificación, capacidades que le permiten completar "
        "tareas de varios pasos y corregir su propio plan.")
    doc.parrafo(
        "La arquitectura y el tipo de agente se eligen según el problema. Un agente único es simple y económico, pero poco escalable; los "
        "sistemas multiagente, ya sean verticales, horizontales o híbridos, aportan especialización y flexibilidad a costa de mayor "
        "complejidad y de riesgos como las fallas compartidas y los bucles infinitos. De ahí la importancia de los registros de actividad, "
        "la interrupción, los identificadores únicos y la supervisión humana.")
    doc.parrafo(
        "Los resultados que reporta IBM, como la reducción de 90 a 45 minutos en la revisión de contratos o el aumento de 45 % en la "
        "productividad de los desarrolladores, muestran el potencial de los agentes, aunque proceden de casos propios y no se verificaron de "
        "forma independiente. Finalmente, evaluar agentes exige medir su desempeño en tareas reales: en Agent Arena los primeros puestos se "
        "traslapan y el costo por tarea de los diez primeros va de USD 0,62 a USD 4,16, de modo que el mejor modelo no siempre es el más barato.")


def referencias(doc: Documento) -> None:
    doc.titulo(1, "Referencias", salto_antes=True)
    refs = (
        [("Arena. (2026, 30 de septiembre). ", False), ("Agent Arena: AI agent performance leaderboard", True),
         (" [Tabla de clasificación]. Recuperado el 30 de septiembre de 2026, de https://arena.ai/leaderboard/agent", False)],
        [("Gutowska, A. (s.\u00a0f.). ", False), ("What are AI agents?", True), (" IBM Think. https://www.ibm.com/think/topics/ai-agents", False)],
        [("IBM. (s.\u00a0f.-a). ", False), ("AI agent use cases", True), (". IBM Think. https://www.ibm.com/think/topics/ai-agent-use-cases", False)],
        [("IBM. (s.\u00a0f.-b). ", False), ("Types of AI agents", True), (". IBM Think. https://www.ibm.com/think/topics/ai-agent-types", False)],
        [("IBM. (s.\u00a0f.-c). ", False), ("What is agentic architecture?", True), (" IBM Think. https://www.ibm.com/think/topics/agentic-architecture", False)],
        [("Russell, S., y Norvig, P. (2021). ", False), ("Artificial intelligence: A modern approach", True), (" (4.ª ed.). Pearson.", False)],
    )
    for partes in refs:
        agregar_referencia(doc.d, partes)


def construir(doc: Documento) -> None:
    portada(doc)
    listas(doc)
    introduccion(doc)
    seccion1(doc)
    seccion2(doc)
    seccion3(doc)
    seccion4(doc)
    seccion5(doc)
    seccion6(doc)
    conclusiones(doc)
    referencias(doc)


if __name__ == "__main__":
    figuras.generar_todas()
    previo = Documento(estricto=False)          # pasada 1: solo registra la numeración (referencias hacia adelante)
    construir(previo)
    doc = Documento(etiquetas=previo.etiquetas, estricto=True)
    construir(doc)
    doc.guardar(SALIDA)
    print(f"docx generado: {SALIDA} | tablas={previo.n_tabla} | figuras={previo.n_figura}")
