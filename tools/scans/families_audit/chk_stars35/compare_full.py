"""compare_full.py (19 Oct 2026): a --full tables workbook against the build before the 35-star change.
Every sheet must be identical (values, row by row, empty rows ignored) except T1, T2 and T24 star rows: there the before rows minus
Polaris must equal the after rows minus the 13 new stars. Also lists the sheets of a default workbook.
usage: compare_full.py before.xlsx full.xlsx [default.xlsx] [pairs_before.xlsx pairs_after.xlsx]"""
import sys, openpyxl
sys.path.insert(0, 'tools')
from jupiter_tables import NEW_STARS
NEW = set(NEW_STARS)


def rows(ws):
    return [tuple(r) for r in ws.iter_rows(values_only=True) if any(v is not None for v in r)]


def star_of(r):
    if r[0] in ('T1', 'T2') and r[1]:
        return str(r[1]).split(' → ')[-1].split(' ', 1)[-1]
    if r[0] == 'T24' and r[1] and not str(r[1]).startswith('T24 '):
        return str(r[1]).split(' ', 1)[-1]
    return None


b, f = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
bad, drop_b, drop_f = [], {}, {}
if b.sheetnames != f.sheetnames:
    bad.append(('sheet list', b.sheetnames, f.sheetnames))
for sh in b.sheetnames:
    if sh not in f.sheetnames:
        continue
    rb, rf = rows(b[sh]), rows(f[sh])
    if sh == 'POSITIONS':                                  # new star positions appended at the end
        cut = next((i for i, r in enumerate(rf) if str(r[0]).startswith('T1 / T2 / T24 only')), len(rf))
        extra = rf[cut:]; rf = rf[:cut]
        drop_f['POSITIONS'] = len(extra)
    else:
        kb = [r for r in rb if star_of(r) == 'Polaris']; kf = [r for r in rf if star_of(r) in NEW]
        drop_b[sh] = len(kb); drop_f[sh] = len(kf)
        rb = [r for r in rb if star_of(r) != 'Polaris']; rf = [r for r in rf if star_of(r) not in NEW]
    if rb != rf:
        n = next(i for i in range(max(len(rb), len(rf))) if i >= len(rb) or i >= len(rf) or rb[i] != rf[i])
        bad.append((sh, len(rb), len(rf), rb[n] if n < len(rb) else None, rf[n] if n < len(rf) else None))
print('Polaris rows dropped per sheet:', {k: v for k, v in drop_b.items() if v})
print('new-star rows per sheet:', {k: v for k, v in drop_f.items() if v})
print('differences beyond those:', len(bad))
for x in bad[:5]:
    print('  ', str(x)[:600])
if len(sys.argv) > 3:
    d = openpyxl.load_workbook(sys.argv[3], read_only=True)
    print('default sheets:', d.sheetnames)
if len(sys.argv) > 5:
    pb, pa = openpyxl.load_workbook(sys.argv[4], read_only=True), openpyxl.load_workbook(sys.argv[5], read_only=True)
    print('pairs workbook identical:', pb.sheetnames == pa.sheetnames and all(rows(pb[s]) == rows(pa[s]) for s in pb.sheetnames))
