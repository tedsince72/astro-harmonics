"""compare_rmsel.py (Eddie, 22 Oct 2026: T24 STAR SELECT removed from the runner sheets): BEFORE.xlsx AFTER.xlsx [BEFORE_pairs AFTER_pairs]
- every sheet: after = before minus exactly the T24 STAR SELECT rows (column A 'T24 STAR SELECT': titles, headers, body rows) and the blank
  rows inside / right after that region (the region runs from its first row to the row before the next written block), row for row:
  values, fills, comments, borders, number formats; merged ranges shifted by the rows removed; no 'T24 STAR SELECT' anywhere in the after;
- optional: the pairs workbooks identical cell by cell.
Prints per sheet the rows removed and 'mismatches: n'."""
import sys, openpyxl


def sig(c):
    b = c.border
    return (c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None,
            tuple(getattr(b, s).style if b and getattr(b, s) else None for s in ('left', 'right', 'top', 'bottom')), c.number_format)


def grid(ws):
    out = [tuple(sig(c) for c in r) for r in ws.iter_rows(min_row=1, max_row=ws.max_row)]
    return [tuple(x for x in r) for r in out]


def strip(r):
    r = list(r)
    while r and r[-1] == (None, None, None, (None,) * 4, 'General'):
        r.pop()
    return tuple(r)


def empty(r):
    return not strip(r)


def main(fb, fa, pb=None, pa=None):
    wb, wa = openpyxl.load_workbook(fb), openpyxl.load_workbook(fa)
    bad = []
    if wb.sheetnames != wa.sheetnames:
        bad.append(('sheet names', wb.sheetnames, wa.sheetnames))
    for sh in wa.sheetnames:
        gb, ga = [strip(r) for r in grid(wb[sh])], [strip(r) for r in grid(wa[sh])]
        if any(r and r[0][0] == 'T24 STAR SELECT' for r in ga) or any('T24 STAR SELECT' in str(c[0]) for r in ga for c in r if c[0]):
            bad.append((sh, 'T24 STAR SELECT still present'))
        ix = [i for i, r in enumerate(gb) if r and r[0][0] == 'T24 STAR SELECT']
        cut = set()
        if ix:
            j = ix[-1] + 1
            while j < len(gb) and empty(gb[j]):
                j += 1
            # before: T24 JOCKEY RATIOS, one blank row, the SELECT tables, their blank rows, the next block; without SELECT the next block
            # starts where the first SELECT row was: the cut is the first SELECT row .. the row before the next block
            k = ix[0]
            cut = set(range(k, j))
            if any(not empty(gb[i]) and gb[i][0][0] not in ('T24 STAR SELECT', 'table', None) for i in cut):
                bad.append((sh, 'cut region holds another block'))
        rest = [r for i, r in enumerate(gb) if i not in cut]
        while rest and empty(rest[-1]):
            rest.pop()
        ga_ = list(ga)
        while ga_ and empty(ga_[-1]):
            ga_.pop()
        if rest != ga_:
            n = sum(1 for x, y in zip(rest, ga_) if x != y) + abs(len(rest) - len(ga_))
            first = next((i for i, (x, y) in enumerate(zip(rest, ga_)) if x != y), min(len(rest), len(ga_)))
            bad.append((sh, f'{n} rows differ', f'first at after row {first + 1}'))
        sh_ = lambda r: r - len(cut) if cut and r > max(cut) else r
        mb = sorted((sh_(m.min_row), m.min_col, sh_(m.max_row), m.max_col) for m in wb[sh].merged_cells.ranges
                    if not (cut and m.min_row - 1 in cut))
        ma = sorted((m.min_row, m.min_col, m.max_row, m.max_col) for m in wa[sh].merged_cells.ranges)
        if mb != ma:
            bad.append((sh, 'merged ranges differ', len(mb), len(ma)))
        nsel = sum(1 for i in ix if str(gb[i][1][0] or '').startswith('T24 STAR SELECT —'))
        if ix or sh.startswith('P'):
            print(f'{sh}: before {len(gb)} rows, removed {len(cut)} ({len(ix)} T24 STAR SELECT rows, {nsel} tables), after {len(ga)} rows')
    if pb:
        for f, g in ((pb, pa),):
            xb, xa = openpyxl.load_workbook(f), openpyxl.load_workbook(g)
            if xb.sheetnames != xa.sheetnames or any([strip(r) for r in grid(xb[s])] != [strip(r) for r in grid(xa[s])] for s in xb.sheetnames):
                bad.append(('pairs workbook differs',))
            else:
                print(f'pairs identical ({len(xb.sheetnames)} sheets)')
    print('mismatches:', len(bad))
    for x in bad[:10]:
        print('  ', x)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(*sys.argv[1:]) else 1)
