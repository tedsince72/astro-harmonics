import sys, openpyxl, itertools
ARGS=sys.argv[1:]
sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans'); sys.argv=sys.argv[:1]
import eddie_bybody as B
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT, SKYP
race=ARGS[0]; NC=float(ARGS[1]); SC=float(ARGS[2])
path=f'reference/classic/race_batch_{race}_active.xlsx'
runners,tt,tp=B.load(path); tr=B.ra_positions(openpyxl.load_workbook(path,read_only=True)['TRANS_POS'])
def sc(a,b,pl):
    if a is None or b is None: return None
    v=dist(a,b,pl); h=nums(v,pl); return (v,h[0]) if h else None
sky={}
for a,b in itertools.combinations(SKYP,2):
    if {a,b}=={'Rahu','Ketu'}: continue
    for pl in ('RA','Dec'):
        r=sc(P(tp,tr,a,pl),P(tp,tr,b,pl),pl)
        if r and r[1][2]>=SC: sky.setdefault(frozenset((a,b)),[]).append((pl,r))
for cl,r in sorted(runners.items()):
    nm=r['name'].get('H'); out=[]
    for ch in ('H','J'):
        pos,ra=r['pos'].get(ch,{}),r.get('ra',{}).get(ch,{}); E={}
        for X,Y in itertools.combinations(NAT,2):
            if {X,Y}=={'Rahu','Ketu'}: continue
            for pl in ('RA','Dec'):
                q=sc(P(pos,ra,X,pl),P(pos,ra,Y,pl),pl)
                if q and q[1][2]>=NC: E.setdefault(frozenset((X,Y)),[]).append((pl,q))
        ks=list(E)
        for e1,e2 in itertools.combinations(ks,2):
            if e1&e2: continue
            a,b=sorted(e1); c,d=sorted(e2)
            for (p,q),(s,t) in (((a,c),(b,d)),((a,d),(b,c))):
                if frozenset((p,q)) in sky and frozenset((s,t)) in sky:
                    f=lambda L:'; '.join(f'{pl} {x[0]:.4f} {x[1][1]} ({x[1][2]:.1f})' for pl,x in L)
                    out.append(f'{ch} {a}–{b} [{f(E[e1])}] + {ch} {c}–{d} [{f(E[e2])}] | S {p}–S {q} [{f(sky[frozenset((p,q))])}] + S {s}–S {t} [{f(sky[frozenset((s,t))])}]')
    print(nm,len(out)); [print('   ',o) for o in out]
