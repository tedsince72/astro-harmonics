# Handover — reading every runner in full detail (8 Oct 2026)

Written at the end of a long chat so a fresh chat can carry on without losing anything. Read this first, then `three-methods.md` (the method doc), then sky-dig §77 (the Doncaster re-read).

## Where we are
- Doncaster 14:40, 18 Mar 2022 has been re-read for the **winning pair only** (Olympe De Gouges 25/1 / David Noonan) with all three methods, the same-body chords, natal-to-transit numbers, the Method 1 lists and a Method 2 revisit with a wider Moon window. Pulled together in the project race summary (`claude/doncaster-1440-20220318-summary.md`, "Second read, 8 Oct 2026").
- A first control (the same measures for all ten charts) showed: totals do not separate the winner; in the 25 minutes around the race the sky bodies other than the Moon keep landing on the winning pair with them tightest (7 of 17 chords exact from off−10 to finish+10; the favourite pair 3); the Moon spreads evenly. Eddie's point (17:06): **counts flatten the texture** — comparisons must be made in texture, side by side, not by totals.
- **Next: build the tools so every runner in a race can be read the same way, then read Doncaster's ten charts, then redo the earlier races (Catterick, Ffos Las, Newcastle, Carlisle, Wincanton, Exeter) the same way, then new races.**

## Standing rules (Eddie)
- Always wait for Eddie's explicit confirmation before building or generating code or artifacts (short go-aheads count; running existing scripts body by body is fine).
- Say what you see. Don't jump to conclusions. One race at a time; layer by layer; one body at a time, then pull it together.
- "More slow may mean more strong." "The moon is the clock" — **and the Sun is equally important: just those two in that way.**
- Combinations matter more than single hits. Keep lists WIDE, not trimmed; no "top this or that"; not prescriptive.
- Midday (12:00) for every horse and jockey birth chart; no discounting for unknown birth time. **The natal Moon is left out** (it moves too far in a day).
- Lottery chart: anonymous; parked.
- Don't say something is saved until it is (this went wrong twice on 8 Oct).

## The agreed procedure (8 Oct 17:38–17:44) — for every runner, horse then jockey
Fixed settings: natal at 12:00; window off−30 min to finish+30 min; chords ≤0.15% (all three ratios in the interval list; shortest side ≥0.05°); numbers ±0.002° (kφ, k√2, whole, φⁿ, ninths; a body's own RA does not count, own Dec does).
1. **Body by body — every natal body including the natal Sun (no natal Moon):**
   - Method 1: what the body is in the chart (star strings, numbers, figures, midpoints, Dec lattice, out of bounds / stationary, links to the partner's chart);
   - Method 3: which sky bodies hold its strings and how (position on the string — inside, beyond which end, midpoint, mirror; UNISON; same body; stacks and sequences; timing through the window; who else in the field is on the string and who is tightest) — every sky body except the transit Sun and Moon;
   - Method 2: the tuned layers on that body (L1 star bases, Nodes, L2, L3, L4; who else is tuned, UNISON, same body).
2. **Then the transit Sun** across all the runner's natal bodies: its chords and holds, the strings where it is a base end (with the Moon and others), same-body chords, natal Sun → sky Sun numbers.
3. **Then the transit Moon** the same way, as the clock; and where the Sun and the Moon play the same string or each other's distances.
4. **Then the pair together:** shared strings, direct links (parallels, numbers), same-body chords (sky X + horse X + jockey X).
- Output: one **runner record** per runner, kept in full (no lost detail), with every item carrying its texture: sky body, natal body, string (base + measure), chord and deviation both sides, time and zone (before off / in race / after finish), position on the string, UNISON / same body, how many charts are on the string and who is tightest, the other sky bodies on the same string (stacks, sequences), whether the string is on the runner's Method 1 list, whether the partner is on it, parallels, numbers.
- In the chat (Eddie chose option b, 17:44): full records saved to the project; each runner taken through in the chat — the main texture body by body, and the Sun and Moon in full. Nothing dropped from the records.
- Comparing: runners side by side by kind of texture (exclusive strike at the off; one natal body struck in sequence around the race; a hub held by the Moon; the two charts meeting on one string; the Sun and Moon on the same string; a whole Method 1 figure held) — what the winner has that the others don't. Then across races.

## Tools (repo https://github.com/tedsince72/astro-harmonics — clone it, then run `bash setup.sh` to make the working folder — /home/claude in the cloud, or `ASTRO_HOME=~/astro-work bash setup.sh` on the Mac, see docs/MAC_SETUP.md)
Data
- `ledger/allpos/<RACE>__NATAL_HOURLY.csv`, `__META.csv`, `__TRANS_POS.csv` — natal positions hourly per tab (P01 horse, P02 jockey, …), race meta.
- `ledger/sky/<RACE>__SKYM.csv` — race sky by minute (scheduled −30…+30; sparse before the off). `ledger/sky_minutes.py` builds it.
- `lattice/skygrid.py RACE [HOURS]` → `ledger/skygrid/<RACE>__GRID.csv` — race sky every minute ±12 h (same engine; checked identical to SKYM). Needed for the wide windows.
- Engine: `rebuild_kit/celestial_bodies_swisseph.py` + `ephe/`. Results: `reference/profiles*.csv` (finish, SP, fav).
Method 1
- `tools/natnums.py RACE OFF DUR TAB BODY 0.002 12` and `tools/natchords.py RACE OFF DUR TAB BODY 12` (one natal body; `tools/m1d.sh BODY TAB` wraps both for Doncaster — generalise).
- `tools/cross.py RACE TAB_A TAB_B` — direct links between two charts (Dec parallels ≤0.1, numbers between every pair).
- `lattice/mlist.py RACE TAB_H TAB_J M1DIR CROSSFILE OUTDIR` — the wide Method 1 lists (each chart + combined, incl. all cross-chart chords ≤0.15%).
Method 3
- `lattice/m3d.py RACE OFF DUR BODY WIN_H WIN_J [SCFILE]` — one sky body: every star chord ≤0.15% from off−30 to off+30, dev at off−30/off/finish/off+30, exact time, every natal body of every chart on the same base (UNISON/tuned, SAME BODY), winners first with distances; whole-day list matched to the winners. `M3DUMP=file.json` dumps all rows with all holders (for comparisons). NB distances print order fixed 8 Oct (base | body–a | body–c).
- `tools/sunchords.py`, `tools/numcheck.py`, `tools/parallels.py` (per sky body; `tools/m3d.sh BODY` runs all four for Doncaster — generalise).
Method 2
- `lattice/layer1_tuned.py RACE OFF DUR`, `lattice/nodes_tuned.py …`, `lattice/layer_tuned.py RACE OFF DUR L2|L3|L4` — tuned layers. **`MOONWIN=wide`** → the Moon from off−30 to finish+30 using the skygrid (default unchanged). `lattice/against.py`, `lattice/fast_points.py`.
- `tools/m2new.py` — extracts Moon strikes outside the old window (run in the output folder).
Same-body and numbers
- `lattice/samebody2.py RACE OFF DUR WIN_H WIN_J` — sky X + horse X + jockey X (with control pairings), and natal X – sky X + third point, window off−30…finish+30, edges followed out ±12 h.
- natal → transit numbers (same body): small snippet in sky-dig §77 (Eris section) — make it a tool.
Control
- `tools/m3compare.py` — the same Method 1/3 measures for every chart (uses the M3DUMP files). Counts are background only.

## What the build should produce next (agreed, awaiting the build)
- A single runner-record builder for any race and any tab: runs the tools above for every runner (or reuses one sky pass for all runners), and writes the record in the procedure's order with every texture field.
- Generic race setup (no hard-coded Doncaster paths/times): race id, off time, duration, tabs, winner known or not.
- Records saved per race as project docs; the chat walk-through per runner.

## Findings to carry (Doncaster, winning pair) — detail in sky-dig §77
- Horse's SUN on Altair–Arcturus: Juno 14:35:17, Mars exactly at the off; her Sun tightest; almost no one else on the string (Method 1 φ + whole 120 to Arcturus).
- Noonan's NEPTUNE: all four Method 1 strings struck on the day — Sun in the race (Alkaid–Arcturus), Mercury 27 s and Sun 7.5 min after the finish (Procyon–Spica), the Moon 6 min after (Alkaid–Regulus), Mars (Capella–Rigel).
- Noonan's SEDNA (hub): Algol–Polaris held by Makemake and by the Moon from 14:36 through the race.
- Both CHIRONS on Betelgeuse–Procyon (a shared string): the Moon 14:38:22, Jupiter closing through the race.
- Transit Sun detail: Sun–Betelgeuse Dec = 75/9 exactly at the finish, the base the Moon plays in the race and 4 min after (horse Quaoar); Sun–Bellatrix (7.277 = half of Bellatrix–Rigel) played by the Moon at 14:36, the Sun at the Bellatrix–Rigel midpoint in the race (horse Pallas both); Noonan's natal Sun → sky Sun RA 1511/9 exact in the race.
- Out of bounds: Ceres and Makemake in the horses (cohort), Makemake in Noonan.
- No Eris natal-to-transit number for either (as Frankel).

## Parked / open
- Lottery chart: control charts, winning numbers, ticket moment, natal Moon in tuned layers.
- Messi blank control; Frankel control race; Queally's chart.
- The near-race measure (sky-body chords exact off−10…finish+10, who is tightest) fixed in advance and run unchanged on the other races — a check, not a ranking.
