"""Planted errors for check_hj.py. usage: plants.py <scratch S> <outdir>"""
import sys, os, subprocess, copy
from collections import defaultdict
import openpyxl
from openpyxl.styles import PatternFill

S, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))
NEW = 'MATCH HORSE | JOCKEY'
SRC_AFTER = f'{S}/ripon_after.xlsx'
SRC_BEFORE = f'{S}/ripon_before.xlsx'


def cp(dst, src):
    dst.value = src.value
    dst._style = copy.copy(src._style)
    dst.comment = copy.copy(src.comment) if src.comment else None


def table(ws):
    rows = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == NEW]
    data = [r for r in rows if ws.cell(r, 2).value in ('EXACT', 'RATIO')]
    hdrs = [r for r in rows if ' — EXACT ' in str(ws.cell(r, 2).value)]
    return data, hdrs


def key(ws, r):
    return (ws.cell(r, 8).value, ws.cell(r, 9).value, ws.cell(r, 2).value, ws.cell(r, 3).value)


def swap_cols(ws, r1, r2, c0, c1):
    for c in range(c0, c1 + 1):
        a, b = ws.cell(r1, c), ws.cell(r2, c)
        va, sa, ca = a.value, copy.copy(a._style), a.comment
        cp(a, b)
        b.value, b._style, b.comment = va, sa, ca


def has(ws, r, side):
    return ws.cell(r, 14 if side == 'h' else 22).value is not None


def plant(name, fn, with_before=False):
    wb = openpyxl.load_workbook(SRC_AFTER)
    ws = wb['P01']
    desc = fn(ws)
    p = f'{OUT}/{name}.xlsx'
    wb.save(p)
    args = [PY, f'{HERE}/check_hj.py', SRC_BEFORE, p] + ([] if with_before else ['--no-before'])
    out = subprocess.run(args, capture_output=True, text=True).stdout
    mm = [l for l in out.splitlines() if l.startswith('mismatches')]
    first = [l.strip() for l in out.splitlines() if l.startswith('   ')][:2]
    print(f'{name}: {desc}\n   -> {mm[0] if mm else out[-500:]}  {first}')


def control(ws):
    return 'unchanged re-save (control)'


def a_missing(ws):
    data, _ = table(ws)
    r = next(r for r in data if has(ws, r, 'h') and has(ws, r, 'j'))
    for c in range(14, 22):
        ws.cell(r, c).value = None
        ws.cell(r, c)._style = copy.copy(ws.cell(r, 40)._style)
    return f'horse side of row {r} cleared (source row missing)'


def a2_line_deleted(ws):
    data, _ = table(ws)
    r = data[5]
    ws.delete_rows(r)
    return f'line {r} deleted'


def b_dup(ws):
    data, _ = table(ws)
    r = data[3]
    ws.insert_rows(r + 1)
    for c in range(1, 30):
        cp(ws.cell(r + 1, c), ws.cell(r, c))
    return f'line {r} duplicated'


def b2_dup_in_empty(ws):
    data, _ = table(ws)
    r = next(r for r in data if not has(ws, r, 'j'))
    src = next(x for x in data if has(ws, x, 'j') and key(ws, x) == key(ws, r)) if any(
        has(ws, x, 'j') and key(ws, x) == key(ws, r) for x in data) else next(x for x in data if has(ws, x, 'j'))
    for c in range(22, 30):
        cp(ws.cell(r, c), ws.cell(src, c))
    return f'jockey side of {src} also copied into the empty jockey side of {r}'


def c_pair_same_key(ws):
    data, _ = table(ws)
    by = defaultdict(list)
    for r in data:
        if has(ws, r, 'j') and has(ws, r, 'h'):
            by[key(ws, r) + (ws.cell(r, 18).value, ws.cell(r, 19).value)].append(r)
    k, rs = next((k, v) for k, v in by.items() if len(v) >= 2)
    swap_cols(ws, rs[0], rs[1], 22, 29)
    return f'jockey sides of {rs[0]} and {rs[1]} swapped (same key {k})'


def c_pair_cross_key(ws):
    data, _ = table(ws)
    both = [r for r in data if has(ws, r, 'j') and has(ws, r, 'h')]
    r1, r2 = both[1], both[2]
    swap_cols(ws, r1, r2, 22, 29)
    return f'jockey sides of {r1} and {r2} swapped (different keys)'


def d_lines(ws):
    data, _ = table(ws)
    r1 = next(r for r, s in zip(data, data[1:]) if s == r + 1 and ws.cell(r, 8).value == ws.cell(s, 8).value
              and key(ws, r) != key(ws, s))
    swap_cols(ws, r1, r1 + 1, 1, 29)
    return f'lines {r1} and {r1 + 1} swapped'


def d_groups(ws):
    data, hdrs = table(ws)
    # two consecutive one-line groups, or swap header+first line of group 1 with group 2 header (+line)
    for h1, h2 in zip(hdrs, hdrs[1:]):
        if h2 == h1 + 2:
            h3 = h2 + 2
            if ws.cell(h3, 2).value is not None and ' — EXACT ' in str(ws.cell(h3, 2).value) or ws.cell(h3, 1).value is None:
                swap_cols(ws, h1, h2, 1, 29)
                swap_cols(ws, h1 + 1, h2 + 1, 1, 29)
                return f'groups at {h1} and {h2} swapped'
    raise SystemExit('no one-line groups')


def e_hdr_count(ws):
    _, hdrs = table(ws)
    r = next(h for h in hdrs if 'RATIO 42 | 45' in str(ws.cell(h, 2).value) and ws.cell(h, 2).value.startswith('S Jupiter'))
    ws.cell(r, 2).value = ws.cell(r, 2).value.replace('RATIO 42 | 45', 'RATIO 42 | 44')
    return f'header B{r} count changed: {ws.cell(r, 2).value}'


def f_grey(ws):
    _, hdrs = table(ws)
    ws.cell(hdrs[2], 29).fill = PatternFill(fill_type=None)
    return f'grey removed from AC{hdrs[2]}'


def f2_grey_extra(ws):
    _, hdrs = table(ws)
    ws.cell(hdrs[2], 30).fill = PatternFill('solid', fgColor='D9D9D9')
    return f'grey added at AD{hdrs[2]}'


def g_elsewhere(ws):
    ws.cell(10, 5).value = (ws.cell(10, 5).value or 0) + 1 if isinstance(ws.cell(10, 5).value, (int, float)) else 'x'
    return 'P01!E10 changed (outside the new table)'


def h_title(ws):
    _, _ = table(ws)
    r = next(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == NEW)
    ws.cell(r, 2).value = ws.cell(r, 2).value.replace('56 with both sides', '57 with both sides')
    return 'title total both 56 -> 57'


def i_side_swap(ws):
    data, _ = table(ws)
    r = next(r for r in data if has(ws, r, 'h') and not has(ws, r, 'j'))
    for c in range(14, 22):
        cp(ws.cell(r, c + 8), ws.cell(r, c))
        ws.cell(r, c).value = None
        ws.cell(r, c)._style = copy.copy(ws.cell(r, 40)._style)
    return f'horse row {r} moved to the jockey side'


def j_fill(ws):
    data, _ = table(ws)
    r = data[0]
    ws.cell(r, 20).fill = PatternFill('solid', fgColor='C6EFCE')
    return f'T20{r} fill changed'


def k_value(ws):
    data, _ = table(ws)
    r = data[7]
    ws.cell(r, 13).value = round(ws.cell(r, 13).value + 0.01, 2)
    return f'sky score M{r} +0.01'


ONLY = sys.argv[3:] 
for n, f, wbf in [('control', control, True), ('a_missing', a_missing, False), ('a2_line_deleted', a2_line_deleted, False),
                  ('b_dup', b_dup, False), ('b2_dup_in_empty', b2_dup_in_empty, False),
                  ('c_pair_same_key', c_pair_same_key, False), ('c_pair_cross_key', c_pair_cross_key, False),
                  ('d_lines', d_lines, False), ('d_groups', d_groups, False), ('e_hdr_count', e_hdr_count, False),
                  ('f_grey', f_grey, False), ('f2_grey_extra', f2_grey_extra, False), ('g_elsewhere', g_elsewhere, True),
                  ('h_title', h_title, False), ('i_side_swap', i_side_swap, False), ('j_fill', j_fill, False),
                  ('k_value', k_value, False)]:
    if not ONLY or n in ONLY:
        plant(n, f, wbf)
