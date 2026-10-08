"""layer_tuned.py RACE OFF DUR_S LAYER - a body layer as TRANSIT AND NATAL TUNED IN (Eddie, 6 Oct 2026).
LAYER = L2 | L3 | L4.  Base = a body of the layer at one end; other end = a Layer-1 point (star, equator, course latitude [transit
only]), a node, or another body of the same layer. Third point = any body. Transit: stars on race day, bodies at the off, the Moon
every 15 s off-2 to the finish. Natal: the chart's own points at midday (no Moon), stars at birth.
TUNED IN = same named base, same measure. Base lengths differ (transit X is not natal X): shown as SAME LENGTH / interval / ratio.
UNISON = same chord type. SAME BODY = same third body. Rahu–Ketu as a pair: RA, Sky skipped. Just say what we see."""
import sys
LNAME = sys.argv[4]; sys.argv = sys.argv[:4]
src = open('/home/claude/lattice/layer1_tuned.py').read()
exec(src.split('# transit chords')[0])
LB = [b for b in BODIES if LAYER[b] == LNAME]
NATP = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] in BODIES and r['body'] != 'Moon':
        NATP[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
MEAS = ('RA', 'Dec', 'Flat', 'Sky')
def rkin(*n): return 'Rahu' in n and 'Ketu' in n
def bases(lay, ends):
    out = []
    for x in lay:
        for e in list(ends) + ['Rahu', 'Ketu'] + lay:
            if e == x: continue
            if e in lay and LB.index(e) < LB.index(x): continue
            out.append((x, e))
    return out
def chords(P, ends, thirds, lay):
    """P: positions of bodies incl. nodes; ends: Layer-1 points; thirds: names of third bodies."""
    out = collections.defaultdict(list)
    for x, e in bases(lay, ends):
        if x not in P: continue
        EP = ends[e] if e in ends else P.get(e)
        if EP is None: continue
        for b in thirds:
            if b in (x, e) or b not in P: continue
            for mm in MEAS:
                if rkin(x, e, b) and mm in ('RA', 'Sky'): continue
                r = tri(P[x], EP, P[b], mm)
                if r and r[1] <= 0.0015: out[(mm, x, e)].append((b, r[0], r[1], ctype(r[0])))
    return out
ENDS_T = {a: REF[a] for a in RN}
TT = collections.defaultdict(dict)
P0 = {b: pos(b, t0) for b in BODIES}
MALL = {}          # (base key, third body, chord type) -> every Moon strike (Moon third, or Moon a base end): (d, dev, minute)
for k, lst in chords(P0, ENDS_T, [b for b in BODIES if b != 'Moon'], [b for b in LB if b != 'Moon']).items():
    for bn, d, dv, typ in lst: TT[k][bn] = (d, dv, typ, t0)
for t in (np.arange(t0 - 30, t1 + 30 + 1e-9, 0.25) if MOONWIN == 'wide' else np.arange(t0 - 2, t1 + 1e-9, 0.25)):        # the Moon as third point, and as base end in L4
    P = dict(P0); P['Moon'] = pos('Moon', t)
    got = chords(P, ENDS_T, ['Moon'], [b for b in LB if b != 'Moon'])
    if 'Moon' in LB:
        for k, v in chords(P, ENDS_T, [b for b in BODIES if b != 'Moon'], ['Moon']).items(): got[k] += v
    for k, lst in got.items():
        for bn, d, dv, typ in lst:
            if bn not in TT[k] or dv < TT[k][bn][1]: TT[k][bn] = (d, dv, typ, t)
            if (k, bn, typ) not in MALL or dv < MALL[(k, bn, typ)][1]: MALL[(k, bn, typ)] = (d, dv, t)
print('=' * 120)
print(f"{RACE}  off {OFF}  finish {hm(t1)}  - LAYER {LNAME} ({', '.join(LB)}): TRANSIT AND NATAL TUNED IN")
print('=' * 120)
print(f"transit chords: {sum(len(v) for v in TT.values())} on {len(TT)} bases")
def blen(k, P, ends):
    mm, x, e = k; return dist(P[x], ends[e] if e in ends else P[e], mm)
def when_transit(k, tb):
    global LOCKT
    mm, x, e = k
    LOCKT = lockT(P0[x], P0[e] if e in P0 else ENDS_T[e], P0[tb], mm)
    movers = [n for n in (x, e, tb) if n in BODIES]
    span = min(SPAN.get(n, 60) for n in movers); step = span / 1500; best = (9, None)
    for dd_ in np.arange(-span, span + 1e-9, step):
        Q = {n: moved(P0[n], n, dd_) for n in movers}
        r = tri(Q[x], Q[e] if e in Q else ENDS_T[e], Q[tb], mm)
        if r and r[1] < best[0]: best = (r[1], dd_)
    if best[1] is not None:
        for dd_ in np.arange(best[1] - 2 * step, best[1] + 2 * step, step / 200):
            Q = {n: moved(P0[n], n, dd_) for n in movers}
            r = tri(Q[x], Q[e] if e in Q else ENDS_T[e], Q[tb], mm)
            if r and r[1] < best[0]: best = (r[1], dd_)
    LOCKT = None
    return when_dv(best[1], best[1] is not None and abs(abs(best[1]) - span) < step, movers[0] if span == 60 else min(movers, key=lambda n: SPAN.get(n, 60)), best[0])
NAMEC = {}
ALL = []
DUMP = []
for tab, (role, cloth, nm) in order:
    f = fin.get(cloth, ('?', '?', '0')); R = role[0].upper(); NAMEC[tab] = (f, role, nm)
    ends = {a: NATB[tab][a] for a in RN if a in STARS and a in NATB[tab]}; ends['Equator'] = REF['Equator']
    NN = chords(NATP[tab], ends, list(NATP[tab]), [b for b in LB if b in NATP[tab]])
    pairs = []
    for k, lst in NN.items():
        if k not in TT: continue
        lt, ln = blen(k, P0, ENDS_T), blen(k, NATP[tab], ends)
        rr = max(lt, ln) / max(min(lt, ln), 1e-9); nmv, dvr = iv(rr)
        rel = 'SAME LENGTH' if nmv == '1' and dvr <= 0.0015 else (f"lengths {nmv}" if dvr <= 0.0015 else f"ratio {rr:.3f}")
        for bn, d, dv, typ in lst:
            for tb, (td, tdv, ttyp, tt) in TT[k].items():
                pairs.append((k, bn, d, dv, typ, tb, td, tdv, ttyp, tt, lt, ln, rel))
                if not (tb == 'Moon' or 'Moon' in k): DUMP.append((LNAME, tab, k[0], k[1], k[2], bn, dv, typ, tb, tdv, ttyp, d[1], d[2], td[1], td[2], tt, ln, lt, rel))
                ALL.append((tab, k, bn, dv, typ, tb, tdv, ttyp, tt, rel))
        for (mk, tbn, mty), (md, mdv, mt) in MALL.items():          # the Moon: every strike on this base
            if mk != k: continue
            Pm = dict(P0); Pm['Moon'] = pos('Moon', mt); ltm = blen(k, Pm, ENDS_T)
            rrm = max(ltm, ln) / max(min(ltm, ln), 1e-9); nm_, dr_ = iv(rrm)
            relm = 'SAME LENGTH' if nm_ == '1' and dr_ <= 0.0015 else (f"lengths {nm_}" if dr_ <= 0.0015 else f"ratio {rrm:.3f}")
            for bn, d, dv, typ in lst:
                DUMP.append((LNAME, tab, k[0], k[1], k[2], bn, dv, typ, tbn, mdv, mty, d[1], d[2], md[1], md[2], mt, ln, ltm, relm))
    print('\n' + '-' * 120)
    print(f"[{f[0]}] {role.upper():6s} {nm:24s} {f[1]:>5s}{' FAV' if f[2] == '1' else ''}   natal chords {sum(len(v) for v in NN.values())}   tuned pairs {len(pairs)}   "
          f"UNISON {sum(1 for p in pairs if p[4] == p[8])}   same body {sum(1 for p in pairs if p[1] == p[5])}   lengths in tune {sum(1 for p in pairs if not p[12].startswith('ratio'))}")
    for p in sorted(pairs, key=lambda p: max(p[3], p[7])):
        k, bn, d, dv, typ, tb, td, tdv, ttyp, tt, lt, ln, rel = p
        flag = [x for x, c in (('UNISON', typ == ttyp), ('SAME BODY', bn == tb)) if c]
        if max(dv, tdv) > 0.0005 and not flag and tb != 'Moon': continue
        ws = f"Moon held at {hm(tt)} ({tt - t0:+.2f})" if tb == 'Moon' or 'Moon' in k else when_transit(k, tb)
        mm, x, e = k
        print(f"   base {mm:4s} {x}–{e}   transit {lt:.3f} / natal {ln:.3f}  {rel}   {' '.join(flag)}")
        print(f"      natal   {R}.{bn:10s} {typ:14s} {d[1]:8.3f} | {d[2]:8.3f}   dev {dv*100:.3f}%")
        print(f"      transit {tb:12s} {LAYER[tb]:5s} {ttyp:14s} {td[1]:8.3f} | {td[2]:8.3f}   dev {tdv*100:.3f}%   {ws}")
    print("   (listed: both sides within 0.05%, every UNISON / SAME BODY, every Moon)")
print('\n' + '=' * 120)
print("TRANSIT CHORDS HELD IN THE RACE WINDOW (Moon) OR EXACT WITHIN 1 HOUR OF THE OFF - and who is tuned in")
rows = []
for k, d_ in TT.items():
    for tb, (td, tdv, ttyp, tt) in d_.items():
        if tb == 'Moon' or 'Moon' in k: rows.append((tt - t0, k, tb, ttyp, tdv, f"Moon held at {hm(tt)} ({tt - t0:+.2f})"))
        else:
            mm, x, e = k; movers = [n for n in (x, e, tb) if n in BODIES]
            span = 1 / 24; best = (9, None); LOCKT = lockT(P0[x], P0[e] if e in P0 else ENDS_T[e], P0[tb], mm)
            for dd_ in np.arange(-span, span + 1e-9, span / 240):
                Q = {n: moved(P0[n], n, dd_) for n in movers}
                r = tri(Q[x], Q[e] if e in Q else ENDS_T[e], Q[tb], mm)
                if r and r[1] < best[0]: best = (r[1], dd_)
            LOCKT = None
            if best[1] is not None and abs(best[1]) < span - span / 240 and best[0] < 0.0002:
                rows.append((best[1] * 1440, k, tb, ttyp, tdv, f"exact {hm(t0 + best[1]*1440)} ({best[1]*1440:+.1f} min)"))
for m_, k, tb, ttyp, tdv, ws in sorted(rows, key=lambda r: r[0]):
    who = [f"{NAMEC[tab][2].split(' ',1)[1]} ({NAMEC[tab][1][0]}{NAMEC[tab][0][0]}) {bn} {typ}{' U' if typ == ttyp else ''} {dv*100:.3f}% [{rel}]"
           for tab, kk, bn, dv, typ, tbb, tdvv, ttypp, tt, rel in ALL if kk == k and tbb == tb]
    print(f"   {ws:34s} {k[0]:4s} {k[1]}–{k[2]} + {tb} {ttyp} {tdv*100:.3f}%")
    print(f"        tuned: {'; '.join(who) if who else '-'}")
import csv as _csv
with open(f"/home/claude/lattice/dump/{RACE}_{LNAME}.csv", "w", newline="") as _f:
    # extra columns (8 Oct): third body–x | –e on each side, minute held (Moon) or the off (slow), natal / transit base lengths and their relation, exact time
    _w = _csv.writer(_f); _w.writerow(["layer", "tab", "mm", "x", "e", "natal_body", "natal_dev", "natal_type", "transit_body", "transit_dev", "transit_type",
                                       "natal_dx", "natal_de", "transit_dx", "transit_de", "transit_t", "natal_base", "transit_base", "lengths", "transit_when"])
    _WT = {}
    for r in DUMP:
        k, tb, tt = (r[2], r[3], r[4]), r[8], r[15]
        if tb == 'Moon' or 'Moon' in k: _w.writerow(list(r) + [f"Moon held at {hm(tt)} ({tt - t0:+.2f})"]); continue     # per strike, never cached
        if (k, tb) not in _WT: _WT[(k, tb)] = when_transit(k, tb)
        _w.writerow(list(r) + [_WT[(k, tb)]])
