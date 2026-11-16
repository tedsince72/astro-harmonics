"""Scan (16 Nov 2026, Eddie: 'are there any combinations of rules in a race that perform well together, taking the whole sample').
Read-only. Holders from the committed docs/eddie_read/bybody_rules/<race>_bbrules.json (watch-only cases left out), 8 result races.
A combination is held by a runner holding every rule in it. Per combination: picks (runner-races), winners, by chance (sum of holders /
field). Pairs and triples with at least 3 picks; ranked by winners minus chance. Every rule was built on these winners (in-sample), and
thousands of combinations are tried, so a noise benchmark is given: the same search with the 'winner' replaced by a random runner of
each race (500 draws) - how many combinations reach the same winners at the same or fewer picks by luck.
Also: winners by the number of rules held (rank in the field)."""
import itertools, json, random, sys
from collections import defaultdict
RACES = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad')]
R = []
for n, r, w in RACES:
    J = json.load(open(f'docs/eddie_read/bybody_rules/{r}_bbrules.json'))
    runners = [x if isinstance(x, str) else (x.get('sheet') or x.get('runner') or str(x)) for x in J['runners']]
    hold = defaultdict(set)
    for rid, cases in J['rules'].items():
        for c in cases:
            if not c.get('watch_only'):
                hold[c['runner']].add(rid)
    win = [x for x in runners if w in x]
    assert len(win) == 1, (n, win)
    R.append((n, runners, hold, win[0]))
rules = sorted({k for _, _, h, _ in R for s in h.values() for k in s})


def score(combo, winners):
    p = wn = 0; c = 0.0
    for (n, runners, hold, _), w in zip(R, winners):
        hs = [x for x in runners if set(combo) <= hold[x]]
        p += len(hs); wn += w in hs; c += len(hs) / len(runners)
    return p, wn, c


real = [w for *_, w in R]
res = {}
for k in (1, 2, 3):
    for combo in itertools.combinations(rules, k):
        p, wn, c = score(combo, real)
        if p >= 3 and wn:
            res[combo] = (p, wn, c)
top = sorted(res.items(), key=lambda kv: -(kv[1][1] - kv[1][2]))
print('## Best combinations (picks >= 3), ranked by winners minus chance')
print('| rules | picks | winners | by chance | winners / picks |\n|---|---|---|---|---|')
for combo, (p, wn, c) in top[:30]:
    print(f"| {' + '.join(combo)} | {p} | {wn} | {c:.1f} | {wn}/{p} |")

# noise benchmark: the best (winners - chance) found per draw, pairs and triples
random.seed(1)
best = []
pairs = [c for k in (2, 3) for c in itertools.combinations(rules, k)]
cand = [c for c in pairs if score(c, real)[0] >= 3]
for _ in range(500):
    fake = [random.choice(runners) for _, runners, _, _ in R]
    b = 0.0
    for combo in cand:
        p, wn, c = score(combo, fake)
        b = max(b, wn - c)
    best.append(b)
best.sort()
bestreal = max((v[1] - v[2]) for k, v in res.items() if len(k) > 1)
print(f"\n## Noise benchmark ({len(cand)} pairs / triples with >= 3 picks, 500 random 'winners' per race)")
print(f"real best winners - chance: {bestreal:.2f}; random draws: median {best[250]:.2f}, 95th percentile {best[475]:.2f}, "
      f"share of draws >= real {sum(b >= bestreal for b in best) / 500:.2f}")

print('\n## Winners by number of rules held')
for n, runners, hold, w in R:
    cnt = sorted(((len(hold[x]), x) for x in runners), reverse=True)
    rank = 1 + sum(1 for c, x in cnt if c > len(hold[w]))
    print(f"  {n}: {w} holds {len(hold[w])} rules, rank {rank} of {len(runners)} (field max {cnt[0][0]})")
