"""Unggah massal foto bangunan dari komputer ke penyimpanan Supabase.

Susunan folder yang dibaca:  FOTO/<folder DI>/<folder saluran atau area>/<nomor>.jpg
dan berkas langsung di folder DI (misalnya "1 Bd Kecambah.jpg").

Pemakaian:
  python tools/unggah_foto.py "D:/DATA/irigasi apk/foto" --kering      (hanya memeriksa, tidak mengunggah)
  python tools/unggah_foto.py "D:/DATA/irigasi apk/foto" --oleh "Nama Anda"
Aman dijalankan berulang: foto yang sudah terunggah dilewati."""
import os,re,sys,json,io,random,argparse,difflib,time,urllib.request,urllib.error,urllib.parse
from datetime import datetime
from PIL import Image,ImageOps
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
ap=argparse.ArgumentParser()
ap.add_argument('foto'); ap.add_argument('--kering',action='store_true',help='periksa saja, tanpa mengunggah')
ap.add_argument('--oleh',default=''); ap.add_argument('--sisi',type=int,default=1280); ap.add_argument('--kualitas',type=int,default=75)
ap.add_argument('--thumb',type=int,default=360); ap.add_argument('--hanya',default='',help='proses DI yang namanya memuat teks ini')
ap.add_argument('--alias',default='',help='berkas JSON {"nama folder": "nama DI"} untuk folder yang gagal dicocokkan')
ap.add_argument('--config',default=os.path.join(ROOT,'config.js')); ap.add_argument('--data',default=os.path.join(ROOT,'data.json'))
ap.add_argument('--url',default=''); ap.add_argument('--key',default='')
A=ap.parse_args()
cfg=open(A.config).read() if os.path.exists(A.config) else ''
URL=(A.url or (re.search(r"SUPABASE_URL:'([^']*)'",cfg) or [0,''])[1]).rstrip('/'); KEY=A.key or (re.search(r"SUPABASE_KEY:'([^']*)'",cfg) or [0,''])[1]
if not A.kering and not (URL and KEY): sys.exit('SUPABASE_URL dan SUPABASE_KEY di config.js belum diisi (lihat docs/FOTO.md).')
sys.path.insert(0,HERE)
import foto_umum as fu
slug=fu.slug; kecil=lambda p: fu.kecil(p,A.sisi,A.kualitas,A.thumb)
PT=fu.Peta(A.data,A.alias)
def api(method,path,body=None,headers=None,tries=4):
    h={'apikey':KEY,'Authorization':'Bearer '+KEY}; h.update(headers or {})
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL+path,data=body,method=method,headers=h),timeout=120) as r: return r.status,r.read()
        except urllib.error.HTTPError as e:
            t=e.read().decode('utf8','ignore')
            if e.code in(400,409) and ('uplicate' in t or 'already exists' in t): return 409,b''
            if e.code<500 and e.code!=429: raise RuntimeError(f'{method} {path[:70]} -> {e.code} {t[:150]}')
        except (urllib.error.URLError,TimeoutError): pass
        time.sleep(2*(i+1))
    raise RuntimeError('gagal terhubung: '+path[:70])
daftar,tak,njd=PT.cari(A.foto,A.hanya); total=len(daftar); lnk=sum(1 for x in daftar if x[3])
print(f'Folder DI cocok: {njd} | foto: {total} | otomatis tertaut ke bangunan: {lnk}')
if tak: print('Folder yang TIDAK cocok dengan DI mana pun (buat berkas alias bila perlu):'); [print('  -',x) for x in tak]
if A.kering:
    smp=random.sample(daftar,min(30,len(daftar))); tot=0; t0=time.time()
    for *_,f in smp: a,b,_=kecil(f); tot+=len(a)+len(b)
    if smp: print(f'Perkiraan ukuran setelah dikecilkan: {tot/len(smp)*total/1e6:.0f} MB (rata-rata {tot/len(smp)/1024:.0f} KB per foto, {(time.time()-t0)/len(smp):.2f} detik per foto)')
    sys.exit(0)
ada=set(); off=0
while True:
    _,r=api('GET',f'/rest/v1/foto?select=path&order=id&limit=1000&offset={off}'); rs=json.loads(r); ada.update(x['path'] for x in rs); off+=1000
    if len(rs)<1000: break
dipakai=set(ada); baru=lewat=0; batch=[]
def simpan():
    global batch
    if batch:
        api('POST','/rest/v1/foto?on_conflict=path',json.dumps(batch).encode(),{'Content-Type':'application/json','Prefer':'return=minimal,resolution=ignore-duplicates'}); batch=[]
for i,(d,folder,stem,b,f) in enumerate(daftar,1):
    base=f'{slug(d["nama"])}/{slug(folder)}/{slug(stem)}'; p=base+'.jpg'; n=2
    key=(d['nama'],folder,stem)
    while p in dipakai and p not in ada: p=f'{base}-{n}.jpg'; n+=1
    if p in ada: lewat+=1; dipakai.add(p); continue
    dipakai.add(p); tp=p[:-4]+'_t.jpg'
    try: full,th,tgl=kecil(f)
    except Exception as e: print('  lewati (tidak terbaca):',f,e); continue
    for pp,bb in((p,full),(tp,th)): api('POST','/storage/v1/object/foto/'+urllib.parse.quote(pp),bb,{'Content-Type':'image/jpeg'})
    batch.append(dict(di_nama=d['nama'],folder=folder,nomor=stem,bangunan=b,path=p,thumb=tp,oleh=A.oleh or None,diambil=tgl)); baru+=1
    if len(batch)>=50: simpan()
    if i%25==0: print(f'  {i}/{total} ...',flush=True)
simpan(); print(f'Selesai. Terunggah baru: {baru} | dilewati (sudah ada): {lewat}')
