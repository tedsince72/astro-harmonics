"""Eddie, 18 Nov 2026: sky - sky pairs scoring >= 80 (Moon out; conj incl.), kept only when both bodies appear in the
runner's natal-to-natal pairs >= 90 (same chart; royal stars incl.). Per chart: count, split into same pair (the sky pair is
itself a natal pair) and cross (the two bodies sit in different natal pairs). Usage: race [race ...] [--show]"""
import sys, itertools, openpyxl
sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans')
ARGS=sys.argv[1:]; sys.argv=sys.argv[:1]
import eddie_bybody as B
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT, SKYP
SHOW='--show' in ARGS; RACES=[a for a in ARGS if not a.startswith('--')]
ROY=set(B.ROYAL)
def score(v,pl):
    h=nums(v,pl); best=(h[0][1],h[0][2]) if h else None
    lim=1.5 if pl=='RA' else 0.3
    if v<lim:
        c=100*(lim-v)/lim
        if not best or c>best[1]: best=('conj',c)
    return best
def sky_pairs(tp,tr):
    out={}
    for a,b in itertools.combinations([x for x in SKYP if x!='Moon'],2):
        if {a,b}=={'Rahu','Ketu'} or (a in ROY and b in ROY): continue
        for pl in ('RA','Dec'):
            A,Bv=P(tp,tr,a,pl),P(tp,tr,b,pl)
            if A is None or Bv is None: continue
            v=dist(A,Bv,pl); s=score(v,pl)
            if s and s[1]>=80: out.setdefault(frozenset((a,b)),[]).append(f'{pl} {v:.4f} {s[0]} ({s[1]:.1f})')
    return out
def natal(pos,ra):
    pairs=set()
    for X,Y in itertools.combinations(NAT+B.ROYAL,2):
        if {X,Y}=={'Rahu','Ketu'} or (X in ROY and Y in ROY): continue
        for pl in ('RA','Dec'):
            A,Bv=P(pos,ra,X,pl),P(pos,ra,Y,pl)
            if A is None or Bv is None: continue
            h=nums(dist(A,Bv,pl),pl)
            if h and h[0][2]>=90: pairs.add(frozenset((X,Y)))
    return pairs
def race_rows(race):
    path=f'reference/classic/race_batch_{race}_active.xlsx'
    runners,tt,tp=B.load(path); tr=B.ra_positions(openpyxl.load_workbook(path,read_only=True)['TRANS_POS'])
    sky=sky_pairs(tp,tr); rows=[]
    for cl,r in sorted(runners.items()):
        res={}
        for ch in 'HJ':
            if not r['pos'].get(ch): res[ch]=([],[]); continue
            nat=natal(r['pos'][ch],r['ra'][ch]); bodies=set().union(*nat) if nat else set()
            same=[p for p in sky if p in nat]; cross=[p for p in sky if p<=bodies and p not in nat]
            res[ch]=(same,cross)
        rows.append((r['name'].get('H'),r['name'].get('J'),res,sky))
    return rows
if __name__=='__main__':
    for race in RACES:
        print('=====',race)
        for h,j,res,sky in race_rows(race):
            s=' | '.join(f'{ch}: same {len(res[ch][0])}, cross {len(res[ch][1])}' for ch in 'HJ')
            tot=sum(len(res[ch][0])+len(res[ch][1]) for ch in 'HJ')
            print(f'  {h} / {j} | {s} | total {tot}')
            if SHOW:
                for ch in 'HJ':
                    for kind,lst in (('same',res[ch][0]),('cross',res[ch][1])):
                        for p in lst: print(f'      {ch} {kind} S '+' – S '.join(sorted(p))+': '+'; '.join(sky[p]))
