#!/usr/bin/env python3
"""scoreboard.py WORKBOOK_DIR OUTDIR  - one row per runner pair with the measures that have picked winners so far (11 Oct 2026):
TN = sky BODY -> natal BODY pairs on RA and Dec together (whole ±0.005 / ninth ±0.0005); NN = natal pairs on RA and Dec together (no star–star);
SKYV = sky-own values taken up by 4+ partners (from OUTDIR/<tab>_soak.txt clusters that contain a sky–sky term, value >= 1); SOAK5 = clusters of 5+;
NODES = node within RA 1.5 or Dec 0.1 of a body (own chart) + horse body on jockey node (RA 0.5 / Dec 0.1);
VEN-NODE = Venus to nearest node (RA, both charts, smallest); VEN-NEP = natal Venus–Neptune Dec (smallest of the two charts)."""
import sys, glob, re, itertools, openpyxl, subprocess
DIR, O = sys.argv[1], sys.argv[2]
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu','Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
def load(wb, t):
    P = {}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b = r[1]
        if b in BOD and isinstance(r[4], (int, float)): P[b] = (float(r[4]), float(r[8]))
        elif isinstance(b, str) and b.endswith('_B'): P[b[:-2] + '*'] = (float(r[4]), float(r[8]))
    return P
st = lambda x: x.endswith('*'); rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
def on(v):
    w = round(v); q = round(v * 9)
    return (abs(v - w) <= 0.005 and w > 0) or (abs(v - q / 9) <= 0.0005 and q % 9)
print(f"{'pair':38s} {'TN':>3s} {'NN':>3s} {'SKYV':>5s} {'SOAK5':>6s} {'NODES':>6s} {'VEN-NODE':>9s} {'VEN-NEP':>8s}")
for f in sorted(glob.glob(f'{DIR}/*.xlsx')):
    wb = openpyxl.load_workbook(f, data_only=True); S, H, J = load(wb, 'TRANS'), load(wb, 'P01'), load(wb, 'P02')
    nm = f"{wb['P01'].cell(2,1).value} / {wb['P02'].cell(2,1).value}"; tab = f.split('__')[-1][:-5]
    tn = sum(1 for N in (H, J) for a in S for b in N if not st(a) and not st(b) and a != b and {a, b} != {'Rahu', 'Ketu'} and on(rd(S[a], N[b])) and on(dd(S[a], N[b])))
    nn = sum(1 for N in (H, J) for a, b in itertools.combinations(N, 2) if not (st(a) and st(b)) and {a, b} != {'Rahu', 'Ketu'} and on(rd(N[a], N[b])) and on(dd(N[a], N[b])))
    txt = subprocess.run(['python3.12', 'tools/soak.py', f, '0.02', '4', '999'], capture_output=True, text=True).stdout.split('\n\n')
    skyv = soak5 = 0
    for blk in txt:
        L = blk.strip().split('\n')
        if not L or 'partners at' not in L[0]: continue
        m = re.search(r'(\d+) partners at ~([\d.]+)', L[0]); k, v = int(m.group(1)), float(m.group(2))
        if v < 1: continue
        if k >= 5: soak5 += 1
        if any(re.search(r'sky \S+ → sky ', l) for l in L[1:]): skyv += 1
    nodes = 0
    for N in (H, J):
        for n in ('Rahu', 'Ketu'):
            for b in N:
                if b in ('Rahu', 'Ketu') or st(b): continue
                if rd(N[n], N[b]) < 1.5 or dd(N[n], N[b]) < 0.1: nodes += 1
    for a in BOD:
        for n in ('Rahu', 'Ketu'):
            if a not in ('Rahu', 'Ketu') and (rd(H[a], J[n]) < 0.5 or dd(H[a], J[n]) < 0.1): nodes += 1
            if a not in ('Rahu', 'Ketu') and (rd(J[a], H[n]) < 0.5 or dd(J[a], H[n]) < 0.1): nodes += 1
    vn = min(min(rd(N['Venus'], N['Rahu']), rd(N['Venus'], N['Ketu'])) for N in (H, J)); vp = min(dd(N['Venus'], N['Neptune']) for N in (H, J))
    print(f"{nm[:38]:38s} {tn:>3d} {nn:>3d} {skyv:>5d} {soak5:>6d} {nodes:>6d} {vn:>9.2f} {vp:>8.2f}")
s = load(openpyxl.load_workbook(f, data_only=True), 'TRANS')
print(f"sky: Venus–Neptune Dec {dd(s['Venus'], s['Neptune']):.3f} RA {rd(s['Venus'], s['Neptune']):.2f}; Venus–nearest node RA {min(rd(s['Venus'], s['Rahu']), rd(s['Venus'], s['Ketu'])):.2f}; Jupiter–Neptune RA {rd(s['Jupiter'], s['Neptune']):.2f} Dec {dd(s['Jupiter'], s['Neptune']):.3f}")
