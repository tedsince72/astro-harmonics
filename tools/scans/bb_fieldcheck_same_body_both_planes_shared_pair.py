"""Field check (15 Nov 2026, from Catterick Wotever Next Ceres): S Ceres → H Ceres RA 179.9663 opposition (95.5) carried by S Mercury –
S Makemake RA 179.5527 (40.4) (and S Venus – S Regulus RA); S Ceres → H Ceres Dec 41.3600 silver 41.4 (1.3) carried by S Ketu – S Makemake
Dec 41.3912 (51.5); shared Makemake: S Makemake – S Ceres Dec ninth (36.3), S Makemake → J Ceres Dec 3×φ (93.8); S Mercury → H Ceres Dec
silver 24.14; S Ketu – S Ceres RA 97×φ (97.0).
C1 the same-body line S X → c X scores in BOTH planes (same chart c; conj / cp not counted), each plane carried by a sky pair S A – S B on its
   target (not naming X, no Moon, no royal star), and the RA pair and the Dec pair share a body Y.
C2 C1 + Y on X (S Y – S X or S Y → H / J X scoring, any plane; conj / cp count).
C3 C2 + the other end of each pair on X too (any chart, any plane).
C1r = C1 allowing royal stars in the pairs."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('C1', 'C1r', 'C2', 'C3'); tot = {v: [0, 0, 0.0] for v in V}
def on_x(b, Y):
    return bool([o for o in b.sky_y(Y) if o['fam']] + [o for c in 'HJ' for o in b.to_natal(Y, c) if o['fam']])
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c in 'HJ':
                P = {}
                for pl in ('RA', 'Dec'):
                    rows = [x for x in b.same_body(c, pl) if x['fam'] and x['fam'] not in CJ]
                    P[pl] = [(x, s, {A, B}) for x in rows for s, A, B in b.pairs_on(x) if X not in (A, B) and 'Moon' not in (A, B)]
                for roy in (False, True):
                    pr = {pl: [p for p in P[pl] if roy or not (p[2] & set(E.ROY))] for pl in P}
                    for xr, sr, er in pr['RA']:
                        for xd, sd, ed in pr['Dec']:
                            for Y in (er & ed) - set(E.ROY):
                                t = f"{runner} {X} {c}: RA {xr['v']:.4f} {xr['tgt']} by {sr['line']} | Dec {xd['v']:.4f} {xd['tgt']} by {sd['line']} | shared {Y}"
                                hold['C1r' if roy else 'C1'].add(runner); ex['C1r' if roy else 'C1'].append(t)
                                if roy: continue
                                if on_x(b, Y):
                                    hold['C2'].add(runner); ex['C2'].append(t)
                                    others = [e for e in (er | ed) if e != Y]
                                    if all(on_x(b, e) for e in others): hold['C3'].add(runner); ex['C3'].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}")
        if v in ('C1', 'C2', 'C3'):
            for t in sorted(set(ex[v])): print('    ', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
