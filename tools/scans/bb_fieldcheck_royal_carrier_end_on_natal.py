"""Field check (16 Nov 2026, from Newcastle AW 16:33 2021 Athmad Mars): H Aldebaran – H Mars RA 155.4460 ninth 155.556 (64.8) carried by
four sky pairs on the same ninth (S Haumea – S Sedna 88.8, S Chiron – S Haumea 56.6, S Sun – S Gonggong 31.8, S Ceres – S Haumea 8.9); the
Sun (an end of S Sun – S Gonggong) lands on J Mars in both planes (Dec 4.1417 silver 4.14 (93.5), RA 14.5756 9×φ (59.0)); J Fomalhaut –
J Mars Dec 51.4307 crossed ratio 1.4152 √2 (52.2) against S Mars -> J Mars RA 36.3410.
M1 a royal line c R – c X in a family (not conj / cp) carried by a sky pair S A – S B on its target (pair not naming X; the Moon not an end),
   and an end A (not royal) lands on natal X (S A -> H X or J X in a family, not conj / cp; either chart, any plane).
M2 M1 with A on natal X in the other chart.
M3 M1 with A on natal X in both planes of one chart.
M4 the royal line carried by 3 or more sky pairs (not naming X, no Moon).
M5 M2 + M3 (Athmad: Sun on J Mars both planes, royal line in H).
M6 a royal – X row in a chart with a same-body or crossed ratio on √2 (any score) and a sky body landing on natal X in that chart on a
   √2 or silver target (not the Moon; Y != X: the same-body line S X -> c X is not counted).
Read-only."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('M1', 'M2', 'M3', 'M4', 'M5', 'M6'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda o: o.get('fam') and o['fam'] not in CJ
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            def on(A, c):
                return [o for o in b.O if o['line'] == f'S {A} → {c} {X}' and fam(o)]
            for c, R, row in b.star_rows(scoring=True):
                if not fam(row): continue
                ps = [(s, A, B) for s, A, B in b.pairs_on(row) if X not in (A, B) and 'Moon' not in (A, B) and fam(s)]
                if len(ps) >= 3:
                    hold['M4'].add(run); ex['M4'].append(f"{run} {X}: {row['line']} {row['plane']} {row['tgt']} carried by {len(ps)}")
                oc = 'J' if c == 'H' else 'H'
                for s, A, B in ps:
                    for Y in (A, B):
                        if Y in E.ROY: continue
                        for cc in 'HJ':
                            o = on(Y, cc)
                            if not o: continue
                            t = f"{run} {X}: {row['line']} {row['plane']} {row['v']:.4f} {row['tgt']} ({row['sc']}) via {s['line']} ({s['sc']}); {Y} on {cc} {X}: " + ', '.join(f"{x['plane']} {x['v']:.4f} {x['tgt']} ({x['sc']})" for x in o)
                            hold['M1'].add(run); ex['M1'].append(t)
                            both = len({x['plane'].split()[0] for x in o}) == 2
                            if cc == oc: hold['M2'].add(run); ex['M2'].append(t)
                            if both: hold['M3'].add(run); ex['M3'].append(t)
                            if cc == oc and both: hold['M5'].add(run); ex['M5'].append(t)
            for c in 'HJ':
                r2 = [x for _, R, x in b.star_rows(c) if any(str(x.get(k) or '').startswith('√2') for k in ('rt', 'xt'))]
                if not r2: continue
                lands = [o for o in b.O if fam(o) and ' → ' in o['line'] and o['line'].endswith(f'{c} {X}') and not o['line'].startswith('S Moon')
                         and o['fam'] in ('sqrt2', 'silver')]
                if lands:
                    hold['M6'].add(run); ex['M6'].append(f"{run} {X} {c}: {r2[0]['line']} {r2[0]['plane']} | " + ', '.join(f"{o['line']} {o['plane']} {o['tgt']} ({o['sc']})" for o in lands))
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('M5', 'M6'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
