"""Field check (15 Nov 2026, Eddie 'ok, do that', from Wotever Next Mercury): S X -> H X and S X -> J X both score
(conj / contraparallel not counted), values within D of each other (any planes).
V1 = that; V2 = + one sky pair S A - S B on the target of BOTH lines (pair not naming X; Moon allowed);
V3 = V2 with the Moon not allowed as a pair end. D = 0.2 and 0.1. Winners as in CLAUDE.md; Chelmsford winner not on record."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel')
for D in (0.2, 0.1):
    tot = {v: [0, 0, 0.0] for v in ('V1', 'V2', 'V3')}
    print(f'=== D = {D}')
    for n, r, w in races:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        hold = {v: [] for v in tot}
        for runner, bodies in data.items():
            for X, d in bodies.items():
                b = E.Body(X, d)
                H = [x for x in b.same_body('H') if x['fam'] and x['fam'] not in CJ]
                J = [x for x in b.same_body('J') if x['fam'] and x['fam'] not in CJ]
                for h in H:
                    for j in J:
                        if abs(h['v'] - j['v']) >= D: continue
                        ph = {s['line'] for s, A, B in b.pairs_on(h) if X not in (A, B)}
                        pj = {s['line'] for s, A, B in b.pairs_on(j) if X not in (A, B)}
                        both = ph & pj
                        tag = f"{runner} {X}: H {h['plane']} {h['v']:.4f} {h['tgt']} ({h['sc']}) / J {j['plane']} {j['v']:.4f} {j['tgt']} ({j['sc']})"
                        hold['V1'].append((runner, tag))
                        if both: hold['V2'].append((runner, tag + ' | ' + '; '.join(sorted(both))))
                        if [p for p in both if 'Moon' not in p]: hold['V3'].append((runner, tag))
        for v, L in hold.items():
            rs = sorted({x for x, _ in L}); won = bool(w) and any(w in x for x in rs)
            if w and rs: tot[v][0] += len(rs); tot[v][1] += won; tot[v][2] += len(rs) / N
            print(f"{n} {v}: {len(rs)}/{N}{' W' if won else ''}")
            for _, t in L: print('    ', t)
    for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
