# New chat: race reads from stage 1 + stage 2 (Eddie, 7 Nov 2026)

Paste this at the start of the new chat. Everything needed is here; nothing depends on earlier chats.

## Where we are
- **Stage 1** (`tools/eddie_read.py`) collects every cell from the race's tables workbook in Eddie's order.
- **Stage 2** (`tools/eddie_layers.py`) lays out the stage 1 data in fixed layers for every runner. It shows data only: no interpretation, no score cut-offs, no centre tags, no ranking, no pick.
  - L0 field check: runners in the tables workbook against the `_active.xlsx`.
  - L1 same bodies.
  - L2 what lands on each same body, with each source's own sky lines.
  - L3 plain matches: same body on both charts, one body in both planes, runner number = sky number, circle divisions, same number in several places, N and N×φ.
  - L4 every natal body with every cell on it.
  - Every item is tagged "only" or "also: <runners>".
- **Stage 3** is the rules (built 7 Nov 2026):
  - `docs/eddie_read/rules.json`: every rule in plain words, with the races it was seen on (`in_sample`); every other race is a test race.
  - `tools/eddie_rules.py`: runs every rule on a race and lists the runners each one selects, with their cells. It never reads results.
  - `tools/eddie_backtest.py`: the only script that reads `docs/eddie_read/results/results.json`. Per rule: picks, winners, 1st or 2nd, each against chance, for test races and in-sample races separately.
  - 14 rules to start: set A (the old register R25, R28, R1b, R7, R26, R40, R42, R1) and set B (B1 strong-line-star filter, B2 top strong-line conj, B3 version 4, B4 same-body clear lead, B5 same body both planes, B6 same body both charts). Back-test so far: `docs/eddie_read/backtest/backtest.md`.
  - New rules are made race by race with Eddie.

## What Eddie does
- Uploads two files for one race: `race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx` and `..._active.xlsx`.
- Pastes the result later.

## What Claude does, every race, the same way
1. `cd /home/claude/astro-harmonics && git pull` (branch `t24-sun-moon`). If the repo is not there, attach it and clone it.
2. Copy both uploads into `reference/classic/` under their race_batch names.
3. Stage 1: `python3 tools/eddie_read.py reference/classic/race_batch_<...>_jupiter_tables.xlsx --out docs/eddie_read`
4. Stage 2: `python3 tools/eddie_layers.py docs/eddie_read/race_batch_<...>_eddie_read.json`
5. Stage 3: `python3 tools/eddie_rules.py docs/eddie_read/race_batch_<...>_eddie_read.json` -> `docs/eddie_read/rules/<race>_rules.md`.
6. Send Eddie the three `.md` files (`_eddie_read.md`, `_layers.md`, `_rules.md`). If L0 shows a runner missing from the tables workbook, say so first.
7. Commit and push the reports, force-adding the tables xlsx (it is git-ignored), before the result is pasted.

## Reading with Eddie
- Show the data; don't judge it. Answer Eddie's questions from the two reports, every cell in full: `source → chart body plane value target family (score)`. Copy the numbers from the report; never invent one.
- Follow Eddie's order: same body first, then sky Jupiter, Sun, Moon, MATCH, T1 / T2, T24 top rows, T24 star rows (`claude/race-read-instruction.md`).
- "Only" / "also" comes from the report's field tags. Don't add a claim of your own without checking every runner.
- A jockey's own natal cells come with him in every ride.
- Don't add conditions or weighing of your own. No picks unless Eddie asks for one.

## After the result
- Add the result to `docs/eddie_read/results/results.json` (ran, first, second, finishing order, non-runners, runners not in the workbook), then `python3 tools/eddie_backtest.py`. This race is a test race for every rule that existed before it.
- Show what each rule selected against the result, and what the winner had in the stage 2 report, layer by layer (same body first), against the field.
- If Eddie names a pattern, write it as a candidate rule in plain words, with the cells it would use. Don't build it until he says go.
- When Eddie agrees: add it to `rules.json` (with this race and any race it was seen on in `in_sample`) and its function to `RULES` in `tools/eddie_rules.py`; rerun the rules on every race and the back-test; tests; checker; commit and push before the next race. Never change a rule after a result: a change is a new rule with a new id.

## Rules (standing)
- Never open any `.csv`, and don't look results up.
- Wait for Eddie's explicit go-ahead before building or changing any code. Running the scripts is fine.
- After every code change or read with claims, run an independent checker (a subagent with its own code, from the stage 1 json or the POSITIONS sheet). Apply its corrections before reporting.
- Tests:
  - `python3 tests/eddie_read_check.py` (stage 1)
  - `python3 tests/eddie_layers_check.py` (stage 2)
  - `python3 tests/eddie_rules_check.py` (stage 3; about 3 min)
- Don't say something is saved until it is committed and pushed. Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
- Race docs go in the project (`claude/<course>-<hhmm>-<yyyymmdd>-blind.md`) and the repo (`docs/eddie_read/results/`).

## Background (read only if needed)
- Rules of each stage: the docstrings of `tools/eddie_read.py`, `tools/eddie_layers.py`, `tools/eddie_rules.py` and `tools/eddie_backtest.py`.
- Eddie's method: `claude/eddie-race-read-method.md`, `claude/race-read-instruction.md`.
- Earlier method versions and the race logs: `claude/full-race-read-method.md`.
- Repo handover: `CLAUDE.md`.