/*
 * SERVICE WORKER — VERSIÓN 2: NETWORK-FIRST («primero la red»)
 * ---------------------------------------------------------------------------
 * Estrategia: ante cada petición, el Service Worker intenta primero la red.
 * Si la red responde, entrega esa respuesta (la más reciente) y además guarda
 * una copia en el caché. Si la red falla (sin conexión o servidor caído), usa
 * la última copia guardada en el caché.
 *
 * Ventajas:  el contenido siempre está al día cuando hay conexión, y el caché
 *            se renueva solo con cada visita.
 * Desventaja: depende de la red para responder (si la red está lenta, la
 *             página también) y no mejora el tiempo de carga.
 *
 * Esta versión solo cambia el evento FETCH respecto de service-worker.js
 * (Cache-First). INSTALL y ACTIVATE son iguales. Para probarla, su contenido se
 * copia sobre service-worker.js, porque app.js registra ese nombre y el
 * navegador solo admite un Service Worker por alcance.
 */

// Nombre del cache — cambia la version cuando actualices la app
const CACHE_NAME = 'mi-pwa-v1';

// Archivos que se guardan en cache al instalar
const ARCHIVOS_CACHE = [
  '/',
  '/index.html',
  '/styles.css',
  '/app.js',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

// EVENTO INSTALL: igual que en Cache-First, guarda los archivos al instalar
// para que exista una copia a la cual recurrir cuando falle la red.
self.addEventListener('install', (event) => {
  console.log('[SW] Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Guardando archivos en cache');
      return cache.addAll(ARCHIVOS_CACHE);
    })
  );
});

// EVENTO ACTIVATE: igual que en Cache-First, limpia caches viejos.
self.addEventListener('activate', (event) => {
  console.log('[SW] Activando...');
  event.waitUntil(
    caches.keys().then((nombres) => {
      return Promise.all(
        nombres.filter(n => n !== CACHE_NAME).map(n => caches.delete(n))
      );
    })
  );
});

// EVENTO FETCH: Network-First (primero la red, si falla usa el cache).
self.addEventListener('fetch', (event) => {
  // Solo se gestionan las peticiones GET: el caché no puede guardar POST, etc.
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((respuestaRed) => {
        // La red respondió: se guarda una copia fresca en el caché.
        // Una respuesta solo se puede leer una vez, por eso se usa clone():
        // una copia va al caché y la original va a la página.
        if (respuestaRed && respuestaRed.status === 200) {
          const copia = respuestaRed.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copia));
        }
        return respuestaRed; // responde con lo más reciente
      })
      .catch(() => {
        // La red falló: se usa la última copia guardada (si existe).
        return caches.match(event.request);
      })
  );
});

/*
 * COMPARACIÓN CON CACHE-FIRST (service-worker.js)
 * ---------------------------------------------------------------------------
 *                        Cache-First                  Network-First (este archivo)
 * Primer intento         caché                        red
 * Si el primero falla    red                          caché
 * Contenido              puede estar desactualizado   siempre el más reciente
 * Velocidad              inmediata                    depende de la red
 * Sin conexión           funciona                     funciona con lo ya guardado
 * Actualiza el caché     solo al instalar             en cada respuesta de la red
 * Conviene para          recursos que casi no cambian contenido que cambia a menudo
 */
