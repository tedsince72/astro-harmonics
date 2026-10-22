"""check_sel_c.py: (c) T24 STAR SELECT = the rule: selection from the sky STAR TIMELINE + LONG STAR TIMELINE, order, layout, body cells =
T24 HORSE / JOCKEY cells, every ratio cell recomputed from POSITIONS. Also (a) every sky star-timeline row is centred on S Jupiter.
usage: check_sel_c.py tables.xlsx"""
import itertools, re, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from check_sel_common import *

wb = openpyxl.load_workbook(sys.argv[1])
sky, ch = load_positions(wb)
PAIRS = list(itertools.combinations(BODIES24, 2))
FILL = {'green': '00C6EFCE', 'yellow': '00FFEB9C', 'light': '00FFF8DC'}
AREAL = {'A': 'A', 'P': 'φ and √2', 'B': 'B'}
bad = []

# ---------------------------------------------------------------- sky events
ws = wb['SKY JUPITER']
ev = {}
nrows = {'STAR TIMELINE': 0, 'LONG STAR TIMELINE': 0}
for r in ws.iter_rows(values_only=True):
    if not r or r[0] not in nrows or r[4] is None or r[1] is None:
        continue
    nrows[r[0]] += 1
    rel, plane, kind, tgt, sc = r[4], r[5], r[6], r[7], r[10]
    single = re.fullmatch(r'S Jupiter → S (.+)', rel)
    pair = re.fullmatch(r'S Jupiter: S (.+?) – S (.+)', rel)
    if not (single and kind == 'distance' and plane in ('RA', 'Dec') or pair and kind in ('ratio', 'midpoint')):
        bad.append(('sky star timeline row not centred on S Jupiter', r[0], rel, plane, kind))
    k = (rel, plane, kind, tgt)
    e = ev.setdefault(k, dict(rel=rel, plane=plane, kind=kind, tgt=tgt, score=sc, blocks=[], single=single, pair=pair))
    if e['score'] != sc:
        bad.append(('score differs between blocks', k, e['score'], sc))
    e['blocks'].append(r[0])
print('sky rows', nrows, 'distinct events', len(ev))

sel = {}
for e in ev.values():
    if e['single'] and e['kind'] == 'distance' and (e['score'] or 0) > 90:
        sel.setdefault(('S', e['single'][1]), []).append(e)
    if e['pair'] and e['kind'] in ('ratio', 'midpoint') and (e['score'] or 0) > 95:
        sel.setdefault(('P', e['pair'][1], e['pair'][2]), []).append(e)


# ---------------------------------------------------------------- per runner
def ratio_expect(d1, d2, legs):
    """legs: [(label, distance, plane)] -> (value, comment, fill)"""
    for lab, d, pl in legs:
        if d < (1.5 if pl == 'RA' else 0.3):
            return 'together', None, lab, d, pl
    v = max(d1, d2) / min(d1, d2)
    return v, F.best(v, None, 'ratio'), None, None, None


def check_ratio_cell(c, d1, d2, legs, where):
    v, b, tlab, td, tpl = ratio_expect(d1, d2, legs)
    fill = c.fill.fgColor.rgb if c.fill is not None and c.fill.fill_type else None
    com = c.comment.text if c.comment else None
    if v == 'together':
        ok = c.value == 'together' and fill is None and com is not None and tlab in com and f'{td:.6f}' in com \
            and f'({tpl} < {1.5 if tpl == "RA" else 0.3})' in com
        if not ok:
            bad.append(('together cell', where, c.value, fill, com, tlab, td))
        return 'together'
    if not isinstance(c.value, (int, float)) or abs(c.value - round(v, 6)) > 1e-9:
        bad.append(('ratio value', where, c.value, round(v, 6)))
    if b:
        lab = b['target']
        offs = f"{b['off']:+.5f}" + ('%' if b['pct'] else '')
        exp = f"{lab} · {b['name']} · {b["group"]} · {AREAL[F.area(lab)]} · {offs} · {b['score']:.2f}"
        expfill = FILL[F.colour(b['score'])]
        if com != exp or fill != expfill:
            bad.append(('ratio hit cell', where, c.value, com, exp, fill, expfill))
        return 'hit'
    o = F.outside(v, None, 'ratio')
    offs = f"{o['off']:+.5f}" + ('%' if o['pct'] else '')
    exp = f"nearest: {o['target']} · {o['name']} — outside · {offs}"
    if com != exp or fill is not None:
        bad.append(('ratio outside cell', where, c.value, com, exp, fill))
    return 'out'


def t24_rows(ws):
    """{('H'|'J', star): {(plane, body): cell}} from the T24 HORSE / JOCKEY blocks"""
    out = {}
    hdr = None
    for row in ws.iter_rows():
        a, b = row[0].value, row[1].value if len(row) > 1 else None
        if a is None and len(row) > 2 and row[2].value == 'Sun':
            hdr = row
        if a == 'T24' and isinstance(b, str) and b[:2] in ('H ', 'J '):
            seen = set()
            m = {}
            for i, h in enumerate(hdr):
                if i < 2 or h.value not in BODIES24:
                    continue
                pl = 'Dec' if h.value in seen else 'RA'
                seen.add(h.value)
                m[(pl, h.value)] = row[i]
            out[(b[0], b[2:])] = m
    return out


def cells_eq_t24(c, t, where):
    fc = c.fill.fgColor.rgb if c.fill is not None and c.fill.fill_type else None
    ft = t.fill.fgColor.rgb if t.fill is not None and t.fill.fill_type else None
    cc = c.comment.text if c.comment else None
    tc = t.comment.text.split('\n')[0] if t.comment else None
    if c.value != t.value or fc != ft or cc != tc:
        bad.append(('body cell != T24', where, (c.value, fc, cc), (t.value, ft, tc)))


tot = {'tables': 0, 'body': 0, 'ratio': 0, 'together': 0, 'hit': 0, 'out': 0}
runners = [s for s in wb.sheetnames if re.fullmatch(r'P\d\d', s)]
for P in runners:
    ws = wb[P]
    T24 = t24_rows(ws)
    star_order = [k[1] for k in T24 if k[0] == 'H']
    pos = {C: ch[P][C] for C in 'HJ'}
    rows = list(ws.iter_rows())
    # expected order
    singles = sorted([k for k in sel if k[0] == 'S'], key=lambda k: star_order.index(k[1]))
    pairs = [k for k in sel if k[0] == 'P']
    # tables on sheet
    tabs, i = [], 0
    first = last_prev = None
    while i < len(rows):
        if rows[i][0].value == 'T24 STAR SELECT' and isinstance(rows[i][1].value, str) and rows[i][1].value.startswith('T24 STAR SELECT — '):
            if first is None:
                first = i
            tabs.append(i)
        i += 1
    # placement: the row before the first table block (skipping blanks) is T24 JOCKEY RATIOS
    j = first - 1
    while j >= 0 and all(c.value is None for c in rows[j]):
        j -= 1
    if rows[j][0].value != 'T24 JOCKEY RATIOS':
        bad.append(('placement', P, rows[j][0].value))
    names = []
    for ti in tabs:
        t = rows[ti][1].value
        m = re.match(r'T24 STAR SELECT — S (.+?)(?: – S (.+?))?: ', t)
        names.append(('S', m[1]) if not m[2] else ('P', m[1], m[2]))
    pair_order = [n for n in names if n[0] == 'P']
    if names[:len(singles)] != singles or set(pair_order) != set(pairs) or len(names) != len(singles) + len(pairs):
        bad.append(('selection / order', P, names, singles, pairs))
    for ti, nm in zip(tabs, names):
        tot['tables'] += 1
        title = rows[ti][1].value
        evs = sel.get(nm, [])
        for e in evs:
            bl = ' + '.join(b for b in ('STAR TIMELINE', 'LONG STAR TIMELINE') if b in e['blocks'])
            frag = f"{bl}: {e['rel']} {e['plane']} {e['kind']} {e['tgt']} ({e['score']:.2f})"
            if frag not in title:
                bad.append(('title missing event', P, nm, frag, title[:300]))
        if title.split('. T24 STAR SELECT (')[0].count(', exact ') != len(evs):
            bad.append(('title event count', P, nm, len(evs), title[:400]))
        if rows[ti][0].value != 'T24 STAR SELECT':
            bad.append(('col A', P, nm))
        h1, h2 = rows[ti + 1], rows[ti + 2]
        # header row 1 + merges
        exp1 = {3: 'RA', 27: 'Dec', 51: 'RA pairs', 327: 'Dec pairs'}
        for col, v in exp1.items():
            if h1[col - 1].value != v:
                bad.append(('header1', P, nm, col, h1[col - 1].value))
        r1 = ti + 2
        merges = {str(m) for m in ws.merged_cells.ranges if m.min_row == r1}
        expm = {f'C{r1}:Z{r1}', f'AA{r1}:AX{r1}', f'AY{r1}:LN{r1}', f'LO{r1}:WD{r1}'}
        if merges != expm:
            bad.append(('merges', P, nm, merges))
        exp2 = BODIES24 + BODIES24 + [f'{x} / {y}' for x, y in PAIRS] * 2
        got2 = [c.value for c in h2[2:2 + len(exp2)]]
        if got2 != exp2 or (h1[0].value, h1[1].value) != ('table', 'row') or len(h2) > 2 + len(exp2) and any(c.value for c in h2[2 + len(exp2):]):
            bad.append(('header2', P, nm))
        # rows
        k = ti + 3
        if nm[0] == 'S':
            plan = [('H', nm[1]), ('J', nm[1]), ('HJ', nm[1])]
        else:
            A, B = nm[1], nm[2]
            plan = [('H', A), ('H', B), ('HAB', A, B), None, ('J', A), ('J', B), ('JAB', A, B), None, ('HJ', A), ('HJ', B)]
        for p in plan:
            row = rows[k]
            k += 1
            if p is None:
                if any(c.value is not None for c in row):
                    bad.append(('blank row expected', P, nm, k))
                continue
            kind = p[0]
            lab = {'H': f'H {p[1]}', 'J': f'J {p[1]}', 'HJ': f'H / J {p[1]}'}.get(kind) or f'{kind[0]} {p[1]} / {p[2]}'
            if row[1].value != lab or row[0].value != 'T24 STAR SELECT':
                bad.append(('row label', P, nm, row[1].value, lab))
                continue
            cells = {}
            for i, h in enumerate(exp2):
                pl = 'RA' if (i < 24 or 48 <= i < 48 + 276) else 'Dec'
                cells[(pl, h)] = row[2 + i] if 2 + i < len(row) else None
            for pl in ('RA', 'Dec'):
                for X in BODIES24:
                    c = cells[(pl, X)]
                    w = (P, nm, lab, pl, X)
                    if kind in ('H', 'J'):
                        cells_eq_t24(c, T24[(kind, p[1])][(pl, X)], w)
                        tot['body'] += 1
                        # and the value from POSITIONS
                        d = rawd(pos[kind][p[1]], pos[kind][X], pl)
                        if c.value != round(d, 6):
                            bad.append(('body value vs POSITIONS', w, c.value, round(d, 6)))
                    elif kind == 'HJ':
                        dh, dj = rawd(pos['H'][p[1]], pos['H'][X], pl), rawd(pos['J'][p[1]], pos['J'][X], pl)
                        tot[check_ratio_cell(c, dh, dj, [(f'H {p[1]}, H {X}', dh, pl), (f'J {p[1]}, J {X}', dj, pl)], w)] += 1
                        tot['ratio'] += 1
                    else:
                        C = kind[0]
                        da, db = rawd(pos[C][p[1]], pos[C][X], pl), rawd(pos[C][p[2]], pos[C][X], pl)
                        tot[check_ratio_cell(c, da, db, [(f'{C} {p[1]}, {C} {X}', da, pl), (f'{C} {p[2]}, {C} {X}', db, pl)], w)] += 1
                        tot['ratio'] += 1
                for X, Y in PAIRS:
                    c = cells[(pl, f'{X} / {Y}')]
                    w = (P, nm, lab, pl, X, Y)
                    if kind in ('H', 'J'):
                        s = pos[kind][p[1]]
                        d1, d2 = rawd(s, pos[kind][X], pl), rawd(s, pos[kind][Y], pl)
                        tot[check_ratio_cell(c, d1, d2, [(f'{kind} {p[1]}, {kind} {X}', d1, pl), (f'{kind} {p[1]}, {kind} {Y}', d2, pl)], w)] += 1
                        tot['ratio'] += 1
                    elif c is not None and (c.value is not None or c.comment or c.fill.fill_type):
                        bad.append(('pair column not blank', w, c.value))
            if len(row) > 2 + len(exp2) and any(c.value is not None for c in row[2 + len(exp2):]):
                bad.append(('cells beyond the table', P, nm, lab))
        # after the table: blank row(s) then next title / other block
        if any(c.value is not None for c in rows[k]):
            bad.append(('no blank after table', P, nm, rows[k][0].value))
    print(P, 'tables', len(tabs), names)

print('selection:')
for k, es in sel.items():
    for e in es:
        print('  ', k, '|', e['rel'], e['plane'], e['kind'], e['tgt'], e['score'], e['blocks'])
print('totals', tot)
print('MISMATCHES', len(bad))
for b in bad[:40]:
    print(' ', b)
