"""Mengambil lembar Skema Daerah Irigasi dari satu berkas DXF menjadi JSON vektor ringan."""
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
def flatten(B,ents,layer0='0',M=None,depth=0,out=None):
    """expand INSERT into primitive entities with transform M=(a,b,c,d,tx,ty)"""
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
                pts=[T(x,y) for x,y in zip(xs,ys)]
                if (e['p'].get('70',['0'])[0] in('1','129')): pts.append(pts[0])
                out.append(('L',l,pts))
        elif t=='CIRCLE':
            x,y,r=fl(e,'10'),fl(e,'20'),fl(e,'40')
            if None not in(x,y,r):
                cx,cy=T(x,y); out.append(('C',l,(cx,cy,r*math.hypot(M[0],M[1]))))
        elif t=='ARC':
            x,y,r,a0,a1=fl(e,'10'),fl(e,'20'),fl(e,'40'),fl(e,'50'),fl(e,'51')
            if None not in(x,y,r,a0,a1):
                if a1<a0: a1+=360
                n=max(4,int((a1-a0)/12)); out.append(('L',l,[T(x+r*math.cos(math.radians(a0+(a1-a0)*i/n)),y+r*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]))
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
                # p' = Minsert * (R*S*(p-base)) + (x,y)
                a,b_,c_,d=c*sx,s*sx,-s*sy,c*sy
                nm_=(M[0]*a+M[2]*b_, M[1]*a+M[3]*b_, M[0]*c_+M[2]*d, M[1]*c_+M[3]*d)
                tx0,ty0=T(x,y); ox,oy=nm_[0]*(-bx)+nm_[2]*(-by),nm_[1]*(-bx)+nm_[3]*(-by)
                flatten(B,B[nm],l,(nm_[0],nm_[1],nm_[2],nm_[3],tx0+ox,ty0+oy),depth+1,out)
    return out
def find_box(B,prims):
    """sheet frame (closed 'batas' rectangle) holding the schema, minus the legend column"""
    title=None
    for k,l,v in prims:
        if k=='T' and re.search(r'SKEMA DAERAH IRIGASI',v[4],re.I) and not re.search(r'PETA',v[4],re.I): title=(v[0],v[1]); break
    if title is None:
        for k,l,v in prims:
            if k=='T' and re.search(r'SKEMA DAERAH',v[4],re.I): title=(v[0],v[1]); break
    if title is None: return None
    rects=[]
    for k,l,v in prims:
        if k=='L' and len(v)==5 and v[0]==v[4]:
            xs=[p[0] for p in v]; ys=[p[1] for p in v]; w,h=max(xs)-min(xs),max(ys)-min(ys)
            if 250<w<900 and 200<h<500 and min(xs)<=title[0]<=max(xs) and min(ys)<=title[1]<=max(ys): rects.append((w*h,min(xs),min(ys),max(xs),max(ys)))
    if not rects: return None
    _,x0,y0,x1,y1=min(rects); w=x1-x0; hgt=y1-y0; cand=[]
    for k,l,v in prims:
        if k=='L' and len(v)==2 and abs(v[0][0]-v[1][0])<0.5 and abs(v[0][1]-v[1][1])>0.9*hgt*0.8 and x0+0.55*w<v[0][0]<x1-0.03*w and min(v[0][1],v[1][1])<y0+0.1*hgt: cand.append(v[0][0])
    xd=min(cand) if cand else x1
    return (x0,y0,xd,y1,title,(x0,y0,x1,y1))
def skema(path):
    B=dxf2.parse(path); ent=B.get('*ENTITIES',[]); prims=flatten(B,ent)
    bx=find_box(B,prims)
    if not bx: return None
    x0,y0,x1,y1=bx[:4]; e=0.6
    def inside(x,y): return x0-e<=x<=x1+e and y0-e<=y<=y1+e
    R=lambda v: round(v,1)
    paths={}; C=[]; T=[]
    for k,l,v in prims:
        c=cat(l)
        if k=='L':
            pts=v
            if all(abs(p[0]-x0)<e or abs(p[0]-x1)<e or abs(p[1]-y0)<e or abs(p[1]-y1)<e for p in pts): continue   # garis bingkai
            if not any(inside(*p) for p in pts): continue
            paths.setdefault(c,[]).append('M'+'L'.join(f'{R(p[0]-x0)} {R(y1-p[1])}' for p in pts))
        elif k=='C':
            if inside(v[0],v[1]) and v[2]<80: C.append([R(v[0]-x0),R(y1-v[1]),R(v[2]),c])
        elif k=='T':
            if inside(v[0],v[1]): T.append([R(v[0]-x0),R(y1-v[1]),R(v[2]),round(v[3]),v[4],v[5],c])
    return dict(w=R(x1-x0),h=R(y1-y0),P={k:' '.join(v) for k,v in paths.items()},C=C,T=T)
