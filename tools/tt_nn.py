#!/usr/bin/env python3
"""tt_nn.py RACE OFF DUR_S  (Eddie, 11 Oct 2026: "transit-transit versus natal-natal on the same pair: do they match, or do they both
have a hit, and in the same vibration family").
For one chart and one pair of bodies (A, B):
  NN = distance natal A - natal B (12:00 chart, POS file; fixed)
  TT = distance sky A - sky B (race sky at the course, minute file interpolated every 2 s over the REAL race, off to finish)
in four measures: RA = |dRA| (wrapped to +-180), Dec = |dDec|, Flat = sqrt(dRA^2 + dDec^2), Sky = great circle.
Bodies: Sun Mercury Venus Mars Jupiter Saturn Uranus Neptune Pluto Chiron Ceres Pallas Juno Vesta Rahu Eris Sedna Haumea Makemake
Gonggong Quaoar Orcus Transpluto (no Moon; no Ketu - always opposite Rahu).
Test 1 MATCH: |TT - NN| <= 0.002 deg at some moment in the race (X = crosses NN inside the race; held = within 0.002 at off and finish).
Test 2 SAME FAMILY: NN is within 0.002 deg of a number AND TT is within 0.002 deg of a number of the SAME family at some moment in the race.
  Families (as natnums / rr_extra): phi (k*phi, phi^n, 10*phi^n, n 2..11), sqrt2 (k*sqrt2), whole (k), ninths (k/9, k not a multiple of 9).
  'same number' when both hit the very same value.
Output: per pair of charts (horse / jockey) the counts, then every item (Sun and Mars first)."""
import sys, os, csv, math, itertools, collections
import numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3]); TOL = 0.002
BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta',
          'Rahu', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto']
MEAS = ('RA', 'Dec', 'Flat', 'Sky')
PHI, R2 = (1 + 5 ** .5) / 2, 2 ** .5
sched = int(R[-4:-2]) * 60 + int(R[-2:]); h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
M = collections.defaultdict(dict)
for r in csv.DictReader(open(f'{REPO}/data/sky/{R}__SKYM.csv')):
    if r['body'] in BODIES: M[r['body']][sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
TS = np.arange(t0, t1 + 1e-9, 2 / 60)
def series(b):
    ks = sorted(M[b]); ra = np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))); de = [M[b][k][1] for k in ks]
    return np.interp(TS, ks, ra) % 360, np.interp(TS, ks, de)
SKY = {b: series(b) for b in BODIES if b in M}
def dist(ra1, de1, ra2, de2, mm):
    dra = (np.asarray(ra1) - ra2 + 180) % 360 - 180
    if mm == 'RA': return np.abs(dra)
    if mm == 'Dec': return np.abs(np.asarray(de1) - de2)
    if mm == 'Flat': return np.hypot(dra, np.asarray(de1) - de2)
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    hv = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(hv, 0, 1))))
def numbers(lo, hi):
    """family numbers between lo and hi: (family, label, value)"""
    out = []
    for k in range(max(1, int(lo / PHI)), int(hi / PHI) + 2): out.append(('phi', f'{k}φ', k * PHI))
    for n in range(2, 12): out += [('phi', f'φ^{n}', PHI ** n), ('phi', f'10φ^{n}', 10 * PHI ** n)]
    for k in range(max(1, int(lo / R2)), int(hi / R2) + 2): out.append(('sqrt2', f'{k}√2', k * R2))
    for k in range(max(1, int(lo)), int(hi) + 2): out.append(('whole', f'{k}', float(k)))
    for k in range(max(1, int(lo * 9)), int(hi * 9) + 2):
        if k % 9: out.append(('ninths', f'{k}/9', k / 9))
    return [x for x in out if lo - TOL <= x[2] <= hi + TOL]
meta = list(csv.reader(open(f'{REPO}/data/allpos/{R}__META.csv')))
hdr = next(i for i, r in enumerate(meta) if r[:3] == ['tab', 'role', 'cloth'])
TABS = [dict(zip(meta[hdr], r)) for r in meta[hdr + 1:] if r and r[0].startswith('P')]
NAT = {}
for t in TABS:
    f = f"{REPO}/data/allpos/{R}__{t['tab']}_POS.csv"
    if os.path.exists(f): NAT[t['tab']] = {q['body']: (float(q['ra']), float(q['dec'])) for q in csv.DictReader(open(f)) if q['ra'] and q['body'] in BODIES}
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
TT = {}
for a, b in itertools.combinations([x for x in BODIES if x in SKY], 2):
    for mm in MEAS: TT[(a, b, mm)] = dist(SKY[a][0], SKY[a][1], SKY[b][0], SKY[b][1], mm)
res = collections.defaultdict(list)
for tab, N in NAT.items():
    for a, b in itertools.combinations([x for x in BODIES if x in SKY and x in N], 2):
        for mm in MEAS:
            nn = float(dist(N[a][0], N[a][1], N[b][0], N[b][1], mm)); tt = TT[(a, b, mm)]
            if nn < 0.05 or tt.min() < 0.05: continue
            # test 1: match
            d = tt - nn; ad = np.abs(d)
            if ad.min() <= TOL:
                i = int(ad.argmin()); held = ad[0] <= TOL and ad[-1] <= TOL; cross = (np.sign(d[0]) != np.sign(d[-1]))
                st = ('X,held' if held else 'X') if cross else ('held' if held else 'near')
                res[tab].append(('MATCH', mm, a, b, st, hm(TS[i]), nn, float(tt[i]), '', ''))
            # test 2: both hit a number, same family
            nh = [x for x in numbers(nn - TOL, nn + TOL) if abs(nn - x[2]) <= TOL]
            if not nh: continue
            th = [x for x in numbers(float(tt.min()) - TOL, float(tt.max()) + TOL) if (np.abs(tt - x[2]) <= TOL).any()]
            for fam, lab, val in nh:
                same = [x for x in th if x[0] == fam]
                if same:
                    x = min(same, key=lambda x: (x[1] != lab, float(np.abs(tt - x[2]).min())))
                    i = int(np.abs(tt - x[2]).argmin())
                    res[tab].append(('FAMILY', mm, a, b, 'same number' if x[1] == lab else 'same family', hm(TS[i]), nn, float(tt[i]), lab, x[1]))
name = {t['tab']: t['name'] for t in TABS}
print(f"== {R}  real off {OFF}, finish {hm(t1)}  (TT v NN same body pair; RA / Dec / Flat / Sky; ±{TOL}°)")
hs = [t['tab'] for t in TABS if t['role'] == 'horse' and t['tab'] in NAT]
for hh in hs:
    j = 'P%02d' % (int(hh[1:]) + 1)
    L = res[hh] + res.get(j, [])
    c = lambda k, f=lambda x: True: sum(1 for x in L if x[0] == k and f(x))
    sm = lambda x: x[2] in ('Sun', 'Mars') or x[3] in ('Sun', 'Mars')
    print(f"  {name[hh]:26s} / {name.get(j, '?'):22s} MATCH {c('MATCH'):2d} (X {c('MATCH', lambda x: x[4].startswith('X')):2d})  FAMILY {c('FAMILY'):3d} "
          f"(same number {c('FAMILY', lambda x: x[4] == 'same number'):2d})   with Sun/Mars: MATCH {c('MATCH', sm)} FAMILY {c('FAMILY', sm)}")
for hh in hs:
    j = 'P%02d' % (int(hh[1:]) + 1); print(f"\n-- {name[hh]} / {name.get(j, '?')}")
    for tab, who in ((hh, 'horse'), (j, 'jockey')):
        for x in sorted(res.get(tab, []), key=lambda x: (x[0], not (x[2] in ('Sun', 'Mars') or x[3] in ('Sun', 'Mars')), x[1])):
            extra = f"NN {x[8]} / TT {x[9]}" if x[0] == 'FAMILY' else ''
            print(f"   {who:6s} {x[0]:6s} {x[1]:4s} {x[2]}–{x[3]}  {x[4]:11s} {x[5]}  NN {x[6]:.4f} TT {x[7]:.4f}  {extra}")
