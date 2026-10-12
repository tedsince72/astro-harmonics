# Jupiter-centred read — tools and outputs (built 12 Oct 2026)

Read each race only from Jupiter's side: horse Jupiter (H), jockey Jupiter (J), sky Jupiter (S), what each connects to, and
how the three connect to each other and to the stars. Instructions: Eddie's "JUPITER-CENTRED READ — instructions" (12 Oct 2026),
with his answers of the same day (below). Counts are background only.

## Run
`bash tools/jup/run_all.sh <race>` (race = folder in reference/classic made by tools/split_batch.py). No results are opened.

| Layer | Script | Output (docs/jupiter/<race>/) |
|---|---|---|
| 0 positions | positions.py | positions.csv (+ positions_log.txt) |
| 1 measures | measures.py | measures/sky.csv, measures/P##.csv — every raw Jupiter pair, movement, Equator, with number/contact tags |
| 2 ratios | ratios.py | layer2/P##.json/.txt — 13, 15, 16/17, 22, 24, 26 |
| 3 shapes | shapes.py | layer3/P##.json/.txt — every measure 1–35 + stars (ST), per runner |
| 4 field | field.py | field.txt — A per measure (k of n, RARE), B rare details per runner, C tightest link, D Jupiter with itself (watch-line definition), E riders |

Shared code: tools/jup/jcore.py.

## Rules as built
- Positions: workbook values as they stand, each chart's own (stars included). Natal 12:00 standard time, no natal Moon; sky Moon is a sky body.
- Dropped: Part of Fortune, Part of Spirit, Ascendant, Midheaven, Vertex; duplicate royal-star rows without `_B`; the empty `equator` row.
- Node: Ketu folded into Rahu (mirror checked); the Ketu mirror is also checked for the shared node (12) and Jupiter on the node (33).
- Planes: RA wrapped 0–180; Dec |dDec|; Flat sqrt(RA²+Dec²) with wrapped RA; GC true distance; Equator |Dec|; movement = sky X vs the same natal X.
- Numbers: whole ±0.005, ninth ±0.0005; movement and Equator whole ±0.01, ninth ±0.0011; whole first (18/9 is "2"); values < 0.5 not tagged or ratioed.
- Ratios p/q, q ≤ 9, p ≤ 30, relative error: sky/natal 0.005% (near 0.01%); h:j and pair family 0.005% (near 0.02%); Equator ratios 0.01% (near 0.05%);
  same-body set worst ≤ 0.15% (not 1; planes RA, Dec, Flat, GC, and Equator = the three |Dec| values); pair set worst ≤ 0.05% (1 allowed); shared pair ≤ 0.5%.
- Contact: cross link close RA < 1.5 or Dec < 0.3 (near RA < 2 or Dec < 0.6); inside one chart RA < 1.5 or Dec < 0.6; on a star RA < 1.5 AND Dec < 0.3 (near 2 / 0.6).
- Midpoint (20): RA and Dec separately; span 0.5–20 (20–60 listed as wide); natal body within 0.05 of the midpoint; strict only in the other chart.
- Split (19): moved body (sky X at a whole/ninth movement from natal X in that plane) between natal X and natal Y in RA or Dec; parts or span/other simple within 0.25%.
- Sky body -> natal star nearly copies the sky pair for every runner: shown (marked "copies sky"), not the runner's own.

## Tests (12 Oct 2026)
- Reproduced from the checklist: Pixie Loc (H Eris – J Jupiter both ends moved, RA 59), Ziggy's Dream (8/9 | 122/9), Present Moment partner strike
  (S Jupiter -> H Ceres GC 640/9), Madame Tantzy Equator H/J 11/9, Hamish Equator S/H 16/5 (+ Equator same-body set), Ffos Las Scudamore
  Jupiter–Vesta Dec 5 struck by Ceres and Haumea, York 15:45 and Nottingham 17:50 Jupiter–Pluto strikes, Sandown 2024 Brace Mars–Jupiter Dec 50,
  Newton Abbot Ring Jupiter moved RA 174, Nottingham 15:30 Jupiter moved Dec 23 and S Jupiter -> Dawson Vesta RA 18 + Dec 137/9, Exeter Jupiter–Vesta pair set.
- Section D equals the frozen watch line (tools/scans/watch_jupiter.py) on Goodwood 18:53, Kempton 14:40, Fontwell 16:45.
- measures.py: 473/473 rows of Pixie Loc recomputed independently, 0 mismatches.
- Independent checker (own code) on Yarmouth 13:54 12 Oct 2026: ~240 items, 0 mismatches.

## Not covered / open
- 36 (same rider / pair again) needs past results: field.txt lists the riders only.
- 6 "movement value = the link's value" is read as the checklist defines it (an end of the link moved).
- Measure 8 triangles use whole numbers only for the sides.
