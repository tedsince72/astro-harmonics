"""Scan (16 Nov 2026, Eddie: 'look at the scoring over 100 - seems to cause some noise; find the strongest rules and see how distances
over 100 may affect those or not'). Read-only; does not change any rule or tool.

1. Every BB rule over the 8 result races: picks (runners holding it), winners, by chance (sum of holders / field size), and the same over
   the races AFTER the rule's origin race ('later').
2. The same rules re-run on the bybody data with every distance > 100 degrees taken out of the families:
   A  a row (Lines, Sky lines on the same target, Other) whose value is > 100 has no family (an S / O row is dropped);
   B  A + a same-body / crossed ratio is dropped when either of its two distances is > 100.
   C  A, but oppositions (all near 180) kept.
   Variant A also drops end lines > 100 that a rule needs besides its main hit (checker, 16 Nov).
   Per rule: picks / winners / chance before -> A -> B, and the share of the holders' cells with a value > 100.
"""
import copy, json, sys
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E

RACES = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad')]


def origin(rid):
    k = int(rid[2:].rstrip('b'))
    for lim, i in ((17, 0), (31, 1), (40, 2), (50, 3), (56, 4), (60, 5), (62, 6), (64, 7)):
        if k <= lim:
            return i
    return 7


big = lambda x: E.num(x) and x > 100


def strip(data, mode):
    d2 = copy.deepcopy(data)
    cut = (lambda r: big(r['v']) and r.get('fam') != 'opposition') if mode == 'C' else (lambda r: big(r['v']))
    for run, bodies in d2.items():
        for X, d in bodies.items():
            for r in d['L']:
                if cut(r):
                    r['fam'] = r['tgt'] = r['sc'] = None
                if mode == 'B':
                    if big(r['v']) or big(r['sbv']):
                        r['rt'] = r['rs'] = None
                    if big(r['v']) or big(r['xbv']):
                        r['xt'] = r['xs'] = None
            d['S'] = [r for r in d['S'] if not cut(r)]
            d['O'] = [r for r in d['O'] if not cut(r)]
    return d2


def holders(data):
    res = {rid: {} for rid, _, _ in E.RULES}
    for rid, fn, _ in E.RULES:
        if fn is None:  # BB67 is built from the other rules' holders (below)
            continue
        for run, D in data.items():
            for X, d in D.items():
                b = E.Body(X, d); b.all = D
                seen = set()
                for case in fn(b):
                    if case.get('watch_only') or case['key'] in seen:
                        continue
                    seen.add(case['key'])
                    cl = res[rid].setdefault(run, [])
                    for c in case['cells']:
                        if (c['line'], c['plane'], c['tgt']) not in {(x['line'], x['plane'], x['tgt']) for x in cl}:
                            cl.append(c)
    return res


T = {m: {} for m in ('0', 'A', 'B', 'C')}
share = {}
for i, (n, r, w) in enumerate(RACES):
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
    for m, dd in (('0', data), ('A', strip(data, 'A')), ('B', strip(data, 'B')), ('C', strip(data, 'C'))):
        h = holders(dd)
        for rid, hs in h.items():
            t = T[m].setdefault(rid, [0, 0, 0.0, 0, 0, 0.0])
            won = any(w in x for x in hs)
            t[0] += len(hs); t[1] += won; t[2] += len(hs) / N
            if i > origin(rid):
                t[3] += len(hs); t[4] += won; t[5] += len(hs) / N
            if m == '0':
                s = share.setdefault(rid, [0, 0])
                for cells in hs.values():
                    s[0] += len(cells); s[1] += sum(1 for c in cells if big(c['v']))

ids = [rid for rid, _, _ in E.RULES]
f = lambda t: f"{t[0]} / {t[1]} ({t[2]:.1f})"
rank = sorted(ids, key=lambda k: -(T['0'][k][1] - T['0'][k][2]))
out = ['| Rule | all 8 races: picks / won (chance) | later races | > 100 cells (distinct per runner) | A: no family > 100 | B: + ratios | C: A but opposition kept |',
       '|---|---|---|---|---|---|---|']
for k in rank:
    t = T['0'][k]; s = share[k]
    lat = f"{t[3]} / {t[4]} ({t[5]:.1f})" if t[3] or origin(k) < 7 else '—'
    out.append(f"| {k} | {f(t)} | {lat} | {s[1]} of {s[0]} | {f(T['A'][k])} | {f(T['B'][k])} | {f(T['C'][k])} |")
for m in ('0', 'A', 'B', 'C'):
    P = sum(T[m][k][0] for k in ids); W = sum(T[m][k][1] for k in ids); C = sum(T[m][k][2] for k in ids)
    out.append(f"\nAll rules {m}: {P} picks, {W} winners, {C:.1f} by chance")
print('\n'.join(out))
json.dump({m: T[m] for m in T} | {'share': share}, open('/tmp/bb_over100.json', 'w'))

# 3. Cells of rule holders with a value > 100: by family, winners' cells vs the others' (distinct per runner within each rule; a cell
#    held under several rules counts once per rule)
from collections import Counter
cw, cl = Counter(), Counter(); nw = nl = 0
for n, r, w in RACES:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx')
    for rid, hs in holders(data).items():
        for run, cells in hs.items():
            for c in {(c['line'], c['plane'], c['v'], c['fam']) for c in cells}:
                tgt = cw if w in run else cl
                if w in run: nw += 1
                else: nl += 1
                if big(c[2]): tgt[c[3] or 'no family'] += 1
print('\nholder cells > 100 by family (winners | others; distinct within each rule):')
for fam in sorted(set(cw) | set(cl), key=lambda k: -(cw[k] + cl[k])):
    print(f"  {fam}: {cw[fam]} of {nw} winner cells ({100*cw[fam]/nw:.1f} %) | {cl[fam]} of {nl} other cells ({100*cl[fam]/nl:.1f} %)")
print(f"  all > 100: winners {sum(cw.values())} of {nw} ({100*sum(cw.values())/nw:.1f} %) | others {sum(cl.values())} of {nl} ({100*sum(cl.values())/nl:.1f} %)")
