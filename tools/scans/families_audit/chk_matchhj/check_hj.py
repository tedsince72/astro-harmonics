"""MATCH HORSE | JOCKEY (Eddie, 30 Oct 2026): checks one build by the new code against the build before (5ea09b4e), same race.
usage: check_hj.py <before.xlsx> <after.xlsx>
- every sheet: every cell of the before workbook identical in the after one (value, fill, font, border, number format, alignment, comment);
  merges = before + the two new ones per runner sheet; every column width and freeze pane identical;
- runner sheets: after the before's last row exactly two blank rows, then MATCH HORSE | JOCKEY, nothing after it;
- the new table rebuilt from the MATCH HORSE / MATCH JOCKEY rows on the same sheet (own code): every source row on its side exactly once, cell
  for cell (value and style; shared A-M from the source's own B-M, horse and jockey agreeing); key = sky cell, section, ratio, T24 family, T24
  target; pairing in source order (T24 score highest first, checked); lines, order (groups by sky score 2 dp, highest first, ties as both
  source tables; EXACT, RATIO by q, p, T24 target value), grey header rows A-AC with counts, the two header rows, title totals.
Prints per runner '<P>: lines n, keys both b / horse only h / jockey only j, sky cells k' and 'mismatches: n' last."""
import sys, re
import openpyxl

PHI = (1 + 5 ** 0.5) / 2
R2, SV = 2 ** 0.5, 1 + 2 ** 0.5
CONST = {'1.414': R2, '14.14': 10 * R2, '141.4': 100 * R2, '0.707': R2 / 2, '7.07': 10 * R2 / 2, '70.7': 100 * R2 / 2,
         '2.414': SV, '24.14': 10 * SV, '0.414': SV - 2, '4.14': 10 * (SV - 2), '41.4': 100 * (SV - 2)}
TID = 'MATCH HORSE | JOCKEY'
bad = []


def tval(fam, lab):
    if fam == 'golden':
        return int(lab[:-2]) * PHI
    if fam == 'phi power':
        m = re.fullmatch(r'(?:(\d+)×)?φ\^(-?\d+)', lab)
        return (int(m.group(1)) if m.group(1) else 1) * PHI ** int(m.group(2))
    if fam in ('sqrt2', 'silver'):
        return CONST[lab]
    return float(lab)


def st(c):
    b = c.border
    return (c.fill.fill_type, c.fill.start_color.rgb if c.fill.fill_type else None, c.font.bold, c.number_format,
            (b.left.style, b.right.style, b.top.style, b.bottom.style), c.alignment.horizontal, c.alignment.wrap_text)


def cv(c):
    return (c.value, st(c), c.comment.text if c.comment else None)


B, A = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
if B.sheetnames != A.sheetnames:
    bad.append(f'sheets {B.sheetnames} / {A.sheetnames}')
ncells = 0
for sh in B.sheetnames:
    wb_, wa = B[sh], A[sh]
    for r in wb_.iter_rows():
        for c in r:
            ncells += 1
            if cv(c) != cv(wa[c.coordinate]):
                bad.append(f'{sh}!{c.coordinate} changed: {c.value!r} -> {wa[c.coordinate].value!r}')
    if wb_.freeze_panes != wa.freeze_panes:
        bad.append(f'{sh} freeze {wb_.freeze_panes} -> {wa.freeze_panes}')
    keys = set(wb_.column_dimensions) | set(wa.column_dimensions)
    for L in keys:
        if wb_.column_dimensions[L].width != wa.column_dimensions[L].width:
            bad.append(f'{sh} width {L} {wb_.column_dimensions[L].width} -> {wa.column_dimensions[L].width}')
    mb, ma = {str(m) for m in wb_.merged_cells.ranges}, {str(m) for m in wa.merged_cells.ranges}
    extra = ma - mb
    if mb - ma:
        bad.append(f'{sh} merges lost {sorted(mb - ma)}')
    last = wb_.max_row
    if not re.fullmatch(r'P\d\d', sh):
        if wa.max_row != last or extra:
            bad.append(f'{sh}: rows / merges added ({wa.max_row} vs {last}; {sorted(extra)})')
        continue
    # ---- runner sheet: two blank rows, then the new table
    rows = [[wa.cell(row=r, column=k) for k in range(1, 31)] for r in range(last + 1, wa.max_row + 1)]
    if any(c.value is not None for c in rows[0] + rows[1]) or rows[2][0].value != TID:
        bad.append(f'{sh}: not two blank rows then {TID}')
    t0 = last + 3
    tab = [[wa.cell(row=r, column=k) for k in range(1, 31)] for r in range(t0, wa.max_row + 1)]
    while tab and all(c.value is None for c in tab[-1]):
        tab.pop()
    if any(r[0].value != TID for k, r in enumerate(tab) if k != 2):      # row 3 = column names ('table', as in MATCH HORSE)
        bad.append(f'{sh}: a row in the new table without its id in column A')
    if extra != {f'N{t0 + 1}:U{t0 + 1}', f'V{t0 + 1}:AC{t0 + 1}'}:
        bad.append(f'{sh}: new merges {sorted(extra)}')
    band, names = tab[1], tab[2]
    if band[13].value != 'HORSE' or band[21].value != 'JOCKEY' or any(c.value is not None for k, c in enumerate(band) if k not in (0, 13, 21)):
        bad.append(f'{sh}: band row {[c.value for c in band]}')
    r0 = next(r for r in range(1, last + 1) if wb_.cell(row=r, column=1).value == 'MATCH HORSE') + 1    # MATCH HORSE column-name row
    src_head = [wb_.cell(row=r0, column=k).value for k in range(1, 22)]
    if [c.value for c in names[:29]] != src_head[:13] + src_head[13:] * 2 or names[29].value is not None:
        bad.append(f'{sh}: column names {[c.value for c in names]}')
    # ---- the two source tables on the sheet (before rows = after rows)
    src = {'H': [], 'J': []}
    shead = {}
    for r in range(1, last + 1):
        a = wa.cell(row=r, column=1).value
        C = {'MATCH HORSE': 'H', 'MATCH JOCKEY': 'J'}.get(a)
        if not C:
            continue
        b = wa.cell(row=r, column=2).value
        cells = [wa.cell(row=r, column=k) for k in range(1, 22)]
        if b in ('EXACT', 'RATIO'):
            src[C].append(cells)
        elif isinstance(b, str) and ' — EXACT ' in b and cells[0].fill.start_color.rgb.endswith('D9D9D9'):
            g = (wa.cell(row=r + 1, column=8).value, wa.cell(row=r + 1, column=9).value)
            shead[(C, g)] = (b.split(' — EXACT ')[0], wa.cell(row=r + 1, column=13).value, len([1 for (c2, _) in shead if c2 == C]))
    # expected: groups -> keys -> sides
    exp, cnt = {}, {}
    for C in 'HJ':
        for cells in src[C]:
            v = [c.value for c in cells]
            g, k = (v[7], v[8]), (v[1], v[2], v[17], v[18])
            exp.setdefault(g, {}).setdefault(k, {'H': [], 'J': []})[C].append(cells)
            cnt.setdefault(g, {'H': [0, 0], 'J': [0, 0]})[C][v[1] == 'RATIO'] += 1
    for g, kk in exp.items():                              # pairing order: source order = T24 score non-increasing
        for k, d in kk.items():
            for C in 'HJ':
                sc = [c[19].value for c in d[C]]
                if sc != sorted(sc, reverse=True):
                    bad.append(f'{sh}: source {C} rows of key {g} {k} not by T24 score {sc}')
    # group order: sky score (2 dp) highest first; ties must agree with the source tables' own order
    pos = {C: {g: i for (c2, g), (_, _, i) in shead.items() if c2 == C} for C in 'HJ'}
    score = {g: next(shead[(C, g)][1] for C in 'HJ' if (C, g) in shead) for g in exp}

    def gkey(g):
        return -score[g]
    order = sorted(exp, key=gkey)
    ties = [(x, y) for x in exp for y in exp if x < y and score[x] == score[y]]
    for x, y in ties:
        ix, iy = order.index(x), order.index(y)
        for C in 'HJ':
            if x in pos[C] and y in pos[C] and (pos[C][x] < pos[C][y]) != (ix < iy):
                order[ix], order[iy] = order[iy], order[ix]
    pq = lambda s: tuple(int(z) for z in s.split('/')) if '/' in s else (int(s), 1)
    want = []                                              # expected lines: ('head', g) or (g, k, i, horse cells, jockey cells)
    for g in order:
        want.append(('head', g))
        for k in sorted(exp[g], key=lambda k: (k[0] != 'EXACT', pq(k[1])[1], pq(k[1])[0], tval(k[2], k[3]), k[2])):
            d = exp[g][k]
            for i in range(max(len(d['H']), len(d['J']))):
                want.append((g, k, i, d['H'][i] if i < len(d['H']) else None, d['J'][i] if i < len(d['J']) else None))
    body = tab[3:]
    if len(body) != len(want):
        bad.append(f'{sh}: {len(body)} rows, expected {len(want)}')
    used = {'H': 0, 'J': 0}
    for row, w in zip(body, want):
        if w[0] == 'head':
            g = w[1]
            h, j = cnt[g]['H'], cnt[g]['J']
            pre = next(shead[(C, g)][0] for C in 'HJ' if (C, g) in shead)
            txt = f'{pre} — EXACT {h[0]} | {j[0]}, RATIO {h[1]} | {j[1]}'
            for C, x in (('H', h), ('J', j)):
                if (C, g) in shead or sum(x):
                    hs = next(wa.cell(row=r, column=2).value for r in range(1, last + 1) if wa.cell(row=r, column=1).value == f"MATCH {'HORSE' if C == 'H' else 'JOCKEY'}"
                              and str(wa.cell(row=r, column=2).value).startswith(pre + ' — EXACT '))
                    if not hs.endswith(f'— EXACT {x[0]}, RATIO {x[1]}'):
                        bad.append(f'{sh}: counts of {g} {C} {x} vs source header {hs!r}')
            if row[1].value != txt or not row[1].font.bold or any(c.value is not None for k, c in enumerate(row) if k > 1):
                bad.append(f'{sh}: header {row[1].value!r} expected {txt!r}')
            if any(not (c.fill.fill_type and c.fill.start_color.rgb.endswith('D9D9D9')) for c in row[:29]) or row[29].fill.fill_type:
                bad.append(f'{sh}: header {g} not grey A-AC exactly')
            continue
        g, k, i, hc, jc = w
        for C, s, c0 in (('H', hc, 13), ('J', jc, 21)):
            if s is None:
                if any(c.value is not None or c.fill.fill_type for c in row[c0:c0 + 8]):
                    bad.append(f'{sh}: {g} {k} line {i}: {C} side should be empty')
                continue
            used[C] += 1
            for m in range(8):
                if (row[c0 + m].value, st(row[c0 + m])) != (s[13 + m].value, st(s[13 + m])):
                    bad.append(f'{sh}: {g} {k} line {i} {C} col {c0 + m + 1}: {row[c0 + m].value!r} vs source {s[13 + m].value!r}')
            for m in range(1, 13):
                if (row[m].value, st(row[m])) != (s[m].value, st(s[m])):
                    bad.append(f'{sh}: {g} {k} line {i} shared col {m + 1} vs {C} source: {row[m].value!r} / {s[m].value!r}')
        if row[29].value is not None:
            bad.append(f'{sh}: cell beyond AC')
    if used != {'H': len(src['H']), 'J': len(src['J'])}:
        bad.append(f"{sh}: rows used {used} vs source {len(src['H'])} / {len(src['J'])}")
    ks = [(bool(d['H']), bool(d['J'])) for kk in exp.values() for d in kk.values()]
    nb, nh, nj = ks.count((True, True)), ks.count((True, False)), ks.count((False, True))
    nl = len([w for w in want if w[0] != 'head'])
    tt = tab[0][1].value
    if not tt.endswith(f"{nl} lines, {len(ks)} keys: {nb} with both sides, {nh} horse only, {nj} jockey only; {len(exp)} sky cells "
                       f"(MATCH HORSE {len(src['H'])} rows, MATCH JOCKEY {len(src['J'])} rows)"):
        bad.append(f'{sh}: title totals {tt[-160:]!r}')
    print(f"{sh}: lines {nl}, keys {len(ks)}: both {nb} / horse only {nh} / jockey only {nj}, sky cells {len(exp)}, "
          f"rows H {len(src['H'])} J {len(src['J'])}, sky-score ties {len(ties)}")
print('cells compared:', ncells)
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
