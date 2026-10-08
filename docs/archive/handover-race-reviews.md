# Handover: baseline race-by-race detail reading (UK rebuild, Phase 4)

## Standing constraint — PRESERVE VERBATIM
> **Always wait for Eddie's explicit confirmation before building or generating code or artifacts.**

Eddie's principles: we only ever SAY WHAT WE SEE and never jump to conclusions. The answer is always in the detail of the bodies, vibrations and matches, and never in general data or occurrences. The system is exact astronomy, not conventional astrology.

Other preferences:
- Eddie uses Safari and prefers PDFs over Docs artifacts for reading.
- Long-running scripts must print progress.
- Keep the explanatory analysis style.

## Working arrangement (Eddie's preferred way of working)

Two chats: an overseeing "expert" chat and a working "apprentice" chat.
- The apprentice chat reads each race and drafts the report.
- Eddie pastes the draft into the expert chat, which checks it against the source files (baseline_review.xlsx RUNNERS, the RV-1 packs, the race zip where it has one) before anything is saved.
- Only after the expert chat's go-ahead does the apprentice save the race to `claude/baseline-race-reports.md`, with the requested edits.
- So far the counts have been exact every time. The slips have been in interpretation: horse birth-year mix-ups, the Eris three-way vs equator wording, reading the TN layer for an NN pack contact, counting "possible" entries into a certain-only figure, a count that did not match its list. That is what the check is for.
- This keeps each chat's context small, and the skills and method get passed on rather than lost when a chat has to be restarted.

## PINPOINT — Eddie's key principle (30 Sep 2026)

**The keyword is PINPOINT.** Counting is a waste of time here. Counts per runner and field tallies do not find the winner. The winner is found by pinpointing the exact connection, reading by **body, family and coordinate across sky, horse and jockey**.

Worked example: original race Lingfield AW 02/04/2021 14:35, Pholas 25/1 with Hollie Doyle. On a count of Type 1 pairs Pholas ranked near the bottom. Everything below is exclusive to the winning partnership:
- **Matched convergence in the sky pair's own family and coordinate:** sky pair Jupiter/Sun is Dec Golden Ratio 86.8, and both bodies hit the horse's natal Gonggong in Dec Golden Ratio (Jupiter 93.7, Sun 80.9, both certain). This is Eddie's original Type 2.
- **Sky pair echoed exactly in a transit hit:** sky Chiron/Makemake is Dec Ninths 92.2, and the horse has TN Chiron→Makemake Dec Ninths 99.7 certain (Eddie's Type 1).
- **Horse–jockey body thread in the same family and coordinate:** the jockey has TN Chiron→Chiron self in Dec Ninths.
- NN Jupiter→Uranus Dec Ninths 98.5 certain on the horse; the jockey has an Orcus hub (self, direct and cross from Pallas, Antares and Mercury).

**Eddie's Type 1 and Type 2** (original terms; definitions still being settled):
- **Type 1:** within one qualifying sky pair A/B, the chart holds two or more of NN A↔B ("direct"), TN cross (A→B or B→A) and TN self (A→A or B→B).
- **Type 2:** sky pairs that share a body, or one sky pair whose two bodies converge, on the same natal target(s) through NN and TN, ideally in the sky pair's own family and coordinate.
- **Link:** the same body carried by horse and jockey in the same family and coordinate.

**Decisions:**
- Keep the **true node** (Eddie: more accurate to the sky). The old engine used the mean node in a mixed frame, which is why the original Sun–Ketu / Jupiter–Ketu carriers do not reappear.
- A **lower qualifying threshold** for sky pairs that carry several connections may be valid. Tiny position shifts of 0.003° tipped pairs across the 80 line (e.g. Mercury/Orcus, Orcus/Antares), so keep this in mind.

**The reading method (agreed with Eddie 30 Sep, from his notes on the three original races):**
1. **Sky pair first.** Every connection starts from a TR–TR pair A/B with its family and coordinate.
2. **Group sky pairs that share a body.** Eddie's pairs chain through a common body: Lingfield Sun–Jupiter–Ketu (+Rahu) and Pallas–Orcus–Antares–Mercury; Haydock Vesta–Pluto–Ceres–Chiron–Sedna (Pluto/Vesta, Ceres/Pluto, Ceres/Chiron, Chiron/Sedna). A pair just under 80 still counts when it belongs to a group.
3. **Mirror the pair on each chart:** NN direct A↔B, TN cross A→B / B→A, TN self A→A / B→B. The same BODIES are what matter. Family and coordinate are recorded, and a match with the sky adds weight, but a different family or a crossed coordinate does not rule a contact out (Haydock Ceres/Pluto Phi Powers/Ninths vs sky Sqrt2; Lingfield Jupiter/Ketu cross in RA on a Dec pair; Beverley Sun/Makemake RA in the sky, Dec on the jockey). Scores well below 80 count (Chiron self 49.9, 43.9, 60.5).
4. **Grade:** Type 1 = 2+ of NN / cross / self on one pair in one chart. Type 2 = grouped pairs, or both bodies of one pair, landing on the same natal body. Link = the same pair or body mirrored on horse AND jockey.
5. **Exclusivity last:** ignore "fixed" star echoes (every runner has them); mark birth-period sharing.

Worked examples: Haydock (Ishvara 40/1 / Kingscote): Regulus/Neptune Type 1 on the jockey; Chiron in Dec Ninths across the Chiron/Sedna chain. Beverley 08/06/2024 14:05 (Perfect Part 125/1 / Cam Hardie): Sun/Makemake Type 1 on BOTH horse (NN RA Ninths + cross Dec Ninths) and jockey (NN Dec Ninths + Makemake self Dec Ninths) = link, Eddie's standout; Chiron/Mercury direct (jockey) and Mercury self on both. Thread seen in all three original winning jockeys: Chiron self in Ninths (Doyle Dec, Kingscote Dec, Hardie RA).

**Natal reference time — decision NT-1 (Eddie 30 Sep: clock changes are artificial):** natal charts use 12:00 in the birth zone's STANDARD time, never summer time (UK/Ireland = 12:00 UTC all year, France = 12:00 CET, Sydney = 12:00 AEST). Engine v2.2 + charts v2.3. UK/Irish births from late 1968 to late 1971 (clocks at UTC+1 all year, legally standard time then) stay at 11:00 UTC; Eddie accepted this on 30 Sep (e.g. Joe Fanning, 1970). Before this, v2.1 charted UK/Irish summer births at 11:00 UTC, which dropped fast natal contacts Eddie saw in v2.5 (e.g. Perfect Part Mercury self Dec Whole Number 91.5 → 0). The 96 races in w48w48 and the originals must be rebuilt with v2.2 before any back-fill or recount. Note: in the active file, "possible" fast-body rows range across the whole birth day and often reach 100 in several families, so read the noon value (score_mid), not score_max.

**Reading script — `pinpoint_reading.py` v1.2 (v1.2, 30 Sep: new section G and a field-wide list — sub-80 group pairs (65–80) that share a body with a qualifying pair and are carried on BOTH horse and jockey; added after race 7, where Le Beau Garcon/Mulrennan's Pallas thread crossed to the jockey only through Mars/Pallas at 76.2. v1.1, 30 Sep: the sky-pair label now lists every family that counts; a match through a secondary family where the pair scores 65–80 is marked `~` and listed with `+` in the label, e.g. `[RA Silver Ratio 96.0; +RA Ninths 71.2]`; `**`/`*` now mean only the primary families, where the pair qualifies). Originally v1.0 (built 30 Sep, Eddie's go-ahead).** It sits next to `active_vibrations.py` (it imports its scoring, so every number is identical to the HITS sheet; each run prints "HITS check: ... all reproduced"). Run from `~/astronomy-project`:
```
python3 pinpoint_reading.py racecards/YYYYMMDD_venue/race_batch_YYYYMMDD_venue_HHMM_active.xlsx
```
It writes `<race>_pinpoint.txt` beside the chart (about 1–2 minutes per race; several files can be given at once). Options: `--sky 80 --sky-group 65 --hit 40 --nn 80 --conv 60 --conv-summary 75 --royal-only` (royal-only = Eddie's original four stars). Per partnership it prints an "ONLY ON THIS PARTNERSHIP" list, then sections A links (T1xT1 / T1 on one / link, judged against partnerships at the same level), B Type 1, C sky pair as natal pair, D self in the sky family, E hubs (one body meeting 2+ sky-pair partners through N or X; sub-80 pairs from 65 join here), F Type 2. Result last. Codes: N natal pair, X cross, S self; ** sky family+coordinate, * sky family; c/p/f certainty. It found every connection in Eddie's notes on the three originals (Doyle Chiron self and Orcus hub with Pallas/Antares/Quaoar, Pholas Jupiter/Sun→Gonggong; Kingscote Chiron/Sedna T1, Neptune/Regulus natal pair, Neptune hub, Ishvara Ceres/Chiron and Ceres hub; Perfect Part/Hardie Sun/Makemake T1xT1). Caution: EVERY partnership has some exclusive items — read which bodies and pairs, not how many.

**For each race reading from now on**, add a PINPOINT section using the method above. Check field exclusivity for each connection. Do not lead with counts.

## Where things stand (30 Sep 2026)

- The rebuild is done through Phase 4. There are 96 races (48 baseline / 48 test, split seed 20260929, never redrawn).
- RV-1 (baseline_review v1.1 + detail_packs v1.0) has been read. Notes are in the project doc `claude/rv1-detail-packs-reading.md` and in the plan doc (Claude Docs, "Upset Predictor Rebuild and Baseline Plan", section "Phase 4 result — RV-1 baseline review").
- **Current activity:** a race-by-race detail reading of the 48 baseline races, in date order. Every race is read the same way, without a favourite/outsider label. The result is shown last.
- The goal is to find, in the detail, how to tell a favourite race from an outsider race, and the runner signals.
- Eddie's note: sections 1–6 and the three-way midpoints were originally built from observed patterns (tissue-type research) before any winner-biased analysis.
- **Races 1–8 are done** (as of 30 Sep): 4 favourite races (2, 3, 5, 7) and 4 outsider races (1, 4, 6, 8). The reports are in `claude/baseline-race-reports.md`. **Add each new race there in the same format.**
- Next: the expert chat brings a check-in tally over races 1–8, then race 9 (Carlisle 14/10/2021 13:55).

## Getting a race's files

Eddie runs this from `~/astronomy-project/racecards` and uploads the zip:

```
find . -type f -name '*YYYYMMDD_*_HHMM*' -print | zip ~/Desktop/raceNN.zip -@
```

- Use date + time, not the venue: venue names in files can be longer than the 12-letter dataset key (e.g. `wolverhampton_aw` vs `wolverhampto`; Kempton races have the key `sunbury`).
- The zip should hold:
  - chart xlsx and `_active.xlsx` (in `YYYYMMDD_venue/`);
  - 10 JSON files (`w48w48/`): section1–6, three_way, alignment, race_summary, metadata;
  - 9 pipeline logs (`w48w48/logs/`) and a dataset log;
  - results txt.
- Ignore stray older files with a wrong time (e.g. `_145`, `_810`, `_205`, `_220`). These are leftovers from the old 12-hour time bug and were not used by RV-1 (it opened exactly 480 files).
- Per-runner counts: the RUNNERS sheet of `baseline_review.xlsx` (v1.1) has every count for every runner (S1–S6 unique counts, HITS, Alignment A/B/C/D, three-way). Ask Eddie to upload it once at the start of the new chat. Its header is on row 3; `race_key` = `YYYYMMDD_<venue[:12]>_HHMM`.
- RV-1 pack contacts are looked up in the HITS sheet of `_active.xlsx` (layer, from, to, mode, family). Mind the layer: pack 04 and 07 are TN, pack 09 is NN.
- The apprentice chat used two throwaway reading scripts in its session scratchpad (sky summary, clusters, S5 vs sky with exclusivity and slow/fast label, S6-TN with sky matches, Alignment B, three-way, RUNNERS rows, S2 uniques, RV-1 contacts). They are not in the project and are lost when the session ends. Making a permanent helper script is still pending item 2 below.

## Reading order for each race (the format Eddie approved)

1. **Field.** Cloth, horse (foaling date), jockey (birth year), from the META sheet of `_active.xlsx`. Look for twins and near-twins (same or close foaling date) and for birth-year groups. Note returning jockeys.
2. **Race sky** (TR_TR sheet):
   - number of pairs at 80+;
   - fast pairs (Asc/MC/Vertex/PoF; also with PoS);
   - family counts;
   - top pairs;
   - busiest bodies;
   - same-distance clusters in RA and Dec (group distances within 0.25; note Ninths centres k×100/9, and same-family clusters at other distances);
   - identities: Asc/PoF = Asc/PoS = Moon/Sun distance is one relationship, not three;
   - what carried over from the previous race.
3. **Field structure.** Twins/near-twins and what they share: S1/S2 lists, and their zero unique counts. Birth-period S2 sets that recur across races. Date-constant line and how many TN date constants are removed.
4. **Counts per partnership** from RUNNERS: S1 unique, S3 certain unique, S5, S6-NN unique, S6-TN, Alignment A/B/D/D certain. When quoting a unique S2 count, give the certain count, with the total including "possible" in brackets.
5. **Where natal meets sky:**
   - Natal repeats (S5) against sky distances: same coordinate, within 0.2. Name the pairs and the sky pairs. The S5 table has two extra columns:
     - **Exclusive on the sky?** Shared if any other chart in the race holds the same distance and coordinate, partner included.
     - **Bodies.** Fast-body when a pair includes Sun, Moon, Mercury, Venus or Mars (the pipeline's FAST set); slow when every body is a slow body or fixed star (asteroids count as slow). A slow repeat marks a birth period; a fast-body repeat is closer to a personal signature.
   - S6-TN entries (transit→natal, unique at 90+): concentrations (Polaris, Arcturus, Sirius), and body + family + coordinate ("full") matches with sky pairs.
   - Caution: transit→natal fixed star is close to the sky pair itself when the runner is young (little precession).
   - The same TN on both sides of a partnership.
   - RV-1 cross-reference: pack 04 (horse TN Transpluto→Mercury Dec Sqrt2), pack 07 (horse TN Eris→Pallas Dec Ninths), pack 09 (jockey NN Sun→Venus Dec Whole Number), plus any other pack the race appears in (e.g. 03, 05); the RV-1 lay measures; whether a pack contact is a date constant in that race.
   - Alignment B contacts: mark which are strong in BOTH charts (both ≥ 70) and near-misses.
   - Three-way and equator hits, with closeness and certainty.
6. **Field as a whole.** Spread of the counts, and where the detail differs.
7. **Result last:** finishing order and SPs. Then a short "compare with earlier races" note that lists counter-examples alongside any feature seen on winners (no winner-biased tallies).

The race 7 and 8 reports show the current format in full.

## Things to track across races (what we have seen so far, no conclusions)

- **Same-distance sky clusters** at Ninths centres: 177.78, 155.56, 144.44, 133.33, 122.22, 111.1 in RA; 11.11, 17.78, 15.56 in Dec. The slow ones carry over within a day. Dec 17.78 has been present in every race except race 2.
- **Natal repeats on sky distances, exclusive vs shared, slow vs fast-body.** Outsider winners: Madame Tantzy (both exclusive, slow), Golden Flame (both exclusive, fast-body), Graces Quest (one exclusive slow, one shared), Ropey Guest (one, shared, slow). Exclusive sky-matched repeats also occur on non-winners (e.g. Marquand's two at 0.001 in race 8, 3rd; Contact race 6; race 2's only exclusives on the last-placed partnership).
- **Birth-period markers:** RA 177.778 Alphecca–Sedna on 2017–2018 foals; the Feb-2018 S2 set (Spica/Sun, Spica/Mercury, Sirius/Pallas, Fomalhaut/Venus: Toussarok won, Papacito 2nd, Tynwald 6th); the Feb-2016 S2 set (Madame Tantzy, Chance); the Mars-declination trio (Swiss Pride, Helm Rock); Orcus–Procyon Dec 15.556 (Graces Quest, Le Beau Garcon).
- **Twins.** One twin won in races 1, 2, 3, 5 and 8; in races 4 and 7 the winner was outside every birth group. The unique measures see twins as zero.
- **Fast-pair count** by race: 17 O, 9 F, 22 F, 12 O, 14 F, 12 O, 14 F, 16 O. No ordering so far.
- **TN concentrations:** Polaris (race 1 8/21, race 5 7/20); Arcturus on four jockeys (races 3 and 6).
- **Jockeys with 3+ unique TN:** 18 charts in races 1–8, 5 won (the four outsider-winning jockeys and Moore); 13 did not.
- **Winning favourites** (races 2, 3, 5, 7): all four horses have 0 unique TN (RV-1 pack 01/02).
- **Two-sided vs one-sided** horse–jockey shared contacts. Not decisive so far (race 8 Chance/Mitchell had three and finished last).
- **Same full-match TN on both sides of a partnership:** race 2 (8th), race 3 (5th, not a sky match), race 6 (1st), race 7 (6th).
- **Date-constant exclusion hides winners:** pack 07 on Golden Flame (race 6), pack 04 on Ropey Guest (race 8).
- **Packs 07 and 09 on a winning favourite** (race 5, Dark Shift/Moore): a direct contrast with RV-1.
- **Recurring jockey signatures:** Atzeni (Sedna equator hit, Dec 17.778 repeat, Arcturus TN), Tudhope (RA 166.667 repeat on the sky in races 1, 6, 7), Marquand (3rd, 2nd, 3rd across three rides).
- **Losing-favourite (lay) signs** from RV-1:
  - unique certain TN on the favourite;
  - the favourite has the lowest unique NN;
  - "possible" declination contacts from near-fixed transit bodies (Transpluto→Mercury, Eris→Pallas, and the jockey Sun→Venus Dec Whole Number), which mark "didn't win", often second.

## Baseline races in date order (read without labels)

1. 20210825 musselburgh 1345 — done
2. 20210825 wolverhampton 2010 — done
3. 20210826 chelmsford 1530 — done
4. 20210827 goodwood 1853 — done
5. 20210903 ascot 1645 — done
6. 20210904 haydock 1420 — done
7. 20210914 redcar 1310 — done
8. 20210915 yarmouth 1520 — done
9. 20211014 carlisle 1355
10. 20211017 kempton ("sunbury") 1440
11. 20211019 exeter 1405
12. 20211019 exeter 1515
13. 20211109 newcastle 1800
14. 20211111 chelmsford 1830
15. 20211112 newcastle 1540
16. 20211126 newbury 1350
17. 20211211 newcastle 1420
18. 20211216 exeter 1415
19. 20211217 kempton ("sunbury") 1845
20. 20211218 haydock 1330
21. 20220102 newcastle 1330
22. 20220110 ludlow 1515
23. 20220121 lingfield 1350
24. 20220129 doncaster 1410
25. 20220214 catterick 1515
26. 20220215 newcastle 1640
27. 20220217 leicester 1445
28. 20220224 newcastle 1830
29. 20220318 doncaster 1440
30. 20220321 wincanton 1420
31. 20220323 haydock 1335
32. 20220325 musselburgh 1605
33. 20220406 lingfield 1425
34. 20220408 kempton ("sunbury") 1830
35. 20220412 newmarket 1645
36. 20220414 newmarket 1535
37. 20220505 chester 1330
38. 20220509 musselburgh 1550
39. 20220510 sedgefield 1500
40. 20220511 bath 1930
41. 20220602 chelmsford 1800
42. 20220603 bath 1750
43. 20220611 chester 1410
44. 20220616 ripon 1525
45. 20220707 carlisle 1630
46. 20220711 windsor 1905
47. 20220714 chepstow 1600
48. 20220716 doncaster 1845

## Pending, waiting for Eddie's go-ahead (nothing built yet)

1. **baseline_review next version:**
   - progress lines (shuffles; race loading in detail_packs);
   - mark S6-TN "certain" as a duplicate of "whole";
   - race-level measures (fast-pair count, share of runners with unique fixed-star values), field-size matched;
   - Alignment A for certain-both or above a score threshold;
   - a favourite-check sheet for both race types;
   - winner age against field age;
   - per-repeat S5 exclusivity and slow/fast-body label.
2. **Helper script** that turns a race zip into the report data (sky summary, clusters, S5-vs-sky matches with exclusivity and slow/fast label, S6-TN with sky matches, Alignment B two-sided/one-sided, three-way, RV-1 pack contacts from HITS). The apprentice's throwaway scratchpad scripts show it works; a permanent project script is not built.
3. **Date-constant exclusion:** in packs 07 and 09 it hid winners, and in race 8 pack 04 did too. Decide whether to show excluded races alongside.
4. **Later:** Gate 4 (write the D17 race call and D18 runner call from the baseline), RV-2 prediction log with D19 ruleset variants, the Phase 5 test blocks, and re-exporting the plan PDF.
5. **Suggested git housekeeping** (not confirmed): commit dataset_split.csv, the manifest, the status file and dataset.py with `git add -f`; clear the old wrong-time files.

## Superseded

The older handover (`claude/handover-baseline-review.md`, geo-scanner era, pre-rebuild) describes the old system and the old time bug. It is kept for history only.
