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

## 9. Questions for Eddie (before building)
- **A. Triangle (8):** which planes for the three pairwise whole-number links? The Ascot hand read used RA only; Layer 3 uses all planes, and
  that is how Rohaan (Dec) came in. Proposal: all planes, with the plane of each side printed.
- **B. In-chart pair (9, 10):** the pair is close OR at a whole/ninth (the checklist has both, e.g. Haydock 14:05 Venus–Pluto conj RA 0.628).
  Proposal: both, labelled.
- **C. Same number in both charts (11):** count Equator and Dec links as one family (Newmarket July: horse Vesta Equator 21 = Hornby
  Venus–Pluto Dec 21). Same-ratio pairs in the same plane only? Proposal: same plane strict, other planes near.
- **D. Midpoint (20):** Golden Flame was in RA. Proposal: test RA and Dec separately, off < 0.05, span < 20.
- **E. Soak (21):** the spreads seen are 0.0015 (Catterick), 0.013 (Ffos Las) and 0.041 (Golden Flame). Proposal: width 0.05,
  4+ non-star partners, at least one sky value among them, value >= 0.5; spread is t. At that width chance soaks will be common, so field
  rarity matters most here. The width could be narrowed after the checks.
- **F. Node loop (33):** what is the shape? (Sedgefield: Ketu and Sun and Mercury all within a few tenths, horse to jockey.) Proposal: leave
  out until defined.
