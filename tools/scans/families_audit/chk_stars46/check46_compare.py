"""check46_compare.py (independent checker, 20 Oct 2026): where the 11 new stars appear, and before (35) vs after (46).
Own code. For every sheet: the rows naming one of the 11 are taken out of the after build; the rest must equal the before build in
order (value, fill, comment, border of every cell); differing rows are printed (only count titles may differ). Default vs --full sheets.
usage: check46_compare.py <S dir>"""
import sys, re, difflib, collections, os
import openpyxl

S = sys.argv[1]
NEW11 = ['Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Menkar', 'Phact', 'Adhara', 'Wezen', 'Menkent', 'Unukalhai', 'Rasalhague']
RX = re.compile(r'\b(' + '|'.join(NEW11) + r')\b')


def fill(c):
    return c.fill.start_color.rgb if c.fill is not None and c.fill.fill_type else None


def sig(row):
    out = []
    for c in row:
        b = c.border
        out.append((c.value, fill(c), c.comment.text if c.comment else None, b.left.style, b.top.style))
    while out and out[-1] == (None, None, None, None, None):
        out.pop()
    return tuple(out)


def names_new(row):
    return any(isinstance(c.value, str) and RX.search(c.value) for c in row) or \
        any(c.comment is not None and RX.search(c.comment.text) for c in row)


def rows(ws):
    return [r for r in ws.iter_rows() if any(c.value is not None for c in r)]


def where_new(wb):
    loc = collections.Counter()
    for sh in wb.sheetnames:
        for r in rows(wb[sh]):
            if names_new(r):
                loc[(sh, str(r[0].value)[:28])] += 1
    return loc


def compare(bp, ap, strip=True):
    b, a = openpyxl.load_workbook(bp), openpyxl.load_workbook(ap)
    print(f'== {os.path.basename(ap)} vs before; sheets equal: {b.sheetnames == a.sheetnames}')
    bad = 0
    for sh in b.sheetnames:
        rb, ra = rows(b[sh]), rows(a[sh])
        keep = [r for r in ra if not (strip and names_new(r))]
        sb, sa = [sig(r) for r in rb], [sig(r) for r in keep]
        ops = [o for o in difflib.SequenceMatcher(None, sb, sa, autojunk=False).get_opcodes() if o[0] != 'equal']
        nd = sum(max(i2 - i1, j2 - j1) for _, i1, i2, j1, j2 in ops)
        print(f'  {sh}: before {len(rb)}, after {len(ra)}, removed (naming one of the 11) {len(ra) - len(keep)}, other differing rows {nd}')
        for op, i1, i2, j1, j2 in ops:
            for k in range(max(i2 - i1, j2 - j1)):
                x = sb[i1 + k] if i1 + k < i2 else None
                y = sa[j1 + k] if j1 + k < j2 else None
                # describe: which cells differ
                if x and y:
                    dif = [(i, x[i] if i < len(x) else None, y[i] if i < len(y) else None) for i in range(max(len(x), len(y)))
                           if (x[i] if i < len(x) else None) != (y[i] if i < len(y) else None)]
                    print(f'     {op} row: {str(x[0][0])[:50]!r} cells differ {[(i, str(p[0])[-70:] if p else p, str(q[0])[-70:] if q else q) for i, p, q in dif][:4]}')
                    # a "title" difference = one text cell, only numbers changed
                    t = [(p, q) for _, p, q in dif]
                    title = len(t) == 1 and isinstance(t[0][0][0], str) and isinstance(t[0][1][0], str) and \
                        re.sub(r'\d+', '#', t[0][0][0]) == re.sub(r'\d+', '#', t[0][1][0]) and t[0][0][1:] == t[0][1][1:]
                    if not title:
                        bad += 1
                        print('       ^ NOT a count-only title change')
                else:
                    bad += 1
                    print(f'     {op} row only in {"before" if x else "after"}: {str((x or y)[:3])[:200]}')
    print('  non-title differences:', bad)
    return bad


def defaults(dp, fp):
    d, f = openpyxl.load_workbook(dp), openpyxl.load_workbook(fp)
    print(f'== default {os.path.basename(dp)}: sheets {d.sheetnames}')
    for sh in d.sheetnames:
        a, b = [sig(r) for r in rows(d[sh])], [sig(r) for r in rows(f[sh])]
        print(f'  {sh}: default rows {len(a)}, full rows {len(b)}, identical {a == b}')


if __name__ == '__main__':
    A, B = f'{S}/after', f'{S}/before'
    asc, lin = 'race_batch_20120619_ascot_1430', 'race_batch_20210402_lingfield_aw_1435'
    for w in (f'{A}/{asc}_full.xlsx', f'{A}/{asc}_full_pairs.xlsx', f'{A}/{lin}_full.xlsx', f'{A}/{lin}_full_pairs.xlsx'):
        loc = where_new(openpyxl.load_workbook(w))
        print(f'== rows naming one of the 11 in {os.path.basename(w)}: {sum(loc.values())}')
        for k, v in sorted(loc.items()):
            print(f'     {k}: {v}')
    tot = 0
    tot += compare(f'{B}/{asc}_full.xlsx', f'{A}/{asc}_full.xlsx')
    tot += compare(f'{B}/{asc}_full_pairs.xlsx', f'{A}/{asc}_full_pairs.xlsx')
    tot += compare(f'{B}/{lin}_full.xlsx', f'{A}/{lin}_full.xlsx', strip=False)
    tot += compare(f'{B}/{lin}_full_pairs.xlsx', f'{A}/{lin}_full_pairs.xlsx', strip=False)
    tot += compare(f'{B}/{lin}_def.xlsx', f'{A}/{lin}_def.xlsx', strip=False)
    defaults(f'{A}/{asc}_def.xlsx', f'{A}/{asc}_full.xlsx')
    defaults(f'{A}/{lin}_def.xlsx', f'{A}/{lin}_full.xlsx')
    print('TOTAL non-title differences:', tot)
