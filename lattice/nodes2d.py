"""nodes2d.py - 2-D nodes of the star lattice in Flat Dist and Sky Dist (Eddie, 5 Oct 2026).
For every star pair A-B and every pair of ratios (r1, r2) with r1, r2 and r1/r2 all on the interval list (or reciprocals),
the points X with d(X,A) = r1*d(A,B) and d(X,B) = r2*d(A,B) complete a chord with A-B (circle intersections; two per case).
A node = a spot where chord points from several different star pairs fall within 0.1 deg of each other: a body there
completes several star chords at once. Chance check: the same for the stars jittered +-3 deg and for random points."""
import itertools, math, random, collections, sys
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])
vals = sorted(set(list(IV.values()) + [1 / v for v in IV.values()]))
vals = np.array(vals)
def inset(x): return np.min(np.abs(vals - x) / vals) <= 0.0015
RR = [(r1, r2) for r1 in vals for r2 in vals if r1 <= 12 and r2 <= 12 and inset(r1 / r2)]
def flat_points(A, B, d1, d2):
    dx, dy = W(B[0] - A[0]), B[1] - A[1]; D = math.hypot(dx, dy)
    if D == 0 or d1 + d2 < D or abs(d1 - d2) > D: return []
    a = (d1 * d1 - d2 * d2 + D * D) / (2 * D); h = math.sqrt(max(0, d1 * d1 - a * a))
    ux, uy = dx / D, dy / D
    out = []
    for s in (1, -1):
        x, y = a * ux - s * h * uy, a * uy + s * h * ux
        out.append(((A[0] + x) % 360, A[1] + y))
    return out
def vec(p): r, d = map(math.radians, p); return np.array([math.cos(d) * math.cos(r), math.cos(d) * math.sin(r), math.sin(d)])
def sky_points(A, B, d1, d2):
    a, b = vec(A), vec(B); c1, c2 = math.cos(math.radians(d1)), math.cos(math.radians(d2))
    ab = a @ b
    if abs(1 - ab * ab) < 1e-12 or d1 > 180 or d2 > 180: return []
    x = (c1 - c2 * ab) / (1 - ab * ab); y = (c2 - c1 * ab) / (1 - ab * ab)
    p = x * a + y * b; n = np.cross(a, b); q = 1 - p @ p
    if q < 0: return []
    out = []
    for s in (1, -1):
        v = p + s * math.sqrt(q) / np.linalg.norm(n) * n
        out.append((math.degrees(math.atan2(v[1], v[0])) % 360, math.degrees(math.asin(max(-1, min(1, v[2]))))))
    return out
def chordpoints(P, names, m):
    pts = []
    for a, b in itertools.combinations(names, 2):
        A, B = P[a], P[b]; D = dist(A, B, m)
        if D < 0.05: continue
        for r1, r2 in RR:
            for X in (flat_points if m == 'Flat' else sky_points)(A, B, r1 * D, r2 * D):
                if -40 <= X[1] <= 90: pts.append((X[0], X[1], a + '–' + b, r1, r2))
    return pts
def nodes(pts, rad=0.1):
    grid = collections.defaultdict(list)
    for i, p in enumerate(pts): grid[(int(p[0] / rad), int((p[1] + 90) / rad))].append(i)
    best = []
    for key, idx in grid.items():
        cand = [j for dx in (-1, 0, 1) for dy in (-1, 0, 1) for j in grid.get((key[0] + dx, key[1] + dy), [])]
        for i in idx:
            near = [j for j in cand if abs(W(pts[j][0] - pts[i][0])) < rad and abs(pts[j][1] - pts[i][1]) < rad]
            prs = {pts[j][2] for j in near}
            best.append((len(prs), i, near))
    best.sort(key=lambda x: -x[0])
    sel = []
    for n, i, near in best:
        if any(abs(W(pts[i][0] - pts[k][0])) < 1 and abs(pts[i][1] - pts[k][1]) < 1 for _, k, _ in sel): continue
        sel.append((n, i, near))
        if len(sel) >= 25: break
    return sel
if __name__ == '__main__':
    for m in ('Flat', 'Sky'):
        pts = chordpoints(S, N, m)
        sel = nodes(pts)
        print(f"\n{m} DIST - {len(pts)} chord points; top nodes (distinct star pairs completed within 0.1°)")
        for n, i, near in sel:
            p = pts[i]; prs = sorted({pts[j][2] for j in near})
            print(f"  RA {p[0]:7.2f} Dec {p[1]:+6.2f}   {n:2d} pairs: " + ', '.join(prs))
        # chance
        random.seed(2); mx = []
        for k in range(12):
            J = {s: ((S[s][0] + random.uniform(-3, 3)) % 360, S[s][1] + random.uniform(-3, 3)) for s in N}
            ps = chordpoints(J, N, m); mx.append([x[0] for x in nodes(ps)[:5]])
        print(f"  chance (stars jittered ±3°, 12 skies): top-5 node sizes " + '; '.join('/'.join(map(str, v)) for v in mx))
        print(f"  real top-5: {'/'.join(str(x[0]) for x in sel[:5])}")
