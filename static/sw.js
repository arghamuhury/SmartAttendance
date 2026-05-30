const CACHE_NAME = 'smart-attendance-v1';
const urlsToCache = [
  '/',
  '/static/css/index.css'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cache hit or network request
        return response || fetch(event.request);
      })
  );
});
