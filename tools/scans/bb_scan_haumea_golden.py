"""Read-only (19 Nov 2026, after Newmarket 14:13 29 Oct 2022; chosen after the result): every result race with a golden sky line >= 90 on Haumea, its sky race score and whether the cover of eight hit."""
import sys,os
sys.argv=sys.argv[:1]; sys.path.insert(0,'tools'); sys.path.insert(0,'tools/scans')
import bb_sky_angles_races as A, bb_scan_negatives as NG, bb_cover8_where as W, bb_sky_race_score as S
from bb_cover8 import C
for r,win in NG.RACES:
    if not os.path.exists(f'reference/classic/race_batch_{r}_active.xlsx'): continue
    L=[x for x in A.lines(r) if x[3]=='golden' and x[5]>=90 and 'Haumea' in x[:2]]
    if not L: continue
    runners,hh=W.holders(r); w=next((x for x in runners if win in x),None)
    hit=w and any(set(c)<=hh.get(w,set()) for c in C)
    print(r,'ORIG' if r in A.ORIG else '', 'score %+d'%S.score(r)[0],'cover HIT' if hit else 'miss', win,'|',['S %s – S %s %s %s (%.0f)'%(x[0],x[1],x[2],x[4],x[5]) for x in L])
