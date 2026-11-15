"""Field check (15 Nov 2026, from Catterick Wotever Next Rahu): S Regulus – S Rahu Dec 6.4662 4×φ (81.8); J Regulus – J Rahu RA 166.9793
ninth 166.667 (6.2), same-body ratio 11/6 (33.5), carried by S Rahu – S Haumea RA 166.8023 ninth (59.3); S Haumea → J Rahu Dec
contraparallel 0.0661 (78.0).
Q1 a royal line c R – c X (family, not conj / cp) carried by a sky line naming X, S X – S Y (Y not a royal star, not the Moon, the line not
   conj / cp), and Y on natal X in the SAME chart (S Y → c X scoring; conj / cp count).  (BB55 is the other-chart version.)
Q2 Q1 + R on sky X (S R – S X a family, not conj / cp).
Q3 Q2 + the royal row has a same-body ratio on a target.
Q4 Q1 with S Y → c X not conj / cp."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); fam = lambda r: bool(r['fam']) and r['fam'] not in CJ
def rat(r): return E.num(r['rs']) and r['rt'] not in (None, 'no target') and 'cut' not in str(r['rt'])
V = ('Q1', 'Q2', 'Q3', 'Q4'); tot = {v: [0, 0, 0.0] for v in V}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c, R, row in b.star_rows(scoring=True):
                if not fam(row): continue
                for s, A, B in b.pairs_on(row):
                    if X not in (A, B) or not fam(s): continue
                    Y = B if A == X else A
                    if Y in E.ROY or Y == 'Moon': continue
                    on = [o for o in b.to_natal(Y, c) if o['fam']]
                    if not on: continue
                    t = f"{runner} {X}: {row['line']} {row['plane']} {row['v']:.4f} {row['tgt']} ({row['sc']}) by {s['line']} {s['plane']}; {Y} → {c} {X} {on[0]['plane']} {on[0]['v']:.4f} {on[0]['fam']} ({on[0]['sc']})"
                    hold['Q1'].add(runner); ex['Q1'].append(t)
                    if any(fam(o) for o in on): hold['Q4'].add(runner)
                    if any(fam(o) for o in b.sky_y(R)):
                        hold['Q2'].add(runner); ex['Q2'].append(t)
                        if rat(row): hold['Q3'].add(runner); ex['Q3'].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}")
        if v in ('Q2', 'Q3'):
            for t in sorted(set(ex[v])): print('    ', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
