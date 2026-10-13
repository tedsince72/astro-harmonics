#!/usr/bin/env python3
"""jupiter_tables.py INPUT [--out X.xlsx] [--off "YYYY-MM-DD HH:MM"] [--site lat,lon,elev]
Viewing tool (13 Oct 2026, Eddie): raw Jupiter tables for one race, nothing filtered.
INPUT = a race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx (TRANS, P01..Pnn, META) or a split race folder in reference/classic
(<course>_<hhmm>_<yyyymmdd>/<race>__P##.xlsx). Output: race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx next to the batch
(for a folder: in reference/classic/), unless --out.

Sheets: POSITIONS; SKY JUPITER; one sheet per runner (P01, P03, ...: tables 1-16) + P## RATIOS; THREADS (13 Oct: hits linking each body
with Jupiter, per runner, tags and field counts - see threads_sheet); P## NUMBERS + FIELD NUMBERS (13 Oct: target numbers, x10 / /10
folded, SKY / HORSE / JOCKEY / SKY->NATAL - see numbers_sheet); FIELD 5-8, 10, 12-16.
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
Midpoints (T10, T11) keep their own tolerance 0.05 / 0.15 (green / yellow; light = within 0.45). Sky-leg values also at off + 5 min
(engine, as JR v3 section F) with an arrow: toward / away from the nearest target; n/a where the engine does not reproduce a point.
Points and engine from tools/jup2 (imported, not changed). Frozen readers are not changed."""
import argparse, glob, os, re, sys, itertools, math
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


def mid_eval(v, tol=MID):
    off = v
    s, nr = tol
    col = 'green' if abs(off) <= s else 'yellow' if abs(off) <= nr else 'light' if abs(off) <= 3 * nr else ''
    return {'target': 'midpoint', 'tv': 0.0, 'family': 'midpoint', 'off': off, 'score': None, 't': abs(off) / s, 'colour': col, 'pct': False}


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
        ws.cell(row=row, column=col + 5, value=round(ev['score'] if ev['score'] is not None else ev['t'], 2))
        if v5 not in ('n/a', None):
            ws.cell(row=row, column=col + 6, value=arrow(v0, v5, ev))
    if also:
        ws.cell(row=row, column=col + 7, value='; '.join(f"{tlabel(d)} {fmt_off(d)} [{d['score']:.1f}]" for d in also))
    if sc:
        c = ws.cell(row=row, column=col + 8, value=f"{sc['scale']}: {tlabel(sc)} {fmt_off(sc)} [{sc['score']:.1f}]"
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
            if nums is not None and KIND[kind] == 'deg':
                hj = a.endswith(' Jupiter') and b.endswith(' Jupiter')
                if not (hj and tid == 'T4'):                   # H Jupiter – J Jupiter: once (from T3), in its own H–J column
                    number_add(nums, 'H–J' if hj else NUM_COL[tid], f'{short(a)}→{short(b)}', 'Dec' if kind == 'equator' else pl, v0)
        row += 1
    return row + 1, out


def mid_rows(ctx, R, triples, plane):
    """triples: [(label, e1, e2, middle)] -> label -> (offset0, offset5, span)"""
    ix = 0 if plane == 'RA' else 1
    out = {}
    for label, e1, e2, m in triples:
        if plane == 'RA' and any(p.split(' ', 1)[1] == 'Ketu' for p in (e1, e2, m)):
            continue
        vals = []
        for st in (0, 5):
            ps = [ctx.pos(R, p, st) for p in (e1, e2, m)]
            if None in ps:
                vals.append('n/a'); continue
            a, b, c = ps[0][ix], ps[1][ix], ps[2][ix]
            if plane == 'RA':
                d = (b - a + 180.0) % 360.0 - 180.0
                mid, span = (a + d / 2) % 360.0, abs(d)
                off = (c - mid + 180.0) % 360.0 - 180.0
            else:
                mid, span, off = (a + b) / 2, abs(b - a), c - (a + b) / 2
            vals.append((off, span))
        sky = any(p.startswith('S ') for p in (e1, e2, m))
        o5 = None if not sky else ('n/a' if vals[1] == 'n/a' else vals[1][0])
        out[label] = (vals[0][0], o5, vals[0][1])
    return out


def write_mids(ws, row, tid, title, ctx, R, triples, thr=None):
    row = header(ws, row, tid, title + '  [value = third point\'s signed offset from the midpoint; span in the label column; score column = t on 0.05]', ('RA', 'Dec'))
    data = {pl: mid_rows(ctx, R, triples, pl) for pl in ('RA', 'Dec')}
    for label, *_ in triples:
        ws.cell(row=row, column=1, value=tid)
        spans = [f"{pl} span {data[pl][label][2]:.4f}" for pl in ('RA', 'Dec') if label in data[pl]]
        ws.cell(row=row, column=2, value=f"{label}   ({'; '.join(spans)})")
        for pl in ('RA', 'Dec'):
            if label in data[pl]:
                o0, o5, span = data[pl][label]
                put_value(ws, row, plane_index(pl, ('RA', 'Dec')), o0, o5, mid_eval(o0), None)
                if thr is not None and abs(o0) <= MID[1]:      # THREADS: midpoints within 0.15 (green / yellow)
                    trip = next(t for t in triples if t[0] == label)[1:]
                    thread_add(thr, tid, 'mid ' + short(label), trip, pl, o0, mid_eval(o0), None)
        row += 1
    return row + 1, data


def runner_sheet(wb, P, R, ctx):
    ws = wb.create_sheet(P)
    ws.cell(row=1, column=1, value=f"{P} {R['name']}").font = BOLD
    ws.cell(row=2, column=1, value='score (Eddie\'s families): green >= 80, yellow 50-80, light yellow < 50; midpoints: green <= 0.05, yellow <= 0.15, '
            'light <= 0.45; off->+5 = toward / away from the nearest target; scaled = best of 10 v and v / 10 (/10 widens a tolerance 10x in degrees)')
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
    row, _ = write_pairs(ws, row, 'T9', 'Jupiter to Jupiter (S–H, S–J movement tolerance; H–J distance) and Equator values', ctx, R,
                         [('S Jupiter – H Jupiter', 'S Jupiter', 'H Jupiter'), ('S Jupiter – J Jupiter', 'S Jupiter', 'J Jupiter'),
                          ('H Jupiter – J Jupiter', 'H Jupiter', 'J Jupiter'), ('S Jupiter Equator', 'S Jupiter', 'S equator'),
                          ('H Jupiter Equator', 'H Jupiter', 'H equator'), ('J Jupiter Equator', 'J Jupiter', 'J equator')], move_or)
    # T10 / T11 midpoints
    tri = []
    for x in NATAL_BODIES:
        if x in H and x in J:
            tri += [(f'S Jupiter / H {x} | J {x}', 'S Jupiter', f'H {x}', f'J {x}'),
                    (f'S Jupiter / J {x} | H {x}', 'S Jupiter', f'J {x}', f'H {x}'),
                    (f'H {x} / J {x} | S Jupiter', f'H {x}', f'J {x}', 'S Jupiter')]
    row, field['T10'] = write_mids(ws, row, 'T10', 'midpoints: S Jupiter / H X, S Jupiter / J X, H X / J X — third point\'s offset', ctx, R, tri, thr)
    tri = [(f'H Jupiter / J Jupiter | S {z}', 'H Jupiter', 'J Jupiter', f'S {z}') for z in SKY_BODIES if z in ctx.S0]
    for C in 'HJ':
        tri += [(f'S Jupiter / {C} Jupiter | {D} {x}', 'S Jupiter', f'{C} Jupiter', f'{D} {x}')
                for D in 'HJ' for x in NATAL_BODIES if x in R[D] and not (D == C and x == 'Jupiter')]
    row, _ = write_mids(ws, row, 'T11', 'midpoints: H Jupiter / J Jupiter with every sky body; S Jupiter / natal Jupiter with every natal body', ctx, R, tri, thr)
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
                ws.cell(row=row, column=col + 3, value=round(ev['score'], 2))
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
                    f = ws.cell(row=row, column=col + 6, value=f"{tlabel(fb)} {fmt_off(fb)} [{fb['score']:.1f}]")
                    f.fill = FILL[fb['colour']]
        row += 1
    return row + 1, out


# ---------------- THREADS (Eddie, 13 Oct 2026)
THREAD_ROWS = [b for b in SKY_BODIES if b not in ('Jupiter', 'Rahu', 'Ketu')] + ['Nodes']
FONT = {'green': '006100', 'yellow': '9C5700', 'light': '8A7400', 'grey': '7F7F7F'}


def short(t):
    return t.replace('Jupiter', 'Jup')


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
    repeat = same_digits(ev, sc)                           # Eddie 13 Oct: a scaled repeat of the main hit - keep the higher, drop the other
    up = repeat and sc['score'] > ev['score']              # unrounded scores (Eddie 14 Oct); an exact tie keeps the main hit
    if ev and ev.get('score') is not None or tid in ('T10', 'T11') and ev:
        tgt = 'midpoint' if tid in ('T10', 'T11') else 'equal' if tid == 'T16' else ev['target']
        sct = f" ({ev['score']:.2f})" if ev.get('score') is not None else ''
        thr.append({'X': X, 'charts': xch, 'dirs': dirs, 'main': True, 'score': ev.get('score'), 'colour': ev['colour'],
                    'hidden': up,   # line not shown (the scaled form scores higher); still counts for tags
                    'text': f"{lab} {pl + ' ' if pl else ''}{num(v)} → {tgt}{sct} [{tid}]"})
    if sc and (not repeat or up):
        thr.append({'X': X, 'charts': xch, 'dirs': set(), 'main': False, 'score': sc['score'], 'colour': sc['colour'],
                    'text': f"{lab} {pl + ' ' if pl else ''}{round(v, 6)} {sc['scale']}: {round(sc['scaled_value'], 6)} → {sc['target']} "
                            f"({sc['score']:.2f}) [{tid}, scaled]"})


THREAD_MIN = 50.0                                          # Eddie, 13 Oct: tags, field counts and cell lines use hits scoring >= 50


def strong(h):
    """a hit scoring >= 50; midpoints (no score) count when within 0.15 (green / yellow), as they are kept"""
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
            'scoring >= 50 (midpoints: within 0.15), main first then scaled x10 / /10 (a scaled repeat of the main hit\'s number - same family, same '
            'digits - shown once, the higher-scoring form; tags still use the main hit), best first, then "+ n weaker" (score-0 hits not counted); automatic unisons left out. '
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
            best = next((h for h in shown if h['main']), shown[0] if shown else None)
            if best and best['colour'] in FILL:
                c.fill = FILL[best['colour']]
        for k, v in enumerate(cnt):
            ws.cell(row=r, column=last + k, value=f'{v}/{len(order)}')
    ws.column_dimensions['A'].width = 18
    ws.freeze_panes = 'B4'


# ---------------- NUMBERS (Eddie, 13 Oct 2026)
NUM_COL = {'SKY': 'SKY', 'T1': 'HORSE', 'T3': 'HORSE', 'T2': 'JOCKEY', 'T4': 'JOCKEY', 'T5': 'SKY→NATAL', 'T6': 'SKY→NATAL',
           'T7': 'SKY→NATAL', 'T8': 'SKY→NATAL'}
NUM_COLS = ('SKY', 'HORSE', 'JOCKEY', 'H–J', 'SKY→NATAL')        # H–J: H Jupiter – J Jupiter, counted once, not in the tag
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
            if k in found and found[k]['score'] >= d['score']:
                continue                                   # a repeat of the same number (same family, same digits): keep the higher (unrounded; tie = main)
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
    HORSE (T1, T3), JOCKEY (T2, T4), SKY->NATAL (T5-T8); hits >= 40, main or scaled, best first; tag from SKY / HORSE / JOCKEY"""
    ws = wb.create_sheet(f'{P} NUMBERS', wb.sheetnames.index(f'{P} RATIOS') + 1)
    ws.cell(row=1, column=1, value=f"{P} {R['name']} — NUMBERS: degree-distance hits scoring >= 40 per target number (x10 / /10 forms folded; "
            'main or scaled; a repeat of the same number keeps the higher form). SKY = S Jupiter -> sky bodies, stars, equator; HORSE = T1 + T3; '
            'JOCKEY = T2 + T4; H–J = H Jupiter – J Jupiter (once; not HORSE or JOCKEY); SKY->NATAL = T5-T8. '
            'Tag: sky + horse + jockey, or two of three (separate hits; H–J and SKY->NATAL not in the tag). Colour: green >= 80, yellow 50-80, light 40-50.').font = BOLD
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
        ws.cell(row=i, column=1, value=num_label(key, r0))
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
                    o0 = src[pl][lab][0]; ev = mid_eval(o0); v = o0
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
                    ws.cell(row=row, column=3 + 2 * i, value=f"{ev['target']} {fmt_off(ev)}" + (f" [{ev['score']:.1f}]" if ev['score'] is not None else '')
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
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'POSITIONS'
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
    write_pairs(ws, 3, 'SKY', 'S Jupiter → sky points', ctx, R0, rows, lambda a, b: 'equator' if b.endswith(' equator') else 'dist',
                nums=sky_nums)
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
        numbers_sheet(wb, P, runners[P], sky_nums + fields[P]['_nums'])
    for tid, title in (('T5', 'S Jupiter → H bodies'), ('T6', 'S Jupiter → J bodies'), ('T7', 'sky bodies → H Jupiter'),
                       ('T8', 'sky bodies → J Jupiter')):
        field_sheet(wb, tid, title, runners, fields, PLANES)
    field_sheet(wb, 'T10', 'midpoints S Jupiter / H X, S Jupiter / J X, H X / J X (third point\'s offset)', runners, fields, ('RA', 'Dec'), mid=True)
    for tid, title, pls in (('T12', '(S Jupiter–S X) / (natal Jupiter–natal X), intervals', PLANES),
                            ('T13', '(S Jupiter–natal X) / (natal Jupiter–natal X), intervals', PLANES),
                            ('T14', 'Equator ratios of the three Jupiters, intervals', ('Equator',)),
                            ('T15', 'apex ratios, intervals', PLANES)):
        field_sheet(wb, tid, title, runners, fields, pls, uni=uni)
    field_sheet(wb, 'T16', 'RA–Dec crossing (value = RA − Dec, inside ±0.02)', runners, fields, [cross_name(a, b) for a, b in CROSS])
    threads_sheet(wb, runners, fields)
    field_numbers_sheet(wb, runners, {P: sky_nums + fields[P]['_nums'] for P in runners})
    wb.save(out)
    print(f'{race}: {len(runners)} runners -> {out} ({os.path.getsize(out) / 1e6:.2f} MB); {repro}'
          + (f"; skipped (no Jupiter in a chart): {', '.join(skipped)}" if skipped else ''))


if __name__ == '__main__':
    main()
