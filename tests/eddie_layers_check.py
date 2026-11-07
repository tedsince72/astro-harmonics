#!/usr/bin/env python3
"""Checks for tools/eddie_layers.py (stage 2). Run from the repo root: python3 tests/eddie_layers_check.py
Recomputes cases 1, 2, 7 and the field tags from the stage 1 json with its own code; checks known cases by hand
(Fontwell 14:35: Paso Doble missing, Fire Flyer Ketu; Aintree 15:00: Rubaud Sedna; Aintree 13:50: All In You)."""
import glob, json, os, subprocess, sys
from collections import defaultdict
ok = bad = 0
def check(c, msg):
    global ok, bad
    if c: ok += 1
    else: bad += 1; print('FAIL', msg)
D = 'docs/eddie_read'
for f in sorted(glob.glob(f'{D}/*_eddie_read.json')):
    subprocess.run([sys.executable, 'tools/eddie_layers.py', f], check=True, capture_output=True)
def load(race):
    return json.load(open(f'{D}/race_batch_{race}_eddie_read.json')), json.load(open(f'{D}/race_batch_{race}_layers.json'))
def runner(L, name):
    return next(r for r in L['runners'] if name in L['report'][r]['name'])
def items(L, r, case):
    return L['report'][r]['cases'][str(case)]
# ---- every race: own recompute of cases 1 and 2, cell texts present in stage 1 md, field tags consistent
for f in sorted(glob.glob(f'{D}/*_eddie_read.json')):
    race = os.path.basename(f)[11:-16]
    S, L = load(race)
    md1 = open(f.replace('.json', '.md')).read()
    names = S['names']
    sb = defaultdict(list)
    for p in S['pieces']:
        if p['layer'] == 'same body' and (p['score'] is not None or p['note'] == 'loose'):
            sb[p['runner']].append(p)
    # (a same-body piece also carried by top rows is one cell; counts below are on same-body pieces)
    for r in S['runners']:
        hb = {p['body'] for p in sb[r] if p['chart'] == 'H'}; jb = {p['body'] for p in sb[r] if p['chart'] == 'J'}
        got1 = {it['label'] for it in items(L, r, 1)}
        check(got1 == hb & jb, f'{race} {r} case 1 {got1} vs {hb & jb}')
        pl = defaultdict(set)
        for p in sb[r]: pl[(p['chart'], p['body'])].add(p['plane'])
        exp2 = {f'{c} {b}' for (c, b), s in pl.items() if s >= {'RA', 'Dec'}}
        got2 = {it['label'] for it in items(L, r, 2)}
        check(got2 == exp2, f'{race} {r} case 2 {got2} vs {exp2}')
        check(len(L['report'][r]['same_bodies']) == len(sb[r]), f'{race} {r} L1 count')
        for c in range(1, 6):
            for it in items(L, r, c):
                for t in it['cells']:
                    core = t.split('] ', 1)[-1].split(' = ')[0]
                    v = core.split(' → ', 1)[1].split()  # chart body plane value ...
                    val = next(x for x in v if x.replace('.', '').isdigit() and '.' in x)
                    check(val in md1, f'{race} {r} value {val} not in stage 1 report')
    for r in S['runners']:
        n4 = sum(len(B['cells']) for B in L['report'][r]['bodies'])
        n1 = len({(p['source'], p['chart'], p['body'], p['plane'], round(p['value'], 6)) for p in S['pieces']
                  if p['runner'] == r and (p['score'] is not None or (p['layer'] == 'same body' and p['note'] == 'loose'))})
        check(n4 == n1, f'{race} {r} L4 cells {n4} vs {n1}')
    # field tags: same label in another runner's same case <=> 'also'
    lab = defaultdict(set)
    for r in S['runners']:
        for c in (1, 2, 4, 5):
            for it in items(L, r, c): lab[(c, it['label'])].add(r)
    for r in S['runners']:
        for c in (1, 2, 4):
            for it in items(L, r, c):
                others = lab[(c, it['label'])] - {r}
                check((it['field'] == 'only') == (not others), f'{race} {r} case {c} {it["label"]} field {it["field"]}')
# ---- by hand
S, L = load('20261106_fontwell_1435')
check(L['l0']['missing_in_tables'] == ['4 Paso Doble'], 'Fontwell Paso Doble missing')
check(L['l0']['cloth_gaps'] == [4], 'Fontwell cloth gap 4')
r = runner(L, 'Fire Flyer')
ket = next(B for B in L['report'][r]['bodies'] if B['body'] == 'Ketu')
kt = {c['text']: c for c in ket['cells']}
check('J Rigel → J Ketu Dec 0.0102 conj (93.31)' in kt, 'Fire Flyer J Rigel conj J Ketu in L4')
check('H Deneb → H Ketu RA 0.1096 conj (85.92)' in kt, 'Fire Flyer H Deneb conj H Ketu in L4')
check(kt.get('J Rigel → J Ketu Dec 0.0102 conj (93.31)', {}).get('field') == 'only', 'Fire Flyer Rigel on Ketu only')
check(any('S Moon → Rigel RA 110.9126' in t for t in kt.get('J Rigel → J Ketu Dec 0.0102 conj (93.31)', {}).get('source_lines', [])),
      'Fire Flyer Rigel source line')
check(any(it['label'] == '26 whole' and it['field'] == 'only' for it in items(L, r, 5)), 'Fire Flyer 26 on H Gonggong and J Juno')
check(not any('centres' in json.dumps(L['report'][x]) for x in L['runners']), 'no centre tags')
S, L = load('20261106_aintree_1500')
r = runner(L, 'Rubaud')
sed = next(x for x in L['report'][r]['landings'] if x['chart'] == 'H' and x['body'] == 'Sedna')
t = [q['text'] for q in sed['on_this_chart']]
check(any('H Zubenelgenubi → H Sedna RA 166.6568 166.667 ninth (99.15)' in x for x in t), 'Rubaud Sedna Zubenelgenubi')
check(any('H Zubeneschamali → H Sedna Dec 17.0016 17 whole (84.21)' in x for x in t), 'Rubaud Sedna Zubeneschamali')
pal = next(x for x in L['report'][r]['landings'] if x['body'] == 'Pallas' and x['chart'] == 'J')
check(any('S Moon → Pallas Dec 11.1105' in b for b in pal['body_lines']), 'Rubaud Pallas body line')
S, L = load('20261106_aintree_1350')
r = runner(L, 'All In You')
check('Makemake' in {it['label'] for it in items(L, r, 1)}, 'All In You Makemake both charts')
check('J Sun' in {it['label'] for it in items(L, r, 2)}, 'All In You J Sun both planes')
check(any('J Makemake Dec 13.0023' in c for it in items(L, r, 3) for c in it['cells']), 'All In You J Makemake 13 = sky')
check(any(it['label'].startswith('4 = 360/90') for it in items(L, r, 4)), 'All In You Sedna 4 = 360/90')
print(f'{ok}/{ok + bad}')
sys.exit(1 if bad else 0)
