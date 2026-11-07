# Race read instruction (Eddie's order, revised 7 Nov 2026)

How to read every race. Eddie's reading hierarchy (7 Nov 2026), then the relationship search. Same body comes first, every time.

## Before the read
1. `cd /home/claude/astro-harmonics && git pull` (branch t24-sun-moon).
2. Copy Eddie's two uploads into `reference/classic/` as `race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx` and `..._active.xlsx`.
3. Run stage 1, stage 2 and stage 3:
   - `python3 tools/eddie_read.py reference/classic/race_batch_<...>_jupiter_tables.xlsx --out docs/eddie_read`
   - `python3 tools/eddie_layers.py docs/eddie_read/race_batch_<...>_eddie_read.json`
   - `python3 tools/eddie_rules.py docs/eddie_read/race_batch_<...>_eddie_read.json`
   Send Eddie the three `.md` files. If L0 shows a runner missing from the tables workbook, say so first.
4. Never open any `.csv`. Don't look results up.

Every cell is written in full: `source → chart body plane value target family (score)`, with toward / away and exact time where it has one. Copy the numbers from the report; never invent one.

## Part 1. The reading hierarchy (Eddie, 7 Nov 2026) — the READ section of the stage 2 report

**Step 1. Same body — start here (READ 1).**
- Every sky X → natal X cell, both planes, H and J, scoring and loose.
- For each cell note: circle division (360/n); ×10 / ×100 digit repeat; the same body on both charts; the same body in both planes.
- Keep this list open for the rest of the read: every later step is checked against these bodies and numbers.

**Step 2. Jupiter and Sun star lines, highest score first (READ 2).**
- The lead lines are sky Jupiter → star and sky Sun → star lines (conj included), in one list, highest score first. Read down the list.
- **Read each line in its entirety before the next one.** Under each line, for every runner:
  - that star's natal rows (horse and jockey; natal and sky copies; every cell);
  - the MATCH rows for that sky cell;
  - natal Jupiter → that star (T1 / T2);
  - every other cell on that line's number (same family and target).
  - each with "only" / "also", and how many runners have cells under the line.

**Step 3. The Moon only confirms.** A Moon line cannot activate a line on its own. It is read only under the Jupiter / Sun star line it confirms: the Moon to the same star, or a Moon line on the same number. Moon lines that confirm nothing are listed as "Moon only, not active" (READ 4) and are not followed onto the runners.

**Step 4. Jupiter / Sun lines to bodies (READ 3)** are listed, not followed. Their cells still show in L2 and L4.

The noted sky lines feeding this (stage 1, Eddie 7 Nov 2026): a line that is not a conj scores 50 or more (exact within ±120 min of the off, or 90 or more and applying); a conj scores 20 or more; a star line at 40–50 stays only when another centre reaches the same star at 50 or more.

## Part 2. Search each runner's report for relationships, not counts

Go through every runner and list each case below, every cell in full, and say for each whether another runner in the field has the same (stage 2 L3 has cases 1–5).

1. **Same body on both charts** — the same body scores in the horse's same-body cells and the jockey's.
2. **One body in both planes** — the same body scores in RA and in Dec, in one chart.
3. **Runner number = sky number** — a same-body, T1 / T2, T24 or star cell whose target equals a sky line's target.
4. **Circle divisions** — whole numbers dividing 360 (4 = 360/90, 5 = 360/72, 6 = 360/60, 10 = 360/36 …).
5. **The same number in more than one place** — different sources, bodies or charts on the same target; a number with its N×φ.
6. **A star and a sky line on one body** — a natal body conj a star, where a Jupiter or Sun line (Moon as confirmation) also reaches that body or star.
7. **Jupiter and Sun meeting** — both centres (or their stars) pointing at the same star, body or number; the Moon only as confirmation.

Then, **for every same body from step 1, say what else lands on it or uses its number** (stage 2 L2).

## Part 3. Read
- For each runner, say how its pieces connect to each other, same bodies included. A runner's read is not finished until its same bodies are tied to the rest.
- Then say which runner's pieces join up the most, and how, in cells.
- No counts and no ranking by numbers of cells. Don't add conditions of your own to a flag.
- Leave out the jockey's own natal cells that come with him to every ride (e.g. a J star conj J Jupiter).
- Say what you see, without preconception.

## Part 4. Check, save, wait
- Independent checker (subagent, own code from the POSITIONS sheet or the stage 1 json, no csv) on every claim, including each "only" / "also". Apply its corrections before reporting.
- Save the blind read to the project (`claude/<course>-<hhmm>-<yyyymmdd>-blind.md`) and the repo (`docs/eddie_read/results/`, force-add the tables xlsx and the reports); commit and push before the result. Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Don't say saved until committed and pushed.
- After Eddie pastes the result: show what the winner had, in the same order (same body first, then each Jupiter / Sun star line), cell by cell, against the field.
