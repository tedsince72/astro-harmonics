# For a workbook race: (1) named pairs in sky / horse / jockey / sky->natal, RA and Dec, with ratios; (2) per point, values repeated across >=3 partners (±W)
import sys,openpyxl,math,itertools,collections
F=sys.argv[1]; W=float(sys.argv[2]) if len(sys.argv)>2 else 0.01; wb=openpyxl.load_workbook(F,data_only=True)
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(t):
    P={}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b=r[1]
        if b in BOD: P[b]=(float(r[4]),float(r[8]))
        elif isinstance(b,str) and b.endswith('_B'): P[b[:-2]+'*']=(float(r[4]),float(r[8]))
    return P
S,H,J=load('TRANS'),load('P01'),load('P02'); hn,jn=wb['P01'].cell(2,1).value,wb['P02'].cell(2,1).value
d=lambda A,B,mm: abs((A[0]-B[0]+180)%360-180) if mm=='RA' else abs(A[1]-B[1])
def lab(v):
    w=round(v); q=round(v*9); return f"{w}" if abs(v-w)<=abs(v-q/9) else f"{q}/9", min(abs(v-w),abs(v-q/9))
def frac(x):
    best=(9,'')
    for q in range(1,10):
        p=round(x*q)
        if p>=q:
            e=abs(x-p/q)/(p/q); g=math.gcd(p,q)
            if e<best[0]: best=(e,f'{p//g}/{q//g}' if q//g>1 else f'{p//g}')
    return best
print(f"== {F.split('/')[-1]}  horse {hn}, jockey {jn}")
for a,b in [x.split('/') for x in sys.argv[3].split(',')] if len(sys.argv)>3 else []:
    print(f"\n-- {a}–{b}")
    for mm in ('RA','Dec'):
        h,j,s=d(H[a],H[b],mm),d(J[a],J[b],mm),d(S[a],S[b],mm)
        rows=[('sky',s),(f'{hn}',h),(f'{jn}',j),(f'sky {a}→{hn} {b}',d(S[a],H[b],mm)),(f'sky {b}→{hn} {a}',d(S[b],H[a],mm)),(f'sky {a}→{jn} {b}',d(S[a],J[b],mm)),(f'sky {b}→{jn} {a}',d(S[b],J[a],mm))]
        print(f"   {mm}: "+'  |  '.join(f"{n} {v:.4f} (≈{lab(v)[0]} {lab(v)[1]:.4f})" for n,v in rows))
        print(f"        J:H {max(h,j)/min(h,j):.5f}≈{frac(max(h,j)/min(h,j))[1]} ({frac(max(h,j)/min(h,j))[0]*100:.3f}%)   S:H {max(s,h)/min(s,h):.5f}≈{frac(max(s,h)/min(s,h))[1]} ({frac(max(s,h)/min(s,h))[0]*100:.3f}%)")
# repeated values on one point
print(f"\n== one point, one value: >=3 different partners within ±{W} of each other (any list, RA or Dec), on the 9 scale (whole/ninth within {W})")
ctx=[('sky',S,S),(hn,H,H),(jn,J,J),(f'sky→{hn}',S,H),(f'{hn}←sky',H,S),(f'sky→{jn}',S,J),(f'{jn}←sky',J,S)]
star=lambda x:x.endswith('*')
res=[]
for P in sorted(set(S)|set(H)):
    vals=[]
    for name,A,B in ctx:
        if P not in A: continue
        for Q in B:
            if Q==P and A is B: continue
            if star(P) and star(Q): continue
            if {P,Q}=={'Rahu','Ketu'}: continue
            for mm in ('RA','Dec'):
                v=d(A[P],B[Q],mm)
                if v>=0.5: vals.append((v,Q,name,mm))
    vals.sort()
    for i in range(len(vals)):
        grp=[x for x in vals if abs(x[0]-vals[i][0])<=W]
        partners={x[1] for x in grp}
        if len(partners)>=3:
            l,e=lab(sum(x[0] for x in grp)/len(grp))
            if e<=W: res.append((len(partners),P,l,tuple(sorted(grp))))
seen=set(); out=[]
for n,P,l,g in sorted(res,key=lambda x:-x[0]):
    k=(P,l)
    if k in seen: continue
    seen.add(k); out.append((n,P,l,g))
for n,P,l,g in out[:25]:
    print(f"   {P:13s} ≈ {l:7s} {n} partners: "+'; '.join(f"{x[2]} {x[3]} {x[1]} {x[0]:.4f}" for x in g))
