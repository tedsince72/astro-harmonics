"""T24 HORSE / JOCKEY (SKY STARS) and SKY STARS SUMMARY (Eddie, 27 Oct 2026): checks one build against the build before (b19fac1f).
usage: check_t24ss.py <before.xlsx> <after.xlsx>
(a) every sheet of the before workbook identical in the after one (values, fills, fonts, borders, number formats, comments, merged
    ranges), runner sheets after removing exactly the two new tables; the after workbook = before + 'SKY STARS SUMMARY' after the runner
    sheets (and their RATIOS / NUMBERS);
(b) selection = every star row of the SKY block (S Jupiter → S star, T1_T2_T24_STARS) with a score in RA or Dec, in T24 order; sky hit
    text from the SKY block cells;
(c) every new-table T24 cell = its T24 row cell; every SCORES cell = the score in its value cell's comment (blank exactly where none),
    fill = the value cell's; header rows;
(d) SKY STARS SUMMARY = the runner tables cell for cell, runners in order, blank rows as specified.
Prints 'mismatches: n' last."""
import sys, os
import openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from jupiter_tables import T1_T2_T24_STARS  # noqa: E402

bad = []


def err(*a):
    bad.append(' '.join(str(x) for x in a))


def sig(c):
    cm = c.comment.text if c.comment else None
    b = c.border
    return (c.value, c.fill.fill_type, c.fill.start_color.rgb if c.fill.fill_type else None, c.font.b, c.number_format,
            (b.left.style, b.right.style, b.top.style, b.bottom.style), cm, c.alignment.wrap_text)


def rowsig(ws, r, ncol):
    return [sig(ws.cell(row=r, column=k)) for k in range(1, ncol + 1)]


B = openpyxl.load_workbook(sys.argv[1])
A = openpyxl.load_workbook(sys.argv[2])
runners = [s for s in B.sheetnames if len(s) == 3 and s[0] == 'P' and s[1:].isdigit()]
exp = list(B.sheetnames)
last = max(exp.index(s) for s in exp if s[:3] in runners)
exp.insert(last + 1, 'SKY STARS SUMMARY')
if A.sheetnames != exp:
    err('sheet order', A.sheetnames, exp)

# (b) selection from the SKY block on the after workbook
sk = A['SKY JUPITER']
sel = []
for r in range(1, sk.max_row + 1):
    if sk.cell(row=r, column=1).value != 'SKY':
        continue
    lab = sk.cell(row=r, column=2).value or ''
    if not lab.startswith('S Jupiter → S '):
        continue
    x = lab[len('S Jupiter → S '):]
    if x not in T1_T2_T24_STARS:
        continue
    hits = []
    for pl, c0 in (('RA', 3), ('Dec', 12)):
        sc = sk.cell(row=r, column=c0 + 5).value
        if sc is None:
            continue
        tgt = sk.cell(row=r, column=c0 + 2).value          # '70 (whole)'
        t, fam = tgt.rsplit(' (', 1)
        fam = fam[:-1]
        if fam == 'conj':
            t, fam = '0', 'conjunction'
        hits.append(f'{pl} {t} {fam} ({sc:.2f})')
    if hits:
        sel.append((x, '; '.join(hits)))
sel.sort(key=lambda z: T1_T2_T24_STARS.index(z[0]))
print('selected:', len(sel))
for x, h in sel:
    print(f'  {x}: {h}')

ss_rows = {}
for P in runners:
    a, b = A[P], B[P]
    # locate the new tables
    tit = {who: next((r for r in range(1, a.max_row + 1) if a.cell(row=r, column=1).value == f'T24 {who} (SKY STARS)'), None)
           for who in ('HORSE', 'JOCKEY')}
    t24 = {who: next(r for r in range(1, a.max_row + 1) if a.cell(row=r, column=1).value == 'T24'
                     and str(a.cell(row=r, column=2).value).startswith(f'T24 {who} (natal)')) for who in ('HORSE', 'JOCKEY')}
    D = a.max_row - b.max_row
    h0 = tit['HORSE']
    # (a) rows outside [h0, h0 + D) identical, shifted
    ncol = max(a.max_column, b.max_column)
    for r in range(1, b.max_row + 1):
        ra = r if r < h0 else r + D
        if rowsig(a, ra, ncol) != rowsig(b, r, ncol):
            err(P, 'row differs', r, '->', ra)
    for r in range(h0, h0 + D):                           # the inserted region holds only the two tables and blank rows
        v = a.cell(row=r, column=1).value
        if v not in (None, 'table', 'T24 HORSE (SKY STARS)', 'T24 JOCKEY (SKY STARS)'):
            err(P, 'unexpected row in the inserted region', r, v)
    mb = {(m.min_row if m.min_row < h0 else m.min_row + D, m.min_col, m.max_row if m.min_row < h0 else m.max_row + D, m.max_col)
          for m in b.merged_cells.ranges}
    ma = {(m.min_row, m.min_col, m.max_row, m.max_col) for m in a.merged_cells.ranges if not (h0 <= m.min_row < h0 + D)}
    if ma != mb:
        err(P, 'merged ranges differ', len(ma ^ mb))
    for L, d in b.column_dimensions.items():
        if d.customWidth and a.column_dimensions[L].width < d.width:
            err(P, 'column narrowed', L)
    # (b) + (c)
    ss_rows[P] = {}
    for who, C in (('HORSE', 'H'), ('JOCKEY', 'J')):
        t0, s = tit[who], t24[who]
        # T24 block geometry
        stars, r = [], s + 3
        while a.cell(row=r, column=1).value == 'T24':
            stars.append(a.cell(row=r, column=2).value[2:]); r += 1
        bodies = []
        k = 3
        while a.cell(row=s + 2, column=k).value != 'star = middle of A, B: total (side, between / far side)':
            bodies.append(a.cell(row=s + 2, column=k).value); k += 1
        n = len(bodies)
        lastc = 3 + 2 * (n + 1)
        want = [(x, h) for x, h in sel if x in stars]
        title = a.cell(row=t0, column=2).value
        if not title.endswith(f'Selected: {len(want)} star{"" if len(want) == 1 else "s"}'):
            err(P, who, 'title count', title[-30:])
        # header rows
        for k2 in range(2):
            for col in range(1, lastc + 1):
                src, dst = a.cell(row=s + 1 + k2, column=col), a.cell(row=t0 + 1 + k2, column=col + (col >= 3))
                if sig(src) != sig(dst):
                    err(P, who, 'header cell', k2, col)
            for i, bd in enumerate(bodies):
                for pl, so in (('RA', lastc + 2), ('Dec', lastc + 2 + n)):
                    v = a.cell(row=t0 + 1 + k2, column=so + i).value
                    if v != ((f'SCORES {pl}' if i == 0 else None) if k2 == 0 else bd):
                        err(P, who, 'scores header', k2, pl, i, v)
        if a.cell(row=t0 + 1, column=3).value != 'sky hit':
            err(P, who, 'sky hit header')
        got = []
        r = t0 + 3
        while a.cell(row=r, column=1).value == f'T24 {who} (SKY STARS)':
            got.append(r); r += 1
        if a.cell(row=r, column=1).value is not None:
            err(P, who, 'row after the table not blank', r)
        if len(got) != len(want):
            err(P, who, 'rows', len(got), len(want))
        for rr, (x, h) in zip(got, want):
            if a.cell(row=rr, column=2).value != f'{C} {x}':
                err(P, who, 'star', rr, a.cell(row=rr, column=2).value, x)
            if a.cell(row=rr, column=3).value != h:
                err(P, who, 'sky hit', x, a.cell(row=rr, column=3).value, h)
            sr = s + 3 + stars.index(x)
            for col in range(2, lastc + 1):
                if sig(a.cell(row=sr, column=col)) != sig(a.cell(row=rr, column=col + (col >= 3))):
                    err(P, who, x, 'T24 cell differs', col)
            for pl, vc0, so in (('RA', 3, lastc + 2), ('Dec', 3 + n + 1, lastc + 2 + n)):
                for i in range(n):
                    vc, sc = a.cell(row=sr, column=vc0 + i), a.cell(row=rr, column=so + i)
                    first = vc.comment.text.split('\n')[0]
                    exp_s = None if first.startswith('nearest') else round(float(first.rsplit(' · ', 1)[1]), 2)
                    if sc.value != exp_s:
                        err(P, who, x, pl, bodies[i], 'score', sc.value, exp_s)
                    ef = (vc.fill.fill_type, vc.fill.start_color.rgb) if (exp_s is not None and vc.fill.fill_type) else (None, None)
                    gf = (sc.fill.fill_type, sc.fill.start_color.rgb if sc.fill.fill_type else None)
                    if gf != ef:
                        err(P, who, x, pl, bodies[i], 'score fill', gf, ef)
                    if exp_s is not None and sc.number_format != '0.00':
                        err(P, who, x, 'score format')
            for col in range(lastc + 2 + 2 * n, a.max_column + 1):
                if a.cell(row=rr, column=col).value is not None:
                    err(P, who, x, 'cell beyond the table', col)
        ss_rows[P][C] = (t0, (got[-1] if got else t0 + 2))
        print(f'{P} {who}: {len(got)} rows')

# (d) summary
S = A['SKY STARS SUMMARY']
row = 1
for P in runners:
    a = A[P]
    if S.cell(row=row, column=1).value != a.cell(row=1, column=1).value:
        err('summary title', P, S.cell(row=row, column=1).value)
    row += 1
    for C in 'HJ':
        r0, r1 = ss_rows[P][C]
        nc = a.max_column
        for r in range(r0, r1 + 1):
            if rowsig(S, row + r - r0, nc) != rowsig(a, r, nc):
                err('summary', P, C, r)
        ma = {(m.min_row - r0, m.min_col, m.max_row - r0, m.max_col) for m in a.merged_cells.ranges if r0 <= m.min_row <= r1}
        ms = {(m.min_row - row, m.min_col, m.max_row - row, m.max_col) for m in S.merged_cells.ranges if row <= m.min_row <= row + r1 - r0}
        if ma != ms:
            err('summary merges', P, C)
        row += r1 - r0 + 1
        gap = 1 if C == 'H' else 2
        for g in range(gap):
            if any(S.cell(row=row + g, column=k).value is not None for k in range(1, S.max_column + 1)):
                err('summary gap not blank', P, C, row + g)
        row += gap
if S.max_row > row - 1:
    err('summary has rows after the last runner', S.max_row, row)
print('summary rows:', S.max_row)
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
