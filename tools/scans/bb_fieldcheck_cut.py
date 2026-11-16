"""Field check (16 Nov 2026, Eddie: 'something in this', Little Girl Blue Uranus, Bath 17:50 3 Jun 2022, won 10/1). Read-only; winners named
below, no results file read. 16 result races, bybody xlsx.
Little Girl Blue: S Uranus -> H Uranus Dec 4.2369 phi^3 (87.0); H Fomalhaut - H Uranus RA 46.6345 (no family) / that Dec line = crossed ratio
11.00675 on 11 '1/11 cut' (87.73); S Uranus -> J Uranus RA 135.9089 84xphi (81.5).
'cut' = a royal-line ratio (same-body or crossed, as in the bybody sheets) on a whole number 10-20 ('1/n cut').
 U0   a royal line c R - c X (any score, no family allowed; not conj / cp) with a cut scoring >= 80
 U1   U0 and the same-body line it is measured against in a number family (not conj / cp / opposition)
 U2   U1 and the same body in the other chart (S X -> c' X) in a number family >= 80, any plane
 U3   U2 with the royal line itself in no family (Little Girl Blue's shape)
 U10  U0 on 10 only, royal line in no family (BB54 needs it scoring)"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_hub import RACES
NO = ('conj', 'contraparallel', 'opposition')
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
KEYS = ['U0', 'U1', 'U2', 'U3', 'U10']
num = lambda r: r['fam'] and r['fam'] not in NO and r['sc'] is not None


def cases(X, d):
    out = []
    for r in d['L']:
        if not any(f' {R} – ' in r['line'] for R in ROY) or r['plane'] not in ('RA', 'Dec'): continue
        if r['fam'] in ('conj', 'contraparallel'): continue
        c = r['line'][0]
        for t, s, base in ((r['rt'], r['rs'], f"{r['sb']} {r['plane']}" if r['sb'] else None), (r['xt'], r['xs'], r['xb'])):
            if not t or 'cut' not in str(t) or s is None or s < 80 or not base: continue
            n = int(str(t).split()[0])
            if not 10 <= n <= 20: continue
            name, pl = base.rsplit(' ', 1)
            b = [o for o in d['L'] if o['line'] == name and o['plane'] == pl]
            other = 'J' if c == 'H' else 'H'
            oth = [o for o in d['L'] if o['line'] == f'S {X} → {other} {X}' and num(o) and o['sc'] >= 80]
            tg = {'U0'}
            if n == 10 and not r['fam']: tg.add('U10')
            if b and num(b[0]):
                tg.add('U1')
                if oth:
                    tg.add('U2')
                    if not r['fam']: tg.add('U3')
            out.append((tg, f"{X}: {r['line']} {r['plane']} {r['v']:.4f} {r['tgt'] or 'no family'} / {base} = {t} ({s})"
                            + (f"; base {b[0]['tgt']} ({b[0]['sc']})" if b and b[0]['fam'] else '')
                            + (f"; other chart {oth[0]['line']} {oth[0]['plane']} {oth[0]['tgt']} ({oth[0]['sc']})" if oth else '')))
    return out


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            tg = set()
            for X, d in D.items():
                for t, s in cases(X, d):
                    tg |= t
                    if 'U2' in t: ex.append(f'{run} [{",".join(k for k in KEYS if k in t)}] {s}')
            for k in tg: held[k].append(run)
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex: print('    ', x)
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
