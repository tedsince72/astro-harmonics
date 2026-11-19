"""Of Corse I Can natal-to-natal (19 Nov 2026, Eddie; read-only). F1 same natal pair >= 90 (number family) in both charts; F2 two such pairs;
F3 a number held by natal pairs >= 90 in both charts with a sky pair >= 50 on it. Usage: RACE=<race> python3 tools/scans/bb_scan_ofcorse_natal.py
(one race) or no RACE (all result races)."""
import sys; sys.argv=['x']; sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans')
import bb_scan_natal_angle as A, eddie_bybody as B, bb_scan_negatives as NG, openpyxl, os
from bb_scan_natal_pairs import nums, P, NAT
from bb_scan_uranus_pairs import dist
def runner_sets(r, bykey):
    S={}
    for ch in 'HJ':
        if not r['pos'].get(ch): continue
        for X,Y in A.pairs(NAT+B.ROYAL):
            for pl in ('RA','Dec'):
                a,b=P(r['pos'][ch],r['ra'][ch],X,pl),P(r['pos'][ch],r['ra'][ch],Y,pl)
                if a is None or b is None: continue
                v=dist(a,b,pl); h=nums(v,pl)
                if h and h[0][2]>=90: S.setdefault(ch,[]).append((frozenset((X,Y)),pl,h[0][0],h[0][1],v))
    H,J=S.get('H',[]),S.get('J',[])
    both=sorted({tuple(sorted(p)) for p,*_ in H} & {tuple(sorted(p)) for p,*_ in J})
    tg={(f,t) for _,_,f,t,_ in H} & {(f,t) for _,_,f,t,_ in J}
    carried=[k for k in tg if bykey.get(k)]
    return both, carried
def race(rc):
    path=f'reference/classic/race_batch_{rc}_active.xlsx'
    if not os.path.exists(path): return None
    runners,tt,tp=B.load(path); tr=B.ra_positions(openpyxl.load_workbook(path,read_only=True)['TRANS_POS'])
    sky=A.sky_lines(tp,tr); bykey={}
    for p,pl,v,s,h in sky:
        for f,t,sc in h:
            if sc>=50: bykey.setdefault((f,t),[]).append(p)
    return [(r['name'].get('H'),)+runner_sets(r,bykey) for cl,r in sorted(runners.items())]
if '--race' in sys.argv[0:] or len(sys.argv)>1: pass
import json
if __name__=='__main__':
    rc=os.environ.get('RACE')
    if rc:
        for n,b,c in race(rc): print(n,'| same pair both charts:',b,'| number both charts with sky pair:',c)
        sys.exit()
    K={'F1 same pair both':lambda b,c:len(b)>=1,'F2 two pairs both':lambda b,c:len(b)>=2,'F3 number both + sky':lambda b,c:len(c)>=1,'F1+F3':lambda b,c:len(b)>=1 and len(c)>=1,'F2+F3':lambda b,c:len(b)>=2 and len(c)>=1}
    T={k:[0,0,0.0,[]] for k in K}; nr=0
    for rc,win in NG.RACES:
        rows=race(rc)
        if not rows: continue
        nr+=1;n=len(rows)
        for name,b,c in rows:
            w=bool(name and win in name)
            for k,f in K.items():
                if f(b,c): T[k][0]+=1;T[k][1]+=w;T[k][2]+=1/n; w and T[k][3].append(win)
    print(nr)
    for k,v in T.items(): print(k,v[0],v[1],round(v[2],1),v[3])
