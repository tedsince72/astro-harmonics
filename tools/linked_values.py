# Linked equalities in one workbook race: two different quantities with the same value (±TOL) that share a body.
# Quantities: pair distances RA/Dec (sky, horse, jockey, sky->horse, sky->jockey), same-body movement sky-natal RA/Dec (horse, jockey), |Dec| from equator.
import sys,openpyxl,itertools,collections,bisect
F=sys.argv[1]; TOL=float(sys.argv[2]); FOCUS=sys.argv[3].split(',') if len(sys.argv)>3 else []
wb=openpyxl.load_workbook(F,data_only=True)
BOD=['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(t):
    P={}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b=r[1]
        if b in BOD: P[b]=(float(r[4]),float(r[8]))
        elif isinstance(b,str) and b.endswith('_B'): P[b[:-2]+'*']=(float(r[4]),float(r[8]))
    return P
S,H,J=load('TRANS'),load('P01'),load('P02'); HN,JN=wb['P01'].cell(2,1).value,wb['P02'].cell(2,1).value
st=lambda x:x.endswith('*')
rd=lambda a,b:abs((a[0]-b[0]+180)%360-180); dd=lambda a,b:abs(a[1]-b[1])
Q=[]
def add(v,lab,bods):
    if v>=1: Q.append((v,lab,frozenset(b.rstrip('*') for b in bods)))
for tag,P in (('sky',S),(HN,H),(JN,J)):
    for b,x in P.items(): add(abs(x[1]),f'{tag} {b} Dec from Equator',[b])
    for a,b in itertools.combinations(P,2):
        if (st(a) and st(b)) or {a,b}=={'Rahu','Ketu'}: continue
        add(rd(P[a],P[b]),f'{tag} {a}–{b} RA',[a,b]); add(dd(P[a],P[b]),f'{tag} {a}–{b} Dec',[a,b])
for nm,N in ((HN,H),(JN,J)):
    for a in S:
        for b in N:
            if (st(a) and st(b)) or a==b: continue
            if {a,b}=={'Rahu','Ketu'}: continue
            add(rd(S[a],N[b]),f'sky {a} → {nm} {b} RA',[a,b]); add(dd(S[a],N[b]),f'sky {a} → {nm} {b} Dec',[a,b])
    for b in N:
        if st(b) or b not in S: continue
        add(rd(S[b],N[b]),f'{nm} {b} moved RA (natal→sky)',[b]); add(dd(S[b],N[b]),f'{nm} {b} moved Dec (natal→sky)',[b])
Q.sort(); vals=[q[0] for q in Q]
L=[]
for i,(v,l,bs) in enumerate(Q):
    j=i+1
    while j<len(Q) and Q[j][0]-v<=TOL:
        v2,l2,bs2=Q[j]
        if (bs & bs2) and bs!=bs2: L.append((v2-v,v,l,v2,l2,bs|bs2))
        j+=1
cnt=collections.Counter(b for x in L for b in x[5])
print(f"{F.split('/')[-1]}: {len(Q)} quantities, {len(L)} linked equalities (±{TOL}, share a body, not the same body set)")
print("bodies by number of linked equalities:",', '.join(f'{b} {n}' for b,n in cnt.most_common(12)))
for f in FOCUS:
    M=sorted(x for x in L if f in x[5])
    print(f"\n-- {f}: {len(M)}")
    for d,v,l,v2,l2,_ in M: print(f"   {d:.4f}  {v:9.4f} {l}   =   {v2:9.4f} {l2}")
# enrichment: links per body vs share of quantities that involve the body
nq=collections.Counter(b for q in Q for b in q[2])
tot_pairs=len(L)
print("\nenrichment (links involving body / expected from its share of quantities):")
E=[]
for b in nq:
    # expected: each link touches 2 quantities; P(link touches b) ≈ 1-(1-p)^2 with p = nq[b]/len(Q)
    p=nq[b]/len(Q); exp=tot_pairs*(1-(1-p)**2); E.append((cnt[b]/exp if exp else 0,b,cnt[b],exp))
for r,b,c,e in sorted(E,reverse=True)[:12]: print(f"   {b:13s} {c:3d} links, expected {e:5.1f}  ×{r:.2f}")
TRIO=set(FOCUS)
M=sorted(x for x in L if len(x[5]&TRIO)>=2)
print(f"\n-- links joining two or more of {sorted(TRIO)}: {len(M)}")
for d,v,l,v2,l2,_ in M: print(f"   {d:.4f}  {v:9.4f} {l}   =   {v2:9.4f} {l2}")
