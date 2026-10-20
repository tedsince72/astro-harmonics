"""T24 conjunction red fill (Eddie, 20 Oct 2026): compare a build before and after, every sheet, every cell.
Rule: a T24 SKY / HORSE / JOCKEY body cell or a T24 H / J distance cell is red (FF8080) exactly when RA < 1.5 / Dec < 0.3, otherwise its
fill is the one it had before; values, comments and borders identical everywhere; every other cell identical (fill too), apart from the
T24 title cells (note text). Usage: compare_red.py BEFORE.xlsx AFTER.xlsx  -> prints red counts per block and the mismatches."""
import sys, openpyxl

TOL = {'RA': 1.5, 'Dec': 0.3}
RED = '00FF8080'
rgb = lambda c: c.fill.start_color.rgb if c.fill and c.fill.fill_type else None
brd = lambda c: (c.border.left.style, c.border.right.style, c.border.top.style, c.border.bottom.style)
com = lambda c: c.comment.text if c.comment else None


def dist_cells(ws):
    """-> {(row, col): (block, plane)} for every T24 body cell and T24 H / J distance cell; title cells"""
    out, titles = {}, set()
    rows = list(ws.iter_rows(min_col=1, max_col=2, values_only=True))
    r = 1
    while r <= len(rows):
        a, b = rows[r - 1]
        if a in ('T24', 'T24 H / J') and r < len(rows) and rows[r][0] == 'table':
            titles.add((r, 2))
            blk = (b or '').split(' (')[0].split(':')[0] if a == 'T24' else 'T24 H / J'
            h1, h2 = r + 1, r + 2
            plane, cols = None, {}
            for c in range(3, ws.max_column + 1):
                v1, v2 = ws.cell(h1, c).value, ws.cell(h2, c).value
                if v1 in ('RA', 'Dec'):
                    plane = v1
                if v1 and str(v1).endswith('midpoints') or v2 is None:
                    continue
                if a == 'T24' or str(v2).startswith('d('):
                    cols[c] = plane
            rr = h2 + 1
            while rr <= len(rows) and rows[rr - 1][0] == a:
                for c, pl in cols.items():
                    out[(rr, c)] = (blk, pl)
                rr += 1
            r = rr
        else:
            r += 1
    return out, titles


def main(fb, fa):
    wb, wa = openpyxl.load_workbook(fb), openpyxl.load_workbook(fa)
    bad, counts = [], {}
    assert wb.sheetnames == wa.sheetnames, (wb.sheetnames, wa.sheetnames)
    for sn in wa.sheetnames:
        sb, sa = wb[sn], wa[sn]
        dc, titles = dist_cells(sa)
        dcb, _ = dist_cells(sb)
        if set(dc) != set(dcb):
            bad.append((sn, 'distance cell set differs'))
        for row_b, row_a in zip(sb.iter_rows(max_row=max(sb.max_row, sa.max_row), max_col=max(sb.max_column, sa.max_column)),
                                sa.iter_rows(max_row=max(sb.max_row, sa.max_row), max_col=max(sb.max_column, sa.max_column))):
            for cb, ca in zip(row_b, row_a):
                k = (ca.row, ca.column)
                if k in titles:
                    if ca.value != cb.value and not (ca.value or '').startswith((cb.value or '').split(':')[0]):
                        bad.append((sn, k, 'title'))
                    continue
                if (ca.value, com(ca), brd(ca)) != (cb.value, com(cb), brd(cb)):
                    bad.append((sn, k, 'value / comment / border', cb.value, ca.value))
                    continue
                if k in dc:
                    blk, pl = dc[k]
                    conj = isinstance(ca.value, (int, float)) and ca.value < TOL[pl]
                    key = (sn, blk)
                    counts.setdefault(key, [0, 0])
                    counts[key][1] += 1
                    if conj:
                        counts[key][0] += 1
                        if rgb(ca) != RED:
                            bad.append((sn, k, blk, pl, ca.value, 'conj not red', rgb(ca)))
                    elif rgb(ca) != rgb(cb) or rgb(ca) == RED:
                        bad.append((sn, k, blk, pl, ca.value, 'fill changed', rgb(cb), rgb(ca)))
                elif rgb(ca) != rgb(cb):
                    bad.append((sn, k, 'fill outside T24 distance cells', rgb(cb), rgb(ca)))
    for (sn, blk), (n, tot) in sorted(counts.items()):
        print(f'{sn:12s} {blk:12s} red {n:4d} of {tot}')
    titles_changed = sum(1 for sn in wa.sheetnames for k in dist_cells(wa[sn])[1] if wa[sn].cell(*k).value != wb[sn].cell(*k).value)
    print('title cells changed:', titles_changed)
    print('mismatches:', len(bad))
    for x in bad[:20]:
        print('  ', x)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
