"""Whole numbers on the target (Eddie, 27 Oct 2026): before / after diff of one tables workbook (and its pairs workbook).
usage: diff_whole.py <before.xlsx> <after.xlsx>
Rows aligned per sheet (difflib on the row signature: values, fill, comment); prints every changed cell, every inserted / dropped row,
and whether the row holds a value 0.98 < v < 1 (a cell value, or a number in a text / comment). Last line: 'rows changed: n | ... '."""
import sys, re, difflib
import openpyxl

NUM = re.compile(r'(?<![\d.])0\.98\d*|(?<![\d.])0\.99\d*')


def sig(c):
    return (c.value, c.fill.start_color.rgb if c.fill.fill_type else None, c.comment.text if c.comment else None,
            c.border.left.style if c.border and c.border.left else None)


def rows(ws):
    out = []
    for r in ws.iter_rows():
        out.append(tuple(sig(c) for c in r))
    while out and not any(v != (None, None, None, None) for v in out[-1]):
        out.pop()
    return [tuple(x for x in r) for r in out]


def near1(row):
    for v, f, cm, b in row:
        if isinstance(v, (int, float)) and 0.98 < v < 1.0:
            return True
        for t in (v, cm):
            if isinstance(t, str) and any(0.98 < float(m) < 1.0 for m in NUM.findall(t)):
                return True
    return False


def show(row, n=6):
    return [v for v, f, cm, b in row if v is not None][:n]


def main(bp, ap):
    tot = {'changed': 0, 'ins': 0, 'del': 0, 'near1': 0, 'other': 0}
    for b_, a_ in ((bp, ap), (bp.replace('_jupiter_tables', '_pairs'), ap.replace('_jupiter_tables', '_pairs'))):
        B, A = openpyxl.load_workbook(b_), openpyxl.load_workbook(a_)
        if B.sheetnames != A.sheetnames:
            print('SHEETS DIFFER', B.sheetnames, A.sheetnames)
        for sh in B.sheetnames:
            rb, ra = rows(B[sh]), rows(A[sh])
            if rb == ra:
                continue
            sm = difflib.SequenceMatcher(None, rb, ra, autojunk=False)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op == 'equal':
                    continue
                if op == 'replace' and i2 - i1 == j2 - j1:
                    for k in range(i2 - i1):
                        x, y = rb[i1 + k], ra[j1 + k]
                        cells = [(c + 1, x[c] if c < len(x) else None, y[c] if c < len(y) else None) for c in range(max(len(x), len(y)))
                                 if (x[c] if c < len(x) else None) != (y[c] if c < len(y) else None)]
                        nr = near1(x) or near1(y)
                        tot['changed'] += 1
                        tot['near1' if nr else 'other'] += 1
                        print(f'CHANGED {sh} row {i1 + k + 1}->{j1 + k + 1} [{"0.98-1" if nr else "FOLLOWS"}] {show(y)}')
                        for c, u, w in cells:
                            print(f'    col {c}: {u[0] if u else None!r} -> {w[0] if w else None!r}'
                                  + (f' | comment {u[2]!r} -> {w[2]!r}' if (u and u[2]) != (w and w[2]) else '')
                                  + (f' | fill {u[1]} -> {w[1]}' if (u and u[1]) != (w and w[1]) else ''))
                else:
                    for k in range(i1, i2):
                        nr = near1(rb[k]); tot['del'] += 1; tot['near1' if nr else 'other'] += 1
                        print(f'DROPPED {sh} row {k + 1} [{"0.98-1" if nr else "FOLLOWS"}] {show(rb[k], 12)}')
                    for k in range(j1, j2):
                        nr = near1(ra[k]); tot['ins'] += 1; tot['near1' if nr else 'other'] += 1
                        print(f'ADDED {sh} row {k + 1} [{"0.98-1" if nr else "FOLLOWS"}] {show(ra[k], 12)}')
    print(f"rows changed: {tot['changed']} | dropped: {tot['del']} | added: {tot['ins']} | with a 0.98-1 value: {tot['near1']} | follow-on: {tot['other']}")


main(sys.argv[1], sys.argv[2])
