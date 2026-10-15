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
  race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx (raw Jupiter tables T1–T14, T16–T22 per runner (T15 removed 15 Oct 2026), field matrices, off and +5 min,
  every family from tools/families.py scored, best = highest score, also, scaled ×10 / ÷10, colours by score; ratios on the interval
  list with Group column, P## RATIOS sheets, FIELD 12–14; T16 RA–Dec crossing + FIELD 16; T17 equidistance + FIELD 17; T18 horse | jockey; T19 + P## PAIRS; T20 + FIELD 20; T21, T22 + FIELD 21, 22 (fixed stars); SKY cells in T1 / T2 and a sky side in T21 with the tag 'same as sky'; THREADS, P## NUMBERS and FIELD NUMBERS
  sheets - rules in the section below). Venv python (swisseph, pandas).
  Planes RA, Dec and Equator only (Flat and GC removed 14 Oct 2026 for noise, Eddie).
  Tests `python3 tests/jupiter_tables_check.py` (96/96). In the card pipeline: `run_card_swiss.py --tables`
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
- Tags (rows): Lingfield 14:35 2021 P01 4, P03 6, P05 7, P07 7, P09 8, P11 1 (33); Ascot 14:30 2012 P01 7. Note: 28 of the 40 carry a
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
  tags of all runners: 0 mismatches. Open point (Eddie): a sky side tagged "X, Y together" still gets an area and can carry a tag (Lingfield
  P07 2 such sides, Ascot P01 7; Ascot H Transpluto – H Regulus RA tagged "ratio 1 · unison" with the sky side together, d(X, Y) 0.929582).

## jupiter_tables: THREADS and NUMBERS sheets (Eddie, 13 Oct 2026; viewing only)
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
- **SKY PAIRS body – royal, T19 sky side (15 Oct 2026, Eddie):** see its section. Tests 96/96.
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
