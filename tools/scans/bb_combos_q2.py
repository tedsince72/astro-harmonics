"""Q2 (bb_fieldcheck_nelson: the same royal star on natal X in both planes, both carried by sky pairs, one carrier holding that star)
combined with every BB rule, pairs and triples (17 Nov 2026, Eddie: 'Q2 is the closest ... and what about combinations'; read-only).
Picks / won / by chance over bb_fieldcheck_nelson.RACES; listed when 2+ winners (and Q2 alone)."""
import json, sys, itertools
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_nelson as Q


def main():
    data = []
    for race, win in Q.RACES:
        J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
        h = {r: set() for r in J['runners']}
        for rid, cs in J['rules'].items():
            for c in cs:
                if not c.get('watch_only'):
                    h.setdefault(c['runner'], set()).add(rid)
        D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        for run, d in D.items():
            if 'Q2' in Q.cases(d): h.setdefault(run, set()).add('Q2')
        data.append((race, win, len(J['runners']), h))
    rules = sorted({x for _, _, _, h in data for s in h.values() for x in s if x != 'Q2'})
    rows = []
    for k in (0, 1, 2):
        for extra in itertools.combinations(rules, k):
            combo = ('Q2',) + extra
            p = w = 0; c = 0.0; ws = []
            for race, win, N, h in data:
                for r, s in h.items():
                    if set(combo) <= s:
                        p += 1; c += 1 / N
                        if win in r: w += 1; ws.append(r)
            if w >= 2 or k == 0:
                rows.append((combo, p, w, c, ws))
    print(f'## Q2 combinations ({len(data)} result races)')
    for combo, p, w, c, ws in sorted(rows, key=lambda x: (-(x[2] - x[3]), -x[2], x[1]))[:40]:
        print(f"  {' + '.join(combo)}: {p} / {w} / {c:.1f}  {', '.join(ws)}")


if __name__ == '__main__':
    main()
