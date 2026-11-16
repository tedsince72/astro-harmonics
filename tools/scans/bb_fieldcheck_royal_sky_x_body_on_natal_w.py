"""Field check (16 Nov 2026, Athmad Venus, Eddie's addition): V1 of bb_fieldcheck_royal_sky_x_body_on_natal.py (S R – S X and
S Y -> c X on the same family + target) plus S Regulus – S Uranus RA 110.0498 68×φ (27.4) (a royal star on sky Y) and
S Uranus -> J Venus RA 177.4498 ninth 177.778 (7.8) (Y on natal X in the other plane too).
W1 V1 + S Y -> c X scores in a family in the other plane too (same chart c).
W2 V1 + a royal star R2 on sky Y (S R2 – S Y scoring, not conj / cp; any royal star).
W3 W2 + R2 on natal X in chart c: c R2 – c X in a family, or with a same-body / crossed ratio on a target (any score).
W4 W1 + W2.
W5 W1 + W3.
Read-only."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('W1', 'W2', 'W3', 'W4', 'W5'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda o: o.get('fam') and o['fam'] not in CJ
tg = lambda t: t and t not in ('no target',) and not str(t).startswith('conjunction')
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        B = {X: E.Body(X, d) for X, d in bodies.items()}
        for X, b in B.items():
            if X in ('Rahu', 'Ketu'): continue
            sr = [o for o in b.O if fam(o) and any(o['line'] == f'S {R} – S {X}' for R in E.ROY)]
            if not sr: continue
            for o in b.O:
                ln = o['line']
                if not fam(o) or ' → ' not in ln or not ln.endswith(f' {X}'): continue
                Y, c = ln[2:].split(' → ')[0], ln.split(' → ')[1][0]
                if Y == 'Moon' or Y in E.ROY or c not in 'HJ': continue
                for a in sr:
                    if a['fam'] != o['fam'] or str(a['tgt']) != str(o['tgt']): continue
                    t = f"{run} {X}: {a['line']} {a['plane']} {a['v']:.4f} ({a['sc']}) = {ln} {o['plane']} {o['v']:.4f} ({o['sc']}) {o['tgt']}"
                    q = 'Dec' if o['plane'].startswith('RA') else 'RA'
                    w1 = [p for p in b.O if p['line'] == ln and p['plane'].startswith(q) and fam(p)]
                    w2 = [p for p in (B[Y].O if Y in B else []) if fam(p) and any(p['line'] == f'S {R} – S {Y}' for R in E.ROY)]
                    w3 = []
                    for p in w2:
                        R2 = p['line'].split(' – ')[0][2:]
                        for cc, RR, x in b.star_rows(c):
                            if RR == R2 and (fam(x) or tg(x.get('rt')) or tg(x.get('xt'))):
                                w3.append(f"{p['line']} {p['plane']} ({p['sc']}) + {x['line']} {x['plane']} {x['fam'] and x['tgt']} r {x.get('rt')} ({x.get('rs')}) x {x.get('xt')} ({x.get('xs')})")
                    s1 = f" | other plane {w1[0]['plane']} {w1[0]['v']:.4f} {w1[0]['tgt']} ({w1[0]['sc']})" if w1 else ''
                    s2 = ' | ' + '; '.join(f"{p['line']} {p['plane']} {p['tgt']} ({p['sc']})" for p in w2) if w2 else ''
                    for v, ok, extra in (('W1', w1, s1), ('W2', w2, s2), ('W3', w3, ' | ' + '; '.join(w3)), ('W4', w1 and w2, s1 + s2),
                                         ('W5', w1 and w3, s1 + ' | ' + '; '.join(w3))):
                        if ok: hold[v].add(run); ex[v].append(t + extra)
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('W1', 'W5'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
