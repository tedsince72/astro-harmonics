"""Natal pairs >= 90 of one runner with the sky lines on their numbers (19 Nov 2026, Eddie on Impatient, Ffos Las 15:37 8 Nov 2026; read-only, race and runner fixed in the file)."""
import sys, openpyxl
sys.argv=sys.argv[:1]; sys.path[:0]=['tools','tools/scans']
import eddie_bybody as B
import bb_scan_activation as A
from bb_scan_natal_pairs import nums, P, NAT
from bb_scan_uranus_pairs import dist
from bb_scan_natal_angle import pairs
A.CUT=40
rc='20261108_ffos_las_1537'; path=f'reference/classic/race_batch_{rc}_active.xlsx'
runners,tt,tp=B.load(path); tr=B.ra_positions(openpyxl.load_workbook(path,read_only=True)['TRANS_POS'])
skyn=A.sky_named(tp,tr)
# all sky pair lines on a target (any bodies)
skyall={}
for n,L in skyn.items():
    for f,t,pl,txt,moon,k in L: skyall.setdefault((f,t),set()).add(txt)
def nat(r):
    out=[]
    for c in 'HJ':
        for X,Y in pairs(NAT+B.ROYAL):
            for pl in ('RA','Dec'):
                a,b=P(r['pos'][c],r['ra'][c],X,pl),P(r['pos'][c],r['ra'][c],Y,pl)
                if a is None or b is None: continue
                v=dist(a,b,pl); h=nums(v,pl)
                if h and h[0][2]>=90: out.append((c,X,Y,pl,h[0][0],h[0][1],v,h[0][2]))
    return out
allp={cl:nat(r) for cl,r in runners.items()}
for cl,r in sorted(runners.items()):
    if 'Impatient' not in r['name'].get('H',''): continue
    for c,X,Y,pl,f,t,v,s in sorted(allp[cl],key=lambda x:-x[7]):
        others=[runners[o]['name']['H'] for o,L in allp.items() if o!=cl and any({x[1],x[2]}=={X,Y} and x[0]==c for x in L)]
        named=[x[3] for n in (X,Y) for x in skyn.get(n,[]) if x[0]==f and x[1]==t]
        sky=sorted(skyall.get((f,t),[]))
        print(f"{c} {X} – {Y} {pl} {v:.4f} {t} {f} ({s:.1f}) | same pair >=90 also: {others or '-'} | sky naming X/Y on it (>=40): {named or '-'} | any sky pair on {t}: {len(sky)} {sky[:3]}")
print()
for cl,L in sorted(allp.items()):
    alone=[x for x in L if not any(o!=cl and any({y[1],y[2]}=={x[1],x[2]} and y[0]==x[0] for y in M) for o,M in allp.items())]
    from collections import Counter
    cnt=Counter(n for x in L for n in (x[1],x[2]))
    print(runners[cl]['name']['H'],'pairs>=90',len(L),'held alone',len(alone),'top bodies',cnt.most_common(3))
