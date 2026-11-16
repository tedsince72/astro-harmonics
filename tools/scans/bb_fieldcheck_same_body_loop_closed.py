"""Field check (16 Nov 2026, Athmad Pluto): S Pluto -> H Pluto RA 9.9931 ninth 10 (65.4) carried by S Mars – S Rahu Dec 9.9948 10 (74.0);
Rahu on sky Pluto (S Rahu – S Pluto Dec 44.4534 ninth 44.4444 (90.0)), Mars on natal H Pluto (S Mars -> H Pluto RA 132.6737 82×φ (84.2));
depth ladder step 4 (repeat: S Jupiter -> H Pluto RA 44.5189 ninth 44.4444 (16.2), the Rahu-Pluto number). Moon lines on H Pluto not used.
P1 a same-body line S X -> c X in a family (not conj / cp) carried by a sky pair S A – S B on its target (not naming X, no Moon), one end A
   on sky X (S A – S X in a family) and the other end B on natal X in the SAME chart c (S B -> c X in a family). Conj / cp never count.
P2 P1 with the three legs (carrier, A on sky X, B on c X) all scoring >= 50 (Athmad 74.0 / 90.0 / 84.2).
P3 P2 + the same-body line >= 50 (Athmad 65.4).
P4 P1 + a line on natal X (S Z -> c X, Z not the Moon) repeating the family + target of the A – X sky line (Athmad: S Jupiter -> H Pluto
   44.4444 = S Rahu – S Pluto 44.4444); Z != B (the B leg itself is not a repeat).
Read-only."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('P1', 'P2', 'P3', 'P4'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda o: o.get('fam') and o['fam'] not in CJ
sc = lambda o: o.get('sc') or 0
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            sky = lambda A: [o for o in b.O if fam(o) and o['line'] in (f'S {A} – S {X}', f'S {X} – S {A}')]
            nat = lambda Bn, c: [o for o in b.O if fam(o) and o['line'] == f'S {Bn} → {c} {X}']
            for c in 'HJ':
                for row in b.same_body(c):
                    if not fam(row): continue
                    for s, A, B in b.pairs_on(row):
                        if X in (A, B) or 'Moon' in (A, B) or not fam(s): continue
                        for a, e in ((A, B), (B, A)):
                            ys, ns = sky(a), nat(e, c)
                            if not ys or not ns: continue
                            y, z = max(ys, key=sc), max(ns, key=sc)
                            t = f"{run} {X}: {row['line']} {row['plane']} {row['tgt']} ({row['sc']}) via {s['line']} {s['plane']} ({s['sc']}); {y['line']} {y['plane']} {y['tgt']} ({y['sc']}); {z['line']} {z['plane']} {z['tgt']} ({z['sc']})"
                            hold['P1'].add(run); ex['P1'].append(t)
                            if min(sc(s), sc(y), sc(z)) >= 50:
                                hold['P2'].add(run); ex['P2'].append(t)
                                if sc(row) >= 50: hold['P3'].add(run); ex['P3'].append(t)
                            rep = [o for o in b.O if fam(o) and ' → ' in o['line'] and o['line'].endswith(f'{c} {X}') and not o['line'].startswith('S Moon') and o['line'] != f'S {e} → {c} {X}'
                                   and any(o['fam'] == yy['fam'] and str(o['tgt']) == str(yy['tgt']) for yy in ys)]
                            if rep: hold['P4'].add(run); ex['P4'].append(t + f" | repeat {rep[0]['line']} {rep[0]['plane']} {rep[0]['tgt']} ({rep[0]['sc']})")
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('P3', 'P4'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
