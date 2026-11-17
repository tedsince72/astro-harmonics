"""Field check (17 Nov 2026, Eddie's Nelson River Chiron lines, Leicester 14:45 17 Feb 2022; read-only; picks / won / by chance).
H Regulus – H Chiron RA 166.5684 ninth 166.667 (70.5) and Dec 13.3237 ninth 13.3333 (63.8); the RA line carried by S Rahu – S Antares RA
166.7918 (62.5), the Dec line by S Eris – S Regulus Dec 13.3130 (23.8); S Regulus – S Chiron RA 144.0191 89×φ (56.5).
  Q0  one royal star R on natal X in RA and in Dec, same chart, both lines in a number family (no conj / cp / opposition)
  Q1  Q0 with both lines carried by a sky pair ('Sky lines on the same target', S A – S B, number family)
  Q2  Q1 with one carrier pair holding R itself (S Y – S R)
  Q3  Q2 with R on sky X (S R – S X in Other, number family)
  Q1r Q1 with R on sky X (Q3 without the same-star carrier)
Runner-level; races = bb_fieldcheck_samenum.RACES + Leicester 14:45 2022."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_samenum as SN
RACES = SN.RACES + [('20220217_leicester_1445', 'Nelson River')]
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['Q0', 'Q1', 'Q2', 'Q3', 'Q1r']


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        for c in 'HJ':
            for Rs in R.ROY:
                ln = {p: [x for x in d['L'] if x['line'] == f'{c} {Rs} – {c} {X}' and x['plane'] == p and ok(x)] for p in ('RA', 'Dec')}
                if not (ln['RA'] and ln['Dec']):
                    continue
                a, b = ln['RA'][0], ln['Dec'][0]
                car = {p: [s for s in d['S'] if s.get('match') == f"{x['line']} {p}" and ok(s) and ' – ' in s['line'] and '→' not in s['line']]
                       for p, x in (('RA', a), ('Dec', b))}
                t = (f"{X}: {a['line']} RA {a['v']:.4f} {a['tgt']} ({a['sc']}) / Dec {b['v']:.4f} {b['tgt']} ({b['sc']})")
                out.setdefault('Q0', []).append(t)
                if not (car['RA'] and car['Dec']):
                    continue
                t += f"; RA by {car['RA'][0]['line']} ({car['RA'][0]['sc']}), Dec by {car['Dec'][0]['line']} ({car['Dec'][0]['sc']})"
                out.setdefault('Q1', []).append(t)
                same = any(f'S {Rs}' in s['line'].split(' – ') for p in car for s in car[p])
                onsky = [o for o in d['O'] if ok(o) and set(o['line'].split(' – ')) == {f'S {Rs}', f'S {X}'}]
                if onsky:
                    out.setdefault('Q1r', []).append(t + f"; {onsky[0]['line']} {onsky[0]['plane']} {onsky[0]['tgt']} ({onsky[0]['sc']})")
                if same:
                    out.setdefault('Q2', []).append(t)
                    if onsky:
                        out.setdefault('Q3', []).append(t + f"; {onsky[0]['line']} {onsky[0]['plane']} {onsky[0]['tgt']} ({onsky[0]['sc']})")
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
            for k in ('Q3', 'Q2', 'Q1r'):
                if k in cs:
                    print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}"); break
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
