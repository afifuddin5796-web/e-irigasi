-- Jalankan SEKALI di Supabase: SQL Editor > New query > tempel seluruh isi berkas ini > Run.

create table if not exists public.foto (
  id        bigint generated always as identity primary key,
  di_nama   text not null,            -- nama DI persis seperti di data.json
  folder    text not null,            -- nama folder saluran atau area
  nomor     text,                     -- nomor atau nama berkas tanpa ekstensi
  bangunan  text,                     -- nama bangunan di peta (boleh kosong)
  path      text not null unique,     -- jalur foto di penyimpanan
  thumb     text,                     -- jalur gambar kecil
  catatan   text,
  oleh      text,                     -- nama pengunggah
  diambil   timestamptz,
  dibuat    timestamptz not null default now()
);
create index if not exists foto_di_idx on public.foto (di_nama);

alter table public.foto enable row level security;
create policy "foto_baca"    on public.foto for select to anon using (true);
create policy "foto_tambah"  on public.foto for insert to anon with check (true);
create policy "foto_tautkan" on public.foto for update to anon using (true) with check (true);

-- Aplikasi hanya boleh mengubah tautan bangunan dan catatan, tidak boleh menghapus.
revoke update, delete on public.foto from anon;
grant select, insert on public.foto to anon;
grant update (bangunan, catatan) on public.foto to anon;

-- Tempat penyimpanan berkas foto (publik untuk dibaca, hanya JPEG, maksimal 5 MB per berkas).
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('foto', 'foto', true, 5242880, array['image/jpeg'])
on conflict (id) do update set public = true, file_size_limit = 5242880, allowed_mime_types = array['image/jpeg'];

create policy "foto_baca_berkas"   on storage.objects for select to anon using (bucket_id = 'foto');
create policy "foto_unggah_berkas" on storage.objects for insert to anon with check (bucket_id = 'foto');
