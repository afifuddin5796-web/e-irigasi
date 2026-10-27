# e-Irigasi

e-Irigasi adalah aplikasi web peta dan skema jaringan irigasi untuk para juru pengairan UPTD Purwosari, Kabupaten Pasuruan.
Menampilkan baku sawah, panjang saluran, bangunan, debit, dan realisasi tanam (padi, tebu, palawija, bero, habis panen) per daerah irigasi. Tema gelap, ringan, dan nyaman dibuka di HP.

## Fitur

- Pilih juru pengairan (Krangkong, Sadan, Sengon, Purwodadi, Rejoso, Sukorejo, Sukun), lalu daerah irigasi di bawahnya.
- Peta satelit atau peta gelap dengan koordinat, saluran, petak baku, dan bangunan (dari berkas KMZ).
- Tab **Skema**: gambar skema jaringan dari berkas DXF, bisa digeser dan diperbesar. Ketuk petak atau bangunan bagi untuk melihat data Excel, debit terukur, dan tombol "Lihat di peta".
- Tab **Ringkasan**: baku, panjang saluran, tanaman per DI, serta menu mengubah luas baku.
- Tab **Debit** dan **Bangunan**.
- Menu **Perbarui data tanaman**: unggah Excel laporan dengan format yang sama, hasilnya langsung tampil.

## Isi repositori

| Berkas | Fungsi |
|---|---|
| `index.html` | Seluruh aplikasi (satu berkas) |
| `data.json` | Data DI: peta, tanaman, debit, per petak |
| `manifest.webmanifest`, `sw.js`, `icons/` | Berkas PWA (bisa dipasang seperti aplikasi dan dibuka tanpa sinyal) |
| `skema/*.json` | Skema jaringan per DI (nama berkas = nomor DI di `data.json`) |
| `tools/` | Skrip Python untuk membangun ulang `data.json` dan `skema/` dari berkas sumber |
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
- Foto bangunan dan sinkronisasi antarperangkat belum ada. Rencananya memakai penyimpanan online bersama.

## Rencana berikutnya

- Foto bangunan (unggah dari HP, terhubung ke kode bangunan) dengan menu sinkron.
- Skema Konstruksi (daftar bangunan per km) dari DXF.
- Hubungan petak ke titik bangunan di peta yang lebih lengkap.
