// Agenda de entregas UMB: lista de entregas guardada en localStorage, indicador de conexión y registro del Service Worker.
(function () {
    'use strict';

    var CLAVE = 'entregas-umb';
    var ENTREGAS_INICIALES = [
        { texto: 'Entregar el Lab 5 de Nuevas Tecnologías', hecha: false },
        { texto: 'Revisar la lectura previa de Service Workers', hecha: true }
    ];

    var formulario = document.getElementById('formulario');
    var campo = document.getElementById('entrega');
    var lista = document.getElementById('lista');
    var resumen = document.getElementById('resumen');
    var estadoRed = document.getElementById('estado-red');

    function leerEntregas() {
        try {
            var guardadas = JSON.parse(localStorage.getItem(CLAVE));
            return Array.isArray(guardadas) ? guardadas : ENTREGAS_INICIALES.slice();
        } catch (error) {
            return ENTREGAS_INICIALES.slice();
        }
    }

    function guardarEntregas(entregas) {
        localStorage.setItem(CLAVE, JSON.stringify(entregas));
    }

    function dibujar() {
        var entregas = leerEntregas();
        lista.textContent = '';
        entregas.forEach(function (entrega, indice) {
            var elemento = document.createElement('li');
            if (entrega.hecha) { elemento.className = 'hecha'; }

            var casilla = document.createElement('input');
            casilla.type = 'checkbox';
            casilla.checked = entrega.hecha;
            casilla.setAttribute('aria-label', 'Marcar como hecha: ' + entrega.texto);
            casilla.addEventListener('change', function () {
                var actuales = leerEntregas();
                actuales[indice].hecha = casilla.checked;
                guardarEntregas(actuales);
                dibujar();
            });

            var texto = document.createElement('span');
            texto.textContent = entrega.texto;

            var borrar = document.createElement('button');
            borrar.type = 'button';
            borrar.textContent = 'Quitar';
            borrar.addEventListener('click', function () {
                var actuales = leerEntregas();
                actuales.splice(indice, 1);
                guardarEntregas(actuales);
                dibujar();
            });

            elemento.appendChild(casilla);
            elemento.appendChild(texto);
            elemento.appendChild(borrar);
            lista.appendChild(elemento);
        });
        var pendientes = entregas.filter(function (e) { return !e.hecha; }).length;
        resumen.textContent = pendientes + ' de ' + entregas.length + ' entregas pendientes.';
    }

    formulario.addEventListener('submit', function (evento) {
        evento.preventDefault();
        var texto = campo.value.trim();
        if (!texto) { return; }
        var entregas = leerEntregas();
        entregas.push({ texto: texto, hecha: false });
        guardarEntregas(entregas);
        campo.value = '';
        dibujar();
    });

    function actualizarEstadoRed() {
        if (navigator.onLine) {
            estadoRed.textContent = 'En línea';
            estadoRed.className = 'estado en-linea';
        } else {
            estadoRed.textContent = 'Sin conexión: la app sigue funcionando';
            estadoRed.className = 'estado sin-conexion';
        }
    }

    window.addEventListener('online', actualizarEstadoRed);
    window.addEventListener('offline', actualizarEstadoRed);
    actualizarEstadoRed();
    dibujar();
})();

// Registrar el Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then((registro) => {
                console.log('[App] Service Worker registrado:', registro.scope);
            })
            .catch((error) => {
                console.error('[App] Error al registrar SW:', error);
            });
    });
} else {
    console.log('[App] Service Workers no soportados en este navegador');
}
