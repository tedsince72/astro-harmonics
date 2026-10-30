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
- Whole numbers 1–200, ±0.02, checked on the TARGET (Eddie, 27 Oct 2026; families.score_whole_t): t = round(v), 1 <= t <= 200,
  dev = |v − t| < 0.02, squared (10 (0.02 − dev) / 0.02)². (active_vibrations.score_whole, not edited, needs 1 <= v <= 200, so before
  0.98 < v < 1 never scored on 1, e.g. 0.997954 -> now 1 whole 80.59.)
- HALF - REMOVED 29 Oct 2026 (Eddie): no half score, never a nearest target; see "half family removed". Text kept for reference:
  HALF (Eddie, 24 Oct 2026; families.score_half): 0.5, 1.5 … 199.5, ±0.01 absolute, squared (10 (0.01 − dev) / 0.01)², family "half",
  scored alongside the others (best = highest score; nearest by tightness includes the half targets). No 4-digit rule on whole or half.
  Half vs conjunction (Eddie, 24 Oct 2026, kept as built): inside the conjunction range (RA < 1.5, Dec < 0.3) the highest score wins - a
  half 0.5 / 1.5 (RA) can outscore the conjunction, as whole 1 already could; the red fill still marks the range (T24). E.g. Lingfield P11
  T3 H Jupiter → J Ketu RA 1.497436 half 1.5 (55.30) vs conj 0.00; P11 T24 JOCKEY J Alphecca – J Quaoar RA 1.498093 half (65.50), red; pairs
  workbook P03 J Sun – J Mars RA 0.498836 half 0.5 (78.08) vs conj 44.55, P05 H Sun – H Pallas RA 0.500948 (81.95) vs 44.35.
- 4-DIGIT RULE (Eddie, 24 Oct 2026; families.digits4 / digit_match): golden, φ powers, ninths, √2 and silver score only when the value's
  first 4 significant digits, TRUNCATED, equal the exact target's at the same order of magnitude (k = floor(log10 x), digits4 = floor(x /
  10^(k − 3)); 2.414 never matches 24.14). Inside the match the score is the family's old formula on its old tolerance (the tolerances
  below stay as the score scale); outside it no score, no fill: a value inside the family's old tolerance that fails the match reads
  '<target> <family> — not a 4-digit match (<offset>)' (T24 comments 'nearest: ' + that; Eddie, 24 Oct 2026), a value beyond the old
  tolerance keeps '— outside ±<tol>'. E.g. silver 24.1421 -> 24.1400 to
  24.1499; ninth 166.667 -> 166.600 to 166.699. Ratios (interval list, areas) and midpoints unchanged. Frozen readers keep their own rules.
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
- Ratio tolerances (families.interval_tol). Area A "whole + 3/2" (Eddie, 15 Oct 2026; families.AREA_A): 1, 3/2, 2, 3, 4, 5, 6, 7,
  8, 9 on ±0.02 ABSOLUTE (|ratio − interval| < 0.02, as whole-number distances), squared score, offset shown absolute (no %).
  Area B "other" = every other interval, tapered (Eddie, 13 Oct 2026, revised the same day): 1 % / k, k = the LARGER number of the
  fraction, 0.15 % when k >= 6: 4/3 -> 0.25 %; 5/4, 5/3, 5/2 -> 0.2 %; 6/5, 8/5, 8/3, 9/4, 9/5, 7/x, 11/x, 13/x, 9/8, 15/8, 16/9,
  16/15 -> 0.15 %; Phi group, √2 and 1+1/√2 -> 0.15 %. Squared score on each interval's own tolerance; Equator ratios the same.
  (Before 15 Oct the A intervals were tapered too: unison 1 %, 2 0.5 %, 3, 3/2 0.333 %, 4 0.25 %, 5 0.2 %, 6–9 0.15 %. Every ratio
  number and count written in this file before the areas entry below was made on those tolerances.)
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
  distance half, total, timing (larger / smaller ratio toward unison). THREADS: a midpoint hit counts only at total >= 50, like every other hit (Eddie, 15 Oct 2026).
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
- No value scaling (Eddie, 16 Oct 2026; replaces "decimal scaling"): the measured value (distance or ratio) is never multiplied or
  divided by 10. Scaled forms exist only as targets in the family lists (φ powers incl. 10φ^n and 100φ, ninths at every decade, √2 1.414 /
  14.14 / 141.4, silver 0.414 / 4.14 / 41.4, as in families.py). jupiter_tables has no scaled column, scaled timing, scaled THREADS /
  NUMBERS / TIMELINE hit or repeat rule (KEEP_MARGIN, same_digits gone). NUMBERS rows still fold the target forms by family and digits.
  (families.scaled stays in families.py, unused by the tables.)
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
  race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx. TRIMMED 29 Oct 2026 (Eddie): POSITIONS, SKY JUPITER (whole) and per runner T1–T8,
  T24 HORSE / T24 JOCKEY (with the four Jupiter rows + 'stars' on top) only; --full accepted, no effect; no _pairs workbook. Before the trim:
  (raw Jupiter tables T1–T14, T16–T22 per runner (T15 removed 15 Oct 2026), field matrices, off and +5 min,
  every family from tools/families.py scored, best = highest score, also (no scaled column since 16 Oct 2026), colours by score; ratios on the interval
  list with Group column, P## RATIOS sheets, FIELD 12–14; T16 RA–Dec crossing + FIELD 16; T17 equidistance + FIELD 17; T18 horse | jockey; T19 + P## PAIRS; T20 + FIELD 20; T21, T22 + FIELD 21, 22 (fixed stars); T23 + FIELD 23 (H / J, S / H, S / J ratios); T24 stars against bodies (SKY, HORSE, JOCKEY grids; T1 / T2 / T24 on 35 stars, 19 Oct; 46 since 20 Oct, 67 since 21 Oct; conjunction cells red, 20 Oct) + T24 H / J, HORSE / JOCKEY RATIOS; default workbook POSITIONS, SKY JUPITER, P## only, --full for RATIOS / NUMBERS / THREADS / FIELD; SKY cells in T1 / T2 and a sky side in T21 with the tag 'same as sky'; THREADS, P## NUMBERS and FIELD NUMBERS
  sheets - rules in the section below). Venv python (swisseph, pandas).
  Planes RA, Dec and Equator only (Flat and GC removed 14 Oct 2026 for noise, Eddie).
  Tests `python3 tests/jupiter_tables_check.py` (148/148; builds with --full). In the card pipeline: `run_card_swiss.py --tables`
  (copy in rebuild_kit/).
- Older single-purpose readers still useful: `tools/fit_read.py`, `movement.py`, `both_ends.py`, `three_way_all.py`, `equator_ratios.py`,
  `strings.py`; scans in `tools/scans/` (field_only_rates, sky_anchored_soak/compare, star_join_scan, jupiter_partner_scan).
- On the Mac: see `docs/MAC_SETUP.md` (venv with Python 3.12+, `pip install openpyxl`). Scripts call `python3.12`; inside the venv
  `python3` is fine (edit `tools/run_layers.sh` if `python3.12` is not on the PATH).

## jupiter_tables: EQUIDISTANCE (Eddie, 14 Oct 2026; viewing only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): T17, T18, T19, FIELD 17 and P## PAIRS (the _pairs workbook) are gone; SKY EQ and SKY PAIRS on SKY JUPITER kept. Text kept for reference.
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
- SKY JUPITER "SKY PAIRS" (Eddie, 14 Oct; once per race): S Jupiter on every pair of sky bodies (Moon included; 15 Oct also body – royal star), T19 rows and
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
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): T20 and FIELD 20 are gone. Text kept for reference.
- T15 (apex ratios) removed: runner sheets, FIELD 15, P## RATIOS rows, unison field counts. Other tables keep their numbers.
- T20: natal Jupiter as the midpoint of sky X and natal X. Horse S X / H X | H Jupiter, jockey S X / J X | J Jupiter, every body X in
  the sky and that chart (no stars, no Moon, not Jupiter). Planes RA (closer of near / far, labelled), Dec, Equator (only when not all on
  one side), on the midpoint scoring (see Families), T10 / T11 columns per plane, timing from the off and +5 min. One line per body,
  horse cells | jockey cells. FIELD 20: bodies x runners, each hit as chart, plane, total ('H Dec 70.99'), runners with a hit k/n.
  THREADS: a T20 hit is a Jupiter–X link, counted at total >= 50 (as every hit).
- Test 16: Lingfield 14:35 2021 P03 T20 S Sun / H Sun | H Jupiter Dec (hand-checked from POSITIONS): Dec 5.028708 / 10.292917 /
  7.682992, d 2.654284 / 2.609925, offset +0.022180, closeness 98.3287 %, 34.68 + 36.31 = 70.99, applying, exact 17:21 (in 166.5 min).
- Hits: Lingfield 14:35 2021 4 of 138 lines (H Dec 1, H RA far 1, J Dec 1, J RA far 1: P07 J Mars RA far 83.79, P03 H Sun Dec 70.99,
  P09 H Ceres RA far 51.24, P07 J Uranus Dec 35.33); Ascot 14:30 2012 0 of 23. Sizes: Lingfield 0.85 + 2.90 MB, Ascot 0.19 + 0.49 MB.
- Independent checker (15 Oct), from POSITIONS: every T20 cell of both races (Lingfield 720 plane cells, Ascot 124), the 4 hits incl.
  timing, near-misses (P03 H Mercury Dec −0.242245, P05 H Ceres Equator 0.224967, P11 H Sun RA −0.826292), FIELD 20, THREADS lines,
  no T15 / FIELD 15: 0 mismatches.

## jupiter_tables: T21, T22 fixed stars (Eddie, 15 Oct 2026; viewing only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): T21, T22, FIELD 21 / 22 are gone. Text kept for reference.
All 22 stars; planes RA, Dec, Equator (only when the three straddle the equator). Existing tables unchanged (Lingfield rebuilt and
compared row by row with the previous version: 0 differences). THREADS and NUMBERS: stars stay out (no T21 / T22).
- T21: natal Jupiter on natal star pairs (as SKY STARS, natal; each chart's own star positions). One line per star pair and plane,
  horse "H Jupiter: H A – H B" | jockey "J Jupiter: J A – J B"; each side the T19 cells (three distances + family, ratio on the interval
  list, midpoint cells, between / far side, together); timing fixed. Listed when either side passes the T19 filter; best first by the
  higher of ratio score and midpoint total. (tools: pair_rows with jup / blocks; defaults keep T19 as before.)
  Filter revised (Eddie, 15 Oct 2026): a line is listed only when a non-together side has a midpoint hit (any total) or a ratio hit
  scoring >= 50 (lines listed only for lower ratio scores or all three families dropped); FIELD 21 follows (midpoint hits and ratio
  hits >= 50, no empty rows). T22, P## PAIRS and the other tables unchanged.
- T22: each star's race-day position as the apex; horse d(star, S Jupiter) / d(star, H Jupiter) | jockey the same with J Jupiter, one
  line per star and plane, every star listed. Both distances + family, ratio larger / smaller on the interval list (score, arrow,
  timing from the off + 5 min), midpoint cells when closeness >= 90 % (the star the middle point between S Jupiter and natal Jupiter).
- FIELD 21 (rows star pairs) / FIELD 22 (rows stars): per runner each hit as side, plane, interval or midpoint and score ('H Dec 1
  (96.59)', 'H Dec midpoint (98.45)'), runners with a hit k/n. Hits = ratio on an interval (T21: >= 50) or midpoint hit (together
  sides left out).
- Test 17 (Lingfield 14:35 2021, by hand from POSITIONS): T21 P03 H Jupiter: H Algorab – H Castor Dec 24.201513 / 24.205672 /
  48.407186, unison 1.000172 (96.59), midpoint −0.002079, 99.9828 %, 49.83 + 48.62 = 98.45, fixed; T22 P11 H Aldebaran RA 103.180242 /
  102.601266, unison 1.005643 (18.98), applying, exact 05 Apr 2021 16:21 (in 4426.2 min), midpoint far +0.289488, 99.4389 %, 44.55 +
  8.86 = 53.41.
- Hits: Lingfield T21 566 lines, ratio 547 (H RA 106, Dec 94, Eq 58; J RA 114, Dec 107, Eq 68), midpoint 36 (H RA 3, Dec 8, Eq 3; J RA 8,
  Dec 9, Eq 5); T22 382 lines, ratio 56 (H RA 10, Dec 12, Eq 6; J RA 10, Dec 5, Eq 13), midpoint 2 (H RA 1, H Eq 1). Ascot T21 128 lines,
  ratio 119 (H RA 17, Dec 22, Eq 20; J RA 24, Dec 19, Eq 17), midpoint 5 (H Dec 1, H Eq 1, J RA 2, J Eq 1); T22 66 lines, ratio 11
  (H RA 2, Dec 3, Eq 1; J Dec 2, Eq 3), midpoint 0. Sizes: Lingfield 1.05 + 2.90 MB, Ascot 0.23 + 0.49 MB.
- Independent checker (15 Oct), from POSITIONS: completeness of T21 / T22 in both races (all counts above), every cell of every listed
  T21 side (Lingfield 1,132, Ascot 256) and every T22 side (750, 132) incl. timing, FIELD 21 / 22 every row: 0 mismatches. Note: FIELD 21
  also showed 0/n rows for T21 lines listed only by all three families (Lingfield 2, e.g. Capella – Spica; Ascot 9) - gone with the
  revised filter.
- T21 revised filter, lines before -> after: Lingfield 566 -> 198 (ratio >= 50: H RA 40, Dec 22, Eq 16; J RA 34, Dec 31, Eq 27 = 170;
  midpoint 36 unchanged: H RA 3, Dec 8, Eq 3; J RA 8, Dec 9, Eq 5; FIELD 21 137 rows, none empty); Ascot 128 -> 40 (ratio >= 50: H RA 4,
  Dec 5, Eq 11; J RA 5, Dec 7, Eq 6 = 38; midpoint 5; FIELD 21 38 rows). Sizes: Lingfield 0.98 + 2.90 MB, Ascot 0.21 + 0.49 MB.
  Tests 86/86 (test 17 T21 / T22 cases still pass; filter check added).
  Independent checker (15 Oct), Lingfield P05 from POSITIONS: 40 lines kept = the sheet (set and order); 72 dropped vs the old rule
  (64 ratio < 50 only, 7 three families only, 1 both), none in the sheet; every cell of the 40 lines, the P05 FIELD 21 column (39 cells,
  42 hits), no 0/n row, T22 unchanged: 0 mismatches.

## jupiter_tables: SKY cells in T1 / T2, sky side in T21 (Eddie, 15 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): the T1 / T2 SKY cells and their "same as sky" tag stay; T21 and its sky side are gone. Text kept for reference.
- T1 / T2: each row (natal Jupiter → body, star or equator X) has SKY cells S Jupiter → S X in the same plane, after the natal RA / Dec
  cells: value, +5 min, best family (score), group, offset, arrow, also, scaled ×10 / ÷10, exact timing (from the off + 5 min), coloured
  by score. The same SKY cells appear in T1 and T2 beside each natal row. Not in THREADS or NUMBERS.
- T21: a sky side "S Jupiter: S A – S B" (race-day star positions) on each line, same star pair and plane, the T19 cells, timing from
  the off + 5 min (Equator only when the sky three straddle the equator, so some Equator lines have no sky side).
- Tag "same as sky" (last column): T1 / T2 - the natal cell and the SKY cell hit the same number (best, also or scaled; family + digits,
  ×10 / ÷10 folded as in NUMBERS; no conjunction), per plane; T21 - per side, d(Jup, A) or d(Jup, B) whose best family hit is the same
  number as the sky side's same cell, or both ratios on the same interval (midpoint not part of the tag). Never d(A, B) (Eddie, 15 Oct
  2026, revised: star-star distances barely change from birth to race day).
- Listing unchanged: the sky side never adds or removes a row or line; FIELD sheets, THREADS and NUMBERS unchanged.
- First version counted d(A, B) too: Lingfield 26 lines (25 d(A, B) only), Ascot 6 (all d(A, B) only); revised the same day.
- Tags: Lingfield 14:35 2021 T1 0, T2 0, T21 1 (P11 Alphecca – Betelgeuse RA, horse 4/3 1.333184 (91.22), sky 4/3 1.335153 (20.61));
  T21 198 lines, 191 with a sky side. Ascot 14:30 2012 T1 0, T2 0, T21 0; T21 40 lines, 34 with a sky side. Sizes: Lingfield 1.05 + 2.90 MB, Ascot 0.23 + 0.49 MB.
- Test 18 (Lingfield 14:35 2021, by hand from POSITIONS): T1 P03 H Jupiter → H Sun SKY Dec 19.418627 (+5 19.419746) → 12×φ +0.00222
  (86.76), away, separating, exact 14:25 (9.9 min ago), no tag; T21 P11 Alphecca – Betelgeuse RA sky side 92.120174 / 122.994551 (φ^10
  99.13, applying 14:55) / 144.885275 (ninth 144.444, 53.32), ratio 1.335153 4/3 +0.13650 % (20.61), applying, exact 23:43 (in 548.3 min),
  far side; its tag (found by the rule) 'H: ratio 4/3 · fourth'; T21 still 198 lines; no tag on d(A, B). Tests 91/91. Lingfield and Ascot compared cell by cell with the previous build: only the new
  columns and the T1 / T2 / T21 titles and header rows differ.
  Independent checker (15 Oct), Lingfield from POSITIONS: every T1 / T2 SKY cell of P03 and P09 (364 plane cells), the T1 / T2 tags of
  all 6 runners (0; closest near-match P11 J equator Dec ÷10 1.438992 vs √2 1.414, not the sky's best scaled), every P11 T21 sky side
  (29 sides, 522 cells), every horse / jockey side of all 198 lines, the 26 tagged lines (same set), the listing (198 = the rule; 7 lines
  without a sky side, all Equator with the sky three on one side): 0 mismatches.

## jupiter_tables: areas A / B (Eddie, 15 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): the area blocks stay only in SKY PAIRS, SKY STARS and SKY ROYAL (SKY JUPITER); T12–T14, T19, T21, T22, P## PAIRS, P## RATIOS and the FIELD sheets are gone. Text kept for reference.
- Area A "whole + 3/2": intervals 1, 3/2, 2, 3, 4, 5, 6, 7, 8, 9, on ±0.02 absolute (see Families), or a midpoint hit (a midpoint is a
  unison). Area B "other": every other interval on the list (tapered %). Interval list, timing and scores otherwise unchanged.
- Split into blocks, area A first, then area B, each with its own title and count: T12, T13, T14, T19, T21, T22, SKY PAIRS, SKY STARS,
  P## PAIRS. Tables that list every row (T12–T14, T22, P## PAIRS) end with a "NO HIT" block. The filtered T19 / SKY PAIRS / SKY STARS
  end with "NO RATIO OR MIDPOINT HIT": rows listed only because all three distances have a family hit (Claude's choice, so the listing
  stays as before; Eddie to confirm or drop). Each row appears once: A if any of its cells / sides is A (T12 / T13 RA or Dec; T21 / T22 horse
  or jockey; T21 sides count at ratio >= 50 or a midpoint, not together), else B, else no hit; the T12 / T13 titles say how many A rows also
  carry a B hit in the other plane. Order inside each block as before (T19 / SKY PAIRS / SKY STARS / T21 best first; T12–T14, T22, PAIRS
  in their old order). Group column kept.
- P## RATIOS: area A, then area B; inside each area the groups in Eddie's order (B: Perfect (4/3), Imperfect, Dissonant, Septimal, High, Phi).
- FIELD 12–14: per plane, blocks A, B, no hit; each runner's cell in the block of its own hit; k/n per area (automatic unisons not
  counted). FIELD 21 / 22: blocks A, B, k/n per area.
- THREADS, NUMBERS and the midpoint tables (T10, T11, T17, T18, T20) keep their layout. Their ratio hits (THREADS T12 / T13) follow
  the new tolerance.
- Effect of ±0.02 on the A intervals (wider than before, e.g. unison was 1 %): Lingfield 14:35 2021 T19 1036 -> 1365 rows, SKY PAIRS
  59 -> 76, T21 198 -> 244 lines; Ascot 14:30 2012 T19 209 -> 265, SKY PAIRS 53 -> 68, T21 40 -> 44. Cobden (Wincanton 14:20 2022 P09)
  22 -> 25 unisons (5 genuine, all return-assisted: J Gonggong RA 1.001741, J Ketu RA 1.001694, J Pallas RA 1.013747, J Makemake Dec
  1.013955, J Haumea Dec 1.019953).
- Messi check (Ascot 19:45 7 Mar 2012 P01): T19 H Venus – H Neptune Dec 8.839548 / 35.534628, ratio 4.01996 -> area A hit on 4, offset
  +0.01996, score 0.00 (just inside ±0.02); also RA 3.015497 on 3 (5.07).
- Counts (rows; A / B / no hit, or A / B / all-three-families-only):
  Lingfield 14:35 2021: T12 P01 5/8/33, P03 5/4/37, P05 4/4/38, P07 10/4/32, P09 5/6/35, P11 4/3/39; T13 P01 3/4/39, P03 5/4/37,
  P05 8/3/35, P07 3/4/39, P09 4/4/38, P11 5/2/39; T14 P01 0/0/3, P03 0/1/2, P05 0/1/2, P07 1/1/1, P09 0/1/2, P11 0/0/3;
  T19 P01 120/118/10, P03 115/120/6, P05 112/101/4, P07 94/115/12, P09 85/142/10, P11 103/94/4; T21 (A / B) P01 14/22, P03 16/22,
  P05 26/20, P07 24/16, P09 16/30, P11 18/20; T22 P01 2/5/59, P03 5/7/54, P05 3/10/53, P07 11/10/38, P09 4/6/49, P11 11/2/53;
  RATIOS (A / B) P01 8/13, P03 10/10, P05 12/9, P07 14/9, P09 9/12, P11 9/6; PAIRS P01 280/244/3969, P03 274/247/4008,
  P05 262/228/4056, P07 248/252/3971, P09 229/276/3888, P11 234/219/4032; SKY PAIRS 34/35/7, SKY STARS 37/32/2;
  FIELD 12 RA 12/14/46, Dec 16/12/46; FIELD 13 RA 8/13/46, Dec 16/11/46; FIELD 14 1/3/3; FIELD 21 94/101; FIELD 22 19/19.
  T12 / T13 rows with A and B: 4 (P01 T12, P03 T12, P05 T13, P09 T13).
  Ascot 14:30 2012 (P01): T12 3/3/40, T13 3/3/40, T14 0/0/3, T19 105/151/9, T21 15/29, T22 6/7/53, RATIOS 6/6, PAIRS 238/295/3895,
  SKY PAIRS 25/31/12, SKY STARS 22/27/7; FIELD 12 RA 0/3/43, Dec 3/0/43; FIELD 13 RA 1/1/44, Dec 2/2/42; FIELD 14 0/0/3;
  FIELD 21 15/30; FIELD 22 6/6. Sizes: Lingfield 1.12 + 2.90 MB, Ascot 0.24 + 0.49 MB.
- Tests 92/92. Test 19 (new): every area A row has an A interval or a midpoint hit, every B row a B interval and no A hit, every
  no-hit row neither, in T12–T14, T19, T21, T22, SKY PAIRS, SKY STARS, P## PAIRS, P## RATIOS, FIELD 12–14 / 21 / 22 (Lingfield every
  runner + Ascot). Expected values changed by the ±0.02 tolerance (checked by hand from (10 (0.02 − dev) / 0.02)²): test 5 P05 Rahu
  1.005972 16.23 -> 49.20 (FIELD 12 now read from the area A block); test 6 Cobden 22 -> 25 unisons, P03 RATIOS now has a Harmonic
  section (check changed to "no empty group header"); test 7 Mars 1.002631 54.31 -> 75.42, Vesta 3/2 1.499361 76.06 -> 93.71 green,
  tolerance list; test 14 Uranus – Pluto unison 60.24 -> 78.87, Pluto – Sedna 1.011174 now a unison hit (19.47, was outside 1 %);
  sort checks per block; PAIRS rows read without block titles; test 17 Algorab – Castor 96.59 -> 98.29, Aldebaran 18.98 -> 51.53;
  test 18 T21 198 -> 244 lines.
- Independent checker (15 Oct), Lingfield P09 from POSITIONS (own interval and midpoint code): every T12–T14 cell (187), every T19
  row (237) incl. block, order and completeness (A 85 / B 142 of 1,982 candidates; 10 all-three-families rows), every P09 PAIRS row
  (4,393: A 229, B 276, no hit 3,888), every T21 / T22 side (46 + 59 lines), P09 RATIOS (21), FIELD 12–14 every cell and k/n, FIELD
  21 / 22 every cell and k/n, and the Messi check (whole Messi P01 T19, 202 rows): 0 mismatches. Not checked: order inside the PAIRS
  blocks, the T21 sky side.

## jupiter_tables: third area "φ and √2" (Eddie, 15 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): as areas A / B - kept on SKY PAIRS, SKY STARS, SKY ROYAL only. Text kept for reference.
- Area order: A "whole + 3/2" (1, 3/2, 2 … 9, ±0.02 absolute, or a midpoint hit); "φ and √2" (φ, φ², φ³, 1+√2, √2, 1+1/√2; 0.15 % as
  before; families.AREA_P, families.AREAS = A, P, B); B "other" (every remaining interval, taper); then "no hit" / "no ratio or midpoint
  hit" as before. Same tables as the A / B split (T12–T14, T19, T21, T22, SKY PAIRS, SKY STARS, P## PAIRS, P## RATIOS, FIELD 12–14 / 21
  / 22). A row goes once in the highest area it has a hit in (A, then φ and √2, then B): T12 / T13 over RA and Dec, T21 / T22 over horse
  and jockey sides, T19 / PAIRS over the midpoint (A) and the ratio. Each block title gives its count and "(n carry hits in more than
  one area)" when n > 0. FIELD sheets: each runner's cell (FIELD 21 / 22: each hit) in its own area's block, k/n per area. RATIOS: A,
  φ and √2, B, groups in order inside each. THREADS, NUMBERS and the midpoint tables unchanged. Tolerances, scores, listings unchanged
  (row totals per table as in the A / B entry).
- Rows per area (A / φ and √2 / B / no hit or all-three-families-only; [m] = rows carrying more than one area, in the A block unless noted):
  Lingfield 14:35 2021: T12 P01 5[1]/1/7/33, P03 5[1]/1/3/37, P05 4/1/3/38, P07 10/0/4/32, P09 5/0/6/35, P11 4/0/3/39;
  T13 P01 3/2/2/39, P03 5/0/4/37, P05 8[1]/1/2/35, P07 3/2/2/39, P09 4[1]/0/4/38, P11 5/0/2/39; T14 P01 0/0/0/3, P03 0/0/1/2,
  P05 0/0/1/2, P07 1/0/1/1, P09 0/1/0/2, P11 0/0/0/3; T19 P01 120/19/99/10, P03 115/12/108/6, P05 112/15/86/4, P07 94/17/98/12,
  P09 85/21/121/10, P11 103/16/78/4; T21 (A / φ√2 / B) P01 14[1]/5/17, P03 16/1/21, P05 26/0/20, P07 24/3/13, P09 16/3/27,
  P11 18/4[1, in the φ and √2 block]/16; T22 P01 2/0/5/59, P03 5/0/7/54, P05 3/3/7/53, P07 11[1]/0/10/38, P09 4/0/6/49, P11 11[2]/0/2/53;
  RATIOS P01 8/3/10, P03 10/1/9, P05 12/2/7, P07 14/2/7, P09 9/1/11, P11 9/0/6; PAIRS P01 280/36/208/3969, P03 274/32/215/4008,
  P05 262[1]/30/198/4056, P07 248/34/218/3971, P09 229/41/235/3888, P11 234/35/184/4032; SKY PAIRS 34/6/29/7; SKY STARS 37/5/27/2;
  FIELD 12 RA 12/1/13/46, Dec 16/2/12/46; FIELD 13 RA 8/4/9/46, Dec 16/1/10/46; FIELD 14 1/1/3/3; FIELD 21 94/17/92; FIELD 22 19/3/19.
  Ascot 14:30 2012 (P01): T12 3/1/2/40, T13 3/0/3/40, T14 0/0/0/3, T19 105[1]/24/127/9, T21 15[2]/2/27, T22 6/2/5/53, RATIOS 6/1/5,
  PAIRS 238[2]/46/249/3895, SKY PAIRS 25/3/28/12, SKY STARS 22/8/19/7; FIELD 12 RA 0/1/2/43, Dec 3/0/0/43; FIELD 13 RA 1/0/1/44,
  Dec 2/0/2/42; FIELD 14 0/0/0/3; FIELD 21 15/2/28; FIELD 22 6/2/5.
- Tests 92/92: test 19 now checks three areas (every φ and √2 row a φ / √2 hit and no A hit; every B row no A or φ / √2 hit) and the
  "carry hits in more than one area" counts in every block title; test 14's block reader knows the new area. No expected value changed.
- Independent checker (15 Oct), Lingfield P07 from POSITIONS (own interval, area and midpoint code): every T12–T14 cell (187), every
  T19 row (221) with completeness (A 94 / φ√2 17 / B 98 / 12 all-three-families), every P07 PAIRS row (4,471), every T21 / T22 side
  (238, incl. the T21 sky side), P07 RATIOS (23), every cell and k/n of FIELD 12–14 / 21 / 22, SKY PAIRS (76 rows, completeness); the
  "more than one area" title counts of all 6 runners: 0 mismatches. Open point (Eddie): a T21 side counted by its midpoint whose ratio
  scores under 50 - the ratio's area is not counted (rule as built); counting it would change only P05 T21 A (1 multi-area row instead of 0).

## jupiter_tables: SKY PAIRS body – royal, T19 sky side (Eddie, 15 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): SKY PAIRS body – royal stays; T19 and its sky side are gone. Text kept for reference.
- SKY PAIRS: new rows S Jupiter on one sky body (Moon included, not Jupiter) and one royal star (Aldebaran, Regulus, Antares,
  Fomalhaut), race-day positions, the T19 cells, timing from the off + 5 min, planes RA, Dec, Equator (straddle rule). Block column
  "body – royal" (body–body rows stay "S–S"); same filter, same area blocks, sorted with the rest. Body–body rows unchanged.
  Rows gained (A / φ√2 / B / no ratio or midpoint hit): Lingfield 14:35 2021 14 / 1 / 19 / 0 (SKY PAIRS 76 -> 110);
  Ascot 14:30 2012 14 / 3 / 10 / 1 (68 -> 96).
- T19 sky side: each T19 row gets "S Jupiter: S X – S Y" (same bodies, royal stars at race-day positions, same plane) after the natal
  cells: the T19 cells (three distances + family, ratio on the interval list, midpoint cells, between / far side, note), timing from the
  off + 5 min, coloured by score, then its area (A / φ and √2 / B / no hit) and the tag. "—" for H X – J X (one point in the sky), for
  Equator when S Jupiter, S X, S Y are on one side, and where X or Y is Jupiter (d = 0). Tag "same as sky": the natal and sky best family
  hit the same number on the same leg (d(S Jup, X), d(S Jup, Y) or d(X, Y); x10 / /10 folded, no conjunction), or both ratios on the same
  interval; parts joined with "; ". Unlike T21, d(X, Y) counts. Listing and blocks unchanged (set by the natal row); P## PAIRS, FIELD,
  THREADS, NUMBERS unchanged.
- Tags (rows, first version; revised below): Lingfield 14:35 2021 P01 4, P03 6, P05 7, P07 7, P09 8, P11 1 (33); Ascot 14:30 2012 P01 7. Note: 28 of the 40 carry a
  royal-star leg d(S Jup, star) (Lingfield 22 x Regulus Equator silver 2.414, one of them also ratio 5/4; Ascot 6 x Aldebaran 2×φ): a
  star hardly moves between birth and race day, so that leg repeats itself. None is on d(X, Y). Sky sides: Lingfield P01 216 of 248 rows, P03 205 / 241,
  P05 183 / 217, P07 194 / 221, P09 212 / 237, P11 182 / 201; Ascot P01 228 / 265. Sizes: Lingfield 1.27 + 2.90 MB, Ascot 0.28 + 0.49 MB.
- Tests 96/96: test 14's SKY PAIRS check allows "body – royal"; test 20 SKY PAIRS S Haumea – S Fomalhaut Dec (by hand from POSITIONS:
  Dec S Jupiter −14.389918, S Haumea 16.069041, S Fomalhaut −29.623914): 30.458960 / 15.233996 / 45.692955, ratio 1.999407 on 2 (−0.00059,
  94.16), between, area A; test 21 T19 P07 J Chiron – J Juno RA sky side (RA S Jupiter 325.797311, S Chiron 7.172849, S Juno 263.624221):
  41.375538 (silver 41.4, 60.65) / 62.173090 / 103.548628 (64×φ, 68.66), ratio 1.502653 on 3/2 (+0.00265, 75.23), between, area A; tag
  found by the rule "ratio 3/2 · fifth" (natal 1.513185 3/2, 11.61); every H–J row "—"; T19 still 1365 rows.
- Independent checker (15 Oct), from POSITIONS (own code): SKY PAIRS every body – royal and S–S row of both races (set per plane, block,
  order, every cell; Lingfield 110, Ascot 96); Lingfield P07 T19 natal set and order (221: A 94 / φ√2 17 / B 98 / 12) and every sky-side
  cell (8,619 cells; 194 sky sides, 27 "—": 7 H–J, 11 Jupiter, 9 Equator one side); Ascot P01 sky sides (10,335 cells, 228 sides, 37 "—");
  tags of all runners: 0 mismatches.
- Revised (Eddie, 15 Oct 2026): a T19 sky side tagged "X, Y together" is shown plain (values kept, no colour, no area, no tag), as
  together sides everywhere else; "same as sky" never counts d(S Jupiter, royal star) (the star barely moves birth -> race day);
  d(X, royal star) and the ratio still count. Together sky sides: Lingfield 8 (P01 2, P03 2, P07 2, P09 1, P11 1), Ascot P01 7.
  Tagged rows before -> after: Lingfield P01 4 -> 0, P03 6 -> 1, P05 7 -> 2, P07 7 -> 5, P09 8 -> 3, P11 1 -> 0 (33 -> 11);
  Ascot P01 7 -> 0. Dropped: 21 Lingfield rows tagged only on d(S Jup, Regulus) Equator silver 2.414 (P05 H Gonggong – H Regulus
  Equator keeps its ratio 5/4), 6 Ascot rows on d(S Jup, Aldebaran) 2×φ, and 1 together side each (Lingfield P03 H Orcus – H Transpluto
  RA, Ascot P01 H Transpluto – H Regulus RA, both ratio 1 · unison). Left: 8 ratio tags (Lingfield P03 J Orcus – J Regulus RA 1,
  P05 H Haumea – H Aldebaran Dec 1, H Gonggong – H Regulus Equator 5/4, P07 J Transpluto – J Regulus RA 1, J Chiron – J Juno RA 3/2,
  P09 J Venus – J Makemake Dec 2, J Orcus – J Regulus RA 1, H Transpluto – H Aldebaran RA 5/3) and 3 on a body leg (P07 J Vesta's
  d(S Jup, Vesta) 100×φ in J Juno – J Vesta, J Chiron – J Vesta, J Vesta – J Gonggong RA). None on d(X, Y). Tests 97/97 (test 21 checks
  both rules).
  Independent checker (15 Oct), from POSITIONS (own code): every cell of every T19 row of all 6 Lingfield runners and Ascot P01 (63,570
  cells), the 15 together sides (no colour, no area, no tag), fills kept on the other sky sides, every tag and why each dropped one went
  (Ascot Aldebaran legs: 2 Dec, 4 Equator): 0 mismatches.

## jupiter_tables: SKY block timing, royal-star-only tables (Eddie, 16 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): SKY block timing and SKY ROYAL stay; T21R, T22R, FIELD 21R / 22R are gone. Text kept for reference.
- SKY JUPITER "SKY" block (S Jupiter → every sky body, star and the equator): four new columns after the planes, "RA timing (best)",
  "RA timing (scaled)", "Dec timing (best)", "Dec timing (scaled)" (moved inside each plane's block the same day, see below): applying / separating and the exact race-local time of the best family
  hit and of the scaled (×10 / ÷10) hit, off -> +5 min linear, the T-table method and wording (exact_time). Empty where there is no hit.
  Nothing else in the block changes. Lingfield 14:35 2021: 15 best / 18 scaled timing cells (47 rows: 46 sky points + the equator); Ascot 14:30 2012: 23 / 28.
- Royal stars only (Aldebaran, Regulus, Antares, Fomalhaut), after the full tables (full tables unchanged); every line listed, hits and
  non-hits (non-hits plain), area blocks A / φ and √2 / B / NO HIT:
  - T21R (runner sheets, after T22): T21 for the six royal pairs, horse | jockey | sky side, same cells, areas (counted sides: not
    together, midpoint or ratio >= 50) and "same as sky" tags. Each T21 royal line is identical in T21R.
  - T22R (runner sheets, after T21R): T22 for the four royal stars; = T22's royal lines.
  - SKY ROYAL (SKY JUPITER, after SKY STARS): S Jupiter on the six royal pairs ("royal – royal") and every sky body with a royal star
    ("body – royal", the SKY PAIRS rows, identical cells), every row, best first per block; a "X, Y together" row plain, in NO HIT.
  - FIELD 21R / FIELD 22R: as FIELD 21 / 22 (T21R ratio hits >= 50), plus a NO HIT block (keys with no hit, 0/n).
- Lines (A / φ√2 / B / no hit): Lingfield T21R P01 1/0/1/16, P03 0/0/0/17, P05 4/0/1/13, P07 0/0/2/15, P09 1/0/1/15, P11 0/0/1/16;
  T22R P01 0/0/1/11, P03 2/0/2/8, P05 1/1/1/9, P07 2/0/3/5, P09 1/0/1/8, P11 1/0/1/10; SKY ROYAL 14/1/19/243 (277 rows: royal – royal 17,
  all no hit; body – royal 260); FIELD 21R rows 3/0/4, no hit 2; FIELD 22R 3/1/3, no hit 0. Ascot P01 T21R 0/0/1/16, T22R 2/1/1/8;
  SKY ROYAL 14/4/10/245 (273: royal – royal 17, 1 in φ and √2; body – royal 256; 2 together rows); FIELD 21R 0/0/1, no hit 5; FIELD 22R
  2/1/1, no hit 1. Sizes: Lingfield 1.36 + 2.90 MB, Ascot 0.32 + 0.49 MB.
- Tests 100/100: test 22 SKY S Jupiter → S Mercury (by hand from POSITIONS, off 14:35: Dec 11.063496 -> 11.065810 at +5, φ^5 11.090170,
  applying, exact 15:32 (in 57.6 min), scaled the same; RA 32.268875 -> 32.27372, /10 2×φ (20φ 32.360680) applying, exact 16:09 (in
  94.7 min); RA best outside, no timing) and a timing cell exactly where each best / scaled hit is; test 23 T21R / T22R = the royal lines
  of T21 / T22 with the same values (all Lingfield runners + Ascot), SKY ROYAL holds the SKY PAIRS body – royal rows unchanged.
- Independent checker (16 Oct), Lingfield from POSITIONS (own code): every SKY block cell incl. the timing (1,023 cells), SKY ROYAL
  (277 rows: 281 generated, 4 Ketu repeats dropped; 5,263 cells, blocks, order, fills), T21R / T22R of all 6 runners (7,760 cells; T21
  and T22 royal lines identical), FIELD 21R / 22R every cell and k/n: 0 mismatches. Lingfield has no together rows; Ascot's 2 (S Transpluto
  – S Regulus RA 0.929582 and Dec 0.156195) checked by hand: in NO HIT, no fill. Revised (Eddie, 16 Oct): a together
  SKY ROYAL row shows its values plain with no score (ratio score, ratio half, distance half, midpoint total empty; the RA unison was 24.22).
- Revised (Eddie, 16 Oct): every together side shows its values plain with no score (ratio score, ratio half, distance half, midpoint
  total empty) and no colour: T19 sky sides (Lingfield 8, e.g. P07 J Orcus – J Gonggong Dec 36.06 and H Venus – H Neptune Equator
  11.43 -> no score; Ascot 7), T21 / T21R sides (none in these two races), SKY ROYAL rows. Checked over both workbooks: none shows a score.
  Not changed: the P## PAIRS workbook (unfiltered; together rows keep their scores: Lingfield 175, Ascot 32) and the T17 / SKY EQ
  together lines (none in these two races).
- SKY block layout (Eddie, 16 Oct): each plane's timing inside its block, after its scaled column ("timing (best)", "timing (scaled)"):
  RA columns C-M, Dec N-X (the block has no Equator plane; the equator row is Dec). The scaled timing only when the scaled hit is a different
  number; a repeat (same family and digits, x10 / /10) shows one timing. Values and timing unchanged. Timing cells: Lingfield best 15,
  scaled 10 (8 repeats hidden); Ascot best 23, scaled 17 (11 hidden). Tests 103/103 (test 22 positions moved; together-score checks added).

## jupiter_tables: TIMELINE (Eddie, 16 Oct 2026; viewing only)
- Block TIMELINE at the end of the SKY JUPITER sheet: every sky Jupiter relationship on that sheet whose exact time falls from the off
  − 30 min to the off + 60 min, one row per event, sorted by time, with marker rows "OFF" (0 min) and "OFF + 5 MIN". Sources: SKY (best
  hit, scaled hit unless a x10 / /10 repeat, or the nearest target outside at the off), SKY EQ (unison), SKY PAIRS / SKY STARS / SKY ROYAL
  (ratio toward its interval or nearest interval, midpoint = unison, each distance leg with a family hit). Columns: exact clock, minutes
  from the off, source, relationship, plane, kind, target (family and number; interval with area), target value, value and score at the
  off (coloured), applying / separating, note ("outside at the off"; "also <other sources>"). Timing: the linear method (exact_t /
  exact_time), off -> +5 min. Left out: together rows, x10 / /10 repeats; each event once (distances by the two points, plane and number
  folded x10 / /10; an Equator distance with both points on one side = the Dec distance; ratios by pair, plane and interval; the first
  source named in the order SKY, SKY EQ, SKY PAIRS, SKY STARS, SKY ROYAL). Nothing else on the sheet changes; runner sheets unchanged.
- Events (before the off / first 5 min / after): Lingfield 14:35 2021 50 (18 / 5 / 27); Ascot 14:30 2012 35 (9 / 4 / 22). Sizes:
  Lingfield 1.37 + 2.90 MB, Ascot 0.32 + 0.49 MB.
- Tests 106/106 (test 24): every event inside −30 / +60, rows and markers in time order, every exact time = its source cell (84 of 85
  events matched to a timing cell on the sheet; the one SKY cell outside at the off recomputed); by hand from POSITIONS: S Jupiter → S Moon
  Dec (S Jupiter −14.389918, +0.0000425872 /min; S Moon −24.052038, −0.000983196 /min): 9.662120 growing 0.00102578 /min to 6×φ 9.708204,
  outside at the off, applying, exact 15:19 (in 44.9 min); markers 14:35 / 14:40.
- Independent checker (16 Oct), Lingfield from POSITIONS (own code): source blocks rebuilt (SKY PAIRS 110, SKY STARS 71, SKY ROYAL 277,
  SKY EQ 9: identical), the 50 events = the rule (none missing or extra; SKY EQ unisons all outside the window, no midpoint in it), every
  cell of the 52 rows incl. markers and fills, order, title counts, and every event's time = its source cells' timing text (49 SKY, 108
  pair-block texts): 0 mismatches.

## jupiter_tables: TIMELINE H / TIMELINE J (Eddie, 16 Oct 2026; viewing only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): TIMELINE H / J are gone (the sky TIMELINE stays). Text kept for reference.
- Two blocks at the end of every runner sheet, built as the sky TIMELINE (window off − 30 / + 60 min, rows, sort, OFF / +5 MIN markers,
  "outside at the off"): every timed relationship involving the horse's chart (H) / the jockey's (J): T5 / T6 S Jupiter → natal X and
  T7 / T8 S X → natal Jupiter (best hit, scaled unless a repeat, or the nearest target outside); T10 / T11 midpoint hits; T12 / T13 rows
  and T14 S / H, S / J (interval or nearest interval, scaled unless a repeat, automatic unisons left out); T16 crossings with a sky leg
  (RA − Dec -> 0); T17 "S Jupiter: X = Y" and T18 block-1 sides (hits, unison); T19 rows (ratio, midpoint, each leg with a sky leg and a
  family hit); T20 midpoint hits; T22 ratio, midpoint and the d(star, natal Jupiter) leg. Midpoints count only as hits at the off (as in
  the sky TIMELINE). Left out: sky-only and natal-only (fixed) relationships, together rows, automatic unisons, repeats. Each event once
  (first table in the order T5 … T22 named, the others "also …"); an event using both charts (e.g. T19 H X – J X, T10, T11 H Jupiter /
  J Jupiter | S X) in both blocks, noted "H + J". Target value written at full precision (a ratio's exact time is sensitive to it).
- Events H n (before / first 5 min / after) | J n (…), "H + J" events: Lingfield 14:35 2021 P01 H 21 (7/3/11) | J 16 (5/3/8), 1;
  P03 H 15 (5/2/8) | J 15 (7/0/8), 0; P05 H 18 (8/2/8) | J 15 (6/0/9), 1; P07 H 17 (7/1/9) | J 16 (6/2/8), 1; P09 H 32 (16/1/15) |
  J 17 (5/2/10), 1; P11 H 20 (5/2/13) | J 18 (6/0/12), 0. Ascot 14:30 2012 P01 H 14 (5/1/8) | J 15 (2/1/12), 1. No midpoint event falls in
  the window in these two races; most events are T19 ratios and T5–T8 distances. Sizes: Lingfield 1.39 + 2.90 MB, Ascot 0.32 + 0.49 MB.
- Tests 109/109 (test 25): every runner timeline event of both races recomputed from POSITIONS (249 events; distance, ratio, crossing,
  midpoint; linear off -> +5) = its exact time and clock, window, applying / separating, order, "H + J" exactly on events using both charts;
  by hand: P05 H S Jupiter → H Neptune RA (S Jupiter 325.797311, +0.000130972 /min; H Neptune 343.738939): 17.941628 shrinking to φ^6
  17.944272 -> separating, exact 14:14 (20.2 min ago), 94.19, also T19; P05 J S Jupiter → J Venus Dec (S Jupiter −14.389918,
  +0.0000425872 /min; J Venus 18.610635): 33.000553 -> 33, applying, exact 14:47 (in 13.0 min), 94.54, also T19.
- Independent checker (16 Oct), Lingfield P05 from POSITIONS (own code): both blocks complete (H 18, J 15; none missing or extra; widening
  to −40 / +70 adds only J Eris – J Antares RA 11/8 at −36.5 min), 481 cells and fills, order, markers, title counts, 31 source timing
  texts (T19, T22): 0 mismatches. Display note: an event a few seconds before the off (J T6 S Jupiter → J Juno RA 988×φ scaled, t −0.034)
  shows 0 min, "separating", 14:34, just above the OFF marker.

## jupiter_tables: LONG TIMELINE, sky equivalents on TIMELINE H / J (Eddie, 16 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): the sky LONG TIMELINE stays; LONG TIMELINE H / J and the sky equivalent cells (runner timelines only) are gone. Text kept for reference.
- LONG TIMELINE on SKY JUPITER and LONG TIMELINE H / J on every runner sheet (after TIMELINE / TIMELINE H / J): the same sources, rules and
  dedupe, filter = score at the off >= 80, any exact time (no-motion / fixed rows, together rows, automatic unisons left out). Two sections:
  SEPARATING, APPLYING; inside each by score at the off, highest first, ties by exact time (separating most recent first, applying soonest
  first) (Eddie, 16 Oct 2026; first built by time only). Columns as TIMELINE, but col 3 "from the off" as text (min under a day, else
  days; beyond 50 years "more than 50 years away / ago", also in the exact column) and a numeric "minutes from the off" last.
- Sky equivalent on every TIMELINE H / J and LONG TIMELINE H / J row (cols 14–19): the same relationship in the sky at the off, natal points
  replaced by the same sky body, same plane: value, best family / interval (area) or nearest outside, score, timing (exact_time), "same as
  sky" when event and sky are hits on the same target. "—" where two points become one (T10, T11, T12–T14, T19 H X – J X, T20, T22 ratio /
  midpoint) or there is no sky equivalent (Equator not straddling). A together sky side: values only. Never adds or removes a row.
- Counts (LONG: events, separating / applying): Lingfield 14:35 2021 SKY 26 (10 / 16); P01 H 24 (12 / 12), J 18 (10 / 8); P03 H 14 (7 / 7),
  J 22 (10 / 12); P05 H 19 (12 / 7), J 20 (9 / 11); P07 H 19 (10 / 9), J 19 (10 / 9); P09 H 23 (11 / 12), J 26 (10 / 16); P11 H 19 (8 / 11),
  J 19 (12 / 7). Ascot 14:30 2012 SKY 31 (14 / 17); P01 H 17 (9 / 8), J 23 (10 / 13). "same as sky" tags: 0 in both races (33 Lingfield +
  5 Ascot rows have both event and sky hits, all on different targets). Sizes: Lingfield 1.40 + 2.90 MB, Ascot 0.33 + 0.49 MB.
- Tests 113/113 (test 26): every LONG row >= 80 in the right section and order; every sky equivalent cell (371) recomputed from POSITIONS
  (value, target, score, timing); "—" on T12 / T13 / T22 ratios; by hand: P05 LONG H S Betelgeuse → H Jupiter RA (S Betelgeuse 88.791862,
  +0.000000131692 /min; H Jupiter 199.732329): 110.940467 -> 10×φ^5 110.901699 (86.51), applying, exact 24 Oct 2021 00:52 (+204.43 days);
  sky S Betelgeuse → S Jupiter RA 122.994551 -> φ^10 (99.13), applying, exact 14:55 (in 20.5 min); no tag.
- Independent checker (16 Oct), Lingfield from POSITIONS (own code): SKY JUPITER LONG TIMELINE (26 events, 560 cells), P07 LONG H / J
  (19 / 19, 441 cells each), every sky equivalent cell of P07 TIMELINE H / J and LONG H / J, and the same for P01, P03, P05, P09, P11:
  0 mismatches; no tag anywhere. Not exercised in this race: a T16 crossing event and a sky midpoint hit on a midpoint-kind event.

## jupiter_tables: LONG TIMELINE real exact times (Eddie, 16 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): real exact times stay on the sky LONG TIMELINE / LONG STAR TIMELINE; the runner LONG TIMELINE H / J are gone. Text kept for reference.
- LONG TIMELINE (sky and H / J): every event whose linear exact time is more than 60 min from the off gets its real exact time from the
  Swiss Ephemeris (the race engine rebuild_kit/celestial_bodies_swisseph.py, the race's site, as the positions; sky point at m minutes =
  workbook value at the off + engine(m) − engine(off); natal fixed): stepping outward from the off (10 min for a day, then 1 h, up to 1 year
  each way), the first crossing of the target, refined by bisection to the minute; not reached -> "not within 1 year" (section from the
  motion at the off). Applying / separating and the sections come from the real time; each section by score, ties by real time. The
  linear estimate is kept in the last column "linear estimate"; the numeric minutes column holds the real time. Short TIMELINE stays linear.
- Counts (events: separating / applying; real-searched; not within 1 year): Lingfield 14:35 2021 SKY 26 (10 / 16), 13, 1; P01 H 24
  (12 / 12), 8, 2; J 18 (10 / 8), 8, 1; P03 H 14 (7 / 7), 8, 0; J 22 (10 / 12), 9, 2; P05 H 19 (12 / 7), 11, 1; J 20 (9 / 11), 8, 4; P07 H
  19 (11 / 8), 11, 1; J 19 (9 / 10), 10, 1; P09 H 23 (11 / 12), 5, 1; J 26 (9 / 17), 10, 1; P11 H 19 (7 / 12), 8, 1; J 19 (12 / 7), 13, 1.
  Ascot 14:30 2012 SKY 31 (15 / 16), 14, 1; P01 H 17 (9 / 8), 7, 1; J 23 (10 / 13), 16, 0. Some events changed section (e.g. P07 H 10 / 9
  -> 11 / 8). Sizes: Lingfield 1.41 + 2.90 MB, Ascot 0.33 + 0.49 MB; Lingfield build about 11 s.
- Tests 114/114: P05 LONG H S Betelgeuse → H Jupiter RA (110.940467, 86.51 on 10×φ^5 110.901699): linear 24 Oct 2021 00:52 (+204.43 days),
  real "not within 1 year" - the engine keeps the distance between 110.933 and 110.945 over ±1 year (daily scan in the test); sky S Jupiter:
  S Pallas – S Rahu Dec on 2 (93.55): real 11:32 (−182.8 min) vs linear 11:31 (−183.4 min), checked by a direct engine lookup (the ratio
  crosses 2 between one minute either side).
- Independent checker (16 Oct), Lingfield with its own engine search (grid as above): SKY LONG TIMELINE and P03 LONG H / J - every real time
  within 1 min (e.g. SKY Pallas – Regulus RA −1064.1 vs linear −1072.1), linear estimates, sections, order, counts; the 3 "not within 1 year"
  (SKY Sirius – Rigel RA 14×φ, linear +15.76 days; P03 J S Deneb Algedi → J Jupiter Dec 22×φ, +196.00 days, and Equator 3.33333, +190.25
  days) confirmed by an hourly ±1 year scan (no sign change); short TIMELINE still linear: 0 mismatches.

## jupiter_tables: value scaling removed (Eddie, 16 Oct 2026)
Note 29 Oct 2026: of the tables named here only T1–T8, the SKY sheet blocks and the sky timelines remain (workbook trim). Text kept for reference.
- Every "scaled ×10 / ÷10" column, scaled timing cell, scaled THREADS / NUMBERS / TIMELINE hit and "(widens 10x in degrees)" note removed
  (tables, SKY sheets, TIMELINE, THREADS, NUMBERS, FIELD). Value cells per plane are 8 (value, +5, target, group, offset, score, arrow,
  also); the SKY block has one timing column per plane (RA C–K, Dec L–T); T1 / T2 SKY cells 8 + timing. Values, targets, scores and
  timings otherwise unchanged.
- Lost, cells whose only hit was a scaled one (value × plane): Lingfield 14:35 2021 SKY 9, T1 114, T2 115, T3 40, T4 31, T5 39, T6 27,
  T7 37, T8 40, T9 2, T12 8, T13 12, T14 0 (T1 / T2 include their SKY cells); Ascot 14:30 2012 SKY 13, T1 22, T2 29, T3 5, T4 5, T5 7,
  T6 7, T7 9, T8 5, T13 3.
- TIMELINE events before -> after: sky Lingfield 50 -> 48 (now 18 / 5 / 25), Ascot 35 -> 31 (7 / 3 / 21); H / J Lingfield P01 21 / 16 ->
  18 / 11, P03 15 / 15 -> 13 / 13, P05 18 / 15 -> 14 / 12, P07 17 / 16 -> 13 / 11, P09 32 / 17 -> 27 / 14, P11 20 / 18 -> 18 / 15;
  Ascot P01 14 / 15 -> 13 / 11. The Ascot sky event S Jupiter → S Deneb Algedi RA ×10 574×φ (score 0.00, 14:09) is gone; no Deneb
  Algedi Dec 216×φ event existed in either race (searched every sheet of all ten tables workbooks).
- THREADS lines (>= 50) before -> after: Lingfield 294 -> 195 (114 scaled lines gone; main lines hidden by a scaled repeat shown again),
  "+ n weaker" 660 -> 389; Ascot 60 -> 40 (25 scaled), 101 -> 56. Tags unchanged (they used the main hits only), cells carrying each: Lingfield
  mutual same chart 1, across 0, both Jupiters 1, both charts 32; Ascot 3 / 0 / 0 / 8 (a first count of 2 / 1 / 3 also counted the
  header row; corrected by the checker); one cell (Lingfield P03 Makemake) held only a scaled line ("directions 0", H Jup→H
  Makemake Dec 18.199475 x10 182) and is now empty. Ascot tags unchanged.
- Tests 110/110. Built on a scaled hit: test 8 (Nottingham Dynamic Force Uranus THREADS 'J Jup→H Uranus Dec 14.141031 /10 → 1.414
  (99.12) [T4, scaled]' and the repeat rule) -> moved to the value as it is, '→ 14.14 (96.90) [T4]' (√2 target form, found by the rule);
  test 22 (SKY S Mercury RA ÷10 on 2×φ, 16:09, and the scaled-timing checks) -> retired; the Dec φ^5 15:32 case kept, RA now outside with
  no timing; test 25 scaled factor dropped. Column positions moved (not results): COL Dec 11 -> 10, test 18 T1 SKY cells, test 19 T12–T14.
  New check: no scaling anywhere in the Lingfield and Ascot workbooks.
- Independent checker (16 Oct), Lingfield from POSITIONS (own code): no scaling left (26 "never scaled" notes only); every value cell of
  T1–T9, T12–T14 and SKY equal to the before workbook after the column shift, scaled-only counts as above; THREADS recomputed (lines 294 ->
  195, scaled 114 -> 0, "+ n weaker" 660 -> 389, tags unchanged, only P03 Makemake emptied); every P## NUMBERS sheet and FIELD NUMBERS
  recomputed (2,313 values; FIELD NUMBERS 1 row, ninth 14.4444 / 144.444, P09); TIMELINE = before minus the 44 scaled events, splits right:
  0 mismatches.

## jupiter_tables: T23 ratios of the T1, T2 and SKY distances (Eddie, 16 Oct 2026; viewing only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): T23 and FIELD 23 are gone. Text kept for reference.
- T23 on every runner sheet, straight after T2: one row per body, star or equator X in both T1 and T2 (not Jupiter), planes RA and Dec
  (equator: Dec, = |Dec| of the Jupiters, scored as T14), three ratios per plane, larger / smaller: H / J = d(H Jupiter, H X) / d(J Jupiter,
  J X) (new, natal, timing "fixed"); S / H = d(S Jupiter, S X) / d(H Jupiter, H X), S / J = d(S Jupiter, S X) / d(J Jupiter, J X) (the
  T12 values repeated; stars and equator new; timing from the off + 5 min). Per ratio 10 cells: value, +5, interval · name · group, group,
  offset, score, arrow, also (unison field count, as T12), area, timing; outside: nearest interval plain. Blocks A, φ and √2, B, no hit by
  the highest area on the row (as T12). Automatic (Jupiter return) unisons grey as T12 (S / H, S / J only; none in these two races).
  Together (Claude's reading of "together rows left out"): a ratio with Jupiter and X within the conjunction tolerance on a leg (RA < 1.5,
  Dec < 0.3) is left out - no value, no score, the leg named; the rest of the row stays. (A chart's own Rahu–Ketu never meets here: every
  leg is Jupiter–X.) FIELD 23: H / J cells, per plane, blocks A / φ and √2 / B / no hit, k/n per area (together cells left out).
  Functions: t23_cells, write_t23. Not in THREADS, NUMBERS, RATIOS or TIMELINE.
- Hits (cells with a score; A / φ and √2 / B): Lingfield 14:35 2021 P01 H / J 9/0/4, S / H 3/0/8, S / J 5/1/4; P03 9/0/6, 1/0/7, 7/1/4;
  P05 6/0/4, 4/2/7, 3/1/2; P07 2/1/4, 10/0/6, 9/0/5; P09 6/2/3, 3/0/5, 5/1/6; P11 6/4/4, 5/0/1, 3/0/2 (totals H / J 38/7/25, S / H 26/2/34,
  S / J 32/4/23). Rows (A / φ√2 / B / no hit, [m] more than one area): P01 15[4]/1/9/21, P03 16[6]/1[1]/9/20, P05 10[1]/3/11/22,
  P07 20[8]/0/8/18, P09 11[1]/3[1]/10/22, P11 12[3]/4/3/27. Together cells: P01 6, P03 10, P05 4, P07 6, P09 4, P11 8 (S Jupiter – S Deneb
  Algedi RA 0.960728 in every runner). Ascot 14:30 2012 P01 H / J 17/0/1, S / H 5/3/1, S / J 3/0/1; rows 21[2]/1/3/21; no together cell.
  Note: Ascot's H and J Jupiters are close (RA 6.77559, Dec 0.664246), so 14 of its 17 H / J area A hits are unisons, mostly on stars
  (first reported as 13: a miscount). Sizes: Lingfield 1.50 + 2.90 MB, Ascot 0.34 + 0.49 MB.
- H / J unisons, H–J Jupiters close (Eddie, 16 Oct 2026): the Jupiter-return rule with d(H Jupiter, J Jupiter) in the role of d(S Jupiter,
  natal Jupiter), per plane: q = d(H Jup, J Jup) / the smaller of d(H Jup, H X), d(J Jup, J X); q < 0.0015 -> grey "automatic (H–J
  Jupiters close)", counted nowhere (not in FIELD 23, the row's area block or title counts; also column "unison: automatic (H–J Jupiters
  close), not counted"); 0.0015 <= q < 0.02 -> tag "H–J assisted" (colour and counts unchanged). S / H, S / J keep T12's rule.
  Result: Lingfield 14:35 2021 7 H / J unisons (P01 Vesta RA, Procyon RA; P03 Vesta RA; P05 Juno RA; P07 Eris RA, q 0.033859 the lowest;
  P09 Sun RA, Dec), none automatic or assisted. Ascot 14:30 2012 14, 0 automatic, 11 assisted (all Dec: Algol, Pleiades, Aldebaran,
  Capella, Regulus, Alkaid, Arcturus, Alphecca, Vega, Polaris, Castor; q 0.005928 Polaris – 0.019112 Regulus); Gonggong RA (q 0.133689),
  Transpluto RA (0.051067), Sirius RA (0.038731) untagged. In Dec q is about the unison offset itself, so automatic would need an
  offset under ~0.0015. Block counts and FIELD 23 unchanged in both races. Tests 119/119 (test 27: every H / J unison's tag recomputed
  from POSITIONS; the automatic branch on a constructed case, J Jupiter and J Algol = H + 0.0001 Dec, q 1.57e-06).
- Distances on each row (Eddie, 16 Oct 2026): per plane, before the three ratios, S Jupiter → S X (= the T1 / T2 SKY cells: value, +5,
  best family, group, offset, score, arrow, also, timing from the off + 5 min), H Jupiter → H X (= T1) and J Jupiter → J X (= T2), timing
  "fixed" where scored; 9 cells each, coloured by score. A plane block is 57 columns (3 x 9 distances, 3 x 10 ratios; RA from C, Dec
  from BH). Ratios, areas, blocks (unchanged counts) and FIELD 23 unchanged. Sizes: Lingfield 1.57 + 2.90 MB, Ascot 0.36 + 0.49 MB.
  Tests 120/120: every distance cell group (1,911 over Lingfield and Ascot; values, texts, timing, value fill) = its T1 / T2 / SKY cells.
  Independent checker (16 Oct), Lingfield P07 from POSITIONS (own code): 46 rows, 2,457 distance cells (values, +5, targets / outside,
  offsets, scores, arrows, also, timing incl. dates, 'fixed'), 273 value fills, H / J = T1 / T2 natal cells, S = the T1 and T2 SKY cells:
  0 mismatches.
- Tests 117/117 (test 27): T23 rows complete; every S / H, S / J cell = T12 (644 cells; the 7 differences are together cells, all without
  a T12 score); P03 Haumea RA H / J by hand from POSITIONS (H Jupiter 165.660805, H Haumea 211.367148, J Jupiter 58.688530, J Haumea
  195.818927: 45.706344 / 137.130397 = 3.000249 (inverted) on 3, +0.00025, 97.53, area A, fixed); FIELD 23 = the T23 H / J cells.
- Independent checker (16 Oct), Lingfield P11 from POSITIONS (own code): 2,730 T23 cells (values, labels, scores, arrows, also, areas,
  timing), blocks and title counts (12[3] / 4 / 3 / 27), 4 together legs, 91 S / H, S / J cell groups = T12, FIELD 23 every runner (608
  checks incl. k/n): 0 mismatches.

## jupiter_tables: Galactic Centre, T24 stars against bodies (Eddie, 19 Oct 2026; viewing only)
- Galactic Centre = the 23rd fixed star (not royal): engine BEHENIAN_STARS ("Galactic Centre", "Galactic Center") = sefstars.txt
  'Galactic Center,SgrA*' (ICRS 17 45 40.036, −29 00 28.17), in rebuild_kit/celestial_bodies_swisseph.py and the card-pipeline copy
  ~/astronomy-project/celestial_bodies_swisseph.py (identical; that repo not committed; ~/astronomy-project/deep_reads_kit/engine copy not
  changed). Engine J2000 apparent at J2000.0: RA 266.410443, Dec −29.007559 (catalogue 266.417 / −29.008; the 0.007° is aberration, as every
  star). New batches carry 'Galactic Centre_B' on TRANS, horse and jockey sheets. Ascot 14:30 2012 rebuilt through run_card_swiss.py:
  every other row identical, GC sky 266.423154 / −29.007984, H 266.413036 / −29.007313, J 266.414632 / −29.008250; engine reproduction
  49 of 49 sky points. jupiter_tables STARS + 'Galactic Centre' (a batch without it: skipped quietly, so existing workbooks unchanged);
  it enters T1 / T2 star rows, SKY, T21, T22, T23, SKY STARS, FIELD 21 / 22, P## PAIRS (not T19 / royal tables). Rebuilt Ascot: GC lines
  SKY 1, T1 1, T2 1, T23 1, T21 4, T22 3, T24 3 rows.
- T24 (write_t24, t24_cell): one row per star (STARS order, those in the chart), one RA / Dec column pair per body: Sun, Moon (SKY only),
  Mercury … Transpluto, Rahu, Ketu (no equator). Header row 1 body names (merged over two columns), row 2 RA / Dec. Cell = distance
  (RA wrapped 0–180, Dec |ΔDec|), 6 dp, filled by its best family score (green >= 80, yellow 50–80, light < 50; conjunction RA < 1.5 /
  Dec < 0.3 counts, as T1; no fill outside); cell comment 'target · family · offset · score' (conjunction: '0 · conjunction (RA < 1.5) ·
  +0.06464 · 91.57', Claude's wording) or 'nearest: 58 · whole — outside ±0.02 · -0.02729'. Blocks: T24 SKY on SKY JUPITER after SKY
  ROYAL (race-day positions at the off); T24 HORSE and T24 JOCKEY on each runner sheet after T22R. No timing, +5 or field sheet.
  Nothing else changes: Lingfield 14:35 2021 and Ascot 14:30 2012 compared with the previous build sheet by sheet - identical apart from
  the T24 blocks and their blank rows (Lingfield 13 blocks, Ascot 3).
- Display (Eddie, 19 Oct 2026, layout only): every T24 value column width 11 (fits 177.745864), the star column at least 18 (it stays 30 on
  SKY JUPITER, 46 on runner sheets); shared columns only ever widened (before: Excel default 8.43). Lingfield 14:35 2021 and the rebuilt
  Ascot 14:30 2012 checked (tools/scans/families_audit/chk_t24/check_widths.py): 14,058 / 3,427 T24 cells fit their column, no column
  narrower, every cell's value, fill and comment unchanged vs the build before.
- Revised (Eddie, 19 Oct 2026): COLUMN ORDER - every block: all RA columns (one per body, body order), "RA midpoints", all Dec columns
  (same order), "Dec midpoints"; header row 1 "RA" / "Dec" merged over their body columns, row 2 body names. Values, fills, comments
  and widths (11) unchanged (checked cell by cell vs the build before: Lingfield 13,772, Ascot rebuilt 3,358; only "midpoint with" lines
  added). Midpoint columns width 40.
- MIDPOINTS (Eddie, 19 Oct 2026; t24_mids): each star row, plane and pair of bodies A, B of the block, the star as the middle point on the
  midpoint rule (mid_geom / mid_score: closeness of d(star, A), d(star, B) >= 90 %, distance half RA ±0.5 closer of near / far, labelled,
  Dec ±0.15 signed; total = ratio half + distance half); hits only. Left out: the chart's own Rahu – Ketu, "A, B together" (d(A, B) RA
  < 1.5, Dec < 0.3), a Ketu pair repeating the Rahu pair (same rounded distances). Midpoint cell: every hit, best total first, "Sun = Mars
  93.42 (near, between)" (Dec without side; between / far side as T17: d(A, B) within 1 % of d1 + d2), filled by the best total; the two
  body cells of each hit get a thick outline and the comment line "midpoint with <other body>: total nn.nn". SKY (Moon incl.), HORSE,
  JOCKEY alike.
  Hits (RA / Dec): Lingfield 14:35 2021 SKY 35 / 26; P01 H 27 / 22, J 29 / 20; P03 H 30 / 13, J 31 / 21; P05 H 25 / 18, J 37 / 18; P07 H
  23 / 23, J 43 / 16; P09 H 28 / 17, J 34 / 16; P11 H 27 / 21, J 37 / 25. Ascot 14:30 2012 rebuilt (23 stars) SKY 43 / 24; P01 H 44 / 17,
  J 32 / 24. Left out that would have been hits: together Ascot P01 H Capella and H Rigel RA Juno – Quaoar (d 1.3896; 64.50 / 52.24),
  Lingfield P05 J Sirius RA Saturn – Neptune (67.07), P07 H Regulus RA Orcus – Transpluto (85.76), P07 J Sirius RA Sun – Mercury (75.79),
  P09 H Regulus RA Venus – Pallas (83.30); Rahu – Ketu Lingfield P03 J Alkaid RA (46.33). Sizes: Lingfield 2.00 -> 2.04 MB, Ascot rebuilt
  0.47 -> 0.48 MB (pairs unchanged).
- Test 29: header layout of every T24 block (rebuilt Ascot 3, Lingfield 13); by hand from POSITIONS: SKY S Galactic Centre RA Mercury =
  Jupiter 153.457407 / 153.219387, offset +0.119010 far, 99.8449 %, 48.46 + 29.03 = 77.49, far side; HORSE H Arcturus RA Jupiter = Orcus
  69.091938 / 69.107610, +0.007836 near, 99.9773 %, 49.77 + 48.45 = 98.22, between; JOCKEY J Regulus Dec Chiron = Orcus 5.534608 /
  5.506910, −0.013849, 99.4996 %, 45.12 + 41.19 = 86.31, between (cell text, outlines, comment lines); the Capella together pair and the
  Alkaid Rahu – Ketu pair not listed, no "Rahu = Ketu" anywhere. Test 28's grid reader moved to the new layout. Tests 134/134.
- Independent checker (19 Oct), own code from POSITIONS (tools/scans/families_audit/chk_t24/check_midpoints.py): every midpoint of
  T24 SKY, HORSE and JOCKEY on the rebuilt Ascot (P01) and Lingfield (P07) - completeness, cell text and order, fills, outlines,
  comment lines: 0 mismatches; dropped would-be hits = the together pairs above; no Rahu – Ketu or Ketu-repeat hit in those six blocks.
- Sizes before -> after (tables + pairs): Lingfield 14:35 2021 1.57 + 2.92 -> 2.00 + 2.92 MB; Ascot 14:30 2012 0.36 + 0.50 -> 0.46 + 0.50 MB
  (22 stars, old batch); Ascot rebuilt with the Galactic Centre 0.47 + 0.51 MB.
- Tests 129/129 (test 28): Ascot rebuilt through the card pipeline in a temp folder (GC row on TRANS / P01 / P02, other rows identical,
  sky ~266.417 / −29.008); GC in SKY, T1, T2, T21, T22, T24, not T19; five T24 cells by hand from POSITIONS: SKY S GC – S Ceres RA
  150.475762 93×φ −0.00140 (91.54), HORSE H GC – H Mars RA 177.745864 ninth 177.778 −0.03191 (97.50), JOCKEY J GC – J Sedna Dec 32.362221
  20×φ +0.00154 (90.70), conjunction H Algorab – H Makemake RA 0.064638 (91.57), outside H GC – H Sun RA 57.972709 nearest 58; every grid
  23 x 50 sky (Moon) / 23 x 48 natal on the rebuilt Ascot, 22 rows on the old Lingfield / Ascot builds, every cell a value and comment.
  Fix: the suite now rebuilds Ascot 14:30 2012 itself (before, its Ascot checks read a workbook built on 16 Oct).
- Independent checker (19 Oct), rebuilt Ascot from POSITIONS (own code, families.py for targets, 262 squared scores re-derived by hand):
  every cell of T24 SKY (1,150: green 48, yellow 41, light 148, none 913, conjunction 12), P01 HORSE (1,104: 32 / 44 / 132 / 896, 6) and
  JOCKEY (1,104: 40 / 41 / 126 / 897, 6) - rows, headers, values, fills, comments: 0 mismatches. Script tools/scans/families_audit/chk_t24/.

## jupiter_tables: 35 stars in T1, T2, T24; trimmed workbook (Eddie, 19 Oct 2026; viewing only)
Note 29 Oct 2026 (workbook trim): the --full-only sheets are gone and --full is now the same as the default. Text kept for reference.
- Engine: 13 more stars in BEHENIAN_STARS (rebuild_kit/celestial_bodies_swisseph.py = ~/astronomy-project copy, identical; Polaris kept):
  Hamal, Pollux, Praesepe ('Praesepe Cluster'), Denebola, Zubenelgenubi, Zubeneschamali ('Zubeneshamali'), Kaus Australis, Nunki, Deneb,
  Sadalsuud, Sadalmelik, Scheat, Markab (sefstars.txt names; all found). Engine J2000 at J2000.0 vs catalogue, all within 0.02°
  (largest: Deneb 310.351008 / +45.282124, dRA −0.0070; Kaus Australis 276.036075 / −34.384768, −0.0069; Pollux 116.335168 / +28.025059,
  +0.0062). New batches carry them as '<name>_B'; the rebuilt Ascot 14:30 2012 batch = the old one + 14 rows (Galactic Centre + 13).
- tools/jupiter_tables.py: T1_T2_T24_STARS (35, |Dec| <= 50) = STARS without Polaris + NEW_STARS (in the given RA order, appended).
  T1, T2 (with their SKY cells) and T24 SKY / HORSE / JOCKEY use it (charts R['HX'] / R['JX'], sky on ctx.x with engine rates for the new
  stars). Every other table keeps STARS (23, Polaris incl.): T23 unchanged (Polaris kept), SKY block, T21 / T22 / R, SKY STARS, SKY ROYAL,
  PAIRS, TIMELINEs. THREADS / NUMBERS are still fed from the T1 / T2 rows on STARS (off-sheet), so they are unchanged. The new stars'
  positions are appended to POSITIONS (block 'T1 / T2 / T24 only ...'; Claude's choice, so the cells can be checked). Older batches: new
  stars skipped quietly, Polaris simply gone from T1 / T2 / T24.
- Sheets: default workbook = POSITIONS, SKY JUPITER, P## only; --full adds P## RATIOS, P## NUMBERS, THREADS, FIELD NUMBERS, every FIELD
  sheet (as before). run_card_swiss.py --tables writes the default. The _pairs workbook unchanged. The test suite builds with --full.
- Checked: --full vs the build before, sheet by sheet (tools/scans/families_audit/chk_stars35/compare_full.py): Lingfield 14:35 2021 only
  the Polaris rows gone (SKY JUPITER 1, each runner 4: T1, T2, T24 H, T24 J), 0 other differences, pairs identical; rebuilt Ascot the same
  plus 13 new-star rows on SKY JUPITER, 52 on P01 and 39 POSITIONS rows. Default runner / SKY sheets = the --full ones.
- Sizes (tables default / --full; pairs): Lingfield 14:35 2021 1.79 / 2.01 MB (before 2.04), pairs 2.92; rebuilt Ascot 14:30 2012 0.47 /
  0.54 MB (before 0.48), pairs 0.51.
- Tests 145/145. Test 30: default sheets (rebuilt Ascot, Lingfield) and equal to --full; T1, T2, T24 x3 = the 35 stars in order; no new
  star outside T1 / T2 / T24 in any sheet of the --full workbook or pairs; T23 = the old build's rows + Galactic Centre, Polaris kept; by
  hand from POSITIONS: T1 H Jupiter → H Pollux RA 166.673131 ninth 166.667 +0.00646 (99.45), H Markab Dec 37.994684 38 −0.00532 (53.90),
  SKY S Jupiter → S Pollux RA 56.678406 -> 56.677607 nearest 35×φ outside +0.04722; T2 J Hamal Dec 46.919384 29×φ −0.00360 (78.98),
  J Kaus Australis RA 0.188691 conj (76.42); T24 S Deneb – S Makemake Dec 17.799198 11×φ +0.00082 (94.97), H Pollux – H Eris Dec 32.999538
  33 −0.00046 (95.43), J Praesepe – J Neptune RA 138.999718 139 −0.00028 (97.20). Changed for the spec: test 28 batch rows (+13), T24
  grids 35 rows (old batches 21); test 27 T23-vs-T1 / T2 cells skip Polaris and the new stars (not in both).
- Independent checker (19 Oct), own code from POSITIONS (chk_stars35/check_t1_t2_t24.py), rebuilt Ascot: T1 / T2 all 35 star rows (natal
  and SKY cells, fills, timing of the 17 + 17 SKY hits), T24 SKY 1,750 / HORSE 1,680 / JOCKEY 1,680 value cells + 210 midpoint cells
  (new-star midpoint hits SKY 46, HORSE 23, JOCKEY 39), no new star elsewhere, --full vs before: 0 mismatches.

- Revised (Eddie, 19 Oct 2026): RA ORDER and the SKY BLOCK. T1_T2_T24_STARS is one fixed order, ascending engine J2000 RA at J2000.0
  (= Eddie's list exactly; engine Pleiades/Alcyone 56.8758 vs his 56.75, same order): Hamal 31.7957, Algol, Pleiades, Aldebaran, Rigel
  78.6399, Capella 79.1800, Bellatrix, Betelgeuse, Sirius, Castor, Procyon, Pollux, Praesepe, Regulus, Denebola, Algorab, Spica, Alkaid,
  Arcturus, Zubenelgenubi, Zubeneschamali, Alphecca, Antares, Galactic Centre, Kaus Australis, Vega, Nunki, Altair, Deneb, Sadalsuud,
  Deneb Algedi, Sadalmelik, Fomalhaut, Scheat, Markab 346.1879. T1 / T2 star rows (with SKY cells) and T24 rows reordered only. The SKY
  JUPITER "SKY" block star rows now use this list too (ctx.x, engine rates for the new stars; cells as before); NUMBERS still fed from the
  old SKY rows on STARS off-sheet; the sky TIMELINE / LONG TIMELINE never read the SKY block (built from STARS) - unchanged. Old batches:
  Lingfield 14:35 2021 has 21 rows (its 22 stars minus Polaris; no Galactic Centre), not 22.
  Compared with the build before (commit 1d37f4a9; chk_raorder/compare_raorder.py): T1 / T2 / T24 star rows matched by label identical
  (value, fill, comment, outline) - Lingfield 525, Ascot 175 rows; SKY block: Lingfield Polaris gone, Ascot Polaris gone + 13 new; every
  other row of every sheet identical (TIMELINE Lingfield 78 rows, Ascot 66). Sizes unchanged (Lingfield 1.79 / 2.01 MB, Ascot 0.47 / 0.54).
  Tests 153/153. Test 31: engine RA order; T1, T2, T24 x3 and SKY block order (Ascot 35, Lingfield 21); the comparison above built in the
  suite from commit 1d37f4a9; SKY block new-star cells = the T1 SKY cells (26 groups); by hand from POSITIONS: S Jupiter → S Praesepe RA
  70.378057 -> 70.377257, 70.7 √2 −0.33262 (0.35), separating, exact 18 Jun 2012 03:50 (2079.9 min ago); S Kaus Australis RA 143.593046
  -> 143.593845, ninth 144.444 −0.85140 (9.85), applying, exact 23 Jun 2012 07:15 (in 5325.3 min). Test 30's "no new star elsewhere"
  now allows the SKY block.
  Independent checker (19 Oct), own code from POSITIONS (chk_raorder/check_sky_block.py), rebuilt Ascot: engine RA order; row order of
  T1, T2, T24 x3 and the SKY block (35 each); every SKY block cell incl. timing (60 rows, 2,160 cells over the default and --full
  workbooks, 238 fills) and = the T1 / T2 SKY cells (4,720 comparisons); --full vs before (star rows by label, 3,248 other rows in order,
  TIMELINE / LONG TIMELINE incl.): 0 mismatches. No new-star SKY timing falls in the TIMELINE window (closest Nunki Dec, 601.5 min ago).

## jupiter_tables: T24 ratio tables (Eddie, 19 Oct 2026; viewing only, natal)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): T24 H / J, T24 HORSE RATIOS, T24 JOCKEY RATIOS are gone. Text kept for reference.
- On each runner sheet after T24 JOCKEY (column A = table id): T24 H / J, T24 HORSE RATIOS, T24 JOCKEY RATIOS (write_t24hj, write_t24r,
  t24r_cell). Rows T1_T2_T24_STARS in RA order (each chart's own star positions; older batches skip missing stars); header row 1 'RA' /
  'Dec' merged, row 2 column names; star column as T24, value columns width 11. Natal, fixed: no +5, no timing; not in THREADS, NUMBERS,
  RATIOS, FIELD or TIMELINEs; no sky version.
  - T24 H / J: per plane d(H star, H Jupiter), d(J star, J Jupiter) (= the T24 Jupiter cells, filled and commented as T24 but without
    T24's midpoint lines - Claude's choice: the midpoints stay in T24), ratio H / J.
  - T24 HORSE / JOCKEY RATIOS: one column per T24 body without Jupiter, RA then Dec; cell d(star, Jupiter) / d(star, X), same chart. No
    midpoint column.
  - Ratio cell: larger / smaller, 6 dp, interval list with the area tolerances, squared score, fill by score; comment 'interval · name ·
    group · area · offset · score' or 'nearest: <interval> · <name> — outside · <offset>'. Together (a distance < RA 1.5 / Dec 0.3): the
    word 'together', no fill, the leg named in the comment. Automatic / assisted as T23, applied (as T23) only to a unison hit: q = d(the two
    compared points) / the smaller distance (H / J: H Jupiter – J Jupiter, 'H–J Jupiters close'; RATIOS: Jupiter – X, 'Jupiter–X close');
    q < 0.0015 grey 'automatic (...), not counted'; 0.0015 to < 0.02 comment tag '... assisted (q ...)'. Title: hits per area (automatic
    not counted).
- Hits A / φ and √2 / B (together, assisted cells). Lingfield 14:35 2021 (21 stars): T24 H / J P01 5/0/3, P03 6/0/3, P05 4/0/1, P07 1/0/2,
  P09 3/1/0, P11 3/2/1 (22/3/10; together 5, assisted 0); HORSE RATIOS P01 48/12/58, P03 71/12/42, P05 36/11/54, P07 54/12/52, P09 51/4/63,
  P11 57/6/49 (317/57/318; together 141, assisted 74); JOCKEY RATIOS P01 63/11/66, P03 35/8/41, P05 70/8/42, P07 69/8/54, P09 54/9/67,
  P11 53/8/39 (344/52/309; together 47, assisted 82). Ascot 14:30 2012 rebuilt (35 stars) P01: T24 H / J 18/0/3 (together 2, assisted 17,
  all Dec: the H and J Jupiters are 0.664246 apart in Dec); HORSE RATIOS 62/17/89 (together 34, assisted 1); JOCKEY RATIOS 82/16/75
  (together 33, assisted 7). Automatic: none in either race.
- Sizes (tables default / --full): Lingfield 1.79 / 2.01 -> 2.15 / 2.37 MB; rebuilt Ascot 0.47 / 0.54 -> 0.57 / 0.63 MB (pairs unchanged).
- Tests 165/165. Test 32: layout (Ascot 35 rows, Lingfield 21, every runner); H / J distance cells = the T24 Jupiter cells; every ratio =
  larger / smaller of the T24 distances, 'together' where due (15,778 cells); T24 H / J of every old star = the T23 H / J star cell (value,
  interval, score; 296 cells); by hand from POSITIONS (Ascot P01): H / J Deneb RA 27.344209 / 34.130222 = 1.248170, 5/4 B −0.14640 % (7.18);
  H / J Altair RA 1.461534 nearest 3/2 outside −0.03847; H / J Vega Dec 1.010896 unison A (20.72), H–J Jupiters assisted (q 0.010788);
  HORSE H Algol / Sun RA 124.035817 / 82.656226 = 1.500623, 3/2 A +0.00062 (93.87); HORSE H Denebola / Uranus RA 1.618250 φ +0.01337 %
  (82.97); JOCKEY J Bellatrix / Makemake RA 2.000170, 2 A (98.31); JOCKEY J Alkaid / Gonggong Dec 1.019820 unison (0.01), Jupiter–X assisted
  (q 0.019820); together H / J Nunki RA (H Nunki – H Jupiter 0.805294); automatic none, assisted Ascot 25, Lingfield 156; every other sheet
  and row identical to the build before (commit 10b7d76a, chk_t24r/compare_t24r.py: values, fills, comments). Changed for the new tables:
  test 30 allows them in the "no new star elsewhere" check; compare_raorder.py (test 31) cuts them out.
  Independent checker (19 Oct), own code from POSITIONS (chk_t24r/check_t24r.py), rebuilt Ascot P01: every cell of the three tables
  (3,430: 140 distance, 3,290 ratio; values, fills, full comments, order, headers, title counts; 40 scores re-derived by hand): 0 mismatches.
  Notes: in Dec, when the star is not between the two compared points, q = the unison offset itself, so every Dec unison inside ±0.02 is
  tagged assisted (all 17 Ascot H / J; q 0.009213 Alkaid – 0.019112 Regulus) and none in RA (Sirius RA 1.019115, q ~0.0387); T24's
  midpoint lines are not copied to the H / J distance cells (9 Ascot cells, e.g. H Arcturus RA); the automatic branch and a two-leg
  together comment are not exercised in these races.

## jupiter_tables: SKY STARS and the sky timelines on the 35 stars (Eddie, 20 Oct 2026; viewing only)
- SKY STARS (SKY JUPITER) now pairs the 35 stars of T1_T2_T24_STARS (no Polaris), sky positions and rates on ctx.x as the SKY block.
  Pair orientation (Claude's choice, so every old pair row stays identical): the old STARS order without Polaris, then the new stars in RA
  order (RA order alone flipped old pairs, e.g. S Alkaid – S Betelgeuse -> S Betelgeuse – S Alkaid). Same cells, filter, blocks, sort.
- Sky TIMELINE and LONG TIMELINE are built on ctx.x (SKY star rows and SKY STARS as on the sheet); LONG real times from Ephem(ctx.x) (the
  engine for the new stars). Runner timelines, SKY PAIRS, SKY ROYAL, SKY EQ, T24 SKY, runner sheets, pairs workbook, NUMBERS unchanged.
- SKY STARS rows (A / φ and √2 / B / no ratio or midpoint hit): Lingfield 14:35 2021 37/5/27/2 -> 36/5/25/2 (3 Polaris rows gone; its old
  batch has no new stars); rebuilt Ascot 14:30 2012 25/8/22/7 -> 74/15/67/17 (5 Polaris rows gone, 116 new-star rows: 51/8/47/10).
- TIMELINE events (before / first 5 min / after): Lingfield 48 (18/5/25) unchanged; Ascot 31 (7/3/21) -> 38 (9/4/25): gone S Jupiter:
  S Capella – S Polaris RA 9/8 15:02 (+32 min); new (all SKY STARS ratios) S Algorab – S Hamal Equator 7/6 14:11 (−18.7), S Regulus –
  S Zubeneschamali Equator 4/3 14:18 (−11.7), S Vega – S Nunki Dec 1+√2 14:32 (+2.8), S Bellatrix – S Scheat Dec 8/5 14:36 (+6.1),
  S Aldebaran – S Scheat Dec 13/5 14:40 (+11.0), S Pollux – S Sadalsuud RA 1+1/√2 14:45 (+15.1), S Algol – S Sadalsuud Equator 3/2 15:16
  (+46.7), S Praesepe – S Sadalsuud RA 11/8 15:23 (+53.4).
- LONG TIMELINE (separating / applying; beyond 60 min, real-searched; not within 1 year): Lingfield 26 (10/16; 14; 1) -> 25 (10/15; 13; 1),
  gone S Jupiter: S Polaris – S Bellatrix Dec 5, 17:49 (+194.7 min); Ascot 31 (15/16; 15; 1) -> 47 (24/23; 25; 4), 16 new-star events
  (e.g. S Pleiades – S Nunki Equator 3/2, real 12:29 (−120.9 min), linear 12:28; S Betelgeuse – S Nunki Equator ninth 18.8889 real 06 Jul
  2012 16:11 (+17.07 days); not within 1 year: S Altair – S Sadalsuud Dec 14.4444, S Aldebaran – S Sadalmelik Equator 10×φ, S Aldebaran –
  S Zubeneschamali Dec 16×φ). No SKY-block star event in either list (none in the window or >= 80). No other event changed.
- Sizes (tables default / --full): Lingfield 2.15 / 2.37 MB (unchanged); Ascot 0.57 / 0.63 -> 0.59 / 0.65 MB.
- Tests 172/172. Test 33: SKY STARS complete (every pair-plane measured, listed = the filter rule; Ascot 1,575 pair-planes, 173 listed;
  Lingfield 609, 68); against commit bb23ade2 (chk_sky35/compare_sky35.py): old rows identical, dropped = Polaris, added = new star,
  every other event and row unchanged; every new-star event: time = its source cell (within 60 min) or re-searched with the engine
  (7 real times, 3 not within 1 year by a daily ±1 year scan); by hand from POSITIONS: S Algol – S Sadalsuud Equator 21.230864 / 14.151491
  / 35.382355, 1.500256 3/2 +0.00026 (97.45), applying 15:16 (in 46.7 min), between; S Vega – S Nunki Dec 19.061666 / 46.018632, 2.414198
  1+√2 −0.00065 % (99.13), applying 14:32 (in 2.8 min) = the TIMELINE event; LONG S Pleiades – S Nunki real 12:29 (ratio crosses 3/2 within
  ±1 min). Changed for this: tests 30 (allows SKY STARS / TIMELINEs), 31 (TIMELINE: before minus Polaris = after minus new stars), the
  compare scripts of tests 31 / 32 skip SKY STARS and the sky timelines.
  Independent checker (20 Oct), own code from POSITIONS + engine (chk_sky35/check_sky35.py), rebuilt Ascot: SKY STARS 595 pairs / 1,575
  pair-planes (13 together), 173 listed = the sheet, blocks 74 / 15 / 67 / 17, order, 3,806 cells and fills; vs before 5 Polaris rows
  dropped, 57 old rows identical, 116 new; TIMELINE / LONG star events rebuilt (13 / 22 = the sheet), every non-new-star event identical,
  11 real times within 1 min of its own search, 4 "not within 1 year" by an hourly ±1 year scan: 0 mismatches. Note: star–star distances
  move non-linearly over days (annual aberration), so their linear estimates can be far off (S Betelgeuse – S Nunki: linear +1.76 days,
  real +17.07 days); the table uses the engine time beyond 60 min.

## jupiter_tables: 11 more stars, 46 in T1, T2, T24 and the sky star tables (Eddie, 20 Oct 2026; viewing only)
- Engine: BEHENIAN_STARS + Alpheratz, Algenib (gamma Peg), Difda (beta Cet; sefstars' own 'Deneb Kaitos' = iota Cet, not used), Mirach,
  Menkar (looked up as ',alCet' = alpha Ceti; plain 'Menkar' returns lambda Ceti, Dec +8.9), Phact, Adhara, Wezen, Menkent, Unukalhai,
  Rasalhague (rebuild_kit copy = ~/astronomy-project copy). J2000 at J2000.0 vs catalogue all within 0.02° (largest Adhara dRA +0.0070,
  Phact +0.0069, Wezen +0.0062, Rasalhague −0.0060). Script tools/scans/families_audit/chk_stars46/engine_check.py.
- T1_T2_T24_STARS = 46 (|Dec| <= 50, no Polaris), engine RA order = Eddie's list exactly (Alpheratz 2.0961 ... Markab 346.1879); NEW_STARS
  = the 13 + the 11. The 11 go exactly where the 35 are used: T1 / T2 (+ SKY cells), T24 SKY / HORSE / JOCKEY (+ midpoints), T24 H / J,
  T24 HORSE / JOCKEY RATIOS, SKY block, SKY STARS (orientation: old STARS order without Polaris, then the 24 new stars in RA order), sky
  TIMELINE / LONG TIMELINE; POSITIONS block 'T1 / T2 / T24 only' lists all 24. No code change beyond the lists.
- Compared with the build before (commit 7d88f329; chk_stars46/compare_46.py): every row not naming one of the 11 identical (values, fills,
  comments) in both races; only count titles differ (SKY STARS and its areas, TIMELINE, LONG TIMELINE + sections, T24 H / J, RATIOS titles);
  pairs workbooks identical; Lingfield 14:35 2021 (old batch, 21 stars) unchanged apart from the SKY STARS title ('35' -> '46').
  Rebuilt Ascot 14:30 2012 new-star rows: POSITIONS 33; SKY JUPITER SKY 11, SKY STARS 139, T24 11, TIMELINE 12, LONG TIMELINE 20; P01 T1 11,
  T2 11, T24 22, T24 H / J 11, T24 HORSE / JOCKEY RATIOS 11 each.
- Rebuilt Ascot counts before -> after: SKY STARS (A / φ and √2 / B / no ratio or midpoint hit) 74/15/67/17 -> 140/24/123/25 (1,035 pairs,
  2,754 pair-planes, 312 listed); TIMELINE 38 (9/4/25) -> 50 (12/4/34), new e.g. S Jupiter: S Denebola – S Unukalhai RA 3/2 14:43 (+13.5,
  99.91), S Menkar – S Praesepe RA 5 14:23 (−6.1, 95.88), S Jupiter → S Adhara RA 45 15:19 (+49.0, SKY, also SKY STARS); LONG TIMELINE 47
  (24/23; 25 real-searched; 4 not within 1 year) -> 67 (33/34; 39; 7), new not within 1 year: S Spica – S Menkar RA 155.556, S Fomalhaut –
  S Algenib RA 18.8889, S Mirach – S Zubeneschamali Dec 45. T24 H / J hits (A / φ√2 / B) 18/0/3 -> 22/0/3, HORSE RATIOS 62/17/89 -> 91/24/119,
  JOCKEY RATIOS 82/16/75 -> 100/21/100 (assisted 25 -> 29; no automatic). T24 midpoint hits on new-star rows: SKY 39, HORSE 18, JOCKEY 24.
- Sizes (tables default / --full; pairs): rebuilt Ascot 0.59 / 0.65 -> 0.69 / 0.76 MB, pairs 0.51 unchanged; Lingfield 2.15 / 2.37 MB unchanged.
- Tests 187/187 (test 34 new): engine catalogue and Menkar = alpha Ceti; the 46 = engine order = Eddie's list; the 46 / 21 in order in every
  table above; vs 7d88f329 (compare_46.py) as above, the 11 only in the allowed tables, pairs identical; TIMELINE / LONG TIMELINE new-star
  counts; by hand from POSITIONS: T1 H Menkar RA 122.563385 ninth 122.222 +0.34116 (52.76), H Adhara Dec 6.184544 10×φ^-1 +0.00420 (74.64);
  T2 J Rasalhague Dec 36.018968 36 +0.01897 (0.27), SKY cell S Jupiter → S Unukalhai Dec 13.296270 ninth 13.3333 −0.03706 (55.52); T24
  HORSE H Phact – H Makemake Dec 63.104540 39×φ +0.00121 (92.64); T24 HORSE RATIOS H Menkar Dec Jupiter / Mercury 1.501372 3/2 A +0.00137
  (86.75); SKY block S Adhara RA 45.007846 45 +0.00785 (36.93) applying 15:19, S Menkar RA 14.076783 14.14 −0.06535 (0.57); SKY STARS
  S Denebola – S Unukalhai RA 3/2 and S Menkar – S Praesepe RA 5. Changed for this: tests 28, 30 – 33 star counts (35 -> 46), T32 assisted
  Ascot 25 -> 29; the comparisons of tests 31 – 33 with their builds before run on a 35-star copy of the rebuilt batch; test 33 handles a
  S Jupiter → star leg event (S Jupiter → S Menkent Equator).
  Independent checker (20 Oct), own code from POSITIONS + engine (chk_stars46/check46_*.py), rebuilt Ascot: engine and batch (+25 '_B' rows,
  rest identical); order of the 46 everywhere; every cell of T1 / T2 (46 rows), T24 SKY 2,300 / HORSE 2,208 / JOCKEY 2,208 + midpoints,
  T24 H / J and RATIOS 4,508, SKY block 2,556, SKY STARS 6,864 (completeness, blocks, order; 173 old rows identical); TIMELINE / LONG star
  events rebuilt, 24 real times within 1 min, 7 not within 1 year by an hourly scan; the 11 nowhere else; Lingfield unchanged: 0 mismatches.

## families.py: half family and the 4-digit rule (Eddie, 24 Oct 2026; every table follows)
PARTLY REMOVED 29 Oct 2026 (Eddie): the half family is gone (see "half family removed"); the 4-digit rule and its wording stay. Text kept for reference.
- Rules in Families above; one change in tools/families.py (active_vibrations.py untouched, wrapped). jupiter_tables.py changed in one line:
  NUM_FAMILIES + 'half' (Claude's choice: NUMBERS lists half numbers too). Half vs conjunction: the highest score wins in the conjunction
  range (Eddie, 24 Oct 2026, kept; examples in Families). Where a digit-family best failed the match the conjunction came back (e.g. Ascot
  S Betelgeuse – S Moon RA 1.415202 √2 92.25 -> conj 0.32).
- Wording (Eddie, 24 Oct 2026, second commit the same day): a value inside its family's old tolerance that fails the 4-digit match reads
  '<target> <family> — not a 4-digit match (<offset>)' in every cell text and comment that shows the nearest target (T-table target cells
  incl. SKY cells, T23, SKY block, T24 / T24 H / J comments 'nearest: ...', FIELD 5–8 cells, timeline sky-equivalent cells); beyond the old
  tolerance '— outside ±<tol>' stays; no score, no fill on either (families.outside 'digit' = inside_old; jupiter_tables digit_text). Offset
  as the offset cells ('-0.00360'). Texts changed vs 10b18003 (cells + comments, default / --full): rebuilt Ascot 1,486 / 1,508, Lingfield
  2,290 / 2,411; texts per form (not a 4-digit match / outside, every family, cells + comments, --full): Ascot 1,508 / 9,238, Lingfield
  2,411 / 16,367. Compared cell by cell (chk_half/compare_wording.py, both
  races, default and --full, pairs too): only those texts differ, same target / family / offset, every value inside the old tolerance and
  scoring nothing now: 0 mismatches. Test 43: that comparison in the suite (builds by 10b18003's code) and by hand T2 J Jupiter → J Hamal Dec
  46.919384 '29×φ golden — not a 4-digit match (-0.00360)' (|off| < 0.03236, 4691 vs 4692) and SKY S Jupiter → S Pollux RA 56.678406
  '35×φ (golden) — outside ±0.0324' (+0.04722); expected texts of tests 1, 18, 22, 30, 31, 34, 36, 42 moved to the new wording; test 26's
  sky-equivalent check reads the new form; test 41 now compares the 5e10f7bf builds with builds by 10b18003's code (old wording, so it still
  checks the repeats alone). Tests 242/242.
  Independent checker (24 Oct), own code (chk_half/indep/: wfam.py, check_wording_cells.py, check_wording.py, diff_wb.py, wording_extra.py),
  all four workbooks: every nearest-target text matched to its value and rebuilt (Ascot 10,570 / 10,746, Lingfield 17,727 / 18,778 texts,
  default / --full; T1–T9, T23, T24 and T24 H / J comments, SKY block, FIELD 5–8, runner timeline sky-equivalent cells), T1 / T2 / SKY block
  / T24 recomputed from POSITIONS, cell by cell vs the build before (only these texts differ; pairs identical): 0 mismatches.
- Hits per family before -> after (whole / half / golden / φ power / ninth / √2 / silver / conj):
  Rebuilt Ascot 14:30 2012: T1 6→6 / 0→5 / 9→2 / 16→0 / 9→1 / 3→0 / 1→0 / 1→1; T2 5→6 / 0→3 / 6→2 / 10→1 / 12→0 / 4→1 / 0→0 / 1→1;
  T24 SKY 141→148 / 0→66 / 114→35 / 144→5 / 169→14 / 37→3 / 29→1 / 25→26; T24 HORSE 127→138 / 0→80 / 106→29 / 132→3 / 160→13 / 31→1 /
  29→1 / 23→24; T24 JOCKEY 117→120 / 0→74 / 106→31 / 135→7 / 154→13 / 40→3 / 24→1 / 21→22; SKY block 7→7 / 0→1 / 9→4 / 6→0 / 10→0 / 5→0 /
  2→0 / 1→1. Lingfield 14:35 2021 (all runners): T1 17→18 / 0→14 / 17→5 / 35→1 / 39→2 / 10→0 / 5→0 / 8→8; T2 21→22 / 0→7 / 23→7 / 20→0 /
  24→2 / 3→0 / 3→0 / 4→4; T24 SKY 33→34 / 0→22 / 54→19 / 47→3 / 41→1 / 8→0 / 12→1 / 7→7; T24 HORSE 214→227 / 0→109 / 190→58 / 217→12 /
  316→27 / 62→2 / 63→1 / 51→55; T24 JOCKEY 229→244 / 0→116 / 234→71 / 226→12 / 305→20 / 63→1 / 54→2 / 24→24; SKY block 3→3 / 0→2 / 3→2 /
  5→2 / 1→0 / 1→0 / 1→0 / 1→1.
- Events before -> after: Ascot sky TIMELINE 90→90, LONG 69→61, STAR 65→66, LONG STAR 45→44; P01 TIMELINE H / J 68→68 / 63→65, LONG 50→49 /
  49→51, STAR 57→57 / 52→52, LONG STAR 45→44 / 44→44. Lingfield sky 48→49, 13→10, 3→5, 2→2; runners (6, H + J summed) TIMELINE 223→253,
  LONG 139→132, STAR 49→73, LONG STAR 39→38 (new events: half hits and nearest targets that are now half). THREADS lines >= 50 (+ n weaker):
  Ascot 40 (56) → 21 (19), Lingfield 195 (389) → 101 (208). T19 Lingfield 1365 → 1334 rows (41 all-three-families rows lost a leg hit, 10
  gained a half leg), Ascot 265 → 257; SKY PAIRS Lingfield 110 → 105, Ascot 96 → 85. T24 repeats: Ascot SKY 24 → 1 rows (S Rukbat 56 whole),
  HORSE 20 → 0, JOCKEY 27 → 1 (J Algol 63 whole); Lingfield SKY 8 → 1 (S Betelgeuse 16 whole), runner blocks (rows, all 12 summed) 88 → 6. Wincanton 14:20 2022 FIELD
  NUMBERS: no number held sky + horse + jockey any more.
- Sizes (tables default / --full; pairs): rebuilt Ascot 0.98 / 1.04 → 0.94 / 1.00 MB, pairs 0.51 → 0.49; Lingfield 2.17 / 2.39 → 2.11 / 2.32 MB,
  pairs 2.92 → 2.85.
- Tests 240/240. Test 42 (new): half and digits4 by hand (27.5 100, 27.505 25.00, 27.515 none; silver 24.1400 match, 24.1500 / 24.1399 not;
  φ^-1 0.6180 match; 2.414 vs 24.14 not; ninth 166.60 match, 166.70 not; golden 95.46 / 95.44; √2 14.141031 / 14.13), the score inside a
  match = the old score; real cells by hand from POSITIONS (rebuilt Ascot P01): T2 J Rasalhague RA 12.499623 half (92.61), T1 H Rahu Dec
  10.487259 '10.5 (half) — outside ±0.01', T2 J Kaus Australis RA 0.188691 conj (76.42), T1 H El Nath RA 158.570201 98×φ (83.05), T2 J Gonggong
  Dec 1.414256 √2 (99.66), T1 H Sun RA 41.379591 silver outside (was 63.73); compare with the build before (commit 83850b1c's tools/ and
  rebuild_kit/, chk_half/compare_half.py), both races default and --full: every target / leg / T24 cell = old families before and new after,
  every changed row holds a value the two families evaluate differently (or count digits, a THREADS weaker line, or a timeline event that
  went with its source row): 0 mismatches. Reworked (old -> new, why): test 1 T5 S Jup → H Mercury RA 14.439854 ninth 95.14 -> outside (1443
  vs 1444); test 8 Dynamic Force Uranus T5 11.10793 ninth line gone (1110 vs 1111), Transpluto tags 'mutual … directions 3' -> 'directions
  1' (T6 141.532633 √2 1415 vs 1414, T8 13.368851 ninth 1336 vs 1333 out; T7 33.33254 still a match, 99.05); test 9 Wincanton P01 'ninth:
  11.1111 / 111.111' sky + horse + jockey -> 'ninth: 11.1111' HORSE only (S Sirius 111.443941, J Venus 11.139997 out; H Regulus 11.11928
  still 86.63), tag checked on P11 'whole: 10' two of three, FIELD NUMBERS empty; test 18 natal Dec 2.609925 φ^2 -> outside, T21 sky leg
  144.885275 ninth -> 'no family'; test 21 S Chiron 41.375538 silver 60.65 -> 'no family' (64×φ 103.548628 still 68.66); test 21 T19 1365 ->
  1334 rows; test 22 S Mercury Dec 11.063496 φ^5 (15:32) -> outside, no timing; test 26 LONG section check allows an event within 0.05 min of
  the off (P07 LONG J S Jupiter → J Spica RA 124.500003 half, 2 s before); test 30 J Hamal Dec 46.919384 29×φ 78.98 -> outside; test 31 SKY
  S Praesepe RA 70.378057 √2 and S Kaus Australis RA 143.593046 ninth -> outside, no timing; test 34 H Menkar RA ninth, H Adhara Dec 10×φ^-1,
  SKY S Unukalhai Dec ninth, S Menkar RA √2 -> outside; test 36 SKY S El Nath Dec ninth, T24 J Facies – J Neptune Dec 1×φ (92.49), SKY
  S Meissa RA silver, S Al Rescha RA 18×φ, SKY S ONC RA silver -> outside; tests 34 / 36 / 37 / 38 / 39 / 40 timeline, SKY STARS and STAR
  SELECT counts (their old-code builds run on today's families); test 41 repeats counts (Ascot SKY 24 / 27 -> 1 / 1, Lingfield 8 / 8 -> 1 / 1)
  and its three hand cases (Menkent silver, ONC ninth, Castor ninth all outside now) moved to Ascot S Rukbat 56, J Algol 63 and Lingfield
  S Betelgeuse 16 (midpoint cells, thick kept). Old-commit builds in the suite get the NUM_FAMILIES half line (old_code()), so each
  comparison still checks its own change.
- Independent checker (24 Oct), own code from POSITIONS (chk_half/indep/: fam.py, check_cells.py, classify.py, conj_scan.py, half_low_scan.py;
  digit test on a 12-significant-digit string), rebuilt Ascot and Lingfield, default and --full, and the before builds against the old rules:
  every T1 / T2 natal and SKY cell, T24 SKY / HORSE / JOCKEY cell (value, comment, fill, red), SKY block (timing where a score is), T24
  repeats, T19 / T19 sky-side / SKY PAIRS legs; hits per family as above; every changed value a lost digit-family hit, a new half hit, a best
  family changed for one of those, or a nearest target changed to half: 0 mismatches. Not checked: T3–T23 cells other than those, timing values.

## families.py: whole numbers on the target (Eddie, 27 Oct 2026; every table follows)
- tools/families.py score_whole_t replaces active_vibrations.score_whole for the whole family (active_vibrations.py untouched): t = round(v),
  1 <= t <= 200, |v − t| < 0.02, same squared formula. Changes only 0.98 < v < 1 (now on 1) and 200 < v < 200.02 (none in any table: distances
  are <= 180). Conjunction rule unchanged: inside the range (RA < 1.5) the highest score wins, so an RA value 0.98–1 now shows whole 1 where
  whole beats the conjunction (e.g. Kelso P05 T24 HORSE H Regulus RA 0.989905: conj 11.56 -> 1 whole 24.53), T24 red kept.
- Compared with the build before (commit f1327932; chk_whole/diff_whole.py, rows aligned per sheet, pairs workbooks too), --full (default
  = the same minus the --full-only sheets); every changed / added row holds a value 0.98 < v < 1, plus follow-ons. Full list:
  docs/classic/whole_on_target_20261027.md. Rows changed / added / follow-on (--full; default):
  Kelso 14:50 2022 127 / 3 / 3 (125 / 2 / 2): T24 cells, T24 (SKY STARS) copies and SCORES, SKY STARS SUMMARY, PAIRS legs; P03 S Jupiter →
  H Eris Dec 0.99268 now 1 whole (40.19) in T5 and FIELD 5, which adds two T19 rows (H Eris – H Makemake, H Eris – H Fomalhaut Dec, all three
  legs with a family) and a P03 NUMBERS row 'whole: 1'; P05 H Rigel 0.99016 (T1, T23, T21 legs, T24, T24 H / J); P01 J Menkar a new T24 repeat
  '1 whole ×2'. Follow-ons: P01 T24 JOCKEY title repeat count, P03 T19 block count (3 -> 5 rows), THREADS P03 Eris '+ 1 weaker'.
  Lingfield 14:35 2021 repo batch (21 stars) 20 / 0 / 0; Eddie's 67-star rebuild (~/astronomy-project/racecards/20210402_lingfield_aw) 31 / 0 / 0,
  incl. P09 T24 HORSE H Meissa – H Transpluto Dec 0.997954 -> '1 · whole · -0.00205 · 80.59' green; rebuilt Ascot 14:30 2012 10 / 0 / 0.
  No SKY block star cell lies in 0.98–1 in these races: the SKY STARS selection is unchanged; no TIMELINE / LONG TIMELINE event changed.
- Tests: test 45 (new): the by-hand family cases (0.997954 -> 80.59, 0.98 none, 0.981 -> 0.25, 1.002 -> 81.00 = score_whole, 199.99 / 200.01
  -> 200), the comparison above (four races, default and --full, counts and follow-ons), Meissa by hand from POSITIONS. Test 44 now
  compares b19fac1f with builds by f1327932's code; test 42 runs its checker from b19fac1f's copy (its families); test 43 compares the
  10b18003 builds with builds by b19fac1f's code, both on today's families. Tests 248/248.
- Independent full scoring sweep (27 Oct; own family code from the Families rules, no families.py / active_vibrations.py, only the 48 ninth
  ranges copied as data; chk_whole/sweep/): every distance cell with a value (T1–T9, T17 / T19 / T21 / T21R / T22 / T22R legs, T23, SKY block,
  T24 SKY / HORSE / JOCKEY / H / J / (SKY STARS) incl. the summary, SKY EQ / PAIRS / STARS / ROYAL, P## PAIRS legs, timeline distance cells),
  default and --full (same counts): tables + pairs cells Ascot 18,843 + 13,710, Kelso 84,527 + 83,301, Lingfield repo 38,311 + 80,751,
  Lingfield 67-star 85,363 + 82,872: 0 cells wrong (no missing / extra hit, no other target or score; scores off at 2 dp only within the
  6-dp rounding of the shown value). On the builds before the fix it finds the old bug (Lingfield 67-star 17 cells, repo batch 6, all 0.98 < v < 1).
  Not covered: midpoint / ratio cells, T16 (no crossing in these races), together sides, the --full-only sheets (FIELD 5–8 text, THREADS,
  NUMBERS, RATIOS), "also" columns, the nearest target of no-hit cells.
  Decided (Eddie, 27 Oct 2026): keep as built (a) - highest score wins; a value just under 1 / 10 / 100 can show as ninth 0.999999 / 9.999999 /
  99.999999 and one just over as whole. (The ninth targets are written that way in _NINTH_RANGES and the 4-digit rule matches against them;
  e.g. Kelso P01 T8 RA 99.998689 ninth 99.13, whole 100 would be 87.32; Ascot P01 T24 Dec 9.999769 ninth 98.47; right at 10.000000 a 6-dp
  value can read either way (Lingfield P07 T24 Dec / Equator 10.0 ninth 100.0).)

## jupiter_tables: MATCH HORSE / MATCH JOCKEY (Eddie, 30 Oct 2026; viewing only)
- RATIO TIGHTENED (Eddie, 30 Oct 2026, same day; EXACT unchanged): whole - a ratio row only when the circle factor gcd(A, B, 360) >= 5 (no
  fraction cap); new columns after 'shared factor': 'circle factor' and 'slice of 360' (1/(360 / circle factor)); golden - gcd of the
  multipliers >= 2 AND p, q <= 6 for the ratio in lowest terms (circle columns blank). Sort unchanged; the title gives the rules and
  'RATIO m rows (whole w, golden g)'. Rows are now 21 columns. RATIO before -> after (whole / golden), EXACT unchanged:
  Kelso P01 H 569 (438 / 131) -> 68 (60 / 8), J 569 (432 / 137) -> 66 (66 / 0); P03 H 570 (426 / 144) -> 85 (82 / 3), J 549 (395 / 154) -> 58
  (49 / 9); P05 H 676 (515 / 161) -> 85 (80 / 5), J 546 (428 / 118) -> 82 (70 / 12); P07 H 589 (463 / 126) -> 88 (76 / 12), J 538 (398 / 140) ->
  69 (57 / 12); P09 H 520 (422 / 98) -> 71 (64 / 7), J 557 (458 / 99) -> 70 (66 / 4); P11 H 625 (470 / 155) -> 80 (70 / 10), J 642 (484 / 158) ->
  74 (67 / 7); total 6,950 (5,329 / 1,621) -> 896 (807 / 89). Lingfield P01 H 42 (30 / 12) -> 10 (9 / 1), J 49 (37 / 12) -> 5 (4 / 1); P03 H 42
  (39 / 3) -> 11 (10 / 1), J 44 (24 / 20) -> 6 (4 / 2); P05 H 47 (37 / 10) -> 10 (9 / 1), J 48 (41 / 7) -> 7 (6 / 1); P07 H 50 (23 / 27) -> 8
  (6 / 2), J 62 (46 / 16) -> 13 (12 / 1); P09 H 38 (28 / 10) -> 9 (8 / 1), J 59 (41 / 18) -> 13 (12 / 1); P11 H 41 (27 / 14) -> 16 (12 / 4), J 50
  (27 / 23) -> 13 (11 / 2); total 572 (400 / 172) -> 121 (103 / 18). Rebuilt Ascot P01 H 459 (429 / 30) -> 90 (89 / 1), J 400 (378 / 22) -> 91
  (90 / 1); total 859 (807 / 52) -> 181 (179 / 2). Largest table now Kelso P05 MATCH HORSE 106 rows (21 + 85). Sizes: Kelso 2.56 -> 2.00 MB,
  Lingfield 0.84 -> 0.80, Ascot 0.62 -> 0.56.
  Test 51 now compares a76a3e99 -> now (EXACT rows identical after the 2-column shift, every RATIO row one of the old ones) and 9e5d5ea5 ->
  now; by hand (Kelso P01 MATCH HORSE): whole kept S Aldebaran RA 69.998800 70 / H Bellatrix – H Chiron RA 90.005060 90 -> 9/7, circle factor
  10, 1/36; whole dropped S Fomalhaut Dec 28 / H Kaus Australis – H Mars RA 30 (circle factor 2; was 15/14); golden kept S Ras Algethi RA
  62×φ / H Menkar – H Saturn RA 93×φ -> 3/2, 31×φ; golden dropped S Haumea RA 88×φ / H Praesepe – H Quaoar RA 86×φ (44/43). Tests 148/148.
  Independent checker (30 Oct), own code (chk_match/indep/check_ratio_rule.py), all three races: outside MATCH identical (Kelso 260,754
  cells), EXACT rows identical after the shift, MATCH rebuilt from POSITIONS on the new rules (set, 21 cells, order, fills, titles): 0
  mismatches; every after RATIO row an old one; dropped whole (cf 1 / 2 / 3 / 4) Kelso 345 / 2,398 / 655 / 1,124, Lingfield 47 / 81 / 82 / 87,
  Ascot 60 / 432 / 136 / 0; golden dropped by the cap Kelso 1,532, Lingfield 154, Ascot 50; 12 planted errors all caught. Note: 'shared
  factor' on whole rows is text ('10'), 'circle factor' a number.
  The text below describes the first rule (gcd >= 2 for both), kept for reference.
- Every runner sheet, after T24 JOCKEY: MATCH HORSE, then MATCH JOCKEY (sky_match_cells, t24_match_cells, match_pairs, write_match). Sky side:
  every scoring cell of the SKY block (SKY JUPITER: S Jupiter → every sky body, star, the equator; RA, Dec). T24 side: every scoring cell of
  T24 HORSE / JOCKEY: star rows × body columns (not the S Jupiter column), and the Jupiter rows H Jupiter → H body, S Jupiter → H body, S body →
  H Jupiter (J on JOCKEY) incl. their Jupiter cell (not S Jupiter → S body). Scoring = the cell's best family has a score (any score);
  conjunction cells (best = conjunction, target 0) left out of both sides (Claude's default). A cell inside the conjunction range whose best is
  whole 1 takes part (red on the T24 sheet; Kelso 3 such cells, all EXACT rows against S Jupiter → S Venus Dec 1.012418 whole 1). Either plane
  with either plane. Families as in families.py at build time (best family only).
- EXACT: same family and target; across families the two 6-dp values with the same first 4 significant digits, truncated, same order of
  magnitude (families.digits4). RATIO (whole and golden only): same family, different targets sharing a factor >= 2 (whole: gcd; golden: gcd
  of the multipliers), ratio = larger / smaller in lowest terms + decimal. Ninths, φ powers, √2, silver: exact only.
- Layout: title (rules, EXACT n / RATIO m rows, scoring cells per side), header, rows: table, section, ratio p/q ('1'), decimal, shared factor
  ('2', '2×φ'), sky relationship, plane, value, family, target, score, T24 row, body, plane, value, family, target, score, lower score. EXACT by
  lower score, highest first (ties: SKY block order, then T24 order); RATIO by ratio, lowest first, ties by lower score. Score cells filled
  by score (as their source cells; a red conjunction-range T24 source -> its score colour). Two blank rows between the blocks; widths unchanged.
- Counts (EXACT / RATIO per table, H | J): Kelso 14:50 2022 (SKY block 18 scoring cells): P01 12 / 569 | 17 / 569, P03 16 / 570 | 15 / 549,
  P05 21 / 676 | 14 / 546, P07 16 / 589 | 16 / 538, P09 14 / 520 | 18 / 557, P11 11 / 625 | 14 / 642 (largest P05 HORSE 697 rows; all under
  2,000); Lingfield 14:35 2021 (7): P01 2 / 42 | 2 / 49, P03 5 / 42 | 2 / 44, P05 3 / 47 | 2 / 48, P07 3 / 50 | 2 / 62, P09 2 / 38 | 1 / 59,
  P11 2 / 41 | 4 / 50; rebuilt Ascot 14:30 2012 (11): P01 9 / 459 | 14 / 400. Totals: Kelso EXACT 184 (5 cross-family) / RATIO 6,950 (whole
  5,329, golden 1,621; 348 under 1.1, e.g. golden 48/47); Lingfield 30 / 572 (whole 400, golden 172); Ascot 23 (2 cross-family) / 859 (whole
  807, golden 52). Every cross-family exact pairs a sky golden with a T24 whole (e.g. Kelso S Praesepe RA 131.047819 81×φ with H Praesepe –
  H Venus RA 131.005156 131). Sizes: Kelso 1.88 -> 2.56 MB, Lingfield 0.77 -> 0.84, Ascot 0.54 -> 0.62.
- Tests 148/148. Test 51 (new): chk_match/check_match.py vs builds by 9e5d5ea5's own tools/, three races: every other cell / merge / width /
  freeze identical; the MATCH rows rebuilt from the SKY block and T24 cells on the sheet (set, cells, fills, order, title counts); by hand from
  POSITIONS (Kelso P01 MATCH HORSE): exact S Rukbat Dec 38.994109 39 / H Hamal – H Quaoar Dec 39.000850 39; cross-family S Praesepe RA 81×φ /
  H Praesepe – H Venus RA 131 (digits 1310); whole ratio S Fomalhaut Dec 28 / H Kaus Australis – H Mars RA 30 -> 15/14, factor 2; golden ratio
  S Haumea RA 88×φ / H Praesepe – H Quaoar RA 86×φ -> 44/43, factor 2×φ; left out: S Rukbat RA 68 against the 58 whole T24 HORSE cells on
  targets coprime to 68. Changed for this: test 30's new-star leak check allows the MATCH tables; tests 49 / 50 now compare builds by
  acf68341 / 2cc2af2b / 9e5d5ea5's own tools/ (each its own change; before they used the current code).
- Independent checker (30 Oct), own code from POSITIONS (chk_match/indep/; only the ninth ranges and φ-power targets as data), all three races:
  every non-MATCH cell before vs after (Kelso 260,754, Lingfield 147,664, Ascot 110,704), merges, widths, freeze; every SKY / T24 value used
  (1e-6), own scoring and matching: row set, all 19 cells, order, fills, title counts: 0 mismatches; 10 planted errors all caught. Not exercised:
  ninth / √2 / silver matches (none in these races; φ powers only φ^10 exact).

## families.py: half family removed (Eddie, 29 Oct 2026; every table follows)
- tools/families.py: 'half' out of DEG_FAMILIES, score_family, evaluate / best and outside() (never a nearest target, so never in "outside" /
  "not a 4-digit match" texts or tightness); score_half and HALF_TOL deleted (nothing else used them). Whole, the 4-digit rule, golden, φ powers,
  ninths, √2, silver, conjunction, ratios and midpoints unchanged. jupiter_tables.py: no change needed (NUM_FAMILIES went with the trim; its
  remaining "half" words are the midpoint method's "ratio half" / "distance half"). Frozen readers untouched (never had half).
- Effects vs 2cc2af2b (Kelso 14:50 2022 / Lingfield 14:35 2021 / rebuilt Ascot 14:30 2012; default = --full), counted by the independent checker:
  half hits before 1,009 / 372 / 244: T-tables 107 / 75 / 18 -> no score, Lingfield 1 -> conjunction (P11 T3 H Jupiter → J Ketu RA 1.497436);
  T24 892 / 295 / 226 -> no score, Kelso 7 -> golden (e.g. P03 J Pollux – J Transpluto RA 27.500448: half 91.23 -> 17×φ 65.71), 1 -> √2 (P07 H
  Difda – H Orcus RA 141.498994: 80.89 -> 141.4 79.25), conjunction back Kelso 2 (P09 H Vindemiatrix – H Makemake RA 1.495272, J Algol – J Rahu RA
  1.490544), Lingfield 1 (P11 J Alphecca – J Quaoar RA 1.498093, was 65.50), all now conj 0.00 (red as before); Kelso 14 'also' cells lost half.
  Nearest targets moved off half: 4,209 / 1,611 / 925 (T24 golden 1,391 / 485 / 292, ninth 1,238 / 432 / 280, φ power 677 / 219 / 163, silver
  175 / 50 / 45, √2 163 / 59 / 24, whole 154 / 60 / 34; T-tables golden 171 / 104 / 31, ninth 145 / 126 / 32, φ power 67 / 49 / 12, silver
  11 / 9 / 3, √2 11 / 7 / 3, whole 6 / 11 / 6). T24 repeats: Kelso 3 half repeats gone (P03 J Kaus Australis 53.5, P07 H Alphecca 36.5, P11
  J Betelgeuse 150.5; repeated targets 25 -> 22); Lingfield, Ascot none. SKY STARS rows listed only for three family legs: Kelso 9 dropped
  (26 -> 17), Ascot 2 (6 -> 4; Sirius – Procyon Equator, Procyon – Alphecca Dec on the 14.5 leg), Lingfield 0; SKY PAIRS / SKY ROYAL unchanged
  (leg cells: Kelso 52, Lingfield 13, Ascot 26 changed). SKY JUPITER timelines (half events lost, none gained): TIMELINE Kelso 75 -> 72,
  Lingfield 49 -> 45, Ascot 90 -> 87; LONG Kelso 54 -> 50, Ascot 61 -> 60; STAR Lingfield 5 -> 3, Ascot 66 -> 65; LONG STAR unchanged; no 95 /
  100 / 95 cell changed. Sizes: Kelso 1.89 -> 1.88 MB, Lingfield 0.78 -> 0.77, Ascot 0.54.
- Compared cell by cell (chk_nohalf/check_nohalf.py, every sheet, rows aligned): every changed cell named half before or sits in its value
  group, dropped rows named half, otherwise title counts and timeline follow-ons; no half family text after: 0 unexplained in all three.
- Tests Tests 146/146. Test 42: '(a) half by hand' retired -> 'half removed' (no half family, score_family raises, no half in evaluate / outside, RA
  1.497 -> conj); (c) J Rasalhague RA 12.499623 '12.5 (half)' 92.61 -> '12.2222 (ninth) — outside ±0.0722', H Rahu Dec 10.487259 '10.5 (half) —
  outside ±0.01' -> '11.1111 (ninth) — outside ±0.0611'; (d) compare_half (83850b1c vs b19fac1f, expected 'half 0 -> 66') retired. Old-commit
  builds that run on today's families.py moved counts (old -> new): T34 Ascot TIMELINE 50 (12 / 5 / 33) -> 47 (10 / 4 / 33), LONG 53 (23 / 30)
  -> 49 (21 / 28); T36 TIMELINE 90 (29 / 8 / 53) -> 87 (27 / 7 / 53), LONG 108 (47 / 61) -> 104 (45 / 59); T37 Ascot sky LONG 108 (>= 90: 60) -> 61 now 104 (59) -> 60, STAR 66 -> 65, TIMELINE 90 -> 87, P01 LONG J 21 (8) -> 51 now 19 (6) -> 49,
  TIMELINE J 13 -> 65 now 11 -> 63; T38 Lingfield LONG STAR P05 J 3 -> 2, P07 J 3 -> 2, P09 H 2 -> 1, P11 J 3 -> 2; T39 Ascot STAR 66 -> 65. Test 50 (new): the
  comparison above in the suite (builds by 2cc2af2b's own tools/ and rebuild_kit/), by hand from POSITIONS: Kelso P03 J Pollux – J Transpluto
  RA 27.500448 -> 17×φ golden (65.71) yellow; Lingfield P11 T3 H Jupiter → J Ketu RA 1.497436 -> conj; Kelso SKY S Jupiter → S Gonggong RA
  21.582451 nearest 21.5 half -> 22.2222 ninth.
- Independent checker (29 Oct), own family code from the rules (chk_nohalf/indep/; only the 48 ninth ranges and the φ-power exponents as data;
  with half switched on it reproduces the before builds: 0 errors), all three races: no half text (midpoint words excluded); every T1–T8, SKY
  block and T24 cell recomputed from POSITIONS (Kelso 6,231 value groups + 45,806 T24 cells, Lingfield 3,931 + 15,906, Ascot 1,191 + 10,426),
  T24 repeats, pair legs (2,919 / 3,231 / 1,344), sky TIMELINE SKY events; before vs after every cell: 0 unexplained; 10 planted errors all
  caught. Not covered: timing values, T24 midpoint cells (unchanged), pair ratio / midpoint cells, LONG real times.

## jupiter_tables: workbook trimmed (Eddie, 29 Oct 2026)
- The workbook is now POSITIONS, SKY JUPITER (whole: SKY block, SKY EQ, SKY PAIRS, SKY STARS, SKY ROYAL, T24 SKY, TIMELINE, LONG TIMELINE,
  STAR TIMELINE, LONG STAR TIMELINE) and one sheet per runner with T1, T2, T3, T4, T5, T6, T7, T8, T24 HORSE, T24 JOCKEY only (S Jupiter column,
  midpoints, repeats, red, widths, freeze C4 as before). Removed: T9, T10, T11, T12, T13, T14, T16, T17, T18, T19, T20, T21, T21R, T22, T22R,
  T23, T24 H / J, T24 HORSE / JOCKEY RATIOS, T24 HORSE / JOCKEY (SKY STARS), TIMELINE H / J, LONG TIMELINE H / J, STAR TIMELINE H / J, LONG STAR
  TIMELINE H / J; the SKY STARS SUMMARY sheet; every --full-only sheet (P## RATIOS, P## NUMBERS, THREADS, FIELD NUMBERS, every FIELD sheet);
  the _pairs workbook (P## PAIRS). --full is accepted and changes nothing (run_card_swiss.py --tables unchanged apart from its help text;
  rebuild_kit copy = ~/astronomy-project copy). The sections above marked REMOVED / PARTLY REMOVED keep their text for reference.
- T24 HORSE / JOCKEY: five rows straight after the two header rows, before the star rows (column A 'T24'): 'S Jupiter → S body' (the T1 / T2
  SKY cells), 'H Jupiter → H body' (J on JOCKEY; T1 / T2), 'S Jupiter → H body' (T5 / T6), 'S body → H Jupiter' (T7 / T8), then 'stars' (bold,
  grey D9D9D9 from A to the repeats column - before it ran to the sky hit column of the (SKY STARS) table). Same cells, format and blanks as on
  the (SKY STARS) tables; the Jupiter column on the last two = d(S Jupiter, natal Jupiter), computed directly (t24_jrows; T9 gone), same value.
  Out of the repeats, midpoints and title counts. The T24 titles are unchanged (no note added, so the kept tables stay identical).
- Code: 96 top-level definitions that only fed the removed sheets deleted from tools/jupiter_tables.py (3,680 -> about 1,640 lines; found by a
  reachability scan from main()), e.g. write_t23, write_t21 / write_t22, write_t20, write_cross, write_t18, write_mids, runner_timeline,
  sky_equiv, write_t24hj / write_t24r / t24r_cell, write_t24ss / summary_sheet, threads / numbers / ratio / FIELD sheet writers, pairs_sheet,
  NUM_FAMILIES; write_pairs lost its THREADS / NUMBERS feeds; the runner timeline context (ctx.t) and the unused Ephem(ctx) are gone (the sky
  timelines use ctx.x, unchanged). Left as is: the runner sheet's row-2 note (it still names T10, T11, T17-T20) so the kept rows stay identical.
  chk_sjcol/check_sjcol.py (test 46's old checker) imports names that are gone; that check is retired.
- Compared with acf68341 (chk_trim/check_trim.py), Kelso 14:50 2022, Lingfield 14:35 2021, rebuilt Ascot 14:30 2012, default and --full: 0
  mismatches. Kelso: POSITIONS + SKY JUPITER 94,654 cells, runner blocks 334,080, five-row cells 2,592 (Lingfield 41,734 / 206,016 / 2,592; Ascot
  83,259 / 55,680 / 432). Columns BD-DB on runner sheets lose the widths only the removed tables set (51 columns, nothing in them now).
  Default = --full (sheet, comment, style and workbook XML identical).
- Sizes (tables default / --full + pairs -> tables): Kelso 4.99 / 5.20 + 2.95 -> 1.89 MB; Lingfield 2.47 / 2.68 + 2.85 -> 0.78 MB; rebuilt
  Ascot 1.05 / 1.11 + 0.49 -> 0.54 MB.
- Tests 145/145 (was 262: 110 check sites retired). Retired in place (comment '# retired 29 Oct 2026 (Eddie, workbook trim): ...'): 110 check sites - tests 2 (T14, RATIOS),
  4 (T16, FIELD 16), 5, 6 (T12 / T13 unisons, RATIOS, FIELD 12), 7 (T12 / T13), 8 (THREADS), 9 (NUMBERS, FIELD NUMBERS), 10 (T10 / T11, FIELD
  10 / 11), 11 / 12 (T17, FIELD 17), 13 (T18), 14 (T19, P## PAIRS), 15 (T11, THREADS, T15), 16 (T20), 17 (T21 / T22), 18 (T21 sky side), 21
  (T19 sky side), 22 (T19 together), 23 (T21R / T22R, FIELD 21R / 22R), 25 (TIMELINE H / J), 26 (LONG H / J, sky equivalents), 27 (T23), 32
  (T24 ratio tables), 34 / 36 (RATIOS cases), 35 (T24 H / J red), 37 (runner star events), 40 (T24 STAR SELECT removal), 44 ((SKY STARS) +
  summary), 46 (check_sjcol), 47 (summary display), 48 (sky hit move). Adapted (20): the T24 readers skip the five rows; tests 14, 15, 19, 22,
  23, 26, 28, 30, 34, 35, 36, 37, 38 keep their SKY JUPITER / T1 / T2 / T24 parts only; old-vs-old comparisons drop their pairs part; test 46's
  by-hand cells now read T24 HORSE itself (+ a layout check). Kept unchanged: POSITIONS, SKY JUPITER, T1-T8, T24 and families checks. Test 49
  (new): the comparison above in the suite (builds by acf68341's code), default = --full, no pairs workbook, Kelso P01 T24 HORSE five rows and
  Jupiter RA 167.634941 = d(S Jupiter, H Jupiter) from POSITIONS.
- Independent checker (29 Oct), own code (chk_trim/indep/), Kelso default and --full: sheets / column A (6,012 cells), POSITIONS + SKY
  JUPITER 94,654 cells, kept runner tables 336,168 cells after the shift, five rows: 2,256 distances recomputed from POSITIONS, 3,144 cells = the
  before (SKY STARS) rows, 2,256 fills, 48 Jupiter cells = T9, title counts; default = --full 445,438 cells: 0 mismatches; 16 planted errors all
  caught (also run on Lingfield and Ascot: 0 mismatches).
- Untracked reference/classic/*_pairs.xlsx files from earlier builds are left on disk (stale; not written any more).

## jupiter_tables: T24 HORSE / JOCKEY (SKY STARS), SKY STARS SUMMARY (Eddie, 27 Oct 2026; viewing only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): both (SKY STARS) tables and the SKY STARS SUMMARY sheet are gone. Text kept for reference.
- Selection (once per race; sky_star_select): every star of T1_T2_T24_STARS whose S Jupiter → S star cell in the SKY block (SKY JUPITER)
  scores in RA or Dec (any score: conjunction, whole, half, 4-digit hit, as on the sheet); bodies and the equator out; T24 (RA) order; a
  star in both planes once; a star missing from a chart skipped quietly. Selected stars are kept on ctx.skysel.
- Runner sheets, after T24 JOCKEY RATIOS: "T24 HORSE (SKY STARS)", then "T24 JOCKEY (SKY STARS)" (write_t24ss). Columns: table | star |
  sky hit ('RA 70 whole (88.36)', both planes joined '; ', a conjunction 'RA 0 conjunction (score)' - Claude's wording) | the T24 row
  copied from T24 HORSE / JOCKEY on the same sheet (every T24 column from C shifted right by one: values, fills incl. red, comments,
  midpoint cells, thick / dotted outlines, repeats; copy_cell, no recalculation) | SCORES RA, SCORES Dec (one per body, same order): the
  score in the value cell's comment (t24_score), 2 dp, filled as the value cell, blank where it has no score. Header rows = T24's plus
  'sky hit' and 'SCORES RA' / 'SCORES Dec' merged; widths: sky hit 36 (Claude's choice), values / scores 11, midpoints 40, repeats 60.
  Shared columns are only ever widened, so on runner sheets column C (sky hit) goes 11 -> 36 and AB (midpoints) 11 -> 40 for every table
  (e.g. T24's RA Sun and Dec Sun columns); display only. Title: what it is, the rule, 'Selected: n stars' (0 and no rows when none).
- Sheet "SKY STARS SUMMARY" (summary_sheet), after the runner sheets (default and --full; in --full after P## RATIOS / NUMBERS, before
  the FIELD sheets / THREADS): per runner in order its A1 line ('P01 1 Bravo Team / Sean Bowen'), T24 HORSE (SKY STARS), one blank row,
  T24 JOCKEY (SKY STARS), two blank rows; cells and merged headers copied from the runner sheets. Not in THREADS, NUMBERS, FIELD or timelines.
- Selected (sky hits): Kelso 14:50 4 May 2022 (batch copied into reference/classic from ~/astronomy-project/racecards/20220504_kelso;
  csv not copied) 14 = Eddie's list: Aldebaran RA 70 whole (88.36), Alhena Dec 18 whole (0.15), Castor Dec 33.5 half (0.56), Praesepe RA
  81×φ golden (36.04), Algorab RA 106×φ (76.48), Vindemiatrix RA 101×φ (56.39), Alkaid RA 94×φ (46.30), Unukalhai RA φ^10 phi power
  (73.34), Antares RA 69×φ (5.09), Ras Algethi RA 62×φ (57.00); Dec 16 whole (30.93), Acumen RA 90.5 half (0.37), Rukbat RA 68 whole
  (81.46); Dec 39 whole (49.76), Deneb Algedi Dec 14.5 half (1.93), Fomalhaut RA 9×φ (86.36); Dec 28 whole (83.46). Rebuilt Ascot
  14:30 2012 10: Rigel RA 19 (10.25), Adhara RA 45 (36.93), Castor RA 54 (97.57), Procyon Dec 14.5 half (85.64), Praesepe Dec 0
  conjunction (1.59), Algorab RA 79×φ (93.96), Vindemiatrix RA 84×φ (37.60), Alkaid RA 91×φ (71.65), Alphecca Dec 7 (45.04), Nunki Dec 46
  (0.47). Lingfield 14:35 2021 (21-star batch) 4: Pleiades Dec 38.5 half (18.07), Betelgeuse RA φ^10 (99.13), Spica RA 124.5 half (16.66),
  Deneb Algedi RA 0 conjunction (12.93).
- Rows per table (horse = jockey): Kelso 14 (6 runners; 38 rows inserted per runner sheet), Ascot 10, Lingfield 4 (6 runners). Summary
  rows: Kelso 228, Ascot 30, Lingfield 108. Sizes (default / --full) before -> after: Kelso 4.23 / 4.44 -> 4.77 / 4.99 MB, rebuilt Ascot
  0.94 / 1.00 -> 1.01 / 1.07, Lingfield 2.12 / 2.33 -> 2.29 / 2.51; pairs identical.
- Tests 245/245. Test 44 (new): chk_t24ss/check_t24ss.py vs builds by b19fac1f's code, three races, default and --full: every other row of
  every sheet identical (runner sheets minus the inserted tables; merged ranges shifted; no column narrowed), sheet order, selection = every
  scoring SKY-block star cell in T24 order, sky hit = the SKY block cells, every T24 cell = its T24 row, every SCORES cell = its comment's
  score (blank exactly where none) and fill, headers, summary = the runner tables cell for cell; pairs identical; Kelso = Eddie's 14; by
  hand from POSITIONS (Kelso P01): H Rukbat sky hit (S Jupiter 358.976662 / −1.620635, S Rukbat 290.974713 / −40.614744: RA 68.001949,
  Dec 38.994109), SCORES RA H Rukbat – H Gonggong 45.003699 whole 45 (66.43), SCORES Dec H Rukbat – H Sun 46.490268 half 46.5 (0.07),
  conjunction H Antares – H Mars RA 1.308631 (1.63) red. Changed for this: test 30 (default sheets + SKY STARS SUMMARY; the new tables and
  the summary allowed in the new-star leak check); tests 42 / 43 now compare with builds by b19fac1f's code.
- Independent checker (27 Oct), own code from POSITIONS (chk_t24ss/indep/), Kelso default and --full: selection (134 SKY cells, the 14,
  sky-hit texts), 8,568 copied cells vs T24, 8,064 value cells and 8,064 SCORES cells recomputed (fills light 366, green 122, yellow 111,
  red 56, blank 7,409), headers, summary (25,758 cells), before vs after (1,535,490 / 1,560,875 cells; 38 rows inserted per runner sheet),
  default = --full (48,108 cells): 0 mismatches; reported the column widths above. Not exercised in Kelso: a conjunction sky hit (Ascot and
  Lingfield have one each), a selected star missing from a chart.

## jupiter_tables: sky hit moved to the end of the (SKY STARS) tables, exact widths (Eddie, 27 Oct 2026; layout only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): the (SKY STARS) tables and the summary are gone. Text kept for reference.
- T24 HORSE / JOCKEY (SKY STARS) (runner sheets) and the SKY STARS SUMMARY: "sky hit" moved from column C to the last column, after SCORES
  Dec (DB with 24 bodies + S Jupiter); the copied T24 part sits in the same columns as T24 HORSE / JOCKEY (C onward: Ketu, S Jupiter, RA
  midpoints, Dec midpoints, repeats as in T24), SCORES RA / Dec right after the repeats column. Cells, fills, comments, outlines unchanged;
  merged headers moved to match; sky hit blank on the four Jupiter rows and the 'stars' row; the 'stars' grey runs A to the new last column.
- Widths ("never narrower" dropped; supersedes the display entry below): values, S Jupiter and SCORES 11, RA / Dec midpoints 40, repeats 60,
  sky hit 36, on runner sheets and the summary; runner-sheet AA, AZ, BA 11 (the T1 / T2 SKY RA timing text in AA shown at 11 again).
  Changed vs d2d4651b: runner sheets C 36 -> 11, AA 40 -> 11, AC 40 -> 11, AZ 40 -> 11, BA 60 -> 11, BB 60 -> 40, BD 60 -> 11, DB 11 -> 36;
  summary C 36 -> 11, AC 40 -> 11, BA 40 -> 11, BB 60 -> 40, BC 40 -> 60, BD 60 -> 11, DB 11 -> 36. Shared columns: the other tables on the
  runner sheets show at these widths too. Freeze panes unchanged (summary C3, runner sheets C4).
- Sizes (tables default / --full): Kelso 4.99 / 5.20 MB, Lingfield 2.47 / 2.68, rebuilt Ascot 1.05 / 1.11; pairs unchanged.
- Tests 262/262. Test 48 (new): chk_skyhit/check_skyhit.py vs builds by d2d4651b's code, Kelso, Lingfield, rebuilt Ascot, default and --full:
  every moved cell otherwise identical (sky hit cells Kelso 386, Lingfield 146, Ascot 50), every (SKY STARS) star row = its T24 row column
  for column (Kelso 168, Lingfield 48, Ascot 20), every T24 / (SKY STARS) / summary column at its width, AA / AZ / BA by name, freeze panes and
  every other row unchanged, pairs identical; Kelso P01 by name (C 'Sun', H Rukbat sky hit in DB). Test 47 now compares a2d20618 with builds
  by d2d4651b's code; test 46 stays on a2d20618 builds; test 44 compares b19fac1f with f1327932 builds (neither the current code).
- Independent checker (27 Oct), own code (chk_skyhit/indep/), Kelso default and --full: 59,400 moved table cells, 9,072 star-row + 1,296
  header cells = T24, summary 30,624 cells, every other row (320,796 / 338,083 cells), pairs, widths (3,132 checks), freeze panes: 0
  mismatches; 10 planted errors all found.

## jupiter_tables: summary header rows, grey 'stars' rows, widths (Eddie, 27 Oct 2026; display only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): the summary and the (SKY STARS) tables are gone. Text kept for reference.
- SKY STARS SUMMARY: rows 1-2 = a copy of the first table's two header rows (values, styles, merges); everything else two rows lower;
  freeze panes C3 (summary only; runner sheets C4 as before).
- Every 'stars' separator row of T24 HORSE / JOCKEY (SKY STARS) (runner sheets and summary): light grey D9D9D9 from column A to the last
  SCORES column.
- Widths: no column narrower than before a2d20618 (the T24 / (SKY STARS) widths of the layout without the S Jupiter column are kept too,
  widest wins): runner sheets AA 11 -> 40, AZ 11 -> 40, BA 11 -> 60, BB 40 -> 60; summary AB 11 -> 40, BA 11 -> 40, BB 11 -> 60 (all wider
  than their content needs, from the old layout). (Superseded the same day: see the sky hit entry.)
- Sizes (tables default / --full): Kelso 4.99 / 5.21 MB, Lingfield 2.47 / 2.68, rebuilt Ascot 1.05 / 1.11; pairs unchanged.
- Tests 260/260. Test 47 (new): chk_display/check_display.py vs builds by a2d20618's code (widths also vs 35255b16), three races, default and
  --full: summary rows 1-2 = the header rows below, freeze C3 on the summary only, every 'stars' row grey A to the last SCORES column
  (Kelso 24 rows, 2,544 cells), no column narrower, midpoints >= 40, repeats >= 60, values >= 11, every other cell identical (summary after
  the shift), pairs identical. Test 46 now compares 35255b16 with builds by a2d20618's code.
- Independent checker (27 Oct), own code (chk_display/indep/), Kelso default and --full: 353,472 / 370,957 cells, 0 mismatches; 7 planted
  errors all found; every width change listed above, each = the 35255b16 width.

## jupiter_tables: T24 "S Jupiter" column, four Jupiter rows on the (SKY STARS) tables (Eddie, 27 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): the S Jupiter column stays; the (SKY STARS) tables and the summary are gone, and the four Jupiter rows (+ "stars") now sit on top of T24 HORSE / JOCKEY themselves, the Jupiter cell computed directly (T9 gone). Text kept for reference.
- T24 HORSE / T24 JOCKEY (every runner sheet), every star row: column "S Jupiter" straight after Ketu in the RA body columns (before "RA
  midpoints") and after Ketu in the Dec body columns (before "Dec midpoints"); cell = d(S Jupiter, S star) at the off = the SKY block value
  (ctx.skycells), T24 cell format (6 dp, best-family fill, red inside the conjunction range, comment 'target · family · offset · score' or the
  nearest target). Not in the repeats or the midpoints (Claude's default). Header "S Jupiter" under RA / Dec (merged over bodies + S Jupiter),
  width 11; every column after it shifts right by one. The T24 HORSE / JOCKEY titles carry a one-line note (T24SJ_NOTE). T24 SKY, T24 H / J,
  T24 RATIOS unchanged.
- T24 HORSE / JOCKEY (SKY STARS) and the SKY STARS SUMMARY: the same column in the copied T24 part and in SCORES RA / SCORES Dec (after Ketu).
  Four rows on top of each table (t24ss_jrows, values taken from the tables on the sheet): 'S Jupiter → S body' (the T1 / T2 SKY cells),
  'H Jupiter → H body' (T1) / 'J Jupiter → J body' (T2), 'S Jupiter → H body' (T5) / J (T6), 'S body → H Jupiter' (T7) / J (T8); one cell per
  T24 body column (Sun ... Ketu, Jupiter), T24 cell format, SCORES as the star rows; Jupiter column blank on the first two rows, d(S Jupiter,
  natal Jupiter) (T9) on the last two; sky hit, midpoints, repeats and S Jupiter blank on them; then a separator row 'stars' (Claude's
  default), then the star rows as before. Title note T24SS_JNOTE.
- Display: the T24 midpoint / repeats columns moved right, so runner-sheet columns AA (40 -> 11), AZ (40 -> 11) and BA (60 -> 11) are now
  narrower (AB, AC, BB 40; BC, BD 60); AA also holds the T1 / T2 SKY RA timing text, now shown at width 11. Display only.
- Sizes (tables default / --full; pairs unchanged) before -> after: Kelso 14:50 2022 4.77 / 4.99 -> 4.98 / 5.19 MB, Lingfield 14:35 2021
  2.29 / 2.51 -> 2.45 / 2.66 MB, rebuilt Ascot 14:30 2012 1.01 / 1.07 -> 1.05 / 1.11 MB.
- Tests 258/258. Test 46 (new): chk_sjcol/check_sjcol.py vs builds by 35255b16's code, Kelso, Lingfield, rebuilt Ascot, default and --full:
  every S Jupiter cell = the SKY block cell (value, target, offset, score, fill, red) in its place (Kelso 1,608, Ascot 268, Lingfield 504);
  every cell of the four rows = T1 / T2 SKY cells, T1 / T2, T5–T8, T9 (Kelso 2,256, Ascot 376, Lingfield 2,256), blanks as stated; SCORES =
  the comments; summary = the runner tables; every other row identical apart from the column shift and the two title notes; merged ranges as
  the layout; pairs identical; by hand from POSITIONS (Kelso P01): S Jupiter column H Aldebaran RA 69.998800 70 whole (88.36), H Fomalhaut Dec
  28.001728 28 whole (83.46); S Jupiter → S Venus Dec 1.012418 1 whole (14.37); H Jupiter → H Uranus RA 147.997469 148 whole (76.29), Dec
  0.078710 conjunction (54.41) red; S Jupiter → H Gonggong RA 23.001896 23 whole (81.94), H Venus RA 0.045495 conjunction (94.03) red; S Rahu
  → H Jupiter Dec 10.995637 11 whole (61.13); Jupiter column 167.634941 = d(S Jupiter, H Jupiter). Changed for this: the T24 grid reader
  (tests 28 ...) skips the S Jupiter column; test 29's header check expects it; test 45 now compares f1327932 with builds by 35255b16's code.
- Independent checker (27 Oct), own code from POSITIONS (chk_sjcol/indep/), Kelso default and --full: 1,608 S Jupiter cells (= SKY block),
  2,256 four-row cells (= T1 / T2 552, SKY cells 552, T5 / T6 552, T7 / T8 552, T9 48), 336 blanks, SCORES 10,656, summary 28,776 cells,
  before vs after 1,645,274 / 1,679,421 cells (only the 36 title notes differ), pairs identical, default = --full: 0 mismatches. Not
  exercised in Kelso: a red S Jupiter column cell (Ascot Praesepe Dec and Lingfield Deneb Algedi RA are red; covered by test 46).

## jupiter_tables: T24 repeats flag (Eddie, 22 Oct 2026; viewing / display only)
- T24 SKY (SKY JUPITER), T24 HORSE and T24 JOCKEY (every runner sheet), each star row: a scoring value = the cell's best target (as its
  comment: family + target number), inside tolerance, any score; conjunction cells (RA < 1.5 / Dec < 0.3, red) left out; only the best
  target counts (Claude's default). A repeat = the same target (same family and target number, no x10 / /10 folding) in two or more body
  cells of the row, any planes. New column "repeats" after "Dec midpoints" (width 60, wrap): every repeated target, most cells first, then by
  the highest score among its cells; text '<target> <family> ×n (<body> <plane> (score), ...)' joined with '; ' (family as in the comments:
  whole, golden, phi power, ninth, sqrt2, silver). Inside a target the cells by score, highest first (ties RA before Dec, body order) -
  Claude's choice. Each repeated cell: dotted outline (DOTTED; a midpoint thick outline kept) and a comment line "repeat: <target> <family>
  ×n (with <other cells>)". Title: T24_NOTE + '. REPEATS (22 Oct 2026): k of N rows with a repeat, m repeated targets'. Values, fills (red
  incl.), existing comments, midpoint columns and outlines, T24 H / J, T24 RATIOS and every other block unchanged.
- Rows with a repeat / rows, repeated targets, largest ×n: rebuilt Ascot 14:30 2012 SKY 24 / 67, 27, ×3 (S Mirach 10×φ^3 phi power); P01
  HORSE 20 / 67, 25, ×3 (H Castor ninth 144.444); JOCKEY 27 / 67, 29, ×3 (J Arcturus silver 41.4). Lingfield 14:35 2021 (21 rows) SKY 8, 8,
  ×2; HORSE / JOCKEY P01 4, 4, ×2 / 7, 7, ×2; P03 10, 14, ×2 / 6, 6, ×3; P05 6, 8, ×2 / 9, 11, ×3; P07 3, 3, ×2 / 13, 15, ×3; P09 9, 10, ×2 /
  7, 7, ×3; P11 8, 9, ×3 / 6, 6, ×2. Sizes (default / --full; pairs unchanged): rebuilt Ascot 0.97 / 1.03 -> 0.98 / 1.04 MB; Lingfield
  2.16 / 2.38 -> 2.17 / 2.39 MB.
- Tests 235/235. Test 41 (new): chk_t24rep/check_rep.py vs the build before (commit 5e10f7bf), both races default and --full: every repeats
  cell recomputed from POSITIONS (own code, families.evaluate), dotted outlines exactly on repeated cells (thick kept), comments = before +
  the repeat lines, titles, every other cell of every sheet identical: 0 mismatches; by hand from POSITIONS (rebuilt Ascot P01): RA–Dec
  T24 HORSE H Menkent silver 24.14 ×2 (Makemake RA 24.137213 (92.01), Rahu Dec 24.066157 (13.73)); Dec–Dec T24 JOCKEY J Orion Nebula Cluster
  ninth 16.6667 ×2 (Uranus Dec 16.673056 (94.52), Gonggong Dec 16.652082 (87.50)); midpoint + repeat T24 HORSE H Castor RA ninth 144.444 ×3
  (Quaoar 144.616864 (81.74), Rahu 143.857791 (37.88), Vesta 143.549007 (5.19); Quaoar and Rahu thick kept with both comment lines, Vesta
  dotted). Changed for this: test 28's T24 grid reader stops at the repeats column; tests 39 / 40 compare on builds by 5e10f7bf's code.
  Independent checker (22 Oct), own code from POSITIONS (chk_t24rep/check_rep_indep.py), rebuilt Ascot default and --full: every repeats
  cell, outlines, comment lines, titles, header / width / wrap, every other cell of every sheet (323,818 / 328,853 cells), 5 scores by
  hand: 0 mismatches. Not exercised: a tie in target order.

## jupiter_tables: sky star timelines trimmed, 95 / 100 / 95 times, T24 STAR SELECT (Eddie, 22 Oct 2026; viewing only)
Note 29 Oct 2026 (workbook trim): the sky STAR / LONG STAR TIMELINE stay; T24 STAR SELECT was already removed 22 Oct. Text kept for reference.
- T24 STAR SELECT REMOVED (Eddie, 22 Oct 2026, the same day; no reason given): the runner sheets no longer carry it (write_t24sel,
  star_select, SEL_NOTE and t24r_cell's tags parameter gone; t24r_cell = its 19 Oct form). The trimmed sky STAR / LONG STAR TIMELINE and the
  95 / 100 / 95 columns stay. Compared with the build before (commit 0ad7d2e5; chk_rmsel/compare_rmsel.py), both races default and --full:
  each runner sheet = before minus exactly the SELECT region (rebuilt Ascot P01 28 tables, 372 rows; Lingfield 2 tables, 22 rows per
  runner), every other row of every sheet identical (values, fills, comments, borders, number formats; merged ranges shifted), pairs
  identical; columns BA onward lose the width 11 only SELECT set (back to the layout before it). Sizes (default / --full): rebuilt Ascot
  3.02 / 3.08 -> 0.97 / 1.03 MB, Lingfield 2.88 / 3.10 -> 2.16 / 2.38 MB. Tests 231/231: test 39 keeps (a) dropped events, (b) the 95
  crossings, (d) every other row; (c) is now "no T24 STAR SELECT anywhere"; test 40 new (the comparison above, code gone). Independent checker
  (22 Oct), own code (chk_rmsel/check_rmsel_indep.py), both races default and --full: 0 mismatches. The text below describes the tables as
  they were built.
- SKY JUPITER STAR TIMELINE and LONG STAR TIMELINE: only events centred on S Jupiter (sj_event: 'S Jupiter → S star' RA / Dec and
  'S Jupiter: S A – S B' ratio / midpoint); star-to-star distances (the d(A, B) leg of a pair row) dropped. Runner timelines, sky TIMELINE /
  LONG TIMELINE unchanged. Dropped: rebuilt Ascot 14:30 2012 LONG STAR 59 -> 45 (14: S Aculeus – S Rukbat RA 16×φ 99.87, S Antares – S Alphard
  Dec ninth 17.7778 96.89, S Rigel – S Alnilam Dec 7 95.94, S Acubens – S Facies RA ninth 144.444 95.42, S Altair – S Sadalsuud Dec ninth 14.4444
  95.32, S Sirius – S Acubens RA ninth 33.3333 93.81, S Procyon – S Facies Dec 18×φ 91.74, S Zosma – S Markab RA ninth 177.778 91.18, S Zosma –
  S Sualocin RA 141.4 90.63, S Betelgeuse – S Nunki Equator ninth 18.8889 99.72, S Fomalhaut – S Algenib RA ninth 18.8889 97.11, S Deneb Algedi –
  S Phact Dec φ^6 93.98, S Mirach – S Zubeneschamali Dec 45 93.42, S Fomalhaut – S Alkes RA 10×φ^6 92.94), STAR 65 -> 65 (none in the window);
  Lingfield 14:35 2021 LONG STAR 3 -> 2 (S Sirius – S Rigel RA 14×φ 92.35), STAR 3 -> 3.
- Three new columns on both blocks (W95_HEAD; win95 / score_at): "> 95 since", "100" (the exact time as before), "< 95 from": the event's
  own score (distance / ratio on its family and target, own tolerance; midpoint total, RA side fixed at the off) from the engine (race site,
  sky at m = workbook value at the off + engine(m) − engine(off)); from the exact time (the off when not within 1 year) step outward on the
  grid of the LONG search (10 min for a day, then 1 h, up to 1 year), first minute under 95, bisect to the minute; "not within 1 year";
  "—" = under 95 at the exact time. Format as the linear-estimate column ('hh:mm (±n.n min)', dates and days beyond a day). E.g. Ascot
  S Jupiter → S Castor RA 54 (whole): 14:28 (−1.7) / 14:31 (+1.5) / 14:34 (+4.4); S Orion Nebula Cluster – S Phact Equator midpoint 91.95:
  16:37 (+127.8) / 20:02 (+332.2) / 23:25 (+535.3). No "—" or "not within 1 year" in these two races.
- T24 STAR SELECT (write_t24sel, star_select; runner sheets after T24 JOCKEY RATIOS): selection from the trimmed sky STAR TIMELINE and LONG
  STAR TIMELINE together (an event in both once): singles = S Jupiter → S star with score at the off > 90 (one table per star), pairs =
  S Jupiter: S A – S B ratio / midpoint > 95 (one table per pair); singles in RA order, then pairs (RA order of the first, then second star).
  Title lists each selecting event (timeline(s), relationship, plane, kind, target, score, exact time). Columns: the 24 natal T24 bodies RA,
  then Dec (as T24 HORSE, no midpoint columns), then 276 RA pairs and 276 Dec pairs 'X / Y' (Jupiter and the own Rahu – Ketu included).
  Rows: single H <star>, J <star> (T24 row cells + pair cells d(star, X) / d(star, Y)), H / J <star> (d(H star, H X) / d(J star, J X), pair
  columns blank); pair H A, H B, H A / B, blank, J A, J B, J A / B, blank, H / J A, H / J B. Ratio cells as T24 RATIOS (t24r_cell, tags off:
  no automatic / assisted - Claude's default, Eddie to say if wanted); 'together' when a leg is under RA 1.5 / Dec 0.3. Natal, fixed.
  Selected, rebuilt Ascot (28 tables): singles Meissa RA 24.14 silver 90.61, Castor RA 54 97.57, Algorab RA 79×φ 93.96; pairs Deneb Algedi –
  Ankaa RA 7/4 95.34, Mirach – Murzim Equator 9 98.41, Betelgeuse – Al Rescha RA 1 96.18, Al Rescha – Adhara Equator 11/6 95.84, Menkar –
  Praesepe RA 5 95.88, Algol – Sadalsuud Equator 3/2 97.45, Mirfak – Orion Nebula Cluster Dec 6/5 99.94, Mirfak – Acumen Equator 2 96.08,
  Pleiades – Vindemiatrix Dec 2 98.48, Pleiades – Diadem Dec 2 98.64, Pleiades – Nunki Equator 3/2 95.80, Capella – Orion Nebula Cluster
  Equator 11/6 98.40, Bellatrix – Scheat Dec 8/5 95.15, Orion Nebula Cluster – Murzim Dec 3/2 96.71, Murzim – Zosma Equator 11/5 95.33,
  Vega – Castor RA 13/5 99.31, Regulus – Zubeneschamali Equator 4/3 99.08, Vega – Alkes RA 4/3 98.57, Denebola – Unukalhai RA 3/2 99.91,
  Vindemiatrix – Zubenelgenubi RA 6/5 98.34, Unukalhai – Sadalmelik RA 2 95.33, Ras Algethi – Kaus Australis Equator 11/4 98.30, Galactic
  Centre – Rukbat Equator 9/4 99.64, Facies – Deneb Dec 1+1/√2 96.78, Vega – Nunki Dec 1+√2 99.13 (P01: 237 rows). Lingfield (2 tables per
  runner, 13 rows): Betelgeuse RA φ^10 99.13; Alkaid – Betelgeuse Equator 5 98.80.
- Sizes (tables default / --full; pairs unchanged): rebuilt Ascot 0.97 / 1.03 -> 3.02 / 3.08 MB; Lingfield 2.16 / 2.38 -> 2.88 / 3.10 MB.
- Compared with the build before (commit 00b6db9e; chk_select/compare_sel.py), both races default and --full: sky STAR / LONG STAR = before
  minus exactly the dropped events above, old cells identical, header + the three new names; every other row identical; 0 mismatches.
- Tests 234/234 (test 39 new): compare_sel as above; every 95 cell of both races re-searched (own score code, engine; >= 95 one minute inside,
  < 95 one minute outside); T24 STAR SELECT selection = the rule, headers (24 + 24, 276 + 276), row labels and blank rows, every body cell =
  the T24 cell, every ratio recomputed from POSITIONS (value, interval, score, fill, together), ratio rows' pair columns blank, both races
  every runner; by hand: S Castor H Castor RA Pluto / Eris 1.750159 7/4 B (88.22), H / J Castor RA Sedna 1.166799 7/6 (85.48), H Mirfak /
  Orion Nebula Cluster RA Sun, together H Mirfak / Orion Nebula Cluster RA Mars (d(H Orion Nebula Cluster, H Mars) 0.333693), the 95
  crossings of S Jupiter → S Castor RA 54 (|d − 54| = 0.000506). Changed for this: test 38 compares 632447ff with builds by 00b6db9e's code; test 30's leak check allows T24 STAR SELECT; test 37's sky STAR
  TIMELINE check uses the S Jupiter rule and the first 12 cells; a 95 cell shown in days is checked at ±8 min (0.01 day).
  Independent checker (22 Oct), own code from POSITIONS + engine (chk_select/check_sel_*.py), both races: (a) dropped events exactly as above
  (Ascot LONG STAR separating 28 -> 19, applying 31 -> 26), old cells identical; (b) all 230 95-crossings of 115 rows re-searched (largest
  difference 0.39 min; day-format cells to 0.01 day); (c) selection = the rule (left out correctly e.g. Vindemiatrix – Diadem 94.30,
  S Jupiter → Alkaid 71.65), layout and merged ranges, 6,816 body cells and 84,768 ratio cells (together 1,743, hit 10,623, outside
  72,402); (d) every other row identical, default = --full: 0 mismatches. Not exercised: "—" and "not within 1 year" cells; pair-table
  order (RA order of the earlier star, then the other) is Claude's choice.

## jupiter_tables: LONG STAR TIMELINE (Eddie, 22 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): the sky LONG STAR TIMELINE stays; LONG STAR TIMELINE H / J are gone. Text kept for reference.
- SKY JUPITER "LONG STAR TIMELINE" straight after STAR TIMELINE, and on each runner sheet "LONG STAR TIMELINE H" / "LONG STAR TIMELINE J"
  straight after STAR TIMELINE H / J: the LONG TIMELINE (H / J) rows between Jupiter and stars only (star_event, as STAR TIMELINE), the same
  cells (score >= 90, real engine time beyond 60 min, linear estimate, "from the off" text, "also", sky-equivalent columns and "H + J" on
  runners), SEPARATING / APPLYING sections, sort and title counts as LONG TIMELINE (write_long on the filtered events). Every other block
  unchanged.
- Events (separating / applying): rebuilt Ascot 14:30 2012 sky 59 (28 / 31); P01 H 45 (21 / 24), J 44 (21 / 23). Lingfield 14:35 2021 sky 3
  (0 / 3); P01 H 3 (1 / 2), J 3 (0 / 3); P03 H 3 (1 / 2), J 4 (1 / 3); P05 H 4 (2 / 2), J 3 (1 / 2); P07 H 4 (3 / 1), J 3 (1 / 2); P09 H 3
  (2 / 1), J 3 (1 / 2); P11 H 4 (1 / 3), J 2 (1 / 1). No empty block in these two races (the 0-event title is not exercised).
- Sizes (tables default / --full): rebuilt Ascot 0.95 / 1.01 -> 0.97 / 1.03 MB; Lingfield 2.15 / 2.37 -> 2.16 / 2.38 MB; pairs unchanged.
- Tests 225/225 (test 38 new): chk_longstar/check_longstar.py vs the build before (commit 632447ff), both races --full: each LONG STAR block =
  the Jupiter–star rows of its LONG block (own star test; cells and fills, order, sections, counts, title, >= 90), every other row of every
  sheet identical; counts as above; own sort check (shown scores never rise; sections). Changed for this: test 30's leak check allows the
  LONG STAR blocks; test 37 now compares 18aff98a with builds by 632447ff's code, test 38 compares those with now.
  Independent checker (22 Oct), own code (chk_longstar/check_longstar_indep.py), both races default and --full: each LONG STAR block = the
  Jupiter–star rows of its LONG block (cells, fills, comments, order), sections, counts, titles, >= 90, placement (sky after STAR TIMELINE;
  runners STAR H, STAR J, LONG STAR H, LONG STAR J), every other row identical, default = --full: 0 mismatches. Note: two pairs show the same
  2-dp score in reverse time order, as in LONG TIMELINE (unrounded order: Ascot sky S Unukalhai – S Sadalmelik RA 95.3332 before S Murzim –
  S Zosma Equator 95.3325; P01 J S Zubeneschamali → J Jupiter 96.6985 before J Orion Nebula Cluster – J Murzim Dec 96.6972) - the sort is
  on the unrounded score; test 38's own sort check reads the shown scores only.

## jupiter_tables: all 67 stars in every timeline, STAR TIMELINE, LONG >= 90 (Eddie, 22 Oct 2026; viewing only)
PARTLY REMOVED 29 Oct 2026 (Eddie, workbook trim): the sky TIMELINE, STAR TIMELINE and LONG >= 90 stay; the runner TIMELINE H / J, LONG H / J and STAR TIMELINE H / J are gone. Text kept for reference.
- Runner TIMELINE H / J and LONG TIMELINE H / J take star events for the 67 stars (T1_T2_T24_STARS), off-sheet, after every table source
  (runner_timeline(..., stars=...); an event a table source already has keeps its name, the star source goes in "also"), in this order:
  "S Jup→star" (S Jupiter → natal star, RA / Dec, best hit or nearest target, as T5 / T6), "star→Jup" (sky star → natal Jupiter, as T7 / T8),
  "S Jup on star pair" (S Jupiter on two natal stars of one chart, RA / Dec / Equator, rows passing the T19 filter: ratio, midpoint, legs
  with a family hit) and "star apex" (T22 for every star). Same rules, dedupe, timing (linear; LONG real engine time beyond 60 min), "H + J"
  and sky-equivalent cells. The runner timelines run on a timeline context ctx.t / Rt holding STARS (Polaris incl.) and the 67, so every
  earlier event keeps its cells. T22 on the sheet stays on its 23 stars; T19 has no star–star rows (so no "royal – royal" T19 events).
- STAR TIMELINE (SKY JUPITER, after LONG TIMELINE) and STAR TIMELINE H / J (runner sheets, after LONG TIMELINE J): the TIMELINE /
  TIMELINE H / J rows between Jupiter and stars only (star_event: every point a Jupiter or a star, at least one star), same cells, window,
  markers (and sky-equivalent cells on runners). Sky: SKY block star rows, SKY STARS, SKY ROYAL royal – royal (and any pair-block leg
  S Jupiter → star); runners: the four star sources, T22, T19 legs S Jupiter → royal star.
- LONG_MIN 80 -> 90 (Eddie, 22 Oct 2026): every LONG TIMELINE (sky and H / J) keeps events scoring >= 90 at the off. A side effect of the
  dedupe (rule unchanged): where a ratio event under 90 and a midpoint event >= 90 share a key, the midpoint now shows (rebuilt Ascot sky:
  S Jupiter: S Orion Nebula Cluster – S Phact Equator midpoint 91.95, real 20:02; before, the unison ratio 86.16 held the key; Lingfield
  P07 LONG H T19 S Jupiter: H Eris – H Antares Dec midpoint 91.21, +255.9 min, ratio 82.73 before).
- Events (TIMELINE: total (before / first 5 min / after)), before -> after:
  Rebuilt Ascot 14:30 2012: sky TIMELINE 90 (29/7/54) unchanged, STAR TIMELINE 65 (23/6/36); P01 TIMELINE H 13 (4/1/8) -> 68 (21/6/41),
  J 11 (1/0/10) -> 63 (16/4/43); STAR TIMELINE H 57 (18/5/34), J 52 (15/4/33). New runner events by source: H S Jup on star pair 50,
  S Jup→star 3, star apex 2; J S Jup on star pair 49, S Jup→star 3.
  Lingfield 14:35 2021 (21 stars): sky TIMELINE 48 unchanged, STAR TIMELINE 3; TIMELINE H / J P01 18 -> 20 / 11 -> 16, P03 13 -> 16 / 13 -> 18,
  P05 14 -> 16 / 12 -> 17, P07 13 -> 17 / 11 -> 15, P09 27 -> 30 / 14 -> 19, P11 18 -> 20 / 15 -> 19; STAR TIMELINE H / J P01 2 / 5,
  P03 4 / 6, P05 3 / 5, P07 5 / 4, P09 3 / 5, P11 2 / 5.
- LONG (events; real-searched = linear beyond 60 min; not within 1 year): before (>= 80, no star sources) | after at >= 80 (scratch build) |
  after at >= 90 (the sheet):
  Rebuilt Ascot sky 126 (72; 13) | 126 (72; 13) | 69 (32; 8); P01 H 17 (8; 1) | 96 (40; 2) | 50 (15; 2); J 23 (17; 0) | 102 (58; 0) | 49 (22; 0).
  Lingfield sky 25 (13; 1) | 25 | 13 (6; 1); P01 H 24 | 28 | 13, J 18 | 21 | 11; P03 H 14 | 17 | 10, J 22 | 28 | 12; P05 H 19 | 23 | 13,
  J 20 | 24 | 10; P07 H 19 | 22 | 13, J 19 | 24 | 10; P09 H 23 | 28 | 12, J 26 | 31 | 9; P11 H 19 | 23 | 14, J 19 | 22 | 12.
- Sizes (tables default / --full; pairs unchanged): rebuilt Ascot 0.91 / 0.97 -> 0.95 / 1.01 MB; Lingfield 2.15 / 2.37 MB (+0.001).
- Compared with the build before (commit 18aff98a; chk_startl/compare_tl.py), both races default and --full: every row outside the
  timelines identical; every earlier TIMELINE / TIMELINE H / J event kept with the same cells, every earlier LONG event scoring >= 90 kept;
  only "also" gained a star source (e.g. Lingfield P01 LONG H T22 S Antares → H Jupiter Dec: 'also star→Jup, star apex').
- Tests 223/223 (test 37 new): compare_tl vs 18aff98a; every star event of TIMELINE H / J and LONG TIMELINE H / J recomputed from POSITIONS
  (own code, families.py targets): none missing or extra, value, score, minutes, source / also, both races every runner; Ascot LONG star
  events: real times cross within ±1 min (engine), "not within 1 year" by a daily scan; STAR TIMELINE (sky, H / J) = the matching TIMELINE
  rows (own Jupiter–star test); every LONG row >= 90; by hand from POSITIONS (Ascot P01): S Jup→star J Meissa RA 24.144132 silver 24.14
  (96.72) +12.5 min, J Al Rescha RA 29.125827 18×φ (92.63) −7.6; star→Jup S Murzim → J Jupiter RA 179.438581 10×φ^6 (99.08) real −68.62
  days, S Pollux → H Jupiter RA 166.685207 ninth (98.41) not within 1 year; S Jup on star pair J Mirach – J Menkar RA 3.000009 (99.91)
  +0.4, H Pleiades – H Nunki Equator 1.499964 3/2 (99.64) +10.3; star apex Nunki / H Jupiter Equator 1.87522 15/8 (84.94) +24.9,
  Sadalsuud / J Jupiter Dec 1.414289 √2 (92.99) −43.7. Changed for this: the LONG P05 S Betelgeuse case (86.51) now checks it is gone
  (< 90); test 30's leak check allows STAR TIMELINE and the runner timelines; test 33 handles a midpoint-kind sky event.
  Independent checker (22 Oct), own code from POSITIONS + engine (chk_startl/check_tl_*.py): rebuilt Ascot P01 every star-source event of
  TIMELINE H / J and LONG H / J (68 / 50 / 63 / 49 rows; 55 / 42 / 52 / 43 from star sources; pair rows kept by the T19 filter H 657, J 678;
  every midpoint hit merged into a unison ratio event) and Lingfield all 6 runners: none missing or extra, every cell; 30 LONG real times
  within 1 min (largest 0.3), 1 not within 1 year (hourly scan); STAR TIMELINE blocks = the matching TIMELINE rows, both races, default and
  --full; before vs after as above; every sky-equivalent cell of the 192 Ascot and 67 Lingfield star events: 0 mismatches. Cosmetic note:
  on the Lingfield P07 Eris – Antares midpoint row the sky-equivalent relationship reads 'S Jupiter: S Eris = S Antares' (midpoint notation)
  while its sky cells show the unison ratio 1.078941, outside (sky_equiv shows the ratio when the sky midpoint is not a hit; as before).

## jupiter_tables: 20 more stars and the Orion Nebula Cluster, 67 in T1, T2, T24 and the sky star tables (Eddie, 21 Oct 2026; viewing only)
- Engine: BEHENIAN_STARS + Ankaa, Al Rescha ('Alrescha'), Mirfak, El Nath ('Elnath'), Meissa, Alnilam, Murzim ('Mirzam'), Alhena, Acubens,
  Alphard, Alkes, Zosma, Vindemiatrix, Diadem, Ras Algethi ('Rasalgethi'), Aculeus (M6), Acumen (M7), Facies (M22), Rukbat, Sualocin (each one
  sefstars.txt line) and the Orion Nebula Cluster ('Orion Nebula', M42; 'Messier 42' a duplicate line, 'Trapezium' = θ¹ Ori not used)
  (rebuild_kit copy = ~/astronomy-project copy). J2000 at J2000.0 vs catalogue all within 0.02° (largest Rukbat dRA −0.0078, Acumen −0.0073;
  Orion Nebula Cluster 83.827615 / −5.391674, +0.0056 / −0.0007); Mirfak Dec +49.864180 (<= 50). Script chk_stars67/engine_check.py.
  Built as one change (the Orion Nebula Cluster came before the 20 were committed).
- T1_T2_T24_STARS = 67 (|Dec| <= 50, no Polaris), engine RA order = Eddie's list exactly; closest pairs Meissa 83.7901 / Orion Nebula
  Cluster 83.8276 / Alnilam 84.0589, Facies 279.0934 / Vega 279.2274, Bellatrix 81.2882 / El Nath 81.5792. NEW_STARS = 13 + 11 + 21. The 21 go
  exactly where the 46 are used (T1 / T2 + SKY cells, T24 SKY / HORSE / JOCKEY + midpoints + red fill, T24 H / J, T24 RATIOS, SKY block,
  SKY STARS (orientation unchanged rule: old STARS order without Polaris, then the new stars in RA order), sky TIMELINE / LONG TIMELINE);
  POSITIONS block lists all 45. No code change beyond the lists.
- Compared with the build before (commit ad0defaf; chk_stars67/compare_67.py): every row not naming one of the 21 identical, row for row
  (values, fills, comments) in both races, default and --full; only count titles differ; pairs identical; Lingfield 14:35 2021 (old batch)
  unchanged apart from the SKY STARS title ('46' -> '67'). Rebuilt Ascot 14:30 2012 batch = the 46-star batch + 21 '_B' rows (TRANS, P01,
  P02; NATAL_HOURLY + 1,050). New-star rows: POSITIONS 63; SKY JUPITER SKY 21, SKY STARS 347, T24 21, TIMELINE 40, LONG TIMELINE 59; P01 T1 21,
  T2 21, T24 42, T24 H / J 21, T24 HORSE / JOCKEY RATIOS 21 each.
- Rebuilt Ascot before -> after: SKY STARS (A / φ and √2 / B / no ratio or midpoint hit) 140/24/123/25 -> 289/58/266/46 (2,211 pairs, 5,930 pair-planes, 52 together, 659 listed; 312 old rows identical);
  TIMELINE 50 (12/4/34) -> 90 (29/7/54); LONG TIMELINE 67 (33/34; 39 real-searched; 7 not within 1 year) -> 126 (61/65; 72; 13);
  T24 H / J (A / φ√2 / B) 22/0/3 -> 32/0/5, HORSE RATIOS 91/24/119 -> 135/35/169, JOCKEY RATIOS 100/21/100 -> 153/25/147; assisted 29 -> 43
  (H / J 30, HORSE 2, JOCKEY 11; no automatic); red cells SKY 20 -> 26, HORSE 16 -> 25, JOCKEY 13 -> 22, H / J 2 -> 2; T24 midpoint hits on
  the new-star rows SKY 62, HORSE 51, JOCKEY 54.
- Orion Nebula Cluster in SKY STARS: with Meissa, Alnilam, Phact every RA pair is together (d 0.037663 / 0.231326 / 1.089043), left out; listed
  only S Orion Nebula Cluster – S Alnilam Dec 6/5 1.200205 (78.49) and S Orion Nebula Cluster – S Phact Equator unison 1.001436 (86.16) and midpoint hit (total 91.95; area A);
  S Meissa – S Orion Nebula Cluster Dec 2.565654 and Equator 1.464108 on no interval. T24 HORSE H Orion Nebula Cluster – H Mars RA 0.333693 red.
- Sizes (tables default / --full; pairs): rebuilt Ascot 0.69 / 0.76 -> 0.91 / 0.97 MB, pairs 0.51 unchanged; Lingfield 2.15 / 2.37 MB unchanged.
- Tests 210/210 (test 36 new): engine catalogue, sefstars names, Mirfak; the 67 = engine order = Eddie's list; the 67 / 21 in order in every
  table above; vs ad0defaf (compare_67.py) as above; TIMELINE / LONG TIMELINE counts; by hand from POSITIONS: T1 H Acumen Dec 12.001827 12
  (82.57), H El Nath RA 158.570201 98×φ (83.05); T2 J Murzim RA 179.445573 10×φ^6 (99.36), SKY cell S El Nath Dec 8.884166 ninth 8.88889
  (66.00); T24 JOCKEY J Facies – J Neptune Dec 1.616795 φ (92.49); T24 JOCKEY RATIOS J Mirfak RA / Uranus 1.199952 6/5 B (94.78); SKY block
  S Meissa RA 24.136328 silver 24.14 (90.61) separating 13:53, S Al Rescha RA 29.133646 18×φ (51.96) separating 13:33; SKY STARS S Pleiades –
  S Diadem Dec 2 (98.64), S Facies – S Deneb Dec 1+1/√2 (96.78); Orion Nebula Cluster: T1 H RA 160.819052 outside (nearest 100×φ^1 −0.98435),
  its SKY cell S RA 24.173991 silver (54.19) applying 17:49, T24 HORSE H – H Venus Dec 16.000211 16 (97.90) and H – H Mars RA 0.333693 red,
  SKY STARS – S Phact Equator unison (86.16), its Meissa / Alnilam / Phact pairs as above. Changed for this: star counts in tests 28, 30 – 33
  (46 -> 67), T32 assisted Ascot 29 -> 43; tests 34 / 35 run on a 46-star copy of the rebuilt batch, test 35 now compares 93e73bc4 with
  builds by ad0defaf's code; test 31's "the 13" check skips the 21; test 33's engine re-search keeps the ratio orientation fixed at the off
  (as the table; with larger / smaller a unison could never cross: two new events, e.g. S Arcturus – S Aculeus RA, failed only in the test).
  Independent checker (21 Oct), own code from POSITIONS + engine (chk_stars67/check67_*.py), rebuilt Ascot: engine and batch; order of the 67
  everywhere (default and --full); every cell of T1 / T2 (67 rows), T24 SKY 3,350 / HORSE 3,216 / JOCKEY 3,216 (+ midpoints, outlines, red),
  T24 H / J and RATIOS 6,566 (40 scores by hand), SKY block 3,312 cells (+ 7,280 comparisons with the T1 / T2 SKY cells), SKY STARS
  completeness and 14,498 cells; TIMELINE / LONG star events rebuilt (65 / 101; 40 / 59 new-star), 46 real times within 1 min, 13 not
  within 1 year by an hourly scan; before vs after, pairs, Lingfield, default = --full: 0 mismatches. Note (rule as written, 20 Oct): a cell
  inside the conjunction tolerance is red even when its best family is another target - 4 cells on the rebuilt Ascot, e.g. T24 HORSE
  H Ras Algethi – H Juno RA 1.002087 (best whole 1, 80.21), T24 JOCKEY J Alkes – J Juno RA 1.395620 (best √2, 6.57).

## jupiter_tables: T24 conjunction red (Eddie, 20 Oct 2026; display only)
Note 29 Oct 2026 (workbook trim): T24 H / J is gone; red stays on T24 SKY / HORSE / JOCKEY. Text kept for reference.
- T24 SKY / HORSE / JOCKEY (every star row, every body column) and the two distance columns of T24 H / J: a distance inside the
  conjunction tolerance (RA < 1.5, Dec < 0.3) is filled red (FF8080, RED in jupiter_tables.py) instead of its score fill. Values, comments
  ('0 · conjunction (RA < 1.5) · … · score'), midpoint outlines and comment lines, the midpoint columns, the H / J ratio cells, T24 HORSE /
  JOCKEY RATIOS and every other table unchanged; the T24 title note says "filled red".
- Red cells (SKY; per runner HORSE / JOCKEY / H / J): rebuilt Ascot 14:30 2012 SKY 20; P01 16 / 13 / 2. Lingfield 14:35 2021 SKY 7;
  P01 13 / 3 / 1, P03 9 / 11 / 2, P05 7 / 1 / 0, P07 9 / 2 / 0, P09 10 / 5 / 1, P11 7 / 3 / 1. Sizes unchanged (Ascot 0.69 / 0.76 MB,
  Lingfield 2.15 / 2.37 MB; pairs identical).
- Kept (Eddie, 21 Oct 2026): red on every cell inside the conjunction range (RA < 1.5, Dec < 0.3), even when its best family is another
  target (e.g. T24 HORSE H Ras Algethi – H Juno RA 1.002087, best whole 1 (80.21)); no code change.
- Tests 189/189. Test 35: both races --full vs the build before (commit 93e73bc4; tools/scans/families_audit/chk_t24red/compare_red.py):
  red exactly when RA < 1.5 / Dec < 0.3, every other fill as before, values / comments / borders and every other cell identical, only the
  T24 title notes changed (Ascot 3, Lingfield 13), pairs identical, the red counts above (and the 35-star copy); by hand T24 H / J H Nunki
  RA 0.805294 red, ratio cell "together", no fill. Test 28's H Algorab – H Makemake RA 0.064638 now expects red. The comparisons of tests
  31 – 34 with their builds before now run on builds by the code of 93e73bc4 (so each still checks its own change).
  compare_46.py (test 34) tightened: a "title" row may differ only in text cells (fills and comments identical) - before, any row whose
  column A matched passed, so fill changes went unseen; re-run on 7d88f329 -> 93e73bc4: still 0 non-title differences in both races.
  Independent checker (20 Oct), own code from POSITIONS (chk_t24red/check_red_indep.py), both races --full: every T24 SKY / HORSE /
  JOCKEY body cell and T24 H / J distance cell recomputed (Ascot 6,900, Lingfield 13,650), red exactly when RA < 1.5 / Dec < 0.3, other
  fills as before, no red anywhere else; every cell of both workbooks compared (244,936 / 1,041,433): only the T24 title notes differ;
  red cells were before green / yellow / light Ascot 7 / 8 / 36, Lingfield 14 / 16 / 62: 0 mismatches. Default builds: compare_red.py,
  same counts, 0 mismatches.

## jupiter_tables: THREADS and NUMBERS sheets (Eddie, 13 Oct 2026; viewing only)
REMOVED 29 Oct 2026 (Eddie, workbook trim; see "workbook trimmed"): THREADS, P## NUMBERS and FIELD NUMBERS are gone. Text kept for reference.
(16 Oct 2026: value scaling removed - the scaled lines, scaled hits and the repeat rule below are gone; see "No value scaling".)
Common to both: a "repeat" is the same hit seen in two forms of one value (main v and scaled ×10 / ÷10) on the same family with the
same digits (target ×10 or ÷10, e.g. ninth 11.1111 / 1.11111, √2 14.14 / 1.414). Only one form is shown: the main form, unless the
scaled form scores more than 0.5 points higher (unrounded scores; Eddie, 14 Oct). Scores are rounded only for display, at 2 dp everywhere
(T-tables, scaled and also columns, FIELD matrices, THREADS, NUMBERS). Automatic (Jupiter return) unisons are left out.
- **THREADS** (one sheet, after the runner sheets): rows = bodies (sky bodies incl. Moon, Jupiter excluded, Rahu / Ketu folded as
  "Nodes"), columns = runners. Hits = every scored hit (inside tolerance) linking body X with Jupiter, from T1–T8, T10–T13, T16 and T20
  (midpoints T10 / T11 / T20 count at total >= 50, like every hit (15 Oct); scaled hits marked "scaled"; stars, equator and Jupiter–Jupiter left out).
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
- **MATCH HORSE / MATCH JOCKEY on every runner sheet (30 Oct 2026, Eddie), RATIO tightened the same day (whole circle factor >= 5, golden
  p, q <= 6):** see its section. Tests 148/148.
- **Half family removed from families.py (29 Oct 2026, Eddie):** see "half family removed". Tests 146/146.
- **Workbook trimmed (29 Oct 2026, Eddie): POSITIONS, SKY JUPITER, runner T1–T8 + T24 HORSE / JOCKEY (five Jupiter rows on top); no
  summary, --full-only sheets or _pairs workbook:** see "workbook trimmed". Tests 145/145.
- **"sky hit" moved to the end of the (SKY STARS) tables; exact widths, "never narrower" dropped (27 Oct 2026, Eddie):** see its
  section. Tests 262/262.
- **SKY STARS SUMMARY header rows + freeze C3, grey 'stars' rows, widths never narrower (27 Oct 2026, Eddie):** see its section.
  Tests 260/260.
- **T24 HORSE / JOCKEY "S Jupiter" column + four Jupiter rows on the (SKY STARS) tables and summary (27 Oct 2026, Eddie):** see its
  section. Tests 258/258.
- **Whole numbers on the target (0.98 < v < 1 now scores on 1), every table follows (27 Oct 2026, Eddie):** see its section.
  Tests 248/248; full scoring sweep 0 wrong cells.
- **T24 HORSE / JOCKEY (SKY STARS) on every runner sheet + SKY STARS SUMMARY sheet (27 Oct 2026, Eddie):** see its section.
  Tests 245/245.
- **35 stars in T1, T2, T24 (13 new in the engine, no Polaris there) + trimmed default workbook, --full for the rest (19 Oct 2026, Eddie):**
  see its section; same day revised: the 35 in RA order, and the SKY block star rows on the 35. 
- **T24 ratio tables T24 H / J, T24 HORSE RATIOS, T24 JOCKEY RATIOS (19 Oct 2026, Eddie):** see its section.
- **families.py: half family (0.5 … 199.5, ±0.01) and the 4-digit rule for golden, φ powers, ninths, √2, silver; every table follows
  (24 Oct 2026, Eddie):** see its section and Families. Same day: half vs conjunction kept (highest score wins, red marks the range);
  '<target> <family> — not a 4-digit match (<offset>)' for values inside the old tolerance that fail the match. Tests 242/242.
- **T24 repeats flag in T24 SKY / HORSE / JOCKEY: "repeats" column, dotted outline, comment line, title counts (22 Oct 2026, Eddie):**
  see its section. Tests 235/235.
- **T24 STAR SELECT removed from the runner sheets (22 Oct 2026, Eddie); sky star timeline trimming and 95 / 100 / 95 kept:** see the
  22 Oct trimmed section. Tests 231/231.
- **Sky STAR / LONG STAR TIMELINE trimmed to S Jupiter-centred events + 95 / 100 / 95 times; runner T24 STAR SELECT tables (22 Oct 2026,
  Eddie):** see its section. Tests 234/234.
- **LONG STAR TIMELINE (sky) and LONG STAR TIMELINE H / J (22 Oct 2026, Eddie):** see its section. Tests 225/225.
- **All 67 stars in every timeline (runner star events off-sheet), STAR TIMELINE (sky) and STAR TIMELINE H / J, LONG TIMELINE >= 90 (22 Oct
  2026, Eddie):** see its section. Tests 223/223.
- **20 more stars (Ankaa ... Sualocin; Aculeus, Acumen, Facies clusters) and the Orion Nebula Cluster: 67 in T1, T2, T24, T24 ratio tables, SKY
  block, SKY STARS, sky timelines (21 Oct 2026, Eddie):** see its section. Tests 210/210.
- **T24 conjunction cells red (FF8080) in T24 SKY / HORSE / JOCKEY and the T24 H / J distance columns, display only (20 Oct 2026, Eddie):**
  see its section. Tests 189/189.
- **11 more stars (Alpheratz ... Rasalhague; Menkar = alpha Ceti): 46 in T1, T2, T24, T24 ratio tables, SKY block, SKY STARS, sky
  timelines (20 Oct 2026, Eddie):** see its section. Tests 187/187.
- **SKY STARS and the sky TIMELINE / LONG TIMELINE on the 35 stars (20 Oct 2026, Eddie):** see its section. Tests 172/172.
- **Galactic Centre as the 23rd star + T24 stars against bodies (19 Oct 2026, Eddie):** see its section. Engine and card pipeline
  carry the Galactic Centre from now on; older batches unchanged. Same day: T24 columns RA half then Dec half, and T24 midpoints (star
  the middle point of two bodies; midpoint column per half, thick outline, comment line). Tests 134/134.
- **Selangor 17 Oct 2026 card (17 Oct, Eddie): read winners line by line — START HERE: docs/handover_20261017_selangor.md.** 12 tables
  workbooks in reference/selangor_20261017/ (dummy jockey: read horse and sky only); results for 12:15–15:15 in the handover. Way of
  working: Eddie pastes lines, Claude says what each is (raw cells), how they connect, and versus the field (every runner's raw rows); no
  pattern yet. Observations for I'm Back (13:45) and Ari (12:15) are in docs/classic/eye_notes.md. Helper scripts (as run) in
  tools/selangor_20261017/. Also added reference/classic/race_batch_20210802_newcastle_aw_1633_jupiter_tables.xlsx (Athmad, read with result known).
  18 Oct: races with real jockeys read sky / horse / jockey / joins + a fixed-star section (rule in the handover): Newcastle AW 16:33 2021
  (Athmad / Jason Hart) and Worcester 13:00 22 Aug 2021 (Rhythm Is A Dancer / Harry Cobden; workbook added to reference/classic); rows in eye_notes.md.
  Also Musselburgh 13:45 25 Aug 2021 (Graces Quest / Andrew Mullen). Reading rules added 18 Oct (handover): family + timing with every score,
  compare runners only on the same number and family; a 'simple standout' per race.
  Also Goodwood 18:53 27 Aug 2021 (Madame Tantzy / Georgia Dobie); simple standouts for all read races in eye_notes.md.
- **T23 ratios of the T1, T2 and SKY distances (H / J, S / H, S / J) + FIELD 23 (16 Oct 2026, Eddie):** see its section; H / J unisons on the
  H–J Jupiters close rule (automatic / H–J assisted); the S / H / J distances on each row. Tests 120/120.
- **LONG TIMELINE real exact times from the Swiss Ephemeris (16 Oct 2026, Eddie):** see its section. Tests 114/114.
- **LONG TIMELINE (score >= 80, any time) and sky equivalents on TIMELINE H / J (16 Oct 2026, Eddie):** see its section. Tests 113/113.
- **Value scaling removed (16 Oct 2026, Eddie):** see its section and Families. Tests 110/110.
- **TIMELINE H / TIMELINE J on every runner sheet (16 Oct 2026, Eddie):** see its section. Tests 109/109.
- **TIMELINE on SKY JUPITER (16 Oct 2026, Eddie):** see its section. Tests 106/106.
- **SKY block timing, royal-star-only tables T21R / T22R / SKY ROYAL / FIELD 21R / 22R (16 Oct 2026, Eddie):** see its section.
  Tests 103/103.
- **SKY PAIRS body – royal, T19 sky side (15 Oct 2026, Eddie):** see its section (revised the same day: together sky sides plain,
  no d(S Jupiter, royal star) in the tag). Tests 97/97.
- **Third area "φ and √2" (15 Oct 2026, Eddie):** between area A and area B, same tables; see its section. Tests 92/92.
- **Areas A / B (15 Oct 2026, Eddie):** area A intervals (1, 3/2, 2, 3 … 9) on ±0.02 absolute; every ratio table split into area A,
  area B (and no hit). See the section "jupiter_tables: areas A / B". Tests 92/92.
- **THREADS midpoint cut (15 Oct 2026, Eddie):** midpoint hits (T10, T11, T20) count only at total >= 50, like every hit. Lingfield
  14:35 2021: 19 midpoint lines (7.83–48.10) moved to "+ n weaker"; 8 cells lost the "both charts" tag (P01 Uranus, P09 Uranus,
  P03 Neptune, P05 Makemake, P11 Makemake, P05 Orcus, P01 Transpluto, P03 Nodes). Ascot 14:30 2012: 1 line (P01 Uranus T11 39.16),
  no tag change. Tests 80/80.
- **Independent checker on the last two unchecked cases (15 Oct 2026), recomputed from POSITIONS (families.py only, not the tool's
  code): 0 mismatches, no corrections.** Wincanton 14:20 2022 P09 Birds Of Prey / Harry Cobden: every T12–T14 ratio of all 6 runners;
  P09 has 22 unisons, all T13 J RA (none T12, Dec or T14); Jupiter return S–J RA 0.032759, Dec 0.521920; 20 automatic (return ratio
  0.000183 Mars – 0.000979 Eris); 2 genuine, return-assisted, field 1/6: J Ketu 1.001694 (68.99, ratio 0.001694), J Gonggong 1.001741
  (68.21, 0.001741); the only other unison in the field is P03 T12 J Eris RA 1.008901 (1.21). Nottingham 15:30 2022 P01 Dynamic Force
  THREADS Transpluto: T6 RA 141.532633 → 141.4 (71.00), T7 Dec 33.33254 → 33.3333 (99.05), T8 Dec 13.368851 → 13.3333 (57.38), T5 no
  hit → directions 3, mutual same chart (T6 + T8), mutual across charts (T6 + T7), both Jupiters (T7 + T8); 'both charts' rightly absent
  (no H Transpluto hit >= 50 in T1–T5, T12, T13; T10, T11, T16, T20 not recomputed, the cell lists none >= 50).
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
  Independent checker (14 Oct) recomputed the moved cases from the input positions (Newcastle P05 / P11 RA Rahu ratios and 2/6, Sandown P07 Vesta 3/2 and J Mars 9/8, Wincanton P01 ninth 11.1111 row and 1/6, Lingfield SKY EQ Mars = Neptune Equator): 0 mismatches. Cobden's 22 unisons and the Nottingham Transpluto tags were checked on 15 Oct (see the THREADS midpoint cut entry above). Ascot 14:30 2012:
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
