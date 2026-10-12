# Layer 3 — the web (tools/layer3_web.py), design: layer3_design.md (approved by Eddie 12 Oct 2026)

Run: `python3.12 tools/layer3_web.py <race>` (needs layer1/ and layer2/) → `docs/classic/<race>/layer3/P*.json|txt`.
Test: `python3.12 tests/layer3_check.py` — 32/32.

## What the first run showed (12 Oct 2026) and what was added
- With the full Layer 1 inventory, 3+ kinds marks about half of every runner's bodies as hubs (counts don't separate — as before).
  Kept as designed, and added STRONG HUB = 5+ tight kinds (near items not counted). The winners' named hubs are hubs; Newmarket July
  horse Uranus is strong (6 kinds).
- Loops of numbers are shapes in themselves (Ascot triangle, Brace's Mars–Jupiter Dec 50 = 14 + 36), so shapes are found on root AND
  derived items, and each shape reports 'roots_behind' (how many independent facts it rests on). Perth's Ceres -> Uranus shape rests on
  few roots: sky Ceres moved 132 onto horse Ceres, horse Ceres – Bowen Uranus RA 1, sky Ceres–Rahu 29; the Rahu/Ketu strikes are arithmetic.
- A sky body on its own natal place (= movement) counts as landing on that body for shapes.
- With the broad inventory (contacts, near bands, Flat, Ketu) several shapes the hand reads found unique to the winner appear in most
  runners. Every shape now carries 'strict' (all items tight: close links, non-Flat strikes, no contacts, no near bands); shapes 1 and 12
  carry 'strict_multi' (2+ sky bodies on both ends, Rahu/Ketu folded). At the strict level the hand-read uniqueness returns:
  Perth and Nottingham 15:30 (only strict 2+ body cross link), Wolverhampton (only strict both ends moved), Sandown 2024 (only swap).
  Layer 4 should therefore compare the field at both levels.

## Tests (all from the hand reads)
York 16:15 shapes 3, 4, 11 (Chiron, node), hubs H Venus, J Uranus; Newmarket July 1, 2, 8 (21), strong hub H Uranus, hubs H/J Chiron;
Perth 1 (2+ bodies), hub J Node; Nottingham 15:30 1 (Venus, Ceres, Juno), hub J Chiron; Wolverhampton 4; Fontwell 6 x2; Sandown 2024 6, 12
(Sun, Uranus, Eris); Ascot 7 (Ceres/Sedna/Haumea by Vesta); Nottingham 17:50 8 (34, 19/8); Venturous and Wholestone 9; Dettori 10;
Venturous 5 (Ceres); plus the four field-uniqueness results above at strict level.

## v1.2 (checker, 12 Oct 2026)
Independent checker recomputed 327 shapes (Sandown 2024, Perth) and all 230 Perth bodies' kinds: identical. Fixes applied:
- false node 'swap' (H Rahu–J Ketu with H Ketu–J Rahu, the same measurement) removed: swaps need two different bodies; Layer 2 v1.2 now
  tags such Ketu copies of cross links as mirror (0 node swaps left, was 8);
- near cross links count as X only when both ends already have a tight kind (as designed);
- shape 1 'multi' now folds Rahu/Ketu like strict_multi;
- roots_behind counts a link's close fact and its numbers as one root.
Tests: layer2_check all pass (5,078 chains exact, one tag per item); layer3_check 32/32.
