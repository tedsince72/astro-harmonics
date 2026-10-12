# Layer 3 — the web (design for Eddie to check before building; 12 Oct 2026)

Layer 3 reads Layer 1 + Layer 2 and, for each runner, (a) finds the bodies struck in more than one way, (b) joins them into a web
across horse, jockey and sky, and (c) names the shapes we have seen in winners. It describes; it does not score. Every finding carries
the exact Layer 1 items behind it.

## What it uses
- ROOT items only (Layer 2). Derived / mirror / duplicate / from-numbers items are shown as 'also' under their root, never counted again.
- Race-level sky items are used as context (e.g. the sky pair of a cross link), not as the runner's own hits.
- NEAR items (near cross links, Equator 0.01–0.05%, ratios 0.005–0.01%, horse:jockey 0.005–0.02%, near contacts) are used only when they
  JOIN something already in the web (both ends, or the body they touch, already have a tight item). Otherwise listed as 'near, unjoined'.

## Step 1 — ways each natal body is struck
For every horse and jockey body, the kinds of root hit it carries:
  P position — a sky body on it (strike or contact; returns flagged)
  M movement — its own sky body has moved a whole/ninth from it
  R ratio — a pair it belongs to is in simple sky/natal ratio (or pair family)
  B same body — sky, horse, jockey of this body form a set
  E Equator — its |Dec| is a whole/ninth, or its Equator is in ratio with the same body elsewhere
  S shared — a pair it belongs to is shared with the other chart, a pair set (horse:jockey:sky), or a horse:jockey ratio
  X cross — it is an end of a cross link
A HUB is a body with 3 or more kinds. Reported: each body's kinds with the items behind them.

## Step 2 — the web
Bodies (horse and jockey; sky bodies are the strikers, not nodes) are joined by: cross links, natal links (close or number), ratio pairs,
shared / pair-set / horse:jockey pairs, same-body sets (horse X – jockey X), Equator ratios between charts, splits, and two natal bodies
struck by the same sky body in the same item family. Reported: each connected web, its bodies, its hubs, whether it spans both charts,
and the path of items joining the hubs. (Size is reported but not used to rank — Huntingdon showed volume misleads.)

## Step 3 — shapes (each reported with its items, offsets, and whether it involves a hub)
 1 Cross link struck on both ends — and by how many different sky bodies; one sky body on both ends; 2+ bodies (Perth, Nottingham 15:30).
 2 Partner strike — on cross link H x – J y, sky y lands on horse x or sky x on jockey y (Newmarket July: sky Venus on horse Uranus).
 3 Pair together in the sky — the two bodies of a cross link are also close in the sky (great circle < 5) (York 16:15 Venus–Uranus).
 4 Both ends moved — both ends of one cross link have a whole/ninth movement (Wolverhampton 2023, York 16:15).
 5 Movement onto a cross link — a body that moved a whole/ninth is an end of a cross link (Venturous Ceres onto Beasley Mars).
 6 Swap — horse x near jockey y AND horse y near jockey x (Fontwell 2023, Sandown 2024).
 7 Triangle — three natal bodies pairwise linked, with one sky body striking all three corners, Ketu included (Ascot 2023).
 8 Same number in both charts — the same whole/ninth value as a root in the horse chart and in the jockey chart (Equator value or natal
   link), or the same sky/natal ratio in both charts (Nottingham 17:50: 34 and 19/8; Newmarket July: 21).
 9 Shared node — horse Rahu within 3 RA of jockey Rahu (or of jockey Ketu) (Venturous, Wholestone).
10 Sky body divides a natal pair — a split where the moved part is a root and the parts or span/other are in a simple ratio within 0.25%
   (Dettori: sky Sun 21 : 7 on his Sun–Chiron, span/other 4).
11 Joined same-body set — a same-body set whose body is also in a cross link or a ratio pair (York 16:15 Chiron, node).
12 Pair split by one sky body on both ends inside one chart (Sandown 2024 Brace's Mars–Jupiter struck by three bodies).

## Annotations (not rules)
Pairs and cross links that recurred in earlier winners are flagged wherever they appear, so we can watch them going forward, without
weighting them: Neptune–node, Chiron–Transpluto, Haumea–Ketu, Pallas–Juno, Jupiter–Vesta, Neptune–Vesta, Saturn–Neptune, Venus–Uranus;
cross links horse Sedna–jockey Chiron, horse Pluto–jockey Neptune, horse Makemake–jockey Haumea, horse Venus/Uranus–jockey Uranus/Venus.

## Output
docs/classic/<race>/layer3/P*.json and .txt per runner: hubs (body, kinds, items), webs (bodies, hubs, path), shapes (type, items,
offsets, hub involvement), near items that joined, annotations.

## Tests (must pass before Layer 4)
Every shape we named by hand in a winner must be found in that winner: York 16:15 (3, 4), Newmarket July (1, 2, 8), Perth (1, 2+ bodies),
Nottingham 15:30 (1, 3 bodies), Wolverhampton 2023 (4), Fontwell 2023 (6 x2), Sandown 2024 (6, 12), Ascot 2023 (7), Nottingham 17:50 (8),
Venturous and Wholestone (9), Dettori (10), York 16:15 (11). Plus: every hub body named in a winner read is a hub.
