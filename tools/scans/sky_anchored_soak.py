#!/usr/bin/env python3
"""sky_anchored_soak.py RACE [RACE ...] [--min N] [--out FILE]   — candidate scan (Eddie 12 Oct 2026), NOT part of the frozen reader.

Sky-anchored soak: take each sky pair value on the day (sky X – sky Y in RA, Dec, Flat or GC, value >= 0.5; e.g. Haydock 14:20 sky Orcus–Eris
Dec 9.7751). For each runner, collect every value within +-0.02 of it that is a separation (any plane) between an instance of X or Y
(sky, horse or jockey) and any other body (any chart), the anchor itself left out. Partners = the distinct natal bodies (horse or jockey,
chart named, node folded) taking part in those values. A runner has the soak when it has >= N partners (default 4) with at least one
horse and one jockey partner. Positions from Layer 1 (docs/classic/<race>/layer1/P*.json). Stars and Moon are not in Layer 1.
Prints, per race, each anchor that any runner has, with every runner's partner count; and per runner the anchors it has."""
import sys, os, glob, json, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from layer1_inventory import rd, dd, fl, gc, BOD

PLANES = (('RA', rd), ('Dec', dd), ('Flat', fl), ('GC', gc))
TOL = 0.02
def fold(b): return 'Node' if b in ('Rahu', 'Ketu') else b
def node_pair(a, b): return {a, b} == {'Rahu', 'Ketu'}

def load(race):
    out = {}
    for f in sorted(glob.glob(f'docs/classic/{race}/layer1/P*.json')):
        I = json.load(open(f))
        out[os.path.basename(f)[:-5]] = (I['runner'], {f"{p['chart']} {p['body']}": (p['ra'], p['dec']) for p in I['points']})
    return out

def anchors(pos):
    A = []
    for a, b in itertools.combinations(BOD, 2):
        if node_pair(a, b) or fold(a) == fold(b): continue
        for pl, f in PLANES:
            v = f(pos[f'S {a}'], pos[f'S {b}'])
            if v >= 0.5: A.append((a, b, pl, v))
    return A

def partners(pos, a, b, v):
    """natal partners for anchor sky a–b = v: values within TOL from an instance of a or b to another body"""
    hits = []
    for x in (a, b):
        for c in 'SHJ':
            xi = f'{c} {x}'
            for y in pos:
                if y == xi or (y[0] == 'S' and c == 'S' and {y[2:], x} == {a, b}): continue   # the anchor itself
                if fold(y[2:]) == fold(x) and y[0] == c: continue
                for pl, f in PLANES:
                    w = f(pos[xi], pos[y])
                    if abs(w - v) <= TOL: hits.append((xi, y, pl, w))
    natal = {fq for h in hits for fq in (h[0], h[1]) if fq[0] in 'HJ'}
    natal = {f"{q[0]} {fold(q[2:])}" for q in natal}
    return natal, hits

def scan(race, nmin=4):
    R = load(race)
    any_pos = next(iter(R.values()))[1]
    res = {}
    for a, b, pl, v in anchors(any_pos):
        row = {}
        for P, (name, pos) in R.items():
            nat, hits = partners(pos, a, b, v)
            ok = len(nat) >= nmin and any(q[0] == 'H' for q in nat) and any(q[0] == 'J' for q in nat)
            row[P] = (len(nat), ok, sorted(nat), hits)
        res[(a, b, pl)] = (v, row)
    return R, res

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    nmin = int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 4
    for race in args:
        R, res = scan(race, nmin)
        print(f"== {race}: sky-anchored soaks (>= {nmin} natal partners incl. horse and jockey, +-{TOL})")
        for (a, b, pl), (v, row) in sorted(res.items(), key=lambda kv: kv[1][0]):
            have = [P for P in row if row[P][1]]
            if not have: continue
            print(f"   sky {a}–{b} {pl} {v:.4f}: " + '  '.join(f"{P}:{row[P][0]}{'*' if row[P][1] else ''}" for P in row))
            for P in have: print(f"        {P} {R[P][0][:34]:34s} " + ', '.join(row[P][2]))
