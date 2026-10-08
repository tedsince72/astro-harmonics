"""natchords RACE OFF DUR TAB BODY: Method 1, one natal body at a time. The body's chords in its own chart at birth
(midday): (a) with the stars at birth (+ Equator in Dec), (b) with two other natal bodies (no Moon, no stars).
Each chord: measure, base, distances, type, deviation at midday, and the deviation at 00:00 and 24:00 (birth-day range)."""
import sys, csv, itertools
TAB, BODY = sys.argv[4], sys.argv[5]; HOUR = float(sys.argv[6]) if len(sys.argv) > 6 else 12.0; sys.argv = sys.argv[:4]
src = open('/home/claude/lattice/layer1_tuned.py').read(); exec(src.split('# transit chords')[0])
H = {}
for r in csv.DictReader(open(f'/home/claude/ledger/allpos/{sys.argv[1]}__NATAL_HOURLY.csv')):
    if r['tab'] == TAB and r['ra']: H.setdefault(int(r['hour']), {})[r['body']] = (float(r['ra']), float(r['dec']))
NAME = [r['name'] for r in csv.DictReader(open(f'/home/claude/ledger/allpos/{sys.argv[1]}__NATAL_HOURLY.csv')) if r['tab'] == TAB][0]
def at(h):
    if h == int(h): return H[int(h)]
    a, b = int(h), int(h) + 1; f = h - a; out = {}
    for k in H[a]:
        if k in H[b]:
            r0, r1 = H[a][k][0], H[b][k][0]
            if r1 - r0 > 180: r1 -= 360
            if r0 - r1 > 180: r1 += 360
            out[k] = ((r0 + f * (r1 - r0)) % 360, H[a][k][1] + f * (H[b][k][1] - H[a][k][1]))
    return out
def pts(h):
    d = at(h); st = {}; bo = {}
    for b, p in d.items():
        if b.endswith('_B'): st[b[:-2]] = p
        elif b in ('equator', 'Moon') or b in ('Aldebaran', 'Antares', 'Regulus', 'Fomalhaut'): continue
        else: bo[b] = p
    st['Equator'] = (None, 0.0)
    return st, bo
st12, bo12 = pts(HOUR); st0, bo0 = pts(0); st24, bo24 = pts(24)
X = BODY
def dev(st, bo, a, c, mm, kind, T):
    global LOCKT
    A = st[a] if kind == 'star' else bo[a]; C = st[c] if kind == 'star' else bo[c]
    LOCKT = T; r = tri(bo[X], A, C, mm); LOCKT = None
    return r[1] if r else None
out = []
for kind, names in (('star', sorted(st12)), ('body', sorted(b for b in bo12 if b != X))):
    S12 = st12 if kind == 'star' else bo12
    for a, c in itertools.combinations(names, 2):
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            r = tri(bo12[X], S12[a], S12[c], mm)
            if r and r[1] <= 0.0015:
                d = [dist(S12[a], S12[c], mm), dist(bo12[X], S12[a], mm), dist(bo12[X], S12[c], mm)]
                T = lockT(bo12[X], S12[a], S12[c], mm)
                d0 = dev(st0, bo0, a, c, mm, kind, T); d24 = dev(st24, bo24, a, c, mm, kind, T)
                out.append((kind, mm, r[1], a, c, d, ctype(r[0]), d0, d24))
print(f"{NAME} — natal {X} at {HOUR:g}h: RA {bo12[X][0]:.3f} Dec {bo12[X][1]:.3f}   (00:00 RA {bo0[X][0]:.3f} Dec {bo0[X][1]:.3f}; 24:00 RA {bo24[X][0]:.3f} Dec {bo24[X][1]:.3f})")
f = lambda v: '  -  ' if v is None else f"{v*100:.3f}%"
for kind, title in (('star', 'WITH THE STARS (at birth)'), ('body', 'WITH TWO OTHER NATAL BODIES')):
    L = sorted([o for o in out if o[0] == kind], key=lambda o: o[2])
    print(f"\n{title}: {len(L)} chords")
    for k, mm, dv, a, c, d, t, d0, d24 in L:
        print(f"  {mm:4s} {a}–{c:13s} base {d[0]:8.3f} | to {a} {d[1]:8.3f} | to {c} {d[2]:8.3f}  {t:14s} {dv*100:.3f}%   [00:00 {f(d0)}  24:00 {f(d24)}]")
