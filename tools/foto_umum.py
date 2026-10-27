"""Fungsi bersama untuk mengolah folder foto: mencocokkan folder dengan DI, menautkan ke bangunan, dan mengecilkan gambar."""
import os,re,io,json,difflib,unicodedata
from datetime import datetime
from PIL import Image,ImageOps
EXT=('.jpg','.jpeg','.png','.webp')
def norm(s):
    s=s.lower(); s=re.sub(r'\b(di|ji|sbr|sumber|ters|desa)\b\.?',' ',s); s=re.sub(r'\b(19|20)\d\d\b',' ',s); s=re.sub(r'\b(ok|sip|fix|fixs|top)\b',' ',s)
    return re.sub(r'[^a-z0-9]','',s)
def slug(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+','-',s).strip('-') or 'x'
def alnum(s): return re.sub(r'[^a-z0-9]','',s.lower())
class Peta:
    def __init__(self,data_json,alias_json=''):
        self.DB=json.load(open(data_json))['di']; self.keys={}
        for d in self.DB:
            self.keys.setdefault(norm(d['nama']),d)
            for k in d['xk']: self.keys.setdefault(k.replace('~s',''),d)
        self.alias=json.load(open(alias_json)) if alias_json else {}; self.byname={d['nama']:d for d in self.DB}
    def cocok(self,folder):
        if folder in self.alias: return self.byname.get(self.alias[folder])
        f=re.sub(r'^\d+[A-Za-z]?\.?\s*','',folder.strip()); f=re.sub(r'\s+(ok|sip|fix|fixs|top)$','',f,flags=re.I)
        luar=re.sub(r'\(.*?\)','',f); dalam=re.findall(r'\((.*?)\)',f)
        for c in [norm(x) for x in [luar]+dalam+[f.replace('(',' ').replace(')',' ')]]:
            if c in self.keys: return self.keys[c]
        for c in [norm(x) for x in dalam+[luar]]:
            m=difflib.get_close_matches(c,list(self.keys),1,0.88)
            if m: return self.keys[m[0]]
    def tautkan(self,d,stem):
        nm=[b[0] for b in d['bangunan']]
        if stem.isdigit():
            c=[n for n in nm if re.match(r'^%d\s'%int(stem),n)]
            return c[0] if len(c)==1 else None
        s=alnum(stem); polos=lambda n: alnum(re.sub(r'^\d+[a-z]?\s*','',n,flags=re.I))
        c=[n for n in nm if polos(n)==s]
        if not c and len(s)>=5: c=[n for n in nm if len(polos(n))>=5 and (polos(n) in s or s in polos(n))]
        return c[0] if len(c)==1 else None
    def cari(self,root,hanya=''):
        """-> (daftar [(d,folder,stem,bangunan,path)], folder_tak_cocok, jumlah_DI)"""
        dis={}; tak=[]
        for nm in sorted(os.listdir(root)):
            p=os.path.join(root,nm)
            if not os.path.isdir(p): continue
            d=self.cocok(nm)
            if not d: tak.append(nm); continue
            if hanya and hanya.lower() not in d['nama'].lower(): continue
            dis.setdefault(d['nama'],(d,[]))[1].append(p)
        daftar=[]
        for nama,(d,paths) in dis.items():
            for p in paths:
                for dp,_,fs in os.walk(p):
                    rel=os.path.relpath(dp,p); folder='umum' if rel=='.' else ' / '.join(rel.split(os.sep))
                    for f in sorted(fs):
                        if f.lower().endswith(EXT):
                            stem=os.path.splitext(f)[0]; daftar.append((d,folder,stem,self.tautkan(d,stem),os.path.join(dp,f)))
        return daftar,tak,len(dis)
def kecil(path,sisi=1280,kualitas=75,thumb=360):
    im=Image.open(path); tgl=None
    try:
        v=im.getexif().get_ifd(0x8769).get(36867)
        if v: tgl=datetime.strptime(v,'%Y:%m:%d %H:%M:%S').isoformat()
    except Exception: pass
    im=ImageOps.exif_transpose(im).convert('RGB'); out=[]
    for s,q in((sisi,kualitas),(thumb,70)):
        t=im.copy(); t.thumbnail((s,s),Image.LANCZOS); b=io.BytesIO(); t.save(b,'JPEG',quality=q,optimize=True); out.append(b.getvalue())
    return out[0],out[1],tgl or datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
