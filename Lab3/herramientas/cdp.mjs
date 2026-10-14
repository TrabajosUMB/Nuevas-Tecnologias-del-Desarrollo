// Cliente mínimo del protocolo Chrome DevTools (CDP) para manejar un Edge headless ya abierto (Node 24, sin dependencias).
// Uso: node cdp.mjs <comando> [args]
//   nav <url>            navega y espera a que cargue
//   evalf <archivo.js>   evalúa el archivo en la página y muestra el resultado (JSON)
//   shot <archivo.png>   captura la ventana completa (opcional: x y ancho alto para recortar)
//   click <x> <y>        clic izquierdo en coordenadas de la ventana
//   type <texto>         inserta texto en el elemento enfocado
//   key <tecla>          pulsa una tecla (Enter, Escape, Tab, ArrowDown...)
//   wait <ms>            espera
import fs from 'node:fs';

const PUERTO = process.env.CDP_PUERTO || '9335';
const [, , comando, ...args] = process.argv;

async function conectar() {
    const lista = await (await fetch(`http://127.0.0.1:${PUERTO}/json/list`)).json();
    const pagina = lista.find((t) => t.type === 'page');
    if (!pagina) throw new Error('No hay una página abierta en el Edge de CDP');
    const ws = new WebSocket(pagina.webSocketDebuggerUrl);
    await new Promise((ok, mal) => { ws.onopen = ok; ws.onerror = mal; });
    let id = 0;
    const pendientes = new Map();
    const eventos = [];
    ws.onmessage = (m) => {
        const msg = JSON.parse(m.data);
        if (msg.id && pendientes.has(msg.id)) { pendientes.get(msg.id)(msg); pendientes.delete(msg.id); } else eventos.push(msg);
    };
    const enviar = (method, params = {}) => new Promise((ok, mal) => {
        const n = ++id;
        pendientes.set(n, (msg) => (msg.error ? mal(new Error(`${method}: ${msg.error.message}`)) : ok(msg.result)));
        ws.send(JSON.stringify({ id: n, method, params }));
    });
    return { enviar, eventos, cerrar: () => ws.close() };
}

const dormir = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
    const c = await conectar();
    try {
        if (comando === 'nav') {
            await c.enviar('Page.enable');
            await c.enviar('Page.navigate', { url: args[0] });
            await dormir(Number(args[1] || 4000));
            console.log('navegado a', args[0]);
        } else if (comando === 'evalf') {
            const codigo = fs.readFileSync(args[0], 'utf8');
            const r = await c.enviar('Runtime.evaluate', { expression: codigo, awaitPromise: true, returnByValue: true });
            if (r.exceptionDetails) console.log('EXCEPCIÓN:', r.exceptionDetails.exception?.description || JSON.stringify(r.exceptionDetails));
            else console.log(typeof r.result.value === 'string' ? r.result.value : JSON.stringify(r.result.value, null, 1));
        } else if (comando === 'shot') {
            const params = { format: 'png' };
            if (args.length >= 5) params.clip = { x: +args[1], y: +args[2], width: +args[3], height: +args[4], scale: 1 };
            const { data } = await c.enviar('Page.captureScreenshot', params);
            fs.writeFileSync(args[0], Buffer.from(data, 'base64'));
            console.log('captura guardada en', args[0]);
        } else if (comando === 'click') {
            const [x, y] = [+args[0], +args[1]];
            await c.enviar('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
            await c.enviar('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
            await c.enviar('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
            console.log('clic en', x, y);
        } else if (comando === 'type') {
            await c.enviar('Input.insertText', { text: args.join(' ') });
            console.log('texto insertado');
        } else if (comando === 'key') {
            const tecla = args[0];
            const codigos = { Enter: 13, Escape: 27, Tab: 9, ArrowDown: 40, ArrowUp: 38, Backspace: 8 };
            const base = { key: tecla, code: tecla, windowsVirtualKeyCode: codigos[tecla] || 0 };
            await c.enviar('Input.dispatchKeyEvent', { type: 'keyDown', ...base, text: tecla === 'Enter' ? '\r' : undefined });
            await c.enviar('Input.dispatchKeyEvent', { type: 'keyUp', ...base });
            console.log('tecla', tecla);
        } else if (comando === 'scroll') {
            const [x, y, dy] = args.map(Number);
            await c.enviar('Input.dispatchMouseEvent', { type: 'mouseWheel', x, y, deltaX: 0, deltaY: dy });
            console.log('desplazamiento', dy, 'en', x, y);
        } else if (comando === 'selectall') {
            // Ctrl+A en el elemento enfocado (el comando de edición lo resuelve el propio navegador).
            const base = { key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65, modifiers: 2 };
            await c.enviar('Input.dispatchKeyEvent', { type: 'keyDown', ...base, commands: ['selectAll'] });
            await c.enviar('Input.dispatchKeyEvent', { type: 'keyUp', ...base });
            console.log('seleccionar todo');
        } else if (comando === 'pegar') {
            // Pega el contenido de un archivo en el editor Monaco enfocado (equivale a Ctrl+V; evita la sangría y los cierres automáticos).
            const texto = fs.readFileSync(args[0], 'utf8');
            const expr = `(() => {
                const ta = document.querySelector('.monaco-editor textarea.inputarea');
                if (!ta) return 'no hay editor';
                ta.focus();
                const dt = new DataTransfer();
                dt.setData('text/plain', ${JSON.stringify(texto)});
                ta.dispatchEvent(new ClipboardEvent('paste', { clipboardData: dt, bubbles: true, cancelable: true }));
                return 'pegado';
            })()`;
            const r = await c.enviar('Runtime.evaluate', { expression: expr, returnByValue: true });
            console.log(r.result.value);
        } else if (comando === 'fijar') {
            // Mantiene abierta una sesión que fija el tamaño de la vista; el tamaño dura mientras este proceso siga vivo.
            await c.enviar('Emulation.setDeviceMetricsOverride', { width: +args[0], height: +args[1], deviceScaleFactor: 1, mobile: false });
            console.log('vista fijada en', args[0], 'x', args[1], '(proceso en espera)');
            await new Promise(() => {});
        } else if (comando === 'size') {
            // Cambia el tamaño real de la ventana (nivel navegador) para que persista entre comandos.
            const version = await (await fetch(`http://127.0.0.1:${PUERTO}/json/version`)).json();
            const nav = new WebSocket(version.webSocketDebuggerUrl);
            await new Promise((ok, mal) => { nav.onopen = ok; nav.onerror = mal; });
            const llamar = (id, method, params) => new Promise((ok) => {
                const h = (m) => { const msg = JSON.parse(m.data); if (msg.id === id) { nav.removeEventListener('message', h); ok(msg); } };
                nav.addEventListener('message', h);
                nav.send(JSON.stringify({ id, method, params }));
            });
            const lista = await (await fetch(`http://127.0.0.1:${PUERTO}/json/list`)).json();
            const objetivo = lista.find((t) => t.type === 'page');
            const ventana = await llamar(1, 'Browser.getWindowForTarget', { targetId: objetivo.id });
            const r = await llamar(2, 'Browser.setWindowBounds', { windowId: ventana.result.windowId, bounds: { width: +args[0], height: +args[1], windowState: 'normal' } });
            console.log('ventana', args[0], 'x', args[1], r.error ? r.error.message : 'ok');
            nav.close();
            await dormir(1500);
        } else if (comando === 'wait') {
            await dormir(Number(args[0]));
        } else {
            console.log('Comando desconocido:', comando);
        }
    } finally {
        c.cerrar();
    }
}

main().catch((e) => { console.error('ERROR:', e.message); process.exit(1); });
