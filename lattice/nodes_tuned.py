"""nodes_tuned.py RACE OFF DUR_S - NODES LAYER as TRANSIT AND NATAL TUNED IN (Eddie, 6 Oct 2026).
Base = a node at one end: Rahu–X or Ketu–X (X = a star, the equator, course latitude [transit only]) and Rahu–Ketu (Dec, Flat only).
Third point = a BODY (stars as third points were Layer 1). Transit: transit node + transit body, stars on race day
(slow bodies at the off; the Moon every 15 s off-2 to the finish). Natal: the chart's own node + own point (midday, no Moon),
stars at birth. TUNED IN = same named base and measure on both sides (e.g. Dec Rahu–Capella).
The two base lengths differ (transit node is not natal node): their ratio is shown - SAME LENGTH, an interval, or none.
UNISON = same chord type. SAME BODY = transit X / natal X as the third point. Rahu–Ketu as a pair: RA, Sky skipped."""
import sys
src = open('/home/claude/lattice/layer1_tuned.py').read()
exec(src.split('# transit chords')[0])
NATP = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] in BODIES and r['body'] != 'Moon':
        NATP[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
MEAS = ('RA', 'Dec', 'Flat', 'Sky')
def rk(a, b): return {a, b} == {'Rahu', 'Ketu'}
def chords(nodes, ends, bodies, label):
    """nodes {name: pos}, ends {name: pos}, bodies {name: pos} -> {(mm, node, end): [(third, d, dev, type)]}"""
    out = collections.defaultdict(list)
    for nn, NP in nodes.items():
        E = dict(ends); E[('Ketu' if nn == 'Rahu' else 'Rahu')] = nodes['Ketu' if nn == 'Rahu' else 'Rahu']
        for en, EP in E.items():
            if en == 'Rahu' and nn == 'Ketu': continue          # Rahu–Ketu base once
            for bn, BP in bodies.items():
                if bn in ('Rahu', 'Ketu'): continue
                for mm in MEAS:
                    if rk(nn, en) and mm in ('RA', 'Sky'): continue
                    if en == 'Equator' and rk(nn, en): continue
                    r = tri(NP, EP, BP, mm)
                    if r and r[1] <= 0.0015: out[(mm, nn, en)].append((bn, r[0], r[1], ctype(r[0])))
    return out
# transit
ENDS_T = {a: REF[a] for a in RN}
TT = collections.defaultdict(dict)
MALL = {}          # (base key, chord type) -> every Moon strike: (d, dev, minute)
for t in [t0] + list((np.arange(t0 - 30, t1 + 30 + 1e-9, 0.25) if MOONWIN == 'wide' else np.arange(t0 - 2, t1 + 1e-9, 0.25))):
    nodes = {'Rahu': pos('Rahu', t), 'Ketu': pos('Ketu', t)}
    bodies = {b: pos(b, t) for b in BODIES if (b == 'Moon') == (t != t0) or (t == t0 and b != 'Moon')}
    if t != t0: bodies = {'Moon': pos('Moon', t)}
    for k, lst in chords(nodes, ENDS_T, bodies, 'T').items():
        for bn, d, dv, typ in lst:
            if bn not in TT[k] or dv < TT[k][bn][1]: TT[k][bn] = (d, dv, typ, t)
            if bn == 'Moon' and ((k, typ) not in MALL or dv < MALL[(k, typ)][1]): MALL[(k, typ)] = (d, dv, t)
NT = sum(len(v) for v in TT.values())
print('=' * 120)
print(f"{RACE}  off {OFF}  finish {hm(t1)}  - NODES LAYER: TRANSIT AND NATAL TUNED IN (bases with a node at one end; third point a body)")
print('=' * 120)
print(f"transit chords: {NT} on {len(TT)} bases   by third body: " + ', '.join(f"{b} {n}" for b, n in collections.Counter(b for v in TT.values() for b in v).most_common()))
def baselen(k, nodes, ends):
    mm, nn, en = k; E = dict(ends); E.update(nodes); return dist(nodes[nn], E[en], mm)
TN0 = {'Rahu': pos('Rahu', t0), 'Ketu': pos('Ketu', t0)}
summ = []
DUMP = []
for tab, (role, cloth, nm) in order:
    f = fin.get(cloth, ('?', '?', '0')); R = role[0].upper()
    ends = {a: NATB[tab][a] for a in RN if a in STARS and a in NATB[tab]}; ends['Equator'] = REF['Equator']
    nodes = {'Rahu': NATP[tab]['Rahu'], 'Ketu': NATP[tab]['Ketu']}
    NN = chords(nodes, ends, NATP[tab], 'N')
    pairs = []
    for k, lst in NN.items():
        if k not in TT: continue
        lt, ln = baselen(k, TN0, ENDS_T), baselen(k, nodes, ends)
        rr = max(lt, ln) / min(lt, ln); nmv, dvr = iv(rr)
        rel = 'SAME LENGTH' if nmv == '1' and dvr <= 0.0015 else (f"lengths {nmv}" if dvr <= 0.0015 else f"ratio {rr:.3f}")
        for bn, d, dv, typ in lst:
            for tb, (td, tdv, ttyp, tt) in TT[k].items():
                pairs.append((k, bn, d, dv, typ, tb, td, tdv, ttyp, tt, lt, ln, rel))
                if tb != 'Moon': DUMP.append(("Nodes", tab, k[0], k[1], k[2], bn, dv, typ, tb, tdv, ttyp, d[1], d[2], td[1], td[2], tt, ln, lt, rel))
            for (mk, mty), (md, mdv, mt) in MALL.items():            # the Moon: every strike on this base
                if mk == k: DUMP.append(("Nodes", tab, k[0], k[1], k[2], bn, dv, typ, 'Moon', mdv, mty, d[1], d[2], md[1], md[2], mt, ln, lt, rel))
    summ.append((f, role, nm, pairs))
    print('\n' + '-' * 120)
    un = sum(1 for p in pairs if p[4] == p[8]); sb = sum(1 for p in pairs if p[1] == p[5])
    sl = sum(1 for p in pairs if not p[12].startswith('ratio'))
    print(f"[{f[0]}] {role.upper():6s} {nm:24s} {f[1]:>5s}{' FAV' if f[2] == '1' else ''}   natal node chords {sum(len(v) for v in NN.values())}   "
          f"tuned pairs {len(pairs)}   UNISON {un}   same body {sb}   base lengths in tune {sl}")
    for p in sorted(pairs, key=lambda p: max(p[3], p[7])):
        k, bn, d, dv, typ, tb, td, tdv, ttyp, tt, lt, ln, rel = p
        flag = [x for x, c in (('UNISON', typ == ttyp), ('SAME BODY', bn == tb), (rel, not rel.startswith('ratio'))) if c]
        if max(dv, tdv) > 0.0005 and not flag: continue
        x, xd, edge = (None, None, False)
        if tb == 'Moon': when_s = f"Moon held at {hm(tt)} ({tt - t0:+.2f})"
        else:
            # exact time of the transit chord at the body's and node's rates
            mm, nn, en = k; P0 = pos(tb, t0); N0 = TN0[nn]; E0 = (TN0[en] if en in TN0 else ENDS_T[en])
            span = SPAN.get(tb, 60); best = (9, None); LOCKT = lockT(N0, E0, P0, mm)
            for dd_ in np.arange(-span, span + 1e-9, span / 1500):
                Ed = moved(E0, en, dd_) if en in TN0 else E0
                r = tri(moved(N0, nn, dd_), Ed, moved(P0, tb, dd_), mm)
                if r and r[1] < best[0]: best = (r[1], dd_)
            if best[1] is not None:
                for dd_ in np.arange(best[1] - span / 750, best[1] + span / 750, span / 300000):
                    Ed = moved(E0, en, dd_) if en in TN0 else E0
                    r = tri(moved(N0, nn, dd_), Ed, moved(P0, tb, dd_), mm)
                    if r and r[1] < best[0]: best = (r[1], dd_)
            LOCKT = None
            when_s = when(best[1], best[1] is not None and abs(abs(best[1]) - span) < span / 1500, tb)
        mm, nn, en = k
        print(f"   base {mm:4s} {nn}–{en}   transit {lt:.3f} / natal {ln:.3f}  {rel}   {' '.join(f for f in flag if not f.startswith('lengths') and f != 'SAME LENGTH')}")
        print(f"      natal   {R}.{nn}–{R}.{en if en in ('Rahu','Ketu') else en} + {R}.{bn:10s} {typ:14s} {d[1]:8.3f} | {d[2]:8.3f}   dev {dv*100:.3f}%")
        print(f"      transit {nn}–{en} + {tb:12s} {LAYER[tb]:5s} {ttyp:14s} {td[1]:8.3f} | {td[2]:8.3f}   dev {tdv*100:.3f}%   {when_s}")
    print("   (listed: both sides within 0.05%, plus every UNISON, SAME BODY and base lengths in tune)")
print('\n' + '=' * 120)
print("SUMMARY   tuned pairs / UNISON / same body / base lengths in tune / both within 0.02%")
for f, role, nm, pairs in summ:
    print(f"   [{f[0]}] {role:6s} {nm:24s} {f[1]:>5s}  {len(pairs):4d} {sum(1 for p in pairs if p[4]==p[8]):4d} {sum(1 for p in pairs if p[1]==p[5]):4d} "
          f"{sum(1 for p in pairs if not p[12].startswith('ratio')):4d} {sum(1 for p in pairs if max(p[3], p[7]) <= 0.0002):4d}")
import csv as _csv
with open(f"/home/claude/lattice/dump/{RACE}_Nodes.csv", "w", newline="") as _f:
    # extra columns (8 Oct): third body–node | –end on each side, minute held (Moon) or the off (slow), base lengths and relation, exact time
    def _node_when(k, tb):     # the same search as the printed list above
        global LOCKT
        mm, nn, en = k; P0 = pos(tb, t0); N0 = TN0[nn]; E0 = (TN0[en] if en in TN0 else ENDS_T[en])
        span = SPAN.get(tb, 60); best = (9, None); LOCKT = lockT(N0, E0, P0, mm)
        for dd_ in np.arange(-span, span + 1e-9, span / 1500):
            Ed = moved(E0, en, dd_) if en in TN0 else E0
            r = tri(moved(N0, nn, dd_), Ed, moved(P0, tb, dd_), mm)
            if r and r[1] < best[0]: best = (r[1], dd_)
        if best[1] is not None:
            for dd_ in np.arange(best[1] - span / 750, best[1] + span / 750, span / 300000):
                Ed = moved(E0, en, dd_) if en in TN0 else E0
                r = tri(moved(N0, nn, dd_), Ed, moved(P0, tb, dd_), mm)
                if r and r[1] < best[0]: best = (r[1], dd_)
        LOCKT = None
        return when(best[1], best[1] is not None and abs(abs(best[1]) - span) < span / 1500, tb)
    _w = _csv.writer(_f); _w.writerow(["layer", "tab", "mm", "x", "e", "natal_body", "natal_dev", "natal_type", "transit_body", "transit_dev", "transit_type",
                                       "natal_dx", "natal_de", "transit_dx", "transit_de", "transit_t", "natal_base", "transit_base", "lengths", "transit_when"])
    _WT = {}
    for r in DUMP:
        k, tb, tt = (r[2], r[3], r[4]), r[8], r[15]
        if tb == 'Moon': _w.writerow(list(r) + [f"Moon held at {hm(tt)} ({tt - t0:+.2f})"]); continue     # per strike, never cached
        if (k, tb) not in _WT: _WT[(k, tb)] = _node_when(k, tb)
        _w.writerow(list(r) + [_WT[(k, tb)]])
