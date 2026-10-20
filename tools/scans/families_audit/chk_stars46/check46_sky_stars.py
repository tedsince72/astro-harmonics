#!/usr/bin/env python3
"""check46_sky_stars.py (independent checker, 20 Oct 2026, adapted from chk_sky35): SKY STARS on the 46 stars of T1 / T2 / T24 (no Polaris) and the sky TIMELINE /
LONG TIMELINE star events, recomputed from the POSITIONS sheet with own code (families.py for targets / scores only; the engine for real
times). Imports from jupiter_tables only the star lists.

usage: check_sky35.py <after tables.xlsx> <before tables.xlsx> <batch.xlsx> [race]"""
import sys, os, math, datetime, re
import openpyxl

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'tools'))
sys.path.insert(0, os.path.join(REPO, 'tools', 'jup2'))
sys.path.insert(0, os.path.join(REPO, 'rebuild_kit'))
import families                                                                # noqa: E402
from jupiter_tables import STARS, T1_T2_T24_STARS, NEW_STARS                  # noqa: E402  (constants only)

AFTER, BEFORE, BATCH = sys.argv[1:4]
RACE = sys.argv[4] if len(sys.argv) > 4 else 'ascot_1430_20120619'
OFF = datetime.datetime(2012, 6, 19, 14, 30)
PLANES = ('RA', 'Dec', 'Equator')
CONJ = {'RA': 1.5, 'Dec': 0.3, 'Equator': 0.3}
MTOL = {'RA': 0.5, 'Dec': 0.15, 'Equator': 0.15}
FILL = {'green': '00C6EFCE', 'yellow': '00FFEB9C', 'light': '00FFF8DC'}
AREA_NAME = {'A': 'A', 'P': 'φ and √2', 'B': 'B'}
NEW11 = ['Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Menkar', 'Phact', 'Adhara', 'Wezen', 'Menkent', 'Unukalhai', 'Rasalhague']
ORDER = [s for s in STARS if s != 'Polaris'] + [s for s in T1_T2_T24_STARS if s not in STARS]   # old order, then the 24 new in RA order
assert sorted(ORDER) == sorted(T1_T2_T24_STARS) and len(ORDER) == 46 and set(NEW11) < set(NEW_STARS)
NEW_STARS = NEW11                                  # 'new' below = the 11 of 20 Oct 2026
bad = []


def mis(where, got, exp):
    bad.append((where, got, exp))


# ---------- positions
def positions(wb):
    ws = wb['POSITIONS']
    P = {}
    for r in ws.iter_rows(values_only=True):
        if r[0] == 'SKY' and r[2] == 'S':
            P[r[3]] = (float(r[5]), float(r[6]), float(r[7]), float(r[8]))
    return P


wa, wbf = openpyxl.load_workbook(AFTER), openpyxl.load_workbook(BEFORE)
P = positions(wa)
for s in ORDER + ['Jupiter']:
    assert s in P, s


def pos(x, t):
    ra, dec, rra, rdec = P[x]
    return ra + t * rra, dec + t * rdec


def wrap(x):
    x = (x + 180.0) % 360.0 - 180.0
    return 180.0 if x == -180.0 else x


def dist_pos(pa, pb, pl):
    if pl == 'RA':
        x = abs(pa[0] - pb[0]) % 360.0
        return min(x, 360.0 - x)
    if pl == 'Dec':
        return abs(pa[1] - pb[1])
    return abs(abs(pa[1]) - abs(pb[1]))


def d(a, b, pl, t=0.0):
    return dist_pos(pos(a, t), pos(b, t), pl)


# ---------- text helpers (own)
def exact_t(v0, v5, tv):
    if v5 == v0:
        return None
    return (tv - v0) / ((v5 - v0) / 5.0)


def clock(t):
    w = OFF + datetime.timedelta(minutes=t)
    return w.strftime('%H:%M') if w.date() == OFF.date() else w.strftime('%d %b %Y %H:%M')


def timing(v0, v5, tv):
    t = exact_t(v0, v5, tv)
    if t is None:
        return 'no motion'
    if abs(t) > 50 * 525960:
        return f"{'applying' if t >= 0 else 'separating'}, exact more than 50 years {'away' if t >= 0 else 'ago'}"
    return f'applying, exact {clock(t)} (in {t:.1f} min)' if t >= 0 else f'separating, exact {clock(t)} ({-t:.1f} min ago)'


def colour(s):
    return 'green' if s >= 80 else 'yellow' if s >= 50 else 'light' if s > 0 else ''


def fam_best(v, pl):
    ev = families.evaluate(v, pl if pl in ('RA', 'Dec') else None, 'deg')
    return ev[0] if ev else None


def tlab(e):
    return f"{e['target']} · {e['name']} · {e['group']}" if e['family'] == 'interval' else f"{e['target']} ({e['family']})"


# ---------- SKY STARS recomputation
def row_for(x, y, pl):
    J = 'Jupiter'
    if pl == 'Equator':
        signs = {P[z][1] >= 0 for z in (J, x, y)}
        if len(signs) == 1:
            return None
    dX0, dY0, dXY0 = d(J, x, pl), d(J, y, pl), d(x, y, pl)
    dX5, dY5, dXY5 = d(J, x, pl, 5), d(J, y, pl, 5), d(x, y, pl, 5)
    h = dict(x=x, y=y, pl=pl, dX=dX0, dY=dY0, dXY=dXY0)
    h['together'] = dXY0 < CONJ[pl]
    legs = []
    for (a, b), v0, v5 in ((('S Jupiter', f'S {x}'), dX0, dX5), (('S Jupiter', f'S {y}'), dY0, dY5), ((f'S {x}', f'S {y}'), dXY0, dXY5)):
        legs.append(((a, b), v0, v5, fam_best(v0, pl)))
    h['legs'] = legs
    if dX0 >= dY0:
        r0, r5 = dX0 / dY0, dX5 / dY5
    else:
        r0, r5 = dY0 / dX0, dY5 / dX5
    h['r0'], h['r5'] = r0, r5
    ev = families.evaluate(r0, None, 'ratio')
    h['ev'] = ev[0] if ev else None
    h['near'] = h['ev'] or families.outside(r0, None, 'ratio')
    c = 100.0 * min(dX0, dY0) / max(dX0, dY0)
    h['c'] = c
    h['mid'] = None
    if c >= 90:
        if pl == 'RA':
            a, b, j = P[x][0], P[y][0], P[J][0]
            m = a + wrap(b - a) / 2.0
            on, of = wrap(j - m), wrap(j - (m + 180.0))
            off, lab = (on, 'near') if abs(on) <= abs(of) else (of, 'far')
        elif pl == 'Dec':
            off, lab = P[J][1] - (P[x][1] + P[y][1]) / 2.0, None
        else:
            off, lab = abs(P[J][1]) - (abs(P[x][1]) + abs(P[y][1])) / 2.0, None
        tol = MTOL[pl]
        h['moff'], h['mlab'] = off, lab
        rh = 0.5 * (10.0 - (100.0 - c)) ** 2
        if abs(off) < tol:
            dh = 0.5 * (10.0 * (tol - abs(off)) / tol) ** 2
            h['mid'] = (rh, dh, rh + dh)
    s = sum(1 for l in legs if l[3])
    h['listed'] = (not h['together']) and (h['ev'] is not None or h['mid'] is not None or s == 3)
    if h['ev'] is not None and families.area(h['ev']['target']) == 'A' or h['mid'] is not None:
        h['area'] = 'A'
    elif h['ev'] is not None:
        h['area'] = families.area(h['ev']['target'])
    else:
        h['area'] = 'none'
    h['key'] = max(h['ev']['score'] if h['ev'] else 0.0, h['mid'][2] if h['mid'] else 0.0)
    return h


def expected_cells(h):
    pl = h['pl']
    out = {'A': 'SKY STARS', 'B': 'S–S', 'C': f"S {h['x']} – S {h['y']}", 'D': pl}
    fills = {}
    for (col, fcol), ((a, b), v0, v5, bf) in zip((('E', 'F'), ('G', 'H'), ('I', 'J')), h['legs']):
        out[col] = round(v0, 6)
        if bf:
            out[fcol] = f"→ {bf['target']} ({bf['family']}, {bf['score']:.2f}) · {timing(v0, v5, bf['tv'])}"
            fills[fcol] = FILL[colour(bf['score'])]
        else:
            out[fcol] = 'no family'
    n, ev = h['near'], h['ev']
    out['K'] = round(h['r0'], 6)
    if ev:
        out['L'] = tlab(n)
        out['N'] = round(ev['score'], 2)
        fills['K'] = fills['N'] = FILL[colour(ev['score'])]
    else:
        out['L'] = f"{tlab(n)} — outside ±{n['tol']:.3g}{' %' if n['pct'] else ''}"
        out['N'] = None
    out['M'] = f"{n['off']:+.5f}{'%' if n['pct'] else ''}"
    out['O'] = timing(h['r0'], h['r5'], n['tv'])
    s = h['dX'] + h['dY']
    out['P'] = 'between' if abs(h['dXY'] - s) <= 0.01 * s else 'far side'
    out['Q'] = None
    if h['c'] >= 90:
        t = f"{h['moff']:+.6f}" + (f" {h['mlab']}" if h['mlab'] else '')
        if h['mid'] is None:
            t += f" (outside ±{MTOL[pl]:g})"
        out['R'] = t
        out['S'] = round(h['c'], 4)
        if h['mid']:
            out['T'], out['U'], out['V'] = (round(v, 2) for v in h['mid'])
            fills['V'] = FILL[colour(h['mid'][2])]
        else:
            out['T'] = out['U'] = out['V'] = None
    else:
        for c in 'RSTUV':
            out[c] = None
    return out, fills


def eq(a, b):
    if isinstance(a, float) or isinstance(b, float):
        try:
            return abs(float(a) - float(b)) < 5e-7
        except (TypeError, ValueError):
            return False
    return a == b


rows = {}
n_pairplanes = 0
for i, x in enumerate(ORDER):
    for y in ORDER[i + 1:]:
        for pl in PLANES:
            h = row_for(x, y, pl)
            if h is None:
                continue
            n_pairplanes += 1
            rows[(f'S {x} – S {y}', pl)] = h
listed = {k: h for k, h in rows.items() if h['listed']}
print(f'pair-planes generated: {n_pairplanes} (pairs {46 * 45 // 2}); together {sum(h["together"] for h in rows.values())}; listed {len(listed)}')
cnt = {}
for h in listed.values():
    cnt[h['area']] = cnt.get(h['area'], 0) + 1
print('listed per area (A / P / B / none):', cnt)


def area_of_title(t):
    return 'A' if 'AREA A' in t else 'P' if 'AREA φ' in t else 'B' if 'AREA B' in t else 'none'


def sheet_stars(ws):
    out, order, titles, blk = {}, [], [], None
    for r in ws.iter_rows():
        a = r[0].value
        if isinstance(a, str) and a.startswith('SKY STARS') and r[1].value is None:
            if 'AREA' in a or 'NO RATIO' in a:
                blk = area_of_title(a)
                titles.append((blk, a))
            continue
        if a == 'SKY STARS':
            v = {openpyxl.utils.get_column_letter(c.column): c.value for c in r[:22]}
            f = {openpyxl.utils.get_column_letter(c.column): c.fill.start_color.rgb for c in r[:22] if c.fill and c.fill.fill_type}
            key = (v['C'], v['D'])
            out[key] = (blk, v, f)
            order.append((blk, key))
    return out, order, titles


SA, OA, TA = sheet_stars(wa['SKY JUPITER'])
SB, OB, TB = sheet_stars(wbf['SKY JUPITER'])
print('sheet SKY STARS rows after', len(SA), 'before', len(SB))
# listed set
for k in listed:
    if k not in SA:
        mis(f'SKY STARS missing {k}', None, 'listed')
for k in SA:
    if k not in listed:
        mis(f'SKY STARS extra {k}', 'on sheet', 'not listed' if k in rows else 'not a pair-plane')
# blocks, titles, order
for blk, title in TA:
    m = re.search(r': (\d+) rows', title)
    n = sum(1 for h in listed.values() if h['area'] == blk)
    if not m or int(m.group(1)) != n:
        mis(f'title count {blk}', title[-12:], n)
ncell = 0
for k, (blk, v, f) in SA.items():
    if k not in listed:
        continue
    h = listed[k]
    if blk != h['area']:
        mis(f'block {k}', blk, h['area'])
    exp, ef = expected_cells(h)
    for col, ev in exp.items():
        ncell += 1
        if not eq(v.get(col), ev):
            mis(f'cell {col} {k}', v.get(col), ev)
    for col in 'EFGHIJKLMNOPQRSTUV':
        if f.get(col) != ef.get(col):
            mis(f'fill {col} {k}', f.get(col), ef.get(col))
for blk in ('A', 'P', 'B', 'none'):
    seq = [listed[k]['key'] for b, k in OA if b == blk and k in listed]
    for i in range(1, len(seq)):
        if seq[i] > seq[i - 1] + 1e-9:
            mis(f'order {blk} at {i}', seq[i], f'<= {seq[i - 1]}')
print('SKY STARS cells compared:', ncell)

# before vs after
old_after = {k: x for k, x in SA.items() if not any(re.search(rf'S {re.escape(s)}( –|$)', k[0]) for s in NEW_STARS)}
dropped = [k for k in SB if k not in SA]
non_pol = [k for k in dropped if 'Polaris' not in k[0]]
print(f'before rows {len(SB)}, of them Polaris {sum("Polaris" in k[0] for k in SB)}; dropped {len(dropped)} (non-Polaris {len(non_pol)})')
for k in non_pol:
    mis(f'dropped non-Polaris {k}', 'gone', 'kept')
for k, (blk, v, f) in old_after.items():
    if k not in SB:
        mis(f'old-star row new in after {k}', 'new', 'in before')
        continue
    bb, bv, bfl = SB[k]
    if bb != blk or any(not eq(v.get(c), bv.get(c)) for c in v) or f != bfl:
        mis(f'old-star row changed {k}', (blk, v), (bb, bv))
print(f'old-star rows in after {len(old_after)}, new-star rows {len(SA) - len(old_after)}')
# relative order of old rows unchanged within blocks
for blk in ('A', 'P', 'B', 'none'):
    oa = [k for b, k in OA if b == blk and k in old_after]
    ob = [k for b, k in OB if b == blk and k in old_after]
    if oa != ob:
        mis(f'old-row order in block {blk}', len(oa), len(ob))

# ---------- TIMELINE / LONG TIMELINE
STAR_ALL = ORDER + ['Polaris']
NEWRX = re.compile(r'S (' + '|'.join(re.escape(s) if s != 'Deneb' else r'Deneb(?! Algedi)' for s in NEW_STARS) + r')\b')


def tl_rows(ws):
    out = {'TIMELINE': [], 'LONG TIMELINE': []}
    titles = {}
    for r in ws.iter_rows(values_only=True):
        a = r[0]
        if a in out:
            if r[3] and str(r[3]).startswith('———') or r[4] is None:
                out[a].append(('MARK', r[:15]))
            else:
                out[a].append(('EV', r[:15]))
        elif isinstance(a, str) and a.startswith(('TIMELINE (', 'LONG TIMELINE (')):
            titles[a.split(' (')[0]] = a
    return out, titles


TLA, TTA = tl_rows(wa['SKY JUPITER'])
TLB, TTB = tl_rows(wbf['SKY JUPITER'])


def ev_key(r):
    return (r[3], r[4], r[5], r[6], r[7])


def is_new(r):
    return bool(NEWRX.search(str(r[4])))


def pts_of(rel):
    return re.findall(r'S ([A-Za-z ]+?)(?= –| →| =|$)', rel.replace('S Jupiter: ', 'S Jupiter – '))


def star_only(r):
    names = [p.strip() for p in re.split(r' → | – | = |: ', str(r[4]))]
    names = [n[2:] for n in names]
    return all(n in STAR_ALL or n == 'Jupiter' for n in names)


# non-new events unchanged vs before (minus Polaris)
for tab in ('TIMELINE', 'LONG TIMELINE'):
    A = {ev_key(r): r for k, r in TLA[tab] if k == 'EV' and not is_new(r)}
    B = {ev_key(r): r for k, r in TLB[tab] if k == 'EV' and 'Polaris' not in str(r[4])}
    pol = [r for k, r in TLB[tab] if k == 'EV' and 'Polaris' in str(r[4])]
    print(f'{tab}: after events {sum(k == "EV" for k, _ in TLA[tab])} (new-star {sum(k == "EV" and is_new(r) for k, r in TLA[tab])}); '
          f'before {sum(k == "EV" for k, _ in TLB[tab])} (Polaris {len(pol)}: {[ (r[4], r[5], r[7]) for r in pol]})')
    for k in A.keys() - B.keys():
        mis(f'{tab} non-new event not in before', k, None)
    for k in B.keys() - A.keys():
        mis(f'{tab} before event gone', k, None)
    for k in A.keys() & B.keys():
        ra, rb = A[k], B[k]
        diff = [i for i in range(15) if not eq(ra[i], rb[i])]
        if diff:
            mis(f'{tab} event changed {k}', [ra[i] for i in diff], [rb[i] for i in diff])

# own reconstruction of star-only events: SKY block star rows (RA / Dec), then SKY STARS listed rows
def tl_target(e):
    if e['family'] == 'interval':
        return f"{tlab(e)} (area {AREA_NAME[families.area(e['target'])]})"
    return tlab(e)


def fold_key(e):
    if e['family'] == 'conj' or not e.get('tv'):
        return ('conj', 0)
    m = e['tv'] / 10 ** math.floor(math.log10(e['tv']))
    return e['family'], round(m, 5)


cands = {}


def add(key, ev):
    if ev['t'] is None:
        return
    if key in cands:
        if ev['src'] != cands[key]['src'] and ev['src'] not in cands[key]['also']:
            cands[key]['also'].append(ev['src'])
        return
    ev['also'] = []
    cands[key] = ev


def add_dist(src, a, b, pl, v0, v5, e, hit):
    kp = pl
    if pl == 'Equator' and (pos(a[2:], 0)[1] >= 0) == (pos(b[2:], 0)[1] >= 0):
        kp = 'Dec'
    rel = f'{a} → {b}' if a == 'S Jupiter' else f'{a} – {b}'
    add(('d', frozenset((a, b)), kp, fold_key(e)),
        dict(src=src, rel=rel, plane=pl, kind='distance', target=tl_target(e), tv=e['tv'], v0=v0, t=exact_t(v0, v5, e['tv']),
             score=e['score'] if hit else None, out=not hit, geo=('d', a[2:], b[2:], pl)))


for s in ORDER:
    for pl in ('RA', 'Dec'):
        v0, v5 = d('Jupiter', s, pl), d('Jupiter', s, pl, 5)
        b = fam_best(v0, pl)
        if b:
            add_dist('SKY', 'S Jupiter', f'S {s}', pl, v0, v5, b, True)
        else:
            o = families.outside(v0, pl, 'deg')
            if o:
                add_dist('SKY', 'S Jupiter', f'S {s}', pl, v0, v5, o, False)
sky_new = [e for e in cands.values() if NEWRX.search(e['rel'])]
for blk_order in [OA]:                                   # SKY STARS rows in sheet order
    for blk, k in blk_order:
        h = listed.get(k)
        if h is None or h['together']:
            continue
        rel = f"S Jupiter: S {h['x']} – S {h['y']}"
        n, ev = h['near'], h['ev']
        geo = ('r', h['x'], h['y'], h['pl'], h['dX'] >= h['dY'])
        add(('r', frozenset((h['x'], h['y'])), h['pl'], n['target']),
            dict(src='SKY STARS', rel=rel, plane=h['pl'], kind='ratio', target=tl_target(n), tv=n['tv'], v0=h['r0'],
                 t=exact_t(h['r0'], h['r5'], n['tv']), score=ev['score'] if ev else None, out=not ev, geo=geo))
        if h['mid'] is not None:
            add(('r', frozenset((h['x'], h['y'])), h['pl'], '1'),
                dict(src='SKY STARS', rel=rel, plane=h['pl'], kind='midpoint', target='1 · unison · midpoint (area A)', tv=1.0, v0=h['r0'],
                     t=exact_t(h['r0'], h['r5'], 1.0), score=h['mid'][2], out=False, geo=geo))
        for (a, b), v0, v5, bf in h['legs']:
            if bf and v0:
                add_dist('SKY STARS', a, b, h['pl'], v0, v5, bf, True)

# ---------- engine for real times
import swisseph as swe                                                         # noqa: E402
import celestial_bodies_swisseph as E                                          # noqa: E402
import motion                                                                  # noqa: E402
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe'))
off_s, site, _ = motion.off_and_site(RACE, 'TRANS', BATCH, None, None)
JD0 = E._to_jd_ut(E._parse_time(off_s, 'Europe/London'))
_cache = {}
NEEDED = ['Jupiter'] + ORDER


def eng(m):
    if m not in _cache:
        b = E.bodies_at(JD0 + m / 1440.0, *site, False)
        _cache[m] = {x: (b[x if x == 'Jupiter' else x + '_B']['ra'], b[x if x == 'Jupiter' else x + '_B']['dec']) for x in NEEDED}
    return _cache[m]


B0 = eng(0.0)


def spos(x, m):
    e = eng(m)
    return ((P[x][0] + wrap(e[x][0] - B0[x][0])) % 360.0, P[x][1] + e[x][1] - B0[x][1])


def geo_val(g, m):
    if g[0] == 'd':
        _, a, b, pl = g
        return dist_pos(spos(a, m), spos(b, m), pl)
    _, x, y, pl, xbig = g
    dx, dy = dist_pos(spos('Jupiter', m), spos(x, m), pl), dist_pos(spos('Jupiter', m), spos(y, m), pl)
    if not dx or not dy:
        return None
    return dx / dy if xbig else dy / dx


GRID = sorted([m * s for s in (1, -1) for m in range(10, 1441, 10)] + [h * 60 * s for s in (1, -1) for h in range(25, 8761)], key=abs)


def real_time(e):
    tv = e['tv']
    f = lambda m: (lambda v: None if v is None else v - tv)(geo_val(e['geo'], m))
    f0 = f(0.0)
    last = {1: (0.0, f0), -1: (0.0, f0)}
    for m in GRID:
        side = 1 if m > 0 else -1
        v = f(float(m))
        if v is None:
            continue
        pm, pv = last[side]
        if (pv <= 0) != (v <= 0):
            lo, hi, flo = pm, float(m), pv
            while abs(hi - lo) > 0.01:
                mid = (lo + hi) / 2
                vm = f(mid)
                if (flo <= 0) == (vm <= 0):
                    lo, flo = mid, vm
                else:
                    hi = mid
            return (lo + hi) / 2
        last[side] = (float(m), v)
    return None


def from_text(t):
    if abs(t) > 50 * 525960:
        return f"more than 50 years {'away' if t >= 0 else 'ago'}"
    return f'{t:+.1f} min' if abs(t) < 1440 else f'{t / 1440:+.2f} days'


def check_event(tab, r, e, real):
    where = f'{tab} {e["rel"]} {e["plane"]} {e["kind"]}'
    srcs_ok = r[3] == e['src'] or (e['src'] != 'SKY' and r[3] in ('SKY', 'SKY EQ', 'SKY PAIRS'))
    if not srcs_ok:
        mis(f'{where} source', r[3], e['src'])
    if r[4] != e['rel']:
        mis(f'{where} rel', r[4], e['rel'])
    if r[5] != e['plane'] and not (e['geo'][0] == 'd' and {r[5], e['plane']} <= {'Dec', 'Equator'}):
        mis(f'{where} plane', r[5], e['plane'])
    if r[7] != e['target']:
        mis(f'{where} target', r[7], e['target'])
    if not eq(r[8], e['tv']) and not abs(float(r[8]) - e['tv']) < 1e-6:
        mis(f'{where} target value', r[8], e['tv'])
    if not eq(r[9], round(e['v0'], 6)):
        mis(f'{where} value', r[9], round(e['v0'], 6))
    sc = None if e['score'] is None else round(e['score'], 2)
    if not eq(r[10], sc):
        mis(f'{where} score', r[10], sc)
    t_lin = e['t']
    if tab == 'TIMELINE':
        if r[1] != clock(t_lin) or not eq(r[2], round(t_lin, 1)):
            mis(f'{where} time', (r[1], r[2]), (clock(t_lin), round(t_lin, 1)))
        aps = 'applying' if t_lin >= 0 else 'separating'
    else:
        if abs(t_lin) > 60:
            tr = real
            if tr is None:
                if r[1] != 'not within 1 year' or r[2] != 'not within 1 year' or r[13] is not None:
                    mis(f'{where} real (none found)', (r[1], r[2], r[13]), 'not within 1 year')
                aps = 'applying' if t_lin >= 0 else 'separating'
            else:
                if r[13] is None or abs(r[13] - tr) > 1.0:
                    mis(f'{where} real time', (r[1], r[13]), (clock(tr), round(tr, 2)))
                elif r[2] != from_text(r[13]) or r[1] not in (clock(tr - 1), clock(tr), clock(tr + 1)):
                    mis(f'{where} real clock text', (r[1], r[2]), (clock(tr), from_text(tr)))
                aps = 'applying' if tr >= 0 else 'separating'
        else:
            if r[1] != clock(t_lin) or r[2] != from_text(t_lin) or not eq(r[13], round(t_lin, 1)):
                mis(f'{where} time', (r[1], r[2], r[13]), (clock(t_lin), from_text(t_lin), round(t_lin, 1)))
            aps = 'applying' if t_lin >= 0 else 'separating'
        lin = f'{clock(t_lin)} ({from_text(t_lin)})'
        if r[14] != lin:
            mis(f'{where} linear estimate', r[14], lin)
    if r[11] != aps:
        mis(f'{where} applying / separating', r[11], aps)
    note = r[12] or ''
    if e['out'] and 'outside at the off' not in note:
        mis(f'{where} note', note, 'outside at the off')
    if r[3] != e['src'] and e['src'] not in note:
        mis(f'{where} note also', note, f'also {e["src"]}')
    return aps


SO = {s for s in NEW_STARS}
real_cache = {}
for tab, keep in (('TIMELINE', lambda e: -30 <= e['t'] <= 60), ('LONG TIMELINE', lambda e: e['score'] is not None and e['score'] >= 80)):
    exp = {k: e for k, e in cands.items() if keep(e)}
    sheet = [r for k, r in TLA[tab] if k == 'EV' and star_only(r)]
    sheet_by = {(r[4], r[6], r[7]): r for r in sheet}
    exp_by = {(e['rel'], e['kind'], e['target']): e for e in exp.values()}
    print(f'{tab}: star-only events on the sheet {len(sheet)} (new-star {sum(is_new(r) for r in sheet)}), own {len(exp_by)} '
          f'(new-star {sum(bool(NEWRX.search(e["rel"])) for e in exp_by.values())}); from SKY block new-star: '
          f'{sum(1 for e in exp_by.values() if e["src"] == "SKY" and NEWRX.search(e["rel"]))}')
    for k in exp_by.keys() - sheet_by.keys():
        mis(f'{tab} missing star event', k, 'expected')
    for k in sheet_by.keys() - exp_by.keys():
        mis(f'{tab} extra star event', k, 'not expected')
    for k in exp_by.keys() & sheet_by.keys():
        e = exp_by[k]
        real = None
        if tab == 'LONG TIMELINE' and abs(e['t']) > 60:
            if k not in real_cache:
                real_cache[k] = real_time(e)
            real = real_cache[k]
            print(f'  real {e["rel"]} {e["plane"]} {e["target"][:28]}: linear {e["t"]:+.1f}, own real '
                  f'{"not within 1 year" if real is None else f"{real:+.2f} ({clock(real)})"}; sheet {sheet_by[k][1]} {sheet_by[k][13]}')
        check_event(tab, sheet_by[k], e, real)

# titles / sections / order on the after sheet
for tab in ('TIMELINE', 'LONG TIMELINE'):
    evs = [r for k, r in TLA[tab] if k == 'EV']
    if tab == 'TIMELINE':
        b4 = sum(1 for r in evs if r[2] < 0); f5 = sum(1 for r in evs if 0 <= r[2] <= 5); af = len(evs) - b4 - f5
        txt = f'{len(evs)} events, {b4} before the off, {f5} in the first 5 min, {af} after'
        if txt not in TTA[tab]:
            mis('TIMELINE title', TTA[tab][-90:], txt)
        ts = [r[2] for k, r in TLA[tab] if k == 'EV' or True]
        tt = [r[2] for k, r in TLA[tab]]
        if any(tt[i] < tt[i - 1] for i in range(1, len(tt)) if tt[i] is not None and tt[i - 1] is not None):
            mis('TIMELINE order', 'not sorted', 'sorted by time')
    else:
        sec, secs = None, {}
        for k, r in TLA[tab]:
            if k == 'MARK':
                sec = 'SEP' if 'SEPARATING' in str(r[3]) else 'APP'
                m = re.search(r'(\d+) events', str(r[3])); secs[sec] = [int(m.group(1)), []]
                continue
            secs[sec][1].append(r)
            want = 'separating' if sec == 'SEP' else 'applying'
            if r[11] != want:
                mis(f'LONG section {r[4]}', r[11], want)
        for s, (n, rs) in secs.items():
            if n != len(rs):
                mis(f'LONG {s} count', n, len(rs))
            sc = [r[10] for r in rs]
            if any(sc[i] > sc[i - 1] for i in range(1, len(sc))):
                mis(f'LONG {s} order by score', sc, 'descending')
        print(f'LONG sections: separating {secs["SEP"][0]}, applying {secs["APP"][0]}')

print()
print('MISMATCHES:', len(bad))
for b in bad[:200]:
    print(' ', b)

# ---------- extra: grid points evaluated, and the "not within 1 year" events scanned hourly over +-1 year (min / max of the value)
print('engine instants cached:', len(_cache))
for k, real in real_cache.items():
    if real is None:
        e = next(x for x in cands.values() if (x['rel'], x['kind'], x['target']) == k)
        vals = [geo_val(e['geo'], float(m)) for m in range(-525600, 525601, 60)]
        print(f'  hourly scan {k[0]} {e["plane"]} target {e["tv"]:.6f}: min {min(vals):.6f} max {max(vals):.6f} '
              f'-> crosses: {min(vals) <= e["tv"] <= max(vals)}')
