#!/usr/bin/env python3
"""Checks for tools/eddie_read.py (stage 1 collector), 6 Nov 2026.

1. Every cell Eddie read by hand in a race appears in the report under the right runner (Haydock 19 Feb 2022 Wholestone,
   Leicester 17 Feb 2022 Nelson River, Newcastle 11 Mar 2022 Peak Time).
2. Every piece's value = the distance recomputed from POSITIONS (own code), its best family = families.best.
3. Every 'only' / 'also' flag = the holders recomputed over the field.
Run from the repo root: python3 tests/eddie_read_check.py
"""
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, 'tools'), os.path.join(ROOT, 'rebuild_kit')]
import openpyxl  # noqa: E402
import eddie_read as E  # noqa: E402
import families as F  # noqa: E402

REF = os.path.join(ROOT, 'reference', 'classic')
CASES = {
    'race_batch_20220219_haydock_1405_jupiter_tables.xlsx': ('5 Wholestone', [
        'S Sun → H Sun RA 45.0052 45 (54.84) [360/8]',
        'S Sun → H Neptune RA 0.4062 conj (53.18)',
        'H Jupiter → H star Vindemiatrix RA 179.4714 10×φ^6 (93.71)',
        'J Wezen → J Neptune RA 179.4430 10×φ^6 (99.94)',
        'H RA midpoints: Sun = Eris 97.36 (far, far side)',
        'S Moon → J Jupiter Dec 0.1147 conj (38.14)',
        'S Chiron → H Jupiter Dec 0.0486 conj (70.20)',
        'S Moon → J Venus RA 45.9949 46 (55.35)',
        'S Sun → J Neptune RA 44.9979 45 (79.69) [360/8]',
    ]),
    'race_batch_20220217_leicester_1445_jupiter_tables.xlsx': ('3 Nelson River', [
        'H Alkes → H Mercury Dec 0.0094 conj (93.85)',
        'H Alkes → H Chiron RA 179.4180 10×φ^6 (94.57)',
        'H Alkes → H Ketu RA 155.5255 155.556 (97.15)',
        'J Alkes → J Juno RA 35.0063 35 (47.24)',
        'S Juno → H Juno RA 177.7114 177.778 (94.81)',
        'S Gonggong → H Gonggong Dec 1.7775 1.77778 (98.15)',
        'S Juno → J Juno Dec 14.5657 9×φ (80.15)',
        'H Sadalmelik → H Haumea Dec 17.7709 17.7778 (94.63)',
        'J Sadalmelik → J Gonggong RA 0.2481 conj (69.65)',
        'J Sadalmelik → J Sun RA 105.0153 105 (5.52)',
        'J Sadalmelik → J Mars RA 67.9857 68 (8.07)',
        'J Sadalmelik → J Mars Dec 15.0080 15 (35.74)',
        'J Sadalmelik → J Pluto Dec 4.9976 5 (77.58)',
    ]),
    'race_batch_20220311_newcastle_1540_jupiter_tables.xlsx': ('3 Peak Time', [
        'J Zubeneschamali → J Eris Dec 0.0002 conj (99.84)',
        'H Jupiter → H Rahu RA 0.4014 conj (53.64)',
    ]),
}
SKY_LINES = {
    'race_batch_20220217_leicester_1445_jupiter_tables.xlsx': ['S Sun conj Sadalmelik RA 0.6895 (29.20)'],
    'race_batch_20220219_haydock_1405_jupiter_tables.xlsx': ['Regulus RA 179.443306 10×φ^6', 'Diadem (Jupiter + Moon)'],
}

ok = bad = 0


def check(cond, msg):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', msg)


def section(md, runner):
    i = md.index(f'## {runner}')
    j = md.find('\n## ', i + 3)
    return md[i: j if j > 0 else None]


def positions(path):
    P = {}
    for r in openpyxl.load_workbook(path, read_only=True)['POSITIONS'].iter_rows(values_only=True):
        if r and len(r) > 6 and isinstance(r[5], (int, float)) and r[2] in 'SHJ':
            P[(r[0], r[2], r[3])] = (r[5], r[6])
    return P


def own_dist(a, b, pl):
    if pl == 'RA':
        x = abs(a[0] - b[0]) % 360
        return min(x, 360 - x)
    return abs(a[1] - b[1])


for wbname, (runner, cells) in CASES.items():
    path = os.path.join(REF, wbname)
    D = E.read(path)
    md = E.report(D)
    sec = section(md, runner)
    for c in cells:
        check(c in sec, f'{wbname} {runner}: missing "{c}"')
    for s in SKY_LINES.get(wbname, []):
        check(s in md[:md.index('## Flags')], f'{wbname} sky: missing "{s}"')

    # values and families from POSITIONS
    P = positions(path)
    for p in D['pieces']:
        ch = p['chart']
        if p['layer'] == 'same body':
            a, b = P[('SKY', 'S', p['body'])], P[(p['runner'], ch, p['body'])]
        elif p['layer'] in ('T1', 'T2'):
            x = p['body'].replace('star ', '')
            a, b = P[(p['runner'], ch, 'Jupiter')], P[(p['runner'], ch, x)]
        elif p['layer'] == 'top rows':
            a, b = P[('SKY', 'S', p['source'][2:])], P[(p['runner'], ch, p['body'])]
        else:
            a, b = P[(p['runner'], ch, p['source'][2:])], P[(p['runner'], ch, p['body'])]
        v = own_dist(a, b, p['plane'])
        check(abs(v - p['value']) < 1e-6, f"{wbname} value {p}")
        if p['layer'] != 'same body':
            e = F.best(v, p['plane'])
            check(e and e['target'] == p['target'] and abs(e['score'] - p['score']) < 0.006, f"{wbname} family {p}")

    # field flags
    def key(p):
        src = p['source'][2:] if p['source'][:2] in ('H ', 'J ') else p['source']
        return (p['layer'] if p['layer'] not in ('T1', 'T2') else 'T1/T2', src, p['body'], p['plane'], p['family'], p['target'])
    hold = defaultdict(set)
    for p in D['pieces']:
        hold[key(p)].add(p['runner'])
    for p in D['pieces']:
        n = len(hold[key(p)]) - 1
        check((p['field'] == 'only') == (n == 0) and (n == 0 or p['field'].count(',') == n - 1), f"{wbname} flag {p}")

# every race runs
for f in sorted(os.listdir(REF)):
    if f.startswith('race_batch_2022') and f.endswith('_jupiter_tables.xlsx'):
        try:
            E.report(E.read(os.path.join(REF, f)))
            check(True, '')
        except Exception as ex:  # noqa: BLE001
            check(False, f'{f}: {ex!r}')

print(f'{ok}/{ok + bad} checks passed')
sys.exit(1 if bad else 0)
