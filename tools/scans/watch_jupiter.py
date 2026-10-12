#!/usr/bin/env python3
"""watch_jupiter.py RACE [RACE ...]  — watch line for the rest of the blind batch (Eddie 12 Oct 2026, defined before Musselburgh 13:45
and not to be changed). Not part of the frozen reader; printed beside each race page before the result is opened.

"A rare item (held by fewer than half the field) linking Jupiter with itself across charts — H/J/S Jupiter in an Equator ratio, a same-body
set, a movement onto a whole/ninth, or a cross link H Jupiter – J Jupiter."
Made exact (from Layer 1, docs/classic/<race>/layer1/P*.json, strict as the frozen reader counts them):
  E  Equator ratio of Jupiter (S/H, S/J or H/J), tight band (<= 0.01 %)
  B  same-body set of Jupiter (any plane, worst <= 0.15 %, no ratio of 1)
  M  horse or jockey Jupiter moved onto a whole/ninth (sky Jupiter vs natal Jupiter, RA/Dec/Flat/GC, +-0.01 / +-0.0011)
  X  close cross link H Jupiter – J Jupiter (RA < 1.5 or Dec < 0.3)
Rare is judged per kind: a kind counts for a runner only when fewer than half the field hold that kind. A runner holds the watch line
when it holds at least one rare kind. Output: docs/classic/<race>/checklist/watch_jupiter.txt (no results used)."""
import sys, os, glob, json

KINDS = {'E': 'Jupiter Equator ratio', 'B': 'Jupiter same-body set', 'M': 'Jupiter moved onto a whole/ninth', 'X': 'cross link H Jupiter – J Jupiter'}

def kinds(I):
    out = {}
    e = [x for x in I['eq_ratios'] if x['body'] == 'Jupiter' and x['band'] == 'tight']
    if e: out['E'] = '; '.join(f"{x['pair']} {x['values'][0]:.4f} / {x['values'][1]:.4f} {x['dir']} {x['ratio']} ({x['err_pct']:.4f}%)" for x in e)
    b = [x for x in I['same_body'] if x['body'] == 'Jupiter' and '1' not in x['ratios']]
    if b: out['B'] = '; '.join(f"{x['plane']} {' : '.join(x['ratios'])} (worst {x['worst_pct']:.4f}%)" for x in b)
    m = [x for x in I['movement'] if x['body'] == 'Jupiter']
    if m: out['M'] = '; '.join(f"{x['chart']} Jupiter moved {x['plane']} {x['value']:.5f} ({x['num']})" for x in m)
    x_ = [l for l in I['links'] if l['kind'] == 'cross' and l['a'] == 'H Jupiter' and l['b'] == 'J Jupiter' and l['close']]
    if x_: out['X'] = '; '.join(f"RA {l['RA']:.4f} Dec {l['Dec']:.4f}" for l in x_)
    return out

def watch(race):
    R = {}
    for f in sorted(glob.glob(f'docs/classic/{race}/layer1/P*.json')):
        I = json.load(open(f)); R[os.path.basename(f)[:-5]] = (I['runner'], kinds(I))
    n = len(R); held = {k: [P for P, (_, d) in R.items() if k in d] for k in KINDS}
    rare = {k for k, ps in held.items() if ps and len(ps) * 2 < n}
    L = [f"== {race}  WATCH LINE (defined 12 Oct 2026, before Musselburgh; not evidence): rare Jupiter–Jupiter across charts",
         f"   field {n}; rare = held by fewer than half the field (< {n / 2:g})"]
    for k, name in KINDS.items():
        L.append(f"   [{k}] {name}: held by {len(held[k])} of {n}{' — RARE' if k in rare else ''}" + (f" ({', '.join(held[k])})" if held[k] else ''))
    L.append('   runners:')
    holders = []
    for P, (name, d) in R.items():
        mine = [k for k in d if k in rare]
        if mine: holders.append(P)
        L.append(f"   {P} {name:44s} {'HOLDS ' + ','.join(mine) if mine else '-':10s} " + ' | '.join(f"[{k}] {v}" for k, v in d.items()))
    L.append(f"   watch line held by: {', '.join(holders) or 'nobody'}")
    return '\n'.join(L)

if __name__ == '__main__':
    for race in sys.argv[1:]:
        t = watch(race); print(t)
        os.makedirs(f'docs/classic/{race}/checklist', exist_ok=True)
        open(f'docs/classic/{race}/checklist/watch_jupiter.txt', 'w').write(t + '\n')
