#!/usr/bin/env python3
"""body_ratio_tt_nn.py WORKBOOK BODY [TOL_PCT]  (Eddie 11 Oct: 'ratios Jupiter to a body in transit and same body in natal')
For every other point X: TT = distance BODY–X in the race sky, NN = distance BODY–X in the natal chart (horse P01, jockey P02),
in RA (|dRA| wrapped), Dec, Flat (sqrt(dRA^2+dDec^2)) and Sky (great circle). Ratio = larger/smaller, compared with p/q (q <= 9);
kept within TOL_PCT (default 0.05%). Distances under 0.5 deg skipped. Sorted by closeness."""
import sys, openpyxl, math
F, BODY = sys.argv[1], sys.argv[2]; TOL = float(sys.argv[3]) / 100 if len(sys.argv) > 3 else 0.0005
wb = openpyxl.load_workbook(F, data_only=True)
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(t):
    P = {}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b = r[1]
        if b in BOD: P[b] = (float(r[4]), float(r[8]))
        elif isinstance(b, str) and b.endswith('_B'): P[b[:-2] + '*'] = (float(r[4]), float(r[8]))
    return P
S, H, J = load('TRANS'), load('P01'), load('P02'); HN, JN = wb['P01'].cell(2, 1).value, wb['P02'].cell(2, 1).value
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
print(f"== {F.split('/')[-1]}: {BODY}–X in the race sky (TT) against {BODY}–X in the natal chart (NN), ratio = p/q (q<=9) within {TOL*100:.3f}%")
for nm, N in ((HN, N0) for N0 in [H]) if False else ((HN, H), (JN, J)):
    out = []
    for X in S:
        if X == BODY or X not in N or {X, BODY} == {'Rahu', 'Ketu'}: continue
        tt, nn = ms(S[BODY], S[X]), ms(N[BODY], N[X])
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            a, b = tt[mm], nn[mm]
            if min(a, b) < 0.5: continue
            r = max(a, b) / min(a, b); e, f = frac(r)
            if e <= TOL: out.append((e, mm, X, a, b, f, 'TT>NN' if a >= b else 'NN>TT'))
    print(f"\n-- {nm}: {len(out)}")
    for e, mm, X, a, b, f, w in sorted(out): print(f"   {e*100:.4f}%  {mm:4s} {BODY}–{X:13s} TT {a:9.4f}  NN {b:9.4f}  ratio {f:6s} ({w})")
