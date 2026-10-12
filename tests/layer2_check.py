#!/usr/bin/env python3
"""layer2_check.py — Layer 2 tests: (1) the design examples; (2) on every race, every derived/mirror chain re-added from the actual
coordinates (independent of the tool's ninth bookkeeping): the chain's signed real distances must sum to the item's real distance
(Dec exactly; RA modulo 360); (3) every Layer 1 item has exactly one tag."""
import json, glob, os, sys
def wrap(x): return (x + 180) % 360 - 180
def tagged(race, P, pred):
    L1 = json.load(open(f'docs/classic/{race}/layer1/{P}.json')); L2 = json.load(open(f'docs/classic/{race}/layer2/{P}.json'))
    return L1, L2
fails = 0
def ok(cond, msg):
    global fails
    print(('  ok   ' if cond else '  FAIL ') + msg); fails += (not cond)
# (1) examples
L1, L2 = tagged('york_1615_20240515', 'P25', None)
def find(L1, sec, pred): return [f'{sec}:{i}' for i, x in enumerate(L1[sec]) if pred(x)]
def tag_of(L2, ids): return [L2['tags'].get(i, {}).get('tag') for i in ids]
ok(tag_of(L2, find(L1, 'strikes', lambda s: s['sky']=='Sun' and s['target']=='J Pallas' and s['plane']=='Dec' and s['num']=='33')) == ['derived'], 'York: sky Sun -> Mason Pallas Dec 33 derived (19 + 14)')
ok(tag_of(L2, find(L1, 'strikes', lambda s: s['sky']=='Sun' and s['target']=='H Ketu' and s['plane']=='Dec' and s['num']=='42')) == ['derived'], 'York: sky Sun -> horse Ketu Dec 42 derived (19 + 23)')
ok(tag_of(L2, [f'links:{i}:Dec' for i, l in enumerate(L1['links']) if l['a']=='H Ketu' and l['b']=='J Pallas' and 'Dec' in l['nums']]) == ['derived'], 'York: horse Ketu – Mason Pallas Dec 9 derived (23 − 14)')
L1, L2 = tagged('newmarket_july_1745_20240816', 'P01', None)
ok(tag_of(L2, find(L1, 'strikes', lambda s: s['sky']=='Pluto' and s['target']=='J Venus' and s['plane']=='Dec' and s['num']=='38')) == ['derived'], 'Newmarket July: sky Pluto -> Hornby Venus Dec 38 derived (21 + 17)')
L1, L2 = tagged('dettori_ascot_19960928', 'P01', None)
ok(tag_of(L2, find(L1, 'movement', lambda m: m['chart']=='J' and m['body']=='Sun' and m['plane']=='Dec' and m['num']=='21')) == ['root'], 'Dettori: sky Sun moved Dec 21 from Dettori Sun is a root')
# (2) chains on every race
nchk = nbad = 0; untagged = 0
for d in sorted(glob.glob('docs/classic/*/layer2')):
    race = d.split('/')[-2]
    sky = json.load(open(f'docs/classic/{race}/layer1/sky.json'))
    for f in sorted(glob.glob(f'{d}/P*.json')):
        L2 = json.load(open(f)); L1 = json.load(open(f.replace('layer2', 'layer1')))
        C = {f"{p['chart']} {p['body']}": (p['ra'], p['dec']) for p in L1['points']}; C['EQ'] = (0.0, 0.0)
        def ends(iid):
            sec, i, *r = iid.split(':')
            if sec == 'axis': return (f'{i} Rahu', f'{i} Ketu')
            if sec == 'sky': a, b = sky[int(i)]['pair'].split('–'); return (f'S {a}', f'S {b}')
            x = L1[sec][int(i)]
            if sec == 'points': return (f"{x['chart']} {x['body']}", 'EQ')
            if sec == 'links': return (x['a'], x['b'])
            if sec == 'movement': return (f"S {x['body']}", f"{x['chart']} {x['body']}")
            if sec == 'strikes': return (f"S {x['sky']}", x['target'])
        for iid, t in L2['tags'].items():
            if 'chain' not in t: continue
            nchk += 1; pl = t['plane']; a, b = ends(iid)
            # walk the chain from a to b using actual coordinates, summing signed differences of chain edges
            cur, tot = a, 0.0
            for c in t['chain']:
                x, y = ends(c['id']) if c['id'] != iid else (None, None)
                nxt = y if x == cur else x if y == cur else None
                if nxt is None: break
                d_ = (C[nxt][1] - C[cur][1]) if pl == 'Dec' else wrap(C[nxt][0] - C[cur][0])
                tot += d_; cur = nxt
            real = abs(C[b][1] - C[a][1]) if pl == 'Dec' else abs(wrap(C[b][0] - C[a][0]))
            got = abs(tot) if pl == 'Dec' else abs(wrap(tot))
            if cur != b or abs(got - real) > 1e-6: nbad += 1; print('  FAIL chain', race, os.path.basename(f), iid, cur, b, got, real)
ok(nbad == 0, f'all {nchk} derived/mirror chains re-add exactly from coordinates (bad {nbad})')
# (3) exactly one tag per Layer 1 item (all races)
bad3 = 0
for d in sorted(glob.glob('docs/classic/*/layer2')):
    race = d.split('/')[-2]; sky = json.load(open(f'docs/classic/{race}/layer1/sky.json'))
    scl = json.load(open(f'docs/classic/{race}/layer1/sky_close.json'))
    for f in sorted(glob.glob(f'{d}/P*.json')):
        L2 = json.load(open(f)); L1 = json.load(open(f.replace('layer2', 'layer1'))); T = L2['tags']
        need = set(['node'] + [f'sky:{i}' for i in range(len(sky))] + [f'sky_close:{i}' for i in range(len(scl))])
        need |= {f'points:{i}' for i, p in enumerate(L1['points']) if p['eq_num']}
        for i, l in enumerate(L1['links']):
            need |= {f'links:{i}:{pl}' for pl in l['nums']}
            if not l['nums'] or l['close'] or l.get('near'): need.add(f'links:{i}')
        for sec in ('strikes','ratios','movement','same_body','shared','eq_ratios','pair_sets','pair_family','splits','contacts','hj_ratios'):
            need |= {f'{sec}:{i}' for i in range(len(L1[sec]))}
        have = set(T)
        if need != have: bad3 += 1; print('  FAIL tags', race, os.path.basename(f), 'missing', list(need - have)[:5], 'extra', list(have - need)[:5])
ok(bad3 == 0, f'every Layer 1 item has exactly one tag on every runner (bad runners {bad3})')
print('FAILS', fails); sys.exit(1 if fails else 0)
