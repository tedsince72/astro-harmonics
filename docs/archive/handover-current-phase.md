# Handover: deep race reads – current phase (2 Oct 2026)

## Standing constraint – PRESERVE VERBATIM
> **Always wait for Eddie's explicit confirmation before building or generating code or artifacts.**

Earlier stages: claude/handover-race-reviews.md (30 Sep) and claude/handover-baseline-review.md (superseded).

## CURRENT PHASE (2 Oct 2026)

**Method now:** deep race-by-race reads from the race_detail v1.3 detail sheets (charts 2.3, engine 2.2 natal 12:00 standard time, fingerprint 64612c16fe, active_vibrations v4.1). Eddie: "say what you see", "we cannot become attached to any concept so we just remain open", "generally I feel it is the combinations that find the winner which is why most measures always show as average".

**Files (Claude's workspace; lost if the session ends – the notes are in the project):**
- Detail sheets: `/home/claude/detail1/` (races 1–24, rebuilt workbooks in `/home/claude/wb1/`), `/home/claude/detail12/` (races 25–48).
- Item records: `/home/claude/reads/bv_items_1_24.csv`, `bv_items.csv` (25–48).
- Scripts in `/home/claude/reads/`: `blind_test.py` v1.0 (P20, P21, C1; holders written before results), `runner_features.py` v1.0 (one line per runner; `--compare`), `royal_record.py` v1.0 (`royal_items.csv`, `--tally`), `royal_race.py <race>` (royal items per runner), `threads.py` / `threads1.py`.
- Notes: project `claude/race-reads-1-24.md` and `claude/race-reads-25-48.md` (both up to date).
- Frozen blind holders for 1–24: `holders_1_24.csv` (md5 53b0a3d143fc0e836503041e6024b8e3).

**Reading protocol per race (outsider races done; favourite races next):** what only the winner holds; the busiest body and top-3 sky pairs (fast points left out); kind – concentrated / spread / around the busiest bodies; C2; **royal star → body for the winner and the losers** (Eddie's minimum detail); the Sun watch (Dec and RA noted); Sedna; the losers' side and the beaten favourite.

**Candidate lines (all found in-sample, none proven):**
- P21 – busiest body in an exclusive A link with `**`. Blind on 1–24: 5 of 25 won; outsiders 8 of 21 over 48.
- C2 (frozen) – outsider 9/1+ with excl_A ≥ 2 and a natal body receiving 2+ only-here sky pairs containing a busy body: 21 outsiders, 11 won.
- C3 (frozen 2 Oct, in words) – a royal sky pair landing (Type 2, only here) on natal Juno, Rahu or Sun: outsiders 19, 9 won; all runners 41, 10 won. C2 + C3: 7 outsiders, 5 won.
- Opposite side: outsiders with none of C2, C3, P20, P21 – 56 runners, 4 won.
- Outsider winners: 14 concentrated, 5 around the busiest, 5 spread. Sedna pairs land on 10 of 24. Royal amount: winner most royal in only 4 of 24 outsider races.

**Next:** deep reads of the 24 favourite races (every non-outsider race in the 48 was won by the favourite), two at a time, same protocol. Then the blind test of P21, C2, C3 when Eddie supplies fresh workbooks.

**Waiting for Eddie's explicit go-ahead (nothing built):** `race_card.py` (fixed per-runner reading card, shortlist + lay flags); adding C3 to `blind_test.py`; extending the royal record to all 22 fixed stars.


## Update 2 Oct 2026 (later)
- All 24 favourite races read with the lens "which pair, onto which body, held how" (notes in both race-reads docs).
- Count across 48: a general "held how" class (own link vs inside a chart vs landing) averages out at base. What holds: royal star as a strong own link across both charts – 32 runners, 0 won; Uranus as receiver – placed, not won, in both halves (winners 27% have a pair onto Uranus; 2nd 48%, 3rd 54%).
- **pair_body.py v1.0** (Eddie's go-ahead) in `/home/claude/reads/`: `--build` → pair_body.csv; `--tally combo|body|pair`; `--race <key>`; `--find "A/B" [--onto X]`. Single body-onto-body rows don't carry across halves – the reading has to be combinations.
- Now: second pass through the 24 outsider winners, two at a time, with pair_body (R1, R4 done).
- Second pass of all 24 outsider races done with grids (first three read, descriptive).
- pair_body.py v1.3 (gathering block) and **profile.py v1.0** (per-runner profile table, `--where`, `--winners`, `--show`) in `/home/claude/reads/`. Next: grids and profiles for fresh races, read before the result.
- **Blind test kit for Claude Code (2 Oct, Eddie: "yes lets go")** – `pinpoint_blind_kit.zip` sent to Eddie; README in project as `claude/blind-kit-readme.md`. Runs the 48 test races blind on Eddie's machine (race_detail without results → bv_record → runner_features → royal_record → pair_body grids → profile → P20/P21/C1 holders), zip back to the chat; calls written; then `score.sh` attaches results from the race CSVs and scores. Script changes for the kit: pair_body v1.4, profile v1.1, royal_record v1.1 (paths as options – outputs on the 48 baseline races verified byte-identical), new attach_results.py v1.1.
