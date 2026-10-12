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
- Older single-purpose readers still useful: `tools/fit_read.py`, `movement.py`, `both_ends.py`, `three_way_all.py`, `equator_ratios.py`,
  `strings.py`; scans in `tools/scans/`.
- On the Mac: see `docs/MAC_SETUP.md` (venv with Python 3.12+, `pip install openpyxl`). Scripts call `python3.12`; inside the venv
  `python3` is fine (edit `tools/run_layers.sh` if `python3.12` is not on the PATH).

## Where we are (12 Oct 2026)
- Layers 1–5 built and tested against all 29 hand reads + Dettori; frozen v2 = commit 4baefa1 (see how_it_works.md).
- Blind batch of 10 older races (results exist, never read with this method), one race at a time:
  done Exeter 15:15 (winner Forget You Not — layers missed it), Redcar 15:15 (winner Present Moment — the only partner strike, layers had it),
  Haydock 14:20 (winner Golden Flame — layers missed it; Orcus: Fanning's Ketu at the midpoint of horse Orcus and sky Orcus; soaks).
  Next: Kempton 14:40 (4 Sep 2021), then Fontwell 16:45, Goodwood 18:53, Musselburgh 13:45, Worcester 13:00, Newcastle AW 16:33,
  Catterick 14:40 (Mason's Wotever Next — partly seen before).
- Lesson so far: the layers find general shapes; winners have been found in specific DETAIL (checklist). Eddie's decision (12 Oct):
  continue on the Mac with Claude Code, short sessions, and build an accurate reader around the winner checklist — each checklist item
  a small test, run on every runner, reported with tightness and field rarity; grow the checklist one confirmed item at a time.
- Checklist reader FROZEN (12 Oct): CR v1.1 = commit 3d62207. `python3 tools/checklist_reader.py <race>` -> docs/classic/<race>/checklist/
  (field.txt = race page with the watch line; P##.txt = runner page with joins). Tests `python3 tests/checklist_check.py` (421/421, 13
  DIFFERENCE/EXPLAINED). Design, as-built notes and Eddie's decisions: docs/classic/checklist_reader_design.md (sections 9–11).
  Item rates: docs/classic/checklist_rates.txt. Blind batch with the frozen reader: Kempton 14:40 done (winner Hamish — its only field-only
  item the node loop); Fontwell 16:45 next. Sky-anchored soak candidate scanned (no separation; checklist section 5 item 9).
- Open candidates (built into the reader as items 14, 17, 20, 21; still not frozen rules): shared pair that is also cross-linked; the Dec 9/4 : 5/4 : 9/5 same-body split; natal body at
  the midpoint of a body and its own sky body; soak (one value from 4+ non-star partners across horse, jockey, sky). Details in the checklist.

## How to run a session
1. Start: `cd ~/astro-harmonics && git pull` then `claude`. Say what you want to do (e.g. "read Kempton 14:40 blind").
2. Work one race or one script change. Checker after each read. Commit + push.
3. End: ask Claude to update "Where we are" here and the checklist, commit and push; then type `exit`.
