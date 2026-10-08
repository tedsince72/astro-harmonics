#!/usr/bin/env python3
"""scalenum.py v1.0 - the SAME number at different decimal places in the sky (Eddie, 3 Oct 11:39: "same numbers just
moving decimal place – I like this"). Pairs of top-12 sky distances where one is 10x or 100x the other (within
0.003 x scale), e.g. R9 40/9 (#3) & 400/9 (#10). For each family, who carries any scale of it (0.1x ... 100x),
in either coordinate: natal-natal, horse x jockey, sky -> natal (natal stars and Moon left out; fast natal * ).
Usage: python3 scalenum.py --race RACE"""
import argparse, sys
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, STARS, FAST, FASTNATAL, results
ap = argparse.ArgumentParser(); ap.add_argument('--race', required=True); a = ap.parse_args()
rc = Race(a.race); res = results(a.race)
order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
vals = [(rc.pairs[k]['rank'], k, e[0], e[3]) for k in rc.byrank[:12] for e in rc.pairs[k]['entries']]
fams = []
for i, x in enumerate(vals):
    for y in vals[i + 1:]:
        lo, hi = sorted([x, y], key=lambda t: t[3])
        for f in (10, 100):
            if lo[3] > 0.05 and abs(hi[3] - f * lo[3]) <= 0.003 * f:
                fams.append((lo, hi, f))
print(f"DECIMAL-SCALE NUMBERS – {a.race}")
if not fams:
    print("  none in the top 12")
for lo, hi, f in fams:
    base = lo[3]
    ts = [base / 10, base, base * 10, base * 100]
    print(f"\n  #{lo[0]} {lo[1][0]}/{lo[1][1]} {lo[2]} {lo[3]:.4f}  &  #{hi[0]} {hi[1][0]}/{hi[1][1]} {hi[2]} {hi[3]:.4f}  (x{f})")
    for c in order:
        th, tj = rc.charts[c]['H'], rc.charts[c]['J']; H = rc.natal[th]; J = rc.natal[tj]; out = []
        for tag, A, B in (('H', H, H), ('J', J, J), ('HxJ', H, J)):
            for x in A:
                for y in B:
                    if tag != 'HxJ' and x >= y: continue
                    if (x in STARS and y in STARS) or 'Moon' in (x, y): continue
                    for m in ('RA', 'Dec'):
                        v = sep(A[x], B[y], m)
                        for t in ts:
                            if t >= 0.05 and abs(v - t) <= 0.003 * max(1, t / 10):
                                out.append(f"{tag} {x}–{y}{'*' if {x, y} & FASTNATAL else ''} {m} {v:.4f}")
        for sd, tab in rc.charts[c].items():
            P = rc.natal[tab]
            for s in rc.sky:
                if s in FAST or s in STARS or s == 'equator': continue
                for n in P:
                    if n in STARS or n == 'Moon': continue
                    for m in ('RA', 'Dec'):
                        v = sep(rc.sky[s], P[n], m)
                        for t in ts:
                            if t >= 0.05 and abs(v - t) <= 0.003 * max(1, t / 10):
                                out.append(f"{sd} sky {s}→{n}{'*' if n in FASTNATAL else ''} {m} {v:.4f}")
        print(f"    {res[c]['finish']:>3} {rc.names[c][0]:18} {res[c]['sp']:>6} ({len(out)}): " + '; '.join(out))
