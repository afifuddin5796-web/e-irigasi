-- Tambahan untuk laporan kondisi bangunan. Jalankan SEKALI di Supabase: SQL Editor > New query > tempel > Run.
-- (Jalankan supabase.sql lebih dulu bila belum.)

create table if not exists public.laporan (
  id        bigint generated always as identity primary key,
  di_nama   text not null,
  bangunan  text not null,            -- nama bangunan di peta
  kondisi   text not null check (kondisi in ('baik','rusak ringan','rusak sedang','rusak berat')),
  catatan   text,
  oleh      text,                     -- nama pelapor
  lat       double precision,         -- lokasi HP saat melapor (boleh kosong)
  lon       double precision,
  akurasi   real,                     -- ketelitian lokasi dalam meter
  dibuat    timestamptz not null default now()
);
create index if not exists laporan_di_idx on public.laporan (di_nama, bangunan, dibuat desc);

alter table public.laporan enable row level security;
create policy "laporan_baca"   on public.laporan for select to anon using (true);
create policy "laporan_tambah" on public.laporan for insert to anon with check (true);
revoke update, delete on public.laporan from anon;
grant select, insert on public.laporan to anon;
