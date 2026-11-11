"""Membuat desa.json (batas desa yang disederhanakan) dari berkas KMZ batas desa.
Pemakaian: python tools/bangun_desa.py "data_sumber/BATAS DESA KAB PASURUAN.kmz" [desa.json]
Aplikasi memakai berkas ini untuk menentukan desa dan kecamatan tiap aset dari koordinatnya."""
import re,sys,json,zipfile,math,html
src=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else 'desa.json'; TOL=0.00012   # sekitar 13 m
z=zipfile.ZipFile(src); t=z.read([n for n in z.namelist() if n.endswith('.kml')][0]).decode('utf8','ignore')
def dp(pts,tol):
    if len(pts)<4: return pts
    keep=[False]*len(pts); keep[0]=keep[-1]=True; st=[(0,len(pts)-1)]
    while st:
        a,b=st.pop(); (x1,y1),(x2,y2)=pts[a],pts[b]; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy); m=-1;mi=a
        for i in range(a+1,b):
            x,y=pts[i]; d=abs(dy*x-dx*y+x2*y1-y2*x1)/L if L else math.hypot(x-x1,y-y1)
            if d>m: m,mi=d,i
        if m>tol: keep[mi]=True; st+= [(a,mi),(mi,b)]
    return [p for p,k in zip(pts,keep) if k]
rows=[]
for pm in re.findall(r'<Placemark>[\s\S]*?</Placemark>',t):
    g=lambda k:(re.search(r'<SimpleData name="%s">([^<]*)</SimpleData>'%k,pm) or [0,''])[1].strip()
    m=re.search(r'<outerBoundaryIs>[\s\S]*?<coordinates>([\s\S]*?)</coordinates>',pm)
    if not m: continue
    pts=[]
    for k in m.group(1).split():
        p=k.split(',')
        if len(p)>=2: pts.append((float(p[1]),float(p[0])))
    if len(pts)<4: continue
    pts=dp(pts,TOL); flat=[round(v,5) for p in pts for v in p]
    la=[p[0] for p in pts]; lo=[p[1] for p in pts]
    rows.append([html.unescape(g('DESA')),html.unescape(g('KECAMATAN')),[min(la),min(lo),max(la),max(lo)],flat])
json.dump(dict(d=rows),open(out,'w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
import os; print('desa:',len(rows),'| titik:',sum(len(r[3])//2 for r in rows),'|',round(os.path.getsize(out)/1024),'KB ->',out)
