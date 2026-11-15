"""Field check (15 Nov 2026, from Catterick Wotever Next Neptune): S Fomalhaut – S Neptune Dec 25.9938 whole 26 (69.1);
H Fomalhaut – H Neptune RA 3.9924 whole 4 (62.0) and its same-body ratio 3.9924 / S Neptune → H Neptune RA 6.040865 = 1.513095 3/2 (34.5);
J Fomalhaut – J Neptune RA 59.8941 37×φ (17.3) and same-body ratio 59.8941 / 69.930687 = 1.167573 7/6 (48.2).
N1 a royal star R on sky X (S R – S X a family, not conj / cp), and in BOTH charts one R – X row has a family (not conj / cp) AND a
   same-body ratio on a target on that same row.
N2 N1 with the same plane in both charts.
N3 N1 without the sky condition (both charts only).
N4 N1 with the same-body or crossed ratio."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); fam = lambda r: bool(r['fam']) and r['fam'] not in CJ
def rat(r, k): return E.num(r[k + 's']) and r[k + 't'] not in (None, 'no target') and 'cut' not in str(r[k + 't'])
V = ('N1', 'N2', 'N3', 'N4'); tot = {v: [0, 0, 0.0] for v in V}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for R in E.ROY:
                sky = any(fam(o) for o in b.sky_y(R))
                ok = {c: [x for _, R2, x in b.star_rows(c) if R2 == R and fam(x) and rat(x, 'r')] for c in 'HJ'}
                ok4 = {c: [x for _, R2, x in b.star_rows(c) if R2 == R and fam(x) and (rat(x, 'r') or rat(x, 'x'))] for c in 'HJ'}
                t = f"{runner} {X} {R}: " + ' | '.join(f"{x['line']} {x['plane']} {x['v']:.4f} {x['tgt']} ({x['sc']}) r {x['rt']} ({x['rs']})" for c in 'HJ' for x in ok[c])
                if ok['H'] and ok['J']:
                    hold['N3'].add(runner); ex['N3'].append(t)
                    if sky:
                        hold['N1'].add(runner); ex['N1'].append(t)
                        if {x['plane'] for x in ok['H']} & {x['plane'] for x in ok['J']}: hold['N2'].add(runner); ex['N2'].append(t)
                if sky and ok4['H'] and ok4['J']: hold['N4'].add(runner); ex['N4'].append(f'{runner} {X} {R}')
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}")
        if v in ('N1', 'N2', 'N3'):
            for t in ex[v]: print('    ', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
