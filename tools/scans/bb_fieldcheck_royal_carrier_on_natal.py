"""Field check (15 Nov 2026, from Newcastle AW 16:33 2021 Athmad Makemake): H Regulus – H Makemake RA 42.3642 10φ³ (94.5) carried by
S Mars – S Makemake RA 42.3978 10φ³ (41.5), Mars on natal Makemake S Mars -> H Makemake RA 39.9914 40 (57.1); H Regulus – H Makemake Dec
13.3363 ninth 13.3333 (88.7) carried by S Venus – S Regulus RA 13.3078 (4.4), Venus on natal Makemake S Venus -> H Makemake RA 29.0670
φ⁷ (25.1); S Makemake -> H Makemake Dec 2.4133 silver (74.8); S Haumea – S Makemake Dec 7 (91.6), RA 18 (85.1).
C1 a royal line c R – c X in a family (not conj / cp) carried by S X – S Y (same target; Y not royal, not the Moon; the sky line not
   conj / cp), and S Y -> c X scores in a family (any family, not conj / cp). (= BB59 without R on sky X.)
C2 C1 + the same royal star on natal X in the other plane also scores in a family.
C3 C2 + that other-plane line carried by a sky pair (any pair, not the Moon) with an end Z (not R) where S Z -> c X scores in a family.
C4 R on natal X in a family in both planes, each line carried by a sky pair (not the Moon) with an end Y (not R, not X) where S Y -> c X
   scores in a family.
C5 C4 + a sky body Y on sky X (S Y – S X in a family, not conj / cp) in both planes."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('C1', 'C2', 'C3', 'C4', 'C5'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda x: x.get('fam') and x['fam'] not in CJ
def on_natal(b, Y, c):
    return [o for o in b.to_natal(Y, c) if fam(o)]
def carriers(b, row, c, R, X):
    """ends Y (not R, not X, not Moon) of sky pairs carrying row, with S Y -> c X in a family"""
    out = set()
    for s, A, B in b.pairs_on(row):
        if 'Moon' in (A, B) or not fam(s): continue
        for Y in (A, B):
            if Y not in (R, X) and on_natal(b, Y, c): out.add(Y)
    return out
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c in 'HJ':
                for R in E.ROY:
                    rows = {x['plane']: x for cc, RR, x in b.star_rows(c) if RR == R and x['plane'] in ('RA', 'Dec') and fam(x)}
                    for p, x in rows.items():
                        c1 = set()
                        for s, A, B in b.pairs_on(x):
                            if X not in (A, B) or not fam(s): continue
                            Y = B if A == X else A
                            if Y in E.ROY or Y == 'Moon': continue
                            if on_natal(b, Y, c): c1.add(Y)
                        if not c1: continue
                        t = f"{run} {X} {c} {R} {p} {x['v']:.4f} {x['tgt']} via {sorted(c1)}"
                        hold['C1'].add(run); ex['C1'].append(t)
                        q = 'Dec' if p == 'RA' else 'RA'
                        if q in rows:
                            hold['C2'].add(run); ex['C2'].append(t)
                            if carriers(b, rows[q], c, R, X): hold['C3'].add(run); ex['C3'].append(t)
                    if len(rows) == 2:
                        cr = {p: carriers(b, x, c, R, X) for p, x in rows.items()}
                        if all(cr.values()):
                            t = f"{run} {X} {c} {R}: " + ' | '.join(f"{p} {x['v']:.4f} {x['tgt']} via {sorted(cr[p])}" for p, x in rows.items())
                            hold['C4'].add(run); ex['C4'].append(t)
                            ys = {}
                            for o in b.O:
                                ln = o.get('line', '')
                                if ln.startswith('S ') and ln.endswith(f' – S {X}') and fam(o):
                                    ys.setdefault(ln, set()).add(o['plane'])
                            if any({'RA', 'Dec'} <= v for v in ys.values()): hold['C5'].add(run); ex['C5'].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('C3', 'C5'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
