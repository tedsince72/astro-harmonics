"""Field check (15 Nov 2026, from Catterick Wotever Next Sun: H Regulus – H Sun Dec 6 carried by S Moon – S Rahu Dec 6;
J Regulus – J Sun RA ninth 166.667 carried by S Rahu – S Haumea RA; Moon on H Sun RA 62, Haumea on J Sun RA 63×φ / cp).
R0 the same royal star R has a scoring natal line to X in both charts (conj / cp out), each carried by a sky pair (pair not naming X).
R1 R0 + a horse pair and a jockey pair share a body Y (Moon allowed).  R1n = R1 with no Moon in either pair.
R2 R1 + each pair's other end lands on natal X in that pair's chart (S E → c X scoring, any plane; cp counts).
R2s = R2 with those end lines not conj / cp."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('R0', 'R1', 'R1n', 'R2', 'R2s')
tot = {v: [0, 0, 0.0] for v in V}
def on(b, E_, c, strict):
    return [o for o in b.to_natal(E_, c) if o['fam'] and (not strict or o['fam'] not in CJ)]
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for R in E.ROY:
                P = {}
                for c in 'HJ':
                    P[c] = [(row, s, A, B) for cc, RR, row in b.star_rows(c, scoring=True) if RR == R and row['fam'] not in CJ
                            for s, A, B in b.pairs_on(row) if X not in (A, B)]
                if not (P['H'] and P['J']): continue
                hold['R0'].append((runner, f'{X} {R}'))
                for hr, hs, ha, hb in P['H']:
                    for jr, js, ja, jb in P['J']:
                        for Y in {ha, hb} & {ja, jb}:
                            if Y in E.ROY: continue
                            t = f"{runner} {X} {R}: {hr['line']} {hr['plane']} {hr['v']:.4f} {hr['tgt']} by {hs['line']} {hs['plane']} | {jr['line']} {jr['plane']} {jr['v']:.4f} {jr['tgt']} by {js['line']} {js['plane']} | shared {Y}"
                            hold['R1'].append((runner, t))
                            moon = 'Moon' in (ha, hb, ja, jb)
                            if not moon: hold['R1n'].append((runner, t))
                            eh = hb if ha == Y else ha; ej = jb if ja == Y else ja
                            for strict, v in ((False, 'R2'), (True, 'R2s')):
                                oh, oj = on(b, eh, 'H', strict), on(b, ej, 'J', strict)
                                if oh and oj:
                                    hold[v].append((runner, t + f" | {eh} → H {X}: {oh[0]['plane']} {oh[0]['v']:.4f} {oh[0]['tgt']} ({oh[0]['sc']}); {ej} → J {X}: {oj[0]['plane']} {oj[0]['v']:.4f} {oj[0]['tgt']} ({oj[0]['sc']})"))
    for v in V:
        rs = sorted({x for x, _ in hold[v]}); won = bool(w) and any(w in x for x in rs)
        if w and rs: tot[v][0] += len(rs); tot[v][1] += won; tot[v][2] += len(rs) / N
        print(f"{n} {v}: {len(rs)}/{N}{' W' if won else ''} {rs if v == 'R0' else ''}")
        if v != 'R0':
            for t in sorted({t for _, t in hold[v]}): print('    ', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
