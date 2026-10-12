# Layer 1 — inventory (tools/layer1_inventory.py)

Lists everything, judges nothing (see how_it_works.md). Run: `python3.12 tools/layer1_inventory.py reference/classic/<race>`
→ `docs/classic/<race>/layer1/P*.json|txt, sky.json|txt`. Reproduction test: `python3.12 tests/layer1_reproduce.py <race>`.

Rules (v1, 12 Oct 2026): whole ±0.005, ninth ±0.0005 (links, strikes, sky numbers); movement ±0.01 / ±0.0011; Equator values ±0.01 / ±0.0011;
sky/natal ratios p <= 30, q <= 9, not 1, <= 0.005%; same-body <= 0.15% all three simple (RA, Dec, Flat, GC, and EqValue); shared pairs <= 0.5%;
Equator ratios <= 0.01%; values < 0.5 skipped; cross link close = RA < 1.5 or Dec < 0.3, inside a chart RA < 1.5 or Dec < 0.6.
Planes: RA, Dec, Flat, GC (+ Equator). Rahu and Ketu both listed (duplicates by symmetry; Layer 2 folds). No stars, no Moon.

## Checks
- Newmarket July 17:45 (16 Aug 2024): 27/27 hand-read winner items reproduced. Independent checker recomputed all 9 runners — exact match in every
  section; frac() correct; RA wrap and GC fine. Older-tool items not in Layer 1 are rule differences only: values < 0.5 (sky Juno–Rahu Dec 3/9);
  Equator ratios between 0.01% and 0.03% (Juno H/J 17/8 0.027%, Pallas S/J 27/2 0.012%). Old equator_ratios.py missed S/H 11/4 (wrote 4/11, q > 9).
  Hardening added: load() asserts all 24 bodies present and no duplicates.

## v1.1 / v1.2 (12 Oct 2026, with Eddie)
- Equator ratios: listed up to 0.03%, each marked 'tight' (<= 0.01%) or 'near' (0.01–0.03%). Near items are kept but Layer 3 uses them
  only when they join the web; Layer 4 reports tight and near separately.
- Pair sets added (horse : jockey : sky on one pair, all simple, 1 allowed, worst <= 0.05%), as three_way_all.py. Difference: a set where all
  three are 1 is not listed here (it is a shared pair with the sky equal — see 'shared', field sky_equal_pct).
- York 16:15 (15 May 2024): 41/41 hand items accounted for. One read item, sky Sun – horse Rahu Dec 4.00502, is just outside the ±0.005 strike
  window and is not listed as a strike; its two roots (sky Sun Equator 19, horse Rahu Equator 23) are listed, and Layer 2 derives it.
  The withdrawn Quaoar Flat same-body set (63/8, p > 30) is correctly absent.
- Newmarket July 17:45: 30/30.

## v1.3 (12 Oct 2026, Eddie: Dettori Sun–Chiron, 'I always come back to this in Dettori's chart')
- pair_family: on one pair A–B, sky A – natal B and natal A – sky B against the natal pair (NN) and the sky pair (TT); simple, tight <= 0.005%,
  near <= 0.02%. About 115–150 per runner (near included).
- splits: a moved body (sky X at a whole/ninth from natal X) lying between natal X and another natal body Y (same or other chart), RA or Dec:
  span = movement + other part, with the best simple ratio of the parts and of span/other, and their errors. No ratio filter (the movement is the
  gate); 0–136 per runner. Layer 3 will judge them.
- Dettori 14:35 (Diffident): sky Sun moved Dec 20.99966 (21) from Dettori's Sun and lies between his Sun and Chiron: span 28.01379 = 21 + 7.01412,
  span/other 4 (0.152%), parts 3 (0.203%). Diffident's Sun–Chiron Dec sky 5.8285 / natal 32.0577 = 11/2 (0.0030%). Sky Sun–Chiron RA 11.11006
  (100/9 off 0.00105; the active file has 11.11058, off 0.00053 — the two files' sky positions differ slightly).
- Tests: Dettori 3/3, Newmarket July 30/30, York 16:15 41/41.
- Checker (independent, 12 Oct 2026): pair_family and splits recomputed for Dettori and all 9 Newmarket July runners — exact match; RA 'between' logic tested across the 0/360 wrap and near 180 (2 million cases, 0 disagreements); all Dettori numbers confirmed.
