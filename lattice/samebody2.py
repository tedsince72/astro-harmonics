"""samebody2.py RACE OFF DUR_S [WINNER_HORSE_TAB WINNER_JOCKEY_TAB]
Same-body chords v2 (Eddie, 8 Oct 08:12-08:13: "some will be exact or slow etc after the race but still valid").
Changes from samebody.py:
 - window = off-30 min to finish+30 min, every 15 s (plus the exact off and finish), from the 1-minute engine grid (skygrid.py)
 - each chord shown at off-30 / off / finish / finish+30, with its movement through the race (applying, exact in race, separating)
 - a chord tightest at a window edge is followed outward through the +-12 h grid to its own exact moment
PART 1 - sky X + horse natal X + jockey natal X.   PART 2 - natal X - sky X + a third point (sky body or race-day star; Equator in Dec).
Natal at 12:00 (midday rule); natal Moon left out. Chord: three distances, all three ratios in the interval list within 0.15%;
shortest side >= 0.05 deg. A chord is listed if it is within 0.15% somewhere in the window."""
import sys, csv, collections
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])   # STARS, IV, iv, dist, ctype
RACE, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
POSD = '/home/claude/ledger/allpos'; GRID = f'/home/claude/ledger/skygrid/{RACE}__GRID.csv'
h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
sched = int(RACE[-4:-2]) * 60 + int(RACE[-2:])
M = {}
for r in csv.DictReader(open(GRID)):
    M.setdefault(r['body'], {})[sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
FAST = {'Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit'}
SKYB = [b for b in M if b not in STARS and b not in FAST]
KS = np.array(sorted(M['Sun']), dtype=float)
TS = np.unique(np.concatenate([np.arange(t0 - 30, t1 + 30 + 1e-9, 0.25), [t0, t1, t1 + 30]]))
I_A, I_OFF, I_FIN, I_B = 0, int(np.argmin(abs(TS - t0))), int(np.argmin(abs(TS - t1))), int(np.argmin(abs(TS - (t1 + 30))))
def series(b, ts):
    ra = np.degrees(np.unwrap(np.radians([M[b][k][0] for k in KS]))); de = np.array([M[b][k][1] for k in KS])
    return np.interp(ts, KS, ra) % 360, np.interp(ts, KS, de)
SER = {b: series(b, TS) for b in SKYB}          # the window, every 15 s
GSER = {b: series(b, KS) for b in SKYB}         # the +-12 h grid, every minute
STAR = {b: tuple(float(x) for x in (series(b, np.array([t0]))[0][0], series(b, np.array([t0]))[1][0])) for b in M if b in STARS}
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
def hm(t):
    x = int(round(t * 60)); day = x // 86400; x %= 86400
    return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}" + (f" (day {day:+d})" if day else "")
def fmt(dv): return '  –   ' if dv is None else f"{dv*100:.3f}%"
def evaluate(mk):
    """mk(src, i) -> point maker; returns dict with window min, the four check points and, for an edge minimum, the outward exact moment"""
    best = (9, None, None); devs = [None] * len(TS)
    for i in range(len(TS)):
        r = mk('w', i)
        if r is None: continue
        devs[i] = r[1]
        if r[1] < best[0]: best = (r[1], i, r[0])
    if best[1] is None or best[0] > 0.0015: return None
    out = dict(dv=best[0], t=TS[best[1]], d=best[2], at=[devs[I_A], devs[I_OFF], devs[I_FIN], devs[I_B]], edge=None)
    if best[1] in (0, len(TS) - 1):                    # follow it outward through the 1-minute grid
        step = -1 if best[1] == 0 else 1
        j = int(np.searchsorted(KS, TS[best[1]])) - (1 if step < 0 else 0); prev = 9; bj = None; bd = None
        while 0 <= j < len(KS):
            r = mk('g', j)
            if r is None: break
            if r[1] > prev: break
            prev, bj, bd = r[1], j, r[0]; j += step
        if bj is not None:
            out['edge'] = (prev, KS[bj], bd, bj in (0, len(KS) - 1))
    return out
def movement(o):
    a, off, fin, b = o['at']
    if o['edge']: return 'still applying at off+30' if o['t'] > t1 else 'separating since before off-30'
    if t0 <= o['t'] <= t1: return 'exact IN THE RACE'
    if o['t'] > t1: return f"applying through the race, exact {o['t'] - t1:.1f} min after the finish"
    return f"exact {t0 - o['t']:.1f} min before the off, separating through the race"
def where(o):
    if o['edge']:
        dv, t, d, lim = o['edge']
        return f"followed out: {'still closing at the ±12 h limit, ' if lim else ''}tightest {dv*100:.3f}% at {hm(t)}", d
    return f"tightest {o['dv']*100:.3f}% at {hm(o['t'])}", o['d']
def line(o):
    w, d = where(o)
    a, off, fin, b = o['at']
    return (f"{w}  — {movement(o)}\n        at off−30 {fmt(a)} | off {fmt(off)} | finish {fmt(fin)} | finish+30 {fmt(b)}", d)
def P(b, src, i): return (SER[b][0][i], SER[b][1][i]) if src == 'w' else (GSER[b][0][i], GSER[b][1][i])
horses = [p for p, (role, nm) in tabs.items() if role == 'horse']; jockeys = [p for p, (role, nm) in tabs.items() if role == 'jockey']
pair = {hh: 'P%02d' % (int(hh[1:]) + 1) for hh in horses}
WH, WJ = (sys.argv[4], sys.argv[5]) if len(sys.argv) > 5 else (None, None)
print('=' * 110); print(f"{RACE}  off {OFF}  finish {hm(t1)}  - SAME-BODY CHORDS v2 (window {hm(TS[0])} to {hm(TS[-1])}; edges followed out to ±12 h)"); print('=' * 110)
print("\nPART 1 - sky X + horse natal X + jockey natal X (≤0.15% somewhere in the window)")
def part1(hh, jj, show):
    hits = []
    for b in SKYB:
        if b == 'Moon' or b not in NAT[hh] or b not in NAT[jj]: continue
        for mm in MEAS:
            o = evaluate(lambda src, i, b=b, mm=mm: chord(P(b, src, i), NAT[hh][b], NAT[jj][b], mm))
            if o: hits.append((o['dv'], b, mm, o))
    if show:
        for dv, b, mm, o in sorted(hits, key=lambda x: x[0]):
            txt, d = line(o)
            print(f"   {b:11s} {mm:4s} {ctype(d):16s} {txt}\n        [sky–horse {d[0]:.3f} | sky–jockey {d[1]:.3f} | horse–jockey {d[2]:.3f}]")
    return hits
for hh in horses:
    jj = pair[hh]; print(f"\n -- {tabs[hh][1]} + {tabs[jj][1]}{'   <== WINNER' if hh == WH else ''}")
    hs = part1(hh, jj, True)
    print(f"    count: {len(hs)} ≤0.15%, {sum(1 for x in hs if x[0] <= 0.0005)} ≤0.05%, {sum(1 for x in hs if x[0] <= 0.0002)} ≤0.02% (window minimum)")
ctrl = [part1(hh, jj, False) for hh in horses for jj in jockeys if jj != pair[hh]]
print(f"\n CONTROL ({len(ctrl)} non-actual pairings): mean {np.mean([len(x) for x in ctrl]):.1f} ≤0.15%, "
      f"{np.mean([sum(1 for y in x if y[0] <= 0.0005) for x in ctrl]):.1f} ≤0.05%, {np.mean([sum(1 for y in x if y[0] <= 0.0002) for x in ctrl]):.1f} ≤0.02%")
print("\nPART 2 - natal X - sky X + a third point (sky body or race-day star)")
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
                if kind == 'sky': fn = lambda src, i, mm=mm, y=y: chord(N, P(b, src, i), P(y, src, i), mm)
                else:
                    Y = (None, 0.0) if y == 'Equator' else STAR[y]
                    fn = lambda src, i, mm=mm, Y=Y: chord(N, P(b, src, i), Y, mm)
                o = evaluate(fn)
                if o: out.append((o['dv'], b, y, mm, o))
    return out
P2 = {tab: part2(tab) for tab in tabs}
def zone(o):
    if o['edge']: return 'edge'
    return 'before' if o['t'] < t0 else ('race' if o['t'] <= t1 else 'after')
print("   counts per chart (window minimum): ≤0.15 / ≤0.05 / ≤0.02   |  of the ≤0.05: tightest before the off / in the race / after the finish / at an edge (slow)")
for tab in sorted(tabs):
    o = P2[tab]; z = collections.Counter(zone(x[4]) for x in o if x[0] <= 0.0005)
    print(f"   {tab} {tabs[tab][0]:6s} {tabs[tab][1]:24s} {len(o):4d} / {sum(1 for x in o if x[0] <= 0.0005):3d} / {sum(1 for x in o if x[0] <= 0.0002):3d}   |  "
          f"{z['before']:3d} / {z['race']:3d} / {z['after']:3d} / {z['edge']:3d}{'   <== WINNER' if tab in (WH, WJ) else ''}")
for tab in (WH, WJ):
    if not tab: continue
    print(f"\n -- {tabs[tab][1]}: ≤0.05% in the window, or ≤0.05% where an edge chord is followed out (tightest first)")
    rows = []
    for dv, b, y, mm, o in P2[tab]:
        true = o['edge'][0] if o['edge'] else dv
        if min(dv, true) <= 0.0005: rows.append((min(dv, true), b, y, mm, o))
    for dv, b, y, mm, o in sorted(rows, key=lambda x: x[0]):
        txt, d = line(o)
        print(f"   natal {b:10s} – sky {b:10s} + {y:12s} {mm:4s} {ctype(d):16s} {txt}\n        [natal–sky {d[0]:.3f} | natal–{y} {d[1]:.3f} | sky–{y} {d[2]:.3f}]")
