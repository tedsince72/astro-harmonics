#!/usr/bin/env python3
"""field_summary.py OUTDIR WORKBOOKDIR  - one line per runner pair from the outputs of workbook_numbers / three_way_wb / three_same_body /
winner_detail (Neptune), plus Venus–Neptune and Jupiter–Neptune in each natal chart. Star echoes (sky star -> natal body, sky body -> natal star)
are counted apart from body-only 'together' pairs."""
import sys, os, re, glob, openpyxl
O, D = sys.argv[1], sys.argv[2]
def nat(f, t):
    wb = openpyxl.load_workbook(f, data_only=True); return {r[1]: (float(r[4]), float(r[8])) for r in list(wb[t].iter_rows(values_only=True))[1:] if isinstance(r[4], (int, float))}
rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
def lab(v):
    w = round(v); q = round(v * 9); return (f"{w}", abs(v - w)) if abs(v - w) <= abs(v - q / 9) else (f"{q}/9", abs(v - q / 9))
print(f"{'pair':36s} {'together NN':>11s} {'together TN body/echo':>21s} {'3-way':>6s} {'same-body sets <=0.15%':28s} {'Nep#':>4s} {'nodes on body':>13s}  Venus–Neptune / Jupiter–Neptune (horse | jockey)")
for f in sorted(glob.glob(f'{D}/*.xlsx')):
    tab = f.split('__')[-1][:-5]
    num = open(f'{O}/{tab}_numbers.txt').read(); tw = open(f'{O}/{tab}_three_way.txt').read(); sb = open(f'{O}/{tab}_same_body.txt').read(); dt = open(f'{O}/{tab}_detail.txt').read()
    wb = openpyxl.load_workbook(f); hn, jn = wb['P01'].cell(2, 1).value, wb['P02'].cell(2, 1).value
    secs = re.split(r'\n-- ', num); nn = tnb = tne = 0
    for s in secs:
        head = s.split('\n')[0]
        if 'together' not in head: continue
        lines = []
        for l in s.split('\n')[1:]:
            if not l.strip(): break
            if '–' in l: lines.append(l)
        if head.startswith('NN'): nn += len(lines)
        elif head.startswith('TN'):
            for l in lines:
                if '*' in l: tne += 1
                else: tnb += 1
    links = tw.count('LINK'); sets = [l.split()[1] + '/' + l.split()[2] for l in sb.split('ratios):')[1].split('best set')[0].split('\n') if re.match(r'\s+[\d.]+%', l)]
    E = dt.split('\nE.')[1].strip().split('\n')[1:]
    C = [l for l in dt.split('\nC.')[1].split('\nD.')[0].split('\n') if ' RA ' in l and not l.strip().startswith('sky')]
    nodes = sum(1 for l in C if '*' not in l.split(':')[0] and (float(re.search(r'RA ([\d.]+)', l).group(1)) < 1.5 or float(re.search(r'Dec ([\d.]+)', l).group(1)) < 0.1))
    VN = []
    for t in ('P01', 'P02'):
        P = nat(f, t); x = []
        for a in ('Venus', 'Jupiter'):
            r, d = rd(P[a], P['Neptune']), dd(P[a], P['Neptune']); lr, er = lab(r); ld, ed = lab(d)
            x.append(f"{a[0]} RA {r:.2f}{'≈'+lr if er<=0.01 else ''} Dec {d:.2f}{'≈'+ld if ed<=0.01 else ''}")
        VN.append('; '.join(x))
    print(f"{(hn+' / '+jn)[:36]:36s} {nn:>11d} {tnb:>12d}/{tne:<8d} {links:>6d} {', '.join(sets)[:28]:28s} {len(E):>4d} {nodes:>13d}  {VN[0]} | {VN[1]}")
