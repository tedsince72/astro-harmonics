"""Field check (16 Nov 2026, Athmad Saturn): J Fomalhaut – J Saturn Dec 18.9247 ninth 18.8889 (5.3), same-body ratio 2.4163 1+√2 (42.4)
against S Saturn -> J Saturn Dec 7.8321; carried by S Sun – S Eris Dec 18.8595 ninth 18.8889 (22.3); the Sun on sky Saturn
(S Sun – S Saturn RA 179.8166 opposition 180 (75.6)); Fomalhaut on sky Saturn (S Fomalhaut – S Saturn Dec 11.0920 φ⁵ (89.2)).
S1 a royal natal line c R – c X in a family (not conj / cp) carried by a sky pair S A – S B on its target (not naming X; no Moon; pair in a
   family), with an end A (not royal) on sky X (S A – S X / S X – S A in a family; opposition counts; not conj / cp).
S2 S1 + the same royal star R on sky X (S R – S X in a family).
S3 S2 + that royal row has a same-body or crossed ratio on a target (any score).
Read-only."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('S1', 'S2', 'S3'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda o: o.get('fam') and o['fam'] not in CJ
tg = lambda t: t and t != 'no target' and not str(t).startswith('conjunction')
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            sky = lambda A: [o for o in b.O if fam(o) and o['line'] in (f'S {A} – S {X}', f'S {X} – S {A}')]
            for c, R, row in b.star_rows(scoring=True):
                if not fam(row): continue
                for s, A, B in b.pairs_on(row):
                    if X in (A, B) or 'Moon' in (A, B) or not fam(s): continue
                    for Y in (A, B):
                        if Y in E.ROY or not sky(Y): continue
                        y = sky(Y)[0]
                        t = f"{run} {X}: {row['line']} {row['plane']} {row['tgt']} ({row['sc']}) via {s['line']} {s['plane']} ({s['sc']}); {y['line']} {y['plane']} {y['tgt']} ({y['sc']})"
                        hold['S1'].add(run); ex['S1'].append(t)
                        rr = sky(R)
                        if rr:
                            t2 = t + f"; {rr[0]['line']} {rr[0]['plane']} {rr[0]['tgt']} ({rr[0]['sc']})"
                            hold['S2'].add(run); ex['S2'].append(t2)
                            if tg(row.get('rt')) or tg(row.get('xt')):
                                hold['S3'].add(run); ex['S3'].append(t2 + f" | r {row.get('rt')} x {row.get('xt')}")
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for t in sorted(set(ex['S3'])): print('   S3', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
