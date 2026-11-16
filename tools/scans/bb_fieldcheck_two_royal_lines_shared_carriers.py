"""Field check (16 Nov 2026, Athmad Mars + Jupiter): H Aldebaran – H Mars RA 155.4460 ninth 155.556 (64.8) carried by S Haumea – S Sedna,
S Chiron – S Haumea, S Sun – S Gonggong, S Ceres – S Haumea; J Fomalhaut – J Jupiter RA 122.1485 ninth 122.222 (69.8) carried by
S Quaoar – S Regulus, S Sun – S Chiron, S Pluto – S Sedna, S Gonggong – S Haumea, S Pluto – S Ceres. The six Mars carrier bodies (Sun,
Chiron, Gonggong, Haumea, Sedna, Ceres) all carry the Jupiter line too. S Rahu -> J Jupiter RA 155.3922 ninth 155.556 (47.5) repeats the
Mars line's target on natal Jupiter.
Royal line = c R – c X in a family (not conj / cp); carriers = 'Sky lines on the same target' pairs S A – S B (not naming X, no Moon,
pair in a family); carrier bodies = their ends, royal stars excluded.
J1 two royal lines on different bodies X, X' of one runner, one in H and one in J, whose carrier-body sets share >= 3 bodies.
J2 J1 with >= 5 shared bodies.
J3 a royal line on X on target t, and a sky body landing on another natal body X' on the same family + target t, X' itself holding a
   carried royal line (any chart; S Y -> c X', Y not the Moon).
J4 J1 + J3 on the same pair of bodies.
Read-only."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('J1', 'J2', 'J3', 'J4'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda o: o.get('fam') and o['fam'] not in CJ
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        B = {X: E.Body(X, d) for X, d in bodies.items()}
        lines = []   # (X, c, row, carrier bodies)
        for X, b in B.items():
            for c, R, row in b.star_rows(scoring=True):
                if not fam(row): continue
                cb = set()
                for s, A, Bb in b.pairs_on(row):
                    if X in (A, Bb) or 'Moon' in (A, Bb) or not fam(s): continue
                    cb |= {A, Bb} - set(E.ROY)
                if cb: lines.append((X, c, row, cb))
        j1, j3 = set(), set()
        for i, (X, c, row, cb) in enumerate(lines):
            for X2, c2, row2, cb2 in lines[i + 1:]:
                if X2 == X or c2 == c: continue
                k = len(cb & cb2)
                if k >= 3:
                    t = f"{run}: {row['line']} {row['plane']} {row['tgt']} | {row2['line']} {row2['plane']} {row2['tgt']}: shared {sorted(cb & cb2)}"
                    hold['J1'].add(run); ex['J1'].append(t); j1.add(frozenset((X, X2)))
                    if k >= 5: hold['J2'].add(run); ex['J2'].append(t)
        held = {X for X, _, _, _ in lines}
        for X, c, row, cb in lines:
            for X2 in held - {X}:
                for o in B[X2].O:
                    if fam(o) and ' → ' in o['line'] and not o['line'].startswith('S Moon') and o['line'].endswith(f' {X2}') \
                       and o['fam'] == row['fam'] and str(o['tgt']) == str(row['tgt']):
                        t = f"{run}: {row['line']} {row['plane']} {row['tgt']} {row['fam']} = {o['line']} {o['plane']} {o['v']:.4f} ({o['sc']})"
                        hold['J3'].add(run); ex['J3'].append(t); j3.add(frozenset((X, X2)))
        if j1 & j3: hold['J4'].add(run); ex['J4'].append(f"{run}: {[sorted(p) for p in j1 & j3]}")
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('J4',):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
