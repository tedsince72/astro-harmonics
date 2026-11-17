"""Combinations of Two For Gold's rules (Lingfield 15:00 23 Jan 2022; 17 Nov 2026; read-only). Rule holders from each race's bbrules json
(watch-only left out). Every 1-, 2- and 3-combination of the winner's rules: picks / won / by chance over the 34 result races
(bb_fieldcheck_twoforgold.RACES); listed when 2+ winners, all holders won, or a single rule."""
import json, sys, itertools
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_fieldcheck_twoforgold as TG
WIN_RACE, WIN = '20220123_lingfield_1500', 'Two For Gold'


def holders(race):
    J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
    h = {}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                h.setdefault(c['runner'], set()).add(rid)
    return J['runners'], h


def main():
    data = [(race, win, *holders(race)) for race, win in TG.RACES]
    mine = next(h for race, win, runners, hh in data if race == WIN_RACE for r, h in hh.items() if WIN in r)
    items = sorted(mine)
    print('Two For Gold items:', ', '.join(items))
    rows = []
    for k in (1, 2, 3):
        for combo in itertools.combinations(items, k):
            p = w = 0; c = 0.0; ws = []
            for race, win, runners, hh in data:
                N = len(runners)
                for r, h in hh.items():
                    if set(combo) <= h:
                        p += 1; c += 1 / N
                        if win in r:
                            w += 1; ws.append(r)
            rows.append((combo, p, w, c, ws))
    for combo, p, w, c, ws in sorted(rows, key=lambda x: (len(x[0]) > 1, -(x[2] / x[1]) if x[1] else 0, -x[2])):
        if w >= 2 or (p and w == p) or len(combo) == 1:
            print(f"  {' + '.join(combo)}: {p} / {w} / {c:.1f}  {', '.join(ws)}")


if __name__ == '__main__':
    main()
