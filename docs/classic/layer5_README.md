# Layer 5 — the reader (tools/layer5_reader.py), design: layer5_design.md (approved by Eddie 12 Oct 2026)

Run: `python3.12 tools/layer5_reader.py <race>` (needs layers 1–4) → `docs/classic/<race>/layer5/P*.md` (one reading per runner) and
`race.md`. Test: `python3.12 tests/layer5_check.py` — all hand-read phrases found in the 12 test winners' readings; no finishing positions
anywhere.

Additions while building (12 Oct 2026):
- an 'Equator values' line (natal whole/ninth) after the web — York's Mason Pallas 14 was otherwise not named;
- section 1: shapes judged on 2+ sky bodies use strict_multi for the strict level (Nottingham 15:30's Sedna–Chiron is strict on its two
  ends even though other items in the shape are broad);
- shapes listed one of each type first, then the rest; inside 'sky body divides a natal pair' the simpler ratio first (Dettori's 21 : 7, span 4);
- section 4 (arithmetic) also covers derived hits on hub bodies and on the other end of their close cross links (Hornby's Dec 38 = 21 + 17).
Full pipeline for a race: layer1_inventory.py -> layer2_roots.py -> layer3_web.py -> layer4_field.py -> layer5_reader.py.
