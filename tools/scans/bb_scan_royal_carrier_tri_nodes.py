"""List the holders of the royal carrier triangle on the jockey chart with a node (Rahu / Ketu) as the sky carrier (read-only;
20 Nov 2026, from Ezenli / Hollie Doyle). python3 tools/scans/bb_scan_royal_carrier_tri_nodes.py"""
import sys,os; sys.argv=['x']; sys.path[:0]=['tools','tools/scans']
import bb_scan_royal_carrier_tri as S
for race,win in S.NG.RACES:
    p=f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(p): continue
    runners,tt,tp=S.EB.load(p)
    for r in runners.values():
        for (ch,R,X),ys in S.shapes(r,tt).items():
            yy=[y for y in ys if y[0] in ('Rahu','Ketu')]
            if ch=='J' and yy:
                won=S.RA.key(r['name']['H'])==S.RA.key(win)
                print(race, r['name']['H'], '/', S.jname(r), f'J {R} - J {X}', [(y[0],y[1],y[2],y[3]) for y in yy], 'WON' if won else '')
