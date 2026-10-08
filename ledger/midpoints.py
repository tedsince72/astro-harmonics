#!/usr/bin/env python3
"""midpoints.py v1.0 - midpoints from the raw positions (Eddie, 3 Oct 08:38: "no stone unturned - check the
midpoints"). Same three types as the detail sheets, plus the three-way, each in RA and Dec separately:
  T3  natal C at the midpoint of natal A / natal B (one chart)          - the imprint
  T4  natal C at the midpoint of an 80+ sky pair A / B                  - the moment onto the runner
  T5  sky C at the midpoint of natal A / natal B (one chart)            - the moment onto the imprint
  3W  the same body: sky, horse natal and jockey natal - one sitting at the midpoint of the other two
RA midpoints are taken on the shorter arc. dev = how far C is from the exact midpoint (deg). Natal Moon and
fast points left out; star-star-star left out; fast natal bodies marked *. Counts at dev <= 0.01 and the
exact ones (<= 0.003) listed when they touch a top-12 sky pair, the busy bodies or a T4.
Usage: python3 midpoints.py --race RACE"""
import argparse, collections, itertools, sys
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, STARS, FAST, FASTNATAL, NODES, results

def mid(p, q, m):
    if m == 'Dec':
        return (p[1] + q[1]) / 2
    d = ((q[0] - p[0] + 180) % 360) - 180
    return (p[0] + d / 2) % 360

def off(x, mp, m):
    v = x[1] if m == 'Dec' else x[0]
    return abs(v - mp) if m == 'Dec' else abs(((v - mp + 180) % 360) - 180)

ap = argparse.ArgumentParser(); ap.add_argument('--race', required=True); a = ap.parse_args()
rc = Race(a.race); res = results(a.race)
order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
sky = {b: v for b, v in rc.sky.items() if b not in FAST and b != 'equator'}
top12 = rc.byrank[:12]
topb = {b for k in top12 for b in k}
pairs80 = rc.byrank
print(f"MIDPOINTS – {a.race}")
print("counts at dev <= 0.01 deg: T3 / T4 / T5 (horse | jockey); 3W per partnership")
store = {}
for c in order:
    row = []
    for sd in ('H', 'J'):
        tab = rc.charts[c][sd]; P = {b: v for b, v in rc.natal[tab].items() if b != 'Moon'}
        t3, t4, t5 = [], [], []
        bodies = sorted(P)
        for A, B in itertools.combinations(bodies, 2):
            for m in ('RA', 'Dec'):
                mp = mid(P[A], P[B], m)
                for C in bodies:
                    if C in (A, B) or (A in STARS and B in STARS and C in STARS):
                        continue
                    d = off(P[C], mp, m)
                    if d <= 0.01:
                        t3.append((d, f"{C} at {A}/{B} {m}"))
                for C, sv in sky.items():
                    if C in (A, B) and False:
                        continue
                    if A in STARS and B in STARS and C in STARS:
                        continue
                    d = off(sv, mp, m)
                    if d <= 0.01:
                        t5.append((d, f"sky {C}{'#' if C in topb else ''} at natal {A}/{B} {m}"))
        for k in pairs80:
            A, B = k
            for m in ('RA', 'Dec'):
                mp = mid(rc.sky[A], rc.sky[B], m)
                for C in bodies:
                    if A in STARS and B in STARS and C in STARS:
                        continue
                    d = off(P[C], mp, m)
                    if d <= 0.01:
                        t4.append((d, f"natal {C}{'*' if C in FASTNATAL else ''} at sky #{rc.pairs[k]['rank']} {A}/{B} {m}"))
        store[(c, sd)] = (t3, t4, t5)
        row.append(f"{len(t3)}/{len(t4)}/{len(t5)}")
    # three-way
    H = rc.natal[rc.charts[c]['H']]; J = rc.natal[rc.charts[c]['J']]; w = []
    for b in sky:
        if b not in H or b not in J or b == 'Moon' or b in STARS:
            continue
        for m in ('RA', 'Dec'):
            for lab, x, y, z in (('sky', sky[b], H[b], J[b]), ('horse', H[b], sky[b], J[b]), ('jockey', J[b], sky[b], H[b])):
                d = off(x, mid(y, z, m), m)
                if d <= 0.01:
                    w.append((d, f"{lab} {b} at mid of the other two {m}"))
    store[(c, '3W')] = w
    print(f"  {res[c]['finish']:>3} {rc.names[c][0]:18} {res[c]['sp']:>5}  H {row[0]:>12} | J {row[1]:>12} | 3W {len(w)}")
print("\nEXACT (dev <= 0.003): every T4 (natal body at a sky pair's midpoint), T5 with a top-12 sky body, T3 on a busy body, all 3W")
for c in order:
    print(f"  {res[c]['finish']} {rc.names[c][0]} {res[c]['sp']}")
    for sd in ('H', 'J'):
        t3, t4, t5 = store[(c, sd)]
        e4 = [t for d, t in sorted(t4) if d <= 0.003]
        e5 = [t for d, t in sorted(t5) if d <= 0.003 and '#' in t]
        e3 = [t for d, t in sorted(t3) if d <= 0.003 and t.split(' at ')[0] in rc.busy]
        if e4: print(f"    {sd} T4: " + '; '.join(e4))
        if e5: print(f"    {sd} T5: " + '; '.join(e5))
        if e3: print(f"    {sd} T3 (busy body): " + '; '.join(e3))
    w = store[(c, '3W')]
    if w: print("    3W: " + '; '.join(f"{t} ({d:.4f})" for d, t in sorted(w)))
