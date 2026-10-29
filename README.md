# e-Irigasi

e-Irigasi adalah aplikasi web peta dan skema jaringan irigasi untuk para juru pengairan UPTD Purwosari, Kabupaten Pasuruan.
Menampilkan baku sawah, panjang saluran, bangunan, debit, dan realisasi tanam (padi, tebu, palawija, bero, habis panen) per daerah irigasi. Tema gelap, ringan, dan nyaman dibuka di HP.

## Fitur

- Setelah memilih juru, aset irigasi di wilayahnya dikelompokkan otomatis dari nama bangunan di peta (sumber air, bendung, bangunan bagi dan sadap, pelimpah, gorong-gorong, boks tersier, ujung saluran, dan lainnya), dan setiap aset bisa dibuka langsung di peta. Tab **Daerah irigasi** menampilkan daftar DI.
- Pilih juru pengairan (Krangkong, Sadan, Sengon, Purwodadi, Rejoso, Sukorejo, Sukun), lalu daerah irigasi di bawahnya.
- Peta satelit atau peta gelap dengan koordinat, saluran, petak baku, dan bangunan (dari berkas KMZ).
- Tab **Skema**: gambar skema jaringan dari berkas DXF, bisa digeser dan diperbesar. Ketuk petak atau bangunan bagi untuk melihat data Excel, debit terukur, dan tombol "Lihat di peta".
- Tab **Ringkasan**: baku, panjang saluran, tanaman per DI, serta menu mengubah luas baku.
- Tab **Debit** dan **Bangunan**.
- Tab **Foto**: galeri foto bangunan. Foto lama bisa disimpan di repositori (folder `foto/`), foto baru diunggah dari HP lewat Supabase dengan antrean tanpa sinyal dan menu **Sinkron** (lihat [docs/FOTO.md](docs/FOTO.md)).
- Laporan kondisi bangunan dari lokasi (kondisi, catatan, foto, lokasi HP); titik di peta berubah warna sesuai kondisi terakhir.
- Pembaruan sederhana dari aplikasi: ubah luas baku, ganti peta DI dari berkas KMZ, unggah Excel tanaman, lalu unduh `data.json` dan unggah ke GitHub (lihat [docs/PEMBARUAN.md](docs/PEMBARUAN.md)). Menu ini hanya tampil di mode pengelola (ketuk judul aplikasi 5 kali). Juru hanya melihat peta, skema, debit, dan menambah foto ([docs/PANDUAN_JURU.md](docs/PANDUAN_JURU.md)).
- Koordinat bisa disalin dan dibuka di Google Maps dari kotak koordinat peta maupun dari tiap bangunan.
- Menu **Perbarui data tanaman**: unggah Excel laporan dengan format yang sama, hasilnya langsung tampil.

## Isi repositori

| Berkas | Fungsi |
|---|---|
| `index.html` | Seluruh aplikasi (satu berkas) |
| `data.json` | Data DI: peta, tanaman, debit, per petak |
| `manifest.webmanifest`, `sw.js`, `icons/` | Berkas PWA (bisa dipasang seperti aplikasi dan dibuka tanpa sinyal) |
| `config.js` | Alamat dan kunci Supabase untuk foto (isi sesuai docs/FOTO.md) |
| `skema/*.json` | Skema jaringan per DI (nama berkas = nomor DI di `data.json`) |
| `tools/` | Skrip Python: membangun ulang `data.json` dan `skema/`, dan `siapkan_foto_repo.py` (foto ke folder `foto/`) dan `unggah_foto.py` (foto massal ke Supabase) |
| `docs/` | Panduan pengaturan GitHub |

## Dijadikan aplikasi (PWA)

Setelah situs aktif di GitHub Pages, aplikasi bisa dipasang dari Chrome lewat **Tambahkan ke layar utama**, atau dibungkus menjadi aplikasi Android lewat pwabuilder.com. Langkahnya ada di [docs/PWABUILDER.md](docs/PWABUILDER.md). Setiap kali `index.html` diganti, naikkan angka `VERSI` di `sw.js` supaya perangkat mengambil versi terbaru.

## Memasang (GitHub Pages)

Lihat langkah lengkap di [docs/PENGATURAN_GITHUB.md](docs/PENGATURAN_GITHUB.md).
Singkatnya: unggah semua isi repositori, lalu **Settings > Pages > Deploy from a branch > main / (root)**.

## Memperbarui data

**Cara cepat (tanpa komputer khusus):**
1. Buka aplikasi, pada layar pilih juru, bagian **Perbarui data tanaman**, pilih file Excel terbaru.
2. Tekan **Unduh data.json untuk dibagikan**.
3. Di GitHub, unggah `data.json` itu ke repositori, menggantikan yang lama. Setelah beberapa menit semua juru melihat data yang sama.

Perubahan luas baku dan hasil unggah Excel hanya tersimpan di perangkat yang melakukannya sampai `data.json` diganti.

**Membangun ulang dari berkas sumber** (bila peta KMZ atau skema DXF berubah):

```bash
pip install -r tools/requirements.txt
# taruh .kmz, .dxf, dan satu .xlsx di folder data_sumber/
python tools/bangun_data.py data_sumber .
python tools/bangun_skema.py data_sumber .
```

Skrip membaca Excel terbaru di folder sumber. Nama berkas KMZ dan DXF dipasangkan ke DI lewat nama (misalnya `1 Tlogo 2022 ok.kmz`). Bila ada DI baru atau nama yang tidak cocok, skrip menampilkan daftarnya di akhir proses.

## Format Excel yang dibaca

Sheet dikenali dari awal namanya: `5 - ...` (per saluran), `5a - ...` (per petak tersier, juga dipakai untuk menentukan juru), dan `06 - ...` (debit). Susunan kolomnya harus sama dengan laporan saat ini.

## Catatan

- Data tanaman dan debit yang tampil adalah periode yang tertulis di bagian atas aplikasi.
- Bila luas baku di Excel dan poligon peta berbeda lebih dari 15%, aplikasi memakai yang terbesar dan menampilkan catatan. Luas baku bisa diubah dari tab Ringkasan.
- Menambah foto dan laporan dari HP baru aktif setelah `config.js` diisi (Supabase). Foto arsip di folder `foto/` tampil tanpa Supabase.

## Rencana berikutnya

- Skema Konstruksi (daftar bangunan per km) dari DXF.
- Hubungan petak ke titik bangunan di peta yang lebih lengkap.
