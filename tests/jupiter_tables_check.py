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
Test 13 (Eddie 14 Oct): T18 - equidistance pair side by side for horse and jockey (block 1 S Jupiter, block 2 natal Jupiters);
'both' tag and count. Test 14: T19 sky Jupiter on natal pairs, P## PAIRS, SKY STARS. (No Messi workbook in the repo: that check skipped.)"""
import os, subprocess, sys
import openpyxl
from openpyxl.cell.rich_text import CellRichText

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
os.chdir(REPO)
GREEN, YELLOW, LIGHT = '00C6EFCE', '00FFEB9C', '00FFF8DC'
COL = {'RA': 2, 'Dec': 11, 'Flat': 20, 'GC': 29}           # 0-based column of each plane's value (tables with 4 planes, 9 columns each)
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
for P, inv in (('P05', ' (inverted)'), ('P11', '')):
    r = row(wb[P], 'T12', lab)
    v, t, o, f, sc = cell(r, 'Flat')
    check(f'{P} T12 {lab} Flat -> 1 · unison · Perfect{inv}, also cell "unison: field 2/6"',
          t == f'1 · unison · Perfect{inv}' and r[COL['Flat'] + 7].value == 'unison: field 2/6', f'{v} {t} {o} {sc} {r[COL["Flat"] + 7].value}')
rs = [x for x in wb['P05 RATIOS'].iter_rows(values_only=True) if x[6] == '1' and x[1] == 'T12' and x[3] == 'Flat']
check('P05 RATIOS: the Flat unison row with field 2/6', len(rs) == 1 and rs[0][11] == '2/6', str(rs))
f12, pl = [], None
for x in wb['FIELD 12'].iter_rows(values_only=True):
    pl = x[0] if x[0] in ('RA', 'Dec', 'Flat', 'GC') else pl
    if pl == 'Flat' and x[0] == lab:
        f12.append(x)
check('FIELD 12 (Flat) tags it "field 2/6" for P05 and P11', len(f12) == 1 and sum(isinstance(v, str) and 'field 2/6' in v for v in f12[0][1:]) == 2, str(f12))

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
v, t, o, f, sc = cell(row(ws, 'T13', 'S Jupiter–J Pluto / J Jupiter–J Pluto'), 'GC')
check('GC unison J Pluto genuine (d(SJ,JJ) 0.522937 / d(JJ,JPluto) 101.36785 = 0.005159): coloured; 1 % tolerance -> 74.77 yellow',
      t == '1 · unison · Perfect' and f == YELLOW and sc == 74.77,
      f'{v} {t} {sc} {f}')
rs = [x for x in wb['P09 RATIOS'].iter_rows(values_only=True) if x[6] == '1']
na = sum('automatic' in x[11] for x in rs)
gp = sorted(x[3] for x in rs if 'automatic' not in x[11])
check("Cobden's 61 unisons (1 % tolerance): 20 automatic (all RA), 41 genuine (Flat 20, GC 20, RA 1)",
      len(rs) == 61 and na == 20 and all(x[3] == 'RA' for x in rs if 'automatic' in x[11])
      and (gp.count('Flat'), gp.count('GC'), gp.count('RA')) == (20, 20, 1), f'{len(rs)} rows, {na} automatic, genuine {gp}')
rb = [x for x in wb['P07 RATIOS'].iter_rows(values_only=True) if x[6] == '1']
check('River Bray (P07) T13 J Pluto GC unison: field 2/6 — Cobden\'s J Pluto GC unison is genuine under the per-plane rule',
      len(rb) == 1 and rb[0][3] == 'GC' and rb[0][11] == '2/6', str(rb))

g = [x for x in rs if 'automatic' not in x[11]]
check("Cobden's 41 genuine unisons all tagged return-assisted, field count kept (two at 2/6)",
      len(g) == 41 and all(x[11].endswith(' return-assisted') for x in g) and sum(x[11].startswith('2/6') for x in g) == 2, str([x[11] for x in g][:3]))
check("River Bray's J Pluto GC (d1/d2 0.917) not tagged", rb[0][11] == '2/6', rb[0][11])
heads = [x[0] for x in wb['P03 RATIOS'].iter_rows(values_only=True) if x[0] in ('Perfect', 'Imperfect', 'Dissonant', 'Septimal', 'Harmonic', 'High', 'Phi') and x[1] is None]
check('P03 RATIOS: no empty group header (no Harmonic section)', 'Harmonic' not in heads, str(heads))

print('\nTest 7: Sandown 14:25 2021 (batch xlsx) — tapered ratio tolerances, nearest target outside the tolerance')
wb = openpyxl.load_workbook('reference/classic/race_batch_20211204_sandown_1425_jupiter_tables.xlsx')   # built in test 4
ws = wb['P05']
r = row(ws, 'T12', 'S Jupiter–S Mars / H Jupiter–H Mars')
v, t, o, f, sc = cell(r, 'RA')
check('P05 T12 RA S Jupiter–S Mars / H Jupiter–H Mars 1.002631 -> unison inside 1 %, +0.26308 %, score 54.31, yellow',
      round(v, 6) == 1.002631 and t == '1 · unison · Perfect (inverted)' and o == '+0.26308%' and sc == 54.31 and f == YELLOW, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(r, 'Flat')
check('same row Flat 1.0445 outside every band: nearest by tightness unison +4.44999 % (4.45 tolerances; 16/15 is 13.9), plain',
      t == '1 · unison · Perfect — outside ±1 % (inverted)' and o == '+4.44999%' and sc is None and f is None
      and r[COL['Flat'] + 3].value is None, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(ws, 'T12', 'S Jupiter–S Haumea / J Jupiter–J Haumea'), 'Flat')
check('3/2 on 0.333 % (k = 3): P05 T12 Flat Haumea 1.506122, +0.40816 % now outside ±0.333 %, plain',
      t == '3/2 · fifth · Perfect — outside ±0.333 %' and o == '+0.40816%' and sc is None and f is None, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(ws, 'T12', 'S Jupiter–S Makemake / H Jupiter–H Makemake'), 'Flat')
check('3/2 hit on 0.333 %: P05 T12 Flat Makemake 1.499624, -0.02508 %, score (10 (1/3 − 0.02508) / (1/3))² = 85.52, green',
      t == '3/2 · fifth · Perfect' and o == '-0.02508%' and sc == 85.52 and f == GREEN, f'{v} {t} {o} {sc} {f}')
v, t, o, f, sc = cell(row(wb['P09'], 'T12', 'S Jupiter–S Mars / H Jupiter–H Mars'), 'Flat')
check('9/8 on 0.15 %: P09 T12 Flat Mars 1.125048, +0.00428 %, score (10 (0.15 − 0.00428) / 0.15)² = 94.37, green',
      t == '9/8 · major second · Dissonant' and o == '+0.00428%' and sc == 94.37 and round((10 * (0.15 - 0.0042844) / 0.15) ** 2, 1) == 94.4
      and f == GREEN, f'{v} {t} {o} {sc} {f}')
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
need = ['S Jup→H Uranus Dec 11.10793 → 11.1111 (94.80) [T5]', 'S Uranus→H Jup GC 142.001746 → 142 (83.30) [T7]',
        'S Uranus→J Jup Dec 18.995206 → 19 (57.80) [T8]']
check('Dynamic Force Uranus cell lists the three hits', all(x in df for x in need), str(df[:8]))
check('Dynamic Force Uranus tags: mutual, same chart · mutual, across charts · both Jupiters · both charts · directions 4',
      df[0] == 'mutual, same chart · mutual, across charts · both Jupiters · both charts · directions 4', df[0])
check('cells list hits >= 50 only; a repeat (same family, same digits) shown once: main kept unless the scaled form is > 0.5 higher '
      '(unrounded): 11.10793 main (/10 only +0.0016), 14.141031 as /10 1.414 (99.12 vs 96.9), 145.643439 as /10 9×φ (87.80 vs 13.7); '
      '"+ 9 weaker" (score-0 and hidden repeats not counted)',
      df[-1] == '+ 9 weaker (see T-tables)' and not any('/10: 1.110793' in x for x in df)
      and 'J Jup→H Uranus Dec 14.141031 /10: 1.414103 → 1.414 (99.12) [T4, scaled]' in df
      and not any(x.startswith('J Jup→H Uranus Dec 14.141031 → 14.14') for x in df)
      and all(float(x.rsplit('(', 1)[1].split(')')[0]) >= 50 for x in df[1:-1] if not x.startswith('mid ')), df[-1])
cnt = [c.value for c in ur[head.index('runners: mutual, same chart'):]]
check('Uranus field counts: mutual same chart 1/5, across charts 2/5 (P01, P07), both Jupiters 1/5, either 2/5', cnt == ['1/5', '2/5', '1/5', '2/5'], str(cnt))

print('\nTest 9: Wincanton 14:20 2022 — NUMBERS, the 7.777 (ninth) row, P07 River Bray / Alan Johns')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20220321_wincanton_1420.xlsx'), rich_text=True)
nr = [r for r in wb['P07 NUMBERS'].iter_rows(min_row=4, values_only=True) if r[0] == 'ninth: 7.77778 / 77.7778']
check('P07 NUMBERS row "ninth: 7.77778 / 77.7778" tagged sky + horse + jockey', len(nr) == 1 and nr[0][1] == 'sky + horse + jockey', str(nr))
sky, horse, jock = (str(nr[0][k]).split('\n') for k in (2, 3, 4))
check('SKY S Jupiter → S Ceres 77.75345 (80.96), HORSE H Jupiter → H Rigel 7.777589 (98.52), JOCKEY J Jupiter → J Haumea 77.798638 (83.67)',
      'S Jup→S Ceres RA 77.75345 → 77.7778 -0.02433 (80.96)' in sky and 'H Jup→H Rigel RA 7.777589 → 7.77778 -0.00019 (98.52)' in horse
      and 'J Jup→J Haumea GC 77.798638 → 77.7778 +0.02086 (83.67)' in jock, f'{sky} {horse} {jock}')
nh = [c.value for c in wb['P07 NUMBERS'][3]]
lines = [x for r in wb['P07 NUMBERS'].iter_rows(min_row=4, values_only=True) for c in r[2:] if c for x in str(c).split('\n')]
check('NUMBERS: HORSE = T1, JOCKEY = T2 only - no H–J column, no cross-chart line (H Jup→J X, J Jup→H X)',
      nh[:6] == ['number', 'tag', 'SKY', 'HORSE', 'JOCKEY', 'SKY→NATAL'] and not any(x.startswith(('H Jup→J ', 'J Jup→H ')) for x in lines), str(nh))
fnr = [r[0] for r in wb['FIELD NUMBERS'].iter_rows(min_row=4, values_only=True)]
check('FIELD NUMBERS (within-chart only): sqrt2 0.707 / 70.7 drops out; 5 numbers left',
      len(fnr) == 5 and not any(str(x).startswith('sqrt2') for x in fnr), str(fnr))
fn = [r for r in wb['FIELD NUMBERS'].iter_rows(min_row=4, values_only=True) if r[0] == 'ninth: 7.77778 / 77.7778']
head = [c.value for c in wb['FIELD NUMBERS'][3]]
check('FIELD NUMBERS lists the number with P07 as holder', len(fn) == 1 and fn[0][[i for i, h in enumerate(head) if str(h).startswith('P07')][0]]
      is not None and fn[0][-1] == '1/6', str(fn))
ok = all(float(x.rsplit('(', 1)[1].split(')')[0]) >= 40 for P in ('P01', 'P07', 'P11') for r in wb[f'{P} NUMBERS'].iter_rows(min_row=4, values_only=True)
         for c in r[2:6] if c for x in str(c).split('\n'))
check('every NUMBERS hit scores >= 40 (P01, P07, P11)', ok, '')

print('\nTest 10: midpoints (Eddie 14 Oct) — Equator |Dec|, RA far, tolerance grows with the span')
import jupiter_tables as JT
check('Equator: Dec +10, +20, −15 -> |Dec| midpoint 15, offset 0 (span 10); all on one side (+10, +20, +15) -> not listed',
      JT.mid_one(10, 20, -15, 'Equator') == (0.0, 10) and JT.mid_one(10, 20, 15, 'Equator') is None, str(JT.mid_one(10, 20, -15, 'Equator')))
check('RA far: 350 / 30 -> near midpoint 10 (span 40), far midpoint 190 (span 320)',
      JT.mid_one(350, 30, 10, 'RA') == (0.0, 40.0) and JT.mid_one(350, 30, 190, 'RA far') == (0.0, 320.0), '')
check('tolerance: green = 0.1 % of span, floor 0.05, cap 0.15; yellow 3x, light 9x (span 5 -> 0.05; 100 -> 0.1; 300 -> 0.15)',
      JT.mid_tol(5) == 0.05 and JT.mid_tol(100) == 0.1 and JT.mid_tol(300) == 0.15 and JT.mid_eval(0.1, 100)['colour'] == 'green'
      and JT.mid_eval(0.3, 100)['colour'] == 'yellow' and JT.mid_eval(0.9, 100)['colour'] == 'light' and JT.mid_eval(0.91, 100)['colour'] == ''
      and JT.mid_eval(1.34, 300)['colour'] == 'light' and JT.mid_eval(1.36, 300)['colour'] == '', '')
wb = openpyxl.load_workbook('reference/classic/race_batch_20220601_nottingham_1530_jupiter_tables.xlsx')
r = row(sheet_of(wb, 'Dynamic Force'), 'T10', 'S Jupiter / J Uranus | H Uranus')
EQ = 2 + 9 * 3                                              # 4th plane block: Equator
v, t, o, f, sc = r[EQ].value, r[EQ + 2].value, r[EQ + 4].value, (r[EQ].fill.start_color.rgb if r[EQ].fill.fill_type else None), r[EQ + 5].value
check('Dynamic Force T10 S Jupiter / J Uranus | H Uranus Equator +0.027875, span 22.1601, tol ±0.0500 (floor), green',
      round(v, 6) == 0.027875 and t == 'midpoint · span 22.1601 · tol ±0.0500' and f == GREEN, f'{v} {t} {o} {sc} {f}')
hd = [c.value for c in wb['P01'][next(i for i, rr in enumerate(wb['P01'].iter_rows(values_only=True), 1) if rr[0] == 'T10') + 1]]
check('T10 header planes RA, RA far, Dec, Equator; FIELD 10 and FIELD 11 have the four planes',
      [hd[2 + 9 * k] for k in range(4)] == ['RA', 'RA far', 'Dec', 'Equator']
      and all([x[0] for x in wb[f].iter_rows(values_only=True) if x[0] in ('RA', 'RA far', 'Dec', 'Equator')] == ['RA', 'RA far', 'Dec', 'Equator']
              for f in ('FIELD 10', 'FIELD 11')),
      str([hd[2 + 9 * k] for k in range(4)]))

t10 = [r[1] for r in wb['P07'].iter_rows(values_only=True) if r[0] == 'T10']
t11 = [r[1] for r in wb['P07'].iter_rows(values_only=True) if r[0] == 'T11']
jo = ('S Jupiter / H Jupiter | J Jupiter', 'S Jupiter / J Jupiter | H Jupiter', 'H Jupiter / J Jupiter | S Jupiter')
check('the three Jupiter-only midpoint lines are in T11 only (Wincanton P07)', not any(x in t10 for x in jo) and all(x in t11 for x in jo), '')

print('\nTest 11 (Eddie 14 Oct): EQUIDISTANCE — Beverley 14:05 2024 (sky-only workbook), SKY JUPITER')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20240608_beverley_1405.xlsx'))
eq = [r for r in wb['SKY JUPITER'].iter_rows(values_only=True) if r[0] == 'SKY EQ' and r[2]]
cp = [r for r in eq if r[1] == 'S Jupiter: S Ceres = S Pallas' and r[2] == 'GC']
check('S Jupiter–S Ceres GC 133.11392 / S Jupiter–S Pallas GC 133.19155 -> ratio 0.999417, unison, far side (Ceres–Pallas 71.55442)',
      len(cp) == 1 and round(cp[0][3], 5) == 133.11392 and round(cp[0][4], 5) == 133.19155 and cp[0][5] == 0.999417
      and cp[0][6].startswith('unison +') and cp[0][8] == 'far side' and round(cp[0][9], 5) == 71.55442, str(cp))
tg = [r for r in eq if r[8].endswith('X, Y together')]
nt = [r for r in eq if not r[8].endswith('X, Y together')]
check('"X, Y together" (Beverley S Sun = S Pluto Equator, d(X, Y) 0.003798) tagged and listed at the bottom',
      any(r[1] == 'S Jupiter: S Sun = S Pluto' and r[2] == 'Equator' for r in tg) and eq[-len(tg):] == tg
      and all(r[9] < (1.5 if r[2] == 'RA' else 0.3) for r in tg) and all(r[9] >= (1.5 if r[2] == 'RA' else 0.3) for r in nt), str(tg))
check('hits only (unison < 1 %), best first above the together lines; no Rahu = Ketu Equator line',
      all(float(r[6].split('+')[1].rstrip('%')) < 1 for r in eq) and [r[7] for r in nt] == sorted([r[7] for r in nt], reverse=True)
      and not any('Rahu' in r[1] and 'Ketu' in r[1] and r[2] == 'Equator' for r in eq), str(len(eq)))
wb = openpyxl.load_workbook('reference/classic/race_batch_20220321_wincanton_1420_jupiter_tables.xlsx')   # built in test 9 / 10
t17 = [r for r in wb['P07'].iter_rows(values_only=True) if r[0] == 'T17' and r[2]]
f17 = list(wb['FIELD 17'].iter_rows(min_row=4, values_only=True))
check('Wincanton P07 T17 present (H, J and S Jupiter lines) and FIELD 17 with holder counts',
      t17 and {r[1].split(':')[0] for r in t17} == {'H Jupiter', 'J Jupiter', 'S Jupiter'} and f17 and all(str(r[-1]).endswith('/6') for r in f17),
      f'{len(t17)} T17 lines, {len(f17)} FIELD 17 rows')
p1 = [(r[1], r[2]) for r in wb['P01'].iter_rows(values_only=True) if r[0] == 'T17' and r[2]]
check('Ketu line repeating a Rahu line dropped: P01 H Jupiter: H Sun = H Ketu (Dec) gone, H Sun = H Rahu (Equator) kept',
      ('H Jupiter: H Sun = H Ketu', 'Dec') not in p1 and ('H Jupiter: H Sun = H Rahu', 'Equator') in p1, '')
ok = all(int(str(r[-1]).split('/')[0]) == sum(1 for c in r[2:-1] if c and not str(c).endswith('not counted')) for r in f17)
check('FIELD 17 holder counts leave out "X, Y together" cells', ok and any(c and str(c).endswith('not counted') for r in f17 for c in r[2:-1]), '')

print('\nTest 12 (Eddie 14 Oct): EQUIDISTANCE family hits and timing — Lingfield AW 14:35 2021 (batch), P09 Pholas / Hollie Doyle')
wb = openpyxl.load_workbook(build('reference/classic/race_batch_20210402_lingfield_aw_1435.xlsx'))
eu = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T17' and r[1] == 'S Jupiter: H Uranus = H Pluto' and r[2] == 'Equator']
check('S Jupiter: H Uranus = H Pluto Equator 7.004077 / 6.988434, between, d(X, Y) 13.992511',
      len(eu) == 1 and eu[0][3] == 7.004077 and eu[0][4] == 6.988434 and eu[0][8] == 'between' and eu[0][9] == 13.992511, str(eu))
e = eu[0]
check('families split in value + family cells: 7.004077 | → 7 (whole, 63.38) · applying ..., 6.988434 | → 7 (whole, 17.78) ..., '
      '13.992511 | → 14 (whole, 39.13) · fixed',
      e[11:17] == (7.004077, '→ 7 (whole, 63.38) · applying, exact 16:10 (in 95.7 min)', 6.988434,
                   '→ 7 (whole, 17.78) · applying, exact 19:06 (in 271.6 min)', 13.992511, '→ 14 (whole, 39.13) · fixed'), str(e[11:17]))
cells = next(r for r in wb['P09'].iter_rows() if r[0].value == 'T17' and r[1].value == 'S Jupiter: H Uranus = H Pluto' and r[2].value == 'Equator')
fc = [cells[k].fill.start_color.rgb if cells[k].fill.fill_type else None for k in (12, 14, 16)]
check('family cells coloured by score: 63.38 yellow, 17.78 light, 39.13 light', fc == [YELLOW, LIGHT, LIGHT], str(fc))
check('ratio +5 min 0.997827, -> toward, unison applying, exact 17:38 (in 183.5 min) (race-local, off 14:35)',
      e[17] == 0.997827 and e[18] == '-> toward' and e[19] == 'applying, exact 17:38 (in 183.5 min)', str(e[17:20]))
na = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T17' and r[2] and r[1].startswith(('H Jupiter', 'J Jupiter'))]
check('natal-only lines: timing "fixed", no +5 ratio; each family hit "· fixed"', na and all(r[19] == 'fixed' and r[17] is None
      and all(c.endswith('· fixed') for c in r[12:17:2] if c and c.startswith('→')) for r in na),
      str(len(na)))

print('\nTest 13 (Eddie 14 Oct): T18 horse | jockey equidistance side by side — Lingfield AW 14:35 2021, P09')
t18 = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T18']
bi = [i for i, r in enumerate(t18) if str(r[1]).startswith('T18 block')]
b1 = [r for r in t18[bi[0] + 1:bi[1]] if r[1] != 'X–Y']
b2 = [r for r in t18[bi[1] + 1:] if r[1] != 'X–Y']
up = [r for r in b1 if r[1] == 'Uranus–Pluto']
check('block 1 row Uranus–Pluto: horse Equator 0.997767 | jockey Dec 0.994741',
      len(up) == 1 and up[0][2] == 'Equator' and up[0][5] == 0.997767 and up[0][10] == 'Dec' and up[0][13] == 0.994741, str(up))
hs = [r for r in b1 if r[7] is not None]
js = [r for r in b1 if r[7] is None]
check('block 1 sorted: horse-inside rows by horse score, then jockey-only rows by jockey score; outside side plain (no score)',
      b1 == hs + js and [r[7] for r in hs] == sorted([r[7] for r in hs], reverse=True)
      and [r[15] for r in js] == sorted([r[15] for r in js], reverse=True) and all(r[6].endswith('(outside 1 %)') for r in js if r[6]), '')
check('no "X, Y together" side; block 2 present', not any('together' in str(c) for r in b1 + b2 for c in r) and len(b2) > 0, f'{len(b1)} / {len(b2)} rows')

check('T18 Uranus–Pluto (both inside 1 %) tagged "both"; block 1 title carries the both count', up[0][18] == 'both'
      and 'both (horse and jockey inside 1 %): ' in t18[bi[0]][1] and int(t18[bi[0]][1].rsplit(': ', 1)[1]) == sum(r[18] == 'both' for r in b1),
      str(up[0][18]))

print('\nTest 14 (Eddie 14 Oct): T19 sky Jupiter on natal pairs + P09 PAIRS — Lingfield AW 14:35 2021')
t19 = [r for r in wb['P09'].iter_rows(values_only=True) if r[0] == 'T19']
uq = [r for r in t19 if r[2] == 'H Uranus – H Pluto' and r[3] == 'Equator']
check('T19 S Jupiter on H Uranus – H Pluto Equator: 7 / 7 / 14 (whole), ratio 1.002238 unison (60.24), between, (also T17)',
      len(uq) == 1 and uq[0][5].startswith('→ 7 (whole, 63.38)') and uq[0][7].startswith('→ 7 (whole, 17.78)') and uq[0][9] == '→ 14 (whole, 39.13) · fixed'
      and uq[0][10] == 1.002238 and uq[0][11] == '1 · unison · Perfect' and uq[0][13] == 60.24 and uq[0][15] == 'between' and uq[0][16] == '(also T17)', str(uq))
sc = [r[13] for r in t19 if r[13] is not None]
check('T19 filter: interval hit or all three families; no together; sorted by ratio score; no star–star, stars royal only',
      all(r[13] is not None or all(c and c.startswith('→') for c in (r[5], r[7], r[9])) for r in t19) and sc == sorted(sc, reverse=True)
      and not any(r[16] and 'together' in r[16] for r in t19)
      and all(sum(p.split(' ', 1)[1] in ('Algol', 'Pleiades', 'Capella', 'Sirius', 'Procyon', 'Alkaid', 'Algorab', 'Spica', 'Arcturus', 'Alphecca',
              'Vega', 'Deneb Algedi', 'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix', 'Aldebaran', 'Regulus', 'Antares',
              'Fomalhaut') for p in r[2].split(' – ')) <= 1 for r in t19)
      and not any(p.split(' ', 1)[1] in ('Algol', 'Sirius', 'Vega', 'Polaris') for r in t19 for p in r[2].split(' – ')), f'{len(t19)} rows')
pr = [r for r in wb['P09 PAIRS'].iter_rows(min_row=3, values_only=True)]
check('P09 PAIRS unfiltered (blocks H–H, J–J, H–J; outside ratios plain; together tagged; stars all 22)',
      len(pr) > len(t19) and {r[1] for r in pr} == {'H–H', 'J–J', 'H–J'} and any(r[13] is None and 'outside' in r[11] for r in pr)
      and any(r[16] and 'X, Y together' in r[16] for r in pr) and any('Polaris' in r[2] for r in pr), f'{len(pr)} rows')
sk = [r for r in wb['SKY JUPITER'].iter_rows(values_only=True) if r[0] == 'SKY STARS' and r[3]]
check('SKY JUPITER: S Jupiter on two sky stars (background, star–star only)', sk and all(r[1] == 'S–S' for r in sk), f'{len(sk)} rows')

print(f'\n{sum(RES)}/{len(RES)} passed')
sys.exit(0 if all(RES) else 1)
