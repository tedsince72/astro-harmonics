"""compare_67.py (21 Oct 2026; copy of chk_stars46/compare_46.py): tables workbook on 67 stars against the build before (46). Every sheet: the rows
that name one of the 21 new stars (20 + the Orion Nebula Cluster) are taken out of the after build; what is left must equal the before build row for row (values, fills, comments), except title
rows whose counts change (printed). Also counts the removed rows per sheet and table id.
usage: compare_67.py before.xlsx after.xlsx"""
import sys, re, difflib, collections, openpyxl
NEW21 = ['Ankaa', 'Al Rescha', 'Mirfak', 'El Nath', 'Meissa', 'Alnilam', 'Murzim', 'Alhena', 'Acubens', 'Alphard', 'Alkes', 'Zosma',
         'Vindemiatrix', 'Diadem', 'Ras Algethi', 'Aculeus', 'Acumen', 'Facies', 'Rukbat', 'Sualocin', 'Orion Nebula Cluster']
RX = re.compile(r'\b(' + '|'.join(NEW21) + r')\b')


def sig(r):
    return tuple((c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None) for c in r)


def rows(ws):
    return [r for r in ws.iter_rows() if any(c.value is not None for c in r)]


b, a = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
assert b.sheetnames == a.sheetnames, (b.sheetnames, a.sheetnames)
other = 0
for sh in b.sheetnames:
    rb, ra = rows(b[sh]), rows(a[sh])
    keep = [r for r in ra if not any(RX.search(str(c.value)) for c in r[1:8] if isinstance(c.value, str))]
    removed = collections.Counter(str(r[0].value)[:20] for r in ra if r not in keep)
    sb, sa = [sig(r) for r in rb], [sig(r) for r in keep]
    diffs = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sb, sa, autojunk=False).get_opcodes():
        if op != 'equal':
            diffs.append((op, [str(x[0][0])[:150] for x in sb[i1:i2]], [str(x[0][0])[:150] for x in sa[j1:j2]], sb[i1:i2], sa[j1:j2]))
    # titles: same table id (first 6 characters of cell A); a differing cell differs only in its text (both values strings; fill and
    # comment identical) - tightened 20 Oct 2026: before, any row whose cell A matched passed as a title (fills unchecked)
    txt = lambda p, q: p == q or (isinstance(p[0], str) and isinstance(q[0], str) and p[1:] == q[1:])
    title_only = all(op == 'replace' and len(x) == len(y) and all(str(p)[:6] == str(q)[:6] for p, q in zip(x, y))
                     and all(len(P) == len(Q) and all(txt(p, q) for p, q in zip(P, Q)) for P, Q in zip(X, Y)) for op, x, y, X, Y in diffs)
    if not title_only:
        other += 1
    print(f'{sh}: rows before {len(rb)}, after {len(ra)}, new-star rows {sum(removed.values())} {dict(removed)}; '
          f'other differences {sum(len(x) for _, x, _, _, _ in diffs)} ({"titles only" if title_only else "NOT titles only"})')
    for op, x, y, _, _ in diffs:
        for p, q in zip(x, y) if op == 'replace' else [(x, y)]:
            print('     before:', p); print('     after: ', q)
print('sheets with differences other than title rows:', other)
