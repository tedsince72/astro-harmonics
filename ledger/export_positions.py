#!/usr/bin/env python3
"""export_positions.py v1.0 - writes META, TRANS_POS, Pxx_POS and NATAL_HOURLY of each baseline
race workbook (wb/, wb1/) to CSV in the same layout as test_positions.zip, so all 96 races
read the same way. Workbooks are not changed.
Usage: python3 export_positions.py --out DIR WORKBOOK..."""
import argparse, csv, os, re, openpyxl
ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); ap.add_argument('books', nargs='+')
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
for f in a.books:
    race = re.sub(r'^race_batch_|_active\.xlsx$', '', os.path.basename(f))
    wb = openpyxl.load_workbook(f, read_only=True)
    for ws in wb.worksheets:
        if ws.title in ('META', 'TRANS_POS', 'NATAL_HOURLY') or re.match(r'P\d\d_POS$', ws.title):
            with open(f'{a.out}/{race}__{ws.title}.csv', 'w', newline='') as o:
                w = csv.writer(o)
                for r in ws.iter_rows(values_only=True):
                    w.writerow(['' if v is None else v for v in r])
    print(race)
