# CLAUDE.md — read this first (Astronomy Research / horse racing reader; Eddie)

Claude Code loads this file at the start of every session. It is the handover: nothing depends on chat history.
Keep it current — at the END of every session, update "Where we are" and commit + push.

## Standing rules (Eddie)
- Wait for Eddie's explicit go-ahead before building or changing code (short go-aheads count). Running existing scripts is fine.
- Say what you see, without preconception; look deeper. Relationships first; combinations matter, counts are background only
  (counts have never separated winners — see the checklist, section 3).
- Natal charts at 12:00 standard time; no natal Moon. Stars are background only.
- Copy numbers from tool output; never invent. No "only / unique / most" without checking every runner in the field.
- After each read, run an independent checker (subagent) and apply its corrections before reporting.
- Don't say something is saved until it is committed and pushed. Back up every script to the repo.
- One race at a time. Blind first: read before opening the result.
- Eddie will not use the race scraper with Claude (`run_race_swiss.py --url ...`): ask for the race's xlsx + csv instead.
- Commit trailer: `Co-Authored-By: Claude <noreply@anthropic.com>` (or the session's own attribution).

## The key file
`docs/classic/winner_checklist.md` — every specific thing found in winners (36 kinds), each with exact numbers, races and field results,
what did NOT separate winners, the blind tests so far, and the open candidates. Read it before any race.

## Data and measures
- Race files: `reference/classic/race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx|csv` (+ `_active.xlsx`); split per runner with
  `python3 tools/split_batch.py <batch.xlsx> reference/classic/<course>_<hhmm>_<yyyymmdd> <course>_<hhmm>_<yyyymmdd>` →
  one workbook per runner (`...__P01.xlsx` = horse+jockey of cloth 1; P = 2*cloth-1). Sheets: TRANS (sky at race time), P01 (horse natal),
  P02 (jockey natal); column B body, E RA (deg), I Dec (signed).
- Planes: RA (wrapped 0–180), Dec (|dDec|), Flat (sqrt(RA²+Dec²)), great circle (GC; old tools call it 'Sky'), Equator (|Dec|),
  movement (sky X vs natal X).

## Families (Eddie's definitions, 13 Oct 2026 — the single reference: tools/families.py)
Correction (Eddie, 13 Oct 2026): the ninths are NOT n/9. They are exactly the 48 `_NINTH_RANGES` in rebuild_kit/active_vibrations.py.
tools/families.py imports Eddie's own scoring functions from that file (not copied). New tools use families.py. The frozen readers
(layers v2, CR v1.1, JR v1, JR v3) and the watch line still use the OLD tolerances (whole ±0.005, ninth n/9 ±0.0005, movement ±0.01 /
±0.0011, Equator ±0.01, golden list incl. 1/φ², any p/q ratio with % bands) until Eddie approves new versions. Past findings built on an n/9 outside the 48
and on a ratio off the interval list are listed in docs/classic/families_correction_20261013.md.
- Whole numbers 1–200, ±0.02 (score_whole).
- Golden interval: every multiple of φ, ±0.03236, zero multiple not scored (score_phi_interval).
- φ powers: φ^-1, φ^1..10, 10φ^-1..7, 100φ^-1, 100φ (score_phi_powers). No 1/φ² forms.
- Ninths: the 48 _NINTH_RANGES, lower <= v < upper, own tol, linear score (score_ninth): 0.111…–0.999…, 1.111…–9.999…, 11.11…–99.99…,
  111.1…, 1.222…–1.888…, 12.22…–18.88…, 122.2…–177.7…. Not n/9.
- √2: 1.414, 14.14, 141.4, 0.707, 7.07, 70.7; silver: 2.414, 24.14, 0.414, 4.14, 41.4. No multiples; tol max(0.5 % of target, 0.025).
  Scored against the exact values (√2 = 1.414213…, 10√2, 100√2, the 1/√2 forms; silver likewise), not the written decimals.
- Conjunction: RA < 1.5 or Dec < 0.3. Not a family hit in the Equator plane (Eddie, 15 Oct 2026; T17, T18, T19, SKY EQ, SKY PAIRS,
  PAIRS): an Equator distance under 0.3 shows a number family or nothing. ("X, Y together" in Equator stays < 0.3. The S Jupiter →
  equator rows of T1–T8 are Dec distances and keep the Dec conjunction.)
- Ratios: NOT any p/q. Eddie's musical interval list (blank-sheet-design section 10; also docs/sky_dig.md l.840, 871):
  Perfect 1, 2, 3/2, 4/3, 3, 4; Imperfect 5/4, 6/5, 5/3, 8/5, 5/2, 8/3, 9/4; Dissonant √2, 1+1/√2, 9/8, 16/9, 9/5, 15/8, 16/15;
  Septimal 7/4, 7/3, 7/2, 7/5, 7/6, 8/7; Harmonic 5, 6, 7, 8, 9; High 11/5, 11/6, 11/3, 11/8, 11/4, 13/5, 13/8, 13/4;
  Phi φ, φ², φ³, 1+√2 only (13 Oct: φ√5, 2−1/φ, φ³+1, 2/φ removed). Each ratio shows interval · name · group; Group column in every ratio table, a RATIOS BY
  GROUP sheet per runner (grouped, tightest first), group tag in the field matrices. Ratio values are scored on this list only.
  Perfect 1 (unison) counts, in the tables and in any new reader version; every unison shows its field count (it can come from age,
  e.g. Equator S/H = 1).
- Ratio tolerances taper (Eddie, 13 Oct 2026, revised the same day; families.interval_tol): unison 1 %; every other whole-number
  interval 1 % / k, k = the whole number or the LARGER number of the fraction, 0.15 % when k >= 6: 2 -> 0.5 %; 3, 3/2 -> 0.333 %;
  4, 4/3 -> 0.25 %; 5, 5/4, 5/3, 5/2 -> 0.2 %; 6/5, 8/5, 8/3, 9/4, 9/5, 7/x, 11/x, 13/x, 9/8, 15/8, 16/9, 16/15, 6–9 -> 0.15 %.
  Phi group, √2 and 1+1/√2 -> 0.15 %. Squared score on each interval's own tolerance; Equator ratios the same.
- Outside every tolerance: every value cell still shows its nearest target and offset, plain text, no score, no colour; conjunction
  is never the nearest target (Eddie, 14 Oct: keep)
  (e.g. '1 · unison · Perfect — outside ±1 %', '+4.44999%'). Nearest by tightness: the target with the smallest offset in units of its
  own tolerance (ratios and degrees alike).
- Planes RA, Dec, Flat, GC (frozen readers). jupiter_tables: RA, Dec and Equator only — Flat and GC removed 14 Oct 2026 for noise (Eddie).
- Midpoints (jupiter_tables; Eddie, 14 Oct 2026, revised the same day): T10, T11, FIELD 10, FIELD 11, THREADS, the midpoint half of T17,
  T18 and SKY EQ, and the unison rows of T19, SKY PAIRS and PAIRS. Three points: ends A, B and the middle point C (in T17-T19 the Jupiter).
  Ratio half: closeness = smaller ÷ larger of d(C, A), d(C, B) × 100, tolerance 10 % (closeness >= 90 %), score (10 (10 − (100 −
  closeness)) / 10)² × 0.5. Distance half: C's offset from the midpoint, squared on RA ±0.5, Dec ±0.15, Equator ±0.15, × 0.5. Hit = both
  halves inside; total = ratio half + distance half (0–100), coloured green >= 80, yellow 50–80, light < 50. Otherwise no score, not a hit,
  counted nowhere; both offsets shown plain. Planes: RA = the closer of the near and far midpoint, labelled near / far, never both; Dec
  (signed); Equator (|Dec| of all three, only when not all on one side). Columns: offset, (RA: near / far), closeness %, ratio half,
  distance half, total, timing (larger / smaller ratio toward unison). THREADS: every midpoint hit counts, whatever its total.
  T19 / SKY PAIRS / PAIRS (Eddie, 15 Oct): the ratio column stays on the interval list only (unison 1 %, 16/15 its own tolerance); the
  midpoint result (offset, closeness %, ratio half, distance half, midpoint total) is in its own cells; a row is listed if the ratio or
  the midpoint is a hit (or all three distances have a family hit); sort by the higher of ratio score and midpoint total. E.g. Lingfield
  P09 H Pluto – H Sedna Equator: ratio 1.011174 outside unison (+1.11741 %), midpoint 98.8949 %, 39.56 + 27.36 = 66.92; Ascot 14:30 2012
  P01 J Venus – J Neptune Equator: 16/15 1.065636 (12.67) and midpoint 93.8406 % (17.00), both shown. The old span
  tolerance and the first (1 %, mean) version are gone. The three Jupiter-only lines are in T11 (and FIELD 11) only.
  Test 15: Haydock 14:20 2021 P03 Golden Flame, T11 H Jupiter / J Jupiter | S Uranus RA far: offset 0.032036, distances 173.135571 /
  173.071498 (POSITIONS), closeness 99.963 %, ratio half 49.63, distance half 43.80, total 93.43. Short span (found by the rule):
  Nottingham 15:30 2022 P03 T11 H Jupiter / J Jupiter | S Sun Equator, span 0.4806: offset −0.002998, 0.243275 / 0.237279, 97.5353 %,
  28.39 + 48.02 = 76.41.
  Independent checker (14 Oct, revised rule): every T10 / T11 cell of Ascot P01 and Lingfield P01–P11 (3,594), Haydock P03 and
  Nottingham P03; T17 / SKY EQ lines and completeness; every T19 / SKY PAIRS / P09 PAIRS row; every T18 side checked: 0 mismatches.
- Decimal scaling: v, 10·v and v/10 are tested against every family, labelled ×10 / ÷10, in their own column (÷10 widens a tolerance 10× in degrees).
- RA–Dec crossing (same body pair, RA distance in one chart = Dec distance in another; natal RA = sky Dec and the reverse): ±0.02,
  linear score; the value need not be in a family (its family score shown beside it). In jupiter_tables: T16 (Jupiter–X, 6 orderings) + FIELD 16.
- No birth-day certainty for now.
- Scores in every cell: squared (10 × (tol − dev) / tol)² for whole, golden, φ powers, √2, silver, conjunction and intervals; linear
  100 × (tol − dev) / tol for ninths. Nearest target = the family with the highest score. Colour: green >= 80, yellow 50–80,
  light yellow < 50 (inside the bounds). No summary totals for now.

## Tools (run from the repo root)
- Layered reader: `tools/run_layers.sh <race>` = layer1_inventory → layer2_roots → layer3_web → layer4_field → layer5_reader.
  Outputs `docs/classic/<race>/layer1..layer5/`. Results only via `python3 tools/layer4_field.py <race> --results` (separate file).
  Designs and test results: `docs/classic/how_it_works.md`, `layer*_design.md`, `layer*_README.md`, `pair_focus_design.md`.
  Tests: `tests/layer1_reproduce.py <race>`, `tests/layer2_check.py`, `tests/layer3_check.py`, `tests/layer4_check.py`, `tests/layer5_check.py`.
- Checklist reader: `tools/checklist_reader.py <race> [--results]`; tests `tests/checklist_check.py`. Watch line: `tools/scans/watch_jupiter.py`.
- Jupiter-centred read (built 12 Oct 2026, Eddie's go-ahead): `bash tools/jup/run_all.sh <race>` -> docs/jupiter/<race>/ (positions, measures,
  layer2 ratios, layer3 every measure per runner, field.txt). Rules, tests and open points: docs/jupiter/README.md. Today's 13 races (12 Oct 2026)
  are run, blind (no results opened).
- Viewing tool (13 Oct 2026, not a reader): `python3 tools/jupiter_tables.py <race_batch xlsx | reference/classic/<race> folder>` ->
  race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx (raw Jupiter tables T1–T14, T16–T20 per runner (T15 removed 15 Oct 2026), field matrices, off and +5 min,
  every family from tools/families.py scored, best = highest score, also, scaled ×10 / ÷10, colours by score; ratios on the interval
  list with Group column, P## RATIOS sheets, FIELD 12–14; T16 RA–Dec crossing + FIELD 16; T17 equidistance + FIELD 17; T18 horse | jockey; T19 + P## PAIRS; T20 + FIELD 20; THREADS, P## NUMBERS and FIELD NUMBERS
  sheets - rules in the section below). Venv python (swisseph, pandas).
  Planes RA, Dec and Equator only (Flat and GC removed 14 Oct 2026 for noise, Eddie).
  Tests `python3 tests/jupiter_tables_check.py` (79/79). In the card pipeline: `run_card_swiss.py --tables`
  (copy in rebuild_kit/).
- Older single-purpose readers still useful: `tools/fit_read.py`, `movement.py`, `both_ends.py`, `three_way_all.py`, `equator_ratios.py`,
  `strings.py`; scans in `tools/scans/` (field_only_rates, sky_anchored_soak/compare, star_join_scan, jupiter_partner_scan).
- On the Mac: see `docs/MAC_SETUP.md` (venv with Python 3.12+, `pip install openpyxl`). Scripts call `python3.12`; inside the venv
  `python3` is fine (edit `tools/run_layers.sh` if `python3.12` is not on the PATH).

## jupiter_tables: EQUIDISTANCE (Eddie, 14 Oct 2026; viewing only)
Jupiter equally far from two bodies X, Y: a midpoint hit (rule above: closeness of d(Jup, X), d(Jup, Y) >= 90 % and Jupiter within RA ±0.5 /
Dec, Equator ±0.15 of the midpoint of X and Y; total = ratio half + distance half), every plane RA, Dec,
Equator (Equator = | |Dec Jup| − |Dec X| |, listed only when Jupiter, X and Y are not all on the same side of the equator, as midpoints; a
chart's own Rahu and Ketu are never paired, any plane). Hits only, best first; stars left out. Each line: both distances, ratio (smaller /
larger), unison offset, score, and "between" (d(X, Y) within 1 % of d(Jup, X) + d(Jup, Y)) or "far side", with d(X, Y) and the sum.
"X, Y together" (Eddie, 14 Oct): d(X, Y) within the conjunction tolerance in that plane (RA < 1.5; Dec, Equator < 0.3) -
tagged, listed at the bottom, shown grey "not counted" in FIELD 17 and left out of its holder counts. A Ketu line with the same numbers
as a Rahu line (e.g. X = Ketu in Dec = X = Rahu in Equator) is dropped; the Rahu one is kept.
Family hits and timing (Eddie, 14 Oct): each line also shows the best family hit (with score) of d(Jup, X), d(Jup, Y) and d(X, Y)
in two cells each: the value (7.004077) and "→ 7 (whole, 63.38) · <timing>", the second coloured by its score. Lines with a sky leg: ratio at off + 5 min, arrow, and "applying, exact hh:mm (in n min)" /
"separating, exact hh:mm (n min ago)" for unison (q = d(Jup, X) / d(Jup, Y) to 1, linear, race-local clock time); the same for each
family hit with a sky leg; natal-only lines and legs show "fixed" (beyond 50 years: "exact more than 50 years away / ago").
FIELD 17 cells add the unison timing. Test 12: Lingfield AW 14:35 2021 (batch copied from ~/astronomy-project/racecards), P09 Pholas,
S Jupiter: H Uranus = H Pluto Equator 7.004077 / 6.988434 (between, 13.992511): whole 7, 7, 14; unison applying, exact 17:38.
- SKY JUPITER sheet (once per race): S Jupiter with any two sky bodies (Moon included).
- Runner sheets T17: H Jupiter with two H bodies; J Jupiter with two J bodies; S Jupiter with two of the runner's natal bodies, same pair
  rule as T19 (Eddie, 14 Oct): H–H, J–J, or the same body in both charts (H X – J X); other H–J mixed pairs (e.g. H Pluto = J Mars) left out. FIELD 17: runners side by side, holders k/n, most held first.
- Test 11: Beverley 14:05 2024 (sky-only workbook copied into reference/classic from ~/astronomy-project/sky_0608_wb): together lines,
  sort. Its value case (S Ceres = S Pallas GC 133.11392 / 133.19155) was retired with GC (14 Oct); moved to Lingfield 14:35 2021 SKY EQ
  S Jupiter: S Mars = S Neptune Equator 9.894 / 9.906583, ratio 0.99873, between, d 19.800583.

T18 (Eddie, 14 Oct; each runner sheet): the same equidistance pair side by side for horse and jockey. Block 1 "S Jupiter: H X = H Y" |
"S Jupiter: J X = J Y"; block 2 "H Jupiter: H X = H Y" | "J Jupiter: J X = J Y". One row per body pair X–Y (bodies in both charts,
Jupiter excluded); each side its best plane (a midpoint hit, highest score; "X, Y together" planes left out) with both distances, ratio,
unison offset, score, between / far side, timing; a side not inside shows its closest plane (smallest offset) plain, uncoloured.
Horse-inside rows first by the horse's score, then jockey-only rows by the jockey's; a Ketu row repeating the Rahu row dropped.
A side outside 1 % never shows a "together" plane as its closest plane (Eddie, 14 Oct).
Test 13: Lingfield 14:35 2021 P09 Uranus–Pluto, horse Equator 0.997767 | jockey Dec 0.994741. Rows with both sides inside 1 % are tagged "both"
(last column; sort unchanged), with a "both" count in each block title.
T19 / P## PAIRS (Eddie, 14 Oct): sky Jupiter on natal pairs X–Y, blocks H–H, J–J and H–J across (H–J: the same body in both charts
  only, H X – J X, bodies only, no stars), every plane (RA, Dec,
Equator; Equator only when S Jupiter, X, Y straddle the equator). Each row: d(S Jup, X), d(S Jup, Y), d(X, Y) as value + family cell
(best family, score, timing; natal d(X, Y) fixed; coloured by score); ratio d(S Jup, X) / d(S Jup, Y) larger / smaller on the interval
list with the tapered tolerances (interval · name · group, offset, score, timing to the interval; outside: nearest interval plain);
between / far side; notes "X, Y together" and "(also T17)" (a unison row whose line is in T17). Natal pairs include the natal Jupiters.
- T19 (runner sheet): natal bodies + the 4 royal stars (each chart's own positions); rows where the ratio is on an interval or all three
  distances have a family hit; "together" rows left out; best ratio score first.
- P## PAIRS (one sheet per runner, in a separate workbook race_batch_<yyyymmdd>_<course>_<hhmm>_pairs.xlsx written next to the
  tables workbook, also via run_card_swiss.py --tables): every pair unfiltered, natal bodies + all 22 stars; no star–star pairs; together rows tagged.
- SKY JUPITER "SKY PAIRS" (Eddie, 14 Oct; once per race): S Jupiter on every pair of sky bodies (Moon included, no stars), T19 rows and
  filter (ratio on an interval or all three distances with a family hit; together out; best ratio score first). Ascot 14:30 2012 xlsx
  copied into reference/classic from ~/astronomy-project/racecards (1 runner; P01 T17 no mixed rows, SKY PAIRS 87 rows).
- SKY JUPITER "SKY STARS" (once per race, background): S Jupiter on two sky stars, filtered as T19.
- A chart's own Rahu–Ketu pair is left out of every plane in T17, T18, T19, PAIRS, SKY EQ and SKY PAIRS (Eddie, 14 Oct; was Equator only).
- A Ketu row with the same numbers as the Rahu row is dropped (any plane, also in T18). Test 14: Lingfield P09 H Uranus – H Pluto Equator, 7 / 7 / 14, unison
  1.002238 (60.24), midpoint total 92.71, (also T17 = a midpoint hit whose line is in T17). Messi (Ascot 19:45 7 Mar 2012) xlsx copied into reference/classic from ~/astronomy-project/racecards/20120307_messi (14 Oct): Venus–Neptune Dec is in neither SKY PAIRS nor T19 (natal 8.839548 / 35.534628, d 44.374176 → ninth 44.4444 (25.60), ratio 4.01996 outside 4 ±0.25 %; sky 0.469427 / 24.936325, ratio 53.12).
- Ketu in every plane (Eddie, 14 Oct, option B): Ketu is measured in RA (and, until 14 Oct, Flat and GC) as well as Dec / Equator in every table, SKY PAIRS, T17–T19, FIELD sheets and NUMBERS (tables tool only, via own_nodes / Ctx.pair; tools/jup2/core.py planes_for, used by the frozen JR v3, is unchanged). A chart's own Rahu–Ketu pair (H, J, and S Rahu – S Ketu) is never paired or counted, in any plane. Ascot 14:30 2012: SKY PAIRS 87 -> 89 (S Ketu – S Sedna RA 9/5, S Sun – S Ketu GC 8), P01 T17 55 -> 62 (7 Ketu hits; S Jupiter: H Ketu = H Rahu RA gone). Test changes: Newcastle P05 Ketu unisons own rows; Cobden 61 -> 63 unisons (J Ketu RA return-assisted, Flat); Lingfield P11 T18 Vesta–Ketu now kept (horse side Ketu RA 148.226037 / 179.265084, not a Rahu repeat).
- Sizes after Flat / GC removal (14 Oct): Lingfield 14:35 2021 tables 0.89 MB + pairs 2.85 MB (26,917 rows); Ascot 14:30 2012
  0.20 + 0.48 MB. Earlier sizes (14 Oct, H–J same body only, with Flat / GC): Lingfield 14:35 2021 (6 runners) tables 1.26 MB + pairs 4.76 MB (44,887 rows). Before that
  change: Lingfield 1.45 + 9.45 MB, York 16:15 2024 (15 runners) 3.63 + 23.18 MB.
- Timing, one method everywhere (Eddie, 14 Oct): the larger / smaller ratio (orientation fixed at the off) moving linearly toward its
  target interval; T17 and T18 unison timing use it too, so a pair has the same exact time in T17, T18 and T19.

## jupiter_tables: T15 removed, T20 (Eddie, 15 Oct 2026; viewing only)
- T15 (apex ratios) removed: runner sheets, FIELD 15, P## RATIOS rows, unison field counts. Other tables keep their numbers.
- T20: natal Jupiter as the midpoint of sky X and natal X. Horse S X / H X | H Jupiter, jockey S X / J X | J Jupiter, every body X in
  the sky and that chart (no stars, no Moon, not Jupiter). Planes RA (closer of near / far, labelled), Dec, Equator (only when not all on
  one side), on the midpoint scoring (see Families), T10 / T11 columns per plane, timing from the off and +5 min. One line per body,
  horse cells | jockey cells. FIELD 20: bodies x runners, each hit as chart, plane, total ('H Dec 70.99'), runners with a hit k/n.
  THREADS: every T20 hit is a Jupiter–X link (as the other midpoints).
- Test 16: Lingfield 14:35 2021 P03 T20 S Sun / H Sun | H Jupiter Dec (hand-checked from POSITIONS): Dec 5.028708 / 10.292917 /
  7.682992, d 2.654284 / 2.609925, offset +0.022180, closeness 98.3287 %, 34.68 + 36.31 = 70.99, applying, exact 17:21 (in 166.5 min).
- Hits: Lingfield 14:35 2021 4 of 138 lines (H Dec 1, H RA far 1, J Dec 1, J RA far 1: P07 J Mars RA far 83.79, P03 H Sun Dec 70.99,
  P09 H Ceres RA far 51.24, P07 J Uranus Dec 35.33); Ascot 14:30 2012 0 of 23. Sizes: Lingfield 0.85 + 2.90 MB, Ascot 0.19 + 0.49 MB.
- Independent checker (15 Oct), from POSITIONS: every T20 cell of both races (Lingfield 720 plane cells, Ascot 124), the 4 hits incl.
  timing, near-misses (P03 H Mercury Dec −0.242245, P05 H Ceres Equator 0.224967, P11 H Sun RA −0.826292), FIELD 20, THREADS lines,
  no T15 / FIELD 15: 0 mismatches.

## jupiter_tables: THREADS and NUMBERS sheets (Eddie, 13 Oct 2026; viewing only)
Common to both: a "repeat" is the same hit seen in two forms of one value (main v and scaled ×10 / ÷10) on the same family with the
same digits (target ×10 or ÷10, e.g. ninth 11.1111 / 1.11111, √2 14.14 / 1.414). Only one form is shown: the main form, unless the
scaled form scores more than 0.5 points higher (unrounded scores; Eddie, 14 Oct). Scores are rounded only for display, at 2 dp everywhere
(T-tables, scaled and also columns, FIELD matrices, THREADS, NUMBERS). Automatic (Jupiter return) unisons are left out.
- **THREADS** (one sheet, after the runner sheets): rows = bodies (sky bodies incl. Moon, Jupiter excluded, Rahu / Ketu folded as
  "Nodes"), columns = runners. Hits = every scored hit (inside tolerance) linking body X with Jupiter, from T1–T8, T10–T13, T16 and T20
  (midpoints T10 / T11 / T20: every midpoint hit counts; scaled hits marked "scaled"; stars, equator and Jupiter–Jupiter left out).
  - Cell: hits scoring >= 50, main first then scaled, best first, short form ("S Transpluto→H Jup Dec 33.33254 → 33.3333 (99.05) [T7]"),
    each line coloured by its score; every family hit of the value (main, and ×10 / ÷10 scaled, no conjunction) is a hit, not only the
  best (Eddie, 14 Oct, as NUMBERS); the cell is coloured by its best line; last line "+ n weaker (see T-tables)" = hits < 50, score-0 (at 2 dp) hits and hidden repeats not counted.
  - Tags (top line), from the MAIN hits scoring >= 50 (a main hit hidden by its scaled repeat still counts; green / yellow midpoints
    count): "mutual, same chart" = S Jup→H X with S X→H Jup, or S Jup→J X with S X→J Jup; "mutual, across charts" = S Jup→J X with
    S X→H Jup, or S Jup→H X with S X→J Jup; "both Jupiters" = S X→H Jup and S X→J Jup; "both charts" = natal X reached in H and in J;
    "directions n" = distinct of S Jup→H X (T5), S Jup→J X (T6), S X→H Jup (T7), S X→J Jup (T8).
  - Last columns: per body, runners with mutual same chart / mutual across charts / both Jupiters / any of the three (k/n).
  - Test 8: Nottingham 15:30 2022, Dynamic Force (values set from the rule, not tuned to the winner). Uranus tags / counts rested on a GC
    hit and were retired 14 Oct; the tags check moved to Transpluto (mutual, same chart · mutual, across charts · both Jupiters · directions 3).
- **P## NUMBERS** (one per runner, after P## RATIOS): rows = target numbers with the ×10 / ÷10 forms folded into one row (key = family +
  the target's digits), degree-distance families only (whole, golden, φ powers, ninths, √2, silver; no conjunction, no ratios).
  - Columns: SKY (S Jupiter → sky bodies, stars, equator), HORSE (T1 only: H Jupiter → H bodies, stars, equator), JOCKEY (T2 only:
    J Jupiter → J bodies, stars, equator), SKY→NATAL (T5–T8). T3 / T4 cross-chart hits are not used (Eddie, 14 Oct; the tables stay).
  - Cell: hits scoring >= 40 on that number, main or scaled (labelled), value, offset and score, best first; colour green >= 80,
    yellow 50–80, light yellow 40–50.
  - Tag: "sky + horse + jockey" (SKY, HORSE and JOCKEY hits, within-chart) or "two of three"; SKY→NATAL never counts. Tagged rows first.
- **FIELD NUMBERS** (one sheet): every number held sky + horse + jockey by any runner, the SKY best hit, each holder's best HORSE and
  JOCKEY hit, and the holder count (k/n).
  - Test 9: Wincanton 14:20 2022. The P07 River Bray "ninth: 7.77778 / 77.7778" case (its jockey hit was J Haumea GC) was retired 14 Oct;
    moved to P01 Reserve Tank "ninth: 11.1111 / 111.111" (S Sirius RA 111.443941, H Regulus Dec 11.11928, J Venus RA 11.139997).

## Where we are (13 Oct 2026)
- **T19 / SKY PAIRS / PAIRS split (15 Oct 2026, Eddie):** ratio on the interval list only, midpoint in its own cells (midpoint total
  column added), listed if either is a hit. Lingfield 14:35 2021: T19 1048 rows (917 ratio hits, 35 of them unison; 99 midpoint hits,
  71 midpoint only; 7 unisons without a midpoint hit), SKY PAIRS 59 rows (45 ratio, 9 midpoint, 7 midpoint only). Ascot 14:30 2012:
  T19 209 rows (191 ratio, 14 midpoint, 8 midpoint only), SKY PAIRS 53 (40 ratio, 1 midpoint). T18 unchanged (a row is dropped only
  when the whole row repeats). Tests 72/72. Independent checker (15 Oct), recomputed from POSITIONS: every Lingfield T19 row (P01 193,
  P03 183, P05 153, P07 172, P09 193, P11 154) and SKY PAIRS (59): 0 mismatches, no missing or extra rows.
- **No conjunction in the Equator plane (15 Oct 2026, Eddie):** sort kept (higher of ratio score and midpoint total). Rows dropped
  (listed before only for an Equator conj): Lingfield 14:35 2021 T19 12 (1048 -> 1036; P01 H Sun – H Ceres, J Gonggong – J Transpluto;
  P03 J Haumea – J Quaoar, J Quaoar – J Transpluto, J Quaoar – J Regulus; P05 J Juno – J Transpluto, H Transpluto – J Transpluto;
  P09 J Mercury – J Quaoar; P11 J Mercury – J Ceres, J Mercury – J Transpluto, J Chiron – J Transpluto, J Ceres – J Regulus),
  SKY PAIRS 0 (59); Ascot 14:30 2012 T19 0 (209), SKY PAIRS 0 (53). T17, T18, SKY EQ unchanged. Tests 73/73. Independent checker
  (15 Oct), from POSITIONS: each of the 12 fails ratio, midpoint and all-three-families without conj (d < 0.3 legs 0.023634–0.239552,
  ratios 5.95–262.6, closeness <= 16.8 %), each still in P## PAIRS with 'no family' on that leg; completeness of every Equator row in
  T19 / SKY PAIRS of both races: exact, these 12 only; no '(conj,' on any Equator row. 0 mismatches. (The earlier "13" was a miscount.)
- **Midpoint scoring revised (14 Oct 2026, Eddie):** closeness >= 90 % (ratio half × 0.5) + distance half × 0.5, total = sum (see Families).
  Midpoint hits, previous version -> revised: Ascot 14:30 2012 T10 0 -> 0, T11 1 -> 2, T17 6 -> 11, T18 horse 3 -> 4 / jockey 3 -> 7,
  T19 5 -> 14, SKY PAIRS 0 -> 1, SKY EQ 0 -> 1; Lingfield 14:35 2021 T10 2 -> 11, T11 1 -> 15, T17 49 -> 138, T18 horse 26 -> 85 /
  jockey 23 -> 49, T19 28 -> 99, SKY PAIRS 2 -> 9, SKY EQ 2 -> 9. Tests 71/71.
- **Midpoint scoring (14 Oct 2026, Eddie, first version, superseded):** two halves (unison ratio 1 % + distance from the midpoint RA 0.5 / Dec 0.15 / Equator 0.15),
  both needed, score = the mean; old span tolerance removed (see Families). Midpoint hits, before -> after: Ascot 14:30 2012 T11 6 coloured
  (2 green / yellow) -> 1 (RA far), T10 2 -> 0, T17 7 -> 6, T19 unison 6 -> 5, SKY PAIRS unison 1 -> 0; Lingfield 14:35 2021 T10 34 coloured
  (10 green / yellow) -> 2, T11 39 (14) -> 1, T17 61 -> 49, T19 unison 35 -> 28, SKY PAIRS 2 -> 2. Short spans now fail on the ratio half.
  Tests 70/70 (test 10 rewritten; tests 11, 13, 14 moved / re-indexed; test 15 Haydock).
- **Planes (14 Oct 2026, Eddie):** jupiter_tables uses RA, Dec and Equator only; Flat and GC removed for noise (every table, SKY sheets,
  FIELD, NUMBERS, THREADS, pairs workbook). Tests retired / moved to RA, Dec, Equator cases: 5, 6, 7, 8, 9, 11 (65/65).
  Independent checker (14 Oct) recomputed the moved cases from the input positions (Newcastle P05 / P11 RA Rahu ratios and 2/6, Sandown P07 Vesta 3/2 and J Mars 9/8, Wincanton P01 ninth 11.1111 row and 1/6, Lingfield SKY EQ Mars = Neptune Equator): 0 mismatches. Not yet independently checked: Cobden's 22 unisons, Nottingham Transpluto tags. Ascot 14:30 2012:
  T17 62 -> 35, T18 28 -> 7, T19 351 -> 201, SKY PAIRS 89 -> 52; Lingfield 14:35 2021: T17 306 -> 165, T18 149 -> 59, T19 1840 -> 978,
  SKY PAIRS 100 -> 52, PAIRS 46,477 -> 26,917.
- **Working view = the tables tool on Eddie's families:** `tools/jupiter_tables.py` on `tools/families.py` (see "Families" above).
  Jupiter return (S Jupiter in conjunction with a natal Jupiter): information line at the top of that chart's T13. A T12–T14 unison is
  greyed "automatic (Jupiter return)" per plane only when d(S Jupiter, natal Jupiter) / d(natal Jupiter, X) < 0.0015; automatic unisons
  are left out of all field counts. 0.0015 <= that ratio < 0.02 = tag "return-assisted" (colour and field count unchanged).
  Tables tool done for now (13 Oct); Eddie is looking at races in it.
- **Not trusted until re-checked:** the frozen readers (layers v2, CR v1.1, JR v1, JR v3), the checklist (docs/classic/winner_checklist.md)
  and the Jupiter watch line still use the OLD definitions (n/9 ninths, any p/q ratios, old tolerances). Their findings are not trusted
  until re-checked against Eddie's families: see docs/classic/families_correction_20261013.md for what relies on a non-48 ninth or an
  off-list ratio.
- **Decision (Eddie, 13 Oct 2026):** look at races in the tables first; rebuild the readers later (no new reader version until Eddie says).
- **Eddie's observations** from the tables go in docs/classic/eye_notes.md (race, runner, table, exact values, field check).
- **Open points, to look at later with Eddie (no changes now):** (1) revisit the scoring; (2) the wide ninth bands at large values
  (e.g. 166.667 ± 1.17, from _NINTH_RANGES).
- **Forward candidates that still stand:** E1 (JR v3: sky Jupiter, horse X, jockey X — one at the midpoint of the other two) and
  checklist item 13 (shared natal pair, horse value ≈ jockey value).

## Earlier state (12 Oct 2026, end of session) — kept for reference; definitions superseded as above
- Frozen tools (do not change during a test; a change = new version + new freeze commit):
  - Layers 1–5 frozen v2 = commit 4baefa1 (how_it_works.md).
  - Checklist reader CR v1.1 = commit 3d62207: `python3 tools/checklist_reader.py <race>` -> docs/classic/<race>/checklist/
    (field.txt = race page incl. the 17/14/15 watch line; P##.txt = runner pages with field-relative joins). Tests
    `python3 tests/checklist_check.py` (421/421; 13 DIFFERENCE/EXPLAINED for Eddie). Design + as-built + Eddie's decisions:
    docs/classic/checklist_reader_design.md (sections 9–11).
  - Jupiter-centred read JR v1 = commit f96f93d: `bash tools/jup/run_all.sh <race>` -> docs/jupiter/<race>/field.txt. Frozen 12 Oct 2026
    before today's races were run; no change until their results are in (a change = JR v2 + new freeze commit).
  - Transit-Jupiter reader JR v3 = commit 1e18081 (frozen 13 Oct 2026; use this one): same command and outputs as below, plus chains (CH,
    RA/Dec, root = the sky pair), one near part allowed in combined hits, runner page strict/exact only. Tests 11/11. Design section 11.
  - (JR v2 = commit 2898024, superseded by v3 before any race was read with it): `python3 tools/jupiter_reader.py <race>` (venv python; engine
    rebuild_kit/celestial_bodies_swisseph.py + ~/astronomy-project/ephe) -> docs/classic/<race>/jupiter/ (field.txt, P##.txt, P##_full.txt,
    P##.json, engine_check.txt). Tests `python3 tests/jr2_check.py` (7/7). Design + as-built + open points: docs/classic/jupiter_reader_design.md
    (section 10). Separate from JR v1 (tools/jup/, f96f93d, unchanged). A change = JR v3 + new freeze commit.
  - Jupiter watch line, fixed 12 Oct before Musselburgh, NOT to be changed after results: `python3 tools/scans/watch_jupiter.py <race>`
    -> checklist/watch_jupiter.txt ("a rare item linking Jupiter with itself across charts": Jupiter Equator ratio, same-body set,
    movement onto a whole/ninth, or close cross link H Jupiter – J Jupiter; rare = held by < half the field). LOOSE: 7 of 14 runners in
    the opened blind races, incl. all 3 winners.
- Blind batch — finished; no genuinely blind race left in it:
  - Blind for the layers: Exeter 15:15 (Forget You Not), Redcar 15:15 (Present Moment), Haydock 14:20 (Golden Flame).
  - Blind for the checklist reader: Kempton 14:40 (Hamish — only field-only item the node loop), Fontwell 16:45 (Pixie Loc — only
    field-only item H Eris – J Jupiter both ends moved, as Ziggy's Dream), Goodwood 18:53 (Madame Tantzy — no field-only item).
  - NOT blind: Musselburgh 13:45 (winner Graces Quest seen in another chat; read anyway, not counted); Worcester 13:00 (Rhythm Is A Dancer)
    and Newcastle AW 16:33 (Athmad; also Dubai Souq 6th seen by mistake) — winners confirmed, not read; Catterick 14:40 2022 (Wotever Next)
    seen before. Southwell 20:00 10 Oct 2026 has layer outputs, no results file, not in the batch — blind only if Eddie has not seen it.
  - Every result and read is in the checklist section 4 (blind tests).
- Scans done this session (read-only, tools/scans/; outputs docs/classic/*.txt). The read races are NOT evidence:
  - field_only_rates: winners by number of strict field-only items. Blind for the reader (3 races, 14 runners): 0 items 1/4, 1 item 2/5,
    2 items 0/3, 3+ 0/2 — far too small to read; worth tracking.
  - sky_anchored_soak (+ compare): no separation; same-afternoon pairs share anchors no more than other runner pairings (checklist sec. 5 item 9).
  - star_join_scan (on = RA < 1.5 AND Dec < 0.3): star joins almost never happen; the few are horse Transpluto (age) or Cobden's J Rahu on Regulus.
  - jupiter_partner_scan: partner body does not separate; rare Jupiter–Jupiter across charts hit all 3 blind winners (23-body control: only
    Jupiter did) -> the watch line above. Recurring cross link added: H Eris – J Jupiter both ends moved (Wolverhampton, Fontwell 16:45).
- Open candidates (checklist section 5): items 14, 17, 20, 21 are in the reader but not proven; sky-anchored soak (no separation); Jupiter watch line.
- Do not open reference/profiles_test_scored.csv or reference/profiles_blind_kit.csv during blind work (they hold results).

## Forward-test routine (every new race from now on — the only genuine tests left)
1. Eddie supplies the race's xlsx + csv (no scraper). Put them in reference/classic/ as race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx|csv.
   Claude does NOT open the csv (it holds the result) and opens nothing else that could hold it.
2. Split: `python3 tools/split_batch.py <batch.xlsx> reference/classic/<course>_<hhmm>_<yyyymmdd> <course>_<hhmm>_<yyyymmdd>`.
3. Blind read with the frozen tools only: `bash tools/run_layers.sh <race>`, `python3 tools/checklist_reader.py <race>`,
   `python3 tools/scans/watch_jupiter.py <race>`, `bash tools/jup/run_all.sh <race>` (JR v1) and `python3 tools/jupiter_reader.py <race>` (JR v3).
   No rule, threshold or watch-line change before the result.
4. Independent checker (subagent, blind: no csv / results / --results) recomputes the race page, field-only claims, joins and watch line
   from the workbooks. Apply corrections. Commit + push the blind read BEFORE the result ("Blind N: <race> ...").
5. Show Eddie the race page, joins per runner and the watch line. Open the result only when Eddie says:
   `python3 tools/checklist_reader.py <race> --results` (writes checklist/field_results.txt). Commit + push.
6. Record in the checklist section 4 (said / result / winner had) and update the tallies (tools/scans/field_only_rates.py: add the race to
   BLIND; watch line holders vs finish). Any new idea is written down as a candidate, fixed before the next race, and only tested forward.

## How to run a session
1. Start: `cd ~/astro-harmonics && git pull`, `source ~/astro-venv/bin/activate`, then `claude`. Say what you want to do (e.g. "forward test: <race>").
2. Work one race or one script change. Checker after each read. Commit + push.
3. End: ask Claude to update "Where we are" here and the checklist, commit and push; then type `exit`.
