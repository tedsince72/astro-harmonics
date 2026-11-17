"""Combinations of Ring The Moon's rules (Ffos Las 17:25 23 Mar 2022; 17 Nov 2026; read-only). Rule holders from each race's bbrules json
(watch-only left out), plus the looser loop L3 (bb_fieldcheck_ringthemoon_loose) and the shared-pair T2 (bb_fieldcheck_ringthemoon).
Every pair and triple of the winner's items: picks / won / by chance over the result races; listed when 2+ winners or all holders won."""
import json, sys, os, itertools
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_fieldcheck_ringthemoon as RM
import bb_fieldcheck_ringthemoon_loose as RL
WIN_RACE, WIN = '20220323_ffos_las_1725', 'Ring The Moon'


def holders(race):
    J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
    h = {}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                h.setdefault(c['runner'], set()).add(rid)
    f = f'docs/eddie_read/depth/{race}_depth.json'
    if os.path.exists(f):
        for r in json.load(open(f))['runners']:
            if RL.holds(r, RL.V['L3 ends any score']):
                h.setdefault(r['runner'], set()).add('L3')
            if 'T2' in RM.runner_tags(r):
                h.setdefault(r['runner'], set()).add('T2')
    return J['runners'], h


def main():
    data = [(race, win, *holders(race)) for race, win in RM.RACES]
    mine = next(h for race, win, runners, hh in data if race == WIN_RACE for r, h in hh.items() if WIN in r)
    items = sorted(mine)
    print('Ring The Moon items:', ', '.join(items))
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
