# movement.py (11 Oct 2026, reading aid) DIR [WIN]: sky body minus the same natal body (RA signed-wrapped, Dec, great circle), whole/ninth within WIN (default 0.01); and what that natal body sits on in the other chart
import sys,glob,openpyxl,math
WIN=float(sys.argv[2]) if len(sys.argv)>2 else 0.01
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
rd=lambda a,b:abs((a[0]-b[0]+180)%360-180); dd=lambda a,b:abs(a[1]-b[1])
def gc(a,b):
    r1,d1,r2,d2=map(math.radians,(a[0],a[1],b[0],b[1])); return math.degrees(math.acos(max(-1,min(1,math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(r1-r2)))))
def lab(v):
    w=round(v); q=round(v*9)
    if abs(v-w)<=WIN and w>0: return f"{w} (off {abs(v-w):.4f})"
    if abs(v-q/9)<=WIN/9 and q%9: return f"{q}/9 (off {abs(v-q/9):.4f})"
for f in sorted(glob.glob(sys.argv[1]+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,read_only=True,data_only=True)
    L={t:{r[1]:(float(r[4]),float(r[8])) for r in wb[t].iter_rows(min_row=2,values_only=True) if r[1] in BOD and isinstance(r[4],(int,float))} for t in ('TRANS','P01','P02')}
    print(f"== {wb['P01'].cell(2,1).value} / {wb['P02'].cell(2,1).value}")
    for c,t,o in (('H','P01','P02'),('J','P02','P01')):
        for b in BOD:
            s,n=L['TRANS'][b],L[t][b]
            for pl,v in (('RA',rd(s,n)),('Dec',dd(s,n)),('GC',gc(s,n))):
                if b=='Rahu' and pl=='RA': v=min(v,180-v)
                if v>=0.5 and lab(v):
                    on=[f"{'J' if c=='H' else 'H'} {x} RA {rd(n,L[o][x]):.3f}/Dec {dd(n,L[o][x]):.3f}" for x in BOD if rd(n,L[o][x])<1.5 or dd(n,L[o][x])<0.3]
                    print(f"   {c} {b:10s} moved {pl:3s} {v:9.4f} = {lab(v)}" + (f"   natal {b} sits on: {'; '.join(on)}" if on else ''))
