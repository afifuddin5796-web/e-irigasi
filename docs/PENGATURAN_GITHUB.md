# Pengaturan GitHub

## Identitas repositori

- **Nama:** `e-irigasi`
- **Deskripsi (kolom About):** e-Irigasi, aplikasi web peta dan skema jaringan irigasi UPTD Purwosari, Kab. Pasuruan: baku sawah, saluran, bangunan, debit, dan realisasi tanam per juru pengairan. Tema gelap, ringan, untuk HP.
- **Website (kolom About):** `https://afifuddin5796-web.github.io/e-irigasi/`
- **Topics:** `irigasi` `peta` `gis` `kmz` `leaflet` `pasuruan` `juru-pengairan` `dark-theme` `github-pages`

## Public atau Private

Repositori memuat peta jaringan, bangunan, dan data tanaman. Bila data itu tidak boleh dilihat umum, pertimbangkan dulu izin dari atasan atau instansi. Repositori **Public** bisa dibuka siapa saja yang tahu alamatnya. GitHub Pages untuk repositori **Private** umumnya memerlukan paket berbayar.

## Langkah membuat dan memasang

1. Masuk GitHub, tekan **New repository**. Isi nama `e-irigasi`, deskripsi di atas, pilih Public atau Private, **jangan** centang README (berkas ini sudah ada). Tekan **Create repository**.
2. Unggah isi repositori:
   - **Lewat browser:** pada halaman repositori yang kosong pilih **uploading an existing file**, lalu seret `index.html`, `data.json`, `README.md`, `.gitignore`, `.nojekyll`, folder `tools`, `docs`, dan `data_sumber`. Isi pesan commit, tekan **Commit changes**.
   - Folder `skema` berisi 117 berkas, sedangkan unggahan lewat browser dibatasi sekitar 100 berkas sekali kirim. Unggah dalam dua kali: berkas 1 sampai 60, lalu sisanya.
   - **Lewat GitHub Desktop** (lebih mudah untuk banyak berkas): buat repositori, **Add local repository** ke folder ini, lalu **Commit** dan **Push**.
3. Aktifkan Pages: **Settings > Pages**, pada Source pilih **Deploy from a branch**, Branch **main**, folder **/ (root)**, tekan **Save**. Tunggu 1 sampai 3 menit.
4. Buka `https://afifuddin5796-web.github.io/e-irigasi/`. Bila layar hanya "Memuat data", pastikan `data.json` dan folder `skema` ada di tingkat yang sama dengan `index.html`.
5. Isi kolom **About** (ikon roda gigi di halaman utama repositori): deskripsi, website, dan topics di atas.

## Setelah itu

- Bagikan alamat Pages ke para juru. Di HP, buka lewat Chrome lalu **Tambahkan ke layar utama**.
- Untuk memperbarui data, lihat bagian "Memperbarui data" di README.
