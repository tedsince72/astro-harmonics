# Race-by-race reads, races 25–48 (race detail v1.1)

The new procedure (Eddie, 1 Oct 2026). Each race is read from its `_detail.txt` sheet, which covers every measure for every partnership on the 12:00 reading. For each race:
- the ways the winner won;
- in outsider races, the ways the favourite lost;
- for each line, the same thing on losers in that race.

This is what was seen, not a rule. The possibilities list at the end grows race by race.

---

## Sheet additions built: race detail v1.2 (Eddie's go-ahead, 1 Oct, 11:28)
v1.2 adds:
- `^` on items at or above their sky pair's score;
- "sky top family: yes/no" on each link;
- section 12: the old post-48 pipeline (S1–S6) run unchanged, with a field comparison for every chart (Nx tighter / +score / not in field) and the fixed stars in 3+ old sections;
- section 13: layers on the same natal body (3+ kinds).

Races 25–48 are being rerun into /home/claude/detail12. The notes below are kept as the record of what was asked for.

## Pending sheet additions (Eddie, 1 Oct, 11:13), now built as v1.2

These come from Eddie's earlier description of the method (the "tuning fork" write-up). Eddie is finding the output it was built from. Build after that, then rerun races 25–48.

1. **Same body, same family, same coordinate.** Already in the sheet as `**`; no change needed.
2. **Natal score ≥ sky score ("pre-existing").** Tag each natal-pair item (and self and cross items, if Eddie wants) with "natal ≥ sky: yes/no", next to the certain-only and royal-only tags. Examples:
   - race 25: winner's natal Arcturus→Ceres 95 against sky 96.2 (natal lower);
   - race 29: winner's natal Quaoar→Sedna 96/98 against sky 50.5 (natal higher).
3. **Layers on the same natal body (possibilities line P8).** A body table per partnership. For each natal body, list every layer that reaches it, each marked only here or shared:
   - link items, selves, natal pairs, hubs;
   - Type 2 targets;
   - three-way;
   - midpoints types 3–5.
   It's a list per body, not a score. It lets P8 be checked on losers. Eddie's old example: natal Jupiter reached by a sky Juno hit, a natal Ketu–Jupiter pair and the Pallas/Saturn midpoint.
4. **The sky's strongest family.** Tag each link "in the race sky's top family: yes/no". The sky's family split is already in the RACE SKY section.

5. **The geometric precision signal (Eddie's earlier geo_scanner method, shared 1 Oct as a diagram).** From the project notes (uk-horseracing-instructions):
   - **Horse:** a tight natal pair, a royal star with a fast or nodal body (≤0.15°), receiving 3 or more transit fast bodies at the same point; or a dense network of natal midpoints ≤0.05°.
   - **Jockey:** a near-zero fixed-star natal midpoint node (≤0.025°), with a transit fast body landing on it.
   - **Rules:** royal stars only (Aldebaran, Antares, Fomalhaut, Regulus); point bodies (PoF, Asc, MC, Vertex) left out; two ranked lists (horse and jockey), and the winner is where the tops of the two lists meet. Everything is relative, with no absolute thresholds.
   - **Example (diagram):** Oh Herberts Reign, horse Mercury·Aldebaran·Saturn 0.001°; Ryan Moore, jockey Sun·Antares·Pluto 0.001°.
   - **In our terms:** this is midpoint type 3 (natal at the midpoint of natal) plus type 5 (sky fast body at the midpoint of natal), royal stars only, ranked by distance.
   - **As seen, quick check on races 29 and 31** (both were in the old 8 training races): every chart in both fields carries a royal-star midpoint at 0.000–0.011° when all other stars are allowed in. "Equator at the midpoint of Aldebaran/Algorab" is on nearly every chart, so it's a date constant. Precision alone doesn't separate the field. The old selection rules (the star + fast-body conjunction receiving 3+ transit bodies, ranking within groups, the two-list intersection) are what picked the winner.
   - **Needed:** geo_scanner.py and UK_HORSERACING_INSTRUCTIONS.md from the earlier chat. They are not on this machine. Eddie is looking for the source output.

6. **Eddie's saved working scripts (uploaded 1 Oct):** UK_HORSERACING_PIPELINE_DOCUMENT.md, section1–6.py and active_vibrations.py v2.5. This is the 8-training-race pipeline, built on field comparison. geo_scanner.py is not in the zip. Sections 5 and 6 also need precision_reader.py, which is missing.
   - **S1, transit clusters on natal pairs.** The number of transit fast bodies (Sun, Moon, Mercury, Venus, Mars) at the midpoint of one natal pair at the same time, within 0.15°. The natal pair includes a fixed star, and star–star pairs are left out. Shown as ★5FB, ★4FB and so on. **Not in the race detail sheet.**
   - **S2, natal fixed-star conjunctions.** A star within 1.0° of a planet or node, in RA or Dec, tightest first. Tags: FAST,FIXED / FIXED / FIXED,NODAL. **Not in the sheet.**
   - **S3, natal fixed-star midpoints.** Natal body at the midpoint of two natal bodies, ≤0.1°, at least one a fixed star, star–star outer pairs left out. Tags: FAST_mid+FIXED_pair and so on. **The sheet has this as type 3, without the star filter or the tags.**
   - **S4, transit body at the midpoint of a natal pair.** ≤0.05°, a fixed star involved, point bodies in a separate [PT] list. **The sheet has this as type 5, at 0.1°.** The old document called it "the most consistent discriminator" in its first 3 races.
   - **S5, vibration repeats.** The same source→target→family→coordinate in 2 or more sky-pair rows, score ≥90, a fixed star involved.
   - **S6-NN and S6-TN, harmonic entries ≥90 with a fixed star.** Shows which entries are in the field and which are not, and reciprocals.
   - **Three-way:** the old threshold was 0.5° (the current one is 0.1°).
   - **Field comparison, the key principle.** Each entry is set against the nearest field runner's same entry:
     - for distances, the ratio ("5.8x tighter");
     - for scores, the difference ("+6.4");
     - "[not in field]" when no other runner has it.
     **The sheet only says "only here" or "also: …", with no ratio.**
   - **Fixed-star accumulation.** The same star in 3 or more sections on one chart. On the old 3 races it was on the winning horse and jockey. **Not in the sheet.**
   - **Old findings (3 races only):** S4 planetary isolation, S6-NN complete isolation, and star accumulation, on all three winners. S5, three-way and S1 varied.
   - **Running them:** they read the P_DIST tabs, which our current workbooks still have. Section 1 needs a one-line quote fix to run on Python 3.11. Sections 5 and 6 need precision_reader.py.

7. **Pipeline after the 48-race test (uploaded 1 Oct).** Kept at /home/claude/geo48.
   - **Scripts:** run_race.py and run_pipeline.py run sections 1–6, the three-way and the race summary. Also included:
     - full_race_detail.py: the unique entries per section, for every runner;
     - uk_race_predictor.py v4: ranks the field;
     - accumulation.py: patterns across races;
     - precision_reader.py: now included.
   - **Predictor v4 signal order** ("from 43 training races"):
     - PRIMARY: unique three-way cross-chart tags, unique equator tags, S6-TN non-date-constant entries;
     - SECONDARY: S6-NN count and score, S5 cross-section, S3/S4 counts, S1.
     It combines them into weighted scores (exclusive_score, depth_score) and labels the gap between first and second as CLEAR, NARROW or CONTESTED. This weighted ranking is the kind of approach PINPOINT moved away from. It is recorded here, not adopted.
   - **Tested on race 29 (1 Oct):** run_pipeline runs on our current workbooks. Sections 1–6 and the summary all completed, and full_race_detail writes its file. The three-way was skipped because it wants the raw race file. The three-way in race_detail.py can stand in for it.
   - **Possible use:** run the old sections on races 25–48 to get S1 (fast-body clusters), S2 (star conjunctions), S6-NN/TN uniqueness and the field-comparison ratios. Then fold the useful parts into the race detail sheet, reported as seen with no weighting. Waits for Eddie's go-ahead.

8. **Old format review notes (Newcastle analysis, shared 1 Oct, 12:45). How they compare with v1.2:**
   - **Already in v1.2:**
     - S1 and S2 leave out star-to-star pairs;
     - the natal Moon is flagged, not removed;
     - S4 point bodies are kept in their own [PT] list;
     - S5 and S6 date constants are stripped before unique entries are read;
     - S6-NN reciprocals are flagged;
     - the type 4 midpoint (the midpoint of two transit bodies on a natal body) is the old "Section 4B";
     - the three-way enforces both equidistance and between-ness;
     - the race-sky header has the sky pairs at 80+ and the type 2 sky midpoints at 0.1°.
   - **Gaps:**
     - S2 is listed by distance only. The notes rank by type first: FAST/FIXED, then NODAL/FIXED, then FIXED/SLOW.
     - FAST_mid + FIXED_pair entries in S3 are tagged but not pulled out on their own.
     - The race-sky header has no list of transit conjunctions ≤1.0°.
     - The three-way runs at 0.1° only. The old check also used 0.5°: at Newcastle the winner had Eris RA 0.194, Ketu and Rahu Dec 0.228 at 0.5°, and nothing at 0.1°.
     - Type 4 runs at 0.1°; the notes say ≤0.05°.
   - The notes judged S6-TN low value. It stays in v1.2 as a short entry.
   - Building the gaps waits for Eddie's go-ahead.

Caution recorded: the old description's last lines ("that horse wins", "the sky is unlocking something pre-existing") are conclusions. These measures are to see whether the features separate winners and losing favourites, not to assume they do.

---

## Standing lenses for every read (Eddie, 1 Oct, 13:30)
Keep these four running in the background of every race read:
1. **MATCH:** the same body, family and coordinate in the sky and on the chart (`**`); natal at or above the sky score (`^`); the same combination on horse and jockey.
2. **Harmonic Vibration:** the family as the carrier. Which family a body is held in across its layers, and how that family relates to the race sky's top family.
3. **Triangulation:** one body reached from three independent directions, for example a sky hit, a natal pair and a midpoint (Eddie's old Jupiter example). Also the three-way (sky, horse, jockey) and Type 1 (N + X + S on one pair).
4. **Fixed stars as AMPLIFICATION GRID:** stars read as amplifiers of a planet combination rather than signals on their own. A combination that also sits on a star (a natal star conjunction, a star at or in a midpoint, a star as the pair partner) is set against the same combination without one.

---

## Race 25 — Catterick 14/02/2022 15:15 (favourite race)
Winner: Omar Maretti / Kielan Woods, 15/8 favourite.

**Ways the winner won (as seen), with the same thing on losers in this race**
1. **Exclusive A link at 90+:** Ceres/Arcturus 96.2. It's a mirror (horse self on Ceres, jockey natal pair Arcturus–Ceres) and possible on both sides. *Losers:* Almazhar 92.2 (2nd), The Paddy Pie 96.3 (3rd), Marown 98.3 (PU), Winds Of Fire 98.5 (PU).
2. **One star in two of its three exclusive links:** Arcturus, in Ceres/Arcturus A and Pallas/Arcturus G. No other partnership has a link through Arcturus. *Losers:* not seen.
3. **Pallas self on both charts inside a link:** horse Dec Sqrt2 96p and jockey RA Sqrt2 97p, in Pallas/Arcturus. *Losers:* not seen.
4. **Exclusive G mirror:** Juno/Quaoar 74.5. *Losers:* mirrors on Almazhar, Boranha, Marown and Winds Of Fire.
5. **Certain three-way, only on this partnership:** Mars Dec, the equator at the midpoint of the sky and jockey natal positions. *Losers:* Boranha has two (Makemake, Chiron) and finished 4th.
6. **Type 2, only here:** on the horse, Neptune/Pallas → natal Vesta (96c, 97c); on the jockey, Haumea/Makemake → natal Jupiter (96c, 99c).
7. **Fast points (confirmation only):** an exclusive Moon/Pallas link at 93.3, Type 1 on the horse, on the same Pallas.

**Losers higher on the winner's bodies:**
- Ceres: The Paddy Pie, Ceres/Alkaid 96.3 against the winner's 96.2 (3rd).
- Pallas: Boranha, Pallas/Transpluto 81.7 (4th), and Almazhar, Pallas/Neptune 80.8 (2nd).

**Where the winner is lighter than the field:**
- 1 exclusive A link; Almazhar and Marown have 3.
- None of its exclusive links survive certain-only. Every other runner keeps at least one.
- 1 of 3 survives royal-only.

**Midpoint on both horse and jockey, no other chart:** none on the winner. Almazhar (2nd) has one: natal Transpluto at the midpoint of natal Haumea/Procyon, Dec.

---

## Race 26 — Newcastle AW 15/02/2022 16:40 (outsider race)
Winner: Sir Chauvelin / Paul Mulrennan, 10/1. Favourite: Onesmoothoperator / Harry Russell, 13/8, finished 2nd.

**Ways the winner won (as seen)**
1. **No exclusive link at any level (A, G or L).** Its four links (Sun/Alkaid 94.0, Venus/Polaris 93.6, Pallas/Capella 65.8, Transpluto/Betelgeuse 70.1) are all shared with 3–5 other partnerships. This is the first 9/1+ winner without an exclusive link. In races 1–24, every 9/1+ winner had at least two exclusive A links.
2. **The only midpoint in the field on both horse and jockey and no other chart:** sky Neptune at the midpoint of natal Quaoar/Sedna, Dec, certain on both charts (0.044). *Losers:* not seen.
3. **Neptune in several of the winner's items:**
   - the jockey has a Neptune hub with Quaoar and Saturn, only here (Neptune/Saturn 93.8, Neptune/Quaoar 78.0);
   - Neptune is the sky body in the both-chart midpoint above.
4. **Saturn in several items:**
   - a horse three-way: natal Saturn at the midpoint of the sky Saturn and the equator, Dec, possible, only here;
   - a jockey Saturn self via Neptune/Saturn, only here.
5. **Only-here hubs:** horse Mars with Pallas and Uranus; jockey Neptune with Quaoar and Saturn; jockey Betelgeuse with Ceres and Transpluto.
6. **Jockey selves, only here:** Haumea, Pluto, Saturn and Transpluto.
7. **Mulrennan's third win in this dataset:** races 7, 17 and 26 (the last two at 14/1 and 10/1).

**Ways the favourite lost (as seen)**
1. **It carried more links than the winner:**
   - 3 exclusive A links: Jupiter/Venus 96.0 (T1×T1), Jupiter/Sedna 89.1 and Eris/Haumea 82.1;
   - all three survive royal-only; 1 survives certain-only (Eris/Haumea);
   - only-here Type 1s on both charts, and 13 only-here hubs.
2. **A Jupiter thread:**
   - Jupiter/Venus and Jupiter/Sedna;
   - a horse Jupiter self in both;
   - a jockey Jupiter hub with Makemake, Sedna and Venus.
3. **Most of its exclusive link items carry a secondary-family or no-family match:** `~` 4 and `-` 2 of 9 items.
4. **Higher than the winner on the winner's Venus:** Jupiter/Venus 96.0 against the winner's Venus/Polaris 93.6.
5. **No midpoint on both charts. No three-way at 12:00.**

**Others:**
- Resumption (7/4, 5th) had 3 exclusive A links, all surviving both certain-only and royal-only.
- Alba Rose (14/1, last) had an exclusive A at 93.6.

---

## Race 27 — Leicester 17/02/2022 14:45 (outsider race, 4 runners)
Winner: Nelson River / Harry Bannister, 20/1. Favourite: Nickolson / Jonjo O'Neill Jr, evens, finished 2nd.

**Ways the winner won (as seen)**
1. **Two exclusive A links, both through Uranus:** Ceres/Uranus 92.9 (mirror) and Rahu/Uranus 86.2.
   - Both are certain on each side and both survive royal-only.
   - The only other links through Uranus are Uranus/Alkaid 68.9 G, held by Fransham (PU) and the favourite.
2. **A jockey self inside an exclusive link:** Rahu self (RA Ninths 65c) in Rahu/Uranus. The same jockey Rahu self is carried by four other sky pairs, including Rahu/Algorab 99.2, a Type 1 only here.
3. **No three-way, and no midpoint on both charts.**
4. **Fast points (confirmation only):** jockey Type 1s on Juno/Ascendant (only here) and Uranus/Ascendant (also on the favourite's horse), and a jockey Ascendant hub with Juno and Uranus (only here).

**Ways the favourite lost (as seen)**
1. **Both of its exclusive A links drop under certain-only:**
   - Mercury/Venus 92.6 (mirror), possible on each side;
   - Mars/Fomalhaut 81.4, a jockey Type 1 holding a royal star, possible on the jockey side.
   - Both of the winner's exclusive A links stay.
2. **More exclusive links overall than the winner:**
   - 2 A, 3 G and 2 L, against the winner's 2, 0 and 1;
   - 10 of its 15 exclusive link items are Ninths.
3. **A certain three-way only it carries:** Haumea Dec, horse natal at the midpoint of the sky and jockey positions. The winner has none.
4. **On Uranus, the winner's body, it is lower:** 68.9 G against the winner's 92.9 A.

**Others:** Stepney Causeway (2/1, 3rd) had the most of everything: 7 exclusive A links, the highest at 98.9, and 8 of its 9 exclusive links survive certain-only.

---

## Race 28 — Newcastle AW 24/02/2022 18:30 (favourite race, 5 runners)
Winner: Gowanlad / Phil Dennis, 2/1 favourite.

**Ways the winner won (as seen)**
1. **One exclusive A link:** Quaoar/Algol 84.3, the same cross (Quaoar→Algol, RA Sqrt2) on both charts, certain on both.
   - Alablaq (5th) is higher on Quaoar: Quaoar/Sedna 88.8.
2. **One exclusive G link:** Sun/Orcus 75.5, a jockey Type 1 with an Orcus self inside it. No other partnership has a link through Sun or Orcus.
3. **Every item on its exclusive links is a full match (`**`), 5 of 5, all RA.**
   - The other winners so far: race 25, 3 of 8; race 27, 2 of 4.
4. **No three-way and no midpoint on both charts.**
   - Losers here with a certain three-way: James Watt (Neptune, only; 4th) and Blazing Hot (Eris, shared with James Watt; 2nd).
5. **Smaller than some losers on links:** Alablaq had 4 exclusive A links (5th), and Tathmeen had 2, the highest at 93.0 (3rd).

---

## Race 29 — Doncaster 18/03/2022 14:40 (outsider race, 5 runners)
Winner: Olympe De Gouges / David Noonan, 25/1. Favourite: Oot Ma Way / Conor O'Farrell, 5/6, finished 2nd.

**Ways the winner won (as seen)**
1. **No exclusive A or G link.** This is the second outsider winner without one (race 26 was the first). Its A and G links (Transpluto/Spica 93.0, Transpluto/Algol 85.0, Jupiter/Polaris 75.4, Transpluto/Arcturus 69.2) are all shared.
2. **Two exclusive L links (50–65):**
   - Quaoar/Sedna 50.5: a natal pair on both charts (horse RA Ninths 96c, jockey Dec Ninths 98c), certain on both;
   - Mercury/Regulus 57.2: a mirror, possible on both sides.
3. **Type 1s only it has:**
   - on the horse, Chiron/Transpluto 99.5, the second-highest pair in the race (the top was Gonggong/Algol 99.7; corrected 1 Oct). The horse cross Chiron→Transpluto is 90c `**` and the Transpluto self 89p `**`. No other runner carries this pair as a link or Type 1;
   - on the jockey, Pallas/Sedna 96.0, Sedna/Arcturus 94.9, Venus/Altair 81.8 and Eris/Mars 81.4.
4. **Sedna through several of the jockey's items:** the Pallas/Sedna and Sedna/Arcturus Type 1s, a Sedna hub with Arcturus and Pallas, and the Quaoar/Sedna L link.
5. **Jockey selves, only here:** Mars (RA Golden Ratio 95p, Dec Ninths 49p) and Venus (Dec Silver Ratio 88p). Horse selves: Transpluto (89p) and Venus.
6. **A certain three-way:** Eris Dec, the sky Eris at the midpoint of the horse's natal Eris and the equator. Suntory Star (80/1, 5th) has the same.
7. **No midpoint on both charts.** None in the field.

**Ways the favourite lost (as seen)**
1. **Both exclusive links are natal pairs on both charts, possible, and both drop under certain-only:**
   - Ceres/Jupiter 83.1 A;
   - Jupiter/Bellatrix 73.9 G.
   All 4 items have no family match (`-`).
2. **No selves anywhere, no Type 1 that only it has, and no three-way.**
3. **Hubs on Jupiter and Ceres on both charts**, only here.
4. **Higher than the winner on Jupiter:** Ceres/Jupiter 83.1 A against the winner's Jupiter/Polaris 75.4 G.

**Others:**
- Poetria (15/8, 3rd) had 5 exclusive A links, the highest at 96.0.
- Suntory Star (80/1, 5th) had 2 exclusive A and 4 G links.

---

## Race 30 — Wincanton 21/03/2022 14:20 (outsider race, 6 runners)
Winner: River Bray / Alan Johns, 22/1. Favourite: Ballyblack / Rex Dingle, 10/11, finished 3rd.

**Ways the winner won (as seen)**
1. **Exclusive A link Rahu/Makemake 82.9, T1×T1.** On the horse, a cross plus a Makemake self. On the jockey, a natal pair, a cross, a Rahu self and a Makemake self. Certain on each side, and it survives royal-only.
2. **Makemake self on both charts inside that link.**
3. **Makemake through several items:**
   - a horse Type 1 Pluto/Makemake 96.3, only here;
   - a horse Makemake hub with Pluto and Rahu;
   - the L link Neptune/Makemake 60.7 (horse Neptune self, jockey Makemake self, only here).
4. **Rahu through several items:** a jockey Rahu self and Rahu hubs on both charts, only here.
5. **Second exclusive A link Ceres/Jupiter 81.0:** jockey Ceres self 95p. It drops under certain-only.
6. **Selves only here:** 10 in all (4 on the horse, 6 on the jockey).
7. **No three-way, and no midpoint on both charts.**

**Ways the favourite lost (as seen)**
1. **Exclusive A link Mars/Transpluto 94.6, a Transpluto self on both charts.** This is the same shape as the winner's Makemake link. It drops under certain-only, because the horse side is 74p.
2. **Second exclusive A link Ketu/Neptune 81.7, a mirror.** It survives both certain-only and royal-only.
3. **Every item on its exclusive links is Phi Powers (4 of 4).**
4. **It has the only midpoint in the field on both charts and no other chart:** natal Transpluto at the midpoint of natal Haumea/Procyon, Dec, certain on both.
   - **This is the same configuration Almazhar had in race 25** (2nd at 5/1).
5. **Higher than the winner on Transpluto:** Mars/Transpluto 94.6 A against the winner's Transpluto/Spica 71.8 G.
6. **Fast points (confirmation only):** an exclusive Polaris/Ascendant link at 86.9.

**Others:**
- Birds Of Prey (10/1, 4th) is higher on Makemake (Gonggong/Makemake 95.1), and all 5 of its exclusive links survive certain-only.
- Electric Annie (9/2, 5th) had the highest exclusive A link in the race, 99.4.

---

## Race 31 — Haydock 23/03/2022 13:35 (favourite race, 5 runners)
Winner: Soldier Of Destiny / Gavin Sheehan, 13/8 favourite.

**Ways the winner won (as seen)**
1. **No exclusive A link.** Its three A links (Haumea/Polaris 96.5, Transpluto/Alphecca 95.9, Neptune/Alkaid 95.1) are shared with 2–3 others.
2. **Three exclusive G links, mostly Ninths (6 of 7 items):**
   - Saturn/Vesta 73.0: the same natal pair (Saturn→Vesta RA Ninths 61c) on both charts, plus a horse Vesta self (87c);
   - Chiron/Antares 70.7: a mirror, with a horse Chiron self;
   - Neptune/Makemake 70.1: a jockey Makemake self.
3. **Neptune/Makemake was also an exclusive link on the race 30 winner** (L, 60.7).
4. **Makemake and Neptune through several items:**
   - the jockey Makemake self sits in two links (Neptune/Makemake and Mercury/Makemake);
   - the horse has a Neptune hub with Algorab, Alkaid and Makemake, only here.
5. **Four exclusive L links.** The jockey has 10 hubs only here, and a Type 1 Venus/Vesta 98.3, only here.
6. **No three-way, and no midpoint on both charts.**

**Others:**
- Dreams Of Home (9/2, 3rd) had an exclusive A at 96.2.
- Ubetya (7/2, 4th) had 2 exclusive A links, the highest at 95.1.
- Burrows Diamond (16/5, 2nd): none of its 3 exclusive links survive certain-only.

---

## Race 32 — Musselburgh 25/03/2022 16:05 (favourite race, 7 runners)
Winner: Hold Onto The Line / Alan Doyle, 100/30 favourite.

**Ways the winner won (as seen)**
1. **No exclusive A link.** It shares Venus/Quaoar 99.2 with Garde Des Champs (7th): a natal pair on both charts, possible. It also shares Transpluto/Bellatrix 99.2 with the field.
2. **One exclusive G link:** Haumea/Polaris 70.9, a jockey Type 1 with a Haumea self. All 3 items are full match, Phi Powers, RA.
3. **The only midpoint in the field on both horse and jockey and no other chart:** sky Eris at the midpoint of natal Jupiter/Pallas, Dec, certain on both (0.004).
   - **The race 26 winner had the same kind:** a type 5, the only one in its field.
4. **A certain three-way, only here:** Jupiter Dec, the jockey's natal Jupiter at the midpoint of the sky and horse positions. Jupiter is also in the both-chart midpoint.
5. **Neptune on the horse:**
   - two Type 1s only here: Neptune/Betelgeuse 93.1 and Neptune/Sun 82.7;
   - a Neptune self;
   - a Neptune hub with Betelgeuse, Spica and Sun.

**Others:**
- Balranald (11/1, 6th) had 2 exclusive A links, the highest at 99.2, and all 3 of its exclusive links survive certain-only.
- Petite Rhapsody (9/2, 2nd) had 2 exclusive A links, the highest at 93.7.
- Sky Eris also shows in the three-ways of Brandy McQueen (4th) and Keep The Faith (5th), shared between the two.

---

## Re-read on race detail v1.3 (from 1 Oct, 13:20)
Each race is read again with every measure against every runner: what only the winner has, what it shares with losers, and where losers show more. In outsider races, the beaten favourite is read the same way.

### R25 Catterick 14/02, v1.3 (favourite race; Omar Maretti / Kielan Woods won at 15/8)
- **Only the winner has / stands out:**
  - The most selves only here in the field: 7 of 7 on the horse and 3 of 4 on the jockey, 10 in all. Losers have 4–6.
  - Pallas reached by 6 kinds of layer on the horse (link G, self, hub, midpoints, old S3/S4).
  - A certain three-way only it carries (Mars Dec, at 0.1°). Boranha (4th) has two.
- **Shared with losers:**
  - Old S3, S4 and S6-NN: every chart has most entries not in the field.
  - Fast body at a star-pair midpoint (S3F): every chart has 3–9, all not in field.
  - Fixed stars in 3+ old sections: 7–11 per chart.
  - Bodies reached by 5+ layer kinds: every runner.
- **Losers show more:**
  - Exclusive A links: Almazhar 3 and Marown 3, against the winner's 1.
  - Highest exclusive A: Winds Of Fire 98.5, Marown 98.3.
  - Three-way in the 0.1–0.5° band: losers have 1–4 that only they carry; the winner has none (only a shared Eris).
  - Certain-only: the winner keeps 0 of 3 links; every loser keeps at least 1.
  - Midpoint on both charts: only Almazhar has one (2nd).

### R26 Newcastle 15/02, v1.3 (outsider race; Sir Chauvelin / Paul Mulrennan won at 10/1; the favourite Onesmoothoperator, 13/8, finished 2nd)
- **Only the winner has / stands out:**
  - The only midpoint in the field on both horse and jockey (sky Neptune at the midpoint of natal Quaoar/Sedna, certain on both).
  - No exclusive link at any level. Every loser has at least 1.
  - The fewest bodies reached by 5+ layer kinds: none on the horse, 1 on the jockey (Betelgeuse). The favourite has 8 such bodies across its two charts, Alba Rose 6.
  - The horse's old S4 entries are all not in the field (15 of 15). So are Wise Eagle's (15 of 15).
- **Shared with losers:**
  - Old S3 and S3F: everyone is mostly not in field.
  - Old S6-NN: nearly all unique for everyone.
  - Fixed stars in 3+ old sections: 6–11 per chart.
- **Losers show more:**
  - The favourite: 3 exclusive A links (96.0 T1×T1), 13 only-here hubs, and Makemake reached by 7 layer kinds on the jockey.
  - Three-way at 0.1°: Alba Rose (Jupiter, certain) and Aced It (Eris, certain). The winner's is possible only (Saturn).
- **The favourite lost with:**
  - the most layers and links in the field;
  - only 1 of 9 exclusive items at or above its sky score;
  - only 1 of 3 exclusive links surviving certain-only;
  - no three-way at 12:00 (its 0.1–0.5° Mars has a between-ness error of 0.443).

### R27 Leicester 17/02, v1.3 + combinations (outsider race, 4 runners; Nelson River / Harry Bannister won at 20/1; the favourite Nickolson, evens, was 2nd)
**Race sky:**
- Top family Ninths (29%), then Phi Powers (21%).
- Busiest bodies: Mars (9), Rahu (7), Quaoar (7).
- Top pairs: Sedna/Arcturus 99.8 (Dec Phi Powers, RA Ninths), Mars/Rahu 99.5 (Phi Powers), Rahu/Algorab 99.2 (RA Ninths).

**Winner, bodies and vibrations (as seen):**
- **Jockey, Rahu in Ninths (top family; Rahu is the 2nd-busiest sky body):**
  - a Rahu self (RA Ninths 65c `**`), carried by Rahu/Algorab 99.2 (the #3 sky pair) and the exclusive link Rahu/Uranus 86.2;
  - a natal pair Rahu–Algorab (Dec Ninths 74c), making Rahu/Algorab a Type 1 only here;
  - triangulation: reached by sky hit, natal pair and midpoint (3 directions); star partner Algorab.
- **Jockey, Arcturus–Sedna in Ninths:** a natal pair (Dec Ninths 76c) on Sedna/Arcturus 99.8, the #1 sky pair.
- **Horse, Uranus (the thread of both exclusive A links):**
  - Ceres–Uranus natal pair in Golden Ratio 81c (the sky pair is Phi Powers, so no family match);
  - Rahu→Uranus cross in Ninths 80c;
  - 3 directions.
- **Horse, Sqrt2 group:** a Saturn–Sirius natal pair (RA Sqrt2 86c `**`) on Saturn/Sirius 94.0, unique to the winner. Jupiter and Spica are also held in Sqrt2 (hub, natal pair).
- **Every one of the winner's link, Type 1, natal-pair and self items is certain.**

**Beaten favourite (Nickolson), as seen:**
- **Jockey, Fomalhaut (royal) in Phi Powers on 5 kinds of layer** (Type 1, hub, link, natal pair, S6-NN) through Mars/Fomalhaut.
- **Jockey Mars on 7 layer kinds.** Mars is the busiest sky body.
- Its two exclusive A links drop under certain-only.
- A certain three-way only it carries (Haumea).

**Others:** Stepney Causeway (2/1, 3rd) has 24 race-unique combinations, mostly Phi Powers. Quaoar, Venus and Vega appear on both charts.

**As seen across the lenses:**
- The winner holds two of the top three sky pairs in the top family (Ninths) through the jockey.
- The favourite holds the busiest body (Mars) and a royal star in the second family (Phi Powers).
- Stepney is full of Phi Powers.

### R28 Newcastle 24/02, v1.3 + combinations (favourite race, 5 runners; Gowanlad / Phil Dennis won at 2/1)
**Race sky:**
- Top family Ninths (29%), then Sqrt2 (22%) and Silver Ratio (21%).
- Busiest body: Quaoar (10), then Makemake (8) and Mars (7).
- Top pairs: Sun/Aldebaran 99.7, Quaoar/Transpluto 99.6 (Ninths), Mercury/Makemake 99.5.

**Winner, bodies and vibrations (as seen):**
- **Exclusive link Quaoar/Algol 84.3:** sky Quaoar (the busiest body) crosses natal Algol in RA Sqrt2 on both charts (horse 87c `**`, jockey 93c `**`). The same body, family and coordinate on both charts, certain on both.
- **Its other links all reach natal stars too:**
  - Neptune→Algol in Whole Number 71/98c `**`;
  - Transpluto→Altair, →Rigel and →Regulus in Golden Ratio and Phi Powers, all `**` and certain.
  These are shared with the field. Seen through the star-grid lens, the winner's links are a sky body striking natal stars on both charts.
- **Exclusive G link Sun/Orcus 75.5 (Whole Number):** a jockey Orcus self, 40c `**`.
- **Few combinations of its own:** 2 (Alkaid Whole Number, Arcturus Silver Ratio).
- **Horse:** a Juno/Pallas Type 1 96.4 in Golden Ratio (possible), and a Pallas self.

**Others, as seen:**
- Tathmeen (3/1, 3rd): 10 combinations, with jockey Transpluto in Golden Ratio on 5 kinds of layer.
- Blazing Hot (18/5, 2nd): horse Rigel in Whole Number on 4 kinds.
- Alablaq (7/2, 5th): three combinations in the top family Ninths (Algol, Chiron, Polaris), and 4 exclusive A links.

**Repeat noted:**
- R25: the winner's Pallas in Sqrt2 is on both charts, and Pallas is a busy sky body.
- R28: the busiest sky body, Quaoar, hits natal Algol in Sqrt2 on both charts.
- R27: the winner's jockey Rahu (the 2nd-busiest body) is in the top family.
- To check across all 24: a busy sky body carrying one family on both horse and jockey.

**Check of the R28 repeat across all 24 races (as seen):**
- A body + family on both horse and jockey, carried by no other runner (any vibration layer): 71 runners have one, and 8 of them won (11%). Of the 66 runners without one, 14 won (21%).
- With a busy sky body in it: 2 of 6 won (R25, R44).
- So it doesn't separate winners. The same feature sits on many 2nd and 3rd placers.

### R29 Doncaster 18/03, v1.3 + combinations (outsider race; Olympe De Gouges / David Noonan won at 25/1; the favourite Oot Ma Way, 5/6, was 2nd)
**Race sky:**
- Top family Ninths at 44%, the highest share among the 24 races.
- Busiest bodies: Chiron, Vesta (8 each).
- Top pairs: Gonggong/Algol 99.7, Chiron/Transpluto 99.5, Gonggong/Spica 98.5, Chiron/Altair 98.5.

**Winner, bodies and vibrations (as seen):**
- **Jockey, Sedna in Ninths (the top family), all certain:**
  - a Sedna self (RA Ninths 91c `**`/`*`) in two Type 1s only it has: Pallas/Sedna 96.0 and Sedna/Arcturus 94.9;
  - a natal pair Arcturus–Sedna (Dec Ninths 83c);
  - triangulation: 3 directions.
- **Sedna in Ninths on both charts:** the L link Quaoar/Sedna is a natal pair in Ninths on horse (96c) and jockey (98c).
- **Horse, Transpluto in Whole Number:** a Type 1 on Chiron/Transpluto 99.5 (the #2 sky pair). The cross Chiron→Transpluto is 90c `**`, with a self at 89p. Chiron is the busiest sky body.
- **Jockey:** a Mars self in Golden Ratio 95p (Eris/Mars Type 1), and Venus/Altair in Silver Ratio. These are possible only.

**Beaten favourite, as seen:**
- Its exclusive links are Ceres/Jupiter and Jupiter/Bellatrix. They are natal pairs in Sqrt2, Whole Number and Golden Ratio, with no family match to the sky pair (`-`) and mostly possible.
- None of its only-here link, Type 1, natal-pair or self items is in Ninths (0%).

**Repeat seen:**
- A natal pair Sedna–Arcturus on the winner's jockey in R27 (Ninths 76), R28 (Sqrt2 91) and R29 (Ninths 83). These are three winners in a row; the sky pair Sedna/Arcturus is in every race from February to April.
- 11 runners carry it in all, so 3 of 11 won.
- The losers carrying it: R25 Bewley 4th and Paddy Pie 3rd; R26 Marquand 5th (Sqrt2); R31 Frost 4th; R32 Wadge 2nd; R33 Marquand 3rd, Burns 5th, Haynes 4th.

### R30 Wincanton 21/03, v1.3 + combinations (outsider race; River Bray / Alan Johns won at 22/1; the favourite Ballyblack, 10/11, was 3rd)
**Race sky:**
- Top family Ninths (37%).
- Busiest bodies: Moon, Regulus (6 each), then Makemake (5).
- Top pairs: Sun/Quaoar 99.4 (Ninths, Sqrt2), Chiron/Algorab 99.1, Orcus/Sirius 98.6.

**Winner, bodies and vibrations (as seen):**
- **Makemake (3rd-busiest sky body) on both charts:**
  - horse Makemake in Dec Sqrt2 (Rahu→Makemake 75c `**`, Makemake self 60c `**`, Pluto/Makemake Type 1 96.3);
  - jockey Rahu–Makemake natal pair RA Ninths 91c, plus a Makemake self (Ninths/Phi Powers).
  - The exclusive A link Rahu/Makemake is T1×T1. Every item is certain except the jockey's Sqrt2 Rahu items.
- **Horse, Neptune in Ninths:**
  - a self 88c `**`;
  - a Neptune/Transpluto Type 1 84.8 (Transpluto 89c `**` in Ninths);
  - the L link Neptune/Makemake.
- **Horse:** Jupiter–Capella in Silver Ratio 96p `**` (a Type 1, possible).

**Beaten favourite, as seen:**
- Phi Powers carries it (15% of the sky): a Transpluto self on both charts (Mars/Transpluto 94.6) and Ketu/Neptune in Phi Powers.
- Its Ceres–Haumea (Ninths 95) and Haumea–Regulus (Whole Number 96) natal pairs have no family match (`-`).

**Check across all 24 races:** the share of each runner's only-here link, Type 1, natal-pair and self items in the race sky's top family. Ninths is the top family in every race.
- Winners 41%, beaten favourites 37%, others 40%. No difference overall.
- Winner against beaten favourite: the winner is higher in 7 of 12 outsider races.

### R31 Haydock 23/03, v1.3 + combinations (favourite race, 5 runners; Soldier Of Destiny / Gavin Sheehan won at 13/8)
**Race sky:**
- Top family Ninths (39%), then Sqrt2 (18%).
- Busiest bodies (not counting fast points): Sun, Vesta (7 each), Mars, Neptune and Transpluto (6 each).
- Top pairs: Mars/Betelgeuse 99.5 (Ninths), Pallas/Sun 99.4, Sun/Vesta 99.4 (Sqrt2).
- Tightest sky conjunction: Bellatrix/Chiron, Dec 0.007.

**Winner, bodies and vibrations (as seen):**
- **Vesta in Ninths on both charts (Vesta is a busy body, and Sun/Vesta is the #3 pair):**
  - the natal pair Saturn→Vesta in RA Ninths 61c `**`, identical on horse and jockey;
  - a horse Vesta self (RA Ninths 87c `**`), reached from 3 directions;
  - star grid: Aldebaran within 0.376° Dec of the horse's natal Vesta. On the horse, natal Altair sits at the midpoint of natal Juno/Vesta (0.010).
  - The jockey also has the Venus/Vesta Type 1 98.3: a natal pair in Ninths (86p, `-`) and a cross in Sqrt2 (64c `**`).
- **Horse, Chiron in Ninths:** a self (79c `**`) carried by Chiron/Algorab 92.5 and the G link Chiron/Antares (royal).
- **Horse, Neptune in Ninths:** Makemake→Neptune 80c `**` (G link Neptune/Makemake), and Neptune is a busy body.
- Almost every item is certain. The jockey's Venus–Vesta and Juno–Uranus natal pairs are possible.

**2nd, Burrows Diamond (16/5), as seen:**
- Carried by Golden Ratio (Pallas–Regulus 86p, a `~` secondary match) and Silver Ratio (Rahu–Polaris 98p, Uranus–Vesta). Mostly possible, mostly with no family match (`-`).
- It holds the #1 sky pair Mars/Betelgeuse as a natal pair (Ninths 82p `*`).

### R32 Musselburgh 25/03, v1.3 + combinations (favourite race, 7 runners; Hold Onto The Line / Alan Doyle won at 100/30)
**Race sky:**
- Top family Ninths (29%), then Phi Powers (17%) and Sqrt2 (16%).
- Busiest bodies (not counting fast points): Pallas, Neptune and Chiron (7 each), then Ketu and Uranus.
- Top pairs: Ceres/Aldebaran 99.3 (Conjunction; also the tightest sky conjunction, RA 0.004), Venus/Quaoar 99.2 (Ninths), Transpluto/Bellatrix 99.2.

**Winner, bodies and vibrations (as seen):**
- **Horse, Neptune (a busy body) in RA/Dec Sqrt2:**
  - the Neptune/Betelgeuse Type 1 93.1: a natal pair Neptune–Betelgeuse 71c `**` and a Neptune self 40c `**`;
  - the Neptune/Sun Type 1 82.7: a Sun self 68p `**` and a cross;
  - reached from 3 directions;
  - star grid: the star partner is Betelgeuse; natal Rahu sits at the midpoint of natal Castor/Neptune (0.004).
- **Horse, Venus–Quaoar in Dec Ninths 92p `**`** on the #2 sky pair Venus/Quaoar 99.2, in the top family. The jockey carries the same pair in Sqrt2 (`-`); Garde Des Champs (7th) shares the pair.
- **Horse, Chiron–Transpluto in Ninths 68c `**`.**
- **Jockey, Haumea in Phi Powers:** the G link Haumea/Polaris, with a self at 71c `**`.

**2nd, Petite Rhapsody (9/2), as seen:**
- **Jockey, Neptune in Ninths:** the Neptune/Algorab and Neptune/Makemake Type 1s, and a self at 86c, all certain.
- **Jockey, Sedna in Ninths:** the Sedna/Arcturus Type 1 (natal pair in Silver Ratio 90c, self 73c `**`).
- So the runner-up has a busy body (Neptune) held as a self inside Type 1s too, in the top family.

**Check (all 24 races):** a busy sky body held as a certain self inside a Type 1 or link, in the same family, reached from 3 directions.
- 51 runners have it, and 9 won (18%). Of the 92 without it, 15 won (16%).
- So it doesn't separate. Winners with it: R25, R27, R30, R31, R32, R41, R42, R44, R47.

**Note on method:** each winner thread picked out by eye so far has turned up on about a third of the runners, at the base win rate. Reads need to go one step deeper: set the winner's thread directly against the same kind of thread on each loser (score, certainty, match, layers, stars, triangulation), so the difference between them is what gets recorded.

**Thread against thread (threads.py, from R31):** a thread is a self plus at least one other layer, on one body in one family on one chart. Each runner's threads are set side by side: kinds of layer, best score, share certain, `**` count, only or shared, triangulation, stars, sky pairs.
- **R31:** the winner's three threads (Vesta, Chiron and Makemake, all Ninths) are all 100% certain. The runner-up's Venus threads are 0% certain. The 3rd, Dreams Of Home, has the strongest-looking thread in the field (jockey Rahu Sqrt2: 4 kinds, best 100, 7 `**`, certain, only here).
- **R32:** the winner's Neptune Sqrt2 thread has 4 kinds, is 100% certain, has 4 `**`, is only here, reaches 3 directions and has the star Betelgeuse. The runner-up's Neptune thread is in Ninths and certain but shared. Its Sun Ninths thread (5 kinds) is 0% certain.
- **Check across all 24 races:** runners whose threads are all fully certain won 6 of 25 (24%). Others won 18 of 113 (16%). That's a lean, but on small numbers.

### R33 Lingfield 06/04 (outsider race; Man On A Mission / Luke Morris won at 12/1; the favourite Judy's Park, 13/8, was 2nd)
**Race sky:**
- Top family Ninths (30%), then Golden Ratio (19%).
- Busiest body: Pallas (9), then Haumea, Ketu and Jupiter.
- Top pairs: Chiron/Procyon 99.6 (Ninths), Sun/Altair 99.4, Venus/Algol 99.1.

**Winner's threads (as seen):**
- **Horse, Uranus in Ninths (top family):** Type 1, natal pair and self; best 83; 100% certain; 4 `**`; only here; 3 directions. Its sky pair is Uranus/Alphecca 83.4, with the star Alphecca as partner.
- **Horse, Pluto in Whole Number:** 4 kinds (Type 1, Type 2, natal pair, self); best 93; 100% certain; 4 `**`; shared. Star Alphecca again (Pluto/Alphecca 81.5).
- **Jockey, Sedna in Ninths:** a self in the A link Jupiter/Sedna, also on Sedna/Arcturus 80.2; 100% certain. This is a Sedna self, not the Arcturus–Sedna natal pair.
- **Jockey:** Gonggong in Golden Ratio (Pallas/Gonggong Type 1 97.2, certain, only here), and Mercury in Ninths (possible).
- **Star grid:** Alphecca is the partner in both horse threads.

**Beaten favourite (2nd), as seen:**
- **Its two biggest threads are both on the horse and almost wholly possible:**
  - Pallas (the busiest body) in Whole Number, 5 kinds, 0% certain (star Algol);
  - Mercury in Ninths, 5 kinds, 11% certain.
- Its only fully certain thread is Makemake in Phi Powers (2 kinds, shared).

**Others:** Bang On The Bell (3rd) has jockey Chiron in Ninths on the #1 sky pair Chiron/Procyon 99.6 (certain, shared).

### R34 Kempton 08/04 (favourite race; King Francis / David Egan won at 5/4)
**Race sky:**
- Top family Ninths (39%), then Phi Powers (17%).
- Busiest bodies: Juno (9), Vesta (8), Haumea (7).
- Top pairs: Vesta/Procyon 100.0 (Sqrt2), Juno/Pleiades 99.8, Jupiter/Alkaid 99.6, Vesta/Sedna 99.6.

**Winner's threads (as seen):**
- **Jockey, Ceres in Ninths:** Type 1, link A and self; best 95; 5 `**`; only here; 3 directions. But only 40% certain.
- **Jockey, Chiron in Ninths:** 100% certain, shared.
- **Horse, Uranus in Ninths:** an old S6-NN entry and a self; 0% certain; star Rigel.
- **Rigel in Ninths** (natal pair, link, S6-NN) on both charts, certain. Many runners in the field share it.
- **None of the winner's threads holds a busy sky body.**

**Losers, as seen:**
- **Ilhabela Fact (9/1, 2nd)** has the most threads in the field (12):
  - Vesta in Ninths, 4 kinds, 100% certain, stars Betelgeuse and Fomalhaut;
  - Sedna in Whole Number on the Vesta/Sedna 99.6 sky pair, 6 `**`, certain, only here.
- **Busby (9/4, 3rd):** jockey Jupiter in Sqrt2, 4 kinds, best 98, but 0% certain.

**R34 doesn't fit the certainty lean:** the winner's main thread is 40% certain, while the 2nd's threads are mostly fully certain.

**Candidate C1, the "R33 thread" (Eddie, 1 Oct, 13:50: "that sounds a good reason that this one won"):**
- **Definition:** one natal body in the race sky's top family, on 3+ kinds of layer including a self. Every item certain, every item only on this runner, 3+ full matches (`**`), and reached from 3 directions.
- **Across races 25–48:** 5 runners in 4 races. **2 won: R27 Nelson River 20/1 and R33 Man On A Mission 12/1, both outsider winners.** The others were 3rd (R37 Night On Earth) and 2nd and 5th (R47 Study The Stars, Regulator). Nobody has it in 20 of the 24 races.
- **Removing any one condition brings it back to about the base rate:**
  - any family: 4 of 21;
  - not only here: 3 of 15;
  - not all certain: 3 of 10.
  It holds only as the full combination.
- **Status:** found after seeing R33, so it's a candidate, not a finding. Freeze it as defined and test it blind on races 1–24 and on fresh races.

### R35 Newmarket 12/04 (favourite race, 7 runners; Educator / Tom Marquand won at 11/4)
**Race sky:**
- Top family Ninths (32%); the other families are level at 14% each.
- Busiest body: Mars (7), then Uranus, Haumea, Jupiter, Sun, Ceres (6 each).
- Top pairs: Orcus/Polaris 99.8, Mars/Sirius 99.6, Neptune/Uranus 98.9.

**Winner's threads (as seen):** modest.
- Horse Jupiter (busy) in Ninths: Type 1, link A, self; 100% certain; no `**`; shared.
- Jockey Transpluto in Ninths: 0% certain, shared.
- Horse Venus in Phi Powers: only here, 0% certain.
- Nothing in the winner's threads stands out from the field.

**Losers carry the louder threads:**
- High Fibre (2nd): horse Makemake in Ninths, 5 kinds, 100% certain, 5 `**`, shared.
- Israr (3rd): horse Sun in Ninths, 6 kinds, 0% certain.
- Mr Alan (6th): jockey Ceres in Ninths, 4 kinds, only here, 0% certain.

**Jockey note:** Marquand rides 7 times in races 25–48, and this is his only win.

### R36 Newmarket 14/04 (outsider race; Eydon / David Egan won at 22/1; the favourite Masekela, 2/1, was 2nd)
**Race sky:**
- Top family Ninths (36%), then Golden Ratio (18%).
- Busiest body: Jupiter (9), then Mercury, Pallas, Saturn, Makemake, Sedna (6 each).
- Top pairs: Transpluto/Regulus 100.0 (Ninths), Sun/Orcus 99.9, Mercury/Pallas 99.3, Mars/Algorab 99.2.

**Winner's threads (as seen; all on the jockey):**
- Pluto in Whole Number: Type 1, link A, natal pair, self; 100% certain; 6 `**`; star Deneb Algedi (Pluto/Deneb Algedi 91.7); shared.
- Orcus in Golden Ratio: 3 kinds; 100% certain; only here.
- Chiron in Ninths: a self 86c `**` (Chiron/Juno 95.1, L link Chiron/Orcus) and an old S6-NN Chiron–Bellatrix 98.7; 75% certain.

**Beaten favourite (2nd), as seen:**
- Its main thread is jockey Mars in Ninths: 5 kinds, 6 `**`, star Algorab, on the #4 sky pair Mars/Algorab 99.2. Only 29% certain, and shared.
- Horse Chiron in Sqrt2: 25% certain.

**Jockey repeat:** David Egan won R34 (King Francis) and R36 (Eydon), six days apart. **In both races his jockey chart holds a Chiron self in RA Ninths, certain (76c and 86c).** He has no other rides in races 25–48.

**What "certain" means (Eddie asked, 1 Oct, 13:55):**
- An item is certain if its score stays above zero at every hour of the birth day. It does not mean the body didn't move.
- Example, William Buick (R36), natal Algorab–Mars in RA Ninths: Mars moves about 0.38° in RA across the day (177.62°–178.00°), and the score stays between 82.8 and 100 (97.9 at 12:00), so it is certain. His Mars self scores 0–100 across the day, so it is possible.
- **To keep an eye on (Eddie, 13:58):** a certain item can still dip low at some hour. Eddie doesn't want an absolute limit (such as lowest score ≥ 40). Consider later, and keep relative.

### R37 Chester 05/05 (favourite race, 7 runners; Look Out Louis / Jason Hart won at 2/1)
**Race sky:**
- Top family Ninths (29%).
- Busiest bodies: Mars (7), Sun, Ceres and Haumea (6 each).
- Top pairs: Sun/Vega 100.0 (Phi Powers), Ceres/Pluto 99.7, Rahu/Polaris 99.5 (Ninths).

**Winner's threads (as seen):**
- **Jockey Mars (busy) in Golden Ratio:** 5 kinds; best 99; 6 `**`; star Alkaid (Mars/Alkaid 90.5); 0% certain; shared.
- **Horse Rahu in Ninths:** 3 kinds; 100% certain; 4 `**`; on Rahu/Polaris 99.5 (#3 pair) and Rahu/Haumea; shared.
- **Horse Juno in Ninths:** 3 kinds; 100% certain; only here.
- Main thread 0% certain, so this goes against the certainty lean.

**Losers, as seen:**
- Sunday Sovereign (5th) has a very similar jockey Mars thread: Whole Number, 6 kinds, 10 `**`, 0% certain, star Alkaid.
- Night On Earth (3rd) has Jupiter in Ninths on both charts (horse 6 kinds 70% certain; jockey only here, 100% certain). It meets candidate C1 (see above).

### R38 Musselburgh 09/05 (outsider race; John Kirkup / Connor Beasley won at 14/1; the favourite The Thin Blue Line, 5/6, was 5th)
**Race sky:**
- Top family Ninths (38%), then Silver Ratio (19%).
- Busiest bodies: Uranus (6), then Haumea, Quaoar and Orcus.
- Top pairs: Venus/Sedna 99.6 (Phi Powers), Ceres/Castor 99.4, Haumea/Alkaid 99.1 (Ninths), Venus/Quaoar 98.4 (Ninths).

**Winner's threads (as seen):**
- **Horse Venus (busy) in Ninths:** 5 kinds (Type 1, link G, natal pair, S6-NN, self); best 97; 5 `**`; on Venus/Quaoar 98.4. **Star Aldebaran (royal).** 0% certain; shared.
- **Jockey Jupiter in Ninths:** Type 2, S6-NN and self; best 97; only here; 50% certain. **Star Fomalhaut (royal);** on Venus/Quaoar and Quaoar/Fomalhaut.
- **Jockey Orcus (busy) in Ninths:** 100% certain; shared.
- **Star grid:** a royal star in both the horse's and the jockey's main thread.

**Beaten favourite (5th), as seen:**
- Mostly certain. Jockey Chiron in Ninths: 5 kinds, 100% certain, shared, 1 `**`.
- Horse Makemake in Silver Ratio: 100% certain, star Regulus (royal).
- Horse Ketu in Phi Powers: only here.
- **The favourite is more certain than the winner here, so R38 goes against the certainty lean.**

**Decision (Eddie, 1 Oct, 14:02): certainty is causing distraction. Reads go back to the 12:00 values only.** The % certain stays as a column in the records, but it isn't used in the reads. C1 is kept as frozen for now. Without its "all certain" condition it's 3 of 10, as recorded above.

### R39 Sedgefield 10/05 (outsider race; Blue Collar Glory / Craig Nichol won at 20/1; the favourite Wheres Maud Gone, 5/6, was 5th)
**Race sky:**
- Top family Ninths (39%), then Phi Powers (17%).
- Busiest bodies: Jupiter (7), Eris and Uranus (6 each), Mars (5).
- Top pairs: Mars/Procyon 99.9 (Phi Powers), Chiron/Jupiter 99.4 (Ninths), Eris/Capella 99.3.

**Winner (as seen):** quiet on threads, with just 2.
- Jockey Makemake in Silver Ratio: Type 1 and link A, best 97, 4 `**`, shared.
- Horse Sun in Ninths: only here.
- **It holds the #2 sky pair Chiron/Jupiter (Ninths, 99.4) as a link only it has** (see P19). Chiron/Jupiter are not busy bodies in its threads.

**Beaten favourite (5th), as seen:** the loud one.
- Horse Mars (busy) in Phi Powers on the #1 sky pair Mars/Procyon 99.9: 5 kinds, best 99, star Alkaid.
- Mars in Ninths on both charts (Mars/Bellatrix 98.4).

### R40 Bath 11/05 (favourite race, 8 runners; Mrembo / Hector Crouch won at 11/4)
**Race sky:**
- Top family Ninths (33%).
- Busiest bodies (not counting fast points): Orcus, Eris (7 each), Pallas (5).
- Top pairs: Orcus/Procyon 99.6 (Ninths), Rahu/Haumea 99.5, Vesta/Orcus 99.2.

**Winner (as seen):** quiet.
- Jockey Haumea in Silver Ratio: Type 2 and self; best 99; only here. **Stars Antares (royal) and Capella**, via Juno/Antares, Juno/Capella, Juno/Saturn and Haumea/Fomalhaut (royal).
- Jockey Gonggong in Silver Ratio: only here.
- Jockey Chiron in Ninths.

**Losers are louder:**
- Delahoussaye (3rd): Orcus (busy) in Ninths on the #1 pair Orcus/Procyon, and Haumea in Golden Ratio on the #2 pair Rahu/Haumea on both charts.
- The Residencies (4th): Orcus in Golden Ratio, 5 kinds, 6 `**`, star Bellatrix.

**Check, quiet or loud (all 24 races).** Each runner is ranked within its race by how loud its threads are (most kinds in one thread, number of threads, full matches). On a 0–1 scale, 0 is the loudest and 1 the quietest; random is 0.5.
- **Winners:** 0.42 / 0.48 / 0.53, which is about random. The winner is the loudest runner in 3–5 races and the quietest in 6–9.
- **Beaten favourites:** 0.36 / 0.31 / 0.40, leaning loud.
- As seen, beaten favourites tend to be among the loudest in their race. Winners are spread.

### R41 Chelmsford 02/06 (favourite race, 7 runners; Tahani / Hollie Doyle won at 6/4)
**Race sky:** top family Ninths (37%). Top pair **Makemake/Aldebaran (royal) 99.9** (RA Sqrt2; also Dec Golden Ratio 90.1), then Juno/Neptune 99.5, Rahu/Polaris 99.5. Busiest bodies Juno (6), Makemake, Sun, Fomalhaut, Saturn, Procyon (5).

**Winner, as seen (the specific thing): Makemake with royal Aldebaran, on the jockey, all only here.**
- Jockey holds the #1 pair inside his own chart: natal pair Aldebaran→Makemake Dec Golden Ratio 49 `**` plus Makemake self 43 `**` (Type 1, only here). Low scores, exact family and coordinate.
- Jockey Makemake is reached by 7 kinds of layer, every one only here (link, Type 1, natal pairs with Aldebaran and Betelgeuse, self, hub with Aldebaran/Betelgeuse/Sedna, old S2, midpoints). Jockey Aldebaran: 4 kinds, all only.
- **Closed triangle on the jockey, Makemake–Aldebaran–Orcus:** natal Aldebaran sits at the midpoint of natal Makemake/Orcus (0.014); the sky pair Makemake/Aldebaran falls on natal Orcus (Type 2, Golden Ratio 69/77); old S6-NN Aldebaran↔Orcus Phi Powers 90.3 reciprocal. Nobody else in the race.
- Royal Regulus also at the midpoint of the jockey's natal Chiron/Makemake (0.002).
- Horse carries Makemake too: exclusive link A Makemake/Betelgeuse Dec Ninths 82.1 (horse 95 `**` ^, top family); hub Makemake with Betelgeuse, Procyon, Bellatrix (only); old S1 5FB Makemake/Pleiades 0.027, 5.3x tighter than the next. So Makemake on both charts.
- P20 holds here (sole holder of the #1 pair, `**`).

**Losers, as seen:**
- Reckon I'm Hot (2nd, 4/1): the #1 pair as Type 2 on both charts (horse → natal Juno, Golden Ratio 84/80; jockey → natal Sun 98/89). The pair lands on another body; it isn't Makemake–Aldebaran in its own chart.
- Beloved Of All (7th): jockey Type 2 Makemake/Aldebaran → natal Neptune 97.
- Tabeeb (5th): horse Makemake in Ninths via Sun/Makemake 97.8 (Type 1, self) – Makemake, different partner, no royal.
- Glasstrees (3rd, 5/2): jockey Makemake natal pairs with Procyon and Sun, Sqrt2 87, no match.

### R42 Bath 03/06 (outsider race, 4 runners; Little Girl Blue / Luke Morris won at 10/1; the favourite Soi Dao, 13/8, was 2nd)
**Race sky:** top family Ninths (40%). Busiest body **Quaoar (8 of the 80+ pairs)**, Neptune 7. Top pairs (not fast): Vesta/Antares (royal) 99.5, Sedna/Aldebaran (royal) 99.1, Ketu/Neptune 99.0.

**Winner, as seen (the specific thing): the busiest body Quaoar on both charts, matched, only here.**
- Link A Quaoar/Alphecca 89.8 (RA Whole Number), only this partnership: horse X Quaoar→Alphecca 90 `**`; jockey Quaoar self 69. Soi Dao's horse (96 `**`) and Hattie C's horse (91 `**`) have the horse side, but no jockey side – so only the winner holds it as a link.
- Jockey Quaoar: 6 kinds, all only – Type 1 Quaoar/Altair (natal Altair→Quaoar Dec Whole Number 90 `**` ^ plus self), hub with Altair, Ceres, Jupiter; old S6-NN Quaoar→Altair 90.0.
- Horse Alphecca: 5 kinds, all only – the link, Type 1 Pallas/Alphecca 97.5 (natal 97), hub with Pallas and Quaoar.
- Royal: the #2 pair Sedna/Aldebaran falls on horse natal Juno (Golden Ratio 82, only); Pallas/Aldebaran also → natal Juno; the fast top pair Eris/PoF 100.0 → natal Juno. Juno is a receiver for Aldebaran.
- Exclusive link A Venus/Vega 98.2.
- Holds none of the top 3 pairs alone.

**Beaten favourite Soi Dao (2nd), as seen – the loud one:**
- Sole holder of the #3 pair Ketu/Neptune 99.0 as a link A, but in Ninths / Phi Powers, not the sky's Golden Ratio – no match (P20's losing side).
- 4 exclusive A links, 14 Type 2s only here, including the #1 pair Vesta/Antares (royal) → jockey natal Jupiter (Sqrt2 69/75).
- Horse Neptune 6 kinds all only. More of everything; nothing matched on the race's main bodies on both charts.

**Check (all 24 races): deepest body with every layer only here.** For each runner, the most kinds of layer on one body where all are only here. Winner is the sole deepest in 5 races (R25, R29, R30, R32, R41), tied deepest in 7, below in 12. Close to chance on its own; it's which body (a body of the top pair or the busiest body) that looks to matter, not depth alone.

**Note on fixed-star midpoints:** a fixed star's sky position is almost its natal position, so "natal star at midpoint X" (T3) and "sky star at midpoint X" (T5) are usually the same fact twice (R41 Aldebaran at Makemake/Orcus; R42 Regulus at Jupiter/Sedna). Counted once in the reads.

### R43 Chester 11/06 (favourite race, 8 runners; Copper Knight / Sean Kirrane won at 5/2)
**Race sky:** top family Ninths (41%). Busiest bodies Quaoar (8), Eris, Jupiter, Chiron (7). Top pairs Mercury/Capella 99.9, Eris/Jupiter 99.9 (Ninths), Eris/Sirius 99.9.

**Winner, as seen: quiet, nothing loud.** No exclusive links at any level.
- Horse Type 1 Vesta/Betelgeuse (sky 90.0 Dec Whole Number): natal Betelgeuse→Vesta 90 `**` (at the sky's score) plus Vesta self 77 `**`, only here.
- The sky pair Chiron/Gonggong (90.8 Ninths; Chiron is a busy body) falls on both charts as Type 2: horse → natal Transpluto (99), jockey → natal Orcus (100). Only here.
- Horse: Quaoar (busiest body) as a natal pair with Jupiter (only here), hub Quaoar with Jupiter, Rahu, Transpluto (only); hub Sun with Regulus (royal) and Transpluto (only); hub Jupiter with Quaoar and Regulus (only). Low scores (46–80).
- Wider three-way band (0.1–0.5): 4 bodies only on this partnership (Uranus, Sedna, Neptune, Gonggong).
- Quaoar is carried by every runner in the race in some way, so Quaoar itself isn't specific here.

**Losers, as seen – louder:**
- Glory Fighter (2nd, 3/1): horse Sedna in Sqrt2, 5 kinds, 8 `**`, on Quaoar/Sedna 99.0 and Quaoar/Capella, shared.
- Count d'Orsay (3rd): Jupiter in Ninths on both charts (6 and 5 kinds) on the #2 pair Eris/Jupiter, no match on the link.
- Militia (5th): also on Eris/Jupiter, no match.

### R44 Ripon 16/06 (outsider race, 4 runners; Society Red / Oisin Orr won at 16/1; the favourite Bollin Joan, 10/11, was 4th, last)
**Race sky:** top family Ninths (35%). Busiest non-fast body **Haumea (7)**, then Polaris, Quaoar, Ketu, Jupiter, Chiron (6). Top pairs Saturn/Rigel 99.7 (Ninths), Uranus/Aldebaran (royal) 99.5, Makemake/Sedna 99.5.

**Winner, as seen (the specific thing): the busiest body Haumea on both charts, in Ninths, through three links only it has.**
- Exclusive A links Rahu/Haumea 90.6, Ceres/Haumea 89.2, Vesta/Haumea 85.4 (all RA Ninths), plus L Mercury/Haumea. Horse: Haumea self Dec Ninths 64 (with the natal pair Haumea→Rahu, Type 1). Jockey: Rahu→Haumea 93 `**` ^, Ceres→Haumea 85 `**`, Vesta→Haumea 94 `**` ^; hub Haumea with Ceres, Rahu, Vesta.
- Horse Haumea: 5 kinds, all only. Horse Rahu: 6 kinds, all only.
- Also exclusive A Mercury/Quaoar 94.3 (Quaoar busy, 6) and Chiron/Alkaid 90.4 (Chiron busy, 6); horse hub Chiron with Alkaid, Altair, Castor, Ketu (only); jockey natal pair Chiron→Jupiter 92 (only).
- Exact three-way: equator at the midpoint of sky / horse natal Venus, 0.014, only.

**Beaten favourite (4th, last), as seen:** one exclusive link, Eris/Mars 92.9 Ninths, made of two different selves (Eris on the horse, Mars on the jockey) – no shared body. Everything else shared with the field (the Transpluto star links all four runners hold). Horse Quaoar in Whole Number on Quaoar/Altair 99.4, shared.

**Check (all 24 races), busiest body:** the busiest non-fast body in the race held in a link only this partnership has (A, 80+), with a full match on at least one chart: **19 holders, 6 won** (R28 Gowanlad 2/1F, R33 Man On A Mission 12/1, R39 Blue Collar Glory 20/1, R42 Little Girl Blue 10/1, R44 Society Red 16/1, R46 Lequinto 11/4F); also 3 seconds and 2 thirds. Base is about 1 in 6.
**Opposite case:** a body of the #1 sky pair held in a *different* exclusive link (not the #1 pair itself), with a match: 12 holders, 1 won (R41 Tahani). As seen, the #1 pair's bodies lean the wrong way when the link is another pair.

### R45 Carlisle 07/07 (outsider race, 6 runners; Whitefeathersfall / Franny Norton won at 10/1; the favourite Million Thanks, 13/8, was 3rd)
**Race sky:** top family Ninths (31%), Golden Ratio 23%. Busiest bodies Pluto, Sedna, Haumea (6 each). Top pairs Pallas/Deneb Algedi 99.8 (Dec Ninths), Ketu/Mercury 99.8, Quaoar/Vega 98.9.

**Winner, as seen: no exclusive A link (G Jupiter/Venus 75.4 Phi Powers, `**` both sides, is its best). The specific things:**
- **The #1 pair meets the busiest body on the horse's natal Pallas:** horse has the #1 pair as a natal pair (Deneb Algedi→Pallas 83, shared with Aswan and Kevin Stott), and *only this horse* has the hub Deneb Algedi with Pallas and Haumea; Haumea's sky pairs Saturn/Haumea (93) and Neptune/Haumea (94) both fall on natal Pallas (Type 2, Ninths, only here); Pallas self Sqrt2 95 `**`.
- Busy bodies on both charts through Type 2s, only here: Saturn/Haumea → horse Pallas and jockey Vesta; Haumea/Polaris → horse Ketu and jockey Vesta; Sedna/Betelgeuse → natal Saturn on both charts.
- Pluto (busy): horse natal pair Mars/Pluto and hub Pluto with Mars, Transpluto, only here.
- Exact three-way: Sun (busy, 5), jockey natal at the midpoint of sky / horse natal, 0.001, only.

**Losers, as seen:**
- Persist (2nd, 7/4): horse Sun in Ninths, link A on Chiron/Sun 98.0 and Pluto/Sun 98.2, only here.
- Million Thanks (fav, 3rd): jockey Chiron in Ninths on Chiron/Sun 98.0, shared.
- Louder losers: Lucia Joy (6th, 28/1) jockey Venus 5 kinds, 6 `**`; Aswan (4th) horse Saturn 9 `**`.

### R46 Windsor 11/07 (favourite race, 7 runners; Lequinto / Andrea Atzeni won at 11/4)
**Race sky:** top family Ninths (33%), Whole Number 26%. Busiest body **Saturn (8)**, Pallas 7. Top pairs Pallas/Antares (royal) 99.7, Ketu/Mars 99.7 (Dec Golden Ratio), Rahu/Procyon 99.2.

**Winner, as seen – loud *and* specific (the favourite):**
- 4 exclusive A links: Ketu/Mars 99.7 (#2 pair; horse 74 `**`), Neptune/Algol 98.6, Saturn/Rigel 97.0 (busiest body; horse 88 `**`), Vesta/Rigel 84.8 (horse 94 `**` ^). Fits P20 and P21.
- Mars on both charts through links only it has (Ketu/Mars, Mars/Algol), and the sky pair Rahu/Algol falls on horse natal Mars (99/95, only).
- Jockey Saturn: natal pairs with Haumea and Vesta (only here); Saturn/Rigel link on both charts.
- Horse Rigel 7 kinds, Vesta 6 kinds.

**Losers, as seen:**
- King Of Jungle (2nd, 7/2): sole holder of the #3 pair Rahu/Procyon as a link, no match (P20's losing side).
- Impeach (7th, 20/1): horse Rahu in Ninths, 6 kinds, 6 `**`, on Rahu/Procyon and Rahu/Algol, shared – loud.

**Check (all 24 races): the same sky pair landing as Type 2 on both horse and jockey, only this partnership.** With a busy body in the pair: 34 holders, 6 won (18%). Without: 44 holders, 5 won (11%). **Base rate – the both-chart Type 2 is common and says nothing on its own.** (R43 and R45 winners had it; so did 72 others.)

### R47 Chepstow 14/07 (favourite race, 6 runners; Beryl Burton / Faye McManoman won at 11/8)
**Race sky:** top family Ninths (35%). Busiest bodies **Mars, Uranus, Spica, Sun (7 each)**. Top pairs Saturn/Castor 99.9, Eris/Quaoar 99.8 (RA Ninths), Vesta/Algorab 99.6.

**Winner, as seen – the busy bodies on both charts through links only it has:**
- 4 exclusive A links: Eris/Quaoar 99.8 (#2 pair; jockey 43 `**`) – P20; Mars/Spica 85.7 (two busiest bodies in one pair, Ninths); Rahu/Makemake 84.9; Sun/Transpluto 84.0; plus G Pluto/Sun 74.9 (horse Sun self 69 `**`).
- **Mars:** on both charts; jockey Mars reached by 8 kinds (Type 1 Mars/Rahu and Mars/Spica, only here).
- **Sun (busy, watched):** on both charts through two exclusive links; horse Sun 6 kinds, jockey Sun 5 kinds; the sky pairs Pluto/Alphecca and Pluto/Alkaid both fall on horse natal Sun (only).
- No exact three-way. The Mars/Spica and Sun links match family only partly (`*`), so not in P21's strict count.

**Losers, as seen:**
- Study The Stars (2nd, 4/1): links on Ketu/Mars 99.2 and Mars/Rahu only it holds, with `**` (in P21) – Mars, but not Mars with Spica, and no Sun.
- Regulator (5th): horse Venus 5 kinds, loud. Pedro De Styles (6th, 50/1): jockey Sedna 4 kinds; link Mars/Algorab only (P21).

### R48 Doncaster 16/07 (outsider race, 6 runners; Novakai / Tom Eaves won at 12/1; the favourite Crackovia, 8/15, was 2nd)
**Race sky:** top family Ninths (31%). Busiest body **Haumea (7)**, then Spica (6). Top pairs Saturn/Uranus 99.9 (RA Golden Ratio), Eris/Betelgeuse 99.0, Sun/Sedna 98.7.

**Winner, as seen – the second-busiest body Spica, with Jupiter, on both charts, only here:**
- Exclusive A link Jupiter/Spica 93.5 (RA Ninths, the top family): jockey Type 1 – natal Jupiter→Spica 66 `**` plus Jupiter self 93 `**` (only here); horse natal Jupiter→Spica 83.
- Jockey Jupiter reached by 7 kinds; horse Jupiter 5 kinds.
- Jockey holds the #1 pair Saturn/Uranus as a natal pair (Dec Sqrt2 87, no match), only here.
- Exact three-way Chiron (horse natal at the midpoint of sky / equator, 0.029), only.

**Beaten favourite Crackovia (2nd, 8/15), as seen – holds the busiest body:** exclusive A link Haumea/Deneb Algedi 84.2 (Ninths), `**` on both charts (horse 75, jockey Haumea self 75). Jockey Haumea 4 kinds. This is P21's losing side: the busiest body, matched on both charts, beaten by the runner on the second-busiest body.

**P21 recheck (1 Oct 14:30):** the earlier count missed star names with a space (Deneb Algedi). Corrected: **20 holders, 6 won** (adds Crackovia, 2nd). Widening "busiest" to the top two levels: 46 holders, 9 won (20%) – back to base, so the strict busiest body is the version that leans.

### Body + vibration view (bv_profile.py, from 1 Oct, 13:35)
A combination is one natal body in one family, carried by 2 or more kinds of vibration layer (link, Type 1, natal pair, self, hub, Type 2, old S6-NN), and no other chart in the race has that body in that family. "Both charts" means the horse and the jockey each carry the same combination.

As seen, races 25–33:

| Race | Winner (combinations) | Runners with a combination on both charts |
|---|---|---|
| R25 | Omar Maretti, 15/8 favourite (9): Pallas Sqrt2 and Arcturus Sqrt2 **on both charts** | winner; Marown (Uranus Golden Ratio, PU) |
| R26 | Sir Chauvelin, 10/1 (3) | favourite Onesmoothoperator, 2nd (Haumea Whole Number; 9 of its 11 combinations in Whole Number) |
| R27 | Nelson River, 20/1 (8) | Stepney Causeway, 3rd (24 combinations, three on both charts) |
| R28 | Gowanlad, 2/1 favourite (2, the fewest in the field) | none |
| R29 | Olympe De Gouges, 25/1 (1, the fewest) | favourite Oot Ma Way, 2nd (Jupiter Whole Number, Mars Phi Powers) |
| R30 | River Bray, 22/1 (3) | favourite Ballyblack, 3rd (Ketu Phi Powers); Reserve Tank, 6th (Orcus Whole Number) |
| R31 | Soldier Of Destiny, 13/8 favourite (5) | Burrows Diamond, 2nd (Betelgeuse Ninths) |
| R32 | Hold Onto The Line, 100/30 favourite (4) | none |
| R33 | Man On A Mission, 12/1 (9, the most in the field) | none |

- **Seen so far:** a combination on both charts belongs to the winner once (R25, a favourite). It belongs to beaten runners 7 times, finishing 2nd, 3rd or worse. The beaten favourites in R26, R29 and R30 all have one.
- **Seen so far:** the 25/1 and 10/1 winners (R29, R26) carry very few combinations of their own. The R33 winner carries the most in its field.

### Combination record, races 25–48 (bv_record.py and combo_table.py, 1 Oct, 13:45)
- **What's in it:** 23,421 body + vibration items, giving 4,573 combinations (one body in one family on one chart, on 2+ kinds of layer). 658 of them are race-unique: no other chart in that race carries that body in that family.
- **Base rate:** winners are about 1 in 6 of the partnerships, and they hold 109 of the 658 race-unique combinations (16.6%). So overall, winners don't carry more unique combinations than anyone else.
- **By feature (as seen; share of race-unique combinations on winners, against the 16.6% base):**
  - **MATCH (`**`, the sky pair's own family and coordinate): 24 of 93 (26%)**, against 15% without it. This is the clearest difference.
  - **Family:** Whole Number 23% and Phi Powers 22%; Golden Ratio 16%, Sqrt2 15%, Ninths 15%; Silver Ratio 12%; Conjunction 0 of 30.
  - **5+ kinds of layer:** 6 of 20 (30%). The numbers are small.
  - **No difference from base:** `^` (17%), certain (16%), triangulation by count (14–18%), royal star in the grid (18%), star partner (17%), horse against jockey (16%/17%).
- **Body + family pairs unique on 2 winners:** Ceres Phi Powers, Fomalhaut Phi Powers, Betelgeuse Phi Powers, Regulus Phi Powers, Rahu Phi Powers, Vega Phi Powers, Alkaid Sqrt2, Ceres Sqrt2, Algol Whole Number, Eris Whole Number (2 of 2), Quaoar Silver Ratio, Orcus Golden Ratio, Pluto Golden Ratio. Each is carried by 2–6 runners in all, so it's too early to call any of them positive.
- **Files:** /home/claude/reads/bv_items.csv, combos.csv, combos.txt.

## Possibilities list (running)

| # | Way seen | Winners | Same thing on losers |
|---|---|---|---|
| P1 | Exclusive A link at 90+ | R25, R27 (R30 winner: highest 82.9) | R25: 4 losers; R26: favourite, Resumption, Alba Rose; R27: favourite, Stepney; R28: Tathmeen |
| P2 | One body or star in 2+ of the winner's exclusive links, no other partnership linked through it at that level | R25 (Arcturus), R27 (Uranus) | not yet checked on losers |
| P3 | Same-body self on both charts inside an exclusive link | R25 (Pallas), R30 (Makemake) | R30: favourite (Transpluto, 3rd) |
| P4 | Mirror link (exclusive) | R25, R27 | R25: 4 losers; R26: favourite; R27: favourite, Stepney; R28: Alablaq, Tathmeen |
| P5 | Certain three-way, only on this partnership | R25, R32 | R25: Boranha; R27: favourite, Stepney, Fransham; R28: James Watt |
| P6 | Midpoint on both horse and jockey, no other chart | R26 (T5), R32 (T5) | R25: Almazhar (2nd); R30: favourite (3rd). Both are the same configuration: natal Transpluto at mid of natal Haumea/Procyon, Dec |
| P7 | Winner with no exclusive A or G link | R26 (none at any level), R29 (L only) | — |
| P8 | One body through several of the winner's items (hub plus midpoint or self) | R25 (Pallas), R26 (Neptune, Saturn), R27 (Rahu), R29 (Sedna), R30 (Makemake, Rahu), R31 (Makemake, Neptune), R32 (Neptune, Jupiter) | not yet checked on losers |
| P9 | Loser higher on a body the winner links through | — | R25: Paddy Pie, Boranha, Almazhar; R26: favourite (Venus); R28: Alablaq (Quaoar) |
| P10 | Self inside an exclusive link | R25 (Ceres, Pallas), R27 (jockey Rahu), R28 (jockey Orcus) | R26: favourite (Jupiter, Venus); R27: favourite (jockey Mars) |
| P11 | All exclusive links survive certain-only | R27, R28 | R26: Resumption; R25: Winds Of Fire, Paddy Pie |
| P13 | Losing favourite's exclusive links mostly or all drop under certain-only | — | R26 (2 of 3), R27 (both A), R29 (both); R30: 1 of 2 drops |
| P14 | Winner's natal pair on both charts, certain, exclusive | R29 (Quaoar/Sedna, L) | R29: favourite's two are possible |
| P15 | Several Type 1s only here on one chart | R29 (jockey 4, horse 1), R30 (horse 4, jockey 1) | R26: favourite (both charts) |
| P12 | Every item on the exclusive links a full match `**` | R28 | not yet checked on losers |
| P16 | Winner with no exclusive A link (80+) | R26, R29 (outsiders); R31, R32 (favourites) | — |
| P17 | Same exclusive link pair on winners of different races | R30 (Neptune/Makemake, L), R31 (Neptune/Makemake, G) | — |
| P18 | Same natal pair on both charts inside an exclusive link | R29 (Quaoar/Sedna, L, certain), R31 (Saturn→Vesta, G, identical values) | R29: favourite (Ceres/Jupiter, Jupiter/Bellatrix, possible) |
| P19 | One of the race's top 3 sky pairs (not fast) as a Type 1 or link only this partnership holds | R27 (Rahu/Algorab, J), R29 (Chiron/Transpluto, H), R37 (Rahu/Polaris, H), R39 (Chiron/Jupiter link), R41 (Makemake/Aldebaran, J), R46 (Ketu/Mars link) | R28 Alablaq 5th; R30 Electric Annie 5th; R31 Nero Rock UR; R32 Balranald 6th; R33 Bang On The Bell 3rd; R34 Ilhabela Fact 2nd; R35 High Fibre 2nd; R37 Militia 6th; R40 Delahoussaye 3rd; R42 Soi Dao (favourite) 2nd; R43 Count d'Orsay 3rd; R46 King Of Jungle 2nd. Nobody holds one in R25, R26, R36, R38, R44, R45 |
| P20 | Only partnership in the race holding one of the top 3 sky pairs (not fast) as a link or Type 1, **with a full match `**` on at least one chart** (counted by partnership, 1 Oct 14:10) | 6 of 13 holders won: R27 Nelson River 20/1, R29 Olympe De Gouges 25/1, R39 Blue Collar Glory 20/1, R41 Tahani 6/4F, R46 Lequinto 11/4F, R47 Beryl Burton 11/8F | R28 Alablaq 5th; R31 Nero Rock UR; R34 Ilhabela Fact 2nd; R35 High Fibre 2nd; R37 Militia 6th; R40 Delahoussaye 3rd; R48 Passing Storm 5th. Sole holders **without** `**`: 0 of 4 won (R30 Electric Annie 5th, R33 Bang On The Bell 3rd, R42 Soi Dao (fav) 2nd, R46 King Of Jungle 2nd). `**` on both horse and jockey: R39 winner and R35 High Fibre (2nd) only. When the pair is shared by most of the field (R32, R36) it says nothing. No sole holder in R25, R26, R32, R36, R38, R43, R44, R45 |

**Eddie (1 Oct, 14:05):** "the winner holds something specific, like a top sky pair as a link only it has (race 39) or royal stars in a thread only it has (races 38 and 40), rather than the most of everything" — "yes exactly this … this is the deep detail we need to uncover." Standing lens for the reads: look for what only the winner holds, not who holds the most.
| P21 | The race's busiest non-fast body held in an A link (80+) only this partnership has, with a full match `**` on at least one chart (checked 1 Oct 14:20; corrected 14:30) | 6 of 20 won: R28 Gowanlad, R33 Man On A Mission, R39 Blue Collar Glory, R42 Little Girl Blue, R44 Society Red (Haumea, three links), R46 Lequinto | R25 Winds Of Fire PU, The Paddy Pie 3rd; R27 Nickolson (fav) 2nd; R29 Fiamette 4th; R32 Keep The Faith 5th; R34 Ilhabela Fact 2nd; R37 Sunday Sovereign 5th; R40 The Residencies 4th; R46 A Sure Welcome 4th, Amazonian Dream 6th; R47 Study The Stars 2nd, Pedro De Styles 6th; R48 Mother India 3rd, Crackovia (fav) 2nd. Opposite: a #1-pair body in a different exclusive link, 1 of 12 won |
| P22 | Closed triangle on one chart: a natal star at the midpoint of two natal bodies, and the sky pair (one body + that star) falling on the other body | R41 jockey (Makemake–Aldebaran–Orcus) | not yet checked |
| P23 | The #1 sky pair and the busiest body meeting on one natal body (natal pair of the #1 pair + busy-body sky pairs falling on the same natal body + a hub joining them), only here | R45 horse natal Pallas (Pallas/Deneb Algedi with Haumea) | not yet checked |
| — | Checked and dropped: same sky pair as Type 2 on both charts, only this partnership | 11 of 78 won | base rate |


**Eddie (1 Oct, 14:18): the R45 exact three-way (jockey natal Sun at the midpoint of sky Sun / horse natal Sun, 0.001, only) "stands out to me".** Checked across all 24 races (exact band, ≤0.1):
- Any exact three-way: 80 partnerships, 12 won. Only this partnership: 53, 9 won (17%, base). Only + busy body: 14, 2 won. Only + ≤0.01: 6, 1 won (Birds Of Prey R30 Haumea 0.001 was 4th).
- By form, only this partnership: jockey natal between sky and horse natal – 7 holders, 2 won (R32 Hold Onto The Line, Jupiter; R45 Whitefeathersfall, Sun), 3 thirds; horse natal between sky and jockey natal – 7, 1 won (R38 John Kirkup), 2 seconds, 1 third; sky between horse and jockey – 9, 0 won (3 seconds, 2 thirds); forms using the equator – 1–2 wins each, base.
- As seen: on its own, base rate. The forms with three real points (no equator): 21 partnerships, 3 won, 13 in the first three – with fields of 4–8 about half would place by chance. Kept as a lens to watch in combination, not a line on its own.
- Note: the Sun moves about 0.3° of Dec a day in early May, so 0.001 is the 12:00 value; through the horse's birth day the real figure could be several hundredths either way. It stays inside the band.
- **Eddie (14:20): "keep an eye on which body – Sun might be significant."** Standing watch on the Sun. Exact three-ways on the Sun, 24 races: 4, all only this partnership – R45 Whitefeathersfall won (jockey natal between sky and horse, 0.001); R32 Balranald 6th (sky Sun between horse and jockey, 0.018); R34 Settle Petal 6th (equator form, 0.019); R41 Beloved Of All 7th (horse natal between sky and equator, 0.053). The R45 form (jockey Sun between sky Sun and horse Sun) appears once. By body overall: Eris 37 three-ways (mostly shared, the equator form), 6 won; Chiron 6 (2 won), Juno 6 (2 won); Neptune, Rahu/Ketu, Quaoar, Pallas 0 wins from 4–6 each. All small numbers.

**blind_test.py v1.0 (1 Oct 15:50, Eddie: "yes to the script")** – freezes P20, P21 and C1 and writes their holders without reading any result; `--score` joins the result afterwards. Check on races 25–48: P20 13 holders, 6 won (the earlier "12" missed R48 Passing Storm, 5th – corrected above); P21 20 holders, 6 won; C1 5 holders, 2 won. Same as the reads.

## Blind test on races 1–24 (1 Oct, 18:45)
Workbooks rebuilt by Eddie on charts 2.3 / engine 2.2 (fingerprint 64612c16fe) / active v4.1. Detail sheets race_detail v1.3 → /home/claude/detail1; item record bv_items_1_24.csv; holders frozen in holders_1_24.csv (md5 53b0a3d1…) and shown to Eddie before any result was read. 148 partnerships, 24 winners (16% base).

| Line | Fitted on 25–48 | Blind on 1–24 | Blind places (1st–3rd) |
|---|---|---|---|
| P20 top-3 pair held alone, `**` | 6 of 13 won | **2 of 13 won** (R4 Madame Tantzy 12/1; R19 Mercian Hymn 13/8F) | 7 of 13 |
| P21 busiest body in an exclusive A link, `**` | 6 of 20 won | **5 of 25 won** (R6 Golden Flame 9/1; R9 Arvico Bleu 25/1; R12 Forget You Not 25/1; R18 Deja Vue 10/1; R22 Java Point 2/1F) | 14 of 25 |
| C1 R33 thread | 2 of 5 won | **0 of 6 won** (three 3rds) | 3 of 6 |

As seen: P20 and C1 fall back to base on fresh races – the 25–48 figures were hindsight. P21 holds a little above base (20% against 16%), with two 25/1 and a 10/1 and 9/1 among its winners; small numbers. All 48 together: P21 11 of 45 (24%). Losers beside P21's blind winners: R6 Valley Forge (fav) 3rd; R9 If Not For Dylan 4th; R12 Jarlath 2nd; R22 Une De La Seniere 3rd, Fanamix 4th.

**P21 and outsiders (Eddie, 1 Oct 19:20: "8 out of 24 outsiders showed this pattern").** Checked, all 48 races (24 won at 9/1 or longer):
- Runners at 9/1+: P21 holders 21, **8 won (38%)**; all other 9/1+ runners 84, 16 won (19%).
- Runners under 9/1: P21 holders 24, 3 won (12%); others 162, 21 won (13%) – no difference.
- Blind races 1–24 only, 9/1+: P21 holders 13, **4 won (31%)** (Forget You Not 25/1, Arvico Bleu 25/1, Deja Vue 10/1, Golden Flame 9/1); others 42, 8 won (19%). The 9 blind losers: Jarlath 2nd, Get An Oscar 3rd, Une De La Seniere 3rd, If Not For Dylan 4th, Mr Ginja Ninja 4th, Fanamix 4th, Suanni 4th, Poco Contante 6th, Van Zant 8th.
- As seen: P21's lean sits with the outsiders; among shorter-priced runners it says nothing. Small numbers; to keep testing on fresh races.

## Outsider races 25–48 re-read with the newer lenses (from 2 Oct, 06:45)
Lenses now standard: what only the winner holds; busiest body and top pairs; concentrated / spread / around the busiest; C2; **royal star → body for winner and losers**; the Sun watch. Results known for these races – adds to the picture, not a blind test. Outsider winners (9/1+) in 25–48: R26, R27, R29, R30, R33, R36, R38, R39, R42, R44, R45, R48.

### R26 Newcastle 15/02/2022 16:40 – Sir Chauvelin / Paul Mulrennan 10/1 (favourite Onesmoothoperator 13/8, 2nd)
- **Sky:** busiest Ketu (8), Makemake (7), Ceres (6). Top pairs Sun/Algorab 99.5, Makemake/Transpluto 98.5, Chiron/Spica 97.8.
- **Winner – SPREAD, quiet, royal pairs landing on its natal bodies (not C2: no exclusive A link):**
  - **Ceres/Aldebaran (Ceres busy) falls on the horse's natal Mercury and Venus and the jockey's natal Sun** – only here, both charts.
  - **Sun/Fomalhaut falls on the horse's natal Quaoar, Rahu and Transpluto** – only here.
  - Horse natal Rahu receives three sky pairs (Sun/Fomalhaut, Ceres/Polaris, Makemake/Sedna – Makemake busy), only; Juno/Algorab → horse natal Sun (only).
  - Both-chart midpoint: sky Neptune at the midpoint of natal Quaoar/Sedna on horse and jockey (0.044), only (P6). Three-way Saturn (0.098), only.
  - Sun watch: the Sun is in the #1 pair; Sun/Fomalhaut onto three natal bodies; Ceres/Aldebaran and Juno/Algorab onto natal Suns.
- **Royal → body:** Aldebaran → Mercury, Venus (horse), Sun (jockey); Fomalhaut → Quaoar, Rahu, Transpluto (horse) – all as sky pairs landing, all only.
- **Losers:** favourite Onesmoothoperator – loud (Jupiter/Makemake, Jupiter/Venus links, shared Makemake thread), little royal. Wise Eagle (4th, 10/1) – Antares–Gonggong link L both charts. Resumption (5th, 7/4) – Aldebaran–Venus link L. Alba Rose (6th) – Regulus–Eris natal 100.

### R27 Leicester 17/02/2022 14:45 – Nelson River / Harry Bannister 20/1 (favourite Nickolson evens, 2nd)
- **Sky:** busiest **Mars (9)**, Rahu and Quaoar (7), Makemake 6. Top pairs Sedna/Arcturus 99.8, Mars/Rahu 99.5, **Rahu/Algorab 99.2**.
- **Winner – CONCENTRATED on Rahu, on the jockey (P20, C1):**
  - **#3 pair Rahu/Algorab as a jockey Type 1** (74 `**`), only; jockey Rahu 4 kinds, all only (Type 1, link A, natal pair, self).
  - Exclusive A links Ceres/Uranus 92.9 and **Rahu/Uranus 86.2** (jockey Rahu self 65 `**`).
  - Other busy bodies on the jockey, only: Makemake/Pleiades → natal Quaoar (88/95); Haumea/Makemake Type 1. Mars (busiest) is not its own.
- **Royal → body:** **Regulus – Sun** horse natal pair 98 (sky Sun/Regulus), only; Fomalhaut–Mars natal (shared). Light.
- **Losers:** favourite **Nickolson** (P21) – **Fomalhaut – Mars** (the busiest body) as its own link both charts and jockey Type 1 99 – royal on the busiest body, beaten. **Stepney Causeway (3rd) – the most royal in the race (12)**: Aldebaran – Pluto, Pluto/Aldebaran → Sedna, Ketu/Antares → Neptune and Sedna, Mars/Fomalhaut → Sun, Regulus – Eris link A both charts; 7 exclusive A links – loud. Fransham (PU) – Regulus – Sun self.
- **Seen:** Regulus with the Sun on the winner again (R17 jockey Sun; R27 horse natal pair) – tally Regulus–Sun only-here 11 runners, 2 won: base.

### R29 Doncaster 18/03/2022 14:40 – Olympe De Gouges / David Noonan 25/1 (favourite Oot Ma Way 5/6, 2nd)
- **Sky:** busiest **Chiron and Vesta (8)**. Top pairs Gonggong/Algol 99.7, **Chiron/Transpluto 99.5 (#2)**, Gonggong/Spica 98.5, Chiron/Altair 98.5, **Pallas/Sedna 96.0 (#5)**.
- **Winner – AROUND THE BUSIEST (Chiron via #2; Vesta pairs landing), plus Sedna on the jockey (P20; not C2 – no exclusive A link):**
  - **#2 pair Chiron/Transpluto as a horse Type 1** (90 `**`), only; it also falls on the horse's natal Uranus (82/83), only. Horse Transpluto 7 kinds.
  - **Sedna on the jockey:** Type 1s Pallas/Sedna (#5) and Sedna/Arcturus, only; jockey Sedna 6 kinds; link L Quaoar/Sedna on both charts (natal 96 / 98), only.
  - **Vesta (busiest) pairs land on the jockey:** Vesta/Pleiades → natal Venus (88); Vesta/Capella → natal Venus (95) and Mercury – only. Jockey Venus 7 kinds, all only (Type 1 Venus/Altair).
- **Royal → body:** **Regulus – Mercury** link L on both charts (81 `**`, 78 `**`), only; **Antares – Quaoar** horse natal 82, only. Light.
- **Losers:** favourite Oot Ma Way (2nd) – no royal of its own; Antares–Pluto and Fomalhaut–Sedna links shared. Poetria (3rd) – 5 exclusive A links, horse Transpluto 5 kinds 8 `**` shared; Rahu/Aldebaran → jockey Juno and Orcus. Fiamette (4th, P21) – Regulus – Transpluto its own. Suntory Star (5th, 80/1) – Antares – Jupiter Type 1.

### R30 Wincanton 21/03/2022 14:20 – River Bray / Alan Johns 22/1 (favourite Ballyblack 10/11, 3rd)
- **Sky:** the busiest non-fast body is a royal star – **Regulus (6)**; then **Makemake (5)**, Sun, Chiron, Ketu, Capella (4). Top pairs Sun/Quaoar 99.4, Chiron/Algorab 99.1, Orcus/Sirius 98.6.
- **Winner – CONCENTRATED on Makemake with Rahu, both charts (C2 fits):**
  - **Exclusive A link Rahu/Makemake 82.9, T1xT1** – a Type 1 on both charts; jockey natal Makemake→Rahu 91 ^.
  - **Pluto/Makemake 96.3:** horse Type 1, and it falls on the jockey's natal Rahu and Venus – only. Rahu/Makemake also falls on the jockey's Venus.
  - **Horse Makemake 7 kinds, jockey Rahu 7 kinds, jockey Makemake 6 kinds – every layer only here.** Horse Jupiter 6 kinds (link Ceres/Jupiter; Type 1 Jupiter/Capella).
  - Horse natal Pallas receives three sky pairs (Sedna/Arcturus, Juno/Bellatrix, Vesta/Castor), only.
- **Royal → body:** the race's busiest body is Regulus, and the winner touches it once of its own – **Regulus – Chiron** (sky Chiron/Regulus; jockey Chiron self 93), only. Everything else royal shared.
- **Losers, more royal:** favourite Ballyblack (3rd) – **Regulus – Haumea** horse natal 96 (only); Gonggong/Aldebaran → horse Eris. Electric Annie (5th; sole holder of the #1 pair, unmatched) – **Aldebaran – Venus** link A both charts (77 `**`, 75 `**`), its own; Haumea/Regulus and Ceres/Regulus → horse Rahu; the most royal (6). Guernesey (2nd) – Chiron/Antares → Gonggong; Haumea/Regulus → Saturn.
- **Seen:** where a royal star is itself the busiest body (R30), the winner holds it lightly and is concentrated elsewhere; the royal-heavy runner loses again.

### R33 Lingfield 06/04/2022 14:25 – Man On A Mission / Luke Morris 12/1 (favourite Judy's Park 13/8, 2nd)
- **Sky:** busiest **Pallas (9)**, Haumea 6, Ketu, Jupiter (5). Top pairs Chiron/Procyon 99.6, Sun/Altair 99.4, Venus/Algol 99.1, **Pallas/Pluto 98.6**, Ceres/Fomalhaut 98.3.
- **Winner – SPREAD across several bodies, each held all-only (P21, C1):**
  - 3 exclusive A links: **Pallas/Polaris 98.1** (busiest body; horse 68 `**`), Jupiter/Quaoar 95.5, Rahu/Haumea 88.3 (Haumea busy). Jockey Type 1 **Pallas/Gonggong 97.2**, only.
  - Horse Uranus 5 kinds (Type 1 Uranus/Alphecca, self), horse Rahu 5 kinds, horse Quaoar 5 kinds – all only. Jockey Jupiter 6 kinds; Jupiter pairs land on the horse's Neptune and Vesta and the jockey's Neptune and Vega, only.
- **Royal → body (all landing on natal bodies, all only):** Ketu/Antares → horse **Quaoar**; **Pallas/Fomalhaut** (busiest body with a royal star) → horse **Sedna**. Regulus–Venus natal pair shared.
- **Losers:** Brazen Idol (4th) holds the same **Fomalhaut – Pallas** inside its own chart (Type 1 89 `**`, self) – royal on the busiest body, own chart, beaten (as R27's favourite: Fomalhaut on Mars). Favourite Judy's Park (2nd) – **Regulus – Mercury** own Type 1; horse Pallas Whole Number 5 kinds, shared, 6 `**` – loud. Bang On The Bell (3rd) – sole holder of #1 Chiron/Procyon, unmatched.

### R36 Newmarket 14/04/2022 15:35 – Eydon / David Egan 22/1 (favourite Masekela 2/1, 2nd)
- **Sky:** busiest **Jupiter (9)**, then Mercury, Pallas, Saturn, Makemake, Sedna (6). Top pairs **Transpluto/Regulus 100.0** (every runner holds it), **Sun/Orcus 99.9 (#2)**, Mercury/Pallas 99.3.
- **Winner – quiet, CONCENTRATED on Orcus (a body of #2):**
  - Exclusive A link **Venus/Orcus 83.0** (jockey Orcus self 96); L links **Chiron/Orcus T1xT1** (horse Orcus→Chiron 87 `**`, jockey Chiron self 86 `**`) and **Uranus/Orcus** (horse natal Orcus→Uranus 99) – all only. Sedna/Castor falls on the jockey's natal Orcus (96), only.
  - **Sedna (busy) pairs land on the jockey:** Sedna/Alkaid → Chiron (99), Sedna/Castor → Orcus, Ceres/Sedna → Transpluto – all only.
  - Jockey Chiron self in Ninths (86 `**`) – David Egan's Chiron in Ninths again (R34, R36 wins).
  - Jupiter (busiest) not held.
- **Royal → body:** none of its own (only Transpluto/Regulus, shared by the field).
- **Losers:** Cresta (5th, 9/4) – **the most royal (9): Regulus – Mercury** own link A both charts + Type 1 99, Fomalhaut – Rahu natal 95, 4 exclusive A links. Favourite Masekela (2nd) – Aldebaran – Chiron link G (own); jockey Mars 5 kinds shared 6 `**` – loud. Austrian Theory (3rd, 25/1) – Fomalhaut – Orcus natal 100 (own), Fomalhaut – Mars link G.
- **Seen:** the winner again holds no royal of its own while the most royal runner loses; Sedna pairs landing on the winner again (R16, R17, R29, R33 via Pallas/Fomalhaut → Sedna, R36).

### R38 Musselburgh 09/05/2022 15:50 – John Kirkup / Connor Beasley 14/1 (favourite The Thin Blue Line 5/6, 5th)
- **Sky:** busiest Uranus (6), then Haumea, Quaoar, Orcus (5). Top pairs **Venus/Sedna 99.6 (#1)**, Ceres/Castor 99.4, Haumea/Alkaid 99.1, Pallas/Alphecca 98.7, **Venus/Quaoar 98.4 (#5)**.
- **Winner – CONCENTRATED on Venus (body of #1 and #5), with the jockey's Jupiter receiving (C2 fits):**
  - Horse Venus 7 kinds: links G Venus/Spica and Venus/Haumea (only), Venus self 95 `**` ^.
  - **#5 pair Venus/Quaoar falls on the jockey's natal Jupiter (97)**, and Quaoar/Fomalhaut on the same Jupiter (88/92) – only. (Same picture as R8 Ropey Guest: Venus concentrated, Jupiter receiving.)
  - Exclusive A links Haumea/Algorab 96.7 (Haumea busy) and Orcus/Betelgeuse 88.2 (Orcus busy; jockey Orcus self 95 `**` ^).
  - Juno/Regulus falls on the horse's natal **Sedna** (82), only. Both-chart midpoint (natal Gonggong at mid of natal Algorab/Neptune, 0.032); three-way Eris (0.074), only.
- **Royal → body (7 items – not light this time):** Fomalhaut – Mercury jockey natal 98 `**` (only); Aldebaran – Gonggong jockey natal 92 (only); Gonggong/Aldebaran → jockey Saturn; Quaoar/Fomalhaut → jockey Jupiter; Juno/Regulus → horse Sedna.
- **Losers:** Rose Bandit (3rd) – **the most royal (14)**: Aldebaran – Saturn own link A both charts, Regulus – Juno Type 1, Quaoar/Fomalhaut and Mercury/Fomalhaut → Ketu. Favourite The Thin Blue Line (5th) – **Regulus – Makemake** own Type 1; jockey Chiron in Ninths 5 kinds. Rory (2nd) – Venus/Regulus → jockey Sedna 98, Mercury/Fomalhaut → horse Vesta.

### R39 Sedgefield 10/05/2022 15:00 – Blue Collar Glory / Craig Nichol 20/1 (favourite Wheres Maud Gone 5/6, 5th)
- **Sky:** busiest **Jupiter (7)**, Eris, Uranus (6). Top pairs Mars/Procyon 99.9, **Chiron/Jupiter 99.4 (#2, Ninths)**, Eris/Capella 99.3.
- **Winner – CONCENTRATED on Chiron/Jupiter, the #2 pair with the busiest body (P20, P21):**
  - Exclusive A link **Chiron/Jupiter on both charts, matched** (horse 88 `**`, jockey 59 `**`); the same pair falls on the jockey's natal Vesta (89/97), only.
  - Exclusive A link Juno/Makemake (jockey Makemake self 97 `**` ^); Juno/Makemake falls on the jockey's natal **Chiron** (98) and Pluto, only. Chiron on both charts.
  - #1 pair Mars/Procyon falls on the horse's natal Quaoar (95), only. G link Ketu/Sun (horse Sun self 95; jockey Sun→Ketu 84 `**`), only.
- **Royal → body:** light – **Antares – Saturn** (horse Saturn self on Saturn/Antares, 90), only; Chiron/Fomalhaut → horse Rahu (shared).
- **Losers:** Bright Sunbird (2nd) – **the most royal (7): Fomalhaut – Chiron** own Type 1, **Fomalhaut – Neptune** own link A both charts. Favourite Wheres Maud Gone (5th) – Chiron–Jupiter natal pair in the wrong family; **Fomalhaut – Quaoar** own natal 85 `**`, Chiron/Fomalhaut → horse Quaoar 99 and jockey Orcus; holds the #1 pair as a shared link, unmatched – loud.
- **Seen:** Fomalhaut sits on Chiron (the winner's body) inside a loser's own chart (Bright Sunbird) – as R27 and R33 (royal on the key body, in the loser's own chart).

### R42 Bath 03/06/2022 17:50 – Little Girl Blue / Luke Morris 10/1 (favourite Soi Dao 13/8, 2nd) – protocol re-read
- **Kind:** CONCENTRATED on Quaoar (the busiest body, 8) – on both charts via the exclusive link Quaoar/Alphecca (horse 90 `**`, jockey Quaoar self); jockey Quaoar 6 kinds and horse Alphecca 5 kinds, all only (P21). Not C2 by the frozen test.
- **Royal → body:** **Sedna/Aldebaran (#2 pair) and Pallas/Aldebaran both fall on the horse's natal Juno** (82, 94), only – Juno receives two Aldebaran pairs (and the fast top pair Eris/PoF); Fomalhaut – Eris horse self (Eris/Fomalhaut 42 `**`), only; Mars/Fomalhaut → Saturn shared. Royal lands on a natal body; Sedna in the #2 pair landing on the winner.
- **Losers:** favourite Soi Dao (2nd) – **the most royal (7)**: Fomalhaut pairs onto the jockey's Juno, Jupiter, Makemake, Transpluto, Vesta; Pallas/Aldebaran → horse Ceres 100; **Aldebaran – Makemake** jockey natal 94 (own); Vesta/Antares (#1) → jockey Jupiter. Between The Sheets (3rd) – Aldebaran – Sedna jockey natal 87 (own), Fomalhaut – Mars shared. Hattie C (4th) – Antares – Vesta natal 91.

### R44 Ripon 16/06/2022 15:25 – Society Red / Oisin Orr 16/1 (favourite Bollin Joan 10/11, 4th) – protocol re-read
- **Kind:** CONCENTRATED on Haumea (the busiest body, 7) – three exclusive A links Rahu/Haumea, Ceres/Haumea, Vesta/Haumea in Ninths (jockey crosses 93/85/94 `**`), horse Haumea self; Haumea on both charts (P21, C2).
- **Rahu as receiver:** the #3 pair **Makemake/Sedna (99.5) falls on the jockey's natal Rahu** (65/92), and **Saturn/Fomalhaut** on the same Rahu (69/73), only; horse Rahu 6 kinds, all only (Chiron/Ketu and Jupiter/Sun fall on the horse's Rahu). Venus/Sedna (98.2) falls on the horse's natal Uranus, only.
- **Royal → body:** light – **Fomalhaut → Rahu** (Saturn/Fomalhaut onto the jockey's natal Rahu), only; Fomalhaut – Transpluto link G shared by the field.
- **Losers:** Commonsensical (2nd) – **the most royal (6)**: **Ceres/Antares falls on the jockey's natal Haumea (the busiest body)**, Ketu and the horse's Pallas; Fomalhaut – Saturn natal; Fomalhaut – Transpluto as its own variant. Favourite Bollin Joan (4th, last) – Ceres/Antares → horse Orcus; its one exclusive link Eris/Mars is two different selves.
- **Seen:** Sedna pairs land on both R42 and R44 winners (Sedna/Aldebaran → Juno; Makemake/Sedna → Rahu, Venus/Sedna → Uranus). A royal star on the busiest body sits with the runner-up, not the winner, again (R44 Antares → Haumea; cf. R27, R33, R39).

### R45 Carlisle 07/07/2022 16:30 – Whitefeathersfall / Franny Norton 10/1 (favourite Million Thanks 13/8, 3rd) – protocol re-read
- **Kind:** CONCENTRATED on the horse's natal Pallas, where the #1 pair (Pallas/Deneb Algedi, natal pair) meets the busiest body Haumea (Saturn/Haumea 93 and Neptune/Haumea 94 fall on natal Pallas, only; hub Deneb Algedi–Pallas–Haumea, only) – P23. No exclusive A link. Not P21. C2 no (exA 0); receiver_busy yes (Pallas receives 3).
- **Sedna:** Sedna/Betelgeuse falls on natal Saturn on **both** charts, only. Sun: jockey natal Sun exact at the midpoint of sky Sun / horse natal Sun (0.001), only.
- **Royal → body:** light (2) – **Ceres/Fomalhaut falls on the horse's natal Juno** (69), only; Regulus–Mars natal pair, shared.
- **Losers:** Aswan (4th, 10/1) – **the most royal (13)**: Regulus–Mars Type 1 and self on the jockey (98 `**`), Regulus–Saturn Type 1 horse, Juno/Regulus → Transpluto, Fomalhaut–Gonggong links on both charts. Favourite Million Thanks (3rd) – Mars/Regulus → jockey Uranus, Regulus–Gonggong natal. Lucia Joy (6th, 28/1) – Ceres/Fomalhaut → jockey Venus (99), Juno/Regulus → horse Sedna. Persist (2nd) – no royal at all.
- **Seen:** the same sky pair Ceres/Fomalhaut lands on the winner's Juno and on a loser's Venus. Royal onto Juno again (R42 too).

### R48 Doncaster 16/07/2022 18:45 – Novakai / Tom Eaves 12/1 (favourite Crackovia 8/15, 2nd) – protocol re-read
- **Kind:** CONCENTRATED on Jupiter with Spica (the second-busiest body) – exclusive A link Jupiter/Spica on both charts (jockey `**` Ninths, Type 1 and Jupiter self 93 `**`); jockey Jupiter 7 kinds. Not P21 (Spica is busy2, not busy1). Not C2.
- **The Sun feeds the winning body:** Sun/Orcus (92) falls on the **jockey's natal Jupiter**, only. **#3 pair Sun/Sedna (98.7) falls on the horse's natal Eris**, only. **Neptune/Fomalhaut falls on the horse's natal Sun** (88), only.
- **Royal → body (5 own):** Fomalhaut → horse Sun (above); Saturn/Antares → jockey Pallas, only; Aldebaran–Mercury horse natal, only. Regulus–Transpluto and Antares–Transpluto are shared by the whole field (say nothing here).
- **Losers:** favourite Crackovia (2nd) – busiest body Haumea, matched link on both charts (P21); Saturn/Antares → jockey Quaoar and Uranus; Regulus–Chiron and Aldebaran–Juno natal, only. Bella Kopella (6th, 40/1) – **the most royal (6 own)**: Vesta/Antares → horse Juno and jockey Ketu, Juno/Aldebaran → jockey Uranus, Fomalhaut pairs → Gonggong, Makemake. Gilded Moon (4th) – Fomalhaut–Quaoar link A both charts, Aldebaran–Mercury self. Mother India (3rd) – no royal of its own, P21.
- **Seen:** Sedna in a top pair lands on the winner again. The Sun on both sides of the winner: as a sky pair onto Jupiter, and as a receiver of a royal pair.

**Check (all 48 races, found by looking – not frozen): which natal body a royal sky pair lands on (Type 2, only this partnership).** Most bodies sit at base. Three stand out among outsiders (9/1+):
- onto natal **Juno**: 11 holders, 4 won; outsiders 5, **4 won** (Madame Tantzy 12/1, Forget You Not 25/1, Little Girl Blue 10/1, Whitefeathersfall 10/1; Bella Kopella 40/1 lost).
- onto natal **Rahu**: 17 holders, 5 won; outsiders 9, 4 won (Nicholas T 14/1, Deja Vue 10/1, Sir Chauvelin 10/1, Society Red 16/1).
- onto natal **Sun**: 16 holders, 3 won; outsiders 7, 3 won (Nicholas T, Sir Chauvelin, Novakai 12/1).
- Juno, Rahu or Sun together, outsiders: **19 holders, 9 won** (against about 1 in 5 for outsiders). Opposite side: onto Uranus 20 holders, 1 won; onto Neptune, Gonggong, Pluto 0 wins.
- Small numbers and picked after looking, so it is a candidate only; it would need freezing and a blind test.

## All 24 outsider winners (9/1+), races 1–48, as seen (2 Oct 2026)
Races 1–24 table: see race-reads-1-24 ("The 12 outsider races in 1–24"). Races 25–48:

| Race | Winner | SP | Kind | C2 | Royal → body on the winner (only here) |
|---|---|---|---|---|---|
| R26 Newcastle | Sir Chauvelin | 10/1 | spread | no | Aldebaran → Mercury, Venus, Sun; Fomalhaut → Quaoar, Rahu, Transpluto |
| R27 Leicester | Nelson River | 20/1 | concentrated – Rahu (jockey) | no | Regulus – Sun natal pair |
| R29 Doncaster | Olympe De Gouges | 25/1 | around the busiest (Chiron, Vesta) | no | Regulus – Mercury link; Antares – Quaoar |
| R30 Wincanton | River Bray | 22/1 | concentrated – Makemake with Rahu | yes | Regulus – Chiron (Regulus the busiest body) |
| R33 Lingfield | Man On A Mission | 12/1 | spread | no | Ketu/Antares → Quaoar; Pallas/Fomalhaut → Sedna |
| R36 Newmarket | Eydon | 22/1 | concentrated – Orcus | no | none of its own |
| R38 Musselburgh | John Kirkup | 14/1 | concentrated – Venus (Jupiter receiving) | yes | 7: Fomalhaut – Mercury, Aldebaran – Gonggong, → Saturn, Jupiter, Sedna |
| R39 Sedgefield | Blue Collar Glory | 20/1 | concentrated – Chiron/Jupiter | no | Antares – Saturn |
| R42 Bath | Little Girl Blue | 10/1 | concentrated – Quaoar (busiest) | no | Sedna/Aldebaran, Pallas/Aldebaran → Juno |
| R44 Ripon | Society Red | 16/1 | concentrated – Haumea (busiest) | yes | Saturn/Fomalhaut → Rahu |
| R45 Carlisle | Whitefeathersfall | 10/1 | concentrated – Pallas (#1 pair meets busiest) | no | Ceres/Fomalhaut → Juno |
| R48 Doncaster | Novakai | 12/1 | concentrated – Jupiter/Spica | no | Neptune/Fomalhaut → Sun |

**Across all 24:**
- Kind: concentrated 14, around the busiest bodies 5, spread 5. 25–48 is mostly concentrated (9 of 12); 1–24 was more mixed.
- C2: 11 of 24 winners (8 in 1–24, 3 in 25–48). Among all outsiders: 21 holders, 11 won.
- Royal pair landing on natal Juno, Rahu or Sun (only here): 9 of 24 winners (R4, R12, R17, R18, R26, R42, R44, R45, R48). Among all outsiders: 19 holders, 9 won.
- C2 and that royal landing together: 7 outsiders, 5 won. Either one: 33 outsiders, 15 won (1–24: 17/8; 25–48: 16/7).
- C2 or the royal landing or P21: 45 outsiders, 18 won. **Outsiders with none of C2, the royal landing, P20 or P21: 56 runners, 4 won (7%)** – the opposite side; the four were R8 Ropey Guest, R15 Heart Throb, R24 Miss Heritage, R36 Eydon.
- Royal amount: the winner was the (joint) most royal runner in only 4 of the 24 outsider races. Across all 48 races the most royal runners win at base (62, 10 won) – being most royal doesn't stop a horse, it just isn't what the outsider winners have. What they have is a few royal pairs landing on their own natal bodies.
- Sedna pairs land on the winner: R16, R17, R29, R33, R36, R38, R42, R44, R45, R48.
- Royal star on a key or busiest body in a loser's own chart: R27, R33, R39, R44.
- **Juno, all layers (Eddie, 2 Oct: "I have seen Juno often appear in winners"):** Juno in general sits at base – any only-here Juno item: outsiders 84, 17 won; sky pairs landing on natal Juno: 39, 7 won; Juno as the busiest sky body: 5 races, 2 outsider winners (R18 Deja Vue, R24 Miss Heritage). What stands out is the royal star with Juno: royal pair landing on natal Juno, outsiders 5, 4 won (R4, R12, R42, R45).
- All of this is in-sample and picked after looking; C2 is frozen, the royal landing on Juno/Rahu/Sun is not yet frozen. Both need a blind test on fresh races.

## C3 – frozen 2 Oct 2026 (in words; not yet in a script)
**C3: a sky pair containing a royal star (Aldebaran, Antares, Fomalhaut or Regulus) falls as a Type 2 on the runner's natal Juno, Rahu or Sun, on horse or jockey, held by this partnership only.** Fast points excluded; old S6-NN items excluded; any score; any family or coordinate. Source: royal_items.csv (royal_record.py v1.0), layer "Type 2", only = 1, body in {Juno, Rahu, Sun}.
- In-sample (races 1–48, found by looking): all runners 41 holders, 10 won; outsiders 9/1+ 19 holders, 9 won. With C2: 7 outsiders, 5 won.
- To be tested blind with C2 and P21 on fresh races. Adding it to blind_test.py waits for Eddie's go-ahead.
- Eddie, 2 Oct: "generally I feel it is the combinations that find the winner which is why most measures always show as average."

## Favourite races – first look (2 Oct 2026)
Every one of the 24 non-outsider races in the 48 was won by the favourite (2/1-ish: 6/5 to 100/30). Same features, winning favourites (24) against beaten favourites (24, all in the outsider races):
- None of C2-shape, C3, P20, P21: winning favourites 15 of 24, beaten favourites 16 of 24 – the outsider signatures are mostly absent on favourites, whether they win or lose.
- A top-3 sky pair (not fast) in an only-here item with a full match `**`: winning favourites 8, beaten favourites 2. P20: 4 against 1. The one clear difference so far.
- Exclusive A links ≥ 2: 9 against 11; busy receiver: 9 against 8; deepest all-only body ≥ 6 kinds: 7 against 5; exact three-ways only here: 10 against 7. Close.
- Royal: average 3.7 against 3.5; most royal in the race 6 against 5. No difference.
- Next: deep reads of the favourite races, two at a time, in date order (R2, R3, R5, R7, R10, R11, R13, R14, R19, R20, R22, R23, R25, R28, R31, R32, R34, R35, R37, R40, R41, R43, R46, R47).

## Favourite races 25–48 (same lens: which pair, onto which body, held how)

### R25 Catterick 14/02/2022 15:15 – Omar Maretti / Kielan Woods 15/8 F (6 runners)
- **Sky:** Ninths 35%. Busiest **Rahu, Orcus (6)**. Top pairs **Rahu/Aldebaran 99.8** (royal + busiest), Pallas/Castor 99.2, Pluto/Pleiades 98.5; Chiron/Orcus 98.5, Haumea/Makemake 95.5, Rahu/Haumea 95.6, Venus/Aldebaran 94.9.
- **Key pairs – who, how, onto which body:**
  - **Rahu/Aldebaran (#1):** Brian Boranha (4th, 18/1) jockey natal pair + → horse Mercury; **Winds Of Fire (PU, 7/1) → jockey Uranus (99)**. The winner doesn't hold it.
  - Pallas/Castor (#2): Marown (PU, 100/30) → horse Eris and Pluto. Pluto/Pleiades (#3): Brian Boranha natal pair.
  - **Chiron/Orcus (busiest):** Winds Of Fire own link A both charts `**` + natal pair (PU); winner jockey Chiron self.
  - Makemake/Rahu (busiest): **Marown own horse Type 1 + natal pair `**`** (PU); The Paddy Pie (3rd) → jockey **Uranus**.
  - **Haumea/Makemake:** only the **winner – horse Type 1 + natal pair Haumea→Makemake 99, and it lands on the jockey's natal Jupiter (96/99)**.
- **Winner – the pair inside the horse's chart and landing on the jockey's Jupiter; both busiest bodies as a natal pair:** horse natal pair **Orcus→Rahu 86** (the two busiest bodies), only; Orcus pairs land on horse Ceres and Eris and twice on jockey Haumea; jockey Jupiter receives Haumea/Makemake and Juno/Bellatrix. Exclusive A Ceres/Arcturus (jockey 95 `**`); G link Pallas/Arcturus (horse Pallas self 96 `**` ^), horse Pallas 6 kinds. Mars three-way (equator at the midpoint of sky / jockey natal, 0.048, certain), only.
- **Royal → body: none of its own.**
- **Losers:** Marown (PU, 100/30) – **the most royal: Antares – Jupiter own link A on both charts + Type 1**, Regulus – Chiron link G both charts; a busiest pair as its own Type 1. Winds Of Fire (PU) – the busiest Chiron/Orcus as its own link; the #1 royal pair onto Uranus. The Paddy Pie (3rd) – Makemake/Rahu onto Uranus, Eris/Regulus → jockey Sedna.

### R28 Newcastle AW 24/02/2022 18:30 – Gowanlad / Phil Dennis 2/1 F (5 runners)
- **Sky:** Ninths 29%. Busiest **Quaoar (10)**, Makemake 8. Top pairs **Sun/Aldebaran 99.7** (royal), Quaoar/Transpluto 99.6, **Mercury/Makemake 99.5**; Saturn/Makemake 97.8, Juno/Pallas 96.4, Quaoar/Venus 95.0, Mars/Makemake 91.2.
- **Key pairs – who, how, onto which body:**
  - Sun/Aldebaran (#1): → Blazing Hot (2nd) jockey Orcus; Tathmeen (3rd) jockey Pallas. The winner doesn't hold it.
  - Quaoar/Transpluto (#2): Tathmeen jockey self; James Watt (4th) natal pair + → jockey Ceres; Alablaq (5th) → jockey Jupiter.
  - **Mercury/Makemake (#3):** **winner → jockey Juno (98/95)**; Blazing Hot → jockey Chiron (2nd); James Watt natal pair (4th); **Alablaq own jockey Type 1 `**` + self `**` (5th, 7/2)**.
  - Saturn/Makemake: Blazing Hot own jockey Type 1 `**` (2nd); Tathmeen → horse Rahu.
  - Mars/Makemake: winner → jockey Pluto; others → Pallas, Ketu, Ceres; James Watt own Type 1 `**`.
  - **Juno/Pallas:** only the **winner – horse Type 1 (inside its own chart), and it lands on the jockey's Venus**.
- **Winner – quiet; the busiest Quaoar matched on both charts; Juno receiving on the jockey:** exclusive A **Quaoar/Algol 84.3 – X Quaoar→Algol `**` on both charts, at or above the sky's score** (P21). **Jockey Juno receives three Makemake/Haumea/Mercury pairs** (#3 Mercury/Makemake, Mercury/Haumea, Haumea/Makemake). Horse Pallas 6 kinds. Jupiter/Arcturus → horse Sun + natal pair.
- **Royal → body: none of its own.**
- **Losers:** Tathmeen (3rd) – **the most royal: Fomalhaut – Chiron and Fomalhaut – Ketu own links on both charts**. James Watt (4th, 9/1) – Fomalhaut – Uranus link G both charts, Venus/Regulus → horse **Uranus** 98. Alablaq (5th) – the #3 pair held as its own Type 1.

### Seen across R25 and R28
- **The pair inside the horse's chart and landing on the jockey** (R25 Haumea/Makemake → jockey Jupiter; R28 Juno/Pallas → jockey Venus) – as R10 Uranus/Haumea (horse Type 1 → jockey Sun).
- **Winners with no royal item of their own:** R22, R25, R28. The most royal runner lost both (Marown PU, Tathmeen 3rd), each holding the royal star with Jupiter/Chiron/Ketu as its own link across both charts.
- The top pairs held as own Type 1 or link: Alablaq 5th, Marown PU, Winds Of Fire PU.
- **Uranus:** R25 Winds Of Fire (Rahu/Aldebaran) PU, The Paddy Pie (Makemake/Rahu) 3rd; R28 James Watt (Venus/Regulus) 4th.
- **Juno receiving the #3 pair** on the winning jockey (R28) – Juno again.

### R31 Haydock 23/03/2022 13:35 – Soldier Of Destiny / Gavin Sheehan 13/8 F (5 runners)
- **Sky:** Ninths 39%. Busiest **Sun, Vesta (7)**. Top pairs Mars/Betelgeuse 99.5, **Pallas/Sun 99.4**, **Sun/Vesta 99.4**; Venus/Vesta 98.3, Jupiter/Regulus 96.0 (royal).
- **Key pairs – who, how, onto which body:**
  - Mars/Betelgeuse (#1): Burrows Diamond (2nd) natal pair; Dreams Of Home (3rd) → horse Saturn; Nero Rock (UR, 11/1) jockey self `**`.
  - **Pallas/Sun (#2, busiest):** **winner – jockey natal pair Pallas→Sun 90**; Nero Rock own horse Type 1 `**` + self `**` (UR).
  - Sun/Vesta (#3): Ubetya (4th) natal pair `**`.
  - **Venus/Vesta (busiest):** **winner – jockey Type 1 `**`** (inside its own chart); Ubetya → horse **Uranus**, jockey Mercury, Transpluto (4th).
  - Pallas/Vesta: → Dreams Of Home Quaoar (3rd), Nero Rock Ketu, Mercury (UR). Procyon/Vesta: Nero Rock own Type 1 `**`.
- **Winner – quiet in A links (none), many low links; both busiest bodies inside the jockey's chart:** jockey Venus/Vesta Type 1 and Pallas→Sun natal pair; G link Saturn/Vesta (Vesta self 87 `**` ^); jockey Vesta 6 kinds. **Jockey natal Ceres receives four pairs** (Eris/Rahu, Neptune/Alkaid, Pluto/Rahu, Eris/Pluto); Juno/Gonggong → jockey Sun; Mars/Sun → jockey Quaoar. L link Chiron/Betelgeuse X on both charts 94/96 `**` ^.
- **Royal → body:** **Antares – Chiron link G on both charts** (79 `**`, 85), only. Light.
- **Losers:** Burrows Diamond (2nd) – **Regulus – Pallas own link A on both charts + natal pair**. Dreams Of Home (3rd) – **Regulus – Vesta link G (Vesta busiest)**. Ubetya (4th) – Aldebaran – Rahu link L and Aldebaran – Venus link G; Venus/Vesta onto Uranus. Nero Rock (UR) – the #2 pair held as its own Type 1.

### R32 Musselburgh 25/03/2022 16:05 – Hold Onto The Line / Alan Doyle 100/30 F (7 runners)
- **Sky:** Ninths 29%. Busiest **Pallas, Chiron, Neptune (7)**. Top pairs Ceres/Aldebaran 99.3 (royal, conjunction), **Venus/Quaoar 99.2**, Transpluto/Bellatrix 99.2; Uranus/Aldebaran 97.5, Gonggong/Regulus 93.7, Neptune/Betelgeuse 93.1, Juno/Aldebaran 89.3, Haumea/Fomalhaut 89.7.
- **Key pairs – who, how, onto which body:**
  - **Venus/Quaoar (#2):** only the **winner – natal pair Quaoar→Venus on both charts (horse 92 `**`), and it lands on the horse's natal Vesta**.
  - Transpluto/Bellatrix (#3): **Balranald (6th, 11/1) holds it every way – own link A both charts `**`, Type 1, self**.
  - **Neptune/Betelgeuse (busiest):** **winner horse Type 1 `**` + natal pair `**` + self `**`**; Balranald → horse Eris.
  - Gonggong/Regulus (royal): **Petite Rhapsody (2nd) own link A both charts `**`** + → horse Vesta.
  - **Juno/Aldebaran (royal):** **winner → horse Venus (90/82)** + Aldebaran – Juno self; Brandy McQueen (4th) → Transpluto; Keep The Faith (5th) → Ceres, Orcus; Balranald (6th) → Pluto; City Derby (3rd) jockey natal pair.
  - **Haumea/Fomalhaut (royal):** **winner → jockey Mars**; City Derby (3rd) → jockey Sun (C3); Balranald (6th) → jockey Jupiter; Keep The Faith natal pair.
  - Chiron/Vesta (busiest): Brandy McQueen (4th) own jockey Type 1 `**`, and → jockey **Uranus**.
- **Winner – quiet (no exclusive A link); the #2 pair inside both charts, the busiest Neptune inside the horse's chart:** horse Neptune 6 kinds, all only (Type 1s Neptune/Betelgeuse and Neptune/Sun); horse Sun self; horse Venus receives Juno/Aldebaran; jockey natal pair Pallas→Sirius (Pallas busiest). Jupiter three-way (jockey natal at the midpoint of sky / horse, 0.072, certain), only.
- **Royal → body:** Juno/Aldebaran → horse **Venus**; Haumea/Fomalhaut → jockey **Mars**; Aldebaran – Juno self. Light (3).
- **Losers:** Petite Rhapsody (2nd) – Regulus – Gonggong as its own link A both charts. Balranald (6th) – the #3 pair held every way. City Derby (3rd) – Haumea/Fomalhaut onto the Sun.

**Check (all 48): a royal star held as the runner's own link across both charts (only here), by band.** Sky pair 80+ (link A): **32 runners, 0 won** – Antares 5, Fomalhaut 10, Aldebaran 6, Regulus 11. Sub-80 (link G 65–80 or L 50–65): 51 runners, 9 won. **Antares as a low link: 13 runners, 4 won – all winning favourites** (R2 Cuban Cigar L Sedna, R19 Mercian Hymn L Gonggong, R20 Shakem Up'arry G Gonggong, R31 Soldier Of Destiny G Chiron). As seen: the royal star as a strong own link across both charts never won; held low, Antares sat with four winning favourites.

**Eddie (2 Oct): "I wonder about some of the other fixed stars in a similar way."** All 22 fixed stars, held only here – as the runner's own link across both charts (A = sky pair 80+; G/L = under 80) or as a sky pair (80+) landing on a natal body:
- **The other 18 stars as a strong own link (A): 203 runner-star holdings, 39 won (19%) – at or above base.** So "strong own link never wins" belongs to the royal stars (32, 0 won), not to fixed stars in general.
- **Spica is low every way:** strong link 17, 2 won; low link 17, 1 won; landing 29, 2 won – 5 of 63 (8%).
- Higher as a strong own link (small): Bellatrix 10, 4 won; Betelgeuse 5, 2; Arcturus 14, 4; Vega 16, 4; Pleiades 7, 2.
- Low links with no wins: Pleiades 17, Vega 10, Alphecca 10.
- Landing, most stars sit at 14–24% (base 16%); Castor 23%, Sirius 24%, Aldebaran 22% highest; Algol 12%, Spica 7% lowest.
- Pointers only (22 stars × 3 ways, small cells). Spica is the one consistent across all three ways.

### R34 Kempton AW 08/04/2022 18:30 – King Francis / David Egan 5/4 F (6 runners)
- **Sky:** Ninths 39%. Busiest **Juno (9)**, Vesta 8, Haumea 7. Top pairs Vesta/Procyon 100.0, Juno/Pleiades 99.8, **Jupiter/Alkaid 99.6**; **Vesta/Sedna 99.6**, Chiron/Regulus 99.1 (royal), Juno/Antares 94.6, Juno/Sun 91.7.
- **Key pairs – who, how, onto which body:**
  - Vesta/Procyon (#1): **Ilhabela Fact (2nd, 9/1) own horse Type 1 `**` + self `**`**; Culture (4th) → jockey Sun.
  - Juno/Pleiades (#2): Busby (3rd) → jockey Sedna.
  - **Jupiter/Alkaid (#3):** **winner → horse Uranus (71/64) and jockey Chiron (97/81)**; Busby horse self (3rd).
  - **Vesta/Sedna (busy):** **winner → horse Jupiter (96/96) and Gonggong**; Ilhabela Fact own link A + jockey Type 1 `**` (2nd); → Busby Neptune (3rd), Culture Venus (4th), Settle Petal Haumea (6th).
  - Juno/Sun (busiest): Ilhabela Fact own link A both charts `**`; Culture own horse Type 1 `**` (4th); Busby → Neptune.
  - Juno/Antares (royal + busiest): → Culture jockey Jupiter (4th); Ilhabela Fact self; Settle Petal natal pair `**` (6th).
- **Winner – the #3 pair and a busy pair landing; an exclusive link inside both charts:** exclusive A **Ceres/Pluto 88.8** – horse natal pair Ceres→Pluto 87 `**`, jockey Type 1 (X 95 `**` ^) – Ceres 6 kinds on the jockey, Pluto and Ceres 4 kinds on the horse, all only. Exclusive A Mars/Deneb Algedi (natal on both charts). Jockey Juno (busiest) receives Ceres/Sedna. Chiron three-way (certain, 0.072) and Vesta three-way, only.
- **Royal → body: none of its own** (fourth winner with none: R22, R25, R28, R34).
- **Uranus:** Jupiter/Alkaid lands on the winner's horse Uranus – a Jupiter pair onto Uranus that won (the earlier "placed, not won" Jupiter group counted only busy or royal pairs; this one is neither).
- **Losers:** Ilhabela Fact (2nd) – the #1 pair, Vesta/Sedna and Juno/Sun all held as its own; **Fomalhaut – Vesta horse Type 1 + self 95 `**`** (royal on a busy body in its own chart). Busby (3rd, 9/4) – **Antares – Jupiter link G on both charts** (a low Antares link that lost). Culture (4th) – Juno/Sun own Type 1; Juno/Antares → Jupiter.

### R35 Newmarket 12/04/2022 16:45 – Educator / Tom Marquand 11/4 F (7 runners)
- **Sky:** Ninths 32%. Busiest **Mars (7)**, then Uranus, Haumea, Jupiter, Sun, Ceres, Quaoar (6). Top pairs Orcus/Polaris 99.8, **Mars/Sirius 99.6**, Neptune/Uranus 98.9; Sun/Antares 96.0, Makemake/Sun 91.6, Mars/Regulus 90.7, Mars/Antares 82.1, Mars/Aldebaran 84.1.
- **Key pairs – who, how, onto which body:**
  - Orcus/Polaris (#1): **High Fibre (2nd) own link A both charts `**`**; Israr (3rd) self `**`; Mr Alan (6th) natal pair.
  - **Mars/Sirius (#2, busiest):** only the **winner → horse Transpluto (94/93)**.
  - Neptune/Uranus (#3): High Fibre own link A (2nd); → Independent Act Pallas (4th), Mr Alan Eris (6th).
  - **Mars with the royal stars:** Mars/Regulus → **winner horse Vesta**; Mars/Antares → **winner horse Transpluto** (+ jockey natal pair Antares→Mars), High Fibre jockey Gonggong (2nd), Wind Your Neck In jockey Chiron (7th); Mars/Aldebaran → **winner jockey Makemake**, Israr natal pair (3rd).
  - Sun/Antares: **Israr own link A both charts `**` + self** (3rd); Wind Your Neck In → Quaoar (7th).
  - Makemake/Sun: winner → horse Transpluto; High Fibre own link A + Type 1 `**` (2nd); → Independent Act Mars, Mr Alan Venus.
- **Winner – concentrated on the busiest Mars, its pairs landing on the horse's natal Transpluto, Vesta and Orcus:** horse natal **Transpluto receives Mars/Sirius, Mars/Antares and Sun/Makemake**; Mars/Sun → Orcus on both charts. One exclusive A link Pluto/Alkaid (jockey `**` ^). Horse Type 1 Venus/Quaoar; horse Venus 6 kinds.
- **Royal → body:** Mars/Antares → horse **Transpluto**, Mars/Regulus → horse **Vesta**, Mars/Aldebaran → jockey **Makemake**; Antares – Mars and Regulus – Vesta natal pairs; Regulus – Transpluto link L both charts. **The most royal runner in the race won here** – every royal pair with Mars (the busiest), and all landing or natal, none held as a strong own link.
- **Losers:** High Fibre (2nd) – #1, #3 and Makemake/Sun held as its own links. Israr (3rd) – Antares – Sun as its own strong link; Haumea/Rigel → jockey **Uranus**. Independent Act (4th) – **Regulus – Uranus own link A both charts**. Wind Your Neck In (7th) – Jupiter/Venus and Haumea/Rahu → jockey **Uranus**.

### Seen across R34 and R35
- **Own strong links on the top pairs lost again:** Ilhabela Fact (#1, 2nd), High Fibre (#1 and #3, 2nd). The royal strong own link lost again: Israr (Antares – Sun), Independent Act (Regulus – Uranus).
- **The busiest body's pairs landing on the winner's natal bodies:** R35 Mars pairs onto Transpluto, Vesta, Orcus, Makemake (royal Mars pairs included); R34 Vesta/Sedna onto Jupiter.
- R35 is the first favourite race read where the most royal runner won – its royal stars all came through the busiest body, landing.
- R34: a low Antares link lost (Busby 3rd); a Jupiter pair onto Uranus won (King Francis).

### R37 Chester 05/05/2022 13:30 – Look Out Louis / Jason Hart 2/1 F (7 runners)
- **Sky:** Ninths 29%. Busiest **Mars (7)**, then Sun, Ceres, Haumea (6). Top pairs Sun/Vega 100.0, Ceres/Pluto 99.7, **Rahu/Polaris 99.5**; Mars/Aldebaran 97.6 (royal + busiest), Mars/Sedna 97.3, Venus/Fomalhaut 97.2.
- **Key pairs – who, how, onto which body:**
  - Sun/Vega (#1): winner jockey self; Count d'Orsay (2nd) jockey self `**`.
  - Ceres/Pluto (#2): **Militia (6th) own jockey Type 1 `**` + natal pair `**`**, and → jockey Venus.
  - **Rahu/Polaris (#3):** **winner horse Type 1 `**`** (inside its own chart); Militia self.
  - **Mars/Aldebaran (royal + busiest):** **winner → horse Eris (88/92)**; Night On Earth (3rd) → horse Saturn; Militia (6th) → horse Sun (C3).
  - **Mars/Sedna (busiest):** **winner → jockey Chiron**; Count d'Orsay → Quaoar (2nd); Mokaatil → Makemake (4th); **Sunday Sovereign own link A both charts + Type 1 `**`** (5th).
  - Pallas/Aldebaran and Pallas/Regulus (royal): **winner → horse Vesta**; Count d'Orsay own Aldebaran – Pallas link A both charts (2nd); Militia own Regulus – Pallas link A (6th); → Mokaatil Mars, Bossipop Mercury, Count d'Orsay Sun.
- **Winner – quiet (no exclusive A link); the #3 pair inside the horse's chart, the Mars pairs landing:** horse Type 1s Rahu/Polaris and Rahu/Haumea; horse Rahu 5 kinds; Mars pairs land on horse Eris and Orcus, jockey Chiron and Haumea; horse Vesta receives two royal Pallas pairs. G links Juno/Vesta and Venus/Vesta (horse Juno self 88).
- **Royal → body:** Mars/Aldebaran → horse **Eris**; Pallas/Aldebaran and Pallas/Regulus → horse **Vesta**; Aldebaran – Gonggong horse self 97 `**`. All landing or self; none as a link.
- **Losers:** **Count d'Orsay (2nd) – Aldebaran – Pallas own link A both charts. Militia (6th) – Regulus – Pallas own link A + the #2 pair as its own.** Bossipop (7th) – Regulus – Makemake link G. Sunday Sovereign (5th) – the busiest Mars/Sedna as its own link; Chiron/Haumea → jockey Uranus. Night On Earth (3rd) – Ceres/Deneb Algedi → horse Uranus.

### R40 Bath 11/05/2022 19:30 – Mrembo / Hector Crouch 11/4 F (8 runners)
- **Sky:** Ninths 33%. Busiest **Orcus, Eris (7)**. Top pairs Orcus/Procyon 99.6, **Rahu/Haumea 99.5**, Vesta/Orcus 99.2; Orcus/Bellatrix 98.3, Ceres/Aldebaran 97.1, Eris/Regulus 96.7 (royal + busiest), Venus/Aldebaran 94.3, Eris/Antares 93.6.
- **Key pairs – who, how, onto which body:**
  - Orcus/Procyon (#1): **Delahoussaye (3rd, 100/30) own jockey Type 1 `**` + self `**`**.
  - **Rahu/Haumea (#2):** **winner → horse Saturn (92/98)**; **Delahoussaye holds it every way – own link A both charts `**`, Type 1 both**, and → jockey Ketu (3rd); Falmouth Ballerina → jockey Venus (6th).
  - Vesta/Orcus (#3): The Residencies → horse Chiron (4th).
  - **Orcus/Bellatrix (busiest):** **winner → horse Rahu and jockey Haumea**; **The Residencies own link A both charts + Type 1 `**`** (4th); Rockade → Ketu (8th).
  - **Eris/Regulus (royal + busiest):** **Falmouth Ballerina (6th, 33/1) own jockey Type 1 + natal pair + self `**`**, and → horse Venus; Rockade (8th) → Sun on both charts (C3).
  - **Juno/Antares (royal):** **winner → jockey Haumea (97/78)**; Delahoussaye → Mars (3rd); By Pass → Gonggong, Makemake (5th); Falmouth Ballerina → Rahu (6th, C3).
  - Venus/Aldebaran: **Lark Lane (7th) own link A both charts `**`** + → Eris, Mars.
- **Winner – quiet (no exclusive A link); the jockey's natal Haumea as the receiver:** **jockey Haumea receives five pairs** – Orcus/Bellatrix (busiest), Juno/Saturn, Saturn/Capella, Juno/Antares (royal), Juno/Capella – all only; jockey Haumea self. Jupiter/Orcus → horse Pluto and jockey Sun. Jockey Chiron 6 kinds.
- **Royal → body (light):** Juno/Antares → jockey **Haumea**; Fomalhaut – Haumea self `**`.
- **Losers:** Delahoussaye (3rd) – the #1 and #2 pairs held as its own. The Residencies (4th) – the busiest Orcus/Bellatrix as its own link. **Lark Lane (7th) – Aldebaran – Venus own link A.** Falmouth Ballerina (6th) – Regulus on the busiest Eris in its own chart.

### Seen across R37 and R40
- **Royal star as a strong own link across both charts lost again here** (Count d'Orsay 2nd, Militia 6th, Lark Lane 7th) – these are among the 32 already counted in the all-48 check (0 won); the count stays 0 of 32.
- **The same royal pair onto different bodies:** Mars/Aldebaran – Eris 1st, Saturn 3rd, Sun 6th; Juno/Antares – Haumea 1st, Mars 3rd, Gonggong/Makemake 5th, Rahu 6th.
- **Top and busiest pairs held as own links lost:** Delahoussaye (#1, #2), The Residencies, Militia (#2), Sunday Sovereign.
- **Winners quiet in A links** (R37, R40 – none), the key pairs landing on one or two natal bodies (R40 jockey Haumea ×5).

### R41 Chelmsford AW 02/06/2022 18:00 – Tahani / Hollie Doyle 6/4 F (7 runners)
- **Sky:** Ninths 37%. Busiest **Juno (6)**, then Sun, Fomalhaut, Makemake, Procyon, Saturn (5). Top pairs **Makemake/Aldebaran 99.9** (royal), Juno/Neptune 99.5, Rahu/Polaris 99.5; Sun/Altair 99.3, Sun/Makemake 97.8, Fomalhaut/Sedna 94.2, Rahu/Saturn 93.4.
- **Key pairs – who, how, onto which body:**
  - **Makemake/Aldebaran (#1, royal):** **winner – jockey Type 1 + natal pair + self, all `**` (inside the jockey's chart), and it lands on horse Venus and jockey Orcus**; Reckon I'm Hot (2nd) → horse Juno and jockey Sun (C3); Beloved Of All (7th) → jockey Neptune + self; Vienna Poppy (6th, 150/1) self.
  - Juno/Neptune (#2, busiest): Glasstrees (3rd) and Cabeza De Llave (4th) jockey self `**`; Vienna Poppy → Vesta; Beloved Of All natal pair + self.
  - Rahu/Polaris (#3): Tabeeb (5th) natal pair.
  - Rahu/Saturn: **winner jockey natal pair `**`, and → horse Eris**.
  - Eris/Saturn: **Cabeza De Llave own link A both charts + Type 1 `**`** (4th).
  - Sun/Makemake: Tabeeb own horse Type 1 `**` + self (5th); Glasstrees natal pair.
- **Winner – concentrated on Makemake inside the jockey's chart, with the royal #1 pair:** exclusive A Makemake/Betelgeuse (natal on both charts, horse 95 `**` ^); **jockey Makemake 7 kinds, all only**; jockey Aldebaran 4 kinds. L links Rahu/Quaoar and Sun/Procyon (both charts `**`). P20.
- **Royal → body:** Makemake/Aldebaran **inside the jockey's chart** (Type 1, natal pair, self) and landing on horse **Venus** and jockey **Orcus**; Quaoar/Fomalhaut → jockey **Venus** (91); Antares – Jupiter horse self. The most royal runner – and it won, with the royal #1 pair held inside a chart and landing, not as a link.
- **Losers:** Reckon I'm Hot (2nd) – the royal #1 pair onto Juno and Sun. Cabeza De Llave (4th) – Eris/Saturn as its own link. Beloved Of All (7th) – Ketu/Fomalhaut → Pallas and Sun (C3), Makemake/Aldebaran → Neptune.

### R43 Chester 11/06/2022 14:10 – Copper Knight / Sean Kirrane 5/2 F (8 runners)
- **Sky:** Ninths 41%. Busiest **Quaoar (8)**, then Eris, Jupiter, Chiron (7). Top pairs Mercury/Capella 99.9, **Eris/Jupiter 99.9**, Eris/Sirius 99.9; Quaoar/Sedna 99.0, Chiron/Vesta 98.7, Sun/Regulus 97.6 (royal), Eris/Mars 97.5.
- **Key pairs – who, how, onto which body:**
  - Mercury/Capella (#1): Lord Riddiford (7th) → jockey Ketu.
  - **Eris/Jupiter (#2, busy):** **Count d'Orsay (3rd) holds it every way – own link A and Type 1 both charts, selves**, and → jockey Polaris; Gabrial The Devil (6th) → Saturn + self; Lord Riddiford → Ceres; Night On Earth (8th) → Quaoar, Haumea.
  - Eris/Sirius (#3): Lord Riddiford natal pair.
  - **Quaoar/Sedna (busiest):** **Glory Fighter (2nd) own horse Type 1 `**` + self `**`**; Rebel At Dawn natal pair (4th); Lord Riddiford → Chiron, Mercury.
  - Sun/Regulus (royal): Glory Fighter → jockey **Uranus** (2nd); Militia → horse Venus (5th).
  - Eris/Mars: Lord Riddiford own Type 1 `**` + self (7th); → Count d'Orsay Pluto, Militia Sun, Gabrial Haumea.
  - Alkaid/Chiron: Night On Earth own link A + Type 1 (8th).
  - The winner holds none of the top three or busiest pairs.
- **Winner – the quietest runner (no exclusive link at all); busy bodies inside the horse's chart, pairs landing on Orcus and Transpluto:** horse natal pairs **Jupiter→Quaoar 80** (two busy bodies) and **Sun→Transpluto 94** (Sun/Transpluto 96.6), only; horse Sun 6 kinds. Chiron/Gonggong (Chiron busy) → horse Transpluto and jockey Orcus; Makemake/Sedna → horse Neptune and Orcus; Mars/Sedna → horse Orcus; Chiron/Eris → horse Transpluto. Horse Type 1 Vesta/Betelgeuse 90.0.
- **Royal → body (light, 1):** Regulus – Neptune jockey self 88 `**`.
- **Losers:** Count d'Orsay (3rd) – the #2 pair held every way; **Fomalhaut – Pluto own Type 1 `**`**; Regulus – Jupiter link G. Glory Fighter (2nd) – the busiest pair as its own Type 1; Sun/Regulus onto Uranus. Lord Riddiford (7th) – Eris/Mars as its own Type 1.

### Seen across R41 and R43
- **Two ways of winning, side by side:** R41 – the royal #1 pair held *inside* the jockey's chart and landing on Venus and Orcus (the most royal runner won); R43 – the quietest runner, holding none of the top pairs, with two busy bodies as a natal pair in the horse's chart and Chiron/Sedna pairs landing on Orcus and Transpluto.
- **Busiest / top pairs held as own links or Type 1 lost again:** Count d'Orsay (#2), Glory Fighter (busiest), Cabeza De Llave, Lord Riddiford, Night On Earth, Tabeeb.
- **Royal pair onto Uranus, placed:** Glory Fighter 2nd (Sun/Regulus).
- **Same royal pair onto different bodies (R41 Makemake/Aldebaran):** inside the chart + Venus/Orcus 1st; Juno/Sun 2nd; Neptune 7th.

### R46 Windsor 11/07/2022 19:05 – Lequinto / Andrea Atzeni 11/4 F (7 runners) – protocol re-read
- **Sky:** busiest **Saturn (8)**, Pallas 7. Top pairs Pallas/Antares 99.7 (royal), **Ketu/Mars 99.7**, Rahu/Procyon 99.2; Saturn/Rigel 97.0.
- **Key pairs – who, how, onto which body:**
  - Pallas/Antares (#1): Zim Baby → horse Mercury (5th).
  - **Ketu/Mars (#2):** **winner own link A on both charts – horse natal pair Mars→Ketu 74 `**`**; → A Sure Welcome Neptune (4th), Zim Baby Chiron (5th), Impeach Venus (7th).
  - Rahu/Procyon (#3): **King Of Jungle own link A both charts (2nd)**; Impeach self (7th).
  - **Saturn/Rigel (busiest):** **winner own link A both charts – horse X Saturn→Rigel 88 `**`, jockey natal pair Rigel→Saturn 88**.
- **Winner – loud *and* inside the charts: four exclusive A links, each also a natal pair in at least one chart** (Ketu/Mars, Saturn/Rigel, Vesta/Rigel – horse natal pair 93 + X 94 `**`, Neptune/Algol); horse Rigel 7 kinds, Vesta 6. **Horse natal Uranus receives four pairs** – Ketu/Pleiades, Ketu/Pallas, Eris/Pleiades, Pallas/Pleiades (Pallas busy) – a winner with Uranus receiving, through Ketu/Pallas/Eris/Pleiades (none of the "placed, not won" set). Rahu/Algol → horse Mars; Neptune/Algol → horse Saturn.
- **Royal → body (light, 1):** Mercury/Antares → jockey **Ceres**.
- **Losers:** Amazonian Dream (6th) – **Fomalhaut – Saturn own link A both charts** (royal on the busiest body, as its own strong link); Regulus – Uranus natal 97. King Of Jungle (2nd) – the #3 pair as its own link (no natal pair in either chart); Uranus/Regulus → Ketu.

### R47 Chepstow 14/07/2022 16:00 – Beryl Burton / Faye McManoman 11/8 F (6 runners) – protocol re-read
- **Sky:** busiest **Mars, Uranus, Spica, Sun (7)**. Top pairs Saturn/Castor 99.9, **Eris/Quaoar 99.8**, Vesta/Algorab 99.6; Ketu/Mars 99.2, Pallas/Uranus 99.5, Mars/Uranus 97.0, Saturn/Fomalhaut 97.4.
- **Key pairs – who, how, onto which body:**
  - **Saturn/Castor (#1):** **winner → jockey Sedna (85/70)**; Study The Stars (2nd) horse natal pair + → jockey Jupiter, Pluto.
  - **Eris/Quaoar (#2):** **winner own link A both charts – natal pair Eris→Quaoar on both charts (95, 43 `**`)**; City Escape (4th) self + → Orcus.
  - Vesta/Algorab (#3): → Study The Stars Venus (2nd), Tio Mio Ketu (3rd), City Escape Sedna (4th); Regulator self (5th).
  - **Ketu/Mars (busiest):** **winner → horse Sedna**; **Study The Stars holds it every way – own Type 1 `**`, link A `**`, selves** (2nd); → City Escape Juno, Regulator Venus.
  - Mars/Uranus (busiest ×2): **winner → horse Vesta and jockey Rahu**; → Tio Mio Ketu, City Escape Juno; **Pedro De Styles own Type 1 `**` + natal pair** (6th, 50/1).
  - Saturn/Fomalhaut (royal): winner horse self `**`; Pedro De Styles jockey natal pair `**` + Quaoar/Fomalhaut → Saturn (6th).
- **Winner – loud and on the busy bodies, both charts:** 4 exclusive A links – Eris/Quaoar (#2), **Mars/Spica** (two busiest bodies; jockey Type 1, horse natal 96), Rahu/Makemake, **Sun/Transpluto** (horse natal pair 91); jockey Mars 8 kinds; horse Sun 6 kinds (Pluto/Alphecca and Pluto/Alkaid → horse Sun). **Sedna receives on both charts** (Saturn/Castor #1 → jockey; Ketu/Mars → horse).
- **Royal → body:** Ceres/Fomalhaut → horse **Haumea** and jockey **Pallas**; Fomalhaut – Saturn horse self 42 `**`.
- **Losers:** Study The Stars (2nd) – the busiest Ketu/Mars held every way as its own (no natal pair). Pedro De Styles (6th) – Mars/Uranus own Type 1; Fomalhaut – Saturn natal. City Escape (4th) – Aldebaran – Jupiter link L.

### Seen across R46 and R47 (the last two favourite races)
- **The winners hold top/busiest pairs as their own links – but each link is also a natal pair inside at least one chart** (R46 Mars→Ketu, Rigel→Saturn, Rigel→Vesta; R47 Eris→Quaoar both charts, Mars→Spica, Sun→Transpluto). The losers holding top/busiest pairs as own links had no natal pair of their own on them (R46 King Of Jungle #3; R47 Study The Stars Ketu/Mars – Type 1 and selves only).
- **Sedna receiving on both charts** (R47), **Uranus receiving four non-losing-set pairs** (R46).
- Royal light on both winners; R46 Amazonian Dream – royal on the busiest body as its own strong link – 6th.

## Count across all 48 – how the top-3 and busiest-body pairs are held (2 Oct 2026)
The reads of the 24 favourite races gave an impression: winners keep the top/busiest pair *inside* a chart (Type 1 or natal pair) and *receive* the key pairs; losers hold them as *own links across both charts*. Counted (only-here items, sky pair 80+, top 3 or containing the busiest body; each runner placed in a class per pair):

| How the pair is held | Runners | Won | Rate |
|---|---|---|---|
| lands only (Type 2) | 242 | 38 | 16% |
| natal pair only | 96 | 20 | 21% |
| self only | 92 | 14 | 15% |
| own link A + a natal pair in a chart | 62 | 10 | 16% |
| Type 1 with a natal pair | 43 | 8 | 19% |
| natal pair + lands | 41 | 5 | 12% |
| own link A, no natal pair | 30 | 8 | 27% |
| Type 1 (cross/self only) | 28 | 7 | 25% |
| Type 1 with natal pair + lands | 14 | 1 | 7% |

**The impression does not hold as a general rule – every way of holding these pairs is close to base (16%).** Own links without a natal pair, which looked like the losing side in the reads, are 8 of 30. What did hold in a count is narrower: the **royal star** as a strong own link across both charts (32, 0 won), and specific pair-onto-body combinations (Gonggong/Arcturus onto Neptune/Chiron, Uranus with the Neptune/Jupiter/Regulus/Quaoar/Antares/Ceres pairs, royal pairs onto Juno/Rahu/Sun for outsiders). As Eddie said: it's the combinations – the single "held how" class averages out.

## Outsider winners 25–48 – second pass with pair_body grids (read for the first three; "say what you see")

### R26 Newcastle AW 15/02 – 1 Sir Chauvelin 10/1, 2 Onesmoothoperator 13/8 F, 3 Aced It 9/1 (second pass, grid)
- Sky: busiest Ketu, then Makemake. Top pairs Algorab/Sun 99.5, Makemake/Transpluto 98.5, Chiron/Spica 97.8. None of the top or busiest pairs are held by the first three except Makemake/Transpluto (Aced It).
- **1st Sir Chauvelin – everything under 90, all landing, on the horse:** Aldebaran/Ceres → horse Mercury and Venus, jockey Sun; Fomalhaut/Sun → horse Quaoar, Rahu, Transpluto; Algorab/Juno → horse Sun; Ceres/Polaris → horse Rahu; Makemake/Sedna → horse Rahu (**horse Rahu receives three**); Deneb Algedi/Gonggong → jockey Sedna; Betelgeuse/Ketu → jockey Gonggong. Natal pairs Betelgeuse/Ceres (jockey), Makemake/Rahu (horse); selves Neptune/Saturn, Pluto/Sirius (jockey). No own links.
- **2nd Onesmoothoperator (fav) – the Jupiter pairs as its own:** Jupiter/Venus own link + Type 1 + self on both charts; Jupiter/Sedna own link + horse Type 1 + jockey natal pair, and → horse Venus, jockey Chiron; Jupiter/Makemake jockey Type 1 + self; Pluto/Uranus jockey Type 1; Eris/Haumea own link + → horse Uranus; Neptune/Saturn → horse Rahu.
- **3rd Aced It – the horse's Juno receives three:** Makemake/Transpluto (#2), Haumea/Makemake, Haumea/Transpluto → horse Juno; Jupiter/Venus → horse Vesta; Jupiter/Makemake → horse Pallas; Chiron/Gonggong → horse Jupiter, jockey Saturn; natal pairs Neptune/Saturn, Orcus/Polaris. No own links.
- Unplaced: Wise Eagle (4th) – Jupiter/Sedna → jockey Uranus, Algol/Uranus jockey Type 1, Bellatrix/Saturn horse Type 1, Fomalhaut/Mars → Sedna. Resumption (5th, 7/4) – own links Haumea/Makemake, Chiron/Ketu, Makemake/Rahu (+ self). Alba Rose (6th) – Polaris/Venus natal pairs both charts + link + Type 1; Chiron/Orcus, Juno/Sirius Type 1s.
- Seen: Jupiter/Venus – own every way on the favourite (2nd); landing on Aced It's Vesta (3rd), Wise Eagle's Eris. Neptune/Saturn – winner jockey self; Onesmoothoperator → Rahu; Aced It natal pair. Each of the first three gathers pairs on one natal body: winner horse Rahu (×3), Aced It horse Juno (×3); Onesmoothoperator holds its Jupiter pairs as its own.

### R27 Leicester 17/02 – 1 Nelson River 20/1, 2 Nickolson evens F, 3 Stepney Causeway 2/1 (Fransham PU) (second pass, grid)
- Sky: busiest Mars, then Quaoar and Rahu. Top pairs Arcturus/Sedna 99.8, Mars/Rahu 99.5 (no one holds it), Algorab/Rahu 99.2; Mars/Pallas 95.9.
- **1st Nelson River:** Arcturus/Sedna (#1) jockey natal pair; **Algorab/Rahu (#3) jockey Type 1 + natal pair + self**; Haumea/Makemake jockey Type 1; Eris/Haumea jockey natal pair; Makemake/Saturn jockey self; Ceres/Uranus horse natal pair + own link; Rahu/Uranus own link; Mars/Pallas horse self. Almost all inside the jockey's chart.
- **2nd Nickolson (fav):** Arcturus/Sedna (#1) → horse Ceres and Eris; Mars/Pallas → jockey Ketu; Eris/Haumea → horse Saturn; Eris/Venus → jockey Uranus; Mercury/Venus natal pair + own link; Mars/Pleiades jockey natal pair + Type 1; Fomalhaut/Mars own link + Type 1.
- **3rd Stepney Causeway – the loudest:** own links Mars/Pallas (+ natal pair), Eris/Regulus (+ natal pair + self), Capella/Makemake, Ketu/Rigel, Eris/Haumea, Eris/Venus (+ Type 1), Quaoar/Venus (+ natal pairs both charts); jockey Type 1 Rigel/Vesta; Type 1s Mercury/Sun, Rahu/Uranus; Arcturus/Sedna (#1) → horse Chiron; Aldebaran/Pluto → horse Sedna + natal pair; Haumea/Makemake → horse Rahu; Fomalhaut/Mars → horse Ketu, jockey Sun.
- PU Fransham: Makemake/Saturn horse Type 1 + → horse Ceres; Mars/Pallas → jockey Orcus; Mercury/Sun self.
- Seen: Mars/Pallas (busiest) – Stepney Causeway own link (3rd), Nickolson → Ketu (2nd), Fransham → Orcus (PU), winner horse self. The #3 Algorab/Rahu – inside the winner's jockey chart; Stepney Causeway self. Eris/Haumea – winner natal pair; Nickolson → Saturn; Stepney Causeway own link. The winner's holdings are inside its charts; the 3rd's are mostly own links.

### R29 Doncaster 18/03 – 1 Olympe De Gouges 25/1, 2 Oot Ma Way 5/6 F, 3 Poetria 15/8 (second pass, grid)
- Sky: busiest Chiron and Vesta. Top pairs Algol/Gonggong 99.7, Chiron/Transpluto 99.5, Gonggong/Spica 98.5; royal Antares/Jupiter, Antares/Chiron, Antares/Quaoar.
- **1st Olympe De Gouges:** Chiron/Transpluto (#2, busiest) horse Type 1 + self, and → horse Uranus; Antares/Quaoar horse natal pair; **the Sedna pairs inside the jockey's chart** – Pallas/Sedna jockey Type 1, Arcturus/Sedna jockey natal pair + Type 1; also Altair/Venus jockey natal pair + Type 1, Eris/Mars jockey Type 1 + self, Ketu/Pallas jockey natal pair, Mars/Orcus jockey self; Gonggong/Transpluto → jockey Orcus; Pleiades/Vesta → jockey Venus; Chiron/Venus → horse Ketu.
- **2nd Oot Ma Way (fav) – quiet, landing on the horse's Mercury and Pluto:** Chiron/Transpluto (#2) → horse Pluto; Pallas/Sedna and Ketu/Pallas → horse Mercury; Alphecca/Vesta → horse Pluto; Orcus/Saturn → horse Vesta; Ceres/Jupiter natal pairs both charts + → jockey Vesta.
- **3rd Poetria – own links:** Pallas/Sedna own link + natal pair; Neptune/Sedna own link + natal pairs both charts + self; Ketu/Pallas, Chiron/Venus, Alphecca/Vesta own links; Altair/Chiron jockey natal pair; Mars/Orcus natal pair; Arcturus/Sedna → horse Uranus; Haumea/Uranus → jockey Mars.
- Unplaced: Fiamette (4th) – Spica/Transpluto own link + Type 1 + → horse Venus; Mars/Orcus own link + Type 1 + → horse Sun; Haumea/Uranus horse Type 1; Pleiades/Vesta own link; Orcus/Vesta and Alphecca/Vesta → horse Mercury. Suntory Star (5th, 80/1) – Arcturus/Chiron own link; Antares/Jupiter horse Type 1 + self; #1 → horse Vesta.
- Seen: the Sedna pairs split three ways – inside the winner's jockey chart (Type 1 / natal pair), landing on Oot Ma Way's Mercury (2nd), own links on Poetria (3rd); Arcturus/Sedna also onto Poetria's Uranus. The #2 Chiron/Transpluto – winner Type 1 + self (+ Uranus); Oot Ma Way → Pluto.

### R30 Wincanton 21/03 – 1 River Bray 22/1, 2 Guernesey 9/2, 3 Ballyblack 10/11 F (second pass, grid)
- Sky: busiest Regulus, then Makemake. Top pairs Quaoar/Sun 99.4, Algorab/Chiron 99.1, Orcus/Sirius 98.6; Makemake/Pluto 96.3, Makemake/Sun 95.2, Gonggong/Makemake 95.1.
- **1st River Bray – Makemake, the jockey's Venus receiving:** Makemake/Pluto → jockey Rahu and Venus (and more); Makemake/Rahu → jockey Venus + jockey natal pair + self; Capella/Jupiter → horse Makemake + natal pair + self; Neptune/Transpluto horse Type 1 + → horse Sedna; Ceres/Jupiter own link + self; Quaoar/Sun (#1) jockey self.
- **2nd Guernesey:** Orcus/Sirius (#3) → horse Venus; Gonggong/Makemake → horse Ceres; Ceres/Jupiter → horse Juno and **Uranus** (and more); Makemake/Sun horse self.
- **3rd Ballyblack (fav):** Quaoar/Sun (#1) → jockey Venus; Gonggong/Makemake → jockey Mars and Pallas; Aldebaran/Gonggong → horse Eris; Ceres/Jupiter → horse Mercury, Pallas (and more); own links Mars/Transpluto (+ selves) and Ketu/Neptune.
- Unplaced: Birds Of Prey (4th) – Gonggong/Makemake own link + Type 1 + self; Makemake/Pluto and Makemake/Rahu → horse Ceres. Electric Annie (5th) – Quaoar/Sun (#1) own link + → horse Ketu; Aldebaran/Venus and Algol/Pallas own links; Haumea/Uranus → jockey Juno. Reserve Tank (6th) – Algorab/Chiron (#2) → horse Sedna, jockey Saturn; Haumea/Uranus own link + Type 1 + natal pair.
- Seen: **Venus receives on each of the first three** – winner jockey Venus (Makemake/Pluto, Makemake/Rahu), Guernesey horse Venus (#3), Ballyblack jockey Venus (#1). Ceres/Jupiter – winner own link + self; Guernesey → Juno, Uranus (2nd); Ballyblack → Mercury, Pallas (3rd). Gonggong/Makemake – own link on Birds Of Prey (4th); landing on Guernesey's Ceres, Ballyblack's Mars and Pallas. Quaoar/Sun (#1) – own link on Electric Annie (5th); winner self; Ballyblack → Venus.

### R33 Lingfield AW 06/04 – 1 Man On A Mission 12/1, 2 Judy's Park 13/8 F, 3 Bang On The Bell 3/1 (second pass, grid)
- Sky: busiest Pallas, then Haumea. Top pairs Chiron/Procyon 99.6, Altair/Sun 99.4 (no one holds it), Algol/Venus 99.1; Pallas/Pluto 98.6, Pallas/Polaris 98.1, Gonggong/Pallas 97.2, Fomalhaut/Pallas 92.6.
- **1st Man On A Mission:** own link Pallas/Polaris (busiest); Gonggong/Pallas jockey Type 1 + self; Fomalhaut/Pallas → horse Sedna; Antares/Ketu → horse Quaoar; Jupiter/Quaoar own link + → horse Neptune; Jupiter/Ketu → horse Vesta; Haumea/Rahu own link + natal pairs both charts; Alphecca/Uranus horse Type 1 + natal pair + self; Mercury/Spica jockey Type 1; Jupiter/Sedna → jockey Vega; selves Alphecca/Pluto, Arcturus/Sedna.
- **2nd Judy's Park (fav):** Chiron/Procyon (#1) → horse Ketu; Antares/Ketu → jockey Gonggong; Gonggong/Pallas → jockey Orcus and Rahu; Haumea/Pluto → jockey Mercury; Regulus/Venus → jockey Sedna; Jupiter/Quaoar → jockey Sun; Jupiter/Ketu → horse Mercury; Alphecca/Uranus → horse Juno; own links Juno/Mars, Alphecca/Pluto; Mercury/Regulus horse Type 1; Chiron/Gonggong horse natal pair; Algol/Pallas horse self.
- **3rd Bang On The Bell:** Chiron/Procyon (#1) jockey Type 1 + self; Pallas/Pluto → jockey Orcus; Fomalhaut/Pallas → jockey Mercury; Jupiter/Quaoar → jockey Uranus; Jupiter/Ketu → jockey Pluto; Mercury/Spica → horse Venus; Chiron/Gonggong jockey Type 1 + → horse Pallas; own link Alkaid/Eris.
- Unplaced: Brazen Idol (4th) – Fomalhaut/Pallas horse Type 1 + self; Algol/Venus (#3) → jockey Sun; Gonggong/Pallas → horse Ceres, Mercury; Haumea/Pluto → jockey Sun. Jaas Yard (5th) – Pallas/Pluto → horse Rigel, jockey Ceres; Mercury/Spica own link; Juno/Mars → jockey Rahu, Transpluto. Vintage Fashion (6th, 7/2) – Jupiter/Ketu own link + Type 1 both charts; Jupiter/Sedna and Haumea/Mercury own links; Pallas/Pluto → jockey Jupiter, Rahu.
- Seen: **Jupiter/Quaoar** – winner own link + → Neptune; Judy's Park → Sun (2nd); Bang On The Bell → Uranus (3rd); Jaas Yard → Transpluto (5th). **Gonggong/Pallas** – winner jockey Type 1 + self; Judy's Park → Orcus, Rahu; Vintage Fashion → Vesta; Brazen Idol → Ceres, Mercury. **Fomalhaut/Pallas** – winner → Sedna; Bang On The Bell → Mercury; Vintage Fashion → Transpluto; Brazen Idol Type 1 + self. Jupiter/Ketu – own every way on Vintage Fashion (6th); landing on the others.

### R36 Newmarket 14/04 – 1 Eydon 22/1, 2 Masekela 2/1 F, 3 Austrian Theory 25/1 (second pass, grid)
- Sky: busiest Jupiter, then Makemake, Mercury, Pallas, Saturn, Sedna. Top pairs Regulus/Transpluto 100.0 (royal), Orcus/Sun 99.9, Mercury/Pallas 99.3; Jupiter/Rahu 98.5, Saturn/Venus 98.1, Arcturus/Makemake 97.8.
- **1st Eydon – quiet, almost all landing:** Saturn/Venus → jockey Polaris; Arcturus/Makemake → horse Pluto; Alkaid/Sedna → jockey Chiron; Castor/Sedna → jockey Orcus; Algol/Vesta → jockey Venus; Neptune/Pluto → horse Transpluto; Orcus/Venus own link + jockey self. No Jupiter pair, no top-3 pair.
- **2nd Masekela (fav):** Mercury/Pallas (#3) → jockey Sedna; Jupiter/Rahu horse self; Arcturus/Makemake horse self; Pallas/Rigel → jockey Vesta; Arcturus/Saturn → horse Sedna; Castor/Makemake → horse Mercury; Haumea/Rahu → horse Juno; Mercury/Regulus jockey self; Algorab/Mars jockey Type 1; Ceres/Mercury own link + horse natal pair.
- **3rd Austrian Theory:** Orcus/Sun (#2) → horse Pluto + jockey natal pair; Jupiter/Rahu (busiest) → jockey Ceres + self; Arcturus/Makemake → horse and jockey Juno; Arcturus/Saturn → horse Neptune; Algorab/Mars → horse Orcus, jockey Quaoar; Algorab/Ceres → jockey Quaoar; Neptune/Pluto → jockey Sun; Jupiter/Quaoar → jockey Uranus; Haumea/Venus → jockey Mercury; natal pairs Ceres/Saturn (jockey), Fomalhaut/Orcus (horse). No own links.
- Unplaced: Sonny Liston (4th) – Chiron/Juno and Haumea/Venus own links; Arcturus/Makemake → jockey Uranus; Jupiter/Rahu → jockey Quaoar. Cresta (5th, 9/4) – the most own links: Saturn/Venus (+ Type 1), Mercury/Regulus (+ Type 1 + natal pair), Algorab/Mars, Haumea/Rahu; Type 1s Mercury/Saturn, Alkaid/Eris, Algol/Vesta, Castor/Vesta; Makemake/Procyon → horse Uranus, jockey Saturn. Dawn Of Liberation (6th) – Regulus/Transpluto (#1) jockey self; own links Castor/Sedna, Spica/Transpluto, Algorab/Ceres (+ Type 1s); Fomalhaut/Rahu → jockey Uranus.
- Seen: the busiest Jupiter – Austrian Theory (3rd) → Ceres + self; Masekela (2nd) self; Dawn Of Liberation → Gonggong; Sonny Liston → Quaoar; the winner none. **Arcturus/Makemake** – winner → Pluto; Austrian Theory → Juno (both charts); Masekela self; Cresta → Saturn; Sonny Liston → Uranus. **Saturn/Venus** – Cresta own link + Type 1 (5th); winner → Polaris. **Castor/Sedna** – winner → Orcus; Dawn Of Liberation own link + Type 1 (6th). The two with the most own links finished 5th and 6th.

### R38 Musselburgh 09/05 – 1 John Kirkup 14/1, 2 Rory 10/1, 3 Rose Bandit 15/2 (fav The Thin Blue Line 5th) (second pass, grid)
- Sky: busiest Uranus, then Haumea, Orcus, Quaoar. Top pairs Sedna/Venus 99.6, Castor/Ceres 99.4, Alkaid/Haumea 99.1 (no one holds it); Quaoar/Venus 98.4, Makemake/Uranus 98.0, Regulus/Venus 97.8, Juno/Regulus 93.3.
- **1st John Kirkup:** Quaoar/Venus → jockey Jupiter + horse self; Juno/Regulus → horse Sedna; Chiron/Sun → horse Ketu; own links Algorab/Haumea and Betelgeuse/Orcus; Gonggong/Quaoar horse natal pair.
- **2nd Rory:** Castor/Ceres (#2) → jockey Vesta; Regulus/Venus → jockey Sedna; Haumea/Rahu horse Type 1 + self; Chiron/Sun → horse Uranus; Betelgeuse/Orcus → horse Vesta; Orcus/Procyon own link + → horse Venus; Sedna/Venus (#1) jockey self; Chiron/Mercury self.
- **3rd Rose Bandit:** Juno/Regulus jockey Type 1 + natal pair + self; Regulus/Venus jockey natal pair; Fomalhaut/Sun jockey natal pair; Chiron/Sun own link + Type 1 + natal pair + self; Aldebaran/Saturn own link + → horse Juno; Orcus/Polaris → jockey Sun; Eris/Uranus (busiest) → horse Quaoar, jockey Ketu; Jupiter/Mercury natal pair; Sedna/Venus jockey self.
- Unplaced: Albegone (4th) – Makemake/Uranus (busiest) horse Type 1; Orcus/Polaris and Pallas/Vega own links + natal pairs both charts; Regulus/Venus → horse Vesta. The Thin Blue Line (fav, 5th) – Makemake/Uranus → jockey Rahu; Eris/Uranus → jockey Chiron; Makemake/Regulus horse Type 1 + self; Ketu/Orcus horse Type 1 + natal pair + self; Rigel/Venus → jockey Sun; Chiron/Mercury jockey Type 1. Primo's Comet (6th) – Quaoar/Venus own link + self; Haumea/Mars own link.
- Seen: **Juno/Regulus** – onto the winner's Sedna; inside Rose Bandit's jockey chart (3rd). **Regulus/Venus** – onto Rory's Sedna (2nd); Rose Bandit natal pair (3rd); Albegone → Vesta (4th). **Chiron/Sun** – winner → Ketu; Rory → Uranus (2nd); Rose Bandit own every way (3rd). **Quaoar/Venus** – winner → Jupiter + self; Primo's Comet own link (6th). Royal pairs land on natal Sedna for both the 1st and the 2nd. The busiest Uranus pairs sit with the 3rd, 4th and 5th.

### R39 Sedgefield 10/05 – 1 Blue Collar Glory 20/1, 2 Bright Sunbird 13/2, 3 Emorelle 13/2 (fav Wheres Maud Gone 5th) (second pass, grid)
- Sky: busiest Jupiter, then Eris and Uranus. Top pairs Mars/Procyon 99.9, Chiron/Jupiter 99.4, Capella/Eris 99.3 (no one holds it); Antares/Uranus 98.7, Jupiter/Uranus 95.2, Fomalhaut/Neptune 95.1.
- **1st Blue Collar Glory:** Chiron/Jupiter (#2, busiest) own link + → jockey Vesta; Mars/Procyon (#1) → horse Quaoar; Juno/Makemake own link + → jockey Chiron and Pluto; Mars/Sedna jockey natal pair.
- **2nd Bright Sunbird:** Jupiter/Uranus (busiest) jockey Type 1; **Fomalhaut/Neptune own link + Type 1 + self**; Chiron/Fomalhaut horse Type 1 + self; Eris/Pallas → horse Makemake; Jupiter/Saturn → horse Orcus.
- **3rd Emorelle – own links:** Jupiter/Uranus, Eris/Pallas (+ → horse Jupiter), Altair/Venus, Rigel/Uranus, Mercury/Vega, Mercury/Transpluto (+ natal pairs both charts); selves Chiron/Jupiter (#2), Antares/Uranus, Mars/Sedna; Altair/Eris natal pair; Spica/Vesta → horse Sun.
- Unplaced: Mrs Paisley (4th) – Spica/Vesta own link + Type 1; Algorab/Eris own link + natal pair; Fomalhaut/Neptune → jockey Makemake; Eris/Sedna → horse Gonggong. Wheres Maud Gone (fav, 5th) – Mars/Procyon (#1) selves both charts; Chiron/Jupiter (#2) natal pair; Bellatrix/Mars own link; Mars/Sedna horse Type 1; Juno/Makemake → horse Spica + natal pair; Chiron/Fomalhaut → horse Quaoar, jockey Orcus; Rigel/Uranus → Vesta; Mercury/Vega → Rahu.
- Seen: **Chiron/Jupiter (#2)** – winner own link + landing on Vesta; Emorelle self (3rd); Wheres Maud Gone natal pair (5th). **Juno/Makemake** – winner own link + → Chiron, Pluto; Wheres Maud Gone → Spica + natal pair. **Jupiter/Uranus** – Bright Sunbird Type 1 (2nd), Emorelle own link (3rd). **Fomalhaut/Neptune** – Bright Sunbird own every way (2nd); Mrs Paisley → Makemake (4th). The #1 pair – onto the winner's Quaoar; selves on the favourite.

### R42 Bath 03/06 – 1 Little Girl Blue 10/1, 2 Soi Dao 13/8 F, 3 Between The Sheets 2/1 (4 runners) (second pass, grid)
- Sky: busiest Quaoar, then Neptune. Top pairs Antares/Vesta 99.5 (royal), Aldebaran/Sedna 99.1 (royal), Ketu/Neptune 99.0; Fomalhaut/Neptune 98.7, Fomalhaut/Mars 94.4.
- **1st Little Girl Blue:** Aldebaran/Sedna (#2) → horse Juno; Alphecca/Quaoar (busiest) own link + jockey self; Alphecca/Pallas horse Type 1 + natal pair + self; Haumea/Jupiter jockey Type 1 + natal pair; Altair/Quaoar jockey Type 1 + natal pair; own links Vega/Venus, Rigel/Saturn; Gonggong/Neptune → horse Sun.
- **2nd Soi Dao (fav):** Antares/Vesta (#1) → jockey Jupiter; Ketu/Neptune (#3) own link + natal pairs both charts; Fomalhaut/Neptune → jockey Juno; Fomalhaut/Mars → jockey Makemake; own links Rigel/Transpluto (+ Type 1), Algorab/Jupiter (+ natal pair + self); Ceres/Transpluto → jockey Vega + natal pair + self; Gonggong/Neptune jockey Type 1 + self + → Polaris; selves Neptune/Pallas, Haumea/Jupiter.
- **3rd Between The Sheets:** Antares/Vesta (#1) → horse Makemake; Aldebaran/Sedna (#2) → jockey Chiron + jockey natal pair; Fomalhaut/Mars → horse Orcus; Alphecca/Neptune and Algorab/Jupiter → jockey Mercury; Juno/Makemake own link + self.
- 4th Hattie C: Antares/Vesta natal pair; Neptune/Quaoar own link + Type 1; Neptune/Pallas → horse Ketu, Venus; Juno receives Ceres/Transpluto (jockey), Gonggong/Neptune (jockey), Algorab/Jupiter (horse).
- Seen: the #1 royal pair Antares/Vesta – Soi Dao → Jupiter (2nd), Between The Sheets → Makemake (3rd), Hattie C natal pair (4th); the winner doesn't hold it. The #2 royal Aldebaran/Sedna – winner → Juno; Between The Sheets → Chiron + natal pair. Juno receives on three runners: the winner (royal #2), Soi Dao (Fomalhaut/Neptune), Hattie C (three non-royal pairs). The busiest Quaoar – winner own link + self; Hattie C own link + Type 1.

### R44 Ripon 16/06 – 1 Society Red 16/1, 2 Commonsensical 4/1, 3 Urban War 100/30 (fav Bollin Joan 4th, 4 runners) (second pass, grid)
- Sky: busiest Haumea, then Chiron, Jupiter, Ketu, Polaris, Quaoar. Top pairs Rigel/Saturn 99.7, Aldebaran/Uranus 99.5 (no one holds it), Makemake/Sedna 99.5; Antares/Ceres 97.8.
- **1st Society Red:** Haumea/Rahu (busiest) own link + horse Type 1 + natal pair + self; Ceres/Haumea own link + → jockey Sun; Haumea/Vesta own link; Mercury/Quaoar own link + natal pairs both charts; Alkaid/Chiron own link + natal pairs both charts; Chiron/Jupiter jockey natal pair; **horse/jockey Rahu receives three** – Makemake/Sedna (#3) → jockey Rahu, Chiron/Ketu → horse Rahu (+ natal pair), Jupiter/Sun → horse Rahu; Chiron/Haumea → jockey Gonggong.
- **2nd Commonsensical:** Antares/Ceres → horse Pallas, jockey Haumea (and more); Jupiter/Mercury jockey Type 1; Spica/Transpluto own link + natal pair + Type 1; Chiron/Haumea natal pair + Type 1; Quaoar/Rahu own link; Orcus/Polaris → horse Venus; Eris/Mars → jockey Venus; Jupiter/Venus → jockey Pluto + natal pair; Chiron/Jupiter → horse Vesta + self; selves Haumea/Rahu, Haumea/Vesta.
- **3rd Urban War – the horse's Juno receives three:** Mercury/Quaoar → horse Juno and Venus; Haumea/Rahu → horse Juno; Quaoar/Rahu → horse Juno + natal pair; Makemake/Sedna (#3) → horse Pallas; Ceres/Haumea → horse Neptune; own links Rigel/Sedna, Arcturus/Mars (natal pairs both charts), Jupiter/Sun (+ selves), Jupiter/Venus (+ Type 1); Rigel/Saturn (#1) jockey natal pair; Juno/Venus → jockey Gonggong, Mercury.
- 4th Bollin Joan (fav): Antares/Ceres → horse Orcus; Mercury/Quaoar → horse Vesta; Ceres/Haumea → jockey Uranus; Eris/Mars → horse Saturn, jockey Jupiter; Quaoar/Rahu → horse Sedna; natal pairs Orcus/Polaris, Pallas/Polaris, Haumea/Vesta; Type 1s Mars/Orcus, Juno/Venus.
- Seen: **Haumea/Rahu (busiest)** – winner own every way; Commonsensical self; Urban War → Juno. **Ceres/Haumea** – winner own link + → Sun; Urban War → Neptune; Bollin Joan → Uranus. **Mercury/Quaoar** – winner own link + natal pairs; Urban War → Juno, Venus; Bollin Joan → Vesta. Gathering: winner Rahu ×3; Urban War Juno ×3.

### R45 Carlisle 07/07 – 1 Whitefeathersfall 10/1, 2 Persist 7/4, 3 Million Thanks 13/8 F (second pass, grid)
- Sky: busiest Haumea, Pluto, Sedna. Top pairs Deneb Algedi/Pallas 99.8, Ketu/Mercury 99.8, Quaoar/Vega 98.9; Pluto/Sun 98.2, Mars/Regulus 97.8, Juno/Regulus 96.1. Most of the winner's holdings are under 90 or shared, so it is quiet in the grid.
- **1st Whitefeathersfall – no own links; the Haumea pairs landing:** **horse Pallas receives three** (Haumea/Saturn, Haumea/Neptune, Betelgeuse/Uranus); **jockey Vesta receives two** (Haumea/Saturn, Haumea/Polaris); Haumea/Polaris → horse Ketu; Betelgeuse/Sedna → Saturn on both charts; Alkaid/Ceres → jockey Saturn; Ceres/Chiron → horse Pluto + horse natal pair; Ceres/Fomalhaut → horse Juno; Bellatrix/Eris → horse Neptune; Alphecca/Neptune → horse Rahu; Castor/Ketu → horse Makemake + natal pair. Horse natal pairs Quaoar/Vega (#3), Mars/Pluto, Makemake/Venus, Eris/Pleiades; Transpluto/Venus horse self.
- **2nd Persist:** Chiron/Sun own link A both charts; Pluto/Sun (busiest) horse self + → horse Saturn; Ceres/Chiron → jockey Mercury, Spica; Alphecca/Neptune → jockey Pluto; jockey natal pairs Procyon/Sedna, Haumea/Polaris; Transpluto/Venus jockey self.
- **3rd Million Thanks (fav):** Chiron/Sun jockey Type 1; Mars/Regulus and Polaris/Sun → jockey Uranus; Haumea/Saturn → horse Ceres, jockey Jupiter; Betelgeuse/Sedna → jockey Jupiter + jockey natal pair; Betelgeuse/Uranus → horse Juno; Orcus/Transpluto → jockey Juno; Transpluto/Venus → horse Chiron, jockey Pallas; Bellatrix/Eris → jockey Sun + natal pair; Alkaid/Ceres → horse Pluto, Transpluto; natal pairs Gonggong/Regulus, Alkaid/Pallas, Algol/Makemake.
- Unplaced: Aswan (4th) – Mars/Regulus jockey Type 1 + self, Regulus/Saturn horse Type 1, Altair/Saturn own link + natal pairs, Orcus/Transpluto own link, Pluto/Sun → jockey Orcus + natal pair, Juno/Regulus → horse Transpluto. Noble Mark (5th) – Pluto/Sun own link + → jockey Ceres, Transpluto/Venus own link, Ketu/Mercury (#2) → horse Quaoar. Lucia Joy (6th, 28/1) – Algol/Venus, Makemake/Venus, Orcus/Transpluto Type 1s; Juno/Regulus → horse Sedna.
- Seen: **Haumea/Saturn** – winner → Pallas, Vesta; Million Thanks → Ceres, Jupiter. **Betelgeuse/Sedna** – winner → Saturn (both charts); Million Thanks → Jupiter + natal pair. **Betelgeuse/Uranus** – winner → Pallas; Million Thanks → Juno. **Chiron/Sun** – Persist own link (2nd), Million Thanks Type 1 (3rd), Noble Mark → Orcus (5th). **Pluto/Sun (busiest)** – Persist self + → Saturn (2nd); Noble Mark own link (5th); Aswan → Orcus + natal pair (4th).

### R48 Doncaster 16/07 – 1 Novakai 12/1, 2 Crackovia 8/15 F, 3 Mother India 8/1 (second pass, grid)
- Sky: busiest Haumea, then Spica. Top pairs Saturn/Uranus 99.9, Betelgeuse/Eris 99.0 (no one holds it), Sedna/Sun 98.7; Eris/Haumea 93.9, Jupiter/Spica 93.5, Antares/Saturn 91.0, Mercury/Venus 98.7.
- **1st Novakai:** Jupiter/Spica own link + jockey Type 1 + self; Saturn/Uranus (#1) jockey natal pair; Sedna/Sun (#3) → horse Eris; Antares/Saturn → jockey Pallas; Mercury/Venus → horse Juno.
- **2nd Crackovia (fav):** Eris/Haumea (busiest) → horse Juno + self; Deneb Algedi/Haumea own link; Makemake/Sedna jockey Type 1 + self; Chiron/Regulus jockey natal pair; Antares/Saturn → jockey Quaoar and Uranus; Mercury/Venus → jockey Gonggong + natal pair; Transpluto/Vesta → jockey Juno; Juno/Orcus → horse Uranus, jockey Transpluto; Eris/Sun → horse Ketu.
- **3rd Mother India:** Sedna/Sun (#3) → horse Saturn; Mercury/Venus jockey Type 1 + self + → jockey Haumea; own links Eris/Sun (+ self), Transpluto/Vesta (+ → horse Gonggong), Haumea/Venus; Algol/Ceres → jockey Uranus; Spica/Uranus jockey natal pair.
- Unplaced: Gilded Moon (4th) – Spica/Transpluto, Fomalhaut/Quaoar, Quaoar/Spica own links; Mercury/Venus → horse Sun; Juno/Orcus → jockey Pallas, Sun. Passing Storm (5th) – Sedna/Sun (#3) jockey Type 1 + self; Castor/Uranus own link + Type 1; Chiron/Spica horse Type 1; Algol/Ceres horse Type 1. Bella Kopella (6th, 40/1) – Saturn/Uranus (#1) → horse Ceres; Sedna/Sun → horse Haumea; Antares/Vesta → horse Juno, jockey Ketu; Haumea/Makemake jockey Type 1.
- Seen: **Mercury/Venus** – winner → Juno; Crackovia → Gonggong + natal pair; Mother India Type 1 + → Haumea; Gilded Moon → Sun. **Sedna/Sun (#3)** – winner → Eris; Mother India → Saturn; Bella Kopella → Haumea; Passing Storm Type 1 + self. **Antares/Saturn** – winner → Pallas; Crackovia → Quaoar, Uranus. **Juno receives** on the winner (Mercury/Venus) and on Crackovia's horse and jockey (Eris/Haumea, Transpluto/Vesta).

## Second pass of the 24 outsider races – done (2 Oct 2026)
Every outsider race read for the first three with the pair × runner grid. What was seen, without scoring it against any line:
- In most races the same key pair is held by several runners in different ways, and the first three each hold it differently from one another (examples: R6 Chiron/Juno, R18 Jupiter/Regulus, R27 Mars/Pallas, R30 Ceres/Jupiter, R33 Jupiter/Quaoar, R38 Chiron/Sun, R44 Haumea/Rahu, R48 Mercury/Venus).
- Winners often gather several pairs on one natal body (R1 jockey Pluto ×3; R4 horse Sun ×3; R26 horse Rahu ×3; R44 Rahu ×3; R45 horse Pallas ×3 and jockey Vesta ×2); so do some placed runners (R26 Aced It Juno ×3; R44 Urban War Juno ×3).
- Some winners hold almost nothing in the top rows and win on pairs under 90, all landing (R26 Sir Chauvelin, R45 Whitefeathersfall, R36 Eydon).
- Next step proposed: grids for races not yet seen, read for the first three before the result is looked at.

## pair_body.py v1.3 and profile.py v1.0 (2 Oct 2026, Eddie: "we really need the ability to show all the winners who follow some kind of profile")
- **pair_body.py v1.3 – gathering block** in the grid: each runner's natal bodies receiving 2+ pairs, busiest-body pairs marked *. Checked: the runner with the race's strongest gathering wins at base whichever way it's measured (most pairs on one body 13% / 18% by halves; most busiest pairs on one body 17% / 15%; most gathering bodies 12% / 15%). Useful for reading, not a profile on its own.
- **profile.py v1.0** – one row per runner (291), features built without the result: gmax, gbusy, gbodies; top-3 pairs held as own / natal pair / landing; busiest pairs the same; ownA, t1, np, lands, selfs; royal_A (royal star as own link A), royal_land, c3; ura, ura_set; field, sp_odds. Result joined last. `--where "<combination>"` lists every runner that fits with counts by halves; `--winners` shows all 48 winners side by side; `--show <race>`.
- First runs: **royal_A ≥ 1 – 32 runners, 0 won** (1–24: 15, 0; 25–48: 17, 0), 13 placed. **ura_set ≥ 1 – 51 runners, 4 won (10% / 5%), 2nd/3rd 52% / 55%.** gbusy ≥ 2 with no royal_A and no ura_set – 80 runners, 20 won (23% / 27%), 2nd/3rd 21% / 20%. All 48 winners have royal_A = 0. (These lines were shaped by looking at the same 48 races – they need fresh races.)
