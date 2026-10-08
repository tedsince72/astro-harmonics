#!/usr/bin/env python3
"""carrier.py v1.0 - the CARRIER BODY (seen in all six winners T33, T32, R21, R29, R9, R30, 3 Oct): one natal body that
carries the race's numbers in the horse, in the jockey and between them, and that the sky touches at the off.
Race numbers = the top-12 sky distances (each scoring coordinate) and the same numbers x10 and /10.
For every runner and every natal body (not stars, not the Moon): where it carries a race number (same coordinate,
within 0.005 x scale) - H = horse natal, J = jockey natal, HxJ = between horse and jockey (the body on either side);
'?' when a fast natal body moves the value more than 0.02 over the birth day; and what the sky does to it (top-12
landings on that body, top-12 sky bodies hitting it at >= 90). Carriers listed when they hold numbers in 2+ places.
Usage: python3 carrier.py --race RACE"""
import argparse, collections, sys
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, NODES, FAST, FASTNATAL, results
ap = argparse.ArgumentParser(); ap.add_argument('--race', required=True); a = ap.parse_args()
rc = Race(a.race); rc.build(); res = results(a.race)
order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
nums = []
for k in rc.byrank[:12]:
    for e in rc.pairs[k]['entries']:
        for sc in (0.1, 1, 10):
            v = e[3] * sc
            if 0.3 <= v <= 180:
                nums.append((rc.pairs[k]['rank'], e[0], v, sc))
topb = {b for k in rc.byrank[:12] for b in k} - STARS
def hr(tab, b):
    return rc.hourly[tab].get(b) or [rc.natal[tab][b]] * 25
def unsure(ta, x, tb, y, m, cross):
    if not ({x, y} & FASTNATAL):
        return False
    A, B = hr(ta, x), hr(tb, y)
    vv = [sep(p, q, m) for p in A for q in B] if cross else [sep(p, q, m) for p, q in zip(A, B)]
    return max(vv) - min(vv) > 0.02
print(f"CARRIER BODIES – {a.race}  (race numbers: top-12 sky distances and x10 / /10)")
for c in order:
    th, tj = rc.charts[c]['H'], rc.charts[c]['J']; H = rc.natal[th]; J = rc.natal[tj]
    car = collections.defaultdict(list)
    for tag, A, B, ta, tb in (('H', H, H, th, th), ('J', J, J, tj, tj), ('HxJ', H, J, th, tj)):
        for x in A:
            for y in B:
                if tag != 'HxJ' and x >= y: continue
                if (x in STARS and y in STARS) or 'Moon' in (x, y): continue
                for rk, m, v0, scl in nums:
                    if m == 'RA' and {x, y} == NODES and tag != 'HxJ': continue
                    v = sep(A[x], B[y], m)
                    if abs(v - v0) <= 0.005 * max(1, scl):
                        q = '?' if unsure(ta, x, tb, y, m, tag == 'HxJ') else ''
                        lab = f"{tag} {x}–{y} {m} {v:.4f} =#{rk}{'' if scl == 1 else ('x10' if scl == 10 else '/10')}{q}"
                        for b, side in ((x, 'H' if tag != 'J' else 'J'), (y, 'J' if tag != 'H' else 'H')):
                            if b in STARS: continue
                            car[b].append((tag, q, lab))
    out = []
    for b, L in car.items():
        places = {t for t, q, _ in L if not q}
        if len(places) < 2:
            continue
        touch = []
        for k, sides in rc.land[c].items():
            if rc.pairs[k]['rank'] <= 12:
                for sd, ls in sides.items():
                    for ld in ls:
                        if ld['C'] == b:
                            touch.append(f"#{rc.pairs[k]['rank']} lands on {sd} {''.join(l['mv'] or 'n' for l in ld['legs'])}")
        for sd, tab in rc.charts[c].items():
            if b not in rc.natal[tab]: continue
            for s in topb:
                if s == b or s in FAST: continue
                for m in ('RA', 'Dec'):
                    v = sep(rc.sky[s], rc.natal[tab][b], m)
                    f = max(FAMS, key=lambda k: FN[k](v, m))
                    if FN[f](v, m) >= 90:
                        touch.append(f"sky {s}→{sd} {FN[f](v, m):.0f}")
        out.append((len(places), len(touch), b, sorted(places), L, touch))
    out.sort(key=lambda t: (-t[0], -t[1]))
    print(f"\n  {res[c]['finish']:>3} {rc.names[c][0]} {res[c]['sp']}: " + (', '.join(f"{b} [{'/'.join(p)}{' +sky' if t else ''}]" for n, nt, b, p, L, t in out) or '-'))
    for n, nt, b, p, L, t in out[:3]:
        print(f"      {b}: " + '; '.join(l for _, _, l in L[:8]) + (f" | the sky: {'; '.join(t[:6])}" if t else ''))
