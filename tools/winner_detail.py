#!/usr/bin/env python3
"""winner_detail.py WORKBOOK [FOCUS]  - the winner-first read used on Catterick (11 Oct 2026), for one race_batch workbook (TRANS / P01 horse / P02 jockey).
A close pairs inside each chart and the sky (RA < 1.5 = conjunction, Dec < 0.6 = same Dec; bodies, and body-star conjunctions)
B horse body near jockey body (RA < 2 or Dec < 0.15)   C nodes: what sits on Rahu/Ketu in each chart and the sky
D movement since birth (sky - natal, same body), horse and jockey, with whole/ninth flags (±0.01)
E every RA/Dec distance (sky, natal, sky->natal, movements, Dec from Equator) involving FOCUS (default Neptune) that is whole (±0.005) or a ninth (±0.0005)"""
import sys, openpyxl, itertools
F = sys.argv[1]; FOC = sys.argv[2] if len(sys.argv) > 2 else 'Neptune'
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
st = lambda x: x.endswith('*'); rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
def lab(v):
    w = round(v); q = round(v * 9)
    return (f"{w}", abs(v - w)) if abs(v - w) <= abs(v - q / 9) else (f"{q}/9", abs(v - q / 9))
def on(v): l, e = lab(v); return l if ((('/' not in l) and e <= 0.005) or ('/' in l and e <= 0.0005)) and v >= 0.1 else None
print(f"== {F.split('/')[-1]}: horse {HN}, jockey {JN}")
print("\nA. close pairs (conjunction RA<1.5 / same Dec <0.6 between bodies)")
for nm, P in (('sky', S), (HN, H), (JN, J)):
    for a, b in itertools.combinations(P, 2):
        if (st(a) and st(b)) or {a, b} == {'Rahu', 'Ketu'}: continue
        r, d = rd(P[a], P[b]), dd(P[a], P[b])
        if r < 1.5 or (d < 0.6 and not st(a) and not st(b)): print(f"   {nm:18s} {a}–{b}: RA {r:.4f} Dec {d:.4f} {'conj' if r < 1.5 else 'same Dec'}")
print(f"\nB. {HN} body near {JN} body")
for a in BOD:
    for b in BOD:
        r, d = rd(H[a], J[b]), dd(H[a], J[b])
        if r < 2 or d < 0.15: print(f"   horse {a:10s} – jockey {b:10s} RA {r:.4f} Dec {d:.4f}")
print("\nC. on the nodes (RA < 3 or Dec < 0.3)")
for nm, P in (('sky', S), (HN, H), (JN, J)):
    for n in ('Rahu', 'Ketu'):
        for b in P:
            if b in ('Rahu', 'Ketu'): continue
            r, d = rd(P[n], P[b]), dd(P[n], P[b])
            if r < 3 or (d < 0.3 and not st(b)): print(f"   {nm:18s} {n}–{b}: RA {r:.4f} Dec {d:.4f}")
print("\nD. movement since birth (sky − natal)")
for nm, P in (('horse', H), ('jockey', J)):
    for b in BOD:
        mr = (S[b][0] - P[b][0] + 180) % 360 - 180; md = S[b][1] - P[b][1]
        l1, e1 = lab(abs(mr)); l2, e2 = lab(abs(md))
        print(f"   {nm:6s} {b:10s} RA {mr:+10.4f} Dec {md:+9.4f}" + (f"  RA≈{l1}" if e1 <= 0.01 else '') + (f"  Dec≈{l2}" if e2 <= 0.01 else ''))
print(f"\nE. {FOC}: whole (±0.005) / ninth (±0.0005) RA or Dec distances")
rows = []
for nm, P in (('sky', S), (HN, H), (JN, J)):
    v = abs(P[FOC][1]); l = on(v)
    if l: rows.append((nm, f'{FOC} Dec from Equator', v, l))
    for b in P:
        if b == FOC: continue
        for mm, v in (('RA', rd(P[FOC], P[b])), ('Dec', dd(P[FOC], P[b]))):
            l = on(v)
            if l: rows.append((nm, f'{FOC}–{b} {mm}', v, l))
for nm, N in ((HN, H), (JN, J)):
    for b in S:
        for x, y, tag in ((S[FOC], N[b], f'sky {FOC} → {nm} {b}'), (S[b], N[FOC], f'sky {b} → {nm} {FOC}')):
            if b == FOC and tag.startswith(f'sky {b} →'): continue
            for mm, v in (('RA', rd(x, y)), ('Dec', dd(x, y))):
                l = on(v)
                if l: rows.append(('sky→natal', f'{tag} {mm}', v, l))
for nm, w, v, l in rows: print(f"   {nm:18s} {w:40s} {v:9.4f} = {l}")
