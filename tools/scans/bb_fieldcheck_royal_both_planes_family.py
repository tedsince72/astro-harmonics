"""Field check (15 Nov 2026, from Fontwell 15:30 2023 Kilcummin Pallas): J Antares – J Pallas RA 77.6974 ninth 77.7778 (48.3), crossed
ratio vs S Pallas -> J Pallas Dec 4.5726 = 16.9918 on 17 (90.3); J Antares – J Pallas Dec 24.9984 25 (92.2); S Antares – S Pallas RA
54.9823 55 (11.4). (S Antares – S Pallas RA + S Pallas -> J Pallas RA = 54.9823 + 22.7148 = 77.6971 ~ J Antares – J Pallas RA: geometry.)
A1 the same royal star R on natal X in one chart scores in a family (not conj / cp) in BOTH RA and Dec.
A2 A1 + a same-body or crossed ratio on a target on one of the two rows (whole 10-20 'cut' targets counted).
A3 A1 + R on sky X: S R – S X scores in a family (any score, not conj / cp).
A4 A2 + A3."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('A1', 'A2', 'A3', 'A4'); tot = {v: [0, 0, 0.0] for v in V}
def on_t(x):
    return any(E.num(x.get(k)) and x.get(t) not in (None, 'no target') for k, t in (('rs', 'rt'), ('xs', 'xt')))
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c in 'HJ':
                for R in E.ROY:
                    rows = {x['plane']: x for cc, RR, x in b.star_rows(c) if RR == R and x['plane'] in ('RA', 'Dec')
                            and x['fam'] and x['fam'] not in CJ}
                    if len(rows) < 2: continue
                    a2 = any(on_t(x) for x in rows.values())
                    a3 = any(o['fam'] and o['fam'] not in CJ for o in b.sky_y(R))
                    t = f"{run} {X} {c} {R}: " + ' | '.join(f"{p} {x['v']:.4f} {x['tgt']} ({x['sc']})" for p, x in rows.items())
                    for v, ok in (('A1', 1), ('A2', a2), ('A3', a3), ('A4', a2 and a3)):
                        if ok: hold[v].add(run); ex[v].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for t in sorted(set(ex['A4'])): print('   A4', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 7 result races: {p} picks, {wn} won, {c:.1f} by chance')

# A5 A4 with the ratio on a target a CROSSED one. A6 A1 + S R – S X whole and one of the two natal rows whole, the two targets in a
#    ratio on the interval list (exact on the targets: 55 / 25 = 11/5).
print('--- A5 / A6')
from fractions import Fraction as F
IV = {F(1), F(2), F(3, 2), F(4, 3), F(3), F(4), F(5, 4), F(6, 5), F(5, 3), F(8, 5), F(5, 2), F(8, 3), F(9, 4), F(9, 8), F(16, 9), F(9, 5),
      F(15, 8), F(16, 15), F(7, 4), F(7, 3), F(7, 2), F(7, 5), F(7, 6), F(8, 7), F(5), F(6), F(7), F(8), F(9), F(11, 5), F(11, 6), F(11, 3),
      F(11, 8), F(11, 4), F(13, 5), F(13, 8), F(13, 4)}
tot = {'A5': [0, 0, 0.0], 'A6': [0, 0, 0.0]}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); h = {'A5': set(), 'A6': set()}; ex = []
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c in 'HJ':
                for R in E.ROY:
                    rows = {x['plane']: x for cc, RR, x in b.star_rows(c) if RR == R and x['plane'] in ('RA', 'Dec')
                            and x['fam'] and x['fam'] not in CJ}
                    if len(rows) < 2: continue
                    sky = [o for o in b.sky_y(R) if o['fam'] and o['fam'] not in CJ]
                    if sky and any(E.num(x.get('xs')) and x.get('xt') not in (None, 'no target') for x in rows.values()):
                        h['A5'].add(run)
                    for o in sky:
                        for x in rows.values():
                            if o['fam'] == x['fam'] == 'whole':
                                a, bb = sorted((int(o['tgt']), int(x['tgt'])))
                                if F(bb, a) in IV:
                                    h['A6'].add(run); ex.append(f"{run} {X} {c} {R}: {o['plane']} {o['tgt']} / {x['plane']} {x['tgt']}")
    for v in h:
        won = bool(w) and any(w in x for x in h[v])
        if w and h[v]: tot[v][0] += len(h[v]); tot[v][1] += won; tot[v][2] += len(h[v]) / N
        print(f"{n} {v}: {len(h[v])}/{N}{' W' if won else ''}  {sorted(h[v])}")
    for t in sorted(set(ex)): print('   A6', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 7 result races: {p} picks, {wn} won, {c:.1f} by chance')
