"""Sun-Moon in the race sky (no charts): (A) chords Sun+Moon+X (all three ratios in the interval list); (B) direct ratios of two sides
sharing a point: d(Sun,Moon)/d(Sun,X), d(Sun,Moon)/d(Moon,X) [and d(Sun,X)/d(Moon,X)]. Scanned every 2 s over the REAL race (off..finish)."""
import sys, csv, math, itertools, collections
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])
R = sys.argv[1]; OFF = sys.argv[2]; DUR = float(sys.argv[3]); TOL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0005
sched = int(R[-4:-2]) * 60 + int(R[-2:])
h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
M = collections.defaultdict(dict)
import os
SKYDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'sky')
for r in csv.DictReader(open(f'{SKYDIR}/{R}__SKYM.csv')):
    if r['body'] == 'body': continue
    M[r['body']][sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
FAST = {'Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit'}
def pos(b, t):
    ks = sorted(M[b]); ra = np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))); de = [M[b][k][1] for k in ks]
    return float(np.interp(t, ks, ra)) % 360, float(np.interp(t, ks, de))
TS = np.arange(t0, t1 + 1e-9, 2 / 60)
P = {b: [pos(b, t) for t in TS] for b in M if b not in FAST}
P['Equator'] = [(None, 0.0)] * len(TS)
X = [b for b in P if b not in ('Sun', 'Moon')]
def d(a, b, mm):
    if a[0] is None or b[0] is None:
        return abs(a[1] - b[1]) if mm == 'Dec' else None
    return dist(a, b, mm)
chords, ratios = [], []
for x in X:
    for mm in ('RA', 'Dec', 'Flat', 'Sky'):
        if x == 'Equator' and mm != 'Dec': continue
        best = None; rb = {}
        for i, t in enumerate(TS):
            S, Mo, Y = P['Sun'][i], P['Moon'][i], P[x][i]
            sm, sx, mx = d(S, Mo, mm), d(S, Y, mm), d(Mo, Y, mm)
            if None in (sm, sx, mx) or min(sm, sx, mx) < 0.05: continue
            sides = {'SM/SX': (sm, sx), 'SM/MX': (sm, mx), 'SX/MX': (sx, mx)}
            devs = {}
            for k, (a, b) in sides.items():
                q, dv = iv(max(a, b) / min(a, b)); devs[k] = (dv, q)
                if k not in rb or dv < rb[k][0]: rb[k] = (dv, q, t, i)
            dvc = max(v[0] for v in devs.values())
            if best is None or dvc < best[0]: best = (dvc, t, (sm, sx, mx), i)
        if best and best[0] <= 0.0015: chords.append((best[0], x, mm, ctype(best[2]), best[1], best[2]) + (('edge' if best[3] in (0, len(TS) - 1) else 'in'),))
        for k, (dv, q, t, i) in rb.items():
            if dv <= TOL and 0 < i < len(TS) - 1: ratios.append((dv, x, mm, k, q, t))   # interior minimum = it comes exact in the race
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
print(f"== {R} off {OFF} finish {hm(t1)} ({DUR:.0f}s)")
print(f"A. Sun–Moon–X chords (min over the race, ≤0.15%): {len(chords)}")
for dv, x, mm, ty, t, dd, e in sorted(chords): print(f"   {dv*100:.3f}% {e:4s} {mm:4s} Sun–Moon–{x:12s} {ty:22s} at {hm(t)}  [SM {dd[0]:.3f} SX {dd[1]:.3f} MX {dd[2]:.3f}]")
print(f"B. direct ratios exact in the race (≤{TOL*100:.3f}%): {len(ratios)}  (SM/SX {sum(r[3]=='SM/SX' for r in ratios)}, SM/MX {sum(r[3]=='SM/MX' for r in ratios)}, SX/MX {sum(r[3]=='SX/MX' for r in ratios)})")
for dv, x, mm, k, q, t in sorted(ratios, key=lambda r: (r[3], r[0])): print(f"   {k}  {mm:4s} X={x:12s} ratio {q:6s} {dv*100:.4f}% at {hm(t)}")
