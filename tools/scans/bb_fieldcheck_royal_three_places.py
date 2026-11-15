"""Field check (15 Nov 2026, from Fontwell 15:30 2023 Kilcummin Chiron): Aldebaran on Chiron in all three places, all golden:
S Aldebaran – S Chiron RA 53.3821 33×φ (59.7), H Aldebaran – H Chiron Dec 12.9353 8×φ (72.4), J Aldebaran – J Chiron RA 113.2757 70×φ (59.0);
H line carried by S Chiron – S Makemake Dec 12.9214 (29.3) and S Mercury – S Orcus Dec 12.9737 (9.3); J line by S Moon – S Ceres RA 113.2319
(5.9); S Makemake → H Chiron RA 161.7904 100φ (94.7, also 100×φ golden); S Sun – S Chiron Dec 13.3404 ninth (73.4); S Moon → J Chiron RA 78 (97.1).
M1 the same royal star R scores on X in the sky (S R – S X), on H X (H R – H X) and on J X (J R – J X); conj / cp not counted; any plane each.
M2 M1 with all three in the same family.
M3 M1 + the H line and the J line each carried by a sky pair on its target ('Sky lines on the same target', not naming X; the Moon allowed).
M3n M3 without the Moon.
M4 M2 + M3."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell 15:30', '20231006_fontwell_1530', 'Kilcummin'), ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('M1', 'M2', 'M3', 'M3n', 'M4'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda x: x['fam'] and x['fam'] not in CJ
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for R in E.ROY:
                sk = [o for o in b.sky_y(R) if fam(o)]
                hh = [x for c, RR, x in b.star_rows('H', scoring=True) if RR == R and fam(x)]
                jj = [x for c, RR, x in b.star_rows('J', scoring=True) if RR == R and fam(x)]
                if not (sk and hh and jj): continue
                t = f"{runner} {X} {R}: S {', '.join(o['plane'] + ' ' + o['tgt'] for o in sk)} | H {', '.join(x['plane'] + ' ' + x['tgt'] for x in hh)} | J {', '.join(x['plane'] + ' ' + x['tgt'] for x in jj)}"
                hold['M1'].add(runner); ex['M1'].append(t)
                same = any(a['fam'] == h['fam'] == j['fam'] for a in sk for h in hh for j in jj)
                if same: hold['M2'].add(runner); ex['M2'].append(t)
                def car(xs, moon):
                    return any(X not in (A, B) and (moon or 'Moon' not in (A, B)) for x in xs for s, A, B in b.pairs_on(x))
                m3 = car(hh, True) and car(jj, True); m3n = car(hh, False) and car(jj, False)
                if m3: hold['M3'].add(runner); ex['M3'].append(t)
                if m3n: hold['M3n'].add(runner)
                if m3 and same: hold['M4'].add(runner); ex['M4'].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('M3', 'M4'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 7 result races: {p} picks, {wn} won, {c:.1f} by chance')
