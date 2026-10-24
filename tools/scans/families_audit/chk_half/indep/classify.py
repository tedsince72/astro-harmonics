"""before / after classification from the records of check_cells.py (old rules on the before workbook, new rules on the after one).
usage: classify.py <before.json> <after.json>"""
import sys, json, collections
B = {tuple(r[:4]): r for r in json.load(open(sys.argv[1]))}
A = {tuple(r[:4]): r for r in json.load(open(sys.argv[2]))}
assert B.keys() == A.keys(), (len(B), len(A))
DIG = {'golden', 'phi power', 'ninth', 'sqrt2', 'silver'}
FAMS = ['whole', 'half', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver', 'conj']
fb, fa, cls = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
ex = collections.defaultdict(list)
for k in B:
    t = k[0] if k[0].startswith('T24') or k[0] == 'SKY block' else k[0]
    b, a = B[k], A[k]
    assert abs(b[4] - a[4]) < 1e-9
    if b[5]: fb[t][b[5][0]] += 1
    if a[5]: fa[t][a[5][0]] += 1
    ob, oa = b[5], a[5]
    if ob and oa and ob[:2] == oa[:2]:
        if abs(ob[2] - oa[2]) > 1e-6: cls[t]['SCORE CHANGED (unexpected)'] += 1
        continue
    if not ob and not oa:
        if b[6] == a[6]: continue
        c = 'nearest target changed' + (' (to half)' if a[6][0] == 'half' else '')
    elif oa and oa[0] == 'half':
        c = 'new half hit' + (f' (was {ob[0]})' if ob else ' (was outside)')
    elif ob and not oa:
        c = 'lost digit-family hit' if ob[0] in DIG else f'lost {ob[0]} hit (unexpected)'
    elif ob and oa:
        c = f'best family changed ({ob[0]} -> {oa[0]})'
    else:
        c = f'new {oa[0]} hit (unexpected)'
    cls[t][c] += 1
    if len(ex[(t, c)]) < 2: ex[(t, c)].append((k[1], k[2], k[3], a[4], ob, oa, b[6], a[6]))
for t in sorted(fb.keys() | fa.keys() | cls.keys()):
    print(t)
    print('   hits before -> after: ' + ', '.join(f'{f} {fb[t][f]} -> {fa[t][f]}' for f in FAMS))
    for c, n in sorted(cls[t].items(), key=lambda z: -z[1]):
        print(f'   {c}: {n}   e.g. {ex[(t, c)][0]}')
