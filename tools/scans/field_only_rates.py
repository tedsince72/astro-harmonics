#!/usr/bin/env python3
"""field_only_rates.py  — number of strict field-only items (checklist reader, frozen CR v1.1) per runner against finishing position.
Table for the blind races, then the win rate by count (0 / 1 / 2 / 3+), with the chance expectation (sum of 1/field size) beside it;
then the same for the read races (NOT evidence: the checklist and the reader were built from them). Uses results: only for races whose
result has been opened."""
import sys, os, glob, csv, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import checklist_reader as CR

BLIND = [('exeter_1515_20211019', 'blind for the layers only (reader built after its result)'),
         ('redcar_1515_20211015', 'blind for the layers only (reader built after its result)'),
         ('haydock_1420_20210904', 'blind for the layers only (reader built after its result)'),
         ('kempton_aw_1440_20210904', 'blind for the reader'), ('fontwell_1645_20210914', 'blind for the reader')]
READ = ['ascot_1350_20231021', 'carlisle_1630_20220707', 'catterick_1505_20211119', 'chelmsford_aw_1320_20240118', 'ffos_las_1420_20220105',
        'fontwell_1530_20231006', 'haydock_1405_20220219', 'haydock_1718_20220507', 'huntingdon_1352_20211205', 'lingfield_1500_20220123',
        'newbury_1350_20211126', 'newcastle_1540_20220311', 'newcastle_aw_1220_20211112', 'newcastle_aw_1330_20220102', 'newcastle_aw_1540_20211112',
        'newcastle_aw_1640_20220215', 'newmarket_1535_20220414', 'newton_abbot_1525_20220717', 'nottingham_1530_20220601', 'nottingham_1750_20220613',
        'perth_1610_20220420', 'sandown_1425_20211204', 'sandown_1430_20240215', 'sedgefield_1500_20220510', 'wincanton_1420_20220321',
        'wolverhampton_aw_1725_20231021', 'york_1545_20240515', 'york_1615_20240515', 'newmarket_july_1745_20240816', 'exeter_1515_20211019',
        'redcar_1515_20211015', 'haydock_1420_20210904']

# Redcar has no race csv: finishing order from docs/classic/redcar_1515_20211015/blind_test.md
FALLBACK = {'redcar_1515_20211015': {'5 Present Moment': ('1', '14/1'), '4 Oheka': ('2', '15/8'), '3 Divine Jewel': ('3', '10/11'),
                                     '8 World Without Love': ('4', '12/1'), '6 Sea Time': ('5', '33/1')}}

def finish(race):
    if race in FALLBACK: return FALLBACK[race]
    m = re.match(r'(.+)_(\d{4})_(\d{8})$', race)
    rows = list(csv.DictReader(open(glob.glob(f'reference/classic/race_batch_{m.group(3)}_{m.group(1)}_{m.group(2)}.csv')[0])))
    return {r['name']: (r['finish_pos'], r['sp']) for r in rows if r['subject_type'] == 'horse'}

def rows(race):
    F = CR.run(race); pos = finish(race); out = []
    for P, n in F['runners'].items():
        fo = [it for it in F['items'] if F['field'][str(it)].get('strict', {}).get('k') == 1 and P in F['field'][str(it)]['strict']['runners']]
        p, sp = pos.get(n.split(' / ')[0], ('?', '?'))
        out.append((P, n, fo, p, sp, F['n']))
    return out

def rates(races, label):
    g = {}
    for r in races:
        for P, n, fo, p, sp, nf in rows(r):
            k = min(len(fo), 3); d = g.setdefault(k, [0, 0, 0.0]); d[0] += 1; d[1] += p == '1'; d[2] += 1 / nf
    print(f"-- {label}: win rate by number of strict field-only items")
    print(f"   {'items':>6s} {'runners':>8s} {'won':>4s} {'win %':>6s} {'chance wins':>12s}")
    for k in sorted(g):
        d = g[k]
        print(f"   {('3+' if k == 3 else str(k)):>6s} {d[0]:8d} {d[1]:4d} {100 * d[1] / d[0]:5.0f}% {d[2]:12.2f}")

if __name__ == '__main__':
    print('== Field-only items (strict, checklist reader CR v1.1) against finish')
    for r, note in BLIND:
        print(f"-- {r} ({note})")
        for P, n, fo, p, sp, nf in rows(r):
            print(f"   {P} {n:44s} field-only {len(fo)} ({','.join(map(str, fo)) or '-'})  finish {p:>3s}  SP {sp}")
    rates([r for r, _ in BLIND], 'the 5 blind races (only Kempton and Fontwell blind for the reader)')
    rates([r for r, note in BLIND if note == 'blind for the reader'], 'Kempton + Fontwell only (blind for the reader)')
    rates(READ, f'the {len(READ)} read races — NOT evidence (the checklist and the reader were built from them)')
