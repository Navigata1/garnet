const CACHE_NAME = "garnet-web-v4";
const OFFLINE_ASSETS = [
  "./",
  "getting-started.html",
  "index.html",
  "install.sh",
  "ladder.html",
  "manifest.webmanifest",
  "minispec.html",
  "novel.html",
  "playground.html",
  "status.html",
  "stdlib.html",
  "synthesis.html",
  "blog/index.html",
  "blog/feed.xml",
  "releases.xml",
  "assets/garnet-hero.webp",
  "assets/garnet-demonstration-poster.jpg",
  "icons/garnet-192.png",
  "icons/garnet-512.png"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(OFFLINE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(
        names
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const request = event.request;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
          return response;
        })
        .catch(() => caches.match(request).then((hit) => hit || caches.match("index.html")))
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((hit) => {
      if (hit) {
        return hit;
      }
      return fetch(request).then((response) => {
        if (request.method === "GET" && response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
        }
        return response;
      });
    })
  );
});
