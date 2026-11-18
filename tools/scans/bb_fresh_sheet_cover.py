"""Greedy cover (18 Nov 2026, Eddie: 'which of the above cover the largest group of winners starting with BB32'; read-only).
Start with BB32, then add from the fresh-sheet profit items the one adding the most winners above chance (new winners minus the sum
of 1 / field size over its new picks); stop when that gain is 0.5 or less. (Most new winners alone picks BB3: 283 of 333 runners.)
Running totals on the union of picks (a runner counted once): picks / won / by chance, level-stake profit at SP."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as N, bb_fresh_sheet as F, bb_fresh_sheet_profit as P

data = []
for race, win in N.RACES:
    runners, hh = F.holders(race); w = next(r for r in runners if win in r)
    data.append((race, w, runners, hh, P.sp(race, win)[0]))


def picks(it):
    s = set(it); return {(d[0], r) for d in data for r, rs in d[3].items() if s <= rs}


W = {(d[0], d[1]) for d in data}; info = {d[0]: d for d in data}
items = {' + '.join(it): picks(it) for it in P.ITEMS}
def gain(k, cur):
    new = items[k] - cur; return len(new & W) - sum(1 / len(info[r][2]) for r, _ in new)


chosen = ['BB32']; cur = set(items['BB32'])
while True:
    best = max((k for k in items if k not in chosen), key=lambda k: gain(k, cur))
    if gain(best, cur) <= 0.5: break
    chosen.append(best); cur |= items[best]
    pass
cur = set(); print('| add | new winners | total picks / won / chance | profit | ROI |\n|---|---|---|---|---|')
for k in chosen:
    new = (items[k] - cur) & W; cur |= items[k]
    n = len(cur); w = len(cur & W); c = sum(1 / len(info[r][2]) for r, _ in cur)
    pr = sum(info[r][4] if (r, x) in W else -1 for r, x in cur)
    print(f"| {k} | {len(new)}: {', '.join(info[r][1].split(' ', 1)[-1] for r, _ in sorted(new))} | {n} / {w} / {c:.1f} | {pr:+.1f} | {100*pr/n:+.0f} % |")
miss = sorted(W - cur); print(f"\nNot covered ({len(miss)}): " + ', '.join(info[r][1].split(' ', 1)[-1] for r, _ in miss))
