import sys, openpyxl
def grids(f, new):
    w = openpyxl.load_workbook(f); out = {}; mids = {}
    for s in w.sheetnames:
        if not (s == 'SKY JUPITER' or (s.startswith('P') and s[1:].isdigit())): continue
        it = list(w[s].iter_rows()); i = 0
        while i < len(it):
            r = it[i]
            if r[0].value == 'T24' and str(r[1].value).startswith('T24 '):
                blk = r[1].value.split(' (')[0]; h1, h2 = it[i + 1], it[i + 2]; i += 3
                cols = {}
                if new:
                    pl = None
                    for c in range(2, len(h1)):
                        if h1[c].value in ('RA', 'Dec'): pl = h1[c].value
                        if h2[c].value and not str(h1[c].value or '').endswith('midpoints'): cols[c] = (h2[c].value, pl)
                        elif str(h1[c].value or '').endswith('midpoints'): cols[c] = ('MID', h1[c].value.split()[0])
                else:
                    for c in range(2, len(h2)):
                        if h2[c].value in ('RA', 'Dec'): cols[c] = (h1[c].value if h2[c].value == 'RA' else h1[c - 1].value, h2[c].value)
                order = [cols[c] for c in sorted(cols)]
                out[(s, blk, '_order')] = order
                while i < len(it) and it[i][0].value == 'T24':
                    for c, (b, pl) in cols.items():
                        x = it[i][c]
                        if b == 'MID':
                            mids[(s, blk, it[i][1].value, pl)] = (x.value, x.fill.start_color.rgb if x.fill.fill_type else None)
                        else:
                            out[(s, blk, it[i][1].value, b, pl)] = (x.value, x.fill.start_color.rgb if x.fill.fill_type else None,
                                                                    x.comment.text if x.comment else None, x.border.left.style)
                    i += 1
            i += 1
    return out, mids
for new, old in zip(sys.argv[1::2], sys.argv[2::2]):
    a, m = grids(new, True); b, _ = grids(old, False)
    bad = []; nthick = 0
    for k, v in b.items():
        if k[2] == '_order': continue
        g = a.get(k)
        if g is None or g[0] != v[0] or g[1] != v[1] or not g[2].startswith(v[2]): bad.append(k); continue
        extra = g[2][len(v[2]):]
        if extra and not all(l.startswith('midpoint with ') for l in extra.strip('\n').split('\n')): bad.append(('extra', k))
        if (g[3] == 'thick') != bool(extra): bad.append(('border', k))
        nthick += g[3] == 'thick'
    order_ok = all(a[(s, blk, '_order')][:len(a[(s, blk, '_order')])] and
                   [o for o in a[(s, blk, '_order')] if o[1] == 'RA' and o[0] != 'MID'] + [o for o in a[(s, blk, '_order')] if o[1] == 'Dec' and o[0] != 'MID']
                   == [o for o in a[(s, blk, '_order')] if o[0] != 'MID'] for (s, blk, _) in [k for k in a if k[2] == '_order'])
    cnt = {}
    for (s, blk, star, pl), (v, f) in m.items():
        if v: cnt.setdefault((s, blk), [0, 0]); cnt[(s, blk)][pl == 'Dec'] += v.count(';') + 1
    print(new.split('/')[-1], 'cells', len([k for k in b if k[2] != '_order']), 'mismatch', len(bad), bad[:3], 'thick', nthick, 'RA-then-Dec', order_ok)
    for k, v in sorted(cnt.items()): print('  ', k, 'RA', v[0], 'Dec', v[1])
