import sys, openpyxl
def rows(ws):
    out, skip = [], 0
    it = list(ws.iter_rows())
    i = 0
    while i < len(it):
        r = it[i]
        if r[0].value == 'T24' and str(r[1].value).startswith('T24 '):
            i += 3
            while i < len(it) and it[i][0].value == 'T24':
                i += 1
            i += 1                      # blank row after the block
            skip += 1
            continue
        v = tuple(c.value for c in r)
        while v and v[-1] is None: v = v[:-1]
        f = tuple(c.fill.start_color.rgb if c.fill and c.fill.fill_type else None for c in r[:len(v)])
        if v: out.append((v, f))
        i += 1
    return out, skip
a, b = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
print('sheets equal', a.sheetnames == b.sheetnames)
tot = 0
for s in a.sheetnames:
    ra, _ = rows(a[s]); rb, k = rows(b[s])
    # drop trailing empties
    while ra and not ra[-1][0]: ra.pop()
    while rb and not rb[-1][0]: rb.pop()
    tot += k
    if ra != rb:
        d = next((i for i, (x, y) in enumerate(zip(ra, rb)) if x != y), min(len(ra), len(rb)))
        print('DIFF', s, len(ra), len(rb), d, ra[d][0][:4] if d < len(ra) else None, rb[d][0][:4] if d < len(rb) else None)
print('T24 blocks removed', tot)
