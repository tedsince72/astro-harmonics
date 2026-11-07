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
4. Send Eddie the `.md` file. That report is the starting place and the only source for the read.

## How to read (Eddie's way)
- Read the report runner by runner, in its own order: sky notes, same body, MATCH, T1 / T2, T24 top rows, T24 star rows, threads, flags held.
- Look at the details and how they relate, not at counts. Nothing is just about counts. Say what the cells are, which ones point at the same thing, and how. For example:
  - the same body scoring on both charts;
  - one body scoring in both planes;
  - a same-body number that is also a sky line number;
  - a star on a natal body that a sky line also reaches;
  - Jupiter, the Sun and the Moon meeting at the same point.
- Write every cell as `value target family (score)`, copied from the report. Never invent a number.
- Check "only" against every runner in the field before writing it (the report's "only" / "also: ..." tags do this).
- One fixed star on one natal body counts once, whether it comes from the natal (H / J) copy or the sky copy.
- A jockey's own natal cells (e.g. J star conj J Jupiter) come with the jockey to every ride, so they don't separate one horse from another.
- Don't add conditions of your own to a flag. Report what is there.
- Say what you see, without preconception. Give the read blind, then wait for the result.

## Every race: the seven cases, then the connections (Eddie, 7 Nov 2026; must be done for every race)
Go through every runner's section and list each case of the following. Write each cell as `value target family (score)`, and say for every case whether another runner in the field has the same thing.
1. Same body on both charts. The same body scores in both the horse's same-body cells and the jockey's (e.g. S Makemake → H Makemake and S Makemake → J Makemake).
2. One body in both planes. The same body scores in RA and in Dec, in one chart (e.g. J Sun RA and J Sun Dec).
3. A runner's number that is also a sky number. A same-body, T1 / T2, T24 or star cell whose target equals the target of a Jupiter, Sun or Moon sky line (e.g. J Makemake 13 = S Moon → Menkar 13).
4. Circle divisions. A whole number that divides 360 (4 = 360/90, 5 = 360/72, 6 = 360/60, 10 = 360/36 …).
5. The same number in more than one place for one runner. Different sources, bodies or charts landing on the same target, and the same number with its N×φ.
6. A star and a sky line on one body. A natal body conj a star, where a sky line from Jupiter, the Sun or the Moon also reaches that body or star.
7. Jupiter, Sun and Moon meeting. Two or three centres pointing at the same star, body or number for this runner.

Then, for each runner, describe how its pieces connect to each other. Say which runner's pieces join up the most, and how. Don't count or rank by numbers of cells. Leave out jockey-only cells that come with the jockey to every ride.

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
