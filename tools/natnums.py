"""natnums RACE OFF DUR TAB BODY [TOL]: Method 1 (original imprint, numbers), one natal body at a time.
The body's own RA / |Dec|, and its RA, Dec, Flat and Sky distances to every other natal body (no Moon) and every star at birth,
tested against kφ, φ^n (and 10φ^n), k√2, whole numbers and ninths within ±TOL (default 0.002°).
Over the birth day (hourly positions, interpolated by the minute) each hit gets its time window: ALL DAY, or hh:mm–hh:mm."""
import sys, csv, numpy as np
TAB, BODY = sys.argv[4], sys.argv[5]; TOL = float(sys.argv[6]) if len(sys.argv) > 6 else 0.002; HOUR = float(sys.argv[7]) if len(sys.argv) > 7 else 12.0; sys.argv = sys.argv[:4]
src = open('/home/claude/lattice/layer1_tuned.py').read(); exec(src.split('# transit chords')[0])
PHI = (1 + 5 ** .5) / 2; R2 = 2 ** .5
H = {}
for r in csv.DictReader(open(f'/home/claude/ledger/allpos/{sys.argv[1]}__NATAL_HOURLY.csv')):
    if r['tab'] == TAB and r['ra']: H.setdefault(r['body'], {})[int(r['hour'])] = (float(r['ra']), float(r['dec']))
def name(b): return b[:-2] if b.endswith('_B') else b
SKIP = {'Moon', 'equator', 'Aldebaran', 'Antares', 'Regulus', 'Fomalhaut'}
others = [b for b in H if b != BODY and b not in SKIP]
MIN = np.arange(0, 24 * 60 + 1)
def track(b):
    hs = sorted(H[b]); ra = np.degrees(np.unwrap(np.radians([H[b][h][0] for h in hs]))); de = [H[b][h][1] for h in hs]
    return np.interp(MIN / 60, hs, ra) % 360, np.interp(MIN / 60, hs, de)
X = track(BODY)
def targets(x):
    out = []
    k = round(x / PHI)
    if k > 0: out.append((f"{k}φ", k * PHI))
    for n in range(2, 12):
        out += [(f"φ^{n}", PHI ** n), (f"10φ^{n}", 10 * PHI ** n)]
    k = round(x / R2)
    if k > 0: out.append((f"{k}√2", k * R2))
    k = round(x * 9)
    if k % 9: out.append((f"{k}/9", k / 9))
    k = round(x)
    if k > 0: out.append((f"whole {k}", float(k)))
    return out
def window(vals, t):
    ok = np.abs(vals - t) <= TOL
    if ok.all(): return 'ALL DAY'
    if not ok.any(): return None
    idx = np.where(ok)[0]; segs = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i != p + 1: segs.append((s, p)); s = i
        p = i
    segs.append((s, p))
    return ', '.join(f"{a // 60:02d}:{a % 60:02d}–{b // 60:02d}:{b % 60:02d}" for a, b in segs)
def dists(o, mm):
    Y = track(o)
    return np.array([dist((X[0][i], X[1][i]), (Y[0][i], Y[1][i]), mm) for i in range(0, len(MIN))])
rows = []
vals = {('own', 'RA'): X[0], ('own', '|Dec|'): np.abs(X[1])}
for o in others:
    for mm in ('RA', 'Dec', 'Flat', 'Sky'):
        vals[(name(o) + (' ★' if o.endswith('_B') else ''), mm)] = dists(o, mm)
n = {}
for (o, mm), v in vals.items():
    n[mm] = n.get(mm, 0) + 1
    mid = v[int(round(HOUR * 60))]
    for lab, t in targets(mid):
        w = window(v, t)
        if w and abs(mid - t) <= TOL: rows.append((mm, o, mid, lab, t, w, v[0], v[-1]))
        elif w and abs(mid - t) > TOL and w != 'ALL DAY': rows.append((mm, o, mid, lab, t, w + ' (not at midday)', v[0], v[-1]))
pp = 2 * TOL * (1 / PHI + 1 / R2 + 1); p9 = 2 * TOL * 8
print(f"{name(BODY)} — natal numbers ({TAB}, at {HOUR:g}h); ±{TOL}°; ★ = star at birth. Values tested: " + ', '.join(f"{k} {v}" for k, v in n.items()))
print(f"   chance per value at one moment: φ/√2/whole {pp:.4f}, ninths {p9:.4f}")
for mm in ('own', 'RA', '|Dec|', 'Dec', 'Flat', 'Sky'):
    L = [r for r in rows if r[0] == mm]
    if not L: continue
    print(f"\n{mm}:")
    for _, o, mid, lab, t, w, a, b in sorted(L, key=lambda r: (('ALL DAY' not in r[5]), 'not at' in r[5], abs(r[2] - r[4]))):
        print(f"  to {o:14s} {mid:10.4f} = {lab:10s} ({t:.4f}, off {mid - t:+.4f})   {w}   [00:00 {a:.4f} · 24:00 {b:.4f}]")
