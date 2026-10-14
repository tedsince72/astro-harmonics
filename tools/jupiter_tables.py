#!/usr/bin/env python3
"""jupiter_tables.py INPUT [--out X.xlsx] [--off "YYYY-MM-DD HH:MM"] [--site lat,lon,elev]
Viewing tool (13 Oct 2026, Eddie): raw Jupiter tables for one race, nothing filtered.
INPUT = a race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx (TRANS, P01..Pnn, META) or a split race folder in reference/classic
(<course>_<hhmm>_<yyyymmdd>/<race>__P##.xlsx). Output: race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx next to the batch
(for a folder: in reference/classic/), unless --out.

Sheets: POSITIONS; SKY JUPITER (+ EQUIDISTANCE, 14 Oct); one sheet per runner (P01, P03, ...: tables 1-19; T17 equidistance, T18 horse | jockey side by side, T19 sky Jupiter on natal pairs); P## PAIRS (unfiltered) in a separate race_batch_<yyyymmdd>_<course>_<hhmm>_pairs.xlsx next to it + P## RATIOS; THREADS (13 Oct: hits linking each body
with Jupiter, per runner, tags and field counts - see threads_sheet); P## NUMBERS + FIELD NUMBERS (13 Oct: target numbers, x10 / /10
folded, SKY / HORSE / JOCKEY / SKY->NATAL - see numbers_sheet); FIELD 5-8, 10, 11, 12-17.
Each value (13 Oct 2026, Eddie's correction): every family of tools/families.py (Eddie's definitions, his scores from
rebuild_kit/active_vibrations.py) is scored; nearest target = the family with the highest score; the other families with a score > 0
are listed beside it ('also'); 'scaled' = best family of 10 v or v / 10 (/10 widens a tolerance 10x in degrees). Ratio values (T12-T15)
are scored against Eddie's musical interval list only (tapered tolerances, families.interval_tol): target 'interval · name · group' plus a Group column; per runner a
'P## RATIOS' sheet (RATIOS BY GROUP: grouped, tightest first) and FIELD 12-15 matrices with the group tag. Colours by score: green >= 80,
yellow 50-80, light yellow < 50. No summary totals. Outside every tolerance (13 Oct): the value cell still shows its nearest target
(by tightness: smallest offset in units of its own tolerance) and offset, e.g. '1 · unison · Perfect — outside ±1 %' / '+1.26300%', plain text. Unison (Perfect 1) counts; every unison carries its field count (runners holding
unison on the same ratio; it can come from age, e.g. Equator S/H = 1) in the 'also' column, the RATIOS sheet and FIELD 12-15.
Jupiter return (13 Oct): when S Jupiter is in conjunction (RA < 1.5 or Dec < 0.3) with a natal Jupiter, that chart's T13 starts with
'Jupiter return: S-H (S-J) Jupiter RA .. Dec ..' (information). A T12-T14 unison is greyed as 'automatic (Jupiter return)', per plane,
only when d(S Jupiter, natal Jupiter) / d(natal Jupiter, X) in that plane < 0.0015; all other unisons are genuine.
Automatic unisons are left out of every field count. A unison with 0.0015 <= d1/d2 < 0.02 is tagged 'return-assisted' (colour and field
count unchanged). RATIOS sheets show only groups with hits. T16 (13 Oct 2026, Eddie): RA-Dec crossing, Jupiter-X RA distance in one chart =
its Dec distance in another (6 orderings), +-0.02, linear score, family of the value beside it; FIELD 16.
Midpoints (T10, T11; planes RA near, RA far, Dec, Equator = |Dec| when the three are not on one side): tolerance grows with the span,
green = 0.1 % of the span, floor 0.05, cap 0.15; yellow 3x, light 9x (Eddie, 14 Oct 2026, revised). FIELD 10 and FIELD 11. Sky-leg values also at off + 5 min
(engine, as JR v3 section F) with an arrow: toward / away from the nearest target; n/a where the engine does not reproduce a point.
Points and engine from tools/jup2 (imported, not changed). Frozen readers are not changed."""
import argparse, glob, os, re, sys, itertools, math, datetime
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools', 'jup2'))
from core import (MID, ROYAL, NATAL_BODIES, SKY_BODIES, STAR_NAMES, EQUATOR, plane_value, planes_for,
                  wrap_ra)                                                     # noqa: E402
import motion                                                                  # noqa: E402
sys.path.insert(0, os.path.join(REPO, 'tools'))
import families                                                                # noqa: E402

PLANES = ('RA', 'Dec', 'Flat', 'GC')
STARS = ['Algol', 'Pleiades', 'Aldebaran', 'Capella', 'Sirius', 'Procyon', 'Regulus', 'Alkaid', 'Algorab', 'Spica', 'Arcturus',
         'Alphecca', 'Antares', 'Vega', 'Deneb Algedi', 'Fomalhaut', 'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix']
BODIES = [b for b in SKY_BODIES if b != 'Ketu']           # workbook rows (Ketu rebuilt as Rahu's mirror)
GREEN = PatternFill('solid', start_color='C6EFCE'); YELLOW = PatternFill('solid', start_color='FFEB9C')
LIGHT = PatternFill('solid', start_color='FFF8DC'); HEAD = PatternFill('solid', start_color='D9E1F2')
BOLD = Font(bold=True)
GREY = PatternFill('solid', start_color='D9D9D9')
FILL = {'green': GREEN, 'yellow': YELLOW, 'light': LIGHT, 'grey': GREY}
COLS = 9                                                   # per plane: value, +5, target, group, offset, score, arrow, also, scaled


# ---------------- reading
def read_sheet(ws):
    out, label = {}, None
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r is None or len(r) < 9 or r[1] is None or r[4] is None:
            continue
        label = label or r[0]
        out[str(r[1]).strip()] = (float(r[4]), float(r[8]))
    return label, out


def jname(lab):
    """jockey tab label '1 Oisin Murphy' -> 'Oisin Murphy' (cloth number dropped only when present)"""
    p = str(lab).split(' ', 1)
    return p[1] if len(p) == 2 and p[0].isdigit() else str(lab)


def chart(sheet, sky):
    ch = {}
    for b in BODIES:
        if b == 'Moon' and not sky:
            continue
        if b in sheet:
            ch[b] = (sheet[b][0], sheet[b][1], 'body')
    for s in STARS:
        if s + '_B' in sheet:
            ch[s] = (sheet[s + '_B'][0], sheet[s + '_B'][1], 'star')
    if 'Rahu' in ch:
        ch['Ketu'] = ((ch['Rahu'][0] + 180.0) % 360.0, -ch['Rahu'][1], 'body')
    ch[EQUATOR] = (0.0, 0.0, 'equator')
    return ch


def load_input(path):
    """-> race name, batch path, trans label, sky, runners {P##: {'name', 'H', 'J'}}"""
    path = path.rstrip('/')
    runners = {}
    if os.path.isdir(path):
        race = os.path.basename(path)
        course, hhmm, ymd = motion.race_parts(race)
        batch = os.path.join(os.path.dirname(path), f'race_batch_{ymd}_{course}_{hhmm}.xlsx')
        sky = label = None
        for f in sorted(glob.glob(f'{path}/*__P[0-9][0-9].xlsx')):
            P = re.search(r'__(P\d\d)\.xlsx$', f).group(1)
            wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
            label, t = read_sheet(wb['TRANS'])
            hl, h = read_sheet(wb['P01']); jl, j = read_sheet(wb['P02'])
            sky = sky or chart(t, True)
            runners[P] = {'name': f'{hl} / {jname(jl)}', 'H': chart(h, False), 'J': chart(j, False)}
    else:
        m = re.match(r'^race_batch_(\d{8})_(.+)_(\d{4})\.xlsx$', os.path.basename(path))
        if not m:
            sys.exit(f'not a race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx: {path}')
        ymd, course, hhmm = m.groups()
        race, batch = f'{course}_{hhmm}_{ymd}', path
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        label, t = read_sheet(wb['TRANS'])
        sky = chart(t, True)
        tabs = [s for s in wb.sheetnames if re.fullmatch(r'P\d+', s)]
        for i in range(0, len(tabs) - 1, 2):
            hl, h = read_sheet(wb[tabs[i]]); jl, j = read_sheet(wb[tabs[i + 1]])
            runners[f'P{int(tabs[i][1:]):02d}'] = {'name': f'{hl} / {jname(jl)}', 'H': chart(h, False), 'J': chart(j, False)}
    return race, batch, label, sky, runners


# ---------------- numbers
KIND = {'dist': 'deg', 'move': 'deg', 'equator': 'deg', 'ratio': 'ratio', 'eqratio': 'eqratio'}


def nearest(v, kind, plane=None):
    """-> best family (highest score) or None, the other families with a score > 0, the best scaled (x10 / /10) or None"""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None, [], None
    k = KIND[kind]
    ev = families.evaluate(v, plane if k == 'deg' else None, k)
    sc = families.scaled(v, plane if k == 'deg' else None, k)
    return (ev[0] if ev else None), ev[1:], (dict(sc[0], deg=k == 'deg') if sc else None)


def mid_tol(span):
    """midpoint tolerance grows with the span (Eddie, 14 Oct 2026, revised): green = 0.1 % of the span, floor 0.05, cap 0.15;
    yellow 3x, light 9x"""
    return min(MID_CAP, max(MID[0], 0.001 * span))


def mid_eval(v, span):
    off = v
    g = mid_tol(span)
    col = 'green' if abs(off) <= g else 'yellow' if abs(off) <= 3 * g else 'light' if abs(off) <= 9 * g else ''
    return {'target': f'midpoint · span {span:.4f} · tol ±{g:.4f}', 'tv': 0.0, 'family': 'midpoint', 'off': off, 'score': None,
            't': abs(off) / g, 'colour': col, 'pct': False, 'span': span, 'tol': g}


# ---------------- race context
class Ctx:
    def __init__(self, sky, rates):
        self.S0 = sky
        self.S5 = {b: None if rates.get(b) is None else ((p[0] + rates[b][0] * 5.0) % 360.0, p[1] + rates[b][1] * 5.0, p[2])
                   for b, p in sky.items()}

    def pos(self, R, pt, st):
        c, b = pt.split(' ', 1)
        if c == 'S':
            return self.S0[b] if st == 0 else self.S5[b]
        return R[c][b]

    def pair(self, R, a, b, pl):
        """distance a-b in plane pl at the off and at +5 (None if no sky leg or rate n/a)."""
        if pl not in planes_for(a.split(' ', 1)[1], b.split(' ', 1)[1]):
            return None, None
        f = (lambda p, q: abs(p[1])) if b.endswith(' equator') else (lambda p, q: plane_value(p, q, pl))
        v0 = f(self.pos(R, a, 0), self.pos(R, b, 0))
        sky = a.startswith('S ') or b.startswith('S ')
        p5 = [self.pos(R, a, 5), self.pos(R, b, 5)]
        v5 = f(*p5) if sky and None not in p5 else ('n/a' if sky else None)
        return v0, v5


def ratio(n0, n5, d0, d5):
    """larger / smaller at the off; same orientation at +5"""
    if not n0 or not d0:
        return None, None, ''
    flip = n0 < d0
    v0 = d0 / n0 if flip else n0 / d0
    if n5 == 'n/a' or d5 == 'n/a':
        v5 = 'n/a'
    elif n5 is None and d5 is None:
        v5 = None
    else:
        a = n0 if n5 is None else n5
        b = d0 if d5 is None else d5
        v5 = (b / a if flip else a / b) if a and b else None
    return v0, v5, ' (inverted)' if flip else ''


# ---------------- writing
def fmt_off(d):
    return f"{d['off']:+.5f}{'%' if d['pct'] else ''}"


def tlabel(d):
    """target label: 'interval · name · group' for intervals, 'target (family)' otherwise"""
    if d['family'] == 'midpoint':
        return d['target']
    return f"{d['target']} · {d['name']} · {d['group']}" if d['family'] == 'interval' else f"{d['target']} ({d['family']})"


def out_text(d):
    """nearest target outside every tolerance (Eddie, 13 Oct 2026): plain text, no score, no colour"""
    return f"{tlabel(d)} — outside ±{d['tol']:.3g}{' %' if d['pct'] else ''}"


def put_value(ws, row, col, v0, v5, ev, also, note='', sc=None, ox=None):
    """9 cells from col: value, +5, target, group, offset, score (midpoints: t), arrow, also, scaled.
    ox = (kind, plane): with no family, the nearest target and offset are still written (plain text, no score, no colour)"""
    if v0 is None:
        return
    if not ev and ox and v0:
        near = families.outside(v0, ox[1] if KIND[ox[0]] == 'deg' else None, KIND[ox[0]])
        if near:
            ws.cell(row=row, column=col + 2, value=f"{out_text(near)}{note}")
            ws.cell(row=row, column=col + 4, value=fmt_off(near))
    c = ws.cell(row=row, column=col, value=round(v0, 6))
    if ev and ev['colour']:
        c.fill = FILL[ev['colour']]
    if v5 == 'n/a':
        ws.cell(row=row, column=col + 1, value='n/a')
        ws.cell(row=row, column=col + 6, value='n/a')        # engine does not reproduce the point (with or without a family)
    elif v5 is not None:
        ws.cell(row=row, column=col + 1, value=round(v5, 6))
    if ev:
        ws.cell(row=row, column=col + 2, value=f"{tlabel(ev)}{note}")
        if ev.get('group'):
            ws.cell(row=row, column=col + 3, value=ev['group'])
        ws.cell(row=row, column=col + 4, value=fmt_off(ev))
        ws.cell(row=row, column=col + 5, value=round(ev['score'] if ev['score'] is not None else ev['t'], 2)).number_format = '0.00'
        if v5 not in ('n/a', None):
            ws.cell(row=row, column=col + 6, value=arrow(v0, v5, ev))
    if also:
        ws.cell(row=row, column=col + 7, value='; '.join(f"{tlabel(d)} {fmt_off(d)} [{d['score']:.2f}]" for d in also))
    if sc:
        c = ws.cell(row=row, column=col + 8, value=f"{sc['scale']}: {tlabel(sc)} {fmt_off(sc)} [{sc['score']:.2f}]"
                    + (' (widens 10x in degrees)' if sc['scale'] == '/10' and sc['deg'] else ''))
        c.fill = FILL[sc['colour']]


def arrow(v0, v5, ev):
    if ev['family'] == 'midpoint':
        d0, d5 = abs(v0), abs(v5)
    elif ev['pct']:
        d0, d5 = abs(v0 / ev['tv'] - 1), abs(v5 / ev['tv'] - 1)
    else:
        d0, d5 = abs(v0 - ev['tv']), abs(v5 - ev['tv'])
    return '-> toward' if d5 < d0 else '<- away'


def header(ws, row, tid, title, planes):
    ws.cell(row=row, column=1, value=tid).font = BOLD
    ws.cell(row=row, column=2, value=title).font = BOLD
    row += 1
    for i, pl in enumerate(planes):
        col = 3 + COLS * i
        for k, h in enumerate((pl, '+5 min', 'nearest target', 'group', 'offset', 'score', 'off->+5', 'also (score)', 'scaled x10 / /10')):
            c = ws.cell(row=row, column=col + k, value=h); c.fill = HEAD; c.font = BOLD
    ws.cell(row=row, column=1, value='table').fill = HEAD
    ws.cell(row=row, column=2, value='points').fill = HEAD
    return row + 1


def plane_index(pl, planes):
    return 3 + COLS * planes.index(pl)


def write_pairs(ws, row, tid, title, ctx, R, rows, kind_of, thr=None, nums=None):
    """rows: [(label, a, b)] -> distances in RA/Dec/Flat/GC (equator: Dec only)."""
    row = header(ws, row, tid, title, PLANES)
    out = {}
    for label, a, b in rows:
        ws.cell(row=row, column=1, value=tid); ws.cell(row=row, column=2, value=label)
        for pl in PLANES:
            v0, v5 = ctx.pair(R, a, b, pl)
            if v0 is None:
                continue
            kind = kind_of(a, b)
            ev, also, sc = nearest(v0, kind, 'Dec' if kind == 'equator' else pl)
            put_value(ws, row, plane_index(pl, PLANES), v0, v5, ev, also, sc=sc, ox=(kind, 'Dec' if kind == 'equator' else pl))
            out[(label, pl)] = (v0, ev)
            if thr is not None:
                thread_add(thr, tid, f'{short(a)}→{short(b)}', (a, b), pl, v0, ev, sc)
            if nums is not None and KIND[kind] == 'deg' and tid in NUM_COL:
                number_add(nums, NUM_COL[tid], f'{short(a)}→{short(b)}', 'Dec' if kind == 'equator' else pl, v0)
        row += 1
    return row + 1, out


MID_PLANES = ('RA', 'RA far', 'Dec', 'Equator')
MID_CAP = 0.15


def mid_one(a, b, c, plane):
    """-> (offset of c from the midpoint of a and b, span) or None. RA: the near midpoint (shortest arc); RA far: the point 180 deg
    opposite, span 360 - near span; Dec: signed Dec; Equator: |Dec| of all three, only when the three are not all on the same side
    of the equator (otherwise it repeats Dec) (Eddie, 14 Oct 2026)"""
    if plane in ('RA', 'RA far'):
        d = (b - a + 180.0) % 360.0 - 180.0
        mid, span = (a + d / 2) % 360.0, abs(d)
        if plane == 'RA far':
            mid, span = (mid + 180.0) % 360.0, 360.0 - span
        return (c - mid + 180.0) % 360.0 - 180.0, span
    if plane == 'Equator':
        if (a >= 0) == (b >= 0) == (c >= 0):
            return None
        a, b, c = abs(a), abs(b), abs(c)
    return c - (a + b) / 2, abs(b - a)


def mid_rows(ctx, R, triples, plane):
    """triples: [(label, e1, e2, middle)] -> label -> (offset0, offset5, span)"""
    ix = 0 if plane.startswith('RA') else 1
    out = {}
    for label, e1, e2, m in triples:
        if plane.startswith('RA') and any(p.split(' ', 1)[1] == 'Ketu' for p in (e1, e2, m)):
            continue
        vals = []
        for st in (0, 5):
            ps = [ctx.pos(R, p, st) for p in (e1, e2, m)]
            vals.append('n/a' if None in ps else mid_one(ps[0][ix], ps[1][ix], ps[2][ix], plane))
        if vals[0] is None:
            continue                                       # Equator: all on one side
        sky = any(p.startswith('S ') for p in (e1, e2, m))
        o5 = None if not sky else ('n/a' if vals[1] in ('n/a', None) else vals[1][0])
        out[label] = (vals[0][0], o5, vals[0][1])
    return out


def write_mids(ws, row, tid, title, ctx, R, triples, thr=None):
    row = header(ws, row, tid, title + '  [value = third point\'s signed offset from the midpoint; target column = span and the tolerance '
                 'used (green = 0.1 % of the span, floor 0.05, cap 0.15; yellow 3x, light 9x); score column = t = |offset| / green tol]', MID_PLANES)
    data = {pl: mid_rows(ctx, R, triples, pl) for pl in MID_PLANES}
    for label, *_ in triples:
        ws.cell(row=row, column=1, value=tid)
        ws.cell(row=row, column=2, value=label)
        for pl in MID_PLANES:
            if label in data[pl]:
                o0, o5, span = data[pl][label]
                ev = mid_eval(o0, span)
                put_value(ws, row, plane_index(pl, MID_PLANES), o0, o5, ev, None)
                if thr is not None and ev['colour'] in ('green', 'yellow'):   # THREADS: green and yellow midpoints
                    trip = next(t for t in triples if t[0] == label)[1:]
                    thread_add(thr, tid, 'mid ' + short(label), trip, pl, o0, ev, None)
        row += 1
    return row + 1, data


def runner_sheet(wb, P, R, ctx):
    ws = wb.create_sheet(P)
    ws.cell(row=1, column=1, value=f"{P} {R['name']}").font = BOLD
    ws.cell(row=2, column=1, value='score (Eddie\'s families): green >= 80, yellow 50-80, light yellow < 50; midpoints: green <= 0.1 % of the span (0.05-0.15), '
            'yellow 3x, light 9x; off->+5 = toward / away from the nearest target; scaled = best of 10 v and v / 10 (/10 widens a tolerance 10x in degrees)')
    row = 4
    H, J = R['H'], R['J']
    thr = []                                               # THREADS: every scored hit linking a body with Jupiter
    nums = []                                              # NUMBERS: degree-distance hits >= 40 per target number
    dist = lambda a, b: 'equator' if b.endswith(' equator') else 'dist'
    move_or = lambda a, b: 'move' if a == 'S Jupiter' and b.endswith(' Jupiter') else dist(a, b)
    field = {}
    for tid, C in (('T1', 'H'), ('T2', 'J')):
        rows = [(f'{C} Jupiter → {C} {x}', f'{C} Jupiter', f'{C} {x}') for x in R[C] if x != 'Jupiter']
        row, _ = write_pairs(ws, row, tid, f'{C} Jupiter → {C} bodies, stars, equator (natal)', ctx, R, rows, dist, thr, nums)
    row, _ = write_pairs(ws, row, 'T3', 'H Jupiter → J bodies (natal, cross)', ctx, R,
                         [(f'H Jupiter → J {x}', 'H Jupiter', f'J {x}') for x in NATAL_BODIES if x in J], dist, thr, nums)
    row, _ = write_pairs(ws, row, 'T4', 'J Jupiter → H bodies (natal, cross)', ctx, R,
                         [(f'J Jupiter → H {x}', 'J Jupiter', f'H {x}') for x in NATAL_BODIES if x in H], dist, thr, nums)
    for tid, C in (('T5', 'H'), ('T6', 'J')):
        rows = [(f'S Jupiter → {C} {x}', 'S Jupiter', f'{C} {x}') for x in NATAL_BODIES if x in R[C] and x != 'Jupiter']
        row, field[tid] = write_pairs(ws, row, tid, f'S Jupiter → {C} bodies, at the off and +5 min', ctx, R, rows, dist, thr, nums)
    for tid, C in (('T7', 'H'), ('T8', 'J')):
        rows = [(f'S {z} → {C} Jupiter', f'S {z}', f'{C} Jupiter') for z in SKY_BODIES if z in ctx.S0 and z != 'Jupiter']
        row, field[tid] = write_pairs(ws, row, tid, f'every sky body (Moon incl.) → {C} Jupiter, at the off and +5 min', ctx, R, rows, dist, thr, nums)
    row, _ = write_pairs(ws, row, 'T9', 'Jupiter to Jupiter (S–H, S–J, H–J distances, scored on the families) and Equator values', ctx, R,
                         [('S Jupiter – H Jupiter', 'S Jupiter', 'H Jupiter'), ('S Jupiter – J Jupiter', 'S Jupiter', 'J Jupiter'),
                          ('H Jupiter – J Jupiter', 'H Jupiter', 'J Jupiter'), ('S Jupiter Equator', 'S Jupiter', 'S equator'),
                          ('H Jupiter Equator', 'H Jupiter', 'H equator'), ('J Jupiter Equator', 'J Jupiter', 'J equator')], move_or)
    # T10 / T11 midpoints
    tri = []
    for x in NATAL_BODIES:
        if x in H and x in J and x != 'Jupiter':           # Jupiter-only lines: T11 only (Eddie 14 Oct)
            tri += [(f'S Jupiter / H {x} | J {x}', 'S Jupiter', f'H {x}', f'J {x}'),
                    (f'S Jupiter / J {x} | H {x}', 'S Jupiter', f'J {x}', f'H {x}'),
                    (f'H {x} / J {x} | S Jupiter', f'H {x}', f'J {x}', 'S Jupiter')]
    row, field['T10'] = write_mids(ws, row, 'T10', 'midpoints: S Jupiter / H X, S Jupiter / J X, H X / J X — third point\'s offset', ctx, R, tri, thr)
    tri = [(f'H Jupiter / J Jupiter | S {z}', 'H Jupiter', 'J Jupiter', f'S {z}') for z in SKY_BODIES if z in ctx.S0]
    for C in 'HJ':
        tri += [(f'S Jupiter / {C} Jupiter | {D} {x}', 'S Jupiter', f'{C} Jupiter', f'{D} {x}')
                for D in 'HJ' for x in NATAL_BODIES if x in R[D] and not (D == C and x == 'Jupiter')]
    row, field['T11'] = write_mids(ws, row, 'T11', 'midpoints: H Jupiter / J Jupiter with every sky body; S Jupiter / natal Jupiter with every natal body', ctx, R, tri, thr)
    # T12-T15 ratios (interval list); every scored ratio also goes to the RATIOS BY GROUP sheet and the FIELD 12-15 matrices
    rats = []
    for t in ('T12', 'T13', 'T14', 'T15'):
        field[t] = {}

    field['_uni'] = {}

    def keep(tid, lab, pl, v0, v5, ev, inv, row, col):
        field[tid][(lab, pl)] = (v0, ev)
        if ev:
            rats.append((tid, lab + inv, pl, v0, v5, ev, (tid, lab, pl)))
            if ev['target'] == '1':                              # unison: field count written after all runners (may come from age)
                field['_uni'][(tid, lab, pl)] = (row, col + 7, ev.get('auto', False), ev.get('assisted', False))

    for tid, title, num, den in (
            ('T12', '(S Jupiter–S X) / (natal Jupiter–natal X), same plane', lambda C, x: ('S Jupiter', f'S {x}'), lambda C, x: (f'{C} Jupiter', f'{C} {x}')),
            ('T13', '(S Jupiter–natal X) / (natal Jupiter–natal X), same plane', lambda C, x: ('S Jupiter', f'{C} {x}'), lambda C, x: (f'{C} Jupiter', f'{C} {x}'))):
        row = header(ws, row, tid, title + '  [larger / smaller]', PLANES)
        for C in 'HJ':
            if tid == 'T13':                                   # Jupiter return (Eddie, 13 Oct): information line only
                ra, de = (ctx.pair(R, 'S Jupiter', f'{C} Jupiter', p)[0] for p in ('RA', 'Dec'))
                if ra < families.CONJ['RA'] or de < families.CONJ['Dec']:
                    ws.cell(row=row, column=1, value='T13')
                    ws.cell(row=row, column=2, value=f'Jupiter return: S–{C} Jupiter RA {ra:.5f} Dec {de:.5f}; a unison is automatic (grey) only where '
                            f'd(S Jupiter, {C} Jupiter) / d({C} Jupiter, X) < {AUTO_TOL} in that plane').font = BOLD
                    row += 1
            for x in NATAL_BODIES:
                if x == 'Jupiter' or x not in R[C]:
                    continue
                ws.cell(row=row, column=1, value=tid)
                lab = f'{num(C, x)[0]}–{num(C, x)[1]} / {den(C, x)[0]}–{den(C, x)[1]}'
                for pl in PLANES:
                    n0, n5 = ctx.pair(R, *num(C, x), pl); d0, d5 = ctx.pair(R, *den(C, x), pl)
                    if n0 is None or d0 is None:
                        continue
                    v0, v5, inv = ratio(n0, n5, d0, d5)
                    ev, also, sc = nearest(v0, 'ratio') if v0 else (None, [], None)
                    ev = unison_kind(ctx, R, C, f'{C} {x}', pl, ev)  # automatic (grey, not counted) / return-assisted (tag)
                    put_value(ws, row, plane_index(pl, PLANES), v0, v5, ev, also, inv, sc, ox=('ratio', pl))
                    if v0:
                        keep(tid, lab, pl, v0, v5, ev, inv, row, plane_index(pl, PLANES))
                        if not (ev and ev.get('auto')):        # automatic unisons stay out of THREADS
                            thread_add(thr, tid, short(lab), num(C, x) + den(C, x), pl, v0, ev, sc)
                ws.cell(row=row, column=2, value=lab)
                row += 1
        row += 1
    row = header(ws, row, 'T14', 'Equator ratios of the three Jupiters (|Dec|, larger / smaller)', ('Equator',))
    for a, b in (('S', 'H'), ('S', 'J'), ('H', 'J')):
        A, B = f'{a} Jupiter', f'{b} Jupiter'
        n0, n5 = ctx.pair(R, A, f'{a} equator', 'Dec'); d0, d5 = ctx.pair(R, B, f'{b} equator', 'Dec')
        v0, v5, inv = ratio(n0, n5, d0, d5)
        ws.cell(row=row, column=1, value='T14'); ws.cell(row=row, column=2, value=f'|Dec| {A} / |Dec| {B}{inv}')
        ev, also, sc = nearest(v0, 'eqratio') if v0 else (None, [], None)
        if a == 'S':
            ev = unison_kind(ctx, R, b, f'{b} equator', 'Dec', ev)
        put_value(ws, row, 3, v0, v5, ev, also, sc=sc, ox=('eqratio', None))
        if v0:
            keep('T14', f'|Dec| {A} / |Dec| {B}', 'Equator', v0, v5, ev, inv, row, 3)
        row += 1
    row += 1
    row = header(ws, row, 'T15', 'apex ratios: (Jupiter–X) / (Jupiter–equator) in Dec, X = bodies + royal stars; (Jupiter–royal A) / (Jupiter–royal B)', PLANES)
    for C in 'SHJ':
        CH = ctx.S0 if C == 'S' else R[C]
        for x in [b for b in NATAL_BODIES + ['Moon'] if b in CH and b != 'Jupiter'] + ROYAL:
            if x not in CH:
                continue
            n0, n5 = ctx.pair(R, f'{C} Jupiter', f'{C} {x}', 'Dec'); d0, d5 = ctx.pair(R, f'{C} Jupiter', f'{C} equator', 'Dec')
            v0, v5, inv = ratio(n0, n5, d0, d5)
            ws.cell(row=row, column=1, value='T15'); ws.cell(row=row, column=2, value=f'({C} Jupiter–{C} {x}) / ({C} Jupiter–equator){inv}')
            ev, also, sc = nearest(v0, 'ratio') if v0 else (None, [], None)
            put_value(ws, row, plane_index('Dec', PLANES), v0, v5, ev, also, sc=sc, ox=('ratio', 'Dec'))
            if v0:
                keep('T15', f'({C} Jupiter–{C} {x}) / ({C} Jupiter–equator)', 'Dec', v0, v5, ev, inv, row, plane_index('Dec', PLANES))
            row += 1
        for A, B in itertools.combinations(ROYAL, 2):
            ws.cell(row=row, column=1, value='T15'); ws.cell(row=row, column=2, value=f'({C} Jupiter–{C} {A}) / ({C} Jupiter–{C} {B})')
            for pl in PLANES:
                n0, n5 = ctx.pair(R, f'{C} Jupiter', f'{C} {A}', pl); d0, d5 = ctx.pair(R, f'{C} Jupiter', f'{C} {B}', pl)
                v0, v5, inv = ratio(n0, n5, d0, d5)
                ev, also, sc = nearest(v0, 'ratio') if v0 else (None, [], None)
                put_value(ws, row, plane_index(pl, PLANES), v0, v5, ev, also, inv, sc, ox=('ratio', pl))
                if v0:
                    keep('T15', f'({C} Jupiter–{C} {A}) / ({C} Jupiter–{C} {B})', pl, v0, v5, ev, inv, row, plane_index(pl, PLANES))
            row += 1
    row, field['T16'] = write_cross(ws, row, ctx, R)
    nat = [f'{C} {x}' for C in 'HJ' for x in NATAL_BODIES if x in R[C]]         # natal Jupiters included for S Jupiter
    field['T17'] = (equi_hits(ctx, R, 'H Jupiter', [p for p in nat if p[0] == 'H' and p != 'H Jupiter'], 'T17')
                    + equi_hits(ctx, R, 'J Jupiter', [p for p in nat if p[0] == 'J' and p != 'J Jupiter'], 'T17')
                    + equi_hits(ctx, R, 'S Jupiter', nat, 'T17'))
    field['T17'].sort(key=lambda h: (h['together'], -h['score']))        # 'X, Y together' lines at the bottom
    row = write_equi(ws, row, 'T17 EQUIDISTANCE: H Jupiter with two H bodies; J Jupiter with two J bodies; S Jupiter with two natal bodies (H–H, J–J, or the same body H X – J X)',
                     field['T17'])
    row, field['T18'] = write_t18(ws, row, ctx, R)
    t17k = frozenset(h['key'] for h in field['T17'])
    allp = pair_rows(ctx, R, STARS, t17k, 'PAIRS')
    t19 = t19_filter([dict(h, tid='T19') for h in allp
                      if not any(p.split(' ', 1)[1] in STARS and p.split(' ', 1)[1] not in ROYAL for p in (h['x'], h['y']))])
    row = pairs_header(ws, row, 'T19 sky Jupiter on natal pairs (filtered: ratio on an interval, or all three distances with a family hit; '
                       '"X, Y together" left out; natal bodies + royal stars; best ratio score first) — ' + PAIR_NOTE)
    row = write_pairs_rows(ws, row, t19) + 1
    field['T19'] = t19
    field['_pairs'] = allp
    for (lab, cn), (d, ev) in field['T16'].items():
        x = lab.split('–', 1)[1]
        a, b = cn[0], cn.split('= ')[1][0]
        thread_add(thr, 'T16', f'Jup–{x} {cn}', (f'{a} {x}', f'{b} {x}'), '', d, ev, None)
    field['_thr'] = thr
    field['_nums'] = nums
    ws.column_dimensions['B'].width = 46
    ws.freeze_panes = 'C4'
    field['_rats'] = rats
    return field


AUTO_TOL = 0.0015                                          # Eddie's rule (13 Oct), kept when the ratio tolerances tapered


ASSIST_TOL = 0.02                                          # return-assisted: AUTO_TOL <= d1/d2 < 0.02 (tag only)


def unison_kind(ctx, R, C, xpt, pl, ev):
    """for a unison: d(S Jupiter, C Jupiter) / d(C Jupiter, X) in plane pl -> ev greyed 'automatic' if < 0.0015 (Eddie, 13 Oct),
    tagged 'return-assisted' if 0.0015 <= ratio < 0.02 (colour and field count unchanged), else unchanged"""
    if not ev or ev['target'] != '1':
        return ev
    d1 = ctx.pair(R, 'S Jupiter', f'{C} Jupiter', pl)[0]
    d2 = ctx.pair(R, f'{C} Jupiter', xpt, pl)[0]
    if d1 is None or not d2:
        return ev
    q = d1 / d2
    if q < AUTO_TOL:
        return dict(ev, colour='grey', auto=True)
    if q < ASSIST_TOL:
        return dict(ev, assisted=True)
    return ev


CROSS = [(a, b) for a in 'SHJ' for b in 'SHJ' if a != b]       # RA distance in chart a = Dec distance in chart b
CROSS_TOL = 0.02
XCOLS = 8


def cross_name(a, b):
    return f'{a} RA = {b} Dec'


def cross_eval(ra, de):
    """-> crossing dict (diff = RA - Dec, linear score on +-0.02) or None outside the tolerance"""
    d = ra - de
    if abs(d) >= CROSS_TOL:
        return None
    sc = 100.0 * (CROSS_TOL - abs(d)) / CROSS_TOL
    return {'target': 'crossing', 'family': 'crossing', 'tv': 0.0, 'off': d, 'pct': False, 'score': sc, 'colour': families.colour(sc)}


def write_cross(ws, row, ctx, R):
    """T16 RA-Dec crossing (Eddie, 13 Oct 2026): the same body pair Jupiter-X, its RA distance in one chart equal to its Dec distance
    in another (6 orderings of S, H, J), +-0.02, linear score. The value need not be in a family; the best family of the mean of the
    two distances is shown beside it when it has one. Sky legs also at +5 min with the arrow toward / away from equality."""
    ws.cell(row=row, column=1, value='T16').font = BOLD
    ws.cell(row=row, column=2, value='RA–Dec crossing: Jupiter–X RA distance in one chart = Jupiter–X Dec distance in another (±0.02, '
            'linear score); family = best family of the mean of the two (shown when it has one)').font = BOLD
    row += 1
    for i, (a, b) in enumerate(CROSS):
        col = 3 + XCOLS * i
        for k, h in enumerate((f'{a} RA', f'{b} Dec', 'RA − Dec', 'score', '+5 RA − Dec', 'off->+5', 'family of the value', '')):
            if h:
                c = ws.cell(row=row, column=col + k, value=h if k else f'{cross_name(a, b)}: {a} RA'); c.fill = HEAD; c.font = BOLD
    ws.cell(row=row, column=1, value='table').fill = HEAD
    ws.cell(row=row, column=2, value='pair').fill = HEAD
    row += 1
    out = {}
    for x in NATAL_BODIES:
        if x == 'Jupiter' or x not in R['H'] or x not in R['J'] or x not in ctx.S0:
            continue
        lab = f'Jupiter–{x}'
        ws.cell(row=row, column=1, value='T16'); ws.cell(row=row, column=2, value=lab)
        for i, (a, b) in enumerate(CROSS):
            ra0, ra5 = ctx.pair(R, f'{a} Jupiter', f'{a} {x}', 'RA')
            de0, de5 = ctx.pair(R, f'{b} Jupiter', f'{b} {x}', 'Dec')
            if ra0 is None or de0 is None:
                continue                                       # Ketu: no RA (mirror of Rahu)
            col = 3 + XCOLS * i
            ws.cell(row=row, column=col, value=round(ra0, 6)); ws.cell(row=row, column=col + 1, value=round(de0, 6))
            c = ws.cell(row=row, column=col + 2, value=round(ra0 - de0, 6))
            ev = cross_eval(ra0, de0)
            if ev:
                c.fill = FILL[ev['colour']]
                ws.cell(row=row, column=col + 3, value=round(ev['score'], 2)).number_format = '0.00'
                out[(lab, cross_name(a, b))] = (ra0 - de0, ev)
            if 'n/a' in (ra5, de5):
                ws.cell(row=row, column=col + 4, value='n/a'); ws.cell(row=row, column=col + 5, value='n/a')
            elif ra5 is not None or de5 is not None:
                d5 = (ra0 if ra5 is None else ra5) - (de0 if de5 is None else de5)
                ws.cell(row=row, column=col + 4, value=round(d5, 6))
                ws.cell(row=row, column=col + 5, value='-> toward' if abs(d5) < abs(ra0 - de0) else '<- away')
            if ev:
                fb = families.best((ra0 + de0) / 2, None, 'deg')
                if fb:
                    f = ws.cell(row=row, column=col + 6, value=f"{tlabel(fb)} {fmt_off(fb)} [{fb['score']:.2f}]")
                    f.fill = FILL[fb['colour']]
        row += 1
    return row + 1, out


# ---------------- EQUIDISTANCE (Eddie, 14 Oct 2026)
EQ_PLANES = ('RA', 'Dec', 'Flat', 'GC', 'Equator')
EQ_HEAD = ('table', 'Jupiter: X = Y', 'plane', 'd(Jup, X)', 'd(Jup, Y)', 'ratio (smaller / larger)', 'unison offset', 'score', 'Jupiter',
           'd(X, Y)', 'd(Jup, X) + d(Jup, Y)', 'd(Jup, X)', 'family', 'd(Jup, Y)', 'family', 'd(X, Y)', 'family', 'ratio +5 min', 'off->+5',
           'unison timing')


def eq_dist(ctx, R, a, b, pl):
    """distance a-b in a plane; Equator = | |Dec a| - |Dec b| | (distances from the equator compared)"""
    return eq_dist2(ctx, R, a, b, pl)[0]


def eq_dist2(ctx, R, a, b, pl):
    """-> (at the off, at +5 min): +5 is None with no sky leg, 'n/a' where a rate is n/a"""
    if pl == 'Equator':
        pa, pb = ctx.pos(R, a, 0), ctx.pos(R, b, 0)
        if pa is None or pb is None:
            return None, None
        v0 = abs(abs(pa[1]) - abs(pb[1]))
        if not (a.startswith('S ') or b.startswith('S ')):
            return v0, None
        p5 = [ctx.pos(R, a, 5), ctx.pos(R, b, 5)]
        return v0, ('n/a' if None in p5 else abs(abs(p5[0][1]) - abs(p5[1][1])))
    return ctx.pair(R, a, b, pl)


def exact_time(ctx, v0, v5, target):
    """linear motion from the off to +5 min: when v reaches target -> 'applying, exact hh:mm (in n min)' / 'separating, exact hh:mm
    (n min ago)' in race-local clock time; natal-only 'fixed'"""
    if v5 is None:
        return 'fixed'
    if v5 == 'n/a':
        return 'n/a (rate)'
    rate = (v5 - v0) / 5.0
    if rate == 0:
        return 'no motion'
    t = (target - v0) / rate
    if abs(t) > 50 * 525960:                               # almost no relative motion: exact more than 50 years away
        return f"{'applying' if t >= 0 else 'separating'}, exact more than 50 years {'away' if t >= 0 else 'ago'}"
    when = ctx.off + datetime.timedelta(minutes=t)
    clock = when.strftime('%H:%M') if when.date() == ctx.off.date() else when.strftime('%d %b %Y %H:%M')
    return f'applying, exact {clock} (in {t:.1f} min)' if t >= 0 else f'separating, exact {clock} ({-t:.1f} min ago)'


def eq_family(ctx, v0, v5, pl):
    """best family hit of a distance with its score, and its timing when it has a sky leg"""
    b = families.best(v0, 'Dec' if pl == 'Equator' else pl if pl in ('RA', 'Dec') else None, 'deg')
    if not b:
        return (round(v0, 6), 'no family', ''), None       # (value cell, family cell, family cell colour)
    return (round(v0, 6), f"→ {b['target']} ({b['family']}, {b['score']:.2f}) · {exact_time(ctx, v0, v5, b['tv'])}", b['colour']), b


def equi_line(ctx, R, jup, x, y, pl, tid):
    """one plane of Jupiter's distances to X and Y -> dict (inside = within unison 1 %) or None (plane not measured).
    A chart's Rahu and Ketu are not paired in Equator (equal |Dec| by construction); Equator only when Jupiter, X and Y are not all on one
    side of the equator (else it repeats Dec)."""
    tol = families.TOL['1']
    if pl == 'Equator' and x[0] == y[0] and {x[2:], y[2:]} == {'Rahu', 'Ketu'}:
        return None
    if pl == 'Equator':
        ps = [ctx.pos(R, p, 0) for p in (jup, x, y)]
        if None in ps or (ps[0][1] >= 0) == (ps[1][1] >= 0) == (ps[2][1] >= 0):
            return None
    (dx, dx5), (dy, dy5) = eq_dist2(ctx, R, jup, x, pl), eq_dist2(ctx, R, jup, y, pl)
    if not dx or not dy:
        return None
    dev = (max(dx, dy) / min(dx, dy) - 1) * 100
    dxy, dxy5 = eq_dist2(ctx, R, x, y, pl)
    together = dxy is not None and dxy < (families.CONJ['RA'] if pl == 'RA' else families.CONJ['Dec'])
    base = {'tid': tid, 'label': f'{jup}: {x} = {y}', 'key': (f'{jup}: {x} = {y}', pl), 'plane': pl, 'd1': dx, 'd2': dy,
            'ratio': min(dx, dy) / max(dx, dy), 'off': dev, 'inside': dev < tol, 'together': together}
    if dev >= tol:
        return base
    sc = (10.0 * (tol - dev) / tol) ** 2
    sm = dx + dy
    # +5 min and timing: q = larger / smaller (as T19) moves linearly; exact unison when q = 1
    n5 = dx if dx5 is None else dx5
    m5 = dy if dy5 is None else dy5
    if dx5 is None and dy5 is None:
        r5, arw, tim = None, None, 'fixed'
    elif 'n/a' in (dx5, dy5) or not n5 or not m5:
        r5, arw, tim = 'n/a', 'n/a', 'n/a (rate)'
    else:
        # one timing method everywhere (Eddie 14 Oct): the larger / smaller ratio (orientation fixed at the off) moving toward its target
        q0, q5 = (dx / dy, n5 / m5) if dx >= dy else (dy / dx, m5 / n5)
        r5 = min(n5, m5) / max(n5, m5)
        arw = '-> toward' if abs(q5 - 1) < abs(q0 - 1) else '<- away'
        tim = exact_time(ctx, q0, q5, 1.0)
    fams = [eq_family(ctx, dx, dx5, pl)[0], eq_family(ctx, dy, dy5, pl)[0],
            eq_family(ctx, dxy, dxy5, pl)[0] if dxy else (None, None, '')]
    pos = 'between' if dxy is not None and abs(dxy - sm) <= 0.01 * sm else 'far side'
    if together:                                           # Eddie 14 Oct: X and Y in conjunction in that plane
        pos += ' · X, Y together'
    return dict(base, together=together, fams=fams, r5=r5, arrow=arw, timing=tim, score=sc, colour=families.colour(sc), pos=pos,
                dxy=dxy, sum=sm)


def same_rule(x, y):
    """T17 / T19 pair rule (Eddie, 14 Oct): H-H, J-J, or the same body in both charts (H X - J X); other H-J mixed pairs left out"""
    return x[0] == y[0] or x[2:] == y[2:]


def equi_hits(ctx, R, jup, pts, tid):
    """Jupiter equally far from two bodies: d(Jup, X) / d(Jup, Y) within unison 1 % (squared score), every plane; hits only, best first.
    Jupiter 'between' X and Y when d(X, Y) is within 1 % of d(Jup, X) + d(Jup, Y), otherwise 'far side'. Pairs in a fixed body order, so
    a pair has one label in every plane and runner. Pairs follow same_rule."""
    out = [h for x, y in itertools.combinations(pts, 2) if same_rule(x, y) for pl in EQ_PLANES
           for h in [equi_line(ctx, R, jup, x, y, pl, tid)] if h and h['inside']]
    # Eddie 14 Oct: a Ketu line with the same numbers as a Rahu line (e.g. X = Ketu in Dec = X = Rahu in Equator) is dropped
    rahu = {(h['label'], round(h['d1'], 6), round(h['d2'], 6)) for h in out if 'Rahu' in h['label']}
    out = [h for h in out if not ('Ketu' in h['label'] and
                                  (h['label'].replace('Ketu', 'Rahu'), round(h['d1'], 6), round(h['d2'], 6)) in rahu)]
    return sorted(out, key=lambda h: (h['together'], -h['score']))      # 'X, Y together' lines at the bottom


# ---------------- T19 / P## PAIRS: sky Jupiter on natal pairs (Eddie, 14 Oct 2026)
PAIR_HEAD = ('table', 'block', 'S Jupiter on X – Y', 'plane', 'd(S Jup, X)', 'family', 'd(S Jup, Y)', 'family', 'd(X, Y)', 'family',
             'ratio (larger / smaller)', 'interval', 'offset', 'score', 'ratio timing', 'Jupiter', 'note')


def pair_points(R, C, stars):
    return [f'{C} {b}' for b in NATAL_BODIES if b in R[C]] + [f'{C} {x}' for x in stars if x in R[C]]


def pair_rows(ctx, R, stars, t17keys=frozenset(), tid='T19', sky=False):
    """S Jupiter on every pair X-Y: blocks H-H, J-J, H-J across (sky: S-S, the points given: stars or sky bodies), every plane. No star-star pairs on a runner (sky:
    star-star only). Each row: the three distances with their best family (score, timing), the ratio d(S Jup, X) / d(S Jup, Y)
    (larger / smaller) on the interval list with the tapered tolerances (timing), between / far side, 'X, Y together' tag.
    A Ketu row with the same numbers as the Rahu row is dropped. A unison row also in T17 is marked."""
    jup = 'S Jupiter'
    if sky:
        pts = [f'S {x}' for x in stars if x in ctx.S0]
        blocks = [('S–S', list(itertools.combinations(pts, 2)))]
    else:
        H, J = pair_points(R, 'H', stars), pair_points(R, 'J', stars)
        isstar = lambda p: p.split(' ', 1)[1] in STARS
        ok = lambda a, b: not (isstar(a) and isstar(b))
        blocks = [('H–H', [(a, b) for a, b in itertools.combinations(H, 2) if ok(a, b)]),
                  ('J–J', [(a, b) for a, b in itertools.combinations(J, 2) if ok(a, b)]),
                  ('H–J', [(f'H {b}', f'J {b}') for b in NATAL_BODIES if b in R['H'] and b in R['J']])]   # same body only (Eddie 14 Oct)
    dcache, fcache = {}, {}

    def dist(p, pl):
        if (p, pl) not in dcache:
            dcache[(p, pl)] = eq_dist2(ctx, R, jup, p, pl)
        return dcache[(p, pl)]

    def fam(p, pl):
        if (p, pl) not in fcache:
            v0, v5 = dist(p, pl)
            fcache[(p, pl)] = eq_family(ctx, v0, v5, pl)
        return fcache[(p, pl)]

    out = []
    for blk, pairs in blocks:
        for x, y in pairs:
            for pl in EQ_PLANES:
                if pl == 'Equator':
                    if x[0] == y[0] and {x[2:], y[2:]} == {'Rahu', 'Ketu'}:
                        continue
                    ps = [ctx.pos(R, q, 0) for q in (jup, x, y)]
                    if None in ps or (ps[0][1] >= 0) == (ps[1][1] >= 0) == (ps[2][1] >= 0):
                        continue
                (dx, dx5), (dy, dy5) = dist(x, pl), dist(y, pl)
                if not dx or not dy:
                    continue
                dxy, dxy5 = eq_dist2(ctx, R, x, y, pl)
                (fx, bx), (fy, by) = fam(x, pl), fam(y, pl)
                fxy, bxy = eq_family(ctx, dxy, dxy5, pl) if dxy else ((dxy, None, ''), None)
                flip = dx < dy
                r0 = dx / dy if not flip else dy / dx
                n5, m5 = (dx if dx5 is None else dx5), (dy if dy5 is None else dy5)
                r5 = None if dx5 is None and dy5 is None else ('n/a' if 'n/a' in (dx5, dy5) or not n5 or not m5 else (n5 / m5 if not flip else m5 / n5))
                ev = families.best(r0, None, 'ratio')
                near = ev or families.outside(r0, None, 'ratio')
                tim = (exact_time(ctx, r0, None if r5 is None else r5, near['tv']) if r5 != 'n/a' else 'n/a (rate)')
                sm = dx + dy
                pos = 'between' if dxy is not None and abs(dxy - sm) <= 0.01 * sm else 'far side'
                together = dxy is not None and dxy < (families.CONJ['RA'] if pl == 'RA' else families.CONJ['Dec'])
                note = []
                if together:
                    note.append('X, Y together')
                lab = f'{jup}: {x} = {y}'
                if ev and ev['target'] == '1' and (lab, pl) in t17keys:
                    note.append('(also T17)')
                out.append({'tid': tid, 'block': blk, 'x': x, 'y': y, 'pair': f'{x} – {y}', 'plane': pl, 'fx': fx, 'fy': fy, 'fxy': fxy,
                            'allfam': bool(bx and by and bxy), 'r0': r0, 'ev': ev, 'near': near, 'timing': tim, 'pos': pos,
                            'together': together, 'note': '; '.join(note), 'sig': (round(dx, 6), round(dy, 6))})
    rahu = {(h['pair'], h['sig']) for h in out if 'Rahu' in h['pair']}            # any plane, as T17 (X = Ketu in Dec = X = Rahu in Equator)
    out = [h for h in out if not ('Ketu' in h['pair'] and (h['pair'].replace('Ketu', 'Rahu'), h['sig']) in rahu)]
    return out


def t19_filter(rows):
    """T19: ratio on an interval, or all three distances with a family hit; 'X, Y together' left out; best ratio score first"""
    keep = [h for h in rows if not h['together'] and (h['ev'] or h['allfam'])]
    return sorted(keep, key=lambda h: -(h['ev']['score'] if h['ev'] else -1))


def write_pairs_rows(ws, row, rows):
    for h in rows:
        n = h['near']
        rv = [h['tid'], h['block'], h['pair'], h['plane'], *h['fx'][:2], *h['fy'][:2], *h['fxy'][:2], round(h['r0'], 6),
              f"{n['target']} · {n['name']} · {n['group']}" + ('' if h['ev'] else f" — outside ±{n['tol']:.3g} %"), fmt_off(n),
              round(h['ev']['score'], 2) if h['ev'] else None, h['timing'], h['pos'], h['note'] or None]
        for k, v in enumerate(rv):
            ws.cell(row=row, column=1 + k, value=v)
        for k, f in enumerate((h['fx'], h['fy'], h['fxy'])):
            if f[2]:
                ws.cell(row=row, column=6 + 2 * k).fill = FILL[f[2]]
        if h['ev']:
            ws.cell(row=row, column=11).fill = FILL[h['ev']['colour']]
            ws.cell(row=row, column=14).number_format = '0.00'
        row += 1
    return row


def pairs_header(ws, row, title):
    ws.cell(row=row, column=1, value=title).font = BOLD
    row += 1
    for k, h in enumerate(PAIR_HEAD):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    return row + 1


PAIR_NOTE = ('sky Jupiter on natal pairs: d(S Jup, X), d(S Jup, Y), d(X, Y) with their best family (score, timing; natal d(X, Y) fixed); '
             'ratio d(S Jup, X) / d(S Jup, Y) larger / smaller on the interval list (tapered tolerances, timing); between / far side; '
             'blocks H–H, J–J, H–J; planes RA, Dec, Flat, GC, Equator (Equator only when S Jupiter, X, Y straddle the equator); '
             'no star–star pairs; a Ketu row repeating the Rahu row dropped')


def pairs_sheet(wb, P, R, rows):
    """P## PAIRS: every pair, unfiltered (natal bodies + all 22 stars); in the separate _pairs.xlsx workbook (Eddie 14 Oct)"""
    ws = wb.create_sheet(f'{P} PAIRS')
    row = pairs_header(ws, 1, f"{P} {R['name']} — PAIRS (unfiltered): " + PAIR_NOTE + '; "X, Y together" tagged')
    write_pairs_rows(ws, row, rows)
    ws.column_dimensions['C'].width = 34
    ws.freeze_panes = 'E3'


# ---------------- T18: equidistance, horse and jockey side by side (Eddie, 14 Oct 2026)
T18_SIDE = ('plane', 'd(Jup, X)', 'd(Jup, Y)', 'ratio', 'unison offset', 'score', 'Jupiter', 'timing')


def t18_side(ctx, R, jup, C, x, y):
    """best plane of one side: the inside (not 'together') plane with the highest score, else the closest plane (smallest offset) plain"""
    ls = [h for pl in EQ_PLANES for h in [equi_line(ctx, R, jup, f'{C} {x}', f'{C} {y}', pl, 'T18')] if h]
    ins = [h for h in ls if h['inside'] and not h['together']]
    if ins:
        return max(ins, key=lambda h: h['score'])
    out = [h for h in ls if not h['together']]             # a 'together' plane is never the closest plane (Eddie 14 Oct)
    return dict(min(out, key=lambda h: h['off']), inside=False) if out else None


def t18_rows(ctx, R, jupH, jupJ):
    """rows per body pair X-Y (bodies in both charts, Jupiter excluded): horse side, jockey side; rows with an inside side only;
    horse-inside rows first by the horse's score, then jockey-only rows by the jockey's score; a Ketu row repeating the Rahu row dropped"""
    bodies = [b for b in NATAL_BODIES if b != 'Jupiter' and b in R['H'] and b in R['J']]
    rows = []
    for x, y in itertools.combinations(bodies, 2):
        h, j = t18_side(ctx, R, jupH, 'H', x, y), t18_side(ctx, R, jupJ, 'J', x, y)
        if (h and h['inside']) or (j and j['inside']):
            rows.append({'pair': f'{x}–{y}', 'x': x, 'y': y, 'H': h, 'J': j})
    sig = lambda r: tuple((round(r[c]['d1'], 6), round(r[c]['d2'], 6)) if r[c] else None for c in 'HJ')    # numbers only, any plane
    rahu = {(r['pair'], sig(r)) for r in rows if 'Rahu' in r['pair']}
    rows = [r for r in rows if not ('Ketu' in r['pair'] and (r['pair'].replace('Ketu', 'Rahu'), sig(r)) in rahu)]
    hin = sorted([r for r in rows if r['H'] and r['H']['inside']], key=lambda r: -r['H']['score'])
    jin = sorted([r for r in rows if not (r['H'] and r['H']['inside'])], key=lambda r: -r['J']['score'])
    return hin + jin


def t18_cells(h):
    if not h:
        return [None] * len(T18_SIDE)
    if not h['inside']:
        return [h['plane'], round(h['d1'], 6), round(h['d2'], 6), round(h['ratio'], 6), f"unison +{h['off']:.5f}% (outside 1 %)", None, None, None]
    return [h['plane'], round(h['d1'], 6), round(h['d2'], 6), round(h['ratio'], 6), f"unison +{h['off']:.5f}%", round(h['score'], 2), h['pos'],
            h['timing']]


def write_t18(ws, row, ctx, R):
    """T18: the same equidistance pair side by side for horse and jockey. Block 1: S Jupiter: H X = H Y | S Jupiter: J X = J Y.
    Block 2: H Jupiter: H X = H Y | J Jupiter: J X = J Y. Each side its best plane (inside 1 %, highest score; 'together' planes left
    out); a side not inside shows its closest plane's ratio plain, uncoloured."""
    out = {}
    for blk, (jh, jj, title) in enumerate((('S Jupiter', 'S Jupiter', 'S Jupiter: H X = H Y  |  S Jupiter: J X = J Y'),
                                          ('H Jupiter', 'J Jupiter', 'H Jupiter: H X = H Y  |  J Jupiter: J X = J Y')), start=1):
        ws.cell(row=row, column=1, value='T18').font = BOLD
        ws.cell(row=row, column=2, value=f'T18 block {blk} — equidistance, horse and jockey side by side: {title}. Each side its best plane '
                '(inside unison 1 %, highest score; "X, Y together" planes left out); a side not inside shows its closest plane plain. '
                'Horse-inside rows first (closest to unison first), then jockey-only rows.').font = BOLD
        row += 1
        rows = t18_rows(ctx, R, jh, jj)
        both = lambda r: bool(r['H'] and r['H']['inside'] and r['J'] and r['J']['inside'])
        ws.cell(row=row - 1, column=2).value += f'  both (horse and jockey inside 1 %): {sum(both(r) for r in rows)}'
        heads = ('table', 'X–Y') + tuple(f'horse {h}' for h in T18_SIDE) + tuple(f'jockey {h}' for h in T18_SIDE) + ('both',)
        for k, h in enumerate(heads):
            c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
        row += 1
        out[blk] = rows
        for r in rows:
            vals = ['T18', r['pair']] + t18_cells(r['H']) + t18_cells(r['J']) + ['both' if both(r) else None]
            for k, v in enumerate(vals):
                ws.cell(row=row, column=1 + k, value=v)
            for k, c in enumerate('HJ'):
                h = r[c]
                col = 3 + k * len(T18_SIDE)
                if h and h['inside']:
                    ws.cell(row=row, column=col + 3).fill = FILL[h['colour']]
                    ws.cell(row=row, column=col + 5).number_format = '0.00'
            row += 1
        if not rows:
            ws.cell(row=row, column=2, value='(no pair inside 1 % on either side)'); row += 1
        row += 1
    return row, out


def write_equi(ws, row, title, hits):
    ws.cell(row=row, column=1, value=hits[0]['tid'] if hits else 'T17').font = BOLD
    ws.cell(row=row, column=2, value=title + ' — d(Jup, X) / d(Jup, Y) within unison 1 % (squared score), every plane (Equator = | |Dec| − |Dec| |, only when Jupiter, X and Y '
            'are not all on one side of the equator); '
            'Jupiter between X and Y when d(X, Y) is within 1 % of d(Jup, X) + d(Jup, Y), otherwise far side; stars left out; hits only, '
            'best first; "X, Y together" (d(X, Y) < 1.5 RA / 0.3 other planes) at the bottom; a Ketu line repeating a Rahu line dropped').font = BOLD
    row += 1
    for k, h in enumerate(EQ_HEAD):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    row += 1
    for h in hits:
        vals = (h['tid'], h['label'], h['plane'], round(h['d1'], 6), round(h['d2'], 6), round(h['ratio'], 6), f"unison +{h['off']:.5f}%",
                round(h['score'], 2), h['pos'], None if h['dxy'] is None else round(h['dxy'], 6), round(h['sum'], 6),
                *[x for f in h['fams'] for x in f[:2]], h['r5'] if h['r5'] in (None, 'n/a') else round(h['r5'], 6), h['arrow'], h['timing'])
        for k, v in enumerate(vals):
            c = ws.cell(row=row, column=1 + k, value=v)
        ws.cell(row=row, column=8).number_format = '0.00'
        ws.cell(row=row, column=6).fill = FILL[h['colour']]
        for k, f in enumerate(h['fams']):                  # family cell coloured by its score
            if f[2]:
                ws.cell(row=row, column=13 + 2 * k).fill = FILL[f[2]]
        row += 1
    if not hits:
        ws.cell(row=row, column=2, value='(no equidistance within 1 %)'); row += 1
    return row + 1


def field_equi_sheet(wb, runners, fields):
    """FIELD 17: every T17 equidistance, runners side by side (ratio, score, between / far side), holder count, most held first"""
    ws = wb.create_sheet('FIELD 17')
    ws.cell(row=1, column=1, value='T17 field matrix — equidistance (Jupiter equally far from two bodies, unison 1 %): per runner ratio [score] '
            'and between / far side; holders = runners with that line').font = BOLD
    order = sorted(runners)
    keys = {}
    for P in order:
        for h in fields[P]['T17']:
            keys.setdefault(h['key'], {})[P] = h
    held = lambda k: [P for P, h in keys[k].items() if not h['together']]     # 'X, Y together' not counted
    heads = ('Jupiter: X = Y', 'plane') + tuple(f"{P} {runners[P]['name']}" for P in order) + ('holders',)
    for k, h in enumerate(heads):
        c = ws.cell(row=3, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    r = 4
    for key in sorted(keys, key=lambda k: (-len(held(k)), -max(h['score'] for h in keys[k].values()), k)):
        ws.cell(row=r, column=1, value=key[0]); ws.cell(row=r, column=2, value=key[1])
        for i, P in enumerate(order):
            h = keys[key].get(P)
            if h:
                c = ws.cell(row=r, column=3 + i, value=f"{h['ratio']:.6f} [{h['score']:.2f}] {h['pos']} · {h['timing']}"
                            + (', not counted' if h['together'] else ''))
                c.fill = GREY if h['together'] else FILL[h['colour']]
        ws.cell(row=r, column=3 + len(order), value=f'{len(held(key))}/{len(order)}')
        r += 1
    ws.column_dimensions['A'].width = 46
    ws.freeze_panes = 'C4'


# ---------------- THREADS (Eddie, 13 Oct 2026)
THREAD_ROWS = [b for b in SKY_BODIES if b not in ('Jupiter', 'Rahu', 'Ketu')] + ['Nodes']
FONT = {'green': '006100', 'yellow': '9C5700', 'light': '8A7400', 'grey': '7F7F7F'}


def short(t):
    return t.replace('Jupiter', 'Jup')


KEEP_MARGIN = 0.5                                          # Eddie 14 Oct: a scaled repeat replaces the main form only if > 0.5 higher (unrounded)


def same_digits(ev, sc):
    """the scaled hit repeats the main hit: same family and the same digits (target x10 or /10, e.g. ninth 11.1111 / 1.11111)"""
    if not ev or not sc or ev.get('score') is None or ev['family'] != sc['family'] or not ev.get('tv') or not sc.get('tv'):
        return False
    f = 10.0 if sc['scale'] == 'x10' else 0.1
    return abs(sc['tv'] / (ev['tv'] * f) - 1) < 1e-6


def thread_add(thr, tid, lab, pts, pl, v, ev, sc):
    """one THREADS entry per scored hit (main value, and the scaled x10 / /10 value when it scores) on a body X linked with Jupiter.
    pts = the points of the measure ('S Jupiter', 'H Uranus', ...); X = the non-Jupiter body (Rahu / Ketu folded into 'Nodes')."""
    xs = [p for p in pts if not p.endswith(' Jupiter')]
    bodies = {p.split(' ', 1)[1] for p in xs}
    bodies = {'Nodes' if b in ('Rahu', 'Ketu') else b for b in bodies}
    if len(bodies) != 1 or next(iter(bodies)) not in THREAD_ROWS:
        return                                             # Jupiter-Jupiter, stars, equator
    X = next(iter(bodies))
    xch = {p[0] for p in xs}
    dirs = set()
    if tid in ('T5', 'T6'):
        dirs.add(f'S Jup→{tid == "T5" and "H" or "J"} X')
    if tid in ('T7', 'T8'):
        dirs.add(f'S X→{tid == "T7" and "H" or "J"} Jup')
    num = lambda v: f'{round(v, 6)}' if tid not in ('T10', 'T11', 'T16') else f'{v:+.6f}'
    if tid not in ('T10', 'T11', 'T16'):
        thread_all(thr, tid, lab, pl, v, X, xch, dirs)
        return
    repeat = same_digits(ev, sc)                           # Eddie 13 Oct: a scaled repeat of the main hit - keep the higher, drop the other
    up = repeat and sc['score'] > ev['score'] + KEEP_MARGIN   # main kept unless the scaled form is > 0.5 higher (unrounded; Eddie 14 Oct)
    if ev and ev.get('score') is not None or tid in ('T10', 'T11') and ev:
        tgt = ev['target'] if tid in ('T10', 'T11') else 'equal' if tid == 'T16' else ev['target']
        sct = f" ({ev['score']:.2f})" if ev.get('score') is not None else ''
        thr.append({'X': X, 'charts': xch, 'dirs': dirs, 'main': True, 'score': ev.get('score'), 'colour': ev['colour'],
                    'hidden': up,   # line not shown (the scaled form scores higher); still counts for tags
                    'text': f"{lab} {pl + ' ' if pl else ''}{num(v)} → {tgt}{sct} [{tid}]"})
    if sc and (not repeat or up):
        thr.append({'X': X, 'charts': xch, 'dirs': set(), 'main': False, 'score': sc['score'], 'colour': sc['colour'],
                    'text': f"{lab} {pl + ' ' if pl else ''}{round(v, 6)} {sc['scale']}: {round(sc['scaled_value'], 6)} → {sc['target']} "
                            f"({sc['score']:.2f}) [{tid}, scaled]"})


def thread_all(thr, tid, lab, pl, v, X, xch, dirs):
    """THREADS (Eddie 14 Oct): every family hit of v (main) and of 10 v, v / 10 (scaled, no conjunction), as NUMBERS does. A scaled hit on
    the same number (family + digits) as a main hit is a repeat: the main kept unless the scaled scores > 0.5 higher (then the main line
    is hidden but still counts for the tags)."""
    kind = 'ratio' if tid in ('T12', 'T13') else 'deg'
    plane = None if kind == 'ratio' else pl
    key = lambda d: num_key(d['family'], d['tv']) if d['tv'] else (d['family'], d['target'])
    main = {}
    for d in families.evaluate(v, plane, kind):
        e = {'X': X, 'charts': xch, 'dirs': dirs, 'main': True, 'score': d['score'], 'colour': d['colour'], 'hidden': False,
             'text': f"{lab} {pl + ' ' if pl else ''}{round(v, 6)} → {d['target']} ({d['score']:.2f}) [{tid}]"}
        main.setdefault(key(d), e)
        thr.append(e)
    scl = {}
    for f, tag in ((10.0, 'x10'), (0.1, '/10')):
        for d in families.evaluate(v * f, plane, kind):
            if d['family'] == 'conj':
                continue
            k = key(d)
            if k in main and d['score'] <= main[k]['score'] + KEEP_MARGIN:
                continue                                   # a repeat of a main hit: main kept
            if k in scl and scl[k]['score'] >= d['score']:
                continue
            if k in main:
                main[k]['hidden'] = True                   # scaled > 0.5 higher: main line hidden, still counts for the tags
            scl[k] = {'X': X, 'charts': xch, 'dirs': set(), 'main': False, 'score': d['score'], 'colour': d['colour'],
                      'text': f"{lab} {pl + ' ' if pl else ''}{round(v, 6)} {tag}: {round(v * f, 6)} → {d['target']} ({d['score']:.2f}) [{tid}, scaled]"}
    thr.extend(scl.values())


THREAD_MIN = 50.0                                          # Eddie, 13 Oct: tags, field counts and cell lines use hits scoring >= 50


def strong(h):
    """a hit scoring >= 50; midpoints (no score) count when green or yellow (span-scaled tolerance), as they are kept"""
    return h['score'] is None or h['score'] >= THREAD_MIN


def thread_tags(hits):
    """tags from the main (unscaled) hits scoring >= 50: mutual same chart (S Jup->H X with S X->H Jup, or the J pair), mutual across
    charts (S Jup->J X with S X->H Jup, or S Jup->H X with S X->J Jup), both Jupiters (S X->H and J Jup), both charts (natal X in
    H and in J), number of distinct directions"""
    m = [h for h in hits if h['main'] and strong(h)]
    d = set().union(*[h['dirs'] for h in m]) if m else set()
    ch = set().union(*[h['charts'] for h in m]) if m else set()
    tags = []
    if any({f'S Jup→{c} X', f'S X→{c} Jup'} <= d for c in 'HJ'):
        tags.append('mutual, same chart')
    if any({f'S Jup→{a} X', f'S X→{b} Jup'} <= d for a, b in (('J', 'H'), ('H', 'J'))):
        tags.append('mutual, across charts')
    if {'S X→H Jup', 'S X→J Jup'} <= d:
        tags.append('both Jupiters')
    if {'H', 'J'} <= ch:
        tags.append('both charts')
    tags.append(f'directions {len(d)}')
    return tags


COUNTED = ('mutual, same chart', 'mutual, across charts', 'both Jupiters')


def threads_sheet(wb, runners, fields):
    ws = wb.create_sheet('THREADS', wb.sheetnames.index('FIELD 5'))
    ws.cell(row=1, column=1, value='THREADS: hits inside tolerance linking body X with Jupiter, from T1-T8, T10-T13, T16; a cell lists those '
            'scoring >= 50 (midpoints: green / yellow), main first then scaled x10 / /10 (a scaled repeat of the main hit\'s number - same family, same '
            'digits - shown once: the main form unless the scaled one scores > 0.5 higher; tags still use the main hit), best first, then "+ n weaker" (score-0 hits not counted); automatic unisons left out. '
            'Top line: tags from the main hits >= 50 - mutual, same chart (S Jup->H X and S X->H Jup, or the J pair); mutual, across charts '
            '(S Jup->J X and S X->H Jup, or S Jup->H X and S X->J Jup); both Jupiters (S X->H Jup and S X->J Jup); both charts (natal X in H '
            'and in J); directions = distinct of S Jup->H X, S Jup->J X, S X->H Jup, S X->J Jup. Line colour = score.').font = BOLD
    order = sorted(runners)
    ws.cell(row=3, column=1, value='body').fill = HEAD
    for i, P in enumerate(order):
        c = ws.cell(row=3, column=2 + i, value=f"{P} {runners[P]['name']}"); c.fill = HEAD; c.font = BOLD
        ws.column_dimensions[openpyxl.utils.get_column_letter(2 + i)].width = 60
    last = 2 + len(order)
    for k, h in enumerate(COUNTED + ('mutual (either) or both Jupiters',)):
        c = ws.cell(row=3, column=last + k, value=f'runners: {h}'); c.fill = HEAD; c.font = BOLD
        ws.column_dimensions[openpyxl.utils.get_column_letter(last + k)].width = 16
    for r, X in enumerate(THREAD_ROWS, start=4):
        ws.cell(row=r, column=1, value=X + (' (Rahu / Ketu)' if X == 'Nodes' else '')).font = BOLD
        cnt = [0] * (len(COUNTED) + 1)
        for i, P in enumerate(order):
            hits = [h for h in fields[P]['_thr'] if h['X'] == X]
            if not hits:
                continue
            tags = thread_tags(hits)
            for k, t in enumerate(COUNTED):
                cnt[k] += t in tags
            cnt[-1] += any(t in tags for t in COUNTED)
            shown = sorted([h for h in hits if strong(h) and not h.get('hidden')], key=lambda h: (not h['main'], -(100.0 if h['score'] is None else h['score'])))
            rt = CellRichText(TextBlock(InlineFont(b=True), ' · '.join(tags)))
            for h in shown:
                rt.append(TextBlock(InlineFont(color=FONT.get(h['colour'], '000000')), '\n' + h['text']))
            weak = sum(1 for h in hits if not strong(h) and not h.get('hidden') and round(h['score'], 2) > 0)   # score-0 hits not counted (Eddie 13 Oct)
            if weak:
                rt.append(TextBlock(InlineFont(i=True), f'\n+ {weak} weaker (see T-tables)'))
            c = ws.cell(row=r, column=2 + i, value=rt)
            c.alignment = Alignment(wrap_text=True, vertical='top')
            sc_ = [h for h in shown if h['score'] is not None]
            best = max(sc_, key=lambda h: h['score']) if sc_ else (shown[0] if shown else None)     # cell colour = its best line
            if best and best['colour'] in FILL:
                c.fill = FILL[best['colour']]
        for k, v in enumerate(cnt):
            ws.cell(row=r, column=last + k, value=f'{v}/{len(order)}')
    ws.column_dimensions['A'].width = 18
    ws.freeze_panes = 'B4'


# ---------------- NUMBERS (Eddie, 13 Oct 2026)
NUM_COL = {'SKY': 'SKY', 'T1': 'HORSE', 'T2': 'JOCKEY', 'T5': 'SKY→NATAL', 'T6': 'SKY→NATAL',     # T3 / T4 cross-chart not used (Eddie 14 Oct)
           'T7': 'SKY→NATAL', 'T8': 'SKY→NATAL'}
NUM_COLS = ('SKY', 'HORSE', 'JOCKEY', 'SKY→NATAL')
NUM_MIN = 40.0
NUM_FAMILIES = ('whole', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver')     # degree-distance families (no conjunction, no ratios)


def num_colour(sc):
    return 'green' if sc >= 80 else 'yellow' if sc >= 50 else 'light'


def num_key(fam, tv):
    """x10 / /10 forms folded: family + the digits of the target (mantissa in [1, 10))"""
    m = tv / 10 ** math.floor(math.log10(tv))
    return fam, round(m, 5)


def number_add(nums, col, lab, pl, v):
    """every degree-distance family scoring >= 40 on v (main) and on 10 v, v / 10 (scaled); forms of v on the same number (same family,
    same digits) are the same hit: the higher-scoring one is kept (Eddie 13 Oct)"""
    if not v or v <= 0:
        return
    found = {}                                             # key -> the kept hit of this value (main or scaled, the higher score)
    for f, scl in ((1.0, ''), (10.0, 'x10'), (0.1, '/10')):
        for d in families.evaluate(v * f, pl, 'deg'):
            if d['family'] not in NUM_FAMILIES or d['score'] < NUM_MIN or not d['tv']:
                continue
            k = num_key(d['family'], d['tv'])
            if k in found and d['score'] <= found[k]['score'] + (0 if found[k]['scaled'] else KEEP_MARGIN):
                continue                                   # a repeat (same family, same digits): main kept unless the scaled form is > 0.5 higher
            txt = (f"{lab} {pl} {round(v, 6)} → {d['target']} {d['off']:+.5f} ({d['score']:.2f})" if not scl else
                   f"{lab} {pl} {round(v, 6)} {scl}: {round(v * f, 6)} → {d['target']} {d['off']:+.5f} ({d['score']:.2f}) [scaled]")
            found[k] = {'key': k, 'col': col, 'form': d['target'], 'tv': d['tv'], 'score': d['score'], 'colour': num_colour(d['score']),
                        'text': txt, 'scaled': bool(scl)}
    nums.extend(found.values())


def num_rows(nums):
    """key -> {col: hits best first}, forms, tag"""
    rows = {}
    for h in nums:
        r = rows.setdefault(h['key'], {'cols': {}, 'forms': []})
        r['cols'].setdefault(h['col'], []).append(h)
        if h['form'] not in [f for f, _ in r['forms']]:
            r['forms'].append((h['form'], h['tv']))
    for r in rows.values():
        for c in r['cols']:
            r['cols'][c].sort(key=lambda h: -h['score'])
        k = sum(c in r['cols'] for c in ('SKY', 'HORSE', 'JOCKEY'))
        r['tag'] = 'sky + horse + jockey' if k == 3 else 'two of three' if k == 2 else ''
    return rows


def num_label(key, r):
    return f"{key[0]}: {' / '.join(f for f, _ in sorted(r['forms'], key=lambda x: x[1]))}"


def rich(hits):
    rt = CellRichText()
    for i, h in enumerate(hits):
        rt.append(TextBlock(InlineFont(color=FONT[h['colour']]), ('\n' if i else '') + h['text']))
    return rt


def numbers_sheet(wb, P, R, nums):
    """P## NUMBERS: rows = target numbers (x10 / /10 folded, degree-distance families), columns SKY (S Jupiter -> sky points),
    HORSE (T1), JOCKEY (T2), SKY->NATAL (T5-T8); hits >= 40, main or scaled, best first; tag from SKY / HORSE / JOCKEY"""
    ws = wb.create_sheet(f'{P} NUMBERS', wb.sheetnames.index(f'{P} RATIOS') + 1)
    ws.cell(row=1, column=1, value=f"{P} {R['name']} — NUMBERS: degree-distance hits scoring >= 40 per target number (x10 / /10 forms folded; "
            'main or scaled; a repeat of the same number keeps the main form unless the scaled is > 0.5 higher). SKY = S Jupiter -> sky bodies, '
            'stars, equator; HORSE = T1 (H Jupiter -> H bodies, stars, equator); JOCKEY = T2 (J Jupiter -> J); SKY->NATAL = T5-T8; T3 / T4 '
            'cross-chart hits not used. Tag: sky + horse + jockey, or two of three (SKY->NATAL not in the tag). Colour: green >= 80, yellow 50-80, light 40-50.').font = BOLD
    for k, h in enumerate(('number', 'tag') + NUM_COLS):
        c = ws.cell(row=3, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    rows = num_rows(nums)
    rank = {'sky + horse + jockey': 0, 'two of three': 1, '': 2}
    r = 4
    for key in sorted(rows, key=lambda k: (rank[rows[k]['tag']], k)):
        row = rows[key]
        ws.cell(row=r, column=1, value=num_label(key, row)).alignment = Alignment(vertical='top', wrap_text=True)
        ws.cell(row=r, column=2, value=row['tag']).font = BOLD
        for k, col in enumerate(NUM_COLS):
            hits = row['cols'].get(col)
            if hits:
                c = ws.cell(row=r, column=3 + k, value=rich(hits))
                c.alignment = Alignment(wrap_text=True, vertical='top')
                c.fill = FILL[hits[0]['colour']]
        r += 1
    ws.column_dimensions['A'].width = 30; ws.column_dimensions['B'].width = 20
    for k in range(len(NUM_COLS)):
        ws.column_dimensions[openpyxl.utils.get_column_letter(3 + k)].width = 62
    ws.freeze_panes = 'C4'


def field_numbers_sheet(wb, runners, allnums):
    """FIELD NUMBERS: each number held with sky + horse + jockey by any runner; which runners hold it (their best horse / jockey hit)"""
    ws = wb.create_sheet('FIELD NUMBERS', wb.sheetnames.index('THREADS') + 1)
    ws.cell(row=1, column=1, value='FIELD NUMBERS: numbers held sky + horse + jockey (hits >= 40, x10 / /10 folded); per runner its best HORSE and '
            'JOCKEY hit on that number; SKY is the same for every runner').font = BOLD
    order = sorted(runners)
    rows = {P: num_rows(allnums[P]) for P in order}
    keys = sorted({k for P in order for k, r in rows[P].items() if r['tag'] == 'sky + horse + jockey'})
    heads = ('number', 'SKY (best)') + tuple(f"{P} {runners[P]['name']}" for P in order) + ('runners',)
    for k, h in enumerate(heads):
        c = ws.cell(row=3, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    for i, key in enumerate(keys, start=4):
        holders = [P for P in order if key in rows[P] and rows[P][key]['tag'] == 'sky + horse + jockey']
        r0 = rows[holders[0]][key]
        forms = {f: tv for P in holders for f, tv in rows[P][key]['forms']}           # forms seen across the holders
        ws.cell(row=i, column=1, value=num_label(key, {'forms': list(forms.items())}))
        sky = r0['cols']['SKY'][0]
        c = ws.cell(row=i, column=2, value=rich([sky])); c.fill = FILL[sky['colour']]
        for k, P in enumerate(order):
            if P in holders:
                hj = [rows[P][key]['cols']['HORSE'][0], rows[P][key]['cols']['JOCKEY'][0]]
                c = ws.cell(row=i, column=3 + k, value=rich(hj))
                c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=i, column=3 + len(order), value=f'{len(holders)}/{len(order)}')
    ws.column_dimensions['A'].width = 30; ws.column_dimensions['B'].width = 55
    for k in range(len(order)):
        ws.column_dimensions[openpyxl.utils.get_column_letter(3 + k)].width = 55
    ws.freeze_panes = 'C4'


def ratio_sheet(wb, P, R, rats, uni, n):
    """RATIOS BY GROUP: every T12-T15 ratio on an interval, grouped (Eddie's group order), tightest (highest score) first;
    unison rows carry the field count (runners with unison on the same ratio)"""
    ws = wb.create_sheet(f'{P} RATIOS', wb.sheetnames.index(P) + 1)
    ws.cell(row=1, column=1, value=f"{P} {R['name']} — RATIOS BY GROUP (T12-T15 ratios on Eddie's interval list, each on its own tolerance; tightest first)").font = BOLD
    row = 3
    for g in families.GROUPS:
        if not any(r[5]['group'] == g for r in rats):
            continue                                           # empty group: no header (Eddie, 13 Oct)
        ws.cell(row=row, column=1, value=g).font = BOLD
        row += 1
        for k, h in enumerate(('group', 'table', 'ratio', 'plane', 'value', '+5 min', 'interval', 'name', 'offset', 'score', 'off->+5',
                               'unison field')):
            c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
        row += 1
        for tid, lab, pl, v0, v5, ev, key in sorted([r for r in rats if r[5]['group'] == g], key=lambda r: -r[5]['score']):
            vals = (g, tid, lab, pl, round(v0, 6), v5 if v5 in ('n/a', None) else round(v5, 6), ev['target'], ev['name'], fmt_off(ev),
                    round(ev['score'], 2), 'n/a' if v5 == 'n/a' else (None if v5 is None else arrow(v0, v5, ev)),
                    ('automatic (Jupiter return), not counted' if ev.get('auto') else f'{uni[key]}/{n}' + (' return-assisted' if ev.get('assisted') else ''))
                    if ev['target'] == '1' else None)
            for k, x in enumerate(vals):
                ws.cell(row=row, column=1 + k, value=x)
            ws.cell(row=row, column=5).fill = FILL[ev['colour']]
            ws.cell(row=row, column=10).number_format = '0.00'
            row += 1
        row += 1
    ws.column_dimensions['C'].width = 52


def field_sheet(wb, tid, title, runners, fields, planes, mid=False, uni=None):
    ws = wb.create_sheet(f'FIELD {tid[1:]}')
    ws.cell(row=1, column=1, value=f'{tid} field matrix — {title}; per runner: value (coloured), nearest target + offset').font = BOLD
    order = sorted(runners)
    row = 3
    for pl in planes:
        ws.cell(row=row, column=1, value=pl).font = BOLD
        for i, P in enumerate(order):
            c = ws.cell(row=row, column=2 + 2 * i, value=f"{P} {runners[P]['name']}"); c.fill = HEAD; c.font = BOLD
        row += 1
        labels = []
        for P in order:
            src = fields[P][tid]
            ks = (list(src[pl].keys()) if mid else [k[0] for k in src if k[1] == pl])
            for k in ks:
                if k not in labels:
                    labels.append(k)
        for lab in labels:
            ws.cell(row=row, column=1, value=lab)
            for i, P in enumerate(order):
                src = fields[P][tid]
                if mid:
                    if lab not in src[pl]:
                        continue
                    o0 = src[pl][lab][0]; ev = mid_eval(o0, src[pl][lab][2]); v = o0
                else:
                    if (lab, pl) not in src:
                        continue
                    v, ev = src[(lab, pl)]
                c = ws.cell(row=row, column=2 + 2 * i, value=round(v, 6))
                if ev and ev['colour']:
                    c.fill = FILL[ev['colour']]
                if not ev and tid != 'T16' and v:                 # outside every tolerance: nearest target + offset, plain
                    near = families.outside(v, pl, 'ratio' if tid in ('T12', 'T13', 'T14', 'T15') else 'deg')
                    if near:
                        ws.cell(row=row, column=3 + 2 * i, value=f"{near['target']} {fmt_off(near)} (outside ±{near['tol']:.3g}{' %' if near['pct'] else ''})")
                if ev:
                    ws.cell(row=row, column=3 + 2 * i, value=f"{ev['target']} {fmt_off(ev)}" + (f" [{ev['score']:.2f}]" if ev['score'] is not None else '')
                            + (f" [{ev['group']}]" if ev.get('group') else '')
                            + ((' automatic (Jupiter return), not counted' if ev.get('auto') else f" field {uni[(tid, lab, pl)]}/{len(runners)}"
                                + (' return-assisted' if ev.get('assisted') else ''))
                               if uni is not None and ev.get('target') == '1' and ev.get('group') else ''))
            row += 1
        row += 1
    ws.column_dimensions['A'].width = 34
    ws.freeze_panes = 'B4'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('--out'); ap.add_argument('--off'); ap.add_argument('--site')
    a = ap.parse_args()
    race, batch, label, sky, runners = load_input(a.input)
    skipped = {P: R['name'] for P, R in runners.items() if 'Jupiter' not in R['H'] or 'Jupiter' not in R['J']}
    for P in skipped:                                          # e.g. a jockey tab with no chart (jockey None): no Jupiter to read
        del runners[P]
    course, hhmm, ymd = motion.race_parts(race)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(batch)), f'race_batch_{ymd}_{course}_{hhmm}_jupiter_tables.xlsx')
    off, site, src = motion.off_and_site(race, label, batch, a.off, a.site)
    rates, elines = motion.engine_rates(sky, off, site)
    ctx = Ctx(sky, rates)
    ctx.off = datetime.datetime.strptime(str(off)[:16], '%Y-%m-%d %H:%M')     # race-local off time (clock times of exact)
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'POSITIONS'
    wbp = openpyxl.Workbook(); wbp.remove(wbp.active)        # P## PAIRS: separate workbook next to the tables one
    repro = next((l for l in elines if l.startswith('reproduction')), elines[0] if elines else '')
    ws.append([f'{race} — Jupiter tables (raw, nothing filtered). off {off}; {src}']); ws.append([repro])
    ws.append(['skipped (no Jupiter in a chart): ' + '; '.join(f'{P} {n}' for P, n in skipped.items())] if skipped else [])
    ws.append(['runner', 'name', 'chart', 'point', 'kind', 'RA', 'Dec', 'rate RA /min', 'rate Dec /min'])
    for b, p in sky.items():
        r = rates.get(b)
        ws.append(['SKY', '', 'S', b, p[2], p[0], p[1], 'n/a' if r is None else r[0], 'n/a' if r is None else r[1]])
    for P in sorted(runners):
        for C in 'HJ':
            for b, p in runners[P][C].items():
                ws.append([P, runners[P]['name'], C, b, p[2], p[0], p[1]])
    # SKY JUPITER
    ws = wb.create_sheet('SKY JUPITER')
    ws.cell(row=1, column=1, value=f'{race} — S Jupiter to every sky body, star and the equator (at the off and +5 min)').font = BOLD
    R0 = {'H': {}, 'J': {}}
    rows = [(f'S Jupiter → S {x}', 'S Jupiter', f'S {x}') for x in sky if x != 'Jupiter']
    sky_nums = []
    row, _ = write_pairs(ws, 3, 'SKY', 'S Jupiter → sky points', ctx, R0, rows, lambda a, b: 'equator' if b.endswith(' equator') else 'dist',
                         nums=sky_nums)
    row = write_equi(ws, row, 'EQUIDISTANCE: S Jupiter with two sky bodies',
                     [dict(h, tid='SKY EQ') for h in equi_hits(ctx, R0, 'S Jupiter', [f'S {z}' for z in SKY_BODIES if z in sky and z != 'Jupiter'], 'SKY EQ')])
    row = pairs_header(ws, row, 'SKY PAIRS (Eddie, 14 Oct): S Jupiter on every pair of sky bodies (Moon included, no stars), filtered as T19 '
                       '(ratio on an interval, or all three distances with a family hit; "X, Y together" left out; best ratio score first): '
                       'd(S Jup, X), d(S Jup, Y), d(X, Y) with their best family (score, timing); ratio larger / smaller on the interval list '
                       '(tapered tolerances, timing); between / far side; planes RA, Dec, Flat, GC, Equator (only when S Jupiter, X, Y '
                       'straddle the equator; sky Rahu–Ketu not in Equator); a Ketu row repeating the Rahu row dropped')
    row = write_pairs_rows(ws, row, t19_filter(pair_rows(ctx, R0, [z for z in SKY_BODIES if z != 'Jupiter'], tid='SKY PAIRS', sky=True))) + 1
    row = pairs_header(ws, row, 'SKY STARS (background, once per race): S Jupiter on two sky stars, filtered as T19 (ratio on an interval, '
                       'or all three distances with a family hit; "X, Y together" left out)')
    write_pairs_rows(ws, row, t19_filter(pair_rows(ctx, R0, STARS, tid='SKY STARS', sky=True)))
    ws.column_dimensions['B'].width = 30
    fields = {}
    for P in sorted(runners):
        fields[P] = runner_sheet(wb, P, runners[P], ctx)
    # unison (Perfect 1) field counts: unison can come from age (e.g. Equator S/H = 1), so every unison shows how many runners hold it
    uni = {}
    for P in fields:
        for k, (r, c, auto, _) in fields[P]['_uni'].items():
            if not auto:                                       # automatic unisons are left out of every field count
                uni[k] = uni.get(k, 0) + 1
    n = len(runners)
    for P in sorted(runners):
        ws = wb[P]
        for k, (r, c, auto, assisted) in fields[P]['_uni'].items():
            ws.cell(row=r, column=c, value='unison: automatic (Jupiter return), not counted' if auto
                    else f'unison: field {uni[k]}/{n}' + (' return-assisted' if assisted else ''))
        ratio_sheet(wb, P, runners[P], fields[P]['_rats'], uni, n)
        pairs_sheet(wbp, P, runners[P], fields[P]['_pairs'])
        numbers_sheet(wb, P, runners[P], sky_nums + fields[P]['_nums'])
    for tid, title in (('T5', 'S Jupiter → H bodies'), ('T6', 'S Jupiter → J bodies'), ('T7', 'sky bodies → H Jupiter'),
                       ('T8', 'sky bodies → J Jupiter')):
        field_sheet(wb, tid, title, runners, fields, PLANES)
    field_sheet(wb, 'T10', 'midpoints S Jupiter / H X, S Jupiter / J X, H X / J X (third point\'s offset)', runners, fields, MID_PLANES, mid=True)
    field_sheet(wb, 'T11', 'midpoints H Jupiter / J Jupiter | sky body; S Jupiter / natal Jupiter | natal body (third point\'s offset)', runners,
                fields, MID_PLANES, mid=True)
    for tid, title, pls in (('T12', '(S Jupiter–S X) / (natal Jupiter–natal X), intervals', PLANES),
                            ('T13', '(S Jupiter–natal X) / (natal Jupiter–natal X), intervals', PLANES),
                            ('T14', 'Equator ratios of the three Jupiters, intervals', ('Equator',)),
                            ('T15', 'apex ratios, intervals', PLANES)):
        field_sheet(wb, tid, title, runners, fields, pls, uni=uni)
    field_sheet(wb, 'T16', 'RA–Dec crossing (value = RA − Dec, inside ±0.02)', runners, fields, [cross_name(a, b) for a, b in CROSS])
    field_equi_sheet(wb, runners, fields)
    threads_sheet(wb, runners, fields)
    field_numbers_sheet(wb, runners, {P: sky_nums + fields[P]['_nums'] for P in runners})
    wb.save(out)
    pout = out[:-len('_jupiter_tables.xlsx')] + '_pairs.xlsx' if out.endswith('_jupiter_tables.xlsx') else out[:-5] + '_pairs.xlsx'
    if not wbp.sheetnames:
        wbp.create_sheet('PAIRS').cell(row=1, column=1, value='no runners')
    wbp.save(pout)
    print(f'{race}: {len(runners)} runners -> {out} ({os.path.getsize(out) / 1e6:.2f} MB); pairs -> {pout} '
          f'({os.path.getsize(pout) / 1e6:.2f} MB); {repro}'
          + (f"; skipped (no Jupiter in a chart): {', '.join(skipped)}" if skipped else ''))


if __name__ == '__main__':
    main()
