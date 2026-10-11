#!/usr/bin/env python3
"""three_way_wb.py WORKBOOK [TOL_PCT]  - the Pholas test (Ketu–Deneb Algedi RA 10 : 36 : 66.67) on a race_batch workbook.
One pair (A,B), RA or Dec: H = horse natal, J = jockey natal, S = race sky. Link = J:H and S:H both p/q (q <= 9), ratios <= 12,
within TOL_PCT (default 0.02%); also lists 0.02–0.05% as 'near'. Star–star and Rahu–Ketu pairs out; no Moon; distances >= 0.5."""
import sys, openpyxl, math, itertools
F = sys.argv[1]; TOL = float(sys.argv[2]) / 100 if len(sys.argv) > 2 else 0.0002
wb = openpyxl.load_workbook(F, data_only=True)
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(t):
    P = {}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b = r[1]
        if b in BOD: P[b] = (float(r[4]), float(r[8]))
        elif isinstance(b, str) and b.endswith('_B'): P[b[:-2] + '*'] = (float(r[4]), float(r[8]))
    return P
S, H, J = load('TRANS'), load('P01'), load('P02')
d = lambda A, B, mm: abs((A[0] - B[0] + 180) % 360 - 180) if mm == 'RA' else abs(A[1] - B[1])
def frac(x):
    best = (9, '')
    for q in range(1, 10):
        p = round(x * q)
        if p >= q:
            e = abs(x - p / q) / (p / q); g = math.gcd(p, q)
            if e < best[0]: best = (e, f'{p // g}/{q // g}' if q // g > 1 else f'{p // g}')
    return best
out = []
for a, b in itertools.combinations(sorted(H), 2):
    if (a.endswith('*') and b.endswith('*')) or {a, b} == {'Rahu', 'Ketu'}: continue
    for mm in ('RA', 'Dec'):
        h, j, s = d(H[a], H[b], mm), d(J[a], J[b], mm), d(S[a], S[b], mm)
        if min(h, j, s) < 0.5: continue
        rj, rs = max(h, j) / min(h, j), max(s, h) / min(s, h)
        if rj > 12 or rs > 12: continue
        ej, fj = frac(rj); es, fs = frac(rs); rsj = max(s, j) / min(s, j); e3, f3 = frac(rsj)
        if max(ej, es) <= 0.0005: out.append((max(ej, es), mm, a, b, h, j, s, fj, ej, fs, es, f3, e3))
print(f"== {F.split('/')[-1]}: horse : jockey : sky on one pair (J:H and S:H simple, q<=9)")
for w, mm, a, b, h, j, s, fj, ej, fs, es, f3, e3 in sorted(out):
    tag = 'LINK' if w <= TOL else 'near'
    print(f"   {tag} {mm:3s} {a}–{b:13s} H {h:9.4f}  J {j:9.4f}  S {s:9.4f}   J:H {fj} ({ej*100:.4f}%)  S:H {fs} ({es*100:.4f}%)  S:J {f3} ({e3*100:.3f}%)")
