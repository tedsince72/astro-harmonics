"""MATCH HORSE / MATCH JOCKEY (Eddie, 30 Oct 2026): checks one build against the build before, same race.
Tightened RATIO (Eddie, 30 Oct 2026, a76a3e99 -> now): whole kept only when the circle factor gcd(A, B, 360) >= 5 (+ columns 'circle factor',
'slice of 360' = 1/(360 / cf) after 'shared factor'); golden only when p, q <= 6. With a before build that already has MATCH tables (old
layout, 19 columns): before the MATCH title rows identical; every EXACT row = its before row (columns shifted by 2, new columns blank); every
RATIO row = a before RATIO row with the same cells (+ the new columns), i.e. the new RATIO rows are a subset kept by the new rules.
usage: check_match.py <before.xlsx> <after.xlsx>
(a) every sheet identical to before (value, fill, font, border, number format, comment; merges, widths, freeze), runner sheets apart from the
    two new blocks appended after T24 JOCKEY (MATCH HORSE, then MATCH JOCKEY);
(b) the MATCH rows rebuilt from the sheet cells themselves: SKY block cells (SKY JUPITER, value + target text 'target (family)' + score) and
    T24 HORSE / JOCKEY cells (value + comment 'target · family · offset · score'): scoring, not conjunction; T24 star rows x body columns (not
    S Jupiter), Jupiter rows except 'S Jupiter → S body'; pairs by the rules (exact same family + target, or across families the same 4
    significant digits of the two 6-dp values; ratio: whole / golden, gcd >= 2); every row's cells, order, fills, title counts.
Grouped by sky cell (Eddie, 30 Oct 2026, 8f42f04e -> now): one list per table, a grey header row (D9D9D9, A to U) above each sky cell's
rows '<relationship> <plane> <value> <target> <family> (<score>) — EXACT n, RATIO m'; groups by the sky score highest first (ties SKY block
order), inside a group EXACT (T24 score highest first, then T24 order) then RATIO (q, p, T24 score, T24 order); no blank rows between groups,
two between MATCH HORSE and MATCH JOCKEY; title ends '..., k sky cells (SKY block ...)'.
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
    bm0 = next((r for r in range(1, b.max_row + 1) if b.cell(row=r, column=1).value == 'MATCH HORSE'), None)
    if bm0 is not None and bm0 != m0:
        err(P, 'MATCH starts at another row', bm0, m0)
    for r in range(1, (bm0 - 1) if bm0 else b.max_row + 1):   # (a) everything before the MATCH blocks
        for k in range(1, nc + 1):
            if sig(a.cell(row=r, column=k)) != sig(b.cell(row=r, column=k)):
                err(P, 'cell', r, k)
    if bm0 is None and any(b.cell(row=r, column=1).value for r in range(m0, b.max_row + 1)):
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
                    exact.append(('1', 1.0, None, None, None, s, t, low))
                elif s[3] == t[4] and s[3] in ('whole', 'golden'):
                    x, y = (int(s[4]), int(t[5])) if s[3] == 'whole' else (int(s[4].split('×')[0]), int(t[5].split('×')[0]))
                    g = math.gcd(x, y)
                    p_, q_ = max(x, y) // g, min(x, y) // g
                    cf = math.gcd(math.gcd(x, y), 360)
                    if s[3] == 'whole' and cf >= 5:
                        ratio.append((f'{p_}/{q_}', max(x, y) / min(x, y), str(g), cf, f'1/{360 // cf}', s, t, low))
                    elif s[3] == 'golden' and g >= 2 and p_ <= 6 and q_ <= 6:
                        ratio.append((f'{p_}/{q_}', max(x, y) / min(x, y), f'{g}×φ', None, None, s, t, low))
        # order: exact by lower score (2 dp shown; unrounded ties kept stable), ratio by ratio then lower score
        while r < amr and a.cell(row=r, column=1).value is None:
            r += 1
        if a.cell(row=r, column=1).value != tid:
            err(P, tid, 'title row', r); break
        title = a.cell(row=r, column=2).value
        nw = sum(1 for e in ratio if e[3] is not None)
        nk = len({(e[5][0], e[5][1]) for e in exact + ratio})
        if not title.endswith(f'EXACT {len(exact)} rows, RATIO {len(ratio)} rows (whole {nw}, golden {len(ratio) - nw}), {nk} sky cells (SKY block '
                              f'{len(sky)} scoring cells, T24 {who} {len(t24)})') or 'circle factor gcd(A, B, 360) >= 5' not in title or 'p, q <= 6' not in title \
                or 'ORDER (30 Oct 2026, grouped by sky cell)' not in title:
            err(P, tid, 'title', title[-90:])
        r += 2
        got, heads, gof = [], [], []                       # data rows, header rows (row, text, cells), header index of each data row
        while a.cell(row=r, column=1).value == tid:
            cells = [a.cell(row=r, column=k) for k in range(1, 22)]
            if cells[1].value in ('EXACT', 'RATIO'):
                if not heads:
                    err(P, tid, 'data row before any header row', r)
                got.append(cells); gof.append(len(heads) - 1)
            else:
                heads.append((r, cells[1].value, cells))
            r += 1
        if who == 'HORSE' and not (a.cell(row=r, column=1).value is None and a.cell(row=r + 1, column=1).value is None
                                   and a.cell(row=r + 2, column=1).value == 'MATCH JOCKEY'):
            err(P, 'not two blank rows between MATCH HORSE and MATCH JOCKEY', r)
        r += 1
        # header rows and groups: each header names one sky cell, its rows follow it, counts, grey A to U, nothing else on it
        grp = {}
        for g, h in zip(got, gof):
            grp.setdefault(h, []).append(g)
        if len(heads) != nk or set(grp) != set(range(len(heads))):
            err(P, tid, 'header rows', len(heads), nk)
        sbyk = {(x[0], x[1]): x for x in sky}
        for h, (hr, txt, cells) in enumerate(heads):
            rows_ = grp.get(h, [])
            ks = {(g[7].value, g[8].value) for g in rows_}
            if len(ks) != 1:
                err(P, tid, 'group with several sky cells', hr); continue
            x = sbyk[ks.pop()]
            ne = sum(1 for g in rows_ if g[1].value == 'EXACT')
            want_t = f'{x[0]} {x[1]} {x[2]:.6f} {x[4]} {x[3]} ({x[5]:.2f}) — EXACT {ne}, RATIO {len(rows_) - ne}'
            if txt != want_t:
                err(P, tid, 'header text', hr, txt, want_t)
            if cells[0].value != tid or any(c.value is not None for c in cells[2:]) or not cells[1].font.b:
                err(P, tid, 'header cells', hr)
            if any(not (c.fill.fill_type == 'solid' and c.fill.start_color.rgb in ('00D9D9D9', 'FFD9D9D9')) for c in cells) or \
                    a.cell(row=hr, column=22).fill.fill_type:
                err(P, tid, 'header grey A to U', hr)
            if any(g[1].fill.fill_type for g in rows_):
                err(P, tid, 'data row grey', hr)
        key = lambda e: (e[5][0], e[5][1], e[6][0], e[6][1], e[6][2])
        gkey = lambda g: (g[7].value, g[8].value, g[13].value, g[14].value, g[15].value)
        want = {('EXACT', key(e)): e for e in exact} | {('RATIO', key(e)): e for e in ratio}
        have = {(g[1].value, gkey(g)): g for g in got}
        if set(want) != set(have) or len(got) != len(want):
            err(P, tid, 'set', len(want), len(have), sorted(set(want) ^ set(have))[:3])
        for k_, e in want.items():
            g = have.get(k_)
            if g is None:
                continue
            pq, dec, fac, cf, sl, s, t, low = e
            exp = [tid, k_[0], pq, round(dec, 6), fac, cf, sl, s[0], s[1], s[2], s[3], s[4], round(s[5], 2), t[0], t[1], t[2], t[3], t[4], t[5],
                   round(t[6], 2), round(low, 2)]
            if [c.value for c in g] != exp:
                err(P, tid, 'row', k_, [c.value for c in g], exp)
            fills = [g[k].fill.start_color.rgb if g[k].fill.fill_type else None for k in (12, 19, 20)]
            # score fill = the source cell's fill (a T24 cell inside the conjunction range is red there: then the score colour; a shown 0.00 is
            # a real hit, light)
            tf = t[7] if t[7] != '00FF8080' else (colour(t[6]) or '00FFF8DC')
            lf = colour(low) or '00FFF8DC'
            if fills[0] != s[6] or fills[1] != tf or fills[2] not in (lf, tf, s[6]):
                err(P, tid, 'fills', k_, fills)
        # order (Eddie, 30 Oct 2026, grouped): groups by sky score highest first (ties: SKY block order); inside a group EXACT (T24 score
        # highest first, then T24 order), then RATIO (q, p, T24 score highest first, T24 order) (shown 2-dp scores)
        sidx = {(x[0], x[1]): i for i, x in enumerate(sky)}
        tidx = {(x[0], x[1], x[2]): i for i, x in enumerate(t24)}
        qp = lambda g: tuple(reversed([int(z) for z in str(g[2].value).split('/')])) if '/' in str(g[2].value) else (0, 0)
        sk_ = [(-g[12].value, sidx[(g[7].value, g[8].value)], 0 if g[1].value == 'EXACT' else 1) + qp(g)
               + (-g[19].value, tidx[(g[13].value, g[14].value, g[15].value)]) for g in got]
        if sk_ != sorted(sk_):
            err(P, tid, 'order', next(i for i in range(len(sk_) - 1) if sk_[i] > sk_[i + 1]))
        if [gof[i] for i in range(len(gof))] != sorted(gof):
            err(P, tid, 'groups not contiguous')
        print(f'{P} {tid}: {len(heads)} sky-cell groups')
        # against the before MATCH block (old layout): EXACT rows identical after the 2-column shift, RATIO rows a subset
        newlay = bm0 is not None and b.cell(row=bm0 + 1, column=6).value == 'circle factor'
        if newlay:                                         # before already on the 21-column layout: the same rows, cell for cell, any order
            br = bm0
            while b.cell(row=br, column=1).value != tid:
                br += 1
            br, bro = br + 2, []
            while b.cell(row=br, column=1).value == tid:
                bro.append(tuple(sig(b.cell(row=br, column=k)) for k in range(1, 22))); br += 1
            if sorted(bro, key=str) != sorted([tuple(sig(c) for c in g) for g in got], key=str):
                err(P, tid, 'rows differ from before (as a set)')
            moved = sum(1 for x, g in zip(bro, got) if x != tuple(sig(c) for c in g))
            print(f'{P} {tid}: same {len(bro)} rows as before, {moved} in a new position')
        elif bm0 is not None:
            br, bt = bm0, None
            while bt != tid:
                while b.cell(row=br, column=1).value != tid:
                    br += 1
                bt = tid
            bro, br = [], br + 2
            while b.cell(row=br, column=1).value == tid:
                bro.append([b.cell(row=br, column=k) for k in range(1, 20)]); br += 1
            omap = lambda g: [sig(c) for c in g[:5]] + [sig(c) for c in g[7:21]]
            bex = [[sig(c) for c in x] for x in bro if x[1].value == 'EXACT']
            aex = [omap(g) for g in got if g[1].value == 'EXACT']
            if bex != aex or any(g[5].value is not None or g[6].value is not None for g in got if g[1].value == 'EXACT'):
                err(P, tid, 'EXACT rows differ from before')
            brat = {tuple(sig(c) for c in x) for x in bro if x[1].value == 'RATIO'}
            extra = [g for g in got if g[1].value == 'RATIO' and tuple(omap(g)) not in brat]
            if extra:
                err(P, tid, 'RATIO rows not in the before table', len(extra))
            print(f'{P} {tid}: before RATIO {len(brat)} -> {sum(1 for g in got if g[1].value == "RATIO")}')
        print(f'{P} {tid}: SKY {len(sky)} x T24 {len(t24)} -> EXACT {len(exact)}, RATIO {len(ratio)} (whole {nw}, golden {len(ratio) - nw}) '
              f'(cross-family exact {sum(1 for e in exact if e[5][3] != e[6][4])})')
    if any(a.cell(row=x, column=k).value is not None for x in range(r, amr + 1) for k in range(1, 22)):
        err(P, 'rows after MATCH JOCKEY')
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
