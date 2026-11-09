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
def strip_new(X, rows):
    # rows added after the verified file (8 Nov 2026): H X – J X lines, S Y → natal X rows in the same-target section,
    # and same-target rows matched to an H X – J X line
    hj = f'| H {X} – J {X} |'
    out, sec = [], 0
    for l in rows:
        if l.startswith(hj):
            continue
        c = [x.strip() for x in l.strip('|').split('|')]
        if len(c) == 5 and (c[4] == '' or ': ratio ' in c[4]):     # line row: drop the same-body ratio column (9 Nov 2026)
            l = '| ' + ' | '.join(c[:4]) + ' |'
            out.append(l)
            continue
        if len(c) == 5 and ('→' in c[0] or c[4].startswith(f'H {X} – J {X}')):
            continue
        out.append(l)
    return out
for X in ref:
    check(ref[X] == strip_new(X, new.get(X, [])), f'1 {X} rows identical to the verified file (new rows set aside)')

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
            good &= sum(1 for l in b['lines'] if 'contraparallel' not in l['plane']) == 20 - 10 * len(r['missing']) + (0 if r['missing'] else 2)
            good &= not any(l['line'].split(' ')[-2] in r['missing'] for l in b['lines'] + b['other'])
            good &= desc(b['matches'], lambda m: m['hit'][2])
            tg = {(h[0], h[1]): f"{l['line']} {l['plane']}" for l in b['lines'] for h in l['hits'] if h[0] != 'conj'}
            mk = {(m['line'], m['plane'], m['hit'][1], m['matches']) for m in b['matches']}
            for o in b['other']:
                if '→' in o['line']:
                    for h in o['hits']:
                        if h[0] != 'conj':
                            for l in b['lines']:
                                if any((x[0], x[1]) == (h[0], h[1]) for x in l['hits']):
                                    good &= (o['line'], o['plane'], h[1], f"{l['line']} {l['plane']}") in mk
            hjl = [l for l in b['lines'] if l['line'].startswith('H ') and ' – J ' in l['line']]
            if not r['missing']:
                X = b['body']
                hra, jra = r['ra']['H'][X], r['ra']['J'][X]
                d = abs(hra - jra) % 360
                good &= abs(next(l['value'] for l in hjl if l['plane'] == 'RA') - min(d, 360 - d)) < 1e-9
                good &= abs(next(l['value'] for l in hjl if l['plane'] == 'Dec') - abs(r['pos']['H'][X] - r['pos']['J'][X])) < 1e-9
            grp = [0 if ' – ' in o['line'] else (1 if '→ H ' in o['line'] else 2) for o in b['other']]
            good &= grp == sorted(grp)
            for g in (0, 1, 2):
                good &= desc([o for o, k in zip(b['other'], grp) if k == g], lambda o: o['hits'][0][2])
    check(good, f'4 {os.path.basename(f)} structure and order')
# 5 Excel output = the same rows as the .md content (every runner of Catterick)
import openpyxl
with tempfile.TemporaryDirectory() as td:
    xp = os.path.join(td, 'x.xlsx')
    BB.write_xlsx(xp, '20220406_catterick_1440', res)
    wb = openpyxl.load_workbook(xp)
    check(len(wb.sheetnames) == len(res), '5 one sheet per runner')
    for (c_, (r, bodies)), sn in zip(res.items(), wb.sheetnames):
        got = [x for x in wb[sn].iter_rows(values_only=True) if x[0] and x[1] is not None and x[0] != 'Line']
        want = []
        for b in bodies:
            for l in b['lines']:
                want.append((l['line'], l['plane'], round(l['value'], 6), round(l['hits'][0][2], 2) if l['hits'] else None))
            for m in b['matches']:
                want.append((m['line'], m['plane'], round(m['value'], 6), round(m['hit'][2], 2)))
            for o in b['other']:
                want.append((o['line'], o['plane'], round(o['value'], 6), round(o['hits'][0][2], 2)))
        check([(g[0], g[1], g[2], g[5]) for g in got] == want, f'5 {sn} rows = the .md rows ({len(want)})')
        wr = [(l['ratio']['same'], l['ratio']['ratio']) for b in bodies for l in b['lines'] if 'ratio' in l]
        gr = [(g[9], g[10]) for g in got if len(g) > 9 and g[8]]
        check(len(gr) == len(wr) and all(abs(a - round(c, 6)) < 1e-9 and (b is None or abs(b - round(d, 6)) < 1e-9)
                                          for (a, b), (c, d) in zip(gr, wr)), f'5 {sn} ratio columns ({len(wr)})')
        score_cells = [wb[sn].cell(i, 6) for i in range(1, wb[sn].max_row + 1) if isinstance(wb[sn].cell(i, 6).value, (int, float))]
        check(all(sc.fill.fgColor.rgb[-6:] == BB._fill(sc.value) for sc in score_cells), f'5 {sn} score fills')
# 6 same-body ratio on the royal-star rows (Eddie, 9 Nov 2026)
uv = {(l['line'], l['plane']): l for l in next(b for b in b5 if b['body'] == 'Uranus')['lines']}
rt = uv[('H Fomalhaut – H Uranus', 'RA')]['ratio']
check(abs(rt['same'] - 11.2375) < 5e-5 and abs(rt['ratio'] - uv[('H Fomalhaut – H Uranus', 'RA')]['value'] / rt['same']) < 1e-12
      and rt['hits'][0][0] == '4' and abs(rt['hits'][0][2] - 100 * (0.02 - abs(rt['ratio'] - 4)) / 0.02) < 1e-9,
      '6 Wotever Next H Fomalhaut – H Uranus RA ratio 3.9948 on 4 (linear, ±0.02)')
check(not uv[('H Regulus – H Uranus', 'RA')]['ratio']['hits'], '6 H Regulus – H Uranus RA 10.9272 no target (10 ±0.5 % = 9.95–10.05)')
check(abs(BB.ratio_hits(111.24 / 11.09)[0][2] - 100 * (0.05 - abs(111.24 / 11.09 - 10)) / 0.05) < 1e-9, '6 Perfect Part 10.03 on 10')
check(BB.ratio_hits(133 / 6.657)[0][0] == '20', '6 Pholas 19.98 on 20')
check(BB.ratio_hits(28 / 21)[0][0] == '4/3', '6 Dettori 28 / 21 on 4/3')
good = True
for f in files:
    for c_, (r, bodies) in BB.run(f).items():
        for b in bodies:
            for l in b['lines']:
                royal = any(l['line'].startswith(f'{ch} {Y} – ') for ch in 'HJ' for Y in BB.ROYAL) and 'contra' not in l['plane']
                if not royal:
                    good &= 'ratio' not in l
                    continue
                ch = l['line'][0]
                sv = r['dist'][ch].get(('S', l['plane'], b['body'], b['body']))
                if sv is None or not min(sv, l['value']) > 0:
                    good &= 'ratio' not in l
                    continue
                rt = l['ratio']
                q = max(sv, l['value']) / min(sv, l['value'])
                good &= abs(rt['ratio'] - q) < 1e-9 and abs(rt['pct'] - 100 * sv / l['value']) < 1e-9
                if min(sv, l['value']) < BB.CONJ[l['plane']]:
                    good &= not rt['hits'] and rt.get('note') == 'conjunction leg, not scored'
                else:
                    want = sorted([(lab, n, 100 * (t - abs(q - v)) / t) for lab, n, v, t in BB.RATIO_TARGETS if abs(q - v) < t],
                                  key=lambda h: -h[2])
                    good &= rt['hits'] == want
check(good, '6 every royal-star row on every _active file: ratio, %, hits; no ratio elsewhere')
rc = BB.run(os.path.join(ROOT, 'reference/classic/race_batch_20240118_chelmsford_aw_1320_active.xlsx'))
check(rc[1][0]['missing'] == ['J'] and 'No birth date for the jockey' in BB.md('x', rc[1][0], rc[1][1]), '4 jockey without birth date noted')
print(f'{ok}/{ok + bad}')
