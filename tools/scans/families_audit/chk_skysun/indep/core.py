#!/usr/bin/env python3
"""Independent checker core (1 Nov 2026): rebuild the SKY <centre> sheets of jupiter_tables from POSITIONS with own code.
Only tools/families.py is imported (Eddie's family definitions). Does NOT import jupiter_tables."""
import math, os, sys, datetime as dt, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import families as F  # noqa: E402
import openpyxl  # noqa: E402

ROYAL = ['Aldebaran', 'Regulus', 'Antares', 'Fomalhaut']
BODY_ORDER = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas',
              'Juno', 'Vesta', 'Rahu', 'Ketu', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Orcus', 'Quaoar', 'Gonggong', 'Transpluto', 'Moon']
TOLMID = {'RA': 0.5, 'Dec': 0.15, 'Equator': 0.15}
CONJT = {'RA': 1.5, 'Dec': 0.3, 'Equator': 0.3}
FAMTXT = {'whole': 'whole', 'golden': 'golden', 'phi power': 'phi power', 'ninth': 'ninth', 'sqrt2': 'sqrt2', 'silver': 'silver',
          'conj': 'conj'}


class Pos:
    def __init__(self, wb):
        ws = wb['POSITIONS']
        h = ws.cell(1, 1).value
        i = h.index(' off ') + 5
        self.off = dt.datetime.strptime(h[i:i + 16], '%Y-%m-%d %H:%M')
        self.p = {}            # name -> (ra, dec, rra, rdec, kind)
        self.first_stars, self.new_stars = [], []
        second = False
        for r in range(5, ws.max_row + 1):
            a = ws.cell(r, 1).value
            if isinstance(a, str) and a.startswith('T1 / T2 / T24 only'):
                second = True
                continue
            if a != 'SKY':
                continue
            nm, kind = ws.cell(r, 4).value, ws.cell(r, 5).value
            v = [float(ws.cell(r, c).value or 0) for c in (6, 7, 8, 9)]
            self.p[nm] = (v[0], v[1], v[2], v[3], kind)
            if kind == 'star':
                (self.new_stars if second else self.first_stars).append(nm)

    def at(self, nm, t):
        ra, dec, rr, rd, k = self.p[nm]
        return ((ra + rr * t) % 360.0, dec + rd * t)


def dist(pos, a, b, plane, t):
    ra1, d1 = pos.at(a, t)
    ra2, d2 = pos.at(b, t)
    if plane == 'RA':
        x = abs(ra1 - ra2) % 360.0
        return 360.0 - x if x > 180 else x
    if plane == 'Dec':
        return abs(d1 - d2)
    return abs(abs(d1) - abs(d2))


def straddle(pos, pts):
    s = [pos.p[n][1] >= 0 for n in pts]       # sign at the off
    return not (all(s) or not any(s))


# ---------- formatting
def clock(pos, t):
    when = pos.off + dt.timedelta(minutes=t)
    if when.date() == pos.off.date():
        return when.strftime('%H:%M')
    return when.strftime('%d %b %Y %H:%M')


def exact_t(v0, v5, tv):
    if v5 == v0:
        return None
    return (tv - v0) / (v5 - v0) * 5.0


def timing_text(pos, t):
    if t is None:
        return None
    if abs(t) > 50 * 365.25 * 1440:
        return ('applying, exact more than 50 years away' if t > 0 else 'separating, exact more than 50 years ago')
    if t >= 0:
        return f'applying, exact {clock(pos, t)} (in {t:.1f} min)'
    return f'separating, exact {clock(pos, t)} ({-t:.1f} min ago)'


def g3(x):
    s = f'{x:.3g}'
    return s


def target_text(v, plane, kind='deg'):
    """-> (text, off, score or None, best dict or None)"""
    ev = F.evaluate(v, plane if plane != 'Equator' else 'Equator', kind)
    if ev:
        b = ev[0]
        if kind == 'deg':
            return f"{b['target']} ({FAMTXT[b['family']]})", b['off'], b['score'], b, ev
        return f"{b['target']} · {b['name']} · {b['group']}", b['off'], b['score'], b, ev
    o = F.outside(v, None, kind)
    if o is None:
        return None, None, None, None, []
    if kind == 'deg':
        if o.get('digit'):
            return f"{o['target']} {FAMTXT[o['family']]} — not a 4-digit match ({o['off']:+.5f})", o['off'], None, o, []
        return f"{o['target']} ({FAMTXT[o['family']]}) — outside ±{g3(o['tol'])}", o['off'], None, o, []
    tol = o['tol']
    tt = f'±{g3(tol)} %' if o['pct'] else f'±{g3(tol)}'
    return f"{o['target']} · {o['name']} · {o['group']} — outside {tt}", o['off'], None, o, []


def off_text(b):
    if b.get('pct'):
        return f"{b['off']:+.5f}%"
    return f"{b['off']:+.5f}"


# ---------- SKY block
def sky_points(pos, centre, star_order):
    bodies = [b for b in BODY_ORDER if b in pos.p and b not in ('Ketu',)]
    pts = [b for b in bodies if b != centre] + [s for s in star_order] + (['Ketu'] if 'Ketu' in pos.p and centre != 'Ketu' else [])
    return pts + ['equator']


def sky_cell(pos, centre, x, plane):
    if x == 'equator':
        if plane == 'RA':
            return None
        v0 = abs(pos.at(centre, 0)[1]); v5 = abs(pos.at(centre, 5)[1])
    else:
        v0 = dist(pos, centre, x, plane, 0); v5 = dist(pos, centre, x, plane, 5)
    txt, off, sc, b, ev = target_text(v0, plane)
    d = {'v0': v0, 'v5': v5, 'txt': txt, 'off': off, 'score': sc, 'b': b, 'ev': ev}
    if sc is not None:
        t = exact_t(v0, v5, b['tv'])
        d['t'] = t
        d['timing'] = timing_text(pos, t)
        d['arrow'] = '-> toward' if abs(v5 - b['tv']) < abs(v0 - b['tv']) else '<- away'
        d['also'] = '; '.join(f"{e['target']} ({FAMTXT[e['family']]}) {e['off']:+.5f} [{e['score']:.2f}]" for e in ev[1:])
    else:
        d['t'] = exact_t(v0, v5, b['tv']) if b else None
    return d


# ---------- pair rows
def mid_geom(pos, c, x, y, plane, d1, d2):
    clos = min(d1, d2) / max(d1, d2) * 100 if max(d1, d2) > 0 else 0.0
    if plane == 'RA':
        a, b, cc = pos.at(x, 0)[0], pos.at(y, 0)[0], pos.at(c, 0)[0]
        diff = ((b - a + 540) % 360) - 180
        near = (a + diff / 2) % 360
        o1 = ((cc - near + 540) % 360) - 180
        o2 = ((cc - (near + 180) + 540) % 360) - 180
        off, lab = (o1, 'near') if abs(o1) <= abs(o2) else (o2, 'far')
    elif plane == 'Dec':
        off, lab = pos.at(c, 0)[1] - (pos.at(x, 0)[1] + pos.at(y, 0)[1]) / 2, ''
    else:
        off, lab = abs(pos.at(c, 0)[1]) - (abs(pos.at(x, 0)[1]) + abs(pos.at(y, 0)[1])) / 2, ''
    tol = TOLMID[plane]
    hit = clos >= 90 and abs(off) < tol
    rh = (10 * (10 - (100 - clos)) / 10) ** 2 * 0.5 if clos >= 90 else None
    dh = (10 * (tol - abs(off)) / tol) ** 2 * 0.5 if abs(off) < tol else None
    return {'clos': clos, 'off': off, 'lab': lab, 'hit': hit, 'rh': rh if hit else None, 'dh': dh if hit else None,
            'total': (rh + dh) if hit else None}


def leg(pos, a, b, plane, centre_leg=True):
    v0 = dist(pos, a, b, plane, 0); v5 = dist(pos, a, b, plane, 5)
    ev = F.evaluate(v0, plane)
    bb = ev[0] if ev else None
    out = {'v0': v0, 'v5': v5, 'b': bb}
    if bb:
        t = exact_t(v0, v5, bb['tv'])
        out['t'] = t
        out['txt'] = f"→ {bb['target']} ({FAMTXT[bb['family']]}, {bb['score']:.2f}) · {timing_text(pos, t)}"
    else:
        out['txt'] = 'no family'
    return out


def pair_row(pos, c, x, y, plane, block):
    L1 = leg(pos, c, x, plane); L2 = leg(pos, c, y, plane); L3 = leg(pos, x, y, plane)
    d1, d2, d3 = L1['v0'], L2['v0'], L3['v0']
    together = d3 < CONJT[plane]
    if min(d1, d2) <= 0:
        return None
    big1 = d1 >= d2
    q0 = d1 / d2 if big1 else d2 / d1
    q5 = (L1['v5'] / L2['v5']) if big1 else (L2['v5'] / L1['v5'])
    ev = F.evaluate(q0, kind='ratio')
    r = {'c': c, 'x': x, 'y': y, 'plane': plane, 'block': block, 'L': (L1, L2, L3), 'q0': q0, 'q5': q5, 'together': together}
    if ev:
        b = ev[0]
        r['rb'] = b; r['rscore'] = b['score']
        r['rtxt'] = f"{b['target']} · {b['name']} · {b['group']}"
        r['areas'] = {F.area(e['target']) for e in ev}
    else:
        o = F.outside(q0, None, 'ratio')
        r['rb'] = o; r['rscore'] = None
        tt = f"±{g3(o['tol'])} %" if o['pct'] else f"±{g3(o['tol'])}"
        r['rtxt'] = f"{o['target']} · {o['name']} · {o['group']} — outside {tt}"
        r['areas'] = set()
    r['rt'] = exact_t(q0, q5, r['rb']['tv'])
    r['rtiming'] = timing_text(pos, r['rt'])
    r['ut'] = exact_t(q0, q5, 1.0)       # unison timing (midpoint event)
    s = d1 + d2
    r['between'] = 'between' if abs(d3 - s) <= 0.01 * s else 'far side'
    r['mid'] = mid_geom(pos, c, x, y, plane, d1, d2)
    if together:
        r['rscore'] = None; r['mid'] = dict(r['mid'], hit=False, total=None, rh=None, dh=None)
        r['areas'] = set()
    if r['mid']['hit']:
        r['areas'] = r['areas'] | {'A'}
    r['area'] = next((a for a in ('A', 'P', 'B') if a in r['areas']), None)
    r['key'] = max(r['rscore'] or 0.0, r['mid']['total'] or 0.0)
    r['all3'] = all(L['b'] for L in (L1, L2, L3))
    r['listed'] = (not together) and (r['area'] is not None or r['all3'])
    return r


def planes_for(pos, pts):
    out = ['RA', 'Dec']
    if straddle(pos, pts):
        out.append('Equator')
    return out


def ketu_drop(rows, rkey):
    """drop a Ketu row whose numbers equal a Rahu row (any plane) with the same other point"""
    seen = {}
    for r in rows:
        if 'Ketu' in (r['x'], r['y']):
            continue
        if 'Rahu' in (r['x'], r['y']):
            other = r['y'] if r['x'] == 'Rahu' else r['x']
            seen.setdefault(other, set()).add(rkey(r))
    out = []
    for r in rows:
        if 'Ketu' in (r['x'], r['y']):
            other = r['y'] if r['x'] == 'Ketu' else r['x']
            if rkey(r) in seen.get(other, set()):
                r['ketu_dropped'] = True
                continue
        out.append(r)
    return out


def pkey(r):
    L = r['L']
    o = [round(L[0]['v0'], 6), round(L[1]['v0'], 6)]
    if r['x'] in ('Rahu', 'Ketu'):
        o = o[::-1] if False else o
    return (tuple(sorted(o)), round(L[2]['v0'], 6))


def build(pos, centre, star_order, star_pair_order):
    bodies = [b for b in BODY_ORDER if b in pos.p and b != centre]
    out = {'centre': centre}
    out['sky'] = [(x, {pl: sky_cell(pos, centre, x, pl) for pl in ('RA', 'Dec')}) for x in sky_points(pos, centre, star_order)]
    # SKY PAIRS: body-body, body-royal
    rows = []
    for x, y in itertools.combinations(bodies, 2):
        if {x, y} == {'Rahu', 'Ketu'}:
            continue
        for pl in planes_for(pos, [centre, x, y]):
            r = pair_row(pos, centre, x, y, pl, 'S–S')
            if r: rows.append(r)
    royal_rows = []
    for x in bodies:
        for y in ROYAL:
            if y not in pos.p: continue
            for pl in planes_for(pos, [centre, x, y]):
                r = pair_row(pos, centre, x, y, pl, 'body – royal')
                if r: royal_rows.append(r)
    rows = ketu_drop(rows, pkey); royal_rows = ketu_drop(royal_rows, pkey)
    out['pairs_all'] = rows + royal_rows
    out['pairs'] = [r for r in rows + royal_rows if r['listed']]
    srows = []
    for x, y in itertools.combinations(star_pair_order, 2):
        for pl in planes_for(pos, [centre, x, y]):
            r = pair_row(pos, centre, x, y, pl, 'S–S')
            if r: srows.append(r)
    out['stars_all'] = srows
    out['stars'] = [r for r in srows if r['listed']]
    rr = []
    for x, y in itertools.combinations([s for s in ROYAL if s in pos.p], 2):
        for pl in planes_for(pos, [centre, x, y]):
            r = pair_row(pos, centre, x, y, pl, 'royal – royal')
            if r: rr.append(r)
    out['royal'] = rr + royal_rows
    # SKY EQ
    eq = []
    for x, y in itertools.combinations(bodies, 2):
        if {x, y} == {'Rahu', 'Ketu'}:
            continue
        for pl in planes_for(pos, [centre, x, y]):
            d1 = dist(pos, centre, x, pl, 0); d2 = dist(pos, centre, y, pl, 0)
            if min(d1, d2) <= 0: continue
            m = mid_geom(pos, centre, x, y, pl, d1, d2)
            d3 = dist(pos, x, y, pl, 0)
            tog = d3 < CONJT[pl]
            if m['hit']:
                r = pair_row(pos, centre, x, y, pl, 'eq')
                r['eqmid'] = m; r['eqtog'] = tog
                eq.append(r)
    # Ketu repeat across planes: same d1, d2 (rounded) with Rahu
    def ek(r):
        return tuple(sorted([round(r['L'][0]['v0'], 6), round(r['L'][1]['v0'], 6)]))
    eq = ketu_drop(eq, ek)
    out['eq'] = eq
    return out
