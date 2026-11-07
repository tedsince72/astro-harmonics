# New chat: race reads from the stage 1 report (Eddie, 7 Nov 2026)

Paste this at the start of the new chat. Everything needed is here; nothing depends on earlier chats.

## What Eddie will do
- Upload two files for one race: `race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx` and `..._active.xlsx`.
- Paste the result only after the read is done.

## What Claude does first (every race, the same way)
1. Repo: `cd /home/claude/astro-harmonics && git pull` (branch t24-sun-moon). If the repo is not there, attach it and clone it.
2. Copy both uploads into `reference/classic/` under their race_batch names.
3. Run: `python3 tools/eddie_read.py reference/classic/race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx --out docs/eddie_read`
   It writes `docs/eddie_read/race_batch_<...>_eddie_read.md` (+ `.json`).
4. Run stage 2: `python3 tools/eddie_layers.py docs/eddie_read/race_batch_<...>_eddie_read.json` (writes `_layers.md`).
5. Send Eddie both `.md` files. The two reports are the starting place and the only source for the read.

## How to read
Follow `claude/race-read-instruction.md` (repo: `docs/eddie_read/RACE_READ_INSTRUCTION.md`) step by step: Eddie's order (same body first, then sky Jupiter, Sun, Moon, MATCH, T1 / T2, T24 top rows, T24 star rows), then the relationship search, then the read. No counts.

## Rules (standing)
- Never open any `.csv` (the race csv holds the result). Don't look results up; Eddie pastes them.
- Wait for Eddie's explicit go-ahead before building or changing any code. Running the script is fine.
- After each read, run an independent checker (subagent, own code from the POSITIONS sheet) on the claims. Apply its corrections before reporting.
- Save the blind read to the project (`claude/<course>-<hhmm>-<yyyymmdd>-blind.md`) and the repo (`docs/eddie_read/results/`). Force-add the tables xlsx (git-ignored) and the report. Commit and push before the result is pasted.
  Commit trailer:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`
- Don't say something is saved until it is committed and pushed.
- After the result: add it to the race doc and say what the winner had in the report, cell by cell, against the field.

## Background (read only if needed)
- Project docs: `claude/full-race-read-method.md` (earlier method versions and logs), `claude/eddie-race-read-method.md` (Eddie's method).
- Rules of the report itself: the docstring of `tools/eddie_read.py`.
- Repo handover: `CLAUDE.md`.
