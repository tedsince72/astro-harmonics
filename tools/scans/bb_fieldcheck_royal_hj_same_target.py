"""Field check (15 Nov 2026, from Fontwell 15:30 2023 Kilcummin Uranus): J Regulus – J Uranus Dec 33.3542 ninth 33.3333 (68.8) and
H Uranus – J Uranus Dec 33.3475 ninth 33.3333 (78.8), both carried by S Uranus – S Quaoar Dec 33.3183 (77.4) and S Saturn – S Pluto RA
33.3375 (93.8); Quaoar on Uranus: S Quaoar – S Uranus RA 133.2926 ninth (84.7), S Quaoar → J Uranus RA 22.1875 ninth (21.8).
Also: H Aldebaran – H Uranus RA 38.3194 / S Uranus → H Uranus RA 19.165768 = 1.999366 on 2 (96.8), H Fomalhaut – H Uranus RA 46.2541 /
19.165768 = 2.413373 on 1+√2 (76.8), H Antares – H Uranus Dec crossed 38.3934 / 19.165768 = 2.003227 on 2 (83.9): three royal rows of
the horse on one base line (S Uranus → H Uranus RA 19.165768, itself no family).
K1 H X – J X (family, not conj / cp) and a royal row c R – c X (family, not conj / cp) on the same family + target (any plane), the
   royal row carried by a sky line naming X itself (S X – S Y, Y not the Moon).
K2 K1 + Y on natal X (S Y → H X or J X scoring; conj / cp count).
K3 K1 + the H X – J X line carried by the same sky line.
L1 three or more royal rows of one chart with a same-body or crossed ratio on a target, all on the same base line (S X → c X, one plane).
L2 two or more (as L1).
L3 L1 + the base line itself scores in no family."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell 15:30', '20231006_fontwell_1530', 'Kilcummin'), ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('K1', 'K2', 'K3', 'L1', 'L2', 'L3'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda x: x['fam'] and x['fam'] not in CJ
def ontgt(s, t):
    return E.num(s) and t not in (None, 'no target') and 'cut' not in str(t)
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            hj = [x for x in b.L if x['line'] == f'H {X} – J {X}' and fam(x)]
            for c, R, a in b.star_rows(scoring=True):
                if not fam(a): continue
                for h in hj:
                    if (h['fam'], h['tgt']) != (a['fam'], a['tgt']): continue
                    sxy = [(s, B if A == X else A) for s, A, B in b.pairs_on(a) if X in (A, B) and 'Moon' not in (A, B)]
                    if not sxy: continue
                    t = f"{runner} {X}: {a['line']} {a['plane']} {a['v']:.4f} / {h['line']} {h['plane']} {h['v']:.4f} {a['tgt']} by " + ', '.join(f"{s['line']} {s['plane']}" for s, _ in sxy)
                    hold['K1'].add(runner); ex['K1'].append(t)
                    if any(o['fam'] for _, Y in sxy for cc in 'HJ' for o in b.to_natal(Y, cc)): hold['K2'].add(runner); ex['K2'].append(t)
                    hs = {(s['line'], s['plane']) for s, A, B in b.pairs_on(h)}
                    if any((s['line'], s['plane']) in hs for s, _ in sxy): hold['K3'].add(runner); ex['K3'].append(t)
            for c in 'HJ':
                base = {}
                for cc, R, x in b.star_rows(c):
                    other = 'Dec' if x['plane'] == 'RA' else 'RA'
                    if ontgt(x.get('rs'), x.get('rt')): base.setdefault(x['plane'], []).append((R, x['plane'], 'sb', x['rt']))
                    if ontgt(x.get('xs'), x.get('xt')): base.setdefault(other, []).append((R, x['plane'], 'x', x['xt']))
                for pl, lst in base.items():
                    rs = {e[0] for e in lst}
                    bl = [o for o in b.same_body(c, pl, scoring=False)]
                    nofam = not any(fam(o) for o in bl)
                    t = f"{runner} {X} {c} base S {X} → {c} {X} {pl}: " + ', '.join(f"{e[0]} {e[1]} {e[2]} {e[3]}" for e in lst)
                    if len(rs) >= 2: hold['L2'].add(runner); ex['L2'].append(t)
                    if len(rs) >= 3:
                        hold['L1'].add(runner); ex['L1'].append(t)
                        if nofam: hold['L3'].add(runner); ex['L3'].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('K1', 'L1'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 7 result races: {p} picks, {wn} won, {c:.1f} by chance')
