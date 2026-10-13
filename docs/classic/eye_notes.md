# Eye notes — Eddie's observations from the Jupiter tables

Started 13 Oct 2026. The working view is `tools/jupiter_tables.py` on Eddie's families (`tools/families.py`; CLAUDE.md "Families").
One entry per observation. Copy values from the workbook cells (never rounded by hand). Field check: how many runners in the same race
hold the same thing (same table, row, plane, target), from the FIELD sheets or by reading every runner sheet. No conclusions here, only what
is seen; a candidate idea is written down separately and tested forward.

Build a race: `~/astro-venv/bin/python3 tools/jupiter_tables.py reference/classic/race_batch_<yyyymmdd>_<course>_<hhmm>.xlsx`
(blind races: don't open the csv or any result file before the note is written and committed).

| date | race | runner (P##, horse / jockey) | table, row, plane | exact values (value, target, offset, score, +5, arrow) | field check (k/n) | result known when noted? | Eddie's note |
|---|---|---|---|---|---|---|---|
| 13 Oct 2026 | Nottingham 15:30 1 Jun 2022 | P01 2 Dynamic Force / Ray Dawson (winner) | T12 (S Jupiter–S X) / (natal Jupiter–natal X), groups Perfect / Harmonic | S Jupiter–S Haumea / H Jupiter–H Haumea RA 2.999826 → 3 twelfth −0.00581 % [92.4]; S Jupiter–S Mars / J Jupiter–J Mars (inverted) Flat 8.999505 → 9 9th harmonic −0.00550 % [92.8]; S Jupiter–S Pluto / J Jupiter–J Pluto Flat 1.49989 → 3/2 fifth −0.00731 % [90.49] | only runner of 5 with a T12 Perfect/Harmonic hit >= 90; the others' T12 Perfect/Harmonic hits all <= 53.49 (P03 7th harmonic GC), any other T12 hit <= 83.6 (P09 1+√2 RA) | yes (read race, not evidence) | Three T12 Perfect/Harmonic hits >= 90, no other runner close. |
| 13 Oct 2026 | Nottingham 15:30 1 Jun 2022 | P01 2 Dynamic Force / Ray Dawson (winner) | Uranus thread: T5, T7, T8 | T5 S Jupiter → H Uranus Dec 11.10793 → 11.1111 (ninth) −0.00318 [94.8], +5 11.107725, away; T7 S Uranus → H Jupiter GC 142.001746 → 142 (whole) +0.00175 [83.3], +5 142.001931, away; T8 S Uranus → J Jupiter Dec 18.995206 → 19 (whole) −0.00479 [57.8], +5 18.995259, toward | not yet checked across the field | yes (read race, not evidence) | Uranus thread: sky Jupiter to horse Uranus, sky Uranus to horse Jupiter and to jockey Jupiter. |

## Scans from these notes (read-only)
- 13 Oct 2026 — T12 Perfect or Harmonic at score >= 90, all 48 races with known results (automatic unisons left out):
  `tools/scans/t12_perfect_harmonic_scan.py` -> docs/classic/eye_scans/t12_perfect_harmonic_90.txt.
  Older 35 races (read; results known — not evidence): 19 holders, winners 4 (chance 3.14), beaten 15.
  13 races of 12 Oct 2026 (blind when read, results now known): 8 holders, winners 2 (chance 1.39; without non-runners 1.52), beaten 6.
  The idea came from Nottingham 15:30 (in the older set), so the older set is not a test of it.
