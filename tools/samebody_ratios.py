#!/usr/bin/env python3
"""samebody_ratios.py RACE OFF DUR_S [TOL]  (Eddie, 11 Oct 2026: "in the transit to natal same body distances, are there any ratios between
pairs in RA, Dec or direct" - a simpler look).
Same-body distance of a body X for one chart = distance from sky X (race sky, topocentric, minute file) to natal X (12:00 chart, POS file);
natal Moon left out (so the sky Moon too); Ketu left out (its same-body distance always equals Rahu's). Measures: RA, Dec, Sky (direct, great circle).
Ratios: every pair of same-body distances in one measure, (a) within a chart, (b) across the pair (horse X with jockey Y), compared with the
interval list (lattice/families.py IV). Kept when the ratio is within TOL (default 0.005%) at some moment in the real race (scanned every 2 s);
'held' = within TOL at both the off and the finish, 'X' = comes exact inside the race. Distances under 0.05 deg are skipped.
Output: one line per chart (count), then the ratios of each chart, Sun and Mars first."""
import sys, os, csv, itertools, collections, math
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3]); TOL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.00005
BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta',
          'Rahu', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto']
sched = int(R[-4:-2]) * 60 + int(R[-2:]); h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
M = collections.defaultdict(dict)
for r in csv.DictReader(open(f'{REPO}/data/sky/{R}__SKYM.csv')):
    if r['body'] in BODIES: M[r['body']][sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
TS = np.arange(t0, t1 + 1e-9, 2 / 60)
def series(b):
    ks = sorted(M[b]); ra = np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))); de = [M[b][k][1] for k in ks]
    return np.interp(TS, ks, ra) % 360, np.interp(TS, ks, de)
SKY = {b: series(b) for b in BODIES if b in M}
meta = list(csv.reader(open(f'{REPO}/data/allpos/{R}__META.csv')))
hdr = next(i for i, r in enumerate(meta) if r[:3] == ['tab', 'role', 'cloth'])
TABS = [dict(zip(meta[hdr], r)) for r in meta[hdr + 1:] if r and r[0].startswith('P')]
NAT = {}
for t in TABS:
    f = f"{REPO}/data/allpos/{R}__{t['tab']}_POS.csv"
    if os.path.exists(f): NAT[t['tab']] = {q['body']: (float(q['ra']), float(q['dec'])) for q in csv.DictReader(open(f)) if q['ra'] and q['body'] in BODIES}
def sbd(tab, b, mm):
    """same-body distance series (sky b to natal b) over the race"""
    ra, de = SKY[b]; n = NAT[tab][b]
    if mm == 'RA': return np.abs((ra - n[0] + 180) % 360 - 180)
    if mm == 'Dec': return np.abs(de - n[1])
    r1, d1, r2, d2 = np.radians(ra), np.radians(de), math.radians(n[0]), math.radians(n[1])
    hv = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * math.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(hv, 0, 1))))
IVV = np.array(list(IV.values())); IVK = list(IV.keys())
def best(a, b):
    """min over the race of the ratio's deviation from its nearest interval value -> (dev, name, i)"""
    ok = (a >= 0.05) & (b >= 0.05)
    if not ok.any(): return None
    r = np.where(ok, np.maximum(a, b) / np.minimum(np.where(ok, a, 1), np.where(ok, b, 1)), np.nan)
    dv = np.abs(IVV[None, :] - r[:, None]) / IVV[None, :]; k = np.nanargmin(np.nan_to_num(dv, nan=9).min(axis=1))
    j = int(np.argmin(dv[k])); return float(dv[k, j]), IVK[j], int(k), float(dv[0].min()), float(dv[-1].min())
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
D = {(tab, b, mm): sbd(tab, b, mm) for tab in NAT for b in BODIES if b in SKY and b in NAT[tab] for mm in ('RA', 'Dec', 'Sky')}
hits = collections.defaultdict(list)
def scan(ta, tb, kind):
    for mm in ('RA', 'Dec', 'Sky'):
        pairs = itertools.combinations(BODIES, 2) if ta == tb else itertools.product(BODIES, BODIES)
        for x, y in pairs:
            if (ta, x, mm) not in D or (tb, y, mm) not in D: continue
            r = best(D[(ta, x, mm)], D[(tb, y, mm)])
            if not r or r[0] > TOL: continue
            dv, name, i, d0, d1 = r
            st = 'held' if (d0 <= TOL and d1 <= TOL) else ('X' if 0 < i < len(TS) - 1 else ('at off' if i == 0 else 'at finish'))
            hits[(ta, tb)].append((dv, kind, mm, x, y, name, st, hm(TS[i]), float(D[(ta, x, mm)][i]), float(D[(tb, y, mm)][i])))
for t in TABS:
    if t['tab'] in NAT: scan(t['tab'], t['tab'], 'chart')
role = {t['tab']: t['role'] for t in TABS}; name = {t['tab']: t['name'] for t in TABS}
partner = {}
for t in TABS:
    if t['role'] == 'horse':
        j = 'P%02d' % (int(t['tab'][1:]) + 1)
        if j in NAT and t['tab'] in NAT: partner[t['tab']] = j; scan(t['tab'], j, 'pair')
print(f"== {R}  real off {OFF}, finish {hm(t1)}  (same-body distance ratios ≤{TOL*100:.3f}% in the race; RA / Dec / Sky)")
print("counts: chart (own two bodies) | pair (horse body : jockey body)  ·  with Sun or Mars")
for t in TABS:
    tab = t['tab']
    if t['role'] != 'horse' or tab not in partner: continue
    j = partner[tab]; c = hits[(tab, tab)] + hits[(j, j)]; p = hits[(tab, j)]
    sm = lambda L: sum(1 for z in L if 'Sun' in (z[3], z[4]) or 'Mars' in (z[3], z[4]))
    print(f"  {name[tab]:28s} / {name[j]:24s}  horse {len(hits[(tab, tab)]):2d}  jockey {len(hits[(j, j)]):2d}  pair {len(p):2d}   Sun/Mars: {sm(c)} + pair {sm(p)}")
for t in TABS:
    tab = t['tab']
    if t['role'] != 'horse' or tab not in partner: continue
    j = partner[tab]; print(f"\n-- {name[tab]} / {name[j]}")
    for who, L in (('horse', hits[(tab, tab)]), ('jockey', hits[(j, j)]), ('pair H:J', hits[(tab, j)])):
        for z in sorted(L, key=lambda z: (not ('Sun' in z[3:5] or 'Mars' in z[3:5]), z[0])):
            print(f"   {who:8s} {z[2]:3s} {z[3]}:{z[4]}  {z[5]:6s} {z[0]*100:.4f}%  {z[6]:9s} {z[7]}  [{z[8]:.3f} / {z[9]:.3f}]")
