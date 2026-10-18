# Handover — Selangor 17 Oct 2026 card, reading winners line by line (for the next chat)

Written 17 Oct 2026 at the end of a long chat. The next chat starts from this file plus CLAUDE.md. Nothing here depends on chat history.

## 1. What to do first in the new chat
1. `cd ~/astro-harmonics && git pull` (cloud session: the repo is at /home/claude/astro-harmonics; pull there).
2. Read CLAUDE.md (standing rules, families, tables), then this file, then `docs/classic/eye_notes.md` (the 17 Oct rows at the bottom of the table).
3. Python with openpyxl is enough to read the workbooks (`python3 -c "import openpyxl"`). families.py: `tools/families.py`.
4. Wait for Eddie. He will paste lines (or upload a file of lines) from one runner's sheet. Do the three steps in section 3.

## 2. The data
- Selangor (Malaysia) 17 Oct 2026, 12 races, one jupiter_tables workbook each, in `reference/selangor_20261017/`:
  `race_batch_20261017_selangor_<hhmm>_jupiter_tables.xlsx` for 1215 1245 1315 1345 1415 1445 1515 1545 1615 1645 1715 1745.
- Built by Eddie on the Mac with `run_card_swiss.py --folder racecards/20261017_selangor --skip-scrape --tables --skip-pipeline --skip-detail --skip-predict`.
- **The jockey is a dummy**: every runner has the same jockey "<cloth> DUMMY JOCKEY", dob 01-Jan-1990, birth country Great Britain
  (added so the tables tool would run; Malaysia is not in the country list). **Every J item (J Jupiter, J X, T2, T3, T4, T6, T8, T10/T11 with J,
  T21 jockey side, T23 H/J, "mutual, across charts", "both Jupiters", FIELD cells starting with "J ") is the same for every runner and means
  nothing. Read horse (H) and sky (S) only.**
- Runner sheets are P01, P03, P05 … (P = 2 × cloth − 1). POSITIONS sheet: runner, name, chart (S / H / J), point, kind (body / star), RA, Dec, rates per min.
- Also in the repo: `reference/classic/race_batch_20210802_newcastle_aw_1633_jupiter_tables.xlsx` (Newcastle AW 16:33 2 Aug 2021, real jockeys;
  winner Athmad P03 — read with the result known, see section 5).

### Results Eddie gave (scheduled time; actual off when given)
| race | winner (cloth, P##) | placed | off |
|---|---|---|---|
| 12:15 | Ari (6, P11) | 2nd Sabah Win (5, P09) | 12:23 |
| 12:45 | Fa Fa Star (1, P01) | 2nd The Star (2, P03), 3rd Outfit (6, P11) | 12:53 |
| 13:15 | Rhythm Of Zen (2, P03), favourite | 2nd Dark Moon (7, P13) | 13:23 |
| 13:45 | I'm Back (9, P17), 20-1 | 2nd Banker's Dragon (2, P03) | — |
| 14:15 | Mega Fortune (3, P05) | — | — |
| 14:45 | Pacific Energy (2, P03) | — | — |
| 15:15 | He Man (10, P19) | — | — |
| 15:45 – 17:45 | not given yet | | |

**Race time at Selangor (Eddie, 17 Oct 18:28, worked out that day):** the published race time is when they start loading the runners into
the stalls; the start is usually 7–12 minutes later. The workbooks' "off" (and every timing, TIMELINE window, "+5 min") is the published time,
so read exact times against a real start of about +7 to +12 min (12:15 → 12:23, 12:45 → 12:53, 13:15 → 13:23 where given).

All reads of these races were done before or after the result as noted in the chat; none is a blind test except where Eddie gave the result after
the read (13:45, 14:15, 14:45, 15:15 were read before their results). Do not open any csv for these races.

## 3. How Eddie wants to work now (agreed 17 Oct 2026, 17:24)
Eddie: "i paste you the lines that interest me and you note what they are and if they connect — then versus the field".
For every pasted line (or file of lines):
1. **What it is.** Table, points, plane; the raw values (value, +5, target, offset, score, arrow, timing) — find the row in the workbook and
   confirm the numbers from the cells. Copy numbers, never invent or round by hand. Say which column block is horse, which is jockey (dummy),
   which is sky (T21 rows: H block cols 3–20, J block 21–38 = dummy, S block 39–56, tag 57; T19: natal cols 4–21, sky side 22–40;
   T1: natal RA 2–9, natal Dec 10–17, SKY RA 18–26, SKY Dec 27–35, tag 36).
2. **How the lines connect.** Shared bodies; shared legs (e.g. one sky Jupiter distance d(S Jup, H Jup) carrying several natal bodies in T19);
   the same geometry seen in several tables (T13 unison = T11 midpoint = T19 "H Jupiter – H X" on 2); natal and sky both in a family on the same
   star/plane (T1 + SKY cells); links to what Eddie read in earlier winners (section 5). **Observations only — no pattern, no rule, no ranking**
   ("we cant define a pattern yet").
3. **Versus the field.** For each item, read the same row/plane in every runner's sheet of that race (raw rows, not only FIELD sheets) and give
   who else holds it and how strongly (k/n and their numbers).
- Due diligence (Eddie, 17 Oct 16:54): "when i ask questions i expect you to use due diligence and full detail in the actual raw data not
  summaries or general numbers". Answer from the raw rows; show exact detail with scores and bodies.
- Level of detail (Eddie, 17 Oct 18:10, after the Ari line-by-line read: "we need to ALWAYS use this level of detail"): every pasted line
  confirmed from its raw cells; connections traced through shared legs, shared bodies and the same geometry across tables (and lines not
  pasted that tie to them, flagged as such); for every item every runner's same row and plane read, and recomputed from POSITIONS with
  families.py when the row is not listed (filtered tables T17, T19, T21 - check T21R for royal pairs); exact numbers and scores; note the
  workbook off vs the real off for timings; independent checker before reporting, its corrections applied. Example: the Ari rows of 17 Oct
  18:00 in docs/classic/eye_notes.md.
- Fixed stars in every race (Eddie, 18 Oct 11:21: "this is really important to highlight in each race"): after the sky / horse / jockey / joins
  passes, give a separate fixed-star section — every star item scoring >= 70 for the winner (T1 / T2 star rows, T19 rows with a royal
  star, T21 horse / jockey / sky sides, T22 ratios and legs; a natal star distance and its T22 leg count once), each with the field (who
  else scores on the same item), the sky star events near the off, star joins across sky / horse / jockey, and star items shared with
  earlier winners; the per-runner count of star items >= 70 as background only (it has not separated winners). Example: Newcastle AW 16:33
  2021 (Athmad) and Selangor 13:45 (I'm Back), 18 Oct 2026.
- Families and timing with every score (Eddie, 18 Oct 17:45: "scores by themselves are not enough because some families are going to be
  more significant than others"): every hit is given as value → target number, family (and interval group for ratios), score with its
  scale (ninths linear; whole, golden, φ powers, √2, silver, conjunction and intervals squared), and applying / separating with the exact
  time ("fixed" for natal-only). Two runners are called stronger / weaker only on the same number in the same family (or both midpoint
  totals); otherwise they are listed side by side with their families. E.g. Musselburgh 13:45 2021 T3 H Jupiter → J Chiron Dec: Graces
  Quest 33.3333 (ninth, linear 70.30) vs Major Snugfit 9 (whole, squared 85.67) — different numbers, not comparable; T10 Orcus Equator
  midpoints Graces Quest 78.9 (applying, exact 26 Aug 08:55) vs Yukon 86.79 (applying, exact 26 Aug 02:16) — same kind, comparable.
- Simple standout in every race (Eddie, 18 Oct 17:47): end each race with the one thing the winner has that makes it stand out, if only
  one could be chosen (field-checked, family and timing given).
- After the work, write the observations into `docs/classic/eye_notes.md` (one table row per observation, format as the existing rows) and
  commit + push only when Eddie says (standing rules). Independent checker (subagent) on any new read before reporting, as CLAUDE.md says.
- Wait for Eddie's go-ahead before building or changing any code (running existing scripts is fine).

## 4. Rules and definitions used in the reads (all from CLAUDE.md / families.py)
- Planes RA (wrapped 0–180), Dec |ΔDec|, Equator | |Dec A| − |Dec B| | only when the points straddle the equator. Conjunction (RA < 1.5,
  Dec < 0.3) is not a family hit in Equator.
- Distance families: whole ±0.02, golden k×φ ±0.03236, φ powers, the 48 ninth ranges, √2 / silver; ratios on Eddie's interval list
  (area A 1, 3/2, 2 … 9 ±0.02 absolute; "φ and √2" 0.15 %; area B tapered).
- Midpoint (T10, T11, T17, T18, T20): closeness >= 90 % ratio half + distance half (RA ±0.5, Dec / Equator ±0.15), total = sum.
- Tables most used: T1 natal Jupiter → natal X (+ SKY cells); T5 S Jupiter → H X; T7 S X → H Jupiter; T11 natal X at the midpoint of
  S Jupiter / H Jupiter; T12 d(S Jup, S X) / d(H Jup, H X); T13 d(S Jup, H X) / d(H Jup, H X); T14 |Dec| Jupiters; T17 Jupiter equidistant
  from two bodies; T19 S Jupiter on natal pairs X–Y (three distances + ratio); T20 natal Jupiter at the midpoint of S X / H X; T21 natal
  Jupiter on natal star pairs (+ sky side); T22 a star as apex of S Jupiter / H Jupiter; TIMELINE H (off −30 / +60), LONG TIMELINE H (>= 80).
- Linear timing off → +5 min; LONG TIMELINE uses real ephemeris times beyond 60 min.

## 5. What Eddie read in the winners so far (observations, no pattern) — full rows in docs/classic/eye_notes.md
- **Newcastle AW 16:33 2021, Athmad** (real jockey Jason Hart): Neptune three-way — S Neptune → H Jupiter RA 179.456384 → 10×φ^6 (96.98),
  S Neptune → J Jupiter Dec 11.324733 → 7×φ (90.92), J Jupiter → H Neptune Dec 6.181902 → 10×φ^-1 (90.14; the only cross-chart Neptune–Jupiter
  link >= 50 in the field). Orcus line: T13 Dec 3.999225 → 4 (92.40; H Orcus 1/5 of the way from S Jupiter to H Jupiter) and T12 RA J Orcus
  2.002901 → 2 (73.09). Chiron reciprocal, both Dec: T5 12.230755 → 12.2222 (88.18), T7 2.618734 → φ² (94.47). Timing: T17 S Jupiter: J Mercury =
  J Vesta RA 99.96, exact 16:30. Eddie: "the timed events are a small part of it, maybe like a tie breaker — but there needs to be strong
  fundamentals first — like this neptune 3 way link"; "also pay attention to the bodies involved Chiron Neptune etc".
- **13:45 I'm Back** (5 rows in eye_notes): Makemake both ways (106 [99.46] 13:48, 54 [93.15] 13:51); T1 Deneb Algedi natal 18.887076 → 18.8889
  [98.69] with sky 177.778203 → 177.778 [99.97] exact 13:40 (1/10); T19 Equator rows from d(S Jup, H Jup) 4.61578: Vesta ~1, Sedna 3/2 [93.94],
  Neptune 2 [86.31]; T21 Procyon – Alphecca horse 9/4 [95.32] / sky 3 [85.60], Regulus – Rigel horse 3/2 [53.54] / sky 7/3 [93.43] exact 13:37,
  Pleiades – Antares; T7 S Venus → H Jupiter Dec 0.409791 → 0.414 [67.75] (only one in the field).
- **12:15 Ari** (7 rows): T12 RA Sun 3/2 [96.24] (1/9); T5 Mercury, Mars, Ketu, Eris; Haumea at the RA midpoint of S Jupiter / H Jupiter
  (T13 unison, T19 on 2, T11 73.67; 1/9); T19 RA rows from d(S Jup, H Jup) 142.687198: Chiron unison, Pallas 16/15, Eris 6/5, Haumea 2;
  T17 Pallas = Makemake, Mars = Neptune, Jupiter = Chiron (each Ari only); T20 Venus [95.76] (only T20 in field); T21 Arcturus – Altair 7 [99.65]
  and five more pairs; T22 Polaris 3/2 [95.15] (6/9 hold it, Ari highest).
- Bodies Eddie asked to watch: Chiron, Neptune, Orcus, Saturn (and the stars Deneb Algedi, Rigel, Regulus came up in two winners).

## 6. Things tried in the chat that did NOT separate (for reference; do not reuse as rules)
- My own "fundamentals" ranking (both-ways links, area A ratios >= 85, threads of >= 3 tables, T20): winners ranked 1st (I'm Back), 3rd
  (Mega Fortune), missed (Rhythm Of Zen, Pacific Energy, He Man).
- Star-lattice power points (sky_dig §42/§69 method, re-implemented in tools/selangor_20261017/pp.py): sky Neptune RA 2.44 is on a power point
  all afternoon; nearly every runner has a natal point on one; Neptune's star chords do not pick the winners (nep.py).
- "Same as sky" tags (same number only) in the first two races: nothing on the placed horses.
- Fixed-star counts (T21 hits >= 90 per runner): every runner has several; no separation.

## 7. Scripts from the chat (as run; read-only helpers, not frozen tools)
`tools/selangor_20261017/`: read_race.py, read_race_hj.py (extract FIELD / THREADS / TIMELINE items), fund.py, race.py, shapes.py (fundamentals,
key bodies, timed events), stars.py, pp.py, nep.py (power points). They were run against the uploaded copies; the upload prefixes map to the
repo files as 12:15 7566745e, 12:45 2673848e, 13:15 e96aa387, 13:45 afee33f2, 14:15 929b5b49, 14:45 8a883cbf, 15:15 792f2545, 15:45 49a23bd4,
16:15 4f275ecf, 16:45 61dc3d7a, 17:15 692f0455, 17:45 a6b9a230 — change the path `U=` / glob to `reference/selangor_20261017/race_batch_20261017_selangor_<hhmm>_jupiter_tables.xlsx`
before reuse. Scan output: `docs/classic/eye_scans/t1_star_natal_sky_selangor_20261017.txt`.
For Eddie's line-by-line work it is simpler to read the rows directly with openpyxl (find the runner sheet, the table code in column A, the
points in column B).

## 8. Next
- Eddie will paste lines from other winners (12:45 Fa Fa Star, 13:15 Rhythm Of Zen, 14:15 Mega Fortune, 14:45 Pacific Energy, 15:15 He Man)
  and later races. Do sections 3.1–3.3 for each, then add eye_notes rows when he says.
