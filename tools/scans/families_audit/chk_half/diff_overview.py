"""diff_overview.py BEFORE AFTER: per sheet, rows (by position) and whether row count / content differ - a first look"""
import sys, openpyxl
def sig(r):
    return tuple((c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None) for c in r)
wb, wa = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
for sh in wa.sheetnames:
    rb = [sig(r) for r in wb[sh].iter_rows()]; ra = [sig(r) for r in wa[sh].iter_rows()]
    tb = {}
    for r in rb: tb[r[0][0]] = tb.get(r[0][0], 0) + 1
    ta = {}
    for r in ra: ta[r[0][0]] = ta.get(r[0][0], 0) + 1
    nd = sum(1 for x, y in zip(rb, ra) if x != y)
    print(sh, len(rb), len(ra), 'pos-diff', nd, 'count changes', {k: (tb.get(k, 0), ta.get(k, 0)) for k in set(tb) | set(ta) if tb.get(k, 0) != ta.get(k, 0)})
