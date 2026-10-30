#!/usr/bin/env python3
"""jupiter_tables.py INPUT [--out X.xlsx] [--off "YYYY-MM-DD HH:MM"] [--site lat,lon,elev] [--full]
Viewing tool (13 Oct 2026, Eddie): raw Jupiter tables for one race, nothing filtered.
INPUT = a race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx (TRANS, P01..Pnn, META) or a split race folder in reference/classic
(<course>_<hhmm>_<yyyymmdd>/<race>__P##.xlsx). Output: race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx next to the batch
(for a folder: in reference/classic/), unless --out.

TRIMMED (Eddie, 29 Oct 2026): the workbook is POSITIONS, SKY JUPITER (whole, unchanged) and one sheet per runner with T1-T8, T24 HORSE
and T24 JOCKEY only (T24 HORSE / JOCKEY: the four Jupiter rows and a 'stars' row above the star rows); --full is accepted and changes
nothing; no _pairs workbook. Removed that day: T9-T14, T16-T23, T21R, T22R, T24 H / J, T24 HORSE / JOCKEY RATIOS, T24 HORSE / JOCKEY (SKY
STARS), the runner timelines, SKY STARS SUMMARY, P## RATIOS / NUMBERS, THREADS, every FIELD sheet, P## PAIRS. The history below describes
the tables as they were built (code in git before 29 Oct 2026).

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
LONG TIMELINE (16 Oct 2026): score >= 80 at the off (>= 90 since 22 Oct 2026), any exact time, SEPARATING / APPLYING; sky equivalent cells on TIMELINE H / J and LONG H / J.
Timelines on every star (22 Oct 2026): runner timelines also take star events for the 67 stars (S Jup→star, star→Jup, S Jup on star pair,
star apex; off-sheet); STAR TIMELINE (sky) and STAR TIMELINE H / J = the timeline events between Jupiter and stars only; LONG STAR TIMELINE (sky) and LONG STAR
TIMELINE H / J the same for the LONG timelines (22 Oct 2026).
T24 (19 Oct 2026): stars against bodies, one row per star, RA / Dec distance per body, coloured by the best family, a cell comment with
target, family, offset, score; SKY block on SKY JUPITER (Moon included), HORSE and JOCKEY blocks on each runner sheet after T22R.
Stars (Eddie, 19 Oct 2026): T1, T2, T24 and the SKY block use T1_T2_T24_STARS (67 stars with |Dec| <= 50: STARS without Polaris + 13 new, 11 more 20 Oct 2026, 20 more and the Orion Nebula Cluster 21 Oct 2026,
in RA order); every other table (and TIMELINE, NUMBERS) keeps STARS (23, Polaris included); the new stars' positions are appended to POSITIONS. Default workbook (19 Oct 2026):
POSITIONS, SKY JUPITER and the runner sheets only; --full also writes P## RATIOS, P## NUMBERS, THREADS, FIELD NUMBERS and every FIELD sheet.
T24 ratio tables (Eddie, 19 Oct 2026; natal only): T24 H / J (d(H star, H Jupiter) / d(J star, J Jupiter)), T24 HORSE RATIOS and T24 JOCKEY
RATIOS (d(star, Jupiter) / d(star, X), same chart), on each runner sheet after T24 JOCKEY; not in THREADS, NUMBERS, RATIOS, FIELD or TIMELINEs.
SKY STARS and the sky TIMELINE / LONG TIMELINE (Eddie, 20 Oct 2026): on the 67 stars (21 Oct 2026) (ctx.x), as the SKY block; runner timelines on STARS.
T24 HORSE / JOCKEY (SKY STARS) (Eddie, 27 Oct 2026): after T24 JOCKEY RATIOS, the T24 rows of the stars whose S Jupiter → S star SKY block cell
scores (RA or Dec), copied, with the sky hit and a SCORES block; sheet SKY STARS SUMMARY (after the runner sheets) = those tables per runner.
T24 HORSE / JOCKEY "S Jupiter" column (Eddie, 27 Oct 2026): d(S Jupiter, S star) after Ketu in RA and Dec (= the SKY block); the (SKY STARS)
tables carry it (and its SCORES) and four Jupiter rows on top (S Jupiter → S body, natal Jupiter → natal body, S Jupiter → natal body, S body → natal Jupiter).
Points and engine from tools/jup2 (imported, not changed). Frozen readers are not changed."""
import argparse, glob, os, re, sys, itertools, math, datetime
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
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
             'Rasalhague',                                 # Eddie, 20 Oct 2026: 11 more, the same tables as the 13 (RA order)
             'Ankaa', 'Al Rescha', 'Mirfak', 'El Nath', 'Meissa', 'Alnilam', 'Murzim', 'Alhena', 'Acubens', 'Alphard', 'Alkes', 'Zosma',
             'Vindemiatrix', 'Diadem', 'Ras Algethi', 'Aculeus', 'Acumen', 'Facies', 'Rukbat',
             'Sualocin',                                   # Eddie, 21 Oct 2026: 20 more, the same tables as the 11 (RA order)
             'Orion Nebula Cluster']                       # Eddie, 21 Oct 2026: the 67th, the same tables
# the 67 stars with |Dec| <= 50 (Eddie, 19 Oct 2026; 46 since 20 Oct 2026, 67 since 21 Oct 2026): STARS without Polaris + NEW_STARS, in RA order (engine J2000 RA at J2000.0, ascending;
# one fixed order, Eddie 19 Oct 2026); T1, T2, T24 and the SKY block star rows; every other table keeps STARS
T1_T2_T24_STARS = ['Alpheratz', 'Algenib', 'Ankaa', 'Difda', 'Mirach', 'Al Rescha', 'Hamal', 'Menkar', 'Algol', 'Mirfak', 'Pleiades',
                   'Aldebaran', 'Rigel', 'Capella', 'Bellatrix', 'El Nath', 'Meissa', 'Orion Nebula Cluster', 'Alnilam', 'Phact',
                   'Betelgeuse', 'Murzim', 'Alhena', 'Sirius', 'Adhara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Praesepe', 'Acubens',
                   'Alphard', 'Regulus', 'Alkes', 'Zosma', 'Denebola', 'Algorab', 'Vindemiatrix', 'Diadem', 'Spica', 'Alkaid', 'Menkent',
                   'Arcturus', 'Zubenelgenubi', 'Zubeneschamali', 'Alphecca', 'Unukalhai', 'Antares', 'Ras Algethi', 'Rasalhague',
                   'Aculeus', 'Galactic Centre', 'Acumen', 'Kaus Australis', 'Facies', 'Vega', 'Nunki', 'Rukbat', 'Altair', 'Sualocin',
                   'Deneb', 'Sadalsuud', 'Deneb Algedi', 'Sadalmelik', 'Fomalhaut', 'Scheat', 'Markab']
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


def digit_text(d):
    """a value inside its family's old tolerance that fails the 4-digit match (Eddie, 24 Oct 2026): no score, no colour"""
    return f"{d['target']} {d['family']} — not a 4-digit match ({fmt_off(d)})"


def out_text(d):
    """nearest target outside every tolerance (Eddie, 13 Oct 2026): plain text, no score, no colour; inside the old tolerance but not a
    4-digit match: digit_text (24 Oct 2026)"""
    if d.get('digit'):
        return digit_text(d)
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


def write_pairs(ws, row, tid, title, ctx, R, rows, kind_of, sky=False, timing=False):
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


def runner_sheet(wb, P, R, ctx):
    """runner sheet (trimmed, Eddie 29 Oct 2026): T1-T8, T24 HORSE, T24 JOCKEY (with the five Jupiter rows on top)"""
    ws = wb.create_sheet(P)
    ws.cell(row=1, column=1, value=f"{P} {R['name']}").font = BOLD
    ws.cell(row=2, column=1, value='score (Eddie\'s families): green >= 80, yellow 50-80, light yellow < 50; midpoints (T10, T11, T17-T20): two halves, closeness >= 90 % and '
            'distance from the midpoint (RA 0.5, Dec 0.15, Equator 0.15), each squared x 0.5, a hit needs both, total = the sum; off->+5 = toward / away from the nearest target; values are never scaled x10 / /10 (16 Oct 2026)')
    row = 4
    H, J = R['H'], R['J']
    dist = lambda a, b: 'equator' if b.endswith(' equator') else 'dist'
    field = {}
    RX = {'H': R['HX'], 'J': R['JX']}                      # T1, T2 (and T24) on T1_T2_T24_STARS (Eddie, 19 Oct 2026)
    for tid, C in (('T1', 'H'), ('T2', 'J')):
        rows = [(f'{C} Jupiter → {C} {x}', f'{C} Jupiter', f'{C} {x}') for x in RX[C] if x != 'Jupiter']
        row, field[tid] = write_pairs(ws, row, tid, f'{C} Jupiter → {C} bodies, stars, equator (natal); SKY cells S Jupiter → S X beside each row',
                                      ctx.x, RX, rows, dist, sky=True)
    row, _ = write_pairs(ws, row, 'T3', 'H Jupiter → J bodies (natal, cross)', ctx, R,
                         [(f'H Jupiter → J {x}', 'H Jupiter', f'J {x}') for x in NATAL_BODIES if x in J], dist)
    row, _ = write_pairs(ws, row, 'T4', 'J Jupiter → H bodies (natal, cross)', ctx, R,
                         [(f'J Jupiter → H {x}', 'J Jupiter', f'H {x}') for x in NATAL_BODIES if x in H], dist)
    for tid, C in (('T5', 'H'), ('T6', 'J')):
        rows = [(f'S Jupiter → {C} {x}', 'S Jupiter', f'{C} {x}') for x in NATAL_BODIES if x in R[C] and x != 'Jupiter']
        row, field[tid] = write_pairs(ws, row, tid, f'S Jupiter → {C} bodies, at the off and +5 min', ctx, R, rows, dist)
    for tid, C in (('T7', 'H'), ('T8', 'J')):
        rows = [(f'S {z} → {C} Jupiter', f'S {z}', f'{C} Jupiter') for z in SKY_BODIES if z in ctx.S0 and z != 'Jupiter']
        row, field[tid] = write_pairs(ws, row, tid, f'every sky body (Moon incl.) → {C} Jupiter, at the off and +5 min', ctx, R, rows, dist)
    sky = {(x, pl): v[0] for (lab, pl), v in getattr(ctx, 'skycells', {}).items()
           if lab.startswith('S Jupiter → S ') and (x := lab[14:]) in T1_T2_T24_STARS}
    for C, who in (('H', 'HORSE'), ('J', 'JOCKEY')):        # T24 (Eddie, 19 Oct 2026): stars against bodies, natal
        jr = t24_jrows(ctx, R, field, C)
        row, _, _ = write_t24(ws, row + 1, RX[C], C, f'T24 {who} (natal): {T24_NOTE}{T24SJ_NOTE}', sky=sky, jrows=jr)
        field[f'_t24c{C}'] = t24_match_cells(RX[C], C, jr)
    skym = sky_match_cells(getattr(ctx, 'skycells', {}))
    for C, who in (('H', 'HORSE'), ('J', 'JOCKEY')):        # MATCH HORSE / MATCH JOCKEY (Eddie, 30 Oct 2026), after T24 JOCKEY
        row = write_match(ws, row + 1, who, skym, field[f'_t24c{C}'])
    ws.column_dimensions['B'].width = 46
    ws.freeze_panes = 'C4'
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
    if near and near.get('digit'):
        return '', f"nearest: {digit_text(near)}"
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
DOTTED = openpyxl.styles.Side(style='dotted')      # T24 repeats (Eddie, 22 Oct 2026)


def write_t24(ws, row, ch, C, title, sky=None, jrows=()):
    """T24 block (Eddie, 19 Oct 2026): rows = stars (T1_T2_T24_STARS order, those in the chart; 19 Oct 2026); columns (revised the same day) = every body's RA
    distance (Moon only in the sky), then "RA midpoints", then every body's Dec distance, then "Dec midpoints"; cell = the distance (RA
    wrapped 0-180, Dec |ΔDec|), 6 dp, filled by its best family score (a conjunction red, 20 Oct 2026), comment = target · family · offset · score or the nearest target
    outside, plus a line per midpoint the body is in; the two body cells of a midpoint hit get a thick outline; midpoint column = every hit,
    best total first, coloured by the best. No timing, no +5, no field sheet.
    sky (T24 HORSE / JOCKEY, Eddie 27 Oct 2026): {(star, plane): d(S Jupiter, S star)} (the SKY block values) -> a column "S Jupiter" after
    Ketu in each plane, the same cell format; not in the repeats or the midpoints.
    jrows (T24 HORSE / JOCKEY, Eddie 29 Oct 2026; moved from the (SKY STARS) tables): the four Jupiter rows (t24_jrows) above the star rows,
    then a grey separator row 'stars'; not in the repeats, the midpoints or the title counts.
    -> (next row, {(star, body, plane): (v, colour, text)}, {(star, plane): [midpoint hits]})"""
    bodies = [b for b in T24_BODIES if b in ch and ch[b][2] == 'body' and (C == 'S' or b != 'Moon')]
    stars = [x for x in T1_T2_T24_STARS if x in ch]
    n = len(bodies)
    m = n + (sky is not None)                              # value columns per plane: the bodies (+ S Jupiter on HORSE / JOCKEY)
    c0 = {'RA': 3, 'Dec': 3 + m + 1}                       # first body column of each half; its midpoint column at c0 + m
    ws.cell(row=row, column=1, value='T24').font = BOLD
    ws.cell(row=row, column=2, value=title).font = BOLD
    row += 1
    for r in (row, row + 1):
        for c, v in ((1, 'table'), (2, 'star')):
            ws.cell(row=r, column=c, value=v if r == row else None).fill = HEAD
    for pl in PLANES:
        c = ws.cell(row=row, column=c0[pl], value=pl); c.fill = HEAD; c.font = BOLD
        for k in range(1, m):
            ws.cell(row=row, column=c0[pl] + k).fill = HEAD
        ws.merge_cells(start_row=row, start_column=c0[pl], end_row=row, end_column=c0[pl] + m - 1)
        for i, b in enumerate(bodies + (['S Jupiter'] if sky is not None else [])):
            c = ws.cell(row=row + 1, column=c0[pl] + i, value=b); c.fill = HEAD; c.font = BOLD
        for r, v in ((row, f'{pl} midpoints'), (row + 1, 'star = middle of A, B: total (side, between / far side)')):
            c = ws.cell(row=r, column=c0[pl] + m, value=v); c.fill = HEAD; c.font = BOLD
    crep = c0['Dec'] + m + 1                               # repeats column (Eddie, 22 Oct 2026), after "Dec midpoints"
    for r, v in ((row, 'repeats'), (row + 1, 'target family ×n (body plane (score), ...)')):
        c = ws.cell(row=r, column=crep, value=v); c.fill = HEAD; c.font = BOLD
    trow = row - 1
    row += 2
    for lab, vals in jrows:                                # the four Jupiter rows (Eddie, 29 Oct 2026), as on the (SKY STARS) tables before
        ws.cell(row=row, column=1, value='T24')
        ws.cell(row=row, column=2, value=lab)
        for pl in PLANES:
            for i, b in enumerate(bodies):
                if vals.get((b, pl)) is not None:
                    t24_put(ws, row, c0[pl] + i, vals[(b, pl)], pl)
        row += 1
    if jrows:
        ws.cell(row=row, column=1, value='T24')
        ws.cell(row=row, column=2, value='stars').font = BOLD
        for k in range(1, crep + 1):                       # light grey across the block, A to the repeats column
            ws.cell(row=row, column=k).fill = GREY
        row += 1
    out, mids = {}, {}
    nrep, ntgt = 0, 0
    for x in stars:
        best = {}                                          # (body, plane) -> (target key, score) of the cell's best target (no conjunction)
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
                ev, _ = nearest(v, 'dist', pl)
                if ev and ev['family'] != 'conj' and v >= families.CONJ[pl]:
                    best[(b, pl)] = (f"{ev['target']} {ev['family']}", ev['score'])
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
            if sky is not None and (x, pl) in sky:         # S Jupiter column (Eddie, 27 Oct 2026): d(S Jupiter, S star) = the SKY block value
                v = sky[(x, pl)]
                colour, text = t24_cell(v, pl)
                c = ws.cell(row=row, column=c0[pl] + n, value=round(v, 6))
                c.number_format = '0.000000'
                if v < families.CONJ[pl]:
                    c.fill = RED
                elif colour:
                    c.fill = FILL[colour]
                c.comment = Comment(text, 'T24', width=260, height=40)
            if hits:
                c = ws.cell(row=row, column=c0[pl] + m, value='; '.join(t24_mid_text(h) for h in hits))
                c.fill = FILL[families.colour(hits[0]['score'])]
        # REPEATS (Eddie, 22 Oct 2026): the same best target (family and target number, no x10 / /10 folding) in two or more body cells of
        # the row, any planes; conjunction cells left out. Column: most cells first, then the highest score; cells by score. Each repeated
        # cell: dotted outline (a midpoint thick outline kept) and a comment line
        grp = {}
        for (b, pl), (k, sc) in best.items():
            grp.setdefault(k, []).append((b, pl, sc))
        reps = []
        for k, cells in grp.items():
            if len(cells) >= 2:
                cells.sort(key=lambda z: (-z[2], PLANES.index(z[1]), bodies.index(z[0])))
                reps.append((k, cells))
        reps.sort(key=lambda kc: (-len(kc[1]), -kc[1][0][2]))
        if reps:
            nrep += 1
            ntgt += len(reps)
            c = ws.cell(row=row, column=crep, value='; '.join(f"{k} ×{len(cells)} (" + ', '.join(f'{b} {pl} ({sc:.2f})' for b, pl, sc in cells) + ')'
                                                              for k, cells in reps))
            c.alignment = openpyxl.styles.Alignment(wrap_text=True, vertical='top')
            for k, cells in reps:
                for b, pl, sc in cells:
                    c = ws.cell(row=row, column=c0[pl] + bodies.index(b))
                    others = ', '.join(f'{b2} {pl2} ({sc2:.2f})' for b2, pl2, sc2 in cells if (b2, pl2) != (b, pl))
                    txt = c.comment.text + f'\nrepeat: {k} ×{len(cells)} (with {others})'
                    c.comment = Comment(txt, 'T24', width=260, height=40 + 15 * txt.count('\n'))
                    if not (c.border and c.border.left and c.border.left.style == 'thick'):
                        c.border = openpyxl.styles.Border(left=DOTTED, right=DOTTED, top=DOTTED, bottom=DOTTED)
        row += 1
    ws.cell(row=trow, column=2, value=f'{title}. REPEATS (22 Oct 2026): {nrep} of {len(stars)} rows with a repeat, {ntgt} repeated targets').font = BOLD
    # display (Eddie, 19 Oct 2026): value columns wide enough for 177.745864, star names ~18, midpoint columns wider; shared columns only
    # ever widened
    def lay(mm):                                           # widths of the layout with mm value columns per plane
        cc = {'RA': 3, 'Dec': 3 + mm + 1}
        return ([(cc[pl] + k, T24_VAL_W) for pl in PLANES for k in range(mm)] + [(cc[pl] + mm, T24_MID_W) for pl in PLANES]
                + [(cc['Dec'] + mm + 1, T24_REP_W)])
    widths = [(2, T24_NAME_W)] + lay(m)                    # the layout's own widths (Eddie, 27 Oct 2026: "never narrower" dropped)
    for col, w in widths:
        L = openpyxl.utils.get_column_letter(col)
        if L not in ws.column_dimensions or not ws.column_dimensions[L].customWidth:
            ws.column_dimensions[L].width = w
        else:
            ws.column_dimensions[L].width = max(ws.column_dimensions[L].width, w)
    return row + 1, out, mids


T24_MID_W = 40
T24_REP_W = 60                                             # repeats column (Eddie, 22 Oct 2026)
T24_VAL_W, T24_NAME_W = 11, 18


T24_NOTE = ('stars against bodies (Eddie, 19 Oct 2026): one row per star; the RA distance of every body, RA midpoints, the Dec '
            'distance of every body, Dec midpoints; cell = the distance (RA wrapped 0–180, '
            'Dec |ΔDec|), coloured by its best family score (green >= 80, yellow 50–80, light < 50; conjunction RA < 1.5 / Dec < 0.3 counts, '
            'as T1, but filled red; no fill outside); cell comment = target · family · offset · score, or the nearest target outside. MIDPOINTS: the star as the '
            'middle point of two bodies A, B (closeness of d(star, A), d(star, B) >= 90 % and the star within RA ±0.5 (closer of near / far) / '
            'Dec ±0.15 of their midpoint; total = ratio half + distance half; hits only, best first; own Rahu – Ketu, "A, B together" (RA < 1.5, '
            'Dec < 0.3) and Ketu repeats of a Rahu pair left out; between / far side as T17); the two body cells get a thick outline and a '
            'comment line. REPEATS (22 Oct 2026): the same best target (family and target number, no x10 / /10 folding; conjunction cells '
            'left out) in two or more body cells of a row, any planes - listed in the "repeats" column (most cells first, then by the highest '
            'score), dotted outline and a comment line on each repeated cell (a midpoint thick outline kept). No timing, no +5')


def t24_jrows(ctx, R, field, C):
    """the four Jupiter rows of T24 HORSE / JOCKEY (Eddie, 27 Oct 2026 on the (SKY STARS) tables; 29 Oct 2026 in T24), values taken from the
    tables on the sheet (T1 / T2 with their SKY cells, T5–T8); the Jupiter column on the last two = d(S Jupiter, natal Jupiter), computed
    here (T9 removed 29 Oct 2026). -> [(label, {(body, plane): distance or None})]; None (blank) where a point meets itself"""
    t12, t58, t78 = ('T1', 'T5', 'T7') if C == 'H' else ('T2', 'T6', 'T8')
    g = lambda tab, key: (field.get(tab, {}).get(key) or (None,))[0]
    sj = lambda pl: ctx.pair(R, 'S Jupiter', f'{C} Jupiter', pl)[0]       # d(S Jupiter, natal Jupiter)
    out = []
    for lab, f in (('S Jupiter → S body', lambda b, pl: None if b == 'Jupiter' else g(t12, (f'{C} Jupiter → {C} {b}', pl, 'sky'))),
                   (f'{C} Jupiter → {C} body', lambda b, pl: None if b == 'Jupiter' else g(t12, (f'{C} Jupiter → {C} {b}', pl))),
                   (f'S Jupiter → {C} body', lambda b, pl: sj(pl) if b == 'Jupiter' else g(t58, (f'S Jupiter → {C} {b}', pl))),
                   (f'S body → {C} Jupiter', lambda b, pl: sj(pl) if b == 'Jupiter' else g(t78, (f'S {b} → {C} Jupiter', pl)))):
        out.append((lab, {(b, pl): f(b, pl) for b in T24_BODIES for pl in PLANES}))
    return out


def t24_put(ws, row, col, v, pl):
    """one T24-format distance cell (value 6 dp, best family fill, conjunction red, comment) -> the cell"""
    colour, text = t24_cell(v, pl)
    c = ws.cell(row=row, column=col, value=round(v, 6))
    c.number_format = '0.000000'
    if v < families.CONJ[pl]:
        c.fill = RED
    elif colour:
        c.fill = FILL[colour]
    c.comment = Comment(text, 'T24', width=260, height=40)
    return c


# ---------------- MATCH HORSE / MATCH JOCKEY (Eddie, 30 Oct 2026): SKY block hits against T24 HORSE / JOCKEY hits
MATCH_HEAD = ('table', 'section', 'ratio p/q', 'ratio', 'shared factor', 'circle factor', 'slice of 360', 'sky: relationship', 'plane', 'value', 'family', 'target', 'score',
              'T24: row', 'body', 'plane', 'value', 'family', 'target', 'score', 'lower score')
MATCH_RATIO_FAM = ('whole', 'golden')                      # ratio matches: whole and golden only, for now
MATCH_CIRCLE_MIN = 5                                       # whole: circle factor gcd(A, B, 360) >= 5 (Eddie, 30 Oct 2026, tightened)
MATCH_GOLDEN_MAX = 6                                       # golden: p and q of the ratio in lowest terms <= 6 (Eddie, 30 Oct 2026)


def match_cell(v, ev):
    """a scoring cell for MATCH: (value 6 dp, best family, target label, score, colour) or None (no score, or a conjunction: target 0)"""
    if not ev or ev['family'] == 'conj':
        return None
    return round(v, 6), ev['family'], ev['target'], ev['score'], ev['colour']


def sky_match_cells(skycells):
    """SKY block (SKY JUPITER): every scoring cell, S Jupiter → every sky body, star and the equator, RA and Dec (sheet order)"""
    out = []
    for (lab, pl), (v, ev) in skycells.items():
        m = match_cell(v, ev)
        if m:
            out.append((lab, pl) + m)
    return out


def t24_match_cells(ch, C, jrows):
    """T24 HORSE / JOCKEY: every scoring cell of the Jupiter rows (not 'S Jupiter → S body'; Jupiter cell incl.) and of the star rows (body
    columns, not the S Jupiter column), RA and Dec, in sheet order -> [(row label, body, plane, value, family, target, score, colour)]"""
    bodies = [b for b in T24_BODIES if b in ch and ch[b][2] == 'body' and b != 'Moon']
    out = []
    for lab, vals in jrows:
        if lab == 'S Jupiter → S body':
            continue
        for pl in PLANES:
            for b in bodies:
                v = vals.get((b, pl))
                m = v is not None and match_cell(v, nearest(v, 'dist', pl)[0])
                if m:
                    out.append((lab, b, pl) + m)
    for x in [x for x in T1_T2_T24_STARS if x in ch]:
        for pl in PLANES:
            for b in bodies:
                v = plane_value(ch[x], ch[b], pl)
                m = match_cell(v, nearest(v, 'dist', pl)[0])
                if m:
                    out.append((f'{C} {x}', b, pl) + m)
    return out


def golden_k(t):
    return int(t.split('×')[0])


def match_pairs(sky, t24):
    """-> (exact, ratio) rows. EXACT: same family and target, or (different families) the two values' first 4 significant digits, truncated,
    the same at the same order of magnitude (families.digits4). RATIO: same family, whole or golden, different targets whose whole numbers /
    φ multipliers share a factor >= 2: p/q = larger / smaller in lowest terms. Tightened (Eddie, 30 Oct 2026): whole only when the circle factor
    gcd(A, B, 360) >= 5 (slice of 360 = 1/(360 / circle factor)); golden only when p and q <= 6.
    Row: (p/q, decimal, factor, circle factor, slice, sky cell, T24 cell, lower score)"""
    exact, ratio = [], []
    for s in sky:
        for t in t24:
            sf, st, tf, tt = s[3], s[4], t[4], t[5]
            low = min(s[5], t[6])
            if (sf == tf and st == tt) or (sf != tf and families.digits4(s[2]) == families.digits4(t[3])):
                exact.append(('1', 1.0, None, None, None, s, t, low))
            elif sf == tf and sf in MATCH_RATIO_FAM:
                a, b = (int(st), int(tt)) if sf == 'whole' else (golden_k(st), golden_k(tt))
                g = math.gcd(a, b)
                hi, lo = max(a, b), min(a, b)
                if sf == 'whole':
                    cf = math.gcd(g, 360)
                    if cf >= MATCH_CIRCLE_MIN:
                        ratio.append((f'{hi // g}/{lo // g}', hi / lo, f'{g}', cf, f'1/{360 // cf}', s, t, low))
                elif g >= 2 and hi // g <= MATCH_GOLDEN_MAX and lo // g <= MATCH_GOLDEN_MAX:
                    ratio.append((f'{hi // g}/{lo // g}', hi / lo, f'{g}×φ', None, None, s, t, low))
    # order (Eddie, 30 Oct 2026, revised): the sky cell's score, highest first (each sky cell's matches together; ties: SKY block order);
    # RATIO inside a sky cell by q, then p of p/q (whole-number ratios first); then the T24 score, highest first; then T24 order
    si, ti = {id(x): i for i, x in enumerate(sky)}, {id(x): i for i, x in enumerate(t24)}
    pq = lambda r: tuple(int(z) for z in r[0].split('/'))
    exact.sort(key=lambda r: (-r[5][5], si[id(r[5])], -r[6][6], ti[id(r[6])]))
    ratio.sort(key=lambda r: (-r[5][5], si[id(r[5])], pq(r)[1], pq(r)[0], -r[6][6], ti[id(r[6])]))
    return exact, ratio


MATCH_NOTE = ('every scoring cell of the SKY block (SKY JUPITER: S Jupiter → every sky body, star and the equator, RA and Dec) against every '
              'scoring cell of T24 {who} (star rows × body columns, not the S Jupiter column; the Jupiter rows {C} Jupiter → {C} body, S Jupiter → '
              '{C} body, S body → {C} Jupiter incl. their Jupiter cell, not S Jupiter → S body), either plane with either plane; scoring = the '
              "cell's best family has a score (any score); conjunction cells (target 0) left out. EXACT: same family and same target, or across "
              'families the two values (6 dp) with the same first 4 significant digits, truncated, at the same order of magnitude; order below. '
              'RATIO (same family, whole and golden only; tightened 30 Oct 2026): whole - kept only when the circle '
              'factor gcd(A, B, 360) >= 5 (the largest number dividing both targets and 360; slice of 360 = 1/(360 / circle factor)), shared '
              'factor = gcd(A, B); golden n×φ - the two multipliers share a factor >= 2 and the ratio in lowest terms p/q has p, q <= 6; ratio = '
              'larger / smaller in lowest terms. ORDER (30 Oct 2026, grouped by sky cell): one list, grouped by sky cell (SKY block '
              'relationship + plane), each group under a grey header row \'<sky relationship> <plane> <value> <target> <family> (<score>) — '
              'EXACT n, RATIO m\'; groups by the sky cell\'s score, highest first (ties: SKY block order, a row\'s RA cell before its Dec cell); '
              'inside a group the EXACT rows first (T24 score highest first, then T24 order), then the RATIO rows by the bottom number q of p/q, '
              'smallest first (whole-number ratios first: 2, 3, 4 ..., then 3/2, 5/2 ..., then 4/3, 5/3 ...), then p, then the T24 score highest '
              'first, then T24 order; the section column says EXACT or RATIO on every row. Ninths, φ powers, √2, silver: exact only. Score cells '
              'coloured by their score as the source cells')


def write_match(ws, row, who, sky, t24):
    """MATCH HORSE / MATCH JOCKEY block -> next row + 1"""
    tid, C = f'MATCH {who}', who[0]
    exact, ratio = match_pairs(sky, t24)
    ws.cell(row=row, column=1, value=tid).font = BOLD
    ws.cell(row=row, column=2, value=f'{tid} (Eddie, 30 Oct 2026): {MATCH_NOTE.format(who=who, C=C)}. EXACT {len(exact)} rows, RATIO '
                                     f"{len(ratio)} rows (whole {sum(1 for r in ratio if r[3] is not None)}, golden {sum(1 for r in ratio if r[3] is None)}), "
                                     f'{len({id(r[5]) for r in exact + ratio})} sky cells (SKY block {len(sky)} scoring cells, T24 {who} {len(t24)})').font = BOLD
    row += 1
    for k, h in enumerate(MATCH_HEAD):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    row += 1
    groups = {}                                            # sky cell -> [(section, row)]; exact / ratio already in group order
    for sec, rows in (('EXACT', exact), ('RATIO', ratio)):
        for r in rows:
            groups.setdefault(id(r[5]), (r[5], []))[1].append((sec, r))
    si = {id(x): i for i, x in enumerate(sky)}
    for s, grp in sorted(groups.values(), key=lambda g: (-g[0][5], si[id(g[0])])):
        ne = sum(1 for sec, _ in grp if sec == 'EXACT')
        ws.cell(row=row, column=1, value=tid)
        ws.cell(row=row, column=2, value=f'{s[0]} {s[1]} {s[2]:.6f} {s[4]} {s[3]} ({s[5]:.2f}) — EXACT {ne}, RATIO {len(grp) - ne}').font = BOLD
        for k in range(1, len(MATCH_HEAD) + 1):
            ws.cell(row=row, column=k).fill = GREY
        row += 1
        for sec, (pq, dec, g, cf, sl, s, t, low) in grp:
            vals = [tid, sec, pq, round(dec, 6), g, cf, sl, s[0], s[1], s[2], s[3], s[4], round(s[5], 2), t[0], t[1], t[2], t[3], t[4], t[5],
                    round(t[6], 2), round(low, 2)]
            for k, v in enumerate(vals):
                ws.cell(row=row, column=1 + k, value=v)
            for col, sc, colour in ((13, s[5], s[6]), (20, t[6], t[7]), (21, low, families.colour(low))):
                c = ws.cell(row=row, column=col)
                c.number_format = '0.00'
                if colour:
                    c.fill = FILL[colour]
            for col in (10, 17):
                ws.cell(row=row, column=col).number_format = '0.000000'
            row += 1
    return row + 1


T24SJ_NOTE = ('. S JUPITER column (Eddie, 27 Oct 2026): after Ketu in each plane, d(S Jupiter, S star) at the off = the SKY block value, '
              'same cell format; not in the repeats or the midpoints')


# ---------------- pair-row cells (T21 / T22 used them; removed 29 Oct 2026): SKY PAIRS, SKY STARS, SKY ROYAL
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


# ---------------- EQUIDISTANCE (Eddie, 14 Oct 2026)
EQ_PLANES = ('RA', 'Dec', 'Equator')                       # Flat and GC removed (Eddie, 14 Oct 2026)
EQ_HEAD = ('table', 'Jupiter: X = Y', 'plane', 'd(Jup, X)', 'd(Jup, Y)', 'closeness %', 'midpoint offset',
           'ratio half', 'distance half', 'total', 'Jupiter',
           'd(X, Y)', 'd(Jup, X) + d(Jup, Y)', 'd(Jup, X)', 'family', 'd(Jup, Y)', 'family', 'd(X, Y)', 'family', 'ratio +5 min', 'off->+5',
           'unison timing')


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


# ---------------- pair rows (Eddie, 14 Oct 2026; T19 and P## PAIRS removed 29 Oct 2026): SKY PAIRS, SKY STARS, SKY ROYAL
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
LONG_MIN = 90.0                                            # LONG TIMELINE (Eddie, 16 Oct 2026): score at the off >= 90 (22 Oct 2026; was 80), any exact time
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
            kind='distance', target=tlabel(d), tv=d['tv'], v0=v0, fam=d['family'], lab=d['target'],
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
                    fam='interval', lab=n['target'],
                    score=h['ev']['score'] if h['ev'] else None, colour=h['ev']['colour'] if h['ev'] else '', out=not h['ev'])
                if h['mid'] is not None:
                    add(key('1'), exact_t(r0, r5, 1.0), src=src, rel=rel, plane=h['plane'], kind='midpoint', geo=('r', h['jup'], h['x'], h['y']),
                        target='1 · unison · midpoint (area A)',
                        tv=1.0, v0=r0, score=h['mid'], colour=h['m']['colour'], out=False)
            for (a, b), d0, d5, bf in h['legs']:
                if bf and d0:
                    dist(src, a, b, h['plane'], d0, d5, bf, True)
    return sorted(ev_by.values(), key=lambda e: e['t'])


ALL_STARS = set(STARS) | set(T1_T2_T24_STARS)


def star_event(e):
    """STAR TIMELINE (Eddie, 22 Oct 2026): an event between Jupiter and stars only - every point of the relationship a Jupiter or a star,
    at least one star"""
    if e['geo'][0] not in ('d', 'r'):
        return False
    names = [p.split(' ', 1)[1] for p in e['geo'][1:]]
    return all(n == 'Jupiter' or n in ALL_STARS for n in names) and any(n in ALL_STARS for n in names)


def sj_event(e):
    """sky STAR / LONG STAR TIMELINE (Eddie, 22 Oct 2026): events centred on S Jupiter only - 'S Jupiter → S star' and 'S Jupiter: S A – S B'
    (ratio, midpoint); a star-to-star distance (the d(A, B) leg of a pair row) is dropped"""
    g = e['geo']
    return star_event(e) and (g[1] == 'S Jupiter' if g[0] == 'r' else 'S Jupiter' in g[1:3])


S95 = 95.0                                                 # 95 / 100 / 95 times (Eddie, 22 Oct 2026)


def score_at(ctx, e, m, side=None):
    """the event's own score at m minutes from the off, sky points from the engine (ctx.eph): distance / ratio on the event's family and
    target (its own tolerance), midpoint = the midpoint total (0 when not a hit); ratio orientation and the RA near / far side of the off"""
    sk = ctx.eph.at(m)
    pos = lambda p: sk[p.split(' ', 1)[1]]
    g, pl = e['geo'], e['plane']
    if g[0] == 'd':
        v = geo_value(None, g, pl, pos)
        return next((d['score'] for d in families.evaluate(v, pl if pl in ('RA', 'Dec') else None, 'deg')
                     if d['family'] == e['fam'] and d['target'] == e['lab']), 0.0)
    dx, dy = geo_value(None, g, pl, pos)
    if not dx or not dy:
        return 0.0
    if e['kind'] == 'ratio':
        v = dx / dy if e['big'] else dy / dx
        return next((d['score'] for d in families.evaluate(v, None, 'ratio') if d['target'] == e['lab']), 0.0)
    ix = 0 if pl == 'RA' else 1
    gm = mid_geom(pos(g[2])[ix], pos(g[3])[ix], pos(g[1])[ix], pl, side)
    if gm is None:
        return 0.0
    ms = mid_score(dx, dy, gm[0], pl)
    return ms['score'] if ms and ms['hit'] else 0.0


def win95(ctx, e):
    """'> 95 since' / '< 95 from' (Eddie, 22 Oct 2026): from the exact time (the off when not within 1 year) step outward on the engine grid
    (from the off: 10 min for a day, then 1 h, up to 1 year each way) to the first minute the score is under 95, bisect to the minute ->
    (since, from) minutes from the off, 'nf' (not within 1 year) or None ('—': under 95 at the exact time)"""
    if getattr(ctx, 'eph', None) is None:
        return None, None
    g = e['geo']
    if g[0] == 'r':
        sk = ctx.eph.at(0)
        dx, dy = geo_value(None, g, e['plane'], lambda p: sk[p.split(' ', 1)[1]])
        e['big'] = dx >= dy
    side = None
    if e['kind'].startswith('midpoint') and e['plane'] == 'RA':
        sk = ctx.eph.at(0)
        side = mid_geom(sk[g[2][2:]][0], sk[g[3][2:]][0], sk[g[1][2:]][0], 'RA')[1]
    m0 = 0.0 if e.get('nf') else e['t']
    if abs(m0) > EPH_YEAR or score_at(ctx, e, m0, side) < S95:
        return None, None
    grid = sorted(EPH_DAY + [h * 60 * s for s in (1, -1) for h in range(25, EPH_YEAR // 60 + 1)])
    out = []
    for sgn in (-1, 1):
        pts = sorted((x for x in grid if (x - m0) * sgn > 0), key=lambda x: abs(x - m0))
        lo, res = m0, 'nf'
        for x in pts:
            if score_at(ctx, e, x, side) < S95:
                hi = x
                while abs(hi - lo) > 1.0:
                    mid = (lo + hi) / 2
                    if score_at(ctx, e, mid, side) < S95:
                        hi = mid
                    else:
                        lo = mid
                res = (lo + hi) / 2
                break
            lo = x
        out.append(res)
    return tuple(out)


W95_HEAD = ('> 95 since', '100', '< 95 from')
W95_NOTE = ('95 / 100 / 95 (Eddie, 22 Oct 2026): "> 95 since" = when the event\'s own score (its family / interval on its own tolerance; '
            'midpoint total) rose to 95 before the exact time, "100" = the exact time, "< 95 from" = when it falls under 95 after it; engine '
            'times (race site; 10 min for a day, then 1 h, up to 1 year each way, to the minute), "not within 1 year", "—" = under 95 at the '
            'exact time')


def w95_cells(ctx, e):
    """the three cells: clock (from the off) / 'not within 1 year' / '—'"""
    a, b = e.get('w95', (None, None))
    f = lambda t: '—' if t is None else 'not within 1 year' if t == 'nf' else f'{tl_clock(ctx, t)} ({tl_from(t)})'
    return (f(a), 'not within 1 year' if e.get('nf') else f(e['t']), f(b))


SKY_TL_HEAD = ('sky equivalent', 'sky value at the off', 'sky target', 'sky score', 'sky timing', 'same as sky')


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


def write_long(ws, row, ctx, evs, tid, title, skyf=None, w95=False):
    """LONG TIMELINE (Eddie, 16 Oct 2026): every event scoring >= 80 at the off, any exact time; SEPARATING, then APPLYING, each by
    score at the off (highest first; ties: separating most recent first, applying soonest first); runner sheets add the sky equivalent cells"""
    # Eddie 16 Oct 2026: inside each section by score at the off, highest first; ties by exact time (separating most recent first)
    # 16 Oct 2026 (Eddie): by the real time (ephemeris) beyond 60 min; 'not within 1 year' last among equal scores
    sep = sorted([e for e in evs if e['t'] < 0], key=lambda e: (-e['score'], bool(e.get('nf')), -e['t']))
    app = sorted([e for e in evs if e['t'] >= 0], key=lambda e: (-e['score'], bool(e.get('nf')), e['t']))
    ws.cell(row=row, column=1, value=f'{title}: {len(evs)} events, {len(sep)} separating, {len(app)} applying').font = BOLD
    row += 1
    head = TL_HEAD[:2] + ('from the off',) + TL_HEAD[3:] + (SKY_TL_HEAD if skyf else ()) + ('minutes from the off', 'linear estimate') + (W95_HEAD if w95 else ())
    for k, h in enumerate(head):
        c = ws.cell(row=row, column=1 + k, value=h); c.fill = HEAD; c.font = BOLD
    row += 1
    last = len(head) - 1 - (len(W95_HEAD) if w95 else 0)
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
            if w95:                                        # 95 / 100 / 95 (Eddie, 22 Oct 2026)
                for k, v in enumerate(w95_cells(ctx, e)):
                    ws.cell(row=row, column=last + 2 + k, value=v)
            row += 1
    return row + 1


def write_timeline(ws, row, ctx, evs, tid='TIMELINE', title=None, skyf=None, w95=False):
    """TIMELINE rows in time order, with marker rows for the off and the off + 5 min"""
    nb = sum(1 for e in evs if e['t'] < 0); nd = sum(1 for e in evs if 0 <= e['t'] <= 5); na = len(evs) - nb - nd
    title = title or ('TIMELINE (Eddie, 16 Oct 2026): every sky Jupiter relationship on this sheet whose exact time falls from the '
                      'off − 30 min to the off + 60 min (SKY best hit or nearest target; SKY EQ; SKY PAIRS, SKY STARS, SKY ROYAL ratio, midpoint '
                      'and each distance leg with a family hit), linear from the off and the off + 5 min as everywhere; "outside at the off" = not a hit '
                      'at the off; together rows left out, each event once (other sources in the note); values are never scaled')
    ws.cell(row=row, column=1, value=f'{title}: {len(evs)} events, {nb} before the off, {nd} in the first 5 min, {na} after').font = BOLD
    row += 1
    for k, h in enumerate(TL_HEAD + (SKY_TL_HEAD if skyf else ()) + (W95_HEAD if w95 else ())):
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
        if w95:                                            # 95 / 100 / 95 (Eddie, 22 Oct 2026)
            for k, v in enumerate(w95_cells(ctx, e)):
                ws.cell(row=row, column=1 + len(TL_HEAD) + (len(SKY_TL_HEAD) if skyf else 0) + k, value=v)
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


def num_key(fam, tv):
    """x10 / /10 forms folded: family + the digits of the target (mantissa in [1, 10))"""
    m = tv / 10 ** math.floor(math.log10(tv))
    return fam, round(m, 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('--out'); ap.add_argument('--off'); ap.add_argument('--site')
    ap.add_argument('--full', action='store_true', help='accepted, no effect (29 Oct 2026, Eddie: the --full-only sheets are removed; the '
                    'workbook is POSITIONS, SKY JUPITER and the runner sheets)')
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
        ctx.x.eph = Ephem(ctx.x)                           # sky LONG TIMELINE real exact times on the 67 stars (Eddie, 16 / 20 Oct 2026)
    except Exception as ex:                                # engine cannot run: the linear estimate stays
        print(f'ephemeris not run ({type(ex).__name__}: {ex}): LONG TIMELINE keeps the linear times')
        ctx.x.eph = None
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
    row, skycells = write_pairs(ws, 3, 'SKY', 'S Jupiter → sky points', ctx.x, R0, rows, skind, timing=True)
    ctx.skycells = skycells                                # T24 HORSE / JOCKEY "S Jupiter" column (Eddie, 27 Oct 2026)
    skyeq = [dict(h, tid='SKY EQ') for h in equi_hits(ctx, R0, 'S Jupiter', [f'S {z}' for z in SKY_BODIES if z in sky and z != 'Jupiter'], 'SKY EQ')]
    row = write_equi(ws, row, 'EQUIDISTANCE: S Jupiter with two sky bodies', skyeq)
    skypairs = t19_filter(pair_rows(ctx, R0, None, tid='SKY PAIRS', blocks=sky_pair_blocks(ctx)))
    # SKY STARS on the 67 stars (Eddie, 20 Oct 2026; 67 since 21 Oct); pair orientation: the old STARS order, then the new stars in RA order, so every old pair keeps
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
    row = write_pair_blocks(ws, row, 'SKY STARS (background, once per race; 20 Oct 2026: the 67 stars of T1 / T2 / T24, RA order, no Polaris): S Jupiter on two sky stars, filtered as T19 (ratio on an interval, '
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
    # sky TIMELINE / LONG TIMELINE on the 67 stars (Eddie, 20 Oct 2026): SKY star events from the sky on T1_T2_T24_STARS (ctx.x), as the SKY block
    stl = timeline(ctx.x, R0, skyeq, srcs)
    row = write_timeline(ws, row, ctx.x, stl)
    slt = realise(ctx.x, R0, timeline(ctx.x, R0, skyeq, srcs, keep=long_keep))
    row = write_long(ws, row, ctx.x, slt, 'LONG TIMELINE',
                     'LONG TIMELINE (Eddie, 16 Oct 2026): every sky Jupiter event on this sheet scoring >= 90 at the off (22 Oct 2026; was 80), any exact time (same sources '
                     'and rules as TIMELINE). Exact time: beyond 60 min the real time from the Swiss Ephemeris (race engine and site; stepping out from the off, '
                     'refined to the minute, up to 1 year each way, else "not within 1 year"), the linear estimate in the last column; each section by score at the off, highest first (ties by exact time)')
    # STAR / LONG STAR TIMELINE (Eddie, 22 Oct 2026): S Jupiter-centred events only (star-to-star distances dropped, same day), with the
    # 95 / 100 / 95 times from the engine
    sst, slst = [e for e in stl if sj_event(e)], [e for e in slt if sj_event(e)]
    w95n = W95_NOTE
    for e in sst + slst:
        if 'w95' not in e:
            e['w95'] = win95(ctx.x, e)
    row = write_timeline(ws, row, ctx.x, sst, 'STAR TIMELINE',     # Eddie, 22 Oct 2026
                         'STAR TIMELINE (Eddie, 22 Oct 2026): the events of TIMELINE centred on S Jupiter with stars only (S Jupiter → S star, S Jupiter: '
                         'S A – S B ratio and midpoint; star-to-star distances left out), the same rows, window and markers. ' + w95n, w95=True)
    row = write_long(ws, row, ctx.x, slst, 'LONG STAR TIMELINE',          # Eddie, 22 Oct 2026
                     'LONG STAR TIMELINE (Eddie, 22 Oct 2026): the events of LONG TIMELINE centred on S Jupiter with stars only (as STAR TIMELINE), the '
                     'same rows (score >= 90 at the off, real exact time beyond 60 min, linear estimate), sections and sort. ' + w95n, w95=True)
    ws.column_dimensions['B'].width = 30
    for P in sorted(runners):
        runner_sheet(wb, P, runners[P], ctx)
    # trimmed (Eddie, 29 Oct 2026): no SKY STARS SUMMARY, no --full-only sheets (P## RATIOS / NUMBERS, THREADS, FIELD), no _pairs workbook
    wb.save(out)
    print(f'{race}: {len(runners)} runners -> {out} ({os.path.getsize(out) / 1e6:.2f} MB); {repro}'
          + (f"; skipped (no Jupiter in a chart): {', '.join(skipped)}" if skipped else ''))


if __name__ == '__main__':
    main()
