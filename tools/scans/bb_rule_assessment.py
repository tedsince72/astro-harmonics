"""Scan (16 Nov 2026, Eddie: 'run each rule through an assessment for distances, families, bodies, RA or Dec or both ... I strongly
suspect Dec is more important'). Read-only; no rule or tool changed. 8 result races, every BB rule (watch-only cases left out).

1. Cells of rule cases (distinct per runner within each rule): winners' cells vs the others', by plane, distance band, family, score.
2. Cases (one per rule case key; a runner-body can hold several cases in a rule): plane mix all RA / all Dec / both; winners vs
   others. (Checker, 16 Nov: one per rule, runner, body gives winners 26 / 12 / 147, others 77 / 60 / 479 - same picture.)
3. Body: runners holding any rule on body X per race -> picks / winners / chance.
4. The rules re-run on one plane only: 'Dec only' = every RA row loses its family (an S / O row is dropped) and the crossed ratio on a
   Dec row (it uses the RA same-body leg) is dropped; 'RA only' the same the other way. Per rule and in total: picks / winners / chance,
   all races and later races (after the rule's origin race).
"""
import copy, sys
from collections import Counter, defaultdict
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
from bb_over100_tighten import RACES, holders, origin

pl = lambda p: 'Dec' if str(p).startswith('Dec') else 'RA'


def band(v):
    if not E.num(v):
        return '?'
    return '<1.5' if v < 1.5 else '1.5-10' if v < 10 else '10-30' if v < 30 else '30-60' if v < 60 else '60-100' if v < 100 else '>100'


def sband(s):
    s = s or 0
    return '<25' if s < 25 else '25-50' if s < 50 else '50-80' if s < 80 else '>=80'


def one_plane(data, keep):
    d2 = copy.deepcopy(data)
    for run, bodies in d2.items():
        for X, d in bodies.items():
            for r in d['L']:
                if pl(r['plane']) != keep:
                    r['fam'] = r['tgt'] = r['sc'] = None; r['rt'] = r['rs'] = None
                r['xt'] = r['xs'] = None          # the crossed ratio always uses the other plane
            d['S'] = [r for r in d['S'] if pl(r['plane']) == keep]
            d['O'] = [r for r in d['O'] if pl(r['plane']) == keep]
    return d2


cw = defaultdict(Counter); cl = defaultdict(Counter); nw = nl = 0
mixw, mixl = Counter(), Counter()
body = defaultdict(lambda: [0, 0, 0.0])
T = {m: defaultdict(lambda: [0, 0, 0.0, 0, 0, 0.0]) for m in ('0', 'Dec', 'RA')}
for i, (n, r, w) in enumerate(RACES):
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
    # per-body cases for 2 and 3
    fns = {rid: fn for rid, fn, _ in E.RULES}
    bh = defaultdict(set)
    for rid, fn in fns.items():
        for run, D in data.items():
            for X, d in D.items():
                b = E.Body(X, d); b.all = D; seen = set()
                for case in fn(b):
                    if case.get('watch_only') or case['key'] in seen:
                        continue
                    seen.add(case['key'])
                    bh[case.get('body', X)].add(run)
                    ps = {pl(c['plane']) for c in case['cells']}
                    (mixw if w in run else mixl)['both' if len(ps) == 2 else 'all ' + ps.pop()] += 1
    for X, hs in bh.items():
        t = body[X]; t[0] += len(hs); t[1] += any(w in x for x in hs); t[2] += len(hs) / N
    for m, dd in (('0', data), ('Dec', one_plane(data, 'Dec')), ('RA', one_plane(data, 'RA'))):
        for rid, hs in holders(dd).items():
            t = T[m][rid]; won = any(w in x for x in hs)
            t[0] += len(hs); t[1] += won; t[2] += len(hs) / N
            if i > origin(rid):
                t[3] += len(hs); t[4] += won; t[5] += len(hs) / N
            if m == '0':
                for run, cells in hs.items():
                    tgt = cw if w in run else cl
                    for c in cells:
                        if w in run: nw += 1
                        else: nl += 1
                        tgt['plane'][pl(c['plane'])] += 1; tgt['band'][band(c['v'])] += 1
                        tgt['family'][c['fam'] or 'no family'] += 1; tgt['score'][sband(c['sc'])] += 1

print(f'## 1. Cells of rule cases: winners {nw} | others {nl} (distinct per runner within each rule)')
for k in ('plane', 'band', 'family', 'score'):
    print(f'\n{k}:')
    for v in sorted(set(cw[k]) | set(cl[k]), key=lambda x: -(cw[k][x] + cl[k][x])):
        a, b = cw[k][v], cl[k][v]
        print(f'  {v}: winners {a} ({100 * a / nw:.1f} %) | others {b} ({100 * b / nl:.1f} %)')
print('\n## 2. Cases by plane mix (winners | others)')
tw, tl = sum(mixw.values()), sum(mixl.values())
for v in ('all RA', 'all Dec', 'both'):
    print(f'  {v}: {mixw[v]} ({100 * mixw[v] / tw:.1f} %) | {mixl[v]} ({100 * mixl[v] / tl:.1f} %)')
print('\n## 3. Body: runners holding any rule on that body (picks / winners / chance)')
for X, (p, wn, c) in sorted(body.items(), key=lambda kv: -(kv[1][1] - kv[1][2])):
    print(f'  {X}: {p} / {wn} ({c:.1f})')
print('\n## 4. Rules on one plane only (picks / winners (chance); later races)')
ids = [rid for rid, _, _ in E.RULES]
f = lambda t: f'{t[0]} / {t[1]} ({t[2]:.1f})'
fl = lambda t: f'{t[3]} / {t[4]} ({t[5]:.1f})'
for m in ('0', 'Dec', 'RA'):
    P = sum(T[m][k][0] for k in ids); W = sum(T[m][k][1] for k in ids); C = sum(T[m][k][2] for k in ids)
    Pl = sum(T[m][k][3] for k in ids); Wl = sum(T[m][k][4] for k in ids); Cl = sum(T[m][k][5] for k in ids)
    print(f'  {m}: all races {P} / {W} ({C:.1f}, {W / C:.2f}x); later {Pl} / {Wl} ({Cl:.1f}, {Wl / Cl if Cl else 0:.2f}x)')
print('\n| Rule | as built | later | Dec only | later | RA only | later |\n|---|---|---|---|---|---|---|')
for k in sorted(ids, key=lambda k: -(T['0'][k][1] - T['0'][k][2])):
    print(f"| {k} | {f(T['0'][k])} | {fl(T['0'][k])} | {f(T['Dec'][k])} | {fl(T['Dec'][k])} | {f(T['RA'][k])} | {fl(T['RA'][k])} |")
