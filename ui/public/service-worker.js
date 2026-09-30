// Bugify service worker stub — prevents 404 errors
// No caching strategy implemented; app works fully online
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', () => self.clients.claim());
