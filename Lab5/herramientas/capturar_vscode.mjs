// Abre los archivos del laboratorio en VS Code y guarda capturas reales del editor (código con el resaltado de sintaxis de VS Code).
// Requiere VS Code abierto con lanzar_vscode.ps1 (puerto 9340). Uso: CDP_PUERTO=9340 node capturar_vscode.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { conectar, dormir, listarObjetivos } from './cdp_lib.mjs';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const SALIDA = path.join(AQUI, '..', 'evidencia', 'vscode');
const ANCHO_VISTA = 1500;
const ALTO_VISTA_CODIGO = 2300;             // alto suficiente para que VS Code dibuje todas las líneas (se virtualizan fuera de la ventana)
const ALTO_VISTA_ESTRUCTURA = 760;
const ANCHO_ESTRUCTURA = 1000;            // solo el explorador y el comienzo del editor: así la letra se lee en el informe
const ANCHO_RECORTE = 700;                  // píxeles CSS que se recortan a partir del borde izquierdo del editor
const ESCALA = 1.5;

// «desde»: texto con el que empieza la primera línea que se recorta (sin él se captura el archivo completo).
const ARCHIVOS = [
    { id: 'service_worker_cache_first', archivo: 'service-worker.js' },
    { id: 'service_worker_network_first', archivo: 'service-worker-network-first.js' },
    { id: 'registro_en_app', archivo: 'app.js', desde: '// Registrar el Service Worker' },
];

async function main() {
    fs.mkdirSync(SALIDA, { recursive: true });
    const pagina = (await listarObjetivos()).find((t) => t.type === 'page' && t.url.includes('workbench'));
    if (!pagina) throw new Error('No hay una ventana de VS Code con el puerto de depuración');
    const c = await conectar(pagina);
    const foto = async (nombre, x, y, ancho, alto) => {
        const { data } = await c.enviar('Page.captureScreenshot', { format: 'png', clip: { x, y, width: ancho, height: alto, scale: ESCALA } });
        fs.writeFileSync(path.join(SALIDA, nombre), Buffer.from(data, 'base64'));
    };
    const abrir = async (archivo) => {
        await c.tecla('Escape');
        await dormir(300);
        await c.tecla('Escape');
        await dormir(300);
        await c.tecla('ctrl+p');
        await dormir(700);
        await c.enviar('Input.insertText', { text: archivo });
        await dormir(900);
        await c.tecla('Enter');
        await dormir(2500);
    };

    // 1) ventana completa con el explorador: estructura del proyecto
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: ANCHO_VISTA, height: ALTO_VISTA_ESTRUCTURA, deviceScaleFactor: 0, mobile: false });
    await dormir(1200);
    await c.tecla('ctrl+shift+e');
    await dormir(800);
    await c.tecla('ctrl+k');                    // Ctrl+K W: cierra todos los editores abiertos de ejecuciones anteriores
    await dormir(300);
    await c.tecla('w');
    await dormir(800);
    await abrir('service-worker.js');
    await foto('estructura_proyecto.png', 0, 0, ANCHO_ESTRUCTURA, ALTO_VISTA_ESTRUCTURA);

    // 2) código de cada archivo
    await c.enviar('Emulation.setDeviceMetricsOverride', { width: ANCHO_VISTA, height: ALTO_VISTA_CODIGO, deviceScaleFactor: 0, mobile: false });
    await dormir(1500);
    for (const p of ARCHIVOS) {
        await abrir(p.archivo);
        const medida = JSON.parse(await c.evaluar(`JSON.stringify((() => {
            const rect = (el) => { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; };
            const grupo = rect(document.querySelector('.editor-group-container'));
            const lineas = [...document.querySelectorAll('.editor-instance .view-lines .view-line')].map((l) => ({ ...rect(l), texto: l.innerText }));
            lineas.sort((a, b) => a.y - b.y);
            return { grupo, lineas };
        })())`));
        const { grupo, lineas } = medida;
        const primera = p.desde ? lineas.find((l) => l.texto.replace(/ /g, ' ').trim().startsWith(p.desde)) : lineas[0];
        if (!primera) throw new Error(`${p.archivo}: no se encontró la línea «${p.desde}»`);
        const ultimaY = lineas.reduce((m, l) => Math.max(m, l.y + l.h), 0);
        const inicioY = p.desde ? primera.y - 6 : grupo.y;
        await foto(`${p.id}.png`, grupo.x, inicioY, ANCHO_RECORTE, ultimaY - inicioY + 8);
        const enRecorte = lineas.filter((l) => l.y >= inicioY - 1);
        fs.writeFileSync(path.join(SALIDA, `${p.id}_meta.json`), JSON.stringify({
            archivo: p.archivo, desde: p.desde || null, anchoRecorte: ANCHO_RECORTE, escala: ESCALA,
            lineas: enRecorte.map((l) => ({ top: l.y - inicioY, alto: l.h, texto: l.texto.replace(/ /g, ' ') })),
        }, null, 1));
        console.log(`${p.id}: ${lineas.length} líneas renderizadas`);
        await c.tecla('ctrl+w');                // cierra la pestaña para que no se acumulen en las capturas siguientes
        await dormir(700);
    }
    c.cerrar();
}

main().then(() => process.exit(0)).catch((e) => { console.error('ERROR:', e.message); process.exit(1); });
