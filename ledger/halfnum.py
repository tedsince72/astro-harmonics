#!/usr/bin/env python3
"""halfnum.py v1.0 - HALF NUMBERS kept in a separate area (Eddie, 3 Oct 08:21-08:22: "half numbers 0.50000
same as whole numbers but with half the tolerance ... keep it in a separate area for the moment").
Family: targets 0.5, 1.5 ... 199.5; scored as the engine's Whole Number (squared, no decay) with tolerance
0.01 deg instead of 0.02: score = (10*(0.01-dev)/0.01)^2. The engine and the other scripts are unchanged;
nothing here alters the 80+ list, ranks or busiest body.
Shows for one race: sky pairs on a half number (>= 80) and whether they are applying; each runner's
natal-natal half numbers (>= 80), dead-exact ones, and the bodies they sit on; natal-natal half numbers
that repeat a sky half number (same coordinate, within 0.005); horse x jockey cross; sky -> natal.
Usage: python3 halfnum.py --race RACE"""
import argparse, collections, itertools, sys
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, STARS, NODES, FAST, FASTNATAL, results

def half_score(v):
    if not (0.5 <= v <= 199.5):
        return 0.0
    dev = abs(v - (int(v) + 0.5))
    return 0.0 if dev >= 0.01 else (10.0 * (0.01 - dev) / 0.01) ** 2

def hdev(v):
    return abs(v - (int(v) + 0.5))

ap = argparse.ArgumentParser(); ap.add_argument('--race', required=True); a = ap.parse_args()
rc = Race(a.race); res = results(a.race)
fin = {c: res[c]['finish'] for c in res}
order = sorted(rc.charts, key=lambda c: (not fin[c].isdigit(), int(fin[c]) if fin[c].isdigit() else 99))
name = {c: rc.names[c][0] for c in rc.charts}
sky = [b for b in rc.sky if b not in FAST and b != 'equator']
S = []
for x, y in itertools.combinations(sorted(sky), 2):
    if x in STARS and y in STARS:
        continue
    for m in ('RA', 'Dec'):
        if m == 'RA' and {x, y} == NODES:
            continue
        v = sep(rc.sky[x], rc.sky[y], m); s = half_score(v)
        if s >= 80:
            dm = hdev(sep(rc.S3[x]['m2'], rc.S3[y]['m2'], m)); dp = hdev(sep(rc.S3[x]['p2'], rc.S3[y]['p2'], m))
            S.append((s, x, y, m, v, 'A' if dp < dm else 'S'))
S.sort(reverse=True)
cnt = collections.Counter(b for s, x, y, *_ in S for b in (x, y))
print(f"HALF NUMBERS – {a.race}   order: " + ', '.join(f"{fin[c]}:{name[c]} {res[c]['sp']}" for c in order))
print(f"\nSKY pairs on a half number (>=80): {len(S)}; bodies in most: " + ', '.join(f'{b} {n}' for b, n in cnt.most_common(6)))
for s, x, y, m, v, mv in S[:20]:
    old = rc.pairs.get((x, y)) or rc.pairs.get((y, x))
    print(f"  {x}/{y} {m} {v:.4f} half {s:.1f} dev {hdev(v):.4f} {mv}" + (f"   (also 80+ in the usual families: #{old['rank']})" if old else ''))
print('\nNATAL–NATAL half numbers per chart (>=80; dead-exact = dev <= 0.0005; natal Moon left out, fast bodies marked *)')
nat = {}
for c in order:
    for sd, tab in sorted(rc.charts[c].items()):
        P = rc.natal[tab]; out = []
        for x, y in itertools.combinations(sorted(P), 2):
            if (x in STARS and y in STARS) or 'Moon' in (x, y):
                continue
            for m in ('RA', 'Dec'):
                if m == 'RA' and {x, y} == NODES:
                    continue
                v = sep(P[x], P[y], m); s = half_score(v)
                if s >= 80:
                    out.append((hdev(v), x, y, m, v, s))
        out.sort(); nat[(c, sd)] = out
        bod = collections.Counter(b for _, x, y, *_ in out for b in (x, y) if b not in STARS)
        ex = [o for o in out if o[0] <= 0.0005]
        print(f"  {fin[c]} {name[c]:16} {sd}: {len(out):2} (dead-exact {len(ex)}) | bodies: {', '.join(f'{b} {n}' for b, n in bod.most_common(4))} | "
              + '; '.join(f"{x}–{y}{'*' if {x, y} & FASTNATAL else ''} {m} {v:.4f}" for d, x, y, m, v, s in ex[:6]))
print('\nIMPRINT ↔ MOMENT on half numbers: natal–natal (and horse×jockey) repeating a sky half-number pair (same coordinate, within 0.005)')
for c in order:
    out = []
    H, J = rc.natal[rc.charts[c]['H']], rc.natal[rc.charts[c]['J']]
    for s, sx, sy, sm, sv, mv in S:
        for sd in ('H', 'J'):
            for d, x, y, m, v, sc in nat[(c, sd)]:
                if m == sm and abs(v - sv) <= 0.005:
                    out.append(f"{sx}/{sy} {sm} {sv:.4f}: {sd} {x}–{y} {v:.4f}")
        for x in H:
            for y in J:
                if (x in STARS and y in STARS) or 'Moon' in (x, y):
                    continue
                v = sep(H[x], J[y], sm)
                if abs(v - sv) <= 0.005 and half_score(v) >= 80:
                    out.append(f"{sx}/{sy} {sm} {sv:.4f}: H {x} × J {y} {v:.4f}")
    print(f"  {fin[c]} {name[c]:16} {len(out)}: " + '; '.join(out))
print('\nSKY → NATAL on half numbers (>=90, not onto natal stars or Moon): count, applying, and the natal bodies taking 2+')
for c in order:
    tot = apn = 0; rec = collections.Counter(); ex = []
    for sd, tab in rc.charts[c].items():
        P = rc.natal[tab]
        for s_ in sky:
            if s_ in STARS:
                continue
            for n in P:
                if n in STARS or n == 'Moon':
                    continue
                for m in ('RA', 'Dec'):
                    v = sep(rc.sky[s_], P[n], m); sc = half_score(v)
                    if sc >= 90:
                        tot += 1; rec[(sd, n)] += 1
                        A = hdev(sep(rc.S3[s_]['p2'], P[n], m)) < hdev(sep(rc.S3[s_]['m2'], P[n], m)); apn += A
                        if hdev(v) <= 0.0005:
                            ex.append(f"{sd} {s_}→{n} {m} {v:.4f} {'A' if A else 'S'}")
    print(f"  {fin[c]} {name[c]:16} {tot:2} ({apn} applying) | receivers: {', '.join(f'{sd} {n} ×{k}' for (sd, n), k in rec.most_common() if k >= 2) or '-'} | dead-exact: {'; '.join(ex[:5])}")
