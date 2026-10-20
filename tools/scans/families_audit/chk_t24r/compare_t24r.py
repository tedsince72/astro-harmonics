"""compare_t24r.py (19 Oct 2026): tables workbook with the T24 ratio tables against the build before.
On each runner sheet the new block (from the 'T24 H / J' title through T24 JOCKEY RATIOS) is cut out; everything else must be identical
to the before workbook: every cell's value, fill and comment, row by row (empty rows ignored). Also prints per table: hits per area
(from the titles), together, automatic, assisted cells.
usage: compare_t24r.py before.xlsx after.xlsx"""
import sys, re, openpyxl
SKY35 = ('SKY STARS', 'TIMELINE', 'LONG TIMELINE')     # 20 Oct 2026: on the 35 stars since; checked by chk_sky35/compare_sky35.py
sky35 = lambda v: str(v or '').startswith(SKY35)
NEW = ('T24 H / J', 'T24 HORSE RATIOS', 'T24 JOCKEY RATIOS')


def sig(r):
    return tuple((c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None) for c in r)


def rows(ws, cut):
    out, it, i, stats = [], list(ws.iter_rows()), 0, {}
    while i < len(it):
        r = it[i]
        if cut and r[0].value in NEW:
            j = i
            while j < len(it) and (it[j][0].value in NEW + ('table', None)):
                if it[j][0].value in NEW and str(it[j][1].value or '').startswith(it[j][0].value + ' ('):
                    m = re.search(r'Hits: A (\d+), φ and √2 (\d+), B (\d+)', it[j][1].value)
                    cur = it[j][0].value; stats[cur] = {'hits': m.groups(), 'together': 0, 'automatic': 0, 'assisted': 0, 'rows': 0}
                elif it[j][0].value in NEW:
                    st = stats[it[j][0].value]; st['rows'] += 1
                    for c in it[j][2:]:
                        st['together'] += c.value == 'together'
                        t = c.comment.text if c.comment else ''
                        st['automatic'] += 'automatic (' in t
                        st['assisted'] += ' assisted (q' in t
                j += 1
            i = j
            continue
        if any(c.value is not None for c in r) and not sky35(r[0].value):
            out.append(sig(r))
        i += 1
    return out, stats


b, a = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
bad = []
assert b.sheetnames == a.sheetnames
for sh in b.sheetnames:
    rb, _ = rows(b[sh], False)
    ra, st = rows(a[sh], True)
    if rb != ra:
        n = next((k for k in range(min(len(rb), len(ra))) if rb[k] != ra[k]), min(len(rb), len(ra)))
        bad.append((sh, len(rb), len(ra), str(rb[n] if n < len(rb) else None)[:150], str(ra[n] if n < len(ra) else None)[:150]))
    for t, d in st.items():
        print(sh, t, d)
print('sheets', len(b.sheetnames), '- differences outside the new tables:', len(bad))
for x in bad[:5]:
    print('  ', x)
