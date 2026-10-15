#!/usr/bin/env python3
"""jupiter_tables_check.py - tests for tools/jupiter_tables.py (13 Oct 2026). Builds the three test workbooks and checks cells.
13 Oct 2026, Eddie's correction (tools/families.py): scores replace tolerance bands (green >= 80, yellow 50-80, light < 50);
ninths = the 48 _NINTH_RANGES only. Test 1's ninth check (Dec 15.222681 -> 137/9, not one of the 48) replaced by T5 S Jupiter -> H Mercury
RA 14.4444; expected values changed: T6 RA 18 green -> yellow (whole score 62.9), Pholas phi yellow -> green (golden 1xphi),
Venturous S Uranus Dec 7.008205 yellow -> light (whole score 34.78).
Same day, Eddie's interval list for ratios (0.15 %, squared): Pholas phi now an interval, phi · golden ratio · Phi, +0.05151 %, score 43.11,
light (green under the first families.py build, yellow under JR v3 bands); RATIOS BY GROUP sheet checked.
Test 6 (Eddie 13 Oct): Jupiter return line (information); per-plane automatic unisons (d(S Jup, natal Jup) / d(natal Jup, X) < 0.0015) greyed, not counted;\nreturn-assisted tag for 0.0015 <= d1/d2 < 0.02; empty RATIOS group headers hidden.\nTest 5 (Eddie 13 Oct): unison counts, with its field count.\nTest 4 (T16 RA–Dec crossing, Eddie 13 Oct): Sandown 14:25 2021 Nube Negra / Harry Skelton, Jupiter–Orcus J RA = H Dec.
Test 7 (Eddie 13 Oct): tapered ratio tolerances (unison 1 %, 1 % / k, floor 0.15 %; Phi group φ, φ², φ³, 1+√2 only) and the nearest
target + offset shown outside every tolerance (plain text, no score, no colour). Expected values changed by it: test 1 Dec 15.222681
now shows '15.5556 (ninth) — outside ±0.106' -0.33287 (still no score, no colour); test 5 P05 now has 5 unison rows (the Rahu ratio is a
unison in RA, Flat and GC); test 6 Cobden J Pluto GC 1.001353 score 0.96 light -> 74.77 yellow, Cobden 41 -> 61 unisons (20 automatic,
all RA; 41 genuine: Flat 20, GC 20, RA 1, all return-assisted, two at 2/6).
Revised same day (Eddie): k = the LARGER number of the ratio (3/2 -> 0.333 %, 4/3 -> 0.25 %, 5/x -> 0.2 %, 6/5 and up -> 0.15 %) and the
nearest target outside the tolerance by tightness (offset / own tolerance) for ratios too. Test 7 changed: Flat 1.0445 nearest 16/15
-2.07813 % -> unison +4.44999 % (outside ±1 %); Haumea 1.506122 3/2 score 3.37 -> outside ±0.333 %; the 3/2 hit is now Makemake 1.499624
on 0.333 % (85.52). Tests 1-6 unchanged.
Test 8 (Eddie 13 Oct): THREADS sheet, Nottingham 15:30 2022 Uranus row; expected values set from the rule (hits >= 50 for tags, counts
and cell lines; mutual same chart / across charts), not tuned to the winner. Same day: scaled repeats of a main hit (same family, same
digits) dropped and score-0 hits left out of '+ n weaker': Dynamic Force Uranus '+ 11 weaker' -> '+ 9 weaker', 5 scaled lines -> 1.
Test 9 (Eddie 13 Oct): NUMBERS sheet per runner + FIELD NUMBERS, Wincanton 14:20 2022 P07 7.777 (ninth) row.
Same day (Eddie): a repeat (same family, same digits) keeps the higher form at the shown precision (tie = main), in THREADS and NUMBERS;
H Jupiter – J Jupiter in its own H–J column, once. Changed: test 8 '+ 9 weaker' -> '+ 8 weaker' (J Jup→H Uranus 14.14 shown as /10 1.414,
99.1); test 9 J Haumea 77.798638 (83.67) -> its /10 form 7.779864 (83.68); P07 silver 0.414 sky + horse + jockey -> two of three.
14 Oct (Eddie): keep-higher compares unrounded scores, display 2 dp in THREADS and NUMBERS. Changed: Dynamic Force S Jup→H Uranus 11.10793
now shown as /10 1.110793 (94.7963 > 94.7947), '+ 8 weaker' -> '+ 9 weaker'; Wincanton P07 H Rigel 7.777589 now shown as x10 77.775893
(98.5224 > 98.5209); scores in THREADS lines at 2 dp.
14 Oct, revised (Eddie): the main form is kept unless the scaled form scores > 0.5 higher (unrounded); all scores at 2 dp everywhere
(scaled, also, FIELD matrices). Changed back: Dynamic Force 11.10793 main (94.80), Wincanton P07 H Rigel 7.777589 main (98.52) and
J Haumea 77.798638 main (83.67); FIELD 16 tag '[92.3]' -> '[92.30]'.
Test 10 (Eddie 14 Oct): midpoints - Equator plane (|Dec|, only when the three are not on one side), RA far (span 360 - near), tolerance
green = max(0.05, 0.5 % of span), yellow 3x, light 9x. No earlier test checked a midpoint value; THREADS test 8 now also lists midpoint
lines (they carry span and tolerance); its tags and counts are unchanged.
Revised 14 Oct (Eddie): green = 0.1 % of span, floor 0.05, cap 0.15 (yellow 3x, light 9x); FIELD 11 added. Test 10 changed: tolerance
cases; Dynamic Force T10 Equator tol ±0.1108 -> ±0.0500 (still green).
14 Oct (Eddie): Jupiter-only midpoint lines in T11 only; NUMBERS HORSE = T1, JOCKEY = T2 (no T3 / T4, no H–J column). Changed: test 9's
H–J check replaced; Wincanton FIELD NUMBERS 6 -> 5 numbers (sqrt2 0.707 / 70.7 drops out; 166.667 3/6 -> 1/6; silver 2.414 2/6 -> 1/6).
Test 11 (Eddie 14 Oct): EQUIDISTANCE on SKY JUPITER (Beverley 14:05 2024, sky-only workbook copied from ~/astronomy-project/sky_0608_wb),
T17 + FIELD 17 (Wincanton). Same day: "X, Y together" (d(X, Y) < 1.5 RA / 0.3 other planes) tagged, at the bottom, not counted in
FIELD 17; a Ketu line with the same numbers as a Rahu line dropped. Changed: test 11 best-first check now above the together lines.
Test 12 (Eddie 14 Oct): EQUIDISTANCE family hits for d(Jup, X), d(Jup, Y), d(X, Y) and timing (ratio +5, arrow, applying / separating,
exact clock time, linear) - Lingfield AW 14:35 2021 batch (copied from ~/astronomy-project/racecards/20210402_lingfield_aw; xlsx only).
Same day: each family hit split into a value cell and a family cell (coloured by its score); test 12 column positions changed.
14 Oct (Eddie): THREADS every family hit >= 50 (not only the best), cell colour = best line - test 8 '+ 9 weaker' -> '+ 11 weaker';
T19 / PAIRS H–J across = same body only; T18 never a 'together' plane as the closest plane.
Test 13 (Eddie 14 Oct): T18 - equidistance pair side by side for horse and jockey (block 1 S Jupiter, block 2 natal Jupiters);
'both' tag and count. Test 14: T19 sky Jupiter on natal pairs, P## PAIRS, SKY STARS. (No Messi workbook in the repo: that check skipped.)"""
import os, subprocess, sys
import openpyxl
from openpyxl.cell.rich_text import CellRichText

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
os.chdir(REPO)
GREEN, YELLOW, LIGHT = '00C6EFCE', '00FFEB9C', '00FFF8DC'
COL = {'RA': 2, 'Dec': 11}                                # 0-based column of each plane's value (RA, Dec; 9 columns each; Flat, GC removed 14 Oct 2026)
RES = []


def check(name, ok, detail):
    RES.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")


import time
T0, NBUILT = time.time() - 1, [0]


def build(inp):
    NBUILT[0] += 1
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
    return c.value, r[c0 + 2].value, r[c0 + 4].value, (c.fill.start_color.rgb if c.fill.fill_type else None), r[c0 + 5].value


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
check('T6 S Jupiter → J Vesta Dec 15.222681: no family (137/9 is not one of the 48), no colour, no score; nearest shown: '
      '15.5556 (ninth) — outside ±0.106, -0.33287', round(v, 6) == 15.222681 and t == '15.5556 (ninth) — outside ±0.106' and o == '-0.33287'
      and f is None and sc is None,
      f'{v} {t} {o} {sc} {f}')

print('\nTest 2: Pholas, Lingfield 2 Apr 2021 (split folder, older workbook) — T14 J/S Jupiter Equator')
wb = openpyxl.load_workbook(build('reference/classic/lingfield_aw_1435_20210402'))
ws = sheet_of(wb, 'Pholas')
r = row(ws, 'T14', '|Dec| S Jupiter / |Dec| J Jupiter (inverted)')
v, t, o, f, sc = cell(r, 'RA')
check('1.61887 -> φ · golden ratio · Phi (interval, +0.05151 %, score 43.11), light; Group column Phi',
      round(v, 5) == 1.61887 and t == 'φ · golden ratio · Phi' and o == '+0.05151%' and sc == 43.11 and f == LIGHT and r[COL['RA'] + 1 + 2].value == 'Phi',
      f'{v} {t} {o} {sc} {f} group {r[COL["RA"] + 3].value}')
rs = wb[[n for n in wb.sheetnames if n.endswith(' RATIOS')][0]]
hit = [x for x in rs.iter_rows(values_only=True) if x[1] == 'T14' and x[0] == 'Phi' and x[6] == 'φ']
check('RATIOS BY GROUP sheet lists it under Phi, marked (inverted)', len(hit) == 1 and hit[0][9] == 43.11 and hit[0][2].endswith('(inverted)'), str(hit))
r = row(ws, 'T7', 'S Rahu → H Jupiter')
check('arrow n/a where the engine does not reproduce (S Rahu)', r[COL['RA'] + 1].value == 'n/a' and r[COL['RA'] + 6].value == 'n/a',
      f"+5 {r[COL['RA'] + 1].value}, arrow {r[COL['RA'] + 6].value}")

print('\nTest 3: Newcastle AW 13:30 2022 (batch xlsx) — Venturous, T7')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220102_newcastle_aw_1330.xlsx'))
ws = sheet_of(wb, 'Venturous')
v, t, o, f, sc = cell(row(ws, 'T7', 'S Venus → H Jupiter'), 'Dec')
check('S Venus → H Jupiter Dec 40.00191 (whole score 81.81), green', round(v, 5) == 40.00191 and t == '40 (whole)' and sc == 81.81 and f == GREEN,
      f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(ws, 'T7', 'S Uranus → H Jupiter'), 'Dec')
check('S Uranus → H Jupiter Dec 7.008205 (whole score 34.78), light yellow', round(v, 4) == 7.0082 and t == '7 (whole)' and sc == 34.78 and f == LIGHT,
      f'{v} {t} {o} {sc} {f}')

print('\nTest 4: Sandown 14:25 2021 (batch xlsx) — Nube Negra / Harry Skelton, T16 RA–Dec crossing')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20211204_sandown_1425.xlsx'))
ws = sheet_of(wb, 'Nube Negra')
r = row(ws, 'T16', 'Jupiter–Orcus')
c0 = 2 + 8 * 5                                              # 6th ordering: J RA = H Dec (8 columns each)
vals = [r[c0 + k].value for k in range(4)]
check('Jupiter–Orcus J RA 30.55841 = H Dec 30.55995, RA − Dec −0.001541, score 92.3, green', vals == [30.55841, 30.55995, -0.001541, 92.3]
      and r[c0 + 2].fill.start_color.rgb == GREEN, str(vals))
f16 = [x for x in wb['FIELD 16'].iter_rows(values_only=True) if x[0] == 'Jupiter–Orcus' and any(v is not None for v in x[1:])]
check('FIELD 16 shows it (Nube Negra column)', len(f16) == 1 and 'crossing -0.00154 [92.30]' in f16[0], str(f16))

print('\nTest 5: Newcastle AW 12:20 2021 (batch xlsx) — unison (Perfect 1) with its field count')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20211112_newcastle_aw_1220.xlsx'))
lab = 'S Jupiter–S Rahu / H Jupiter–H Rahu'
for P, inv in (('P05', ' (inverted)'), ('P11', ' (inverted)')):    # RA: both inverted (Flat had P11 not inverted)
    r = row(wb[P], 'T12', lab)
    v, t, o, f, sc = cell(r, 'RA')                         # moved from Flat (Flat removed 14 Oct 2026): RA, found by the rule
    check(f'{P} T12 {lab} RA -> 1 · unison · Perfect{inv}, also cell "unison: field 2/6"',
          t == f'1 · unison · Perfect{inv}' and r[COL['RA'] + 7].value == 'unison: field 2/6', f'{v} {t} {o} {sc} {r[COL["RA"] + 7].value}')
rs = [x for x in wb['P05 RATIOS'].iter_rows(values_only=True) if x[6] == '1' and x[1] == 'T12' and x[3] == 'RA' and 'Rahu' in x[2]]
check('P05 RATIOS: the Rahu RA unison row 1.005972 (16.23) with field 2/6', len(rs) == 1 and rs[0][4] == 1.005972 and rs[0][9] == 16.23
      and rs[0][11] == '2/6', str(rs))
f12, pl = [], None
for x in wb['FIELD 12'].iter_rows(values_only=True):
    pl = x[0] if x[0] in ('RA', 'Dec') else pl
    if pl == 'RA' and x[0] == lab:
        f12.append(x)
check('FIELD 12 (RA) tags it "field 2/6" for P05 and P11', len(f12) == 1 and sum(isinstance(v, str) and 'field 2/6' in v for v in f12[0][1:]) == 2, str(f12))

print('\nTest 6: Wincanton 14:20 2022 (batch xlsx) — P09 Cobden Jupiter return (S–J Jupiter RA 0.03276, Dec 0.52192)')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220321_wincanton_1420.xlsx'))
ws = wb['P09']
top = [r for r in ws.iter_rows(values_only=True) if r[0] == 'T13' and str(r[1]).startswith('Jupiter return')]
check('return line kept as information', len(top) == 1 and top[0][1].startswith('Jupiter return: S–J Jupiter RA 0.03276 Dec 0.52192;'), str(top))
r = row(ws, 'T13', 'S Jupiter–J Makemake / J Jupiter–J Makemake')
v, t, o, f, sc = cell(r, 'RA')
check('RA unison J Makemake automatic (d ratio < 0.0015): grey, not counted',
      t == '1 · unison · Perfect' and f == '00D9D9D9' and r[COL['RA'] + 7].value == 'unison: automatic (Jupiter return), not counted',
      f'{v} {t} {sc} {f} {r[COL["RA"] + 7].value}')
# retired 14 Oct 2026 (GC removed): 'GC unison J Pluto genuine ... 74.77 yellow' (built on T13 J Pluto GC 1.001353)
rs = [x for x in wb['P09 RATIOS'].iter_rows(values_only=True) if x[6] == '1']
na = sum('automatic' in x[11] for x in rs)
gp = sorted(x[3] for x in rs if 'automatic' not in x[11])
# moved 14 Oct 2026 (Flat, GC removed): was 63 unisons, 43 genuine (Flat 21, GC 20, RA 2), 41 return-assisted, River Bray J Pluto GC 2/6
g = sorted((x[2], x[4], x[11]) for x in rs if 'automatic' not in x[11])
check("Cobden's 22 unisons (1 % tolerance, RA / Dec): 20 automatic (all RA); 2 genuine, RA, both return-assisted 1/6 "
      "(T13 J Gonggong 1.001741, J Ketu 1.001694)",
      len(rs) == 22 and na == 20 and all(x[3] == 'RA' for x in rs if 'automatic' in x[11]) and gp == ['RA', 'RA']
      and g == [('S Jupiter–J Gonggong / J Jupiter–J Gonggong', 1.001741, '1/6 return-assisted'),
                ('S Jupiter–J Ketu / J Jupiter–J Ketu', 1.001694, '1/6 return-assisted')], f'{len(rs)} rows, {na} automatic, genuine {g}')
# retired 14 Oct 2026 (GC removed): River Bray (P07) T13 J Pluto GC unison 2/6, not tagged (built on GC; P07 has no unison now)
heads = [x[0] for x in wb['P03 RATIOS'].iter_rows(values_only=True) if x[0] in ('Perfect', 'Imperfect', 'Dissonant', 'Septimal', 'Harmonic', 'High', 'Phi') and x[1] is None]
check('P03 RATIOS: no empty group header (no Harmonic section)', 'Harmonic' not in heads, str(heads))

print('\nTest 7: Sandown 14:25 2021 (batch xlsx) — tapered ratio tolerances, nearest target outside the tolerance')
wb = openpyxl.load_workbook('reference/classic/race_batch_20211204_sandown_1425_jupiter_tables.xlsx')   # built in test 4
ws = wb['P05']
r = row(ws, 'T12', 'S Jupiter–S Mars / H Jupiter–H Mars')
v, t, o, f, sc = cell(r, 'RA')
check('P05 T12 RA S Jupiter–S Mars / H Jupiter–H Mars 1.002631 -> unison inside 1 %, +0.26308 %, score 54.31, yellow',
      round(v, 6) == 1.002631 and t == '1 · unison · Perfect (inverted)' and o == '+0.26308%' and sc == 54.31 and f == YELLOW, f'{v} {t} {o} {sc} {f}')
# retired 14 Oct 2026 (Flat removed): Flat 1.0445 outside every band (nearest by tightness), P05 Flat Haumea 1.506122 outside 3/2,
# P05 Flat Makemake 1.499624 3/2 (85.52), P09 Flat Mars 1.125048 9/8 (94.37). The 3/2 and 9/8 cases are moved to RA (P07, found by the rule).
v, t, o, f, sc = cell(row(wb['P07'], 'T12', 'S Jupiter–S Vesta / H Jupiter–H Vesta'), 'RA')
check('3/2 hit on 0.333 % (moved from Flat): P07 T12 RA Vesta 1.499361, -0.04263 %, score (10 (1/3 − 0.04263) / (1/3))² = 76.06, yellow',
      round(v, 6) == 1.499361 and t == '3/2 · fifth · Perfect (inverted)' and o == '-0.04263%' and sc == 76.06
      and round((10 * (1 / 3 - 0.04263) / (1 / 3)) ** 2, 1) == 76.1 and f == YELLOW, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(wb['P07'], 'T13', 'S Jupiter–J Mars / J Jupiter–J Mars'), 'RA')
check('9/8 on 0.15 % (moved from Flat): P07 T13 RA J Mars 1.125881, +0.07832 %, score (10 (0.15 − 0.07832) / 0.15)² = 22.83, light',
      round(v, 6) == 1.125881 and t == '9/8 · major second · Dissonant (inverted)' and o == '+0.07832%' and sc == 22.83
      and round((10 * (0.15 - 0.07832) / 0.15) ** 2, 1) == 22.8 and f == LIGHT, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(ws, 'T5', 'S Jupiter → H Mars'), 'Dec')
check('degrees outside every family: T5 S Jupiter → H Mars Dec 8.398276 -> 5×φ (golden) — outside ±0.0324, +0.30811, plain',
      t == '5×φ (golden) — outside ±0.0324' and o == '+0.30811' and sc is None and f is None, f'{v} {t} {o} {sc} {f}')
import families
TK = ('1', '2', '3/2', '3', '4/3', '4', '5/4', '5', '5/2', '5/3', '6/5', '8/5', '8/3', '9/4', '7/4', '13/4', '11/5', '7/2', '√2', '1+1/√2', 'φ')
check('Phi group = φ, φ², φ³, 1+√2 only; tolerances by the larger number (1 %, 1 % / k, 0.15 % from k = 6)',
      [i[0] for i in families.INTERVALS if i[3] == 'Phi'] == ['φ', 'φ²', 'φ³', '1+√2']
      and [round(families.TOL[k], 3) for k in TK] == [1.0, 0.5, 0.333, 0.333, 0.25, 0.25, 0.2, 0.2, 0.2, 0.2] + [0.15] * 11
      and all(families.TOL[k] == 0.15 for k in families.TOL
              if k[0].isdigit() and '√' not in k and max(int(x) for x in k.split('/')) >= 6), str(families.TOL))

print('\nTest 8: Nottingham 15:30 2022 — THREADS, Uranus row')
wb = openpyxl.load_workbook('reference/classic/race_batch_20220601_nottingham_1530_jupiter_tables.xlsx', rich_text=True)  # built in test 1
ws = wb['THREADS']
head = [c.value for c in ws[3]]
ur = next(r for r in ws.iter_rows(min_row=4) if r[0].value == 'Uranus')
df = str(ur[head.index('P01 2 Dynamic Force / Ray Dawson')].value).split('\n')
# 14 Oct 2026 (Flat, GC removed): retired the GC line 'S Uranus→H Jup GC 142.001746 → 142 (83.30) [T7]', the Uranus tags
# ('mutual, same chart · mutual, across charts · both Jupiters · both charts · directions 4'), '+ 11 weaker' and the Uranus field counts
# (1/5, 2/5, 1/5, 2/5): all rested on the GC hit. The tags check is moved to P01 Transpluto (RA / Dec hits, found by the rule).
need = ['S Jup→H Uranus Dec 11.10793 → 11.1111 (94.80) [T5]', 'S Uranus→J Jup Dec 18.995206 → 19 (57.80) [T8]']
check('Dynamic Force Uranus cell lists the two Dec hits (T5, T8)', all(x in df for x in need), str(df[:8]))
tp = next(r for r in ws.iter_rows(min_row=4) if r[0].value == 'Transpluto')
dt = str(tp[head.index('P01 2 Dynamic Force / Ray Dawson')].value).split('\n')
check('Dynamic Force Transpluto tags (moved): mutual, same chart · mutual, across charts · both Jupiters · directions 3, from '
      'S Transpluto→H Jup Dec 33.33254 (99.05) [T7], S Jup→J Transpluto RA 141.532633 → 141.4 (71.00) [T6], S Transpluto→J Jup Dec 13.368851 (57.38) [T8]',
      dt[0] == 'mutual, same chart · mutual, across charts · both Jupiters · directions 3'
      and all(x in dt for x in ('S Transpluto→H Jup Dec 33.33254 → 33.3333 (99.05) [T7]', 'S Jup→J Transpluto RA 141.532633 → 141.4 (71.00) [T6]',
                                 'S Transpluto→J Jup Dec 13.368851 → 13.3333 (57.38) [T8]')), str(dt[:5]))
check('cells list hits >= 50 only; a repeat (same family, same digits) shown once: main kept unless the scaled form is > 0.5 higher '
      '(unrounded): 11.10793 main (/10 only +0.0016), 14.141031 as /10 1.414 (99.12 vs 96.9); last line "+ n weaker"',
      df[-1].startswith('+ ') and df[-1].endswith(' weaker (see T-tables)') and not any('/10: 1.110793' in x for x in df)
      and 'J Jup→H Uranus Dec 14.141031 /10: 1.414103 → 1.414 (99.12) [T4, scaled]' in df
      and not any(x.startswith('J Jup→H Uranus Dec 14.141031 → 14.14') for x in df)
      and all(float(x.rsplit('(', 1)[1].split(')')[0]) >= 50 for x in df[1:-1] if not x.startswith('mid ')), df[-1])

print('\nTest 9: Wincanton 14:20 2022 — NUMBERS (moved 14 Oct 2026 from P07 7.777 to P01 Reserve Tank, ninth 11.1111)')
# retired 14 Oct 2026 (GC removed): P07 River Bray "ninth: 7.77778 / 77.7778" sky + horse + jockey (its JOCKEY hit was J Haumea GC 77.798638);
# FIELD NUMBERS "5 numbers left" and the 7.777 row with P07 as holder. Moved to P01 "ninth: 11.1111 / 111.111" (RA / Dec, found by the rule).
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220321_wincanton_1420.xlsx'), rich_text=True)
nr = [r for r in wb['P01 NUMBERS'].iter_rows(min_row=4, values_only=True) if r[0] == 'ninth: 11.1111 / 111.111']
check('P01 NUMBERS row "ninth: 11.1111 / 111.111" tagged sky + horse + jockey', len(nr) == 1 and nr[0][1] == 'sky + horse + jockey', str(nr))
sky, horse, jock = (str(nr[0][k]).split('\n') for k in (2, 3, 4))
check('SKY S Jupiter → S Sirius RA 111.443941 (45.54), HORSE H Jupiter → H Regulus Dec 11.11928 (86.63), JOCKEY J Jupiter → J Venus RA 11.139997 (52.73)',
      'S Jup→S Sirius RA 111.443941 → 111.111 +0.33283 (45.54)' in sky and 'H Jup→H Regulus Dec 11.11928 → 11.1111 +0.00817 (86.63)' in horse
      and 'J Jup→J Venus RA 11.139997 → 11.1111 +0.02889 (52.73)' in jock, f'{sky} {horse} {jock}')
nh = [c.value for c in wb['P07 NUMBERS'][3]]
lines = [x for r in wb['P07 NUMBERS'].iter_rows(min_row=4, values_only=True) for c in r[2:] if c for x in str(c).split('\n')]
check('NUMBERS: HORSE = T1, JOCKEY = T2 only - no H–J column, no cross-chart line (H Jup→J X, J Jup→H X)',
      nh[:6] == ['number', 'tag', 'SKY', 'HORSE', 'JOCKEY', 'SKY→NATAL'] and not any(x.startswith(('H Jup→J ', 'J Jup→H ')) for x in lines), str(nh))
fnr = [r[0] for r in wb['FIELD NUMBERS'].iter_rows(min_row=4, values_only=True)]
check('FIELD NUMBERS (within-chart only): no sqrt2 0.707 / 70.7 row',
      not any(str(x).startswith('sqrt2') for x in fnr), str(fnr))
fn = [r for r in wb['FIELD NUMBERS'].iter_rows(min_row=4, values_only=True) if r[0] == 'ninth: 11.1111 / 111.111']
head = [c.value for c in wb['FIELD NUMBERS'][3]]
check('FIELD NUMBERS lists the number with P01 as holder', len(fn) == 1 and fn[0][[i for i, h in enumerate(head) if str(h).startswith('P01')][0]]
      is not None and fn[0][-1] == '1/6', str(fn))
ok = all(float(x.rsplit('(', 1)[1].split(')')[0]) >= 40 for P in ('P01', 'P07', 'P11') for r in wb[f'{P} NUMBERS'].iter_rows(min_row=4, values_only=True)
         for c in r[2:6] if c for x in str(c).split('\n'))
check('every NUMBERS hit scores >= 40 (P01, P07, P11)', ok, '')

print('\nTest 10: midpoints (Eddie 14 Oct 2026, revised scoring) — closeness half + distance half (each x 0.5), RA closer of near / far')
# rewritten 14 Oct 2026: the span-scaled tolerance (0.1 % of span, floor 0.05, cap 0.15, yellow 3x, light 9x) is removed
import jupiter_tables as JT
g = JT.mid_geom(10, 20, -15, 'Equator')
check('geometry: Equator Dec +10, +20, −15 -> |Dec| midpoint 15, offset 0, distances 5 / 5; all on one side -> not listed',
      g == (0.0, '', 5.0, 5.0) and JT.mid_geom(10, 20, 15, 'Equator') is None, str(g))
check('geometry: RA 350 / 30 -> c = 10 at the near midpoint (offset 0, near); c = 190 at the far one (offset 0, far); never both',
      JT.mid_geom(350, 30, 10, 'RA')[:2] == (0.0, 'near') and JT.mid_geom(350, 30, 190, 'RA')[:2] == (0.0, 'far')
      and JT.mid_geom(350, 30, 100, 'RA')[1] == 'near' and JT.mid_geom(350, 30, 101, 'RA')[1] == 'far', '')
m = JT.mid_score(10.0, 10.05, 0.1, 'Dec')
check('a hit needs both halves: Dec 10 / 10.05 closeness 99.5025 % (45.15) and offset 0.1 on 0.15 (5.56) -> total 50.70; offset 0.16 -> '
      'no score; 10 / 11 closeness 90.9091 % still inside (0.41); 10 / 11.2 = 89.2857 % under 90 % -> no score; RA 100 / 100.5, offset 0.25 '
      'on 0.5 -> 45.15 + 12.50 = 57.65, offset 0.51 -> no score',
      m['hit'] and round(m['score'], 2) == 50.70 and round(m['rscore'], 2) == 45.15 and round(m['dscore'], 2) == 5.56
      and JT.mid_score(10.0, 10.05, 0.16, 'Dec')['score'] is None and round(JT.mid_score(10.0, 11.0, 0.1, 'Dec')['rscore'], 2) == 0.41
      and JT.mid_score(10.0, 11.2, 0.1, 'Dec')['score'] is None and round(JT.mid_score(100.0, 100.5, 0.25, 'RA')['score'], 2) == 57.65
      and not JT.mid_score(100.0, 100.5, 0.51, 'RA')['hit'], str(m))
wb = openpyxl.load_workbook('reference/classic/race_batch_20220601_nottingham_1530_jupiter_tables.xlsx')
ws = sheet_of(wb, 'Dynamic Force')
hd = [c.value for c in ws[next(i for i, rr in enumerate(ws.iter_rows(values_only=True), 1) if rr[0] == 'T10') + 1]]
EQc = hd.index('Equator offset')
r = [c.value for c in row(ws, 'T10', 'S Jupiter / J Uranus | H Uranus')]
check('Dynamic Force T10 S Jupiter / J Uranus | H Uranus Equator (hand from POSITIONS: |Dec| S Jup 0.327192, J Uranus 22.487302, '
      'H Uranus 11.435122): offset +0.027875, distances 11.10793 / 11.05218, closeness 99.4981 %, ratio half 45.11, distance half 33.14, '
      'total 78.25 (yellow)',
      r[EQc:EQc + 5] == [0.027875, 99.4981, 45.11, 33.14, 78.25], str(r[EQc:EQc + 6]))
check('T10 header planes RA (offset, midpoint near / far, closeness %, ratio half, distance half, total), Dec, Equator, no span / tolerance column; FIELD 10 and FIELD 11 have the three planes',
      [h for h in hd if h and str(h).endswith(' offset')] == ['RA offset', 'Dec offset', 'Equator offset'] and hd[3:8] == ['midpoint', 'closeness %', 'ratio half', 'distance half', 'total']
      and not any('span' in str(h) or 'RA far' == h for h in hd)
      and all([x[0] for x in wb[f].iter_rows(values_only=True) if x[0] in ('RA', 'RA far', 'Dec', 'Equator')] == ['RA', 'Dec', 'Equator']
              for f in ('FIELD 10', 'FIELD 11')), str(hd[:10]))
t10 = [r[1] for r in wb['P07'].iter_rows(values_only=True) if r[0] == 'T10']
t11 = [r[1] for r in wb['P07'].iter_rows(values_only=True) if r[0] == 'T11']
jo = ('S Jupiter / H Jupiter | J Jupiter', 'S Jupiter / J Jupiter | H Jupiter', 'H Jupiter / J Jupiter | S Jupiter')
check('the three Jupiter-only midpoint lines are in T11 only (Wincanton P07)', not any(x in t10 for x in jo) and all(x in t11 for x in jo), '')

print('\nTest 11 (Eddie 14 Oct): EQUIDISTANCE — Beverley 14:05 2024 (sky-only workbook), SKY JUPITER')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20240608_beverley_1405.xlsx'))
eq = [r for r in wb['SKY JUPITER'].iter_rows(values_only=True) if r[0] == 'SKY EQ' and r[2]]
# retired 14 Oct 2026 (GC removed): Beverley S Jupiter: S Ceres = S Pallas GC 133.11392 / 133.19155, 0.999417, far side. Beverley's SKY EQ
# has no non-together line left; the value case is moved to Lingfield 14:35 2021 SKY EQ (Equator, found by the rule), checked in test 12.
tg = [r for r in eq if r[10].endswith('X, Y together')]     # columns (14 Oct, revised): closeness %, midpoint offset, ratio half, distance half, total
nt = [r for r in eq if not r[10].endswith('X, Y together')]
# 14 Oct 2026 (midpoint scoring): Beverley's together lines (S Sun = S Pluto Equator, d(X, Y) 0.003798) are no longer hits - Jupiter is
# not near the midpoint of two bodies in conjunction in Dec / Equator - so that case is retired; moved to Newcastle 13:30 2022 P07 (RA far)
check('"X, Y together" lines tagged, d(X, Y) under the conjunction tolerance, and listed at the bottom (Beverley SKY EQ; none left there)',
      (eq[-len(tg):] == tg if tg else True)
      and all(r[11] < (1.5 if r[2] == 'RA' else 0.3) for r in tg) and all(r[11] >= (1.5 if r[2] == 'RA' else 0.3) for r in nt), str(tg))
wn = openpyxl.load_workbook('reference/classic/race_batch_20220102_newcastle_aw_1330_jupiter_tables.xlsx')   # built in test 3
nt7 = [r for r in wn['P07'].iter_rows(values_only=True) if r[0] == 'T17' and r[2]]
tgn = [r for r in nt7 if r[10].endswith('X, Y together')]
check('"X, Y together" (moved): Newcastle 13:30 P07 S Jupiter: H Orcus = H Transpluto RA 179.975528 / 179.599503, far midpoint −0.212485, '
      'd(X, Y) 0.376025 < 1.5, tagged and at the bottom',
      [(r[1], r[2], r[3], r[4], r[6], r[11]) for r in tgn] == [('S Jupiter: H Orcus = H Transpluto', 'RA', 179.975528, 179.599503, '-0.212485 far', 0.376025)]
      and nt7[-1] == tgn[0], str([r[1:13] for r in tgn]))
check('hits only (closeness >= 90 %, total scored), best first above the together lines; no Rahu = Ketu Equator line',
      all(r[5] >= 90 and r[9] is not None for r in eq) and [r[9] for r in nt] == sorted([r[9] for r in nt], reverse=True)
      and not any('Rahu' in r[1] and 'Ketu' in r[1] and r[2] == 'Equator' for r in eq), str(len(eq)))
wb = openpyxl.load_workbook('reference/classic/race_batch_20220321_wincanton_1420_jupiter_tables.xlsx')   # built in test 9 / 10
t17 = [r for r in wb['P07'].iter_rows(values_only=True) if r[0] == 'T17' and r[2]]
f17 = list(wb['FIELD 17'].iter_rows(min_row=4, values_only=True))
check('Wincanton P07 T17 present (H, J and S Jupiter lines) and FIELD 17 with holder counts',
      t17 and {r[1].split(':')[0] for r in t17} == {'H Jupiter', 'J Jupiter', 'S Jupiter'} and f17 and all(str(r[-1]).endswith('/6') for r in f17),
      f'{len(t17)} T17 lines, {len(f17)} FIELD 17 rows')
p1 = [(r[1], r[2]) for r in wb['P05'].iter_rows(values_only=True) if r[0] == 'T17' and r[2]]
# moved 14 Oct 2026 (midpoint scoring; P01 H Sun = H Rahu Equator is no longer a hit): P05, distances 2.196357 / 2.211567 in both
check('Ketu line repeating a Rahu line dropped: P05 S Jupiter: H Juno = H Ketu (Dec) gone, H Juno = H Rahu (Equator) kept',
      ('S Jupiter: H Juno = H Ketu', 'Dec') not in p1 and ('S Jupiter: H Juno = H Rahu', 'Equator') in p1, str([x for x in p1 if 'Juno' in x[0]]))
f17n = list(wn['FIELD 17'].iter_rows(min_row=4, values_only=True))
ok = all(int(str(r[-1]).split('/')[0]) == sum(1 for c in r[2:-1] if c and not str(c).endswith('not counted')) for r in f17 + f17n)
check('FIELD 17 holder counts leave out "X, Y together" cells (Wincanton; moved case Newcastle 13:30 H Orcus = H Transpluto RA 0/5)',
      ok and any(r[0] == 'S Jupiter: H Orcus = H Transpluto' and r[-1] == '0/5' and any(c and str(c).endswith('not counted') for c in r[2:-1])
                 for r in f17n), '')

print('\nTest 12 (Eddie 14 Oct): EQUIDISTANCE family hits and timing — Lingfield AW 14:35 2021 (batch), P09 Pholas / Hollie Doyle')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx'))
sq = [r for r in wb['SKY JUPITER'].iter_rows(values_only=True) if r[0] == 'SKY EQ' and r[1] == 'S Jupiter: S Mars = S Neptune' and r[2] == 'Equator']
check('SKY EQ (moved from Beverley GC, test 11): S Jupiter: S Mars = S Neptune Equator 9.894 / 9.906583, closeness 99.873 %, between, d(X, Y) 19.800583',
      len(sq) == 1 and sq[0][3] == 9.894 and sq[0][4] == 9.906583 and sq[0][5] == 99.873 and sq[0][10] == 'between' and sq[0][11] == 19.800583, str(sq))
eu = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T17' and r[1] == 'S Jupiter: H Uranus = H Pluto' and r[2] == 'Equator']
check('S Jupiter: H Uranus = H Pluto Equator 7.004077 / 6.988434, between, d(X, Y) 13.992511',
      len(eu) == 1 and eu[0][3] == 7.004077 and eu[0][4] == 6.988434 and eu[0][10] == 'between' and eu[0][11] == 13.992511, str(eu))
e = eu[0]
check('families split in value + family cells: 7.004077 | → 7 (whole, 63.38) · applying ..., 6.988434 | → 7 (whole, 17.78) ..., '
      '13.992511 | → 14 (whole, 39.13) · fixed',
      e[13:19] == (7.004077, '→ 7 (whole, 63.38) · applying, exact 16:10 (in 95.7 min)', 6.988434,
                   '→ 7 (whole, 17.78) · applying, exact 19:06 (in 271.6 min)', 13.992511, '→ 14 (whole, 39.13) · fixed'), str(e[13:19]))
cells = next(r for r in wb['P09'].iter_rows() if r[0].value == 'T17' and r[1].value == 'S Jupiter: H Uranus = H Pluto' and r[2].value == 'Equator')
fc = [cells[k].fill.start_color.rgb if cells[k].fill.fill_type else None for k in (14, 16, 18)]
check('family cells coloured by score: 63.38 yellow, 17.78 light, 39.13 light', fc == [YELLOW, LIGHT, LIGHT], str(fc))
check('ratio +5 min 0.997827, -> toward, unison applying, exact 17:38 (in 183.5 min) (race-local, off 14:35)',
      e[19] == 0.997827 and e[20] == '-> toward' and e[21] == 'applying, exact 17:38 (in 183.5 min)', str(e[19:22]))
na = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T17' and r[2] and r[1].startswith(('H Jupiter', 'J Jupiter'))]
check('natal-only lines: timing "fixed", no +5 ratio; each family hit "· fixed"', na and all(r[21] == 'fixed' and r[19] is None
      and all(c.endswith('· fixed') for c in r[14:19:2] if c and c.startswith('→')) for r in na),
      str(len(na)))

print('\nTest 13 (Eddie 14 Oct): T18 horse | jockey equidistance side by side — Lingfield AW 14:35 2021, P09')
t18 = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T18']
bi = [i for i, r in enumerate(t18) if str(r[1]).startswith('T18 block')]
b1 = [r for r in t18[bi[0] + 1:bi[1]] if r[1] != 'X–Y']
b2 = [r for r in t18[bi[1] + 1:] if r[1] != 'X–Y']
up = [r for r in b1 if r[1] == 'Uranus–Pluto']
check('block 1 row Uranus–Pluto: horse Equator closeness 99.7767 % | jockey Dec 99.4741 %',
      len(up) == 1 and up[0][2] == 'Equator' and up[0][5] == 99.7767 and up[0][12] == 'Dec' and up[0][15] == 99.4741, str(up))
hs = [r for r in b1 if r[9] is not None]                  # side = 10 columns (14 Oct, revised); horse total col 9, jockey total col 19
js = [r for r in b1 if r[9] is None]
check('block 1 sorted: horse-inside rows by horse score, then jockey-only rows by jockey score; outside side plain (no score)',
      b1 == hs + js and [r[9] for r in hs] == sorted([r[9] for r in hs], reverse=True)
      and [r[19] for r in js] == sorted([r[19] for r in js], reverse=True) and all(r[7] is None and r[10] is None for r in js), '')
check('no "X, Y together" side; block 2 present', not any('together' in str(c) for r in b1 + b2 for c in r) and len(b2) > 0, f'{len(b1)} / {len(b2)} rows')

check('T18 Uranus–Pluto (both inside 1 %) tagged "both"; block 1 title carries the both count', up[0][22] == 'both'
      and 'both (horse and jockey midpoint hits): ' in t18[bi[0]][1] and int(t18[bi[0]][1].rsplit(': ', 1)[1]) == sum(r[22] == 'both' for r in b1),
      str(up[0][22]))

p11 = [r[1] for r in wb['P11'].iter_rows(values_only=True) if r[0] == 'T18']
p11k = [r for r in wb['P11'].iter_rows(values_only=True) if r[0] == 'T18' and r[1] == 'Vesta–Ketu']
check('T18 P11 Vesta–Ketu kept since Ketu is in every plane (14 Oct): horse side Ketu RA 148.226037 / 179.265084 differs from the Rahu row '
      '(jockey side Dec 11.035301 / 11.049429 = Rahu Equator)', 'Vesta–Rahu' in p11 and len(p11k) == 1 and p11k[0][2] == 'RA'
      and p11k[0][3] == 148.226037 and p11k[0][12] == 'Dec' and p11k[0][13] == 11.035301, str(p11k))

print('\nTest 14 (Eddie 14 Oct): T19 sky Jupiter on natal pairs + P09 PAIRS — Lingfield AW 14:35 2021')
t19 = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T19']
uq = [r for r in t19 if r[2] == 'H Uranus – H Pluto' and r[3] == 'Equator']
check('T19 S Jupiter on H Uranus – H Pluto Equator: 7 / 7 / 14 (whole), ratio 1.002238 unison, between, (also T17); '
      'ratio on the interval list only (15 Oct): unison 60.24; midpoint in its own cells: offset (7.004077 − 6.988434) / 2 = +0.007822, '
      'closeness 99.7767 %, ratio half 47.79, distance half 44.92, midpoint total 92.71',
      len(uq) == 1 and uq[0][5].startswith('→ 7 (whole, 63.38)') and uq[0][7].startswith('→ 7 (whole, 17.78)') and uq[0][9] == '→ 14 (whole, 39.13) · fixed'
      and uq[0][10] == 1.002238 and uq[0][11] == '1 · unison · Perfect' and uq[0][15] == 'between' and uq[0][16] == '(also T17)'
      and uq[0][17] == '+0.007822' and uq[0][18] == 99.7767 and uq[0][19] == 47.79 and uq[0][20] == 44.92 and uq[0][13] == 60.24 and uq[0][21] == 92.71, str(uq))
ps = [r for r in t19 if r[2] == 'H Pluto – H Sedna' and r[3] == 'Equator']
check('T19 H Pluto – H Sedna Equator (Eddie 15 Oct): ratio 1.011174 outside unison ±1 % (+1.11741 %, no ratio score); '
      'midpoint hit in its own cells: closeness 98.8949 %, 39.56 + 27.36 = 66.92; listed for the midpoint',
      len(ps) == 1 and ps[0][10] == 1.011174 and ps[0][11] == '1 · unison · Perfect — outside ±1 %' and ps[0][12] == '+1.11741%'
      and ps[0][13] is None and ps[0][18] == 98.8949 and ps[0][19] == 39.56 and ps[0][20] == 27.36 and ps[0][21] == 66.92, str(ps))
best = lambda r: max(-1 if r[13] is None else r[13], -1 if len(r) < 22 or r[21] is None else r[21])
sc = [best(r) for r in t19]
check('T19 filter: interval hit, midpoint hit or all three families; no together; sorted by the higher of ratio score and midpoint total; '
      'no star–star, stars royal only',
      all(r[13] is not None or r[21] is not None or all(c and c.startswith('→') for c in (r[5], r[7], r[9])) for r in t19)
      and sc == sorted(sc, reverse=True)
      and not any(r[16] and 'together' in r[16] for r in t19)
      and all(sum(p.split(' ', 1)[1] in ('Algol', 'Pleiades', 'Capella', 'Sirius', 'Procyon', 'Alkaid', 'Algorab', 'Spica', 'Arcturus', 'Alphecca',
              'Vega', 'Deneb Algedi', 'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix', 'Aldebaran', 'Regulus', 'Antares',
              'Fomalhaut') for p in r[2].split(' – ')) <= 1 for r in t19)
      and not any(p.split(' ', 1)[1] in ('Algol', 'Sirius', 'Vega', 'Polaris') for r in t19 for p in r[2].split(' – ')), f'{len(t19)} rows')
wbp = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_pairs.xlsx', read_only=True)
check('P## PAIRS in the separate _pairs.xlsx workbook, not in the tables workbook',
      'P09 PAIRS' in wbp.sheetnames and not any(n.endswith(' PAIRS') for n in wb.sheetnames), str(wbp.sheetnames))
pr = [r for r in wbp['P09 PAIRS'].iter_rows(min_row=3, values_only=True)]
t17t = {(r[1].split(': ', 1)[1].replace(' = ', ' – '), r[2]): r[21] for r in wb['P09'].iter_rows(values_only=True)
        if r[0] == 'T17' and r[2] and r[1].startswith('S Jupiter')}  # col 20 = unison timing
same = [(k, t17t[k], r[14]) for r in t19 for k in [(r[2], r[3])] if k in t17t and r[11].startswith('1 ·')]
check('one timing method: the same unison pair gives the same exact time in T17 and T19', same and all(a == b for _, a, b in same),
      str([x for x in same if x[1] != x[2]][:3]))
check('H–J across = the same body in both charts only (bodies, no stars), in T19 and PAIRS',
      all(r[2].split(' – ')[0][2:] == r[2].split(' – ')[1][2:] and r[2].split(' – ')[0][2:] not in ('Aldebaran', 'Regulus', 'Antares', 'Fomalhaut',
          'Polaris', 'Sirius') for r in t19 + pr if r[1] == 'H–J'), '')
check('P09 PAIRS unfiltered (blocks H–H, J–J, H–J; outside ratios plain; together tagged; stars all 22)',
      len(pr) > len(t19) and {r[1] for r in pr} == {'H–H', 'J–J', 'H–J'} and any(r[13] is None and 'outside' in r[11] for r in pr)
      and any(r[16] and 'X, Y together' in r[16] for r in pr) and any('Polaris' in r[2] for r in pr), f'{len(pr)} rows')
sk = [r for r in wb['SKY JUPITER'].iter_rows(values_only=True) if r[0] == 'SKY STARS' and r[3]]
check('SKY JUPITER: S Jupiter on two sky stars (background, star–star only)', sk and all(r[1] == 'S–S' for r in sk), f'{len(sk)} rows')

# Eddie 14 Oct: SKY PAIRS (S Jupiter on two sky bodies, Moon included, no stars, filtered as T19) and the T17 pair rule
STARN = ('Algol', 'Pleiades', 'Capella', 'Sirius', 'Procyon', 'Alkaid', 'Algorab', 'Spica', 'Arcturus', 'Alphecca', 'Vega', 'Deneb Algedi',
         'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix', 'Aldebaran', 'Regulus', 'Antares', 'Fomalhaut')
sp = [r for r in wb['SKY JUPITER'].iter_rows(values_only=True) if r[0] == 'SKY PAIRS' and r[3]]
spc = [best(r) for r in sp]
check('SKY PAIRS: S Jupiter on two sky bodies (S–S, no stars, no together, interval hit, midpoint hit or all three families, best first by the higher of ratio score and midpoint total)',
      sp and all(r[1] == 'S–S' and not any(q[2:] in STARN for q in r[2].split(' – ')) for r in sp)
      and not any(r[16] and 'together' in r[16] for r in sp) and spc == sorted(spc, reverse=True)
      and all(r[13] is not None or r[21] is not None or all(c and c.startswith('→') for c in (r[5], r[7], r[9])) for r in sp), f'{len(sp)} rows')
mixed = []
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx',
          'reference/classic/race_batch_20220601_nottingham_1530_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    for n in w.sheetnames:
        if n[0] == 'P' and n[1:].isdigit():
            for r in w[n].iter_rows(values_only=True):
                if r[0] == 'T17' and r[2] and isinstance(r[1], str) and ': ' in r[1]:
                    x, y = r[1].split(': ', 1)[1].split(' = ')
                    if x[0] != y[0] and x[2:] != y[2:]:
                        mixed.append((n, r[1]))
check('T17: S Jupiter pairs H–H, J–J or the same body H X – J X only (no other H–J mixed rows; Lingfield, Nottingham)', not mixed, str(mixed[:3]))

own = []
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20210402_lingfield_aw_1435_pairs.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    for n in w.sheetnames:
        for r in w[n].iter_rows(values_only=True):
            if r and r[0] in ('T17', 'T18', 'T19', 'PAIRS', 'SKY EQ', 'SKY PAIRS') and isinstance(r[1], str) and isinstance(r[2], str):
                t = r[2] if r[0] in ('T19', 'PAIRS', 'SKY PAIRS') else r[1]
                for C in 'SHJ':
                    if f'{C} Rahu' in t and f'{C} Ketu' in t or (r[0] == 'T18' and t == 'Rahu–Ketu'):
                        own.append((n, r[0], t))
check("a chart's own Rahu–Ketu pair never paired, any plane (T17, T18, T19, PAIRS, SKY EQ, SKY PAIRS; Lingfield)", not own, str(own[:3]))

print('\nTest 15 (Eddie 14 Oct 2026): midpoint scoring — Haydock 14:20 2021, P03 Golden Flame / Joe Fanning, T11 Uranus row')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20210904_haydock_1420.xlsx'))
ws = wb['P03']
hd = [c.value for c in ws[next(i for i, rr in enumerate(ws.iter_rows(values_only=True), 1) if rr[0] == 'T11') + 1]]
r = [c.value for c in row(ws, 'T11', 'H Jupiter / J Jupiter | S Uranus')]
check('T11 H Jupiter / J Jupiter | S Uranus RA far (revised scoring, checked by hand from POSITIONS): offset 0.032036, closeness 99.963 %, '
      'ratio half 49.63, distance half 43.80, total 93.43',
      r[2:8] == [0.032036, 'far', 99.963, 49.63, 43.8, 93.43], str(r[2:9]))
pos = {(x[0], x[2], x[3]): (x[5], x[6]) for x in wb['POSITIONS'].iter_rows(min_row=5, values_only=True) if x and x[3]}
u, hj, jj = pos[('SKY', 'S', 'Uranus')], pos[('P03', 'H', 'Jupiter')], pos[('P03', 'J', 'Jupiter')]
arc = lambda a, b: abs((a - b + 180) % 360 - 180)
check('its distances from POSITIONS: d(S Uranus, H Jupiter) RA 173.135571, d(S Uranus, J Jupiter) RA 173.071498 (the hand values '
      '173.135586 / 173.071514 were 0.000015 high; the offset, ratio and scores are unchanged)',
      round(arc(u[0], hj[0]), 6) == 173.135571 and round(arc(u[0], jj[0]), 6) == 173.071498, f'{arc(u[0], hj[0]):.6f} {arc(u[0], jj[0]):.6f}')
th = str([c.value for c in next(rr for rr in wb['THREADS'].iter_rows(min_row=4) if rr[0].value == 'Uranus')][1 + sorted(
    n for n in wb.sheetnames if n[0] == 'P' and n[1:].isdigit()).index('P03')])
check('THREADS: the midpoint hit counts (Golden Flame Uranus cell lists it)', 'mid H Jup / J Jup | S Uranus RA' in th and '(93.43)' in th, th[:300])
wn3 = openpyxl.load_workbook('reference/classic/race_batch_20220601_nottingham_1530_jupiter_tables.xlsx')   # built in test 1
hd3 = [c.value for c in wn3['P03'][next(i for i, rr in enumerate(wn3['P03'].iter_rows(values_only=True), 1) if rr[0] == 'T11') + 1]]
r3 = [c.value for c in row(wn3['P03'], 'T11', 'H Jupiter / J Jupiter | S Sun')]
e3 = hd3.index('Equator offset')
check('short span (found by the rule; checked by hand from POSITIONS): Nottingham 15:30 2022 P03 T11 H Jupiter / J Jupiter | S Sun Equator, '
      '|Dec| H Jupiter 22.301199, J Jupiter 21.820645 (span 0.4806), S Sun 22.057924: offset −0.002998, distances 0.243275 / 0.237279, '
      'closeness 97.5353 %, ratio half 28.39, distance half 48.02, total 76.41',
      r3[e3:e3 + 5] == [-0.002998, 97.5353, 28.39, 48.02, 76.41], str(r3[e3:e3 + 6]))
bad, NH = [], 0
for n in [n for n in wb.sheetnames if n[0] == 'P' and n[1:].isdigit()]:
    hdr = None
    for rr in wb[n].iter_rows(values_only=True):
        if rr[0] == 'table' and rr[2] == 'RA offset':
            hdr = rr
        if rr[0] in ('T10', 'T11') and hdr and isinstance(rr[1], str) and ' | ' in rr[1]:
            for j, h in enumerate(hdr):
                if h == 'total':
                    rs, ds, sc = rr[j - 2], rr[j - 1], rr[j]
                    NH += sc is not None
                    if sc is not None and not (isinstance(rs, (int, float)) and isinstance(ds, (int, float)) and abs(rs + ds - sc) <= 0.011):
                        bad.append((n, rr[1], rs, ds, sc))
                    if sc is None and isinstance(rs, (int, float)) and isinstance(ds, (int, float)):
                        bad.append((n, rr[1], 'both halves inside but no score'))
check('every midpoint hit: total = ratio half + distance half; no score unless both halves inside (Haydock, all runners)', not bad and NH > 0, f'{NH} hits; {bad[:3]}')

# Eddie 14 Oct 2026: planes RA, Dec, Equator only - no Flat or GC column, row or text in any sheet of either workbook
import glob, re
pat, fg = re.compile(r'\b(Flat|GC)\b'), []
for f in sorted(glob.glob('reference/classic/race_batch_*_jupiter_tables.xlsx') + glob.glob('reference/classic/race_batch_*_pairs.xlsx')):
    if os.path.getmtime(f) < T0:
        continue                                           # built in this run only
    w = openpyxl.load_workbook(f, read_only=True)
    fg += [(os.path.basename(f), n) for n in w.sheetnames for r in w[n].iter_rows(values_only=True) for v in (r or ())
           if isinstance(v, str) and pat.search(v)]
check('no Flat or GC column, row or label in any sheet of the tables and pairs workbooks built in this run',
      not fg and NBUILT[0] >= 6, f'{NBUILT[0]} tables workbooks; {fg[:3]}')

# Eddie 15 Oct 2026: no conjunction family hit in the Equator plane (T17, T18, T19, SKY EQ, SKY PAIRS, PAIRS)
eqc = []
for f in sorted(glob.glob('reference/classic/race_batch_*_jupiter_tables.xlsx') + glob.glob('reference/classic/race_batch_*_pairs.xlsx')):
    if os.path.getmtime(f) < T0:
        continue
    w = openpyxl.load_workbook(f, read_only=True)
    eqc += [(os.path.basename(f), n, r[2]) for n in w.sheetnames for r in w[n].iter_rows(values_only=True)
            if r and 'Equator' in r and any(isinstance(v, str) and '(conj,' in v for v in r)]
wbl = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', read_only=True)
lp9 = [r for r in wbl['P01'].iter_rows(values_only=True) if r[0] == 'T19' and r[2] == 'H Sun – H Ceres' and r[3] == 'Equator']
check('no conjunction in the Equator plane (Eddie 15 Oct): no Equator row with a conj family cell in any sheet built in this run; '
      'Lingfield P01 H Sun – H Ceres Equator (d(S Jup, H Sun) 0.116879, listed before only for its conj) gone from T19',
      not eqc and not lp9, f'{eqc[:3]} {lp9}')

# Eddie 15 Oct 2026: T15 (apex ratios) removed - no T15 row, no FIELD 15 sheet, no T15 line in RATIOS / THREADS, in any workbook built in this run
t15 = []
for f in sorted(glob.glob('reference/classic/race_batch_*_jupiter_tables.xlsx')):
    if os.path.getmtime(f) < T0:
        continue
    w = openpyxl.load_workbook(f, read_only=True)
    t15 += [(os.path.basename(f), 'FIELD 15')] if 'FIELD 15' in w.sheetnames else []
    t15 += [(os.path.basename(f), n) for n in w.sheetnames for r in w[n].iter_rows(values_only=True)
            if r and (r[0] == 'T15' or (len(r) > 1 and r[1] == 'T15') or any(isinstance(v, str) and '[T15' in v for v in r))]
check('T15 removed (Eddie 15 Oct): no T15 row, no FIELD 15 sheet, no T15 ratio in RATIOS or THREADS', not t15, str(t15[:3]))

# Eddie 15 Oct 2026: T20 natal Jupiter as the midpoint of sky X and natal X (horse | jockey per body), FIELD 20, THREADS
print('\nTest 16 (Eddie 15 Oct): T20 — Lingfield AW 14:35 2021 P03, S Sun / H Sun | H Jupiter Dec')
t20 = [r for r in wbl['P03'].iter_rows(values_only=True) if r and r[0] == 'T20' and r[1] == 'Sun']
check('T20 P03 Sun horse Dec (found by the rule; checked by hand from POSITIONS): Dec S Sun 5.028708, H Sun 10.292917, H Jupiter 7.682992 -> '
      'd 2.654284 / 2.609925, offset +0.022180, closeness 98.3287 %, ratio half 34.68, distance half 36.31, total 70.99; '
      'ratio 1.016997 -> 1.016486 at +5 min: applying, exact 17:21 (in 166.5 min)',
      len(t20) == 1 and t20[0][9:15] == (0.02218, 98.3287, 34.68, 36.31, 70.99, 'applying, exact 17:21 (in 166.5 min)'), str(t20[0][9:15] if t20 else t20))
hd20 = next(r for r in wbl['P03'].iter_rows(values_only=True) if r and r[0] == 'table' and r[1] == 'body')
check('T20 layout: one line per body, horse RA (offset, midpoint, closeness, halves, total, timing), Dec, Equator | jockey the same',
      hd20[2] == 'H RA offset' and hd20[3] == 'H midpoint' and hd20[9] == 'H Dec offset' and hd20[15] == 'H Equator offset'
      and hd20[21] == 'J RA offset' and hd20[28] == 'J Dec offset' and hd20[34] == 'J Equator offset' and hd20[39] == 'J timing', str(hd20[:41]))
nb = [r[1] for r in wbl['P03'].iter_rows(values_only=True) if r and r[0] == 'T20' and isinstance(r[1], str) and not r[1].startswith('T20')]
check('T20 bodies only: no stars, no Moon, not Jupiter; non-hits plain (no total)', nb and not set(nb) & {'Moon', 'Jupiter', 'Regulus', 'Sirius', 'Aldebaran'}
      and 'Sun' in nb and t20[0][7] is None, f'{len(nb)} bodies')
f20 = [r for r in wbl['FIELD 20'].iter_rows(values_only=True) if r and r[0] == 'Sun']
check('FIELD 20: Sun row, P03 column "H Dec 70.99", count 1/6',
      len(f20) == 1 and f20[0][2] == 'H Dec 70.99' and f20[0][-1] == '1/6', str(f20))
th20 = [r for r in wbl['THREADS'].iter_rows(values_only=True) if r and r[0] == 'Sun']
check('THREADS: the T20 hit is a Jupiter–Sun link in P03 (total 70.99 >= 50)',
      th20 and 'mid S Sun / H Sun | H Jup Dec +0.022180 → midpoint (70.99) [T20]' in str(th20[0][2]), str(th20[0][2])[:300] if th20 else '')

# Eddie 15 Oct 2026: THREADS midpoint hits count only at total >= 50 (P07 J Uranus T20 Dec 35.33 is a hit, not listed, in '+ n weaker')
hp = next(i for i, c in enumerate(next(wbl['THREADS'].iter_rows(min_row=3, max_row=3, values_only=True))) if c and str(c).startswith('P07'))
thu = [r for r in wbl['THREADS'].iter_rows(values_only=True) if r and r[0] == 'Uranus']
check('THREADS midpoints at total >= 50 only (Eddie 15 Oct): Lingfield P07 J Uranus T20 Dec 35.33 not listed, counted in "+ n weaker"',
      thu and '[T20]' not in str(thu[0][hp]) and 'weaker' in str(thu[0][hp]), str(thu[0][hp])[:300] if thu else '')

print(f'\n{sum(RES)}/{len(RES)} passed')
sys.exit(0 if all(RES) else 1)
