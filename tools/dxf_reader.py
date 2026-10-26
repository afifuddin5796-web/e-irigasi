"""Pembaca DXF ASCII sederhana (cukup untuk gambar skema irigasi)."""
import re
BASES={}
def parse(path):
    BASES.clear()
    """Return blocks: name -> list of entities (type, layer, dict code->list of str)."""
    with open(path,'r',errors='ignore') as f: L=f.read().split('\n')
    n=len(L); i=0; sec=None; blocks={}; cur_blk=None; ent=None; hdr=None
    while i<n-1:
        c=L[i].strip()
        if not c.lstrip('-').isdigit(): i+=1; continue   # resync
        v=L[i+1].strip(); i+=2
        if c=='0':
            if ent is not None and cur_blk is not None: blocks[cur_blk].append(ent)
            ent=None
            if v=='SECTION': pass
            elif v=='ENDSEC': sec=None; cur_blk=None
            elif v=='BLOCK': ent=None; cur_blk='?'; pend=True
            elif v=='ENDBLK': cur_blk=None
            elif sec in('BLOCKS','ENTITIES'):
                ent={'t':v,'p':{}}
                if cur_blk is None and sec=='ENTITIES': cur_blk='*ENTITIES'; blocks.setdefault(cur_blk,[])
        elif c=='2' and sec is None and v in('HEADER','CLASSES','TABLES','BLOCKS','ENTITIES','OBJECTS'): sec=v
        elif sec=='BLOCKS' and cur_blk=='?' and c=='2': cur_blk=v; blocks.setdefault(v,[])
        elif ent is None and cur_blk not in(None,'?') and c in('10','20'):
            try: BASES.setdefault(cur_blk,{})[c]=float(v)
            except: pass
        elif ent is not None: ent['p'].setdefault(c,[]).append(v)
    if ent is not None and cur_blk is not None: blocks[cur_blk].append(ent)
    return blocks
