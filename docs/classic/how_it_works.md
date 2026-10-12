# How It Works (agreed with Eddie, 12 Oct 2026)

**What goes in.** Three charts per runner: the race-time sky, the horse natal and the jockey natal (12:00 standard time, no Moon).
Every body is measured in every plane — RA, Dec, Flat, great circle, Equator (|Dec|) — plus movement since birth (sky body against the
same natal body). Stars are background only.

**Layer 1 — the inventory.** Lists everything, judges nothing. For each runner: every link inside the horse chart, inside the jockey chart
and between them (cross links); every whole-number and ninth value (Equator at ±0.01); every simple sky/natal ratio (p <= 30, q <= 9, not 1);
every movement landing on a whole number or ninth; every same-body set and shared pair; and for each link, which sky bodies touch it,
in which plane, with the exact offset.

**Layer 2 — roots.** Some hits are just arithmetic from others (York: sky Sun 19 and Mason Pallas 14 make 'Dec 33'; Newmarket July:
Hornby's natal 21 plus his Pluto's movement 17 make 'Dec 38'). Layer 2 traces each hit back to its root so one fact isn't counted three times.

**Layer 3 — the web.** Joins what's left into each runner's web: which bodies are struck in more than one way, and how they connect across
horse, jockey and sky. Looks for the shapes seen in winners — cross link struck on both ends, the sky partner landing on the link, the same
pair together in the sky, both ends moved, swaps, triangles, the same number in both charts, shared node, one body carrying several kinds
of strike (Uranus at Newmarket July, Chiron in Dec).

**Layer 4 — the field.** For each shape: how many runners in the race have it, and how tight. No control — where the winner's detail
stands against the rest of the field.

**Layer 5 — the reader.** A plain written reading per runner, body by body, relationships first. Not a score; Eddie judges.

**How we build it.** One layer at a time, going back through the races in reverse order (Newmarket July 17:45, York 16:15, York 15:45,
Sandown, ...). Each layer must reproduce what was found by hand in each winner before the next goes on top. Independent checker after each
race. Rules frozen before testing on new races. Every script backed up to the repo.
