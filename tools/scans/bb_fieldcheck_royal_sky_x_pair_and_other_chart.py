"""Field check (15 Nov 2026, from Catterick Wotever Next Chiron): H Fomalhaut – H Chiron Dec 33.3819 ninth 33.3333 (27.2) carried by
S Chiron – S Gonggong RA 33.3465 (80.2), S Vesta → J Chiron Dec 33.3144 (71.6), S Vesta – S Haumea Dec 33.3849 (22.6); S Gonggong – S Chiron
Dec ninth 17.7778 (16.0), S Vesta – S Chiron Dec 15×φ (60.7), S Haumea → J Chiron Dec conj (76.5); J Fomalhaut – J Chiron Dec 45.3428 /
S Chiron → J Chiron Dec 9.056628 = 5.00659 on 5 (67.1); S Regulus – S Chiron RA √2 141.4 (42.9).
E1 royal line c R – c X (family, not conj / cp) carried by a sky pair S X – S Y (any plane) AND by S Z → c' X (c' the other chart; Z not Moon).
E2 E1 + Z on sky X (S Z – S X scoring, conj / cp count).
E3 E1 + Y on sky X in the other plane (S Y – S X scoring in the plane the carrier is not in; conj / cp count).
E4 E1 + a third carrier S A – S B (not X, no Moon) with both ends on X (sky or either natal, scoring; conj / cp count).
E5 E1 + the same royal star R on X in chart c' with a same-body or crossed ratio on a target.
E6 = Wotever Next's whole set: E2 + E3 + E4.
E7 E4 + E5."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7'); tot = {v: [0, 0, 0.0] for v in V}
def on_x(b, Y):
    return bool([o for o in b.sky_y(Y) if o['fam']] + [o for c in 'HJ' for o in b.to_natal(Y, c) if o['fam']])
def tgt_ratio(r):
    return any(E.num(r.get(k)) and r.get(t) not in (None, 'no target') and 'cut' not in str(r.get(t))
               for k, t in (('rs', 'rt'), ('xs', 'xt')))
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            for c, R, a in b.star_rows(scoring=True):
                if a['fam'] in CJ: continue
                c2 = E.other_chart(c); S = b.same_on(a)
                sxy = []
                for s in S:
                    p = s['line'].split(' – ')
                    if len(p) == 2 and p[0].startswith('S ') and p[1].startswith('S ') and X in (p[0][2:], p[1][2:]):
                        Y = p[1][2:] if p[0][2:] == X else p[0][2:]
                        if Y != 'Moon': sxy.append((s, Y))
                szx = [(s, s['line'].split(' → ')[0][2:]) for s in S if s['line'].endswith(f' → {c2} {X}')]
                szx = [(s, Z) for s, Z in szx if Z not in ('Moon', X)]
                if not (sxy and szx): continue
                t = f"{runner} {X}: {a['line']} {a['plane']} {a['v']:.4f} {a['tgt']} | " + ', '.join(f"{s['line']} {s['plane']}" for s, _ in sxy + szx)
                hold['E1'].add(runner); ex['E1'].append(t)
                e2 = any(o['fam'] for _, Z in szx for o in b.sky_y(Z))
                e3 = any(o['fam'] and o['plane'] != s['plane'] for s, Y in sxy for o in b.sky_y(Y))
                e4 = False
                for s, A, B in b.pairs_on(a):
                    if X in (A, B) or 'Moon' in (A, B): continue
                    if on_x(b, A) and on_x(b, B): e4 = True
                e5 = any(tgt_ratio(x) for cc, RR, x in b.star_rows(c2) if RR == R)
                for v, ok in (('E2', e2), ('E3', e3), ('E4', e4), ('E5', e5), ('E6', e2 and e3 and e4), ('E7', e4 and e5)):
                    if ok: hold[v].add(runner); ex[v].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for t in sorted(set(ex['E1'])): print('    ', t)
    for t in sorted(set(ex['E5'])): print('   E5', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')
