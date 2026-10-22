"""Independent check of the LONG STAR TIMELINE blocks (Eddie, 22 Oct 2026).

Own code (openpyxl only; does not import tools/jupiter_tables.py or check_longstar.py).
Usage: python3 check_longstar_indep.py <dir with before/ and after/>
Workbooks: {asc,lin}_{full,def}_jupiter_tables.xlsx in before/ and after/.
Checks:
 (1) each LONG STAR block = exactly the Jupiter-star rows of its LONG block (values, fills, comments, order),
     sections, counts, title, sort, score >= 90;
 (2) placement: sky after STAR TIMELINE; runner STAR H, STAR J, LONG STAR H, LONG STAR J;
 (3) every other row of every sheet identical before / after, in order (values, fills, comments);
 (4) default sheets = the --full ones.
"""
import re
import sys
import os
import openpyxl

BODIES = {'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron',
          'Ceres', 'Pallas', 'Juno', 'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar',
          'Orcus', 'Transpluto', 'Rahu', 'Ketu', 'equator', 'Equator', 'Nodes'}

problems = []


def bad(msg):
    problems.append(msg)
    print('MISMATCH:', msg)


def cell_sig(c):
    fill = None
    if c.fill is not None and c.fill.fill_type:
        fill = (c.fill.fill_type, c.fill.fgColor.rgb if c.fill.fgColor is not None else None)
    com = c.comment.text if c.comment is not None else None
    return (c.value, fill, com)


def sheet_rows(ws):
    """list of (rownum, tuple of cell sigs, trimmed of trailing empties)"""
    out = []
    for row in ws.iter_rows():
        sig = [cell_sig(c) for c in row]
        while sig and sig[-1] == (None, None, None):
            sig.pop()
        out.append((row[0].row, tuple(sig)))
    return out


def stars_of(wb):
    ws = wb['P01']
    stars = set()
    for row in ws.iter_rows(values_only=True):
        a = row[0]
        if a == 'T1' and isinstance(row[1], str) and row[1].startswith('H Jupiter → H '):
            x = row[1][len('H Jupiter → H '):].strip()
            if x not in BODIES:
                stars.add(x)
        elif a in ('T21', 'T22', 'T21R', 'T22R') and isinstance(row[1], str) and len(row[1]) < 60:
            for p in row[1].split(' – '):
                stars.add(p.strip())
    stars.discard('Jupiter')
    return stars


def points(rel):
    t = rel.replace('d(star,', '(')
    toks = re.split(r'\s*(?:→|:|–|=|\||/|\(|\))\s*', t)
    pts = []
    for tok in toks:
        tok = tok.strip()
        if not tok:
            continue
        tok = re.sub(r'^[SHJ] ', '', tok)
        pts.append(tok)
    return pts


unknown = set()


def is_jup_star(rel, stars):
    pts = points(rel)
    has_star = False
    for p in pts:
        if p == 'Jupiter':
            continue
        if p in stars:
            has_star = True
            continue
        if p in BODIES:
            return False
        unknown.add(p)
        return False
    return has_star


def blocks(ws):
    """dict name -> list of (rownum, row values, row cells); plus title row and header row index"""
    res = {}
    rows = list(ws.iter_rows())
    for i, row in enumerate(rows):
        a = row[0].value
        if isinstance(a, str) and 'TIMELINE' in a and '(Eddie' in a:
            name = a.split(' (Eddie')[0]
            hdr = rows[i + 1]
            data = []
            j = i + 2
            while j < len(rows) and rows[j][0].value == name:
                data.append(rows[j])
                j += 1
            res[name] = dict(title=row, hdr=hdr, data=data, start=row[0].row, end=(rows[j - 1][0].row))
    return res


def vals(r):
    v = [c.value for c in r]
    while v and v[-1] is None:
        v.pop()
    return v


def check_block(sheetname, long_b, star_b, stars, tag):
    hdr = [c.value for c in long_b['hdr']]
    shdr = [c.value for c in star_b['hdr']]
    if vals(long_b['hdr']) != vals(star_b['hdr']):
        bad(f'{tag} {sheetname}: header differs')
    mcol = hdr.index('minutes from the off')
    # expected = filtered LONG data rows (excluding section rows)
    exp_sep, exp_app = [], []
    sec = None
    for r in long_b['data']:
        d = r[3].value
        if isinstance(d, str) and d.startswith('———'):
            sec = 'S' if 'SEPARATING' in d else 'A'
            continue
        if is_jup_star(r[4].value, stars):
            (exp_sep if sec == 'S' else exp_app).append(r)
    got_sep, got_app = [], []
    sec_rows = []
    sec = None
    for r in star_b['data']:
        d = r[3].value
        if isinstance(d, str) and d.startswith('———'):
            sec = 'S' if 'SEPARATING' in d else 'A'
            sec_rows.append(d)
            continue
        (got_sep if sec == 'S' else got_app).append(r)
    for name, e, g in (('separating', exp_sep, got_sep), ('applying', exp_app, got_app)):
        if len(e) != len(g):
            bad(f'{tag} {sheetname} {name}: expected {len(e)} rows, got {len(g)}')
        for er, gr in zip(e, g):
            es = [cell_sig(c) for c in er[1:]]
            gs = [cell_sig(c) for c in gr[1:]]
            while es and es[-1] == (None, None, None): es.pop()
            while gs and gs[-1] == (None, None, None): gs.pop()
            if es != gs:
                bad(f'{tag} {sheetname} {name}: row {gr[0].row} != LONG row {er[0].row}')
        # every row's own section word, score, sort
        for gr in g:
            if gr[11].value != name:
                bad(f'{tag} {sheetname}: row {gr[0].row} in {name} says {gr[11].value}')
            if not (isinstance(gr[10].value, (int, float)) and gr[10].value >= 90):
                bad(f'{tag} {sheetname}: row {gr[0].row} score {gr[10].value}')
            if not is_jup_star(gr[4].value, stars):
                bad(f'{tag} {sheetname}: row {gr[0].row} not Jupiter-star: {gr[4].value}')

        def key(r):
            m = r[mcol].value
            nw = not isinstance(m, (int, float))
            if name == 'separating':
                return (-r[10].value, nw, -(m if not nw else 0))
            return (-r[10].value, nw, (m if not nw else 0))
        # The tool sorts on the unrounded score; at equal displayed (2 dp) scores the time tie-break
        # can look reversed. Such pairs are reported as notes (checked by hand from POSITIONS), not mismatches.
        for a, b in zip(g, g[1:]):
            ka, kb = key(a), key(b)
            if ka > kb:
                if a[10].value == b[10].value:
                    print(f'NOTE {tag} {sheetname} {name}: rows {a[0].row}/{b[0].row} equal displayed score '
                          f'{a[10].value}, time order reversed (unrounded score decides)')
                else:
                    bad(f'{tag} {sheetname} {name}: sort order wrong at row {b[0].row}')
    ns, na = len(got_sep), len(got_app)
    want_secs = [f'——— SEPARATING: {ns} events ———', f'——— APPLYING: {na} events ———']
    if sec_rows != want_secs:
        bad(f'{tag} {sheetname}: section rows {sec_rows} != {want_secs}')
    title = star_b['title'][0].value
    if not title.endswith(f': {ns + na} events, {ns} separating, {na} applying'):
        bad(f'{tag} {sheetname}: title tail {title[-60:]!r}')
    # star block fill/value on column A of data rows equal to the name (already by construction)
    return ns, na


def check_wb(before_p, after_p, tag):
    wa = openpyxl.load_workbook(after_p)
    wbf = openpyxl.load_workbook(before_p)
    stars = stars_of(wa)
    counts = {}
    if wa.sheetnames != wbf.sheetnames:
        bad(f'{tag}: sheet names differ')
    for sn in wa.sheetnames:
        ws = wa[sn]
        new_rows = set()
        if sn == 'SKY JUPITER' or re.fullmatch(r'P\d\d', sn):
            bl = blocks(ws)
            pairs = ([('LONG TIMELINE', 'LONG STAR TIMELINE')] if sn == 'SKY JUPITER'
                     else [('LONG TIMELINE H', 'LONG STAR TIMELINE H'), ('LONG TIMELINE J', 'LONG STAR TIMELINE J')])
            for ln, sname in pairs:
                if sname not in bl:
                    bad(f'{tag} {sn}: {sname} missing')
                    continue
                counts[(sn, sname)] = check_block(sn, bl[ln], bl[sname], stars, tag)
                b = bl[sname]
                new_rows.update(range(b['start'], b['end'] + 1))
            # placement
            if sn == 'SKY JUPITER':
                order = ['STAR TIMELINE', 'LONG STAR TIMELINE']
            else:
                order = ['STAR TIMELINE H', 'STAR TIMELINE J', 'LONG STAR TIMELINE H', 'LONG STAR TIMELINE J']
            for x, y in zip(order, order[1:]):
                gap = bl[y]['start'] - bl[x]['end']
                between = [r for r in range(bl[x]['end'] + 1, bl[y]['start'])
                           if any(c.value is not None for c in ws[r])]
                if between or gap > 4:
                    bad(f'{tag} {sn}: {y} not right after {x} (gap {gap}, rows {between[:3]})')
            # nothing after the last new block? report what follows
            last = bl[order[-1]]['end']
            follow = [r for r in range(last + 1, ws.max_row + 1) if any(c.value is not None for c in ws[r])]
            counts[(sn, 'follow')] = len(follow)
            # blank rows inserted before the new block(s)
            first_new = bl['LONG STAR TIMELINE' if sn == 'SKY JUPITER' else 'LONG STAR TIMELINE H']['start']
            prev_end = bl['STAR TIMELINE' if sn == 'SKY JUPITER' else 'STAR TIMELINE J']['end']
            new_rows.update(range(prev_end + 1, first_new))
            if sn != 'SKY JUPITER':
                new_rows.update(range(bl['LONG STAR TIMELINE H']['end'] + 1, bl['LONG STAR TIMELINE J']['start']))
        ra = [s for n, s in sheet_rows(ws) if n not in new_rows]
        rb = [s for n, s in sheet_rows(wbf[sn])]
        # before sheets may end with trailing blank rows that move; compare trimmed of trailing blanks
        while ra and ra[-1] == (): ra.pop()
        while rb and rb[-1] == (): rb.pop()
        if ra != rb:
            n = next((i for i, (x, y) in enumerate(zip(ra, rb)) if x != y), min(len(ra), len(rb)))
            bad(f'{tag} {sn}: other rows differ (lens {len(ra)} / {len(rb)}, first at index {n})')
        # merged cells / widths quick check for untouched sheets
        if not new_rows:
            if sorted(map(str, ws.merged_cells.ranges)) != sorted(map(str, wbf[sn].merged_cells.ranges)):
                bad(f'{tag} {sn}: merged ranges differ')
    return wa, counts


def compare_def_full(wd_p, wf, tag):
    wd = openpyxl.load_workbook(wd_p)
    for sn in wd.sheetnames:
        if sn not in wf.sheetnames:
            bad(f'{tag}: default sheet {sn} not in full')
            continue
        if sheet_rows(wd[sn]) != sheet_rows(wf[sn]):
            bad(f'{tag}: default {sn} != full')
    return wd.sheetnames


def main():
    base = sys.argv[1]
    for race in ('asc', 'lin'):
        for kind in ('full', 'def'):
            tag = f'{race}_{kind}'
            p = f'{race}_{kind}_jupiter_tables.xlsx'
            wa, counts = check_wb(os.path.join(base, 'before', p), os.path.join(base, 'after', p), tag)
            for k, v in counts.items():
                print(tag, k, v)
            if kind == 'full':
                full_wb = wa
            else:
                sheets = compare_def_full(os.path.join(base, 'after', p), full_wb, tag)
                print(tag, 'default sheets', sheets)
    print('unknown points:', sorted(unknown))
    print('MISMATCHES:', len(problems))


if __name__ == '__main__':
    main()
