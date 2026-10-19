"""compare_raorder.py (19 Oct 2026): tables workbook after the RA-order change against the build before.
T1, T2, T24 star rows: matched by (sheet, label), every cell identical (value, fill, comment, border); order = T1_T2_T24_STARS.
SKY block star rows (SKY JUPITER, col A 'SKY'): matched by label; before minus Polaris (+ new stars) = after. Everything else: the
remaining rows, in order, identical (values; empty rows ignored).
usage: compare_raorder.py before.xlsx after.xlsx [batch_a.xlsx batch_b.xlsx]"""
import sys, openpyxl
sys.path.insert(0, 'tools')
from jupiter_tables import STARS, T1_T2_T24_STARS
ALL = set(STARS) | set(T1_T2_T24_STARS)


def star_of(r):
    a, b = r[0].value, r[1].value
    if a in ('T1', 'T2', 'SKY') and b and ' → ' in str(b):
        x = str(b).split(' → ')[1].split(' ', 1)[1]
        return x if x in ALL else None
    if a == 'T24' and b and not str(b).startswith('T24 '):
        return str(b).split(' ', 1)[1]
    return None


def cell_sig(c):
    return (c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None,
            c.border.left.style, c.border.right.style)


def split(ws):
    rest, keyed, order = [], {}, {}
    for r in ws.iter_rows():
        if not any(c.value is not None for c in r):
            continue
        x = star_of(r)
        if x:
            blk = r[0].value
            keyed[(blk, r[1].value)] = tuple(cell_sig(c) for c in r if c.value is not None or c.comment or c.fill.fill_type)
            order.setdefault((blk, str(r[1].value).split(' → ')[0] if blk != 'T24' else str(r[1].value)[0]), []).append(x)
        else:
            rest.append(tuple(c.value for c in r))
    return rest, keyed, order


b, a = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
bad, tot, skyd = [], 0, {}
assert b.sheetnames == a.sheetnames, (b.sheetnames, a.sheetnames)
for sh in b.sheetnames:
    if sh not in ('SKY JUPITER',) and not (sh.startswith('P') and sh[1:].isdigit()):
        rb = [tuple(r) for r in b[sh].iter_rows(values_only=True) if any(v is not None for v in r)]
        ra = [tuple(r) for r in a[sh].iter_rows(values_only=True) if any(v is not None for v in r)]
        if rb != ra:
            bad.append((sh, 'whole sheet differs'))
        continue
    (rb, kb, ob), (ra, ka, oa) = split(b[sh]), split(a[sh])
    if rb != ra:
        n = next(i for i in range(min(len(rb), len(ra))) if rb[i] != ra[i]) if any(x != y for x, y in zip(rb, ra)) else min(len(rb), len(ra))
        bad.append((sh, 'other rows differ', len(rb), len(ra), str(rb[n] if n < len(rb) else None)[:200], str(ra[n] if n < len(ra) else None)[:200]))
    for k in set(kb) | set(ka):
        if k[0] == 'SKY':
            if kb.get(k) != ka.get(k):
                skyd.setdefault(sh, {'gone': [], 'new': [], 'changed': []})['gone' if k not in ka else 'new' if k not in kb else 'changed'].append(k[1])
            continue
        tot += 1
        if kb.get(k) != ka.get(k):
            bad.append((sh, 'T1/T2/T24 cells differ', k))
    for k, v in oa.items():
        want = [x for x in T1_T2_T24_STARS if x in v]
        if k[0] != 'SKY' and v != want or k[0] == 'SKY' and v != [x for x in T1_T2_T24_STARS if x in v]:
            bad.append((sh, 'order', k))
    print(sh, {k: len(v) for k, v in oa.items()})
print('T1 / T2 / T24 star rows matched by label:', tot)
print('SKY block star rows:', {sh: {k: v for k, v in d.items() if v} for sh, d in skyd.items()})
print('differences beyond those:', len(bad))
for x in bad[:8]:
    print('  ', x)
if len(sys.argv) > 4:
    x, y = openpyxl.load_workbook(sys.argv[3], read_only=True), openpyxl.load_workbook(sys.argv[4], read_only=True)
    print('batch values identical:', x.sheetnames == y.sheetnames and all(
        [r for r in x[s].iter_rows(values_only=True)] == [r for r in y[s].iter_rows(values_only=True)] for s in x.sheetnames))
