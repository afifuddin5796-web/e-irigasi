# Membuat aplikasi lewat PWABuilder

Prasyarat: situs sudah aktif di `https://afifuddin5796-web.github.io/e-irigasi/` (HTTPS dari GitHub Pages), dan berkas `manifest.webmanifest`, `sw.js`, serta folder `icons/` sudah ikut terunggah.

## Langkah

1. Buka pwabuilder.com, tempel alamat situs di atas, lalu tekan **Start**.
2. Tunggu laporan. Bagian **Manifest** dan **Service Worker** seharusnya terbaca. Kalau ada yang belum terbaca, muat ulang halaman situs sekali (agar service worker terpasang), lalu ulangi.
3. Tekan **Package for stores** dan pilih platform:
   - **Android**: pilih **Other Android** untuk berkas `.apk` yang bisa langsung dipasang di HP para juru (tanpa Play Store), atau **Google Play** untuk berkas `.aab`.
   - Windows juga tersedia bila diperlukan.
4. Isi pilihan Android:
   - **Package ID**: contoh `io.github.afifuddin5796web.eirigasi` (huruf kecil dan titik saja, tanpa tanda hubung).
   - **App name**: e-Irigasi. **Launcher name**: e-Irigasi.
   - **Signing key**: pilih buat kunci baru, lalu **simpan berkas kunci dan kata sandinya di tempat aman**. Tanpa kunci yang sama, pembaruan aplikasi tidak bisa dipasang menimpa versi lama.
5. Unduh paketnya. Untuk `.apk`, kirim berkasnya ke para juru dan izinkan pemasangan dari sumber luar saat diminta.

## Hal yang perlu diketahui

- Aplikasi Android dari PWABuilder membuka situs Anda, jadi **data selalu mengikuti isi repositori**. Memperbarui `data.json` di GitHub otomatis memperbarui aplikasi, tanpa membuat paket baru.
- Bilah alamat peramban baru bisa disembunyikan sepenuhnya bila berkas `/.well-known/assetlinks.json` tersedia di akar domain. Untuk situs proyek seperti ini (`.../e-irigasi/`), berkas itu harus berada di repositori khusus bernama `afifuddin5796-web.github.io`. Tanpa itu aplikasi tetap berjalan, hanya menampilkan bilah alamat kecil di atas.
- Pendaftaran Google Play memerlukan akun pengembang berbayar (biaya sekali bayar). Untuk dipakai sendiri oleh para juru, `.apk` sudah cukup.
- Layar tangkapan (screenshots) di manifest bersifat opsional. Tambahkan nanti bila ingin tampil lebih rapi di toko aplikasi.
