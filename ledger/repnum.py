#!/usr/bin/env python3
"""repnum.py v1.1 - the race's REPEATED number(s): a number carried by two or more of the top-12 sky pairs
(same coordinate, within 0.03 deg). Seen in T33, T32 and R21 (3 Oct): the winner connected to it each time.
For each runner: who carries the number (natal-natal on either chart, horse x jockey, sky -> natal on a natal
body that is not a star or the Moon) within 0.006, with the value over the unknown birth hour where a fast
natal body is involved; and how each runner holds the pairs that carry the number (inside / landings).
v1.1 (3 Oct, R39): a number repeated ACROSS coordinates also counts (e.g. #2 RA 12.2226 and #6 Dec 12.2211);
carriers are then searched in both coordinates.
Usage: python3 repnum.py --race RACE"""
import argparse, sys
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, STARS, FAST, FASTNATAL, results
ap = argparse.ArgumentParser(); ap.add_argument('--race', required=True); a = ap.parse_args()
rc = Race(a.race); rc.build(); res = results(a.race)
order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
vals = [(rc.pairs[k]['rank'], k, e[0], e[3]) for k in rc.byrank[:12] for e in rc.pairs[k]['entries']]
groups = []
for i, x in enumerate(vals):
    for y in vals[i + 1:]:
        if abs(x[3] - y[3]) <= 0.03 and x[1] != y[1]:
            g = next((g for g in groups if x in g or y in g), None)
            if g: g.update([x, y])
            else: groups.append({x, y})
print(f"REPEATED NUMBERS – {a.race}")
if not groups:
    print("  none in the top 12")
def hr(tab, b):
    return rc.hourly[tab].get(b) or [rc.natal[tab][b]] * 25
for g in groups:
    g = sorted(g); modes = sorted({x[2] for x in g}); tgt = sum(v for *_, v in g) / len(g)
    print(f"\n  {'/'.join(modes)} ≈ {tgt:.4f}: " + '; '.join(f"#{rk} {k[0]}/{k[1]} {mm} {v:.4f}" for rk, k, mm, v in g))
    for c in order:
        H = rc.natal[rc.charts[c]['H']]; J = rc.natal[rc.charts[c]['J']]; out = []
        th, tj = rc.charts[c]['H'], rc.charts[c]['J']
        for tag, A, B, ta, tb in (('H', H, H, th, th), ('J', J, J, tj, tj), ('HxJ', H, J, th, tj)):
            for x in A:
                for y in B:
                    if tag != 'HxJ' and x >= y: continue
                    if (x in STARS and y in STARS) or 'Moon' in (x, y): continue
                    for m in modes:
                        v = sep(A[x], B[y], m)
                        if abs(v - tgt) <= 0.006:
                            rng = ''
                            if {x, y} & FASTNATAL:
                                vv = [sep(p, q, m) for p in hr(ta, x) for q in hr(tb, y)] if tag == 'HxJ' else [sep(p, q, m) for p, q in zip(hr(ta, x), hr(tb, y))]
                                rng = f" (birth day {min(vv):.3f}-{max(vv):.3f})"
                            out.append(f"{tag} {x}{'*' if x in FASTNATAL else ''}–{y}{'*' if y in FASTNATAL else ''} {m} {v:.4f}{rng}")
        for sd, tab in rc.charts[c].items():
            P = rc.natal[tab]
            for s in rc.sky:
                if s in FAST or s in STARS or s == 'equator': continue
                for n in P:
                    if n in STARS or n == 'Moon': continue
                    for m in modes:
                        v = sep(rc.sky[s], P[n], m)
                        if abs(v - tgt) <= 0.006:
                            out.append(f"{sd} sky {s}→{n}{'*' if n in FASTNATAL else ''} {m} {v:.4f}")
        held = []
        for rk, k, mm, v in g:
            sides = rc.hold[c].get(k, {})
            hows = [f"{sd} {rc.how(it)}" for sd, it in sides.items() if rc.how(it)]
            lands = [f"{sd} lands {ld['C']}" for sd, ls in rc.land[c].get(k, {}).items() for ld in ls]
            if hows or lands:
                held.append(f"#{rk}: " + ', '.join(hows + lands) + (' ALONE' if hows and rc.inside[k] == {c} else ''))
        print(f"    {res[c]['finish']:>3} {rc.names[c][0]:18} {res[c]['sp']:>6} | carries: {'; '.join(out) or '-'} | holds: {'; '.join(held) or '-'}")
