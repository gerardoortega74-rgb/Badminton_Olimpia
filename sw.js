// Caché de la web y de la app del club: abre aunque la cobertura sea mala.
// Las páginas se piden siempre a la red primero (así nunca se queda una versión vieja); si la red tarda o no hay, se usa la copia guardada.
const CACHE = 'olimpia-v1';
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))).then(() => self.clients.claim())));
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const u = new URL(r.url);
  if (u.origin !== self.location.origin) return;                 // Firebase, Meta, fuentes…: sin tocar
  if (r.headers.has('range') || /\.(mp4|webm)$/i.test(u.pathname)) return; // vídeos: sin tocar
  const esPagina = r.mode === 'navigate' || /\.html$/i.test(u.pathname) || u.pathname.endsWith('/');
  if (esPagina) {
    const clave = u.pathname;
    const red = fetch(r).then(res => { if (res.ok) { const c = res.clone(); caches.open(CACHE).then(x => x.put(clave, c)); } return res; });
    const espera = new Promise(ok => setTimeout(ok, 4000)).then(() => caches.match(clave)).then(m => m || red);
    e.respondWith(Promise.race([red.catch(() => caches.match(clave).then(m => m || Response.error())), espera]));
    return;
  }
  e.respondWith(caches.match(r).then(m => {
    const red = fetch(r).then(res => { if (res.ok) { const c = res.clone(); caches.open(CACHE).then(x => x.put(r, c)); } return res; }).catch(() => m || Response.error());
    return m || red;
  }));
});
