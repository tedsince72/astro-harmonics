> **SUPERSEDED (30 Sep 2026).** This describes the old geo-scanner system before the rebuild. For current work read `claude/handover-race-reviews.md`. Kept for history only.

# Handover: UK Race Baseline Review (Geo-Scanner System)

## Standing Constraint — PRESERVE VERBATIM
> **Always wait for Eddie's explicit confirmation before building or generating code or artifacts.**

---

## What This Session Was Doing

Conducting a systematic **baseline review** of historical UK horse race file pairs — verifying that the geo-scanner system correctly identifies the winner in every training/baseline race, and documenting the full signal detail for each.

The review also compared **old (bugged-time) predict files** against **corrected-time predict files** to confirm the time-fix produces stronger/tighter signals.

---

## Background: The Time Bug

`extract_time_from_title()` captured race time in 12-hour format with no AM/PM conversion. All historic predict files used a race time **12 hours early** (e.g. a 13:00 race was computed at 01:00). Celestial positions differ materially over 12 hours, so the old signals were wrong.

**Fix was applied.** All new predict files use corrected times.

**Confirmed pattern:** corrected times produce more and tighter exclusive signals (S6-TN, UNIQUE EQ, UNIQUE 3W) compared to old bugged-time versions.

---

## File System — Predict File Format

Each race has two uploaded files:
- `race_batch_YYYYMMDD_venue_HHMM.txt` — full detail (raw signal data)
- `race_batch_YYYYMMDD_venue_HHMM_predict.txt` — summary output (TR-TR, Gap, ranked runners, winner marked)

---

## Signal Hierarchy (geo-scanner system)

**PRIMARY / EXCLUSIVE signals** (identify winner):
1. UNIQUE 3W (unique cross-chart three-way hit) — strongest
2. UNIQUE EQ (unique equator hit)
3. S6-TN non-DC (transit-to-natal harmonic signal, not a date constant)

**SECONDARY / DEPTH signals** (field background, not discriminating):
- S6-NN, S5, S4, S3, S1

**Key principle:** A horse with EXCLUSIVE signals always outranks a horse with rich DEPTH-only signals. No exceptions across all 12 baseline races reviewed.

**TR-TR classifier:**
- LOW = 1 pair has exclusives (clear winner signal environment)
- MIXED = 2 pairs have exclusives
- HIGH = 0 exclusives or broad field distribution

**Gap classifier:**
- CLEAR = large points gap between #1 and #2 in predict file
- NARROW / CONTESTED / NONE = progressively tighter field

---

## Baseline Races Reviewed — Status

All 12 races confirmed ✅ CORRECT (system correctly identified winner in every case).

### Races reviewed this session (Races 9–12 of the baseline set):

**Race 9 — Carlisle 13:55 — 14/10/2021**
- `race_batch_20211014_carlisle_1355`
- Winner: **Arvico Bleu** / Brian Hughes (P01/P02) — Cat 1 (25/1)
- EXCLUSIVE: 3 S6-TN [99.9, 98.7, 93.6] on horse + 2 UNIQUE EQ (Uranus [Dec] 0.0019°, Eris [Dec] 0.3488°) + UNIQUE 3W hit
- TR-TR: LOW | Gap: CLEAR
- Rating: STANDOUT
- No old log entry — cannot compare bugged vs corrected time

**Race 10 — Exeter 14:05 — 19/10/2021**
- `race_batch_20211019_exeter_205`  *(note: file uses 205, not 1405)*
- Winner: **An Tailliur** / Jonjo O'Neill Jr (P01/P02) — Favourite (6/5)
- NEW (corrected time): 2 S6-TN [98.8, 90.5] + 2 non-unique EQ (Uranus [Dec] 0.0378°, Eris [Dec] 0.2927°)
- OLD (bugged time): 0 S6-TN + 2 non-unique EQ — discriminator was S5 depth only
- ✅ Corrected time: TIGHTER — gained 2 S6-TN where old had zero

**Race 11 — Exeter 15:15 — 19/10/2021**
- `race_batch_20211019_exeter_1515`
- Winner: **Forget You Not** / James Best (P11/P12) — Outsider (25/1)
- NEW (corrected time): 6 S6-TN [99.2, 96.5, 94.8, 94.5, 92.9, 91.4] + 2 UNIQUE EQ (Pallas [Dec] 0.0311°, Sedna [Dec] 0.2498°) — 1,013pts EXCLUSIVE
- OLD (bugged time): 0 S6-TN + 2 UNIQUE EQ (Pallas [Dec] 0.196°, Sedna [Dec] 0.252°)
- ✅ Corrected time: SIGNIFICANTLY TIGHTER — gained 6 S6-TN; Pallas orb collapsed from 0.196° → 0.0311° (6× tighter)
- TR-TR: LOW | Gap: CLEAR | Rating: STANDOUT

**Race 12 — Doncaster 13:00 — 22/10/2021**
- `race_batch_20211022_doncaster_1300`
- Winner: **Oh Herberts Reign** / Ryan Moore (P03/P04) — Cat 1 (16/5)
- EXCLUSIVE: 9 S6-TN [99.2, 97.4, 97.2, 96.9, 96.6, 96.3, 93.8, 92.8, 92.1] — ALL on jockey Ryan Moore (P04)
- Key S6-TN pairs: Chiron→Arcturus [Ninths] Dec 99.2, Haumea→Castor [Silver Ratio] Dec 97.4, Vertex→Alphecca [Ninths] RA 97.2, Vesta→Rigel [Silver Ratio] Dec 96.9, Part_of_Fortune→Arcturus [Ninths] Dec 96.6, Neptune→Castor [Sqrt2] RA 96.3, Eris→Spica [Golden Ratio] RA 93.8, Quaoar→Regulus [Ninths] RA 92.8, Part_of_Fortune→Antares [Whole Number] Dec 92.1
- Winner had ZERO 3W or EQ hits — signal was purely S6-TN
- Non-winners had rich 3W/EQ (Baikal: 2 UNIQUE 3W + 5 EQ; Superior Force: 1 3W + 4 EQ) but ZERO S6-TN
- Jockey S4 22/22 PERFECT | Horse S6-NN 6/6 all unique | Jockey S6-NN 8/9
- TR-TR: LOW | Gap: CLEAR | 7 runners | Rating: STANDOUT
- Silvestre De Sousa had S6-NN 15/15 all unique (99.6 top) — depth-only, no exclusives

---

## Races in Old Log (bugged-time predict files)

The `uk-race-log.md` memory file contains old production entries for:
- Race 7 (Exeter 14:05) — log label: "Race 7" — old signals noted above
- Race 8 (Exeter 15:15) — log label: "Race 8" — old signals noted above
- Earlier races (Kempton, Musselburgh, Ascot, Haydock, Brighton, Yarmouth) — comparison already done in prior session

**Carlisle has NO old log entry** — it was not part of the original bugged-time baseline set.

---

## Old-vs-New Comparison Summary (all races)

| Race | Winner | Old S6-TN | New S6-TN | Tighter? |
|------|---------|-----------|-----------|----------|
| Kempton 310 | Exceedingly Regal | 1 | (checked prior) | ✅ |
| Musselburgh 145 | Graces Quest | 3 | (checked prior) | ✅ |
| Ascot 445 | Dark Shift | 2 | (checked prior) | ✅ |
| Haydock 220 | Golden Flame | 4 | (checked prior) | ✅ |
| Brighton 425 | Discomatic | 1 | (checked prior) | ✅ |
| Yarmouth 320 | Ropey Guest | 2 | (checked prior) | ✅ |
| Exeter 14:05 | An Tailliur | 0 | 2 | ✅ gained 2 |
| Exeter 15:15 | Forget You Not | 0 (2 UNIQUE EQ) | 6 + tighter EQ | ✅ significantly tighter |
| Carlisle | Arvico Bleu | N/A | N/A | ❌ no old entry |
| Doncaster | Oh Herberts Reign | (not in old log) | 9 | N/A |

**Pattern confirmed across all races: corrected times produce more/tighter exclusive signals.**

---

## Pending Work (in order)

1. **Continue baseline review** — next race pair(s) beyond Race 12 (Doncaster). Eddie to upload next file pair(s).
2. **Confirm results scraper fix** — mentioned as complete in another chat; verify tested.
3. **Re-scrape all 96 historical races** with fixed scraper.
4. **Regenerate full_race_detail txt files** and re-run `uk_race_predictor.py` on all 96.
5. **Conduct full baseline review** on clean re-generated data (all 96 races).

---

## Key Memory Files to Read Before Starting

Always read before any race analysis:
- `/projects/019cbbbf-aa90-770a-b141-527039ffee5c/football-pipeline-protocol.md` — horse racing master protocol
- `/projects/019cbbbf-aa90-770a-b141-527039ffee5c/uk-horseracing-instructions.md` — geo-scanner instructions
- `/projects/019cbbbf-aa90-770a-b141-527039ffee5c/uk-race-log.md` — production race log (old format entries)

Race logs continued in:
- `uk-race-log-2.md` (Race 5 Brighton onwards)
- `uk-race-log-3.md` (Race 12 Newbury onwards — note: this is a different numbering system from the baseline review above)
- `uk-race-log-4.md`, `uk-race-log-5.md`

---

## 8 Training Races (confirmed double-power in all 8)

| Race | Date | Winner | Odds | Cat |
|------|------|---------|------|-----|
| Newcastle AW 433 | 02/08/21 | Athmad / Jason Hart | 25/1 | Cat 1 |
| Chelmsford AW 330 | 26/08/21 | Toussarok / Oisin Murphy | 2/1F | Cat 2 |
| Carlisle 1355 | 14/10/21 | Arvico Bleu / Brian Hughes | 25/1 | Cat 1 |
| Doncaster 1300 | 22/10/21 | Oh Herberts Reign / Ryan Moore | 16/5 | Cat 1 |
| Doncaster 1300 | 18/03/22 | Olympe De Gouges | 25/1 | Cat 1 |
| Haydock | 23/03/22 | Soldier Of Destiny | 13/8F | Cat 2 |
| Ripon | 16/06/22 | Society Red / Oisin Orr | 16/1 | Cat 1 |
| Ascot | 17/06/22 | Changingoftheguard | 11/10F | Cat 2 |

---

## Scripts (installed at /home/claude/)

- `geo_scanner.py` — primary tool (two ranked lists per race)
- `race_observer.py` — full raw signal data
- `step1_table.py` — dominant family table (reference only)
- `uk_race_predictor.py` — generates predict files

---

## Pending Script Fix

`DATE_CONSTANT_MIN_TABS` in section scripts (section1–6.py) is hardcoded at 5. Should be proportional to runner count:

```python
n_runners = len(p_tabs) // 2
DATE_CONSTANT_MIN_TABS = max(5, round(n_runners * 0.5))
```

Apply to section1.py through section6.py before accumulation analysis. Not yet implemented.
