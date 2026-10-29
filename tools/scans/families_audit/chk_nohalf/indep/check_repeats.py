"""T24 repeats (after): from each body cell's best target (comment first line, itself verified by check_cells.py), the
repeated targets per star row (same family + target, >= 2 cells, conjunction and the S Jupiter column left out) = the
repeats column; dotted outline exactly on repeated cells (thick midpoint kept); title 'k of N rows ..., m repeated targets'.
usage: check_repeats.py <wb>"""
import re, sys, collections
import openpyxl
sys.path.insert(0, __import__('os').path.dirname(__file__))
from check_cells import RE_CHIT

wb = openpyxl.load_workbook(sys.argv[1])
bad = []; nrows = 0; nrep = 0
for ws in wb:
    if ws.title == 'POSITIONS':
        continue
    rows = list(ws.iter_rows())
    i = 0
    while i < len(rows):
        r = rows[i]
        if r[0].value == 'T24' and isinstance(r[1].value, str) and r[1].value.startswith('T24 ') and 'REPEATS' in r[1].value:
            title = r[1].value
            hdr = {c.column: c.value for c in rows[i + 1]}
            names = {c.column: c.value for c in rows[i + 2]}
            plane = {}
            cur = None
            for c in sorted(hdr):
                if hdr[c] in ('RA', 'Dec'):
                    cur = hdr[c]
                elif hdr[c] is not None:
                    cur = None
                plane[c] = cur
            repcol = [c for c, h in hdr.items() if h == 'repeats'][0]
            body = {c: (names[c], plane[c]) for c in names if names[c] and plane.get(c) and names[c] != 'S Jupiter'
                    and not str(names[c]).startswith('star =')}
            j = i + 3; k = 0; m = 0; N = 0
            while j < len(rows) and rows[j][0].value == 'T24':
                row = rows[j]
                lab = row[1].value
                if lab == 'stars' or '→' in str(lab):
                    if row[repcol - 1].value:
                        bad.append(f'{ws.title} r{row[0].row} repeats on a non-star row')
                    j += 1
                    continue
                N += 1
                groups = collections.defaultdict(list)
                for c, (b, p) in body.items():
                    cell = row[c - 1]
                    line = cell.comment.text.split('\n')[0] if cell.comment else ''
                    mm = RE_CHIT.match(line)
                    if mm:
                        groups[(mm.group(1), mm.group(2))].append((b, p, float(mm.group(4)), cell))
                rep = {g: v for g, v in groups.items() if len(v) >= 2}
                exp = {(g[0], g[1], len(v), frozenset((b, p) for b, p, s, _ in v)) for g, v in rep.items()}
                got = set()
                for part in [x.strip() for x in str(row[repcol - 1].value or '').split(';') if x.strip()]:
                    mm = re.match(r'^(.*) (whole|half|golden|phi power|ninth|sqrt2|silver) ×(\d+) \((.*)\)$', part)
                    if not mm:
                        bad.append(f'{ws.title} r{row[0].row} unparsed {part!r}'); continue
                    items = frozenset(re.findall(r'([A-Z][\w ]*?) (RA|Dec) \([\d.]+\)', mm.group(4)))
                    got.add((mm.group(1), mm.group(2), int(mm.group(3)), items))
                if exp != got:
                    bad.append(f'{ws.title} r{row[0].row} {lab}: repeats {got} vs {exp}')
                repcells = {id(x[3]) for v in rep.values() for x in v}
                for c in body:
                    cell = row[c - 1]
                    st = cell.border.left.style if cell.border is not None and cell.border.left is not None else None
                    if id(cell) in repcells and st not in ('dotted', 'thick'):
                        bad.append(f'{ws.title} {cell.coordinate} repeated, border {st}')
                    if id(cell) not in repcells and st == 'dotted':
                        bad.append(f'{ws.title} {cell.coordinate} dotted but not repeated')
                    rl = [x for x in (cell.comment.text.split('\n') if cell.comment else []) if x.startswith('repeat:')]
                    if bool(rl) != (id(cell) in repcells):
                        bad.append(f'{ws.title} {cell.coordinate} repeat comment line {rl}')
                if rep:
                    k += 1; m += len(rep)
                j += 1
            nrows += N; nrep += m
            t = re.search(r'REPEATS \(22 Oct 2026\): (\d+) of (\d+) rows with a repeat, (\d+) repeated targets', title)
            if not t or (int(t.group(1)), int(t.group(2)), int(t.group(3))) != (k, N, m):
                bad.append(f'{ws.title} r{r[0].row} title counts {t.groups() if t else None} vs {(k, N, m)}')
            i = j
        else:
            i += 1
print(sys.argv[1].split('/')[-1], 'star rows', nrows, 'repeated targets', nrep, 'errors', len(bad))
for b in bad[:20]:
    print('   ', b)
