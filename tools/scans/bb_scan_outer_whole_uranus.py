"""Slow outer sky bodies (Sedna, Neptune, Quaoar) on natal Uranus as whole numbers (18 Nov 2026, Eddie, after Newcastle AW 14:20 11 Dec 2021:
the favourite Coltrane, last at 6/4F, had S Sedna -> J Uranus RA 116 whole 72.7 and S Quaoar -> H Uranus Dec 23 whole 89.4). Read-only; over
bb_fieldcheck_outer_uranus.RACES with favourites from bb_favs_outer_uranus.FAV; chosen after the result."""
import sys; sys.path[:0]=['tools','tools/scans']
import eddie_bybody_rules as E, bb_fieldcheck_outer_uranus as O, bb_favs_outer_uranus as F
def ls(D,y): return O.lines(D,y) if 'Uranus' in D else []
for v in [('whole',80),('whole',50),('any',80)]:
    p=w=0;c=0.0;fh=0;fe=0.0;fw=0;rows=[]
    for race,win in O.RACES:
        R=E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx');N=len(R)
        fav=next((r for r in R if race in F.FAV and F.FAV[race] in r),None)
        for run,D in R.items():
            hit=[r for y in ('Sedna','Neptune','Quaoar') for r in ls(D,y) if r['sc']>=v[1] and (v[0]=='any' or r['fam']=='whole')]
            if not hit: continue
            p+=1;c+=1/N;won=win in run;w+=won
            if fav: fe+=1/N
            if run==fav: fh+=1; fw+=won
            if v==('whole',80): rows.append(f"  {race} {run}{' WON' if won else ''}{' FAV' if run==fav else ''}: "+'; '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})" for r in hit))
    print(f"{v}: {p} holders, {w} won ({c:.1f} by chance); favourites holding {fh} ({fe:.1f} expected if favourites were like any runner), of them won {fw}")
    print('\n'.join(rows))
