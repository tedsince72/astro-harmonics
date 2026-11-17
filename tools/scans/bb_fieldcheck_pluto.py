"""Field check (17 Nov 2026, Eddie: 'another Pluto S to J, S to H'; read-only; picks / won / by chance over the result races).
Wholestone: S Pluto → J Pluto RA 66.6385 ninth 66.6667 (78.86) and Dec 17.9960 18 (80.08); Arvico Bleu: S Pluto → J Pluto RA 59.8664 37×φ (97.48).
  P0     S Pluto → H / J Pluto in a number family (no conj / cp / opposition), any score
  P50    P0 >= 50;  P80  P0 >= 80
  P2     S Pluto → c Pluto in both planes, same chart, number family, any score
  P2_50  P2 with both >= 50
  X2_50  control: any body X with S X → c X in both planes, same chart, both >= 50 (Pluto not required)
Runner-level; races = bb_fieldcheck_arvico.RACES + Haydock 14:05 19 Feb 2022."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_arvico as A
RACES = list(A.RACES) + [('20220219_haydock_1405', 'Wholestone')]
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['P0', 'P50', 'P80', 'P2', 'P2_50', 'X2_50']


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        for c in 'HJ':
            ls = {x['plane']: x for x in d['L'] if x['line'] == f'S {X} → {c} {X}' and ok(x)}
            if not ls:
                continue
            t = f'{X} {c}: ' + '; '.join(f"{p} {x['v']:.4f} {x['tgt']} ({x['sc']})" for p, x in ls.items())
            both = len(ls) == 2
            b50 = both and min(x['sc'] for x in ls.values()) >= 50
            if b50: out.setdefault('X2_50', []).append(t)
            if X != 'Pluto':
                continue
            out.setdefault('P0', []).append(t)
            m = max(x['sc'] for x in ls.values())
            if m >= 50: out.setdefault('P50', []).append(t)
            if m >= 80: out.setdefault('P80', []).append(t)
            if both: out.setdefault('P2', []).append(t)
            if b50: out.setdefault('P2_50', []).append(t)
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
            if 'P2' in cs:
                print(f"  [P2] {race} {run}{' WON' if win in run else ''}: {cs['P2'][0]}")
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws) if k != "X2_50" else ""}')


if __name__ == '__main__':
    main()
