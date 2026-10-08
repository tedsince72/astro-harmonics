"""samebody.py RACE OFF DUR_S [WINNER_HORSE_TAB WINNER_JOCKEY_TAB]
Same-body chords at race time (Eddie, 8 Oct 2026).
PART 1 - one body, three positions: sky X (moving), horse natal X, jockey natal X. Chord in RA / Dec / Flat / Sky?
         Actual horse+jockey pairs, plus every other horse x jockey pairing as a control.
PART 2 - the same-body string: natal X and sky X, with a third point = another sky body or a race-day star (Equator in Dec only).
         Each chart (horse, jockey) on its own; counts for every chart so the winner can be compared with the field.
Natal at 12:00 (midday rule); natal Moon left out. Window: off-30 min to the finish, sampled every 15 s. Chord rule as in the layers
(three distances, all three ratios in the interval list, within 0.15%); shortest side >= 0.05 deg."""
import sys, csv, math, collections
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])   # STARS, IV, iv, dist, W, ctype
RACE, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
POSD = '/home/claude/ledger/allpos'
h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
sched = int(RACE[-4:-2]) * 60 + int(RACE[-2:])
M = {}
for r in csv.DictReader(open(f"{SKYD}/{RACE}__SKYM.csv")):
    M.setdefault(r['body'], {})[sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
FAST = {'Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit'}
SKYB = [b for b in M if b not in STARS and b not in FAST]
TS = np.arange(t0 - 30, t1 + 1e-9, 0.25)
def series(b):
    ks = sorted(M[b]); ra = np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))); de = np.array([M[b][k][1] for k in ks])
    return np.interp(TS, ks, ra) % 360, np.interp(TS, ks, de)
SER = {b: series(b) for b in SKYB}
STAR = {b: (float(np.interp(t0, sorted(M[b]), [M[b][k][0] for k in sorted(M[b])])), float(np.interp(t0, sorted(M[b]), [M[b][k][1] for k in sorted(M[b])]))) for b in M if b in STARS}
META = list(csv.reader(open(f"{POSD}/{RACE}__META.csv")))
tabs = {r[0]: (r[1], r[3]) for r in META if r and r[0].startswith('P') and r[0][1:].isdigit()}
NAT = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    b = r['body']
    if r['hour'] == '12' and r['ra'] and b in SKYB and b != 'Moon': NAT[r['tab']][b] = (float(r['ra']), float(r['dec']))
MEAS = ('RA', 'Dec', 'Flat', 'Sky')
def chord(A, B, C, mm):
    if (A[0] is None or B[0] is None or C[0] is None) and mm != 'Dec': return None
    d = [dist(A, B, mm), dist(A, C, mm), dist(B, C, mm)]
    if min(d) < 0.05: return None
    rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
    return d, max(iv(x)[1] for x in rs)
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
def best_over(fn):
    """fn(i) -> (d, dev) or None over the window; returns (dev_min, t_min, dev_at_off, d_at_min, edge)"""
    best = (9, None, None); i0 = int(round((t0 - TS[0]) / 0.25)); doff = None
    for i in range(len(TS)):
        r = fn(i)
        if r is None: continue
        if i == i0: doff = r[1]
        if r[1] < best[0]: best = (r[1], i, r[0])
    if best[1] is None: return None
    edge = best[1] in (0, len(TS) - 1)
    return best[0], TS[best[1]], doff, best[2], edge
def skyp(b, i): return (SER[b][0][i], SER[b][1][i])
def tlab(t, edge):
    if edge: return f"tightest at the window edge ({hm(t)})"
    if t < t0: return f"tightest {t0 - t:.1f} min before the off ({hm(t)})"
    if t <= t1: return f"tightest IN THE RACE ({hm(t)})"
    return f"tightest {t - t1:.1f} min after the finish ({hm(t)})"
horses = [p for p, (role, nm) in tabs.items() if role == 'horse']; jockeys = [p for p, (role, nm) in tabs.items() if role == 'jockey']
pair = {h: 'P%02d' % (int(h[1:]) + 1) for h in horses}
WH, WJ = (sys.argv[4], sys.argv[5]) if len(sys.argv) > 5 else (None, None)
print('=' * 110); print(f"{RACE}  off {OFF}  finish {hm(t1)}  - SAME-BODY CHORDS (window {hm(TS[0])} to {hm(TS[-1])})"); print('=' * 110)
# PART 1
print("\nPART 1 - sky X + horse natal X + jockey natal X (chords <= 0.15% somewhere in the window)")
def part1(hh, jj, show):
    hits = []
    for b in SKYB:
        if b == 'Moon' or b not in NAT[hh] or b not in NAT[jj]: continue
        for mm in MEAS:
            r = best_over(lambda i: chord(skyp(b, i), NAT[hh][b], NAT[jj][b], mm))
            if r and r[0] <= 0.0015: hits.append((r[0], b, mm, r))
    if show:
        for dv, b, mm, r in sorted(hits):
            print(f"   {b:11s} {mm:4s} {ctype(r[3]):16s} min {dv*100:.3f}%  at off {r[2]*100 if r[2] is not None else float('nan'):.3f}%  {tlab(r[1], r[4])}"
                  f"   [sky–horse {r[3][0]:.3f} | sky–jockey {r[3][1]:.3f} | horse–jockey {r[3][2]:.3f}]")
    return hits
for hh in horses:
    jj = pair[hh]; print(f"\n -- {tabs[hh][1]} + {tabs[jj][1]}{'   <== WINNER' if hh == WH else ''}")
    hs = part1(hh, jj, True)
    print(f"    count: {len(hs)} chords ≤0.15%, {sum(1 for x in hs if x[0] <= 0.0005)} ≤0.05%, {sum(1 for x in hs if x[0] <= 0.0002)} ≤0.02%")
ctrl = [part1(hh, jj, False) for hh in horses for jj in jockeys if jj != pair[hh]]
print(f"\n CONTROL (the {len(ctrl)} non-actual horse x jockey pairings): mean {np.mean([len(x) for x in ctrl]):.1f} chords ≤0.15%, "
      f"{np.mean([sum(1 for y in x if y[0] <= 0.0005) for x in ctrl]):.1f} ≤0.05%, {np.mean([sum(1 for y in x if y[0] <= 0.0002) for x in ctrl]):.1f} ≤0.02%")
# PART 2
print("\nPART 2 - the same-body string natal X - sky X, with a third point (sky body or race-day star)")
THIRD = [('sky', b) for b in SKYB] + [('star', b) for b in STAR] + [('star', 'Equator')]
def part2(tab):
    out = []
    for b in SKYB:
        if b == 'Moon' or b not in NAT[tab]: continue
        N = NAT[tab][b]
        for kind, y in THIRD:
            if kind == 'sky' and y == b: continue
            for mm in MEAS:
                if y == 'Equator' and mm != 'Dec': continue
                if kind == 'sky':
                    fn = lambda i, mm=mm, y=y: chord(N, skyp(b, i), skyp(y, i), mm)
                else:
                    Y = (None, 0.0) if y == 'Equator' else STAR[y]
                    fn = lambda i, mm=mm, Y=Y: chord(N, skyp(b, i), Y, mm)
                r = best_over(fn)
                if r and r[0] <= 0.0015: out.append((r[0], b, y, mm, r))
    return out
P2 = {tab: part2(tab) for tab in tabs}
print("   counts per chart: ≤0.15% / ≤0.05% / ≤0.02% / tightest inside the race (≤0.05%)")
for tab in sorted(tabs):
    o = P2[tab]
    print(f"   {tab} {tabs[tab][0]:6s} {tabs[tab][1]:24s} {len(o):4d} / {sum(1 for x in o if x[0] <= 0.0005):3d} / {sum(1 for x in o if x[0] <= 0.0002):3d} / "
          f"{sum(1 for x in o if x[0] <= 0.0005 and t0 <= x[4][1] <= t1 and not x[4][4]):2d}{'   <== WINNER' if tab in (WH, WJ) else ''}")
for tab in (WH, WJ):
    if not tab: continue
    print(f"\n -- {tabs[tab][1]}: same-body strings with a third point, ≤0.05% (tightest first)")
    for dv, b, y, mm, r in sorted(P2[tab]):
        if dv > 0.0005: continue
        print(f"   natal {b:10s} – sky {b:10s} + {y:12s} {mm:4s} {ctype(r[3]):16s} min {dv*100:.3f}%  {tlab(r[1], r[4])}"
              f"   [natal–sky {r[3][0]:.3f} | natal–{y} {r[3][1]:.3f} | sky–{y} {r[3][2]:.3f}]")
