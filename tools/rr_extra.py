"""rr_extra.py RACE OFF DUR_S OUTJSON - the pieces of the runner record that had no tool yet (Eddie, 8 Oct 17:38 procedure).
Window off-30 min to finish+30 min, from the 1-minute engine grid (MOONWIN=wide), checked every 5 s.
1. NATAL -> TRANSIT numbers, same body: natal X at 12:00 to sky X (RA, Dec, Flat, Sky), every chart, every body but the Moon.
2. SKY BODY -> STAR numbers: each sky body's |Dec| and its RA and Dec distances to the race-day stars (and Dec to course latitude);
   own RA left out (a body's own RA does not count, own Dec does).
3. PARALLELS: sky body Dec on a natal Dec (parallel / contraparallel) and sky RA on a natal RA, within 0.1 deg somewhere in the window.
Numbers: kφ, φ^n and 10φ^n (n 2..11), k√2, whole, ninths, within ±0.002 deg (as natnums / numcheck). Each hit: the span of time it
holds, the exact moment (closest), the value there, and the zone (before the off / in the race / after the finish)."""
import os, sys, json
os.environ['MOONWIN'] = 'wide'
OUTJ = sys.argv[4]; sys.argv = sys.argv[:4]
exec(open('/home/claude/lattice/layer1_tuned.py').read().split('# transit chords')[0])
TOL = 0.002
PHI_ = (1 + 5 ** .5) / 2; R2 = 2 ** .5
TS = np.unique(np.concatenate([np.arange(t0 - 30, t1 + 30 + 1e-9, 1 / 12), [t0, t1, t1 + 30]]))
def zone(t): return 'before the off' if t < t0 else ('in the race' if t <= t1 else 'after the finish')
def ser(b): return np.array([pos(b, t) for t in TS])
def dser(P, Q, mm):
    """distance series; P, Q arrays (n,2) or a fixed (ra, dec) / (None, dec)"""
    P = np.atleast_2d(P); Q = np.atleast_2d(Q)
    if mm == 'Dec': return np.abs(P[:, 1] - Q[:, 1])
    dra = np.abs((P[:, 0] - Q[:, 0] + 180) % 360 - 180)
    if mm == 'RA': return dra
    if mm == 'Flat': return np.hypot(dra, P[:, 1] - Q[:, 1])
    r1, d1, r2, d2 = (np.radians(x) for x in (P[:, 0], P[:, 1], Q[:, 0], Q[:, 1]))
    h = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(np.clip(h, 0, 1))))
def targets(lo, hi):
    """every number of the families between lo and hi"""
    out = []
    for k in range(max(1, int(lo / PHI_)), int(hi / PHI_) + 2): out.append((f"{k}φ", k * PHI_))
    for n in range(2, 12): out += [(f"φ^{n}", PHI_ ** n), (f"10φ^{n}", 10 * PHI_ ** n)]
    for k in range(max(1, int(lo / R2)), int(hi / R2) + 2): out.append((f"{k}√2", k * R2))
    for k in range(max(1, int(lo * 9)), int(hi * 9) + 2):
        if k % 9: out.append((f"{k}/9", k / 9))
    for k in range(max(1, int(lo)), int(hi) + 2): out.append((f"whole {k}", float(k)))
    return [(l, v) for l, v in out if lo - TOL <= v <= hi + TOL]
def hits(v):
    """spans where the series v is within TOL of a family number"""
    out = []
    if np.nanmax(v) < 0.05: return out
    for lab, x in targets(float(np.nanmin(v)), float(np.nanmax(v))):
        ok = np.abs(v - x) <= TOL
        if not ok.any(): continue
        idx = np.where(ok)[0]; segs = []; s = idx[0]; p = idx[0]
        for i in idx[1:]:
            if i != p + 1: segs.append((s, p)); s = i
            p = i
        segs.append((s, p))
        for a, b in segs:
            j = a + int(np.argmin(np.abs(v[a:b + 1] - x)))
            out.append(dict(num=lab, target=x, start=float(TS[a]), end=float(TS[b]), t=float(TS[j]), val=float(v[j]), off=float(v[j] - x),
                            zone=zone(TS[j]), at_start=bool(a == 0), at_end=bool(b == len(TS) - 1)))
    return out
SKYB = [b for b in BODIES]
S = {b: ser(b) for b in SKYB}
NATP = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] in BODIES and r['body'] != 'Moon': NATP[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
OUT = dict(race=RACE, t0=t0, t1=t1, tend=t1 + 30, n2t={}, skynum={}, par={})
# 1. natal -> transit, same body
for tab in tabs:
    L = []
    for b, p in NATP[tab].items():
        if b not in S: continue
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            v = dser(S[b], np.array([p]), mm)
            for h_ in hits(v): L.append(dict(body=b, mm=mm, **h_))
    OUT['n2t'][tab] = L
# 2. sky body -> stars
for b in SKYB:
    L = []
    for h_ in hits(np.abs(S[b][:, 1])): L.append(dict(to='Equator (own |Dec|)', mm='Dec', **h_))
    for s_ in RN:
        if s_ == 'Equator': continue
        for mm in (('Dec',) if s_ == 'CourseLat' else ('RA', 'Dec')):
            v = dser(S[b], np.array([REF[s_] if REF[s_][0] is not None else (0.0, REF[s_][1])]), mm)
            for h_ in hits(v): L.append(dict(to=s_, mm=mm, **h_))
    OUT['skynum'][b] = L
# 3. parallels: sky Dec on natal Dec (and contraparallel), sky RA on natal RA, within 0.1
for tab in tabs:
    L = []
    for nb, p in NATP[tab].items():
        for b in SKYB:
            for kind, v in (('parallel', np.abs(S[b][:, 1] - p[1])), ('contraparallel', np.abs(S[b][:, 1] + p[1])),
                            ('same RA', np.abs((S[b][:, 0] - p[0] + 180) % 360 - 180))):
                if v.min() > 0.1: continue
                j = int(np.argmin(v)); ok = np.where(v <= 0.1)[0]
                L.append(dict(natal=nb, sky=b, kind=kind, min=float(v[j]), t=float(TS[j]), zone=zone(TS[j]), start=float(TS[ok[0]]), end=float(TS[ok[-1]]),
                              at_off=float(v[int(np.argmin(np.abs(TS - t0)))]), at_finish=float(v[int(np.argmin(np.abs(TS - t1)))]),
                              natal_dec=p[1], sky_dec_off=pos(b, t0)[1], edge=bool(j in (0, len(TS) - 1))))
    OUT['par'][tab] = L
json.dump(OUT, open(OUTJ, 'w'))
print(f"rr_extra {RACE}: n2t {sum(len(v) for v in OUT['n2t'].values())}, sky numbers {sum(len(v) for v in OUT['skynum'].values())}, "
      f"parallels {sum(len(v) for v in OUT['par'].values())} -> {OUTJ}", file=sys.stderr)
