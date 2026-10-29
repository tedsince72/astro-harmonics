"""SKY-sourced events of the sky TIMELINE: every SKY block cell (S Jupiter -> S X, RA / Dec) whose best target, or nearest
target when no hit, is reached (linear, off -> +5 min) within off -30 / +60 min must be a TIMELINE event with source SKY,
and no other SKY event. usage: check_tl_sky.py <wb> [--half]"""
import sys
import openpyxl
sys.path.insert(0, __import__('os').path.dirname(__file__))
import ifam
from check_cells import Pos, pt

path = sys.argv[1]; half = '--half' in sys.argv
wb = openpyxl.load_workbook(path)
pos = Pos(wb)
ws = wb['SKY JUPITER']
exp, got = {}, {}
blk = None
for row in ws.iter_rows(max_col=20):
    a = row[0].value
    if isinstance(a, str) and a.startswith('TIMELINE (') :
        blk = 'TL'
    elif isinstance(a, str) and a.startswith(('LONG TIMELINE (', 'STAR TIMELINE (', 'LONG STAR')):
        blk = None
    if a == 'SKY' and isinstance(row[1].value, str) and row[1].value.startswith('S Jupiter → S '):
        x = row[1].value.split('→ S ', 1)[1]
        for plane in ('RA', 'Dec'):
            if x == 'equator' and plane == 'RA':
                continue
            v = pos.dist('SKY', ('S', 'Jupiter'), ('S', x), plane)
            v5 = pos.dist('SKY', ('S', 'Jupiter'), ('S', x), plane, 5)
            e = ifam.evaluate(v, plane, half)
            if e['fam'] == 'conj' or v5 == v:
                continue
            m = 5 * (e['t'] - v) / (v5 - v)
            if -30 <= m <= 60:
                exp[(row[1].value, plane)] = (e['fam'], round(m, 1), e['hit'])
    if blk == 'TL' and a == 'TIMELINE' and row[3].value == 'SKY':
        got[(row[4].value, row[5].value)] = (str(row[7].value), float(row[2].value))
print(path.split('/')[-1], 'expected SKY events', len(exp), 'on sheet', len(got))
bad = 0
for k in sorted(set(exp) | set(got)):
    if k not in exp or k not in got or abs(exp[k][1] - got[k][1]) > 0.11 or exp[k][0] not in got[k][0]:
        bad += 1
        print('   mismatch', k, exp.get(k), got.get(k))
print('  mismatches', bad)
