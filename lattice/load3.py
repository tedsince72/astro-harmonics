"""load3.py GROUP.csv - STEP 3: chord load of every body against the star lattice, race by race (Eddie, 5 Oct 2026).
For every transit body (Nodes, L2, L3, Sun/Mercury/Venus, Moon) and every 0.05 min of the afternoon: the number of star
pairs with which it completes a full chord (all three distances in interval ratios, 0.15%), in RA, Dec, Flat Dist and Sky Dist.
Positions stitched from the race minute files (each minute from the nearest race's file; the Moon as seen from that course).
Race window = 2 min before the off to the finish. A body is LIT at a race when its peak load in the window is at or above
its own 95th percentile for the afternoon. Output: race by race, lit bodies with the chords; then a B/W summary."""
import sys, csv, itertools, collections, math
import numpy as np
sys.path.insert(0, '/home/claude/ledger')
from readrace import STARS, FAST, PHI, SKYD
G = list(csv.DictReader(open(sys.argv[1])))
for g in G:
    h, m, s = map(int, g['off'].split(':')); g['t0'] = h * 60 + m + s / 60; g['t1'] = g['t0'] + float(g['dur_s'] or 90) / 60
    g['sched'] = int(g['race'][-4:-2]) * 60 + int(g['race'][-2:]); g['label'] = g['race'].split('_', 1)[1]
G.sort(key=lambda g: g['t0'])
IV = [1, 2, 1.5, 4 / 3, 3, 4, 1.25, 1.2, 5 / 3, 1.6, 2.5, 8 / 3, 9 / 4, 2 ** .5, 1 + 2 ** -.5, 9 / 8, 16 / 9, 9 / 5, 15 / 8, 16 / 15, 7 / 4, 7 / 3, 7 / 2, 7 / 5, 7 / 6, 8 / 7,
      5, 6, 7, 8, 9, 11 / 5, 11 / 6, 11 / 3, 11 / 8, 11 / 4, 13 / 5, 13 / 8, 13 / 4, PHI, PHI ** 2, PHI ** 3, 1 + 2 ** .5, PHI * 5 ** .5, 2 - 1 / PHI, PHI ** 3 + 1, 2 / PHI]
IVa = np.array(IV)
def W(x): return (x + 180) % 360 - 180
P = {}
for g in G:
    for r in csv.DictReader(open(f"{SKYD}/{g['race']}__SKYM.csv")):
        t = g['sched'] + int(r['minute'])
        cur = P.setdefault(r['body'], {})
        if t not in cur or abs(t - g['t0']) < cur[t][2]: cur[t] = (float(r['ra']), float(r['dec']), abs(t - g['t0']))
T = np.arange(G[0]['t0'] - 20, G[-1]['t1'] + 20, 0.05)
def arr(d):
    ks = np.array(sorted(d)); ra = np.unwrap(np.radians([d[k][0] for k in ks])); de = np.array([d[k][1] for k in ks])
    return np.degrees(np.interp(T, ks, ra)) % 360, np.interp(T, ks, de)
stars = sorted(b for b in P if b in STARS)
SP = {s: arr(P[s]) for s in stars}
SPOS = {s: (float(np.median(SP[s][0])), float(np.median(SP[s][1]))) for s in stars}
pairs = list(itertools.combinations(stars, 2))
def dmat(X, m):
    """distances body->each star over T: (nstars, T)"""
    out = []
    for s in stars:
        a = SPOS[s]
        if m == 'RA': out.append(np.abs(W(X[0] - a[0])))
        elif m == 'Dec': out.append(np.abs(X[1] - a[1]))
        elif m == 'Flat': out.append(np.sqrt(W(X[0] - a[0]) ** 2 + (X[1] - a[1]) ** 2))
        else:
            r1, d1, r2, d2 = map(np.radians, (X[0], X[1], a[0], a[1]))
            hh = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
            out.append(np.degrees(2 * np.arcsin(np.sqrt(np.clip(hh, 0, 1)))))
    return np.array(out)
def sdist(a, b, m):
    A, B = SPOS[a], SPOS[b]
    if m == 'RA': return abs(W(A[0] - B[0]))
    if m == 'Dec': return abs(A[1] - B[1])
    if m == 'Flat': return math.hypot(W(A[0] - B[0]), A[1] - B[1])
    r1, d1, r2, d2 = map(math.radians, (A[0], A[1], B[0], B[1]))
    hh = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin((r2 - r1) / 2) ** 2
    return math.degrees(2 * math.asin(math.sqrt(min(1, max(0, hh)))))
def isiv(r):
    out = np.zeros(r.shape, bool)
    for v in IVa: out |= np.abs(r - v) <= 0.0015 * v
    return out
idx = {s: i for i, s in enumerate(stars)}
BODIES = ['Rahu', 'Ketu', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Transpluto', 'Eris', 'Sedna', 'Makemake', 'Haumea', 'Gonggong', 'Quaoar', 'Orcus',
          'Jupiter', 'Saturn', 'Mars', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Sun', 'Mercury', 'Venus', 'Moon']
LOAD = {}; WHO = {}
for b in [x for x in BODIES if x in P]:
    X = arr(P[b]); tot = np.zeros(len(T), int); who = collections.defaultdict(list)
    for m in ('RA', 'Dec', 'Flat', 'Sky'):
        D = dmat(X, m)
        for a, c in pairs:
            d1, d2, d3 = D[idx[a]], D[idx[c]], sdist(a, c, m)
            if d3 < 0.05: continue
            ok = (np.minimum(d1, d2) > 0.05)
            r12 = np.maximum(d1, d2) / np.maximum(np.minimum(d1, d2), 1e-9)
            r13 = np.maximum(d1, d3) / np.maximum(np.minimum(d1, d3), 1e-9)
            r23 = np.maximum(d2, d3) / np.maximum(np.minimum(d2, d3), 1e-9)
            hit = ok & isiv(r12) & isiv(r13) & isiv(r23)
            if hit.any():
                tot += hit
                for k in np.nonzero(hit)[0]: who[k].append(f"{m} {a}–{c}")
    LOAD[b] = tot; WHO[b] = who
    print(f"  {b}", file=sys.stderr)
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
print('=' * 120)
print(f"STEP 3 - CHORD LOAD AGAINST THE STAR LATTICE   {G[0]['race'][:8]}   race window = off-2 min to finish; LIT = peak >= the body's own 95th percentile for the afternoon")
print('=' * 120)
print("   body        afternoon mean  95th pct  max (time)")
P95 = {}
for b in LOAD:
    L = LOAD[b]; P95[b] = max(1, np.percentile(L, 95)); k = int(L.argmax())
    print(f"   {b:11s} {L.mean():8.2f} {P95[b]:9.0f} {L.max():5d} ({hm(T[k])})")
summ = []
def peak(b, a, z):
    w = (T >= a) & (T <= z)
    if not w.any() or a < T[0] or z > T[-1]: return None, None
    k = np.nonzero(w)[0][int(LOAD[b][w].argmax())]; return int(LOAD[b][k]), k
for g in G:
    a, z = g['t0'] - 2, g['t1']
    lit, held = [], []
    for b in LOAD:
        n, k = peak(b, a, z)
        if n is None or n == 0: continue
        sh = [peak(b, a + d, z + d)[0] for d in (-90, -60, -30, 30, 60, 90)]
        sh = [x for x in sh if x is not None]
        if np.ptp(LOAD[b]) == 0: held.append((b, n)); continue
        if sh and n > max(sh): lit.append((b, n, T[k], WHO[b][k], sh))
    summ.append((g, lit, held))
    print(f"\n--- {g['band']} {g['label']:22s} off {g['off']}  finish {hm(g['t1'])}  {g['note']}")
    print(f"    LIT (peak in the race window higher than in every window 30/60/90 min either side): {len(lit)}")
    for b, n, t, wh, sh in sorted(lit, key=lambda x: x[2]):
        rel = f"off {t - g['t0']:+.2f}m" if t < g['t0'] else f"+{t - g['t0']:.2f}m"
        print(f"      {hm(t)} {rel:12s} {b:10s} {n:2d} chords (shifted peaks {'/'.join(map(str, sh))}): {', '.join(wh)}")
print('\n' + '=' * 120)
print("SUMMARY")
for band in ('B', 'W'):
    S_ = [x for x in summ if x[0]['band'] == band]
    if S_: print(f"   {band}: {len(S_)} races  mean lit bodies {np.mean([len(x[1]) for x in S_]):.2f}")
for g, lit, held in summ: print(f"   {g['band']} {g['label']:22s} lit {len(lit):2d}   {', '.join(f'{b} {n}' for b, n, *_ in sorted(lit, key=lambda x: x[2]))}")
