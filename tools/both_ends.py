# both_ends.py (11 Oct 2026, reading aid) DIR : natal links (same chart, or horse–jockey cross) with one sky moving body at whole/ninth to BOTH ends
import sys,glob,openpyxl,itertools
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
rd=lambda a,b:abs((a[0]-b[0]+180)%360-180); dd=lambda a,b:abs(a[1]-b[1])
def on(v):
    w=round(v); q=round(v*9)
    if abs(v-w)<=0.005 and w>0: return f"{w}"
    if abs(v-q/9)<=0.0005 and q%9: return f"{q}/9"
def hits(s,p,node):
    out=[]
    for pl,v in (('RA',rd(s,p)),('Dec',dd(s,p))):
        if pl=='RA' and node: v=min(v,180-v)
        if v>=0.5 and on(v): out.append(f"{pl} {on(v)}")
    return out
for f in sorted(glob.glob(sys.argv[1]+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,read_only=True,data_only=True)
    L={t:{r[1]:(float(r[4]),float(r[8])) for r in wb[t].iter_rows(min_row=2,values_only=True) if r[1] in BOD and isinstance(r[4],(int,float))} for t in ('TRANS','P01','P02')}
    pts=[('H',b,L['P01'][b]) for b in BOD]+[('J',b,L['P02'][b]) for b in BOD]
    res=[]
    for (c1,b1,p1),(c2,b2,p2) in itertools.combinations(pts,2):
        if (c1,b1)==(c2,b2): continue
        r,d=rd(p1,p2),dd(p1,p2)
        linked = r<1.5 or d<0.6 or (c1==c2 and (on(r) or on(d)))
        if not linked: continue
        for s in BOD:
            nd=s=='Rahu'
            h1=hits(L['TRANS'][s],p1,nd or b1=='Rahu'); h2=hits(L['TRANS'][s],p2,nd or b2=='Rahu')
            if h1 and h2: res.append(f"{c1} {b1}–{c2} {b2} (RA {r:.3f} Dec {d:.3f}) <- sky {s}: {','.join(h1)} | {','.join(h2)}")
    print(f"{wb['P01'].cell(2,1).value} / {wb['P02'].cell(2,1).value}: {len(res)}")
    for x in res: print('    '+x)
