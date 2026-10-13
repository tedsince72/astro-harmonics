# Families correction (Eddie, 13 Oct 2026)

**Correction.** The ninths are NOT n/9. They are exactly the 48 `_NINTH_RANGES` in `rebuild_kit/active_vibrations.py` (lower <= v < upper,
own tol, linear score). The full family definitions are in CLAUDE.md ("Families") and `tools/families.py` (imports Eddie's scores).
`tools/jupiter_tables.py` uses families.py from commit 65e9d6c. **The frozen readers are NOT changed** (layers v2, CR v1.1, JR v1, JR v3,
watch line); new versions only on Eddie's go-ahead.

Audit: read-only, by an independent subagent, 13 Oct 2026. Scripts: `tools/scans/families_audit/` (they write to a scratch folder;
paths inside them). Full lists: `docs/classic/families_audit/` (jr3_non48_single_SIP.txt, jr1_non48.txt, wc_ninths.txt, ranges.txt).
No csv, result, field_results, scored or profile file was opened. Who won was not evaluated.

## Notes on the definition itself (for Eddie)
- `score_sqrt2` / `score_silver` in active_vibrations.py score every multiple (tol 0.02828 / 0.04828) and have only 10√2, 100√2, 10·silver as
  fixed targets — not Eddie's lists. families.py therefore scores √2 / silver from Eddie's lists itself (tol max(0.5 %, 0.025), squared as
  score_phi_powers). Likewise `CONJUNCTION_TOL` there is RA 1.0 / Dec 0.125; families.py uses RA 1.5 / Dec 0.3 with the same squared formula.
  Imported unchanged: score_whole, score_phi_interval, score_phi_powers, score_ninth.
- Colour bands in degrees: whole green (>= 80) = |dev| <= 0.0021, yellow (>= 50) = |dev| <= 0.0059. Ninths: green = |dev| <= 0.2 x the
  range tol (1.111 ±0.0012, 11.11 ±0.012, 111.1 ±0.12, 133.3 ±0.17).
- Upper bounds sit close to the target: 8/9 range is 0.8875 <= v < 0.889 (0.8894 scores 0); 6/9 range 0.6655 <= v < 0.667.
- Overlaps: 0.9985–1.0 with whole 1; 9.985–10 with 10; 99.85–100 with 100; 110.5–112 with whole 111; 121.5–123 with 122 and φ^10 = 122.99.
- Every frozen reader has a minimum value 0.5, so the 1/9–4/9 ranges could never be reached there.

## Task A — what would change in each frozen reader
**Layers 1–5 (v2, 4baefa1).** Layer 1 (tools/layer1_inventory.py l.32–46, 59–67): whole ±0.005 (links/strikes/sky numbers), movement ±0.01,
Equator ±0.01, no upper limit; ninth n/9 any n, ±0.0005 / movement ±0.0011 / Equator ±0.0011; no golden, φ, √2, silver, scaling; contact
cross link RA < 1.5 or Dec < 0.3 (near RA < 2, Dec < 0.6), inside one chart RA < 1.5 or Dec < 0.6; ratio % bands (sky/natal 0.005/0.01,
h:j and pair family 0.005/0.02, Equator 0.01/0.05, same-body set 0.15, pair set 0.05, shared pair 0.5); MIN_V 0.5. Layer 2 (l.19–23) adds
chains in ninths (FULL = 3240): with 48 non-uniform ranges a chain total is generally not a target, so Rule 1 (derived / loop mismatch) needs a
redesign. Layers 3–5 inherit Layer 1. Changes: whole → ±0.02, 1–200; ninth → 48 ranges; add golden interval, φ powers, √2/silver, scaling,
RA–Dec crossing; inside-chart Dec 0.6 → 0.3; bands → scores; Layer 2 chain arithmetic.

**CR v1.1 (3d62207).** Imports WHOLE, NINTH, MOVE_*, EQ_* from layer1_inventory (l.15) and reads layer1/2 JSON — inherits all the above. Own:
t = |off| / tol (l.51–52) behind every ordering; item 8 "ninth sides" (l.432); near_num prints the nearest n/9 (l.466–468); item 27 return
RA < 0.3 and Dec < 1.2 (l.170); item 17 (ratio rule) unaffected. Changes: as layers, plus t and strict/near re-based on scores.

**JR v1 (f96f93d).** jcore.py l.12 / measures.py l.25: pair ±0.005 / ±0.0005, movement and Equator ±0.01 / ±0.0011; tag() whole then n/9
(no upper limit); MIN_VALUE 0.5; contact as layers (inside-chart Dec 0.6); stars on = RA < 1.5 and Dec < 0.3; ratio % bands as layers;
item 25 adds Equator labels. Changes: as layers; tags → scores.

**JR v3 (1e18081).** core.py: golden list incl. 0.382 / 3.82 / 38.20 (1/φ², to drop), lacks φ^10 = 122.99; no golden interval; √2 and silver
lists already as Eddie's; absolute tolerances (distance whole/const 0.005/0.02, ninth 0.0005/0.002; movement and Equator 0.01/0.03,
0.0011/0.004), not max(0.5 %, 0.025); targets() whole 1–180 (→ 1–200), ninth n/9 n <= 1620 (→ 48); ratio targets = p/q plus every
constant > 1 as a ratio (Eddie's definition does not say whether constants stay ratio targets); levels strict / exact-in-race /
exact-pre-off / near (would need a score-over-time equivalent); chains same-plane only, no RA–Dec crossing, no scaling.

**Watch line (tools/scans/watch_jupiter.py, fixed 12 Oct).** M = movement onto whole ±0.01 / n/9 ±0.0011 changes (ninths → 48, whole
tolerance wider); E (Equator ratio 0.01 %), B (same-body set 0.15 %), X (close cross link) unchanged. A change = a new watch line.

## Task B — past findings relying on an n/9 that is not one of the 48
(The 48 in n/9 terms: 1–9, 10–90, 100–900, 1000, 11–17, 110–170, 1100–1600. Ratios with q = 9 are ratios, unaffected, skipped.
Only ninths written as "n/9" were found; a ninth cited only as a decimal would be missed.)

### B1. docs/classic/winner_checklist.md (L = line)
- Item 1: L21 Chelmsford AW 13:20 2024 Sullivan Bay — sky Ceres Dec 26 | 231/9 (sky Chiron 30/9 is in the 48).
- Item 2: L27 Huntingdon 13:52 First Flow — sky Juno Dec 64/9 | 32; L28 Catterick 15:05 Brian Boranha — J Sun RA 48.33347 (435/9);
  L29 Lingfield 15:00 2022 Two For Gold — sky Orcus Dec 276/9, sky Saturn Dec 323/9; L30 Haydock 17:18 Aldhaja — sky Venus RA 671/9;
  L33 York 16:15 Diligent Resdev — sky Pluto Dec 62/9.
- Item 3: L38 Newmarket July 17:45 Anniversary — sky Neptune – Hornby Saturn Dec 25/9; **L39 / L420 Redcar 15:15 (blind) Present Moment —
  sky Jupiter -> H Ceres GC 71.11139 (640/9), the only partner strike in the field, called before the result**; L41 Haydock 17:18 RA 671/9.
- Item 5: **L50 / L386–387 Wolverhampton AW 17:25 Ziggy's Dream** — O'Neill Jupiter moved GC 13.5560 (122/9); the other end H Eris moved RA
  0.8894 (8/9) is outside the 8/9 range (upper 0.889) → scores 0; **L53 / L416 Exeter 15:15 (blind) Forget You Not** — node moved RA
  129.2226 (1163/9; mirror 457/9).
- Item 6: L59 Newcastle AW 16:40 Sir Chauvelin — Mulrennan Juno moved Dec 3.6672 (33/9); L60 Haydock 14:05 Wholestone — horse Haumea moved
  Dec 3.6674 (33/9); L61 Lingfield — Bass Saturn moved RA 48.3337 (435/9); L65 Newmarket 15:35 Eydon — Egan Haumea moved Dec 5.8896 (53/9),
  field Dawn Of Liberation 4.5548 (41/9); L67 Chelmsford — Kelly Neptune moved Dec 18.5565 (167/9), horse Pluto moved GC 5.6675 (51/9);
  L69 Fontwell 15:30 2023 Kilcummin — horse Vesta 6.3343 (57/9), Noonan Gonggong 7.6665 (69/9), Noonan Neptune GC 62.6674 (564/9);
  L72 Perth 16:10 — Bowen Neptune GC 56.4454 (508/9); L76 Newmarket July — horse Sedna GC 26/9.
- Item 8: L89 Newton Abbot 15:25 — sky Rahu Dec 93/9, 143/9, 239/9 (all three sides).
- Item 9: L96 Carlisle 16:30 Whitefeathersfall — horse Sun–Uranus RA 8.333 (75/9) by sky Vesta (527/9 | 452/9); Norton Pallas–Eris by sky
  Rahu (644/9 | 250/9); L98 Haydock 14:05 — sky Saturn RA 784/9; L99 Huntingdon — sky Juno Dec 133/9 | 79/9; L100 Lingfield — sky Mercury
  Dec 278/9 | RA 1450/9, sky Saturn RA 435/9 | 7; L103 Newton Abbot — sky Gonggong RA 420/9 | 523/9; L104 Nottingham 15:30 — sky Juno
  Dec 35/9 | 8, sky Makemake RA 467/9 | 1204/9; L105 Nottingham 17:50 — sky Rahu Dec 362/9 | 68/9, 362/9 | 2, 68/9 | 142/9 (extra strikes);
  L106 Sandown 14:25 Greaneteen — Frost Sun Dec 8.2218 (74/9); L110 York 15:45 — sky Pluto Dec 131/9.
- Item 11: L126 Sedgefield — 69/9 twice (horse Sedna |Dec| 7.66622, horse Saturn moved Dec 7.6668). ("Newcastle AW 12:20 horse 47/9 twice"
  is given with % errors, p = 47 — looks like a ratio; ambiguous.)
- Item 25: L281 Equator values — Haydock 14:05 horse Chiron 4.8888 (44/9); Sedgefield horse Pluto 21.22188 (191/9), Nichol Rahu 19.77741
  (178/9); Chelmsford sky Mercury 22.66629 (204/9).
- Item 28: L312 Newcastle AW 12:20 — sky Gonggong -> Mulrennan Uranus Dec 9.22193 (83/9); L313 Nottingham 15:30 — sky Jupiter -> Dawson
  Vesta Dec 137/9; L314 Perth — sky Juno -> Bowen Haumea RA 1219/9.
- Item 29: L319 Sandown 14:25 — Frost Mars–Sun Dec 10.2219 (92/9); L321 Wincanton — Johns Pallas–Rahu RA 380/9; L322 Perth — horse
  Pallas–Uranus RA 951/9 and Dec 112/9.
- Item 31 (hubs): L345 Fontwell 15:30 moved 69/9; L349 Chelmsford 167/9; **L350 / L416 Exeter (blind) Best Jupiter moved GC 171.6676
  (1545/9)**; L352 Catterick — sky Makemake -> H Pallas 980/9, J Sun 435/9, J Ketu 42/9.
- Item 33: **L366 / L424 Haydock 14:20 (blind) — Fanning node moved RA 88.666 (798/9).**
- Item 35: **L388 / L441 Fontwell 16:45 (blind) Pixie Loc — sky Venus RA 174.11130 (1567/9)**, the second end of the both-ends strike.
- Section 4: **L437 Fontwell 16:45 — Spike Jones item 28, sky Ketu -> J Mercury RA 229/9 + Dec 4** (a field-only strict item said before the result).

In the 48 and kept (new score): L71 Haydock 17:18 Crowley Eris 12.2231 (110/9) 98.8; L72 Perth horse Makemake 3.3323 (30/9) 87.6;
L74 Nottingham 17:50 horse Eris 1.3332 (12/9) 98.4; L208 Dettori 11.11006 (100/9) 98.3; L220 Ffos Las soak 8.8894 (80/9) 96.3;
L21/L98 Dec 30/9 and L108 Wincanton 10/9 (no value given); L320 Fontwell 15:30 RA 0.667 (6/9) at the exclusive upper bound — needs the exact
value; L363 Newcastle AW 12:20 Ketu–Gonggong Dec 0.1107 (1/9) 32.7 (below the readers' 0.5 minimum).
Already marked "not a ninth" / withdrawn (not counted): L218 88/9 and 183/9; L219 165/9; L221 129/9.

### B2. JR v3 outputs (docs/classic/*/jupiter/P##.json, 20 races) — total (in the 48 / not)
| | strict | exact-in-race | exact-pre-off | near |
|---|---|---|---|---|
| single hits, all 20 races | 992 (49/943) | 187 (7/180) | 233 (10/223) | 2717 (151/2566) |
| single hits, 13 blind races of 12 Oct | 720 (33/687) | 106 (7/99) | 149 (6/143) | 1976 (114/1862) |
| parts in combined hits, all 20 | 1801 (110/1691) | 532 (22/510) | 640 (37/603) | 1403 (117/1286) |
| parts in combined hits, 13 blind | 1328 (85/1243) | 250 (22/228) | 386 (18/368) | 1007 (77/930) |
| chain root numbers, all 20 | 41 (6/35) | 53 (1/52) | 56 (5/51) | 54 (6/48) |
| chain root numbers, 13 blind | 28 (5/23) | 30 (1/29) | 34 (3/31) | 39 (3/36) |

Parts are counted once per combined hit (786 unique non-48 parts at strict/exact). 60 of the 1346 non-48 single strict/exact hits still fall
inside one of the 48 ranges under the new score (33 score >= 50, 14 >= 80; e.g. 111.22262 → 111.111, 81.8).
Per blind race, single hits strict / exact-in-race / exact-pre-off, total (in/not): Kempton 17:15 79 (4/75), 2 (0/2), 10 (0/10);
Kempton 19:15 39 (1/38), 10 (0/10), 15 (0/15); Musselburgh 14:17 30 (0/30), 4 (0/4), 7 (0/7); Musselburgh 15:47 61 (4/57), 6 (0/6), 9 (1/8);
Musselburgh 16:50 71 (5/66), 11 (2/9), 14 (2/12); Newcastle 16:28 83 (3/80), 6 (0/6), 15 (0/15); Newcastle 18:00 58 (1/57), 1 (0/1), 15 (1/14);
Worcester 15:07 25 (3/22), 10 (1/9), 11 (1/10); Worcester 15:37 54 (1/53), 14 (1/13), 12 (0/12); Worcester 16:07 50 (3/47), 13 (2/11), 6 (0/6);
Worcester 16:37 59 (1/58), 22 (1/21), 9 (0/9); Yarmouth 13:54 51 (3/48), 2 (0/2), 14 (1/13); Yarmouth 15:54 60 (4/56), 5 (0/5), 12 (0/12).
Every line: docs/classic/families_audit/jr3_non48_single_SIP.txt.

### B3. JR v1 outputs (docs/jupiter/*/layer3/P##.json, 25 races)
761 items cite a ninth: 23 only the 48, 738 at least one non-48 ninth (tags 50 in / 944 out). 13 blind races: 407 items, 11 all-48,
396 non-48. Non-48 by item: stars 317, m2 156, m19 122, m9 63, m6 44, m10 13, m3 12, m28 3, m25 2, m29 2, m5 2, m33 1, m1 1.
m6 Jupiter moved (16): Exeter 15:15 P11 1545/9; Goodwood 18:53 P01 897/9; Kempton 14:40 P07 285/9; Kempton 19:15 P11 89/9; Musselburgh 15:47
P07 1220/9; Musselburgh 16:50 P07 1577/9; Newcastle 16:28 P13 260/9; Nottingham 15:30 P03 985/9, P05 841/9; Redcar 15:15 P07 619/9;
Wolverhampton 17:25 P05 122/9; Worcester 15:37 P09 334/9; Worcester 16:07 P01 1362/9; Yarmouth 13:54 P01 31/9 and 1516/9; York 15:45 P09 896/9.
Every line: docs/classic/families_audit/jr1_non48.txt.

### B4. CR v1.1 text outputs and the watch line
P##.txt lines citing a ninth: 9216, of which 8585 cite a non-48 ninth (13 blind races: 2385 / 2235); field.txt 428 / 404 (rough: display lines
repeat). **Watch line M:** 11 of 11 ninth M entries are outside the 48; in 9 races the runner holds the watch line only through that ninth M:
Goodwood 18:53 P01 J Flat 99.66562 (897/9); Kempton 14:40 P07 H Dec 31.66616 (285/9); Musselburgh 13:45 P01 H GC 159.55475 (1436/9);
Musselburgh 15:47 P07 H GC 135.55457 (1220/9); Musselburgh 16:50 P07 H GC 175.22327 (1577/9); Newcastle 16:28 P13 J RA 28.88917 (260/9);
Worcester 15:37 P09 J RA 37.11015 (334/9); Worcester 16:07 P01 H GC 151.33306 (1362/9); Yarmouth 13:54 P01 H Dec 3.44393 (31/9) and
J GC 168.44350 (1516/9). (Kempton 19:15 P11 89/9: M held by 4 of 6, not rare.)

### Not checked
JR v3 _full.txt / field.txt text (JSON used); CR P##.json; layer 1–3 outputs; whether a dropped ninth would return under scaling or another family.
