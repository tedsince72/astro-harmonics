#!/usr/bin/env python3
"""jupiter_tables_check.py - tests for tools/jupiter_tables.py (13 Oct 2026). Builds the three test workbooks and checks cells.
13 Oct 2026, Eddie's correction (tools/families.py): scores replace tolerance bands (green >= 80, yellow 50-80, light < 50);
ninths = the 48 _NINTH_RANGES only. Test 1's ninth check (Dec 15.222681 -> 137/9, not one of the 48) replaced by T5 S Jupiter -> H Mercury
RA 14.4444; expected values changed: T6 RA 18 green -> yellow (whole score 62.9), Pholas phi yellow -> green (golden 1xphi),
Venturous S Uranus Dec 7.008205 yellow -> light (whole score 34.78)."""
import os, subprocess, sys
import openpyxl

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
GREEN, YELLOW, LIGHT = '00C6EFCE', '00FFEB9C', '00FFF8DC'
COL = {'RA': 2, 'Dec': 10, 'Flat': 18, 'GC': 26}           # 0-based column of each plane's value (tables with 4 planes, 8 columns each)
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
    return c.value, r[c0 + 2].value, r[c0 + 3].value, (c.fill.start_color.rgb if c.fill.fill_type else None), r[c0 + 4].value


print('Test 1: Nottingham 15:30 2022 (batch xlsx) — Dynamic Force')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220601_nottingham_1530.xlsx'))
ws = sheet_of(wb, 'Dynamic Force')
v, t, o, f, sc = cell(row(ws, 'T5', 'S Jupiter → H Mercury'), 'RA')
check('T5 S Jupiter → H Mercury RA 14.439854 -> ninth 14.4444 (-0.00459, score 95.14), green',
      round(v, 6) == 14.439854 and t == '14.4444 (ninth)' and o == '-0.00459' and sc == 95.14 and f == GREEN, f'{v} {t} {o} {sc} {f}')
r = row(ws, 'T6', 'S Jupiter → J Vesta')
v, t, o, f, sc = cell(r, 'RA')
check('T6 S Jupiter → J Vesta RA 18 (+0.00414, whole score 62.9), yellow', t == '18 (whole)' and o == '+0.00414' and sc == 62.9 and f == YELLOW,
      f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(r, 'Dec')
check('T6 S Jupiter → J Vesta Dec 15.222681: no family (137/9 is not one of the 48), no colour', round(v, 6) == 15.222681 and t is None and f is None,
      f'{v} {t} {o} {sc} {f}')

print('\nTest 2: Pholas, Lingfield 2 Apr 2021 (split folder, older workbook) — T14 J/S Jupiter Equator')
wb = openpyxl.load_workbook(build('reference/classic/lingfield_aw_1435_20210402'))
ws = sheet_of(wb, 'Pholas')
r = row(ws, 'T14', '|Dec| S Jupiter / |Dec| J Jupiter (inverted)')
v, t, o, f, sc = cell(r, 'RA')
check('1.61887 -> 1×φ (golden, +0.00083, score 94.92), green; also φ^1 (phi power)',
      round(v, 5) == 1.61887 and t == '1×φ (golden)' and o == '+0.00083' and sc == 94.92 and f == GREEN and 'φ^1 (phi power)' in str(r[COL['RA'] + 6].value),
      f'{v} {t} {o} {sc} {f} also {r[COL["RA"] + 6].value}')
r = row(ws, 'T7', 'S Rahu → H Jupiter')
check('arrow n/a where the engine does not reproduce (S Rahu)', r[COL['RA'] + 1].value == 'n/a' and r[COL['RA'] + 5].value == 'n/a',
      f"+5 {r[COL['RA'] + 1].value}, arrow {r[COL['RA'] + 5].value}")

print('\nTest 3: Newcastle AW 13:30 2022 (batch xlsx) — Venturous, T7')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220102_newcastle_aw_1330.xlsx'))
ws = sheet_of(wb, 'Venturous')
v, t, o, f, sc = cell(row(ws, 'T7', 'S Venus → H Jupiter'), 'Dec')
check('S Venus → H Jupiter Dec 40.00191 (whole score 81.81), green', round(v, 5) == 40.00191 and t == '40 (whole)' and sc == 81.81 and f == GREEN,
      f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(ws, 'T7', 'S Uranus → H Jupiter'), 'Dec')
check('S Uranus → H Jupiter Dec 7.008205 (whole score 34.78), light yellow', round(v, 4) == 7.0082 and t == '7 (whole)' and sc == 34.78 and f == LIGHT,
      f'{v} {t} {o} {sc} {f}')

print(f'\n{sum(RES)}/{len(RES)} passed')
sys.exit(0 if all(RES) else 1)
