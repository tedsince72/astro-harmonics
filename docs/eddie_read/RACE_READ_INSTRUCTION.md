# Race read instruction (Eddie's order, 7 Nov 2026)

How to read every race. It follows the order Eddie used when he showed his reads (Newcastle 15 Feb, Leicester 17 Feb, Haydock 19 Feb 2022; claude/eddie-race-read-method.md), then the relationship search. Same body comes first, every time.

## Before the read
1. `cd /home/claude/astro-harmonics && git pull` (branch t24-sun-moon).
2. Copy Eddie's two uploads into `reference/classic/` as `race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx` and `..._active.xlsx`.
3. Run `python3 tools/eddie_read.py reference/classic/race_batch_<...>_jupiter_tables.xlsx --out docs/eddie_read` (stage 1), then
   `python3 tools/eddie_layers.py docs/eddie_read/race_batch_<...>_eddie_read.json` (stage 2: L0 field check, same bodies, what lands
   on each same body, the seven cases, every item field-tagged). Send Eddie both `.md` files. Part 1 and Part 2 below are read from
   these two reports; nothing is judged by hand before Part 3. If L0 shows a runner missing from the tables workbook, say so first.
4. Never open any `.csv`. Don't look results up.

Every cell is written in full: `source → chart body plane value target family (score)`, with toward / away and exact time where it has one. Copy the numbers from the report; never invent one.

## Part 1. Collect, in this order, for every runner (horse H and jockey J)

**Step 1. Same body — start here.**
- Every sky X → natal X cell, both planes, H and J, scoring and loose (the report's "1. Same body", loose cells included).
- For each cell note: circle division (360/n); ×10 / ×100 digit repeat; the same body on both charts; the same body in both planes; same-body Jupiter, Sun or Moon.
- Keep this list open for the rest of the read: every later step is checked against these bodies and numbers.

**Step 2. Sky Jupiter** — every line (star, body, conj) with value, target, score, toward / away, exact time; circle divisions; conj points; lines that another centre shares.

**Step 3. Sky Sun** — the same, including the Sun's conj stars and bodies, however weak.

**Step 4. Sky Moon** — the same; mark any point the Moon shares with Jupiter or the Sun.
- From 2–4 also note: the hub (a point two centres reach); the top line (highest, exact at the off); each centre's conj stars; each centre's line stars at any score; the body lines (a centre → a sky body, e.g. S Moon → Pallas).

**Step 5. MATCH** — the runner's T24 cells that match a sky line; mark where the T24 star is itself a line star.

**Step 6. T1, then T2** — natal Jupiter → body / star cells on a noted star, body or number; a repeated top-line number. Write "none" when there is none.

**Step 7. T24 top rows, horse then jockey** — S Jupiter / Sun / Moon → natal body, S body → natal Jupiter: conj, circle divisions, the nodes, "match horse" (jockey repeats a body or number), "matches back to the sky".

**Step 8. T24 star rows, horse and jockey together** — Jupiter stars, then Sun stars, then Moon stars (conj stars included). For each star: every scoring cell, conj (a natal body on the star), midpoints, cells on the runner's own Jupiter / Sun / Moon, sky numbers, "same as horse". One fixed star on one natal body counts once (natal and sky copies are one).

## Part 2. Search each runner's report for relationships, not counts

Go through every runner and list each case below, every cell in full, and say for each whether another runner in the field has the same.

1. **Same body on both charts** — the same body scores in the horse's same-body cells and the jockey's.
2. **One body in both planes** — the same body scores in RA and in Dec, in one chart.
3. **Runner number = sky number** — a same-body, T1 / T2, T24 or star cell whose target equals a Jupiter, Sun or Moon sky line's target.
4. **Circle divisions** — whole numbers dividing 360 (4 = 360/90, 5 = 360/72, 6 = 360/60, 10 = 360/36 …).
5. **The same number in more than one place** — different sources, bodies or charts on the same target; a number with its N×φ.
6. **A star and a sky line on one body** — a natal body conj a star, where a sky line from Jupiter, the Sun or the Moon also reaches that body or star.
7. **Jupiter, Sun and Moon meeting** — two or three centres (or their stars) pointing at the same star, body or number.

Then, **for every same body from step 1, say what else lands on it or uses its number**: centre lines, centre body lines, line stars, conj stars, natal Jupiter, other same bodies, circle divisions. (Aintree 15:00 6 Nov: Rubaud's same bodies were Sedna — where the Sun's and Moon's conj stars both land — Pallas and Transpluto — the Moon's two top-line bodies — and Mars, carrying the 7 that Jupiter and the Moon put on H Mercury and H Sun.)

## Part 3. Read
- For each runner, say how its pieces connect to each other, same bodies included. A runner's read is not finished until its same bodies are tied to the rest.
- Then say which runner's pieces join up the most, and how, in cells.
- No counts and no ranking by numbers of cells. Don't add conditions of your own to a flag.
- Leave out the jockey's own natal cells that come with him to every ride (e.g. a J star conj J Jupiter).
- Say what you see, without preconception.

## Part 4. Check, save, wait
- Independent checker (subagent, own code from the POSITIONS sheet, no csv) on every claim, including each "only" / "also". Apply its corrections before reporting.
- Save the blind read to the project (`claude/<course>-<hhmm>-<yyyymmdd>-blind.md`) and the repo (`docs/eddie_read/results/`, force-add the tables xlsx and the report); commit and push before the result. Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Don't say saved until committed and pushed.
- After Eddie pastes the result: show what the winner had, in the same order (same body first), cell by cell, against the field.
