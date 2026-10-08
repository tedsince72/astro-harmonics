# Doncaster 14:40, 18 Mar 2022 — runner records

Race id `20220318_doncaster_1440`. Off 14:40:41, winning time 4m 7.70s, finish 14:44:49. Five ran.
Repo: `tedsince72/astro-harmonics` (branch `main`). Every path below is relative to the repo root.

Settings (the agreed procedure, 8 Oct 17:38–17:44): natal charts at 12:00, natal Moon left out; window off−30 (14:10:41) to finish+30 (15:14:49); chords ≤0.15% (all three ratios in the interval list, shortest side ≥0.05°); numbers ±0.002° (kφ, φⁿ, k√2, whole, ninths; own RA does not count, own Dec does).

## The ten charts

| Finish | Tab | Runner | Role | SP | Full record | Walk-through (project doc) |
|---|---|---|---|---|---|---|
| 1 | P03 | Olympe De Gouges | horse | 25/1 | `rr/20220318_doncaster_1440/records/P03_olympe-de-gouges.md` | `claude/walk-doncaster-1440-20220318-p03-olympe-de-gouges.md` |
| 1 | P04 | David Noonan | jockey | 25/1 | `rr/20220318_doncaster_1440/records/P04_david-noonan.md` | `claude/walk-doncaster-1440-20220318-p04-david-noonan.md` |
| 2 | P05 | Oot Ma Way | horse | 5/6 fav | not built yet | — |
| 2 | P06 | Conor O'Farrell | jockey | 5/6 fav | not built yet | — |
| 3 | P07 | Poetria | horse | 15/8 | not built yet | — |
| 3 | P08 | Jamie Hamilton | jockey | 15/8 | not built yet | — |
| 4 | P01 | Fiamette | horse | 5/1 | `rr/20220318_doncaster_1440/records/P01_fiamette.md` | `claude/walk-doncaster-1440-20220318-p01-fiamette.md` |
| 4 | P02 | James Davies | jockey | 5/1 | `rr/20220318_doncaster_1440/records/P02_james-davies.md` | `claude/walk-doncaster-1440-20220318-p02-james-davies.md` |
| 5 | P09 | Suntory Star | horse | 80/1 | not built yet | — |
| 5 | P10 | Stephen Mulqueen | jockey | 80/1 | not built yet | — |

Each full record has the same order: 0 the chart; 1 body by body (Method 1, Method 3, Method 2, same body, numbers, parallels); 2 the transit Sun; 3 the transit Moon; Sun and Moon together; 4 the pair. Each `.json` next to it is the flat list of Method 3 items for side-by-side comparison. Walk-throughs (`*_walk.md`) hold, body by body: the body's Method 1 line (strongest strings, numbers and figures, out of bounds / stationary, partner links); every sky body (not the Sun or Moon) on its star strings within 0.15% at any point in the window, string by string, with the deviation at off−30 / off / finish / finish+30, the exact time wherever it falls and the zone (slow holds included — "more slow may mean more strong"); and the other items exact in the window; the Sun in full, the Moon (every strike from off−10 to finish+10; outside that only strikes with texture — strongest Method 1 strings, a string another sky body or the Sun also plays, UNISON or same body, the runner tightest in the field, the partner on the string, or the Sun's own distances — each marked with why), the pair, and my notes (kept in `notes/<TAB>.md`). The full Moon list is in each full record.

Also here: `mlist/` — the wide Method 1 lists for all ten charts and the five combined pair lists; `cross_<H>_<J>.txt` — direct links between each horse and its jockey.

## Rebuilding

```
bash setup.sh
python3 tools/runner_record.py 20220318_doncaster_1440            # every stage, every runner (~25 min on 2 CPUs)
python3 tools/runner_record.py 20220318_doncaster_1440 --stages records --tabs P01,P02
```
Working files go to `/home/claude/rr/20220318_doncaster_1440/`; records are copied here once checked.

## Corrections found while building (8 Oct)

- **Mars on Altair–Arcturus is exact at 14:41:34, 53 s into the race (0.003% at the off), not "exactly at the off"; Juno is exact at 14:34:30, not 14:35:17.** The old exact-time search left slow bodies on a 1.8-minute step; it now refines to the second.
- **The Moon striking the same string more than once in the window is now kept strike by strike.** This restored the Moon 5:8:13 on Sun–Betelgeuse at 14:43:41 in the race (the horse's Quaoar tightest), which the wide Moon window had replaced with the φ at 14:48:56.
- **Exact times of the Sun (and other sky bodies) are a few seconds earlier than in §77** (e.g. Alkaid–Arcturus 14:42:53, not 14:42:56; Procyon–Spica 14:52:08, not 14:52:18): the old minute file ended at 15:10, before off+30, so the Sun's rate came out ~1.2% low. The 1-minute grid gives the correct rate.
- **The direct links between two charts (`cross.py`) no longer include the natal Moon** (it had been counted as a body): now 24 × 24 bodies, 2,304 values (§77 had 25 × 25). For Olympe De Gouges / Noonan: φ/√2/whole/φⁿ 21 (chance ≈ 21), ninths 84 (chance ≈ 74).
- **MIRROR** is named when a sky body and the natal body sit inside the same string nearer opposite ends at distances within 1% of the base (three in the four records built so far, each 0.01–0.02% apart, all UNISON).
