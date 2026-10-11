# Whole numbers (±0.005), ninths (±0.0005) and RA+Dec together from one of Eddie's race_batch workbooks (TRANS + Pxx tabs, single moment).
import sys,openpyxl,itertools
F=sys.argv[1]; wb=openpyxl.load_workbook(F,data_only=True)
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto','Moon']
def load(ws,natal):
    P={}; 
    for r in list(ws.iter_rows(values_only=True))[1:]:
        b=r[1]
        if b in BOD and not (natal and b=='Moon'): P[b]=(float(r[4]),float(r[8]))
        elif isinstance(b,str) and b.endswith('_B'): P[b[:-2]+'*']=(float(r[4]),float(r[8]))
    return P
star=lambda b:b.endswith('*')
def on(v,fam):
    if fam=='whole': k=round(v); return (abs(v-k)<=0.005 and k>0), str(k), abs(v-k)
    q=round(v*9); return (abs(v-q/9)<=0.0005 and q%9!=0), f'{q}/9', abs(v-q/9)
def scan(P,Q,same):
    hits=[]; tog=[]
    it=itertools.combinations(sorted(P),2) if same else itertools.product(sorted(P),sorted(Q))
    for a,b in it:
        A=P[a]; B=(P if same else Q)[b]
        if (star(a) and star(b)) or {a,b}=={'Rahu','Ketu'}: continue
        ra=abs((A[0]-B[0]+180)%360-180); de=abs(A[1]-B[1]); got={}
        for mm,v in (('RA',ra),('Dec',de)):
            for fam in ('whole','ninths'):
                ok,lab,e=on(v,fam)
                if ok: hits.append((fam,e,mm,a,b,lab,v)); got[mm]=(lab,e)
        if len(got)==2: tog.append((a,b,got['RA'],got['Dec']))
    if same:
        for a in P:
            if a!='Ketu':
                for fam in ('whole','ninths'):
                    ok,lab,e=on(abs(P[a][1]),fam)
                    if ok: hits.append((fam,e,'Dec',a,'Equator',lab,abs(P[a][1])))
    return hits,tog
def show(t,res):
    hits,tog=res
    for fam in ('whole','ninths'):
        L=sorted(x for x in hits if x[0]==fam); print(f"\n== {t} — {fam}: {len(L)}")
        for x in L: print(f"   {x[1]:.5f} {x[2]:3s} {x[3]}–{x[4]:13s} = {x[5]:>7s}  ({x[6]:.5f}){'  MOON' if 'Moon' in x[3:5] else ''}")
    print(f"-- {t} — RA and Dec together: {len(tog)}")
    for a,b,r,d in tog: print(f"   {a}–{b}: RA {r[0]} (±{r[1]:.5f})  Dec {d[0]} (±{d[1]:.5f}){'  MOON' if 'Moon' in (a,b) else ''}")
SKY=load(wb['TRANS'],False)
print(F.split('/')[-1],"  stars marked * ; star–star and Rahu–Ketu out; natal Moon out; whole ±0.005, ninths ±0.0005; sky at the workbook time")
show('TT sky',scan(SKY,None,True))
for t in wb.sheetnames[1:]:
    ws=wb[t]; nm=ws.cell(2,1).value; N=load(ws,True)
    show(f'NN {nm}',scan(N,None,True)); show(f'TN sky → {nm}',scan(SKY,N,False))
