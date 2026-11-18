"""The 19 winners the fresh-sheet cover misses (18 Nov 2026, Eddie: 'what do they have in pattern terms'; read-only).
In those 19 races only: each rule and rule pair, picks / won / by chance; best by p (bb_fresh_sheet.tail). Also the
watch-only notes and the BB rules each winner holds alone."""
import sys, itertools, json
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as N, bb_fresh_sheet as F
MISS = ['Graces Quest', 'Hamish', 'Arvico Bleu', 'Present Moment', 'Sir Chauvelin', 'Not Available', 'First Flow', 'Nicholas T',
        'Venturous', 'New Age Dawning', 'Two For Gold', 'Silva Eclipse', 'Olympe De Gouges', 'River Bray', 'Daphne Moon',
        'Domandlouis', 'Cafe Sydney', 'Novakai']
data = []
for race, win in N.RACES:
    if win in MISS:
        runners, hh = F.holders(race); data.append((race, next(r for r in runners if win in r), runners, hh))
print(f'{len(data)} races, {sum(len(d[2]) for d in data)} runners\n')
print('## Each winner: rules held (alone = only holder in the race)\n')
for race, w, runners, hh in data:
    al = [x for x in sorted(hh[w]) if sum(x in s for s in hh.values()) == 1]
    cnt = sorted((len(s) for s in hh.values()), reverse=True)
    print(f"- {w} ({race}): {len(hh[w])} rules, field {cnt}; alone {al}; all {sorted(hh[w])}")
rules = sorted({x for d in data for s in d[3].values() for x in s})
for k in (1, 2):
    rows = []
    for c in itertools.combinations(rules, k):
        cs = set(c); ps = []; w = 0; wins = []
        for race, win, runners, hh in data:
            for r, s in hh.items():
                if cs <= s:
                    ps.append(1 / len(runners))
                    if r == win: w += 1; wins.append(win.split(' ', 1)[-1])
        if w >= 2: rows.append((F.tail(ps, w), c, len(ps), w, sum(ps), wins))
    rows.sort()
    print(f"\n## {'Single rules' if k == 1 else 'Pairs'} in these races, best 15\n")
    for p, c, n, w, ch, wins in rows[:15]:
        print(f"- {' + '.join(c)}: {n} / {w} / {ch:.1f} (p {p:.3f}) - {', '.join(wins)}")
