#!/usr/bin/env python3
"""sky_numbers.py RACE OFF DUR_S [TOL] [MARGIN_MIN]  (Eddie, 11 Oct 2026: "any other extremely strong connections in the transit sky at that
time" - after Uranus-Regulus Dec = 9.00002 deg at Southwell 20:00).
Race sky only (no charts). Every pair of sky points - the bodies (Sun..Transpluto, Rahu, Ketu, Moon), the 22 stars as on the day, and the
Equator (Dec only, distance = |Dec|) - except star-star pairs (fixed for years). Measures RA (|dRA| wrapped), Dec (|dDec|),
Flat (sqrt(dRA^2+dDec^2)), Sky (great circle). The distance is compared with the numbers: whole k, ninths k/9 (k not a multiple of 9),
k*phi, phi^n and 10*phi^n (n 2..11), k*sqrt2. Kept when within TOL (default 0.0001 deg) at some moment from off-MARGIN to finish+MARGIN
(default 0, the real race), scanned every 2 s. 'crossing' = the distance passes through the number in the window; 'held' = within TOL
at both ends of the window."""
import sys, os, csv, math, itertools, collections
import numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
TOL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0001; MARG = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
exec(open('/home/claude/lattice/families.py').read().split("N = sorted(S)")[0].split("S = {}")[0])   # STARS, PHI
STARSET = set(STARS)
SKIP = {'Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit', 'equator', 'body'}
sched = int(R[-4:-2]) * 60 + int(R[-2:]); h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60 - MARG; t1 = h * 60 + m + s / 60 + DUR / 60 + MARG
M = collections.defaultdict(dict)
for r in csv.DictReader(open(f'{REPO}/data/sky/{R}__SKYM.csv')):
    if r['body'] not in SKIP: M[r['body']][sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
TS = np.arange(t0, t1 + 1e-9, 2 / 60)
def series(b):
    ks = sorted(M[b]); ra = np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))); de = [M[b][k][1] for k in ks]
    return np.interp(TS, ks, ra) % 360, np.interp(TS, ks, de)
P = {b: series(b) for b in M}
PHI_, R2 = (1 + 5 ** .5) / 2, 2 ** .5
def nums(lo, hi):
    out = []
    for k in range(max(1, math.floor(lo)), math.ceil(hi) + 1): out.append(('whole', f'{k}', float(k)))
    for k in range(max(1, math.floor(lo * 9)), math.ceil(hi * 9) + 1):
        if k % 9: out.append(('ninths', f'{k}/9', k / 9))
    for k in range(max(1, math.floor(lo / PHI_)), math.ceil(hi / PHI_) + 1): out.append(('phi', f'{k}φ', k * PHI_))
    for n in range(2, 12): out += [('phi', f'φ^{n}', PHI_ ** n), ('phi', f'10φ^{n}', 10 * PHI_ ** n)]
    for k in range(max(1, math.floor(lo / R2)), math.ceil(hi / R2) + 1): out.append(('sqrt2', f'{k}√2', k * R2))
    return [x for x in out if lo - TOL <= x[2] <= hi + TOL]
def dist(a, b, mm):
    ra1, d1 = P[a];
    if b == 'Equator': return np.abs(d1) if mm == 'Dec' else None
    ra2, d2 = P[b]; dra = (ra1 - ra2 + 180) % 360 - 180
    if mm == 'RA': return np.abs(dra)
    if mm == 'Dec': return np.abs(d1 - d2)
    if mm == 'Flat': return np.hypot(dra, d1 - d2)
    r1, e1, r2, e2 = map(np.radians, (ra1, d1, ra2, d2))
    hv = np.sin((e2 - e1) / 2) ** 2 + np.cos(e1) * np.cos(e2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(hv, 0, 1))))
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
pts = sorted(P) + ['Equator']; hits = []; n_dist = 0
for a, b in itertools.combinations(pts, 2):
    if a == 'Equator': a, b = b, a
    if a in STARSET and b in STARSET: continue
    if {a, b} == {'Rahu', 'Ketu'}: continue
    for mm in ('RA', 'Dec', 'Flat', 'Sky'):
        d = dist(a, b, mm)
        if d is None or d.max() < 0.05: continue
        n_dist += 1
        for fam, lab, v in nums(float(d.min()), float(d.max())):
            e = np.abs(d - v); i = int(e.argmin())
            if e[i] <= TOL:
                cross = np.sign(d[0] - v) != np.sign(d[-1] - v); held = e[0] <= TOL and e[-1] <= TOL
                hits.append((float(e[i]), a, b, mm, fam, lab, float(d[i]), hm(TS[i]), 'crossing' if cross else ('held' if held else 'touch'),
                             'Moon' in (a, b), float(d.max() - d.min())))
print(f"== {R} window {hm(t0)}–{hm(t1)}  sky distances within {TOL}° of a number ({n_dist} distances tested, star-star left out)")
fc = collections.Counter(x[4] for x in hits); print("   by family:", dict(fc), f"  with the Moon: {sum(x[9] for x in hits)}")
SLOW = 0.0005   # 'still' = the distance moved less than this over the window (both points nearly fixed)
print(f"   still distances (moved <{SLOW}° in the window): {sum(1 for x in hits if x[10] < SLOW)}  (whole numbers {sum(1 for x in hits if x[10] < SLOW and x[4] == 'whole')})")
for x in sorted(hits, key=lambda x: (x[10] >= SLOW, x[9], x[0])):
    print(f"   {x[0]:.6f}  {x[3]:4s} {x[1]}–{x[2]:12s} = {x[5]:8s} ({x[4]:6s}) dist {x[6]:.6f} at {x[7]}  {x[8]:8s} moved {x[10]:.6f}{'  STILL' if x[10] < SLOW else ''}{'  MOON' if x[9] else ''}")
