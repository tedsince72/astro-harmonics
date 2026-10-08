"""race_read.py RACE OFF DUR_S - one race in detail against the star lattice (Eddie, 5 Oct 2026)."""
import sys, csv, itertools, collections, math
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])   # S (stars), N, IV, iv, dist, W, ctype
sys.path.insert(0, '/home/claude/ledger')
from readrace import SKYD, FAST
RACE, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
POSD = '/home/claude/ledger/allpos'
h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
sched = int(RACE[-4:-2]) * 60 + int(RACE[-2:])
M = {}
for r in csv.DictReader(open(f"{SKYD}/{RACE}__SKYM.csv")):
    M.setdefault(r['body'], {})[sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
S = {b: M[b][sched] for b in M if b in STARS}; N = sorted(S)
def pos(b, t):
    ks = sorted(M[b]); ra = np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))); de = [M[b][k][1] for k in ks]
    return (float(np.interp(t, ks, ra)) % 360, float(np.interp(t, ks, de)))
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
def chords_of(X, refs):
    out = []
    for a, b in itertools.combinations(sorted(refs), 2):
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            d = [dist(X, refs[a], mm), dist(X, refs[b], mm), dist(refs[a], refs[b], mm)]
            if min(d) < 0.05: continue
            rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
            dv = max(iv(x)[1] for x in rs)
            if dv <= 0.0015: out.append((mm, a, b, d, ctype(d), dv))
    return out
BODIES = ['Rahu', 'Ketu', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Transpluto', 'Eris', 'Sedna', 'Makemake', 'Haumea', 'Gonggong', 'Quaoar', 'Orcus',
          'Jupiter', 'Saturn', 'Mars', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Sun', 'Mercury', 'Venus', 'Moon']
print('=' * 110); print(f"{RACE}  off {OFF}  finish {hm(t1)}  - against the star lattice"); print('=' * 110)
# 1 load timeline
print("\n1  STAR-CHORD LOAD OF EACH BODY, off-10 to finish+1 (own minute file), every 30 s - peak marked *")
ts = np.arange(t0 - 10, t1 + 1.001, 0.5)
print("   " + ' ' * 11 + ''.join(f"{(t - t0):+6.1f}" for t in ts))
TL = {}
for b in [x for x in BODIES if x in M]:
    row = [len(chords_of(pos(b, t), S)) for t in ts]; TL[b] = row
    if max(row) == min(row): continue
    k = int(np.argmax(row))
    print(f"   {b:10s} " + ''.join(f"{v:5d}{'*' if i == k else ' '}" for i, v in enumerate(row)))
print("   (bodies with a constant load not shown: " + ', '.join(f"{b} {TL[b][0]}" for b in TL if max(TL[b]) == min(TL[b])) + ")")
# 2 key bodies at the off
for b in ('Mercury', 'Moon', 'Mars', 'Saturn', 'Juno', 'Sun', 'Venus'):
    X = pos(b, t0); ch = chords_of(X, S)
    print(f"\n2  {b.upper()} AT THE OFF  RA {X[0]:.3f} Dec {X[1]:+.3f}  - {len(ch)} star chords")
    for mm, a, c, d, typ, dv in sorted(ch, key=lambda x: (x[0], x[4])):
        print(f"     {mm:4s} {typ:12s} {b}–{a} {d[0]:.3f} | {b}–{c} {d[1]:.3f} | {a}–{c} {d[2]:.3f}   dev {dv*100:.3f}%")
# 3 runners
META = list(csv.reader(open(f"{POSD}/{RACE}__META.csv")))
tabs = {r[0]: (r[1], r[2], r[3]) for r in META if r and r[0].startswith('P') and r[0][1:].isdigit()}
NAT = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] not in STARS and not r['body'].endswith('_B') and r['body'] not in ('Moon', 'equator') and r['body'] not in FAST:
        NAT[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
fin = {}
for p in ('/home/claude/pinpoint_blind_kit/reference/profiles.csv', '/home/claude/scored/profiles_test_scored.csv'):
    for r in csv.DictReader(open(p)):
        if r['race'] == RACE: fin[r['cloth']] = (r['finish'], r['sp'], r['fav'])
print("\n3  THE RUNNERS - each natal point in a chord with the lit/key bodies at the off and a star (body–natal–star triangle, all three in interval ratios)")
for tab, (role, cloth, nm) in sorted(tabs.items(), key=lambda x: (int(fin.get(x[1][1], ('99',))[0] or 99), x[1][0] != 'horse')):
    f = fin.get(cloth, ('?', '?', '0'))
    rows = []
    for b in ('Mercury', 'Moon', 'Mars', 'Saturn', 'Juno', 'Sun', 'Venus'):
        X = pos(b, t0)
        for nb, NP in NAT[tab].items():
            for c in N:
                for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                    d = [dist(X, NP, mm), dist(X, S[c], mm), dist(NP, S[c], mm)]
                    if min(d) < 0.05: continue
                    rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
                    dv = max(iv(x)[1] for x in rs)
                    if dv <= 0.0015: rows.append((b, nb, c, mm, d, ctype(d), dv))
    print(f"   [{f[0]}] {role:6s} {nm:28s} {f[1]:>6s}{' FAV' if f[2]=='1' else ''}   {len(rows)} chords   " +
          ', '.join(f"{b} {n}" for b, n in collections.Counter(r[0] for r in rows).most_common()))
    for b, nb, c, mm, d, typ, dv in sorted(rows, key=lambda r: r[6])[:12]:
        print(f"        {b:8s} {mm:4s} {typ:12s} {b}–{role[0].upper()}.{nb} {d[0]:.3f} | {b}–{c} {d[1]:.3f} | {role[0].upper()}.{nb}–{c} {d[2]:.3f}  dev {dv*100:.3f}%")
