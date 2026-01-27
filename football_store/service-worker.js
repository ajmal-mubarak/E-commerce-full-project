const CACHE_NAME = 'ecommerce-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/images'
  // add more static files, images, fonts if needed
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(resp => resp || fetch(event.request))
  );
});
