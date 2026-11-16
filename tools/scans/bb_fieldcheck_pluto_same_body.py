"""Field check (16 Nov 2026, Eddie: 'a s pluto to h pluto score winning again'): the same-body line S Pluto -> H Pluto / J Pluto scoring in
a family (conj / cp not counted), per runner, against the winners of the 8 result races; also every other body for comparison.
Read-only."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel')
fam = lambda o: o.get('fam') and o['fam'] not in CJ
keys = [('H', None), ('J', None), ('H+J', None), ('H', 50), ('H', 80)]
tot = {}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
    for run, bodies in data.items():
        for X, d in bodies.items():
            b = E.Body(X, d)
            h = [o for o in b.same_body('H') if fam(o)]; j = [o for o in b.same_body('J') if fam(o)]
            hs = max([o['sc'] or 0 for o in h], default=None)
            conds = {('H', None): bool(h), ('J', None): bool(j), ('H+J', None): bool(h and j),
                     ('H', 50): hs is not None and hs >= 50, ('H', 80): hs is not None and hs >= 80}
            for k, ok in conds.items():
                if ok:
                    t = tot.setdefault((X, k), [0, 0, 0.0])
                    if w: t[0] += 1; t[1] += (w in run); t[2] += 1 / N
            if X == 'Pluto' and h:
                print(f"{n} {run}: " + '; '.join(f"{o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})" for o in h) + ('  W' if w and w in run else ''))
print()
for k in keys:
    rows = sorted(((X, *tot[(X, kk)]) for (X, kk) in tot if kk == k), key=lambda t: -(t[2] - t[3]))
    print(f"{k}: " + ', '.join(f"{X} {p}/{wn} ({c:.1f})" for X, p, wn, c in rows))

# H or J (16 Nov 2026): runners with S X -> H X or S X -> J X scoring, per body, over the 8 result races
print()
T = {}
for n, r, w in races:
    if not w: continue
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx')
    for X in next(iter(data.values())):
        h = {run for run, bs in data.items() if any(fam(o) for c in 'HJ' for o in E.Body(X, bs[X]).same_body(c))}
        t = T.setdefault(X, [0, 0, 0.0]); t[0] += len(h); t[1] += any(w in x for x in h); t[2] += len(h) / len(data)
print('H or J: ' + ', '.join(f"{X} {p}/{wn} ({c:.1f})" for X, (p, wn, c) in sorted(T.items(), key=lambda kv: -(kv[1][1] - kv[1][2]))))
