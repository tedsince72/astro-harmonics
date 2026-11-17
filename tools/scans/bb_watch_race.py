"""Watch items on one race (16 Nov 2026; read blind, never reads results). Usage: python3 tools/scans/bb_watch_race.py <race>
(race = the bybody folder name, e.g. 20220717_newton_abbot_1525). Items kept from the 16 Nov discussions (RULE_CANDIDATES.md):
- rules held per runner (as built, from docs/eddie_read/bybody_rules/<race>_bbrules.json) and under T2 (tolerances above 100 tightened:
  ninth, φ power, √2, silver ±0.05, opposition ±0.25; tools/scans/bb_over100_tighten.py)
- combinations to watch: BB3 + BB63, BB3 + BB54, BB59, BB48 + BB55, BB13 + BB48 + BB55, BB32 + BB34; from River Bray (Eddie, 17 Nov 2026,
  'keep them on watch because in the end combinations will be where we select from'; tools/scans/bb_combos_riverbray.py): BB63 + BB68,
  BB3 + BB63 + BB68, BB1 + BB14, BB1 + BB14 + BB68, BB1 + BB12 + BB7, J1any + BB14, J1any + BB20, J1any + BB68 (J1any from
  bb_fieldcheck_riverbray; under T2 the J1any part is taken as held)
- P4 (Athmad Pluto loop; tools/scans/bb_fieldcheck_same_body_loop_closed.py) and its looser P1-P3
- S Pluto -> H Pluto / J Pluto scoring (any family, conj / cp not counted).
- Jupiter loop C (Eddie, 16 Nov 2026, from Cafe Sydney; tools/scans/bb_fieldcheck_jupiter_loop.py): S Jupiter -> c Jupiter, a sky
  pair on its target, both ends on the same natal Jupiter, line and pair >= 50; versions A, B, D listed too.
- N2 / N4 (Eddie, 16 Nov 2026, from Whitefeathersfall; tools/scans/bb_fieldcheck_whitefeathersfall.py): N2 BB29 held and its sky body
  conjunct / contraparallel natal X >= 90; N4 all three of BB3 + BB63, BB3 + BB54, BB59.
- Mirror (Eddie, 16 Nov 2026, from Society Red Venus; tools/scans/bb_fieldcheck_mirror.py): S X -> c X conj / contraparallel in Dec
  >= 80, with the sky bodies and royal stars conj / cp sky X; M4 (mirror >= 90 + a sky body + a royal star on sky X) is the watch item.
- Royal star on both natal X (Eddie, 16 Nov 2026, from Dynamic Force Jupiter Antares; tools/scans/bb_fieldcheck_royal_both.py): A2 is the
  watch item (1 pick 1 won over 17 result races); A1 cases listed too.
- One sky body on both natal X (Eddie, 16 Nov 2026, from Blue Collar Glory Venus / Ketu; tools/scans/bb_fieldcheck_hj_both.py): K1d is
  the watch item (H X – J X in Dec >= 90, a sky body on H X and J X >= 90; 5 picks 2 won over 18 result races); K1 / K2 tags shown.
- Regulus on 11 (Eddie, 17 Nov 2026, 'keep this'; from Haydock 17:18 Aldhaja Rahu and Kelso 14:50 Domandlouis Jupiter;
  tools/scans/bb_fieldcheck_royal_cut.py): a Regulus natal line to X whose same-body or crossed ratio is on '11 1/11 cut' scoring
  >= 90 is the watch item (6 picks 3 won, 1.0 by chance over 21 result races: Secret Satire, Cafe Sydney, Aldhaja; chosen after the
  results); cases scoring 50-90 listed too (19 / 5 / 3.0 at >= 50).
- Same royal star in the sky pair (Eddie, 17 Nov 2026, from Newmarket 15:35 Eydon Jupiter; tools/scans/bb_fieldcheck_eydon.py): G0s is
  the watch item - a natal royal line R – X carried by a sky pair S Y – S R with the same royal star, both lines >= 90 (3 picks 2 won,
  0.4 by chance over 23 result races: Diligent Resdev, Eydon); G1 / G2 / G2s tags shown on its cases.
- Jupiter–Jupiter on a sky number + BB68 (Eddie, 17 Nov 2026, 'keep the 2 out of 2 on watch'; from Wincanton 14:20 2022 River Bray and Ripon
  15:25 2022 Society Red; tools/scans/bb_fieldcheck_riverbray.py): J1any+B68 is the watch item - H Jupiter – J Jupiter in a number family
  (any score) with 2 or more sky pairs (not naming Jupiter) on its target, and BB68 held (2 picks 2 won, 0.4 by chance over 26 result races;
  Society Red is BB68's origin; chosen after the result); J1any without BB68 listed too."""
import json, sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_over100_tighten as TT
import bb_fieldcheck_jupiter_loop as JL
import bb_fieldcheck_mirror as MR
import bb_fieldcheck_royal_both as RB
import bb_fieldcheck_hj_both as HB
import bb_fieldcheck_royal_cut as RC
import bb_fieldcheck_eydon as EY
import bb_fieldcheck_riverbray as RBY

race = sys.argv[1]
data = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
runners = list(data)
hold = {x: set() for x in runners}
for rid, cases in J['rules'].items():
    for c in cases:
        if not c.get('watch_only'):
            hold[c['runner']].add(rid)
t2 = {x: set() for x in runners}
for rid, hs in TT.holders(TT.tighten(data, TT.V['T2'])).items():
    for x in hs:
        t2[x].add(rid)
out = [f'# Watch items — {race} (blind)', '', '## Rules held', '| runner | as built | under T2 | lost under T2 |', '|---|---|---|---|']
key = lambda r: (int(''.join(ch for ch in r[2:] if ch.isdigit())), r)
for x in runners:
    out.append(f"| {x} | {len(hold[x])}: {', '.join(sorted(hold[x], key=key))} | {len(t2[x])} | {', '.join(sorted(hold[x] - t2[x], key=key)) or '—'} |")
out += ['', '## Combinations to watch (as built | under T2)']
import bb_fieldcheck_riverbray as RBY0
j1 = {x for x in runners if 'J1any' in RBY0.tags(data[x], False)[0]}
hx = {x: hold[x] | ({'J1any'} if x in j1 else set()) for x in runners}
tx = {x: t2[x] | ({'J1any'} if x in j1 else set()) for x in runners}
for combo in (('BB3', 'BB63'), ('BB3', 'BB54'), ('BB59',), ('BB48', 'BB55'), ('BB13', 'BB48', 'BB55'), ('BB32', 'BB34'),
              ('BB63', 'BB68'), ('BB3', 'BB63', 'BB68'), ('BB1', 'BB14'), ('BB1', 'BB14', 'BB68'), ('BB1', 'BB12', 'BB7'),
              ('J1any', 'BB14'), ('J1any', 'BB20'), ('J1any', 'BB68')):
    a = [x for x in runners if set(combo) <= hx[x]]; b = [x for x in runners if set(combo) <= tx[x]]
    out.append(f"- {' + '.join(combo)}: {', '.join(a) or 'none'} | {', '.join(b) or 'none'}")
CJ = ('conj', 'contraparallel'); fam = lambda o: o.get('fam') and o['fam'] not in CJ; sc = lambda o: o.get('sc') or 0
P = {v: [] for v in ('P1', 'P2', 'P3', 'P4')}
pl = []
for run, bodies in data.items():
    for X, d in bodies.items():
        b = E.Body(X, d)
        if X == 'Pluto':
            for c in 'HJ':
                for o in b.same_body(c):
                    if fam(o):
                        pl.append(f"{run}: {o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} {o['fam']} ({o['sc']})")
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
                        t = (f"{run} {X}: {row['line']} {row['plane']} {row['v']:.4f} {row['tgt']} ({row['sc']}) via {s['line']} {s['plane']} "
                             f"{s['v']:.4f} ({s['sc']}); {y['line']} {y['plane']} {y['v']:.4f} {y['tgt']} ({y['sc']}); {z['line']} {z['plane']} "
                             f"{z['v']:.4f} {z['tgt']} ({z['sc']})")
                        P['P1'].append(t)
                        if min(sc(s), sc(y), sc(z)) >= 50:
                            P['P2'].append(t)
                            if sc(row) >= 50: P['P3'].append(t)
                        rep = [o for o in b.O if fam(o) and ' → ' in o['line'] and o['line'].endswith(f'{c} {X}') and not o['line'].startswith('S Moon')
                               and o['line'] != f'S {e} → {c} {X}' and any(o['fam'] == yy['fam'] and str(o['tgt']) == str(yy['tgt']) for yy in ys)]
                        if rep: P['P4'].append(t + f" | repeat {rep[0]['line']} {rep[0]['plane']} {rep[0]['v']:.4f} {rep[0]['tgt']} ({rep[0]['sc']})")
out += ['', '## P4 watch (Athmad Pluto loop) and P1-P3']
for v in ('P1', 'P2', 'P3', 'P4'):
    hs = sorted({t.split(':')[0].rsplit(' ', 1)[0] for t in P[v]})
    out.append(f"- {v}: {', '.join(hs) or 'none'}")
    if v in ('P3', 'P4'):
        out += [f'  - {t}' for t in sorted(set(P[v]))]
out += ['', '## S Pluto -> natal Pluto scoring'] + ([f'- {t}' for t in pl] or ['- none'])
out += ['', '## Jupiter loop (watch C; A, B, D listed too)']
jl = []
for run, bodies in data.items():
    if 'Jupiter' in bodies:
        jl += [f"- {run} [{''.join(sorted(t))}]: {txt}" for t, txt in JL.loops('Jupiter', bodies['Jupiter'])]
out += jl or ['- none']
out += ['', '## N2 / N4 watch (Whitefeathersfall)']
n2, n4 = [], []
for rid_cases in [J['rules'].get('BB29', [])]:
    for c in rid_cases:
        if c.get('watch_only'): continue
        for x in c['cells']:
            if ('conj' in x or 'contraparallel' in x) and ' → ' in x and x.split(' → ')[1].split(' ')[1] == c['body'] \
               and float(x.rsplit('(', 1)[1].rstrip(')')) >= 90:
                n2.append(f"- N2 {c['runner']} {c['body']}: {x}")
for x in runners:
    if all(set(cb) <= hold[x] for cb in (('BB3', 'BB63'), ('BB3', 'BB54'), ('BB59',))):
        n4.append(f"- N4 {x}: BB3 + BB63, BB3 + BB54, BB59")
out += (sorted(set(n2)) + n4) or ['- none']
out += ['', '## Mirror watch (Society Red Venus; M4 = mirror >= 90 + sky body + royal star on sky X)']
mr = []
for run, bodies in data.items():
    for X, d in bodies.items():
        for t, s_ in MR.cases(X, d, set(bodies) | {'Rahu', 'Ketu'}):
            mr.append(f"- {run} [{', '.join(k for k in MR.KEYS if k in t)}]: {s_}")
out += mr or ['- none']
out += ['', '## Royal star both natal X watch (Dynamic Force Jupiter Antares; A2 = same royal star on natal X both charts, same plane, one '
        'same-body ratio >= 50, the other chart\'s line in a family carried by a sky pair >= 90 naming sky X)']
rb = []
for run, bodies in data.items():
    for X, d in bodies.items():
        for t, s_ in RB.cases(X, d):
            if 'A1' in t:
                rb.append(f"- {run} {X} [{' '.join(sorted(t))}]: {s_}")
out += rb or ['- none']
out += ['', '## One sky body on both natal X watch (Blue Collar Glory Venus / Ketu; K1d = H X – J X in Dec >= 90 + a sky body on H X and J X '
        '>= 90; K2 = + that body in a sky pair on the H X – J X number)']
hb = []
for run, bodies in data.items():
    for X, d in bodies.items():
        for t, s_ in HB.cases(X, d):
            if 'K1' in t:
                hb.append(f"- {run} {X} [{' '.join(sorted(t))}]: {s_}")
out += hb or ['- none']
out += ['', '## Regulus on 11 watch (Aldhaja Rahu, Domandlouis Jupiter; R11 = a Regulus natal line with a same-body or crossed ratio on '
        '11 scoring >= 90; R11w = 50-90)']
r11 = []
for run, bodies in data.items():
    for X, d in bodies.items():
        for x in d['L']:
            if not x['line'].startswith(('H Regulus – ', 'J Regulus – ')):
                continue
            for kind, t, sc, base in (('same-body', x['rt'], x['rs'], x['sb'] and f"{x['sb']} {x['plane']}"), ('crossed', x['xt'], x['xs'], x['xb'])):
                m = RC.CUT.match(str(t or ''))
                if m and m.group(1) == '11' and sc is not None and sc >= 50:
                    tag = 'R11' if sc >= 90 else 'R11w'
                    fam = f"{x['tgt']} {x['fam']} ({x['sc']})" if x['fam'] else '(no family)'
                    r11.append((-sc, f"- {run} {X} [{tag}]: {x['line']} {x['plane']} {x['v']:.6f} {fam}; {kind} ratio vs {base} = "
                                     f"{(x['r'] if kind == 'same-body' else x['xr']):.6f} {t} ({sc})"))
out += [t for _, t in sorted(r11)] or ['- none']
out += ['', '## Same royal star in the sky pair watch (Eydon Jupiter; G0s = a natal royal line R – X carried by S Y – S R, both >= 90; '
        'G1 + sky X on natal Y, G2 + a Sun / Moon line on sky X, G2s light >= 90)']
ey = []
for run, bodies in data.items():
    cs = EY.cases(bodies)
    for t in cs.get('G0s', []):
        tags = [k for k in ('G1', 'G2', 'G2s') if any(u.startswith(t) for u in cs.get(k, []))]
        ey.append(f"- {run} [G0s{' ' + ' '.join(tags) if tags else ''}]: {t}")
out += ey or ['- none']
out += ['', '## Jupiter–Jupiter on a sky number watch (River Bray, Society Red; J1any = H Jupiter – J Jupiter in a number family, any score, '
        'with 2+ sky pairs on its target; J1any+B68 = and BB68 held)']
b68 = {c['runner'] for c in J['rules']['BB68'] if not c['watch_only']}
jj = []
for run, bodies in data.items():
    t, txt = RBY.tags(bodies, run in b68)
    if 'J1any' in t:
        jj.append(f"- {run} [{'J1any+B68' if 'J1any+B68' in t else 'J1any'}]: {txt}")
out += jj or ['- none']
txt = '\n'.join(out) + '\n'
open(f'docs/eddie_read/bybody_rules/{race}_watch.md', 'w').write(txt); print(txt)
