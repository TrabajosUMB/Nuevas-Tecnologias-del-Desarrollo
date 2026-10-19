/*
 * SERVICE WORKER — VERSIÓN 1: CACHE-FIRST («primero el caché»)
 * ---------------------------------------------------------------------------
 * Estrategia: ante cada petición, el Service Worker busca primero en el caché.
 * Si encuentra una copia, responde con ella y no toca la red; solo si no la
 * hay, va a la red.
 *
 * Ventajas:  responde de inmediato (no espera a la red) y funciona sin conexión.
 * Desventaja: puede mostrar contenido desactualizado, porque nunca revisa si el
 *             servidor tiene una versión más nueva mientras el caché no cambie
 *             de nombre (CACHE_NAME).
 *
 * La otra versión, con estrategia Network-First, está en
 * service-worker-network-first.js. Las dos son idénticas salvo por el evento
 * FETCH (ver la comparación al final de este archivo).
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

// EVENTO INSTALL: guarda archivos en cache (pre-caching).
// waitUntil() obliga al navegador a esperar a que termine la promesa antes de
// dar la instalación por terminada. addAll() es atómico: si un solo archivo
// falla (por ejemplo, un 404), no se guarda ninguno y la instalación falla.
self.addEventListener('install', (event) => {
  console.log('[SW] Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Guardando archivos en cache');
      return cache.addAll(ARCHIVOS_CACHE);
    })
  );
});

// EVENTO ACTIVATE: limpia caches viejos.
// Borra todos los cachés cuyo nombre no sea el actual; así, al subir de
// 'mi-pwa-v1' a 'mi-pwa-v2', el caché anterior no queda ocupando espacio.
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

// EVENTO FETCH: Cache-First (primero cache, si no hay, va a la red).
// respondWith() decide qué respuesta recibe la página. caches.match() busca la
// petición en todos los cachés; devuelve undefined si no hay copia.
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((respuestaCache) => {
      if (respuestaCache) {
        return respuestaCache; // responde desde cache
      }
      return fetch(event.request); // va a la red
    })
  );
});

/*
 * COMPARACIÓN CON NETWORK-FIRST (service-worker-network-first.js)
 * ---------------------------------------------------------------------------
 *                        Cache-First (este archivo)   Network-First
 * Primer intento         caché                        red
 * Si el primero falla    red                          caché
 * Contenido              puede estar desactualizado   siempre el más reciente
 * Velocidad              inmediata                    depende de la red
 * Sin conexión           funciona                     funciona con lo ya guardado
 * Actualiza el caché     solo al instalar             en cada respuesta de la red
 * Conviene para          recursos que casi no cambian contenido que cambia a menudo
 */
