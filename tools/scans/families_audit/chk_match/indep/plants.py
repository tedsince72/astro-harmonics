"""Plant errors in copies of the after workbook and confirm the checkers catch each."""
import sys, os, copy, io, contextlib, openpyxl
from openpyxl.styles import PatternFill
sys.path.insert(0, os.path.dirname(__file__))
import check_match, compare_rest

old, new, tmp = sys.argv[1:4]
os.makedirs(tmp, exist_ok=True)


def rowof(ws, tab, sec, k=0):
    rs = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == tab and ws.cell(r, 2).value == sec]
    return rs[k]


def copyrow(ws, src, dst):
    for c in range(1, 20):
        a, b = ws.cell(src, c), ws.cell(dst, c)
        b.value = a.value; b.fill = copy.copy(a.fill)


def p1(ws):  # drop a row
    ws.delete_rows(rowof(ws, 'MATCH HORSE', 'RATIO', 5))
def p2(ws):  # swap two EXACT rows (first and last of EXACT, different lower scores)
    a = rowof(ws, 'MATCH HORSE', 'EXACT', 0); b = rowof(ws, 'MATCH HORSE', 'EXACT', 3)
    va = [(ws.cell(a, c).value, copy.copy(ws.cell(a, c).fill)) for c in range(1, 20)]
    copyrow(ws, b, a)
    for c, (v, f) in enumerate(va, 1): ws.cell(b, c).value = v; ws.cell(b, c).fill = f
def p3(ws):  # wrong factor
    r = rowof(ws, 'MATCH HORSE', 'RATIO', 0); ws.cell(r, 5).value = '4'
def p4(ws):  # wrong fill
    r = rowof(ws, 'MATCH JOCKEY', 'EXACT', 0); ws.cell(r, 11).fill = PatternFill('solid', fgColor='FFF8DC')
def p5(ws):  # extra row (duplicate inserted)
    r = rowof(ws, 'MATCH JOCKEY', 'RATIO', 2); ws.insert_rows(r); copyrow(ws, r + 1, r)
def p6(ws):  # changed value
    r = rowof(ws, 'MATCH JOCKEY', 'RATIO', 7); ws.cell(r, 15).value = ws.cell(r, 15).value + 0.000001
def p7(ws):  # title count
    r = [r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == 'MATCH HORSE'][0]
    ws.cell(r, 2).value = ws.cell(r, 2).value.replace('EXACT 9 rows', 'EXACT 8 rows')
def p8(ws):  # wrong ratio p/q
    r = rowof(ws, 'MATCH HORSE', 'RATIO', 10); ws.cell(r, 3).value = '2/1'
def p9(ws):  # changed non-MATCH cell (T24 JOCKEY value)
    ws.cell(490, 3).value = ws.cell(490, 3).value + 1
def p10(ws):  # wrong lower score
    r = rowof(ws, 'MATCH HORSE', 'RATIO', 20); ws.cell(r, 19).value = max(ws.cell(r, 11).value, ws.cell(r, 18).value)

plants = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
for p in plants:
    wb = openpyxl.load_workbook(new)
    p(wb['P01'])
    path = os.path.join(tmp, p.__name__ + '.xlsx'); wb.save(path)
    with contextlib.redirect_stdout(io.StringIO()):
        m = check_match.main(path, p.__name__)
        d = compare_rest.main(old, path, p.__name__) if p is p9 else []
    print(p.__name__, (p.__doc__ or ''), 'caught' if (m or d) else 'MISSED', len(m), len(d), (m or d)[:1])
