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
import os, re, subprocess, sys
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
check('P05 RATIOS: the Rahu RA unison row 1.005972 (49.20 on ±0.02 absolute, area A; was 16.23 on 1 %) with field 2/6', len(rs) == 1 and rs[0][4] == 1.005972 and rs[0][9] == 49.2
      and rs[0][11] == '2/6', str(rs))
f12, pl, ar = [], None, None
for x in wb['FIELD 12'].iter_rows(values_only=True):
    pl = x[0] if x[0] in ('RA', 'Dec') else pl
    ar = x[0][len(pl) + 3:len(pl) + 9] if pl and isinstance(x[0], str) and x[0].startswith(pl + ' — ') else ar   # 'AREA A' / 'AREA B' / 'NO HIT'
    if pl == 'RA' and ar == 'AREA A' and x[0] == lab:
        f12.append(x)
check('FIELD 12 (RA) area A tags it "field 2/6" for P05 and P11', len(f12) == 1 and sum(isinstance(v, str) and 'field 2/6' in v for v in f12[0][1:]) == 2, str(f12))

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
# 15 Oct 2026 (Eddie): unison on ±0.02 absolute (was 1 %): 22 -> 25 unisons, 3 more genuine (Pallas RA, Makemake Dec, Haumea Dec)
check("Cobden's 25 unisons (±0.02 absolute, RA / Dec): 20 automatic (all RA); 5 genuine, all return-assisted 1/6 "
      "(T13 J Gonggong RA 1.001741, J Ketu RA 1.001694, J Pallas RA 1.013747, J Makemake Dec 1.013955, J Haumea Dec 1.019953)",
      len(rs) == 25 and na == 20 and all(x[3] == 'RA' for x in rs if 'automatic' in x[11]) and gp == ['Dec', 'Dec', 'RA', 'RA', 'RA']
      and g == [('S Jupiter–J Gonggong / J Jupiter–J Gonggong', 1.001741, '1/6 return-assisted'),
                ('S Jupiter–J Haumea / J Jupiter–J Haumea (inverted)', 1.019953, '1/6 return-assisted'),
                ('S Jupiter–J Ketu / J Jupiter–J Ketu', 1.001694, '1/6 return-assisted'),
                ('S Jupiter–J Makemake / J Jupiter–J Makemake (inverted)', 1.013955, '1/6 return-assisted'),
                ('S Jupiter–J Pallas / J Jupiter–J Pallas', 1.013747, '1/6 return-assisted')], f'{len(rs)} rows, {na} automatic, genuine {g}')
# retired 14 Oct 2026 (GC removed): River Bray (P07) T13 J Pluto GC unison 2/6, not tagged (built on GC; P07 has no unison now)
# 15 Oct 2026: P03 now has a Harmonic hit (area A ±0.02); the check is now: every group header has rows under it
rr = list(wb['P03 RATIOS'].iter_rows(values_only=True))
heads = [(i, x[0]) for i, x in enumerate(rr) if x[0] in ('Perfect', 'Imperfect', 'Dissonant', 'Septimal', 'Harmonic', 'High', 'Phi') and x[1] is None]
empty = [g for i, g in heads if not (i + 2 < len(rr) and rr[i + 2][0] == g)]
check('P03 RATIOS: no empty group header', heads and not empty, f'{heads} empty {empty}')

print('\nTest 7: Sandown 14:25 2021 (batch xlsx) — tapered ratio tolerances, nearest target outside the tolerance')
wb = openpyxl.load_workbook('reference/classic/race_batch_20211204_sandown_1425_jupiter_tables.xlsx')   # built in test 4
ws = wb['P05']
r = row(ws, 'T12', 'S Jupiter–S Mars / H Jupiter–H Mars')
v, t, o, f, sc = cell(r, 'RA')
check('P05 T12 RA S Jupiter–S Mars / H Jupiter–H Mars 1.002631 -> unison inside ±0.02 absolute (15 Oct; was 1 %), +0.00263, score '
      '(10 (0.02 − 0.002631) / 0.02)² = 75.42, yellow',
      round(v, 6) == 1.002631 and t == '1 · unison · Perfect (inverted)' and o == '+0.00263' and sc == 75.42 and f == YELLOW, f'{v} {t} {o} {sc} {f}')
# retired 14 Oct 2026 (Flat removed): Flat 1.0445 outside every band (nearest by tightness), P05 Flat Haumea 1.506122 outside 3/2,
# P05 Flat Makemake 1.499624 3/2 (85.52), P09 Flat Mars 1.125048 9/8 (94.37). The 3/2 and 9/8 cases are moved to RA (P07, found by the rule).
v, t, o, f, sc = cell(row(wb['P07'], 'T12', 'S Jupiter–S Vesta / H Jupiter–H Vesta'), 'RA')
check('3/2 hit on ±0.02 absolute (15 Oct; was 0.333 %): P07 T12 RA Vesta 1.499361, -0.00064, score (10 (0.02 − 0.000639) / 0.02)² = 93.71, green',
      round(v, 6) == 1.499361 and t == '3/2 · fifth · Perfect (inverted)' and o == '-0.00064' and sc == 93.71
      and round((10 * (0.02 - 0.000639) / 0.02) ** 2, 2) == 93.71 and f == GREEN, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(wb['P07'], 'T13', 'S Jupiter–J Mars / J Jupiter–J Mars'), 'RA')
check('9/8 on 0.15 % (moved from Flat): P07 T13 RA J Mars 1.125881, +0.07832 %, score (10 (0.15 − 0.07832) / 0.15)² = 22.83, light',
      round(v, 6) == 1.125881 and t == '9/8 · major second · Dissonant (inverted)' and o == '+0.07832%' and sc == 22.83
      and round((10 * (0.15 - 0.07832) / 0.15) ** 2, 1) == 22.8 and f == LIGHT, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(ws, 'T5', 'S Jupiter → H Mars'), 'Dec')
check('degrees outside every family: T5 S Jupiter → H Mars Dec 8.398276 -> 5×φ (golden) — outside ±0.0324, +0.30811, plain',
      t == '5×φ (golden) — outside ±0.0324' and o == '+0.30811' and sc is None and f is None, f'{v} {t} {o} {sc} {f}')
import families
TK = ('1', '2', '3/2', '3', '4/3', '4', '5/4', '5', '5/2', '5/3', '6/5', '8/5', '8/3', '9/4', '7/4', '13/4', '11/5', '7/2', '√2', '1+1/√2', 'φ')
check('Phi group = φ, φ², φ³, 1+√2 only; area A (1, 3/2, 2, 3 ... 9) ±0.02 absolute (15 Oct); area B by the larger number (1 % / k, 0.15 % from k = 6)',
      [i[0] for i in families.INTERVALS if i[3] == 'Phi'] == ['φ', 'φ²', 'φ³', '1+√2']
      and families.AREA_A == ('1', '3/2', '2', '3', '4', '5', '6', '7', '8', '9')
      and [round(families.TOL[k], 3) for k in TK] == [0.02, 0.02, 0.02, 0.02, 0.25, 0.02, 0.2, 0.02, 0.2, 0.2] + [0.15] * 11
      and all(families.TOL[k] == 0.15 for k in families.TOL
              if k[0].isdigit() and '√' not in k and k not in families.AREA_A and max(int(x) for x in k.split('/')) >= 6), str(families.TOL))

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
      'ratio on the interval list only (15 Oct): unison 78.87 (±0.02 absolute; was 60.24 on 1 %); midpoint in its own cells: offset (7.004077 − 6.988434) / 2 = +0.007822, '
      'closeness 99.7767 %, ratio half 47.79, distance half 44.92, midpoint total 92.71',
      len(uq) == 1 and uq[0][5].startswith('→ 7 (whole, 63.38)') and uq[0][7].startswith('→ 7 (whole, 17.78)') and uq[0][9] == '→ 14 (whole, 39.13) · fixed'
      and uq[0][10] == 1.002238 and uq[0][11] == '1 · unison · Perfect' and uq[0][15] == 'between' and uq[0][16] == '(also T17)'
      and uq[0][17] == '+0.007822' and uq[0][18] == 99.7767 and uq[0][19] == 47.79 and uq[0][20] == 44.92 and uq[0][13] == 78.87 and uq[0][21] == 92.71, str(uq))
ps = [r for r in t19 if r[2] == 'H Pluto – H Sedna' and r[3] == 'Equator']
check('T19 H Pluto – H Sedna Equator (Eddie 15 Oct): ratio 1.011174 now inside unison ±0.02 absolute (+0.01117, (10 (0.02 − 0.011174) / 0.02)² = 19.47; '
      'was outside ±1 %); midpoint hit in its own cells: closeness 98.8949 %, 39.56 + 27.36 = 66.92',
      len(ps) == 1 and ps[0][10] == 1.011174 and ps[0][11] == '1 · unison · Perfect' and ps[0][12] == '+0.01117'
      and ps[0][13] == 19.47 and ps[0][18] == 98.8949 and ps[0][19] == 39.56 and ps[0][20] == 27.36 and ps[0][21] == 66.92, str(ps))
best = lambda r: max(-1 if r[13] is None else r[13], -1 if len(r) < 22 or r[21] is None else r[21])


def blocks(ws, tid):
    """rows of a pair table by area block (15 Oct 2026): {'A': [...], 'B': [...], 'rest': [...]}"""
    out, cur = {}, None
    for r in ws.iter_rows(values_only=True):
        if r and isinstance(r[0], str) and r[0].startswith(tid + ' ') and ': ' in r[0]:
            cur = 'A' if 'AREA A' in r[0] else 'P' if 'AREA φ' in r[0] else 'B' if 'AREA B' in r[0] else 'rest'
        elif r and r[0] == tid:
            out.setdefault(cur, []).append(r)
    return out


sorted_blocks = lambda bl: all([best(r) for r in v] == sorted([best(r) for r in v], reverse=True) for v in bl.values())
sc = [best(r) for r in t19]
check('T19 filter: interval hit, midpoint hit or all three families; no together; sorted by the higher of ratio score and midpoint total; '
      'no star–star, stars royal only',
      all(r[13] is not None or r[21] is not None or all(c and c.startswith('→') for c in (r[5], r[7], r[9])) for r in t19)
      and sorted_blocks(blocks(wb['P09'], 'T19'))                       # best first inside each area block (15 Oct)
      and not any(r[16] and 'together' in r[16] for r in t19)
      and all(sum(p.split(' ', 1)[1] in ('Algol', 'Pleiades', 'Capella', 'Sirius', 'Procyon', 'Alkaid', 'Algorab', 'Spica', 'Arcturus', 'Alphecca',
              'Vega', 'Deneb Algedi', 'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix', 'Aldebaran', 'Regulus', 'Antares',
              'Fomalhaut') for p in r[2].split(' – ')) <= 1 for r in t19)
      and not any(p.split(' ', 1)[1] in ('Algol', 'Sirius', 'Vega', 'Polaris') for r in t19 for p in r[2].split(' – ')), f'{len(t19)} rows')
wbp = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_pairs.xlsx', read_only=True)
check('P## PAIRS in the separate _pairs.xlsx workbook, not in the tables workbook',
      'P09 PAIRS' in wbp.sheetnames and not any(n.endswith(' PAIRS') for n in wb.sheetnames), str(wbp.sheetnames))
pr = [r for r in wbp['P09 PAIRS'].iter_rows(min_row=3, values_only=True) if r and r[0] == 'PAIRS']   # data rows (block titles / headers left out)
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
ROYALN = ('Aldebaran', 'Regulus', 'Antares', 'Fomalhaut')
# 15 Oct 2026 (Eddie): body – royal rows added (one sky body, one royal star), in the same blocks and sort
check('SKY PAIRS: S Jupiter on two sky bodies (S–S, no stars) or a sky body and a royal star ("body – royal", 15 Oct), no together, interval hit, '
      'midpoint hit or all three families, best first by the higher of ratio score and midpoint total',
      sp and all((r[1] == 'S–S' and not any(q[2:] in STARN for q in r[2].split(' – '))) or
                 (r[1] == 'body – royal' and r[2].split(' – ')[0][2:] not in STARN + ('Jupiter',) and r[2].split(' – ')[1][2:] in ROYALN) for r in sp)
      and {r[1] for r in sp} == {'S–S', 'body – royal'}
      and not any(r[16] and 'together' in r[16] for r in sp) and sorted_blocks(blocks(wb['SKY JUPITER'], 'SKY PAIRS'))
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

# Eddie 15 Oct 2026: T21 natal Jupiter on natal star pairs, T22 fixed star as the apex (sky Jupiter against natal Jupiter), FIELD 21 / 22
print('\nTest 17 (Eddie 15 Oct): T21 / T22 fixed stars — Lingfield AW 14:35 2021')
t21 = [r for r in wbl['P03'].iter_rows(values_only=True) if r and r[0] == 'T21' and r[1] == 'Algorab – Castor' and r[2] == 'Dec']
check('T21 P03 horse H Jupiter: H Algorab – H Castor Dec (found by the rule; by hand from POSITIONS: Dec H Jupiter 7.682992, Algorab −16.518521, '
      'Castor 31.888664): 24.201513 / 24.205672 / 48.407186, ratio 1.000172 unison (98.29 on ±0.02 absolute; was 96.59 on 1 %), between, midpoint −0.002079, closeness 99.9828 %, '
      '49.83 + 48.62 = 98.45, fixed',
      len(t21) == 1 and t21[0][3] == 24.201513 and t21[0][5] == 24.205672 and t21[0][7] == 48.407186 and t21[0][9] == 1.000172
      and t21[0][10] == '1 · unison · Perfect' and t21[0][12] == 98.29 and t21[0][13] == 'fixed' and t21[0][14] == 'between'
      and t21[0][16] == '-0.002079' and t21[0][17] == 99.9828 and t21[0][18] == 49.83 and t21[0][19] == 48.62 and t21[0][20] == 98.45, str(t21[0][:21] if t21 else t21))
t22 = [r for r in wbl['P11'].iter_rows(values_only=True) if r and r[0] == 'T22' and r[1] == 'Aldebaran' and r[2] == 'RA']
check('T22 P11 horse d(Aldebaran, S Jupiter) / d(Aldebaran, H Jupiter) RA (found by the rule; by hand from POSITIONS: RA S Aldebaran 68.977553, '
      'S Jupiter 325.797311, H Jupiter 171.578818): 103.180242 / 102.601266, ratio 1.005643 unison (51.53 on ±0.02 absolute; was 18.98), applying, exact 05 Apr 2021 16:21 '
      '(in 4426.2 min); midpoint far +0.289488, closeness 99.4389 %, 44.55 + 8.86 = 53.41',
      len(t22) == 1 and t22[0][3] == 103.180242 and t22[0][5] == 102.601266 and t22[0][7] == 1.005643 and t22[0][8] == '1 · unison · Perfect'
      and t22[0][10] == 51.53 and t22[0][12] == 'applying, exact 05 Apr 2021 16:21 (in 4426.2 min)' and t22[0][13] == '+0.289488 far'
      and t22[0][14] == 99.4389 and t22[0][15] == 44.55 and t22[0][16] == 8.86 and t22[0][17] == 53.41, str(t22[0][:18] if t22 else t22))
n22 = [r for r in wbl['P11'].iter_rows(values_only=True) if r and r[0] == 'T22' and r[2] in ('RA', 'Dec', 'Equator')]
check('T22 lists every star (22), RA and Dec each', {r[1] for r in n22 if r[2] == 'RA'} == set(STARN) and {r[1] for r in n22 if r[2] == 'Dec'} == set(STARN),
      f'{len(n22)} lines')
f21 = [r for r in wbl['FIELD 21'].iter_rows(values_only=True) if r and r[0] == 'Algorab – Castor']
f22 = [r for r in wbl['FIELD 22'].iter_rows(values_only=True) if r and r[0] == 'Aldebaran']
check('FIELD 21 / 22 show them with side, plane and score, and a k/n count',
      f21 and 'H Dec midpoint (98.45)' in str(f21[0][2]) and 'H Dec 1 (98.29)' in str(f21[0][2]) and str(f21[0][-1]).endswith('/6')
      and f22 and 'H RA far midpoint (53.41)' in str(f22[0][6]) and str(f22[0][-1]).endswith('/6'), f'{f21[0] if f21 else f21} | {f22[0] if f22 else f22}')
bad21 = []
for n in [x for x in wbl.sheetnames if x.startswith('P') and x[1:].isdigit()]:
    for r in wbl[n].iter_rows(values_only=True):
        if r and r[0] == 'T21' and r[2] in ('RA', 'Dec', 'Equator'):
            sides = [r[c0:c0 + 18] for c0 in (3, 21) if len(r) >= c0 + 18]
            if not any(sd[17] is not None or (sd[9] is not None and sd[9] >= 50) for sd in sides if not (sd[12] and 'together' in sd[12])):
                bad21.append((n, r[1], r[2]))
e21 = [r[0] for r in wbl['FIELD 21'].iter_rows(min_row=4, values_only=True) if r and r[0] and str(r[-1]).startswith('0/')]
check('T21 filter (Eddie 15 Oct, revised): every line has a side with a midpoint hit or a ratio hit >= 50; FIELD 21 has no empty (0/n) row; '
      'FIELD 21 ratio lines all >= 50', not bad21 and not e21 and all(float(x.rsplit('(', 1)[1].rstrip(')')) >= 50 for r in wbl['FIELD 21'].iter_rows(min_row=4, values_only=True)
      for c in r[1:-1] if c for x in str(c).split('\n') if 'midpoint' not in x), f'{bad21[:3]} {e21[:3]}')
st = [r for r in wbl['THREADS'].iter_rows(values_only=True) for v in r if isinstance(v, str) and ('[T21' in v or '[T22' in v)]
check('THREADS and NUMBERS: no T21 / T22 (stars stay out)', not st and not any(isinstance(v, str) and ('T21' in v or 'T22' in v)
      for n in wbl.sheetnames if n.endswith('NUMBERS') for r in wbl[n].iter_rows(values_only=True) for v in r), '')

# Eddie 15 Oct 2026: SKY cells in T1 / T2 (S Jupiter -> S X, same plane), sky side in T21 (S Jupiter: S A – S B), tag 'same as sky'
print('\nTest 18 (Eddie 15 Oct): SKY cells in T1 / T2, sky side in T21, "same as sky" — Lingfield AW 14:35 2021')
t1 = [r for r in wbl['P03'].iter_rows(values_only=True) if r and r[0] == 'T1' and r[1] == 'H Jupiter → H Sun']
check('T1 P03 H Jupiter → H Sun, SKY Dec cell S Jupiter → S Sun (by hand from POSITIONS: Dec S Jupiter −14.389918, S Sun 5.028708; rates '
      '+0.0000426 / +0.0002664 per min): 19.418627, +5 min 19.419746, 12×φ golden +0.00222 (86.76), away, separating, exact 14:25 (9.9 min ago); '
      'natal Dec 2.609925 (φ^2) unchanged; no same as sky tag (φ^2 / 10×φ^2 against 12×φ / 120×φ)',
      len(t1) == 1 and t1[0][11] == 2.609925 and t1[0][13] == 'φ^2 (phi power)' and t1[0][30] == 19.418627 and t1[0][31] == 19.419746
      and t1[0][32] == '12×φ (golden)' and t1[0][34] == '+0.00222' and t1[0][35] == 86.76 and t1[0][36] == '<- away'
      and t1[0][39] == 'separating, exact 14:25 (9.9 min ago)' and (len(t1[0]) < 41 or t1[0][40] is None), str(t1[0][28:41] if t1 else t1))
t21s = [r for r in wbl['P11'].iter_rows(values_only=True) if r and r[0] == 'T21' and r[1] == 'Alphecca – Betelgeuse' and r[2] == 'RA']
check('T21 P11 Alphecca – Betelgeuse RA, sky side S Jupiter: S Alphecca – S Betelgeuse (by hand from POSITIONS: RA S Jupiter 325.797311, '
      'S Alphecca 233.677137, S Betelgeuse 88.791862): 92.120174 / 122.994551 (φ^10, 99.13, applying, exact 14:55) / 144.885275 (ninth 144.444, '
      '53.32), ratio 1.335153 4/3 +0.13650 % (20.61), applying, exact 23:43 (in 548.3 min), far side; horse side unchanged (1.333184 4/3, 91.22)',
      len(t21s) == 1 and t21s[0][9] == 1.333184 and t21s[0][12] == 91.22 and t21s[0][39] == 92.120174 and t21s[0][41] == 122.994551
      and t21s[0][42] == '→ φ^10 (phi power, 99.13) · applying, exact 14:55 (in 20.5 min)' and t21s[0][43] == 144.885275
      and t21s[0][45] == 1.335153 and t21s[0][46] == '4/3 · fourth · Perfect' and t21s[0][47] == '+0.13650%' and t21s[0][48] == 20.61
      and t21s[0][49] == 'applying, exact 23:43 (in 548.3 min)' and t21s[0][50] == 'far side', str(t21s[0][39:51] if t21s else t21s))
check('"same as sky" found by the rule on that line: horse ratio and sky ratio both on 4/3 (d(A, B) never counted, Eddie 15 Oct)',
      t21s and t21s[0][57] == 'same as sky — H: ratio 4/3 · fourth',
      str(t21s[0][57] if t21s else t21s))
n21 = [r for n in wbl.sheetnames if n.startswith('P') and n[1:].isdigit() for r in wbl[n].iter_rows(values_only=True)
       if r and r[0] == 'T21' and r[2] in ('RA', 'Dec', 'Equator')]
# 15 Oct 2026: 198 -> 244 lines (area A on ±0.02 absolute: more ratio hits >= 50); the listing rule itself is checked in test 17 (bad21)
check('T21 listing unchanged by the sky side: 244 lines (rule as before, area A ±0.02)', len(n21) == 244, f'{len(n21)} lines')
check('T21 "same as sky" never on d(A, B)', not any(len(r) > 57 and r[57] and 'd(A, B)' in r[57] for r in n21), '')

# Eddie 15 Oct 2026: every ratio table split into area A "whole + 3/2" (1, 3/2, 2, 3 ... 9 on ±0.02 absolute, or a midpoint hit) and
# area B "other" (every other interval); "no hit" at the bottom where every row is listed
print('\nTest 19 (Eddie 15 Oct): areas A / φ and √2 / B — Lingfield AW 14:35 2021 (every runner) and Ascot 14:30 2012')
AA, AP = set(families.AREA_A), set(families.AREA_P)    # 15 Oct 2026: third area "φ and √2" between A and B
iv = lambda t: str(t).split(' ')[0]                    # '4 · double octave · Perfect' -> '4'
iarea = lambda lab: 'A' if lab in AA else 'P' if lab in AP else 'B'
tarea = lambda t: 'A' if 'AREA A' in t else 'P' if 'AREA φ' in t else 'B' if 'AREA B' in t else 'rest'


def side_area(tgt, score, mid, rmin=0.0):
    """every area a cell / side has a hit in: the midpoint (A) and the ratio"""
    out = ['A'] if mid is not None else []
    if score is not None and score >= rmin:
        out.append(iarea(iv(tgt)))
    return out


def row_ar(areas):
    """-> (highest area A, φ and √2 (P), B, or 'rest'; hits in more than one area)"""
    areas = [a for x in areas for a in x]
    return next((a for a in ('A', 'P', 'B') if a in areas), 'rest'), len(set(areas)) > 1


def walk(ws, tids, row_area, title=lambda r: None):
    """-> (n data rows, [mismatches]): block from the title rows, area of each data row from its own cells"""
    cur, n, bad, seen, nm, tm = None, 0, [], set(), 0, 0
    for r in ws.iter_rows(values_only=True):
        if not r:
            continue
        t = title(r)
        if t is None:
            for v in r[:2]:
                if isinstance(v, str) and ': ' in v and ('AREA ' in v or 'NO HIT' in v or 'NO RATIO' in v) \
                        and any(v.startswith(x + ' ') for x in tids):    # this table's block titles only
                    t = v
        if t:
            if nm != tm:                               # the previous block title's "n carry hits in more than one area"
                bad.append((ws.title, 'multi count', cur, tm, nm))
            cur = tarea(t)
            m = re.search(r'\((\d+) carry hits in more than one area\)', t)
            nm, tm = 0, int(m.group(1)) if m else 0
            seen.add(cur)
            continue
        if r[0] in tids and isinstance(r[1], str):
            a = row_area(r)
            if a == 'skip':                            # a table's main title row
                continue
            n += 1
            a, mu = a
            nm += mu
            if a != cur:
                bad.append((ws.title, r[0], r[1], r[2] if len(r) > 2 else None, cur, a))
    if nm != tm:
        bad.append((ws.title, 'multi count', cur, tm, nm))
    return n, bad, seen


t1214 = lambda r: row_ar([side_area(r[c + 2], r[c + 5], None) for c in ((2, 11) if r[0] != 'T14' else (2,)) if len(r) > c + 5])
PL = ('RA', 'Dec', 'Equator')
pairs = lambda r: 'skip' if len(r) < 4 or r[3] not in PL else row_ar([side_area(r[11], r[13], r[21] if len(r) > 21 else None)])
t21 = lambda r: 'skip' if len(r) < 3 or r[2] not in PL else row_ar([side_area(r[c + 7], r[c + 9], r[c + 17], 50.0) for c in (3, 21)
                        if len(r) > c + 17 and not (r[c + 12] and 'together' in str(r[c + 12]))])
t22 = lambda r: 'skip' if len(r) < 3 or r[2] not in PL else row_ar([side_area(r[c + 5], r[c + 7], r[c + 14]) for c in (3, 18) if len(r) > c + 14])
res, tot = [], {}
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    pw = openpyxl.load_workbook(f.replace('_jupiter_tables.xlsx', '_pairs.xlsx'), read_only=True)
    for n in [x for x in w.sheetnames if x.startswith('P') and x[1:].isdigit()]:
        for tids, fn in ((('T12', 'T13', 'T14'), t1214), (('T19',), pairs), (('T21',), t21), (('T22',), t22)):
            k, b, _ = walk(w[n], tids, fn, title=(lambda r: r[1] if r[0] in ('T12', 'T13', 'T14') and isinstance(r[1], str) and 'rows' in r[1]
                                                    and ('AREA' in r[1] or 'NO HIT' in r[1]) else None) if 'T12' in tids else (lambda r: None))
            if 'T12' in tids:                          # T12-T14 data rows: the label rows (not the titles)
                k, b, _ = walk(w[n], tids, lambda r: fn(r) if not ('AREA' in r[1] or 'NO HIT' in r[1] or r[1].startswith('Jupiter return')) else 'skip',
                               title=lambda r: r[1] if r[0] in tids and isinstance(r[1], str) and ('AREA' in r[1] or 'NO HIT' in r[1]) else None)
            tot[tids[0]] = tot.get(tids[0], 0) + k
            res += b
        rr, cur = list(w[f'{n} RATIOS'].iter_rows(values_only=True)), None
        for x in rr:
            if isinstance(x[0], str) and x[0].startswith('AREA'):
                cur = tarea(x[0])
            elif x[1] in ('T12', 'T13', 'T14') and x[6]:
                tot['RATIOS'] = tot.get('RATIOS', 0) + 1
                if iarea(x[6]) != cur:
                    res.append((n + ' RATIOS', x[2], x[3], x[6], cur))
        k, b, _ = walk(pw[n + ' PAIRS'], ('PAIRS',), pairs)
        tot['PAIRS'] = tot.get('PAIRS', 0) + k
        res += b
    k, b, _ = walk(w['SKY JUPITER'], ('SKY PAIRS', 'SKY STARS'), pairs)
    tot['SKY'] = tot.get('SKY', 0) + k
    res += b
    for fs in ('FIELD 12', 'FIELD 13', 'FIELD 14', 'FIELD 21', 'FIELD 22'):
        cur = None
        for r in w[fs].iter_rows(min_row=3, values_only=True):
            if r and isinstance(r[0], str) and ('AREA' in r[0] or 'NO HIT' in r[0]) and ': ' in r[0]:
                cur = tarea(r[0])
                continue
            if not r or not r[0] or cur is None:
                continue
            for c in r[1:]:
                if not isinstance(c, str) or c.endswith('/6') or c.endswith('/1') or c.startswith('P'):
                    continue
                for line in c.split('\n'):
                    tot[fs] = tot.get(fs, 0) + 1
                    if fs in ('FIELD 21', 'FIELD 22'):
                        a = 'A' if 'midpoint' in line else iarea(line.split(' ')[2])
                    else:
                        a = 'rest' if 'outside' in line else iarea(line.split(' ')[0])
                    if a != cur:
                        res.append((fs, r[0], line, cur, a))
check('every area A row has an A interval (1, 3/2, 2, 3 ... 9) or a midpoint hit, every φ and √2 row a φ / √2 interval and no A hit, '
      'every area B row a B interval (and no A or φ / √2 hit), every no-hit row neither; block titles count the rows with hits in more than one area; '
      '(15 Oct: third area φ and √2) (T12-T14, T19, T21 counted sides >= 50, T22, SKY PAIRS, SKY STARS, P## PAIRS, P## RATIOS, FIELD 12-14 / 21 / 22 cells)',
      not res and all(tot.values()), f'{tot}; mismatches {res[:5]}')

# Eddie 15 Oct 2026: SKY PAIRS body – royal rows
print('\nTest 20 (Eddie 15 Oct): SKY PAIRS body – royal — Lingfield AW 14:35 2021')
wbl = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', read_only=True)
hf = [r for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'SKY PAIRS' and r[2] == 'S Haumea – S Fomalhaut' and r[3] == 'Dec']
check('SKY PAIRS body – royal S Haumea – S Fomalhaut Dec (by hand from POSITIONS: Dec S Jupiter −14.389918, S Haumea 16.069041, '
      'S Fomalhaut −29.623914): 30.458960 / 15.233996 / 45.692955, ratio 1.999407 on 2 (offset −0.00059, (10 (0.02 − 0.000593) / 0.02)² = 94.16), '
      'between, in the area A block',
      len(hf) == 1 and hf[0][1] == 'body – royal' and abs(hf[0][4] - 30.45896) < 2e-6 and hf[0][6] == 15.233996 and hf[0][8] == 45.692955
      and hf[0][10] == 1.999407 and hf[0][11] == '2 · octave · Perfect' and hf[0][12] == '-0.00059' and hf[0][13] == 94.16 and hf[0][15] == 'between'
      and any(x[2] == 'S Haumea – S Fomalhaut' and x[3] == 'Dec' for x in blocks(wbl['SKY JUPITER'], 'SKY PAIRS').get('A', [])),
      str(hf[0][:16] if hf else hf))

# Eddie 15 Oct 2026: sky side on T19 rows, S Jupiter: S X – S Y; '—' for H X – J X and where there is none; 'same as sky' incl. d(X, Y)
print('\nTest 21 (Eddie 15 Oct): T19 sky side and "same as sky" — Lingfield AW 14:35 2021 P07')
cj = [r for r in wbl['P07'].iter_rows(values_only=True) if r and r[0] == 'T19' and r[2] == 'J Chiron – J Juno' and r[3] == 'RA']
check('T19 P07 J Chiron – J Juno RA sky side S Jupiter: S Chiron – S Juno (by hand from POSITIONS: RA S Jupiter 325.797311, S Chiron 7.172849, '
      'S Juno 263.624221): 41.375538 (silver 41.4, 60.65) / 62.173090 / 103.548628 (64×φ, 68.66), ratio 1.502653 on 3/2 (+0.00265, '
      '(10 (0.02 − 0.002653) / 0.02)² = 75.23), between, area A; natal side unchanged (76.319284 / 115.485225, 1.513185 3/2, 11.61)',
      len(cj) == 1 and cj[0][10] == 1.513185 and cj[0][13] == 11.61 and cj[0][22] == 41.375538 and cj[0][23].startswith('→ 41.4 (silver, 60.65)')
      and cj[0][24] == 62.17309 and cj[0][26] == 103.548628 and cj[0][27].startswith('→ 64×φ (golden, 68.66)') and cj[0][28] == 1.502653
      and cj[0][29] == '3/2 · fifth · Perfect' and cj[0][30] == '+0.00265' and cj[0][31] == 75.23 and cj[0][33] == 'between' and cj[0][40] == 'A',
      str(cj[0][22:42] if cj else cj))
check('"same as sky" found by the rule on that row: natal ratio 1.513185 and sky ratio 1.502653 both on 3/2',
      cj and cj[0][41] == 'same as sky — ratio 3/2 · fifth', str(cj[0][41] if cj else cj))
t19l = [r for n in wbl.sheetnames if n.startswith('P') and n[1:].isdigit() for r in wbl[n].iter_rows(values_only=True)
        if r and r[0] == 'T19' and len(r) > 3 and r[3] in ('RA', 'Dec', 'Equator')]
RY = ('Aldebaran', 'Regulus', 'Antares', 'Fomalhaut')
royleg = [r for r in t19l if r[41] and any((q.startswith('d(S Jup, X)') and r[2].split(' – ')[0][2:] in RY)
                                           or (q.startswith('d(S Jup, Y)') and r[2].split(' – ')[1][2:] in RY) for q in r[41][14:].split('; '))]
tog = [r for r in t19l if r[22] != '—' and r[34] and 'together' in r[34]]
gg = [r for r in wbl['P05'].iter_rows(values_only=True) if r and r[0] == 'T19' and r[2] == 'H Gonggong – H Regulus' and r[3] == 'Equator']
check('T19 "same as sky" (Eddie 15 Oct, revised): never on d(S Jupiter, royal star) (P05 H Gonggong – H Regulus Equator keeps only its ratio 5/4); '
      'a sky side with "X, Y together" plain: no area, no tag (Lingfield: 8 such sides, P03 H Orcus – H Transpluto RA among them)',
      not royleg and len(gg) == 1 and gg[0][41] == 'same as sky — ratio 5/4 · major third' and len(tog) == 8
      and all(r[40] is None and r[41] is None for r in tog) and any(r[2] == 'H Orcus – H Transpluto' and r[3] == 'RA' for r in tog),
      f'{len(royleg)} royal-leg tags, {len(tog)} together sides, {gg[0][41] if gg else gg}')
check('T19 sky side: every H–J row "—"; every Equator sky side has S Jupiter, S X, S Y straddling (else "—"); the listing unchanged (1365 rows)',
      len(t19l) == 1365 and all(r[22] == '—' for r in t19l if r[1] == 'H–J') and all(r[22] is not None for r in t19l), f'{len(t19l)} rows')
# Eddie 16 Oct 2026: timing on the SKY JUPITER "SKY" block, best and scaled hit per plane
print('\nTest 22 (Eddie 16 Oct): SKY block timing — Lingfield AW 14:35 2021')
wbl = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', read_only=True)
sm = [r for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'SKY' and r[1] == 'S Jupiter → S Mercury']
check('SKY S Jupiter → S Mercury (by hand from POSITIONS: Dec S Jupiter −14.389918 (+0.0000425872 /min), S Mercury −3.326422 '
      '(+0.000505303 /min), off 14:35): Dec 11.063496 → 11.065810 at +5, φ^5 11.090170, rate 0.00046272 /min -> applying, exact 15:32 '
      '(in 57.6 min); its scaled x10 10×φ^5 is a repeat (same family and digits): one timing only (Eddie 16 Oct); RA 32.268875 -> 32.27372, '
      'scaled /10 2×φ (20φ 32.360680, a different number) reached in 94.7 min -> 16:09; RA best (outside) no timing. Timing inside each '
      'plane block, after its scaled column (16 Oct): RA cols 3-13, Dec cols 14-24',
      len(sm) == 1 and sm[0][13] == 11.063496 and sm[0][15] == 'φ^5 (phi power)' and sm[0][22] == 'applying, exact 15:32 (in 57.6 min)'
      and sm[0][23] is None and sm[0][21].startswith('x10: 10×φ^5') and sm[0][11] is None
      and sm[0][12] == 'applying, exact 16:09 (in 94.7 min)' and sm[0][10].startswith('/10: 2×φ'),
      str(sm[0][2:24] if sm else sm))
skr = [list(r) + [None] * 30 for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'SKY' and r[1] != 'S Jupiter → sky points']
check('SKY block: a best timing exactly where the best hit (score) is; a scaled timing only with a scaled hit, and a missing one only '
      'where the scaled hit repeats the best (then the best timing is there), per plane (RA, Dec)',
      skr and all((r[c + 5] is not None) == (r[c + 9] is not None) and (r[c + 10] is None or r[c + 8] is not None)
                  and (r[c + 8] is None or r[c + 10] is not None or r[c + 9] is not None)
                  for r in skr for c in (2, 13)) and sum(1 for r in skr for c in (2, 13) if r[c + 8] and r[c + 10] is None) > 0, f'{len(skr)} rows')

# Eddie 16 Oct 2026: no together side shows a score (T19 sky side, T21 / T21R sides, SKY ROYAL rows)
tsc = []
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    for n in w.sheetnames:
        for r in w[n].iter_rows(values_only=True):
            if not r or r[0] not in ('T19', 'T21', 'T21R', 'SKY ROYAL'):
                continue
            sides = ([(16, 13, 19)] if r[0] == 'SKY ROYAL' else [(34, 31, 37)] if r[0] == 'T19' else [(c + 12, c + 9, c + 15) for c in (3, 21, 39)])
            for nc, sc_, m0 in sides:
                if len(r) > m0 + 2 and r[nc] and 'together' in str(r[nc]) and any(x is not None for x in (r[sc_], r[m0], r[m0 + 1], r[m0 + 2])):
                    tsc.append((n, r[0], r[1], r[2], r[3] if len(r) > 3 else None))
check('no together side shows a score (Eddie 16 Oct): T19 sky sides (e.g. Lingfield P07 J Orcus – J Gonggong Dec, was 36.06), T21 / T21R '
      'sides, SKY ROYAL rows; Lingfield and Ascot', not tsc, str(tsc[:4]))
p7 = [r for r in wbl['P07'].iter_rows(values_only=True) if r and r[0] == 'T19' and r[2] == 'J Orcus – J Gonggong' and r[3] == 'Dec']
check('T19 P07 J Orcus – J Gonggong Dec sky side together: values kept (ratio 1.007991), no score', len(p7) == 1 and p7[0][28] == 1.007991
      and p7[0][31] is None and 'together' in p7[0][34], str(p7[0][28:35] if p7 else p7))

# Eddie 16 Oct 2026: royal-star-only tables T21R, T22R, SKY ROYAL, FIELD 21R / 22R
print('\nTest 23 (Eddie 16 Oct): royal-star-only tables — Lingfield AW 14:35 2021 (every runner) and Ascot 14:30 2012')
RY = ('Aldebaran', 'Regulus', 'Antares', 'Fomalhaut')
bad, n21r, n22r = [], 0, 0
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    for n in [x for x in w.sheetnames if x.startswith('P') and x[1:].isdigit()]:
        rows = [r for r in w[n].iter_rows(values_only=True) if r and len(r) > 2 and r[2] in PL]
        for t in ('T21', 'T22'):
            full = {(r[1], r[2]): r[1:] for r in rows if r[0] == t}
            roy = {(r[1], r[2]): r[1:] for r in rows if r[0] == t + 'R'}
            want = {k for k in full if all(x in RY for x in k[0].split(' – '))}
            if t == 'T22' and set(roy) != want:
                bad.append((n, t, 'set'))
            if t == 'T21' and (not want <= set(roy) or any(k[0] not in [f'{a} – {b}' for i, a in enumerate(RY) for b in RY[i + 1:]] for k in roy)):
                bad.append((n, t, 'set'))
            bad += [(n, t, k) for k in want if roy.get(k) != full[k]]
            n21r += len(roy) if t == 'T21' else 0
            n22r += len(roy) if t == 'T22' else 0
    sk = [r for r in w['SKY JUPITER'].iter_rows(values_only=True) if r and len(r) > 3 and r[3] in PL]
    spb = {(r[2], r[3]): r[1:22] for r in sk if r[0] == 'SKY PAIRS' and r[1] == 'body – royal'}
    sr = {(r[2], r[3]): r[1:22] for r in sk if r[0] == 'SKY ROYAL'}
    bad += [('SKY ROYAL', k) for k in spb if sr.get(k) != spb[k]]
    if not all(r[1] in ('royal – royal', 'body – royal') for r in sk if r[0] == 'SKY ROYAL'):
        bad.append('SKY ROYAL blocks')
    for fs in ('FIELD 21R', 'FIELD 22R'):
        if fs not in w.sheetnames:
            bad.append(fs)
wa = openpyxl.load_workbook('reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx', read_only=True)
tg = [r for r in wa['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'SKY ROYAL' and len(r) > 16 and r[16] and 'together' in r[16]]
check('SKY ROYAL "X, Y together" rows plain with no score (Eddie 16 Oct): Ascot S Transpluto – S Regulus RA 0.929582 (unison, was 24.22) '
      'and Dec, values kept, no ratio score, no midpoint scores',
      len(tg) == 2 and any(r[3] == 'RA' and r[8] == 0.929582 and r[10] is not None for r in tg)
      and all(r[13] is None and all(x is None for x in r[19:22]) for r in tg), str([r[2:4] + r[13:14] for r in tg]))
check('T21R / T22R lines = the royal lines of T21 / T22 with the same values (T21R: every one of the six royal pairs, T21\'s royal lines '
      'among them; T22R exactly T22\'s royal lines); SKY ROYAL holds the SKY PAIRS body – royal rows unchanged; FIELD 21R / 22R present',
      bool(not bad and n21r and n22r), f"T21R {n21r}, T22R {n22r} lines; {bad[:5]}")
print(f'\n{sum(RES)}/{len(RES)} passed')
sys.exit(0 if all(RES) else 1)
