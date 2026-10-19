"""Contenido del informe del Lab 5 «Service Worker» (estilo UMB, APA 7).

Las cifras salen de evidencia/resultados.json, que escribe ejecutar_laboratorio.mjs al correr el laboratorio de verdad en Chrome; las
comprobaciones cruzadas (caché frente a ARCHIVOS_CACHE, versiones mostradas) se verifican al construir el documento.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

sys.path.insert(0, r"C:\Users\cuent\Documents\Universidad\Katherin\2026-02\Sistemas Transaccionales\herramientas_doc\build")
sys.path.insert(0, r"C:\Users\cuent\.claude\skills\umb-documento\references")

from constructor import Documento  # noqa: E402
from corregir_docx import agregar_referencia, cabecera_azul  # noqa: E402

AQUI = pathlib.Path(__file__).resolve().parent.parent
FIG = AQUI / "figuras"
EVIDENCIA = AQUI / "evidencia"
PROYECTO = AQUI / "proyecto"
SF = "s.\u00a0f."
NBSP = "\u00a0"

RESULTADOS = json.loads((EVIDENCIA / "resultados.json").read_text(encoding="utf-8"))
MANIFIESTO = json.loads((EVIDENCIA / "vscode" / "figuras" / "manifiesto.json").read_text(encoding="utf-8"))
PARTE_A = RESULTADOS["parteA"]
CACHE_FIRST = RESULTADOS["parteB"]["cacheFirst"]
NETWORK_FIRST = RESULTADOS["parteB"]["networkFirst"]
FECHA = "19 de octubre de 2026"


def T(clave: str) -> str:
    return "{T:" + clave + "}"


def F(clave: str) -> str:
    return "{F:" + clave + "}"


def tabla_umb(doc: Documento, *args, **kwargs):
    kwargs.setdefault("negrita_primera_col", True)
    kwargs.setdefault("sombrear_primera_col", True)
    t = doc.tabla(*args, **kwargs)
    cabecera_azul(t)
    return t


def lineas(clave: str, parte: int) -> str:
    """Rango de líneas de una captura de código, leído del manifiesto de las capturas (para que el texto no pueda desfasarse)."""
    ini, fin = MANIFIESTO[clave][parte - 1]["lineas"]
    return f"líneas {ini} a {fin}"


def figura_codigo(doc: Documento, clave_figura: str, titulo: str, clave: str, parte: int, archivo: str, extra: str = "") -> None:
    total = len(MANIFIESTO[clave])
    doc.figura(clave_figura, f"{titulo} (parte {parte} de {total})", FIG / f"vscode_{MANIFIESTO[clave][parte - 1]['archivo']}",
               nota=f"Captura real de Visual Studio Code 1.142.0 con el resaltado de sintaxis del editor: {archivo}, {lineas(clave, parte)}.{extra}")


# --------------------------------------------------------------------------- comprobaciones cruzadas
def verificar_datos() -> None:
    archivos = re.search(r"ARCHIVOS_CACHE = \[(.*?)\]", (PROYECTO / "service-worker.js").read_text(encoding="utf-8"), re.S).group(1)
    declarados = sorted(re.findall(r"'([^']+)'", archivos))
    assert PARTE_A["caches"]["mi-pwa-v1"] == declarados, "el caché mi-pwa-v1 no coincide con ARCHIVOS_CACHE"
    assert PARTE_A["swActivado"] and PARTE_A["primeraCarga"]["sw"]["activo"] == "activated"
    assert not PARTE_A["primeraCarga"]["controlada"] and PARTE_A["recargaControlada"]["controlada"]
    s = PARTE_A["sinConexion"]
    assert s["enLinea"] is False and s["controlada"] and s["version"] == "v1"
    assert all(r["desdeSw"] for r in s["registroDeRed"]), "alguna solicitud sin conexión no pasó por el Service Worker"
    assert s["entregas"] == 2 and s["entregasTrasAgregar"] == 3 and PARTE_A["conConexionDeNuevo"]["entregas"] == 3
    assert PARTE_A["conConexionDeNuevo"]["estadoRed"] == "En línea"
    assert PARTE_A["nuevaVersionEnEspera"] and PARTE_A["cachesConVersionEnEspera"] == ["mi-pwa-v1", "mi-pwa-v2"]
    assert PARTE_A["versionNuevaActivada"] and list(PARTE_A["cachesTrasActualizar"]) == ["mi-pwa-v2"] and PARTE_A["versionTrasActualizar"] == "v2"
    assert (CACHE_FIRST["trasCambio"]["version"], CACHE_FIRST["versionEnCacheTrasCambio"], CACHE_FIRST["segundaRecarga"]["version"]) == ("v1", "v1", "v1")
    assert (NETWORK_FIRST["trasCambio"]["version"], NETWORK_FIRST["versionEnCacheTrasCambio"], NETWORK_FIRST["segundaRecarga"]["version"]) == ("v2", "v2", "v2")
    assert CACHE_FIRST["versionEnServidor"] == NETWORK_FIRST["versionEnServidor"] == "v2"
    assert CACHE_FIRST["sinServidor"]["cargo"] and NETWORK_FIRST["sinServidor"]["cargo"]
    assert (CACHE_FIRST["sinServidor"]["version"], NETWORK_FIRST["sinServidor"]["version"]) == ("v1", "v2")


# --------------------------------------------------------------------------- introducción
def introduccion(doc: Documento) -> None:
    doc.titulo(1, "Introducción", salto_antes=True)
    doc.parrafo(
        "Este informe documenta la guía de laboratorio n.º 5, «Service Worker», del módulo 2 (PWA) de Nuevas Tecnologías del Desarrollo. El "
        "objetivo de la guía es implementar un Service Worker funcional que permita que una aplicación web siga funcionando sin conexión, "
        "gestione el caché de sus recursos e intercepte las peticiones de red (Universidad Manuela Beltrán [UMB], 2026).")
    doc.parrafo(
        "Se construyó una aplicación pequeña, «Agenda de entregas UMB», y se le agregó el Service Worker de la guía con estrategia Cache-First. "
        "Después se registró en la aplicación, se verificó en Chrome DevTools, se probó sin conexión y se resolvió el desafío: reescribir el "
        "evento <i>fetch</i> con Network-First y comparar las dos estrategias con una medición. El informe cierra con la reflexión sobre qué "
        "estrategia conviene para un blog de noticias, una calculadora y un chat en tiempo real.")
    doc.parrafo(
        "El título y el objetivo de la guía mencionan las notificaciones push, pero ninguno de sus pasos ni de sus criterios de evaluación las "
        "pide; por eso no se implementaron. Todas las capturas son de ejecuciones reales; la sección 2.1 explica el entorno y cómo se operó. "
        f"La {T('datos')} reúne los datos de la práctica y la {T('entregable')} indica dónde está cada elemento del entregable.")
    tabla_umb(doc, "datos", "Datos de la práctica", ["Campo", "Valor"], [
        ("Grupo", "Grupo 6"),
        ("Integrante 1", "Rodríguez Ángel, Santiago"),
        ("Integrante 2", "Olaya Rojas, Santiago"),
        ("Fecha de ejecución", FECHA),
        ("Asignatura", "Nuevas Tecnologías del Desarrollo, módulo 2: PWA"),
        ("Guía", "Guía de laboratorio n.º 5: Service Worker (offline, caché, fetch)"),
    ], [1.6, 4.9], tam=9.5, nota="Elaboración propia con base en la guía (UMB, 2026).")
    tabla_umb(doc, "entregable", "Dónde está cada elemento del entregable", ["Elemento del entregable", "Dónde está"], [
        ("1. Carpeta .zip con todo el proyecto, con service-worker.js funcional",
         f"Archivo Lab5_ServiceWorker_Grupo6.zip, carpeta proyecto; estructura en la {F('estructura')}"),
        ("2. Captura del Service Worker activo en DevTools", f"{F('dt_sw')} y {F('dt_consola')}, sección 2.4"),
        ("3. Captura de Cache Storage con los archivos", f"{F('dt_cache')}, sección 2.4"),
        ("4. Captura de la app funcionando sin conexión", f"{F('dt_offline')}, {F('dt_net')} y {F('app_off')}, sección 2.5"),
        ("5. Ambas versiones del Service Worker, comentadas",
         f"Secciones 2.3 y 2.7 ({F('cf1')} a {F('cf3')} y {F('nf1')} a {F('nf3')}); archivos service-worker.js y service-worker-network-first.js"),
        ("6. Respuesta escrita a la reflexión sobre estrategias de caché", f"Sección 2.8 y {T('reflexion')}"),
    ], [3.4, 3.1], tam=9.5, nota="Elaboración propia con base en el entregable de la guía (UMB, 2026).")


# --------------------------------------------------------------------------- 1. marco conceptual
def marco_conceptual(doc: Documento) -> None:
    doc.titulo(1, "1. Marco conceptual")
    doc.titulo(2, "1.1 Qué es un Service Worker")
    doc.parrafo(
        "Un Service Worker es un intermediario dirigido por eventos que se sitúa entre la aplicación web, el navegador y la red cuando esta "
        "está disponible. Permite interceptar y modificar las peticiones, guardar recursos en caché y ofrecer una experiencia sin conexión "
        "(MDN Web Docs, s.\u00a0f.-a). Corre en un contexto de trabajador, en un hilo distinto al de la página, por lo que no accede al DOM, "
        "y solo está disponible en contextos seguros: se sirve por HTTPS, y <i>http://localhost</i> también está permitido para desarrollar "
        "(MDN Web Docs, s.\u00a0f.-a, s.\u00a0f.-b).")
    doc.titulo(2, "1.2 Ciclo de vida")
    doc.parrafo(
        f"El Service Worker de la guía usa tres eventos, que resume la {T('ciclo')}. A ellos se suma una fase intermedia que explica la "
        "sección 2.6: cuando se instala una versión nueva, esta espera hasta que ninguna página use la anterior, de modo que solo una "
        "versión controle las páginas a la vez (Archibald, 2016).")
    tabla_umb(doc, "ciclo", "Eventos del ciclo de vida del Service Worker", ["Evento", "Cuándo ocurre", "Qué se hace aquí"], [
        ("<i>install</i>", "La primera vez que se registra el Service Worker, y con cada versión nueva.",
         "Guardar los archivos en caché (pre-caching). Si la promesa de <i>waitUntil</i> falla, la instalación falla (MDN Web Docs, s.\u00a0f.-b)."),
        ("<i>waiting</i>", "Después de instalar una versión nueva, mientras la anterior controle páginas.",
         "Nada: la versión nueva espera; <i>skipWaiting()</i> permite saltar la espera (Archibald, 2016)."),
        ("<i>activate</i>", "Cuando la versión anterior ya no controla páginas.",
         "Eliminar los cachés viejos y migrar datos (Archibald, 2016)."),
        ("<i>fetch</i>", "Cada vez que la app hace una petición HTTP.",
         "Interceptar la petición y responder desde el caché o desde la red, con <i>event.respondWith()</i>."),
    ], [0.9, 2.5, 3.1], tam=9.5,
        nota="Elaboración propia con base en la guía (UMB, 2026), MDN Web Docs (s.\u00a0f.-b) y Archibald (2016).")
    doc.titulo(2, "1.3 Caché y estrategias de respuesta")
    doc.parrafo(
        "La API Cache guarda pares petición-respuesta en cachés con nombre. <i>caches.open()</i> crea o abre uno, <i>cache.addAll()</i> "
        "guarda varios recursos a la vez, <i>cache.put()</i> guarda uno, y <i>caches.match()</i> devuelve la respuesta guardada o "
        "<i>undefined</i> si no hay copia (MDN Web Docs, s.\u00a0f.-b). Una respuesta es un flujo que se lee una sola vez, por eso, para "
        "guardarla y a la vez entregarla a la página, se usa <i>clone()</i>: una copia va al caché y la original va al navegador (MDN Web "
        "Docs, s.\u00a0f.-b).")
    doc.parrafo(
        f"Sobre esa API se construyen las estrategias de la {T('estrategias')}. Las dos que pide la guía son Cache-First, que consulta primero "
        "el caché, y Network-First, que consulta primero la red.")
    tabla_umb(doc, "estrategias", "Estrategias de respuesta de un Service Worker", ["Estrategia", "Cómo responde", "Para qué contenido conviene"], [
        ("Cache-First (caché y, si no hay, red)", "Devuelve la copia del caché; solo si no existe va a la red. Los cambios del servidor no se ven "
                                                  "mientras haya copia.",
         "Aplicaciones que funcionan primero sin conexión y recursos estáticos, sobre todo los versionados con un identificador en el nombre "
         "(Archibald, 2014; Chrome for Developers, 2021)."),
        ("Network-First (red y, si falla, caché)", "Pide a la red; si responde, guarda una copia y la entrega; si falla, entrega la última copia.",
         "Contenido que cambia a menudo, como artículos o respuestas de una API. Con una red lenta o intermitente, el usuario espera mucho antes "
         "de ver la copia (Archibald, 2014; Chrome for Developers, 2021)."),
        ("Stale-while-revalidate", "Entrega la copia del caché de inmediato y actualiza el caché en segundo plano para la próxima visita.",
         "Contenido que debe mantenerse razonablemente al día pero no es crítico, como los avatares (Archibald, 2014; Chrome for Developers, 2021)."),
        ("Solo red (<i>network only</i>)", "Siempre va a la red, sin alternativa sin conexión.",
         "Lo que no tiene equivalente sin conexión, como las peticiones que no son GET (Archibald, 2014)."),
    ], [1.5, 2.5, 2.5], tam=9.5,
        nota="Elaboración propia con base en Archibald (2014) y Chrome for Developers (2021).")
    doc.titulo(2, "1.4 Herramientas de Chrome DevTools")
    doc.parrafo(
        "El panel Application de Chrome DevTools tiene un panel «Service workers» con el estado de cada Service Worker y tres casillas: "
        "<i>Offline</i> pone a DevTools en modo sin conexión, <i>Update on reload</i> actualiza el Service Worker en cada carga y "
        "<i>Bypass for network</i> hace que las peticiones salten el Service Worker y vayan directo a la red. Más abajo, «Cache storage» "
        "muestra de solo lectura los recursos que el Service Worker guardó con la API Cache (Basques y Emelianova, 2016). Esas son las "
        "herramientas con las que se verifica el laboratorio.")


# --------------------------------------------------------------------------- 2. desarrollo
def entorno(doc: Documento) -> None:
    e = RESULTADOS["entorno"]
    doc.titulo(1, "2. Desarrollo del laboratorio", salto_antes=True)
    doc.titulo(2, "2.1 Entorno y método de ejecución")
    doc.parrafo(
        "La guía propone abrir la app con Live Server de Visual Studio Code y usar Chrome. Como equivalente se usó un servidor web local "
        "mínimo, escrito en Python, que sirve la carpeta del proyecto en <i>http://localhost:8095</i>; <i>localhost</i> es un origen seguro, "
        "así que el Service Worker funciona sin HTTPS (MDN Web Docs, s.\u00a0f.-b). El servidor envía el encabezado <i>Cache-Control: no-store</i> "
        "para que la caché HTTP del navegador nunca oculte lo que hace, o deja de hacer, el Service Worker.")
    doc.parrafo(
        "Las pruebas las ejecutó un script que controla Google Chrome mediante el protocolo Chrome DevTools. Chrome sirve su propia interfaz "
        "de DevTools; el script la abrió conectada a la pestaña de la app, de modo que los paneles de las capturas son los reales de Chrome, "
        "y los clics sobre ellos, como marcar «Offline», son eventos de entrada reales. La excepción es la actualización de versión de la "
        "sección 2.6, que se activó con el comando <i>ServiceWorker.skipWaiting</i> del mismo protocolo, equivalente al botón "
        f"<i>skipWaiting</i> que muestra DevTools. La {T('entorno')} resume el entorno.")
    tabla_umb(doc, "entorno", "Entorno de ejecución del laboratorio", ["Parámetro", "Valor"], [
        ("Fecha de ejecución", FECHA),
        ("Navegador", f"Google Chrome {e['navegador'].split('/')[1]}, en modo sin ventana (<i>headless</i>), controlado por script"),
        ("Servidor local", "Python (<i>http.server</i>) en http://localhost:8095, con <i>Cache-Control: no-store</i>"),
        ("Editor", "Visual Studio Code 1.142.0, con un perfil aislado y sin extensiones"),
        ("Script de pruebas", f"herramientas/ejecutar_laboratorio.mjs, con Node.js {e['node'].lstrip('v')}"),
        ("Resultados medidos", "evidencia/resultados.json, escrito por el script con cada medición"),
    ], [1.6, 4.9], tam=9.5, nota="Elaboración propia con datos de la ejecución en Chrome (Google, s.\u00a0f.) y Visual Studio Code (Microsoft, s.\u00a0f.).")


def paso1(doc: Documento) -> None:
    doc.titulo(2, "2.2 Paso 1. Ciclo de vida y proyecto de prueba")
    doc.parrafo(
        "El primer paso de la guía es conceptual: los tres eventos del ciclo de vida (sección 1.2). Para poder probarlos se creó una "
        "aplicación completa, «Agenda de entregas UMB», una lista de entregas pendientes que se guarda en el navegador (<i>localStorage</i>) y "
        "muestra si hay conexión. La página lleva además un renglón «Versión del contenido» que sirve de testigo en las pruebas de las "
        f"secciones 2.6 y 2.7: cambiarlo en el servidor permite ver qué versión entrega cada estrategia. La {T('archivos')} lista los archivos y "
        f"la {F('estructura')} muestra el proyecto abierto en Visual Studio Code.")
    tabla_umb(doc, "archivos", "Archivos del proyecto", ["Archivo", "Función"], [
        ("index.html", "Página única de la app: encabezado con la versión del contenido y el estado de la red, formulario y lista de entregas."),
        ("styles.css", "Estilos de la app; los colores y las medidas están definidos como variables al inicio del archivo."),
        ("app.js", "Lógica de la lista (agregar, marcar, quitar), indicador de conexión y, al final, el registro del Service Worker."),
        ("manifest.json", "Manifiesto de la app: nombre, colores, modo de visualización e íconos de 192 y 512 píxeles."),
        ("icons/icon-192.png, icons/icon-512.png", "Íconos de la app; también se guardan en el caché."),
        ("service-worker.js", "Service Worker con estrategia Cache-First, tal como lo entrega la guía, con comentarios agregados."),
        ("service-worker-network-first.js", "Versión del desafío, con estrategia Network-First; solo cambia el evento <i>fetch</i>."),
    ], [2.1, 4.4], tam=9.5, nota="Elaboración propia.")
    doc.figura("estructura", "Estructura del proyecto en Visual Studio Code", FIG / "vscode_estructura_proyecto.png",
               nota="Captura real del explorador de Visual Studio Code con la carpeta proyecto y service-worker.js abierto.")


def paso2(doc: Documento) -> None:
    doc.titulo(2, "2.3 Paso 2. Crear service-worker.js con Cache-First")
    doc.parrafo(
        "Se creó <i>service-worker.js</i> en la raíz del proyecto con el código de la guía, sin cambiar su lógica, y se le agregaron "
        "comentarios en español que explican cada parte. "
        f"{F('cf1')} a {F('cf3')} muestran el archivo completo. El encabezado resume la estrategia, el nombre del caché "
        "(<i>mi-pwa-v1</i>) cambia cuando se actualiza la app, y la lista <i>ARCHIVOS_CACHE</i> reúne los siete recursos que se guardan al instalar.")
    figura_codigo(doc, "cf1", "Código de service-worker.js con Cache-First", "service_worker_cache_first", 1, "service-worker.js")
    doc.parrafo(
        "En <i>install</i>, <i>waitUntil()</i> obliga al navegador a esperar a que termine la promesa antes de dar la instalación por "
        "terminada, y <i>addAll()</i> es atómico: si un solo archivo falla, por ejemplo con un error 404, no se guarda ninguno y la instalación "
        "falla (MDN Web Docs, s.\u00a0f.-b).")
    figura_codigo(doc, "cf2", "Código de service-worker.js con Cache-First", "service_worker_cache_first", 2, "service-worker.js")
    doc.parrafo(
        "En <i>activate</i>, el Service Worker borra todos los cachés cuyo nombre no sea el actual; así, al subir la versión del nombre, "
        "el caché anterior desaparece. En <i>fetch</i>, <i>caches.match()</i> busca la petición: si hay copia la devuelve sin tocar la red, "
        "y si no, la pide con <i>fetch()</i>.")
    figura_codigo(doc, "cf3", "Código de service-worker.js con Cache-First", "service_worker_cache_first", 3, "service-worker.js",
                  extra=" Al final del archivo, un cuadro compara las dos estrategias.")


def paso3(doc: Documento) -> None:
    a = PARTE_A
    doc.titulo(2, "2.4 Paso 3. Registrar el Service Worker y verificarlo en DevTools")
    doc.parrafo(
        "Al final de <i>app.js</i> se agregó el bloque de registro de la guía. Registra el Service Worker solo si el navegador lo admite y "
        f"espera al evento <i>load</i> para no competir con la carga de la página ({F('registro')}).")
    doc.figura("registro", "Registro del Service Worker en app.js", FIG / "vscode_registro_en_app_1.png",
               nota="Captura real de Visual Studio Code 1.142.0: app.js, líneas 97 a 110.")
    doc.parrafo(
        f"Con la app cargada, el panel Application > Service workers muestra el Service Worker como «activated and is running», con el punto "
        f"verde, para el origen {a['primeraCarga']['sw']['alcance']} ({F('dt_sw')}). La consola registra los cuatro mensajes: el de la app y los "
        f"tres del Service Worker ({F('dt_consola')}), y Cache storage muestra el caché <i>mi-pwa-v1</i> con los siete archivos de "
        f"<i>ARCHIVOS_CACHE</i> ({F('dt_cache')}).")
    doc.figura("dt_sw", "Service Worker activo en Chrome DevTools", FIG / "devtools_service_worker.png",
               nota="Captura real de Chrome DevTools, Application > Service workers. Se recortó el espacio vacío bajo el cuadro «Update Cycle».")
    doc.figura("dt_consola", "Mensajes del Service Worker y de la app en la consola", FIG / "devtools_consola.png",
               nota="Captura real de la consola de Chrome DevTools, sin errores. A la derecha de cada mensaje aparece el archivo y la línea que lo emitió.")
    doc.figura("dt_cache", "Cache Storage con el caché mi-pwa-v1", FIG / "devtools_cache_v1.png",
               nota="Captura real de Chrome DevTools, Application > Cache storage. Se unió la franja inferior con el total de entradas al recorte de la "
                    "tabla, y se dejó entre ambas un pequeño espacio en blanco.")
    tabla_umb(doc, "verificacion", "Verificación del resultado esperado del paso 3", ["Resultado esperado por la guía", "Resultado observado", "Evidencia"], [
        ("Service Worker activo y corriendo (verde en DevTools)", "«#1 activated and is running», punto verde.", F("dt_sw")),
        ("Mensajes [SW] Instalando... y [SW] Activando... en la consola", "Aparecen los cuatro mensajes, sin errores.", F("dt_consola")),
        ("Cache Storage con todos los archivos de ARCHIVOS_CACHE", "mi-pwa-v1 con 7 entradas: las 7 de la lista.", F("dt_cache")),
    ], [2.4, 2.9, 1.2], alinear=["l", "l", "c"], tam=9.5, nota="Elaboración propia con base en la guía (UMB, 2026) y en la ejecución.")
    doc.parrafo(
        "Un detalle que la medición confirmó: la primera carga de la página no queda controlada por el Service Worker, solo las siguientes. "
        f"En la primera carga, <i>navigator.serviceWorker.controller</i> fue nulo; tras una recarga, ya apuntaba al Service Worker "
        f"(sección 2.5). Se debe a que el código de la guía no llama a <i>clients.claim()</i>, que es lo que permite a un Service Worker "
        "recién activado tomar el control de páginas cargadas sin él (Archibald, 2016).")


def paso4(doc: Documento) -> None:
    s = PARTE_A["sinConexion"]
    doc.titulo(2, "2.5 Paso 4. Probar el modo sin conexión")
    doc.parrafo(
        f"Siguiendo el procedimiento de la guía, en Application > Service workers se marcó la casilla «Offline» ({F('dt_offline')}) y se "
        f"recargó la página. En el panel Network, las seis solicitudes de la carga, con el documento, la hoja de estilos, el script, el "
        f"manifiesto y el ícono (dos veces), tuvieron estado 200 y tamaño «(ServiceWorker)», con 0 B transferidos ({F('dt_net')}). La app "
        f"cargó completa ({F('app_off')}a).")
    doc.figura("dt_offline", "Casilla Offline marcada en el panel Service workers", FIG / "devtools_offline_casilla.png",
               nota="Captura real de Chrome DevTools. La pestaña Network muestra una advertencia porque la limitación de red está activa.")
    doc.figura("dt_net", "Panel Network con Offline marcado: solicitudes atendidas por el Service Worker", FIG / "devtools_network_offline.png",
               nota="Captura real del panel Network de Chrome DevTools. Se unió la franja inferior con el resumen de solicitudes al recorte de la tabla, y "
                    "se dejó entre ambas un pequeño espacio en blanco.")
    doc.parrafo(
        f"Además de la carga, se comprobó que la app sigue siendo útil sin conexión: con «Offline» activo se agregó la entrega «Subir el Lab 5 sin "
        f"conexión», y la lista pasó de {s['entregas']} a {s['entregasTrasAgregar']} entregas ({F('app_off')}b). Esto no depende del Service "
        f"Worker, sino de que los datos viven en el navegador. La {T('offline')} reúne las mediciones.")
    doc.figura("app_off", "La app sin conexión: recarga y nueva entrega", FIG / "app_sin_conexion.png",
               nota="Capturas reales de la pestaña de la app con «Offline» marcado: a) recarga completa, con el indicador «Sin conexión: la app sigue "
                    "funcionando»; b) después de agregar una entrega. Se recortó el espacio vacío bajo cada página.")
    tabla_umb(doc, "offline", "Mediciones de la prueba sin conexión", ["Medición", "Resultado"], [
        ("Indicador de la app con «Offline» marcado", s["estadoRed"]),
        ("<i>navigator.onLine</i> con «Offline» marcado", "false"),
        ("Página controlada por el Service Worker", "Sí"),
        ("Recursos de la página atendidos por el Service Worker", f"{len(s['registroDeRed'])} de {len(s['registroDeRed'])}, además del documento"),
        ("Versión del contenido que se muestra", s["version"]),
        ("Entregas antes y después de agregar una", f"{s['entregas']} y {s['entregasTrasAgregar']}"),
        ("Después de desmarcar «Offline» y recargar", f"{PARTE_A['conConexionDeNuevo']['estadoRed']}, con {PARTE_A['conConexionDeNuevo']['entregas']} entregas"),
    ], [3.4, 3.1], tam=9.5, nota="Elaboración propia con las mediciones de evidencia/resultados.json. Los recursos atendidos se cuentan con la propiedad "
                                  "<i>workerStart</i> de la API de rendimiento del navegador.")
    doc.parrafo(
        "Antes de continuar se desmarcó la casilla «Offline», como pide la guía, y se verificó con el script que quedó desmarcada.")


def actualizacion(doc: Documento) -> None:
    a = PARTE_A
    doc.titulo(2, "2.6 Actualizar la versión del Service Worker")
    doc.parrafo(
        "La guía recuerda que el nombre del caché debe cambiar cuando se actualiza la app. Para ver qué ocurre, se cambió <i>CACHE_NAME</i> a "
        "<i>mi-pwa-v2</i> y el contenido de la página a «v2». Al pedir una actualización, el navegador instaló la versión nueva, que "
        f"creó el caché <i>mi-pwa-v2</i> pero quedó «waiting to activate», porque la versión anterior seguía controlando la página: DevTools "
        f"muestra las dos versiones y el botón <i>skipWaiting</i>, y en ese momento coexistían los cachés <i>{a['cachesConVersionEnEspera'][0]}</i> y "
        f"<i>{a['cachesConVersionEnEspera'][1]}</i> ({F('dt_espera')}).")
    doc.figura("dt_espera", "Versión nueva del Service Worker en espera", FIG / "devtools_version_en_espera.png",
               nota="Captura real de Chrome DevTools, Application > Service workers: la versión n.º 1 activa y la n.º 2 en espera, con el botón skipWaiting.")
    doc.parrafo(
        "Al saltar la espera con <i>skipWaiting</i>, la versión nueva se activó y su evento <i>activate</i> borró el caché viejo: solo quedó "
        f"<i>mi-pwa-v2</i> ({F('dt_cache2')}). Tras recargar, la página mostró «{a['versionTrasActualizar']}». Esto demuestra para qué sirven los "
        "dos mecanismos que el código de la guía deja listos, el nombre del caché y la limpieza en <i>activate</i>, y es la forma de superar la "
        "desventaja de Cache-First que se mide en la sección 2.7.")
    doc.figura("dt_cache2", "Cache Storage después de actualizar: solo queda mi-pwa-v2", FIG / "devtools_cache_v2.png",
               nota="Captura real de Chrome DevTools, Application > Cache storage. Se unió la franja inferior con el total de entradas al recorte de la "
                    "tabla.")


def desafio(doc: Documento) -> None:
    cf, nf = CACHE_FIRST, NETWORK_FIRST
    doc.titulo(2, "2.7 Desafío: Network-First")
    doc.parrafo(
        "El desafío pide cambiar la estrategia del evento <i>fetch</i> a Network-First: primero intenta la red y, si falla, usa el caché. Se "
        "reimplementó en <i>service-worker-network-first.js</i>, que conserva <i>install</i> y <i>activate</i> y solo cambia <i>fetch</i>. "
        "Como <i>app.js</i> registra siempre el nombre <i>service-worker.js</i> y el navegador admite un solo Service Worker por alcance, "
        f"para probar esta versión se copia su contenido sobre <i>service-worker.js</i>. {F('nf1')} a {F('nf3')} muestran el archivo "
        "completo, comentado.")
    figura_codigo(doc, "nf1", "Código de service-worker-network-first.js con Network-First", "service_worker_network_first", 1,
                  "service-worker-network-first.js")
    figura_codigo(doc, "nf2", "Código de service-worker-network-first.js con Network-First", "service_worker_network_first", 2,
                  "service-worker-network-first.js")
    doc.parrafo(
        "El evento <i>fetch</i> atiende solo las peticiones GET, porque el caché no puede guardar las demás. Pide la petición a la red y, "
        "si responde con estado 200, guarda una copia con <i>cache.put()</i> usando <i>clone()</i> y entrega la respuesta original; si la "
        "red falla, el <i>catch</i> devuelve la última copia con <i>caches.match()</i>.")
    figura_codigo(doc, "nf3", "Código de service-worker-network-first.js con Network-First", "service_worker_network_first", 3,
                  "service-worker-network-first.js", extra=" Al final del archivo, un cuadro compara las dos estrategias.")
    doc.parrafo(f"La {T('diferencias')} resume en qué difieren las dos versiones del evento <i>fetch</i>.")
    tabla_umb(doc, "diferencias", "Diferencias entre las dos versiones del evento fetch", ["Aspecto", "Cache-First (service-worker.js)", "Network-First (service-worker-network-first.js)"], [
        ("Primer intento", "<i>caches.match(event.request)</i>", "<i>fetch(event.request)</i>"),
        ("Alternativa", "Si no hay copia, <i>fetch()</i> a la red.", "Si la red falla, <i>caches.match()</i> con la última copia."),
        ("Escritura en el caché", "Solo en <i>install</i>.", "En <i>install</i> y en cada respuesta de la red con estado 200 (<i>cache.put</i>)."),
        ("Uso de <i>clone()</i>", "No lo necesita.", "Sí: una copia va al caché y la original a la página."),
        ("Peticiones que atiende", "Todas.", "Solo las GET."),
    ], [1.5, 2.4, 2.6], tam=9.5, nota="Elaboración propia a partir del código de las figuras de esta sección y de la sección 2.3.")
    doc.parrafo(
        "Para comparar las dos estrategias con datos, el script repitió con cada una el mismo experimento: cargar la app, esperar a que el "
        "Service Worker controlara la página, cambiar la versión del contenido de «v1» a «v2» en el servidor y recargar, y después detener "
        f"el servidor y recargar otra vez. La {T('comparacion')} reúne las mediciones; {F('comp_serv')} y {F('comp_sin')} las muestran.")
    tabla_umb(doc, "comparacion", "Comparación de Cache-First y Network-First con el contenido cambiado en el servidor",
              ["Medición", "Cache-First", "Network-First"], [
                  ("Versión en el servidor tras el cambio", cf["versionEnServidor"], nf["versionEnServidor"]),
                  ("Versión que muestra la página al recargar", cf["trasCambio"]["version"], nf["trasCambio"]["version"]),
                  ("Versión guardada en el caché para «/» tras recargar", cf["versionEnCacheTrasCambio"], nf["versionEnCacheTrasCambio"]),
                  ("Versión que muestra en una segunda recarga", cf["segundaRecarga"]["version"], nf["segundaRecarga"]["version"]),
                  ("Con el servidor detenido: ¿carga la página?", "Sí" if cf["sinServidor"]["cargo"] else "No", "Sí" if nf["sinServidor"]["cargo"] else "No"),
                  ("Con el servidor detenido: versión que muestra", cf["sinServidor"]["version"], nf["sinServidor"]["version"]),
              ], [3.3, 1.6, 1.6], alinear=["l", "c", "c"], tam=9.5,
              nota="Elaboración propia con las mediciones de evidencia/resultados.json, con el contenido cambiado de v1 a v2 en el servidor.")
    doc.figura("comp_serv", "Página tras cambiar el contenido en el servidor: Cache-First y Network-First", FIG / "comparacion_servidor_actualizado.png",
               nota="Capturas reales de la pestaña de la app tras recargar con el servidor en v2: arriba, Cache-First (muestra v1); abajo, Network-First (muestra v2).")
    doc.figura("comp_sin", "Página con el servidor detenido: Cache-First y Network-First", FIG / "comparacion_sin_servidor.png",
               nota="Capturas reales tras detener el servidor y recargar: arriba, Cache-First (v1); abajo, Network-First (v2). El indicador dice «En línea» "
                    "porque el navegador tiene red; el que falló es el servidor, no la conexión.")
    doc.parrafo(
        "Los resultados confirman lo que el código anticipa. Cache-First siguió mostrando «v1» aunque el servidor ya tenía «v2», y lo seguirá "
        "haciendo hasta que cambie el nombre del caché (sección 2.6): nunca consultó la red. Network-First mostró «v2» desde la primera recarga y "
        "además actualizó la copia guardada. Con el servidor detenido, las dos estrategias cargaron la página: Cache-First con la copia que ya "
        "tenía y Network-First con la última copia que había guardado, que ya era la de «v2».")
    doc.parrafo(
        "Esto matiza el enunciado de la guía, según el cual Network-First no funciona sin conexión. Funciona sin conexión con lo que ya haya "
        "guardado, porque su alternativa ante una falla de red es el caché; lo que no puede ofrecer es contenido que nunca se haya guardado. Su "
        "costo es otro: depende de la red para responder, y si esta es lenta o intermitente, el usuario espera antes de ver la copia "
        "(Archibald, 2014). Esa espera no se midió aquí, porque la red de pruebas es local.")


def reflexion(doc: Documento) -> None:
    doc.titulo(2, "2.8 Reflexión: qué estrategia usar y por qué")
    doc.parrafo(
        "<b>Pregunta.</b> La estrategia Cache-First es rápida pero puede mostrar contenido desactualizado, y Network-First tiene contenido "
        "fresco pero depende de la red. ¿Cuál se usaría para (a) un blog de noticias, (b) una app de calculadora y (c) un chat en tiempo real? "
        f"La {T('reflexion')} resume la respuesta y cada caso se justifica después.")
    tabla_umb(doc, "reflexion", "Estrategia elegida para cada caso", ["Caso", "Estrategia", "Razón principal"], [
        ("(a) Blog de noticias", "Network-First para los artículos; Cache-First para estilos, scripts e imágenes.",
         "El contenido cambia a menudo y debe estar al día; el aspecto casi no cambia."),
        ("(b) App de calculadora", "Cache-First.", "Todo el código viaja con la app y nada cambia entre usos; responde de inmediato y sin red."),
        ("(c) Chat en tiempo real", "Solo red para los mensajes; Cache-First para la interfaz.",
         "Un mensaje en caché es un mensaje viejo; lo que sí puede guardarse es la pantalla."),
    ], [1.4, 2.3, 2.8], tam=9.5, nota="Elaboración propia con base en las mediciones de las secciones 2.6 y 2.7, Archibald (2014) y Chrome for Developers (2021).")
    doc.parrafo(
        "<b>(a) Blog de noticias.</b> Se usaría Network-First para el contenido de los artículos y la portada. Quien abre un blog de noticias "
        "quiere lo último, y la prueba de la sección 2.7 muestra el problema de la alternativa: con Cache-First, el lector habría seguido viendo "
        "«v1» aunque el servidor ya publicara «v2». Con Network-First ve lo más reciente cuando hay conexión y, sin ella, puede releer los "
        "artículos que ya había abierto. Es la recomendación para páginas HTML y respuestas de API (Chrome for Developers, 2021) y para "
        "contenido como los artículos (Archibald, 2014). Su riesgo es que una red lenta retrasa la página; una opción es stale-while-revalidate, "
        "que muestra la copia de inmediato y la renueva para la próxima visita, aceptable si la última noticia no es crítica. Los estilos, "
        "scripts e imágenes versionados sí van con Cache-First, porque no cambian.")
    doc.parrafo(
        "<b>(b) App de calculadora.</b> Cache-First. Una calculadora no depende de datos del servidor: su lógica y su interfaz son archivos "
        "estáticos que se guardan al instalar. Con Cache-First abre al instante, sin red, y el riesgo de contenido desactualizado casi no "
        "existe, porque lo único que cambia son las versiones de la propia app; para esas basta cambiar el nombre del caché, como se hizo en la "
        "sección 2.6. Es el caso típico de las aplicaciones que funcionan primero sin conexión y de los recursos estáticos (Archibald, 2014; "
        "Chrome for Developers, 2021).")
    doc.parrafo(
        "<b>(c) Chat en tiempo real.</b> Ninguna de las dos estrategias sirve para los mensajes en sí. Un chat vale por lo que acaba de pasar, y "
        "una respuesta guardada en el caché es, por definición, una foto vieja: mostrarla como si fuera la conversación actual es peor que no "
        "mostrarla. Los mensajes deberían pedirse siempre a la red, sin caché (estrategia «solo red»), y la interfaz, que sí es estática, "
        "se serviría con Cache-First para que la pantalla abra aunque no haya conexión, con un aviso de que los mensajes no se pueden "
        "actualizar. Si hubiera que elegir solo entre las dos de la guía, sería Network-First, con el caché como último recurso para mostrar el "
        "historial ya recibido. Para avisar de mensajes nuevos con la app cerrada, la propia documentación propone los mensajes push (Archibald, 2014), "
        "que esta guía menciona pero no pide.")
    doc.parrafo(
        "<b>Idea común.</b> La elección no se hace por aplicación, sino por tipo de recurso: lo que no cambia se sirve del caché; lo que cambia, "
        "de la red. Un mismo Service Worker puede aplicar estrategias distintas según la ruta de cada petición, como en el blog, donde los artículos "
        "y los estilos siguen reglas diferentes.")


# --------------------------------------------------------------------------- conclusiones y referencias
def conclusiones(doc: Documento) -> None:
    a = PARTE_A
    doc.titulo(1, "Conclusiones")
    doc.parrafo(
        "Un Service Worker es un intermediario entre la app y la red que se instala una vez, se activa cuando la versión anterior deja de "
        "usarse y desde entonces decide cómo responder cada petición. El de la guía, con Cache-First, quedó activo, sin errores en la consola, "
        f"y con un caché de siete entradas que coincide con la lista de archivos del código; la primera carga no quedó controlada y las siguientes sí.")
    doc.parrafo(
        f"Con la casilla «Offline» marcada, la página recargada se sirvió completa desde el Service Worker: {len(a['sinConexion']['registroDeRed'])} "
        "recursos más el documento, con 0 B transferidos. Al actualizar la versión se observó la fase de espera y cómo <i>activate</i> deja "
        "solo el caché nuevo.")
    doc.parrafo(
        "El desafío mostró la diferencia entre las dos estrategias con datos: ante un cambio en el servidor, Cache-First siguió mostrando la versión "
        "guardada y Network-First mostró la nueva y actualizó su copia; con el servidor detenido, las dos cargaron la página. Por eso la elección "
        "depende del tipo de contenido: caché para lo que no cambia, red para lo que debe estar al día.")
    doc.parrafo(
        "Las limitaciones del trabajo son tres. Las notificaciones push no se implementaron porque la guía no las pide. Las pruebas corrieron en un "
        "solo navegador, Chrome 155 sin ventana, con un servidor local; no se midió la latencia con redes lentas ni se probó en otros navegadores. Y la "
        "actualización de versión se activó con el comando <i>skipWaiting</i> del protocolo de DevTools y no con un clic en el botón.")


def referencias(doc: Documento) -> None:
    doc.titulo(1, "Referencias", salto_antes=True)
    refs = (
        [("Archibald, J. (2014, 9 de diciembre). ", False), ("Common techniques to build offline applications", True),
         (". web.dev. https://web.dev/articles/offline-cookbook", False)],
        [("Archibald, J. (2016, 29 de septiembre). ", False), ("The service worker lifecycle", True),
         (". web.dev. https://web.dev/articles/service-worker-lifecycle", False)],
        [("Basques, K., y Emelianova, S. (2016, 25 de julio). ", False), ("Debug Progressive Web Apps", True),
         (". Chrome for Developers. https://developer.chrome.com/docs/devtools/progressive-web-apps", False)],
        [("Chrome for Developers. (2021, 24 de septiembre). ", False), ("Strategies for service worker caching", True),
         (". Workbox. https://developer.chrome.com/docs/workbox/caching-strategies-overview", False)],
        [("Google. (s.\u00a0f.). ", False), ("Google Chrome", True), (" (Versión 155) [Software]. https://www.google.com/chrome/", False)],
        [(f"MDN Web Docs. ({SF}-a). ", False), ("Service Worker API", True),
         (". Mozilla. https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API", False)],
        [(f"MDN Web Docs. ({SF}-b). ", False), ("Using Service Workers", True),
         (". Mozilla. https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers", False)],
        [("Microsoft. (s.\u00a0f.). ", False), ("Visual Studio Code", True), (" (Versión 1.142.0) [Software]. https://code.visualstudio.com", False)],
        [("Universidad Manuela Beltrán. (2026). ", False), ("Guía de laboratorio n.º 5: Service Worker", True),
         (" [Guía de laboratorio, módulo 2: PWA, Nuevas Tecnologías del Desarrollo]. UMB.", False)],
    )
    for partes in refs:
        agregar_referencia(doc.d, partes)
