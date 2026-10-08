"""nodes_chords.py RACE OFF DUR_S - HARMONICS FROM THE STARS, the NODES layer, one race (Eddie, 6 Oct 2026).
Points in play: Layer 1 (22 stars as on race day; equator and course latitude as Dec-only points) + the Nodes.
Chord = three points, three distances in the same measure (RA, Dec, Flat, Sky), all three ratios in the interval list (0.15%).
Rahu–Ketu as a pair: RA skipped (always 180), Sky skipped (always 180); equator skipped with a Rahu–Ketu pair (always the midpoint).
Nodes move ~0.05 deg/day, so their chords stand all afternoon: timing is given in DAYS to/from exact at the node's rate on the day.
Order: A transit nodes with star pairs; B transit Rahu+Ketu with one point; then each runner, horse then jockey:
C natal node + transit node + star; D natal node with star pairs (stars on race day, and whether it stood with the stars at birth);
E natal Rahu + natal Ketu + one point."""
import sys, datetime as _dt, csv, itertools, collections, math
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("CH = []")[0])   # STARS, IV, iv, dist, W, ctype
RACE, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3])
POSD = '/home/claude/ledger/allpos'
h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
sched = int(RACE[-4:-2]) * 60 + int(RACE[-2:])
M = {}
import os as _os
MOONWIN = _os.environ.get("MOONWIN", "")   # "wide": the Moon from off-30 to finish+30 (Eddie 8 Oct), using the 1-minute grid
_SKYF = f"/home/claude/ledger/skygrid/{RACE}__GRID.csv" if MOONWIN == "wide" else f"{SKYD}/{RACE}__SKYM.csv"
for r in csv.DictReader(open(_SKYF)):
    M.setdefault(r['body'], {})[sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
_PC = {}
def pos(b, t):
    if b not in _PC:
        ks = sorted(M[b]); _PC[b] = (ks, np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks]))), [M[b][k][1] for k in ks])
    ks, ra, de = _PC[b]
    return (float(np.interp(t, ks, ra)) % 360, float(np.interp(t, ks, de)))
META = list(csv.reader(open(f"{POSD}/{RACE}__META.csv")))
LAT = float([r for r in META if r and r[0] == 'racecourse_lat_lon_elev'][0][1].split(',')[0])
REF = {b: pos(b, t0) for b in M if b in STARS}
DECONLY = {'Equator': (None, 0.0), 'CourseLat': (None, LAT)}
REF.update(DECONLY)
RN = sorted(REF)
TN = {b: pos(b, t0) for b in ('Rahu', 'Ketu')}
RATE = {}
for b in TN:   # deg/day from the minute file (off-30 to off+30)
    a, z = pos(b, t0 - 30), pos(b, t0 + 30); RATE[b] = (W(z[0] - a[0]) * 24, (z[1] - a[1]) * 24)
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
def ok_meas(p, q, mm):
    return not ((p[0] is None or q[0] is None) and mm != 'Dec')
def tri(A, B, C, mm):
    if not (ok_meas(A, B, mm) and ok_meas(A, C, mm) and ok_meas(B, C, mm)): return None
    d = [dist(A, B, mm), dist(A, C, mm), dist(B, C, mm)]
    if min(d) < 0.05: return None
    rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
    if LOCKT: return d, max(abs(x - t) / t for x, t in zip(rs, LOCKT))
    return d, max(iv(x)[1] for x in rs)
LOCKT = None
def lockT(A, B, C, mm):
    """the three interval values of the chord as it stands now - exact-time searches follow THIS chord, not another type"""
    d = [dist(A, B, mm), dist(A, C, mm), dist(B, C, mm)]
    rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
    return [IV[iv(x)[0]] for x in rs]
def moved(p, b, days):
    if p[0] is None: return p
    return ((p[0] + RATE[b][0] * days) % 360, p[1] + RATE[b][1] * days)
DAYS = np.arange(-60, 60.001, 0.05)
def exact_days(build, T=None):
    """build(days) -> (d, dev) or None; returns days of best dev within +-60 d (node moving at today's rate).
    T = the chord's own interval values (lockT) so the search follows the same chord."""
    global LOCKT
    LOCKT = T; best = (9, None)
    for dd in DAYS:
        r = build(dd)
        if r and r[1] < best[0]: best = (r[1], dd)
    if best[1] is not None:
        for dd in np.arange(best[1] - 0.06, best[1] + 0.06, 0.0007):
            r = build(dd)
            if r and r[1] < best[0]: best = (r[1], dd)
    LOCKT = None
    return best
def fmt_days(x):
    if x is None: return ''
    if abs(x) < 1:
        tt = t0 + x * 1440; dd = int(tt // 1440); tt -= dd * 1440
        return f"exact {abs(x)*24:.1f} h {'after' if x > 0 else 'before'} the off ({(_dt.date(int(RACE[:4]),int(RACE[4:6]),int(RACE[6:8]))+_dt.timedelta(days=dd)).strftime('%-d %b')} {hm(tt)})"
    return f"exact in {x:.1f} d (applying)" if x > 0 else f"exact {-x:.1f} d ago (separating)"
def pair_ok(a, b, mm):   # Rahu–Ketu pairing rules
    names = {a.split('.')[-1], b.split('.')[-1]}
    if names == {'Rahu', 'Ketu'} and mm in ('RA', 'Sky'): return False
    return True
print('=' * 112)
print(f"{RACE}  off {OFF}  finish {hm(t1)}  - NODES LAYER chords (Layer 1 + Nodes)   course latitude {LAT:.4f}")
print('=' * 112)
for b in TN: print(f"   transit {b:5s} RA {TN[b][0]:8.3f} Dec {TN[b][1]:+7.3f}   moving RA {RATE[b][0]:+.4f}/d Dec {RATE[b][1]:+.4f}/d")
# A
print("\nA  TRANSIT NODE + TWO LAYER-1 POINTS  (at the off; days to exact at today's rate)")
for b in TN:
    rows = []
    for a, c in itertools.combinations(RN, 2):
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            if 'Equator' in (a, c) and 'CourseLat' in (a, c): pass
            r = tri(TN[b], REF[a], REF[c], mm)
            if r and r[1] <= 0.0015:
                ex = exact_days(lambda dd: tri(moved(TN[b], b, dd), REF[a], REF[c], mm), lockT(TN[b], REF[a], REF[c], mm))
                rows.append((mm, a, c, r[0], ctype(r[0]), r[1], ex[1]))
    print(f"   {b}: {len(rows)} chords")
    for mm, a, c, d, typ, dv, ex in sorted(rows, key=lambda x: abs(x[6] or 99)):
        print(f"     {mm:4s} {typ:14s} {b}–{a} {d[0]:.3f} | {b}–{c} {d[1]:.3f} | {a}–{c} {d[2]:.3f}  dev {dv*100:.3f}%  {fmt_days(ex)}")
# B
print("\nB  TRANSIT RAHU + TRANSIT KETU + ONE LAYER-1 POINT  (Dec and Flat only; equator skipped)")
for a in RN:
    if a == 'Equator': continue
    for mm in ('Dec', 'Flat'):
        r = tri(TN['Rahu'], TN['Ketu'], REF[a], mm)
        if r and r[1] <= 0.0015:
            ex = exact_days(lambda dd: tri(moved(TN['Rahu'], 'Rahu', dd), moved(TN['Ketu'], 'Ketu', dd), REF[a], mm), lockT(TN['Rahu'], TN['Ketu'], REF[a], mm))
            print(f"     {mm:4s} {ctype(r[0]):14s} Rahu–Ketu {r[0][0]:.3f} | Rahu–{a} {r[0][1]:.3f} | Ketu–{a} {r[0][2]:.3f}  dev {r[1]*100:.3f}%  {fmt_days(ex[1])}")
# runners
tabs = {r[0]: (r[1], r[2], r[3]) for r in META if r and r[0].startswith('P') and r[0][1:].isdigit()}
NAT = collections.defaultdict(dict); NATB = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] != '12' or not r['ra']: continue
    if r['body'] in ('Rahu', 'Ketu'): NAT[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
    if r['body'].endswith('_B'): NATB[r['tab']][r['body'][:-2]] = (float(r['ra']), float(r['dec']))
fin = {}
for p in ('/home/claude/pinpoint_blind_kit/reference/profiles.csv', '/home/claude/scored/profiles_test_scored.csv'):
    for r in csv.DictReader(open(p)):
        if r['race'] == RACE: fin[r['cloth']] = (r['finish'], r['sp'], r['fav'])
def _fp(v):
    v = (v or '').strip()
    return int(v) if v.isdigit() else 90
order = sorted(tabs.items(), key=lambda x: (_fp(fin.get(x[1][1], ('99',))[0]), x[1][0] != 'horse'))
for tab, (role, cloth, nm) in order:
    f = fin.get(cloth, ('?', '?', '0')); R = role[0].upper()
    print('\n' + '-' * 112)
    print(f"[{f[0]}] {role.upper()} {nm}  {f[1]}{' FAV' if f[2] == '1' else ''}   natal " +
          '  '.join(f"{b} RA {NAT[tab][b][0]:.3f} Dec {NAT[tab][b][1]:+.3f}" for b in ('Rahu', 'Ketu')))
    print(f"   C  natal node + transit node + Layer-1 point")
    rows = []
    for nb in ('Rahu', 'Ketu'):
        for tb in ('Rahu', 'Ketu'):
            NP, TP = NAT[tab][nb], TN[tb]
            for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                dd = [dist(TP, NP, mm)]
            for a in RN:
                for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                    r = tri(TP, NP, REF[a], mm)
                    if r and r[1] <= 0.0015:
                        ex = exact_days(lambda dd: tri(moved(TP, tb, dd), NP, REF[a], mm), lockT(TP, NP, REF[a], mm))
                        rows.append((tb, nb, a, mm, r[0], ctype(r[0]), r[1], ex[1]))
    for tb, nb, a, mm, d, typ, dv, ex in sorted(rows, key=lambda x: abs(x[7] if x[7] is not None else 99)):
        print(f"     {mm:4s} {typ:14s} {tb}–{R}.{nb} {d[0]:.3f} | {tb}–{a} {d[1]:.3f} | {R}.{nb}–{a} {d[2]:.3f}  dev {dv*100:.3f}%  {fmt_days(ex)}")
    if not rows: print("     none")
    print(f"   D  natal node + two Layer-1 points (stars on race day; 'B' = also stood with the stars at birth)")
    rows = []
    for nb in ('Rahu', 'Ketu'):
        NP = NAT[tab][nb]
        for a, c in itertools.combinations(RN, 2):
            for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                r = tri(NP, REF[a], REF[c], mm)
                if r and r[1] <= 0.0015:
                    A_ = NATB[tab].get(a, REF[a]) if a in STARS else REF[a]; C_ = NATB[tab].get(c, REF[c]) if c in STARS else REF[c]
                    rb = tri(NP, A_, C_, mm)
                    rows.append((nb, a, c, mm, r[0], ctype(r[0]), r[1], rb[1] if rb else None))
    for nb, a, c, mm, d, typ, dv, dvb in sorted(rows, key=lambda x: x[6]):
        bt = (f"B {dvb*100:.3f}%" if dvb is not None and dvb <= 0.0015 else f"not at birth ({dvb*100:.2f}%)" if dvb is not None else '')
        print(f"     {mm:4s} {typ:14s} {R}.{nb}–{a} {d[0]:.3f} | {R}.{nb}–{c} {d[1]:.3f} | {a}–{c} {d[2]:.3f}  dev {dv*100:.3f}%  {bt}")
    if not rows: print("     none")
    print(f"   E  natal Rahu + natal Ketu + one Layer-1 point (Dec and Flat; equator skipped)")
    n = 0
    for a in RN:
        if a == 'Equator': continue
        for mm in ('Dec', 'Flat'):
            r = tri(NAT[tab]['Rahu'], NAT[tab]['Ketu'], REF[a], mm)
            if r and r[1] <= 0.0015:
                n += 1; print(f"     {mm:4s} {ctype(r[0]):14s} {R}.Rahu–{R}.Ketu {r[0][0]:.3f} | {R}.Rahu–{a} {r[0][1]:.3f} | {R}.Ketu–{a} {r[0][2]:.3f}  dev {r[1]*100:.3f}%")
    if not n: print("     none")
