"""Planted errors on a copy of an after workbook; check.py must catch each. usage: plants.py <before> <after> <outdir>"""
import copy
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402
import lib as L  # noqa: E402


def snap(ws, r, n=29):
    return [(ws.cell(r, c).value, copy.copy(ws.cell(r, c).fill), copy.copy(ws.cell(r, c).font)) for c in range(1, n + 1)]


def put(ws, r, s):
    for c, (v, f, fo) in enumerate(s, 1):
        ws.cell(r, c).value = v
        ws.cell(r, c).fill = f
        ws.cell(r, c).font = fo


def rows_with(ws, a, pred):
    return [r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == a and pred(r)]


def sec_band(ws, a, sec):
    return next(r for r in rows_with(ws, a, lambda r: ws.cell(r, 2).value == sec and L.fillrgb(ws.cell(r, 2)) == L.SEC_FILL))


def move(ws, src, dst):
    """move row src to position dst (dst < src): rows dst..src-1 shift down by one"""
    rows = [snap(ws, r) for r in range(dst, src + 1)]
    new = [rows[-1]] + rows[:-1]
    for k, s in enumerate(new):
        put(ws, dst + k, s)


def plant(after, kind):
    wb = openpyxl.load_workbook(after)
    ws = wb['P01']
    if kind == 'a':   # a SUN row moved to the end of the JUPITER section (MATCH HORSE)
        sun = sec_band(ws, 'MATCH HORSE', 'SUN')
        first = next(r for r in range(sun + 1, sun + 50) if ws.cell(r, 2).value in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR'))
        move(ws, first, sun)
        return wb, f'P01 MATCH HORSE row {first} (SUN) moved to row {sun} (end of JUPITER)'
    if kind == 'b':   # a JUPITER-section value changed
        jup = sec_band(ws, 'MATCH HORSE', 'JUPITER')
        r = next(r for r in range(jup + 1, jup + 50) if ws.cell(r, 2).value in ('EXACT', 'RATIO'))
        ws.cell(r, 20).value = ws.cell(r, 20).value + 0.01
        return wb, f'P01 MATCH HORSE T{r} +0.01'
    if kind == 'c':   # missing section band (MATCH JOCKEY SUN)
        sun = sec_band(ws, 'MATCH JOCKEY', 'SUN')
        end = sun
        while ws.cell(end + 1, 1).value == 'MATCH JOCKEY':
            end += 1
        rows = [snap(ws, r) for r in range(sun + 1, end + 1)]
        for k, s in enumerate(rows):
            put(ws, sun + k, s)
        put(ws, end, [(None, openpyxl.styles.PatternFill(), openpyxl.styles.Font())] * 29)
        return wb, f'P01 MATCH JOCKEY SUN band (row {sun}) removed'
    if kind == 'd':   # a SUN horse row placed on a JUPITER HJ line (horse side empty, jockey present)
        a = 'MATCH HORSE | JOCKEY'
        jup, sun = sec_band(ws, a, 'JUPITER'), sec_band(ws, a, 'SUN')
        tgt = next(r for r in range(jup + 1, sun) if ws.cell(r, 2).value in ('EXACT', 'RATIO') and ws.cell(r, 14).value is None
                   and ws.cell(r, 22).value is not None)
        src = next(r for r in range(sun + 1, sun + 60) if ws.cell(r, 2).value in ('EXACT', 'RATIO', 'BODY') and ws.cell(r, 14).value)
        for c in range(14, 22):
            ws.cell(tgt, c).value = ws.cell(src, c).value
            ws.cell(src, c).value = None
        return wb, f'P01 HJ horse side of SUN line {src} moved onto JUPITER line {tgt}'
    if kind == 'e':   # a SUMMARY SUN line moved under the JUPITER band (P01 block)
        ws = wb['SUMMARY']
        a = 'MATCH HORSE | JOCKEY'
        sun = sec_band(ws, a, 'SUN')
        first = next(r for r in range(sun + 1, sun + 60) if ws.cell(r, 2).value in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR'))
        move(ws, first, sun)
        return wb, f'SUMMARY row {first} (P01 SUN line) moved to row {sun} (under JUPITER)'
    raise ValueError(kind)


if __name__ == '__main__':
    before, after, out = sys.argv[1:4]
    for k in 'abcde':
        wb, what = plant(after, k)
        f = Path(out) / f'plant_{k}.xlsx'
        wb.save(f)
        errs = check.check(before, str(f), quiet=True)
        print(f'plant {k}: {what}: {"CAUGHT" if errs else "MISSED"} ({len(errs)} mismatches); first: {errs[0] if errs else "-"}')
