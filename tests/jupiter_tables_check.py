#!/usr/bin/env python3
"""jupiter_tables_check.py - tests for tools/jupiter_tables.py (13 Oct 2026). Builds the three test workbooks and checks cells."""
import os, subprocess, sys
import openpyxl

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
GREEN, YELLOW = '00C6EFCE', '00FFEB9C'
COL = {'RA': 2, 'Dec': 9, 'Flat': 16, 'GC': 23}            # 0-based column of each plane's value (tables with 4 planes)
RES = []


def check(name, ok, detail):
    RES.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")


def build(inp):
    r = subprocess.run([sys.executable, 'tools/jupiter_tables.py', inp], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr)
    return r.stdout.split(' -> ')[1].split(' (')[0]


def row(ws, tid, label):
    for r in ws.iter_rows():
        if r[0].value == tid and r[1].value == label:
            return r


def sheet_of(wb, horse):
    return next(wb[s] for s in wb.sheetnames if s.startswith('P') and horse in str(wb[s]['A1'].value))


def cell(r, pl, col0=None):
    c0 = COL[pl] if col0 is None else col0
    c = r[c0]
    return c.value, r[c0 + 2].value, r[c0 + 3].value, (c.fill.start_color.rgb if c.fill.fill_type else None)


print('Test 1: Nottingham 15:30 2022 (batch xlsx) — Dynamic Force, T6 S Jupiter → J Vesta')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220601_nottingham_1530.xlsx'))
r = row(sheet_of(wb, 'Dynamic Force'), 'T6', 'S Jupiter → J Vesta')
v, t, o, f = cell(r, 'RA'); check('RA 18 (+0.00414), green', t == '18 (whole)' and o == '+0.00414' and f == GREEN, f'{v} {t} {o} {f}')
v, t, o, f = cell(r, 'Dec'); check('Dec 137/9 (+0.00046), green', t == '137/9 (ninth)' and o == '+0.00046' and f == GREEN, f'{v} {t} {o} {f}')

print('\nTest 2: Pholas, Lingfield 2 Apr 2021 (split folder, older workbook) — T14 J/S Jupiter Equator')
wb = openpyxl.load_workbook(build('reference/classic/lingfield_aw_1435_20210402'))
ws = sheet_of(wb, 'Pholas')
r = row(ws, 'T14', '|Dec| S Jupiter / |Dec| J Jupiter (inverted)')
v, t, o, f = cell(r, 'RA')
check('1.61887 -> phi, +0.0515 %, yellow', round(v, 5) == 1.61887 and t == '1.618 (golden)' and o == '+0.05151%' and f == YELLOW, f'{v} {t} {o} {f}')
r = row(ws, 'T7', 'S Rahu → H Jupiter')
check('arrow n/a where the engine does not reproduce (S Rahu)', r[COL['RA'] + 1].value == 'n/a' and r[COL['RA'] + 5].value == 'n/a',
      f"+5 {r[COL['RA'] + 1].value}, arrow {r[COL['RA'] + 5].value}")

print('\nTest 3: Newcastle AW 13:30 2022 (batch xlsx) — Venturous, T7')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220102_newcastle_aw_1330.xlsx'))
ws = sheet_of(wb, 'Venturous')
v, t, o, f = cell(row(ws, 'T7', 'S Venus → H Jupiter'), 'Dec')
check('S Venus → H Jupiter Dec 40.00191, green', round(v, 5) == 40.00191 and t == '40 (whole)' and f == GREEN, f'{v} {t} {o} {f}')
v, t, o, f = cell(row(ws, 'T7', 'S Uranus → H Jupiter'), 'Dec')
check('S Uranus → H Jupiter Dec 7.00821, yellow', round(v, 5) == 7.00821 and t == '7 (whole)' and f == YELLOW, f'{v} {t} {o} {f}')

print(f'\n{sum(RES)}/{len(RES)} passed')
sys.exit(0 if all(RES) else 1)
