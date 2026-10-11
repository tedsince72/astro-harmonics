#!/usr/bin/env python3
"""three_same_body.py WORKBOOK [TOL_PCT]  (Eddie 11 Oct: 'ratios together of the 3 Jupiters in all planes', then every body)
For each body X: the three points sky X, horse natal X, jockey natal X. The three distances between them (sky-horse, horse-jockey, sky-jockey)
in RA, Dec, Flat, Sky, and the three |Dec| from the Equator. For each set of three values: the three ratios (larger/smaller) against p/q
(q <= 9); the set's score is the WORST of its three ratio errors. Listed when the worst is within TOL_PCT (default 0.15%), tightest first,
plus every body's best set."""
import sys, openpyxl, math, itertools
F = sys.argv[1]; TOL = float(sys.argv[2]) / 100 if len(sys.argv) > 2 else 0.0015
wb = openpyxl.load_workbook(F, data_only=True)
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
L = {t: {r[1]: (float(r[4]), float(r[8])) for r in list(wb[t].iter_rows(values_only=True))[1:] if r[1] in BOD} for t in ('TRANS', 'P01', 'P02')}
HN, JN = wb['P01'].cell(2, 1).value, wb['P02'].cell(2, 1).value
def ms(a, b):
    dra = (a[0] - b[0] + 180) % 360 - 180; dd = a[1] - b[1]; r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    hv = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin((r2 - r1) / 2) ** 2
    return {'RA': abs(dra), 'Dec': abs(dd), 'Flat': math.hypot(dra, dd), 'Sky': math.degrees(2 * math.asin(math.sqrt(hv)))}
def frac(x):
    best = (9, '')
    for q in range(1, 10):
        p = round(x * q)
        if p >= q:
            e = abs(x - p / q) / (p / q); g = math.gcd(p, q)
            if e < best[0]: best = (e, f'{p // g}/{q // g}' if q // g > 1 else f'{p // g}')
    return best
rows = []
for b in BOD:
    s, h, j = L['TRANS'][b], L['P01'][b], L['P02'][b]
    sh, hj, sj = ms(s, h), ms(h, j), ms(s, j)
    sets = {mm: (sh[mm], hj[mm], sj[mm]) for mm in ('RA', 'Dec', 'Flat', 'Sky')}
    sets['Equator'] = (abs(s[1]), abs(h[1]), abs(j[1]))
    for mm, v in sets.items():
        if min(v) < 0.5: continue
        rs = [frac(max(x, y) / min(x, y)) for x, y in itertools.combinations(v, 2)]
        rows.append((max(e for e, _ in rs), b, mm, v, rs))
lab = {'Equator': ('sky', 'horse', 'jockey')}
print(f"== {F.split('/')[-1]}: same body in sky / {HN} / {JN}; three values per plane; worst of the three ratios")
print(f"\nwithin {TOL*100:.2f}% (all three ratios):")
for w, b, mm, v, rs in sorted(rows):
    if w > TOL: break
    names = lab.get(mm, ('sky–horse', 'horse–jockey', 'sky–jockey'))
    print(f"   {w*100:.3f}%  {b:10s} {mm:7s} " + '  '.join(f"{n} {x:.4f}" for n, x in zip(names, v)) + '   ratios ' + ', '.join(f"{f} ({e*100:.3f}%)" for e, f in rs))
print("\nbest set for each body:")
best = {}
for r in sorted(rows):
    best.setdefault(r[1], r)
for b in BOD:
    if b in best:
        w, _, mm, v, rs = best[b]; print(f"   {b:10s} {mm:7s} worst {w*100:.3f}%   " + ', '.join(f for _, f in rs))
