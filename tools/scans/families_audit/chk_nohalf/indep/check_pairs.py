"""Pair blocks (SKY PAIRS / SKY STARS / SKY ROYAL / SKY EQ): every leg cell 'd(...)' + family text in the after workbook
recomputed from its shown value with the no-half rules (best family + score); the NO RATIO OR MIDPOINT HIT blocks: every
before row is kept in after exactly when all three legs still have a family hit without half.
usage: check_pairs.py <old.xlsx> <new.xlsx>"""
import re, sys, collections
import openpyxl
sys.path.insert(0, __import__('os').path.dirname(__file__))
import ifam

LEG = re.compile(r'^→ (.*) \((whole|half|golden|phi power|ninth|sqrt2|silver|conj), (\S+)\)')


def legs(path):
    ws = openpyxl.load_workbook(path)['SKY JUPITER']
    hdr, block = None, None
    out = []
    for row in ws.iter_rows(max_col=30):
        a = row[0].value
        if isinstance(a, str) and a.startswith(('SKY PAIRS', 'SKY STARS', 'SKY ROYAL')) and row[1].value is None:
            block = a.split(' (')[0][:60]
        if a == 'table':
            hdr = {c.column: c.value for c in row}
            continue
        if hdr and isinstance(a, str) and a in ('SKY PAIRS', 'SKY STARS', 'SKY ROYAL') and row[1].value:
            out.append((block, row, hdr))
    return out


def check_after(path):
    n = collections.Counter(); bad = []
    for block, row, hdr in legs(path):
        plane = row[3].value
        for vc in (5, 7, 9):
            if not str(hdr.get(vc, '')).startswith('d('):
                continue
            v, t = row[vc - 1].value, row[vc].value
            if not isinstance(v, (int, float)):
                continue
            n['legs'] += 1
            together = 'together' in str(row[16].value or '') or 'together' in ' '.join(str(c.value) for c in row)
            e = ifam.evaluate(v, plane if plane != 'Equator' else 'Equator')
            if 'half' in str(t):
                bad.append(f'r{row[0].row} half text {t!r}')
            if e['hit']:
                m = LEG.match(str(t))
                if together and not m:
                    n['together leg plain'] += 1
                    continue
                ok = bool(m) and m.group(2) == e['fam'] and (e['fam'] == 'conj' or ifam.label_eq(e['fam'], ifam.parse_label(e['fam'], m.group(1)), e['lab'])) \
                    and abs(float(m.group(3)) - round(e['score'], 2)) <= 0.0101
                if not ok:
                    bad.append(f'r{row[0].row} {row[2].value} {plane} {hdr[vc]} {v}: {t!r} vs {e["fam"]} {e["lab"]} {e["score"]:.2f}')
                n['leg hits'] += 1
            else:
                if t != 'no family':
                    bad.append(f'r{row[0].row} {row[2].value} {plane} {hdr[vc]} {v}: {t!r} vs no family')
    return n, bad


def noratio(path):
    rows = {}
    for block, row, hdr in legs(path):
        if 'NO RATIO' in block:
            rows[(row[0].value, row[2].value, row[3].value)] = [row[c - 1].value for c in (5, 7, 9)]
    return rows


if __name__ == '__main__':
    old, new = sys.argv[1], sys.argv[2]
    n, bad = check_after(new)
    print(new.split('/')[-1], dict(n), 'leg errors', len(bad))
    for b in bad[:20]:
        print('   ', b)
    ro, rn = noratio(old), noratio(new)
    keep_bad = []
    for k, vals in ro.items():
        plane = k[2]
        allhit = all(ifam.evaluate(v, plane)['hit'] for v in vals)
        if allhit != (k in rn):
            keep_bad.append((k, vals, allhit, k in rn))
    extra = [k for k in rn if k not in ro]
    print(f'  NO RATIO rows before {len(ro)}, after {len(rn)}, dropped {len(ro) - len(rn) + len(extra)}, '
          f'kept/dropped vs rule mismatches {len(keep_bad)}, new rows {len(extra)}')
    for k in keep_bad[:10]:
        print('   ', k)
