# Whole-number RA and Dec distances (and Dec from the Equator), ±TOL: TT (race sky), NN (natal chart), TN (sky -> natal), for chosen tabs.
import sys,csv,collections,itertools,numpy as np
exec(open('/home/claude/lattice/families.py').read().split("N = sorted(S)")[0].split("S = {}")[0]); STARSET=set(STARS)
REPO='/home/claude/astro-harmonics'; R,OFF,DUR,TOL=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4]); TABS=sys.argv[5].split(',')
import os; FAM=os.environ.get('WN_FAM','whole')   # 'whole' or 'ninths' (k/9, k not a multiple of 9)
SKIP={'Ascendant','Midheaven','Vertex','Part_of_Fortune','Part_of_Spirit','equator','body'}
sched=int(R[-4:-2])*60+int(R[-2:]); h,m,s=map(int,OFF.split(':')); t0=h*60+m+s/60; t1=t0+DUR/60
M=collections.defaultdict(dict)
for r in csv.DictReader(open(f'{REPO}/data/sky/{R}__SKYM.csv')):
    if r['body'] not in SKIP: M[r['body']][sched+int(r['minute'])]=(float(r['ra']),float(r['dec']))
TS=np.arange(t0,t1+1e-9,2/60)
def ser(b): ks=sorted(M[b]); return np.interp(TS,ks,np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))))%360, np.interp(TS,ks,[M[b][k][1] for k in ks])
SKY={b:ser(b) for b in M}
def hm(t): x=int(round(t*60)); return f"{x//3600}:{(x//60)%60:02d}:{x%60:02d}"
def check(v,a,b,mm,out):
    v=np.atleast_1d(v)
    if v.max()<0.5: return
    if FAM == 'ninths': ks = [(q / 9, f'{q}/9') for q in range(max(1, int(v.min() * 9) - 1), int(v.max() * 9) + 2) if q % 9]
    else: ks = [(float(q), str(q)) for q in range(max(1, int(v.min()) - 1), int(v.max()) + 2)]
    for k, lab in ks:
        e=np.abs(v-k); i=int(e.argmin())
        if e[i]<=TOL:
            st='fixed' if len(v)==1 else ('X' if np.sign(v[0]-k)!=np.sign(v[-1]-k) else 'held')
            out.append((float(e[i]),mm,a,b,lab,float(v[i]),hm(TS[i]) if len(v)>1 else '',st))
def pairs(P,Q,same):
    out=[]
    it=itertools.combinations(sorted(P),2) if same else itertools.product(sorted(P),sorted(Q))
    for a,b in it:
        A=P[a]; B=(P if same else Q)[b]
        if a in STARSET and b in STARSET: continue
        if {a,b}=={'Rahu','Ketu'}: continue
        check(np.abs((A[0]-B[0]+180)%360-180),a,b,'RA',out); check(np.abs(A[1]-B[1]),a,b,'Dec',out)
    if same:
        for a in P:
            if a != 'Ketu': check(np.abs(P[a][1]),a,'Equator','Dec',out)   # Rahu kept (checker 11 Oct); Ketu = same value
    return out
def show(title,out):
    print(f"\n== {title}: {len(out)} {FAM} hits ≤{TOL}")
    for o in sorted(out): print(f"   {o[0]:.5f}  {o[1]:3s} {o[2]}–{o[3]:12s} = {o[4]:>6s}   {o[5]:.5f} {o[6]} {o[7]}{'  MOON' if 'Moon' in (o[2],o[3]) else ''}")
print(f"{R}  race {hm(t0)}–{hm(t1)}  {FAM}, RA = |dRA| wrapped, Dec = |dDec|; star–star and Rahu–Ketu left out; natal Moon left out")
show('TT race sky',pairs(SKY,None,True))
meta=list(csv.reader(open(f'{REPO}/data/allpos/{R}__META.csv'))); hdr=next(i for i,r in enumerate(meta) if r[:3]==['tab','role','cloth'])
name={r[0]:r[3] for r in meta[hdr+1:] if r and r[0].startswith('P')}
for tab in TABS:
    N={q['body']:(np.float64(q['ra']),np.float64(q['dec'])) for q in csv.DictReader(open(f"{REPO}/data/allpos/{R}__{tab}_POS.csv")) if q['ra'] and q['body'] not in SKIP and q['body']!='Moon'}
    show(f'NN {name[tab]} natal (12:00)',pairs(N,None,True))
    show(f'TN sky → {name[tab]} natal',pairs(SKY,N,False))
