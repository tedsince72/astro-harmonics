# Layer 4 — the field (tools/layer4_field.py), design: layer4_design.md (approved by Eddie 12 Oct 2026)

Run: `python3.12 tools/layer4_field.py <race> [--results]` (needs layer3/) → `docs/classic/<race>/layer4/field.json|txt` (blind);
`field_results.txt` only with --results (finishing positions are never used by any layer). Test: `python3.12 tests/layer4_check.py` — 10/10.

Shape table at STRICT and BROAD level, plus '1m' (cross link with 2+ sky bodies on both ends) and '12m' (pair in one chart, 2+ bodies);
tightest instance per shape; field-only findings per runner; strong hubs across the field; same pair / body across the field;
recurring annotations.

## First look across all races with results (12 Oct 2026) — descriptive only, NOT a test
Runners with at least one STRICT shape that no other runner in the field has: winners 16 of 36, other runners 51 of 192.
Caution: the 12 shapes were named from these same winners, so this is not evidence; the test is races Layer 1–4 have never seen.

## v1.1 (checker, 12 Oct 2026)
Independent checker rebuilt the shape table, field-only lists and tightest picks for York 16:15, Fontwell, Perth: identical. Fixes: tightest is now chosen separately at strict and broad level and flagged; shapes 7, 8, 12 left out of 'tightest' (no single tightness measure); each instance carries n_sky_bodies (Rahu/Ketu folded) and rests_on_near_or_broad; shape 5 key fixed.
