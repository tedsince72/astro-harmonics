# Layer 2 — roots (design for Eddie to check before building; 12 Oct 2026)

Layer 2 reads Layer 1's inventory and marks which items are ROOTS and which are just ARITHMETIC from other items, so one fact is not
counted several times. It removes nothing: every Layer 1 item stays, tagged root / derived / mirror / race-level, and every derived item
carries the chain it comes from.

## Rule 1 — numbers on a line add up (Dec and RA)
In Dec, every body sits on one line (the Equator is the point 0). In RA, every body sits on one circle. A whole or ninth number is a
distance between two points on that line. If A–B is a number and B–C is a number, then A–C is automatically a number (their sum or
difference). So within one runner, in one plane:
- Points: sky bodies, horse bodies, jockey bodies, and (Dec only) the Equator point 0.
- Edges: every Layer 1 item that is a whole/ninth distance in that plane between two of these points — Equator values (point–0),
  natal links (inside a chart and cross), movements (sky X–natal X), strikes (sky X–natal Y), sky numbers (sky X–sky Y).
- Points joined by number edges form a GROUP. A group of k points has only k−1 independent numbers; every further number edge
  inside the group closes a loop and is DERIVED from the chain of the others.
- Which edge in a loop is called derived: the one lowest in this order (most 'downstream'), so roots are the most fixed facts:
    1 Equator value  >  2 natal link inside a chart  >  3 cross link (horse–jockey)  >  4 movement  >  5 sky number  >  6 strike.
  Ties: the tighter offset stays root.
- Check: the derived item's number must equal the signed sum of its chain's numbers (counted in ninths, RA modulo 360). If it doesn't
  (tolerances stacking up), it stays a root and is flagged.
- Flat and great circle are not lines, so nothing in them adds up — their items are always roots.

Examples this must reproduce:
- York 16:15: sky Sun Equator 19 + Mason Pallas Equator 14 -> 'sky Sun – Mason Pallas Dec 33' DERIVED (chain: Sun–0, 0–Pallas);
  'sky Sun – horse Ketu Dec 42' DERIVED (19 + 23); 'horse Ketu – Mason Pallas Dec 9' DERIVED (23 − 14).
- Newmarket July: Hornby Venus–Pluto Dec 21 (natal link) + Hornby Pluto moved Dec 17 -> 'sky Pluto – Hornby Venus Dec 38' DERIVED;
  horse Sun Equator 12 + horse Vesta Equator 21 -> horse Sun–Vesta Dec 9 (only if listed; 8.9896 is outside the window, so it isn't).
- Dettori: sky Sun moved Dec 21 from Dettori's Sun stays a ROOT (nothing else in that loop is a number; 7.014 and 28.014 are not).

## Rule 2 — the node mirror
Ketu is Rahu's mirror (RA + 180, Dec negated). Ketu items that repeat a Rahu item are tagged MIRROR of it:
RA items (Ketu value = 180 − Rahu value), Equator values (identical), same-body sets (identical distances), Equator ratios (identical).
Ketu items that are NOT a copy (e.g. a Dec distance from Ketu to another body) stay as they are.

## Rule 3 — same-body strike = movement
A strike where the sky body hits its own natal place (sky X on natal X) is the same fact as the movement item; tagged DUPLICATE of the
movement.

## Rule 4 — ratios made of numbers
A ratio item (sky/natal ratio, Equator ratio, horse:jockey ratio, pair family, same-body set) whose values are themselves whole/ninth
number items is tagged FROM NUMBERS (it says nothing the two numbers don't). Example: 28 and 7 make 4. A ratio between values that are not
numbers stays a root.

## Rule 5 — race-level items
Sky numbers and close sky pairs are the same for every runner. Tagged RACE-LEVEL; they still serve as chain links in Rule 1 for each
runner, but are not counted as a runner's own items.

## Not touched
Contacts, close links (non-number), shared pairs, pair sets, splits' own ratios (unless Rule 4 applies): roots. Layer 2 does not judge
importance — that is Layer 3.

## Output
docs/classic/<race>/layer2/P*.json and .txt per runner: every Layer 1 item with its tag (root / derived / mirror / duplicate /
from numbers / race-level) and, for derived items, the chain; the Dec and RA groups with their members; counts (Layer 1 items, roots).
Tests: the York, Newmarket July and Dettori examples above, plus a check that every derived item's chain really adds up, on all 30 races.
