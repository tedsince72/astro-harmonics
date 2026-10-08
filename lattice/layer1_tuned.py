"""layer1_tuned.py RACE OFF DUR_S - HARMONICS FROM THE STARS, LAYER 1 redone as TRANSIT AND NATAL TUNED IN (Eddie, 6 Oct 2026).
Base = two Layer-1 points (22 stars, equator; course latitude on the transit side only) in one measure (RA, Dec, Flat, Sky).
Transit side: every transit body (Nodes, L2, L3, Sun/Mercury/Venus/Moon) + a base, stars as on race day.
  Slow bodies tested at the off; the Moon every 15 s from off-2 to the finish (topocentric, this course).
Natal side: every natal point of the chart at midday (no natal Moon, no natal stars) + a base, stars AT BIRTH.
TUNED IN = a transit chord and a natal chord on the same base. UNISON = same chord type too. SAME BODY = transit X / natal X.
Transit exact time: at the body's rate on the day (linear; Moon searched within +-6 h, Sun/Mercury/Venus +-3 d, others +-60 d)."""
import sys, datetime as _dt
src = open('/home/claude/lattice/nodes_chords.py').read()
exec(src.split('# A')[0]); exec(src.split('# runners')[1].split('for tab, (role')[0])
BODIES = ['Rahu', 'Ketu', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Transpluto', 'Eris', 'Sedna', 'Makemake', 'Haumea', 'Gonggong', 'Quaoar', 'Orcus',
          'Jupiter', 'Saturn', 'Mars', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Sun', 'Mercury', 'Venus', 'Moon']
LAYER = {**{b: 'Nodes' for b in BODIES[:2]}, **{b: 'L2' for b in BODIES[2:14]}, **{b: 'L3' for b in BODIES[14:21]}, **{b: 'L4' for b in BODIES[21:]}}
for b in BODIES:
    a, z = pos(b, t0 - 30), pos(b, t0 + 30); RATE[b] = (W(z[0] - a[0]) * 24, (z[1] - a[1]) * 24)
SPAN = {'Moon': 0.25, 'Sun': 3, 'Mercury': 3, 'Venus': 3}
def exact_t(b, a, c, mm):
    global LOCKT
    span = SPAN.get(b, 60); step = span / 1200
    P0 = pos(b, t0); best = (9, None); LOCKT = lockT(P0, REF[a], REF[c], mm)
    for dd in np.arange(-span, span + 1e-9, step):
        r = tri(moved(P0, b, dd), REF[a], REF[c], mm)
        if r and r[1] < best[0]: best = (r[1], dd)
    if best[1] is not None:
        for dd in np.arange(best[1] - 2 * step, best[1] + 2 * step, step / 40):
            r = tri(moved(P0, b, dd), REF[a], REF[c], mm)
            if r and r[1] < best[0]: best = (r[1], dd)
    LOCKT = None
    edge = best[1] is not None and abs(abs(best[1]) - span) < step
    return best[1], best[0], edge
def when(x, edge, b):
    if x is None: return ''
    if edge: return f"(exact beyond ±{SPAN.get(b, 60)} d)"
    if abs(x) < 1:
        mins = x * 1440
        if abs(mins) < 60: return f"exact {abs(mins):.1f} min {'after' if mins > 0 else 'before'} the off ({hm(t0 + mins)})"
        tt = t0 + mins; dd = int(tt // 1440); tt -= dd * 1440
        return f"exact {abs(x)*24:.1f} h {'after' if x > 0 else 'before'} the off ({(_dt.date(int(RACE[:4]),int(RACE[4:6]),int(RACE[6:8]))+_dt.timedelta(days=dd)).strftime('%-d %b')} {hm(tt)})"
    return f"exact in {x:.1f} d (applying)" if x > 0 else f"exact {-x:.1f} d ago (separating)"
PAIRS = list(itertools.combinations(RN, 2))
# transit chords
TT = collections.defaultdict(list)
MALL = {}                                  # (base key, chord type) -> the Moon's best strike of that type (d, dev, minute)
TTT = {}                                   # (base key, transit body) -> minute the transit chord is tightest (the off for slow bodies)
for b in BODIES:
    times = list((np.arange(t0 - 30, t1 + 30 + 1e-9, 0.25) if MOONWIN == 'wide' else np.arange(t0 - 2, t1 + 1e-9, 0.25))) if b == 'Moon' else [t0]
    seen = {}
    for t in times:
        P = pos(b, t)
        for a, c in PAIRS:
            for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                r = tri(P, REF[a], REF[c], mm)
                if r and r[1] <= 0.0015:
                    k = (mm, a, c)
                    if k not in seen or r[1] < seen[k][1]: seen[k] = (r[0], r[1], ctype(r[0])); TTT[(k, b)] = t
                    if b == 'Moon':
                        ty_ = ctype(r[0])
                        if (k, ty_) not in MALL or r[1] < MALL[(k, ty_)][1]: MALL[(k, ty_)] = (r[0], r[1], t)
    for k, (d, dv, typ) in seen.items(): TT[k].append((b, d, dv, typ))
print(f"transit chords: {sum(len(v) for v in TT.values())} on {len(TT)} bases", file=sys.stderr)
# natal chords
NATP = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] in BODIES and r['body'] != 'Moon':
        NATP[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
NN = {}
for tab, (role, cloth, nm) in order:
    pts = {a: NATB[tab][a] for a in RN if a in STARS and a in NATB[tab]}; pts['Equator'] = REF['Equator']
    rows = []
    for nb, NP in NATP[tab].items():
        for a, c in itertools.combinations(sorted(pts), 2):
            k0 = tuple(sorted((a, c)))
            for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                k = (mm,) + k0
                if k not in TT: continue          # only bases that carry a transit chord can tune
                r = tri(NP, pts[a], pts[c], mm)
                if r and r[1] <= 0.0015: rows.append((k, nb, r[0], r[1], ctype(r[0])))
    NN[tab] = rows
    print(f"  {nm}: {len(rows)}", file=sys.stderr)
EX = {}
def ex(b, k):
    if (b, k) not in EX: EX[(b, k)] = exact_t(b, k[1], k[2], k[0])
    return EX[(b, k)]
print('=' * 120)
print(f"{RACE}  off {OFF}  finish {hm(t1)}  - LAYER 1 REDONE: TRANSIT AND NATAL TUNED IN ON THE STAR BASES")
print('=' * 120)
print(f"transit chords on Layer-1 bases (off; Moon off-2 to finish): {sum(len(v) for v in TT.values())} on {len(TT)} bases")
print("   by body: " + ', '.join(f"{b} {n}" for b, n in collections.Counter(x[0] for v in TT.values() for x in v).most_common()))
summ = []
DUMP = []
for tab, (role, cloth, nm) in order:
    f = fin.get(cloth, ('?', '?', '0')); R = role[0].upper()
    pairs = []
    for k, nb, d, dv, typ in NN[tab]:
        for tb, td, tdv, ttyp in TT[k]:
            pairs.append((k, nb, d, dv, typ, tb, td, tdv, ttyp))
            DUMP.append(("L1", tab, k[0], k[1], k[2], nb, dv, typ, tb, tdv, ttyp, d[0], d[1], td[0], td[1],
                         TTT[(k, tb)], d[2], td[2]))
    un = [p for p in pairs if p[4] == p[8]]; sb = [p for p in pairs if p[1] == p[5]]
    tight = [p for p in pairs if max(p[3], p[7]) <= 0.0002]
    summ.append((f, role, nm, len(pairs), len(un), len(sb), len(tight)))
    print('\n' + '-' * 120)
    print(f"[{f[0]}] {role.upper():6s} {nm:24s} {f[1]:>5s}{' FAV' if f[2] == '1' else ''}   tuned pairs {len(pairs)}   UNISON {len(un)}   same body {len(sb)}   both within 0.02% {len(tight)}")
    show = sorted(pairs, key=lambda p: max(p[3], p[7]))
    for k, nb, d, dv, typ, tb, td, tdv, ttyp in show:
        flag = []
        if typ == ttyp: flag.append('UNISON')
        if nb == tb: flag.append('SAME BODY')
        if max(dv, tdv) > 0.0005 and not flag: continue
        x, xd, edge = ex(tb, k)
        mm, a, c = k
        print(f"   base {mm:4s} {a}–{c} {td[2]:.3f}   {' '.join(flag)}")
        print(f"      natal   {R}.{nb:10s} {typ:14s} {d[0]:8.3f} | {d[1]:8.3f}   dev {dv*100:.3f}%")
        print(f"      transit {tb:12s} {LAYER[tb]:5s} {ttyp:14s} {td[0]:8.3f} | {td[1]:8.3f}   dev {tdv*100:.3f}%   {when(x, edge, tb)}")
    print(f"   (listed: pairs with both sides within 0.05%, plus every UNISON and SAME BODY)")
print('\n' + '=' * 120)
print("SUMMARY  finish  chart  SP  tuned pairs / UNISON / same body / both within 0.02%")
for f, role, nm, n, u, s_, t in summ: print(f"   [{f[0]}] {role:6s} {nm:24s} {f[1]:>5s}   {n:4d} {u:4d} {s_:4d} {t:4d}")
import csv as _csv
with open(f"/home/claude/lattice/dump/{RACE}_L1.csv", "w", newline="") as _f:
    # extra columns (8 Oct): natal body–x | –e, transit body–x | –e, minute held (Moon) or the off (slow), natal base, transit base, exact time
    _w = _csv.writer(_f); _w.writerow(["layer", "tab", "mm", "x", "e", "natal_body", "natal_dev", "natal_type", "transit_body", "transit_dev", "transit_type",
                                       "natal_dx", "natal_de", "transit_dx", "transit_de", "transit_t", "natal_base", "transit_base", "transit_when"])
    for r in DUMP:
        tb, k = r[8], (r[2], r[3], r[4])
        if tb == 'Moon': continue                      # the Moon is written below, every strike
        _w.writerow(list(r) + [when(*ex(tb, k)[:1], ex(tb, k)[2], tb)])
    MIDX = collections.defaultdict(list)
    for (k, ty_), v in MALL.items(): MIDX[k].append((ty_, v))
    for tab, (role, cloth, nm) in order:
        for k, nb, d, dv, typ in NN[tab]:
            for ty_, (td, tdv, tt) in sorted(MIDX.get(k, []), key=lambda x: x[1][2]):
                _w.writerow(["L1", tab, k[0], k[1], k[2], nb, dv, typ, 'Moon', tdv, ty_, d[0], d[1], td[0], td[1], tt, d[2], td[2],
                             f"Moon held at {hm(tt)} ({tt - t0:+.2f})"])
