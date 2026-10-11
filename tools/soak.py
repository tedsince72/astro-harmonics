#!/usr/bin/env python3
"""soak.py WORKBOOK [W] [MIN]  (Eddie 11 Oct: 'Pholas Ketu was soaked in 11.11')
For each body X (sky X, horse natal X, jockey natal X treated as one 'X'), collect every RA and Dec distance from X to any other point in any
context (sky–sky, natal–natal in either chart, sky X → natal Y, sky Y → natal X). Find values shared by at least MIN (default 3) DIFFERENT partners
within ±W (default 0.02) of each other. Star partners count once whatever the chart (a sky star and a natal star are the same partner).
Shows the value, whether it is a whole number or ninth, and the partners. Sorted by number of partners, then spread."""
import sys, openpyxl, collections
F = sys.argv[1]; W = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02; MIN = int(sys.argv[3]) if len(sys.argv) > 3 else 3
wb = openpyxl.load_workbook(F, data_only=True)
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(t):
    P = {}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b = r[1]
        if b in BOD: P[b] = (float(r[4]), float(r[8]))
        elif isinstance(b, str) and b.endswith('_B'): P[b[:-2] + '*'] = (float(r[4]), float(r[8]))
    return P
C = {'sky': load('TRANS'), 'H': load('P01'), 'J': load('P02')}
st = lambda x: x.endswith('*'); rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
def lab(v):
    w = round(v); q = round(v * 9)
    return f"{w} ({abs(v-w):.4f})" if abs(v - w) <= abs(v - q / 9) else f"{q}/9 ({abs(v-q/9):.4f})"
ctx = [('sky','sky'), ('H','H'), ('J','J'), ('sky','H'), ('H','sky'), ('sky','J'), ('J','sky')]
out = []
for X in BOD:
    vals = []
    for c1, c2 in ctx:
        A, B = C[c1], C[c2]
        for Y in B:
            if Y == X or (st(Y) and False) or {X, Y} == {'Rahu', 'Ketu'}: continue
            pid = Y if st(Y) else f"{'sky' if c2=='sky' else c2} {Y}"
            for mm, v in (('RA', rd(A[X], B[Y])), ('Dec', dd(A[X], B[Y]))):
                if v >= 0.5: vals.append((v, pid, f"{c1} {X} → {c2} {Y} {mm}"))
    vals.sort()
    best = []
    for i in range(len(vals)):
        j = i; grp = []
        while j < len(vals) and vals[j][0] - vals[i][0] <= 2 * W: grp.append(vals[j]); j += 1
        parts = {}
        for g in grp: parts.setdefault(g[1], g)
        if len(parts) >= MIN: best.append((len(parts), -(grp[-1][0] - grp[0][0]), X, list(parts.values())))
    seen = set()
    for n, sp, X_, g in sorted(best, reverse=True):
        key = round(sum(x[0] for x in g) / len(g), 1)
        if key in seen: continue
        seen.add(key); out.append((n, -sp, X_, g))
print(f"== {F.split('/')[-1]}: values one body takes from {MIN}+ different partners (±{W})")
for n, sp, X, g in sorted(out, key=lambda x: (-x[0], x[1]))[:25]:
    m = sum(x[0] for x in g) / len(g)
    print(f"\n   {X}: {n} partners at ~{m:.4f} ≈ {lab(m)}, spread {sp:.4f}")
    for v, pid, lbl in g: print(f"      {v:.4f}  {lbl}")
