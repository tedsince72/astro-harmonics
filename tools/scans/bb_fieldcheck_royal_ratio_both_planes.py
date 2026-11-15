"""Field check (15 Nov 2026, from Catterick Wotever Next Makemake): J Aldebaran – J Makemake RA 100.7310 (no family) same-body ratio
3.499665 on 7/2 (93.6); Dec 19.4043 12×φ (62.7) carried by S Neptune – S Haumea Dec 19.4187 (93.0), same-body ratio 1.49784 on 3/2 (89.2),
crossed 1.483331 3/2 (16.7); S Aldebaran – S Makemake Dec 6.4519 4×φ (37.5); S Makemake → J Makemake Dec 12.9549 8×φ (67.3) carried by
S Juno – S Chiron Dec 12.9664 (31.8); S Regulus – S Makemake Dec 10.9932 11 (66.1) with H Regulus – H Makemake RA 44.0171 44 (14.5).
F1 the same royal star R on natal X in one chart has a same-body (or crossed) ratio on a target in BOTH planes (RA row and Dec row), and at
   least one of the two rows scores in a family (not conj / cp).
F2 F1 + R on sky X (S R – S X a family, not conj / cp).
F3 F1 + a family row of the two carried by a sky pair not naming X (no Moon).
F4 F2 + F3.
F5 F1 with same-body ratios only (no crossed).
G1 (Regulus part) a royal star R on sky X and on natal X (either chart), both whole, the natal target a multiple 2-9 of the sky one (or equal)."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('F1', 'F2', 'F3', 'F4', 'F5', 'G1'); tot = {v: [0, 0, 0.0] for v in V}
def on_t(r, keys):
    return any(E.num(r.get(k)) and r.get(t) not in (None, 'no target') and 'cut' not in str(r.get(t)) for k, t in keys)
SB, BOTH = (('rs', 'rt'),), (('rs', 'rt'), ('xs', 'xt'))
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c in 'HJ':
                for R in E.ROY:
                    rows = {x['plane']: x for cc, RR, x in b.star_rows(c) if RR == R and x['plane'] in ('RA', 'Dec')}
                    if len(rows) < 2: continue
                    fam = [x for x in rows.values() if x['fam'] and x['fam'] not in CJ]
                    if not fam: continue
                    t = f"{runner} {X} {c} {R}: " + ' | '.join(f"{p} {x['v']:.4f} {x['tgt']} sb {x['rt']} x {x['xt']}" for p, x in rows.items())
                    f1 = all(on_t(x, BOTH) for x in rows.values()); f5 = all(on_t(x, SB) for x in rows.values())
                    if not f1: continue
                    f2 = any(o['fam'] and o['fam'] not in CJ for o in b.sky_y(R))
                    f3 = any(X not in (A, B) and 'Moon' not in (A, B) for x in fam for s, A, B in b.pairs_on(x))
                    for v, ok in (('F1', 1), ('F2', f2), ('F3', f3), ('F4', f2 and f3), ('F5', f5)):
                        if ok: hold[v].add(runner); ex[v].append(t)
            for R in E.ROY:
                for o in b.sky_y(R):
                    if o['fam'] != 'whole': continue
                    for cc, RR, x in b.star_rows(scoring=True):
                        if RR == R and x['fam'] == 'whole' and int(x['tgt']) % int(o['tgt']) == 0 and int(x['tgt']) // int(o['tgt']) <= 9:
                            hold['G1'].add(runner); ex['G1'].append(f"{runner} {X}: {o['line']} {o['plane']} {o['tgt']} / {x['line']} {x['plane']} {x['tgt']}")
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('F4', 'G1'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')

# F6 F1 + in one plane the royal row and the same-body line S X -> c X score in the SAME family (the ratio on a target follows from the
#    two targets, e.g. 12×φ / 8×φ = 3/2). F7 F6 + R on sky X (as F2).
print('--- F6 / F7')
tot = {'F6': [0, 0, 0.0], 'F7': [0, 0, 0.0]}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); h = {'F6': set(), 'F7': set()}; ex = []
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c in 'HJ':
                for R in E.ROY:
                    rows = {x['plane']: x for cc, RR, x in b.star_rows(c) if RR == R and x['plane'] in ('RA', 'Dec')}
                    if len(rows) < 2 or not all(on_t(x, BOTH) for x in rows.values()): continue
                    ok = False
                    for p, x in rows.items():
                        if not x['fam'] or x['fam'] in CJ or not on_t(x, SB): continue
                        sb = [o for o in b.same_body(c, p) if o['fam'] == x['fam']]
                        if sb: ok = True; ex.append(f"{run} {X} {c} {R} {p} {x['tgt']} / {sb[0]['line']} {sb[0]['tgt']} = {x['rt']}")
                    if ok:
                        h['F6'].add(run)
                        if any(o['fam'] and o['fam'] not in CJ for o in b.sky_y(R)): h['F7'].add(run)
    for v in h:
        won = bool(w) and any(w in x for x in h[v])
        if w and h[v]: tot[v][0] += len(h[v]); tot[v][1] += won; tot[v][2] += len(h[v]) / N
        print(n, v, f"{len(h[v])}/{N}", 'W' if won else '', sorted(h[v]))
    for t in sorted(set(ex)): print('   ', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
