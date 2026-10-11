#!/usr/bin/env python3
"""race_to_workbooks.py RACE OFF OUTDIR - one workbook per runner pair, in the format of Eddie's race_batch xlsx
(TRANS = race sky at the real off, interpolated from the minute sky file; P01 = horse 12:00 chart; P02 = jockey 12:00 chart;
stars written as '<name>_B'; body in col B, ra col E, dec col I) so the workbook tools run the same way on every runner."""
import sys, os, csv, collections, openpyxl
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("N = sorted(S)")[0].split("S = {}")[0]); STARSET = set(STARS)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R, OFF, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT, exist_ok=True)
sched = int(R[-4:-2]) * 60 + int(R[-2:]); h, m, s = map(int, OFF.split(':')); t = h * 60 + m + s / 60
M = collections.defaultdict(dict)
for r in csv.DictReader(open(f'{REPO}/data/sky/{R}__SKYM.csv')): M[r['body']][sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
SKY = {}
for b, d in M.items():
    ks = sorted(d); ra = np.degrees(np.unwrap(np.radians([d[k][0] for k in ks])))
    SKY[b] = (float(np.interp(t, ks, ra) % 360), float(np.interp(t, ks, [d[k][1] for k in ks])))
meta = list(csv.reader(open(f'{REPO}/data/allpos/{R}__META.csv'))); hdr = next(i for i, r in enumerate(meta) if r[:3] == ['tab', 'role', 'cloth'])
TABS = [dict(zip(meta[hdr], r)) for r in meta[hdr + 1:] if r and r[0].startswith('P')]
def sheet(wb, title, label, P):
    ws = wb.create_sheet(title); ws.append(['name', 'body_A', 'body_B', 'measurement_type', 'ra_A', 'ra_B', 'ra_diff', 'ra_midpoint', 'dec_A'])
    for b, (ra, de) in P.items():
        nm = b + '_B' if b in STARSET else b
        ws.append([label, nm, nm, 'transit_self', ra, ra, 0, ra, de])
for tt in TABS:
    if tt['role'] != 'horse': continue
    jt = 'P%02d' % (int(tt['tab'][1:]) + 1); jn = next(x['name'] for x in TABS if x['tab'] == jt)
    pos = lambda tab: {q['body']: (float(q['ra']), float(q['dec'])) for q in csv.DictReader(open(f'{REPO}/data/allpos/{R}__{tab}_POS.csv')) if q['ra']}
    wb = openpyxl.Workbook(); wb.remove(wb.active)
    sheet(wb, 'TRANS', f'{R} off {OFF}', SKY); sheet(wb, 'P01', tt['name'], pos(tt['tab'])); sheet(wb, 'P02', jn, pos(jt))
    f = f"{OUT}/{R}__{tt['tab']}.xlsx"; wb.save(f); print(f, tt['name'], '/', jn)
