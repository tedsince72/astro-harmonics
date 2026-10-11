#!/usr/bin/env python3
"""split_batch.py BATCH.xlsx OUTDIR NAME - Eddie's full-field race_batch workbook (TRANS, P01..Pnn) -> one workbook per horse/jockey pair
(TRANS, P01 = horse, P02 = jockey), same format, so the workbook tools run per runner. Used when the repo POS files are empty."""
import sys, os, openpyxl
src, out, name = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(out, exist_ok=True)
wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
tabs = [t for t in wb.sheetnames if t.startswith('P') and t[1:].isdigit()]
rows = {t: list(wb[t].iter_rows(values_only=True)) for t in ['TRANS'] + tabs}
for i in range(0, len(tabs) - 1, 2):
    h, j = tabs[i], tabs[i + 1]; nb = openpyxl.Workbook(); nb.remove(nb.active)
    for new, old in (('TRANS', 'TRANS'), ('P01', h), ('P02', j)):
        ws = nb.create_sheet(new)
        for r in rows[old]: ws.append([c for c in r[:9]])
    f = f"{out}/{name}__{h}.xlsx"; nb.save(f); print(f, rows[h][1][0], '/', rows[j][1][0])
