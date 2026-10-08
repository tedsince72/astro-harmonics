# PINPOINT blind test kit – instructions for Claude Code

Prepared 2 Oct 2026 in Eddie's Claude chat ("Astronomy Research" project). Eddie runs this on his own
machine in `~/astronomy-project`. Read this whole file before doing anything.

## Standing rule – preserve verbatim
> **Always wait for Eddie's explicit confirmation before building or generating code or artifacts.**

Running the scripts in this kit as described below is what Eddie has asked for. Changing them, writing
new ones, or "improving" the method is not – ask Eddie first.

## What this is for
The research reads each race "pair by pair": which sky pair, onto which natal body, held how
(own link, Type 1, natal pair, self, or landing on a natal body), and how the field splits each pair.
It was built and read on the 48 **baseline** races. The 48 **test** races (split seed 20260929, never
redrawn – see `dataset_split.csv` in the repo) have not been looked at. This kit runs the test races
**blind**: everything is produced without the result, Eddie uploads it to the Claude chat, the calls for
the first three are written down there, and only then are the results attached and scored.

**The blind part matters more than anything else.** Do not open, print or summarise finishing
positions, SPs or favourite marks for the test races at any point before Eddie says the calls are saved.
That includes the race CSVs (they hold `finish_pos`, `sp`, `is_fav`), `dataset_manifest.csv`
(`race_type`, `fav_sp`, `win_sp`), results txt files and `_pinpoint.txt` files.

## Kit contents
- `tools/` – `race_detail.py` v1.3 and what it imports (`active_vibrations.py` v4.1, `pinpoint_reading.py`
  v1.2, `sections_common.py`, `three_way_midpoints.py` v2.0, `old_sections.py`); `bv_record.py`,
  `runner_features.py`, `blind_test.py` (frozen P20/P21/C1), `royal_record.py` v1.1, `pair_body.py` v1.4
  (grids), `profile.py` v1.1, `attach_results.py` v1.1. Keep them together in `tools/`; they import each other.
- `run_blind.sh` – the blind run. `score.sh` – the scoring run, after the calls.
- `reference/` – the 48 baseline races' outputs (item records, pair_body, profiles, features, royal items,
  frozen P20/P21/C1 holders of races 1–24). For later comparison only; nothing in the blind run reads them.
  `not_in_baseline_race_keys.txt` lists the 49 race keys in the manifest that are not baseline races –
  `dataset_split.csv` is the authority for which 48 are the test set.

## Steps

### 0. Place the kit
Put the folder at `~/astronomy-project/pinpoint_blind_kit/`. Python 3 with numpy, pandas, openpyxl
(already used by the pipeline). Do not overwrite the repo's own copies of `active_vibrations.py` or
`pinpoint_reading.py` – the kit uses its own copies inside `tools/`.

### 1. List the test races and check their workbooks
- From `dataset_split.csv`, take the test rows. For each, find
  `racecards/YYYYMMDD_venue/race_batch_YYYYMMDD_venue_HHMM_active.xlsx`.
  Use date + time, not the venue name, to match (venue names in files can be longer than the
  12-letter dataset key; Kempton races have the key `sunbury`). Ignore stray older files with a wrong time.
- Each workbook must be the current build: charts v2.3, engine v2.2 (natal at 12:00 standard time,
  fingerprint `64612c16fe`), `active_vibrations` v4.1, every chart with a date of birth and country.
  Check the META sheet. **Do not read the race CSV's result columns while doing this.**
- If any workbook is older, list them for Eddie and stop. Eddie rebuilds them with commands in this format
  (one pair of lines per race, run from `~/astronomy-project`):
  ```
  python racingpost_excel_charts_swiss.py --csv racecards/<folder>/<race>.csv --ephemeris-path ephe --engine celestial_bodies_swisseph.py
  python active_vibrations.py --input racecards/<folder>/<race>.xlsx
  ```
- Write the 48 `_active.xlsx` paths, one per line, to `pinpoint_blind_kit/races.txt`.

### 2. Blind run
```
cd ~/astronomy-project/pinpoint_blind_kit
OLD_DIR=<folder of the post-48-race pipeline, the one holding run_pipeline.py> bash run_blind.sh races.txt
```
- Step 1 (detail sheets) takes several minutes per race and prints progress; it skips races already done,
  so it can be restarted. Every sheet must end "result not found" – the script checks and stops if not.
- At the end it writes `blind_out_for_claude.zip` (grids, detail sheets, profiles, pair_body, features,
  royal items, P20/P21/C1 holders). Every finish in it shows "?".
- Tell Eddie it's ready; he uploads the zip to the Claude chat. Don't summarise the grids yourself.

### 3. Scoring – only after Eddie confirms the calls are saved
```
RACECARDS=~/astronomy-project/racecards bash score.sh
```
- Attaches each race's result from the race CSV beside its chart (blind copies kept as `*.blind`),
  re-runs features, royal record, pair_body, grids and profiles with the result, scores P20/P21/C1,
  and writes `scored_for_claude.zip` for Eddie to upload.
- Check one race's RESULT block against the official result before reporting done.

## If something fails
Report the exact error and the race. Don't change the method or thresholds to make it run. The settings
in `run_blind.sh` (`--low 50 --mp 0.1 --mp4 0.05 --tw-wide 0.5`) are the ones used for all 48 baseline races.
