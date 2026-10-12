# Checklist reader — design for Eddie to check before building (12 Oct 2026)

Goal: an accurate reader built around `winner_checklist.md`. Each checklist item is one small test, run on every runner in the race,
reported with its exact numbers, its tightness, and where it stands in the field. No score, no ranking: Eddie judges. The checklist
grows one confirmed item at a time, and each new item is one new test.

## 1. Where it sits
- Runs beside the frozen layers (v2, commit 4baefa1), not in place of them. Layers 1–5 stay as they are for the blind batch.
- Input: each runner's Layer 1 inventory (`docs/classic/<race>/layer1/P##.json`), with Layer 2 roots used to mark derived hits.
  Layer 1 already holds the positions of every body (sky, horse, jockey) plus links, strikes, ratios, movement, same-body sets,
  shared pairs, Equator ratios, pair family, h:j, splits, pair sets, contacts and node data. The reader does not re-measure
  anything Layer 1 has measured. It only combines it. The few items that need a new measurement compute it from Layer 1's positions.
- Layer 3 shapes are NOT used as input. Each test is written straight from its checklist definition, so it can be read and checked
  on its own. Where a test matches a Layer 3 shape, the two are compared as a cross-check (section 6).
- Command: `python3 tools/checklist_reader.py <race>` (blind). `--results` writes the finishing positions to a separate file, as Layer 4 does.

## 2. One test per item
Every test returns a list of instances. Each instance carries:
- **what**: one line with the bodies and the numbers copied from Layer 1 (value, whole/ninth or ratio, offset). Same style as the checklist.
- **bodies**: the natal bodies it rests on (`H Juno`, `J Chiron`; node folded for joins), plus any sky bodies.
- **level**: `strict` (the checklist definition) or `near` (the near bands the checklist already names). They are never mixed.
- **tightness t**: each part's offset divided by its own tolerance, so 0 = exact and 1 = at the edge. A compound instance takes its worst part.
  For example, a cross link struck on both ends takes the max of the link (min(RA/1.5, Dec/0.3)) and the two strike offsets / ±0.005
  (or ±0.0005 for a ninth). One scale for every item, so "tightest in the field" means the same thing everywhere. The raw numbers are
  always printed beside t.
- **derived**: yes if Layer 2 traces it to other hits (e.g. York's Dec 33 = 19 + 14). Derived instances are shown, but marked.
- **plane note**: Flat strikes and GC hits are kept, and labelled (Golden Flame's partner strike is Flat 26).

## 3. Field rarity (per item, per race)
- How many runners have it, strict and near separately: `only runner`, `k of n`, `none`.
- Each runner's tightest instance, with its rank in the field by t, and the field's tightest instance named.
- How many instances each runner has: printed, but only as background (section 3 of the checklist: counts never separated winners).
- No combined table or total across items.

## 4. Joins (relationships first)
Per runner, after the item list: every natal body and every pair (node folded) touched by two or more different items, with those items
listed together and their t. For example, Exeter's Chiron–Juno should show items 2, 13, 14, 17 and 22 on one pair. The join view
replaces items 31 (hub) and 32 (pair lit many ways). It shows the combinations, not a count of them. Each instance line also says
"joined: items ..." when another item touches the same body, so a field-only detail that stands alone looks different from one inside the web.

## 5. The items

| # | item | from Layer 1 | test (strict) | t from | notes |
|---|------|--------------|---------------|--------|-------|
| 1 | cross link struck both ends, 2+ sky bodies | links, strikes | cross link close (RA<1.5 or Dec<0.3); 2+ different sky bodies each hit both ends (Rahu/Ketu one body) | worst of link + strikes | near: link Dec to 0.6 |
| 2 | cross link struck both ends (1 body, or 1 per end) | links, strikes | as 1 with one body, or a different body on each end | same | |
| 3 | partner strike | links, strikes | on H x – J y: sky y -> H x, or sky x -> J y | link + strike | |
| 4 | cross-link pair together in the sky | links, points | same two bodies close in the sky: GC < 5, or RA < 1.5 / Dec < 0.3 | link + sky GC/5 | NEW measure (sky pair from positions) |
| 5 | both ends of a cross link moved | links, movement | both ends whole/ninth movement (±0.01 / ±0.0011) | worst | |
| 6 | movement onto a cross link | links, movement | a moved body is an end of a cross link | worst | |
| 7 | swap | links | H x ~ J y and H y ~ J x | worst of the two links | |
| 8 | triangle struck at every corner | links, strikes | 3 natal bodies pairwise at whole numbers; one sky body (Ketu included) strikes all three | worst | QUESTION A |
| 9 | in-chart pair struck both ends, 1 sky body | links, strikes | in-chart link that is close or at whole/ninth; one sky body hits both ends | worst | QUESTION B |
| 10 | in-chart pair, 2+ sky bodies | links, strikes | as 9 with 2+ bodies | worst | |
| 11 | same number / ratio in both charts | points, links, ratios | same whole/ninth in H and J (Equator and Dec links count as one family), or same sky/natal ratio in H and J ratios in the same plane | worst | QUESTION C |
| 12 | shared node | points | horse Rahu within GC 3 of jockey Rahu or Ketu | GC/3 | NEW measure |
| 13 | shared natal pair | shared | <= 0.5%, slow–slow pairs dropped | diff/0.5% | |
| 14 | shared pair also cross-linked | shared, links | 13 whose two bodies are also a cross link (either way round) | worst | open candidate 1 |
| 15 | pair set H:J:S | pair_sets | as Layer 1 (all simple, worst <= 0.05%) | worst/0.05% | |
| 16 | same-body set | same_body | as Layer 1 (p <= 30, not 1, <= 0.15%) | worst/0.15% | |
| 17 | Dec 9/4 : 5/4 : 9/5 | same_body | 16 in Dec with those three ratios | worst/0.15% | annotation, open candidate 2 |
| 18 | same-body set joined to the web | same_body, links, ratios | 16 whose body is a cross-link end or in a ratio pair | worst | |
| 19 | sky body divides a natal pair | splits | as Layer 1, parts or span/other simple within 0.25% | err/0.25% | |
| 20 | natal body at midpoint of X and sky X | points | natal Y (other chart) within 0.05 of the midpoint of natal X and sky X, span < 20 | off/0.05 | NEW measure; QUESTION D |
| 21 | soak | points | one body (any chart) at the same separation to 4+ non-star partners across H, J, S | spread/width | NEW measure; QUESTION E |
| 22 | sky/natal ratio of a pair | ratios | as Layer 1 (tight <= 0.005%, near <= 0.01%) | err/0.005% | present for every runner: weigh by joins |
| 23 | one body in ratios in both charts | ratios | the same body in H ratios and J ratios | worst | |
| 24 | pair family, h:j | pair_family, hj_ratios | as Layer 1 (tight <= 0.005%; h:j near <= 0.02%) | err/tol | |
| 25 | Equator whole/ninth + chains | points, Layer 2 | \|Dec\| whole/ninth (±0.01 / ±0.0011); Dec strikes made from two of them shown as derived chains | off/tol | |
| 26 | Equator ratios | eq_ratios | as Layer 1 (tight <= 0.01%, near <= 0.05%) | err/tol | |
| 27 | return / contact | contacts | as Layer 1 (return: RA < 0.3 and Dec < 1.2) | RA/1.5 or Dec/0.3 | |
| 28 | one sky body on one natal body in RA and Dec | strikes | same sky -> same target, whole/ninth in RA and in Dec | worst | |
| 29 | in-chart pair whole/ninth in RA and Dec | links | one in-chart link numbered in both RA and Dec | worst | |
| 30 | tightest cross link in the field | links | each runner's tightest close cross link (non-star), ranked across the field | link t | field-relative by nature |
| 31, 32 | hub, pair lit many ways | — | given by the join view (section 4), not as separate tests | | |
| 33 | node loop | — | not built until defined | | QUESTION F |
| 34, 35 | recurring pairs / cross links | — | lookup list from the checklist, printed as notes, never weighed | | |
| 36 | same rider winning again | — | across races; out of scope for a one-race reader | | |

Stars excluded everywhere. No Moon. Natal charts at 12:00.

## 6. Tests before it is used (the checklist is the test)
- `tests/checklist_check.py`: every numbered example in the checklist becomes a check. The winner's instance is found, with the same bodies
  and numbers (to Layer 1's printed precision), in every race folder named. 29 hand reads + Dettori, all with Layer 1 output already in the repo.
- Field claims become checks: "ONLY runner", "NOT unique — k", "tightest", race by race. Any difference is explained in the test file,
  not forced (as with Layer 1: Ascot's triangle RA-only vs all planes).
- WITHDRAWN claims become negative checks. They must NOT appear: York 16:15 Quaoar Flat set (p > 30), the Newcastle AW 13:30 Mercury–Orcus
  set, the soaks at Newcastle 15:40, York 15:45 and Newcastle AW 12:20.
- Cross-check: where an item has the same definition as a Layer 3 shape (1, 2, 3, 5, 6, 7, 12), the strict counts should agree. Disagreements are listed for Eddie.
- Runs twice give identical output (sorted everywhere; no set order — see the Layer 3 fix of 12 Oct).
- Independent checker (subagent) on the first full race output.

## 7. Output
`docs/classic/<race>/checklist/`
- `field.txt`: one block per item: who has it (strict | near), the tightest, the field count; then field-only items per runner.
- `P##.txt`: per runner, every item with its instances (tightest first, with t and "joined: ..."), then the join view.
- `field.json`, `P##.json`: the same, for checking.
- `field_results.txt`: only with `--results`.

## 8. Build order (one step at a time, each tested before the next)
1. Frame + items read straight from Layer 1: 13, 15, 16, 17, 19, 22, 24, 26, 27, plus field rarity and output.
2. Items combining Layer 1 parts: 1, 2, 3, 5, 6, 7, 9, 10, 14, 18, 23, 28, 29, 30, 25 (with Layer 2 chains), 11.
3. New measures from positions: 4, 12, 8, 20, 21.
4. Join view. Then the full check on all 30 folders, the checker, freeze, and continue the blind batch with Kempton 14:40.

## 9. Eddie's answers (12 Oct 2026) — built to these
- **A. Triangle (8):** all planes; each side's plane printed; each triangle labelled "one plane" or "mixed planes".
- **B. In-chart pair (9, 10):** close pairs and whole/ninth pairs both count, labelled.
- **C. Same number (11):** Equator values and Dec links are one number family. A matching ratio must be in the same plane;
  cross-plane matches listed separately as "other plane".
- **D. Midpoint (20):** RA and Dec separately, within 0.05 of the midpoint, span under 20; span and offset printed. Spans 20–60 in a
  separate "wide" list (Tynwald 21.7).
- **E. Soak (21):** width ±0.02 around the cluster centre (total spread <= 0.04), 4+ non-star partners, at least one sky value, partners
  from BOTH horse and jockey charts. Centre, spread and nearest whole/ninth printed. Field rarity decides, not the count.
- **F. Node loop (33):** Sedgefield 15:00 — a closed loop of close links (inside a chart and across) through the horse node AND the
  jockey node. Built as cycles of close links of length <= 6 including a node in each chart; the loop printed. Built last.

## 10. As built — CR v1 (12 Oct 2026; tools/checklist_reader.py, tests/checklist_check.py 415/415)
Built in the four steps, each tested before the next; independent checker run on the whole; its corrections applied and given their own checks.
Builder's choices beyond the answers (all labelled in the output; for Eddie to keep or change):
- Item 4: strict = the two bodies within GC 5 in the sky; pairs close only in RA or Dec (often 100°+ apart) go to near.
- Item 7: swap on exact bodies; a swap needing Rahu one way and Ketu the other is 'other' (needed for Sandown 2024 'ONLY swap').
- Item 13: slow–slow shared pairs (age) listed as 'other', not dropped (Fontwell Gonggong–Orcus, Sedgefield Haumea–Makemake, York Eris–Haumea).
- Item 16: Equator-value sets containing a 1 are 'other' (item 16 says not 1).
- Item 20: same-chart midpoints are 'other' (checklist: the natal body is in the other chart); span 20–60 'wide' in any chart (Tynwald).
- Item 21: the tightest core sets t; the cluster is then widened (spread <= 0.04) to show every partner. 'near' when the partners are not from both
  natal charts but the values touch both (Catterick Chiron ~18.3438 — otherwise lost). Ffos Las Juno ~8.889 (no horse chart) does not pass.
- Item 27: returns of slow bodies (Uranus outward) listed as 'other'.
- Item 33: no Sedgefield loop exists in close links alone; 'near' loops may close through the same body in both charts (H X = J X, <= 2 steps),
  which is how Eddie's example closes (J Mercury = H Mercury, J Ketu = H Ketu).
- Join view: items 14, 18, 30 left out (they are joins or field-relative); a body's same-body sets (16, 17) count on its pairs.
Checker corrections (12 Oct): item 11 lost node-mirror RA numbers (Sandown 2021 number 118); item 20 same-chart strict; item 21 hid tighter clusters;
item 16 Equator-value '1' sets and their display; item 3 one strike per plane (now one per direction). t is computed from Layer 1 offsets rounded to
5 decimals, so for ninths it moves in steps of about 0.02.
Rates across the 32 read races (winners vs other runners, strict) — docs/classic/checklist_rates.txt.

## 11. Eddie's decisions on the as-built reader (12 Oct 2026) — CR v1.1, frozen for the blind batch
1. The builder's choices in section 10 (items 4, 7, 13, 21, join view): kept.
2. Join view is field-relative: an item counts only when fewer than half the field has it at strict level; the others are shown beside it as
   "also (common in this field)". Every item is still listed with its numbers. (Built: a pair or body is listed when it has a counted item and
   at least one other item, counted first.)
3. Watch line at the top of each race page: runners with items 17, 14, 15 — "from the read races — not evidence yet". Not weighted.
4. Triangles: ninth sides accepted and labelled ("ninth", "[n ninth sides]" / "[all whole]").
5. Node loops: counted only with 4+ distinct bodies (node folded, by name) and at least one cross link between different bodies; the rest near.
