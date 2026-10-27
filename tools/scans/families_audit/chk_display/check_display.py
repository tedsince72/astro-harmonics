"""Three display changes (Eddie, 27 Oct 2026): checks one build against the build before (commit a2d20618).
usage: check_display.py <before.xlsx> <after.xlsx> [<build before the S Jupiter column (35255b16)>]
(1) SKY STARS SUMMARY: rows 1-2 = the header rows of the first table (rows 5-6 after the shift: values, styles, comments, merges); every
    other row = the before row two rows up; merged ranges shifted by two; freeze pane C3 on the summary, every other sheet's freeze as before;
(2) every 'stars' separator row of T24 HORSE / JOCKEY (SKY STARS) (runner sheets and summary): fill D9D9D9 from column A to the last SCORES
    column, none beyond; otherwise as before (value 'stars', bold);
(3) column widths: no column on any sheet narrower than before; every T24 / (SKY STARS) midpoint column >= 40, repeats >= 60, value /
    S Jupiter / SCORES columns >= 11;
every other cell of every sheet identical (values, fills, fonts, borders, number formats, comments). Prints 'mismatches: n' last."""
import sys, re
import openpyxl
from openpyxl.utils import get_column_letter as L

bad = []
err = lambda *a: bad.append(' '.join(str(x) for x in a))


def sig(c, fill=True):
    b = c.border
    return (c.value, (c.fill.fill_type, c.fill.start_color.rgb if c.fill.fill_type else None) if fill else None, c.font.b, c.number_format,
            (b.left.style, b.right.style, b.top.style, b.bottom.style), c.comment.text if c.comment else None, c.alignment.wrap_text)


B = openpyxl.load_workbook(sys.argv[1])
A = openpyxl.load_workbook(sys.argv[2])
if A.sheetnames != B.sheetnames:
    err('sheet order')
SUM = 'SKY STARS SUMMARY'
nsep = ngrey = nwide = 0
for sh in A.sheetnames:
    a, b = A[sh], B[sh]
    d = 2 if sh == SUM else 0
    nc = max(a.max_column, b.max_column)
    if a.max_row != b.max_row + d:
        err(sh, 'rows', a.max_row, b.max_row)
    seps = set()
    for r in range(1, b.max_row + 1):
        if str(b.cell(row=r, column=1).value).endswith('(SKY STARS)') and b.cell(row=r, column=2).value == 'stars':
            seps.add(r)
    for r in range(1, b.max_row + 1):
        ra = r + d
        if r in seps:
            nsep += 1
            last = max(k for k in range(1, nc + 1) if b.cell(row=r - 1, column=k).value is not None or b.cell(row=r + 1, column=k).value is not None
                       or b.cell(row=r - 5, column=k).value is not None)
            # the table's last column = its header row 2 (body names) last filled column
            h = r
            while not (b.cell(row=h, column=1).value is None and b.cell(row=h, column=3).value == 'SKY block hit(s): plane target family (score)'):
                h -= 1
            last = max(k for k in range(1, nc + 1) if b.cell(row=h, column=k).value is not None)
            for k in range(1, nc + 1):
                ca, cb = a.cell(row=ra, column=k), b.cell(row=r, column=k)
                if sig(ca, False) != sig(cb, False):
                    err(sh, 'separator', r, k)
                g = ca.fill.fill_type == 'solid' and ca.fill.start_color.rgb.endswith('D9D9D9')
                if g != (k <= last):
                    err(sh, 'separator fill', r, k, g, last)
                ngrey += g
            if a.cell(row=ra, column=2).value != 'stars' or not a.cell(row=ra, column=2).font.b:
                err(sh, 'separator text')
            continue
        if any(sig(a.cell(row=ra, column=k)) != sig(b.cell(row=r, column=k)) for k in range(1, nc + 1)):
            err(sh, 'row differs', r, '->', ra)
    ma = {(m.min_row, m.min_col, m.max_row, m.max_col) for m in a.merged_cells.ranges}
    mb = {(m.min_row + d, m.min_col, m.max_row + d, m.max_col) for m in b.merged_cells.ranges}
    if sh == SUM:
        for k in range(2):
            if any(sig(a.cell(row=1 + k, column=c)) != sig(a.cell(row=5 + k, column=c)) for c in range(1, nc + 1)):
                err(sh, 'header copy row', 1 + k)
        mb |= {(m[0] - 4, m[1], m[2] - 4, m[3]) for m in mb if 5 <= m[0] and m[2] <= 6}
        if a.freeze_panes != 'C3':
            err(sh, 'freeze', a.freeze_panes)
        if not (b.cell(row=1, column=1).value or '').startswith('P') or a.cell(row=1, column=1).value != 'table' or a.cell(row=1, column=3).value != 'sky hit':
            err(sh, 'top rows', a.cell(row=1, column=1).value, a.cell(row=1, column=3).value)
    elif a.freeze_panes != b.freeze_panes:
        err(sh, 'freeze', a.freeze_panes, b.freeze_panes)
    if ma != mb:
        err(sh, 'merged ranges', sorted(ma ^ mb)[:4])
    # widths
    for col, dim in b.column_dimensions.items():
        if dim.customWidth and a.column_dimensions[col].width < dim.width - 1e-9:
            err(sh, 'column narrower', col, a.column_dimensions[col].width, dim.width)
    W = lambda k: a.column_dimensions[L(k)].width if L(k) in a.column_dimensions and a.column_dimensions[L(k)].customWidth else 0
    for r in range(1, a.max_row + 1):
        v = a.cell(row=r, column=1).value
        t = str(a.cell(row=r, column=2).value or '')
        if not ((v == 'T24' and t.startswith('T24 ')) or (str(v).endswith('(SKY STARS)') and t.startswith(str(v) + ' ('))):
            continue
        for k in range(3, a.max_column + 1):
            h1, h2 = a.cell(row=r + 1, column=k).value, a.cell(row=r + 2, column=k).value
            if h1 is None and h2 is None:
                continue
            need = 60 if h1 == 'repeats' else 40 if str(h1).endswith(' midpoints') else 36 if h1 == 'sky hit' else 11
            nwide += 1
            if W(k) < need:
                err(sh, 'width', L(k), W(k), need, h1, h2)
if len(sys.argv) > 3:                                     # (3) also no column narrower than before a2d20618
    O = openpyxl.load_workbook(sys.argv[3])
    for sh in O.sheetnames:
        for col, dim in O[sh].column_dimensions.items():
            if dim.customWidth and A[sh].column_dimensions[col].width < dim.width - 1e-9:
                err(sh, 'column narrower than before the S Jupiter column', col, A[sh].column_dimensions[col].width, dim.width)
    print('widths also checked against', sys.argv[3].rsplit('/', 1)[-1])
print('separator rows:', nsep, '| grey cells:', ngrey, '| header columns checked:', nwide)
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
