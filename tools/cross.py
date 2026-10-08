"""cross.py RACE TAB_A TAB_B : direct links between two natal charts at 12:00 — Dec parallels/contraparallels (<=0.1) and clean numbers (RA, Dec, Flat, Sky) between every body of A and every body of B (±0.002)."""
import csv, math, sys
R, A, B = sys.argv[1], sys.argv[2], sys.argv[3]
stars={'Polaris','Alkaid','Capella','Algol','Vega','Castor','Alphecca','Pleiades','Arcturus','Aldebaran','Regulus','Altair','Betelgeuse','Bellatrix','Procyon','Rigel','Spica','Deneb Algedi','Algorab','Sirius','Antares','Fomalhaut','equator','Ascendant','Midheaven','Vertex','Part_of_Fortune','Part_of_Spirit'}
SLOW={'Saturn','Uranus','Neptune','Pluto','Chiron','Eris','Sedna','Haumea','Makemake','Quaoar','Orcus','Gonggong','Transpluto','Rahu','Ketu','Jupiter'}
P={}
for r in csv.DictReader(open(f'/home/claude/ledger/allpos/{R}__NATAL_HOURLY.csv')):
    b=r['body'].replace('_B','')
    if r['hour']=='12' and r['dec'] and b not in stars and b!='Moon' and r['tab'] in (A,B): P.setdefault(r['tab'],{})[b]=(float(r['ra']),float(r['dec']))   # natal Moon left out (8 Oct)
phi=(1+5**.5)/2
def ra(x,y): d=abs(x-y)%360; return min(d,360-d)
def sky(p,q):
    r1,d1,r2,d2=map(math.radians,(p[0],p[1],q[0],q[1])); return math.degrees(math.acos(max(-1,min(1,math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(r1-r2)))))
def num(x,t=0.002):
    o=[]
    if x<0.05: return o
    if abs(x-round(x))<=t and round(x)>0: o.append(f"whole {round(x)}")
    k=round(x/phi)
    if k>0 and abs(x-k*phi)<=t: o.append(f"{k}φ")
    k=round(x/2**.5)
    if k>0 and abs(x-k*2**.5)<=t: o.append(f"{k}√2")
    for e in range(2,12):
        if abs(x-phi**e)<=t: o.append(f"φ^{e}")
    if not o and abs(x*9-round(x*9))<=t*9: o.append(f"{round(x*9)}/9")
    return o
par=[];nums=[];cnt={'pw':0,'n9':0,'vals':0}
for a,pa in P[A].items():
    for b,pb in P[B].items():
        dd=pa[1]-pb[1]; cd=pa[1]+pb[1]
        if abs(dd)<=0.1: par.append(f"PARALLEL       {A} {a:11s} {pa[1]:+8.3f}  {B} {b:11s} {pb[1]:+8.3f}  diff {abs(dd):.3f}")
        if abs(cd)<=0.1: par.append(f"CONTRAPARALLEL {A} {a:11s} {pa[1]:+8.3f}  {B} {b:11s} {pb[1]:+8.3f}  diff {abs(cd):.3f}")
        v={'RA':ra(pa[0],pb[0]),'Dec':abs(dd),'Flat':math.hypot(ra(pa[0],pb[0]),dd),'Sky':sky(pa,pb)}
        for k,x in v.items():
            cnt['vals']+=1; n=num(x)
            if n:
                if '/9' in n[0]: cnt['n9']+=1
                else: cnt['pw']+=1
                slow='slow–slow' if a in SLOW and b in SLOW else ('one fast' if (a in SLOW or b in SLOW) else 'both fast')
                nums.append((0 if '/9' not in n[0] else 1, slow, f"{A} {a:11s} – {B} {b:11s} {k:4s} {x:9.4f} = {', '.join(n):14s} [{slow}]"))
print(f"{len(P[A])} × {len(P[B])} bodies; {cnt['vals']} values; hits: φ/√2/whole/φⁿ {cnt['pw']} (chance ≈ {cnt['vals']*0.0093:.0f}), ninths {cnt['n9']} (chance ≈ {cnt['vals']*0.032:.0f})")
print('\n'.join(par) or 'no parallels')
for g in ('slow–slow','one fast','both fast'):
    print(f"--- {g}")
    for t,s,l in sorted(nums):
        if s==g: print('  '+l)
