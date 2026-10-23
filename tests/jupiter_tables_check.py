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
COL = {'RA': 2, 'Dec': 10}                                # 0-based column of each plane's value (RA, Dec; 8 columns each since the scaled column went, 16 Oct 2026)
RES = []


def check(name, ok, detail):
    RES.append(ok); print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")


import time
T0, NBUILT = time.time() - 1, [0]


def build(inp):
    NBUILT[0] += 1
    r = subprocess.run([sys.executable, 'tools/jupiter_tables.py', inp, '--full'], capture_output=True, text=True)   # every sheet (19 Oct 2026)
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
# 16 Oct 2026 (Eddie): values never scaled - retired 'J Jup→H Uranus Dec 14.141031 /10: 1.414103 → 1.414 (99.12) [T4, scaled]' and the
# repeat rule; the same value now shows its hit as it is on the √2 target 14.14 (found by the rule, not tuned)
check('cells list hits >= 50 only, on the value as it is (no scaled lines): J Jup→H Uranus Dec 14.141031 → 14.14 (96.90) [T4]; last line "+ n weaker"',
      df[-1].startswith('+ ') and df[-1].endswith(' weaker (see T-tables)') and not any('scaled' in x or 'x10:' in x or '/10:' in x for x in df)
      and 'J Jup→H Uranus Dec 14.141031 → 14.14 (96.90) [T4]' in df
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
      len(t1) == 1 and t1[0][10] == 2.609925 and t1[0][12] == 'φ^2 (phi power)' and t1[0][27] == 19.418627 and t1[0][28] == 19.419746
      and t1[0][29] == '12×φ (golden)' and t1[0][31] == '+0.00222' and t1[0][32] == 86.76 and t1[0][33] == '<- away'
      and t1[0][35] == 'separating, exact 14:25 (9.9 min ago)' and (len(t1[0]) < 37 or t1[0][36] is None), str(t1[0][26:37] if t1 else t1))
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


t1214 = lambda r: row_ar([side_area(r[c + 2], r[c + 5], None) for c in ((2, 10) if r[0] != 'T14' else (2,)) if len(r) > c + 5])
PL = ('RA', 'Dec', 'Equator')
pairs = lambda r: 'skip' if len(r) < 4 or r[3] not in PL else row_ar([side_area(r[11], r[13], r[21] if len(r) > 21 else None)])
t21 = lambda r: 'skip' if len(r) < 3 or r[2] not in PL else row_ar([side_area(r[c + 7], r[c + 9], r[c + 17], 50.0) for c in (3, 21)
                        if len(r) > c + 17 and not (r[c + 12] and 'together' in str(r[c + 12]))])
t22 = lambda r: 'skip' if len(r) < 3 or r[2] not in PL else row_ar([side_area(r[c + 5], r[c + 7], r[c + 14]) for c in (3, 18) if len(r) > c + 14])
build('reference/classic/race_batch_20120619_ascot_1430.xlsx')     # 19 Oct 2026: Ascot rebuilt here (the checks below had read an older build)
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
# Eddie 16 Oct 2026: timing on the SKY JUPITER "SKY" block (the scaled timing retired the same day: values are never scaled)
print('\nTest 22 (Eddie 16 Oct): SKY block timing — Lingfield AW 14:35 2021')
wbl = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', read_only=True)
sm = [r for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'SKY' and r[1] == 'S Jupiter → S Mercury']
check('SKY S Jupiter → S Mercury (by hand from POSITIONS: Dec S Jupiter −14.389918 (+0.0000425872 /min), S Mercury −3.326422 '
      '(+0.000505303 /min), off 14:35): Dec 11.063496 → 11.065810 at +5, φ^5 11.090170, rate 0.00046272 /min -> applying, exact 15:32 '
      '(in 57.6 min); RA 32.268875 outside every family (20×φ 32.360680 outside ±0.0324): no timing. Timing inside each plane block, '
      'after its cells: RA cols 3-11, Dec cols 12-20. (16 Oct 2026: the RA /10 2×φ scaled hit, 16:09, and the scaled timing column retired '
      '- values are never scaled)',
      len(sm) == 1 and sm[0][11] == 11.063496 and sm[0][13] == 'φ^5 (phi power)' and sm[0][19] == 'applying, exact 15:32 (in 57.6 min)'
      and sm[0][2] == 32.268875 and sm[0][4].startswith('20×φ (golden) — outside') and sm[0][7] is None and sm[0][10] is None,
      str(sm[0][2:21] if sm else sm))
skr = [list(r) + [None] * 30 for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'SKY' and r[1] != 'S Jupiter → sky points']
check('SKY block: a timing exactly where the best hit (score) is, per plane (RA, Dec); no scaled column',
      skr and all((r[c + 5] is not None) == (r[c + 8] is not None) for r in skr for c in (2, 11))
      and not any(isinstance(x, str) and ('x10:' in x or '/10:' in x) for r in skr for x in r), f'{len(skr)} rows')

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

# Eddie 16 Oct 2026: no value scaling anywhere (no scaled column, scaled timing, scaled THREADS / NUMBERS / TIMELINE hits, 'widens' note)
scl = []
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    for n in w.sheetnames:
        for r in w[n].iter_rows(values_only=True):
            for x in r or ():
                if isinstance(x, str) and ('x10:' in x or '/10:' in x or 'scaled x10 / /10' == x or '[scaled]' in x or ', scaled]' in x
                                           or 'widens 10x' in x or x.startswith('distance (scaled') or x.startswith('ratio (scaled') or x.startswith('timing (scaled')):
                    scl.append((n, x[:60]))
check('no value scaling anywhere in the Lingfield and Ascot workbooks (Eddie 16 Oct): no scaled column or timing, no scaled THREADS / NUMBERS / '
      'TIMELINE hit, no "widens 10x" note', not scl, str(scl[:4]))

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
# Eddie 16 Oct 2026: TIMELINE on the SKY JUPITER sheet
print('\nTest 24 (Eddie 16 Oct): TIMELINE — Lingfield AW 14:35 2021 and Ascot 14:30 2012')
import datetime


def tl_check(f, off):
    """-> (events, [problems]): window, order, and each event's exact time = its source cell (a timing cell on the sheet with the same text;
    SKY cells outside at the off have none and are recomputed from POSITIONS, linear off -> +5 min)"""
    w = openpyxl.load_workbook(f, read_only=True)
    allr = [r for r in w['SKY JUPITER'].iter_rows(values_only=True) if r]
    pos = {r[3]: r for r in w['POSITIONS'].iter_rows(values_only=True) if r and r[0] == 'SKY'}
    tl = [r for r in allr if r[0] == 'TIMELINE' and isinstance(r[2], (int, float))]
    ev = [r for r in tl if r[4]]
    bad, last = [], -1e9
    for r in tl:
        if r[2] < last:
            bad.append(('order', r[1:5]))
        last = r[2]
    for r in ev:
        if not -30 <= r[2] <= 60:
            bad.append(('window', r[1:5]))
        txt = (f'applying, exact {r[1]} (in {r[2]:.1f} min)' if r[2] >= 0 else f'separating, exact {r[1]} ({-r[2]:.1f} min ago)')
        names = [x for x in re.split(r'S Jupiter: |S Jupiter → | – ', r[4]) if x]
        src = 'SKY EQ' if r[3] == 'SKY EQ' else r[3]
        cand = [x for x in allr if x[0] == src and all(any(isinstance(c, str) and nm in c for c in x[1:3]) for nm in names)]
        if any(isinstance(c, str) and txt in c for x in cand for c in x):
            continue
        if r[3] == 'SKY' and r[12] and 'outside at the off' in r[12]:
            b = r[4].split('→ S ')[1]
            p0, q0 = pos['Jupiter'], pos[b]
            ix = 5 if r[5] == 'RA' else 6
            dd = lambda m: (abs((p0[5] + m * p0[7]) - (q0[5] + m * q0[7])) % 360) if ix == 5 else abs((p0[6] + m * p0[8]) - (q0[6] + m * q0[8]))
            d = lambda m: min(dd(m), 360 - dd(m)) if ix == 5 else dd(m)
            t = (r[8] - d(0)) / ((d(5) - d(0)) / 5)
            clock = (off + datetime.timedelta(minutes=t)).strftime('%H:%M')
            if abs(t - r[2]) < 0.06 and clock == r[1]:
                continue
        bad.append(('source', r[1:9]))
    return ev, bad


bad, n = [], 0
for f, off in (('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', datetime.datetime(2021, 4, 2, 14, 35)),
               ('reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx', datetime.datetime(2012, 6, 19, 14, 30))):
    ev, b = tl_check(f, off)
    n += len(ev); bad += b
check('TIMELINE: every event inside the off − 30 / + 60 min, rows (and the OFF / +5 MIN markers) in time order, each exact time = its source '
      'cell on the sheet (SKY outside at the off: recomputed from POSITIONS)', not bad and n > 0, f'{n} events; {bad[:4]}')
wbl = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', read_only=True)
tm = [r for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'TIMELINE' and r[4] == 'S Jupiter → S Moon' and r[5] == 'Dec']
check('TIMELINE S Jupiter → S Moon Dec (by hand from POSITIONS: Dec S Jupiter −14.389918 (+0.0000425872 /min), S Moon −24.052038 '
      '(−0.000983196 /min)): d 9.662120 growing 0.00102578 /min, nearest 6×φ 9.708204 outside at the off, reached in 44.9 min -> 15:19, '
      'applying, no score',
      len(tm) == 1 and tm[0][1] == '15:19' and tm[0][2] == 44.9 and tm[0][7] == '6×φ (golden)' and tm[0][9] == 9.66212 and tm[0][10] is None
      and tm[0][11] == 'applying' and 'outside at the off' in tm[0][12], str(tm[0] if tm else tm))
mk = [r for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'TIMELINE' and isinstance(r[3], str) and r[3].startswith('———')]
check('TIMELINE markers: OFF 14:35 (0 min) and OFF + 5 MIN 14:40', [(r[1], r[2]) for r in mk] == [('14:35', 0), ('14:40', 5)], str([r[1:4] for r in mk]))
# Eddie 16 Oct 2026: TIMELINE H / TIMELINE J on every runner sheet
print('\nTest 25 (Eddie 16 Oct): TIMELINE H / J — Lingfield AW 14:35 2021 (every runner) and Ascot 14:30 2012')


def rtl_check(f, off):
    """every runner timeline row recomputed from POSITIONS (linear off -> +5 min, the larger / smaller ratio fixed at the off): exact
    time and clock, window, order; 'H + J' exactly on events using both charts -> (n events, [problems])"""
    w = openpyxl.load_workbook(f, read_only=True)
    posr = list(w['POSITIONS'].iter_rows(values_only=True))
    sky = {r[3]: r for r in posr if r and r[0] == 'SKY'}
    n, bad = 0, []
    for P in [x for x in w.sheetnames if x.startswith('P') and x[1:].isdigit()]:
        nat = {(r[2], r[3]): r for r in posr if r and r[0] == P}

        def pos(pt, m):
            c, b = pt.split(' ', 1)
            if c == 'S':
                r = sky[b]
                return ((r[5] + m * r[7]) % 360, r[6] + m * r[8]) if r[7] is not None else None
            r = nat[(c, b)]
            return r[5], r[6]

        def d(a, b, pl, m):
            if b.endswith(' equator'):
                return abs(pos(a, m)[1])
            p, q = pos(a, m), pos(b, m)
            if pl == 'RA':
                x = abs(p[0] - q[0]) % 360
                return min(x, 360 - x)
            return abs(p[1] - q[1]) if pl == 'Dec' else abs(abs(p[1]) - abs(q[1]))

        def lr(a, b, pl):                              # larger / smaller of two distances (pairs of points), orientation fixed at the off
            x0, y0, x5, y5 = d(*a, pl, 0), d(*b, pl, 0), d(*a, pl, 5), d(*b, pl, 5)
            return (x0 / y0, x5 / y5) if x0 >= y0 else (y0 / x0, y5 / x5)

        rows = [r for r in w[P].iter_rows(values_only=True) if r and r[0] in ('TIMELINE H', 'TIMELINE J') and isinstance(r[2], (int, float))]
        for C in 'HJ':
            last = -1e9
            for r in [x for x in rows if x[0] == f'TIMELINE {C}']:
                if r[2] < last:
                    bad.append((P, 'order', r[1:5]))
                last = r[2]
                if not r[4]:
                    continue
                n += 1
                rel, pl, kind, tv = r[4], r[5], r[6], r[8]
                f_ = 1.0                                   # values never scaled (16 Oct 2026)
                try:
                    if kind.startswith('distance'):
                        a, b = rel.split(' → ')
                        v0, v5 = d(a, b, pl, 0) * f_, d(a, b, pl, 5) * f_
                    elif kind == 'crossing':
                        x, rest = rel[len('Jupiter–'):].split(' ', 1)
                        ca, cb = rest[0], rest.split('= ')[1][0]
                        v0, v5 = (d(f'{ca} Jupiter', f'{ca} {x}', 'RA', m) - d(f'{cb} Jupiter', f'{cb} {x}', 'Dec', m) for m in (0, 5))
                    elif r[3] in ('T12', 'T13'):
                        nn, dd = rel.split(' / ')
                        v0, v5 = lr(tuple(nn.split('–')), tuple(dd.split('–')), pl)
                        v0, v5 = v0 * f_, v5 * f_
                    elif r[3] == 'T14':
                        c = rel.split(' / ')[1].split(' ')[1]
                        v0, v5 = lr(('S Jupiter', 'S equator'), (f'{c} Jupiter', f'{c} equator'), 'Dec')
                        v0, v5 = v0 * f_, v5 * f_
                    elif r[3] == 'T22':
                        st, rest = rel.split(': ', 1)
                        c = rest.split('d(star, ')[2][0]
                        v0, v5 = lr((f'S {st}', 'S Jupiter'), (f'S {st}', f'{c} Jupiter'), pl)
                    elif ': ' in rel:                        # T17 / T18 / T19: S Jupiter on X, Y
                        jup, xy = rel.split(': ')
                        x, y = re.split(' – | = ', xy)
                        v0, v5 = lr((jup, x), (jup, y), pl)
                    else:                                  # T10 / T11 / T20: e1 / e2 | middle (RA: arc distance)
                        ends, mid = rel.split(' | ')
                        e1, e2 = ends.split(' / ')
                        v0, v5 = lr((mid, e1), (mid, e2), pl)
                except Exception as e:
                    bad.append((P, 'parse', rel, repr(e)))
                    continue
                t = (tv - v0) / ((v5 - v0) / 5)
                clock = (off + datetime.timedelta(minutes=t)).strftime('%H:%M')
                if abs(t - r[2]) > 0.06 or clock != r[1] or not -30 <= r[2] <= 60 or (r[11] == 'applying') != (t >= 0):
                    bad.append((P, rel, pl, r[3], round(t, 3), r[2], clock, r[1]))
                pts = re.findall(r'\b([SHJ]) [A-Z]', rel)
                both = {'H', 'J'} <= set(pts) or (r[3] == 'T16' and {rel.split(' ')[1][0], rel.split('= ')[1][0]} == {'H', 'J'})
                if both != bool(r[12] and 'H + J' in r[12]):
                    bad.append((P, 'H + J', rel))
        hj = [x[1:5] for x in rows if x[12] and 'H + J' in x[12]]
        if sorted(x for x in hj if True) != sorted(hj) or len([x for x in rows if x[0] == 'TIMELINE H' and x[12] and 'H + J' in x[12]]) != \
                len([x for x in rows if x[0] == 'TIMELINE J' and x[12] and 'H + J' in x[12]]):
            bad.append((P, 'H + J in both timelines'))
    return n, bad


bad, n = [], 0
for f, off in (('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', datetime.datetime(2021, 4, 2, 14, 35)),
               ('reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx', datetime.datetime(2012, 6, 19, 14, 30))):
    k, b = rtl_check(f, off)
    n += k; bad += b
check('TIMELINE H / J: every event recomputed from POSITIONS (distance, ratio, crossing, midpoint unison; linear off -> +5 min) gives the '
      'same exact time and clock, inside −30 / +60, applying / separating right, rows and markers in time order, "H + J" exactly on events '
      'using both charts and in both timelines', not bad and n > 0, f'{n} events; {bad[:4]}')
w5 = [r for r in wbl['P05'].iter_rows(values_only=True) if r and r[0] in ('TIMELINE H', 'TIMELINE J') and r[4]]
hn = [r for r in w5 if r[0] == 'TIMELINE H' and r[4] == 'S Jupiter → H Neptune' and r[5] == 'RA']
jv = [r for r in w5 if r[0] == 'TIMELINE J' and r[4] == 'S Jupiter → J Venus' and r[5] == 'Dec']
check('TIMELINE H P05 S Jupiter → H Neptune RA (by hand from POSITIONS: RA S Jupiter 325.797311 (+0.000130972 /min), H Neptune 343.738939): '
      '17.941628 shrinking 0.000130972 /min, φ^6 17.944272 passed 20.2 min before the off -> separating, exact 14:14 (94.19), also T19',
      len(hn) == 1 and hn[0][1] == '14:14' and hn[0][2] == -20.2 and hn[0][7] == 'φ^6 (phi power)' and hn[0][9] == 17.941628
      and hn[0][10] == 94.19 and hn[0][11] == 'separating' and 'also T19' in hn[0][12], str(hn))
check('TIMELINE J P05 S Jupiter → J Venus Dec (by hand: Dec S Jupiter −14.389918 (+0.0000425872 /min), J Venus 18.610635): 33.000553 '
      'shrinking 0.0000425872 /min, 33 reached in 13.0 min -> applying, exact 14:47 (94.54), also T19',
      len(jv) == 1 and jv[0][1] == '14:47' and jv[0][2] == 13.0 and jv[0][7] == '33 (whole)' and jv[0][9] == 33.000553
      and jv[0][10] == 94.54 and jv[0][11] == 'applying' and 'also T19' in jv[0][12], str(jv))
# Eddie 16 Oct 2026: LONG TIMELINE (score >= 80, any time) and the sky equivalent cells on TIMELINE H / J and LONG TIMELINE H / J
print('\nTest 26 (Eddie 16 Oct): LONG TIMELINE and sky equivalents — Lingfield AW 14:35 2021 (every runner) and Ascot 14:30 2012')
import families as FAM


def long_check(f, off):
    """LONG rows: score >= 80, SEPARATING (t < 0, most recent first) then APPLYING (soonest first); every sky equivalent cell (TIMELINE H / J
    and LONG H / J) recomputed from POSITIONS: value, target (best family / interval or nearest outside), score, timing minutes"""
    w = openpyxl.load_workbook(f, read_only=True)
    posr = list(w['POSITIONS'].iter_rows(values_only=True))
    sky = {r[3]: r for r in posr if r and r[0] == 'SKY'}
    bad, nl, ns = [], 0, 0

    def pos(pt, m):
        r = sky[pt.split(' ', 1)[1]]
        return ((r[5] + m * r[7]) % 360, r[6] + m * r[8])

    def d(a, b, pl, m):
        p, q = pos(a, m), pos(b, m)
        if pl == 'RA':
            x = abs(p[0] - q[0]) % 360
            return min(x, 360 - x)
        return abs(p[1] - q[1]) if pl == 'Dec' else abs(abs(p[1]) - abs(q[1]))

    mins = lambda txt: (float(re.search(r'\(in ([\d.]+) min\)', txt).group(1)) if '(in ' in txt else
                        -float(re.search(r'\(([\d.]+) min ago\)', txt).group(1)))
    for n in [x for x in w.sheetnames if x == 'SKY JUPITER' or (x.startswith('P') and x[1:].isdigit())]:
        sec, last = None, None
        for r in w[n].iter_rows(values_only=True):
            if not r or not isinstance(r[0], str):
                continue
            if r[0].startswith('LONG TIMELINE') and isinstance(r[3], str) and r[3].startswith('———'):
                sec, last = r[3].split()[1].rstrip(':'), None
                continue
            ti = 13 if n == 'SKY JUPITER' else 19            # 'minutes from the off' (last column: after the sky cells on runner sheets)
            if r[0].startswith('LONG TIMELINE') and r[4] and len(r) > ti and isinstance(r[ti], (int, float)):
                nl += 1
                t = r[ti]
                key = (-r[10], -t if sec == 'SEPARATING' else t) if r[10] is not None else None   # 16 Oct: score first, ties by time
                if r[10] is None or r[10] < 80 or (sec == 'SEPARATING') != (t < 0) or r[11] != ('applying' if t >= 0 else 'separating') \
                        or (last is not None and key < last):
                    bad.append((n, 'long', r[1:6], sec))
                last = key
            if r[0] in ('TIMELINE H', 'TIMELINE J', 'LONG TIMELINE H', 'LONG TIMELINE J') and r[4] and len(r) > 14 and r[14] not in (None, '—'):
                ns += 1
                rel, pl, v, tgt, sc, tim = r[13], r[5], r[14], r[15], r[16], r[17]
                if ' RA = S Dec' in rel:
                    x = rel.split('–', 1)[1].split(' S RA')[0]
                    v0, v5 = (d('S Jupiter', f'S {x}', 'RA', m) - d('S Jupiter', f'S {x}', 'Dec', m) for m in (0, 5))
                    ev = None if abs(v0) >= 0.02 else 1
                    tv, lab = 0.0, 'crossing'
                elif ': ' in rel:
                    m_, xy = rel.split(': ')
                    x, y = re.split(' – | = ', xy)
                    a0, b0, a5, b5 = d(m_, x, pl, 0), d(m_, y, pl, 0), d(m_, x, pl, 5), d(m_, y, pl, 5)
                    v0, v5 = (a0 / b0, a5 / b5) if a0 >= b0 else (b0 / a0, b5 / a5)
                    ev = FAM.best(v0, None, 'ratio')
                    dd = ev or FAM.outside(v0, None, 'ratio')
                    tv, lab = (1.0, '1 · unison · midpoint') if tgt.startswith('1 · unison · midpoint') else (dd['tv'], dd['target'] + ' · ')
                else:
                    a, b = rel.split(' → ')
                    v0, v5 = d(a, b, pl, 0), d(a, b, pl, 5)
                    fp = pl if pl in ('RA', 'Dec') else None
                    ev = FAM.best(v0, fp, 'deg')
                    dd = ev or FAM.outside(v0, fp, 'deg')
                    tv, lab = dd['tv'], dd['target'] + ' ('
                tt = (tv - v0) / ((v5 - v0) / 5)
                ok = abs(v0 - v) < 2e-6 and tgt.startswith(lab) and abs(tt - mins(tim)) < 0.06 if abs(tt) < 50 * 525960 else 'more than 50' in tim
                if 'together' not in tgt and not tgt.startswith('1 · unison · midpoint') and (sc is None) != (ev is None):
                    ok = False
                if not ok:
                    bad.append((n, rel, pl, round(v0, 6), v, tgt[:30], round(tt, 1), tim))
    return nl, ns, bad


bad, nl, ns = [], 0, 0
for f, off in (('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', None),
               ('reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx', None)):
    a_, b_, c_ = long_check(f, off)
    nl += a_; ns += b_; bad += c_
check('LONG TIMELINE (sky and every runner H / J): every row scores >= 80, SEPARATING then APPLYING, each by score at the off (highest first; '
      'ties: separating most recent first, applying soonest first, Eddie 16 Oct); '
      'every sky equivalent cell (TIMELINE H / J, LONG H / J) = the same relationship recomputed from POSITIONS (value, target, score, timing)',
      not bad and nl > 0 and ns > 0, f'{nl} long rows, {ns} sky cells; {bad[:3]}')
bg = [r for r in wbl['P05'].iter_rows(values_only=True) if r and r[0] == 'LONG TIMELINE H' and r[4] == 'S Betelgeuse → H Jupiter' and r[5] == 'RA']
# 16 Oct 2026 (Eddie): real exact times from the ephemeris beyond 60 min; this event's linear estimate (+204.43 days) is not the real one
import sys as _s
_s.path.insert(0, 'rebuild_kit'); _s.path.insert(0, 'tools/jup2')
import swisseph as swe, celestial_bodies_swisseph as EN, motion as MO
swe.set_ephe_path(MO.EPHE)
JD0 = {'L': EN._to_jd_ut(EN._parse_time('2021-04-02 14:35', 'Europe/London'))}
SITE = MO.off_and_site('lingfield_aw_1435_20210402', 'TRANS', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', None, None)[1]
b0 = EN.bodies_at(JD0['L'], *SITE, False)
scan = [abs(199.7323286437921 - (88.79186212954453 + EN.bodies_at(JD0['L'] + dd, *SITE, False)['Betelgeuse_B']['ra'] - b0['Betelgeuse_B']['ra']))
        for dd in range(-366, 367)]
# 22 Oct 2026 (Eddie, LONG >= 90): this event (86.51) is no longer listed; the ephemeris scan below still holds (it was "not within 1 year")
check('LONG TIMELINE H P05 S Betelgeuse → H Jupiter RA (by hand from POSITIONS: H Jupiter 199.732329, S Betelgeuse 88.791862): 110.940467 at the '
      'off, 86.51 on 10×φ^5 110.901699 - under 90, so not in LONG TIMELINE H since 22 Oct 2026 (was "not within 1 year": the ephemeris, '
      'Betelgeuse daily ±1 year, keeps the distance between 110.933 and 110.945)',
      len(bg) == 0 and min(scan) > 110.9017 + 0.03 and abs(abs(199.7323286437921 - 88.79186212954453) - 110.940467) < 1e-6
      and abs((10 * (0.005 * 10 * ((1 + 5 ** 0.5) / 2) ** 5 - abs(110.940467 - 10 * ((1 + 5 ** 0.5) / 2) ** 5)) / (0.005 * 10 * ((1 + 5 ** 0.5) / 2) ** 5)) ** 2 - 86.51) < 0.01,
      f'{bg[:1]}; scan {min(scan):.6f}..{max(scan):.6f}')
pr = [r for r in wbl['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] == 'LONG TIMELINE' and r[4] == 'S Jupiter: S Pallas – S Rahu' and r[5] == 'Dec']
skyp = {r[3]: r for r in wbl['POSITIONS'].iter_rows(values_only=True) if r and r[0] == 'SKY'}


def dec_at(b, m):
    eb = b + '_B' if skyp[b][4] == 'star' else b
    return skyp[b][6] + EN.bodies_at(JD0['L'] + m / 1440.0, *SITE, False)[eb]['dec'] - b0[eb]['dec']


qv = lambda m: abs(dec_at('Jupiter', m) - dec_at('Rahu', m)) / abs(dec_at('Jupiter', m) - dec_at('Pallas', m))   # larger / smaller at the off
check('LONG TIMELINE (sky) S Jupiter: S Pallas – S Rahu Dec on 2 (93.55): real exact 11:32 (−182.8 min) vs linear 11:31 (−183.4 min); direct '
      'ephemeris lookup: d(S Jup, S Rahu) / d(S Jup, S Pallas) (larger / smaller) crosses 2 between one minute before and one minute after the found time',
      len(pr) == 1 and pr[0][1] == '11:32' and pr[0][13] == -182.8 and pr[0][14] == '11:31 (-183.4 min)'
      and (qv(pr[0][13] - 1) - 2) * (qv(pr[0][13] + 1) - 2) < 0, f"{pr[0][:15] if pr else pr}; {qv(-183.8):.7f} {qv(-181.8):.7f}")
dash = [r for r in wbl['P05'].iter_rows(values_only=True) if r and r[0] in ('TIMELINE H', 'LONG TIMELINE H') and r[3] in ('T12', 'T13', 'T22') and r[6] == 'ratio']
check('sky equivalent "—" where two points become one (T12 / T13 both Jupiters, T22 star to S Jupiter and H Jupiter)',
      dash and all(r[14] == '—' for r in dash), str([r[3:6] + r[13:15] for r in dash][:3]))
# Eddie 16 Oct 2026: T23 = H / J, S / H, S / J ratios of the T1, T2 and SKY distances, after T2; FIELD 23 (H / J)
T23N = ('H / J', 'S / H', 'S / J')


def t23_rows(ws):
    """{(X, plane, ratio): cells (value, +5, interval, group, offset, score, arrow, also, area, timing)} and the T12 cells by (X, plane, 'S / C')"""
    t23, t12, seen = {}, {}, []
    for r in ws.iter_rows(values_only=True):
        if not r or not r[1]:
            continue
        if r[0] == 'T23' and r[1] != 'X' and not str(r[1]).startswith('T23 ratios'):
            seen.append(r[1])
            for i, pl in enumerate(('RA', 'Dec')):
                for j, nm in enumerate(T23N):
                    c = 2 + 57 * i + 27 + 10 * j            # per plane: 3 distances x 9 cells (16 Oct 2026), then 3 ratios x 10
                    if any(x is not None for x in r[c:c + 10]):
                        t23[(r[1], pl, nm)] = r[c:c + 10]
                for k, C in enumerate('SHJ'):
                    c = 2 + 57 * i + 9 * k
                    if any(x is not None for x in r[c:c + 9]):
                        t23[(r[1], pl, C)] = r[c:c + 9]
        if r[0] == 'T12' and '–S ' in str(r[1]):
            C, x = r[1].split('/ ')[1][0], r[1].split('–S ')[1].split(' /')[0]
            for i, pl in enumerate(('RA', 'Dec')):
                if r[2 + 8 * i] is not None:
                    t12[(x, pl, f'S / {C}')] = r[2 + 8 * i:2 + 8 * i + 8]
    return t23, t12, seen


bad, nc, ntog = [], 0, 0
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    pos = {(r[0], r[2], r[3]): (r[5], r[6]) for r in w['POSITIONS'].iter_rows(values_only=True) if r and r[0] and r[2] in ('S', 'H', 'J')}
    for P in [x for x in w.sheetnames if x.startswith('P') and x[1:].isdigit()]:
        t23, t12, seen = t23_rows(w[P])
        xs = [b for (q, C, b) in pos if q == P and C == 'H' and (P, 'J', b) in pos and b != 'Jupiter']
        if sorted(seen) != sorted(set(xs) | ({'equator'} if 'equator' not in xs else set())) or len(seen) != len(set(seen)):
            bad.append((P, 'rows', len(seen), len(xs)))
        for k, v in t12.items():
            nc += 1
            g = t23.get(k)
            if g and str(g[2]).startswith('together, left out'):
                ntog += 1
                x, pl, nm = k
                legs = [(c, abs((pos[(P if c != 'S' else 'SKY', c, x)][0] - pos[(P if c != 'S' else 'SKY', c, 'Jupiter')][0] + 180) % 360 - 180)
                         if pl == 'RA' else abs(pos[(P if c != 'S' else 'SKY', c, x)][1] - pos[(P if c != 'S' else 'SKY', c, 'Jupiter')][1]))
                        for c in ('S', nm[-1])]
                if not any(d < (1.5 if pl == 'RA' else 0.3) for _, d in legs) or v[5] is not None:
                    bad.append((P, k, 'together', legs, v[5]))
                continue
            if g is None or tuple(g[:7]) != tuple(v[:7]) or (v[7] != g[7] and not (str(v[7]).startswith('unison') and str(g[7]).startswith('unison'))) \
                    or (v[5] is not None) != (g[9] is not None) or (v[5] is None) != (g[8] is None):
                bad.append((P, k, g, v))
check('T23 rows = every body, star and equator in both T1 and T2 (not Jupiter), once each; every S / H and S / J cell = T12 (value, +5, '
      'interval, group, offset, score, arrow), with area and timing exactly where there is a score; a cell left out only where Jupiter and X are '
      'together on a leg (RA < 1.5, Dec < 0.3; T12 has no score there) (Lingfield every runner + Ascot)',
      not bad and nc > 0, f'{nc} T12 cells, {ntog} together; {bad[:3]}')
w = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', read_only=True)
t23, _, _ = t23_rows(w['P03'])
h = t23.get(('Haumea', 'RA', 'H / J'))
check('T23 P03 Haumea RA H / J (by hand from POSITIONS: RA H Jupiter 165.660805, H Haumea 211.367148, J Jupiter 58.688530, J Haumea 195.818927): '
      'd 45.706344 / 137.130397, ratio 3.000249 (inverted) on 3 (+0.00025, 97.53), area A, fixed',
      h is not None and h[0] == 3.000249 and h[1] is None and h[2] == '3 · twelfth · Perfect (inverted)' and h[4] == '+0.00025' and h[5] == 97.53
      and h[8] == 'A' and h[9] == 'fixed', str(h))
f23 = {}
cur = None
for r in w['FIELD 23'].iter_rows(values_only=True):
    if r and isinstance(r[0], str) and r[0] in ('RA', 'Dec'):
        cur = r[0]
    elif r and r[0] and cur and r[3] is not None and ' — ' not in r[0]:
        f23[(r[0], cur)] = r[3:5]
check('FIELD 23: P03 column = the T23 H / J cells (value and interval; Haumea RA 3.000249 on 3)',
      f23.get(('Haumea', 'RA'), (None, ''))[0] == 3.000249 and str(f23[('Haumea', 'RA')][1]).startswith('3 +0.00025 [97.53]')
      and all(f23[(x, pl)][0] == t23[(x, pl, 'H / J')][0] for (x, pl) in f23 if (x, pl, 'H / J') in t23), str(f23.get(('Haumea', 'RA'))))
# Eddie 16 Oct 2026: T23 H / J unisons on the Jupiter-return rule with d(H Jupiter, J Jupiter) / the smaller of d(H Jup, H X), d(J Jup, J X)
tags, bad = {}, []
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f, read_only=True)
    pos = {(r[0], r[2], r[3]): (r[5], r[6]) for r in w['POSITIONS'].iter_rows(values_only=True) if r and r[0] and r[2] in ('H', 'J')}
    dist = lambda P, C, x, pl: (abs((pos[(P, C, x)][0] - pos[(P, C, 'Jupiter')][0] + 180) % 360 - 180) if pl == 'RA'
                                else abs(pos[(P, C, x)][1] - (0 if x == 'equator' else pos[(P, C, 'Jupiter')][1])) if x != 'equator'
                                else abs(pos[(P, C, 'Jupiter')][1]))
    for P in [x for x in w.sheetnames if x.startswith('P') and x[1:].isdigit()]:
        t23, _, _ = t23_rows(w[P])
        hj = (lambda pl: abs((pos[(P, 'H', 'Jupiter')][0] - pos[(P, 'J', 'Jupiter')][0] + 180) % 360 - 180) if pl == 'RA'
              else abs(pos[(P, 'H', 'Jupiter')][1] - pos[(P, 'J', 'Jupiter')][1]))
        for (x, pl, nm), c in t23.items():
            if nm != 'H / J' or not str(c[2]).startswith('1 · unison') or c[5] is None:
                continue
            q = hj(pl) / min(dist(P, 'H', x, pl), dist(P, 'J', x, pl))
            want = 'automatic' if q < 0.0015 else 'assisted' if q < 0.02 else ''
            got = 'automatic' if 'automatic (H–J Jupiters close)' in str(c[7]) else 'assisted' if 'H–J assisted' in str(c[7]) else ''
            rk = 'ascot' if 'ascot' in f else 'lingfield'
            tags[(rk, want)] = tags.get((rk, want), 0) + 1
            if want != got or (want == 'automatic' and (c[8] is not None)):
                bad.append((P, x, pl, q, c[7]))
check('T23 H / J unisons (Eddie 16 Oct): "automatic (H–J Jupiters close)" when d(H Jup, J Jup) / the smaller of d(H Jup, H X), d(J Jup, J X) < '
      '0.0015, "H–J assisted" from 0.0015 to < 0.02, recomputed from POSITIONS (Lingfield every runner + Ascot): Lingfield 7 unisons, none tagged; '
      'Ascot 14, 11 assisted (e.g. Polaris Dec 1.005865, q 0.005928), 0 automatic',
      not bad and tags == {('lingfield', ''): 7, ('ascot', ''): 3, ('ascot', 'assisted'): 11}, f'{tags}; {bad[:3]}')
# a constructed case for the automatic branch: Ascot P01 with the jockey's Jupiter and Algol 0.0001 deg from the horse's (Dec)
sys.path.insert(0, 'tools')
import jupiter_tables as JT
_r, _b, _l, _sky, _run = JT.load_input('reference/classic/race_batch_20120619_ascot_1430.xlsx')
_off, _site, _ = MO.off_and_site(_r, _l, _b, None, None)
_ctx = JT.Ctx(_sky, MO.engine_rates(_sky, _off, _site)[0])
_R = dict(_run['P01']); _R['J'] = dict(_R['J'])
hjup, halg = _R['H']['Jupiter'], _R['H']['Algol']
_R['J']['Jupiter'] = (hjup[0], hjup[1] + 0.0001, hjup[2]); _R['J']['Algol'] = (halg[0], halg[1] + 0.0001, halg[2])
cc = JT.t23_cells(_ctx, _R, 'Algol', 'Dec')['H / J']
check('T23 H / J automatic branch (constructed: J Jupiter and J Algol = H + 0.0001 Dec): unison greyed "automatic (H–J Jupiters close)"',
      cc[3] and cc[3]['target'] == '1' and cc[3]['colour'] == 'grey' and cc[3]['auto'] == 'automatic (H–J Jupiters close)', str(cc[3] and (cc[0], cc[3].get('q'))))
# Eddie 16 Oct 2026: T23 distance cells = the T1 / T2 natal cells (H, J; timing "fixed") and the T1 / T2 SKY cells (S), values and fills
bad, nd = [], 0
for f in ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 'reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'):
    w = openpyxl.load_workbook(f)
    for P in [x for x in w.sheetnames if x.startswith('P') and x[1:].isdigit()]:
        ref, got = {}, {}
        for r in w[P].iter_rows():
            v = [c.value for c in r]
            fl = [c.fill.start_color.rgb if c.fill and c.fill.fill_type else None for c in r]
            if v[0] in ('T1', 'T2') and v[1] and re.match(r'^[HJ] Jupiter → [HJ] \S', str(v[1])) and 'bodies, stars' not in str(v[1]):
                C, x = v[1][0], v[1].split(' → ')[1][2:]
                for i, pl in enumerate(('RA', 'Dec')):
                    a = 2 + 8 * i
                    if v[a] is not None:
                        ref[(x, pl, C)] = (tuple(v[a:a + 8]) + ('fixed' if v[a + 5] is not None else None,), fl[a])
                    b = 18 + 9 * i
                    if len(v) > b and v[b] is not None:
                        k = (x, pl, 'S')
                        if k in ref and ref[k] != (tuple(v[b:b + 9]), fl[b]):
                            bad.append(('T1 / T2 SKY differ', P, k))
                        ref[k] = (tuple(v[b:b + 9]), fl[b])
            if v[0] == 'T23' and v[1] and v[1] != 'X' and not str(v[1]).startswith('T23 ratios'):
                for i, pl in enumerate(('RA', 'Dec')):
                    for k, C in enumerate('SHJ'):
                        c = 2 + 57 * i + 9 * k
                        if any(x is not None for x in v[c:c + 9]):
                            got[(v[1], pl, C)] = (tuple(v[c:c + 9]), fl[c])
        for k in set(ref) | set(got):
            if k[0] in set(JT.STARS) ^ set(JT.T1_T2_T24_STARS):   # 19 Oct 2026: Polaris only in T23, the 13 new stars only in T1 / T2 (T23 unchanged: test 30)
                continue
            nd += 1
            if ref.get(k) != got.get(k):
                bad.append((P, k, got.get(k), ref.get(k)))
check('T23 distance cells (Eddie 16 Oct): every S Jupiter → S X, H Jupiter → H X, J Jupiter → J X cell group (value, +5, target, group, offset, '
      'score, arrow, also, timing; value fill) = the matching T1 / T2 SKY cells and T1 / T2 natal cells (timing "fixed" where scored), none '
      'missing or extra (Lingfield every runner + Ascot)', not bad and nd > 0, f'{nd} cell groups; {bad[:3]}')
# Test 28 (Eddie, 19 Oct 2026): Galactic Centre as the 23rd star (engine + card pipeline) and T24 stars against bodies
import shutil, tempfile, math
print('test 28: Galactic Centre (card pipeline rebuild of Ascot 14:30 2012) and T24')
AP = os.path.expanduser('~/astronomy-project')
tmp = tempfile.mkdtemp(prefix='jt_gc_')
shutil.copy(f'{AP}/racecards/20120619_ascot/race_batch_20120619_ascot_1430.csv', tmp)
r = subprocess.run([sys.executable, 'run_card_swiss.py', '--folder', tmp, '--skip-scrape', '--skip-vibrations', '--skip-pipeline',
                    '--skip-detail', '--skip-predict', '--tables'], cwd=AP, capture_output=True, text=True)
gcf = f'{tmp}/race_batch_20120619_ascot_1430_jupiter_tables.xlsx'
check('T28 card pipeline rebuild of Ascot 14:30 2012 writes the tables workbook', r.returncode == 0 and os.path.exists(gcf), r.stdout[-300:] + r.stderr[-300:])
gb = openpyxl.load_workbook(f'{tmp}/race_batch_20120619_ascot_1430.xlsx', read_only=True)
ob = openpyxl.load_workbook('reference/classic/race_batch_20120619_ascot_1430.xlsx', read_only=True)
bad = []
for sh in ('TRANS', 'P01', 'P02'):
    g = {x[1]: x for x in gb[sh].iter_rows(min_row=2, values_only=True) if x and x[1]}
    o = {x[1]: x for x in ob[sh].iter_rows(min_row=2, values_only=True) if x and x[1]}
    if set(g) - set(o) != {x + '_B' for x in ['Galactic Centre'] + JT.NEW_STARS} or any(g.get(k) != o[k] for k in o):   # + 13 stars (19 Oct 2026)
        bad.append(sh)
gsky = next(x for x in gb['TRANS'].iter_rows(min_row=2, values_only=True) if x and x[1] == 'Galactic Centre_B')
check('T28 batch: Galactic Centre_B (and, 19 Oct 2026, the 13 new stars) on TRANS, horse and jockey sheets, every other row identical to the old batch; sky RA / Dec = Sgr A* '
      '(apparent J2000; ~266.417 / -29.008 to 0.01)', not bad and abs(gsky[4] - 266.417) < 0.01 and abs(gsky[8] + 29.008) < 0.01,
      f'{bad}; sky {gsky[4]:.6f} / {gsky[8]:.6f}')
gw = openpyxl.load_workbook(gcf)


def t24_blocks(ws, mids=None):
    """{block title start: (header bodies [(body, plane)], {star label: [cells]})}. Layout (Eddie, 19 Oct 2026, revised): header row 1
    'RA' merged over the RA body columns, 'RA midpoints', 'Dec' merged over the Dec body columns, 'Dec midpoints'; row 2 body names.
    mids: filled with {(block, star label, plane): midpoint cell}"""
    out, cur, hdr, rows = {}, None, None, None
    it = list(ws.iter_rows())
    for i, x in enumerate(it):
        if x[0].value == 'T24' and str(x[1].value).startswith('T24 '):
            cur = x[1].value.split(' (')[0]; rows = {}
            h1, h2 = it[i + 1], it[i + 2]
            hdr, cols, mcol, pl = [], [], {}, None
            for c in range(2, len(h1)):
                if h1[c].value in ('RA', 'Dec'):
                    pl = h1[c].value
                if h1[c].value == 'repeats':                 # T24 repeats column (Eddie, 22 Oct 2026; test 41)
                    break
                if str(h1[c].value or '').endswith(' midpoints'):
                    mcol[h1[c].value.split()[0]] = c
                elif pl and h2[c].value:
                    hdr.append((h2[c].value, pl)); cols.append(c)
            out[cur] = (hdr, rows)
        elif cur and x[0].value == 'T24':
            rows[x[1].value] = [x[c] for c in cols]
            if mids is not None:
                for p, c in mcol.items():
                    mids[(cur, x[1].value, p)] = x[c]
        elif cur and x[0].value != 'table' and x[0].value is None and rows:
            cur = None
    return out


gc_in = {}
for sh in ('SKY JUPITER', 'P01'):
    for x in gw[sh].iter_rows():
        if x[1].value and 'Galactic Centre' in str(x[1].value) and x[0].value:
            gc_in.setdefault(x[0].value, 0); gc_in[x[0].value] += 1
check('T28 Galactic Centre in T1, T2, T21, T22, T24 (and SKY) of the rebuilt Ascot, not in T19 (royal only)',
      all(gc_in.get(t) for t in ('SKY', 'T1', 'T2', 'T21', 'T22', 'T24')) and not gc_in.get('T19'), str(gc_in))
# (b) five cells by hand from POSITIONS
pos = {}
for x in gw['POSITIONS'].iter_rows(min_row=5, values_only=True):
    if x and x[3]:
        pos[(x[0] if x[0] != 'SKY' else 'SKY', x[2], x[3])] = (x[5], x[6])
PHI = (1 + 5 ** 0.5) / 2
sq = lambda tol, dev: (10 * (tol - dev) / tol) ** 2
cases = [  # (sheet, block, chart, star, body, plane, expected value, score formula, fill, comment)
    ('SKY JUPITER', 'T24 SKY', ('SKY', 'S'), 'Galactic Centre', 'Ceres', 'RA', 150.475762, lambda v: sq(0.03236, abs(v - 93 * PHI)), GREEN,
     '93×φ · golden · {o} · {s}', lambda v: v - 93 * PHI),
    ('P01', 'T24 HORSE', ('P01', 'H'), 'Galactic Centre', 'Mars', 'RA', 177.745864, lambda v: 100 * (1.277778 - abs(v - 1600 / 9)) / 1.277778,
     GREEN, '177.778 · ninth · {o} · {s}', lambda v: v - 1600 / 9),
    ('P01', 'T24 JOCKEY', ('P01', 'J'), 'Galactic Centre', 'Sedna', 'Dec', 32.362221, lambda v: sq(0.03236, abs(v - 20 * PHI)), GREEN,
     '20×φ · golden · {o} · {s}', lambda v: v - 20 * PHI),
    ('P01', 'T24 HORSE', ('P01', 'H'), 'Algorab', 'Makemake', 'RA', 0.064638, lambda v: sq(1.5, v), '00FF8080',   # conjunction red (20 Oct 2026)
     '0 · conjunction (RA < 1.5) · {o} · {s}', lambda v: v),
    ('P01', 'T24 HORSE', ('P01', 'H'), 'Galactic Centre', 'Sun', 'RA', 57.972709, None, None, 'nearest: 58 · whole — outside ±0.02 · {o}',
     lambda v: v - 58),
]
for sh, blk, (who, C), star, body, pl, exp, sc, fill, txt, off in cases:
    a, b = pos[(who, C, star)], pos[(who, C, body)]
    d = abs(a[0] - b[0]) % 360.0
    v = (min(d, 360.0 - d)) if pl == 'RA' else abs(a[1] - b[1])
    hdr, rows = t24_blocks(gw[sh])[blk]
    c = rows[f'{C[-1]} {star}'][hdr.index((body, pl))]
    want = txt.format(o=f'{off(v):+.5f}', s=f'{sc(v):.2f}' if sc else '')
    got_fill = c.fill.start_color.rgb if c.fill and c.fill.fill_type else None
    check(f'T28 {blk} {C[-1]} {star} – {C[-1]} {body} {pl} by hand from POSITIONS', abs(c.value - round(v, 6)) < 1e-9 and abs(v - exp) < 1e-6
          and got_fill == fill and c.comment and c.comment.text.split('\n')[0] == want, f'{c.value} / {v:.6f}, {got_fill}, {c.comment and c.comment.text!r} vs {want!r}')
# (c) grid shapes: rebuilt Ascot 23 stars; the old Lingfield and Ascot batches 22 (Galactic Centre skipped quietly)
# 19 Oct 2026 (Eddie): T24 on T1_T2_T24_STARS (no Polaris, + 13 stars): rebuilt Ascot 35 rows, the old batches 21
bad, n = [], 0
for f, nstar in ((gcf, 67), ('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx', 21),
                 ('reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx', 21)):
    w = gw if f == gcf else openpyxl.load_workbook(f)
    for sh in [s for s in w.sheetnames if s == 'SKY JUPITER' or re.fullmatch(r'P\d\d', s)]:
        bl = t24_blocks(w[sh])
        want = ['T24 SKY'] if sh == 'SKY JUPITER' else ['T24 HORSE', 'T24 JOCKEY']
        if sorted(bl) != sorted(want):
            bad.append((f, sh, list(bl))); continue
        for k, (hdr, rows) in bl.items():
            n += 1
            nb = 25 if k == 'T24 SKY' else 24
            moon = any(b == 'Moon' for b, _ in hdr)
            cells = [c for cs in rows.values() for c in cs]
            if (len(rows) != nstar or len(hdr) != 2 * nb or moon != (k == 'T24 SKY')
                    or any(c.value is None or c.comment is None for c in cells) or ('Galactic Centre' in str(list(rows))) != (nstar == 67)):
                bad.append((f[-40:], sh, k, len(rows), len(hdr), moon))
check('T28 every T24 grid = stars x (2 x bodies): 67 x 50 sky (Moon incl.), 67 x 48 natal on the rebuilt Ascot (35 until 20 Oct 2026, 46 until 21 Oct); 21 rows on the old batches; '
      'every cell a value and a comment', not bad and n == 3 + 13 + 3, f'{n} grids (rebuilt Ascot 3, Lingfield 13, old Ascot 3); {bad[:3]}')
# Test 29 (Eddie, 19 Oct 2026): T24 columns RA then Dec, and T24 midpoints (the star the middle point of two bodies of the block)
print('test 29: T24 RA-then-Dec columns and midpoints')
bad, n = [], 0
for f in (gcf, 'reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx'):
    w = gw if f == gcf else openpyxl.load_workbook(f)
    for sh in [s for s in w.sheetnames if s == 'SKY JUPITER' or re.fullmatch(r'P\d\d', s)]:
        for r0 in w[sh].iter_rows():
            if r0[0].value == 'T24' and str(r0[1].value).startswith('T24 '):
                n += 1
                h1 = [c.value for c in w[sh][r0[0].row + 1]]; h2 = [c.value for c in w[sh][r0[0].row + 2]]
                nb = 25 if 'SKY' in r0[1].value else 24
                want1 = ['RA'] + [None] * (nb - 1) + ['RA midpoints', 'Dec'] + [None] * (nb - 1) + ['Dec midpoints']
                body = [b for b in JT.T24_BODIES if nb == 25 or b != 'Moon']
                if h1[2:2 + 2 * nb + 2] != want1 or h2[2:2 + nb] != body or h2[3 + nb:3 + 2 * nb] != body:
                    bad.append((f[-40:], sh, r0[1].value[:12]))
check('T29 every T24 block: header row 1 RA (merged) .. RA midpoints, Dec (merged) .. Dec midpoints; row 2 the bodies in order, RA half then Dec half',
      not bad and n == 3 + 13, f'{n} blocks; {bad[:3]}')
gp = {}
for x in gw['POSITIONS'].iter_rows(min_row=5, values_only=True):
    if x and x[3]:
        gp[(x[0], x[2], x[3])] = (x[5], x[6])


def by_hand(who, C, star, a, b, pl):
    """midpoint from POSITIONS, own code: RA near / far midpoint (closer), arc distances; Dec signed"""
    s, pa, pb = (gp[(who, C, z)] for z in (star, a, b))
    if pl == 'RA':
        arc = lambda u, v: abs((u - v + 180) % 360 - 180)
        mid = (pa[0] + ((pb[0] - pa[0] + 180) % 360 - 180) / 2) % 360
        near, far = (s[0] - mid + 180) % 360 - 180, (s[0] - mid) % 360 - 180
        side, off = ('near', near) if abs(near) <= abs(far) else ('far', far)
        d1, d2, dab, tol = arc(s[0], pa[0]), arc(s[0], pb[0]), arc(pa[0], pb[0]), 0.5
    else:
        side, off = '', s[1] - (pa[1] + pb[1]) / 2
        d1, d2, dab, tol = abs(s[1] - pa[1]), abs(s[1] - pb[1]), abs(pa[1] - pb[1]), 0.15
    close = 100 * min(d1, d2) / max(d1, d2)
    rh, dh = 0.5 * (10 * (10 - (100 - close)) / 10) ** 2, 0.5 * (10 * (tol - abs(off)) / tol) ** 2
    pos = 'between' if abs(dab - (d1 + d2)) <= 0.01 * (d1 + d2) else 'far side'
    return d1, d2, off, side, close, rh, dh, rh + dh, pos


gm = {}
for sh in ('SKY JUPITER', 'P01'):
    t24_blocks(gw[sh], gm)
cases = [  # (block, who, chart, star, A, B, plane, d1, d2, offset, side, closeness, ratio half, distance half, total, between / far side)
    ('T24 SKY', 'SKY', 'S', 'Galactic Centre', 'Mercury', 'Jupiter', 'RA', 153.457407, 153.219387, 0.119010, 'far', 99.8449, 48.46, 29.03, 77.49, 'far side'),
    ('T24 HORSE', 'P01', 'H', 'Arcturus', 'Jupiter', 'Orcus', 'RA', 69.091938, 69.107610, 0.007836, 'near', 99.9773, 49.77, 48.45, 98.22, 'between'),
    ('T24 JOCKEY', 'P01', 'J', 'Regulus', 'Chiron', 'Orcus', 'Dec', 5.534608, 5.506910, -0.013849, '', 99.4996, 45.12, 41.19, 86.31, 'between'),
]
for blk, who, C, star, a, b, pl, e1, e2, eo, es, ec, er, ed, et, ep in cases:
    d1, d2, off, side, close, rh, dh, tot, pos = by_hand(who, C, star, a, b, pl)
    txt = f"{a} = {b} {tot:.2f} ({side + ', ' if side else ''}{pos})"
    mc = gm[(blk, f'{C} {star}', pl)]
    hdr, rows = t24_blocks(gw['SKY JUPITER' if who == 'SKY' else 'P01'])[blk]
    ca, cb = (rows[f'{C} {star}'][hdr.index((z, pl))] for z in (a, b))
    ok = (abs(d1 - e1) < 1e-6 and abs(d2 - e2) < 1e-6 and abs(off - eo) < 1e-6 and side == es and abs(close - ec) < 1e-4
          and f'{rh:.2f}' == f'{er:.2f}' and f'{dh:.2f}' == f'{ed:.2f}' and f'{tot:.2f}' == f'{et:.2f}' and pos == ep
          and txt in str(mc.value) and ca.border.left.style == 'thick' == cb.border.right.style
          and f'midpoint with {b}: total {tot:.2f}' in ca.comment.text and f'midpoint with {a}: total {tot:.2f}' in cb.comment.text)
    check(f'T29 {blk} {C} {star} {pl} {a} = {b} by hand from POSITIONS', ok,
          f'{d1:.6f} / {d2:.6f}, offset {off:+.6f} {side}, {close:.4f} %, {rh:.2f} + {dh:.2f} = {tot:.2f}, {pos}; cell {mc.value!r}')
# not listed: "A, B together" (Ascot P01 H Capella RA Juno – Quaoar, d 1.3896 < 1.5, would score 64.50) and the own Rahu – Ketu pair
# (Lingfield P03 J Alkaid RA, d 180, would score 46.33); no 'Rahu = Ketu' anywhere
d1, d2, off, side, close, rh, dh, tot, pos = by_hand('P01', 'H', 'Capella', 'Juno', 'Quaoar', 'RA')
dab = abs((gp[('P01', 'H', 'Juno')][0] - gp[('P01', 'H', 'Quaoar')][0] + 180) % 360 - 180)
cap = gm[('T24 HORSE', 'H Capella', 'RA')].value
lw = openpyxl.load_workbook('reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx')
lm = {}
t24_blocks(lw['P03'], lm)
alk = lm[('T24 JOCKEY', 'J Alkaid', 'RA')].value
rk = sum('Rahu = Ketu' in str(c.value) for w in (gw, lw) for sh in w.sheetnames for r in w[sh].iter_rows() if r[0].value == 'T24' for c in r)
check('T29 not listed: together pair Ascot P01 H Capella RA Juno – Quaoar (by hand d(A, B) < 1.5, a midpoint hit otherwise) and own Rahu – Ketu '
      '(Lingfield P03 J Alkaid RA); no "Rahu = Ketu" in any T24 cell',
      dab < 1.5 and tot >= 50 and 'Juno = Quaoar' not in str(cap) and 'Rahu = Ketu' not in str(alk) and rk == 0,
      f'd(Juno, Quaoar) {dab:.4f}, total {tot:.2f}; Capella cell {cap!r}; Alkaid cell {alk!r}; Rahu = Ketu cells {rk}')
# Test 30 (Eddie, 19 Oct 2026): 13 more stars in the engine; T1, T2 and T24 on T1_T2_T24_STARS (35 stars, |Dec| <= 50: no Polaris),
# every other table on STARS as before; the default workbook = POSITIONS, SKY JUPITER and the runner sheets (--full: every sheet as before)
print('test 30: T1 / T2 / T24 star list and the trimmed default workbook')
NEWRE = re.compile(r'\b(' + '|'.join(x if x != 'Deneb' else r'Deneb(?! Algedi)' for x in JT.NEW_STARS) + r')\b')
runner_tabs = lambda w: [s for s in w.sheetnames if re.fullmatch(r'P\d\d', s)]
lf = 'reference/classic/race_batch_20210402_lingfield_aw_1435_jupiter_tables.xlsx'      # built with --full above
ld = f'{tmp}/lingfield_default_jupiter_tables.xlsx'
r = subprocess.run([sys.executable, 'tools/jupiter_tables.py', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', '--out', ld],
                   capture_output=True, text=True)
ldw, lfw = openpyxl.load_workbook(ld, read_only=True), openpyxl.load_workbook(lf, read_only=True)
vals = lambda ws: [tuple(x) for x in ws.iter_rows(values_only=True)]
same = [sh for sh in ldw.sheetnames if sh in lfw.sheetnames and vals(ldw[sh]) == vals(lfw[sh])]
check('T30 default workbook = POSITIONS, SKY JUPITER and the P## sheets only (rebuilt Ascot via run_card_swiss.py --tables, Lingfield); '
      'each equal to the --full workbook\'s sheet',
      gw.sheetnames == ['POSITIONS', 'SKY JUPITER', 'P01'] and ldw.sheetnames == ['POSITIONS', 'SKY JUPITER'] + runner_tabs(lfw)
      and same == ldw.sheetnames and len(lfw.sheetnames) > len(ldw.sheetnames),
      f'Ascot {gw.sheetnames}; Lingfield {ldw.sheetnames} ({len(same)} equal to --full, which has {len(lfw.sheetnames)} sheets)')
# T1, T2 and T24 on the rebuilt Ascot: the 35 stars in order, the 13 new ones in, no Polaris
gs = {}
for sh in ('SKY JUPITER', 'P01'):
    for x in gw[sh].iter_rows(values_only=True):
        if x[0] in ('T1', 'T2') and x[1] and ' → ' in str(x[1]) and x[1].split(' → ')[1].split(' ', 1)[1] in JT.T1_T2_T24_STARS + ['Polaris']:
            gs.setdefault(x[0], []).append(x[1].split(' → ')[1].split(' ', 1)[1])
for k, (hdr, rows) in {**t24_blocks(gw['SKY JUPITER']), **t24_blocks(gw['P01'])}.items():
    gs[k] = [lab.split(' ', 1)[1] for lab in rows]
check('T30 rebuilt Ascot T1, T2, T24 SKY / HORSE / JOCKEY: the 67 stars of T1_T2_T24_STARS in order (13 + 11 + 21 new ones in, no Polaris)',
      len(JT.T1_T2_T24_STARS) == 67 and all(gs.get(k) == JT.T1_T2_T24_STARS for k in ('T1', 'T2', 'T24 SKY', 'T24 HORSE', 'T24 JOCKEY')),
      str({k: len(v) for k, v in gs.items()}))
# no other table carries the 13 (rebuilt Ascot, --full, and its pairs workbook); T23 unchanged (Polaris kept)
gf = f'{tmp}/full_jupiter_tables.xlsx'
r = subprocess.run([sys.executable, 'tools/jupiter_tables.py', f'{tmp}/race_batch_20120619_ascot_1430.xlsx', '--full', '--out', gf],
                   capture_output=True, text=True)
gfw = openpyxl.load_workbook(gf, read_only=True)
# 20 Oct 2026 (Eddie, 11 more stars): the comparisons of tests 31 - 33 with their builds before run on a 35-star copy of the rebuilt batch
# (the 11 '_B' rows taken out), so they keep checking their own change; test 34 checks 35 -> 46
NEW11 = ['Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Menkar', 'Phact', 'Adhara', 'Wezen', 'Menkent', 'Unukalhai', 'Rasalhague']
# 21 Oct 2026 (Eddie, 20 more stars and the Orion Nebula Cluster): likewise a 46-star copy (the 21 '_B' rows taken out) for tests 34 and 35;
# test 36 checks 46 -> 67
NEW21 = ['Ankaa', 'Al Rescha', 'Mirfak', 'El Nath', 'Meissa', 'Alnilam', 'Murzim', 'Alhena', 'Acubens', 'Alphard', 'Alkes', 'Zosma',
         'Vindemiatrix', 'Diadem', 'Ras Algethi', 'Aculeus', 'Acumen', 'Facies', 'Rukbat', 'Sualocin', 'Orion Nebula Cluster']


def batch_copy(out, drop):
    _w = openpyxl.load_workbook(f'{tmp}/race_batch_20120619_ascot_1430.xlsx')
    for _ws in _w.worksheets:
        for _i in [x[0].row for x in _w[_ws.title].iter_rows() if len(x) > 1 and x[1].value in {n + '_B' for n in drop}][::-1]:
            _ws.delete_rows(_i)
    _w.save(out)


os.makedirs(f'{tmp}/s35', exist_ok=True)
os.makedirs(f'{tmp}/s46', exist_ok=True)
b35, b46 = f'{tmp}/s35/race_batch_20120619_ascot_1430.xlsx', f'{tmp}/s46/race_batch_20120619_ascot_1430.xlsx'
batch_copy(b35, NEW11 + NEW21)
batch_copy(b46, NEW21)
gf35, gf46 = f'{tmp}/s35/full_jupiter_tables.xlsx', f'{tmp}/s46/full_jupiter_tables.xlsx'
for _b, _o in ((b35, gf35), (b46, gf46)):
    subprocess.run([sys.executable, 'tools/jupiter_tables.py', _b, '--full', '--out', _o], capture_output=True, text=True)
gw46 = openpyxl.load_workbook(gf46)
# 20 Oct 2026 (Eddie, T24 conjunction red): the comparisons of tests 31 - 34 with their builds before run on builds by the code of commit
# 93e73bc4 (before the red fill), so they keep checking their own change; test 35 checks 93e73bc4 -> now (red fill only)
bf = 'tools/_jt_before_93e73bc4.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '93e73bc4:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
os.makedirs(f'{tmp}/h93', exist_ok=True)
lf_h, gf_h, gf35_h = (f'{tmp}/h93/{n}_jupiter_tables.xlsx' for n in ('lingfield', 'ascot', 'ascot35'))
for inp, out in (('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_h), (b46, gf_h),          # 46-star copy (21 Oct 2026)
                 (b35, gf35_h)):
    subprocess.run([sys.executable, bf, inp, '--full', '--out', out], capture_output=True, text=True)
os.remove(bf)
# 21 Oct 2026 (Eddie, 20 more stars): builds by the code of commit ad0defaf (46 stars, red fill) - test 35 compares 93e73bc4 with these,
# test 36 compares these with now (lf_r, gf_r on the full 66-star batch)
bf = 'tools/_jt_before_ad0defaf.py'
open(bf, 'w').write(subprocess.run(['git', 'show', 'ad0defaf:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
os.makedirs(f'{tmp}/had', exist_ok=True)
lf_r, gf_r, gf46_r, gf35_r = (f'{tmp}/had/{n}_jupiter_tables.xlsx' for n in ('lingfield', 'ascot', 'ascot46', 'ascot35'))
for inp, out in (('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_r), (f'{tmp}/race_batch_20120619_ascot_1430.xlsx', gf_r),
                 (b46, gf46_r), (b35, gf35_r)):
    subprocess.run([sys.executable, bf, inp, '--full', '--out', out], capture_output=True, text=True)
os.remove(bf)
# 22 Oct 2026 (Eddie, every star in every timeline, LONG >= 90): builds by the code of commit 18aff98a (67 stars, before that change) - tests 34
# and 36 count and compare on these, test 37 compares them with now
bf = 'tools/_jt_before_18aff98a.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '18aff98a:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
os.makedirs(f'{tmp}/h18', exist_ok=True)
lf_s, gf_s, gf46_s = (f'{tmp}/h18/{n}_jupiter_tables.xlsx' for n in ('lingfield', 'ascot', 'ascot46'))
for inp, out in (('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_s), (f'{tmp}/race_batch_20120619_ascot_1430.xlsx', gf_s),
                 (b46, gf46_s)):
    subprocess.run([sys.executable, bf, inp, '--full', '--out', out], capture_output=True, text=True)
os.remove(bf)
gw46_s, gw_s = openpyxl.load_workbook(gf46_s), openpyxl.load_workbook(gf_s)
# 22 Oct 2026 (Eddie, LONG STAR TIMELINE): builds by the code of commit 632447ff (star timelines, before LONG STAR TIMELINE) - test 37 compares
# 18aff98a with these, test 38 compares these with now
bf = 'tools/_jt_before_632447ff.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '632447ff:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
os.makedirs(f'{tmp}/h63', exist_ok=True)
lf_t, gf_t = (f'{tmp}/h63/{n}_jupiter_tables.xlsx' for n in ('lingfield', 'ascot'))
for inp, out in (('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_t), (f'{tmp}/race_batch_20120619_ascot_1430.xlsx', gf_t)):
    subprocess.run([sys.executable, bf, inp, '--full', '--out', out], capture_output=True, text=True)
os.remove(bf)
# 22 Oct 2026 (Eddie, sky star timelines trimmed, T24 STAR SELECT): builds by the code of commit 00b6db9e (LONG STAR TIMELINE) - test 38
# compares 632447ff with these, test 39 compares these with now
bf = 'tools/_jt_before_00b6db9e.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '00b6db9e:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
os.makedirs(f'{tmp}/h00', exist_ok=True)
lf_u, gf_u = (f'{tmp}/h00/{n}_jupiter_tables.xlsx' for n in ('lingfield', 'ascot'))
lf_ud, gf_ud = (f'{tmp}/h00/{n}_def_jupiter_tables.xlsx' for n in ('lingfield', 'ascot'))
for inp, out, fl in (('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_u, ['--full']), (f'{tmp}/race_batch_20120619_ascot_1430.xlsx', gf_u, ['--full']),
                     ('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_ud, []), (f'{tmp}/race_batch_20120619_ascot_1430.xlsx', gf_ud, [])):
    subprocess.run([sys.executable, bf, inp] + fl + ['--out', out], capture_output=True, text=True)
os.remove(bf)
# 22 Oct 2026 (Eddie, T24 STAR SELECT removed): builds by the code of commit 0ad7d2e5 (with T24 STAR SELECT), default and --full, with their
# pairs workbooks - test 40 compares these with now
bf = 'tools/_jt_before_0ad7d2e5.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '0ad7d2e5:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
os.makedirs(f'{tmp}/h0a', exist_ok=True)
H0A = {(n, f): f'{tmp}/h0a/{n}_{f}_jupiter_tables.xlsx' for n in ('lingfield', 'ascot') for f in ('full', 'def')}
for (n, f), out in H0A.items():
    inp = 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx' if n == 'lingfield' else f'{tmp}/race_batch_20120619_ascot_1430.xlsx'
    subprocess.run([sys.executable, bf, inp] + (['--full'] if f == 'full' else []) + ['--out', out], capture_output=True, text=True)
os.remove(bf)
# 22 Oct 2026 (Eddie, T24 repeats flag): builds by the code of commit 5e10f7bf (T24 STAR SELECT removed, before the repeats), default and
# --full - test 41 compares these with now
bf = 'tools/_jt_before_5e10f7bf.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '5e10f7bf:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
os.makedirs(f'{tmp}/h5e', exist_ok=True)
H5E = {(n, f): f'{tmp}/h5e/{n}_{f}_jupiter_tables.xlsx' for n in ('lingfield', 'ascot') for f in ('full', 'def')}
for (n, f), out in H5E.items():
    inp = 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx' if n == 'lingfield' else f'{tmp}/race_batch_20120619_ascot_1430.xlsx'
    subprocess.run([sys.executable, bf, inp] + (['--full'] if f == 'full' else []) + ['--out', out], capture_output=True, text=True)
os.remove(bf)
leak = []
for w in (gfw, openpyxl.load_workbook(f'{tmp}/full_pairs.xlsx', read_only=True)):
    for sh in w.sheetnames:
        if sh == 'POSITIONS':
            continue
        for x in w[sh].iter_rows(values_only=True):
            if x and (x[0] in ('T1', 'T2', 'T24', 'T24 H / J', 'T24 HORSE RATIOS', 'T24 JOCKEY RATIOS')   # T24 ratio tables (test 32)
                      or sh == 'SKY JUPITER' and x[0] in ('SKY', 'SKY STARS', 'TIMELINE', 'LONG TIMELINE', 'STAR TIMELINE', 'LONG STAR TIMELINE')   # SKY block (test 31); SKY STARS, sky timelines (test 33)
                      or x[0] in ('TIMELINE H', 'TIMELINE J', 'LONG TIMELINE H', 'LONG TIMELINE J', 'STAR TIMELINE H', 'STAR TIMELINE J',
                                 'LONG STAR TIMELINE H', 'LONG STAR TIMELINE J', 'T24 STAR SELECT')):  # 22 Oct 2026 (tests 37 - 39)
                continue
            hit = [v for v in x if isinstance(v, str) and NEWRE.search(v)]
            if hit:
                leak.append((sh, x[0], hit[0][:60]))
t23 = lambda w: {x[1]: x for x in w['P01'].iter_rows(values_only=True) if x and x[0] == 'T23' and x[1] in JT.STARS + JT.BODIES + ['Ketu', JT.EQUATOR]}
n23, o23 = t23(gfw), t23(openpyxl.load_workbook('reference/classic/race_batch_20120619_ascot_1430_jupiter_tables.xlsx', read_only=True))
check('T30 rebuilt Ascot --full: none of the 13 new stars in any table but T1, T2, T24 and (19 Oct 2026) the SKY block (every sheet, pairs workbook too); T23 on STARS as '
      'before (Polaris kept; every row = the old 22-star Ascot build\'s, the Galactic Centre row added)',
      not leak and 'Polaris' in n23 and set(n23) - set(o23) == {'Galactic Centre'} and all(n23[k] == o23[k] for k in o23)
      and not any(x in n23 for x in JT.NEW_STARS),
      f'{len(gfw.sheetnames)} sheets; leaks {leak[:3]}; T23 rows {len(n23)} vs old {len(o23)}')
# two T1, two T2 and three T24 cells of new stars by hand from POSITIONS (rebuilt Ascot)
rates = {x[3]: (x[7], x[8]) for x in gw['POSITIONS'].iter_rows(min_row=5, values_only=True) if x and x[0] == 'SKY' and x[3]}
ra_d = lambda u, v: min(abs(u - v) % 360, 360 - abs(u - v) % 360)
dist = lambda p, q, pl: ra_d(p[0], q[0]) if pl == 'RA' else abs(p[1] - q[1])
cases = [  # (table, chart, star, plane, value, target text, offset text, score by hand, fill)
    ('T1', 'H', 'Pollux', 'RA', 166.673131, '166.667 (ninth)', lambda v: v - 500 / 3, lambda v: 100 * (1.166667 - abs(v - 500 / 3)) / 1.166667, GREEN),
    ('T1', 'H', 'Markab', 'Dec', 37.994684, '38 (whole)', lambda v: v - 38, lambda v: sq(0.02, abs(v - 38)), YELLOW),
    ('T2', 'J', 'Hamal', 'Dec', 46.919384, '29×φ (golden)', lambda v: v - 29 * PHI, lambda v: sq(0.03236, abs(v - 29 * PHI)), YELLOW),
    ('T2', 'J', 'Kaus Australis', 'RA', 0.188691, 'conj (conj)', lambda v: v, lambda v: sq(1.5, v), YELLOW),
]
for tid, C, star, pl, exp, tt, off, sc, fill in cases:
    x = row(gw['P01'], tid, f'{C} Jupiter → {C} {star}')
    c0 = 2 if pl == 'RA' else 10
    v = dist(gp[('P01', C, 'Jupiter')], gp[('P01', C, star)], pl)
    got_fill = x[c0].fill.start_color.rgb if x[c0].fill and x[c0].fill.fill_type else None
    check(f'T30 {tid} {C} Jupiter → {C} {star} {pl} by hand from POSITIONS', abs(v - exp) < 1e-6 and x[c0].value == round(v, 6)
          and x[c0 + 2].value == tt and x[c0 + 4].value == f'{off(v):+.5f}' and f'{x[c0 + 5].value:.2f}' == f'{sc(v):.2f}' and got_fill == fill,
          f'{v:.6f}; {x[c0 + 2].value}, {x[c0 + 4].value}, {x[c0 + 5].value} (by hand {sc(v):.2f}), {got_fill}')
# its SKY cell: S Jupiter → S Pollux RA, at the off and +5 min from the POSITIONS rates; nearest 35×φ outside
x = row(gw['P01'], 'T1', 'H Jupiter → H Pollux')
sj, sp = gp[('SKY', 'S', 'Jupiter')], gp[('SKY', 'S', 'Pollux')]
v0 = ra_d(sj[0], sp[0]); v5 = ra_d(sj[0] + 5 * rates['Jupiter'][0], sp[0] + 5 * rates['Pollux'][0])
check('T30 T1 H Pollux row, SKY cell S Jupiter → S Pollux RA by hand from POSITIONS (+5 min from the rates): 56.678406 -> 56.677607, nearest 35×φ outside',
      abs(v0 - 56.678406) < 1e-6 and x[18].value == round(v0, 6) and x[19].value == round(v5, 6) and x[20].value == '35×φ (golden) — outside ±0.0324'
      and x[22].value == f'{v0 - 35 * PHI:+.5f}', f'{v0:.6f} -> {v5:.6f}; {x[18].value}, {x[19].value}, {x[20].value}, {x[22].value}')
cases = [  # (sheet, block, who, chart, star, body, plane, value, comment, offset, score)
    ('SKY JUPITER', 'T24 SKY', 'SKY', 'S', 'Deneb', 'Makemake', 'Dec', 17.799198, '11×φ · golden', lambda v: v - 11 * PHI, lambda v: sq(0.03236, abs(v - 11 * PHI))),
    ('P01', 'T24 HORSE', 'P01', 'H', 'Pollux', 'Eris', 'Dec', 32.999538, '33 · whole', lambda v: v - 33, lambda v: sq(0.02, abs(v - 33))),
    ('P01', 'T24 JOCKEY', 'P01', 'J', 'Praesepe', 'Neptune', 'RA', 138.999718, '139 · whole', lambda v: v - 139, lambda v: sq(0.02, abs(v - 139))),
]
for sh, blk, who, C, star, body, pl, exp, tt, off, sc in cases:
    v = dist(gp[(who, C, star)], gp[(who, C, body)], pl)
    hdr, rows = t24_blocks(gw[sh])[blk]
    c = rows[f'{C} {star}'][hdr.index((body, pl))]
    want = f'{tt} · {off(v):+.5f} · {sc(v):.2f}'
    got_fill = c.fill.start_color.rgb if c.fill and c.fill.fill_type else None
    check(f'T30 {blk} {C} {star} – {C} {body} {pl} by hand from POSITIONS', abs(v - exp) < 1e-6 and c.value == round(v, 6)
          and c.comment.text.split('\n')[0] == want and got_fill == GREEN, f'{v:.6f}; {c.comment.text.splitlines()[0]!r} vs {want!r}; {got_fill}')
# Test 31 (Eddie, 19 Oct 2026): T1, T2, T24 and the SKY block star rows on T1_T2_T24_STARS in RA order (engine J2000 RA at J2000.0);
# the SKY block on the 35 stars (ctx.x), everything else as before (TIMELINE, LONG TIMELINE on STARS). "Before" = commit 1d37f4a9.
print('test 31: RA order of the 35 stars; SKY block on the 35 stars')
sys.path.insert(0, 'rebuild_kit')
import swisseph as swe, datetime
import celestial_bodies_swisseph as ENG
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe')); swe.set_topo(0, 51.5, 0)
era = {x: swe.fixstar2_ut(dict(ENG.BEHENIAN_STARS)[x], 2451545.0, ENG._FLAG)[0][0] for x in JT.T1_T2_T24_STARS}
check('T31 T1_T2_T24_STARS = the 67 stars (35 until 20 Oct 2026, 46 until 21 Oct) sorted by engine J2000 RA at J2000.0 (Alpheratz 2.10 ... Markab 346.19)',
      JT.T1_T2_T24_STARS == sorted(era, key=era.get) and len(era) == 67,
      ', '.join(f'{x} {era[x]:.2f}' for x in JT.T1_T2_T24_STARS[:3]) + ' ... ' + f'Markab {era["Markab"]:.2f}')
sky_star_rows = lambda w: [x[1].split(' → S ')[1] for x in w['SKY JUPITER'].iter_rows(values_only=True)
                           if x[0] == 'SKY' and x[1] and ' → S ' in str(x[1]) and x[1].split(' → S ')[1] in set(JT.STARS) | set(JT.T1_T2_T24_STARS)]
lfw = openpyxl.load_workbook(lf)
ok, det = True, []
for nm, w, nst in (('Ascot', gw, 67), ('Lingfield', lfw, 21)):
    want = [x for x in JT.T1_T2_T24_STARS if nst == 67 or x in JT.STARS and x != 'Galactic Centre']
    got = {'SKY': sky_star_rows(w)}
    for sh in ['SKY JUPITER'] + runner_tabs(w):
        for x in w[sh].iter_rows(values_only=True):
            if x[0] in ('T1', 'T2') and x[1] and ' → ' in str(x[1]) and x[1].split(' → ')[1][2:] in JT.T1_T2_T24_STARS + ['Polaris']:
                got.setdefault(f'{sh} {x[0]}', []).append(x[1].split(' → ')[1][2:])
        for k, (hdr, rows) in t24_blocks(w[sh]).items():
            got[f'{sh} {k}'] = [lab.split(' ', 1)[1] for lab in rows]
    ok &= len(want) == nst and all(v == want for v in got.values()) and len(got) == 1 + 1 + 4 * len(runner_tabs(w))
    det.append(f'{nm} {len(got)} lists of {nst}')
check('T31 T1, T2, T24 SKY / HORSE / JOCKEY and SKY block star rows in RA order: rebuilt Ascot 67 (35 until 20 Oct 2026, 46 until 21 Oct), Lingfield 21 (its old batch: 22 stars '
      'with Polaris, no Galactic Centre)', ok, '; '.join(det))
# the build before (commit 1d37f4a9) and the comparison, both races (--full)
bf = 'tools/_jt_before_1d37f4a9.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '1d37f4a9:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
cmp = {}
for nm, inp, after in (('Lingfield', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_h),
                       ('Ascot', b35, gf35_h)):               # 35-star copy (20 Oct 2026), code of 93e73bc4
    bo = f'{tmp}/{nm}_before_jupiter_tables.xlsx'
    subprocess.run([sys.executable, bf, inp, '--full', '--out', bo], capture_output=True, text=True)
    r = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_raorder/compare_raorder.py', bo, after], capture_output=True, text=True)
    cmp[nm] = (r.stdout, bo)
os.remove(bf)
line = lambda out, k: next((l for l in out.splitlines() if l.startswith(k)), '')
check('T31 every T1 / T2 / T24 star row identical to the build before, matched by star (value, fill, comment, outline; only the order '
      'differs); the rest of the workbook identical apart from the SKY block star rows',
      all(line(o, 'differences beyond those:') == 'differences beyond those: 0' for o, _ in cmp.values())
      and line(cmp['Lingfield'][0], 'T1 / T2 / T24 star rows matched') == 'T1 / T2 / T24 star rows matched by label: 525'
      and line(cmp['Ascot'][0], 'T1 / T2 / T24 star rows matched') == 'T1 / T2 / T24 star rows matched by label: 175',
      ' | '.join(f"{n}: {line(o, 'T1 / T2 / T24')}; {line(o, 'differences')}" for n, (o, _) in cmp.items()))
sd = {n: line(o, 'SKY block star rows:') for n, (o, _) in cmp.items()}
check('T31 SKY block star rows vs before: Lingfield Polaris gone; Ascot Polaris gone + the 13 new stars; no other row changed',
      sd['Lingfield'] == "SKY block star rows: {'SKY JUPITER': {'gone': ['S Jupiter → S Polaris']}}"
      and "'gone': ['S Jupiter → S Polaris']" in sd['Ascot'] and 'changed' not in sd['Ascot']
      and all(f'S Jupiter → S {x}' in sd['Ascot'] for x in JT.NEW_STARS if x not in NEW11 + NEW21), str(sd)[:300])   # the 13 (35-star copy)
# 20 Oct 2026 (Eddie): the sky timelines now take their star events from the 35 stars (test 33): before minus the Polaris events = after
# minus the new-star events (section count rows left out)
tl = lambda f, drop: [x for x in openpyxl.load_workbook(f, read_only=True)['SKY JUPITER'].iter_rows(values_only=True)
                      if x and x[0] in ('TIMELINE', 'LONG TIMELINE') and not str(x[3] or '').startswith('———') and not drop(str(x))]
tls = {n: (tl(b, lambda t: 'Polaris' in t), tl(a, lambda t: bool(NEWRE.search(t))))
       for n, (b, a) in (('Lingfield', (cmp['Lingfield'][1], lf_h)), ('Ascot', (cmp['Ascot'][1], gf35_h)))}
check('T31 sky TIMELINE and LONG TIMELINE rows identical to the build before apart from the Polaris events (gone) and the new-star events '
      '(20 Oct 2026; both races)', all(b == a and b for b, a in tls.values()),
      ', '.join(f'{n} {len(a)} rows' for n, (b, a) in tls.items()))
# SKY block new-star cells = the T1 SKY cells (rebuilt Ascot)
sb = {x[1].value.split(' → S ')[1]: x for x in gw['SKY JUPITER'].iter_rows() if x[0].value == 'SKY' and x[1].value and ' → S ' in str(x[1].value)}
t1 = {x[1].value.split(' → H ')[1]: x for x in gw['P01'].iter_rows() if x[0].value == 'T1' and x[1].value and ' → H ' in str(x[1].value)}
sig = lambda cs: [c.value for c in cs] + [cs[0].fill.start_color.rgb if cs[0].fill and cs[0].fill.fill_type else None]
bad = [(x, pl) for x in JT.NEW_STARS for i, pl in enumerate(('RA', 'Dec'))
       if sig(sb[x][2 + 9 * i:11 + 9 * i]) != sig(t1[x][18 + 9 * i:27 + 9 * i])]
check('T31 every SKY block new-star cell on the rebuilt Ascot = the T1 SKY cell for the same star and plane (value, +5, target, group, '
      'offset, score, arrow, also, timing, fill)', not bad and len(JT.NEW_STARS) == 45, f'90 cell groups (13 + 11 + 21 stars); {bad[:3]}')
# two SKY block new-star cells by hand from POSITIONS (rates for +5 and timing; linear, off 2012-06-19 14:30)
off = datetime.datetime(2012, 6, 19, 14, 30)
cases = [  # (star, plane, value, target text, target, tol, score, timing text)
    ('Praesepe', 'RA', 70.378057, '70.7 (sqrt2)', 50 * 2 ** 0.5, 0.005 * 50 * 2 ** 0.5, 'sq', 'separating'),
    ('Kaus Australis', 'RA', 143.593046, '144.444 (ninth)', 1300 / 9, 0.944444, 'lin', 'applying'),
]
for star, pl, exp, tt, tv, tol, kind, way in cases:
    sj, sx = gp[('SKY', 'S', 'Jupiter')], gp[('SKY', 'S', star)]
    v0 = ra_d(sj[0], sx[0]); v5 = ra_d(sj[0] + 5 * rates['Jupiter'][0], sx[0] + 5 * rates[star][0])
    dev = abs(v0 - tv)
    sc = (10 * (tol - dev) / tol) ** 2 if kind == 'sq' else 100 * (tol - dev) / tol
    t = (tv - v0) / ((v5 - v0) / 5)
    clk = (off + datetime.timedelta(minutes=t)).strftime('%d %b %Y %H:%M')
    txt = f"{way}, exact {clk} ({abs(t):.1f} min {'ago' if t < 0 else ''})".replace(' )', ')') if t < 0 else f"{way}, exact {clk} (in {t:.1f} min)"
    x = sb[star]
    check(f'T31 SKY block S Jupiter → S {star} {pl} by hand from POSITIONS', abs(v0 - exp) < 1e-6 and x[2].value == round(v0, 6)
          and x[3].value == round(v5, 6) and x[4].value == tt and x[6].value == f'{v0 - tv:+.5f}' and f'{x[7].value:.2f}' == f'{sc:.2f}'
          and x[10].value == txt, f'{v0:.6f} -> {v5:.6f}; {x[4].value}, {x[6].value}, {x[7].value} (by hand {sc:.2f}); {x[10].value!r} vs {txt!r}')
# Test 32 (Eddie, 19 Oct 2026): T24 ratio tables - T24 H / J, T24 HORSE RATIOS, T24 JOCKEY RATIOS (natal; after T24 JOCKEY)
print('test 32: T24 H / J and T24 HORSE / JOCKEY RATIOS')
T24R = ('T24 H / J', 'T24 HORSE RATIOS', 'T24 JOCKEY RATIOS')


def t24r_read(ws):
    """{table: ([(column name, plane)], {row label: [cells]})}"""
    out, it, cur = {}, list(ws.iter_rows()), None
    for i, x in enumerate(it):
        t = x[0].value
        if t in T24R and str(x[1].value).startswith(t + ' ('):
            h1, h2, pl, cols, idx = it[i + 1], it[i + 2], None, [], []
            for c in range(2, len(h1)):
                pl = h1[c].value if h1[c].value in ('RA', 'Dec') else pl
                if h2[c].value:
                    cols.append((h2[c].value, pl)); idx.append(c)
            out[t] = (cols, {}); cur = (t, idx)
        elif t in T24R:
            out[t][1][x[1].value] = [x[c] for c in cur[1]]
    return out


fillrgb = lambda c: c.fill.start_color.rgb if c.fill and c.fill.fill_type else None
first = lambda c: c.comment.text.split('\n')[0] if c.comment else None
bad, nchk, nruns = [], 0, 0
for nm, w, nst in (('Ascot', gw, 67), ('Lingfield', lfw, 21)):
    for P in runner_tabs(w):
        nruns += 1
        nr, nb = t24r_read(w[P]), t24_blocks(w[P])
        stars = [x for x in JT.T1_T2_T24_STARS if nst == 67 or x in JT.STARS and x != 'Galactic Centre']
        if sorted(nr) != sorted(T24R):
            bad.append((nm, P, 'tables', list(nr))); continue
        hj_cols = [(n, pl) for pl in ('RA', 'Dec') for n in ('d(H star, H Jupiter)', 'd(J star, J Jupiter)', 'H / J')]
        if nr['T24 H / J'][0] != hj_cols or list(nr['T24 H / J'][1]) != stars:
            bad.append((nm, P, 'H / J layout'))
        for C, who in (('H', 'HORSE'), ('J', 'JOCKEY')):
            hdr, rows = nb[f'T24 {who}']
            bodies = [b for b, pl in hdr if pl == 'RA' and b != 'Jupiter']
            cols, rr = nr[f'T24 {who} RATIOS']
            if cols != [(b, pl) for pl in ('RA', 'Dec') for b in bodies] or list(rr) != [f'{C} {x}' for x in stars]:
                bad.append((nm, P, who, 'layout')); continue
            for x in stars:
                t24 = {k: c for k, c in zip(hdr, rows[f'{C} {x}'])}
                # T24 H / J distance cells = the T24 Jupiter cells (value, fill, first comment line)
                for pl in ('RA', 'Dec'):
                    c = nr['T24 H / J'][1][x][hj_cols.index((f'd({C} star, {C} Jupiter)', pl))]
                    j = t24[('Jupiter', pl)]
                    nchk += 1
                    if (c.value, fillrgb(c), first(c)) != (j.value, fillrgb(j), first(j)):
                        bad.append((nm, P, 'H / J dist', x, pl))
                # every RATIOS cell from the two T24 distances
                for k, (b, pl) in enumerate(cols):
                    c, dj, dx = rr[f'{C} {x}'][k], t24[('Jupiter', pl)].value, t24[(b, pl)].value
                    nchk += 1
                    if min(dj, dx) < (1.5 if pl == 'RA' else 0.3):
                        if c.value != 'together' or fillrgb(c):
                            bad.append((nm, P, who, x, b, pl, 'together')); 
                        continue
                    r = max(dj, dx) / min(dj, dx)
                    if not isinstance(c.value, float) or abs(c.value - r) > r * 1e-6 * (1 / dj + 1 / dx) + 2e-6:
                        bad.append((nm, P, who, x, b, pl, c.value, r))
            # H / J ratio from its two distance cells
        for x in stars:
            for pl in ('RA', 'Dec'):
                row_ = nr['T24 H / J'][1][x]
                dh, dj_, c = (row_[hj_cols.index((n, pl))] for n in ('d(H star, H Jupiter)', 'd(J star, J Jupiter)', 'H / J'))
                nchk += 1
                if min(dh.value, dj_.value) < (1.5 if pl == 'RA' else 0.3):
                    ok_ = c.value == 'together'
                else:
                    r = max(dh.value, dj_.value) / min(dh.value, dj_.value)
                    ok_ = isinstance(c.value, float) and abs(c.value - r) <= r * 1e-6 * (1 / dh.value + 1 / dj_.value) + 2e-6
                if not ok_:
                    bad.append((nm, P, 'H / J ratio', x, pl, c.value))
check('T32 layout and every distance: rows = T1_T2_T24_STARS in order (Ascot 35, Lingfield 21), columns RA then Dec (H / J: d(H star, H '
      'Jupiter), d(J star, J Jupiter), H / J; RATIOS: the T24 bodies without Jupiter); H / J distance cells = the T24 Jupiter cells (value, '
      'fill, comment); every ratio = larger / smaller of the T24 distances, "together" where one is within RA 1.5 / Dec 0.3',
      not bad and nruns == 7, f'{nruns} runner sheets, {nchk} cells; {bad[:3]}')
# T24 H / J for the old stars = the T23 H / J star cells (value, interval, score)
bad, n23 = [], 0
for nm, w in (('Ascot', gw), ('Lingfield', lfw)):
    for P in runner_tabs(w):
        hj = t24r_read(w[P])['T24 H / J']
        for x in w[P].iter_rows(values_only=True):
            if x[0] != 'T23' or x[1] not in hj[1]:
                continue
            for i, pl in enumerate(('RA', 'Dec')):
                col = JT.t23_rcol(i, 0) - 1
                c = hj[1][x[1]][hj[0].index(('H / J', pl))]
                n23 += 1
                if str(x[col + 2] or '').startswith('together'):
                    ok_ = c.value == 'together'
                else:
                    t23_int = str(x[col + 2]).split(' · ')[0]
                    cm = first(c)
                    new_int = cm.replace('nearest: ', '').split(' · ')[0]
                    sc = None if 'outside' in cm else float(cm.split(' · ')[-1])
                    ok_ = c.value == x[col] and t23_int == new_int and sc == x[col + 5]
                if not ok_:
                    bad.append((nm, P, x[1], pl, x[col], x[col + 2], x[col + 5], c.value, first(c)))
check('T32 T24 H / J ratio of every old star = the T23 H / J star cell (value, interval, score; together alike), Ascot + Lingfield every runner',
      not bad and n23 > 0, f'{n23} cells; {bad[:3]}')
# by hand from POSITIONS (rebuilt Ascot P01)
nr = t24r_read(gw['P01'])
col_ = lambda t, n, pl: nr[t][0].index((n, pl))
pct = lambda v, t: (v / t - 1) * 100
cases = [  # (table, row label, column, plane, chart, star, X (second point), interval, comment by hand)
    ('T24 H / J', 'Deneb', 'H / J', 'RA', None, 'Deneb', None, 1.25,
     lambda v: f'5/4 · major third · Imperfect · B · {pct(v, 1.25):+.5f}% · {sq(0.2, abs(pct(v, 1.25))):.2f}'),
    ('T24 H / J', 'Altair', 'H / J', 'RA', None, 'Altair', None, 1.5, lambda v: f'nearest: 3/2 · fifth — outside · {v - 1.5:+.5f}'),
    ('T24 H / J', 'Vega', 'H / J', 'Dec', None, 'Vega', None, 1.0, lambda v: f'1 · unison · Perfect · A · {v - 1:+.5f} · {sq(0.02, abs(v - 1)):.2f}'),
    ('T24 HORSE RATIOS', 'H Algol', 'Sun', 'RA', 'H', 'Algol', 'Sun', 1.5, lambda v: f'3/2 · fifth · Perfect · A · {v - 1.5:+.5f} · {sq(0.02, abs(v - 1.5)):.2f}'),
    ('T24 HORSE RATIOS', 'H Denebola', 'Uranus', 'RA', 'H', 'Denebola', 'Uranus', PHI,
     lambda v: f'φ · golden ratio · Phi · φ and √2 · {pct(v, PHI):+.5f}% · {sq(0.15, abs(pct(v, PHI))):.2f}'),
    ('T24 JOCKEY RATIOS', 'J Bellatrix', 'Makemake', 'RA', 'J', 'Bellatrix', 'Makemake', 2.0,
     lambda v: f'2 · octave · Perfect · A · {v - 2:+.5f} · {sq(0.02, abs(v - 2)):.2f}'),
    ('T24 JOCKEY RATIOS', 'J Alkaid', 'Gonggong', 'Dec', 'J', 'Alkaid', 'Gonggong', 1.0,
     lambda v: f'1 · unison · Perfect · A · {v - 1:+.5f} · {sq(0.02, abs(v - 1)):.2f}'),
]
colour_of = lambda sc: GREEN if sc >= 80 else YELLOW if sc >= 50 else LIGHT
for t, lab, cn, pl, C, star, X, tv, want in cases:
    if C is None:                                          # T24 H / J: d(H star, H Jupiter) / d(J star, J Jupiter); q = d(H Jup, J Jup) / smaller
        a, b = dist(gp[('P01', 'H', star)], gp[('P01', 'H', 'Jupiter')], pl), dist(gp[('P01', 'J', star)], gp[('P01', 'J', 'Jupiter')], pl)
        qd, close = dist(gp[('P01', 'H', 'Jupiter')], gp[('P01', 'J', 'Jupiter')], pl), 'H–J Jupiters'
    else:                                                  # RATIOS: d(star, Jupiter) / d(star, X); q = d(Jupiter, X) / smaller
        a, b = dist(gp[('P01', C, star)], gp[('P01', C, 'Jupiter')], pl), dist(gp[('P01', C, star)], gp[('P01', C, X)], pl)
        qd, close = dist(gp[('P01', C, 'Jupiter')], gp[('P01', C, X)], pl), 'Jupiter–X'
    v = max(a, b) / min(a, b)
    w_ = want(v)
    q = qd / min(a, b)
    if tv == 1.0 and 0.0015 <= q < 0.02:
        w_ += f'\n{close} assisted (q {q:.6f})'
    c = nr[t][1][lab][col_(t, cn, pl)]
    sc = None if 'outside' in w_ else float(w_.split('\n')[0].split(' · ')[-1])
    check(f'T32 {t} {lab} {cn} {pl} by hand from POSITIONS', c.value == round(v, 6) and c.comment.text == w_
          and fillrgb(c) == (colour_of(sc) if sc is not None else None),
          f'{a:.6f} / {b:.6f} = {v:.6f}; q {q:.6f}; {c.comment.text!r} vs {w_!r}; {fillrgb(c)}')
a = dist(gp[('P01', 'H', 'Nunki')], gp[('P01', 'H', 'Jupiter')], 'RA')
c = nr['T24 H / J'][1]['Nunki'][col_('T24 H / J', 'H / J', 'RA')]
w_ = f'together (RA < 1.5): H Nunki, H Jupiter {a:.6f} — no ratio, no score'
check('T32 T24 H / J Nunki RA together by hand from POSITIONS (d(H Nunki, H Jupiter) RA < 1.5): "together", no fill, the leg named',
      a < 1.5 and c.value == 'together' and not fillrgb(c) and c.comment.text == w_, f'{a:.6f}; {c.value!r}, {c.comment.text!r}')
# automatic / assisted found by the rule: counts over both races (none automatic in these two races)
cnt = {}
for nm, w in (('Ascot', gw), ('Lingfield', lfw)):
    for P in runner_tabs(w):
        for t, (cols, rr) in t24r_read(w[P]).items():
            for cs in rr.values():
                for c in cs:
                    tx = c.comment.text if c.comment else ''
                    k = (nm, 'automatic' if 'automatic (' in tx else 'assisted' if ' assisted (q ' in tx else None)
                    if k[1]:
                        cnt[k] = cnt.get(k, 0) + 1
                        if k[1] == 'automatic' and fillrgb(c) != '00D9D9D9':
                            bad.append(('automatic not grey', nm, P))
check('T32 automatic / assisted unisons by the rule: automatic none in either race; assisted Ascot 43 (H / J 30, HORSE 2, JOCKEY 11; 25 on 35 stars, '
      '29 on 46), Lingfield 156', cnt == {('Ascot', 'assisted'): 43, ('Lingfield', 'assisted'): 156}, str(cnt))
# every other sheet and row identical to the build before (commit 10b7d76a), both races, --full
bf = 'tools/_jt_before_10b7d76a.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '10b7d76a:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
res = {}
for nm, inp, after in (('Lingfield', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_h),
                       ('Ascot', b35, gf35_h)):               # 35-star copy (20 Oct 2026), code of 93e73bc4
    bo = f'{tmp}/{nm}_before32_jupiter_tables.xlsx'
    subprocess.run([sys.executable, bf, inp, '--full', '--out', bo], capture_output=True, text=True)
    r = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_t24r/compare_t24r.py', bo, after], capture_output=True, text=True)
    res[nm] = line(r.stdout, 'sheets')
os.remove(bf)
check('T32 every other sheet and row identical to the build before (commit 10b7d76a; values, fills, comments; the new block cut out), both races',
      all(v.endswith('differences outside the new tables: 0') for v in res.values()) and len(res) == 2, str(res))
# Test 33 (Eddie, 20 Oct 2026): SKY STARS and the sky TIMELINE / LONG TIMELINE on the 35 stars (ctx.x); everything else unchanged
print('test 33: SKY STARS and the sky timelines on the 35 stars')
import itertools
SS_ORDER = [x for x in JT.STARS if x in JT.T1_T2_T24_STARS] + [x for x in JT.T1_T2_T24_STARS if x not in JT.STARS]


def pos_ctx(w, off):
    """a Ctx from the POSITIONS sky rows (positions and rates at the off), for the listing rule"""
    sky, rt = {}, {}
    for x in w['POSITIONS'].iter_rows(min_row=5, values_only=True):
        if x and x[0] == 'SKY' and x[3]:
            sky[x[3]] = (x[5], x[6], x[4]); rt[x[3]] = None if x[7] in (None, 'n/a') else (x[7], x[8])
    c = JT.Ctx(sky, rt); c.off = off; c.off_str = off.strftime('%Y-%m-%d %H:%M')
    return c


def ss_rows(w):
    blk, out = None, {}
    for x in w['SKY JUPITER'].iter_rows(values_only=True):
        if x and str(x[0] or '').startswith('SKY STARS') and x[1] is None:
            blk = x[0]
        elif x and x[0] == 'SKY STARS':
            out[(x[2], x[3])] = (blk, x)
    return out


bad, det = [], []
for nm, w, off, nst in (('Ascot', gw, datetime.datetime(2012, 6, 19, 14, 30), 67), ('Lingfield', lfw, datetime.datetime(2021, 4, 2, 14, 35), 21)):
    cx = pos_ctx(w, off)
    stars = [x for x in SS_ORDER if x in cx.S0]
    rows = JT.pair_rows(cx, {'H': {}, 'J': {}}, stars, tid='SKY STARS', sky=True)
    jd = cx.S0['Jupiter'][1]
    want_cand = {(f'S {a} – S {b}', pl) for a, b in itertools.combinations(stars, 2) for pl in ('RA', 'Dec', 'Equator')
                 if pl != 'Equator' or not ((jd >= 0) == (cx.S0[a][1] >= 0) == (cx.S0[b][1] >= 0))}
    got_cand = {(h['pair'], h['plane']) for h in rows}
    rule = {(h['pair'], h['plane']) for h in rows if not h['together'] and (h['ev'] or h['mid'] is not None or h['allfam'])}
    sheet = ss_rows(w)
    ok_ = len(stars) == nst and got_cand == want_cand and set(sheet) == rule and not any('Polaris' in k[0] for k in sheet)
    bad += [] if ok_ else [(nm, len(stars), len(got_cand ^ want_cand), sorted(set(sheet) ^ rule)[:3])]
    det.append(f'{nm} {nst} stars, {len(want_cand)} pair-planes, {len(rule)} listed')
check('T33 SKY STARS complete: every pair of the batch\'s stars (67 / 21, no Polaris; 35 until 20 Oct 2026, 46 until 21 Oct) and plane (Equator: straddle) measured, and the rows '
      'on the sheet = exactly those passing the filter (ratio on an interval, midpoint hit, or all three families; together out)',
      not bad, '; '.join(det) + f' {bad[:2]}')
# against the build before (commit bb23ade2): old-star rows unchanged, Polaris rows / events gone, new-star rows / events added, rest identical
bf = 'tools/_jt_before_bb23ade2.py'
open(bf, 'w').write(subprocess.run(['git', 'show', 'bb23ade2:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
out33 = {}
for nm, inp, after in (('Lingfield', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_h),
                       ('Ascot', b35, gf35_h)):               # 35-star copy (20 Oct 2026), code of 93e73bc4
    bo = f'{tmp}/{nm}_before33_jupiter_tables.xlsx'
    subprocess.run([sys.executable, bf, inp, '--full', '--out', bo], capture_output=True, text=True)
    out33[nm] = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_sky35/compare_sky35.py', bo, after], capture_output=True, text=True).stdout
os.remove(bf)
ok_ = True
for nm, o in out33.items():
    ls = o.splitlines()
    ok_ &= ('old rows changed: 0 []' in line(o, '  gone') and 'all Polaris: True' in line(o, '  gone') and 'all with a new star: True' in line(o, '  gone')
            and all(l.endswith('True') for l in ls if l.startswith(('   - gone', '   + new ')))
            and not any(l.startswith('   ~ changed') for l in ls)
            and all(', changed 0' in l for l in ls if l.startswith(('TIMELINE:', 'LONG TIMELINE:')))
            and line(o, 'differences outside') == 'differences outside SKY STARS / TIMELINE / LONG TIMELINE: 0 []')
check('T33 against the build before (commit bb23ade2): every old-star SKY STARS row identical (cells, fills, block); the rows dropped all '
      'Polaris, the rows added all with a new star; TIMELINE / LONG TIMELINE: events dropped all Polaris, added all new-star, every other event '
      'unchanged (time, cells, also); every other row of every sheet identical (both races)', ok_,
      ' | '.join(f"{n}: {line(o, 'SKY STARS rows per area')[24:]}; {line(o, 'TIMELINE:')}; {line(o, 'LONG TIMELINE:')}" for n, o in out33.items()))
# new-star events: exact time = the source cell's timing; beyond 60 min the real time re-searched with the engine
A_OFF = datetime.datetime(2012, 6, 19, 14, 30)
JA = EN._to_jd_ut(EN._parse_time('2012-06-19 14:30', 'Europe/London'))
SA = _site
ba = EN.bodies_at(JA, *SA, False)
skp = {x[3]: x for x in gw['POSITIONS'].iter_rows(min_row=5, values_only=True) if x and x[0] == 'SKY' and x[3]}
ecache = {}


def eng(m):
    if m not in ecache:
        ecache[m] = EN.bodies_at(JA + m / 1440.0, *SA, False)
    return ecache[m]


def sky_at(p, m):
    eb = p + '_B' if skp[p][4] == 'star' else p
    b = eng(m)
    return ((skp[p][5] + (b[eb]['ra'] - ba[eb]['ra'] + 180) % 360 - 180) % 360, skp[p][6] + b[eb]['dec'] - ba[eb]['dec'])


def pdist(p, q, pl):
    if pl == 'RA':
        return ra_d(p[0], q[0])
    return abs(p[1] - q[1]) if pl == 'Dec' else abs(abs(p[1]) - abs(q[1]))


ss = ss_rows(gw)
tlr = [x for x in gw['SKY JUPITER'].iter_rows(values_only=True) if x and x[0] in ('TIMELINE', 'LONG TIMELINE') and x[4] and NEWRE.search(str(x[4]))]
bad, nreal, nnf = [], 0, 0
for e in tlr:
    rel, pl, kind, tv = e[4], e[5], e[6], e[8]
    if kind in ('ratio', 'midpoint'):                      # 22 Oct 2026: a midpoint event (unison) of a SKY STARS row, e.g. ONC – Phact (LONG >= 90)
        a, b = rel.split(': ')[1].split(' – ')
        src = ss[(f'{a} – {b}', pl)][1][14]                 # ratio timing cell
        # orientation fixed at the off, as the table (21 Oct 2026: larger / smaller can never cross a unison)
        big = pdist(sky_at('Jupiter', 0), sky_at(a[2:], 0), pl) >= pdist(sky_at('Jupiter', 0), sky_at(b[2:], 0), pl)
        f = lambda m: (lambda dx, dy: (dx / dy if big else dy / dx) - tv)(*(pdist(sky_at('Jupiter', m), sky_at(z[2:], m), pl) for z in (a, b)))
    elif ' → ' in rel:                                     # a S Jupiter leg of a SKY STARS row (20 Oct 2026: e.g. S Jupiter → S Menkent)
        a, b = rel.split(' → ')
        r_ = next(r for k, (_, r) in ss.items() if k[1] == pl and re.search(rf'{re.escape(b)}( –|$)', k[0]))
        src = r_[5] if r_[2].startswith(b + ' –') else r_[7]
        f = lambda m: pdist(sky_at('Jupiter', m), sky_at(b[2:], m), pl) - tv
    else:
        a, b = rel.split(' – ')
        r_ = next(r for k, (_, r) in ss.items() if k[1] == pl and a in k[0] and b in k[0])
        src = r_[9] if f'{a} – {b}' == r_[2] else None     # d(X, Y) family cell: '→ T (fam, sc) · timing'
        f = lambda m: pdist(sky_at(a[2:], m), sky_at(b[2:], m), pl) - tv
    if e[1] == 'not within 1 year':
        nnf += 1
        days = [f(d * 1440) for d in range(-366, 367)]
        ok_ = all((x > 0) == (days[0] > 0) for x in days)
    elif e[0] == 'TIMELINE' or abs(e[13]) <= 60:
        mins = e[2] if e[0] == 'TIMELINE' else e[13]
        ok_ = src and f'exact {e[1]}' in src and f'{abs(mins):.1f} min' in src
    else:
        nreal += 1
        ok_ = f(e[13] - 1) * f(e[13] + 1) < 0
    if not ok_:
        bad.append((e[0], rel, pl, e[1], e[2], src))
check('T33 every new-star event on the rebuilt Ascot: within 60 min the exact time = its SKY STARS source cell\'s timing; beyond 60 min the '
      'real time re-searched with the engine (the value crosses the target between one minute before and after; "not within 1 year": no '
      'crossing in a daily scan of ±1 year)', not bad and len(tlr) > 0, f'{len(tlr)} event rows, {nreal} real times, {nnf} not within 1 year; {bad[:3]}')
# by hand from POSITIONS (rates for +5): two new-star SKY STARS rows, the TIMELINE event, the LONG TIMELINE event
for a, b, pl, area, tv, tt, kind in (('Algol', 'Sadalsuud', 'Equator', 'A', 1.5, '3/2 · fifth · Perfect', 'abs'),
                                     ('Vega', 'Nunki', 'Dec', 'φ and √2', 1 + 2 ** 0.5, '1+√2 · silver ratio · Phi', 'pct')):
    J0, J5 = gp[('SKY', 'S', 'Jupiter')], (gp[('SKY', 'S', 'Jupiter')][0] + 5 * rates['Jupiter'][0], gp[('SKY', 'S', 'Jupiter')][1] + 5 * rates['Jupiter'][1])
    X0, Y0 = gp[('SKY', 'S', a)], gp[('SKY', 'S', b)]
    X5, Y5 = ((p[0] + 5 * rates[z][0], p[1] + 5 * rates[z][1]) for p, z in ((X0, a), (Y0, b)))
    dx, dy, dxy = pdist(J0, X0, pl), pdist(J0, Y0, pl), pdist(X0, Y0, pl)
    r0 = max(dx, dy) / min(dx, dy)
    r5 = (pdist(J5, X5, pl) / pdist(J5, Y5, pl)) if dx > dy else (pdist(J5, Y5, pl) / pdist(J5, X5, pl))
    off_ = r0 - tv if kind == 'abs' else (r0 / tv - 1) * 100
    sc = sq(0.02, abs(off_)) if kind == 'abs' else sq(0.15, abs(off_))
    t = (tv - r0) / ((r5 - r0) / 5)
    clk = (A_OFF + datetime.timedelta(minutes=t)).strftime('%H:%M')
    tim = f"{'applying' if t > 0 else 'separating'}, exact {clk} (in {t:.1f} min)" if t > 0 else f"separating, exact {clk} ({-t:.1f} min ago)"
    pos_ = 'between' if abs(dxy - (dx + dy)) <= 0.01 * (dx + dy) else 'far side'
    blk, x = ss[(f'S {a} – S {b}', pl)]
    offt = f'{off_:+.5f}' + ('%' if kind == 'pct' else '')
    check(f'T33 SKY STARS S {a} – S {b} {pl} by hand from POSITIONS', [round(v, 6) for v in (dx, dy, dxy, r0)] == [x[4], x[6], x[8], x[10]]
          and x[11] == tt and x[12] == offt and f'{x[13]:.2f}' == f'{sc:.2f}' and x[14] == tim and x[15] == pos_ and area.upper() in blk.upper(),
          f'{dx:.6f} / {dy:.6f} / {dxy:.6f}, ratio {r0:.6f} -> {r5:.6f}, {tt} {offt} ({sc:.2f}), {tim}, {pos_}; {blk[:30]}; sheet {x[10:16]}')
ev = [x for x in gw['SKY JUPITER'].iter_rows(values_only=True) if x and x[0] == 'TIMELINE' and x[4] == 'S Jupiter: S Vega – S Nunki']
check('T33 TIMELINE new-star event S Jupiter: S Vega – S Nunki Dec 1+√2, exact 14:32 (+2.8 min), applying, 99.13 - inside −30 / +60',
      len(ev) == 1 and ev[0][1:4] == ('14:32', 2.8, 'SKY STARS') and ev[0][5] == 'Dec' and ev[0][10] == 99.13 and ev[0][11] == 'applying', str(ev))
lv = [x for x in gw['SKY JUPITER'].iter_rows(values_only=True) if x and x[0] == 'LONG TIMELINE' and x[4] == 'S Jupiter: S Pleiades – S Nunki']
fpn = lambda m: (lambda dx, dy: max(dx, dy) / min(dx, dy) - 1.5)(*(pdist(sky_at('Jupiter', m), sky_at(z, m), 'Equator') for z in ('Pleiades', 'Nunki')))
check('T33 LONG TIMELINE new-star event S Jupiter: S Pleiades – S Nunki Equator 3/2 (95.80 at the off): real 12:29 (−120.9 min) by the engine, '
      'linear 12:28 (−121.1 min); direct engine lookup: the ratio crosses 3/2 between one minute before and after',
      len(lv) == 1 and lv[0][1] == '12:29' and lv[0][13] == -120.9 and lv[0][14] == '12:28 (-121.1 min)' and lv[0][10] == 95.8
      and fpn(-121.9) * fpn(-119.9) < 0, f'{lv[0][:15] if lv else lv}; {fpn(-121.9):+.7f} {fpn(-119.9):+.7f}')
# Test 34 (Eddie, 20 Oct 2026): 11 more stars (Alpheratz, Algenib, Difda, Mirach, Menkar = alpha Ceti, Phact, Adhara, Wezen, Menkent,
# Unukalhai, Rasalhague); T1_T2_T24_STARS 46 in engine RA order, the same tables as the 13; everything else unchanged. "Before" = 7d88f329.
print('test 34: 11 more stars (46 in T1, T2, T24, T24 ratio tables, SKY block, SKY STARS, sky timelines)')
NEW11 = ['Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Menkar', 'Phact', 'Adhara', 'Wezen', 'Menkent', 'Unukalhai', 'Rasalhague']
CAT11 = {'Alpheratz': (2.097, 29.090), 'Algenib': (3.309, 15.184), 'Difda': (10.897, -17.987), 'Mirach': (17.433, 35.621),
         'Menkar': (45.570, 4.090), 'Phact': (84.912, -34.074), 'Adhara': (104.656, -28.972), 'Wezen': (107.098, -26.393),
         'Menkent': (211.671, -36.370), 'Unukalhai': (236.067, 6.426), 'Rasalhague': (263.734, 12.560)}
EXPECT46 = ['Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Hamal', 'Menkar', 'Algol', 'Pleiades', 'Aldebaran', 'Rigel', 'Capella', 'Bellatrix',
            'Phact', 'Betelgeuse', 'Sirius', 'Adhara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Praesepe', 'Regulus', 'Denebola', 'Algorab',
            'Spica', 'Alkaid', 'Menkent', 'Arcturus', 'Zubenelgenubi', 'Zubeneschamali', 'Alphecca', 'Unukalhai', 'Antares', 'Rasalhague',
            'Galactic Centre', 'Kaus Australis', 'Vega', 'Nunki', 'Altair', 'Deneb', 'Sadalsuud', 'Deneb Algedi', 'Sadalmelik', 'Fomalhaut',
            'Scheat', 'Markab']
B46 = dict(ENG.BEHENIAN_STARS)
e11 = {x: swe.fixstar2_ut(B46[x], 2451545.0, ENG._FLAG) for x in NEW11}
off11 = {x: (e11[x][0][0] - CAT11[x][0], e11[x][0][1] - CAT11[x][1]) for x in NEW11}
check('T34 engine: the 11 stars at J2000.0 within 0.02° of the catalogue (largest Adhara dRA +0.0070); Menkar looked up as ",alCet" = alpha '
      'Ceti (plain "Menkar" would give lambda Ceti, Dec +8.9)', all(abs(a) < 0.02 and abs(b) < 0.02 for a, b in off11.values())
      and B46['Menkar'] == ',alCet' and e11['Menkar'][1] == 'Menkar,alCet' and e11['Difda'][1] == 'Difda,beCet' and e11['Algenib'][1] == 'Algenib,gaPeg',
      ', '.join(f'{x} {a:+.4f}/{b:+.4f}' for x, (a, b) in off11.items()) + f'; Menkar -> {e11["Menkar"][1]} {e11["Menkar"][0][1]:+.4f}')
era46 = {x: swe.fixstar2_ut(B46[x], 2451545.0, ENG._FLAG)[0] for x in EXPECT46}
check('T34 T1_T2_T24_STARS = the 46 stars (|Dec| <= 50, no Polaris) sorted by engine J2000 RA at J2000.0 = Eddie\'s list (no pair differs)',
      [x for x in JT.T1_T2_T24_STARS if x in EXPECT46] == EXPECT46 == sorted(EXPECT46, key=lambda x: era46[x][0]) and all(abs(era46[x][1]) <= 50 for x in EXPECT46),
      ', '.join(f'{x} {era46[x][0]:.2f}' for x in EXPECT46[:6]) + ' ...')
# the 46 in order in every table that uses the list (46-star copy of the rebuilt Ascot since 21 Oct 2026; Lingfield 21)
ok, det = True, []
for nm, w, nst in (('Ascot', gw46, 46), ('Lingfield', lfw, 21)):
    want = [x for x in EXPECT46 if nst == 46 or x in JT.STARS and x != 'Galactic Centre']
    got = {'SKY': sky_star_rows(w)}
    for sh in ['SKY JUPITER'] + runner_tabs(w):
        for x in w[sh].iter_rows(values_only=True):
            if x[0] in ('T1', 'T2') and x[1] and ' → ' in str(x[1]) and x[1].split(' → ')[1][2:] in JT.T1_T2_T24_STARS + ['Polaris']:
                got.setdefault(f'{sh} {x[0]}', []).append(x[1].split(' → ')[1][2:])
        for k, (hdr, rows) in t24_blocks(w[sh]).items():
            got[f'{sh} {k}'] = [lab.split(' ', 1)[1] for lab in rows]
        for k, (cols, rows) in t24r_read(w[sh]).items():
            got[f'{sh} {k}'] = [lab.split(' ', 1)[1] if k != 'T24 H / J' else lab for lab in rows]
    ok &= len(want) == nst and all(v == want for v in got.values()) and len(got) == 1 + 1 + 7 * len(runner_tabs(w))
    det.append(f'{nm} {len(got)} lists of {nst}')
check('T34 the 46 (Ascot) / 21 (Lingfield) in RA order in T1, T2, T24 SKY / HORSE / JOCKEY, T24 H / J, T24 HORSE / JOCKEY RATIOS and the SKY block',
      ok, '; '.join(det))
# against the build before (commit 7d88f329): the after workbook minus the rows naming one of the 11 = the before workbook, row for row
# (values, fills, comments), except title rows with counts; the 11 only in the allowed tables; pairs workbooks identical
bf = 'tools/_jt_before_7d88f329.py'
open(bf, 'w').write(subprocess.run(['git', 'show', '7d88f329:tools/jupiter_tables.py'], capture_output=True, text=True).stdout)
out34 = {}
for nm, inp, after, apairs in (('Lingfield', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf_h, lf.replace('_jupiter_tables', '_pairs')),
                               ('Ascot', b46, gf_h, gf.replace('_jupiter_tables', '_pairs'))):     # 46-star copy (21 Oct 2026)
    bo = f'{tmp}/{nm}_before34_jupiter_tables.xlsx'
    subprocess.run([sys.executable, bf, inp, '--full', '--out', bo], capture_output=True, text=True)
    o = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_stars46/compare_46.py', bo, after], capture_output=True, text=True).stdout
    pw = [openpyxl.load_workbook(p, read_only=True) for p in (bo.replace('_jupiter_tables', '_pairs'), apairs)]
    psame = pw[0].sheetnames == pw[1].sheetnames and all(vals(pw[0][s]) == vals(pw[1][s]) for s in pw[0].sheetnames)
    out34[nm] = (o, psame)
os.remove(bf)
ALLOW = {'POSITIONS': {'SKY', 'P01'}, 'SKY JUPITER': {'SKY', 'SKY STARS', 'T24', 'TIMELINE', 'LONG TIMELINE'},
         'P01': {'T1', 'T2', 'T24', 'T24 H / J', 'T24 HORSE RATIOS', 'T24 JOCKEY RATIOS'}}
rem = {}
for l in out34['Ascot'][0].splitlines():
    m = re.match(r'(.+?): rows before \d+, after \d+, new-star rows (\d+) (\{.*?\});', l)
    if m:
        rem[m.group(1)] = (int(m.group(2)), set(eval(m.group(3))))
ok_ = (all(line(o, 'sheets with differences other than title rows:') == 'sheets with differences other than title rows: 0' and ps for o, ps in out34.values())
       and all(n == 0 or ids <= ALLOW.get(sh, set()) for sh, (n, ids) in rem.items())
       and not any('new-star rows 0 {}' not in l for l in out34['Lingfield'][0].splitlines() if ': rows before' in l))
check('T34 against the build before (commit 7d88f329), both races --full: every row not naming one of the 11 identical (values, fills, '
      'comments) - the earlier 35 stars\' rows, SKY STARS pairs and timeline events included - only count titles differ; the 11 only in '
      'POSITIONS, T1, T2, T24, T24 H / J, T24 RATIOS, the SKY block, SKY STARS, TIMELINE, LONG TIMELINE; pairs workbooks identical; '
      'Lingfield (old batch) gains nothing', ok_,
      f"Ascot new-star rows { {k: v for k, v in rem.items() if v[0]} }; pairs identical {[ps for _, ps in out34.values()]}")
# TIMELINE / LONG TIMELINE = before plus the new-star events (count titles)
tlt = lambda w: [str(x[0]) for x in w['SKY JUPITER'].iter_rows(values_only=True) if x and str(x[0] or '').startswith(('TIMELINE (', 'LONG TIMELINE ('))]
tln = lambda w, t: sum(1 for x in w['SKY JUPITER'].iter_rows(values_only=True) if x and x[0] == t and x[4] and re.search(r'\b(' + '|'.join(NEW11) + r')\b', str(x[4])))
check('T34 rebuilt Ascot: TIMELINE 38 -> 50 events (12 new-star; 12 before the off, 4 in the first 5 min, 34 after), LONG TIMELINE 47 -> 67 '
      '(20 new-star; 33 separating, 34 applying; built by the code of 18aff98a, LONG >= 80)', tln(gw46_s, 'TIMELINE') == 12 and tln(gw46_s, 'LONG TIMELINE') == 20
      and tlt(gw46_s)[0].endswith('50 events, 12 before the off, 4 in the first 5 min, 34 after') and tlt(gw46_s)[1].endswith('67 events, 33 separating, 34 applying'),
      f"{tln(gw46_s, 'TIMELINE')} / {tln(gw46_s, 'LONG TIMELINE')}; {tlt(gw46_s)[0][-70:]}; {tlt(gw46_s)[1][-40:]}")
# by hand from POSITIONS (rebuilt Ascot): two cells each of T1, T2, T24 (one ratio table cell), the SKY block and SKY STARS; Menkar in each table
NT = {122.222: 0.722222, 13.3333: 0.083333}                 # the _NINTH_RANGES tolerances of these two bands
cases = [  # (table, chart, star, plane, column, value, target text, offset, score by hand, fill)
    ('T1', 'H', 'Menkar', 'RA', 2, 122.563385, '122.222 (ninth)', lambda v: v - 1100 / 9, lambda v: 100 * (0.722222 - abs(v - 1100 / 9)) / 0.722222, YELLOW),
    ('T1', 'H', 'Adhara', 'Dec', 10, 6.184544, '10×φ^-1 (phi power)', lambda v: v - 10 / PHI, lambda v: sq(0.005 * 10 / PHI, abs(v - 10 / PHI)), YELLOW),
    ('T2', 'J', 'Rasalhague', 'Dec', 10, 36.018968, '36 (whole)', lambda v: v - 36, lambda v: sq(0.02, abs(v - 36)), LIGHT),
]
for tid, C, star, pl, c0, exp, tt, off, sc, fill in cases:
    x = row(gw46['P01'], tid, f'{C} Jupiter → {C} {star}')
    v = dist(gp[('P01', C, 'Jupiter')], gp[('P01', C, star)], pl)
    got_fill = x[c0].fill.start_color.rgb if x[c0].fill and x[c0].fill.fill_type else None
    check(f'T34 {tid} {C} Jupiter → {C} {star} {pl} by hand from POSITIONS', abs(v - exp) < 1e-6 and x[c0].value == round(v, 6)
          and x[c0 + 2].value == tt and x[c0 + 4].value == f'{off(v):+.5f}' and f'{x[c0 + 5].value:.2f}' == f'{sc(v):.2f}' and got_fill == fill,
          f'{v:.6f}; {x[c0 + 2].value}, {x[c0 + 4].value}, {x[c0 + 5].value} (by hand {sc(v):.2f}), {got_fill}')
# T2's SKY cell S Jupiter → S Unukalhai Dec (the J Unukalhai row), +5 min from the POSITIONS rates
x = row(gw46['P01'], 'T2', 'J Jupiter → J Unukalhai')
sj, su = gp[('SKY', 'S', 'Jupiter')], gp[('SKY', 'S', 'Unukalhai')]
v0, v5 = abs(sj[1] - su[1]), abs(sj[1] + 5 * rates['Jupiter'][1] - su[1] - 5 * rates['Unukalhai'][1])
check('T34 T2 J Unukalhai row, SKY cell S Jupiter → S Unukalhai Dec by hand from POSITIONS: 13.296270 -> ninth 13.3333 −0.03706 (55.52)',
      abs(v0 - 13.29627) < 1e-6 and x[27].value == round(v0, 6) and x[28].value == round(v5, 6) and x[29].value == '13.3333 (ninth)'
      and x[31].value == f'{v0 - 120 / 9:+.5f}' and f'{x[32].value:.2f}' == f'{100 * (0.083333 - abs(v0 - 120 / 9)) / 0.083333:.2f}',
      f'{v0:.6f} -> {v5:.6f}; {x[27].value}, {x[28].value}, {x[29].value}, {x[31].value}, {x[32].value}')
# T24 HORSE H Phact – H Makemake Dec; T24 HORSE RATIOS H Menkar Dec Jupiter / Mercury
v = dist(gp[('P01', 'H', 'Phact')], gp[('P01', 'H', 'Makemake')], 'Dec')
hdr, rws = t24_blocks(gw['P01'])['T24 HORSE']
c = rws['H Phact'][hdr.index(('Makemake', 'Dec'))]
want = f'39×φ · golden · {v - 39 * PHI:+.5f} · {sq(0.03236, abs(v - 39 * PHI)):.2f}'
check('T34 T24 HORSE H Phact – H Makemake Dec by hand from POSITIONS: 63.104540, 39×φ +0.00121 (92.64)', abs(v - 63.10454) < 1e-6
      and c.value == round(v, 6) and c.comment.text.split('\n')[0] == want and fillrgb(c) == GREEN, f'{v:.6f}; {first(c)!r} vs {want!r}')
dj = dist(gp[('P01', 'H', 'Menkar')], gp[('P01', 'H', 'Jupiter')], 'Dec'); dm = dist(gp[('P01', 'H', 'Menkar')], gp[('P01', 'H', 'Mercury')], 'Dec')
r_ = max(dj, dm) / min(dj, dm)
cols, rws = t24r_read(gw['P01'])['T24 HORSE RATIOS']
c = rws['H Menkar'][cols.index(('Mercury', 'Dec'))]
want = f'3/2 · fifth · Perfect · A · {r_ - 1.5:+.5f} · {sq(0.02, abs(r_ - 1.5)):.2f}'
check('T34 T24 HORSE RATIOS H Menkar Dec d(Menkar, Jupiter) / d(Menkar, Mercury) by hand from POSITIONS: 3/2 area A +0.00137 (86.75)',
      abs(r_ - 1.501372) < 1e-6 and c.value == round(r_, 6) and first(c) == want and fillrgb(c) == GREEN,
      f'{dj:.6f} / {dm:.6f} = {r_:.6f}; {first(c)!r} vs {want!r}')
# SKY block: S Jupiter → S Adhara RA (45 whole, timing = the TIMELINE event 15:19) and S Jupiter → S Menkar RA (√2 14.14)
for star, tt, tv, tol, timing in (('Adhara', '45 (whole)', 45, 0.02, 'applying'), ('Menkar', '14.14 (sqrt2)', 10 * 2 ** 0.5, max(0.005 * 10 * 2 ** 0.5, 0.025), None)):
    x = row(gw['SKY JUPITER'], 'SKY', f'S Jupiter → S {star}')
    sx = gp[('SKY', 'S', star)]
    v0 = ra_d(sj[0], sx[0]); v5 = ra_d(sj[0] + 5 * rates['Jupiter'][0], sx[0] + 5 * rates[star][0])
    t = (tv - v0) / ((v5 - v0) / 5)
    tim = f"applying, exact {(A_OFF + datetime.timedelta(minutes=t)).strftime('%H:%M')} (in {t:.1f} min)" if timing else None
    check(f'T34 SKY block S Jupiter → S {star} RA by hand from POSITIONS: {v0:.6f} -> {tt} {v0 - tv:+.5f} ({sq(tol, abs(v0 - tv)):.2f})'
          + (f', {tim}' if tim else ''), x[2].value == round(v0, 6) and x[3].value == round(v5, 6) and x[4].value == tt
          and x[6].value == f'{v0 - tv:+.5f}' and f'{x[7].value:.2f}' == f'{sq(tol, abs(v0 - tv)):.2f}' and (not timing or x[10].value == tim),
          f'{x[2].value}, {x[3].value}, {x[4].value}, {x[6].value}, {x[7].value}, {x[10].value}')
# SKY STARS: S Denebola – S Unukalhai RA 3/2 and S Menkar – S Praesepe RA 5 (area A, absolute)
ss = ss_rows(gw)
for a, b, pl, tv, tt in (('Denebola', 'Unukalhai', 'RA', 1.5, '3/2 · fifth · Perfect'), ('Menkar', 'Praesepe', 'RA', 5, '5 · 5th harmonic · Harmonic')):
    J0, J5 = gp[('SKY', 'S', 'Jupiter')], (gp[('SKY', 'S', 'Jupiter')][0] + 5 * rates['Jupiter'][0], gp[('SKY', 'S', 'Jupiter')][1] + 5 * rates['Jupiter'][1])
    X0, Y0 = gp[('SKY', 'S', a)], gp[('SKY', 'S', b)]
    X5, Y5 = ((p[0] + 5 * rates[z][0], p[1] + 5 * rates[z][1]) for p, z in ((X0, a), (Y0, b)))
    dx, dy, dxy = pdist(J0, X0, pl), pdist(J0, Y0, pl), pdist(X0, Y0, pl)
    r0 = max(dx, dy) / min(dx, dy)
    r5 = (pdist(J5, X5, pl) / pdist(J5, Y5, pl)) if dx > dy else (pdist(J5, Y5, pl) / pdist(J5, X5, pl))
    t = (tv - r0) / ((r5 - r0) / 5)
    clk = (A_OFF + datetime.timedelta(minutes=t)).strftime('%H:%M')
    tim = f"applying, exact {clk} (in {t:.1f} min)" if t > 0 else f"separating, exact {clk} ({-t:.1f} min ago)"
    pos_ = 'between' if abs(dxy - (dx + dy)) <= 0.01 * (dx + dy) else 'far side'
    blk, x = ss[(f'S {a} – S {b}', pl)]
    check(f'T34 SKY STARS S {a} – S {b} {pl} by hand from POSITIONS', [round(v, 6) for v in (dx, dy, dxy, r0)] == [x[4], x[6], x[8], x[10]]
          and x[11] == tt and x[12] == f'{r0 - tv:+.5f}' and f'{x[13]:.2f}' == f'{sq(0.02, abs(r0 - tv)):.2f}' and x[14] == tim and x[15] == pos_
          and 'AREA A' in blk.upper(), f'{dx:.6f} / {dy:.6f} / {dxy:.6f}, ratio {r0:.6f} -> {r5:.6f}, {tt} {r0 - tv:+.5f} '
          f'({sq(0.02, abs(r0 - tv)):.2f}), {tim}, {pos_}; sheet {x[10:16]}')
# ---- 35. T24 conjunction red fill (Eddie, 20 Oct 2026; display only): every T24 SKY / HORSE / JOCKEY body cell and T24 H / J distance
# cell red (FF8080) exactly when RA < 1.5 / Dec < 0.3, otherwise the fill of the build before (commit 93e73bc4); values, comments, borders
# and every other cell identical (only the T24 title note changes); pairs workbooks identical
out35 = {}
for nm, bo, after in (('Lingfield', lf_h, lf_r), ('Ascot', gf_h, gf46_r), ('Ascot35', gf35_h, gf35_r)):   # builds by ad0defaf's code (21 Oct 2026)
    o = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_t24red/compare_red.py', bo, after], capture_output=True, text=True).stdout
    pw = [openpyxl.load_workbook(p, read_only=True) for p in (bo.replace('_jupiter_tables', '_pairs'), after.replace('_jupiter_tables', '_pairs'))]
    psame = pw[0].sheetnames == pw[1].sheetnames and all(vals(pw[0][s]) == vals(pw[1][s]) for s in pw[0].sheetnames)
    reds = {(m.group(1), m.group(2)): int(m.group(3)) for m in re.finditer(r'^(\S+(?: JUPITER)?)\s+(T24 \S+(?: / J)?)\s+red\s+(\d+) of', o, re.M)}
    out35[nm] = (o, psame, reds)
W35 = {'Ascot': {('SKY JUPITER', 'T24 SKY'): 20, ('P01', 'T24 HORSE'): 16, ('P01', 'T24 JOCKEY'): 13, ('P01', 'T24 H / J'): 2},
       'Lingfield': {('SKY JUPITER', 'T24 SKY'): 7, **{(p, t): n for p, ns in (('P01', (13, 3, 1)), ('P03', (9, 11, 2)), ('P05', (7, 1, 0)),
                     ('P07', (9, 2, 0)), ('P09', (10, 5, 1)), ('P11', (7, 3, 1))) for t, n in zip(('T24 HORSE', 'T24 JOCKEY', 'T24 H / J'), ns)}}}
check('T35 T24 conjunction red, both races --full, commit 93e73bc4 vs commit ad0defaf (the red fill): every T24 SKY / HORSE / JOCKEY body cell and T24 '
      'H / J distance cell red exactly when RA < 1.5 / Dec < 0.3, otherwise the fill it had; values, comments, outlines and every other cell '
      'identical; only the T24 title notes changed (Ascot 3, Lingfield 13); pairs identical; red cells per block as reported; the 35-star '
      'copy of tests 31 - 33 the same',
      all('mismatches: 0' in o and ps for o, ps, _ in out35.values()) and 'title cells changed: 3' in out35['Ascot'][0]
      and 'title cells changed: 13' in out35['Lingfield'][0] and 'title cells changed: 3' in out35['Ascot35'][0]
      and all(out35[k][2] == W35[k] for k in W35),
      f"{ {k: (line(v[0], 'mismatches:'), v[1], v[2]) for k, v in out35.items()} }")
# by hand from POSITIONS (rebuilt Ascot P01): T24 H / J H Nunki RA d(H Nunki, H Jupiter) red, = the T24 HORSE Nunki – Jupiter cell; the
# ratio cell beside it still "together", no fill
a = dist(gp[('P01', 'H', 'Nunki')], gp[('P01', 'H', 'Jupiter')], 'RA')
hj = nr['T24 H / J'][1]['Nunki']
c, cr = hj[col_('T24 H / J', 'd(H star, H Jupiter)', 'RA')], hj[col_('T24 H / J', 'H / J', 'RA')]
check('T35 T24 H / J Nunki RA d(H Nunki, H Jupiter) by hand from POSITIONS: 0.805294 < 1.5 -> red, comment the conjunction line unchanged; '
      'the H / J ratio cell "together", no fill', a < 1.5 and c.value == round(a, 6) and fillrgb(c) == '00FF8080'
      and first(c).startswith('0 · conjunction (RA < 1.5)') and cr.value == 'together' and not fillrgb(cr),
      f'{a:.6f}; {fillrgb(c)}, {first(c)!r}; {cr.value!r} {fillrgb(cr)}')
# Test 36 (Eddie, 21 Oct 2026): 20 more stars (Ankaa ... Sualocin; Aculeus = M6, Acumen = M7, Facies = M22) and the Orion Nebula Cluster
# (M42), built as one change; T1_T2_T24_STARS 67 in engine RA order, the same tables as the 11; everything else unchanged. "Before" = ad0defaf.
print('test 36: 20 more stars and the Orion Nebula Cluster (67 in T1, T2, T24, T24 ratio tables, SKY block, SKY STARS, sky timelines)')
CAT21 = {'Ankaa': (6.571, -42.306), 'Al Rescha': (30.512, 2.764), 'Mirfak': (51.081, 49.861), 'El Nath': (81.573, 28.607),
         'Meissa': (83.784, 9.934), 'Alnilam': (84.053, -1.202), 'Murzim': (95.675, -17.956), 'Alhena': (99.428, 16.399),
         'Acubens': (134.622, 11.858), 'Alphard': (141.897, -8.659), 'Alkes': (164.944, -18.299), 'Zosma': (168.527, 20.524),
         'Vindemiatrix': (195.544, 10.959), 'Diadem': (197.497, 17.529), 'Ras Algethi': (258.662, 14.390), 'Aculeus': (265.083, -32.253),
         'Acumen': (268.463, -34.793), 'Facies': (279.100, -23.905), 'Rukbat': (290.972, -40.616), 'Sualocin': (309.910, 15.912),
         'Orion Nebula Cluster': (83.822, -5.391)}
EXPECT67 = ['Alpheratz', 'Algenib', 'Ankaa', 'Difda', 'Mirach', 'Al Rescha', 'Hamal', 'Menkar', 'Algol', 'Mirfak', 'Pleiades', 'Aldebaran',
            'Rigel', 'Capella', 'Bellatrix', 'El Nath', 'Meissa', 'Orion Nebula Cluster', 'Alnilam', 'Phact', 'Betelgeuse', 'Murzim', 'Alhena', 'Sirius', 'Adhara',
            'Wezen', 'Castor', 'Procyon', 'Pollux', 'Praesepe', 'Acubens', 'Alphard', 'Regulus', 'Alkes', 'Zosma', 'Denebola', 'Algorab',
            'Vindemiatrix', 'Diadem', 'Spica', 'Alkaid', 'Menkent', 'Arcturus', 'Zubenelgenubi', 'Zubeneschamali', 'Alphecca', 'Unukalhai',
            'Antares', 'Ras Algethi', 'Rasalhague', 'Aculeus', 'Galactic Centre', 'Acumen', 'Kaus Australis', 'Facies', 'Vega', 'Nunki',
            'Rukbat', 'Altair', 'Sualocin', 'Deneb', 'Sadalsuud', 'Deneb Algedi', 'Sadalmelik', 'Fomalhaut', 'Scheat', 'Markab']
B67 = dict(ENG.BEHENIAN_STARS)
e21 = {x: swe.fixstar2_ut(B67[x], 2451545.0, ENG._FLAG) for x in NEW21}
off21 = {x: (e21[x][0][0] - CAT21[x][0], e21[x][0][1] - CAT21[x][1]) for x in NEW21}
check('T36 engine: the 21 stars at J2000.0 within 0.02° of the catalogue (largest Rukbat dRA −0.0078); sefstars names as given (Murzim = '
      'Mirzam,beCMa; clusters Aculeus M6, Acumen M7, Facies M22; Orion Nebula Cluster = Orion Nebula,M42); Mirfak Dec +49.864 <= 50',
      all(abs(u) < 0.02 and abs(v) < 0.02 for u, v in off21.values()) and e21['Murzim'][1] == 'Mirzam,beCMa'
      and [e21[x][1] for x in ('Aculeus', 'Acumen', 'Facies', 'Orion Nebula Cluster')] == ['Aculeus,M6', 'Acumen,M7', 'Facies,M22', 'Orion Nebula,M42'] and abs(e21['Mirfak'][0][1]) <= 50,
      ', '.join(f'{x} {u:+.4f}/{v:+.4f}' for x, (u, v) in off21.items()) + f"; Mirfak Dec {e21['Mirfak'][0][1]:+.6f}")
era67 = {x: swe.fixstar2_ut(B67[x], 2451545.0, ENG._FLAG)[0] for x in EXPECT67}
check('T36 T1_T2_T24_STARS = the 67 stars (|Dec| <= 50, no Polaris) sorted by engine J2000 RA at J2000.0 = Eddie\'s list (no pair differs; '
      'closest Meissa 83.7901 / Orion Nebula Cluster 83.8276)', JT.T1_T2_T24_STARS == EXPECT67 == sorted(EXPECT67, key=lambda x: era67[x][0])
      and all(abs(era67[x][1]) <= 50 for x in EXPECT67) and len(EXPECT67) == 67,
      f"Facies {era67['Facies'][0]:.4f} / Vega {era67['Vega'][0]:.4f}; Meissa {era67['Meissa'][0]:.4f} / ONC {era67['Orion Nebula Cluster'][0]:.4f} / Alnilam {era67['Alnilam'][0]:.4f}; "
      f"Bellatrix {era67['Bellatrix'][0]:.4f} / El Nath {era67['El Nath'][0]:.4f}")
ok, det = True, []
for nm, w, nst in (('Ascot', gw, 67), ('Lingfield', lfw, 21)):
    want = [x for x in EXPECT67 if nst == 67 or x in JT.STARS and x != 'Galactic Centre']
    got = {'SKY': sky_star_rows(w)}
    for sh in ['SKY JUPITER'] + runner_tabs(w):
        for x in w[sh].iter_rows(values_only=True):
            if x[0] in ('T1', 'T2') and x[1] and ' → ' in str(x[1]) and x[1].split(' → ')[1][2:] in JT.T1_T2_T24_STARS + ['Polaris']:
                got.setdefault(f'{sh} {x[0]}', []).append(x[1].split(' → ')[1][2:])
        for k, (hdr, rows) in t24_blocks(w[sh]).items():
            got[f'{sh} {k}'] = [lab.split(' ', 1)[1] for lab in rows]
        for k, (cols, rows) in t24r_read(w[sh]).items():
            got[f'{sh} {k}'] = [lab.split(' ', 1)[1] if k != 'T24 H / J' else lab for lab in rows]
    ok &= len(want) == nst and all(v == want for v in got.values()) and len(got) == 1 + 1 + 7 * len(runner_tabs(w))
    det.append(f'{nm} {len(got)} lists of {nst}')
check('T36 the 67 (Ascot) / 21 (Lingfield) in RA order in T1, T2, T24 SKY / HORSE / JOCKEY, T24 H / J, T24 HORSE / JOCKEY RATIOS and the SKY block',
      ok, '; '.join(det))
# against the build before (commit ad0defaf), both races --full: the after workbook minus the rows naming one of the 20 = the before
# workbook, row for row (values, fills, comments; every row of the 46 earlier stars, SKY STARS pairs and timeline events), only count titles
# differ; the 21 only in the allowed tables; pairs identical
out36 = {}
for nm, bo, after in (('Lingfield', lf_r, lf_s), ('Ascot', gf_r, gf_s)):   # 22 Oct 2026: the after = built by the code of 18aff98a
    o = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_stars67/compare_67.py', bo, after], capture_output=True, text=True).stdout
    pw = [openpyxl.load_workbook(p, read_only=True) for p in (bo.replace('_jupiter_tables', '_pairs'), after.replace('_jupiter_tables', '_pairs'))]
    psame = pw[0].sheetnames == pw[1].sheetnames and all(vals(pw[0][s]) == vals(pw[1][s]) for s in pw[0].sheetnames)
    out36[nm] = (o, psame)
rem = {}
for l in out36['Ascot'][0].splitlines():
    m = re.match(r'(.+?): rows before \d+, after \d+, new-star rows (\d+) (\{.*?\});', l)
    if m:
        rem[m.group(1)] = (int(m.group(2)), eval(m.group(3)))
W36 = {'POSITIONS': {'SKY': 21, 'P01': 42}, 'SKY JUPITER': {'SKY': 21, 'SKY STARS': 347, 'T24': 21, 'TIMELINE': 40, 'LONG TIMELINE': 59},
       'P01': {'T1': 21, 'T2': 21, 'T24': 42, 'T24 H / J': 21, 'T24 HORSE RATIOS': 21, 'T24 JOCKEY RATIOS': 21}}
ok_ = (all(line(o, 'sheets with differences other than title rows:') == 'sheets with differences other than title rows: 0' and ps for o, ps in out36.values())
       and {k: v[1] for k, v in rem.items() if v[0]} == W36
       and not any('new-star rows 0 {}' not in l for l in out36['Lingfield'][0].splitlines() if ': rows before' in l))
check('T36 against the build before (commit ad0defaf), both races --full: every row not naming one of the 21 identical, row for row (values, '
      'fills, comments) - the 46 earlier stars\' rows, SKY STARS pairs and timeline events included - only count titles differ; the 21 only in '
      'POSITIONS, T1, T2, T24, T24 H / J, T24 RATIOS, the SKY block, SKY STARS, TIMELINE, LONG TIMELINE (rows as reported); pairs identical; '
      'Lingfield (old batch) gains nothing', ok_,
      f"Ascot new-star rows { {k: v for k, v in rem.items() if v[0]} }; pairs identical {[ps for _, ps in out36.values()]}")
RX21 = re.compile(r'\b(' + '|'.join(NEW21) + r')\b')
tln21 = lambda w, t: sum(1 for x in w['SKY JUPITER'].iter_rows(values_only=True) if x and x[0] == t and x[4] and RX21.search(str(x[4])))
check('T36 rebuilt Ascot: TIMELINE 50 -> 90 events (40 new-star; 29 before the off, 7 in the first 5 min, 54 after), LONG TIMELINE 67 -> 126 '
      '(59 new-star; 61 separating, 65 applying; built by the code of 18aff98a, LONG >= 80)', tln21(gw_s, 'TIMELINE') == 40 and tln21(gw_s, 'LONG TIMELINE') == 59
      and tlt(gw_s)[0].endswith('90 events, 29 before the off, 7 in the first 5 min, 54 after') and tlt(gw_s)[1].endswith('126 events, 61 separating, 65 applying'),
      f"{tln21(gw_s, 'TIMELINE')} / {tln21(gw_s, 'LONG TIMELINE')}; {tlt(gw_s)[0][-70:]}; {tlt(gw_s)[1][-40:]}")
# by hand from POSITIONS (rebuilt Ascot): two cells each of T1, T2, T24 (one ratio table cell), the SKY block and SKY STARS; clusters in T1,
# T24 and SKY STARS
cases = [  # (table, chart, star, plane, column, value, target text, offset, score by hand, fill)
    ('T1', 'H', 'Acumen', 'Dec', 10, 12.001827, '12 (whole)', lambda v: v - 12, lambda v: sq(0.02, abs(v - 12)), GREEN),
    ('T1', 'H', 'El Nath', 'RA', 2, 158.570201, '98×φ (golden)', lambda v: v - 98 * PHI, lambda v: sq(0.03236, abs(v - 98 * PHI)), GREEN),
    ('T2', 'J', 'Murzim', 'RA', 2, 179.445573, '10×φ^6 (phi power)', lambda v: v - 10 * PHI ** 6, lambda v: sq(0.005 * 10 * PHI ** 6, abs(v - 10 * PHI ** 6)), GREEN),
]
for tid, C, star, pl, c0, exp, tt, off, sc, fill in cases:
    x = row(gw['P01'], tid, f'{C} Jupiter → {C} {star}')
    v = dist(gp[('P01', C, 'Jupiter')], gp[('P01', C, star)], pl)
    check(f'T36 {tid} {C} Jupiter → {C} {star} {pl} by hand from POSITIONS: {exp} -> {tt} ({sc(exp):.2f})', abs(v - exp) < 1e-6 and x[c0].value == round(v, 6)
          and x[c0 + 2].value == tt and x[c0 + 4].value == f'{off(v):+.5f}' and f'{x[c0 + 5].value:.2f}' == f'{sc(v):.2f}' and fillrgb(x[c0]) == fill,
          f'{v:.6f}; {x[c0 + 2].value}, {x[c0 + 4].value}, {x[c0 + 5].value} (by hand {sc(v):.2f}), {fillrgb(x[c0])}')
# T2's SKY cell S Jupiter → S El Nath Dec (the J El Nath row): ninth 8.88889 (_NINTH_RANGES tolerance 0.013889), +5 min from the POSITIONS rates
x = row(gw['P01'], 'T2', 'J Jupiter → J El Nath')
sj, se = gp[('SKY', 'S', 'Jupiter')], gp[('SKY', 'S', 'El Nath')]
v0, v5 = abs(sj[1] - se[1]), abs(sj[1] + 5 * rates['Jupiter'][1] - se[1] - 5 * rates['El Nath'][1])
check('T36 T2 J El Nath row, SKY cell S Jupiter → S El Nath Dec by hand from POSITIONS: 8.884166 -> ninth 8.88889 −0.00472 (66.00)',
      abs(v0 - 8.884166) < 1e-6 and x[27].value == round(v0, 6) and x[28].value == round(v5, 6) and x[29].value == '8.88889 (ninth)'
      and x[31].value == f'{v0 - 80 / 9:+.5f}' and f'{x[32].value:.2f}' == f'{100 * (0.013889 - abs(v0 - 80 / 9)) / 0.013889:.2f}',
      f'{v0:.6f} -> {v5:.6f}; {x[27].value}, {x[28].value}, {x[29].value}, {x[31].value}, {x[32].value}')
# T24 JOCKEY J Facies – J Neptune Dec (cluster); T24 JOCKEY RATIOS J Mirfak RA d(Mirfak, Jupiter) / d(Mirfak, Uranus)
v = dist(gp[('P01', 'J', 'Facies')], gp[('P01', 'J', 'Neptune')], 'Dec')
hdr, rws = t24_blocks(gw['P01'])['T24 JOCKEY']
c = rws['J Facies'][hdr.index(('Neptune', 'Dec'))]
want = f'1×φ · golden · {v - PHI:+.5f} · {sq(0.03236, abs(v - PHI)):.2f}'
check('T36 T24 JOCKEY J Facies – J Neptune Dec by hand from POSITIONS: 1.616795, 1×φ −0.00124 (92.49)', abs(v - 1.616795) < 1e-6
      and c.value == round(v, 6) and first(c) == want and fillrgb(c) == GREEN, f'{v:.6f}; {first(c)!r} vs {want!r}')
dj = dist(gp[('P01', 'J', 'Mirfak')], gp[('P01', 'J', 'Jupiter')], 'RA'); du = dist(gp[('P01', 'J', 'Mirfak')], gp[('P01', 'J', 'Uranus')], 'RA')
r_ = max(dj, du) / min(dj, du)
cols, rws = t24r_read(gw['P01'])['T24 JOCKEY RATIOS']
c = rws['J Mirfak'][cols.index(('Uranus', 'RA'))]
want = f'6/5 · minor third · Imperfect · B · {(r_ / 1.2 - 1) * 100:+.5f}% · {sq(0.15, abs((r_ / 1.2 - 1) * 100)):.2f}'
check('T36 T24 JOCKEY RATIOS J Mirfak RA d(Mirfak, Jupiter) / d(Mirfak, Uranus) by hand from POSITIONS: 1.199952, 6/5 area B −0.00397 % (94.78)',
      abs(r_ - 1.199952) < 1e-6 and c.value == round(r_, 6) and first(c) == want and fillrgb(c) == GREEN,
      f'{dj:.6f} / {du:.6f} = {r_:.6f}; {first(c)!r} vs {want!r}')
# SKY block: S Jupiter → S Meissa RA (silver 24.14 = 10 (1 + √2)) and S Jupiter → S Al Rescha RA (18×φ), both separating
for star, tt, tv, tol in (('Meissa', '24.14 (silver)', 10 * (1 + 2 ** 0.5), max(0.005 * 10 * (1 + 2 ** 0.5), 0.025)), ('Al Rescha', '18×φ (golden)', 18 * PHI, 0.03236)):
    x = row(gw['SKY JUPITER'], 'SKY', f'S Jupiter → S {star}')
    sx = gp[('SKY', 'S', star)]
    v0 = ra_d(sj[0], sx[0]); v5 = ra_d(sj[0] + 5 * rates['Jupiter'][0], sx[0] + 5 * rates[star][0])
    t = (tv - v0) / ((v5 - v0) / 5)
    tim = f"separating, exact {(A_OFF + datetime.timedelta(minutes=t)).strftime('%H:%M')} ({-t:.1f} min ago)"
    check(f'T36 SKY block S Jupiter → S {star} RA by hand from POSITIONS: {v0:.6f} -> {tt} {v0 - tv:+.5f} ({sq(tol, abs(v0 - tv)):.2f}), {tim}',
          t < 0 and x[2].value == round(v0, 6) and x[3].value == round(v5, 6) and x[4].value == tt and x[6].value == f'{v0 - tv:+.5f}'
          and f'{x[7].value:.2f}' == f'{sq(tol, abs(v0 - tv)):.2f}' and x[10].value == tim,
          f'{x[2].value}, {x[3].value}, {x[4].value}, {x[6].value}, {x[7].value}, {x[10].value}')
# SKY STARS: S Pleiades – S Diadem Dec 2 (area A, absolute) and S Facies – S Deneb Dec 1+1/√2 (φ and √2, 0.15 %; cluster)
ss = ss_rows(gw)
for a, b, pl, tv, tt, area, kind in (('Pleiades', 'Diadem', 'Dec', 2.0, '2 · octave · Perfect', 'AREA A', 'abs'),
                                     ('Facies', 'Deneb', 'Dec', 1 + 1 / 2 ** 0.5, '1+1/√2 · √2 division partner · Dissonant', 'AREA Φ AND √2', 'pct')):
    J0, J5 = gp[('SKY', 'S', 'Jupiter')], (gp[('SKY', 'S', 'Jupiter')][0] + 5 * rates['Jupiter'][0], gp[('SKY', 'S', 'Jupiter')][1] + 5 * rates['Jupiter'][1])
    X0, Y0 = gp[('SKY', 'S', a)], gp[('SKY', 'S', b)]
    X5, Y5 = ((p[0] + 5 * rates[z][0], p[1] + 5 * rates[z][1]) for p, z in ((X0, a), (Y0, b)))
    dx, dy, dxy = pdist(J0, X0, pl), pdist(J0, Y0, pl), pdist(X0, Y0, pl)
    r0 = max(dx, dy) / min(dx, dy)
    r5 = (pdist(J5, X5, pl) / pdist(J5, Y5, pl)) if dx > dy else (pdist(J5, Y5, pl) / pdist(J5, X5, pl))
    t = (tv - r0) / ((r5 - r0) / 5)
    clk = (A_OFF + datetime.timedelta(minutes=t)).strftime('%H:%M')
    tim = f"applying, exact {clk} (in {t:.1f} min)" if t > 0 else f"separating, exact {clk} ({-t:.1f} min ago)"
    pos_ = 'between' if abs(dxy - (dx + dy)) <= 0.01 * (dx + dy) else 'far side'
    offt, sct = (f'{r0 - tv:+.5f}', sq(0.02, abs(r0 - tv))) if kind == 'abs' else (f'{(r0 / tv - 1) * 100:+.5f}%', sq(0.15, abs((r0 / tv - 1) * 100)))
    blk, x = ss[(f'S {a} – S {b}', pl)]
    check(f'T36 SKY STARS S {a} – S {b} {pl} by hand from POSITIONS: {dx:.6f} / {dy:.6f} / {dxy:.6f}, {r0:.6f} {tt.split(" · ")[0]} {offt} ({sct:.2f}), {tim}, {pos_}',
          [round(v, 6) for v in (dx, dy, dxy, r0)] == [x[4], x[6], x[8], x[10]] and x[11] == tt and x[12] == offt
          and f'{x[13]:.2f}' == f'{sct:.2f}' and x[14] == tim and x[15] == pos_ and area in blk.upper(),
          f'sheet {x[10:16]}; {blk[:40]}')
# Orion Nebula Cluster by hand from POSITIONS (rebuilt Ascot): T1 H Jupiter → H ONC RA (outside: nearest 100×φ^1, no score, no fill) and its
# SKY cell S Jupiter → S ONC RA (silver 24.14, applying); T24 HORSE H ONC – H Venus Dec (16 whole) and H ONC – H Mars RA (conjunction, red);
# SKY STARS S ONC – S Phact Equator (unison); its pairs with Meissa, Alnilam, Phact: RA "together" (left out), the rest by the filter
ONC = 'Orion Nebula Cluster'
x = row(gw['P01'], 'T1', f'H Jupiter → H {ONC}')
v = dist(gp[('P01', 'H', 'Jupiter')], gp[('P01', 'H', ONC)], 'RA')
check('T36 T1 H Jupiter → H Orion Nebula Cluster RA by hand from POSITIONS: 160.819052, nearest 100×φ^1 outside ±0.809, −0.98435, no score, no fill',
      abs(v - 160.819052) < 1e-6 and x[2].value == round(v, 6) and x[4].value == '100×φ^1 (phi power) — outside ±0.809'
      and x[6].value == f'{v - 100 * PHI:+.5f}' and x[7].value is None and fillrgb(x[2]) is None, f'{v:.6f}; {x[4].value}, {x[6].value}, {x[7].value}')
so = gp[('SKY', 'S', ONC)]
v0 = ra_d(sj[0], so[0]); v5 = ra_d(sj[0] + 5 * rates['Jupiter'][0], so[0] + 5 * rates[ONC][0])
tv, tol = 10 * (1 + 2 ** 0.5), max(0.005 * 10 * (1 + 2 ** 0.5), 0.025)
t_ = (tv - v0) / ((v5 - v0) / 5)
tim = f"applying, exact {(A_OFF + datetime.timedelta(minutes=t_)).strftime('%H:%M')} (in {t_:.1f} min)"
check(f'T36 T1 H Orion Nebula Cluster row, SKY cell S Jupiter → S ONC RA by hand from POSITIONS: {v0:.6f} -> 24.14 silver {v0 - tv:+.5f} '
      f'({sq(tol, abs(v0 - tv)):.2f}), {tim}', abs(v0 - 24.173991) < 1e-6 and x[18].value == round(v0, 6) and x[19].value == round(v5, 6)
      and x[20].value == '24.14 (silver)' and x[22].value == f'{v0 - tv:+.5f}' and f'{x[23].value:.2f}' == f'{sq(tol, abs(v0 - tv)):.2f}'
      and x[26].value == tim, f'{x[18].value}, {x[19].value}, {x[20].value}, {x[22].value}, {x[23].value}, {x[26].value}')
hdr, rws = t24_blocks(gw['P01'])['T24 HORSE']
for body, pl, exp, want, fill in (('Venus', 'Dec', 16.000211, lambda v: f'16 · whole · {v - 16:+.5f} · {sq(0.02, abs(v - 16)):.2f}', GREEN),
                                  ('Mars', 'RA', 0.333693, lambda v: f'0 · conjunction (RA < 1.5) · {v:+.5f} · {sq(1.5, v):.2f}', '00FF8080')):
    v = dist(gp[('P01', 'H', ONC)], gp[('P01', 'H', body)], pl)
    c = rws[f'H {ONC}'][hdr.index((body, pl))]
    check(f'T36 T24 HORSE H Orion Nebula Cluster – H {body} {pl} by hand from POSITIONS: {v:.6f}, {want(v)}, fill {fill}', abs(v - exp) < 1e-6
          and c.value == round(v, 6) and first(c) == want(v) and fillrgb(c) == fill, f'{v:.6f}; {first(c)!r}; {fillrgb(c)}')
J0, J5 = gp[('SKY', 'S', 'Jupiter')], (gp[('SKY', 'S', 'Jupiter')][0] + 5 * rates['Jupiter'][0], gp[('SKY', 'S', 'Jupiter')][1] + 5 * rates['Jupiter'][1])
X0, Y0 = gp[('SKY', 'S', ONC)], gp[('SKY', 'S', 'Phact')]
X5, Y5 = ((p[0] + 5 * rates[z][0], p[1] + 5 * rates[z][1]) for p, z in ((X0, ONC), (Y0, 'Phact')))
dx, dy, dxy = pdist(J0, X0, 'Equator'), pdist(J0, Y0, 'Equator'), pdist(X0, Y0, 'Equator')
r0 = max(dx, dy) / min(dx, dy)
r5 = (pdist(J5, X5, 'Equator') / pdist(J5, Y5, 'Equator')) if dx > dy else (pdist(J5, Y5, 'Equator') / pdist(J5, X5, 'Equator'))
t_ = (1 - r0) / ((r5 - r0) / 5)
tim = (f"applying, exact {(A_OFF + datetime.timedelta(minutes=t_)).strftime('%H:%M')} (in {t_:.1f} min)" if t_ > 0 else
       f"separating, exact {(A_OFF + datetime.timedelta(minutes=t_)).strftime('%H:%M')} ({-t_:.1f} min ago)")
pos_ = 'between' if abs(dxy - (dx + dy)) <= 0.01 * (dx + dy) else 'far side'
blk, x = ss[(f'S {ONC} – S Phact', 'Equator')]
check(f'T36 SKY STARS S Orion Nebula Cluster – S Phact Equator by hand from POSITIONS: {dx:.6f} / {dy:.6f} / {dxy:.6f}, {r0:.6f} unison '
      f'{r0 - 1:+.5f} ({sq(0.02, abs(r0 - 1)):.2f}), {tim}, {pos_}', [round(v, 6) for v in (dx, dy, dxy, r0)] == [x[4], x[6], x[8], x[10]]
      and x[11] == '1 · unison · Perfect' and x[12] == f'{r0 - 1:+.5f}' and f'{x[13]:.2f}' == f'{sq(0.02, abs(r0 - 1)):.2f}' and x[14] == tim
      and x[15] == pos_ and 'AREA A' in blk.upper(), f'sheet {x[10:16]}')
# its pairs with Meissa, Alnilam, Phact (orientation: RA order of the new stars, so S Meissa – S ONC): every RA pair "together" (d < 1.5),
# not listed; listed exactly: ONC – Alnilam Dec (6/5) and ONC – Phact Equator (unison)
cx = pos_ctx(gw, A_OFF)
prs = [(f'S Meissa – S {ONC}'), f'S {ONC} – S Alnilam', f'S {ONC} – S Phact']
allr = {(h['pair'], h['plane']): h for h in JT.pair_rows(cx, {'H': {}, 'J': {}}, [x for x in SS_ORDER if x in cx.S0], tid='SKY STARS', sky=True)
        if h['pair'] in prs}
listed = sorted(k for k in ss if k[0] in prs)
check('T36 SKY STARS pairs of the Orion Nebula Cluster with Meissa, Alnilam, Phact: RA together (d(X, Y) 0.037663 / 0.231326 / 1.089043), not '
      'listed; listed exactly ONC – Alnilam Dec (6/5) and ONC – Phact Equator (unison)',
      all(allr[(p_, 'RA')]['together'] for p_ in prs) and listed == [(f'S {ONC} – S Alnilam', 'Dec'), (f'S {ONC} – S Phact', 'Equator')]
      and [round(pdist(gp[('SKY', 'S', a)], gp[('SKY', 'S', b)], 'RA'), 6) for a, b in ((ONC, 'Meissa'), (ONC, 'Alnilam'), (ONC, 'Phact'))]
      == [0.037663, 0.231326, 1.089043], f'{sorted(allr)}; listed {listed}')
# Test 37 (Eddie, 22 Oct 2026): all 67 stars in every timeline - runner TIMELINE H / J and LONG TIMELINE H / J take star events off-sheet
# (S Jup→star, star→Jup, S Jup on star pair, star apex), STAR TIMELINE (sky) and STAR TIMELINE H / J (the Jupiter–star events), LONG
# TIMELINE threshold >= 90 (was 80). "Before" = commit 18aff98a.
print('test 37: all 67 stars in every timeline, STAR TIMELINE, LONG >= 90')
SSRC = ('S Jup→star', 'star→Jup', 'S Jup on star pair', 'star apex')
out37 = {}
for nm, bo, after in (('Lingfield', lf_s, lf_t), ('Ascot', gf_s, gf_t)):   # 18aff98a -> 632447ff (the builds above)
    out37[nm] = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_startl/compare_tl.py', bo, after], capture_output=True, text=True).stdout
W37 = {'Ascot': ['SKY JUPITER  LONG TIMELINE    before  126 (>= 90: 68) after   69', 'SKY JUPITER  STAR TIMELINE    before    0 after   65',
                 'SKY JUPITER  TIMELINE         before   90 after   90', 'P01          LONG TIMELINE H  before   17 (>= 90: 8) after   50',
                 'P01          LONG TIMELINE J  before   23 (>= 90: 6) after   49', 'P01          STAR TIMELINE H  before    0 after   57',
                 'P01          STAR TIMELINE J  before    0 after   52', 'P01          TIMELINE H       before   13 after   68',
                 'P01          TIMELINE J       before   11 after   63']}
check('T37 against the build before (commit 18aff98a), both races --full: every earlier TIMELINE / TIMELINE H / J event kept with the same cells '
      '(only "also" may gain a star source), every LONG event scoring >= 90 kept, every row outside the timelines identical; counts as reported',
      all(line(o, 'mismatches:') == 'mismatches: 0' for o in out37.values()) and all(any(l.startswith(w_) for l in out37['Ascot'].splitlines()) for w_ in W37['Ascot']),
      ' | '.join(f"{k}: {line(o, 'mismatches:')}" for k, o in out37.items()))
# every star event recomputed from POSITIONS (own code; families.py for the targets): TIMELINE H / J (window) and LONG TIMELINE H / J (>= 90)
PL3 = ('RA', 'Dec', 'Equator')


def star_expect(w, P, keep):
    sky, nat = {}, {}
    for x in w['POSITIONS'].iter_rows(min_row=5, values_only=True):
        if x and x[3] and x[0] == 'SKY':
            sky[x[3]] = (x[5], x[6], 0.0 if x[7] in (None, 'n/a') else x[7], 0.0 if x[8] in (None, 'n/a') else x[8])
        elif x and x[3] and x[0] == P:
            nat[(x[2], x[3])] = (x[5], x[6])

    def pos(p, m):
        c, n = p.split(' ', 1)
        if c == 'S':
            q = sky[n]
            return ((q[0] + m * q[2]) % 360.0, q[1] + m * q[3])
        return nat[(c, n)]

    def d(a, b, pl, m=0.0):
        pa, pb = pos(a, m), pos(b, m)
        if pl == 'RA':
            x = abs(pa[0] - pb[0]) % 360.0
            return min(x, 360.0 - x)
        return abs(pa[1] - pb[1]) if pl == 'Dec' else abs(abs(pa[1]) - abs(pb[1]))
    straddle = lambda *ps: not ((pos(ps[0], 0)[1] >= 0) == (pos(ps[1], 0)[1] >= 0) == (pos(ps[2], 0)[1] >= 0))
    lin = lambda v0, v5, tv: None if v5 == v0 else (tv - v0) / ((v5 - v0) / 5.0)
    fp = lambda pl: pl if pl in ('RA', 'Dec') else None

    def fold(dd):
        if dd['family'] == 'conj':
            return ('conj', 0)
        return (dd['family'], re.sub('[^0-9]', '', f"{dd['tv']:.6g}").strip('0'))

    def midhit(a, b, c, pl, da, db):                       # c the middle point of a and b
        if 100.0 * min(da, db) / max(da, db) < 90.0:
            return None
        if pl == 'RA':
            pa, pb, pc = pos(a, 0)[0], pos(b, 0)[0], pos(c, 0)[0]
            mid = (pa + ((pb - pa + 180) % 360 - 180) / 2) % 360
            near, far = (pc - mid + 180) % 360 - 180, (pc - mid) % 360 - 180
            off, tol = (near if abs(near) <= abs(far) else far), 0.5
        else:
            f = (lambda v: v) if pl == 'Dec' else abs
            off, tol = f(pos(c, 0)[1]) - (f(pos(a, 0)[1]) + f(pos(b, 0)[1])) / 2, 0.15
        if abs(off) > tol:
            return None
        dev = 100.0 - 100.0 * min(da, db) / max(da, db)
        return 0.5 * (10 * (10 - dev) / 10) ** 2 + 0.5 * (10 * (tol - abs(off)) / tol) ** 2
    ev = {}

    def add(key, src, t, **e):
        if t is None or not keep(t, e['score']):
            return
        if key in ev:
            if src != ev[key]['src'] and src not in ev[key]['also']:
                ev[key]['also'].append(src)
            return
        ev[key] = dict(e, src=src, t=t, also=[])

    def dist(src, a, b, pl, dd, hit):
        v0, v5 = d(a, b, pl), d(a, b, pl, 5.0)
        kp = 'Dec' if pl == 'Equator' and not straddle(a, b, b) else pl
        add(('d', frozenset((a, b)), kp, fold(dd)), src, lin(v0, v5, dd['tv']), rel=f'{a} → {b}', plane=pl, kind='distance', tv=dd['tv'],
            v0=v0, score=dd['score'] if hit else None, C=next(p[0] for p in (a, b) if p[0] != 'S'))

    def cell(src, a, b, pl):
        v0 = d(a, b, pl)
        b_ = families.best(v0, pl, 'deg')
        dist(src, a, b, pl, b_ or families.outside(v0, pl, 'deg'), bool(b_))
    stars = [x for x in EXPECT67 if x in sky]
    for C in 'HJ':
        for x in EXPECT67:
            if (C, x) in nat:
                for pl in ('RA', 'Dec'):
                    cell('S Jup→star', 'S Jupiter', f'{C} {x}', pl)
    for C in 'HJ':
        for x in stars:
            for pl in ('RA', 'Dec'):
                cell('star→Jup', f'S {x}', f'{C} Jupiter', pl)
    sj = 'S Jupiter'
    for C in 'HJ':
        pts = [f'{C} {x}' for x in EXPECT67 if (C, x) in nat]
        for x, y in itertools.combinations(pts, 2):
            for pl in PL3:
                if pl == 'Equator' and not straddle(sj, x, y):
                    continue
                dx, dy, dxy = d(sj, x, pl), d(sj, y, pl), d(x, y, pl)
                if not dx or not dy:
                    continue
                dx5, dy5 = d(sj, x, pl, 5.0), d(sj, y, pl, 5.0)
                bx, by = families.best(dx, fp(pl), 'deg'), families.best(dy, fp(pl), 'deg')
                bxy = families.best(dxy, fp(pl), 'deg') if dxy else None
                r0, r5 = (dx / dy, dx5 / dy5) if dx >= dy else (dy / dx, dy5 / dx5)
                e_ = families.best(r0, None, 'ratio')
                near = e_ or families.outside(r0, None, 'ratio')
                mh = midhit(x, y, sj, pl, dx, dy)
                if dxy < (1.5 if pl == 'RA' else 0.3) or not (e_ or mh is not None or (bx and by and bxy)):
                    continue
                rel = f'S Jupiter: {x} – {y}'
                add(('r', sj, frozenset((x, y)), pl, near['target']), 'S Jup on star pair', lin(r0, r5, near['tv']), rel=rel, plane=pl, kind='ratio',
                    tv=near['tv'], v0=r0, score=e_['score'] if e_ else None, C=C)
                if mh is not None:
                    add(('r', sj, frozenset((x, y)), pl, '1'), 'S Jup on star pair', lin(r0, r5, 1.0), rel=rel, plane=pl, kind='midpoint', tv=1.0,
                        v0=r0, score=mh, C=C)
                for a, b, bb in ((sj, x, bx), (sj, y, by)):
                    if bb:
                        dist('S Jup on star pair', a, b, pl, bb, True)
    for x in stars:
        st = f'S {x}'
        for pl in PL3:
            for C in 'HJ':
                cj = f'{C} Jupiter'
                if pl == 'Equator' and not straddle(st, sj, cj):
                    continue
                d1, d2 = d(st, sj, pl), d(st, cj, pl)
                if not d1 or not d2:
                    continue
                d15, d25 = d(st, sj, pl, 5.0), d(st, cj, pl, 5.0)
                r0, r5 = (d1 / d2, d15 / d25) if d1 >= d2 else (d2 / d1, d25 / d15)
                e_ = families.best(r0, None, 'ratio')
                near = e_ or families.outside(r0, None, 'ratio')
                rel = f'{x}: d(star, S Jupiter) / d(star, {C} Jupiter)'
                add(('r', st, frozenset((sj, cj)), pl, near['target']), 'star apex', lin(r0, r5, near['tv']), rel=rel, plane=pl, kind='ratio',
                    tv=near['tv'], v0=r0, score=e_['score'] if e_ else None, C=C)
                mh = midhit(sj, cj, st, pl, d1, d2)
                if mh is not None:
                    add(('r', st, frozenset((sj, cj)), pl, '1'), 'star apex', lin(r0, r5, 1.0), rel=rel, plane=pl, kind='midpoint', tv=1.0, v0=r0,
                        score=mh, C=C)
                b2 = families.best(d2, fp(pl), 'deg')
                if b2:
                    dist('star apex', st, cj, pl, b2, True)
    return ev, pos


def tl_rows(w, P, tid):
    return [x for x in w[P].iter_rows(values_only=True) if x and x[0] == tid and x[3] and not str(x[3]).startswith('———')]


def also_of(n):
    return next((p[5:].split(', ') for p in (n or '').split('; ') if p.startswith('also ')), [])


def kp_of(row, pos):
    if row[6] != 'distance' or row[5] != 'Equator':
        return row[5]
    a, b = row[4].split(' → ')
    return 'Dec' if (pos(a, 0)[1] >= 0) == (pos(b, 0)[1] >= 0) else 'Equator'


bad, det = [], []
in_win = lambda t, sc: -30.0 <= t <= 60.0
long90 = lambda t, sc: sc is not None and sc >= 90.0
for nm, w in (('Ascot', gw), ('Lingfield', lfw)):
    for P in runner_tabs(w):
        for long_ in (False, True):
            ev, pos = star_expect(w, P, long90 if long_ else in_win)
            for C in 'HJ':
                tid = f"{'LONG ' if long_ else ''}TIMELINE {C}"
                rows = tl_rows(w, P, tid)
                idx = {}
                for r in rows:
                    idx.setdefault((r[4], kp_of(r, pos), r[6], round(r[8], 6)), []).append(r)
                mine = [e for e in ev.values() if e['C'] == C]
                n_ok = 0
                for e in mine:
                    k = (e['rel'], 'Dec' if e['kind'] == 'distance' and e['plane'] == 'Equator' and not ((pos(e['rel'].split(' → ')[0], 0)[1] >= 0) != (pos(e['rel'].split(' → ')[1], 0)[1] >= 0)) else e['plane'], e['kind'], round(e['tv'], 6))
                    rr = idx.get(k)
                    if not rr:
                        bad.append((nm, P, tid, 'missing', e['src'], e['rel'], e['plane'], e['kind'], round(e['tv'], 6))); continue
                    r = rr[0]
                    src_ok = r[3] == e['src'] or (r[3] not in SSRC and e['src'] in also_of(r[12]))
                    val_ok = r[9] == round(e['v0'], 6) and (r[10] is None if e['score'] is None else r[10] == round(e['score'], 2))
                    t_ok = long_ or r[2] == round(e['t'], 1)
                    if not (src_ok and val_ok and t_ok):
                        bad.append((nm, P, tid, 'cells', e['src'], e['rel'], e['plane'], r[2:13], round(e['t'], 1), round(e['v0'], 6), e['score']))
                    else:
                        n_ok += 1
                mk = {(e['rel'], e['kind'], round(e['tv'], 6)) for e in mine}
                extra = [r[3:9] for r in rows if r[3] in SSRC and (r[4], r[6], round(r[8], 6)) not in mk]
                bad += [(nm, P, tid, 'extra', x) for x in extra]
                det.append(f'{nm} {P} {tid} {n_ok}')
check('T37 every star event recomputed from POSITIONS (own code: S Jup→star, star→Jup, S Jup on star pair with the T19 filter, star apex; '
      'dedupe in that order, after the table sources): none missing or extra in TIMELINE H / J (window) and LONG TIMELINE H / J (>= 90), '
      'value, score, minutes (TIMELINE) and source / "also" as on the sheet, both races every runner', not bad,
      f"{len(det)} blocks, {sum(int(x.split()[-1]) for x in det)} events; {det[:4]}; {bad[:3]}")
# LONG star events on the rebuilt Ascot: real time (beyond 60 min) crosses the target within ±1 min (engine, orientation fixed at the off);
# "not within 1 year": no crossing in a daily ±1 year scan
gpp = {(k[1], k[2]): v for k, v in gp.items() if k[0] == 'P01'}


def at_m(p, m):
    c, n = p.split(' ', 1)
    return sky_at(n, m) if c == 'S' else gpp[(c, n)]


def f_ev(r, m, flip):
    rel, pl, kind, tv = r[4], r[5], r[6], r[8]
    if kind == 'distance':
        a, b = rel.split(' → ')
        return pdist(at_m(a, m), at_m(b, m), pl) - tv
    if ': d(star, ' in rel:
        x, C = rel.split(':')[0], rel.split('d(star, ')[2][0]
        u, v = pdist(at_m(f'S {x}', m), at_m('S Jupiter', m), pl), pdist(at_m(f'S {x}', m), at_m(f'{C} Jupiter', m), pl)
    else:
        a, b = rel.split(': ')[1].split(' – ')
        u, v = pdist(at_m('S Jupiter', m), at_m(a, m), pl), pdist(at_m('S Jupiter', m), at_m(b, m), pl)
    return ((v / u) if flip else (u / v)) - tv


bad, nreal, nnf = [], 0, 0
for C in 'HJ':
    for r in tl_rows(gw, 'P01', f'LONG TIMELINE {C}'):
        if r[3] not in SSRC:
            continue
        flip = r[6] != 'distance' and f_ev(r, 0, False) + r[8] < 1
        if r[1] == 'not within 1 year':
            nnf += 1
            days = [f_ev(r, dd * 1440, flip) for dd in range(-366, 367)]
            if not all((x > 0) == (days[0] > 0) for x in days):
                bad.append(('nf', r[3:9]))
        elif abs(r[19]) > 60:
            nreal += 1
            if not f_ev(r, r[19] - 1, flip) * f_ev(r, r[19] + 1, flip) < 0:
                bad.append(('real', r[3:9], r[19]))
check('T37 rebuilt Ascot LONG TIMELINE H / J star events: every real time beyond 60 min crosses the target within ±1 min (engine; ratio '
      'orientation fixed at the off); every "not within 1 year" has no crossing in a daily ±1 year scan', not bad and nreal > 0,
      f'{nreal} real times, {nnf} not within 1 year; {bad[:3]}')
# STAR TIMELINE (sky) and STAR TIMELINE H / J = the TIMELINE rows between Jupiter and stars only (own test: no body name, at least one star)
BODYW = re.compile(r'\b(' + '|'.join(b for b in JT.SKY_BODIES + JT.NATAL_BODIES + ['equator'] if b != 'Jupiter') + r')\b')
STW = re.compile(r'\b(' + '|'.join(re.escape(x) for x in sorted(set(JT.STARS) | set(EXPECT67), key=len, reverse=True)) + r')\b')
isstar = lambda rel: bool(STW.search(rel)) and not BODYW.search(STW.sub('', rel))
bad, det = [], []
for nm, w in (('Ascot', gw), ('Lingfield', lfw)):
    for sh, pairs in [('SKY JUPITER', [('TIMELINE', 'STAR TIMELINE')])] + [(P, [(f'TIMELINE {C}', f'STAR TIMELINE {C}') for C in 'HJ']) for P in runner_tabs(w)]:
        for src_t, st_t in pairs:
            allr = [x for x in w[sh].iter_rows(values_only=True) if x and x[0] in (src_t, st_t)]
            # 22 Oct 2026 (test 39): the sky STAR TIMELINE keeps S Jupiter-centred events only and has three more columns
            sky_ = sh == 'SKY JUPITER'
            a_ = [x[1:13] if sky_ else x[1:] for x in allr if x[0] == src_t and isstar(str(x[4] or '')) and not str(x[3]).startswith('———')
                  and (not sky_ or str(x[4]).startswith('S Jupiter'))]
            b_ = [x[1:13] if sky_ else x[1:] for x in allr if x[0] == st_t and not str(x[3]).startswith('———')]
            mk = [x[3] for x in allr if x[0] == st_t and str(x[3]).startswith('———')]
            if a_ != b_ or mk != ['——— OFF ———', '——— OFF + 5 MIN ———']:
                bad.append((nm, sh, st_t, len(a_), len(b_), mk))
            det.append(f'{nm} {sh} {st_t} {len(b_)}')
check('T37 STAR TIMELINE (sky) and STAR TIMELINE H / J = exactly the TIMELINE rows whose relationship is between Jupiter and stars only (same '
      'cells, same order; sky since 22 Oct 2026: S Jupiter-centred only, first 12 cells), with the OFF / OFF + 5 MIN markers, both races', not bad, f'{det[:3]} ...; {bad[:3]}')
# LONG threshold >= 90 (22 Oct 2026): every LONG row scores >= 90 at the off; the >= 80 events of the build before scoring >= 90 all kept
# (compare_tl above); titles
lows = [(sh, x[0], x[10]) for w in (gw, lfw) for sh in ['SKY JUPITER'] + runner_tabs(w) for x in w[sh].iter_rows(values_only=True)
        if x and str(x[0] or '').startswith('LONG TIMELINE') and x[3] and not str(x[3]).startswith('———') and x[1] != 'exact (race-local)'
        and (x[10] is None or x[10] < 90)]
check('T37 every LONG TIMELINE / LONG TIMELINE H / J event scores >= 90 at the off (was >= 80), both races; titles say >= 90', not lows
      and all('scoring >= 90 at the off' in str(x[0]) for x in gw['SKY JUPITER'].iter_rows(values_only=True) if str(x[0] or '').startswith('LONG TIMELINE (')),
      f'{lows[:3]}')
# by hand from POSITIONS (rebuilt Ascot P01): two events per star source
def rowf(tid, rel, pl):
    return next((x for x in tl_rows(gw, 'P01', tid) if x[4] == rel and x[5] == pl), None)


sjp, sjr = gp[('SKY', 'S', 'Jupiter')], rates['Jupiter']
mv = lambda p, r_, m: ((p[0] + m * r_[0]) % 360, p[1] + m * r_[1])
eqd = lambda p, q: abs(abs(p[1]) - abs(q[1]))
dd = lambda p, q, pl: pdist(p, q, pl) if pl != 'Equator' else eqd(p, q)
cases = [  # (block, relationship, plane, kind, target value, score fn, by-hand fn -> (v0, v5))
    ('TIMELINE J', 'S Jupiter → J Meissa', 'RA', 24.14213562373095, lambda v: sq(max(0.005 * 24.142136, 0.025), abs(v - 24.14213562373095)),
     lambda: (dd(sjp, gp[('P01', 'J', 'Meissa')], 'RA'), dd(mv(sjp, sjr, 5), gp[('P01', 'J', 'Meissa')], 'RA'))),
    ('TIMELINE J', 'S Jupiter → J Al Rescha', 'RA', 18 * PHI, lambda v: sq(0.03236, abs(v - 18 * PHI)),
     lambda: (dd(sjp, gp[('P01', 'J', 'Al Rescha')], 'RA'), dd(mv(sjp, sjr, 5), gp[('P01', 'J', 'Al Rescha')], 'RA'))),
]
for tid, rel, pl, tv, scf, hand in cases:
    v0, v5 = hand()
    t_ = (tv - v0) / ((v5 - v0) / 5)
    r = rowf(tid, rel, pl)
    check(f'T37 {tid} {rel} {pl} (S Jup→star) by hand from POSITIONS: {v0:.6f} -> {tv:.6f} ({scf(v0):.2f}), {t_:+.1f} min',
          r is not None and r[3] == 'S Jup→star' and r[9] == round(v0, 6) and r[10] == round(scf(v0), 2) and r[2] == round(t_, 1), f'{r[:13] if r else r}')
# star→Jup (LONG): S Murzim → J Jupiter RA 10×φ^6 real -68.62 days; S Pollux → H Jupiter RA ninth 166.667 not within 1 year
for tid, x, C, tv, scf, real in (('LONG TIMELINE J', 'Murzim', 'J', 10 * PHI ** 6, lambda v: sq(0.005 * 10 * PHI ** 6, abs(v - 10 * PHI ** 6)), True),
                                 ('LONG TIMELINE H', 'Pollux', 'H', 500 / 3, lambda v: 100 * (1.166667 - abs(v - 500 / 3)) / 1.166667, False)):
    v0 = pdist(gp[('SKY', 'S', x)], gp[('P01', C, 'Jupiter')], 'RA')
    r = rowf(tid, f'S {x} → {C} Jupiter', 'RA')
    ok_ = r is not None and r[3] == 'star→Jup' and r[9] == round(v0, 6) and r[10] == round(scf(v0), 2)
    if real:
        ok_ = ok_ and f_ev(r, r[19] - 1, False) * f_ev(r, r[19] + 1, False) < 0 and r[2] == '-68.62 days'
    else:
        ok_ = ok_ and r[1] == 'not within 1 year'
    check(f'T37 {tid} S {x} → {C} Jupiter RA (star→Jup) by hand from POSITIONS: {v0:.6f} ({scf(v0):.2f}), ' + ('real -68.62 days (engine crossing)' if real else 'not within 1 year'),
          ok_, f'{r[:13] if r else r}; {r[19] if r else None}')
# S Jup on star pair: J Mirach – J Menkar RA (3, area A), H Pleiades – H Nunki Equator (3/2, area A)
for tid, C, a, b, pl, tv in (('TIMELINE J', 'J', 'Mirach', 'Menkar', 'RA', 3.0), ('TIMELINE H', 'H', 'Pleiades', 'Nunki', 'Equator', 1.5)):
    X, Y = gp[('P01', C, a)], gp[('P01', C, b)]
    dx, dy = dd(sjp, X, pl), dd(sjp, Y, pl)
    dx5, dy5 = dd(mv(sjp, sjr, 5), X, pl), dd(mv(sjp, sjr, 5), Y, pl)
    r0, r5 = (dx / dy, dx5 / dy5) if dx >= dy else (dy / dx, dy5 / dx5)
    t_ = (tv - r0) / ((r5 - r0) / 5)
    r = rowf(tid, f'S Jupiter: {C} {a} – {C} {b}', pl)
    check(f'T37 {tid} S Jupiter: {C} {a} – {C} {b} {pl} (S Jup on star pair) by hand from POSITIONS: {dx:.6f} / {dy:.6f} = {r0:.6f} on {tv:g} '
          f'({sq(0.02, abs(r0 - tv)):.2f}), {t_:+.1f} min', r is not None and r[3] == 'S Jup on star pair' and r[9] == round(r0, 6)
          and r[10] == round(sq(0.02, abs(r0 - tv)), 2) and r[2] == round(t_, 1), f'{r[:13] if r else r}')
# star apex: H Nunki Equator (15/8, area B 0.15 %), J Sadalsuud Dec (√2, 0.15 %)
for tid, C, x, pl, tv in (('TIMELINE H', 'H', 'Nunki', 'Equator', 15 / 8), ('LONG TIMELINE J', 'J', 'Sadalsuud', 'Dec', 2 ** 0.5)):
    st, cj = gp[('SKY', 'S', x)], gp[('P01', C, 'Jupiter')]
    st5 = mv(st, rates[x], 5)
    d1, d2 = dd(st, sjp, pl), dd(st, cj, pl)
    d15, d25 = dd(st5, mv(sjp, sjr, 5), pl), dd(st5, cj, pl)
    r0, r5 = (d1 / d2, d15 / d25) if d1 >= d2 else (d2 / d1, d25 / d15)
    t_ = (tv - r0) / ((r5 - r0) / 5)
    sc_ = sq(0.15, abs((r0 / tv - 1) * 100))
    r = rowf(tid, f'{x}: d(star, S Jupiter) / d(star, {C} Jupiter)', pl)
    tcheck = (r[2] == round(t_, 1)) if r and not tid.startswith('LONG') else (r is not None and r[19] == round(t_, 1))
    check(f'T37 {tid} {x}: d(star, S Jupiter) / d(star, {C} Jupiter) {pl} (star apex) by hand from POSITIONS: {d1:.6f} / {d2:.6f} = {r0:.6f} '
          f'({sc_:.2f}), {t_:+.1f} min', r is not None and r[3] == 'star apex' and r[9] == round(r0, 6) and r[10] == round(sc_, 2) and tcheck,
          f'{r[:13] if r else r}')
# Test 38 (Eddie, 22 Oct 2026): LONG STAR TIMELINE (sky) and LONG STAR TIMELINE H / J = the LONG TIMELINE rows between Jupiter and stars only;
# every other row unchanged. "Before" = commit 632447ff.
print('test 38: LONG STAR TIMELINE')
out38 = {}
for nm, bo, after in (('Lingfield', lf_t, lf_u), ('Ascot', gf_t, gf_u)):    # 632447ff -> 00b6db9e (the builds above)
    out38[nm] = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_longstar/check_longstar.py', bo, after], capture_output=True, text=True).stdout
W38 = {'Ascot': {'SKY JUPITER LONG STAR TIMELINE': '59 (28 / 31)', 'P01 LONG STAR TIMELINE H': '45 (21 / 24)', 'P01 LONG STAR TIMELINE J': '44 (21 / 23)'},
       'Lingfield': {'SKY JUPITER LONG STAR TIMELINE': '3 (0 / 3)', 'P01 LONG STAR TIMELINE H': '3 (1 / 2)', 'P01 LONG STAR TIMELINE J': '3 (0 / 3)',
                     'P03 LONG STAR TIMELINE H': '3 (1 / 2)', 'P03 LONG STAR TIMELINE J': '4 (1 / 3)', 'P05 LONG STAR TIMELINE H': '4 (2 / 2)',
                     'P05 LONG STAR TIMELINE J': '3 (1 / 2)', 'P07 LONG STAR TIMELINE H': '4 (3 / 1)', 'P07 LONG STAR TIMELINE J': '3 (1 / 2)',
                     'P09 LONG STAR TIMELINE H': '3 (2 / 1)', 'P09 LONG STAR TIMELINE J': '3 (1 / 2)', 'P11 LONG STAR TIMELINE H': '4 (1 / 3)',
                     'P11 LONG STAR TIMELINE J': '2 (1 / 1)'}}
got38 = {nm: {f'{m.group(1)} {m.group(2)}': m.group(3) for m in re.finditer(r'^(\S+(?: JUPITER)?)\s+(LONG STAR TIMELINE(?: [HJ])?)\s+(\d+ \(\d+ / \d+\))$', o, re.M)}
         for nm, o in out38.items()}
check('T38 LONG STAR TIMELINE (sky) / LONG STAR TIMELINE H / J, both races --full (chk_longstar/check_longstar.py): every row = a row of the '
      'matching LONG TIMELINE (identical cells and fills), every LONG row between Jupiter and stars only in it, none missing or extra, same order, '
      'SEPARATING / APPLYING with their counts, title counts, every row >= 90; every other row of every sheet identical to the build before '
      '(commit 632447ff); counts (separating / applying) as reported', all(line(o, 'mismatches:') == 'mismatches: 0' for o in out38.values())
      and got38 == W38, f"{ {k: line(o, 'mismatches:') for k, o in out38.items()} }; {got38['Ascot']}")
# sort (own check): inside each section by score at the off, highest first; ties: separating most recent first, applying soonest first
bad = []
for nm, w in (('Ascot', gw), ('Lingfield', lfw)):
    for sh in ['SKY JUPITER'] + runner_tabs(w):
        for tid in ('LONG STAR TIMELINE', 'LONG STAR TIMELINE H', 'LONG STAR TIMELINE J'):
            sec, parts = None, {}
            for x in w[sh].iter_rows(values_only=True):
                if x and x[0] == tid:
                    if str(x[3]).startswith('———'):
                        sec = x[3].split()[1].rstrip(':'); parts[sec] = []
                    else:
                        parts[sec].append(x)
            for sec, rs in parts.items():
                nf = lambda x: x[1] == 'not within 1 year'
                # scores on the sheet are rounded to 2 dp: two rows may show the same score with different unrounded scores (e.g. Ascot SKY
                # 95.3332 before 95.3325), so the time tie-break is checked only where the next row's shown score is not lower (unrounded order kept)
                sc = [x[10] for x in rs]
                if sc != sorted(sc, reverse=True) or any((x[11] == 'separating') != (sec == 'SEPARATING') for x in rs):
                    bad.append((nm, sh, tid, sec))
check('T38 LONG STAR TIMELINE sections in order (own check): by score at the off, highest first (shown 2-dp scores never rise; the time '
      'tie-break is the LONG TIMELINE order, compared row for row above); separating / applying in the right section', not bad, f'{bad[:3]}')
# Test 39 (Eddie, 22 Oct 2026): sky STAR / LONG STAR TIMELINE trimmed to S Jupiter-centred events, 95 / 100 / 95 times; runner T24 STAR
# SELECT tables. "Before" = commit 00b6db9e.
print('test 39: sky star timelines trimmed, 95 / 100 / 95 (T24 STAR SELECT removed)')
out39 = {}
for nm, inp, after, bfull, bdef in (('Lingfield', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx', lf, lf_u, lf_ud),
                                    ('Ascot', f'{tmp}/race_batch_20120619_ascot_1430.xlsx', gf, gf_u, gf_ud)):
    for fl in ('--full', None):
        # 22 Oct 2026 (T24 repeats): the "after" is the build by 5e10f7bf's code (before the repeats), so this keeps checking its own change
        ao = H5E[(nm.lower(), 'full' if fl else 'def')]
        out39[(nm, fl or 'default')] = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_select/compare_sel.py', bfull if fl else bdef, ao],
                                                      capture_output=True, text=True).stdout
DROP39 = {'Ascot': ('SKY JUPITER LONG STAR TIMELINE: before 59, after 45, dropped 14: S Aculeus – S Rukbat RA 16×φ (golden) (99.87); S Antares – '
                    'S Alphard Dec 17.7778 (ninth) (96.89)'), 'Lingfield': 'SKY JUPITER LONG STAR TIMELINE: before 3, after 2, dropped 1: S Sirius – S Rigel RA 14×φ (golden) (92.35)'}
check('T39 against the build before (commit 00b6db9e), both races, default and --full (chk_select/compare_sel.py): sky STAR / LONG STAR '
      'TIMELINE = before minus exactly the star-to-star distance events (Ascot LONG 14, e.g. S Aculeus – S Rukbat RA 16×φ; STAR 0; Lingfield '
      'LONG 1, S Sirius – S Rigel RA 14×φ), every remaining row S Jupiter-centred, its cells identical, the header + "> 95 since", "100", '
      '"< 95 from"; every other row identical (T24 STAR SELECT removed the same day: none on the runner sheets)',
      all(line(o, 'mismatches:') == 'mismatches: 0' for o in out39.values()) and all(DROP39[k[0]] in o for k, o in out39.items())
      and all('STAR TIMELINE: before 65, after 65, dropped 0' in o for k, o in out39.items() if k[0] == 'Ascot'),
      f"{ {k: line(o, 'mismatches:') for k, o in out39.items()} }")
# (b) every 95 / 100 / 95 cell re-searched with the engine (own score code from POSITIONS + engine; families.py for the targets)
_s.path.insert(0, 'tools/jup2')
import motion as MO2


def sky_engine(w, off, race, batch):
    jd = EN._to_jd_ut(EN._parse_time(off, 'Europe/London'))
    site = MO2.off_and_site(race, 'TRANS', batch, None, None)[1]
    b0 = EN.bodies_at(jd, *site, False)
    sk = {x[3]: x for x in w['POSITIONS'].iter_rows(min_row=5, values_only=True) if x and x[0] == 'SKY' and x[3]}
    cache = {}

    def at(p, m):
        if m not in cache:
            cache[m] = EN.bodies_at(jd + m / 1440.0, *site, False)
        eb = p + '_B' if sk[p][4] == 'star' else p
        b = cache[m]
        return ((sk[p][5] + (b[eb]['ra'] - b0[eb]['ra'] + 180) % 360 - 180) % 360, sk[p][6] + b[eb]['dec'] - b0[eb]['dec'])
    return at


def dpl(p, q, pl):
    if pl == 'RA':
        x = abs(p[0] - q[0]) % 360
        return min(x, 360 - x)
    return abs(p[1] - q[1]) if pl == 'Dec' else abs(abs(p[1]) - abs(q[1]))


def own_score(at, r, m, big, side):
    rel, pl, kind, tgt = r[4], r[5], r[6], r[7]
    if kind == 'distance':
        a, b = rel.split(' → ')
        lab, fam = tgt.rsplit(' (', 1)
        v = dpl(at(a[2:], m), at(b[2:], m), pl)
        return next((d['score'] for d in families.evaluate(v, pl if pl in ('RA', 'Dec') else None, 'deg') if d['family'] == fam[:-1] and d['target'] == lab), 0.0)
    x, y = rel.split(': ')[1].split(' – ')
    J, X, Y = at('Jupiter', m), at(x[2:], m), at(y[2:], m)
    dx, dy = dpl(J, X, pl), dpl(J, Y, pl)
    if kind == 'ratio':
        v = dx / dy if big else dy / dx
        return next((d['score'] for d in families.evaluate(v, None, 'ratio') if d['target'] == tgt.split(' · ')[0]), 0.0)
    close = 100 * min(dx, dy) / max(dx, dy)
    if 100 - close > 10:
        return 0.0
    if pl == 'RA':
        mid = (X[0] + ((Y[0] - X[0] + 180) % 360 - 180) / 2) % 360
        near, far = (J[0] - mid + 180) % 360 - 180, (J[0] - mid) % 360 - 180
        off, tol = (near if side == 'near' else far), 0.5
    else:
        f = (lambda v: v) if pl == 'Dec' else abs
        off, tol = f(J[1]) - (f(X[1]) + f(Y[1])) / 2, 0.15
    if abs(off) > tol:
        return 0.0
    return 0.5 * (10 * (10 - (100 - close)) / 10) ** 2 + 0.5 * (10 * (tol - abs(off)) / tol) ** 2


def mins_of(cell):
    if cell in ('—', 'not within 1 year'):
        return cell
    t = cell.split('(')[1].rstrip(')').replace('−', '-')
    return float(t.split()[0]) * (1440 if 'days' in t else 1)


bad, n95, nd, nnf = [], 0, 0, 0
for nm, w, off, race, batch in (('Ascot', gw, '2012-06-19 14:30', 'ascot_1430_20120619', f'{tmp}/race_batch_20120619_ascot_1430.xlsx'),
                                ('Lingfield', lfw, '2021-04-02 14:35', 'lingfield_aw_1435_20210402', 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx')):
    at = sky_engine(w, off, race, batch)
    for tid, c95 in (('STAR TIMELINE', 13), ('LONG STAR TIMELINE', 15)):
        for r in w['SKY JUPITER'].iter_rows(values_only=True):
            if not (r and r[0] == tid and r[3] and not str(r[3]).startswith('———')):
                continue
            big = side = None
            if r[6] != 'distance':
                x, y = r[4].split(': ')[1].split(' – ')
                J, X, Y = at('Jupiter', 0), at(x[2:], 0), at(y[2:], 0)
                big = dpl(J, X, r[5]) >= dpl(J, Y, r[5])
                if r[5] == 'RA':
                    mid = (X[0] + ((Y[0] - X[0] + 180) % 360 - 180) / 2) % 360
                    side = 'near' if abs((J[0] - mid + 180) % 360 - 180) <= abs((J[0] - mid) % 360 - 180) else 'far'
            sc = lambda m: own_score(at, r, m, big, side)
            since, exact, frm = (mins_of(v) for v in r[c95:c95 + 3])
            if since == '—':
                nd += 1
                m0 = 0.0 if exact == 'not within 1 year' else exact
                if not (frm == '—' and sc(m0) < 95):
                    bad.append((nm, tid, r[4], r[5], 'dash', sc(m0)))
                continue
            for v, sgn in ((since, -1), (frm, 1)):
                if v == 'not within 1 year':
                    nnf += 1
                    m0 = 0.0 if exact == 'not within 1 year' else exact
                    if not all(sc(m0 + sgn * dd * 1440) >= 95 for dd in range(1, 367)):
                        bad.append((nm, tid, r[4], r[5], 'nf', sgn))
                    continue
                n95 += 1
                dm = 8.0 if abs(v) >= 1440 else 1.0               # shown in days beyond a day (0.01 day = 14.4 min): ±8 min
                ins, outs = sc(v - sgn * dm), sc(v + sgn * dm)      # inside the 95 window on the exact-time side, outside beyond
                if not (ins >= 95 > outs):
                    bad.append((nm, tid, r[4], r[5], 'since' if sgn < 0 else 'from', v, round(ins, 3), round(outs, 3)))
check('T39 every "> 95 since" / "< 95 from" cell of the sky STAR / LONG STAR TIMELINE re-searched (own score code: family / interval on its own '
      'tolerance, midpoint total; engine positions): the score is >= 95 one minute inside and < 95 one minute outside (8 min for a cell shown '
      'in days, 0.01 day); "—" only where the score '
      'is under 95 at the exact time; "not within 1 year" by a daily ±1 year scan; both races', not bad and n95 > 0,
      f'{n95} crossings, {nd} dashes, {nnf} not within 1 year; {bad[:3]}')
# (c) T24 STAR SELECT removed (Eddie, 22 Oct 2026, the same day): no T24 STAR SELECT title or row on any sheet (both races, --full)
left = [(nm, sh) for nm, w in (('Ascot', gw), ('Lingfield', lfw)) for sh in w.sheetnames
        if any(x and any('T24 STAR SELECT' in str(v) for v in x[:2] if v) for x in w[sh].iter_rows(max_col=2, values_only=True))]
check('T39 T24 STAR SELECT removed (22 Oct 2026): no T24 STAR SELECT title or row on any sheet, both races (--full)', not left, f'{left[:5]}')
# 95 crossing: S Jupiter → S Castor RA on 54 (whole, ±0.02): score 95 at |v − 54| = 0.02 (1 − √0.95) = 0.000506
at = sky_engine(gw, '2012-06-19 14:30', 'ascot_1430_20120619', f'{tmp}/race_batch_20120619_ascot_1430.xlsx')
r = next(x for x in gw['SKY JUPITER'].iter_rows(values_only=True) if x and x[0] == 'STAR TIMELINE' and x[4] == 'S Jupiter → S Castor' and x[5] == 'RA')
dv = lambda m: dpl(at('Jupiter', m), at('Castor', m), 'RA') - 54
since, frm = mins_of(r[13]), mins_of(r[15])
lim = 0.02 * (1 - 0.95 ** 0.5)
check(f'T39 STAR TIMELINE S Jupiter → S Castor RA (54 whole) by hand with the engine: score 95 where |d − 54| = {lim:.6f}; "> 95 since" {r[13]}, '
      f'"100" {r[14]}, "< 95 from" {r[15]}', abs(dv(since - 1)) > lim > abs(dv(since + 1)) and abs(dv(frm + 1)) > lim > abs(dv(frm - 1)),
      f'd−54 at since ±1: {dv(since - 1):+.6f} / {dv(since + 1):+.6f}; at from ±1: {dv(frm - 1):+.6f} / {dv(frm + 1):+.6f}')
# ---------------------------------------------------------------------------------------------------------------------------------
# Test 40 (Eddie, 22 Oct 2026): T24 STAR SELECT removed from the runner sheets; every other block unchanged. "Before" = commit 0ad7d2e5.
print('test 40: T24 STAR SELECT removed')
out40 = {}
for n in ('lingfield', 'ascot'):
    for f in ('full', 'def'):
        ao = f'{tmp}/after40/{n}_{f}_jupiter_tables.xlsx'
        os.makedirs(f'{tmp}/after40', exist_ok=True)
        inp = 'reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx' if n == 'lingfield' else f'{tmp}/race_batch_20120619_ascot_1430.xlsx'
        subprocess.run([sys.executable, 'tools/jupiter_tables.py', inp] + (['--full'] if f == 'full' else []) + ['--out', ao], capture_output=True, text=True)
        # 22 Oct 2026 (T24 repeats): the comparison runs on the builds by 5e10f7bf's code (the removal alone); ao (now) feeds test 41
        out40[(n, f)] = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_rmsel/compare_rmsel.py', H0A[(n, f)], H5E[(n, f)],
                                        H0A[(n, f)].replace('_jupiter_tables', '_pairs'), ao.replace('_jupiter_tables', '_pairs')],
                                       capture_output=True, text=True).stdout
RM40 = {'lingfield': 'removed 22 (13 T24 STAR SELECT rows, 2 tables)', 'ascot': 'removed 372 (237 T24 STAR SELECT rows, 28 tables)'}
check('T40 against the build before (commit 0ad7d2e5), both races, default and --full (chk_rmsel/compare_rmsel.py): each runner sheet = the '
      'build before minus exactly the T24 STAR SELECT tables and their blank rows (Ascot P01 28 tables, 372 rows; Lingfield 2 tables, 22 rows '
      'per runner), every other row of every sheet identical (values, fills, comments, borders, number formats; merged ranges shifted); pairs '
      'workbooks identical', all(line(o, 'mismatches:') == 'mismatches: 0' and 'pairs identical' in o for o in out40.values())
      and all(sum(1 for x in o.splitlines() if RM40[k[0]] in x) == (1 if k[0] == 'ascot' else 6) for k, o in out40.items()),
      f"{ {k: line(o, 'mismatches:') for k, o in out40.items()} }")
src = open('tools/jupiter_tables.py').read()
check('T40 code: write_t24sel, star_select and SEL_NOTE gone; t24r_cell back to its 19 Oct form (no tags parameter)',
      not any(z in src for z in ('def write_t24sel', 'def star_select', 'SEL_NOTE', 'ctx.sel', 'tags=')), '')
# ---------------------------------------------------------------------------------------------------------------------------------
# Test 41 (Eddie, 22 Oct 2026): T24 repeats flag - T24 SKY / HORSE / JOCKEY: the same best target (family + target number, no x10 / /10
# folding; conjunction cells out) in two or more body cells of a star row; "repeats" column, dotted outline (thick midpoint outline kept),
# comment line, title counts. "Before" = commit 5e10f7bf.
print('test 41: T24 repeats flag')
out41 = {}
for (n, f), bo in H5E.items():
    ao = f'{tmp}/after40/{n}_{f}_jupiter_tables.xlsx'           # the current builds of test 40
    out41[(n, f)] = subprocess.run([sys.executable, 'tools/scans/families_audit/chk_t24rep/check_rep.py', bo, ao], capture_output=True, text=True).stdout
check('T41 against the build before (commit 5e10f7bf), both races, default and --full (chk_t24rep/check_rep.py): every repeats cell of T24 SKY / '
      'HORSE / JOCKEY recomputed from POSITIONS (own code, families.evaluate: best target per cell, conjunction cells out, every target in >= 2 '
      'cells with its cells, scores and order; none missing or extra); dotted outline exactly on repeated cells (thick kept on midpoint cells); '
      'comment = before + the repeat lines; title = the counts; header "repeats"; every other cell of every sheet identical (values, fills, '
      'comments, borders, formats)', all(line(o, 'mismatches:') == 'mismatches: 0' for o in out41.values())
      and all('SKY JUPITER T24 SKY: 24 / 67 rows, 27 targets' in o for k, o in out41.items() if k[0] == 'ascot')
      and all('SKY JUPITER T24 SKY: 8 / 21 rows, 8 targets' in o for k, o in out41.items() if k[0] == 'lingfield'),
      f"{ {k: line(o, 'mismatches:') for k, o in out41.items()} }")
# by hand from POSITIONS (rebuilt Ascot P01, --full after): an RA–Dec repeat, a Dec–Dec repeat, a midpoint body cell that is also a repeat
w41 = openpyxl.load_workbook(f'{tmp}/after40/ascot_full_jupiter_tables.xlsx')
pp = {(x[2], x[3]): (x[5], x[6]) for x in w41['POSITIONS'].iter_rows(min_row=5, values_only=True) if x and x[0] == 'P01' and x[3]}
rows41 = list(w41['P01'].iter_rows())


def t24cell(tid, lab, body, pl):
    i = next(k for k, r in enumerate(rows41) if r[0].value == 'T24' and str(r[1].value).startswith(tid))
    h1, h2 = rows41[i + 1], rows41[i + 2]
    cm = [k for k, c in enumerate(h1) if c.value in ('RA midpoints', 'Dec midpoints')]
    r = next(r for r in rows41[i + 3:i + 80] if r[1].value == lab)
    lo, hi = (2, cm[0]) if pl == 'RA' else (cm[0] + 1, cm[1])
    return r[next(k for k in range(lo, hi) if h2[k].value == body)], r[cm[1] + 1].value


SILVER = 10 * (1 + 2 ** 0.5)
tol = max(SILVER * 0.005, 0.025)
a, b = dpl(pp[('H', 'Menkent')], pp[('H', 'Makemake')], 'RA'), dpl(pp[('H', 'Menkent')], pp[('H', 'Rahu')], 'Dec')
sa_, sb_ = sq(tol, abs(a - SILVER)), sq(tol, abs(b - SILVER))
ca, rp = t24cell('T24 HORSE', 'H Menkent', 'Makemake', 'RA')
cb, _ = t24cell('T24 HORSE', 'H Menkent', 'Rahu', 'Dec')
want = f'24.14 silver ×2 (Makemake RA ({sa_:.2f}), Rahu Dec ({sb_:.2f}))'
check(f'T41 RA–Dec repeat by hand from POSITIONS: T24 HORSE H Menkent – H Makemake RA {a:.6f}, H Menkent – H Rahu Dec {b:.6f}, both silver '
      f'24.14 (10 (1 + √2), tol {tol:.6f}): {sa_:.2f} / {sb_:.2f}; repeats cell {rp!r}', want in (rp or '') and
      ca.border.left.style == 'dotted' and cb.border.left.style == 'dotted'
      and ca.comment.text.endswith(f'repeat: 24.14 silver ×2 (with Rahu Dec ({sb_:.2f}))')
      and cb.comment.text.endswith(f'repeat: 24.14 silver ×2 (with Makemake RA ({sa_:.2f}))'), f'{ca.comment.text!r}; {cb.comment.text!r}')
lo_, hi_, ntol, nt = next(z for z in families._NINTH_RANGES if abs(z[3] - 16.666667) < 1e-5)
a, b = dpl(pp[('J', 'Orion Nebula Cluster')], pp[('J', 'Uranus')], 'Dec'), dpl(pp[('J', 'Orion Nebula Cluster')], pp[('J', 'Gonggong')], 'Dec')
sa_, sb_ = 100 * (ntol - abs(a - nt)) / ntol, 100 * (ntol - abs(b - nt)) / ntol
ca, rp = t24cell('T24 JOCKEY', 'J Orion Nebula Cluster', 'Uranus', 'Dec')
cb, _ = t24cell('T24 JOCKEY', 'J Orion Nebula Cluster', 'Gonggong', 'Dec')
check(f'T41 Dec–Dec repeat by hand from POSITIONS: T24 JOCKEY J Orion Nebula Cluster – J Uranus Dec {a:.6f}, – J Gonggong Dec {b:.6f}, ninth '
      f'16.6667 (range {lo_} – {hi_}, tol {ntol}, linear): {sa_:.2f} / {sb_:.2f}; repeats cell {rp!r}',
      rp == f'16.6667 ninth ×2 (Uranus Dec ({sa_:.2f}), Gonggong Dec ({sb_:.2f}))' and lo_ <= a < hi_ and lo_ <= b < hi_
      and ca.border.left.style == cb.border.left.style == 'dotted', f'{ca.comment.text!r}')
# midpoint body cell + repeat: H Castor RA, ninth 144.444 ×3 (Quaoar, Rahu, Vesta); the thick-outlined one keeps thick, the others dotted
cells = {B: t24cell('T24 HORSE', 'H Castor', B, 'RA')[0] for B in ('Quaoar', 'Rahu', 'Vesta')}
rp = t24cell('T24 HORSE', 'H Castor', 'Quaoar', 'RA')[1]
lo_, hi_, ntol, nt = next(z for z in families._NINTH_RANGES if abs(z[3] - 144.444444) < 1e-4)
vals = {B: dpl(pp[('H', 'Castor')], pp[('H', B)], 'RA') for B in cells}
scs = {B: 100 * (ntol - abs(v - nt)) / ntol for B, v in vals.items()}
thick = [B for B, c in cells.items() if c.border.left.style == 'thick']
check(f'T41 midpoint cell that is also a repeat, by hand from POSITIONS: T24 HORSE H Castor RA Quaoar / Rahu / Vesta '
      f'{" / ".join(f"{v:.6f}" for v in vals.values())}, ninth 144.444 (tol {ntol}): {" / ".join(f"{v:.2f}" for v in scs.values())}; thick '
      f'(midpoint) {thick}, kept, with both comment lines; the others dotted; repeats cell {rp!r}',
      rp.startswith('144.444 ninth ×3 (' + ', '.join(f'{B} RA ({scs[B]:.2f})' for B in sorted(scs, key=lambda z: -scs[z])) + ')') and len(thick) >= 1
      and all('midpoint with ' in cells[B].comment.text and 'repeat: 144.444 ninth ×3' in cells[B].comment.text for B in thick)
      and all(cells[B].border.left.style == 'dotted' for B in cells if B not in thick), f'{[cells[B].comment.text for B in thick]}')
shutil.rmtree(tmp, ignore_errors=True)
print(f'\n{sum(RES)}/{len(RES)} passed')
sys.exit(0 if all(RES) else 1)
