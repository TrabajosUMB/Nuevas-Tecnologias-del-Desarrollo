"""Contenido del informe del Lab 3 «Solidity y contratos» (estilo UMB, APA 7).

Las cifras de gas y los resultados salen de las capturas reales de Remix guardadas en evidencia/ (ver DATOS); las comprobaciones
aritméticas se verifican al construir el documento.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, r"C:\Users\cuent\Documents\Universidad\Katherin\2026-02\Sistemas Transaccionales\herramientas_doc\build")
sys.path.insert(0, r"C:\Users\cuent\.claude\skills\umb-documento\references")

from docx.shared import Pt  # noqa: E402

from constructor import Documento  # noqa: E402
from corregir_docx import agregar_referencia, cabecera_azul, crear_estilo_codigo  # noqa: E402

AQUI = pathlib.Path(__file__).resolve().parent.parent
FIG = AQUI / "figuras"
CONTRATOS = AQUI / "contratos"
SF = "s.\u00a0f."
NBSP = "\u00a0"

# Valores leídos de las capturas de Remix (evidencia/); entre paréntesis, la captura de donde salen.
DATOS = {
    "mensaje_inicial": "Hola Blockchain!",
    "mensaje_nuevo": "Mensaje actualizado desde Remix",       # 04c, 04e
    "precio_prueba": 1000000,                                  # 05b, 05c
    "gas_transaccion": 50708,                                  # 06a: transaction cost de cambiarMensaje
    "gas_ejecucion": 28864,                                    # 06a: execution cost de cambiarMensaje
    "gas_lectura": 2447,                                       # 06b: execution cost de la llamada contador()
    "gas_base": 21000,                                         # ethereum.org (2026a): transferencia estándar
    "gas_byte_no_cero": 16,                                    # EIP-2028
    "gas_byte_cero": 4,
    "bloque": 2,                                               # 06a
}


def T(clave: str) -> str:
    return "{T:" + clave + "}"


def F(clave: str) -> str:
    return "{F:" + clave + "}"


def n(valor: int) -> str:
    """Entero con punto de miles (formato español)."""
    return f"{valor:,}".replace(",", ".")


def tabla_umb(doc: Documento, *args, **kwargs):
    kwargs.setdefault("negrita_primera_col", True)
    kwargs.setdefault("sombrear_primera_col", True)
    t = doc.tabla(*args, **kwargs)
    cabecera_azul(t)
    return t


def codigo(doc: Documento, texto: str) -> None:
    for linea in texto.rstrip("\n").split("\n"):
        doc.d.add_paragraph(linea if linea else " ", style="Codigo")


def descomponer_calldata(mensaje: str) -> tuple[int, int, int]:
    """Bytes de entrada de cambiarMensaje(string): selector (4) + desplazamiento (32) + longitud (32) + texto relleno a 32 bytes.

    Devuelve (total, distintos de cero, en cero). El selector se toma como 4 bytes distintos de cero y se comprueba contra el
    costo medido por Remix (ver verificar_gas).
    """
    texto = len(mensaje.encode("utf-8"))
    palabras_texto = -(-texto // 32) * 32
    total = 4 + 32 + 32 + palabras_texto
    no_cero = 4 + 1 + 1 + texto          # selector + 0x20 + longitud (< 256) + bytes del texto
    return total, no_cero, total - no_cero


def verificar_gas() -> dict[str, int]:
    total, no_cero, cero = descomponer_calldata(DATOS["mensaje_nuevo"])
    datos = no_cero * DATOS["gas_byte_no_cero"] + cero * DATOS["gas_byte_cero"]
    suma = DATOS["gas_base"] + datos + DATOS["gas_ejecucion"]
    assert suma == DATOS["gas_transaccion"], f"la descomposición ({suma}) no coincide con el costo medido ({DATOS['gas_transaccion']})"
    return {"bytes": total, "no_cero": no_cero, "cero": cero, "datos": datos, "suma": suma}


# --------------------------------------------------------------------------- portada, listas e introducción
def introduccion(doc: Documento) -> None:
    doc.titulo(1, "Introducción", salto_antes=True)
    doc.parrafo(
        "Este informe documenta la guía de laboratorio n.º 3, «Solidity y contratos», del módulo de aplicaciones multiplataforma de Nuevas "
        f"Tecnologías del Desarrollo. El objetivo de la guía es comprender qué es un contrato inteligente, conocer el lenguaje Solidity, y "
        f"escribir, desplegar y probar un contrato básico con Remix IDE (Universidad Manuela Beltrán [UMB], 2026).")
    doc.parrafo(
        "El trabajo se hizo sobre el contrato de ejemplo de la guía, que guarda un mensaje, un propietario y un contador. Se compiló, se "
        "desplegó en una cadena simulada y se probó. Después se modificó para agregar un precio, y se midió con cifras reales cuánto cuesta "
        "una escritura frente a una lectura, para responder la pregunta de reflexión. También se diseñó un contrato para un caso del entorno "
        "universitario, apoyado en la lectura previa sobre el proyecto Esbrinachain del libro <i>Blockchain práctico</i>.")
    doc.parrafo(
        f"Todas las capturas son de ejecuciones reales de Remix; en la sección 2.1 se explica el entorno y cómo se operó. La {T('datos')} reúne "
        f"los datos de la práctica y la {T('entregable')} indica dónde está cada elemento del entregable.")
    tabla_umb(doc, "datos", "Datos de la práctica", ["Campo", "Valor"], [
        ("Grupo", "Grupo 6"),
        ("Integrante 1", "Rodríguez Ángel, Santiago"),
        ("Integrante 2", "Olaya Rojas, Santiago"),
        ("Fecha de ejecución", "14 de octubre de 2026"),
        ("Asignatura", "Nuevas Tecnologías del Desarrollo, módulo 1: Aplicaciones multiplataforma"),
        ("Guía", "Guía de laboratorio n.º 3: Solidity y contratos (Smart Contracts, lenguaje Solidity, Remix IDE)"),
    ], [1.6, 4.9], tam=9.5, nota="Elaboración propia con base en la guía (UMB, 2026).")
    tabla_umb(doc, "entregable", "Dónde está cada elemento del entregable", ["Elemento del entregable", "Dónde está"], [
        ("1. Captura de Remix con el contrato original funcionando (mensaje y contador)", f"{F('original')} y {F('consola')}, sección 2.5"),
        ("2. Código del contrato modificado con la variable precio (.sol)", "Sección 2.6, Anexo B y archivo contratos/MiContrato_v2.sol"),
        ("3. Captura del contrato modificado desplegado y funcionando", f"{F('compilacion2')} y {F('modificado')}, sección 2.6"),
        ("4. Respuesta escrita a la reflexión del Paso 4", "Sección 2.7"),
        ("5. Diseño del contrato inteligente universitario del Paso 1", f"Sección 2.2, {F('estados')} y tablas de la sección"),
    ], [3.4, 3.1], tam=9.5, nota="Elaboración propia con base en el entregable de la guía (UMB, 2026).")


# --------------------------------------------------------------------------- 1. marco conceptual
ELEMENTOS = (
    ("<i>// SPDX-License-Identifier: MIT</i>", "Indica la licencia del código fuente (MIT)."),
    ("<i>pragma solidity ^0.8.0;</i>", "Versión del compilador admitida: desde la 0.8.0 hasta antes de la 0.9.0. Remix usó la 0.8.34."),
    ("<i>contract MiPrimerContrato</i>", "Agrupa código (funciones) y datos (estado) que residen en una dirección de la cadena "
                                          "(Solidity, s.\u00a0f.-b)."),
    ("<i>string public mensaje;</i><br/><i>address public propietario;</i><br/><i>uint public contador;</i>",
     "Variables de estado: viven en el almacenamiento (<i>storage</i>), que persiste entre llamadas y transacciones (Solidity, s.\u00a0f.-b). "
     "Al ser <i>public</i>, el compilador crea una función de lectura para cada una (Solidity, s.\u00a0f.-a). <i>uint</i> es un alias de "
     "<i>uint256</i> y <i>address</i> guarda un valor de 20 bytes (Solidity, s.\u00a0f.-c)."),
    ("<i>constructor(string memory _mensajeInicial)</i>", "Se ejecuta una sola vez, cuando se crea el contrato (Solidity, s.\u00a0f.-a). "
                                                        "<i>memory</i> es la ubicación de datos que Solidity exige para tipos por referencia como "
                                                        "<i>string</i> (Solidity, s.\u00a0f.-c)."),
    ("<i>propietario = msg.sender;</i>", "<i>msg.sender</i> es la dirección de la que viene la llamada externa actual (Solidity, s.\u00a0f.-b); en el "
                                         "constructor es la cuenta que despliega el contrato."),
    ("<i>cambiarMensaje(...)</i> y <i>contador++</i>", "Escribe en el almacenamiento. Es una transacción: la envía una cuenta, la "
                                                     "ejecutan los nodos y cuesta gas."),
    ("<i>obtenerContador() ... view</i>", "<i>view</i> promete no modificar el estado (Solidity, s.\u00a0f.-a); por eso solo lee."),
)


def marco_conceptual(doc: Documento) -> None:
    doc.titulo(1, "1. Marco conceptual")
    doc.titulo(2, "1.1 Contrato inteligente")
    doc.parrafo(
        "Un contrato inteligente es un programa que se ejecuta en la blockchain de Ethereum: un conjunto de código (sus funciones) y datos "
        "(su estado) que reside en una dirección específica (ethereum.org, 2026b). Las reglas quedan escritas en el código y se aplican solas "
        "cuando se cumplen las condiciones, sin intermediarios; además, cualquiera puede leer el código y, una vez desplegado, no se modifica "
        f"(UMB, 2026). Por defecto no se pueden eliminar y sus interacciones son irreversibles (ethereum.org, 2026b).")
    doc.parrafo(
        "Tienen un límite importante: por sí solos no pueden obtener información de eventos del mundo real ni recuperar datos de fuentes "
        "externas a la cadena. Para eso se usan oráculos, herramientas que llevan datos externos al contrato (ethereum.org, 2026b). Esa "
        "limitación condiciona el diseño del caso universitario de la sección 2.2.")
    doc.titulo(2, "1.2 Solidity y el contrato de ejemplo")
    doc.parrafo(
        f"Solidity es el lenguaje con el que se escriben contratos para la máquina virtual de Ethereum. La {T('elementos')} explica, elemento "
        f"por elemento, el contrato <i>MiPrimerContrato</i> de la guía, cuyo texto completo está en el Anexo A.")
    tabla_umb(doc, "elementos", "Elementos del contrato MiPrimerContrato", ["Elemento", "Qué hace"],
              [(e.replace("<br/>", "\n"), d) for e, d in ELEMENTOS], [2.3, 4.2], tam=9.5,
              nota="Elaboración propia con base en la guía (UMB, 2026) y en la documentación de Solidity (s.\u00a0f.-a, s.\u00a0f.-b, s.\u00a0f.-c).")
    doc.titulo(2, "1.3 Transacciones, llamadas y gas")
    doc.parrafo(
        "Una transacción es un mensaje que una cuenta envía a otra; se aplica completa o no se aplica (Solidity, s.\u00a0f.-b). Cada transacción "
        "debe pagarse con gas, que mide el esfuerzo computacional de una operación, y lo paga quien origina la transacción. El gas existe para "
        "que la red no sea vulnerable al spam ni se quede atrapada en ciclos de cómputo infinitos (ethereum.org, 2026a; Solidity, s.\u00a0f.-b). El "
        "costo total es el gas usado multiplicado por el precio por unidad, que suma la tarifa base y la propina al validador (ethereum.org, 2026a).")
    doc.parrafo(
        "El almacenamiento es la parte más costosa de la máquina virtual: es comparativamente caro leerlo y más aún inicializarlo y modificarlo "
        "(Solidity, s.\u00a0f.-b). Esta idea es la base de la reflexión de la sección 2.7.")
    doc.titulo(2, "1.4 Lectura previa: el caso Esbrinachain")
    doc.parrafo(
        "La lectura sobre contratos inteligentes del libro <i>Blockchain práctico</i> (sección 3.1) presenta Esbrinachain, un proyecto cuyos "
        "contratos ponen por escrito las reglas del sistema: quién pregunta, quién responde y quién vota, y cuándo. Sirven como ejemplo de "
        f"cómo el contrato de la guía crece hasta un caso real ({T('esbrinachain')}).")
    tabla_umb(doc, "esbrinachain", "Del contrato de la guía al caso Esbrinachain", ["En el contrato de la guía", "En Esbrinachain"], [
        ("<i>propietario = msg.sender</i>", "Un administrador (<i>esbAdmin</i>) y el modificador <i>soloAdmin</i>, que reserva funciones para él."),
        ("Variables de estado como <i>contador</i>", "Contadores (<i>total_preg</i>, <i>total_usuarios</i>) y mapeos de preguntas y usuarios."),
        ("<i>cambiarMensaje</i> (escritura)", "<i>creaPregunta</i>, <i>creaRespuesta</i> y <i>votarRespuesta</i>, que validan plazos, estados y votos únicos."),
        ("<i>obtenerContador</i> (<i>view</i>)", "<i>estadoPreg</i>, que devuelve el estado de una pregunta sin gastar gas."),
        ("(no aparece en la guía)", "Funciones <i>payable</i>: la recompensa de cada pregunta queda en el saldo del contrato."),
        ("Un solo contrato", "Tres contratos con herencia: preguntar, responder y el principal, que hereda de los dos."),
    ], [2.4, 4.1], tam=9.5, nota="Elaboración propia con base en la lectura del libro <i>Blockchain práctico</i>, sección 3.1.")
    doc.parrafo(
        "Dos ideas de esa lectura se aprovechan en el diseño de la sección 2.2. La primera es que los plazos se comprueban cuando alguien "
        "llama al contrato: el contrato no tiene un reloj que lo despierte, y por ejemplo la pregunta pasa a votación cuando llega la primera "
        "respuesta fuera de plazo. La segunda es que el tamaño del contrato y el gas obligan a ser austero: cada contrato tiene un límite de "
        "tamaño, los ciclos deben ser cortos y finitos, y conviene acortar mensajes de error y evitar variables innecesarias.")


# --------------------------------------------------------------------------- 2. desarrollo
def entorno(doc: Documento) -> None:
    doc.titulo(1, "2. Desarrollo del laboratorio", salto_antes=True)
    doc.titulo(2, "2.1 Entorno y método de ejecución")
    doc.parrafo(
        "El laboratorio se ejecutó en Remix IDE, el entorno en línea que pide la guía. La dirección remix.ethereum.org redirigió a "
        "app.remix.live, y la propia aplicación mostró el aviso «Welcome to the new home of Remix». Las acciones sobre la interfaz (crear el "
        "archivo, pegar el código, compilar, desplegar y llamar las funciones) las hizo un script que controla Microsoft Edge mediante el "
        "protocolo Chrome DevTools, y las capturas son recortes de esa ejecución real, sin retoques. En el cuadro de preferencias de Remix se "
        "desactivaron la analítica de rendimiento y el asistente de inteligencia artificial; la analítica anónima que Remix marca como "
        f"necesaria no se puede desactivar. La {T('entorno')} resume el entorno.")
    tabla_umb(doc, "entorno", "Entorno de ejecución del laboratorio", ["Parámetro", "Valor"], [
        ("Fecha de ejecución", "14 de octubre de 2026"),
        ("IDE", "Remix IDE 2.6.6 (app.remix.live)"),
        ("Compilador de Solidity", "0.8.34+commit.80d5c536"),
        ("Entorno de ejecución", "Remix VM (Cancun), una cadena simulada"),
        ("Cuenta de prueba", "Account 1, 0x5B38Da6a701c568545dCfcB03FcB875f56beddC4, con 100 ETH simulados"),
        ("Navegador", "Microsoft Edge 155, controlado por script (herramientas/cdp.mjs)"),
    ], [1.8, 4.7], tam=9.5, nota="Elaboración propia con datos de la ejecución en <i>Remix IDE</i> (s.\u00a0f.).")
    doc.parrafo(
        "La guía pide «Remix VM (Cancun)». Esta versión de Remix trae «Osaka» como versión de la EVM por defecto, así que se seleccionó "
        "Cancun en el menú desplegable para seguir el procedimiento tal como está escrito.")


def paso1(doc: Documento) -> None:
    doc.titulo(2, "2.2 Paso 1. Contrato inteligente universitario: EntregaEvidencias")
    doc.parrafo(
        "<b>Actividad.</b> La guía pide diseñar un contrato inteligente para un caso real del entorno universitario, definiendo las condiciones, "
        "las partes y qué se ejecuta automáticamente. Se desarrolló el ejemplo de la guía (registrar la nota 5,0 a quien sube todas las "
        "evidencias antes de la fecha límite) hasta un diseño con reglas completas, a partir de lo aprendido en la lectura de Esbrinachain.")
    doc.parrafo(
        f"<b>Partes.</b> Intervienen cuatro actores ({T('partes')}). El docente cumple el papel del administrador de Esbrinachain y el "
        f"estudiante, el del usuario que actúa sobre sus propios datos.")
    tabla_umb(doc, "partes", "Partes y responsabilidades del contrato EntregaEvidencias", ["Parte", "Rol", "Qué puede hacer"], [
        ("Docente", "Administrador del contrato", "Configura la fecha límite, el número de evidencias requeridas y el plazo de revisión; anula una entrega, "
                                                  "con motivo, dentro del plazo de revisión."),
        ("Estudiante", "Usuario", "Registra la huella (<i>hash</i>) de cada evidencia, una sola vez, y consulta su estado y su nota."),
        ("Contrato", "Árbitro automático", "Verifica la fecha y la cantidad, cambia el estado, registra la nota y emite eventos."),
        ("Coordinación académica", "Observador", "Consulta el estado de cualquier entrega: la lectura es pública y no gasta gas."),
    ], [1.4, 1.6, 3.5], tam=9.5, nota="Elaboración propia.")
    doc.parrafo(
        f"<b>Condiciones y ejecución automática.</b> La {T('condiciones')} enumera las condiciones y lo que el contrato ejecuta solo en cada "
        f"caso, y la {F('estados')} muestra los estados por los que pasa una entrega.")
    tabla_umb(doc, "condiciones", "Condiciones y acciones que ejecuta el contrato", ["Condición", "Qué ejecuta el contrato"], [
        ("1. El docente fija la fecha límite, las N evidencias requeridas y el plazo de revisión.", "Guarda los parámetros. Solo el docente puede "
                                                                                                   "(modificador <i>soloDocente</i>)."),
        ("2. El estudiante registra una evidencia antes de la fecha límite y su huella no estaba registrada.", "Guarda la huella y el momento del bloque, "
                                                                                                              "suma una evidencia y emite <i>EvidenciaRegistrada</i>."),
        ("3. El número de evidencias llega a N antes de la fecha límite.", "Pasa la entrega a <i>Completa</i>, registra la nota 5,0 y emite "
                                                                           "<i>NotaRegistrada</i>."),
        ("4. Pasa la fecha límite sin llegar a N.", "La entrega se evalúa como <i>Vencida</i> cuando alguien la consulta o intenta registrar; no se "
                                                    "registra nota automática."),
        ("5. El docente detecta un problema dentro del plazo de revisión.", "Pasa la entrega a <i>Anulada</i>, deja la nota en 0 y emite el motivo en "
                                                                            "<i>EntregaAnulada</i>."),
        ("6. Alguien intenta algo fuera de las reglas (evidencia repetida, fecha vencida, no ser el docente).", "Revierte la transacción y no cambia "
                                                                                                               "nada."),
    ], [3.3, 3.2], tam=9.5, nota="Elaboración propia.")
    doc.figura("estados", "Estados de una entrega en el contrato EntregaEvidencias", FIG / "fig1_estados_contrato_universitario.png",
               nota="Elaboración propia. N es el número de evidencias requeridas que fija el docente.")
    doc.parrafo(
        f"<b>Funciones propuestas.</b> La {T('funciones')} resume la interfaz del contrato. La nota se guardaría como un entero en décimas "
        f"(5,0 se representa como 50), porque en Solidity se trabaja con enteros.")
    tabla_umb(doc, "funciones", "Funciones propuestas del contrato EntregaEvidencias", ["Función", "Quién", "Tipo", "Efecto"], [
        ("<i>configurar(fechaLimite, requeridas, plazoRevision)</i>", "Docente", "Escritura", "Guarda los parámetros antes de abrir la entrega."),
        ("<i>registrarEvidencia(bytes32 huella)</i>", "Estudiante", "Escritura (paga gas)", "Registra una evidencia y, si completa las N a tiempo, "
                                                                                             "registra la nota."),
        ("<i>anularEntrega(address estudiante, string motivo)</i>", "Docente", "Escritura", "Anula una entrega completa dentro del plazo de revisión."),
        ("<i>estadoEntrega(address estudiante)</i>", "Cualquiera", "<i>view</i> (sin gas)", "Devuelve el estado, la cantidad de evidencias y la nota."),
    ], [2.5, 0.9, 1.1, 2.0], tam=9, nota="Elaboración propia. Es una interfaz de diseño: no se implementó ni se desplegó en este laboratorio.")
    doc.parrafo("<b>Decisiones de diseño.</b> Seis decisiones sostienen la coherencia del contrato:")
    for texto in (
        "<b>Huella en lugar de archivo.</b> El contrato no puede abrir un archivo ni consultar el aula virtual, porque los contratos no recuperan "
        "datos externos a la cadena (ethereum.org, 2026b). Por eso solo guarda la huella de cada evidencia, que sirve de prueba de que existía en "
        "ese momento sin exponer su contenido.",
        "<b>Tiempo del bloque.</b> La fecha de cada registro la da la cadena, no el reloj del estudiante, lo que evita discusiones sobre cuándo se entregó.",
        "<b>Plazos evaluados al llamar.</b> Como en Esbrinachain, el contrato no tiene reloj propio: el estado <i>Vencida</i> se determina cuando "
        "alguien consulta o intenta registrar.",
        "<b>Una nota que certifica entrega, no calidad.</b> El 5,0 automático significa «entregó todo a tiempo»; la calificación académica sigue siendo "
        "decisión del docente, y por eso existen el plazo de revisión y la anulación.",
        "<b>Sin datos personales en la cadena.</b> Lo que se escribe no se puede borrar (ethereum.org, 2026b), de modo que se guardan direcciones y "
        "huellas, no nombres.",
        "<b>Costo del gas.</b> Cada registro es una transacción que cuesta gas (sección 2.7); en un uso real convendría una red de pruebas o una red "
        "privada de la universidad.",
    ):
        doc.parrafo(texto)


def paso2_3(doc: Documento) -> None:
    doc.titulo(2, "2.3 Paso 2. Crear el contrato en Remix")
    doc.parrafo(
        "En el explorador de archivos de Remix se creó <i>MiContrato.sol</i> dentro de la carpeta <i>contracts</i> del espacio de trabajo "
        "<i>default_workspace</i> y se pegó el contrato de la guía. El código se extrajo por programa del documento de la guía, de modo que el "
        "contrato probado es exactamente el que ella entrega (Anexo A). El editor lo mostró sin líneas rojas ({F:compilacion1}).")
    doc.titulo(2, "2.4 Paso 3. Compilar el contrato")
    doc.parrafo(
        "En el panel del compilador, la versión seleccionada fue la 0.8.34, que cumple la condición de la guía (0.8.0 o superior) y el "
        "<i>pragma ^0.8.0</i> del contrato. Al pulsar «Compile MiContrato.sol», el icono del compilador mostró la marca verde y el contrato "
        f"<i>MiPrimerContrato</i> quedó disponible para desplegar ({F('compilacion1')}).")
    doc.figura("compilacion1", "Compilación de MiContrato.sol sin errores", FIG / "fig2_compilacion_original.png",
               nota="Captura real de Remix IDE 2.6.6: marca verde en el icono del compilador, versión 0.8.34 y el contrato MiPrimerContrato seleccionado.")


def paso4_original(doc: Documento) -> None:
    d = DATOS
    doc.titulo(2, "2.5 Paso 4. Despliegue y pruebas del contrato original")
    doc.parrafo(
        f"Se siguió el procedimiento de la guía en Remix VM (Cancun). La {T('pruebas')} muestra cada acción y su resultado. Remix muestra el "
        f"resultado de una sola función a la vez, por eso las lecturas se presentan como cuatro capturas ({F('original')}), y las transacciones, "
        f"en la consola ({F('consola')}).")
    tabla_umb(doc, "pruebas", "Pruebas del contrato original en Remix VM (Cancun)", ["Acción", "Resultado observado", "Evidencia"], [
        ("Constructor con el mensaje «" + d["mensaje_inicial"] + "» y Deploy", "Transacción de creación exitosa; contrato en 0xd91…39138.", F("consola") + "a"),
        ("Botón <i>mensaje</i>", "0: string: " + d["mensaje_inicial"], F("original") + "a"),
        ("Botón <i>contador</i>", "0: uint256: 0", F("original") + "b"),
        ("<i>cambiarMensaje</i> con «" + d["mensaje_nuevo"] + "»", f"Transacción exitosa en el bloque {d['bloque']}.", F("consola") + "b"),
        ("Botón <i>contador</i>", "0: uint256: 1", F("original") + "c"),
        ("Botón <i>mensaje</i>", "0: string: " + d["mensaje_nuevo"], F("original") + "d"),
    ], [2.5, 2.8, 1.2], alinear=["l", "l", "c"], tam=9.5, nota="Elaboración propia con los resultados mostrados por Remix.")
    doc.figura("original", "Contrato original funcionando: mensaje y contador", FIG / "fig3_contrato_original_funcionando.png",
               nota="Recortes reales del panel de contratos desplegados de Remix, en orden cronológico. En d) el texto se parte en dos líneas por el "
                    "ancho del panel.")
    doc.figura("consola", "Transacciones registradas en la consola de Remix", FIG / "fig4_transacciones_consola.png",
               nota="Recortes reales de la consola. Cada transacción exitosa lleva la marca verde. La transacción c) corresponde al contrato modificado "
                    "de la sección 2.6.")
    doc.parrafo(
        "El contador pasó de 0 a 1 por una sola llamada a <i>cambiarMensaje</i>, y el mensaje cambió: el estado del contrato quedó guardado entre "
        "una transacción y la siguiente. Las lecturas, en cambio, no generaron transacciones nuevas: en la consola aparecen como «CALL» (sección 2.7).")


def modificacion(doc: Documento) -> None:
    d = DATOS
    doc.titulo(2, "2.6 Actividad: agregar precio y establecerPrecio")
    doc.parrafo(
        "La actividad pide agregar una variable <i>uint</i> llamada <i>precio</i> y una función <i>establecerPrecio(uint _precio)</i> que la "
        "modifique. Se hizo con el mismo patrón que <i>mensaje</i> y <i>cambiarMensaje</i>: una variable de estado pública, que crea sola su "
        "función de lectura, y una función que escribe en ella. Los fragmentos agregados son estos; el contrato completo está en el Anexo B.")
    codigo(doc, "uint public precio;  // NUEVA: precio almacenado en el contrato\n\n"
                "// NUEVA: funcion para establecer el precio (escribe en la blockchain)\n"
                "function establecerPrecio(uint _precio) public {\n    precio = _precio;\n}")
    doc.parrafo(
        f"El contrato se compiló sin errores ({F('compilacion2')}) y se desplegó como una instancia nueva, en 0xf8e…9fBe8, con el mismo mensaje "
        f"inicial. Las funciones de la instancia incluyen ahora <i>establecerPrecio</i> y <i>precio</i>, que la instancia anterior no tenía. Se "
        f"llamó <i>establecerPrecio({d['precio_prueba']})</i>, una transacción exitosa ({F('consola')}c), y luego <i>precio</i>, que devolvió "
        f"{d['precio_prueba']} ({F('modificado')}).")
    doc.figura("compilacion2", "Contrato modificado compilado sin errores", FIG / "fig5_compilacion_modificado.png",
               nota="Captura real de Remix: el editor muestra la variable precio y la función establecerPrecio, y el compilador la marca verde.")
    doc.figura("modificado", "Contrato modificado desplegado y funcionando", FIG / "fig6_contrato_modificado_funcionando.png",
               nota="Recortes reales del panel de contratos desplegados: la escritura de precio y su lectura.")


def reflexion(doc: Documento) -> None:
    d = DATOS
    v = verificar_gas()
    doc.titulo(2, "2.7 Reflexión: por qué escribir cuesta gas y leer no")
    doc.parrafo(
        "<b>Pregunta.</b> Cada vez que se llama a <i>cambiarMensaje</i> se genera una transacción que cuesta gas. ¿Por qué las operaciones de "
        "escritura en la blockchain cuestan dinero pero las de lectura son gratuitas?")
    doc.parrafo(
        "<b>Respuesta.</b> Una escritura cambia el estado compartido de la red, y ese cambio lo deben ejecutar, verificar y guardar todos los "
        "nodos; además queda en el almacenamiento, que es la parte más cara de la máquina virtual (Solidity, s.\u00a0f.-b). El gas pone precio a ese "
        "trabajo, evita el spam y los ciclos infinitos, y compensa a quienes validan (ethereum.org, 2026a). Una lectura, en cambio, solo consulta "
        "la copia local del estado que ya tiene un nodo: no cambia nada, no necesita consenso y no genera una transacción.")
    doc.parrafo(
        f"Las mediciones de Remix lo muestran ({F('gas')}). La transacción <i>cambiarMensaje</i> costó {n(d['gas_transaccion'])} gas. La "
        f"llamada <i>contador()</i> no creó ninguna transacción: Remix muestra un costo de ejecución de {n(d['gas_lectura'])} gas con la nota "
        f"«Cost only applies when called by a contract», es decir, ese costo solo se aplicaría si otro contrato la invocara dentro de una "
        f"transacción. Por eso la gratuidad de la lectura tiene una condición: una función <i>view</i> es gratis al consultarla desde fuera, "
        f"pero no cuando forma parte de una transacción.")
    doc.figura("gas", "Costo de una escritura frente a una lectura en Remix", FIG / "fig7_gas_escritura_vs_lectura.png",
               nota="Recortes reales del detalle de la consola de Remix: a) la transacción cambiarMensaje y b) la llamada contador().")
    doc.parrafo(
        f"Los {n(d['gas_transaccion'])} gas de la escritura se pueden descomponer y la suma coincide con la medida ({T('gasdesglose')}).")
    tabla_umb(doc, "gasdesglose", "Descomposición del costo de la transacción cambiarMensaje", ["Concepto", "Gas", "Cómo se obtiene"], [
        ("Costo base de toda transacción", n(d["gas_base"]), "Mínimo que cuesta una transacción: la transferencia estándar de ETH requiere "
                                                              "exactamente 21.000 (ethereum.org, 2026a)."),
        ("Datos de entrada", n(v["datos"]), f"{v['bytes']} bytes: {v['no_cero']} distintos de cero a {d['gas_byte_no_cero']} gas y {v['cero']} en cero a "
                                            f"{d['gas_byte_cero']} gas (Akhunov et al., 2019)."),
        ("Ejecución de la función", n(d["gas_ejecucion"]), "<i>Execution cost</i> de Remix: incluye escribir <i>mensaje</i> y <i>contador</i> en el "
                                                            "almacenamiento."),
        ("Total (<i>transaction cost</i>)", n(v["suma"]), "Suma de los tres conceptos; coincide con el valor de Remix."),
    ], [2.0, 0.8, 3.7], alinear=["l", "c", "l"], tam=9.5,
        nota="Elaboración propia con las cifras de Remix y las reglas de cobro de los datos de entrada. Los 100 bytes son el selector de la función (4), "
             "el desplazamiento (32), la longitud (32) y el texto de 31 caracteres relleno a 32 bytes.")
    doc.parrafo(
        "La conclusión práctica es que el costo de una escritura depende de cuánto se guarda y cuántas veces se hace. Por eso en los contratos "
        "reales, como Esbrinachain, se recomienda evitar variables innecesarias y ciclos largos, y por eso el diseño de la sección 2.2 guarda "
        "una huella de 32 bytes por evidencia y no el archivo.")


# --------------------------------------------------------------------------- conclusiones, referencias, anexos
def conclusiones(doc: Documento) -> None:
    d = DATOS
    doc.titulo(1, "Conclusiones")
    doc.parrafo(
        "Un contrato inteligente es código y datos que residen en una dirección de la cadena y que aplican reglas escritas de antemano, sin "
        "intermediarios. El contrato de la guía reúne los elementos básicos de Solidity: variables de estado, un constructor que se ejecuta una "
        "vez, funciones que escriben y funciones <i>view</i> que solo leen.")
    doc.parrafo(
        f"El contrato compiló sin errores con la versión 0.8.34, se desplegó en Remix VM (Cancun) y se comportó como se esperaba: el mensaje "
        f"inicial se leyó, el contador pasó de 0 a 1 tras una transacción y el mensaje cambió. La modificación con <i>precio</i> y "
        f"<i>establecerPrecio</i> siguió el mismo patrón y devolvió {n(d['precio_prueba'])} al leerla.")
    doc.parrafo(
        f"Las mediciones de Remix respondieron la reflexión con datos: una escritura costó {n(d['gas_transaccion'])} gas, de los cuales "
        f"{n(d['gas_base'])} son el mínimo de toda transacción, y una lectura externa no generó transacción alguna. La lectura solo cuesta gas si "
        f"la invoca otro contrato.")
    doc.parrafo(
        "El diseño de <i>EntregaEvidencias</i> aplica lo aprendido: roles con modificadores, estados y plazos evaluados al llamar, una huella en vez "
        "del archivo y una nota que certifica la entrega, no la calidad. Su límite principal es que un contrato no puede verificar el contenido de "
        "una evidencia, por lo que se mantiene la revisión humana.")


def referencias(doc: Documento) -> None:
    doc.titulo(1, "Referencias", salto_antes=True)
    refs = (
        [("Akhunov, A., Ben Sasson, E., Brand, T., Guthmann, L., y Levy, A. (2019). ", False), ("EIP-2028: Transaction data gas cost reduction", True),
         (". Ethereum Improvement Proposals. https://eips.ethereum.org/EIPS/eip-2028", False)],
        [("Blockchain práctico", True), (f". ({SF}). [Libro; lectura previa del Lab 3, sección 3.1 «Smart Contracts»].", False)],
        [("ethereum.org. (2026a, 24 de junio). ", False), ("Gas and fees", True), (". https://ethereum.org/developers/docs/gas/", False)],
        [("ethereum.org. (2026b, 25 de febrero). ", False), ("Introduction to smart contracts", True),
         (". https://ethereum.org/developers/docs/smart-contracts/", False)],
        [("Remix IDE", True), (f" (Versión 2.6.6) [Software]. ({SF}). https://app.remix.live", False)],
        [(f"Solidity. ({SF}-a). ", False), ("Contracts", True), (". Solidity Documentation. https://docs.soliditylang.org/en/latest/contracts.html", False)],
        [(f"Solidity. ({SF}-b). ", False), ("Introduction to smart contracts", True),
         (". Solidity Documentation. https://docs.soliditylang.org/en/latest/introduction-to-smart-contracts.html", False)],
        [(f"Solidity. ({SF}-c). ", False), ("Types", True), (". Solidity Documentation. https://docs.soliditylang.org/en/latest/types.html", False)],
        [("Universidad Manuela Beltrán. (2026). ", False), ("Guía de laboratorio n.º 3: Solidity y contratos", True),
         (" [Guía de laboratorio, módulo 1: Aplicaciones multiplataforma, Nuevas Tecnologías del Desarrollo]. UMB.", False)],
    )
    for partes in refs:
        agregar_referencia(doc.d, partes)


def anexos(doc: Documento) -> None:
    anexos_ = (
        ("Anexo A. Contrato original (MiContrato.sol)", CONTRATOS / "MiContrato.sol",
         "Contrato de la guía, extraído por programa del documento de la guía y probado en Remix."),
        ("Anexo B. Contrato modificado (MiContrato_v2.sol)", CONTRATOS / "MiContrato_v2.sol",
         "Contrato con la variable <i>precio</i> y la función <i>establecerPrecio</i>, probado en Remix."),
    )
    for i, (titulo, ruta, descripcion) in enumerate(anexos_):
        doc.titulo(1, titulo, salto_antes=True)
        doc.parrafo(descripcion)
        codigo(doc, ruta.read_text(encoding="utf-8"))


def estilo_codigo(doc: Documento) -> None:
    crear_estilo_codigo(doc.d).font.size = Pt(8.5)
