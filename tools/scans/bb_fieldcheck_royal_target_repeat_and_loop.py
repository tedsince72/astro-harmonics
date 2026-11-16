"""Field check (16 Nov 2026, Athmad Rahu / Ketu): J Antares – J Ketu RA 155.8290 ninth 155.556 (12.1) is carried by the same four sky pairs
as H Aldebaran – H Mars RA 155.4460 ninth 155.556 (S Haumea – S Sedna, S Chiron – S Haumea, S Sun – S Gonggong, S Ceres – S Haumea);
J Antares – J Rahu RA 24.1710 silver 24.14 (20.3) = S Venus -> J Rahu Dec 24.1332 silver 24.14 (75.3), Venus on sky Rahu (S Venus – S Rahu
Dec 14.1268 √2 27.8), Antares on sky Rahu (S Antares – S Rahu RA 179.5221 10φ⁶ 70.5). The Ketu unisons (S Ketu -> H / J Ketu vs H / J
Antares – Ketu RA) are forced: S Antares – S Ketu RA 0.4779 conj.
K1 two royal natal lines (any charts) on different bodies X != X' (Rahu / Ketu one body) on the same family + target, sharing >= 1 carrier
   pair ('Sky lines on the same target', not naming X / X', no Moon, pair in a family).
K2 K1 sharing >= 3 carrier pairs.
K3 a royal natal line c R – c X (family f, target t) and S Y -> c X on the same f, t (Y not Moon, not royal, Y != X), and Y on sky X
   (S Y – S X or S X – S Y in a family). Conj / cp never count.
K4 K3 + the same royal star R on sky X (S R – S X in a family).
Carrier pairs come from the bybody 'Matches' column, which can match a royal row through an 'also' family (Dubai Souq).
Read-only."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('K1', 'K2', 'K3', 'K4'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda o: o.get('fam') and o['fam'] not in CJ
node = lambda X: 'Nodes' if X in ('Rahu', 'Ketu') else X
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        B = {X: E.Body(X, d) for X, d in bodies.items()}
        lines = []
        for X, b in B.items():
            for c, R, row in b.star_rows(scoring=True):
                if not fam(row): continue
                ps = {s['line'] + ' ' + s['plane'] for s, A, Bb in b.pairs_on(row) if node(X) not in (node(A), node(Bb)) and 'Moon' not in (A, Bb) and fam(s)}
                lines.append((X, c, R, row, ps))
                # K3 / K4
                for o in b.O:
                    ln = o['line']
                    if not fam(o) or ' → ' not in ln or not ln.endswith(f'{c} {X}'): continue
                    Y = ln[2:].split(' → ')[0]
                    if Y == 'Moon' or Y in E.ROY or Y == X or o['fam'] != row['fam'] or str(o['tgt']) != str(row['tgt']): continue
                    ys = [p for p in b.O if fam(p) and p['line'] in (f'S {Y} – S {X}', f'S {X} – S {Y}')]
                    if not ys: continue
                    t = f"{run} {X}: {row['line']} {row['plane']} {row['v']:.4f} {row['tgt']} ({row['sc']}) = {ln} {o['plane']} {o['v']:.4f} ({o['sc']}); {ys[0]['line']} {ys[0]['plane']} {ys[0]['tgt']} ({ys[0]['sc']})"
                    hold['K3'].add(run); ex['K3'].append(t)
                    rs = [p for p in b.O if fam(p) and p['line'] == f'S {R} – S {X}']
                    if rs: hold['K4'].add(run); ex['K4'].append(t + f"; {rs[0]['line']} {rs[0]['plane']} {rs[0]['tgt']} ({rs[0]['sc']})")
        for i, (X, c, R, row, ps) in enumerate(lines):
            for X2, c2, R2, row2, ps2 in lines[i + 1:]:
                if node(X2) == node(X) or row['fam'] != row2['fam'] or str(row['tgt']) != str(row2['tgt']): continue
                k = len({p for p in ps & ps2 if node(X2) not in [node(z) for z in p.rsplit(' ', 1)[0][2:].split(' – S ')]})
                if k >= 1:
                    t = f"{run}: {row['line']} {row['plane']} | {row2['line']} {row2['plane']} {row['tgt']}: {k} shared"
                    hold['K1'].add(run); ex['K1'].append(t)
                    if k >= 3: hold['K2'].add(run); ex['K2'].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('K2', 'K4'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
