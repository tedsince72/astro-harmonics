"""Combinations of Silva Eclipse's rules (Doncaster 16:00 23 Feb 2022; 17 Nov 2026; read-only). Rule holders from each race's bbrules json
(watch-only left out), plus S1s / R3s / R3s+ / T70 (bb_fieldcheck_silva) and N2s / N3s (bb_fieldcheck_silva_ninths). Every pair and triple of the
winner's items: picks / won / by chance over the result races (bb_fieldcheck_silva.RACES); listed when 2+ winners or all holders won."""
import json, sys, itertools
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_silva as S
import bb_fieldcheck_silva_ninths as SN
WIN_RACE, WIN = '20220223_doncaster_1600', 'Silva Eclipse'
EXTRA = ('S1s', 'R3s', 'R3s+', 'T70', 'N2s', 'N3s')


def holders(race):
    J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
    h = {}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                h.setdefault(c['runner'], set()).add(rid)
    D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
    for run, data in D.items():
        cs = {**S.cases(data), **SN.cases(data)}
        for k in EXTRA:
            if k in cs:
                h.setdefault(run, set()).add(k)
    return J['runners'], h


def main():
    data = [(race, win, *holders(race)) for race, win in S.RACES]
    mine = next(h for race, win, runners, hh in data if race == WIN_RACE for r, h in hh.items() if WIN in r)
    items = sorted(mine)
    print('Silva Eclipse items:', ', '.join(items), f'({len(data)} result races)')
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
