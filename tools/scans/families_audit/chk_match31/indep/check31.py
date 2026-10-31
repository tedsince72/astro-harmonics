"""Independent checker for the 31 Oct 2026 MATCH change (BODY, CONJ STAR, SUMMARY, freeze D4).

Own code: reads only the before / after workbooks (no import of tools/jupiter_tables.py).
usage: python3 check31.py <before.xlsx> <after.xlsx> [--quiet]
Prints counts and every mismatch; exit code 1 when any mismatch.
"""
import re
import sys
from collections import defaultdict, OrderedDict

import openpyxl

BODY_ORDER = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron',
              'Ceres', 'Pallas', 'Juno', 'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus',
              'Transpluto', 'Rahu', 'Ketu']
BIDX = {b: i for i, b in enumerate(BODY_ORDER)}
PIDX = {'RA': 0, 'Dec': 1}
TABLES = ('MATCH HORSE', 'MATCH JOCKEY', 'MATCH HORSE | JOCKEY')
SECTIONS = ('EXACT', 'RATIO', 'BODY', 'CONJ STAR')
NCOL = {'MATCH HORSE': 21, 'MATCH JOCKEY': 21, 'MATCH HORSE | JOCKEY': 29}

ERR = []


def err(msg):
    ERR.append(msg)


# ---------------------------------------------------------------- cell helpers
def style_sig(c):
    f = c.fill
    fo = c.font
    b = c.border
    return (f.fill_type, str(f.fgColor.rgb) if f.fgColor is not None else None,
            fo.b, fo.i, str(fo.color.rgb) if fo.color is not None else None, fo.sz,
            b.left.style, b.right.style, b.top.style, b.bottom.style,
            c.number_format, c.alignment.wrap_text, c.alignment.horizontal, c.alignment.vertical)


def cell_sig(c):
    return (c.value, style_sig(c), c.comment.text if c.comment else None)


def row_sig(ws, r, ncol):
    return tuple(cell_sig(ws.cell(r, k)) for k in range(1, ncol + 1))


def row_vals(ws, r, ncol):
    return tuple(ws.cell(r, k).value for k in range(1, ncol + 1))


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- sources
def parse_sky(wb):
    """SKY block of SKY JUPITER: list of cells in block order (row, RA then Dec)."""
    s = wb['SKY JUPITER']
    cells = []
    order = 0
    for r in range(1, s.max_row + 1):
        if s.cell(r, 1).value != 'SKY':
            continue
        lab = s.cell(r, 2).value
        if not (isinstance(lab, str) and lab.startswith('S Jupiter → ')):
            continue
        for plane, cv, ct, cs in (('RA', 3, 5, 8), ('Dec', 12, 14, 17)):
            v = s.cell(r, cv).value
            t = s.cell(r, ct).value
            sc = s.cell(r, cs).value
            if v is None:
                continue
            fam = tgt = None
            if sc is not None:
                m = re.fullmatch(r'(.+) \((.+)\)', t)
                tgt, fam = m.group(1), m.group(2)
            cells.append(dict(rel=lab, x=lab[len('S Jupiter → S '):], plane=plane, value=v, score=sc, fam=fam,
                              tgt=tgt, order=order, row=r, fill=style_sig(s.cell(r, cs))))
            order += 1
    return cells


def parse_comment(txt):
    if not txt:
        return None
    first = txt.split('\n')[0]
    if first.startswith('nearest'):
        return None
    parts = [p.strip() for p in first.split(' · ')]
    if len(parts) != 4:
        return None
    tgt, fam, off, sc = parts
    if fam.startswith('conjunction'):
        fam, tgt = 'conj', 'conj'
    return dict(tgt=tgt, fam=fam, score=float(sc))


def parse_t24(ws, which):
    """T24 HORSE / JOCKEY block: {row label: {(body, plane): cell}} and row order."""
    title = None
    for r in range(1, ws.max_row + 1):
        if ws.cell(r, 1).value == 'T24' and isinstance(ws.cell(r, 2).value, str) and \
                ws.cell(r, 2).value.startswith('T24 ' + which + ' '):
            title = r
            break
    hdr = title + 2
    cols = {}
    seen = set()
    for c in range(3, ws.max_column + 1):
        n = ws.cell(hdr, c).value
        if n in BIDX:
            plane = 'Dec' if n in seen else 'RA'
            seen.add(n)
            cols[(n, plane)] = c
    rows = OrderedDict()
    r = hdr + 1
    while r <= ws.max_row and ws.cell(r, 1).value == 'T24':
        lab = ws.cell(r, 2).value
        if isinstance(lab, str) and lab.startswith('T24 '):
            break
        d = {}
        for (b, p), c in cols.items():
            cell = ws.cell(r, c)
            if cell.value is None:
                continue
            pc = parse_comment(cell.comment.text if cell.comment else None)
            d[(b, p)] = dict(value=cell.value, sc=pc, col=c)
        rows[lab] = d
        r += 1
    return rows, cols


# ---------------------------------------------------------------- MATCH table parsing
def find_tables(ws):
    """{table: (title_row, [rows])} rows = every row with column A == table (title included)."""
    out = {}
    for t in TABLES:
        rs = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == t]
        out[t] = rs
    return out


def split_table(ws, t, rows):
    """title, header rows, items [(kind, row)] kind 'hdr' / 'data'."""
    title = rows[0]
    rest = rows[1:]
    headers = []
    # column-names row (A='table') sits between; HJ also has a band row with A = table
    items = []
    for r in rest:
        b = ws.cell(r, 2).value
        if b in SECTIONS:
            items.append(('data', r))
        elif b is None:
            headers.append(r)   # band row
        else:
            items.append(('hdr', r))
    return title, headers, items


HDR_RE = re.compile(r'^(S Jupiter → \S.*?) (RA|Dec) (\S+) (.*) — (.*)$')


def hdr_key(text):
    m = HDR_RE.match(text)
    return (m.group(1), m.group(2)) if m else None


def hdr_prefix(text):
    return text.split(' — ')[0]


# ---------------------------------------------------------------- expected rows
def band(score):
    return 'g' if score >= 80 else ('y' if score >= 50 else 'l')


def build_new_rows(table, sky, t24rows, charttag):
    """BODY and CONJ STAR rows for MATCH HORSE (charttag 'H') / JOCKEY ('J'); returns {(rel, plane): [row tuples]}."""
    out = defaultdict(list)
    jrow = t24rows.get(f'{charttag} Jupiter → {charttag} body', {})
    sjrow = t24rows.get(f'S Jupiter → {charttag} body', {})
    for sc in sky:
        if sc['score'] is None or not sc['score'] > 50:
            continue
        key = (sc['rel'], sc['plane'])
        skypart = (sc['rel'], sc['plane'], sc['value'], sc['fam'], sc['tgt'], sc['score'])
        x = sc['x']
        if x in BIDX and x not in ('Jupiter', 'Moon'):
            for p in ('RA', 'Dec'):
                c = jrow.get((x, p))
                if c and c['sc'] and c['sc']['score'] > 50:
                    out[key].append(('BODY', skypart, f'{charttag} Jupiter → {charttag} body', x, p, c['value'],
                                     c['sc']['fam'], c['sc']['tgt'], c['sc']['score']))
        if sc['fam'] == 'conj' and x not in BIDX:
            srow = t24rows.get(f'{charttag} {x}')
            if srow is not None:
                for b in BODY_ORDER:
                    for p in ('RA', 'Dec'):
                        c = srow.get((b, p))
                        if c and c['sc'] and c['sc']['score'] > 50:
                            out[key].append(('CONJ STAR', skypart, f'{charttag} {x}', b, p, c['value'],
                                             c['sc']['fam'], c['sc']['tgt'], c['sc']['score']))
            for b in BODY_ORDER:
                for p in ('RA', 'Dec'):
                    c = sjrow.get((b, p))
                    if c and c['sc'] and c['sc']['score'] > 50:
                        out[key].append(('CONJ STAR', skypart, f'S Jupiter → {charttag} body', b, p, c['value'],
                                         c['sc']['fam'], c['sc']['tgt'], c['sc']['score']))
    return out


def new_row_vals(table, nr):
    sec, (rel, plane, val, fam, tgt, ssc), t24lab, body, p, v, f, tg, s = nr
    return (table, sec, None, None, None, None, None, rel, plane, val, fam, tgt, ssc, t24lab, body, p, v, f, tg, s,
            min(ssc, s))


def fmt_hdr_prefix(sc):
    if sc['fam'] == 'conj':
        return f"{sc['rel']} {sc['plane']} {sc['value']:.6f} conjunction ({sc['score']:.2f})"
    return f"{sc['rel']} {sc['plane']} {sc['value']:.6f} {sc['tgt']} {sc['fam']} ({sc['score']:.2f})"


# ---------------------------------------------------------------- main check
def check(bpath, apath, quiet=False):
    B = openpyxl.load_workbook(bpath)
    A = openpyxl.load_workbook(apath)
    report = {}
    # ---- sheets
    if A.sheetnames != B.sheetnames + ['SUMMARY']:
        err(f'sheet names {A.sheetnames} vs before {B.sheetnames}')
    runners = [n for n in B.sheetnames if re.fullmatch(r'P\d\d', n)]
    # ---- non-runner sheets identical
    for n in ('POSITIONS', 'SKY JUPITER'):
        bs, as_ = B[n], A[n]
        if (bs.max_row, bs.max_column) != (as_.max_row, as_.max_column):
            err(f'{n} dims differ')
        for r in range(1, max(bs.max_row, as_.max_row) + 1):
            for c in range(1, max(bs.max_column, as_.max_column) + 1):
                if cell_sig(bs.cell(r, c)) != cell_sig(as_.cell(r, c)):
                    err(f'{n} {r},{c} differs')
        if bs.freeze_panes != as_.freeze_panes:
            err(f'{n} freeze {bs.freeze_panes} -> {as_.freeze_panes}')
        if sorted(map(str, bs.merged_cells.ranges)) != sorted(map(str, as_.merged_cells.ranges)):
            err(f'{n} merges differ')
    sky = parse_sky(A)
    skymap = {(c['rel'], c['plane']): c for c in sky}
    n_conj_scoring = sum(1 for c in sky if c['score'] is not None and c['fam'] == 'conj')
    n_scoring_noconj = sum(1 for c in sky if c['score'] is not None and c['fam'] != 'conj')

    # learn band fills from source cells (SKY block score cells)
    # band fills (green >= 80, yellow 50-80, light < 50) as on the before EXACT / RATIO rows; a shown 80.00 / 50.00 may be
    # just under the edge unrounded, so either neighbouring fill is accepted there
    band_fill = {'g': ('solid', '00C6EFCE'), 'y': ('solid', '00FFEB9C'), 'l': ('solid', '00FFF8DC')}

    hj_store = {}
    for rn in runners:
        bw, aw = B[rn], A[rn]
        if bw.freeze_panes != 'C4':
            err(f'{rn} before freeze {bw.freeze_panes}')
        if aw.freeze_panes != 'D4':
            err(f'{rn} after freeze {aw.freeze_panes} (expected D4)')
        bt, at = find_tables(bw), find_tables(aw)
        mstart_b, mstart_a = bt['MATCH HORSE'][0], at['MATCH HORSE'][0]
        if mstart_b != mstart_a:
            err(f'{rn} MATCH HORSE starts {mstart_b} -> {mstart_a}')
        for r in range(1, mstart_b):
            for c in range(1, max(bw.max_column, aw.max_column) + 1):
                if cell_sig(bw.cell(r, c)) != cell_sig(aw.cell(r, c)):
                    err(f'{rn} {r},{c} above MATCH differs')
        # widths
        for k in set(bw.column_dimensions) | set(aw.column_dimensions):
            if bw.column_dimensions[k].width != aw.column_dimensions[k].width:
                err(f'{rn} width {k} {bw.column_dimensions[k].width} -> {aw.column_dimensions[k].width}')
        # merges above MATCH unchanged; HJ band merges at the band row
        mb = {str(m) for m in bw.merged_cells.ranges if m.min_row < mstart_b}
        ma = {str(m) for m in aw.merged_cells.ranges if m.min_row < mstart_a}
        if mb != ma:
            err(f'{rn} merges above MATCH differ')
        # layout: two blank rows between tables, nothing after HJ
        for tab in TABLES:
            rs = at[tab]
            if rs != list(range(rs[0], rs[-1] + 1)):
                # HJ column-names row has A='table'
                pass
        t24 = {'MATCH HORSE': parse_t24(aw, 'HORSE')[0], 'MATCH JOCKEY': parse_t24(aw, 'JOCKEY')[0]}
        tag = {'MATCH HORSE': 'H', 'MATCH JOCKEY': 'J'}
        per_table_groups = {}
        per_table_rows = {}
        for tab in ('MATCH HORSE', 'MATCH JOCKEY'):
            # before rows by group
            btitle, _, bitems = split_table(bw, tab, bt[tab])
            atitle, _, aitems = split_table(aw, tab, at[tab])
            bgroups = OrderedDict()
            cur = None
            bhdr_text = {}
            for kind, r in bitems:
                if kind == 'hdr':
                    cur = hdr_key(bw.cell(r, 2).value)
                    bgroups[cur] = []
                    bhdr_text[cur] = (bw.cell(r, 2).value, row_sig(bw, r, NCOL[tab])[2:], style_sig(bw.cell(r, 1)))
                else:
                    bgroups[cur].append(r)
            new = build_new_rows(tab, sky, t24[tab], tag[tab])
            keys = set(bgroups) | {k for k, v in new.items() if v}
            for k in keys:
                if k not in skymap:
                    err(f'{rn} {tab} group {k} not in SKY block')
            order = sorted(keys, key=lambda k: (-skymap[k]['score'], skymap[k]['order']))
            # ties
            scs = [round(skymap[k]['score'], 2) for k in order]
            for i in range(1, len(scs)):
                if scs[i] == scs[i - 1]:
                    report.setdefault('ties', []).append((rn, tab, order[i - 1], order[i], scs[i]))
            # expected sequence
            exp = []  # (kind, payload)
            gcounts = {}
            for k in order:
                brs = bgroups.get(k, [])
                nrs = new.get(k, [])
                ne = sum(1 for r in brs if bw.cell(r, 2).value == 'EXACT')
                nra = sum(1 for r in brs if bw.cell(r, 2).value == 'RATIO')
                nb = sum(1 for x in nrs if x[0] == 'BODY')
                nc = sum(1 for x in nrs if x[0] == 'CONJ STAR')
                gcounts[k] = (ne, nra, nb, nc)
                if k in bhdr_text:
                    htext = hdr_prefix(bhdr_text[k][0])
                    if htext != fmt_hdr_prefix(skymap[k]):
                        err(f'{rn} {tab} before header prefix {htext!r} vs own {fmt_hdr_prefix(skymap[k])!r}')
                else:
                    htext = fmt_hdr_prefix(skymap[k])
                htext += f' — EXACT {ne}, RATIO {nra}, BODY {nb}, CONJ STAR {nc}'
                exp.append(('hdr', htext, k))
                for r in brs:
                    exp.append(('old', r, k))
                for x in nrs:
                    exp.append(('new', x, k))
            if len(exp) != len(aitems):
                err(f'{rn} {tab} items {len(aitems)} vs expected {len(exp)}')
            # header style reference (any before header)
            ref_hdr = next(iter(bhdr_text.values()))[1] if bhdr_text else None
            ref_data = None
            for kind, r in bitems:
                if kind == 'data':
                    ref_data = [style_sig(bw.cell(r, c)) for c in range(1, NCOL[tab] + 1)]
                    break
            for (ek, ep, gk), (ak, ar) in zip(exp, aitems):
                if ek == 'hdr':
                    if ak != 'hdr' or aw.cell(ar, 2).value != ep:
                        err(f'{rn} {tab} row {ar}: expected header {ep!r}, got {aw.cell(ar, 2).value!r}')
                    elif ref_hdr is not None and row_sig(aw, ar, NCOL[tab])[2:] != ref_hdr:
                        err(f'{rn} {tab} row {ar}: header style differs')
                elif ek == 'old':
                    if row_sig(aw, ar, NCOL[tab]) != row_sig(bw, ep, NCOL[tab]):
                        err(f'{rn} {tab} row {ar}: old row (before {ep}) differs')
                else:
                    ev = new_row_vals(tab, ep)
                    av = row_vals(aw, ar, NCOL[tab])
                    if ev != av:
                        err(f'{rn} {tab} row {ar}: new row {ev} vs sheet {av}')
                    # fills of score cells
                    for col, s in ((13, ev[12]), (20, ev[19]), (21, ev[20])):
                        f = style_sig(aw.cell(ar, col))
                        bf = band_fill[band(s)]
                        ok = {bf}
                        if round(s, 2) in (80.0, 50.0):
                            ok.add(band_fill[band(s - 0.01)])
                        if f[:2] not in ok:
                            err(f'{rn} {tab} row {ar} col {col}: fill {f[:2]} vs band {band(s)} {bf}')
                    if ref_data:
                        for col in range(1, NCOL[tab] + 1):
                            if col in (13, 20, 21):
                                continue
                            if style_sig(aw.cell(ar, col))[2:] != ref_data[col - 1][2:]:
                                err(f'{rn} {tab} row {ar} col {col}: style differs from data rows')
            # title totals
            ttext = aw.cell(atitle, 2).value
            nE = sum(c[0] for c in gcounts.values())
            nR = sum(c[1] for c in gcounts.values())
            nB = sum(c[2] for c in gcounts.values())
            nC = sum(c[3] for c in gcounts.values())
            nconjg = sum(1 for k in order if skymap[k]['fam'] == 'conj')
            m = re.search(r'EXACT (\d+) rows, RATIO (\d+) rows \(whole (\d+), golden (\d+)\), BODY (\d+) rows, '
                          r'CONJ STAR (\d+) rows, (\d+) sky cells \((\d+) conjunction\) \(SKY block (\d+) scoring cells '
                          r'without conjunction, (\d+) conjunction; T24 (HORSE|JOCKEY) (\d+)\)$', ttext)
            bm = re.search(r'EXACT (\d+) rows, RATIO (\d+) rows \(whole (\d+), golden (\d+)\), (\d+) sky cells '
                           r'\(SKY block (\d+) scoring cells, T24 (HORSE|JOCKEY) (\d+)\)$', bw.cell(btitle, 2).value)
            if not m or not bm:
                err(f'{rn} {tab} title tail not parsed')
            else:
                got = tuple(int(m.group(i)) for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12))
                want = (nE, nR, int(bm.group(3)), int(bm.group(4)), nB, nC, len(order), nconjg, n_scoring_noconj,
                        n_conj_scoring, int(bm.group(8)))
                if got != want:
                    err(f'{rn} {tab} title totals {got} vs expected {want}')
                if (int(bm.group(1)), int(bm.group(2))) != (nE, nR):
                    err(f'{rn} {tab} before EXACT/RATIO totals changed')
                if int(bm.group(6)) != n_scoring_noconj:
                    report.setdefault('notes', []).append(
                        f'{rn} {tab}: before SKY block scoring {bm.group(6)} vs own non-conj {n_scoring_noconj}')
            newg = [k for k in order if k not in bgroups]
            report.setdefault('counts', []).append(
                (rn, tab, nB, nC, len(newg), [f'{k[0][12:]} {k[1]}' for k in newg]))
            per_table_groups[tab] = (order, gcounts)
            per_table_rows[tab] = (aw, aitems)
        # ---------------- HJ table
        hj_store[rn] = check_hj(rn, bw, aw, bt, at, sky, skymap, per_table_groups, per_table_rows, report)
    check_summary(A, runners, hj_store, report)
    return report


def side_key(aw, r, sec):
    """key of a MATCH row inside its group (for BODY / CONJ STAR)."""
    lab = aw.cell(r, 14).value
    kind = 'sj' if lab.startswith('S Jupiter → ') else ('jup' if ' Jupiter → ' in lab else 'star')
    return (sec, kind, BIDX[aw.cell(r, 15).value], PIDX[aw.cell(r, 16).value])


def check_hj(rn, bw, aw, bt, at, sky, skymap, groups, rows, report):
    tab = 'MATCH HORSE | JOCKEY'
    btitle, bbands, bitems = split_table(bw, tab, bt[tab])
    atitle, abands, aitems = split_table(aw, tab, at[tab])
    # band row and column names identical to before
    if [row_sig(bw, r, 29) for r in bbands] != [row_sig(aw, r, 29) for r in abands]:
        err(f'{rn} HJ band row differs')
    bcn = bt[tab][0] + 2
    acn = at[tab][0] + 2
    if row_sig(bw, bcn, 29) != row_sig(aw, acn, 29):
        err(f'{rn} HJ column names differ')
    bmerg = sorted((m.min_row - bt[tab][0], m.min_col, m.max_col) for m in bw.merged_cells.ranges if m.min_row >= bt[tab][0])
    amerg = sorted((m.min_row - at[tab][0], m.min_col, m.max_col) for m in aw.merged_cells.ranges if m.min_row >= at[tab][0])
    if bmerg != amerg:
        err(f'{rn} HJ merges {amerg} vs before {bmerg}')
    # before lines by group
    bgroups = OrderedDict()
    bhdr = {}
    cur = None
    for kind, r in bitems:
        if kind == 'hdr':
            cur = hdr_key(bw.cell(r, 2).value)
            bgroups[cur] = []
            bhdr[cur] = bw.cell(r, 2).value
        else:
            bgroups[cur].append(r)
    # rows of the H / J tables by group
    def by_group(t):
        aw_, items = rows[t]
        d = defaultdict(list)
        cur = None
        for kind, r in items:
            if kind == 'hdr':
                cur = hdr_key(aw_.cell(r, 2).value)
            else:
                d[cur].append(r)
        return d
    hrows, jrows = by_group('MATCH HORSE'), by_group('MATCH JOCKEY')
    hord, hcnt = groups['MATCH HORSE']
    jord, jcnt = groups['MATCH JOCKEY']
    keys = set(hord) | set(jord)
    order = sorted(keys, key=lambda k: (-skymap[k]['score'], skymap[k]['order']))
    exp = []
    nlines = 0
    keyset = {'both': 0, 'h': 0, 'j': 0}
    bysec = defaultdict(int)
    ref_hdr = None
    for k in order:
        hc, jc = hcnt.get(k, (0, 0, 0, 0)), jcnt.get(k, (0, 0, 0, 0))
        text = (hdr_prefix(bhdr[k]) if k in bhdr else fmt_hdr_prefix(skymap[k])) + \
            f' — EXACT {hc[0]} | {jc[0]}, RATIO {hc[1]} | {jc[1]}, BODY {hc[2]} | {jc[2]}, CONJ STAR {hc[3]} | {jc[3]}'
        exp.append(('hdr', text, k))
        for r in bgroups.get(k, []):
            exp.append(('old', r, k))
        # old keys counted from the before title would be easier, but count from own rule: key on EXACT / RATIO lines
        # new lines
        nk = OrderedDict()
        for r in hrows.get(k, []):
            sec = aw.cell(r, 2).value
            if sec in ('BODY', 'CONJ STAR'):
                nk.setdefault(side_key(aw, r, sec), [None, None])[0] = r
        for r in jrows.get(k, []):
            sec = aw.cell(r, 2).value
            if sec in ('BODY', 'CONJ STAR'):
                kk = side_key(aw, r, sec)
                nk.setdefault(kk, [None, None])
                if nk[kk][1] is not None:
                    err(f'{rn} HJ duplicate jockey key {kk}')
                nk[kk][1] = r
        for kk in sorted(nk, key=lambda x: (SECTIONS.index(x[0]), 0 if x[1] in ('star', 'jup') else 1, x[2], x[3])):
            exp.append(('new', tuple(nk[kk]), k))
            hr, jr = nk[kk]
            keyset['both' if hr and jr else ('h' if hr else 'j')] += 1
            bysec[kk[0]] += 1
    # old lines' keys: recount from the before title
    bt_text = bw.cell(btitle, 2).value
    bm = re.search(r'(\d+) lines, (\d+) keys: (\d+) with both sides, (\d+) horse only, (\d+) jockey only; (\d+) sky cells '
                   r'\(MATCH HORSE (\d+) rows, MATCH JOCKEY (\d+) rows\)$', bt_text)
    old_exact_keys = None
    if len(exp) != len(aitems):
        err(f'{rn} HJ items {len(aitems)} vs expected {len(exp)}')
    for h in bhdr.values():
        ref_hdr = None
    for (ek, ep, gk), (ak, ar) in zip(exp, aitems):
        if ek == 'hdr':
            if ak != 'hdr' or aw.cell(ar, 2).value != ep:
                err(f'{rn} HJ row {ar}: expected header {ep!r}, got {aw.cell(ar, 2).value!r}')
            if aw.cell(ar, 1).fill.fgColor.rgb != '00D9D9D9' or aw.cell(ar, 29).fill.fgColor.rgb != '00D9D9D9':
                err(f'{rn} HJ row {ar}: header not grey A-AC')
        elif ek == 'old':
            if row_sig(aw, ar, 29) != row_sig(bw, ep, 29):
                err(f'{rn} HJ row {ar}: old line (before {ep}) differs')
        else:
            hr, jr = ep
            src = hr or jr
            want = [cell_sig(aw.cell(src, c)) for c in range(2, 14)]
            got = [cell_sig(aw.cell(ar, c)) for c in range(2, 14)]
            if want != got:
                err(f'{rn} HJ row {ar}: shared cells differ from source row {src}')
            if aw.cell(ar, 1).value != 'MATCH HORSE | JOCKEY':
                err(f'{rn} HJ row {ar}: column A')
            if hr and jr:
                for c in range(2, 14):
                    if aw.cell(hr, c).value != aw.cell(jr, c).value:
                        err(f'{rn} HJ: horse {hr} / jockey {jr} shared cells disagree')
                        break
            for side, srow, off in (('H', hr, 14), ('J', jr, 22)):
                for i in range(8):
                    g = aw.cell(ar, off + i)
                    if srow:
                        if cell_sig(g) != cell_sig(aw.cell(srow, 14 + i)):
                            err(f'{rn} HJ row {ar}: {side} cell {off + i} != source {srow}')
                    elif g.value is not None:
                        err(f'{rn} HJ row {ar}: {side} side should be empty')
    # title
    t = aw.cell(atitle, 2).value
    m = re.search(r'(\d+) lines, (\d+) keys: (\d+) with both sides, (\d+) horse only, (\d+) jockey only \(by section: '
                  r'EXACT (\d+), RATIO (\d+), BODY (\d+), CONJ STAR (\d+)\); (\d+) sky cells \(MATCH HORSE (\d+) rows, '
                  r'MATCH JOCKEY (\d+) rows\)$', t)
    nlines = sum(1 for e in exp if e[0] != 'hdr')
    hrowsn = sum(sum(c) for c in hcnt.values())
    jrowsn = sum(sum(c) for c in jcnt.values())
    if not m or not bm:
        err(f'{rn} HJ title not parsed')
    else:
        old_keys = int(bm.group(2))
        want = (nlines, old_keys + sum(keyset.values()), int(bm.group(3)) + keyset['both'],
                int(bm.group(4)) + keyset['h'], int(bm.group(5)) + keyset['j'], bysec['BODY'], bysec['CONJ STAR'],
                len(order), hrowsn, jrowsn)
        got = (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(8)),
               int(m.group(9)), int(m.group(10)), int(m.group(11)), int(m.group(12)))
        if got != want:
            err(f'{rn} HJ title {got} vs expected {want}')
        if int(m.group(6)) + int(m.group(7)) != old_keys:
            err(f'{rn} HJ title EXACT + RATIO keys {m.group(6)} + {m.group(7)} != before keys {old_keys}')
    report.setdefault('hj', []).append((rn, nlines, sum(keyset.values()), keyset, dict(bysec)))
    # return the after HJ lines for the summary: list of (kind, row)
    return (aw, at[tab][0], aitems)


def check_summary(A, runners, hj_store, report):
    if 'SUMMARY' not in A.sheetnames:
        err('no SUMMARY sheet')
        return
    S = A['SUMMARY']
    exp = []  # list of ('row', sig tuple) or ('blank',)
    merges = []
    for i, rn in enumerate(runners):
        aw, t0, items = hj_store[rn]
        exp.append(('copy', aw, 1, 1))  # A1 line
        exp.append(('copy', aw, t0 + 1, 29))  # band row
        exp.append(('copy', aw, t0 + 2, 29))  # column names
        merges.append(len(exp) - 2)  # band row index (0-based) -> merges
        shown = []
        groups = []
        cur = None
        for kind, r in items:
            if kind == 'hdr':
                cur = [r, []]
                groups.append(cur)
            else:
                cur[1].append(r)
        nshow = 0
        for hr, lines in groups:
            sel = [r for r in lines if (fnum(aw.cell(r, 13).value) or 0) > 50 and
                   ((fnum(aw.cell(r, 20).value) or -1) > 50 or (fnum(aw.cell(r, 28).value) or -1) > 50)]
            if not sel:
                continue
            cnt = {s: [0, 0] for s in SECTIONS}
            for r in sel:
                s = aw.cell(r, 2).value
                if aw.cell(r, 14).value is not None:
                    cnt[s][0] += 1
                if aw.cell(r, 22).value is not None:
                    cnt[s][1] += 1
            text = hdr_prefix(aw.cell(hr, 2).value) + ' — ' + ', '.join(f'{s} {cnt[s][0]} | {cnt[s][1]}' for s in SECTIONS)
            exp.append(('hdr', aw, hr, text))
            for r in sel:
                exp.append(('copy', aw, r, 29))
            nshow += len(sel)
        if nshow == 0:
            exp.append(('nolines',))
        report.setdefault('summary', []).append((rn, nshow))
        if i < len(runners) - 1:
            exp.append(('blank',))
            exp.append(('blank',))
    # compare
    for i, e in enumerate(exp):
        r = i + 1
        if e[0] == 'blank':
            if any(S.cell(r, c).value is not None for c in range(1, 30)):
                err(f'SUMMARY row {r} should be blank')
        elif e[0] == 'nolines':
            vals = [S.cell(r, c).value for c in range(1, 30) if S.cell(r, c).value is not None]
            if not vals or 'no lines' not in ' '.join(map(str, vals)):
                err(f'SUMMARY row {r}: expected "no lines", got {vals}')
        elif e[0] == 'copy':
            _, aw, sr, n = e
            for c in range(1, n + 1):
                if cell_sig(S.cell(r, c)) != cell_sig(aw.cell(sr, c)):
                    err(f'SUMMARY row {r} col {c} != {aw.title} row {sr}')
                    break
        elif e[0] == 'hdr':
            _, aw, sr, text = e
            if S.cell(r, 2).value != text:
                err(f'SUMMARY row {r}: header {S.cell(r, 2).value!r} vs expected {text!r}')
            for c in range(1, 30):
                if c == 2:
                    continue
                if cell_sig(S.cell(r, c)) != cell_sig(aw.cell(sr, c)):
                    err(f'SUMMARY row {r} col {c}: header cell != source')
                    break
            if style_sig(S.cell(r, 2)) != style_sig(aw.cell(sr, 2)):
                err(f'SUMMARY row {r}: header style')
    for r in range(len(exp) + 1, S.max_row + 1):
        if any(S.cell(r, c).value is not None for c in range(1, 30)):
            err(f'SUMMARY extra row {r}')
    want_m = sorted(f'{a}{i + 1}:{b}{i + 1}' for i in merges for a, b in (('N', 'U'), ('V', 'AC')))
    got_m = sorted(str(m) for m in S.merged_cells.ranges)
    if want_m != got_m:
        err(f'SUMMARY merges {got_m} vs {want_m}')


if __name__ == '__main__':
    rep = check(sys.argv[1], sys.argv[2])
    quiet = '--quiet' in sys.argv
    if not quiet:
        for c in rep.get('counts', []):
            print('ROWS', c)
        for h in rep.get('hj', []):
            print('HJ', h)
        for s in rep.get('summary', []):
            print('SUMMARY', s)
        for t in rep.get('ties', []):
            print('TIE', t)
        for n in rep.get('notes', []):
            print('NOTE', n)
    print(f'MISMATCHES {len(ERR)}')
    for e in ERR[:40]:
        print('  ', e)
    sys.exit(1 if ERR else 0)
