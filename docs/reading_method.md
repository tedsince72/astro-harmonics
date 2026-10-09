# How a race is read in full (Doncaster and Catterick, 9 Oct 2026)

This is the procedure that found the connections in the Doncaster and Catterick reads (results in `docs/cross_race_bodies_chords.md`,
section I). Eddie, 9 Oct: "please learn this" — **every race is read at this depth**. A quick read of the summary parts only (timeline, natal
Sun/Mars, joint) found two of Catterick's threads; the full read found the rest.

Principles carried in from the project: say what you see; one race at a time; one layer at a time, waiting between layers; the pairing
(horse + jockey + sky) is the unit; counts are background, never the signal; the answer is in the detail of bodies, chords and timing.

---

## 0. What has to exist first
- The race built on the Mac (records, `compare/table.csv`), with the **real off time and winning time** in `reference/races.csv`.
- `tools/reading_pack.py RACE` → `rr/<RACE>/compare/reading-pack.md` (all layers, focus bodies, joint, triangle corners, numbers, timeline).
- `tools/layer_view.py RACE KIND [LAYER]` prints one layer for every runner (the view used layer by layer):
  `M3` · `M2 Nodes` · `M2 L2` · `M2 L3` · `M2 L4`.

## 1. What counts as "live at the race"
- **X** = the sky chord comes exact between the off and the finish.
- **Held** = the sky chord is within **0.02% at both the off and the finish** — then **A** applying (exact after the finish) or **S**
  separating (exact before the off), with the time to exact. Slow holds (hours, days) are the background; holds exact within minutes are the
  near-race layer.
- For each item read: sky body + chord · measure (RA / Dec / Flat / Sky) + base (two stars, or a body and a point) · natal body + chord ·
  natal tightness (Method 3: the Method 1 string, STRONG ≤0.02%; Method 2: the natal chord on the same base) · the chart's rank on that
  string/base (tightest = #1) · flags SAME BODY (sky X on natal X), UNISON (same chord both sides), MIRROR.

## 2. The order, and what to look at in each layer
Read **every runner** in every layer, winners first, then **every beaten runner for contrast**. Write down what each layer adds and how it links
to the layers before.

1. **Method 3 — sky bodies on natal star strings.** Who is struck in the race; which natal bodies are tightest and live; which are STRONG.
   Look for: both charts of a pair live on the same natal body (e.g. both natal Suns, Doncaster); a natal body struck IN SEQUENCE by several sky
   bodies (Doncaster horse's Sun+Mars: Juno → Mercury → Mars; Catterick horse's Chiron: Jupiter → Jupiter → Mercury); a sky body on a natal body
   while another body sits on the reverse (Doncaster jockey: the Sun on his Neptune, Uranus on his Sun; Catterick jockey: Sedna on her Eris and Eris
   on her Sedna); slow bodies holding a chart's nodes or outer bodies at 0.001%; the STARS that recur on the pair's strings (Doncaster Altair,
   Arcturus; Catterick Altair, Procyon).
2. **Method 2 — Nodes layer** (Rahu/Ketu as base ends). Often thin for the winners; note the repeats from Method 3 (same natal body reached again,
   same star) and the same-body holds (Catterick: the horse's own Haumea held by Haumea).
3. **Method 2 — L2** (slow outer bodies as base ends). Fast bodies moving on slow bases. Look for the same natal bodies coming back (Doncaster:
   Mercury on Haumea–Altair holding the horse's Sun+Mars again); one transit running through the pair across the race (Doncaster Mercury on the
   jockey's Juno and Neptune); bases both charts share in the race.
4. **Method 2 — L3** (Jupiter, Saturn, Mars, Ceres, Pallas, Juno, Vesta as base ends). Mars itself as a base end; the asteroid hubs (Catterick:
   Pallas triangles carrying horse-Mars with jockey-Pluto, and jockey-Mars with horse-Saturn); same-body crossings across the pair (Doncaster:
   Haumea through the horse's own Haumea, Sedna through the jockey's own Sedna).
5. **Method 2 — L4** (Sun, Mercury, Venus, Moon as base ends). The same triangles as L2/L3 read from another corner. Note who is tightest on which
   corner (section 3).
6. **Same body, pair same body, natal→sky numbers, parallels** near the race (pack section 5): the jockey's Sun number in the race (Doncaster
   1511/9, Catterick 201/9); natal body + a third point that ties to the other chart's strike (Catterick: horse's Mercury + Alphecca 18 s after
   Mercury struck the jockey's Neptune on Algorab–Alphecca); a chart's two receivers in one same-body chord (Catterick horse: Neptune + Chiron).
7. **The timeline** (pack section 6): every non-Moon event per pair, off −2 min to finish +2 min, at ANY natal tightness (since 9 Oct; loose ones
   marked "(loose)" — before, the pack dropped M3 strings >0.05% and M2 natal chords >0.03%, and Method 2 items that do not come exact were wrongly
   listed), ◆ = both charts within 10 s; the beats are listed in two groups, both sides tight and with a loose side. Read the beats as
   moments: which bodies fire together in both charts (Doncaster: Mars on the horse's Sun at 14:41:34 and the jockey's Mars number at 14:41:36;
   then the Sun beat 14:42:36–53).

## 3. Triangles and corners
A tuned base + a moving body = three points. The same three points appear in several layers with a different body moving (pack section 4):
e.g. Mercury moving on Haumea–Altair (L2) and Haumea moving on Mercury–Altair (L4). For each triangle near the race, read every corner:
- **Which chart is tightest on which corner.** Doncaster: the winners on the corner where a fast body moves on a slow/star base; the beaten on the
  corner where a slow body moves on a fast-body base. Catterick: Sun–Mars–Antares — the Sun corner the winning jockey's Pluto, the Mars corner the
  beaten favourite's jockey; on the two Venus triangles the winning pair took both corners.
- **Double same-body triangles**: one triangle holding TWO of a chart's own bodies, each by its own sky body (Catterick horse: Rahu–Haumea–Altair,
  Venus–Neptune–Equator; jockey: Mercury–Pluto–Rahu). Seen on a beaten chart too (Hart, Mars–Pallas–Alphecca, looser) — read the tightness.
- **Joint triangles**: one triangle holding a body of each chart of the pair (Catterick: Sun–Venus–Algol with both charts tightest; Pallas–Juno–
  Sirius with the jockey's Mars and the horse's Saturn; Neptune–Transpluto–Sedna with the horse's Jupiter and the jockey's Mars and Pluto).

## 4. Threads to follow across layers (observations so far — not rules)
- **Mars and the Sun** in both charts of the pair, and on which corner (Doncaster Mars beat in both charts; Catterick Sun–Mars–Antares).
- **Juno with Mars or the Sun** (Doncaster: Juno on the horse's Sun–Mars string, her Mars on a Juno base; Catterick: the jockey's Mars on Pallas–
  Juno–Sirius, her natal Sun + Juno same-body chord).
- **A natal body that keeps receiving** (Noonan's Neptune; the Catterick horse's Neptune and Chiron) — follow it through every layer.
- **Venus** (Catterick: Venus on Neptune bases at the off in both charts).
- **Stars that recur** on the pair (Altair in both races).
- The jockey's Sun number in the race.

## 5. The beaten runners
Every layer is read for every beaten runner too, and what they have is written down: the tightest places they take (whole layers at Doncaster
L4 and the Nodes layers), their own same-body figures, their Sun/Mars numbers in the race (Capuchinero), their strong strikes just after the race
(Hart). A feature only means something if the beaten runners do not have it in the same form — so each finding is checked against the field
before it is called different.

## 6. Cautions
- **Short bases swing fast**: on a small base the sky deviation can be large at the off and the finish and still pass through exact in between
  (Catterick: Mars/Saturn √2 on Saturn/Mars–Deneb Algedi — 0.063% at the off, 0.002% at 14:40:45, 0.097% at the finish; real). Since 9 Oct
  `race_table.py` re-measures every non-Moon Method 2 "exact" time in the window on the 1-minute sky: kept if ≤0.005%, re-timed if it comes exact
  within ±10 min, otherwise marked "does not come exact"; the pack shows which. Do not judge exactness from the off/finish deviations alone.
- **Checks before words**: no "only", "unique", "the most" or "different" without a query over all charts in the race; numbers and times copied
  from the tool output (never from a rounded column); unchecked points marked "not yet checked against the field".
- **Joins**: count is not the signal (Ffos Las: the beaten pairs are joined MORE); read which bodies and stars make the joins (pack section 3b).
- **Independent check** after each race: a reviewer that has not seen the reading checks the race's section of the note against the table.
- L1 rows repeat Method 3 rows (left out of the views).
- Counts (beats, crossings, strings struck) do not follow the result across the seven races — background only.
- The reads so far were done with the result known; the test is a blind read (results withheld, then compared).

## 7. Writing it down
After each race: its section in `docs/cross_race_bodies_chords.md` (section I), layer by layer, then the timeline, then a short "in short";
commit, push, and update the project copy `claude/cross-race-bodies-chords.md`.
