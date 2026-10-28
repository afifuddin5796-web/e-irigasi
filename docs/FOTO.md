# Foto, kondisi bangunan, dan koordinat

## Pilihan penyimpanan foto

| | Foto lama (arsip) lewat repositori | Foto baru dan laporan lewat Supabase |
|---|---|---|
| Biaya dan akun | Gratis, tanpa akun tambahan | Perlu akun Supabase (ada paket gratis) |
| Bisa ditambah dari HP juru | Tidak | Ya |
| Batas | Repositori sebaiknya di bawah 1 GB, jadi foto harus dikecilkan | Penyimpanan paket gratis kecil (sekitar 1 GB, periksa batas terbaru) |
| Bisa dilihat tanpa Supabase | Ya | Tidak |

**Saran:** arsip foto lama ditaruh di repositori (bagian A), sedangkan foto baru dan laporan kondisi dari lapangan lewat Supabase (bagian B), karena hanya itu yang bisa ditulis dari HP. Dengan begitu Supabase hanya menampung foto yang jumlahnya jauh lebih sedikit. Keduanya tampil bersama di tab **Foto**.

## A. Foto lama lewat repositori

Foto Anda (folder DI, folder saluran, lalu `1.jpg`, `2.jpg`) dikecilkan dan disusun menjadi folder `foto/` beserta daftar per DI. Foto asli di komputer tidak berubah.

```bash
pip install -r tools/requirements.txt
# 1) periksa dulu: jumlah foto, perkiraan ukuran, folder yang tidak cocok
python tools/siapkan_foto_repo.py "D:/DATA/MOHAMAD- AFIFUDDIN/irigasi apk/foto" --kering
# 2) buat folder foto/ di dalam repositori
python tools/siapkan_foto_repo.py "D:/DATA/MOHAMAD- AFIFUDDIN/irigasi apk/foto"
```

- Pemeriksaan memberi **perkiraan ukuran**. Bila melebihi sekitar 900 MB, perkecil dengan `--sisi 800 --kualitas 65`, atau pakai Supabase untuk sebagian foto.
- Folder yang tidak cocok dengan nama DI ditampilkan di akhir. Buat `alias.json` berisi `{"nama folder": "nama DI di data.json"}` lalu tambahkan `--alias alias.json`.
- Skrip aman dijalankan ulang: foto yang sudah ada dilewati.
- Penautan otomatis ke bangunan memakai dua aturan. (1) Nama berkas dicocokkan dengan nama bangunan: `1 bd kecambah.jpg` tertaut ke `1 Bd Kecambah`, `1 Bd Sembojo.jpg` ke `0 Bd Sembojo`. (2) Berkas bernomor (`3.jpg`) dicocokkan dengan nomor bangunan. Bila ada beberapa bangunan bernomor sama, dipilih yang paling dekat dengan petak atau saluran yang namanya sama dengan folder (misalnya folder `Banyak Putih`). Bila tetap tidak yakin, foto dibiarkan tanpa tautan. Hasil otomatis ini tebakan terbaik: koreksi dengan mengetuk foto di aplikasi lalu memilih bangunan yang benar.
- Unggah folder `foto/` ke GitHub memakai **GitHub Desktop** (berkasnya ribuan, sedangkan unggahan lewat browser dibatasi sekitar 100 berkas). Foto dari repositori tidak bisa diubah tautannya dari aplikasi.

## B. Foto baru, laporan kondisi, dan sinkron (Supabase)

1. Daftar di supabase.com, **New project**, nama `e-irigasi`, region Southeast Asia (Singapore). Simpan kata sandi database.
2. Buka **SQL Editor > New query**. Tempel isi [supabase.sql](supabase.sql), tekan **Run**. Lalu query baru lagi, tempel isi [supabase_laporan.sql](supabase_laporan.sql), tekan **Run**. Masing-masing dijalankan sekali saja.
3. Buka **Project Settings > API**. Salin **Project URL** dan kunci **anon public**.
4. Isi `SUPABASE_URL` dan `SUPABASE_KEY` di `config.js` pada repositori. Tunggu semenit, muat ulang aplikasi.

Setelah aktif, di tab **Foto** setiap DI ada formulir untuk memilih folder, bangunan, dan foto dari kamera atau galeri. Foto dikecilkan di HP lebih dulu. Tanpa sinyal, foto masuk antrean dan terkirim saat tombol **Sinkron** ditekan.

Bila Anda lebih suka menaruh semua foto lama di Supabase, `python tools/unggah_foto.py "<folder foto>" --kering` lalu tanpa `--kering` melakukannya (skrip bisa dijalankan ulang bila terputus).

## C. Laporan kondisi bangunan saat juru di lokasi

1. Buka DI, tab **Bangunan**, ketuk bangunannya (atau ketuk titik hijau di peta lalu **Detail**).
2. Pada **Laporkan kondisi** pilih kondisi (baik, rusak ringan, rusak sedang, rusak berat), isi catatan dan nama pelapor, pilih foto bila ada.
3. Ketuk **Pakai lokasi saya** bila ingin menyertakan lokasi HP. Aplikasi menampilkan jarak ke bangunan dan memberi peringatan bila lebih dari 300 m.
4. Ketuk **Kirim laporan**.

Titik bangunan di peta berubah warna sesuai laporan terakhir (biru baik, kuning rusak ringan, oranye rusak sedang, merah rusak berat). Di rincian bangunan tampil enam laporan terakhir dan foto yang tertaut. Laporan yang dikirim tanpa sinyal tersimpan di HP dan terkirim lewat **Sinkron** di tab Foto.

## Tanda bangunan di peta

Saat sebuah bangunan dipilih (di formulir foto, di daftar bangunan, atau lewat tombol **Lihat di peta**), peta bergerak ke bangunan itu dan menandainya dengan lingkaran merah berdenyut. Label merah di atas peta menampilkan namanya, dan tombol **Hapus tanda** menghilangkannya.

## D. Koordinat dan Google Maps

- Kotak di kiri bawah peta menampilkan koordinat titik yang disentuh atau pusat peta, dengan tombol **Salin** dan **Maps**.
- Pada bangunan (popup di peta dan rincian bangunan) ada **Salin** dan **Maps**. Tombol Maps membuka lokasi di Google Maps (di HP biasanya langsung ke aplikasi Maps) sehingga bisa dipakai untuk navigasi.

## Catatan

- Kunci `anon public` memang dirancang berada di aplikasi. Konsekuensinya siapa pun yang tahu alamat dan kunci itu bisa menambah foto dan laporan. Aplikasi tidak bisa menghapus apa pun. Penghapusan lewat dashboard Supabase (Table Editor dan Storage). Bila nanti perlu pembatasan per juru, ada opsi login Supabase.
- Paket gratis Supabase menjeda proyek yang tidak aktif sekitar seminggu. Aktifkan lagi dari dashboard.
- Simpan foto asli di komputer sebagai cadangan.
