# two_wins.py WB1 WB2 TOL%: same pair (horse/jockey) in simple sky/natal ratio in both races (11 Oct 2026, reading aid)
import sys,openpyxl,math,itertools
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def ms(a,b):
    dra=(a[0]-b[0]+180)%360-180; dd=a[1]-b[1]; r1,d1,r2,d2=map(math.radians,(a[0],a[1],b[0],b[1]))
    hv=math.sin((d2-d1)/2)**2+math.cos(d1)*math.cos(d2)*math.sin((r2-r1)/2)**2
    return {'RA':abs(dra),'Dec':abs(dd),'Flat':math.hypot(dra,dd),'GC':math.degrees(2*math.asin(math.sqrt(hv)))}
def fr(x,pmax=30):
    best=(9,'')
    for q in range(1,10):
        p=round(x*q)
        if p>=q and p<=pmax:
            e=abs(x-p/q)/(p/q); g=math.gcd(p,q)
            if e<best[0]: best=(e,f"{p//g}/{q//g}" if q//g>1 else f"{p//g}")
    return best
def load(f):
    wb=openpyxl.load_workbook(f,read_only=True,data_only=True)
    return {t:{r[1]:(float(r[4]),float(r[8])) for r in wb[t].iter_rows(min_row=2,values_only=True) if r[1] in BOD and isinstance(r[4],(int,float))} for t in ('TRANS','P01','P02')}
A,B=load(sys.argv[1]),load(sys.argv[2]); TOL=float(sys.argv[3])/100
def hits(L):
    out={}
    for a,b in itertools.combinations(BOD,2):
        if {a,b}=={'Rahu','Ketu'}: continue
        S=ms(L['TRANS'][a],L['TRANS'][b])
        for t,c in (('P01','H'),('P02','J')):
            N=ms(L[t][a],L[t][b])
            for pl in S:
                s,n=S[pl],N[pl]
                if min(s,n)<0.5: continue
                e,f=fr(max(s,n)/min(s,n))
                if f and f!='1' and e<=TOL: out[(c,a,b,pl)]=(f,e,s,n)
    return out
ha,hb=hits(A),hits(B)
print(f"simple sky/natal ratios <= {TOL*100}%: race1 {len(ha)}, race2 {len(hb)}")
pairs_a={(c,a,b) for c,a,b,p in ha}; pairs_b={(c,a,b) for c,a,b,p in hb}
print("same natal pair lit in BOTH races (any plane):")
for k in sorted(pairs_a & pairs_b):
    print('  ',k,' | race1:',[(p,ha[k+(p,)][0],f"{ha[k+(p,)][1]*100:.4f}%") for p in ('RA','Dec','Flat','GC') if k+(p,) in ha],' | race2:',[(p,hb[k+(p,)][0],f"{hb[k+(p,)][1]*100:.4f}%") for p in ('RA','Dec','Flat','GC') if k+(p,) in hb])
import collections
for nm,h in (('race1',ha),('race2',hb)):
    c=collections.Counter()
    for (ch,a,b,p) in h: c[(ch,a)]+=1; c[(ch,b)]+=1
    print(nm,'bodies:',', '.join(f"{ch} {x} {n}" for (ch,x),n in c.most_common(8)))
