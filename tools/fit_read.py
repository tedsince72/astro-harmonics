# fit_read.py (11 Oct 2026, reading aid for the planned 2nd script) WB : labelled simple sky/natal ratios (p<=30,q<=9,<=TOL%), shared horse/jockey pairs (<=0.5%) with sky ratio, equator whole/ninth
import sys,openpyxl,math,itertools
W=sys.argv[1]; TOL=float(sys.argv[2]) if len(sys.argv)>2 else 0.005
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
wb=openpyxl.load_workbook(W,read_only=True,data_only=True)
L={t:{r[1]:(float(r[4]),float(r[8])) for r in wb[t].iter_rows(min_row=2,values_only=True) if r[1] in BOD and isinstance(r[4],(int,float))} for t in ('TRANS','P01','P02')}
def ms(a,b):
    dra=(a[0]-b[0]+180)%360-180; dd=a[1]-b[1]; r1,d1,r2,d2=map(math.radians,(a[0],a[1],b[0],b[1]))
    hv=math.sin((d2-d1)/2)**2+math.cos(d1)*math.cos(d2)*math.sin((r2-r1)/2)**2
    return {'RA':abs(dra),'Dec':abs(dd),'Flat':math.hypot(dra,dd),'Sky':math.degrees(2*math.asin(math.sqrt(hv)))}
def fr(x,pmax=30):
    best=(9,'')
    for q in range(1,10):
        p=round(x*q)
        if p>=q and p<=pmax:
            e=abs(x-p/q)/(p/q); g=math.gcd(p,q)
            if e<best[0]: best=(e,f"{p//g}/{q//g}" if q//g>1 else f"{p//g}")
    return best
def lab(v):
    w=round(v); q=round(v*9)
    if abs(v-w)<=0.005 and w: return f"{w}"
    if abs(v-q/9)<=0.0005 and q%9: return f"{q}/9"
    return ""
HN,JN=wb['P01'].cell(2,1).value,wb['P02'].cell(2,1).value
print(f"== {HN} / {JN}\n-- simple sky/natal ratios (p<=30, q<=9, <= {TOL}%, ratio != 1)")
for a,b in itertools.combinations(BOD,2):
    if {a,b}=={'Rahu','Ketu'}: continue
    S=ms(L['TRANS'][a],L['TRANS'][b])
    for t,c in (('P01','H'),('P02','J')):
        N=ms(L[t][a],L[t][b])
        for pl in ('RA','Dec','Flat','Sky'):
            s,n=S[pl],N[pl]
            if min(s,n)<0.5: continue
            e,f=fr(max(s,n)/min(s,n))
            if f and f!='1' and e*100<=TOL: print(f"   {c} {a}–{b} {pl:4s} sky {s:9.4f} natal {n:9.4f}  {'sky/natal' if s>n else 'natal/sky'} {f} ({e*100:.4f}%)")
print("-- shared pairs: horse and jockey natal values within 0.5% (>=1), with sky ratio")
for a,b in itertools.combinations(BOD,2):
    if {a,b}=={'Rahu','Ketu'}: continue
    S,H,J=ms(L['TRANS'][a],L['TRANS'][b]),ms(L['P01'][a],L['P01'][b]),ms(L['P02'][a],L['P02'][b])
    for pl in ('RA','Dec','Flat','Sky'):
        h,j,s=H[pl],J[pl],S[pl]
        if min(h,j)>=1 and abs(h-j)/min(h,j)<=0.005 and s>=0.5:
            eh,fh=fr(max(h,s)/min(h,s)); ej,fj=fr(max(j,s)/min(j,s))
            print(f"   {a}–{b} {pl:4s} H {h:9.4f} J {j:9.4f} ({abs(h-j)/min(h,j)*100:.3f}%)  sky {s:9.4f}  H~sky {fh} ({eh*100:.4f}%)  J~sky {fj} ({ej*100:.4f}%)")
print("-- Equator |Dec| whole/ninth")
for t,c in (('TRANS','S'),('P01','H'),('P02','J')):
    for b in BOD:
        if b=='Ketu': continue
        v=abs(L[t][b][1])
        if v>=0.5 and lab(v): print(f"   {c} {b} {v:.5f} = {lab(v)}")
