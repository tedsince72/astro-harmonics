#!/usr/bin/env python3
"""jupiter_tables.py INPUT [--out X.xlsx] [--off "YYYY-MM-DD HH:MM"] [--site lat,lon,elev] [--full]
Viewing tool (13 Oct 2026, Eddie): raw Jupiter tables for one race, nothing filtered.
INPUT = a race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx (TRANS, P01..Pnn, META) or a split race folder in reference/classic
(<course>_<hhmm>_<yyyymmdd>/<race>__P##.xlsx). Output: race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx next to the batch
(for a folder: in reference/classic/), unless --out.

Sheets: POSITIONS; SKY JUPITER (+ EQUIDISTANCE, 14 Oct); one sheet per runner (P01, P03, ...: tables 1-14, 16-20 (T15 removed 15 Oct 2026); T17 equidistance, T18 horse | jockey side by side, T19 sky Jupiter on natal pairs); P## PAIRS (unfiltered) in a separate race_batch_<yyyymmdd>_<course>_<hhmm>_pairs.xlsx next to it + P## RATIOS; THREADS (13 Oct: hits linking each body
with Jupiter, per runner, tags and field counts - see threads_sheet); P## NUMBERS + FIELD NUMBERS (13 Oct: target numbers, x10 / /10
folded, SKY / HORSE / JOCKEY / SKY->NATAL - see numbers_sheet); FIELD 5-8, 10-14, 16, 17, 20.
Each value (13 Oct 2026, Eddie's correction): every family of tools/families.py (Eddie's definitions, his scores from
rebuild_kit/active_vibrations.py) is scored; nearest target = the family with the highest score; the other families with a score > 0
are listed beside it ('also'); values are never scaled x10 / /10 (Eddie, 16 Oct 2026: the x10 / /10 forms exist only as targets in
the family lists; the 'scaled' column, scaled timing and scaled THREADS / NUMBERS hits removed). Ratio values (T12-T14; T15 removed 15 Oct 2026)
are scored against Eddie's musical interval list only (families.interval_tol: area A 1, 3/2, 2 ... 9 on ±0.02 absolute, area B tapered %, 15 Oct 2026): target 'interval · name · group' plus a Group column; per runner a
'P## RATIOS' sheet (RATIOS BY GROUP: grouped, tightest first) and FIELD 12-14 matrices with the group tag. Colours by score: green >= 80,
yellow 50-80, light yellow < 50. No summary totals. Outside every tolerance (13 Oct): the value cell still shows its nearest target
(by tightness: smallest offset in units of its own tolerance) and offset, e.g. '1 · unison · Perfect — outside ±1 %' / '+1.26300%', plain text. Unison (Perfect 1) counts; every unison carries its field count (runners holding
unison on the same ratio; it can come from age, e.g. Equator S/H = 1) in the 'also' column, the RATIOS sheet and FIELD 12-14.
Jupiter return (13 Oct): when S Jupiter is in conjunction (RA < 1.5 or Dec < 0.3) with a natal Jupiter, that chart's T13 starts with
'Jupiter return: S-H (S-J) Jupiter RA .. Dec ..' (information). A T12-T14 unison is greyed as 'automatic (Jupiter return)', per plane,
only when d(S Jupiter, natal Jupiter) / d(natal Jupiter, X) in that plane < 0.0015; all other unisons are genuine.
Automatic unisons are left out of every field count. A unison with 0.0015 <= d1/d2 < 0.02 is tagged 'return-assisted' (colour and field
count unchanged). RATIOS sheets show only groups with hits. T16 (13 Oct 2026, Eddie): RA-Dec crossing, Jupiter-X RA distance in one chart =
its Dec distance in another (6 orderings), +-0.02, linear score, family of the value beside it; FIELD 16.
Midpoints (T10, T11, and the midpoint half of T17-T19, SKY EQ, SKY PAIRS; planes RA = the closer of near / far, Dec, Equator = |Dec|
when the three are not on one side; Eddie, 14 Oct 2026, revised): ratio half = closeness (smaller / larger x 100) >= 90 %, distance
half = offset from the midpoint on RA 0.5 / Dec 0.15 / Equator 0.15, each squared x 0.5; a hit needs both, total = the sum. FIELD 10 and FIELD 11.
T20 (15 Oct 2026): natal Jupiter as the midpoint of S X and natal X (horse | jockey per body), FIELD 20. Sky-leg values also at off + 5 min
(engine, as JR v3 section F) with an arrow: toward / away from the nearest target; n/a where the engine does not reproduce a point.
Planes (14 Oct 2026, Eddie): RA, Dec and Equator only; Flat and GC removed for noise.
Areas (Eddie, 15 Oct 2026): every ratio table (T12-T14, T19, T21, T22, SKY PAIRS, SKY STARS, P## PAIRS, P## RATIOS, FIELD 12-14, 21, 22)
in blocks: area A "whole + 3/2" (an A interval, or a midpoint hit), area "φ and √2" (φ, φ², φ³, 1+√2, √2, 1+1/√2), area B "other"
(a B interval), then no hit where every row is listed; each row once, in the highest area it has a hit in (A, φ and √2, B; the block
title counts rows with hits in more than one area), order inside a block as before.
SKY PAIRS body – royal (Eddie, 15 Oct 2026): S Jupiter on each sky body (Moon included) with each royal star, block "body – royal", same
filter, area blocks and sort. T19 sky side (Eddie, 15 Oct 2026): S Jupiter: S X – S Y beside each T19 row ("—" for H X – J X or where there
is none), its area, and "same as sky" (same number on the same leg incl. d(X, Y), or the same ratio interval); listing unchanged.
16 Oct 2026 (Eddie): SKY block timing column (best hit, per plane); royal-star-only tables after the full ones, every line:
T21R, T22R (runner sheets), SKY ROYAL (SKY JUPITER), FIELD 21R / 22R.
TIMELINE (16 Oct 2026): at the end of SKY JUPITER, every sky Jupiter event on that sheet exact from the off - 30 to + 60 min, in time order.
TIMELINE H / J (16 Oct 2026): at the end of each runner sheet, the same for every timed relationship involving that chart (T5-T22).
LONG TIMELINE (16 Oct 2026): score >= 80 at the off, any exact time, SEPARATING / APPLYING; sky equivalent cells on TIMELINE H / J and LONG H / J.
T24 (19 Oct 2026): stars against bodies, one row per star, RA / Dec distance per body, coloured by the best family, a cell comment with
target, family, offset, score; SKY block on SKY JUPITER (Moon included), HORSE and JOCKEY blocks on each runner sheet after T22R.
Stars (Eddie, 19 Oct 2026): T1, T2, T24 and the SKY block use T1_T2_T24_STARS (46 stars with |Dec| <= 50: STARS without Polaris + 13 new, 11 more 20 Oct 2026,
in RA order); every other table (and TIMELINE, NUMBERS) keeps STARS (23, Polaris included); the new stars' positions are appended to POSITIONS. Default workbook (19 Oct 2026):
POSITIONS, SKY JUPITER and the runner sheets only; --full also writes P## RATIOS, P## NUMBERS, THREADS, FIELD NUMBERS and every FIELD sheet.
T24 ratio tables (Eddie, 19 Oct 2026; natal only): T24 H / J (d(H star, H Jupiter) / d(J star, J Jupiter)), T24 HORSE RATIOS and T24 JOCKEY
RATIOS (d(star, Jupiter) / d(star, X), same chart), on each runner sheet after T24 JOCKEY; not in THREADS, NUMBERS, RATIOS, FIELD or TIMELINEs.
SKY STARS and the sky TIMELINE / LONG TIMELINE (Eddie, 20 Oct 2026): on the 46 stars (ctx.x), as the SKY block; runner timelines on STARS.
Points and engine from tools/jup2 (imported, not changed). Frozen readers are not changed."""
import argparse, glob, os, re, sys, itertools, math, datetime
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.comments import Comment

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools', 'jup2'))
from core import (ROYAL, NATAL_BODIES, SKY_BODIES, STAR_NAMES, EQUATOR, plane_value, planes_for,
                  wrap_ra)                                                     # noqa: E402
import motion                                                                  # noqa: E402
sys.path.insert(0, os.path.join(REPO, 'tools'))
import families                                                                # noqa: E402

PLANES = ('RA', 'Dec')                                     # Flat and GC removed (Eddie, 14 Oct 2026: noise); Equator where a table uses it
STARS = ['Algol', 'Pleiades', 'Aldebaran', 'Capella', 'Sirius', 'Procyon', 'Regulus', 'Alkaid', 'Algorab', 'Spica', 'Arcturus',
         'Alphecca', 'Antares', 'Vega', 'Deneb Algedi', 'Fomalhaut', 'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix',
         'Galactic Centre']                               # Galactic Centre (Eddie, 19 Oct 2026): 23rd star, not royal; skipped where a batch lacks it
NEW_STARS = ['Hamal', 'Pollux', 'Praesepe', 'Denebola', 'Zubenelgenubi', 'Zubeneschamali', 'Kaus Australis', 'Nunki', 'Deneb', 'Sadalsuud',
             'Sadalmelik', 'Scheat', 'Markab',             # Eddie, 19 Oct 2026: T1, T2 and T24 only (RA order)
             'Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Menkar', 'Phact', 'Adhara', 'Wezen', 'Menkent', 'Unukalhai',
             'Rasalhague']                                 # Eddie, 20 Oct 2026: 11 more, the same tables as the 13 (RA order)
# the 46 stars with |Dec| <= 50 (Eddie, 19 Oct 2026; 46 since 20 Oct 2026): STARS without Polaris + NEW_STARS, in RA order (engine J2000 RA at J2000.0, ascending;
# one fixed order, Eddie 19 Oct 2026); T1, T2, T24 and the SKY block star rows; every other table keeps STARS
T1_T2_T24_STARS = ['Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Hamal', 'Menkar', 'Algol', 'Pleiades', 'Aldebaran', 'Rigel', 'Capella',
                   'Bellatrix', 'Phact', 'Betelgeuse', 'Sirius', 'Adhara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Praesepe', 'Regulus',
                   'Denebola', 'Algorab', 'Spica', 'Alkaid', 'Menkent', 'Arcturus', 'Zubenelgenubi', 'Zubeneschamali', 'Alphecca',
                   'Unukalhai', 'Antares', 'Rasalhague', 'Galactic Centre', 'Kaus Australis', 'Vega', 'Nunki', 'Altair', 'Deneb', 'Sadalsuud',
                   'Deneb Algedi', 'Sadalmelik', 'Fomalhaut', 'Scheat', 'Markab']
assert sorted(T1_T2_T24_STARS) == sorted([x for x in STARS if x != 'Polaris'] + NEW_STARS)
BODIES = [b for b in SKY_BODIES if b != 'Ketu']           # workbook rows (Ketu rebuilt as Rahu's mirror)
GREEN = PatternFill('solid', start_color='C6EFCE'); YELLOW = PatternFill('solid', start_color='FFEB9C')
LIGHT = PatternFill('solid', start_color='FFF8DC'); HEAD = PatternFill('solid', start_color='D9E1F2')
BOLD = Font(bold=True)
GREY = PatternFill('solid', start_color='D9D9D9')
RED = PatternFill('solid', start_color='FF8080')            # T24 conjunction cells (Eddie, 20 Oct 2026), display only
FILL = {'green': GREEN, 'yellow': YELLOW, 'light': LIGHT, 'grey': GREY}
COLS = 8                                                   # per plane: value, +5, target, group, offset, score, arrow, also (scaled column removed 16 Oct 2026)


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


def chart(sheet, sky, stars=STARS):
    ch = {}
    for b in BODIES:
        if b == 'Moon' and not sky:
            continue
        if b in sheet:
            ch[b] = (sheet[b][0], sheet[b][1], 'body')
    for s in stars:
        if s + '_B' in sheet:
            ch[s] = (sheet[s + '_B'][0], sheet[s + '_B'][1], 'star')
    if 'Rahu' in ch:
        ch['Ketu'] = ((ch['Rahu'][0] + 180.0) % 360.0, -ch['Rahu'][1], 'body')
    ch[EQUATOR] = (0.0, 0.0, 'equator')
    return ch


def load_input(path, with_skyx=False):
    """-> race name, batch path, trans label, sky, runners {P##: {'name', 'H', 'J', 'HX', 'JX'}}; with_skyx: the sky on T1_T2_T24_STARS
    after sky. HX / JX (and that sky) = the charts on T1_T2_T24_STARS, for T1, T2 and T24 only (Eddie, 19 Oct 2026)"""
    path = path.rstrip('/')
    runners = {}
    if os.path.isdir(path):
        race = os.path.basename(path)
        course, hhmm, ymd = motion.race_parts(race)
        batch = os.path.join(os.path.dirname(path), f'race_batch_{ymd}_{course}_{hhmm}.xlsx')
        sky = skyx = label = None
        for f in sorted(glob.glob(f'{path}/*__P[0-9][0-9].xlsx')):
            P = re.search(r'__(P\d\d)\.xlsx$', f).group(1)
            wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
            label, t = read_sheet(wb['TRANS'])
            hl, h = read_sheet(wb['P01']); jl, j = read_sheet(wb['P02'])
            sky = sky or chart(t, True)
            skyx = skyx or chart(t, True, T1_T2_T24_STARS)
            runners[P] = {'name': f'{hl} / {jname(jl)}', 'H': chart(h, False), 'J': chart(j, False),
                          'HX': chart(h, False, T1_T2_T24_STARS), 'JX': chart(j, False, T1_T2_T24_STARS)}
    else:
        m = re.match(r'^race_batch_(\d{8})_(.+)_(\d{4})\.xlsx$', os.path.basename(path))
        if not m:
            sys.exit(f'not a race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx: {path}')
        ymd, course, hhmm = m.groups()
        race, batch = f'{course}_{hhmm}_{ymd}', path
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        label, t = read_sheet(wb['TRANS'])
        sky = chart(t, True)
        skyx = chart(t, True, T1_T2_T24_STARS)
        tabs = [s for s in wb.sheetnames if re.fullmatch(r'P\d+', s)]
        for i in range(0, len(tabs) - 1, 2):
            hl, h = read_sheet(wb[tabs[i]]); jl, j = read_sheet(wb[tabs[i + 1]])
            runners[f'P{int(tabs[i][1:]):02d}'] = {'name': f'{hl} / {jname(jl)}', 'H': chart(h, False), 'J': chart(j, False),
                                                   'HX': chart(h, False, T1_T2_T24_STARS), 'JX': chart(j, False, T1_T2_T24_STARS)}
    return (race, batch, label, sky, skyx, runners) if with_skyx else (race, batch, label, sky, runners)


# ---------------- numbers
KIND = {'dist': 'deg', 'move': 'deg', 'equator': 'deg', 'ratio': 'ratio', 'eqratio': 'eqratio'}


def nearest(v, kind, plane=None):
    """-> best family (highest score) or None, the other families with a score > 0. The value is never scaled (Eddie, 16 Oct 2026):
    x10 / /10 forms exist only as targets in the family lists"""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None, []
    k = KIND[kind]
    ev = families.evaluate(v, plane if k == 'deg' else None, k)
    return (ev[0] if ev else None), ev[1:]


MID_DTOL = {'RA': 0.5, 'Dec': 0.15, 'Equator': 0.15}     # midpoint distance half (Eddie, 14 Oct 2026): offset of X from the midpoint


MID_RTOL = 10.0                                            # ratio half: closeness >= 90 % (Eddie, 14 Oct 2026, revised)


def mid_score(d1, d2, off, pl):
    """midpoint scoring (Eddie, 14 Oct 2026, revised), two halves: ratio half = closeness (smaller / larger x 100), tolerance 10 %
    (closeness >= 90 %), (10 (10 − (100 − closeness)) / 10)² x 0.5; distance half = |offset| from the midpoint, squared on RA 0.5,
    Dec 0.15, Equator 0.15, x 0.5. A hit needs both halves inside; total = ratio half + distance half; otherwise no score, not a hit."""
    if not d1 or not d2:
        return None
    dtol = MID_DTOL[pl]
    q = max(d1, d2) / min(d1, d2)
    close = 100.0 * min(d1, d2) / max(d1, d2)
    dev = 100.0 - close
    rin, din = dev <= MID_RTOL, abs(off) <= dtol
    rs = 0.5 * (10.0 * (MID_RTOL - dev) / MID_RTOL) ** 2 if rin else None
    ds = 0.5 * (10.0 * (dtol - abs(off)) / dtol) ** 2 if din else None
    hit = rin and din
    sc = rs + ds if hit else None
    return {'q': q, 'close': close, 'dev': dev, 'off': off, 'rscore': rs, 'dscore': ds, 'score': sc, 'hit': hit, 'dtol': dtol,
            'colour': families.colour(sc) if hit else '', 'rin': rin, 'din': din}


def mid_text(m):
    """plain text of a midpoint that is not a hit: both offsets"""
    r = f"closeness {m['close']:.4f}%" + ('' if m['rin'] else ' (under 90 %)')
    d = f"midpoint {m['off']:+.6f}" + ('' if m['din'] else f" (outside ±{m['dtol']})")
    return f'not a hit: {r}, {d}'


# ---------------- race context
def own_nodes(a, b):
    """a chart's own Rahu-Ketu pair (H Rahu - H Ketu, J ..., S Rahu - S Ketu): never measured, never counted, every plane (Eddie, 14 Oct)"""
    return a[0] == b[0] and {a[2:], b[2:]} == {'Rahu', 'Ketu'}


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
        """distance a-b in plane pl at the off and at +5 (None if no sky leg or rate n/a). Ketu is measured in every plane like any
        body (Eddie, 14 Oct; was Dec only); the equator in Dec only; a chart's own Rahu-Ketu pair is not measured."""
        if (b.endswith(' equator') and pl != 'Dec') or own_nodes(a, b):
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


# ---------------- areas (Eddie, 15 Oct 2026): every ratio table split into area A "whole + 3/2" and area B "other"
AREA_NAME = {'A': 'AREA A "whole + 3/2" (intervals 1, 3/2, 2, 3, 4, 5, 6, 7, 8, 9 on ±0.02 absolute, or a midpoint hit: a midpoint is a unison)',
             'P': 'AREA φ AND √2 (φ, φ², φ³, 1+√2, √2, 1+1/√2 on 0.15 %)',
             'B': 'AREA B "other" (every other interval on the list, tapered % tolerances)',
             None: 'NO HIT'}


def hit_area(ev, mid=False):
    """'A' for an A interval or a midpoint hit, 'P' for a φ / √2 interval, 'B' for a B interval, None without a hit"""
    if mid:
        return 'A'
    return families.area(ev['target']) if ev and ev.get('family', 'interval') == 'interval' else None


def row_area(areas):
    """a row with several cells / sides / hits: the highest area present, A, then φ and √2, then B, else None (each row once)"""
    return next((a for a in families.AREAS if a in areas), None)


def multi(areas):
    """the row carries hits in more than one area"""
    return len({a for a in areas if a}) > 1


def multi_text(n):
    return f' ({n} carry hits in more than one area)' if n else ''


# ---------------- writing
def fmt_off(d):
    return f"{d['off']:+.5f}{'%' if d['pct'] else ''}"


def tlabel(d):
    """target label: 'interval · name · group' for intervals, 'target (family)' otherwise"""
    return f"{d['target']} · {d['name']} · {d['group']}" if d['family'] == 'interval' else f"{d['target']} ({d['family']})"


def tol_text(d):
    """'±0.02' (degrees, area A ratios: absolute) or '±0.25 %' (area B ratios)"""
    return f"±{d['tol']:.3g}{' %' if d['pct'] else ''}"


def out_text(d):
    """nearest target outside every tolerance (Eddie, 13 Oct 2026): plain text, no score, no colour"""
    return f"{tlabel(d)} — outside ±{d['tol']:.3g}{' %' if d['pct'] else ''}"


def put_value(ws, row, col, v0, v5, ev, also, note='', ox=None):
    """8 cells from col: value, +5, target, group, offset, score (midpoints: t), arrow, also.
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
        ws.cell(row=row, column=col + 5, value=round(ev['score'], 2)).number_format = '0.00'
        if v5 not in ('n/a', None):
            ws.cell(row=row, column=col + 6, value=arrow(v0, v5, ev))
    if also:
        ws.cell(row=row, column=col + 7, value='; '.join(f"{tlabel(d)} {fmt_off(d)} [{d['score']:.2f}]" for d in also))


def arrow(v0, v5, ev):
    if ev['pct']:
        d0, d5 = abs(v0 / ev['tv'] - 1), abs(v5 / ev['tv'] - 1)
    else:
        d0, d5 = abs(v0 - ev['tv']), abs(v5 - ev['tv'])
    return '-> toward' if d5 < d0 else '<- away'


def header(ws, row, tid, title, planes, extra=()):
    ws.cell(row=row, column=1, value=tid).font = BOLD
    ws.cell(row=row, column=2, value=title).font = BOLD
    row += 1
    for i, pl in enumerate(planes):
        col = 3 + (COLS + len(extra)) * i
        for k, h in enumerate((pl, '+5 min', 'nearest target', 'group', 'offset', 'score', 'off->+5', 'also (score)') + extra):
            c = ws.cell(row=row, column=col + k, value=h); c.fill = HEAD; c.font = BOLD
    ws.cell(row=row, column=1, value='table').fill = HEAD
    ws.cell(row=row, column=2, value='points').fill = HEAD
    return row + 1


def plane_index(pl, planes):
    return 3 + COLS * planes.index(pl)


SKY_COLS = COLS + 1                                        # T1 / T2 SKY cells per plane: the 9 value cells + exact timing
SAME_COL = 3 + COLS * len(PLANES) + SKY_COLS * len(PLANES)  # T1 / T2 'same as sky' tag column


def hit_keys(ev, also):
    """the numbers a cell hits (best, also), x10 / /10 target forms folded as in NUMBERS (family + digits); no conjunction -> {key: target}"""
    out = {}
    for d in [ev] + list(also or []):
        if d and d.get('family') != 'conj' and d.get('tv'):
            out.setdefault(num_key(d['family'], d['tv']), d)
    return out


def same_as_sky(nat, sky):
    """'same as sky' (Eddie, 15 Oct 2026): the natal cell and the SKY cell hit the same target (same family and number, x10 / /10
    folded) -> text per shared number or ''"""
    return '; '.join(f"{k[0]} {nat[k]['target']} | sky {sky[k]['target']}" for k in nat if k in sky)


def write_pairs(ws, row, tid, title, ctx, R, rows, kind_of, thr=None, nums=None, sky=False, timing=False):
    """rows: [(label, a, b)] -> distances in RA / Dec (equator: Dec only).
    sky (T1 / T2, Eddie 15 Oct 2026): SKY cells S Jupiter -> S X in the same plane beside each natal row (value, best family,
    +5 min, arrow, exact timing; not in THREADS / NUMBERS) and the tag 'same as sky' where both hit the same number."""
    # SKY block (Eddie, 16 Oct 2026): each plane's timing inside its own block, after its cells (no scaled timing: values never scaled)
    W = COLS + (1 if timing else 0)
    pcol = lambda pl: 3 + W * PLANES.index(pl)
    row = header(ws, row, tid, title, PLANES, ('timing',) if timing else ())
    if sky:
        ws.cell(row=row - 2, column=3 + COLS * len(PLANES), value='SKY: S Jupiter → S X, same plane (at the off and +5 min)').font = BOLD
        for i, pl in enumerate(PLANES):
            col = 3 + COLS * len(PLANES) + SKY_COLS * i
            for k, h in enumerate((f'SKY {pl}', '+5 min', 'nearest target', 'group', 'offset', 'score', 'off->+5', 'also (score)', 'timing')):
                c = ws.cell(row=row - 1, column=col + k, value=h); c.fill = HEAD; c.font = BOLD
        c = ws.cell(row=row - 1, column=SAME_COL, value='same as sky'); c.fill = HEAD; c.font = BOLD
    out = {}
    for label, a, b in rows:
        ws.cell(row=row, column=1, value=tid); ws.cell(row=row, column=2, value=label)
        same = []
        for pl in PLANES:
            v0, v5 = ctx.pair(R, a, b, pl)
            if v0 is None:
                continue
            kind = kind_of(a, b)
            ev, also = nearest(v0, kind, 'Dec' if kind == 'equator' else pl)
            put_value(ws, row, pcol(pl), v0, v5, ev, also, ox=(kind, 'Dec' if kind == 'equator' else pl))
            out[(label, pl)] = (v0, ev)
            if timing:                                     # applying / separating, exact clock time (off -> +5 min, linear), as the T-tables
                tc = pcol(pl) + COLS
                if ev:
                    ws.cell(row=row, column=tc, value=exact_time(ctx, v0, v5, ev['tv']))
            if thr is not None:
                thread_add(thr, tid, f'{short(a)}→{short(b)}', (a, b), pl, v0, ev)
            if nums is not None and KIND[kind] == 'deg' and tid in NUM_COL:
                number_add(nums, NUM_COL[tid], f'{short(a)}→{short(b)}', 'Dec' if kind == 'equator' else pl, v0)
            if sky:
                sa, sb = 'S ' + a.split(' ', 1)[1], 'S ' + b.split(' ', 1)[1]
                if sb.split(' ', 1)[1] not in ctx.S0:
                    continue
                s0, s5 = ctx.pair(R, sa, sb, pl)
                if s0 is None:
                    continue
                sev, salso = nearest(s0, kind, 'Dec' if kind == 'equator' else pl)
                col = 3 + COLS * len(PLANES) + SKY_COLS * PLANES.index(pl)
                put_value(ws, row, col, s0, s5, sev, salso, ox=(kind, 'Dec' if kind == 'equator' else pl))
                ws.cell(row=row, column=col + COLS, value=exact_time(ctx, s0, s5, sev['tv']) if sev else None)
                t = same_as_sky(hit_keys(ev, also), hit_keys(sev, salso))
                if t:
                    same.append(f'{pl}: {t}')
                out[(label, pl, 'sky')] = (s0, sev, t)
        if same:
            ws.cell(row=row, column=SAME_COL, value='same as sky — ' + '; '.join(same))
        row += 1
    return row + 1, out


MID_PLANES = ('RA', 'Dec', 'Equator')                       # RA: the closer of the near and far midpoint (Eddie, 14 Oct 2026)
MID_HEAD = {'RA': ('RA offset', 'midpoint', 'closeness %', 'ratio half', 'distance half', 'total', 'timing'),
            'Dec': ('Dec offset', 'closeness %', 'ratio half', 'distance half', 'total', 'timing'),
            'Equator': ('Equator offset', 'closeness %', 'ratio half', 'distance half', 'total', 'timing')}


def mid_geom(a, b, c, plane, side=None):
    """-> (offset of c from the midpoint of a and b, 'near' / 'far' / '', d(c, a), d(c, b)) or None, from the coordinate of the plane
    (RA, or signed Dec). RA: the closer of the near midpoint (shortest arc) and the far one (180 deg opposite), labelled; side fixes it
    (used at +5 min). Dec: signed Dec. Equator: |Dec| of all three, only when the three are not all on the same side of the equator."""
    if plane == 'RA':
        d = (b - a + 180.0) % 360.0 - 180.0
        mid = (a + d / 2) % 360.0
        near = (c - mid + 180.0) % 360.0 - 180.0
        far = (c - mid) % 360.0 - 180.0
        lab = side or ('near' if abs(near) <= abs(far) else 'far')
        arc = lambda x, y: abs((x - y + 180.0) % 360.0 - 180.0)
        return (near if lab == 'near' else far), lab, arc(c, a), arc(c, b)
    if plane == 'Equator':
        if (a >= 0) == (b >= 0) == (c >= 0):
            return None
        a, b, c = abs(a), abs(b), abs(c)
    return c - (a + b) / 2, '', abs(c - a), abs(c - b)


def mid_line(ctx, pts, plane):
    """pts = (e1, e2, middle) positions at the off and +5 -> dict: offset, side, distances, the two-half score (mid_score), the ratio at
    +5 (orientation fixed at the off) and its timing to unison; None when the plane does not apply"""
    p0, p5, sky = pts
    ix = 0 if plane == 'RA' else 1
    g0 = mid_geom(p0[0][ix], p0[1][ix], p0[2][ix], plane)
    if g0 is None:
        return None
    o0, lab, d1, d2 = g0
    m = mid_score(d1, d2, o0, plane)
    if m is None:
        return None
    q0 = d1 / d2 if d1 >= d2 else d2 / d1
    if not sky:
        o5, q5, tim = None, None, 'fixed'
    elif p5 is None:
        o5, q5, tim = 'n/a', 'n/a', 'n/a (rate)'
    else:
        g5 = mid_geom(p5[0][ix], p5[1][ix], p5[2][ix], plane, side=lab or None)
        if g5 is None or not g5[2] or not g5[3]:
            o5, q5, tim = 'n/a', 'n/a', 'n/a (rate)'
        else:
            o5 = g5[0]
            q5 = g5[2] / g5[3] if d1 >= d2 else g5[3] / g5[2]   # one timing method: larger / smaller toward unison
            tim = exact_time(ctx, q0, q5, 1.0)
    return dict(m, o0=o0, o5=o5, side=lab, d1=d1, d2=d2, q5=q5, timing=tim)


def mid_rows(ctx, R, triples, plane):
    """triples: [(label, e1, e2, middle)] -> label -> mid_line"""
    out = {}
    for label, e1, e2, m in triples:
        p0 = [ctx.pos(R, p, 0) for p in (e1, e2, m)]
        if None in p0:
            continue
        sky = any(p.startswith('S ') for p in (e1, e2, m))
        p5 = [ctx.pos(R, p, 5) for p in (e1, e2, m)] if sky else None
        h = mid_line(ctx, (p0, None if p5 is None or None in p5 else p5, sky), plane)
        if h:
            out[label] = dict(h, pts=(e1, e2, m))          # TIMELINE H / J (16 Oct): the ends and the middle point
    return out


def mid_cells(h, pl):
    """the per-plane cells of a midpoint: offset, (RA: near / far), ratio with % off unison, ratio score, distance score, score, timing"""
    cells = [round(h['o0'], 6)] + ([h['side']] if pl == 'RA' else []) + [
        round(h['close'], 4),
        round(h['rscore'], 2) if h['hit'] else (None if h['rin'] else 'under 90 %'),
        round(h['dscore'], 2) if h['hit'] else (None if h['din'] else f"outside ±{h['dtol']}"),
        round(h['score'], 2) if h['hit'] else None, h['timing']]
    return cells


def write_mids(ws, row, tid, title, ctx, R, triples, thr=None):
    ws.cell(row=row, column=1, value=tid).font = BOLD
    ws.cell(row=row, column=2, value=title + '  [midpoint scoring (Eddie, 14 Oct 2026): ratio half = closeness of the third point\'s distances to the two ends '
            '(smaller / larger x 100), at least 90 %, (10 (10 − (100 − closeness)) / 10)² x 0.5; distance half = its signed offset from the midpoint, '
            'squared on RA ±0.5, Dec ±0.15, Equator ±0.15, x 0.5; a hit needs both, total = the sum; otherwise no score, not a hit (plain). RA: the closer of the '
            'near and far midpoint. Timing: the ratio toward unison]').font = BOLD
    row += 1
    starts, col = {}, 3
    for pl in MID_PLANES:
        starts[pl] = col
        for k, h in enumerate(MID_HEAD[pl]):
            c = ws.cell(row=row, column=col + k, value=h); c.fill = HEAD; c.font = BOLD
        col += len(MID_HEAD[pl])
    ws.cell(row=row, column=1, value='table').fill = HEAD
    ws.cell(row=row, column=2, value='points').fill = HEAD
    row += 1
    data = {pl: mid_rows(ctx, R, triples, pl) for pl in MID_PLANES}
    for label, *trip in triples:
        ws.cell(row=row, column=1, value=tid)
        ws.cell(row=row, column=2, value=label)
        for pl in MID_PLANES:
            h = data[pl].get(label)
            if not h:
                continue
            c0 = starts[pl]
            for k, v in enumerate(mid_cells(h, pl)):
                ws.cell(row=row, column=c0 + k, value=v)
            if h['hit']:
                sc_col = c0 + len(MID_HEAD[pl]) - 2
                ws.cell(row=row, column=c0).fill = FILL[h['colour']]
                ws.cell(row=row, column=sc_col).fill = FILL[h['colour']]
                for k in range(len(MID_HEAD[pl]) - 4, len(MID_HEAD[pl]) - 1):
                    ws.cell(row=row, column=c0 + k).number_format = '0.00'
                if thr is not None:                        # THREADS: a midpoint hit counts at total >= 50 (Eddie 15 Oct)
                    ev = {'target': f"{h['side'] + ' ' if h['side'] else ''}midpoint", 'score': h['score'], 'colour': h['colour']}
                    thread_add(thr, tid, 'mid ' + short(label), tuple(trip), pl, h['o0'], ev)
        row += 1
    return row + 1, data


def runner_sheet(wb, P, R, ctx):
    ws = wb.create_sheet(P)
    ws.cell(row=1, column=1, value=f"{P} {R['name']}").font = BOLD
    ws.cell(row=2, column=1, value='score (Eddie\'s families): green >= 80, yellow 50-80, light yellow < 50; midpoints (T10, T11, T17-T20): two halves, closeness >= 90 % and '
            'distance from the midpoint (RA 0.5, Dec 0.15, Equator 0.15), each squared x 0.5, a hit needs both, total = the sum; off->+5 = toward / away from the nearest target; values are never scaled x10 / /10 (16 Oct 2026)')
    row = 4
    H, J = R['H'], R['J']
    thr = []                                               # THREADS: every scored hit linking a body with Jupiter
    nums = []                                              # NUMBERS: degree-distance hits >= 40 per target number
    dist = lambda a, b: 'equator' if b.endswith(' equator') else 'dist'
    move_or = lambda a, b: 'move' if a == 'S Jupiter' and b.endswith(' Jupiter') else dist(a, b)
    field = {}
    RX = {'H': R['HX'], 'J': R['JX']}                      # T1, T2 (and T24) on T1_T2_T24_STARS (Eddie, 19 Oct 2026)
    for tid, C in (('T1', 'H'), ('T2', 'J')):
        rows = [(f'{C} Jupiter → {C} {x}', f'{C} Jupiter', f'{C} {x}') for x in RX[C] if x != 'Jupiter']
        row, field[tid] = write_pairs(ws, row, tid, f'{C} Jupiter → {C} bodies, stars, equator (natal); SKY cells S Jupiter → S X beside each row',
                                      ctx.x, RX, rows, dist, sky=True)
        # THREADS / NUMBERS keep the T1 / T2 rows on STARS, as before (the new stars stay out, Polaris stays in): fed off-sheet
        old = [(f'{C} Jupiter → {C} {x}', f'{C} Jupiter', f'{C} {x}') for x in R[C] if x != 'Jupiter']
        write_pairs(openpyxl.Workbook().active, 1, tid, '', ctx, R, old, dist, thr, nums, sky=True)
    row, field['T23'], field['_t23'], unis = write_t23(ws, row, ctx, R)        # T23 (Eddie, 16 Oct 2026): H / J, S / H, S / J ratios of the T1 / T2 / SKY distances
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
    # T12-T14 ratios (interval list); every scored ratio also goes to the RATIOS BY GROUP sheet and the FIELD 12-14 matrices
    # (T15 apex ratios removed, Eddie 15 Oct 2026; the other tables keep their numbers)
    rats = []
    for t in ('T12', 'T13', 'T14'):
        field[t] = {}

    field['_uni'] = dict(unis)                              # T23 unisons (written above T12)

    def keep(tid, lab, pl, v0, v5, ev, inv):
        field[tid][(lab, pl)] = (v0, ev)
        if ev:
            rats.append((tid, lab + inv, pl, v0, v5, ev, (tid, lab, pl)))

    def write_ratio_blocks(row, tid, title, planes, lines, info=()):
        """area blocks (Eddie, 15 Oct 2026): A (an A interval in any plane), B (otherwise a B interval), no hit; each row once, in the
        order as before; info lines (Jupiter return) on top. lines: [(label, {plane: (v0, v5, inv, ev, also)})]"""
        for t in info:
            ws.cell(row=row, column=1, value=tid)
            ws.cell(row=row, column=2, value=t).font = BOLD
            row += 1
        by = {a: [] for a in families.AREAS + (None,)}
        for lab, cells in lines:
            by[row_area([hit_area(c[3]) for c in cells.values()])].append((lab, cells))
        for a in families.AREAS + (None,):
            mixed = sum(1 for _, cells in by[a] if multi([hit_area(c[3]) for c in cells.values()]))
            row = header(ws, row, tid, f'{title} — {AREA_NAME[a]}: {len(by[a])} rows' + multi_text(mixed), planes)
            for lab, cells in by[a]:
                ws.cell(row=row, column=1, value=tid)
                for pl, (v0, v5, inv, ev, also) in cells.items():
                    col = plane_index(pl, planes)
                    put_value(ws, row, col, v0, v5, ev, also, '' if tid == 'T14' else inv, ox=('eqratio' if tid == 'T14' else 'ratio', pl))
                    if ev and ev['target'] == '1':             # unison: field count written after all runners (may come from age)
                        field['_uni'][(tid, lab, pl)] = (row, col + 7, ev.get('auto', False), ev.get('assisted', False))
                ws.cell(row=row, column=2, value=lab + (next(iter(cells.values()))[2] if tid == 'T14' else ''))
                row += 1
            row += 1
        return row

    for tid, title, num, den in (
            ('T12', '(S Jupiter–S X) / (natal Jupiter–natal X), same plane', lambda C, x: ('S Jupiter', f'S {x}'), lambda C, x: (f'{C} Jupiter', f'{C} {x}')),
            ('T13', '(S Jupiter–natal X) / (natal Jupiter–natal X), same plane', lambda C, x: ('S Jupiter', f'{C} {x}'), lambda C, x: (f'{C} Jupiter', f'{C} {x}'))):
        info, lines = [], []
        for C in 'HJ':
            if tid == 'T13':                                   # Jupiter return (Eddie, 13 Oct): information line only
                ra, de = (ctx.pair(R, 'S Jupiter', f'{C} Jupiter', p)[0] for p in ('RA', 'Dec'))
                if ra < families.CONJ['RA'] or de < families.CONJ['Dec']:
                    info.append(f'Jupiter return: S–{C} Jupiter RA {ra:.5f} Dec {de:.5f}; a unison is automatic (grey) only where '
                                f'd(S Jupiter, {C} Jupiter) / d({C} Jupiter, X) < {AUTO_TOL} in that plane')
            for x in NATAL_BODIES:
                if x == 'Jupiter' or x not in R[C]:
                    continue
                lab = f'{num(C, x)[0]}–{num(C, x)[1]} / {den(C, x)[0]}–{den(C, x)[1]}'
                cells = {}
                for pl in PLANES:
                    n0, n5 = ctx.pair(R, *num(C, x), pl); d0, d5 = ctx.pair(R, *den(C, x), pl)
                    if n0 is None or d0 is None:
                        continue
                    v0, v5, inv = ratio(n0, n5, d0, d5)
                    ev, also = nearest(v0, 'ratio') if v0 else (None, [])
                    ev = unison_kind(ctx, R, C, f'{C} {x}', pl, ev)  # automatic (grey, not counted) / return-assisted (tag)
                    cells[pl] = (v0, v5, inv, ev, also)
                    if v0:
                        keep(tid, lab, pl, v0, v5, ev, inv)
                        if not (ev and ev.get('auto')):        # automatic unisons stay out of THREADS
                            thread_add(thr, tid, short(lab), num(C, x) + den(C, x), pl, v0, ev)
                lines.append((lab, cells))
        row = write_ratio_blocks(row, tid, title + '  [larger / smaller]', PLANES, lines, info)
    lines = []
    for a, b in (('S', 'H'), ('S', 'J'), ('H', 'J')):
        A, B = f'{a} Jupiter', f'{b} Jupiter'
        n0, n5 = ctx.pair(R, A, f'{a} equator', 'Dec'); d0, d5 = ctx.pair(R, B, f'{b} equator', 'Dec')
        v0, v5, inv = ratio(n0, n5, d0, d5)
        ev, also = nearest(v0, 'eqratio') if v0 else (None, [])
        if a == 'S':
            ev = unison_kind(ctx, R, b, f'{b} equator', 'Dec', ev)
        if v0:
            keep('T14', f'|Dec| {A} / |Dec| {B}', 'Equator', v0, v5, ev, inv)
        lines.append((f'|Dec| {A} / |Dec| {B}', {'Equator': (v0, v5, inv, ev, also)}))
    row = write_ratio_blocks(row, 'T14', 'Equator ratios of the three Jupiters (|Dec|, larger / smaller)', ('Equator',), lines)
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
    sky19 = t19_sky(ctx, R)
    for h in t19:                                          # sky side (Eddie 15 Oct): never adds or removes a row, area set by the natal row
        h['S'] = None if h['block'] == 'H–J' else sky19.get((h['x'][2:], h['y'][2:], h['plane']))
        # Eddie 15 Oct: a together sky side has no tag; d(S Jupiter, royal star) never counts (the star barely moves birth -> race day)
        cells = [(n, i) for n, i in T19_CELLS if not (i < 2 and h['xy'[i]][2:] in ROYAL)]
        h['same'] = [] if h['S'] is None or h['S']['together'] else t21_same(h, h['S'], cells)
    row = write_pair_blocks(ws, row, 'T19 sky Jupiter on natal pairs (filtered: ratio on an interval, or a midpoint hit, or all three distances with a family hit; '
                            '"X, Y together" left out; natal bodies + royal stars; best first by the higher of the ratio score and the midpoint total) — ' + PAIR_NOTE
                            + '. SKY side (Eddie, 15 Oct 2026): S Jupiter: S X – S Y, the same two bodies (royal stars too) at race-day positions in the same '
                            'plane, the same cells, timing from the off + 5 min, its area; "—" for H X – J X (one point in the sky) and where there is no sky '
                            'side (Equator: S Jupiter, S X, S Y on one side; X = Jupiter). It never adds or removes a row; the block is set by the natal row. '
                            '"same as sky": the natal and the sky side hit the same number on the same leg (d(S Jup, X), d(S Jup, Y) or d(X, Y); best family, '
                            'x10 / /10 folded; never d(S Jup, royal star), the star barely moves) or the ratio on the same interval. A sky side with '
                            '"X, Y together" is shown plain: no colour, no area, no tag',
                            t19, 'T19', skyside=True)
    field['T19'] = t19
    field['_pairs'] = allp
    row, field['T20'] = write_t20(ws, row, ctx, R, thr)
    row, field['T21'] = write_t21(ws, row, ctx, R)        # fixed stars (Eddie 15 Oct): not in THREADS or NUMBERS
    row, field['T22'] = write_t22(ws, row, ctx, R)
    row, field['T21R'] = write_t21(ws, row + 1, ctx, R, royal=True)    # royal stars only (Eddie 16 Oct), after the full tables
    row, field['T22R'] = write_t22(ws, row + 1, ctx, R, royal=True)
    for C, who in (('H', 'HORSE'), ('J', 'JOCKEY')):        # T24 (Eddie, 19 Oct 2026): stars against bodies, natal
        row, field[f'_t24{C}'], field[f'_t24m{C}'] = write_t24(ws, row + 1, RX[C], C, f'T24 {who} (natal): {T24_NOTE}')
    row, field['_t24hj'] = write_t24hj(ws, row + 1, RX['H'], RX['J'])        # T24 ratio tables (Eddie, 19 Oct 2026), natal only
    for C, who in (('H', 'HORSE'), ('J', 'JOCKEY')):
        row, field[f'_t24r{C}'] = write_t24r(ws, row + 1, RX[C], C, who)
    tl = runner_timeline(ctx, R, field)                    # TIMELINE H / J (Eddie, 16 Oct 2026), after the other tables
    skyf = lambda e: sky_equiv(ctx, R, e)                  # sky equivalent cells (Eddie, 16 Oct 2026)
    for C, who in (('H', 'horse'), ('J', 'jockey')):
        row = write_timeline(ws, row + 1, ctx, tl[C], f'TIMELINE {C}',
                             f"TIMELINE {C} (Eddie, 16 Oct 2026): every timed relationship involving the {who}'s chart ({C}) whose exact time falls from "
                             'the off − 30 min to the off + 60 min (T5–T8, T10, T11, T12–T14, T16, T17, T18, T19, T20, T22), linear from the off and the '
                             'off + 5 min as everywhere; "outside at the off" = not a hit at the off; sky-only and natal-only (fixed) relationships, '
                             'together rows and automatic unisons left out; values never scaled x10 / /10; each event once (other tables in the note); "H + J" = '
                             'uses both charts, in both timelines. SKY EQUIVALENT (16 Oct 2026): the same relationship in the sky at the off, every natal '
                             'point replaced by the same sky body, same plane: value, best family / interval (area), score, timing; "—" where two points '
                             'become one; "same as sky" = the sky on the same target as the event (both hits)', skyf=skyf)
    lt = runner_timeline(ctx, R, field, keep=long_keep)    # LONG TIMELINE H / J (Eddie, 16 Oct 2026): score >= 80, any exact time
    for C in 'HJ':
        realise(ctx, R, lt[C])                             # real exact time beyond 60 min (ephemeris; an H + J event once per block)
    for C, who in (('H', 'horse'), ('J', 'jockey')):
        row = write_long(ws, row + 1, ctx, lt[C], f'LONG TIMELINE {C}',
                         f"LONG TIMELINE {C} (Eddie, 16 Oct 2026): every timed relationship involving the {who}'s chart ({C}) scoring >= 80 at the off, "
                         'any exact time (same sources and rules as TIMELINE {C}; beyond 60 min the real exact time from the Swiss Ephemeris, up to 1 year each '
                         'way, else "not within 1 year"; linear estimate in the last column); SEPARATING, then '
                         'APPLYING, each by score at the off, highest first (ties by exact time); sky equivalent cells as in TIMELINE {C}'.replace('{C}', C), skyf=skyf)
    field['_tl'] = tl
    field['_lt'] = lt
    for (lab, cn), (d, ev) in field['T16'].items():
        x = lab.split('–', 1)[1]
        a, b = cn[0], cn.split('= ')[1][0]
        thread_add(thr, 'T16', f'Jup–{x} {cn}', (f'{a} {x}', f'{b} {x}'), '', d, ev)
    field['_thr'] = thr
    field['_nums'] = nums
    ws.column_dimensions['B'].width = 46
    ws.freeze_panes = 'C4'
    field['_rats'] = rats
    return field


# ---------------- T24: stars against bodies (Eddie, 19 Oct 2026)
T24_BODIES = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas',
              'Juno', 'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto', 'Rahu', 'Ketu']


def t24_cell(v, pl):
    """-> (fill colour or '', comment text) for a T24 distance: best family (conjunction counts, as T1), else the nearest target outside"""
    ev, _ = nearest(v, 'dist', pl)
    if ev:
        fam = f"conjunction ({pl} < {families.CONJ[pl]})" if ev['family'] == 'conj' else ev['family']
        return ev['colour'], f"{'0' if ev['family'] == 'conj' else ev['target']} · {fam} · {fmt_off(ev)} · {ev['score']:.2f}"
    near = families.outside(v, pl, 'deg')
    return '', f"nearest: {near['target']} · {near['family']} — outside ±{near['tol']:.3g} · {fmt_off(near)}" if near else 'no target'


def t24_mids(ch, x, bodies, pl):
    """T24 midpoints (Eddie, 19 Oct 2026): star x as the middle point of two bodies A, B of the block, the midpoint rule (mid_geom /
    mid_score: closeness >= 90 %, distance half RA ±0.5 closer of near / far, Dec ±0.15 signed; total = the two halves); hits only, best
    total first. Left out: the chart's own Rahu – Ketu, "A, B together" (d(A, B) < 1.5 RA / 0.3 Dec), a Ketu pair repeating the Rahu pair.
    -> [dict(a, b, d1, d2, off, side, close, rscore, dscore, score, dab, pos)]"""
    ix = 0 if pl == 'RA' else 1
    out = []
    for a, b in itertools.combinations(bodies, 2):
        if {a, b} == {'Rahu', 'Ketu'}:
            continue
        dab = plane_value(ch[a], ch[b], pl)
        if dab < families.CONJ[pl]:
            continue
        off, side, d1, d2 = mid_geom(ch[a][ix], ch[b][ix], ch[x][ix], pl)
        m = mid_score(d1, d2, off, pl)
        if not m or not m['hit']:
            continue
        sm = d1 + d2
        out.append(dict(m, a=a, b=b, d1=d1, d2=d2, side=side, dab=dab, pos='between' if abs(dab - sm) <= 0.01 * sm else 'far side'))
    rahu = {(h['a'], h['b'], round(h['d1'], 6), round(h['d2'], 6)) for h in out if 'Rahu' in (h['a'], h['b'])}
    out = [h for h in out if not ('Ketu' in (h['a'], h['b']) and
                                  (*(('Rahu' if z == 'Ketu' else z) for z in (h['a'], h['b'])), round(h['d1'], 6), round(h['d2'], 6)) in rahu)]
    return sorted(out, key=lambda h: -h['score'])


def t24_mid_text(h):
    return f"{h['a']} = {h['b']} {h['score']:.2f} ({h['side'] + ', ' if h['side'] else ''}{h['pos']})"


THICK = openpyxl.styles.Side(style='thick')


def write_t24(ws, row, ch, C, title):
    """T24 block (Eddie, 19 Oct 2026): rows = stars (T1_T2_T24_STARS order, those in the chart; 19 Oct 2026); columns (revised the same day) = every body's RA
    distance (Moon only in the sky), then "RA midpoints", then every body's Dec distance, then "Dec midpoints"; cell = the distance (RA
    wrapped 0-180, Dec |ΔDec|), 6 dp, filled by its best family score (a conjunction red, 20 Oct 2026), comment = target · family · offset · score or the nearest target
    outside, plus a line per midpoint the body is in; the two body cells of a midpoint hit get a thick outline; midpoint column = every hit,
    best total first, coloured by the best. No timing, no +5, no field sheet.
    -> (next row, {(star, body, plane): (v, colour, text)}, {(star, plane): [midpoint hits]})"""
    bodies = [b for b in T24_BODIES if b in ch and ch[b][2] == 'body' and (C == 'S' or b != 'Moon')]
    stars = [x for x in T1_T2_T24_STARS if x in ch]
    n = len(bodies)
    c0 = {'RA': 3, 'Dec': 3 + n + 1}                       # first body column of each half; its midpoint column at c0 + n
    ws.cell(row=row, column=1, value='T24').font = BOLD
    ws.cell(row=row, column=2, value=title).font = BOLD
    row += 1
    for r in (row, row + 1):
        for c, v in ((1, 'table'), (2, 'star')):
            ws.cell(row=r, column=c, value=v if r == row else None).fill = HEAD
    for pl in PLANES:
        c = ws.cell(row=row, column=c0[pl], value=pl); c.fill = HEAD; c.font = BOLD
        for k in range(1, n):
            ws.cell(row=row, column=c0[pl] + k).fill = HEAD
        ws.merge_cells(start_row=row, start_column=c0[pl], end_row=row, end_column=c0[pl] + n - 1)
        for i, b in enumerate(bodies):
            c = ws.cell(row=row + 1, column=c0[pl] + i, value=b); c.fill = HEAD; c.font = BOLD
        for r, v in ((row, f'{pl} midpoints'), (row + 1, 'star = middle of A, B: total (side, between / far side)')):
            c = ws.cell(row=r, column=c0[pl] + n, value=v); c.fill = HEAD; c.font = BOLD
    row += 2
    out, mids = {}, {}
    for x in stars:
        ws.cell(row=row, column=1, value='T24')
        ws.cell(row=row, column=2, value=f'{C} {x}')
        for pl in PLANES:
            hits = t24_mids(ch, x, bodies, pl)
            mids[(x, pl)] = hits
            extra = {b: [] for b in bodies}
            for h in hits:
                extra[h['a']].append(f"midpoint with {h['b']}: total {h['score']:.2f}")
                extra[h['b']].append(f"midpoint with {h['a']}: total {h['score']:.2f}")
            for i, b in enumerate(bodies):
                v = plane_value(ch[x], ch[b], pl)
                colour, text = t24_cell(v, pl)
                c = ws.cell(row=row, column=c0[pl] + i, value=round(v, 6))
                c.number_format = '0.000000'
                if v < families.CONJ[pl]:                  # conjunction (RA < 1.5, Dec < 0.3): red instead of the score fill (Eddie, 20 Oct 2026)
                    c.fill = RED
                elif colour:
                    c.fill = FILL[colour]
                full = '\n'.join([text] + extra[b])
                c.comment = Comment(full, 'T24', width=260, height=40 + 15 * len(extra[b]))
                if extra[b]:
                    c.border = openpyxl.styles.Border(left=THICK, right=THICK, top=THICK, bottom=THICK)
                out[(x, b, pl)] = (v, colour, full)
            if hits:
                c = ws.cell(row=row, column=c0[pl] + n, value='; '.join(t24_mid_text(h) for h in hits))
                c.fill = FILL[families.colour(hits[0]['score'])]
        row += 1
    # display (Eddie, 19 Oct 2026): value columns wide enough for 177.745864, star names ~18, midpoint columns wider; shared columns only
    # ever widened
    widths = [(2, T24_NAME_W)] + [(c0[pl] + k, T24_VAL_W) for pl in PLANES for k in range(n)] + [(c0[pl] + n, T24_MID_W) for pl in PLANES]
    for col, w in widths:
        L = openpyxl.utils.get_column_letter(col)
        if L not in ws.column_dimensions or not ws.column_dimensions[L].customWidth:
            ws.column_dimensions[L].width = w
        else:
            ws.column_dimensions[L].width = max(ws.column_dimensions[L].width, w)
    return row + 1, out, mids


T24_MID_W = 40
T24_VAL_W, T24_NAME_W = 11, 18


T24_NOTE = ('stars against bodies (Eddie, 19 Oct 2026): one row per star; the RA distance of every body, RA midpoints, the Dec '
            'distance of every body, Dec midpoints; cell = the distance (RA wrapped 0–180, '
            'Dec |ΔDec|), coloured by its best family score (green >= 80, yellow 50–80, light < 50; conjunction RA < 1.5 / Dec < 0.3 counts, '
            'as T1, but filled red; no fill outside); cell comment = target · family · offset · score, or the nearest target outside. MIDPOINTS: the star as the '
            'middle point of two bodies A, B (closeness of d(star, A), d(star, B) >= 90 % and the star within RA ±0.5 (closer of near / far) / '
            'Dec ±0.15 of their midpoint; total = ratio half + distance half; hits only, best first; own Rahu – Ketu, "A, B together" (RA < 1.5, '
            'Dec < 0.3) and Ketu repeats of a Rahu pair left out; between / far side as T17); the two body cells get a thick outline and a '
            'comment line. No timing, no +5')


# ---------------- T24 ratio tables (Eddie, 19 Oct 2026; natal only, viewing only)
T24R_NOTE = ('larger / smaller on the interval list (area A ±0.02 absolute, φ and √2 0.15 %, B tapered), squared score, fill green >= 80, '
             'yellow 50–80, light < 50, none outside; comment = interval · name · group · area · offset · score, or the nearest interval '
             'outside; "together" (no ratio, no score) when a distance is within the conjunction tolerance (RA < 1.5, Dec < 0.3), the leg named '
             'in the comment; a unison with the two compared points close: q = d(the two points) / the smaller distance, < 0.0015 grey '
             '"automatic, not counted", 0.0015 to < 0.02 tag "assisted" (as T23). Natal, fixed: no +5, no timing')


def t24r_cell(ws, row, col, legs, pl, qd, close):
    """one T24 ratio cell: legs = [(name, distance), (name, distance)]; qd = distance of the two compared points (automatic / assisted
    unison, as T23 H / J); close = 'H–J Jupiters' / 'Jupiter–X'. -> area of the hit ('A', 'P', 'B') or None (no hit, together, automatic)"""
    (na, a), (nb, b) = legs
    tog = [f'{n} {v:.6f}' for n, v in legs if v < families.CONJ[pl]]
    if tog:
        c = ws.cell(row=row, column=col, value='together')
        c.comment = Comment('together (' + ('RA < 1.5' if pl == 'RA' else 'Dec < 0.3') + '): ' + '; '.join(tog) + ' — no ratio, no score', 'T24', width=260, height=55)
        return None
    v, _, inv = ratio(a, None, b, None)
    ev, _ = nearest(v, 'ratio')
    c = ws.cell(row=row, column=col, value=round(v, 6))
    c.number_format = '0.000000'
    if not ev:
        near = families.outside(v, None, 'ratio')
        c.comment = Comment(f"nearest: {near['target']} · {near['name']} — outside · {fmt_off(near)}" if near else 'no interval', 'T24', width=260, height=40)
        return None
    area = hit_area(ev)
    text = f"{ev['target']} · {ev['name']} · {ev['group']} · {SKY_AREA[area]} · {fmt_off(ev)} · {ev['score']:.2f}"
    if ev['target'] == '1':
        q = qd / min(a, b) if min(a, b) else float('inf')
        if q < AUTO_TOL:
            c.fill = FILL['grey']
            c.comment = Comment(f'{text}\nautomatic ({close} close, q {q:.6f}), not counted', 'T24', width=260, height=55)
            return None
        if q < ASSIST_TOL:
            text += f'\n{close} assisted (q {q:.6f})'
    c.fill = FILL[ev['colour']]
    c.comment = Comment(text, 'T24', width=260, height=40 + 15 * text.count('\n'))
    return area


def t24r_head(ws, row, tid, title, groups, cols):
    """title row; header row 1 'RA' / 'Dec' merged over each plane's columns, row 2 the column names; -> first data row"""
    ws.cell(row=row, column=1, value=tid).font = BOLD
    ws.cell(row=row, column=2, value=title).font = BOLD
    row += 1
    ws.cell(row=row, column=1, value='table').fill = HEAD
    ws.cell(row=row, column=2, value='star').fill = HEAD
    ws.cell(row=row + 1, column=1).fill = HEAD
    ws.cell(row=row + 1, column=2).fill = HEAD
    n = len(cols)
    for i, pl in enumerate(groups):
        c0 = 3 + n * i
        c = ws.cell(row=row, column=c0, value=pl); c.fill = HEAD; c.font = BOLD
        for k in range(1, n):
            ws.cell(row=row, column=c0 + k).fill = HEAD
        ws.merge_cells(start_row=row, start_column=c0, end_row=row, end_column=c0 + n - 1)
        for k, h in enumerate(cols):
            c = ws.cell(row=row + 1, column=c0 + k, value=h); c.fill = HEAD; c.font = BOLD
    widths = [(2, T24_NAME_W)] + [(3 + k, T24_VAL_W) for k in range(n * len(groups))]
    for col, w in widths:                                  # shared columns only ever widened (as T24)
        L = openpyxl.utils.get_column_letter(col)
        if L not in ws.column_dimensions or not ws.column_dimensions[L].customWidth:
            ws.column_dimensions[L].width = w
        else:
            ws.column_dimensions[L].width = max(ws.column_dimensions[L].width, w)
    return row + 2


def t24r_title(tid, what, n):
    return f"{tid} (Eddie, 19 Oct 2026): {what}. {T24R_NOTE}. Hits: A {n['A']}, φ and √2 {n['P']}, B {n['B']}"


def write_t24hj(ws, row, H, J):
    """T24 H / J: one row per star (T1_T2_T24_STARS, in both charts); per plane d(H star, H Jupiter), d(J star, J Jupiter) (the Jupiter
    cells of T24 HORSE / JOCKEY, filled and commented as there, without the midpoint lines) and the ratio H / J. -> row, hits per area"""
    stars = [x for x in T1_T2_T24_STARS if x in H and x in J]
    n = {'A': 0, 'P': 0, 'B': 0}
    body = []
    for x in stars:
        line = [x]
        for pl in PLANES:
            dh, dj = plane_value(H[x], H['Jupiter'], pl), plane_value(J[x], J['Jupiter'], pl)
            line.append((pl, dh, dj))
        body.append(line)
    title_row = row
    row = t24r_head(ws, row, 'T24 H / J', '', PLANES, ('d(H star, H Jupiter)', 'd(J star, J Jupiter)', 'H / J'))
    for line in body:
        x = line[0]
        ws.cell(row=row, column=1, value='T24 H / J')
        ws.cell(row=row, column=2, value=x)
        for i, (pl, dh, dj) in enumerate(line[1:]):
            c0 = 3 + 3 * i
            for k, v in enumerate((dh, dj)):
                colour, text = t24_cell(v, pl)
                c = ws.cell(row=row, column=c0 + k, value=round(v, 6)); c.number_format = '0.000000'
                if v < families.CONJ[pl]:                  # conjunction red, as the T24 Jupiter cells (Eddie, 20 Oct 2026)
                    c.fill = RED
                elif colour:
                    c.fill = FILL[colour]
                c.comment = Comment(text, 'T24', width=260, height=40)
            a = t24r_cell(ws, row, c0 + 2, [(f'H {x}, H Jupiter', dh), (f'J {x}, J Jupiter', dj)], pl,
                          plane_value(H['Jupiter'], J['Jupiter'], pl), 'H–J Jupiters')
            if a:
                n[a] += 1
        row += 1
    ws.cell(row=title_row, column=2, value=t24r_title('T24 H / J', 'd(H star, H Jupiter) / d(J star, J Jupiter) per star, RA and Dec', n))
    return row + 1, n


def write_t24r(ws, row, ch, C, who):
    """T24 HORSE RATIOS / T24 JOCKEY RATIOS: one row per star, one column per body X of the chart (T24 bodies without Jupiter), RA
    columns then Dec columns; cell = d(star, Jupiter) / d(star, X), larger / smaller, same chart. -> row, hits per area"""
    bodies = [b for b in T24_BODIES if b in ch and ch[b][2] == 'body' and b not in ('Moon', 'Jupiter')]
    stars = [x for x in T1_T2_T24_STARS if x in ch]
    n = {'A': 0, 'P': 0, 'B': 0}
    title_row = row
    row = t24r_head(ws, row, f'T24 {who} RATIOS', '', PLANES, bodies)
    for x in stars:
        ws.cell(row=row, column=1, value=f'T24 {who} RATIOS')
        ws.cell(row=row, column=2, value=f'{C} {x}')
        for i, pl in enumerate(PLANES):
            dj = plane_value(ch[x], ch['Jupiter'], pl)
            for k, b in enumerate(bodies):
                a = t24r_cell(ws, row, 3 + len(bodies) * i + k, [(f'{C} {x}, {C} Jupiter', dj), (f'{C} {x}, {C} {b}', plane_value(ch[x], ch[b], pl))],
                              pl, plane_value(ch['Jupiter'], ch[b], pl), 'Jupiter–X')
                if a:
                    n[a] += 1
        row += 1
    ws.cell(row=title_row, column=2, value=t24r_title(f'T24 {who} RATIOS', f'd({C} star, {C} Jupiter) / d({C} star, {C} X) per star and body X', n))
    return row + 1, n


# ---------------- T23: ratios of the T1, T2 and SKY distances (Eddie, 16 Oct 2026)
T23_RATIOS = (('H / J', 'H', 'J'), ('S / H', 'S', 'H'), ('S / J', 'S', 'J'))
T23_W = COLS + 2                                           # per ratio: the 8 value cells, area, timing
T23_DIST = (('S', 'S Jupiter → S X'), ('H', 'H Jupiter → H X'), ('J', 'J Jupiter → J X'))
T23_D = COLS + 1                                           # per distance (16 Oct 2026): the 8 value cells (as T1 / T2 / SKY), timing
T23_PW = len(T23_DIST) * T23_D + len(T23_RATIOS) * T23_W   # one plane: three distances, then the three ratios
t23_dcol = lambda i, k: 3 + T23_PW * i + T23_D * k
t23_rcol = lambda i, j: 3 + T23_PW * i + len(T23_DIST) * T23_D + T23_W * j


def t23_cells(ctx, R, x, pl):
    """{ratio name: (v0, v5, inv, ev, also, together)} for body / star / equator x in plane pl: larger / smaller of d(a Jupiter, a X) and
    d(b Jupiter, b X). S / H and S / J = T12 (automatic and return-assisted unisons as there); H / J natal-only (fixed). together = the
    leg where Jupiter and X are within the conjunction tolerance (RA < 1.5, Dec < 0.3): the cell is left out (no value, no score)"""
    out = {}
    kind = 'eqratio' if x == 'equator' else 'ratio'
    for name, a, b in T23_RATIOS:
        n0, n5 = ctx.pair(R, f'{a} Jupiter', f'{a} {x}', pl)
        d0, d5 = ctx.pair(R, f'{b} Jupiter', f'{b} {x}', pl)
        if n0 is None or d0 is None:
            continue
        tog = [f'{c} Jupiter, {c} {x} {v:.6f}' for c, v in ((a, n0), (b, d0)) if v < families.CONJ['Dec' if x == 'equator' else pl]]
        v0, v5, inv = ratio(n0, n5, d0, d5)
        ev, also = nearest(v0, kind) if v0 and not tog else (None, [])
        if a == 'S':
            ev = unison_kind(ctx, R, b, f'{b} {x}', pl, ev)
        elif ev and ev['target'] == '1':                   # H / J (Eddie, 16 Oct 2026): the Jupiter-return rule with d(H Jupiter, J Jupiter)
            q = ctx.pair(R, 'H Jupiter', 'J Jupiter', pl)[0] / min(n0, d0)
            if q < AUTO_TOL:
                ev = dict(ev, colour='grey', auto='automatic (H–J Jupiters close)', q=q)
            elif q < ASSIST_TOL:
                ev = dict(ev, assisted='H–J assisted', q=q)
        out[name] = (v0, v5, inv, ev, also, tog)
    return out


def write_t23(ws, row, ctx, R):
    """T23 (Eddie, 16 Oct 2026): one row per body, star or equator X in both T1 and T2 (not Jupiter), planes RA and Dec (equator: Dec);
    three ratios per plane, H / J (new, fixed), S / H and S / J (= T12, timing from the off + 5 min); area blocks A, φ and √2, B, no hit
    by the highest area on the row (as T12). -> row, {(X, plane): (v0, ev)} of the H / J cells (FIELD 23), the lines (tests)"""
    xs = [x for x in R['H'] if x in R['J'] and x != 'Jupiter']
    lines = []
    for x in xs:
        cells = {pl: t23_cells(ctx, R, x, pl) for pl in PLANES}
        lines.append((x, {pl: c for pl, c in cells.items() if c}))
    title = ('T23 ratios of the T1, T2 and SKY distances (Eddie, 16 Oct 2026), larger / smaller: H / J = d(H Jupiter, H X) / d(J Jupiter, J X) '
             '(natal, fixed); S / H = d(S Jupiter, S X) / d(H Jupiter, H X) and S / J = d(S Jupiter, S X) / d(J Jupiter, J X) (the T12 values, '
             'repeated; timing from the off + 5 min); interval list, area, group, offset, score; outside: nearest interval plain; Jupiter return '
             'unisons grey (automatic) as in T12; H / J unisons (16 Oct 2026) the same rule with d(H Jupiter, J Jupiter) / the smaller of d(H Jupiter, '
             'H X), d(J Jupiter, J X): < 0.0015 grey "automatic (H–J Jupiters close)", counted nowhere (not in FIELD 23, areas, title counts); '
             '0.0015 to < 0.02 "H–J assisted" (tag only). A ratio with Jupiter and X together on a leg (RA < 1.5, Dec < 0.3) is left out (no value, '
             'no score; the leg is named). Before the ratios, per plane (16 Oct 2026): the distances S Jupiter → S X (= the T1 / T2 SKY cells, timing '
             'from the off + 5 min), H Jupiter → H X (= T1) and J Jupiter → J X (= T2), fixed')
    by = {a: [] for a in families.AREAS + (None,)}
    areas = lambda cells: [hit_area(c[3]) for pc in cells.values() for n, c in pc.items()
                           if not (n == 'H / J' and c[3] and c[3].get('auto'))]    # an automatic H / J unison counts nowhere
    for lab, cells in lines:
        by[row_area(areas(cells))].append((lab, cells))
    out, unis = {}, {}
    for a in families.AREAS + (None,):
        mixed = sum(1 for _, cells in by[a] if multi(areas(cells)))
        ws.cell(row=row, column=1, value='T23').font = BOLD
        ws.cell(row=row, column=2, value=f'{title} — {AREA_NAME[a]}: {len(by[a])} rows' + multi_text(mixed)).font = BOLD
        row += 1
        for i, pl in enumerate(PLANES):
            for k, (_, name) in enumerate(T23_DIST):
                for m, h in enumerate((f'{name} {pl}', '+5 min', 'nearest target', 'group', 'offset', 'score', 'off->+5', 'also (score)', 'timing')):
                    c = ws.cell(row=row, column=t23_dcol(i, k) + m, value=h); c.fill = HEAD; c.font = BOLD
            for j, (name, _, _) in enumerate(T23_RATIOS):
                col = t23_rcol(i, j)
                for k, h in enumerate((f'{name} {pl}', '+5 min', 'interval', 'group', 'offset', 'score', 'off->+5', 'also (score)', 'area', 'timing')):
                    c = ws.cell(row=row, column=col + k, value=h); c.fill = HEAD; c.font = BOLD
        ws.cell(row=row, column=1, value='table').fill = HEAD
        ws.cell(row=row, column=2, value='X').fill = HEAD
        row += 1
        for lab, cells in by[a]:
            ws.cell(row=row, column=1, value='T23'); ws.cell(row=row, column=2, value=lab)
            for i, pl in enumerate(PLANES):
                # distances (Eddie, 16 Oct 2026): S Jupiter → S X (the T1 / T2 SKY cells), H Jupiter → H X (T1), J Jupiter → J X (T2), fixed
                kind = 'equator' if lab == 'equator' else 'dist'
                for k, (C, _) in enumerate(T23_DIST):
                    if C == 'S' and lab not in ctx.S0:
                        continue
                    d0, d5 = ctx.pair(R, f'{C} Jupiter', f'{C} {lab}', pl)
                    if d0 is None:
                        continue
                    dev, dalso = nearest(d0, kind, 'Dec' if kind == 'equator' else pl)
                    put_value(ws, row, t23_dcol(i, k), d0, d5, dev, dalso, ox=(kind, 'Dec' if kind == 'equator' else pl))
                    if dev:
                        ws.cell(row=row, column=t23_dcol(i, k) + COLS, value=exact_time(ctx, d0, d5, dev['tv']) if C == 'S' else 'fixed')
                for j, (name, _, _) in enumerate(T23_RATIOS):
                    if name not in cells.get(pl, {}):
                        continue
                    v0, v5, inv, ev, also, tog = cells[pl][name]
                    col = t23_rcol(i, j)
                    if tog:
                        ws.cell(row=row, column=col + 2, value='together, left out: ' + '; '.join(tog))
                        continue
                    put_value(ws, row, col, v0, v5, ev, also, '' if lab == 'equator' else inv, ox=('eqratio' if lab == 'equator' else 'ratio', pl))
                    if ev and not ev.get('auto'):
                        ws.cell(row=row, column=col + COLS, value=SKY_AREA[hit_area(ev)])
                    if ev:
                        ws.cell(row=row, column=col + COLS + 1, value='fixed' if name == 'H / J' else exact_time(ctx, v0, v5, ev['tv']))
                    if ev and ev['target'] == '1':          # unison: field count written after all runners, as T12
                        unis[('T23' if name == 'H / J' else f'T23 {name}', lab, pl)] = (row, col + 7, ev.get('auto', False), ev.get('assisted', False))
                    if name == 'H / J' and v0 and not (ev and ev.get('auto')):     # automatic H / J unison: not in FIELD 23
                        out[(lab, pl)] = (v0, ev)
            row += 1
        row += 1
    return row, out, lines, unis


# ---------------- T21 / T22: fixed stars (Eddie, 15 Oct 2026)
SIDE_HEAD = ('d(Jup, A)', 'family', 'd(Jup, B)', 'family', 'd(A, B)', 'family', 'ratio (larger / smaller)', 'interval', 'offset', 'score',
             'ratio timing', 'Jupiter', 'note', 'midpoint offset', 'closeness %', 'ratio half', 'distance half', 'midpoint total')


def side_cells(h):
    """one side of a T21 line (the T19 cells without table / block / pair / plane) -> (values, {index: colour})"""
    n, m = h['near'], h['m']
    miss = '' if h['ev'] else f" — outside {tol_text(n)}"
    vals = [*h['fx'][:2], *h['fy'][:2], *h['fxy'][:2], round(h['r0'], 6), f"{n['target']} · {n['name']} · {n['group']}" + miss, fmt_off(n),
            round(h['ev']['score'], 2) if h['ev'] else None, h['timing'], h['pos'], h['note'] or None]
    vals += ([mid_tcells(m)[0], round(m['close'], 4), *mid_tcells(m)[1:], round(m['score'], 2) if m['hit'] else None] if m else [None] * 5)
    if h['together']:                                      # Eddie 16 Oct: a together side plain - values kept, no score, no colour
        for k in (9, 15, 16, 17):
            vals[k] = None
        return vals, {}
    fill = {1 + 2 * k: f[2] for k, f in enumerate((h['fx'], h['fy'], h['fxy'])) if f[2]}
    if h['ev']:
        fill[6] = fill[9] = h['ev']['colour']
    if h['mid'] is not None:
        fill[17] = m['colour']
    return vals, fill


def row_best(h):
    return max(h['ev']['score'] if h['ev'] else -1, -1 if h['mid'] is None else h['mid'])


T21_CELLS = (('d(Jup, A)', 0), ('d(Jup, B)', 1))         # never d(A, B): star-star distances barely change birth -> race day (Eddie 15 Oct)
T19_CELLS = (('d(S Jup, X)', 0), ('d(S Jup, Y)', 1), ('d(X, Y)', 2))   # T19: d(X, Y) counts, bodies move birth -> race day (Eddie 15 Oct)


def t19_sky(ctx, R):
    """T19 sky side (Eddie, 15 Oct 2026): S Jupiter on S X – S Y for every natal-body / royal-star pair (no star-star), same order as the
    natal pairs, every plane; once per race (sky only) -> {(X, Y, plane): row}"""
    if getattr(ctx, 't19sky', None) is None:
        pts = [f'S {b}' for b in NATAL_BODIES if b in ctx.S0] + [f'S {x}' for x in STARS if x in ROYAL and x in ctx.S0]
        prs = [(a, b) for a, b in itertools.combinations(pts, 2) if not (a[2:] in ROYAL and b[2:] in ROYAL)]
        ctx.t19sky = {(h['x'][2:], h['y'][2:], h['plane']): h for h in
                      pair_rows(ctx, R, STARS, tid='T19', jup='S Jupiter', blocks=[('S–S', prs)], dedupe=False)}
    return ctx.t19sky


def t21_same(h, s, cells=None):
    """'same as sky' on a T21 side (Eddie, 15 Oct 2026): the natal side and the sky side hit the same target in the same cell - a distance
    from Jupiter (d(Jup, A), d(Jup, B); never d(A, B)) on the same family and number (x10 / /10 folded as in NUMBERS), or the ratio on the
    same interval -> list of texts"""
    out = []
    if h is None or s is None:
        return out
    for name, i in cells or T21_CELLS:
        a, b = h['best'][i], s['best'][i]
        if a and b and a['family'] != 'conj' and b['family'] != 'conj' and a.get('tv') and b.get('tv') and \
                num_key(a['family'], a['tv']) == num_key(b['family'], b['tv']):
            out.append(f"{name} {a['family']} {a['target']} | sky {b['target']}")
    if h['ev'] and s['ev'] and h['ev']['target'] == s['ev']['target']:
        out.append(f"ratio {h['ev']['target']} · {h['ev']['name']}")
    return out


def write_t21(ws, row, ctx, R, royal=False):
    """T21 (Eddie, 15 Oct 2026): natal Jupiter on natal star pairs, all 22 stars, each chart's own star positions; horse 'H Jupiter: H A –
    H B' | jockey 'J Jupiter: J A – J B' side by side per star pair and plane (RA, Dec, Equator when the three straddle the equator).
    T19 cells per side; a line is listed when either side has a midpoint hit (any total) or a ratio hit scoring >= 50 (Eddie 15 Oct, revised;
    together sides left out); best first by the higher of the ratio score and the midpoint total. All natal: 'fixed'."""
    tid = 'T21R' if royal else 'T21'                       # T21R (Eddie, 16 Oct 2026): the six royal pairs only, every line listed
    stars = [x for x in STARS if x in ROYAL] if royal else STARS
    sides = {}
    for C in 'HJ':
        pts = [f'{C} {x}' for x in stars if x in R[C]]
        for h in pair_rows(ctx, R, STARS, tid='T21', jup=f'{C} Jupiter', blocks=[(f'{C}–{C}', list(itertools.combinations(pts, 2)))]):
            sides.setdefault((h['x'][2:], h['y'][2:], h['plane']), {})[C] = h
    # Eddie 15 Oct (revised): a side counts with a midpoint hit (any total) or a ratio hit scoring >= 50; together sides left out
    ok = lambda h: h is not None and not h['together'] and (h['mid'] is not None or (h['ev'] is not None and h['ev']['score'] >= T21_RMIN))
    lines = [(k, v) for k, v in sides.items() if royal or ok(v.get('H')) or ok(v.get('J'))]
    # sky side (Eddie 15 Oct): S Jupiter on the same sky star pair and plane; never adds or removes a line
    spts = [f'S {x}' for x in stars if x in ctx.S0]
    sky = {(h['x'][2:], h['y'][2:], h['plane']): h for h in
           pair_rows(ctx, R, STARS, tid='T21', jup='S Jupiter', blocks=[('S–S', list(itertools.combinations(spts, 2)))])}
    lines.sort(key=lambda kv: -max(row_best(kv[1][C]) if ok(kv[1].get(C)) else -1 for C in 'HJ'))
    ws.cell(row=row, column=1, value=tid).font = BOLD
    ws.cell(row=row, column=2, value=('T21R ROYAL STARS ONLY (Eddie, 16 Oct 2026): T21 for the six pairs of Aldebaran, Regulus, Antares, Fomalhaut, '
                                      'every line listed (hits and non-hits; a line with no counted side in NO HIT), same cells, areas and tags. ' if royal else '')
            + 'T21 natal Jupiter on natal star pairs (all 22 stars, each chart\'s own positions): horse H Jupiter: H A – H B | '
            'jockey J Jupiter: J A – J B, per star pair and plane (RA, Dec; Equator only when the three straddle the equator). Cells as T19: the three '
            'distances with their family, ratio d(Jup, A) / d(Jup, B) on the interval list (area A ±0.02 absolute, area B tapered %), midpoint (closeness >= 90 %, '
            'ratio half + distance half), between / far side, together. Listed when either side has a midpoint hit (any total) or a ratio hit '
            'scoring >= 50 (together left out); best first by the higher of the ratio score and the midpoint total. '
            'Natal sides: timing fixed. SKY side (Eddie, 15 Oct 2026): S Jupiter: S A – S B, the same star pair and plane at race time, '
            'the same cells, timing from the off + 5 min; it never adds or removes a line. "same as sky": the horse or jockey side and the '
            'sky side hit the same target in the same cell (d(Jup, A) or d(Jup, B) on the same family and number, x10 / /10 folded; '
            'the ratio on the same interval; never d(A, B), star-star distances barely change)').font = BOLD
    row += 1
    ws.cell(row=row, column=4, value='HORSE: H Jupiter on H star A – H star B').font = BOLD
    ws.cell(row=row, column=4 + len(SIDE_HEAD), value='JOCKEY: J Jupiter on J star A – J star B').font = BOLD
    ws.cell(row=row, column=4 + 2 * len(SIDE_HEAD), value='SKY: S Jupiter on S star A – S star B').font = BOLD
    row += 1
    for k, hh in enumerate(('table', 'star pair', 'plane') + tuple(f'H {x}' for x in SIDE_HEAD) + tuple(f'J {x}' for x in SIDE_HEAD)
                           + tuple(f'S {x}' for x in SIDE_HEAD) + ('same as sky',)):
        c = ws.cell(row=row, column=1 + k, value=hh); c.fill = HEAD; c.font = BOLD
    row += 1
    out = []
    # areas (Eddie, 15 Oct 2026): a line goes in A if a counted side (not together) has an A interval (>= 50) or a midpoint hit, else B
    side_areas = lambda h: ([hit_area(h['ev'] if h['ev'] and h['ev']['score'] >= T21_RMIN else None), hit_area(None, h['mid'] is not None)]
                            if ok(h) else [])
    sareas = lambda v: [x for C in 'HJ' for x in side_areas(v.get(C))]
    larea = lambda v: row_area(sareas(v))
    blocks = [(a, [kv for kv in lines if larea(kv[1]) == a]) for a in families.AREAS + ((None,) if royal else ())]
    seq = []
    for a, blk in blocks:
        seq.append(('title', f'{tid} {AREA_NAME[a]}: {len(blk)} lines' + multi_text(sum(multi(sareas(kv[1])) for kv in blk))))
        seq += [('line', kv) for kv in blk]
        seq.append(('gap', None))
    for kind, item in seq:
        if kind == 'title':
            ws.cell(row=row, column=1, value=item).font = BOLD
            row += 1
            continue
        if kind == 'gap':
            row += 1
            continue
        (a, b, pl), v = item
        ws.cell(row=row, column=1, value=tid); ws.cell(row=row, column=2, value=f'{a} – {b}'); ws.cell(row=row, column=3, value=pl)
        s = sky.get((a, b, pl))
        for i, C in enumerate('HJS'):
            h = s if C == 'S' else v.get(C)
            if h is None:
                continue
            vals, fill = side_cells(h)
            c0 = 4 + i * len(SIDE_HEAD)
            for k, x in enumerate(vals):
                ws.cell(row=row, column=c0 + k, value=x)
            for k, col in fill.items():
                ws.cell(row=row, column=c0 + k).fill = FILL[col]
            for k in (9, 17):
                ws.cell(row=row, column=c0 + k).number_format = '0.00'
        same = {C: t21_same(v.get(C), s) for C in 'HJ'}
        if same['H'] or same['J']:
            ws.cell(row=row, column=4 + 3 * len(SIDE_HEAD),
                    value='same as sky — ' + '; '.join(f'{C}: ' + ', '.join(same[C]) for C in 'HJ' if same[C]))
        out.append({'pair': f'{a} – {b}', 'plane': pl, 'H': v.get('H'), 'J': v.get('J'), 'S': s, 'same': same, 'area': larea(v)})
        row += 1
    return row, out


T22_HEAD = ('d(star, S Jup)', 'family', 'd(star, natal Jup)', 'family', 'ratio (larger / smaller)', 'interval', 'offset', 'score', 'off->+5',
            'ratio timing', 'midpoint offset', 'closeness %', 'ratio half', 'distance half', 'midpoint total')


def t22_line(ctx, R, star, C, pl):
    """the star (race-day position) as the apex: d(star, S Jupiter) / d(star, C Jupiter), larger / smaller (orientation fixed at the off),
    on the interval list with timing from the off + 5 min; midpoint cells when closeness >= 90 % (the star the middle point between the
    two Jupiters). Equator only when the three straddle the equator. -> dict or None"""
    st, sj, cj = f'S {star}', 'S Jupiter', f'{C} Jupiter'
    if pl == 'Equator':
        ps = [ctx.pos(R, q, 0) for q in (st, sj, cj)]
        if None in ps or (ps[0][1] >= 0) == (ps[1][1] >= 0) == (ps[2][1] >= 0):
            return None
    (d1, d15), (d2, d25) = eq_dist2(ctx, R, st, sj, pl), eq_dist2(ctx, R, st, cj, pl)
    if not d1 or not d2:
        return None
    flip = d1 < d2
    r0 = d1 / d2 if not flip else d2 / d1
    n5, m5 = (d1 if d15 is None else d15), (d2 if d25 is None else d25)
    r5 = 'n/a' if 'n/a' in (d15, d25) or not n5 or not m5 else (n5 / m5 if not flip else m5 / n5)
    ev = families.best(r0, None, 'ratio')
    near = ev or families.outside(r0, None, 'ratio')
    m = jup_mid(ctx, R, st, sj, cj, pl, d1, d2) if 100.0 / r0 >= 100.0 - MID_RTOL else None
    return {'d1': d1, 'f1': eq_family(ctx, d1, d15, pl), 'd2': d2, 'd25': d25, 'f2': eq_family(ctx, d2, d25, pl), 'r0': r0, 'r5': r5, 'ev': ev,
            'near': near, 'timing': exact_time(ctx, r0, r5, near['tv']) if r5 != 'n/a' else 'n/a (rate)', 'm': m,
            'mid': m['score'] if m and m['hit'] else None}


def write_t22(ws, row, ctx, R, royal=False):
    """T22 (Eddie, 15 Oct 2026): each fixed star (race-day position) as the apex, sky Jupiter against natal Jupiter; one line per star and
    plane, horse d(star, S Jup) / d(star, H Jup) | jockey d(star, S Jup) / d(star, J Jup); every star listed, hits coloured"""
    tid = 'T22R' if royal else 'T22'                       # T22R (Eddie, 16 Oct 2026): the four royal stars only, every line listed
    ws.cell(row=row, column=1, value=tid).font = BOLD
    ws.cell(row=row, column=2, value=('T22R ROYAL STARS ONLY (Eddie, 16 Oct 2026): T22 for Aldebaran, Regulus, Antares, Fomalhaut, every line listed. '
                                      if royal else '') + 'T22 fixed star as the apex (race-day position), sky Jupiter against natal Jupiter: horse d(star, S Jupiter) / '
            'd(star, H Jupiter) | jockey d(star, S Jupiter) / d(star, J Jupiter), larger / smaller on the interval list (area A ±0.02 absolute, area B tapered %; timing '
            'from the off + 5 min, sky Jupiter and the star move); midpoint cells when closeness >= 90 % (the star the middle point between S Jupiter and '
            'natal Jupiter; ratio half + distance half). Planes RA, Dec, Equator (only when the three straddle the equator). Every star listed').font = BOLD
    row += 1
    ws.cell(row=row, column=4, value='HORSE: d(star, S Jupiter) / d(star, H Jupiter)').font = BOLD
    ws.cell(row=row, column=4 + len(T22_HEAD), value='JOCKEY: d(star, S Jupiter) / d(star, J Jupiter)').font = BOLD
    row += 1
    for k, hh in enumerate(('table', 'star', 'plane') + tuple(f'H {x}' for x in T22_HEAD) + tuple(f'J {x}' for x in T22_HEAD)):
        c = ws.cell(row=row, column=1 + k, value=hh); c.fill = HEAD; c.font = BOLD
    row += 1
    out, allv = [], []
    for star in STARS:
        if f'{star}' not in ctx.S0 or (royal and star not in ROYAL):
            continue
        for pl in EQ_PLANES:
            v = {C: t22_line(ctx, R, star, C, pl) for C in 'HJ'}
            if any(v.values()):
                allv.append((star, pl, v))
    # areas (Eddie, 15 Oct 2026): A (an A interval or a midpoint hit on either side), B (a B interval), no hit; order as before
    sareas = lambda v: [x for h in v.values() if h for x in (hit_area(h['ev']), hit_area(None, h['mid'] is not None))]
    larea = lambda v: row_area(sareas(v))
    seq = []
    for a in families.AREAS + (None,):
        blk = [x for x in allv if larea(x[2]) == a]
        seq.append((None, f'{tid} {AREA_NAME[a]}: {len(blk)} lines' + multi_text(sum(multi(sareas(x[2])) for x in blk)), None))
        seq += blk
        seq.append((None, None, None))
    for star, pl, v in seq:
        if star is None:
            if pl:
                ws.cell(row=row, column=1, value=pl).font = BOLD
            row += 1
            continue
        ws.cell(row=row, column=1, value=tid); ws.cell(row=row, column=2, value=star); ws.cell(row=row, column=3, value=pl)
        for i, C in enumerate('HJ'):
            h = v[C]
            if h is None:
                continue
            n, m = h['near'], h['m']
            vals = [*h['f1'][0][:2], *h['f2'][0][:2], round(h['r0'], 6),
                    f"{n['target']} · {n['name']} · {n['group']}" + ('' if h['ev'] else f" — outside {tol_text(n)}"), fmt_off(n),
                    round(h['ev']['score'], 2) if h['ev'] else None,
                    h['r5'] if h['r5'] == 'n/a' else arrow(h['r0'], h['r5'], n), h['timing']]
            vals += ([mid_tcells(m)[0], round(m['close'], 4), *mid_tcells(m)[1:], round(m['score'], 2) if m['hit'] else None] if m else [None] * 5)
            c0 = 4 + i * len(T22_HEAD)
            for k, x in enumerate(vals):
                ws.cell(row=row, column=c0 + k, value=x)
            for k, f in ((1, h['f1'][0]), (3, h['f2'][0])):
                if f[2]:
                    ws.cell(row=row, column=c0 + k).fill = FILL[f[2]]
            if h['ev']:
                ws.cell(row=row, column=c0 + 4).fill = ws.cell(row=row, column=c0 + 7).fill = FILL[h['ev']['colour']]
            if h['mid'] is not None:
                ws.cell(row=row, column=c0 + 14).fill = FILL[m['colour']]
            for k in (7, 14):
                ws.cell(row=row, column=c0 + k).number_format = '0.00'
        out.append({'pair': star, 'plane': pl, 'H': v['H'], 'J': v['J'], 'area': larea(v)})
        row += 1
    return row, out


T21_RMIN = 50.0                                            # T21 / FIELD 21: ratio hits count at >= 50 (Eddie 15 Oct); midpoints at any total


def field_star_sheet(wb, tid, title, runners, fields, rmin=0.0, every=False):
    """FIELD 21 / FIELD 22 (Eddie, 15 Oct 2026): rows = star pairs (T21) / stars (T22), runners as columns; each hit as side, plane and score
    (ratio: the interval; midpoint: total); last column = runners with a hit (k/n). Hits = a ratio on an interval scoring >= rmin
    (T21: 50) or a midpoint hit."""
    ws = wb.create_sheet(f'FIELD {tid[1:]}')
    ws.cell(row=1, column=1, value=f'{tid} field matrix — {title}; per runner every hit: side (H / J), plane, ratio on an interval '
            f"(interval, score{', >= ' + format(rmin, 'g') if rmin else ''}) or midpoint (total); cell coloured by its best hit; last column = runners "
            'with a hit (k/n)').font = BOLD
    order = sorted(runners)
    ws.cell(row=3, column=1, value='star pair' if tid.startswith('T21') else 'star').fill = HEAD
    for i, P in enumerate(order):
        c = ws.cell(row=3, column=2 + i, value=f"{P} {runners[P]['name']}"); c.fill = HEAD; c.font = BOLD
        ws.column_dimensions[openpyxl.utils.get_column_letter(2 + i)].width = 40
    last = 2 + len(order)
    c = ws.cell(row=3, column=last, value='runners with a hit in that area'); c.fill = HEAD; c.font = BOLD
    keys = []
    for P in order:
        for h in fields[P][tid]:
            if h['pair'] not in keys:
                keys.append(h['pair'])
    if tid.startswith('T22'):
        keys = [x for x in STARS if x in keys]
    hits = {}                                              # (key, P) -> [(area, score, colour, text)]
    for P in order:
        for line in fields[P][tid]:
            for C in 'HJ':
                h = line[C]
                if h is None or h.get('together'):
                    continue
                key = (line['pair'], P)
                if h['ev'] and h['ev']['score'] >= rmin:
                    hits.setdefault(key, []).append((families.area(h['ev']['target']), h['ev']['score'], h['ev']['colour'],
                                                     f"{C} {line['plane']} {h['ev']['target']} ({h['ev']['score']:.2f})"))
                if h['mid'] is not None:
                    side = f" {h['m']['side']}" if h['m']['side'] else ''
                    hits.setdefault(key, []).append(('A', h['mid'], h['m']['colour'], f"{C} {line['plane']}{side} midpoint ({h['mid']:.2f})"))
    r = 4
    for a in families.AREAS:                               # areas (Eddie, 15 Oct 2026): A (A interval or midpoint), φ and √2, B; k/n per area
        rows = [key for key in keys if any(t[0] == a for P in order for t in hits.get((key, P), []))]
        ws.cell(row=r, column=1, value=f'{AREA_NAME[a]}: {len(rows)} rows').font = BOLD
        r += 1
        for key in rows:
            ws.cell(row=r, column=1, value=key).font = BOLD
            k = 0
            for i, P in enumerate(order):
                hs = sorted([t for t in hits.get((key, P), []) if t[0] == a], key=lambda t: -t[1])
                if not hs:
                    continue
                k += 1
                c = ws.cell(row=r, column=2 + i, value='\n'.join(t[3] for t in hs))
                if hs[0][2] in FILL:
                    c.fill = FILL[hs[0][2]]
                c.alignment = Alignment(wrap_text=True, vertical='top')
            ws.cell(row=r, column=last, value=f'{k}/{len(order)}')
            r += 1
        r += 1
    if every:                                              # FIELD 21R / 22R (Eddie 16 Oct): every line, the rest with no hit
        rows = [key for key in keys if not any(hits.get((key, P)) for P in order)]
        ws.cell(row=r, column=1, value=f'NO HIT: {len(rows)} rows').font = BOLD
        r += 1
        for key in rows:
            ws.cell(row=r, column=1, value=key).font = BOLD
            ws.cell(row=r, column=last, value=f'0/{len(order)}')
            r += 1
    ws.column_dimensions['A'].width = 26
    ws.freeze_panes = 'B4'


T20_BODIES = [x for x in NATAL_BODIES if x != 'Jupiter']   # bodies only: no stars, no Moon (no natal Moon), not Jupiter


def write_t20(ws, row, ctx, R, thr=None):
    """T20 (Eddie, 15 Oct 2026): natal Jupiter as the midpoint of sky X and natal X. Horse: S X / H X | H Jupiter; jockey: S X / J X |
    J Jupiter; every body X in the sky and in that chart (no stars, no Moon, not Jupiter). Planes RA (closer of near / far), Dec, Equator,
    on the current midpoint scoring (as T10 / T11, same columns, timing from the off + 5 min). Horse and jockey on one line per body.
    Every hit goes to THREADS as a Jupiter-X link, counted at total >= 50 (as every hit). -> (row, {body: {'H': {plane: line}, 'J': {...}}})"""
    ws.cell(row=row, column=1, value='T20').font = BOLD
    ws.cell(row=row, column=2, value='T20 natal Jupiter as the midpoint of sky X and natal X: horse S X / H X | H Jupiter, jockey S X / J X | J Jupiter '
            '(bodies only, no stars, no Moon, not Jupiter)  [midpoint scoring as T10 / T11: closeness of natal Jupiter\'s distances to S X and natal X '
            'at least 90 %, ratio half (10 (10 − (100 − closeness)) / 10)² x 0.5; distance half = its signed offset from the midpoint, squared on '
            'RA ±0.5, Dec ±0.15, Equator ±0.15, x 0.5; a hit needs both, total = the sum; otherwise plain. RA: the closer of the near and far '
            'midpoint. Equator only when the three are not all on one side. Timing: the ratio toward unison, from the off and +5 min]').font = BOLD
    row += 1
    starts, col = {}, 3
    for C, side in (('H', 'HORSE: S X / H X | H Jupiter'), ('J', 'JOCKEY: S X / J X | J Jupiter')):
        ws.cell(row=row, column=col, value=side).font = BOLD
        for pl in MID_PLANES:
            starts[(C, pl)] = col
            col += len(MID_HEAD[pl])
    row += 1
    ws.cell(row=row, column=1, value='table').fill = HEAD
    ws.cell(row=row, column=2, value='body').fill = HEAD
    for (C, pl), c0 in starts.items():
        for k, h in enumerate(MID_HEAD[pl]):
            c = ws.cell(row=row, column=c0 + k, value=f'{C} {h}'); c.fill = HEAD; c.font = BOLD
    row += 1
    tri = {C: [(f'S {x} / {C} {x} | {C} Jupiter', f'S {x}', f'{C} {x}', f'{C} Jupiter') for x in T20_BODIES if x in R[C] and x in ctx.S0]
           for C in 'HJ'}
    data = {C: {pl: mid_rows(ctx, R, tri[C], pl) for pl in MID_PLANES} for C in 'HJ'}
    out = {}
    for x in T20_BODIES:
        if not any(x in R[C] for C in 'HJ') or x not in ctx.S0:
            continue
        ws.cell(row=row, column=1, value='T20')
        ws.cell(row=row, column=2, value=x)
        out[x] = {'H': {}, 'J': {}}
        for C in 'HJ':
            lab = f'S {x} / {C} {x} | {C} Jupiter'
            for pl in MID_PLANES:
                h = data[C][pl].get(lab)
                if not h:
                    continue
                out[x][C][pl] = h
                c0 = starts[(C, pl)]
                for k, v in enumerate(mid_cells(h, pl)):
                    ws.cell(row=row, column=c0 + k, value=v)
                if h['hit']:
                    n = len(MID_HEAD[pl])
                    ws.cell(row=row, column=c0).fill = FILL[h['colour']]
                    ws.cell(row=row, column=c0 + n - 2).fill = FILL[h['colour']]
                    for k in range(n - 4, n - 1):
                        ws.cell(row=row, column=c0 + k).number_format = '0.00'
                    if thr is not None:                    # THREADS: a Jupiter-X link, counted at total >= 50 (as every hit)
                        ev = {'target': f"{h['side'] + ' ' if h['side'] else ''}midpoint", 'score': h['score'], 'colour': h['colour']}
                        thread_add(thr, 'T20', 'mid ' + short(lab), (f'S {x}', f'{C} {x}', f'{C} Jupiter'), pl, h['o0'], ev)
        row += 1
    return row + 1, out


def field_t20_sheet(wb, runners, fields):
    """FIELD 20 (Eddie, 15 Oct 2026): bodies as rows, runners as columns; each T20 hit with its chart, plane and score; runners with a hit k/n"""
    ws = wb.create_sheet('FIELD 20')
    ws.cell(row=1, column=1, value='T20 field matrix — natal Jupiter as the midpoint of sky X and natal X (H: S X / H X | H Jupiter; J: S X / J X | '
            'J Jupiter); per runner every midpoint hit: chart, plane (RA near / far), total; cell coloured by its best hit; last column = runners '
            'with a hit on that body (k/n)').font = BOLD
    order = sorted(runners)
    ws.cell(row=3, column=1, value='body').fill = HEAD
    for i, P in enumerate(order):
        c = ws.cell(row=3, column=2 + i, value=f"{P} {runners[P]['name']}"); c.fill = HEAD; c.font = BOLD
        ws.column_dimensions[openpyxl.utils.get_column_letter(2 + i)].width = 34
    last = 2 + len(order)
    c = ws.cell(row=3, column=last, value='runners with a hit'); c.fill = HEAD; c.font = BOLD
    r = 4
    for x in T20_BODIES:
        if not any(x in fields[P]['T20'] for P in order):
            continue
        ws.cell(row=r, column=1, value=x).font = BOLD
        k = 0
        for i, P in enumerate(order):
            hits = [(C, pl, h) for C in 'HJ' for pl, h in fields[P]['T20'].get(x, {}).get(C, {}).items() if h['hit']]
            if not hits:
                continue
            k += 1
            hits.sort(key=lambda t: -t[2]['score'])
            c = ws.cell(row=r, column=2 + i, value='\n'.join(f"{C} {pl}{' ' + h['side'] if h['side'] else ''} {h['score']:.2f}" for C, pl, h in hits))
            c.fill = FILL[hits[0][2]['colour']]
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(row=r, column=last, value=f'{k}/{len(order)}')
        r += 1
    ws.column_dimensions['A'].width = 16
    ws.freeze_panes = 'B4'


AUTO_TOL = 0.0015                                          # Eddie's rule (13 Oct), kept when the ratio tolerances tapered


ASSIST_TOL = 0.02                                          # return-assisted: AUTO_TOL <= d1/d2 < 0.02 (tag only)


def auto_text(a):
    """automatic unison label: T23 H / J carries its own ('automatic (H–J Jupiters close)'), else the Jupiter return"""
    return a if isinstance(a, str) else 'automatic (Jupiter return)'


def assist_text(a):
    return a if isinstance(a, str) else 'return-assisted'


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
                continue
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
EQ_PLANES = ('RA', 'Dec', 'Equator')                       # Flat and GC removed (Eddie, 14 Oct 2026)
EQ_HEAD = ('table', 'Jupiter: X = Y', 'plane', 'd(Jup, X)', 'd(Jup, Y)', 'closeness %', 'midpoint offset',
           'ratio half', 'distance half', 'total', 'Jupiter',
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


def exact_t(v0, v5, target):
    """minutes from the off until v reaches target, linear from the off to +5 min; None without motion (fixed, n/a, no motion)"""
    if v5 is None or v5 == 'n/a' or v5 == v0:
        return None
    return (target - v0) / ((v5 - v0) / 5.0)


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
    """best family hit of a distance with its score, and its timing when it has a sky leg; no conjunction in the Equator plane
    (Eddie, 15 Oct 2026: an Equator distance under 0.3 shows a number family or nothing)"""
    b = families.best(v0, pl if pl in ('RA', 'Dec') else None, 'deg')
    if not b:
        return (round(v0, 6), 'no family', ''), None       # (value cell, family cell, family cell colour)
    return (round(v0, 6), f"→ {b['target']} ({b['family']}, {b['score']:.2f}) · {exact_time(ctx, v0, v5, b['tv'])}", b['colour']), b


def equi_line(ctx, R, jup, x, y, pl, tid):
    """one plane of Jupiter's distances to X and Y -> dict (inside = within unison 1 %) or None (plane not measured).
    A chart's own Rahu and Ketu are never paired, in any plane (Eddie, 14 Oct); Equator only when Jupiter, X and Y are not all on one
    side of the equator (else it repeats Dec)."""
    tol = families.TOL['1']
    if own_nodes(x, y):
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
    m = jup_mid(ctx, R, jup, x, y, pl, dx, dy)             # midpoint scoring (Eddie 14 Oct): ratio half + distance half, both inside
    base = {'tid': tid, 'label': f'{jup}: {x} = {y}', 'key': (f'{jup}: {x} = {y}', pl), 'plane': pl, 'd1': dx, 'd2': dy,
            'ratio': min(dx, dy) / max(dx, dy), 'off': m['dev'], 'inside': m['hit'], 'together': together, 'm': m}
    if not m['hit']:
        return base
    sc = m['score']
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
    if r5 is None or r5 == 'n/a':
        q0 = q5 = None
    fams = [eq_family(ctx, dx, dx5, pl)[0], eq_family(ctx, dy, dy5, pl)[0],
            eq_family(ctx, dxy, dxy5, pl)[0] if dxy else (None, None, '')]
    pos = 'between' if dxy is not None and abs(dxy - sm) <= 0.01 * sm else 'far side'
    if together:                                           # Eddie 14 Oct: X and Y in conjunction in that plane
        pos += ' · X, Y together'
    return dict(base, together=together, fams=fams, r5=r5, arrow=arw, timing=tim, score=sc, colour=families.colour(sc), pos=pos,
                dxy=dxy, sum=sm, q=(q0, q5), pts=(x, y))


def jup_mid(ctx, R, jup, x, y, pl, dx, dy):
    """Jupiter's offset from the midpoint of X and Y in the plane (RA: the closer of near / far) -> mid_score with d(Jup, X), d(Jup, Y)"""
    ix = 0 if pl == 'RA' else 1
    px, py, pj = (ctx.pos(R, p, 0) for p in (x, y, jup))
    g = mid_geom(px[ix], py[ix], pj[ix], 'RA' if pl == 'RA' else pl)
    off, side = (g[0], g[1]) if g else (float('inf'), '')
    return dict(mid_score(dx, dy, off, pl), side=side)


def mid_tcells(m):
    """midpoint offset (with near / far in RA), ratio half, distance half"""
    side = f" {m['side']}" if m['side'] else ''
    return [f"{m['off']:+.6f}{side}" + ('' if m['din'] else f" (outside ±{m['dtol']})"),
            round(m['rscore'], 2) if m['hit'] else None, round(m['dscore'], 2) if m['hit'] else None]   # a non-hit has no score (as T10 / T11)


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
             'ratio (larger / smaller)', 'interval', 'offset', 'score', 'ratio timing', 'Jupiter', 'note', 'midpoint offset', 'closeness %', 'ratio half',
             'distance half', 'midpoint total')


def pair_points(R, C, stars):
    return [f'{C} {b}' for b in NATAL_BODIES if b in R[C]] + [f'{C} {x}' for x in stars if x in R[C]]


def pair_rows(ctx, R, stars, t17keys=frozenset(), tid='T19', sky=False, jup='S Jupiter', blocks=None, dedupe=True):
    """S Jupiter on every pair X-Y: blocks H-H, J-J, H-J across (sky: S-S, the points given: stars or sky bodies), every plane. No star-star pairs on a runner (sky:
    star-star only). Each row: the three distances with their best family (score, timing), the ratio d(S Jup, X) / d(S Jup, Y)
    (larger / smaller) on the interval list with the tapered tolerances (timing), between / far side, 'X, Y together' tag.
    A Ketu row with the same numbers as the Rahu row is dropped. A unison row also in T17 is marked."""
    if blocks is not None:                                 # T21 (15 Oct): natal Jupiter on that chart's star pairs
        pass
    elif sky:
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
            if own_nodes(x, y):                            # a chart's own Rahu-Ketu pair: never, any plane (Eddie 14 Oct)
                continue
            for pl in EQ_PLANES:
                if pl == 'Equator':
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
                ev = families.best(r0, None, 'ratio')        # the ratio on the interval list only (unison 1 %, 16/15 its own tolerance)
                # the midpoint in its own cells (Eddie 15 Oct): closeness >= 90 % and the distance half, total = the two halves
                m = jup_mid(ctx, R, jup, x, y, pl, dx, dy) if 100.0 / r0 >= 100.0 - MID_RTOL else None
                near = ev or families.outside(r0, None, 'ratio')
                tim = (exact_time(ctx, r0, None if r5 is None else r5, near['tv']) if r5 != 'n/a' else 'n/a (rate)')
                sm = dx + dy
                pos = 'between' if dxy is not None and abs(dxy - sm) <= 0.01 * sm else 'far side'
                together = dxy is not None and dxy < (families.CONJ['RA'] if pl == 'RA' else families.CONJ['Dec'])
                note = []
                if together:
                    note.append('X, Y together')
                lab = f'{jup}: {x} = {y}'
                if m and m['hit'] and (lab, pl) in t17keys:
                    note.append('(also T17)')
                rq = (r0, None if r5 in (None, 'n/a') else r5)          # TIMELINE (16 Oct): the ratio and the legs, off and +5
                legs = [((jup, x), dx, dx5, bx), ((jup, y), dy, dy5, by), ((x, y), dxy, dxy5, bxy)]
                out.append({'tid': tid, 'block': blk, 'x': x, 'y': y, 'pair': f'{x} – {y}', 'plane': pl, 'fx': fx, 'fy': fy, 'fxy': fxy, 'm': m,
                            'rq': rq, 'legs': legs, 'jup': jup,
                            'mid': m['score'] if m and m['hit'] else None,
                            'allfam': bool(bx and by and bxy), 'r0': r0, 'ev': ev, 'near': near, 'timing': tim, 'pos': pos,
                            'together': together, 'note': '; '.join(note), 'sig': (round(dx, 6), round(dy, 6)), 'best': (bx, by, bxy)})
    if not dedupe:                                         # T19 sky side: every pair measured as it is (looked up by its natal row)
        return out
    rahu = {(h['pair'], h['sig']) for h in out if 'Rahu' in h['pair']}            # any plane, as T17 (X = Ketu in Dec = X = Rahu in Equator)
    out = [h for h in out if not ('Ketu' in h['pair'] and (h['pair'].replace('Ketu', 'Rahu'), h['sig']) in rahu)]
    return out


def sky_pair_blocks(ctx):
    """SKY PAIRS: S–S body pairs (Moon included, not Jupiter) and 'body – royal' (Eddie, 15 Oct 2026): each sky body with each royal star"""
    bod = [f'S {z}' for z in SKY_BODIES if z != 'Jupiter' and z in ctx.S0]
    roy = [f'S {x}' for x in ROYAL if x in ctx.S0]
    return [('S–S', list(itertools.combinations(bod, 2))), ('body – royal', [(b, x) for b in bod for x in roy])]


def t19_filter(rows):
    """T19: ratio on an interval, or a midpoint hit, or all three distances with a family hit (Eddie 15 Oct); 'X, Y together' left out;
    best first by the higher of the ratio score and the midpoint total"""
    keep = [h for h in rows if not h['together'] and (h['ev'] or h['mid'] is not None or h['allfam'])]
    return sorted(keep, key=lambda h: -max(h['ev']['score'] if h['ev'] else -1, -1 if h['mid'] is None else h['mid']))


SKY_AREA = {'A': 'A', 'P': 'φ and √2', 'B': 'B', None: 'no hit'}


def write_pairs_rows(ws, row, rows, skyside=False, notog=False):
    for h in rows:
        n = h['near']
        m = h['m']
        miss = '' if h['ev'] else f" — outside {tol_text(n)}"
        rv = [h['tid'], h['block'], h['pair'], h['plane'], *h['fx'][:2], *h['fy'][:2], *h['fxy'][:2], round(h['r0'], 6),
              f"{n['target']} · {n['name']} · {n['group']}" + miss, fmt_off(n),
              round(h['ev']['score'], 2) if h['ev'] else None, h['timing'], h['pos'], h['note'] or None] + ([mid_tcells(m)[0], round(m['close'], 4), *mid_tcells(m)[1:], round(m['score'], 2) if m['hit'] else None] if m else [])
        for k, v in enumerate(rv):
            ws.cell(row=row, column=1 + k, value=v)
        if notog and h['together']:                        # SKY ROYAL: a together row plain, no score, in NO HIT (Eddie 16 Oct)
            for k in (14, 20, 21, 22):                     # ratio score, ratio half, distance half, midpoint total
                ws.cell(row=row, column=k).value = None      # (cell(value=None) would not clear it)
            row += 1
            continue
        for k, f in enumerate((h['fx'], h['fy'], h['fxy'])):
            if f[2]:
                ws.cell(row=row, column=6 + 2 * k).fill = FILL[f[2]]
        if h['ev']:
            ws.cell(row=row, column=11).fill = FILL[h['ev']['colour']]
            ws.cell(row=row, column=14).fill = FILL[h['ev']['colour']]
            ws.cell(row=row, column=14).number_format = '0.00'
        if h['mid'] is not None:
            ws.cell(row=row, column=22).fill = FILL[h['m']['colour']]
            ws.cell(row=row, column=22).number_format = '0.00'
        if skyside:                                        # T19 sky side (Eddie 15 Oct): S Jupiter: S X – S Y, '—' where there is none
            s, c0 = h.get('S'), 1 + len(PAIR_HEAD)
            if s is None:
                ws.cell(row=row, column=c0, value='—')
            else:
                vals, fill = side_cells(s)
                for k, x in enumerate(vals):
                    ws.cell(row=row, column=c0 + k, value=x)
                if not s['together']:                      # Eddie 15 Oct: a together sky side plain, no colour, no area, no tag
                    for k, col in fill.items():
                        ws.cell(row=row, column=c0 + k).fill = FILL[col]
                    ws.cell(row=row, column=c0 + len(SIDE_HEAD), value=SKY_AREA[pair_area(s)])
                for k in (9, 17):
                    ws.cell(row=row, column=c0 + k).number_format = '0.00'
            if h.get('same'):
                ws.cell(row=row, column=c0 + len(SIDE_HEAD) + 1, value='same as sky — ' + '; '.join(h['same']))
        row += 1
    return row


def pair_areas(h):
    return [hit_area(h['ev']), hit_area(None, h['mid'] is not None)]


def pair_area(h):
    return row_area(pair_areas(h))


def write_pair_blocks(ws, row, title, rows, tid, every=False, skyside=False, notog=False):
    """T19, SKY PAIRS, SKY STARS, P## PAIRS in area blocks (Eddie, 15 Oct 2026): A (an A interval or a midpoint hit), φ and √2, B (a B interval),
    then the rest - P## PAIRS (every row): "no hit"; filtered tables: rows listed only for all three distances with a family hit.
    Order inside each block as before."""
    ws.cell(row=row, column=1, value=title).font = BOLD
    row += 1
    rest = 'NO HIT' if every else 'NO RATIO OR MIDPOINT HIT (listed for all three distances with a family hit)'
    for a in families.AREAS + (None,):
        blk = [h for h in rows if (None if notog and h['together'] else pair_area(h)) == a]
        if a is None and not blk and not every:
            continue
        row = pairs_header(ws, row, f'{tid} {AREA_NAME[a] if a else rest}: {len(blk)} rows'
                           + multi_text(sum(multi(pair_areas(h)) for h in blk if not (notog and h['together']))),
                           skyside)
        row = write_pairs_rows(ws, row, blk, skyside, notog) + 1
    return row


# ---------------- TIMELINE (Eddie, 16 Oct 2026): sky Jupiter events from the off - 30 min to the off + 60 min, SKY JUPITER sheet
TL_HEAD = ('table', 'exact (race-local)', 'min from the off', 'source', 'relationship', 'plane', 'kind', 'target', 'target value',
           'value at the off', 'score at the off', 'applying / separating', 'note')
TL_WIN = (-30.0, 60.0)


TL_FAR = 50 * 525960                                       # beyond 50 years: 'more than 50 years away / ago' (as exact_time)
LONG_MIN = 80.0                                            # LONG TIMELINE (Eddie, 16 Oct 2026): score at the off >= 80, any exact time
in_window = lambda t, score: TL_WIN[0] <= t <= TL_WIN[1]
long_keep = lambda t, score: score is not None and score >= LONG_MIN


def tl_clock(ctx, t):
    """race-local clock time of an event t minutes from the off (as exact_time; date and time when not on race day)"""
    if abs(t) > TL_FAR:
        return f"more than 50 years {'away' if t >= 0 else 'ago'}"
    when = ctx.off + datetime.timedelta(minutes=t)
    return when.strftime('%H:%M') if when.date() == ctx.off.date() else when.strftime('%d %b %Y %H:%M')


def tl_key(d):
    """a distance target folded over x10 / /10 (as NUMBERS); conjunction has no digits"""
    return ('conj', 0) if d['family'] == 'conj' or not d.get('tv') else num_key(d['family'], d['tv'])


class Ephem:
    """sky positions from the race engine (rebuild_kit/celestial_bodies_swisseph.py, the race's site, apparent, topocentric) at any minute
    from the off: workbook value at the off + engine(t) - engine(off), as the rates; cached per minute"""
    def __init__(self, ctx):
        sys.path.insert(0, motion.ENGINE_DIR)
        import swisseph as swe
        import celestial_bodies_swisseph as E
        swe.set_ephe_path(motion.EPHE)
        self.E, self.ctx, self.cache = E, ctx, {}
        t0 = E._parse_time(ctx.off_str, 'Europe/London')
        self.jd0 = E._to_jd_ut(t0)
        self.b0 = self.raw(0)

    def raw(self, m):
        return self.E.bodies_at(self.jd0 + m / 1440.0, *self.ctx.site, False)

    def at(self, m):
        m = round(m, 3)
        if m not in self.cache:
            b = self.raw(m)
            out = {}
            for x, p in self.ctx.S0.items():
                eb = x + '_B' if p[2] == 'star' else x
                if x == 'equator' or eb not in b or b[eb]['ra'] is None:
                    out[x] = (p[0], p[1])
                    continue
                out[x] = ((p[0] + (b[eb]['ra'] - self.b0[eb]['ra'] + 180.0) % 360.0 - 180.0) % 360.0, p[1] + b[eb]['dec'] - self.b0[eb]['dec'])
            self.cache[m] = out
        return self.cache[m]


EPH_DAY = [m * s for s in (1, -1) for m in range(10, 1441, 10)]          # search grid: 10 min for a day, then 1 h to 1 year, each way
EPH_YEAR = 525600


def geo_value(R, g, pl, pos):
    """the event's value from positions pos(point) (natal fixed, sky from the engine); ratios larger / smaller with the orientation of the
    off kept by the caller (returns the raw pair)"""
    def d(a, b, p):
        if b.endswith(' equator'):
            return abs(pos(a)[1])
        pa, pb = pos(a), pos(b)
        if p == 'RA':
            x = abs(pa[0] - pb[0]) % 360.0
            return min(x, 360.0 - x)
        return abs(pa[1] - pb[1]) if p == 'Dec' else abs(abs(pa[1]) - abs(pb[1]))
    if g[0] == 'd':
        return d(g[1], g[2], pl)
    if g[0] == 'r':
        return d(g[1], g[2], pl), d(g[1], g[3], pl)
    if g[0] == 'q':
        return d(*g[1], g[3]), d(*g[2], g[3])
    x, a, b = g[1:]
    return d(f'{a} Jupiter', f'{a} {x}', 'RA') - d(f'{b} Jupiter', f'{b} {x}', 'Dec')


def real_time(ctx, R, e):
    """the real exact time (Eddie, 16 Oct 2026): the event's value from the Swiss Ephemeris, stepping outward from the off (10 min for a
    day, then 1 h, up to 1 year each way) to the first crossing of the target, refined to the minute -> minutes from the off, or None
    when not within 1 year"""
    eph = ctx.eph

    def pos_at(m):
        sk = eph.at(m)
        return lambda p: sk[p.split(' ', 1)[1]] if p.startswith('S ') else ctx.pos(R, p, 0)

    g, pl, tv = e['geo'], e['plane'], e['tv']
    raw0 = geo_value(R, g, pl, pos_at(0))
    flip = isinstance(raw0, tuple) and raw0[0] < raw0[1]

    def f(m):
        v = geo_value(R, g, pl, pos_at(m))
        if isinstance(v, tuple):
            if not v[0] or not v[1]:
                return None
            v = v[1] / v[0] if flip else v[0] / v[1]
        return v - tv
    f0 = f(0)
    if f0 is None:
        return None
    grid = sorted(EPH_DAY + [h * 60 * s for s in (1, -1) for h in range(25, EPH_YEAR // 60 + 1)], key=abs)
    last = {1: (0.0, f0), -1: (0.0, f0)}
    for m in grid:
        side = 1 if m > 0 else -1
        v = f(m)
        if v is None:
            continue
        pm, pv = last[side]
        if (pv <= 0) != (v <= 0):
            lo, hi, flo = pm, m, pv
            while abs(hi - lo) > 1.0:
                mid = (lo + hi) / 2
                vm = f(mid)
                if (flo <= 0) == (vm <= 0):
                    lo, flo = mid, vm
                else:
                    hi = mid
            return (lo + hi) / 2
        last[side] = (m, v)
    return None


def realise(ctx, R, evs):
    """LONG TIMELINE (Eddie, 16 Oct 2026): every event whose linear exact time is more than 60 min from the off gets its real exact time
    from the ephemeris ('t'; the linear one kept as 't_lin'); not reached within 1 year -> 'nf' (its section from the motion at the off)"""
    for e in evs:
        if 't_lin' in e:                                   # an H + J event already done in the other block
            continue
        e['t_lin'] = e['t']
        if abs(e['t']) > TL_WIN[1] and getattr(ctx, 'eph', None) is not None:
            tr = real_time(ctx, R, e)
            e['nf'] = tr is None
            e['t'] = e['t'] if tr is None else tr
    return evs


def tl_from(t):
    """minutes or days from the off, as text"""
    if abs(t) > TL_FAR:
        return f"more than 50 years {'away' if t >= 0 else 'ago'}"
    return f'{t:+.1f} min' if abs(t) < 1440 else f'{t / 1440:+.2f} days'


def timeline(ctx, R0, eq, sources, keep=in_window):
    """events = every sky Jupiter relationship on the sheet whose exact time (linear, off -> +5 min, as everywhere) falls within
    TL_WIN: SKY (S Jupiter -> sky point; best hit, or the nearest target outside at the off), SKY EQ
    (unison), the pair blocks (ratio on its interval or nearest interval, midpoint = unison, each distance leg with a family hit).
    Together rows / lines left out; one event once (distances by number, target forms folded x10 / /10; ratio by pair, plane and interval); the first source
    is named, later ones in the note. -> [event dict] sorted by time"""
    ev_by = {}

    def add(key, t, **e):
        if t is None or not keep(t, e['score']):
            return
        if key in ev_by:
            o = ev_by[key]
            if e['src'] != o['src'] and e['src'] not in o['also']:
                o['also'].append(e['src'])
            return
        ev_by[key] = dict(e, t=t, also=[])

    def dist(src, a, b, pl, v0, v5, d, hit):
        if v5 in (None, 'n/a'):
            return
        rel = f'{a} → {b}' if a == 'S Jupiter' else f'{a} – {b}'
        kp = pl
        if pl == 'Equator' and (ctx.pos(R0, a, 0)[1] >= 0) == (ctx.pos(R0, b, 0)[1] >= 0):
            kp = 'Dec'                                     # both on one side: the Equator distance is the Dec distance, one event
        add(('d', frozenset((a, b)), kp, tl_key(d)), exact_t(v0, v5, d['tv']), src=src, rel=rel, plane=pl, geo=('d', a, b),
            kind='distance', target=tlabel(d), tv=d['tv'], v0=v0,
            score=d['score'] if hit else None, colour=d['colour'] if hit else '', out=not hit)

    for x in ctx.S0:                                       # SKY block
        if x == 'Jupiter':
            continue
        b = f'S {x}'
        for pl in PLANES:
            v0, v5 = ctx.pair(R0, 'S Jupiter', b, pl)
            if v0 is None:
                continue
            fp = 'Dec' if x == 'equator' else pl
            ev, also = nearest(v0, 'dist', fp)
            if ev:
                dist('SKY', 'S Jupiter', b, pl, v0, v5, ev, True)
            else:
                near = families.outside(v0, fp, 'deg')
                if near:
                    dist('SKY', 'S Jupiter', b, pl, v0, v5, near, False)
    for h in eq:                                           # SKY EQ: unison (Jupiter at the midpoint)
        if h['together'] or not h.get('q') or h['q'][0] is None:
            continue
        x, y = h['pts']
        add(('r', 'S Jupiter', frozenset((x, y)), h['plane'], '1'), exact_t(h['q'][0], h['q'][1], 1.0), src='SKY EQ', geo=('r', 'S Jupiter', x, y),
            rel=f'S Jupiter: {x} = {y}', plane=h['plane'], kind='midpoint (equidistance)', target='1 · unison · midpoint (area A)', tv=1.0,
            v0=h['q'][0], score=h['score'], colour=h['colour'], out=False)
    for src, rows in sources:                              # pair blocks: ratio, midpoint, legs
        for h in rows:
            if h['together']:
                continue
            (r0, r5), n = h['rq'], h['near']
            rel = f"{h['jup']}: {h['x']} – {h['y']}"
            key = lambda tg: ('r', h['jup'], frozenset((h['x'], h['y'])), h['plane'], tg)
            if r5 is not None:
                add(key(n['target']), exact_t(r0, r5, n['tv']), src=src, rel=rel, plane=h['plane'], kind='ratio', geo=('r', h['jup'], h['x'], h['y']),
                    target=f"{n['target']} · {n['name']} · {n['group']} (area {SKY_AREA[families.area(n['target'])]})", tv=n['tv'], v0=r0,
                    score=h['ev']['score'] if h['ev'] else None, colour=h['ev']['colour'] if h['ev'] else '', out=not h['ev'])
                if h['mid'] is not None:
                    add(key('1'), exact_t(r0, r5, 1.0), src=src, rel=rel, plane=h['plane'], kind='midpoint', geo=('r', h['jup'], h['x'], h['y']),
                        target='1 · unison · midpoint (area A)',
                        tv=1.0, v0=r0, score=h['mid'], colour=h['m']['colour'], out=False)
            for (a, b), d0, d5, bf in h['legs']:
                if bf and d0:
                    dist(src, a, b, h['plane'], d0, d5, bf, True)
    return sorted(ev_by.values(), key=lambda e: e['t'])


def runner_timeline(ctx, R, field, keep=in_window):
    """TIMELINE H / J (Eddie, 16 Oct 2026): every timed relationship of a runner sheet that involves the horse's (H) or the jockey's (J)
    chart, exact from the off - 30 to + 60 min, built as the sky TIMELINE: T5-T8 distances (best hit, or the
    nearest target outside at the off), T10 / T11 midpoint hits, T12-T14 ratios (interval or nearest interval;
    automatic unisons left out), T16 crossings (RA - Dec -> 0), T17 / T18 S Jupiter equidistance hits, T19 rows (ratio, midpoint, each leg
    with a sky leg and a family hit), T20 midpoint hits, T22 ratio, midpoint and the d(star, natal Jupiter) leg. Sky-only and natal-only
    (fixed) relationships, together rows and repeats left out; each event once (the first table named, later ones in the note); an event
    using both charts goes to both, marked 'H + J'. -> {'H': [events], 'J': [events]}"""
    ev_by = {}

    def add(key, t, pts, **e):
        ch = {p[0] for p in pts} - {'S'}
        if not ch or t is None or not keep(t, e['score']):
            return
        if key in ev_by:
            o = ev_by[key]
            if e['src'] != o['src'] and e['src'] not in o['also']:
                o['also'].append(e['src'])
            return
        ev_by[key] = dict(e, t=t, also=[], charts=ch, both=len(ch) == 2)

    def dist(src, a, b, pl, v0, v5, d, hit):
        if v5 in (None, 'n/a') or not d:
            return
        kp = pl
        if pl == 'Equator' and (ctx.pos(R, a, 0)[1] >= 0) == (ctx.pos(R, b, 0)[1] >= 0):
            kp = 'Dec'                                     # both on one side: the Equator distance is the Dec distance
        add(('d', frozenset((a, b)), kp, tl_key(d)), exact_t(v0, v5, d['tv']), (a, b), src=src, rel=f'{a} → {b}', plane=pl, geo=('d', a, b), dk=tl_key(d),
            kind='distance', target=tlabel(d), tv=d['tv'], v0=v0,
            score=d['score'] if hit else None, colour=d['colour'] if hit else '', out=not hit)

    def cell(src, a, b, pl, kind):                         # a T5-T8 cell: best, or the nearest target outside
        v0, v5 = ctx.pair(R, a, b, pl)
        if v0 is None:
            return
        ev, also = nearest(v0, kind, pl)
        if ev:
            dist(src, a, b, pl, v0, v5, ev, True)
        else:
            dist(src, a, b, pl, v0, v5, families.outside(v0, pl, 'deg'), False)

    def iv_text(d):
        return f"{tlabel(d)} (area {SKY_AREA[families.area(d['target'])]})" if d['family'] == 'interval' else tlabel(d)

    def rat(src, lab, pts, pl, v0, v5, ev, kind, geo):
        if v5 in (None, 'n/a') or v0 is None or (ev and ev.get('auto')):   # automatic (Jupiter return) unison: left out
            return
        d = ev or families.outside(v0, None, kind)
        if d:
            add(('q', src, lab, pl, d['target']), exact_t(v0, v5, d['tv']), pts, src=src, rel=lab, plane=pl, geo=geo, dk=d['target'], kind='ratio', target=iv_text(d),
                tv=d['tv'], v0=v0, score=d['score'] if ev else None, colour=d['colour'] if ev else '', out=not ev)

    def uni(src, mid, ends, pl, q0, q5, score, colour, rel):    # a midpoint: the larger / smaller ratio toward unison
        if q0 is None or q5 in (None, 'n/a'):
            return
        add(('r', mid, frozenset(ends), pl, '1'), exact_t(q0, q5, 1.0), (mid,) + tuple(ends), src=src, rel=rel, plane=pl, geo=('r', mid) + tuple(ends), dk='1',
            kind='midpoint', target='1 · unison · midpoint (area A)', tv=1.0, v0=q0, score=score, colour=colour, out=False)

    def pratio(src, mid, ends, pl, r0, r5, near, ev, rel):     # a pair ratio toward its interval (hit) or its nearest interval
        if r5 in (None, 'n/a'):
            return
        add(('r', mid, frozenset(ends), pl, near['target']), exact_t(r0, r5, near['tv']), (mid,) + tuple(ends), src=src, rel=rel, geo=('r', mid) + tuple(ends), dk=near['target'],
            plane=pl, kind='ratio', target=iv_text(near), tv=near['tv'], v0=r0, score=ev['score'] if ev else None,
            colour=ev['colour'] if ev else '', out=not ev)

    for tid, C in (('T5', 'H'), ('T6', 'J')):              # T5-T8 distances
        for x in NATAL_BODIES:
            if x in R[C] and x != 'Jupiter':
                for pl in PLANES:
                    cell(tid, 'S Jupiter', f'{C} {x}', pl, 'dist')
    for tid, C in (('T7', 'H'), ('T8', 'J')):
        for z in SKY_BODIES:
            if z in ctx.S0 and z != 'Jupiter':
                for pl in PLANES:
                    cell(tid, f'S {z}', f'{C} Jupiter', pl, 'dist')
    for tid in ('T10', 'T11'):                             # midpoint hits
        for pl, lines in field[tid].items():
            for lab, h in lines.items():
                if h['hit']:
                    e1, e2, m = h['pts']
                    q0 = h['d1'] / h['d2'] if h['d1'] >= h['d2'] else h['d2'] / h['d1']
                    uni(tid, m, (e1, e2), pl, q0, h['q5'], h['score'], h['colour'], lab)
    for tid, num in (('T12', lambda C, x: ('S Jupiter', f'S {x}')), ('T13', lambda C, x: ('S Jupiter', f'{C} {x}'))):
        for C in 'HJ':
            for x in NATAL_BODIES:
                if x == 'Jupiter' or x not in R[C]:
                    continue
                n, d = num(C, x), (f'{C} Jupiter', f'{C} {x}')
                lab = f'{n[0]}–{n[1]} / {d[0]}–{d[1]}'
                for pl in PLANES:
                    n0, n5 = ctx.pair(R, *n, pl); d0, d5 = ctx.pair(R, *d, pl)
                    if n0 is None or d0 is None:
                        continue
                    v0, v5, _ = ratio(n0, n5, d0, d5)
                    if not v0:
                        continue
                    ev, also = nearest(v0, 'ratio')
                    rat(tid, lab, n + d, pl, v0, v5, unison_kind(ctx, R, C, f'{C} {x}', pl, ev), 'ratio', ('q', n, d, pl))
    for C in 'HJ':                                         # T14 S / H, S / J
        n0, n5 = ctx.pair(R, 'S Jupiter', 'S equator', 'Dec'); d0, d5 = ctx.pair(R, f'{C} Jupiter', f'{C} equator', 'Dec')
        v0, v5, _ = ratio(n0, n5, d0, d5)
        if v0:
            ev, also = nearest(v0, 'eqratio')
            rat('T14', f'|Dec| S Jupiter / |Dec| {C} Jupiter', ('S Jupiter', f'{C} Jupiter'), 'Equator', v0, v5,
                unison_kind(ctx, R, C, f'{C} equator', 'Dec', ev), 'eqratio', ('q', ('S Jupiter', 'S equator'), (f'{C} Jupiter', f'{C} equator'), 'Dec'))
    for x in NATAL_BODIES:                                 # T16 crossings with a sky leg: RA - Dec -> 0
        if x == 'Jupiter' or x not in R['H'] or x not in R['J'] or x not in ctx.S0:
            continue
        for a, b in CROSS:
            if 'S' not in (a, b):
                continue
            ra0, ra5 = ctx.pair(R, f'{a} Jupiter', f'{a} {x}', 'RA'); de0, de5 = ctx.pair(R, f'{b} Jupiter', f'{b} {x}', 'Dec')
            if ra0 is None or de0 is None or 'n/a' in (ra5, de5):
                continue
            v0, v5 = ra0 - de0, (ra0 if ra5 is None else ra5) - (de0 if de5 is None else de5)
            ev = cross_eval(ra0, de0)
            add(('x', x, a, b), exact_t(v0, v5, 0.0), (f'{a} {x}', f'{b} {x}'), src='T16', rel=f'Jupiter–{x} {cross_name(a, b)}', geo=('x', x, a, b), dk='crossing',
                plane='RA = Dec', kind='crossing', target='crossing (RA − Dec = 0)', tv=0.0, v0=v0, score=ev['score'] if ev else None,
                colour=ev['colour'] if ev else '', out=not ev)
    for h in field['T17']:                                 # T17 / T18: S Jupiter equidistance hits
        if h['label'].startswith('S Jupiter') and h['inside'] and not h['together'] and h.get('q') and h['q'][0] is not None:
            uni('T17', 'S Jupiter', h['pts'], h['plane'], h['q'][0], h['q'][1], h['score'], h['colour'], h['label'])
    for r in field['T18'].get(1, []):
        for C in 'HJ':
            h = r[C]
            if h and h['inside'] and not h['together'] and h.get('q') and h['q'][0] is not None:
                uni('T18', 'S Jupiter', h['pts'], h['plane'], h['q'][0], h['q'][1], h['score'], h['colour'], h['label'])
    for h in field['T19']:                                 # T19: ratio, midpoint, legs with a sky leg
        if h['together']:
            continue
        (r0, r5), rel = h['rq'], f"S Jupiter: {h['x']} – {h['y']}"
        pratio('T19', 'S Jupiter', (h['x'], h['y']), h['plane'], r0, r5, h['near'], h['ev'], rel)
        if h['mid'] is not None:
            uni('T19', 'S Jupiter', (h['x'], h['y']), h['plane'], r0, r5, h['mid'], h['m']['colour'], rel)
        for (a, b), d0, d5, bf in h['legs']:
            if bf and d0:
                dist('T19', a, b, h['plane'], d0, d5, bf, True)
    for x, sides in field['T20'].items():                  # T20 midpoint hits
        for C in 'HJ':
            for pl, h in sides[C].items():
                if h['hit']:
                    q0 = h['d1'] / h['d2'] if h['d1'] >= h['d2'] else h['d2'] / h['d1']
                    uni('T20', f'{C} Jupiter', (f'S {x}', f'{C} {x}'), pl, q0, h['q5'], h['score'], h['colour'], f'S {x} / {C} {x} | {C} Jupiter')
    for line in field['T22']:                              # T22: ratio, midpoint, d(star, natal Jupiter)
        st = f"S {line['pair']}"
        for C in 'HJ':
            h = line[C]
            if h is None:
                continue
            rel = f"{line['pair']}: d(star, S Jupiter) / d(star, {C} Jupiter)"
            pratio('T22', st, ('S Jupiter', f'{C} Jupiter'), line['plane'], h['r0'], h['r5'], h['near'], h['ev'], rel)
            if h['mid'] is not None:
                uni('T22', st, ('S Jupiter', f'{C} Jupiter'), line['plane'], h['r0'], h['r5'], h['mid'], h['m']['colour'], rel)
            if h['f2'][1]:
                dist('T22', st, f'{C} Jupiter', line['plane'], h['d2'], h['d25'], h['f2'][1], True)
    evs = sorted(ev_by.values(), key=lambda e: e['t'])
    return {C: [e for e in evs if C in e['charts']] for C in 'HJ'}


def iv_label(d):
    """target text: 'interval · name · group (area ..)' for intervals, 'target (family)' otherwise"""
    return f"{tlabel(d)} (area {SKY_AREA[families.area(d['target'])]})" if d['family'] == 'interval' else tlabel(d)


SKY_TL_HEAD = ('sky equivalent', 'sky value at the off', 'sky target', 'sky score', 'sky timing', 'same as sky')


def sky_equiv(ctx, R, e):
    """the event's relationship in the sky at the off (Eddie, 16 Oct 2026): every natal point replaced by the same body in the sky, same
    plane -> dict (rel, v0, target, score, colour, timing, same) or {'rel': .., 'dash': True} where two points become one (T10, T11, T12-T14,
    T19 H X - J X, T20, T22 ratio / midpoint) or the sky point / plane does not exist. A together sky side shows its values only."""
    g, pl = e['geo'], e['plane']
    sp = lambda p: 'S ' + p.split(' ', 1)[1]
    have = lambda *ps: all(p.split(' ', 1)[1] in ctx.S0 for p in ps)
    if g[0] == 'q':
        return {'rel': None, 'dash': True}
    if g[0] == 'x':
        x = g[1]
        rel = f'Jupiter–{x} S RA = S Dec'
        ra0, ra5 = ctx.pair(R, 'S Jupiter', f'S {x}', 'RA'); de0, de5 = ctx.pair(R, 'S Jupiter', f'S {x}', 'Dec')
        if not have(f'S {x}') or ra0 is None or de0 is None or 'n/a' in (ra5, de5):
            return {'rel': rel, 'dash': True}
        v0, v5 = ra0 - de0, ra5 - de5
        ev = cross_eval(ra0, de0)
        return {'rel': rel, 'v0': v0, 'target': 'crossing (RA − Dec = 0)' + ('' if ev else ' — outside'), 'score': ev['score'] if ev else None,
                'colour': ev['colour'] if ev else '', 'timing': exact_time(ctx, v0, v5, 0.0), 'same': bool(ev and e['score'] is not None)}
    if g[0] == 'd':
        a, b = sp(g[1]), sp(g[2])
        rel = f'{a} → {b}'
        if a == b or not have(a, b):
            return {'rel': rel, 'dash': True}
        v0, v5 = eq_dist2(ctx, R, a, b, pl)
        if not v0:
            return {'rel': rel, 'dash': True}
        fp = pl if pl in ('RA', 'Dec') else None
        ev = families.best(v0, fp, 'deg')
        d = ev or families.outside(v0, fp, 'deg')
        return {'rel': rel, 'v0': v0, 'target': (tlabel(d) + ('' if ev else ' — outside')) if d else 'no family',
                'score': ev['score'] if ev else None, 'colour': ev['colour'] if ev else '',
                'timing': exact_time(ctx, v0, v5, d['tv']) if d else None,
                'same': bool(ev and e['score'] is not None and tl_key(ev) == e['dk'])}
    m, x, y = (sp(p) for p in g[1:])
    rel = f"{m}: {x} {'=' if e['kind'] == 'midpoint' else '–'} {y}"
    if len({m, x, y}) < 3 or not have(m, x, y):
        return {'rel': rel, 'dash': True}
    if pl == 'Equator':
        ps = [ctx.pos(R, q, 0) for q in (m, x, y)]
        if (ps[0][1] >= 0) == (ps[1][1] >= 0) == (ps[2][1] >= 0):
            return {'rel': rel, 'dash': True}
    (dx, dx5), (dy, dy5) = eq_dist2(ctx, R, m, x, pl), eq_dist2(ctx, R, m, y, pl)
    if not dx or not dy or 'n/a' in (dx5, dy5):
        return {'rel': rel, 'dash': True}
    flip = dx < dy
    q0, q5 = (dy / dx, dy5 / dx5) if flip else (dx / dy, dx5 / dy5)
    ev = families.best(q0, None, 'ratio')
    near = ev or families.outside(q0, None, 'ratio')
    mid = jup_mid(ctx, R, m, x, y, pl, dx, dy) if 100.0 / q0 >= 100.0 - MID_RTOL else None
    dxy = eq_dist(ctx, R, x, y, pl)
    together = dxy is not None and dxy < (families.CONJ['RA'] if pl == 'RA' else families.CONJ['Dec'])
    if e['kind'] == 'midpoint' and mid and mid['hit']:
        out = {'target': '1 · unison · midpoint (area A)', 'score': mid['score'], 'colour': mid['colour'], 'timing': exact_time(ctx, q0, q5, 1.0),
               'same': e['score'] is not None}
    else:
        out = {'target': iv_label(near) + ('' if ev else ' — outside'), 'score': ev['score'] if ev else None, 'colour': ev['colour'] if ev else '',
               'timing': exact_time(ctx, q0, q5, near['tv']), 'same': bool(ev and e['score'] is not None and ev['target'] == e['dk'])}
    if together:                                           # a together side: values only (no score, no colour, no tag)
        out.update(score=None, colour='', same=False, target=out['target'] + ' (X, Y together)')
    return dict(out, rel=rel, v0=q0)


def write_sky_cells(ws, row, c0, se):
    """the sky equivalent cells of one event row from column c0"""
    if se is None:
        return
    if se.get('dash'):
        ws.cell(row=row, column=c0, value=se['rel'] or '—')
        ws.cell(row=row, column=c0 + 1, value='—')
        return
    for k, v in enumerate((se['rel'], round(se['v0'], 6), se['target'], None if se['score'] is None else round(se['score'], 2), se['timing'],
                           'same as sky' if se['same'] else None)):
        ws.cell(row=row, column=c0 + k, value=v)
    if se['colour']:
        ws.cell(row=row, column=c0 + 1).fill = ws.cell(row=row, column=c0 + 3).fill = FILL[se['colour']]
    ws.cell(row=row, column=c0 + 3).number_format = '0.00'


def tl_vals(ctx, e, tid, long=False):
    note = '; '.join((['H + J'] if e.get('both') else []) + (['outside at the off'] if e['out'] else [])
                     + (['also ' + ', '.join(e['also'])] if e['also'] else []))
    if e.get('nf'):
        return (tid, 'not within 1 year', 'not within 1 year') + tl_vals(ctx, dict(e, nf=False), tid, long)[3:]
    return (tid, tl_clock(ctx, e['t']), tl_from(e['t']) if long else round(e['t'], 1), e['src'], e['rel'], e['plane'], e['kind'], e['target'],
            e['tv'], round(e['v0'], 6), None if e['score'] is None else round(e['score'], 2),
            'applying' if e['t'] >= 0 else 'separating', note or None)


def write_long(ws, row, ctx, evs, tid, title, skyf=None):
    """LONG TIMELINE (Eddie, 16 Oct 2026): every event scoring >= 80 at the off, any exact time; SEPARATING, then APPLYING, each by
    score at the off (highest first; ties: separating most recent first, applying soonest first); runner sheets add the sky equivalent cells"""
    # Eddie 16 Oct 2026: inside each section by score at the off, highest first; ties by exact time (separating most recent first)
    # 16 Oct 2026 (Eddie): by the real time (ephemeris) beyond 60 min; 'not within 1 year' last among equal scores
    sep = sorted([e for e in evs if e['t'] < 0], key=lambda e: (-e['score'], bool(e.get('nf')), -e['t']))
    app = sorted([e for e in evs if e['t'] >= 0], key=lambda e: (-e['score'], bool(e.get('nf')), e['t']))
    ws.cell(row=row, column=1, value=f'{title}: {len(evs)} events, {len(sep)} separating, {len(app)} applying').font = BOLD
    row += 1
    head = TL_HEAD[:2] + ('from the off',) + TL_HEAD[3:] + (SKY_TL_HEAD if skyf else ()) + ('minutes from the off', 'linear estimate')
    for k, h in enumerate(head):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    row += 1
    last = len(head) - 1
    for lab, part in (('SEPARATING', sep), ('APPLYING', app)):
        ws.cell(row=row, column=1, value=tid).font = BOLD
        ws.cell(row=row, column=4, value=f'——— {lab}: {len(part)} events ———').font = BOLD
        row += 1
        for e in part:
            for k, v in enumerate(tl_vals(ctx, e, tid, long=True)):
                ws.cell(row=row, column=1 + k, value=v)
            if e['colour']:
                ws.cell(row=row, column=10).fill = ws.cell(row=row, column=11).fill = FILL[e['colour']]
            ws.cell(row=row, column=11).number_format = '0.00'
            if skyf:
                write_sky_cells(ws, row, 1 + len(TL_HEAD), skyf(e))
            ws.cell(row=row, column=last, value=None if e.get('nf') else round(e['t'], 1))
            tl_ = e.get('t_lin', e['t'])
            ws.cell(row=row, column=last + 1, value=f'{tl_clock(ctx, tl_)} ({tl_from(tl_)})')
            row += 1
    return row + 1


def write_timeline(ws, row, ctx, evs, tid='TIMELINE', title=None, skyf=None):
    """TIMELINE rows in time order, with marker rows for the off and the off + 5 min"""
    nb = sum(1 for e in evs if e['t'] < 0); nd = sum(1 for e in evs if 0 <= e['t'] <= 5); na = len(evs) - nb - nd
    title = title or ('TIMELINE (Eddie, 16 Oct 2026): every sky Jupiter relationship on this sheet whose exact time falls from the '
                      'off − 30 min to the off + 60 min (SKY best hit or nearest target; SKY EQ; SKY PAIRS, SKY STARS, SKY ROYAL ratio, midpoint '
                      'and each distance leg with a family hit), linear from the off and the off + 5 min as everywhere; "outside at the off" = not a hit '
                      'at the off; together rows left out, each event once (other sources in the note); values are never scaled')
    ws.cell(row=row, column=1, value=f'{title}: {len(evs)} events, {nb} before the off, {nd} in the first 5 min, {na} after').font = BOLD
    row += 1
    for k, h in enumerate(TL_HEAD + (SKY_TL_HEAD if skyf else ())):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    row += 1
    marks = [(0.0, 'OFF'), (5.0, 'OFF + 5 MIN')]

    def mark(t, lab):
        for k, v in enumerate((tid, tl_clock(ctx, t), t, f'——— {lab} ———')):
            ws.cell(row=row, column=1 + k, value=v).font = BOLD

    for e in evs:
        while marks and e['t'] >= marks[0][0]:
            mark(*marks.pop(0)); row += 1
        for k, v in enumerate(tl_vals(ctx, e, tid)):
            ws.cell(row=row, column=1 + k, value=v)
        if e['colour']:
            ws.cell(row=row, column=10).fill = ws.cell(row=row, column=11).fill = FILL[e['colour']]
        ws.cell(row=row, column=11).number_format = '0.00'
        if skyf:
            write_sky_cells(ws, row, 1 + len(TL_HEAD), skyf(e))
        row += 1
    while marks:
        mark(*marks.pop(0)); row += 1
    return row + 1


def pairs_header(ws, row, title, skyside=False):
    ws.cell(row=row, column=1, value=title).font = BOLD
    row += 1
    head = PAIR_HEAD + (tuple(f'S {x}' for x in SIDE_HEAD) + ('S area', 'same as sky') if skyside else ())
    for k, h in enumerate(head):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    return row + 1


PAIR_NOTE = ('sky Jupiter on natal pairs: d(S Jup, X), d(S Jup, Y), d(X, Y) with their best family (score, timing; natal d(X, Y) fixed); '
             'ratio d(S Jup, X) / d(S Jup, Y) larger / smaller on the interval list only (area A 1, 3/2, 2 ... 9 on ±0.02 absolute, area B tapered %; timing); the midpoint in its own '
             'cells (Eddie, 15 Oct 2026): closeness >= 90 % and S Jupiter within RA ±0.5 / Dec, Equator ±0.15 of the midpoint of X and Y (RA: '
             'closer of near / far), midpoint total = ratio half + distance half (each squared x 0.5); a row is listed if the ratio or the midpoint is a hit; '
             'between / far side; '
             'blocks H–H, J–J, H–J; planes RA, Dec, Equator (Equator only when S Jupiter, X, Y straddle the equator); '
             'no star–star pairs; a Ketu row repeating the Rahu row dropped')


def pairs_sheet(wb, P, R, rows):
    """P## PAIRS: every pair, unfiltered (natal bodies + all 22 stars); in the separate _pairs.xlsx workbook (Eddie 14 Oct)"""
    ws = wb.create_sheet(f'{P} PAIRS')
    write_pair_blocks(ws, 1, f"{P} {R['name']} — PAIRS (unfiltered): " + PAIR_NOTE + '; "X, Y together" tagged', rows, 'PAIRS', every=True)
    ws.column_dimensions['C'].width = 34
    ws.freeze_panes = 'E3'


# ---------------- T18: equidistance, horse and jockey side by side (Eddie, 14 Oct 2026)
T18_SIDE = ('plane', 'd(Jup, X)', 'd(Jup, Y)', 'closeness %', 'midpoint offset', 'ratio half', 'distance half', 'total', 'Jupiter', 'timing')


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
    m = h['m']
    cl = round(m['close'], 4) if m['rin'] else f"{m['close']:.4f} (under 90 %)"
    if not h['inside']:
        return [h['plane'], round(h['d1'], 6), round(h['d2'], 6), cl, mid_tcells(m)[0], None, None, None, None, None]
    return [h['plane'], round(h['d1'], 6), round(h['d2'], 6), cl, *mid_tcells(m), round(h['score'], 2), h['pos'], h['timing']]


def write_t18(ws, row, ctx, R):
    """T18: the same equidistance pair side by side for horse and jockey. Block 1: S Jupiter: H X = H Y | S Jupiter: J X = J Y.
    Block 2: H Jupiter: H X = H Y | J Jupiter: J X = J Y. Each side its best plane (inside 1 %, highest score; 'together' planes left
    out); a side not inside shows its closest plane's ratio plain, uncoloured."""
    out = {}
    for blk, (jh, jj, title) in enumerate((('S Jupiter', 'S Jupiter', 'S Jupiter: H X = H Y  |  S Jupiter: J X = J Y'),
                                          ('H Jupiter', 'J Jupiter', 'H Jupiter: H X = H Y  |  J Jupiter: J X = J Y')), start=1):
        ws.cell(row=row, column=1, value='T18').font = BOLD
        ws.cell(row=row, column=2, value=f'T18 block {blk} — equidistance, horse and jockey side by side: {title}. Each side its best plane '
                '(a midpoint hit: closeness >= 90 % and Jupiter within RA ±0.5 / Dec, Equator ±0.15 of the midpoint; highest total; "X, Y together" planes '
                'left out); a side not a hit shows its closest plane (highest closeness) plain. '
                'Horse-inside rows first (closest to unison first), then jockey-only rows.').font = BOLD
        row += 1
        rows = t18_rows(ctx, R, jh, jj)
        both = lambda r: bool(r['H'] and r['H']['inside'] and r['J'] and r['J']['inside'])
        ws.cell(row=row - 1, column=2).value += f'  both (horse and jockey midpoint hits): {sum(both(r) for r in rows)}'
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
                    ws.cell(row=row, column=col + 7).fill = FILL[h['colour']]
                    for k in (5, 6, 7):
                        ws.cell(row=row, column=col + k).number_format = '0.00'
            row += 1
        if not rows:
            ws.cell(row=row, column=2, value='(no pair inside 1 % on either side)'); row += 1
        row += 1
    return row, out


def write_equi(ws, row, title, hits):
    ws.cell(row=row, column=1, value=hits[0]['tid'] if hits else 'T17').font = BOLD
    ws.cell(row=row, column=2, value=title + ' — midpoint scoring (Eddie, 14 Oct 2026): closeness of d(Jup, X), d(Jup, Y) at least 90 % and Jupiter\'s offset from the midpoint of X and Y within RA ±0.5 / Dec, Equator ±0.15 (RA: closer of near / far), each half squared x 0.5, total = the sum, a hit needs both; every plane (Equator = | |Dec| − |Dec| |, only when Jupiter, X and Y '
            'are not all on one side of the equator); '
            'Jupiter between X and Y when d(X, Y) is within 1 % of d(Jup, X) + d(Jup, Y), otherwise far side; stars left out; hits only, '
            'best first; "X, Y together" (d(X, Y) < 1.5 RA / 0.3 Dec, Equator) at the bottom; a Ketu line repeating a Rahu line dropped').font = BOLD
    row += 1
    for k, h in enumerate(EQ_HEAD):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    row += 1
    for h in hits:
        vals = (h['tid'], h['label'], h['plane'], round(h['d1'], 6), round(h['d2'], 6), round(h['m']['close'], 4),
                *mid_tcells(h['m']), round(h['score'], 2), h['pos'], None if h['dxy'] is None else round(h['dxy'], 6), round(h['sum'], 6),
                *[x for f in h['fams'] for x in f[:2]], h['r5'] if h['r5'] in (None, 'n/a') else round(h['r5'], 6), h['arrow'], h['timing'])
        for k, v in enumerate(vals):
            c = ws.cell(row=row, column=1 + k, value=v)
        for k in (8, 9, 10):
            ws.cell(row=row, column=k).number_format = '0.00'
        ws.cell(row=row, column=6).fill = FILL[h['colour']]
        ws.cell(row=row, column=10).fill = FILL[h['colour']]
        for k, f in enumerate(h['fams']):                  # family cell coloured by its score
            if f[2]:
                ws.cell(row=row, column=15 + 2 * k).fill = FILL[f[2]]
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
                c = ws.cell(row=r, column=3 + i, value=f"{h['m']['close']:.4f}% [{h['score']:.2f}] {h['pos']} · {h['timing']}"
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


def thread_add(thr, tid, lab, pts, pl, v, ev):
    """one THREADS entry per scored hit on a body X linked with Jupiter (the value as it is; never scaled x10 / /10, Eddie 16 Oct 2026).
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
    num = lambda v: f'{round(v, 6)}' if tid not in ('T10', 'T11', 'T16', 'T20') else f'{v:+.6f}'
    if tid not in ('T10', 'T11', 'T16', 'T20'):
        thread_all(thr, tid, lab, pl, v, X, xch, dirs)
        return
    if ev and ev.get('score') is not None or tid in ('T10', 'T11', 'T20') and ev:
        tgt = ev['target'] if tid in ('T10', 'T11', 'T20') else 'equal' if tid == 'T16' else ev['target']
        sct = f" ({ev['score']:.2f})" if ev.get('score') is not None else ''
        thr.append({'X': X, 'charts': xch, 'dirs': dirs, 'main': True, 'score': ev.get('score'), 'colour': ev['colour'],
                    'mid': tid in ('T10', 'T11', 'T20'), 'hidden': False,
                    'text': f"{lab} {pl + ' ' if pl else ''}{num(v)} → {tgt}{sct} [{tid}]"})


def thread_all(thr, tid, lab, pl, v, X, xch, dirs):
    """THREADS (Eddie 14 Oct): every family hit of the value, as NUMBERS does (never scaled, 16 Oct 2026)"""
    kind = 'ratio' if tid in ('T12', 'T13') else 'deg'
    plane = None if kind == 'ratio' else pl
    for d in families.evaluate(v, plane, kind):
        thr.append({'X': X, 'charts': xch, 'dirs': dirs, 'main': True, 'score': d['score'], 'colour': d['colour'], 'hidden': False,
                    'text': f"{lab} {pl + ' ' if pl else ''}{round(v, 6)} → {d['target']} ({d['score']:.2f}) [{tid}]"})


THREAD_MIN = 50.0                                          # Eddie, 13 Oct: tags, field counts and cell lines use hits scoring >= 50


def strong(h):
    """a hit scoring >= 50; midpoints (T10, T11, T20) too: total >= 50 (Eddie, 15 Oct 2026; was every midpoint hit)"""
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
    ws.cell(row=1, column=1, value='THREADS: hits inside tolerance linking body X with Jupiter, from T1-T8, T10-T13, T16, T20; a cell lists those '
            'scoring >= 50 (midpoints too: total >= 50; the value as it is, never scaled x10 / /10), best first, then "+ n weaker" (score-0 hits not counted); automatic unisons left out. '
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
    """every degree-distance family scoring >= 40 on the value as it is (never scaled x10 / /10, Eddie 16 Oct 2026); rows fold the target
    forms by family and digits (e.g. ninth 11.1111 / 111.111, real family targets); one hit per number and value (the higher score)"""
    if not v or v <= 0:
        return
    found = {}
    for d in families.evaluate(v, pl, 'deg'):
        if d['family'] not in NUM_FAMILIES or d['score'] < NUM_MIN or not d['tv']:
            continue
        k = num_key(d['family'], d['tv'])
        if k in found and d['score'] <= found[k]['score']:
            continue
        found[k] = {'key': k, 'col': col, 'form': d['target'], 'tv': d['tv'], 'score': d['score'], 'colour': num_colour(d['score']),
                    'text': f"{lab} {pl} {round(v, 6)} → {d['target']} {d['off']:+.5f} ({d['score']:.2f})"}
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
    HORSE (T1), JOCKEY (T2), SKY->NATAL (T5-T8); hits >= 40 on the value as it is, best first; tag from SKY / HORSE / JOCKEY"""
    ws = wb.create_sheet(f'{P} NUMBERS', wb.sheetnames.index(f'{P} RATIOS') + 1)
    ws.cell(row=1, column=1, value=f"{P} {R['name']} — NUMBERS: degree-distance hits scoring >= 40 per target number (x10 / /10 target forms folded "
            'by family and digits; hits on the value as it is, never scaled). SKY = S Jupiter -> sky bodies, '
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
    """RATIOS BY GROUP: every T12-T14 ratio on an interval, grouped (Eddie's group order), tightest (highest score) first;
    unison rows carry the field count (runners with unison on the same ratio)"""
    ws = wb.create_sheet(f'{P} RATIOS', wb.sheetnames.index(P) + 1)
    ws.cell(row=1, column=1, value=f"{P} {R['name']} — RATIOS BY GROUP (T12-T14 ratios on Eddie's interval list, each on its own tolerance; "
            "area A, then φ and √2, then area B (Eddie, 15 Oct 2026), groups in order inside each area; tightest first)").font = BOLD
    row = 3
    for ar, g in [(a, g) for a in families.AREAS for g in families.GROUPS]:
        if g == families.GROUPS[0]:
            n_ar = sum(1 for r in rats if families.area(r[5]['target']) == ar)
            ws.cell(row=row, column=1, value=f'{AREA_NAME[ar]}: {n_ar} ratios').font = BOLD
            row += 2
        sel = [r for r in rats if r[5]['group'] == g and families.area(r[5]['target']) == ar]
        if not sel:
            continue                                           # empty group: no header (Eddie, 13 Oct)
        ws.cell(row=row, column=1, value=g).font = BOLD
        row += 1
        for k, h in enumerate(('group', 'table', 'ratio', 'plane', 'value', '+5 min', 'interval', 'name', 'offset', 'score', 'off->+5',
                               'unison field')):
            c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
        row += 1
        for tid, lab, pl, v0, v5, ev, key in sorted(sel, key=lambda r: -r[5]['score']):
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


def field_ratio_sheet(wb, tid, title, runners, fields, planes, uni):
    """FIELD 12-14 in areas (Eddie, 15 Oct 2026): per plane, area A, φ and √2, area B and no hit; a runner's cell goes in the block of its own
    hit (each cell once); rows = labels with at least one cell in that block; last column = runners with a hit in that area (k/n;
    automatic unisons not counted)"""
    ws = wb.create_sheet(f'FIELD {tid[1:]}')
    ws.cell(row=1, column=1, value=f'{tid} field matrix — {title}; per runner: value (coloured), nearest target + offset; area A, φ and √2, area B, '
            'no hit (Eddie, 15 Oct 2026), each runner\'s cell in the block of its own hit; k/n = runners with a hit in that area').font = BOLD
    order = sorted(runners)
    last = 2 + 2 * len(order)
    row = 3
    for pl in planes:
        ws.cell(row=row, column=1, value=pl).font = BOLD
        for i, P in enumerate(order):
            c = ws.cell(row=row, column=2 + 2 * i, value=f"{P} {runners[P]['name']}"); c.fill = HEAD; c.font = BOLD
        row += 1
        labels = []
        for P in order:
            for k in [k[0] for k in fields[P][tid] if k[1] == pl]:
                if k not in labels:
                    labels.append(k)
        for a in families.AREAS + (None,):
            cell_of = lambda P, lab: fields[P][tid].get((lab, pl))
            rows = [lab for lab in labels if any(cell_of(P, lab) and hit_area(cell_of(P, lab)[1]) == a for P in order)]
            ws.cell(row=row, column=1, value=f'{pl} — {AREA_NAME[a]}: {len(rows)} rows').font = BOLD
            if a:
                c = ws.cell(row=row, column=last, value=f"runners with a hit in {AREA_NAME[a].split(' (')[0]}"); c.fill = HEAD; c.font = BOLD
            row += 1
            for lab in rows:
                ws.cell(row=row, column=1, value=lab)
                k = 0
                for i, P in enumerate(order):
                    x = cell_of(P, lab)
                    if not x or hit_area(x[1]) != a:
                        continue
                    v, ev = x
                    c = ws.cell(row=row, column=2 + 2 * i, value=round(v, 6))
                    if ev and ev['colour']:
                        c.fill = FILL[ev['colour']]
                    if not ev and v:                       # outside every tolerance: nearest target + offset, plain
                        near = families.outside(v, pl, 'ratio')
                        if near:
                            ws.cell(row=row, column=3 + 2 * i, value=f"{near['target']} {fmt_off(near)} (outside {tol_text(near)})")
                    if ev:
                        k += not ev.get('auto')
                        ws.cell(row=row, column=3 + 2 * i, value=f"{ev['target']} {fmt_off(ev)} [{ev['score']:.2f}] [{ev['group']}]"
                                + ((' automatic (Jupiter return), not counted' if ev.get('auto') else f" field {uni[(tid, lab, pl)]}/{len(runners)}"
                                    + (' ' + assist_text(ev['assisted']) if ev.get('assisted') else '')) if ev.get('target') == '1' else ''))
                if a:
                    ws.cell(row=row, column=last, value=f'{k}/{len(order)}')
                row += 1
            row += 1
        row += 1
    ws.column_dimensions['A'].width = 34
    ws.freeze_panes = 'B4'


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
                if mid:                                    # midpoints (Eddie 14 Oct): offset coloured by the combined score
                    h = src[pl].get(lab)
                    if not h:
                        continue
                    c = ws.cell(row=row, column=2 + 2 * i, value=round(h['o0'], 6))
                    side = f"{h['side']} · " if h['side'] else ''
                    if h['hit']:
                        c.fill = FILL[h['colour']]
                        ws.cell(row=row, column=3 + 2 * i, value=f"{side}closeness {h['close']:.4f}% [{h['score']:.2f}] · {h['timing']}")
                    else:
                        ws.cell(row=row, column=3 + 2 * i, value=side + mid_text(h))
                    continue
                else:
                    if (lab, pl) not in src:
                        continue
                    v, ev = src[(lab, pl)]
                c = ws.cell(row=row, column=2 + 2 * i, value=round(v, 6))
                if ev and ev['colour']:
                    c.fill = FILL[ev['colour']]
                if not ev and tid != 'T16' and v:                 # outside every tolerance: nearest target + offset, plain
                    near = families.outside(v, pl, 'ratio' if tid in ('T12', 'T13', 'T14') else 'deg')
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


def full_sheets(wb, runners, fields, uni, sky_nums):
    """--full (Eddie, 19 Oct 2026): every FIELD sheet, THREADS and FIELD NUMBERS, as before"""
    for tid, title in (('T5', 'S Jupiter → H bodies'), ('T6', 'S Jupiter → J bodies'), ('T7', 'sky bodies → H Jupiter'),
                       ('T8', 'sky bodies → J Jupiter')):
        field_sheet(wb, tid, title, runners, fields, PLANES)
    field_sheet(wb, 'T10', 'midpoints S Jupiter / H X, S Jupiter / J X, H X / J X (third point\'s offset)', runners, fields, MID_PLANES, mid=True)
    field_sheet(wb, 'T11', 'midpoints H Jupiter / J Jupiter | sky body; S Jupiter / natal Jupiter | natal body (third point\'s offset)', runners,
                fields, MID_PLANES, mid=True)
    for tid, title, pls in (('T12', '(S Jupiter–S X) / (natal Jupiter–natal X), intervals', PLANES),
                            ('T13', '(S Jupiter–natal X) / (natal Jupiter–natal X), intervals', PLANES),
                            ('T14', 'Equator ratios of the three Jupiters, intervals', ('Equator',)),
                            ('T23', 'H / J = d(H Jupiter, H X) / d(J Jupiter, J X), natal, fixed (Eddie, 16 Oct 2026); bodies, stars, equator (Dec); '
                             'a ratio with Jupiter and X together on a leg left out', PLANES)):
        field_ratio_sheet(wb, tid, title, runners, fields, pls, uni)
    field_sheet(wb, 'T16', 'RA–Dec crossing (value = RA − Dec, inside ±0.02)', runners, fields, [cross_name(a, b) for a, b in CROSS])
    field_equi_sheet(wb, runners, fields)
    field_t20_sheet(wb, runners, fields)
    field_star_sheet(wb, 'T21', 'natal Jupiter on natal star pairs (H Jupiter: H A – H B | J Jupiter: J A – J B)', runners, fields, T21_RMIN)
    field_star_sheet(wb, 'T22', 'fixed star as the apex, d(star, S Jupiter) / d(star, natal Jupiter)', runners, fields)
    field_star_sheet(wb, 'T21R', 'ROYAL STARS ONLY (Eddie, 16 Oct 2026): natal Jupiter on the six royal star pairs', runners, fields, T21_RMIN, every=True)
    field_star_sheet(wb, 'T22R', 'ROYAL STARS ONLY (Eddie, 16 Oct 2026): royal star as the apex, d(star, S Jupiter) / d(star, natal Jupiter)',
                     runners, fields, every=True)
    threads_sheet(wb, runners, fields)
    field_numbers_sheet(wb, runners, {P: sky_nums + fields[P]['_nums'] for P in runners})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('--out'); ap.add_argument('--off'); ap.add_argument('--site')
    ap.add_argument('--full', action='store_true', help='also write P## RATIOS, P## NUMBERS, THREADS, FIELD NUMBERS and every FIELD sheet '
                    '(default since 19 Oct 2026, Eddie: POSITIONS, SKY JUPITER and the runner sheets only)')
    a = ap.parse_args()
    race, batch, label, sky, skyx, runners = load_input(a.input, with_skyx=True)
    skipped = {P: R['name'] for P, R in runners.items() if 'Jupiter' not in R['H'] or 'Jupiter' not in R['J']}
    for P in skipped:                                          # e.g. a jockey tab with no chart (jockey None): no Jupiter to read
        del runners[P]
    course, hhmm, ymd = motion.race_parts(race)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(batch)), f'race_batch_{ymd}_{course}_{hhmm}_jupiter_tables.xlsx')
    off, site, src = motion.off_and_site(race, label, batch, a.off, a.site)
    rates, elines = motion.engine_rates(sky, off, site)
    ctx = Ctx(sky, rates)
    xtra = [b for b in skyx if b not in sky]               # the new stars (Eddie, 19 Oct 2026): T1, T2 and T24 only
    xrates = motion.engine_rates({b: skyx[b] for b in xtra}, off, site)[0] if xtra else {}
    ctx.x = Ctx(skyx, {**rates, **xrates})                 # the sky on T1_T2_T24_STARS, for the T1 / T2 SKY cells
    ctx.off = datetime.datetime.strptime(str(off)[:16], '%Y-%m-%d %H:%M')     # race-local off time (clock times of exact)
    ctx.off_str, ctx.site = str(off)[:16], site
    ctx.x.off, ctx.x.off_str, ctx.x.site = ctx.off, ctx.off_str, ctx.site
    try:
        ctx.eph = Ephem(ctx)                               # LONG TIMELINE real exact times (Eddie, 16 Oct 2026)
        ctx.x.eph = Ephem(ctx.x)                           # sky LONG TIMELINE on the 46 stars (Eddie, 20 Oct 2026)
    except Exception as ex:                                # engine cannot run: the linear estimate stays
        print(f'ephemeris not run ({type(ex).__name__}: {ex}): LONG TIMELINE keeps the linear times')
        ctx.eph = ctx.x.eph = None
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
    if xtra:                                               # positions of the new stars (Eddie, 19 Oct 2026), used in T1, T2 and T24 only
        ws.append([]); ws.append(['T1 / T2 / T24 only (Eddie, 19 Oct 2026): ' + ', '.join(xtra)])
        for b in xtra:
            p, r = skyx[b], xrates.get(b)
            ws.append(['SKY', '', 'S', b, p[2], p[0], p[1], 'n/a' if r is None else r[0], 'n/a' if r is None else r[1]])
        for P in sorted(runners):
            for C in 'HJ':
                for b, p in runners[P][C + 'X'].items():
                    if b not in runners[P][C]:
                        ws.append([P, runners[P]['name'], C, b, p[2], p[0], p[1]])
    # SKY JUPITER
    ws = wb.create_sheet('SKY JUPITER')
    ws.cell(row=1, column=1, value=f'{race} — S Jupiter to every sky body, star and the equator (at the off and +5 min)').font = BOLD
    R0 = {'H': {}, 'J': {}}
    skind = lambda a, b: 'equator' if b.endswith(' equator') else 'dist'
    rows = [(f'S Jupiter → S {x}', 'S Jupiter', f'S {x}') for x in skyx if x != 'Jupiter']     # stars on T1_T2_T24_STARS (Eddie, 19 Oct 2026)
    row, _ = write_pairs(ws, 3, 'SKY', 'S Jupiter → sky points', ctx.x, R0, rows, skind, timing=True)
    sky_nums = []                                          # NUMBERS keep the SKY rows on STARS, as before: fed off-sheet
    write_pairs(openpyxl.Workbook().active, 3, 'SKY', '', ctx, R0, [(f'S Jupiter → S {x}', 'S Jupiter', f'S {x}') for x in sky if x != 'Jupiter'],
                skind, nums=sky_nums, timing=True)
    skyeq = [dict(h, tid='SKY EQ') for h in equi_hits(ctx, R0, 'S Jupiter', [f'S {z}' for z in SKY_BODIES if z in sky and z != 'Jupiter'], 'SKY EQ')]
    row = write_equi(ws, row, 'EQUIDISTANCE: S Jupiter with two sky bodies', skyeq)
    skypairs = t19_filter(pair_rows(ctx, R0, None, tid='SKY PAIRS', blocks=sky_pair_blocks(ctx)))
    # SKY STARS on the 46 stars (Eddie, 20 Oct 2026); pair orientation: the old STARS order, then the new stars in RA order, so every old pair keeps
    # its X / Y as before
    skystars = t19_filter(pair_rows(ctx.x, R0, [x for x in STARS if x in T1_T2_T24_STARS] + [x for x in T1_T2_T24_STARS if x not in STARS],
                                    tid='SKY STARS', sky=True))
    row = write_pair_blocks(ws, row, 'SKY PAIRS (Eddie, 14 Oct): S Jupiter on every pair of sky bodies (Moon included), and (15 Oct 2026) on every sky body '
                       'with a royal star (Aldebaran, Regulus, Antares, Fomalhaut; race-day positions; block "body – royal"; no star–star), filtered as T19 '
                       '(ratio on an interval, or a midpoint hit, or all three distances with a family hit; "X, Y together" left out; best first by the higher '
                       'of the ratio score and the midpoint total): '
                       'd(S Jup, X), d(S Jup, Y), d(X, Y) with their best family (score, timing); ratio larger / smaller on the interval list '
                       '(area A ±0.02 absolute, area B tapered %; timing); between / far side; planes RA, Dec, Equator (only when S Jupiter, X, Y '
                       'straddle the equator); Ketu in every plane; the sky Rahu–Ketu pair never paired; a Ketu row repeating the Rahu row dropped',
                            skypairs, 'SKY PAIRS')
    row = write_pair_blocks(ws, row, 'SKY STARS (background, once per race; 20 Oct 2026: the 46 stars of T1 / T2 / T24, RA order, no Polaris): S Jupiter on two sky stars, filtered as T19 (ratio on an interval, '
                      'or all three distances with a family hit; "X, Y together" left out)',
                      skystars, 'SKY STARS')
    roy = [f'S {x}' for x in STARS if x in ROYAL and x in ctx.S0]
    srows = pair_rows(ctx, R0, None, tid='SKY ROYAL', blocks=[('royal – royal', list(itertools.combinations(roy, 2))), sky_pair_blocks(ctx)[1]])
    srows.sort(key=lambda h: -max(h['ev']['score'] if h['ev'] else -1, -1 if h['mid'] is None else h['mid']))
    row = write_pair_blocks(ws, row, 'SKY ROYAL (Eddie, 16 Oct 2026; royal stars only): S Jupiter on the six pairs of Aldebaran, Regulus, Antares, '
                            'Fomalhaut ("royal – royal") and every sky body with a royal star ("body – royal", the SKY PAIRS rows), race-day positions; '
                            'every row listed (hits and non-hits); a row with "X, Y together" is plain, in NO HIT; same cells and areas as SKY PAIRS, best '
                            'first inside each block',
                            srows, 'SKY ROYAL', every=True, notog=True)
    row, _, _ = write_t24(ws, row + 1, skyx, 'S', f'T24 SKY (race-day positions at the off, Moon included): {T24_NOTE}')     # Eddie, 19 Oct 2026
    srcs = (('SKY PAIRS', skypairs), ('SKY STARS', skystars), ('SKY ROYAL', srows))
    # sky TIMELINE / LONG TIMELINE on the 46 stars (Eddie, 20 Oct 2026): SKY star events from the sky on T1_T2_T24_STARS (ctx.x), as the SKY block
    row = write_timeline(ws, row, ctx.x, timeline(ctx.x, R0, skyeq, srcs))
    row = write_long(ws, row, ctx.x, realise(ctx.x, R0, timeline(ctx.x, R0, skyeq, srcs, keep=long_keep)), 'LONG TIMELINE',
                     'LONG TIMELINE (Eddie, 16 Oct 2026): every sky Jupiter event on this sheet scoring >= 80 at the off, any exact time (same sources '
                     'and rules as TIMELINE). Exact time: beyond 60 min the real time from the Swiss Ephemeris (race engine and site; stepping out from the off, '
                     'refined to the minute, up to 1 year each way, else "not within 1 year"), the linear estimate in the last column; each section by score at the off, highest first (ties by exact time)')
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
            ws.cell(row=r, column=c, value=f'unison: {auto_text(auto)}, not counted' if auto
                    else f'unison: field {uni[k]}/{n}' + (' ' + assist_text(assisted) if assisted else ''))
        pairs_sheet(wbp, P, runners[P], fields[P]['_pairs'])
        if a.full:                                         # P## RATIOS, P## NUMBERS only with --full (Eddie, 19 Oct 2026)
            ratio_sheet(wb, P, runners[P], fields[P]['_rats'], uni, n)
            numbers_sheet(wb, P, runners[P], sky_nums + fields[P]['_nums'])
    if a.full:                                             # FIELD sheets, THREADS, FIELD NUMBERS only with --full (Eddie, 19 Oct 2026)
        full_sheets(wb, runners, fields, uni, sky_nums)
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
