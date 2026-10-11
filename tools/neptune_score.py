#!/usr/bin/env python3
"""neptune_score.py WORKBOOK_DIR  (Eddie 11 Oct 2026: 'score Neptune directly' — rules fixed before running across the races; Redcar was used to set them)
For each runner pair (horse H, jockey J, race sky S), what reaches or holds the horse's Neptune and the jockey's Neptune:
 EQ    natal Neptune's |Dec| (distance from the Equator) on a whole number (±0.005) or a ninth (±0.0005)          [per chart, 0–2]
 OWN   a body in the same natal chart close to Neptune: RA < 1.5 (with Dec < 1.0) or same Dec (< 0.3)                [count]
 PART  a body of the PARTNER's natal chart close to Neptune: RA < 1.5 (with Dec < 1.0) or same Dec (< 0.1)          [count]
 SKY1  a sky body (not a star) -> natal Neptune, RA or Dec, whole ±0.002 or ninth ±0.0005 (one coordinate)          [count]
 SKY2  a sky body -> natal Neptune with RA AND Dec both whole (±0.005) / ninth (±0.0005)                            [count]
 NEP→  sky Neptune -> a natal body with RA AND Dec both on whole/ninth (as SKY2, other direction)                   [count]
SCORE = EQ + OWN + PART + SKY1 + 3*SKY2 + 3*NEP→ . Nodes Rahu/Ketu count as bodies; stars are left out of OWN/PART/SKY."""
import sys, glob, openpyxl
D = sys.argv[1]
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(wb, t):
    return {r[1]: (float(r[4]), float(r[8])) for r in list(wb[t].iter_rows(values_only=True))[1:] if r[1] in BOD + ['Neptune'] and isinstance(r[4], (int, float))}
rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
def on(v, tw=0.005):
    w = round(v); q = round(v * 9)
    return (abs(v - w) <= tw and w > 0) or (abs(v - q / 9) <= 0.0005 and q % 9)
rows = []
for f in sorted(glob.glob(f'{D}/*.xlsx')):
    wb = openpyxl.load_workbook(f, data_only=True); S, H, J = load(wb, 'TRANS'), load(wb, 'P01'), load(wb, 'P02')
    nm = f"{wb['P01'].cell(2,1).value} / {wb['P02'].cell(2,1).value}"; det = []
    eq = own = part = s1 = s2 = n2 = 0
    for cn, N, P in (('H', H, J), ('J', J, H)):
        if on(abs(N['Neptune'][1])): eq += 1; det.append(f"{cn} Neptune |Dec| {abs(N['Neptune'][1]):.4f}")
        for b in BOD:
            r, d = rd(N[b], N['Neptune']), dd(N[b], N['Neptune'])
            if (r < 1.5 and d < 1.0) or d < 0.3: own += 1; det.append(f"{cn} own {b}–Neptune RA {r:.2f} Dec {d:.3f}")
            r, d = rd(P[b], N['Neptune']), dd(P[b], N['Neptune'])
            if (r < 1.5 and d < 1.0) or d < 0.1: part += 1; det.append(f"partner {b} → {cn} Neptune RA {r:.2f} Dec {d:.3f}")
            r, d = rd(S[b], N['Neptune']), dd(S[b], N['Neptune'])
            if on(r) and on(d): s2 += 1; det.append(f"sky {b} → {cn} Neptune RA {r:.4f} Dec {d:.4f} TOGETHER")
            else:
                for mm, v in (('RA', r), ('Dec', d)):
                    if on(v, 0.002): s1 += 1; det.append(f"sky {b} → {cn} Neptune {mm} {v:.4f}")
            r, d = rd(S['Neptune'], N[b]), dd(S['Neptune'], N[b])
            if on(r) and on(d): n2 += 1; det.append(f"sky Neptune → {cn} {b} RA {r:.4f} Dec {d:.4f} TOGETHER")
    sc = eq + own + part + s1 + 3 * s2 + 3 * n2
    rows.append((sc, nm, eq, own, part, s1, s2, n2, det, f.split('__')[-1][:-5]))
print(f"== {D}\n{'pair':38s} {'EQ':>3s} {'OWN':>4s} {'PART':>5s} {'SKY1':>5s} {'SKY2':>5s} {'NEP→':>5s} {'SCORE':>6s}")
for sc, nm, eq, own, part, s1, s2, n2, det, tab in sorted(rows, key=lambda r: -r[0]):
    print(f"{nm[:38]:38s} {eq:>3d} {own:>4d} {part:>5d} {s1:>5d} {s2:>5d} {n2:>5d} {sc:>6d}   [{tab}]")
if '-v' in sys.argv:
    for r in sorted(rows, key=lambda r: -r[0]): print(f"\n-- {r[1]}\n   " + '\n   '.join(r[8]))
