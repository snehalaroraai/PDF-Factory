const CACHE_NAME = 'pdf-factory-v1';
const APP_SHELL = [
  './',
  './PDF Factory.html',
  './PDF%20Factory.html',
  './manifest.json',
  './browserconfig.xml',
  './icons/icon-180.svg',
  './icons/icon-192.svg',
  './icons/icon-512.svg',
  './icons/icon-192-maskable.svg',
  './icons/icon-512-maskable.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.map((key) => {
      if (key !== CACHE_NAME) {
        return caches.delete(key);
      }
      return undefined;
    }))).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(request)
      .then((response) => {
        const copy = response.clone();
        if (response.ok) {
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        }
        return response;
      })
      .catch(() => caches.match(request).then((cached) => cached || caches.match('./PDF Factory.html')))
  );
});
