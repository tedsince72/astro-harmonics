# Same pair on the 9 scale in BOTH RA and Dec at once (in the race): whole ±0.005 or ninth ±0.0005. TT, NN and TN per chart. Moon pairs listed apart.
import sys,csv,collections,itertools,numpy as np
exec(open('/home/claude/lattice/families.py').read().split("N = sorted(S)")[0].split("S = {}")[0]); ST=set(STARS)
REPO='/home/claude/astro-harmonics'; R,OFF,DUR='20261010_southwell_aw_2000','20:00:13',187.83
SKIP={'Ascendant','Midheaven','Vertex','Part_of_Fortune','Part_of_Spirit','equator','body'}
sched=20*60; t0=20*60+13/60; t1=t0+DUR/60; TS=np.arange(t0,t1+1e-9,2/60)
M=collections.defaultdict(dict)
for r in csv.DictReader(open(f'{REPO}/data/sky/{R}__SKYM.csv')):
    if r['body'] not in SKIP: M[r['body']][sched+int(r['minute'])]=(float(r['ra']),float(r['dec']))
def ser(b): ks=sorted(M[b]); return np.interp(TS,ks,np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))))%360, np.interp(TS,ks,[M[b][k][1] for k in ks])
SKY={b:ser(b) for b in M}
def hit(v):
    """per sample: label if on whole (±0.005) or ninth (±0.0005) else None -> return best (err,label,idx-mask)"""
    v=np.atleast_1d(v); q=np.round(v*9); e9=np.abs(v-q/9); w=np.round(v); ew=np.abs(v-w)
    okw=ew<=0.005; ok9=(e9<=0.0005)&(q%9!=0)
    return okw|ok9, np.where(okw, w.astype(int).astype(str), np.char.add(q.astype(int).astype(str),'/9')), np.where(okw,ew,e9)
def scan(P,Q,same):
    out=[]
    it=itertools.combinations(sorted(P),2) if same else itertools.product(sorted(P),sorted(Q))
    for a,b in it:
        A=P[a]; B=(P if same else Q)[b]
        if (a in ST and b in ST) or {a,b}=={'Rahu','Ketu'}: continue
        ra=np.abs((np.asarray(A[0])-B[0]+180)%360-180); de=np.abs(np.asarray(A[1])-B[1])
        o1,l1,e1=hit(ra); o2,l2,e2=hit(de)
        both=np.broadcast_to(o1,TS.shape if np.ndim(ra) or np.ndim(de) else (1,)) & o2 if True else None
        both=np.atleast_1d(o1&o2)
        if both.any():
            i=int(np.argmax(both)); l1=np.atleast_1d(l1); l2=np.atleast_1d(l2); e1=np.atleast_1d(e1); e2=np.atleast_1d(e2)
            j=min(i,len(l1)-1); k=min(i,len(l2)-1)
            out.append((a,b,l1[j],float(e1[j]),l2[k],float(e2[k]),int(both.sum())))
    return out
def pr(t,L):
    L=[x for x in L if x[2]!='0' and x[4]!='0']
    nm=[x for x in L if 'Moon' not in x[:2]]; mo=[x for x in L if 'Moon' in x[:2]]
    print(f"  {t}: {len(nm)} (+{len(mo)} Moon)")
    for x in nm: print(f"     {x[0]}–{x[1]}: RA {x[2]} (±{x[3]:.5f})  Dec {x[4]} (±{x[5]:.5f})")
    for x in mo: print(f"     MOON {x[0]}–{x[1]}: RA {x[2]}  Dec {x[4]}")
pr('TT race sky',scan(SKY,None,True))
meta=list(csv.reader(open(f'{REPO}/data/allpos/{R}__META.csv'))); hdr=next(i for i,r in enumerate(meta) if r[:3]==['tab','role','cloth'])
for r in meta[hdr+1:]:
    if not r or not r[0].startswith('P'): continue
    N={q['body']:(float(q['ra']),float(q['dec'])) for q in csv.DictReader(open(f"{REPO}/data/allpos/{R}__{r[0]}_POS.csv")) if q['ra'] and q['body'] not in SKIP and q['body']!='Moon'}
    print(f"\n== {r[3]} ({r[1]})"); pr('NN natal',scan(N,None,True)); pr('TN sky→natal',scan(SKY,N,False))
