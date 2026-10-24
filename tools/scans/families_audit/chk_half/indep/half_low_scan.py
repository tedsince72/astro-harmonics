"""(g) every cell of a workbook naming the half targets 0.5 or 1.5 as a hit (target cells, T24 comments, leg family cells)"""
import sys, re, openpyxl
wb = openpyxl.load_workbook(sys.argv[1])
pat = re.compile(r'^(→ )?(0\.5|1\.5) (\(half|· half)')
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            for t in (c.value if isinstance(c.value, str) else None, c.comment.text.split('\n')[0] if c.comment else None):
                if t and pat.match(t) and 'outside' not in t:
                    print(ws.title, c.coordinate, row[0].value, row[1].value, repr(t[:60]))
# second pass: leg cells (T19 / PAIRS / SKY PAIRS) with their plane (col D) and value (the cell before), RA and value < 1.5 flagged
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            t = c.value if isinstance(c.value, str) else ''
            if pat.match(t) and t.startswith('→'):
                v = ws.cell(c.row, c.column - 1).value
                pl = ws.cell(c.row, 4).value
                print('  leg', ws.title, c.coordinate, ws.cell(c.row, 3).value, pl, v, 'CONJ RANGE' if pl == 'RA' and v < 1.5 else '')
