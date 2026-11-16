"""Watch items on one race (16 Nov 2026; read blind, never reads results). Usage: python3 tools/scans/bb_watch_race.py <race>
(race = the bybody folder name, e.g. 20220717_newton_abbot_1525). Items kept from the 16 Nov discussions (RULE_CANDIDATES.md):
- rules held per runner (as built, from docs/eddie_read/bybody_rules/<race>_bbrules.json) and under T2 (tolerances above 100 tightened:
  ninth, φ power, √2, silver ±0.05, opposition ±0.25; tools/scans/bb_over100_tighten.py)
- combinations to watch: BB3 + BB63, BB3 + BB54, BB59, BB48 + BB55, BB13 + BB48 + BB55, BB32 + BB34
- P4 (Athmad Pluto loop; tools/scans/bb_fieldcheck_same_body_loop_closed.py) and its looser P1-P3
- S Pluto -> H Pluto / J Pluto scoring (any family, conj / cp not counted).
- Jupiter loop C (Eddie, 16 Nov 2026, from Cafe Sydney; tools/scans/bb_fieldcheck_jupiter_loop.py): S Jupiter -> c Jupiter, a sky
  pair on its target, both ends on the same natal Jupiter, line and pair >= 50; versions A, B, D listed too."""
import json, sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_over100_tighten as TT
import bb_fieldcheck_jupiter_loop as JL

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
for combo in (('BB3', 'BB63'), ('BB3', 'BB54'), ('BB59',), ('BB48', 'BB55'), ('BB13', 'BB48', 'BB55'), ('BB32', 'BB34')):
    a = [x for x in runners if set(combo) <= hold[x]]; b = [x for x in runners if set(combo) <= t2[x]]
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
txt = '\n'.join(out) + '\n'
open(f'docs/eddie_read/bybody_rules/{race}_watch.md', 'w').write(txt); print(txt)
