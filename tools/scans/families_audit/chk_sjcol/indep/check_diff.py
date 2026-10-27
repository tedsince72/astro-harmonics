#!/usr/bin/env python3
"""Independent checker (27 Oct 2026), part (e): BEFORE vs AFTER workbooks, every row of every sheet, after removing the inserted
S Jupiter columns (T24 HORSE / JOCKEY rows; (SKY STARS) rows incl. SCORES) and the inserted four rows + 'stars' separator.
usage: check_diff.py before.xlsx after.xlsx | --same a.xlsx b.xlsx (cell-by-cell identical, shared sheets) | --zip a b"""
import sys, collections, zipfile, re
import openpyxl
from openpyxl.utils import get_column_letter as L

NEW4 = ('S Jupiter → S body', 'H Jupiter → H body', 'S Jupiter → H body', 'S body → H Jupiter',
        'J Jupiter → J body', 'S Jupiter → J body', 'S body → J Jupiter', 'stars')

def rgb(c):
    f = c.fill
    if f is None or f.fill_type in (None, 'none'):
        return None
    return f.fgColor.rgb

def sig(c):
    b = c.border
    return (c.value, rgb(c), c.comment.text if c.comment else None, b.left.style, b.right.style, b.top.style, b.bottom.style,
            c.number_format, bool(c.font and c.font.b))

def row_kind(ws, r):
    a, b = ws.cell(r, 1).value, str(ws.cell(r, 2).value or '')
    if a in ('T24 HORSE (SKY STARS)', 'T24 JOCKEY (SKY STARS)'):
        return 'ss'
    return None

def classify(ws, after):
    """-> list of (row, kind) where kind in None / 't24' / 'ss'; t24 rows = title + 2 header rows + star rows of T24 HORSE / JOCKEY (natal)"""
    out = []; r = 1; mx = ws.max_row
    kinds = {}
    t24 = None
    for r in range(1, mx + 1):
        a, b = ws.cell(r, 1).value, str(ws.cell(r, 2).value or '')
        if a == 'T24' and (b.startswith('T24 HORSE (natal)') or b.startswith('T24 JOCKEY (natal)')):
            t24 = b[4]                      # 'H' / 'J'
            kinds[r] = 't24'; continue
        if a in ('T24 HORSE (SKY STARS)', 'T24 JOCKEY (SKY STARS)'):
            kinds[r] = 'ss'; t24 = None; continue
        if t24 and (a == 'table' or (a is None and ws.cell(r, 3).value is not None and r - 2 in kinds and kinds.get(r - 1) == 't24')):
            kinds[r] = 't24'; continue
        if t24 and a == 'T24' and (b.startswith('H ') or b.startswith('J ')):
            kinds[r] = 't24'; continue
        if t24 and a is None and kinds.get(r - 1) == 't24' and kinds.get(r - 2) == 't24' and ws.cell(r - 1, 1).value == 'table':
            kinds[r] = 't24'; continue
        if a not in ('T24', None, 'table'):
            t24 = None
        # SKY STARS header rows: 'table' row after an ss title, and the row after it
        if a == 'table' and kinds.get(r - 1) == 'ss':
            kinds[r] = 'ss'; continue
        if a is None and kinds.get(r - 1) == 'ss' and ws.cell(r - 1, 1).value == 'table':
            kinds[r] = 'ss'; continue
    return kinds

def inserted_cols(ws, r, kind, after):
    if not after or kind is None:
        return set()
    if kind == 't24':
        return {27, 53}
    return {28, 54, 81, 106}

def colmap(ws_after_maxcol, ins):
    m = {}; k = 0
    for c in range(1, ws_after_maxcol + 1):
        if c in ins:
            continue
        k += 1; m[k] = c
    return m

def rows_of(ws, after):
    kinds = classify(ws, after)
    rows = []
    for r in range(1, ws.max_row + 1):
        if after and kinds.get(r) == 'ss' and ws.cell(r, 2).value in NEW4:
            continue
        rows.append((r, kinds.get(r)))
    return rows, kinds

def cmp_sheet(wb0, wb1, name, rep):
    s0, s1 = wb0[name], wb1[name]
    r0, k0 = rows_of(s0, False)
    r1, k1 = rows_of(s1, True)
    if len(r0) != len(r1):
        rep['bad'].append(f'{name}: row count {len(r0)} vs {len(r1)} (after inserted rows removed)')
    mc = max(s0.max_column, s1.max_column) + 4
    for (a, ka), (b, kb) in zip(r0, r1):
        if ka != kb:
            rep['bad'].append(f'{name}: kind {a}:{ka} vs {b}:{kb}')
        ins = inserted_cols(s1, b, kb, True)
        cm = colmap(mc, ins)
        diffs = []
        for c in range(1, mc - len(ins) + 1):
            x, y = sig(s0.cell(a, c)), sig(s1.cell(b, cm[c]))
            if x != y:
                diffs.append((c, cm[c], x, y))
        rep['rows'] += 1; rep['cells'] += mc - len(ins)
        if kb:
            rep['rows_' + kb] += 1
        if diffs:
            title_only = all(d[0] == 2 and isinstance(d[2][0], str) and d[2][1:] == d[3][1:] for d in diffs)
            key = 'title' if title_only else 'other'
            rep['diff_' + key].append((name, a, b, diffs))
    # inserted rows count
    ins_rows = [r for r in range(1, s1.max_row + 1) if k1.get(r) == 'ss' and s1.cell(r, 2).value in NEW4]
    rep['inserted_rows'] += len(ins_rows)
    # merged ranges: map after ranges back
    def back(rng, ws, kinds, rows_after):
        idx = {b: i for i, (b, _) in enumerate(rows_after)}
        return rng
    m0 = sorted(str(m) for m in s0.merged_cells.ranges)
    rowmap = {b: a for (a, _), (b, _) in zip(r0, r1)}
    m1b = []
    for m in s1.merged_cells.ranges:
        if m.min_row not in rowmap:
            m1b.append(('INSERTED', str(m))); continue
        ins = inserted_cols(s1, m.min_row, k1.get(m.min_row), True)
        inv = {v: k for k, v in colmap(max(s1.max_column, s0.max_column) + 4, ins).items()}
        lo = m.min_col
        while lo in ins: lo += 1
        hi = m.max_col
        while hi in ins: hi -= 1
        m1b.append(f'{L(inv[lo])}{rowmap[m.min_row]}:{L(inv[hi])}{rowmap[m.max_row]}')
    m1b = sorted(m1b, key=str)
    if [x for x in m1b if not isinstance(x, tuple)] != m0:
        a = set(m0); b = set(x for x in m1b if not isinstance(x, tuple))
        rep['bad'].append(f'{name}: merged ranges differ: before only {sorted(a-b)[:10]} after only {sorted(b-a)[:10]}')
    rep['merged'] += len(m0)
    # widths
    for c in range(1, max(s0.max_column, s1.max_column) + 2):
        w0 = s0.column_dimensions[L(c)].width; w1 = s1.column_dimensions[L(c)].width
        if w0 != w1:
            rep['widths'].append(f'{name} {L(c)}: {w0} -> {w1}')

def main(p0, p1):
    wb0 = openpyxl.load_workbook(p0); wb1 = openpyxl.load_workbook(p1)
    rep = collections.defaultdict(int); rep['bad'] = []; rep['diff_title'] = []; rep['diff_other'] = []; rep['widths'] = []
    if wb0.sheetnames != wb1.sheetnames:
        rep['bad'].append(f'sheets {wb0.sheetnames} vs {wb1.sheetnames}')
    for n in wb0.sheetnames:
        cmp_sheet(wb0, wb1, n, rep)
    print('==', p0, '->', p1)
    for k in ('rows', 'cells', 'rows_t24', 'rows_ss', 'inserted_rows', 'merged'):
        print(f'  {k}: {rep[k]}')
    print('  title-only rows differing:', len(rep['diff_title']))
    for n, a, b, d in rep['diff_title'][:40]:
        print(f'    {n} r{a}->r{b}: {str(d[0][2][0])[-160:]!r}\n        -> {str(d[0][3][0])[-220:]!r}')
    print('  other rows differing:', len(rep['diff_other']))
    for n, a, b, d in rep['diff_other'][:30]:
        print(f'    {n} r{a}->r{b}: {[(L(x[0]), L(x[1]), x[2], x[3]) for x in d[:3]]}')
    print('  width changes:', len(rep['widths']))
    for w in rep['widths'][:40]:
        print('    ', w)
    print('  structural problems:', len(rep['bad']))
    for b in rep['bad'][:30]:
        print('    ', b)

def same(p0, p1, sheets=None):
    wb0 = openpyxl.load_workbook(p0); wb1 = openpyxl.load_workbook(p1)
    n = 0; bad = []
    for s in (sheets or [x for x in wb0.sheetnames if x in wb1.sheetnames]):
        a, b = wb0[s], wb1[s]
        if (a.max_row, a.max_column) != (b.max_row, b.max_column):
            bad.append(f'{s} size {a.max_row}x{a.max_column} vs {b.max_row}x{b.max_column}')
        for r in range(1, max(a.max_row, b.max_row) + 1):
            for c in range(1, max(a.max_column, b.max_column) + 1):
                n += 1
                if sig(a.cell(r, c)) != sig(b.cell(r, c)):
                    bad.append(f'{s} {L(c)}{r}: {sig(a.cell(r,c))[:3]} vs {sig(b.cell(r,c))[:3]}')
        if sorted(map(str, a.merged_cells.ranges)) != sorted(map(str, b.merged_cells.ranges)):
            bad.append(f'{s} merged differ')
    print('== same', p0, p1, 'sheets', sheets or 'shared', 'cells', n, 'mismatches', len(bad))
    for x in bad[:20]:
        print('   ', x)

def zipsame(p0, p1):
    z0, z1 = zipfile.ZipFile(p0), zipfile.ZipFile(p1)
    n0, n1 = sorted(z0.namelist()), sorted(z1.namelist())
    diff = [n for n in n0 if n in n1 and z0.read(n) != z1.read(n)]
    print('== zip', p0, p1, 'members', len(n0), len(n1), 'differing', diff)

if __name__ == '__main__':
    if sys.argv[1] == '--same':
        same(sys.argv[2], sys.argv[3], sys.argv[4].split(',') if len(sys.argv) > 4 else None)
    elif sys.argv[1] == '--zip':
        zipsame(sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2])
