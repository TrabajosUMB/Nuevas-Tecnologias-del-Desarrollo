// Biblioteca mínima del protocolo Chrome DevTools (CDP) para Node 24, sin dependencias: pestañas, evaluación, clics, teclas y capturas.
import fs from 'node:fs';

export const PUERTO_CDP = Number(process.env.CDP_PUERTO || 9336);
export const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
const ESPERA_MAXIMA_MS = 30000;                                          // un comando CDP sin respuesta en 30 s es un error, no una espera infinita
const BASE = () => `http://127.0.0.1:${PUERTO_CDP}`;

export async function listarObjetivos() {
    return (await fetch(`${BASE()}/json/list`)).json();
}

export async function nuevaPestana(url = 'about:blank') {
    const respuesta = await fetch(`${BASE()}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' });
    return respuesta.json();
}

export async function cerrarPestana(id) {
    await fetch(`${BASE()}/json/close/${id}`);
}

const MODS = { alt: 1, ctrl: 2, meta: 4, shift: 8 };
const ESPECIALES = { Enter: 13, Escape: 27, Tab: 9, Backspace: 8, ArrowDown: 40, ArrowUp: 38, F5: 116 };

/** Abre una sesión CDP con un objetivo (pestaña, worker...). Devuelve un objeto con helpers de alto nivel. */
export async function conectar(objetivo) {
    const ws = new WebSocket(objetivo.webSocketDebuggerUrl);
    await new Promise((ok, mal) => { ws.onopen = ok; ws.onerror = () => mal(new Error(`no se pudo conectar con ${objetivo.url}`)); });
    let id = 0;
    const pendientes = new Map();
    const oyentes = [];
    ws.onmessage = (m) => {
        const msg = JSON.parse(m.data);
        if (msg.id && pendientes.has(msg.id)) {
            pendientes.get(msg.id)(msg);
            pendientes.delete(msg.id);
        } else if (msg.method) {
            oyentes.forEach((o) => o(msg));
        }
    };
    const enviar = (method, params = {}) => new Promise((ok, mal) => {
        const n = ++id;
        const reloj = setTimeout(() => {
            pendientes.delete(n);
            mal(new Error(`${method}: sin respuesta en ${ESPERA_MAXIMA_MS / 1000} s`));
        }, ESPERA_MAXIMA_MS);
        pendientes.set(n, (msg) => {
            clearTimeout(reloj);
            if (msg.error) mal(new Error(`${method}: ${msg.error.message}`));
            else ok(msg.result);
        });
        ws.send(JSON.stringify({ id: n, method, params }));
    });
    const evaluar = async (expresion) => {
        const r = await enviar('Runtime.evaluate', { expression: expresion, awaitPromise: true, returnByValue: true });
        if (r.exceptionDetails) throw new Error(`evaluar: ${r.exceptionDetails.exception?.description || r.exceptionDetails.text}`);
        return r.result.value;
    };
    const clic = async (x, y) => {
        await enviar('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
        await enviar('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
        await enviar('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
    };
    const tecla = async (combo) => {
        const partes = combo.split('+');
        const nombre = partes.pop();
        const modificadores = partes.reduce((acc, p) => acc | (MODS[p.toLowerCase()] || 0), 0);
        const vk = ESPECIALES[nombre] || (nombre.length === 1 ? nombre.toUpperCase().charCodeAt(0) : 0);
        const base = { key: nombre, code: /^[a-zA-Z]$/.test(nombre) ? `Key${nombre.toUpperCase()}` : nombre, windowsVirtualKeyCode: vk, nativeVirtualKeyCode: vk, modifiers: modificadores };
        await enviar('Input.dispatchKeyEvent', { type: 'rawKeyDown', ...base });
        await enviar('Input.dispatchKeyEvent', { type: 'keyUp', ...base });
    };
    const foto = async (archivo, clip) => {
        const params = { format: 'png' };
        if (clip) params.clip = { ...clip, scale: 1 };
        const { data } = await enviar('Page.captureScreenshot', params);
        fs.writeFileSync(archivo, Buffer.from(data, 'base64'));
        return archivo;
    };
    const fijarVista = async (ancho, alto, factor = 1) => enviar('Emulation.setDeviceMetricsOverride', { width: ancho, height: alto, deviceScaleFactor: factor, mobile: false });
    const escuchar = (fn) => oyentes.push(fn);
    return { enviar, evaluar, clic, tecla, foto, fijarVista, escuchar, cerrar: () => ws.close(), objetivo };
}

/** Código JS (para evaluar en la pestaña) que recorre el DOM incluyendo shadow roots y devuelve el rectángulo del primer elemento que cumple. */
export const BUSCAR_PROFUNDO = `(function () {
    function* recorrer(raiz) {
        for (const e of raiz.querySelectorAll('*')) {
            yield e;
            if (e.shadowRoot) yield* recorrer(e.shadowRoot);
        }
    }
    window.__buscar = function (predicado) {
        for (const e of recorrer(document)) {
            if (predicado(e)) {
                const r = e.getBoundingClientRect();
                if (r.width > 0 && r.height > 0) return { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height, texto: (e.innerText || e.getAttribute('aria-label') || '').slice(0, 60) };
            }
        }
        return null;
    };
    window.__marcada = function (texto) {
        for (const e of recorrer(document)) {
            if (e.tagName === 'LABEL' && (e.innerText || '').trim() === texto) {
                const campo = e.control || e.querySelector('input[type=checkbox]');   // en DevTools la etiqueta apunta al campo con «for»
                if (campo) return campo.checked;
            }
        }
        return null;
    };
    window.__todos = function (predicado, max) {
        const salida = [];
        for (const e of recorrer(document)) {
            if (predicado(e)) {
                const r = e.getBoundingClientRect();
                if (r.width > 0 && r.height > 0) salida.push({ etiqueta: e.tagName.toLowerCase(), texto: (e.innerText || e.getAttribute('aria-label') || '').slice(0, 60).replace(/\\n/g, ' '), x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) });
                if (salida.length >= (max || 60)) break;
            }
        }
        return salida;
    };
    return true;
})()`;
