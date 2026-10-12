# Layer 4 — the field (design for Eddie to check before building; 12 Oct 2026)

Layer 4 reads Layer 3 for every runner in a race and says, for each finding, where each runner stands against the rest of the field.
No control, no score, no combined ranking. Runners stay in racecard order.

## Blind by default
Layer 4 runs without finishing positions. Results (from the race csv) are written to a separate file only when asked (--results), so a
reading can be done blind first and checked afterwards.

## What it reports
1. Shape table — for each of the 12 shapes, at two levels:
   STRICT (every item tight: close links, non-Flat strikes, no contacts, no near bands) and BROAD (everything Layer 3 found):
   which runners have it, how many times, and the field count ('only runner', 'k of n').
2. Detail of each instance, so like can be compared with like:
   tightness (the link's RA/Dec offset, the item offsets), number of different sky bodies (shapes 1 and 12, Rahu/Ketu folded),
   roots_behind (how many independent facts it rests on), whether it touches a hub / strong hub, tight vs near items.
   For each shape, the field's tightest instance is named, so 'the winner's is the tightest' can be read straight off.
3. Field-only findings per runner — every shape (by level) where that runner is the only one in the field, and every shape it shares
   with only one other runner.
4. Hubs across the field — each runner's strong hubs; for each strong-hub body, which other runners have the same body as a strong hub.
5. Same pair / same body across the field — when the same cross link (e.g. horse Venus – jockey Uranus) or the same same-body set
   occurs in several runners, they are listed together with their tightness.
6. Recurring annotations — which runners carry each recurring pair / cross link (Neptune–node, Chiron–Transpluto, Venus–Uranus, ...).
7. Tight and near kept apart everywhere; a finding resting only on near items is labelled so.

## Output
docs/classic/<race>/layer4/field.json and field.txt (blind); field_results.txt only with --results.

## Tests (all from the hand reads, before Layer 5)
- Perth and Nottingham 15:30: winner the only runner with a strict cross link struck on both ends by 2+ sky bodies.
- Wolverhampton 2023: winner the only runner with both ends of a cross link moved (strict).
- Sandown 2024: winner the only runner with a swap. Fontwell 2023: winner has two swaps, no other runner more than one.
- Venturous and Wholestone: the only runners with a shared node.
- York 16:15: the Venus–Uranus cross link with the pair together in the sky — winner plus True Promise (looser), with the winner's the
  tighter; both ends moved and the sky pair together only in the winner.
- Then (as with Layer 1) each winner read's field claims ('only runner', 'k of n') turned into checks by race, with any differences
  explained (e.g. Ascot's triangle: the hand read used RA number links only; Layer 3 uses all planes — to be looked at, not forced).
