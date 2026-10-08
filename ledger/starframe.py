#!/usr/bin/env python3
"""starframe.py v1.0 (4 Oct 2026) - a TRANSIT body framed by TWO fixed stars in transit (Eddie 07:14 / 07:56: "how a
transit body relates to 2 fixed stars in transit - like a midpoint but maybe distances or ratios").
For each sky body X (not a star, not a fast point) and each pair of fixed stars A, B, in RA and in Dec, with X lying
BETWEEN A and B (d(X,A) + d(X,B) = d(A,B) within 0.01 deg): the ratio of the larger to the smaller distance is
compared with 1 (midpoint), phi, phi^2, sqrt2, 1+sqrt2, 2, 3 (tolerance 0.1% of the ratio; smaller distance >= 1 deg).
For each hit: the minute it is exact (-30..+30, one-minute grid; slow bodies barely move), and whether either distance
is itself a top-12 race number (within 0.005).
Then per runner: which framed bodies X reach that runner's natal bodies (certain bodies, >= 95 between -2 and +15 min),
with family, value and peak minute.
Usage: python3 starframe.py RACE"""
import sys, csv, itertools, math
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, FAST, FASTNATAL, results, SKYD
R = sys.argv[1]; rc = Race(R); rc.build(); res = results(R)
M = {}
for r in csv.DictReader(open(f'{SKYD}/{R}__SKYM.csv')):
    M.setdefault(r['body'], {})[int(r['minute'])] = (float(r['ra']), float(r['dec']))
PHI = (1 + 5 ** .5) / 2
TG = {'1:1 midpoint': 1.0, 'phi': PHI, 'phi^2': PHI ** 2, 'sqrt2': 2 ** .5, '1+sqrt2': 1 + 2 ** .5, '2': 2.0, '3': 3.0}
stars = sorted(b for b in M if b in STARS)
bodies = sorted(b for b in M if b not in STARS and b not in FAST and b != 'equator')
top = [(rc.pairs[k]['rank'], e[0], e[3]) for k in rc.byrank[:12] for e in rc.pairs[k]['entries']]
def ratio_at(X, A, B, m, t):
    d1 = sep(M[X][t], M[A][t], m); d2 = sep(M[X][t], M[B][t], m); dab = sep(M[A][t], M[B][t], m)
    return d1, d2, dab
hits = []
for X in bodies:
    for A, B in itertools.combinations(stars, 2):
        for m in ('RA', 'Dec'):
            d1, d2, dab = ratio_at(X, A, B, m, 0)
            if abs(d1 + d2 - dab) > 0.01 or min(d1, d2) < 1: continue
            r = max(d1, d2) / min(d1, d2)
            for name, t in TG.items():
                if abs(r / t - 1) <= 0.001:
                    # minute of exactness
                    best = min(M[X], key=lambda tt: abs((lambda a, b, c: max(a, b) / max(min(a, b), 1e-9))(*ratio_at(X, A, B, m, tt)) / t - 1))
                    near = (A if d1 < d2 else B)
                    nums = [f"#{rk} {mm} {v:.4f}" for rk, mm, v in top if mm == m and (abs(d1 - v) <= 0.005 or abs(d2 - v) <= 0.005)]
                    hits.append((X, A, B, m, name, r, d1, d2, best, near, nums))
print(f"STAR FRAMES – {R}   sky bodies {len(bodies)}, stars {len(stars)}, hits {len(hits)}")
by = {}
for h in hits: by.setdefault(h[0], []).append(h)
for X in sorted(by, key=lambda x: -len(by[x])):
    print(f"\n  {X}  ({len(by[X])} frames)")
    for X_, A, B, m, name, r, d1, d2, best, near, nums in sorted(by[X], key=lambda h: (h[4], h[3])):
        print(f"      {A}–{X}–{B} {m:3} ratio {name:12} {r:.4f}  ({A} {d1:.4f} / {B} {d2:.4f})  exact @{best:+d} min" + (f"  RACE NUMBER {', '.join(nums)}" if nums else ''))
print("\nPER RUNNER – framed sky bodies reaching the runner's natal bodies (>= 95 in the window -2..+15)")
order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
for c in order:
    out = []
    for sd, tab in rc.charts[c].items():
        P = rc.natal[tab]
        for X in by:
            for n in P:
                if n in STARS or n in FASTNATAL: continue
                for m in ('RA', 'Dec'):
                    v0 = sep(M[X][0], P[n], m); f = max(FAMS, key=lambda k: FN[k](v0, m))
                    sc = {t: FN[f](sep(M[X][t], P[n], m), m) for t in M[X]}
                    pk = max(range(-2, 16), key=lambda t: sc[t])
                    if sc[pk] >= 95: out.append(f"{sd} {X}({len(by[X])})→{n} {f[:6]} {m} {v0:.4f} off {sc[0]:.0f} pk {sc[pk]:.1f}@{pk:+d}")
    print(f"  {res[c]['finish']:>3} {rc.names[c][0]:20} {res[c]['sp']:>6}  {len(out)}: " + '; '.join(out))
