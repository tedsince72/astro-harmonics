"""Field check (15 Nov 2026, from Catterick Wotever Next Venus): Antares on sky Venus (S Antares – S Venus Dec 15.5429 ninth),
H Antares – H Venus no family but same-body ratios 9 (RA, 20.5) and 7 (Dec, 91.8), J Antares – J Venus RA 44.4184 ninth (70.7);
Regulus also on sky Venus (RA 179.4772 10φ⁶, 87.2).
A1 a royal star R scores on sky X (S R – S X, not conj / cp) and R's natal line to X in BOTH charts has a family (not conj / cp)
   or a same-body / crossed ratio on a target (= BB10 without its pair).
A2 A1 with every ratio used scoring >= 50 (a family still counts at any score).
A3 A1 + a second royal star on sky X (scoring, not conj / cp).
A4 A1 with one chart carried only by a ratio (no family) and the other chart by a family.
Second part (A5-A7, run with --tight):
A5 R on sky X; the other chart's R – X has the sky line's family; this chart has a same-body / crossed ratio >= 50.
A6 this chart's R – X has no family in either plane but a same-body ratio in both planes; the other chart has a family.
A7 A6 + the other chart's family = the sky line's family."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('A1', 'A2', 'A3', 'A4')
def fam(r): return bool(r['fam']) and r['fam'] not in CJ
def sc(x): return x if E.num(x) else 0.0
def rat(r, m=None): return (E.num(r['rs']) or E.num(r['xs'])) if m is None else max(sc(r['rs']), sc(r['xs'])) >= m
tot = {v: [0, 0, 0.0] for v in V}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for runner, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            skyR = [R for R in E.ROY if [o for o in b.sky_y(R) if fam(o)]]
            for R in skyR:
                nat = {c: [x for _, R2, x in b.star_rows(c) if R2 == R] for c in 'HJ'}
                f = {c: any(fam(x) for x in nat[c]) for c in 'HJ'}
                q = {c: any(rat(x) for x in nat[c]) for c in 'HJ'}
                q50 = {c: any(rat(x, 50) for x in nat[c]) for c in 'HJ'}
                t = f"{runner} {X} {R}"
                if all(f[c] or q[c] for c in 'HJ'):
                    hold['A1'].add(runner); ex['A1'].append(t)
                    if all(f[c] or q50[c] for c in 'HJ'): hold['A2'].add(runner); ex['A2'].append(t)
                    if len(skyR) > 1: hold['A3'].add(runner); ex['A3'].append(t + ' + ' + ','.join(x for x in skyR if x != R))
                    if (f['H'] and not f['J'] and q['J']) or (f['J'] and not f['H'] and q['H']): hold['A4'].add(runner); ex['A4'].append(t)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {ex[v]}")
for v, (p, wn, c) in tot.items(): print(f'{v} over the 6 result races: {p} picks, {wn} won, {c:.1f} by chance')


if '--tight' in sys.argv:
    V=('A5','A6','A7'); tot={v:[0,0,0.0] for v in V}
    for n,r,w in races:
        data=E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N=len(data); hold={v:set() for v in V}; ex={v:[] for v in V}
        for runner,bodies in data.items():
            for X,d in bodies.items():
                b=E.Body(X,d)
                for R in E.ROY:
                    sky=[o for o in b.sky_y(R) if fam(o)]
                    if not sky: continue
                    nat={c:[x for _,R2,x in b.star_rows(c) if R2==R] for c in 'HJ'}
                    for c in 'HJ':
                        o='J' if c=='H' else 'H'
                        # A6: chart c line has NO family in either plane but same-body ratio scores in both planes; other chart has a family
                        if nat[c] and all(not fam(x) for x in nat[c]) and len([x for x in nat[c] if E.num(x['rs'])])>=2 and any(fam(x) for x in nat[o]):
                            hold['A6'].add(runner); ex['A6'].append(f'{runner} {X} {R} ({c} ratios)')
                            if any(s['fam']==y['fam'] for s in sky for y in nat[o] if fam(y)): hold['A7'].add(runner); ex['A7'].append(f'{runner} {X} {R}')
                        # A5: other chart family same as the sky line family, chart c ratio >= 50
                        if any(fam(y) and y['fam']==s['fam'] for s in sky for y in nat[o]) and any((x['rs'] if E.num(x['rs']) else 0)>=50 or (x['xs'] if E.num(x['xs']) else 0)>=50 for x in nat[c]):
                            hold['A5'].add(runner); ex['A5'].append(f'{runner} {X} {R}')
        for v in V:
            won=bool(w) and any(w in x for x in hold[v])
            if w and hold[v]: tot[v][0]+=len(hold[v]); tot[v][1]+=won; tot[v][2]+=len(hold[v])/N
            print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(set(ex[v]))}")
    for v,(p,wn,c) in tot.items(): print(f'{v}: {p} picks, {wn} won, {c:.1f} by chance')
