"""Field check (16 Nov 2026, from Newcastle AW 16:33 2021 Athmad Venus): S Fomalhaut – S Venus Dec 37.2291 23×φ (55.8) and
S Uranus -> J Venus Dec 37.2201 23×φ (83.5); amplification H Fomalhaut – H Venus Dec same-body ratio 4.0013 on 4 (93.4) and
J Regulus – J Venus Dec crossed ratio 1.6178 φ (92.0). BB56 with the Sun replaced by any sky body.
V1 a scoring sky line S R – S X (R royal, not conj / cp) and a scoring S Y -> H X or S Y -> J X (Y any sky body, not the Moon, not a
   royal star; not conj / cp) on the same family and target. X not Rahu / Ketu. Any score.
V2 V1 with the S Y -> natal X line scoring >= 50.
V3 V1 with Y != X (the same-body line S X -> natal X not counted).
V4 V1 + a royal – X natal row (any royal star, plane) with a same-body or crossed ratio scoring >= 90 in the chart of the V1 natal line.
V5 V1 + such a ratio >= 90 in both charts (Athmad's shape).
Read-only; no results file opened except through the winner names below."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); V = ('V1', 'V2', 'V3', 'V4', 'V5'); tot = {v: [0, 0, 0.0] for v in V}
fam = lambda o: o.get('fam') and o['fam'] not in CJ
def hi_ratio(b, c):
    out = []
    for cc, R, x in b.star_rows(c):
        for k, t in (('rs', 'rt'), ('xs', 'xt')):
            if x.get(k) is not None and x[k] >= 90: out.append(f"{x['line']} {x['plane']} {t[0]} {x[t]} ({x[k]})")
    return out
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data); hold = {v: set() for v in V}; ex = {v: [] for v in V}
    for run, bodies in data.items():
        for X, d in bodies.items():
            if X in ('Rahu', 'Ketu'): continue
            b = E.Body(X, d)
            sr = [o for o in b.O if fam(o) and any(o['line'] == f'S {R} – S {X}' for R in E.ROY)]
            if not sr: continue
            hr = {c: hi_ratio(b, c) for c in 'HJ'}
            for o in b.O:
                ln = o['line']
                if not fam(o) or ' → ' not in ln or not ln.endswith(f' {X}'): continue
                Y, c = ln[2:].split(' → ')[0], ln.split(' → ')[1][0]
                if Y == 'Moon' or Y in E.ROY or c not in 'HJ': continue
                for a in sr:
                    if a['fam'] != o['fam'] or str(a['tgt']) != str(o['tgt']): continue
                    t = f"{run} {X}: {a['line']} {a['plane']} {a['v']:.4f} ({a['sc']}) = {ln} {o['plane']} {o['v']:.4f} ({o['sc']}) {o['tgt']} {o['fam']}"
                    hold['V1'].add(run); ex['V1'].append(t)
                    if (o['sc'] or 0) >= 50: hold['V2'].add(run); ex['V2'].append(t)
                    if Y != X: hold['V3'].add(run); ex['V3'].append(t)
                    if hr[c]: hold['V4'].add(run); ex['V4'].append(t + ' | ' + '; '.join(hr[c]))
                    if hr['H'] and hr['J']: hold['V5'].add(run); ex['V5'].append(t + ' | ' + '; '.join(hr['H'] + hr['J']))
    for v in V:
        won = bool(w) and any(w in x for x in hold[v])
        if w and hold[v]: tot[v][0] += len(hold[v]); tot[v][1] += won; tot[v][2] += len(hold[v]) / N
        print(f"{n} {v}: {len(hold[v])}/{N}{' W' if won else ''}  {sorted(hold[v])}")
    for v in ('V2', 'V5'):
        for t in sorted(set(ex[v])): print(f'   {v}', t)
for v, (p, wn, c) in tot.items(): print(f'{v} over the 8 result races: {p} picks, {wn} won, {c:.1f} by chance')
