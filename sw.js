// Service worker e-Irigasi: cangkang aplikasi tersimpan untuk dipakai tanpa sinyal.
// Naikkan angka VERSI setiap kali index.html diganti, supaya perangkat mengambil yang baru.
const VERSI='e-irigasi-v5',CANGKANG=['./','index.html','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(VERSI).then(c=>c.addAll(CANGKANG)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==VERSI).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
const jaringanDulu=async r=>{const c=await caches.open(VERSI);try{const x=await fetch(r);if(x.ok)c.put(r,x.clone());return x}catch(e){return(await c.match(r))||Response.error()}};
const simpanLaluSegarkan=async r=>{const c=await caches.open(VERSI),ada=await c.match(r),net=fetch(r).then(x=>{if(x&&(x.ok||x.type==='opaque'))c.put(r,x.clone());return x}).catch(()=>ada);return ada||net};
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);
  if(/arcgisonline|cartocdn|openstreetmap|supabase/.test(u.hostname))return;              // ubin peta: selalu dari jaringan
  if(u.origin===location.origin&&/\/foto\/.*\.jpg$/.test(u.pathname))return;                                   // gambar foto: biar peramban yang mengelola
  if(u.origin===location.origin&&u.pathname.endsWith('/data.json')){e.respondWith(jaringanDulu(r));return}   // data terbaru lebih dulu
  e.respondWith(simpanLaluSegarkan(r));
});
