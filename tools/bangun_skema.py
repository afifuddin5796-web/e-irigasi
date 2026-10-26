"""Membangun folder skema/ dari berkas DXF.
Pemakaian: python tools/bangun_skema.py FOLDER_SUMBER [FOLDER_KELUARAN]  (data.json harus sudah ada di folder keluaran)"""
import re,os,sys,json,glob,difflib
sys.path.insert(0,os.path.dirname(__file__))
import skema_extract
SUMBER=sys.argv[1] if len(sys.argv)>1 else 'data_sumber'; OUT=sys.argv[2] if len(sys.argv)>2 else '.'
def norm(s):
    s=s.lower(); s=re.sub(r'\b(di|ji|sbr|sumber|ters|desa)\b\.?',' ',s); s=re.sub(r'\(.*?\)',' ',s)
    s=re.sub(r'\b(19|20)\d\d\b',' ',s); s=re.sub(r'\b(ok|sip|fix|fixs|top)\b',' ',s)
    return re.sub(r'[^a-z0-9]','',s)
DB=json.load(open(os.path.join(OUT,'data.json'))); keys={}
for d in DB['di']:
    keys.setdefault(norm(d['nama']),d['id'])
    for k in d['xk']: keys.setdefault(k.replace('~s',''),d['id'])
byname={d['nama']:d['id'] for d in DB['di']}
# nama berkas DXF yang mirip tetapi milik DI berbeda
OVR={'35. DI KARANGLEBAK':'Kr. Lebak','276. DI SUMBER KARANGLEBAK':'Sbr. Karanglebak','SUMBERTITING':'Sumbertiting'}
rx=re.compile(r'^(?:\d+[A-Z]?\s+)?(?:\d+\.?\s*)?(?:(?:DI|JI)\.?\s*)?(.*?)\s+((?:19|20)\d\d)\s+\w+\.dxf$',re.I)
best={}; unk=[]
for f in glob.glob(os.path.join(SUMBER,'**','*.dxf'),recursive=True):
    b=os.path.basename(f); m=rx.match(b)
    if not m: unk.append(b); continue
    yr=int(m.group(2)); did=None
    for pre,x in OVR.items():
        if pre in b and x in byname: did=byname[x]
    if did is None:
        mk=difflib.get_close_matches(norm(m.group(1)),list(keys),1,0.8)
        if not mk: unk.append(b); continue
        did=keys[mk[0]]
    if did not in best or yr>best[did][1]: best[did]=(f,yr)
os.makedirs(os.path.join(OUT,'skema'),exist_ok=True); gagal=[]
for did,(f,yr) in sorted(best.items()):
    try: r=skema_extract.skema(f)
    except Exception as e: r=None
    if not r: gagal.append(os.path.basename(f)); continue
    json.dump(r,open(os.path.join(OUT,'skema',f'{did}.json'),'w'),ensure_ascii=False,separators=(',',':'))
print('skema dibuat:',len(best)-len(gagal),'dari',len(DB['di']),'DI')
print('DXF tak terpetakan:',unk); print('DXF gagal dibaca:',gagal)
print('DI tanpa DXF:',[d['nama'] for d in DB['di'] if d['id'] not in best])
