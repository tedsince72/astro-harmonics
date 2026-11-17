"""Field check (17 Nov 2026, Eddie: 'and same number'; read-only; picks / won / by chance over the result races).
Wholestone Pluto: H Fomalhaut – H Pluto RA 66.6744 ninth 66.6667 (94.2) on the same number as S Pluto → J Pluto RA 66.6385 (78.86) - a royal
natal line on X and the same-body line S X → natal X on one family + target.
  N0   a natal royal line c R – c X and a same-body line S X → H X or J X (any chart, any plane) in the same number family on the same target
  N0x  N0 with the same-body line in the other chart (as Wholestone)
  N50  N0 with both >= 50;  N50x  N0x with both >= 50
  N70  N0 with both >= 70;  N70x  N0x with both >= 70
  NP   N50 on Pluto
Runner-level; races = bb_fieldcheck_pluto.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_pluto as P
RACES = P.RACES
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['N0', 'N0x', 'N50', 'N50x', 'N70', 'N70x', 'NP']


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        sb = [x for x in d['L'] if x['line'] in (f'S {X} → H {X}', f'S {X} → J {X}') and ok(x)]
        roy = [x for x in d['L'] if ' – ' in x['line'] and x['line'][0] in 'HJ' and ok(x) and x['line'].split(' – ')[0][2:] in R.ROY]
        for r in roy:
            for s in sb:
                if r['fam'] != s['fam'] or str(r['tgt']) != str(s['tgt']):
                    continue
                cross = r['line'][0] != s['line'].split(' → ')[1][0]
                t = f"{X}: {r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']}) = {s['line']} {s['plane']} {s['v']:.4f} ({s['sc']})"
                m = min(r['sc'], s['sc'])
                for k, c in (('N0', True), ('N0x', cross), ('N50', m >= 50), ('N50x', cross and m >= 50), ('N70', m >= 70),
                             ('N70x', cross and m >= 70), ('NP', X == 'Pluto' and m >= 50)):
                    if c: out.setdefault(k, []).append(t)
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for race, win in RACES:
        D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        N = len(D)
        for run, data in D.items():
            cs = cases(data)
            for k in KEYS:
                if k in cs:
                    t = tot[k]; t[0] += 1; t[1] += win in run; t[2] += 1 / N
                    if win in run: t[3].append(f'{race} {run}')
            if 'N70x' in cs:
                print(f"  [N70x] {race} {run}{' WON' if win in run else ''}: {cs['N70x'][0]}")
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
