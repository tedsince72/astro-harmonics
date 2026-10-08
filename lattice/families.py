"""families.py - harmonic families of the 22 fixed stars (Eddie, 5 Oct 2026). Stars as on 6 Apr 2022.
Standing chord = three stars whose three distances (RA, Dec, Flat Dist or Sky Dist) are all in interval ratios (0.15%).
Chord types named by their proportion (a:b:c of the three distances, smallest = 1 unit) using the full interval list.
Family = the stars linked by chords of one type."""
import csv, itertools, collections, sys, math
import numpy as np
sys.path.insert(0, '/home/claude/ledger')
from readrace import STARS, SKYD, PHI
S = {}
for r in csv.DictReader(open(f'{SKYD}/20220406_catterick_1440__SKYM.csv')):
    if r['minute'] == '0' and r['body'] in STARS: S[r['body']] = (float(r['ra']), float(r['dec']))
N = sorted(S)
IV = {'1': 1, '2': 2, '3/2': 1.5, '4/3': 4 / 3, '3': 3, '4': 4, '5/4': 1.25, '6/5': 1.2, '5/3': 5 / 3, '8/5': 1.6, '5/2': 2.5, '8/3': 8 / 3, '9/4': 9 / 4,
      '√2': 2 ** .5, '1+1/√2': 1 + 2 ** -.5, '9/8': 9 / 8, '16/9': 16 / 9, '9/5': 9 / 5, '15/8': 15 / 8, '16/15': 16 / 15, '7/4': 7 / 4, '7/3': 7 / 3,
      '7/2': 7 / 2, '7/5': 7 / 5, '7/6': 7 / 6, '8/7': 8 / 7, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '11/5': 11 / 5, '11/6': 11 / 6, '11/3': 11 / 3,
      '11/8': 11 / 8, '11/4': 11 / 4, '13/5': 13 / 5, '13/8': 13 / 8, '13/4': 13 / 4, 'φ': PHI, 'φ²': PHI ** 2, 'φ³': PHI ** 3, '1+√2': 1 + 2 ** .5,
      'φ√5': PHI * 5 ** .5, '2−1/φ': 2 - 1 / PHI, 'φ³+1': PHI ** 3 + 1, '2/φ': 2 / PHI}
def iv(r):
    k = min(IV, key=lambda k: abs(IV[k] - r) / IV[k]); return k, abs(IV[k] - r) / IV[k]
def W(x): return (x + 180) % 360 - 180
def dist(a, b, m):
    if m == 'RA': return abs(W(a[0] - b[0]))
    if m == 'Dec': return abs(a[1] - b[1])
    if m == 'Flat': return math.hypot(W(a[0] - b[0]), a[1] - b[1])
    r1, d1, r2, d2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin((r2 - r1) / 2) ** 2
    return math.degrees(2 * math.asin(math.sqrt(min(1, max(0, h)))))
INT = {'1': (1, 1), '2': (1, 2), '3/2': (2, 3), '4/3': (3, 4), '3': (1, 3), '4': (1, 4), '5/4': (4, 5), '6/5': (5, 6), '5/3': (3, 5), '8/5': (5, 8), '5/2': (2, 5),
       '8/3': (3, 8), '9/4': (4, 9), '7/4': (4, 7), '7/3': (3, 7), '7/2': (2, 7), '7/5': (5, 7), '7/6': (6, 7), '8/7': (7, 8), '5': (1, 5), '6': (1, 6), '7': (1, 7),
       '8': (1, 8), '9': (1, 9), '11/5': (5, 11), '11/6': (6, 11), '11/3': (3, 11), '11/8': (8, 11), '11/4': (4, 11), '13/5': (5, 13), '13/8': (8, 13), '13/4': (4, 13),
       '9/8': (8, 9), '16/9': (9, 16), '9/5': (5, 9), '15/8': (8, 15), '16/15': (15, 16)}
def ctype(d):
    a, b, c = sorted(d)
    k1, _ = iv(b / a); k2, _ = iv(c / a)
    if k1 in INT and k2 in INT:
        p1, q1 = INT[k1]; p2, q2 = INT[k2]
        L = p1 * p2 // math.gcd(p1, p2)
        x = [L, L * q1 // p1, L * q2 // p2]; g = math.gcd(math.gcd(x[0], x[1]), x[2]); x = [v // g for v in x]
        return ':'.join(map(str, x))
    names = {k1, k2, iv(c / b)[0]}
    if names & {'√2', '1+1/√2', '1+√2'} and '√2' in names | {iv(c / b)[0]}: return '1:√2:1+√2' if '1+√2' in names else '1:1:√2' if k1 == '1' else '1:√2:2'
    if names & {'φ', 'φ²', 'φ³', 'φ√5', '2−1/φ', 'φ³+1', '2/φ'}: return 'φ: ' + '/'.join(sorted(names))
    return 'other: ' + '/'.join(sorted(names))
CH = []
for a, b, c in itertools.combinations(N, 3):
    for m in ('RA', 'Dec', 'Flat', 'Sky'):
        d = [dist(S[a], S[b], m), dist(S[a], S[c], m), dist(S[b], S[c], m)]
        if min(d) < 0.05: continue
        rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
        dv = max(iv(x)[1] for x in rs)
        if dv <= 0.0015: CH.append((ctype(d), m, (a, b, c), d, dv))
print(f"STANDING CHORDS AMONG THE 22 STARS: {len(CH)}  (RA {sum(1 for x in CH if x[1]=='RA')}, Dec {sum(1 for x in CH if x[1]=='Dec')}, Flat {sum(1 for x in CH if x[1]=='Flat')}, Sky {sum(1 for x in CH if x[1]=='Sky')})")
byt = collections.defaultdict(list)
for x in CH: byt[x[0]].append(x)
print("\nFAMILIES (chord type -> the stars it links)")
for t, L in sorted(byt.items(), key=lambda kv: -len(kv[1])):
    deg = collections.Counter(s for x in L for s in x[2])
    print(f"\n  {t}   {len(L)} chords   stars: " + ', '.join(f"{s} {n}" for s, n in deg.most_common()))
    for typ, m, tri, d, dv in sorted(L, key=lambda x: x[4]):
        print(f"      {m:4s} {tri[0]}–{tri[1]} {d[0]:.3f} | {tri[0]}–{tri[2]} {d[1]:.3f} | {tri[1]}–{tri[2]} {d[2]:.3f}   dev {dv*100:.3f}%")
print("\nSTARS - how many standing chords each is in, by measure, and its families")
for s in sorted(N, key=lambda s: -sum(1 for x in CH if s in x[2])):
    L = [x for x in CH if s in x[2]]
    print(f"  {s:13s} {len(L):3d}  " + ' '.join(f"{m} {sum(1 for x in L if x[1]==m)}" for m in ('RA', 'Dec', 'Flat', 'Sky')) + "   " +
          ', '.join(f"{t} {n}" for t, n in collections.Counter(x[0] for x in L).most_common(6)))
# pair strength: star pairs that are the base of many chords
pc = collections.Counter()
for x in CH:
    for p in itertools.combinations(sorted(x[2]), 2): pc[(p, x[1])] += 1
print("\nSTAR PAIRS IN THE MOST STANDING CHORDS (pair, measure)")
for (p, m), n in pc.most_common(20): print(f"  {p[0]}–{p[1]} {m}: {n}")
