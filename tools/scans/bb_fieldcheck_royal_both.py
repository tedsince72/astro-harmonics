"""Field check (16 Nov 2026, Eddie's Dynamic Force Jupiter lines; Nottingham 15:30 1 Jun 2022, won 18/1): Antares on both natal
Jupiters in RA - H Antares - H Jupiter RA 16.1680 10xphi (61.8), carried by S Aldebaran - S Jupiter Dec 16.1801 (99.3), same-body ratio
100.175487 / 16.167965 = 6.1959 (no target; Eddie: '6.18 is close'); J Antares - J Jupiter RA 58.0434 (no family), same-body ratio
174.387093 / 58.043406 = 3.004426 on 3 (77.9). Read-only; winners named below, no results file read. 17 result races, bybody xlsx.
R = a royal star; the R - X natal line in each chart, same plane (cells from the X sheet, 'L').
 A0   R on natal X in both charts, same plane, and one of the two lines has a same-body ratio on a target scoring >= 50
 A1   A0 and the other chart's R - X line (same plane) is in a number family and carried by a sky pair (S row on its family + target)
      scoring >= 90
 A2   A1 with the carrying pair naming sky X itself (S X - S Y)
 A1j / A2j  the same with X = Jupiter"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_sbcount import RACES
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
NO = ('conj', 'contraparallel', 'opposition')
KEYS = ['A0', 'A1', 'A2', 'A0j', 'A1j', 'A2j']


def cases(X, d):
    out = []
    for R in ROY:
        for pl in ('RA', 'Dec'):
            ln = {c: next((r for r in d['L'] if r['line'] == f'{c} {R} – {c} {X}' and r['plane'] == pl), None) for c in 'HJ'}
            if not all(ln.values()):
                continue
            for a, o in (('H', 'J'), ('J', 'H')):
                ra, ro = ln[a], ln[o]
                if not (ra.get('rs') is not None and ra['rs'] >= 50):
                    continue
                tg = {'A0'}
                car = []
                if ro['fam'] and ro['fam'] not in NO and ro['sc'] is not None:
                    car = [s for s in d['S'] if ' – ' in s['line'] and ' → ' not in s['line'] and s.get('match') == f"{ro['line']} {pl}" and s['sc'] is not None and s['sc'] >= 90
                           and s['fam'] not in NO]
                if car:
                    tg.add('A1')
                    if any(f'S {X} – ' in s['line'] or s['line'].endswith(f'– S {X}') for s in car):
                        tg.add('A2')
                out.append((tg, f"{R} {pl}: {ra['line']} {ra['v']:.4f} ratio {ra['r']:.6f} {ra['rt']} ({ra['rs']}); {ro['line']} {ro['v']:.4f} "
                                 f"{ro['tgt']} ({ro['sc']})" + (f" by {car[0]['line']} {car[0]['plane']} ({car[0]['sc']})" if car else '')))
    return out


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: set() for k in KEYS}; ex = []
        for run, D in data.items():
            for X, d in D.items():
                for tg, txt in cases(X, d):
                    for k in tg:
                        held[k].add(run)
                        if X == 'Jupiter': held[k + 'j'].add(run)
                    if 'A1' in tg: ex.append(f"{run} {X} [{' '.join(sorted(tg))}] {txt}")
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(sorted(held[k]))}")
        for x in ex: print('   ', x)
    print('\n## Totals (picks, won, by chance)')
    for k in KEYS: print(f"  {k}: {tot[k][0]} picks, {tot[k][1]} won, {tot[k][2]:.1f} by chance")


if __name__ == '__main__':
    main()
