# Layer 5 — the reader (design for Eddie to check before building; 12 Oct 2026)

Layer 5 turns Layers 1–4 into a plain written reading for each runner, body by body, relationships first — the way the hand reads
are written. It is not a score and does not rank runners; runners stay in racecard order. Blind: it never sees finishing positions.
It is written by fixed rules from the data (no guessing, no free text), so every sentence points to an exact item and value.

## For each runner (in this order)
1. What only this runner has — every shape no other runner in the field has (strict first, then broad), and shapes it shares with
   just one other runner. One line each, with the exact items, e.g.
   'Only runner with a cross link struck on both ends by 2+ sky bodies: horse Ceres – Bowen Uranus (RA 0.999), sky Ceres and the node.'
2. The web, hub by hub — start from the strong hubs, then the other hubs on the same web. For each hub body: the kinds it carries,
   and the exact items behind each (cross link with offsets; sky body on it; movement; ratios; same-body set; Equator; shared pairs),
   then how it joins the next hub (the item path from Layer 3).
3. Shapes, with their detail — each shape the runner has, strict before broad, saying: the items and values, how many independent
   facts it rests on, whether it involves a hub, and where it stands in the field ('tightest in the field', '2nd tightest of 5',
   'also in P11, looser').
4. What is arithmetic — for the items in 1–3, any that Layer 2 found to be the sum of others, written out (e.g. 'sky Pluto on Hornby
   Venus Dec 38 = natal Venus–Pluto 21 + Pluto moved 17'), so the reader sees which facts are the roots.
5. Same pair elsewhere — when the runner's cross links or sets also occur in other runners, named with their tightness.
6. Recurring pairs from earlier winners (annotation only).
7. Near items that joined the web, listed separately and labelled near.
Each section is capped (most field-rare and tightest first) so a reading stays readable; the full lists remain in Layers 3–4.

## Race page
A short page per race: each runner's section-1 lines side by side (racecard order), then the field's tightest instance of each shape.
No ordering by any count.

## Output
docs/classic/<race>/layer5/P*.md (one reading per runner) and race.md.

## Tests (before use on new races)
- Blind: no finishing position or SP anywhere in layer5.
- Each test winner's reading contains its hand-read shapes and items in words: York 16:15 (horse Venus – Mason Uranus, both ends moved,
  pair together in the sky; Chiron and node same-body sets; Equator 23 and 14), Newmarket July (horse Uranus – Hornby Venus, sky Venus
  on horse Uranus GC 123, sky Pluto Dec 38 = 21 + 17, 21 in both charts, Chiron in Dec), Perth (Ceres -> Uranus, 2+ bodies), Nottingham
  15:30 (Sedna–Chiron, three bodies), Wolverhampton (both ends moved), Fontwell (two swaps), Sandown 2024 (swap; Brace Mars–Jupiter),
  Ascot (triangle by sky Vesta), Nottingham 17:50 (34, 19/8), Venturous and Wholestone (shared node), Dettori (sky Sun 21 : 7 on his
  Sun–Chiron).
- You read two or three of the generated readings next to the hand reads and say whether they read the way you read.
