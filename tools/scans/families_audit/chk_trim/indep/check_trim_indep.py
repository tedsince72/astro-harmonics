#!/usr/bin/env python3
"""Independent checker (29 Oct 2026) for the jupiter_tables trim.

Usage: check_trim_indep.py <old_def.xlsx> <old_full.xlsx> <new_def.xlsx> <new_full.xlsx> [new_folder]
Compares the AFTER workbooks with the BEFORE ones (own code; nothing from chk_trim/ or tools/).
Prints counts per part and every mismatch; exit code 1 if any mismatch.
"""
import math
import os
import re
import sys

import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string

KEPT = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T24 HORSE', 'T24 JOCKEY']
LABELS_H = ['S Jupiter → S body', 'H Jupiter → H body', 'S Jupiter → H body', 'S body → H Jupiter']
GREEN, YELLOW, LIGHT, RED, GREY = 'C6EFCE', 'FFEB9C', 'FFF8DC', 'FF8080', 'D9D9D9'

MIS = []
INFO = []
COUNT = {}


def bad(part, msg):
    MIS.append((part, msg))


def cnt(part, n=1):
    COUNT[part] = COUNT.get(part, 0) + n


def col_rgb(c):
    if c is None:
        return None
    if c.type == 'rgb':
        return c.rgb
    if c.type == 'theme':
        return ('theme', c.theme, c.tint)
    if c.type == 'indexed':
        return ('idx', c.indexed)
    return (c.type, c.value)


def sig(c):
    """Everything about a cell that matters for display."""
    f, fo, b, a = c.fill, c.font, c.border, c.alignment
    return (
        c.value,
        c.number_format,
        (f.fill_type, col_rgb(f.fgColor) if f.fill_type else None, col_rgb(f.bgColor) if f.fill_type else None),
        (fo.b, fo.i, fo.u, fo.sz, fo.name, col_rgb(fo.color)),
        tuple(((s.style, col_rgb(s.color) if s.style else None) if s is not None else (None, None)) for s in (b.left, b.right, b.top, b.bottom)),
        (a.horizontal, a.vertical, a.wrap_text),
        c.comment.text if c.comment else None,
    )


SIGNAMES = ['value', 'numfmt', 'fill', 'font', 'border', 'align', 'comment']


def diff_sig(s1, s2):
    return [SIGNAMES[i] for i in range(len(s1)) if s1[i] != s2[i]]


def row_empty(ws, r, maxc):
    for c in range(1, maxc + 1):
        cell = ws.cell(r, c)
        if cell.value is not None or cell.comment is not None or cell.fill.fill_type:
            return False
        b = cell.border
        if any(s is not None and s.style for s in (b.left, b.right, b.top, b.bottom)):
            return False
    return True


def widths(ws):
    w = {}
    for key, d in ws.column_dimensions.items():
        lo = d.min or column_index_from_string(key)
        hi = d.max or lo
        for i in range(lo, hi + 1):
            w[i] = d.width if d.customWidth or d.width else None
    return w


def maxcol(*wss):
    return max(ws.max_column for ws in wss)


# ---------------------------------------------------------------- table finding (own)
def table_starts(ws):
    """Rows where a table starts: column A non-empty, previous row empty, key differs from the running key."""
    starts = []
    prev_key = None
    mc = ws.max_column
    for r in range(4, ws.max_row + 1):
        a = ws.cell(r, 1).value
        if a is None:
            continue
        if not row_empty(ws, r - 1, mc):
            continue
        b = ws.cell(r, 2).value
        b = b if isinstance(b, str) else ''
        if a == 'T24':
            key = 'T24 HORSE' if b.startswith('T24 HORSE') else 'T24 JOCKEY' if b.startswith('T24 JOCKEY') else 'T24 ?'
        else:
            key = str(a).split(' AREA')[0]
        if key != prev_key:
            starts.append((r, key))
            prev_key = key
    return starts


def regions(ws):
    st = table_starts(ws)
    out = {}
    order = []
    for i, (r, k) in enumerate(st):
        e = st[i + 1][0] - 1 if i + 1 < len(st) else ws.max_row
        while e > r and row_empty(ws, e, ws.max_column):
            e -= 1
        if k in out:
            bad('a', f'{ws.title}: table {k} found twice ({out[k][0]}, {r})')
        out[k] = (r, e)
        order.append(k)
    return out, order


# ---------------------------------------------------------------- whole-sheet compare
def compare_sheet(part, ws1, ws2):
    mr = max(ws1.max_row, ws2.max_row)
    mc = maxcol(ws1, ws2)
    for r in range(1, mr + 1):
        for c in range(1, mc + 1):
            s1, s2 = sig(ws1.cell(r, c)), sig(ws2.cell(r, c))
            cnt(part)
            if s1 != s2:
                bad(part, f'{ws2.title}!{get_column_letter(c)}{r}: {diff_sig(s1, s2)} {s1[0]!r} -> {s2[0]!r}')
    m1 = sorted(str(m) for m in ws1.merged_cells.ranges)
    m2 = sorted(str(m) for m in ws2.merged_cells.ranges)
    if m1 != m2:
        bad(part, f'{ws2.title}: merged ranges differ {set(m1) ^ set(m2)}')
    w1, w2 = widths(ws1), widths(ws2)
    for c in range(1, mc + 1):
        cnt(part + ' widths')
        if w1.get(c) != w2.get(c):
            bad(part, f'{ws2.title}: width {get_column_letter(c)} {w1.get(c)} -> {w2.get(c)}')
    if ws1.freeze_panes != ws2.freeze_panes:
        bad(part, f'{ws2.title}: freeze {ws1.freeze_panes} -> {ws2.freeze_panes}')
    h1 = {k: v.height for k, v in ws1.row_dimensions.items() if v.height}
    h2 = {k: v.height for k, v in ws2.row_dimensions.items() if v.height}
    if h1 != h2:
        bad(part, f'{ws2.title}: row heights differ')


# ---------------------------------------------------------------- positions
def positions(ws):
    pos = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[2] in ('S', 'H', 'J') and row[3] is not None and isinstance(row[5], (int, float)):
            pos[(row[0], row[2], row[3])] = (row[5], row[6])
    return pos


def d_ra(a, b):
    x = abs(a - b) % 360.0
    return 360.0 - x if x > 180.0 else x


def score_of(comment):
    if comment is None:
        return None
    first = comment.split('\n')[0]
    if first.startswith('nearest:'):
        return None
    try:
        return float(first.split(' · ')[-1])
    except ValueError:
        return 'unparsed'


def expect_fill(v, plane, comment):
    if (plane == 'RA' and v < 1.5) or (plane == 'Dec' and v < 0.3):
        return RED
    s = score_of(comment)
    if s is None:
        return None
    if s == 'unparsed':
        return 'unparsed'
    return GREEN if s >= 80 else YELLOW if s >= 50 else LIGHT


def fill_rgb(cell):
    if not cell.fill.fill_type:
        return None
    rgb = cell.fill.fgColor.rgb
    return rgb[-6:] if isinstance(rgb, str) else rgb


# ---------------------------------------------------------------- runner sheet
def check_runner(name, wo, wn, pos):
    ncol = wn.max_column  # columns the after sheet uses (read before any cell access creates cells)
    reg_o, _ = regions(wo)
    reg_n, order_n = regions(wn)
    # (a) table list
    if order_n != KEPT:
        bad('a', f'{name}: after tables {order_n}')
    for k in order_n:
        cnt('a tables')
    mcol = max(wo.max_column, wn.max_column)
    covered = set()
    # rows 1-3
    for r in (1, 2, 3):
        for c in range(1, mcol + 1):
            cnt('c cells')
            s1, s2 = sig(wo.cell(r, c)), sig(wn.cell(r, c))
            if s1 != s2:
                bad('c', f'{name}!{get_column_letter(c)}{r}: {diff_sig(s1, s2)}')
        covered.add(r)
    rowmap = {}  # new row -> old row
    five = {}
    for k in KEPT:
        if k not in reg_o or k not in reg_n:
            bad('c', f'{name}: table {k} missing old={k in reg_o} new={k in reg_n}')
            continue
        (os_, oe), (ns, ne) = reg_o[k], reg_n[k]
        extra = 5 if k.startswith('T24') else 0
        if (oe - os_) + extra != ne - ns:
            bad('c', f'{name}: {k} length old {oe - os_ + 1} new {ne - ns + 1} (extra {extra})')
        for i in range(oe - os_ + 1):
            nr = ns + (i if (extra == 0 or i < 3) else i + extra)
            rowmap[nr] = os_ + i
        if extra:
            five[k] = ns + 3
            for j in range(5):
                covered.add(ns + 3 + j)
    # (c) mapped rows cell for cell
    for nr, orow in rowmap.items():
        covered.add(nr)
        for c in range(1, mcol + 1):
            cnt('c cells')
            s1, s2 = sig(wo.cell(orow, c)), sig(wn.cell(nr, c))
            if s1 != s2:
                bad('c', f'{name}!{get_column_letter(c)}{nr} (old row {orow}): {diff_sig(s1, s2)} {s1[0]!r} -> {s2[0]!r}')
        ho = wo.row_dimensions[orow].height if orow in wo.row_dimensions else None
        hn = wn.row_dimensions[nr].height if nr in wn.row_dimensions else None
        if ho != hn:
            bad('c', f'{name}: row height old {orow} {ho} new {nr} {hn}')
    # every other after row empty
    for r in range(1, wn.max_row + 1):
        if r not in covered:
            cnt('c empty rows')
            if not row_empty(wn, r, mcol):
                bad('c', f'{name}: stray content in row {r}')
    # merged ranges
    inv = {}
    for nr, orow in rowmap.items():
        inv[orow] = nr
    exp = set()
    for m in wo.merged_cells.ranges:
        if m.min_row in inv and m.max_row in inv:
            r1, r2 = inv[m.min_row], inv[m.max_row]
            if r2 - r1 != m.max_row - m.min_row:
                bad('c', f'{name}: merged {m} spans the five-row gap')
            exp.add(f'{get_column_letter(m.min_col)}{r1}:{get_column_letter(m.max_col)}{r2}')
    got = set(str(m) for m in wn.merged_cells.ranges)
    cnt('c merges', len(got))
    if exp != got:
        bad('c', f'{name}: merged expected-only {sorted(exp - got)} after-only {sorted(got - exp)}')
    # widths / freeze
    w1, w2 = widths(wo), widths(wn)
    for c in range(1, ncol + 1):
        cnt('c widths')
        if w1.get(c) != w2.get(c):
            bad('c', f'{name}: width {get_column_letter(c)} {w1.get(c)} -> {w2.get(c)}')
    gone = [get_column_letter(c) for c in sorted(w1) if c > ncol and w1[c] is not None and w2.get(c) is None]
    extra = [get_column_letter(c) for c in sorted(w2) if c > ncol]
    if extra:
        bad('c', f'{name}: widths set beyond the used columns: {extra}')
    INFO.append(f'{name}: after uses columns A..{get_column_letter(ncol)}; before-only widths dropped beyond: '
                f'{gone[0] + ".." + gone[-1] if gone else "none"} ({len(gone)})')
    if wn.freeze_panes != 'C4' or wo.freeze_panes != wn.freeze_panes:
        bad('c', f'{name}: freeze {wo.freeze_panes} -> {wn.freeze_panes}')
    # (d) five rows
    for k in ('T24 HORSE', 'T24 JOCKEY'):
        if k in five:
            check_five(name, k, wo, wn, reg_o, reg_n, five[k], pos)


def find_old_ss(wo, k):
    """Rows of the before (SKY STARS) table: label -> row."""
    title = f'{k} (SKY STARS)'
    rows = {}
    for r in range(1, wo.max_row + 1):
        if wo.cell(r, 1).value == title and isinstance(wo.cell(r, 2).value, str):
            lab = wo.cell(r, 2).value
            if lab not in rows:
                rows[lab] = r
    return rows


def old_t9(wo, ch):
    for r in range(1, wo.max_row + 1):
        if wo.cell(r, 1).value == 'T9' and wo.cell(r, 2).value == f'S Jupiter – {ch} Jupiter':
            return wo.cell(r, 3).value, wo.cell(r, 11).value
    return None, None


def check_five(name, k, wo, wn, reg_o, reg_n, r0, pos):
    ch = 'H' if k == 'T24 HORSE' else 'J'
    ns = reg_n[k][0]
    hdr1, hdr2 = ns + 1, ns + 2
    labels = ['S Jupiter → S body', f'{ch} Jupiter → {ch} body', f'S Jupiter → {ch} body', f'S body → {ch} Jupiter']
    # columns from header row 2, plane from header row 1 (RA from C, Dec from the column holding 'Dec')
    dec_start = None
    rep_col = None
    for c in range(1, wn.max_column + 1):
        v = wn.cell(hdr1, c).value
        if v == 'Dec':
            dec_start = c
        if v == 'repeats':
            rep_col = c
    cols = []
    for c in range(3, rep_col):
        body = wn.cell(hdr2, c).value
        plane = 'Dec' if c >= dec_start else 'RA'
        cols.append((c, plane, body))
    old_rows = find_old_ss(wo, k)
    t9 = old_t9(wo, ch)
    pid = name
    SJ = pos[('SKY', 'S', 'Jupiter')]
    NJ = pos[(pid, ch, 'Jupiter')]
    for j, lab in enumerate(labels):
        r = r0 + j
        if wn.cell(r, 1).value != 'T24' or wn.cell(r, 2).value != lab:
            bad('d', f'{name} {k} row {r}: label {wn.cell(r, 1).value!r} {wn.cell(r, 2).value!r}, expected {lab!r}')
        orow = old_rows.get(lab)
        if orow is None:
            bad('d', f'{name} {k}: no before (SKY STARS) row {lab}')
        for c, plane, body in cols:
            cell = wn.cell(r, c)
            cnt('d five-row cells')
            # vs before (SKY STARS)
            if orow is not None:
                s1, s2 = sig(wo.cell(orow, c)), sig(cell)
                cnt('d vs before cells')
                if s1 != s2:
                    bad('d', f'{name}!{get_column_letter(c)}{r} {lab} {body} {plane}: vs before {diff_sig(s1, s2)} {s1[0]!r} -> {s2[0]!r}')
            # expected blank?
            if body in ('S Jupiter', None) or (isinstance(body, str) and 'middle' in body):
                if cell.value is not None or cell.comment is not None or cell.fill.fill_type:
                    bad('d', f'{name}!{get_column_letter(c)}{r} {lab}: {body} column should be blank, has {cell.value!r}')
                continue
            idx = 0 if plane == 'RA' else 1
            if body == 'Jupiter' and j < 2:
                if cell.value is not None or cell.comment is not None or cell.fill.fill_type:
                    bad('d', f'{name}!{get_column_letter(c)}{r} {lab} Jupiter: should be blank, has {cell.value!r}')
                continue
            if j == 0:
                a, b = SJ, pos[('SKY', 'S', body)]
            elif j == 1:
                a, b = NJ, pos[(pid, ch, body)]
            elif j == 2:
                a, b = SJ, pos[(pid, ch, body)]
            else:
                a, b = pos[('SKY', 'S', body)], NJ
            d = d_ra(a[0], b[0]) if idx == 0 else abs(a[1] - b[1])
            cnt('d recomputed')
            v = cell.value
            if not isinstance(v, (int, float)) or abs(v - round(d, 6)) > 1.5e-6 or abs(v - round(v, 6)) > 1e-12:
                bad('d', f'{name}!{get_column_letter(c)}{r} {lab} {body} {plane}: value {v!r}, own {d:.8f}')
            if cell.number_format != '0.000000':
                bad('d', f'{name}!{get_column_letter(c)}{r}: number format {cell.number_format}')
            com = cell.comment.text if cell.comment else None
            if com is None:
                bad('d', f'{name}!{get_column_letter(c)}{r}: no comment')
            elif 'repeat' in com or 'midpoint' in com:
                bad('d', f'{name}!{get_column_letter(c)}{r}: comment carries a repeat / midpoint line')
            b_ = cell.border
            if any(s is not None and s.style for s in (b_.left, b_.right, b_.top, b_.bottom)):
                bad('d', f'{name}!{get_column_letter(c)}{r}: has an outline')
            ef = expect_fill(v if isinstance(v, (int, float)) else 1e9, plane, com)
            cnt('d fills')
            if ef != fill_rgb(cell):
                bad('d', f'{name}!{get_column_letter(c)}{r} {lab} {body} {plane}: fill {fill_rgb(cell)} expected {ef} ({com})')
            if body == 'Jupiter' and j >= 2:
                cnt('d T9')
                ref = t9[idx]
                if ref is None or abs(v - ref) > 1e-9:
                    bad('d', f'{name}!{get_column_letter(c)}{r}: Jupiter {v} vs before T9 {ref}')
        # repeats column blank
        rc = wn.cell(r, rep_col)
        if rc.value is not None:
            bad('d', f'{name}!{get_column_letter(rep_col)}{r}: repeats not blank')
        for c in range(rep_col + 1, wn.max_column + 1):
            if wn.cell(r, c).value is not None:
                bad('d', f'{name}!{get_column_letter(c)}{r}: value beyond repeats')
    # stars row
    r = r0 + 4
    if wn.cell(r, 1).value != 'T24' or wn.cell(r, 2).value != 'stars':
        bad('d', f'{name} {k}: stars row {r} reads {wn.cell(r, 1).value!r} {wn.cell(r, 2).value!r}')
    for c in range(1, wn.max_column + 1):
        cell = wn.cell(r, c)
        cnt('d stars-row cells')
        want = GREY if c <= rep_col else None
        if fill_rgb(cell) != want:
            bad('d', f'{name}!{get_column_letter(c)}{r} stars row: fill {fill_rgb(cell)} expected {want}')
        if c > 2 and cell.value is not None:
            bad('d', f'{name}!{get_column_letter(c)}{r} stars row: value {cell.value!r}')
    # stars row vs before (SKY STARS) stars row, columns A..repeats except A value
    orow = old_rows.get('stars')
    if orow:
        for c in range(2, rep_col + 1):
            s1, s2 = sig(wo.cell(orow, c)), sig(wn.cell(r, c))
            cnt('d vs before cells')
            if s1 != s2:
                bad('d', f'{name}!{get_column_letter(c)}{r} stars row vs before {diff_sig(s1, s2)}')
    # title count: N = star rows, k = star rows with a repeats value
    title = wn.cell(ns, 2).value
    m = re.search(r'REPEATS \(22 Oct 2026\): (\d+) of (\d+) rows with a repeat', title or '')
    star_rows = []
    rr = r0 + 5
    while rr <= wn.max_row and wn.cell(rr, 1).value == 'T24':
        star_rows.append(rr)
        rr += 1
    nrep = sum(1 for x in star_rows if wn.cell(x, rep_col).value)
    cnt('d titles')
    if not m or int(m.group(2)) != len(star_rows) or int(m.group(1)) != nrep:
        bad('d', f'{name} {k}: title count {m.groups() if m else None}, star rows {len(star_rows)}, with repeat {nrep}')


# ---------------------------------------------------------------- main
def main():
    old_def, old_full, new_def, new_full = sys.argv[1:5]
    new_folder = sys.argv[5] if len(sys.argv) > 5 else None
    wo = openpyxl.load_workbook(old_def)
    wof = openpyxl.load_workbook(old_full)
    wn = openpyxl.load_workbook(new_def)
    wnf = openpyxl.load_workbook(new_full)
    runners = [s for s in wo.sheetnames if re.fullmatch(r'P\d\d', s)]
    # (a)
    exp_sheets = ['POSITIONS', 'SKY JUPITER'] + runners
    for w, lab in ((wn, 'default'), (wnf, '--full')):
        if w.sheetnames != exp_sheets:
            bad('a', f'{lab} sheets {w.sheetnames} expected {exp_sheets}')
        for s in runners:
            ws = w[s]
            allowed = {'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T24', 'table', None}
            for r in range(4, ws.max_row + 1):
                a = ws.cell(r, 1).value
                cnt('a column-A cells')
                if a not in allowed:
                    bad('a', f'{lab} {s}!A{r}: {a!r}')
            for row in ws.iter_rows(values_only=True):
                for v in row:
                    if isinstance(v, str) and ('(SKY STARS)' in v or 'TIMELINE' in v or 'RATIOS' in v):
                        bad('a', f'{lab} {s}: text from a removed table: {v[:60]!r}')
    if new_folder:
        pairs = [f for f in os.listdir(new_folder) if 'pairs' in f]
        if pairs:
            bad('a', f'pairs files in new folder: {pairs}')
    # (b)
    for s in ('POSITIONS', 'SKY JUPITER'):
        compare_sheet('b', wo[s], wn[s])
    # (c), (d)
    pos = positions(wn['POSITIONS'])
    for s in runners:
        check_runner(s, wo[s], wn[s], pos)
    # (e)
    for s in wn.sheetnames:
        if s in wnf.sheetnames:
            compare_sheet('e', wn[s], wnf[s])
    # --full before vs default before for kept sheets (sanity: the before builds agree on the kept sheets)
    for k in sorted(COUNT):
        print(f'{k}: {COUNT[k]}')
    for i in INFO:
        print('info:', i)
    print(f'mismatches: {len(MIS)}')
    for p, m in MIS[:200]:
        print(f'  [{p}] {m}')
    if len(MIS) > 200:
        print(f'  ... {len(MIS) - 200} more')
    return 1 if MIS else 0


if __name__ == '__main__':
    sys.exit(main())
