#!/usr/bin/env python3
"""surprise.py v1.1 - ranks the 96 races from the most unexpected winner to the most expected
(Eddie, 2 Oct 2026: "start with the highest odds / most unexpected winners and work towards the most
expected ones"). Measure agreed 21:21: winner's odds against the favourite's - ratio of decimal odds
(winner SP + 1) / (favourite SP + 1). A favourite that won scores 1 (joint favourites: the shorter
co-favourite counts); ties broken by the winner's own price (a longer-priced winner is less expected).
Also shown: the winner's share of the market (normalised implied probability) and its price rank.
Labels: R1-R48 = first 48 by date (reads_1_24/25_48), T1-T48 = test 48 (grids_scored order).
v1.1 (3 Oct, Eddie spotted T47 wrong): odds are read from the SP text itself (e.g. 15/8J, Evens) -
the stored sp_odds column had 0.0 for the joint favourites 15/8J, which made T47's ratio x17.0 instead of x5.9.
Usage: python3 surprise.py --base profiles.csv --test profiles_test_scored.csv --grids DIR --out CSV"""
import argparse, csv, os, collections
ap = argparse.ArgumentParser()
for k in ('base', 'test', 'grids', 'out'): ap.add_argument('--' + k, required=True)
a = ap.parse_args()
rows = list(csv.DictReader(open(a.base))) + list(csv.DictReader(open(a.test)))
by = collections.defaultdict(list)
for r in rows: by[r['race']].append(r)
base = sorted({r['race'] for r in csv.DictReader(open(a.base))})
test = [f[:-9] for f in sorted(os.listdir(a.grids)) if f.endswith('_grid.txt')]
label = {R: f'R{i+1}' for i, R in enumerate(base)}; label.update({R: f'T{i+1}' for i, R in enumerate(test)})
out = []
for R, rs in by.items():
    def odds(r):
        t = r['sp'].strip().rstrip('FJC').strip()
        if t.lower() in ('evens', 'evs'):
            return 1.0
        n, d = t.split('/')
        return float(n) / float(d)
    w = [r for r in rs if r['finish'] == '1']
    if len(w) != 1: print('no single winner', R); continue
    w = w[0]; fav = min(rs, key=odds)
    dec = {r['cloth']: odds(r) + 1 for r in rs}
    share = (1 / dec[w['cloth']]) / sum(1 / d for d in dec.values())
    ratio = dec[w['cloth']] / (odds(fav) + 1)
    prank = 1 + sum(1 for r in rs if odds(r) < odds(w))
    favr = [r for r in rs if abs(odds(r) - odds(fav)) < 1e-9]   # joint favourites both shown
    out.append(dict(label=label.get(R, '?'), race=R, field=len(rs), winner=w['partnership'].split('  /')[0], winner_sp=w['sp'],
                    fav=' & '.join(r['partnership'].split('  /')[0] for r in favr), fav_sp=fav['sp'],
                    fav_finish=' & '.join(r['finish'] for r in favr), ratio=round(ratio, 3), win_share=round(share, 3), price_rank=prank))
out.sort(key=lambda d: (-d['ratio'], -float(eval(d['winner_sp'].rstrip('FJC').replace('Evens', '1/1')))))
with open(a.out, 'w', newline='') as o:
    w = csv.DictWriter(o, fieldnames=['order'] + list(out[0])); w.writeheader()
    for i, d in enumerate(out): w.writerow(dict(order=i + 1, **d))
print(len(out))
