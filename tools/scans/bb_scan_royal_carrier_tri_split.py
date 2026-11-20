import sys,os,io,contextlib; sys.argv=['x']; sys.path[:0]=['tools','tools/scans']
import bb_scan_royal_carrier_tri as S
EB,NG,RA,F=S.EB,S.NG,S.RA,S.F
from collections import defaultdict
tests={'all':lambda k,ys:True,'jockey chart':lambda k,ys:k[0]=='J','horse chart':lambda k,ys:k[0]=='H',
 'Y a node':lambda k,ys:any(y[0] in('Rahu','Ketu') for y in ys),'R Antares':lambda k,ys:k[1]=='Antares',
 'R Regulus':lambda k,ys:k[1]=='Regulus','R Aldebaran':lambda k,ys:k[1]=='Aldebaran','R Fomalhaut':lambda k,ys:k[1]=='Fomalhaut',
 'X Orcus':lambda k,ys:k[2]=='Orcus','jockey + node':lambda k,ys:k[0]=='J' and any(y[0] in('Rahu','Ketu') for y in ys),
 'two Ys (conj pair)':lambda k,ys:len(ys)>=2,'2+ shapes on runner':None}
T={k:[0,0,0.0] for k in tests}
for race,win in NG.RACES:
    p=f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(p): continue
    runners,tt,tp=EB.load(p); n=len(runners)
    sh={RA.key(r['name'].get('H') or ''):S.shapes(r,tt) for r in runners.values()}
    for t,f in tests.items():
        if f is None: hold={x for x,s in sh.items() if len(s)>=2}
        else: hold={x for x,s in sh.items() if any(f(k,ys) for k,ys in s.items())}
        T[t][0]+=len(hold); T[t][1]+=RA.key(win) in hold; T[t][2]+=len(hold)/n
for t,v in T.items(): print(f'{t}: {v[0]} holders, {v[1]} won, {v[2]:.1f} by chance')
