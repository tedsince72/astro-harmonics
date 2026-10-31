"""Independent checker (31 Oct 2026) for the MATCH group order by block (FIXED STARS / CONJUNCTIONS / OTHER BODIES),
band rows, title group counts and the SUMMARY filter on unrounded scores.

Own code: does not import tools/jupiter_tables.py or tools/families.py.
Usage: python3 check32i.py <before.xlsx> <after.xlsx> [--quiet]
Whole, golden (4-digit rule) and conjunction scores recomputed unrounded from POSITIONS; other families (ninth, phi power,
sqrt2, silver) take the 2-dp score shown on the sheet and are flagged if within 0.01 of 50 or of a competing score.
"""
import sys, math, collections, copy
import openpyxl

PHI = (1 + 5 ** 0.5) / 2
BODIES = {'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres',
          'Pallas', 'Juno', 'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto',
          'Rahu', 'Ketu'}
TABLES = ('MATCH HORSE', 'MATCH JOCKEY', 'MATCH HORSE | JOCKEY')
NCOL = {'MATCH HORSE': 21, 'MATCH JOCKEY': 21, 'MATCH HORSE | JOCKEY': 29}
BAND_FILL = 'A6A6A6'
GREY = 'D9D9D9'
BLOCK_NAMES = ['FIXED STARS', 'CONJUNCTIONS', 'OTHER BODIES']

ERR = []
NOTES = []
FAMCOUNT = collections.Counter()
CLOSE50 = [99.0, '']


def err(*a):
    ERR.append(' '.join(str(x) for x in a))


def fnum(v):
    return None if v is None or v == '' else float(v)


def fillrgb(c):
    f = c.fill
    if f is None or f.fill_type is None:
        return None
    return str(f.fgColor.rgb)[-6:]


def sig(c):
    return (c.value, copy.copy(c.font), copy.copy(c.fill), copy.copy(c.border), copy.copy(c.alignment), c.number_format,
            c.comment.text if c.comment is not None else None)


def rowsig(ws, r, ncol):
    return tuple(sig(ws.cell(r, k)) for k in range(1, ncol + 1))


def rowvals(ws, r, ncol):
    return tuple(ws.cell(r, k).value for k in range(1, ncol + 1))


# ---------------- scoring (own) ----------------
def digits4(x):
    k = math.floor(math.log10(x))
    return math.floor(x / 10 ** (k - 3) + 1e-9), k


def fam_scores(v, plane):
    out = {}
    tol = 1.5 if plane == 'RA' else 0.3
    if v < tol:
        out['conj'] = (10 * (tol - v) / tol) ** 2
    t = round(v)
    if 1 <= t <= 200 and abs(v - t) < 0.02:
        out['whole'] = (10 * (0.02 - abs(v - t)) / 0.02) ** 2
    n = round(v / PHI)
    if n >= 1 and abs(v - n * PHI) < 0.03236 and v > 0:
        if digits4(v) == digits4(n * PHI):
            out['golden'] = (10 * (0.03236 - abs(v - n * PHI)) / 0.03236) ** 2
    return out


def true_score(v, plane, shown_fam, shown_score, where):
    """unrounded best score; for families not implemented use the shown score."""
    mine = fam_scores(v, plane)
    FAMCOUNT[(where.split()[0] == 'SKY', shown_fam in ('whole', 'golden', 'conj'))] += 1
    if shown_fam in ('whole', 'golden', 'conj'):
        if shown_fam not in mine:
            err('score: shown family', shown_fam, 'not reproduced', where, v)
            return shown_score, True
        s = mine[shown_fam]
        best = max(mine.values())
        if best > s + 1e-9:
            err('score: my best family differs', where, mine, shown_fam)
        if shown_score is not None and abs(round(s, 2) - shown_score) > 0.0051:
            err('score: rounding mismatch', where, s, shown_score)
        if abs(s - 50) < CLOSE50[0]:
            CLOSE50[0], CLOSE50[1] = abs(s - 50), '%s %.6f' % (where, s)
        return s, True
    # other family: shown score; my families must not beat it
    if mine and max(mine.values()) > (shown_score or 0) + 0.01:
        err('score: my family beats shown other family', where, mine, shown_fam, shown_score)
    if shown_score is not None and abs(shown_score - 50) <= 0.01:
        NOTES.append('other-family score within 0.01 of 50: %s %s' % (where, shown_score))
    return shown_score, False


# ---------------- positions ----------------
def load_positions(wb):
    ws = wb['POSITIONS']
    P = {}
    r = 5
    while ws.cell(r, 1).value is not None or ws.cell(r + 1, 1).value is not None:
        who, ch, name, ra, dec = (ws.cell(r, 1).value, ws.cell(r, 3).value, ws.cell(r, 4).value,
                                  ws.cell(r, 6).value, ws.cell(r, 7).value)
        if who is not None and ch in ('S', 'H', 'J') and isinstance(ra, (int, float)):
            P[(who if ch != 'S' else 'SKY', ch, name)] = (ra, dec)
        r += 1
    return P


def dist(a, b, plane):
    if plane == 'RA':
        d = abs(a[0] - b[0]) % 360
        return min(d, 360 - d)
    return abs(a[1] - b[1])


def pos(P, runner, ch, name):
    return P[('SKY', 'S', name)] if ch == 'S' else P[(runner, ch, name)]


def sky_dist(P, rel, plane):
    x = rel.split('→ S ', 1)[1]
    sj = P[('SKY', 'S', 'Jupiter')]
    if x == 'equator':
        return abs(sj[1])
    return dist(sj, P[('SKY', 'S', x)], plane)


def t24_dist(P, runner, label, body, plane):
    if '→' in label:
        a, b = [s.strip() for s in label.split('→')]
        ca, na = a.split(' ', 1)
        cb, nb = b.split(' ', 1)
        na = body if na == 'body' else na
        nb = body if nb == 'body' else nb
        return dist(pos(P, runner, ca, na), pos(P, runner, cb, nb), plane)
    ch, star = label.split(' ', 1)
    return dist(pos(P, runner, ch, star), pos(P, runner, ch, body), plane)


# ---------------- sky block ----------------
def load_sky(wb, P):
    ws = wb['SKY JUPITER']
    r = 1
    while not (ws.cell(r, 1).value == 'table' and ws.cell(r, 2).value == 'points'):
        r += 1
    r += 1
    order = {}
    info = {}
    i = 0
    while ws.cell(r, 1).value == 'SKY':
        rel = ws.cell(r, 2).value
        for plane, cv, ct, cs in (('RA', 3, 5, 8), ('Dec', 12, 14, 17)):
            order[(rel, plane)] = (i, 0 if plane == 'RA' else 1)
            v = fnum(ws.cell(r, cv).value)
            tgt = ws.cell(r, ct).value
            sc = fnum(ws.cell(r, cs).value)
            if v is None:
                continue
            d = sky_dist(P, rel, plane)
            if abs(d - v) > 1.5e-6:
                err('sky value mismatch', rel, plane, d, v)
            if sc is None:
                continue
            fam = str(tgt).rsplit('(', 1)[1].rstrip(')')
            fam = {'phi power': 'phi power'}.get(fam, fam)
            s, own = true_score(d, plane, fam, sc, 'SKY %s %s' % (rel, plane))
            info[(rel, plane)] = dict(score=s, fam=fam, own=own, shown=sc, value=d)
        r += 1
        i += 1
    return order, info


# ---------------- table parsing ----------------
def find_titles(ws):
    t = {}
    for r in range(1, ws.max_row + 1):
        a = ws.cell(r, 1).value
        b = ws.cell(r, 2).value
        if a in TABLES and isinstance(b, str) and b.startswith(a + ' ('):
            t[a] = r
    return t


def parse_table(ws, tid, r0):
    """returns dict: title row, header rows, items list [(kind, row)], end row (exclusive)"""
    nh = 2 if tid == 'MATCH HORSE | JOCKEY' else 1
    r = r0 + 1 + nh
    items = []
    while ws.cell(r, 1).value is not None:
        if ws.cell(r, 1).value != tid:
            err(ws.title, tid, 'row', r, 'col A not table id', ws.cell(r, 1).value)
        f = fillrgb(ws.cell(r, 1))
        if f == BAND_FILL:
            items.append(('band', r))
        elif f == GREY:
            items.append(('group', r))
        else:
            items.append(('data', r))
        r += 1
    return dict(title=r0, nh=nh, items=items, end=r)


def groups_of(ws, tab, ncol):
    """list of dict(key, header row, data rows) and bands [(pos index, row)]"""
    groups = []
    bands = []
    for kind, r in tab['items']:
        if kind == 'band':
            bands.append((len(groups), r))
        elif kind == 'group':
            groups.append(dict(hrow=r, rows=[]))
        else:
            if not groups:
                err(ws.title, 'data row before any group', r)
                continue
            groups[-1]['rows'].append(r)
    for g in groups:
        r = g['rows'][0]
        g['key'] = (ws.cell(r, 8).value, ws.cell(r, 9).value)
        for rr in g['rows']:
            if (ws.cell(rr, 8).value, ws.cell(rr, 9).value) != g['key']:
                err(ws.title, 'mixed sky cell in group', g['hrow'], rr)
    return groups, bands


def block_of(key, sky):
    rel, plane = key
    x = rel.split('→ S ', 1)[1]
    conj = sky[key]['fam'] == 'conj'
    if x in BODIES:
        return 3 if conj else 2
    return 1 if conj else 0


def expected_order(keys, sky, order):
    return sorted(keys, key=lambda k: (block_of(k, sky), -sky[k]['score'], order[k]))


def check_bands(ws, tid, groups, bands, sky, ncol):
    exp = []
    seen = set()
    for i, g in enumerate(groups):
        b = block_of(g['key'], sky)
        bn = min(b, 2)
        if bn not in seen:
            seen.add(bn)
            exp.append((i, BLOCK_NAMES[bn]))
    got = [(i, ws.cell(r, 2).value) for i, r in bands]
    if got != exp:
        err(ws.title, tid, 'bands', got, 'expected', exp)
    for i, r in bands:
        c = ws.cell(r, 2)
        if not c.font.b:
            err(ws.title, tid, 'band not bold', r)
        if ws.cell(r, 1).value != tid:
            err(ws.title, tid, 'band col A', r)
        for k in range(1, ncol + 1):
            if fillrgb(ws.cell(r, k)) != BAND_FILL:
                err(ws.title, tid, 'band fill missing', r, k)
                break
        if fillrgb(ws.cell(r, ncol + 1)) == BAND_FILL:
            err(ws.title, tid, 'band fill beyond last column', r)
        for k in range(3, ncol + 1):
            if ws.cell(r, k).value is not None:
                err(ws.title, tid, 'band has extra text', r, k)
    return exp


def block_counts(groups, sky):
    c = collections.Counter(block_of(g['key'], sky) for g in groups)
    return c[0], c[1], c[2] + c[3], c[3]


# ---------------- main per workbook pair ----------------
def check(before, after, quiet=False):
    wb0 = openpyxl.load_workbook(before)
    wb1 = openpyxl.load_workbook(after)
    if wb0.sheetnames != wb1.sheetnames:
        err('sheet names differ', wb0.sheetnames, wb1.sheetnames)
    P = load_positions(wb1)
    order, sky = load_sky(wb1, P)
    report = []
    # identical sheets
    for sn in ('POSITIONS', 'SKY JUPITER'):
        a, b = wb0[sn], wb1[sn]
        mr = max(a.max_row, b.max_row)
        mc = max(a.max_column, b.max_column)
        for r in range(1, mr + 1):
            if rowsig(a, r, mc) != rowsig(b, r, mc):
                err(sn, 'row differs', r)
    runners = [s for s in wb1.sheetnames if s not in ('POSITIONS', 'SKY JUPITER', 'SUMMARY')]
    hj_after = {}
    for sn in runners:
        a, b = wb0[sn], wb1[sn]
        ta, tb = find_titles(a), find_titles(b)
        if set(ta) != set(TABLES) or set(tb) != set(TABLES):
            err(sn, 'tables missing', ta, tb)
            continue
        first = ta['MATCH HORSE']
        if tb['MATCH HORSE'] != first:
            err(sn, 'MATCH HORSE moved')
        mc = max(a.max_column, b.max_column)
        for r in range(1, first):
            if rowsig(a, r, mc) != rowsig(b, r, mc):
                err(sn, 'row before MATCH differs', r)
        # widths, freeze
        if a.freeze_panes != b.freeze_panes:
            err(sn, 'freeze differs')
        for col in set(a.column_dimensions) | set(b.column_dimensions):
            if a.column_dimensions[col].width != b.column_dimensions[col].width:
                err(sn, 'width differs', col)
        tabs0 = {t: parse_table(a, t, ta[t]) for t in TABLES}
        tabs1 = {t: parse_table(b, t, tb[t]) for t in TABLES}
        # gaps between tables / after last
        for t0, t1 in (('MATCH HORSE', 'MATCH JOCKEY'), ('MATCH JOCKEY', 'MATCH HORSE | JOCKEY')):
            g0 = ta[t1] - tabs0[t0]['end']
            g1 = tb[t1] - tabs1[t0]['end']
            if g0 != g1:
                err(sn, 'gap differs', t0, g0, g1)
        e0, e1 = tabs0['MATCH HORSE | JOCKEY']['end'], tabs1['MATCH HORSE | JOCKEY']['end']
        if a.max_row - e0 != b.max_row - e1:
            err(sn, 'rows after last table differ', a.max_row - e0, b.max_row - e1)
        for k in range(0, a.max_row - e0 + 1):
            if rowsig(a, e0 + k, mc) != rowsig(b, e1 + k, mc):
                err(sn, 'row after tables differs', e1 + k)
        # merges (map to table + offset)
        def mmap(ws, titles, tabs):
            out = []
            for m in ws.merged_cells.ranges:
                r = m.min_row
                if r < first:
                    out.append(('pre', str(m)))
                    continue
                tid = max((t for t in TABLES if titles[t] <= r), key=lambda t: titles[t])
                off = r - titles[tid]
                if off > tabs[tid]['nh']:
                    err(ws.title, 'merge inside table body', str(m))
                out.append((tid, off, m.min_col, m.max_col, m.max_row - m.min_row))
            return sorted(out, key=str)
        if mmap(a, ta, tabs0) != mmap(b, tb, tabs1):
            err(sn, 'merged ranges differ')
        line = []
        for t in TABLES:
            nc = NCOL[t]
            T0, T1 = tabs0[t], tabs1[t]
            # header rows identical, title: compare separately
            for k in range(1, T0['nh'] + 1):
                if rowsig(a, T0['title'] + k, nc + 2) != rowsig(b, T1['title'] + k, nc + 2):
                    err(sn, t, 'header row differs', k)
            tit0, tit1 = a.cell(T0['title'], 2).value, b.cell(T1['title'], 2).value
            g0, bd0 = groups_of(a, T0, nc)
            g1, bd1 = groups_of(b, T1, nc)
            if bd0:
                err(sn, t, 'before has band rows?')
            # group contents identical
            d0 = {g['key']: g for g in g0}
            d1 = {g['key']: g for g in g1}
            if set(d0) != set(d1) or len(d0) != len(g0) or len(d1) != len(g1):
                err(sn, t, 'group set differs', set(d0) ^ set(d1))
            for k in d0.keys() & d1.keys():
                x, y = d0[k], d1[k]
                if rowsig(a, x['hrow'], nc + 1) != rowsig(b, y['hrow'], nc + 1):
                    err(sn, t, 'group header differs', k)
                if len(x['rows']) != len(y['rows']):
                    err(sn, t, 'group row count differs', k)
                    continue
                for r0, r1 in zip(x['rows'], y['rows']):
                    if rowsig(a, r0, nc + 1) != rowsig(b, r1, nc + 1):
                        err(sn, t, 'data row differs', k, r0, r1)
            # order
            keys = [g['key'] for g in g1]
            for k in keys:
                if k not in sky:
                    err(sn, t, 'group sky cell not a scoring SKY cell', k)
            keys = [k for k in keys if k in sky]
            exp = expected_order(keys, sky, order)
            if exp != keys:
                err(sn, t, 'group order differs', [(i, k, e) for i, (k, e) in enumerate(zip(keys, exp)) if k != e][:3])
            # group header score = sky score
            for g in g1:
                txt = b.cell(g['hrow'], 2).value
                if g['key'] in sky and ('(%.2f)' % sky[g['key']]['score']) not in txt:
                    err(sn, t, 'group header score', txt, sky[g['key']]['score'])
            check_bands(b, t, g1, bd1, sky, nc)
            # gap check: ties at 2 dp inside a block
            for i in range(len(exp) - 1):
                p, q = exp[i], exp[i + 1]
                if block_of(p, sky) == block_of(q, sky) and abs(sky[p]['score'] - sky[q]['score']) < 0.01:
                    NOTES.append('%s %s close sky scores in one block: %s %s / %s %s' % (sn, t, p, sky[p]['score'], q, sky[q]['score']))
            fs, cj, ob, bc = block_counts(g1, sky)
            want = 'groups: FIXED STARS %d, CONJUNCTIONS %d, OTHER BODIES %d (%d of them body conjunctions, at the end)' % (fs, cj, ob, bc)
            if want not in tit1:
                err(sn, t, 'title groups sentence', want)
            if 'ORDER (30 Oct' in tit1 or ('ORDER' in tit1 and '31 Oct 2026' not in tit1.split('ORDER', 1)[1][:30]):
                err(sn, t, 'title ORDER sentence not replaced')
            line.append('%s %d/%d/%d+%d' % ({'MATCH HORSE': 'H', 'MATCH JOCKEY': 'J', 'MATCH HORSE | JOCKEY': 'HJ'}[t], fs, cj, ob - bc, bc))
            if t == 'MATCH HORSE | JOCKEY':
                hj_after[sn] = (b, T1, g1, bd1)
        report.append('%s %s' % (sn, ' '.join(line)))
    # ---------------- SUMMARY ----------------
    s0, s1 = wb0['SUMMARY'], wb1['SUMMARY']
    exp_rows = []   # list of ('copy', ws, row) | ('hdr', ws, row, text) | ('blank',) | ('nolines', a1)
    exp_merges = []
    disagree = []
    shown_lines = {}
    nlines_rep = []
    for sn in runners:
        b, T1, g1, bd1 = hj_after[sn]
        a1_idx = len(exp_rows)
        exp_rows.append(('a1', b, 1))
        for k in (1, 2):
            exp_rows.append(('copy', b, T1['title'] + k))
        kept_total = 0
        band_at = {i: r for i, r in bd1}
        cur_band = None
        out_groups = []
        for i, g in enumerate(g1):
            if i in band_at:
                cur_band = band_at[i]
            sk = g['key']
            s_true = sky[sk]['score']
            kept = []
            for r in g['rows']:
                vals = [b.cell(r, c).value for c in range(1, 30)]
                shown_sky = fnum(vals[12])
                sides = []
                sides2 = []
                for off, lab in ((13, 'H'), (21, 'J')):
                    if vals[off] is None:
                        sides.append(None)
                        sides2.append(None)
                        continue
                    label, body, plane = vals[off], vals[off + 1], vals[off + 2]
                    v = fnum(vals[off + 3])
                    fam = vals[off + 4]
                    sc = fnum(vals[off + 6])
                    d = t24_dist(P, sn, label, body, plane)
                    if abs(d - v) > 1.5e-6:
                        err(sn, 'T24 value mismatch', r, label, body, plane, d, v)
                    ts, _ = true_score(d, plane, fam, sc, '%s r%d %s %s %s' % (sn, r, label, body, plane))
                    sides.append(ts)
                    sides2.append(sc)
                keep = s_true > 50 and any(x is not None and x > 50 for x in sides)
                keep2 = shown_sky > 50 and any(x is not None and x > 50 for x in sides2)
                if keep != keep2:
                    disagree.append((sn, r, sk, s_true, sides, shown_sky, sides2, keep))
                if keep:
                    kept.append(r)
            if kept:
                out_groups.append((cur_band, g, kept))
        last_band = None
        for band, g, kept in out_groups:
            if band != last_band:
                exp_rows.append(('copy', b, band))
                last_band = band
            cnt = collections.Counter()
            for r in kept:
                sec = b.cell(r, 2).value
                if b.cell(r, 14).value is not None:
                    cnt[(sec, 'h')] += 1
                if b.cell(r, 22).value is not None:
                    cnt[(sec, 'j')] += 1
            head = b.cell(g['hrow'], 2).value.split(' — ')[0]
            txt = head + ' — ' + ', '.join('%s %d | %d' % (s, cnt[(s, 'h')], cnt[(s, 'j')])
                                            for s in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR'))
            exp_rows.append(('hdr', b, g['hrow'], txt))
            for r in kept:
                exp_rows.append(('copy', b, r))
                kept_total += 1
        if kept_total == 0:
            del exp_rows[a1_idx:]
            exp_rows.append(('a1', b, 1))
            exp_rows.append(('nolines',))
        nlines_rep.append('%s %d' % (sn, kept_total))
        shown_lines[sn] = kept_total
        exp_rows.append(('blank',))
        exp_rows.append(('blank',))
    # compare SUMMARY
    r = 1
    for e in exp_rows:
        if e[0] == 'blank':
            if any(s1.cell(r, k).value is not None for k in range(1, 30)):
                err('SUMMARY row', r, 'expected blank')
        elif e[0] == 'nolines':
            vals = [s1.cell(r, k).value for k in range(1, 30)]
            if not any(isinstance(v, str) and 'no lines' in v for v in vals):
                err('SUMMARY row', r, 'expected no lines', vals[:3])
        elif e[0] == 'a1':
            if sig(s1.cell(r, 1)) != sig(e[1].cell(1, 1)):
                err('SUMMARY row', r, 'A1 line differs', s1.cell(r, 1).value)
        elif e[0] == 'copy':
            if rowsig(s1, r, 30) != rowsig(e[1], e[2], 30):
                err('SUMMARY row', r, 'differs from', e[1].title, e[2], s1.cell(r, 2).value)
        elif e[0] == 'hdr':
            if s1.cell(r, 2).value != e[3]:
                err('SUMMARY row', r, 'header text', s1.cell(r, 2).value, 'expected', e[3])
            exp_sig = list(rowsig(e[1], e[2], 30))
            got = list(rowsig(s1, r, 30))
            exp_sig[1] = exp_sig[1][1:]
            got[1] = got[1][1:]
            if got != exp_sig:
                err('SUMMARY row', r, 'header style differs')
        r += 1
    while r <= s1.max_row:
        if any(s1.cell(r, k).value is not None for k in range(1, 30)):
            err('SUMMARY extra row', r, s1.cell(r, 1).value, s1.cell(r, 2).value)
        r += 1
    # merges on SUMMARY: N-U and V-AC on each copied band header row (the HJ header row 1)
    exp_m = set()
    r = 1
    for e in exp_rows:
        if e[0] == 'copy' and e[2] == hj_after[e[1].title][1]['title'] + 1:
            exp_m.add('N%d:U%d' % (r, r))
            exp_m.add('V%d:AC%d' % (r, r))
        r += 1
    got_m = {str(m) for m in s1.merged_cells.ranges}
    if got_m != exp_m:
        err('SUMMARY merges', sorted(got_m ^ exp_m)[:6])
    if s1.freeze_panes not in (None, 'A1'):
        err('SUMMARY freeze', s1.freeze_panes)
    for col in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        pass
    p1 = wb1[runners[0]]
    from openpyxl.utils import get_column_letter
    for k in range(1, 30):
        L = get_column_letter(k)
        if s1.column_dimensions[L].width != p1.column_dimensions[L].width:
            err('SUMMARY width', L)
    # SUMMARY before vs after lines (multiset of data-line signatures)
    def lines(ws):
        out = collections.Counter()
        for rr in range(1, ws.max_row + 1):
            if ws.cell(rr, 1).value == 'MATCH HORSE | JOCKEY' and ws.cell(rr, 2).value in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR'):
                out[rowvals(ws, rr, 29)] += 1
        return out
    l0, l1 = lines(s0), lines(s1)
    gone, new = l0 - l1, l1 - l0
    dis_keys = collections.Counter()
    for (sn, rr, *_rest) in disagree:
        dis_keys[rowvals(wb1[sn], rr, 29)] += 1
    unexplained = (gone + new) - dis_keys
    if unexplained:
        err('SUMMARY lines before vs after not explained by the 2-dp / unrounded filter:', len(unexplained))
    # style check of before SUMMARY lines kept: compare signatures
    def lsig(ws):
        out = collections.Counter()
        for rr in range(1, ws.max_row + 1):
            if ws.cell(rr, 1).value == 'MATCH HORSE | JOCKEY' and ws.cell(rr, 2).value in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR'):
                out[repr(rowsig(ws, rr, 29))] += 1
        return out
    if (lsig(s0) - lsig(s1)) - collections.Counter() and len(lsig(s0) - lsig(s1)) != len(gone):
        err('SUMMARY kept line style changed')
    return report, nlines_rep, disagree, sum(l0.values()), sum(l1.values())


if __name__ == '__main__':
    rep, nl, dis, n0, n1 = check(sys.argv[1], sys.argv[2])
    for x in rep:
        print(x)
    print('summary lines per runner:', ', '.join(nl), '| total before', n0, 'after', n1)
    print('2-dp vs unrounded filter disagreements:', len(dis))
    for d in dis:
        print('  ', d)
    for n in sorted(set(NOTES)):
        print('NOTE', n)
    print('score cells (sky?, own-recomputed?):', dict(FAMCOUNT))
    print('closest own-recomputed score to 50:', CLOSE50)
    print('mismatches:', len(ERR))
    for e in ERR[:40]:
        print('  ', e)
    sys.exit(1 if ERR else 0)
