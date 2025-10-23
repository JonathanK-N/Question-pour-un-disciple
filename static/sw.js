const CACHE_NAME = 'disciple-quiz-cache-v1';
const APP_SHELL = [
  '/',
  '/static/manifest.json',
  '/static/pwa.js',
  '/static/style.css',
  '/static/script.js',
  '/static/icons/app-icon.png',
  '/static/assets/social-card.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const { request } = event;

  if (request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(request)
        .then(response => {
          const shouldCache =
            response &&
            response.status === 200 &&
            response.type === 'basic' &&
            !request.url.includes('/socket.io');
          if (shouldCache) {
            const cloned = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, cloned));
          }
          return response;
        })
        .catch(() => caches.match('/'));
    })
  );
});
