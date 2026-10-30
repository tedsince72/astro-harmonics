"""MATCH HORSE / MATCH JOCKEY (Eddie, 30 Oct 2026): checks one build against the build before (9e5d5ea5), same race.
usage: check_match.py <before.xlsx> <after.xlsx>
(a) every sheet identical to before (value, fill, font, border, number format, comment; merges, widths, freeze), runner sheets apart from the
    two new blocks appended after T24 JOCKEY (MATCH HORSE, then MATCH JOCKEY);
(b) the MATCH rows rebuilt from the sheet cells themselves: SKY block cells (SKY JUPITER, value + target text 'target (family)' + score) and
    T24 HORSE / JOCKEY cells (value + comment 'target · family · offset · score'): scoring, not conjunction; T24 star rows x body columns (not
    S Jupiter), Jupiter rows except 'S Jupiter → S body'; pairs by the rules (exact same family + target, or across families the same 4
    significant digits of the two 6-dp values; ratio: whole / golden, gcd >= 2); every row's cells, order, fills, title counts.
Prints counts and 'mismatches: n' last."""
import sys, math
import openpyxl

bad = []


def err(*a):
    bad.append(' '.join(str(x) for x in a))


def sig(c):
    b = c.border
    return (c.value, c.fill.fill_type, c.fill.start_color.rgb if c.fill.fill_type else None, c.font.b, c.number_format,
            (b.left.style, b.right.style, b.top.style, b.bottom.style), c.comment.text if c.comment else None)


def d4(x):
    """first 4 significant digits, truncated, and the order of magnitude"""
    s = f'{x:.12e}'                                       # d.ddddddddddddE±kk
    return int(s.split('e')[1]), int(s[0] + s[2:5])


def colour(s):
    return '00C6EFCE' if s >= 80 else '00FFEB9C' if s >= 50 else '00FFF8DC' if s > 0 else None


B, A = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
if A.sheetnames != B.sheetnames:
    err('sheets', A.sheetnames)
AMAX = {s: (A[s].max_row, A[s].max_column) for s in A.sheetnames}
runners = [s for s in A.sheetnames if s[0] == 'P' and s[1:].isdigit()]

# SKY block cells
sk = A['SKY JUPITER']
sky = []
for r in range(1, sk.max_row + 1):
    if sk.cell(row=r, column=1).value != 'SKY' or not str(sk.cell(row=r, column=2).value).startswith('S Jupiter → S '):
        continue
    for pl, c0 in (('RA', 3), ('Dec', 12)):
        v, tg, sc = (sk.cell(row=r, column=c0 + k).value for k in (0, 2, 5))
        if sc is None or tg is None or tg.startswith('conj'):
            continue
        t, fam = tg.rsplit(' (', 1)
        sky.append((sk.cell(row=r, column=2).value, pl, v, fam[:-1], t, sc, sk.cell(row=r, column=c0).fill.start_color.rgb))
print('SKY block scoring cells:', len(sky))


def t24cells(ws, who):
    t0 = next(r for r in range(1, ws.max_row + 1) if ws.cell(row=r, column=1).value == 'T24' and str(ws.cell(row=r, column=2).value).startswith(f'T24 {who} (natal)'))
    cols = {}
    for k in range(3, ws.max_column + 1):
        h1 = ws.cell(row=t0 + 1, column=k).value
        if h1 in ('RA', 'Dec'):
            pl = h1
        name = ws.cell(row=t0 + 2, column=k).value
        if name in (None, 'S Jupiter') or str(name).startswith('star ='):
            if str(name).startswith('star =') and pl == 'Dec':
                break
            continue
        cols[k] = (pl, name)
    out, r = [], t0 + 3
    while ws.cell(row=r, column=1).value == 'T24':
        lab = ws.cell(row=r, column=2).value
        if lab not in ('S Jupiter → S body', 'stars'):
            for k, (pl, b) in cols.items():
                c = ws.cell(row=r, column=k)
                if c.value is None or c.comment is None:
                    continue
                f = c.comment.text.split('\n')[0].split(' · ')
                if f[0].startswith('nearest') or f[0] == 'no target' or f[1].startswith('conjunction'):
                    continue
                out.append((lab, b, pl, c.value, f[1], f[0], float(f[-1]), c.fill.start_color.rgb if c.fill.fill_type else None))
        r += 1
    return out


for P in runners:
    a, b = A[P], B[P]
    amr, amc = AMAX[P]
    m0 = next((r for r in range(1, amr + 1) if a.cell(row=r, column=1).value == 'MATCH HORSE'), None)
    if m0 is None:
        err(P, 'no MATCH HORSE'); continue
    nc = max(amc, b.max_column)
    for r in range(1, b.max_row + 1):                     # (a) everything before the new blocks
        for k in range(1, nc + 1):
            if sig(a.cell(row=r, column=k)) != sig(b.cell(row=r, column=k)):
                err(P, 'cell', r, k)
    if m0 <= b.max_row + 1 - 1 and any(b.cell(row=r, column=1).value for r in range(m0, b.max_row + 1)):
        err(P, 'MATCH overlaps old rows')
    if {str(m) for m in a.merged_cells.ranges} != {str(m) for m in b.merged_cells.ranges}:
        err(P, 'merges')
    for k in range(1, nc + 1):
        L = openpyxl.utils.get_column_letter(k)
        wa, wb_ = a.column_dimensions.get(L), b.column_dimensions.get(L)
        if (wa.width if wa is not None and wa.customWidth else None) != (wb_.width if wb_ is not None and wb_.customWidth else None):
            err(P, 'width', L)
    if a.freeze_panes != b.freeze_panes:
        err(P, 'freeze')
    # (b) rebuild
    r = m0
    for who in ('HORSE', 'JOCKEY'):
        tid = f'MATCH {who}'
        t24 = t24cells(a, who)
        exact, ratio = [], []
        for s in sky:
            for t in t24:
                low = min(s[5], t[6])
                if (s[3] == t[4] and s[4] == t[5]) or (s[3] != t[4] and d4(s[2]) == d4(t[3])):
                    exact.append(('1', 1.0, None, s, t, low))
                elif s[3] == t[4] and s[3] in ('whole', 'golden'):
                    x, y = (int(s[4]), int(t[5])) if s[3] == 'whole' else (int(s[4].split('×')[0]), int(t[5].split('×')[0]))
                    g = math.gcd(x, y)
                    if g >= 2:
                        ratio.append((f'{max(x, y) // g}/{min(x, y) // g}', max(x, y) / min(x, y), str(g) if s[3] == 'whole' else f'{g}×φ', s, t, low))
        # order: exact by lower score (2 dp shown; unrounded ties kept stable), ratio by ratio then lower score
        while r < amr and a.cell(row=r, column=1).value is None:
            r += 1
        if a.cell(row=r, column=1).value != tid:
            err(P, tid, 'title row', r); break
        title = a.cell(row=r, column=2).value
        if not title.endswith(f'EXACT {len(exact)} rows, RATIO {len(ratio)} rows (SKY block {len(sky)} scoring cells, T24 {who} {len(t24)})'):
            err(P, tid, 'title', title[-90:])
        r += 2
        got = []
        while a.cell(row=r, column=1).value == tid:
            got.append([a.cell(row=r, column=k) for k in range(1, 20)]); r += 1
        r += 1
        key = lambda e: (e[3][0], e[3][1], e[4][0], e[4][1], e[4][2])
        gkey = lambda g: (g[5].value, g[6].value, g[11].value, g[12].value, g[13].value)
        want = {('EXACT', key(e)): e for e in exact} | {('RATIO', key(e)): e for e in ratio}
        have = {(g[1].value, gkey(g)): g for g in got}
        if set(want) != set(have) or len(got) != len(want):
            err(P, tid, 'set', len(want), len(have), sorted(set(want) ^ set(have))[:3])
        for k_, e in want.items():
            g = have.get(k_)
            if g is None:
                continue
            pq, dec, fac, s, t, low = e
            exp = [tid, k_[0], pq, round(dec, 6), fac, s[0], s[1], s[2], s[3], s[4], round(s[5], 2), t[0], t[1], t[2], t[3], t[4], t[5],
                   round(t[6], 2), round(low, 2)]
            if [c.value for c in g] != exp:
                err(P, tid, 'row', k_, [c.value for c in g], exp)
            fills = [g[k].fill.start_color.rgb if g[k].fill.fill_type else None for k in (10, 17, 18)]
            # score fill = the source cell's fill (a T24 cell inside the conjunction range is red there: then the score colour; a shown 0.00 is
            # a real hit, light)
            tf = t[7] if t[7] != '00FF8080' else (colour(t[6]) or '00FFF8DC')
            lf = colour(low) or '00FFF8DC'
            if fills[0] != s[6] or fills[1] != tf or fills[2] not in (lf, tf, s[6]):
                err(P, tid, 'fills', k_, fills)
        for sec in ('EXACT', 'RATIO'):
            rows = [g for g in got if g[1].value == sec]
            if sec != 'EXACT' and any(x[1].value != 'RATIO' for x in got[len(got) - len(rows):]):
                err(P, tid, 'sections not in order')
            sk_ = [(-g[18].value,) if sec == 'EXACT' else (g[3].value, -g[18].value) for g in rows]
            if sk_ != sorted(sk_):
                err(P, tid, sec, 'order')
        print(f'{P} {tid}: SKY {len(sky)} x T24 {len(t24)} -> EXACT {len(exact)}, RATIO {len(ratio)} '
              f'(cross-family exact {sum(1 for e in exact if e[3][3] != e[4][4])})')
    if any(a.cell(row=x, column=k).value is not None for x in range(r, amr + 1) for k in range(1, 20)):
        err(P, 'rows after MATCH JOCKEY')
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
