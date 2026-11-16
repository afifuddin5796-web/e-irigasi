"""Mengambil semua lembar skema (daerah irigasi, konstruksi, sosiohidro, operasi) dari satu berkas DXF menjadi JSON vektor ringan."""
import re,math,json
import dxf_reader as dxf2
def fl(e,c,i=0,d=None):
    try: return float(e['p'][c][i])
    except: return d
def clean(t):
    t=re.sub(r'\\[ACcFfHhQqTtWw][^;]*;','',t); t=re.sub(r'\\[LlOoKk]','',t); t=t.replace('\\P','\n').replace('\\~',' ').replace('\\\\','\\')
    return re.sub(r'[{}]','',t).strip()
def cat(layer):
    l=layer.lower()
    if 'primer' in l: return 'p'
    if 'skund' in l or 'sekunder' in l: return 's'
    if 'ters' in l: return 't'
    if 'bangunan' in l: return 'b'
    return 'x'
def etext(e):
    return clean(''.join(e['p'].get('3',[]))+(e['p'].get('1',[''])[0]))
def bspline(ctrl,kn,deg,n=None):
    n=n or max(12,len(ctrl)*6); t0,t1=kn[deg],kn[len(ctrl)]; out=[]
    for i in range(n+1):
        t=t0+(t1-t0)*i/n
        if i==n: t=t1-1e-9
        k=deg
        while k<len(ctrl)-1 and not (kn[k]<=t<kn[k+1]): k+=1
        d=[list(ctrl[j+k-deg]) for j in range(deg+1)]
        for r in range(1,deg+1):
            for j in range(deg,r-1,-1):
                den=kn[j+1+k-r]-kn[j+k-deg]; a=(t-kn[j+k-deg])/den if den else 0
                d[j]=[(1-a)*d[j-1][0]+a*d[j][0],(1-a)*d[j-1][1]+a*d[j][1]]
        out.append(tuple(d[deg]))
    return out
def spline(e):
    P=e['p']; deg=int(float(P.get('71',['3'])[0]))
    ctrl=list(zip([float(v) for v in P.get('10',[])],[float(v) for v in P.get('20',[])]))
    kn=[float(v) for v in P.get('40',[])]
    fit=list(zip([float(v) for v in P.get('11',[])],[float(v) for v in P.get('21',[])]))
    if len(ctrl)>=deg+1 and len(kn)==len(ctrl)+deg+1:
        try: return bspline(ctrl,kn,deg)
        except Exception: pass
    if len(fit)>=2: return fit
    return ctrl
def arcpts(cx,cy,r,a0,a1,ccw=True):
    if ccw:
        while a1<=a0: a1+=360
    else:
        while a1>=a0: a1-=360
    n=max(6,int(abs(a1-a0)/10)); return [(cx+r*math.cos(math.radians(a0+(a1-a0)*i/n)),cy+r*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
def bulge_pts(p1,p2,b):
    """titik antara untuk segmen polyline berbulge (busur)"""
    if abs(b)<1e-9: return []
    dx,dy=p2[0]-p1[0],p2[1]-p1[1]; d=math.hypot(dx,dy)
    if d==0: return []
    off=(d/2)*(1-b*b)/(2*b); cx=(p1[0]+p2[0])/2+(-dy/d)*off; cy=(p1[1]+p2[1])/2+(dx/d)*off
    r=math.hypot(p1[0]-cx,p1[1]-cy); a0=math.atan2(p1[1]-cy,p1[0]-cx); th=4*math.atan(b); n=max(4,int(abs(th)/(math.pi/12)))
    return [(cx+r*math.cos(a0+th*i/n),cy+r*math.sin(a0+th*i/n)) for i in range(1,n)]
def poly_bulge(vs,bs,closed):
    out=[]
    for i,v in enumerate(vs):
        out.append(v)
        j=i+1 if i+1<len(vs) else (0 if closed else None)
        if j is not None and bs[i]: out+=bulge_pts(v,vs[j],bs[i])
    if closed: out.append(vs[0])
    return out
def hatch(e):
    """batas HATCH (jalur polyline atau tepi garis, busur, spline) menjadi daftar poligon"""
    r=e.get('r') or []; i=0; polys=[]
    def nxt(code):
        nonlocal i
        while i<len(r) and r[i][0]!=code: i+=1
        if i>=len(r): raise IndexError
        v=r[i][1]; i+=1; return v
    try:
        n=int(nxt('91'))
        for _ in range(n):
            flag=int(nxt('92')); pts=[]
            if flag&2:
                nv=int(nxt('93')); vs=[]; bl=[]
                for _ in range(nv):
                    x=float(nxt('10')); y=float(nxt('20')); b=0.0
                    if i<len(r) and r[i][0]=='42': b=float(r[i][1]); i+=1
                    vs.append((x,y)); bl.append(b)
                pts=poly_bulge(vs,bl,True)
            else:
                ne=int(nxt('93'))
                for _ in range(ne):
                    et=int(nxt('72'))
                    if et==1:
                        x1=float(nxt('10')); y1=float(nxt('20')); x2=float(nxt('11')); y2=float(nxt('21')); pts+=[(x1,y1),(x2,y2)]
                    elif et==2:
                        cx=float(nxt('10')); cy=float(nxt('20')); rr=float(nxt('40')); a0=float(nxt('50')); a1=float(nxt('51')); ccw=int(nxt('73'))
                        pts+=arcpts(cx,cy,rr,a0,a1,bool(ccw))
                    elif et==3:
                        cx=float(nxt('10')); cy=float(nxt('20')); mx=float(nxt('11')); my=float(nxt('21')); ratio=float(nxt('40')); a0=float(nxt('50')); a1=float(nxt('51')); ccw=int(nxt('73'))
                        a=math.hypot(mx,my); b=a*ratio; rot=math.atan2(my,mx)
                        if ccw:
                            while a1<=a0: a1+=360
                        else:
                            while a1>=a0: a1-=360
                        m=max(8,int(abs(a1-a0)/10))
                        for q in range(m+1):
                            th=math.radians(a0+(a1-a0)*q/m); px=a*math.cos(th); py=b*math.sin(th)
                            pts.append((cx+px*math.cos(rot)-py*math.sin(rot),cy+px*math.sin(rot)+py*math.cos(rot)))
                    elif et==4:
                        deg=int(nxt('94')); nxt('73'); nxt('74'); nk=int(nxt('95')); nc=int(nxt('96'))
                        kn=[float(nxt('40')) for _ in range(nk)]; ctrl=[]
                        for _ in range(nc):
                            x=float(nxt('10')); y=float(nxt('20')); ctrl.append((x,y))
                        pts+= bspline(ctrl,kn,deg) if len(kn)==nc+deg+1 and nc>=deg+1 else ctrl
            if len(pts)>=3: polys.append(pts)
    except (IndexError,ValueError): pass
    return polys
def flatten(B,ents,layer0='0',M=None,depth=0,out=None):
    """mengurai INSERT menjadi entitas dasar dengan transformasi M=(a,b,c,d,tx,ty)"""
    out=out if out is not None else []
    M=M or (1,0,0,1,0,0)
    def T(x,y): return (M[0]*x+M[2]*y+M[4], M[1]*x+M[3]*y+M[5])
    for e in ents:
        l=e['p'].get('8',['0'])[0]; l=layer0 if l=='0' and layer0!='0' else l
        t=e['t']
        if t=='LINE':
            x1,y1,x2,y2=fl(e,'10'),fl(e,'20'),fl(e,'11'),fl(e,'21')
            if None not in(x1,y1,x2,y2): out.append(('L',l,[T(x1,y1),T(x2,y2)]))
        elif t=='LWPOLYLINE':
            xs=[float(v) for v in e['p'].get('10',[])]; ys=[float(v) for v in e['p'].get('20',[])]
            if len(xs)==len(ys) and len(xs)>1:
                bs=[float(v) for v in e['p'].get('42',[])]; bs=bs if len(bs)==len(xs) else [0]*len(xs)
                pts=[T(*p) for p in poly_bulge(list(zip(xs,ys)),bs,e['p'].get('70',['0'])[0] in('1','129'))]
                out.append(('L',l,pts))
        elif t=='CIRCLE':
            x,y,r=fl(e,'10'),fl(e,'20'),fl(e,'40')
            if None not in(x,y,r):
                cx,cy=T(x,y); out.append(('C',l,(cx,cy,r*math.hypot(M[0],M[1]))))
        elif t=='ARC':
            x,y,r,a0,a1=fl(e,'10'),fl(e,'20'),fl(e,'40'),fl(e,'50'),fl(e,'51')
            if None not in(x,y,r,a0,a1): out.append(('L',l,[T(*p) for p in arcpts(x,y,r,a0,a1)]))
        elif t=='SPLINE':
            pts=spline(e)
            if len(pts)>1: out.append(('L',l,[T(*p) for p in pts]))
        elif t=='SOLID':
            q=[(fl(e,'10'),fl(e,'20')),(fl(e,'11'),fl(e,'21')),(fl(e,'13'),fl(e,'23')),(fl(e,'12'),fl(e,'22'))]
            if all(a is not None and b is not None for a,b in q): out.append(('F',l,[T(*p) for p in q]))
        elif t=='HATCH':
            for poly in hatch(e): out.append(('F',l,[T(*p) for p in poly]))
        elif t=='POINT':
            x,y=fl(e,'10'),fl(e,'20')
            if x is not None and y is not None: px,py=T(x,y); out.append(('C',l,(px,py,0.6)))
        elif t=='MTEXT' or t=='TEXT':
            x,y,h=fl(e,'10'),fl(e,'20'),fl(e,'40',0,2.5)
            if x is None or y is None: continue
            rot=fl(e,'50',0,0) or 0
            if fl(e,'11') is not None and t=='MTEXT': rot=math.degrees(math.atan2(fl(e,'21',0,0),fl(e,'11')))
            tx=etext(e) if t=='MTEXT' else clean(e['p'].get('1',[''])[0])
            if tx:
                px,py=T(x,y); sc=math.hypot(M[0],M[1]); rot+=math.degrees(math.atan2(M[1],M[0]))
                out.append(('T',l,(px,py,h*sc,rot,tx,int(fl(e,'71',0,1) or 1))))
        elif t=='INSERT' and depth<3:
            nm=e['p'].get('2',[''])[0]
            if nm in B:
                x,y=fl(e,'10',0,0),fl(e,'20',0,0); sx,sy=fl(e,'41',0,1),fl(e,'42',0,None); sy=sx if sy is None else sy
                r=math.radians(fl(e,'50',0,0)); c,s=math.cos(r),math.sin(r)
                bx,by=dxf2.BASES.get(nm,{}).get('10',0),dxf2.BASES.get(nm,{}).get('20',0)
                a,b_,c_,d=c*sx,s*sx,-s*sy,c*sy
                nm_=(M[0]*a+M[2]*b_, M[1]*a+M[3]*b_, M[0]*c_+M[2]*d, M[1]*c_+M[3]*d)
                tx0,ty0=T(x,y); ox,oy=nm_[0]*(-bx)+nm_[2]*(-by),nm_[1]*(-bx)+nm_[3]*(-by)
                flatten(B,B[nm],l,(nm_[0],nm_[1],nm_[2],nm_[3],tx0+ox,ty0+oy),depth+1,out)
    return out
TITLE=re.compile(r'SKEMA\s+(DAERAH\s+IRIGASI|KONTRUKSI|KONSTRUKSI|SOSIOHIDRO|OPERASI)',re.I)
NAMA={'DAERAH IRIGASI':'Skema daerah irigasi','KONTRUKSI':'Skema konstruksi','KONSTRUKSI':'Skema konstruksi','SOSIOHIDRO':'Skema sosiohidro','OPERASI':'Skema operasi'}
def find_frames(prims):
    """bingkai lembar gambar (persegi tertutup berukuran seperti kertas) yang memuat judul skema atau legenda"""
    tx=[(v[0],v[1],v[4]) for k,l,v in prims if k=='T' and (TITLE.search(v[4]) or re.search(r'LEGENDA',v[4],re.I))]
    cand=set()
    for k,l,v in prims:
        if k=='L' and len(v)==5 and abs(v[0][0]-v[4][0])<.01 and abs(v[0][1]-v[4][1])<.01:
            xs=[q[0] for q in v]; ys=[q[1] for q in v]; w,h=max(xs)-min(xs),max(ys)-min(ys)
            if 250<w<900 and 200<h<500 and len(set((round(a,1),round(b,1)) for a,b in v))==4:
                if any(min(xs)<=a<=max(xs) and min(ys)<=b<=max(ys) for a,b,_ in tx): cand.add((round(min(xs)),round(min(ys)),round(max(xs)),round(max(ys))))
    fr=[]
    for r in sorted(cand,key=lambda r:-(r[2]-r[0])*(r[3]-r[1])):
        if not any(r[0]>=q[0]-2 and r[1]>=q[1]-2 and r[2]<=q[2]+2 and r[3]<=q[3]+2 for q in fr): fr.append(r)
    return sorted(fr,key=lambda r:(-round(r[1]/60),r[0]))
def divider(prims,fr):
    x0,y0,x1,y1=fr; w=x1-x0; h=y1-y0; cand=[]
    for k,l,v in prims:
        if k=='L' and len(v)==2 and abs(v[0][0]-v[1][0])<0.5 and abs(v[0][1]-v[1][1])>0.72*h and x0+0.55*w<v[0][0]<x1-0.03*w and min(v[0][1],v[1][1])<y0+0.1*h: cand.append(v[0][0])
    return min(cand) if cand else x1
def clip_seg(p,q,box):
    """pemotongan segmen terhadap kotak (Liang-Barsky); mengembalikan (p2,q2) atau None"""
    x0,y0,x1,y1=box; dx,dy=q[0]-p[0],q[1]-p[1]; t0,t1=0.0,1.0
    for pp,qq in((-dx,p[0]-x0),(dx,x1-p[0]),(-dy,p[1]-y0),(dy,y1-p[1])):
        if pp==0:
            if qq<0: return None
        else:
            r=qq/pp
            if pp<0:
                if r>t1: return None
                t0=max(t0,r)
            else:
                if r<t0: return None
                t1=min(t1,r)
    return (p[0]+t0*dx,p[1]+t0*dy),(p[0]+t1*dx,p[1]+t1*dy)
def clip_poly(v,box):
    out=[];cur=[]
    for a,b in zip(v,v[1:]):
        c=clip_seg(a,b,box)
        if not c: 
            if len(cur)>1: out.append(cur)
            cur=[]; continue
        (p,q)=c
        if cur and abs(cur[-1][0]-p[0])<1e-6 and abs(cur[-1][1]-p[1])<1e-6: cur.append(q)
        else:
            if len(cur)>1: out.append(cur)
            cur=[p,q]
    if len(cur)>1: out.append(cur)
    return out
def sheet(prims,box,fr,nomor):
    x0,y0,x1,y1=box; e=0.6; R=lambda v: round(v,1)
    inside=lambda x,y:x0-e<=x<=x1+e and y0-e<=y<=y1+e
    paths={}; fills={}; C=[]; T=[]; tit=[]
    for k,l,v in prims:
        c=cat(l)
        if k=='L':
            if all(abs(p[0]-x0)<e or abs(p[0]-x1)<e or abs(p[1]-y0)<e or abs(p[1]-y1)<e for p in v): continue
            for sub in clip_poly(v,(x0-e,y0-e,x1+e,y1+e)):
                paths.setdefault(c,[]).append('M'+'L'.join(f'{R(p[0]-x0)} {R(y1-p[1])}' for p in sub))
        elif k=='F':
            if not all(inside(*p) for p in v): continue
            fills.setdefault(c,[]).append('M'+'L'.join(f'{R(p[0]-x0)} {R(y1-p[1])}' for p in v)+'Z')
        elif k=='C':
            if inside(v[0],v[1]) and v[2]<80: C.append([R(v[0]-x0),R(y1-v[1]),R(v[2]),c])
        elif k=='T':
            if inside(v[0],v[1]):
                T.append([R(v[0]-x0),R(y1-v[1]),R(v[2]),round(v[3]),v[4],v[5],c])
                m=TITLE.search(v[4])
                if m and 'PETA' not in v[4].upper(): tit.append((-v[1],v[0],NAMA[re.sub(r'\s+',' ',m.group(1).upper())]))
    judul=' · '.join(dict.fromkeys(n for _,_,n in sorted(tit))) or f'Lembar {nomor}'
    return dict(judul=judul,w=R(x1-x0),h=R(y1-y0),P={k:' '.join(v) for k,v in paths.items()},F={k:' '.join(v) for k,v in fills.items()},C=C,T=T)
def skema(path):
    B=dxf2.parse(path); prims=flatten(B,B.get('*ENTITIES',[]))
    frames=find_frames(prims)
    if not frames: return None
    sheets=[]; leg=None
    for n,fr in enumerate(frames,1):
        xd=divider(prims,fr); sheets.append(sheet(prims,(fr[0],fr[1],xd,fr[3]),fr,n))
        if leg is None and xd<fr[2]-20: leg=sheet(prims,(xd,fr[1],fr[2],fr[3]),fr,0); leg['judul']='Legenda'
    return dict(sheets=sheets,leg=leg)
