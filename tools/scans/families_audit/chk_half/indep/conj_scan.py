"""(g): conjunction-range cells (RA < 1.5, Dec < 0.3) whose best family is not the conjunction, before and after; plus Lingfield P11 T3
H Jupiter -> J Ketu RA by hand. usage: conj_scan.py <records_before.json> <records_after.json> [after workbook]"""
import sys, json, openpyxl
from fam import fams, CONJ
B = {tuple(r[:4]): r for r in json.load(open(sys.argv[1]))}
A = {tuple(r[:4]): r for r in json.load(open(sys.argv[2]))}
for k, a in A.items():
    v, pl = a[4], k[3]
    if pl in CONJ and v < CONJ[pl]:
        b = B[k]
        if (a[5] and a[5][0] != 'conj') or (b[5] and b[5][0] != 'conj'):
            cs = [f for f in fams(v, pl, True) if f[1] == 'conj'][0][0]
            print(k, v, 'before', b[5], 'after', a[5], f'conj score {cs:.2f}')
if len(sys.argv) > 3:
    wb = openpyxl.load_workbook(sys.argv[3])
    P = {(r[0], r[2], r[3]): r[5:7] for r in wb['POSITIONS'].iter_rows(min_row=5, values_only=True) if r[0]}
    ws = wb['P11']
    for row in ws.iter_rows():
        if row[0].value == 'T3' and row[1].value == 'H Jupiter → J Ketu':
            d = abs(P[('P11', 'H', 'Jupiter')][0] - P[('P11', 'J', 'Ketu')][0]) % 360; d = min(d, 360 - d)
            print('T3 P11 H Jupiter → J Ketu RA', round(d, 6), fams(d, 'RA', True), [c.value for c in row[2:8]])
