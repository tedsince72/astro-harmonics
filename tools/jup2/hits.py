"""hits.py - JR v2 measures A-E (design section 5), every hit with numbers, family, level, offset, t, a/s.
Points are 'S Mars', 'H Jupiter', 'J Ketu', 'S equator'. S = race sky, H = horse natal, J = jockey natal."""
import itertools, math
from core import *

STRUCK = ('strict', 'exact-in-race', 'exact-pre-off')     # levels that count as a hit for joins / combined hits


class Race:
    def __init__(self, sky, rates, dur_min):
        self.S0 = sky
        self.S5 = {b: None if rates.get(b) is None else
                   ((p[0] + rates[b][0] * 5.0) % 360.0, p[1] + rates[b][1] * 5.0, p[2]) for b, p in sky.items()}
        self.dur = dur_min


class Ctx:
    def __init__(self, race, runner=None):
        self.race = race
        self.H = runner['H'] if runner else {}
        self.J = runner['J'] if runner else {}

    def pos(self, pt, st):
        c, b = pt.split(' ', 1)
        if c == 'S':
            return self.race.S0[b] if st == 0 else self.race.S5[b]
        return (self.H if c == 'H' else self.J)[b]

    def series(self, fn, pts):
        v0 = fn(*[self.pos(p, 0) for p in pts])
        p5 = [self.pos(p, 5) for p in pts]
        v5 = None if any(x is None for x in p5) or not any(p.startswith('S ') for p in pts) else fn(*p5)
        return v0, v5


def sky_leg(pts):
    return any(p.startswith('S ') for p in pts)


def mk(m, pts, plane, value, h, desc, **kw):
    d = {'m': m, 'pts': list(pts), 'plane': plane, 'value': value, 'desc': desc, 'flags': []}
    d.update(h); d.update(kw)
    d['key'] = f"{m}|{'|'.join(pts)}|{plane}|{h['target']}"
    return d


def dist_hits(ctx, m, a, b, plane, kind='dist', **kw):
    if plane == 'Equator':                                   # movement in the Equator plane: | |Dec a| - |Dec b| |
        fn = lambda p, q: abs(abs(p[1]) - abs(q[1]))
    elif b.endswith(' equator'):
        fn = lambda p, q: abs(p[1])
    else:
        fn = lambda p, q: plane_value(p, q, plane)
    v0, v5 = ctx.series(fn, [a, b])
    return [mk(m, [a, b], plane, v0, h, f'{a} – {b}', v5=v5, **kw) for h in classify(v0, v5, kind, ctx.race.dur)]


def ratio_hits(ctx, m, num, den, plane, kind='ratio', label=''):
    """num, den = (fn, pts). value = larger / smaller."""
    pts = list(dict.fromkeys(num[1] + den[1]))
    n0, n5 = ctx.series(num[0], num[1]); d0, d5 = ctx.series(den[0], den[1])
    if not sky_leg(num[1]):
        n5 = n0                                           # natal values do not move
    if not sky_leg(den[1]):
        d5 = d0
    if min(n0, d0) < RATIO_MIN:
        return []
    flip = n0 < d0
    v0 = (d0 / n0) if flip else (n0 / d0)
    v5 = None
    if sky_leg(pts) and n5 is not None and d5 is not None and min(n5, d5) > 0:
        v5 = (d5 / n5) if flip else (n5 / d5)
    elif sky_leg(pts):
        v5 = None
    out = []
    for h in classify(v0, v5, kind, ctx.race.dur):
        out.append(mk(m, pts, plane, v0, h, label + (' (inverted)' if flip else ''), num=n0, den=d0, flip=flip, v5=v5))
    return out


def P(pt_a, pt_b, plane):
    if pt_b.endswith(' equator'):
        return (lambda p, q: abs(p[1]), [pt_a, pt_b])
    return (lambda p, q, pl=plane: plane_value(p, q, pl), [pt_a, pt_b])


def EQ(pt):
    return (lambda p: abs(p[1]), [pt])


# ---------------- midpoints (E)
def sep_signed(m, mid, plane):
    if plane == 'RA':
        return (m - mid + 180.0) % 360.0 - 180.0
    return m - mid


def mid_of(a, b, plane):
    if plane == 'RA':
        d = (b - a + 180.0) % 360.0 - 180.0
        return (a + d / 2) % 360.0, abs(d)
    return (a + b) / 2, abs(b - a)


def mid_hits(ctx, m, ends, middle, plane, dur):
    ix = 0 if plane == 'RA' else 1
    def off(*ps):
        e1, e2, mm = ps
        mid, span = mid_of(e1[ix], e2[ix], plane)
        return sep_signed(mm[ix], mid, plane), span
    pts = list(ends) + [middle]
    p0 = [ctx.pos(p, 0) for p in pts]
    o0, span = off(*p0)
    if not (0.5 <= span <= 60):
        return []
    p5 = [ctx.pos(p, 5) for p in pts]
    o5 = None if (not sky_leg(pts) or any(x is None for x in p5)) else off(*p5)[0]
    rate = None if o5 is None else (o5 - o0) / 5.0
    eta = None if not rate else -o0 / rate
    if abs(o0) <= MID[0]:
        lev = 'strict'
    elif eta is not None and 0 < eta <= dur:
        lev = 'exact-in-race'
    elif eta is not None and -PRE_OFF_MIN <= eta < 0:
        lev = 'exact-pre-off'
    elif abs(o0) <= MID[1]:
        lev = 'near'
    else:
        return []
    h = {'target': 'midpoint', 'target_value': 0.0, 'family': 'midpoint', 'level': lev, 'offset': o0, 'unit': 'deg',
         'tol': MID[0], 't': abs(o0) / MID[0], 'rate': rate, 'eta': eta,
         'as': 'n/a' if rate is None else ('applying' if -o0 * rate > 0 else 'separating')}
    wide = ', wide' if span >= 20 else ''
    return [mk(m, [middle] + list(ends), plane, span, h, f'{middle} at the midpoint of {ends[0]} and {ends[1]} (span {span:.4f}{wide})')]


def struck(hs):
    return [h for h in hs if h['level'] in STRUCK]


def combine(m, parts, desc):
    """combined hit (parts are strict / exact-in-race / exact-pre-off only - 'on a number'): weaker level, largest t."""
    lev = weaker([p['level'] for p in parts])
    pts = list(dict.fromkeys(x for p in parts for x in p['pts']))
    h = {'target': ' + '.join(f"{p['plane']} {p['target']}" for p in parts), 'target_value': None, 'family': '+'.join(p['family'] for p in parts),
         'level': lev, 'offset': None, 'unit': '', 'tol': None, 't': max(p['t'] for p in parts), 'rate': None,
         'eta': None, 'as': ', '.join(p['as'] for p in parts)}
    d = {'m': m, 'pts': pts, 'plane': '+'.join(p['plane'] for p in parts), 'value': None, 'desc': desc,
         'flags': sorted({f for p in parts for f in p['flags']}), 'parts': parts}
    d.update(h)
    d['key'] = f"{m}|{desc}|{h['target']}"
    return d


# ---------------- A: the race's own sky
def sky_hits(race):
    ctx = Ctx(race); out = []
    SJ = 'S Jupiter'
    pts = [b for b in race.S0 if b != 'Jupiter']
    for X in pts:
        x = f'S {X}'
        if X == EQUATOR:
            out += dist_hits(ctx, 'A1', SJ, x, 'Dec', 'equator')
            continue
        for pl in planes_for(X):
            out += dist_hits(ctx, 'A1', SJ, x, pl)
    for X in [b for b in SKY_BODIES if b != 'Jupiter'] + ROYAL:
        out += ratio_hits(ctx, 'A2', P(SJ, f'S {X}', 'Dec'), P(SJ, 'S equator', 'Dec'), 'Dec',
                          label=f'(S Jupiter–S {X}) / (S Jupiter–equator)')
    for A, B in itertools.combinations(ROYAL, 2):
        for pl in PLANES:
            out += ratio_hits(ctx, 'A2', P(SJ, f'S {A}', pl), P(SJ, f'S {B}', pl), pl,
                              label=f'(S Jupiter–S {A}) / (S Jupiter–S {B})')
    return out


# ---------------- per runner: B, C, D, E
def runner_hits(race, R):
    ctx = Ctx(race, R); out = []
    SJ = 'S Jupiter'
    other = {'H': 'J', 'J': 'H'}
    nat_bodies = [b for b in NATAL_BODIES if b != 'Jupiter']

    # B1 natal Jupiter to its own chart
    for C in 'HJ':
        CJ = f'{C} Jupiter'
        for X in [b for b in (R[C]) if b != 'Jupiter']:
            x = f'{C} {X}'
            if X == EQUATOR:
                out += dist_hits(ctx, 'B1', CJ, x, 'Dec', 'equator'); continue
            for pl in planes_for(X):
                out += dist_hits(ctx, 'B1', CJ, x, pl, flags_star=(R[C][X][2] == 'star'))
    # B2 apex ratios
    for C in 'HJ':
        CJ, OJ = f'{C} Jupiter', f'{other[C]} Jupiter'
        for X in nat_bodies + ROYAL:
            out += ratio_hits(ctx, 'B2', P(CJ, f'{C} {X}', 'Dec'), P(CJ, f'{C} equator', 'Dec'), 'Dec',
                              label=f'({CJ}–{C} {X}) / ({CJ}–equator)')
            for pl in planes_for(X):
                out += ratio_hits(ctx, 'B2', P(CJ, f'{C} {X}', pl), P(CJ, OJ, pl), pl,
                                  label=f'({CJ}–{C} {X}) / ({CJ}–{OJ})')
        for A, B in itertools.combinations(ROYAL, 2):
            for pl in PLANES:
                out += ratio_hits(ctx, 'B2', P(CJ, f'{C} {A}', pl), P(CJ, f'{C} {B}', pl), pl,
                                  label=f'({CJ}–{C} {A}) / ({CJ}–{C} {B})')
    # B3 cross: H Jupiter to J bodies, J Jupiter to H bodies (H Jupiter – J Jupiter once)
    cross = [('H Jupiter', f'J {X}') for X in NATAL_BODIES] + [(f'H {X}', 'J Jupiter') for X in nat_bodies]
    links = {}
    for a, b in cross:
        bx = b.split(' ', 1)[1] if a == 'H Jupiter' else a.split(' ', 1)[1]
        pls = planes_for(bx)
        for pl in pls:
            out += dist_hits(ctx, 'B3', a, b, pl)
        pa, pb = ctx.pos(a, 0), ctx.pos(b, 0)
        ra = wrap_ra(pa[0], pb[0]) if 'RA' in pls else 999.0
        de = abs(pa[1] - pb[1])
        lev = contact_level(ra, de)
        if lev:
            t = min(ra / CLOSE[0], de / CLOSE[1])
            h = {'target': 'contact', 'target_value': None, 'family': 'contact', 'level': lev, 'offset': min(ra, de), 'unit': 'deg',
                 'tol': None, 't': t, 'rate': None, 'eta': None, 'as': 'n/a (natal)'}
            d = mk('B3', [a, b], 'RA/Dec', None, h, f'cross link {a} – {b} RA {ra if ra < 999 else float("nan"):.4f} Dec {de:.4f}', RA=ra, Dec=de)
            out.append(d)
            links[(a, b)] = d

    # C1 sky Jupiter to each natal point (bodies and stars; natal Jupiter is C3)
    c1 = {}
    for C in 'HJ':
        for X in [b for b in R[C] if b not in ('Jupiter', EQUATOR)]:
            x = f'{C} {X}'
            for pl in planes_for(X):
                hs = dist_hits(ctx, 'C1', SJ, x, pl)
                for h in hs:
                    if R[C][X][2] == 'star':
                        h['flags'].append('copy')
                out += hs
                c1.setdefault(x, []).extend(hs)
    # C3 movement sky Jupiter vs natal Jupiter, all planes + Equator
    for C in 'HJ':
        CJ = f'{C} Jupiter'
        for pl in PLANES + ('Equator',):
            hs = dist_hits(ctx, 'C3', SJ, CJ, pl, 'move')
            out += hs
            c1.setdefault(CJ, []).extend(hs)          # sky Jupiter on natal Jupiter counts as a strike on that end (C1 both ends)
    # C2 each sky body (Moon included) to natal Jupiter
    c2 = {}
    for C in 'HJ':
        CJ = f'{C} Jupiter'
        for Z in [b for b in SKY_BODIES if b != 'Jupiter']:
            for pl in planes_for(Z):
                hs = dist_hits(ctx, 'C2', f'S {Z}', CJ, pl)
                out += hs
                c2.setdefault(CJ, {}).setdefault(Z, []).extend(hs)
    # C1 both ends: natal pairs inside one chart (strict number in any plane or close contact) and close H–J cross links
    pairs = []
    for C in 'HJ':
        bodies = [b for b in NATAL_BODIES if b in R[C]]
        for X, Y in itertools.combinations(bodies, 2):
            if X in ('Rahu', 'Ketu') and Y in ('Rahu', 'Ketu'):
                continue
            px, py = R[C][X], R[C][Y]
            pls = planes_for(X, Y)
            ra = wrap_ra(px[0], py[0]) if 'RA' in pls else 999.0
            de = abs(px[1] - py[1])
            why = 'close' if contact_level(ra, de) == 'strict' else ''
            if not why:
                for pl in pls:
                    v = plane_value(px, py, pl)
                    if any(h['level'] == 'strict' for h in classify(v, None, 'dist', 0)):
                        why = f'{pl} number'; break
            if why:
                pairs.append((f'{C} {X}', f'{C} {Y}', why))
    for X in NATAL_BODIES:
        for Y in NATAL_BODIES:
            px, py = R['H'][X], R['J'][Y]
            pls = planes_for(X, Y)
            ra = wrap_ra(px[0], py[0]) if 'RA' in pls else 999.0
            if contact_level(ra, abs(px[1] - py[1])) == 'strict':
                pairs.append((f'H {X}', f'J {Y}', 'cross link close'))
    for a, b, why in pairs:
        ha, hb = struck(c1.get(a, [])), struck(c1.get(b, []))
        if ha and hb:
            for x in ha:
                for y in hb:
                    out.append(combine('C1b', [x, y], f'S Jupiter strikes both ends of {a} – {b} ({why})'))
    # C2 pairs of sky bodies on the same natal Jupiter
    for CJ, byZ in c2.items():
        Zs = sorted(z for z in byZ if struck(byZ[z]))
        for z1, z2 in itertools.combinations(Zs, 2):
            for x in struck(byZ[z1]):
                for y in struck(byZ[z2]):
                    out.append(combine('C2b', [x, y], f'S {z1} and S {z2} both on {CJ}'))
    # C4 RA AND Dec together, a Jupiter at one end
    cands = [(SJ, p, c1.get(p, [])) for p in c1] + [(f'S {Z}', CJ, hs) for CJ, byZ in c2.items() for Z, hs in byZ.items()]
    for z, y, hs in cands:
        ras = [h for h in struck(hs) if h['plane'] == 'RA']; des = [h for h in struck(hs) if h['plane'] == 'Dec']
        for x in ras:
            for w in des:
                out.append(combine('C4', [x, w], f'{z} on {y} in RA AND Dec'))
    # C5 partner strike: sky Jupiter on a natal body that is cross-linked (close) to the other chart's Jupiter
    for (a, b), link in links.items():
        if link['level'] != 'strict':       # close contact only (design: cross-linked = close)
            continue
        y = b if a == 'H Jupiter' else a                # the non-Jupiter end (or the other Jupiter for H Jupiter–J Jupiter)
        if a == 'H Jupiter' and b == 'J Jupiter':
            ends = ['H Jupiter', 'J Jupiter']
        else:
            ends = [y]
        for e in ends:
            for h in struck(c1.get(e, [])):
                out.append(combine('C5', [link, h], f'partner strike: S Jupiter on {e}, cross-linked to the other Jupiter ({a} – {b})'))

    # D1 / D2 same relationship ratios
    for C in 'HJ':
        CJ = f'{C} Jupiter'
        for X in nat_bodies:
            for pl in planes_for(X):
                out += ratio_hits(ctx, 'D1', P(SJ, f'S {X}', pl), P(CJ, f'{C} {X}', pl), pl,
                                  label=f'(S Jupiter–S {X}) / ({CJ}–{C} {X})')
                out += ratio_hits(ctx, 'D2', P(SJ, f'{C} {X}', pl), P(CJ, f'{C} {X}', pl), pl,
                                  label=f'(S Jupiter–{C} {X}) / ({CJ}–{C} {X})')
    # D3 Equator ratios of the three Jupiters (+ golden section, reported on the same line)
    for a, b in (('S', 'H'), ('S', 'J'), ('H', 'J')):
        A, B = f'{a} Jupiter', f'{b} Jupiter'
        hs = ratio_hits(ctx, 'D3', EQ(A), EQ(B), 'Equator', 'eqratio', label=f'|Dec| {A} / |Dec| {B}')
        for h in hs:
            pa, pb = ctx.pos(A, 0), ctx.pos(B, 0)
            if h['family'] == 'golden' and h['target'].split()[0] in ('1.618', '2.618') and pa[1] * pb[1] > 0:
                small, big = (A, B) if abs(pa[1]) < abs(pb[1]) else (B, A)
                part = 'golden section (1/phi)' if h['target'].startswith('1.618') else 'golden section (1/phi^2)'
                h['desc'] += f'; {part}: {small} between the equator and {big}, same hemisphere'
        out += hs

    # E midpoints, RA and Dec separately
    for X in NATAL_BODIES:
        for pl in [p for p in ('RA', 'Dec') if p in planes_for(X)]:
            tri = [SJ, f'H {X}', f'J {X}']
            for i in range(3):
                mdl = tri[i]; ends = [t for t in tri if t != mdl]
                out += mid_hits(ctx, 'E1', ends, mdl, pl, race.dur)
    for Z in [b for b in SKY_BODIES if b != 'Jupiter']:
        for pl in [p for p in ('RA', 'Dec') if p in planes_for(Z)]:
            tri = [f'S {Z}', 'H Jupiter', 'J Jupiter']
            for i in range(3):
                mdl = tri[i]; ends = [t for t in tri if t != mdl]
                out += mid_hits(ctx, 'E2', ends, mdl, pl, race.dur)
    for C in 'HJ':
        O = other[C]
        for Y in NATAL_BODIES:
            for pl in [p for p in ('RA', 'Dec') if p in planes_for(Y)]:
                out += mid_hits(ctx, 'E3', [f'{C} Jupiter', SJ], f'{O} {Y}', pl, race.dur)
    return out
