"""Independent check of the nearest-target wording (24 Oct 2026; built on check_cells.py) of the half family + 4-digit rule (Eddie, 24 Oct 2026) in a jupiter_tables workbook, from POSITIONS.
usage: check_cells.py <workbook.xlsx> new|old [records.json]
Checks T1 / T2 (natal + SKY cells), T24 SKY / HORSE / JOCKEY (value, first comment line, fill, repeats column and title counts),
the SKY JUPITER 'SKY' block (value, +5, target, offset, score, fill, also, timing present iff score), T19 / SKY PAIRS leg cells.
Writes per-cell records (table, sheet, label, plane, value, best family / target or outside) to records.json for the before / after
classification (classify.py). Own code only (fam.py)."""
import sys, json, re, collections
import openpyxl
from wfam import outside, fams, target_text, t24_comment, colour, FILLHEX, ra_d, CONJ, nearest_form

path, mode = sys.argv[1], sys.argv[2]
NEW = mode == 'new'
recout = sys.argv[3] if len(sys.argv) > 3 else None
wb = openpyxl.load_workbook(path)
mism = collections.defaultdict(list)
nchk = collections.Counter()
records = []

# ---- POSITIONS
P = {}
for r in wb['POSITIONS'].iter_rows(min_row=5, values_only=True):
    if r[0] in (None, '') or r[2] not in ('S', 'H', 'J') or r[5] is None:
        continue
    P[(r[0], r[2], r[3])] = (r[5], r[6], r[7] or 0.0, r[8] or 0.0)


def pos(runner, ch, pt, m=0.0):
    ra, dec, rra, rdec = P[('SKY', 'S', pt)] if ch == 'S' else P[(runner, ch, pt)]
    return (ra + rra * m) % 360.0, dec + rdec * m


def dist(a, b, pl):
    if pl == 'RA':
        return ra_d(a[0], b[0])
    if pl == 'Dec':
        return abs(a[1] - b[1])
    return abs(abs(a[1]) - abs(b[1]))


def fillhex(c):
    return c.fill.fgColor.rgb if c.fill is not None and c.fill.fill_type else None


def bad(key, msg):
    mism[key].append(msg)


def close(a, b, tol=1.5e-6):
    return a is not None and b is not None and abs(a - b) <= tol


def also_text(fl):
    return '; '.join(f'{lab} ({fam}) {o} [{s:.2f}]' for s, fam, lab, t, o in fl) if fl else None


def check_group(key, ws, row, col, v0, v5, plane, timing_col=None, also=True):
    """8 cells value, +5, target, group, offset, score, arrow, also (1-based col of the value)"""
    nchk[key] += 1
    txt, off, sc, col_, fl = target_text(v0, plane, NEW)
    cv = ws.cell(row, col).value
    if not close(cv, round(v0, 6)):
        bad(key, f'{ws.title}!{ws.cell(row, col).coordinate} value {cv} != {round(v0, 6)}')
    if v5 is not None:
        c5 = ws.cell(row, col + 1).value
        if not close(c5, round(v5, 6), 3e-6):
            bad(key, f'{ws.title}!{ws.cell(row, col + 1).coordinate} +5 {c5} != {round(v5, 6)}')
    if ws.cell(row, col + 2).value != txt:
        bad(key, f'{ws.title}!{ws.cell(row, col + 2).coordinate} v={v0:.6f} target {ws.cell(row, col + 2).value!r} != {txt!r}')
    if ws.cell(row, col + 4).value != off:
        bad(key, f'{ws.title}!{ws.cell(row, col + 4).coordinate} v={v0:.6f} offset {ws.cell(row, col + 4).value!r} != {off!r}')
    cs = ws.cell(row, col + 5).value
    if (cs is None) != (sc is None) or (sc is not None and abs(cs - sc) > 0.0051):
        bad(key, f'{ws.title}!{ws.cell(row, col + 5).coordinate} v={v0:.6f} score {cs!r} != {sc!r}')
    fh = fillhex(ws.cell(row, col))
    if fh != FILLHEX[col_]:
        bad(key, f'{ws.title}!{ws.cell(row, col).coordinate} v={v0:.6f} fill {fh} != {FILLHEX[col_]}')
    if also:
        exp = also_text([(s, fam, lab, t, f'{v0 - t:+.5f}') for s, fam, lab, t in fl[1:]])
        if ws.cell(row, col + 7).value != exp:
            bad(key, f'{ws.title}!{ws.cell(row, col + 7).coordinate} v={v0:.6f} also {ws.cell(row, col + 7).value!r} != {exp!r}')
    if timing_col is not None:
        tv = ws.cell(row, timing_col).value
        if (sc is not None) != bool(tv):
            bad(key, f'{ws.title}!{ws.cell(row, timing_col).coordinate} v={v0:.6f} timing {tv!r} with score {sc!r}')
    return fl


def rec(table, sheet, label, plane, v, fl):
    b = fl[0] if fl else None
    o = None if b else outside(v, NEW)
    records.append([table, sheet, label, plane, round(v, 6), (b[1], b[2], round(b[0], 4)) if b else None, (o[0], o[1]) if o else None])


runners = [s for s in wb.sheetnames if re.fullmatch(r'P\d\d', s)]
STARS67 = None

# ---- (a) T1 / T2
for sh in runners:
    ws = wb[sh]
    hdr = None
    for row in range(1, ws.max_row + 1):
        a = ws.cell(row, 1).value
        if a == 'table' and ws.cell(row, 2).value == 'points' and ws.cell(row - 1, 1).value in ('T1', 'T2'):
            hdr = {ws.cell(row, c).value: c for c in range(1, ws.max_column + 1) if ws.cell(row, c).value}
            hdr['_skyra'] = [c for c in range(1, ws.max_column + 1) if ws.cell(row, c).value == 'SKY RA'][0]
            hdr['_skydec'] = [c for c in range(1, ws.max_column + 1) if ws.cell(row, c).value == 'SKY Dec'][0]
            continue
        if a not in ('T1', 'T2') or not re.match(r'[HJ] Jupiter → [HJ] ', str(ws.cell(row, 2).value or '')):
            continue
        if not isinstance(ws.cell(row, 11).value, (int, float)):
            continue
        lab = ws.cell(row, 2).value
        ch = lab[0]
        x = lab.split('→')[1].strip()[2:]
        jn, xn = pos(sh, ch, 'Jupiter'), pos(sh, ch, x)
        js0, xs0 = pos(sh, 'S', 'Jupiter'), pos(sh, 'S', x)
        js5, xs5 = pos(sh, 'S', 'Jupiter', 5), pos(sh, 'S', x, 5)
        for pl, col in (('RA', 3), ('Dec', 11)):
            if x == 'equator' and pl == 'RA':
                continue
            v = dist(jn, xn, pl)
            fl = check_group(f'{a} natal', ws, row, col, v, None, pl)
            rec(a, sh, lab, pl, v, fl)
            scol = hdr['_skyra'] if pl == 'RA' else hdr['_skydec']
            if ('SKY', 'S', x) in P:
                vs, vs5 = dist(js0, xs0, pl), dist(js5, xs5, pl)
                fl = check_group(f'{a} SKY', ws, row, scol, vs, vs5, pl, timing_col=scol + 8)
                rec(a + ' SKY', sh, lab, pl, vs, fl)

# ---- (c) SKY block
ws = wb['SKY JUPITER']
for row in range(5, ws.max_row + 1):
    if ws.cell(row, 1).value != 'SKY':
        if ws.cell(row, 1).value is None:
            break
        continue
    lab = ws.cell(row, 2).value
    x = lab.split('→')[1].strip()[2:]
    for pl, col in (('RA', 3), ('Dec', 12)):
        if x == 'equator' and pl == 'RA':
            continue
        v0 = dist(pos('SKY', 'S', 'Jupiter'), pos('SKY', 'S', x), pl)
        v5 = dist(pos('SKY', 'S', 'Jupiter', 5), pos('SKY', 'S', x, 5), pl)
        fl = check_group('SKY block', ws, row, col, v0, v5, pl, timing_col=col + 8)
        rec('SKY block', 'SKY JUPITER', lab, pl, v0, fl)

# ---- (b) T24 + (d) repeats
rep_summary = []
for sh in ['SKY JUPITER'] + runners:
    ws = wb[sh]
    runner = 'SKY' if sh == 'SKY JUPITER' else sh
    row = 1
    while row <= ws.max_row:
        b = str(ws.cell(row, 2).value or '')
        if ws.cell(row, 1).value == 'T24' and re.match(r'T24 (SKY|HORSE|JOCKEY) ', b):
            kind = b.split()[1]
            ch = {'SKY': 'S', 'HORSE': 'H', 'JOCKEY': 'J'}[kind]
            title_row = row
            h1 = {ws.cell(row + 1, c).value: c for c in range(1, ws.max_column + 1) if ws.cell(row + 1, c).value}
            cra, cramid, cdec, cdecmid, crep = h1['RA'], h1['RA midpoints'], h1['Dec'], h1['Dec midpoints'], h1['repeats']
            cols = [(ws.cell(row + 2, c).value, 'RA', c) for c in range(cra, cramid)] + \
                   [(ws.cell(row + 2, c).value, 'Dec', c) for c in range(cdec, cdecmid)]
            bodies = [ws.cell(row + 2, c).value for c in range(cra, cramid)]
            r = row + 3
            nrow = nrep = ntgt = 0
            key = f'T24 {kind}'
            while ws.cell(r, 1).value == 'T24' and str(ws.cell(r, 2).value or '')[:2] in ('S ', 'H ', 'J '):
                lab = ws.cell(r, 2).value
                st = lab[2:]
                nrow += 1
                best = {}
                for bod, pl, c in cols:
                    v = dist(pos(runner, ch, st), pos(runner, ch, bod), pl)
                    cell = ws.cell(r, c)
                    nchk[key] += 1
                    if not close(cell.value, round(v, 6)):
                        bad(key, f'{sh}!{cell.coordinate} value {cell.value} != {round(v, 6)}')
                    txt, colr, fl = t24_comment(v, pl, NEW)
                    first = cell.comment.text.split('\n')[0] if cell.comment else None
                    if first != txt:
                        bad(key, f'{sh}!{cell.coordinate} {lab} {bod} {pl} v={v:.6f} comment {first!r} != {txt!r}')
                    expf = FILLHEX['red'] if v < CONJ[pl] else FILLHEX[colr]
                    if fillhex(cell) != expf:
                        bad(key, f'{sh}!{cell.coordinate} {lab} {bod} {pl} v={v:.6f} fill {fillhex(cell)} != {expf}')
                    rec(key, sh, f'{lab} | {bod}', pl, v, fl)
                    if fl and fl[0][1] != 'conj' and v >= CONJ[pl]:
                        best[(bod, pl)] = (f'{fl[0][2]} {fl[0][1]}', fl[0][0])
                grp = {}
                for (bod, pl), (k, s) in best.items():
                    grp.setdefault(k, []).append((bod, pl, s))
                reps = []
                for k, cl in grp.items():
                    if len(cl) >= 2:
                        cl.sort(key=lambda z: (-z[2], ['RA', 'Dec'].index(z[1]), bodies.index(z[0])))
                        reps.append((k, cl))
                reps.sort(key=lambda kc: (-len(kc[1]), -kc[1][0][2]))
                exp = '; '.join(f'{k} ×{len(cl)} (' + ', '.join(f'{bb} {pp} ({ss:.2f})' for bb, pp, ss in cl) + ')' for k, cl in reps) or None
                nchk[key + ' repeats'] += 1
                if ws.cell(r, crep).value != exp:
                    bad(key + ' repeats', f'{sh}!{ws.cell(r, crep).coordinate} {lab} repeats {ws.cell(r, crep).value!r} != {exp!r}')
                if reps:
                    nrep += 1
                    ntgt += len(reps)
                    # repeat comment lines and dotted outline
                    for k, cl in reps:
                        for bb, pp, ss in cl:
                            c = [cc for b2, p2, cc in cols if b2 == bb and p2 == pp][0]
                            cell = ws.cell(r, c)
                            if f'\nrepeat: {k} ×{len(cl)} (with ' not in (cell.comment.text if cell.comment else ''):
                                bad(key + ' repeats', f'{sh}!{cell.coordinate} missing repeat line {k}')
                            if not (cell.border.left and cell.border.left.style in ('dotted', 'thick')):
                                bad(key + ' repeats', f'{sh}!{cell.coordinate} no outline')
                # no stray repeat line
                for bod, pl, c in cols:
                    cell = ws.cell(r, c)
                    t = cell.comment.text if cell.comment else ''
                    n_lines = t.count('\nrepeat: ')
                    n_exp = sum(1 for k, cl in reps for bb, pp, ss in cl if (bb, pp) == (bod, pl))
                    if n_lines != n_exp:
                        bad(key + ' repeats', f'{sh}!{cell.coordinate} repeat lines {n_lines} != {n_exp}')
                    if cell.border.left and cell.border.left.style == 'dotted' and n_exp == 0:
                        bad(key + ' repeats', f'{sh}!{cell.coordinate} dotted but no repeat')
                r += 1
            tt = ws.cell(title_row, 2).value
            exp_t = f'REPEATS (22 Oct 2026): {nrep} of {nrow} rows with a repeat, {ntgt} repeated targets'
            if not tt.endswith(exp_t):
                bad(key + ' repeats', f'{sh}!B{title_row} title ...{tt[-80:]!r} != ...{exp_t!r}')
            rep_summary.append((sh, kind, nrep, nrow, ntgt))
            row = r
        row += 1


# ---- (f) T19 / SKY PAIRS legs
def leg_check(key, ws, row, col, v, pl, plain=False):
    nchk[key] += 1
    cv = ws.cell(row, col).value
    if not close(cv, round(v, 6)):
        bad(key, f'{ws.title}!{ws.cell(row, col).coordinate} value {cv} != {round(v, 6)}')
    fl = fams(v, pl if pl in ('RA', 'Dec') else None, NEW)
    t = ws.cell(row, col + 1).value
    if not fl:
        if t != 'no family':
            bad(key, f'{ws.title}!{ws.cell(row, col + 1).coordinate} v={v:.6f} {pl} {t!r} != no family')
        if fillhex(ws.cell(row, col + 1)):
            bad(key, f'{ws.title}!{ws.cell(row, col + 1).coordinate} fill on no family')
        return
    s, fam, lab, tv = fl[0]
    exp = f'→ {lab} ({fam}, {s:.2f}) · '
    if not (t or '').startswith(exp):
        bad(key, f'{ws.title}!{ws.cell(row, col + 1).coordinate} v={v:.6f} {pl} {t!r} !startswith {exp!r}')
    if fillhex(ws.cell(row, col + 1)) != (None if plain else FILLHEX[colour(s)]):
        bad(key, f'{ws.title}!{ws.cell(row, col + 1).coordinate} family fill {fillhex(ws.cell(row, col + 1))} != {FILLHEX[colour(s)]}')


def pt(runner, s):
    ch, name = s.split(' ', 1)
    return pos(runner, ch, name)


for sh in ['SKY JUPITER'] + runners:
    ws = wb[sh]
    runner = 'SKY' if sh == 'SKY JUPITER' else sh
    tid = 'SKY PAIRS' if sh == 'SKY JUPITER' else 'T19'
    for row in range(1, ws.max_row + 1):
        if ws.cell(row, 1).value != tid or ' – ' not in str(ws.cell(row, 3).value or ''):
            continue
        a, b = ws.cell(row, 3).value.split(' – ')
        pl = ws.cell(row, 4).value
        sj = pos(runner, 'S', 'Jupiter')
        A, B = pt(runner, a), pt(runner, b)
        for col, v in ((5, dist(sj, A, pl)), (7, dist(sj, B, pl)), (9, dist(A, B, pl))):
            leg_check(f'{tid} legs', ws, row, col, v, pl, 'together' in str(ws.cell(row, 17).value or ''))
        if tid == 'T19' and isinstance(ws.cell(row, 23).value, (int, float)):
            As, Bs = pos(runner, 'S', a.split(' ', 1)[1]), pos(runner, 'S', b.split(' ', 1)[1])
            for col, v in ((23, dist(sj, As, pl)), (25, dist(sj, Bs, pl)), (27, dist(As, Bs, pl))):
                leg_check('T19 sky-side legs', ws, row, col, v, pl, 'together' in str(ws.cell(row, 35).value or ''))

print(path, mode)
for k in sorted(nchk):
    print(f'  {k:28s} cells {nchk[k]:7d}  mismatches {len(mism[k])}')
    for m in mism[k][:8]:
        print('     ', m)
print('  T24 repeats (sheet, block, rows with repeat, rows, targets):', rep_summary)
if recout:
    json.dump(records, open(recout, 'w'))

# ---- form counts over the recomputed cells (records with no family hit)
fc = collections.Counter()
for t, sh, lab, pl, v, b, o in records:
    if b is None and o is not None:
        fc[(t.split()[0] + (' SKY' if t.endswith('SKY') else ''), nearest_form(v)[0])] += 1
print('  recomputed no-hit cells by form:', sorted(fc.items()))
