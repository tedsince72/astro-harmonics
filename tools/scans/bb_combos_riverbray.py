"""Combinations of River Bray's rules (Wincanton 14:20 21 Mar 2022; 17 Nov 2026; read-only). Rule holders from each race's bbrules json
(watch-only left out) plus J1any (H Jupiter – J Jupiter, any score, 2+ sky pairs on its target; bb_fieldcheck_riverbray). Every single,
pair and triple of the winner's items: picks / won / by chance over the 26 result races; listed when 2+ winners or all holders won."""
import json, sys, os, itertools
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_riverbray as F
WIN_RACE, WIN = '20220321_wincanton_1420', 'River Bray'


def holders(race):
    J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
    h = {}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                h.setdefault(c['runner'], set()).add(rid)
    for run, D in R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx').items():
        if 'J1any' in F.tags(D, False)[0]:
            h.setdefault(run, set()).add('J1any')
    return J['runners'], h


def main():
    data = [(race, win, *holders(race)) for race, win in F.RACES
            if os.path.exists(f'docs/eddie_read/bybody_rules/{race}_bbrules.json')]
    mine = next(h for race, win, runners, hh in data if race == WIN_RACE for r, h in hh.items() if WIN in r)
    items = sorted(mine)
    print(f'{len(data)} result races. River Bray items:', ', '.join(items))
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
    for combo, p, w, c, ws in sorted(rows, key=lambda x: (-(x[2] / x[1]) if x[1] else 0, -x[2])):
        if w >= 2 or (p and w == p) or len(combo) == 1:
            print(f"  {' + '.join(combo)}: {p} / {w} / {c:.1f}  {', '.join(ws)}")


if __name__ == '__main__':
    main()
