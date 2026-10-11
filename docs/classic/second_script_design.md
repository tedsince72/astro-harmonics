# Second script — design note (Eddie, 11 Oct 2026; to be built race by race, not yet built)

Purpose: read the winner the way Eddie reads it — how the strands FIT TOGETHER across horse, jockey and race sky,
not how many items there are. strings.py (counts of 'ways') is the base layer only; it ranked winners at chance.
It must read EVERY plane: RA, Dec, Flat, great circle, Equator (|Dec|), and movement since birth.

## What the reading must include (from the races so far)
1. Sky : natal ratio of a pair, simple p/q (q <= 9), in each chart — e.g. Gonggong–Uranus x18 (Newcastle 12:20),
   Juno–Pallas x2 and Chiron–Transpluto x5 (Newbury), Mercury 3+3 (Sandown), Juno–Gonggong x3 (Huntingdon).
2. A body in simple ratios in BOTH charts (Transpluto at Newbury; Mercury 3+3 at Sandown).
3. A pair the horse and jockey SHARE (near-equal natal value), with one of them in simple sky ratio
   (Newbury Juno–Pallas: horse 138.29, jockey 138.82, horse x2). Shared node (Newcastle 13:30: horse Rahu within 1.86 of Beasley's;
   Rahu–Sedna and Mars–Rahu shared).
4. Carry-over: a body from that pair appears again in the other chart (Pallas into Sheppard's chart, 23/9, and onto his Mars Dec 6).
5. Three-way sets: horse : jockey : sky all simple on one pair — Neptune–Rahu RA 4:3:3 (Huntingdon); Neptune–node recurs
   (Newcastle 12:20 Neptune–Rahu 9/4; Eddie's earlier Neptune–Rahu 8.99, Pholas Ketu).
6. Same-body sets (sky, horse, jockey of one body) — tight ones occur in losers too, so they weigh only when joined to the web.
7. A natal pair struck on BOTH ends by one sky body (Hart's Newcastle win; Frost Mars–Sun by sky Ceres) — common on its own (2–8 per runner).
8. Equator: natal body at a whole number / multiple of 3 (Newbury horse Sun 15), and sky : natal Equator ratio
   (Newcastle 13:30 sky Sun / horse Sun = 12, the only sky Equator ratio in the field).
9. Movement since birth (sky body minus the same natal body) at a whole number / ninth, ESPECIALLY when the moved body sits on
   a link between the charts. Eddie: 'you cannot underestimate this' — Newcastle 13:30 sky Ceres moved 30 (30.0058) from horse Ceres,
   and horse Ceres sits on Beasley's Mars (RA 0.14), the Mars of the shared Mars–Rahu pair.
   Tolerance note: 30.0058 is just outside ±0.005 — movement needs a slightly wider window or the near-whole value reported.
10. Returns: a sky body back on its own natal place (Sheppard's Mars, Newbury) — only one in that field.

## Scoring idea
Build a web per runner (bodies = nodes; ratios, strikes, shared pairs, movement = links). Score how joined-up it is across
both charts and the sky, and how much hangs on one body / one known pair (Neptune–node, Pallas–Juno, Sun on Equator),
not the number of items. Huntingdon showed volume misleads (Master Tommytucker had most items, finished 4th).

## Races to build it from (one by one, winner first)
Newcastle AW 12:20 and 15:40 (12 Nov 21), Catterick 15:05 (19 Nov 21), Newbury 13:50 (26 Nov 21), Sandown 14:25 (4 Dec 21),
Huntingdon 13:52 (5 Dec 21), Newcastle AW 13:30 (2 Jan 22), plus Exeter 15:15 and the earlier ten.
Reading aids already saved: tools/fit_read.py, tools/both_ends.py, tools/three_way_all.py, tools/equator_ratios.py.

## Patterns to track going backwards (added 12 Oct 2026, after Ffos Las, Lingfield, Newcastle 16:40, Haydock 14:05)
- Shared node: horse Rahu within 3° of jockey Rahu (horse born ~one 18.6-yr node cycle after the jockey) — 3 of 119 runner pairs:
  Venturous (W 25/1), Wholestone (W 16/1), Bristol De Mai (3rd; same jockey Twiston-Davies). Carries shared node pairs.
- Chiron–Transpluto sky/natal simple ratio in Dec: Not Available (x5), New Age Dawning (21/8), Two For Gold (14/5); others 1/87; NOT at Haydock.
  Dec chosen after seeing the winners — test only on new races.
- Movement landing on a cross link: horse Ceres 30 -> on Beasley Mars; Mulrennan Juno 33/9 -> on horse Pluto; Twiston-Davies Quaoar 39 -> on horse Gonggong;
  horse Orcus 9 -> on Bass Vesta. 33/9 moved twice (Mulrennan Juno, Wholestone Haumea).
- Same pair winning twice (Sir Chauvelin / Mulrennan, Nov and Feb): no natal pair in simple sky ratio in both races; the same natal bodies lit
  (Chiron, Neptune, Gonggong, Venus–Uranus, Ceres on the Equator, Pluto–Juno cross link) by different means — read body by body, all planes.
- Neptune–node: Newcastle 12:20 (9/4), Huntingdon (4:3:3, Bass natal = sky); not at Lingfield (Bass) or Haydock.
- Recurring hub bodies per winner: Gonggong, Orcus, Makemake (striking), Pallas/Juno, Mercury, Juno, Neptune, Sun (Equator x12, 15), Jupiter–Vesta, Haumea, Pluto.
- Jockeys seen more than once: Bass (2 wins), Mulrennan (2 wins), Cobden (2nd, 2nd, 4th, F), Twiston-Davies (3rd, W), Beasley, Marquand, Scudamore, Hart.

## Several scripts (Eddie, 12 Oct 2026: 'maybe we need several scripts to be able to read like this')
One reader per kind of link — sky/natal ratios per chart; movement since birth (with cross-link check, both planes); shared node and shared pairs;
Equator; three-way sets; natal pairs struck on both ends; same-body sets — then a final script that joins their output into each runner's web
and reads it body by body.
