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
