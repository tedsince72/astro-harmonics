#!/usr/bin/env python3
"""eddie_read.py - stage 1 of Eddie's race read: collect, organise, field-flag. No lead, no ranking.

Usage:  python3 tools/eddie_read.py race_batch_<date>_<course>_<hhmm>_jupiter_tables.xlsx [--out DIR]

Reads only the tables workbook (POSITIONS, SKY JUPITER / SKY SUN / SKY MOON, the runner sheets' T24 midpoints and
MATCH rows). Never the csv. Writes two files next to the workbook (or in --out):
  <race>_eddie_read.md    the report, in Eddie's order (claude/eddie-race-read-method.md, Part 1 and Part 2)
  <race>_eddie_read.json  every piece as data (for stage 2, the narrower)

Eddie's order (6 Nov 2026):
  1 same body          sky X -> natal X, every body, both planes, both charts; loose 3-digit match; 4-digit score shown
  2-4 sky notes        S Jupiter, S Sun, S Moon lines (noted lines), conj points, hubs, the top line, sky numbers
  5 MATCH              the runner sheet's MATCH rows (EXACT / BODY / CONJ STAR) for the noted sky cells
  6 T1 / T2            natal Jupiter -> natal body / noted star that matches a note (same point or same number), or conj
  7 T24 top rows       S Jupiter / Sun / Moon -> natal body, then S body -> natal Jupiter (bodies only);
                       order Jupiter, Sun, Moon, horse then jockey, highest score first
  8 T24 star rows      the noted stars (Jupiter stars, Sun stars, Moon stars), horse and jockey together:
                       body cells, conj, midpoints (read from the T24 sheets), sky numbers carried, own centre bodies,
                       and the sky star onto natal Jupiter (S star -> H / J Jupiter)
  Part 2               threads in detail; every piece flagged 'only' or 'also: ...'
  Flags                the shapes found so far (named, field-checked, no ranking), each with its cells
  One star, one body   a fixed star's natal and sky copies onto the same natal body (same plane) are one line, the best
                       copy, the others beside it; a thread counts a star once per body (Eddie, 7 Nov 2026). The old
                       'locked line star on natal Jupiter' flag (natal and sky copy on the same number) is gone.

Rules fixed here so the output repeats race to race (Claude's choices, 6 Nov 2026; change only with Eddie):
  noted line   : a SKY block line of S Jupiter / Sun / Moon scoring >= 40 and exact within +-120 min of the off,
                 or scoring >= 90 and applying at any time, or a conj (centre within RA 1.5 / Dec 0.3) at any score and time
  a cell counts: best family score >= 50 (conj too); star rows list every scoring cell (any score, as the sheet colours them)
  loose        : whole within +-0.03 of a whole 1-200, or a non-whole family whose first 3 significant digits
                 match truncated or rounded (values >= 0.3), the value also inside that family's own tolerance
                 (golden +-0.03236, phi powers / sqrt2 / silver max(0.5 %, 0.025), ninths inside their range)
  T1 / T2      : natal Jupiter -> body or noted star >= 50 when the point is noted, the number is a sky number,
                 or the cell is a conj
  MATCH        : the runner sheet's MATCH rows whose sky cell (centre, point, plane) is a noted line
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ('.', '../rebuild_kit'):
    p = os.path.normpath(os.path.join(HERE, sub))
    if p not in sys.path:
        sys.path.insert(0, p)
import families as F  # noqa: E402

CENTRES = ('Jupiter', 'Sun', 'Moon')
SKY_SHEETS = (('SKY JUPITER', 'Jupiter'), ('SKY SUN', 'Sun'), ('SKY MOON', 'Moon'))
NOTE_MIN, NOTE_WIN, NOTE_APPLY, CONJ_MIN = 40, 120, 90, 0
CELL_MIN, STAR_HI, CONJ_LIST = 50, 0, 0
ORIG_DIGIT = F.digit_match


# ---------------------------------------------------------------- basics
def dist(a, b, pl):
    if pl == 'RA':
        x = abs(a[0] - b[0]) % 360
        return min(x, 360 - x)
    return abs(a[1] - b[1])


def best(v, pl):
    e = F.best(v, pl)
    return e


def lim(pl):
    return 1.5 if pl == 'RA' else 0.3


def d3(x):
    x = round(x, 10)
    k = math.floor(math.log10(x))
    m = round(x * 10 ** (2 - k), 6)
    if m >= 1000:
        k, m = k + 1, round(x * 10 ** (1 - k), 6)
    elif m < 100:
        k, m = k - 1, round(x * 10 ** (3 - k), 6)
    return k, math.floor(m)


def r3(x):
    k, _ = d3(x)
    m = round(x * 10 ** (2 - k))
    return (k + 1, 100) if m >= 1000 else (k, m)


def loose(v, pl):
    """Loose same-body match: (target, family) or None."""
    if v < 0.3:
        return None
    t = round(v)
    if 1 <= t <= 200 and abs(v - t) < 0.03:
        return str(t), 'whole'
    F.digit_match = lambda x, tt: x > 0 and tt > 0 and d3(tt) in (d3(x), r3(x))
    try:
        ev = F.evaluate(v, pl)
    finally:
        F.digit_match = ORIG_DIGIT
    ev = [e for e in ev if e['family'] not in ('whole', 'conj')]
    return (ev[0]['target'], ev[0]['family']) if ev else None


def circle(target, family):
    if family == 'whole' and target.isdigit():
        t = int(target)
        if t >= 1 and 360 % t == 0:
            return f'360/{360 // t}'
    return ''


def mins(t):
    m = re.search(r'\((?:in )?([\d.]+) min( ago)?\)', t or '')
    return float(m.group(1)) if m else 1e9


def tf(e):
    """target, family and score as written in every cell: '45 whole (54.84)', 'conj (53.18)'."""
    if e['family'] == 'conj':
        return f"conj ({e['score']:.2f})"
    return f"{e['target']} {e['family']} ({e['score']:.2f})"


def cell(label, pl, x, e):
    return f"{label} {pl} {x:.4f} {tf(e)}"


def golden_mult(target):
    m = re.match(r'^(\d+)×φ$', target or '')
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- load
def load(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    P, kinds, names = {}, {}, {}
    for r in wb['POSITIONS'].iter_rows(values_only=True):
        if r and len(r) > 6 and isinstance(r[5], (int, float)) and r[2] in ('S', 'H', 'J'):
            if r[3] == 'Polaris':
                continue
            P[(r[0], r[2], r[3])] = (float(r[5]), float(r[6]))
            kinds[r[3]] = r[4]
            if r[1] and r[0] != 'SKY':
                names[r[0]] = str(r[1])
    sky = []   # every scoring SKY block cell
    for sh, c in SKY_SHEETS:
        if sh not in wb.sheetnames:
            continue
        for r in wb[sh].iter_rows(values_only=True):
            if not r or r[0] != 'SKY' or not isinstance(r[2], (int, float)) or '→ S ' not in str(r[1]):
                continue
            pt = r[1].split('→ S ')[1]
            for pl, o in (('RA', 2), ('Dec', 11)):
                sc = r[o + 5]
                if isinstance(sc, (int, float)):
                    e = best(r[o], pl)
                    sky.append(dict(centre=c, point=pt, plane=pl, value=float(r[o]), plus5=r[o + 1],
                                    target=e['target'], family=e['family'], score=float(sc),
                                    arrow=r[o + 6], timing=str(r[o + 8] or '')))
    mids, match = {}, defaultdict(list)
    for sh in wb.sheetnames:
        if not re.match(r'^P\d+$', sh):
            continue
        rows = list(wb[sh].iter_rows(values_only=True))
        cols = None
        for r in rows:
            if not r:
                continue
            if r[0] == 'table' and r[1] == 'star' and 'RA midpoints' in r:
                cols = (list(r).index('RA midpoints'), list(r).index('Dec midpoints'))
                continue
            if r[0] == 'T24' and cols and isinstance(r[1], str) and r[1][:2] in ('H ', 'J ') and '→' not in r[1]:
                for pl, ci in (('RA', cols[0]), ('Dec', cols[1])):
                    if ci < len(r) and r[ci]:
                        mids[(sh, r[1][0], r[1][2:], pl)] = str(r[ci])
            if r[0] in ('MATCH HORSE', 'MATCH JOCKEY') and r[1] in ('EXACT', 'BODY', 'CONJ STAR'):
                vals = [x for x in r if x not in (None, '')]
                skyc = [v for v in vals if isinstance(v, str) and v.startswith('S ') and ' → S ' in v]
                if not skyc:
                    continue
                i = vals.index(skyc[0])
                c, p = skyc[0][2:].split(' → S ')
                pl = vals[i + 1]
                t = vals[i + 6:]
                if len(t) >= 7:
                    match[sh].append(dict(chart='H' if r[0] == 'MATCH HORSE' else 'J', kind=r[1], centre=c, point=p,
                                          plane=pl, sky_value=vals[i + 2], t24_row=t[0], body=t[1], t24_plane=t[2],
                                          value=t[3], family=t[4], target=t[5], score=t[6]))
    return P, kinds, names, sky, mids, match


# ---------------------------------------------------------------- read
def read(path):
    P, kinds, names, sky, mids, match = load(path)
    S = lambda x: P.get(('SKY', 'S', x))
    runners = sorted({k[0] for k in P if k[0] != 'SKY'}, key=lambda s: int(s[1:]))
    bodies = [k[2] for k in P if k[0] == runners[0] and k[1] == 'H' and kinds.get(k[2]) == 'body' and k[2] != 'Moon']

    def noted(l):
        return ((l['score'] >= NOTE_MIN and mins(l['timing']) <= NOTE_WIN)
                or (l['score'] >= NOTE_APPLY and 'applying' in l['timing'])
                or (l['family'] == 'conj' and l['score'] >= CONJ_MIN))
    lines = [l for l in sky if noted(l)]
    pts_by_centre = defaultdict(set)
    for l in lines:
        pts_by_centre[l['point']].add(l['centre'])
    hubs = sorted(p for p, cs in pts_by_centre.items() if len(cs) >= 2)
    noted_stars = sorted({l['point'] for l in lines if kinds.get(l['point']) == 'star'})
    noted_points = sorted({l['point'] for l in lines})
    noted_cells = {(l['centre'], l['point'], l['plane']) for l in lines}
    star_centre = {s: [c for c in CENTRES if c in pts_by_centre[s]] for s in noted_stars}
    numbers = {(l['family'], l['target']): f"S {l['centre']} → {l['point']} {l['plane']} {l['value']:.4f} {tf(l)}"
               for l in lines if l['family'] != 'conj'}
    atoff = [l for l in lines if mins(l['timing']) <= 5 and l['family'] != 'conj']
    top = max(atoff, key=lambda l: l['score']) if atoff else None
    conj_pts = [l for l in lines if l['family'] == 'conj']
    strong_stars = sorted({l['point'] for l in lines if l['score'] >= 90 and kinds.get(l['point']) == 'star'})
    regulus = [l for l in sky if l['point'] == 'Regulus']

    pieces = []   # every collected cell

    def add(R, layer, chart, source, body, pl, v, e, note=''):
        pieces.append(dict(runner=R, layer=layer, chart=chart, source=source, body=body, plane=pl, value=round(v, 6),
                           target=e['target'] if e else '', family=e['family'] if e else '',
                           score=round(e['score'], 2) if e else None,
                           sky_number=numbers.get((e['family'], e['target'])) if e else None,
                           circle=circle(e['target'], e['family']) if e else '', note=note))

    for R in runners:
        for ch in 'HJ':
            nat = lambda x: P.get((R, ch, x))
            # 1 same body
            for X in bodies:
                if S(X) is None or nat(X) is None:
                    continue
                for pl in ('RA', 'Dec'):
                    v = dist(S(X), nat(X), pl)
                    lc = loose(v, pl)
                    if lc:
                        e = best(v, pl)
                        e4 = e if (e and e['family'] != 'conj' and e['target'] == lc[0]) else None
                        pieces.append(dict(runner=R, layer='same body', chart=ch, source=f'S {X}', body=X, plane=pl,
                                           value=round(v, 6), target=lc[0], family=lc[1],
                                           score=round(e4['score'], 2) if e4 else None,
                                           sky_number=numbers.get((lc[1], lc[0])), circle=circle(lc[0], lc[1]),
                                           note='4-digit' if e4 else 'loose'))
            # 6 T1 / T2
            J = nat('Jupiter')
            for X in bodies + noted_stars:
                if X == 'Jupiter' or nat(X) is None:
                    continue
                for pl in ('RA', 'Dec'):
                    v = dist(J, nat(X), pl)
                    e = best(v, pl)
                    if e and e['score'] >= CELL_MIN and (X in noted_points or (e['family'], e['target']) in numbers
                                                         or e['family'] == 'conj'):
                        add(R, 'T1' if ch == 'H' else 'T2', ch, f'{ch} Jupiter', X if X in bodies else f'star {X}', pl, v, e)
            # 7 top rows
            for c in CENTRES:
                for X in bodies:
                    for pl in ('RA', 'Dec'):
                        v = dist(S(c), nat(X), pl)
                        e = best(v, pl)
                        if e and (e['score'] >= CELL_MIN or (e['family'] == 'conj' and e['score'] >= CONJ_LIST)):
                            add(R, 'top rows', ch, f'S {c}', X, pl, v, e)
            for X in bodies:   # the whole 'S body → natal Jupiter' row (bodies only, as on the sheet)
                if X in CENTRES or S(X) is None:
                    continue
                for pl in ('RA', 'Dec'):
                    v = dist(S(X), J, pl)
                    e = best(v, pl)
                    if e and (e['score'] >= CELL_MIN or (e['family'] == 'conj' and e['score'] >= CONJ_LIST)):
                        add(R, 'top rows', ch, f'S {X}', 'Jupiter', pl, v, e)
            # 8 star rows
            for st in noted_stars:
                if S(st) is not None:   # the sky star onto natal Jupiter, read beside the natal star's row
                    for pl in ('RA', 'Dec'):
                        v = dist(S(st), J, pl)
                        e = best(v, pl)
                        if e and (e['score'] > STAR_HI or e['family'] == 'conj'):
                            add(R, 'star rows', ch, f'S {st}', 'Jupiter', pl, v, e)
                if nat(st) is None:
                    continue
                for X in bodies:
                    for pl in ('RA', 'Dec'):
                        v = dist(nat(st), nat(X), pl)
                        e = best(v, pl)
                        if not e:
                            continue
                        if ((e['family'] == 'conj' and e['score'] >= CONJ_LIST) or e['score'] > STAR_HI
                                or (e['score'] >= CELL_MIN and (e['family'], e['target']) in numbers)
                                or (X in CENTRES and e['score'] >= CELL_MIN)):
                            add(R, 'star rows', ch, f'{ch} {st}', X, pl, v, e)

    # ------------------------------------------------ one fixed star on one natal body counts once (Eddie, 7 Nov 2026)
    # A star barely moves between birth and race day, so the natal copy (H / J star) and the sky copy (S star) of a
    # star onto the same natal body are one connection: one line, the best-scoring copy, the other copies beside it.
    grp, order = {}, []
    for p in pieces:
        if p['layer'] != 'star rows':
            order.append(p)
            continue
        k = (p['runner'], p['chart'], p['body'], p['plane'], p['source'][2:])
        if k not in grp:
            grp[k] = [p]
            order.append(k)
        else:
            grp[k].append(p)
    pieces = []
    for x in order:
        if isinstance(x, dict):
            pieces.append(x)
            continue
        g = sorted(grp[x], key=lambda q: -(q['score'] or 0))
        keep = dict(g[0])
        keep['star'] = x[4]
        keep['copies'] = [dict(source=q['source'], value=q['value'], target=q['target'], family=q['family'], score=q['score'])
                          for q in g[1:]]
        pieces.append(keep)

    # ------------------------------------------------ field flags
    def key(p):
        src = p['star'] if p.get('star') else p['source'][2:] if p['source'][:2] in ('H ', 'J ') else p['source']
        return (p['layer'] if p['layer'] not in ('T1', 'T2') else 'T1/T2', src, p['body'], p['plane'], p['family'], p['target'])
    short = {r: names.get(r, r).split(' / ')[0] for r in runners}
    holders = defaultdict(set)
    for p in pieces:
        holders[key(p)].add(p['runner'])
    for p in pieces:
        others = sorted(holders[key(p)] - {p['runner']})
        p['field'] = 'only' if not others else 'also: ' + ', '.join(short.get(o, o) for o in others)

    # ------------------------------------------------ flags (named shapes found so far)
    flags = defaultdict(list)
    for R in runners:
        nat = lambda ch, x: P.get((R, ch, x))
        for ch in 'HJ':
            J = nat(ch, 'Jupiter')
            # natal body in conj with the star of a strong line (>= 90)
            for st in strong_stars:
                if nat(ch, st) is None:
                    continue
                for X in bodies:
                    for pl in ('RA', 'Dec'):
                        x = dist(nat(ch, st), nat(ch, X), pl)
                        e = best(x, pl)
                        if e and e['family'] == 'conj' and e['score'] >= CELL_MIN:
                            flags['natal body on a strong line star'].append(
                                dict(runner=R, text=cell(f"{ch} {st} → {ch} {X}", pl, x, e), score=e['score']))
            # centre in conj with natal Jupiter
            for c in CENTRES:
                for pl in ('RA', 'Dec'):
                    x = dist(S(c), J, pl)
                    e = best(x, pl)
                    if e and e['family'] == 'conj' and e['score'] >= CONJ_LIST:
                        flags['sky centre conj natal Jupiter'].append(dict(runner=R, text=cell(f"S {c} → {ch} Jupiter", pl, x, e), score=e['score']))
            # same-body Jupiter scoring >= 50 (4-digit)
            for pl in ('RA', 'Dec'):
                x = dist(S('Jupiter'), J, pl)
                e = best(x, pl)
                if e and e['family'] != 'conj' and e['score'] >= CELL_MIN:
                    flags['same-body Jupiter >= 50'].append(dict(runner=R, text=cell(f"S Jupiter → {ch} Jupiter", pl, x, e), score=e['score']))
            # hub point onto natal Jupiter
            for h in hubs:
                if S(h) is None or h in CENTRES:
                    continue
                for pl in ('RA', 'Dec'):
                    x = dist(S(h), J, pl)
                    e = best(x, pl)
                    if e and e['score'] >= CELL_MIN:
                        flags['hub point onto natal Jupiter'].append(dict(runner=R, text=cell(f"S {h} → {ch} Jupiter", pl, x, e), score=e['score']))
            # hub landing: natal body conj a hub star with the line landing; or a hub body conj a noted star
            for h in hubs:
                if kinds.get(h) == 'star' and nat(ch, h) is not None:
                    for X in bodies:
                        for l in lines:
                            if l['point'] != h:
                                continue
                            pl = l['plane']
                            x = dist(nat(ch, h), nat(ch, X), pl)
                            e = best(x, pl)
                            if e and e['family'] == 'conj' and e['score'] >= CELL_MIN:
                                y = dist(S(l['centre']), nat(ch, X), pl)
                                if abs(y - l['value']) < 0.05:
                                    flags['hub landing'].append(dict(runner=R, text=cell(f"{ch} {h} → {ch} {X}", pl, x, e) + f" | S {l['centre']} → {ch} {X} {pl} {y:.4f} on the line S {l['centre']} → {h} {l['value']:.4f} {tf(l)}", score=e['score']))
                elif kinds.get(h) == 'body' and nat(ch, h) is not None:
                    for st in noted_stars:
                        if nat(ch, st) is None:
                            continue
                        for pl in ('RA', 'Dec'):
                            x = dist(nat(ch, st), nat(ch, h), pl)
                            e = best(x, pl)
                            if e and e['family'] == 'conj' and e['score'] >= CELL_MIN:
                                flags['hub landing'].append(dict(runner=R, text=cell(f"hub body {ch} {h} → {ch} {st}", pl, x, e), score=e['score']))
            # a centre's conj star landing with the centre on the same natal body
            for l in conj_pts:
                st, c = l['point'], l['centre']
                if kinds.get(st) != 'star' or nat(ch, st) is None:
                    continue
                for X in bodies:
                    for pl in ('RA', 'Dec'):
                        x, y = dist(nat(ch, st), nat(ch, X), pl), dist(S(c), nat(ch, X), pl)
                        if x < lim(pl) and y < lim(pl):
                            e1, e2 = best(x, pl), best(y, pl)
                            if e1 and e2 and e1['score'] >= CELL_MIN and e2['score'] >= CELL_MIN:
                                flags['centre conj star landing with the centre'].append(
                                    dict(runner=R, text=cell(f"{ch} {st} → {ch} {X}", pl, x, e1) + ' | ' + cell(f"S {c} → {ch} {X}", pl, y, e2), score=min(e1['score'], e2['score'])))
            # top-line number on natal Jupiter
            if top:
                for k, v in P.items():
                    if k[2] == 'Jupiter' or (k[0] != 'SKY' and (k[0] != R or k[1] != ch)):
                        continue
                    for pl in ('RA', 'Dec'):
                        x = dist(v, J, pl)
                        e = best(x, pl)
                        if e and e['score'] >= CELL_MIN and e['target'] == top['target'] and e['family'] == top['family']:
                            flags['top-line number on natal Jupiter'].append(dict(runner=R, text=cell(f"{'S' if k[0] == 'SKY' else ch} {k[2]} → {ch} Jupiter", pl, x, e) + f" | top line S {top['centre']} → {top['point']} {top['plane']} {top['value']:.4f} {tf(top)}", score=e['score']))
        # N and N×φ on one Jupiter
        for ch in 'HJ':
            J = nat(ch, 'Jupiter')
            ws, gs = defaultdict(list), defaultdict(list)
            for k, v in P.items():
                if k[2] == 'Jupiter' or (k[0] != 'SKY' and (k[0] != R or k[1] != ch)):
                    continue
                for pl in ('RA', 'Dec'):
                    x = dist(v, J, pl)
                    e = best(x, pl)
                    if e and e['score'] >= CELL_MIN:
                        lab = cell(f"{'S' if k[0] == 'SKY' else ch} {k[2]} → {ch} Jupiter", pl, x, e)
                        if e['family'] == 'whole':
                            ws[e['target']].append(lab)
                        g = golden_mult(e['target'])
                        if g:
                            gs[str(g)].append(lab)
            for n in sorted(set(ws) & set(gs), key=int):
                flags['N and N×φ on one Jupiter'].append(dict(runner=R, text=f"{ws[n][0]} | {gs[n][0]}", score=None))

    # cross-chart: same source on the same body on both charts, same number on the same body on both charts
    for R in runners:
        mine = [p for p in pieces if p['runner'] == R and p['score'] is not None and p['score'] >= CELL_MIN]
        src = lambda p: p['star'] if p.get('star') else p['source'][2:] if p['source'][:2] in ('H ', 'J ') else p['source']
        for b in sorted({p['body'] for p in mine}):
            H = [p for p in mine if p['body'] == b and p['chart'] == 'H']
            Jc = [p for p in mine if p['body'] == b and p['chart'] == 'J']
            for s in sorted({src(p) for p in H} & {src(p) for p in Jc}):
                cs = [p for p in H + Jc if src(p) == s]
                flags['same source on the same body, both charts'].append(dict(runner=R, text=' | '.join(fmt_cell(p) for p in cs), score=None))
            for f, t in sorted({(p['family'], p['target']) for p in H if p['family'] != 'conj'} & {(p['family'], p['target']) for p in Jc if p['family'] != 'conj'}):
                cs = [p for p in H + Jc if (p['family'], p['target']) == (f, t)]
                flags['same number on the same body, both charts'].append(dict(runner=R, text=' | '.join(fmt_cell(p) for p in cs), score=None))
        for p in mine:
            if p['layer'] == 'star rows' and p['family'] != 'conj' and p['sky_number']:
                flags['line star carries a sky number'].append(dict(runner=R, text=fmt_cell(p) + f" = {p['sky_number']}", score=p['score']))

    # threads (Part 2F): >= 4 cells on one body, both charts, >= 2 layers
    threads = defaultdict(list)
    for R in runners:
        mine = [p for p in pieces if p['runner'] == R and (p['score'] or 0) >= CELL_MIN or (p['runner'] == R and p['layer'] == 'same body')]
        mine.sort(key=lambda p: -(p['score'] or 0))   # the best cell of a repeated star / cell is the one kept
        byb, seen = defaultdict(list), set()
        for p in mine:   # a cell found by two layers (e.g. S Sun → H Sun: same body and top row) counts once; a star once per body
            k = (('star', p['star']) if p.get('star') else (p['source'], p['plane']), p['chart'], p['body'])   # a star once per body
            if k not in seen:
                seen.add(k)
                byb[p['body']].append(p)
        for b, v in byb.items():
            ch = {p['chart'] for p in v}
            lay = {p['layer'] if p['layer'] not in ('T1', 'T2') else 'T1/T2' for p in v}
            if len(v) >= 4 and ch == {'H', 'J'} and len(lay) >= 2:
                threads[R].append(dict(body=b, cells=len(v), H=sum(p['chart'] == 'H' for p in v),
                                       J=sum(p['chart'] == 'J' for p in v), layers=sorted(lay),
                                       detail=[f"{p['layer']}: {fmt_piece(p)}" for p in
                                               sorted(v, key=lambda p: (LAYERS.index(p['layer']), p['chart'], -(p['score'] or 0)))]))
        threads[R].sort(key=lambda t: -t['cells'])

    # field counts per flag
    flag_holders = {k: sorted({x['runner'] for x in v}) for k, v in flags.items()}
    return dict(workbook=os.path.basename(path), runners=runners, names=names, lines=lines, hubs=hubs,
                noted_stars=noted_stars, star_centre=star_centre, strong_stars=strong_stars, top=top,
                conj_points=conj_pts, regulus=regulus, numbers=sorted(numbers.values()), pieces=pieces,
                mids={f'{k[0]}|{k[1]}|{k[2]}|{k[3]}': v for k, v in mids.items() if k[2] in noted_stars},
                match={k: [m for m in v if (m['centre'], m['point'], m['plane']) in noted_cells] for k, v in match.items()},
                flags=flags, flag_holders=flag_holders, threads=threads)


# ---------------------------------------------------------------- report
LAYERS = ['same body', 'T1', 'T2', 'top rows', 'star rows']


def fmt_cell(p):
    """source → chart body, plane, value, target, family, score."""
    s = f"{p['source']} → {p['chart']} {p['body']} {p['plane']} {p['value']:.4f} "
    if p['family'] == 'conj':
        return s + f"conj ({p['score']:.2f})"
    return s + f"{p['target']} {p['family']}" + (f" ({p['score']:.2f})" if p['score'] is not None else ' (loose)')


def fmt_piece(p):
    s = fmt_cell(p)
    for q in p.get('copies', []):
        s += f" [same star: {q['source']} {q['value']:.4f} " + (f"conj ({q['score']:.2f})]" if q['family'] == 'conj' else f"{q['target']} {q['family']} ({q['score']:.2f})]")
    if p['circle']:
        s += f" [{p['circle']}]"
    if p['sky_number']:
        s += f" [sky number: {p['sky_number']}]"
    s += f" — {p['field']}"
    return s


def report(D):
    out = []
    w = out.append
    nm = D['names']
    w(f"# Eddie's race read (stage 1): {D['workbook']}")
    w('Collected by tools/eddie_read.py. No lead, no ranking. Every piece says whether it is held by this runner only.')
    w('')
    w('## Sky notes')
    reg = [l for l in D['regulus']]
    w('- Regulus: ' + ('; '.join(f"S {l['centre']} → Regulus {l['plane']} {l['value']:.4f} {l['target']} ({l['score']:.2f}) {l['timing']}" for l in reg) if reg else 'no Regulus line'))
    for c in CENTRES:
        w(f'### Sky {c}')
        for l in sorted([l for l in D['lines'] if l['centre'] == c], key=lambda l: -l['score']):
            w(f"- {l['point']} {l['plane']} {l['value']:.6f} {tf(l)} {l['arrow'] or ''} — {l['timing']}"
              + (f" [{circle(l['target'], l['family'])}]" if circle(l['target'], l['family']) else ''))
    w(f"- **Hubs** (a point two centres reach): {', '.join(f'{h} ({' + '.join(D['star_centre'].get(h, []) or sorted({l['centre'] for l in D['lines'] if l['point'] == h}))})' for h in D['hubs']) or 'none'}")
    t = D['top']
    w(f"- **Top line** (highest, exact within 5 min of the off): " + (f"S {t['centre']} → {t['point']} {t['plane']} {t['value']:.6f} {t['target']} ({t['score']:.2f})" if t else 'none'))
    w(f"- **Conj points**: " + ('; '.join(f"S {l['centre']} conj {l['point']} {l['plane']} {l['value']:.4f} ({l['score']:.2f}) {l['timing']}" for l in D['conj_points']) or 'none'))
    w(f"- **Noted stars**: " + ', '.join(f"{s} ({'/'.join(D['star_centre'][s])})" for s in D['noted_stars']))
    w(f"- **Strong line stars** (>= 90): " + (', '.join(D['strong_stars']) or 'none'))
    w('')
    w('## Flags (shapes found so far; field-checked; no ranking)')
    for k in sorted(D['flags']):
        w(f"### {k} — held by {len(D['flag_holders'][k])} of {len(D['runners'])}: {', '.join(nm[r] for r in D['flag_holders'][k])}")
        for x in sorted(D['flags'][k], key=lambda x: -(x['score'] or 0)):
            w(f"- {nm[x['runner']]}: {x['text']}")
    w('')
    for R in D['runners']:
        w(f"## {nm[R]}")
        mine = [p for p in D['pieces'] if p['runner'] == R]
        for lay, title in (('same body', '1. Same body'), (None, '5. MATCH'), ('T1', '6. T1 (horse Jupiter)'), ('T2', '6. T2 (jockey Jupiter)'),
                           ('top rows', '7. T24 top rows'), ('star rows', '8. T24 star rows')):
            w(f"### {title}")
            if lay is None:
                ms = D['match'].get(R, [])
                if not ms:
                    w('- no MATCH rows for the noted sky cells')
                for m in ms:
                    w(f"- {m['chart']} {m['kind']}: S {m['centre']} → {m['point']} {m['plane']} {m['sky_value']} | {m['t24_row']} {m['body']} {m['t24_plane']} {m['value']} {m['target']} {m['family']} ({m['score']})")
                continue
            ps = [p for p in mine if p['layer'] == lay]
            if lay == 'star rows':
                for c in CENTRES:
                    for st in [s for s in D['noted_stars'] if D['star_centre'][s][0] == c]:
                        rows = [p for p in ps if p['source'][2:] == st]
                        mids = [f"{ch} {pl} midpoints: {D['mids'][f'{R}|{ch}|{st}|{pl}']}" for ch in 'HJ' for pl in ('RA', 'Dec') if f'{R}|{ch}|{st}|{pl}' in D['mids']]
                        if rows or mids:
                            w(f"- **{st}** (sky {' + '.join(D['star_centre'][st])})")
                            for p in sorted(rows, key=lambda p: (p['chart'], -(p['score'] or 0))):
                                w(f"  - {fmt_piece(p)}")
                            for m in mids:
                                w(f"  - {m}")
                continue
            if not ps:
                w('- none')
            if lay == 'top rows':   # Jupiter, Sun, Moon, then S body → natal Jupiter; horse, jockey; score
                order = lambda p: ((CENTRES.index(p['source'][2:]) if p['source'][2:] in CENTRES else 3), p['chart'], -(p['score'] or 0))
            else:
                order = lambda p: (p['chart'], -(p['score'] or 0))
            for p in sorted(ps, key=order):
                w(f"- {fmt_piece(p)}")
        th = D['threads'].get(R, [])
        w('### Threads (4 or more cells on one body, both charts, 2 or more layers)')
        if not th:
            w('- none')
        for t in th:
            w(f"- **{t['body']}**: {t['cells']} cells (H {t['H']}, J {t['J']}; {', '.join(t['layers'])})")
            for d in t['detail']:
                w(f"  - {d}")
        mf = sorted(k for k, v in D['flag_holders'].items() if R in v)
        w('### Flags held')
        if not mf:
            w('- none')
        for k in mf:
            n = len(D['flag_holders'][k])
            w(f"- **{k}** ({'only this runner' if n == 1 else f'{n} of {len(D["runners"])} runners'})")
            for x in sorted([x for x in D['flags'][k] if x['runner'] == R], key=lambda x: -(x['score'] or 0)):
                w(f"  - {x['text']}")
        w('')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('workbook')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    D = read(a.workbook)
    out = a.out or os.path.dirname(os.path.abspath(a.workbook))
    os.makedirs(out, exist_ok=True)
    base = os.path.basename(a.workbook).replace('_jupiter_tables.xlsx', '').replace('.xlsx', '')
    md = os.path.join(out, f'{base}_eddie_read.md')
    js = os.path.join(out, f'{base}_eddie_read.json')
    with open(md, 'w') as f:
        f.write(report(D))
    with open(js, 'w') as f:
        json.dump(D, f, ensure_ascii=False, indent=1, default=str)
    print(md)
    print(js)


if __name__ == '__main__':
    main()
