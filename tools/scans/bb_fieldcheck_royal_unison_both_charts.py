"""Field check (15 Nov 2026, from Catterick Wotever Next Saturn): H Regulus – H Saturn Dec 33.5440 / S Saturn → H Saturn RA 33.584453 =
crossed ratio 1.001207 unison (94.0); J Regulus – J Saturn Dec 33.6851 / S Saturn → J Saturn RA 33.460658 = 1.006709 unison (66.5).
U1 the same royal star R: natal R – X in BOTH charts has a same-body or crossed ratio on unison (scored).
U2 U1 with crossed ratios in both charts.
U3 the same royal star R, both charts, a same-body or crossed ratio on the same interval (any interval) in both.
U4 any royal star(s) (may differ), both charts with a unison ratio.
Also printed per holder: H X – J X (how close the two natal X are; a Saturn-return-like pair makes both charts automatic)."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
V = ('U1', 'U2', 'U3', 'U4'); tot = {v: [0, 0, 0.0] for v in V}
def ivs(r, kinds=('r', 'x')):
    out = []
    for k in kinds:
        t, s = r[k + 't'], r[k + 's']
        if E.num(s) and t and t not in ('no target',) and 'cut' not in str(t):
            out.append((k, str(t).split(' ')[0], s))
    return out
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            hj = '; '.join(f"{x['plane']} {x['v']:.4f}" for x in b.lines(f'H {X} – J {X}'))
            uni = {c: [] for c in 'HJ'}
            for R in E.ROY:
                rows = {c: [x for _, R2, x in b.star_rows(c) if R2 == R] for c in 'HJ'}
                I = {c: [(k, t, s, x) for x in rows[c] for k, t, s in ivs(x)] for c in 'HJ'}
                for c in 'HJ': uni[c] += [(R, k, s, x) for k, t, s, x in I[c] if t == '1']
                u = {c: [i for i in I[c] if i[1] == '1'] for c in 'HJ'}
                tag = f"{runner} {X} {R} [H X – J X {hj}]"
                if u['H'] and u['J']:
                    hold['U1'].add(runner); ex['U1'].append(tag + ' ' + ' | '.join(f"{c} {i[3]['plane']} {i[0]} {i[2]}" for c in 'HJ' for i in u[c]))
                    if any(i[0] == 'x' for i in u['H']) and any(i[0] == 'x' for i in u['J']): hold['U2'].add(runner); ex['U2'].append(tag)
                common = {i[1] for i in I['H']} & {i[1] for i in I['J']}
                if common: hold['U3'].add(runner); ex['U3'].append(tag + ' on ' + ','.join(sorted(common)))
            if uni['H'] and uni['J']: hold['U4'].add(runner); ex['U4'].append(f"{runner} {X} H {sorted({u[0] for u in uni['H']})} J {sorted({u[0] for u in uni['J']})}")
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}")
        if v in ('U1', 'U2'):
            for t in ex[v]: print('    ', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
