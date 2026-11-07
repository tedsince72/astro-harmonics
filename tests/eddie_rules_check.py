#!/usr/bin/env python3
"""Tests for stage 3: tools/eddie_rules.py and tools/eddie_backtest.py (Eddie, 7 Nov 2026).

  - every rule in rules.json has a function; rules output exists for every race in results.json
  - set A picks = the SUMMARY lines race_rows.py prints (section 9) for the same workbook
  - set B recomputed here from the stage 1 json (own code)
  - known cases: Aintree 13:50 All In You in B4, B5 (J Sun), B6 (Makemake); B1 / B3 / B4 in-sample records as written
    in claude/full-race-read-method.md (B1 winner held 11 of 14, 8.2 expected; version 4 6 of 14, 2.4; B4 6 picks, 2 won)
  - every horse in the workbooks is in its results order (non-runners apart); eddie_rules.py never reads results
  - back-test tallies recomputed here
"""
import contextlib
import io
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
ok = bad = 0


def check(c, msg):
    global ok, bad
    if c:
        ok += 1
    else:
        bad += 1
        print('FAIL', msg)


ER = os.path.join(ROOT, 'docs', 'eddie_read')
rules = json.load(open(os.path.join(ER, 'rules.json')))['rules']
results = {k: v for k, v in json.load(open(os.path.join(ER, 'results', 'results.json'))).items() if not k.startswith('_')}
import eddie_rules  # noqa: E402
import eddie_backtest  # noqa: E402

for r in rules:
    check(r['id'] in eddie_rules.RULES, f"rule {r['id']} has a function")
src = open(os.path.join(ROOT, 'tools', 'eddie_rules.py')).read()
check('results.json' not in src and "'results'" not in src, 'eddie_rules.py does not read results')

# run the rules fresh into a temp dir
tmp = '/tmp/eddie_rules_check'
os.makedirs(tmp, exist_ok=True)
for race in results:
    j = os.path.join(ER, f'race_batch_{race}_eddie_read.json')
    check(os.path.exists(j), f'{race} stage 1 json')
    with contextlib.redirect_stdout(io.StringIO()):
        eddie_rules.write(eddie_rules.run(j, rules), tmp, rules)
sel = {race: json.load(open(os.path.join(tmp, f'{race}_rules.json'))) for race in results}
for race, o in sel.items():
    saved = os.path.join(ER, 'rules', f'{race}_rules.json')
    check(os.path.exists(saved) and json.load(open(saved)) == o, f'{race} saved rules output = a fresh run')

# set A against race_rows.py's printed summary
AIDS = [r['id'] for r in rules if r['set'] == 'A']
for race, o in sel.items():
    wb = os.path.join(ROOT, 'reference', 'classic', o['workbook'])
    pr = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'race_rows.py'), wb], capture_output=True, text=True)
    txt = pr.stdout
    if 'SUMMARY (runners each rule picks out)' not in txt:
        check(False, f'{race}: race_rows.py printed no summary (rc {pr.returncode}) {pr.stderr[-300:]}')
        continue
    summ = txt[txt.index('SUMMARY (runners each rule picks out)'):]
    for rid in AIDS:
        m = re.search(rf'^\s+{re.escape(rid)}\s+(\d+): (.*)$', summ, re.M)
        printed = set() if m.group(2) == 'none' else set(re.findall(r'(P\d\d)', m.group(2)))
        got = next(set(r['selected']) for r in o['rules'] if r['id'] == rid)
        check(printed == got and int(m.group(1)) == len(got), f'{race} {rid}: printed {sorted(printed)} vs {sorted(got)}')


# set B recomputed
def sb(d):
    out = defaultdict(list)
    for p in d['pieces']:
        if p['layer'] == 'same body' and p.get('score') is not None and p['score'] >= 50:
            out[p['runner']].append(p)
    return out


for race, o in sel.items():
    d = json.load(open(os.path.join(ER, f'race_batch_{race}_eddie_read.json')))
    got = {r['id']: set(r['selected']) for r in o['rules']}
    fl = d['flags'].get('natal body on a strong line star', [])
    e1 = {c['runner'] for c in fl}
    e2 = {c['runner'] for c in fl if fl and abs(c['score'] - max(x['score'] for x in fl)) < 1e-6}
    hub = {c['runner'] for c in d['flags'].get('hub landing', [])}
    e3 = hub if len(hub) == 1 else e2
    s = sb(d)
    cnt = sorted((len(s.get(R, [])) for R in d['runners']), reverse=True)
    top = [R for R in d['runners'] if len(s.get(R, [])) == cnt[0]] if cnt and cnt[0] else []
    e4 = set(top) if len(top) == 1 and cnt[0] - (cnt[1] if len(cnt) > 1 else 0) >= 2 else set()
    e5 = {R for R, ps in s.items() if any({p['plane'] for p in ps if (p['chart'], p['body']) == k} >= {'RA', 'Dec'}
                                          for k in {(p['chart'], p['body']) for p in ps})}
    e6 = {R for R, ps in s.items() if any({p['chart'] for p in ps if p['body'] == X} >= {'H', 'J'} for X in {p['body'] for p in ps})}
    for rid, e in (('B1', e1), ('B2', e2), ('B3', e3), ('B4', e4), ('B5', e5), ('B6', e6)):
        check(got[rid] == e, f'{race} {rid}: {sorted(got[rid])} vs {sorted(e)}')

# known cases
a = {r['id']: r for r in sel['20261106_aintree_1350']['rules']}
check(a['B4']['selected'] == ['P07'] and a['B4']['cells']['P07'][0].startswith('7 same-body cells >= 50, next 4'), 'All In You B4 lead 7 vs 4')
check(a['B5']['selected'] == ['P07'] and a['B5']['cells']['P07'][0].startswith('J Sun:'), 'All In You B5 J Sun')
check('P07' in a['B6']['selected'] and any(c.startswith('Makemake:') for c in a['B6']['cells']['P07']), 'All In You B6 Makemake')
check(a['B3']['selected'] == ['P05'], 'Aintree 13:50 version 4 picks Manuelito')

# horses in results; back-test recomputed
for race, o in sel.items():
    res = results[race]
    for R, nm in o['names'].items():
        h = eddie_backtest.horse(nm)
        check(h in res['order'] or h in res.get('nonrunners', []), f'{race} {h} in the results')
    for k in res.get('not_in_workbook', []):
        check(k not in [eddie_backtest.horse(n) for n in o['names'].values()], f'{race} {k} not in the workbook')
    check(res['ran'] == len(res['order']), f'{race} ran = order length')
bt = json.load(open(os.path.join(ER, 'backtest', 'backtest.json')))
for r in rules:
    ins = set(r.get('in_sample', []))
    for part in ('test', 'in_sample', 'all'):
        n = dict(races=0, fired=0, picks=0, winners=0, top2=0, cw=0.0, c2=0.0, alone=0)
        for race in results:
            if (part == 'test' and race in ins) or (part == 'in_sample' and race not in ins):
                continue
            res, o = results[race], sel[race]
            n['races'] += 1
            nm = o['names']
            pk = [eddie_backtest.horse(nm[R]) for R in next(x['selected'] for x in o['rules'] if x['id'] == r['id'])]
            pk = [h for h in pk if h not in res.get('nonrunners', [])]
            if not pk:
                continue
            n['fired'] += 1
            n['picks'] += len(pk)
            w = sum(h in res['first'] for h in pk)
            n['winners'] += w
            n['top2'] += sum(h in res['first'] or h in res['second'] for h in pk)
            n['cw'] += len(pk) / res['ran']
            n['c2'] += len(pk) * (len(res['first']) + len(res['second'])) / res['ran']
            n['alone'] += 1 if len(pk) == 1 and w == 1 else 0
        t = bt[r['id']][part]
        check((t['races'], t['fired'], t['picks'], t['winners'], t['top2'], t['alone']) ==
              (n['races'], n['fired'], n['picks'], n['winners'], n['top2'], n['alone'])
              and abs(t['chance_w'] - n['cw']) < 1e-9 and abs(t['chance_2'] - n['c2']) < 1e-9, f"backtest {r['id']} {part}")
b = {k: bt[k]['in_sample'] for k in ('B1', 'B3', 'B4')}
check(b['B1']['fired'] == 14 and b['B1']['winners'] == 11 and round(b['B1']['chance_w'], 1) == 8.2, 'B1 in-sample 11 of 14 (8.2)')
check(b['B3']['picks'] == 14 and b['B3']['winners'] == 6 and round(b['B3']['chance_w'], 1) == 2.4, 'version 4 in-sample 6 of 14 (2.4)')
check(b['B4']['picks'] == 6 and b['B4']['winners'] == 2, 'B4 in-sample 6 picks, 2 won')

print(f'{ok}/{ok + bad}')
sys.exit(1 if bad else 0)
