"""Field check (15 Nov 2026, from Catterick Wotever Next Neptune): H Regulus – H Neptune Dec 18.0001 whole 18 (99.5) carried by
S Venus – S Vesta RA 17.9953 (and S Sun – S Moon Dec 17.9815); S Venus → H Neptune Dec 4.8551 3×φ (96.9). J Aldebaran – J Neptune RA
144.4702 ninth (91.1) carried by S Pluto – S Orcus RA 144.7260; S Pluto → J Neptune RA 16.1635 10×φ (47.9). S Sun → J Neptune RA 90.6269 56×φ.
P1 in each chart c a scoring royal line c R – c X (not conj / cp; any royal star) carried by a sky pair (not naming X) with an end E on
   natal X in the same chart (S E → c X scoring, not conj / cp, any plane). Moon allowed as the other end, E not the Moon.
P2 P1 with different royal stars in the two charts.
P3 P1 + an end of a horse-side carrying pair lands on J X, or an end of a jockey-side pair lands on H X (crossing over; any end, not the Moon).
P4 P1 with the end-on-X lines scoring >= 50 in both charts."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); ok = lambda rs: [o for o in rs if o['fam'] and o['fam'] not in CJ]
V = ('P1', 'P2', 'P3', 'P4'); tot = {v: [0, 0, 0.0] for v in V}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            side = {}
            for c in 'HJ':
                oc = 'J' if c == 'H' else 'H'; L = []
                for _, R, row in b.star_rows(c, scoring=True):
                    if row['fam'] in CJ: continue
                    for s, A, B in b.pairs_on(row):
                        if X in (A, B): continue
                        for e in (A, B):
                            if e == 'Moon' or e in E.ROY: continue
                            on = ok(b.to_natal(e, c))
                            if on:
                                cross = [f for f in (A, B) if f != 'Moon' and f not in E.ROY and ok(b.to_natal(f, oc))]
                                L.append((R, row, s, e, max(o['sc'] for o in on), on[0], cross))
                side[c] = L
            if side['H'] and side['J']:
                t = f"{runner} {X}: " + ' || '.join(f"{c} {R} {row['plane']} {row['v']:.4f} {row['tgt']} by {s['line']} {s['plane']}; {e} → {c} {X} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})" for c in 'HJ' for R, row, s, e, m, o, cr in side[c][:1])
                hold['P1'].add(runner); ex['P1'].append(t)
                if {x[0] for x in side['H']} != {x[0] for x in side['J']} or len({x[0] for x in side['H']} | {x[0] for x in side['J']}) > 1:
                    if any(a[0] != c_[0] for a in side['H'] for c_ in side['J']): hold['P2'].add(runner)
                if any(x[6] for c in 'HJ' for x in side[c]): hold['P3'].add(runner); ex['P3'].append(f'{runner} {X}')
                if max(x[4] for x in side['H']) >= 50 and max(x[4] for x in side['J']) >= 50: hold['P4'].add(runner); ex['P4'].append(f'{runner} {X}')
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}")
    for t in ex['P1']:
        if 'Catterick' in n: print('    ', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
