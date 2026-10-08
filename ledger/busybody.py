#!/usr/bin/env python3
"""busybody.py v1.0 (3 Oct 2026) - who OWNS the sky's busiest body (Eddie 16:41-16:42, T41: "the busiest body at its
strongest in its own horse, and a body on both charts reached by the next-busiest body at race time"; run it "only
if it is a detailed result, not a general average").
For each race: the busiest body (Moon kept), the busiest without the Moon, and the next-busiest (Moon itself left out).
For each such body B and each runner (finish order, SP): the natal hub count of B in the horse and in the jockey
(natal-natal relationships at >= 50 / >= 70 / >= 90, any family, star-star and natal Moon left out - same count as
readrace NATAL HOTSPOTS), its rank in the field at >= 90 and >= 70 (1 = strongest; ties share), and what reaches
natal B at the race time: top-12 / busy landings on B, and sky bodies (not stars, not fast points) on B scoring
>= 90 between -2 and +15 min, with the score at the off and the minute of the peak (from SKYM).
* after a body = moves over the birth day (Sun/Mercury/Venus/Mars). No totals, no averages.
Usage: python3 busybody.py RACE [RACE ...]"""
import sys, csv, itertools
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, FAST, FASTNATAL, NODES, results, SKYD

def hubs(P):
    cnt = {b: [0, 0, 0] for b in P if b not in STARS and b != 'Moon'}
    for x, y in itertools.combinations(sorted(P), 2):
        if (x in STARS and y in STARS) or 'Moon' in (x, y): continue
        for m in ('RA', 'Dec'):
            if m == 'RA' and {x, y} == NODES: continue
            sc = max(FN[f](sep(P[x], P[y], m), m) for f in FAMS)
            for i, lv in enumerate((50, 70, 90)):
                if sc >= lv:
                    for b in (x, y):
                        if b in cnt: cnt[b][i] += 1
    return cnt

def rank(vals, v):
    return 1 + sum(1 for w in vals if w > v)

for R in sys.argv[1:]:
    rc = Race(R); rc.build(); res = results(R)
    M = {}
    for r in csv.DictReader(open(f'{SKYD}/{R}__SKYM.csv')):
        M.setdefault(r['body'], {})[int(r['minute'])] = (float(r['ra']), float(r['dec']))
    order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
    H = {(c, sd): hubs(rc.natal[tab]) for c in rc.charts for sd, tab in rc.charts[c].items()}
    nxt = sorted(set(rc.count.values()), reverse=True)
    second = [b for b, n in rc.count.items() if n == nxt[1]] if len(nxt) > 1 else []
    roles = {}
    for b in rc.busiest: roles.setdefault(b, []).append(f'busiest {rc.count[b]}')
    for b in rc.busiest_nm: roles.setdefault(b, []).append(f'busiest w/o Moon {rc.count_nm[b]}')
    for b in second: roles.setdefault(b, []).append(f'next {rc.count[b]}')
    roles.pop('Moon', None)
    print(f"\n######## {R}   field {len(rc.charts)}   " + ' | '.join(f"{b}: {', '.join(v)}" for b, v in roles.items()))
    for B, why in roles.items():
        if B in STARS:
            print(f"  {B} ({', '.join(why)}) – a fixed star: the same natal place for everyone; hub counts below still differ by runner")
        print(f"\n  == {B}{'*' if B in FASTNATAL else ''}  ({', '.join(why)})")
        for sd in ('H', 'J'):
            pass
        v90 = [H[k][B][2] for k in H if B in H[k]]; v70 = [H[k][B][1] for k in H if B in H[k]]
        for c in order:
            line = f"    {res[c]['finish']:>3} {rc.names[c][0][:18]:18} {res[c]['sp']:>6}"
            for sd in ('H', 'J'):
                if B not in H[(c, sd)]:
                    line += f" | {sd} –"; continue
                a, b7, b9 = H[(c, sd)][B]
                line += f" | {sd} {a:>2}/{b7:>2}/{b9:>2} (r90 {rank(v90, b9)}, r70 {rank(v70, b7)})"
            print(line)
            for sd, tab in rc.charts[c].items():
                P = rc.natal[tab]
                if B not in P: continue
                lands = [f"#{rc.pairs[k]['rank']} {k[0]}/{k[1]}" for k, sides in rc.land[c].items() for s2, ls in sides.items()
                         if s2 == sd for ld in ls if ld['C'] == B]
                hits = []
                for s in M:
                    if s in STARS or s in FAST or s == 'equator': continue
                    for m in ('RA', 'Dec'):
                        v0 = sep(M[s][0], P[B], m); f = max(FAMS, key=lambda k: FN[k](v0, m))
                        sc = {t: FN[f](sep(M[s][t], P[B], m), m) for t in M[s]}
                        pk = max(range(-2, 16), key=lambda t: sc[t])
                        if sc[pk] >= 90:
                            hits.append((pk, f"{s} {m} {v0:.4f} {f[:6]} off {sc[0]:.1f} peak {sc[pk]:.1f}@{pk:+d}"))
                hits.sort()
                if lands or hits:
                    print(f"          {sd} {B}: " + (f"lands {', '.join(lands)}; " if lands else '') + '; '.join(h for _, h in hits))
