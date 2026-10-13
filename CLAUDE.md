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
  movement (sky X vs natal X). Whole ±0.005, ninth ±0.0005; movement ±0.01 / ±0.0011; Equator values ±0.01; simple ratio p/q with
  q <= 9, p <= 30, not 1, within 0.005% (near bands listed separately); cross link close = RA < 1.5 or Dec < 0.3 (near RA < 2, Dec < 0.6).

## Tools (run from the repo root)
- Layered reader: `tools/run_layers.sh <race>` = layer1_inventory → layer2_roots → layer3_web → layer4_field → layer5_reader.
  Outputs `docs/classic/<race>/layer1..layer5/`. Results only via `python3 tools/layer4_field.py <race> --results` (separate file).
  Designs and test results: `docs/classic/how_it_works.md`, `layer*_design.md`, `layer*_README.md`, `pair_focus_design.md`.
  Tests: `tests/layer1_reproduce.py <race>`, `tests/layer2_check.py`, `tests/layer3_check.py`, `tests/layer4_check.py`, `tests/layer5_check.py`.
- Checklist reader: `tools/checklist_reader.py <race> [--results]`; tests `tests/checklist_check.py`. Watch line: `tools/scans/watch_jupiter.py`.
- Jupiter-centred read (built 12 Oct 2026, Eddie's go-ahead): `bash tools/jup/run_all.sh <race>` -> docs/jupiter/<race>/ (positions, measures,
  layer2 ratios, layer3 every measure per runner, field.txt). Rules, tests and open points: docs/jupiter/README.md. Today's 13 races (12 Oct 2026)
  are run, blind (no results opened).
- Older single-purpose readers still useful: `tools/fit_read.py`, `movement.py`, `both_ends.py`, `three_way_all.py`, `equator_ratios.py`,
  `strings.py`; scans in `tools/scans/` (field_only_rates, sky_anchored_soak/compare, star_join_scan, jupiter_partner_scan).
- On the Mac: see `docs/MAC_SETUP.md` (venv with Python 3.12+, `pip install openpyxl`). Scripts call `python3.12`; inside the venv
  `python3` is fine (edit `tools/run_layers.sh` if `python3.12` is not on the PATH).

## Where we are (12 Oct 2026, end of session)
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
   `python3 tools/scans/watch_jupiter.py <race>`. No rule, threshold or watch-line change before the result.
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
