#!/usr/bin/env python3
"""Checks for tools/eddie_bybody.py (Eddie, 8 Nov 2026).
1. Catterick 14:40 6 Apr 2022 cloth 5 Wotever Next / Joanna Mason = tests/ref/catterick_1440_20220406_wotever_by_body_verified.md
   (built and checked by independent checkers in the session, 0 mismatches), row for row in every section.
2. Hand cases (from the workbook values, scored by hand on the rules).
3. Scoring rules: an own scorer (no code shared with the tool) on every hit of the Catterick runners.
4. Every _active.xlsx in reference/classic: every runner has 24 body sections, 20 distance lines each (+ contraparallels),
   every 'Sky lines on the same target' / 'Other scoring sky lines' group in descending score."""
import glob, math, os, re, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import eddie_bybody as BB  # noqa: E402

ok = bad = 0
def check(cond, what):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', what)

CAT = os.path.join(ROOT, 'reference/classic/race_batch_20220406_catterick_1440_active.xlsx')
res = BB.run(CAT)
r5, b5 = res[5]
doc = BB.md('20220406_catterick_1440', r5, b5)

def rows_by_section(s):
    s = s.replace('Dec (signed)', 'Dec contraparallel')
    out = {}
    for part in s.split('\n## ')[1:]:
        X = part.split('\n', 1)[0].strip()
        out[X] = [l for l in part.split('\n') if l.startswith('|') and not l.startswith(('|---', '| Line', '| Sky line'))]
    return out

ref = rows_by_section(open(os.path.join(HERE, 'ref/catterick_1440_20220406_wotever_by_body_verified.md')).read())
new = rows_by_section(doc)
check(list(ref) == list(new) and len(new) == 24, '1 same 24 sections in order')
for X in ref:
    check(ref[X] == new.get(X), f'1 {X} rows identical to the verified file')

# 2 hand cases (values from the workbook; scores by hand)
def row(X, line, plane):
    b = next(b for b in b5 if b['body'] == X)
    return next(l for l in b['lines'] if l['line'] == line and l['plane'] == plane)
c = row('Ceres', 'S Ceres → H Ceres', 'RA')        # 179.966337: opposition 100 (0.75 - 0.033663) / 0.75 = 95.51
check(abs(c['value'] - 179.966337) < 1e-5 and c['hits'][0][0] == 'opposition' and abs(c['hits'][0][2] - 95.5116) < 0.01, '2 opposition')
c = row('Ceres', 'H Fomalhaut – H Ceres', 'Dec')    # 12.9983: whole 13, 100 (0.02 - 0.0017) / 0.02 = 91.3
check(c['hits'][0][:2] == ('whole', '13') and abs(c['hits'][0][2] - 91.3) < 0.1, '2 whole 13')
c = row('Ceres', 'H Aldebaran – H Ceres', 'Dec contraparallel')   # -16.6254 + 16.5074 -> 0.1181, 100 (0.3 - 0.1181) / 0.3 = 60.6
check(c['hits'][0][0] == 'contraparallel' and abs(c['value'] - 0.1181) < 1e-3 and abs(c['hits'][0][2] - 60.6) < 0.1, '2 contraparallel')
c = row('Jupiter', 'H Antares – H Jupiter', 'RA')   # 16.1872: 10×φ (0.0069 of 0.0324 -> 78.7), also 10φ phi power (tol 0.02427 -> 71.5)
check([h[:2] for h in c['hits']] == [('golden', '10×φ'), ('phi power', '10φ')] and abs(c['hits'][0][2] - 78.7) < 0.1
      and abs(c['hits'][1][2] - 71.5) < 0.1, '2 golden + phi power overlap')
c = row('Mercury', 'J Regulus – J Mercury', 'RA')   # 141.4422: √2 141.4214, tol 0.2121 -> 90.2
check(c['hits'][0][:2] == ('sqrt2', '141.4') and abs(c['hits'][0][2] - 90.2) < 0.1, '2 sqrt2')
c = row('Neptune', 'J Aldebaran – J Neptune', 'RA')  # 144.4702: ninth 144.444, tol 0.2889 -> 91.1
check(c['hits'][0][:2] == ('ninth', '144.444') and abs(c['hits'][0][2] - 91.1) < 0.1, '2 ninth 0.2 %')
ce = next(b for b in b5 if b['body'] == 'Ceres')
check(any(o['line'] == 'S Neptune → H Ceres' and o['plane'] == 'Dec' and o['hits'][0][1] == '13' for o in ce['other']),
      '2 other: S Neptune -> H Ceres Dec 13')
check(not any(o['line'].startswith('S Ceres') and '→' not in o['line'] for o in ce['other']), '2 other: centre never a partner')

# 3 own scorer on every hit of all Catterick runners
PHI = (1 + 5 ** .5) / 2
def own(v, plane):
    hs = {}
    def add(f, l, s):
        if f not in hs or s > hs[f][1]:
            hs[f] = (l, s)
    t = round(v)
    if 1 <= t <= 200 and abs(v - t) < 0.02:
        add('whole', str(t), 100 * (0.02 - abs(v - t)) / 0.02)
    k = round(v / PHI)
    if 1 <= k <= 124 and abs(v - k * PHI) < 0.0324:
        add('golden', f'{k}×φ', 100 * (0.0324 - abs(v - k * PHI)) / 0.0324)
    c = 1.5 if plane == 'RA' else 0.3
    if v < c:
        add('conj', '0', 100 * (c - v) / c)
    if plane == 'RA' and 180 - v < 0.75:
        add('opposition', '180', 100 * (0.75 - (180 - v)) / 0.75)
    return hs
n = 0
for c_, (r, bodies) in res.items():
    for b in bodies:
        for ln in b['lines'] + b['other']:
            if 'contraparallel' in ln['plane']:
                continue
            o = own(ln['value'], ln['plane'])
            mine = {h[0]: (h[1], h[2]) for h in ln['hits'] if h[0] in ('whole', 'golden', 'conj', 'opposition')}
            n += 1
            if set(o) != set(mine) or any(o[f][0] != mine[f][0] or abs(o[f][1] - mine[f][1]) > 1e-6 for f in o):
                check(False, f'3 {c_} {ln["line"]} {ln["plane"]} {ln["value"]}: own {o} tool {mine}')
check(n > 2000, f'3 own scorer covered {n} lines')

# 4 every active file: structure and order
def desc(xs, key):
    return all(key(xs[i]) >= key(xs[i + 1]) - 1e-9 for i in range(len(xs) - 1))
files = sorted(glob.glob(os.path.join(ROOT, 'reference/classic/race_batch_*_active.xlsx')))
for f in files:
    rr = BB.run(f)
    good = True
    for c_, (r, bodies) in rr.items():
        good &= len(bodies) == 24
        for b in bodies:
            good &= sum(1 for l in b['lines'] if 'contraparallel' not in l['plane']) == 20 - 10 * len(r['missing'])
            good &= not any(l['line'].split(' ')[-2] in r['missing'] for l in b['lines'] + b['other'])
            good &= desc(b['matches'], lambda m: m['hit'][2])
            grp = [0 if ' – ' in o['line'] else (1 if '→ H ' in o['line'] else 2) for o in b['other']]
            good &= grp == sorted(grp)
            for g in (0, 1, 2):
                good &= desc([o for o, k in zip(b['other'], grp) if k == g], lambda o: o['hits'][0][2])
    check(good, f'4 {os.path.basename(f)} structure and order')
rc = BB.run(os.path.join(ROOT, 'reference/classic/race_batch_20240118_chelmsford_aw_1320_active.xlsx'))
check(rc[1][0]['missing'] == ['J'] and 'No birth date for the jockey' in BB.md('x', rc[1][0], rc[1][1]), '4 jockey without birth date noted')
print(f'{ok}/{ok + bad}')
