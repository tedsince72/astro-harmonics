import sys, glob, math, itertools, openpyxl
sys.argv=[sys.argv[0], sys.argv[1]]
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
gc=lambda a,b: math.degrees(math.acos(max(-1,min(1,math.sin(math.radians(a[1]))*math.sin(math.radians(b[1]))+math.cos(math.radians(a[1]))*math.cos(math.radians(b[1]))*math.cos(math.radians(a[0]-b[0]))))))
def on(v,w1=0.005,w9=0.0005):
    w=round(v); q=round(v*9)
    if abs(v-w)<=w1 and w>0: return f'{w}'
    if abs(v-q/9)<=w9 and q%9: return f'{q}/9'
def frac(x):
    best=(9,'')
    for q in range(1,10):
        p=round(x*q)
        if p>=q and p<=30:
            e=abs(x-p/q)/(p/q); g=math.gcd(p,q)
            if e<best[0]: best=(e,f'{p//g}/{q//g}' if q//g>1 else f'{p//g}')
    return best
def load(wb,t):
    P={}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        if r[1] in BOD and isinstance(r[4],(int,float)): P[r[1]]=(float(r[4]),float(r[8]))
    return P
for f in sorted(glob.glob(sys.argv[1]+'/*.xlsx')):
    wb=openpyxl.load_workbook(f,data_only=True); S,H,J=load(wb,'TRANS'),load(wb,'P01'),load(wb,'P02')
    nm=f"{wb['P01'].cell(2,1).value} / {wb['P02'].cell(2,1).value}"
    out=[]
    cl=[(x,y) for x in H for y in J if rd(H[x],J[y])<1.5 or dd(H[x],J[y])<0.3]
    # cross link struck by 2+ sky bodies (both ends)
    for x,y in cl:
        st=[]
        for s in S:
            if s in('Ketu',): continue
            a=[f'{pl}{on(v)}' for pl,v in(('RA',rd(S[s],H[x])),('Dec',dd(S[s],H[x])),('GC',gc(S[s],H[x]))) if v>=0.5 and on(v)]
            b=[f'{pl}{on(v)}' for pl,v in(('RA',rd(S[s],J[y])),('Dec',dd(S[s],J[y])),('GC',gc(S[s],J[y]))) if v>=0.5 and on(v)]
            if a and b: st.append(f'{s}[{",".join(a)}|{",".join(b)}]')
        if len(st)>=2: out.append(f'  XL2+ H {x}-J {y} (RA {rd(H[x],J[y]):.3f} Dec {dd(H[x],J[y]):.3f}): '+' '.join(st))
        # both ends moved
        mx=[f'{pl}{on(v,0.01,0.0011)}' for pl,v in(('RA',rd(S[x],H[x])),('Dec',dd(S[x],H[x])),('GC',gc(S[x],H[x]))) if v>=0.5 and on(v,0.01,0.0011)]
        my=[f'{pl}{on(v,0.01,0.0011)}' for pl,v in(('RA',rd(S[y],J[y])),('Dec',dd(S[y],J[y])),('GC',gc(S[y],J[y]))) if v>=0.5 and on(v,0.01,0.0011)]
        if mx and my: out.append(f'  BOTHMOVED H {x}{mx} - J {y}{my} (RA {rd(H[x],J[y]):.3f} Dec {dd(H[x],J[y]):.3f})')
    # swaps
    for x,y in itertools.combinations(BOD,2):
        if {x,y}=={'Rahu','Ketu'}: continue
        if (x,y) in cl and (y,x) in cl: out.append(f'  SWAP {x}<->{y}')
    # Chiron-Transpluto Dec
    for pl,f_ in(('RA',rd),('Dec',dd)):
        for c,N in(('H',H),('J',J)):
            sv,nv=f_(S['Chiron'],S['Transpluto']),f_(N['Chiron'],N['Transpluto'])
            if min(sv,nv)>=0.5:
                e,fr=frac(max(sv,nv)/min(sv,nv))
                if e<=0.00005: out.append(f'  CHI-TP {c} {pl} {fr} {e*100:.4f}%')
    # shared pair where sky equals one natal value (pair same value in three)
    for x,y in itertools.combinations(BOD,2):
        if {x,y}=={'Rahu','Ketu'}: continue
        for pl,f_ in(('RA',rd),('Dec',dd)):
            h,j,s=f_(H[x],H[y]),f_(J[x],J[y]),f_(S[x],S[y])
            if min(h,j,s)>=1 and max(h,j,s)/min(h,j,s)-1<=0.006: out.append(f'  SAME3 {x}-{y} {pl} H {h:.4f} J {j:.4f} S {s:.4f} spread {(max(h,j,s)/min(h,j,s)-1)*100:.3f}%')
    # Makemake-Haumea and Venus-Uranus cross links
    for a,b in (('Makemake','Haumea'),('Venus','Uranus'),('Uranus','Venus')):
        if (a,b) in cl: out.append(f'  XL {a}-{b} RA {rd(H[a],J[b]):.3f} Dec {dd(H[a],J[b]):.3f}')
    print(nm); print('\n'.join(out))
