"""Menyiapkan foto bangunan agar bisa disimpan langsung di repositori GitHub (folder foto/).

Foto dikecilkan, ditaruh di foto/<DI>/<folder>/<nomor>.jpg dengan gambar kecil <nomor>_t.jpg,
dan dibuatkan daftar foto/<DI>.json yang dibaca aplikasi. Foto asli tidak diubah.

Pemakaian:
  python tools/siapkan_foto_repo.py "D:/DATA/irigasi apk/foto" --kering     (hanya memeriksa dan memperkirakan ukuran)
  python tools/siapkan_foto_repo.py "D:/DATA/irigasi apk/foto"
Lalu unggah folder foto/ ke repositori dengan GitHub Desktop (jumlah berkasnya banyak)."""
import os,sys,json,argparse,random,time
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); sys.path.insert(0,HERE)
import foto_umum as fu
ap=argparse.ArgumentParser(); ap.add_argument('foto'); ap.add_argument('--kering',action='store_true')
ap.add_argument('--keluaran',default=os.path.join(ROOT,'foto')); ap.add_argument('--sisi',type=int,default=1024); ap.add_argument('--kualitas',type=int,default=70)
ap.add_argument('--thumb',type=int,default=360); ap.add_argument('--hanya',default=''); ap.add_argument('--alias',default='')
ap.add_argument('--data',default=os.path.join(ROOT,'data.json')); A=ap.parse_args()
PT=fu.Peta(A.data,A.alias); daftar,tak,njd=PT.cari(A.foto,A.hanya); total=len(daftar)
print(f'Folder DI cocok: {njd} | foto: {total} | otomatis tertaut ke bangunan: {sum(1 for x in daftar if x[3])}')
if tak: print('Folder yang TIDAK cocok dengan DI mana pun (buat berkas alias bila perlu):'); [print('  -',x) for x in tak]
if A.kering:
    smp=random.sample(daftar,min(40,len(daftar))); tot=0; t0=time.time()
    for *_,f in smp: a,b,_=fu.kecil(f,A.sisi,A.kualitas,A.thumb); tot+=len(a)+len(b)
    if smp:
        mb=tot/len(smp)*total/1e6; print(f'Perkiraan ukuran folder foto/: {mb:.0f} MB (rata-rata {tot/len(smp)/1024:.0f} KB per foto, {(time.time()-t0)/len(smp):.2f} detik per foto)')
        print('Batas yang dianjurkan GitHub: repositori di bawah 1 GB.', 'MELEBIHI, perkecil dengan --sisi 800 --kualitas 65 atau simpan sebagian foto di Supabase.' if mb>900 else 'Masih di bawah batas.')
    sys.exit(0)
idx={}; dipakai=set(); n=0
for i,(d,folder,stem,b,f) in enumerate(daftar,1):
    base=f'{fu.slug(d["nama"])}/{fu.slug(folder)}/{fu.slug(stem)}'; p=base; k=2
    while p in dipakai: p=f'{base}-{k}'; k+=1
    dipakai.add(p); out=os.path.join(A.keluaran,*p.split('/'))
    os.makedirs(os.path.dirname(out),exist_ok=True)
    if not os.path.exists(out+'.jpg'):
        try: full,th,tgl=fu.kecil(f,A.sisi,A.kualitas,A.thumb)
        except Exception as e: print('  lewati (tidak terbaca):',f,e); continue
        open(out+'.jpg','wb').write(full); open(out+'_t.jpg','wb').write(th); n+=1
    idx.setdefault(fu.slug(d['nama']),[]).append(dict(folder=folder,nomor=stem,bangunan=b,path='foto/'+p+'.jpg',thumb='foto/'+p+'_t.jpg'))
    if i%100==0: print(f'  {i}/{total} ...',flush=True)
for k,v in idx.items(): json.dump(v,open(os.path.join(A.keluaran,k+'.json'),'w'),ensure_ascii=False,separators=(',',':'))
print(f'Selesai. Foto diproses baru: {n} | daftar per DI: {len(idx)} berkas | lokasi: {A.keluaran}')
