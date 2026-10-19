// Ejecuta de verdad el laboratorio 5 en Google Chrome y guarda evidencia/resultados.json y las capturas.
//
// Parte A (Cache-First, pasos 3 y 4 de la guía): la app corre en una pestaña y el panel real de Chrome DevTools (frontend servido por el propio
//   Chrome) se abre en otra conectada a ella. Se capturan Application > Service workers, la Consola, Application > Cache storage y la prueba
//   sin conexión con la casilla «Offline» de DevTools, más una actualización de versión del caché.
// Parte B (desafío): se compara Cache-First con Network-First con una página que cambia en el servidor y con el servidor detenido.
//
// Requiere Chrome abierto con lanzar_chrome.ps1 (puerto 9336). Uso: node ejecutar_laboratorio.mjs
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { BUSCAR_PROFUNDO, PUERTO_CDP, cerrarPestana, conectar, dormir, listarObjetivos, nuevaPestana } from './cdp_lib.mjs';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const RAIZ = path.join(AQUI, '..');
const PROYECTO = path.join(RAIZ, 'proyecto');
const TRABAJO = path.join(RAIZ, 'trabajo_pruebas');
const EVIDENCIA = path.join(RAIZ, 'evidencia');
const PUERTO_WEB = 8095;
const ANCHO_DEVTOOLS = 860;                  // píxeles CSS; con un panel más estrecho el texto de las capturas se lee mejor en el informe
const ALTO_DEVTOOLS = 760;
const ANCHO_APP = 800;
const ALTO_APP = 560;
const FACTOR_PANTALLA = 2;                   // capturas al doble de densidad para que sigan nítidas al reducirlas en el documento
const ORIGEN = `http://localhost:${PUERTO_WEB}`;
const ARCHIVOS_SW = { cacheFirst: 'service-worker.js', networkFirst: 'service-worker-network-first.js' };

fs.mkdirSync(EVIDENCIA, { recursive: true });
const resultados = { generado: new Date().toISOString(), evidencias: [] };

// ------------------------------------------------------------------------------------------ utilidades de archivos y servidor
const leer = (carpeta, nombre) => fs.readFileSync(path.join(carpeta, nombre), 'utf8');
const escribir = (carpeta, nombre, texto) => fs.writeFileSync(path.join(carpeta, nombre), texto, 'utf8');

function copiarProyecto(archivoSw) {
    fs.cpSync(PROYECTO, TRABAJO, { recursive: true, force: true });
    escribir(TRABAJO, 'service-worker.js', leer(PROYECTO, archivoSw));       // el navegador registra siempre «service-worker.js»
}

function cambiarVersion(de, a) {
    const html = leer(TRABAJO, 'index.html');
    if (!html.includes(`<strong>${de}</strong>`)) throw new Error(`index.html no contiene la versión ${de}`);
    escribir(TRABAJO, 'index.html', html.replace(`<strong>${de}</strong>`, `<strong>${a}</strong>`));
}

let servidor = null;
async function iniciarServidor() {
    servidor = spawn('py', [path.join(AQUI, 'servidor.py'), String(PUERTO_WEB), TRABAJO], { stdio: 'ignore', windowsHide: true });
    for (let i = 0; i < 30; i++) {
        await dormir(300);
        try { await fetch(`${ORIGEN}/manifest.json`); return; } catch { /* aún no responde */ }
    }
    throw new Error('el servidor local no arrancó');
}
async function detenerServidor() {
    if (!servidor) return;
    servidor.kill();
    servidor = null;
    for (let i = 0; i < 30; i++) {                                             // se espera a que el puerto quede cerrado
        await dormir(300);
        try { await fetch(`${ORIGEN}/manifest.json`); } catch { return; }
    }
    throw new Error('el servidor local no se detuvo');
}

// ------------------------------------------------------------------------------------------ utilidades de la app en Chrome
async function esperarEstadoSw(app, estado = 'activated', espera = 15000) {
    const limite = Date.now() + espera;
    while (Date.now() < limite) {
        const actual = await app.evaluar(`navigator.serviceWorker.getRegistration().then((r) => (r && r.active ? r.active.state : null))`).catch(() => null);
        if (actual === estado) return true;
        await dormir(300);
    }
    return false;
}

/** Repite la comprobación hasta que sea verdadera o venza el plazo; devuelve si llegó a cumplirse. */
async function esperar(comprobacion, plazoMs) {
    const limite = Date.now() + plazoMs;
    while (Date.now() < limite) {
        if (await comprobacion().catch(() => false)) return true;
        await dormir(300);
    }
    return false;
}

const estadoApp = (app) => app.evaluar(`(async () => {
    const registro = await navigator.serviceWorker.getRegistration();
    return {
        titulo: document.title,
        version: (document.querySelector('#version-contenido strong') || {}).textContent || null,
        estadoRed: (document.getElementById('estado-red') || {}).textContent || null,
        enLinea: navigator.onLine,
        controlada: !!navigator.serviceWorker.controller,
        sw: registro ? { alcance: registro.scope, activo: registro.active ? registro.active.state : null, archivo: registro.active ? new URL(registro.active.scriptURL).pathname : null } : null,
        entregas: document.querySelectorAll('#lista li').length,
    };
})()`);

const estadoCaches = (app) => app.evaluar(`(async () => {
    const salida = {};
    for (const nombre of await caches.keys()) {
        const cache = await caches.open(nombre);
        salida[nombre] = (await cache.keys()).map((r) => new URL(r.url).pathname).sort();
    }
    return salida;
})()`);

const versionEnCache = (app, ruta = '/') => app.evaluar(`caches.match(${JSON.stringify(ruta)}).then(async (r) => {
    if (!r) return null;
    const m = (await r.text()).match(/<strong>(v\\d+)<\\/strong>/);
    return m ? m[1] : null;
})`);

async function cargar(app, url = `${ORIGEN}/`) {
    await app.enviar('Page.navigate', { url });
    await dormir(1800);
}

async function recargar(app, espera = 1800) {
    await app.enviar('Page.reload');
    await dormir(espera);
}

async function limpiarOrigen(app) {
    await app.enviar('Page.navigate', { url: 'about:blank' });
    await dormir(400);
    await app.enviar('Storage.clearDataForOrigin', { origin: ORIGEN, storageTypes: 'all' });
    await dormir(600);
}

// ------------------------------------------------------------------------------------------ utilidades de DevTools
async function abrirDevtools(appId) {
    const url = `http://127.0.0.1:${PUERTO_CDP}/devtools/inspector.html?ws=127.0.0.1:${PUERTO_CDP}/devtools/page/${appId}&panel=resources`;
    const objetivo = await nuevaPestana(url);
    const dev = await conectar(objetivo);
    await dev.fijarVista(ANCHO_DEVTOOLS, ALTO_DEVTOOLS, FACTOR_PANTALLA);
    await dormir(3000);
    // Ajustes del frontend: tema claro, sin vista previa de la pantalla (screencast) e interfaz en inglés, como en la guía.
    await dev.evaluar(`localStorage.clear(); localStorage.setItem('ui-theme', '"default"'); localStorage.setItem('screencast-enabled', 'false'); localStorage.setItem('language', '"en-US"'); true`);
    await dev.enviar('Page.enable');
    await dev.enviar('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] });
    await dev.enviar('Page.reload');
    await dormir(5000);
    await dev.evaluar(BUSCAR_PROFUNDO);
    const aviso = await dev.evaluar(`window.__buscar((e) => e.tagName === 'DEVTOOLS-BUTTON' && (e.innerText || '').startsWith('Don'))`);
    if (aviso) await dev.clic(aviso.x, aviso.y);                               // «DevTools is now available in Spanish» -> Don't show again
    await dormir(500);
    return { dev, objetivo };
}

async function clicBuscado(dev, predicado, descripcion) {
    const r = await dev.evaluar(`window.__buscar((e) => { ${predicado} })`);
    if (!r) throw new Error(`DevTools: no se encontró ${descripcion}`);
    await dev.clic(r.x, r.y);
    return r;
}

const pestanaSuperior = (dev, texto) => clicBuscado(dev, `return (e.innerText || '').trim() === ${JSON.stringify(texto)} && e.children.length === 0 && e.getBoundingClientRect().top < 80;`, `la pestaña ${texto}`);
const itemLateral = (dev, texto) => clicBuscado(dev, `return e.tagName === 'LI' && (e.innerText || '').trim().startsWith(${JSON.stringify(texto)});`, `el elemento lateral ${texto}`);
/** Abre un caché en Application > Cache storage; si el árbol está plegado, lo despliega primero (el estado inicial varía entre ejecuciones). */
async function abrirCache(dev, nombre) {
    const existe = () => dev.evaluar(`!!window.__buscar((e) => e.tagName === 'LI' && (e.innerText || '').trim().startsWith(${JSON.stringify(nombre)}))`);
    if (!(await existe())) {
        await itemLateral(dev, 'Cache storage');
        await dev.tecla('ArrowRight');
        await dormir(800);
    }
    return itemLateral(dev, nombre);
}

const casilla = (dev, texto) => clicBuscado(dev, `return e.tagName === 'LABEL' && (e.innerText || '').trim() === ${JSON.stringify(texto)};`, `la casilla ${texto}`);

/** Deja la casilla en el estado pedido (DevTools recuerda «Offline» entre sesiones) y comprueba que quedó así. */
async function fijarCasilla(dev, texto, marcada) {
    if ((await dev.evaluar(`window.__marcada(${JSON.stringify(texto)})`)) !== marcada) {
        await casilla(dev, texto);
        await dormir(800);
    }
    const final = await dev.evaluar(`window.__marcada(${JSON.stringify(texto)})`);
    if (final !== marcada) throw new Error(`la casilla ${texto} quedó en ${final}, se esperaba ${marcada}`);
}

async function capturar(sesion, nombre, descripcion) {
    const archivo = path.join(EVIDENCIA, nombre);
    await sesion.enviar('Page.bringToFront');                                  // una pestaña oculta no genera cuadros y la captura se cuelga
    await dormir(300);
    await sesion.foto(archivo);
    resultados.evidencias.push({ archivo: nombre, descripcion });
    console.log('  captura:', nombre, new Date().toTimeString().slice(0, 8));
}

const mensajesConsola = (dev) => dev.evaluar(`JSON.stringify(window.__todos((e) => e.classList && e.classList.contains('console-message-text'), 30).map((m) => m.texto))`).then(JSON.parse);

// ------------------------------------------------------------------------------------------ parte A: Cache-First con DevTools
async function parteA(app, appObjetivo) {
    console.log('Parte A: Cache-First y DevTools');
    const a = {};
    copiarProyecto(ARCHIVOS_SW.cacheFirst);
    await limpiarOrigen(app);

    await cargar(app);
    a.swActivado = await esperarEstadoSw(app);
    a.primeraCarga = await estadoApp(app);
    a.caches = await estadoCaches(app);

    const { dev, objetivo } = await abrirDevtools(appObjetivo.id);
    await pestanaSuperior(dev, 'Console');
    await dormir(1200);
    a.consolaDevtools = await mensajesConsola(dev);
    await capturar(dev, '02_devtools_consola.png', 'Console: mensajes del Service Worker y de la app');
    await pestanaSuperior(dev, 'Application');
    await dormir(800);
    await abrirCache(dev, 'mi-pwa-v1');
    await dormir(1800);
    await capturar(dev, '03_devtools_cache_storage.png', 'Application > Cache storage: mi-pwa-v1 con los archivos');

    // La segunda carga ya está controlada por el Service Worker: el panel muestra la pestaña en «Clients».
    await recargar(app, 2000);
    a.recargaControlada = await estadoApp(app);
    await itemLateral(dev, 'Service workers');
    await dormir(1500);
    await capturar(dev, '01_devtools_service_worker.png', 'Application > Service workers: el Service Worker activo y la pestaña controlada');

    // Paso 4: modo sin conexión con la casilla Offline de DevTools
    await fijarCasilla(dev, 'Offline', false);
    await fijarCasilla(dev, 'Offline', true);
    await capturar(dev, '04_devtools_offline_activado.png', 'Application > Service workers con la casilla Offline marcada');
    await pestanaSuperior(dev, 'Network');
    await dormir(1500);
    await recargar(app, 2500);
    a.sinConexion = await estadoApp(app);
    a.sinConexion.registroDeRed = await app.evaluar(`JSON.stringify(performance.getEntriesByType('resource').map((r) => ({ ruta: new URL(r.name).pathname, desdeSw: r.workerStart > 0 })))`).then(JSON.parse);
    await capturar(app, '05_app_sin_conexion.png', 'La app recargada sin conexión: carga completa desde el Service Worker');
    await dev.clic(ANCHO_DEVTOOLS - 150, ALTO_DEVTOOLS - 150);                                                  // quita el foco del filtro para una captura limpia
    await dormir(300);
    await capturar(dev, '06_devtools_network_sin_conexion.png', 'Network: las solicitudes se responden desde el Service Worker con Offline marcado');

    // La app sigue siendo utilizable sin conexión: se agrega una entrega.
    await app.evaluar(`(() => { const campo = document.getElementById('entrega'); campo.value = 'Subir el Lab 5 sin conexión'; document.getElementById('formulario').requestSubmit(); return true; })()`);
    await dormir(500);
    a.sinConexion.entregasTrasAgregar = (await estadoApp(app)).entregas;
    await capturar(app, '07_app_sin_conexion_con_entrega.png', 'La app sin conexión después de agregar una entrega');

    await itemLateral(dev, 'Service workers').catch(() => null);
    await pestanaSuperior(dev, 'Application');
    await dormir(600);
    await itemLateral(dev, 'Service workers');
    await dormir(800);
    await fijarCasilla(dev, 'Offline', false);                                // se desmarca antes de continuar, como pide la guía
    await recargar(app, 1800);
    a.conConexionDeNuevo = await estadoApp(app);

    // Actualización de versión: cambia CACHE_NAME y el contenido; skipWaiting equivale al botón skipWaiting de DevTools.
    const sw = leer(TRABAJO, 'service-worker.js');
    escribir(TRABAJO, 'service-worker.js', sw.replace("const CACHE_NAME = 'mi-pwa-v1';", "const CACHE_NAME = 'mi-pwa-v2';"));
    cambiarVersion('v1', 'v2');
    await app.evaluar(`navigator.serviceWorker.getRegistration().then((r) => r.update())`);
    a.nuevaVersionEnEspera = await esperar(() => app.evaluar(`navigator.serviceWorker.getRegistration().then((r) => !!r.waiting)`), 10000);
    a.cachesConVersionEnEspera = Object.keys(await estadoCaches(app)).sort();
    await itemLateral(dev, 'Service workers');
    await dormir(1500);
    await capturar(dev, '08_devtools_version_en_espera.png', 'Application > Service workers: la versión nueva instalada y en espera de activarse');
    await app.enviar('ServiceWorker.enable');
    await app.enviar('ServiceWorker.skipWaiting', { scopeURL: `${ORIGEN}/` });
    a.versionNuevaActivada = await esperar(async () => JSON.stringify(Object.keys(await estadoCaches(app))) === '["mi-pwa-v2"]', 10000);
    a.cachesTrasActualizar = await estadoCaches(app);
    await recargar(app, 1800);
    a.versionTrasActualizar = (await estadoApp(app)).version;
    await cerrarPestana(objetivo.id);
    dev.cerrar();
    const { dev: dev2, objetivo: objetivo2 } = await abrirDevtools(appObjetivo.id);
    await abrirCache(dev2, 'mi-pwa-v2');
    await dormir(1800);
    await capturar(dev2, '09_devtools_cache_actualizado.png', 'Cache storage tras subir la versión: solo queda mi-pwa-v2');
    await cerrarPestana(objetivo2.id);
    dev2.cerrar();
    return a;
}

// ------------------------------------------------------------------------------------------ parte B: Cache-First frente a Network-First
async function comparar(app, estrategia, prefijoCaptura) {
    console.log(`Parte B: ${estrategia}`);
    const r = { estrategia, archivoSw: ARCHIVOS_SW[estrategia] };
    await detenerServidor().catch(() => null);
    copiarProyecto(ARCHIVOS_SW[estrategia]);
    await iniciarServidor();
    await limpiarOrigen(app);
    await cargar(app);
    await esperarEstadoSw(app);
    await recargar(app);                                                         // la segunda carga ya está controlada por el Service Worker
    r.inicial = await estadoApp(app);
    r.versionEnCacheInicial = await versionEnCache(app);

    cambiarVersion('v1', 'v2');                                                  // el contenido cambia en el servidor
    r.versionEnServidor = (await (await fetch(`${ORIGEN}/index.html`)).text()).match(/<strong>(v\d+)<\/strong>/)[1];
    await recargar(app);
    r.trasCambio = await estadoApp(app);
    r.versionEnCacheTrasCambio = await versionEnCache(app);
    await capturar(app, `${prefijoCaptura}_con_servidor_actualizado.png`, `${estrategia}: la página tras cambiar el contenido en el servidor a v2`);
    await recargar(app);
    r.segundaRecarga = await estadoApp(app);

    await detenerServidor();                                                     // sin red: el servidor deja de responder
    await recargar(app, 2500);
    r.sinServidor = await estadoApp(app);
    r.sinServidor.cargo = r.sinServidor.titulo === 'Agenda de entregas UMB';
    await capturar(app, `${prefijoCaptura}_sin_servidor.png`, `${estrategia}: la página con el servidor detenido`);
    await iniciarServidor();
    return r;
}

// ------------------------------------------------------------------------------------------ programa principal
async function main() {
    const version = await (await fetch(`http://127.0.0.1:${PUERTO_CDP}/json/version`)).json();
    resultados.entorno = { navegador: version.Browser, userAgent: version['User-Agent'], servidor: `Python http.server en ${ORIGEN} con Cache-Control: no-store`, sistema: process.platform, node: process.version };

    for (const t of await listarObjetivos()) {                                  // pestañas de pruebas anteriores
        if (t.type === 'page' && (t.url.includes(`localhost:${PUERTO_WEB}`) || t.url.includes('/devtools/inspector.html'))) await cerrarPestana(t.id);
    }
    copiarProyecto(ARCHIVOS_SW.cacheFirst);
    await iniciarServidor();
    const appObjetivo = await nuevaPestana('about:blank');
    const app = await conectar(appObjetivo);
    await app.fijarVista(ANCHO_APP, ALTO_APP, FACTOR_PANTALLA);
    await app.enviar('Page.enable');
    try {
        resultados.parteA = await parteA(app, appObjetivo);
        resultados.parteB = {
            cacheFirst: await comparar(app, 'cacheFirst', '10_cache_first'),
            networkFirst: await comparar(app, 'networkFirst', '11_network_first'),
        };
    } finally {
        await detenerServidor().catch(() => null);
        await cerrarPestana(appObjetivo.id).catch(() => null);
        app.cerrar();
    }
    fs.writeFileSync(path.join(EVIDENCIA, 'resultados.json'), JSON.stringify(resultados, null, 1), 'utf8');
    console.log('resultados.json guardado');
}

main().then(() => process.exit(0)).catch((e) => { console.error('ERROR:', e.stack || e.message); servidor?.kill(); process.exit(1); });
