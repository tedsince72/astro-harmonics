# Transit-Jupiter reader — design (agreed with Eddie, 13 Oct 2026)

Status: go-ahead 13 Oct 2026 (Eddie), built as JR v2 (`tools/jup2/` + `tools/jupiter_reader.py`). JR v1 (`tools/jup/`, f96f93d) unchanged.
Decisions of 13 Oct added below: Equator-ratio near band 0.06 %; levels strict / exact-in-race / exact-pre-off / near (5G);
lines show level, offset and tightness t, sorted by t; field counts per level (section 6). As built: section 10.
Script (when built): `tools/jupiter_reader.py <race>` -> `docs/classic/<race>/jupiter/`.
Separate from the frozen layers and the frozen checklist reader (CR v1.1) — those are not changed.

Purpose: read every runner from the perspective of **sky (transit) Jupiter at the off**, and of the horse's and jockey's
natal Jupiter, relationship by relationship. No scores, no totals. Each hit carries its numbers, tightness, number family,
applying / separating, and how many runners in the field hold the same hit.

## 1. Points

- Sky (TRANS): all bodies at the off, **sky Moon included**; the 22 stars (`*_B` rows); the **equator** (Dec 0, Dec plane only).
- Horse (P01) and jockey (P02): natal at 12:00 standard time, **no natal Moon**; the 22 stars; the equator.
- Excluded everywhere: Ascendant, Midheaven, Vertex, Part of Fortune, Part of Spirit.
- Rahu/Ketu: one node. In RA they are always 180 apart, so only one is measured in RA (no duplicate hits); both kept in Dec.
- Each chart uses its own star positions (workbook values as they stand, same frame as that chart's planets).
- Royal stars: Aldebaran, Regulus, Antares, Fomalhaut.

## 2. Planes

- RA: |dRA| wrapped 0–180.
- Dec: |dDec|.
- Flat: sqrt(RA² + Dec²) (kept for now — Flat and GC differ by degrees at larger separations / higher Dec, so they give different hits).
- GC: true great-circle distance.
- Equator: |Dec| of one point (its distance from the equator).

## 3. Number families (each hit labelled with its family)

1. Whole numbers 1–180.
2. Ninths n/9 (not whole).
3. Simple ratios p/q: q <= 9, p <= 30, not 1 (ratios only).
4. Golden (φ = 1.618034), in x1 / x10 / x100 forms up to 180 — no other multiples:
   0.382, 3.82, 38.20 (1/φ²) · 0.618, 6.18, 61.80 (1/φ) · 1.618, 16.18, 161.80 (φ) · 2.618, 26.18 (φ²) · 4.236, 42.36 (φ³) ·
   6.854, 68.54 (φ⁴) · 11.09, 110.90 (φ⁵) · 17.94, 179.40 (φ⁶) · 29.03 (φ⁷) · 46.98 (φ⁸) · 76.01 (φ⁹).
5. √2 (the number only, no n√2 multiples): 1.414, 14.14, 141.4; 0.707, 7.07, 70.7 (1/√2).
6. Silver (1 + √2): 2.414, 24.14; 0.414, 4.14, 41.4 (its inverse).

Exact constants are used in the code (e.g. 10φ = 16.18034), not the rounded labels above.
No decimal scaling of whole numbers, ninths or simple ratios.

## 4. Tolerances

| What | Strict | Near (full file only) |
|---|---|---|
| Distances (RA, Dec, Flat, GC): whole, constants | ±0.005 | ±0.02 |
| Distances: ninth | ±0.0005 | ±0.002 |
| Movement (sky X vs natal X): whole, constants / ninth | ±0.01 / ±0.0011 | ±0.03 / ±0.004 |
| Equator values: whole, constants / ninth | ±0.01 / ±0.0011 | ±0.03 / ±0.004 |
| Ratios (all families) | 0.005 % | 0.02 % |
| Equator ratios (all families) | 0.01 % | 0.06 % (13 Oct; was 0.05 %) |
| Close contact | RA < 1.5 or Dec < 0.3 | RA < 2 or Dec < 0.6 |
| Midpoint | within 0.05° | within 0.15° |

Overlaps: a value that is whole is labelled whole only (18/9 = 2 is "2"). A value matching two families lists both.

## 5. The measures

### A. Transit to transit — the race's own sky (same for every runner; printed once on the race page)
- A1. Sky Jupiter to every other sky body, every star, and the equator (Dec plane): raw distances, all planes, all families.
- A2. Apex ratios with sky Jupiter at the apex, ONLY:
  - (sky Jupiter–X) / (sky Jupiter–equator) in Dec, X = any sky body or royal star;
  - (sky Jupiter–royal A) / (sky Jupiter–royal B), all planes.
- Shown under a runner only when that runner joins it (same value or same pair in its natal charts, see D1).

### B. Natal to natal (horse chart, jockey chart, and across)
- B1. Horse Jupiter and jockey Jupiter to every body in their own chart, every star, the equator: raw distances.
- B2. Apex ratios, ONLY: (natal Jupiter–X) / (natal Jupiter–equator) in Dec; (natal Jupiter–royal A) / (natal Jupiter–royal B);
  (natal Jupiter–X) / (natal Jupiter–other chart's Jupiter).
- B3. Cross: horse Jupiter to jockey bodies, jockey Jupiter to horse bodies (contacts and numbers).
- **Printed only when joined by the sky** (cut 4): the same pair has a D1 hit, or a sky body strikes either end (C1/C2).
  Unjoined natal hits go to the full file only.

### C. Transit to natal (per runner)
- C1. Sky Jupiter to each natal body (horse and jockey), all planes, all families; and sky Jupiter striking BOTH ends of a natal pair
  (inside one chart, or an H–J cross link).
- C2. Each sky body (Moon included) to natal Jupiter (horse, jockey), all planes; and pairs of sky bodies striking natal Jupiter
  (two sky bodies each on a number to the same natal Jupiter).
- C3. Movement: sky Jupiter vs horse Jupiter, sky Jupiter vs jockey Jupiter, all planes + Equator.
- C4. RA and Dec together: a sky body on a natal body in RA AND Dec at once (both whole/ninth/constant), where either is a Jupiter.
- C5. Partner strike: sky Jupiter on a natal body that is cross-linked (close contact) to the other chart's Jupiter (Redcar shape).

### D. Ratios of the same relationship (same pair, same plane)
- D1. (sky Jupiter–sky X) / (natal Jupiter–natal X), for horse and jockey.
- D2. (sky Jupiter–natal X) / (natal Jupiter–natal X), for horse and jockey.
- D3. Equator ratios: sky : horse : jockey Jupiter |Dec| (S/H, S/J, H/J), plus the golden-section check: a Jupiter's |Dec| at
  φ between the equator and another Jupiter (the Doyle shape — this is the same fact as S/J = φ when they share a hemisphere; report once).

### E. Three-way midpoints (RA and Dec separately)
- E1. Sky Jupiter, horse X, jockey X (same body X): is any one of the three at the midpoint of the other two?
- E2. Sky X, horse Jupiter, jockey Jupiter: the same.
- E3. A natal body (other chart) at the midpoint of natal Jupiter and sky Jupiter (span 0.5–20°; 20–60° listed as wide).

### F. Applying / separating
- Second sky snapshot at **off + 5 minutes**, computed with the chart engine (celestial_bodies_swisseph.py, Mac ephemeris folder),
  same flags as the race workbook. Check first that the engine reproduces the workbook's TRANS at the off (to 0.0001°).
- For each hit with a sky leg: deviation at the off and at +5 min -> **applying** (moving toward exact) or **separating**, and the
  estimated time to/from exact (linear rate). Natal points don't move; tr-tr hits have both legs moving.
- If the engine can't be run, the reader still runs and marks every hit "a/s: n/a".

### G. Levels (Eddie, 13 Oct 2026)
- Every hit has one level, in this order of precedence:
  1. **strict** — inside the strict tolerance at the off;
  2. **exact-in-race** — has a sky leg, and F's rate (linear) puts the exact moment between the off and the finish
     (expected duration from the day's race_info.csv, column expected_dur_s; default 5 min when the race is not listed);
  3. **exact-pre-off** — has a sky leg, exact within the 5 minutes before the off and separating at the off;
  4. **near** — inside the near band at the off.
- Natal-only hits (no sky leg) are strict or near only. A sky-leg hit whose rate is n/a is strict or near only.
- Combined hits (both ends struck, two sky bodies on one Jupiter, RA AND Dec together) take the weaker level of their parts.

## 6. Field and report

- For every hit: how many runners in the race hold the same hit (same measure, same bodies by chart role, same number).
- Flags: `copy` = sky body to a natal star (≈ the sky pair; same for everyone); `age` = natal slow-body hit held by >= half the field.
- Files:
  - `field.txt` — race page: sky Jupiter's own relationships (A), then each runner's strict hits held by fewer than half the field.
  - `P##.txt` — runner page: the same, grouped by measure (C, D, E, then joined B), each line: measure, bodies (with chart),
    plane, value, family + target, **level, offset, tightness t (= |offset| / strict tolerance)**, a/s (+ time to/from exact),
    field count; lines **sorted by t** inside each group.
    Shown on the runner page: strict, exact-in-race and exact-pre-off always; near only when rare in the field
    (held by fewer than half the field at any level) or joined to a strict hit (another strict / exact-in-race / exact-pre-off
    hit of the same runner on the same set of points, any plane or measure).
  - Field count: each level counted separately (strict / exact-in-race / exact-pre-off / near, of n runners).
  - `P##_full.txt` / `P##.json` — everything, including near hits, common hits and unjoined natal hits.
- No scores, no totals, no ranking.

## 7. Acceptance tests (must reproduce before any race is read with it)

| Race | Expect |
|---|---|
| Lingfield 14:35, 2 Apr 2021 (Pholas / Holly Doyle; file reference/classic/race_batch_pholas.xlsx, this pair only) | D3: J/S Jupiter Equator 23.29537 / 14.38992 = 1.61887, φ at 0.0515 %, level near (0.06 % band); S Jupiter Dec −14.38992, H −7.06006, J −23.29537 |
| Fontwell 16:45 2021 (Pixie Loc / Ben Jones) | C3: J Jupiter moved RA 58.99549 (59) |
| Kempton 14:40 2021 (Hamish) | D3: Equator S/H 16/5 (0.0019 %) |
| Goodwood 18:53 2021 (Madame Tantzy / Dobie) | D3: Equator H/J 11/9 (0.0038 %) |
| Nottingham 15:30 2022 (Dynamic Force / Dawson) | C4: sky Jupiter -> J Vesta RA 18 (±0.00414), Dec 137/9 (±0.00046) |
| Redcar 15:15 2021 (Present Moment / Hogan) | C5: H Ceres – J Jupiter Dec 0.1131; sky Jupiter -> H Ceres GC 71.11139 (640/9) |

Plus an independent checker recomputing one runner's page from the raw workbook.

## 8. Not in the first version (can be added later, one at a time)
- Apex ratios to any two bodies (cut 1), natal-only hits on the main page (cut 4), ratios between non-royal stars (cut 6),
  multiples of √2 / silver / φ (n·√2 etc.), decimal scaling of whole numbers, ninths and simple ratios.
- A time window beyond off + 5 min.

## 9. How it's used
- Forward only: run on races not yet run, commit + push the race page before the off, open the result after (CLAUDE.md routine).
- Anything that looks good on old races is a candidate, fixed before the next race, tested forward.
