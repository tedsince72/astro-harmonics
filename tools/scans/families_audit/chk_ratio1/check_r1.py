"""Ratio 1 in column C, SUMMARY freeze D4 (Eddie, 31 Oct 2026): a build before (Part 1 commit e6267326) against a build after.
usage: python3 check_r1.py <before.xlsx> <after.xlsx>
Allowed differences only: SUMMARY freeze None -> D4; the fill of column C on MATCH HORSE / MATCH JOCKEY / MATCH HORSE | JOCKEY data rows (runner
sheets and SUMMARY), none -> solid BDD7EE, exactly where column C is '1'. Everything else (sheets, values, fonts, fills, borders, alignment,
number formats, comments, merges, widths, other freezes) identical. Prints per-runner counts of filled cells per table and 'mismatches: n'."""
import sys, openpyxl
from collections import Counter

TIDS = ('MATCH HORSE', 'MATCH JOCKEY', 'MATCH HORSE | JOCKEY')
SECS = ('EXACT', 'RATIO', 'BODY', 'CONJ STAR')
b, a = (openpyxl.load_workbook(p) for p in sys.argv[1:3])
bad = []
memo = {}


def sty(wb, c):
    if getattr(c, '_style', None) is None:                 # merged cell
        return 'merged'
    k = (id(wb), tuple(c._style))
    if k not in memo:
        memo[k] = (repr(c.font), repr(c.border), repr(c.alignment), c.number_format, repr(c.protection))
    return memo[k]


def fillkey(c):
    if getattr(c, '_style', None) is None:
        return 'merged'
    f = c.fill
    return (f.fill_type, str(f.start_color.rgb)[-6:] if f.start_color is not None else None)   # 'BDD7EE' (stored '00BDD7EE')


if b.sheetnames != a.sheetnames:
    bad.append(('sheets', b.sheetnames, a.sheetnames))
cnt = {}                                                   # (sheet, table) -> filled C cells
for name in a.sheetnames:
    wb_, wa = b[name], a[name]
    fz = (wb_.freeze_panes, wa.freeze_panes)
    if name == 'SUMMARY':
        if fz != (None, 'D4'):
            bad.append(('freeze', name, fz))
    elif fz[0] != fz[1]:
        bad.append(('freeze', name, fz))
    if sorted(map(str, wb_.merged_cells.ranges)) != sorted(map(str, wa.merged_cells.ranges)):
        bad.append(('merges', name))
    wd = lambda ws: {k: (d.width, d.customWidth) for k, d in ws.column_dimensions.items() if d.customWidth}
    if wd(wb_) != wd(wa):
        bad.append(('widths', name))
    if (wb_.max_row, wb_.max_column) != (wa.max_row, wa.max_column):
        bad.append(('size', name, wb_.max_row, wa.max_row))
    for rb, ra in zip(wb_.iter_rows(), wa.iter_rows()):
        tid, sec = ra[0].value, ra[1].value if len(ra) > 1 else None
        data = tid in TIDS and sec in SECS
        for cb, ca in zip(rb, ra):
            if cb.value != ca.value or sty(b, cb) != sty(a, ca) or (cb.comment.text if cb.comment else None) != (ca.comment.text if ca.comment else None):
                bad.append(('cell', name, ca.coordinate, cb.value, ca.value))
                continue
            fb, fa = fillkey(cb), fillkey(ca)
            if ca.column == 3 and data:
                want = ('solid', 'BDD7EE') if ca.value == '1' else fb
                if fa != want or (ca.value == '1' and fb == want):
                    bad.append(('C fill', name, ca.coordinate, ca.value, fb, fa))
                if ca.value == '1':
                    cnt[(name, tid)] = cnt.get((name, tid), 0) + 1
                    if sec != 'EXACT':
                        bad.append(('ratio 1 off EXACT', name, ca.coordinate, sec))
                elif sec == 'EXACT':
                    bad.append(('EXACT without 1', name, ca.coordinate, ca.value))
            elif fb != fa:
                bad.append(('fill', name, ca.coordinate, fb, fa))
# no BDD7EE anywhere else
for name in a.sheetnames:
    for row in a[name].iter_rows():
        for c in row:
            if fillkey(c)[1] == 'BDD7EE' and not (c.column == 3 and row[0].value in TIDS and row[1].value in SECS and c.value == '1'):
                bad.append(('stray blue', name, c.coordinate))
runners = [n for n in a.sheetnames if n[0] == 'P' and n[1:].isdigit()]
for P in runners:
    print(P, 'filled C:', ', '.join(f'{t} {cnt.get((P, t), 0)}' for t in TIDS))
print('SUMMARY filled C:', cnt.get(('SUMMARY', TIDS[2]), 0))
print('totals:', ', '.join(f'{t} {sum(v for (s, tt), v in cnt.items() if tt == t and s != "SUMMARY")}' for t in TIDS),
      '| SUMMARY', cnt.get(('SUMMARY', TIDS[2]), 0))
print('freeze:', {n: a[n].freeze_panes for n in a.sheetnames if n in ('POSITIONS', 'SKY JUPITER', 'SUMMARY') or n == (runners[:1] or [''])[0]})
for x in bad[:20]:
    print('  ', x)
print('mismatches:', len(bad))
