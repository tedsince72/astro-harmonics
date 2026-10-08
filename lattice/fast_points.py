"""fast_points.py RACE OFF DUR_S - Layer 5 side note: the fast points (Ascendant, Midheaven, Vertex, Part of Fortune, Part of Spirit)
in the race minutes. Transit only (no natal angles at midday). Base = a fast point at one end, other end any Layer-1 point, body or
fast point; third point a body. Chords exact (locked search, 1 s) between off-2 and the finish."""
import sys
src = open('/home/claude/lattice/layer1_tuned.py').read()
exec(src.split('# transit chords')[0])
FPN = [b for b in ('Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit') if b in M]
def P(n, t): return REF[n] if n in REF else pos(n, t)
ends = list(RN) + BODIES + FPN
hits = {}
for t in np.arange(t0 - 2, t1 + 1e-9, 0.25):
    for f in FPN:
        for e in ends:
            if e == f or (e in FPN and FPN.index(e) < FPN.index(f)): continue
            for b in BODIES:
                if b == e: continue
                for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                    if {'Rahu', 'Ketu'} <= {e, b} and mm in ('RA', 'Sky'): continue
                    r = tri(P(f, t), P(e, t), P(b, t), mm)
                    if r and r[1] <= 0.0015:
                        k = (mm, f, e, b)
                        if k not in hits: hits[k] = lockT(P(f, t), P(e, t), P(b, t), mm)
out = []
for k, T in hits.items():
    mm, f, e, b = k
    LOCKT = T; best = (9, None, None)
    for t in np.arange(t0 - 2.5, t1 + 0.5, 1 / 60):
        r = tri(P(f, t), P(e, t), P(b, t), mm)
        if r and r[1] < best[0]: best = (r[1], t, r[0])
    LOCKT = None
    if best[1] is not None and t0 - 2 <= best[1] <= t1 and best[0] <= 0.0002:
        out.append((best[1], k, best[0], ctype(best[2]), best[2]))
print('=' * 110); print(f"{RACE}  off {OFF}  finish {hm(t1)}  - LAYER 5 SIDE NOTE: fast-point chords exact in the race window (to 0.02%)"); print('=' * 110)
for t, k, dv, typ, d in sorted(out):
    mm, f, e, b = k; tag = 'DURING' if t >= t0 else 'before'
    print(f"   {hm(t)} ({t - t0:+.2f}) {tag:6s} {mm:4s} {f}–{e} + {b:10s} {typ:14s} {d[0]:.3f} | {d[1]:.3f} | {d[2]:.3f}  dev {dv*100:.4f}%")
print(f"   ({len(out)} chords)")
