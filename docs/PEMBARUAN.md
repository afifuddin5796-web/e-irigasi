# Memperbarui baku sawah, peta KMZ, dan data tanaman

Semua pembaruan dilakukan dari aplikasi. Setelah itu satu berkas `data.json` diunggah ke GitHub supaya semua juru melihat data yang sama. Tidak perlu Python.

## Pembagian tugas

- **Juru:** hanya menambah foto bangunan (dan bila diminta, melaporkan kondisi). Menu perubahan data tidak tampil di HP mereka. Panduan singkatnya ada di [PANDUAN_JURU.md](PANDUAN_JURU.md), bisa dikirim lewat WhatsApp.
- **Pengelola data (Anda):** luas baku, peta KMZ, data tanaman dan debit, serta mengunggah `data.json`.

## Membuka mode pengelola

Menu perubahan data (luas baku, ganti peta KMZ, unggah Excel, unduh `data.json`) disembunyikan secara bawaan. Untuk membukanya di HP atau komputer Anda, **ketuk judul e-Irigasi di bagian atas 5 kali berturut-turut**. Muncul pesan "Mode pengelola aktif" dan label **Pengelola** di sebelah judul. Ketuk lima kali lagi untuk menutupnya.

Ini hanya merapikan tampilan juru, bukan kunci keamanan. Data bersama tetap terlindungi karena perubahan di aplikasi hanya tersimpan di perangkat itu, dan `data.json` di GitHub hanya berubah bila akun GitHub Anda yang mengunggahnya.

## Aturan emas

**Tunjuk satu orang sebagai pengelola data.** Hanya dia yang mengunggah `data.json` ke GitHub. Bila dua orang mengunggah bergantian dari data yang berbeda, unggahan terakhir menimpa yang sebelumnya.

## 1. Mengubah luas baku sawah

1. Buka DI, tab **Ringkasan**.
2. Pada kolom **Luas baku (ha)** isi angka yang benar, tekan **Simpan**.
3. Tombol **Kembalikan** membatalkan perubahan itu.

## 2. Mengganti peta (KMZ) sebuah DI

1. Buka DI yang petanya berubah, tab **Ringkasan**.
2. Pada **Ganti peta DI ini dari KMZ** pilih berkas `.kmz` atau `.kml` yang baru.
3. Aplikasi menampilkan perbandingan jumlah bangunan, saluran, panjang, dan luas poligon, sebelum dan sesudah. Tekan **OK** bila benar.
4. Peta, bangunan, panjang saluran, dan luas poligon DI itu berganti. Data tanaman dan debit tidak berubah.
5. **Kembalikan peta asli** membatalkannya.

Agar foto dan laporan kondisi tetap tertaut, **pertahankan nama bangunan** di KMZ yang baru (misalnya `3 BP 1` tetap `3 BP 1`).

## 3. Data tanaman dan debit (mingguan)

Di layar pilih juru, bagian **Perbarui data tanaman**, pilih Excel laporan terbaru.

## 4. Mengirim pembaruan ke semua juru

1. Di layar pilih juru, tekan **Unduh data.json untuk dibagikan**. Berkas ini sudah memuat semua perubahan di atas.
2. Buka halaman repositori e-irigasi di GitHub. Tekan **Add file > Upload files**, seret `data.json` yang baru diunduh, lalu **Commit changes**. Berkas dengan nama yang sama otomatis menggantikan yang lama.
3. Tunggu 2 sampai 5 menit. HP para juru mengambil data baru saat aplikasi dibuka dengan sinyal.

Perubahan yang tadinya hanya tersimpan di perangkat pengelola **dibersihkan otomatis** begitu `data.json` baru terbaca, jadi tidak ada data lama yang menutupi data resmi. Kalau perlu membatalkan semua perubahan di sebuah perangkat, tekan **Hapus semua perubahan di perangkat ini** di layar pilih juru.

## 5. Menambah sumber air, bendung, atau bangunan baru

Dikerjakan di **mode pengelola**. Ada dua cara.

**Satu atau beberapa titik (cara termudah):**
1. Buka DI-nya, tab **Ringkasan**, bagian **Tambah aset (titik) di DI ini**.
2. Pilih **jenis aset** (sumber air, bendung, pelimpah, dan seterusnya) dan isi **nama atau nomor**. Aplikasi menyusun namanya sesuai aturan, misalnya sumber air `Gayam 3` menjadi `MA Gayam 3`, dan menampilkan kelompoknya sebelum disimpan.
3. Isi koordinat: tekan **Pakai lokasi saya** (bila Anda sedang di lokasi), **Pakai titik tengah peta** (geser peta lalu tekan), atau tempel koordinat dari Google Maps (titik sebagai desimal, misalnya `-7.71290, 112.69362`).
4. Tekan **Simpan aset**. Titik langsung muncul di peta dan masuk ke kelompoknya. Salah memasukkan? Buka asetnya, tekan **Hapus aset**.

Untuk **bangunan bagi dan sadap**, tulis kode dan nomor seperti yang biasa dipakai, misalnya `BP 3`. Bila nama tidak dikenali, pratinjau menunjukkan "Aset lainnya" sehingga bisa dikoreksi sebelum disimpan.

**Banyak perubahan sekaligus (jaringan baru, banyak titik atau saluran):** perbarui berkas KMZ-nya di Google Earth atau aplikasi pemetaan Anda (tambah titik, garis saluran, atau poligon petak), lalu pakai **Ganti peta DI ini dari KMZ** seperti di bagian 2. Beri nama titik sesuai kebiasaan (`MA ...` untuk sumber air, `Bd ...` untuk bendung, `... bok`, `... ujung`, `... pelimpah`), karena pengelompokan aset membaca nama itu.

## 6. Menambah daerah irigasi (jaringan irigasi) baru

1. Siapkan berkas KMZ DI baru.
2. Buka layar juru yang membawahi DI itu, tab **Daerah irigasi**, bagian **Tambah daerah irigasi baru** (hanya tampil di mode pengelola).
3. Isi **nama DI**, pilih berkas KMZ, tekan **Tambah DI**, lalu setujui ringkasan yang muncul.
4. DI baru langsung masuk ke wilayah juru itu lengkap dengan peta, bangunan, panjang saluran, dan luas poligon.
5. Data tanaman dan debit terisi saat Excel yang memuat DI itu diunggah (menu **Perbarui data tanaman**), asalkan **nama DI di Excel sama** dengan yang Anda tulis di sini. Cek pesan "Tidak ditemukan di Excel" setelah mengunggah Excel.
6. Skema belum ada karena skema dibuat dari berkas DXF. Bila nanti DXF-nya ada, jalankan skrip pembuat skema (bagian 7).
7. Setelah selesai, kirim ke semua juru seperti di bagian 4 (**Unduh data.json** lalu unggah ke GitHub).

Simpan juga berkas KMZ baru di folder `data_sumber` di komputer Anda. Bila suatu saat `data.json` dibuat ulang dengan skrip, DI baru ikut terbawa.

## 7. Yang masih memakai skrip (jarang)

- DI yang namanya berubah di Excel.
- Skema jaringan (DXF) yang berubah.

Untuk keduanya, jalankan `tools/bangun_data.py` dan `tools/bangun_skema.py` (lihat README).

## Catatan

- Perubahan di aplikasi tersimpan di peramban perangkat itu. Bila data peramban dihapus sebelum diunggah, perubahan hilang. Biasakan menekan **Unduh data.json** lalu mengunggahnya segera setelah selesai mengedit.
- Peta KMZ yang sangat besar bisa membuat penyimpanan peramban penuh. Aplikasi memberi pesan bila itu terjadi.
