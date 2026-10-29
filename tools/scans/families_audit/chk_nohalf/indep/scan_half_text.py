"""Check 1: any half-family text left in a workbook (cell values and comments); midpoint wording excluded."""
import re, sys, openpyxl
OK = re.compile(r'ratio half|distance half|each half|halves|two halves|both halves|the half|half of T1[78]|other half', re.I)
for f in sys.argv[1:]:
    wb = openpyxl.load_workbook(f)
    n = 0; hits = []
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                for src, t in (('value', c.value), ('comment', c.comment.text if c.comment else None)):
                    if isinstance(t, str) and re.search(r'half', t, re.I):
                        rest = OK.sub('', t)
                        if re.search(r'half', rest, re.I):
                            hits.append((ws.title, c.coordinate, src, t[:160]))
                        else:
                            n += 1
    print(f, 'midpoint-wording cells (excluded):', n, 'half-family texts:', len(hits))
    for h in hits[:15]:
        print('   ', h)
