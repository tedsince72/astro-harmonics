import sys, openpyxl, itertools
sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans'); sys.argv=sys.argv[:1]
import eddie_bybody as B
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT
race='20210802_newcastle_aw_1633'; path=f'reference/classic/race_batch_{race}_active.xlsx'
runners,tt,tp=B.load(path)
T={'12.2222','33.3333','7','155.556','18','141.4','16×φ','9×φ'}
for cl,r in sorted(runners.items()):
    out=[]
    for ch in 'HJ':
        pos,ra=r['pos'][ch],r['ra'][ch]
        for X,Y in itertools.combinations(list(NAT)+list(B.ROYAL),2):
            if {X,Y}=={'Rahu','Ketu'}: continue
            for pl in ('RA','Dec'):
                A,Bv=P(pos,ra,X,pl),P(pos,ra,Y,pl)
                if A is None or Bv is None: continue
                v=dist(A,Bv,pl); h=nums(v,pl)
                if h and h[0][2]>=80 and str(h[0][1]) in T: out.append(f'{ch} {X}–{Y} {pl} {v:.4f} {h[0][1]} ({h[0][2]:.1f})')
    print(r['name']['H'],len(out)); [print('   ',o) for o in out]
