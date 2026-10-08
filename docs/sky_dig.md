# SKY DIG – what in the sky lets a favourite, a mid price or an outsider win (sky only)

> **NOTE (8 Oct 2026):** the exact-time search used up to §77 reported the closest approach of a chord as "exact" without checking the leftover deviation. Chords whose three ratios cannot all come exact (mixed or composite types) were sometimes printed with an "exact" time. From 8 Oct the tools only call a chord exact when the leftover is ≤0.005%, otherwise "closest X% at T". Exact times in the sections before the runner records may be closest approaches; each race's times are put right when it is redone in the runner-record form. Doncaster corrections are marked in §62 and §77.

Started 4 Oct 2026. Sky only: no runners. Same "say what you see" method as the race reads.
Bodies, families and distances, including the Sun with the Moon, and the fast points (Ascendant, Midheaven, Vertex,
Part of Fortune, Part of Spirit). The fast points are checked by conjunction and opposition in RA (0 / 180) and by
parallel and contra-parallel in Dec.

Tools (ledger/):
- skysheet.py RACE: sky sheet with five sections: structure, Moon & Sun, the moment, signatures, fast points
- dig_sky/fpdig.py RACE FASTPOINT PARTNER [NUMBER MODE]: one fast point dug in detail
- dig_sky/n1444.py and dig_sky/fpbusy.py: field checks

Outputs: sky_out/all/<label>_SKY.txt for all 96 races.

**All 96 races were read at the SCHEDULED time.** The actual off times are now being scraped (sky_results_scraper.py).
Every thread below must be re-checked at the real off. The three races checked so far all went off late:
- R11 14:05:45 (+0.75 min)
- R12 15:16:04 (+1.1)
- R2 20:11:22 (+1.4)

Moving R2 to its real off already pushes its Part of Fortune + Sun completion (−0.3 from the scheduled time) to −1.7,
just outside ±1.5.

## 1. Matched pairs (same day): what fell away
R11/R12 (Exeter, the same afternoon) looked different in:
- whether the busiest body leads
- the Sun's place in the top 30
- the Moon peaking at the off with #1's number

Across 7 more same-day pairs and then all 96, none of these held:
- **Busiest body in the top 7:** 33/48 fav won vs 28/48 fav beaten. In the top 3: 20 vs 20.
- **Fast point conjunct or opposite any body within ±1 min:** 12 vs 9.
- **13/9-scale numbers (1.444 / 14.44 / 144.4) in the top 12:** 22 vs 22. Common.
- **Fast point completing a busiest body's number at the off:** about 18 vs 18. Common.

## 2. Four threads, FROZEN for blind testing (scheduled times, 96 races)
A "completion" means the RA or Dec distance between the fast point and the Sun or Moon equals a top-12 race number.

| # | Thread | Window | Fav won | Fav beaten | R half (won–beaten) | T half (won–beaten) |
|---|---|---|---|---|---|---|
| T1 | Part of Fortune + Sun completes a top-12 number | ±1.5 min | 5/48 | 0/48 | 2–0 | 3–0 |
| T2 | Vertex + Sun or Moon completes a top-12 number | ±3 min | 0/48 | 9/48 | 0–5 | 0–4 |
| T3 | Vertex + Moon completes a top-12 number | −5..+15 | 5/48 | 18/48 | 2–7 | 3–11 |
| T4 | Midheaven + Sun completes a top-12 number | −5..+15 | 15/48 | 6/48 | 7–4 | 8–2 |

Notes:
- T1 is only tight to the off: at ±3 min it is 5 vs 3, and over the whole window it is 10 vs 10.
- About 40 combinations were looked at (5 points × Sun/Moon × 4 windows). These four held on both halves.
- **At Selangor (3°N) the Vertex barely moves (0.01°/min), so T2 and T3 may not apply there.**

## 3. New thread (5th): the Vertex itself exact on a body near the off
The Vertex is exactly conjunct, opposite, parallel or contra-parallel to a body (not a star) within ±1.2 min of the off.

| | Fav won | Fav beaten |
|---|---|---|
| All 96 | 6/48 | 17/48 |
| R half | 2 | 11 |
| T half | 4 | 6 |

It leans the same way on both halves, but strongly only on R. The other fast points show no lean (Ascendant 9 v 13,
Midheaven 9 v 10, Part of Fortune 4 v 10, Part of Spirit 5 v 7).

The sharpest form: **T43 and R42 have the Vertex on the Sun in RA and Dec at once**, about 1 minute from the off.
Both are fav beaten.

When the Vertex sits on a body, it carries that body's numbers. That is why "Vertex + Sun/Moon completes a number"
often happens (R27, R4).

## 4. Part of Fortune + Sun races (fav won), dug in detail
- **T45 York, Asaassi 6/5**
  - 144.45 is held by #3 Jupiter/Regulus and #5 Pallas/Vega, and by #1 Betelgeuse/Venus ×10 (14.4441).
  - Part of Fortune–Sun RA is 144.487 at the off and crosses 144.45 at +0.2. The race's repeated number lands on the Sun.
  - Part of Fortune → busiest Pallas, Dec 48.2852 = 20(1+√2) at +5 = #7's number.
  - 61.80 lands on Regulus twice: Part of Fortune Dec at +2 and the Moon RA at +4.
- **R2 Wolverhampton, Cuban Cigar 5/2**
  - #2 is busiest Makemake/Orcus at 41.000; no other pair holds it.
  - Part of Fortune–Sun crosses 41 at −0.3 (−1.7 from the real off).
  - Part of Fortune–Moon crosses #9 Gonggong/Sun (177.75) at +0.5.
  - Whole-number triangle #2/#6/#11 (Makemake/Orcus/Uranus): Part of Fortune lands Whole on all three at +10.
- **R10 Kempton, Mercian Prince 13/8**
  - #2 Altair/Rahu (122.2262); no other pair holds it. Part of Fortune–Sun crosses it at +0.8.
  - Part of Fortune → Bellatrix RA 1.4447 (13/9) exactly at the off. That is busiest Haumea's #6 number, crossing over.
- **T5 Kempton AW, Geremia 6/4**
  - #6 Gonggong/Procyon (Dec 150/9). Part of Fortune–Sun Dec crosses it at +1.4.
  - 150/9 is held three times in the top 19.
  - Part of Fortune comes almost exactly opposite the Sun at about +3.
  - Part of Fortune → Makemake RA 1300/9, 100.0 at +1.
- **T37 Bath, Symbol Of Hope 5/4**
  - #4 Deneb Algedi/Makemake (128.6932); no other pair holds it. Part of Fortune–Sun crosses it at −0.1.
  - **Part of Fortune is exact on busiest Neptune at the off** (Dec 13φ, 99.3). Field: 2/48 fav won, 0/48 fav beaten.

Across the five: the number Part of Fortune puts on the Sun is always a top-6 number. In three races it is held by no
other pair; in T45 it is the race's repeated number.

## 5. Vertex races (fav beaten), dug in detail
- **R27 Leicester (20/1; Evens fav 2nd)**
  - #1 Arcturus/Sedna and #10 Neptune/Quaoar share Dec 11.09 (φ⁵); busiest Quaoar is in #10.
  - Vertex–Sun puts it on the Sun at +2.5.
  - The Vertex is parallel to busiest Mars at −0.2 (0.004° away), so it carries #2 Mars/Rahu (−0.2) and the 14.14 of
    #9 and #15 (−0.4).
- **R4 Goodwood (12/1)**
  - The Vertex is parallel to Sedna at +1.1, so Vertex + Sun = #4 Sedna/Sun.
- **T36 Perth (10/1; 8/13 fav 3rd)**
  - The Vertex is opposite Orcus in RA at +0.2.
  - Vertex + Sun = #3 Uranus/Venus (Silver 9(1+√2)) at −0.7.
- **R18 Exeter (10/1)**
  - #11 Juno/Quaoar and #4 Ceres/Mercury are the same number ×100 (busiest Juno).
  - Vertex + Moon carries it at +2.9.
  - The Vertex is contra-parallel to Sedna at +0.8.
- **R33 Lingfield (12/1)**
  - Vertex + Sun = #5 (800/9) at +0.2.
  - Vertex + Deneb Algedi = #10 exactly at the off.
- **T40 Haydock (10/1)**
  - Vertex + Moon = #3 Alphecca/Juno (101, busiest Juno) at −1.0.
- **T41 Nottingham (18/1)**
  - Vertex + Moon = #2 at +2.7.
  - Vertex + Sun = #11, the Sun's own pair, at +2.6.
- **R21 Newcastle (25/1; 2/5 fav 3rd)**
  - Vertex + Moon = #10 at +2.4.
  - The Vertex is contra-parallel to Transpluto (a #9 body) at −1.9.
- **T1 Newcastle (25/1)**
  - Edge case only: Vertex + Sun = #3 at +3.0. The Vertex makes no conjunctions or oppositions at all.

## 6. The mirror (the link Eddie asked for)
A fast point brings the race's own REPEATED number onto the Sun or the Moon:

| Race | Fast point | Result |
|---|---|---|
| T45 | Part of Fortune | Fav won |
| R27 | Vertex | Fav beaten |
| R18 | Vertex | Fav beaten |

Same shape, different point, opposite result. Only three races so far, so this is being watched.

## 7. Next
- Scraper Step 4: all UK races on the 86 dates of the 96, with actual off times.
- Sky-only script for Eddie's Mac, so the outer bodies are included.
- Re-run the 96 at their real off times, then test the five threads on the whole days.

## 8. Re-check at the REAL off times (Eddie looked them up by hand, 4 Oct) – 14 thread races
**Part of Fortune + Sun (fav won)** – crossing time measured from the real off:

| Race | Real off | Crossing vs off | Race length | Where |
|---|---|---|---|---|
| T45 | 15:51:26 | 1.2 min before | 2m13 | before the off |
| R2 | 20:11:22 | 1.6 min before | 2m01 | before the off |
| R10 | 14:40:29 | 0.3 min after | 4m29 | during the race |
| T5 | 20:45:21 | 1.1 min after | 3m33 | during the race |
| T37 | 13:22:24 | 1.5 min before | 1m01 | before the off |

All five are still within about ±1.6 min of the real off: two during the race, three in the loading minutes just before.

**Vertex (fav beaten)** – window from 3 min before the off to 1 min after the finish:
- **R27** (off +0.7, 4m05 race): Vertex parallel to busiest Mars 0.9 min before the off. Vertex + Sun = #1 and #10 (the repeated φ⁵ number) DURING the race (+2.5/+2.6).
- **R4** (off +1.1, 1m37): Vertex parallel to Sedna and Vertex + Sun = #4 **exactly at the off**.
- **T36** (off +0.7, 6m11): Vertex opposite Orcus 0.5 min before. Vertex conjunct Mars and conjunct Gonggong DURING. Vertex + Sun = #3 1.3 min before.
- **R18** (off +0.5, 4m23): Vertex contra-parallel to Sedna, conjunct Makemake, and Vertex + Moon = #4 (the ×100 repeated number), all DURING.
- **R21** (off +2.8, 59 s): Vertex + Moon = #10 0.4 min before. Vertex opposite Eris DURING.
- **T40** (off +0.8, 1m46): Vertex parallel to Transpluto DURING. Vertex + Moon = #3 1.8 min before.
- **T1** (off +0.8, 2m11): Vertex + Sun = #3 0.1 min after the finish (edge).
- **T41** (off +0.5, 1m01): the Vertex completions come about 1 min after the finish. Outside.
- **R33** (off **+3.8**, 1m12): its completion was 3.6 min before the real off. Outside.

So 6 of 9 have the Vertex active (exact on a body, or completing a top number) between just before the off and the finish; 1 is on the edge; 2 fall outside.

**Caution:** jump races last 4–6 minutes, so they give the Vertex more time to hit something. Before anything is concluded, the fav-won races need the same check at their real offs.

## 9. Wolverhampton AW 29 Sep 2026 – two odds-on favourites beaten 30 min apart (Eddie)
Sky only, built from Eddie's chart workbooks (exact, London time). Real offs and race lengths are from the Racing Post pages.
- **18:30:** Nightbloom 11/1 beat Oxbridge 2/5F (3rd). Off 18:31:26 (+1.4); race 1m13, finished about +2.65.
  - **Vertex + Sun = #9 Haumea/Venus (6.8535) at +0.2, 1.2 min before the off. T2 fires (fav beaten).** ✓
  - Vertex contra-parallel to Neptune at +2.6 (at the finish).
  - Part of Fortune conjunct Venus (a #1 body, Pluto/Venus) in RA at −0.2, 1.6 min before the off.
  - Ascendant + Moon (the same event as Part of Spirit + Sun) completes #4 busiest Gonggong/Pallas at +0.6 and #3 at +1.8.
  - No Part of Fortune + Sun and no Midheaven + Sun (the fav threads T1/T4 do not fire).
- **19:00:** Go Lockers Go 16/1 beat Methgal 4/9F (2nd). Off 19:00:42 (+0.7); finished about +1.9.
  - **The Vertex is contra-parallel to Saturn at +0.5 (0.2 min before the off; Saturn is a #3 and #8 body) and parallel to Vesta at +1.4 (during the race; Vesta is a #7 body). The 5th thread (Vertex exact on a body at the off) fires.** ✓
  - **The Vertex is on the Sun in RA AND Dec at +6.7**, the same shape as T43 and R42 (fav beaten), though here about 5 min after the finish.
  - Ascendant + Moon / Part of Spirit + Sun completes #5 Regulus/Sun at −0.2 and #3 Pallas/Saturn at +1.1.
  - The Moon is on Vega (next-busiest) at φ¹⁰, 99.5 at +2.
  - T1/T4 do not fire.
- **Both:**
  - the Vertex is active from just before the off to the finish
  - neither favourite thread (Part of Fortune + Sun, Midheaven + Sun) fires
  - Ascendant + Moon completes top numbers during both races.
- **Correction to the Selangor "fav shape"**, which counted ANY fast point + Sun/Moon on a top number: it does not hold here (Ascendant + Moon fired in two beaten-favourite races). The UK threads are specific: **Part of Fortune + Sun and Midheaven + Sun lean to the fav; the Vertex leans to the fav beaten.**
- **What spans both Wolverhampton races (slow layer):**
  - **Saturn** is in the top 30 of both (Gonggong/Saturn, Algol/Saturn, Saturn/Transpluto, plus Mercury/Saturn at 18:30 and Pallas/Saturn #3 at 19:00); **Pallas** is busiest in both.
  - Timeline:
    - 18:36: Mercury/Saturn Dec = 130/9 exact
    - 18:54: Sun/Regulus Dec = 130/9 exact (the same number handed on)
    - 18:58: Pallas/Saturn = 10√2 and Haumea/Rahu = 46(1+√2) (#1 at 19:00), with the Moon on Haumea and Gonggong
    - 19:00:30: the Vertex contra-parallel to Saturn
  - **Star frames (exact crossings; error checked minute by minute):**
    - **Pallas exactly midway between Deneb Algedi and Rigel in Dec at 18:32:33**: race 1 finished about 18:32:39. The error is +0.32% at 18:00, +0.015% at 18:31, −0.28% at 19:01.
    - **Saturn in Spica–Saturn–Bellatrix, Dec ratio 3, exact at 19:01:06**, 24 s after the race 2 off. The error is +0.04% at 18:00, +0.0001% at 19:01, −0.02% at 19:30.
    - The Moon at 18:29 (2.4 min before the race 1 off): at the midpoint of Saturn and Vega in Dec, and in the frame Antares–Moon–Alkaid at φ.
  - Midpoints of slow bodies: Saturn = mid(Moon, Algorab) Dec at 18:49:56; the Moon = mid(Pallas, Sedna) RA at 18:50:28. Fast-point midpoints are too many to mean anything (the Ascendant sweeps through dozens).
  - **Caution:** many frame and midpoint combinations were tested, so some will be exact in any window. The test is whether slow-body frames at the off cluster in fav-beaten races (needs real offs on many races).

## 10. 4 Sep 2021: R6 Haydock 14:20 (Golden Flame 9/1; Valley Forge 11/8F 3rd) and T6 Kempton AW 14:40 (Hamish 9/1; Hukum 30/100F 2nd)
Two beaten favourites 20 minutes apart (Eddie: "another type"). Read at the scheduled times; the real offs are still to come.
- **The spanning body is MARS:** it is busiest in both (R6 Mars and Mercury joint; T6 Mars). Makemake/Mars is R6 #1 and T6 #6.
- 20 pairs sit in the top 30 of both races, e.g. Pluto/Quaoar (R6 #4, T6 #1), Orcus/Polaris, Aldebaran/Orcus, Saturn/Transpluto, Neptune/Transpluto, Algorab/Chiron.
- Timeline:
  - 14:22:50: **R6's #1 Makemake/Mars, Dec 170/9, goes exact**, about 3 min after R6's scheduled time.
  - 14:22:39: the Moon = mid(Ceres, Spica) in RA.
  - 14:29:16: Mercury = mid(Altair, Sirius) in Dec.
  - **14:30:40: Mercury (joint busiest in R6) exactly at the midpoint of Gonggong and Mars (busiest) in Dec**, between the races (both course files agree to within 5 s).
  - 14:40:12: **the Moon in Betelgeuse–Moon–Regulus at φ² (RA), exact at T6's scheduled time.** This was T6's original standout (the Moon star frame at the off).
  - 14:44:12: Antares–Moon–Algol 1+√2 (Dec).
  - 14:51:04: Sun/Venus Dec = 10φ (T6 #10).
- **Compared with Wolverhampton:**
  - There, Saturn and Pallas spanned the two races and Mercury handed on 130/9.
  - Here, Mars spans both and Mercury sits exactly at the Gonggong–Mars midpoint between the races.
  - Both times there is a slow or busiest body common to the two tops, a fast body (Mercury) linking to it between the races, and star frames at the race moments.
- **Real offs (Eddie):**
  - R6 Haydock off 14:20:21 (+0.35), race 3m03.5 → finish about 14:23:25.
  - T6 Kempton off 14:41:08 (+1.13), race 2m34.5 → finish about 14:43:43.
- **R6 Haydock:** **its #1, Makemake/Mars (busiest Mars), goes exact at 14:22:50, DURING the race**, and the Moon is at mid(Ceres, Spica) at 14:22:39, also during the race. **No fast point does anything from the off to the finish** (the empty sky, like the 12:10 Selangor outsider).
- **T6 Kempton:**
  - **the Vertex is opposite Pluto in RA at +1.1 (14:41:06, two seconds before the real off). Pluto is a #1 body (Pluto/Quaoar).**
  - In the same minute the Vertex is on the nodal axis in Dec (contra-parallel to Ketu, parallel to Rahu, +0.9) and parallel to the Moon (+0.6).
  - The Moon's φ² star frame came 56 s before the off; Antares–Moon–Algol 1+√2 came 29 s after the finish.
  - The Midheaven is parallel to Vesta (+2.5) and Mercury (+3.5) during the race.
  - **The Vertex thread fires at the real off: fav beaten** ✓
- Between the races: Mercury exactly at the Gonggong–Mars midpoint at 14:30:40.

## 11. 8 Jun 2024: Beverley 14:05 (Perfect Part 125/1; Maw Lam 7/2F 2nd) and Bangor-on-Dee 14:15 (Almazhar Garde 12/1; Daranova 3/1F 7th)
- Real offs: Beverley 14:07:02 (+2.0), 1m04 race, finish about 14:08:06. Bangor 14:15:08 (+0.1), 6m02 chase, finish about 14:21:10.
- **Busiest body in BOTH races: SATURN. Next-busiest in BOTH: PALLAS.** This is the same pair that spanned Wolverhampton 29 Sep 2026.
- 24 pairs sit in the top 30 of both races; #1 is Altair/Uranus in both.
- Timeline:
  - 14:05:02: Mercury in Polaris–Mercury–Capella, RA ratio 3
  - 14:07:02: Beverley off. Sun–Orcus 57√2 at the off (Orcus is a #2 body). **No fast point does anything from the off to the finish** (empty sky, like R6).
  - 14:13:40: Part of Spirit on the nodal axis in Dec, 1.5 min before the Bangor off
  - 14:15:00: **Moon/Quaoar, Bangor's #2, peaks at 10φ³, 99.8, at the Bangor off**
  - 14:19:42: **Mercury in Deneb Algedi–Mercury–Algol, Dec ratio 2, during Bangor**
  - 14:20:00: Sun/Gonggong 70√2 at 100.0 (Beverley #16), during Bangor
  - **14:21:00: Chiron/Mercury Dec 110/9 at 99.9 (Bangor #8), at the Bangor finish**
- **Field check:** Saturn or Pallas as busiest or next-busiest across the 96: Saturn 4 fav-won vs 5 fav-beaten; Pallas 8 vs 7; both together 1 vs 1. Mars 9 vs 4. **So a Saturn/Pallas-heavy sky by itself does NOT mark a beaten favourite.** What repeats in these pairs is how things land at the race moments: Mercury links in, exact star frames or numbers come right at the off or the finish, and the fast-point fav threads are absent.
- Moon star frames in this pair are not trusted: the two courses' Moon positions are stitched at 14:10, which gave duplicate crossings.

## 12. Control pair, both favourites WON: 2 Oct 2026 Ascot 14:25 (Pink Larkspur 7/4F) and Hexham 14:48 (Mr McLoughlan 13/8F)
- Real offs: Ascot 14:25:08 (+0.13), 1m29 race, finish about 14:26:37. Hexham 14:48:49 (+0.82), 4m05 race, finish about 14:52:55.
- **The fav threads T1–T4: NONE fire in either race.** Both favourites won anyway.
- Busiest body in BOTH: **JUNO** (Ascot Juno and Neptune joint; Hexham Juno). #1 in both: Gonggong/Regulus. 23 pairs are in both top 30s. So a spanning body is present here too.
- At the offs:
  - Ascot: the Ascendant is opposite Betelgeuse (a star) at +0.8, during the race. The Midheaven is parallel to Pallas at +1.9, about 17 s after the finish. No Vertex, no Part of Fortune, nothing on the nodal axis.
  - Hexham: Part of Fortune is opposite Fomalhaut (a star) at +0.3, just before the off. **Part of Spirit is conjunct Saturn in RA at +1.5, 41 s after the off.** The Vertex is contra-parallel to Deneb Algedi (a star) at +2.9, during the race. Nothing on the nodal axis.
- Timeline:
  - 14:36:00: Sun/Vega Dec 10φ³ at 99.9 (Ascot #6), between the races
  - 14:47:00: **Mercury/Rahu RA 75φ at 99.6**, 1.8 min before the Hexham off
  - 14:50:30: Moon = mid(Betelgeuse, Bellatrix) in RA (frame 1:1), during Hexham
  - 14:52:48: Neptune = mid(Moon, Quaoar) in RA, 7 s before the Hexham finish
  - about 14:53:00: **Sun–Mercury RA 15√2 at 99.5**, at the Hexham finish
  - During Ascot: nothing exact.
- **Against the four beaten-fav pieces:**
  1. Fav threads absent: **also true here, so absence alone does not mark a beaten favourite.**
  2. Fast points quiet at the off: Ascot is nearly quiet, and the favourite won. **Quiet does not separate.** But the **Vertex on a body at the off, or a fast point on the nodal axis, is absent here.** Here the Vertex touches only stars. Fits the 5th thread (Vertex exact on a non-star body).
  3. Mercury linking at race moments: **also here** (Mercury/Rahu before the Hexham off; Sun–Mercury at the Hexham finish, like Chiron/Mercury at the Bangor finish). **Does not separate.**
  4. Top numbers or slow-body frames exact during the races: **absent here.** No top-12 number goes exact during either race, and the only events during Hexham are Moon-driven midpoints. In the beaten pairs, the mover was a slower body: Makemake/Mars #1 during Haydock, Pallas at the Deneb Algedi–Rigel midpoint at the Wolverhampton finish, Saturn in the Spica–Bellatrix frame during Wolverhampton 19:00, and Mercury in the Deneb Algedi–Algol frame during Bangor.
- What is left from the pair pattern after one control: **the Vertex on a body (not a star) at the off, and a top number or non-Moon body frame going exact DURING the race.** A spanning busiest body, Mercury links, and missing fav threads all show up when favourites win too.
- A fast point on a slow body still happened here (Part of Spirit on Saturn at the Hexham off), and the favourite won. So it is the Vertex in particular, not any fast point.

## 13. The course latitude as a fixed point in declination (latplace.py)
- Tool: /home/claude/selangor/tools/latplace.py `RACE OFF DUR`. The points are LAT, -LAT (the mirror below the equator) and COLAT (90 minus lat).
  - A: slow bodies holding a clean Dec distance to the place at the off.
  - B: |Dec| / lat on an equator ratio.
  - C: events from OFF-5 to the finish+3. Fast-point numbers to the place are shown only when they equal one of the race's top-12 values (**) or a number the place already holds (==). Also midpoints with the place and star–body–place frames.
- Run on the 8 UK pair races at their real offs and 6 Selangor races (offs to the minute; race length assumed 1.5 min).
- **Fast-point frames and midpoints with the place happen in EVERY race**, several each, whether the favourite won or not. Like Mercury, they do not separate on their own.
- **Slow holdings and ratios on the place are rare:**
  - Ascot (fav won): Betelgeuse to LAT 44 (95.0); Pleiades to COLAT 6(1+√2).
  - Hexham (fav won): Deneb Algedi to -LAT 24φ (99.2); Uranus |Dec| = 1/φ² of the latitude.
  - Haydock (beaten): Alphecca |Dec| = ½ the latitude.
  - Beverley (beaten, 125/1): Ceres |Dec| = ½ the latitude, below the equator.
  - Bangor (beaten): Antares |Dec| = ½ the latitude, below the equator; Haumea to COLAT 9(1+√2).
  - Kempton, both Wolverhampton races and Selangor: none.
  - So 3 of the 6 beaten-fav races have a body at half the course latitude. Neither fav-won race does (Hexham has 1/φ² instead). The tolerance is loose (0.15%), and these are slow, so they hold all afternoon at that course. That would fit "one course all favs, the others not".
- **The place delivering numbers:**
  - Hexham (fav won): the Vertex to LAT = 24φ at 14:50:54, during the race. That is the same number Deneb Algedi holds to -LAT (a mirror through the place).
  - Bangor (beaten): Part of Spirit to COLAT = 10φ³ during the race. That is the race's #2, Moon/Quaoar, which peaked at the off. The Vertex to COLAT = 35 (#5 Jupiter/Quaoar) also falls during the race.
  - Selangor 14:10 (Lim's Craft, mid price): Part of Fortune to -LAT = 7φ (#9) and the Ascendant to -LAT = φ⁶ (#2), both during the race.
  - Selangor 15:15 (Pacific Hawk, outsider): the Midheaven to -LAT = 130/9 (#10) at the finish.
  - Selangor 16:15 (Anjou Crown, fav): the Ascendant and then Part of Fortune bring the #1, 130/9 (Ketu/Vesta), and the #3, 6(1+√2), onto LAT during the race. LAT = mid(Ascendant, Part of Fortune) during the race.
  - Selangor 13:40, 14:40 and 15:45 (favourites): none.
- Next test: a single day where one course was all favourites and the others were outsiders. Same sky, different latitudes, so A and B per course show what the place alone adds.

## 14. 3 Sep 2026: Lingfield AW 16:55 (Lion Of God 33/1; Mouj Albuhoor 8/13F 2nd) and Haydock 17:00 (Mehmas Champion 80/1; Storm Point 5/2F 5th)
- Real offs: Lingfield 16:55:57 (+0.95), 1m25, finish 16:57:22. Haydock 17:00:51 (+0.85), 2m15, finish 17:03:06. The two races overlap.
- Same sky: busiest is Jupiter in both. The top 12s are nearly the same: Altair/Rahu, Pluto/Vesta, Alkaid/Pallas, Alkaid/Sedna.
- Fav threads: T4 (Midheaven + Sun) shows on both sheets, but at +9.5 (Lingfield) and +15 (Haydock), after both real finishes. T3 at Lingfield is at +13.6, also after. **Nothing fav-leaning lands between the off and the finish.**
- **Lingfield:** the Ascendant is contra-parallel to Mars 2.2 min before the off and conjunct Vega (a star) 15 s before. **No fast point is on a body during the race.** Sun–Gonggong RA 124√2 peaks during the race (98.7). The Midheaven is parallel to Deneb Algedi (a star) 20 s after the finish.
- **Haydock:**
  - The Midheaven is conjunct Haumea 1.75 min before the off.
  - **The Ascendant + Moon AND Part of Spirit + Sun both = #4 Alkaid/Sedna 144.4666, 27 s before the off.** This is the broad "fav shape" again, with the favourite beaten, as at Wolverhampton.
  - **The Vertex is contra-parallel to Quaoar (a body) 6 s before the finish, DURING the race.**
  - The Vertex is at mid(LAT, Ascendant) during the race and at mid(LAT, Pluto) 55 s after the finish. Pluto is a #1 body (Pluto/Vesta).
  - The Moon = mid(Capella, Polaris) in RA at 17:03:06, the Haydock finish.
- **Mercury does NOT link these two.** Between and during the races there is no non-Moon slow body or top number going exact.
- Latitude:
  - Lingfield: Neptune to COLAT = 24φ (98.4). 24φ also appeared at Hexham, where the favourite won.
  - Haydock: **Alphecca = ½ the latitude again.**
- **Field check of the latitude ratios across the 96 (scheduled time, slow bodies):**
  - ½: 6 fav-won vs 5 beaten
  - 1/φ²: 5 vs 2
  - 1/(1+√2): 4 vs 7
  - 1/√2: 0 vs 2
  - The ½ hits are ALL fixed stars at fixed courses. Alphecca at Haydock: 3 won and 3 beaten in the 96, plus Market Rasen. Antares (below the equator) at Nottingham, Fakenham and Bangor. **A star ratio is a permanent property of the course, so it cannot mark a race or a day.** Only a moving body (planet or TNO) on the course latitude could change between days at one course.
- Where the pair pieces stand after 4 beaten pairs and 1 fav-won pair:
  - Missing fav threads, a common busiest body, and fast-point frames with stars and the latitude: present either way.
  - Mercury links: in 3 of 4 beaten pairs, and also in the fav-won pair.
  - A slow or top-number contact exact during the race: Wolverhampton, Haydock 2021 and Bangor; not here, not in the control.
  - The Vertex on a body (not a star) from just before the off to the finish: Wolverhampton 18:30 (Sun) and 19:00 (Saturn, Vesta, Sun), Kempton 2021 (Pluto, nodes), Haydock 2026 (Quaoar). Absent at Haydock 2021, Beverley, Bangor and Lingfield (empty or star-only fast points). In the fav-won control, the Vertex touches only stars.

## 15. Slow sky, race by race (slowsky.py, fast points left out)
- Tool: /home/claude/selangor/tools/slowsky.py `RACE [OFF DUR]`. Output: slow_sky_pairs.txt (the pairs at real offs) and slow_sky_96.txt (fav won and fav beaten halves).
- What the pairs show at the race moments:
  - **A race top-12 slow pair exact between the off and the finish:**
    - Bangor: #1 Altair/Uranus 6φ exact at the off to the second, #4 Chiron/Vesta during, #8 Chiron/Mercury at the finish.
    - Haydock 2021: #1 Makemake/Mars during, #3 Arcturus/Venus at the off.
    - Kempton 2021: #5 Ceres/Chiron during; #8 Mars/Mercury and #12 Arcturus/Mars at the off.
    - Wolverhampton 18:30: #3 Arcturus/Vesta at the finish. 19:00: #7 Algol/Vesta and #12 Alkaid/Pallas just after the finish.
    - None at Beverley, Lingfield or Haydock 2026.
    - Fav won: Hexham #3 Juno/Neptune 41φ during; Ascot none.
  - **The Moon landing on the race's own top number at the race:**
    - Beverley: Moon–Procyon 6φ at the finish, the #1 number (Altair/Uranus 6φ, the same #1 as Bangor that day).
    - Bangor: Moon/Quaoar #2 at the off.
    - Wolverhampton 19:00: Moon–Vega #10 at the off.
    - Fav-won pair: none.
  - **The Sun on a number DURING the race:**
    - Beaten: Beverley (Orcus 57√2), Bangor (Gonggong 70√2), Lingfield (Gonggong 124√2), Haydock 2026 (Sirius 61).
    - Fav won: Hexham (Mercury 15√2).
    - None: Ascot, Wolverhampton, Haydock/Kempton 2021.
  - Sun–Moon number during the race: only Kempton 2021 (Dec 10√2 at 14:42:45).
  - Slow shapes held at the off are shared by both races of each day (they are slow), so they belong to the day. Saturn is in one on 4 of the 5 days, the fav-won day included.
  - Standing still:
    - Venus turns retrograde in RA on the day of Ascot/Hexham (both favs won) and 2.8 days after Wolverhampton (both beaten).
    - Uranus, Pallas and Vesta turn within about a week of 3 Sep 2026.
    - Nothing on 4 Sep 2021 or 8 Jun 2024.
- The Moon to some body makes a number every few seconds in RA in every race, so a Moon–body number on its own means nothing. Only the "=" lines (Moon on the race's own top number) are kept apart.

## 16. 8 Jul 2022 afternoon around T45 York 15:50: favs beaten until about 15:40, then favs win everywhere
- Results (real offs):
  - York 15:15: off 15:16:43, fav 8/11 2nd (BEATEN; xlsx still to come)
  - Ascot 15:25: off 15:25:48, 1m43, 22/1 beat 5/2F (BEATEN)
  - Newmarket July 15:35: off 15:38:37, 1m36, 16/1 beat Inspiral 1/7F (BEATEN)
  - **York 15:50 (T45): off 15:51:26, Asaassi 6/5F WON** (race time still needed)
  - Ascot 16:00: off 16:00:13, 2m36, 2/1F WON
  - Newmarket 16:10: off 16:12:28, 1m23, 11/4JF WON
  - York 16:25: off 16:25:52, 1m24, 7/4F WON
- **The same sky, how the top pairs move through the afternoon (slow pairs exact at the same clock time at every course):**
  - 15:04 Pallas/Vega RA 1300/9 (144.44) exact
  - 15:28–15:31 Ketu/Pallas Dec 10φ and Gonggong/Juno Dec 13 exact (just after the Ascot 15:25 finish)
  - **15:33 Juno/Mercury Dec 9(1+√2); 15:34:20 Mercury/Vega RA 1600/9.** These are the #2/#3 at Newmarket 15:35, exact 4–5 min before its off.
  - 15:35:36 Algorab/Mars Dec 27
  - **15:45:45 Antares/Venus Dec 20(1+√2)**
  - 15:48:32 Alkaid/Mars Dec 24φ; 15:48:58 Fomalhaut/Pallas RA 49φ
  - **15:52:31–15:53:52 Capella/Venus Dec 10(1+√2) and Betelgeuse/Venus Dec 130/9 exact (#2 and #1 at York 15:50), during York 15:50**
  - 15:58:40 Algol/Pallas RA 150/9 (Ascot 16:00 #1, 1.5 min before its off)
  - **16:00:24 Fomalhaut/Venus RA 93**, during Ascot 16:00
  - **16:03:38 Quaoar/Venus Dec 37**, at the Ascot finish
  - **16:08:57 Mars/Venus RA 29φ**, 3.5 min before the Newmarket 16:10 off
  - 16:21 Chiron/Juno and Deneb Algedi/Vesta
  - **16:24:56 Sun/Transpluto RA 29φ (York 16:25 #1), 56 s before its off.** The same 29φ as Mars/Venus.
  - 16:26:58 Mars/Pallas Dec 110/9 (#3), during York 16:25
  - 18:16 Jupiter/Regulus RA 1300/9, the same number as Pallas/Vega at 15:04
- **Ranks:**
  - **Mercury pairs** are high in the beaten races (Mercury/Vega #5, #2; Juno/Mercury #6, #3) and sink after 15:40 (#8, #8, #12, #19).
  - **Venus pairs** climb: Betelgeuse/Venus #10, #9 → #1, #3, #2; Capella/Venus #18, #11 → #2, #4, #6. Venus becomes busiest by 16:10.
  - Moon pairs are in the beaten tops (Algol/Moon #7, Moon/Vesta #1) and absent after.
  - **The beaten stretch belongs to Mercury and the Moon; the winning stretch to Venus.** (Compare the Venus station on the Ascot/Hexham fav-won day.)
- **Fast points at the real offs:**
  - Ascot 15:25 (beaten): the fast points are silent. Moon–Algol RA 1500/9 (#7 Algol/Moon) during the race.
  - **Newmarket 15:35 (beaten):**
    - Part of Fortune + Sun = 1300/9 (#6, #7) at +4.1, DURING the race. The T1 shape fired during a beaten race; by its frozen ±1.5 of scheduled, it is outside.
    - The Vertex is contra-parallel to Pluto at +4.6, during the race.
    - The Ascendant + Moon and Part of Spirit + Sun = #1 Moon/Vesta at +5.2, at the finish.
    - The Midheaven is opposite Saturn 20 s after the finish.
  - **York 15:50 (won):**
    - Part of Fortune + Sun = 1300/9 at +0.2 and the Vertex contra-parallel to Pluto at +0.4. These are the SAME two contacts as Newmarket, but 1.0–1.2 min BEFORE the off rather than during the race.
    - At the off, the Ascendant is parallel to Vesta.
    - The Ascendant is parallel to Saturn at +2.9 and the Midheaven contra-parallel to the Moon at +3.2.
  - Ascot 16:00 (won): the Midheaven is parallel to Regulus (#2 body) at +0.4, Part of Spirit conjunct Castor, and Part of Fortune conjunct Saturn at +1.6, during the race. Moon–Algol Dec 38√2 at the off.
  - Newmarket 16:10 (won): **the Midheaven + Sun = #5 Mars/Venus 29φ at +1.0** (T4 shape), with the Midheaven conjunct and parallel to Transpluto at +1.1. The Midheaven is parallel to Mars at +2.2, at the off. Moon–Pallas Dec 100/9 at +1.
  - York 16:25 (won): the fast points are quiet. Sun/Transpluto 29φ (#1) exact at the off.
- **What the fast points do in this group:**
  - The same contacts appear on both sides of the switch, with different timing.
  - At Newmarket (beaten), Part of Fortune + Sun and the Vertex–Pluto contact land INSIDE the race. At York (won), they come just before the off.
- **York 15:50 race time 2m12.94 → finish 15:53:39.**
  - DURING the race: **#2 Capella/Venus Dec 10(1+√2) exact at 15:53:03**; Sun–Ketu RA 50(1+√2) (#24) at 15:52:40; Moon–Pluto Dec 10 at 15:51:55; Moon–Saturn Dec 17/9 at 15:52:12.
  - **#1 Betelgeuse/Venus Dec 130/9 exact at 15:53:52, 13 s after the finish.**
  - Moon–Spica Dec 1φ (the same number as #6 Ketu/Pallas) at 15:54:32, 53 s after the finish. The "Moon on the race's own number" happens here too, in a fav-won race, just after the finish.
  - **So a top-12 slow number exact during the race happens in fav-won races too (Hexham, York 15:50).** What differs here is that the exact pairs are Venus pairs.
- **York 15:15 (BEATEN: The Platinum Queen 3/1 beat Yahsat 8/11F; off 15:16:43, 58.4 s, finish 15:17:41):**
  - #1 Pallas/Rigel Dec 4φ exact 15:15:32, 1.2 min before the off. Part of Fortune to -LAT = 4φ at 15:13:33. The Midheaven + Sun complete the #1 at about 15:14 (the T4 shape, 2.7 min before the off).
  - **The Mercury pairs are forming: #7 Mercury/Vega and #9 Juno/Mercury, both exact 15:33–15:34.** Betelgeuse/Venus is only #11, exact 15:53.
  - At the off: the Ascendant parallel to the Moon and Part of Spirit parallel to the Sun (15:16:06); the Midheaven parallel to Haumea. **Part of Spirit + Moon complete #9 Juno/Mercury's number at 15:17:42, the finish.**
  - Moon–Neptune RA 88φ at 15:16:49 (during). Moon–Aldebaran Dec 18φ (the #10 Orcus/Rahu number) 17 s after the finish.
- **The afternoon in one line:** all three beaten races (15:16–15:40) sit in the run-up to the Mercury pairs going exact at 15:33–15:34. At York 15:15 a fast point brings a Mercury pair's number to the finish. All four winning races sit in the run of Venus pairs going exact (15:45 Antares/Venus → 16:09 Mars/Venus), with the #1 and #2 of York 15:50 exact as Asaassi finished.
- Caution from earlier pairs: Haydock 2021 (beaten) had #3 Arcturus/Venus exact at the off, and Hexham (fav won) had Sun–Mercury at the finish. So Mercury vs Venus is the shape of THIS afternoon, not yet a rule.
- **Looking again, transit sky only (no fast points). Every slow-pair exact (≥99.9) between 15:00 and 16:40, at York; star–star pairs left out.**
  - **The Sun goes quiet through the beaten stretch.** Sun contacts at 15:03 (Bellatrix, Sirius, Venus Dec φ⁻¹), 15:08 Castor, 15:11 Algorab and 15:20 Alphecca. **Then nothing from 15:20 to 15:52**, while all three favourites lose. Then Ketu/Sun 50(1+√2) at 15:52:41 (during York 15:50), Mars/Sun 77 at 16:03:32, Makemake/Sun 90 at 16:23 and Sun/Transpluto 29φ at 16:24:56.
  - **Mercury has a burst in the gap, 15:41–15:49:** Pallas 300/9 at 15:41:49 (Pallas is busiest all afternoon), Sirius 3√2 at 15:43, Procyon 160/9 at 15:44:50, Algol 50 at 15:45, Sirius φ³ at 15:47, Altair 66(1+√2) at 15:48 and Chiron 83 at 15:48:56. Seven Mercury contacts in seven minutes, then Venus takes over.
  - **Venus becomes the steady beat after 15:44:** Polaris, Antares, Rigel, Capella, Betelgeuse, Fomalhaut, Quaoar, Mars, Castor, Pluto, Algorab, Transpluto, Alkaid and Sedna, about one every 3–6 min until 16:34. Before that, only Capella RA 16/9 at 15:26:22 (during Ascot 15:25) and Jupiter Dec 20 at 15:30.
  - **Family:**
    - The silver (1+√2) numbers gather in the fav-won stretch: Antares/Venus 20(1+√2), Altair/Mercury 66(1+√2), Ketu/Sun 50(1+√2), Capella/Venus 10(1+√2), Castor/Venus 15(1+√2) (16:11:44, 44 s before the Newmarket 16:10 off) and Pluto/Venus 57(1+√2).
    - In the beaten stretch there is only Juno/Mercury 9(1+√2).
    - Venus makes 5 of those silver numbers.
  - **A closed figure, 16:03–16:25:** Mars/Sun = 77 (16:03:32) and Transpluto/Venus = 77 (16:23:04); Mars/Venus = 29φ (16:08:54) and Sun/Transpluto = 29φ (16:24:56). Sun, Mars, Venus and Transpluto swap the same two numbers in RA. It is complete at the York 16:25 off.
  - **The same numbers carried through the afternoon (scaled ×10 counted as one):**
    - 1300/9: Pallas/Vega at 15:04:20 → Moon/Jupiter 130/9 at 15:13 (3.6 min before the York 15:15 off) → Moon/Ketu 1300/9 at 15:37:34 (1 min before Inspiral's off) → Betelgeuse/Venus 130/9 at 15:53:55 (York 15:50 finish) → Jupiter/Regulus at 18:16.
    - 160/9: Capella/Venus 16/9 at 15:26 → Mercury/Vega 1600/9 at 15:34 → Mercury/Procyon 160/9 at 15:44:50 → Sedna/Venus 160/9 at 16:34. Venus holds it, Mercury carries it through the beaten stretch, and Venus takes it back.
    - 110/9: Makemake/Mars at 15:11:56 (York 15:15 #3) → Rigel/Venus 11/9 at 15:47:55 → Mars/Pallas 110/9 at 16:26:56 (during York 16:25).
    - 57(1+√2): Pallas/Spica at 15:06 → Pluto/Venus at 16:18.
    - 10φ / 1φ: Ketu/Pallas at 15:27:58 → Moon/Spica at 15:54:32 → Altair/Mars at 16:14:41.
  - Mars goes back to the same partners an hour on: Algorab at 15:32/15:35 and 16:34; Makemake at 15:11 (Dec) and 16:33 (RA).
- **Sun and Moon midpoints and midpoint ratios, 15:00–16:40** (Sun/Moon = mid(Y,Z); Y–Sun/Moon–Z at φ, φ², √2, 1+√2, 2, 3; body = mid(Sun,Moon); bodies dividing Sun–Moon; Sun/Moon as an end):
  - **The Sun is silent in midpoints too, from 15:06 to 16:07.** 15:04:34 Venus–Sun–Makemake Dec φ²; 15:05:53 Sun = mid(Castor, Sirius) RA; then nothing until 16:07:42 Arcturus–Sun–Pleiades Dec 2; 16:18:59 Arcturus–Sun–Mercury Dec φ²; 16:22:55 Algorab divides Sun–Moon 3:1 in RA.
  - No body sat at the Sun–Moon midpoint all afternoon.
  - **The Moon as the exact MIDDLE (1:1) appears only from 15:57:** Moon = mid(Gonggong, Vesta) at 15:57:31, mid(Gonggong, Saturn) at 16:07, **mid(Quaoar, Regulus) RA at 16:12:58 (during Newmarket 16:10)**, **mid(Spica, Vesta) at 16:14:05 (Newmarket finish)**, mid(Orcus, Vesta) at 16:20, mid(Neptune, Pluto) at 16:22, mid(Saturn, Spica) at 16:23:57 and mid(Orcus, Saturn) at 16:29.
    - Between 15:06 and 15:57 (the beaten stretch) the Moon is never the middle of anything. It is only an END (Saturn = mid(Moon, Sirius) at 15:12, Vesta = mid(Moon, Algorab) at the York 15:15 finish) or in unequal frames.
    - Around 15:59–16:00 the Moon is an end three times: Saturn = mid(Moon, Algorab), Juno = mid(Moon, Uranus), **Jupiter = mid(Moon, Aldebaran) during Ascot 16:00**.
  - The Moon's frames all afternoon are among the same southern-Dec group: Spica, Orcus, Gonggong, Algorab, Sirius, Deneb Algedi, Quaoar and Saturn.
    - At the beaten races: York 15:15 at the off Saturn–Moon–Spica √2, at the finish Deneb Algedi–Moon–Spica 1+√2; Ascot 15:25 during Deneb Algedi–Moon–Orcus 1+√2; Newmarket 15:35 at the finish Quaoar–Moon–Orcus φ and Deneb Algedi–Moon–Gonggong 2.
    - At the fav-won races: York 15:50 at the off Transpluto–Moon–Alphecca RA 3, during Algorab–Moon–Orcus 1+√2; Ascot 16:00 during Quaoar–Moon–Spica √2, at the finish Deneb Algedi–Moon–Spica 2; York 16:25 at the off Sirius–Moon–Gonggong 2, during Ketu–Moon–Gonggong φ².
- **Six more checks on the afternoon:**
  1. **The Moon's state:**
     - Waxing between first quarter (7 Jul 03:14) and full (13 Jul 19:37); elongation 109°.
     - Dec -12.0 and falling toward its monthly low (-26.9 on 12 Jul).
     - 16° before the south node; it crosses the ecliptic on 9 Jul at 18:27. Mid speed (12.84°/day).
     - Not out of bounds. **Nothing in the Moon's state changes at 15:40–15:50.**
  2. **Sun–Moon distance:** RA 65φ at 14:33:56, then **no Sun–Moon number until 75√2 at 16:22:56** (3 min before the York 16:25 off), then 44(1+√2) at 16:42. The Dec makes no number. So the Sun–Moon pair makes no number through all the beaten races and the switch. The first one comes at the last race.
  3. **Mercury–Venus:**
     - Their own distance makes no number near the switch: RA 12φ at 10:18 and 14√2 at 19:38; Dec flat about 1.80–1.84.
     - **Mercury is out of bounds all day** (Dec +23.70, beyond the Sun's 23.44). Venus is at +21.88 and rising.
     - Mercury moves 2.27°/day and Venus 1.28°/day.
  4. **Royal stars (Regulus, Aldebaran, Antares, Fomalhaut):**
     - Before the switch only the Moon (plus Mercury/Aldebaran at 15:05) touches them: Antares at 15:12, Regulus at 15:14, Aldebaran 18φ at the York 15:15 finish, Fomalhaut 12√2 at the Ascot 15:25 off.
     - **In the switch window, four royal contacts in 8 min, three of them silver:** Fomalhaut/Moon 7(1+√2) at 15:41:16, Antares/Venus 20(1+√2) at 15:45:50, Aldebaran/Moon 60(1+√2) at 15:46:18, Fomalhaut/Pallas 49φ at 15:48:59.
     - After the switch: Regulus/Moon 100φ⁻¹ at the York 15:50 finish; Fomalhaut/Venus 93 during Ascot 16:00; Antares/Moon 300/9 1.4 min before the Newmarket 16:10 off (the same 300/9 as Mercury/Pallas at 15:41:49); Mercury/Regulus at 16:08 and 16:16; Moon/Regulus at 16:19.
  5. **The backbone (slow pairs held for hours):**
     - Ketu/Rigel Dec 6φ (exact 12:48), Pallas/Vega RA 1300/9 (exact 15:04), Jupiter/Regulus RA 1300/9 (exact 18:16), Orcus/Rahu Dec 18φ (exact 18:25), Deneb Algedi/Saturn conjunction (exact 01:54 next day).
     - **The afternoon sits between 1300/9 going exact on Pallas/Vega (15:04) and on Jupiter/Regulus (18:16).** The Moon carries 130/9 to Jupiter (15:13) and Ketu (15:35); Betelgeuse/Venus has it at 15:53. No backbone pair goes exact at the switch; the backbone runs through both stretches.
  6. **Planetary hours (Friday = Venus day):**
     - The Venus hour ends and the Mercury hour begins at **Newmarket 15:47:51, Ascot 15:50:33 and York 15:57:10**. The switch falls at the hour change at all three courses.
     - **All three beaten races ran in the Venus hour.** Ascot 16:00, Newmarket 16:10 and York 16:25 (favs won) ran in the Mercury hour. York 15:50 (fav won) ran in the last minutes of York's Venus hour (finish 15:53:39, hour ends 15:57:10).
     - This is the opposite way round to the bodies: in the Venus hour Mercury's pairs are going exact; in the Mercury hour Venus's pairs are.

## 17. Method for the rest of the 96 (agreed 4 Oct 2026)
- Each of the 96 is dug as a GROUP, like 8 Jul 2022: the race at its real off, plus every UK race within about ±45 min at any course and the races before and after at its own course. Real offs, winning times and results come from pasted Racing Post pages. One sky-only CSV per race; Eddie makes the workbooks; I process them.
- The fast points are set aside (Eddie: "they are not doing the heavy lifting"). We read the transit sky and just say what we see.
- Tool: /home/claude/selangor/tools/afternoon.py GROUP.csv (columns race,off,dur_s,band,note). Report sections:
  - A: results and threads (reference only)
  - B: top-pair ranks across the group
  - C: slow-pair exacts by time and by body
  - D: numbers carried
  - E: Sun/Moon midpoints and ratios
  - F: Moon state, Sun–Moon, Mercury–Venus, out of bounds
  - G: royal stars
  - H: backbone
  - I: planetary hours at each course
- Group files and reports are in /home/claude/afternoon/ (g_YYYYMMDD.csv, r_YYYYMMDD.txt). 8 Jul 2022 reproduces section 16. The new run adds: Ceres is also out of bounds (+25.8) that day.
- Night planetary hours (races after sunset) are not computed yet.

## 18. 4 Sep 2021 afternoon (R6 Haydock 14:20, T6 Kempton 14:40): 16 races, Thirsk / Haydock / Stratford / Ascot / Kempton
- Results by real off:
  - 13:42 Thirsk B
  - 13:45 Haydock B
  - 13:55 Stratford W (chase)
  - 14:00 Ascot B
  - 14:06 Kempton B
  - 14:18 Thirsk B
  - **14:20 Haydock B (R6)**
  - 14:30 Stratford W
  - 14:35 Ascot W
  - **14:41 Kempton B (T6, Hukum 30/100)**
  - 14:53 Thirsk W
  - 14:55 Haydock B
  - 15:05 Stratford W
  - 15:10 Ascot B
  - 15:18 Kempton W
  - 15:27 Thirsk W
  - Before 14:30: 6 of 7 favs beaten (the one winner over jumps). From 14:30: 6 of 9 won.
- Report: /home/claude/afternoon/r_20210904.txt
- **Busiest bodies:**
  - Mercury is busiest in the early beaten races (Haydock 13:45; Ascot 14:00 with the Sun; Haydock 14:20 with Mars), and also at Stratford 13:55 (W, joint with Chiron). Mars runs through 13:40–14:41.
  - From 14:53 Transpluto and Juno take over (Thirsk 14:50 W: Moon, Sun and Transpluto).
  - **Mercury busiest in the beaten stretch, as on 8 Jul.**
- **Top pairs pass the lead:** Chiron/Juno #1 (exact 13:40) → Orcus/Polaris #1 (exact 14:07) → Makemake/Mars #1 (exact 14:22:48, during Haydock 14:20) → Pluto/Quaoar #1 from Ascot 14:35 (exact 14:51) → Fomalhaut/Juno #1 at Thirsk 15:25 (exact 15:23). Sun/Venus climbs to #3–#4 at 14:51 (Dec 10φ exact 14:51:04).
- **The Sun is quiet 14:03–14:37** (no non-Moon Sun contact) across Kempton 14:05 B, Thirsk 14:15 B, Haydock 14:20 B and Stratford 14:30 W. The Sun is the MIDDLE of nothing from 13:26 to 14:50. Then: 14:50 Ketu–Sun–Aldebaran 3, 15:09 Ketu–Sun–Rahu 2 (during Stratford 15:05 W), 15:13 Rigel–Sun–Aldebaran φ (Ascot 15:10 B finish), 15:34 Sun = mid(Ceres, Eris).
- **The Moon as the exact middle at a race moment:**
  - Fav WON: Ascot 14:35 (= mid(Alphecca, Uranus) at the finish); Stratford 15:05 (= mid(Aldebaran, Venus) at the off, = mid(Alphecca, Haumea) during); Kempton 15:15 (= mid(Capella, Vesta) during); Thirsk 15:25 (= mid(Castor, Orcus) during).
  - Fav BEATEN: only Haydock 14:20 (= mid(Ceres, Spica) during).
  - **With 8 Jul (Newmarket 16:10 twice), the Moon is the exact middle at a race moment in 6 fav-won races and 1 beaten race.**
- **Where each race's own #1 pair goes exact:**
  - **During the race:** Kempton 14:05 B (+1.2 m), Haydock 14:20 B (+2.4 m). Earlier: Bangor 2024 B (#1 at the off).
  - **Within 2 min before the off:** Stratford 13:55 W (−0.4, with #2 also at the off), Stratford 14:30 W (−1.1), Thirsk 14:50 W (−1.8, #2 at the off), plus Ascot 16:00 W (−1.5) and York 16:25 W (−0.9) on 8 Jul. Against: York 15:15 B (−1.2) and Ascot 14:00 B (Moon/Regulus −0.8, a Moon pair).
  - 3–6 min before: Thirsk 13:40 B, Haydock 13:45 B, Haydock 14:55 B, Newmarket 15:35 B (Moon pair) / Kempton 15:15 W, Thirsk 15:25 W.
  - 10+ min away: mixed (Thirsk 14:15 B, Ascot 15:10 B, Kempton 14:40 B after; Ascot 14:35 W after, Stratford 15:05 W).
- Planetary hours (Saturday, Saturn): Moon hour B, B, W, B; Saturn hour B, B, B, W, W, B, W, B, W, B; Jupiter hour W, W. **No clean switch at an hour boundary this day.**
- The Moon is a waning crescent (new 7 Sep), Dec +21.7 near its high. Sun–Moon numbers: RA 18φ at the Thirsk 13:40 off (B), Dec 10√2 during Kempton 14:40 (B), RA 28 1.4 min before the Stratford 15:05 off (W). Mercury–Venus: no number. Nothing out of bounds.
- Caveats: the RA node axis (Ketu/Rahu = 180) filled section C; now removed from the tool. Moon Dec frames repeat when several courses are stitched (Regulus–Moon–Alphecca listed several times).
- **Across the two afternoons so far:**
  - Mercury leads the beaten stretch.
  - The Sun goes quiet (numbers and as a middle point) through the beaten races.
  - The Moon is the exact middle in winning races.
  - A race's own #1 going exact inside the race goes with the favourite beaten; going exact in the 2 min before the off goes with it winning.
  - The planetary-hour switch was clean on 8 Jul only.
- **Detail of the two outsider races (racedetail.py, each race's own minute file, off to finish ±30 s), against the fav-won races either side.**
  - Planetary hours dropped (Eddie: not needed).
  - **Haydock 14:20 (Golden Flame 9/1; Valley Forge 11/8F 3rd), busiest Mars and Mercury:**
    - During: **#3 Arcturus/Venus RA 120/9 at +0.34 m; #1 Makemake/Mars Dec 170/9 at +2.47 m.** Two of its own top three go exact inside the race.
    - Also during: Pallas/Venus 148 (#20) at +0.31; Mercury/Neptune 167 at +1.72; Jupiter/Moon 22φ at +1.92; Moon = mid(Ceres, Spica) RA at +2.29; Procyon/Venus 53φ at +2.76.
    - Castor/Mars 20√2 (#16) 8 s after the finish.
  - **Kempton 14:40 (Hamish 9/1; Hukum 30/100F 2nd), busiest Mars:**
    - **#12 Arcturus/Mars RA 40, 27 s before the off.** **#5 Ceres/Chiron RA 41√2 during (+0.72 m).**
    - Arcturus – Moon – Makemake Dec φ at +0.60. **Sun/Moon Dec 10√2 at +1.62** (the only Sun–Moon number inside a race that afternoon). Moon/Sirius 300/9 at +1.95; Gonggong/Moon 158 at +2.28.
    - **The Moon on the node axis (Dec = Rahu) 19 s after the finish.**
  - **What the two outsider races share:**
    - **Mars is busiest.**
    - **Arcturus** is in both: Arcturus/Venus (#3) during Haydock; Arcturus/Mars (#12) at the Kempton off; the Arcturus–Moon–Makemake frame during Kempton.
    - **Makemake** is in both: Makemake/Mars #1 during Haydock; in the Moon's frame during Kempton.
    - **Their own top-12 pairs go exact inside the race.**
  - **The fav-won races either side:**
    - **Stratford 14:30 W:** no top-30 pair exact in the race. Juno/Venus Dec 3/9; Mercury = mid(Gonggong, Mars) Dec at +0.25; Rigel – Mercury – Eris φ; Gonggong – Venus – Rigel φ²; Haumea – Moon – Pleiades 2.
    - **Ascot 14:35 W:** only #16 Mercury/Vega and #24 Haumea/Venus during. Chiron/Moon 130/9 and Venus on the node axis (Ketu 43, Rahu 137) just after the finish.
    - **Thirsk 14:50 W:** #2 Aldebaran/Orcus exact 17 s BEFORE the off. During: the Moon makes 12/9 with Makemake, the same number as #7 Haumea/Vesta.
    - None of the three has one of its own top 12 going exact during the race. (Earlier exceptions: York 15:50 #2 and Hexham #3 went exact during fav-won races.)

## 19. 17 Oct 2021 (Sunday; R10 Kempton 14:40, Mercian Prince 13/8F WON): 6 jumps races, Kempton and Sedgefield
- First group made with Eddie's make_sky_group.py (group file and workbooks in one zip). Kempton 14:40 was processed as `kemptonsky_1440` so R10's horse files are not overwritten. Its off is 14:40:29, matching Eddie's earlier timing.
- Results:
  - 14:05 Kempton B (10/11F 3rd)
  - 14:20 Sedgefield W (4/11F)
  - **14:40 Kempton W (R10)**
  - 14:55 Sedgefield B (100/30F 2nd)
  - 15:15 Kempton B (4/6F 2nd)
  - 15:30 Sedgefield W (3/1F)
  - All jumps races, 3.7–7.5 min long.
  - The results alternate; there is no clean before/after split.
- **The slow sky:**
  - **Mercury is standing still**: it turns direct about 18 Oct 01:00 in RA (13:00 in longitude), RA speed −0.07°/day. It makes few contacts: 13:45, 13:58, **14:54 Haumea/Mercury #2 at the Sedgefield 14:55 off (B)**, 15:01 Mercury/Sun 8φ a minute after that finish, 15:06 and 15:44. Also Venus–Sun–Mercury φ² during Kempton 15:15 (B). In Moon frames it appears at Sedgefield 14:20 W and 15:30 W too.
  - **Venus is out of bounds** (Dec −25.2).
  - Haumea is busiest in every race. Altair/Rahu is #1–#2 all afternoon and goes exact at 15:29:48, **the Sedgefield 15:30 off (W)**.
  - The Sun is not quiet in the beaten races here: Procyon/Sun 9φ during Kempton 14:05 B; Juno/Sun 2√2 and the Venus–Sun–Mercury frame during Kempton 15:15 B; Ketu–Sun–Eris during Sedgefield 14:55 B.
- **Kempton 14:40 (R10, fav WON), its own minute file:**
  - **#1 Aldebaran/Sun RA 1200/9 exact during (+1.52 m) and #4 Algol/Pallas 27(1+√2) during (+3.53 m).** Its own top numbers go exact INSIDE the race, and the favourite won.
  - **The Sun and Moon make numbers during the race:** RA 106√2 at +0.57 (race file) and Dec φ⁻¹ about 14:41.
  - Moon = mid(Fomalhaut, Transpluto) 12 s before the off. The Moon touches Saturn, Deneb Algedi, Vega, Pallas, Venus (140/9 and 11√2) and Orcus during. Deneb Algedi – Moon – Chiron φ.
- **Where each race's top pairs go exact:**
  - Sedgefield 14:20 W: #1 during (+3.3)
  - Kempton 14:40 W: #1 during (+1.5)
  - Sedgefield 15:30 W: #1 −0.9, #3 −1.5 before the off
  - Sedgefield 14:55 B: #2 Haumea/Mercury −0.7 before the off
  - Kempton 14:05 B and 15:15 B: nothing near the race
- **Correction:**
  - "Own #1 going exact inside the race → fav beaten" FAILS here: two fav-won jumps races have their #1 exact during the race, as do York 15:50 and Hexham earlier.
  - Still standing: #1 exact in the 2 min before the off goes with a fav win (now 6 W: Stratford ×2, Thirsk, Ascot, York, Sedgefield 15:30, against 2 B).
  - The Moon as the exact middle at a race moment: Kempton 14:40 W at the off and Sedgefield 14:55 B (twice, during). Running total: 7 W races, 2 B races.

## 20. Layered view (layers.py) and half-degree numbers — 8 Jul 2022, 4 Sep 2021, 17 Oct 2021
- Tool: /home/claude/selangor/tools/layers.py GROUP.csv. Reports: /home/claude/afternoon/L_YYYYMMDD.txt.
- Layers:
  - Background (< ~0.1°/day): outer planets, far bodies, Chiron, Transpluto, nodes, stars.
  - Middle (~0.2–2°/day): Sun, Mercury, Venus, Mars, Ceres, Pallas, Juno, Vesta.
  - Fast: the Moon and the fast points.
- New family **HALF** (n + 0.5°), tolerance 0.01 (Eddie: half the whole-number tolerance of 0.02).
- **CORRECTION, the Moon differs by course.** The engine's Moon is topocentric: at the same minute, Ascot, York and Newmarket differ by about 0.03° RA and 0.02° Dec, about 4 min of Moon motion. Moon events read from a STITCHED multi-course timeline are wrong by minutes. The fast layer now uses each race's own file.
  - **The "Moon as exact middle → fav won" count (7 W v 2 B) came from stitching and does not stand.** With each course's own Moon: W Ascot 16:00, Sedgefield 14:20 (×2), Kempton 14:40; B Haydock 14:20, Haydock 14:55 (×2), Sedgefield 14:55, Kempton 15:15. **3 W v 4 B races: no separation.**
  - Same caution for any Moon item in the group timelines (afternoon.py C/E). The Sun, planets and stars are identical across courses.
- **Background:**
  - 8 Jul: backbone Jupiter/Regulus 1300/9 (exact 18:16), Orcus/Rahu 18φ, Ketu/Rigel 6φ. **Bellatrix/Jupiter Dec 4.5 (half) exact 15:54**, the switch (York 15:50 finished 15:53:39; beaten before, won after).
  - 4 Sep: background pairs go exact through the afternoon: Regulus/Saturn 13:50, Orcus/Polaris 14:07, **Chiron/Jupiter 26φ 14:29:24 (the turn; Stratford 14:30 off 14:30:26)**, **Haumea/Jupiter 112.5 (half) 14:37:48**, Pluto/Quaoar 14:51, Aldebaran/Orcus 14:52, Ketu/Transpluto 15:52, Gonggong/Makemake 15:53.
  - 17 Oct: in the window Aldebaran/Haumea 14:24, Haumea/Uranus 14:27, Gonggong/Ketu 14:45, Ketu/Saturn 15:01, Pluto/Sirius 15:25, Altair/Rahu 15:29. **No Jupiter background pair exact, and no turn that day** (the results alternate).
  - **Seen so far: on the two days with a clear turn, a Jupiter background pair goes exact at the turn, one of them a half-degree number each day.**
- **Middle layer:**
  - Mercury makes 37 exacts on 8 Jul and 41 on 4 Sep, and is among the busiest middle bodies in the early beaten races (Thirsk 13:40, Ascot 14:00, Thirsk 14:15). On 17 Oct (standing still) it makes 7.
  - 8 Jul: Pallas and Venus are the busiest middle bodies all afternoon.
  - 4 Sep: Mars and Mercury early, then the Sun and Juno.
  - 17 Oct: the Sun early, then Ceres.
  - **8 Jul Sun: its silence 15:20–15:52 was only in the usual families. With halves it makes Eris 80.5 (15:21), Aldebaran 38.5 (15:28), Neptune Dec 25.5 (15:29) and Neptune RA 111.5 (15:30), then Quaoar 168.5 at 15:46 in the switch window.** 4 Sep: the Sun stays silent 14:03–14:37 even with halves.
  - Middle-layer half hits at the 8 Jul switch: Mars/Gonggong 21.5 (15:44), Juno/Mars 8.5 (15:45), Sun/Quaoar 168.5 (15:46), Venus/Arcturus 136.5 at the York 15:50 off, Pallas–nodes 164.5 / 15.5 at the York finish.
- **Fast layer:** the Moon makes a half number with some body in almost every race (1–5 per race), so a count does not separate. The fast points deliver race top-12 numbers often in every race; as Eddie said, they are not the heavy lifting.
- **Half-degree numbers are kept in their own pile** (Eddie, 5 Oct). They are removed from layers.py sections 1–3 (background list, middle-layer timeline and counts, Moon contacts and deliveries) and listed only in section 4, by layer: background held, middle exacts, Moon at race moments. Reason: they may matter more in the slower layers than the fast one, so they are read layer by layer and not mixed into the main counts.

## 21. Further digging on the three dates (5 Oct)
- **Which middle-layer body leads in the 10 min before the off through the finish** (non-half exacts with the background or each other; from layers.py section 2). Count per race; leader = most contacts:
  - **Mercury leads:** B York 15:15, Newmarket 15:35, Thirsk 13:40, Haydock 13:45 (tie with Mars), Ascot 14:00, Kempton 14:05, Thirsk 14:15, Haydock 14:20 = **8 B**; W York 15:50 (Mercury 7, Venus 5), Newmarket 16:10, Stratford 13:55, Kempton 15:15 (2021-09) = **4 W**.
  - **Venus leads:** W Ascot 16:00, York 16:25 (tie), Stratford 14:30 (tie with Mars), Ascot 14:35, Thirsk 15:25, Sedgefield 14:20 = **6 W**; B Kempton 14:40 (2021-09), Kempton 15:15 (2021-10) = **2 B**.
  - **The Sun leads:** W Thirsk 14:50, Stratford 15:05, Kempton 14:40 (2021-10); B Haydock 14:55 (Sun 9), Ascot 15:10, Kempton 14:05 (2021-10). Even.
- **Jupiter, layer to layer:**
  - 4 Sep: the background pair Chiron/Jupiter 26φ goes exact at 14:29:24, 1 min before the Stratford 14:30 off. It is that race's #1. **During the race the fast layer brings the same 26φ twice**: Vertex–Transpluto at +0.41 m and Part of Fortune–Mars at +2.91 m. Fav won (the first fav win after the turn).
  - 8 Jul: Venus/Jupiter Dec 20 at 15:30 (beaten stretch). Bellatrix/Jupiter Dec 4.5 (half) exact at 15:54 (the switch). The Moon makes Dec 4.5 with Rigel during Newmarket 15:35 (B), 15 min earlier.
  - 17 Oct: no Jupiter background exact. The Vertex is opposite Jupiter in RA 10 s into Sedgefield 14:20 (W). Fast points touch Jupiter around Sedgefield 15:30 (W). No turn that day.

## 22. Mars and Saturn on the three dates (5 Oct)
- **Mars:**
  - **4 Sep:** Mars is busiest in the beaten races up to 14:41. It makes 3 contacts in the run-up and race at Thirsk 13:40, Haydock 13:45 and Haydock 14:20 (all B), with #1 Makemake/Mars 170/9 exact during Haydock 14:20. Then 4 at Stratford 14:30 (W: Makemake 170/9, Castor 20√2, Procyon 1φ) and Procyon at Ascot 14:35 (W). **After 14:41 Mars goes nearly quiet** (0–1 per race).
  - **8 Jul:** a Mars burst 15:32–15:48: Algorab 111√2 and 27, Transpluto 1/9, and halves Quaoar 114.5, Gonggong 21.5, Juno 8.5, then Alkaid 24φ. It runs from Newmarket 15:35 (B) through the switch gap. Then Mars/Sun 77 (16:03) and Mars/Venus 29φ (16:08) in the winning stretch.
  - **Mars carries 110/9 at York on 8 Jul:** Mars/Makemake 110/9 at 15:11 (York 15:15, B, its #3); Mars/Pallas 110/9 during York 16:25 (W, its #3). Same course, same number, beaten first race to winning last race.
- **Saturn (background):**
  - 4 Sep: Regulus/Saturn 22√2 goes exact at 13:50 and is in the top 12 of the early races (#2–#8). **The fast points bring its number inside four beaten races:** Haydock 13:45 (Part of Fortune–Mars, during), Ascot 14:00 (Ascendant–Transpluto, during), Kempton 14:05 (Part of Fortune–Ketu, during), Thirsk 14:15 (Ascendant–Transpluto, 12 s before the off). After 14:20 it leaves the tops.
  - 8 Jul: Saturn is quiet. Backbone Deneb Algedi/Saturn conjunction (exact overnight); the only middle-layer exact is Ceres/Saturn at 16:48.
  - 17 Oct: Saturn is busiest of the background (Altair/Saturn 20√2, Ketu/Saturn, Jupiter/Saturn).
- **17 Oct, three bodies standing still:** **Saturn turned direct on 11 Oct, Jupiter turns direct on 18 Oct, and Mercury on 18–19 Oct (RA).** Plus Venus out of bounds. This is the day with no turn (the results alternate) and no Jupiter background exact. A Jupiter barely moving cannot carry a new number into exactness. By contrast, on 4 Sep and 8 Jul Jupiter was moving (retrograde 4 Sep; turning retrograde only on 29 Jul 2022).

## 23. Every body, race by race, over the three dates (bodystudy.py; 29 races: 15 fav beaten, 14 fav won)
- File: /home/claude/afternoon/bodies/bodystudy.txt (sent to Eddie). Per body and per race:
  - middle-layer exacts in the run-up (off −10 min to finish) and inside the race;
  - its pairs in the race top 12, and whether it is busiest;
  - its race-top-12 numbers delivered inside the race by the fast layer;
  - Moon–body numbers inside the race (own course file);
  - background exacts near the race;
  - stations within 20 days.
- **Leaning to the favourite BEATEN** (number of races, B of 15 / W of 14):
  - **Mercury in the race top 12: 10 / 4** (B: York 15:15, Ascot 15:25, Newmarket 15:35, Thirsk 13:40, Haydock 13:45, Ascot 14:00, Thirsk 14:15, Kempton 14:40, Ascot 15:10, Sedgefield 14:55; W: York 15:50, Ascot 16:00, Newmarket 16:10, Kempton 15:15). Its top-12 numbers are delivered inside the race 6 / 1; middle exacts in the run-up 14 / 9.
  - **A Moon pair in the race top 12: 7 / 2** (B: Ascot 15:25, Newmarket 15:35 #1, Thirsk 13:40, Ascot 14:00 #1 #2, Kempton 14:05 (Sep), Kempton 14:05 (Oct), Kempton 15:15 (Oct); W: Stratford 15:05, Kempton 14:40 (Oct)).
  - **Saturn's top-12 numbers delivered inside the race: 7 / 3** (B: Haydock 13:45, Ascot 14:00, Kempton 14:05 ×2 days, Thirsk 14:15, Sedgefield 14:55, Kempton 15:15).
  - **Makemake middle exacts in the run-up: 7 / 3.**
  - Juno numbers delivered inside the race 10 / 6; Rahu–Moon in the race 4 / 1; Vesta middle exacts inside the race 3 / 0 (Haydock 14:55, Ascot 15:10, Sedgefield 14:55); Mars busiest 4 / 2; Neptune in the top 12 10 / 7; Eris and Sedna run-up 4 / 1 each.
- **Leaning to the favourite WON:**
  - **Venus middle exacts inside the race: 7 / 4** (W: York 15:50, Ascot 16:00, Stratford 13:55, Stratford 14:30, Ascot 14:35, Kempton 15:15, Sedgefield 14:20); Venus busiest 2 / 0.
  - **Moon–Quaoar inside the race: 4 / 0** (Ascot 16:00, York 16:25, Stratford 15:05, Sedgefield 15:30).
  - **Moon–Chiron inside the race: 4 / 1**; Chiron busiest 2 / 0 and background exact near 2 / 0.
  - **Ketu (south node) pairs in the top 12: 8 / 5.** Ketu middle exacts in the run-up 5 / 2.
  - Orcus numbers delivered 6 / 3; Pluto numbers delivered 6 / 4; Moon–Orcus 4 / 2.
- No lean: the Sun, Ceres, Pallas, Gonggong, Transpluto, Haumea.
- **Stations:**
  - 17 Oct 2021: Mercury direct +2 d, Jupiter direct +1 d, Saturn direct −6 d, **Pluto direct −10 d**, Ceres retrograde −8 d. Four planets standing still on the day with no turn.
  - 8 Jul 2022: **Vesta turns retrograde that same day**; Neptune turned retrograde −10 d; Chiron +12 d; Juno +17 d.
  - 4 Sep 2021: Uranus retrograde −15 d.
- Caution: these are counts over 29 races on three days. They are leads to test on the next groups, not rules.

## 24. 18 Apr 2022 (Easter Monday): every race at 7 courses, 50 races, 37 favs beaten, 13 won (from Eddie's short-price list)
- Courses: Fakenham, Redcar, Kempton AW, Wolverhampton AW, Huntingdon, Chepstow, Plumpton. Reports: L_20220418.txt and bodies/bodystudy_0418.txt.
- Sequence by off:
  - **the first 11 all beaten (13:00–14:22)**
  - W Wolverhampton 14:26
  - 6 beaten (14:30–15:01)
  - W Huntingdon 15:05, W Chepstow 15:12, B Fakenham 15:20, W Redcar 15:26
  - B ×5, W Chepstow 15:47, B ×3
  - W Wolverhampton 16:12, W Huntingdon 16:16
  - B ×3
  - **W Plumpton 16:37, W Kempton 16:40**, B Wolverhampton 16:47, **W Huntingdon 16:50, W Chepstow 16:55**
  - B Redcar 17:13, W Plumpton 17:13, B ×5, W Plumpton 17:48, B Chepstow 18:01
- Day state:
  - The Moon is waning gibbous (elongation 204°), Dec −18.4, fast (14.4°/day).
  - **Ceres is out of bounds (Dec +25.5).** Out of bounds on the earlier days: 8 Jul Mercury and Ceres; 17 Oct Venus.
  - Jupiter is moving (+0.20°/day). Pluto turns retrograde in 11 days. Mercury is fast (1.7°/day): 85 middle-layer exacts.
- **Background:**
  - Bellatrix/Makemake 150/9 (#1 in most races, exact 17:18:58). Haumea/Spica 140/9 (exact 12:50, before racing). Regulus/Uranus, Chiron/Deneb Algedi, Deneb Algedi/Uranus, Makemake/Pleiades.
  - Busiest background bodies: Makemake, Transpluto, Uranus. No Jupiter background pair is exact today (Alphecca/Jupiter only at 23:00), and **no background half number.**
  - **The background pairs that go exact during racing, and the next off after each:**
    - Deneb Algedi/Uranus 46φ at 15:23:04 → Redcar 15:24 W (off 15:26:23, 3.3 min later; Fakenham 15:20 B was running).
    - Chiron/Deneb Algedi 400/9 at 16:08:53 → Wolverhampton 16:11 W (off 16:12:09, 3.3 min later).
    - Regulus/Uranus at 17:00:29 → 38 s after the Chepstow 16:55 W finish; the next offs are Redcar 17:13 B and Plumpton 17:13 W together.
    - Bellatrix/Makemake at 17:18:58 → during Plumpton 17:12 W; the next off is Wolverhampton 17:22 B.
    - **No background exact during the 11 beaten races at the start (13:00–14:22).**
- **The 3-day leads tested on this day** (share of the 37 B races v share of the 13 W races):
  - **Mercury in the race top 12: 57% v 54% — NOT confirmed.**
  - **A Moon pair in the top 12: 51% v 62% — NOT confirmed (reversed).**
  - **Venus exacts inside the race: 49% v 31% — reversed** (Venus led the winners on 8 Jul and 4 Sep).
  - Makemake in the run-up: 22% v 54% — reversed. Ketu in the top 12: 5 B v 0 W — reversed.
  - **Saturn holds:** Saturn pairs in the top 12 in 6 races, all B; its numbers delivered inside the race 6 B v 0 W; Moon–Saturn inside the race 11 B (30%) v 1 W (8%).
  - Moon–Quaoar inside the race 14% v 23% and Moon–Chiron 11% v 23%: the same direction as before (towards W), but weak.
  - Other B leans this day: Neptune in the top 12 (12 B v 1 W) and its numbers delivered 12 v 1; Pluto in the run-up 12 v 0; the Sun in the top 12 13 v 2; Orcus–Moon 13 v 2. W leans: Moon–Juno 8% v 31%, Moon–Mercury 14% v 31%.
- With 7 courses running every ~5 min, nearly every minute is inside some race, so "during a race" tags lose meaning on a day like this. The day-level and next-off reading is cleaner.

## 25. Five layers and five measures (layers5.py), from Eddie 5 Oct 2026
- **Layers:**
  - L1 FIXED: fixed stars plus the Equator (Dec 0, no RA).
  - L2 SLOW: Uranus, Neptune, Pluto, Chiron, Transpluto, Eris, Sedna, Makemake, Haumea, Gonggong, Quaoar, Orcus, the nodes.
  - L3 MEDIUM: Jupiter, Saturn, Mars, Ceres, Pallas, Juno, Vesta.
  - L4 FAST: the Sun, Mercury, Venus, the Moon.
  - L5 POINTS (separate container): Ascendant, Midheaven, Vertex, Part of Fortune, Part of Spirit.
- **Measures:**
  - RA and Dec, as before (the main lists).
  - **Flat** = √(RA² + Dec²), the RA difference taken the short way.
  - **Sky** = the true angle on the sphere.
  - **Dir** = the direction (position angle, north through east) of the faster body seen from the slower one, as a line 0–180.
  - Flat, Sky and Dir are kept in a separate "new measures" pile, and the halves in their own pile, until we see what they add.
  - Scoring: the same families and tolerances. Conjunction uses the RA tolerance (1°) for Flat and Sky and is not used for Dir. Equator pairs are Dec only.
- **Study tools only.** The ledger's own ranking (RA and Dec) is unchanged, so race top-12s stay comparable with all earlier work.
- Reports: /home/claude/afternoon/L5_YYYYMMDD.txt for 8 Jul 2022, 4 Sep 2021, 17 Oct 2021 and 18 Apr 2022.
- **First reading: Jupiter clusters at the turn, in every measure.**
  - **8 Jul 2022** (switch about 15:45–15:54): Transpluto/Saturn Sky 171.5 (half) at 15:49; Mars/Saturn Sky 42φ at 15:53 (during York 15:50 W); **Bellatrix/Jupiter Dec 4.5 (half) at 15:54, then Bellatrix/Jupiter Sky 52√2 at 15:58**; Capella/Jupiter Dir 700/9 at 16:21. Also Alkaid/Pallas Sky φ¹⁰ at 15:43.
  - **4 Sep 2021** (turn about 14:25–14:30): **Deneb Algedi/Jupiter Dir 18√2 at 14:24; Chiron/Jupiter RA 26φ at 14:29 (1 min before the Stratford 14:30 off); Jupiter/Pallas Sky 16φ at 14:33 (during Stratford 14:30 W); Haumea/Jupiter RA 112.5 (half) at 14:37.** Four Jupiter contacts in 13 minutes, in four different measures.
  - **17 Oct 2021** (no turn; Jupiter turning direct): only Ketu/Jupiter RA at the Kempton 14:05 finish (B), Jupiter/Sun RA 122.5 (half) at 13:43, Jupiter/Mercury Flat 84φ at 14:11, Jupiter/Mars Sky 121 at 15:36.
  - **18 Apr 2022** (mostly losing; Jupiter moving at 0.2°/day): Jupiter is busy all day (10 RA exacts plus many new-measure ones), including **Neptune/Jupiter RA 1° at the Fakenham 13:35 off** (B). This is the Jupiter–Neptune conjunction of April 2022. With Jupiter this busy all day, a Jupiter cluster can't mark a turn on this day.

## 26. Portal scan (portal.py): an opening through the layers at the race? (5 Oct 2026)
- Eddie's idea: a portal or opening through the layers gives an outsider an energy kick.
- Two definitions, scanned at every race on the four days (79 races: **17 outsider wins (winner 8/1+), 35 mid-price wins over the fav, 27 fav wins**). Reports: /home/claude/afternoon/P_YYYYMMDD.txt.
  - **A) Number thread.** One number (×10 the same) in 3+ of the layers fixed/slow/medium/fast, landed by the Moon in the race (off −1 to finish +1). Layers: slow holds ≥97 at the off; medium and Sun/Mercury/Venus exacts from off −30 min; the Moon from the race's own file. All five measures. (Threads that only reach 3 layers through the fast points are counted separately; they are in every race, 2–18 each.)
  - **B) Line.** A medium body on the great circle through a slow/fixed body and a fast body: a real crossing in the window, or a Moon line closest inside the window within 0.05°. "+4" = a body from a fourth layer within 0.1° of the same circle.
- **What we see:**
  - **A) Moon-landed threads are rare: 7 in 79 races** (OUT 2/17, MID 2/35, FAV 3/27). No lean to outsiders.
    - Newmarket 15:35 (Prosperous Voyage 16/1, Inspiral beaten): Antares/Neptune Flat 1000/9 held → Transpluto/Mars Dec 1/9 at 15:36 → Arcturus/Moon RA 1/9, 1.8 min after the finish.
    - Fakenham 13:00 (Royal Plaza 9/1): Vega/Orcus Flat 133.33 held → Ketu/Pallas Dir 1200/9 at 12:56 → Ketu/Moon Sky 12/9 during the race (+2.6 m).
    - York 15:50 (fav won): Procyon/Pluto Sky 161.80 held → Ketu/Pallas Dec 10φ (15:28) → Spica/Moon Dec 1φ 3 min after the finish.
    - Plumpton 17:47 (fav won): Algorab/Chiron Flat 177.81 held → Gonggong/Vesta Sky 160/9 (17:44) → Rahu/Moon RA 1600/9 during.
    - **18 Apr 16:16–16:34, one thread through three races in a row:** Algol/Quaoar and Pleiades/Makemake hold 141.43 (= 100√2) → Sirius/Vesta goes exact on 100√2 at 16:19–16:20 → the Moon lands 100√2 with Betelgeuse during Huntingdon 16:15 (**fav won**) and Chepstow 16:17 (fav beaten by 6/4), and with Rigel during Fakenham 16:30 (fav beaten by 100/30).
  - **B) Lines are rare: 4 races, none of them an outsider win.** Rigel – Pallas – Moon during Kempton 15:15 (Oct; mid); Castor – Mars – Moon during Sedgefield 15:30 (fav won); and **Pleiades – Pallas – Moon with Ketu and Rahu on the same circle (a four-layer line: fixed, slow, medium, fast) at 16:21–16:22, during Huntingdon 16:15 (fav won) and Chepstow 16:17 (mid).** That is the same moment as the 100√2 thread.
  - **The strongest "opening" found (18 Apr 16:19–16:22: a number thread through three layers plus a four-layer line) came during a favourite's win and a mid-price win, not an outsider.**
- **So as defined, a portal through the layers does not single out the outsider races.** The 17 outsider wins have no lines and only 2 Moon-landed threads. The next step is to read the outsider races one by one, in full, for what IS there.

## 27. Two stars — 8 Jul 2022 (twostars.py, S2_20220708.txt)
Question: does a moving body sit in a scoring relationship with two fixed stars at once — equal distance (a kind of midpoint), a ratio (φ, φ², φ³, √2, 2, 1+√2, 3), on a line between/beyond them, or scoring with both within a minute? Measured in Flat and Sky. Direction is now the line's orientation on the chart, 0–180°, the same from either end (also changed in layers5.py and portal.py).

What was seen:
- Slow: the only slow shape inside the racing window is Orcus, Vega = (1+√2) × Sirius (Flat) at 15:46:44 — inside the 15:44–15:54 switch.
- Inspiral's race (Newmarket 15:35, 1/7F beaten): Venus Alphecca = 2 × Polaris (Flat) 15:39:36 and Mars Arcturus = 2 × Sirius (Sky) 15:40:00, both during the race; Sun Alkaid = φ³ × Procyon at the finish 15:41:06. The only race with medium + fast two-star shapes during the running.
- Moon equally far from Deneb Algedi and Sirius twice: Flat 16:07:55 (4½ min before Newmarket 16:10 off, W) and Sky 16:25:24 (28 s before York 16:25 off, W).
- Sun Algorab = 2 × Regulus (Sky) 16:12:19, 9 s before the Newmarket 16:10 off (W).
- Moon "both" clusters: heavy at Ascot 16:00 W (15, mostly during the race), York 16:25 W (15, all before the off), Newmarket 16:10 W (6); light at the beaten races York 15:15 (3), Ascot 15:25 (4), Newmarket 15:35 (2). York 15:50 W has none — only ratios.
- One Moon line all afternoon: Fomalhaut–Moon–Spica (between), 16:03:46, after the Ascot 16:00 finish.
Caution: the Moon's cluster density depends partly on how many stars happen to sit at number distances as it passes; one day only.

## 28. Two references incl. slower bodies — 8 Jul 2022 (twobodies.py, B2_20220708.txt)
Option (a): references = fixed stars + bodies slower than the mover (medium → stars+slow; Sun/Mercury/Venus → +medium; Moon → +Sun/Mercury/Venus). Tagged [star+star] / [star+body] / [body+body]. Rahu/Ketu pair skipped.
What was seen:
- Two midpoints echo each other: Moon equidistant Deneb Algedi/Sirius (Flat 16:07:55, Sky 16:25:24) and Venus equidistant Algorab/Saturn (Sky 16:09:04, Flat 16:24:29) — both pairs land before Newmarket 16:10 W and York 16:25 W, with the measures swapped.
- York 16:25 W: Mars Haumea = φ × Pluto 15 s before the off; during, Pallas Haumea = φ × Polaris and Ceres Algorab = 2 × Transpluto (1 s apart).
- York 15:50 W: Sun Spica = 2 × Sedna 47 s before the off; Mercury Alphecca = φ × Chiron at the finish. Moon during: Eris = 3 × Orcus, Alkaid = φ³ × Ketu, equidistant Betelgeuse/Vesta.
- York 15:15 B: Mercury Vesta = φ³ × Aldebaran 2 s before the off; Moon on the line Spica–Pluto (between) 25 s before the off. The same Moon line comes at Ascot 15:25 B 2 min before its off (later at Ascot — parallax).
- Ascot 15:25 B (22/1 winner): with bodies added it has the busiest during-race Moon chain of the beaten races — 11 events in the first minute, Regulus, Spica, Rahu, Mercury, Sedna chaining; then Transpluto = φ³ × Ketu and equidistant Alkaid/Quaoar near the finish.
- Newmarket 15:35 B (Inspiral): Moon during Makemake = φ² × Ketu and Vega = √2 × Orcus at 15:40:02–03, the same moment as Mars Arcturus = 2 × Sirius (15:40:00).
- Ascot 16:00 W: Moon during — equidistant Rigel/Juno, Uranus and Orcus join the star chain, Juno = φ³ × Arcturus.
- Newmarket 16:10 W: Moon on the line Neptune–Eris 1 min before the off; Moon Sun = φ³ × Algorab during.
- With bodies added the light/heavy Moon split between beaten and winning races from §27 no longer holds (non star+star totals: 22, 32, 16 beaten; 13, 20, 38, 30 won).
- Ketu turns up as the short leg of Moon ratios in 4 races (Ascot 15:25, Newmarket 15:35, York 15:50, Ascot 16:00) — it sits ~15° from the Moon all afternoon.

## 29. Option (b): any body against any two others — 8 Jul 2022 (twoall.py, BB_20220708.txt)
Only what is new beyond (a): pairs where a reference is as fast as or faster than the mover; the Moon as a reference read per race (own file). "Both" no longer counts a number between two slow bodies/stars (they are held, nothing lands) or Rahu–Ketu.
What was seen:
- Triangles that close: Aldebaran sits at the midpoint of Sun–Mars (Flat) at 15:31 — Sun: Mars = 2 × Aldebaran and Mars: Sun = 2 × Aldebaran, both 38.959°, 7 min before Inspiral's off. Venus equally far from Rigel and the Sun (30.080°) at 16:33, with Jupiter = (1+√2) × both — after racing.
- Inspiral's race (Newmarket 15:35 B): Eris Castor = φ × Venus 23 s before the off; Eris Mercury = φ² × Rahu during; Gonggong Regulus = √2 × Mercury at the finish 15:41:06, the same second as Sun Alkaid = φ³ × Procyon (§27).
- Ascot 15:25 B (22/1): Jupiter Transpluto = φ² × Pallas 2 s after the off (repeats with Haumea at 15:34).
- The two early beaten races (York 15:15, Ascot 15:25) both get two Moon lines before the off: Vega–Uranus–Moon (Uranus between) and Spica–Pluto–Moon; ~4 and ~0.5–2 min before.
- Ketu with the Moon as reference appears only at the three beaten races: Algorab = φ² × Moon (York 15:15; and 2 s after Inspiral's off), Alphecca = 3 × Moon (Ascot 15:25), Haumea = (1+√2) × Moon (Newmarket 15:35). None at the four fav wins.
- Newmarket 16:10 W: Uranus Moon = 2 × Deneb Algedi and = φ × Altair at 16:07:43–55, the same moment as the Moon's Deneb Algedi/Sirius midpoint; Neptune–Eris–Moon line 1 min before the off.
- York 16:25 W: during, Transpluto Capella = √2 × Mercury and Sedna Sun = √2 × Eris; at the finish Transpluto Algol = (1+√2) × Ceres. Pluto has Mercury 164 and Moon 61√2 2 min before the off.
- Same event at two courses (Moon parallax): Makemake Sirius = φ² × Moon after the York 15:50 finish and 4½ min before the Ascot 16:00 off.

## 30. 4 Sep 2021 — sky and runners together (runners2.py; R2_20210904_haydock_1420.txt, R2_20210904_kempton_aw_1440.txt; sky S2/B2/BB_20210904.txt)
runners2.py: per race, own minute file, off−10 to finish+1. Each runner's noon natal charts (horse H., jockey J.; natal Moon left out, ~ = natal place moves >0.1° across the birth day) added as references. A = a transit mover with a natal point as one of its two references; B = a natal point as the centre between two transit bodies (or a body and a star). ONLY = no other runner has the same shape.
What was seen:
- Volume does not separate runners: every runner gets 190–290 shapes, ~100–130 ONLY, 13–34 ONLY during. Haydock: Golden Flame (W) 27 during, Valley Forge (fav, 3rd) 34 — the most. Kempton: Hamish (W) 13 — the fewest; Prince Of Arran (last) 30.
- Sky story, Haydock 14:20: Mercury Rahu = φ³ × Makemake during (+0.8m); Moon Ketu = 3 × Orcus and Rigel = φ × Orcus (+0.95–1.0m); Moon Uranus = φ × Mercury (+2.9m); option b: Mercury equally far from Alkaid and the Moon (+2.7m), Sun Arcturus = φ × Moon (+2.8m). #1 Makemake/Mars exact +2.45m.
- Golden Flame / Joe Fanning: the jockey's natal Makemake is equally far from transit Mars and Alkaid 51 s before the off, and has Uranus = φ × Mercury 32 s before — the race's #1 pair (Makemake/Mars) and its busiest body (Mercury) meet on the jockey's Makemake just before the off. During: horse's natal Orcus has Rigel = 3 × Mars (+1.44m), 26 s after the sky's Moon Rigel = φ × Orcus; Moon H.Makemake = φ² × J.Orcus (+1.31m, horse×jockey).
- Valley Forge (fav): the Moon joins horse Makemake and jockey Makemake (φ, +1.0m) and horse Makemake has Moon = 2 × Mercury (+0.8m) — Makemake too, but by the Moon during the race, not Mars/Mercury before it.
- Sky story, Kempton 14:40: Pallas Bellatrix = φ × Pluto during; Mars equally far from Arcturus and the Moon (+1.9m) — the Arcturus/Mars pair (#12) at the off; Sun quiet until 14:26.
- Hamish / Pat Dobbs: the Sun equally far from the horse's natal Transpluto and transit Mars (Flat 11.116°, +0.76m); the jockey's Mars is the centre for Sun = 3 × Moon and Transpluto = (1+√2) × Moon just before the off; Moon H.Mars = 2 × J.Jupiter 15 s before the off.
- Hukum (30/100, 2nd): it is the fav whose natal joins the Arcturus/Mars theme — jockey Mars has Arcturus = (1+√2) × Mercury (+1.5m), jockey Jupiter Arcturus = φ³ × Moon (+2.2m); Moon equally far from horse Pluto and horse Gonggong 16 s before the off.
- Caution: with ~100 references per runner most of this is chance; the lines above are the ones that tie to the race's own sky story.

## 31. 4 Sep 2021 all in — runners3.py (R3_*.txt story reports, R3_*_full.txt everything; hay_story.txt / kem_story.txt = ONLY + exact natal + top-12 pair or the 3 busiest bodies, off−3 to finish+1)
Added: EQUAL/RATIO in RA, Dec, Flat and Sky; direction 0–180 scored as a number (Dir); parallel lines (transit→natal line or horse–jockey natal line parallel to a top-12 sky pair line); half numbers kept apart; single exact numbers transit→natal; strongest ledger contacts (≥95 at the off) joined.
Counts still don't separate (each runner 835–1400 shapes, 560–860 ONLY). Busiest for the tight filter: Haydock Mercury, Mars, Neptune; Kempton Mars, Transpluto, Chiron.
What was seen — Haydock 14:20 (top pair Makemake/Mars Dec 170/9; busiest Mercury, Mars):
- Golden Flame / Joe Fanning (W 9/1): the #1 pair lands on both of its charts before the off — the line Mars→horse Makemake runs at direction 47 (14:17:54), then the jockey's Makemake is equally far from Mars and Alkaid (14:19:30). Mercury then binds the jockey's Makemake (Uranus = φ × Mercury, 14:19:49) and horse Neptune / jockey Transpluto (= 3×, 14:18:17, echo of top pair Neptune/Transpluto). During: Mars has horse Quaoar = φ × Haumea in Dec (14:22:17); Mercury has horse Pluto = √2 × horse Ketu in Dec (14:23:02). At the finish the jockey's Chiron is the Dec midpoint of Mercury and Uranus.
- Only Golden Flame has Makemake/Mars on both horse and jockey before the off (Roseabad horse Makemake Dir 45 once; Praiano and Contact get it during the race).
- Valley Forge / David Probert (fav 11/8, 3rd): the most story lines (37), Mercury-heavy. A Mercury burst on the jockey's chart during the race, 14:21:22–14:21:53: Mercury makes Sky 45 with jockey Transpluto, RA 40√2 with jockey Orcus, RA 12/9 with jockey Haumea, then RA 167 with transit Neptune — four numbers in 30 s. Strongest ledger: horse Rahu ← Vega Dec 13φ 100.0, horse Makemake ← Pallas 99.9.
What was seen — Kempton 14:40 (top pairs Pluto/Quaoar, Mars/Mercury RA 12 exact 14:40:35; busiest Mars, Transpluto, Chiron):
- Hamish / Pat Dobbs (W 9/1): Mars + Transpluto on the horse's natal Transpluto. Mars–Moon Sky 26φ at 14:38:15 sets off four number pairs on Hamish (horse Transpluto Flat 200/9, horse Haumea, jockey Jupiter, jockey Sedna Dir); Mars–horse Transpluto Flat 200/9 (14:38:58); horse Transpluto has Saturn = 3 × Moon in Dec (14:40:05, echo of top pair Saturn/Transpluto); jockey Transpluto has Alphecca = φ² × Mars; horse Chiron is the Dec midpoint of Venus and Mars at 14:40:35 (= the moment Mars/Mercury goes exact); during, the Sun is equally far from horse Transpluto and Mars (14:41:53). Ledger: jockey Uranus ← transit Uranus RA 1600/9 99.8 (its own body back), only.
- Hukum (30/100, 2nd): Mars → horse Makemake Dir 18(1+√2) at the same Mars–Moon 26φ moment; during, Mars ties jockey Uranus and jockey Neptune to Transpluto (RA, 14:41:21 and 14:41:46); Sun/Venus top pair on horse Rahu and jockey Transpluto.
- The Mars/Mercury RA 12 exact moment (14:40:35) lands on Prince Of Arran (last) three times (horse Sedna, horse Gonggong, jockey Gonggong) and on Hamish's horse Chiron.
- Both winners: the race's #1 or busiest bodies reach a slow natal point of the winner before the off (Golden Flame Makemake ← Mars; Hamish Transpluto ← Mars), and the same point is touched again during the race or at the finish. Both favourites: a busiest body works on the jockey's chart during the race (Valley Forge Mercury burst; Hukum Mars on jockey Uranus/Neptune).

## 32. Blank sheet STEP 1 — Contact with the Fixed layer, 4 Sep 2021 (fixed1.py; afternoon/fixed/F1_20210904_haydock_1420.txt, F1_20210904_kempton_aw_1440.txt)
Order per star row: 1a transit (exact moments off−10 to finish+1, own minute file; held ≥90 at the off with A/S; the same star across the afternoon), 1b horse, 1c jockey (midday chart, natal-natal = star at birth, transit-natal = star on race day, A/S, EXACT yyyy = crossed since birth).
What was seen:
- Arcturus and Spica are the stars the fast/medium bodies keep switching on through the beaten-favourite stretch: Arcturus — Sun 14:11 (Kempton 14:05 B), Venus RA 120/9 DURING Haydock 14:20 (+0.34m), Mercury RA 28 and Mars RA 40 two seconds apart 30 s before the Kempton 14:40 off, Venus DURING Ascot 15:10 B — every non-Moon Arcturus contact of the afternoon falls at a beaten-fav race. Spica — Mercury 14:10 (Kempton 14:05 B) and 14:15 (Thirsk 14:15 B), **Mars DURING Haydock 14:20 (Sky 31, +1.28m) and Mars 5 s before the Kempton 14:40 off (Flat 22√2)**; later only fast bodies (Mercury Kempton 15:15 W, Sun and Venus Thirsk 15:25 W).
- Pleiades: non-Moon contacts only at Stratford 13:55 W and 15:05 W (Mercury, Mars, Sun). The Moon is on the Pleiades during both outsider races (Haydock +1.20m Flat 48φ and Sky 50√2 at the finish; Kempton 16 s before and 14 s after the off).
- Kempton: the Moon makes three numbers with Procyon during the race (+1.9–2.4m, Dec 16, RA 14√2, Flat 18√2); Venus and the Moon on Sirius during; Mars–Rigel Flat 96 during; Ketu–Rigel and Rahu–Deneb Algedi before the off (the only node–star exacts at either race).
- Haydock natal: Joe Fanning (Golden Flame, W) plugs into three stars switched on during/at the finish — natal Juno on the Pleiades (RA conjunction, exact at his birth, 99.7 now, separating) while the Moon hits the Pleiades during and at the finish; natal Juno–Spica Sky 144.448 (99.6) while Mars hits Spica during; natal Orcus–Castor RA 14/9 (went exact 2020) while Mars hits Castor 9 s after the finish. Ray Dawson (Contact, 4th) also plugs into three (Arcturus, Spica, Deneb Algedi). Valley Forge (fav): horse Juno–Algorab Dec 160/9 (Moon on Algorab during).
- Kempton natal: Hukum (fav) horse Ceres–Arcturus Flat 1500/9 (99.8) — the star Mercury and Mars hit together before the off. Hamish (W): horse Transpluto–Regulus Sky 11/9 (99.2, applying) — the Moon hits Regulus 1.6 min before the off. Fox Tal (3rd) twice on Spica.
- Caution: "went exact since birth" is common (≈35–55 per chart at ≥97) — the star drift since birth passes many targets, so by itself it says little.

## 33. Blank sheet STEP 2 — Contact with the Nodes layer, 4 Sep 2021 (nodes2.py; afternoon/fixed/N2_*.txt)
Rows: transit Rahu and Ketu (2a transit L2/L3/L4/Moon, 2b horse natal, 2c jockey natal, natal lists ≥90, "exact in/ago" in days at the node's rate), then each runner's own natal Rahu/Ketu (transit bodies onto them; natal-natal). Rahu–Ketu skipped in RA only.
What was seen:
- **Mars–Rahu in √2 at both outsider races, before the off:** RA 78√2 at 14:16:11 (Haydock, −4.2 min) and Sky 76√2 at 14:39:45 (Kempton, −1.4 min); then Flat 79√2 at 14:46:47 after Kempton. All three Mars–node contacts of the afternoon are √2 and all fall in the beaten-fav stretch (Thirsk 14:15 B, Haydock 14:20 B, Kempton 14:40 B).
- Moon–Ketu Sky 81√2 during Haydock at 14:21:38 — the same second as Mars–Spica Sky 31 (step 1).
- Kempton: Moon–Rahu 71 (Flat and RA; Ketu RA 109) 2 min before the off; Venus–Rahu RA 137 / Ketu RA 43 at −3.9 min; Moon conjunct Rahu in Dec 19 s after the finish.
- Runners' own nodes: **neither winner's own nodes are touched during the race.** Golden Flame's are touched only before the off (Sun RA 10φ², Moon Dec 3φ and Flat 50/9 on horse Rahu, 4–8 min before; Mercury Sky 146/34 and Venus RA 95√2 on Joe Fanning's nodes, 3–6 min before). Hamish: Vesta Flat 21√2 and Moon Flat 30√2 on horse Rahu ten seconds apart, 2.3–2.4 min before the off. At Kempton all four beaten runners have a contact on their own nodes during the race (Hukum's jockey Moon RA 45/135 +1.9m; Fox Tal's jockey Venus Sky 5/175 +2.1m; Outbox Venus/Mercury/Ceres; Prince Of Arran's jockey Moon and Mars). At Haydock: Valley Forge (fav) horse Ketu Mercury Sky 76φ +2.9m and jockey Ketu Moon +1.3m; Contact's jockey nodes Sun Sky 89/91 +0.3m; Roseabad's jockey Rahu Venus +1.7m; Praiano and Tynwald none.
- Hukum (fav): the Moon makes Sky 9(1+√2) with the horse's natal Rahu 4 s before the off.
- Natal on transit nodes: Pat Dobbs J.Vesta–transit Rahu RA 1600/9 (99.8); Hamish horse Gonggong–transit Ketu RA 38(1+√2) (98.8, applying); Hamish's own nodes Sky 66φ from the transit nodes.
- **Body + family (Eddie: "important possibly — worth noting body and family").** Tally of all non-Moon exact contacts with the Fixed and Nodes layers across 4 Sep afternoon, by the nearest race (B = fav beaten, W = fav won): Mars Whole Number B6 W0; Mars √2 B5 W4 overall (but its three node contacts all B); Mercury Silver Ratio B4 W0; Mercury √2 B2 W6; Venus Whole Number B1 W6; Vesta Whole Number B4 W1; Ceres W only (Whole 3, Golden 1); Sun spread evenly. One afternoon only — to be kept as a running body×family tally as the layers and days go on.
- Eddie: **√2 is discord in musical harmony** — √2 = 2^(6/12), the tritone (half an octave, "diabolus in musica"). Mars–Rahu in √2 three times, all in the beaten-favourite stretch. Families to be read with their musical character in mind: whole-number ratios consonant (2 octave, 3/2 fifth), √2 the tritone.

## 34. Blank sheet STEP 3 — Contact with the L2 slow layer, 4 Sep 2021 (slow3.py; afternoon/fixed/S3_*.txt)
Rows: each transit slow body (3a: other slow bodies held, L3/L4/Moon exact; 3b horse; 3c jockey ≥90 with days to exact), then each runner's own natal slow bodies (transit onto them; natal-natal ≥97), then a body × family tally.
What was seen:
- Haydock during the race: **Mercury–Neptune 167 twice (RA +1.72m, Flat +2.39m)**; Mars–Makemake Dec 170/9 (+2.47m, the race's #1 pair); the Moon on Sedna (Dec 13), Chiron (Sky 119), Eris (Sky 107), Gonggong (Flat 114√2).
- **A Neptune thread on the Haydock winner:** Golden Flame's natal Neptune sits exactly Silver Ratio from transit Pluto (Sky 20(1+√2), 100.0 — the only 100.0 on the slow rows at that race), and the Moon hits the horse's Neptune during the race (Flat 153, +2.27m), while transit Mercury–Neptune makes 167 during. Also Jupiter → horse Gonggong Sky 5φ 10 s after the off (Jupiter's only contact on any runner's slow bodies there); Ceres → Joe Fanning's Quaoar RA 142 and Venus → his Sedna during.
- Valley Forge (fav): jockey David Probert's Transpluto, Haumea and Orcus all hit by Mercury during the race (the Mercury burst seen in §31 — now on his slow bodies).
- Kempton during the race: Ceres–Chiron RA 41√2 (+0.72m, the #5 pair); the Moon on Neptune (Flat 144, Flat 89φ) and Gonggong (RA 158).
- Hamish: the Moon works the horse's slow bodies through the first two minutes — Sedna Dec 14 (+0.19m) and Flat 81 (+0.31m), Makemake RA 37φ (+0.23m) and Flat 60 (+0.91m), Uranus Sky 114 (+0.62m), Transpluto RA 13√2 (+1.91m) — four of six whole numbers. Pat Dobbs's natal Uranus is 1600/9 in RA from transit Uranus (99.8, applying). Horse Pallas–transit Haumea RA 86 (99.3, applying). Not unique: Hukum's jockey Jim Crowley also gets 6 during (Moon ×5, Venus, Sun).
- The Moon hits a slow body with one number first in RA, then in Flat Dist a few minutes later (Makemake 26(1+√2), Haumea 57√2, Quaoar 89φ/144, Orcus 39 and 24φ) — the Moon closing in RA first.
- Tally note: Moon events seen from two courses are counted twice in the afternoon tally (parallax) — to be de-duplicated. Non-Moon: Mercury–Neptune Whole Number B2 W0 (the Haydock 167 pair); Sun Whole/√2 lean W; nothing else one-sided with 2+.

## 35. Blank sheet STEP 4 — Contact with the L3 medium layer, 4 Sep 2021 (medium4.py; afternoon/fixed/M4_*.txt). Moon events seen from two courses now counted once in the tally.
What was seen:
- **Mars changes partners with the switch.** Every Mars contact with another medium or fast body before 14:50 falls at a beaten-fav race: Jupiter Dec φ⁶ (Thirsk 13:40 B), Pallas Dec 1+√2 (Thirsk 13:40 B), Jupiter Sky 152 six seconds before the Haydock 13:45 off (B), **Mercury Flat 10√2 (13:48) and Sky 10√2 (14:04, Kempton 14:05 B) — the same √2 number in two measures** — and Mercury RA 12 thirty seconds before the Kempton 14:40 off (B). After the switch: Sun Flat 100/9 (Stratford 15:05 W), Jupiter RA 95φ (Thirsk 15:25 W). Mercury–Mars √2: B2 W0.
- **Saturn is touched only at fav-won races** (3 of 3): Vesta Sky 75√2 during Stratford 13:55 W, Sun Sky 103√2 six seconds before the Stratford 15:05 off W, Venus Sky 65φ before Kempton 15:15 W.
- Tally (non-Moon, medium rows): Sun Whole Number B3 W0, Mercury √2 B3 W0; Moon Silver Ratio B5 W0, Moon Golden Ratio B6 W2, Moon Whole/√2 lean W (9/9 v 5/4).
- Haydock during: Venus–Pallas RA 148 (+0.31m), Moon–Jupiter Dec 22φ (+1.92m). Kempton before the off: Jupiter–Pallas Sky 16φ (−7.9m), Moon–Mars Sky 26φ (−2.9m, the moment that hit four of Hamish's points), Mercury–Mars RA 12 (−0.55m).
- **Joe Fanning's natal Jupiter is worked through the race:** transit Juno Dec φ³ 34 s before the off (99.7), then Vesta RA 120/9 (+1.6m), Venus RA 9φ (+2.3m), Sun Flat 500/9 (+3.0m); his natal Vesta gets Venus and the Moon during and transit Vesta at the finish. Transit Jupiter → Golden Flame's Gonggong Sky 5φ (99.9, 10 s after the off) and → Joe Fanning's Orcus RA 144.441 (99.7).
- Hamish: transit Juno on three of the horse's points (Mercury Silver 99.3, Saturn 110/9 99.0 applying, Vesta 78φ); Mars → horse Transpluto Flat 200/9 again; Moon on the horse's Jupiter (Flat 42), Saturn and Mars. Pat Dobbs's natal Saturn: Venus Dec 16√2 during, Sun Flat 14 at the finish.

## 36. Blank sheet STEP 5 — Contact with the L4 fast layer, 4 Sep 2021 (fast5.py; afternoon/fixed/L4_*.txt). Pairs among Sun, Mercury, Venus, Moon each once; runners' own natal Sun/Mercury/Venus.
What was seen:
- **Moon–Mercury: no contact at all through the beaten stretch; all of them come after the switch, at fav-won races** — Flat 57 during Thirsk 14:50 W, Sky 56 at the Stratford 15:05 off W, Dec 25 and RA 36√2 after Thirsk 15:25 W.
- **Sun–Moon: nothing from 14:06 to 14:42 except Dec 10√2 during Kempton 14:40 B** (+1.62m) — √2 again in the beaten stretch. Sun–Venus Dec 10φ goes exact at 14:51 (2 min before Thirsk 14:50 W) — the pair that was the Kempton #10 held at 97.9 applying.
- Haydock 14:20: no exact among Sun, Mercury, Venus and the Moon anywhere in its window — the fast layer is silent at that race.
- Moon–Venus whole numbers B2 W0 (73 at Thirsk 13:40 B, 66 before Kempton 14:40 B); Moon–Mercury whole numbers B0 W3.
- **Winners' own Sun/Mercury/Venus are touched only before the off** (as with their nodes in step 2): Golden Flame's Mercury (Moon Flat 108φ, −1.4m) and Venus (Moon Sky 122√2, −3.0m), Joe Fanning's Mercury (Moon Sky 21φ, −0.5m); Hamish's Mercury (Moon Dec 26φ −2.65m, Flat 161 −0.58m) and Venus (Moon Flat 110√2 −2.6m, Flat 1400/9 −1.7m). Every other Haydock runner has a contact on its natal Sun/Mercury/Venus during the race or at the finish. At Kempton, Hamish's jockey Pat Dobbs has one during (Moon–natal Sun Dec 26√2, +1.05m); Hukum, Outbox and Prince Of Arran have them during too.
- 26φ recurs at Kempton: Moon–Mars Sky 26φ (14:38:15) and Moon–Hamish's Mercury Dec 26φ (14:38:29), with Hamish's Venus hit by the Moon one second later.

## 37. 6 Apr 2022 — the biggest outsider (Catterick 14:40 Wotever Next 33/1, fav Beluga Gold 2/5 2nd) and Lingfield 14:25 (Man On A Mission 12/1, fav 13/8 2nd); all five layers (afternoon/l0406/F1, N2, S3, M4, L4_*.txt). Group: 15 races Catterick/Nottingham/Lingfield 13:00–16:00, favs beaten in 11 (incl. Giant Steps 33/1 at Catterick 13:00, Gold Ring 22/1 at 14:05); favs win only Lingfield 13:55, Nottingham 15:25, Catterick 15:50, Nottingham 16:00 — the switch comes late (~15:25).
Checking the 4 Sep threads:
- **Mars in √2 just before the outsider — HOLDS:** Mars–Pallas Flat 41√2 at 14:39:32, 37 s before the Catterick off (4 Sep: Mars–Rahu √2 before both outsiders).
- **Sun–Moon in √2 during the outsider race — HOLDS:** RA 43√2 (+0.17m) and Sky 43√2 (+0.34m) during Catterick (4 Sep: Sun–Moon Dec 10√2 during Kempton, the only Sun–Moon number in 36 min).
- **Pleiades switched on at the outsider — HOLDS:** Moon Dec 3/9 41 s before the Catterick off, Sun Flat 28φ during (+1.31m); Lingfield: Moon–Pleiades 19 (Flat and RA) 2.4–2.9 min before the off.
- **Mars moves to Jupiter after the switch, at a fav-won race — HOLDS:** Mars–Jupiter Sky φ⁷ at the Catterick 15:50 off (W, 0.0 min); Mars–Ceres before Nottingham 16:00 W (4 Sep: Mars–Jupiter RA 95φ after Thirsk 15:25 W). Before the switch every Mars contact is at a beaten race (Saturn, Mercury, Pallas, Venus, Juno, Vesta).
- Arcturus and Spica active through the beaten stretch — mostly holds (Arcturus non-Moon B6 before the first W at 15:23; Spica all B until after 16:00) — but most races that day were B.
- **Winners' nodes untouched during — FAILS:** Venus hits both winners' natal nodes in √2 within a second of the off — Venus–Wotever Next's Ketu RA 27√2 (+0.01m), Venus–Luke Morris's Rahu Sky 9√2 (+0.02m); the Moon then hits Joanna Mason's Rahu (Mercury RA 37φ +1.2m), Man On A Mission's Rahu and Luke Morris's Ketu during.
- **Saturn only at fav-won races — FAILS** (Saturn's contacts here are at beaten races: Mercury, Mars, Juno). **Moon–Mercury only W — FAILS** (Moon–Mercury √2 B4 W0).
New:
- **√2 is everywhere on the beaten side:** Moon on the fast layer √2 B9 W0; Lingfield 14:25 fast layer all √2 (Moon–Mercury Flat 42√2 −5.5m and Dec 12√2 during; Moon–Venus RA 73√2 −5.9m and Dec 25√2 at the finish).
- **Luke Morris (Lingfield winner's jockey): transit Orcus goes exact on his natal Sedna during the race — Dec 11√2, 100.0, +0.45m** — a slow body perfecting on the winning jockey inside the race window. (Luke Morris rode Outbox at Kempton on 4 Sep.)
- Wotever Next: the Moon hits the horse's natal Chiron during the race with Flat 700/9 (+0.34m) and Flat 55√2 (+0.89m) — the same two numbers the Moon carried from Alkaid to the Pleiades on 4 Sep. Horse Pluto–Arcturus Sky 800/9 (99.8, applying) while the Sun (RA 114√2) and the Moon hit Arcturus before the off. Moon on horse Uranus (Sky 46) and Ceres → horse Uranus (RA 44) during.

## 38. Musical intervals as ratio relations — 6 Apr 2022 (intervals.py; afternoon/l0406/IV_*.txt)
Intervals added (pure ratios, tritone = √2): PERFECT octave 2, fifth 3/2, fourth 4/3, twelfth 3, double octave 4; IMPERFECT major/minor third 5/4, 6/5, major/minor sixth 5/3, 8/5, major tenth 5/2, octave+fourth 8/3; DISSONANT tritone √2, major second 9/8, minor seventh 16/9, major seventh 15/8, minor second 16/15; PHI group φ, φ², φ³, 1+√2 (not musical). Ratio of two distances from one mover (RA, Dec, Flat, Sky), exact crossings, off−10 to finish+1, sky and each runner (natal refs; ONLY).
(Eddie: some of these values are already in the single-number families — 5/3, 4/3, 8/3, 16/9 are ninths; 3/2, 5/2, 5/4 are half/quarter values.)
What was seen:
- **Catterick 14:40 (33/1): the winner has the least dissonance during the race.** Dissonant intervals during the race per minute (ONLY): Wotever Next 4.1 (down from 10.5/min before the off), Thakuri 12.9, Beluga Gold (fav) 10.9, Capuchinero 10.2, Tea Garden 16.3. Wotever Next's first half-minute is all consonant/φ (fourth Mercury–Ceres–jockey Vesta, fifth and twelfth Moon–Transpluto–jockey Chiron, octave Mars–Sirius–jockey Rahu); its first dissonance comes at +0.55m. The favourite takes dissonance from the off (Moon–jockey Vesta–horse Mars major second at +0.02m, then minor seconds, a major seventh, two tritones by +0.56m).
- **Lingfield 14:25 (12/1): not repeated.** Man On A Mission 10.0 dissonant/min during, mid-field (Brazen Idol 5.0, Vintage Fashion 6.7, Judy's Park fav 10.8, Jaas Yard 15.0, Bang On The Bell 15.8). Man On A Mission has the highest φ-group rate (10.0, with Vintage Fashion).
- Sky: during Catterick perfect intervals rise (6.8/min v 4.6 before); dissonance level (6.1 v 5.6). During Lingfield perfect falls (2.5 v 4.7).
- **Mars–Saturn conjunction background (Mars conjunct Saturn 5 Apr 2022):** Mars, Juno and Saturn within 1.6° RA; 63 s before the Catterick off they make a perfect chord in RA — Mars: Juno = fifth × Saturn, Saturn: Mars = octave × Juno, Juno: Mars = twelfth × Saturn (14:39:06). During the race Mars: Saturn = tritone × Deneb Algedi (+0.58m).
- Counts are small (6–20 per runner during a 1.2–1.5 min race), so one race either way is noise-level; the shifted-clock baseline is needed before reading the rates.

## 39. 6 Apr 2022 — the Mars–Saturn conjunction on Deneb Algedi, in detail
Positions at 14:40: Mars RA 325.992 Dec −14.982; Saturn RA 324.908 Dec −15.006; Deneb Algedi RA 326.759 Dec −16.127; Juno RA 324.367 Dec −6.305. Mars and Saturn 1.05° apart (Sky Dist) at the same declination (0.024° apart — they were exactly parallel in Dec around 12:00 and separate slowly through the afternoon); both within ~2° of Deneb Algedi (Mars 1.36°, Saturn 2.11°); Juno 8.8° north in the same RA column. Mars moves +0.031° RA/h towards Deneb Algedi, Saturn +0.004, Juno +0.015.
Intervals among the four across the afternoon (non-Moon, exact moments):
- **The 1:2:3 chord in RA (octave, fifth and twelfth at one instant — one point dividing the other two in RA at 1:2) comes twice, both one minute before a Catterick off, both outsider wins:**
  - 13:29:32 — Juno–Mars–Deneb Algedi (Mars: Juno = octave × Deneb Algedi; Juno: Deneb Algedi = fifth × Mars; twelfth) — 1.0 min before Catterick 13:30 (Vadamiah 14/1 beat the 3/1 fav).
  - 14:39:10 — Juno–Saturn–Mars (Saturn: Mars = octave × Juno; Mars: Juno = fifth × Saturn; Juno: Mars = twelfth × Saturn) — 1.0 min before Catterick 14:40 (Wotever Next 33/1 beat the 2/5 fav).
  - Before the second: Saturn: Deneb Algedi = octave × Mars (Flat) at 14:37:14, 2.9 min before the off.
- **Then the tritone inside the race:** at 14:40:47 (+0.64 min) Mars: Saturn = √2 × Deneb Algedi in RA (and Deneb Algedi: Saturn = (1+√2) × Mars — the same moment, Mars dividing Saturn–Deneb Algedi at √2). Consonant chord a minute before the off, discord during the race.
- Other moments: fourths around Nottingham 13:40 (+4.5m) and during Lingfield 13:55 (W); octave (Sky) after Nottingham 14:50; **a 2:3:5 chord in RA 1.3 min before Lingfield 15:35** (Mars: Saturn = fifth × Deneb Algedi; Saturn: Deneb Algedi = major sixth × Mars; major tenth) — Pistoletto 100/30 beat the joint favourites; major third (Flat) 0.3 min before Catterick 15:15 (B); major third (Sky) during Nottingham 16:00 (W).
- Runners: neither winner has a natal point in or tied to the cluster around their race. Thakuri (Catterick, 28/1, last) has natal Venus inside it (RA 325.81, Dec −14.12, 0.9° from Mars) and takes three cluster intervals in the minute before the off and one during. Capuchinero's jockey Mars: Juno: Deneb Algedi = minor third during.
- **Note (Eddie): "harmonics from the stars" — we now go back to Layer 1 and work layer by layer looking for harmonics and chords (blank-sheet design §9).**

## 40. Harmonics from the stars — Layer 1 chords (chords1.py; afternoon/harm/H1_*.txt)
Chord = three points whose three distances (same measure) are all in interval ratios at one instant (one exact, the other two within 0.15%). In RA and Dec a body between two stars makes a chord whenever it divides them in a simple proportion: 1:1:2 (midpoint — unison/octave), 1:2:3 (octave+fifth+twelfth), 1:3:4 (fourth+twelfth+double octave), 2:3:5 (fifth+major sixth+major tenth), 1:4:5 (major third+double octave+5th harmonic), 1:5:6 (minor third+5th+6th harmonic), **3:5:8 (minor sixth+major sixth+octave+fourth — Fibonacci, the nearest simple chord to φ)**, and the φ triad 1:φ:φ² (golden section).
What was seen, 6 Apr 2022 (Catterick 14:40):
- **Standing chords among the stars themselves (29):** tightest — Bellatrix–Sirius–Spica in RA 20.003° / 100.020° / 120.023° (1:5:6, 0.008%); Alkaid–Altair–Deneb Algedi in Dec (golden section, 0.010%); Algol–Betelgeuse–Fomalhaut RA (2:3:5); Algorab–Pleiades–Rigel RA (1:5:6); Algol–Polaris–Regulus Dec (3:5:8); Algol–Bellatrix–Sirius Dec (2:3:5); Aldebaran–Castor–Fomalhaut Dec (1:3:4). At Nottingham 15:25 (fav won) the Moon sits in the Bellatrix–Sirius–Spica chord in RA (1:4:5 with Sirius–Spica and Bellatrix–Sirius, 15:27).
- Catterick 14:40 race chords: Sun Aldebaran–Sirius 3:5:8 (−7.8m); Moon Pleiades–Regulus 1:4:5 (−5.2m); Moon Regulus–Rigel golden section in Dec (−3.4m); **Moon Capella–Rigel 1:5:6 in RA 41 s before the off** (Capella and Rigel only 0.538° apart in RA); Mercury Altair–Procyon 3:5:8 in Dec during (+0.68m); **Mars Altair–Capella 1:4:5 in RA during (+1.28m)**; Moon Betelgeuse–Capella 1:3:4 and Ceres Algol–Regulus 1:3:4 after the finish. Capella is in four of them.
- **Moon–star chords race by race on 6 Apr: the Moon makes a 1:2:3 chord with two stars at 7 of the 11 beaten-favourite races and at none of the 4 favourite wins; the 3:5:8 (Fibonacci) chord comes only at favourite wins (Lingfield 13:55, Nottingham 15:25 ×2, Catterick 15:50).**
- **Not repeated on 4 Sep 2021:** there the Moon's 1:2:3 chords fall at fav-won races too (Stratford 14:30 / Ascot 14:35 ×3, Kempton 15:15 ×4, Thirsk 15:25) and 3:5:8 at six beaten races. 8 Jul 2022: no Moon 1:2:3 at all; 3:5:8 only at the two early beaten races. (Moon events seen from two nearby courses appear at both.)
- Natal: every runner has ~70–125 static chords between its midday points and star pairs, and every runner shares some star pairs with the race's transit chords — no separation by count. Wotever Next: horse Vesta in a 1:4:5 chord with Regulus–Rigel in Dec (0.003%) — the pair the Moon made a golden section with 3.4 min before the off; Beluga Gold (fav) horse Sun 3:5:8 on Aldebaran–Sirius in Dec (0.002%) — the pair the Sun made 3:5:8 with in RA 7.8 min before; Capuchinero (3rd) horse Rahu 1:3:4 on Betelgeuse–Capella in RA — the same chord the Moon made after the finish.

## 41. Layer 1 chords with the full interval list (chords1.py v2; afternoon/harm/v2/H1_*.txt)
Added (Eddie: 11 and 13 in from the start): SEPTIMAL 7/4, 7/3, 7/2, 7/5, 7/6, 8/7; IMPERFECT 9/4; DISSONANT 9/5 and 1+1/√2 (the partner that completes the √2 division 1 : √2 : 1+√2 — the discord chord); HARMONIC 9; HIGH 11/5, 11/6, 11/3, 11/8, 11/4, 13/5, 13/8, 13/4; PHI φ√5, 2−1/φ, φ³+1, 2/φ (complete the φ², φ³ divisions). Standing star chords 29 → 67 (e.g. Alphecca–Arcturus–Vega Dec 5:8:13 Fibonacci, 0.004%; Betelgeuse–Deneb Algedi–Vega Dec 3:4:7; Antares–Deneb Algedi–Regulus RA 5:6:11).
**The √2 division (discord chord) — the Moon splitting two stars at √2:**
- 6 Apr Catterick 13:00 (Giant Steps 33/1): Moon on Fomalhaut–Polaris (RA) 2.3 min before the off.
- 6 Apr Catterick 14:40 (Wotever Next 33/1): **Moon on Arcturus–Castor (Dec) 70 s before the off** (14:38:59); during the race the Moon is at the √2 complement of Algol–Pleiades (+1.26m).
- 4 Sep Haydock 14:20 (Golden Flame 9/1): **Moon on Altair–Vega (Dec) during the race** (+0.95m).
- 4 Sep Kempton 14:40 (Hamish 9/1): Moon on Arcturus–Pleiades (Dec) 0.7 min after the finish.
- Also at beaten races: Nottingham 13:40, Catterick 15:15 (×2), Lingfield 15:35 (6 Apr); Thirsk 14:15 (4 Sep).
- But also at fav wins: Stratford 14:30 and Thirsk 15:25 ×2 (4 Sep); **Newmarket 16:10 on 8 Jul twice, one during the race** (fav won). On 8 Jul every √2 division of the afternoon falls in the fav-won stretch (Sun, Pallas, Mars, Moon, Jupiter).
- 6 Apr all bodies: 12 of 13 √2 division chords at beaten races (Mercury on Deneb Algedi–Pleiades three times through Catterick 13:00/13:30; Mars on Aldebaran–Vega during Nottingham 13:40).
- Catterick 14:40 with the new list: Moon Pleiades–Sirius 3:4:7 (septimal, −6.7m); Moon Pleiades–Rigel and Alphecca–Pleiades 1:7:8 (−5.4, −4.3m); Mercury Regulus–Vega 1:6:7 (−2.3m); Mercury Algorab–Alphecca 4:5:9 (−0.8m); Moon Betelgeuse–Procyon Sky octave+φ triangle at −6.3m and again during (+0.96m).

## 42. The star lattice — chords among the stars and their empty "nodes" (scratch: starnet.py, moonnode.py)
Eddie: "the stars are all connected in harmonics and chords — we should be able to work out from the star-only connections any missing chords / harmonics and which are linked in which harmonic families."
First pass, Dec and RA (1-D), stars as on 6 Apr 2022, full interval list, 0.15%:
- For every position on the Dec axis (−35° to +90°) and the RA circle, count the star pairs with which a point there would make a complete chord. Background: a random position completes 5.6 (Dec) / 4.1 (RA) star chords; 99.9th percentile 15 (Dec) / 13 (RA). **The empty positions that complete the most star chords are the "nodes" of the star lattice — the missing points of the chords.**
- Dec nodes (13–16 pairs): −34.48, −31.22, −24.47, −24.29, −20.31, −19.92/−19.86 (16), −8.04, −4.02 (16), −0.44, **−0.005 (the equator itself, 14 pairs)**, +7.28, +12.43 (16), +13.14, +18.61, +19.57, **+24.33 (15)**, +27.49, +54.45 (16), +55.62, +58.85, +66.24/66.30, +77.22, +77.97.
- RA nodes (12–16): 10.52 (16), 21.32, 49.65, 53.59, 93.10, 111.27, 121.30, 131.12, **134.62 (16)**, 136.65, 138.39, 139.52, 146.52/146.58, 172.48, 342.95 …
First check — the Moon against the nodes, peak number of star chords it completes from 2 min before the off to the finish, every race on the three days:
- **Kempton 14:40, 4 Sep (Hamish 9/1): the Moon reaches RA 134.62 — the top RA node — at +2.50m (the finish is +2.58m) and completes 17 star chords at once, the most of any race on the three days.** It was approaching the node at Ascot 14:35 (W, 9) and past it by Stratford 15:05 / Ascot 15:10 (11).
- 6 Apr: the Moon sits on the Dec node +24.33 two minutes before Nottingham 13:40 (Barley 3/1 beat the 6/5 fav) — 15 chords. At Catterick 14:40 (33/1) it completes only 6 (not at a node).
- Other races 4–11.
Next: harmonic families (which stars are linked by which chord types) and the nodes in Flat/Sky Dist; then when each transit body crosses a node at the races.

## 43. Harmonic families of the 22 stars (lattice/families.py → families.txt; chance check lattice/chance.py)
67 standing chords among the stars (RA 25, Dec 37, Flat 2, Sky 3). Families (chord type → stars):
- 5:8:13 (Fibonacci) 8 chords — Alphecca 4, Vega 3, Betelgeuse 3, Procyon 2, Capella 2 …
- golden section 1:φ:φ² 7 — Deneb Algedi 3, Alkaid 3, Arcturus 2, Pleiades 2, Sirius 2 …
- 2:5:7 (septimal) 6 — Fomalhaut, Sirius, Procyon, Rigel, Vega 2 each
- 3:8:11 5 — Rigel 3; 1:3:4 5 — Arcturus 3; 3:4:7 4; φ² division 4; 2:3:5 4; 3:5:8 4; 1:8:9 3 — Betelgeuse 3; 4:5:9 3; 5:6:11, 1:2:3, 1:5:6 2 each; 1:1:2, 1:4:5, 1:6:7, 6:10:15 one each.
- Most connected stars: Betelgeuse 14, Fomalhaut 14, Algol 13, Arcturus 13, Deneb Algedi 13 (11 of them in Dec), Sirius 13; least: Regulus, Polaris, Bellatrix, Altair, Alkaid, Algorab 6.
- **Chance check: 22 random points (uniform, or the real stars jittered ±3°) give the same number of chords** — RA mean 26–27 (real 25), Dec mean 36–39 (real 37); the real stars sit mid-range. With 47 intervals at 0.15% any set of 22 points is this connected. So the stars ARE all linked in chords, but not more than any 22 points would be; the families and the nodes are the structure the bodies move through, and what can carry meaning is the timing — which nodes/chords the bodies complete at the races, against the times either side.

## 44. 2-D nodes of the star lattice — Flat Dist and Sky Dist (lattice/nodes2d.py → nodes2d.txt)
Every star pair × every pair of ratios (r1, r2, r1/r2 all on the interval list): the points completing a chord with that pair (circle intersections) — ~230,000 chord points in each measure. Node = where chord points from several different star pairs fall within 0.1°.
- Top nodes complete 5–7 star chords at once. **Almost all of them lie in the Taurus–Orion–Gemini region, RA ~50–100°, Dec −5 to +40** (where Aldebaran, the Pleiades, Capella, Bellatrix, Betelgeuse, Rigel, Castor, Procyon, Sirius crowd together) — the ecliptic runs through it.
  - Sky Dist: RA 53.17 Dec +14.47 (7: Aldebaran–Algol, Aldebaran–Capella, Aldebaran–Pleiades, Algol–Bellatrix, Algol–Capella, Alphecca–Castor, Capella–Procyon); RA 99.20 +15.41 (6); RA 82.95 +17.88 (6); RA 99.02 +20.04 (6); RA 97.16 +6.59 (6); outside the region RA 275.38 +7.82 (6) and RA 171.11 −0.28 (6, on the equator).
  - Flat Dist: RA 82.07 Dec +30.67 (6); then many 5s around RA 71–95.
- Chance check (stars jittered ±3°, 12 skies): top nodes 6–7 — the same as the real stars. The node sizes are what the stars' clustering gives, not extra.
- The Moon on 6 Apr was in this region (RA ~75–77, Dec +24).

## 45. STEP 3 — chord load of each body against the star lattice, race by race (lattice/load3.py → L3_YYYYMMDD.txt)
Every body, every 0.05 min: how many star pairs it completes a full chord with (RA, Dec, Flat, Sky; full interval list). Race window = off−2 to the finish. LIT = the body's peak in the race window is higher than its peak in every same-length window 30, 60 and 90 min either side. (Slow bodies with a constant load are never lit. The first and last races of a day have fewer comparison windows, so they light up more easily; peaks at −1.95/−2.0 min are the window's edge.)
What was seen — the outsider wins:
- **Kempton 14:40, 4 Sep (Hamish 9/1): the Moon completes 25 star chords at +1.12 min, during the race — its highest of the afternoon (17/21/17/19 in the windows either side).** Ketu also lit (9, −2.0m).
- **Catterick 14:40, 6 Apr (Wotever Next 33/1): Mercury completes 15 star chords 2 s before the off** (13/8/10/11/10/14 either side) — the only lit body.
- **Haydock 14:20, 4 Sep (Golden Flame 9/1): Rahu completes 16 star chords 39 s before the off** (15/14/14 either side) — the only lit body.
- Catterick 14:05, 6 Apr (Gold Ring 22/1): Mars 18 (window edge, −2.0m). Kempton 14:05, 4 Sep (Eve Lodge 16/1): the Moon 17 during the race (+1.2m). Nottingham 13:40, 6 Apr (3/1 beat 6/5 fav): the Moon 19 (edge). York 15:15, 8 Jul (3/1 beat 8/11 fav): the Moon 18 three seconds before the off, plus Jupiter 22 (edge).
- Lingfield 14:25, 6 Apr (Man On A Mission 12/1): nothing lit.
- Fav-won races average more lit bodies (6 Apr W 3.75 v B 1.09; 4 Sep W 2.29 v B 1.22) but that is mostly the late races (Catterick 15:50, Nottingham 16:00, Kempton 15:15, Thirsk 15:25) at the end of the day, where the edge effect applies; 8 Jul the other way (B 3.33, W 1.75).
- So at the charted outsider wins one body at a time peaks in star chords at the off or during the race: Rahu (Haydock), the Moon (Kempton — the strongest), Mercury (Catterick 33/1).

## 46. Catterick 14:40, 6 Apr 2022 — the race read against the star lattice (lattice/race_read.py → R_20220406_catterick_1440.txt)
- **Load timeline (own minute file, every 30 s, off−10 to finish+1):** Mercury steps up to 15 star chords exactly at the off (13–14 before); the Sun goes 7 → 6 at −1.0m → 8 at the off; Pallas rises 12 → 13 (−5m) → 14 at +1.5m; Juno drops 12 → 11 at −3m; **the Moon falls from 14 (−8m) to 7 at the off** — its load collapses into the race as it moves off the Hexagon chords. Constant (slow): Chiron 15, Transpluto 13, Gonggong 12, Rahu/Uranus/Eris/Sedna/Haumea/Orcus 11, Ketu 10.
- **Mercury at the off (RA 18.94, Dec +7.50), 15 chords:** two √2 divisions (discord) — Dec Algol–Deneb Algedi, RA Algorab–Betelgeuse; 1:6:7 twice (Dec Arcturus–Polaris, Regulus–Vega); Fibonacci 5:8:13 twice (Dec Arcturus–Spica, RA Bellatrix–Vega); 4:5:9 Algorab–Alphecca (0.005%); 3:8:11 ×3; 3:5:8 Altair–Procyon; 1:4:5 Algol–Alkaid; 1:5:6 RA Algol–Algorab; golden RA Regulus–Sirius. Algorab is in four, Algol in three.
- **The Moon at the off (RA 75.95, Dec +24.44, inside the Hexagon), 7 chords:** √2 division Dec Arcturus–Castor; golden section Dec Regulus–Rigel; 5:6:11 Fomalhaut–Polaris; 5:8:13 Deneb Algedi–Polaris; 4:5:9 RA Antares–Regulus.
- **Mars at the off (in the conjunction on Deneb Algedi), 16 chords:** √2 division Dec Aldebaran–Vega; RA 1:4:5 Altair–Capella (0.003%); RA 3:5:8 Spica–Vega; 1:2:3 RA Algorab–Alphecca; Dec 1:8:9 Capella–Rigel; three 3:8:11 / 5:6:11 with the Pleiades.
- **Runners** (body at the off – natal point – star triangles in full chord): 130–177 per chart, no separation by count (Beluga Gold the fav has the most Mercury chords, 34). Specific to the winner:
  - Wotever Next: **transit Mercury – horse's own natal Mercury – Alphecca in RA 1:4:5 (0.002%)** — the lit body in a chord with its own natal place; transit Mercury exactly midway in Dec between the horse's Vesta and Arcturus (1:1:2, 0.006%); Juno – horse Chiron – Antares Dec 1:2:3; Saturn – horse Pallas – Regulus RA 1:2:3; Saturn – horse Rahu – Fomalhaut Dec 2:5:7 (0.003%).
  - Joanna Mason: **Mars exactly midway in Dec between her natal Rahu and Sirius** (1:1:2, 0.007%); Saturn – her Venus – Algorab Dec 1:3:4 (0.001%); Mars – her Saturn – Regulus Dec 1:4:5; Saturn – her Pluto – Betelgeuse 3:4:7.
  - Shared by both 2018 horses (Wotever Next, Beluga Gold): Mars midway in Dec between horse Pluto and Rigel.

## 47. Catterick 14:40 — the Moon's drop from 14 to 7 star chords, every 5 s (lattice/R_20220406_catterick_1440_MOON.txt)
- Peak 14 at off−8 (14:32:09); 7 at the off; nothing lost during the race.
- Lost off−8 to the off: the REGULUS chords (Castor–Regulus Dec 3:5:8 −6.92, Alkaid–Regulus Dec 1:2:3 −5.83, Regulus–Sirius RA 1:2:3 −4.83, Pleiades–Regulus RA 1:4:5 −1.92, Fomalhaut–Regulus RA 5:6:11 −1.75) and the PLEIADES chords (Pleiades–Rigel RA 1:7:8, Pleiades–Sirius RA 3:4:7 −4.33); also Bellatrix–Castor RA 1:6:7 −7.83, Alkaid–Altair Dec 5:8:13 −0.83, Capella–Rigel RA 1:5:6 (in −1.25, exact −0.67, out 5 s before the off).
- Left at the off: 6 long holds from before the window (Antares–Sirius Dec φ, Deneb Algedi–Polaris Dec 5:8:13, Fomalhaut–Polaris Dec 5:6:11, Regulus–Rigel Dec φ/φ², Antares–Regulus RA 4:5:9, Betelgeuse–Procyon Sky φ) + one new chord, the √2 Arcturus–Castor Dec (in −3.33, exact 14:38:59 −1.17, out +1.08). 5 of 7 in Dec.
- During the race: one gain, RA 1:3:4 Betelgeuse–Capella at 14:41:19 (+1.17, 18 s before the finish). Just after: RA √2 Bellatrix–Betelgeuse (+1.75, exact +2.83). The long holds all break up after the race (+2.58 to +10.75) and the count climbs on short Orion/Taurus RA chords — the Moon at RA 75.9 sits among Capella, Rigel, Bellatrix, Aldebaran.
- Deneb Algedi is in one of the Moon's chords at the off (Dec 5:8:13 with Polaris, exact −15.25, out +2.58).

## 48. Catterick 14:40 — transit Mercury – natal Mercury – star chords, all runners (lattice/R_20220406_catterick_1440_MERCURY.txt)
- Transit Mercury RA 18.94 Dec +7.50, nearly still (0.0015°/min in RA), so the chords last the whole hour; what differs is WHEN each is exact (5 s steps).
- The horses' natal Mercuries all sit at RA 347–360 (spring 2019 births, Tea Garden 2018); the jockeys' are spread.
- Exact in the race window (off−2 to finish): Wotever Next (1st, 33/1) RA 1:4:5 with Alphecca, exact 14:39:44, 25 s before the off; Beluga Gold (2nd, 2/5F) Dec 5:8:13 with Antares, exact −1.58; Thakuri (5th, 28/1) Dec 3:5:8 with the Pleiades, exact +0.58 (during the race). Just outside: Capuchinero RA 5:8:13 Pleiades −2.08, Tea Garden Dec φ Alphecca −2.58.
- Wotever Next's is the closest to the off. Also Wotever Next Dec 1:5:6 Rigel (exact −14.25).
- Jockeys: Joanna Mason and Connor Beasley have no Mercury–natal Mercury–star chord at all; Jason Hart a Dec √2 with Fomalhaut (in −3.00, exact after +15); Dougie Costello Dec 2:3:5 Algol exact −8.17; David Allan RA 1:4:5 Capella.
- Alphecca appears for two horses (Wotever Next RA, Tea Garden Dec).

## 49. Catterick 14:40 — NODES LAYER chords (lattice/nodes_chords.py → N_20220406_catterick_1440.txt)
- Points: Layer 1 (22 stars on race day + equator + course latitude 54.37, Dec-only) + Nodes. Rahu–Ketu pair: RA and Sky skipped, equator skipped (always the midpoint). Nodes move ~0.03°/d RA, 0.007°/d Dec here, so chords stand all afternoon; timing = when exact at the day's rate.
- Transit: Rahu 12 chords, Ketu 12. Closest to the afternoon: Rahu Dec 2:5:7 on Betelgeuse–Capella (Dec 38.592), exact 13:32:28 (55 s after the Catterick 13:30 finish, Vadamiah 14/1 B); Ketu Dec 5:8:13 on Bellatrix–Capella, exact 16:47. Ketu Dec 1:7:8 with Deneb Algedi and the equator (exact 38 d before, separating) — Ketu + Deneb Algedi, cf. the Pholas lead.
- WINNER Wotever Next: natal Ketu Dec 3:4:7 on the SAME Betelgeuse–Capella length as transit Rahu, dev 0.000% (stood at birth too). Only other chart near that base: Dougie Costello J.Ketu 0.111%. Transit–natal node chords for the winner not exact on the day (nearest 21 h before: Rahu–H.Ketu–Capella RA 1:4:5; 8.7 h after: Ketu–H.Rahu–Spica RA 1:3:4).
- Closest transit–natal node exact to the race: Thakuri (28/1, 5th) Rahu–H.Ketu–Pleiades Dec 1:7:8, 12:49 (1.8 h before).
- Own Rahu + own Ketu + one point (E): horse AND jockey both have one for the three outsiders (Wotever Next/Joanna Mason, Tea Garden/Connor Beasley, Thakuri/David Allan); none for the 2/5F pair or the 9/4 pair (who ran 2nd and 3rd). One race only.

## 50. Catterick 14:40 — Nodes layer, TRANSIT AND NATAL TUNED IN (lattice/tuned_nodes.py → T_20220406_catterick_1440_nodes.txt)
- 24 transit node chords on 24 bases; each chart's natal node chords (stars at birth) 15–33.
- Tuned in (same base, same measure): Wotever Next 4 (most of any chart); Dougie Costello 3; David Allan 2; Beluga Gold 1; Thakuri 1; Joanna Mason, Jason Hart, Capuchinero, Tea Garden, Connor Beasley 0.
- Wotever Next's four, all Dec: Betelgeuse–Capella (H.Ketu 3:4:7 0.001% / Rahu 2:5:7 0.004%, exact 13:32 — the tightest pair in the race, and the transit chord nearest the afternoon); Alphecca–Betelgeuse (H.Ketu 2:3:5 / Rahu 3:4:7); Alphecca–Castor (H.Rahu 1:1:2 / Rahu 5:8:13); Deneb Algedi–Equator (H.Rahu 3:4:7 / Ketu 1:7:8). Three of four are crossed (natal Ketu ↔ transit Rahu, natal Rahu ↔ transit Ketu). Stars: Betelgeuse ×2, Alphecca ×2 (Alphecca also in his Mercury chord, §48), Capella, Castor, Deneb Algedi.
- Only other chart on Betelgeuse–Capella: Dougie Costello J.Ketu 4:5:9 0.124%. Ketu RA 2:5:7 Algorab–Antares is the shared one for the beaten favourite (Beluga Gold), Dougie Costello and David Allan.
- No UNISON (same chord type) in this race.

## 51. Catterick 14:40 — LAYER 1 REDONE, TRANSIT AND NATAL TUNED IN on the star bases (lattice/layer1_tuned.py → T1_20220406_catterick_1440.txt)
- Stars-only tuning is empty of meaning (stars at birth ≈ stars on race day), so Layer 1 = the star BASES: every transit body + base (race day; Moon off−2 to finish) vs every natal point at midday + base (stars at birth). 292 transit chords on 225 bases; each chart 120–180 tuned pairs, so counts alone say nothing.
- Pairs with BOTH sides within 0.02%: Wotever Next 5, Joanna Mason 4 (winning pair 9); Jason Hart 4; everyone else 1–2.
- Wotever Next's tight five: Dec Betelgeuse–Capella (H.Ketu / Rahu, §50); Dec Algorab–Fomalhaut (H.Neptune 0.001% / Rahu); Dec Aldebaran–Fomalhaut (H.Chiron / Jupiter); Dec Regulus–Rigel (H.Vesta 0.004% / Gonggong); RA Capella–Rigel (H.Juno / Moon). Capella ×2, Fomalhaut ×2, Rigel ×2.
- Joanna Mason also tuned to Betelgeuse–Capella (J.Uranus / Rahu) — horse and jockey on the same base. Her UNISON: RA 3:5:8 on Castor–Deneb Algedi (J.Eris / Sedna).
- THE MOON AND NATAL MAKEMAKE: three of the Moon's seven chords at the off are UNISON (same chord type, same base) with natal Makemake of the first two home only: Dec 5:6:11 Fomalhaut–Polaris (Moon exact 14:29:34), Dec φ Antares–Sirius (14:13:44), Dec 5:8:13 Deneb Algedi–Polaris (12:10). Wotever Next tighter on two (natal 0.036%, 0.002%), Beluga Gold on one (0.028%). No other chart.
- The Moon's √2 Arcturus–Castor (exact 14:38:59) is tuned by Connor Beasley (J.Mercury 0.005%), Thakuri, David Allan — not the winning pair.
- Winner only: Dec Alphecca–Fomalhaut, transit Transpluto 2:5:7 dev 0.000% at the off / natal Saturn 1:6:7.
- Shared by many (not special): Dec Algorab–Fomalhaut (Rahu), Dec Alkaid–Altair (Pallas, exact 14:49), Dec Fomalhaut–Regulus (Neptune).
- Slow bodies: exact minute is arithmetic; the chord holds for days.

## 52. Catterick 14:40 — the Moon and natal Makemake, layer completed (lattice/moon_tuned.py → MT_20220406_catterick_1440.txt)
- WHY the three UNISONs: the Moon is PARALLEL (same Dec) to the natal Makemake of the 2019 horses. Same Dec ⇒ every Dec chord the Moon makes with a star pair, that Makemake makes too. Moon Dec 24.374 (off−30) → 24.439 (off) → 24.500 (off+30), rising ~0.002°/min.
- Moon on Wotever Next's natal Makemake Dec (+24.4065) at 14:24:48 (off −15.35); the Moon's Dec 5:8:13 Deneb Algedi–Polaris chord exact 14:24:54 — 6 s apart (his Makemake is itself 0.002% on that chord). Moon on Beluga Gold's Makemake Dec (+24.3769) at 14:11:07 (off −29). Thakuri's (+24.306) ~an hour before; Capuchinero's (+24.098) earlier; Tea Garden's (+24.660) well after. The Moon walks up through the 2019 crop's Makemake Dec in this hour and reaches the winner's 15 min before the off.
- Of every transit body/natal point Dec-parallel or same-RA, the two nearest the off in time are these two (Moon–Wotever Next Makemake, Moon–Beluga Gold Makemake) — 1st and 2nd home. Next: Mercury–Dougie Costello Orcus 1.1 h before.
- Moon chords held in the race window (off−2 to finish), charts tuned: Wotever Next 11 natal points (3 UNISON), Beluga Gold 8 (3 UNISON), Capuchinero 4 (1), all others 0 UNISON. Winner's tightest: Makemake DA–Polaris 0.002%, Pallas Dec Arcturus–Procyon 0.003%, Vesta Dec Regulus–Rigel 0.004%, Juno RA Capella–Rigel 0.013%.
- RA Capella–Rigel 1:5:6 (Moon in −1.25, exact 14:39:29, out 10 s before the off) — tuned by Wotever Next's Juno ONLY.
- During the race, RA Betelgeuse–Capella 1:3:4 (in +1.17): Dougie Costello J.Sedna 0.000%, Wotever Next Rahu 0.062%, Capuchinero Rahu (UNISON).

## 53. Catterick 14:40 — NODES LAYER, tuned in (lattice/nodes_tuned.py → TN_20220406_catterick_1440.txt)
- Base = a node at one end (Rahu–X, Ketu–X, X = star/equator/course lat; Rahu–Ketu in Dec/Flat); third point = a body. Transit 63 chords on 54 bases. Tuned = same NAMED base and measure. Caveat: transit Rahu ≠ natal Rahu, so the two base lengths differ — shown as SAME LENGTH / an interval / no relation. Weaker tuning than Layer 1 (where the base was one fixed star pair).
- No standout counts (17–35 tuned pairs per chart).
- MOON ON NODE BASES IN THE RACE: Rahu–Fomalhaut Dec 1:8:9 (held 14:40:24, +0.25) and Rahu–Capella RA 1:8:9 (held 14:41:09, +1.00, 28 s before the finish). The winning pair are the only charts tuned to these with the √2 DISCORD DIVISION: Wotever Next natal Uranus √2 on his Rahu–Capella (0.006%); Joanna Mason natal Orcus √2 on her Rahu–Fomalhaut (0.044%). Others on those bases: Beluga Gold Mars 3:5:8 on Rahu–Capella (lengths 5/4); Jason Hart Chiron/Eris, Capuchinero Ceres on Rahu–Fomalhaut.
- Also near the off: Mercury on Rahu–Deneb Algedi RA 3:5:8 exact 14:37:16 (tuned Jason Hart Neptune 0.006%, Dougie Costello, David Allan); Jupiter on Rahu–Castor Dec 3:5:8 exact at the off (tuned Capuchinero Jupiter, Connor Beasley, David Allan). Neither the winning pair.
- Capella again (Rahu–Capella); Deneb Algedi bases busy with Ketu/Rahu for many charts.

## CORRECTION (6 Oct 2026) — exact times of slow-body chords in §49–§53
- Bug: the exact-time search followed whatever chord fitted best as the body moved, so for slow bodies it sometimes reported the time of a DIFFERENT chord type (days or weeks away). Fixed: the search is now locked to the chord's own three intervals, with a fine pass (≈1 min). Moon times (minute-file scans) and §47/§48/§52 unaffected.
- §49/§50: Rahu Dec 2:5:7 Betelgeuse–Capella 13:32:28 and Ketu Dec 5:8:13 Bellatrix–Capella 16:47 STAND. But it is NOT the node chord nearest the race: Rahu Dec φ Aldebaran–Arcturus exact 14:58:35 (18 min after the off; tuned only loosely, Dougie Costello) and Ketu Dec 1:5:6 Rigel–Sirius 13:41:33 (Wotever Next Gonggong 3:4:7 0.032%). Ketu Dec 1:7:8 Deneb Algedi–Equator exact 22:05 that evening (not 38 d before).
- §51 additions (now timed): Jupiter Dec 4:5:9 Aldebaran–Fomalhaut exact 14:25:45 and Jupiter Dec 2:5:7 Betelgeuse–Regulus 14:31:09 — both tuned by Wotever Next's natal CHIRON (φ 0.012%, 4:5:9 0.022%); the first only by him. Mercury Dec 1:6:7 Regulus–Vega exact 14:37:54 (winner Orcus 0.013%, Ketu; Joanna Mason Mars 0.010%; Dougie Costello loose). MERCURY Dec 4:5:9 ALGORAB–ALPHECCA exact 14:39:20, 49 s before the off — tuned ONLY by the winning pair (Wotever Next Vesta 0.035%, Joanna Mason Neptune 0.017%). These two Mercury chords are the last non-Moon star-base chords to go exact before the off.
- §53: Mercury on Rahu–Deneb Algedi RA 3:5:8 exact 14:36:58; Jupiter on Rahu–Castor Dec 3:5:8 exact 14:34:06 (not at the off). Tuned charts unchanged.

## 54. Catterick 14:40 — LAYER L2, tuned in (lattice/layer_tuned.py … L2 → TL2_20220406_catterick_1440.txt)
- Base = an L2 body at one end (other end a star/equator/course lat, a node, or another L2 body); third point any body. 409 transit chords on 321 bases; each chart 171–200 tuned pairs. The 2019 horses' natal L2 bodies are close to where they are now, so their base lengths are near the transit ones (ratio ~1.0–1.15); the jockeys' are not.
- JOANNA MASON — the strongest thing in the layer: RA Pluto–Rahu base, transit MERCURY 2:5:7 exact 14:38:44 (85 s before the off) and her natal MERCURY 2:5:7 on her own Pluto–Rahu (0.001%) — UNISON and SAME BODY. Others on that transit chord: Tea Garden Vesta 1:4:5 0.043%, David Allan Haumea 2:5:7 (UNISON, 0.140% loose).
- Joanna Mason also: Dec Quaoar–Bellatrix, Juno √2 exact 14:42:45 (1 min after the finish) / her Saturn 2:5:7 0.003% (Jason Hart Makemake 0.004% too); Dec Neptune–Equator, Venus 1:2:3 exact 14:37:21 / her Quaoar 0.009% (also Capuchinero, Wotever Next loose).
- Wotever Next: Moon RA φ on Gonggong–Castor held 14:38:24 (0.000%) / his Uranus 5:8:13 0.011%, base lengths almost equal (1.005) — also Joanna Mason Sedna 0.037%, Jason Hart Uranus 0.038%. Moon Dec 4:5:9 on Neptune–Regulus held during the race (14:41:24) / his Sun 1:2:3 0.016%. Pallas Dec 2:3:5 on Orcus–Algorab exact 14:26:37 / his Neptune √2 0.017%.
- Busy at the off, not the winning pair: Venus RA 5:8:13 Neptune–Altair exact 14:40:04 (5 s before the off) — Capuchinero Juno UNISON, Thakuri, Dougie Costello, David Allan, and Joanna Mason (Sun φ). Mercury RA 5:8:13 Uranus–Fomalhaut 14:45:17 — Joanna Mason Venus 0.001%, Wotever Next, Beluga Gold, Tea Garden Pallas/Saturn.

## 55. Catterick 14:40 — LAYER L3, tuned in (layer_tuned.py … L3 → TL3_20220406_catterick_1440.txt)
- Base = an L3 body at one end (Jupiter, Saturn, Mars, Ceres, Pallas, Juno, Vesta). 223 transit chords on 180 bases; each chart 70–114 tuned pairs (Wotever Next fewest, 70).
- THE MARS–SATURN–DENEB ALGEDI CLUSTER COMES BACK (cf. §39): RA Mars–Juno–Saturn 1:2:3 exact 14:39:09 (1 min before the off); RA Mars–Saturn–Deneb Algedi √2 exact 14:40:39 (30 s into the race). Neither is tightly tuned to the winning pair (Wotever Next Eris/Sun ~0.10% on the √2; others: Dougie Costello Jupiter 0.017%, Thakuri Juno 0.038%).
- JOANNA MASON, both in UNISON:
  - RA Pallas–Bellatrix: transit PLUTO √2 division exact 14:40:54 (45 s into the race) / her Saturn √2 on her own Pallas–Bellatrix (0.042%), base lengths a 16/15 interval. Only UNISON on that transit chord.
  - RA Mars–Antares: transit SUN 5:8:13 exact 14:38:39 (90 s before the off) / her Pluto 5:8:13 (0.022%). Only UNISON on that chord.
  - also Dec Pallas–Regulus: transit Ketu 5:6:11 exact 14:23:27 / her Pluto 5:6:11 (0.026%).
- Wotever Next: Mars–Juno–Vesta RA 1:6:7 exact 14:37:54 / his Eris 2:3:5 0.037% (only horse tight on it); Mercury Dec 1:1:2 Pallas–Sirius exact 14:42:39 / his Juno 0.021% (also Joanna Mason Uranus 0.043%); his natal Mars and Pallas sit equidistant from Regulus in Dec (1:1:2), and transit Mars/Pallas make 5:8:13 on Regulus, exact 16:07 (same bodies, not near the race).
- Moon on L3 bases in the race window: Vesta–Rahu Dec 1:6:7 (−1.00) — Beluga Gold Saturn 0.000%; Juno–Procyon (−2) — Jason Hart Mercury 0.008%; nothing tight for the winning pair.

## 56. Catterick 14:40 — LAYER L4, tuned in (layer_tuned.py … L4 → TL4_20220406_catterick_1440.txt) + FULL-TRIANGLE UNISONS across all layers
- Base = Sun, Mercury, Venus or Moon at one end. 114 transit chords on 89 bases; each chart 20–41 tuned pairs. Moon bases cannot tune (no natal Moon), so the Moon here only shows as a third point. Note: a triangle has three sides, so L4 re-sees triangles already met in L2/L3 from another base (e.g. Joanna Mason's Mercury–Pluto–Rahu).
- New in L4 for Wotever Next: Venus–Equator Dec, transit Neptune 1:2:3 exact 14:37:24 / his Saturn 5:8:13 0.006% (also his Mars 0.023%; Joanna Mason Orcus 0.042%, lengths 4/3). Sun–Regulus RA, Moon 4:5:9 held during the race (14:41:24) — only Wotever Next tuned: his Uranus 1:8:9 0.011% (base lengths almost equal, 1.009), Rahu 0.051%. Sun–Capella Dec, Moon 5:6:11 (just before the window) / his Transpluto 0.002%.
- FULL-TRIANGLE UNISON = the same three points making the same chord in the natal chart and in the sky (UNISON + SAME BODY on a same-named base). Whole race, all layers: Joanna Mason Mercury–Pluto–Rahu RA 2:5:7 (natal 0.001%, sky exact 14:38:44, 85 s before the off) — the ONLY one exact within an hour of the race. Others: Wotever Next Vesta–Pluto–Gonggong RA φ (sky exact 15:00:53, 20 min after; 0.061%/0.073%), Dougie Costello Venus–Neptune–Quaoar Dec 3:5:8 (14:20:50, loose 0.119%/0.144%), Joanna Mason Mars–Makemake–Quaoar RA φ (13:27), Thakuri Ceres–Vesta–Altair Dec 3:5:8 (16:57), Dougie Costello Mars–Makemake–Orcus (19:12), Connor Beasley Jupiter–Castor–Regulus (20:41).

## 57. Catterick 14:40 — LAYER 5 side note, fast points (lattice/fast_points.py → L5_20220406_catterick_1440.txt)
- Transit only (charts at midday have no angles). Ascendant, Midheaven, Vertex, Part of Fortune, Part of Spirit as base ends, any body as third point. They sweep fast: ~1,700 chords go exact (to 0.02%) between off−2 and the finish (652 during the race) — about five a second — so any single one means little alone.
- Eddie's two picks, as they show in L5:
  - SUN–MOON–REGULUS: Midheaven–Regulus + Moon RA 1:2:3 exact 14:40:15 (6 s after the off); Midheaven–Regulus + Sun RA 1:5:6 exact 14:40:36 (27 s in). Before the off: Ascendant–Moon + Sun Dec 5:8:13 (14:38:51), Ascendant–Regulus + Sun Dec 1:4:5 (14:39:22), Part of Spirit–Regulus + Moon Dec 3:4:7 (14:39:50).
  - MERCURY–PLUTO–RAHU: Midheaven–Mercury + Pluto RA φ (14:38:25), Ascendant–Pluto + Rahu Dec 1:7:8 (14:39:37), Midheaven–Mercury + Rahu RA 2:3:5 (14:39:39), Midheaven–Mercury + Pluto Dec 1:4:5 during the race (14:41:06).
- At the off: Midheaven RA 37.85, Ascendant RA 146.96 (Regulus RA 152.10).

## 58. Catterick 14:40 — how the EARLIER work on this race (T33) fits the tuned-in read
- Earlier phases: test read "STANDOUT WINNER: no"; blind call picked Tea Garden (4th), Wotever Next not named; blank-sheet ranking had T33 as the most unexpected of the 96. Blank-sheet/ledger story = ORCUS carrier (horse Betelgeuse–Orcus Dec 160/9, jockey Arcturus–Orcus 140/9, closed loop #4 on horse Orcus) and the jockey's ERIS receiving (Juno/Moon pair; Sedna → Eris Dec 160/9; Moon → Eris peaking +1).
- Same bodies, now as chords:
  - REGULUS–SUN–NEPTUNE in the horse: earlier = royal Regulus–Sun Dec 6.0007 and Regulus–Neptune Dec 18.0001 (whole numbers). Together they are a natal Dec 1:2:3 chord (Sun–Neptune 11.999 | Sun–Regulus 6.001). In the race the Moon makes 4:5:9 on transit Neptune–Regulus (tuned by that Sun) and 4:5:9 on transit Sun–Regulus (tuned by his Uranus) at 14:41:24 — Eddie's pick 1 sits on the horse's royal Regulus imprint.
  - HORSE URANUS as end-of-race receiver: earlier Moon → horse Uranus RA 46.6474 (√2, peak +3), Moon Sky 46 at 14:40:25, Ceres RA 44 at 14:41:24, natal Uranus–Alphecca own link; now Uranus tuned to the Moon on Rahu–Capella (√2, 14:41:09) and Sun–Regulus (14:41:24).
  - JOANNA MASON MERCURY–RAHU: earlier N2 transit Mercury → her natal Rahu RA 37φ at 14:41:21 (during the race), and her natal Mercury–Alphecca 37φ; IV logged the sky Mercury–Pluto–Rahu 2:5 at 14:38:45. New: her own natal Mercury–Pluto–Rahu 2:5:7 = the full-triangle unison.
  - ORCUS / ERIS: winner's Orcus tuned to Mercury on Regulus–Vega (14:37:54); Joanna Mason's Orcus √2 on her Rahu–Fomalhaut tuned to the Moon in the race (14:40:24); her Eris UNISON with Sedna (RA 3:5:8 Castor–Deneb Algedi) — earlier Sedna → Eris Dec 160/9. Same carrier pair, different measure.
  - MAKEMAKE: earlier sky pair #3 Makemake/Betelgeuse, horse Makemake Type 1, Sun → horse Makemake Dec building; now the Moon parallel to his Makemake at 14:24:48 (outside every earlier window, which began at 14:30).
  - MARS–SATURN: detail sheet listed Mars/Saturn Dec 0.024 unread; IV had 1:2:3 at 14:39:06 and √2 at 14:40:44; now timed 14:39:09 / 14:40:39.
- IV and H1 already held most of the SKY chords (Mercury 2:5 Rahu–Pluto 14:38:45; Mercury Algorab–Alphecca 14:39:21; Moon Capella–Rigel 14:39:28; Rahu Betelgeuse–Capella 13:32:55; Sun 5:8 Mars–Antares 14:38:32; Pluto √2 Pallas–Bellatrix 14:40:55). What is new is tuning them to the natal charts (unison, full triangle) and the Moon on Sun–Regulus / Rahu–Fomalhaut.
- Precision on Algorab–Alphecca: the winning pair are TUNED (same base) but not in UNISON — H.Vesta 2:5:7, J.Neptune 1:8:9 vs Mercury 4:5:9. Joanna Mason's Saturn makes the same 4:5:9 on Algorab–Alphecca but in RA (0.019%).
- Only in the earlier work: 160/9 and 140/9 numbers, Haumea/Polaris link 98c, 73 natal pairs ≥90 (strongest imprint), 5-body Ninths groups, Antares–Saturn 3φ exact.

## 59. Ffos Las 17:25, 23 Mar 2022 (T32) — full read with the draft procedure (off 17:25:24, winning time 3m 56.81s, finish 17:29:21)
Result: 1st Ring The Moon 28/1 (Adam Wedge) · 2nd You Say Nothing 2/5F (Jack Tudor) · 3rd Time Leader 5/2 (Stan Sheppard) · 4th Yourholidayisover 22/1 (Tabitha Worsley). Outputs lattice/*_20220323_ffos_las_1725.txt.
STEP 1 imprint (blank-sheet, 3 Oct): VESTA carries 70/9 three ways (horse Castor–Vesta, jockey Sirius–Vesta, horse Vesta × jockey Castor); horse URANUS gets the #1 number (sky Venus → horse Uranus Dec 17.7780 = 160/9, culminating AT the off); horse Ketu–Polaris holds #4 inside; partnership whole-number group H Uranus–Mercury–Makemake–Rigel + J Jupiter; jockey Gonggong biggest hub.
MEETING POINTS:
1. THE MOON PARALLEL TO ADAM WEDGE'S NATAL VESTA (Dec −24.4889) at 17:19:11, 6 min before the off — the only Moon parallel/same-RA with any natal point in off±30, and the closest-in-time of any transit body to any natal point. Same Dec ⇒ 7 Moon star chords in UNISON with his Vesta: Dec 1:3:4 Algorab–Betelgeuse (natal 0.001%, Moon exact 17:21:02), Dec 4:5:9 Aldebaran–Alkaid (17:22:28), Dec 3:8:11 Aldebaran–Castor (17:27:56, during the race), plus Aldebaran–Fomalhaut, Betelgeuse–Regulus, Capella–Castor, Pleiades–Regulus. Vesta = the step-1 carrier body. Same mechanism as Catterick (Moon parallel to Wotever Next's Makemake 15 min before).
2. RING THE MOON'S URANUS: Moon RA 5:8:13 on Ceres–Juno exact 17:23:21 (2 min before the off), UNISON with his natal Uranus 5:8:13 on his own Ceres–Juno (0.008%) — only tight chart (You Say Nothing Rahu 0.134%, Yourholidayisover Mars 0.090%). Uranus = the step-1 #1-number body. (Catterick: the winner's Uranus also tuned to the Moon in the race.) Also Moon Dec 1:8:9 on Orcus–Polaris at the finish, UNISON with his Uranus (0.075%).
3. ADAM WEDGE'S URANUS √2 on Sirius–Spica (RA, 0.015%) tuned to the Moon's 1:2:3 on Sirius–Spica exact AT the off (17:25:22). (Jack Tudor Orcus 0.010% too.)
Other:
- Sky alone: Moon RA √2 Algorab–Arcturus exact 17:25:04 (20 s before the off) — tuned Time Leader Chiron 0.006%, Jack Tudor; Moon count 11–12 through the off (no big drop as at Catterick).
- FULL-TRIANGLE UNISON near the off: only Jack Tudor (beaten favourite's jockey) Mercury–Juno–Deneb Algedi Dec φ, sky exact 17:24:55, natal LOOSE 0.130%. Not the winning pair this time. Deneb Algedi again.
- Transit Mercury – natal Mercury – star: nothing for the winning pair near the off (Catterick had Wotever Next's at −25 s).
- Adam Wedge's Venus same body: Venus RA 1:7:8 on Transpluto–Altair exact 17:24:41 / his Venus φ (0.042%).
REPEATS WITH CATTERICK (kinds, not counts): (a) the Moon goes parallel to a winning-pair natal body that the earlier imprint work had picked out, minutes before the off, and makes UNISON chords through it; (b) the winning horse's Uranus tuned to the Moon around the race. NOT repeated: the winning jockey's own full-triangle unison; the transit–natal Mercury timing.

- §59 LAYER 1 in detail (6 Oct, Eddie: "I prefer it when we go layer by layer"): race-day group 23 Mar processed (g_20220323.csv: Ffos Las 16:15 W, Ludlow 16:40 B, Ffos Las 16:50 B, Ludlow 17:10 B, Ffos Las 17:25 B, Ludlow 17:40 B; Ffos Las 17:25 sky identical to the 96 file, max diff 1e-5).
  - Moon load 13 → PEAK 15 at off−6 to −4.5 (17:19–17:21, i.e. right as it reaches Adam Wedge's Vesta Dec at 17:19:11) → 10 at −2.5 → 12 at the off → 9 at +1.5. Other steps: Mars 7→8 at −2, Rahu 13→14 at −1.5, Sun 10→11 at the off.
  - Moon key chords: Dec 1:3:4 Algorab–Betelgeuse 17:21:02 (A. Wedge Vesta UNISON 0.001%, Ring The Moon Uranus 0.062%, Yourholidayisover Juno/Saturn); Dec 4:5:9 Aldebaran–Alkaid 17:22:28; RA √2 Algorab–Arcturus 17:25:04; RA 1:2:3 Sirius–Spica AT the off (A. Wedge Uranus √2 0.015%, Jack Tudor Orcus 0.010%); RA φ Algorab–Alphecca +1 min (nobody tuned); Dec 3:8:11 Aldebaran–Castor 17:27:56 in the race (A. Wedge Vesta UNISON, Yourholidayisover Vesta 0.013%).
  - Non-Moon star-base chords exact within 15 min: sparse; none tight for the winning pair before the off. After the race: Sun RA 1:3:4 Fomalhaut–Pleiades 17:30:26 (A. Wedge Sedna 0.013%), Mars RA 5:8:13 Altair–Deneb Algedi 17:30:48 (Ring The Moon Ketu 0.043%), Vesta RA 2:5:7 Alkaid–Vega 17:32:36 (Ring The Moon Uranus 0.048% — transit Vesta on the horse's Uranus, both imprint bodies).
  - Imprint meeting points in L1: Vesta (Moon parallel + 7 UNISON); horse Uranus (on the Moon's Algorab–Betelgeuse, and transit Vesta's Alkaid–Vega after the race); horse Ketu (Moon Pleiades–Regulus 0.032%); Gonggong none.

- §59 NODES LAYER (6 Oct): thin for this race.
  - Node chords on star bases (transit node + star pair vs natal node + star pair, stars at birth): only Adam Wedge J.Ketu on Dec Algol–Rigel (Rahu 5:6:11 exact 09:00, loose 0.085%); nothing for the horse; nothing near the off for anyone. Own Rahu+Ketu+point: none for either winning chart.
  - Node bases (node at one end, body third): the Moon RA 1:7:8 on Ketu–Betelgeuse exact 17:23:34 (1 min 50 s before the off; held −4.1 to +0.5) — Adam Wedge's natal Mercury φ on his own Ketu–Betelgeuse (0.011%); also Time Leader Gonggong 0.021%, Stan Sheppard Pallas 0.011%. Moon φ on Ketu–Bellatrix in the race (17:26:24) — Time Leader Pluto only.
  - Ring The Moon: UNISONs only loose/far (Ketu–Alphecca + Mercury 5:8:13, sky 18.7 h after; Rahu–Procyon + Pallas). Imprint touch, loose: his Uranus on Rahu–Polaris (φ, 0.132%; transit Juno 3:8:11 exact 10:33) — Polaris was in his Ketu–Polaris imprint.
  - Transit node to natal node (C, timing check only): Ketu – H.Rahu – Alphecca RA 2:5:7 exact 15:32; Rahu – H.Ketu – Aldebaran 13:22.

- §59 L2 (slow-body bases), 6 Oct:
  - Imprint meetings: Ring The Moon's URANUS (with Polaris, his Ketu–Polaris imprint): the Moon's Dec 1:8:9 on transit Orcus–Polaris comes IN during the race (17:26:34) — his Uranus makes the same 1:8:9 on his own Orcus–Polaris (UNISON, 0.075%, loose); also Jack Tudor Quaoar 0.035%, Tabitha Worsley Transpluto 0.026%. Adam Wedge's VESTA: Ceres 3:5:8 on Eris–Deneb Algedi exact 17:13:36 (12 min before) / his Vesta 4:5:9 0.014%.
  - √2 in the winning horse's own chart: his Venus √2 on his Haumea–Procyon (0.007%) — the Moon's RA 1:3:4 on transit Haumea–Procyon comes IN at 17:27:29, mid-race (shared: Stan Sheppard Venus 0.016%, Adam Wedge Neptune 0.020%). Natal Venus is a fast body, uncertain over the birth day.
  - Adam Wedge: Venus 1:7:8 on Transpluto–Altair exact 17:24:41 / his Venus φ (same body, 0.042%); Mercury 1:2:3 Quaoar–Aldebaran 17:19:17 / his Mars 0.023% (busy chord — Stan Sheppard UNISON 0.006%, six charts); Venus 3:8:11 Sedna–Rigel IN 17:24:39 / his Ketu √2 0.041% (also Time Leader Pallas 0.007%, Jack Tudor Jupiter 0.017%).
  - Ring The Moon before the window: Mars √2 on Chiron–Quaoar exact 17:14:45 / his Mercury φ 0.023%; Jupiter 1:5:6 Eris–Arcturus 17:18:29 / his Rahu 0.030%.
  - Against (L2): live √2 — Jack Tudor Mars on the Moon's √2 Gonggong–Polaris (IN 17:23:44, 0.014%); Tabitha Worsley Orcus UNISON (0.128%); Time Leader Gonggong on the Moon's √2 Pluto–Chiron (IN 17:28:44). Winning pair: none. No live same-note contest in L2. No full-triangle unison near the race.

- §59 L3 (Jupiter … Vesta bases), 6 Oct:
  - RING THE MOON'S URANUS on JUNO bases: the Moon RA 5:8:13 on Ceres–Juno exact 17:23:21 — his Uranus UNISON 0.008% (only tight chart); and his Uranus 4:5:9 on his own Juno–Fomalhaut (0.042%) is tuned to three transit chords on that base: Neptune φ exact 17:14:09, Jupiter φ IN 17:24:24 (45 s before the off), Eris 3:5:8 exact 17:30:09.
  - RING THE MOON'S RAHU, exact in his chart: Rahu 1:5:6 on his Jupiter–Algol (0.000%) — transit Ceres 3:8:11 on Jupiter–Algol exact 17:28:39, DURING the race (Jack Tudor Ceres loose 0.143%).
  - ADAM WEDGE'S ERIS on VESTA–DENEB ALGEDI: his Eris 4:5:9 (0.014%) — transit Mars 3:8:11 on Vesta–Deneb Algedi comes IN 17:24:59 (25 s before the off; exact 17:32:54). Vesta + Deneb Algedi again. Also his Eris UNISON φ on Pallas–Capella with Mars (exact 17:15:24, 0.045%); his Quaoar wins the same note on Mars–Aldebaran + Gonggong 1:4:5 (0.023% vs Stan Sheppard 0.066%; the chord goes OUT 17:27:44 in the race).
  - The favourite pair both UNISON on Vesta–Aldebaran + Mercury φ (exact 17:18:39; You Say Nothing Venus 0.037%, Jack Tudor Mars 0.033%) — fast natal bodies (Venus/Mars of the horse uncertain over the birth day).
  - Against (L3): Jack Tudor Quaoar on the Moon's Dec √2 Pallas–Betelgeuse in the race (0.007%). Winning pair none.

- §59 L4 (Sun, Mercury, Venus, Moon bases), 6 Oct:
  - SUN–MOON–ALPHECCA: the Moon sits at the Dec midpoint of the Sun and Alphecca (1:1:2), held from 17:21:07 right through the race (exact 17:35:08). Ring The Moon tuned on his own Sun–Alphecca: Eris 3:5:8 (0.005%) and Venus 1:4:5 (0.013%). Cf. Catterick's Sun–Moon–Regulus (Eddie's pick). Others on it looser (Jack Tudor Sedna 0.041%, Adam Wedge Ceres 0.052%).
  - ADAM WEDGE: Venus–Transpluto–Altair — sky RA 1:7:8 exact 17:24:41 (43 s before the off) and in his chart the same three points make φ (0.042%): same three points, different chord (seen from the L2 side too). The Moon RA 3:4:7 on Venus–Spica comes IN 17:27:34 during the race / his Chiron 2:5:7 (0.010%; You Say Nothing Gonggong 0.050%).
  - RING THE MOON before the off: Gonggong 1:6:7 on Mercury–Alphecca exact 17:16:09 / his Pallas 0.021% (Alphecca again); Eris 3:5:8 on Mercury–Capella 17:20:24 / his Haumea 0.029%. Just after: Vesta 1:3:4 on Mercury–Equator 17:31:37 / his Mars UNISON 0.015%.
  - Against (L4): the Moon's √2 on Sun–Arcturus (shared: Ring The Moon Transpluto 0.037%, You Say Nothing Chiron 0.027%) goes OUT 17:28:39, before the finish; Jack Tudor's Sun on the Moon's √2 Venus–Equator, IN 17:25:04 (0.012%), with Time Leader's Eris √2 in UNISON (0.061%).

- §59 L5 side note (fast points), 6 Oct: ~2,900 fast-point chords exact to 0.02% between off−2 and the finish (1,742 during the race) — about eight a second, so colour only. Around this race's key triangles:
  - SUN–MOON–ALPHECCA: the VERTEX joins all three within 6 s a minute into the race — Vertex–Alphecca + Sun Dec 1:3:4 (17:26:21), Vertex–Moon + Sun Dec 1:2:3 (17:26:24), Vertex–Alphecca + Moon Dec 1:2:3 (17:26:27); earlier Part of Spirit–Alphecca + Sun RA 5:8:13 (17:24:23), Ascendant–Alphecca + Moon (17:24:37). (Catterick: the Midheaven joined Sun–Moon–Regulus at the start of the race.)
  - VESTA–DENEB ALGEDI (Adam Wedge's Eris base): Part of Spirit–Deneb Algedi + Vesta RA 3:4:7 at 17:25:26 (2 s after the off); Midheaven–Deneb Algedi + Vesta 17:26:33; Vertex 17:24:09.
  - VENUS–TRANSPLUTO–ALTAIR (Adam Wedge's triangle): Ascendant–Transpluto + Venus 17:24:19; Part of Spirit–Altair + Venus √2 17:24:22; Midheaven–Transpluto + Venus Dec 1:2:3 at 17:29:16 (5 s before the finish).
  - CERES–JUPITER–ALGOL (Ring The Moon's Rahu chord in the race): Midheaven 17:25:41, Part of Fortune 17:25:44 / 17:26:50, Vertex 17:28:25.
  - MOON–CERES–JUNO (Ring The Moon's Uranus): Part of Spirit–Ceres + Juno 17:25:12 (12 s before the off); Ascendant/Part of Fortune with Juno + Moon in the race.

## 61. Newcastle AW 13:30, 2 Jan 2022 (R21) — off 13:32:49, winning time 58.95s, finish 13:33:48
Result: 1st Venturous 25/1 (Connor Beasley) · 2nd Mondammej 4/1 (Cam Hardie) · 3rd Good Effort 2/5F (Jim Crowley) · 4th Regional 7/1 (Daniel Tudhope) · 5th King Of Stars 22/1 (Jason Watson). Outputs lattice/*_20220102_newcastle_aw_1330.txt. (Minute file runs to sched+30 = off+27.)
Step 1 imprint (blank-sheet): the repeated number 23√2 held only by Venturous, via horse Gonggong × jockey Vesta; #12 lands alone on the jockey's Saturn; busiest Ceres pairs on the horse's Chiron; Juno → jockey Orcus hub peaking at the off.
- LAYER 1 (6 Oct):
  - NO Moon crossing: the Moon reaches no natal point's Dec or RA in the hour. The Moon is near its southern Dec limit (−27.31, moving ~0.0004°/min), so its Dec chords hold the whole hour. The strongest repeat of the first two races does NOT appear here.
  - The Moon's Dec √2 on Algol–Polaris (held all hour): tightest charts Venturous Jupiter (0.005%) and Rahu (0.020%) — the winning horse tuned to the Moon's discord (held, not live).
  - The Moon RA 4:5:9 on Algorab–Castor comes in 13:29:14 (3.6 min before the off): Mondammej (2nd) URANUS in UNISON (0.010%) — the horse-Uranus-to-the-Moon shape goes to the runner-up here; Venturous Eris 0.033%.
  - Connor Beasley: Moon Dec 3:8:11 Castor–Spica (held through) / his Uranus 0.010% (only him); Moon Dec 3:8:11 Alphecca–Regulus / his Ceres 0.009% (tightest; Jason Watson Saturn UNISON 0.012%); Jupiter Dec 1:5:6 Betelgeuse–Deneb Algedi exact 13:34:37 (49 s after the finish) / his Haumea 0.008% (only him; his Haumea also UNISON with Makemake on that base).
  - Venturous: Mercury Dec 1:4:5 Capella–Rigel exact 13:37:57 / his Vesta 0.010% (only him). Capella again.
  - Imprint meetings in L1: weak — horse Vesta (above); jockey Orcus UNISON with Neptune on Procyon–Rigel (natal 0.001%, sky exact 4.7 h later); Saturn/Gonggong only far or loose.
  - Note: Connor Beasley also rode Tea Garden (4th) at Catterick 14:40.

- §61 NODES (6 Oct): quiet for the winning pair.
  - Star bases: neither Venturous nor Connor Beasley has a natal node tuned to a transit node chord. Transit Ketu RA 1:4:5 on Arcturus–Procyon exact 13:09:55 (23 min before the off) carries Connor Beasley's Sedna √2 (0.008%) — a Layer-1 tuning, not his nodes. Only UNISON near anything: Jason Watson (5th) Ketu 3:8:11 with Rahu on Aldebaran–Bellatrix (exact 15:27).
  - Node bases: Venturous only a loose same-body (Ketu–Procyon + Transpluto, days away); Connor Beasley Rahu–Fomalhaut + his Juno with Pluto (0.027%, sky 9.7 h later) and Ketu–Altair √2 UNISON with Transpluto (loose, 9.8 h later). Nothing on node bases near the off except Mercury on Ketu–Spica 13:26:18 (Daniel Tudhope, loose). No Moon on node bases in the window.
  - Transit node to natal node: Rahu – J.Rahu – Regulus RA 4:5:9 exact 08:38 (0.018%) — morning.

- §61 L2 (slow-body bases), 6 Oct:
  - The Moon's L2 chords held in the race (59 s): Dec 2:5:7 on Sedna–Makemake — Venturous Juno 4:5:9 (0.003%) the tightest of nine charts; Dec 1:2:3 on Sedna–Quaoar — Connor Beasley Venus 3:5:8 (0.009%; Daniel Tudhope Ceres 0.006% tighter); RA 5:6:11 on Chiron–Capella — Connor Beasley Jupiter (0.031%, base lengths 9/8; Capella again); RA 1:5:6 on Eris–Algol — Mondammej Rahu UNISON 0.011% (2nd), Venturous Mars √2 (uncertain body).
  - Mercury just after the race: RA 4:5:9 on Gonggong–Quaoar exact 13:36:19 (3.5 min after the off) / Connor Beasley Uranus φ 0.009%; RA 2:3:5 on Eris–Bellatrix 13:44:17 / Venturous Transpluto 0.005%.
  - Before: Haumea 1:8:9 on Transpluto–Antares exact 12:50:12 / Venturous Pallas 1:1:2 at 0.000% (Pallas exactly midway between his Transpluto and Antares in Dec). Mercury 3:8:11 on Sedna–Arcturus 13:04:28 / Connor Beasley ORCUS (imprint hub) 0.036%.
  - Imprint meetings in L2: weak (horse Gonggong, jockey Vesta, jockey Saturn only hours away; jockey Orcus 28 min before).
  - AGAINST (L2): the WINNING HORSE is caught on live discord — Venturous Uranus 5:6:11 on Mercury's Dec √2 Orcus–Deneb Algedi, which comes IN at 13:32:24 (25 s before the off; exact 13:35:44) — first time in three races; Daniel Tudhope (4th) Makemake √2 in UNISON. Deneb Algedi again.

- §61 L3 (Jupiter … Vesta bases), 6 Oct:
  - The Moon in the window: Dec 1:7:8 on Saturn–Sirius — Venturous NEPTUNE 2:5:7 at 0.002% (tightest; King Of Stars Vesta 0.009%); Dec 5:8:13 on Jupiter–Regulus — Venturous Eris same chord (UNISON, loose 0.097%) and Rahu 1:3:4 (0.029%); RA φ on Ceres–Antares in the race — Connor Beasley Haumea 0.030% (Daniel Tudhope Venus 0.018%, King Of Stars Pallas 0.015% tighter).
  - 3.3 min before the off (13:29:34): Neptune 1:3:4 on Jupiter–Deneb Algedi — Venturous Uranus 0.043% (Deneb Algedi again); Neptune √2 on Jupiter–Mars — King Of Stars Saturn √2 UNISON 0.022%, Mondammej Pluto √2 UNISON (loose).
  - Connor Beasley's ORCUS (imprint hub) 3:5:8 on his own Ceres–Betelgeuse (0.004%): transit Neptune 1:2:3 on Ceres–Betelgeuse exact 13:42:37, ~9 min after the finish.
  - Venturous's Pallas: Uranus 1:5:6 on Saturn–Altair exact 13:04:01 (0.005%); Jupiter φ on Saturn–Fomalhaut 13:47:30 (0.014%).
  - Against (L3): nothing on the winning pair.

- §61 L4 (Sun, Mercury, Venus, Moon bases), 6 Oct:
  - Bases with the Moon at one end carry no natal side (no natal Moon) — the Moon only tunes as the third point.
  - The Moon RA 2:3:5 on Mercury–Venus, held to 13:32:54 (goes OUT 5 s after the off): Venturous JUNO 2:3:5 — the only UNISON (0.075%); Jim Crowley Orcus √2 0.003% (his own √2), Daniel Tudhope Saturn 0.022%, King Of Stars Rahu 0.014%.
  - Uranus RA 3:5:8 on Venus–Sirius exact 13:20:05 (12.7 min before): Venturous JUNO 5:8:13 0.024% (tightest; King Of Stars Juno √2 0.037%). Venturous's Juno twice at L4.
  - Chiron Dec 1:8:9 on Sun–Antares (slow, holds): Venturous NEPTUNE 4:5:9 0.009% tightest — his Neptune again (tightest on the Moon's Saturn–Sirius at L3).
  - Haumea RA 1:3:4 on Mercury–Ketu: Venturous Mars 5:6:11 0.021%, base lengths almost the same (ratio 1.017).
  - The Moon RA 1:2:3 on Mercury–Alphecca in the race: Venturous Pluto loose (0.117%); Good Effort's base lengths match (1.003) but loose.
  - Good Effort: Pallas 1:2:3 on Mercury–Alkaid exact 13:30:20 (2.5 min before) — his Venus UNISON, base lengths the same (1.002), loose 0.115%. His natal Mercury bases match the sky's lengths on four stars (ratio 1.002–1.003).
  - Connor Beasley: only slow √2 UNISONs (Saturn on Sun–Spica with his Makemake; Neptune on Sun–Betelgeuse with his Jupiter), exact hours away — background.
  - AGAINST (L4): Jim Crowley (favourite's jockey) caught — Orcus √2 on Mercury–Deneb Algedi comes IN 13:32:24, his Eris 1:7:8 0.042%. This is the SAME three points (Mercury, Orcus, Deneb Algedi) as the L2 discord that caught Venturous's Uranus at the same second, read from the other base. Daniel Tudhope Mars φ UNISON on Venus–Deneb Algedi + Mercury comes in 13:31:49 (0.009%).
- §61 L5 (fast points, side note only), 6 Oct: ~1,300 fast-point chords in the window — colour only.
  - Vertex joins Orcus–Deneb Algedi (the discord pair) RA 2:5:7 at 13:32:48, 1 s before the off.
  - Uranus–Sirius (Venturous Juno's Venus–Sirius chord): Part of Fortune 13:32:19, Part of Spirit 13:32:37, then Ascendant 13:33:28 and Vertex 13:33:36 in the race.
  - Saturn–Sirius (the Moon's L3 chord, Venturous Neptune): Part of Spirit 13:32:45, 4 s before the off.
  - Jupiter–Neptune (L3 Neptune on Jupiter's bases): Ascendant 13:31:01, Midheaven 13:31:10 and 13:31:39, Part of Spirit 13:31:27, Vertex 13:33:35 in the race.
  - Moon–Mercury: Vertex 13:32:22, Midheaven 13:32:33; Moon–Saturn: Midheaven 13:32:36.
  - At the off second: Part of Spirit–Gonggong–Pluto RA 2:5:7 (0.0001%) — Gonggong is the horse's imprint body; Part of Fortune–Jupiter–Saturn 1:5:6; Ascendant–Midheaven–Neptune 5:8:13. At the finish (13:33:47): Part of Fortune on Algol–Gonggong 4:5:9.

## 60. THE 'AGAINST' CHECK (Eddie 6 Oct: "in a 4 runner race maybe the other runners are negatively affected") — lattice/against.py → AG_<race>.txt
- Every runner, every layer (dumps in lattice/dump/). Only LIVE sky chords (exact between off−2 and the finish, or coming in / going out then); slow chords that just hold are left out. Natal side within 0.05% (UNISON 0.15%). A discord = sky chord is the √2 division; B same note = two+ runners in UNISON with one sky chord, who is tighter; C in/out.
- FFOS LAS 17:25: discord falls on the BEATEN FAVOURITE'S JOCKEY — Jack Tudor tuned to 5 live √2 sky chords (of 11 in the race): the Moon's RA √2 Algorab–Arcturus (exact 17:25:04; his Venus 0.039%, Transpluto 0.034%; goes OUT 17:29:14, 7 s before the finish), the Moon's Dec √2 Venus–Equator (IN 17:25:04; his Sun 0.012%), the Moon's RA √2 Gonggong–Polaris (IN 17:23:44; his Mars 0.014%), the Moon's Dec √2 Pallas–Betelgeuse in the race (his Quaoar 0.007%). Adam Wedge 0; Ring The Moon 1 (Moon √2 Sun–Arcturus, Transpluto 0.037%, shared with You Say Nothing Chiron 0.027%); Time Leader 3.
- Same note (only one live): Mars–Aldebaran + Gonggong Dec 1:4:5 — Adam Wedge Quaoar 0.023% > Stan Sheppard Chiron 0.066%.
- In/out does not separate (Adam Wedge's Vesta chords go OUT during the race as the Moon leaves his Vesta's Dec).
- CATTERICK 14:40 for comparison: discord — Wotever Next 0, Jason Hart 0, Beluga Gold 1 (Makemake on Pluto √2 Pallas–Bellatrix), Joanna Mason 1 but as UNISON (her own Saturn √2 = the sky's √2), Dougie Costello 3 (Mars–Saturn–Deneb Algedi √2), Thakuri 2, Connor Beasley/David Allan 1 (Moon √2 Arcturus–Castor). Same note (only one live): Mercury–Pluto–Rahu 2:5:7 — Joanna Mason 0.001% > David Allan 0.140%.
- WHAT I SEE (two races): the only live same-note contest in each race goes to the winning JOCKEY. The winning horse is caught by no live √2 discord in either race. Discord falls on beaten runners (Catterick: 3rd and 5th; Ffos Las: the favourite's jockey heavily). Being IN UNISON with a √2 (own natal √2) may be a different thing from being caught on someone else's √2 — keep apart.

## EDDIE'S PICKS — Catterick 14:40 (6 Oct 2026)
- SUN–MOON–REGULUS: RA Sun–Regulus base, the Moon makes 4:5:9 during the race (14:41:24); only Wotever Next tuned (natal Uranus 1:8:9 0.011%, base lengths almost equal).
- MERCURY–PLUTO–RAHU: Joanna Mason's own natal Mercury–Pluto–Rahu RA 2:5:7 (0.001%) comes round in the sky as the same chord 85 s before the off (14:38:44); no other chart has anything like it near the race.

## TO LOOK AT LATER (Eddie, 5 Oct 2026)
- **Fast points, Dec only (Eddie 6 Oct 14:09–14:11):** "in the fast points do you think that dec is better as more slow" — fast-point Dec moves 3–10× slower than RA (Dec 0.02–0.15°/min vs RA 0.15–0.37°/min), but Dec gives as many chords (Doncaster ~1,500 Dec vs ~1,270 RA). Possible filter: Dec only + chords held longest. Parked — "maybe the fast parts will be clearer when we know more about the slower pieces".
- **Deneb Algedi with Ketu in the Pholas win** — Lingfield AW 02/04/2021 14:35, Pholas 25/1 with Hollie Doyle (the original PINPOINT worked example). Eddie has seen Deneb Algedi associated with Ketu there. Look at it alongside the 6 Apr 2022 Mars–Saturn conjunction on Deneb Algedi (Catterick 14:40, Wotever Next 33/1), Mercury's √2 chord on Algol–Deneb Algedi at that off, and the 8 Jul Moon equidistant Deneb Algedi/Sirius.

## 62. Doncaster 14:40, 18 Mar 2022 (R29) — off 14:40:41, winning time 4m 7.70s, finish 14:44:49
Result: 1st Olympe De Gouges 25/1 (David Noonan) · 2nd Oot Ma Way 5/6F (Conor O'Farrell) · 3rd Poetria 15/8 (Jamie Hamilton) · 4th Fiamette 5/1 (James Davies) · 5th Suntory Star 80/1 (Stephen Mulqueen). Outputs lattice/*_20220318_doncaster_1440.txt.
Step 1 imprint (blank-sheet #4): busiest body VESTA (jockey Vesta hub; horse Eris–Vesta carries the repeated 130/9); jockey NEPTUNE the receiver (three Vesta pairs alone); jockey SEDNA the biggest natal hub; horse Uranus takes #2 alone; Orcus in both charts (φ⁶); Saturn in both charts.
- LAYER 1 (6 Oct):
  - FULL MOON day (Moon RA ~183 opposite the Sun ~358; Moon Dec +2.4 → +2.2, near the equator; Sun near the equator, equinox 20 Mar). NO Moon crossing of any natal point's Dec or RA in the hour (second race running).
  - AT THE OFF (14:40:41): Mars RA 1:6:7 on Altair–Arcturus exact (0.003%) — ONLY Olympe De Gouges tuned: his natal Sun φ (0.017%) and his Mars (same body, loose 0.096%). Juno φ on the same base exact 14:35:17 (0.008%) — again only his Sun.
  - AT THE OFF: Pallas RA 2:3:5 on Altair–Fomalhaut exact (0.000%) — shared: David Noonan Makemake (loose 0.047%), Oot Ma Way Vesta 0.014%, Fiamette Mars 0.012%, James Davies Neptune.
  - The Moon Dec 3:4:7 on Betelgeuse–Procyon exact 14:38:20 (2.4 min before): Olympe De Gouges CHIRON 5:8:13 0.004% (tightest; Poetria Makemake 0.005%) AND David Noonan CHIRON φ — both winning charts' Chiron; Jupiter 1:5:6 on the same base later (15:22).
  - The Moon Dec 4:5:9 on Algol–Polaris exact 14:36:00, held through the race: David Noonan SEDNA (imprint hub) 3:4:7 0.004% (Poetria Transpluto 0.001% tighter; James Davies Sun, Jupiter).
  - The Moon Dec 1:3:4 on Algol–Regulus exact 14:37:29: David Noonan SATURN 5:8:13 0.022% (tightest) and Orcus 0.052%.
  - The Moon Dec 1:5:6 on Alphecca–Bellatrix exact 14:43:55 (in the race): David Noonan's own VENUS √2 (0.027%) met by an ordinary chord (Fiamette Neptune 0.009%, Jamie Hamilton Neptune tighter). Alphecca again.
  - Sun Dec 2:3:5 on Alkaid–Arcturus exact 14:42:56 (in the race): David Noonan NEPTUNE (imprint receiver) 3:4:7 0.016% (Poetria Eris √2). Sun 3:5:8 on Procyon–Spica exact 14:52:18: David Noonan Neptune UNISON (0.017%).
  - Sun Dec 1:1:2 (midpoint) on Bellatrix–Rigel exact 14:42:45 (in the race): Olympe De Gouges Pallas 0.038% (Jamie Hamilton Quaoar 0.005% tighter).
  - Pallas Dec √2 on Altair–Equator exact 14:31:41: David Noonan Haumea √2 UNISON (0.019%).
  - Juno 3:4:7 on Antares–Deneb Algedi exact 14:46:05: Olympe De Gouges Eris UNISON (loose 0.058%). Deneb Algedi.
  - Horse Uranus: only on the Moon's Flat φ on Betelgeuse–Procyon (exact 14:26:36, out 14:36:06) 0.038%, before the window.
  - Vesta (busiest imprint body): weak at L1 (horse Vesta same body on Alphecca–Castor, loose; Vesta exact 14:08).
- §62 NODES (6 Oct): quiet for the winning pair, as at Newcastle and Ffos Las.
  - Transit node + star pair against natal node + star pair: neither Olympe De Gouges nor David Noonan tuned (only Oot Ma Way, Fiamette, James Davies, Suntory Star — all hours or days away, loose).
  - Node bases: the Moon Dec 3:5:8 on Rahu–Capella during the race (14:43:56): Olympe De Gouges Makemake 3:8:11 0.019% — but the favourite Oot Ma Way's Orcus 1:1:2 is tighter (0.016%, base lengths nearly the same 1.016). Capella again.
  - Mercury Dec 5:6:11 on Rahu–Bellatrix exact 14:30:02 (10.7 min before): Olympe De Gouges Venus 3:5:8 0.015% (Fiamette Orcus 0.010% tighter; shared by five charts).
  - David Noonan: nothing near the off (Rahu–Procyon and Ketu–Aldebaran only, hours away, loose).
  - For the 'against' check later: the Moon's Dec √2 on Ketu–Castor, held during the race (14:44:41) — the favourite horse Oot Ma Way tuned (Mercury 0.010%, base lengths almost the same 1.009; Transpluto √2 UNISON).
- §62 L2 (slow-body bases), 6 Oct:
  - The Moon on ERIS bases during the race, Olympe De Gouges tightest: Dec 1:7:8 on Eris–Alphecca (14:42:56) — horse PALLAS 1:2:3 0.010% (next 0.074%; Alphecca again); Dec 1:5:6 on Eris–Ketu (14:42:41) — horse SEDNA √2 0.013% (only chart; his own √2 met by an ordinary chord); RA 3:8:11 on Eris–Aldebaran (14:44:41) — horse Juno 0.056% (Oot Ma Way Sedna 0.016% tighter), Juno itself 5:8:13 on that base 14:28:01 (same body).
  - Mercury RA 3:5:8 on Haumea–Altair exact 14:38:15 (2.4 min before): Olympe De Gouges SUN φ 0.022% tightest (Poetria Mercury 0.026%). Altair again, the horse's Sun again (L1 Mars/Juno on Altair–Arcturus).
  - The Moon Dec 5:6:11 on Haumea–Alphecca held to 14:38:41: David Noonan NEPTUNE (imprint receiver) 1:8:9 0.023% tightest, and his Makemake UNISON 0.058%.
  - Mercury RA 1:3:4 on Orcus–Castor exact 14:41:04 (23 s after the off, 0.000%): David Noonan JUNO 0.022% tightest (Stephen Mulqueen 0.047%).
  - Saturn Dec 1:8:9 on Neptune–Polaris exact 14:28:01: David Noonan Haumea 0.015% (only chart).
  - The Moon at the Orcus–Aldebaran Dec midpoint (1:1:2) around 14:39:56: David Noonan Mars 0.041% (Jamie Hamilton Uranus 0.021% tighter).
  - Horse Uranus: the Moon's 1:2:3 on Eris–Rigel in the race (14:41:26) — UNISON but loose (0.104%); Suntory Star Uranus same chord 0.094%.
  - For the 'against' check: the Moon's Dec √2 on Sedna–Aldebaran in the race (14:43:56) — Olympe De Gouges Ketu 0.008% tightest (and Venus 0.032%); the Moon's Dec √2 on Uranus–Pleiades in the race (14:44:26) — David Noonan Chiron 0.041% tightest.
- §62 L3 (Jupiter … Vesta bases), 6 Oct: lighter than L1/L2.
  - The Moon Dec 1:3:4 on Jupiter–Juno held to 14:39:11 (1.5 min before the off): Olympe De Gouges NEPTUNE 1:5:6 0.024% tightest (Suntory Star Vesta 0.035%); his Chiron too (0.055%).
  - Transpluto on Jupiter–Spica exact 14:10:44: Olympe De Gouges GONGGONG φ 0.004% tightest (30 min before).
  - Haumea RA 1:5:6 on Jupiter–Pallas exact 14:38:41 (2 min before): only Olympe De Gouges tuned (Eris 1:7:8, loose 0.074%).
  - Gonggong RA 2:3:5 on Pallas–Vega exact 14:47:41: horse Jupiter φ 0.027% (James Davies 0.004%, Jamie Hamilton 0.017% tighter).
  - Sun RA 1:2:3 on Juno–Rigel exact 14:44:41 (8 s before the finish): Olympe De Gouges Ceres UNISON 0.054% (Suntory Star Ceres UNISON 0.019% tighter).
  - David Noonan: Ceres 1:6:7 on Jupiter–Arcturus and Jupiter on Ceres–Arcturus, exact 14:24:16 — the sky's Jupiter–Ceres–Arcturus triangle; his natal Jupiter–Ceres–Arcturus make 4:5:9 (0.042%) — same three points, different chord (like Adam Wedge's Venus–Transpluto–Altair at Ffos Las). The Moon Dec 2:3:5 on Mars–Aldebaran at −0.25 min: his Orcus 0.041% (Jamie Hamilton Pluto 0.002% tighter).
  - VESTA (the busiest imprint body) on Regulus: Vesta √2 on Pallas–Regulus exact 14:37:56, and the Sun √2 on Vesta–Regulus exact 14:40:26 (15 s before the off) — for the 'against' check: Oot Ma Way (fav) Saturn 0.080% (base lengths 1.038), David Noonan Sedna 0.100%, Fiamette Pluto — all loose.
- §62 L4 (Sun, Mercury, Venus, Moon bases), 6 Oct:
  - SUN–STAR CHORD HELD BY THE MOON IN THE RACE: the Moon Dec 5:8:13 on Sun–Betelgeuse (14:43:41) — Olympe De Gouges QUAOAR 1:6:7 0.021% tightest (Stephen Mulqueen 0.029%; David Noonan Ceres 0.064%). Saturn φ on Sun–Betelgeuse (RA) exact 14:33:56 — Olympe De Gouges Ceres UNISON 0.012% (the only UNISON; others tighter on other chords). Sun–Betelgeuse twice for the horse. (Catterick Sun–Regulus, Ffos Las Sun–Alphecca, now Sun–Betelgeuse.)
  - Sun–Regulus (Catterick's Sun–star): the Moon Dec 1:3:4 at 14:39:11 and Vesta √2 at 14:40:26 — the favourite Oot Ma Way Makemake tightest (0.042%); Olympe De Gouges Neptune loose (0.149%).
  - AT THE OFF: Chiron Dec 1:2:3 on Sun–Venus exact 14:40:41 (0.000%) — winning pair NOT tuned; the favourite pair is (Conor O'Farrell Ketu 0.019%, Oot Ma Way Saturn 0.026%).
  - David Noonan: the Moon Dec 1:6:7 on Venus–Procyon at 14:40:56 (15 s after the off) — his TRANSPLUTO φ 0.001% tightest (James Davies 0.019%), his Saturn UNISON (loose 0.120%); Saturn RA 2:3:5 on Venus–Altair exact 14:37:12 — his Jupiter at the midpoint (1:1:2, 0.013%); Jupiter 2:3:5 on Venus–Fomalhaut (14:14) — his Neptune UNISON 0.028%, the horse's Saturn 0.021% on the same base.
- §62 L5 (fast points, side note only), 6 Oct: ~2,900 fast-point chords in the window — colour only.
  - Mars–Altair (the L1 chord at the off, Mars 1:6:7 on Altair–Arcturus): Vertex 14:40:04; Part of Fortune 14:41:57; MIDHEAVEN–Altair + Mars RA 1:6:7 at 14:42:47 (0.0004%) — the same chord type as at the off, with the Midheaven in Arcturus's place.
  - Sun–Betelgeuse (L4, horse Quaoar/Ceres): Part of Fortune 14:39:01; Ascendant 14:41:00, 14:42:01, 14:42:56; Midheaven √2 14:43:06 — all in the race.
  - Eris–Alphecca (L2 Moon, horse Pallas): Part of Fortune 14:39:05; Midheaven 14:41:39, Ascendant 14:41:59, Part of Spirit 14:42:59 in the race. Eris–Ketu (horse Sedna √2): Part of Spirit 14:44:08.
  - Haumea–Altair (L2 Mercury, horse Sun): Part of Fortune 14:39:30, 14:42:24; Vertex 14:42:42.
  - Jupiter–Ceres (David Noonan's triangle): Midheaven √2 14:39:09, Part of Fortune 14:39:19, Part of Spirit 14:40:46 (5 s after the off).
  - At the off second: Midheaven–Sun–Neptune 1:5:6; Part of Spirit–Capella–Jupiter 1:3:4; Ascendant–Sirius–Ceres 4:5:9. At the finish: Vertex–Moon–Neptune 5:8:13.
- §62 AGAINST (all layers), 6 Oct — lattice/AG_20220318_doncaster_1440.txt:
  - DISCORD (live √2): the FAVOURITE HORSE Oot Ma Way the most — the Moon's Dec √2 on Ketu–Castor comes IN 14:40:31 (10 s before the off; his Mercury 0.010%, his Transpluto √2 UNISON 0.082%), held through the finish to 14:49:22 [corrected 8 Oct: tightest 14:44:57, 0.0001%; 0.144% at the off, 0.005% at the finish – helper recheck second by second]; Vesta √2 on Sun–Regulus exact 14:40:26 (his Makemake 0.042%). Conor O'Farrell 0.
  - The WINNING HORSE caught again (second race running): the Moon's Dec √2 on Sedna–Aldebaran comes IN 14:41:41 (1 min into the race), exact 14:43:51 — Olympe De Gouges Ketu 0.008% (only tight chart) and Venus 0.032%. David Noonan: the Moon's √2 on Uranus–Pleiades IN 14:39:51 (his Chiron 0.041%).
  - Poetria (3rd) Eris 0.003% on the Moon's √2 on Haumea–Algorab — goes OUT 14:39:46, before the off (shared with Suntory Star, Stephen Mulqueen).
  - SAME NOTE (three live): Eris–Rigel + Moon 1:2:3 (horse Uranus) — Suntory Star 0.094% > Olympe De Gouges 0.104% > Fiamette; Juno–Rigel + Sun 1:2:3 (Ceres) — Suntory Star 0.019% > Olympe De Gouges 0.054%; Aldebaran–Regulus + Venus — Stephen Mulqueen > Oot Ma Way. The winning pair wins none (David Noonan in none). Not repeated from Catterick / Ffos Las.
  - In/out: does not separate.

## 63. Carlisle 13:55, 14 Oct 2021 (R9) — off 13:57:10, winning time 3m 56.10s, finish 14:01:06
Result: 1st Arvico Bleu 25/1 (Callum Bewley) · 2nd Gold Des Bois EvensF (Conor O'Farrell) · 3rd Slanelough 4/1 (Craig Nichol) · 4th If Not For Dylan 11/1 (Sam Coltherd) · 5th Finisk River 5/2 (Brian Hughes). Outputs lattice/*_20211014_carlisle_1355.txt. Conor O'Farrell also rode the beaten favourite at Doncaster 14:40.
Step 1 imprint (blank-sheet #5): MAKEMAKE leads both charts (horse hub; jockey hub; sky Makemake → horse Orcus); the #1 pair Arcturus/Jupiter held inside and alone by the jockey (1+√2); the busiest body Mercury strikes the horse's PLUTO, peaking at the off; horse HAUMEA hub struck by Neptune; 40/9 and 100/9 families carried by both.
- LAYER 1 (6 Oct):
  - NO Moon crossing (third race running). Moon near its southern Dec (−23.3, slow).
  - The Moon Dec 3:4:7 on Regulus–Rigel, exact 13:43:10, held until 14:00:35 (into the race): Arvico Bleu VESTA 0.000% — tightest in the field (Brian Hughes Makemake 0.016%, Conor O'Farrell Gonggong 0.018%); his Neptune too (0.048%).
  - THE MOON IN THE RACE: RA 1:2:3 on Altair–Fomalhaut — comes in 13:58:00, exact 13:59:25, out 14:00:55 (entirely inside the race): Arvico Bleu SATURN in UNISON (1:2:3, 0.012%) — the only tight UNISON (Finisk River Vesta 0.005% on another chord; Brian Hughes Vesta UNISON loose 0.133%); his Pluto (imprint) 0.059% too. ALTAIR again (Doncaster: Mars on Altair–Arcturus at the off).
  - Mercury Dec 5:6:11 on Algorab–Spica exact 13:57:59 (49 s after the off): Arvico Bleu's own ERIS √2 (0.046%) met by an ordinary chord (Craig Nichol Juno 0.022% tighter).
  - Callum Bewley: Venus Dec 2:3:5 on Altair–Spica exact 13:51:19 (6 min before) — his JUNO 0.001% tightest (Altair again). Moon chords loose for him (Gonggong 0.026% on Capella–Polaris, exact 14:25).
  - Favourite Gold Des Bois: Rahu 0.006% on the Moon's 4:5:9 Alphecca–Polaris (exact 13:47, held all hour).
  - Imprint meetings in L1: horse Vesta and Saturn above; horse Pluto on the Moon's Altair–Fomalhaut (loose); Makemake (both charts) and the jockey's Arcturus–Jupiter: nothing near the off.
- §63 NODES (6 Oct): quiet near the off again.
  - Transit node + star pair against natal node + star pair: Arvico Bleu only loosely (Ketu on Algol–Fomalhaut, days away); Callum Bewley none. The favourite pair has the most here (Gold Des Bois 3, Conor O'Farrell Ketu φ 0.003% — all hours or days away).
  - Node bases: sky MAKEMAKE (the imprint body leading both winning charts) Dec 3:4:7 on Rahu–Pleiades (0.009%) — Arvico Bleu's Quaoar 1:7:8 0.006% tightest (Sam Coltherd Sun 0.021%). Slow chord (holds for days; the 13:31:49 exact is arithmetic).
  - The Moon RA 1:2:3 on Rahu–Castor at 13:57:25 (15 s after the off): Conor O'Farrell (fav jockey) Eris 0.014% — the favourite's side.
  - The Moon Dec 3:5:8 on Ketu–Deneb Algedi in the race: Craig Nichol (3rd) Mercury, Sedna, Transpluto; Sam Coltherd. Deneb Algedi + Ketu again (Pholas lead) — on the 3rd's jockey, not the winner.
- §63 L2 (slow-body bases), 6 Oct: modest.
  - NEPTUNE–PLUTO–ALTAIR Dec 3:4:7, exact 13:44:12 (13 min before; slow chord): on Neptune–Altair the horse's HAUMEA (imprint hub, struck by Neptune in step 1) 1:2:3 0.048%; on Pluto–Altair his Venus 0.034% (Brian Hughes tighter on both). Altair again.
  - Makemake (imprint) Dec 1:3:4 on Transpluto–Arcturus (slow): Arvico Bleu PLUTO (imprint) φ 0.026% — only tight chart. The two imprint bodies meet in one chord.
  - Pallas Dec 3:4:7 on Chiron–Pleiades exact 14:01:12 (6 s after the finish): Arvico Bleu Sedna 0.027% tightest (Craig Nichol 0.031%).
  - The Moon Dec 1:4:5 on Haumea–Betelgeuse held to 13:55:10: horse Neptune φ 0.038% (If Not For Dylan 0.026% tighter).
  - Callum Bewley: the Moon Dec 1:5:6 on Chiron–Regulus held to 13:55:10 — his NEPTUNE φ 0.010% tightest; the Moon Dec 1:7:8 on Eris–Antares at 13:57:55 (45 s into the race) — his own GONGGONG √2 0.021% met by an ordinary chord (Finisk River Makemake 0.009% tighter).
  - The Moon's chords on Makemake–Gonggong (13:55:55) and Haumea–Gonggong (13:59:10) — no chart tuned within 0.06%.
- §63 L3 (Jupiter … Vesta bases), 6 Oct:
  - Saturn Dec φ on Pallas–Regulus exact 13:54:00 (3.2 min before the off): Callum Bewley tightest — his own CERES √2 0.014% (met by an ordinary chord) and his Quaoar 0.026% (next If Not For Dylan 0.034%).
  - AT THE OFF: Vesta Dec 2:3:5 on Saturn–Equator exact 13:57:10 (0.000%) — the favourite's JOCKEY Conor O'Farrell Chiron 0.004% tightest (Callum Bewley Sun 0.048%, loose). As at Doncaster (Chiron on Sun–Venus at the off → the favourite pair, including O'Farrell).
  - Neptune Dec 1:2:3 on Juno–Antares (slow, 13:39): Arvico Bleu PLUTO (imprint) same chord, UNISON 0.048% — only chart.
  - Pallas √2 on Ceres–Vega (13:28): Arvico Bleu Sedna 0.004% (only chart; 29 min before). Vesta 1:3:4 on Mars–Betelgeuse (14:13): Arvico Bleu Ceres 0.014% tightest, Callum Bewley Gonggong 0.026%.
  - The Moon on Jupiter–Altair and Ceres–Sirius at the end of the race (14:00:55): Arvico Bleu Orcus / Makemake, Callum Bewley Saturn — all loose on the Moon's side (0.06–0.13%).
- §63 L4 (Sun, Mercury, Venus, Moon bases), 6 Oct:
  - The WINNING PAIR holds the top places on two Mercury–star chords:
    - Juno Dec 1:7:8 on Mercury–Capella exact 13:50:49 (6.4 min before): Callum Bewley CERES 0.013% (1st), Arvico Bleu HAUMEA (imprint hub) 0.032% (2nd), Finisk River 0.043%. Capella again.
    - Haumea RA 2:3:5 on Mercury–Regulus exact 14:07:06 (10 min after the off; the Mercury base moves, so the time is real): Arvico Bleu JUPITER 0.004%, his PALLAS 0.012%, Callum Bewley ORCUS 0.016% — the first three places; Conor O'Farrell Orcus 0.049% next. Sky Haumea = the horse's imprint hub body.
  - NO clean Sun–star chord held by the Moon in the race: the Moon on Sun–Venus 2:3:5 at the end of the race (If Not For Dylan Jupiter √2 0.008% tightest; Arvico Bleu Vesta 0.078%), the Moon on Sun–Castor loose (0.146%). (Repeat #3 not here; present at Catterick, Ffos Las, Doncaster.)
  - Ketu on Sun–Aldebaran (14:11:57): Arvico Bleu Eris 0.005%. Ketu √2 on Sun–Altair (14:22): Callum Bewley Venus 0.026%.
- §63 L5 (fast points, side note only), 6 Oct: ~2,100 chords in the window — colour only.
  - The Moon's Altair–Fomalhaut 1:2:3 (L1, horse Saturn UNISON): ASCENDANT–Altair + Moon RA 1:2:3 at 13:58:10 (0.0017%) — the same chord type, the Ascendant in Fomalhaut's place (cf. Doncaster: the Midheaven repeating Mars's 1:6:7 with Altair). Vertex–Altair + Moon φ 14:00:03.
  - Mercury–Regulus–Haumea (L4, winning pair top three): Midheaven–Regulus + Mercury 13:55:38/43, Vertex–Regulus + Haumea 13:55:53; in the race the ASCENDANT joins both — Regulus + Haumea 4:5:9 at 13:59:17 and Regulus + Mercury 1:2:3 at 13:59:19.
  - Pallas–Regulus (L3, Callum Bewley's Ceres √2): Part of Fortune 13:57:01 (9 s before the off); Vertex 13:58:44, Midheaven 13:58:56 in the race.
  - At the off: Part of Spirit–Equator + Saturn 3:4:7 and + Vesta 2:5:7 (the Vesta–Saturn–Equator chord exact at the off, the favourite's jockey's); 1 s after: Midheaven–Makemake + Vesta 2:5:7 (Makemake imprint).
- §63 AGAINST (all layers), 6 Oct — lattice/AG_20211014_carlisle_1355.txt:
  - DISCORD: only one live √2 — Mars–Pallas–Rigel (Dec), held from before the window, goes OUT 14:00:40 (26 s before the finish). Caught: Brian Hughes (5th, 5/2) Makemake 0.006%, Craig Nichol (3rd) Neptune 0.018% and Transpluto 0.028%, Slanelough (3rd) Eris 0.016%. Callum Bewley on it only as UNISON (his own Mercury √2 = the sky's √2, 0.071%) — like Joanna Mason at Catterick. Winning horse 0. Favourite pair 0.
  - SAME NOTE: the Moon's Altair–Fomalhaut 1:2:3 IN THE RACE — Arvico Bleu Saturn 0.012% > Brian Hughes Vesta 0.133% (the winning horse wins it). Ceres 1:3:4 on Sun–Polaris — Arvico Bleu Neptune 0.031% > If Not For Dylan. After the finish (14:02:55): the Moon on Quaoar–Antares — Gold Des Bois Transpluto 0.030% > Arvico Bleu Transpluto 0.039%.
  - In/out: does not separate.

## 64. Wincanton 14:20, 21 Mar 2022 (R30) — off 14:20:30, winning time 4m 56.31s, finish 14:25:26
Result: 1st River Bray 22/1 (Alan Johns) · 2nd Guernesey 9/2 (Tom O'Brien) · 3rd Ballyblack 10/11F (Rex Dingle) · 4th Birds Of Prey 10/1 (Harry Cobden) · 5th Electric Annie 9/2 (Nick Scholfield) · 6th Reserve Tank 17/2 (Brendan Powell). 6 ran. Outputs lattice/*_20220321_wincanton_1420.txt.
Step 1 imprint (blank-sheet #6): QUAOAR — same body both charts, the horse's Quaoar a natal hub, #12 Haumea/Venus lands alone on it, the race number 140/9 built on Quaoar/Sun; MAKEMAKE — the busiest body without the Moon, the horse's highest-quality Makemake, horse Makemake × jockey Haumea repeats #3; the jockey's RAHU takes #10 Makemake/Pluto alone; the jockey's ORCUS receives the same three pairs as Ballyblack's Juno.
- LAYER 1 (6 Oct):
  - MOON CROSSING IS BACK: the Moon reaches River Bray's natal QUAOAR Dec (−15.404, the #1 imprint body) at 14:26:26 — 1 min after the finish; first in the field (then Guernesey's Quaoar 14:36, Electric Annie's 14:38; horses born the same year share a near-identical Quaoar Dec). As it closes in, the Moon makes UNISONS with his Quaoar IN THE RACE: Dec 1:5:6 on Betelgeuse–Regulus exact 14:23:40 (0.024%) and Dec 3:5:8 on Alkaid–Altair exact 14:24:30 (0.020%, the only chart), earlier φ on Alkaid–Polaris (14:09, loose).
  - At the off: the Moon Dec φ on Antares–Spica exact 14:20:40 (10 s after) — River Bray Ceres 0.004% (Guernesey Jupiter, Reserve Tank Pluto 0.003% — three-way).
  - ALAN JOHNS: the Moon RA 1:4:5 on Antares–Arcturus exact 14:18:55 and on Antares–Castor exact 14:19:55 (35 s before the off) — his ORCUS (imprint receiver) both times (0.038% tightest; 0.022%, Guernesey Ceres 0.018% tighter on another chord). The SUN RA 1:6:7 on Antares–Fomalhaut exact 14:23:28 (in the race) — his MAKEMAKE (imprint) 4:5:9 at 0.001%, the tightest (Guernesey Haumea 0.013%). The Moon Dec 1:8:9 on Alkaid–Rigel 14:23:34 (in the race): his Pluto UNISON (0.077%) and Ketu.
  - For the 'against' check: the Moon RA √2 on Algorab–Alkaid exact 14:20:50 (20 s after the off): River Bray Chiron 0.033% (Brendan Powell Juno 0.016% tighter).
- §64 NODES (6 Oct): quiet for the winning pair (fifth race running).
  - Transit node + star pair against natal node + star pair: River Bray Rahu on Altair–Procyon and Alan Johns Rahu on Altair–Polaris — both days away (Altair again, but background). The favourite pair has the most (Ballyblack, Rex Dingle), all hours or days away.
  - Node bases, the Moon in the race: Dec √2 on Ketu–Sirius (14:24:15) — Guernesey Vesta 0.017%, Ballyblack (fav) Uranus √2 UNISON 0.020%, River Bray Chiron 0.039% (→ against); RA 3:4:7 on Ketu–Alkaid (14:23:00) — Brendan Powell 0.008% tightest, Alan Johns Ceres 0.028%.
- §64 L2 (slow-body bases), 6 Oct:
  - QUAOAR (the imprint body) in BOTH charts on chords around the off:
    - Alan Johns's QUAOAR: the Moon Dec 3:5:8 on Pluto–Spica held to 14:19:30 (1 min before the off) — 0.007% tightest (Tom O'Brien 0.014%); Ceres RA 5:8:13 on Neptune–Castor exact 14:13:53 — 0.008% tightest (next 0.047%).
    - River Bray's QUAOAR: Venus RA 3:4:7 on Chiron–Bellatrix exact 14:24:39 (in the race) — 0.018% (Rex Dingle, the favourite's jockey, 0.010% tighter).
  - River Bray Neptune: Venus Dec φ on Pluto–Procyon exact 14:22:10 (in the race) — 0.007%, joint tightest with Rex Dingle.
  - Alan Johns Sedna: the Moon Dec 1:6:7 on Pluto–Alphecca in the race (14:22:15) — 0.015% (Ballyblack Uranus 0.011% tighter). Alphecca again.
  - The Moon coming to the Eris–Fomalhaut Dec midpoint at the finish (14:25:15, still loose 0.148%): River Bray's natal SUN and JUPITER sit at the same midpoint (UNISON 0.007% / 0.031%) — the only charts.
  - Juno 1:7:8 on Orcus–Rahu exact 14:23:23 (in the race): River Bray Sedna 0.043% (Reserve Tank 0.039%).
- §64 L3 (Jupiter … Vesta bases), 6 Oct: lighter.
  - Mercury Dec 5:6:11 on Saturn–Antares exact 14:22:00 (1.5 min into the race): River Bray Pallas 3:5:8 0.045% — the only close chart.
  - The Moon RA 3:8:11 on Juno–Antares in the race (14:22:15): Alan Johns HAUMEA same chord (UNISON 0.032%; his Haumea is the imprint partner of the horse's Makemake) — Rex Dingle (fav's jockey) Gonggong / Uranus 0.003% tighter on other chords.
  - Haumea RA 1:5:6 on Ceres–Polaris exact 14:22:31 (in the race): Alan Johns Haumea same body (loose 0.077%) and Chiron UNISON (loose); Harry Cobden Neptune 0.003% tightest.
  - Orcus 1:7:8 on Juno–Rahu (14:23:15, in the race): River Bray's Ketu √2 0.043% (Electric Annie Ketu √2 0.006% tighter).
  - Rahu 2:5:7 on Vesta–Rigel (14:04:57): Alan Johns Neptune 0.005% (Tom O'Brien Eris UNISON 0.003% tighter); his Makemake UNISON (loose).
  - Rex Dingle (favourite's jockey) again tight on the Moon's chords.
- §64 L4 (Sun, Mercury, Venus, Moon bases), 6 Oct:
  - Vesta Dec 1:2:3 on Mercury–Equator exact 14:22:52 (in the race): Alan Johns JUNO 5:6:11 0.003% tightest (Rex Dingle Uranus 0.011%); his Saturn too (0.019%). Chiron 1:1:2 on the same base 14:16:35 — the same two.
  - Sun–star chords held by the Moon: Sun–Antares, the Moon RA φ at 14:20:45 (15 s after the off) — ONLY Alan Johns tuned (Gonggong 0.055%, loose); the Moon Dec √2 on Sun–Antares at 14:19:30 — Birds Of Prey Makemake 0.003%. SUN–REGULUS, the Moon Dec 3:4:7 at 14:18:30 — Rex Dingle (favourite's jockey) Pallas 0.007% / Eris UNISON 0.008% tightest; River Bray Uranus √2 loose (Doncaster: Sun–Regulus also went to the favourite's side). No Sun–star chord with the winning horse tightest here.
  - Jupiter φ on Sun–Fomalhaut (14:30): Alan Johns Pallas UNISON 0.018%, River Bray Eris at the midpoint 0.007% (Tom O'Brien 0.005%).
  - Saturn RA 4:5:9 on Sun–Algol exact 14:25:15 (11 s before the finish): River Bray tuned through four bodies incl. QUAOAR φ — all loose (0.05–0.10%).
- §64 L5 (fast points, side note only), 6 Oct: ~3,200 chords in the window — colour only.
  - Eris–Fomalhaut (the Dec midpoint the Moon reaches at the finish, River Bray's natal Sun and Jupiter): Part of Fortune 14:20:29 (1 s before the off); Vertex 14:22:10, Midheaven 14:23:28 (Dec 1:2:3) in the race.
  - Mercury–Equator (Alan Johns Juno, L4): Midheaven 14:18:59.
  - Sky Quaoar sits in many fast-point chords through the race, but no more than other slow bodies — nothing specific to the horse's Quaoar crossing (which is a natal Dec, not a sky point).
  - No fast-point repeat of the Moon's Alkaid–Altair or Betelgeuse–Regulus chords (unlike Doncaster's Midheaven and Carlisle's Ascendant repeats).
- §64 AGAINST (all layers), 6 Oct — lattice/AG_20220321_wincanton_1420.txt:
  - DISCORD is everywhere in this race (6 runners): 11 of 12 charts on at least one live √2. Two √2 chords catch most of the field: Jupiter–Saturn–Fomalhaut (Dec, slow, comes IN 14:19:05) and the Moon's √2 on Ceres–Betelgeuse (IN 14:24:55, 30 s before the finish).
  - The winning horse is caught 3 times: the Moon's √2 on Algorab–Alkaid (IN 14:19:10, exact 14:20:50, OUT 14:22:30) — his CHIRON 0.033% (Brendan Powell 0.016% tighter); the Moon's √2 on Ketu–Sirius in the race (14:23:40–14:24:40) — his Chiron again 0.039% (Guernesey 0.017%, Ballyblack UNISON 0.020% tighter); Jupiter–Saturn–Fomalhaut — his Eris 0.031%. Alan Johns 1 (Pallas on Ceres–Betelgeuse). Favourite horse 3, Guernesey 3, Tom O'Brien and Reserve Tank 0.
  - SAME NOTE: four contests, none involving the winning pair; Rex Dingle (fav's jockey) loses two (to Reserve Tank, to Guernesey).
  - WHAT I SEE: in a 6-runner race the discord check does not separate — the winning horse is as caught as the favourite.

## 65. Exeter 15:15, 19 Oct 2021 (R12) — off 15:16:04, winning time 4m 51.10s, finish 15:20:55
Result: 1st Forget You Not 25/1 (James Best) · 2nd Jarlath 11/1 (Sean Houlihan) · 3rd Caspers Court 5/2 (Tom Scudamore) · 4th Pens Man 5/4F (Jonjo O'Neill Jr) · PU Pointed And Sharp 11/2 (Tom O'Brien) · PU Blaze A Trail 10/1 (Connor Brace). 6 ran. Outputs lattice/*_20211019_exeter_1515.txt.
FIX (6 Oct): nodes_chords.py crashed on non-numeric finish ('PU'); sort now puts PU/F etc. after the placed runners (backup nodes_chords.py.bak). No effect on earlier races.
Step 1 imprint (blank-sheet #7): JUNO with royal REGULUS and φ — #10 Regulus/Transpluto (φ) lands alone on the horse's Juno with both legs applying, and Juno carries that number in the horse (Juno–Regulus), between horse and jockey (horse Juno × jockey Regulus) and ×10 in the jockey (Ceres–Juno 10φ); sky Mars → jockey Juno peaking at the off; horse Neptune × jockey Rahu = #7 exact; horse Procyon–Vesta held inside alone.
- LAYER 1 (6 Oct):
  - The sky: near Full Moon again (Moon RA ~15, Dec +1.4, near the equator). Only one Moon crossing in the hour — Pointed And Sharp (PU) Uranus Dec at 15:02. None for the winning pair.
  - AT THE OFF (15:16:04): Mercury Dec 5:8:13 on Algol–Pleiades exact (0.000%) — Forget You Not's ERIS makes the SAME chord (UNISON 0.007%, the tightest in the field); his JUNO (imprint) also UNISON (loose 0.127%); James Best Orcus 0.024%. Sean Houlihan (2nd's jockey) 0.009% on another chord.
  - The Moon Dec 1:3:4 on Aldebaran–Procyon exact 15:17:09 (1 min into the race): Forget You Not GONGGONG 5:8:13 0.005% — clear tightest (next 0.063%).
  - The Moon RA 2:3:5 on Capella–Vega exact 15:17:49 (in the race): horse Neptune 0.021% (Caspers Court Ketu 0.001% tighter).
  - JAMES BEST: the Moon Dec 1:5:6 on Altair–Capella exact 15:15:09 (1 min before the off) — his CERES (imprint: Ceres–Juno 10φ) 0.007% (Tom Scudamore Neptune 0.001% tighter); the sky's JUNO RA 1:3:4 on Algol–Altair exact 15:17:52 (in the race) — his Gonggong 0.022% (only close chart); the Moon RA φ on Arcturus–Fomalhaut exact 15:20:54 (1 s before the finish) — his SATURN 0.038% and PLUTO 0.045%, the tightest.
  - For the 'against' check: the Moon Dec √2 on Algol–Antares comes in 15:17:04 (in the race) — James Best Mars 0.019% (Pens Man Chiron 0.000%, Sean Houlihan Eris 0.002% tighter).
- §65 NODES (6 Oct): quiet near the off (sixth race running).
  - Transit node + star pair against natal node + star pair: Forget You Not none; James Best Rahu on Capella–Procyon (10 h away, loose).
  - Node bases: the Moon Dec 1:4:5 on Ketu–Polaris held to 15:14:04 (2 min before the off) — Forget You Not ORCUS 1:7:8 0.019%, James Best Venus 0.045%. Sun at the Rahu–Procyon midpoint (15:52 → 23.5 min before) — horse Mercury 0.019%. Vesta 3:4:7 on Rahu–Bellatrix (45.8 min before) — horse Neptune 0.013%. Nothing on node bases during the race for the winning pair.
- §65 L2 (slow-body bases), 6 Oct:
  - The Moon RA 5:6:11 on Uranus–Fomalhaut, held to 15:16:34 (30 s after the off): Forget You Not SUN 3:8:11 0.005% — tightest (Jonjo O'Neill Jr, the favourite's jockey, 0.012%).
  - Vesta φ on Pluto–Algorab exact 15:12:02 (4 min before): Forget You Not's own VESTA √2 (same body, 0.039%) met by an ordinary chord — only chart (imprint: horse Procyon–Vesta held inside alone).
  - Rahu RA φ on Sedna–Pleiades exact 15:16:21 (17 s after the off): James Best Transpluto 0.031% — only chart.
  - Mars Dec on Orcus–Spica exact 15:20:58 (3 s after the finish; Mars at the Orcus–Spica... 1:8:9): James Best JUPITER at the Orcus–Spica midpoint (1:1:2, 0.002%) — only chart.
  - The Moon Dec 1:2:3 on Uranus–Antares held to 15:14:04 (2 min before): James Best Pluto 0.003% (joint tightest with Tom O'Brien).
  - The Moon in the race on Haumea bases: Dec 5:6:11 on Haumea–Altair (15:18:49) — James Best CERES (imprint) 0.010% (Tom Scudamore 0.006% tighter); Dec φ on Haumea–Procyon (15:19:34) — his Gonggong 0.016% (Jarlath 0.014%).
- §65 L3 (Jupiter … Vesta bases), 6 Oct:
  - The Moon Dec 3:8:11 on Vesta–Vega at 15:16:49 (45 s into the race): Forget You Not MARS 5:6:11 0.001% — tightest (Jarlath Mars 0.011%); his Pallas 0.040%. Same moment, the Moon 3:8:11 on Jupiter–Capella — James Best MERCURY 0.012% tightest (next 0.054%).
  - Quaoar Dec 2:3:5 on Mars–Antares exact 15:13:28 (2.6 min before): James Best Pallas 0.002% (Tom O'Brien 0.001%).
  - Saturn √2 on Pallas–Betelgeuse exact 15:07:08: James Best JUNO (imprint) 0.016% (Connor Brace 0.012%).
  - AT THE OFF: Mercury Dec 5:6:11 on Vesta–PROCYON exact 15:16:04 (0.000%) — Procyon–Vesta is the horse's imprint pair (held inside alone, RA) but Forget You Not is not tuned to this Dec chord; only loose others.
  - Vesta 1:6:7... Saturn–Vesta + Gonggong 1:7:8 (15:19:49, in the race): Forget You Not Gonggong same body (loose 0.089%).
- §65 L4 (Sun, Mercury, Venus, Moon bases), 6 Oct:
  - 3 s BEFORE THE OFF: Vesta Dec 5:6:11 on Mercury–Procyon exact 15:16:01 (0.000%) — Forget You Not's RAHU makes the SAME chord (UNISON 0.019%), the only chart on it. The same Mercury–Vesta–Procyon triangle as the L3 chord exact at the off (read there from the Vesta–Procyon base, where he was not tuned) — Procyon–Vesta = the horse's imprint pair. Rahu = the busiest body in step 1 (horse Neptune × jockey Rahu = #7).
  - SUN–ANTARES: Transpluto Dec 4:5:9 exact 15:16:19 (15 s after the off) — Forget You Not KETU 1:4:5 0.013% tightest (Pointed And Sharp Vesta 0.020%); the Moon then makes a √2 on Sun–Antares at the finish (15:20:49) — his Ketu again, tightest (→ against: a Sun–star chord held by the Moon with the horse tightest, but as √2).
  - The Moon RA 3:8:11 on Sun–Venus held to 15:14:04 (2 min before): Jarlath Orcus 0.012% tightest; Forget You Not loose (Rahu, Jupiter, Juno 0.085–0.149%).
  - James Best: nothing tight near the off at L4 (Pallas 0.021% on Orcus's Sun–Mercury chord 15:21:34, after the finish).
- §65 L5 (fast points, side note only), 6 Oct: ~3,600 chords in the window — colour only.
  - REGULUS–JUNO (the imprint pair: #10 Regulus/Transpluto lands on the horse's Juno; horse Juno–Regulus; horse Juno × jockey Regulus): Part of Spirit 15:14:21 and 15:16:14 (10 s after the off); Ascendant 15:17:01, 15:17:45; Midheaven 15:18:33, 15:19:40 — all in the race.
  - AT THE FINISH SECOND (15:20:55): Ascendant–Ceres + Juno RA 1:3:4 (0.0003%) — Ceres–Juno is the jockey's imprint pair (10φ); 15:20:54 Midheaven–Juno + Rahu 1:4:5. At the off (15:16:04): Vertex–Castor + Juno 1:1:2.
  - Procyon–Vesta (horse imprint): Part of Spirit, Vertex before the off; Vertex, Midheaven 15:17:46–49 in the race. Sun–Antares (horse Ketu): Ascendant 15:17:03, Vertex 15:19:33, Part of Spirit 15:20:08 in the race. Algol–Mercury (the off chord, horse Eris): Vertex 15:17:45, Midheaven 15:17:54.
- §65 AGAINST (all layers), 6 Oct — lattice/AG_20211019_exeter_1515.txt:
  - DISCORD widespread again (6 runners): 9 of 12 charts on a live √2. The Moon's √2 chords: Transpluto–Spica (goes OUT 15:14:49, before the off; Tom Scudamore 0.001%), Saturn–Ceres (IN 15:16:34; Jarlath 0.010%), Sun–Antares (IN 15:17:14; FORGET YOU NOT Ketu 0.013%, tightest), Algol–Antares (IN 15:17:04; the FAVOURITE Pens Man Chiron 0.000% — the tightest discord in the race; Sean Houlihan 0.002%; James Best Mars 0.019%).
  - Winning horse 1 (Sun–Antares in the race), James Best 2, Pens Man 2, Jonjo O'Neill Jr 0.
  - SAME NOTE: four contests, none involving the winning pair.
  - WHAT I SEE: as at Wincanton, in a 6-runner field discord does not separate; the single tightest √2 (0.000%) in the race is on the beaten favourite.

## 66. REVIEW AFTER 7 RACES (Eddie 6 Oct 16:42: "just say what you see – the 2 methods – how they interact – are we heading in the right direction")
| race | Moon reaches imprint Dec | chord at/near the off held by the winner (UNISON or only chart) | Sun–star chord held by Moon, horse tightest | winner free of live discord | same note won |
|---|---|---|---|---|---|
| Catterick 5 ran | yes (−15 min, horse Makemake) | yes (jockey's full triangle, −85 s) | yes (Sun–Regulus) | yes | jockey |
| Ffos Las 4 ran | yes (−6 min, jockey Vesta) | partly (Moon 1:2:3 on jockey's own √2 at the off) | yes (Sun–Alphecca) | yes | jockey |
| Newcastle 5 ran | no (Moon at Dec limit) | partly (Moon held to +5 s, horse Juno UNISON loose) | no | no | – |
| Doncaster 5 ran | no | yes (Mars at the off, only the horse) | yes (Sun–Betelgeuse) | no | no |
| Carlisle 5 ran | no | no (off chord → favourite's jockey); Moon chord inside the race, horse UNISON | no | yes | horse |
| Wincanton 6 ran | yes (+1 min after the finish, UNISONs in the race) | no | no | n/a (everyone caught) | – |
| Exeter 6 ran | no | yes (Mercury at the off UNISON; Vesta −3 s UNISON on the imprint pair) | √2 only | n/a | – |
Cautions recorded: all 7 races chosen with the result known, all outsiders; step-1 imprint picks were made knowing the winner; every chart has 100–200 tuned pairs, so "tightest on some chord" happens for every runner somewhere; off times vary by minutes; no favourite-won races and no blind runs yet.

## 67. SECOND LOOK — the weakest races, starting with Newcastle (Eddie 6 Oct 16:45: "some things we may rethink like discords… just keep saying what we see… go back to the weakest looking races, starting with Newcastle")
- New one-off scan (scratchpad offscan.py, reads the dumps): every sky chord, all layers, EXACT between off−3 min and finish+1 min, with the tuned charts ranked.
- NEWCASTLE (13 chords exact 13:30:27–13:34:39):
  - JIM CROWLEY (favourite's jockey, 3rd) is the tightest chart on 7 of the 13 — Mercury–Venus + Moon (Orcus 0.003%), Uranus–Ketu + Moon (Mars 0.006%), Pallas–Alkaid + Mercury (Haumea 0.005%), Quaoar–Altair + Vesta, Mars–Altair + Moon, Vesta–Fomalhaut + Moon, and more. The chords around the off belong mostly to the favourite's jockey. (Doncaster and Carlisle: the chord exact at the off also went to the favourite's jockey, O'Farrell.)
  - Connor Beasley is the ONLY chart on two: Mercury Sky 5:8:13 on Jupiter–Saturn at 13:31:48 (1 min before the off; his Uranus 0.048%) and Jupiter Dec 1:5:6 on Betelgeuse–Deneb Algedi at 13:34:39 (51 s after the finish; his Haumea 0.008%). Venturous is tightest on none; tuned on two (Juno UNISON on the Moon's Mercury–Venus 2:3:5, loose; nothing else).
  - The Moon at its southern Dec limit: the nearest natal point of ANY runner is 1.7° away (Regional's Saturn, RA). The Moon is out of reach of every chart — nobody gets a crossing.
  - What Venturous does hold tightest is DISCORD: the Moon's √2 on Algol–Polaris held all hour (his Jupiter 0.005%, Rahu 0.020%), and Mercury's √2 on Orcus–Deneb Algedi coming in 25 s before the off (his Uranus 0.036%).
- DISCORD ACROSS THE 7 RACES (who is tightest on each live √2): the WINNING HORSE is the tightest chart on at least one live √2 in 4 races — Newcastle (Uranus, Mercury's √2), Doncaster (Ketu, the Moon's √2 Sedna–Aldebaran), Wincanton (Eris, Jupiter–Saturn–Fomalhaut), Exeter (Ketu, the Moon's √2 Sun–Antares). Not at Catterick, Ffos Las, Carlisle (the three 4–5 runner races where discord looked "against"). Beaten favourites/their jockeys are tightest on √2s too (Jack Tudor ×3, Oot Ma Way ×2, Pens Man 0.000%).
- Eddie 16:52: "we are missing the detail of the families here, the distances – what does 'the Moon's √2 on Algol–Polaris… his Jupiter 0.005%' mean? – also some things are going to be strong that are not exact within that race, or hour or even the day."
  - Worked example (Dec, degrees): base Algol–Polaris = 48.311 (sky) and 48.311 (Venturous's stars at birth — same string).
    - SKY at the off: Moon −27.308 → Moon–Algol 68.266, Moon–Polaris 116.577; 48.311 : 68.266 : 116.577 = 1 : 1.413 : 2.413 = the √2 division 1 : √2 : 1+√2 (dev 0.082% at the off; tightest 0.066% half an hour before; the Moon is at its Dec limit so this holds all hour and is drifting away).
    - NATAL Venturous Jupiter Dec 21.633 → Jupiter–Algol 19.323, Jupiter–Polaris 67.634; 19.323 : 48.311 : 67.634 = 2 : 5 : 7 (0.005%). Rahu: 48.311 : 57.984 : 106.295 = 5:6:11 (0.020%). Pallas: Algol–Polaris = Pallas–Algol (1:1:2, 0.068%).
    - So "tuned in" = the sky and the horse are on the SAME string (Algol–Polaris Dec 48.311); the Moon divides it 1:√2:1+√2, his Jupiter divides it 2:5:7. Not the same chord (not UNISON).
    - Families inside: the √2 division holds √2 (dissonant), 1+√2 (silver, PHI family) and 1+1/√2 (dissonant); 2:5:7 holds 5/2 (imperfect), 7/5 and 7/2 (septimal).
  - Agreed to rethink: strength may lie in tightness on both sides and the families, not in the exact minute — slow chords that hold for days were being set aside as "background".
- §67 NEWCASTLE RE-READ, LAYER 1 WITH DISTANCES ("more slow may mean more strong", Eddie 16:55). One-off scripts in the scratchpad: detail.py (distances + families both sides), parallels.py (sky bodies sitting on a natal Dec/RA at the off).
  - SLOW PARALLELS AT THE OFF (sky body on a natal point's Dec, within 0.03°): CONNOR BEASLEY has three — the most in the field: sky MAKEMAKE Dec 22.124 on his natal HAUMEA 22.115 (0.008°), sky JUNO −13.814 on his natal QUAOAR −13.808 (0.006°), sky VESTA −21.123 on his natal NEPTUNE −21.146 (0.023°). Everyone else 0 or 1 (Mondammej and King Of Stars: sky Quaoar on their own Quaoar — same-age horses; Cam Hardie: Saturn on Gonggong 0.005°). Venturous 0.
    - So the slow version of the Moon crossing is there for the winning jockey: because Makemake sits on his Haumea's Dec, every Dec chord Makemake makes, his Haumea makes too — UNISONs on Capella–Procyon (Haumea 23.881/16.887 vs Makemake 23.873/16.906, 1:√2:1+√2), Betelgeuse–Deneb Algedi (14.707/38.240 vs 14.717/38.254, 5:8:13), Algorab–Capella (φ), Altair–Antares (3:8:11), Fomalhaut–Rigel (√2 div.), Antares–Sirius (1:4:5). Same for Juno on his Quaoar: Algol–Altair (√2 div.), Altair–Bellatrix (1:8:9), Polaris–Regulus (1:3:4), Alkaid–Vega (1:5:6). Makemake barely moves — this holds for about a day.
  - CONNOR BEASLEY'S ORCUS (the step-1 imprint hub) — his tightest Layer-1 string: Dec Procyon–Rigel (base 13.420 sky / 13.427 natal): natal Orcus to Procyon 3.357, to Rigel 10.071 → 1:3:4 (0.001%, all PERFECT: 3, 4/3, 4). Sky NEPTUNE to Procyon 10.067, to Rigel 3.354 → 1:3:4 (0.055%, exact 4.7 h after the off) — the MIRROR image of his Orcus (same distances, swapped ends); sky Eris sits at the midpoint (1:1:2, 6.715/6.706). UNISON, slow.
  - VENTUROUS'S tightest strings (all slow): Sedna RA 5:6:11 on Bellatrix–Procyon 0.000% (27.953/61.496; sky Transpluto same chord 5:6:11, 0.143%, exact in 11 d — UNISON; HIGH/IMPERFECT); Pluto Dec 1:6:7 on Deneb Algedi–Procyon 0.001% (3.558/24.907; sky Rahu √2 division, 8.4 h after); Gonggong (step-1 imprint) Dec 1:5:6 on Algol–Castor 0.002% (54.408/45.340; sky Mars 1:6:7 18.7 h before); Orcus RA at the Bellatrix–Procyon midpoint 0.004%; Jupiter 2:5:7 on Algol–Polaris 0.005% (the Moon's √2 division held all hour).
  - BOTH WINNING CHARTS ON ONE SKY CHORD: Mars RA 5:6:11 on Alkaid–Regulus (Mars to Alkaid 45.645, to Regulus 100.431; 0.023% at the off, exact 21.6 min after) — UNISON with the jockey's MARS (same body, 120.614/65.819, 0.100%) and the horse's Ceres (120.479/65.684, 0.107%). Mars 5:8:13 on Arcturus–Regulus — UNISON with the horse's Sedna (0.145%). Regulus in both.
  - HOW THE MARS CHORD LINKS TO THE HORSE (Eddie 17:08 — the jockey link "100% what I think it should be"): (1) through the pair — horse natal CERES RA 86.413 sits on jockey natal MARS RA 86.269 (0.144°; Dec 5.2° apart), so it holds the same 5:6:11 on Alkaid–Regulus (120.479/65.684, 0.107%); the horse's own Mars (RA 9.486) is not on the string. (2) the same sky Mars MIRRORED on the neighbouring string RA Arcturus–Regulus (61.811): sky Mars beyond Arcturus 38.621 / to Regulus 100.431 = 5:8:13; horse SEDNA beyond Regulus 98.767 / to Arcturus 160.587 = 5:8:13 (0.145%); natal unit 12.36 = 8/5 of sky unit 7.72 (jockey case: 6/5). Sky Mars–Regulus 100.431 common to both; the pair holds both chords from the far side of Regulus.
  - Jockey case shape: sky Mars beyond ALKAID (Mars–Alkaid 45.645, base 54.787 = 5:6 of 11, unit 9.130); jockey Mars beyond REGULUS (base 54.795 = 5, Regulus–Mars 65.819 = 6, unit 10.963 = 6/5 of the sky unit) — mirror image.
- §67 THE SUN ON THE STARS, NEWCASTLE 2 Jan 2022 (Eddie 17:11: "show me what the sun looks like connected to the stars in transit that day – show me all its chords"). Sun at the off RA 282.849, Dec −22.913. scratchpad sunchords.py.
  - Live at the off (within 0.15%): RA Polaris–Spica 1:√2:2 (Sun–Spica 81.552, Sun–Polaris 115.332, base 163.116; 0.007%, EXACT 13:32:33 — 16 s before the off; no chart tuned to it); RA Alphecca–Fomalhaut 4:5:9 (49.181/61.563/110.744; exact 14:26); RA Capella–Pleiades 1:6:7 (156.331/134.027/22.305; exact 18:06); Dec Pleiades–Spica 1:3:4 (47.019/11.752/35.267; exact 12:40); Dec Antares–Procyon 1:8:9 (3.518/28.131/31.649; exact 13:12); Dec Arcturus–Polaris 3:5:8 (42.081/112.182/70.101; exact 19:15); Dec Fomalhaut–Pleiades 1:7:8 (6.713/47.019/53.732; exact 14:34).
  - Winning pair on the Sun's chords: Connor Beasley TIGHTEST on Capella–Pleiades 1:6:7 (Eris 2:3:5 0.027%, Haumea 1:5:6 0.028%); Venturous Orcus φ on Arcturus–Polaris 0.055% (Good Effort Orcus 0.015% tighter); Venturous Juno 5:6:11 on Antares–Procyon 0.040% (King Of Stars / Jim Crowley 0.018% tighter).
  - Through the whole day ~30 Sun–star chords come exact (to 0.15%), every 10–60 min; listed in the reply.
- "THE MOON IS THE CLOCK" (Eddie 17:14). Working idea: slow chords set the strings and the notes (what / who); the Moon strikes the time (when).
  - Newcastle check (scratchpad moonclock.py — the Moon minute by minute, off−30 to off+27, on the winning pair's slow strings): the Moon is SILENT on almost all of them (Procyon–Rigel, Capella–Procyon, Betelgeuse–Deneb Algedi, Bellatrix–Procyon, Algol–Castor, Deneb Algedi–Procyon, Arcturus–Regulus, Capella–Pleiades, Polaris–Spica). Only: Algol–Polaris (the √2 division held all hour — horse Jupiter 2:5:7) and ALKAID–REGULUS: the Moon comes onto the Mars string with 3:4:7 at 13:54:19 — 6 s before Mars's own 5:6:11 on that string is exact (13:54:25) — the Moon and Mars on the winning pair's string at the same moment, but 21 min after the race (scheduled time 13:30, off 2 min 49 late).
- MERCURY ON THE STARS, NEWCASTLE (Eddie 17:16: "do not jump to conclusions yet… show me the mercury chords"). Mercury at the off RA 302.622, Dec −21.754 (Deneb Algedi 24.1° away in RA, 5.6° in Dec).
  - Live at the off (≤0.15%): RA Aldebaran–Deneb Algedi φ (126.364/24.136/102.228; exact 13:36:25), RA Antares–Spica 5:6:11 (55.275/101.325/46.050; 13:15:54), RA Algol–Betelgeuse 2:5:7 (14:21), RA Algol–Fomalhaut 2:3:5 (104.425/41.790/62.635; 14:09:38), RA Betelgeuse–Fomalhaut 2:5:7 (14:11), RA Rigel–Sirius 1:6:7 (15:42); Dec Capella–Rigel 1:4:5 (67.750/13.551/54.199; 13:37:57), Dec Bellatrix–Deneb Algedi 1:4:5 (28.103/5.623/22.480; 13:43:15), Dec Deneb Algedi–Regulus 1:5:6 (5.623/33.719/28.097; 13:45:57), Dec Polaris–Vega 5:6:11 (10:55), Dec Bellatrix–Regulus 1:5:6 (14:48), Dec Procyon–Regulus 1:4:5 (12:19), Dec Antares–Bellatrix 1:6:7 (13:52). No Flat/Sky at the off.
  - Tightest charts: Capella–Rigel — Venturous VESTA 3:4:7 0.010% (only close chart); Algol–Fomalhaut — Venturous ORCUS φ 0.006% (tightest); Deneb Algedi–Regulus — Connor Beasley PLUTO 3:5:8 0.022% (tightest; Venturous Venus √2 div. 0.026% next); Procyon–Regulus — Mondammej Venus UNISON 0.045%, Venturous Ketu 0.055%; Bellatrix–Deneb Algedi, Antares–Bellatrix — King Of Stars; Antares–Spica — King Of Stars; Polaris–Vega — Regional; Betelgeuse–Fomalhaut, Aldebaran–Deneb Algedi — Jason Watson; Bellatrix–Regulus — Good Effort.
  - Through the day Mercury comes exact with some star pair ~100 times (every 10–20 min); Deneb Algedi and Regulus recur around the off (13:36–13:46 three Deneb Algedi chords in Dec/RA).
- VENUS ON THE STARS, NEWCASTLE. Venus at the off RA 293.414, Dec −18.369 (retrograde, near the Sun — inferior conjunction 8 Jan 2022).
  - Live at the off: RA Antares–Spica 1:1:2 (Venus–Antares 46.068 = base 46.050; Venus–Spica 92.118; exact 14:17:11), RA Deneb Algedi–Regulus φ (33.343/141.319/174.663; 14:07:23), RA Algol–Vega 1:8:9 (113.632/14.185/127.818; 12:52:57); Dec Pleiades–Regulus 2:5:7 (42.475/30.335/12.140; 11:12), Dec Pleiades–Procyon 4:5:9 (42.475/23.587/18.888; 10:08), Dec Alphecca–Fomalhaut 1:4:5 (45.080/11.258/56.338; 15:00), Dec Alphecca–Betelgeuse 3:4:7 (45.080/25.775/19.305; 18:43), Dec Algol–CourseLat φ (01:22).
  - Tightest charts: JIM CROWLEY (favourite's jockey) on three — Pleiades–Procyon (Sedna 0.003%), Pleiades–Regulus (Ketu 1:1:2 0.002%), Alphecca–Betelgeuse (Rahu 0.014%); Mondammej Venus on Alphecca–Fomalhaut (0.007%); King Of Stars Juno on Antares–Spica (0.013%); Mondammej Gonggong on Algol–Vega (0.024%); Cam Hardie Chiron on Deneb Algedi–Regulus (0.034%). Winning pair: none tightest — Venturous Sun 1:2:3 on Algol–Vega 0.073% (2nd), Vesta on Antares–Spica 0.095% (2nd), Saturn φ on Deneb Algedi–Regulus 0.079% (4th).
  - Through the day ~45 Venus–star chords come exact.
- MARS ON THE STARS, NEWCASTLE (Eddie 18:32: "great, mars – leave the moon, it is the clock for the racetime"). Mars at the off RA 252.527, Dec −22.616.
  - Live at the off (≤0.15%): RA Alkaid–Regulus 5:6:11 (45.645/100.431/54.787; exact 13:54:25), RA Arcturus–Regulus 5:8:13 (38.621/100.431/61.811; exact 13:54:25), Dec Algorab–Antares 5:8:13 (6.101/3.815/9.916; 13:54:25 as φ), RA Alphecca–Vega √2 div. (18.858/26.702/45.561; 13:59:49), RA Algorab–Fomalhaut √2 div. (11:50), RA Algorab–Capella 3:5:8 (65.061/173.346/108.284; 10:32), Dec Aldebaran–Algol 5:8:13 (39.124/63.574/24.450; 12:15), Dec Antares–Spica 1:3:4 (3.815/11.455/15.270; 12:56), Dec Castor–Pleiades 1:6:7 (02:50), Dec Algol–Castor 1:6:7 (63.574/54.502/9.072; 1 Jan 18:53), Flat Capella–Castor 1:4:5, Sky Algorab–Castor 15:21:35.
  - THREE MARS CHORDS EXACT AT THE SAME MOMENT, 13:54:25 (21.6 min after the off): Alkaid–Regulus 5:6:11, Arcturus–Regulus 5:8:13 (both through Mars–Regulus 100.442), Algorab–Antares (Dec). The Moon comes onto Alkaid–Regulus at 13:54:19.
  - Tightest charts: Algol–Castor — Venturous GONGGONG (imprint) 1:5:6 0.002%; Algorab–Capella — Venturous ERIS 1:2:3 0.030%; Alphecca–Vega (√2 div.) — Connor Beasley CHIRON 5:8:13 0.013%; Alkaid–Regulus — Cam Hardie Jupiter 0.057% tightest, but the only UNISONs are Connor Beasley MARS (0.100%) and Venturous CERES (0.107%); Arcturus–Regulus — Jim Crowley Mars 3:8:11 0.020% (Venturous Sedna UNISON 0.145%); Castor–Pleiades — Good Effort Orcus 0.016%; Algorab–Antares — Jason Watson Juno 0.016%; Aldebaran–Algol — Daniel Tudhope 0.017%; Antares–Spica — King Of Stars 0.019%; Algorab–Fomalhaut — Regional 0.026%.
  - Winning pair tightest on 3 of 12 Mars chords (Venturous 2, Connor Beasley 1) plus the only UNISONs on Alkaid–Regulus.
  - ★ MARS NOTE (Eddie 18:39: "this mars is very important – make note of how exact it is and applying during the race"): RA Mars–Alkaid–Regulus 5:6:11 — 0.058% at off−30, 0.0229% at the OFF (Mars–Alkaid 45.6450, Mars–Regulus 100.4315), 0.0218% at the FINISH, 0.0086% at off+30, EXACT 13:54:25 — APPLYING (tightening) all through the race; within 0.15% from 11:39 to 16:09. Same for RA Mars–Arcturus–Regulus 5:8:13 (0.0286% off → 0.0273% finish → exact 13:54:25; in range 12:01–15:50) and Dec Mars–Algorab–Antares 5:8:13 (0.0597% → 0.0570%). Winning pair: Connor Beasley's own MARS and Venturous's CERES in UNISON on Alkaid–Regulus (the only UNISONs), Venturous's Sedna UNISON on Arcturus–Regulus; mirror shape (pair beyond Regulus, sky Mars beyond Alkaid/Arcturus).
- JUPITER ON THE STARS, NEWCASTLE. Jupiter at the off RA 332.974, Dec −12.208. NO RA chords; 9 Dec chords.
  - ★ Dec Betelgeuse–Deneb Algedi 1:5:6 (base 23.538; Jupiter–Betelgeuse 19.615, Jupiter–Deneb Algedi 3.923): 0.048% at off−30 → 0.0028% at the OFF → 0.0013% at the FINISH → EXACT 13:34:37 (49 s after the finish) — APPLYING through the race to dead exact. Tightest chart: CONNOR BEASLEY HAUMEA 5:8:13 (14.707/38.240, 0.008%) — the only close chart (next 0.099%). On the same string sky MAKEMAKE (sitting on his Haumea's Dec) makes his Haumea's own 5:8:13 (UNISON). So the jockey's Haumea is played on this string by Jupiter (applying, exact just after the finish) and by Makemake (held).
  - Dec Arcturus–Deneb Algedi 1:8:9 (31.376/3.923/35.299; exact 13:16:37, separating through the race 0.0215% → 0.0229%): Venturous MERCURY 1:4:5 0.012% tightest.
  - Dec Algol–Regulus 5:6:11 (53.166/24.174/28.992; applying slowly, exact 18:17): Venturous RAHU 1:1:2 0.010% tightest (Rahu at the Algol–Regulus... Rahu–Algol 57.984 = 2× base).
  - Others: Betelgeuse–Vega 5:8:13 (Regional 0.044%), Arcturus–Vega 5:8:13 (Jim Crowley Sun 0.005%), Fomalhaut–Procyon 1:1:2 midpoint (Cam Hardie 0.041%; Venturous Eris 0.066%), Arcturus–Betelgeuse 3:5:8 (King Of Stars 0.019%), Arcturus–Procyon 4:5:9 (Regional 0.013%), Bellatrix–CourseLat φ.
  - Winning pair tightest on 3 of 9 Jupiter chords (Connor Beasley 1, Venturous 2). Deneb Algedi in 2 of the 3.
- SATURN ON THE STARS, NEWCASTLE. Saturn at the off RA 314.470, Dec −18.048. 5 RA + 6 Dec chords (≤0.15%), all slow (exact hours or a day away).
  - RA Altair–Antares 1:3:4 (16.776/67.123/50.347; 14:57) — Good Effort Vesta 0.009%; RA Aldebaran–Procyon 2:5:7 (1 Jan 17:36) — Jason Watson 0.037%, then CONNOR BEASLEY Venus 0.040%, VENTUROUS Makemake 0.043%; RA Altair–Betelgeuse 1:8:9 — Jason Watson; RA Altair–Arcturus 1:5:6 — Jim Crowley Eris 0.022%; RA Algorab–Fomalhaut φ — Regional; Dec Equator–Rigel 5:6:11 (18.048/9.846/8.202; 15:53) — Daniel Tudhope 0.010%; Dec Algol–Pleiades 2:5:7 — Jim Crowley 0.010%; Dec Aldebaran–Algol √2 div. — Daniel Tudhope; Dec Arcturus–Procyon 3:5:8 — Regional; Dec Algol–Rigel 1:5:6 — Cam Hardie; Dec Alkaid–Altair 2:3:5 — Jason Watson 0.001%.
  - SATURN SITS ON CAM HARDIE'S (2nd) natal GONGGONG Dec (0.005°) → his Gonggong in UNISON with Saturn on four Dec strings (Algol–Rigel, Algol–Pleiades, Equator–Rigel, Aldebaran–Algol) plus Arcturus–Procyon.
  - Winning pair tightest on NONE of Saturn's 11 chords (best: Connor Beasley Venus 2nd and Venturous Makemake 3rd on Aldebaran–Procyon, ~0.04%).
- CERES ON THE STARS, NEWCASTLE. Ceres at the off RA 56.407, Dec 17.797. 3 RA + 12 Dec chords; all slow.
  - Winning pair tightest on ONE: Dec Alphecca–Altair 1:1:2 (Ceres at the Dec midpoint: 8.914/8.927, base 17.841; exact 10:15, separating) — VENTUROUS PLUTO 5:8:13 0.016%. Also RA Capella–Polaris 4:5:9 (22.774/18.226/41.000; APPLYING through the race, exact 14:25) — VENTUROUS SUN the only UNISON (4:5:9, 0.057%; Cam Hardie Transpluto 0.022% tighter on another chord).
  - Others: Algol–Spica 4:5:9 (King Of Stars 0.015%; Connor Beasley Orcus 0.033% 3rd), Algorab–Bellatrix 1:2:3 (Regional 0.002%; Connor Beasley Mars 0.030% 2nd), Algorab–Fomalhaut φ (Regional 0.011%; Connor Beasley Pluto 0.029% 2nd), Procyon–Vega 3:5:8 (King Of Stars / Daniel Tudhope 0.002%), Alkaid–Pleiades 1:4:5 (Cam Hardie 0.008%), Equator–Fomalhaut (Cam Hardie 0.022%), Deneb Algedi–Sirius RA 1:2:3 (Jason Watson 0.008%), Altair–Polaris (Jim Crowley), Antares–Polaris φ (King Of Stars), Altair–Pleiades √2 div. (King Of Stars), Deneb Algedi–Vega φ (Mondammej), Algol–Alphecca (King Of Stars), Betelgeuse–Vega φ (Connor Beasley Saturn only, loose 0.127%).
  - Ceres spreads across the field; Cam Hardie, King Of Stars and Regional take most. Connor Beasley 2nd/3rd on three.
  - Eddie 18:48: "Dec 17.79 a phi number itself". Yes — Ceres Dec at the off 17.79736 = 11φ (17.79837) to −0.006%; Ceres's Dec is rising 0.0019°/h, so it reaches exactly 11φ at about 14:05, ~32 min after the off (applying). (Ceres–Equator in Dec = 11φ: the distance from the equator point itself is a φ number.) Not φ⁶ (17.944).
- NUMBER CHECK added (Eddie 19:26: "add that check because I think they are there"). scratchpad numcheck.py: is the body's Dec (from the equator), RA, or its RA/Dec distance to each star itself a special number — kφ, φⁿ, 10φⁿ, k√2, k/9, whole — within ±0.002°. 47 values per body. CORRECTED 19:35: chance hits expected per body ≈ 0.44 for φ/√2/whole together and ≈ 1.5 for ninths (ninths are 9 to the degree — the earlier '0.6' under-counted them).
  - CERES (3 φ/√2/whole hits vs 0.44 expected; 1 ninth vs 1.5): Dec 17.7974 = 11φ (17.7984); Dec to Rigel 25.9998 = 26 (whole); RA to Vega 137.1777 = 97√2 (137.1787); RA to Spica 144.8903 = 1304/9.
  - PALLAS: none at ±0.002 (at ±0.004 only three ninths, ≈ chance).
- PALLAS ON THE STARS, NEWCASTLE. Pallas at the off RA 350.489, Dec −11.962. 3 RA + 11 Dec + 1 Flat + 1 Sky chords.
  - RA Regulus–Rigel 5:6:11 (161.606/88.151/73.455; 0.006% at the off, APPLYING, exact 14:01:37) — Mondammej Ketu and Jason Watson Haumea 0.013% tightest; Connor Beasley Juno 4th (0.059%).
  - Winning pair tightest on ONE: Dec Antares–Capella 1:4:5 (14.469/57.959/72.428; exact 23:54) — VENTUROUS KETU 2:3:5 0.010%. 2nd places: Dec Alkaid–Antares φ (Daniel Tudhope 0.000%, CONNOR BEASLEY QUAOAR 0.007%), Dec Alphecca–Polaris φ (King Of Stars 0.008%, CONNOR BEASLEY CHIRON 0.010%), Dec Castor–Regulus 5:6:11 (Cam Hardie 0.003%, VENTUROUS SEDNA 0.011%).
  - Pallas at the Equator–Regulus Dec midpoint (11.962/11.966, 1:1:2) — Jim Crowley Ceres 0.086%, Venturous's own PALLAS 0.106% (same body, loose).
- JUNO ON THE STARS, NEWCASTLE. Juno at the off RA 288.025, Dec −13.814 (sitting on Connor Beasley's natal Quaoar Dec, 0.006°).
  - Two Juno chords exact together at 13:50:49 (18 min after the off, applying through the race): RA Aldebaran–Fomalhaut 2:3:5 (140.961/56.387/84.574; 0.009% at the off) — the FAVOURITE GOOD EFFORT's own JUNO in UNISON 0.016% (tightest; same body); Dec Betelgeuse–Spica 1:7:8 (21.221/2.653/18.568) — Regional Jupiter 0.004%, Good Effort Ceres 0.013%, Venturous ORCUS φ 3rd 0.021%.
  - CONNOR BEASLEY'S QUAOAR in UNISON with Juno on four Dec strings (the parallel): Alkaid–Antares 1:5:6 (0.007%, 2nd to Daniel Tudhope 0.000%), Algol–Altair √2 div. (0.038%), Altair–Bellatrix 1:8:9 (0.044%, tightest), Alkaid–Vega 1:5:6 (loose). Polaris–Regulus 1:3:4: Venturous Rahu 0.019% 3rd, Connor Beasley Rahu 0.029% 4th.
  - Others: Antares–Bellatrix (King Of Stars 0.004%), Alphecca–Regulus RA 2:3:5 (Daniel Tudhope 0.016%), Arcturus–Regulus RA 5:6:11 (Jim Crowley Mars 0.020% — the same Arcturus–Regulus string Mars plays 5:8:13).
  - Numbers: Dec to Betelgeuse 21.2206 ≈ 191/9; Dec to Regulus 25.7796 ≈ 232/9 — two ninths (chance level is 1.5).
- VESTA ON THE STARS, NEWCASTLE. Vesta at the off RA 264.712, Dec −21.123 (0.023° from Connor Beasley's natal Neptune Dec). Few chords: 2 RA, 3 Dec, 2 Flat, 1 Sky — none tightening onto the race.
  - Winning pair tightest on ONE: Dec Arcturus–Capella 2:3:5 (40.291/67.120/26.829; exact 1.2 days ago, separating) — VENTUROUS URANUS φ 0.020% (Good Effort Eris 0.037%).
  - Others: Dec Pleiades–Rigel 2:5:7 (45.229/12.921/32.308; exact 14:57) — Daniel Tudhope 0.050%; RA Alphecca–Deneb Algedi 1:2:3 (31.043/62.046/93.089; exact 12:57) — Daniel Tudhope; RA Pleiades–Rigel 1:7:8 — Daniel Tudhope Makemake 0.005%; Flat Fomalhaut–Spica 4:5:9 — Jason Watson; Connor Beasley's own Vesta on it, loose (0.124%).
  - NUMBERS: RA distance to Sirius 163.4220 = 101φ (163.4214, diff 0.0006°); RA to Algol 142.3351 ≈ 1281/9. (1 φ hit vs 0.44 expected; 1 ninth vs 1.5.)
- NUMBER CHECK, ALL BODIES TO SATURN + ASTEROIDS (Newcastle, at the off, ±0.002°; expected per body: φ/√2/whole 0.44, ninths 1.5):
  - Sun: ninths only — Dec to Alkaid 72.2221 = 650/9 (to 0.0001°), RA to Capella 1407/9, RA to Polaris 1038/9. Mercury: 2 ninths. Venus: 1 ninth. Mars: none. Jupiter: 3 ninths. Saturn: Dec to Arcturus 37.2161 = 23φ, Dec to Betelgeuse 25.4549 = 18√2, plus 3 ninths. Ceres: 11φ (Dec), 26 (Dec to Rigel), 97√2 (RA to Vega), 1 ninth. Pallas: none. Juno: 2 ninths. Vesta: 101φ (RA to Sirius), 1 ninth.
  - TOTALS over 10 bodies: φ/√2/whole 6 (expected 4.4); ninths 16 (expected 15) — overall at chance level; CERES stands out (3 vs 0.44).

### §67 cont. — Natal number check (winning pair) and Uranus
- Natal special numbers (steady values, ±0.002°): the whole field sits around chance level; Venturous 4 vs 6.7 expected, Connor Beasley 6 vs 5.7; King Of Stars (last) highest at 2.13×. Eddie: "does not mean much on their own". Horse × jockey cross distances not yet checked.
- **Uranus** (RA 38.338, Dec 14.625). The only chords exact on the day are both hours from the race:
  - RA 3:5:8 on Bellatrix–Deneb Algedi, exact 11:48 (0.003% at the off, separating). Tightest is Jim Crowley's Chiron (0.054%); the winning pair is not close.
  - Dec 1:3:4 on Altair–Castor, exact 15:33 (0.007% at the off, applying). Jim Crowley's Pallas 0.044%; Connor Beasley's Sun φ next at 0.045%.
  - The rest are days off and loose (0.05–0.14%). The closest single holding is Connor Beasley's Chiron at 0.013% on Alphecca–Vega φ, but the sky chord there is loose (0.142%).
- No slow parallel for the winning pair (Uranus Dec is near Daniel Tudhope's Transpluto and King Of Stars's Ceres, both loose at 0.07–0.10°).
- Number check: 2 ninths (Dec to Algol 237/9, RA to Vega 1072/9) vs 1.5 expected; no φ/√2/whole. Chance level.
- What we see: Uranus is quiet for the winning pair. Where it touches anyone near the race, it is the favourite's jockey.

### §67 cont. — Neptune (RA 351.620, Dec −4.849)
- Three Dec chords come exact on race day. None of them goes to the winning pair at the off:
  - Alphecca–Spica 1:5:6, exact 13:20 (0.001% at the off). Mondammej's Jupiter (2nd) is tightest at 0.023%.
  - Equator–Vega 1:8:9, exact 15:29. Jason Watson's Jupiter is tightest.
  - Procyon–Rigel 1:3:4, exact 18:13 (0.055% at the off, applying).
- **Procyon–Rigel Dec 1:3:4 — Connor Beasley's ORCUS (the imprint hub), UNISON 0.001%, the only tight chart.** It is a mirror inside the string:
  - Sky Neptune–Procyon 10.067, Neptune–Rigel 3.354 (base 13.420).
  - Natal Orcus–Procyon 3.357, Orcus–Rigel 10.071.
  - The distances are the same, swapped end for end: Neptune sits a quarter in from Rigel, his Orcus a quarter in from Procyon.
  - Families: 4/3, 4 and 3, all perfect.
- **Altair–Arcturus Dec 3:4:7 (0.080%, 1.5 d old): Venturous's ORCUS is tightest (5:8:13, 0.032%).**
  - Both Neptune and his Orcus are beyond the Altair end of the string: sky 13.719/24.017, natal 16.483/26.789.
  - This is the same Altair–Arcturus base as Mars at the Doncaster off.
- So **Neptune reaches the Orcus of both winning charts**: the jockey's through an exact mirror, the horse's loosely.
- Others: Good Effort's Neptune on Algol–Bellatrix φ (0.006%); Mondammej's Gonggong on Capella–Regulus.
- No slow parallel.
- Number check: 3 ninths (Dec to Algorab 105/9, RA to Bellatrix 807/9, Dec to Fomalhaut 223/9) vs 1.5 expected; no φ/√2/whole.

### §67 cont. — Pluto (RA 298.006, Dec −22.704, close to the Sun)
- Only one chord comes exact on race day: Dec 1:6:7 on Arcturus–Sirius, exact 04:50 (0.027% at the off, separating).
  - The favourite pair is 1st and 2nd: Good Effort's Mars φ (0.025%) and Jim Crowley's Sedna (0.041%).
- Winning pair: only loose holdings.
  - Venturous's Mars on Antares–Spica Sky 1:1:2 (0.077%; the sky chord is 0.099%, 1.1 d old).
  - Venturous's Haumea on Fomalhaut–Spica (0.103%).
- No slow parallel.
- Number check: 2 ninths (Dec to Betelgeuse 271/9, RA to Vega 169/9) vs 1.5 expected. Chance level.
- What we see: Pluto is quiet for the winning pair. The one chord exact that day goes to the favourite pair.

### §67 cont. — Chiron (RA 6.698, Dec 5.241)
- No star chord comes exact on race day; all are 1–6.5 d away.
- The tightest at the off is Aldebaran–Arcturus Dec φ (φ³ family), 0.019% and applying (exact in 1 d). Jim Crowley's Mercury is tightest at 0.024%.
- The favourite pair shows again:
  - Good Effort's Mars on Arcturus–Fomalhaut (0.015%).
  - Good Effort's Neptune on Algorab–Rigel φ (0.011%).
- Winning pair: loose only (Venturous's Makemake 0.074%, Pluto 0.105%; Connor Beasley's Pluto 0.064%).
- On the star bases Chiron is quiet for the winners. The one earlier Chiron link stays where it was found, off the star layer (L4): Chiron 1:8:9 on Sun–Antares, with Venturous's Neptune tightest (0.009%).
- No slow parallel. Number check: 1 ninth (Dec to Rigel 121/9) vs 1.5 expected.
- Running pattern: Mars, Jupiter and Neptune play the winning pair; Uranus, Pluto and Chiron lean to the favourite pair.

### §67 cont. — Eris (RA 25.826, Dec −1.497)
- No star chord comes exact on race day. The tightest at the off:
  - Flat Altair–Rigel 3:5:8, 0.011% (exact in 1.1 d). Nobody close (Jim Crowley's Uranus 0.076%).
  - Dec Procyon–Vega 1:5:6, 0.020%. King Of Stars's Quaoar and Daniel Tudhope's Rahu are both at 0.002%.
  - RA Fomalhaut–Pleiades 3:4:7, 0.033%. Good Effort's Mars is at 0.028%.
- **Procyon–Rigel again.** Eris sits almost exactly at the Dec midpoint (6.715 / 6.706, 1:1:2, 0.135%, 3.5 d away). Connor Beasley's Orcus is again the tightest chart on that string (his own 1:3:4, 0.001%).
  - The string now carries three points: Neptune a quarter in from Rigel, Eris at the middle, and his natal Orcus a quarter in from Procyon (Dec −4.849 / −1.497 / ≈ +1.86).
  - Number check: Eris RA to Procyon = **89 whole** (89.0009).
- **Venturous's Orcus again**: tightest on Bellatrix–Equator φ (0.015%), but the sky chord is loose (0.144%).
- Other winning-pair holdings, each tightest but on loose sky chords:
  - Venturous's Mercury on Arcturus–Deneb Algedi √2 (0.012%; sky 0.149%).
  - Connor Beasley's Pallas on Alkaid–Alphecca (0.017%; sky 29 d old).
- Slow parallel: Eris on Good Effort's Chiron Dec (0.050°), for the favourite.
- Number check: 1 whole (89, to Procyon) vs 0.44 expected; 2 ninths (RA to Algol 191/9, Dec to Arcturus 186/9) vs 1.5. Chance level overall.
- **Procyon–Rigel (Dec) whole-string check** (Eddie 19:46: "looks interesting and the type of thing we are looking for"):
  - Sky: only Neptune (1:3:4, 0.055%) and Eris (1:1:2, 0.135%) make chords on it at the off. No other body does, the Sun through the nodes and TNOs included.
  - Natal: the only body tight on it in any chart is Connor Beasley's Orcus (1:3:4, 0.001%); the rest of the charts show only star variants. Daniel Tudhope's Gonggong 1:1:2 sits beyond the Rigel end (0.015%). Venturous has nothing on it.
  - The Moon makes no chord on it in the hour (it is 19° beyond Rigel in Dec), so the clock does not strike this string at Newcastle.
  - The string is slow: nothing on it says *when*.

### §67 cont. — Sedna (RA 58.456, Dec 8.005; the slowest body: exact times are days to months away)
- Tightest at the off: Aldebaran–Alphecca Dec 5:6:11, 0.004% (1.9 d old). **Cam Hardie's Saturn 0.000%** (the runner-up's jockey; Saturn held him before). Venturous's Neptune is 3rd (0.050%).
- **Connor Beasley, twice:**
  - Deneb Algedi–Pleiades Dec 2:3:5 (0.061%): **his Juno is tightest (3:5:8, 0.010%) and his Vesta 2nd (0.037%)**. Both Sedna and his Juno are inside the string: sky 24.136/16.101, natal 15.087/25.142.
  - Alkaid–Antares Dec 5:6:11 (0.050%): **his Quaoar at 0.007%** (1:5:6, beyond the Antares end, 63.126/12.624). Daniel Tudhope's Mars is 0.000%.
  - Juno and Quaoar are the same two bodies already linked by the slow parallel (sky Juno on his Quaoar, 0.006°).
- Slow parallel: Sedna on Jason Watson's Pallas Dec (0.014°).
- Number check: Dec to CourseLat = **φ⁸** (46.9777 vs 46.9787); ninths: RA to Antares 1540/9, Dec to Vega 277/9. That is 1 φ vs 0.44 expected and 2 ninths vs 1.5. Chance level.

### §67 cont. — Haumea (RA 217.349, Dec 14.927)
- Two chords come exact on race day, both in the evening:
  - RA 1:4:5 on Alphecca–Regulus, exact 22:11. Daniel Tudhope's Makemake is tightest (0.016%).
  - **Dec 1:3:4 on Arcturus–Castor, exact 22:29** (0.035% at the off, applying). **Connor Beasley's Mercury is tightest at 0.005%** (1:7:8).
    - Both are beyond the Arcturus end: sky Haumea 4.241/16.959 (base 12.718), natal Mercury 1.814/14.515.
    - The sky distance Haumea–Arcturus Dec 4.2409 = **3√2** (number check).
- Connor Beasley's Mars is 2nd on Algorab–Bellatrix 3:8:11 (0.030%; Regional's Makemake 0.002%).
- His own Haumea is only loose on sky Haumea's chords (Capella–Deneb Algedi, 0.079%). His Haumea is played instead by Jupiter (Betelgeuse–Deneb Algedi) and by the Makemake parallel.
- Favourite side: Good Effort's Jupiter on Pleiades–Vega (0.007%); Jim Crowley's Jupiter √2 on Bellatrix–Deneb Algedi (0.014%).
- No slow parallel.
- Number check: Dec to Arcturus 3√2 and Dec to Procyon 6φ (2 vs 0.44 expected); 1 ninth (RA to Arcturus 31/9) vs 1.5. Both φ/√2 hits sit on stars of chords in play: Arcturus (his Mercury chord) and Procyon (his Orcus string).

### §67 cont. — Makemake (RA 199.283, Dec 22.124)
- No star chord comes exact on race day. Makemake **sits on Connor Beasley's natal Haumea Dec (22.124 vs 22.115, 0.008°)**, so his Haumea makes the **same chord (UNISON) on every Makemake Dec string**. It is the tightest chart on three of them:
  - Capella–Procyon √2 (1:√2:1+√2): his Haumea UNISON **0.003%** (sky 0.147%). Procyon again.
  - **Betelgeuse–Deneb Algedi 5:8:13: his Haumea UNISON 0.008%** (sky 0.040%, exact 23.6 h before). This is the same base where Jupiter makes 1:5:6 with his Haumea (exact 13:34:37), so two sky bodies hold his Haumea on one string.
  - Algorab–Capella φ: his Haumea UNISON 0.028% (sky 0.030%).
  - Also in UNISON, but not tightest: Altair–Antares 3:8:11 (0.054%) and Fomalhaut–Rigel √2 (0.073%).
- Venturous: his Makemake is tightest on Antares–Capella RA (0.067%, loose); his Neptune is on Bellatrix–Castor φ (0.042%).
- Favourite side: Good Effort's Ketu on Castor–Vega √2 (0.003%); Jim Crowley's Chiron on Bellatrix–Regulus (0.020%).
- Second slow parallel: Makemake RA on Mondammej's (2nd) Jupiter (0.063°).
- Number check: 1 ninth (Dec to Antares 437/9 = 48.5548) vs 1.5. This echoes his natal Haumea–Antares Dec 30φ (48.542–48.554), because Makemake sits on his Haumea Dec. The sky value itself is 0.014 off 30φ, outside tolerance.

### §67 cont. — Quaoar (RA 275.705, Dec −15.532)
- No star chord comes exact on race day. The tightest at the off:
  - RA 1:1:2 on **Arcturus–Regulus** (0.018%, exact 00:04 next day). This is the string where Mars makes 5:8:13 with Venturous's Sedna mirrored. On Quaoar's chord the tightest is Jim Crowley's Mars (0.020%); the winning pair is not in the top four.
  - Dec φ on Procyon–Vega (0.023%). King Of Stars's Quaoar UNISON and Daniel Tudhope's Rahu are both at 0.002%.
- Same-age horses share the natal Quaoar Dec, so sky Quaoar sits near four horses' Quaoar: King Of Stars 0.008°, Mondammej 0.028°, Regional 0.049°, Venturous 0.073°. King Of Stars (last) is closest and takes the UNISONs.
- Winning pair: nothing on Quaoar's chords. The jockey's Quaoar is played by sky Juno (parallel 0.006°) and Sedna instead.
- Number check: no hits (0 vs 0.44; 0 ninths vs 1.5).
- What we see: Quaoar is quiet for the winners.

### §67 cont. — Orcus (RA 157.392, Dec −12.161)
- Nothing on sky Orcus plays Connor Beasley's Orcus hub. His Orcus is held by Neptune (the Procyon–Rigel mirror), with Eris at the middle of that string.
- One chord comes exact on race day: Flat 3:5:8 on Algol–Procyon at 19:54. It is loose (0.11%), and the tightest charts there are not the winners'.
- Tightest at the off: RA φ on Algorab–Rigel (0.027%, exact 09:19 next day). Nobody is close (Daniel Tudhope's Makemake 0.065%).
- Venturous: **his Rahu is tightest on Algol–Regulus Dec (1:1:2, 0.010%)**. The sky chord is loose (5:6:11, 0.140%). Both points are beyond the Regulus end: sky 53.119/24.126, his Rahu 57.984/28.994, one base length out (base 28.992).
- **Slow parallel: sky Orcus sits on Jim Crowley's natal Eris Dec (0.047°).** This explains the one live discord: the Mercury–Orcus–Deneb Algedi √2 caught Jim Crowley's Eris, because sky Orcus is sitting on his Eris Dec.
  - Also near Regional's Gonggong (0.085°).
- Number check: Dec to Spica = **1 whole** (0.9998), vs 0.44 expected; no ninths.

### §67 cont. — Gonggong (RA 336.274, Dec −11.493)
- No star chord comes exact on race day.
- Tightest at the off:
  - Flat Arcturus–Polaris 15:16:24 (0.019%; nobody tuned).
  - RA Altair–Capella 3:8:11 (0.023%); only Regional's Sun, loose.
  - Dec Aldebaran–Altair 3:8:11 (0.023%); Jim Crowley's Jupiter at 0.054% and Venturous's Eris at 0.077%.
- Winning pair: nothing tight. Venturous's own Gonggong (his imprint body) is not on any sky-Gonggong chord. His Gonggong showed only in the fast points (Part of Spirit at the off, Part of Fortune at the finish).
- Favourite side: Jim Crowley's Vesta on Pleiades–Vega √2 (0.006%). Others: Cam Hardie's Makemake (0.008%), Jason Watson's Ceres (0.008%).
- No slow parallel.
- Number check: Dec to Aldebaran = **28 whole** (28.0017), plus 1 ninth (Dec to Spica 3/9). This echoes Connor Beasley's natal **Gonggong–Aldebaran Dec = 25√2**: the same pair of points is special in the sky (whole) and in his chart (√2), but with different values.

### §67 cont. — Transpluto (RA 155.130, Dec 10.332)
- Four chords come exact on race day. None goes to the winners at its exact time:
  - Dec Aldebaran–Rigel 1:3:4 at 02:57.
  - Dec Equator–Pleiades 3:4:7 at 07:22.
  - Dec Altair–Procyon 2:5:7 at 10:18 (Venturous's Mars is tightest but loose, 0.062%).
  - RA Aldebaran–Sirius 3:5:8 at 17:05 (0.001% at the off). Cam Hardie's Neptune is 0.014%; Connor Beasley's Sedna is 2nd at 0.033%.
- **★ Bellatrix–Procyon RA 5:6:11: Venturous's Sedna UNISON 0.000% and his Orcus 0.004%**, the two tightest in the field.
  - The sky chord is loose (0.143%, within range 08:32–18:31, so held through the race).
  - Mirror shape: sky Transpluto is beyond the **Procyon** end (40.304/73.842, base 33.539); his Sedna is beyond the **Bellatrix** end (27.953/61.496). Same chord, opposite ends.
  - His Orcus is 1:1:2, one base length beyond Procyon (33.542), on the same side as sky Transpluto.
  - Procyon again, and the horse's Orcus again (Neptune on Altair–Arcturus and Eris on Bellatrix–Equator also went to his Orcus).
- **★ Aldebaran–Bellatrix RA 1:6:7 (0.037%, steady): Connor Beasley's Saturn tightest, 0.006%** (his Pallas √2 2nd, 0.031%).
  - True mirror about Aldebaran: sky Transpluto is 86.145 from Aldebaran on the Bellatrix side (7 base lengths); his Saturn is 86.107 from Aldebaran on the far side (7 base lengths; 1:7:8).
  - His Saturn is the imprint body (#12 landed on it alone).
- Connor Beasley also: Algorab–Alkaid 3:5:8 (his Quaoar 0.015%, then his Saturn and Pallas, 1st–3rd); his Juno 2nd on Aldebaran–Algorab (0.014%).
- Favourite side: Jim Crowley's Makemake 0.003% (Aldebaran–Algorab), his Saturn 0.009% (Bellatrix–Spica).
- No slow parallel.
- Number check: **5 ninths** vs 1.5 expected: Dec from the Equator 93/9, RA to Algorab 291/9, RA to Betelgeuse 597/9, Dec to Capella 321/9, Dec to Castor 194/9. No φ/√2/whole. More ninths than any of the outer bodies (Uranus–Gonggong had 0–3 each).

### §67 cont. — The nodes (Rahu RA 58.674 Dec +20.320; Ketu opposite)
- **Ketu RA 1:4:5 on Arcturus–Procyon, exact 13:09:25 (23 min before the off)**: 0.002% at off−30, 0.005% at the off, 0.006% at the finish (separating).
  - The runner-up's Mars (Mondammej) is tightest at 0.005%.
  - **Connor Beasley's Sedna is 2nd at 0.008%**, his own √2 (169.159/70.065).
- **★ Rahu Dec √2 on Deneb Algedi–Procyon (0.038%, exact 21:58): Venturous's Pluto is tightest at 0.001%** (his 1:6:7). Mirror shape:
  - Sky Rahu is beyond the **Procyon** end (36.450/15.102).
  - His Pluto is beyond the **Deneb Algedi** end (3.558/24.907).
  - Base 21.349.
- Rahu RA 1:1:2 on Capella–Polaris (exact 11:37): Venturous's Orcus and Sun are 2nd and 3rd (0.057%) behind Cam Hardie's Transpluto.
- Ketu Dec Bellatrix–Pleiades 2:3:5: Venturous's Sun is tightest (0.016%), but the sky chord is loose (0.127%).
- Favourite side: little. Cam Hardie's Saturn is 0.005–0.007% on two Ketu chords (Arcturus–Pleiades, Regulus–Rigel), again the runner-up's jockey on Saturn.
- No slow parallel. Number check: 1 ninth each (Rahu RA to Vega 1255/9; Ketu Dec to Antares 55/9, RA to Vega 365/9).

### §67 — PROCYON across the Newcastle slow-body read (what we see)
| body | string | who |
|---|---|---|
| Neptune (1:3:4) + Eris (midpoint) | Procyon–Rigel Dec | jockey Orcus, mirror |
| Makemake (parallel) | Capella–Procyon Dec √2 | jockey Haumea UNISON 0.003% |
| Transpluto | Bellatrix–Procyon RA 5:6:11 | horse Sedna UNISON 0.000% (mirror), horse Orcus 0.004% |
| Rahu | Deneb Algedi–Procyon Dec √2 | horse Pluto 0.001% (mirror) |
| Ketu (exact 23 min before off) | Arcturus–Procyon RA 1:4:5 | jockey Sedna √2 2nd (0.008%) |

- Numbers: Haumea Dec to Procyon 6φ; Eris RA to Procyon 89.
- Caution: Procyon is one of about 20 stars and every body makes many chords. The base rate (how often any one star collects this many winner holdings) has not been checked.

## 68. QUICK LOOK — York 14:40, 24 Jul 2021 (Sky Bet Dash, 6f): Venturous 33/1 SP (Eddie: 25/1), Connor Beasley — the same pair as Newcastle
- Eddie: 14 ran; off 14:41:03; winning time 1m 12.63s (slow by 2.43s); finish 14:42:16; total SP 120%. Mondammej/Cam Hardie 7th.
- Set-up: the winning pair only (no field, so "tightest in the field" cannot be judged here). Race id 20210724_york_1440.
  - Natal rows copied from Newcastle. Sky from the same engine; York 53.9948, −1.0859, 19 m.
  - The TNOs have no ephemeris file here. They were fitted as straight-line heliocentric motion with Earth and aberration, from 22 races' TRANS_POS (Aug–Oct 2021). Holding out a race 18 d beyond the fit gave errors ≤0.00012°.
  - Script: scratchpad setup_york.py + tnofit.py.
- The Moon is again near its southern Dec limit (−23.1°). No Moon crossing of either chart. Slow parallels are loose: Mars on the jockey's Transpluto 0.049°, Jupiter on the horse's Saturn 0.059°.
- **Repeats from Newcastle (the same natal holding, played by a different sky body):**
  - **Bellatrix–Procyon RA: the horse's Sedna 0.000% / Orcus 0.004%.** Played by Pallas φ (0.075%) and Juno 1:4:5 (Newcastle: Transpluto).
  - **Deneb Algedi–Procyon Dec: the horse's Pluto 0.001%.** Played by Makemake 5:6:11 (0.075%) (Newcastle: Rahu √2).
  - **Arcturus–Castor Dec: the jockey's Mercury 0.005%.** Played by Eris 5:8:13 (0.022%) (Newcastle: Haumea 1:3:4).
  - **Jupiter–Deneb Algedi: the horse's Uranus 2:3:5 (0.043%).** Struck by the **Moon (RA φ) at 14:41:15, 12 s after the off** (Newcastle: Neptune 1:3:4, 3 min before the off).
  - **Ceres–Betelgeuse RA: the jockey's Orcus 3:5:8 0.004%.** Played by Gonggong 2:5:7 (0.017%) (Newcastle: Neptune 1:2:3). Gonggong is the horse's imprint body.
- **Not played at York:** Procyon–Rigel (the jockey's Orcus mirror), Capella–Procyon, Alkaid–Regulus (Mars), Betelgeuse–Deneb Algedi, Aldebaran–Bellatrix, Altair–Arcturus, Arcturus–Procyon, Algol–Regulus.
- Around the off (pair only):
  - Moon on Saturn–Altair 1:8:9 at 14:39:05: the horse's Pallas 0.005%.
  - Mars φ on Uranus–Transpluto at 14:39:54: the jockey's Juno √2 0.010%.
  - Mars–Capella + Rahu at 14:40:30: the jockey's Sedna.
  - Sun–Fomalhaut + Moon at 14:41:41 (in the race): the jockey's Pallas 0.025%.
- Tightest pairings overall:
  - Gonggong φ on Capella–Pleiades (0.000%): the horse's Pluto 0.011%.
  - Neptune 1:2:3 on Altair–Fomalhaut (0.009%): the jockey's Uranus 0.004%.
  - Ceres/Ketu on Bellatrix: the jockey's Ceres/Ketu 0.005% (both ways round).
- Cautions:
  - The natal holdings on star strings are fixed for life. What changes is which sky body plays the string. A tight natal holding gets played often, so the base rate is needed.
  - The pair is read alone, with no field to compare.

## 69. Newcastle (and York) against the star-lattice power points (the §42 nodes) — Eddie 21:27 "was there any connection to the power points we identified in the stars yesterday"
- Script: scratchpad powerpt.py. Load = how many star pairs a position completes a full chord with (Dec or RA; full interval list, 0.15%), with the race-day stars.
  - Background on 2 Jan 2022: Dec mean 5.6, 99% 12, 99.9% 14; RA mean 4.1, 99% 10, 99.9% 13.
  - Natal points are measured against each chart's own birth-day stars.
- **Sky at the Newcastle off:** only ONE body sits on a power point — **Transpluto, RA 155.130, completing 11 star pairs (99% level)**. Ceres Dec 17.797 completes 11 (just under the Dec 99% of 12). Every other body is at 0–9.
  - The Moon peaks at only 5 (it is at Dec −27.3, below the lattice).
  - **Transpluto's 11 pairs include the chords that hold the winners:**
    - Bellatrix–Procyon (Venturous's Sedna UNISON 0.000%, his Orcus 0.004%, mirror).
    - Aldebaran–Bellatrix (Connor Beasley's Saturn 0.006%, mirror about Aldebaran).
    - Algorab–Alkaid (Connor Beasley's Quaoar / Saturn / Pallas 1st–3rd).
    - Aldebaran–Algorab (his Juno 2nd).
    - Aldebaran–Sirius (his Sedna 2nd).
  - So the one sky body on a power point is the one whose chords hold BOTH winning charts.
- **Natal:** neither Venturous nor Connor Beasley has a natal point on a power point. Others do: Good Effort's Ceres Dec (14), Jason Watson's Sun RA (14), King Of Stars's Sun Dec (12), Daniel Tudhope's Makemake RA (12), Cam Hardie's Transpluto RA (10).
- **York 24 Jul 2021:** no sky body on a power point (the Moon peaks at 5, again at the bottom of the lattice, Dec −23); neither natal chart on one.
- Caution: §43/§44 showed the lattice and its nodes are what any 22 points would give. A body on a node is a fact of where it is, not yet a tested signal.

## 70. SECOND LOOK — Wincanton 14:20, 21 Mar 2022 (River Bray 22/1, Alan Johns), read the Newcastle way (Eddie 21:32)
### Sun (RA 0.583, Dec +0.251; the equinox is the day before, so the Sun sits on the equator)
- **★ RA 1:6:7 on Antares–Fomalhaut, exact 14:23:28, in the race.** Deviation 0.128% at off−30 → 0.011% at the off → exact → 0.008% at the finish → 0.103% at off+30. It comes into range and goes out around the race.
  - **Alan Johns's Makemake is tightest, 0.001%** (his 4:5:9). Next is Guernesey (2nd) Haumea at 0.013%.
  - Opposite ends of the string (base 97.055):
    - Sky Sun is beyond the **Fomalhaut** end (113.229/16.174; Sun–Fomalhaut = 1/6 of the base).
    - His Makemake is beyond the **Antares** end (77.656/174.724; Makemake–Antares = 4/5 of the base).
  - Families: sky 7/6 septimal, 6 and 7 harmonic.
  - His Makemake is the imprint body (the busiest; horse Makemake × jockey Haumea).
- **Dec 3:5:8 on Aldebaran–Bellatrix, exact 14:25:22, 4 s before the finish** (0.022% at the off → 0.0005% at the finish).
  - The favourite's jockey **Rex Dingle's Makemake is tightest, 0.002%**. It is a mirror about Aldebaran: Sun–Aldebaran 16.255 on the Bellatrix side, his Makemake–Aldebaran 16.256 on the other side.
  - River Bray's Mercury √2 is at 0.033%.
- Others near the off: Altair–Capella 4:5:9 exact 14:06 (Ballyblack's Eris 0.003%); Fomalhaut–Spica φ exact 14:03 (Rex Dingle's Venus 0.010%).
- River Bray (horse) is only loose on the Sun's chords (Chiron on Altair–Sirius 0.069%; Juno on Algol–Pleiades √2 0.023%, behind Reserve Tank 0.012%).
- No slow parallel for the pair (the Sun's RA is near Birds Of Prey's Mercury, 0.061°).
- Number check: no hits (0 vs 0.44; 0 ninths vs 1.5).
- (sunchords day list: rows over 0.15% are lookup noise and are ignored.)
### Mercury (RA 350.790, Dec −6.311)
- **★ Dec 3:8:11 on Alkaid–Altair: River Bray's QUAOAR (the #1 imprint body) is tightest at 0.020%** (his Pluto is the only other chart, 0.135%).
  - Applying through the race: 0.187% at off−30, 0.085% at the off, 0.069% at the finish, 0.015% at off+30; exact 14:45:53.
  - Both points are beyond the Altair end (base 40.44): sky Mercury 55.621/15.179 (3/8 of the base out); his Quaoar 64.721/24.273 (3/5 of the base out).
  - **The same string is where the Moon makes Dec 3:5:8 at 14:24:30, in the race, with his Quaoar in UNISON (0.020%, the only chart; §64).** So slow Mercury holds the string through the race and the Moon strikes his Quaoar's own chord on it.
- **RA 2:5:7 on Alphecca–Polaris: Alan Johns's RAHU is tightest at 0.026%** (his Rahu took #10 Makemake/Pluto alone in the imprint).
  - Applying: 0.151% at off−30, 0.049% at the off, 0.033% at the finish; exact 14:35:05.
  - Both points are inside the string: sky 117.114/46.869, his Rahu 91.488/73.210 (4:5:9).
- Dec 2:3:5 on Castor–Polaris (0.141%, separating): Alan Johns's Vesta is tightest at 0.013%.
- Others: Algorab–Equator φ exact 14:23:39, in the race (Nick Scholfield's Haumea 0.019%); Altair–Capella (Ballyblack's Eris 0.003%); Alphecca–Equator (Brendan Powell's Sedna 0.007%).
- No slow parallel. Number check: Dec to Spica 3φ (4.8523 vs 4.8541, applying to 4.8549 at the finish); RA to Vega 644/9. That is 1 φ vs 0.44 and 1 ninth vs 1.5.
### Venus (RA 315.978, Dec −14.771)
- **★ Dec 4:5:9 on Equator–Rigel: River Bray's GONGGONG is tightest at 0.007%** (his Mars 0.084% and Alan Johns's Gonggong 0.090% also on it).
  - Applying through the race: 0.101% at off−30, 0.041% at the off, 0.031% at the finish, 0.017% at off+30; exact 14:41:28.
  - Both points are beyond the Rigel end (base 8.20): sky Venus 14.771/6.566 (Rigel side 4/5 of the base); his Gonggong 13.328/5.126 (5/8 of the base; his chord is 5:8:13).
  - Families: 9/5 dissonant, 5/4 and 9/4 imperfect.
- Dec 3:4:7 on Castor–Procyon (0.078%, 2 h old): River Bray's Mars is tightest at 0.025% (9.999/16.669).
- Dec 1:5:6 on Castor–Pleiades: Alan Johns's Haumea is 2nd at 0.008% (Tom O'Brien's Pluto 0.002%). His Haumea is the partner of the horse's Makemake in the imprint.
- Venus's Dec sits near the favourite's jockey Rex Dingle's natal Quaoar (0.046°) and Harry Cobden's Quaoar (0.061°). Same-generation Quaoar.
- Already seen in §64 (L2): Venus φ on Pluto–Procyon (horse Neptune 0.007%, joint tightest), Venus 3:4:7 on Chiron–Bellatrix in the race (horse Quaoar 0.018%).
- Number check: RA to Aldebaran = **113 whole**, crossing it during the race (113.0009 at the off → 112.9975 at the finish); 2 ninths (RA to Deneb Algedi 97/9, RA to Pleiades 908/9). That is 1 vs 0.44 and 2 vs 1.5.
### Mars (RA 313.951, Dec −18.466)
- **★ Dec 3:8:11 on Arcturus–Rigel: River Bray's TRANSPLUTO in UNISON, 0.011%, the tightest** (next Reserve Tank 0.053%).
  - The sky chord was exact 14:02:30, 18 min before the off; separating: 0.015% at off−30, 0.025% at the off, 0.032% at the finish, 0.064% at off+30.
  - Same chord, different places (base 27.37):
    - His Transpluto is INSIDE the string, near Arcturus (7.467/19.911).
    - Sky Mars is OUTSIDE, beyond Rigel (37.633/10.262).
    - Families: 11/8 and 11/3 high, 8/3 imperfect.
- **★ Equator–Rigel Dec 4:5:9 AGAIN, the same string and the same chord as Venus**, holding River Bray's Gonggong (0.007%).
  - Applying: 0.099% at off−30, 0.059% at the off, 0.052% at the finish; exact 15:05:30.
  - Venus and Mars are reciprocal on it, both beyond Rigel: Venus 6.566 out (4/5 of the base), Mars 10.262 out (5/4 of the base).
  - His Gonggong is 5.126 out (5/8). So three points sit beyond Rigel on one Dec string: Gonggong, Venus, Mars.
- Dec 1:2:3 on Alkaid–Alphecca (0.050%): River Bray's Chiron is 2nd at 0.031%.
- Favourite's jockey Rex Dingle: Quaoar 0.001% on Arcturus–Regulus φ (exact 13:48), Mercury √2 0.002% on Bellatrix–Capella.
- Slow parallel: Mars on Electric Annie's Saturn Dec (0.041°).
- Number check: 4 ninths (Dec to Alkaid 610/9, Dec to Altair 246/9, RA to Capella 1127/9, RA to Sirius 1326/9) vs 1.5; no φ/√2/whole.
### Jupiter (RA 349.841, Dec −5.453; Dec chords only)
- **★ Dec 2:5:7 on Castor–Procyon, applying through the race** (0.032% at off−30, 0.014% at the off, 0.011% at the finish, 0.003% at off+30; exact 14:43:54). **River Bray's MARS is tightest, 0.025%** (his chord there is 3:5:8).
  - Venus also makes a chord on Castor–Procyon (3:4:7, 0.078%) with his Mars tightest. So two sky bodies hold his Mars on one string.
  - Positions (base 26.67): sky Jupiter is beyond the Procyon end (37.341/10.670); his Mars is inside the string (9.999 from Castor / 16.669 from Procyon).
  - Families: 7/5 and 7/2 septimal, 5/2 imperfect.
- River Bray's KETU is 2nd on two Jupiter chords: Alphecca–Vega 3:8:11 (0.011%) and Algorab–Vega 1:4:5 (0.026%).
- **Deneb Algedi–Procyon** again (Newcastle: Rahu with Venturous's Pluto). Here Jupiter sits at its Dec midpoint (1:1:2, 0.068%, exact 13:22). Electric Annie's Sun is 0.000%; River Bray's Haumea is 2nd at 0.014%.
- Alan Johns: nothing tight on Jupiter's chords.
- Slow parallel: Jupiter RA on Harry Cobden's natal Jupiter (0.033°).
- Number check: 1 ninth (RA to Sirius 1003/9) vs 1.5; no φ/√2/whole.
### Saturn (RA 323.425, Dec −15.457)
- Quiet for the winning pair. Nothing exact on race day near the race.
  - The tightest at the off is RA 1:6:7 on Algorab–Alkaid (0.007%, exact 12:27): Brendan Powell's Juno 0.016%, River Bray's Chiron 2nd at 0.033%.
  - River Bray's Transpluto is 3rd on Algol–Betelgeuse (0.048%).
  - Alan Johns: nothing.
- Saturn's Dec (−15.457) sits in the band of the same-age horses' natal Quaoar: Electric Annie 0.008°, Guernesey 0.017°, River Bray 0.052°, Reserve Tank 0.071°. Also Rex Dingle's Chiron (0.015°) and Harry Cobden's Venus.
  - This is the band the Moon crosses after the finish (River Bray's Quaoar first, 14:26:26). Saturn is closer to the others' Quaoar than to his.
- Number check: 3 ninths (RA to Aldebaran 950/9, RA to Deneb Algedi 30/9, RA to Pleiades 841/9) vs 1.5; no φ/√2/whole.
### Ceres (RA 67.594, Dec +23.555)
- **★ Slow parallel: Ceres sits on River Bray's natal VESTA Dec (23.555 vs 23.543, 0.012°).** So his Vesta makes the same chord on Ceres's Dec strings.
  - Tightest: **Capella–Rigel Dec √2 division, his Vesta UNISON 0.029%** (sky 0.064%, exact 11:47). His Pallas is 2nd on it (0.044%).
- River Bray's Pallas is also 2nd on Antares–Castor 1:6:7 (0.057%; that chord is applying, exact 14:54).
- Alan Johns's Sun is 3rd on Betelgeuse–Polaris RA √2 (0.031%; Guernesey's Ceres 0.002% and Uranus 0.008% ahead).
- In the first read (§64, L2): Ceres 5:8:13 on Neptune–Castor at 14:13:53 — Alan Johns's Quaoar tightest (0.008%).
- Others: CourseLat–Procyon 2:3:5 exact 14:43:54 (no chart close); Guernesey (2nd) holds several Ceres chords (Ceres 0.002%, Eris 0.003%, Transpluto 0.010%).
- Number check: 4 ninths vs 1.5 — Dec from the Equator 212/9; RA to Algol 185/9; Dec to Capella 202/9; **Dec to Castor 75/9 = 8.3333 exactly at the off** (on the Antares–Castor 1:6:7). No φ/√2/whole.
### Pallas (RA 16.707, Dec −6.002)
- **★ RA φ on Aldebaran–Fomalhaut: Alan Johns's NEPTUNE 0.000%, the only chart** (his 3:4:7).
  - Applying through the race: 0.066% at off−30, 0.025% at the off, 0.019% at the finish, 0.014% at off+30; exact 14:40:18. In range 12:47–16:31.
  - Sky Pallas is inside the string (52.272/32.298, base 84.57, the golden cut). His Neptune is beyond the Fomalhaut end (147.997/63.427, 3/4 of the base out).
  - Families: φ, φ, φ² (PHI).
- **Dec 2:5:7 on Algol–Betelgeuse: River Bray's GONGGONG is tightest, 0.009%** (his φ). The sky chord is loose (0.094%, 3.4 h old).
  - Both points are beyond the Betelgeuse end: sky 46.959/13.408 (2/5 of the base), his Gonggong 54.281/20.735 (1/φ of the base).
  - The horse's Gonggong is now held by Venus, Mars (Equator–Rigel) and Pallas.
- River Bray's Haumea is 3rd on Algorab–Altair √2 (0.039%; sky exact 14:07).
- The chord exact 1.8 min before the off, Aldebaran–Sirius φ (0.001%), goes to Electric Annie's / Nick Scholfield's Orcus (0.029%).
- Number check: Dec to Capella = **52 whole** (51.9997); 1 ninth (Dec to Castor 341/9). That is 1 vs 0.44 and 1 vs 1.5.
### Juno (RA 318.586, Dec −8.085)
- Quiet for the winning pair on the star bases: no tightest place.
  - River Bray's Mercury is 2nd on Equator–Fomalhaut Dec 3:8:11 (0.032%; Guernesey's Haumea 0.012%), with Alan Johns's Mars 3rd (0.036%).
  - River Bray's Pallas is 4th on Fomalhaut–Procyon φ.
- Chords near the off go to others:
  - Flat Altair–Fomalhaut 4:5:9, exact 14:16:54 (3.6 min before): Rex Dingle's Pallas 0.031%.
  - Capella–Polaris 4:5:9 (0.008%): Guernesey's Transpluto UNISON.
  - Deneb Algedi–Pleiades 1:4:5, exact 14:43:54: Reserve Tank's Pallas 0.002%.
- In the first read (§64, L3) Juno's string carried the Moon: the Moon 3:8:11 on Juno–Antares in the race, with Alan Johns's Haumea in UNISON.
- No parallel for the pair. Number check: 1 ninth (RA to Altair 188/9) vs 1.5.
### Vesta (RA 307.140, Dec −18.930)
- On the star bases Vesta leans to the favourite's jockey. **Slow parallel: Vesta on Rex Dingle's natal Uranus Dec (0.046°)**, so his Uranus is in UNISON on Capella–Vega 1:8:9 (0.039%) and Polaris–Regulus 2:5:7.
- Winning pair, 2nd places only:
  - **Procyon–Rigel Dec 4:5:9 (the Newcastle string): River Bray's Gonggong 2nd, 0.025%** (Birds Of Prey's Eris 0.009%). The sky chord is loose (0.113%, 3.6 h old).
  - River Bray's Haumea is 2nd on Algol–Castor RA 2:3:5 (0.056%).
  - Alan Johns's Venus is 2nd on Polaris–Regulus.
- In the first read (§64, L4): Vesta 1:2:3 on Mercury–Equator in the race, with **Alan Johns's Juno tightest (0.003%)**.
- Number check: 2 ninths (RA to Altair 85/9, Dec to Betelgeuse 237/9) vs 1.5.
### Uranus (RA 39.752, Dec +15.104)
- Quiet for the winning pair. The one chord exact near the race, Dec 1:2:3 on Bellatrix–Spica (exact 13:03, 0.009% at the off), goes to Ballyblack's Chiron (0.006%); River Bray's Pallas is 2nd, loose (0.093%).
- Alan Johns's Orcus (imprint receiver) is only 4th on Aldebaran–Deneb Algedi RA 2:5:7 (0.067%). **Rex Dingle's Mercury is tightest there (0.009%)** — favourite's jockey again.
- Slow parallel: Uranus on Brendan Powell's Ketu Dec (0.025°).
- Number check: Dec to Pleiades = **9 whole** (9.0002); 1 ninth (Dec to Procyon 89/9). That is 1 vs 0.44 and 1 vs 1.5.
### Neptune (RA 353.900, Dec −3.858) — River Bray tightest on three strings (all slow; sky chords 0.05–0.11%)
- **Dec 3:5:8 on Aldebaran–Altair (sky 0.053%, exact 03:14): River Bray's own NEPTUNE is tightest, 0.023%** (his 2:5:7). The same body on both sides.
  - Both are beyond the Altair end (base 7.64): sky Neptune 20.366/12.726 (5/3 of the base out); his natal Neptune 26.732/19.093 (5/2 of the base out).
- **RA φ on Polaris–Regulus (sky 0.107%, applying, exact in 1.4 d): River Bray's MAKEMAKE is tightest, 0.028%** (his 1:3:4). Makemake is the imprint body (the horse's Makemake is the strongest in the field).
  - Mirror shape: sky Neptune is beyond the **Polaris** end (43.758/158.196); his Makemake is beyond the **Regulus** end (152.565/38.133, 1/3 of the base out). Base 114.44.
  - Alan Johns's Orcus is 4th on it (φ, 0.063%).
- **Dec 2:5:7 on Bellatrix–Castor (sky 0.097%): River Bray's ERIS is tightest, 0.003%** (his 3:8:11). Both are beyond the Bellatrix end: sky 10.206/35.746 (2/5), his Eris 9.577/35.117 (3/8).
- The chord exact 1.1 h before the off, Algorab–Regulus 4:5:9 (0.009%), goes to Tom O'Brien's Rahu (Guernesey's jockey, 2nd).
- No slow parallel. Number check: 1 ninth (RA to Vega 672/9) vs 1.5.
### Pluto (RA 300.418, Dec −22.405)
- **Dec 2:3:5 on Rigel–Sirius (sky 0.066%, 2.4 d old): Alan Johns holds three of the top four** — his Saturn √2 0.040% (tightest), Transpluto φ 0.042%, and **his own PLUTO 0.051%**.
  - Sky Pluto is beyond the **Sirius** end (14.201/5.678; Sirius side 2/3 of the base, base 8.52).
  - His natal Pluto is beyond the **Rigel** end (6.386/14.896; 3/4 of the base out, 3:4:7). The same body at opposite ends (mirror shape).
  - His Saturn is on the Sirius side with sky Pluto (14.525/6.015).
- Dec √2 on Algorab–Rigel (sky loose 0.144%): River Bray's Ceres is tightest (0.028%), his Chiron 2nd.
- River Bray's Pallas is 3rd on Pleiades–Sirius φ (0.021%).
- Rigel keeps coming up for the winners at Wincanton: Equator–Rigel (Venus/Mars → horse Gonggong), Arcturus–Rigel (Mars → horse Transpluto UNISON), Rigel–Sirius (Pluto → jockey), Algorab–Rigel (horse Ceres).
- Slow parallel: Pluto near the favourite's jockey Rex Dingle's natal Sun (0.046°), Tom O'Brien's Neptune and Nick Scholfield's Saturn.
- Number check: 1 ninth (Dec to Algorab 53/9) vs 1.5.
### Chiron (RA 9.681, Dec +6.313)
- On the star bases Chiron is quiet for the winning pair: 2nd places only.
  - River Bray's Neptune is 2nd on Aldebaran–Alphecca 1:1:2 (Chiron at the Dec midpoint, 10.194/20.397; 0.033% behind Ballyblack 0.019%).
  - Alan Johns's own Chiron is 2nd on Capella–Deneb Algedi φ (0.077%).
- **Slow parallel: Chiron sits on the favourite Ballyblack's natal Uranus Dec (0.019°)** — the favourite horse this time.
- Off the stars (from §64/§70):
  - Chiron 1:1:2 on Mercury–Equator at 14:16:35, 4 min before the off: Alan Johns's Juno tightest (with Rex Dingle's Uranus).
  - The Venus 3:4:7 on Chiron–Bellatrix in the race holds the horse's Quaoar.
- Number check: 4 ninths (Dec to Altair 23/9, RA to Betelgeuse 712/9, Dec to Deneb Algedi 202/9, RA to Vega 814/9) vs 1.5; no φ/√2/whole.
### Eris (RA 26.118, Dec −1.197) — slow; tightest places for both winners, sky chords mostly loose
- **RA 2:3:5 on Castor–Rigel (sky 0.019%, 1.2 d old): Alan Johns's MAKEMAKE is tightest, 0.032%** (his 5:8:13).
  - Mirror shape (base 35.02): sky Eris is beyond the **Rigel** end (87.533/52.516, 3/2 of the base out); his Makemake is beyond the **Castor** end (56.039/91.052, 8/5 of the base out).
  - Rigel again; Makemake again (the Sun's chord in the race held the same Makemake).
- RA 4:5:9 on Deneb Algedi–Vega (sky 0.071%): **River Bray's KETU 0.003%**, tightest. Both are beyond the Deneb Algedi end (sky 59.361/106.883; his 76.888/124.409).
- Dec 1:2:3 on Alkaid–Antares (sky 0.071%): River Bray's Sedna is tightest (0.024%).
- Dec 1:8:9 on Altair–Polaris (sky loose 0.144%): Alan Johns's Haumea is tightest (0.003%; inside the string, 13.399/66.995).
- RA 1:1:2 on Castor–Spica (sky loose 0.137%): Alan Johns's Venus is tightest (0.022%).
- The only chord exact on the day, Altair–Capella 3:5:8 at 15:55, goes to Ballyblack's Eris (0.003%).
- Slow parallels: Eris on Reserve Tank's Chiron Dec (0.021°) and Rex Dingle's Pallas Dec (0.051°).
- Number check: no hits.
### Sedna (RA 58.432, Dec +8.182)
- **Dec 1:2:3 on Algol–Rigel (sky 0.008% at the off, exact 19:57): Alan Johns's GONGGONG is tightest, 0.008%** (his 1:4:5; Rex Dingle's Makemake 2nd, 0.017%).
  - Base 49.16. Sky Sedna is inside the string, a third of the way from Rigel (32.775/16.386). His Gonggong is beyond the Rigel end, a quarter of the base out (61.444/12.288).
  - Families: 3/2, 3, 2 (all perfect). Rigel again; Gonggong again (the horse's Gonggong is held by Venus, Mars and Pallas).
- **Dec 1:8:9 on Castor–Procyon (sky 0.050%, exact 05:33): River Bray's MARS is tightest, 0.025%.** Castor–Procyon now carries three sky bodies on his Mars: Venus 3:4:7, Jupiter 2:5:7 (applying, exact 14:43) and Sedna 1:8:9.
- River Bray's Makemake is tightest on Arcturus–Bellatrix 1:6:7 (0.054%; sky loose 0.148%).
- Alan Johns's Ceres is 2nd on Aldebaran–Castor φ (0.035%); the sky chord is 0.011%, exact 18:19.
- No slow parallel. Number check: 1 ninth (Dec to Betelgeuse 7/9) vs 1.5.
- **Eddie 21:58: "this type of occurrence is very significant — the combinations"** (several sky bodies making chords on ONE string that holds the SAME natal body). Stacks seen so far:
  - Wincanton: **Castor–Procyon → River Bray's Mars**: Venus 3:4:7, Jupiter 2:5:7 (applying, exact 14:43), Sedna 1:8:9.
  - Wincanton: **Equator–Rigel → River Bray's Gonggong**: Venus and Mars, both 4:5:9 (applying, exact 14:41 and 15:05).
  - Wincanton: **Alkaid–Antares → River Bray's Sedna**: Eris 1:2:3 and Haumea 4:5:9 (his Sedna UNISON with Haumea).
  - Newcastle: **Betelgeuse–Deneb Algedi → Connor Beasley's Haumea**: Jupiter 1:5:6 (exact 13:34:37) and Makemake 5:8:13.
  - Newcastle: **Procyon–Rigel → Connor Beasley's Orcus**: Neptune 1:3:4 (mirror) and Eris (midpoint).
  - Not yet checked: whether losers get stacks as often (a whole-field count is needed before reading anything into it).
### Haumea (RA 217.277, Dec +15.643)
- **Dec 4:5:9 on Alkaid–Antares (sky 0.021%): River Bray's SEDNA in UNISON, 0.024%, the tightest** — the second sky body on this string with his Sedna (Eris 1:2:3 was the first).
- **Slow parallel: Haumea on Alan Johns's natal CHIRON Dec (0.046°)** → his Chiron is in UNISON, tightest on Algorab–Spica 1:5:6 (0.039%; sky loose 0.118%).
- River Bray's Eris is tightest on Equator–Procyon 1:2:3 (0.031%; sky 0.071%).
- The chord tightest at the off, Algol–Equator φ (0.012%, exact 17:07), goes to Birds Of Prey's Sun (0.002%) and Rex Dingle's Makemake; Alan Johns's Gonggong is 3rd.
- Number check: 1 ninth (Dec to Alkaid 303/9) vs 1.5.
### Makemake (RA 198.760, Dec +22.850)
- **★ RA 1:2:3 on Antares–Fomalhaut: Alan Johns's MAKEMAKE is tightest, 0.001%.** The same string as the Sun's 1:6:7, exact in the race (14:23:28) — a **stack: Sun + sky Makemake on Antares–Fomalhaut → his natal Makemake**, and here sky Makemake meets natal Makemake (same body).
  - Sky Makemake is beyond the Antares end, half a base out (48.594/145.650, base 97.06). His Makemake is also beyond Antares, 4/5 of a base out (77.656/174.724). The Sun is beyond the other end (Fomalhaut).
  - The sky Makemake chord itself is loose and slow (0.137%, 4.3 d old); the Sun supplies the timing.
- **For balance — the favourite's jockey has the same kind of stack:** Aldebaran–Bellatrix → **Rex Dingle's Makemake**: the Sun 3:5:8 (exact 14:25:22, 4 s before the finish, mirror about Aldebaran) + sky Makemake 5:8:13 (his Makemake UNISON 0.002%; sky 0.110%).
- River Bray's Mars is 3rd on Alphecca–Betelgeuse 1:4:5 (0.054%).
- The tightest Makemake chord at the off, CourseLat–Procyon 5:8:13 (0.005%, exact 16:04), has no chart close.
- Slow parallels: Makemake RA on Birds Of Prey's Mars (0.020°); Dec on Nick Scholfield's Jupiter (0.010°).
- Number check: 2 ninths (Dec to Betelgeuse 139/9, RA to Castor 766/9) vs 1.5.
### Quaoar (RA 277.216, Dec −15.305)
- Sky Quaoar is slow and its chords are loose (0.06–0.15%). For the winners:
  - **Rigel–Sirius again** (Dec 1:5:6, exact 03:54, 0.128% at the off): Alan Johns holds the top places again — Saturn √2 0.040%, Transpluto 0.042%, Pluto 0.051%. A loose **stack: Pluto 2:3:5 + Quaoar 1:5:6 on Rigel–Sirius → his Saturn / Transpluto / Pluto.**
  - River Bray's Orcus is 2nd on Alkaid–Sirius RA 2:3:5 (0.030%).
  - Alan Johns's Sun and Rahu are 3rd and 4th on Bellatrix–Vega.
- Sky Quaoar is 0.099° from River Bray's natal Quaoar Dec (loose; the same-age horses share it). His Quaoar is played by the Moon (UNISON in the race, crossing 1 min after the finish) and Mercury (Alkaid–Altair), not by sky Quaoar.
- Number check: no hits.
### Orcus (RA 156.177, Dec −11.899)
- **Algorab–Rigel Dec 4:5:9 (sky 0.050%, exact 11:24): River Bray's CERES is tightest (0.028%), his Chiron 2nd in UNISON (0.063%).** With Pluto's √2 on the same string (his Ceres also tightest), this is a **stack: Pluto + Orcus on Algorab–Rigel → the horse's Ceres** (both sky chords slow). Rigel again.
- River Bray also:
  - Mars UNISON 3rd on Alphecca–Sirius 1:8:9 (0.027%). Note: Mars–Alphecca–Sirius shows his Mars on yet another string.
  - Quaoar 2nd on Betelgeuse–Regulus φ (0.024%).
  - Venus 3rd on Betelgeuse–Capella RA (0.028%).
- Alan Johns: his Venus is 2nd on Alphecca–Regulus φ (0.012%). His Orcus (the imprint receiver) is only loose, on Alphecca–Rigel (0.134%).
- The tightest chord at the off, Alphecca–Betelgeuse 1:1:2 (0.003%, exact 12:39), has no chart close (River Bray's Mars 3rd at 0.054%).
- No slow parallel. Number check: no hits.
### Gonggong (RA 337.056, Dec −11.149)
- **Castor–Polaris Dec: Alan Johns's VESTA is tightest, 0.013%** (his 1:1:2, one base length beyond Castor: 57.370/114.747).
  - Sky Gonggong makes 3:4:7 (0.007% at the off, exact 07:21 next day; 43.037/100.417, 3/4 of the base beyond Castor).
  - Mercury makes 2:5:7 on it (0.141%; 38.199/95.578, 2/3 of the base beyond Castor).
  - **Stack: Mercury + Gonggong on Castor–Polaris → the jockey's Vesta.** All three points are beyond the Castor end.
- **Aldebaran–Altair Dec: River Bray's NEPTUNE is tightest, 0.023%.** Gonggong φ (0.083%) joins Neptune 3:5:8 on the same string → **stack: Neptune + Gonggong → the horse's Neptune** (sky Neptune meets natal Neptune).
- Equator–Sirius Dec 1:2:3 (exact 02:45): Alan Johns's Mercury φ 0.032% and Haumea 0.046% are 1st and 2nd.
- The Gonggong chord exact in the race, RA 2:5:7 on Betelgeuse–Pleiades (exact 14:24:06, 0.000% at the off), goes to Guernesey's Juno (0.043%) and Rex Dingle's Chiron/Juno — not the winners.
- Number check: RA to Aldebaran = **65√2** (91.9226 vs 91.9239); 1 ninth (Dec to Betelgeuse 167/9). That is 1 vs 0.44 and 1 vs 1.5.
### Transpluto (RA 154.496, Dec +10.572)
- **★ Algol–Rigel Dec φ (0.011% at the off, exact 00:48 next day): Alan Johns's GONGGONG tightest again, 0.008%** (Rex Dingle's Makemake 2nd, 0.017%).
  - With Sedna 1:2:3 on the same string (0.008%), this is a **stack: Sedna + Transpluto on Algol–Rigel → the jockey's Gonggong**, and both sky chords are tight.
  - Sky Transpluto is inside the string (30.384/18.777, the golden cut from the Rigel side); Sedna is inside (32.775/16.386); his Gonggong is beyond the Rigel end (61.444/12.288). Rigel again.
- River Bray: only loose (Orcus on Antares–Betelgeuse √2, 0.113%).
- Others near the off: Antares–Equator 2:5:7 (0.008%) → Brendan Powell's Mars; Capella–Pleiades φ → Nick Scholfield's Juno.
- Number check: 2 ninths (Dec to Bellatrix 38/9, Dec to Rigel 169/9) vs 1.5.
### The nodes (Rahu RA 50.968 Dec +18.610; Ketu opposite)
- **★ Rahu Dec 5:6:11 on Algol–Rigel (0.005% at the off, exact 11:43): Alan Johns's GONGGONG tightest, 0.008%** — the THIRD sky body on Algol–Rigel with his Gonggong. **Stack: Sedna 1:2:3 (0.008%) + Transpluto φ (0.011%) + Rahu 5:6:11 (0.005%) → the jockey's Gonggong.** All three sky chords are tight. Rahu is inside the string (22.347/26.815).
- **Rahu RA 5:8:13 on Arcturus–Castor (sky 0.031%): Alan Johns's ORCUS tightest, 0.011%** — the imprint receiver, at last. His Orcus is inside the string, a sixth from Castor (83.552/16.709); Rahu is beyond the Castor end (162.945/62.683).
- **Ketu Dec 2:3:5 on Betelgeuse–Rigel (0.014%, exact 07:53): River Bray's SATURN tightest, 0.002%.** Both are beyond the Rigel end: Ketu 26.015/10.405 (2/3 of the base), his Saturn 18.210/2.601 (1/6 of the base). Rigel again.
- Rahu Dec 2:5:7 on Polaris–Vega (sky loose 0.120%): River Bray's Sedna tightest, 0.007%.
- Ketu RA 2:3:5 on Altair–Polaris: Alan Johns's Rahu 2nd (0.027%).
- Slow parallel: Rahu Dec on River Bray's natal Haumea (0.048°) and on Electric Annie's Sun.
- Number check: Rahu 2 ninths (Dec to Arcturus 5/9, RA to Rigel 249/9); Ketu 2 ninths (Dec to Arcturus 340/9, RA to Rigel 1371/9). Chance level.
### Power points (§42 star-lattice nodes) — Wincanton
- **No sky body sits on a power point** at the off (Dec 99% = 12, RA 99% = 10). The nearest: Rahu Dec 18.610 and Juno Dec −8.085, 11 pairs each; Jupiter and Orcus Dec 10. Rahu's 11 include Algol–Rigel (the jockey's Gonggong stack).
- The Moon peaks at 8 (RA 220.603, 83 s before the off).
- **Neither River Bray nor Alan Johns has a natal point on a power point.** Others do: Reserve Tank's Mars Dec (15**), Ballyblack's Rahu RA (13**), Harry Cobden's Mars RA.
- So unlike Newcastle (Transpluto on a power point carrying both winners' mirrors), there is no power-point connection at Wincanton.

## 71. SECOND LOOK — Carlisle 13:55, 14 Oct 2021 (Arvico Bleu 25/1, Callum Bewley), read with the three methods (Eddie 7 Oct 07:02)
Method 1 (imprint, from the first read): Makemake leads both charts; the #1 pair Arcturus–Jupiter is held inside the jockey's chart alone (1+√2); Mercury strikes the horse's Pluto; **the horse's Haumea is a hub** (struck by Neptune); 40/9 and 100/9 in both.
Method 2 (first read): the Moon's RA 1:2:3 on Altair–Fomalhaut entirely inside the race, horse Saturn UNISON (wins the same note); the off chord goes to the favourite's jockey.
### Sun (RA 199.495, Dec −8.234)
- **★ RA 2:3:5 on Antares–Vega: Arvico Bleu's HAUMEA (the imprint hub) is tightest, 0.004%** (his 4:5:9). Next: Conor O'Farrell's Pluto 0.056%, Callum Bewley's Pallas 0.057% (3rd).
  - Applying through the race: 0.085% at off−30, 0.045% at the off, 0.040% at the finish, 0.008% at off+30; exact 14:32:21.
  - Both are beyond the Antares end (base 31.88): the Sun 47.852/79.739 (3/2 of the base out), his Haumea 39.851/71.733 (5/4 of the base out).
  - Families: 3/2 perfect, 5/2 and 5/3 imperfect.
- **★ Slow parallel: the Sun sits on Callum Bewley's natal ERIS Dec (−8.234 vs −8.204, 0.031°).** So his Eris is in UNISON on the Sun's Dec chords.
  - **Alphecca–Procyon Dec 5:8:13: his Eris UNISON 0.001%, the tightest.** Sun 34.951/13.455 vs his Eris 34.923/13.432 — almost the same point.
  - The sky chord is separating (0.084% at off−30, 0.141% at the off, 0.148% at the finish). It is in range 11:20–**14:01:10, going out 4 s after the finish (14:01:06).**
- Others: Alphecca–Vega 3:4:7 exact 13:52:18 (5 min before the off), no chart tuned. Altair–Fomalhaut 4:5:9 applying, exact 14:04:44 (Finisk River's Vesta 0.005%). Algol–Procyon (Conor O'Farrell's Venus 0.002%).
- Number check: Dec to Sirius = **6√2** (8.4859 vs 8.4853; 8.4848 at the finish, crossing it in the race); no ninths.
### Mercury (RA 190.346, Dec −4.734) — the busiest body in the imprint
- **RA √2 division on Polaris–Sirius (sky 0.098%, slowly applying, exact 17:50): Arvico Bleu's HAUMEA is tightest, 0.008%** (his 3:5:8). Callum Bewley's Neptune is 2nd (0.030%).
  - Both are beyond the Sirius end: Mercury 151.974/89.061 (√2 of the base out, base 62.91); his Haumea 169.953/106.224 (5/3 of the base out).
  - So the horse's Haumea hub is held by the Sun (Antares–Vega, 0.004%) and by Mercury (Polaris–Sirius, 0.008%) on two different strings. The sky chord here is a √2 (the discord family); his own chord is 3:5:8.
- **Dec 5:6:11 on Algorab–Spica, exact 13:57:59, 49 s after the off** (0.197% at off−30 → 0.005% at the off → 0.020% at the finish; in range 13:35–14:21).
  - Arvico Bleu's own **Eris √2 is 3rd** (0.046%; Craig Nichol's Juno 0.022% tightest).
  - Both are beyond the Spica end: Mercury 11.779/6.425, his Eris 12.924/7.569.
- Dec 3:8:11 on Betelgeuse–Regulus (sky 0.136%, separating): Callum Bewley's CERES in UNISON, tightest (0.028%) — the jockey's Ceres (his own √2 elsewhere).
- Fomalhaut–Procyon 2:5:7 exact 13:56:00, 70 s before the off: the favourite Gold Des Bois's Makemake (0.016%), the only chart.
- Slow parallel: Mercury's Dec near Arvico Bleu's natal Juno (0.055°).
- Number check: RA to Antares = **57 whole** (57.0019 → 57.0035); **RA to Vega = 800/9 exactly at the off (88.8889)**; ninths also Dec to Algorab 106/9, RA to Arcturus 212/9, Dec to Fomalhaut 224/9. That is 1 whole vs 0.44 and 4 ninths vs 1.5 — above chance for ninths. (100/9 and 40/9 are in both winning charts' imprints; 800/9 = 8 × 100/9.)
### Venus (RA 245.019, Dec −24.516)
- **★ STACK on Betelgeuse–Regulus (Dec) → Callum Bewley's CERES (3:8:11, 0.028%, tightest on both):**
  - Mercury 3:8:11, a **true mirror and UNISON**: Mercury is 12.143 beyond the **Betelgeuse** end; his Ceres is 12.165 beyond the **Regulus** end (base 4.56). The same chord, the same distance, from opposite ends. Exact 13:15 (0.034% at off−30, 0.136% at the off, separating).
  - Venus 1:7:8: Venus is 31.924 beyond Betelgeuse (7 bases). Exact 13:23 (0.001% at off−30, 0.017% at the off, 0.019% at the finish).
  - Both were exact 35–40 min before the off and are still in range through the race.
- **Dec 2:3:5 on Altair–Spica, exact 13:51:19 (6 min before the off): Callum Bewley's JUNO 0.001%, the tightest** (the first read had this). 0.030% at off−30, 0.007% at the off, 0.012% at the finish.
  - His Juno is inside the string (10.926/9.105); Venus is beyond the Spica end (33.389/13.356). Altair again.
- Arvico Bleu: Juno in UNISON on Betelgeuse–Procyon RA 1:5:6 (4th, 0.043%); Mars 3rd on Fomalhaut–Spica φ (0.050%). Slow parallel: Venus RA near his natal Juno (0.093°, loose).
- Venus RA sits on Sam Coltherd's natal Quaoar (0.007°).
- Number check: Dec to Algorab = **8 whole**; Dec to Arcturus = **27φ** (43.6882 vs 43.6869); 2 ninths (RA to Betelgeuse 1406/9, Dec to Polaris 1024/9). That is 2 vs 0.44 and 2 vs 1.5.
### Mars (RA 197.765, Dec −6.884)
- **★ Slow parallel: Mars sits on Arvico Bleu's natal ORCUS Dec (−6.884 vs −6.864, 0.020°).** So his Orcus is in UNISON on Mars's Dec chords: Capella–Pleiades √2 (0.018%, 3rd) and Algol–Bellatrix φ (0.048%, 2nd).
- **Dec φ on Arcturus–Regulus — only the two winning charts are on it.** Arvico Bleu's VESTA is tightest (4:5:9, 0.053%); Callum Bewley's Saturn is the other (0.127%).
  - Applying through the race: 0.072% at off−30, 0.043% at the off, 0.039% at the finish, 0.017% at off+30; exact 14:43:58.
  - Mars and his Vesta are both beyond the Regulus end (Mars 26.057/18.853; his Vesta 12.971/5.763; base 7.20).
  - Arcturus–Regulus is the string where Mars made 5:8:13 with Venturous's Sedna mirrored at Newcastle (RA there; Dec here).
- Dec 3:4:7 on Antares–Arcturus (applying, exact 14:15:10; 0.027% at the off, 0.020% at the finish): Callum Bewley's PLUTO is 2nd (0.034%; both inside the string), behind the favourite Gold Des Bois's Chiron (0.027%).
- RA 4:5:9 on Fomalhaut–Vega (exact 13:28) → Finisk River's Eris; Altair–Sirius → Craig Nichol.
- **Number check — three exact at the off:** RA to Deneb Algedi = **129** (128.9999), RA to Alkaid = **82/9** (9.1111), RA to Pleiades = **1268/9** (140.8888). That is 1 whole vs 0.44 and 2 ninths vs 1.5.
### Jupiter (RA 324.804, Dec −15.250)
- **Number check meets Method 1: Jupiter's RA distance to Arcturus = 10φ⁵** (110.9015 vs 110.9017). This is the race's **#1 sky pair** (Arcturus/Jupiter, 100.0, from the imprint read). Its partner inside the winning pair: **Callum Bewley's natal Arcturus–Jupiter RA = 2.4144 = 1+√2**, held alone in the field. Sky Jupiter–Arcturus and natal Jupiter–Arcturus are both special numbers (φ family in the sky, silver ratio in his chart).
- On the star strings Jupiter is slow (only Alphecca–Vega 1:1:2 at 0.006%, exact 20:02; no chart close). Winning-pair tightest places, on loose sky chords (0.106–0.121%):
  - Callum Bewley's JUNO 0.001% on Procyon–Spica Dec 1:4:5 — his Juno again (Venus held it on Altair–Spica at 0.001%, exact 6 min before the off). Spica is the shared star.
  - Arvico Bleu's MARS 0.010% on Algol–Spica RA; his SUN 0.008% on Pleiades–Rigel RA φ.
  - Callum Bewley's Gonggong 2nd on Capella–Polaris √2.
- No slow parallel.
### Saturn (RA 309.194, Dec −19.417)
- Slow; nothing exact on race day. The sky's Saturn does not play the horse's natal Saturn (that is the Moon's job, Altair–Fomalhaut in the race).
- **Antares–Rigel Dec 5:8:13 (sky 0.054%, 2 d old): the winners take 1st, 2nd and 4th** — Arvico Bleu's QUAOAR 0.019% (2:3:5), Callum Bewley's GONGGONG 0.022% (√2 division), Callum Bewley's Transpluto 0.056%.
  - All inside the string (base 18.23): Saturn 7.015 from Antares; the jockey's Gonggong 7.552 from Antares; the horse's Quaoar 7.291 from Rigel (the other side).
- Arvico Bleu's PALLAS is tightest on Betelgeuse–Equator φ (0.013%; sky loose 0.108%); his Ketu 2nd on Equator–Vega 1:2:3.
- Callum Bewley's TRANSPLUTO is tightest on Algorab–Capella RA (0.003%; sky loose 0.102%); his Sedna 3rd on Algol–Polaris.
- Number check: **Saturn's Dec from the Equator = 12φ** (19.4169 vs 19.4164); **RA to Rigel = 80φ** (129.4434 vs 129.4427; also near 1165/9). That is 2 φ hits vs 0.44.
### Ceres (RA 71.072, Dec +16.167)
- On the star strings Ceres leans to the **favourite's side**: Gold Des Bois's Orcus 0.011% (Castor–Pleiades RA 1:3:4, applying, exact 16:03); Conor O'Farrell's Sun 0.009% (Bellatrix–Castor) and his Ceres tightest on Polaris–Rigel 1:3:4 (the tightest Ceres chord at the off, 0.003%, exact 12:48).
- Winning pair: Callum Bewley's Gonggong is tightest only on loose Arcturus–Castor φ (0.078%; sky 0.142%); his Quaoar 3rd on Algorab–Alkaid.
- Off the stars (first read, L4): **Ceres on Sun–Polaris — Arvico Bleu wins the same note.**
- Number check: 2 ninths (Dec to Sirius 296/9, RA to Spica 1172/9) vs 1.5.
### Pallas (RA 342.126, Dec −7.429)
- On the star strings the winners take 2nd/3rd places only:
  - Arvico Bleu's CERES is 2nd on Deneb Algedi–Spica Dec 3:4:7 (0.037%; applying, exact 14:27).
  - Arvico Bleu's SEDNA is 2nd on Arcturus–Fomalhaut 5:6:11 (0.030%).
  - Callum Bewley's Jupiter is 3rd on Equator–Sirius 4:5:9 (0.031%; applying, exact 14:13).
- **Callum Bewley's SATURN in UNISON on two Pallas RA chords** — Procyon–Rigel 3:8:11 (0.091%, 2nd) and Algol–Regulus φ (0.142%). Pallas's RA sits near his natal Saturn RA (0.088°, a loose RA parallel).
- Already in the first read: **Pallas on Chiron–Pleiades 6 s after the finish, the horse's Sedna tightest** (L2); and Saturn φ on Pallas–Regulus 3 min before the off with the jockey's own Ceres √2 (L3).
- Number check: RA to Castor = **93√2 exactly** (131.5219); 3 ninths (RA to Algorab 1392/9, RA to Antares 853/9, RA to Arcturus 1154/9). That is 1 vs 0.44 and 3 vs 1.5.
### Juno (RA 259.799, Dec −11.985) — two more stacks
- **★ STACK on Alphecca–Procyon (Dec) → Callum Bewley's ERIS (0.001%, tightest):** the Sun 5:8:13 (his Eris in UNISON through the Sun's parallel; the chord goes out 4 s after the finish) + Juno 4:5:9 (0.043% at the off, slowly separating).
- **★ STACK on Betelgeuse–Equator (Dec) → Arvico Bleu's PALLAS (0.013%, tightest):**
  - His natal Pallas (Dec 3.703) sits **exactly at the midpoint** of Betelgeuse (7.406) and the Equator: 1:1:2.
  - Juno makes φ, beyond the Equator end (19.393/11.985). Applying through the race: 0.036% at off−30, 0.024% at the off, 0.022% at the finish; exact 15:00; in range 08:57–18:56.
  - Saturn makes φ on the same string (0.108%).
- Dec 1:3:4 on Algol–Fomalhaut (sky 0.047%): Arvico Bleu's SUN is tightest (φ, 0.010%). Both inside the string — his Sun at the golden cut (26.960/43.617), Juno at a quarter from Fomalhaut (52.940/17.639).
- Arvico Bleu's Sun is 2nd on Antares–Pleiades 2:5:7 (0.020%); his own Juno tightest on Alkaid–Fomalhaut RA (loose).
- Others: Betelgeuse–Vega φ (0.009%, applying, exact 14:36) → Conor O'Farrell's Jupiter (0.004%), the favourite's jockey.
- No parallel. Number check: no hits.
### Vesta (RA 220.871, Dec −11.650)
- The two Vesta chords nearest the race go to others: Procyon–Regulus 2:5:7 exact 13:55:22, 1.8 min before the off (0.001%; Craig Nichol's Jupiter 0.030%); Antares–Deneb Algedi RA 1:3:4 exact 14:07:58 (If Not For Dylan).
- From the first read (L3): Vesta 2:3:5 on Saturn–Equator exact AT THE OFF → the favourite's jockey Conor O'Farrell (Chiron 0.004%).
- Winning pair (slow sky chords):
  - **Arvico Bleu's PALLAS tightest on Alkaid–Castor Dec 2:5:7 (0.024%; sky 0.079%)** — his Pallas again (the Betelgeuse–Equator midpoint stack).
  - Arvico Bleu's Chiron tightest on Polaris–Vega 1:1:2 (0.028%); his Mars UNISON tightest on Arcturus–Betelgeuse φ (loose); his Haumea joint 2nd on Alkaid–Equator φ (0.029%).
  - Callum Bewley's Gonggong 3rd on Capella–Vega 1:7:8 (0.010%).
- No parallel. Number check: Dec to Bellatrix = **18 whole** (18.0014); 2 ninths (RA to Aldebaran 1367/9, RA to Castor 965/9). That is 1 vs 0.44 and 2 vs 1.5.
### Uranus (RA 41.020, Dec +15.436)
- No tightest place for the winners. 2nd places: Arvico Bleu's Saturn on Bellatrix–Procyon RA 5:6:11 (0.019%); Callum Bewley's Sedna on Bellatrix–Rigel (0.018%), his Venus on Alphecca–Fomalhaut (0.012%), his Gonggong on Capella–Polaris √2 (0.026%).
- **The favourite's side again:** Conor O'Farrell's Ketu tightest on Bellatrix–Procyon (0.002%); Gold Des Bois's Mars tightest on Capella–Polaris √2 (0.014%) and his Vesta on Bellatrix–Regulus φ. (Uranus leaned to the favourite's side at Newcastle and Wincanton too.)
- The tightest Uranus chords at the off: Pleiades–Regulus Dec 2:5:7 (0.010%, applying, exact 14:31) → Sam Coltherd's Eris; Aldebaran–Algorab RA φ (0.013%) → Brian Hughes's Vesta.
- No parallel. Number check: 2 ninths (Dec to Capella 275/9, Dec to CourseLat 355/9) vs 1.5.
### Neptune (RA 351.919, Dec −4.760)
- **Number check meets Method 1 again: Neptune's Dec distance to Bellatrix = 100/9** (11.1109). This is the race's **#2 sky pair** (Bellatrix/Neptune Dec 11.1109). The 100/9 family is carried by both winners in the imprint (e.g. the jockey's Procyon–Rahu RA 111.1089). So the #1 pair (Jupiter–Arcturus, 10φ⁵) and the #2 pair both come out of the slow-body number check.
- **★ Slow parallel: Neptune's RA sits on Arvico Bleu's natal PALLAS RA (0.008°)** (and its Dec near his natal Juno, 0.030°). His Pallas is in UNISON on Neptune's RA chords: **Capella–Vega 5:6:11, his Pallas tightest, 0.017%** (Neptune 87.258/72.684, his Pallas 87.240/72.688 — almost the same point); Betelgeuse–Vega 3:4:7 (0.056%).
  - The horse's PALLAS is now held by Juno + Saturn (Betelgeuse–Equator, his Pallas at the exact midpoint), Vesta (Alkaid–Castor) and Neptune (RA parallel).
- **★ Betelgeuse–Regulus becomes a THREE-body stack → Callum Bewley's CERES (UNISON 3:8:11, tightest):** Mercury 3:8:11 + Venus 1:7:8 + **Neptune 3:8:11** (12.168 beyond Betelgeuse; Mercury and Neptune are almost at the same Dec, −4.73 / −4.76). His Ceres mirrors both from beyond the Regulus end (12.165). Neptune's chord is slow (0.072%, separating).
- Bellatrix–Procyon RA: Uranus 5:6:11 + Neptune 3:8:11 → Arvico Bleu's Saturn 2nd on both (UNISON with Neptune, 0.019%); Conor O'Farrell's Ketu tighter (0.002%).
- Algorab–Polaris 1:8:9 (0.011%, exact 17:15) → Conor O'Farrell's Ceres (0.022%); the winners 3rd/4th.
### Pluto (RA 296.230, Dec −22.937)
- **★ A mirror in the sky itself on Algorab–Spica (Dec 5:6:11):** Pluto is 6.423 beyond the **Algorab** end (6.423/11.778); Mercury is 6.425 beyond the **Spica** end (11.779/6.425). The same chord at the same distance from opposite ends. Both cross-distances are **106/9** (Pluto–Spica 11.7778 exactly; Mercury–Algorab 11.7794).
  - Mercury's chord is exact 49 s after the off; Pluto's is slow (0.030%, applying).
  - Arvico Bleu's own Eris √2 is 3rd on this string (0.046%; Craig Nichol's Juno 0.022%).
- Winning pair, tightest on loose sky chords: Arvico Bleu's RAHU on Spica–Vega φ (0.005%; sky 0.117%); Callum Bewley's VENUS on Arcturus–Polaris 3:5:8 (0.019%; sky 0.132%).
- The horse's own Pluto (struck by Mercury in the imprint) is not on Pluto's star chords.
- Others: Betelgeuse–Deneb Algedi RA → Conor O'Farrell's Mercury (0.017%).
- Number check: 3 ninths (Dec to Aldebaran 355/9, Dec to Arcturus 379/9, Dec to Spica 106/9 exact) vs 1.5.
### Chiron (RA 8.130, Dec +6.086)
- **★ RA 3:5:8 on Betelgeuse–Polaris: Callum Bewley's MAKEMAKE in UNISON, 0.010%, the tightest** (Craig Nichol's Makemake UNISON 2nd, 0.029%). Makemake leads both winning charts in the imprint.
  - Opposite ends, the same chord: Chiron is beyond the **Polaris** end (80.666/30.242); his Makemake is beyond the **Betelgeuse** end (84.525/135.235).
  - The sky chord is slow and steady (0.046% at off−30, 0.043% at the off and the finish; exact 22:06).
- **Capella–Vega RA becomes a STACK → Arvico Bleu's PALLAS (0.017%, tightest):** Neptune 5:6:11 (his Pallas in UNISON via the RA parallel) + Chiron 4:5:9 (0.096%).
- Arvico Bleu's Mercury is 3rd on Betelgeuse–Polaris (0.059%).
- The tightest Chiron chord at the off, Fomalhaut–Rigel Dec 2:3:5 (0.012%, exact 16:12), goes to Brian Hughes's Haumea (UNISON 0.005%).
- Number check: 1 ninth (RA to Betelgeuse 726/9) vs 1.5.
### Eris (RA 26.400, Dec −1.419)
- Eris leans to the **favourite's jockey Conor O'Farrell**: his Jupiter 0.000% (Betelgeuse–Deneb Algedi 3:5:8, the tightest Eris chord at the off, 0.028%), his Neptune 0.000% (Altair–Arcturus 1:1:2), his Pluto 0.008% (Antares–Castor).
- Winning pair, tightest on looser sky chords:
  - Callum Bewley's KETU on Pleiades–Sirius 3:5:8 (0.013%; sky 0.092%).
  - Callum Bewley's CERES on Altair–Bellatrix RA φ (0.065%; sky 0.119%) — his Ceres again.
  - Arvico Bleu's MARS UNISON on Arcturus–Betelgeuse 3:4:7 (0.091%) — a loose stack with Vesta φ on the same string.
- No parallel. Number check: 2 ninths (RA to Capella 475/9, Dec to Rigel 61/9) vs 1.5.
### Sedna (RA 59.196, Dec +8.151) — the clock and the holder on one string
- **★ Altair–Fomalhaut (RA) → Arvico Bleu's SATURN (his 1:2:3, 0.012%, tightest on Sedna's chord):**
  - **Sedna HOLDS it:** 5:8:13 at 0.032%, constant all day (0.0320% → 0.0317% over the hour; in range 08:57–18:56). Sedna is beyond the **Fomalhaut** end (121.496/74.776).
  - **The Moon STRIKES it:** 1:2:3, entirely inside the race (in 13:58:00, exact 13:59:25, out 14:00:55; Method 2) — his Saturn in UNISON, and he wins the same note against Brian Hughes. The Moon is inside the string, a third from Altair (15.57/31.14).
  - His natal Saturn is beyond the **Altair** end (93.412/140.124, twice the base out) — opposite to Sedna.
  - This is the "slow holds, the Moon strikes" shape on one string, and it is the chord that marked Carlisle in the first read.
- **Capella–Vega RA → Arvico Bleu's PALLAS: a THREE-body stack** — Neptune 5:6:11 (his Pallas UNISON via the RA parallel) + Chiron 4:5:9 + Sedna 1:7:8. His Pallas tightest on all three (0.017%).
- **Aldebaran–Vega Dec 3:8:11: Callum Bewley's JUNO tightest, 0.006%** (sky 0.030%) — his Juno again (Venus exact 6 min before the off; Jupiter; now Sedna).
- Callum Bewley's MERCURY √2 tightest on Arcturus–Bellatrix RA 1:6:7 (0.013%); 2nd on Castor–Polaris φ (0.025%).
- Arvico Bleu's CHIRON tightest on Algol–Pleiades RA φ (0.032%; sky 0.012%, exact 12:39).
- Slow parallel: Sedna on Sam Coltherd's Saturn Dec (0.020°).
- Number check: 3 ninths (Dec to Algorab 222/9, RA to Fomalhaut 673/9, Dec to Polaris 730/9) vs 1.5.
### Haumea (RA 215.844, Dec +15.090)
- On the star strings sky Haumea is quiet for the winners: Callum Bewley's Sedna 2nd on Bellatrix–Rigel 3:5:8 (0.018%; Uranus 5:8:13 on the same string also had his Sedna 2nd); Callum Bewley's Ketu/Mars 3rd–4th on Deneb Algedi–Vega.
- Its main link is off the stars, from the first read (L4): **sky Haumea on Mercury–Regulus at 14:07:06 — the winning pair 1st, 2nd and 3rd** (horse Jupiter, horse Pallas, jockey Orcus).
- The horse's own Haumea (the imprint hub) is held by the Sun (Antares–Vega) and Mercury (Polaris–Sirius), not by sky Haumea.
- Number check: 1 ninth (RA to Capella 1230/9) vs 1.5.
### Makemake (RA 198.076, Dec +22.109)
- Sky Makemake gives **Arvico Bleu four tightest places** (all on slow sky chords, 0.047–0.094%):
  - **his MARS 0.002%, the only chart,** on Algorab–Capella Dec φ (sky 0.062%);
  - his Ceres 0.024% on Antares–Sirius Dec 1:4:5;
  - his Ketu 0.031% on Capella–Deneb Algedi 5:8:13;
  - his Mercury 0.041% on Alphecca–Arcturus RA 4:5:9.
- His Neptune is 3rd on the tightest Makemake chord at the off, Capella–Procyon √2 (0.004%, exact 12:55).
- Callum Bewley's Sedna 2nd on Aldebaran–Sirius RA.
- The natal Makemakes of the winners (which lead both charts) are not on sky Makemake's chords; the jockey's Makemake is held by Chiron (Betelgeuse–Polaris, UNISON 0.010%).
- Number check: **Dec to Antares = 30φ** (48.5407 vs 48.5410); 2 ninths (Dec to Castor 88/9, Dec to Procyon 152/9). Note: the same 30φ came up at Newcastle (Makemake moves slowly, so this distance stays near 48.54 for months — not race-specific).
### Quaoar (RA 273.937, Dec −15.467)
- Quiet for the winners. Sky Quaoar sits in the same-age horses' natal Quaoar band (Arvico Bleu 0.028°, If Not For Dylan 0.028°, Slanelough 0.044°), so it does not single him out. His Quaoar is in UNISON on Altair–Pleiades 5:8:13 but loose (0.072%, 2nd).
- **Bellatrix–Rigel (Dec) now carries three sky bodies — Uranus 5:8:13, Haumea 3:5:8, Quaoar 1:2:3 — and Callum Bewley's SEDNA is 2nd (0.018%) on all three**, behind Finisk River's Rahu (0.016%). A stack where the winner is a close second, not first.
- Number check: 1 ninth (RA to Algol 1198/9) vs 1.5.
### Orcus (RA 157.111, Dec −11.475)
- **Arcturus–Bellatrix (RA) → Callum Bewley's MERCURY √2 (0.013%, tightest):** Sedna 1:6:7 (0.059%) + Orcus 3:4:7 (0.135%) — a loose stack (both sky chords slow).
- Others 2nd/3rd only: Callum Bewley's Ceres 2nd on Fomalhaut–Rigel RA; Arvico Bleu's Mercury 2nd on Equator–Rigel; his Vesta 3rd on Algorab–Bellatrix; his Haumea 3rd on Antares–Sirius φ.
- Favourite's side: Conor O'Farrell's Makemake tightest on Aldebaran–Altair (0.020%).
- Number check: 3 ninths (RA 1414/9, RA to Alphecca 689/9, Dec to Regulus 211/9) vs 1.5.
### Gonggong (RA 336.270, Dec −11.557)
- **Regulus–Rigel Dec 1:6:7: Arvico Bleu's VESTA 0.000%, the tightest** (his 2:5:7; sky 0.086%, applying, exact in 1.2 d). His Vesta is inside the string, 5.763 from Regulus (5.763/14.407); Gonggong is beyond the Rigel end (23.526/3.358).
  - The horse's Vesta is now held by Mars (Arcturus–Regulus φ, applying through the race, only the two winners on it) and Gonggong — both through Regulus, his Vesta 5.763 from Regulus each time.
- **Fomalhaut–Sirius Dec 2:5:7: Callum Bewley's HAUMEA tightest, 0.021%** (sky 0.030%, exact 05:29 next day).
- Arvico Bleu's Chiron 2nd on Algorab–Antares 1:2:3 (0.010%; Conor O'Farrell's Gonggong 0.002%); his Venus 2nd on Procyon–Rigel.
- Slow parallel: Gonggong RA on Finisk River's Neptune (0.009°).
- Number check: 4 ninths (Dec from the Equator 104/9, RA to Algol 637/9, Dec to Castor 391/9, Dec to Procyon 151/9) vs 1.5; no φ/√2/whole.
### Transpluto (RA 155.047, Dec +10.363)
- Winning pair tightest (slow sky chords):
  - **Callum Bewley's ERIS 0.007% on Capella–Castor RA 5:6:11** (sky 0.083%) — his Eris again (the Sun + Juno stack on Alphecca–Procyon).
  - **Arvico Bleu's own TRANSPLUTO 0.035% on Arcturus–Pleiades RA 3:5:8** (sky 0.081%) — sky Transpluto meets natal Transpluto.
  - Arvico Bleu's Eris tightest on Castor–Polaris Dec 3:8:11 (0.066%; sky 0.033%), his Neptune 2nd.
- **Bellatrix–Procyon RA now has three sky bodies (Uranus 5:6:11, Neptune 3:8:11, Transpluto 5:6:11), Arvico Bleu's Saturn 2nd on all three (0.019%) — but the favourite's jockey Conor O'Farrell's Ketu is tightest each time (0.002%).** A stack held tighter by the favourite's side.
- Callum Bewley's Gonggong 2nd on Aldebaran–Bellatrix RA (0.024%).
- Number check: RA to Algol = **108 whole** (107.9988); no ninths.
### The nodes (Rahu RA 60.183 Dec +20.611; Ketu opposite) — they complete stacks already seen
- **Alphecca–Procyon (Dec) → Callum Bewley's ERIS 0.001%: now a THREE-body stack** — the Sun 5:8:13 (via the Sun's parallel on his Eris; out 4 s after the finish) + Juno 4:5:9 + **Ketu 5:6:11** (0.138%, slow).
- **Aldebaran–Vega (Dec) → Callum Bewley's JUNO 0.006%: stack** — Sedna 3:8:11 (0.030%) + **Ketu 3:5:8** (0.039%).
- **Arcturus–Regulus (Dec) → only the two winners, again** — Mars φ (applying through the race, exact 14:43:58) + **Rahu 1:5:6** (0.138%): Arvico Bleu's VESTA tightest (0.053%), Callum Bewley's Saturn the only other chart, on both.
- Rahu √2 on Algol–Rigel: Callum Bewley's Juno tightest (0.012%; sky loose 0.136%) — his Juno is now held by Venus, Jupiter, Sedna, Ketu and Rahu.
- Rahu Sky 2:5:7 on Alkaid–Capella: Callum Bewley's Pallas tightest (0.030%).
- Ketu 4:5:9 on Aldebaran–Equator: Arvico Bleu's Chiron tightest (0.021%); Ketu on Regulus–Rigel RA: his Neptune 2nd.
- Number check: Rahu 2 ninths (Dec to Sirius 336/9, RA to Spica 1270/9); Ketu 1 ninth (RA to Spica 350/9). Chance level.
### Power points — Carlisle
- **Transpluto is again the only sky body on a power point** (RA 155.047, 10 pairs, at the RA 99% level). Its 10 pairs include **Capella–Castor (Callum Bewley's Eris 0.007%, tightest)**, **Arcturus–Pleiades (Arvico Bleu's own Transpluto 0.035%, tightest)**, Bellatrix–Procyon (Arvico Bleu's Saturn 2nd — the favourite's jockey's Ketu tighter), Aldebaran–Bellatrix (Callum Bewley's Gonggong 2nd).
  - **Caution:** Transpluto barely moves — RA 155.05 here (14 Oct 2021), 155.13 at Newcastle (2 Jan 2022). It sits on this RA node for months, so "Transpluto on a power point" is true of every race in that period, not a sign of this race. What can differ is which runners hold its strings.
- The Moon peaks at 7 (Dec −23.3, at its southern limit — below the lattice).
- **Natal: Arvico Bleu's HAUMEA (the imprint hub) is on a power point (RA 207.506, 10)**, and his Chiron Dec (12). Callum Bewley: none. The favourite pair has more: Gold Des Bois's Sun RA (16**), Orcus Dec (13), Ketu RA; Conor O'Farrell's Pallas Dec (14**), Pluto Dec (12). Sam Coltherd's Neptune Dec (14**).

## 72. SECOND LOOK — Exeter 15:15, 19 Oct 2021 (Forget You Not 25/1, James Best), read with the three methods (Eddie 7 Oct 07:43)
Method 1 (imprint, first read): **Juno with royal Regulus and φ** (#10 Regulus/Transpluto lands alone on the horse's Juno; horse Juno–Regulus, horse Juno × jockey Regulus, jockey Ceres–Juno 10φ); sky Mars → the jockey's Juno peaking at the off; horse Neptune × jockey Rahu = #7; **the horse's Procyon–Vesta held inside alone.**
Method 2 (first read): Mercury 5:8:13 on Algol–Pleiades exact AT the off — horse Eris UNISON 0.007%; Vesta on Mercury–Procyon 3 s before the off — horse Rahu UNISON (imprint pair).
### Sun (RA 204.215, Dec −10.084)
- **Capella–Procyon Dec 3:8:11: James Best's MAKEMAKE in UNISON, 0.011%, tightest** (sky 0.094%, separating; exact 14:17). His Makemake is inside the string, 3/11 from Capella (11.119/29.652); the Sun is beyond the Procyon end (56.078/15.305). Procyon (the imprint pair's star).
- **Betelgeuse–Procyon Dec 1:7:8: James Best's TRANSPLUTO tightest (0.026%), his ORCUS 3rd (0.040%)** — his Orcus exactly one base beyond Procyon (4.360/2.180), his Transpluto three bases beyond Betelgeuse. Sky 0.089% (applying, exact 16:11).
- The Sun's chord exact in the race, **Aldebaran–Bellatrix Dec φ (exact 15:17:52, 1.8 min in; 0.048% → 0.003% → 0.005% → 0.041%)**, goes to Sean Houlihan's Sun (the runner-up's jockey, 0.028%); James Best's Rahu 4th (0.063%).
- Forget You Not's Sun 2nd on Deneb Algedi–Equator (0.068%) and 3rd on Fomalhaut–Vega (0.039%).
- No parallel. Number check: Dec to Alkaid = 42√2 (59.3987 vs 59.3970; 59.3999 at the finish — just outside ±0.002 in the race).
### Mercury (RA 189.564, Dec −2.855) — **almost stationary** (it turned direct the day before, 18 Oct 2021: RA moving 0.24°/day, Dec 0.13°/day), so it behaves like a slow body
- **★ Slow parallel: Mercury sits on Forget You Not's natal ERIS Dec (−2.855 vs −2.859, 0.005°).** Mercury crossed his Eris Dec about 40 min before the off and is still within 0.006° through the race. So his Eris is in UNISON on Mercury's Dec chords:
  - **Algol–Pleiades 5:8:13, exact AT THE OFF (15:16:04): his Eris UNISON 0.007%, the tightest** — the first read's chord at the off. Mercury 43.811/26.961, his Eris 43.815/26.964 — the same point (beyond the Pleiades end).
  - **Castor–Deneb Algedi φ (0.027%, exact 14:48): his Eris UNISON 0.022%, the tightest** (Mercury 34.741/13.274; his Eris 34.748/13.270).
  - Also on Algol–Pleiades: James Best's Orcus 4th (0.024%).
- Altair–Spica √2 (sky 0.136%): the horse's Ceres 2nd (0.029%), Chiron 3rd.
- The imprint's Procyon string: Procyon–Vega RA 5:6:11 (0.024%) → Tom O'Brien's Haumea; James Best's Sun only 4th.
- Number check: no hits.
### Venus (RA 250.830, Dec −25.572)
- **★ Bellatrix–Castor Dec 4:5:9 (exact 14:39:53, 36 min before the off; 0.002% at off−30, 0.014% at the off, 0.016% at the finish): Forget You Not's CHIRON 0.001%, the tightest** (his 1:4:5).
  - Both beyond the Bellatrix end (base 25.535): his Chiron 6.385 out (1/4 of the base); Venus 31.924 out (5/4 of the base).
  - **Venus sits exactly one base length beyond his Chiron** (31.924 − 6.385 = 25.539). And Venus–Bellatrix (31.924) = his Chiron–Castor (31.926).
  - James Best's Haumea is 3rd (φ, 0.065%).
- Forget You Not's Makemake 3rd on Arcturus–Equator 3:4:7 (0.044%); his Juno in UNISON on Alphecca–Castor RA 1:7:8 (loose, 0.109%).
- No parallel. Number check: 2 ninths (Dec to Altair 310/9, Dec to Deneb Algedi 85/9) vs 1.5.
### Mars (RA 200.882, Dec −8.179) — both its race-time chords go to James Best
- **★ Deneb Algedi–Spica Dec 3:5:8, exact 15:12:28 (3.6 min before the off): James Best's RAHU tightest, 0.026%** (his 5:6:11). Rahu is the busiest body in the imprint (horse Neptune × jockey Rahu = #7).
  - 0.156% at off−30 → exact → 0.021% at the off → 0.050% at the finish → 0.193% at off+30: it comes and goes with the race.
  - **Mirror shape** (base 4.97): Mars is beyond the **Spica** end (7.950/2.981); his Rahu is beyond the **Deneb Algedi** end (4.139/9.106).
- **★ Fomalhaut–Procyon Dec 5:8:13, applying through the race, exact 15:30:28** (0.095% at off−30, 0.031% at the off, 0.020% at the finish): **James Best's GONGGONG tightest, 0.012%** (his 3:8:11); his Transpluto 4th (1:4:5, a quarter of the base beyond Procyon). Both Mars and his Gonggong are inside the string (Mars 21.445/13.399; his Gonggong 9.504/25.348). Procyon again (the Sun's chords also put his Makemake/Transpluto/Orcus on Procyon strings).
- Algol–Procyon 3:8:11 (exact 15:28) → Caspers Court's Pallas; Antares–Capella RA φ (exact 14:38) → Jarlath's Orcus.
- Slow parallel: Mars Dec near the favourite Pens Man's Orcus (0.045°).
- Number check: RA to Pleiades = 89φ (144.0061 vs 144.0050); 2 ninths (Dec to Algorab 75/9, Dec to Fomalhaut 193/9).
### Jupiter (RA 324.781, Dec −15.246)
- Slow; nothing exact near the race. Winning pair: Forget You Not's Sun tightest on Algol–Spica RA (0.028%; sky 0.076%); James Best's Rahu 2nd on Algorab–Fomalhaut RA 1:7:8 (0.017%) and his Mercury 2nd on Alkaid–Fomalhaut RA 1:6:7 (0.021%). Otherwise quiet; the field spreads across its chords.
- No parallel. Number check: no hits.
### Saturn (RA 309.246, Dec −19.404) — slow, but it holds both winners
- **Alkaid–Bellatrix Dec 3:5:8 (sky 0.089%): the winners are 1st and 2nd — Forget You Not's PLUTO 0.001%, James Best's MERCURY 0.007%.** All three points are beyond the Bellatrix end (base 42.96): Saturn 3/5 of the base out (25.755), his Pluto 5/8 (26.853), the jockey's Mercury 3/4 (32.218).
- **Altair–Vega RA 5:8:13 (sky 0.055%): the winners are 1st and 2nd — James Best's JUNO 0.038% (the imprint body), Forget You Not's Uranus 0.049%.** Mirror shape: Saturn is beyond the **Altair** end (11.547/30.012); the jockey's Juno is beyond the **Vega** end (43.089/24.626, 4/3 of the base out).
- **Equator–Vega Dec 1:2:3 (sky 0.045%, applying): Forget You Not's QUAOAR 0.000%, the tightest** (his 2:5:7). Both beyond the Equator end: Saturn half a base out (19.404), his Quaoar 2/5 of a base out (15.512).
- Number check: 2 ninths (Dec to Algorab 26/9, Dec to Polaris 978/9) vs 1.5.
### Ceres (RA 70.789, Dec +16.226)
- **Fomalhaut–Polaris RA 3:5:8: James Best's JUNO in UNISON, 0.038%, the tightest** (sky 0.091%, applying, exact 01:51 next day). His Juno (the imprint body) is now held by Saturn (Altair–Vega, mirror) and Ceres.
- **Polaris–Spica Dec 3:8:11 (sky 0.012%, exact 20:34): James Best's TRANSPLUTO 0.005%, the tightest.**
- **Slow parallel: Ceres sits on Forget You Not's natal MARS Dec (0.018°)** — his Mars in UNISON on Ceres's Dec chords (e.g. Polaris–Spica, 0.090%).
- Regulus–Sirius RA 3:5:8 (0.049%): James Best's Ketu (0.005%) and Makemake (0.010%) 3rd/4th behind Tom O'Brien (0.000%).
- James Best's Saturn 2nd on Betelgeuse–Deneb Algedi.
- Number check: 1 ninth (RA to Vega 1364/9) vs 1.5.
### Pallas (RA 341.717, Dec −8.299)
- **Altair–Spica (Dec): Pallas 1:6:7 exact 15:05:16 (11 min before the off; 0.050% at the off) + Mercury √2 (0.136%) — on both, Forget You Not's CERES is 2nd (0.029%) and his CHIRON 3rd (0.033%)**, behind Pointed And Sharp's Gonggong (0.024%). A stack where the winner is close but not first. Altair again.
- **Betelgeuse–Vega Dec 1:2:3: Forget You Not's SATURN 0.009%, the tightest** (sky loose, 0.105%).
- Forget You Not's Pluto 2nd on Alkaid–Betelgeuse 3:8:11 (only two charts on it, applying, exact 16:20).
- James Best's Makemake in UNISON on Arcturus–Betelgeuse (4th, loose).
- Slow parallel: Pallas Dec near Forget You Not's natal Orcus (0.057°).
- Number check: 1 ninth (RA to Algol 588/9) vs 1.5.
### Juno (RA 261.249, Dec −12.316) — the imprint body; its race chord goes to the jockey
- **★ Algol–Altair RA 1:3:4, exact 15:17:52 (1.8 min into the race): James Best's GONGGONG tightest, 0.022%** (his 2:5:7; the first read had this as the only chart).
  - Centred on the race: 0.018% at off−30, 0.001% at the off, 0.002% at the finish, 0.015% at off+30.
  - His Gonggong is inside the string, 2/7 of the base from Altair (78.118/31.240); Juno is beyond the Altair end, a third of a base out (145.800/36.450). Altair again.
  - **The Sun's Aldebaran–Bellatrix φ is exact at the same second (15:17:52)** — two sky chords exact together in the race (the Sun's goes to the runner-up's jockey).
  - The jockey's Gonggong is now held by Mars (Fomalhaut–Procyon, applying, exact 15:30) and Juno (exact in the race).
- Sky Juno does not play the winners' natal Juno on the stars (the jockey's Juno is held by Saturn and Ceres).
- Others: Aldebaran–Rigel 1:6:7 exact 15:43 → Pens Man's Pluto (0.002%), the favourite.
- No parallel. Number check: 1 ninth (Dec to Bellatrix 168/9) vs 1.5.
### Vesta (RA 223.437, Dec −12.545)
- On the star strings Vesta is quiet for the winners: **James Best's MAKEMAKE tightest on Pleiades–Regulus RA 3:4:7** (0.026%; sky 0.085%); his Makemake also 4th on Alkaid–Alphecca φ (exact 15:07, 9 min before the off). Forget You Not's Juno 3rd on Procyon–Rigel RA; his Neptune 2nd on Alkaid–Alphecca.
- Vesta's Dec sits near James Best's natal JUNO (0.078°, loose) — Juno the imprint body.
- Its main link stays off the stars (first read, L4): **Vesta 5:6:11 on Mercury–Procyon, exact 3 s before the off — Forget You Not's Rahu in UNISON, the only chart, on his imprint pair Procyon–Vesta.**
- Number check: 1 ninth (Dec to Vega 462/9) vs 1.5.
### Uranus (RA 40.829, Dec 15.379)
- 11 star chords (RA 4, Dec 6, Flat 1). Nothing exact in the race; Uranus barely moves through it.
- **Forget You Not's MARS — the only chart on Algorab–Bellatrix Flat φ** (his Mars 3:8:11, 0.092%). Sky Uranus and his Mars sit on the same side, beyond Bellatrix, close together (Uranus 150.058/41.452; his Mars 149.306/40.697). Exact 23 h after the off. Mars again.
- **Algorab–Betelgeuse Dec 1:3:4** (exact 8.5 h before the off): Forget You Not's Pluto 1:6:7 2nd (0.027%). His Pluto is 3.986 beyond the Algorab end; sky Uranus is 7.970 beyond the Betelgeuse end — opposite ends, twice the distance.
- **Altair–Castor RA √2 (applying 1.7 d): SAME BODY** — his natal Uranus 4:5:9 (0.085%, 3rd), inside the string (78.237/97.713); sky Uranus beyond Castor. Jarlath's Jupiter is tighter (0.064%). Altair again.
- Alphecca–Vega RA 3:8:11 (applying): his Mercury 2nd, his Ceres 4th; Jarlath's Mars tightest (0.017%).
- James Best: nothing on Uranus.
- Favourite's side: **Pens Man's Vesta tightest on Arcturus–Spica Dec 1:7:8 (0.006%)**, his Saturn 4th; his Juno 3rd on Capella–Polaris. 3rd home Caspers Court/Tom Scudamore: Tom Scudamore's Quaoar tightest on Capella–Polaris (0.003%). Pulled-up Pointed And Sharp on four strings.
- Parallels: Uranus on Pointed And Sharp's Jupiter Dec (0.014°) and on Tom Scudamore's Transpluto (0.068°). Not the winners.
- Deneb Algedi–Procyon 1:1:2 and the course-latitude strings: no natal charts on them.
- Number check: 2 hits vs 0.44 — Dec to Fomalhaut 45 (whole), Dec to course latitude 25√2. Neither on a winners' string.
- Eddie (7 Oct): "maybe Uranus is unsettling the fav as well in these races — keep it on watch". ON WATCH: Uranus on the favourite's side (Newcastle, Wincanton, Carlisle, Exeter).
### Neptune (RA 351.816, Dec −4.802)
- 10 star chords (RA 5, Dec 5). One is close to the race: Equator–Rigel Dec √2, exact 16:35 (1.3 h after the off).
- **James Best's ERIS tightest on Regulus–Vega Dec 5:8:13** (0.017%, exact 21.5 h before the off). Neptune is beyond Regulus (16.771/43.593); his Eris is beyond Regulus too, further out (21.458/48.277).
- **James Best's HAUMEA tightest on Castor–Polaris RA φ** (1:1:2, 0.026%). His Haumea is one base length beyond Castor (75.356/150.692); Neptune is beyond the other end, Polaris (121.833/46.566).
- **Forget You Not's MARS on Bellatrix–Pleiades RA** (φ, 0.112%, 3rd; applying, exact in 1.7 d). Neptune and his Mars are both beyond the Pleiades end (Neptune 89.470/65.061; Mars 39.485/15.071). His Mars is now held by Ceres (parallel), Uranus (Algorab–Bellatrix Flat) and Neptune — different strings, two of them Bellatrix strings.
- **Forget You Not's PLUTO 2:3:5 on Equator–Rigel Dec** (0.045%, 2nd). His Pluto is beyond Rigel (20.505/12.306); Neptune is inside the string. Exact 16:35. His Pluto was also on Uranus's Algorab–Betelgeuse.
- **SAME BODY on Bellatrix–Procyon RA (Procyon):** his natal Neptune 1:3:4 (0.105%, 3rd). Both beyond Bellatrix; his Neptune 11° further out (100.522/134.064 vs sky 89.470/123.006). Separating (exact 2.2 d ago).
- Alkaid–Antares Dec: his Jupiter 2nd (√2), with his Ketu and Sun also on it, all inside the string with Neptune.
- **The runner-up's pair:** Neptune sits on Sean Houlihan's natal JUNO Dec (0.013°) and near Jarlath's Chiron Dec (0.060°). Jarlath's Haumea tightest on Capella–Regulus (0.008%).
- Favourite: Pens Man's Gonggong 2nd on Capella–Regulus and Orcus 3rd on Regulus–Vega; Jonjo O'Neill Jr's Neptune UNISON 4th on Equator–Rigel. Light this time.
- Number check: 1 hit vs 0.44 — Dec to Deneb Algedi 7φ (11.3260).
### Pluto (RA 296.258, Dec −22.936)
- 11 star chords (RA 4, Dec 6, Sky 1). The tightest: Betelgeuse–Deneb Algedi RA 1:4:5, 0.006%, exact 08:40 on the day.
- **Betelgeuse–Deneb Algedi RA 1:4:5 — SAME BODY for the favourite:** Pens Man's natal PLUTO 1:3:4 tightest (0.009%). Sky Pluto and his Pluto are both beyond Deneb Algedi (sky 152.537/30.506; his 162.698/40.672). His Sedna is 3rd.
  - On the same string: James Best's SEDNA 2nd (φ, 0.021%), inside (46.621/75.419); Forget You Not's SUN at the midpoint (1:1:2, 61.033/60.998).
- **James Best's VENUS in UNISON on Arcturus–Polaris Dec 3:5:8** (0.048%). Sky Pluto 42.108/112.199; his Venus 42.028/112.108 — almost the same spot, beyond Arcturus. That is the slow parallel: Pluto 0.095° from his natal Venus Dec (applying, exact in 60 d).
  - Jonjo O'Neill Jr's Eris 4th on the same string; Pluto is also near Jonjo O'Neill Jr's Mercury Dec (0.073°).
- Forget You Not: only his Sun at the midpoint above.
- Favourite heavy again: Pens Man's Pluto (same body, tightest), Makemake tightest on Algorab–Spica Dec, Ceres 2nd on Arcturus–Regulus. The runner-up's jockey Sean Houlihan's Sun tightest on Polaris–Vega RA (exact 03:35).
- Number check: 2 ninths (Dec to Aldebaran 355/9, Dec to Spica 106/9) vs 1.5.
- Eddie (7 Oct, after Pluto): "it looks like the horse or jockey needs to lead but definitely needs plenty of support from the other". Next after Exeter: a detour to Frankie Dettori's seven-winner day (Ascot, 28 Sep 1996), read in this format.
### Chiron (RA 7.930, Dec 5.991)
- 10 star chords (RA 6, Dec 2, Flat 1, Sky 1). Closest to the race: Altair–Bellatrix Dec 1:7:8, exact 15:25 (4 min after the finish) — Pointed And Sharp (pulled up) tightest.
- **Rigel–Sirius Dec 3:5:8 (exact 15.6 h before the off) — HORSE AND JOCKEY TOGETHER:** Forget You Not's KETU tightest (√2, 0.009%), James Best's PLUTO 2nd in UNISON (0.013%), Forget You Not's CERES 3rd (0.019%); also James Best's Uranus (0.092%) and Gonggong. No other runner in the top three.
  - Chiron is beyond Rigel (14.190/22.711). His Ketu is beyond Rigel just inside it (12.049/20.569); James Best's Pluto beyond Rigel (5.107/13.618). His Ceres is beyond the Sirius end (15.336/6.815), at nearly the same spot as James Best's Uranus (15.313/6.802).
- **Aldebaran–Procyon RA 3:4:7 (applying, exact in 1.6 d) — Procyon:** James Best's HAUMEA tightest at 0.001%, beyond Procyon (120.025/74.179); Chiron beyond the other end, Aldebaran (61.055/106.892). Forget You Not's RAHU sits 0.08° from James Best's Haumea (119.942/74.096) — horse and jockey at the same spot. Sean Houlihan's Haumea 3rd.
- Capella–Procyon RA 1:2:3: James Best's Vesta 3rd (0.019%); Sean Houlihan's Neptune tightest (0.000%), Pens Man's Haumea 2nd.
- Algorab–Pleiades RA 3:8:11: James Best's MAKEMAKE tightest (0.015%).
- Antares–Regulus Sky 5:6:7: Forget You Not's SUN in UNISON, tightest (0.096%, loose sky chord).
- Favourite: Pens Man's CHIRON tightest on Altair–Arcturus Flat (same body, 0.018%); his Haumea 2nd on Capella–Procyon; Jonjo O'Neill Jr's Sun 2nd on Antares–Spica.
- No parallel. Number check: no hits.
### Eris (RA 26.353, Dec −1.435)
- 15 star chords (RA 6, Dec 8, Sky 1). The tightest: Fomalhaut–Procyon Dec φ (0.008%, exact 11:47) and Betelgeuse–Sirius RA 1:5:6 (0.009%).
- **STACK — Fomalhaut–Procyon Dec → James Best's GONGGONG:** Eris φ (exact 11:47, 3.5 h before the off) + Mars 5:8:13 (applying, exact 15:30). His Gonggong tightest (0.012%) on Eris's chord as on Mars's. Eris 28.189/6.655, Mars 21.445/13.399, his Gonggong 9.504/25.348 — all inside the string. His Transpluto 4th again (beyond Procyon). With Juno (Algol–Altair, exact in the race) his Gonggong is now held three ways. Procyon.
- **STACK — Regulus–Vega Dec → James Best's ERIS:** Neptune 5:8:13 + Eris 1:2:3 (SAME BODY). His Eris tightest on both (0.017%). All beyond Regulus in a row: sky Eris 13.403, Neptune 16.771, his Eris 21.458.
- **STACK — Bellatrix–Pleiades RA → Forget You Not's MARS:** Neptune 3:8:11 + Eris 4:5:9 (his Mars 3rd, 0.112%, loose). All beyond Pleiades: his Mars 15.071, Eris 30.524, Neptune 65.061. With Ceres (parallel) and Uranus (Algorab–Bellatrix Flat), his Mars is held by four slow bodies.
- **Antares–Deneb Algedi RA 3:4:7: Forget You Not's TRANSPLUTO tightest (0.009%).** His Transpluto beyond Antares (95.275/174.677); Eris beyond Deneb Algedi (139.006/59.588) — opposite ends. Deneb Algedi again.
- Others: James Best's Haumea tightest on Algol–Sirius RA (0.060%); his Sun 2nd on Bellatrix–Spica Dec, with Forget You Not's Ceres 4th; Forget You Not's Neptune and Rahu on Alphecca–Bellatrix Dec.
- Favourite light: Pens Man 3rd on three strings. Caspers Court (3rd home) and the runner-up's pair busy.
- Parallel: Eris on Connor Brace's Orcus (pulled up). Number check: 2 hits — Dec to Aldebaran φ⁶ (17.9438), RA to Betelgeuse 562/9.
### Sedna (RA 59.157, Dec 8.136)
- 10 star chords (RA 4, Dec 4, Flat 2).
- **STACK grows — Regulus–Vega Dec → James Best's ERIS:** Sedna 1:7:8 (0.020%, exact 08:58 on the day) joins Neptune 5:8:13 and Eris 1:2:3. His Eris tightest on all three (0.017%). All beyond Regulus in a row: Sedna 3.832, sky Eris 13.403, Neptune 16.771, his Eris 21.458.
- Forget You Not: only his Haumea 2nd on Algol–Algorab Dec (0.087%, loose).
- Sedna leans to the 3rd home, Caspers Court / Tom Scudamore: two parallels (Sedna on Tom Scudamore's natal Sun RA 0.036°, Caspers Court's Venus Dec 0.087°); Tom Scudamore's Sun in UNISON tightest on Deneb Algedi–Fomalhaut, his Venus tightest on Aldebaran–Bellatrix. Runner-up's jockey Sean Houlihan's Transpluto 0.001% on Algol–Castor Dec. Favourite: Pens Man's Uranus 2nd on Altair–Fomalhaut.
- Number check: 2 ninths (RA to Procyon 501/9, Dec to Rigel 147/9) vs 1.5.
### Haumea (RA 215.950, Dec 15.048)
- 7 star chords (RA 3, Dec 3, Sky 1).
- **★ Procyon–Spica Dec 3:5:8 — EXACT IN THE RACE** (checked minute by minute on the true positions: 0.0018% at off−30, 0.0001% at the off, exact about 15:17:40, 0.0002% at 15:21, 0.0016% at off+30). So three chords come exact in the first two minutes of the race: this one, Juno's Algol–Altair (15:17:52, James Best's Gonggong) and the Sun's Aldebaran–Bellatrix (15:17:52, runner-up's jockey). (Slow-body exact seconds are arithmetic; the minute is what counts.)
  - Favourite Pens Man's CERES tightest (4:5:9, 0.002%), beyond the Spica end (29.490/13.107).
  - **Forget You Not's TRANSPLUTO 2nd (φ, 0.026%)**, beyond the Procyon end with Haumea (Haumea 9.828/26.207; his Transpluto 6.256/22.639). Procyon again. James Best's Pallas 5th (beyond Spica).
- **Castor–Vega RA φ: Forget You Not's RAHU joint tightest (5:6:11, 0.004%)** with Tom Scudamore's Quaoar. Both inside the string (Haumea 102.301/63.284; his Rahu 75.270/90.320). Applying, exact in 1.8 d. (His Rahu also sat next to James Best's Haumea on Chiron's Aldebaran–Procyon.)
- **Algol–Antares Dec 5:8:13: James Best's MARS 3rd (3:8:11, 0.019%)**, inside the string (18.376/49.013); Haumea inside too (25.908/41.480). Pens Man's Chiron tightest (0.000%), Sean Houlihan's Eris 2nd (0.002%). Applying, exact in 1.3 d. Mars again — this time the jockey's natal Mars.
- Altair–Vega Sky: Forget You Not's Pallas the only chart (0.016%, loose sky chord). Deneb Algedi–Vega RA: James Best's Mercury 2nd.
- Favourite again on Haumea: Pens Man tightest on Procyon–Spica (in the race) and on Algol–Antares.
- No parallel. Number check: no hits.
### Makemake (RA 198.180, Dec 22.076)
- 13 star chords (RA 3, Dec 9, Sky 1). Makemake sits on James Best's natal HAUMEA Dec (0.054°), so his Haumea joins Makemake's Dec chords (e.g. UNISON √2 on Fomalhaut–Rigel, 4th).
- **Castor–Regulus RA 5:6:11: James Best's JUNO tightest, 0.001%** (his 3:8:11; applying, exact in 1.8 d). Makemake and his Juno both beyond Regulus (Makemake 84.531/46.091; his Juno further out 140.946/102.507). His Juno — the imprint body — is now held by Saturn (Altair–Vega, mirror), Ceres (Fomalhaut–Polaris UNISON) and Makemake (tightest of all), with Vesta near its Dec.
- **SAME BODY — Aldebaran–Alphecca Dec 5:6:11 (exact 09:16): James Best's MAKEMAKE 4th** (0.026%), beyond Alphecca (18.370/8.166); sky Makemake inside (5.566/4.641). Forget You Not's Sun also on it (loose).
- Others: James Best's Jupiter 3rd on Alkaid–Procyon (Procyon); his Mars 4th on Aldebaran–Vega (loose); Forget You Not's Orcus 4th on Aldebaran–Sirius (loose).
- Favourite: Pens Man's ORCUS tightest on Makemake's tightest chord, Aldebaran–Sirius RA 1:3:4 (0.003%; exact 00:46 tonight); Jonjo O'Neill Jr 2nd on two strings.
- Parallel also on Blaze A Trail's Sun (pulled up). Number check: 3 hits — RA to Capella whole 119 (119.0017), Dec to Betelgeuse 132/9, RA to Spica 28/9.
### Quaoar (RA 273.998, Dec −15.480)
- 7 star chords (RA 2, Dec 5). Quaoar has hardly moved since 2011–15, so it sits near the natal Quaoar Dec of most horses (Forget You Not closest, 0.032°; Jarlath, Caspers Court, Pens Man and others within 0.08°) — not distinctive on its own.
- **★ Altair–Pleiades Dec 5:8:13 (applying, exact in 7.5 d) — the top FOUR are the winning pair:** Forget You Not's QUAOAR in UNISON (0.001%, same body), James Best's TRANSPLUTO (1:2:3, 0.001%), his MAKEMAKE (√2, 0.007%), his ORCUS (φ, 0.015%). Jarlath's Quaoar 5th (0.016%).
  - Sky Quaoar beyond Altair (24.353/39.585); his Quaoar at nearly the same spot (24.379/39.616). James Best's Transpluto (5.079/10.158) and Orcus (5.821/21.059) beyond Altair, close in; his Makemake beyond the Pleiades end (26.012/10.774).
  - One sky body, the horse's body and three of the jockey's on one string — the horse and jockey together (as on Chiron's Rigel–Sirius). Altair again. Transpluto, Makemake and Orcus are the jockey's bodies from the Sun read (Capella–Procyon, Betelgeuse–Procyon).
- **Arcturus–Castor RA 3:5:8 (applying, exact in 4.4 d): the top TWO are the winning pair** — James Best's VENUS (2:5:7, 0.001%) beyond Arcturus (40.104/140.362), Forget You Not's MERCURY (3:4:7, 0.004%) beyond Castor (175.472/75.204); Quaoar beyond Arcturus (60.095/160.349). (Natal Mercury and Venus move over the unknown birth hour, so these two are softer.)
- Favourite: Jonjo O'Neill Jr's Haumea tightest on Betelgeuse–Fomalhaut Dec (0.001%, the tightest Quaoar chord), his Venus 2nd, Pens Man's Gonggong 3rd.
- Number check: 3 hits — RA whole 274 (273.9981), Dec to Fomalhaut 10√2, Dec to Betelgeuse 206/9. The Betelgeuse–Fomalhaut chord carries two of them (favourite's string).
- Eddie (7 Oct, after Quaoar): "what seemed to be a weak race is now looking pretty strong to me".
### Orcus (RA 157.186, Dec −11.532)
- 9 star chords (RA 4, Dec 4, Sky 1). Orcus is near Transpluto (RA ≈155), the slow power-point body.
- **Alkaid–Pleiades Dec √2 (applying, exact in 1.2 d): James Best's SEDNA tightest at 0.000%** (his 4:5:9), with his QUAOAR 3rd (0.020%) and his ERIS just behind (0.023%). All beyond the Pleiades end: his Sedna 20.164, Orcus 35.638, his Eris 33.598, his Quaoar 37.814 (from Pleiades). Three of the jockey's bodies on one Orcus string; his Eris is the one stacked on Regulus–Vega.
- **SAME BODY — Algol–Spica RA 2:5:7 (applying, 2.6 d): James Best's ORCUS 3rd (0.062%)**, inside the string with sky Orcus (his 84.110/70.135; Orcus 110.137/44.107). **Forget You Not's SUN tightest (0.028%)**, beyond Algol (19.278/173.546) — soft, natal Sun moves ~1° over the birth day.
- Forget You Not's Quaoar 4th on Antares–Bellatrix (loose).
- Others: Sean Houlihan's Ceres 0.004% and Jonjo O'Neill Jr's Uranus 0.010% on Algol–Procyon; Caspers Court's Quaoar UNISON on Fomalhaut–Rigel; Pens Man's Neptune tightest on Arcturus–Procyon.
- No parallel. Number check: 1 ninth (Dec to Rigel 30/9).
- Eddie (7 Oct): "What stands out for the winners is the combinations, more than single tight hits — which is what we have agreed before."
### Gonggong (RA 336.238, Dec −11.566)
- 12 star chords (RA 4, Dec 6, Flat 2). Gonggong's Dec (−11.566) is within 0.034° of Orcus's (−11.532), so the two share Dec strings.
- **STACK — Alkaid–Pleiades Dec √2 → James Best's SEDNA (0.000%) and QUAOAR (0.020%):** Orcus and Gonggong side by side beyond Pleiades (Orcus 35.638, Gonggong 35.672 from Pleiades); his Sedna 20.164, his Quaoar 37.814, his Eris 33.598 on the same string.
- **Fomalhaut–Sirius Dec 2:5:7: James Best's SEDNA 3rd (5:8:13, 0.026%)** — his Sedna on a second Gonggong string. Both beyond Sirius (Gonggong 18.058/5.154; his Sedna 33.567/20.654). Jarlath's Neptune tightest (0.003%).
- **Betelgeuse–Spica RA 5:5:6: James Best's TRANSPLUTO 2nd at the MIDPOINT** (1:1:2, 0.011%; 56.251/56.245); his Pallas 4th.
- Forget You Not: his PALLAS in UNISON on Altair–Spica RA 2:5:7 (3rd, 0.077%, inside the string); his Mercury 2nd and Ceres 4th on Alphecca–Vega RA (the same string as Uranus's 3:8:11 — both Uranus and Gonggong put his Mercury/Ceres on it, Jarlath's Mars tightest on both); his Quaoar 3rd on Procyon–Vega Dec 1:2:3 (Gonggong's tightest chord, 0.007%; Procyon).
- Runner-up Jarlath strong on Gonggong: Uranus 0.000% on Altair–Spica, Neptune 0.003% on Fomalhaut–Sirius, Mars tightest on Alphecca–Vega.
- No parallel. Number check: 2 ninths (RA to Algorab 1339/9, RA to Antares 800/9).
### Transpluto (RA 155.082, Dec 10.350)
- 21 star chords (RA 10, Dec 11) — the busiest slow body, as at the other races (it sits near a power point for months). Several of its strings are shared with other slow bodies, which makes stacks:
- **STACK — Castor–Vega RA → Forget You Not's RAHU:** Haumea φ + Transpluto 1:3:4; his Rahu joint tightest on both (0.004%), inside the string (75.270/90.320). Tom Scudamore's Quaoar shares it (0.004% on both).
- **STACK — Algol–Antares Dec → James Best's MARS 3rd on both** (Haumea 5:8:13 + Transpluto 5:6:11, his Mars 0.019%). Shared: Pens Man's Chiron 0.000% and Sean Houlihan's Eris 0.002% are ahead on both.
- **STACK — Bellatrix–Procyon RA → Forget You Not's NEPTUNE 3rd on both** (Neptune 3:8:11 + Transpluto 5:6:11; 0.105%, loose). Procyon.
- **Forget You Not's GONGGONG tightest on Aldebaran–Procyon Dec 5:6:11 (0.005%)**, beyond Procyon (29.351/18.062); Transpluto inside (6.159/5.130). Procyon.
- **James Best's CHIRON on two Procyon strings:** tightest on Procyon–Rigel Dec φ (0.031%) and 2nd on Algorab–Procyon Dec φ (0.028%). Both times his Chiron (8.302 from Procyon) and Transpluto (5.130 from Procyon) sit on the same side of Procyon.
- **SAME BODY — Aldebaran–Castor Dec 2:5:7: James Best's TRANSPLUTO 2nd (1:6:7, 0.010%)**, beyond Aldebaran alongside sky Transpluto (his 2.563/17.939; sky 6.159/21.536).
- Others: Forget You Not's Venus 2nd on Betelgeuse–Castor RA (0.011%; natal Venus soft); James Best's Saturn 2nd and Haumea 4th on Betelgeuse–Deneb Algedi Dec; his Makemake 4th on Arcturus–Betelgeuse; his Vesta 4th on Alphecca–Deneb Algedi.
- Favourite's stack: Aldebaran–Sirius RA (Makemake 1:3:4 + Transpluto 3:5:8) → Pens Man's ORCUS tightest on both (0.003%). Caspers Court's Ceres tightest on two Deneb Algedi strings (0.001%); parallel on Caspers Court's Juno (0.077°).
- Number check: 3 hits — Dec to Bellatrix whole 4 (3.9987), Dec to Regulus φ (1.6184), RA to Rigel 688/9.
### The nodes — Rahu (RA 59.695, Dec 20.519) / Ketu (RA 239.695, Dec −20.519)
- Rahu 11 star chords (RA 3, Dec 7, Flat 1); Ketu 7 (RA 3, Dec 4). The nodes move ~0.05°/day, so their exact times are in hours.
- **KETU on Forget You Not's natal PLUTO Dec (0.014°)** — his Pluto joins every Ketu Dec chord. **Alkaid–Bellatrix Dec 5:8:13: his PLUTO in UNISON, tightest (0.001%), James Best's MERCURY 2nd (0.007%)** — the winning pair 1st and 2nd. Ketu and his Pluto at the same spot beyond Bellatrix (69.833/26.870 and 69.817/26.853); his Mercury further out (75.179/32.218; natal Mercury soft). Exact 13:11 next day.
  - His Pluto is now held by Uranus (Algorab–Betelgeuse), Neptune (Equator–Rigel), Ketu (parallel) — and **STACK on Equator–Rigel Dec: Neptune √2 + Rahu 2:5:7, his Pluto 2nd on both (0.045%)** (Tom Scudamore's Sedna tightest on both, 0.003%).
  - The favourite Pens Man's Pluto is also near Ketu's Dec (0.039°), UNISON on Alkaid–Betelgeuse (just ahead of Forget You Not's) and Algol–Betelgeuse.
- **RAHU: James Best's ERIS tightest on Alphecca–Castor Dec 5:6:11, 0.000%** (his 1:7:8; exact 21:23). Both beyond Alphecca (Rahu 6.198/11.368; his Eris 36.206/41.379). His Eris is now held by Neptune, Eris and Sedna (Regulus–Vega), Orcus and Gonggong (Alkaid–Pleiades) and Rahu — six slow bodies.
- **STACK — Capella–Procyon Dec → James Best's MAKEMAKE:** the Sun 3:8:11 (his Makemake UNISON, exact 14:17) + Rahu 3:5:8 (exact 01:29 next day); his Makemake tightest on both (0.011%), inside the string (11.119/29.652). His natal Rahu is also on it (0.048%). Procyon. His Makemake also tightest on Rahu's Pleiades–Rigel Dec (0.046%).
- Ketu: James Best's SEDNA tightest on Alphecca–Antares Dec (0.038%).
- **Ketu on Algorab–Deneb Algedi RA 3:5:8, exact 14:25:40 (50 min before the off), only chart Jonjo O'Neill Jr's Quaoar (√2, 0.031%)** — the favourite's jockey. Ketu with Deneb Algedi (the Pholas lead).
- Shared stack, not the winners: Capella–Regulus RA (Neptune 5:6:11 + Ketu 5:6:11) → Jarlath's Haumea tightest on both (0.008%), Pens Man's Gonggong 2nd on both; Forget You Not's Haumea 4th.
- Other parallels: Rahu near Tom Scudamore's Sun, Ketu near his Uranus.
- Number check: Rahu 1 ninth (Dec to Betelgeuse 118/9); Ketu Dec to Bellatrix 19√2 — on the Alkaid–Bellatrix string where the winners are 1st and 2nd.
### Power points (star-lattice nodes)
- Background (race day): Dec mean 5.6, 99% 12, 99.9% 14; RA mean 4.1, 99% 10, 99.9% 13.
- Sky: only TRANSPLUTO on a power point (RA 155.082, load 10 = the 99% level; its Dec load 11 just under). Same as Newcastle — it sits there for months. Its strings here carry the winners: the Castor–Vega stack on Forget You Not's Rahu, his Gonggong on Aldebaran–Procyon, James Best's Chiron on two Procyon strings, James Best's own Transpluto (same body). The Moon peaks at 10 Dec pairs 91 s before the off (below 99%).
- Natal points on power points (against each chart's own birth-day stars):
  - **James Best's SEDNA Dec 3.943 — load 13, the highest natal load in the field** (above the 99% level, just under 99.9%). His Sedna is the body Orcus + Gonggong hold tightest on Alkaid–Pleiades (0.000%), Gonggong again on Fomalhaut–Sirius, and Ketu on Alphecca–Antares (tightest) — and Pluto's Betelgeuse–Deneb Algedi (2nd).
  - Forget You Not's Pallas RA 270.172 (10, at the 99% level).
  - Others: Sean Houlihan's Saturn Dec (12), Jarlath's Jupiter and Mercury RA (11), Tom Scudamore's Orcus RA (10), Pens Man's Juno RA (10), Pointed And Sharp's Jupiter RA (10).
- So: the winning jockey's power-point body is one the slow sky holds hard in this race. Power points so far: Transpluto (sky) at Newcastle, Carlisle and Exeter — but it sits there for months, so not race-specific. Exeter adds a natal one: James Best's Sedna (load 13).
- **Eddie (7 Oct 08:44) — THE WORKING PROCESS, for every method:** "we have been very successful in these race reads because we have gone one body at a time, methodically, and say what we see with that body — then pull it all together as we go & at the end. This is the working process we need to implement for each method. One at a time — even one body per one layer at a time — that is how you consistently see all the details."

## 73. DETOUR — Frankie Dettori's seven-winner day, Ascot 28 Sep 1996 (Eddie 7 Oct 08:46): "we just need to look at one of his charts for one race to see what is going on as he must have some major chords that come together that last all day". Race chosen: the Diffident race.
- Racal Diadem Stakes, Group 2, 6f, Good to Firm, 12 ran. Scheduled 14:35; **off 14:36:00** (BST = 13:36:00 UT); **winning time 1m 15.36s** (slow by 2.86s). Total SP 119%.
- 1st DIFFIDENT (FR) 12/1, Frankie Dettori (Saeed bin Suroor), draw 3. Born 16 Jan 1992, France. Dettori born 15 Dec 1970, Italy.
- 2nd Lucayan Prince 15/8F (W R Swinburn) by a short head; 3rd Leap For Joy 14/1 (Richard Hills) by a short head.
- Charts: Eddie builds them on the Mac (race_batch_19960928_ascot_1435) — waiting for the workbook.
- Files built (7 Oct): Eddie's workbook (charts v2.3, engine v2.2, fingerprint 64612c16fe) → allpos/19960928_ascot_1435__*, sky/…__SKYM (local engine matches the workbook to 2e-12°; TNOs: heliocentric position from the workbook held fixed, re-projected each minute — reflex motion only, so their exact-day estimates are rough). Tuned layers run (lattice/dump, TL*/TN_ files).
### Method 1 — Dettori's chart, one body at a time (natal chords with the stars at birth and with two of his own bodies; no birth time, so each chord is checked at 00:00 and 24:00 of 15 Dec 1970 — "held all day" = within 0.15% at both ends)
#### Sun (RA 262.883, Dec −23.284; moves 1.1° in RA over the day, 0.05° in Dec — so his Sun's RA chords are soft, its Dec chords firm)
- Held through his whole birth day (Dec): **Castor–Vega 1:8:9** (0.032%; 0.019% at 00:00, 0.073% at 24:00); **Betelgeuse–Polaris 3:8:11** (0.023%); **Altair–Polaris 2:5:7** (0.035%); **Capella–Polaris 5:8:13** (0.086%); **Alphecca–Polaris 4:5:9** (0.090%); **Procyon–Regulus φ** (0.015%; 0.111% / 0.064%); **Equator–Vega 3:5:8** (0.061%; 0.159% at 24:00, just out).
  - **POLARIS four times**: his Sun is 112.552 from Polaris in Dec and makes chords with Polaris and Betelgeuse, Altair, Capella and Alphecca. Vega twice (Castor–Vega, Equator–Vega).
- With his own bodies (Dec, held): **his Sun at the Dec midpoint of JUPITER and RAHU (1:1:2, 0.016%;** 5.188 / 5.187 / 10.376).
- RA chords (Aldebaran–Deneb Algedi 5:8:13 0.033%, Mars–Rahu 3:4:7 0.016%, Mercury–Rahu 1:2:3 0.038%, Chiron–Pluto 3:4:7 0.041%, Mars–Sedna) depend on the birth hour — only true if born near midday. Mars–Uranus Dec 3:4:7 0.006% also moves (Mars).
#### Mercury (RA 284.614, Dec −24.106; moves 0.6° in RA and 0.25° in Dec over the day — nothing holds the whole day)
- No chord held at both 00:00 and 24:00. Closest: Eris–Rahu Dec 1:6:7 (0.061% midday, 0.080% at 00:00, out by 24:00); Capella–Polaris Dec φ (0.144% midday, 0.038% at 24:00 — tighter late in the day).
- Tight at midday only (true if born near midday): **Equator–Pleiades Dec 1:1:2, 0.005%** — his Mercury is the Pleiades' mirror across the equator (24.106 south / Pleiades 24.107 north); **Arcturus–Polaris Dec φ 0.008%** (Polaris again); Makemake–Pluto RA 2:5:7 0.007%; Chiron–Transpluto Dec 2:5:7 0.009%; Haumea–Jupiter RA 5:6:11 0.012%; Jupiter–Vesta Dec 1:3:4 0.015%; Aldebaran–Fomalhaut RA √2 0.018%.
- Mercury–Rahu–Sun RA 1:2:3 (the same chord seen from the Sun).
#### Venus (RA 222.389, Dec −13.378; moves 0.5° in RA, 0.045° in Dec over the day)
- Nearly held all day: **Arcturus–Procyon Dec 3:4:7** (0.038% midday, 0.083% at 24:00, 0.159% at 00:00 — just out at midnight). Antares–Vega Dec 1:4:5 (0.094%, out at 00:00).
- Tight at midday: **a SPICA cluster in Dec** — Venus 2.218 from Spica: Rigel–Spica 3:4:7 (0.012%), Sirius–Spica 2:3:5 (0.014%), Algorab–Spica √2 (0.104%). Small bases, so they hold only a few hours around midday.
- With his own bodies: Ceres–Neptune Dec φ (0.019%), Quaoar–Uranus Dec 4:5:9 (0.030%), Orcus–Pallas Dec φ (0.032%).
- **The RAHU–SEDNA string (RA, base 65.295) now has all three fast bodies on it:** Sun 1:1:2 (Rahu at the midpoint of Sun and Sedna; 0.128%), Mercury 2:3:5 (0.116%), Venus φ (0.052%). Each one soft, but the same string three times. Rahu also with the Sun (Jupiter–Rahu Dec midpoint; Mars–Rahu, Mercury–Rahu RA).
#### Mars (RA 213.966, Dec −12.651; moves 0.6° in RA and 0.21° in Dec over the day — fast for Mars)
- Held all day: **Pallas–Sedna RA 1:2:3** (0.073% midday; 0.017% at 00:00, 0.122% at 24:00). His Pallas sits between Mars and Sedna, Mars two bases out from Pallas (119.644 / 179.422; base 59.778). SEDNA again.
- Tight at midday only: Sun–Uranus Dec 3:4:7 (0.006%); Gonggong–Juno Dec 3:5:8 (0.006%); Rahu–Sun RA 3:4:7 (0.016%, Rahu again); Alphecca–Arcturus Dec φ (0.019%); Juno–Orcus RA 3:5:8 (0.026%, nearly held: 0.297% / 0.245% at the ends); Antares–Pleiades Dec 3:8:11 (0.034%); Sedna–Sun RA 3:8:11 (0.048%); Jupiter–Sedna Dec φ (0.045%).
- **SEDNA now on every body so far:** Sun (Rahu–Sedna 1:1:2, Mars–Sedna, Mercury–Sedna), Mercury (Rahu–Sedna, Sedna–Sun, Pallas–Sedna Dec), Venus (Rahu–Sedna), Mars (Pallas–Sedna — held all day — Sedna–Sun, Jupiter–Sedna). Rahu with Sun, Mercury, Venus and Mars.
#### Jupiter (RA 232.560, Dec −18.096; moves 0.2° in RA, 0.05° in Dec — the first steady body)
- **Held all day, with the stars:** **Alkaid–Altair Dec 2:3:5, 0.004%** (0.097% / 0.087% at the ends); **Alphecca–Bellatrix Dec 5:6:11** (0.035%; 0.068% / 0.136%); Algol–Alkaid Sky φ (0.131%, loose). Nearly: Aldebaran–Algol Dec √2 (0.026% at 00:00, 0.171% at 24:00), Equator–Pleiades Dec 3:4:7 (0.054% at 00:00).
- **Held all day, with his own bodies:** **Haumea–Orcus Dec 1:3:4, 0.008%** (0.053% / 0.037% — steady all day); **Eris–Gonggong RA 5:8:13, 0.022%** (0.122% / 0.079%); **Ketu–Pluto RA 5:6:11, 0.024%** (0.037% / 0.112%). Nearly: Haumea–Pallas RA φ (0.032%; 0.185% at 24:00); Rahu–Sun Dec (Sun at the midpoint, 0.016%; 0.216% at 24:00).
- Outer bodies take over from here: Haumea twice, Orcus, Eris, Gonggong, Pluto, Ketu. Stars: Alkaid, Altair, Algol, Bellatrix, Alphecca.
#### Saturn (RA 45.331, Dec 14.602; hardly moves over the day)
- **Held all day:** **Spica–Vega RA φ** (0.068%; 0.049% / 0.098%); **Antares–Rigel Dec 4:5:9** (0.074%; 0.102% / 0.048%); **Pallas–Sedna RA 1:5:6** (0.109%; 0.100% / 0.122%) — **the Pallas–Sedna string a second time, both held all day: Mars 1:2:3 and Saturn 1:5:6.** Saturn sits near Sedna (11.943 from Sedna, 71.721 from Pallas).
- Nearly: Gonggong–Haumea Dec φ (0.053%; 0.178% at 00:00, 0.067% at 24:00); Alkaid–Castor Sky (loose).
- Midday only (the other body moves): **Ceres–Neptune Dec 2:3:5, 0.001%** — the same Ceres–Neptune string Venus played (φ, 0.019%); Haumea–Mercury Dec 1:4:5 (0.023%); Ceres–Sedna RA 2:3:5 (Sedna again).
- Saturn is quiet on the stars (5 chords); its weight is on Sedna and Haumea.
#### Ceres (RA 25.437, Dec 1.185; RA steady, Dec moves 0.08° over the day — near the equator, so its small Dec distances shift)
- **Held all day (RA):** **Pleiades–Sirius √2** (0.093%; 0.067% / 0.122%); **Betelgeuse–Regulus 1:1:2** (0.099%; Ceres one base beyond Betelgeuse, 63.361 / 126.660); **Bellatrix–Procyon 3:5:8** (0.110%; 0.124% / 0.093%).
- **Held all day, with his own bodies:** **Chiron–Haumea RA 1:7:8** (0.088%; 0.044% / 0.137%) — Haumea again; **Makemake–Pluto Sky 3:8:11** (0.110%). Nearly: Chiron–Juno RA 5:6:11 (0.192% at 00:00).
- Midday only (Ceres's Dec moves): **Neptune–Saturn Dec 2:3:5, 0.001%** and **Neptune–Venus Dec φ, 0.019%** — the Ceres–Neptune string from the other side (Saturn and Venus on it); Ketu–Uranus Dec 1:2:3 (0.015%); Pallas–Rahu Dec 1:2:3 (0.025%); Jupiter–Rahu RA 3:5:8 (0.040%); Saturn–Sedna RA 2:3:5.
#### Pallas (RA 333.610, Dec −8.211; moves 0.24° in RA, little in Dec)
- **Held all day:** **Castor–Rigel RA 1:3:4, 0.020%** (0.096% / 0.135%); **Gonggong–Pluto Dec 4:5:9** (0.059%; 0.031% / 0.144%); and **the Pallas–Sedna string from Pallas's side — Mars 1:2:3 (0.073%) and Saturn 1:5:6 (0.109%)**, both held all day.
- Nearly (in for part of the day): Algorab–Procyon Dec φ (0.029% at 00:00), Alphecca–Procyon Dec 5:8:13 (0.093% at 00:00), Antares–Bellatrix Dec 4:5:9 and Alkaid–Equator Dec 1:6:7 (in late in the day), Haumea–Jupiter RA φ (0.032%; 0.185% at 24:00); Polaris three times in RA at the same distance 64.625 (Polaris–Rigel 5:8:13 0.037%, Bellatrix–Polaris 2:3:5, Antares–Polaris 3:4:7) — midday only.
- Midday only: Chiron–Neptune RA 1:3:4 (0.015%); Ceres–Rahu Dec 1:2:3 (0.025%); Mercury–Sedna Dec φ (0.032%); Orcus–Venus Dec φ (0.032%); Eris–Quaoar RA 3:8:11 (0.040%).
#### Juno (RA 50.246, Dec −4.401; Dec moves 0.065° over the day)
- **Held all day:** only **Algol–Castor Dec 1:4:5** (0.027%; 0.114% / 0.066%).
- Nearly (in for part of the day): Capella–Fomalhaut Dec 1:2:3 (0.082%; 0.109% at 00:00), Gonggong–Makemake Dec 1:2:3 (0.063%; 0.132% at 00:00), Eris–Rahu RA 3:5:8 (0.060% at 24:00), Ceres–Chiron RA 5:6:11, Orcus–Transpluto Dec 1:7:8 (late), Aldebaran–Vega / Aldebaran–Altair RA, Arcturus–Polaris Flat (Polaris).
- Very tight at midday only: **Betelgeuse–Pleiades Dec √2, 0.001%**; **Fomalhaut–Procyon Dec φ, 0.004%** (the string of James Best's Gonggong stack at Exeter); Gonggong–Mars Dec 3:5:8 (0.006%); Chiron–Jupiter Dec 2:3:5 (0.017%); Mars–Orcus RA 3:5:8 (0.026%); Rahu–Sedna Dec √2 (0.094% — Rahu–Sedna again, in Dec this time).
- Eddie (09:40): Method 1 was originally distances and numbers, not chords → **option 2: for each body, the numbers first, then the chords**; go back over Sun–Juno for their numbers first. Script natnums.py (scratchpad): the body's RA/|Dec| and its RA, Dec, Flat, Sky distances to his other bodies (no Moon) and the stars at birth, against kφ, φⁿ, 10φⁿ, k√2, whole, ninths (±0.002°), with the time window over the birth day.
#### Numbers — Sun (182 values; chance ≈ 1.7 φ/√2/whole and ≈ 5.8 ninths at any one moment)
- None all day (the Sun moves too fast). At midday: Dec to ALPHECCA = 50 (11:57–13:53; Alphecca is also on his Sun's Alphecca–Polaris chord); Dec to Eris = 79/9 (11:33–13:23); RA to Alkaid = 56 and RA to Ceres = 1103/9 (minutes only); Sky to Quaoar 458/9, to Pallas 622/9 (minutes only). About chance.
#### Numbers — Mercury (182 values; chance ≈ 1.7 / 5.8)
- None all day. Around midday (minutes to an hour): RA to VENUS = 44√2 (11:40–12:31, the longest window); Dec to Spica = 8φ (11:57–12:20; Spica again — Venus's Dec cluster); Sky to Altair = 25√2; ninths: RA to Procyon 1528/9, Dec to Vega 566/9, Flat to Algorab 877/9, Flat to Deneb Algedi 386/9, Sky to Antares 303/9, Sky to Arcturus 732/9. 3 φ/√2 + 6 ninths — about chance; all depend on a birth near midday.
#### Numbers — Venus (182 values; chance ≈ 1.7 / 5.8)
- None all day. Around midday: **RA to SEDNA = whole 171** (11:54–12:05; Sedna again — Venus is on the Rahu–Sedna string); **Dec to CERES = 9φ** (11:31–12:16; Venus is on the Ceres–Neptune chord); RA to Mercury = 44√2 (the same pair as from Mercury); Flat to Pleiades = 120√2; ninths: RA to Pallas 1001/9, Dec to Aldebaran 269/9 (10:20–12:37, the longest window), Flat to Castor 1060/9, Flat to Haumea 580/9. 4 φ/√2/whole (a little above chance) + 4 ninths.
#### Numbers — Mars (182 values; chance ≈ 1.7 / 5.8)
- None all day. Around midday: **BELLATRIX twice** — RA = 82φ (11:58–12:06) and Dec = whole 19 (11:38–12:04); Dec to Fomalhaut = 12√2; ninths: Dec to Jupiter 49/9 (11:42–12:16), Dec to Orcus 237/9, Dec to Antares 124/9, Flat to Pleiades 1452/9, Flat to Antares 325/9, Flat to Algorab 241/9, Sky to Altair 773/9. 3 φ/√2/whole + 7 ninths — about chance.
#### Numbers — Jupiter (182 values; chance ≈ 1.7 / 5.8)
- None all day — at ±0.002° even Jupiter's distances (changing 0.05–0.2°/day) hold a number for 1–2 hours at most; an all-day number needs two slow points.
- Around midday: **ORCUS twice** — Dec = 286/9 (10:36–12:31) and Sky = 1109/9 (11:48–12:13); Orcus is on Jupiter's all-day chord Haumea–Orcus. **ANTARES twice** — Dec 75/9 (11:58–13:54), Sky whole 16. **BELLATRIX** Dec 220/9 (10:27–12:22) — Bellatrix again (Mars's two numbers; Jupiter's all-day Alphecca–Bellatrix chord). Dec to Mars 49/9 (same pair as from Mars); RA to Vega 420/9; Sky to Transpluto 895/9. 1 whole + 7 ninths — ninths a little above chance.
#### Numbers — Saturn (182 values; chance ≈ 1.7 / 5.8) — windows now run for hours
- **Dec to POLARIS = 672/9** (08:55–16:54, 8 h) — Polaris again (his Sun's four Polaris chords).
- **Dec to QUAOAR = 217/9** (09:22–22:10, 13 h — the longest so far).
- **ALPHECCA twice:** Dec = 109/9 (06:05–13:45), RA = 1545/9 (10:53–12:35) — with the Sun's Dec to Alphecca = 50.
- Dec to Algorab = 22√2 (11:49–19:48); Dec to Eris 262/9 (05:40–12:00); Flat to Ketu 925/9; Sky to Castor 577/9; Saturn's own RA = 408/9.
- 1 √2 + 8 ninths (ninths a little above chance). Mostly ninths, mostly in Dec.
#### Numbers — Ceres (182 values; chance ≈ 1.7 / 5.8)
- **BETELGEUSE twice:** Flat = 573/9 (04:46–18:16, 13½ h) and Dec = 56/9 (11:33–12:40) — Ceres is one base beyond Betelgeuse on its all-day Betelgeuse–Regulus 1:1:2 chord.
- RA to Alkaid = 1607/9 (07:29–14:27, 7 h); Dec to Sirius 161/9; Dec to Venus = 9φ (the same pair as from Venus); RA to Sun 1103/9 (minutes).
- 1 φ + 5 ninths — about chance.
#### Numbers — Pallas (182 values; chance ≈ 1.7 / 5.8)
- **Dec to BELLATRIX = 9φ** (09:51–17:22, 7½ h) — Bellatrix again (Mars RA 82φ and Dec 19; Jupiter Dec 220/9; Jupiter's all-day Alphecca–Bellatrix chord). 9φ also Ceres–Venus in Dec.
- **Dec to Procyon = 121/9** (07:53–15:15, 7½ h).
- **RA to SEDNA = 538/9** (11:53–12:15) — the base of his Pallas–Sedna string itself is a ninth around midday (Mars and Saturn hold all-day chords on it).
- RA to Deneb Algedi = φ⁴; RA to Venus 1001/9 (same as from Venus); Flat to Altair 358/9; Sky to Sun 622/9 (same as from the Sun).
- 2 φ + 5 ninths — about chance.
#### Numbers — Juno (182 values; chance ≈ 1.7 / 5.8)
- **Sky to CASTOR = 632/9** (06:38–17:59, 11 h) — Castor is on Juno's one all-day chord (Algol–Castor).
- **Dec to GONGGONG = whole 22** (10:46–12:22) — Juno's chords Gonggong–Mars and Gonggong–Makemake.
- **Dec to Algorab = 109/9** — the same number as Saturn's Dec to Alphecca (109/9): a repeated number in his chart.
- Sky to Capella = 40√2; Dec to Fomalhaut 227/9; Flat to Eris 292/9.
- 2 √2/whole + 4 ninths — about chance.
#### Numbers, first nine bodies pulled together
- About chance overall; what they add is agreement with the chord threads: **BELLATRIX** (Mars RA 82φ + Dec 19, Jupiter Dec 220/9, Pallas Dec 9φ; Jupiter's all-day Alphecca–Bellatrix chord), **ALPHECCA** (Sun Dec 50, Saturn Dec 109/9 + RA 1545/9), **POLARIS** (Saturn Dec 672/9, 8 h), **BETELGEUSE** (Ceres Flat 573/9 13½ h + Dec 56/9), **SEDNA** (Venus RA whole 171; Pallas–Sedna base = 538/9), **ORCUS** (Jupiter Dec + Sky), Castor (Juno), Quaoar (Saturn Dec 217/9, 13 h).
- Repeated numbers inside his chart (two different pairs): 9φ (Ceres–Venus Dec; Pallas–Bellatrix Dec), 109/9 (Saturn–Alphecca Dec; Juno–Algorab Dec).
#### Vesta (RA 238.793, Dec −16.092; moves 0.54° in RA and 0.12° in Dec over the day — fast for Vesta)
- **Numbers** (182 values; chance ≈ 1.7 / 5.8): none all day. Around midday: **Dec to KETU = whole 29** (11:40–12:17), RA to Chiron = whole 126 (minutes); 9 ninths (a little above chance), longest Sky to POLARIS 961/9 (11:47–12:35), Flat to Alphecca 388/9, Dec to Makemake 501/9, Dec to Rigel 71/9; Flat to Ketu, Gonggong, Uranus, Procyon, Sky to Haumea (minutes each).
- **Chords:** none held all day. Nearly: Aldebaran–Algol Dec 3:4:7 (0.024%; 0.160% / 0.205%) — the same string Jupiter nearly held (√2).
- Tight at midday: **Castor–Procyon Dec 4:5:9, 0.006%**; **Betelgeuse–Spica RA 1:3:4 and Sirius–Spica RA 3:8:11, both 0.007%** (Vesta 37.497 from Spica — Spica again, as with Venus and Mercury); Algorab–Antares RA 1:6:7 (0.013%); Gonggong–Neptune Dec φ (0.014%); Jupiter–Mercury Dec 1:3:4 (0.015%); Haumea–Mercury RA 2:3:5; Makemake–Pluto RA 3:4:7 (the Makemake–Pluto string again — Mercury 2:5:7, Ceres Sky 3:8:11).
#### Uranus (RA 192.628, Dec −4.676; steady)
- **Numbers** (182; chance ≈ 1.7 / 5.8): 5 ninths, no φ/√2/whole — chance. Flat to ALPHECCA = 465/9 (09:11–15:22, 6 h); Flat to GONGGONG = 1189/9 (10:42–15:05); Flat to Aldebaran 1129/9 (10:14–13:28); RA to Spica 78/9 (11:39–15:00); Flat to Vesta 428/9 (minutes).
- **Chords held all day:** **Alphecca–Antares RA 1:3:4, 0.010%** (0.025% / 0.045%); **Fomalhaut–Regulus Dec 2:3:5** (0.068%; 0.010% at 00:00); **Betelgeuse–Procyon Flat 1:3:4** (0.045%); Alphecca–Sirius Sky (0.011%, odd ratio set 9:16:24); Arcturus–POLARIS Sky 4:9:12 (0.075%). With his own bodies: **Gonggong–Haumea Dec 3:4:7** (0.050%; 0.122% / 0.020%) — the Gonggong–Haumea string Saturn nearly held (φ); **Haumea–Pluto RA 3:8:11** (0.049%; 0.141% / 0.044%). Nearly: Alkaid–Rigel RA 1:8:9, Antares–Vega Dec 1:2:3, Alphecca–Betelgeuse Dec 5:8:13.
- ALPHECCA again (chord, number, Alphecca–Sirius, nearly Alphecca–Betelgeuse); HAUMEA twice all day.
- Midday only: Mars–Sun Dec 3:4:7 (0.006%), Ceres–Ketu Dec 1:2:3 (0.015%), Quaoar–Venus Dec 4:5:9 (0.030%).
#### Neptune (RA 240.083, Dec −18.942; very steady)
- **Numbers** (182; chance ≈ 1.7 / 5.8): **ERIS twice** — Sky = 79φ (10:53–13:47) and RA = 1254/9 (11:00–13:23); Sky to Rahu = whole 84 (= Ketu 96 — one hit, the nodes are opposite) (11:47–12:30); RA to Rigel 1453/9 (11:48–14:26). About chance.
- **Chords held all day — 10, the most of any body so far:** Algorab–Procyon Sky 2:3:5 (0.014%); **Algol–Antares Dec 1:8:9 (0.019%)**; **Polaris–Regulus Dec 2:5:7 (0.041%)**; Capella–Vega Dec 1:8:9 (0.055%); Aldebaran–Betelgeuse Sky 1:7:8; **Capella–Polaris Dec 2:3:5 (0.068%) — the same string his Sun holds all day (5:8:13): two bodies on Capella–Polaris, both all day**; Procyon–Rigel Dec 4:5:9 (0.069%); Algol–Fomalhaut RA 3:5:8; Fomalhaut–Vega RA 3:5:8; Alkaid–Capella Sky 1:1:2 (Neptune one base beyond Alkaid).
  - POLARIS twice (with the Sun's four), CAPELLA three times, Procyon twice, Algol twice.
- With his own bodies (midday only — the others move): Ceres–Saturn Dec 2:3:5 (0.001%) and Ceres–Venus Dec φ (0.019%) — the Ceres–Neptune string again; Gonggong–Vesta Dec φ (0.014%); Chiron–Pallas RA 1:3:4 (0.015%).
#### Pluto (RA 186.483, Dec 14.541; very steady)
- **Numbers — the first ALL-DAY number: Sky to ALGOL = whole 113** (112.9989 at 00:00, 113.0004 midday, 113.0018 at 24:00). Long windows: **Dec to DENEB ALGEDI = 276/9** (00:56–22:14, 21 h); Sky to CAPELLA = 820/9 (06:32–24:00); Sky to CASTOR = 42φ (10:10–21:22).
- **Chords held all day (stars):** **Equator–Vega Dec 3:5:8** (0.030%) — the same chord his Sun makes on that string (3:5:8, 0.061%, in for most of the day): Sun and Pluto in UNISON on Equator–Vega; **Antares–Bellatrix Dec 1:4:5** (0.057%; Pallas 4:5:9 on it late in the day); **Arcturus–Procyon Dec 1:2:3** (0.064%; Venus 3:4:7 on it most of the day); **Polaris–Rigel RA 3:8:11** (0.088%; Pallas on it at midday); **Capella–POLARIS RA φ** (0.101%). Nearly: Procyon–Regulus Dec φ (the Sun's Procyon–Regulus φ, 0.015% — Sun and Pluto in UNISON there too around midday/early).
- **With his own bodies, all day:** Jupiter–Ketu RA 5:6:11 (0.024%); Haumea–Uranus RA 3:8:11 (0.049%); Gonggong–Pallas Dec 4:5:9 (0.059%); Ceres–Makemake Sky 3:8:11 (0.110%) — all four seen from the other side already. Nearly: Ketu–Sedna Flat 1:3:4 (0.036%; 0.185% / 0.166%).
- POLARIS twice more — all-day Polaris chords now 9 (Sun 4, Neptune 2, Pluto 2, Uranus 1 on Sky); Capella twice; Procyon twice.
#### Chiron (RA 4.791, Dec 4.730; almost stationary on his birth day — moves ~0.001°, so everything it makes holds all day)
- **Numbers all day:** **RA to ANTARES = 1057/9** and **Sky to SPICA = 1462/9** (both ALL DAY); long: Dec to Spica 143/9 (05:28–24:00); **Sky to ALGOL = 471/9** (08:16–24:00 — Algol again, after Pluto's all-day 113); **RA to POLARIS = 301/9** (05:27–14:13). Spica twice.
- **Chords held all day (stars), 15 of 16:** **Algol–Polaris Dec 3:4:7, 0.013%** (Algol and Polaris together); Arcturus–Vega Sky √2 (0.023%); **Altair–Antares RA 3:4:7 (0.025%)**; Deneb Algedi–Vega RA 4:5:9 (0.031%); Aldebaran–Vega RA 3:4:7 (0.032%); Altair–Regulus Dec 3:4:7 (0.050%); Arcturus–Regulus Dec 1:1:2 (Chiron one base beyond Arcturus, 0.073%); Altair–Arcturus Dec 2:5:7; Pleiades–Rigel Dec 2:3:5; Capella–Fomalhaut Dec 5:6:11; Aldebaran–Capella Dec 2:5:7; Algorab–Fomalhaut Dec φ; Altair–Arcturus RA 4:5:9; Altair–Betelgeuse Flat; Arcturus–Bellatrix Sky (odd set).
  - ALTAIR five times, ARCTURUS five, VEGA four.
- **With his own bodies, all day:** Eris–Gonggong Dec φ (0.051% — Eris–Gonggong again, Jupiter's RA string); Eris–Transpluto Dec 3:5:8; Ceres–Haumea RA 1:7:8 (Ceres's chord); Makemake–Orcus RA 1:3:4. Midday only: Mercury–Transpluto Dec 2:5:7 (0.009%), Neptune–Pallas RA 1:3:4 (0.015%), Juno–Jupiter Dec 2:3:5 (0.017%).
- Because Chiron barely moves, "held all day" is automatic for it; what stands out is the tight ones (Algol–Polaris, Altair–Antares) and the two all-day numbers.
#### Eris (RA 19.417, Dec −14.507; very steady)
- **Numbers — the most so far, many all or most of the day:** **Sky to FOMALHAUT = 22φ (ALL DAY)**; Eris's own RA = 12φ (01:57–24:00); RA to Alkaid = 122√2 (04:16–24:00); **RA to Regulus = 82φ** (00:00–13:12) — **the same 82φ as Mars's RA to Bellatrix**; **Dec to DENEB ALGEDI = φ** (00:00–20:55; Deneb Algedi again, after Pluto's 276/9); **Dec to ALPHECCA = 371/9** (00:00–22:15; Alphecca again); RA to Rigel 533/9 (00:00–15:49); Flat to Orcus 868/9 (11:56–18:39); with Neptune (79φ Sky, 1254/9 RA) and the Sun (79/9) around midday. 7 φ/√2 hits — well above chance (≈1.7).
- **Chords held all day, 8 of 9 (stars):** **Arcturus–Procyon Dec √2 (0.039%)** — **the Arcturus–Procyon string now has Pluto (1:2:3, all day), Eris (√2, all day) and Venus (3:4:7, most of the day)**; **Capella–Fomalhaut Dec 1:4:5** (0.071%; Chiron 5:6:11 on it all day too — two bodies); Aldebaran–Betelgeuse RA 2:5:7; Betelgeuse–Procyon RA 3:8:11 (Uranus on Betelgeuse–Procyon in Flat); Bellatrix–Vega RA φ; Altair–Fomalhaut RA 3:4:7; Aldebaran–Fomalhaut RA √2; Alkaid–Castor Dec 3:8:11.
- **With his own bodies, all day:** **Gonggong–Jupiter RA 5:8:13 (0.022%) and Chiron–Gonggong Dec φ (0.051%)** — the Eris–Gonggong pair carries Jupiter and Chiron; Chiron–Transpluto Dec 3:5:8; **Orcus–Sedna Dec 3:4:7** (0.101%; Sedna again). Nearly: Mercury–Rahu Dec 1:6:7, Ketu–Rahu Sky φ.
- FOMALHAUT five times (number + 4 chords), PROCYON twice.
#### Sedna (RA 33.389, Dec 1.609; stationary on his birth day)
- **Numbers:** **RA to ALDEBARAN = 22φ** (03:07–21:50) — **the same 22φ as Eris's all-day Sky to Fomalhaut**; Flat to Capella 574/9 (00:52–24:00); Dec to HAUMEA 204/9 (00:47–13:22); Flat to Sirius 633/9 (00:00–14:12); at midday Venus (whole 171), Pallas (538/9, the Pallas–Sedna base), Rahu (602/9).
- **Chords with the stars — all 12 hold all day:** **Capella–Spica RA 3:8:11, 0.006%** (0.011% / 0.000% — the tightest all-day star chord in his chart so far); **PROCYON three times tight:** Procyon–Rigel RA 4:5:9 (0.014%), Algorab–Procyon Dec 1:5:6 (0.015%), Betelgeuse–Procyon Dec 3:5:8 (0.046%); then Algol–Altair, Arcturus–Fomalhaut, Alphecca–Deneb Algedi √2, Altair–Bellatrix 1:2:3, Algorab–Altair, Capella–Deneb Algedi, Algol–Pleiades, Rigel–Sirius (0.09–0.14%).
- **With his own bodies — 20 chords, the most of any body:** all day: **Haumea–Orcus Flat 3:4:7, 0.010%** — the same pair Jupiter holds all day in Dec (1:3:4): **Haumea–Orcus links the Sedna group to the Haumea group**; Quaoar–Transpluto RA √2 (0.033%); Mars–Pallas RA 1:2:3 and Pallas–Saturn RA 1:5:6 (the Pallas–Sedna string); Orcus–Transpluto RA 1:3:4; Eris–Orcus Dec 3:4:7. Nearly: Ketu–Pluto Flat, Orcus–Rahu RA (0.032% at 00:00), Makemake–Rahu Dec (0.004% at 00:00), Rahu–Transpluto RA.
  - ORCUS five times with Sedna; RAHU seven times (Rahu–Sun, Rahu–Venus, Mercury–Rahu, Juno–Rahu, Makemake–Rahu, Orcus–Rahu, Rahu–Transpluto — mostly birth-hour).
#### Haumea (RA 170.088, Dec 24.277; very steady)
- **Numbers:** **RA to DENEB ALGEDI = 1410/9 (ALL DAY)** — Deneb Algedi a third time (Pluto Dec 276/9 for 21 h, Eris Dec φ for 21 h); **Flat to POLARIS = whole 147** (04:28–14:29); Dec to Sedna 204/9 (00:47–13:22, the same pair as from Sedna).
- **Chords held all day (stars):** Betelgeuse–Rigel RA 1:8:9 (0.029%); **Polaris–Rigel Dec 1:2:3 (0.054%)** — Polaris–Rigel also with Pluto (RA 3:8:11, all day) and Pallas (RA, midday); Alkaid–Spica Dec √2; Altair–Fomalhaut Dec 2:5:7; Alkaid–Procyon RA 2:3:5; **Spica–Vega RA 2:5:7 — Saturn holds Spica–Vega RA all day too (φ): two bodies**. Nearly: Castor–Regulus Dec φ, Castor–Procyon Dec 2:5:7, Arcturus–Castor Dec, Algol–Alkaid Dec 1:2:3, Altair–Procyon Dec φ.
- **With his own bodies, all day:** **Jupiter–Orcus Dec 1:3:4 (0.008%)**, **Gonggong–Quaoar Dec 1:2:3 (0.008%)**, **Orcus–Sedna Flat 3:4:7 (0.010%)**, Pluto–Uranus RA 3:8:11, Gonggong–Uranus Dec 3:4:7, Ceres–Chiron RA 1:7:8. Nearly: Gonggong–Saturn Dec φ, Jupiter–Pallas RA φ.
  - Haumea's partners: ORCUS (with Jupiter, Sedna, Mars), GONGGONG (with Quaoar, Uranus, Saturn), Uranus–Pluto, Ceres–Chiron. Three all-day chords at 0.008–0.010%.
#### Makemake (RA 147.233, Dec 39.573; very steady)
- **Numbers:** **Sky to ALPHECCA = 637/9 (ALL DAY, exact to 0.0000 at midday)**; Sky to Sirius = 50√2 (00:00–20:57); **Sky to POLARIS = 456/9** (10:53–19:37); Flat to Castor 310/9 (02:32–18:28); Flat to Altair 1382/9 (08:05–16:55); **Dec to BELLATRIX 299/9** (05:04–13:55); **ORCUS three numbers** (Dec 233/9 and 16φ at once, Sky 365/9); RA to Antares 901/9; Dec to Ketu 240/9.
- **Chords held all day (stars), 13 of 18:** **Aldebaran–Spica Dec 5:6:11 (0.011%)**; **Altair–Polaris Dec φ (0.018%) — the Sun holds Altair–Polaris all day too (2:5:7): two bodies**; Aldebaran–Fomalhaut Dec 1:2:3 (0.024%); **Algol–Fomalhaut RA 5:8:13 (0.039%) — Neptune holds it all day too (3:5:8)**; Alphecca–Procyon RA 3:8:11; Castor–Fomalhaut Dec 1:8:9; Betelgeuse–Sirius Dec 3:4:7; Aldebaran–Deneb Algedi Dec √2; Altair–Sirius Dec; Aldebaran–Procyon RA √2; **Antares–Rigel Dec φ — Saturn holds it all day too (4:5:9)**; Procyon–Spica RA. Nearly: Alphecca–Capella Dec 1:2:3 (0.016%), Aldebaran–Castor, Betelgeuse–Capella, Alphecca–Betelgeuse (Uranus nearly on it too).
  - ALDEBARAN six times (Makemake 23.062 from Aldebaran in Dec).
- **With his own bodies, all day:** Chiron–Orcus RA 1:3:4; Ceres–Pluto Sky 3:8:11 (Ceres's); Rahu–Transpluto Dec 4:5:9 (just in). Nearly: Rahu–Sedna Dec φ (0.004% at 00:00), Gonggong–Juno Dec. Midday only: Mercury–Pluto RA 2:5:7 (0.007%).
- Makemake leans to the STARS (18 chords, 3 strings shared all day with the Sun, Neptune and Saturn) more than to his own bodies.
#### Quaoar (RA 211.509, Dec −9.510; very steady)
- **Numbers:** **Dec to POLARIS = 889/9** (00:00–18:43, 19 h) — Polaris again; Dec to Saturn 217/9 (09:22–22:10, same pair as from Saturn); Flat to Alkaid = whole 59 (00:00–12:57); RA to Algorab = 17√2 (07:58–13:41); RA to Bellatrix 1172/9 (11:48–17:41); Flat to Sirius 994/9.
- **Chords held all day (stars), 10 of 12:** **Bellatrix–Capella Dec 2:5:7, 0.003%** (0.018% / 0.011%) — the tightest all-day star chord in his chart; **Antares–Betelgeuse Dec 1:1:2, 0.020%** (Quaoar at the Dec midpoint of Antares and Betelgeuse); **ALPHECCA five times:** Alphecca–Castor Dec 1:7:8 (0.021%), Alphecca–Fomalhaut RA 1:5:6 (0.035%), Alphecca–Rigel RA 1:6:7, Alphecca–Vega Dec 1:3:4, and Alphecca–Antares RA φ (nearly; **Uranus holds Alphecca–Antares RA all day**); Alkaid–Pleiades Dec 3:4:7; Pleiades–Procyon RA 3:5:8; **Castor–Vega Dec 1:6:7 — his Sun holds Castor–Vega all day (1:8:9): two bodies**; Regulus–Vega Dec 4:5:9.
- **With his own bodies, all day:** Gonggong–Haumea Dec 1:2:3 (0.008%); Sedna–Transpluto RA √2 (0.033%) — both seen from the other side. Chiron–Gonggong RA (just). Midday only: Uranus–Venus Dec 4:5:9, Eris–Pallas RA 3:8:11.
#### Orcus (RA 111.651, Dec 13.683; very steady)
- **Numbers — two ALL DAY:** **Dec to ALDEBARAN = 2√2 (2.8284, exact all day)** and **Dec to BELLATRIX = 66/9 (all day)** — Bellatrix again (Mars, Jupiter, Pallas, Makemake, Quaoar numbers). **Sky to POLARIS = 685/9** (00:00–12:46). With his own bodies: MAKEMAKE three (Dec 233/9 and 16φ, Sky 365/9), Jupiter two (Dec 286/9, Sky 1109/9), Rahu (Flat whole 146, RA 1292/9), Mars, Eris, Ketu; RA to Aldebaran 384/9, Regulus 364/9; Flat to Vega 1525/9.
- **Chords held all day (stars), 11 of 13:** Betelgeuse–Vega Dec 1:4:5 (0.017%); **Antares–Rigel Dec 5:6:11 (0.043%) — the Antares–Rigel string now carries THREE of his bodies all day: Saturn 4:5:9, Makemake φ, Orcus 5:6:11**; Deneb Algedi–Spica Dec 1:5:6; Alphecca–Pleiades Dec 1:4:5; **Algol–Pleiades Dec φ (Sedna 3:4:7 on it all day — two)**; Equator–Rigel Dec 3:5:8; Antares–Vega Dec 5:8:13; **Altair–Fomalhaut Dec 1:8:9 (Haumea 2:5:7 on it all day — two)**; Algorab–POLARIS Dec 2:5:7; Pleiades–Spica Flat; Alphecca–Spica Sky. Nearly: Bellatrix–Regulus RA 3:4:7, Algorab–Bellatrix RA.
- **With his own bodies, all day:** Haumea–Jupiter Dec 1:3:4 (0.008%), Haumea–Sedna Flat 3:4:7 (0.010%), Sedna–Transpluto RA 1:3:4, Eris–Sedna Dec 3:4:7, Chiron–Makemake RA 1:3:4. Nearly: Rahu–Sedna RA 5:6:11 (0.032% at 00:00). Midday only: Juno–Mars RA 3:5:8 (0.026%).
- Orcus is the link body: with Haumea, Jupiter, Sedna (three ways), Makemake, Eris, Chiron, Transpluto.
#### Gonggong (RA 322.941, Dec −26.402; very steady)
- **Numbers:** Dec to Algorab = 89/9 (07:02–24:00); Dec to Fomalhaut = 29/9 (07:22–24:00); **Dec to Transpluto = 384/9** (00:00–17:28) — **the same 384/9 as Orcus's RA to Aldebaran** (a repeated number); Dec to Juno whole 22 (same pair as from Juno); Rahu (Flat 130/9, Sky 129/9 around midday); Flat to Uranus 1189/9 (10:42–15:05).
- **Chords with the stars — only 4, all held all day:** Algol–Capella RA φ (0.017%); Aldebaran–Equator Dec 5:8:13; Bellatrix–Rigel Dec 4:5:9; **Algol–Pleiades Dec 1:3:4 — the Algol–Pleiades string now carries THREE of his bodies all day: Sedna 3:4:7, Orcus φ, Gonggong 1:3:4** (the second three-body string, after Antares–Rigel).
- **With his own bodies, all day (all seen from the other side):** Haumea–Quaoar Dec 1:2:3 (0.008%), Eris–Jupiter RA 5:8:13 (0.022%), Haumea–Uranus Dec 3:4:7, Chiron–Eris Dec φ, Pallas–Pluto Dec 4:5:9. Nearly: Haumea–Saturn Dec φ, Juno–Makemake Dec 1:2:3. Midday only: Juno–Mars Dec 3:5:8 (0.006%), Neptune–Vesta Dec φ.
- Gonggong works through his own bodies (Haumea, Eris, Jupiter, Quaoar, Uranus, Chiron) more than the stars.
#### Transpluto (RA 137.715, Dec 16.263; very steady)
- **Numbers:** **RA to ALGOL = 816/9** (03:02–19:01) — Algol again (Pluto 113 all day, Chiron 471/9); **Flat to DENEB ALGEDI = whole 174** (06:28–23:48) — Deneb Algedi a fourth time; Sky to PROCYON = whole 25 (00:00–12:41); Sky to Capella 510/9 (00:00–13:54); Dec to Gonggong 384/9 (the repeated 384/9).
- **Chords with the stars — all 12 hold all day, several very tight:** **Bellatrix–Capella Dec 1:3:4, 0.002% — Quaoar holds the same string all day at 0.003% (2:5:7): the two tightest all-day chords in his chart on ONE string**; **Algorab–Fomalhaut Dec 2:5:7, 0.005%** (Chiron φ on it all day — two); Betelgeuse–Deneb Algedi Flat 2:5:7 (0.010%); Alkaid–Betelgeuse RA √2 (0.016%); **Algorab–POLARIS RA 1:2:3 (0.024%)**; Capella–Fomalhaut RA φ; Alphecca–Altair RA 2:3:5 and Dec √2; Alkaid–Rigel Flat; Altair–Equator Dec; Algol–Sirius Dec; Alkaid–Procyon Dec.
- **With his own bodies, all day:** Quaoar–Sedna RA √2 (0.033%), Chiron–Eris Dec 3:5:8, Orcus–Sedna RA 1:3:4, Makemake–Rahu Dec 4:5:9 (just). Nearly: Rahu–Sedna RA 5:8:13 (0.063% at 00:00), Juno–Orcus Dec. Midday only: Chiron–Mercury Dec 2:5:7 (0.009%).
#### The nodes — Rahu (RA 328.094, Dec −12.908) / Ketu (RA 148.094, Dec +12.908); the true node moves ~0.1° in RA and 0.03° in Dec over the day
- **Rahu numbers:** all around midday (Orcus RA 1292/9 and Flat whole 146, Transpluto, Gonggong, Sedna 602/9, Makemake, Neptune 84, Aldebaran). **Rahu star chords:** one held all day — **Algol–Rigel RA 2:5:7** (0.032%; Algol again); the rest drift in or out (Antares–Fomalhaut Dec φ 0.012% at midday; Arcturus–Bellatrix, Pleiades–Sirius, Alkaid–Regulus, Castor–Regulus come in later in the day).
- **Rahu with his own bodies — 19 chords, mostly with the fast bodies (birth-hour):** Jupiter–Sun Dec midpoint (0.016%), Mars–Sun, Mercury–Sun, Ceres–Pallas, Ceres–Jupiter; **SEDNA eight times** (Sedna–Venus, Juno–Sedna, Makemake–Sedna, Mercury–Sedna, Orcus–Sedna, Sedna–Sun, Sedna–Transpluto, and the Rahu–Sedna string itself) — none quite all day.
- **Ketu numbers:** **Dec to DENEB ALGEDI = φ⁷** (10:42–13:35); Rigel 190/9; Makemake 240/9; Saturn Flat 925/9; around midday Vesta (whole 29), Neptune 96, Regulus, Aldebaran.
- **Ketu star chords:** **Antares–DENEB ALGEDI RA 4:5:9, 0.010%, held all day** (0.063% / 0.033%); also Deneb Algedi–Equator Dec 4:5:9 (0.057%, in most of the day) and Deneb Algedi–Rigel Dec 3:8:11 (later in the day) — **KETU WITH DENEB ALGEDI three chords + a φ⁷ number: the Pholas lead (Deneb Algedi with Ketu) is in Dettori's own chart.** Others: Procyon–Spica RA 5:8:13 (0.019%), Antares–Bellatrix Dec 1:5:6 (0.030%; Pluto and Pallas on it too), Alphecca–Castor Dec, Fomalhaut–Sirius RA, Capella–Castor RA 1:1:2, Arcturus–Polaris RA.
- **Ketu with his own bodies, all day:** Jupiter–Pluto RA 5:6:11 (0.024%). Nearly: Pluto–Sedna Flat 1:3:4, Eris–Rahu Sky φ.
### METHOD 1 SUMMARY — Frankie Dettori's chart (born 15 Dec 1970; no birth time, so "all day" = holds from 00:00 to 24:00)
Tally across all 24 bodies (natchords all-day chords; scratchpad dett/):
- **Fast bodies (Sun, Mercury, Venus, Mars, Juno, Vesta) give birth-hour chords only**, except the Sun's Dec chords. The firm chart is the slow bodies.
- **CORRECTION to the running notes:** counted properly, POLARIS is not the most-used star. All-day star chords per star: Procyon 18, Fomalhaut 18, Altair 18, Alphecca 17, Rigel 16, Vega 15, Capella 15, Betelgeuse 15, Polaris 14, Algol 13, Antares 12, Aldebaran 11 (Chiron and Sedna, being stationary, add to every star they touch). The stars are spread fairly evenly; Polaris stood out on the Sun, not overall.
- **Strings held all day by 2–3 of his bodies (stars):**
  - three bodies: **Antares–Rigel Dec** (Saturn 4:5:9, Makemake φ, Orcus 5:6:11); **Algol–Pleiades Dec** (Sedna 3:4:7, Orcus φ, Gonggong 1:3:4)
  - two bodies: **Bellatrix–Capella Dec (Transpluto 0.002%, Quaoar 0.003% — the tightest in the chart)**; Arcturus–Procyon Dec (Pluto, Eris; Venus most of the day); Capella–Fomalhaut Dec (Eris, Chiron); Algorab–Fomalhaut Dec (Transpluto 0.005%, Chiron); Castor–Vega Dec (Sun, Quaoar); Altair–Polaris Dec (Sun, Makemake); Capella–Polaris Dec (Sun, Neptune); Algol–Fomalhaut RA (Makemake, Neptune); Alphecca–Antares RA (Uranus 0.010%, Quaoar); Pleiades–Sirius RA (Ceres, Rahu); Spica–Vega RA (Saturn, Haumea); Altair–Fomalhaut Dec (Haumea, Orcus).
- **His own bodies — all-day triads (19).** Tightest: Gonggong–Haumea–Quaoar Dec 1:2:3 (0.008%), Haumea–Jupiter–Orcus Dec 1:3:4 (0.008%), Haumea–Orcus–Sedna Flat 3:4:7 (0.010%), Eris–Gonggong–Jupiter RA 5:8:13 (0.022%), Jupiter–Ketu–Pluto RA 5:6:11 (0.024%), Quaoar–Sedna–Transpluto RA √2 (0.033%). Also Mars–Pallas–Sedna and Pallas–Saturn–Sedna (the Pallas–Sedna string).
  - **Hubs:** HAUMEA, ORCUS and SEDNA (6 triads each), then GONGGONG and CHIRON (5), Eris, Pluto, Transpluto (4). Orcus sits between the Haumea group (Jupiter, Gonggong, Quaoar, Uranus) and the Sedna group (Pallas, Mars, Saturn, Transpluto, Eris).
- **Numbers:** about chance overall, but those that hold all or most of the day: Pluto–Algol Sky 113 (all day); Chiron–Antares RA 1057/9 and Chiron–Spica Sky 1462/9 (all day); Eris–Fomalhaut Sky 22φ (all day); Haumea–Deneb Algedi RA 1410/9 (all day); Makemake–Alphecca Sky 637/9 (all day); Orcus–Aldebaran Dec 2√2 and Orcus–Bellatrix Dec 66/9 (all day). Repeated: 22φ (Eris–Fomalhaut, Sedna–Aldebaran), 82φ (Mars–Bellatrix, Eris–Regulus), 384/9 (Orcus–Aldebaran, Gonggong–Transpluto), 9φ, 109/9. Stars carrying numbers on several bodies: Bellatrix (6 bodies), Alphecca, Deneb Algedi (Pluto, Eris, Haumea, Transpluto, Ketu φ⁷), Algol (Pluto, Chiron, Transpluto), Polaris.
- **Ketu with Deneb Algedi** (Antares–Deneb Algedi RA 0.010% all day; Deneb Algedi–Equator and –Rigel; φ⁷) — the Pholas lead in his own chart.
- **Rahu–Sedna**: on the Sun, Mercury, Venus, Juno, Makemake, Orcus, Transpluto — always near, never quite all day.
- Next: Method 3 — which of these strings the sky plays on 28 Sep 1996 (the slow sky holding his chords all day), then Method 2 around 14:36.
### METHOD 3 — the race-day sky on Dettori's chart (Ascot 28 Sep 1996; Diadem off 14:36:00, finish 14:37:15)
- **Fix (7 Oct):** the 1996 sky/position files carried the stars as "Algol_B" etc., so the star layer was missing (first Sun run showed no chords). Renamed to plain names (duplicates of Aldebaran/Antares/Regulus/Fomalhaut dropped — identical values), POS files trimmed to the usual layout, tuned layers re-run. Method 1 (natal) was unaffected (read from NATAL_HOURLY).
#### Sun (RA 185.273, Dec −2.284)
- **Two Sun chords come exact in the 90 s before the off, both on Dettori's ALL-DAY natal strings:**
  - **Alphecca–Altair Dec, exact 14:34:39 (81 s before the off)** — Dettori's TRANSPLUTO (√2, all day), the ONLY chart tuned to it.
  - **Castor–Fomalhaut Dec 4:5:9, exact 14:35:06 (54 s before the off)** — Dettori's MAKEMAKE (1:8:9, 0.048%, all day) tightest; Diffident's Eris 2nd.
  - Then Polaris–Sirius RA 3:4:7 exact 14:42:07 (5 min after the finish) — no chart.
- **Through the day the Sun plays Dettori's all-day strings again and again** (exact times): Procyon–Spica 01:19 (Makemake); Alkaid–Procyon 04:29 (Transpluto); **Antares–Rigel 04:31 (his three-body string: Orcus 5:6:11, Saturn, Makemake)**; Alphecca–Capella 09:18 (Makemake 0.016%); Altair–Equator 10:30 (Transpluto); Arcturus–Vega Sky 10:40 (Chiron 0.023%); Betelgeuse–Sirius 11:50 (Makemake); Alphecca–Betelgeuse 12:15 (Makemake); Antares–Betelgeuse 13:07 (Quaoar at the midpoint, 0.020%); Alphecca–Altair 14:34 (Transpluto); Castor–Fomalhaut 14:35 (Makemake); Algol–Sirius 15:15 (Transpluto); Aldebaran–Equator 19:11 and Bellatrix–Rigel 20:26 (Gonggong).
  - **MAKEMAKE five times and TRANSPLUTO four times** through the day.
- Diffident on the Sun: Mercury 0.003% on Arcturus–Capella (exact 13:07), Haumea in UNISON on Alkaid–Regulus φ (exact 15:22), Uranus on Rigel–Spica.
- No slow parallel; number check: no hits.
- Caution: the Sun makes ~120 exact star chords a day and his chart has many strings, so day-long matches are expected; what stands out is the two exact in the 90 s before the off, both on all-day natal strings, one with only Dettori on it.
#### Mercury (RA 170.308, Dec 4.486; m3.sh + dmatch.py in scratchpad)
- **Castor–Rigel RA φ, exact 14:00:00 (36 min before the off — the scheduled time of the first of his seven, Wall Street, 2:00): Dettori's PALLAS 1:3:4 tightest (0.020%, his all-day chord)**; Diffident's Eris in UNISON (φ). Sky 0.017% at the off.
- **Algorab–Fomalhaut Dec 5:8:13 (exact 09:37): Dettori's TRANSPLUTO tightest (0.005%, all day), Diffident's RAHU 2nd (0.008%), Dettori's Chiron 3rd** — horse and jockey together; Transpluto again (after the Sun's Alphecca–Altair before the off).
- **Deneb Algedi–Rigel Dec 5:8:13, exact 14:25:12 (11 min before the off): only Dettori's KETU** (3:8:11) — Ketu with Deneb Algedi again.
- Antares–Deneb Algedi Dec 1:2:3, exact 14:47:26 (10 min after the finish): Diffident's Uranus UNISON, Dettori's Jupiter.
- Altair–Regulus Dec √2 (exact 15:26): Dettori's Chiron (all day). Arcturus–Vega RA: Dettori's Pallas, Sun, Jupiter.
- Through the day on his all-day strings: Spica–Vega RA 02:40 (Saturn + Haumea, his two-body string), Altair–Equator 05:00 (Transpluto), Castor–Regulus 17:12 (Haumea), Betelgeuse–Procyon 17:30 and Arcturus–Fomalhaut 20:55 (Sedna), Aldebaran–Equator 17:54 and Bellatrix–Rigel 23:37 (Gonggong).
- Number check: 4 hits (Dec to Algorab whole 21, Dec to course latitude 29φ, Dec to Polaris 763/9, RA to Fomalhaut 1567/9) vs 0.44 + 1.5. No parallel.
#### Venus (RA 145.941, Dec 13.565; Dec falling 0.31°/day)
- **★ Venus crossed Dettori's natal ORCUS Dec (13.683) at about 05:30 on race day** — a slow-ish parallel that morning: Orcus (his link hub) then makes Venus's chord in UNISON on every Dec string Venus plays. Seen in the day list as Venus making Orcus's own chord types between 03:30 and 07:45: Algorab–Polaris 2:5:7 (03:34), Antares–Vega 5:8:13 (03:55), **Betelgeuse–Vega 1:4:5 (05:23, his Orcus 0.017%)**, Altair–Fomalhaut 1:8:9 (05:33), **Antares–Rigel 5:6:11 (05:38 — his three-body string)**, Deneb Algedi–Spica 1:5:6 (06:16), Equator–Rigel 3:5:8 (06:55), Alphecca–Pleiades 1:4:5 (07:43).
- **Algol–Pleiades Dec 5:8:13, exact 13:49 (46 min before the off) — his other three-body string: only Dettori's ORCUS, GONGGONG, SEDNA tuned** (no Diffident).
- Capella–Polaris Dec 3:4:7 (exact 15:54) — his Sun + Neptune string (Diffident's Saturn tightest, 0.013%). Capella–Fomalhaut Dec (exact 12:44) — his Eris + Chiron string. Polaris–Rigel RA (exact 13:06) — his Pallas (0.037%) and Pluto.
- Fomalhaut–Sirius RA φ, exact 14:18 (18 min before the off): **Diffident's Sun 0.004% tightest, his Transpluto 2nd** (Dettori's Ketu 4th).
- Through the day on his all-day strings: Algol–Castor 00:09 (Juno), Capella–Spica RA 11:16 (Sedna 0.006% — his tightest all-day star chord), Arcturus–Procyon 11:37 (Pluto + Eris), Procyon–Regulus 14:56 (Sun φ, UNISON), Castor–Vega 20:38 (Sun + Quaoar), Spica–Vega 19:41 (Saturn + Haumea), and more.
- Number check: 1 ninth (Dec to Vega 227/9). No parallel at the off.
#### Mars (RA 134.389, Dec 18.439)
- **Bellatrix–Regulus RA 1:3:4, exact 14:34:12 (108 s before the off; 0.008% at the off): only Dettori's ORCUS tuned** (3:4:7, his all-day chord) — Orcus, his hub, in the minute and a half before the off, alongside the Sun's two (Transpluto 14:34:39, Makemake 14:35:06). Mars also on Algorab–Bellatrix RA 1:1:2 (exact 13:58) with his Orcus.
- **STACK — Algorab–Fomalhaut Dec: Mercury 5:8:13 (exact 09:37) + Mars 3:8:11 (exact 14:10:48, 25 min before the off) → Dettori's TRANSPLUTO tightest on both (0.005%), Diffident's RAHU 2nd on both (0.008%)** — horse and jockey together; his Chiron 3rd. Transpluto now struck by the Sun, Mercury and Mars.
- Algorab–Regulus RA 1:2:3 (exact 15:08): **SAME BODY for both** — Diffident's Mars (2:5:7, tightest) and Dettori's Mars (3:4:7).
- Rigel–Spica RA 5:6:11 exact 14:37:48 — 33 s after the finish (no chart tuned).
- Alphecca–Castor Dec (exact 13:13): his Quaoar (0.021%, all day) and Ketu; Alphecca–Betelgeuse Dec (exact 13:58): his Makemake.
- Through the day: Betelgeuse–Deneb Algedi Flat 01:27 (Transpluto 0.010%), Altair–Fomalhaut 06:12 (Haumea + Orcus), Algol–Antares 06:22 (Neptune 0.019%), **Algol–Pleiades 06:55 (his three-body string, again)**, Alkaid–Betelgeuse 07:38 (Transpluto 0.016%), Aldebaran–Castor 15:31 (Makemake), Polaris–Rigel 23:19 (Haumea).
- Number check: 1 ninth (Dec to Pleiades 51/9). No parallel.
#### Jupiter (RA 279.637, Dec −23.367; slow — nothing exact on the day, all held)
- **★ SLOW PARALLEL: sky Jupiter sits 0.083° from Dettori's natal SUN Dec** — his Sun in UNISON on Jupiter's Dec chords, and they are **his Sun's own all-day chords**: Castor–Vega 1:8:9 (UNISON 0.032%), Procyon–Regulus φ (UNISON 0.015%), Alphecca–POLARIS 4:5:9 (UNISON 0.090%). Jupiter replays his natal Sun's star chords.
- **Bellatrix–Capella Dec 3:4:7 (0.052%): Dettori's TRANSPLUTO 0.002% and QUAOAR 0.003% are 1st and 2nd** — his tightest string, held by sky Jupiter; Diffident's Transpluto 3rd (0.030%).
- **Algol–POLARIS Dec 3:4:7: his CHIRON in UNISON, 0.013%** (Chiron's tightest all-day star chord).
- Castor–Vega is also his Sun + Quaoar two-body string; Aldebaran–Equator √2: his Gonggong (all day); Sirius–Spica: his Venus (0.014%), Diffident's Pluto and Chiron.
- Number check: 3 hits vs 0.44 + 1.5 — Dec to Algorab = φ⁴ (6.8537), RA to Rigel = whole 159, Dec to Arcturus 383/9.
#### Saturn (RA 4.593, Dec −0.863) — quiet
- 6 star chords; only one touches Dettori: Algol–Alkaid Dec 1:5:6 (exact 03:53) — **Diffident's Eris tightest (0.021%)**, Dettori's Haumea loose (0.133%). Betelgeuse–Polaris RA (exact 02:12): Diffident's Ketu and Haumea. Late: Procyon–Rigel Dec 23:46 (Dettori's Neptune, all day).
- No number hits, no parallel. Saturn leans to the horse, lightly.
#### Ceres (RA 252.843, Dec −24.735)
- **Dettori's MAKEMAKE on three Ceres strings, each also played by another sky body that day — STACKS on Makemake:**
  - **Alphecca–Betelgeuse Dec: Sun 1:2:3 (exact 12:15) + Mars 3:4:7 (exact 13:58) + Ceres 3:5:8** → his Makemake (2:3:5, all day) — three sky bodies.
  - **Alphecca–Capella Dec: Sun 2:3:5 (exact 09:18) + Ceres 3:8:11** → his Makemake tightest (1:2:3, 0.016%, all day).
  - **Betelgeuse–Capella Dec: Mars 2:5:7 (exact 15:21) + Ceres 5:6:11 (exact 19:38)** → his Makemake (1:5:6). Also Betelgeuse–Sirius: Sun (11:50) + Ceres (21:03) → Makemake.
- **Algorab–Fomalhaut Dec: Ceres 3:5:8 (exact 02:45) joins Mercury (09:37) and Mars (14:10)** → his TRANSPLUTO (0.005%) — three sky bodies on his Transpluto's string through the day (Diffident's Rahu 2nd on Mercury's and Mars's).
- Antares–Spica Dec 1:8:9, exact 14:28:48 (7 min before the off): only Dettori's Jupiter (loose, 0.148%).
- Through the day: Alphecca–Antares RA 12:57 (his Uranus 0.010% + Quaoar), Alkaid–Procyon RA 19:11 (Haumea), Altair–Antares RA 22:06 (Chiron 0.025%). Diffident: Pallas on Castor–Regulus RA (0.030%), Sedna on Algorab–Rigel.
- Number check: 3 hits — RA to Betelgeuse = 116√2, Dec to Algorab 74/9, RA to Sirius 1364/9. No parallel.
#### Pallas (RA 233.293, Dec 9.286) — quiet for Dettori, leans to Diffident
- At the off only loose: Aldebaran–Alphecca Dec √2 (exact 13:31) — Dettori's Ceres (0.148%).
- **Diffident:** his KETU in UNISON on Capella–Castor Dec 5:8:13 (0.031%, exact 09:24); his Haumea tightest on Regulus–Sirius RA (0.025%).
- Through the day on Dettori's all-day strings: Fomalhaut–Vega RA 03:40 (Neptune), Altair–Regulus 09:28, Arcturus–Bellatrix Sky 09:46 and Arcturus–Regulus 19:11 (CHIRON three times), Procyon–Regulus 17:14 (Sun φ), Bellatrix–Rigel 19:16 (Gonggong), Alphecca–Bellatrix 19:22 (Jupiter 0.035%).
- Number check: 4 hits vs 0.44 + 1.5 — RA to Spica = whole 32 (31.9998), Dec to Arcturus = 7√2, Dec to Aldebaran 65/9, Dec to Spica 184/9. No parallel.
#### Juno (RA 15.735, Dec −2.331 — almost the Sun's Dec, −2.284)
- **Juno sits within 0.05° of the Sun's Dec, so it plays the SAME Dec strings as the Sun that day** — the stacks on Dettori's Makemake and Transpluto grow:
  - **Alphecca–Betelgeuse Dec → his MAKEMAKE: Sun (12:15) + Mars (13:58) + Ceres + Juno (05:39) — four sky bodies.**
  - Alphecca–Capella Dec → Makemake (0.016%): Sun (09:18) + Ceres + Juno (00:37) — three.
  - Betelgeuse–Sirius Dec → Makemake: Sun (11:50) + Ceres (21:03) + Juno (04:56) — three.
  - **Castor–Fomalhaut Dec → Makemake: Sun (exact 54 s before the off) + Juno (09:37).**
  - **Alphecca–Altair Dec → his TRANSPLUTO: Sun (exact 81 s before the off) + Juno (09:37).** Algol–Sirius → Transpluto: Sun (15:15) + Juno (10:47).
  - Antares–Betelgeuse → Quaoar (midpoint, 0.020%): Sun (13:07) + Juno (07:07).
- **Algol–Fomalhaut RA 1:1:2 (Juno at the midpoint; 0.013% at the off, exact 14:57): Dettori's MAKEMAKE tightest (0.039%) and NEPTUNE 2nd — his two-body all-day string**; Diffident's Makemake 3rd.
- Algol–Betelgeuse RA 3:4:7, exact 14:03 (32 min before the off): Dettori's Mars tightest, Diffident's Sun 2nd. Pleiades–Procyon Dec: Diffident's Pluto, Rahu, Venus.
- Number check: 1 hit (Dec to course latitude = 38√2). No parallel.
- Eddie asked (12:50): "is that Juno and Jupiter on the Sun?" — Two different Suns: **Jupiter sits on Dettori's NATAL Sun Dec** (sky Jupiter −23.367 / his natal Sun −23.284); **Juno sits on the race-day SKY Sun's Dec** (−2.331 / −2.284), so Juno shadows the transiting Sun and plays its strings. (Mercury's Castor–Rigel exact time re-checked minute by minute: ≈13:59–14:00, genuine; slow bodies' exact minutes are arithmetic.)
#### Vesta (RA 248.629, Dec −20.947)
- **★ SLOW PARALLEL on the HORSE: sky Vesta sits 0.065° from Diffident's natal SUN Dec** — his Sun in UNISON on Vesta's Dec chords (Alkaid–Arcturus 3:4:7, 0.075%). The mirror of Jupiter on Dettori's natal Sun: **Jupiter on the jockey's Sun, Vesta on the horse's Sun**.
- Antares–Regulus Dec 1:6:7, exact 14:23 (13 min before the off): Diffident's Makemake (3:5:8, 0.081%), the only chart.
- Altair–Arcturus RA √2 (exact ≈14:00): Dettori's Chiron (all day, loose 0.136%).
- Through the day: Alphecca–Procyon RA 09:12 (his Makemake 0.048%, all day), Antares–Bellatrix 19:22 (Pluto), Altair–Sirius 20:57 (Makemake). Makemake again.
- Number check: 3 hits — Dec to Sirius = φ³, Dec to Alphecca 429/9, RA to Polaris 1347/9.
#### Uranus (RA 303.091, Dec −20.577; slow, nothing exact on the day)
- Leans to DIFFIDENT: **Antares–Arcturus RA 3:5:8 (0.023%, applying): his RAHU tightest (1:1:2, at the midpoint, 0.016%), his VENUS 2nd (0.021%), his Makemake 3rd** — three horse bodies, no Dettori.
- Dettori: his MARS in UNISON on Alphecca–Procyon Dec 5:6:11 (0.091%), with his Pallas.
- Number check: 1 ninth (RA to Castor 1535/9). No parallel. (We only have the winners' charts here, so the Uranus-on-the-favourite watch can't be checked in this race.)
#### Neptune (RA 296.894, Dec −20.670) — nothing for Dettori; SAME BODY for the horse
- No Dettori chart on any Neptune chord.
- **Diffident's natal NEPTUNE on two Neptune strings (same body):** Regulus–Rigel Dec φ (his 2:3:5, 0.017%) and Algorab–Rigel Dec 1:2:3 (his φ, 0.093%; exact 20:18). Also his Gonggong (Bellatrix–Vega) and Jupiter (Alkaid–Pleiades).
- Number check: 1 ninth (Dec to Capella 600/9). No parallel.
#### Pluto (RA 241.495, Dec −8.011; slow)
- Pluto holds three of Dettori's all-day strings that faster bodies also played that day:
  - **Betelgeuse–Capella Dec → his MAKEMAKE: Mars (15:21) + Ceres (19:38) + Pluto** — three sky bodies.
  - **Capella–Fomalhaut Dec → his ERIS + CHIRON (two-body string): Venus (12:44) + Pluto** (Diffident's Pallas tightest, 0.048%).
  - **Capella–Polaris Dec → his SUN + NEPTUNE (two-body string): Venus (15:54) + Pluto** (Diffident's Saturn tightest, 0.013%).
  - Alphecca–Antares RA (exact 05:07) → his URANUS (0.010%) + Quaoar: Ceres (12:57) + Pluto.
- Betelgeuse–Regulus RA √2: his CERES (1:1:2, all day — Ceres one base beyond Betelgeuse).
- Aldebaran–Bellatrix Dec √2 (exact 23:25): his Mercury. Algol–Arcturus Dec: Diffident's Makemake.
- CAPELLA in four of Pluto's chords. No number hits, no parallel.
#### Chiron (RA 196.383, Dec −8.113; slow)
- More stacks on Dettori's all-day strings:
  - **Bellatrix–Regulus RA → his ORCUS: Mars (exact 14:34:12, 108 s before the off) + Chiron 5:8:13.**
  - **Aldebaran–Castor Dec → his MAKEMAKE (1:2:3, 0.040%, tightest): Mars (15:31) + Chiron 5:8:13.** Also Aldebaran–Spica Dec (his Makemake 0.011%) held by Chiron.
  - **Capella–Polaris Dec → his SUN + NEPTUNE: Venus (15:54) + Pluto + Chiron — three sky bodies** (Diffident's Saturn tightest, 0.013%).
- **Castor–Procyon Dec 1:2:3: Dettori's VESTA tightest (0.006%), Diffident's VENUS 2nd (0.019%), Dettori's Haumea 3rd** — horse and jockey together.
- Diffident: KETU 0.007% tightest on Aldebaran–Alkaid Dec (with his Chiron 2nd — same body); Neptune on Fomalhaut–Sirius (0.018%); Orcus on Antares–Procyon (0.020%).
- Loose parallel: Chiron 0.099° from Dettori's natal Pallas Dec. Number check: Dec to Castor = whole 40 (40.0003); Chiron's |Dec| 73/9.
#### Eris (RA 23.371, Dec −7.844; slow)
- **Algol–Rigel RA 3:4:7: Dettori's RAHU tightest (0.032%, his one all-day Rahu chord) and Diffident's RAHU too — same body for both.**
- **SAME BODY: Altair–Fomalhaut RA 5:6:11 — Dettori's natal ERIS 3:4:7 (all day)**; Diffident's Uranus tightest (0.002%).
- Dettori's JUNO tightest on Fomalhaut–Procyon Dec (0.004%, the only chart); his SEDNA on Betelgeuse–Procyon Dec (0.046%, all day); his ORCUS on Deneb Algedi–Spica Dec (all day; Diffident's Vesta tightest, 0.009%); Chiron + Saturn on Altair–Arcturus.
- **Horse STACK — Fomalhaut–Sirius RA: Venus φ (exact 14:18, 18 min before the off) + Eris 1:2:3 → Diffident's SUN tightest (0.004%) and his TRANSPLUTO 2nd (0.019%)** on both.
- Diffident also: Orcus 0.002% tightest on Bellatrix–Sirius Dec; Vesta in UNISON on Equator–Procyon Dec (0.014%).
- Number check: 1 ninth (Dec to Fomalhaut 196/9). No parallel.
- Eddie asked (13:00): natal Eris to race-day Eris — Dettori: RA 3.954, **Dec 6.663** (6.662–6.665 over his birth day), Flat 7.748, Sky 7.709; Diffident: RA 1.320, Dec 1.288, Flat 1.844, Sky 1.834. Dettori's Dec gap is 0.0035 under 60/9 (6.6667) — outside ±0.002 on the day, but sky Eris's Dec moves ~0.004°/day and the gap was exactly 60/9 about 0.8 day earlier (≈19:30 on 27 Sep; approximate, TNO reflex model). 6.663 does not occur elsewhere in his natal pairs or the race-day sky pairs.
#### Sedna (RA 45.599, Dec 4.872; very slow)
- **Procyon–Spica RA 4:5:9 → Dettori's KETU tightest (0.019%) and MAKEMAKE (all day)** — the Sun also played Procyon–Spica that day (exact 01:19, Makemake): Sun + Sedna on it.
- **Aldebaran–Fomalhaut RA φ: Dettori's MERCURY tightest (√2, 0.018%) and his ERIS (√2, all day)** — only Dettori's bodies.
- Diffident: Pallas on Deneb Algedi–Pleiades RA (0.028%), Chiron on Castor–Sirius.
- Number check: 2 hits — **Dec to Altair = whole 4 (3.9989)**, Dec to Alkaid 400/9. No parallel.
#### Haumea (RA 193.320, Dec 21.281; very slow)
- **Antares–Rigel Dec φ — his THREE-BODY string held: Dettori's ORCUS (0.043%), SATURN (0.074%), MAKEMAKE (0.104%) all tuned, only Dettori.** The Sun (exact 04:31) and Venus (exact 05:38, while Venus sat on his Orcus Dec) also played Antares–Rigel that morning: **Sun + Venus + Haumea on his three-body string.**
- Algol–Rigel Dec 2:3:5: his CERES (0.034%). Aldebaran–Altair Dec: Diffident's Juno tightest (0.024%), Dettori's Saturn loose.
- Number check: 2 ninths (RA to Deneb Algedi 1201/9, RA to Pleiades 1228/9). No parallel.
#### Makemake (RA 176.188, Dec 32.756; very slow) — holds strings the faster bodies struck
- **Antares–Betelgeuse Dec → his QUAOAR (at the midpoint, 0.020%, all day): Sun (13:07) + Juno (07:07) + Makemake** — three sky bodies.
- **Altair–Antares RA → his CHIRON (0.025%, all day): Ceres (22:06) + Makemake.** Arcturus–Bellatrix Sky → his Chiron (0.013%): Pallas (09:46) + Makemake.
- **Algol–Rigel Dec → his CERES (0.034%): Haumea + Makemake.** Alkaid–Procyon RA → his Haumea: Ceres (19:11) + Makemake (exact 21:08). Equator–Rigel Dec → his ORCUS: Venus (06:55, on his Orcus Dec) + Makemake.
- Also: Fomalhaut–Regulus Dec (his Uranus, all day), Alphecca–Vega Dec 1:1:2 (his Quaoar), Aldebaran–Bellatrix (his Mercury).
- Diffident: JUPITER 0.009% tightest on Arcturus–Equator Dec; Transpluto on Antares–Bellatrix.
- No number hits, no parallel. Sky Makemake does not touch his natal Makemake (that body is held by the Sun, Mars, Ceres, Juno, Chiron, Pluto).
#### Quaoar (RA 241.215, Dec −14.272; very slow)
- **Antares–Rigel Dec 1:2:3 → his THREE-BODY string (Orcus 0.043%, Saturn, Makemake; only Dettori): now Sun + Venus + Haumea + Quaoar — four sky bodies.**
- **Aldebaran–Castor Dec 1:2:3 → his MAKEMAKE in UNISON (1:2:3, 0.040%, all day): Mars (15:31) + Chiron + Quaoar** — three sky bodies, UNISON on Quaoar's.
- **Deneb Algedi–Vega RA 4:5:9, exact 07:51 → his CHIRON in UNISON (4:5:9, 0.031%, all day).**
- Alphecca–Arcturus RA φ (exact 13:22): Diffident's Haumea, Dettori's Venus (loose). Diffident's Quaoar on Altair–Spica (same body).
- Number check: 1 ninth (Dec to Spica 28/9). No parallel.
#### Orcus (RA 136.112, Dec 0.454; very slow) — quiet
- Only one Dettori holding: Capella–Fomalhaut RA 3:5:8 → his TRANSPLUTO (φ, 0.063%, all day) — loose (sky 0.146%). Venus also crossed Capella–Fomalhaut in RA that evening (19:38, √2): Venus + Orcus on his Transpluto.
- Diffident: his ORCUS on Procyon–Regulus RA (same body, 0.053%); Ketu loose on Polaris–Spica.
- Number check: 3 ninths (Orcus's own RA 1225/9, RA to Alphecca 878/9, Dec to Vega 345/9) vs 1.5. No parallel.
#### Gonggong (RA 330.704, Dec −18.389; very slow) — the horse's body
- Dettori: only Antares–Capella Dec (his Vesta, loose 0.098%).
- **Diffident:** JUPITER 0.002% tightest on Pleiades–Regulus Dec (his Pluto 2nd, 0.029%); Pluto tightest on Pleiades–Procyon (Juno and Chiron played it too); Uranus on Capella–Equator Dec (0.021%) and Alphecca–Spica RA.
- No number hits, no parallel.
#### Transpluto (RA 146.876, Dec 13.330; very slow)
- **SAME BODY — Alphecca–Altair Dec 1:3:4 → Dettori's natal TRANSPLUTO (√2, all day): the Sun (exact 14:34:39, 81 s before the off) + Juno (09:37) + sky Transpluto** — his Transpluto held by its own sky body and struck by the Sun just before the off.
- **Algorab–Bellatrix RA φ → his ORCUS: Mars (exact 13:58) + Transpluto.** Altair–Arcturus RA 4:5:9 → his CHIRON in UNISON: Vesta (≈14:00) + Transpluto. Pleiades–Rigel Dec → his Chiron. Arcturus–Polaris RA → his Ketu.
- **Number check — 5 hits vs 0.44 + 1.5: RA to ALKAID = whole 60, RA to PLEIADES = whole 90** — so the Alkaid–Pleiades RA chord (2:3:5, 0.002%, exact 16:18) is 60 : 90 : 150, all whole numbers; also Dec to Capella 294/9, Dec to Castor 167/9, RA to Deneb Algedi 1619/9.
- Diffident: Chiron (Castor–Sirius), Jupiter (Alkaid–Pleiades), loose.
- Eddie (13:23): "how close in transit Transpluto and Venus" — at the off sky Venus–sky Transpluto RA 0.935, Dec 0.234, Sky 0.939; Venus closing ~1.1°/day (Transpluto ~0.008), meeting in Dec ≈08:55 and in RA ≈10:50 on 29 Sep (the morning after). In the same small patch of sky: **Diffident's natal TRANSPLUTO** (RA 145.135, Dec 13.920 — Venus passed its RA the evening before), **Dettori's natal MAKEMAKE** RA 147.233 (0.36° in RA from sky Transpluto), **Dettori's natal ORCUS Dec** 13.683 (Venus crossed it at 05:30). Sky Venus, sky Transpluto, the horse's Transpluto and the jockey's Makemake/Orcus within ~2°.
#### The nodes — Rahu (RA 187.381, Dec −3.188) / Ketu (RA 7.381, Dec 3.188)
- **Ketu: Antares–Rigel Dec 5:8:13 → his THREE-BODY string (Orcus, Saturn, Makemake): now Sun + Venus + Haumea + Quaoar + Ketu — FIVE sky bodies on it through the day.**
- **Rahu: Algol–Pleiades Dec φ → his other THREE-BODY string — his ORCUS in UNISON (φ), Gonggong, Sedna: Venus (13:49, 46 min before the off) + Mars (06:55) + Rahu.**
- Rahu: Procyon–Regulus Dec → his SUN (φ, 0.015%): Venus (14:56) + Pallas (17:14) + Rahu (and Jupiter on his Sun's Dec all day).
- Ketu: Antares–Pleiades Dec √2 → his MARS (0.034%); Alphecca–Pleiades Dec → his ORCUS (Venus 07:43, during the Orcus crossing); Alkaid–Rigel RA → his Uranus (Sun 20:48 too).
- **The nodes lean hard to DIFFIDENT:** his ERIS 0.000% on Pleiades–Rigel RA (Rahu), JUPITER 0.002% on Pleiades–Regulus Dec (Rahu; Gonggong holds it too — STACK), HAUMEA 0.006% on Equator–Sirius Dec (Rahu), KETU 0.007% on Aldebaran–Alkaid Dec (Rahu; Chiron holds it too — STACK), JUNO 0.001% and QUAOAR 0.004% on Castor–Polaris Dec (Ketu).
- Number check: Rahu 2 ninths (RA to Algol 1263/9, RA to Procyon 653/9); Ketu Dec to Arcturus = whole 16, plus 3 ninths. No parallel.
### METHOD 3 SUMMARY (Dettori race) — written to dettori_ascot_19960928_summary.md (project claude/dettori-ascot-19960928-summary.md)
- Before the off: Mars 14:34:12 → only his ORCUS (Bellatrix–Regulus); Sun 14:34:39 → only his TRANSPLUTO (Alphecca–Altair); Sun 14:35:06 → his MAKEMAKE tightest (Castor–Fomalhaut); earlier Venus 13:49 (Algol–Pleiades, only his three bodies), Mercury ≈14:00 (Pallas), Mars 14:10 (Transpluto + Diffident's Rahu), Mercury 14:25 (only his Ketu, Deneb Algedi).
- All day: Jupiter on his natal Sun Dec (replays his Sun's chords; holds Bellatrix–Capella); Vesta on Diffident's natal Sun Dec; Venus over his Orcus Dec at 05:30; five sky bodies on Antares–Rigel, three on Algol–Pleiades; Makemake stacked on six strings; Transpluto and Orcus stacked.
- The horse: slow bodies and nodes; stacks on his Sun, Jupiter, Ketu.
- Not done: power points; Method 2.
### Power points (Dettori race)
- Background: Dec mean 5.6, 99% 12, 99.9% 14; RA mean 4.1, 99% 10, 99.9% 13.
- Sky: **no body on a power point.** Highest: the Sun Dec 11 (just under 99%), Chiron Dec 10, Mercury/Venus/Jupiter Dec 9; the Moon peaks at 7 RA pairs 2 min before the off. Transpluto is at RA 146.9 in 1996 — not on the RA 155 node it sat on in 2021–22 (so that node is a period, not a constant).
- **Natal: only one point in either chart — DETTORI's MAKEMAKE Dec 39.573, load 13** (above 99%, just under 99.9%). That is the body the Sun struck 54 s before the off (Castor–Fomalhaut) and the sky stacked on six strings through the day.
- **Same as Exeter:** there James Best's SEDNA (load 13) was the only top natal power point and the body the slow sky gathered on. Two winning jockeys, each with one natal power-point body at load 13, each the body the race-day sky held hardest.
- Eddie (13:37): no Method 2 for this race — the detour was to see what Dettori had on the day. Detour closed.

## 74. DETOUR — Lionel Messi's five goals, Barcelona 7–1 Bayer Leverkusen, Camp Nou, 7 Mar 2012 (Eddie 7 Oct 13:54)
- Champions League last 16, 2nd leg. Messi goals ≈25', 42', 49', 58', 84' (order and 84' confirmed by UEFA's report; other minutes from memory — to confirm). Kick-off assumed 20:45 CET (19:45 UT) — Eddie's own Japan-engine command used 21:45 Madrid; to confirm.
- Messi born 24 Jun 1987, Rosario, Argentina. Eddie gave a birth time of 20:30 (Japan-engine command); the workbook route uses noon like all other charts, so "all day" checks are kept and 20:30 can be checked against them.
- Files: Eddie's workbook (charts v2.3, engine v2.2; Ascot stand-in at 19:45 GMT = the same instant) → setup_messi.py: Barcelona coordinates (41.38087, 2.122802, 50 m), race id 20120307_barcelona_2045, sky every minute from −60 to +150 (whole match). Engine vs workbook differs only by location (Moon 0.12°, angles; planets ≤0.0005° parallax); TNOs from the workbook.
### Method 1 — Messi's chart (numbers, then chords), one body at a time
#### Sun (RA 93.001, Dec 23.414 — born at the June solstice, so the Sun's Dec barely moves over the day: 23.422 → 23.402)
- **Numbers:** Dec to ARCTURUS = 38/9 (10:46–15:35); Dec to REGULUS = 103/9 (11:31–16:06); the Sun's own RA = whole 93 at midday (11:56–12:01); Flat to Aldebaran = 25, RA to Alkaid 1025/9 (minutes). About chance.
- **Chords held all day (Dec — the solstice Sun is steady in Dec):** **Alkaid–Betelgeuse φ, 0.010%** (0.068% / 0.133%); **Altair–Procyon 1:4:5, 0.026%** (0.028% / 0.109%); Deneb Algedi–POLARIS 3:5:8 (0.081%); with his own bodies **Chiron–Ketu Dec 1:4:5** (0.091%). Nearly: Alkaid–Spica 3:4:7, Capella–Castor 3:5:8, Algol–Equator 3:4:7.
- RA chords (Fomalhaut–Vega 3:5:8 0.031%, Regulus–Spica, Eris–Transpluto √2 0.022%, Mars–Rahu 1:4:5) depend on the birth hour.
#### Mercury (RA 107.612, Dec 19.926; retrograde-ish — RA falling 0.3°, Dec falling 0.24° over the day; nothing holds all day)
- **Numbers** (midday only): Dec to SEDNA = whole 16 (11:38–12:02); Dec to Jupiter 102/9; Dec to POLARIS 624/9 (11:43–12:07); RA to Bellatrix 237/9; Flat to Algorab 790/9. About chance.
- **Chords** — none all day. Tight at midday only: **Algorab–Antares RA 3:4:7, 0.002%**; **Alkaid–Procyon Dec 1:2:3, 0.005%**; **Orcus–Pallas Dec 3:8:11, 0.000%**; Haumea–Transpluto Dec √2 (0.013%); Makemake–Pallas RA 5:6:11 (0.024%); Orcus–Pluto RA 1:5:6 (0.027%). Nearly: Jupiter–Ketu Sky 1:1:2 (Mercury at the midpoint), Ketu–Sedna RA 5:6:11.
- **Birth time (Eddie 14:06): 20:30 local, Rosario, 24 Jun 1987 (Astro-Databank / astridsigns).** = hour 20.5 in the natal file (UTC−3, 23:30 UT). natchords.py / natnums.py now take an hour argument; from here Messi's bodies are read at 20:30 (the 00:00/24:00 range kept for reference).
#### Sun at 20:30 (RA 93.366, Dec 23.406)
- **Numbers — above chance, mostly Dec (the solstice Sun is steady in Dec, so they hold for hours around 20:30):** Dec to BETELGEUSE = whole 16 (17:43–21:19); Dec to QUAOAR = whole 36 (20:13–23:33); Dec to CASTOR = 6√2 (19:53–23:31); Dec to Eris 299/9 (18:48–22:32), Uranus 422/9, Haumea 2/9 (17:02–22:15), Rahu 183/9 (20:11–21:50); Sky to Jupiter = 48√2; RA/Flat/Sky ninths to Altair, Arcturus, Spica, Alkaid, Ceres, Orcus (minutes). 4 φ/√2/whole (vs 1.7) and ~10 ninths (vs 5.8).
- **Chords at 20:30:** **Ketu–Transpluto Sky 1:1:2, 0.012% — his TRANSPLUTO at the midpoint of his Sun and Ketu**; **Mercury–Transpluto RA 2:5:7, 0.012%** (Sun–Mercury–Transpluto); Algol–Equator Dec 3:4:7 (0.042%); Alkaid–Alphecca RA φ; Deneb Algedi–Polaris Dec 3:5:8 (0.047%, all day); Alkaid–Spica Dec; Altair–Procyon and Alkaid–Betelgeuse (all day); Chiron–Mars Flat; Mars–Quaoar Sky; Pallas–Venus Flat.
#### Mercury at 20:30 (RA 107.496, Dec 19.841)
- **Numbers:** Sky to SEDNA = 41φ (20:29–20:46); Dec to Algol 190/9, Dec to Aldebaran 30/9, RA to Capella 255/9, Flat to Orcus 213/9, Chiron 221/9, Aldebaran 348/9 — a little above chance on ninths.
- **Chords:** **Antares–POLARIS Dec 2:3:5, 0.011%**; **Sun–Transpluto RA 2:5:7, 0.012%** (the same Sun–Mercury–Transpluto chord); Bellatrix–Fomalhaut Dec 3:8:11 (0.024%); Pallas–Quaoar Dec 1:6:7 (0.040%); Bellatrix–Deneb Algedi and Deneb Algedi–Fomalhaut Dec (0.05%); Makemake–Transpluto RA 5:8:13 (0.050%). (The midday chords — Orcus–Pallas 0.000%, Algorab–Antares, Alkaid–Procyon — do not hold at 20:30.)
- **TRANSPLUTO already central at his birth hour:** Sun–Mercury–Transpluto RA, Sun–Transpluto–Ketu Sky midpoint, Makemake–Transpluto–Mercury RA.
#### Venus at 20:30 (RA 75.861, Dec 22.221)
- **Numbers:** **Sky to SEDNA = 27√2 (38.1837 vs 38.1838)**; Flat to Castor = whole 39; Venus's own |Dec| = 200/9 (20:22–20:58); Dec to Capella 214/9; Flat to Haumea, Sky to Uranus (ninths). 3 φ/√2/whole (vs 1.7).
- **Chords — an EQUATOR cluster in Dec** (Venus 22.221 from the equator): **Betelgeuse–Equator 1:2:3, 0.001%**; Bellatrix–Equator 2:5:7 (0.018%); Equator–Fomalhaut 3:4:7 (0.031%); also Altair–Spica Dec 2:3:5 (0.014%), Betelgeuse–Fomalhaut Dec 2:5:7 (0.025%), Antares–Regulus RA 4:5:9 (0.021%), Fomalhaut–Regulus RA (0.030%), Altair–POLARIS RA φ (0.046%).
- **With his own bodies — the NODES and ORCUS:** **Ketu–Orcus RA 5:6:11, 0.002%**; **Makemake–Rahu Dec 3:4:7, 0.006%**; Juno–Orcus RA 1:2:3 (0.015%); **Ketu–Rahu RA φ, 0.016% — Venus at a φ point of his nodal axis**; Orcus–Pluto Dec φ (0.034%); Orcus–Transpluto Dec 5:6:11; Rahu–Saturn, Rahu–Uranus RA. ORCUS five times, the nodes six.
- Venus moves 1.3° in RA and 0.16° in Dec over the day — these hold for an hour or two around 20:30.
#### Mars at 20:30 (RA 114.689, Dec 22.663; moves 0.7° in RA, 0.1° in Dec over the day)
- **Numbers:** RA to POLARIS = whole 77 (20:23–20:30); RA to Algorab 655/9; Sky to Altair 1335/9 (20:20–20:53). About chance.
- **Chords with the stars:** Capella–Fomalhaut RA 3:8:11 (0.019%); Bellatrix–Sirius Dec √2 (0.038%); Aldebaran–Castor Dec 2:3:5 (0.039%); Aldebaran–Vega Dec φ; Betelgeuse–Procyon Dec 1:7:8 and **Fomalhaut–Procyon Dec 1:2:3** (0.058–0.059%); Alkaid–POLARIS Dec 2:3:5.
- **With his own bodies:** **Quaoar–Rahu Dec 4:5:9, 0.012%**; **Jupiter–Sedna Dec 1:3:4, 0.013%**; **Gonggong–Jupiter RA 3:5:8, 0.018%** (holds most of the day: 0.282% at 00:00, 0.027% at 24:00); Chiron–Juno Dec 1:4:5 (0.035%); Haumea–Makemake RA 3:8:11 (0.043%); Haumea–Quaoar RA 2:3:5; Quaoar–Sun Sky; Eris–Haumea RA; Sun–Transpluto Sky √2 (Mars on the Sun–Transpluto string again).
- JUPITER three times, HAUMEA three, QUAOAR three.
#### Jupiter at 20:30 (RA 23.818, Dec 8.612; moves 0.15° in RA, 0.05° in Dec)
- **Numbers:** **Sky to SEDNA = φ⁶** (20:30–21:16) — Sedna again (Venus 27√2, Mercury 41φ); Sky to Sun = 48√2 (same pair as from the Sun); RA to Arcturus = 105φ (19:52–20:30); ninths: RA to Juno 442/9 (19:43–21:02), Flat to Antares, Rigel, Sky to Gonggong 550/9, Spica, Algol. 3 φ/√2 (vs 1.7) + 6 ninths.
- **Chords — VEGA six times:** Arcturus–Vega RA 5:8:13 (0.064%, held all day); Alphecca–Vega Dec 2:3:5 (0.035%); Deneb Algedi–Vega RA 5:6:11 (0.052%, nearly all day); Algorab–Vega Dec 5:6:11; Regulus–Vega Dec; Deneb Algedi–Vega Flat. Also Arcturus–Castor Dec 5:6:11 (0.030%), Capella–Pleiades Dec √2.
- **With his own bodies:** **Makemake–Orcus RA 3:8:11, 0.025%, held all day** (0.111% / 0.010%); Mars–Sedna Dec 1:3:4 (0.013%); Gonggong–Mars RA 3:5:8 (0.018%, most of the day); Chiron–Pallas Dec 3:4:7 (0.027%); Eris–Saturn Dec φ.
#### Saturn at 20:30 (RA 255.938, Dec −21.214; near-stationary)
- **Numbers:** Saturn's own |Dec| = **15√2** (21.2142; 15:01–24:00); **Dec to PROCYON = 238/9** (03:58–24:00); Sky to HAUMEA 750/9 (20:06–21:29); Flat to Spica 500/9, to Juno 734/9.
- **Chords with the stars (most hold all day):** **Algol–Altair RA φ, 0.004%** at 20:30 (0.022% at 24:00, 0.157% at 00:00 — in from early morning); Capella–Fomalhaut Dec 1:8:9 (0.037%, all day); **Alkaid–PROCYON Dec 3:5:8 (0.037%, all day)**; Regulus–Rigel RA √2 (0.043%, all day); Betelgeuse–Rigel Dec 5:6:11 (0.045%); Castor–Regulus Dec 3:5:8; Fomalhaut–Spica RA φ; Algol–Fomalhaut RA √2.
- **With his own bodies:** Ketu–Uranus Dec 1:8:9 (0.030%); Rahu–Venus RA φ (Venus's nodal φ point seen from Saturn — Venus–Rahu–Saturn); Eris–Jupiter Dec φ (0.075%); Rahu–Vesta Dec √2.
#### Ceres at 20:30 (RA 267.555, Dec −26.018; moves 0.25° RA, 0.05° Dec)
- **Numbers (around 20:30):** Flat to Rigel = whole 172 (20:21–20:43); ninths to Chiron (RA 1579/9), Alkaid (RA 546/9 and Dec 678/9), Castor, Vesta, Sun (Sky 1567/9 — same as from the Sun), Altair; Ceres's own RA 2408/9. 1 whole + 9 ninths (ninths above chance).
- **Chords:** **Betelgeuse–Spica Dec 4:5:9, 0.000%** at 20:30 (0.052% at 24:00); Alkaid–Arcturus Dec 2:3:5 (0.043%, all day); Algorab–Regulus Dec 1:3:4; Aldebaran–Polaris Sky (all day); Algol–Alkaid Dec 1:8:9 (all day); Betelgeuse–Pleiades Dec 1:2:3 (all day). ALKAID three times.
- **With his own bodies:** Makemake–Pluto Flat 5:6:11 (0.024%); Juno–Makemake Dec √2; Chiron–Haumea Dec 1:8:9; **Makemake–Orcus RA 3:8:11 (0.064%) — Jupiter holds the same pair (Jupiter–Makemake–Orcus all day)**; Haumea–Rahu Dec √2; Mars–Sedna Dec 5:8:13 (Jupiter–Mars–Sedna too).
#### Pallas at 20:30 (RA 233.623, Dec 25.245) — quiet on the stars
- Numbers: Dec to HAUMEA = φ (19:33–20:33); RA to Uranus 274/9 (19:14–20:55); Sky to Fomalhaut 1074/9 (19:47–21:46); Flat to Polaris 1585/9.
- Only 2 star chords: Algorab–Castor RA 5:8:13 (0.035%), Castor–Regulus Dec 1:2:3.
- With his own bodies: Chiron–Jupiter Dec 3:4:7 (0.027%); Mercury–Quaoar Dec 1:6:7 (0.040%); Quaoar–Rahu Dec √2 (0.050%; Mars also on Quaoar–Rahu); Ketu–Makemake Dec 2:5:7; Ketu–Orcus Flat (Venus has Ketu–Orcus in RA). Nodes five times.
#### Juno at 20:30 (RA 334.707, Dec −0.081 — on the equator)
- **Numbers:** **Flat to SEDNA = 600/9 (66.6663)** — Sedna's fourth number (Venus 27√2, Mercury 41φ, Jupiter φ⁶, Juno 600/9); RA to Fomalhaut = 6φ; RA to Algorab = 91φ; RA to Transpluto 1513/9; RA to Jupiter 442/9 (same pair as from Jupiter); Flat to Saturn 734/9. 2 φ (vs 1.7) + 4 ninths.
- **Chords with the stars:** **Algol–Sirius RA 3:4:7, 0.003%** (all day); **Regulus–Rigel RA √2, 0.030% — Saturn holds Regulus–Rigel RA √2 all day too: two bodies, same chord** (all day); Fomalhaut–Spica Dec 3:5:8; Arcturus–Regulus, Arcturus–Deneb Algedi, Deneb Algedi–Regulus Dec.
- **With his own bodies:** Orcus–Venus RA 1:2:3 (0.015%, the Venus chord); Chiron–Mars Dec 1:4:5 (0.035%); Ceres–Makemake Dec √2; Neptune–Transpluto Dec 2:3:5; Pluto–Uranus RA φ (all day); Makemake–Quaoar and Neptune–Quaoar RA (all day).

#### Vesta at 20:30 (RA 77.781, Dec +20.261)
- Numbers: Dec to SEDNA = 147/9 (16.3331, holds 19:39–21:34) — Sedna's fifth number (Venus 27√2, Mercury 41φ, Jupiter φ⁶, Juno 600/9, Vesta 147/9); Dec to Polaris = whole 69 (19:07–21:00); RA to Algol = 19φ; own RA = 55√2; RA to Rahu 636/9 (Ketu 984/9, same fact); Dec to Ketu 210/9; Dec to Algorab 331/9; Sky to Ceres 1524/9, Altair 1180/9, Algorab 1023/9; Flat to Antares 1583/9. 3 φ/√2/whole (vs ~1.7) + 8 ninths (vs ~5.8) — about chance overall; the Dec hits hold for hours.
- Chords with the stars: Aldebaran–Betelgeuse RA 4:5:9, 0.016% (Betelgeuse again: Sun Dec 16, Venus Betelgeuse–Equator, Ceres Betelgeuse–Spica); Capella–Deneb Algedi Dec 1:√2:1+√2 (all day-ish, 0.011% at 24:00); Altair–Fomalhaut RA 1:2:3; Betelgeuse–Capella Dec 1:2:3; Alkaid–Castor Dec 2:3:5.
- With his own bodies: Eris–Rahu Dec 3:4:7, 0.002% (tightest); SEDNA four times — Chiron–Sedna RA 1:7:8 (0.009%), Neptune–Sedna Dec 5:8:13 (0.015%), Makemake–Sedna Dec 1:1:2 (Vesta at the Dec midpoint of Makemake and Sedna), Orcus–Sedna RA 3:4:7; Chiron–Transpluto Dec 5:8:13 (0.023%); Gonggong–Quaoar Dec 1:4:5 (all day); Haumea–Rahu RA 2:3:5; Rahu–Saturn Dec 1:√2:1+√2.

#### Uranus at 20:30 (RA 264.069, Dec −23.482)
- Numbers: Dec to ORCUS = 18φ (29.1246, off 0.0000, holds 09:28–24:00); Dec to Betelgeuse 278/9 (all day); Flat to Betelgeuse 110φ; Flat to Antares 12√2; Dec to Eris 123/9 (all day); Dec to Haumea 424/9 and to Sun 422/9; Dec to Rahu 239/9; RA to Pallas 274/9; Sky to Venus 1551/9. 3 φ/√2/whole (vs ~1.7) + 6 ninths (vs ~5.8).
- Chords with the stars: Regulus–Sirius Dec φ, 0.000% (all day); Alphecca–Betelgeuse Dec 5:8:13, 0.019% (all day); Betelgeuse also in Betelgeuse–Capella Dec 4:5:9 and Arcturus–Betelgeuse Dec φ — Betelgeuse is now on Sun, Venus, Ceres, Vesta, Uranus; Arcturus group in RA: Arcturus–Castor 1:2:3 (0.014%), Arcturus–Deneb Algedi 4:5:9, Antares–Arcturus 1:2:3; Antares–Castor RA 1:8:9; Alkaid–Altair, Algol–Polaris Dec (all day).
- With his own bodies: Haumea–Neptune RA 1:6:7 (0.015%); Haumea–Orcus Dec φ (all day — Uranus Dec 18φ to Orcus with Haumea at 424/9: Uranus–Haumea–Orcus a Dec triangle); Ketu–Saturn Dec 1:8:9; Juno–Pluto RA φ (the same three as Juno's Pluto–Uranus RA φ — Juno, Pluto, Uranus close a φ triangle); Quaoar–Sedna RA 1:4:5; Sedna–Venus Dec 2:3:5; Rahu–Venus RA 2:3:5.

#### Neptune at 20:30 (RA 277.459, Dec −22.210) — quieter
- Numbers: Flat to Rigel = 1456/9 (off 0.0000, 18:49–22:10); Sky to GONGGONG = whole 48 (18:42–23:27); RA to Procyon = 115√2; Dec to Antares 38/9 (06:25–24:00); RA to Makemake 1013/9; Sky to Algol 1205/9. 2 φ/√2/whole (vs ~1.7) + 4 ninths (vs ~5.8) — at chance.
- Chords with the stars: none under 0.05%; Betelgeuse three times in Dec — Betelgeuse–Equator 1:3:4 (same base as Venus's Betelgeuse–Equator), Alkaid–Betelgeuse 1:√2:1+√2, Betelgeuse–Fomalhaut 1:4:5; Capella–Fomalhaut RA 1:√2:1+√2; Antares–Spica Dec φ.
- With his own bodies (mostly the other side of chords already seen): Sedna–Vesta Dec 5:8:13 (Vesta's); Haumea–Uranus RA 1:6:7 (Uranus's); new: Makemake–Sedna Dec 4:5:9 (all day-ish, 0.014% at 00:00) — Vesta had Makemake–Sedna Dec 1:1:2: two bodies on the same string of his own; Juno–Transpluto Dec 2:3:5 (closes Juno's Neptune–Transpluto); Eris–Mercury RA φ; Eris–Mars Dec φ.
- **Eddie's spot — Neptune Dec and Venus Dec:** Venus +22.221, Neptune −22.210 at 20:30 — contraparallel (mirror across the equator), 0.012° apart. Exact at 18:42 (sum 0.0000), 1h48m before birth; separating slowly (0.0116 at 20:30, 0.034 at 24:00) — holds all day within 0.13°. Venus Dec = 200/9 (22.2222) at 20:40 (off −0.0011 at 20:30). Betelgeuse Dec ≈ 7.407 ≈ one third of that: Venus at 3× Betelgeuse Dec on one side (Betelgeuse–Equator 1:2:3), Neptune at 3× on the other (Betelgeuse–Equator 1:3:4) — the same Betelgeuse–Equator string from both sides of the equator. A mirror inside his own chart.
- **Juno Dec with the mirror (Eddie):** Juno −0.0815 at 20:30 sits between Venus (+22.221) and Neptune (−22.210), 0.087 south of their midpoint; it never reaches the equator on the birth day (−0.111 at 00:00 → −0.077 at 24:00), so V–J 22.303 : J–N 22.128 is 1:1:2 at 0.8% — close, not inside a chord. Betelgeuse Dec at birth 7.4071 = 200/27 (7.4074, off −0.0003): Betelgeuse exactly a third of Venus's 200/9. Picture: Venus +200/9, Betelgeuse +200/27, Juno ≈ 0, Neptune ≈ −200/9 — one Dec line, with Juno near its centre.
- **CARRY TO THE TRANSITS (Eddie 14:37):** check the match sky against this Dec line — Venus +200/9, Betelgeuse +200/27, Juno ≈ 0, Neptune −22.21.

#### Pluto at 20:30 (RA 220.455, Dec +1.727)
- Numbers: SPICA twice — Sky to Spica = whole 23 (14:58–21:47) and Dec to Spica 116/9 (10:46–24:00); RA to Alphecca 119/9 (17:55–24:00); RA to Betelgeuse 1185/9; Flat to Pleiades 1486/9; Flat to Rahu 1320/9 (20:07–20:38, birth hour only); Sky to Eris 1444/9. 1 whole (vs ~1.7) + 6 ninths (vs ~5.8) — at chance; mostly long-holding.
- Chords with the stars: Alphecca–Altair Dec 2:5:7, 0.004%; Regulus–Vega Dec φ, 0.008% (0.002% at 24:00); Altair–Deneb Algedi Dec 2:5:7, 0.016% — Pluto sits on one Dec line with Alphecca, Altair and Deneb Algedi (the same 2:5:7 both ways); Alkaid–Deneb Algedi Dec 3:8:11; Altair–Rigel Sky 6:11:11. Spica (Ceres Betelgeuse–Spica, Vesta Pleiades–Spica, Pluto by number) is building.
- With his own bodies: ORCUS three times — Orcus–Venus Dec φ (0.034%; Juno had Orcus–Venus RA 1:2:3 — the same pair now in RA and Dec), Mars–Orcus RA 1:8:9, Orcus–Pallas Dec 1:5:6; Ceres–Makemake Flat 5:6:11 (0.024%; Juno had Ceres–Makemake Dec √2); Juno–Uranus RA φ — the same Juno–Pluto–Uranus φ triangle, now seen from each of its three bodies (one fact, not three); Ketu–Makemake RA 2:3:5; Ceres–Ketu RA 1:√2:1+√2.

#### Chiron at 20:30 (RA 83.000, Dec +18.115)
- Numbers: own RA = whole 83 (82.9998; 20:02–21:04 — the birth hour); Dec to VEGA 186/9 (all day); Sky to Rigel 240/9 (15:14–21:10); RA to Alkaid 1115/9; Sky to Gonggong 1061/9; Flat to Procyon 309/9, Sirius 354/9, Haumea 908/9, Mercury 221/9; RA to Ceres 1579/9. 1 whole (vs ~1.7) + 10 ninths (vs ~5.8) — ninths above chance.
- Chords with the stars: Altair–Deneb Algedi RA 1:4:5, 0.015% (0.003% at 24:00) — Pluto has Altair–Deneb Algedi Dec 2:5:7: same string, two bodies (Pluto in Dec, Chiron in RA); Castor–Vega Dec 1:2:3 — Vega now Jupiter ×6, Pluto (Regulus–Vega φ), Chiron (186/9 + Castor–Vega); Algol–Deneb Algedi Dec 2:3:5; Alphecca–Arcturus Dec 1:7:8.
- With his own bodies: Gonggong–Orcus RA φ, 0.008% — ORCUS again; Eris–Haumea RA 3:5:8, 0.023%; Jupiter–Pallas Dec 3:4:7, 0.027%; repeats seen from the other side: Sedna–Vesta RA 1:7:8 (Vesta's), Transpluto–Vesta Dec 5:8:13 (Vesta's), Juno–Mars Dec 1:4:5 (Juno's); Ceres–Haumea Dec 1:8:9; Orcus–Vesta Flat 1:8:9.

#### Eris at 20:30 (RA 22.542, Dec −9.816) — strong on ninths, all long-holding
- Numbers (11 ninths vs ~5.8; 0 φ/√2/whole): Dec to Betelgeuse 155/9 (all day); Sky to Alkaid 1263/9 (all day); Dec to Uranus 123/9 (all day, Uranus's); RA to Deneb Algedi 502/9 (00:00–22:49); Flat to Rigel 505/9 (01:18–24:00); RA to ORCUS 935/9 (16:58–23:14); Dec to Haumea 301/9 (16:28–24:00) and to Sun 299/9 (18:48–22:32) — Sun and Haumea 2/9 apart in Dec around Eris; Dec to Quaoar 25/9; Dec to Rahu 116/9; Sky to Pluto 1444/9 (Pluto's).
- Chords with the stars: Rigel–Spica Dec 5:6:11, 0.010% (Spica again); Algol–Arcturus Dec 3:4:7 (all day); Aldebaran–Procyon Dec 3:4:7 (all day — the Exeter string); DENEB ALGEDI five times: Betelgeuse–Deneb Algedi Sky 4:5:9, Deneb Algedi–Procyon Flat 3:5:8, Deneb Algedi–Rigel Flat 1:1:2 (Eris at the Flat midpoint), Aldebaran–Deneb Algedi RA 5:6:11, Alphecca–Deneb Algedi RA 3:5:8 — Deneb Algedi now on Pluto, Chiron, Eris; Betelgeuse also in Betelgeuse–Castor RA, Betelgeuse–Sirius Dec.
- With his own bodies: MAKEMAKE–ORCUS Dec 1:2:3 (all day) — Jupiter and Ceres already on Makemake–Orcus: three of his bodies on one string of his own (a natal stack); Gonggong–Sedna Dec 4:5:9 (all day); Jupiter–Saturn Dec φ; repeats: Rahu–Vesta Dec 3:4:7 0.002% (Vesta's), Chiron–Haumea RA 3:5:8 (Chiron's), Mercury–Neptune RA φ and Mars–Neptune Dec φ (Neptune's); Gonggong–Venus RA 1:1:2.

#### Sedna at 20:30 (RA 41.252, Dec +3.927) — the receiver
- Numbers: 7 φ/√2/whole (vs ~1.7) + 7 ninths (vs ~5.8) — the strongest body by number so far.
  - From his own bodies, all inside the birth hour: Sky to VENUS 27√2 (off 0.0000, 20:28–20:32); Sky to MERCURY 41φ (20:29–20:46); Sky to JUPITER φ⁶ (20:30–21:16); Flat to JUNO 600/9 (19:44–21:02); Dec to VESTA 147/9 (19:39–21:34); Dec to KETU whole 7 (20:18–21:26). All six overlap 20:30–20:32. CORRECTION (7 Oct 17:45): these are hits found AT 20:30, so their windows must include 20:30 — the overlap is not evidence for the birth time; what counts is that six bodies land on Sedna by number.
  - Long-holding: Flat to Makemake 1151/9 (all day); Dec and Sky to Polaris 768/9 (all day, both); Dec to Algorab 184/9 (all day); Flat to Fomalhaut whole 66 (13:02–24:00); Flat to Aldebaran 274/9 (12:20–24:00); RA to Altair 64φ (17:22–24:00); Flat to Capella 35φ (19:52–24:00).
- Chords with the stars: Aldebaran–Fomalhaut Dec 3:8:11, 0.017% (all day); Castor–Fomalhaut Dec 5:6:11 (all day) — Fomalhaut also whole 66 and Fomalhaut–Sirius Dec; Bellatrix–Sirius–Spica RA lattice: Bellatrix–Sirius 1:2:3, Sirius–Spica 3:5:8, Bellatrix–Spica 1:3:4 (Spica again); Alphecca–Deneb Algedi RA 4:5:9 (Eris has Alphecca–Deneb Algedi RA 3:5:8 — same string, two bodies); Alphecca–Altair RA φ (Pluto has Alphecca–Altair Dec 2:5:7); Alkaid–Pleiades Dec 4:5:9.
- With his own bodies: Jupiter–Mars Dec 1:3:4, 0.013% (new); the rest are the Sedna chords already seen from the other side — Chiron–Vesta, Neptune–Vesta, Makemake–Vesta, Makemake–Neptune, Eris–Gonggong, Quaoar–Uranus, Uranus–Venus, Orcus–Vesta; Ceres–Mars Dec 5:8:13 (0.003% at 24:00).

#### Haumea at 20:30 (RA 183.739, Dec +23.629 — next to the solstice Sun)
- Numbers: 1 φ (vs ~1.7) + 11 ninths (vs ~5.8) — ninths well above chance, most long-holding.
  - Dec to SUN 2/9 (0.2229; 17:02–22:15) — Haumea and the solstice Sun share the Dec band, 2/9 apart (Eris sees them as 299/9 and 301/9).
  - Long: RA to Rigel 946/9 (06:39–24:00); Dec to BETELGEUSE 146/9 (13:14–24:00); Dec to Uranus 424/9 and to Eris 301/9 (both seen from their side); Flat to Deneb Algedi 1336/9 (13:51–24:00); Flat to TRANSPLUTO 377/9 (18:02–24:00).
  - Birth hour: Dec to Rahu 185/9 (20:03–21:18); Sky to Saturn 750/9; Flat to Chiron 908/9; Flat to Venus 971/9 (20:26–20:30); Dec to Pallas 1φ (19:33–20:33, at the edge).
- Chords with the stars: Betelgeuse–Regulus RA 1:2:3, 0.011% (all day) — Sedna has Betelgeuse–Regulus RA 3:4:7 and Flat 3:4:7: two bodies on one string; Equator–Sirius Dec 1:√2:1+√2, 0.023% (0.006% at 00:00); Altair–Equator Dec 3:5:8; Castor–Rigel RA 1:2:3; Alphecca–Sirius Sky 1:2:3; Bellatrix–Sirius Dec 3:4:7; Castor–Vega Dec 5:6:11 (Chiron has Castor–Vega Dec 1:2:3).
- With his own bodies: ORCUS three times — Orcus–Rahu Dec 1:7:8, Orcus–Uranus Dec φ (the Uranus triangle), Orcus–Transpluto RA 2:5:7; Makemake–Mars RA 3:8:11 (0.043%); Mars–Quaoar RA 2:3:5; Ceres–Rahu Dec (0.007% at 24:00); repeats: Neptune–Uranus RA 1:6:7, Chiron–Eris RA 3:5:8, Rahu–Vesta RA 2:3:5, Ceres–Chiron Dec 1:8:9.

#### Makemake at 20:30 (RA 164.902, Dec +36.581) — a partner more than a maker
- Numbers: 0 φ/√2/whole (vs ~1.7) + 6 ninths (vs ~5.8) — at chance. Flat to SEDNA 1151/9 (all day; Sedna's); Sky to TRANSPLUTO 265/9 (00:39–21:32); Flat to Antares 934/9; Sky to Bellatrix 730/9 and Arcturus 415/9; RA to Neptune 1013/9 (Neptune's).
- Chords with the stars: only 6, loose; two midpoints — RA midway between Polaris and Sirius (1:1:2, 0.034%), Dec midway between Deneb Algedi and Polaris (1:1:2); Castor–Regulus RA 1:3:4; Arcturus–Vega RA 3:4:7.
- With his own bodies: Rahu–Venus Dec 3:4:7, 0.006% (new — tightest); the ORCUS string from Makemake's side — Jupiter–Orcus RA 3:8:11 (0.025%, 0.010% at 24:00), Ceres–Orcus RA 3:8:11, Eris–Orcus Dec 1:2:3 (the three bodies already found on Makemake–Orcus); Sedna from Makemake's side — Neptune–Sedna Dec 4:5:9, Sedna–Vesta Dec 1:1:2; Mercury–Transpluto RA 5:8:13; Ceres–Pluto Flat 5:6:11 (Pluto's); Ceres–Juno Dec √2 (Juno's); Haumea–Mars RA 3:8:11 (Haumea's).
- Reads as: Makemake makes little of its own; it is the other end of the Orcus string and a side of the Sedna strings.

#### Quaoar at 20:30 (RA 229.804, Dec −12.596) — quiet
- Numbers: 1 whole (vs ~1.7) + 3 ninths (vs ~5.8) — below chance. Dec to SUN whole 36 (20:13–23:33; the Sun's number seen from Quaoar); Dec to Eris 25/9 (Eris's); RA to Antares 158/9 (20:04–24:00); Sky to Altair 637/9 (17:56–24:00).
- Chords with the stars: Pleiades–Vega Dec 2:5:7, 0.011% (all day; Vega again); Algol–Altair Flat 5:8:13, 0.016%; Aldebaran–Polaris Dec 2:5:7, 0.017% (all day); Alkaid–Fomalhaut RA 1:5:6; Antares–Capella Dec φ.
- With his own bodies: Mars–Rahu Dec 4:5:9, 0.012% — Mars had Quaoar–Rahu Dec: the same three (Mars, Quaoar, Rahu), now from Quaoar's side; Mercury–Pallas Dec 1:6:7; Pallas–Rahu Dec √2; repeats: Gonggong–Vesta (Vesta's), Haumea–Mars (Haumea's), Sedna–Uranus (Uranus's), Juno–Makemake / Juno–Neptune (Juno's).

#### Orcus at 20:30 (RA 126.431, Dec +5.642) — the hub
- Numbers: 1 φ (vs ~1.7) + 4 ninths (vs ~5.8) — modest by itself, but two land at birth: Sky to SUN 328/9 (20:29–20:35) and Flat to MERCURY 213/9 (19:58–20:41); Dec to Uranus 18φ (09:28–24:00, Uranus's); RA to Eris 935/9 (Eris's); RA to Deneb Algedi 1437/9 (15:33–20:36).
- Chords with the stars (18): Algorab–Pleiades Dec 5:6:11, 0.019%; Pleiades–Rigel Dec 3:4:7, 0.021% (0.010% at 00:00); Algol–Capella Dec 1:7:8, 0.022%; Alphecca–Fomalhaut Sky 6:7:8, 0.025%; Aldebaran four times (Aldebaran–Algol RA φ, Aldebaran–Castor Dec √2, Aldebaran–Spica Sky, Aldebaran–Deneb Algedi Dec); Regulus–Vega Dec φ (Pluto has Regulus–Vega Dec φ too — two bodies, same string, same family). No Betelgeuse at Orcus.
- With his own bodies (17 chords, 19 different bodies take part — nearly the whole chart ties to Orcus):
  - VENUS five times: Ketu–Venus RA 5:6:11 0.002%; Juno–Venus RA 1:2:3 0.015%; Pluto–Venus Dec φ 0.034%; Transpluto–Venus Dec 5:6:11 (new); Saturn–Venus Dec φ (new; 0.028% at 24:00). Orcus–Venus is his key pair.
  - The MAKEMAKE string: Jupiter–Makemake RA 3:8:11, Ceres–Makemake RA 3:8:11, Eris–Makemake Dec 1:2:3.
  - Chiron–Gonggong RA φ 0.008%; Haumea–Rahu, Haumea–Uranus (φ triangle), Haumea–Transpluto; Mars–Pluto; Sedna–Vesta, Chiron–Vesta; new: Ketu–Pallas Flat 8:9:16.

#### Gonggong at 20:30 (RA 329.286, Dec −20.807)
- Numbers: 2 whole (vs ~1.7) + 6 ninths (vs ~5.8), all in Sky/Flat, mostly long-holding: Sky to Antares whole 74 (09:10–23:26); Sky to NEPTUNE whole 48 (18:42–23:27, Neptune's); Sky to Arcturus 1077/9 (07:04–24:00), Capella 1066/9 (10:39–24:00), Bellatrix 1015/9 (06:01–22:22); Flat to Aldebaran 958/9 (14:56–24:00); birth hour: Sky to JUPITER 550/9 (20:06–20:41), to Chiron 1061/9.
- Chords with the stars — the tightest Dec set so far, all day: Alphecca–Bellatrix Dec 3:4:7, 0.001%; REGULUS–RIGEL Dec 5:8:13, 0.006% (0.003% at 24:00) — Saturn and Juno both hold Regulus–Rigel RA √2: three of his bodies on Regulus–Rigel; Deneb Algedi–Regulus Dec 1:6:7, 0.010% (0.001% at 24:00; Juno has Deneb Algedi–Regulus Dec too); Regulus–Sirius Dec 1:7:8 (Uranus has Regulus–Sirius Dec φ 0.000%); Aldebaran–Fomalhaut Dec φ (Sedna has Aldebaran–Fomalhaut Dec 3:8:11 — two bodies); Algol–Capella Sky 1:4:5 (Orcus has Algol–Capella Dec).
- With his own bodies: Jupiter–Mars RA 3:5:8, 0.018% — Sedna has Jupiter–Mars Dec 1:3:4: Jupiter–Mars held in RA by Gonggong and in Dec by Sedna; Ketu–Transpluto Dec 1:1:2 (Gonggong at their Dec midpoint; 0.009% at 24:00); Jupiter–Mercury Dec φ; Venus three times (Quaoar–Venus φ, Eris–Venus 1:1:2, Makemake–Venus 1:3:4); repeats: Chiron–Orcus RA φ 0.008%, Quaoar–Vesta, Eris–Sedna, Transpluto–Vesta, Makemake–Uranus.

#### Transpluto at 20:30 (RA 142.816, Dec +14.683) — tied to the Sun
- Numbers: 0 φ/√2/whole (vs ~1.7) + 6 ninths (vs ~5.8; Ketu/Rahu counted once) — at chance. Dec to Bellatrix 75/9 (all day); RA to Algol 862/9 (11:54–23:42); Flat to Haumea 377/9 (Haumea's); Sky to Makemake 265/9 (Makemake's); Sky to KETU 426/9 / Rahu 1194/9 (20:07–20:32, ends at birth); RA to Juno 1513/9 (19:10–20:30, Juno's).
- Chords with the stars: 16 but loose; tightest Castor–Rigel RA 5:6:11, 0.026%; Capella–Fomalhaut Dec √2 (Neptune has Capella–Fomalhaut RA √2 — same string, same family, two bodies); Aldebaran–Bellatrix RA 1:5:6; Spica–Vega RA 3:4:7.
- With his own bodies — the Sun chords, both 0.012%: Mercury–Sun RA 2:5:7 (Sun–Mercury–Transpluto RA 2:5:7 from the Sun read) and Ketu–Sun Sky 1:1:2 (Transpluto at the Sky midpoint of Sun and Ketu); also Mars–Sun Sky √2. Then: Makemake–Mercury RA 5:8:13; Orcus–Venus Dec 5:6:11 and Haumea–Orcus RA 2:5:7 (ORCUS twice); Juno–Neptune Dec 2:3:5 (the Juno–Neptune–Transpluto triangle); Gonggong–Ketu Dec 1:1:2 (Gonggong's midpoint); Chiron–Vesta, Gonggong–Vesta.
- Reads as: Transpluto's weight is in the Sun — it sits between Sun, Mercury and Ketu — and it touches the Orcus hub twice (no direct Sedna chord).

#### Nodes at 20:30 (Rahu RA 7.114 Dec +3.074; Ketu RA 187.114 Dec −3.074) — the true node moves, so most windows sit inside the birth hour
- Numbers: Rahu 9 ninths, all inside the birth hour — Dec to Betelgeuse 39/9 (19:58–21:06), Haumea 185/9, Uranus 239/9, SUN 183/9 (20:11–21:50), Eris 116/9; Flat to Pluto 1320/9; Sky to Transpluto 1194/9; Sky to Spica 1474/9; RA to Vesta 636/9. Ketu: Dec to SEDNA whole 7 (Sedna's); Flat to Alkaid whole 56 (12:41–23:15, the one long one); Sky to Bellatrix 75√2; Dec to SPICA 5φ and Sky to Spica 146/9; Dec to Polaris 831/9, Algorab 121/9, Vesta 210/9. Spica on both nodes (3 numbers). 3 φ/√2/whole + ~13 ninths across the pair.
- Chords with the stars: Ketu Antares–Procyon RA 5:6:11, 0.001%; Rahu Algol–Antares RA 1:3:4, 0.010%; Ketu Algol–Regulus RA 1:3:4, 0.015%; Rahu Alkaid–Fomalhaut Dec √2, 0.019%; Rahu Algorab–Antares RA 1:2:3, 0.020% — Antares three times in RA on the nodes; Regulus–Spica Dec 5:8:13 (Rahu).
- With his own bodies — VENUS on the nodal axis: Rahu–Venus / Ketu–Venus RA φ, 0.016% (Venus at the φ point of the axis); Orcus–Venus RA 5:6:11, 0.002% (Ketu); Makemake–Venus Dec 3:4:7, 0.006% (Rahu); Uranus–Venus RA 2:3:5 (Rahu). And SATURN–VENUS RA φ from both nodes: Venus to Rahu 68.747 / Ketu 111.253, Saturn to Rahu 111.177 / Ketu 68.823 — Venus and Saturn sit on the two φ points of the nodal axis, opposite each other (179.924 apart). Checked (Eddie: "significant"): it is a Venus–Saturn OPPOSITION in RA, exact at 21:50 on the birth day (0.076° at 20:30; −1.25° at 00:00, +0.13° at 24:00); Venus = Rahu + 68.75, Saturn = Ketu + 68.82 — the pair lies parallel to the nodal axis, Venus on Rahu's φ point and Saturn on Ketu's. Because they are opposite, once Venus is on a φ point Saturn is on the other. (Venus's Dec mirror is Neptune across the equator.)
- Others: Eris–Vesta Dec 3:4:7, 0.002% (Rahu); Mars–Quaoar Dec 4:5:9, 0.012% (Rahu); Sun–Transpluto Sky 1:1:2, 0.012% (Ketu); Saturn–Uranus Dec 1:8:9 (Ketu); Haumea–Orcus Dec 1:7:8 (Rahu); Orcus–Pallas Flat (Ketu).

### METHOD 1 SUMMARY — Lionel Messi's chart (24 Jun 1987, Rosario, read at 20:30)
**Two hubs**
- **SEDNA — the receiver by number.** Six of his own bodies land on Sedna by number, all inside the birth window: Venus Sky 27√2 (exact), Mercury Sky 41φ, Jupiter Sky φ⁶, Juno Flat 600/9, Vesta Dec 147/9, Ketu Dec whole 7 — all six found at 20:30 (CORRECTION: the overlap at 20:30 is built in by reading at 20:30, so it is not evidence for the time). Sedna's own numbers: 7 φ/√2/whole (vs ~1.7). Strings: Makemake–Sedna held by Vesta (1:1:2) and Neptune (4:5:9); Jupiter–Mars–Sedna; Chiron–Vesta–Sedna 0.009%.
- **ORCUS — the receiver by chord.** 19 of his bodies take part in Orcus chords. The MAKEMAKE–ORCUS string is held three times (Jupiter RA 3:8:11 all day, Ceres RA 3:8:11, Eris Dec 1:2:3 all day) — a stack built into the birth chart. Uranus Dec 18φ to Orcus (exact, 09:28–24:00) with Haumea closing a Dec φ triangle (all day). Sun (Sky 328/9) and Mercury (Flat 213/9) hit Orcus at the birth time.
**Venus — the busiest inner body, Orcus's partner**
- Orcus–Venus five ways: Ketu–Orcus–Venus RA 0.002%, Juno RA 1:2:3, Pluto Dec φ, Transpluto Dec, Saturn Dec φ.
- Two partners across a line: NEPTUNE contraparallel in Dec (exact 18:42) and SATURN in opposition in RA (exact 21:50), Venus and Saturn on the two φ points of the nodal axis.
- The DEC LINE: Venus +200/9, Betelgeuse +200/27, Juno ≈ 0, Neptune −22.21; Betelgeuse–Equator held by Venus (1:2:3, 0.001%) and Neptune (1:3:4).
**Transpluto — the Sun's partner**: Sun–Mercury–Transpluto RA 2:5:7 and Transpluto at the Sky midpoint of Sun and Ketu, both 0.012%; Orcus twice.
**Recurring stars**
- BETELGEUSE on most bodies (Sun Dec whole 16, Venus, Ceres 0.000%, Vesta, Uranus, Neptune ×3, Pluto, Eris, Haumea, Rahu) — but not at Orcus.
- REGULUS: Regulus–Rigel held by three (Saturn and Juno RA √2, Gonggong Dec 5:8:13 0.006%); Regulus–Sirius (Uranus φ 0.000%, Gonggong); Regulus–Vega (Pluto, Orcus, both φ); Betelgeuse–Regulus (Haumea 0.011%, Sedna).
- DENEB ALGEDI (Pluto, Chiron, Eris ×5, Sedna, Gonggong), VEGA (Jupiter ×6, Pluto, Chiron, Quaoar, Orcus), SPICA (Ceres, Pluto, Eris, Sedna, both nodes), ANTARES (three times on the nodes).
**Strings held by two or more bodies**: Regulus–Rigel (3); Capella–Fomalhaut (Saturn, Mars, Neptune, Transpluto — 4); Betelgeuse–Equator (Venus, Neptune); Altair–Deneb Algedi (Pluto Dec, Chiron RA); Alphecca–Deneb Algedi (Eris, Sedna); Alphecca–Altair (Pluto, Sedna); Aldebaran–Fomalhaut (Sedna, Gonggong); Betelgeuse–Regulus (Haumea, Sedna); Regulus–Vega (Pluto, Orcus). Aldebaran–Procyon Dec (Eris, all day) is the Exeter string.
**Tightest (≤0.002%)**: Ceres Betelgeuse–Spica 0.000%; Uranus Regulus–Sirius 0.000%; Venus Betelgeuse–Equator 0.001%; Gonggong Alphecca–Bellatrix 0.001%; Ketu Antares–Procyon 0.001%; Ketu–Orcus–Venus 0.002%; Eris–Rahu–Vesta 0.002%.
**Quiet**: Pallas, Quaoar (the Sun's whole 36; Mars–Quaoar–Rahu), Neptune on its own (its weight is the Venus mirror), Makemake (the other end of the Orcus and Sedna strings).
**Like Dettori**: a natal stack (his Makemake–Orcus; Dettori's hubs Haumea, Orcus, Sedna — Orcus and Sedna again).
**Carry to the transits**: the Dec line (Venus/Betelgeuse/Juno/Neptune); the Venus–Saturn opposition on the nodal φ points; Sedna and Orcus; the Makemake–Orcus string; Regulus–Rigel; Capella–Fomalhaut; Betelgeuse.

### METHOD 3 — the match sky on Messi's chart (Camp Nou, KO 20:45 CET; Eddie's 21:45 = mid-game; full time ≈ 22:37)
Wrapper m3m.sh (sunchords + numcheck + parallels + mmatch against Messi's natal chords at 20:30, saved in scratchpad/mnat/). No tuned layers run for this match. Goal minutes (25', 42', 49', 58', 84') not yet confirmed, so goal clock times are not used.
#### Sun (RA 348.472, Dec −4.953 at KO)
- Numbers at KO: RA to Algorab = whole 161 (161.0014); RA to Altair 457/9; RA to Arcturus 1211/9; Dec to Polaris 848/9; Dec to course latitude 417/9 — 1 whole + 4 ninths (chance 0.44 and 1.5): above chance. No Sun parallel to a natal Dec.
- **MID-GAME — the Sun on his Venus/Neptune strings, 21:40–21:43:**
  - 21:40:05 Dec Betelgeuse–Fomalhaut 1:2:3 — natal Venus 2:5:7 (0.025%) and Neptune 1:4:5 (all day) on the same string
  - 21:40:43 RA Alkaid–Antares 2:5:7 exact
  - 21:41:31 Dec Equator–Fomalhaut 1:5:6 — natal Venus 3:4:7 (0.031%), Neptune 1:3:4 (all day)
  - 21:42:20 Dec Alkaid–Arcturus 4:5:9 — natal Ceres 2:3:5 (all day)
  - **21:43:03 Dec BETELGEUSE–EQUATOR 1:√2:1+√2 — natal Venus 1:2:3 (0.001%) and Neptune 1:3:4 (all day): the Dec line string itself.**
  - Four exact chords in under 3 minutes, all one Sun Dec (≈ −4.94) against the fixed stars; three of them are Venus's and Neptune's Dec strings. Two minutes before Eddie's 21:45.
- Around KO: Dec Deneb Algedi–Spica 4:5:9 exact 20:39:36 (5.4 min before KO; natal Haumea 1:7:8, loose); Dec Rigel–Sirius φ 20:53:11; Polaris–Sirius Dec 1:8:9 21:06:47; Altair–Castor Dec 3:5:8 21:10:12.
- Later: RA Aldebaran–Algol 3:8:11 exact 22:15:05 — natal ORCUS Aldebaran–Algol RA φ (all day); after FT: Altair–Deneb Algedi RA 22:49 (natal Chiron 0.015%, Pluto's string), Algorab–Pleiades Dec 23:18 (natal ORCUS 0.019%).
- Before KO: Betelgeuse–Spica Dec 1:2:3 at 19:28:46 — natal Ceres's 0.000% string.
#### Mercury (RA 3.808, Dec +4.187 at KO; moving in Dec, so its Dec chords come one after another)
- Numbers at KO: Dec to Algol = 26√2; Dec to REGULUS 70/9 — 1 + 1 (chance 0.44 / 1.5).
- In the match, on his natal strings (natal holder in brackets):
  - 20:49:41 Dec Alphecca–Betelgeuse 1:6:7 (Uranus 5:8:13, 0.019%, all day) — 5 min after KO
  - 21:18:23 Dec Algorab–Regulus (Ceres, Neptune all day, Mars)
  - 21:26:51 Dec Deneb Algedi–Regulus φ (Gonggong 0.010% all day, Juno)
  - **21:39:27 Dec Aldebaran–Castor 4:5:9 (ORCUS all day, Mars 0.039%)**; 21:39:43 Dec Alkaid–Fomalhaut 3:4:7 (Rahu 0.019%); 21:41:58 RA Algorab–Altair 3:5:8 exact — Mercury's own mid-game cluster, alongside the Sun's 21:40–21:43
  - **21:50:58 Dec REGULUS–RIGEL 5:8:13 — natal Gonggong makes the SAME chord, 5:8:13 (0.006%, all day)** — same string, same ratio; Regulus–Rigel is the string three of his bodies hold
  - **21:57:43 Dec Aldebaran–Spica 5:6:11 — natal SEDNA makes the SAME chord, 5:6:11 (all day)**
  - 22:00:31 Arcturus–Bellatrix (Venus φ 0.044%); 22:26:47 Algorab–Vega (Jupiter); 22:35:20 Fomalhaut–Spica (Juno)
  - 22:36:41 Dec Pleiades–Rigel (ORCUS 3:4:7, 0.021%, all day) — at full time
- Same chord as natal SEDNA five times on the day (Algol–Alphecca 5:8:13 06:32, Capella–Regulus φ 07:21, Alkaid–Pleiades 4:5:9 07:55, Fomalhaut–Sirius 5:8:13 18:50, Aldebaran–Spica 5:6:11 21:57) — the last one in the match.
- Before KO: Equator–Sirius 20:27 (Haumea 0.023% all day), Capella–Sirius 20:35 (Chiron all day).
#### Venus (RA 29.703, Dec +13.795 at KO)
- Numbers: Dec to RIGEL = whole 22 (22.0000 at KO; 22.035 at FT) — exact at kick-off. Only hit (chance 0.44). No parallel to a natal Dec.
- Before KO: RA Regulus–Rigel 2:3:5 exact 19:44:47 — natal Juno and Saturn both hold Regulus–Rigel RA √2 all day; RA Alkaid–Rigel φ 19:24:38 — natal Saturn the SAME chord (φ, 0.116%).
- In the match, on his natal strings:
  - 20:55:16 Dec Alphecca–Altair 3:8:11 (Pluto 2:5:7, 0.004%, all day) — 10 min in
  - 21:20:55 RA Algol–Fomalhaut 2:5:7 (Saturn √2)
  - 21:23:31 Dec Antares–Capella 4:5:9 (Quaoar φ 0.036% all day; Chiron); 21:26:35 Dec Alphecca–Regulus 1:8:9 (Quaoar all day)
  - **21:32:20 Dec Algol–Fomalhaut 5:8:13 (Pluto, Gonggong, ORCUS — three natal bodies, all day)**
  - 21:42:14 Dec Algol–Betelgeuse φ (Mars) — mid-game again; 21:46:17 RA Alkaid–Betelgeuse 1:2:3 exact (no natal RA link; natal Sun holds Alkaid–Betelgeuse in Dec, φ, all day)
  - 21:50:20 Dec Alphecca–Procyon 2:3:5 — natal Chiron the SAME chord (2:3:5, loose 0.119%)
  - 22:15:32 Dec Arcturus–Betelgeuse (Uranus φ, all day); 22:19:19 RA Polaris–Sirius 1:8:9 (Makemake 1:1:2 all day; natal Venus 2:3:5)
- Tightest of its own in the match (no natal link): Castor–Deneb Algedi RA 3:4:7 0.025% at 20:57:36; Deneb Algedi–Pleiades Sky 2:5:7 at 20:54:38.
#### Mars (RA 164.915, Dec +10.894 at KO; retrograde, just past opposition — slow, RA falling ~0.016°/h)
- **Mars sits on natal MAKEMAKE's RA (parallels: 164.915 vs 164.898/164.902, diff 0.017 at KO). Exact on Makemake's 20:30 RA (164.9015) at 21:38** — mid-game again. RA only (Mars Dec +10.9, Makemake +36.6).
- Because Mars is on Makemake's RA, it replays Makemake's natal RA chords — same string, same ratio:
  - 20:01:48 RA Arcturus–Vega 3:4:7 — natal Makemake 3:4:7 (all day); natal Jupiter 5:8:13 too
  - **20:55:48 RA Castor–Regulus 1:3:4 — natal Makemake 1:3:4 (0.039%, all day)**; Ceres 1:3:4 too — 11 min after KO (0.024% at KO)
  - 23:55:48 RA Algol–Capella 3:8:11 — natal Makemake 3:8:11; 00:17 (8 Mar) RA Polaris–Sirius 1:1:2 — natal Makemake's RA midpoint
- Makemake is the other end of his ORCUS string (Makemake–Orcus held by Jupiter, Ceres, Eris) — Mars now sits on that end through the match.
- Numbers at KO: RA to Arcturus = whole 49 (48.9997); RA to Algorab 203/9; RA to Altair 1195/9 — 1 + 2 (chance 0.44 / 1.5).
- Dec: Arcturus–Spica 3:8:11 exact 21:42:36 (mid-game; no natal link); Aldebaran–Regulus φ 20:37:48 and Bellatrix–Regulus φ 20:34:12 (just before KO; Mars 1.07° from Regulus in Dec).
#### Jupiter (RA 36.069, Dec +13.326 at KO)
- Numbers at KO: Dec to VEGA = 18√2; Dec to Pleiades 97/9 — 1 + 1 (chance 0.44 / 1.5).
- On his natal strings — three STACKS form with bodies already read:
  - **RA Aldebaran–Algol 1:2:3, 0.008%, exact 20:37:48 (7 min before KO)** — natal ORCUS's string (φ, all day). The Sun plays the same string at 22:15:05 → two sky bodies on Orcus's Aldebaran–Algol, one at KO, one late in the match.
  - **Dec Alphecca–Altair 1:3:4, exact 21:30:00** — natal PLUTO's string (2:5:7, 0.004%, all day). Venus played it at 20:55:16 → two sky bodies on Pluto's Alphecca–Altair in the first half.
  - **Dec Betelgeuse–Equator 4:5:9, exact 22:22:12** — the DEC LINE string (natal Venus 1:2:3 0.001%, Neptune 1:3:4 all day). The Sun played it at 21:43:03 → two sky bodies on the Dec-line string, mid-game and late.
- Others: RA Capella–Castor 4:5:9, 0.011%, exact 21:21:00 (natal Chiron, loose); Dec Aldebaran–Vega 1:7:8 exact 20:59:24 (natal Mars φ); before: RA Betelgeuse–Regulus 5:6:11 at 17:09 (natal Haumea 0.011% and Sedna, all day).
- **Eddie: where do the Sun and Jupiter hit the Venus–Neptune Dec line?** (V = natal Venus Dec +22.221; Neptune −V; natal Betelgeuse +V/3 = 200/27; natal Juno ≈ 0)
  - Sun at 21:43 (Betelgeuse–Equator √2, mid-game): Dec −4.937 = −2/9 of V (ratio −0.2222) = −2/3 of Betelgeuse — on Neptune's side of the equator; Sun to natal Juno Dec = 3φ (4.8556 vs 4.8541).
  - Jupiter at 22:22 (Betelgeuse–Equator 4:5:9): Dec +13.330 = 3/5 of V (ratio 0.5999) = 9/5 of Betelgeuse (≈120/9) — on Venus's side, between Betelgeuse and Venus.
  - So the line in units of V: Neptune −1 · Sun −2/9 · Juno 0 · Betelgeuse 1/3 · Jupiter 3/5 · Venus 1. The two transits divide his natal Venus–Neptune line in clean fractions, one each side of the equator.

#### EDDIE'S SPOTS — what came from what he gave (kept at his request, 7 Oct 15:28)
| Eddie gave | What we found |
|---|---|
| Birth time 20:30, Rosario | Read every body at 20:30. Sedna receives six of his bodies by number, and all six windows overlap 20:30–20:32 (a fit with his time, not a proof). |
| His engine time 21:45 = "middle of the game" (KO 20:45) | Sun, Mercury, Venus and Mars all strike between 21:38 and 21:46. Transit Mars sits on natal Makemake's RA, exact at 21:38. Sun on the Dec-line string at 21:43:03. Transit Venus–Jupiter RA gap reaches 57/9 at 21:43. |
| "Look at Neptune Dec and Venus Dec" | Venus +22.221 and Neptune −22.210 are contraparallel (exact 18:42 on the birth day). Venus Dec is 200/9; Betelgeuse at 200/27 is a third of it. Venus and Neptune hold Betelgeuse–Equator from both sides (1:2:3 and 1:3:4). |
| "Also Juno Dec" | Juno −0.082 sits near the centre of the Venus–Neptune line, 0.087 south of the exact midpoint; it is not inside a chord (0.8%). The Dec line: Venus +200/9 · Betelgeuse +200/27 · Juno ≈ 0 · Neptune −22.21. |
| "Venus–Saturn — significant" | Venus–Saturn opposition in RA (0.076° at 20:30, exact 21:50 on the birth day). Venus on Rahu's φ point, Saturn on Ketu's. |
| "What does it hit Venus–Neptune at" | Taking Venus's Dec as 1: the Sun strikes at 21:43 at −2/9 (Neptune's side; Sun to natal Juno Dec = 3φ); Jupiter strikes at 22:22 at +3/5 (Venus's side; 9/5 of Betelgeuse). Line: Neptune −1 · Sun −2/9 · Juno 0 · Betelgeuse 1/3 · Jupiter 3/5 · Venus 1. |
#### Saturn (RA 207.554, Dec −8.454 at KO; slow — its chords are held through the whole match)
- Numbers: Saturn's own RA = 1868/9 (207.5543). Only hit.
- **Held through the match (both under 0.01% from KO to FT):**
  - **Dec Capella–Regulus 3:5:8 — 0.003% at KO** (exact 19:56, 0.0033% at KO, ≈0.007% at FT) — natal SEDNA holds Capella–Regulus Dec φ all day: Saturn holds a Sedna string for the whole game.
  - RA Pleiades–Procyon 5:8:13 — 0.004% at KO (exact 18:51) — natal Orcus on the same string (1:5:6, loose 0.147%).
  - RA Aldebaran–Regulus 2:3:5 applying (exact in a day) — natal SEDNA Aldebaran–Regulus RA 1:3:4 all day.
- **That morning, Saturn played the Dec-line strings** — Betelgeuse–Fomalhaut 08:07, Equator–Fomalhaut 08:32, Bellatrix–Equator 08:43 (natal Venus 0.018–0.031%, Neptune all day). The same strings the Sun hit 21:40–21:43. Over the day: Saturn (morning) → Sun (mid-game) → Jupiter (22:22) on the Venus–Neptune strings.
- Also 04:24 Dec Deneb Algedi–Regulus (natal Gonggong 0.010%); Algol–Capella RA (Makemake, separating).
#### Ceres (RA 18.056, Dec +0.447 at KO — just north of the equator)
- Numbers: Dec to Vega 345/9 — 1 ninth (chance 1.5).
- **Before KO:** 19:45:36 Dec REGULUS–RIGEL 3:4:7 (natal Gonggong 5:8:13, 0.006%, all day) — Regulus–Rigel again; **20:07:12 Dec Betelgeuse–Spica 3:5:8 — natal CERES's own tightest string (4:5:9, 0.000%)**: sky Ceres on natal Ceres's string, 38 min before KO (same body both sides).
- In the match: Dec Procyon–Regulus √2 exact 21:10:12 and RA Capella–Vega φ exact 22:34:48 (at full time) — no natal link.
- Earlier on the day: 01:34 RA Aldebaran–Algol (natal ORCUS all day — now Jupiter, Sun and Ceres on it over the day); 04:56 Dec Betelgeuse–Fomalhaut (Venus/Neptune string); 17:14 Dec Alkaid–Betelgeuse (natal Sun φ and Neptune, all day; Ketu 0.033%).
#### Pallas (RA 336.190, Dec +0.148 at KO — on the equator)
- Numbers: Dec to Algorab 150/9; RA to Rigel 922/9; RA to Spica 1214/9 — 3 ninths (chance 1.5), above chance.
- **In the match: Dec REGULUS–RIGEL 1:√2:1+√2, exact 21:24:36 (40 min in)** — natal Gonggong 5:8:13, 0.006%, all day. Regulus–Rigel in the match now: Pallas 21:24, Mercury 21:50 (same chord as Gonggong); before KO Venus (RA) and Ceres.
- RA Alphecca–Polaris 3:5:8, 0.027%, exact 21:31:48 — no natal link.
- Before KO: Dec Alphecca–Procyon φ 20:07:12 (natal Chiron, loose); RA Alphecca–Vega 4:5:9, 0.016%, 20:03:36 (no link); RA Altair–Polaris 5:8:13 at 18:49 (natal Venus holds Altair–Polaris RA φ, 0.046%).
- Over the day, SEDNA strings four times: Alphecca–Altair RA φ 14:32 (the SAME chord as natal Sedna, φ 0.036%), Alphecca–Antares 17:32, Aldebaran–Betelgeuse 11:54, Bellatrix–Rigel 07:27.
#### Juno (RA 246.439, Dec −9.073 at KO)
- Numbers: Dec to Algorab 67/9 — 1 ninth (chance 1.5).
- **22:22:12 Dec CAPELLA–REGULUS φ, 0.020% at KO** — natal SEDNA's string (φ family too, all day). Saturn holds Capella–Regulus 3:5:8 the whole match → a STACK on Sedna's Capella–Regulus: Saturn throughout + Juno exact at 22:22. Same moment as Jupiter on the Dec-line string (Betelgeuse–Equator, 22:22:12).
- 22:00:36 Dec Arcturus–Deneb Algedi 1:4:5 — natal JUNO's own string (5:6:11, loose 0.106%): same body both sides.
- 22:16:48 Dec Bellatrix–Fomalhaut 3:4:7 — natal Mercury 3:8:11 (0.024%).
- Before KO: Dec Algol–Procyon 2:5:7, 0.018%, 19:47 (no link). Earlier in the day: SEDNA's Aldebaran–Fomalhaut 02:09 (Gonggong too) and Castor–Fomalhaut 02:28; Gonggong's Deneb Algedi–Regulus 07:58; Ceres's Betelgeuse–Spica 10:24; Orcus's Aldebaran–Castor 00:33.
#### Vesta (RA 6.594, Dec −2.779 at KO — just south of the equator, Neptune's side)
- Numbers at KO: Dec to Procyon = whole 8 (7.9990); Dec from the equator 25/9; RA to Algol 364/9; Dec to Capella 439/9; Dec to Castor 312/9 — 1 + 4 (chance 0.44 / 1.5), above chance.
- **21:03:00 Dec BETELGEUSE–EQUATOR 3:8:11 — the Dec-line string (natal Venus 1:2:3 0.001%, Neptune 1:3:4 all day), 18 min in.** Vesta's Dec then = −2.777 = −1/8 of natal Venus's Dec (ratio −0.1250; −3/8 of Betelgeuse). The line now: Neptune −1 · Sun −2/9 (21:43) · Vesta −1/8 (21:03) · Juno 0 · Betelgeuse 1/3 · Jupiter 3/5 (22:22) · Venus 1. In the match the Dec-line string is struck three times: Vesta 21:03, Sun 21:43, Jupiter 22:22 (Saturn in the morning).
- 20:43:12 Dec Alphecca–Regulus 1:1:2, 0.002% (2 min before KO) — Vesta at the Dec midpoint; natal QUAOAR holds Alphecca–Regulus (3:5:8, all day).
- 20:50:24 Dec Arcturus–Spica φ, 0.013% (5 min in) — no natal link. 20:09 RA Algorab–Altair 5:8:13, 0.015% — no link.
- Later: 22:54 Dec Aldebaran–Procyon (natal Eris all day — the Exeter string); 23:27 RA Aldebaran–Regulus (natal SEDNA all day; Saturn applying to it too). Earlier: Juno's Algol–Sirius RA 3:4:7 at 07:04 — the SAME chord as natal Juno (0.003%); Makemake's Arcturus–Vega 3:4:7 at 05:25 — the SAME chord as natal Makemake (Mars played it at 20:01).
#### Uranus (RA 3.375, Dec +0.708 at KO; slow — held all match)
- Numbers: Dec to ALPHECCA = whole 26 (26.0020 at KO → 26.0003 at FT — closing to exact at full time); Dec to Fomalhaut 273/9 — 1 + 1.
- Held through the match (slow, deviation barely changes):
  - Dec Algol–Polaris 5:6:11, 0.026% — natal URANUS's own string (3:4:7, all day): same body both sides, all game.
  - RA Capella–Fomalhaut 1:4:5, 0.094% — the four-body natal string (Mars RA 0.019%, Sedna RA, Neptune RA; Saturn and Transpluto in Dec).
  - Dec Aldebaran–Procyon 2:5:7, 0.087% — natal Eris (all day; the Exeter string).
  - Applying: Antares–Capella Dec (natal Quaoar φ all day), Alkaid–Fomalhaut Dec (natal Rahu 0.019%).
- Earlier: 07:34 Dec Aldebaran–Spica (natal SEDNA — Mercury played Sedna's same chord on it at 21:57); 17:39 Dec Bellatrix–Equator (Venus's equator cluster).
#### Neptune (RA 333.308, Dec −11.611 at KO; slowest of the planets — background holds)
- Numbers: Dec to Sirius 46/9 — 1 ninth (chance 1.5).
- Held through the match (all loose-to-medium, slow):
  - RA Antares–Polaris 3:4:7, 0.090% — natal NEPTUNE's own string (1:4:5, loose) and natal Uranus (0.051%).
  - Dec Alkaid–Procyon φ, 0.061% — natal Saturn (3:5:8, all day).
  - Dec Alphecca–Regulus 5:8:13, 0.067% — natal QUAOAR (all day); Vesta sat at its Dec midpoint at 20:43 → a small stack on Quaoar's Alphecca–Regulus.
  - Dec Algol–Arcturus √2, 0.083% — natal Eris (all day); Dec Arcturus–Betelgeuse φ — natal Uranus φ (same family).
- Tightest of its own: RA Betelgeuse–Pleiades φ, 0.022% (no natal RA link; natal Ceres holds Betelgeuse–Pleiades in Dec).
- Reads as: Neptune sits in the background on Saturn, Quaoar, Eris and Uranus strings; nothing sharp in the match.
#### Pluto (RA 279.613, Dec −19.253 at KO; near-stationary)
- **Numbers: Dec to SPICA = 5φ (8.0897 vs 8.0902; unchanged through the match)** — the same number natal KETU makes to Spica (Dec 5φ). Same star, same number, natal node and transit Pluto.
- Held: Dec Altair–Deneb Algedi 1:8:9, 0.062% — natal PLUTO's own string (2:5:7, 0.016%, all day; Chiron holds it in RA): same body both sides. Dec Betelgeuse–Rigel √2, 0.090% — natal Saturn (all day). Flat Fomalhaut–Spica 5:6:11 (natal Saturn). RA Algorab–Castor (natal Pallas 0.035%), RA Deneb Algedi–Fomalhaut (natal Gonggong) — loose, applying.
- Tightest of its own: Dec Capella–Procyon 3:5:8, 0.019% (applying, no natal link).
#### Chiron (RA 335.633, Dec −4.423 at KO)
- Numbers: RA to Rigel = whole 103 (103.0019 at KO → 102.9972 at FT; passes exact ≈21:30, mid-first-half). Rigel again (Venus Dec whole 22 to Rigel at KO).
- Held through the match (applying to exact after FT, all under 0.1%):
  - Dec Alphecca–Antares √2, 0.030% — natal SEDNA (3:4:7, all day).
  - Dec Capella–Fomalhaut 1:2:3, 0.039% — the four-body natal string (Transpluto 0.031% and Saturn 0.037% in Dec; Mars, Sedna, Neptune in RA). Uranus holds it in RA in the sky too.
  - Dec Deneb Algedi–Polaris 1:8:9, 0.042% — natal SUN (3:5:8, 0.047%, all day) and Makemake (1:1:2, all day).
  - RA Deneb Algedi–Polaris 1:7:8, 0.090% — natal Pluto and ORCUS (all day), Saturn.
  - Dec Regulus–Sirius 3:4:7, 0.071% — natal Uranus (φ, 0.000%) and Gonggong.
  - RA Capella–Castor 1:3:4 — natal CHIRON's own string (loose): same body both sides.
- Earlier: 00:44 Dec Betelgeuse–Equator — the Dec-line string (over the day: Chiron 00:44, Ceres 04:56 Betelgeuse–Fomalhaut, Saturn 08:07–08:43, Vesta 21:03, Sun 21:43, Jupiter 22:22).
#### Eris (RA 24.766, Dec −3.830 at KO; stationary for the match)
- **Natal (20:30: RA 22.542, Dec −9.816) to transit Eris (Eddie asked):** RA 2.2240 · Dec 5.9867 · Flat 6.3864 · Sky 6.3806 at KO (FT: 2.2245 · 5.9870 · 6.3870 · 6.3811). RA = 20/9 (2.2222, off +0.0018 at KO — inside ±0.002 at KO, just outside by FT); Dec 0.013 short of whole 6 (outside tolerance); Flat and Sky no clean number.
- Numbers to stars: Dec to Arcturus = whole 23 (23.0019); Dec to SPICA 66/9 (7.3333, exact) — Spica again (Pluto Dec 5φ to Spica; natal Ketu Dec 5φ to Spica); RA to Regulus 1146/9 — 1 + 2, above chance.
- Held through the match:
  - RA Altair–Capella 5:8:13, 0.024% — natal ERIS's own string (2:3:5, all day): same body both sides (now Uranus, Neptune, Pluto, Chiron, Eris all on their own natal strings).
  - Dec Alphecca–Bellatrix 1:2:3, 0.033% — natal GONGGONG's tightest string (3:4:7, 0.001%, all day); natal Jupiter too.
  - Dec Fomalhaut–Sirius 1:1:2, 0.053% — natal SEDNA (5:8:13, all day); Eris at the Dec midpoint.
  - Dec Altair–Pleiades 5:6:11, 0.016% — natal Transpluto (φ, all day).
  - RA Arcturus–Vega φ — natal Makemake and Jupiter (all day).
#### Sedna (RA 52.656, Dec +6.785 at KO; fixed for the match — its chord deviations do not change in the game, so they are held, not timed)
- Natal (20:30: RA 41.252, Dec +3.927) to transit Sedna: RA 11.404 · Dec 2.857 · Flat 11.757 · Sky 11.707 — no clean number. No number hits to stars either (chance 0.44 / 1.5).
- **Dec ALPHECCA–ANTARES 3:5:8, 0.023% — natal SEDNA's own string (3:4:7, all day): transit Sedna on natal Sedna's string.** Transit Chiron holds the same string (√2, 0.030%) all match → a STACK on natal Sedna's Alphecca–Antares: sky Sedna + sky Chiron (and Vesta 16:27, Pallas 17:32 earlier in the day).
- **Dec ALGOL–POLARIS √2, 0.032% — natal URANUS's own string (3:4:7, all day). Transit Uranus holds it too (5:6:11, 0.026%)** → a stack on natal Uranus's string: sky Uranus + sky Sedna.
- RA Algol–Pleiades 3:4:7, 0.002% (tightest; no natal link). Capella–Sirius in RA (natal Saturn, Jupiter) and Dec (natal Chiron).
- So the hub: sky Saturn holds Sedna's Capella–Regulus all match (Juno exact 22:22); sky Sedna and sky Chiron hold Sedna's Alphecca–Antares; Mercury matched Sedna's chord at 21:57; Eris holds Sedna's Fomalhaut–Sirius.
#### Haumea (RA 208.284, Dec +18.443 at KO; fixed for the match)
- Natal (20:30: RA 183.739, Dec +23.629) to transit Haumea: RA 24.544 · Dec 5.186 · Flat 25.086 · Sky 23.455 — no clean number.
- Numbers to stars — well above chance (1 whole + 5 ninths vs 0.44 / 1.5): RA to Bellatrix = whole 127 (127.0004 at KO → 126.9993 at FT, passes exact in the match); Dec from the equator 166/9; RA to Capella 1162/9; Dec to Capella 248/9; Dec to Castor 121/9 (exact at FT); Dec to Procyon 119/9.
- **Dec BETELGEUSE–RIGEL √2, 0.007% (held all match)** — natal SATURN's string (5:6:11, all day). Transit Pluto holds Betelgeuse–Rigel Dec √2 too (0.090%) → a stack on natal Saturn's Betelgeuse–Rigel: sky Pluto + sky Haumea, same chord.
- Also: Alphecca–Procyon Dec (natal Chiron, loose); Alphecca–Betelgeuse Dec (natal Uranus 0.019%, separating); Castor–Pleiades RA 3:5:8, 0.008% (no natal link).
#### Makemake (RA 190.698, Dec +27.493 at KO; fixed for the match — 17 Dec chords, many very tight)
- Natal (20:30: RA 164.902, Dec +36.581) to transit Makemake: RA 25.797 · Dec 9.088 · Flat 27.350 · Sky 23.586 — no clean number. Numbers to stars: Dec to course latitude 125/9 only.
- Held all match, on his natal strings:
  - **Dec Aldebaran–Castor 2:5:7, 0.019% — natal ORCUS (√2, all day) and Mars (0.039%).** Mercury struck the same string at 21:39 → Orcus's Aldebaran–Castor: sky Makemake holding + Mercury at mid-game. With sky Mars on natal Makemake's RA (exact 21:38), the Makemake–Orcus pair is lit from both ends: sky Mars on natal Makemake, sky Makemake on natal Orcus's string.
  - Dec Algol–Arcturus φ, 0.001% — natal Eris (3:4:7, all day); sky Neptune on it too (√2, 0.083%) → stack on Eris's Algol–Arcturus.
  - Dec Alkaid–Fomalhaut φ, 0.006% — natal Rahu (√2, 0.019%); Mercury struck it at 21:39:43 → Makemake holding + Mercury at mid-game.
  - Dec Alkaid–Deneb Algedi 1:2:3, 0.020% — natal Pluto (0.032%, all day), Venus.
  - Dec Arcturus–Betelgeuse √2, 0.008% — natal Uranus (φ, all day).
  - Looser: Algol–Capella Dec (natal Orcus 0.022%), Betelgeuse–Sirius (Eris), Alkaid–Arcturus (Ceres), Deneb Algedi–Polaris (natal Sun, Makemake).
#### Quaoar (RA 263.800, Dec −15.653 at KO; fixed for the match)
- Natal (20:30: RA 229.804, Dec −12.596) to transit Quaoar: RA 33.996 (0.004 short of whole 34 — outside tolerance) · Dec 3.057 · Flat 34.133 · Sky 33.075.
- Numbers to stars: Dec to Bellatrix = whole 22 (22.0011) — a second "22" (Venus Dec to Rigel whole 22 at KO); Dec to Antares 97/9.
- Held all match, on his natal strings:
  - RA Sirius–Spica 5:8:13, 0.019% — natal SEDNA (3:5:8, 0.035%, all day).
  - RA Alkaid–Procyon φ, 0.018% — natal SEDNA (4:5:9, all day). Two Sedna strings from Quaoar.
  - Dec Algol–Arcturus 5:8:13, 0.087% — natal ERIS (all day): now three sky bodies on Eris's Algol–Arcturus (Makemake 0.001%, Neptune, Quaoar).
  - Dec Equator–Procyon 1:3:4 (natal Makemake, all day); Dec Algol–Equator φ (natal Sun 3:4:7, 0.042%).
  - RA Altair–Bellatrix φ, 0.008% (natal Jupiter, loose).
#### Orcus (RA 147.775, Dec −7.275 at KO; fixed for the match) — quiet on his chart
- Natal (20:30: RA 126.431, Dec +5.642) to transit Orcus: RA 21.343 · Dec 12.917 · Flat 24.948 · Sky 24.907 — no clean number.
- Numbers: Dec to SPICA 35/9 (3.8879) — Spica a third time in transit (Pluto Dec 5φ, Eris Dec 66/9, Orcus Dec 35/9; natal Ketu Dec 5φ).
- Own tight chords, no natal link: Dec Antares–Fomalhaut 1:6:7, 0.007%; Dec Aldebaran–Regulus φ, 0.015% (natal Sedna holds Aldebaran–Regulus in RA, not Dec); Dec Algorab–Castor φ, 0.031%.
- On his strings only loosely: Algorab–Arcturus RA (natal Quaoar 0.053%), Arcturus–Regulus Dec (Juno), Alkaid–Polaris Dec (Mars).
- Reads as: sky Orcus does not hold natal Orcus's strings. Natal ORCUS is lit by others — Jupiter (KO), Ceres and the Sun on Aldebaran–Algol; Mercury (21:39) and sky Makemake (all match) on Aldebaran–Castor; Venus on Algol–Fomalhaut (21:32); Mercury on Pleiades–Rigel at FT; and sky Mars on the Makemake end (21:38).
#### Gonggong (RA 334.857, Dec −13.789 at KO; fixed for the match)
- Natal (20:30: RA 329.286, Dec −20.807) to transit Gonggong: RA 5.571 · Dec 7.017 (0.017 past whole 7 — outside) · Flat 8.960 · Sky 8.802.
- Transit Gonggong's RA is 0.150 from natal JUNO's RA (334.707) — near, not inside the 0.1 parallel check. (Transit Neptune 333.31, Chiron 335.63, Pallas 336.19 are also within 1.5° of natal Juno's RA.)
- Numbers: RA to Rigel 934/9; RA to SPICA 1202/9 (Spica a fourth time in transit).
- On his natal strings (applying/separating, loose-to-medium):
  - RA Antares–Arcturus φ, 0.042% — natal ORCUS the same family (φ, 0.049%, all day) and Uranus (0.040%).
  - RA Regulus–Rigel √2, 0.109% — the SAME chord natal Juno and Saturn hold all day (√2); separating.
  - RA Pleiades–Procyon √2 (natal Orcus, loose; sky Saturn 0.004% on it); Dec Fomalhaut–Procyon 5:6:11, 0.036% (natal Mars).
#### Transpluto (RA 151.400, Dec +11.724 at KO; fixed for the match)
- Natal (20:30: RA 142.816, Dec +14.683) to transit Transpluto: RA 8.585 · Dec 2.958 · Flat 9.080 · Sky 8.864 — no clean number.
- Numbers: Dec to SPICA 206/9 (Spica a fifth time in transit: Pluto, Eris, Orcus, Gonggong, Transpluto); RA to Sirius 451/9.
- **Dec ALGOL–FOMALHAUT √2, 0.018% (held all match)** — the string natal Pluto, Gonggong and ORCUS all hold (all day). Venus struck it at 21:32 → Transpluto holding + Venus striking, on a three-body natal string that includes Orcus.
- RA Algol–Fomalhaut 3:5:8, 0.023% — natal Saturn holds Algol–Fomalhaut in RA (√2): the same pair of stars in both RA and Dec.
- Looser: Antares–Spica Dec (natal Neptune φ), Altair–Spica Dec (natal Venus 0.014%; 0.142% here), Algorab–Pleiades RA (natal Chiron).
#### Nodes (transit Rahu RA 246.915 Dec −21.742; Ketu RA 66.915 Dec +21.742 at KO; RA falling ~0.017° over the match)
- **Natal Rahu (RA 7.114) to transit Rahu: RA = 85√2 (120.2082), exact at 21:46** (off −0.009 at KO) — mid-game again (same for Ketu–Ketu). Dec 24.816, Flat 122.73, Sky 119.11 — no number.
- **Transit Rahu to natal KETU: Dec = 168/9 (18.6667) — inside tolerance the whole match, exact at 22:06.**
- At KO: transit Rahu RA to Arcturus = whole 33 (exact 20:44, one minute before KO; Ketu whole 147, the same fact); Rahu RA to Altair 457/9 — the SAME number as the Sun's RA to Altair at KO: Altair sits at the RA midpoint of the Sun and Rahu (exact 20:48). Ketu Dec to Regulus 88/9; RA ninths to Algorab, Altair.
- Own tight chords just before KO, no natal link: Ketu RA Altair–Vega 1:7:8, 0.006% (19:54); Ketu Dec Alkaid–Vega φ, 0.006% (20:00); Rahu Dec Bellatrix–Regulus 1:5:6, 0.014%.
- On his strings (loose): Rahu on Haumea/Sedna's Betelgeuse–Regulus RA, Sedna's Aldebaran–Spica Dec, Gonggong's Deneb Algedi–Regulus Dec; Ketu on Saturn's Alkaid–Procyon (exact 12:24, the SAME chord 3:5:8 as natal Saturn) and Mars/Haumea's Bellatrix–Sirius.

### METHOD 3 SUMMARY — the match sky on Messi's chart (KO 20:45, mid-game ≈21:45 per Eddie, FT ≈22:37; goal minutes still to confirm)
**1. The two hubs, two ways**
- SEDNA is HELD: Saturn on Capella–Regulus 0.003% → 0.007% all match (Juno strikes it at 22:22); sky Sedna + sky Chiron on Sedna's OWN Alphecca–Antares; Eris on Fomalhaut–Sirius; Quaoar on Sirius–Spica and Alkaid–Procyon; Mercury plays Sedna's exact chord on Aldebaran–Spica at 21:57.
- ORCUS is STRUCK (sky Orcus itself is quiet): Jupiter Aldebaran–Algol 0.008% at 20:37 (Sun again 22:15); Venus Algol–Fomalhaut 21:32 under Transpluto's hold (0.018%; Pluto and Gonggong share it); Mercury Aldebaran–Castor 21:39 under sky Makemake's hold (0.019%); Mercury Pleiades–Rigel at FT; and sky MARS exact on natal MAKEMAKE's RA at 21:38 — the Makemake–Orcus string lit from both ends.
**2. The Dec line (Eddie's) — struck through the day, three times in the match** (units of natal Venus Dec): Neptune −1 · Sun −2/9 (21:43) · Vesta −1/8 (21:03) · Juno 0 · Betelgeuse 1/3 · Jupiter 3/5 (22:22) · Venus 1. Also Chiron 00:44, Ceres 04:56, Saturn 08:07–08:43.
**3. Timing — three windows**
- Around KO (20:37–20:55): Jupiter on Orcus 20:37; Vesta at the Alphecca–Regulus midpoint 20:43 (Quaoar); Rahu RA to Arcturus whole 33 at 20:44; Venus Dec to Rigel whole 22 at KO; Altair at the Sun–Rahu RA midpoint 20:48; Mars replays Makemake's Castor–Regulus 1:3:4 at 20:55; Venus on Pluto's Alphecca–Altair 20:55.
- MID-GAME 21:38–21:46 (Eddie's 21:45): Mars on natal Makemake 21:38; Mercury on Orcus's Aldebaran–Castor 21:39 and Rahu's Alkaid–Fomalhaut 21:39; Sun Betelgeuse–Fomalhaut 21:40, Alkaid–Antares 21:40, Equator–Fomalhaut 21:41, Alkaid–Arcturus 21:42, BETELGEUSE–EQUATOR (Dec line) 21:43; Venus Algol–Betelgeuse 21:42; transit Venus–Jupiter RA 57/9 21:43; natal→transit Rahu RA 85√2 21:46.
- Second half: Mercury Regulus–Rigel (Gonggong's chord) 21:50 and Aldebaran–Spica (Sedna's chord) 21:57; transit Rahu → natal Ketu Dec 168/9 22:06; Sun on Orcus 22:15; Juno 22:16; 22:22:12 — Jupiter on the Dec line AND Juno on Sedna's Capella–Regulus at the same moment; Mercury on Orcus at FT; Uranus Dec to Alphecca whole 26 closing to exact at FT.
**4. Slow stacks held all match**: Pluto + Haumea on Saturn's Betelgeuse–Rigel (both √2); Makemake (0.001%) + Neptune + Quaoar on Eris's Algol–Arcturus; Uranus (RA) + Chiron (Dec) on the four-body Capella–Fomalhaut; Uranus + Sedna on Uranus's own Algol–Polaris; Eris on Gonggong's Alphecca–Bellatrix (0.001% natal).
**5. Same body both sides** (sky body on its own natal string): Uranus, Neptune, Pluto, Chiron, Eris, Sedna all match; Ceres 20:07 and Juno 22:00 as strikes.
**6. Recurring stars by number**: SPICA from five transit bodies (Pluto Dec 5φ — the same number as natal Ketu; Eris 66/9, Orcus 35/9, Gonggong 1202/9, Transpluto 206/9); RIGEL (Venus whole 22, Chiron whole 103, Gonggong 934/9, Haumea/Quaoar); REGULUS–RIGEL struck by Venus, Ceres, Pallas, Mercury.
**Against Method 1**: everything Method 1 named is lit — Sedna and Orcus (the hubs), the Makemake–Orcus string, the Dec line, Regulus–Rigel, Capella–Fomalhaut, Betelgeuse. Method 2 (tuned layers, the Moon) not run for this match.

### GOALS against the match sky (Eddie 16:52: goals 25', 42', 49', 58', 84'; allow 20 min for half time)
Clock used: KO 20:45; first half ends ≈21:31; 20-min break; second half from ≈21:50. Goal windows: G1 21:09–21:10 · G2 21:26–21:27 · G3 21:53–21:54 · G4 22:02–22:03 · G5 22:28–22:29. (± a minute or two for stoppage.) Slow-body "exact" times (Sedna, Haumea, Makemake) are held, not timed, and are left out.
- **Correction to the mid-game cluster: 21:38–21:46 falls in the HALF-TIME BREAK** (Mars on natal Makemake 21:38, the Sun's five chords ending on the Dec line 21:43, Rahu 85√2 21:46). Eddie's 21:45 is half-time on this clock.
- **G1 25' (21:09–21:10):** Sun Altair–Castor and Ceres Procyon–Regulus both exact 21:10:12; Sun Polaris–Sirius 21:06:47 — none on his strings. Nearest natal strike: Vesta on the Dec line at 21:03 (6 min before).
- **G2 42' (21:26–21:27) — a REGULUS cluster on his strings:** Pallas Regulus–Rigel 21:24:36 (Gonggong 0.006%); Venus Alphecca–Regulus 21:26:35 (Quaoar, all day); Mercury Deneb Algedi–Regulus 21:26:51 (Gonggong 0.010%, all day); Venus Antares–Capella 21:23:31 (Quaoar φ, all day). Gonggong twice, Quaoar twice, inside 3½ minutes.
- **G3 49' (21:53–21:54):** Mercury Regulus–Rigel 5:8:13 at 21:50:58 — the SAME chord as natal Gonggong (3 min before); Venus Alphecca–Procyon 2:3:5 at 21:50:20 — the same chord as natal Chiron; Mercury Aldebaran–Spica 5:6:11 at 21:57:43 — the SAME chord as natal SEDNA (4 min after).
- **G4 58' (22:02–22:03):** Mercury Arcturus–Bellatrix 22:00:31 (natal Venus φ 0.044%); Juno on natal JUNO's own string 22:00:36; Mercury Altair–Rigel 22:01:25 (Vesta, loose); transit Rahu → natal Ketu Dec 168/9 exact 22:06.
- **G5 84' (22:28–22:29):** Mercury Algorab–Vega 22:26:47 (natal Jupiter 0.055%); Mercury Altair–Regulus φ 22:26:58; Mars Betelgeuse–Procyon 22:25:48 — natal MARS's own string (1:7:8, 0.058%): sky Mars on natal Mars; six minutes earlier, 22:22:12, Jupiter on the Dec line and Juno on Sedna's Capella–Regulus together.
- Caution: Mercury has ~20 exact events in the match (one every ~5–6 min), so a Mercury strike within ±3 min of a goal is common by itself. What stands out is G2 (three Regulus strings on Gonggong and Quaoar in 2½ min from three bodies) and G3 (Mercury replaying Gonggong's and Sedna's own chords either side).
- The Moon (the clock) and the tuned layers (Method 2) are not yet run for this match.

### THE MOON — the clock (Moon RA 159.889 Dec +2.690 at KO → RA 160.672 Dec +2.277 at FT; near full)
- No Moon crossing of a natal Dec, |Dec| or RA during 19:45–23:15. (It passed natal Rahu's Dec, +3.074, ≈19:01, before the window.)
- **Moon strikes on his natal strings at the goals** (goal windows as above; natal holder in brackets):
  - **G1 25' (21:09–21:10): 21:09:43 Dec Deneb Algedi–Regulus 1:2:3 (GONGGONG 0.010%, all day; Juno)** — Mercury hits the same string at 21:26:51 (G2): Gonggong's Deneb Algedi–Regulus struck at goal 1 (Moon) and goal 2 (Mercury).
  - **G2 42' (21:26–21:27): 21:26:06 Dec Antares–Capella 3:4:7 (QUAOAR φ 0.036%, all day)** — Venus played the same string at 21:23:31. With Pallas, Venus and Mercury on Regulus strings (21:24–21:26), G2 has Quaoar ×3 and Gonggong ×2 inside three minutes.
  - G3 49' (21:53–21:54): Moon chords (Algol–Antares Dec, Polaris–Spica RA, Rigel–Spica RA √2) — none on his strings. (Mercury's Gonggong and Sedna chords sit either side, 21:50 and 21:57.)
  - **G4 58' (22:02–22:03): 22:03:59 Dec Regulus–Sirius 2:5:7 (URANUS φ 0.000%, all day; Gonggong 0.062%)** — Regulus again.
  - **G5 84' (22:28–22:29): 22:29:50 Dec Algol–Polaris 4:5:9 — natal URANUS's own string (3:4:7, all day), held all match by sky Uranus (0.026%) and sky Sedna (0.032%): the Moon strikes a held stack.**
  - Half-time: 21:39 Dec Antares–Polaris (natal Mercury 0.011%); 21:48:45 Dec Algol–Fomalhaut 1:1:2 — natal Orcus's SAME chord (1:1:2) on the string Transpluto holds all match (Venus struck it 21:32).
- Caution on chance: in the first half the Moon makes a natal-linked chord about every 2 minutes (≈8 with natal ≤0.05% in 40 min), so G1/G2 Moon hits could come by chance. In the second half it makes only ~5, and two of them fall within about a minute of G4 and G5 — one of them on a string held by two slow sky bodies.
- Regulus strings at the goals: G1 Moon (Deneb Algedi–Regulus), G2 Pallas/Venus/Mercury (Regulus–Rigel, Alphecca–Regulus, Deneb Algedi–Regulus), G3 Mercury (Regulus–Rigel, 3 min before), G4 Moon (Regulus–Sirius). Natal Gonggong holds three of these strings, Uranus and Quaoar one each.

## 75. DETOUR — the lottery chart (Eddie 7 Oct 17:06; a person Eddie knows, birth time known to be accurate; kept anonymous)
- Event: lottery draw, Saturday 18 Mar 2000, 20:30 Melbourne (AEDT, UTC+11 = 09:30 UT); location −37.8139, 144.9634, 21 m. Race id 20000318_melbourne_2030; sky every minute −60 to +150.
- Chart: born 23 Jun 1969, 11:05 Paris (France had no summer time in 1969: UTC+1 = hour 11.0833 in the natal file). Workbook from Eddie's Mac (charts v2.3, engine v2.2; Ascot stand-in at 09:30 GMT = the same instant) → setup_lotto.py. Wrapper m1l.sh.
- Note: born the day before Messi's birthday (different year), so the Sun sits on the same solstice band — some Sun strings repeat Messi's for that reason alone.
### Method 1 — the lottery chart (numbers, then chords), at 11:05
#### Sun (RA 92.379, Dec +23.424 — solstice, Dec steady)
- Numbers: long-holding — Dec to PLUTO 58/9 (00:00–18:04); Flat to VENUS 435/9 (05:38–19:44); Dec to Arcturus 38/9 (08:54–15:14; Messi's midday Sun had the same 38/9 — solstice). At the birth time only: Sky to CHIRON whole 85 (11:00–11:05); Flat to Arcturus 86√2 (11:03–11:08); Flat to Castor 206/9; Sky to Alphecca 1057/9; RA to Vesta 51/9 (10:57–11:06). 2 φ/√2/whole (vs ~1.7) + 7 ninths (vs ~5.8) — about chance. (Hits read at 11:05 always have windows that include 11:05 — that is not evidence for the time.)
- Chords with the stars: Capella–Castor Dec 3:5:8, 0.006% (Messi's Sun nearly had the same); Aldebaran–Spica Dec 1:4:5 (0.014% at 00:00); Alkaid–Betelgeuse Dec φ and Deneb Algedi–Polaris Dec 3:5:8 — the same two strings as Messi's Sun (solstice); Regulus–Sirius Dec 2:5:7.
- With own bodies: Jupiter–Makemake RA √2, 0.025% (birth hour); Eris–Venus Dec 1:3:4; Eris–Haumea Sky 5:6:11; Neptune–Quaoar RA φ; Juno–Quaoar Dec 1:8:9 (all day-ish).
#### Mercury at 11:05 (RA 68.794, Dec +18.581)
- Numbers: RA to the NODAL AXIS = whole 73 to Rahu / 107 to Ketu (one fact); Sky to Castor = 10φ³ (42.3623); Dec to Jupiter 149/9; Sky to Makemake 596/9 and RA to Makemake 667/9; RA to Vega 1346/9; Sky to Algorab 1096/9. 2 φ/whole (vs ~1.7) + 5 ninths (vs ~5.8) — about chance. Mercury moves ~1° a day, so all are birth-hour only.
- Chords with the stars: Alkaid–Procyon RA 1:2:3, 0.001%; Aldebaran–Pleiades Dec 3:8:11, 0.001% (Mercury 2.07° from Aldebaran in Dec); Deneb Algedi–Procyon Dec 5:8:13, 0.008%; Betelgeuse–Sirius RA 5:8:13; Capella–Polaris RA 1:3:4; Polaris–Vega Dec 2:5:7; Fomalhaut–Rigel Dec 4:5:9. Procyon three times.
- With own bodies: Orcus–Vesta RA 4:5:9, 0.002%; Chiron–Venus Flat 3:5:8, 0.017% (the Sun had Chiron–Venus RA and Sky whole 85 to Chiron); Ceres–Transpluto RA 3:5:8, 0.033%; VENUS three times (Chiron–Venus, Venus–Vesta Flat 3:4:7, Pallas–Venus Dec 4:5:9); Makemake–Pallas Dec; Ketu–Rahu Sky √2.
#### Venus at 11:05 (RA 44.976, Dec +13.984)
- Numbers: RA to Aldebaran = whole 24; Flat to SUN 435/9 (05:38–19:44, the Sun's); Dec to Alkaid 318/9 (10:54–11:14); RA to CHIRON 356/9; RA to Juno 1121/9; RA to Pleiades 107/9; Flat to Ceres 875/9, Spica 1425/9; Sky to Altair 939/9; Sky to the nodes 461/9 (Rahu) / 1159/9 (Ketu), one fact. 1 whole (vs ~1.7) + 9 ninths (vs ~5.8) — ninths above chance.
- Chords with the stars: Betelgeuse–Polaris RA 1:6:7, 0.008%; Deneb Algedi–Polaris Dec 2:5:7, 0.009% — the Sun holds Deneb Algedi–Polaris Dec 3:5:8: two bodies on one string; Arcturus–Sirius RA 1:2:3, 0.018%; Procyon–Spica Flat 4:5:9; Algol three times in Dec (Algol–Fomalhaut φ, Algol–Antares, Algol–Pleiades).
- With own bodies: Ceres–Rahu RA 4:5:9, 0.008%; CHIRON four times — Chiron–Mercury Flat 3:5:8 0.017% (Mercury's), Chiron–Eris RA 3:5:8 0.046%, Chiron–Sun RA 5:6:11, Chiron–Makemake Flat; Mercury–Vesta Flat 3:4:7; Eris–Sun Dec 1:3:4 (the Sun's); Mercury–Pallas Dec; Haumea–Makemake Dec 3:4:7.
- Building: CHIRON — Sun Sky whole 85 to Chiron, Mercury's Chiron–Venus, Venus RA 356/9 to Chiron + four Chiron chords.
#### Mars at 11:05 (RA 241.002, Dec −23.838; slow — Dec steady over the day)
- Numbers: Mars's own RA = whole 241 (241.0020, 11:05–11:33); Sky to Vega = 51√2 (10:16–11:24); Dec to Alphecca 455/9 (06:17–19:31); RA to Alkaid 307/9, Uranus 543/9, Transpluto 943/9; Sky to Gonggong 661/9. 2 whole/√2 (vs ~1.7) + 5 ninths (vs ~5.8).
- Chords with the stars: Alphecca–Betelgeuse Dec φ, 0.001% (all day — 0.024% / 0.007%); Algorab–Arcturus Sky 7:8:8, 0.022%; Arcturus–Rigel RA 1:5:6; Betelgeuse–Polaris Dec φ (all day; Venus holds Betelgeuse–Polaris in RA 0.008% — same pair of stars, two bodies); Deneb Algedi–Fomalhaut Dec 3:4:7 (0.015% at 24:00); Altair–Procyon Dec 1:8:9.
- With own bodies: Haumea–Saturn Dec φ, 0.030% (all day); URANUS three times — Ceres–Uranus RA 4:5:9 (0.040%), Neptune–Uranus Dec 1:3:4 (all day), Makemake–Uranus RA 5:8:13 (0.026% at 00:00); Chiron–Saturn Flat φ (0.028% at 24:00 — Chiron again); Neptune–Rahu Dec φ (0.025% at 00:00).

- **RULE (Eddie 7 Oct 17:57): a body's OWN RA as a number does not count** — RA has no fixed absolute start (the equinox point is a convention that moves), unlike Dec, which is measured from the equator. RA DISTANCES between bodies/stars still count. Own-RA hits set aside: lottery Mars whole 241 (Mars recount: 1 √2 + 5 ninths); earlier Messi Sun midday whole 93, Vesta own RA 55√2, Chiron own RA whole 83, transit Saturn own RA 1868/9.
#### Jupiter at 11:05 (RA 178.621, Dec +2.025)
- Numbers: RA to KETU = 2√2 (2.8272 — Jupiter 2.8° from Ketu in RA); Sky to Regulus 253/9; Sky to SEDNA 1303/9; RA to Sirius 696/9; Flat to Algol 1235/9; Dec to Mercury 149/9 (Mercury's). 1 √2 (vs ~1.7) + 5 ninths (vs ~5.8) — at chance.
- Chords with the stars: Algol–Bellatrix Dec 1:8:9, 0.021%; Aldebaran–Algol RA 1:5:6 (0.036%; 0.002% at 24:00); Algorab–Regulus RA 1:3:4; Algorab–Fomalhaut Dec √2 (0.049% at 24:00); Bellatrix–Regulus RA 3:8:11. Algol again (Venus ×3 in Dec), Regulus twice.
- With own bodies: Neptune–Transpluto Sky 3:4:7, 0.004% (and Flat 3:4:7 — same ratio in two measures); Ceres–Makemake Dec 3:4:7, 0.016%; Makemake–Sun RA √2, 0.025% (the Sun's); CHIRON–SATURN Dec 3:5:8, 0.026% — Mars holds Chiron–Saturn in Flat (φ): the same pair from two bodies; Orcus–Quaoar Dec 4:5:9, 0.035%; Gonggong–Haumea Dec 4:5:9.
#### Saturn at 11:05 (RA 34.995, Dec +11.499; slow)
- Numbers: Dec to QUAOAR = 14√2 (19.8004, 07:47–11:40); RA to Aldebaran = 21φ (10:40–11:46); RA to Orcus 667/9; Flat to Altair 876/9; Sky to Sirius 642/9. 2 φ/√2 (vs ~1.7) + 3 ninths (vs ~5.8).
- Chords with the stars: ALDEBARAN–PROCYON Dec 4:5:9, 0.000% (the Exeter string; Messi's Eris held it too); Alkaid–Pleiades Dec 1:2:3, 0.007%; Capella–Equator Dec 1:3:4, 0.018%; Procyon–Spica Dec φ, 0.030%; Bellatrix–Vega RA 2:5:7; Algol–Capella RA 3:8:11; Capella–Deneb Algedi Dec 4:5:9 (0.006% at 00:00).
- With own bodies — CHIRON four times: Chiron–Rahu Dec 4:5:9, 0.008%; Chiron–Jupiter Dec 3:5:8, 0.026% (Jupiter's); Chiron–Sedna Dec 5:8:13 (0.030% at 24:00); Chiron–Mars Flat φ (Mars's). So SATURN–CHIRON is held from Mars (Flat) and Jupiter (Dec), and Saturn itself sits on Chiron with Rahu, Jupiter, Sedna. Also Pallas–Sedna Dec 3:4:7, 0.024%; Haumea–Mars Dec φ (Mars's); Eris–Ketu Dec 3:5:8 (0.024% at 24:00).
#### Ceres at 11:05 (RA 316.451, Dec −26.208)
- Numbers: 0 φ/√2/whole (vs ~1.7) + 8 ninths (vs ~5.8) — ninths above chance, most holding 1–2 hours: Flat to Neptune 737/9 (10:15–12:02), Haumea 1427/9 (10:27–12:03), Vega 674/9 (10:34–12:40), Venus 875/9 (Venus's); RA to Polaris 731/9; Dec to Bellatrix 293/9; Sky to Algorab 1031/9, Juno 365/9.
- Chords with the stars: Aldebaran–Altair RA 1:6:7, 0.003%; Antares–Spica RA 2:3:5, 0.011% (all day); Algorab–Altair Dec φ, 0.027%; Pleiades–Procyon Dec 3:5:8, 0.027%; Alkaid–Regulus RA 1:2:3 (0.005% at 00:00).
- With own bodies (mostly the other side of chords already seen): Rahu–Venus RA 4:5:9, 0.008% (Venus's Ceres–Rahu); Jupiter–Makemake Dec 3:4:7 (Jupiter's); Mercury–Transpluto RA (Mercury's); Mars–Uranus RA (Mars's); new: Neptune–Uranus RA 2:3:5 (all day — Mars has Neptune–Uranus in Dec: same pair, two bodies); Pallas–Sedna Dec 4:5:9 (Saturn has Pallas–Sedna Dec 3:4:7: same pair, two bodies).
- Ceres is the first body with no Chiron chord.
#### Pallas at 11:05 (RA 273.173, Dec +24.332)
- Numbers: Sky to ALGOL = 63φ (101.9352); Dec to Haumea 6/9 (05:31–11:39); RA to Sirius 1547/9; Flat to Vesta 1562/9. 1 φ (vs ~1.7) + 3 ninths (vs ~5.8).
- Chords with the stars (19 — busy): Alphecca–Arcturus RA 1:2:3, 0.007%; Bellatrix–Fomalhaut Dec 1:2:3, 0.012% (all day); Bellatrix–Deneb Algedi Dec 4:5:9, 0.018% (all day); Arcturus–Sirius Dec 1:7:8, 0.020% — Venus holds Arcturus–Sirius in RA (0.018%): same pair of stars, two bodies; CAPELLA–POLARIS RA 1:3:4, 0.027% — Mercury makes the SAME chord (RA 1:3:4): two bodies, same chord; Antares–Betelgeuse Dec 1:2:3, 0.028%; Algol–Rigel RA φ, 0.028%. Polaris, Capella, Algol, Deneb Algedi recur.
- With own bodies — SEDNA three times: Saturn–Sedna Dec 3:4:7 (Saturn's), Eris–Sedna RA 1:8:9 0.025% (new), Ceres–Sedna Dec 4:5:9 (Ceres's) — the Pallas–Sedna pair is held from Saturn and Ceres; also Mercury–Venus and Makemake–Mercury Dec (Mercury's).
#### Juno at 11:05 (RA 280.420, Dec −4.774)
- Numbers: 0 φ/√2/whole (vs ~1.7) + 7 ninths (vs ~5.8), several long: Sky to Polaris 856/9 (03:56–13:07); Dec to Vega 392/9 (08:25–19:23); Flat to Capella 1500/9 (166.6662); RA to Venus 1121/9 (Venus's), Aldebaran 1337/9, Pleiades 1228/9; Sky to Ceres 365/9 (Ceres's). Also RA to CHIRON 85.002 — just outside ±0.002 of whole 85, the same 85 the Sun makes to Chiron (Sky): Chiron at 85 from two bodies.
- Chords with the stars: Antares–Pleiades Dec 3:4:7, 0.004% (all day); Equator–Sirius Dec 2:5:7, 0.012%; Regulus twice in Dec (Regulus–Vega, Regulus–Spica φ).
- With own bodies: Neptune–Quaoar RA 3:5:8, 0.025% — the Sun has Neptune–Quaoar RA φ: same pair, two bodies; CHIRON–MAKEMAKE RA φ, 0.040% (Venus has Chiron–Makemake Flat: same pair, two bodies); Pluto–Rahu RA 3:4:7; Quaoar–Sun Dec 1:8:9 (the Sun's Juno–Quaoar).
#### Vesta at 11:05 (RA 86.711, Dec +21.697)
- Numbers — above chance (4 φ/whole vs ~1.7): **Dec to TRANSPLUTO = whole 5 (10:26–13:27) and Dec to QUAOAR = whole 30 (10:34–14:07)** — so Quaoar–Transpluto is 25 apart in Dec: a whole-number set 5 / 25 / 30 (and the chord Quaoar–Transpluto Dec 1:5:6, 0.021%); Flat to Makemake = whole 59; RA to Gonggong = 76φ; ninths: Sky to Bellatrix 146/9, Fomalhaut 997/9; RA to Sun 51/9 (the Sun's), Flat to Pallas 1562/9 (Pallas's).
- Chords with the stars: Polaris–Regulus RA 3:4:7, 0.000%; ALGOL five times — Algol–Pleiades Dec 1:7:8 0.016%, Algol–Antares Dec 2:5:7 0.023%, Algol–Polaris RA φ 0.032%, Algol–Altair Dec 2:3:5 0.042%, Algol–Fomalhaut Dec 3:8:11 (Venus has Algol–Fomalhaut Dec φ, Algol–Antares and Algol–Pleiades Dec too: Venus and Vesta share three Algol strings); Altair–Fomalhaut Dec 1:3:4; Procyon–Sirius Dec 3:4:7.
- With own bodies: Mercury–Orcus RA 4:5:9, 0.002% (Mercury's Orcus–Vesta); Makemake–Rahu RA φ, 0.005%; Haumea–Sedna Dec 1:6:7, 0.012%; Quaoar–Transpluto Dec 1:5:6, 0.021%; Eris–Uranus RA √2, 0.035%; SEDNA three times (Haumea–Sedna Dec and RA, Gonggong–Sedna Flat). No Chiron chord from Vesta.
#### Uranus at 11:05 (RA 180.667, Dec +0.505 — on the equator; slow, held all day)
- In RA Uranus sits with JUPITER (178.621, 2.05° away) and KETU (Jupiter–Ketu RA 2√2) — the 1969 Jupiter–Uranus conjunction with the south node.
- Numbers (all long-holding): Sky to Alkaid = 38√2 (all day); Flat to ORCUS = whole 73 (05:52–15:00); RA to TRANSPLUTO 400/9 (00:00–21:55); Dec to Spica 105/9 (05:36–20:33); RA to Alkaid 236/9; Sky to Alphecca 515/9, Gonggong 1223/9; RA to Neptune 489/9, Mars 543/9 (Mars's). 2 √2/whole (vs ~1.7) + 7 ninths (vs ~5.8).
- Chords with the stars (all day): Pleiades–Spica RA 1:6:7, 0.001%; Aldebaran–Castor RA 2:3:5, 0.023%; Fomalhaut–Sirius Dec 3:4:7, 0.031%; Bellatrix–Procyon Dec φ (0.004% at 00:00).
- With own bodies (mostly seen from the other side): Ceres–Neptune RA 2:3:5 and Mars–Neptune Dec 1:3:4 — the NEPTUNE–URANUS pair seen from Uranus (held by Ceres in RA and Mars in Dec); Ceres–Mars RA (Mars's); Eris–Vesta RA √2 (Vesta's); Quaoar–Saturn Dec. No Chiron chord.
#### Neptune at 11:05 (RA 234.999, Dec −17.757; slow)
- Numbers — ninths above chance (2 φ + 8 ninths vs ~1.7 / ~5.8): Sky to Haumea = 49φ (09:40–12:51); RA to Castor = 75φ (10:14–14:46); Dec to Rigel 86/9 (00:00–22:26); CHIRON twice — Dec 210/9 (00:00–12:17) and Sky 1171/9; TRANSPLUTO twice — RA 889/9 and Sky 928/9; Flat to Ceres 737/9 (Ceres's), Deneb Algedi 826/9; RA to Uranus 489/9 (Uranus's).
- Chords with the stars: Algol–Betelgeuse Dec 3:4:7, 0.017% (all day) — Algol again; Alkaid–Betelgeuse Dec 3:5:8.
- With own bodies — TRANSPLUTO the theme: Jupiter–Transpluto Sky 3:4:7, 0.004% (Jupiter's Neptune–Transpluto); Makemake–Transpluto Dec 2:3:5, 0.031% (all day); Quaoar–Transpluto Sky 3:8:11 (with Vesta's whole-number Quaoar–Transpluto set); Juno–Quaoar RA 3:5:8 (Juno's Neptune–Quaoar); Neptune–Uranus seen from Neptune (Ceres–Uranus RA, Mars–Uranus Dec); Mars–Rahu Dec φ; Chiron–Haumea Dec 5:6:11.
- Slow layer building: TRANSPLUTO — Vesta Dec whole 5, Uranus RA 400/9, Neptune ×4 (two numbers, Jupiter–Transpluto, Makemake–Transpluto), Quaoar–Transpluto.
#### Pluto at 11:05 (RA 179.862, Dec +16.980; slow)
- **Pluto joins the RA cluster: Jupiter 178.621 · Pluto 179.862 · Uranus 180.667 · Ketu ≈181.45 — four points within ~2.8° of RA** (Dec differs: Pluto +17.0, Jupiter +2.0, Uranus +0.5).
- Numbers: Sky to Gonggong 1307/9 (145.2222, exact); Dec to Sun 58/9 (the Sun's, 00:00–18:04); Dec to Arcturus 20/9; RA and Flat to Aldebaran both 998/9. 0 φ/whole + 4 ninths — at chance.
- Chords with the stars: Alphecca–Altair Dec 5:6:11, 0.001%; Antares–Rigel RA 2:3:5, 0.011% (0.002% at 24:00, all day); Algorab–Betelgeuse Dec 2:5:7 (0.026% at 24:00); Castor–Vega RA 2:3:5.
- With own bodies (only 2): **CHIRON–TRANSPLUTO RA 1:3:4 (all day, 0.088–0.091%)** — the two hubs (Chiron for the inner bodies, Transpluto for the slow ones) joined on one chord through Pluto; Juno–Rahu RA (Juno's Pluto–Rahu).
#### Chiron at 11:05 (RA 5.422, Dec +5.578; slow) — the hub
- Numbers: Sky to SUN = whole 85 (the Sun's; Juno RA 85.002 just outside); NEPTUNE twice — Dec 210/9, Sky 1171/9 (Neptune's); RA to Venus 356/9 (Venus's); ninths to stars: RA Pleiades 463/9 (06:15–14:24), Castor 974/9; Dec Rigel 124/9; Flat Deneb Algedi 399/9; Sky Spica 1470/9. 1 whole + 8 ninths — ninths above chance.
- Chords with the stars (17): Polaris–Spica Dec 1:5:6 (0.001% at 00:00); Aldebaran–Alkaid Dec 1:3:4 (0.003% at 00:00); ALGOL four times (Algol–Castor RA 5:8:13 0.036%, Algol–Pleiades RA φ, Algol–Algorab Dec, Algol–Capella Dec); SPICA three times in Dec (Polaris–Spica, Equator–Spica 1:2:3, Regulus–Spica φ).
- With own bodies (15 — the receiver): SATURN four times — Rahu–Saturn Dec 4:5:9 0.008%, Jupiter–Saturn Dec 3:5:8 0.026%, Saturn–Sedna Dec 5:8:13, Mars–Saturn Flat φ; VENUS four times — Mercury–Venus Flat 0.017%, Eris–Venus RA 0.046%, Sun–Venus RA, Makemake–Venus Flat; also Juno–Makemake RA φ; TRANSPLUTO three times — Pluto–Transpluto RA 1:3:4, Sedna–Transpluto Dec 1:3:4, Quaoar–Transpluto Dec 4:5:9 (base 25.000 — Vesta's whole-number pair); SEDNA three times (Saturn–Sedna, Rahu–Sedna Dec 1:1:2, Sedna–Transpluto).
- Reads as: Chiron is the receiver of this chart — its partners Saturn and Venus, and it reaches the slow hub Transpluto three ways.
#### Eris at 11:05 (RA 20.250, Dec −14.322; stationary — everything holds all day)
- Numbers (all long): Dec to Alkaid = 45√2 (all day); Dec to Antares 109/9 (all day); Dec to Procyon 176/9 (all day); Flat to Arcturus 1527/9 (00:00–23:08); Flat to Antares 1201/9; RA to Altair 743/9; Sky to Rigel 517/9, Castor 903/9. 1 √2 (vs ~1.7) + 7 ninths (vs ~5.8) — ninths a little above chance, all holding the whole day.
- Chords with the stars (all day): Bellatrix–Pleiades RA 2:3:5, 0.004%; Pleiades–Vega Dec φ, 0.006%; Altair–Rigel RA √2, 0.007%; Castor–Rigel RA 3:5:8, 0.031%; Fomalhaut–Rigel Dec 2:5:7, 0.034% — RIGEL three times.
- With own bodies (mostly seen already): Pallas–Sedna RA 1:8:9 (Pallas's Eris–Sedna), Uranus–Vesta RA √2 (Vesta's), Chiron–Venus RA 3:5:8 (Venus's), Sun–Venus Dec 1:3:4 and Haumea–Sun Sky (the Sun's); new: Ketu–Orcus RA 3:4:7 (0.029% at 24:00); Ketu–Saturn Dec 3:5:8 (Saturn's Eris–Ketu); Chiron–Orcus RA 1:6:7.
#### Sedna at 11:05 (RA 33.632, Dec +1.876; fixed)
- Numbers: **Dec to DENEB ALGEDI = whole 18 (17.9997, all day)**; RA to Betelgeuse = 39√2 (07:42–23:34); REGULUS twice — Flat 1070/9, Sky 1056/9; Flat to Rigel 415/9; Sky to Jupiter 1303/9 (Jupiter's). 2 whole/√2 (vs ~1.7) + 4 ninths — the whole 18 to Deneb Algedi is the standout (it carries Deneb Algedi–Fomalhaut Dec 3:4:7 and Castor–Deneb Algedi Dec 3:5:8, all day).
- Chords with the stars (loose, 0.04–0.15%, all day): Procyon–Rigel Dec 1:3:4; Alphecca–Castor RA; Procyon–Sirius RA; Spica twice in Dec; Regulus–Rigel Dec 1:1:2 (Sedna at their Dec midpoint).
- With own bodies (all seen from the other side): PALLAS three times — Pallas–Saturn Dec, Eris–Pallas RA 0.025%, Ceres–Pallas Dec: the Pallas–Sedna pair is held by Saturn, Eris and Ceres; VESTA twice (Haumea–Vesta Dec 0.012%, Gonggong–Vesta Flat); CHIRON three times (Chiron–Saturn, Chiron–Rahu midpoint, Chiron–Transpluto Dec 1:3:4, 0.019% at 24:00).
#### Haumea at 11:05 (RA 166.392, Dec +24.99991; fixed)
- **Haumea's own Dec = whole 25 (24.99991 at 11:05; exact ≈10:50; within ±0.002 from ≈06:00 to ≈16:00)** — Dec counts (measured from the equator). (natnums' |Dec| line missed it; checked by hand.)
- **And Quaoar–Transpluto Dec = 24.99972 — also 25.** The Dec lattice: Haumea +25.000 · Vesta +21.697 · Transpluto +16.698 · equator 0 · Quaoar −8.302. Quaoar sits exactly 25 below Transpluto, as Haumea sits 25 above the equator; so Haumea–Transpluto (8.302) = Quaoar's distance from the equator (8.302). With Vesta: to Transpluto whole 5, to Quaoar whole 30.
- Other numbers: Dec to Capella = whole 21 (02:38–14:28); Sky to Neptune 49φ (Neptune's); Sky to Regulus 169/9 (all day); Flat Arcturus 431/9, Procyon 497/9; Dec Castor 62/9, Pallas 6/9 (Pallas's); Sky to the nodes 224/9 / 1396/9 (one fact); Flat Ceres (Ceres's).
- Chords with the stars: Castor–Vega Dec 1:1:2, 0.007% (Haumea at their Dec midpoint); Algol–Sirius RA 5:6:11, 0.010% (all day); Polaris–Regulus RA 1:8:9, 0.020% (Vesta holds Polaris–Regulus RA 3:4:7 at 0.000%: two bodies); Antares–Polaris Dec 4:5:9.
- With own bodies (mostly seen already): Sedna–Vesta Dec 1:6:7 0.012% (Vesta's); Mars–Saturn Dec φ 0.030% (Mars's); Ketu–Makemake RA 2:5:7 (0.013% at 24:00); Gonggong–Jupiter Dec 4:5:9; Chiron–Neptune Dec 5:6:11.
#### Makemake at 11:05 (RA 142.903, Dec +39.675; fixed)
- Numbers (few): Flat to ORCUS 377/9 (00:57–13:01); RA to the nodes 296/9 / 1324/9 (one fact, 10:21–14:27); Flat to Vesta whole 59 and Mercury ninths (theirs). 0 own φ/whole + 2 ninths — below chance.
- Chords with the stars (all day): Antares–Polaris Dec 3:4:7, 0.008%; Equator–Polaris Dec 4:5:9, 0.019% (0.006% at 24:00); Castor–Pleiades Dec 1:1:2, 0.025% (Makemake at their Dec midpoint); POLARIS three times.
- With own bodies (mostly seen already): Rahu–Vesta RA φ 0.005% (Vesta's); Ceres–Jupiter Dec 0.016% (Jupiter's); Neptune–Transpluto Dec 2:3:5 (Neptune's); Chiron–Juno RA φ (Juno's); new: Gonggong–Rahu Dec 3:5:8, 0.020% (0.009% at 24:00, all day); HAUMEA three times (Haumea–Ketu RA, Haumea–Venus Dec, Haumea–Uranus Dec).
- Reads as: Makemake is a supporting body — Polaris on its stars, Transpluto/Chiron/Rahu among its partners.
#### Quaoar at 11:05 (RA 207.740, Dec −8.302; fixed)
- Numbers — strong (4 whole/√2 vs ~1.7): **RA to GONGGONG = whole 116 (115.9999, all day)**; **Dec to TRANSPLUTO = whole 25 (00:00–20:27)**; Dec to Vesta = whole 30 (Vesta's); Dec to Saturn = 14√2 (Saturn's); RIGEL twice — RA and Flat 1162/9 (02:51–17:51); Flat to Orcus 912/9.
- Chords with the stars: Altair–Spica Dec 1:6:7 (0.010% at 24:00); Aldebaran–Procyon Dec 5:6:11, 0.031% (the Exeter string again — Saturn holds it at 0.000%: two bodies); BETELGEUSE five times (loose 0.05–0.14%); Algol three times.
- With own bodies — TRANSPLUTO five times: Transpluto–Vesta Dec 1:5:6 0.021% and Sky 5:8:13; Saturn–Transpluto RA √2; Neptune–Transpluto Sky; Chiron–Transpluto Dec 4:5:9 (base 25.000). Also Juno–Neptune RA 3:5:8 (Juno's); Jupiter–Orcus Dec 4:5:9 0.035% (Jupiter's).
- The Transpluto set is now: Haumea Dec 25.000; Quaoar–Transpluto Dec 25 (whole, all day); Vesta to Transpluto 5, to Quaoar 30; Quaoar–Gonggong RA whole 116 (all day); Uranus–Transpluto RA 400/9; Neptune ×4; Chiron ×3; Pluto's Chiron–Transpluto.
#### Orcus at 11:05 (RA 109.107, Dec +14.929; fixed)
- Numbers: Flat to Uranus whole 73 (Uranus's); Dec to Algorab 283/9 (01:50–24:00); Flat to Betelgeuse 195/9; Flat to Makemake 377/9 and Quaoar 912/9, RA to Saturn 667/9 (theirs). 0 new φ/whole + 2 new ninths.
- Chords with the stars (18): Algorab–Pleiades RA 2:3:5, 0.001%; Betelgeuse–Rigel RA 1:2:3, 0.017%; Pleiades–Vega Dec 5:8:13, 0.022% (0.005% at 00:00 — Eris holds Pleiades–Vega Dec φ 0.006%: two bodies); Algorab three times (Algorab–Alphecca Dec, Algorab–Capella RA φ, Algorab–Bellatrix Dec); Fomalhaut–Spica Dec √2; Capella–Deneb Algedi Dec 1:1:2 (Orcus at the midpoint).
- With own bodies (only 5, all seen already): Mercury–Vesta RA 0.002% (Mercury's), Jupiter–Quaoar Dec (Jupiter's), Eris–Ketu RA, Chiron–Eris RA, Eris–Mercury Dec. Orcus is busy with stars, light with its own bodies — unlike Messi, where Orcus was the hub.
#### Gonggong at 11:05 (RA 323.740, Dec −26.714; fixed)
- Numbers: RA to Quaoar whole 116 (Quaoar's, all day); RA to Castor = 106√2 (08:27–20:13); RA to Vesta 76φ (Vesta's); Dec to ALGOL 609/9 (00:00–18:55); RA to Rigel 1034/9; Sky to Pluto 1307/9 (exact), Uranus, Mars, the nodes (theirs).
- **Gonggong mirrors ALPHECCA across the equator**: Gonggong Dec −26.714, Alphecca +26.717 — Alphecca–Equator Dec 1:1:2, 0.010% (all day): the equator at the midpoint. Equator chords all day: Aldebaran–Equator Dec φ, 0.000%; Algorab–Equator Dec φ; Aldebaran–Alphecca Dec φ, 0.027%.
- Others: Algol–Castor RA 4:5:9; Algol–Regulus Dec; Polaris–Regulus Dec 1:2:3 (Polaris–Regulus now Vesta, Haumea in RA and Gonggong in Dec).
- With own bodies (5, all seen already): Makemake–Rahu Dec 0.020% (Makemake's Gonggong–Rahu), Sedna–Vesta Flat (Vesta's), Haumea–Jupiter, Ketu–Neptune, Eris–Transpluto.
#### Transpluto at 11:05 (RA 136.222, Dec +16.698; fixed) — the slow hub
- Numbers: Dec to QUAOAR whole 25 (00:00–20:27); Dec to VESTA whole 5; RA to URANUS 400/9 (00:00–21:55); NEPTUNE twice (RA 889/9, Sky 928/9); RA to Alkaid 636/9 (09:06–19:55); RA to Mars 943/9.
- Chords with the stars: Arcturus–Bellatrix RA √2, 0.002%; **Alphecca–Equator Dec 3:5:8, 0.003% — the string Gonggong mirrors (1:1:2, 0.010%): two bodies on Alphecca–Equator, both all day**; Capella–Procyon RA 3:5:8, 0.008%; Pleiades–Regulus RA 1:5:6, 0.009%; Aldebaran–Regulus RA φ (0.000% at 00:00); Equator–Sirius Dec 1:1:2 (Transpluto at half Sirius's Dec — Juno holds Equator–Sirius Dec 2:5:7, 0.012%: two bodies); REGULUS five times in RA.
- With own bodies (13, all seen from the other side): Jupiter–Neptune Sky 0.004%; Quaoar–Vesta Dec 0.021% (the 5/25/30 set); Makemake–Neptune Dec 0.031%; Ceres–Mercury RA 0.033%; Quaoar–Saturn RA √2; Neptune–Quaoar Sky; CHIRON three times (Chiron–Pluto RA, Chiron–Sedna Dec 0.019% at 24:00, Chiron–Quaoar Dec); Ketu–Vesta RA; Eris–Gonggong Dec.
#### Nodes at 11:05 (Rahu RA 355.794 Dec −1.821; Ketu RA 175.794 Dec +1.821; steady all day)
- **KETU and DENEB ALGEDI: Ketu Dec to Deneb Algedi = φ⁶ (17.9449, 00:00–23:44)**; Sedna (Dec +1.876, 0.055 from Ketu) is whole 18 from Deneb Algedi. Ketu–Deneb Algedi–Spica Dec φ (0.045%). (Eddie's saved lead: Deneb Algedi with Ketu — Pholas, Lingfield 2021.)
- Ketu numbers: RA to Jupiter 2√2 (Jupiter's — the Jupiter/Pluto/Uranus/Ketu RA cluster); Flat to Sirius 691/9; RA to Vega 931/9; Mercury whole 107 (Mercury's). Rahu: Dec to Aldebaran 165/9 (all day); Flat to Capella 865/9; RA to Vega 689/9.
- Chords with the stars (all day): Rahu — Aldebaran–Algol Dec 3:4:7, 0.002%; Antares–Betelgeuse Dec 3:8:11, 0.009%; Rigel–Sirius Dec 3:4:7 (0.001% at 24:00); Algol–Bellatrix Dec φ, 0.030% (Algol three times). Ketu — Castor–Rigel Dec 1:3:4, 0.003%; Betelgeuse–Castor RA 2:5:7, 0.004% (0.001% at 24:00).
- With own bodies: **Chiron–Saturn Dec 4:5:9, 0.008% (Rahu)** — Saturn–Chiron now held from Mars, Jupiter and Rahu (Rahu is Saturn's Chiron–Rahu partner); Makemake–Vesta RA φ 0.005%; Ceres–Venus RA 0.008%; Gonggong–Makemake Dec 0.020%; Chiron–Sedna Dec 1:1:2 (Rahu, with Ketu); Ketu–Orcus/Eris, Haumea–Makemake RA.

### METHOD 1 SUMMARY — the lottery chart (23 Jun 1969, 11:05 Paris)
**Two hubs**
- **CHIRON — the hub of the inner bodies.** Every body from the Sun to Juno ties into Chiron (Ceres the exception). Sun Sky whole 85 to Chiron (Juno RA 85.002). Chiron's partners: SATURN (Saturn–Chiron held from Mars Flat φ, Jupiter Dec 3:5:8 0.026%, Rahu Dec 4:5:9 0.008%) and VENUS (Mercury–Venus Flat 0.017%, Eris–Venus, Sun–Venus, Makemake–Venus). Chiron reaches Transpluto three ways; Pluto joins Chiron–Transpluto on one RA chord (all day).
- **TRANSPLUTO — the hub of the slow layer, held by whole numbers in Dec.** Haumea at Dec 25.000; Quaoar 25 below Transpluto (all day); Vesta 5 from Transpluto, 30 from Quaoar; Quaoar–Gonggong RA whole 116 (all day); Uranus–Transpluto RA 400/9 (all day); Neptune ×4; Transpluto and Gonggong both on Alphecca–Equator (0.003% / 0.010%), Gonggong mirroring Alphecca across the equator.
**Other structures**
- RA cluster: Jupiter 178.6 · Pluto 179.9 · Uranus 180.7 · Ketu ≈181.4 (the 1969 Jupiter–Uranus conjunction with the south node).
- Pairs held by two or more bodies: Saturn–Chiron (3), Pallas–Sedna (3: Saturn, Ceres, Eris), Neptune–Uranus (Mars Dec, Ceres RA), Neptune–Quaoar (Sun, Juno), Chiron–Makemake (Venus, Juno), Neptune–Transpluto (Jupiter Sky 0.004%, Makemake Dec).
- KETU and DENEB ALGEDI: Ketu Dec φ⁶ to Deneb Algedi (all day); Sedna, beside Ketu in Dec, whole 18 to Deneb Algedi (all day).
**Recurring stars**: ALGOL (Venus ×3, Vesta ×5, Chiron ×4, Rahu ×3, Pallas Sky 63φ, Gonggong Dec 609/9, Neptune Algol–Betelgeuse 0.017%); POLARIS (Betelgeuse–Polaris from Venus RA 0.008% and Mars Dec; Capella–Polaris from Mercury and Pallas — same chord; Polaris–Regulus from Vesta 0.000%, Haumea, Gonggong; Makemake ×3); REGULUS (Transpluto ×5 in RA); RIGEL (Eris ×3); Aldebaran–Procyon Dec (Saturn 0.000%, Quaoar) — the Exeter string again.
**Numbers**: own RA set aside (Eddie). Strongest by number: Vesta (5/30/59/76φ), Quaoar (116/25/30/14√2), Haumea (Dec 25), Sedna (Deneb Algedi 18), Eris (all-day ninths).
**Compared with Messi/Dettori**: here the hubs are Chiron and Transpluto, not Orcus/Sedna; Sedna is still well held (Pallas–Sedna ×3).
**Carry to the transits (draw 18 Mar 2000 20:30 Melbourne)**: Chiron and Saturn–Chiron; Venus; the Transpluto Dec set (25 / 5 / 30) and Alphecca–Equator; the Jupiter–Pluto–Uranus–Ketu RA cluster; Ketu/Sedna–Deneb Algedi; Algol, Polaris–Regulus.

### METHOD 3 — the draw sky on the lottery chart (draw 18 Mar 2000, 20:30 Melbourne; wrapper m3l.sh, natal strings at 11:05 in scratchpad/lnat/)
#### Sun (RA 358.248, Dec −0.757 at 20:30 — two days before the equinox)
- **20:30:05 Dec ALTAIR–FOMALHAUT 1:3:4 — exact 5 seconds after 20:30 (0.000% at the draw) — natal VESTA makes the SAME chord on the same string (1:3:4, 0.035%, all day)**; natal Makemake on it too (4:5:9). Vesta is in the Transpluto whole-number set (5 to Transpluto, 30 to Quaoar).
- FOMALHAUT three times within 4 minutes of the draw: Bellatrix–Fomalhaut RA 1:6:7 20:26:24 (natal Venus, loose); Alphecca–Fomalhaut RA 1:8:9, 0.002%, 20:29:38 (natal Orcus, loose); Altair–Fomalhaut Dec 20:30:05.
- After: Betelgeuse–Castor Dec 1:3:4 20:34:35 (no link); Deneb Algedi–Polaris RA 20:52:35 (natal Chiron 5:6:11, all day).
- Before: Aldebaran–Algol Dec at 19:09:59 — natal RAHU's string (3:4:7, 0.002%, all day); Arcturus–Sirius Dec 20:01 (natal Pallas 0.020%); Procyon–Sirius Dec 20:13 (natal Vesta 0.048%).
- Numbers: RA to Algorab 1537/9, Altair 545/9 — 2 ninths (chance 1.5). No parallel to a natal Dec.
#### Mercury (RA 335.145, Dec −9.858 at 20:30) — quiet on the chart
- Numbers: none (chance 0.44 / 1.5). No parallel.
- Around the draw: Dec Algol–Arcturus 3:4:7, 0.003%, exact 20:17:46 (12 min before) — ALGOL again; natal Ketu on the same string only loosely (4:5:9, 0.127%). Dec Alkaid–Alphecca φ, 0.008%, 19:42 (no link).
- Later strikes on natal strings: Arcturus–Sirius Dec 21:59 (natal Pallas 0.020%); Algorab–Castor RA 22:24 (Haumea); Aldebaran–Altair RA 23:55 (natal Ceres 0.003%).
#### Venus (RA 338.293, Dec −10.397 at 20:30; 3° from transit Mercury)
- Numbers: none. No parallel.
- Around the draw: 20:24:47 Dec Algorab–Spica 1:8:9 — natal SATURN's string (φ, all day), 5 min before; 20:36:07 Dec Deneb Algedi–Rigel φ (no link).
- After the draw — VESTA's strings: 20:54:18 Dec Algol–Altair 3:5:8 (natal Vesta 2:3:5, 0.042%; Rahu); 21:28:08 Dec Altair–Fomalhaut 1:1:2 (natal Vesta 1:3:4 — the string the Sun hit at 20:30:05); 21:43:32 Dec Algol–Fomalhaut 3:8:11 — the SAME chord as natal Vesta (3:8:11), natal Venus on it too (φ).
- Earlier: 19:05:29 RA Algol–Pleiades — natal CHIRON (φ, 0.051%, all day).
- Pull-together after Sun, Mercury, Venus: VESTA's strings are being struck — the Sun exact on Vesta's Altair–Fomalhaut at the draw, Venus on three Vesta strings in the following 75 minutes; ALGOL on the sky bodies' chords again and again.
#### Mars (RA 24.673, Dec +10.169 at 20:30)
- Numbers: Dec to Sirius 242/9; Dec to Spica 192/9 — 2 ninths (chance 1.5). No parallel.
- Before the draw, on their strongest natal strings: 19:41:24 Dec Aldebaran–Equator 5:8:13 — natal GONGGONG's string (φ, 0.000%, all day; Gonggong's equator mirror); **20:03:00 Dec Alphecca–Betelgeuse 1:6:7 — natal MARS's own string (φ, 0.001%, all day): sky Mars on natal Mars, 27 min before the draw**; 19:39 Algorab–Bellatrix Dec (natal Orcus).
- After: 20:57:00 RA Fomalhaut–Vega φ, 0.033% (no link); 21:18:36 RA Algol–Rigel √2 (natal Pallas φ, 0.028%, all day); 21:20:24 Dec Aldebaran–Pleiades (natal Mercury 3:8:11, 0.001%).
#### Jupiter (RA 34.195, Dec +12.684 at 20:30)
- **Transit Jupiter sits 1.42° (Sky) from natal SATURN** (natal Saturn RA 34.995, Dec 11.499) — the Saturn of the Saturn–Chiron core pair. (Also near: transit Sun 2.68° from natal Rahu; transit Saturn 2.69° from natal Venus.)
- Numbers: Dec to Rigel 188/9 — 1 ninth.
- Before the draw: 19:18 RA Algol–Capella 2:5:7 (natal Eris, Quaoar 0.054% all day; Saturn 0.046%); **19:46:48 Dec Castor–Deneb Algedi 2:3:5, 0.019% — natal SEDNA's string (3:5:8, all day — the Sedna whole-18-to-Deneb Algedi line)**; **20:04:48 Dec Aldebaran–Alphecca 3:8:11 — natal GONGGONG's string (φ, 0.027%, all day)** — Gonggong's strings struck twice before the draw (Mars 19:41 on Aldebaran–Equator, Jupiter 20:04 on Aldebaran–Alphecca).
- After: 20:40:48 RA Algol–Bellatrix 3:8:11, 0.012% (natal Jupiter holds Algol–Bellatrix in Dec only).
#### Saturn (RA 42.209, Dec +14.039 at 20:30; slow)
- **Transit Saturn is PARALLEL natal VENUS** (Dec 14.039 vs natal Venus 13.984 at 11:05 — 0.055; 2.69° Sky) — it holds Venus's Dec for the whole evening. With transit Jupiter 1.42° from natal Saturn, **both of Chiron's partners (Saturn and Venus) are held by the two slow transit planets at the draw.**
- Numbers: Dec to Algorab 275/9; RA to Castor 643/9; RA to Regulus 989/9 — 3 ninths (chance 1.5), above.
- Chords: Dec Algol–Arcturus φ, 0.018%, 19:50:24 (Mercury on the same string at 20:17; natal Ketu loosely); Dec Bellatrix–Sirius 1:3:4, 0.022% (19:14); Dec Alkaid–Procyon 1:4:5, 0.020% (21:31). Held loosely: Bellatrix–Pleiades RA (natal ERIS 0.004%, all day), Aldebaran–Castor RA (natal Uranus 0.023%).
#### Ceres (RA 189.526, Dec +14.253 at 20:30)
- Numbers: RA to Spica 106/9 — 1 ninth. No parallel (Dec 0.27 from natal Venus).
- Before the draw, on their tightest strings: 19:30:36 Dec Capella–Castor 4:5:9 — natal SUN's tightest string (3:5:8, 0.006%, all day); **19:57:36 Dec ALDEBARAN–PROCYON 1:4:5 — natal SATURN's string (4:5:9, 0.000%), natal Quaoar (0.031%, all day), Rahu — the Exeter string, 32 min before the draw**; 20:26:24 Dec Arcturus–Pleiades 1:1:2, 0.004% (Ceres at their Dec midpoint, 3½ min before; no natal link).
- Also: RA Alphecca–Capella 2:5:7, 0.016%, 19:54 (no link); 19:00 Capella–Rigel Dec (natal Pallas).
- SATURN's strings now struck twice before the draw (Ceres 19:57 Aldebaran–Procyon, Venus 20:24 Algorab–Spica), while transit Jupiter sits on natal Saturn.
#### Pallas (RA 115.686, Dec −6.593 at 20:30)
- Numbers: Dec to Betelgeuse = whole 14 (13.9985 at 20:30); RA to Antares 1185/9; Dec to course latitude 281/9 — 1 + 2 (chance 0.44 / 1.5), above.
- 19:27–19:54, a run on their strings: 19:27 Dec Antares–Betelgeuse √2 — natal PALLAS's own string (1:2:3, 0.028%) and natal RAHU (3:8:11, 0.009%, all day); 19:34 Dec Algorab–Betelgeuse √2 — natal Pallas the SAME chord (√2, 0.051%), natal Pluto; 19:36 Antares–Equator (Makemake); 19:39 Algorab–Equator (Gonggong); **19:52:12 Dec Aldebaran–Equator 2:5:7 — natal GONGGONG's 0.000% string, the second sky body on it (Mars 19:41)**.
- After: 20:53:24 Dec Deneb Algedi–Fomalhaut √2 (natal SEDNA 3:4:7 0.038%, all day; natal Pallas, Mars); 21:24 Pleiades–Procyon (natal Ceres 0.027%); 21:49 Capella–Equator (natal Saturn 0.018%).
- Own: Fomalhaut–Pleiades Dec 3:4:7, 0.031%, 20:15:36 (no link).
- GONGGONG's strings before the draw: Mars 19:41 (Aldebaran–Equator), Pallas 19:39 and 19:52, Jupiter 20:04 (Aldebaran–Alphecca) — four strikes in 25 minutes.
#### Juno (RA 305.992, Dec −9.424 at 20:30) — quiet on the chart
- Numbers: none. No parallel.
- Own tight chords, no natal link: Betelgeuse–Fomalhaut Dec 5:6:11, 0.016%, 20:06:36; Deneb Algedi–Pleiades Dec 1:5:6, 0.023%, 20:49:48; Altair–Pleiades Dec 5:6:11, 0.013%, 21:07:48.
- Loose holds on their strings: Castor–Vega Dec (natal Haumea's midpoint 0.007%; 0.063% here); Altair–Deneb Algedi RA 20:51 (natal Rahu, loose); Rigel–Sirius Dec 21:22 (natal Rahu 0.025%).
#### Vesta (RA 283.457, Dec −19.526 at 20:30)
- Natal Vesta (RA 86.711, Dec +21.697) to transit Vesta: Dec 41.2233 = 371/9 (41.2222, off +0.0011 at 20:30; held through the evening); RA 163.25, Flat 168.38, Sky 164.18 — no number.
- Numbers to stars: RA to Vega 38/9 — 1 ninth.
- Own chords: Dec Aldebaran–Vega φ, 0.003% at the draw (exact 21:47; no natal link); RA Antares–Deneb Algedi 19:50; Dec Betelgeuse–Fomalhaut 3:8:11, 0.022% (22:28). Nothing on their strings near the draw — sky Vesta is quiet; natal VESTA is struck by others (the Sun exact at 20:30:05, Venus three times after).
#### Uranus (RA 321.691, Dec −15.743 at 20:30; slow)
- Natal Uranus (RA 180.667, Dec +0.505) to transit: RA 141.02, Dec 16.25, Flat 141.96, Sky 138.64 — no number.
- Numbers: RA to Altair = whole 24 (23.9983); **Dec to ALKAID = 46√2** — Alkaid in √2 again (natal Uranus Sky 38√2, natal Eris Dec 45√2, transit Uranus Dec 46√2). 2 hits (chance 0.44).
- Holds (loose): Alphecca–Betelgeuse Dec 5:6:11, 0.078% — natal MARS's 0.001% string (sky Mars struck it at 20:03); Alphecca–Altair RA 3:8:11, 0.035% (natal Sedna loosely; natal Pluto holds Alphecca–Altair in Dec, 0.001%); Procyon–Vega Dec 0.032%, Betelgeuse–Capella Dec 0.038% (no link).
#### Neptune (RA 308.193, Dec −18.585 at 20:30; slow) — background
- Natal Neptune (RA 234.999, Dec −17.757) to transit: RA 73.19, Dec 0.83, Flat 73.20, Sky 69.01 — no number.
- Numbers: RA to Spica 962/9 — 1 ninth.
- On their strings: only Betelgeuse–Spica Dec 2:5:7, 0.069% — natal TRANSPLUTO's string (1:2:3, all day): a loose hold on the slow hub. Own chords without a natal link: Arcturus–Regulus Dec φ 0.022%; Alphecca–Polaris RA 0.036%; Fomalhaut–Vega RA 0.037%; Capella–Fomalhaut RA φ 0.046%.
#### Pluto (RA 252.892, Dec −11.282 at 20:30; stationary)
- Natal Pluto (RA 179.862, Dec +16.980) to transit: RA 73.03, Dec 28.26, Flat 78.31, Sky 77.49 — no number.
- **Numbers: RA to ALKAID = whole 46 (46.0004, all evening)** — and transit Uranus is Dec 46√2 from Alkaid: the two slowest planets both 46-linked to Alkaid (whole and √2).
- **RA Alkaid–Procyon 1:2:3, 0.069% (held) — natal MERCURY makes the SAME chord on the same string (1:2:3, 0.001%)** (Pluto at the Alkaid–Procyon 1:3 point, 46 from Alkaid).
- Own tight chords, no natal link: Aldebaran–Polaris Dec φ, 0.003%; Algol–Alphecca Dec 3:8:11, 0.010%; Alkaid–Antares Dec 1:4:5, 0.011% (natal Juno loose); Equator–Rigel Dec 3:8:11, 0.027%.
#### Chiron (RA 256.534, Dec −18.061 at 20:30; slow)
- **Natal Chiron (RA 5.422, Dec +5.578) to transit Chiron: RA = 980/9 (108.8883, held all evening)**; Dec 23.64, Flat 111.42, Sky 109.66 — no number.
- Numbers: RA to Aldebaran 1552/9, Deneb Algedi 632/9, Pleiades 1443/9 — 3 ninths (chance 1.5), above.
- Held on their strings: **Dec Equator–Spica φ, 0.025% — natal CHIRON's own string (1:2:3, 0.047%, all day): the hub held by its own transit**; Dec Aldebaran–Algol √2, 0.016% — natal RAHU's 0.002% string (the Sun struck it at 19:09); Dec Algol–Pleiades 2:5:7 (natal Vesta 0.016%; 0.086% here); RA Alkaid–Deneb Algedi √2, 0.026% (natal Jupiter, loose).
#### Eris (RA 23.364, Dec −6.812 at 20:30; stationary) — background
- Natal Eris (RA 20.250, Dec −14.322) to transit: RA 3.114, Dec 7.510, Flat 8.130, Sky 8.109 — no number.
- Numbers: Dec to the course latitude = whole 31 (31.0017); Dec to Regulus 169/9 (natal Haumea is Sky 169/9 from Regulus — same number, same star, different measure); RA to Arcturus 1525/9.
- Own chords, no natal link: Fomalhaut–Sirius RA 1:2:3, 0.011%; Capella–Castor RA φ, 0.028%; Altair–Polaris RA 1:6:7, 0.028%. On their strings only loosely (0.07–0.13%, separating): Pallas's Algol–Rigel and Bellatrix–Deneb Algedi, Orcus's Altair–Fomalhaut, Vesta's Fomalhaut–Vega.
#### Sedna (RA 46.445, Dec +5.251 at 20:30; fixed)
- Natal Sedna (RA 33.632, Dec +1.876) to transit: RA 12.81, Dec 3.37, Flat 13.25, Sky 13.22 — no number. Own RA 418/9 set aside (own RA doesn't count).
- Held: **RA Altair–Castor φ, 0.007% — natal SEDNA's own string (5:6:11, all day; natal Chiron on it too)**: same body both sides; Dec Algorab–Rigel φ, 0.041% (natal Venus 3:8:11, 0.063%).
#### Haumea (RA 197.056, Dec +21.421 at 20:30; fixed) — background
- Natal Haumea (Dec 25.000) to transit: RA 30.66, Dec 3.58, Flat 30.87, Sky 28.35 — no number.
- Numbers: Dec to ALKAID 251/9 (Alkaid again); Dec to Altair 113/9 — 2 ninths.
- Own chords, no natal link: Arcturus–Regulus RA 3:8:11, 0.024%; Algol–Castor Flat 4:5:9, 0.027%; Alphecca–Sirius Sky 1:3:4, 0.039%. On their strings only loosely: Altair–Castor Dec (natal Chiron, 0.090%), Algol–Spica Dec (natal Sedna).
#### Makemake (RA 179.421, Dec +32.686 at 20:30; fixed)
- **Transit Makemake's RA (179.421) sits inside their natal RA cluster** — natal Jupiter 178.621 · Pluto 179.862 · Uranus 180.667 · Ketu ≈181.45 (0.44 from natal Pluto's RA; RA only — Dec 32.7 vs Pluto 17.0).
- Natal Makemake to transit: RA 36.52, Dec 6.99, Flat 37.18, Sky 30.07 — no number. Numbers: RA to Deneb Algedi 1326/9.
- On their strings, loose: Altair–Fomalhaut Dec (natal Vesta's string — the Sun's 20:30:05 strike — 0.141% here, separating); Antares–Betelgeuse RA (natal Quaoar); Capella–Regulus RA (natal Sedna); Procyon–Sirius Dec (natal Vesta). Own: Pleiades–Regulus Dec √2, 0.028% (no link).
#### Quaoar (RA 248.064, Dec −14.950 at 20:30; fixed)
- **Transit Quaoar is CONTRAPARALLEL natal ORCUS** (−14.950 vs +14.929 — 0.021 across the equator; held all evening).
- Natal Quaoar to transit: RA 40.32, Dec 6.65, Flat 40.87, Sky 39.99 — no number. No star numbers.
- On their strings: Algol–Betelgeuse Dec 2:3:5, 0.051% — natal NEPTUNE's 0.017% string (Ketu, Mercury too); Alphecca–Altair Dec 3:4:7, 0.093% (natal Pluto 0.001%, loose here); Spica–Vega RA 2:3:5, 0.014% (natal Makemake, loose). Own: Aldebaran–Alkaid Sky √2, 0.021%; Capella–course latitude Dec 0.031%.
#### Orcus (RA 137.353, Dec −1.261 at 20:30; fixed) — quiet
- Natal Orcus to transit: Flat = 293/9 (32.5572); RA 28.25, Dec 16.19, Sky 32.29 — no other number.
- Numbers: RA to Antares = whole 110 (110.0007); Dec to Betelgeuse 78/9 — 1 + 1.
- Chords: Capella–Fomalhaut Dec 3:5:8, 0.024% (no natal link); nothing on their strings. (Transit Orcus's RA is 1.13 from natal Transpluto's — not close in Dec.)
#### Gonggong (RA 332.279, Dec −17.015 at 20:30; fixed)
- Natal Gonggong to transit: RA 8.54, Dec 9.70, Flat 12.92, Sky 12.52 — no number. No star numbers.
- **On natal GONGGONG's own strings three times (same body both sides):** Polaris–Regulus Dec 3:8:11, 0.027%; Algol–Regulus Dec 1:1:2, 0.036% (transit Gonggong at their Dec midpoint); Castor–Procyon Dec 5:6:11 (the SAME chord as natal Gonggong, 5:6:11). Natal holds are loose (0.09–0.12%).
- RA Capella–Procyon 1:3:4, 0.073% — natal TRANSPLUTO's 0.008% string (all day): a hold on the slow hub.
- Own: Algol–Polaris Dec 5:6:11, 0.002% (natal Vesta holds Algol–Polaris in RA only).
- With the four strikes on Gonggong's strings before the draw (Mars, Pallas ×2, Jupiter), Gonggong is now held by its own transit as well.
#### Transpluto (RA 147.335, Dec +13.171 at 20:30; fixed)
- **Natal Transpluto to transit Transpluto: RA = 100/9 (11.1131 at 20:30, 11.1128 at 21:30 — at the edge of ±0.002)**; Dec 3.53, Flat 11.66, Sky 11.30.
- Numbers: RA to ALKAID 536/9 (Alkaid again — transit Pluto 46, Uranus 46√2, Haumea 251/9); Dec to Sirius 269/9; Dec to Spica 219/9 — 3 ninths, above chance.
- Chords: Aldebaran–Arcturus Dec 4:5:9, 0.012% (16:52); Alphecca–Spica RA 0.026%; Aldebaran–Polaris RA 0.036%; Algol–Algorab RA 0.042% — none on their strings (Betelgeuse–Procyon RA, natal Pluto, loose).
- **Natal → transit, same body, all bodies (Eddie 18:50: "be more lenient with these natal to transit on the same body").** Checked every body at ±0.002 / ±0.005 / ±0.01:
  - ±0.002: Venus Flat whole 71 (70.9996 — missed earlier, Venus's n2t not run), Vesta Dec 371/9, Chiron RA 980/9, Orcus Flat 293/9, Transpluto RA 100/9 (edge, 0.0020) — 5 of 23 bodies; chance ≈ 4.
  - ±0.005 adds: Mars RA 1293/9 (0.0044), Mercury Dec 256/9, Ceres Flat 1199/9, Eris RA 28/9 + Sky 73/9, Sedna Sky 119/9, Haumea RA 276/9. 11 of 23 bodies; chance ≈ 9.
  - ±0.01: 17 of 23 bodies (chance ≈ 13) — at that width almost every body hits a ninth.
  - Reads as: by count, natal→transit numbers are at chance at every width. A lenient band is fair where a position is uncertain (Transpluto is a hypothetical point; fast bodies move in the birth minute), so ±0.002–0.005 can be shown as "near", counted only when it joins something else.
#### Nodes (transit Rahu RA 124.633 Dec +19.633; Ketu RA 304.633 Dec −19.633 at 20:30)
- **Rahu RA to RIGEL = whole 46 (45.9996; Ketu 134, the same fact)** — 46 again: transit Pluto RA 46 to Alkaid, transit Uranus Dec 46√2 to Alkaid, transit Rahu RA 46 to Rigel. Rahu Dec to Regulus 69/9.
- **RA Rigel–Spica 3:5:8, 0.005%, exact 20:06:36** (24 min before the draw; Rahu at 46 from Rigel) — no natal link.
- On their strings: RA Antares–Rigel 3:8:11, 0.045% — natal PLUTO's 0.011% string (all day); RA Algol–Capella √2, 0.040% (natal Saturn 0.046%, Eris, Quaoar); Ketu Dec Algorab–Rigel 3:8:11 at 22:41 — the SAME chord as natal Venus (3:8:11, 0.063%).
- Natal nodes to transit nodes: RA 128.84, Dec 21.45 (Rahu–Rahu); transit Rahu to natal Ketu RA 51.16, Dec 17.81 — no number.
#### The MOON — the clock (RA 158.576, Dec +12.904 at 20:30)
- No Moon crossing of a natal Dec or RA in 19:30–23:00.
- Moon strikes on their strings, 20:00–21:00 (natal holder in brackets):
  - 20:06:55 Dec Algol–Bellatrix (natal JUPITER 0.021%, RAHU 0.030%, all day)
  - **20:22:38 Dec Alphecca–Betelgeuse φ — natal MARS's 0.001% string (all day); sky Mars struck it at 20:03 — Mars's string struck twice before the draw (Mars, then the Moon)**
  - **20:30:30 Dec Deneb Algedi–Equator (natal Ceres, loose) and 20:30:36 Dec Alphecca–Arcturus 3:4:7 (natal TRANSPLUTO 1:3:4, 0.094%, all day) — within 36 seconds of 20:30, the slow hub's string (loose natal hold)**; 20:30:35 RA Alkaid–Bellatrix 5:8:13, 0.015% (no link). Together with the Sun's 20:30:05 strike on Vesta's Altair–Fomalhaut (same chord), the Sun and the Moon both strike the Transpluto layer inside the draw minute.
  - After: 20:41:49 Dec Algol–Altair (natal VESTA 0.042%); 20:44:16 Dec Altair–Spica (natal Quaoar 0.028%); 20:44:32 Dec Algol–Pleiades (natal VESTA 0.016%, Venus) — Vesta's strings again (Venus took Algol–Altair again at 20:54).
- Caution: the Moon makes a natal-linked chord every ~3 minutes in this hour (19 between 20:00 and 21:00), so a Moon strike near 20:30 is likely by itself; what stands out is which strings: Mars's own (after sky Mars), Transpluto's, and Vesta's.

### NATAL MOON — the lottery chart (Eddie 18:57: "it feels like we are missing something" → the natal Moon, usable because the birth time is accurate; left out until now because horse/jockey birth hours are unknown)
#### Moon at 11:05 (RA 185.987, Dec −4.045; moves ~0.27°/h, so every number holds about a minute either side of 11:05)
- Numbers — above chance (4 φ/√2/whole vs ~1.7; 8 ninths vs ~5.8): **Sky to ALGORAB 113/9 (12.5556, exact)**; **Sky to Arcturus = whole 36**; **Flat to URANUS = whole 7**; RA to MARS = 34φ; Dec to MERCURY = 16√2; Dec to RAHU 20/9; Flat to SUN 878/9; Flat to Ceres 1191/9; Sky to SATURN 1353/9; Flat to Polaris 1577/9, Castor 727/9; Sky to Capella 941/9; Dec to Aldebaran 185/9.
- Chords with the stars: an ALGORAB–BELLATRIX–RIGEL set in Dec — Algorab–Rigel 1:2:3, 0.010%; Algorab–Bellatrix 5:6:11, 0.018%; Bellatrix–Rigel 2:5:7, 0.025% (the Moon makes a chord with each pair of the three); Alphecca–Arcturus RA √2, 0.049%; Altair–Arcturus RA 1:3:4.
- With own bodies: **Eris–Quaoar Dec √2, 0.003%**; **Neptune–Pluto RA 1:8:9, 0.008%**; Quaoar–Venus Dec φ, 0.025%; Chiron–Sedna Dec 5:8:13, 0.040%; Haumea–Neptune RA 2:5:7; Ceres–Quaoar RA 1:5:6; **Haumea–Transpluto Dec 2:5:7 — on the 8.302 gap of the Dec-25 lattice**; QUAOAR four times; Mars–Sun Flat; Rahu–Saturn Dec.
- Reads as: the natal Moon is well tied — whole numbers to Uranus (7) and Arcturus (36), φ/√2 to Mars and Mercury, and it sits in the Quaoar/Transpluto/Haumea whole-number layer and on Chiron–Sedna.
#### The draw sky on the natal MOON
- No sky body parallel, contraparallel or within 3° of the natal Moon (RA 185.988, Dec −4.045); the sky Moon (Dec +12.9) does not cross the natal Moon's Dec. Numbers from sky bodies to the natal Moon: Ketu Flat 1077/9, Neptune Sky 1069/9, Saturn RA 1294/9 — 3 ninths, about chance (~3 expected).
- **Held all evening: the natal Moon's tightest star string, Algorab–Rigel Dec (1:2:3, 0.010%) — sky SEDNA holds it (φ, 0.041%) and sky KETU holds it (0.057%, exact 22:41); natal Venus is on the same string (3:8:11, 0.063%) — Ketu at 22:41 plays Venus's own chord.**
- Strikes: 19:39:36 Mars on Algorab–Bellatrix Dec (natal Moon 5:6:11, 0.018%) — 51 min before the draw; 19:45 Pallas on Altair–Arcturus Dec (natal Moon, loose); 20:49:48 Pallas on Bellatrix–Rigel Dec (natal Moon 2:5:7, 0.025%) — 20 min after. Later: Moon 22:51 and Mercury 22:56 on Algorab–Rigel.
- Reads as: the natal Moon is held (Sedna, Ketu on Algorab–Rigel) and touched before and after, but not struck at 20:30 itself.

### METHOD 2 — tuned layers (lottery chart; natal at 11:05 via race id 20000318_melbournet_2030; natal Moon not included in these scripts)
#### L1 — star bases (117 tuned pairs, 4 UNISON, 7 same body, 1 with both sides within 0.02%)
- **Draw minute: Altair–Fomalhaut Dec UNISON — sky SUN 1:3:4, 0.000%, exact 20:30:05; natal VESTA 1:3:4, 0.035%.** The only L1 item exact at the draw. Natal Makemake is on the same base (same body, loose 0.141%).
- **Tightest pair: Aldebaran–Algol Dec — natal RAHU 3:4:7, 0.002%; sky CHIRON √2, 0.016% (exact 06:20, held all day).** Algol (the chart's main star) with the inner hub.
- **The 46s sit on tuned bases:** Alkaid–Procyon RA UNISON — natal MERCURY 1:2:3, 0.001%; sky PLUTO 1:2:3 with the short side = 46.000 (Pluto RA 46 to Alkaid). Antares–Rigel RA — natal PLUTO 2:3:5, 0.011%; sky RAHU 3:8:11 with a side = 46.000 (Rahu RA 46 to Rigel).
- Before the draw: Ceres on Capella–Castor 19:30 (natal SUN 0.006%); Jupiter on Castor–Deneb Algedi 19:46 (natal SEDNA, the 18.000 side); Jupiter on Aldebaran–Alphecca 20:04 (natal GONGGONG φ) — Gonggong's strings again.
- After: Pallas on its own Deneb Algedi–Fomalhaut 20:53 (same body); Venus on Algol–Altair 20:54 (natal VESTA) — Vesta again after the draw.
- UNISON also: Algorab–Rigel 3:8:11 (Ketu with natal Venus, 22:41). Same body all day: Chiron (Equator–Spica), Sedna (Altair–Castor), Gonggong ×3 (days).
#### LATTICE CHECK (Eddie 19:06) — the draw sky's Decs on natal Transpluto's whole-number grid (the Messi "Dec line" equivalent)
- Natal lattice (11:05): Transpluto +16.698; Vesta = T+4.999; Quaoar = T−25.000 (−8.302); Haumea = 25.000 (whole from the equator); Haumea−T = 8.302 = −Quaoar. Also seen now: **natal Sirius −16.706 is contraparallel natal Transpluto (0.008)**; Gonggong/Alphecca mirror 0.003.
- Three grids checked: T + whole, −T + whole (mirror), whole from the equator. Also sky Dec as a fraction (q ≤ 9) of natal Transpluto's Dec.
- **At 20:30: no sky body within 0.005 of any grid point, and no fraction within 0.01.** Nearest: Makemake T+16 (−0.012, exact in 40 h), Jupiter T−4 (−0.014, exact 01:12 on the 19th), Gonggong whole −17 (−0.015), Pluto T−28 (+0.020). About 2 within 0.015 expected by chance — 3 found.
- Timed crossings near the draw: Moon crosses whole 13 at 19:48:48 and T−4 (12.698) at 21:55; Jupiter reaches the same T−4 at 01:12. Sun reaches −T+16 at 00:06. Nothing in 20:00–21:00.
- Reads as: the Transpluto lattice is not struck at the draw — unlike Messi's Dec line. The Moon and Jupiter come to the same point (Transpluto −4) later that night.
- Eddie 19:33: 20:30 is the draw time — the winner was there in the television studio (so the time and the Melbourne location stand).
#### Nodes layer (30 tuned pairs, 0 UNISON, 2 same body, none with both sides within 0.02%)
- **Base RA Rahu–Regulus: natal Rahu–Regulus with natal SUN φ (0.035%); sky Rahu–Regulus with the sky MOON φ (0.008%), held at 20:30:45 — 45 s after the draw.** The Sun at birth and the Moon at the draw play φ on the same node–star base. Sky Saturn joins the base at 22:08 (1:3:4, 0.038%).
- Same body (loose): Mars on Ketu–Betelgeuse (natal 3:4:7, sky 4:5:9 at 22:06, 0.138%); Orcus on Ketu–Spica (0.136/0.138%, days).
- Regulus is the star here (Regulus strings ran through Messi's goals).
#### L2 — slow-body bases (199 tuned pairs, 15 UNISON, 10 same body, 22 base lengths in tune)
- **Draw window, 20:25–20:35:**
  - 20:25:30 **Venus on Uranus–Antares Dec, UNISON + SAME BODY 1:2:3** (sky 0.024%, natal Venus 0.073%).
  - **20:29:53 Sun on Eris–Equator Dec 1:8:9, 0.005%** (Sun at Dec −0.757, two days from the equinox); natal JUNO 1:2:3 on natal Eris–Equator, 0.015%.
  - **20:33:10 Pallas on Eris–Sedna RA 1:3:4, 0.001% — SAME BODY** (natal Pallas 1:8:9, 0.025%).
  - 20:34:54 Pallas on Chiron–Regulus Dec φ, 0.019%, UNISON with natal Juno φ (loose 0.124%) — Chiron and Regulus again.
  - Moon items are at the sampling edge (held at 20:28 or 20:32, 0.04–0.13%) — not exact at the draw.
- **Eris's bases take both tight draw-window strikes** (Sun 20:29:53, Pallas 20:33:10). **Natal JUNO holds six of the listed bases** (Eris–Equator, Chiron–Regulus, Neptune–Quaoar, Uranus–Arcturus, Orcus–Betelgeuse, Haumea–Fomalhaut) — Juno had not stood out before.
- Tight away from the draw: Ketu on Transpluto–Pleiades 0.003% at 19:43 (natal Rahu 0.020%); Transpluto on Quaoar–Alphecca RA 0.009% all day (natal Makemake 0.005%, base lengths 9/5 — the Transpluto/Quaoar layer in RA); Vesta on Makemake–Rahu 0.004% at 21:35 (natal Gonggong); Makemake on Orcus–Procyon 0.006% at 21:25 (natal Mars, loose).
- Caution: 199 tuned pairs from 368 natal chords — tuned pairs are common; only the exact, timed ones carry weight.
#### ERIS natal → transit across the three charts (Eddie 19:36: "I pointed out Eris earlier as Messi had tr-nat Eris and so did Dettori")
- Lottery: natal Eris (11:05) RA 20.250, Dec −14.322 → sky Eris at 20:30: **RA 3.1142 (28/9 = 3.1111, +0.0031, near)**, Dec 7.5097, Flat 8.1298, **Sky 8.1088 (73/9 = 8.1111, −0.0023, near)**. The gaps grow ~0.0003°/h: RA was exactly 28/9 about 10 h before the draw (~10:30), Sky reaches 73/9 about 8 h after (~04:10 on the 19th) — the draw sits between them.
- Messi: RA 20/9 (+0.0018 at KO — a hit). Dettori: Dec 6.663, 0.0035 under 60/9 (near; exact ~0.8 d before).
- All three charts: natal→transit Eris lands on a ninth (one hit, three near). By the agreed rule, the lottery's two "near" Eris numbers count only when joined — and they are joined: both tight draw-window strikes in L2 are on Eris bases (Sun on Eris–Equator 20:29:53; Pallas on Eris–Sedna 20:33:10, same body).
- Chance: one measure in the ±0.005 ninths band ≈ 9%; two of four measures for one body ≈ 4%.
#### L3 — medium-body bases (84 tuned pairs, 4 UNISON, 6 same body)
- **Draw window:**
  - 20:28:15 Moon on Jupiter–Ceres Dec 1:6:7, 0.026% — natal MAKEMAKE 3:4:7, 0.016%.
  - 20:31:45 Moon on Ceres–Aldebaran Dec 3:5:8, 0.019% — UNISON with natal URANUS 3:5:8 (loose 0.141%).
  - **~20:32 Moon on Pallas–Algol RA 5:8:13, 0.001% — natal ERIS 1:4:5 (0.065%).** Eris again, and Algol (the chart's main star).
  - **20:32:36 Haumea on Mars–Sirius RA 4:5:9, 0.002% — natal TRANSPLUTO 1:3:4, 0.027%.** The Transpluto lattice: Haumea (Dec 25.000 in the natal chart) strikes Transpluto's base 2.6 min after the draw, and the base star is SIRIUS — contraparallel natal Transpluto (0.008, found in the lattice check).
- **19:39–19:47 cluster (about 45 min before the draw):** Ketu on Transpluto–Pleiades 19:43:21 (L2, 0.003%, natal Rahu); Rahu on Ceres–Altair 19:45:39 (0.011%, natal Haumea 0.017%; Pluto on the same base 19:29); **Vesta on Saturn–Rahu Dec 19:46:13 (0.009%) — natal CHIRON 4:5:9, 0.008% (the inner hub, on its partner Saturn's base)**; Jupiter on Castor–Deneb Algedi 19:46:48 (L1, natal Sedna). With Method 3's 19:39–19:41 strikes (Mars and Pallas on Gonggong's strings, Mars on the natal Moon's Algorab–Bellatrix) — about eight strikes in eight minutes.
- Same body (loose, hours away): Pluto Mars–Vega, Orcus Juno–Alphecca and Jupiter–Regulus, Mercury Pallas–Polaris, Ketu Mars–Betelgeuse, Makemake Jupiter–Aldebaran.
#### L4 — Sun/Mercury/Venus/Moon bases (32 tuned pairs, 1 UNISON, 2 same body)
- 20:25:30 Uranus on Venus–Antares Dec 1:2:3 (UNISON + SAME BODY with natal Uranus) — the same three points as L2's Venus on Uranus–Antares: sky Venus–Uranus–Antares and natal Venus–Uranus–Antares are both 1:2:3. One fact, seen from two layers.
- **20:38:17 Saturn on Sun–Regulus RA 2:5:7, 0.010% — natal RAHU φ on natal Sun–Regulus (0.035%).** With the Nodes layer: the natal SUN–RAHU–REGULUS triad (Sun at φ of Rahu–Regulus) is echoed at the draw twice — the Moon on sky Rahu–Regulus (20:30:45) and Saturn on sky Sun–Regulus (20:38:17). Saturn (Chiron's partner) then takes Rahu–Regulus at 22:08.
- **20:42:33 Jupiter on Venus–Rahu RA φ, 0.012% — natal CERES 4:5:9, 0.008%** (both sides tight).
- Moon items at the window edge (20:28 Sun–Procyon, 20:32 Sun–Alkaid), loose natal side.
#### METHOD 2 — the draw sequence (20:25–20:43)
- 20:25:30 Venus/Uranus/Antares 1:2:3 both sides · 20:29:53 Sun on Eris–Equator (Juno) · 20:30:05 Sun UNISON Vesta on Altair–Fomalhaut · 20:30:36 Moon on Transpluto's Alphecca–Arcturus (M3) · 20:30:45 Moon on Rahu–Regulus (natal Sun) · ~20:32 Moon on Pallas–Algol (Eris) · 20:32:36 Haumea on Mars–Sirius (Transpluto) · 20:33:10 Pallas on Eris–Sedna (same body) · 20:34:54 Pallas on Chiron–Regulus (Juno) · 20:38:17 Saturn on Sun–Regulus (natal Rahu) · 20:42:33 Jupiter on Venus–Rahu (Ceres).
- Threads: ERIS (three strikes + the Eris→Eris ninths); the RAHU–REGULUS–SUN triad (Moon, then Saturn; Regulus also on Chiron's base); the TRANSPLUTO lattice by chord (Moon, Haumea on Sirius). The earlier 19:39–19:47 cluster is as dense.
- **Lottery chart parked (Eddie 19:44: "we will come back as we discover more").** Not yet found: anything that says winner/money rather than "big moment". Open routes: (1) control — the same draw sky against 30–50 made-up birth charts, to see what only the winner's chart has; (2) the winning numbers / ball order; (3) the ticket-purchase / number-picking moment. Natal Moon not yet in the tuned layers.

## §76 FRANKEL — Queen Anne Stakes, Royal Ascot, 19 Jun 2012 (Eddie 19:44: "Frankel (the Messi of racehorses)")
- Race: off 14:34:00 BST (Eddie), winning time 1m 37.85s (finish ≈14:35:38), 11 ran, won by 11 lengths (Timeform 147). Ascot 51.4062, −0.6756, 77 m. Race id 20120619_ascot_1434 (setup_frankel.py; workbook built at 14:30, sky moved to 14:34).
- Frankel foaled 11 Feb 2008, Banstead Manor Stud, Cheveley (52.2449, 0.4080); Eddie's time 12:00 — taken as a placeholder (no foaling time found), so birth-hour-only findings are weak; all-day findings carry. Jockey Tom Queally (8 Oct 1984, Dungarvan; P02) in the file, time unknown.
### Method 1 — Frankel (P01, at 12:00)
#### Sun (RA 324.386, Dec −14.171 at 12:00; moves ~1°/day RA, 0.33°/day Dec)
- Numbers: Dec to VENUS 65/9 (11:41–12:13); Sky to Quaoar 45√2, Sky to Orcus 1443/9, RA to Procyon 1354/9, Dec to Vesta 16/9, Juno 22/9 — 1 √2 + 5 ninths, under chance (~1.7 / ~5.8); all only around 12:00.
- Chords (all birth-hour only — 0.4–8% off at either end of the day): stars — **RA Altair–Fomalhaut 3:4:7, 0.009%** (the lottery draw's Altair–Fomalhaut, there in Dec); Dec Arcturus–Bellatrix 5:8:13, 0.012%; Sky Deneb Algedi–Fomalhaut 1:7:8, 0.013%. Bodies — RA Ceres–Quaoar 5:6:11, 0.010%; **Dec Mars–Sedna 1:1:2, 0.014% (SEDNA at the Dec midpoint of Mars and the Sun — corrected at Mars)**; RA Chiron–Rahu √2, 0.027%; Dec Saturn–Uranus 1:2:3; Dec Mars–Saturn φ.
- Reads as: nothing in the Sun holds all day; with a placeholder time, the Sun's chords can't be leaned on.
#### Daily motion on the foaling day (what holds all day with an unknown time)
- Fast (birth-hour only): Moon 12.8°/d, Venus 1.32, Sun 0.99, Mercury −0.92 (retrograde, station direct ~19 Feb), Vesta 0.50, Pallas 0.34, Juno 0.26, Ceres 0.22, Jupiter 0.22.
- **MARS: RA +0.15/d but Dec −0.013/d — almost stationary in Dec** (station direct 30 Jan 2008). Saturn RA −0.07 (retrograde). **Pluto Dec +0.001/d** (Dec station). All TNOs, nodes, Neptune, Uranus, Chiron: under ~0.07/d.
#### Mercury (RA 313.310, Dec −13.815 at 12:00; retrograde, −0.92°/d)
- Numbers: 89√2 to Capella (RA) + 9 ninths (Deneb Algedi RA 121/9, Neptune RA 97/9, Betelgeuse Dec 191/9, Pluto Dec 30/9, Bellatrix Flat 1166/9, Rahu Flat 149/9, Chiron Flat 46/9, Sedna Sky 885/9, Aldebaran Sky 1063/9) — ninths a little above chance (9 vs ~5.8), all only at 12:00.
- Chords (all birth-hour only): Dec Betelgeuse–Spica 1:7:8, 0.006%; RA Algol–Altair 1:6:7 and Dec Algol–Altair √2 (Algol–Altair both ways); Polaris–Sirius RA 3:4:7; Jupiter–Quaoar Dec 1:4:5, 0.026%; Gonggong–Rahu RA φ, 0.029%.
- Reads as: nothing all day. Mercury sits close to the Sun in Dec (0.36 apart) but not parallel.
#### Venus (RA 293.997, Dec −21.394 at 12:00; 1.32°/d RA, 0.15°/d Dec)
- Numbers: Dec to PLUTO 3√2 (11:52–12:29); **Dec to VESTA 49/9 (03:12–12:35 — nine hours, Venus and Vesta move together in Dec)**; Dec to Sun 65/9 (the Sun's); Dec to Juno 87/9; Sky to Rahu 25√2; RA to Alkaid 784/9. 2 √2 + 4 ninths — about chance.
- Chords: **Dec Antares–Rigel φ, 0.002%** (birth-hour only, 2% at the day's ends); Flat Antares–Deneb Algedi √2, 0.035%; RA Neptune–Vesta 1:5:6, 0.022%; Dec Neptune–Orcus 3:4:7, 0.033% (0.97% at the ends).
- Seen in passing: natal **Haumea–Uranus Dec base = 24.997 (whole 25)** — for when we reach Uranus/Haumea (the lottery chart's Dec-25 lattice had Haumea at 25.000).
#### MARS (RA 84.159, Dec +26.508 at 12:00; RA +0.15°/d, Dec −0.013°/d — the Dec holds all day)
- **Numbers, long windows (Dec):** **Dec to ALDEBARAN = whole 10 (07:29–16:45)**; **Dec to ORCUS = whole 32 (08:02–14:07)**; **Dec to ARCTURUS 66/9 (08:53–18:39)**. Also RA to Ceres 364/9 (11:02–12:35), Sky to Capella 179/9 (09:46–12:28), Flat to Procyon 336/9, Chiron 1193/9, Sky to Neptune 1108/9, RA to Quaoar 1567/9. 2 whole + 7 ninths, the Dec ones lasting 6–10 hours.
- **A Dec lattice: Mars +26.508, Arcturus +19.174, Aldebaran +16.508, Orcus −5.492** — Mars–Aldebaran 10, Mars–Orcus 32, so Aldebaran–Orcus = 22 (whole), Mars–Arcturus 66/9, Arcturus–Aldebaran 24/9. (Like the lottery chart's Transpluto lattice.)
- **Correction:** the Sun's "Mars–Sedna 1:1:2" puts SEDNA at the Dec midpoint of Mars and the Sun (Mars 26.508, Sedna 6.17, Sun −14.171), not the Sun.
- Chords holding all day (≤ ~0.2% at both ends): Dec Polaris–Spica 3:5:8, 0.037%; **Dec Altair–Antares 1:2:3, 0.045% (0.002% at 00:00)**; Dec Algorab–Castor 1:8:9, 0.022%; Dec Castor–Spica 1:7:8; Dec Altair–Bellatrix 1:7:8; RA Alphecca–Regulus 5:6:11. Bodies: **Dec Haumea–Juno φ, 0.019%**; **RA Ceres–Orcus 2:3:5, 0.030%**; **RA Eris–Neptune 1:1:2, 0.038% (Mars at the RA midpoint of Eris and Neptune)**; **Dec Jupiter–Neptune 1:5:6, 0.040% (0.05/0.04% at the ends)**; Dec Chiron–Haumea 1:4:5, 0.044%.
- Reads as: MARS is the first strong body — whole numbers and a star lattice in Dec, and a dozen chords held all day. Orcus twice (Dec 32, Ceres–Orcus), Neptune twice, Haumea twice.
#### OUT OF BOUNDS (Eddie 21:05: "one point we have not yet covered is DEC out of bounds") — |Dec| beyond the obliquity (~23.44°)
- Natal, classical bodies + Moon (Makemake is always OOB from its 29° tilt; TNOs/asteroids listed separately):
  - **FRANKEL: MARS +26.508 — 3.07° out of bounds** (the only classical body; Mars near-stationary in Dec, so all day). Also Makemake.
  - **Queally: MARS −25.527 — 2.09° OOB**; Jupiter −23.455 (0.012, on the edge).
  - **Messi: MOON +28.039 — 4.60° OOB** (1987, near a major lunar standstill; time known); Uranus −23.482 (0.039, edge). Also Ceres −26.0, Pallas +25.2, Haumea +23.6.
  - **Lottery: MARS −23.838 — 0.39° OOB**. Also Ceres −26.2, Gonggong −26.7, Haumea +25.0, Pallas +24.3.
  - Dettori (12:00 placeholder): Mercury −24.106 (0.66). Diffident (12:00): Mars −23.951 (0.51), Mercury (0.28), Moon (0.08, time-dependent). Also Gonggong/Haumea (Dettori), Ceres (Diffident).
- Event skies: **Frankel race — MERCURY +23.536, OOB by 0.100** (the Sun at its solstice maximum, solstice next day); Dettori race — Ceres −24.7; Messi match and lottery draw — only Makemake.
- Reads as: MARS out of bounds in four of the six natal charts (Frankel, Queally, the lottery winner, Diffident); Messi has the Moon far out of bounds instead. Frankel's Mars is the furthest out among the Mars cases and is also his strongest body by Method 1.
#### Ceres (RA 43.715, Dec +13.901 at 12:00; 0.22°/d RA, 0.12°/d Dec)
- Numbers: RA to MARS 364/9 (Mars's), RA to Quaoar 1309/9, Dec to Antares 363/9, Flat to Haumea 1451/9 — 4 ninths, below chance; all within ~45 min of 12:00.
- Chords: Dec Makemake–Pallas √2, 0.006% (0.48% at the ends); RA Alkaid–Castor 3:4:7, 0.021% (0.14–0.18% at the ends, roughly all day); RA Mars–Orcus 2:3:5, 0.030% (Mars's, all day); RA Aldebaran–Rigel φ, 0.038%; RA Bellatrix–Betelgeuse 1:5:6; RA Deneb Algedi–Vega φ (0.063% at 00:00). Quaoar–Sun 5:6:11 (the Sun's).
- Reads as: a quiet body; its one all-day link is to MARS (Mars–Orcus) — Mars again.
#### Jupiter (RA 283.006, Dec −22.791 at 12:00; RA 0.22°/d, Dec 0.017°/d — Dec holds all day; 0.65° inside the bounds)
- **Numbers: Dec to URANUS = whole 17 (08:09–24:00)** — and Jupiter to HAUMEA in Dec = 41.995 (whole 42, −0.005, near); Haumea–Uranus = 24.997 (whole 25, from Venus). **A second Dec lattice: Jupiter −22.791, Uranus −5.79, Haumea +19.20 — 17, 25, 42.** (Haumea 0.03 from Arcturus +19.174, which is in the Mars lattice.) Others, birth-hour only: RA to Alphecca 444/9, Vega 34/9; Flat to Regulus 1219/9, Alphecca 629/9; Sky to Rigel 1268/9, Vesta 403/9, Chiron 312/9. 1 whole + 7 ninths.
- Chords all day: **Dec Castor–Fomalhaut 1:8:9, 0.001%** (0.13% at the ends); **RA Bellatrix–Deneb Algedi φ, 0.005%** (0.25%); **Dec Polaris–Procyon 1:3:4, 0.016% (0.013/0.046 — all day)**; RA Capella–Pleiades 1:6:7, 0.029%; Dec Aldebaran–Capella 3:4:7; **Dec Juno–Sedna φ, 0.008%**; Dec Mars–Neptune 1:5:6 (Mars's); Dec Eris–Sedna 5:8:13; RA Chiron–Eris 1:2:3. Birth-hour only: RA Eris–Pluto 1:8:9, 0.001%.
#### Saturn (RA 158.528, Dec +10.976 at 12:00; retrograde, RA −0.07°/d, Dec +0.03°/d)
- Numbers: **Dec to CHIRON = whole 21 (10:06–21:32)** (Chiron Dec ≈ −10.02); **Sky to SIRIUS = whole 63** (10:20–12:14); Dec to Alkaid 345/9 (09:34–12:42); RA to Rigel 719/9, Sky to Chiron 1427/9, Sedna 958/9. 2 whole + 4 ninths.
- Chords all day: **Dec Alkaid–Deneb Algedi √2, 0.003% (≤0.10% all day)**; **Dec Chiron–Gonggong φ, 0.003% (0.15% at the ends)**; **RA Haumea–Pluto √2, 0.007% (≤0.054% all day)**; **Dec Eris–Quaoar 2:3:5, 0.019% (≤0.086%)**; Dec Alkaid–Castor 5:6:11; Dec Capella–Pleiades 3:5:8; Dec Alkaid–Rigel 1:2:3; Dec Haumea–Orcus 1:2:3.
- Reads as: Saturn holds Chiron by whole number and by chord (Chiron–Gonggong); Alkaid three times. Slow bodies hold all day by nature — what marks Saturn is four all-day chords at ≤0.02%.
#### Uranus (RA 348.379, Dec −5.792 at 12:00; slow)
- **The Jupiter–Uranus–Haumea Dec lattice, hour by hour:** Haumea–Uranus = 25.0017 at 00:00, **exact 25.0000 at 04:00**, 24.9966 at 12:00 (hit to ~08:45); Uranus–Jupiter = 16.9964 at 00:00, **exact 17.0000 at 20:00** (hit from 08:09); Haumea–Jupiter 41.998 → 41.992 (just short of 42 all day). **Both whole numbers hold together 08:09–08:45.** Uranus is the middle of the lattice.
- Other numbers: RA to Spica 104√2 (11:09–13:06); Flat to Alphecca 1073/9 (10:31–12:49); Sky to Spica 1288/9, Regulus 1465/9. 2 whole (with Haumea's 25) + 1 √2 + 3 ninths.
- Chords all day: Sky Algol–Capella 1:3:4, 0.031% (≤0.055%); Dec Alkaid–Vega φ, 0.051%; **Dec Gonggong–Pluto φ, 0.041% (0.036/0.040 — all day)**; Dec Alkaid–Procyon 1:4:5. Birth-hour only: Dec Juno–Pallas 2:5:7, 0.011%; RA Haumea–Juno φ.
- Reads as: Uranus's weight is the whole-number lattice with Jupiter and Haumea, not its chords. Alkaid again (three Dec chords).
#### Neptune (RA 324.089, Dec −14.577 at 12:00; slow)
- **Sun–Neptune conjunction: 0.30° apart in RA, 0.41° in Dec** (the Sun passes it on the foaling day).
- Numbers: **Sky to RAHU = whole 6 (Ketu 174, the same fact), 09:18–12:37**; **Dec to PROCYON 14√2 (06:06–13:41)**; Dec to Altair 211/9 (07:11–14:49); Dec to CHIRON 41/9 (10:28–20:16); RA to Deneb Algedi 24/9 (10:33–13:08); RA to Makemake 1229/9; Sky to Mars 1108/9 (Mars's), Antares 647/9. 2 whole/√2 (+Ketu) + 6 ninths; long windows.
- Chords all day: **RA Antares–Spica 3:5:8, 0.013% (≤0.036%)**; **Dec Alkaid–Castor 3:8:11, 0.021% (≤0.034%)**; RA Pleiades–Procyon 5:8:13; Dec Castor–Regulus 3:4:7. With bodies — the Mars ones: RA Eris–Mars 1:1:2 (Mars at the midpoint of Eris and Neptune) and Dec Jupiter–Mars 1:5:6 (≤0.05% all day). Gonggong–Sedna RA 1:8:9 (0.030% at 24:00).
- Reads as: Neptune ties MARS and JUPITER together (the Mars–Jupiter–Neptune Dec triad) and holds the nodes by whole number. Alkaid–Castor again (Saturn and Ceres also on it).
#### Pluto (RA 270.368, Dec −17.150 — Dec stationary, −17.150 at both ends of the day)
- Numbers: **Dec to BETELGEUSE 221/9 — ALL DAY (off 0.0001)**; Flat to Betelgeuse 1621/9 (09:36–13:17) — Betelgeuse twice; Sky to Makemake 57φ (11:46–14:34); Sky to Orcus 1095/9; Flat to Juno whole 12, Dec to Venus 3√2 (Venus's), Mercury 30/9 (birth-hour).
- Chords all day: **Dec Procyon–Vega 2:3:5, 0.010% (≤0.013% all day)**; **RA Bellatrix–Pleiades 1:6:7, 0.015% (≤0.024%)**; **Dec Orcus–Sedna 1:1:2, 0.018% — ORCUS at the Dec midpoint of Pluto and Sedna (≤0.045%)**; **RA Antares–Spica 1:2:3, 0.030% — Neptune also holds Antares–Spica (3:5:8): a two-body string**; RA Algol–Altair 1:4:5 (0.001% at 00:00); Dec Procyon–Rigel 2:3:5; Dec Algol–Arcturus 3:5:8; RA Haumea–Saturn √2 (Saturn's); Dec Gonggong–Uranus φ (Uranus's). Birth-hour only: RA Eris–Jupiter 1:8:9, 0.001%.
- Reads as: Pluto is fixed all day — Betelgeuse by number, Procyon three times (Procyon–Vega, Procyon–Rigel, and Neptune's 14√2), Orcus as the midpoint with Sedna, and Antares–Spica shared with Neptune.
#### Chiron (RA 316.735, Dec −10.023 at 12:00; slow)
- Numbers: Dec to SATURN whole 21 (Saturn's) and Dec to NEPTUNE 41/9 (Neptune's, 10:28–20:16) — Chiron sits between them in Dec (Saturn +10.976, Chiron −10.023, Neptune −14.577; Saturn–Neptune 25.553, 0.003 short of 230/9, near); Dec to Altair 170/9 (10:46–15:05); Sky to Castor 1345/9 (off −0.0001, 11:13–12:43); RA to Sirius 1301/9; plus birth-hour ninths to Pallas, Mercury, Mars, Sedna, Jupiter, Saturn. 1 whole + 10 ninths (above chance, ~5.8), most within an hour of 12:00.
- Chords all day: Dec Gonggong–Saturn φ, 0.003% (Saturn's); **RA Fomalhaut–Pleiades φ, 0.022%** (≤0.155%); Dec Haumea–Mars 1:4:5 (Mars's); Dec Aldebaran–Antares φ (0.039% at 00:00); RA Algol–Procyon 3:4:7 (0.043% at 00:00). Birth-hour only: Dec Bellatrix–Rigel 1:8:9, 0.028%.
- Reads as: Chiron is a joint between Saturn and Neptune; its own chords are moderate.
(Eddie 21:19: "remember Pallas, Juno and Vesta" — still to do after the TNOs; Ceres done.)
#### ERIS (RA 24.113, Dec −4.974; slow)
- **Numbers — Eris–MAKEMAKE in both coordinates: RA 101φ (163.4214, off 0.0000, 09:02–14:55) and Dec whole 34 (02:32–18:05).** Sky to Rigel 488/9 (08:20–24:00). Birth-hour: RA to Juno 88√2, Flat to Vesta 496/9. (Own RA 217/9 set aside — own-RA rule.)
- Chords all day: **Dec Capella–Procyon 1:4:5, 0.006% (≤0.028%)**; **RA Capella–Polaris 1:3:4, 0.019% (≤0.057%)**; Dec Betelgeuse–Spica 1:2:3, 0.028%; Dec Algorab–Altair 5:6:11; RA Algol–Deneb Algedi 2:5:7. With bodies: **RA Mars–Neptune 1:1:2 — Mars at the midpoint of Eris and Neptune**; Dec Quaoar–Saturn 2:3:5 (Saturn's); Dec Jupiter–Sedna 5:8:13. Birth-hour only: RA Jupiter–Pluto 1:8:9, 0.001%.
- Reads as: Eris is tied to Makemake twice (φ in RA, whole in Dec), to MARS through the Neptune midpoint, and holds Capella twice. Procyon again (4th time).
#### Makemake (RA 187.534, Dec +29.026 — 5.6° out of bounds, as always; slow)
- Numbers: Eris RA 101φ and Dec whole 34 (Eris's); **Sky to PLEIADES 979/9 (off −0.0002, 08:32–15:00)**; RA to Deneb Algedi 1253/9 (09:55–18:22); Sky to Pluto 57φ (Pluto's); RA to Neptune 1229/9 (Neptune's). Birth-hour: Sky to Vesta 1289/9.
- Chords all day (mostly stars): **Dec Polaris–Rigel φ, 0.005% (≤0.028%)**; RA Altair–Spica 1:7:8, 0.025%; Flat Alphecca–Castor 5:8:13, 0.029%; Dec Altair–Bellatrix 1:8:9; Dec Deneb Algedi–Polaris 3:4:7; RA Pleiades–Rigel 1:5:6; **Dec Polaris–Spica 2:3:5 — MARS also holds Polaris–Spica (3:5:8): two-body string**. With bodies only loose ones (Ceres–Pallas √2 0.006% is birth-hour).
- Seen: Mars–Makemake Dec gap 2.518 = the Altair–Bellatrix Dec base (2.519); Mars and Makemake both hold Altair–Bellatrix (1:7:8, 1:8:9).
- Reads as: a star-holder, tied to the chart mainly through Eris (both ways) and Mars (shared strings).
#### HAUMEA (RA 204.851, Dec +19.205; slow)
- **Parallel ARCTURUS (19.205 vs 19.174, 0.031)** — so Haumea sits in the Mars lattice's Arcturus point as well as the Jupiter–Uranus lattice (Uranus 25, exact 04:00; Jupiter 41.995, near 42).
- Numbers, long windows: **RA to SEDNA 1390/9 (08:17–22:31)**; **RA to FOMALHAUT 1256/9 (00:05–16:47)**; Dec to Deneb Algedi 318/9 (04:39–13:32); **Sky to ALGORAB 28√2 (01:54–15:06)**; **Sky to ALPHECCA 17φ (00:00–14:57)**. Birth-hour: Sky to Juno 44√2, Flat to Ceres. With Uranus 25: 3 whole/φ/√2 held for hours + 3 ninths.
- Chords all day: **RA Betelgeuse–Regulus 5:6:11, 0.005% (≤0.010% all day)**; **Dec Deneb Algedi–Fomalhaut φ, 0.009% (≤0.024%)**; **Dec Algorab–Capella 3:4:7, 0.014%**; **RA Antares–Vega 3:4:7, 0.019% (≤0.026%)**; Flat Bellatrix–Regulus 3:4:7. With bodies: RA Pluto–Saturn √2 (Saturn's), **Dec Juno–Mars φ and Dec Chiron–Mars 1:4:5 (Mars's)**, Dec Orcus–Saturn 1:2:3.
- Reads as: Haumea is a strong slow body — five long-held numbers, four star chords at ≤0.02% all day, in both Dec lattices, and tied to Mars twice.
#### Quaoar (RA 258.272, Dec −15.609; slow)
- Numbers, all day: **Dec to SIRIUS 10/9 — ALL DAY**; **Dec to ALGOL 40√2 (00:00–23:26)**; Dec to Sedna 196/9 (00:00–15:38); Sky to Regulus 977/9 (07:25–14:27); RA to Procyon 1291/9 (11:27–18:12 — Procyon a 5th time). Birth-hour: RA to Ceres, Mars; Sky to Juno, Sun (45√2).
- Chords all day: **RA Algorab–Bellatrix 2:3:5, 0.019% (≤0.029%)**; **Dec Alkaid–Antares 1:6:7, 0.021% (≤0.030%)**; Dec Sirius–Spica 1:4:5, 0.029%; RA Alkaid–Deneb Algedi 3:4:7 (0.016% at 00:00); RA Bellatrix–Regulus 2:3:5. With bodies: Dec Eris–Saturn 2:3:5 (Saturn's); Sky Ketu–Orcus 1:6:6, 0.026% (Quaoar almost equidistant from Ketu and Orcus in Sky).
- Reads as: Quaoar holds Sirius and Algol by number all day; Alkaid twice more in its chords.
#### Gonggong (RA 333.688, Dec −14.980; slow)
- Numbers: **61/9 twice — Dec to RIGEL (00:00–12:17) and Sky to DENEB ALGEDI (10:14–18:18)**; RA to ORCUS 121√2 (09:25–12:40); Flat to Pallas 202/9 (birth-hour). Own Dec −14.980 (0.020 from −15, outside).
- Chords all day: **Dec Capella–Rigel 1:8:9, 0.006% (≤0.043%)**; **Dec Antares–Spica 1:3:4, 0.015% — ANTARES–SPICA now three bodies: Neptune (RA 3:5:8), Pluto (RA 1:2:3), Gonggong (Dec)**; Dec Aldebaran–Vega √2, 0.029%; Dec Pleiades–Polaris 3:5:8; Dec Alphecca–Polaris 2:3:5; RA Alphecca–Castor 5:6:7. With bodies: Dec Chiron–Saturn φ, 0.003% (Saturn's); Dec Pluto–Uranus φ (Uranus's).
- Reads as: Gonggong holds Rigel and Deneb Algedi by the same 61/9; joins the Antares–Spica string; ties into Saturn–Chiron and Pluto–Uranus.
#### ORCUS (RA 144.807, Dec −5.491; slow)
- Numbers: **Dec to ALDEBARAN = whole 22 (00:03–19:01)**; **Dec to MARS = whole 32** (Mars's); **Dec to ARCTURUS 222/9 (00:00–15:13)** — the Mars lattice confirmed from Orcus's side (Mars, Arcturus, Aldebaran, Orcus); Flat to Spica 511/9 (08:57–14:16); RA to Gonggong 121√2 (Gonggong's). Birth-hour: Sky to Sun, Pluto.
- Chords all day: **Dec Bellatrix–Pleiades 2:3:5, 0.010% (≤0.031%)**; **RA Fomalhaut–Polaris 1:2:3, 0.018% (≤0.016% at the ends)**; RA Algol–Arcturus √2; Dec Antares–Regulus 5:6:11 (0.006% at 24:00); Dec Arcturus–Pleiades 1:5:6; Dec Alphecca–Vega 3:8:11; Dec Alkaid–Antares φ. With bodies: **Dec Pluto–Sedna 1:1:2 (Orcus the midpoint)**; **RA Ceres–Mars 2:3:5**; Sky Ketu–Quaoar 1:6:6. Birth-hour: Dec Pallas–Vesta φ, 0.003%.
- Reads as: Orcus is a receiver again (as in Messi and Dettori) — Mars by whole number and chord, Pluto and Sedna through the midpoint, Gonggong by √2, Quaoar/Ketu — and it anchors the Mars star lattice.
#### Sedna (RA 50.406, Dec +6.170; slow)
- Numbers, long: **RA to FOMALHAUT = whole 66 (07:12–24:00)**; **RA to RAHU 57√2 (03:00–15:19)**; **Dec to SPICA 156/9 (02:49–24:00)**; RA to Haumea 1390/9 (Haumea's), Dec to Quaoar 196/9 (Quaoar's). Birth-hour: Sky to Mercury, Saturn, Chiron.
- Chords all day: **RA Altair–Polaris 1:8:9, 0.016%**; **Dec Antares–Vega 1:1:2, 0.028% — Sedna at the Dec midpoint of Antares and Vega** (Haumea holds Antares–Vega in RA); **Dec Alkaid–Rigel 1:3:4 — Saturn also on Alkaid–Rigel (1:2:3): two-body string**; Dec Arcturus–Spica 3:4:7; Dec Algol–Regulus 1:5:6. With bodies: Dec Juno–Jupiter φ, 0.008% (Jupiter's); Dec Orcus–Pluto (Orcus the midpoint). Birth-hour: Dec Mars–Sun (Sedna the midpoint, 0.76% at the ends).
- Reads as: Sedna holds Fomalhaut and Spica by number all day and the nodes by √2; it is a midpoint/partner more than a hub.
#### Transpluto (RA 150.325, Dec +12.113; hypothetical point, slow)
- Numbers: **own Dec 109/9 (12.1111 exact at 00:00, holds 00:00–14:46)** — own Dec counts (the equator is a fixed start); **Dec to VEGA 240/9 (07:07–24:00)**; Flat to Regulus 16/9 (02:43–13:02); Sky to Arcturus 552/9 (00:44–12:58); RA to Polaris 1012/9.
- **Chords all day — a four-star Dec set around DENEB ALGEDI:** Betelgeuse–Deneb Algedi 1:5:6, 0.006%; Capella–Deneb Algedi 5:6:11, 0.014% (0.003% at 00:00); Arcturus–Deneb Algedi 1:4:5, 0.016%; Arcturus–Betelgeuse 2:3:5, 0.020% — Transpluto makes a chord with each pair. Also Dec Algol–Sirius 1:1:2, 0.037% (Transpluto at the Dec midpoint of Algol and Sirius).
- With bodies: only loose (≥0.07%).
- Reads as: Transpluto is a star-holder (Deneb Algedi set) with its own Dec on a ninth; few ties to the other bodies.
#### Nodes (Rahu RA 329.797, Dec −12.303; Ketu RA 149.797, Dec +12.303; slow)
- Numbers, long (Rahu/Ketu pairs are one fact each): **Sky to FOMALHAUT whole 22 / 158 — ALL DAY**; **RA to BETELGEUSE whole 119 / 61 (05:38–16:32)**; **Sky to ALPHECCA 908/9 / 712/9 (off 0.0000, 04:59–19:58)**; Rahu Dec to Regulus 15φ (00:00–12:18); Rahu Flat to Deneb Algedi 44/9 (08:02–20:23); Sedna 57√2 (Sedna's); Neptune Sky whole 6 (Neptune's).
- Chords all day — Ketu is star-rich: **RA Alkaid–Bellatrix 5:6:11, 0.003% (≤0.016%)**; **RA Bellatrix–Fomalhaut √2, 0.012%**; **Dec Pleiades–Procyon 3:5:8, 0.013%**; Dec Algorab–Alphecca 1:2:3, 0.019%; Dec Altair–Arcturus 1:2:3, 0.019%; Dec Equator–Rigel 2:3:5, 0.023%; Dec Betelgeuse–Castor 1:4:5. Rahu: **RA Fomalhaut–Sirius 1:8:9, 0.004%**; RA Pleiades–Rigel 1:4:5, 0.017%. With bodies: Sky Orcus–Quaoar 1:6:6 (Ketu near-equidistant, with Quaoar); the rest loose.
- Reads as: the nodes hold Fomalhaut (whole number all day, and two chords), Betelgeuse (whole) and Alphecca (exact ninth). Procyon again (Pleiades–Procyon). Little direct tie to Mars/Jupiter.
#### Pallas (RA 354.845, Dec −7.488 at 12:00; 0.34°/d RA, 0.07°/d Dec)
- Numbers: 5 ninths, all within ~1 h of 12:00 — RA to Sirius 958/9, Chiron 343/9, Capella 759/9; Dec to Algol 436/9; Flat to Gonggong 202/9. Under chance.
- Chords, tight but birth-hour only (0.3–2% at the ends): Dec Bellatrix–Fomalhaut 5:8:13, 0.002%; RA Algol–Betelgeuse 4:5:9, 0.007%; Dec Orcus–Vesta φ, 0.003%; Dec Ceres–Makemake √2, 0.006%; Dec Juno–Uranus 2:5:7, 0.011%; RA Algol–Fomalhaut 1:5:6. Nothing all day except loose RA Mars–Saturn 5:6:11 (0.08%).
- Reads as: with a placeholder time, Pallas gives nothing to lean on.
#### Juno (RA 259.661, Dec −11.728 at 12:00; RA 0.26°/d, Dec 0.03°/d)
- Numbers: all within ~30 min of 12:00 — RA to Vesta 634/9 (off 0.0001), Eris 88√2; Dec to Venus 87/9, Sun 22/9; Flat to Pluto whole 12; Sky to Haumea 44√2, Quaoar 37/9.
- Chords all day — **Juno sits on both strong bodies' Dec chords: Dec Haumea–MARS φ, 0.019% (≤0.17%) and Dec JUPITER–Sedna φ, 0.008% (≤0.14%)**; with stars only ≥0.04% (Dec Polaris–Vega 1:1:2 — Vega the midpoint of Juno and Polaris; Dec Capella–Vega 1:7:8). Birth-hour: Dec Pallas–Uranus 2:5:7, 0.011%.
- Reads as: Juno's weight is through Mars and Jupiter (φ with each).
#### Vesta (RA 330.106, Dec −15.947 at 12:00; 0.50°/d RA, 0.16°/d Dec)
- Numbers: Dec to Venus 49/9 (03:12–12:35, Venus's — the one long window); the rest within ~30 min of 12:00 (RA Juno 634/9, Dec Sun 16/9, Flat Eris, Sky Makemake, Jupiter, Algorab).
- Chords, birth-hour only: Dec Capella–Rigel 1:7:8, 0.002% (1% at the ends; Gonggong holds Capella–Rigel 1:8:9 all day); RA Regulus–Spica φ, 0.008%; Dec Orcus–Pallas φ, 0.003%; Dec Castor–Equator 1:2:3, 0.021%. Nothing all day.
### FRANKEL — Method 1 summary (placeholder 12:00; weight on what holds all day)
- **MARS is the main body:** out of bounds (+26.508, 3.07° beyond) and near-stationary in Dec. Its star lattice in Dec — Mars, Arcturus, Aldebaran, Orcus on 10 / 22 / 32 and 66/9, 24/9 — held all day. Mars at the RA midpoint of Eris and Neptune; Jupiter–Mars–Neptune Dec 1:5:6 (≤0.05% all day); Ceres–Orcus RA 2:3:5; Haumea–Juno and Chiron–Haumea in Dec; shares Polaris–Spica and Altair–Bellatrix with Makemake.
- **JUPITER second:** Dec lattice with Uranus (17, exact 20:00) and Haumea (25 from Uranus, exact 04:00; 42 near) — both whole numbers together 08:09–08:45; Castor–Fomalhaut 1:8:9 0.001%, Polaris–Procyon, Juno–Sedna φ all day.
- **HAUMEA** in both lattices (parallel Arcturus 0.031); five long-held numbers; four star chords ≤0.02% all day; tied to Mars twice. **SATURN:** Chiron whole 21; four chords ≤0.02% all day. **ORCUS the receiver** (as in Messi and Dettori): Mars 32, Aldebaran 22, Arcturus 222/9, midpoint of Pluto–Sedna, Ceres–Mars, Gonggong 121√2. **NEPTUNE** joins Mars and Jupiter; the Sun is on Neptune (0.3°/0.4°). **ERIS** tied to Makemake in RA (101φ) and Dec (34) and to Mars through the Neptune midpoint.
- Shared star strings: Antares–Spica (Neptune, Pluto, Gonggong); Alkaid–Castor (Saturn, Ceres, Neptune); Alkaid–Rigel (Saturn, Sedna); Polaris–Spica, Altair–Bellatrix (Mars, Makemake); Capella–Rigel (Gonggong, Vesta). Recurring stars: PROCYON (six bodies), ALKAID, FOMALHAUT (nodes 22, Sedna 66, Haumea), BETELGEUSE (Pluto 221/9 all day, nodes 119).
- Fast bodies (Sun, Mercury, Venus, Pallas, Juno numbers, Vesta, Ceres): tight chords but birth-hour only — not leaned on.
- Compared: Messi — Sedna and Orcus hubs; lottery — Chiron and Transpluto hubs (one Dec lattice); Frankel — MARS (out of bounds) with Jupiter, two Dec whole-number lattices, ORCUS receiving.
### Method 3 — the race sky on Frankel's chart (off 14:34:00, finish ≈14:35:38; natal strings at 12:00, fnat/; m3f.sh)
#### Sun (RA 88.349, Dec +23.428 at the off — at its maximum Dec, solstice next day)
- **At the off: RA Aldebaran–Pleiades 5:8:13, 0.001%, exact 14:34:11 — 11 s after the off.** Not one of his natal strings (Aldebaran is in his Mars lattice; Pleiades by Makemake's Sky 979/9).
- Numbers at the off (3 vs ~2 expected): **Dec to ALKAID = 16φ and 233/9 together (25.8892)**; RA to Bellatrix 5√2; Dec to Deneb Algedi 356/9.
- On his strings: **Dec Aldebaran–Spica 1:4:5, 0.029% at the off — the SAME chord as natal SATURN (1:4:5, 0.036%)** (exact 09:37); RA Aldebaran–Sirius 2:3:5, exact 14:46 (12 min after) — the SAME chord as natal KETU (2:3:5, 0.092%, all day), Makemake too; RA Fomalhaut–Sirius 1:8:9 at 13:17:57 — the SAME chord as natal RAHU (1:8:9, 0.004%, all day), 76 min before.
- No parallels.
#### Mercury (RA 112.970, Dec +23.536 at the off — out of bounds by 0.10)
- **14:30:51 (3.2 min before the off): RA Betelgeuse–Regulus φ, 0.023% at the off — natal HAUMEA's tightest all-day string (5:6:11, 0.005%).**
- 14:32:17 (1.7 min before): Dec Alkaid–Bellatrix 2:3:5, 0.004% at the off — the same two stars as natal KETU's RA Alkaid–Bellatrix (0.003%, all day), other coordinate (Mercury took Ketu's RA string at 10:11).
- Mercury through the slow bodies' all-day strings around the race: 13:00:56 Orcus (Arcturus–Pleiades); 13:45:56 Gonggong (Capella–Rigel, natal 0.006%); **14:30:51 Haumea**; 14:51:55 Pluto (Algol–Arcturus); 15:09:33 Pluto (Procyon–Vega, natal 0.010%); 15:32:19 Orcus (Fomalhaut–Polaris, natal 0.018%).
- Numbers at the off: Dec to Altair 132/9; RA to Fomalhaut 1157/9 (about chance).
#### Venus (RA 67.303, Dec +19.039 at the off)
- **Numbers at the off — 6 hits (3 φ/√2 vs ~0.44 expected; 3 ninths vs ~1.5):** **RA to RIGEL 7φ and RA to SIRIUS 21φ** (the same fact as the RA Rigel–Sirius 1:2:3, 0.009%, exact 14:29:25); Dec to Regulus 5√2; Dec to Algorab 320/9, Polaris 632/9; RA to Fomalhaut 746/9.
- **Star strikes just before the off:** 14:27:37 Dec Aldebaran–Pleiades 1:2:3 (the Sun takes RA Aldebaran–Pleiades at 14:34:11 — the same pair in both coordinates 7 min apart); 14:29:25 RA Rigel–Sirius 1:2:3; 14:30:24 RA Polaris–Vega 1:4:5, 0.003% (natal Vesta, loose, birth-hour).
- On his all-day strings, nothing near the race: Eris's Capella–Polaris at 13:38 (56 min before); Orcus's Bellatrix–Pleiades at 15:25 (51 min after); Pluto's Bellatrix–Pleiades RA at 12:42.
- Jockey: sky Venus RA within 0.096 of Queally's natal Chiron.
- Reads as: Venus is busy with stars at the off (Rigel–Sirius by φ numbers, Aldebaran–Pleiades with the Sun), but not on Frankel's own strings at the race.
#### Mars (RA 173.638, Dec +3.466 at the off)
- **At the finish: Dec Bellatrix–Sirius 1:7:8, 0.014%, exact 14:35:48 — 10 s after the finish (≈14:35:38)** — natal TRANSPLUTO 1:4:5 (0.055%, all day; Pallas loose). Then Dec Betelgeuse–Pleiades φ, 0.015%, exact 14:37:36 (2 min after; not natal).
- Before: 14:23:12 Dec Aldebaran–Altair √2; 14:16:00 RA Algorab–Spica 1:1:2 (natal Pluto, loose); **13:47:12 RA Capella–Pleiades φ — natal JUPITER 1:6:7 (0.029%, all day)**, 47 min before.
- **12:15–12:33 — Mars lights Transpluto's four-star Deneb Algedi set: Arcturus–Deneb Algedi 12:15:24, Betelgeuse–Deneb Algedi 12:26:12 (the SAME chord as natal Transpluto, 1:5:6, 0.006%), Arcturus–Betelgeuse 12:33:24** — three strings in 18 min, two hours before the race. Morning: 06:53 Dec Algorab–Castor — natal MARS's own string (1:8:9, all day; same body).
- Numbers at the off: **RA to Fomalhaut 1537/9 (170.7778, exact)**; Dec to Rigel 105/9.
- Jockey: sky Mars Dec within 0.042 of Queally's natal Juno.
- Note: PLEIADES is struck by Sun (with Aldebaran, 14:34:11), Venus (with Aldebaran, 14:27:37) and Mars (Capella 13:47, Betelgeuse 14:37) — but Venus (RA 67) and the Sun (88) sit near Taurus, so Aldebaran/Pleiades chords come easily for them.
#### Jupiter (RA 59.643, Dec +19.722 at the off — next to the Pleiades in the sky)
- Numbers at the off — 6 hits (2 whole/φ vs ~0.44; 4 ninths vs ~1.5): **RA to CASTOR = whole 54 (53.9996)**; RA to Algorab 79φ; RA to Aldebaran 84/9, Pleiades 25/9, Regulus 832/9; Dec to Sirius 328/9.
- **Natal JUPITER's all-day string RA Capella–Pleiades (1:6:7, 0.029%) is struck by sky Mars at 13:47 (φ) and by sky JUPITER itself at 15:37 (1:7:8, same body) — 47 min before and 63 min after the race.**
- Nothing on his strings at the off itself (nearest: Ceres's Altair–Regulus 10:58; Orcus's Arcturus–Pleiades 15:35; Saturn's Capella–Pleiades Dec 16:06).
- Jockey: sky Jupiter Dec within 0.080 of Queally's natal Rahu.
#### Saturn (RA 201.887, Dec −6.380 at the off; slow — holds through the race)
- **Holding his strings all race: Dec Betelgeuse–Deneb Algedi √2, 0.021% — natal TRANSPLUTO 1:5:6, 0.006% (all day); sky Mars struck the same string with Transpluto's own 1:5:6 at 12:26.** **Dec Castor–Spica 1:8:9, 0.027% — natal MARS 1:7:8, 0.041%.** Also Vesta's Castor–Equator and Castor–Polaris (Vesta birth-hour).
- Not natal: Dec Betelgeuse–Sirius 3:4:7, 0.002% (exact 20:02); Dec Alphecca–Bellatrix 5:8:13, 0.006%.
- Numbers at the off: **RA to Alkaid = whole 5 (5.0014)**; Dec to Bellatrix 9√2; Dec to Algol 426/9 (exact), Aldebaran 206/9, Arcturus 230/9. (Own RA 1817/9 set aside.)
- Reads as: sky Saturn sits on MARS's and TRANSPLUTO's natal strings through the race.
#### URANUS (RA 7.753, Dec +2.570 at the off; slow — holds through the race)
- **Dec Altair–Bellatrix 2:3:5, 0.001% at the off (exact 14:43:00) — natal MARS 1:7:8 (all day) and MAKEMAKE 1:8:9 (all day), the string they share; Mercury, Ceres too.** Mars's string held at 0.001% through the race.
- **Dec Alkaid–Deneb Algedi 2:5:7, 0.009% — natal SATURN √2, 0.003% (Saturn's tightest all-day string).**
- **Dec Alphecca–Fomalhaut 3:4:7, 0.013% — the SAME chord as natal ORCUS (3:4:7, all day).** Dec Alphecca–Vega 1:2:3, 0.039% — ORCUS again (3:8:11, 0.043%).
- Looser: RA Altair–Fomalhaut (natal Sun 0.009%, birth-hour; Sedna); Dec Antares–Vega (Sedna's midpoint); Dec Aldebaran–Vega (Gonggong).
- Numbers at the off: RA to Aldebaran 551/9, Castor 953/9; Dec to Bellatrix 34/9 (chance).
- Reads as: sky URANUS holds three of the main natal bodies through the race — MARS (with Makemake) at 0.001%, SATURN at 0.009%, ORCUS twice (once in unison) — a slow stack like Messi's Saturn on Sedna.
- Eddie 21:48: "this is considered Frankel's highest rated performance" (Timeform 147).
#### Neptune (RA 335.083, Dec −10.991 at the off; slow)
- **RA Bellatrix–Regulus 2:3:5, 0.023% — the SAME chord as natal QUAOAR (2:3:5, 0.042%, all day)**; Makemake 1:2:3 too. The rest loose (≥0.066%): Transpluto's Aldebaran–Polaris, Mars's Algorab–Castor RA (0.122%), Sun/Sedna's Altair–Fomalhaut.
- Numbers: RA to Fomalhaut 84/9 only.
- Jockey: sky Neptune Dec within 0.058 of Queally's natal Eris.
#### Pluto (RA 278.818, Dec −19.310 at the off; slow)
- **Number: RA to PROCYON = whole 164 (164.0002)** — Procyon, the star six of his natal bodies hold.
- On his strings: **RA Alkaid–Deneb Algedi 2:3:5, 0.015% — natal QUAOAR 3:4:7 (0.041%, all day).** With Uranus on Dec Alkaid–Deneb Algedi (natal SATURN 0.003%), the ALKAID–DENEB ALGEDI pair is held in both coordinates through the race. Also Dec Pleiades–Polaris 0.054% (Gonggong 0.033%); Dec Arcturus–Bellatrix 0.019% (natal Sun, birth-hour).
- Not natal: RA Altair–Betelgeuse 1:8:9, 0.006%; Dec Betelgeuse–Pleiades 5:8:13, 0.009% (sky Mars takes Betelgeuse–Pleiades φ at 14:37:36).
#### Chiron (RA 338.982, Dec −2.738 at the off; slow)
- Quiet on his strings: Dec Arcturus–Equator 0.043% (natal Mars φ, loose 0.135% — the Arcturus point of the Mars lattice); RA Capella–Polaris 0.096% (Eris 0.019%); Dec Fomalhaut–Pleiades (Gonggong, loose).
- Numbers: Dec to Polaris = whole 92 (91.9982); Dec to Algorab 124/9.
#### Eris (RA 25.644, Dec −3.480 at the off)
- **Natal → transit Eris (Eddie's Messi/Dettori/lottery check): RA 1.5319, Dec 1.4940, Flat 2.1398, Sky 2.1368 — no ninth, φ, √2 or whole even at ±0.005.** (Eris barely moves on the foaling day, so the unknown time doesn't matter.) The Eris pattern does NOT repeat for Frankel.
- On his strings: RA Algol–Bellatrix 5:8:13, 0.038% — natal KETU 1:2:3 (0.035%, all day); Dec Alphecca–Vega 0.083% (Orcus; Uranus holds it tighter). The rest loose.
- Numbers at the off: **RA to CASTOR = whole 88 (87.9983)** — with sky Jupiter's RA to Castor whole 54, Castor taken by whole number twice; Dec to Betelgeuse 98/9; RA to Pleiades 281/9, Regulus 1138/9.
#### Makemake (sky, slow)
- Quiet: no numbers. On his strings only loosely — Dec Polaris–Spica 0.071%, its OWN natal string shared with MARS (same body, loose); RA Procyon–Regulus 0.035% (Haumea, loose); Dec Fomalhaut–Rigel, Altair–Regulus (birth-hour holders). Tight but not natal: RA Castor–Pleiades 3:4:7, 0.004%; Dec Algol–Antares 1:4:5, 0.023%.
#### Haumea (sky, slow)
- Quiet: one number (RA to Algol 1438/9); on his strings only Transpluto's Algol–Sirius, loose (0.116%). Natal → transit Haumea: RA 1.9646, Dec 0.4180, Flat 2.0085, Sky 1.9040 — no number. Natal Haumea is struck by others (Mercury 14:30:51), not by sky Haumea.
#### Quaoar (RA 262.696, Dec −15.386 at the off; slow)
- **Natal → transit Quaoar: Dec 0.2238 = 2/9 (+0.0016, a hit)**; RA 4.4243, Flat 4.4300, Sky 4.2692 — no number.
- Sits on the three-body ANTARES–SPICA string in both coordinates (loose): RA 0.093%, exact 00:13 (Pluto, Neptune 0.013%); Dec 0.080% (Gonggong 0.015%). Dec Alkaid–Rigel 0.080% (Sedna, Saturn).
- Numbers at the off: Dec to SIRIUS 12/9 (natal Quaoar's Dec to Sirius was 10/9), Dec to Spica 38/9.
#### Gonggong (sky, slow)
- Quiet: natal → transit RA 1.6637 (15/9 = 1.6667, −0.003, near), Dec 1.3753, Flat 2.1586, Sky 2.1191. Number: Dec to Aldebaran 271/9. On his strings only loosely (Chiron's Fomalhaut–Pleiades 0.083%; Juno's Aldebaran–Procyon).
#### Orcus (sky, slow)
- Number: **Dec to Fomalhaut = whole 23 (22.9987)**. Natal → transit: Flat 2.8861 (26/9, −0.0028, near); RA 2.6554, Dec 1.1306, Sky 2.8724 — nothing else.
- On his strings: RA Fomalhaut–Pleiades 0.036% (natal CHIRON φ 0.022%, ~all day: 0.11/0.155% at the ends); Dec Altair–Regulus 0.028% (Ceres 0.017%, birth-hour); Dec Algol–Bellatrix 0.042% (Transpluto, Pallas, loose). Natal ORCUS is held by sky Uranus (two strings), not by sky Orcus.
#### Sedna (sky RA 53.754, Dec +7.115 — near the Pleiades in RA; slow)
- Numbers at the off — 6 (1 φ + 5 ninths vs ~2): Dec to Regulus 3φ; RA to Regulus 885/9 (the same 885/9 as natal Sedna's Sky to Mercury), Aldebaran 137/9, Castor 539/9, Pleiades 28/9; Dec to Vega 285/9.
- On his strings: Dec Pleiades–Regulus 2:5:7, 0.028% — natal RAHU 1:2:3 (0.050%, all day); RA Pleiades–Rigel 0.089% (Rahu 0.017%, Makemake). Not natal: Dec Alphecca–Arcturus 5:8:13, 0.005%.
- Natal → transit Sedna: RA 3.3482, Dec 0.9452, Flat 3.4790, Sky 3.4573 — no number.
#### Transpluto (sky, slow)
- **Natal → transit Transpluto: Flat 0.8879 = 8/9 (−0.0010, a hit)**; RA 0.8355, Dec 0.3007, Sky 0.8709 — nothing else. No numbers to stars.
- On his strings: Dec Antares–Bellatrix 1:6:7, 0.023% — natal JUPITER 1:8:9 (0.044%; 0.2–0.3% at the day's ends); the rest loose (Eris's Algorab–Procyon, Chiron's Bellatrix–Rigel, Ketu's Altair–Arcturus ~0.1%).
#### Nodes (sky Rahu RA 242.913, Dec −21.105; Ketu RA 62.913, Dec +21.105)
- **Rahu on RA Regulus–Vega 2:5:7, 0.001% at the off, exact 14:41:12 (7 min after) — the SAME chord as natal VESTA (2:5:7, 0.045%; Vesta birth-hour, so weak with the placeholder time).**
- Numbers: **RA to ARCTURUS = whole 29 (Ketu 151)**; **Ketu Dec to PLEIADES = whole 3 (2.9987)**; RA to Antares 40/9; Polaris 1393/9 (Ketu 227/9); Dec to Vega 539/9; Ketu Dec to Capella 224/9.
- Natal nodes → transit nodes: no number. Others loose (Saturn's Aldebaran–Arcturus RA 0.037%; Neptune/Saturn's Alkaid–Castor Dec 0.12%).
#### Ceres (sky RA 56.900, Dec +15.384 — same RA as the Pleiades)
- **Dec Arcturus–Spica 1:7:8, 0.013% at the off, exact 14:39:24 (5 min after) — natal SEDNA 3:4:7 (0.039%, all day).**
- Before: 14:03:24 Dec Algorab–Betelgeuse 1:3:4 (Juno, loose). After: 15:01 RA Aldebaran–Rigel (natal Ceres, same body, birth-hour), 15:31 Procyon–Rigel (Vesta). Later 21:58 Dec Capella–Procyon (natal ERIS 0.006%, all day).
- Numbers: **RA to Alphecca = 125√2 and 1591/9 together**; Dec to Alphecca 102/9; RA to Betelgeuse 287/9. Natal → transit Ceres: no number.
#### Pallas (sky RA 5.280, Dec +5.811)
- RA Algol–Betelgeuse 1:1:2, 0.015% at the off (exact 15:19) — natal PALLAS (same body, 4:5:9 0.007%) and Mars (1:8:9) — both birth-hour, so weak. RA Algol–Altair φ, 0.019% (exact 13:58) — natal PLUTO 1:4:5 (0.049%, all day).
- Numbers: **RA to SIRIUS = whole 96 (95.9998)**; RA to ALKAID 112√2.
#### Juno (sky RA 234.977, Dec −2.222)
- Numbers at the off — 7 (1 φ-power + 6 ninths vs ~2): own Dec 20/9 (2.2224); Dec to Altair φ⁵; RA 1092/9 and Dec 307/9 to CASTOR; RA to Pleiades 1603/9, Regulus 746/9; Dec to PROCYON 67/9.
- Nothing tight on his strings (Pallas's Aldebaran–Procyon, Venus's Procyon–Spica, both ~0.1%).
#### VESTA (sky RA 50.538, Dec +13.273) — four of his all-day strings held through the race
- **Dec Algorab–Castor 5:8:13, 0.018% at the off (exact 14:05) — natal MARS's own string (1:8:9, 0.022%, all day)**; both sides tight.
- **Dec Antares–Spica 5:8:13, 0.011% (exact 13:54) — natal GONGGONG 1:3:4, 0.015% (the three-body Antares–Spica string)**; both sides tight.
- **Dec Equator–Rigel φ, 0.021% (exact 13:54) — natal KETU 2:3:5, 0.023%** (Rahu too).
- Dec Procyon–Rigel 3:5:8, 0.028% (exact 15:06) — natal PLUTO 2:3:5 (0.049%).
- Sequence: 13:52 Algol–Bellatrix (Transpluto, loose) · 13:54 Antares–Spica + Equator–Rigel · 14:05 Algorab–Castor (Mars) · [race 14:34–14:35:38] · 14:45 Algol–Polaris, 15:01 Polaris–Procyon (Gonggong, loose) · 15:06 Procyon–Rigel (Pluto). Vesta's Dec moves slowly, so the 13:54–14:05 chords are still within 0.011–0.021% at the off.
- Numbers: Dec to Aldebaran 2φ; **RA to CASTOR 39φ** (Castor by φ/whole from Jupiter 54, Eris 88, Vesta 39φ); Dec to Alphecca 121/9.
#### The MOON — the clock (RA 87.399, Dec +20.895 at the off)
- **NEW MOON that afternoon: the Moon is 0.68° behind the Sun in longitude at the off; exact New Moon ≈16:02 BST (15:02 UT), 1 h 28 min after the race.**
- **14:33:39 — 21 s before the off: Dec Altair–Arcturus φ — natal KETU 1:2:3 (0.019%, all day)** (Juno loose). Nothing on his strings inside the race itself (14:34:00–14:35:38); next is 14:39:19 RA Aldebaran–Sirius (Ketu/Makemake, loose — the Sun's 14:46 string).
- The run-in, 14:16–14:33 (natal holder): 14:16:39 Dec Alkaid–Antares (Quaoar 0.021%, ORCUS 0.043%) · 14:23:50 Dec Capella–Procyon (ERIS 0.006%) · 14:24:12 RA Pleiades–Rigel (RAHU 0.017%) · 14:27:23 Dec Algol–Altair · 14:27:29 Dec Bellatrix–Rigel (Chiron) · **14:31:05 RA Bellatrix–Pleiades (natal PLUTO 1:6:7, 0.015%, all day)** · 14:31:27 RA Castor–Rigel (Gonggong) · **14:33:39 Altair–Arcturus (KETU)**.
- Caution: in this hour the Moon makes a natal-linked chord every ~2 min (66 over the day list; 11 in 14:16–14:34), so a strike within a minute of the off is likely by chance; the last two before the off are on tight all-day strings (Pluto 0.015%, Ketu 0.019%).
- Numbers: Dec to Vega 161/9 only.
### Method 2 — tuned layers (Frankel, natal 12:00 placeholder; ft/*.txt)
- Counts — L1: Frankel 161 tuned / 9 UNISON / 6 same body / **5 both within 0.02%** (Queally 139/7/4/1; lottery chart 117/4/7/1). Nodes: 21/1/0/3 lengths in tune/1.
#### L1 — star bases
- **Both within 0.02% (5):** **Alkaid–Deneb Algedi Dec — natal SATURN 0.003% / sky URANUS 0.009%**; **Antares–Spica Dec — natal GONGGONG 0.015% / sky VESTA 0.011%**; **Altair–Arcturus Dec — natal KETU 0.019% / MOON 0.006% at 14:33:39 (21 s before the off)**; Algol–Betelgeuse RA — Pallas same body (natal birth-hour); Arcturus–Bellatrix Dec — natal Sun (birth-hour) / Pluto.
- Mars's strings: Algorab–Castor (natal 0.022% / Vesta 0.018%), Castor–Spica (0.041% / Saturn 0.027%), Altair–Bellatrix (Makemake 0.048% / Uranus 0.001%).
- UNISON (9): Aldebaran–Spica 1:4:5 (Saturn / Sun); Bellatrix–Regulus 2:3:5 (Quaoar / Neptune); Alphecca–Fomalhaut 3:4:7 (ORCUS / URANUS 0.013%); Regulus–Vega 2:5:7 (Vesta / Rahu 0.001%, 14:41); Castor–Rigel 1:3:4 (Gonggong / Moon 14:31:27); Antares–Spica RA 3:5:8 (Neptune / Mars 16:08); Altair–Fomalhaut 3:4:7 (Sun / Quaoar) and √2 (Sedna / Vesta); Aldebaran–Sirius 2:3:5 (Ketu / Sun 14:46).
- Reads as: L1 confirms Method 3 and ranks it — five pairs tight on both sides (lottery had one); the slow holds (Uranus on Saturn, Vesta on Gonggong and Mars) and the Moon on Ketu at the off are the tightest.
#### Nodes layer (21 tuned, 1 UNISON, 0 same body, 3 base lengths in tune, 1 both within 0.02%)
- **RA Rahu–Bellatrix: natal URANUS 1:5:6, 0.002%; sky MARS 3:4:7, 0.008% at the off (exact 14:43:30)** — both sides tight.
- **RA Rahu–Spica, UNISON 1:3:4: sky URANUS 0.000% — exact 14:31:07, 3 min before the off (holds through the race)**; natal SATURN 1:3:4 (loose, 0.138%). Uranus again with Saturn.
- **RA Ketu–Castor: sky ORCUS 2:3:5, 0.001% (exact 14:01)**; natal Quaoar 1:3:4, 0.044% — Castor again.
- Dec Rahu–Altair (base lengths in tune, √2): **natal MARS 5:6:11, 0.004%** — sky side loose (Quaoar, Gonggong ~0.11%).
- Reads as: the nodes add Mars on Rahu–Bellatrix during the race (with natal Uranus), Uranus exactly on Rahu–Spica in unison with Saturn, and Orcus on Ketu–Castor.
#### L2 — slow-body bases (167 tuned, 17 UNISON, 6 same body, 5 lengths in tune)
- **Inside the race — the Moon:**
  - **14:34:15 (15 s after the off): Moon 3:5:8 on Dec URANUS–CASTOR, 0.000% — natal MARS 1:6:7 on natal Uranus–Castor (loose, 0.076%).**
  - **14:35:30 (8 s before the finish): Moon 3:8:11 on Dec SEDNA–FOMALHAUT, 0.014% — natal JUNO 1:1:2, 0.005% and natal JUPITER φ, 0.029%** (Vesta too).
- **Uranus–Spica RA: sky RAHU 1:3:4, 0.000% (exact 14:31:07, through the race) — natal JUPITER 4:5:9, 0.013%** — both tight (the same three points as the Nodes layer's Rahu–Spica + Uranus).
- **Neptune–Eris RA — natal MARS at the midpoint (1:1:2, 0.038%) — sky CERES φ, 0.021%, exact 14:08:39** (25 min before).
- **Orcus–Aldebaran RA (the Mars lattice's stars, in RA) — sky MARS 1:3:4, 0.051% (exact 13:47:55), UNISON with natal Ceres (1:3:4, 0.030%) and SAME BODY with natal Mars (1:4:5, loose).**
- Neptune–Sirius Dec UNISON φ: natal ORCUS 0.006% / sky Vesta 0.031% (exact 16:05). Orcus–Regulus Dec UNISON 5:6:11: natal MARS 0.025% / Makemake (loose).
- Reads as: L2 brings the Moon into the race — on a Uranus–Castor base (Mars's) 15 s after the off and on Sedna–Fomalhaut (Juno, Jupiter) 8 s before the finish — and shows sky Rahu with natal Jupiter, and Mars's own midpoint base (Neptune–Eris) struck by Ceres before the off.
#### L3 — medium-body bases (114 tuned, 5 UNISON, 7 same body; natal Ceres/Pallas/Juno/Vesta bases depend on the placeholder time — Mars/Jupiter/Saturn Dec bases hold all day)
- In the race — Moon: **14:34:15 RA JUPITER–SIRIUS 1:2:3, 0.003%** (natal Sedna, loose 0.149%); 14:35:30 RA Vesta–Aldebaran 1:1:2, 0.014% (natal Pallas, loose) and RA Juno–Aldebaran (natal Rahu √2 0.002%, Juno birth-hour; Moon 0.063%).
- Before the off, on all-day natal bases: **Dec MARS–Juno — natal HAUMEA φ, 0.019% / sky Gonggong 1:2:3, 0.047%, exact 14:14:42**; Dec Jupiter–Juno — natal SEDNA φ, 0.008% / sky Quaoar 0.028% (exact 12:29); RA Mars–Aldebaran / Orcus–Aldebaran — Orcus and Mars both ways (exact 13:47:55); Dec Mars–Alkaid UNISON 5:8:13 — sky Ketu 0.037% (exact 13:46), natal Chiron loose.
- Birth-hour natal sides (weak): Ceres–Pallas (Makemake 0.006%) / Venus 14:27:30; Jupiter–Vega (Vesta) / Mercury 14:39:26; Pallas–Vesta (Orcus 0.003%, same body) / sky Orcus 13:59.
- Reads as: L3 adds the Moon on a Jupiter base 15 s after the off (natal side loose) and Mars–Juno (natal Haumea) struck 19 min before. Weaker than L1/L2.
#### L4 — Sun/Mercury/Venus/Moon bases (35 tuned, 3 UNISON, 2 same body; natal sides all depend on the placeholder time)
- Dec Mercury–Bellatrix: natal MARS at the midpoint (1:1:2, 0.015%) / sky HAUMEA φ, 0.027%, exact 14:27:59 (6 min before the off). Dec Sun–Antares: natal Eris 0.017% / sky Pluto 0.002% (exact 13:48). Rest loose; no Moon items.
#### FRANKEL — Method 2 put together
- L1 ranks Method 3: five pairs tight on both sides (lottery 1) — Uranus on Saturn's Alkaid–Deneb Algedi, Vesta on Gonggong's Antares–Spica and Mars's Algorab–Castor, the Moon on Ketu's Altair–Arcturus 21 s before the off; UNISON of Uranus with ORCUS (Alphecca–Fomalhaut 3:4:7).
- Nodes: sky MARS on natal Uranus's Rahu–Bellatrix (0.008% / 0.002%); sky URANUS exactly on Rahu–Spica in unison with Saturn (0.000%, from 14:31); sky Orcus on Ketu–Castor 0.001%.
- L2 puts the Moon inside the race: 14:34:15 on Uranus–Castor (0.000%; natal MARS's base, loose) and 14:35:30 on Sedna–Fomalhaut (natal JUNO 0.005%, JUPITER 0.029%) — 15 s after the off and 8 s before the finish. Sky Rahu with natal Jupiter on Uranus–Spica (0.000% / 0.013%). Mars's midpoint base Neptune–Eris struck by Ceres 14:08.
- L3/L4 (time-dependent natal sides): Moon on Jupiter–Sirius 14:34:15 (natal loose); Mars–Juno (natal Haumea) by Gonggong 14:14; Haumea on Mercury–Bellatrix (natal Mars midpoint) 14:28.
- Reads as: Method 2 adds what Method 3 couldn't see — the Moon striking Mars's and Jupiter's body-bases inside the 98 s, and the nodes tying sky Mars and sky Uranus to natal Uranus and Saturn.

## §77 DONCASTER 14:40, 18 Mar 2022 — RE-READ with the three methods body by body (Eddie 22:20: "ok Doncaster next")
- Off 14:40:41, finish 14:44:49 (4m 7.70s), 5 ran: 1st Olympe De Gouges 25/1 (David Noonan) P03/P04 · 2nd Oot Ma Way 5/6F (Conor O'Farrell) P05/P06 · 3rd Poetria 15/8 (Jamie Hamilton) P07/P08 · 4th Fiamette 5/1 (James Davies) P01/P02 · 5th Suntory Star 80/1 (Stephen Mulqueen) P09/P10. All charts at 12:00 (midday rule). Method 2 was done before (§62); Method 1 was the blank-sheet imprint (#4); Method 3 not yet run.
### Out of bounds and near-stationary bodies, all ten charts (new check, 7 Oct lessons)
- All five horses (2018 foals) have CERES far out of bounds (+26 to +32) — a cohort feature, not individual. Oot Ma Way also VENUS +25.008 (1.57 out).
- Jockeys: **Stephen Mulqueen (last, 80/1): MARS +26.803 — 3.36 out, and Mars near its station (RA −0.013/d, Dec −0.025/d)** — the same picture as Frankel's Mars. James Davies: Mars −23.845 (0.40 out), Jupiter on the edge. Conor O'Farrell: Uranus (0.25), Vesta (0.13). **David Noonan (winner's jockey) and Jamie Hamilton: nothing out of bounds.**
- Near-stationary: Jupiter in the Feb 2018 foals (Olympe De Gouges Dec −0.014/d, Suntory Star −0.011/d) and Fiamette (Jupiter at station); Fiamette Ceres; Poetria Vesta Dec; Davies Jupiter; Mulqueen Mars and Jupiter.
### Method 1 — Olympe De Gouges (P03, 12:00)
#### Sun (RA 329.701, Dec −12.339)
- Numbers — 4 φ/√2/whole (vs ~1.7) + 4 ninths: **Flat to ARCTURUS = whole 120 (off 0.0001)**; Flat to Uranus 41√2; Flat to Bellatrix 80√2; Dec to Neptune 3φ; Dec to Pleiades 328/9, Pluto 83/9, Procyon 158/9; Sky to Capella 1011/9.
- Chords with stars: **RA Alphecca–Altair 1:2:3, 0.010%**; **RA Altair–Arcturus φ, 0.017% — the base sky Mars struck at the off (1:6:7, 0.003%; only this horse tuned, §62)**; Dec Betelgeuse–Equator 3:5:8, 0.030%.
- With bodies: RA Neptune–Venus 5:8:13, 0.009%; Dec Makemake–Uranus √2, 0.026%.
- Reads as: the Sun's numbers and chords run to ARCTURUS and ALTAIR — Arcturus by whole 120, Altair–Arcturus by φ (the off-time base).
#### Mercury (RA 329.629, Dec −14.510)
- **Mercury and the Sun share an RA (0.07° apart; Dec 2.17 apart).**
- Numbers — 8 ninths, no φ/√2/whole: RA to Sedna 777/9, Polaris 614/9, Transpluto 1585/9, Venus 84/9; Dec to Alphecca 371/9, Polaris 934/9; Sky to Ceres 1421/9.
- Chords: **Dec Arcturus–Procyon √2, 0.004%** (Arcturus again); Sky Alkaid–Fomalhaut 1:6:7, 0.024%; RA Algol–Fomalhaut φ. With bodies: **Dec Saturn–Uranus 1:3:4, 0.012%**; **Dec Haumea–Mars φ, 0.017%**; RA Jupiter–Ketu 1:7:8, 0.020%.
#### Venus (RA 338.964, Dec −10.422)
- **Numbers — 4 whole + 10 ninths (vs ~1.7 and ~5.8): RA to SEDNA whole 77; Dec to SATURN whole 12; Flat to ANTARES whole 93; Sky to PROCYON whole 136**; ninths to Transpluto (1571/9, off 0.0001), Fomalhaut, Polaris, Mercury, Eris, Altair, Spica, Pleiades, Chiron.
- Chords loose: the tightest star chord Dec Capella–Castor 1:3:4, 0.052%; with bodies RA Neptune–Sun 5:8:13 (the Sun's).
- Reads as: Venus is a numbers body — four whole numbers (two bodies, two stars) — with weak chords.
#### Mars (RA 251.128, Dec −21.838; Dec −0.09°/d, inside the bounds)
- Numbers — 2 φ/√2 + 9 ninths: **RA to ARCTURUS 23φ** (Arcturus a third time: Sun Flat 120, Mercury's Arcturus–Procyon); **Dec to JUNO 9√2 (off 0.0001)**; RA to Antares 34/9 (off 0.0001); Dec to Chiron 212/9, Transpluto 295/9, Sirius 46/9; Flat to Altair 502/9, Haumea 481/9, Alkaid 754/9; RA to Betelgeuse 1461/9.
- Chords: **Dec Rigel–Sirius 3:5:8, 0.005%**; **Dec Altair–Polaris φ, 0.016% (≤0.17% all day)**; Dec Altair–Castor 3:4:7, 0.042%; Dec Polaris–Vega 5:6:11 (0.021% at 00:00); **ALTAIR in six of Mars's ten star chords**. With bodies: **Sky Neptune–Pluto √2, 0.008%**; Dec Haumea–Mercury φ (Mercury's).
- Reads as: Mars runs to ALTAIR (six chords) and Arcturus (23φ) — the two stars of the Altair–Arcturus base sky Mars struck at the off (his Sun φ and his own Mars both tuned there, §62).
#### Jupiter (RA 230.210, Dec −17.234; Dec near-stationary)
- Numbers: Flat to SEDNA whole 176 (11:54–13:22); RA to Castor 1049/9 (11:03–12:32), Regulus 703/9, Vesta 211/9; Sky to Neptune 997/9 (11:07–14:44). 1 whole + 4 ninths — about chance.
- Chords modest, all day (Dec stationary): Sky Aldebaran–Procyon 2:5:7, 0.027% (0.019% at 00:00); Dec Capella–Rigel 1:6:7, 0.039%; RA Alkaid–Castor 1:4:5; Dec Arcturus–Spica 1:5:6 (0.019% at 00:00). With bodies: RA Ketu–Mercury 1:7:8 (Mercury's), Dec Juno–Neptune 1:5:6, 0.024%.
- Reads as: a quiet steady body; Sedna by whole number (Venus also whole 77 to Sedna in RA).
#### Saturn (RA 276.555, Dec −22.423; slow)
- Numbers: RA to Transpluto 87√2; Dec to Venus whole 12 (Venus's); RA to Alkaid 627/9; Flat to Polaris 1484/9, Rahu 1302/9; Sky to Transpluto 1121/9 — Transpluto twice. (Own RA 2489/9 set aside.)
- Chords all day: RA Arcturus–Castor 5:8:13, 0.029% (Arcturus again); RA Antares–Sirius 1:5:6, 0.029%; Dec Betelgeuse–Sirius φ, 0.030% (0.007% at 24:00); RA Algol–Deneb Algedi 5:8:13. With bodies: **Dec Neptune–Rahu 5:8:13, 0.027% (≤0.077% all day)**; Dec Chiron–Transpluto φ, 0.028%; Dec Juno–Sedna 4:5:9, 0.022%. Birth-hour: Dec Mercury–Uranus 1:3:4 (Mercury's).
#### URANUS (RA 23.522, Dec +9.231; slow — the earlier imprint's #2-pair body)
- Numbers: RA to Spica 1600/9 (11:24–14:12); Sky to PROCYON 814/9 (11:48–14:34); Flat to Sun 41√2 (the Sun's).
- **Chords with bodies, all day: RA ORCUS–SEDNA 1:3:4, 0.004% (≤0.045% all day)**; **Dec ERIS–RAHU φ, 0.006% (≤0.098%)**; Dec Gonggong–Rahu 1:3:4, 0.049% (0.035% at 00:00); Sky Neptune–Transpluto 1:3:4.
- Chords with stars, all day: **RA Fomalhaut–Vega 3:5:8, 0.017% (≤0.061%)**; RA Regulus–Rigel 3:4:7, 0.035% (0.004% at 24:00); Flat Betelgeuse–Procyon 2:5:7, 0.038%; Dec Bellatrix–Sirius 1:8:9, 0.041%.
- Reads as: Uranus is the strongest slow body so far — Orcus–Sedna and Eris–Rahu held all day at 0.004–0.006%.
#### Neptune (RA 344.753, Dec −7.484; slow)
- Numbers: Dec to BETELGEUSE 134/9 (10:28–17:15); RA to Rahu 1372/9 / Ketu 248/9 (one fact); Flat to Castor 1213/9; Sky to Jupiter 997/9 (Jupiter's); Dec to Sun 3φ (the Sun's).
- Chords all day: **Dec Bellatrix–Deneb Algedi 5:8:13, 0.014%**; Dec Antares–Pleiades 3:5:8, 0.034%; Dec Bellatrix–Fomalhaut 5:8:13, 0.043%. With bodies: **RA Chiron–Pallas 1:5:6, 0.013% (≤0.19%)**; Dec Rahu–Saturn 5:8:13 (Saturn's, all day); RA Chiron–Quaoar 1:7:8. Birth-hour: Sky Mars–Pluto √2, 0.008% (Mars's); RA Sun–Venus 5:8:13 (the Sun's).
- Reads as: moderate; Bellatrix three times in its Dec chords.
#### Pluto (RA 291.620, Dec −21.562; stationary in Dec)
- Numbers: **Dec to PLEIADES 411/9 (04:23–24:00)**; RA to CAPELLA 1328/9 (off 0.0001, 10:31–13:44); RA to Sirius 1527/9 (11:25–14:38), Bellatrix 1347/9; Sky to Fomalhaut 431/9 (08:54–12:44). 6 ninths, several long.
- Chords all day (Dec stationary): **Dec Fomalhaut–Sirius 3:5:8, 0.014% (≤0.062%)**; **Dec Regulus–Vega 4:5:9, 0.023% (≤0.027% all day)**; **Dec Alphecca–Vega 1:4:5, 0.025% (≤0.027%)**; Dec Alphecca–Betelgeuse 2:3:5; Dec Castor–Rigel 1:3:4. With bodies: Dec Ceres–Rahu 2:5:7, 0.023%; RA Eris–Ketu 3:8:11, 0.036%.
- Reads as: Pluto is fixed all day on Vega strings (Regulus–Vega, Alphecca–Vega) and Fomalhaut–Sirius.
#### Chiron (RA 355.216, Dec +1.718; slow)
- Numbers: **Sky to FOMALHAUT whole 33 (09:24–12:16)**; **Dec to Transpluto 83/9 (11:13–17:19) — the same 83/9 as the Sun's Dec to Pluto**; Dec to Sirius 166/9 (11:30–16:31), Mars 212/9 (Mars's); RA to Makemake 1433/9, Gonggong 174/9; Sky to Spica 1372/9, Sedna 547/9.
- Chords all day: **Dec Alkaid–Deneb Algedi 3:8:11, 0.010% (≤0.084%)**; Dec Aldebaran–Betelgeuse 5:8:13, 0.013% (≤0.18%); RA Alkaid–Antares 3:8:11, 0.032% (≤0.055%); Dec Betelgeuse–Procyon 5:8:13, 0.004% (0.27% at the ends). With bodies: RA Neptune–Pallas 1:5:6 (Neptune's), Dec Saturn–Transpluto φ (Saturn's), RA Pallas–Quaoar 5:8:13, 0.026%.
- Reads as: Chiron is star-rich (16 chords); Alkaid twice; Fomalhaut by whole 33.
#### Ceres (RA 134.281, Dec +31.599 — 8.16° out of bounds, as for all the 2018 foals)
- Numbers: RA to ORCUS whole 19, RA to Eris 77√2 (birth-hour); Dec to Alphecca 44/9 (11:24–12:56); Flat to Procyon 295/9 (11:25–12:41).
- Chords: RA Capella–Polaris 3:4:7, 0.009% (0.2% at the ends); **Dec Antares–Procyon 5:6:11, 0.022% (≤0.14%)**; Dec Pluto–Rahu 2:5:7, 0.023% (Pluto's).
- Reads as: modest; out of bounds is shared with every horse in the race.
#### Pallas (RA 47.536, Dec −16.939; 0.16°/d RA, 0.11°/d Dec)
- Numbers: RA to ANTARES 99φ; RA to Aldebaran 193/9, Pleiades 84/9; Dec to Spica 52/9 — all at 12:00.
- Chords: **Dec Orcus–Sedna 3:8:11, 0.002%** (at 12:00; 1.5% at the ends) — Uranus holds Orcus–Sedna in RA all day (0.004%); RA Chiron–Neptune 1:5:6, 0.013% (all day); RA Chiron–Quaoar 5:8:13, 0.026% (Chiron's). Star chords loose (≥0.038%).
#### Juno (RA 327.288, Dec −9.110; at 12:00)
- Numbers — 4 whole/√2 + 6 ninths: **RA to SIRIUS whole 134 (off 0.0001)**; **Flat to CASTOR whole 152**; **Sky to ANTARES whole 77** (Venus's RA to Sedna is also whole 77); Dec to Mars 9√2 (Mars's); own Dec 82/9; ninths to Capella, Pluto (twice), Vega, Sedna.
- Chords: **Dec Alphecca–Procyon 2:3:5, 0.003%** (Procyon again); Dec Saturn–Sedna 4:5:9 (Saturn's), Dec Jupiter–Neptune 1:5:6 (Jupiter's).
- Reads as: like Venus, a numbers body (three whole numbers to stars).
#### Vesta (RA 253.656, Dec −16.835)
- Numbers: Dec to SIRIUS 1/9 (0.110 — just outside the 0.1 parallel); Dec to Transpluto 250/9 (11:37–13:52); Sky to Capella 93φ (11:39–12:39), Orcus 871/9; RA to Jupiter 211/9; Flat to Rahu 1090/9.
- Chords loose (all ≥0.037%): Dec Alkaid–Procyon 1:2:3, Dec Antares–Regulus 1:3:4, Dec Arcturus–Regulus 1:4:5. A quiet body.
#### ERIS (RA 25.385, Dec −2.388; slow)
- **Numbers, held for long stretches:** **Dec to ANTARES 17√2 (00:00–14:47)** and Flat to Antares 1261/9 (00:00–13:24) — Antares twice; **Dec to MAKEMAKE 19√2 (10:49–24:00)**; **Sky to GONGGONG whole 50 (00:00–12:01)**; Dec to ARCTURUS 194/9 (10:26–24:00); Sky to Fomalhaut 427/9 (08:05–22:08). 3 √2/whole + 3 ninths, all long.
- **Chords all day:** **RA Bellatrix–Procyon 3:5:8, 0.004% (≤0.008% all day)**; **Dec Betelgeuse–Castor 2:5:7, 0.016% (≤0.039%)**; with bodies: **Dec Rahu–Uranus φ, 0.006%** (Uranus's Eris–Rahu seen from Eris); **Dec KETU–SEDNA √2, 0.013% (≤0.054%)**; RA Ketu–Pluto 3:8:11, 0.036%; RA Gonggong–Sedna φ, 0.052% (constant).
- **Tie to Method 2 (§62): the Moon struck Eris bases during the race — Eris–Ketu with his SEDNA √2 (0.013%, the only chart) and Eris–Alphecca with his Pallas (0.010%).** Eris–Ketu–Sedna is the √2 seen here from Eris's side.
- Reads as: ERIS is a strong body for this horse — long-held √2/whole numbers (Antares, Makemake, Gonggong), Bellatrix–Procyon at 0.004% all day, and the node–Sedna √2 the Moon played in the race.
#### SEDNA (RA 55.962, Dec +7.529; slow)
- **Numbers, long — 4 whole + 6 ninths:** **Sky to FOMALHAUT = whole 78 — ALL DAY (off 0.0003)**; RA to Fomalhaut 644/9 (09:38–24:00) — Fomalhaut twice; **Flat to ANTARES = whole 172 (11:48–24:00)**; Flat to Jupiter whole 176 (Jupiter's); RA to Venus whole 77 (Venus's); **RA to POLARIS 163/9 (off 0.0001)** and Sky to Polaris 736/9 (00:00–15:50); Dec to Alkaid 376/9 (05:45–24:00); RA to Transpluto 878/9 (10:10–19:18).
- Chords all day: **Dec Algorab–Capella 5:8:13, 0.013% (≤0.023%)**; RA Castor–Regulus 2:3:5; Dec Antares–Sirius 2:5:7. With bodies: **RA Orcus–Uranus 1:3:4, 0.004%** (Uranus's Orcus–Sedna); **Dec Eris–Ketu √2, 0.013% — the base the Moon struck in the race (§62)**; Dec Gonggong–Quaoar 1:6:7 (0.001% at 24:00).
- **Recurring stars so far for the horse:** ANTARES by whole/√2/φ from Venus (Flat 93), Juno (Sky 77), Eris (Dec 17√2), Sedna (Flat 172), Pallas (RA 99φ); FOMALHAUT from Sedna (78 all day), Chiron (33), Eris, Pluto, Venus; ARCTURUS (Sun 120, Mars 23φ, Eris, Mercury, Saturn); PROCYON (Venus 136, Juno, Eris's 0.004% chord, Mercury, Uranus).
- Reads as: Sedna is the strongest number body — Fomalhaut whole 78 all day, Antares 172 — and sits on the Uranus–Orcus and Eris–Ketu figures.
#### Haumea (RA 213.915, Dec +16.522; slow)
- **Parallel ALDEBARAN (16.508, 0.014) and contraparallel ALGORAB (−16.517, 0.005)** — Haumea sits at Aldebaran's Dec and mirrors Algorab across the equator.
- Numbers, long: **Flat to KETU 67φ (01:43–15:42)**; RA to Altair 754/9 (00:00–20:48), Algorab 238/9 (11:33–24:00); Dec to Regulus 41/9 (04:23–13:27); Dec to Rahu 1/9 (0.110, just outside a parallel); Flat to Gonggong 1128/9.
- Chords all day: **Dec Antares–Equator 5:8:13, 0.015% (≤0.047%)** — Antares again; Dec Fomalhaut–Spica 2:3:5; Dec Altair–Spica φ; RA Antares–Castor 1:3:4. With bodies: RA Quaoar–Rahu 3:4:7, 0.050%; Dec Mars–Mercury φ (Mercury's, birth-hour).
#### Makemake (RA 195.995, Dec +24.480; slow)
- Numbers, long: **Dec to ANTARES 36√2 (off 0.0002, 07:56–17:13)** — Antares again (6th body); Dec to Eris 19√2 (Eris's); Dec to Quaoar 361/9 (11:01–23:47); Flat to Altair 926/9, Alkaid 244/9; Sky to Castor 641/9, ARCTURUS 157/9 (11:21–19:46).
- Chords: Dec Algol–Sirius 2:5:7, 0.026% (all day); Dec Alphecca–Altair 1:7:8, 0.006% (0.26% at the ends); Dec Betelgeuse–Sirius √2. With bodies: Dec Gonggong–Uranus √2, 0.054%.
#### Quaoar (RA 271.482, Dec −15.629; slow)
- Numbers, long: **Sky to ALKAID 61√2 (off 0.0000, 05:41–18:32)**; **Sky to DENEB ALGEDI whole 53 (06:25–12:33)**; Dec to Algorab 8/9 (06:59–24:00); Dec to Makemake 361/9 (Makemake's).
- Chords few and loose with stars (≥0.045%); with bodies: RA Chiron–Pallas 5:8:13 (Chiron's), Dec Gonggong–Sedna 1:6:7, 0.036% (0.001% at 24:00), RA Haumea–Rahu 3:4:7.
#### Orcus (RA 153.279, Dec −10.266; slow)
- Numbers: **Sky to RIGEL 52√2 (off 0.0001, 09:04–14:45)**; Dec to Algol 461/9 (08:27–24:00); RA to Ceres whole 19 (Ceres's).
- Chords: Dec Fomalhaut–Procyon 4:5:9, 0.026% (0.003% at 00:00); star chords otherwise ≥0.049%. With bodies: **RA Sedna–Uranus 1:3:4, 0.004%** — the Uranus–Orcus–Sedna figure (Orcus the RA point between Sedna and Uranus at 1:3:4), held all day; Dec Pallas–Sedna 3:8:11 (birth-hour).
- Reads as: Orcus is not a receiver here; it is held in the Uranus–Sedna figure.
#### Gonggong (RA 335.884, Dec −12.322; slow)
- **Parallel the natal SUN at 12:00 (−12.339, 0.017)** — the Sun moves 0.35°/d in Dec, so this holds for the midday chart.
- Numbers: **Flat to POLARIS whole 119 (02:50–16:39)**; Sky to Eris whole 50 (Eris's); Dec to ANTARES 127/9 (10:30–24:00) — Antares a 7th time; Flat to Deneb Algedi 89/9; RA to Makemake, Chiron (theirs).
- Chords all day, several at 0.02–0.04%: Dec Aldebaran–Rigel 1:6:7, 0.021%; Dec Pleiades–Regulus 1:2:3, 0.029%; RA Capella–Polaris 2:3:5, 0.031%; Dec Aldebaran–Fomalhaut 3:5:8, 0.032%; Dec Alkaid–Equator 1:4:5. With bodies: Dec Quaoar–Sedna 1:6:7, 0.036%.
#### TRANSPLUTO (RA 153.519, Dec +10.941; slow)
- Numbers, long: **Dec to SIRIUS 249/9 — ALL DAY (off 0.0001)**; **Flat to ANTARES whole 101 (06:30–16:28)** — Antares an 8th time; **RA to BETELGEUSE 40φ (11:14–21:37)**; RA to Fomalhaut 1522/9 (05:09–15:28), Polaris 1041/9, Sedna 878/9 (Sedna's); RA to Saturn 87√2 (Saturn's); Dec to Chiron 83/9 (Chiron's).
- **Chords all day:** **ARCTURUS–PLEIADES in both coordinates — Dec 3:5:8, 0.001% (≤0.022% all day) and RA 5:8:13, 0.021%**; Flat Fomalhaut–Rigel 4:5:9, 0.019%; Dec Equator–Rigel 3:4:7, 0.022%; Dec Aldebaran–Vega 1:4:5, 0.030%; RA Fomalhaut–Pleiades 3:4:7; RA Aldebaran–Fomalhaut 1:1:2. With bodies: **Dec KETU–RAHU 1:5:6, 0.003% (≤0.011% all day)** — Transpluto on the node axis.
- Reads as: Transpluto is the strongest star-chord body for the horse — Arcturus–Pleiades at 0.001% (Dec) and 0.021% (RA), Sirius all day, Antares whole 101, the nodes at 0.003%.
#### Nodes (Rahu RA 137.199, Dec +16.412; Ketu RA 317.199, Dec −16.412)
- **A Dec cluster at ~16.5: Rahu +16.412 parallel ALDEBARAN (+16.508, 0.096); Haumea +16.522 parallel Aldebaran (0.014) and contraparallel ALGORAB (−16.517, 0.005); Haumea–Rahu 1/9.**
- Numbers: **Ketu Flat to ALPHECCA whole 94 (10:30–17:12)**; Ketu Flat to Haumea 67φ (Haumea's); RA to Deneb Algedi 1534/9 / 86/9 (07:44–13:10); Sky to Algol 715/9 / 905/9.
- Chords all day: **Rahu RA Aldebaran–Alphecca √2, 0.001% (≤0.026%)**; **Ketu RA Alphecca–Vega 5:6:11, 0.007% (≤0.028%)** — Alphecca three times (with the whole 94); Ketu Dec Alkaid–Altair 5:8:13, 0.020%; Ketu Dec Fomalhaut–Polaris 1:8:9, 0.025%; Rahu Dec Equator–Rigel 1:2:3, 0.023%. With bodies: Transpluto 1:5:6 (0.003%), Eris–Uranus φ (0.006%), **Eris–Sedna √2 (0.013%, the Moon's race string)**.
### OLYMPE DE GOUGES — Method 1 put together
- **Strongest bodies (all day):**
  - **TRANSPLUTO** — Arcturus–Pleiades in Dec (0.001%) and RA (0.021%); Sirius 249/9 all day; Antares whole 101; on the node axis (Rahu–Ketu 1:5:6, 0.003%).
  - **SEDNA** — Sky to Fomalhaut whole 78 all day; Antares whole 172; Polaris 163/9.
  - **ERIS** — Antares 17√2, Makemake 19√2, Gonggong whole 50; Bellatrix–Procyon 0.004% all day.
  - **URANUS** — RA Orcus–Sedna 1:3:4 (0.004%) and Dec Eris–Rahu φ (0.006%), all day.
- **Figures held all day between bodies:** Uranus–Orcus–Sedna (RA 1:3:4); Eris–Uranus–Rahu (Dec φ); **ERIS–KETU–SEDNA (Dec √2, 0.013%) — the Moon played this base in the race (§62)**; Transpluto on Rahu–Ketu.
- **Recurring stars:** **ANTARES — eight bodies by whole/√2/φ/ninth** (Venus 93, Juno 77, Eris 17√2, Sedna 172, Transpluto 101, Makemake 36√2, Pallas 99φ, Gonggong 127/9; Haumea's Antares–Equator chord); **ARCTURUS** (Sun 120, Mars 23φ, Transpluto's Arcturus–Pleiades, Eris, Makemake, Mercury, Saturn); FOMALHAUT (Sedna 78, Chiron 33); PROCYON; ALPHECCA (nodes).
- **Fast bodies (at 12:00):** Sun and Mercury share an RA; the Sun's φ on ALTAIR–ARCTURUS and Mars's six Altair chords — the base sky Mars struck at the off (§62).
- Out of bounds: only Ceres (shared by all five horses).
### Method 1 — David Noonan (P04, 4 Oct 1995, 12:00)
#### Sun (RA 189.973, Dec −4.296)
- Numbers: only **RA to FOMALHAUT 1390/9 (off 0.0000)** — under chance.
- Chords: **Dec Alphecca–Castor 1:6:7, 0.006%**; Dec Betelgeuse–Rigel 1:3:4, 0.032%; Dec Bellatrix–Pleiades 3:5:8. With bodies: **RA Mars–Pluto 3:8:11, 0.023%**; RA Venus–Vesta √2, 0.030%.
- A quiet Sun.
#### Mercury (RA 190.139, Dec −6.932; retrograde)
- **Sun and Mercury share an RA (0.17° apart) — as in the horse's chart (0.07°).**
- Numbers — **five √2** (vs ~1.7 φ/√2/whole) + 5 ninths: RA to VEGA 63√2; Flat to TRANSPLUTO 34√2, PALLAS 15√2; Sky to POLARIS 69√2, QUAOAR 35√2; Dec to Pluto 2/9, Mars 98/9, Sirius 88/9, Algol 431/9; Flat to Castor 772/9.
- Chords with stars: **ARCTURUS twice in Dec — Arcturus–Regulus φ, 0.007%; Algol–Arcturus 5:6:11, 0.009%** (Arcturus, the horse's recurring star); RA Arcturus–Regulus 5:8:13, 0.034%; RA Pleiades–Sirius 1:2:3, 0.028%; RA Alkaid–Alphecca 5:8:13, 0.028%.
- With bodies: **Dec Chiron–Venus φ, 0.002%**; **RA Chiron–Pallas 5:8:13, 0.003%**; **Dec Quaoar–Uranus 1:1:2, 0.014% (Mercury at the midpoint)**; Dec Haumea–Orcus φ, 0.028%.
#### Venus (RA 201.432, Dec −8.046)
- **Numbers — 4 φ/√2/whole + 10 ninths (vs ~1.7 / ~5.8):** **ANTARES twice — Dec 13√2 and Sky 425/9 (off 0.0001)** (the horse's eight-body star); **ALGOL twice — Dec whole 49 and Sky whole 140**; Dec to Neptune 8φ; ninths to Makemake (235/9), Alkaid, Pleiades, Deneb Algedi, Aldebaran, Quaoar, Spica, Sirius, Pallas.
- Chords with stars loose (≥0.027%; Alphecca three times). With bodies: **Dec Gonggong–Sedna 5:6:11, 0.005%**; **Dec Transpluto–Vesta φ, 0.012%**; **RA Juno–Mars φ, 0.019%**; Dec Chiron–Mercury φ (Mercury's).
#### Mars (RA 225.905, Dec −17.819)
- Numbers — 2 φ + 9 ninths: **Sky to SATURN 75φ** (and Dec to Saturn 105/9); **Sky to PROCYON 69φ** (and Flat 1021/9); RA to ANTARES 193/9 (the same 193/9 the horse's Pallas makes to Aldebaran), Betelgeuse 1234/9, Algorab 346/9; Flat to Chiron, Alkaid; Sky to Fomalhaut 937/9; Dec to Mercury (Mercury's).
- Chords with stars: only two (RA Regulus–Spica 1:2:3, Dec Alphecca–Equator 2:3:5, ~0.04%). With bodies: RA Juno–Venus φ, 0.019% (Venus's); **RA Ceres–Transpluto 5:8:13, 0.021% (≤0.086% all day)**; RA Pluto–Sun 3:8:11 (the Sun's).
- Reads as: Mars is a numbers body here (Saturn and Procyon both twice), with few chords.
#### Jupiter (RA 249.561, Dec −21.694)
- Numbers — 3 φ/whole + 5 ninths: **Flat to NEPTUNE whole 45**; RA to Bellatrix 104φ; Sky to Transpluto 66φ; **RA to ORCUS 1028/9 (off 0.0000)**; Sky to Makemake 805/9 (off 0.0001); Dec to Haumea 388/9 (08:14–13:29); Sky to Juno 163/9 (08:46–13:01); Flat to Aldebaran 1651/9.
- Chords: **Dec Aldebaran–Altair 1:4:5, 0.020% (≤0.061% all day)**; RA Deneb Algedi–Spica 5:8:13; Dec Bellatrix–Capella √2 (0.003% at 00:00). With bodies loose (≥0.047%): Dec Orcus–Quaoar 1:2:3.
#### SATURN (RA 351.660, Dec −6.152; slow)
- Numbers: **Flat to RIGEL whole 87**; **Flat to NEPTUNE whole 59**; Sky to Mars 75φ (Mars's); Dec to Mars 105/9; Sky to Ketu 331/9 / Rahu 1289/9; Sky to Fomalhaut 220/9.
- **Chords all day (seven at ≤0.031%):** RA Algol–Bellatrix φ, 0.016%; Dec Alkaid–Pleiades 5:6:11, 0.019%; RA Capella–Regulus 5:6:11, 0.021%; Dec Algol–Regulus 5:8:13, 0.022%; RA Antares–Pleiades 5:8:13, 0.031%; Dec Antares–Arcturus 4:5:9, 0.041%; Dec Altair–Spica 1:3:4, 0.006% (0.35% at the ends). With bodies: **Dec Sedna–Transpluto 4:5:9, 0.016%**; **RA Makemake–Rahu 1:5:6, 0.022%**; RA Ceres–Quaoar 2:5:7, 0.011%.
- Reads as: Saturn is the jockey's first strong slow body — many all-day star chords (Algol twice, Pleiades twice, Regulus twice, Antares twice).
#### URANUS (RA 298.724, Dec −21.385 — at its station: RA 298.725 → 298.723 over the day)
- Numbers, ALL DAY: **Flat to CAPELLA 1402/9**; **Sky to ALKAID 965/9**; **Sky to ALDEBARAN 1196/9**; Sky to Rigel 1177/9 (05:04–24:00); Dec to Sedna 235/9 (08:35–24:00); Flat to Makemake 1214/9; RA to Ceres 930/9.
- Chords all day: with bodies — **Dec SEDNA–TRANSPLUTO 1:3:4, 0.005% (≤0.016%)** (Saturn holds Sedna–Transpluto too, 4:5:9, 0.016% — a two-body string); **RA ERIS–GONGGONG 3:5:8, 0.007% (≤0.016%)**; RA Rahu–Transpluto φ, 0.033%; Dec Mercury–Quaoar (Mercury's). With stars — RA Spica–Vega 1:4:5, 0.025%; Dec Antares–Equator φ, 0.041% (constant).
- Reads as: Uranus stationary — every figure holds all day; Sedna–Transpluto is held by both Uranus and Saturn.
#### NEPTUNE (RA 294.556, Dec −20.990 — stationary, unchanged over the day)
- Numbers: ALL DAY — **RA to ALPHECCA 548/9**, **Dec to VEGA 538/9**; Flat to Spica 844/9 (02:52–24:00); whole — **Sky to PLUTO 55**, Flat to Jupiter 45 (Jupiter's), Flat to Saturn 59 (Saturn's); Flat to Pluto 512/9; Dec to Venus 8φ (Venus's). (Own RA 2651/9 set aside.)
- **Chords all day — four at ≤0.021%:** Dec ALKAID–ARCTURUS 3:4:7, 0.016%; Dec PROCYON–SPICA 3:5:8, 0.017%; RA ALKAID–REGULUS 5:8:13, 0.019%; Dec CAPELLA–RIGEL φ, 0.021%; also RA ARCTURUS–Fomalhaut φ, 0.041% (constant). With bodies all loose.
- Uranus and Neptune both stationary and close in the sky (RA 298.7 / 294.6; Dec −21.39 / −20.99), with Jupiter at Dec −21.69 — a Dec band around −21 (no pair within 0.1).
- Reads as: Neptune holds stars all day — Alkaid twice, Arcturus twice.
#### Pluto (RA 239.376, Dec −7.155; slow)
- Numbers, long: **RA to QUAOAR 6/9 (07:35–18:18)**; **Dec to BETELGEUSE 9φ (05:22–13:07)**; Dec to Sirius 86/9 (08:51–16:36), Algol 433/9, Aldebaran 213/9 (10:17–18:04); Flat to Bellatrix 1428/9; Sky to Haumea 487/9 (10:38–22:17); Sky to Neptune whole 55 (Neptune's).
- Chords: **Dec Aldebaran–Betelgeuse 5:8:13, 0.006% (≤0.048% all day)** — with the 9φ and 213/9, Aldebaran–Betelgeuse three times; RA Antares–Vega 1:4:5, 0.016% (0.18% at the ends); Dec Antares–Polaris 1:5:6, 0.035% (0.004% at 00:00); Dec Alkaid–Polaris √2, 0.038%. With bodies: RA Mars–Sun 3:8:11 (the Sun's); RA Orcus–Rahu 1:2:3, 0.038%.
#### Chiron (RA 182.259, Dec −4.014)
- Numbers: **Sky to ARCTURUS 24φ (off 0.0000)**; **Flat to VEGA whole 106**; Sky to Alkaid 517/9 (02:29–14:25), Castor 668/9; Dec to Deneb Algedi 109/9, Transpluto 157/9; Flat to Quaoar 528/9, Mars 412/9 (Mars's).
- **25 star chords** (the most of any body so far): Dec Alphecca–Fomalhaut 5:6:11, 0.010%; Dec Bellatrix–Polaris 1:8:9, 0.013%; Dec Capella–Spica 1:7:8, 0.015%; Dec Algorab–Capella 1:4:5, 0.027%; Sky Betelgeuse–Procyon φ, 0.029% (≤0.133% all day); the tight Dec ones run 0.2–0.45% at the day's ends. With bodies: Dec Mercury–Venus φ, 0.002% and RA Mercury–Pallas 5:8:13, 0.003% (Mercury's); Dec Mars–Vesta 5:6:11, 0.035%.
- Chiron is 7.7° from the Sun and Mercury in RA (182.3 vs 190.0/190.1).
#### Ceres (RA 195.391, Dec +1.022)
- Numbers: **Dec to VESTA 4φ (07:20–15:31)**; Flat to Castor 54φ; Dec to Rigel 83/9 (the 83/9 again — the horse's Sun–Pluto and Chiron–Transpluto); RA to Uranus 930/9 (Uranus's); Flat to Gonggong 1228/9; Sky to Deneb Algedi 1168/9, Sirius 848/9.
- Chords: RA Antares–Regulus 5:6:11, 0.009% (0.86% at the ends); Dec Alphecca–Capella 3:4:7, 0.033%. With bodies: RA Quaoar–Saturn 2:5:7, 0.011% (Saturn's); RA Mars–Transpluto 5:8:13, 0.021% (Mars's, all day); RA Orcus–Pallas 3:4:7, 0.022%; RA Haumea–Mercury and Chiron–Mercury (Mercury's).
#### Pallas (RA 169.651, Dec −1.433; at 12:00)
- **Numbers — 4 φ/√2/whole + 10 ninths:** **Dec to ANTARES whole 25** (Antares again); **Dec to ALDEBARAN φ⁶**; **Sky to REGULUS whole 22**; Flat to Mercury 15√2 (Mercury's); **RA to Vesta 37/9 (off 0.0000, 10:40–13:20)**; ninths to Deneb Algedi, Aldebaran (RA), Pleiades, Vega, Neptune, Haumea, Transpluto, Venus, Altair, Alphecca.
- Chords: with bodies — **RA HAUMEA–ORCUS 2:3:5, 0.000%**; **Dec GONGGONG–MAKEMAKE 1:2:3, 0.002% (0.32% at the ends)**; RA Ceres–Orcus 3:4:7 (Ceres's); RA Chiron–Mercury (Mercury's). With stars — RA Alphecca–Altair 1:1:2, 0.020% (Pallas at the RA midpoint); Dec Algorab–Vega 3:8:11, 0.024%; Dec Antares–Castor 3:4:7, 0.031%.
#### Juno (RA 265.509, Dec −11.906)
- Numbers: 7 ninths, no φ/√2/whole — RA to Capella 1563/9, Sirius 1478/9; Dec to Alkaid 551/9, Altair 187/9, Deneb Algedi 38/9; Flat to Spica 578/9; Sky to Jupiter 163/9 (Jupiter's).
- Chords: with bodies — **Dec KETU–SEDNA 1:3:4, 0.002%** — **the horse holds the KETU–SEDNA base too (Eris √2, 0.013% — part of the Eris–Ketu–Sedna figure whose Eris–Ketu base the Moon struck in the race)**: the same body-pair base held in both charts; RA Mars–Venus φ (Venus's); RA Gonggong–Vesta √2, 0.030% (≤0.099% all day). With stars — Dec Betelgeuse–Regulus φ, 0.014%; Dec Alphecca–Betelgeuse 1:1:2, 0.023% (Juno at the Dec midpoint); Dec Alphecca–Regulus φ, 0.037%.
#### Vesta (RA 173.762, Dec +7.495)
- Numbers: **RA to DENEB ALGEDI whole 153**; RA to SEDNA 91√2; Dec to Ceres 4φ (Ceres's); RA to Pallas 37/9 (Pallas's); ninths to Aldebaran, Pleiades, Alphecca, Ketu.
- Chords: **RA FOMALHAUT–VEGA φ, 0.002% — the horse's URANUS holds Fomalhaut–Vega in RA (3:5:8, 0.017%, all day): a shared string across the two charts.** Other star chords ≥0.058%. With bodies: Dec Transpluto–Venus φ (Venus's); RA Gonggong–Juno √2 (Juno's); RA Sun–Venus √2 (Venus's); Dec Chiron–Mars 5:6:11 (Chiron's).
#### ERIS (RA 23.199, Dec −8.118; slow)
- Numbers, long: **Flat to DENEB ALGEDI whole 57 (07:33–17:40)**; Dec to Pleiades 290/9 (00:00–14:04); RA to Regulus 1160/9 (02:16–12:26); Sky to Sirius 687/9 (09:07–21:56), Aldebaran 464/9 (10:01–20:18).
- **Chords all day:** **Dec DENEB ALGEDI–PROCYON 3:5:8, 0.000% (≤0.035%)**; **Sky ALPHECCA–VEGA 3:8:11, 0.012% (≤0.014%)** — the horse's KETU holds Alphecca–Vega in RA (5:6:11, 0.007%): shared stars, other coordinate; **RA ARCTURUS–DENEB ALGEDI 1:2:3, 0.016%**; **Dec PLEIADES–PROCYON √2, 0.019%**; RA Polaris–Rigel 3:8:11, 0.023%. With bodies: RA Gonggong–Uranus 3:5:8 (Uranus's), Dec Gonggong–Quaoar 3:4:7, 0.035%.
- Reads as: ERIS is strong in BOTH charts (the horse's Eris: Bellatrix–Procyon 0.004%; the jockey's: Deneb Algedi–Procyon 0.000%) — PROCYON on both Erises' tightest chord. Deneb Algedi three times (whole 57, two chords).
#### SEDNA (RA 45.070, Dec +4.727; slow) — a hub
- Numbers, long: **RA to GONGGONG 672/9 — ALL DAY (off 0.0001)**; **Dec to RAHU whole 15 (06:08–12:35)**; Sky to VEGA 1024/9 (00:00–23:46); RA to Spica 1406/9 (03:27–16:37); Sky to Rigel 323/9 (09:52–24:00); Dec to Uranus 235/9 (Uranus's).
- **Star chord: Dec ALGOL–POLARIS 3:4:7, 0.004% (≤0.009% all day; 0.000% at 24:00) — the string the MOON struck in the race (4:5:9, exact 14:36:00, held through the race; §62).** RA Antares–Fomalhaut 5:8:13, 0.025%.
- **With bodies — five at ≤0.016%:** Dec Juno–Ketu 1:3:4, 0.002% (Juno's Ketu–Sedna); Dec Transpluto–Uranus 1:3:4, 0.005% (Uranus's); Dec Gonggong–Venus 5:6:11, 0.005% (Venus's); **RA GONGGONG–KETU 3:8:11, 0.005% (≤0.087% all day)**; Dec Saturn–Transpluto 4:5:9, 0.016% (Saturn's).
- Reads as: SEDNA is the jockey's hub — Juno, Uranus, Venus, Gonggong, Saturn, Transpluto, Ketu and Rahu all tie to it; its Algol–Polaris string is the one the Moon held through the race. (For the horse, Sedna was also strong — Fomalhaut whole 78.)
#### Haumea (RA 192.526, Dec +21.418; slow)
- Numbers: RA to Altair 65φ (07:45–12:17); RA to Rigel 1025/9 (09:12–13:43); Dec to Gonggong 361/9 (00:00–15:15); Sky to Alphecca 340/9 (07:03–12:48), Pluto 487/9 (Pluto's); Dec to Jupiter 388/9 (Jupiter's).
- Chords: **Dec Aldebaran–Arcturus 5:6:11, 0.005%** (0.16% at the ends); **Dec Altair–Equator √2, 0.019% (≤0.048% all day)**; Dec Algol–Spica 3:5:8, 0.049%. With bodies: RA Orcus–Pallas 2:3:5, 0.000% (Pallas's); Dec Mercury–Orcus φ (Mercury's).
#### Makemake (RA 175.321, Dec +33.082; slow)
- Numbers: **RA to QUAOAR 40φ (03:13–23:08)**; Flat to Ketu 1371/9; RA to Alkaid 284/9, Pleiades 1066/9; Flat to Sirius 803/9 (11:59–17:55); Uranus, Venus, Jupiter (theirs).
- Chords all day: **Dec ALGORAB–ANTARES 1:5:6, 0.001% (≤0.005% all day)** — Antares again; **RA PLEIADES–SIRIUS 3:5:8, 0.016% (0.001% at 00:00)**; RA Spica–Vega 1:3:4, 0.033% (Uranus holds Spica–Vega too, 1:4:5 — a two-body string); RA Algorab–Alkaid 5:8:13. With bodies: Dec Gonggong–Pallas 1:2:3 (Pallas's); RA Rahu–Saturn 1:5:6 (Saturn's); RA Orcus–Quaoar φ, 0.045%.
#### Quaoar (RA 240.043, Dec −14.159; slow)
- Numbers: **Dec to SPICA whole 3 (off 0.0001, 03:05–21:50)**; RA to Makemake 40φ (Makemake's); RA to Pluto 6/9 (Pluto's); Dec to Rahu 35/9 (10:32–16:12); Flat to Sirius 1249/9, Betelgeuse 1375/9.
- Chords all day: **RA ALGOL–FOMALHAUT 3:5:8, 0.009% (0.000% at 00:00)**; **RA ARCTURUS–VEGA 2:3:5, 0.015%**; Dec Betelgeuse–Rigel φ, 0.019%; Dec Aldebaran–Antares 2:5:7, 0.040% (0.011% at 24:00). With bodies: Dec Eris–Gonggong 3:4:7 (Eris's), RA Orcus–Makemake φ (Makemake's), Dec Jupiter–Orcus 1:2:3.
#### ORCUS (RA 135.339, Dec +0.902; slow) — the receiver
- Numbers: Dec to ANTARES 246/9 (09:21–19:53); Sky to Aldebaran 604/9 (off 0.0001, 08:56–15:28), Altair 1439/9 (01:14–16:03); RA to Jupiter 1028/9 (off 0.0000, Jupiter's).
- **Bodies landing on Orcus (12 chords): Haumea–Pallas RA 2:3:5 (0.000%), Ceres–Pallas RA 3:4:7 (0.022%), Haumea–Mercury Dec φ (0.028%), Pluto–Rahu RA 1:2:3 (0.038%), Mercury–Transpluto, Makemake–Quaoar RA φ (0.045%), Jupiter–Quaoar Dec 1:2:3 (0.047%)** — plus Jupiter by number. Orcus receives, as in Messi, Dettori and Frankel (not in the horse's chart).
- Star chords: RA Castor–Pleiades φ, 0.022% (0.006% at 00:00); Dec Betelgeuse–Deneb Algedi φ, 0.029%; Dec Alphecca–Regulus 3:4:7, 0.036% (0.006% at 00:00).
#### Gonggong (RA 330.403, Dec −18.691; slow)
- Numbers, long: RA to SEDNA 672/9 ALL DAY (Sedna's); Sky to SIRIUS 1081/9 (off 0.0002, 02:47–19:55); Sky to Bellatrix 1006/9 (04:20–17:19); RA to Spica 1162/9 (03:58–15:49); Flat to Capella 1139/9 (11:11–23:58); Dec to Haumea 361/9 (Haumea's).
- Chords: **RA Alkaid–Vega √2, 0.011% (≤0.019% all day)**; RA Altair–Sirius 1:4:5, 0.044%. With bodies (seen from the others): Makemake–Pallas 0.002%, Sedna–Venus 0.005%, **Ketu–Sedna 0.005%**, Eris–Uranus 0.007%, Juno–Vesta 0.030%, Eris–Quaoar 0.035%.
- Gonggong sits in the jockey's Sedna / Eris / Uranus / Ketu network (with Sedna 672/9 all day).
#### TRANSPLUTO (RA 146.580, Dec +13.432; slow)
- Numbers: RA to ARCTURUS 606/9 (00:49–13:16); Sky to Aldebaran 671/9 (08:26–20:20); Jupiter 66φ, Mercury 34√2, Chiron, Pallas (theirs).
- **26 star chords; all day:** **RA ALKAID–VEGA 5:6:11, 0.002% (≤0.008%)** — Gonggong holds Alkaid–Vega too (√2, 0.011%): a two-body string; **Dec ALPHECCA–ANTARES 1:3:4, 0.010%** (Antares); **Dec ALKAID–FOMALHAUT 5:6:11, 0.017%**; RA Rigel–Sirius 1:2:3, 0.025%; RA Alphecca–Bellatrix 3:4:7, 0.032%; Sky Pleiades–Spica √2, 0.040%.
- With bodies: Dec Sedna–Uranus 1:3:4, 0.005% (Uranus's); Dec Saturn–Sedna 4:5:9 (Saturn's); RA Ceres–Mars 5:8:13 (Mars's); RA Rahu–Uranus φ (Uranus's).
- Reads as: as for the horse, TRANSPLUTO is the jockey's strongest star-chord body (Alkaid–Vega 0.002%); in both charts it ties to Sedna.
#### Nodes (Rahu RA 204.706, Dec −10.271; Ketu RA 24.706, Dec +10.271)
- Numbers: **Rahu Flat to ALPHECCA φ⁸ (off 0.0001, 06:53–16:42)**; Rahu Dec to Sedna whole 15 (Sedna's); Dec to Spica 8/9 (09:40–17:47), Quaoar 35/9; Flat to Polaris 1745/9; Sky to Algorab, Saturn.
- Chords: **Ketu RA FOMALHAUT–VEGA φ, 0.006%** — the same φ as his Vesta (0.002%) on the horse's Uranus string; Ketu Dec Capella–Spica 3:5:8, 0.022%; Ketu RA Algol–Rigel √2, 0.025%; **Ketu Dec ALGORAB–CAPELLA 3:4:7, 0.037% (0.000% at 00:00)** — the horse's SEDNA holds Algorab–Capella (5:8:13, 0.013%). With bodies: Ketu–Juno–Sedna 0.002%, Ketu–Gonggong–Sedna 0.005% (seen); Rahu RA Makemake–Saturn 1:5:6 (Saturn's).
### DAVID NOONAN — Method 1 put together
- **SEDNA is the hub:** Juno, Uranus, Venus, Gonggong, Saturn, Transpluto, Ketu and Rahu tie to it (five chords ≤0.016%; Gonggong 672/9 all day; Rahu whole 15); its Algol–Polaris (0.004%, all day) is the string the Moon held through the race (§62).
- **ORCUS receives** (Haumea–Pallas 0.000%, Ceres–Pallas, Haumea–Mercury, Pluto–Rahu, Makemake–Quaoar, Jupiter–Quaoar; Jupiter 1028/9).
- **Stationary URANUS and NEPTUNE** hold all day: Uranus — Sedna–Transpluto 0.005%, Eris–Gonggong 0.007%, numbers to Capella, Alkaid, Aldebaran all day; Neptune — four star chords ≤0.021% (Alkaid–Arcturus, Procyon–Spica, Alkaid–Regulus, Capella–Rigel).
- **TRANSPLUTO** — 26 star chords, Alkaid–Vega 0.002% (shared with Gonggong). **ERIS** — Deneb Algedi–Procyon 0.000%, Alphecca–Vega 0.012%, Deneb Algedi whole 57. **SATURN** — seven all-day star chords ≤0.031%. **MAKEMAKE** — Algorab–Antares 0.001% all day.
- **Numbers-heavy fast bodies (12:00):** Mercury five √2; Venus — Antares 13√2, Algol whole 49 and 140; Pallas — Antares whole 25, Aldebaran φ⁶, Regulus whole 22; Mars — Saturn 75φ, Procyon 69φ.
- **Recurring stars:** ANTARES (by number — Venus ×2, Pallas whole 25, Orcus, Mars; by chord — Makemake 0.001%, Transpluto, Saturn, Pluto, Sedna, Uranus, Quaoar); ALKAID (Neptune ×2, Transpluto ×2, Gonggong, Uranus, Saturn); ARCTURUS (Mercury ×3, Chiron 24φ, Neptune ×2, Transpluto, Quaoar); PROCYON (Eris ×2, Neptune, Mars 69φ); VEGA; ALPHECCA.
- Out of bounds: none. Stationary: Uranus, Neptune.
### WHERE THE HORSE'S AND THE JOCKEY'S CHARTS MEET (first look)
- **KETU–SEDNA base held in both:** horse's Eris √2 (0.013%; the Eris–Ketu–Sedna figure the Moon struck in the race); jockey's Juno 1:3:4 (0.002%) and Gonggong (RA, 0.005%).
- **FOMALHAUT–VEGA (RA) held by three bodies across the two charts:** horse's Uranus 3:5:8 (0.017%, all day); jockey's Vesta φ (0.002%) and Ketu φ (0.006%).
- **ALPHECCA–VEGA:** horse's Ketu (RA 5:6:11, 0.007%); jockey's Eris (Sky 3:8:11, 0.012%).
- **ALGORAB–CAPELLA (Dec):** horse's Sedna 5:8:13 (0.013%); jockey's Ketu 3:4:7 and Chiron 1:4:5 (0.027%).
- **The nodes to ALPHECCA in both:** horse's Ketu Flat whole 94 (+ Rahu Aldebaran–Alphecca √2 0.001%); jockey's Rahu Flat φ⁸.
- **Sun and Mercury share an RA in both charts** (0.07° / 0.17°).
- **The same bodies strong in both:** ERIS (Procyon on each one's tightest chord — 0.004% / 0.000%), SEDNA (horse — Fomalhaut 78 all day; jockey — the hub), TRANSPLUTO (each chart's strongest star-chord body).
- **The same number:** 83/9 — horse Sun–Pluto and Chiron–Transpluto; jockey Ceres–Rigel.
- **Recurring stars in both:** ANTARES (horse — eight bodies by number; jockey — four by number: Venus 13√2 and 425/9, Pallas whole 25, Orcus 246/9, Mars 193/9 — plus chords from Makemake 0.001%, Transpluto, Saturn, Pluto, Sedna, Uranus, Quaoar), ARCTURUS, PROCYON, ALPHECCA, FOMALHAUT, VEGA.
- Not yet checked: direct horse-body ↔ jockey-body parallels and numbers (cross-chart distances).
### DIRECT LINKS horse (P03) ↔ jockey (P04) at 12:00 (cross.py; Eddie 07:55)
- Counts: 25 × 25 bodies, 2,500 values — φ/√2/whole/φⁿ 24 (chance ≈ 23), ninths 90 (chance ≈ 80): **numbers between the two charts are at chance overall.**
- **Dec links (4):** **horse ORCUS (−10.266) parallel jockey RAHU (−10.271) and contraparallel jockey KETU (+10.271), 0.005** — the horse's Orcus sits on the jockey's node axis in Dec (one fact); horse NEPTUNE (−7.484) contraparallel jockey VESTA (+7.495), 0.011; horse SEDNA (+7.529) parallel jockey VESTA, 0.034 — the jockey's Vesta between the horse's Sedna and mirrored Neptune.
- Whole/φ/√2 between slow bodies (9): **horse nodes ↔ jockey ERIS in RA — Ketu whole 66 / Rahu whole 114 (one fact)**; horse Saturn ↔ jockey Neptune RA whole 18; horse Quaoar ↔ jockey Gonggong Flat whole 59; horse Neptune ↔ jockey Uranus Flat 34√2; horse Transpluto ↔ jockey Rahu Dec 15√2; horse Jupiter ↔ jockey Ketu Dec 17φ; horse Saturn ↔ jockey Haumea Dec 31√2; horse Chiron ↔ jockey Jupiter Sky 65φ. (Plus 37 slow–slow ninths.)
- With one fast body: horse Neptune ↔ jockey Juno Sky whole 78; horse Uranus ↔ jockey Sun Flat whole 167; horse Mars ↔ jockey Orcus Flat whole 118; horse Ceres ↔ jockey Sedna Dec 19√2; horse Juno ↔ jockey Sedna RA 55√2; and others.
- Reads as: by count the direct numbers are chance; what stands out is the Dec link — the horse's ORCUS on the jockey's node axis (0.005) — and the horse's nodes whole-number to the jockey's Eris.
### SAME-BODY CHORDS (samebody.py; Eddie 07:59 — "with the same body, say Jupiter — transit, horse and jockey — 3 positions")
Window 14:10:41 (off−30) to 14:44:41, every 15 s; natal at 12:00; natal Moon left out. Note: the window ends 8 s before the finish (14:44:49), so "window edge 14:44:41" items are in the race; "edge 14:10:41" items are slow chords still closing or opening at off−30.
**Part 1 — sky X + horse X + jockey X:**
- Winner pair: one — **MERCURY Dec 1:4:5, 0.001% at 14:15:11** (25.5 min before the off; 1.0% at the off). Sky–horse 6.063, sky–jockey 1.516, horse–jockey 7.579 — sky Mercury between the two natal Mercuries, four times nearer the jockey's.
- Suntory Star / Mulqueen: the same Mercury Dec 1:4:5 (0.005% at 14:12:41), Transpluto Flat 1:8:9 (0.023%, edge), Gonggong Dec 1:6:7 (0.109%). Fiamette / Davies: Haumea Dec 1:6:7 (0.041%, edge). Oot Ma Way / O'Farrell and Poetria / Hamilton: none.
- Control (20 non-actual pairings): mean 1.2 / 0.6 / 0.3. The winner pair's one chord is at control level.
**Part 2 — natal X – sky X + a third point (sky body or star):** counts ≤0.15 / ≤0.05 / ≤0.02 / in race: Fiamette 55/21/12/1; Davies 69/30/21/2; **Olympe De Gouges 59/24/18/0; Noonan 78/35/22/3**; Oot Ma Way 54/29/19/4; O'Farrell 66/19/12/1; Poetria 59/32/18/3; Hamilton 64/23/12/0; Suntory Star 71/36/22/3; Mulqueen 46/22/13/0. By count the winner does not stand out; Noonan has the most at ≤0.15.
**Horse (P03), ≤0.02% (with exact times):** Sun–Polaris RA √2 0.000% 14:32:56; Juno–Orcus Dec 1:4:5 0.000% 14:25:26; Pallas–Moon RA φ 0.000% 14:17:26; SEDNA–Moon Dec 1:8:9 0.001% 14:14:11; MERCURY with Saturn RA 2:5:7 (14:14:26), Gonggong RA 5:6:11 (14:15:41), Neptune Dec 3:4:7 (14:12:26), Jupiter RA 1:5:6 (14:31:11); Venus–Moon Dec φ 0.002% 14:35:11; Jupiter–Moon Dec √2 0.005% 14:13:11; Ketu–Saturn Dec φ (edge); Pallas–Uranus and Pallas–Sun Dec 1:2:3 (edge); ERIS–Sun Dec φ 0.009% 14:24:26; ERIS–Moon Dec 1:3:4 0.012% 14:33:11; Rahu–Neptune Sky 3:4:7 0.014% 14:33:11; Jupiter–Ketu Dec 1:8:9 (edge); Venus–Algol RA φ 0.018% (14:44:41, in race). Also Mars–Moon Sky 4:5:9 0.024% 14:30:56; Chiron–Moon 1:6:7; Saturn–Regulus; Jupiter–Antares 4:5:9 (edge). The horse's tight items sit 5–28 min before the off.
**Jockey (P04), ≤0.02%:** MARS–Fomalhaut RA φ 0.000% 14:31:56; **MERCURY–Jupiter Dec 4:5:9 0.000% IN THE RACE 14:42:56**; MARS–Saturn Sky 1:7:8 0.000% 14:30:41; Ketu–Moon Dec 3:8:11 0.000% 14:19:11; MARS–Moon RA 1:2:3 0.000% 14:15:26; **PALLAS–RIGEL Dec 2:5:7 0.000% at 14:39:56 (45 s before the off)**; Makemake–Moon Dec 1:2:3 0.001% 14:34:41 (and RA 1:2:3 0.006% 14:26:26); MERCURY–Neptune Dec 1:2:3 0.001% 14:17:26; MERCURY–Mars Dec 1:7:8 0.001% 14:19:41; ORCUS–Sun Dec 1:6:7 0.002% 14:37:26; Jupiter–Moon RA 2:3:5 0.002% 14:26:41; **PLUTO–Moon Dec φ 0.003% IN THE RACE 14:44:26**; Chiron–Moon Dec 5:8:13 0.003% 14:37:26; Haumea–Moon RA φ 0.007%; Uranus–Jupiter RA 1:1:2 0.011% (edge — sky Jupiter at the midpoint of natal and sky Uranus); Vesta–Moon Dec φ 0.011%; **SEDNA–Moon Dec √2 0.015% at 14:39:56 (45 s before the off)**; Juno–Pluto, Pallas–Vesta (edge, in race); Transpluto–Procyon RA 1:4:5 0.018% (in race); Neptune–Bellatrix Dec 3:5:8 (edge). ≤0.05% in race: Juno–Moon Sky φ 0.047% 14:41:26; Quaoar–Deneb Algedi, Sedna–Mars RA, Haumea–Betelgeuse, Ketu–Pallas, Eris–Polaris, Chiron–Rigel, Transpluto–Arcturus (all at 14:44:41).
**What we see:**
- The jockey's items run up to and through the off: Pallas–Rigel and Sedna–Moon together at 14:39:56; Mercury–Jupiter at 14:42:56; Pluto–Moon at 14:44:26. The horse's items are all before the off (14:12–14:35).
- MERCURY in both charts, and in Part 1: the pair's Mercury chord (Part 1), and each chart's natal–sky Mercury string with Neptune in Dec (horse 3:4:7, jockey 1:2:3) and with Jupiter (horse RA 1:5:6, jockey Dec 4:5:9 in the race).
- SEDNA–Moon in both (horse 1:8:9 at 14:14:11, jockey √2 at 14:39:56). Sedna is the jockey's hub and in the horse's Eris–Ketu–Sedna figure.
- The same pairs in both charts: Jupiter–Moon, Chiron–Moon, Mercury–Neptune, Mercury–Jupiter, Sedna–Moon.
- Stars that come back: RIGEL (jockey Pallas 45 s before the off; Chiron in race), PROCYON (jockey Transpluto in race; Eris's Procyon string in both charts in Method 1), POLARIS (horse Sun; jockey Eris; jockey Sedna's Algol–Polaris string), FOMALHAUT (jockey Mars).
- The jockey's MARS three times (Fomalhaut, Saturn, Moon) and ORCUS–Sun 3 min before the off — Orcus is the jockey's receiver in Method 1.
### SAME-BODY CHORDS v2 (samebody2.py + skygrid.py; Eddie 08:12 — "some will be exact or slow etc after the race but still valid")
Window now off−30 (14:10:41) to finish+30 (15:14:49), every 15 s, from a 1-minute engine grid ±12 h (checked: identical to SKYM). Each chord shown at off−30 / off / finish / finish+30; a chord tightest at a window edge is followed out to its own exact moment. Note: followed out over a day, most slow chords near 0.15% come exact at some hour, so for slow chords the exact TIME and the value through the race say more than "0.000%".
**Part 1:** winner pair still only Mercury Dec 1:4:5 (exact 14:15:11, separating through the race: 1.00% at the off, 1.17% at the finish). Fiamette/Davies: Haumea 1:6:7 (exact 15:51) + Sedna 1:7:8 (exact 20:48), both applying. Suntory Star/Mulqueen: Mercury 1:4:5 (14:12:41), Transpluto Flat 1:8:9 (0.023% at the finish, exact 15:28), Gonggong (exact 07:12). Control 1.2 / 0.8 / 0.5.
**Part 2 counts** (≤0.15 / ≤0.05 / ≤0.02 | of the ≤0.05: before off / in race / after finish / slow edge): Fiamette 65/31/25 | 7/1/15/8; Davies 82/44/32 | 14/2/12/16; **Olympe De Gouges 67/33/27 | 15/0/7/11; Noonan 89/48/32 | 14/3/10/21**; Oot Ma Way 69/39/28 | 8/4/13/14; O'Farrell 77/32/19 | 9/1/9/13; Poetria 67/39/25 | 11/3/9/16; Hamilton 74/34/23 | 5/0/15/14; Suntory Star 78/50/40 | 14/3/17/16; Mulqueen 56/35/26 | 10/0/15/10. Noonan has the most at ≤0.15 and ≤0.05-slow (21); Suntory Star the most at ≤0.02.
**New for the horse (P03) — exact just after the finish (applying through the race):** PALLAS–Moon Dec 4:5:9 14:46:11 (+1.4 min; 0.068% at the finish); VENUS–ALGOL RA φ 14:51:26 (+6.6; 0.018% at the finish); SATURN–Moon RA 1:2:3 14:51:56 (+7.1); URANUS–Moon Dec 5:6:11 14:53:41; MERCURY–Rahu RA 1:4:5 14:56:11; VESTA–Venus Dec 2:3:5 15:04:11; KETU–Venus Dec 1:2:3 15:05:56.
**Horse — slow, followed out:** SATURN four times (Regulus Dec 1:4:5 exact 16:41, 0.046% at the finish; Polaris RA 5:8:13 18:28, 0.055%; Transpluto RA φ 01:34 next day; Ketu Dec 5:6:11 12:02); URANUS four times, all separating (Makemake 3:4:7 05:14, Alphecca 1:2:3 07:40, Ceres √2 09:27, Rahu φ applying to 17:16); Pallas–Uranus Dec 1:2:3 (0.006% at off−30, exact 14:04); Ketu–Saturn φ 14:09; Jupiter–Ketu 1:8:9 14:04; Jupiter–Antares 4:5:9 12:42; Jupiter–Quaoar 1:5:6 16:58; Ceres–Antares 1:6:7 12:02; Venus–Pleiades RA 1:3:4 15:40; Sun–Eris RA 1:1:2 15:38 (sky Eris at the RA midpoint of natal and sky Sun); Neptune–Eris Dec 3:4:7 19:50; Ketu–Transpluto Sky 1:1:2 07:39.
**New for the jockey (P04) — exact just after the finish:** MERCURY–Sun Dec 1:4:5 14:46:11 (+1.4 min; 0.046% at the finish) — the same 15-s step as the horse's Pallas–Moon; JUPITER–Moon Dec 1:2:3 14:49:26; ERIS–Moon Dec 1:2:3 14:51:56 — the same step as the horse's Saturn–Moon; JUNO–Pluto Dec 1:3:4 14:52:41 (0.016% at the finish); PALLAS–Vesta Dec 3:8:11 14:57:11 (0.017% at the finish); ORCUS–Mercury Dec 3:8:11 15:01:41 and SATURN–Mercury RA 1:4:5 15:01:56; Pallas–Moon 15:03:56; Venus–Moon √2 15:04:56; Vesta–Moon 15:10:56. (Plus the in-race Mercury–Jupiter 14:42:56, Pluto–Moon 14:44:26, Juno–Moon 14:41:26 and Pallas–Rigel / Sedna–Moon 14:39:56 as before.)
**Jockey — slow, followed out:** TRANSPLUTO on three strings, all applying (Procyon RA 1:4:5 0.018% at the finish, exact 19:02; ARCTURUS Dec 1:2:3 0.047%, exact 01:23 next day; Sun Dec 1:4:5 exact 15:42) — Arcturus also on the horse's Transpluto Arcturus–Pleiades (Method 1); SEDNA (Mars RA 1:7:8 0.021% at the finish, exact 15:20; Chiron RA 3:8:11 05:50; Mars Flat 12:53); MARS (Antares RA 1:3:4 exact 15:57; Mercury RA 2:5:7 16:10; Transpluto 11:42); NEPTUNE–Bellatrix Dec 3:5:8 (0.025% at the finish, exact 12:11), Neptune–Sedna √2 03:38; ORCUS–Jupiter RA 1:7:8 (0.027% through the race, exact 06:13); Haumea–Betelgeuse √2 (0.029%, exact 17:07), Haumea–Capella φ 21:57; Eris–Polaris RA 1:4:5 (0.041%, exact 17:24), Eris–Vesta 13:19; Ketu–Pallas 3:4:7 15:34; Jupiter–Chiron 3:4:7 15:48, Jupiter–Mars 1:5:6 15:22, Jupiter–Aldebaran RA 4:5:9 21:08; Chiron–Aldebaran Dec 1:1:2 11:32, Chiron–Castor 08:11, Chiron–Rigel RA 2:3:5 (0.043% all window); Quaoar–Deneb Algedi Flat 3:4:7 (0.020% all window, still closing at +12 h); Uranus–Jupiter 1:1:2 13:52; Pluto–Ceres 1:2:3 01:28; Saturn–Fomalhaut 20:15, Saturn–Altair 21:37; Venus–Algorab 18:51, Juno–Algorab 18:27; Venus–Sirius 1:5:6 15:27, Orcus–Sirius 3:8:11.
**What we see (v2):** the horse still has nothing tightest in the race, but six chords applying through the race come exact 1–21 min after the finish (Pallas, Venus–Algol, Saturn, Uranus, Mercury–Rahu, Vesta, Ketu). The jockey's run is continuous from 14:30 to 15:11: before the off, in the race, then Mercury–Sun, Jupiter, Eris, Juno–Pluto, Pallas–Vesta, Orcus, Saturn after the finish. Two moments shared by horse and jockey: 14:46:11 (horse Pallas–Moon, jockey Mercury–Sun) and 14:51:56 (horse Saturn–Moon, jockey Eris–Moon). Transpluto (jockey) applying on Procyon, Arcturus and the Sun through the race.
### METHOD 1 LISTS BUILT (mlist.py; Eddie 08:29 "yes, build the lists")
- Project docs: claude/m1-list-olympe-de-gouges.md, claude/m1-list-david-noonan.md, claude/m1-list-olympe-de-gouges-x-david-noonan.md. Kept wide: every number and chord from Method 1 at 12:00 (horse 181 numbers / 556 chords; jockey 191 / 589).
- Each chart list: bodies table (RA, Dec, daily motion, out of bounds, counts) → body by body → star strings and who holds them → figures between bodies → midpoints → stars and who reaches them → body–body numbers → Dec numbers → number families. Combined: shared strings (81 bases in both; horse 212, jockey 228), same star pair in another measure, same figures (3), same numbers in both, shared stars, same-body natal distances, direct links (cross.py), all 589 cross-chart horse body + jockey body + star chords ≤0.15%.
- **Correction to the OOB check above:** MAKEMAKE is out of bounds in both charts — horse +24.480 (1.04 out), jockey +33.082 (9.64 out). Earlier only Ceres was noted. Makemake's Dec moves slowly over years, so like Ceres it is shared by everyone born in those years.
### METHOD 3 — Doncaster race sky on all ten charts (m3d.py / m3d.sh; Eddie 08:35 "method 3 now"). Natal at 12:00, stars at birth; winning pair marked; who is tightest across the field; dev at off−30 / off / finish / off+30.
#### Sun (RA 357.861, Dec −0.929; +0.89/d RA, +0.39/d Dec — two days before the equinox, just south of the equator)
- 22 chords within 0.15% around the off (RA 7, Dec 12, Sky 3).
- **Dec ALKAID–ARCTURUS 2:3:5, exact 14:42:56 IN THE RACE** (0.044% off−30 → 0.003% off → 0.003% finish → 0.037% off+30). **Noonan's NEPTUNE is the tightest in the field, 0.016%** (his 3:4:7; natal Neptune–Alkaid 70.306 | –Arcturus 40.177). Base 30.143: sky Sun beyond the ARCTURUS end (Sun–Arcturus 20.096, Sun–Alkaid 50.239) and his Neptune beyond the same end, further out. Others: Poetria Eris 0.021%, Mars 0.056%; O'Farrell Makemake; Suntory Star Vesta. 14:42:56 is the same 15-s step as the jockey's same-body Mercury–Jupiter in the race.
- **Dec PROCYON–SPICA 3:5:8, exact 14:52:18 (7.5 min after the finish)** (0.296% → 0.082% → 0.052% → 0.128%). **Noonan's NEPTUNE in UNISON, 3:5:8 0.017% — tightest of eight bodies in seven charts** (natal Neptune–Procyon 26.218 | –Spica 9.831); his Transpluto 1:2:3 0.125% too. Base 16.380: sky Sun INSIDE (6.146 from Procyon, 10.234 from Spica); his Neptune beyond the SPICA end. Others: Fiamette Chiron 0.057%; O'Farrell, Mulqueen Neptune; Poetria, Suntory Star Mars.
  - Both strings are on Noonan's Method 1 list: his stationary Neptune's four star chords include Alkaid–Arcturus and Procyon–Spica. The Sun plays the first in the race and the second 7.5 min after the finish.
- **Dec BELLATRIX–RIGEL 1:1:2, exact 14:42:45 IN THE RACE** (the Sun at the Dec MIDPOINT of Bellatrix and Rigel, 7.277 / 7.276 of a 14.553 base; 0.242% → 0.016% → 0.015% → 0.206%). Horse's PALLAS 3:5:8 0.038% and ERIS 2:3:5 0.147%; tightest Hamilton Quaoar 0.005%.
- **Dec BETELGEUSE–EQUATOR 1:8:9, exact 14:52:34 (7.8 min after the finish)** — the horse's natal SUN on the same base (3:5:8, 0.030%, SAME BODY); Oot Ma Way's Sun is tighter (0.001%) and Hamilton's Sun 0.031% — the Feb–Mar births share a Sun Dec near here.
- **Number:** Sun Dec to BETELGEUSE = 75/9 (8.3333), **exact at the finish** (the only number; chance 0.44 + 1.5 ninths). This Sun–Betelgeuse 8.334 is one side of three of the Sun's Dec chords (Betelgeuse–Equator, Betelgeuse–Pleiades, Arcturus–Betelgeuse).
- **ARCTURUS in 4 of the 12 Dec chords** (Alkaid–Arcturus, Alphecca–Arcturus, Arcturus–Capella, Arcturus–Betelgeuse). Arcturus is on both Method 1 lists (horse — Sun Flat whole 120, Transpluto's Arcturus–Pleiades; jockey — Mercury ×3, Neptune ×2, Transpluto).
- Other holdings of the pair: RA Algol–Vega 5:8:13 (exact 15:16; horse Vesta 0.052%, jockey Gonggong 0.143%; 7 charts); RA Capella–Deneb Algedi φ (exact 13:48; jockey Transpluto 0.063%, ORCUS 0.075%); Dec Arcturus–Capella (exact 13:01; jockey Neptune 0.090%, Gonggong 0.092%); Dec Arcturus–Betelgeuse √2 (exact 15:47; jockey Rahu 0.065%, Pallas 0.089%; horse Eris 0.086%); Polaris–Sirius RA (exact 16:08; horse Sedna 0.107%); Sky Sirius–Spica (horse Ceres, only chart); Sky Bellatrix–Procyon (jockey Venus, only chart).
- Whole day: the Sun comes exact on one of the pair's natal strings about 65 times through the day (about every 20 min). In the hour around the race: 14:42:45 Bellatrix–Rigel (horse), 14:42:56 Alkaid–Arcturus (jockey Neptune), 14:52:18 Procyon–Spica (jockey Neptune), 14:52:34 Betelgeuse–Equator (horse Sun), 15:16:25 Algol–Vega (both).
- No slow parallel for the Sun.
- (Correction 08:45: the first m3d.py run printed the three distances in the wrong order — base and sides swapped. Fixed in m3d.py; the Sun lines above now use the corrected distances.)
#### Mercury (RA 345.929, Dec −8.435; +1.59/d RA, +0.68/d Dec)
- 24 chords within 0.15% around the off (RA 9, Dec 14, Sky 1). No numbers (chance 0.44 + 1.5 ninths). No slow parallel.
- **★ STACK — Dec PROCYON–SPICA, Mercury 1:5:6, exact 14:45:16 (27 s after the finish)** (0.724% off−30 → 0.095% off → 0.008% finish → 0.515% off+30). **Noonan's NEPTUNE tightest in the field again, 0.017%** (3:5:8; his Transpluto 1:2:3 0.125%). Base 16.380: sky Mercury INSIDE near Spica (13.652 from Procyon, 2.728 from Spica); his Neptune beyond the Spica end. **The Sun plays the same string 7 min later (14:52:18, 3:5:8 UNISON)** — two sky bodies on one string, both on his Neptune, both just after the finish.
- **Dec ALGOL–PROCYON φ, exact 14:42:24 IN THE RACE** (0.110% → 0.006% → 0.009% → 0.096%). Horse's PLUTO 3:4:7 0.090%. Tightest Oot Ma Way Pallas 0.004%; seven bodies in six charts.
- **Dec ALPHECCA–SIRIUS φ, exact 14:49:09 (4.3 min after the finish)** (0.272% → 0.059% → 0.030% → 0.148%). Noonan's SUN 2:5:7 0.075%. Tightest Davies Ceres 0.010%.
- **RA PLEIADES–SIRIUS 5:8:13 (exact 12:45, separating; 0.179% at the off)** — **Noonan's MAKEMAKE tightest in the field, 0.016%**, and his MERCURY 1:2:3 0.028% (SAME BODY); horse's URANUS 3:4:7 0.110%. Eight bodies in seven charts. The Sun plays the same base at 08:56 in its whole-day list.
- **RA CASTOR–PLEIADES 4:5:9 (exact 14:05, separating; 0.055% at the off)** — **Noonan's ORCUS tightest in the field, 0.022%** (his receiver).
- **Dec ALTAIR–CASTOR 3:4:7 (exact 16:02, applying; 0.220% at the off)** — horse's MARS in UNISON 3:4:7 0.042%; Noonan's QUAOAR 1:1:2 0.057% and HAUMEA 0.123%. Tightest O'Farrell Jupiter 0.001%.
- Others for the pair (exact before the off, separating): Bellatrix–Pleiades 5:6:11 (14:11; Noonan Sun 0.049%, horse Saturn); Deneb Algedi–Pleiades φ (14:17; horse Rahu UNISON 0.141%); Equator–Procyon φ (14:29; horse Venus); Capella–Regulus (14:02; horse Ketu 0.059%); [Algorab–Fomalhaut (14:32) REMOVED 8 Oct – not a real chord: a mixed lock (φ², 13/8, φ) whose closest approach was 0.164% at 14:32; Mercury's only Dec chord on Algorab–Fomalhaut is φ, exact 15:17:41, 0.212% at the off]; Equator–Regulus √2 (13:47; horse Neptune 0.079%, Pallas UNISON). Applying: Aldebaran–Sirius (15:17; Noonan Chiron 0.099%).
- **PROCYON in five of Mercury's chords** (Capella–Procyon, Altair–Procyon, Algol–Procyon, Equator–Procyon, Procyon–Spica) — Procyon is on both Method 1 lists (horse Eris's Bellatrix–Procyon; jockey Eris's Deneb Algedi–Procyon, Neptune's Procyon–Spica).
#### Venus (RA 312.954, Dec −15.286; +0.99/d RA, +0.16/d Dec)
- 13 chords within 0.15% around the off (RA 4, Dec 8, Sky 1). No numbers. Slow parallels only for others: sky Venus on Mulqueen's natal SATURN Dec (0.007) and near Oot Ma Way's Quaoar (0.079).
- Quieter for the pair: nothing of theirs comes exact in the race. Closest in time: **Dec ALGOL–BELLATRIX 5:8:13, applying through the race, exact 15:10:28 (off+30)** (0.031% → 0.016% → 0.013% → 0.000%) — horse's NEPTUNE 2:5:7 0.082%; tightest Fiamette Eris 0.007%.
- Dec ALDEBARAN–REGULUS 1:6:7 exact 14:39:25 (1.3 min before the off; 0.001% at the off) — no pair body; Mulqueen's Saturn (UNISON) and Oot Ma Way's Mercury (UNISON).
- Slow holds for the pair (separating or applying over hours):
  - RA ARCTURUS–REGULUS 5:8:13 — **Noonan's MERCURY in UNISON 0.034%** (exact 11:24).
  - Dec ANTARES–CASTOR φ — Noonan's PALLAS 0.031%, CHIRON 0.091% (exact 13:29).
  - Dec ALKAID–POLARIS φ — Noonan's PLUTO 0.038%, CHIRON 0.127%; horse's JUPITER 0.088% (exact 06:10).
  - Dec CAPELLA–POLARIS √2 — Noonan's ERIS 0.061% and his VENUS 0.072% (SAME BODY) (exact 04:01 next day, applying).
  - Dec BELLATRIX–VEGA 2:3:5 — horse's CHIRON 0.057% (exact 16:27, applying).
- **Small stacks on the horse (two fast bodies on one string, same natal body, neither exact near the race):** horse's SEDNA on RA POLARIS–SIRIUS (Sun 5:8:13, Venus 3:4:7; Sedna 0.107%); horse's KETU on Dec CAPELLA–REGULUS (Mercury 3:5:8, Venus 4:5:9; Ketu 0.059%) — Capella–Regulus is a busy base (11 natal bodies in 8 charts).
#### Mars (RA 311.660, Dec −19.038; +0.76/d RA, +0.19/d Dec)
- 14 chords within 0.15% around the off (RA 4, Dec 8, Sky 2). Number: Dec to Betelgeuse 238/9 (chance level). No slow parallel.
- **★ RA ALTAIR–ARCTURUS 1:6:7, exact AT THE OFF (14:40:41)** (0.118% off−30 → 0.003% off → 0.012% finish → 0.109% off+30). **The horse's SUN is the tightest in the field, 0.017%** (φ), and her MARS is on it too (4:5:9, 0.096%, SAME BODY). Only one other body in the whole field (Hamilton Gonggong 0.132%). Base 83.784: sky Mars beyond the ALTAIR end (13.964 from Altair); her Sun beyond the same end, further out (32.007 from Altair); her Mars inside (46.566 / 37.217).
  - Method 1 and Method 3 meet: Altair–Arcturus φ is on her Method 1 list (her Sun's φ, with Arcturus = her Sun's Flat whole 120). §62 saw the same strike in Method 2.
- **Dec BELLATRIX–EQUATOR 1:3:4 (exact 13:54, separating; 0.031% at the off)** — the horse's ORCUS (φ 0.058%) and Noonan's RAHU (φ 0.054%) make the SAME chord on it, and his KETU too (φ 0.141%) — the direct link from Method 1 (her Orcus parallel his Rahu, contraparallel his Ketu, 0.005) showing on a string. Also her PALLAS 0.061%. 12 bodies in 9 charts — a busy base.
- **RA CAPELLA–RIGEL 1:5:6 (exact 13:45, separating; 0.067% at the off)** — **Noonan's NEPTUNE tightest in the field again, 0.021%** (Capella–Rigel is one of his Neptune's four Method 1 star chords); horse's JUPITER 0.039%.
- Dec RIGEL–SPICA 3:8:11 (exact 12:42) — **Noonan's CHIRON tightest, 0.043%**; horse's Venus 0.089%.
- Others: RA Betelgeuse–Vega φ (horse Uranus 0.141%); Sky Algol–Castor (horse Juno 0.123%, only chart).
- Noonan's NEPTUNE so far: Sun (Alkaid–Arcturus in the race; Procyon–Spica after), Mercury (Procyon–Spica after the finish), Mars (Capella–Rigel, separating) — three of his Neptune's four Method 1 strings played.
#### Jupiter (RA 349.178, Dec −5.730; +0.22/d RA, +0.09/d Dec)
- 10 chords within 0.15% around the off (RA 2, Dec 8). Number: **RA to ANTARES = 72√2** (101.8242; 101.8249 at the finish) — Antares is the recurring star of both Method 1 lists (horse — eight bodies by number). Slow parallel only for Fiamette (her Sun, 0.053).
- **★ Dec BETELGEUSE–PROCYON 1:5:6, applying through the race, exact 15:22:05** (0.041% off−30 → 0.024% off → 0.021% finish → 0.006% off+30). **The horse's CHIRON is the tightest in the field, 0.004%** (5:8:13), **and Noonan's CHIRON is on the same string** (φ 0.047%) — the same natal body in both charts on the string Jupiter plays. The horse's TRANSPLUTO (φ 0.119%) and URANUS (0.131%) too. This string is on the combined Method 1 list (held in both charts: horse Chiron/Transpluto/Uranus, jockey Chiron). Base 2.189: all three beyond the PROCYON end, on the same side — her Chiron nearest (3.500 from Procyon), his Chiron (9.242), sky Jupiter furthest (10.947).
- **Dec ALPHECCA–REGULUS 5:6:11, applying, exact 15:07:41 (23 min after the finish)** (0.021% → 0.010% → 0.008% → 0.001%). Noonan's ORCUS (3:4:7, 0.036% — his receiver) and JUNO (φ 0.037%). Tightest Fiamette Orcus 0.008%.
- Slow, separating: Dec Capella–Castor (horse Venus 0.052%); Dec Altair–Procyon (Noonan Sun, horse Orcus, both ~0.14%); Dec Fomalhaut–Pleiades (horse Juno 0.058%, Noonan Eris 0.096%).
#### Saturn (RA 323.122, Dec −15.548; +0.10/d RA, +0.03/d Dec — its chords stand all afternoon)
- 13 chords within 0.15% around the off (RA 4, Dec 6, Flat 1, Sky 2). Numbers: RA to ALPHECCA 805/9 and RA to VEGA 395/9 (two ninths; chance 1.5). Slow parallel: sky Saturn's Dec near natal QUAOAR in all four 2018 horses (Olympe De Gouges 0.081, Fiamette 0.027, Suntory Star 0.073, Poetria 0.083) — a cohort feature, not individual.
- **★ Dec ALPHECCA–FOMALHAUT 1:3:4, steady all afternoon (0.076% off−30 → 0.069% off → 0.068% finish → 0.063% off+30; exact 20:23)** — **the whole three-body string from Noonan's Method 1 list:** his CHIRON 5:6:11 0.010% (tightest in the field), ERIS φ 0.125%, PALLAS 1:1:2 0.129% (his Pallas at the midpoint). Sky Saturn sits on it through the race. Eight natal bodies in four charts.
- **Noonan's CHIRON again:** Dec BETELGEUSE–SPICA φ (0.034% at the off, exact 15:51; his Chiron 0.090%; tightest Oot Ma Way's Saturn 0.001%). With Jupiter's Betelgeuse–Procyon, his Chiron is on three slow-sky strings so far.
- **Noonan's own SATURN (SAME BODY):** Sky ANTARES–REGULUS √2 (0.028% at the off, steady; his Saturn 0.047%) and Dec BELLATRIX–SPICA 1:4:5 (his Saturn 0.119%, his PALLAS 0.053%).
- **Horse:** RA ALTAIR–DENEB ALGEDI 1:7:8, applying through the race, exact 15:14:53 (0.075% off → 0.066% finish → 0.010% off+30) — her MARS 5:8:13 0.142%. Loose holdings: Pleiades–Procyon (her Transpluto 0.145%), Procyon–Vega (her Rahu 0.086%), Altair–Pleiades (her Pluto 0.146%).
- ALPHECCA: in two of Saturn's chords and one of its numbers; Alphecca is on both Method 1 lists (the nodes to Alphecca in both charts).
#### Uranus (RA 39.618, Dec +15.062; +0.04/d RA, +0.01/d Dec)
- 12 chords within 0.15% around the off (RA 2, Dec 7, Flat 3). Numbers: three ninths (chance 1.5) — Dec to Aldebaran 13/9, RA to Capella 356/9, **RA to Sirius 555/9 (61.6668 at the off, 61.6666 at the finish)**. Slow parallel only for Poetria (her Venus, 0.007).
- **★ Dec ALTAIR–BETELGEUSE φ, exact 14:51:29 — a slow body sitting on an exact chord through the race** (0.007% off−30 → 0.002% off → 0.001% finish → 0.003% off+30). **Noonan's SUN is the tightest in the field, 0.058%** (1:8:9). Only three bodies in the field on it (Mulqueen Jupiter, Poetria Venus).
  - Sky Uranus is 6.194 from Altair in Dec in three chords (Altair–Betelgeuse, Altair–Regulus 1:1:2 with REGULUS at the midpoint of Uranus and Altair, Altair–Capella).
- **Noonan:** Dec ALGORAB–VEGA 3:4:7 (steady 0.143%, exact in 1.4 d) — **his PALLAS tightest in the field, 0.024%**; Dec ALGOL–ANTARES (steady 0.149%) — his VENUS 0.054%; Dec EQUATOR–PLEIADES 3:5:8 (steady 0.066%) — his CHIRON 0.095%, VENUS 0.138%.
- **Horse:** Dec ALPHECCA–RIGEL 1:2:3 (steady 0.131%) — her ERIS 0.066% and PALLAS 0.071%; RA BELLATRIX–PLEIADES √2 (steady 0.075%) — her PALLAS 0.105%. Her Eris and Pallas were together on the Sun's Bellatrix–Rigel too (in the race).
#### Neptune (RA 353.796, Dec −3.902; +0.03/d RA, +0.01/d Dec — nothing of the pair's comes exact on the race day; all holds are steady)
- 20 chords within 0.15% around the off (RA 5, Dec 11, Flat 2, Sky 2). Number: RA to ANTARES 958/9 (Antares again, after Jupiter's 72√2). No slow parallel.
- **Two stacks with earlier sky bodies (same string, same natal bodies):**
  - **Dec ALKAID–POLARIS** — Venus (φ) and now Neptune (3:4:7, steady 0.122%): **Noonan's PLUTO 0.038%**, his CHIRON 3:4:7 (UNISON with Neptune) 0.127%, the horse's JUPITER 0.088%.
  - **Dec ALTAIR–PROCYON** — Jupiter (1:3:4) and now Neptune (2:5:7, steady 0.094%): Noonan's SUN 0.139% and the horse's ORCUS 0.147%.
- **RA ALDEBARAN–FOMALHAUT 1:8:9 (steady 0.112%)** — the horse's TRANSPLUTO 1:1:2 0.042% (Aldebaran at the RA midpoint of her Transpluto and Fomalhaut — on her Method 1 list) and her PLUTO 0.132%. Ten bodies in six charts.
- Dec BELLATRIX–SIRIUS 4:5:9 (steady 0.097%) — horse's URANUS 0.041%, GONGGONG 0.099%; Noonan's PLUTO 0.056%.
- Dec ALDEBARAN–DENEB ALGEDI 3:5:8 — Noonan's VESTA 0.075%, KETU 0.123%; horse's Pluto 0.148%.
- Dec Alphecca–Deneb Algedi (Noonan Ceres 0.103%, Sun 0.140%); Dec Aldebaran–Algorab (Noonan Vesta 0.140%); Dec Arcturus–Bellatrix (Noonan Quaoar 0.132%); RA Alkaid–Altair (horse CERES 0.051%); Sky Pleiades–Regulus (horse CHIRON 0.103% — the tightest, only two bodies in the field).
- Noonan's PLUTO comes up on two Neptune strings (Alkaid–Polaris, Bellatrix–Sirius).
#### Pluto (RA 300.357, Dec −22.410; +0.02/d RA, +0.002/d Dec — near standstill in Dec)
- 8 chords within 0.15% around the off (RA 4, Dec 4). Numbers: RA to Algorab 1016/9, RA to ARCTURUS 778/9 (two ninths; chance 1.5).
- **Slow parallel: sky Pluto on the horse's natal SATURN Dec (0.013)** — also Suntory Star's Saturn (0.002) and Fiamette's (0.058): the 2018 horses share a Saturn Dec. With Pluto on her Saturn's Dec, her Saturn joins Pluto's Dec chords — it is in UNISON on two of them (Bellatrix–Pleiades φ, Alphecca–Bellatrix √2).
- **★ Dec RIGEL–SIRIUS 2:3:5, steady (0.018% at every check)** — **the horse's MARS is the tightest in the field, 0.005%** (3:5:8). Base 8.523: sky Pluto beyond the SIRIUS end (5.683 from Sirius) and her Mars beyond the same end (5.112). Her Mars is now on strings from Mars (Altair–Arcturus at the off), Mercury (Altair–Castor UNISON), Saturn (Altair–Deneb Algedi) and Pluto (Rigel–Sirius).
- **Dec ALPHECCA–BELLATRIX √2 (steady 0.134%)** — **Noonan's VENUS in UNISON 0.027%**, his PALLAS 0.068%; the horse's SATURN in UNISON 0.084% and her HAUMEA at the midpoint (1:1:2). 11 bodies in 7 charts.
- **Stack — Dec BELLATRIX–PLEIADES:** Mercury (5:6:11, exact 14:11) and now Pluto (φ, steady 0.094%): **Noonan's SUN 0.049%** and the horse's SATURN (UNISON with Pluto) 0.140%.
- RA ALGOL–ALPHECCA 5:8:13 (steady 0.009%) — horse's ERIS 0.078%, Noonan's URANUS 0.096%. RA DENEB ALGEDI–VEGA 4:5:9 (steady 0.010%) — Noonan's JUPITER 0.112%. Dec ANTARES–SIRIUS √2 — horse's SEDNA 0.046%.
#### Chiron (RA 9.520, Dec +6.250; +0.05/d RA, +0.02/d Dec — holds steady through the race)
- 16 chords within 0.15% around the off (RA 4, Dec 6, Flat 4, Sky 2). Numbers: **Dec to ALTAIR = φ² (2.6182)**, RA to Fomalhaut 226/9. No slow parallel.
- **★ Both TRANSPLUTOS held:**
  - **Dec ARCTURUS–PLEIADES φ (steady 0.076%)** — **the horse's TRANSPLUTO 0.001%, the tightest in the field** — her strongest Method 1 string. Base 4.938: sky Chiron beyond the ARCTURUS end (12.917 / 17.855) and her Transpluto beyond the same end (8.228 / 13.164). Her Venus 0.093% too.
  - **Dec ALKAID–FOMALHAUT 5:6:11 (steady 0.026%)** — **Noonan's TRANSPLUTO in UNISON, 0.017%, the tightest in the field** — a MIRROR inside the string: sky Chiron 43.060 from Alkaid / 35.874 from Fomalhaut; his Transpluto 35.884 / 43.053 — the same two distances swapped.
- **Stacks with earlier sky bodies:**
  - RA CASTOR–PLEIADES — Mercury (4:5:9) and Chiron (5:6:11, steady 0.062%): **Noonan's ORCUS 0.022%, tightest both times** (his receiver).
  - Dec ALPHECCA–RIGEL — Uranus (1:2:3) and Chiron (√2, steady 0.094%): the horse's ERIS 0.066% and PALLAS 0.071% (her Eris and Pallas also together on the Sun's Bellatrix–Rigel in the race).
- Dec ANTARES–EQUATOR φ (steady 0.157%) — **the horse's HAUMEA 0.015%, tightest**; Noonan's URANUS in UNISON 0.041%, MAKEMAKE 0.127%. (Antares–Equator was on the combined Method 1 list — held in both charts.)
- Dec ALDEBARAN–CASTOR 2:3:5 (steady 0.040%) — horse's JUNO 0.058%; Noonan's ERIS, TRANSPLUTO, CHIRON (SAME BODY) ~0.10%. 12 bodies in 7 charts.
- Others: Dec Sirius–Vega √2 (horse Neptune 0.130%); RA Altair–Bellatrix (Noonan's Chiron, SAME BODY, only chart).
#### Ceres (RA 66.617, Dec +23.317 — just inside the bounds; +0.32/d RA, +0.08/d Dec)
- 13 chords within 0.15% around the off (RA 4, Dec 7, Flat 1, Sky 1). Numbers: four — **Dec to BELLATRIX 12√2** and RA to BELLATRIX 132/9 (Bellatrix both ways), RA to Capella 113/9, RA to Sirius 312/9 (chance 0.44 + 1.5). Slow parallel only for Davies (his Haumea, 0.000).
- **Stack — Dec ALPHECCA–BELLATRIX:** Pluto (√2, steady) and now Ceres (1:5:6, exact 14:22:41, 18 min before the off; 0.035% at the off, 0.044% at the finish): **Noonan's VENUS 0.027%** and PALLAS 0.068%; the horse's SATURN 0.084% and HAUMEA (midpoint) 0.139%. The only whole-day hit near the race.
- RA ALGOL–BELLATRIX 3:4:7 (exact 13:52) — **Noonan's SATURN φ 0.016%** (second tightest; Hamilton Makemake 0.003%).
- **Strings now played by three or more sky bodies, holding the same horse body:**
  - Dec CAPELLA–REGULUS — Mercury, Venus, Ceres: the horse's KETU 0.059%.
  - RA POLARIS–SIRIUS — Sun, Venus, Ceres: the horse's SEDNA 0.107%.
- RA Polaris–Procyon 3:5:8 (exact 13:43) — horse's ORCUS 0.090%.
- BELLATRIX keeps coming: Ceres's two numbers; Alphecca–Bellatrix (Pluto, Ceres), Algol–Bellatrix (Ceres in RA, Venus in Dec), Bellatrix–Rigel (Sun, in the race), Bellatrix–Pleiades (Mercury, Pluto), Bellatrix–Sirius (Neptune), Bellatrix–Equator (Mars).
#### Pallas (RA 15.551, Dec −6.270; +0.38/d RA, +0.09/d Dec)
- 21 chords within 0.15% around the off (RA 6, Dec 14, Sky 1). Number: Dec to Aldebaran 205/9. No slow parallel.
- **★ RA ALTAIR–FOMALHAUT 2:3:5, exact AT THE OFF (14:40:41)** (0.025% off−30 → 0.000% off → 0.004% finish → 0.025% off+30). **Noonan's MAKEMAKE φ 0.047%**, his PLUTO 0.138%. Tighter in the field: Fiamette Mars 0.012%, Oot Ma Way Vesta 0.014%, Davies Neptune 0.034%. **The same instant as sky Mars on Altair–Arcturus (the horse's Sun)** — two sky bodies exact at the off, both on ALTAIR strings: Mars on the horse's, Pallas on the jockey's.
- **Dec ALTAIR–EQUATOR √2, exact 14:31:41 (9 min before the off; 0.008% at the off, 0.012% at the finish)** — **Noonan's HAUMEA in UNISON, 0.019%, the tightest in the field.**
- **★ RA ALKAID–VEGA 3:4:7 (steady ~0.147%)** — **Noonan's strongest Method 1 string, all three of its bodies:** his TRANSPLUTO 0.002% (tightest in the field), GONGGONG √2 0.011%, SATURN at the midpoint 0.097%.
- **Stack — Dec ALPHECCA–FOMALHAUT:** Saturn (1:3:4) and now Pallas (√2): Noonan's CHIRON 0.010%, ERIS 0.125%, PALLAS (midpoint, SAME BODY) 0.129%.
- Dec BETELGEUSE–REGULUS 1:3:4 (exact 13:32) — **Noonan's JUNO 0.014%, tightest**; the horse's HAUMEA at the midpoint (1:1:2, 0.055%).
- **Dec PLEIADES–REGULUS 2:3:5 (steady 0.146%) — four of the horse's bodies:** GONGGONG 0.029% (tightest in the field), SUN 0.100%, NEPTUNE 0.130%, CERES 0.131%.
- Others: Dec Equator–Sirius (horse ERIS 0.046%); Dec Altair–Antares (Noonan Uranus 0.072%, horse Gonggong); RA Procyon–Regulus (Noonan Jupiter 0.088%, horse Rahu); RA Betelgeuse–Deneb Algedi (Noonan Orcus 0.143%); RA Algorab–Bellatrix (horse Mars 0.081%); Dec Aldebaran–Polaris (horse Eris 0.115%).
- ALTAIR in four of Pallas's chords (Altair–Fomalhaut, Altair–Equator, Altair–Antares, Altair–Bellatrix); with Mars's Altair–Arcturus and Chiron's φ² to Altair.
#### Juno (RA 317.477, Dec −8.405; +0.37/d RA, +0.11/d Dec)
- 11 chords within 0.15% around the off (RA 5, Dec 6). No numbers (chance 0.44 + 1.5). No slow parallel.
- **★ STACK ON THE HORSE'S SUN — RA ALTAIR–ARCTURUS:** Juno φ exact **14:35:17 (5.4 min before the off)** (0.031% → 0.008% off → 0.013% finish → 0.046%), then sky Mars 1:6:7 exact **at the off (14:40:41)**. **Her SUN the tightest in the field both times (0.017%)**, her MARS on it too (0.096%); only Hamilton's Gonggong besides. Juno sits beyond the ALTAIR end like Mars (19.780 from Altair; Mars 13.964), her Sun beyond the same end (32.007).
- **Dec ANTARES–DENEB ALGEDI 3:4:7, exact 14:46:05 (1.3 min after the finish; 0.005% at the off, 0.001% at the finish)** — **the horse's ERIS in UNISON 3:4:7, 0.058%.** Tightest Davies Transpluto 0.010%.
- **More stacks (same string, same natal bodies, a second sky body):**
  - Dec ALTAIR–CASTOR 3:4:7 — Mercury and Juno, both 3:4:7: the horse's MARS in UNISON with both (0.042%); Noonan's QUAOAR (midpoint) and HAUMEA.
  - Dec ALDEBARAN–CASTOR — Chiron and Juno: the horse's JUNO (SAME BODY) 0.058%; Noonan's ERIS, TRANSPLUTO, CHIRON.
  - Dec ALGORAB–FOMALHAUT — Mercury and Juno: the horse's PLUTO 0.119%; Noonan's SEDNA in UNISON 0.143%.
  - RA/Dec ALGOL–BELLATRIX — Venus (Dec), Ceres (RA), Juno (RA φ): **Noonan's SATURN 0.016%** (RA).
- RA ANTARES–VEGA 5:6:11 (applying, exact 15:42; 0.038% at the finish) — **Noonan's PLUTO 0.016%** (second tightest; Fiamette Makemake 0.009%).
- RA Alphecca–Arcturus φ — horse's SEDNA 0.089%, Noonan's CHIRON 0.137%. Dec Algorab–Pleiades — Noonan's ORCUS 0.075%.
#### Vesta (RA 305.679, Dec −19.164; +0.49/d RA, +0.08/d Dec)
- 14 chords within 0.15% around the off (RA 5, Dec 8, Flat 1). Numbers: **Dec to SPICA whole 8** (8.0012; 8.0009 at the finish), Dec to ARCTURUS 345/9, RA to Vega 238/9 (the same 238/9 as Mars's Dec to Betelgeuse). Slow parallel only for Mulqueen (his Gonggong, 0.007). Nothing of the pair's comes exact near the race.
- **Vesta plays THREE STRINGS FROM THE COMBINED METHOD 1 LIST (held in both charts):**
  - **RA ALPHECCA–ALTAIR 1:8:9 (applying; 0.245% at the off → 0.120% at off+30, exact 15:38)** — **the horse's SUN 0.010%** (1:2:3), **Noonan's PALLAS at the midpoint 0.020%** (1:1:2), the horse's MARS 0.038%. Fifteen bodies in eight charts; Fiamette Ceres 0.004% tightest.
  - **RA ALGOL–FOMALHAUT φ (applying, 0.059% at the off, exact 15:49)** — **Noonan's QUAOAR 0.009%**, the horse's MERCURY φ 0.038%. (O'Farrell Ketu 0.003% tightest.)
  - **Dec ALTAIR–SPICA 2:5:7 (separating, 0.141% at the off)** — **Noonan's SATURN 0.006%, the tightest in the field**, his PLUTO 0.059%; the horse's HAUMEA φ 0.042%.
- **Stack — RA PLEIADES–SIRIUS (also on the combined Method 1 list — a fourth both-charts string for Vesta):** Mercury (5:8:13) and Vesta (2:5:7): **Noonan's MAKEMAKE 0.016% (tightest both times)** and his MERCURY 0.028%; the horse's URANUS 0.110%.
- RA ALPHECCA–CASTOR 3:5:7 (steady 0.038%) — the horse's SUN and MERCURY (both 4:5:6, 0.063% — they share an RA), her VESTA (SAME BODY) 0.100%; Noonan's CHIRON 0.095%.
- Dec ALDEBARAN–VEGA 5:8:13 — the horse's TRANSPLUTO 0.030%, PALLAS 0.111%. Dec Equator–Regulus 5:8:13 — horse's NEPTUNE in UNISON 0.079%, PALLAS. Dec Alkaid–Regulus — horse's VENUS 0.081%. RA Bellatrix–Fomalhaut — Noonan's ERIS 0.147%.
- ALTAIR again (Alphecca–Altair, Altair–Spica) and ALPHECCA (Alphecca–Altair, Alphecca–Castor, Alphecca–Procyon).
#### Eris (RA 26.092, Dec −1.211; +0.009/d RA, +0.005/d Dec — every chord steady for days)
- 14 chords within 0.15% around the off (RA 6, Dec 7, Flat 1). Numbers: Dec to ANTARES 227/9 (Antares again), RA to Deneb Algedi 534/9, RA to Pleiades 277/9 (three ninths; chance 1.5). Slow parallel only for Oot Ma Way (his Eris, RA, 0.079).
- Quiet for the pair; all holds steady, none exact on the day:
  - RA CASTOR–RIGEL 2:3:5 (0.030% throughout) — Noonan's PALLAS 0.030%, URANUS 0.097%; horse's VESTA 0.047%.
  - Dec ALGOL–SPICA φ (0.024%) — Noonan's HAUMEA 0.049%.
  - RA PLEIADES–RIGEL √2 (0.015%) — Noonan's SATURN 0.106%, horse's SUN 0.126%.
  - RA CASTOR–SPICA 1:1:2 (sky Castor at the RA midpoint of Eris and Spica) — horse's QUAOAR 0.089%, TRANSPLUTO 0.118%.
  - Dec ALDEBARAN–CAPELLA — Noonan's VENUS 0.061%, SEDNA 0.095%.
- **Stacks with earlier bodies:** Dec ANTARES–SIRIUS (Pluto √2, Eris 5:8:13) — the horse's SEDNA 0.046%; Dec ALTAIR–ANTARES (Pallas, Eris) — Noonan's URANUS 0.072%, horse's GONGGONG; RA DENEB ALGEDI–VEGA (Pluto, Eris, both 4:5:9) — Noonan's JUPITER 0.112%.
- **Natal-to-transit numbers, same body, the slow bodies (16 bodies × 4 measures × 2 charts = 128 values; chance ≈ 1.2 φ/√2/whole and ≈ 4 ninths):**
  - **No Eris number for either** (Noonan's Eris RA 2.8938 is only "near" 26/9). Unlike Messi, Dettori and the lottery winner; like Frankel.
  - Hits: **horse TRANSPLUTO — RA whole 1 (1.0011)**; Orcus Sky 30/9; Pluto Flat 79/9. **Noonan SEDNA — Dec 31/9 and Flat 124/9 (his hub, two)**; HAUMEA Flat 18√2; Transpluto Flat 76/9; Jupiter Flat 908/9. Totals: 2 φ/√2/whole (vs 1.2), 7 ninths (vs 4) — a little above chance. Near (0.002–0.005): horse Sedna RA 22/9, Transpluto Dec φ⁻², Chiron Flat whole 15; Noonan Orcus RA 188/9, Uranus Dec 328/9.
#### Sedna (RA 58.411, Dec +8.171; +0.007/d RA, +0.004/d Dec — the slowest; chords stand for days)
- 13 chords within 0.15% around the off (RA 4, Dec 9). Numbers: RA to Rigel 182/9, Dec to Spica 174/9 (chance level). No slow parallel.
- **★ RA CAPELLA–POLARIS 1:1:2 — sky Sedna at the RA MIDPOINT of Capella and Polaris (20.761 / 20.739), steady 0.106%** — a string from the COMBINED Method 1 list, all three of its bodies: **the horse's CERES 0.009% (tightest in the field)**, her GONGGONG 0.031%, Noonan's KETU 0.075%.
- **Stacks:**
  - RA ALDEBARAN–FOMALHAUT — Neptune (1:8:9) and Sedna (1:7:8): the horse's TRANSPLUTO (Aldebaran at the midpoint of her Transpluto and Fomalhaut) 0.042%, her PLUTO.
  - Dec ALTAIR–PROCYON — now three sky bodies (Jupiter, Neptune, Sedna): Noonan's SUN 0.139% and the horse's ORCUS (UNISON with Sedna, φ) 0.147%.
- Dec CAPELLA–FOMALHAUT 1:1:2 (sky Sedna at the Dec midpoint) — the horse's MERCURY 0.079%, CHIRON 0.103%; Noonan's SEDNA (SAME BODY) 0.124%.
- Dec ALGORAB–ALKAID 3:5:8 (steady 0.022%) — the horse's RAHU at the midpoint (1:1:2) 0.100%; Noonan's TRANSPLUTO 0.139%. Only two bodies in the field.
- Others: Dec Algol–Castor (horse Uranus 0.086%); Dec Algorab–Alphecca (Noonan Vesta 0.089%).
- MIDPOINTS: Sedna sits at a midpoint in two of its own chords (Capella–Polaris RA, Capella–Fomalhaut Dec); the horse's Rahu and Transpluto are midpoint figures on two others.
#### Haumea (RA 217.313, Dec +15.613; −0.012/d RA, +0.010/d Dec)
- 7 chords within 0.15% around the off (Dec 6, Sky 1). **Numbers: five ninths (chance 1.5)** — RA to Aldebaran 1335/9, **Dec to ARCTURUS 32/9**, RA to Deneb Algedi 985/9, RA to Pleiades 1444/9, Dec to Spica 241/9. No slow parallel.
- **★ Stack — Dec BETELGEUSE–REGULUS:** Pallas (1:3:4) and now Haumea (4:5:9, 0.014% off−30 → 0.008% off → 0.007% finish → 0.002% off+30, exact 15:24): **Noonan's JUNO 0.014%, tightest in the field both times**; the horse's HAUMEA at the midpoint (1:1:2, 0.055%) — sky Haumea on her Haumea's own string (SAME BODY). Only three bodies in the field.
- Dec ALKAID–ALTAIR 1:5:6 (steady 0.089%) — **the horse's KETU 0.020%, tightest in the field.**
- Dec ALGORAB–SPICA 1:5:6 (steady 0.008%) — Noonan's KETU 0.072%, CHIRON 0.100%; the horse's MERCURY 0.118%.
- Stack — Dec BELLATRIX–VEGA: Venus (2:3:5) and Haumea (2:5:7): the horse's CHIRON 0.057% both times.
- Dec ALKAID–RIGEL √2 — Noonan's VESTA 0.069%, the horse's KETU 0.099%. Sky REGULUS–RIGEL — horse's Mercury (only chart).
#### Makemake (RA 198.806, Dec +22.826; −0.015/d RA, +0.008/d Dec — steady for days)
- 16 chords within 0.15% around the off (RA 5, Dec 9, Sky 2). Number: RA to ALTAIR 890/9. Slow parallel only for Hamilton (his Haumea, 0.037).
- **★ Noonan's SEDNA (his hub) on TWO of its Method 1 strings:**
  - **Dec ALGOL–POLARIS 3:8:11 (steady 0.078%) — his SEDNA 0.004%** — the hub's own string, the one the Moon held through the race in §62. (Poetria Transpluto 0.001% tighter.) Horse's Pallas 0.133%.
  - **RA ANTARES–FOMALHAUT 1:2:3 (steady 0.040%) — the whole three-body string from his Method 1 list: SEDNA 0.025% (tightest), PALLAS 0.054%, ERIS 0.120%.** Only four bodies in the field (Davies Venus the other).
- **Dec ALPHECCA–CASTOR 3:4:7 (steady 0.026%) — Noonan's SUN 0.006%, tightest in the field**; his ORCUS 0.119%. Only three bodies in the field.
- **Strings now played by three sky bodies:**
  - RA CASTOR–PLEIADES — Mercury, Chiron, Makemake: **Noonan's ORCUS 0.022%, tightest every time.**
  - Dec ALPHECCA–BELLATRIX — Pluto, Ceres, Makemake: Noonan's VENUS 0.027%, PALLAS; horse's SATURN, HAUMEA (midpoint).
  - Dec ALPHECCA–RIGEL — Uranus, Chiron, Makemake: the horse's ERIS 0.066%, PALLAS 0.071%.
  - Dec ALGORAB–FOMALHAUT — Mercury, Juno, Makemake: horse's PLUTO, Noonan's SEDNA.
- Stack — Dec ALGOL–CASTOR (Sedna, Makemake): horse's URANUS 0.086%.
- Others: Dec Deneb Algedi–Equator √2 (Noonan TRANSPLUTO 0.048%); RA Alkaid–Antares (horse CHIRON 0.032%); Dec Castor–Regulus (Noonan JUNO in UNISON 0.119%).
#### Quaoar (RA 277.194, Dec −15.316; +0.007/d RA, +0.004/d Dec)
- 9 chords within 0.15% around the off (RA 4, Dec 5). Number: Dec to RIGEL 64/9. Slow parallels only for others (Oot Ma Way's Quaoar, Mulqueen's Saturn).
- **★ Dec ALDEBARAN–BETELGEUSE 2:5:7 (steady 0.146%) — a COMBINED Method 1 string with all four of its bodies:** **Noonan's PLUTO 0.006% (tightest in the field)** and **the horse's CHIRON 0.013%** — both 5:8:13, the same chord in the two charts — plus her KETU φ 0.050% and VESTA 0.130%.
- **Dec ALKAID–POLARIS — now three sky bodies (Venus, Neptune, Quaoar):** Noonan's PLUTO 0.038% each time, his CHIRON (UNISON with Neptune), the horse's JUPITER 0.088%.
- RA Algol–Deneb Algedi φ — the horse's SATURN 0.046%. Dec Capella–Equator — the horse's JUPITER 0.086%.
- Noonan's PLUTO so far: Alkaid–Polaris (Venus, Neptune, Quaoar), Bellatrix–Sirius (Neptune), Aldebaran–Betelgeuse (Quaoar, tightest), Antares–Vega (Juno 0.016%), Altair–Fomalhaut (Pallas, at the off).
#### Orcus (RA 156.225, Dec −11.924; −0.016/d RA, +0.008/d Dec)
- 11 chords within 0.15% around the off (RA 3, Dec 8). Numbers: RA to Alkaid 456/9, Dec to REGULUS 215/9.
- **★ SLOW PARALLEL: sky Orcus on Noonan's natal JUNO Dec (−11.924 / −11.906, 0.018)** — the second slow parallel for the pair (after Pluto on the horse's Saturn); this one is his alone (Oot Ma Way's Gonggong the only other, 0.089). His Juno therefore joins Orcus's Dec chords: **in UNISON on six of them** (Betelgeuse–Polaris φ 0.046%, Betelgeuse–Regulus φ 0.014%, Castor–Regulus 0.119%, Alphecca–Polaris φ 0.078%, Alphecca–Betelgeuse 1:1:2 0.023%, Alphecca–Regulus φ 0.037%).
- **★ RA CASTOR–PLEIADES — now FOUR sky bodies (Mercury, Chiron, Makemake, Orcus): Noonan's ORCUS 0.022%, tightest every time — and sky Orcus is the same body (SAME BODY).** Sky Orcus 3:4:7, steady 0.031%.
- **Dec BETELGEUSE–REGULUS — three sky bodies (Pallas, Haumea, Orcus): Noonan's JUNO tightest every time (0.014%)**; the horse's HAUMEA at the midpoint.
- **Stack — Dec ALPHECCA–REGULUS (Jupiter, Orcus):** Noonan's ORCUS 0.036% (SAME BODY with sky Orcus) and JUNO 0.037%.
- **Dec ALPHECCA–ANTARES 3:8:11 — Noonan's TRANSPLUTO 0.010%, tightest in the field.**
- Horse: Dec Alphecca–Betelgeuse (her PLUTO 0.041%); Dec Alphecca–Polaris (her Chiron, Sun ~0.13%).
- Others: Dec Betelgeuse–Polaris (Noonan SUN 0.096%); RA Betelgeuse–Capella (Noonan TRANSPLUTO, only chart).
- Sky Orcus is the jockey's body: his receiver (Method 1) held as the same body on Castor–Pleiades and Alphecca–Regulus, and his Juno parallel to it.
#### Gonggong (RA 337.026, Dec −11.162; +0.010/d RA, +0.004/d Dec)
- 11 chords within 0.15% around the off (RA 3, Dec 8). Numbers: RA to Algorab 1346/9 (149.5556, dead on), RA to ARCTURUS 1108/9. No slow parallel.
- **★ Stack — RA ALKAID–VEGA (Pallas 3:4:7, Gonggong 4:5:9), steady 0.146%: Noonan's strongest Method 1 string, all three bodies again** — TRANSPLUTO 0.002% (tightest), **GONGGONG 0.011% (SAME BODY with sky Gonggong)**, SATURN at the midpoint 0.097%.
- **Dec ALDEBARAN–FOMALHAUT 2:3:5 (steady 0.086%) — the horse's GONGGONG 0.032%, tightest in the field (SAME BODY)**; her JUNO 0.107%, SUN 0.128%.
- Dec ALDEBARAN–ALTAIR φ — Noonan's JUPITER 0.020%. Dec Algol–Altair — Noonan's PLUTO 0.102%, horse's VESTA 0.122%. Dec Castor–Polaris — Noonan's CHIRON 0.118%.
- Same body both sides: sky Gonggong holds Noonan's Gonggong (Alkaid–Vega) and the horse's Gonggong (Aldebaran–Fomalhaut).
#### Transpluto (RA 154.520, Dec +10.563; −0.008/d RA, +0.003/d Dec)
- 14 chords within 0.15% around the off (RA 6, Dec 6, Flat 2). Number: RA to Fomalhaut 1531/9. Slow parallel only for Davies (his Mercury, RA 0.003).
- **RA PLEIADES–SIRIUS — now three sky bodies (Mercury, Vesta, Transpluto): Noonan's MAKEMAKE 0.016%, tightest every time**, his MERCURY 0.028%; horse's URANUS 0.110%. (A combined Method 1 string.)
- **Dec ANTARES–EQUATOR — Chiron (φ) and Transpluto (2:5:7): the horse's HAUMEA 0.015%, tightest both times**; Noonan's URANUS 0.041%, MAKEMAKE 0.127%. (A combined Method 1 string.)
- RA SPICA–VEGA 3:5:8 (steady 0.050%) — **Noonan's URANUS 0.025% (joint tightest with Davies Mercury)**, his MAKEMAKE 0.033%.
- Dec CASTOR–DENEB ALGEDI — **Noonan's ERIS 0.081%, tightest**, his TRANSPLUTO 0.096% (SAME BODY).
- Stacks: Dec ALGORAB–PLEIADES (Juno, Transpluto) — Noonan's ORCUS 0.075%; RA BELLATRIX–PLEIADES (Uranus √2, Transpluto 1:3:4) — horse's PALLAS 0.105%; Dec ALTAIR–PLEIADES (Saturn, Transpluto) — horse's PLUTO 0.146%.
- Others: RA Algorab–Sirius (Noonan RAHU 0.059%); Dec Capella–Pleiades (horse SUN 0.118%); RA Antares–Betelgeuse (Noonan MAKEMAKE 0.109%).
- PLEIADES in five of Transpluto's chords (Bellatrix–, Sirius–, Algorab–, Capella–, Altair–Pleiades).
#### The nodes — Rahu (RA 51.219, Dec +18.671) and Ketu (RA 231.219, Dec −18.671); −0.14/d RA, ∓0.035/d Dec
- Rahu 15 chords (RA 3, Dec 12), Ketu 4 (RA 2, Dec 2). Numbers: Rahu Dec to VEGA 181/9; Ketu Dec to PLEIADES 385/9 and Dec to PROCYON 215/9 (the same 215/9 as Orcus's Dec to Regulus).
- **★ Slow parallel: sky KETU on Noonan's natal GONGGONG Dec (−18.671 / −18.691, 0.020)** — the third pair parallel (Pluto on the horse's Saturn; Orcus on Noonan's Juno).
- **Two COMBINED Method 1 strings, every one of their bodies (Rahu):**
  - **Dec REGULUS–VEGA 1:3:4 (applying, 0.042% off → 0.040% finish → 0.028% off+30; exact 16:07):** the horse's PLUTO 0.023%, CHIRON 0.047%; Noonan's PALLAS 0.058%, VESTA 0.086%, ERIS 0.139%. (Suntory Star's Pluto 0.001% tightest — the 2018 horses share a Pluto.)
  - **Dec ALGOL–ALKAID 3:8:11 (steady 0.046%):** Noonan's VESTA 0.058%; the horse's JUNO 0.073%, SEDNA 0.077%.
- **Strings now played by three sky bodies (with Rahu):**
  - Dec ALPHECCA–FOMALHAUT — Saturn, Pallas, Rahu: **Noonan's CHIRON 0.010%, tightest every time**, ERIS, PALLAS (midpoint).
  - Dec ALPHECCA–REGULUS — Jupiter, Orcus, Rahu: Noonan's ORCUS 0.036%, JUNO 0.037%.
  - Dec ANTARES–EQUATOR — Chiron, Transpluto, Rahu: **the horse's HAUMEA 0.015%, tightest every time**; Noonan's URANUS, MAKEMAKE.
- **Stacks (with Ketu):** Dec ALTAIR–SPICA — Vesta and Ketu: **Noonan's SATURN 0.006%, tightest both times**, his PLUTO; the horse's HAUMEA (a combined string). RA PLEIADES–RIGEL — Eris and Ketu: Noonan's SATURN, the horse's SUN.
- Others (Rahu): Dec Alphecca–Vega (horse PLUTO 0.025%); Dec Fomalhaut–Spica φ (horse HAUMEA 0.037%, Noonan TRANSPLUTO 0.102%).
### METHOD 2 REVISITED — the Moon from off−30 to finish+30 (Eddie 13:27 "good plan")
- Change: the three Method 2 scripts (layer1_tuned, nodes_tuned, layer_tuned) take MOONWIN=wide → the Moon every 15 s from off−30 (14:10:41) to finish+30 (15:14:49), from the 1-minute engine grid. Default run unchanged (checked: L2 output identical). Extractor: scratchpad m2new.py → m2new_doncaster.txt (only Moon strikes outside the old window 14:38:41–14:44:49).
- New Moon strikes per chart (all tuned / both sides ≤0.02%): Olympe De Gouges 178/24, Noonan 156/26, Oot Ma Way 157/23, O'Farrell 168/24, Poetria 158/25, Hamilton 170/35, Fiamette 183/18, Davies 146/23, Suntory Star 145/21, Mulqueen 187/30 — by count the pair does not stand out (the Moon touches some natal string every minute or so).
- **On strings already found in Methods 1 and 3 (what the wider window adds):**
  - **Noonan's NEPTUNE — the fourth Method 1 string now played: the Moon RA 3:4:7 on ALKAID–REGULUS, exact 14:50:58 (6 min after the finish)**, his Neptune 0.019%. All four of his Neptune's star chords are now struck on the day: Alkaid–Arcturus (Sun, in the race), Procyon–Spica (Mercury 27 s and Sun 7.5 min after the finish), Capella–Rigel (Mars, separating), Alkaid–Regulus (the Moon, 6 min after the finish).
  - **Noonan's ERIS — his tightest Method 1 string: the Moon Dec 1:6:7 on DENEB ALGEDI–PROCYON, exact 15:10:04**, his Eris 0.000%.
  - **Noonan's SATURN — the Moon Dec 1:2:3 on ALTAIR–SPICA, exact 15:04:22** (his Saturn 0.006%) — the Moon joins Vesta and Ketu on that combined string.
  - **Noonan's PLUTO — the Moon RA 1:2:3 on ANTARES–VEGA, exact 15:08:31** (his Pluto 0.016%) — the Moon joins Juno.
  - Noonan's MERCURY — the Moon Dec 3:4:7 on ARCTURUS–REGULUS, exact 14:22:36 (his Mercury φ 0.007%) — Venus's string.
  - **The horse's GONGGONG — the Moon Dec 3:4:7 on ALDEBARAN–RIGEL, exact 14:45:34 (45 s after the finish)** (her Gonggong 0.021%); **and Dec 4:5:9 on PLEIADES–REGULUS, exact 14:49:02** (her Gonggong 0.029%; Pallas's string with four of her bodies). Sky Gonggong held her Gonggong on Aldebaran–Fomalhaut.
  - The horse's PALLAS — the Moon Dec φ on BELLATRIX–RIGEL, exact 14:34:34 (6 min before the off) — the string the Sun plays at 14:42:45 in the race (Sun at the midpoint); her Pallas on both.
  - The horse's HAUMEA — the Moon Dec 1:7:8 on Algorab–Equator, exact 14:23:31 (her Haumea at the midpoint).
- **New on the body-to-body bases (L2/L3, tightest; times are when the Moon holds the chord):** horse — VESTA on Pluto–Spica UNISON 14:29:56 (0.003%); CERES on Quaoar–Alkaid UNISON 14:35:41 (0.004%); RAHU on Transpluto–Ketu 14:59:41; PLUTO on Vesta–Spica 15:08:56 (0.002%); CHIRON on Pallas–Pleiades 14:11:41 and Juno–Antares 14:10:56; Makemake on Transpluto–Rigel 14:56:56. Jockey — ERIS on Transpluto–Aldebaran 15:12:41 (0.002%); PALLAS on Haumea–Orcus 14:47:56 (natal 0.000%); MERCURY on Haumea–Regulus 14:52:56; GONGGONG on Sedna–Ketu 14:55:41; URANUS and SATURN on Transpluto–Sedna 15:04:26; TRANSPLUTO and CHIRON on Eris–Aldebaran 15:08:41; SATURN on Jupiter–Algorab 14:23:11 (natal 0.000%); MARS on Sedna–Antares 14:12:56.
- Nodes layer: the Moon on Ketu–Equator / Rahu–Equator 14:29:41 — the horse's TRANSPLUTO on her node axis (her Method 1 Transpluto on Rahu–Ketu 1:5:6); the Moon on Rahu–Bellatrix 14:52:26 — her Venus.
### DONCASTER — METHODS 1, 2 AND 3 PULLED TOGETHER (8 Oct, 13:56)
Written into the project race summary (claude/doncaster-1440-20220318-summary.md, "Second read, 8 Oct 2026"). Where the three methods meet: (1) the horse's SUN on Altair–Arcturus — Juno 14:35:17, Mars at the off, her Sun tightest; (2) Noonan's NEPTUNE — all four Method 1 strings struck (Sun in the race; Mercury, Sun and the Moon after the finish; Mars separating); (3) Noonan's SEDNA on Algol–Polaris — Makemake holds it, the Moon from 14:36 through the race; (4) both CHIRONS on Betelgeuse–Procyon — the Moon 14:38:22, Jupiter closing through the race.
### CONTROL — the same measures for every chart in the race (Eddie 14:00; scratchpad m3compare.py, m3json/, m3moon/)
Every sky body's star chords around the off (Method 3 dump, all holders in all ten charts) and Method 1 strong strings (natal body on a star base ≤0.02%), measured the same way for every chart.
- **Overall — no separation.** Times a chart is the tightest in the field on a sky chord: Noonan 36, O'Farrell 37, Poetria 37, Hamilton 34, Oot Ma Way 31, Fiamette 31, Davies 27, Suntory Star 25, Mulqueen 23, Olympe De Gouges 17. Method 1 strong strings played by a sky body: Hamilton 25/41, Davies 20/38, Oot Ma Way 19/34, O'Farrell 19/39, Noonan 18/35, Fiamette 18/39, Poetria 10/23, Olympe De Gouges 9/23, Mulqueen 9/29, Suntory Star 8/30. Natal bodies with nearly all their strong strings played: Noonan Transpluto 3/3; Oot Ma Way Vesta 3/3, Pallas 3/3; O'Farrell Mercury 3/4, Makemake 3/3, Pluto 3/3; Hamilton Transpluto 3/4, Haumea 3/3; Fiamette Makemake, Uranus 3/4; Davies Sun 5/6.
- **Near the race — the sky bodies (not the Moon), chords exact from off−10 to finish+10: 16 chords** [corrected 8 Oct, exactness checked – was 17; O'Farrell's Mercury Algorab–Fomalhaut item was not a real exact chord]. Tightest: **winning pair 7** (Olympe De Gouges 2 — Juno and Mars on Altair–Arcturus; Noonan 5 — Pallas on Altair–Equator, the Sun on Alkaid–Arcturus, Mercury and the Sun on Procyon–Spica, Uranus on Altair–Betelgeuse); Poetria 2, Oot Ma Way 2, Davies 2, Hamilton 1, Fiamette 1, Mulqueen 1, O'Farrell 0, Suntory Star 0. With ten charts a pair's share is 0.2; 7 of 16 is about 2.7% by chance (binomial; was 7 of 17, about 4%), but the ±10-min window was chosen after looking.
- **The Moon's star chords, same window: 28.** Tightest: winning pair 6 (horse 3, jockey 3), Poetria 6, Suntory Star 5, Fiamette 3, others 2, O'Farrell 0 — at chance.
- **The favourite pair (Oot Ma Way / O'Farrell)** near the race: Oot Ma Way's PALLAS tightest on Mercury's Algol–Procyon in the race (+1.7 min, 0.004%) and on the Moon's Arcturus–Rigel (−8.2); his SATURN tightest on the Moon's Betelgeuse–Spica in the race (+3.8, 0.001%); his SUN on the Sun's Betelgeuse–Equator (+11.9, 0.001%). [O'Farrell's PALLAS on Mercury's Algorab–Fomalhaut (−8.4) REMOVED 8 Oct – Mercury's chord there is exact only at 15:17:41.] Plus §62's discord on the favourite (the Moon √2 on Ketu–Castor from 10 s before the off, held to 14:49:22).
- Reads as: by totals nothing separates; in the 25 minutes around the race the winning pair, mostly the jockey, is tightest on more of the slow and fast bodies' chords than anyone, while the Moon spreads evenly.
### THE TRANSIT SUN IN DETAIL — the winning pair (Eddie 17:07)
- Sky Sun RA 357.861, Dec −0.929, two days before the equinox (Dec +0.39/day), Full Moon day (the Moon opposite).
- **Natal Sun → sky Sun:** Noonan's natal Sun to the sky Sun in RA = **1511/9 (167.8889), exact 14:41:56–14:43:11 — in the race**. The horse's: RA 28.16, Dec 11.41 — no number.
- **Sun–Betelgeuse Dec = 75/9 (8.3333) exact at the finish.** That distance is the base of the L4 Sun–Betelgeuse Dec chords: the Moon 5:8:13 at 14:43:41 in the race (§62, horse QUAOAR tightest 0.021%) and the Moon φ at 14:48:56, 0.000% (horse QUAOAR 1:6:7 0.021%; Noonan CERES 0.064%, ORCUS 0.124%). In RA, Saturn φ on Sun–Betelgeuse 14:34:01 — horse CERES in UNISON 0.012%.
- Timeline (Sun as the moving body, and the Sun as a base end with the Moon/other bodies):
  - 14:24:26 same-body: horse's natal ERIS – sky Eris + Sun, Dec φ 0.009%.
  - 14:28:56 the Moon on Sun–Rahu (Dec) — horse URANUS 0.129%. 14:29:11 the Moon on Sun–Altair — Noonan MERCURY 0.092%, QUAOAR.
  - 14:32:56 same-body: the horse's natal SUN – sky Sun + POLARIS, RA √2, 0.000%.
  - 14:36:41 the Moon 4:5:9 on Sun–Bellatrix (Dec base 7.277 — the Sun's own distance to Bellatrix, half of Bellatrix–Rigel) — Noonan's HAUMEA √2 0.062%.
  - 14:37:26 same-body: Noonan's natal ORCUS – sky Orcus + SUN, Dec 1:6:7, 0.002% (3 min before the off).
  - 14:39:11 the Moon on Sun–Regulus — horse NEPTUNE (loose; favourite Makemake tightest, §62).
  - 14:40:26 the Sun √2 on Vesta–Regulus — the favourite's side (§62 against).
  - 14:40:41 OFF — Chiron 1:2:3 on Sun–Venus exact (§62) — the favourite pair tuned, not the winners.
  - **14:42:41 (±40 s) Noonan's natal Sun – sky Sun RA 1511/9.**
  - **14:42:45 the Sun at the Dec MIDPOINT of BELLATRIX and RIGEL (7.277 / 7.276) — the horse's PALLAS 3:5:8 0.038%, ERIS 0.147%** (Hamilton Quaoar 0.005% tighter). The Moon played this string at 14:34:34 (φ) with her Pallas.
  - **14:42:56 the Sun Dec 2:3:5 on ALKAID–ARCTURUS — Noonan's NEPTUNE tightest in the field 0.016%**; Sun and his Neptune beyond the Arcturus end, his further out.
  - 14:44:41 the Sun RA 1:2:3 on Juno–Rigel (8 s before the finish, §62) — horse CERES UNISON 0.054% (Suntory Star's Ceres tighter).
  - 14:44:49 FINISH — the Sun's Dec distance to Betelgeuse = 75/9.
  - 14:46:11 same-body: Noonan's natal MERCURY – sky Mercury + SUN, Dec 1:4:5, 0.003% (1.4 min after the finish).
  - 14:47:56 the Moon on Sun–Antares — horse ERIS, Noonan TRANSPLUTO (loose). 14:48:56 the Moon on Sun–Betelgeuse (above).
  - **14:52:18 the Sun Dec 3:5:8 on PROCYON–SPICA — Noonan's NEPTUNE in UNISON, tightest 0.017%** (Mercury played it at 14:45:16); Sun inside the string, his Neptune beyond Spica.
  - 14:52:34 the Sun Dec 1:8:9 on Betelgeuse–Equator — the horse's natal SUN on it (SAME BODY, 0.030%; Oot Ma Way's Sun 0.001% tighter).
  - 14:54:41 the Moon on Sun–Sirius — horse QUAOAR. 15:16:25 the Sun RA 5:8:13 on Algol–Vega — horse VESTA, Noonan GONGGONG.
- Steady Sun holds through the race: Capella–Deneb Algedi (Noonan TRANSPLUTO, ORCUS); Arcturus–Betelgeuse √2 (Noonan RAHU, PALLAS; horse ERIS); Polaris–Sirius (horse SEDNA, with Venus and Ceres); Arcturus–Capella (Noonan NEPTUNE, GONGGONG). ARCTURUS in four of the Sun's Dec chords.
### CORRECTION (8 Oct evening) — exact times from the runner-record tool
The exact-time search for slow bodies stepped 1.8 minutes; refined to the second: **Mars on Altair–Arcturus is exact at 14:41:34 (53 s into the race; 0.003% at the off), not at the off; Juno at 14:34:30, not 14:35:17.** Sun exact times run 5–11 s earlier than written above (the old minute file ended before off+30 and understated the Sun's rate ~1.2%). The Moon also plays Sun–Betelgeuse four times in the window (one strike had been dropped when two chords fell on the same string). Full records: repo tedsince72/astro-harmonics, main.
