# Layer 2 — roots (tools/layer2_roots.py), design: layer2_design.md (approved by Eddie 12 Oct 2026)

Run: `python3.12 tools/layer2_roots.py <race>` (needs layer1/ first) → `docs/classic/<race>/layer2/P*.json|txt`.
Test: `python3.12 tests/layer2_check.py`.

Removes nothing: every Layer 1 item keeps its place and gets a tag (root, derived + chain, mirror, duplicate, from_numbers, race_level),
so all Layer 1 reproduction checks (738/738) still hold.

## First run (12 Oct 2026), all 42 race folders, 252 runners
- ~4,150 derived, ~1,040 mirror, 0 loop mismatches (no tolerance stacking broke a chain).
- Design examples: York sky Sun -> Mason Pallas Dec 33 derived (Equator 19 + 14); sky Sun -> horse Ketu Dec 42 derived (19 + 23);
  horse Ketu – Mason Pallas Dec 9 derived (23 − 14); Newmarket July sky Pluto -> Hornby Venus Dec 38 derived (natal 21 + movement 17);
  Dettori sky Sun moved Dec 21 stays a root.
- All 5,080 derived/mirror chains re-added from the actual coordinates: exact.
- Hand-read items that turn out to be arithmetic (still listed, now tagged): e.g. York 16:15 'sky Pluto -> horse Quaoar RA 30' = sky
  Pluto–Quaoar RA 25 + horse Quaoar's movement 5; 'sky Mars -> horse Orcus Dec 15' = sky Mars–Ketu 9 + sky Ketu -> horse Eris 4 + horse
  Eris–Orcus 10.
