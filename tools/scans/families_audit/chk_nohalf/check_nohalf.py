"""Half family removed (Eddie, 29 Oct 2026): checks one build by the new code against the build before (2cc2af2b), same race.
usage: check_nohalf.py <before.xlsx> <after.xlsx>
Rows aligned per sheet (difflib on the row signature: value, fill, comment, border of every cell). Every difference must be explained:
- a changed cell in a row whose before row names the half family near it ('(half)', '· half ·', ' half (', 'half —', 'half ×') - the cell
  itself, or a cell within 9 columns on the same row (a T-table value group: value, +5, target, group, offset, score, arrow, also, timing),
  or a T24 cell whose before comment has a 'repeat:' line on a half target (its partner went);
- a title row (counts);
- a timeline row (TIMELINE, LONG TIMELINE, STAR TIMELINE, LONG STAR TIMELINE): events dropped (before row names half) or gained / moved
  (follow-on, listed);
- a pair row (SKY PAIRS / SKY STARS / SKY ROYAL) dropped because its before row named half (listed only for its three family legs).
Also: no half family text anywhere in the after workbook. Prints counts by kind, every unexplained difference, and 'mismatches: n' last."""
import sys, re, difflib
import openpyxl

HALF = re.compile(r'\(half\)|· half ·|· half$| half \(| half —|half ×| half,|\bhalf\b(?! (?:squared|of))')
NOTHALF = re.compile(r'ratio half|distance half|midpoint half|each half|halves|two halves')
TL = ('TIMELINE', 'LONG TIMELINE', 'STAR TIMELINE', 'LONG STAR TIMELINE')
PAIRS = ('SKY PAIRS', 'SKY STARS', 'SKY ROYAL')


def is_half(t):
    if not isinstance(t, str):
        return False
    return bool(HALF.search(NOTHALF.sub('', t)))


def sig(c):
    b = c.border
    return (c.value, c.fill.start_color.rgb if c.fill.fill_type else None, c.comment.text if c.comment else None,
            (b.left.style, b.right.style, b.top.style, b.bottom.style) if b else None)


def rows(ws):
    out = [tuple(sig(c) for c in r) for r in ws.iter_rows()]
    while out and all(v == (None, None, None, (None,) * 4) for v in out[-1]):
        out.pop()
    return out


def half_at(row, k):
    v, f, cm, b = row[k] if k < len(row) else (None, None, None, None)
    return is_half(v) or is_half(cm)


def kind(row):
    a = row[0][0] if row else None
    s = str(a or '')
    if any(s == t or s.startswith(t + ' ') or s.startswith(t + ' (') for t in TL):
        return 'timeline'
    if any(s == t or s.startswith(t) for t in PAIRS):
        return 'pairs'
    return 'table'


def title(row):
    return any(isinstance(v, str) and len(v) > 120 for v, f, cm, b in row[:3]) or (row and isinstance(row[0][0], str) and len(row[0][0]) > 40)


bad, cnt = [], {}
B, A = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
if B.sheetnames != A.sheetnames:
    bad.append(f'sheets {B.sheetnames} {A.sheetnames}')
for sh in A.sheetnames:
    for r in A[sh].iter_rows():
        for c in r:
            for t in (c.value, c.comment.text if c.comment else None):
                if is_half(t):
                    bad.append(f'half text in the after workbook: {sh}!{c.coordinate} {str(t)[:80]!r}')
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
                n = max(len(x), len(y))
                for c in range(n):
                    u = x[c] if c < len(x) else None
                    w = y[c] if c < len(y) else None
                    if u == w:
                        continue
                    if half_at(x, c):
                        why = 'cell named half'
                    elif any(half_at(x, d) for d in range(max(0, c - 9), min(len(x), c + 10))):
                        why = 'value group of a half cell'
                    elif u and u[2] and 'repeat:' in u[2] and any(is_half(l) for l in u[2].split('\n') if l.startswith('repeat:')):
                        why = 'T24 repeat partner of a half target'
                    elif title(x):
                        why = 'title count'
                    elif kind(x) == 'timeline' or kind(y) == 'timeline':
                        why = 'timeline follow-on'
                    else:
                        why = None
                    if why is None:
                        bad.append(f'UNEXPLAINED {sh} row {i1 + k + 1}->{j1 + k + 1} col {c + 1}: {u and u[0]!r} -> {w and w[0]!r}')
                    else:
                        cnt[(sh if sh in ('POSITIONS', 'SKY JUPITER') else 'runner', why)] = cnt.get((sh if sh in ('POSITIONS', 'SKY JUPITER') else 'runner', why), 0) + 1
            continue
        for k in range(i1, i2):                            # dropped rows
            x = rb[k]
            if any(half_at(x, c) for c in range(len(x))):
                why = f'{kind(x)} row dropped (named half)'
            elif kind(x) == 'timeline':
                why = 'timeline row moved / dropped (follow-on)'
            elif title(x):
                why = 'title count'
            else:
                bad.append(f'UNEXPLAINED dropped {sh} row {k + 1}: {[v for v, *_ in x if v is not None][:6]}')
                continue
            cnt[(sh, why)] = cnt.get((sh, why), 0) + 1
        for k in range(j1, j2):                            # added rows
            y = ra[k]
            if kind(y) == 'timeline':
                why = 'timeline row gained / moved (follow-on)'
                print(f'  gained/moved {sh} row {k + 1}: {[v for v, *_ in y if v is not None][:8]}')
            elif title(y):
                why = 'title count'
            else:
                bad.append(f'UNEXPLAINED added {sh} row {k + 1}: {[v for v, *_ in y if v is not None][:6]}')
                continue
            cnt[(sh, why)] = cnt.get((sh, why), 0) + 1
for k in sorted(cnt):
    print(f'{k[0]} | {k[1]}: {cnt[k]}')
for x in bad[:40]:
    print('  ', x)
print('mismatches:', len(bad))
