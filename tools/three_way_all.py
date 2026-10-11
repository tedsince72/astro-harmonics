# three_way_all.py (11 Oct 2026, reading aid) DIR [TOL%]: per runner, pairs (non-star) whose horse, jockey and sky distances are ALL in simple ratio (p/q, q<=9, p<=30; 1 allowed)
import sys,glob,openpyxl,math,itertools
TOL=float(sys.argv[2])/100 if len(sys.argv)>2 else 0.0005
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def ms(a,b):
    dra=(a[0]-b[0]+180)%360-180; dd=a[1]-b[1]; r1,d1,r2,d2=map(math.radians,(a[0],a[1],b[0],b[1]))
    hv=math.sin((d2-d1)/2)**2+math.cos(d1)*math.cos(d2)*math.sin((r2-r1)/2)**2
    return {'RA':abs(dra),'Dec':abs(dd),'Flat':math.hypot(dra,dd),'Sky':math.degrees(2*math.asin(math.sqrt(hv)))}
def fr(x):
    best=(9,'')
    for q in range(1,10):
        p=round(x*q)
        if p>=q and p<=30:
            e=abs(x-p/q)/(p/q); g=math.gcd(p,q)
            if e<best[0]: best=(e,f"{p//g}/{q//g}" if q//g>1 else f"{p//g}")
    return best
for f in sorted(glob.glob(sys.argv[1]+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,read_only=True,data_only=True)
    L={t:{r[1]:(float(r[4]),float(r[8])) for r in wb[t].iter_rows(min_row=2,values_only=True) if r[1] in BOD and isinstance(r[4],(int,float))} for t in ('TRANS','P01','P02')}
    res=[]
    for a,b in itertools.combinations(BOD,2):
        if {a,b}=={'Rahu','Ketu'}: continue
        M={t:ms(L[t][a],L[t][b]) for t in L}
        for pl in ('RA','Dec','Flat','Sky'):
            S,H,J=M['TRANS'][pl],M['P01'][pl],M['P02'][pl]
            if min(S,H,J)<0.5: continue
            rs=[fr(max(x,y)/min(x,y)) for x,y in ((H,J),(H,S),(J,S))]
            w=max(e for e,_ in rs)
            if w<=TOL: res.append((w,f"{a}–{b} {pl:4s} H {H:9.4f} J {J:9.4f} S {S:9.4f}   H:J {rs[0][1]}  H:S {rs[1][1]}  J:S {rs[2][1]}   worst {w*100:.4f}%"+('   <-- Neptune/node' if {'Neptune'}&{a,b} and {'Rahu','Ketu'}&{a,b} else '')))
    print(f"== {wb['P01'].cell(2,1).value} / {wb['P02'].cell(2,1).value}: {len(res)}")
    for w,s in sorted(res): print('   '+s)
