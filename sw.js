// 三國演義 読み物版 ─ オフライン読書用サービスワーカー
// HTML/JSON はnetwork-first（再デプロイを即反映）、不変アセット(画像/版数付きscenes)はcache-first（高速・オフライン）。
const V = 'sangokushi-engi-v20260622';
const CORE = [
  './', './index.html', './manifest.webmanifest',
  './scenes/manifest.json', './scenes/roster.json', './scenes/faction.json',
  './assets/title_kv.jpg', './assets/ogp.jpg',
  './assets/icon-180.png', './assets/icon-192.png', './assets/icon-512.png',
];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(V).then(c => c.addAll(CORE).catch(()=>{})).then(()=>self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k))))
    .then(()=>self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url; try { url = new URL(req.url); } catch (_) { return; }
  if (url.origin !== location.origin) return;
  const isDoc = req.mode === 'navigate' || req.destination === 'document';
  const isData = /\.(json|webmanifest)$/.test(url.pathname);
  if (isDoc || isData) {
    // network-first: 最新を取りに行き、取れた版だけキャッシュ更新。オフライン時はキャッシュにフォールバック
    e.respondWith(
      fetch(req).then(res => {
        if (res && res.status === 200) { const cp = res.clone(); caches.open(V).then(c => c.put(req, cp)); }
        return res;
      }).catch(() => caches.match(req).then(h => h || (isDoc ? caches.match('./index.html') : undefined)))
    );
    return;
  }
  // cache-first: 画像・版数付きsceneJS等の不変アセット
  e.respondWith(
    caches.match(req).then(hit =>
      hit || fetch(req).then(res => {
        if (res && res.status === 200 && res.type === 'basic') { const cp = res.clone(); caches.open(V).then(c => c.put(req, cp)); }
        return res;
      }).catch(() => hit)
    )
  );
});
