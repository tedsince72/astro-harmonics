New chat: race reads, stages 1–3 (Eddie, 7 Nov 2026)
Paste this at the start of the new chat. Everything needed is here; nothing depends on earlier chats.
Where we are
Stage 1 (tools/eddie_read.py) collects every cell from the race’s tables workbook, in Eddie’s order. Which sky lines are noted (Eddie, 7 Nov 2026, from his own Haydock 19 Feb 2022 list):
a line that isn’t a conj scores 50 or more and is exact within ±120 min of the off, or scores 90 or more and is applying;
a conj scores 20 or more;
a star line at 40–50 stays only when another centre reaches the same star at 50 or more (Haydock Jupiter → Diadem 47.74, with Moon → Diadem 98.77);
a body line never comes in that way (Sun → Pluto 47.79 stays out).
On Haydock this gives exactly Eddie’s 16 lines.
Stage 2 (tools/eddie_layers.py) sets out the stage 1 data in fixed layers for every runner. It shows data only: no interpretation, no score cut-offs, no centre tags, no ranking, no pick.
L0 field check: runners in the tables workbook against the _active.xlsx.
L1 same bodies.
L2 what lands on each same body, with each source’s own sky lines.
L3 plain matches: same body on both charts, one body in both planes, runner number = sky number, circle divisions, same number in several places, N and N×φ.
L4 every natal body, with every cell on it.
Every item is tagged “only” or “also: <runners>“.
Stage 3 is the rules (built 7 Nov 2026):
docs/eddie_read/rules.json: every rule in plain words, with the races it was seen on (in_sample). Every other race is a test race.
tools/eddie_rules.py: runs every rule on a race and lists the runners each one selects, with their cells. It never reads results.
tools/eddie_backtest.py: the only script that reads docs/eddie_read/results/results.json. Per rule it gives picks, winners and 1st or 2nd, each against chance, for test races and in-sample races separately.
16 rules so far:
set A, the old register: R25, R28, R1b, R7, R26, R40, R42, R1;
set B: B1 strong-line-star filter, B2 top strong-line conj, B3 version 4, B4 same-body clear lead, B5 same body in both planes, B6 same body on both charts, B7 most sky bodies onto the jockey’s Jupiter, B8 one line star on the most natal bodies.
The full list is in rules.json; the back-test so far is in docs/eddie_read/backtest/backtest.md.
New rules are made race by race with Eddie.
What Eddie does
Uploads two files for one race: race_batch_<yyyymmdd>_<course>_<hhmm>_jupiter_tables.xlsx and ..._active.xlsx.
Pastes the result later.
What Claude does, every race, the same way
cd /home/claude/astro-harmonics && git pull (branch t24-sun-moon). If the repo is not there, attach it and clone it.
Copy both uploads into reference/classic/ under their race_batch names.
Stage 1: python3 tools/eddie_read.py reference/classic/race_batch_<...>_jupiter_tables.xlsx --out docs/eddie_read
Stage 2: python3 tools/eddie_layers.py docs/eddie_read/race_batch_<...>_eddie_read.json
Stage 3: python3 tools/eddie_rules.py docs/eddie_read/race_batch_<...>_eddie_read.json → docs/eddie_read/rules/<race>_rules.md
Send Eddie the three .md files (_eddie_read.md, _layers.md, _rules.md). If L0 shows a runner missing from the tables workbook, say so first.
Commit and push the reports before the result is pasted. Force-add the tables xlsx, because it is git-ignored.
Reading with Eddie
Show the data; don’t judge it. Answer Eddie’s questions from the reports, with every cell in full: source → chart body plane value target family (score). Copy the numbers from the report; never invent one.
Follow Eddie’s order: same body first, then sky Jupiter, Sun and Moon, then MATCH, T1 / T2, the T24 top rows and the T24 star rows (claude/race-read-instruction.md).
“Only” and “also” come from the report’s field tags. Don’t add a claim of your own without checking every runner.
A jockey’s own natal cells come with him to every ride.
Don’t add conditions or weighing of your own. Give no picks unless Eddie asks for one.
After the result
Add the result to docs/eddie_read/results/results.json (ran, first, second, finishing order, non-runners, runners not in the workbook), then run python3 tools/eddie_backtest.py. This race is a test race for every rule that existed before it.
Show what each rule selected against the result. Show what the winner had in the stage 2 report against the field, layer by layer, same body first.
If Eddie names a pattern, write it as a candidate rule in plain words, with the cells it would use. Don’t build it until he says go.
When Eddie agrees:
add the rule to rules.json, with this race and any race it was seen on in in_sample;
add its function to RULES in tools/eddie_rules.py;
rerun the rules on every race, then the back-test;
run the tests and the checker;
commit and push before the next race.
Never change a rule after a result. A change is a new rule with a new id.
A change to stage 1 or 2 changes what the rules see. Rerun stages 1–3 on every race in results.json, then the back-test, and show Eddie the back-test before and after.
Standing rules
Never open any .csv, and don’t look results up.
Wait for Eddie’s explicit go-ahead before building or changing any code. Running the scripts is fine.
After every code change, and every read that makes claims, run an independent checker: a subagent with its own code, working from the stage 1 json or the POSITIONS sheet. Apply its corrections before reporting.
Tests:
python3 tests/eddie_read_check.py (stage 1)
python3 tests/eddie_layers_check.py (stage 2)
python3 tests/eddie_rules_check.py (stage 3; about 3 min)
Don’t say something is saved until it is committed and pushed. Commit trailer: Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Race docs go in the project (claude/<course>-<hhmm>-<yyyymmdd>-blind.md) and the repo (docs/eddie_read/results/).
Background (read only if needed)
The rules of each stage: the docstrings of tools/eddie_read.py, tools/eddie_layers.py, tools/eddie_rules.py and tools/eddie_backtest.py.
Eddie’s method: claude/eddie-race-read-method.md and claude/race-read-instruction.md.
Earlier method versions and the race logs: claude/full-race-read-method.md.
The repo handover: CLAUDE.md.
