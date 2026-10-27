"""T24 HORSE / JOCKEY "S Jupiter" column and the four Jupiter rows of T24 HORSE / JOCKEY (SKY STARS) (Eddie, 27 Oct 2026): checks one build
against the build before (commit 35255b16).
usage: check_sjcol.py <before.xlsx> <after.xlsx>
(a) every sheet identical to the before workbook (values, fills, fonts, borders, number formats, comments, wrap), except: in T24 HORSE /
    JOCKEY (natal) the two "S Jupiter" columns are new and the title carries the S JUPITER note; in T24 HORSE / JOCKEY (SKY STARS) the
    S Jupiter value and SCORES columns, the four Jupiter rows and the separator 'stars' are new and the title carries the Jupiter-rows note;
    rows below shift by the inserted rows; merged ranges as the layout; no column narrowed; the summary is checked against the runner tables;
(b) every S Jupiter cell of T24 HORSE / JOCKEY = the SKY block cell S Jupiter → S star (value, target, offset, score; fill, red inside the
    conjunction range), in its place (header 'S Jupiter' after Ketu, RA and Dec);
(c) the four rows of every (SKY STARS) table = the T1 / T2 SKY cells, T1 / T2, T5 / T6, T7 / T8 (Jupiter column: T9 S Jupiter – natal
    Jupiter) on the same sheet, every body, both planes (value, target, offset, score, fill, red); blank where a point meets itself; sky hit,
    S Jupiter, midpoint and repeats cells blank on them;
(d) every SCORES cell of every (SKY STARS) row = the score in its value cell's comment (blank exactly where none), fill as the value cell;
(e) SKY STARS SUMMARY = the runner tables cell for cell (and merged ranges), runners in order, blank rows as specified.
Prints 'mismatches: n' last."""
import sys, os, re
import openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from jupiter_tables import T24SJ_NOTE, T24SS_JNOTE, families  # noqa: E402
CONJ_TOL = families.CONJ

bad = []
err = lambda *a: bad.append(' '.join(str(x) for x in a))


def sig(c):
    cm = c.comment.text if c.comment else None
    b = c.border
    return (c.value, c.fill.fill_type, c.fill.start_color.rgb if c.fill.fill_type else None, c.font.b, c.number_format,
            (b.left.style, b.right.style, b.top.style, b.bottom.style), cm, c.alignment.wrap_text)


EMPTY = sig(openpyxl.Workbook().active.cell(row=1, column=1))


def rowsig(ws, r, ncol, drop=()):
    out = [sig(ws.cell(row=r, column=k)) for k in range(1, ncol + 1) if k not in drop]
    while out and out[-1] == EMPTY:
        out.pop()
    return out


B = openpyxl.load_workbook(sys.argv[1])
A = openpyxl.load_workbook(sys.argv[2])
if A.sheetnames != B.sheetnames:
    err('sheet order', A.sheetnames, B.sheetnames)
runners = [s for s in A.sheetnames if re.fullmatch(r'P\d\d', s)]
for sh in A.sheetnames:
    if sh in runners or sh == 'SKY STARS SUMMARY':
        continue
    a, b = A[sh], B[sh]
    nc = max(a.max_column, b.max_column)
    if a.max_row != b.max_row or any(rowsig(a, r, nc) != rowsig(b, r, nc) for r in range(1, a.max_row + 1)):
        err(sh, 'sheet differs')
    if {str(m) for m in a.merged_cells.ranges} != {str(m) for m in b.merged_cells.ranges}:
        err(sh, 'merged ranges differ')

# SKY block: S Jupiter → S star cells (RA from column 3, Dec from 12: value, +5, target, group, offset, score)
sk = A['SKY JUPITER']
SKY = {}
for r in range(1, sk.max_row + 1):
    lab = sk.cell(row=r, column=2).value
    if sk.cell(row=r, column=1).value == 'SKY' and lab and lab.startswith('S Jupiter → S '):
        for pl, c0 in (('RA', 3), ('Dec', 12)):
            SKY[(lab[14:], pl)] = tuple(sk.cell(row=r, column=c0 + k) for k in range(6))


def same_cell(tc, c, pl, what):
    """tc = the table's six cells (value, +5, target, group, offset, score); c = a T24-format cell"""
    v = tc[0].value
    if v is None:
        if c.value is not None:
            err(what, 'should be blank', c.value)
        return
    if c.value != v:
        err(what, 'value', c.value, v); return
    first = c.comment.text.split('\n')[0] if c.comment else ''
    off = tc[4].value
    if tc[5].value is not None:
        tgt = tc[2].value                                  # '70 (whole)', '0 (conj)' ...
        num, fam = tgt.rsplit(' (', 1)
        fam = fam[:-1]
        parts = first.split(' · ')
        famc = parts[1] if len(parts) == 4 else None
        if fam == 'conj':
            ok = parts[0] == '0' and famc and famc.startswith('conjunction')
        else:
            ok = parts[0] + ' (' + (famc or '') + ')' == tgt or (parts[0] == num)
        if not (ok and len(parts) == 4 and parts[2] == off and parts[3] == f'{tc[5].value:.2f}'):
            err(what, 'comment', first, '| table', tgt, off, tc[5].value)
    elif not first.startswith('nearest') or (off is not None and off not in first):
        err(what, 'no-hit comment', first, off)
    red = v < CONJ_TOL[pl]
    want = '00FF8080' if red else (tc[0].fill.start_color.rgb if tc[0].fill.fill_type else None)
    got = c.fill.start_color.rgb if c.fill.fill_type else None
    if got != want:
        err(what, 'fill', got, want)


def find_row(ws, tid, lab):
    for r in range(1, ws.max_row + 1):
        if ws.cell(row=r, column=1).value == tid and ws.cell(row=r, column=2).value == lab:
            return r


def cells_at(ws, r, c0):
    return tuple(ws.cell(row=r, column=c0 + k) for k in range(6))


def blocks(ws):
    """-> {who: (natal title row, last star row, n bodies, bodies)}, {who: (SS title row, last row)}"""
    nat, ss = {}, {}
    for who in ('HORSE', 'JOCKEY'):
        t = next(r for r in range(1, ws.max_row + 1) if ws.cell(row=r, column=1).value == 'T24'
                 and str(ws.cell(row=r, column=2).value).startswith(f'T24 {who} (natal)'))
        bodies, k = [], 3
        while ws.cell(row=t + 2, column=k).value not in ('S Jupiter', 'star = middle of A, B: total (side, between / far side)'):
            bodies.append(ws.cell(row=t + 2, column=k).value); k += 1
        r = t + 3
        while ws.cell(row=r, column=1).value == 'T24':
            r += 1
        nat[who] = (t, r - 1, len(bodies), bodies)
        s = next((r for r in range(1, ws.max_row + 1) if ws.cell(row=r, column=1).value == f'T24 {who} (SKY STARS)'), None)
        r = s + 3
        while ws.cell(row=r, column=1).value == f'T24 {who} (SKY STARS)':
            r += 1
        ss[who] = (s, r - 1)
    return nat, ss


nsj = njr = 0
narrowed = set()
SSR = {}
for P in runners:
    a, b = A[P], B[P]
    na, sa = blocks(a)
    nb_, sb = blocks(b)
    nc = max(a.max_column, b.max_column) + 4
    # (a) row map after -> before: drop the inserted rows, drop the new columns in the two kinds of block
    amap = []                                              # (after row, drop columns, kind)
    ins = set()
    for who in ('HORSE', 'JOCKEY'):
        s, e = sa[who]
        ins |= set(range(s + 3, s + 8))                    # the four Jupiter rows + the separator
    for r in range(1, a.max_row + 1):
        if r in ins:
            continue
        drop, kind = (), None
        for who in ('HORSE', 'JOCKEY'):
            t, e, n, _ = na[who]
            if t <= r <= e:
                drop, kind = (3 + n, 2 * n + 5), ('nat', who, r == t)
            s, e2 = sa[who]
            if s <= r <= e2:
                drop, kind = (4 + n, 2 * n + 6, 3 * n + 9, 4 * n + 10), ('ss', who, r == s)
        amap.append((r, drop, kind))
    if len(amap) != b.max_row:
        err(P, 'rows', len(amap), b.max_row)
    for (ra, drop, kind), rb in zip(amap, range(1, b.max_row + 1)):
        x, y = rowsig(a, ra, nc, drop), rowsig(b, rb, nc)
        if kind and kind[2]:                               # a title row: the note added
            tb, ta = y[1][0], x[1][0]
            note = T24SJ_NOTE if kind[0] == 'nat' else T24SS_JNOTE.format(C=kind[1][0])
            if kind[0] == 'nat':
                h, t_ = tb.rsplit('. REPEATS (22 Oct 2026)', 1)
                want = h + note + '. REPEATS (22 Oct 2026)' + t_
            else:
                want = tb.replace('. Selected:', note + '. Selected:', 1)
            if ta != want:
                err(P, 'title', ra, ta[-120:])
            x, y = x[:1] + x[2:], y[:1] + y[2:]
        if x != y:
            err(P, 'row differs', rb, '->', ra, kind)
    # merged ranges
    rowmap = {rb: ra for (ra, _, _), rb in zip(amap, range(1, b.max_row + 1))}
    hdr = {}
    for who in ('HORSE', 'JOCKEY'):
        t, _, n, _ = na[who]
        hdr[t + 1] = {(t + 1, 3, t + 1, 3 + n), (t + 1, n + 5, t + 1, 2 * n + 5)}
        s = sa[who][0]
        hdr[s + 1] = {(s + 1, 4, s + 1, 4 + n), (s + 1, n + 6, s + 1, 2 * n + 6), (s + 1, 2 * n + 9, s + 1, 3 * n + 9), (s + 1, 3 * n + 10, s + 1, 4 * n + 10)}
    ma = {(m.min_row, m.min_col, m.max_row, m.max_col) for m in a.merged_cells.ranges}
    mb = {(rowmap[m.min_row], m.min_col, rowmap[m.max_row], m.max_col) for m in b.merged_cells.ranges if rowmap[m.min_row] not in hdr}
    if ma != mb | set().union(*hdr.values()):
        err(P, 'merged ranges', sorted(ma ^ (mb | set().union(*hdr.values())))[:4])
    # widths: columns before the first S Jupiter column never narrowed; from there the T24 columns move right by one (two in the (SKY STARS)
    # tables' SCORES), so a width set by T24 moves with its column: check the new layout's widths instead
    n0 = na['HORSE'][2]
    for L, d in b.column_dimensions.items():
        if d.customWidth and openpyxl.utils.column_index_from_string(L) < 3 + n0 and a.column_dimensions[L].width < d.width:
            err(P, 'column narrowed', L)
    W = lambda k: a.column_dimensions[openpyxl.utils.get_column_letter(k)].width
    n = n0
    want_w = ([(k, 11) for k in list(range(3, 3 + n + 1)) + list(range(n + 5, 2 * n + 6))] + [(3 + n + 1, 40), (2 * n + 6, 40), (2 * n + 7, 60)]
              + [(4 + n + 1, 40), (2 * n + 7, 40), (2 * n + 8, 60), (3, 36)] + [(k, 11) for k in range(2 * n + 9, 4 * n + 11)])
    for k, w in want_w:
        if W(k) < w:
            err(P, 'width', openpyxl.utils.get_column_letter(k), W(k), w)
    narrowed.update(L for L, d in b.column_dimensions.items() if d.customWidth and a.column_dimensions[L].width < d.width)
    # (b) the S Jupiter columns
    for who, C in (('HORSE', 'H'), ('JOCKEY', 'J')):
        t, e, n, bodies = na[who]
        for k, pl in ((3 + n, 'RA'), (2 * n + 5, 'Dec')):
            if a.cell(row=t + 2, column=k).value != 'S Jupiter' or a.cell(row=t + 2, column=k - 1).value != 'Ketu':
                err(P, who, 'S Jupiter header', pl)
            for r in range(t + 3, e + 1):
                x = a.cell(row=r, column=2).value[2:]
                same_cell(SKY[(x, pl)], a.cell(row=r, column=k), pl, f'{P} {who} {x} S Jupiter {pl}')
                nsj += 1
    # (c) four rows, (d) SCORES
    for who, C in (('HORSE', 'H'), ('JOCKEY', 'J')):
        t, e, n, bodies = na[who]
        s, e2 = sa[who]
        m = n + 1
        tc0 = {'RA': 4, 'Dec': 4 + m + 1}
        s0 = {'RA': 2 * n + 9, 'Dec': 3 * n + 10}
        T12, T58, T78 = ('T1', 'T5', 'T7') if C == 'H' else ('T2', 'T6', 'T8')
        r9 = find_row(a, 'T9', f'S Jupiter – {C} Jupiter')
        labs = ['S Jupiter → S body', f'{C} Jupiter → {C} body', f'S Jupiter → {C} body', f'S body → {C} Jupiter', 'stars']
        for i, lab in enumerate(labs):
            r = s + 3 + i
            if a.cell(row=r, column=1).value != f'T24 {who} (SKY STARS)' or a.cell(row=r, column=2).value != lab:
                err(P, who, 'row label', r, a.cell(row=r, column=2).value, lab)
        sep = s + 7
        if any(a.cell(row=sep, column=k).value is not None for k in range(3, a.max_column + 1)):
            err(P, who, 'separator not blank')
        for i in range(4):
            r = s + 3 + i
            for pl in ('RA', 'Dec'):
                for j, bd in enumerate(bodies):
                    c = a.cell(row=r, column=tc0[pl] + j)
                    if bd == 'Jupiter':
                        if i < 2:
                            if c.value is not None:
                                err(P, who, r, 'Jupiter cell not blank'); continue
                            tc = None
                        else:
                            tc = cells_at(a, r9, 3 if pl == 'RA' else 11)
                    elif i == 0:
                        tc = cells_at(a, find_row(a, T12, f'{C} Jupiter → {C} {bd}'), 19 if pl == 'RA' else 28)
                    elif i == 1:
                        tc = cells_at(a, find_row(a, T12, f'{C} Jupiter → {C} {bd}'), 3 if pl == 'RA' else 11)
                    elif i == 2:
                        tc = cells_at(a, find_row(a, T58, f'S Jupiter → {C} {bd}'), 3 if pl == 'RA' else 11)
                    else:
                        tc = cells_at(a, find_row(a, T78, f'S {bd} → {C} Jupiter'), 3 if pl == 'RA' else 11)
                    if tc is not None:
                        if tc[0].value is None:
                            err(P, who, labs[i], bd, pl, 'table cell missing')
                        same_cell(tc, c, pl, f'{P} {who} {labs[i]} {bd} {pl}')
                        njr += 1
                for k in (tc0[pl] + n, tc0[pl] + m):       # S Jupiter, midpoints
                    if a.cell(row=r, column=k).value is not None:
                        err(P, who, r, 'S Jupiter / midpoint cell not blank', k)
            for k in (3, 2 * n + 8):                       # sky hit, repeats
                if a.cell(row=r, column=k).value is not None:
                    err(P, who, r, 'sky hit / repeats not blank', k)
        for r in [s + 3 + i for i in range(4)] + list(range(s + 8, e2 + 1)):
            for pl in ('RA', 'Dec'):
                for j in range(m):
                    vc, sc = a.cell(row=r, column=tc0[pl] + j), a.cell(row=r, column=s0[pl] + j)
                    first = vc.comment.text.split('\n')[0] if vc.comment else None
                    es = None if first is None or first.startswith('nearest') else round(float(first.rsplit(' · ', 1)[1]), 2)
                    if sc.value != es:
                        err(P, who, r, pl, j, 'SCORES', sc.value, es)
                    ef = vc.fill.start_color.rgb if (es is not None and vc.fill.fill_type) else None
                    if (sc.fill.start_color.rgb if sc.fill.fill_type else None) != ef:
                        err(P, who, r, pl, j, 'SCORES fill')
            for k in range(4 * n + 11, a.max_column + 1):
                if a.cell(row=r, column=k).value is not None:
                    err(P, who, r, 'cell beyond the table', k)
        for j, bd in enumerate(bodies + ['S Jupiter']):
            for pl in ('RA', 'Dec'):
                if a.cell(row=s + 2, column=s0[pl] + j).value != bd:
                    err(P, who, 'SCORES header', pl, j)
        SSR[(P, C)] = (s, e2)
    print(f'{P}: S Jupiter cells so far {nsj}, Jupiter-row cells so far {njr}')

# (e) summary
S = A['SKY STARS SUMMARY']
row = 1
for P in runners:
    a = A[P]
    if S.cell(row=row, column=1).value != a.cell(row=1, column=1).value:
        err('summary title', P)
    row += 1
    for C in 'HJ':
        r0, r1 = SSR[(P, C)]
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
        if any(S.cell(row=row + g, column=k).value is not None for g in range(gap) for k in range(1, S.max_column + 1)):
            err('summary gap', P, C)
        row += gap
if S.max_row > row - 1:
    err('summary rows after the last runner', S.max_row, row)
print('S Jupiter cells:', nsj)
print('Jupiter-row cells:', njr)
print('summary rows:', S.max_row)
print('columns narrower than before (moved with the shift):', ' '.join(sorted(narrowed, key=lambda L: (len(L), L))))
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
