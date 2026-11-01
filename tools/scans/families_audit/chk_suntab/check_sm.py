"""SUN and MOON sections in the MATCH tables (Eddie, 1 Nov 2026): checks one build by the new code against the build before (6608676f),
same race.
usage: check_sm.py <before.xlsx> <after.xlsx>
1. Sheet order unchanged; every sheet but the runner sheets and SUMMARY identical (values, styles, comments, merges, widths, freeze); runner
   sheets identical before MATCH HORSE, widths and freeze identical, nothing after MATCH HORSE | JOCKEY, two blank rows between the tables.
2. Each MATCH table (MATCH HORSE, MATCH JOCKEY, MATCH HORSE | JOCKEY): title row (column A), header rows identical; then section bands
   JUPITER, SUN, MOON (column B, bold white on 595959, A to the last column); the JUPITER section = the before table's rows cell for cell.
3. Every section of MATCH HORSE / MATCH JOCKEY rebuilt here from the SKY block cells of SKY JUPITER / SKY SUN / SKY MOON and the T24 cells
   on the sheet (values, targets and families from the cells and comments; unrounded scores recomputed from POSITIONS with
   jupiter_tables.nearest): EXACT, RATIO, BODY, CONJ STAR rows, every cell, fills (score colours, light-blue ratio 1), number formats, order,
   block bands, group headers and counts, 'no matches', and the per-section title counts.
4. MATCH HORSE | JOCKEY rebuilt from the MATCH HORSE / JOCKEY rows on the sheet with the section in the key; title counts per section.
5. SUMMARY rebuilt from MATCH HORSE | JOCKEY with unrounded scores (section and block bands only when a line below them is shown).
Prints per runner 'P01 H J/S/M rows ... | J ... | HJ lines ... | summary ...' and 'mismatches: n' last."""
import math
import sys
import openpyxl
sys.path.insert(0, 'tools')
import jupiter_tables as JT                                 # noqa: E402  (nearest, star / body lists only)
import families                                             # noqa: E402

SEC = ('EXACT', 'RATIO', 'BODY', 'CONJ STAR')
BANDS = ('FIXED STARS', 'CONJUNCTIONS', 'OTHER BODIES')
CENTRES = ('Jupiter', 'Sun', 'Moon')
T24B = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno',
        'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto', 'Rahu', 'Ketu']
COL = {'green': '00C6EFCE', 'yellow': '00FFEB9C', 'light': '00FFF8DC'}
bad = []


def _crash(t, v, tb):                                       # a sheet the checker cannot read is a mismatch, not a pass
    import traceback
    traceback.print_exception(t, v, tb)
    for x in bad[:20]:
        print('  ', x)
    print(f'checker stopped: {t.__name__} {v} (layout not as expected)')
    print('mismatches: crash')


sys.excepthook = _crash


def sig(c):
    return (c.value, repr(c.font), repr(c.fill), repr(c.border), c.number_format, repr(c.alignment), c.comment.text if c.comment else None)


def vals(ws, r, n):
    return [ws.cell(row=r, column=k).value for k in range(1, n + 1)]


def last_row(ws):
    m = ws.max_row
    while m > 0 and all(c.value is None for c in ws[m]):
        m -= 1
    return m


def rgb(c):
    return c.fill.start_color.rgb if c.fill and c.fill.fill_type else None


def colour(s):
    return 'green' if s >= 80 else 'yellow' if s >= 50 else 'light'


B, A = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
RUN = [s for s in A.sheetnames if s.startswith('P') and s[1:].isdigit()]
if A.sheetnames != B.sheetnames:
    bad.append(f'sheets {A.sheetnames}')
for sh in [s for s in B.sheetnames if s not in RUN and s != 'SUMMARY']:
    b, a = B[sh], A[sh]
    if b.freeze_panes != a.freeze_panes or {str(m) for m in b.merged_cells.ranges} != {str(m) for m in a.merged_cells.ranges}:
        bad.append(f'{sh} freeze / merges')
    if {k: d.width for k, d in b.column_dimensions.items()} != {k: d.width for k, d in a.column_dimensions.items()}:
        bad.append(f'{sh} widths')
    for r in range(1, max(b.max_row, a.max_row) + 1):
        for k in range(1, max(b.max_column, a.max_column) + 1):
            if sig(b.cell(row=r, column=k)) != sig(a.cell(row=r, column=k)):
                bad.append(f'{sh} {r},{k}')
                break

POS = {}
for x in A['POSITIONS'].iter_rows(min_row=5, values_only=True):
    if x and x[0] and x[3] and isinstance(x[5], (int, float)):
        POS[(x[0], x[2], x[3])] = (x[5], x[6])


def dist(p, q, pl):
    if pl == 'RA':
        x = abs(p[0] - q[0]) % 360
        return min(x, 360 - x)
    return abs(p[1] - q[1])


def score(v, pl):
    ev = JT.nearest(v, 'dist', pl)[0]
    return ev['score'] if ev else None


def famtgt(t):
    """'12×φ (golden)' -> ('golden', '12×φ'); 'conj (conj)' -> ('conj', 'conj')"""
    t, f = t.rsplit(' (', 1)
    return f.rstrip(')'), t


# SKY block cells per centre: [(lab, plane, value, family, target, unrounded score, sheet score)] in SKY block order (RA before Dec of a row)
SKY = {}
for c in CENTRES:
    ws = A[f'SKY {c.upper()}']
    out = []
    for r in range(1, ws.max_row + 1):
        lab = ws.cell(row=r, column=2).value
        if ws.cell(row=r, column=1).value == 'SKY' and str(lab).startswith(f'S {c} → S '):
            x = lab.split(' → S ', 1)[1]
            for pl, k in (('RA', 3), ('Dec', 12)):
                v, t, s = ws.cell(row=r, column=k).value, ws.cell(row=r, column=k + 2).value, ws.cell(row=r, column=k + 5).value
                if isinstance(v, (int, float)) and isinstance(s, (int, float)):
                    f, tg = famtgt(t)
                    cen = POS[('SKY', 'S', c)]
                    su = score(abs(cen[1]), 'Dec') if x == 'equator' else score(dist(cen, POS[('SKY', 'S', x)], pl), pl)
                    if su is None or round(su, 2) != s:
                        bad.append(f'SKY {c} {lab} {pl}: recomputed {su} vs sheet {s}')
                    out.append((lab, pl, v, f, tg, su, s))
    SKY[c] = out


def t24_score(P, lab, body, pl):
    C = lab[0] if not lab.startswith('S ') else lab.split(' → ')[1][0]
    if lab.startswith(f'{C} Jupiter → '):
        a, b = POS[(P, C, 'Jupiter')], POS[(P, C, body)]
    elif lab.startswith('S Jupiter → '):
        a, b = POS[('SKY', 'S', 'Jupiter')], POS[(P, C, body)]
    elif lab.startswith('S body → '):
        a, b = POS[('SKY', 'S', body)], POS[(P, C, 'Jupiter')]
    else:
        a, b = POS[(P, C, lab.split(' ', 1)[1])], POS[(P, C, body)]
    return score(dist(a, b, pl), pl)


def t24(ws, P, who):
    """T24 HORSE / JOCKEY scoring cells in T24 order (rows, then RA columns, then Dec; not 'S Jupiter → S body', not the S Jupiter column)
    -> ([(row label, body, plane, value, family, target, unrounded score)], {row label: {(body, plane): cell}}, bodies)"""
    r0 = next(r for r in range(1, ws.max_row + 1) if ws.cell(row=r, column=1).value == 'T24'
              and str(ws.cell(row=r, column=2).value).startswith(f'T24 {who}'))
    cols, pl = [], None
    for k in range(3, ws.max_column + 1):
        h1, h2 = ws.cell(row=r0 + 1, column=k).value, ws.cell(row=r0 + 2, column=k).value
        if h1 in ('RA', 'Dec'):
            pl = h1
        if h2 in T24B and pl:
            cols.append((k, h2, pl))
        if isinstance(h1, str) and h1.endswith('midpoints'):
            if h1 == 'Dec midpoints':
                break
            pl = None
    lst, d = [], {}
    r = r0 + 3
    while ws.cell(row=r, column=1).value == 'T24':
        lab = ws.cell(row=r, column=2).value
        d.setdefault(lab, {})                              # every row label, also a star row with no scoring cell (CONJ STAR)
        if lab not in ('stars', 'S Jupiter → S body'):
            for k, b, pl in cols:
                c = ws.cell(row=r, column=k)
                if isinstance(c.value, (int, float)) and c.comment and not c.comment.text.startswith('nearest'):
                    f = c.comment.text.split('\n')[0].split(' · ')
                    fam = 'conj' if f[1].startswith('conjunction') else f[1]
                    su = t24_score(P, lab, b, pl)
                    if su is None or round(su, 2) != float(f[-1]):
                        bad.append(f'{P} T24 {who} {lab} {b} {pl}: recomputed {su} vs comment {f[-1]}')
                    cell = (lab, b, pl, c.value, fam, 'conj' if fam == 'conj' else f[0], su)
                    lst.append(cell)
                    d.setdefault(lab, {})[(b, pl)] = cell
        r += 1
    return lst, d, [b for k, b, pl in cols if pl == 'RA']


def block(lab, fam):
    x = lab.split(' → S ', 1)[1]
    star = x == 'equator' or (x not in JT.SKY_BODIES and x not in T24B)
    return (0 if star else 2) + (fam == 'conj')


def gk(t):
    return int(str(t).split('×')[0])


def expected(c, C, tl, td, bodies):
    """one section of MATCH HORSE / JOCKEY -> (rows [(section, sky, t24, p/q, decimal, factor, circle, slice)], groups in order, counts)"""
    sky = SKY[c]
    si = {(s[0], s[1]): i for i, s in enumerate(sky)}
    ti = {id(t): i for i, t in enumerate(tl)}
    ex, ra = [], []
    for s in sky:
        if s[3] == 'conj':
            continue
        for t in tl:
            if t[4] == 'conj':
                continue
            if (s[3] == t[4] and str(s[4]) == str(t[5])) or (s[3] != t[4] and families.digits4(s[2]) == families.digits4(t[3])):
                ex.append(('EXACT', s, t, '1', 1.0, None, None, None))
            elif s[3] == t[4] and s[3] in ('whole', 'golden'):
                a, b = (int(s[4]), int(t[5])) if s[3] == 'whole' else (gk(s[4]), gk(t[5]))
                g = math.gcd(a, b)
                hi, lo = max(a, b), min(a, b)
                if s[3] == 'whole':
                    cf = math.gcd(g, 360)
                    if cf >= 5:
                        ra.append(('RATIO', s, t, f'{hi // g}/{lo // g}', hi / lo, f'{g}', cf, f'1/{360 // cf}'))
                elif g >= 2 and hi // g <= 6 and lo // g <= 6:
                    ra.append(('RATIO', s, t, f'{hi // g}/{lo // g}', hi / lo, f'{g}×φ', None, None))
    pq = lambda r: tuple(int(z) for z in r[3].split('/')) if '/' in r[3] else (int(r[3]), 1)
    ex.sort(key=lambda r: (-r[2][6], ti[id(r[2])]))
    ra.sort(key=lambda r: (pq(r)[1], pq(r)[0], -r[2][6], ti[id(r[2])]))
    bo, cs = [], []
    pre = f'S {c} → S '
    for s in sky:
        if s[5] <= 50:
            continue
        x = s[0][len(pre):]
        if x in bodies and x != c and x != 'Moon':
            lab = f'{C} Jupiter → {C} body'
            for pl in ('RA', 'Dec'):
                t = td.get(lab, {}).get((x, pl))
                if t and t[6] > 50:
                    bo.append(('BODY', s, t, None, None, None, None, None))
        if s[3] == 'conj' and f'{C} {x}' in td:
            for lab in (f'{C} {x}', f'S Jupiter → {C} body'):
                for b in bodies:
                    if b == 'Moon':
                        continue
                    for pl in ('RA', 'Dec'):
                        t = td.get(lab, {}).get((b, pl))
                        if t and t[6] > 50:
                            cs.append(('CONJ STAR', s, t, None, None, None, None, None))
    groups = {}
    for r in ex + ra + bo + cs:                            # EXACT, RATIO, BODY, CONJ STAR; each already in its order
        groups.setdefault((r[1][0], r[1][1]), (r[1], []))[1].append(r)
    order = sorted(groups.values(), key=lambda g: (block(g[0][0], g[0][3]), -g[0][5], si[(g[0][0], g[0][1])]))
    blk = [block(g[0][0], g[0][3]) for g in order]
    cnt = (f'{c.upper()}: EXACT {len(ex)} rows, RATIO {len(ra)} rows (whole {sum(1 for r in ra if r[6] is not None)}, golden '
           f'{sum(1 for r in ra if r[6] is None)}), BODY {len(bo)} rows, CONJ STAR {len(cs)} rows, {len(order)} sky cells '
           f"({sum(1 for g in order if g[0][3] == 'conj')} conjunction) (SKY {c.upper()} block {sum(1 for s in sky if s[3] != 'conj')} scoring "
           f"cells without conjunction, {sum(1 for s in sky if s[3] == 'conj')} conjunction); groups: FIXED STARS {blk.count(0)}, CONJUNCTIONS "
           f'{blk.count(1)}, OTHER BODIES {blk.count(2) + blk.count(3)} ({blk.count(3)} of them body conjunctions, at the end)')
    return order, cnt, blk


def head(s):
    tf = 'conjunction' if s[3] == 'conj' else f'{s[4]} {s[3]}'
    return f'{s[0]} {s[1]} {s[2]:.6f} {tf} ({s[5]:.2f})'


def sections(ws, rows, n, tid):
    """rows of a table after the header rows -> {centre: [rows]}, checking the three section bands"""
    out, cur = {}, None
    for r in rows:
        b = ws.cell(row=r, column=2).value
        if b in ('JUPITER', 'SUN', 'MOON') and rgb(ws.cell(row=r, column=2)) == '00595959':
            cur = b
            out[cur] = []
            cl = [ws.cell(row=r, column=k) for k in range(1, n + 1)]
            if (cl[0].value != tid or any(rgb(x) != '00595959' for x in cl) or any(x.value is not None for x in cl[2:])
                    or not cl[1].font.b or cl[1].font.color is None or cl[1].font.color.rgb != '00FFFFFF'):
                bad.append(f'{ws.title} {tid} section band row {r} format')
        elif cur is None:
            bad.append(f'{ws.title} {tid} row {r} before the first section band')
        else:
            out[cur].append(r)
    if list(out) != ['JUPITER', 'SUN', 'MOON']:
        bad.append(f'{ws.title} {tid} sections {list(out)}')
    return out


def tables(ws):
    out = {}
    for r in range(1, ws.max_row + 1):
        a = ws.cell(row=r, column=1).value
        if a in ('MATCH HORSE', 'MATCH JOCKEY', 'MATCH HORSE | JOCKEY'):
            out.setdefault(a, []).append(r)
    return out


def tvalue(fam, lab):
    if fam == 'golden':
        return int(lab.split('×')[0]) * families.PHI
    if fam == 'phi power':
        f, p = lab.split('φ^')
        return (float(f.rstrip('×')) if f else 1.0) * families.PHI ** int(p)
    if fam in ('sqrt2', 'silver'):
        return dict(families.SQRT2_T if fam == 'sqrt2' else families.SILVER_T)[lab]
    return float(lab)


summ, report = {}, []
for P in RUN:
    b, a = B[P], A[P]
    if a.freeze_panes != b.freeze_panes or {k: d.width for k, d in b.column_dimensions.items()} != {k: d.width for k, d in a.column_dimensions.items()}:
        bad.append(f'{P} freeze / widths')
    tb, ta = tables(b), tables(a)
    s0 = tb['MATCH HORSE'][0]
    if s0 != ta['MATCH HORSE'][0]:
        bad.append(f'{P} MATCH start')
    for r in range(1, s0):
        if [sig(b.cell(row=r, column=k)) for k in range(1, b.max_column + 1)] != [sig(a.cell(row=r, column=k)) for k in range(1, b.max_column + 1)]:
            bad.append(f'{P} row {r} before MATCH')
    if last_row(a) != ta['MATCH HORSE | JOCKEY'][-1]:
        bad.append(f'{P} rows after the tables')
    if ta['MATCH JOCKEY'][0] != ta['MATCH HORSE'][-1] + 3 or ta['MATCH HORSE | JOCKEY'][0] != ta['MATCH JOCKEY'][-1] + 3:
        bad.append(f'{P} blank rows between tables')
    secrows, line = {}, [P]
    for tid, n, nh in (('MATCH HORSE', 21, 1), ('MATCH JOCKEY', 21, 1), ('MATCH HORSE | JOCKEY', 29, 2)):
        rb, ra = tb[tid], ta[tid]
        # header rows: before rb[0] + 1 .. (column names row has column A 'table'); after the same
        hb = list(range(rb[0] + 1, rb[0] + 1 + nh))
        ha = list(range(ra[0] + 1, ra[0] + 1 + nh))
        if [[sig(b.cell(row=x, column=k)) for k in range(1, n + 1)] for x in hb] != [[sig(a.cell(row=x, column=k)) for k in range(1, n + 1)] for x in ha]:
            bad.append(f'{P} {tid} header rows')
        body_b = [r for r in rb[1:] if r not in hb]
        body_a = [r for r in ra[1:] if r not in ha]
        if body_a and body_a[0] != ha[-1] + 1 or ra[-1] - ra[0] + 1 != len(ra) + 1:
            bad.append(f'{P} {tid} gaps')
        sec = sections(a, body_a, n, tid)
        secrows[tid] = sec
        jb, ja = [vals(b, r, n) for r in body_b], sec.get('JUPITER', [])
        if len(body_b) != len(ja) or any([sig(b.cell(row=x, column=k)) for k in range(1, n + 1)] != [sig(a.cell(row=y, column=k)) for k in range(1, n + 1)]
                                         for x, y in zip(body_b, ja)):
            bad.append(f'{P} {tid} JUPITER section differs from the before table ({len(body_b)} / {len(ja)} rows)')
    # 3. MATCH HORSE / JOCKEY rebuilt
    hjsrc = {}
    for C, who in (('H', 'HORSE'), ('J', 'JOCKEY')):
        tid = f'MATCH {who}'
        tl, td, bodies = t24(a, P, who)
        cnts, per = [], []
        for c in CENTRES:
            order, cnt, blk = expected(c, C, tl, td, bodies)
            cnts.append(cnt)
            rows = secrows[tid].get(c.upper(), [])
            want = []                                      # [(kind, ...)]
            if not order:
                want.append(('none',))
            band = None
            for (s, grp), bk in zip(order, blk):
                if min(bk, 2) != band:
                    band = min(bk, 2)
                    want.append(('band', BANDS[band]))
                n4 = [sum(1 for g in grp if g[0] == k) for k in SEC]
                want.append(('head', f'{head(s)} — EXACT {n4[0]}, RATIO {n4[1]}, BODY {n4[2]}, CONJ STAR {n4[3]}'))
                want += [('row', g) for g in grp]
            if len(want) != len(rows):
                bad.append(f'{P} {tid} {c}: {len(rows)} rows on the sheet, {len(want)} rebuilt')
            for w, r in zip(want, rows):
                v = vals(a, r, 21)
                cl = [a.cell(row=r, column=k) for k in range(1, 22)]
                if w[0] == 'none':
                    if v[:2] != [tid, 'no matches'] or any(x is not None for x in v[2:]) or any(rgb(x) for x in cl):
                        bad.append(f'{P} {tid} {c} no matches row {r}')
                elif w[0] == 'band':
                    if v[:2] != [tid, w[1]] or any(rgb(x) != '00A6A6A6' for x in cl) or not cl[1].font.b:
                        bad.append(f'{P} {tid} {c} band row {r}: {v[1]!r} want {w[1]!r}')
                elif w[0] == 'head':
                    if v[:2] != [tid, w[1]] or any(rgb(x) != '00D9D9D9' for x in cl) or not cl[1].font.b:
                        bad.append(f'{P} {tid} {c} head row {r}: {v[1]!r} want {w[1]!r}')
                else:
                    sec_, s, t, pq, dec, g, cf, sl = w[1]
                    low = min(s[5], t[6])
                    ev = [tid, sec_, pq, None if dec is None else round(dec, 6), g, cf, sl, s[0], s[1], s[2], s[3], str(s[4]), round(s[5], 2),
                          t[0], t[1], t[2], t[3], t[4], str(t[5]), round(t[6], 2), round(low, 2)]
                    got = v[:11] + [str(v[11])] + v[12:18] + [str(v[18])] + v[19:]
                    if got != ev:
                        bad.append(f'{P} {tid} {c} row {r}: {got} want {ev}')
                    fills = {13: COL[colour(s[5])], 20: COL[colour(t[6])], 21: COL[colour(low)], 3: '00BDD7EE' if pq == '1' else None}
                    for k in range(1, 22):
                        if rgb(cl[k - 1]) != fills.get(k):
                            bad.append(f'{P} {tid} {c} row {r} col {k} fill {rgb(cl[k - 1])} want {fills.get(k)}')
                    if any(cl[k - 1].number_format != '0.00' for k in (13, 20, 21)) or any(cl[k - 1].number_format != '0.000000' for k in (10, 17)):
                        bad.append(f'{P} {tid} {c} row {r} number formats')
                    hjsrc.setdefault(C, []).append((c.upper(), r, s, t))
            per.append(f"{sum(1 for w in want if w[0] == 'row')}")
        title = str(a.cell(row=ta[tid][0], column=2).value)
        if not all(x in title for x in cnts) or 'SKY SUN' not in title or 'SKY MOON' not in title or f"T24 {who} {sum(1 for t in tl if t[4] != 'conj')} scoring cells" not in title:
            bad.append(f'{P} {tid} title counts: {[x for x in cnts if x not in title]}')
        line.append(f"{C} {'/'.join(per)}")
    # 4. MATCH HORSE | JOCKEY rebuilt from the MATCH rows on the sheet
    tid = 'MATCH HORSE | JOCKEY'
    heads = {}
    for C, who in (('H', 'HORSE'), ('J', 'JOCKEY')):
        for c, rs in secrows[f'MATCH {who}'].items():
            for r in rs:
                v = a.cell(row=r, column=2).value
                if isinstance(v, str) and ' — EXACT ' in v:
                    heads[(c, a.cell(row=r + 1, column=8).value, a.cell(row=r + 1, column=9).value)] = v.split(' — EXACT ')[0]
    keys = {}
    for C in 'HJ':
        for c, r, s, t in hjsrc.get(C, []):
            v = vals(a, r, 21)
            k = (v[1], v[14], v[15]) if v[1] == 'BODY' else (v[1], 'S Jupiter' if str(v[13]).startswith('S Jupiter →') else 'star', v[14], v[15]) \
                if v[1] == 'CONJ STAR' else (v[1], v[2], v[17], str(v[18]))
            keys.setdefault((c, v[7], v[8]), {}).setdefault(k, {'H': [], 'J': []})[C].append((r, s, t))
    skyi = {(c.upper(), s[0], s[1]): (block(s[0], s[3]), -s[5], i) for c in CENTRES for i, s in enumerate(SKY[c])}
    pqk = lambda k: tuple(int(z) for z in k[1].split('/')) if '/' in k[1] else (int(k[1]), 1)
    korder = lambda k: ((SEC.index(k[0]), pqk(k)[1], pqk(k)[0], tvalue(k[2], k[3]), k[2]) if k[0] in ('EXACT', 'RATIO')
                        else (2, T24B.index(k[1]), ('RA', 'Dec').index(k[2])) if k[0] == 'BODY'
                        else (3, k[1] != 'star', T24B.index(k[2]), ('RA', 'Dec').index(k[3])))
    hjtitle = str(a.cell(row=ta[tid][0], column=2).value)
    hjexp, nl = {}, []
    for c in CENTRES:
        C_ = c.upper()
        gs = sorted([g for g in keys if g[0] == C_], key=lambda g: skyi[g])
        want = [] if gs else [('none',)]
        band = None
        for g in gs:
            if min(skyi[g][0], 2) != band:
                band = min(skyi[g][0], 2)
                want.append(('band', BANDS[band]))
            hc = [(sum(len(d['H']) for k, d in keys[g].items() if k[0] == s_), sum(len(d['J']) for k, d in keys[g].items() if k[0] == s_)) for s_ in SEC]
            want.append(('head', f'{heads[g]} — ' + ', '.join(f'{s_} {h} | {j}' for s_, (h, j) in zip(SEC, hc)), g))
            for k in sorted(keys[g], key=korder):
                d = keys[g][k]
                for i in range(max(len(d['H']), len(d['J']))):
                    want.append(('line', d['H'][i] if i < len(d['H']) else None, d['J'][i] if i < len(d['J']) else None))
        rows = secrows[tid].get(C_, [])
        if len(rows) != len(want):
            bad.append(f'{P} HJ {c}: {len(rows)} rows on the sheet, {len(want)} rebuilt')
        for w, r in zip(want, rows):
            cl = [a.cell(row=r, column=k) for k in range(1, 30)]
            if w[0] == 'none':
                if [x.value for x in cl[:2]] != [tid, 'no matches'] or any(x.value is not None for x in cl[2:]):
                    bad.append(f'{P} HJ {c} no matches row {r}')
            elif w[0] == 'band':
                if [x.value for x in cl[:2]] != [tid, w[1]] or any(rgb(x) != '00A6A6A6' for x in cl):
                    bad.append(f'{P} HJ {c} band row {r}')
            elif w[0] == 'head':
                if [x.value for x in cl[:2]] != [tid, w[1]] or any(rgb(x) != '00D9D9D9' for x in cl):
                    bad.append(f'{P} HJ {c} head row {r}: {cl[1].value!r} want {w[1]!r}')
            else:
                h, j = w[1], w[2]
                if cl[0].value != tid:
                    bad.append(f'{P} HJ {c} row {r} column A')
                src = h or j
                for k in range(2, 30):
                    if k < 14:
                        s_ = a.cell(row=src[0], column=k)
                    elif k < 22:
                        s_ = a.cell(row=h[0], column=k) if h else None
                    else:
                        s_ = a.cell(row=j[0], column=k - 8) if j else None
                    t_ = cl[k - 1]
                    if (sig(s_) if s_ is not None else (None,)) != (sig(t_) if s_ is not None else (t_.value,)):
                        bad.append(f'{P} HJ {c} row {r} col {k}')
                        break
                hjexp[r] = (src[1][5], h[2][6] if h else None, j[2][6] if j else None)
        sides = [(bool(d['H']), bool(d['J'])) for g in gs for d in keys[g].values()]
        nlines = sum(max(len(d['H']), len(d['J'])) for g in gs for d in keys[g].values())
        nl.append(str(nlines))
        txt = (f"{C_}: {nlines} lines, {len(sides)} keys: {sides.count((True, True))} with both sides, {sides.count((True, False))} horse only, "
               f"{sides.count((False, True))} jockey only")
        if txt not in hjtitle:
            bad.append(f'{P} HJ title: {txt!r} missing')
    line.append('HJ ' + '/'.join(nl))
    # 5. SUMMARY expected
    big = lambda x: x is not None and x > 50
    items = []
    for c in ('JUPITER', 'SUN', 'MOON'):
        items.append(('sect', next(r for r in range(ta[tid][0], ta[tid][-1] + 1) if a.cell(row=r, column=2).value == c
                                   and rgb(a.cell(row=r, column=2)) == '00595959'), None))
        for r in secrows[tid].get(c, []):
            v = a.cell(row=r, column=2).value
            if v in SEC:
                sk, h, j = hjexp[r]
                if big(sk) and (big(h) or big(j)):
                    items[-1][2].append(r)
            elif v in BANDS:
                items.append(('band', r, None))
            elif isinstance(v, str) and ' — EXACT ' in v:
                items.append(('group', r, []))
    exp = [('a1', 1)]
    if any(it[2] for it in items if it[0] == 'group'):
        exp += [('row', ta[tid][0] + 1), ('row', ta[tid][0] + 2)]
        for i, it in enumerate(items):
            if it[0] in ('sect', 'band'):
                stop = ('sect',) if it[0] == 'sect' else ('sect', 'band')
                nxt = next((k for k in range(i + 1, len(items)) if items[k][0] in stop), len(items))
                if any(items[k][2] for k in range(i + 1, nxt)):
                    exp.append(('row', it[1]))
                continue
            if not it[2]:
                continue
            sel = it[2]
            cnt = [(sum(1 for r in sel if a.cell(row=r, column=2).value == s_ and a.cell(row=r, column=14).value is not None),
                    sum(1 for r in sel if a.cell(row=r, column=2).value == s_ and a.cell(row=r, column=22).value is not None)) for s_ in SEC]
            exp.append(('head', it[1], a.cell(row=it[1], column=2).value.split(' — EXACT ')[0] + ' — ' + ', '.join(f'{s_} {h} | {j}' for s_, (h, j) in zip(SEC, cnt))))
            exp += [('row', r) for r in sel]
    else:
        exp.append(('none',))
    summ[P] = exp
    line.append(f"summary {sum(1 for e in exp if e[0] == 'row' and a.cell(row=e[1], column=2).value in SEC)} "
                f"(sections {[a.cell(row=e[1], column=2).value for e in exp if e[0] == 'row' and a.cell(row=e[1], column=2).value in ('JUPITER', 'SUN', 'MOON')]})")
    print(' | '.join(line))

S = A['SUMMARY']
r, merges = 1, set()
for P, exp in summ.items():
    a = A[P]
    for e in exp:
        if e[0] == 'a1':
            if sig(S.cell(row=r, column=1)) != sig(a.cell(row=1, column=1)):
                bad.append(f'SUMMARY {r} A1 of {P}')
        elif e[0] == 'none':
            if S.cell(row=r, column=1).value != 'no lines':
                bad.append(f'SUMMARY {r} no lines')
        else:
            for k in range(1, 30):
                s, t = a.cell(row=e[1], column=k), S.cell(row=r, column=k)
                if e[0] == 'head' and k == 2:
                    if t.value != e[2] or (repr(s.font), repr(s.fill)) != (repr(t.font), repr(t.fill)):
                        bad.append(f'SUMMARY {r} head {t.value!r} want {e[2]!r}')
                elif sig(s) != sig(t):
                    bad.append(f'SUMMARY {r},{k} ({P} row {e[1]}): {t.value!r} want {s.value!r}')
            if a.cell(row=e[1], column=14).value == 'HORSE':
                merges |= {f'N{r}:U{r}', f'V{r}:AC{r}'}
        r += 1
    for k in range(2):
        if any(S.cell(row=r + k, column=c).value is not None for c in range(1, 30)):
            bad.append(f'SUMMARY {r + k} not blank')
    r += 2
if last_row(S) != r - 3:
    bad.append(f'SUMMARY last row {last_row(S)} want {r - 3}')
if {str(m) for m in S.merged_cells.ranges} != merges:
    bad.append('SUMMARY merges')
if S.freeze_panes != B['SUMMARY'].freeze_panes:
    bad.append('SUMMARY freeze')
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
