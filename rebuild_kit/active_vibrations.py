"""
active_vibrations.py  v4.1
=====================
Pipeline position: Step 3 of run_race_swiss.py / run_card_swiss.py.
  Input : race_batch_YYYYMMDD_venue_HHMM.xlsx  (TRANS, P01..Pnn, NATAL_HOURLY
          and META sheets - chart generator v2.2 or later)
  Output: race_batch_YYYYMMDD_venue_HHMM_active.xlsx  (input left untouched)
  Calls : no other scripts (pandas + openpyxl only).

Locates the most "active" celestial body pairs at the moment of a race
(transit-to-transit), then traces each qualifying pair through the
natal-to-natal chart and transit-to-natal chart of every subject (horse
and jockey) in the race, flagging recurring hits.

Seven "vibration" (harmonic) scoring families are checked for every distance:
  1. Whole numbers 1-200          (tol 0.02, squared, no decay)
  2. Golden ratio interval (MOD phi)      (tol 0.03236, squared)
  3. Golden ratio powers (phi^-1..10,
     10*phi^-1..7, 100*phi^-1,1)          (relative tol, squared)
  4. Repeating-ninths family (n/9)        (linear, asymmetric bounds, as given)
  5. sqrt(2) interval + 10x/100x targets  (tol 0.02828 / relative, squared)
  6. Silver ratio (1+sqrt2) interval
     + 10x target                        (tol 0.04828 / relative, squared)
  7. Conjunction (distance near 0)        (tol RA 1.0 / Dec 0.125, squared)
  Families 2, 5 and 6 score from their FIRST multiple upward - a distance
  near 0 is scored only by Conjunction (v3.0).

Pipeline:
  1. Compute all transit-to-transit (TT) pairwise distances (RA, Dec) for
     the 53 transit bodies (BODIES_TRANSIT: 26 planets/points + 22 fixed
     stars + 5 transit-only angles/points), skipping star-to-star pairs.
     Score against all 7 families, keep the best score + family
     ("vibration") per pair.
  2. Rank TT pairs by best score, process every pair scoring >= 80
     (TT_THRESHOLD). This list comes only from the shared TRANS chart, so
     it is identical for every subject in the race.
  3. For each qualifying pair and EACH P-tab (horse or jockey) in the race:
       - Natal-to-natal (NN): direct natal(A)-natal(B) distance, plus
         natal(A)-natal(X) / natal(B)-natal(X) convergence checks against
         every other body X.
       - Transit-to-natal (TN): transit(A)->natal(A)/natal(B) (self/cross),
         transit(B)->natal(A)/natal(B) (self/cross), plus convergence
         checks against every other body X.
       - Tally how many times each body appears as a scoring hit across
         NN+TN; flag any body appearing 3 or more times. (The tally counts
         one per scoring FAMILY row, so a distance scoring in 3 families
         counts 3.)
       - Classify into MAIN / ADDITIONAL / SOURCE CHAINS highlight blocks
         (see build_pair_highlights).
  4. Write a NEW Excel file (input file left untouched) containing:
       SUMMARY_MAX  per-subject MAX of per-pair MAIN totals (core pairs),
                    field max / gap / margin / rank (values)
       TR_TR        race-level record: every qualifying transit pair
       HITS         one row per distinct contact per runner, scored at
                    noon and across the whole birth day
       SUMMARY      per-subject MAIN SUMMARY totals by body, field max /
                    gap / margin / rank (Total row = formulas into P tabs)
       P01..Pnn     full per-subject detail + fixed-star extended section
       TT_DIST      transit x transit RA/Dec distance matrices
       TRANS_POS    raw transit RA/Dec        (read by three_way_midpoints.py)
       Pnn_POS      raw natal RA/Dec per subject (read by three_way_midpoints.py)
       Pnn_DIST     Nat x Nat and Tra -> Nat RA/Dec matrices (race_observer.py)

Notes:
  - 'equator' has no RA value. Every TT / NN / TN calculation requires both
    RA and Dec, so equator is silently excluded from TT pairs and NN/TN
    hits in this script; it appears only in the Dec distance matrices.
    Equator (EQ) signals must therefore come from a downstream script
    (to be confirmed when run_pipeline.py is reviewed).
  - Every cell is a plain value (v4.0): no formulas anywhere, so Python
    and Excel read the same numbers.
  - The raw _POS and _DIST sheets still list natal Moon and all bodies;
    the exclusions below apply to scoring only.

Changes in v4.1 (Phase 3):
  The chart generator's META and NATAL_HOURLY sheets are copied unchanged
  into the output, so every later step (sections, three-way, alignment,
  race summary) reads one file: runner roles, cloth numbers, placeholder
  status, race details and the birth-day paths.

Changes in v4.0 (Phase 2 of the rebuild plan):
  H1  HITS sheet: one row per distinct contact per runner (layer, from, to,
      mode, family), however many qualifying pairs produced it; columns for
      relations, via_pairs_n / via_pairs / best_tt_score, MATCH, and the
      MAIN / ADDITIONAL summary label with its rule and linking bodies.
      NN contacts have no direction (one row per body pair).
  H2  Range scoring from NATAL_HOURLY: dist_mid/min/max and score_mid
      (local noon), score_min (holds all day) and score_max (best moment),
      computed exactly from each family's target windows. certainty =
      fixed (holds all day, < 1 point of change) / certain (holds all day)
      / possible (only at some moment). Rows are kept when score_max > 0.
      Natal-to-natal distances follow both bodies hour by hour (H3-A).
  H5  Natal Moon excluded in Dec as well as RA (NN both sides, TN target,
      fixed-star section). Transit Moon is exact and still scored.
  H6  Part_of_Spirit added to TRANSIT_ONLY_BODIES (race chart only).
  D3  Transpluto's model error (+/-0.01 deg) is treated as a band in HITS
      and TR_TR: its contacts are 'certain' only if they hold across it.
  C5c-B  TN node<->node RA is one axis contact: self twins collapse to the
      Rahu row, mirror twins to the Rahu->Ketu row, and the mirror keeps
      only families the self row does not score (cross or convergence).
  TR_TR sheet: every qualifying transit pair with its RA / Dec distance,
      best score, family, mode and all family scores.
  AV-D1/D2  All summary totals written as values (P-tab per-pair sums and
      MAX row, SUMMARY Total row, SUMMARY_MAX); SUMMARY_MAX keeps the v3
      arithmetic and works for a field of one.
  P tabs, SUMMARY and SUMMARY_MAX are otherwise unchanged in layout; their
  scores remain the local-noon values.

Changes in v3.0 (scores change throughout - not comparable with v2.x):
  C1  New 7th family "Conjunction": squared curve, tolerance RA 1.0 deg /
      Dec 0.125 deg; co-exists with other families. Golden Ratio, Sqrt2 and
      Silver interval scoring no longer scores the zero multiple. No
      Conjunction on TN 'self' rows for bodies beyond Pluto
      (SLOW_SELF_NO_CONJUNCTION).
  C2  RECURRING BODIES ranked by strength (sum of best score per distinct
      contact), flagged at race-level top RECURRING_TOP_PCT %, minimum
      RECURRING_MIN_CONTACTS contacts. Script is now two-pass (all subjects
      computed before any sheet is written).
  C3  MATCH only on convergence rows. TN self + cross rows hitting the same
      natal body (same mode/family) are noted "BOTH" - no extra score.
  C4  Type 1 gate uses >= TT_THRESHOLD, matching pair qualification.
  C5  Rahu/Ketu 180 deg axis: (a) Ketu/Rahu TT pair scored on Dec only;
      (b)/(c) node<->node RA rows dropped in NN and TN; (d) RA contacts to or
      from the node axis de-duplicated per family (higher score kept; ties
      prefer a Type 1 relation, then the Rahu label). The RA axis counts as
      one target for MATCH / Type 2 grouping and C2 contacts.
  Housekeeping: unused write_highlight_block parameter and merge_tally
      removed; FAST_NAMES replaced by TRANSIT_ONLY_BODIES.

Changes in v2.6 (output changes confined to the two areas below):
  - Fixed-star section (bottom of each P tab):
      * FS-TN now excludes natal Moon RA, matching the rule used everywhere
        else (previously scored because the natal/transit flag was wrong).
      * Star-to-star combinations are skipped, matching TT ranking and NN/TN
        hit detection (previously a star vs itself scored 100 in three
        families, and natal vs transit star scored on precession alone).
  - SOURCE CHAINS block: ties broken by body name then type, so the same
    input always produces an identical output file.
  All other sheets, scores and totals are unchanged from v2.5.

Usage:
    python active_vibrations.py --input race_batch_20260822_chester_1440.xlsx
"""

import argparse
import itertools
import math
import os
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter


# ── Body lists ────────────────────────────────────────────────────────────────
# BODIES (48)          = 26 planets/points (incl. equator) + 22 fixed stars
# TRANSIT_ONLY_BODIES  = 5 chart angles/points with no natal equivalent
# BODIES_TRANSIT (53)  = BODIES + TRANSIT_ONLY_BODIES

BODIES = [
    # Original planets and slow bodies
    "Ceres", "Chiron", "Eris",
    "Juno", "Jupiter", "Ketu", "Mars", "Mercury", "Moon", "Neptune",
    "Pallas", "Pluto", "Rahu", "Saturn", "Sun", "Uranus",
    "Venus", "Vesta", "equator", "Gonggong", "Haumea", "Makemake",
    "Orcus", "Quaoar", "Sedna", "Transpluto",
    # All 22 fixed stars — full set, treated identically to original 4
    "Aldebaran", "Antares", "Fomalhaut", "Regulus",
    "Algol", "Pleiades", "Capella", "Sirius", "Procyon",
    "Alkaid", "Algorab", "Spica", "Arcturus", "Alphecca",
    "Vega", "Deneb Algedi", "Rigel", "Betelgeuse", "Polaris",
    "Castor", "Altair", "Bellatrix",
]

TRANSIT_ONLY_BODIES = [
    "Ascendant", "Midheaven", "Vertex", "Part_of_Fortune", "Part_of_Spirit",
]

# All bodies that appear in transit charts (standard + transit-only)
BODIES_TRANSIT = BODIES + TRANSIT_ONLY_BODIES

# Full set of all 22 fixed stars — used to filter fixed-star-to-fixed-star pairs
FIXED_STARS = {
    "Aldebaran", "Antares", "Fomalhaut", "Regulus",
    "Algol", "Pleiades", "Capella", "Sirius", "Procyon",
    "Alkaid", "Algorab", "Spica", "Arcturus", "Alphecca",
    "Vega", "Deneb Algedi", "Rigel", "Betelgeuse", "Polaris",
    "Castor", "Altair", "Bellatrix",
}

# Extended fixed-star set — same as FIXED_STARS, kept as ordered list for reference
FIXED_STARS_EXTENDED = sorted(FIXED_STARS)
FIXED_STARS_EXTENDED_SET = FIXED_STARS

BODY_COL_INDEX_HL = {b: i for i, b in enumerate(BODIES)}

TT_THRESHOLD = 80.0   # pairs qualify at >= 80; the Type 1 gate also uses >= 80

# Rahu/Ketu are one axis: always exactly 180 deg apart in RA.
NODES = {"Ketu", "Rahu"}
NODE_AXIS_KEY = "Ketu/Rahu axis"   # target key for RA contacts to either node

# Conjunction family tolerance per mode (degrees)
CONJUNCTION_TOL = {"RA": 1.0, "Dec": 0.125}
# Bodies beyond Pluto: barely move over a subject's lifetime, so a TN 'self'
# conjunction (transit A near natal A) is near-universal - not scored.
SLOW_SELF_NO_CONJUNCTION = {
    "Eris", "Sedna", "Gonggong", "Haumea", "Makemake", "Quaoar", "Orcus", "Transpluto",
}

# Transpluto is a model position, accurate to about +/-0.01 deg (decision D3):
# its RA and Dec are treated as a band of that width in range scoring.
TRANSPLUTO_ERR = 0.01

# Natal Moon moves up to ~16 deg RA and ~5.5 deg Dec in a birth day, more than
# every scoring window, so it is excluded from all natal scoring in both
# coordinates (decisions H5-B and the earlier RA rule). Transit Moon is exact.
NATAL_EXCLUDED = {"Moon"}

# Recurring bodies (C2): race-level top n% by strength, min contacts
RECURRING_TOP_PCT = 2.0
RECURRING_MIN_CONTACTS = 2

# ── Highlight-summary thresholds (Type 1 / Type 2 qualification rules) ────────
T1_MIN_SCORE = 30.0        # a Type 1 pair must have at least one row >= this
T2_MIN_AVG = 30.0          # a Type 2 group qualifies for MAIN if avg(2 scores) >= this
T2_ADDITIONAL_AVG = 30.0   # else qualifies for ADDITIONAL if avg(transit, s1, s2) >= this
DENSE_TRANSIT_THRESHOLD = 90.0  # unlinked-but-dense pairs flagged in ADDITIONAL
SOURCE_CHAIN_MIN = 3       # a body appearing as source in this many+ pairs is a "chain"


# ── Distance helpers ─────────────────────────────────────────────────────────

def angular_sep_ra(ra1: float, ra2: float) -> float:
    diff = abs(ra1 - ra2) % 360
    return diff if diff <= 180 else 360 - diff


def angular_sep_dec(dec1: float, dec2: float) -> float:
    # Dec lies in [-90, +90], so diff never exceeds 180 and the wrap below
    # never triggers. Kept for symmetry with angular_sep_ra.
    diff = abs(dec1 - dec2)
    return diff if diff <= 180 else 360 - diff


# ── Chart loading ────────────────────────────────────────────────────────────

def load_chart(df: pd.DataFrame, allowed_bodies=None) -> Dict[str, Dict[str, float]]:
    """Return {body: {ra, dec}} from a transit_self-style sheet DataFrame.
    allowed_bodies defaults to BODIES if not specified."""
    if allowed_bodies is None:
        allowed_bodies = BODIES
    out = {}
    for _, row in df.iterrows():
        body = str(row["body_A"])
        if body not in allowed_bodies:
            continue
        ra = row["ra_A"]
        dec = row["dec_A"]
        if pd.isna(ra):
            ra = None
        if pd.isna(dec):
            dec = None
        out[body] = {"ra": ra, "dec": dec}
    return out


def load_fixed_stars(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """Load extended fixed-star positions from a chart sheet.
    Chart files store fixed stars with a '_B' suffix (e.g. 'Aldebaran_B').
    Returns {star_name_without_suffix: {ra, dec}}."""
    out = {}
    for _, row in df.iterrows():
        body = str(row["body_A"])
        # Match _B suffix: strip it and check against our extended list
        if body.endswith("_B"):
            name = body[:-2]  # strip '_B'
            if name in FIXED_STARS_EXTENDED_SET:
                ra = row["ra_A"]
                dec = row["dec_A"]
                if pd.isna(ra): ra = None
                if pd.isna(dec): dec = None
                out[name] = {"ra": ra, "dec": dec}
    return out


# ── Fixed-star scoring pass ──────────────────────────────────────────────────

def compute_fs_hits(fs_chart: Dict, planet_chart: Dict,
                    planets_are_natal: bool, layer: str) -> List[dict]:
    """
    Compute distances between every fixed star and every non-star body.
    Both RA and Dec are scored against all 7 vibration families.
    Returns list of hit dicts sorted by score descending.

    fs_chart          : {star_name: {ra, dec}}  - fixed star positions
    planet_chart      : {body_name: {ra, dec}}  - natal or transit positions
                        (may contain stars; star-to-star is skipped)
    planets_are_natal : True if planet_chart is a NATAL chart. Controls the
                        natal Moon exclusion (RA and Dec, H5-B).
    layer             : section label stored on each hit (FS-NN, FS-TN, ...)
    """
    hits = []
    for star, sd in fs_chart.items():
        if sd["ra"] is None or sd["dec"] is None:
            continue
        for body, bd in planet_chart.items():
            # Skip star-to-star: permanent constants (and star vs itself = 0,
            # which scores 100 in the MOD-interval families). Same rule as
            # rank_tt_pairs and gather_chart_hits.
            if body in FIXED_STARS:
                continue
            if bd["ra"] is None or bd["dec"] is None:
                continue
            for coord, sep_fn, sv, bv in (
                ("RA",  angular_sep_ra,  sd["ra"],  bd["ra"]),
                ("Dec", angular_sep_dec, sd["dec"], bd["dec"]),
            ):
                # Natal Moon excluded in both coordinates (H5-B)
                if planets_are_natal and body in NATAL_EXCLUDED:
                    continue
                dist = sep_fn(sv, bv)
                fam_scores = [(name, sc) for name, sc in all_vibrations(dist, coord).items() if sc > 0]
                fam_scores.sort(key=lambda x: -x[1])
                for rank, (family, score) in enumerate(fam_scores):
                    hits.append({
                        "layer":    layer,
                        "star":     star,
                        "body":     body,
                        "coord":    coord,
                        "distance": dist,
                        "family":   family,
                        "score":    score,
                        "fam_rank": rank,
                    })
    hits.sort(key=lambda h: -h["score"])
    return hits


def write_fs_section(ws, r: int, natal_fs: Dict, transit_fs: Dict,
                     natal_planets: Dict, transit_planets: Dict) -> int:
    """
    Write the fixed-star extended analysis section to the subject sheet.
    Four sub-sections:
      FS-NN  : natal fixed stars × natal planets
      FS-TN  : transit fixed stars × natal planets
      FS-TT  : transit fixed stars × transit planets
      FS-NT  : natal fixed stars × transit planets
    Each sub-section lists all hits scored > 0, sorted by score descending,
    then groups them by fixed star for readability.
    """
    ws.cell(row=r, column=1, value="═" * 60)
    r += 1
    ws.cell(row=r, column=1, value="FIXED-STAR EXTENDED ANALYSIS (all 22 stars)")
    ws.cell(row=r, column=1).font = __import__("openpyxl").styles.Font(bold=True)
    r += 1
    ws.cell(row=r, column=1, value="Stars: " + ", ".join(FIXED_STARS_EXTENDED))
    r += 2

    # (title, star chart, planet chart, planets_are_natal, layer)
    sub_sections = [
        ("FS-NN  natal fixed stars × natal planets",
         natal_fs,   natal_planets,   True,  "FS-NN"),
        ("FS-TN  transit fixed stars × natal planets",
         transit_fs, natal_planets,   True,  "FS-TN"),
        ("FS-TT  transit fixed stars × transit planets",
         transit_fs, transit_planets, False, "FS-TT"),
        ("FS-NT  natal fixed stars × transit planets",
         natal_fs,   transit_planets, False, "FS-NT"),
    ]

    for title, fs_chart, planet_chart, planets_are_natal, layer in sub_sections:
        hits = compute_fs_hits(fs_chart, planet_chart, planets_are_natal, layer)
        ws.cell(row=r, column=1, value=f"── {title} ──")
        r += 1

        if not hits:
            ws.cell(row=r, column=1, value="(no hits scored > 0)")
            r += 2
            continue

        # Header
        for col, label in enumerate(
            ["Star", "Body", "Coord", "Distance", "Family", "Score", "Fam Rank"], 1
        ):
            ws.cell(row=r, column=col, value=label)
        r += 1

        # Group by star, write all families per star/body/coord
        current_star = None
        for h in hits:
            if h["star"] != current_star:
                current_star = h["star"]
                ws.cell(row=r, column=1, value=current_star)
            ws.cell(row=r, column=2, value=h["body"])
            ws.cell(row=r, column=3, value=h["coord"])
            ws.cell(row=r, column=4, value=round(h["distance"], 6))
            ws.cell(row=r, column=5, value=h["family"])
            ws.cell(row=r, column=6, value=round(h["score"], 2))
            ws.cell(row=r, column=7, value=h["fam_rank"])
            r += 1
        r += 1

    return r


# ── Scoring: the six "vibration" families ───────────────────────────────────

PHI    = (1.0 + math.sqrt(5)) / 2.0
SQRT2  = math.sqrt(2.0)
SILVER = 1.0 + SQRT2


def score_whole(v: float) -> float:
    """Whole numbers 1-200, tol 0.02, squared, no decay."""
    if not (1.0 <= v <= 200.0):
        return 0.0
    dev = abs(v - round(v))
    if dev >= 0.02:
        return 0.0
    return (10.0 * (0.02 - dev) / 0.02) ** 2


def score_phi_interval(v: float) -> float:
    """Golden ratio as a repeating interval (MOD phi), tol 0.03236, squared."""
    tol = 0.03236
    if round(v / PHI) < 1:      # zero multiple not scored (Conjunction covers it)
        return 0.0
    m = v % PHI
    dev = min(m, PHI - m)
    if dev >= tol:
        return 0.0
    return (10.0 * (tol - dev) / tol) ** 2


_PHI_POWER_TARGETS = (
    [PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] +
    [10.0 * PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7)] +
    [100.0 * PHI ** p for p in (-1, 1)]
)


def score_phi_powers(v: float) -> float:
    """Golden ratio powers (and 10x/100x scaled), relative tol, squared."""
    best = 0.0
    for t in _PHI_POWER_TARGETS:
        tol = max(t * 0.005, 0.025)
        dev = abs(v - t)
        if dev <= tol:
            s = (10.0 * (tol - dev) / tol) ** 2
            if s > best:
                best = s
    return best


# Repeating-ninths family: (lower, upper, tol, target) — transcribed exactly
# from the source formulas, including the asymmetric bounds as given.
_NINTH_RANGES = [
    (0.1105, 0.112,  0.000611, 0.111111),
    (0.2215, 0.223,  0.000722, 0.222222),
    (0.3325, 0.334,  0.000833, 0.333333),
    (0.4435, 0.445,  0.000944, 0.444444),
    (0.5545, 0.556,  0.001056, 0.555556),
    (0.6655, 0.667,  0.001167, 0.666667),
    (0.7765, 0.778,  0.001278, 0.777778),
    (0.8875, 0.889,  0.001389, 0.888889),
    (0.9985, 1.0,    0.0015,   0.999999),
    (1.105,  1.12,   0.006111, 1.111111),
    (2.215,  2.23,   0.007222, 2.222222),
    (3.325,  3.34,   0.008333, 3.333333),
    (4.435,  4.45,   0.009444, 4.444444),
    (5.545,  5.56,   0.010556, 5.555556),
    (6.655,  6.67,   0.011667, 6.666667),
    (7.765,  7.78,   0.012778, 7.777778),
    (8.875,  8.89,   0.013889, 8.888889),
    (9.985,  10.0,   0.015,    9.999999),
    (11.05,  11.2,   0.061111, 11.111111),
    (22.15,  22.3,   0.072222, 22.222222),
    (33.25,  33.4,   0.083333, 33.333333),
    (44.35,  44.5,   0.094444, 44.444444),
    (55.45,  55.6,   0.105556, 55.555556),
    (66.55,  66.7,   0.116667, 66.666667),
    (77.65,  77.8,   0.127778, 77.777778),
    (88.75,  88.9,   0.138889, 88.888889),
    (99.85,  100.0,  0.15,     99.999999),
    (110.5,  112.0,  0.611111, 111.111111),
    # "teens" extension
    (1.215,  1.23,   0.007222, 1.222222),
    (1.325,  1.34,   0.008333, 1.333333),
    (1.435,  1.45,   0.009444, 1.444444),
    (1.545,  1.56,   0.010556, 1.555556),
    (1.655,  1.67,   0.011667, 1.666667),
    (1.765,  1.78,   0.012778, 1.777778),
    (1.875,  1.89,   0.013889, 1.888889),
    (12.15,  12.3,   0.072222, 12.222222),
    (13.25,  13.4,   0.083333, 13.333333),
    (14.35,  14.5,   0.094444, 14.444444),
    (15.45,  15.6,   0.105556, 15.555556),
    (16.55,  16.7,   0.116667, 16.666667),
    (17.65,  17.8,   0.127778, 17.777778),
    (18.75,  18.9,   0.138889, 18.888889),
    (121.5,  123.0,  0.722222, 122.222222),
    (132.5,  134.0,  0.833333, 133.333333),
    (143.5,  145.0,  0.944444, 144.444444),
    (154.5,  156.0,  1.055556, 155.555556),
    (165.5,  167.0,  1.166667, 166.666667),
    (176.5,  178.0,  1.277778, 177.777778),
]


def score_ninth(v: float) -> float:
    """Repeating-ninths family — linear scoring, exact asymmetric bounds."""
    for lo, hi, tol, target in _NINTH_RANGES:
        if lo <= v < hi:
            return max(0.0, 100.0 * (tol - abs(v - target)) / tol)
    return 0.0


def score_sqrt2(v: float) -> float:
    """sqrt(2) as repeating interval (tol 0.02828) plus 10x/100x targets."""
    tol_mod = 0.02828
    m = v % SQRT2
    dev = min(m, SQRT2 - m)
    best = 0.0
    if round(v / SQRT2) >= 1 and dev < tol_mod:   # zero multiple not scored
        best = (10.0 * (tol_mod - dev) / tol_mod) ** 2
    for t in (10.0 * SQRT2, 100.0 * SQRT2):
        tol = max(t * 0.005, 0.025)
        d = abs(v - t)
        if d <= tol:
            s = (10.0 * (tol - d) / tol) ** 2
            if s > best:
                best = s
    return best


def score_silver(v: float) -> float:
    """Silver ratio (1+sqrt2) as repeating interval (tol 0.04828) plus 10x target."""
    tol_mod = 0.04828
    m = v % SILVER
    dev = min(m, SILVER - m)
    best = 0.0
    if round(v / SILVER) >= 1 and dev < tol_mod:  # zero multiple not scored
        best = (10.0 * (tol_mod - dev) / tol_mod) ** 2
    t = 10.0 * SILVER
    tol = max(t * 0.005, 0.025)
    d = abs(v - t)
    if d <= tol:
        s = (10.0 * (tol - d) / tol) ** 2
        if s > best:
            best = s
    return best


def score_conjunction(v: float, mode: str) -> float:
    """Conjunction (distance near 0) - squared, tolerance depends on mode."""
    tol = CONJUNCTION_TOL[mode]
    if v >= tol:
        return 0.0
    return (10.0 * (tol - v) / tol) ** 2


# Every family function is called as fn(value, mode). Only Conjunction uses
# mode; the others are mode-independent. Conjunction is appended LAST so the
# order (and columns/rows) of the original six families is unchanged.
VIBRATION_FAMILIES = [
    ("Whole Number",  lambda v, mode: score_whole(v)),
    ("Golden Ratio",  lambda v, mode: score_phi_interval(v)),
    ("Phi Powers",    lambda v, mode: score_phi_powers(v)),
    ("Ninths",        lambda v, mode: score_ninth(v)),
    ("Sqrt2",         lambda v, mode: score_sqrt2(v)),
    ("Silver Ratio",  lambda v, mode: score_silver(v)),
    ("Conjunction",   score_conjunction),
]


def best_vibration(v: Optional[float], mode: str) -> Tuple[float, Optional[str]]:
    """Return (best_score, family_name) across all 7 families for a value.
    mode is 'RA' or 'Dec'."""
    if v is None:
        return 0.0, None
    best_score = 0.0
    best_family = None
    for name, fn in VIBRATION_FAMILIES:
        s = fn(v, mode)
        if s > best_score:
            best_score = s
            best_family = name
    return best_score, best_family


def all_vibrations(v: Optional[float], mode: str) -> Dict[str, float]:
    """Return {family_name: score} for all 7 families for a value.
    mode is 'RA' or 'Dec' (required - Conjunction tolerance depends on it)."""
    if v is None:
        return {name: 0.0 for name, _ in VIBRATION_FAMILIES}
    return {name: fn(v, mode) for name, fn in VIBRATION_FAMILIES}


# ── Transit-transit pair ranking ─────────────────────────────────────────────

def rank_tt_pairs(tr: Dict) -> List[dict]:
    """
    For every pair of the 52 transit bodies (BODIES_TRANSIT), compute RA and
    Dec transit distances,
    score against all 6 families, and record the best (mode, family, score).
    Returns list of dicts, sorted by best score descending.
    Fixed-star-to-fixed-star pairs are skipped — their distances are permanent
    constants that carry no race-specific information.
    """
    results = []
    for a, b in itertools.combinations(BODIES_TRANSIT, 2):
        # Skip fixed-star-to-fixed-star pairs
        if a in FIXED_STARS and b in FIXED_STARS:
            continue
        da, db = tr.get(a), tr.get(b)
        if da is None or db is None:
            continue
        if da["ra"] is None or db["ra"] is None or da["dec"] is None or db["dec"] is None:
            continue

        ra_dist  = angular_sep_ra(da["ra"], db["ra"])
        dec_dist = angular_sep_dec(da["dec"], db["dec"])

        ra_vibs  = all_vibrations(ra_dist, "RA")
        dec_vibs = all_vibrations(dec_dist, "Dec")
        # C5a: Ketu/Rahu are always exactly 180 deg apart in RA - an artifact,
        # not a race-specific signal. Score this pair on Dec only.
        if {a, b} == NODES:
            ra_vibs = {name: 0.0 for name in ra_vibs}

        # Best score per family (max of RA/Dec), and per-mode scores
        family_best = {}
        family_ra = {}
        family_dec = {}
        for name, _ in VIBRATION_FAMILIES:
            family_best[name] = max(ra_vibs[name], dec_vibs[name])
            family_ra[name] = ra_vibs[name]
            family_dec[name] = dec_vibs[name]

        overall_best = 0.0
        overall_family = None
        overall_mode = None
        for name, _ in VIBRATION_FAMILIES:
            if ra_vibs[name] > overall_best:
                overall_best, overall_family, overall_mode = ra_vibs[name], name, "RA"
            if dec_vibs[name] > overall_best:
                overall_best, overall_family, overall_mode = dec_vibs[name], name, "Dec"

        # Best score in RA across all families, best in Dec across all families
        ra_best = max(ra_vibs.values()) if ra_vibs else 0.0
        dec_best = max(dec_vibs.values()) if dec_vibs else 0.0

        results.append({
            "pair": (a, b),
            "ra_dist": ra_dist,
            "dec_dist": dec_dist,
            "family_best": family_best,
            "family_ra": family_ra,
            "family_dec": family_dec,
            "ra_best": ra_best,
            "dec_best": dec_best,
            "overall_best": overall_best,
            "overall_family": overall_family,
            "overall_mode": overall_mode,
        })

    results.sort(key=lambda r: r["overall_best"], reverse=True)
    return results


# ── NN / TN hit detection for a qualifying pair ──────────────────────────────

def skip_distance(from_body: str, to_body: str, mode: str, same_chart: bool) -> bool:
    """Distances never scored (shared by the P-tab hits and the HITS sheet).
    NN node<->node RA is the fixed 180 deg axis (C5b). Natal Moon is excluded
    in RA and Dec (H5-B): in NN both sides are natal, in TN only the target."""
    if same_chart and mode == "RA" and {from_body, to_body} == NODES:
        return True
    if same_chart and (from_body in NATAL_EXCLUDED or to_body in NATAL_EXCLUDED):
        return True
    if not same_chart and to_body in NATAL_EXCLUDED:
        return True
    return False


def collapse_tn_node_axis(rows: List[dict], score_of) -> List[dict]:
    """C5c-B. In TN, RA only, transit node -> natal node is ONE axis contact:
      - self twins (Rahu->Rahu, Ketu->Ketu) are the same distance: keep the
        Rahu->Rahu row (Ketu->Ketu only if Rahu is absent);
      - mirror twins (Rahu->Ketu, Ketu->Rahu) are the same distance, 180 - d
        of the self row: keep the Rahu->Ketu row (Ketu->Rahu if absent);
      - the kept mirror row keeps only families the self row does not
        already score (score_of(row) > 0). Dec is untouched.
    Applies whether the mirror row is labelled 'cross' (both nodes in the
    pair) or 'convergence' (one node in the pair). Rows are dicts with
    'from', 'to', 'mode', 'family'."""
    def axis(r):
        return r["mode"] == "RA" and r["from"] in NODES and r["to"] in NODES
    ax = [r for r in rows if axis(r)]
    if not ax:
        return rows
    drop = set()
    selfs = [r for r in ax if r["from"] == r["to"]]
    mirrors = [r for r in ax if r["from"] != r["to"]]
    if any(r["from"] == "Rahu" for r in selfs):
        drop.update(id(r) for r in selfs if r["from"] == "Ketu")
    if any(r["from"] == "Rahu" for r in mirrors):
        drop.update(id(r) for r in mirrors if r["from"] == "Ketu")
    self_fams = {r["family"] for r in selfs if id(r) not in drop and score_of(r) > 0}
    drop.update(id(r) for r in mirrors if r["family"] in self_fams)
    return [r for r in rows if id(r) not in drop]


def gather_chart_hits(chart1: Dict, chart2: Dict, a: str, b: str,
                       same_chart: bool) -> Tuple[List[dict], Dict[str, int]]:
    """
    Compute hits between chart1 bodies {a,b} and chart2 bodies (all 48 in
    BODIES). Rows are skipped where either side lacks RA or Dec (this is
    what excludes 'equator').

    If same_chart is True (NN case): chart1 == chart2, skip self-distances
    (A vs A) since they are always zero/degenerate; the direct A-B distance
    is recorded as a "direct" hit; A-X / B-X (X != A,B) are "convergence"
    candidates.

    If same_chart is False (TN case): chart1=transit, chart2=natal;
    A->A, B->B are "self"; A->B, B->A are "cross"; A->X, B->X (X!=A,B)
    are "convergence" candidates.

    Returns (list_of_hit_rows, tally_dict) where tally counts how many
    times each chart2 body appears in a scored (score>0) hit row.

    Rules applied here:
      - NN node<->node RA rows dropped (always exactly 180 deg)           C5b
      - TN node<->node RA: one axis contact with the self row             C5c-B
      - natal Moon excluded in RA and Dec                                 H5-B
      - no Conjunction on TN 'self' rows for SLOW_SELF_NO_CONJUNCTION     C1
      - RA node-axis duplicates removed per family (_dedupe_node_axis)     C5d
    """
    hits = []

    def record(relation: str, from_body: str, to_body: str):
        d1 = chart1.get(from_body)
        d2 = chart2.get(to_body)
        if d1 is None or d2 is None:
            return
        if d1["ra"] is None or d2["ra"] is None or d1["dec"] is None or d2["dec"] is None:
            return
        # Fixed stars barely move — transit fixed star as SOURCE in TN mode is
        # near-constant and carries no race-specific signal. Skip it.
        # Natal fixed star as TARGET is meaningful — do NOT skip it.
        if not same_chart and from_body in FIXED_STARS:
            return
        # Skip fixed-star-to-fixed-star: permanent constants, no race-specific signal
        if from_body in FIXED_STARS and to_body in FIXED_STARS:
            return
        ra_dist  = angular_sep_ra(d1["ra"], d2["ra"])
        dec_dist = angular_sep_dec(d1["dec"], d2["dec"])
        for mode, dist in (("RA", ra_dist), ("Dec", dec_dist)):
            if skip_distance(from_body, to_body, mode, same_chart):
                continue
            # Emit one row per scoring family, not just the highest. A value
            # can satisfy several families independently (e.g. 17.7846 is both
            # Ninths 94.66 and Golden Ratio 32.99); best_vibration() discarded
            # everything but the winner.
            fam_scores = [(name, sc) for name, sc in all_vibrations(dist, mode).items() if sc > 0]
            # C1: slow bodies sit near their own natal position for years -
            # a TN self conjunction is near-universal, so not scored.
            if relation == "self" and not same_chart and from_body in SLOW_SELF_NO_CONJUNCTION:
                fam_scores = [(n, sc) for n, sc in fam_scores if n != "Conjunction"]
            fam_scores.sort(key=lambda x: -x[1])
            for rank, (family, score) in enumerate(fam_scores):
                hits.append({
                    "relation": relation,
                    "from": from_body,
                    "to": to_body,
                    "mode": mode,
                    "distance": dist,
                    "family": family,
                    "score": score,
                    "fam_rank": rank,                 # 0 = highest-scoring family
                    "fam_count": len(fam_scores),     # >1 marks a multi-family hit
                })

    if same_chart:
        # Direct A-B natal distance
        record("direct", a, b)
        # Convergence candidates: A-X and B-X for every other body X
        for x in BODIES:
            if x in (a, b):
                continue
            record("convergence", a, x)
            record("convergence", b, x)
    else:
        # Self
        record("self", a, a)
        record("self", b, b)
        # Cross
        record("cross", a, b)
        record("cross", b, a)
        # Convergence candidates
        for x in BODIES:
            if x in (a, b):
                continue
            record("convergence", a, x)
            record("convergence", b, x)

    if not same_chart:
        hits = collapse_tn_node_axis(hits, lambda h: h["score"])
    hits = _dedupe_node_axis(hits)

    # Re-number family rank/count per distance after de-duplication
    by_dist: Dict[Tuple[str, str, str, str], List[dict]] = {}
    for h in hits:
        by_dist.setdefault((h["relation"], h["from"], h["to"], h["mode"]), []).append(h)
    for rows in by_dist.values():
        rows.sort(key=lambda x: -x["score"])
        for rank, h in enumerate(rows):
            h["fam_rank"] = rank
            h["fam_count"] = len(rows)

    tally: Dict[str, int] = {}
    for h in hits:
        tally[h["to"]] = tally.get(h["to"], 0) + 1
    return hits, tally


def _target_key(h: dict) -> str:
    """Target identity for matching/grouping: in RA, Ketu and Rahu are one
    axis target; in Dec they remain separate bodies."""
    if h["mode"] == "RA" and h["to"] in NODES:
        return NODE_AXIS_KEY
    return h["to"]


_T1_RELATIONS = ("self", "direct", "cross")


def _node_pick_key(h: dict):
    """Preference when two same-family rows describe one node-axis contact:
    higher score, then a Type 1 relation, then the Rahu label."""
    return (h["score"], h["relation"] in _T1_RELATIONS, h["to"] == "Rahu" or h["from"] == "Rahu")


def _dedupe_node_axis(hits: List[dict]) -> List[dict]:
    """C5d: in RA, X->Ketu at d is always mirrored by X->Rahu at 180-d (and,
    for the Ketu/Rahu pair, Ketu->X mirrors Rahu->X). Where the SAME family
    scores on both sides, keep one row. Families scoring on only one side are
    all kept, labelled with the node they came from."""
    drop = set()
    target_side: Dict[Tuple[str, str], List[dict]] = {}
    source_side: Dict[Tuple[str, str], List[dict]] = {}
    for h in hits:
        if h["mode"] != "RA":
            continue
        if h["to"] in NODES and h["from"] not in NODES:
            target_side.setdefault((h["from"], h["family"]), []).append(h)
        elif h["from"] in NODES and h["to"] not in NODES:
            source_side.setdefault((h["to"], h["family"]), []).append(h)
    for groups, side in ((target_side, "to"), (source_side, "from")):
        for rows in groups.values():
            if len({r[side] for r in rows}) < 2:
                continue            # family scored on one node only - keep
            keep = max(rows, key=_node_pick_key)
            for r in rows:
                if r is not keep:
                    drop.add(id(r))
    return [h for h in hits if id(h) not in drop]


def mark_convergence_matches(hits: List[dict]) -> None:
    """
    C3: MATCH is flagged on CONVERGENCE rows only - two rows from different
    pair members hitting the same target (node axis = one target in RA), in
    the same mode and family.

    TN self + cross rows hitting the same natal body in the same mode and
    family (both transit bodies hit the pair's own natal body) are noted
    'BOTH'. They already score in full as Type 1, so 'BOTH' adds no score
    and is never treated as a Type 2 MATCH.

    Adds 'match' ('MATCH' / 'BOTH' / None) and 'match_partner' to each hit.
    """
    for h in hits:
        h["match"] = None
        h["match_partner"] = None
    for relations, label in ((("convergence",), "MATCH"), (("self", "cross"), "BOTH")):
        groups: Dict[Tuple[str, str, str], List[dict]] = {}
        for h in hits:
            if h["relation"] in relations:
                groups.setdefault((_target_key(h), h["mode"], h["family"]), []).append(h)
        for group in groups.values():
            for h in group:
                partners = [g for g in group if g["from"] != h["from"]]
                if partners:
                    h["match"] = label
                    h["match_partner"] = partners[0]["from"]


# ── Highlight summary: Type 1 / Type 2 extraction, linking, source chains ─────
#
# This section implements the "what to highlight" rules worked out by hand
# against many real charts:
#   - Type 1 = self/direct/cross rows. A pair qualifies if it has 2+ such
#     rows, OR the transit-transit pair score is >= 80; and at least one row
#     must score >= T1_MIN_SCORE. Once qualified, every row above zero is
#     kept for display.
#   - Type 2 = matched convergence pairs (mark_convergence_matches already
#     groups these by (to, mode, family)). A group qualifies for the MAIN
#     summary if the average of its two scores is >= T2_MIN_AVG; if not, it
#     still qualifies for the ADDITIONAL summary if the average of the
#     transit score and both convergence scores is >= T2_ADDITIONAL_AVG.
#   - "Bonus" rows: once a genuine matched group exists for a target, any
#     OTHER convergence row (matched or not) in the same pair block sharing
#     one of that group's two source bodies and the same target is folded
#     into that group as extra context, not scored as its own group.
#   - Linking (required for MAIN, both types): Type 1 links via a body
#     recurring across two qualifying pairs (by body identity, not exact
#     value), OR the same body/pair appearing in both RA and Dec within one
#     pair, OR in both NN and TN within one pair. Type 2 links via the same
#     SOURCE body (one of the pair's own two named bodies) recurring across
#     two different pairs' matched groups - tracked completely separately
#     from Type 1 recurrence.
#   - The Ketu/Rahu pair is a single axis, not two bodies: the flat RA=180
#     direct row is dropped outright, and any RA self/cross row that is
#     merely the Ketu-labelled mirror of the same Rahu-labelled row (same
#     relation, family, distance) is counted once. Dec is never touched.
#     What remains is then judged by the ordinary rules above - there is no
#     automatic inclusion for this pair.

def _is_ketu_rahu(a: str, b: str) -> bool:
    return {a, b} == {"Ketu", "Rahu"}


def _adjust_ketu_rahu_hits(hits: List[dict]) -> List[dict]:
    """Strip the flat 180 RA axis artifact and collapse its RA self/cross
    mirrors to one row each. Only ever called for the Ketu/Rahu pair."""
    out = []
    seen_ra_mirror = set()
    for h in hits:
        if h["mode"] == "RA" and h["relation"] in ("self", "direct", "cross") \
                and h["from"] in ("Ketu", "Rahu") and h["to"] in ("Ketu", "Rahu"):
            if h["relation"] == "direct" and abs(h["distance"] - 180.0) < 0.01:
                continue  # the axis artifact itself
            key = (h["relation"], h["family"], round(h["distance"], 4), round(h["score"], 2))
            if key in seen_ra_mirror:
                continue  # this is the Ketu<->Rahu mirror of a row already kept
            seen_ra_mirror.add(key)
        out.append(h)
    return out


def _type1_rows(nn_hits: List[dict], tn_hits: List[dict]) -> List[Tuple[dict, str]]:
    return [(h, "NN") for h in nn_hits if h["relation"] in ("self", "direct", "cross")] + \
           [(h, "TN") for h in tn_hits if h["relation"] in ("self", "direct", "cross")]


def _type1_gate(rows: List[Tuple[dict, str]], transit_score: float) -> bool:
    if not rows:
        return False
    if max(h["score"] for h, _ in rows) < T1_MIN_SCORE:
        return False
    return len(rows) >= 2 or transit_score >= TT_THRESHOLD


def _body_pair_key(h: dict) -> Tuple[str, str]:
    return tuple(sorted((h["from"], h["to"])))


def _type1_internal_link(rows: List[Tuple[dict, str]]) -> bool:
    """RA+Dec or NN+TN repetition of the same body/body-pair within one pair."""
    by_body_pair: Dict[Tuple[str, str], Dict[str, set]] = {}
    for h, src in rows:
        key = _body_pair_key(h)
        entry = by_body_pair.setdefault(key, {"modes": set(), "sources": set()})
        entry["modes"].add(h["mode"])
        entry["sources"].add(src)
    for entry in by_body_pair.values():
        if len(entry["modes"]) >= 2 or len(entry["sources"]) >= 2:
            return True
    return False


def _type1_bodies_involved(rows: List[Tuple[dict, str]]) -> set:
    bodies = set()
    for h, _ in rows:
        bodies.add(h["from"])
        bodies.add(h["to"])
    return bodies


def _type2_groups(nn_hits: List[dict], tn_hits: List[dict]) -> List[dict]:
    """Genuine matched convergence groups (2 rows sharing to/mode/family),
    plus any bonus rows sharing a source+target with an existing group."""
    groups = []
    for section, hits in (("NN", nn_hits), ("TN", tn_hits)):
        by_key: Dict[Tuple[str, str, str], List[dict]] = {}
        for h in hits:
            if h["relation"] == "convergence":
                by_key.setdefault((_target_key(h), h["mode"], h["family"]), []).append(h)
        for (to_key, mode, family), members in by_key.items():
            matched = [h for h in members if h.get("match") == "MATCH"]
            if len(matched) >= 2:
                seen_from = {}
                for h in matched:
                    seen_from.setdefault(h["from"], h)
                pair_rows = list(seen_from.values())[:2]
                if len(pair_rows) == 2:
                    groups.append({
                        "section": section, "to": pair_rows[0]["to"], "to_key": to_key,
                        "mode": mode, "family": family,
                        "rows": pair_rows,
                        "sources": {pair_rows[0]["from"], pair_rows[1]["from"]},
                        "bonus": [],
                    })

    used_ids = {id(r) for g in groups for r in g["rows"]}
    tagged_conv = [(h, "NN") for h in nn_hits if h["relation"] == "convergence"] + \
                  [(h, "TN") for h in tn_hits if h["relation"] == "convergence"]
    for g in groups:
        for h, section in tagged_conv:
            if id(h) in used_ids:
                continue
            same_target = h["to"] == g["to"] or _target_key(h) == g["to_key"]
            if same_target and h["from"] in g["sources"]:
                h["_bonus_section"] = section
                g["bonus"].append(h)
                used_ids.add(id(h))
    return groups


def _type2_group_score(g: dict, transit_score: float) -> Tuple[bool, bool]:
    """Returns (qualifies_main, qualifies_additional)."""
    s1, s2 = g["rows"][0]["score"], g["rows"][1]["score"]
    avg2 = (s1 + s2) / 2.0
    if avg2 >= T2_MIN_AVG:
        return True, False
    avg3 = (transit_score + s1 + s2) / 3.0
    return False, avg3 >= T2_ADDITIONAL_AVG


def _type1_internal_link_bodies(rows: List[Tuple[dict, str]]) -> set:
    """Bodies belonging to a body-pair that repeats across RA+Dec or
    NN+TN within one pair (the internal-link condition)."""
    by_body_pair: Dict[Tuple[str, str], Dict[str, set]] = {}
    for h, src in rows:
        key = _body_pair_key(h)
        entry = by_body_pair.setdefault(key, {"modes": set(), "sources": set()})
        entry["modes"].add(h["mode"])
        entry["sources"].add(src)
    bodies = set()
    for key, entry in by_body_pair.items():
        if len(entry["modes"]) >= 2 or len(entry["sources"]) >= 2:
            bodies.update(key)
    return bodies


def build_pair_highlights(pair_results: List[dict]) -> dict:
    """
    Walks every qualifying pair for one subject and classifies its content
    into MAIN (qualifies + linked), ADDITIONAL (fails linking, or fails the
    strict Type 2 average but clears the 3-way one, or is dense/high-transit
    but unlinked), and per-body source chains (3+ pairs).
    """
    per_pair = []
    for pr in pair_results:
        a, b = pr["a"], pr["b"]
        transit_score = pr["p"]["overall_best"]
        family_best = pr["p"]["family_best"]
        pair_label = f"{a} / {b}"
        nn_hits, tn_hits = pr["nn_hits"], pr["tn_hits"]
        if _is_ketu_rahu(a, b):
            nn_hits = _adjust_ketu_rahu_hits(nn_hits)
            tn_hits = _adjust_ketu_rahu_hits(tn_hits)

        t1_rows = _type1_rows(nn_hits, tn_hits)
        t1_gate = _type1_gate(t1_rows, transit_score)
        t1_gate_reasons = []
        if t1_gate:
            if len(t1_rows) >= 2:
                t1_gate_reasons.append("2+ Type 1 rows")
            if transit_score >= TT_THRESHOLD:
                t1_gate_reasons.append(f"transit score >= {TT_THRESHOLD:.0f}")
        t1_internal_bodies = _type1_internal_link_bodies(t1_rows) if t1_gate else set()
        t1_bodies = _type1_bodies_involved(t1_rows) if t1_gate else set()
        t1_display = sorted([(h, src) for h, src in t1_rows if h["score"] > 0], key=lambda x: -x[0]["score"]) if t1_gate else []

        t2_groups = _type2_groups(nn_hits, tn_hits)
        t2_main, t2_additional = [], []
        for g in t2_groups:
            main_ok, add_ok = _type2_group_score(g, transit_score)
            if main_ok:
                t2_main.append(g)
            elif add_ok:
                t2_additional.append(g)

        per_pair.append({
            "pair": pair_label, "a": a, "b": b, "transit_score": transit_score,
            "family_best": family_best,
            "family_ra": pr["p"].get("family_ra", family_best),
            "family_dec": pr["p"].get("family_dec", family_best),
            "ra_dist": pr["p"]["ra_dist"], "dec_dist": pr["p"]["dec_dist"],
            "ra_best": pr["p"].get("ra_best", 0.0), "dec_best": pr["p"].get("dec_best", 0.0),
            "t1_gate": t1_gate, "t1_gate_reasons": t1_gate_reasons,
            "t1_internal_bodies": t1_internal_bodies,
            "t1_bodies": t1_bodies, "t1_display": t1_display,
            "t2_main": t2_main, "t2_additional": t2_additional,
            "t2_source_bodies": {a, b} if (t2_main or t2_additional) else set(),
        })

    # Second pass: cross-pair linking (body must recur in ANOTHER pair's
    # gated Type1 content, or as a Type2 source in another pair's matched
    # group - tracked as two independent maps)
    t1_body_pairs: Dict[str, set] = {}
    t2_source_pairs: Dict[str, set] = {}
    for pp in per_pair:
        if pp["t1_gate"]:
            for body in pp["t1_bodies"]:
                t1_body_pairs.setdefault(body, set()).add(pp["pair"])
        if pp["t2_main"] or pp["t2_additional"]:
            for body in pp["t2_source_bodies"]:
                t2_source_pairs.setdefault(body, set()).add(pp["pair"])

    main_entries, additional_entries = [], []
    for pp in per_pair:
        t1_cross_bodies = {body for body in pp["t1_bodies"]
                            if len(t1_body_pairs.get(body, set())) >= 2}
        t1_link_bodies = sorted(t1_cross_bodies | pp["t1_internal_bodies"])
        t1_linked = pp["t1_gate"] and bool(t1_link_bodies)

        t1_rule = ""
        if t1_linked:
            reason_bits = list(pp["t1_gate_reasons"])
            link_bits = []
            if t1_cross_bodies:
                link_bits.append(f"cross-pair recurrence ({', '.join(sorted(t1_cross_bodies))})")
            if pp["t1_internal_bodies"]:
                link_bits.append(f"RA/Dec or NN/TN repeat ({', '.join(sorted(pp['t1_internal_bodies']))})")
            t1_rule = f"Type 1: {' + '.join(reason_bits)}; linked via {' and '.join(link_bits)}"

        def _t2_link_bodies(g):
            return sorted(s for s in g["sources"] if len(t2_source_pairs.get(s, set())) >= 2)

        t2_linked_main = []
        for g in pp["t2_main"]:
            lb = _t2_link_bodies(g)
            if lb:
                g["_link_bodies"] = lb
                g["_rule"] = f"Type 2: main avg >= {T2_MIN_AVG:.0f}; linked via source recurrence ({', '.join(lb)})"
                t2_linked_main.append(g)
        t2_unlinked_main = [g for g in pp["t2_main"] if g not in t2_linked_main]

        if t1_linked or t2_linked_main:
            main_entries.append({
                "pair": pp["pair"], "transit_score": pp["transit_score"],
                "family_best": pp["family_best"],
                "family_ra": pp["family_ra"], "family_dec": pp["family_dec"],
                "ra_dist": pp["ra_dist"], "dec_dist": pp["dec_dist"],
                "ra_best": pp["ra_best"], "dec_best": pp["dec_best"],
                "t1_rows": pp["t1_display"] if t1_linked else [],
                "t1_rule": t1_rule, "t1_link_bodies": t1_link_bodies if t1_linked else [],
                "t2_groups": t2_linked_main,
            })

        # Anything that qualified its own gate but didn't link goes to
        # ADDITIONAL if the pair is dense/high-scoring; genuine T2-additional
        # groups always go to ADDITIONAL regardless of linking.
        extra_t1 = pp["t1_display"] if (pp["t1_gate"] and not t1_linked
                                         and pp["transit_score"] >= DENSE_TRANSIT_THRESHOLD) else []
        extra_t1_rule = (f"Type 1: {' + '.join(pp['t1_gate_reasons'])}; unlinked, "
                          f"kept as dense/high-transit (score >= {DENSE_TRANSIT_THRESHOLD:.0f})") if extra_t1 else ""

        for g in pp["t2_additional"]:
            lb = _t2_link_bodies(g)
            g["_link_bodies"] = lb
            g["_rule"] = (f"Type 2: additional (3-way avg >= {T2_ADDITIONAL_AVG:.0f})"
                           + (f"; linked via source recurrence ({', '.join(lb)})" if lb else "; unlinked"))
        for g in t2_unlinked_main:
            g["_link_bodies"] = []
            g["_rule"] = f"Type 2: main avg >= {T2_MIN_AVG:.0f}, but unlinked (no recurring source)"

        extra_t2 = pp["t2_additional"] + t2_unlinked_main
        if extra_t1 or extra_t2:
            additional_entries.append({
                "pair": pp["pair"], "transit_score": pp["transit_score"],
                "family_best": pp["family_best"],
                "family_ra": pp["family_ra"], "family_dec": pp["family_dec"],
                "ra_dist": pp["ra_dist"], "dec_dist": pp["dec_dist"],
                "ra_best": pp["ra_best"], "dec_best": pp["dec_best"],
                "t1_rows": extra_t1, "t1_rule": extra_t1_rule, "t1_link_bodies": [],
                "t2_groups": extra_t2,
            })

    source_chains = []
    for body, pairs in t1_body_pairs.items():
        if len(pairs) >= SOURCE_CHAIN_MIN:
            source_chains.append({"body": body, "type": "Type 1", "pairs": sorted(pairs)})
    for body, pairs in t2_source_pairs.items():
        if len(pairs) >= SOURCE_CHAIN_MIN:
            source_chains.append({"body": body, "type": "Type 2", "pairs": sorted(pairs)})

    return {"main": main_entries, "additional": additional_entries, "source_chains": source_chains}


HL_COL_START_T1_RAW = 14                                        # column N - past Rule(11)/Linking Body(12), 1 gap
HL_GAP = 1
HL_COL_START_T2_RAW = HL_COL_START_T1_RAW + len(BODIES) + HL_GAP  # T2 raw
HL_COL_START_T1_TT = HL_COL_START_T2_RAW + len(BODIES) + HL_GAP   # T1 score + transit
HL_COL_START_T2_TT = HL_COL_START_T1_TT + len(BODIES) + HL_GAP    # T2 score + transit


def write_highlight_block(ws, r: int, title: str, entries: List[dict]) -> Tuple[int, Optional[int], List[List[float]], Dict[str, Tuple[int, int]]]:
    """Renders MAIN or ADDITIONAL summary entries, grouped per pair by
    NN/TN then by vibration family. Every row carries its own NN/TN tag,
    the pair's per-family transit score, the rule that admitted it, and
    every linking body found. Four 48-wide (len(BODIES)) score-by-body blocks (raw and
    +transit, for Type 1 and Type 2 separately) sit at the section top,
    each with its own sum row. Returns (next_row, sum_row, totals,
    pair_row_ranges):
      sum_row         None if there were no entries to summarise
      totals          [t1_raw, t2_raw, t1_tt, t2_tt], each a per-body list
      pair_row_ranges {pair_label: (first_row, last_row)} of each pair's rows

    NN gateway: a pair's rows only add to the body totals if it has at least
    one NN Type 1 row >= 30 or NN Type 2 match row >= 30. Pairs containing a
    fast-moving body (Ascendant, Midheaven, Vertex, Part_of_Fortune) bypass
    the gateway. Non-gatewayed pairs are still printed."""
    ws.cell(row=r, column=1, value=title)
    section_title_row = r
    r += 1
    if not entries:
        ws.cell(row=r, column=1, value="(none)")
        return r + 2, None, [[0.0] * len(BODIES) for _ in range(4)], {}

    def combined(score, family, family_best, family_ra=None, family_dec=None, mode=None):
        """Add transit score, but only from the mode that matches the hit."""
        if mode and family_ra is not None and family_dec is not None:
            fam_dict = family_ra if mode == "RA" else family_dec
            return score + fam_dict.get(family, 0.0)
        return score + family_best.get(family, 0.0)

    # ── Four score-by-body blocks, each with a sum row ───────────────────────
    ws.cell(row=section_title_row, column=HL_COL_START_T1_RAW, value="TYPE 1 - SCORE BY TARGET BODY")
    ws.cell(row=section_title_row, column=HL_COL_START_T1_TT, value="TYPE 1 - SCORE + TRANSIT BY TARGET BODY")
    ws.cell(row=section_title_row, column=HL_COL_START_T2_RAW, value="TYPE 2 - SCORE BY TARGET BODY")
    ws.cell(row=section_title_row, column=HL_COL_START_T2_TT, value="TYPE 2 - SCORE + TRANSIT BY TARGET BODY")
    body_name_row = r
    for ci, body in enumerate(BODIES):
        ws.cell(row=body_name_row, column=HL_COL_START_T1_RAW + ci, value=body)
        ws.cell(row=body_name_row, column=HL_COL_START_T1_TT + ci, value=body)
        ws.cell(row=body_name_row, column=HL_COL_START_T2_RAW + ci, value=body)
        ws.cell(row=body_name_row, column=HL_COL_START_T2_TT + ci, value=body)
    sum_row = body_name_row + 1

    # ── Totals: computed after per-row writing (need per-pair NN gateway) ───
    # We'll accumulate totals as we write rows, then fill the sum row after.
    accum_t1_raw = [0.0] * len(BODIES)
    accum_t2_raw = [0.0] * len(BODIES)
    accum_t1_tt = [0.0] * len(BODIES)
    accum_t2_tt = [0.0] * len(BODIES)
    r = sum_row + 2

    pair_row_ranges = {}  # pair_label -> (start_row, end_row)
    for e in entries:
        family_best = e["family_best"]
        e_family_ra = e.get("family_ra", family_best)
        e_family_dec = e.get("family_dec", family_best)
        pair_start = r

        # Per-pair NN gateway: determines if this pair appears in summary.
        # If ANY NN T1 hit >= 30 or NN T2 MATCH >= 30 exists, the pair
        # is gatewayed and ALL its body columns are shown.
        # Fast-moving pairs skip the gateway entirely.
        pair_bodies = [x.strip() for x in e["pair"].split(" / ")]
        is_fast_pair = any(b in TRANSIT_ONLY_BODIES for b in pair_bodies)

        pair_gatewayed = is_fast_pair
        if not pair_gatewayed:
            for h, src in e["t1_rows"]:
                if src == "NN" and h["score"] >= 30:
                    pair_gatewayed = True
                    break
        if not pair_gatewayed:
            for g in e["t2_groups"]:
                if g.get("section") == "NN":
                    for row in g["rows"]:
                        if row["score"] >= 30:
                            pair_gatewayed = True
                            break
                if pair_gatewayed:
                    break
        ws.cell(row=r, column=1, value="PAIR")
        ws.cell(row=r, column=2, value=e["pair"])
        ws.cell(row=r, column=3, value="RA Score")
        ws.cell(row=r, column=4, value=round(e.get("ra_best", e["transit_score"]), 2))
        ws.cell(row=r, column=5, value="Dec Score")
        ws.cell(row=r, column=6, value=round(e.get("dec_best", 0), 2) if e.get("dec_best", 0) > 0 else None)
        r += 1

        groups: Dict[Tuple[str, str], List[tuple]] = {}
        for h, src in e["t1_rows"]:
            groups.setdefault((src, h["family"]), []).append(("t1", h, None))
        for g in e["t2_groups"]:
            groups.setdefault((g["section"], g["family"]), []).append(("t2_main", g, None))
            for bh in g["bonus"]:
                bsrc = bh.get("_bonus_section", g["section"])
                groups.setdefault((bsrc, bh["family"]), []).append(("t2_bonus", bh, g))

        for src in ("NN", "TN"):
            for fam_name, _ in VIBRATION_FAMILIES:
                key = (src, fam_name)
                if key not in groups:
                    continue
                fam_transit = round(family_best.get(fam_name, 0.0), 2)
                fam_ra = round(e.get("family_ra", family_best).get(fam_name, 0.0), 2) if "family_ra" in e else fam_transit
                fam_dec = round(e.get("family_dec", family_best).get(fam_name, 0.0), 2) if "family_dec" in e else fam_transit
                label = "NATAL-TO-NATAL" if src == "NN" else "TRANSIT-TO-NATAL"
                ws.cell(row=r, column=1, value=f"{label} -- {fam_name} --")
                ws.cell(row=r, column=10, value=fam_transit or None)
                r += 1
                ws.cell(row=r, column=1, value="Relation")
                ws.cell(row=r, column=2, value="From")
                ws.cell(row=r, column=3, value="To")
                ws.cell(row=r, column=4, value="Mode")
                ws.cell(row=r, column=5, value="Distance")
                ws.cell(row=r, column=6, value="Score")
                ws.cell(row=r, column=7, value="Match")
                ws.cell(row=r, column=8, value="Match Partner")
                ws.cell(row=r, column=9, value="NN / TN")
                ws.cell(row=r, column=10, value="Transit Score")
                ws.cell(row=r, column=11, value="Rule")
                ws.cell(row=r, column=12, value="Linking Body")
                ws.cell(row=r, column=13, value="Transit Dist")
                r += 1
                # Look up transit pair raw distances
                tt_ra = e.get("ra_dist")
                tt_dec = e.get("dec_dist")
                for kind, item, parent in groups[key]:
                    if kind == "t1":
                        h = item
                        ws.cell(row=r, column=1, value=h["relation"])
                        ws.cell(row=r, column=2, value=h["from"])
                        ws.cell(row=r, column=3, value=h["to"])
                        ws.cell(row=r, column=4, value=h["mode"])
                        ws.cell(row=r, column=5, value=round(h["distance"], 4))
                        ws.cell(row=r, column=6, value=round(h["score"], 2))
                        if h.get("match") == "BOTH":       # C3 note, no score
                            ws.cell(row=r, column=7, value="BOTH")
                            ws.cell(row=r, column=8, value=h.get("match_partner"))
                        ws.cell(row=r, column=9, value=src)
                        fam_mode = fam_ra if h["mode"] == "RA" else fam_dec
                        ws.cell(row=r, column=10, value=fam_mode if fam_mode > 0 else None)
                        ws.cell(row=r, column=11, value=e.get("t1_rule", ""))
                        ws.cell(row=r, column=12, value=", ".join(e.get("t1_link_bodies", [])))
                        tt_raw = tt_ra if h["mode"] == "RA" else tt_dec
                        ws.cell(row=r, column=13, value=round(tt_raw, 6) if tt_raw is not None else None)
                        bi = BODY_COL_INDEX_HL.get(h["to"])
                        if bi is not None and pair_gatewayed:
                            val_raw = round(h["score"], 2)
                            val_tt = round(combined(h["score"], h["family"], family_best, e_family_ra, e_family_dec, h["mode"]), 2)
                            ws.cell(row=r, column=HL_COL_START_T1_RAW + bi, value=val_raw)
                            ws.cell(row=r, column=HL_COL_START_T1_TT + bi, value=val_tt)
                            accum_t1_raw[bi] += val_raw
                            accum_t1_tt[bi] += val_tt
                        # NN hits also register in the "from" body column
                        if src == "NN":
                            bi_from = BODY_COL_INDEX_HL.get(h["from"])
                            if bi_from is not None and pair_gatewayed:
                                val_raw = round(h["score"], 2)
                                val_tt = round(combined(h["score"], h["family"], family_best, e_family_ra, e_family_dec, h["mode"]), 2)
                                ws.cell(row=r, column=HL_COL_START_T1_RAW + bi_from, value=val_raw)
                                ws.cell(row=r, column=HL_COL_START_T1_TT + bi_from, value=val_tt)
                                accum_t1_raw[bi_from] += val_raw
                                accum_t1_tt[bi_from] += val_tt
                        r += 1
                    elif kind == "t2_main":
                        g = item
                        for row_h in g["rows"]:
                            ws.cell(row=r, column=1, value="convergence")
                            ws.cell(row=r, column=2, value=row_h["from"])
                            ws.cell(row=r, column=3, value=row_h["to"])
                            ws.cell(row=r, column=4, value=row_h["mode"])
                            ws.cell(row=r, column=5, value=round(row_h["distance"], 4))
                            ws.cell(row=r, column=6, value=round(row_h["score"], 2))
                            ws.cell(row=r, column=7, value="MATCH")
                            other = [x for x in g["rows"] if x is not row_h][0]
                            ws.cell(row=r, column=8, value=other["from"])
                            ws.cell(row=r, column=9, value=src)
                            fam_mode = fam_ra if row_h["mode"] == "RA" else fam_dec
                            ws.cell(row=r, column=10, value=fam_mode if fam_mode > 0 else None)
                            ws.cell(row=r, column=11, value=g.get("_rule", ""))
                            ws.cell(row=r, column=12, value=", ".join(g.get("_link_bodies", [])))
                            tt_raw = tt_ra if row_h["mode"] == "RA" else tt_dec
                            ws.cell(row=r, column=13, value=round(tt_raw, 6) if tt_raw is not None else None)
                            bi = BODY_COL_INDEX_HL.get(row_h["to"])
                            if bi is not None and pair_gatewayed:
                                val_raw = round(row_h["score"], 2)
                                val_tt = round(combined(row_h["score"], row_h["family"], family_best, e_family_ra, e_family_dec, row_h["mode"]), 2)
                                ws.cell(row=r, column=HL_COL_START_T2_RAW + bi, value=val_raw)
                                ws.cell(row=r, column=HL_COL_START_T2_TT + bi, value=val_tt)
                                accum_t2_raw[bi] += val_raw
                                accum_t2_tt[bi] += val_tt
                            # NN T2 hits also register in "from" body column
                            if g.get("section") == "NN":
                                bi_from = BODY_COL_INDEX_HL.get(row_h["from"])
                                if bi_from is not None and pair_gatewayed:
                                    val_raw = round(row_h["score"], 2)
                                    val_tt = round(combined(row_h["score"], row_h["family"], family_best, e_family_ra, e_family_dec, row_h["mode"]), 2)
                                    ws.cell(row=r, column=HL_COL_START_T2_RAW + bi_from, value=val_raw)
                                    ws.cell(row=r, column=HL_COL_START_T2_TT + bi_from, value=val_tt)
                                    accum_t2_raw[bi_from] += val_raw
                                    accum_t2_tt[bi_from] += val_tt
                            r += 1
                    else:  # t2_bonus
                        bh = item
                        ws.cell(row=r, column=1, value="convergence (bonus)")
                        ws.cell(row=r, column=2, value=bh["from"])
                        ws.cell(row=r, column=3, value=bh["to"])
                        ws.cell(row=r, column=4, value=bh["mode"])
                        ws.cell(row=r, column=5, value=round(bh["distance"], 4))
                        ws.cell(row=r, column=6, value=round(bh["score"], 2))
                        ws.cell(row=r, column=9, value=bh.get("_bonus_section", src))
                        fam_mode = fam_ra if bh["mode"] == "RA" else fam_dec
                        ws.cell(row=r, column=10, value=fam_mode if fam_mode > 0 else None)
                        ws.cell(row=r, column=11, value=(parent.get("_rule", "") + " (bonus row)") if parent else "bonus row")
                        ws.cell(row=r, column=12, value=", ".join(parent.get("_link_bodies", [])) if parent else "")
                        tt_raw = tt_ra if bh["mode"] == "RA" else tt_dec
                        ws.cell(row=r, column=13, value=round(tt_raw, 6) if tt_raw is not None else None)
                        bi = BODY_COL_INDEX_HL.get(bh["to"])
                        if bi is not None and pair_gatewayed:
                            val_raw = round(bh["score"], 2)
                            val_tt = round(combined(bh["score"], bh["family"], family_best, e_family_ra, e_family_dec, bh["mode"]), 2)
                            ws.cell(row=r, column=HL_COL_START_T2_RAW + bi, value=val_raw)
                            ws.cell(row=r, column=HL_COL_START_T2_TT + bi, value=val_tt)
                            accum_t2_raw[bi] += val_raw
                            accum_t2_tt[bi] += val_tt
                        # NN bonus hits also register in "from" body column
                        bonus_sec = bh.get("_bonus_section", "")
                        if bonus_sec == "NN":
                            bi_from = BODY_COL_INDEX_HL.get(bh["from"])
                            if bi_from is not None and pair_gatewayed:
                                val_raw = round(bh["score"], 2)
                                val_tt = round(combined(bh["score"], bh["family"], family_best, e_family_ra, e_family_dec, bh["mode"]), 2)
                                ws.cell(row=r, column=HL_COL_START_T2_RAW + bi_from, value=val_raw)
                                ws.cell(row=r, column=HL_COL_START_T2_TT + bi_from, value=val_tt)
                                accum_t2_raw[bi_from] += val_raw
                                accum_t2_tt[bi_from] += val_tt
                        r += 1
        pair_row_ranges[e["pair"]] = (pair_start, r - 1)
        r += 1

    # Write accumulated totals to the sum row
    totals_t1_raw = [round(v, 2) for v in accum_t1_raw]
    totals_t2_raw = [round(v, 2) for v in accum_t2_raw]
    totals_t1_tt = [round(v, 2) for v in accum_t1_tt]
    totals_t2_tt = [round(v, 2) for v in accum_t2_tt]
    for ci in range(len(BODIES)):
        ws.cell(row=sum_row, column=HL_COL_START_T1_RAW + ci, value=totals_t1_raw[ci] or None)
        ws.cell(row=sum_row, column=HL_COL_START_T1_TT + ci, value=totals_t1_tt[ci] or None)
        ws.cell(row=sum_row, column=HL_COL_START_T2_RAW + ci, value=totals_t2_raw[ci] or None)
        ws.cell(row=sum_row, column=HL_COL_START_T2_TT + ci, value=totals_t2_tt[ci] or None)

    return r + 1, sum_row, [totals_t1_raw, totals_t2_raw, totals_t1_tt, totals_t2_tt], pair_row_ranges


def write_source_chains_block(ws, r: int, chains: List[dict]) -> int:
    ws.cell(row=r, column=1, value="SOURCE CHAINS (3+ pairs)")
    r += 1
    if not chains:
        ws.cell(row=r, column=1, value="(none)")
        return r + 2
    ws.cell(row=r, column=1, value="Body")
    ws.cell(row=r, column=2, value="Type")
    ws.cell(row=r, column=3, value="Pairs")
    r += 1
    # Ties broken by body name, then type, so output is identical run to run
    for c in sorted(chains, key=lambda x: (-len(x["pairs"]), x["body"], x["type"])):
        ws.cell(row=r, column=1, value=c["body"])
        ws.cell(row=r, column=2, value=c["type"])
        ws.cell(row=r, column=3, value=", ".join(c["pairs"]))
        r += 1
    return r + 1


# ── Output writing ───────────────────────────────────────────────────────────

def compute_pair_results(tt_pairs: List[dict], natal: Dict, tr: Dict) -> List[dict]:
    """NN/TN hits (with MATCH / BOTH flags) for every qualifying TT pair."""
    pair_results = []
    for p in tt_pairs:
        if p["overall_best"] < TT_THRESHOLD:
            continue
        a, b = p["pair"]
        nn_hits, nn_tally = gather_chart_hits(natal, natal, a, b, same_chart=True)
        mark_convergence_matches(nn_hits)
        tn_hits, tn_tally = gather_chart_hits(tr, natal, a, b, same_chart=False)
        mark_convergence_matches(tn_hits)
        pair_results.append({
            "p": p, "a": a, "b": b,
            "nn_hits": nn_hits, "nn_tally": nn_tally,
            "tn_hits": tn_hits, "tn_tally": tn_tally,
        })
    return pair_results


def body_strengths(pr: dict) -> Dict[str, List[float]]:
    """C2: for one pair block, {target body: [best score of each distinct
    contact]}. A contact is (layer, relation, from, target, mode) - counted
    once however many families it scores in; the RA node axis is one target."""
    best: Dict[tuple, Tuple[float, str]] = {}
    for layer, hits in (("NN", pr["nn_hits"]), ("TN", pr["tn_hits"])):
        for h in hits:
            key = (layer, h["relation"], h["from"], _target_key(h), h["mode"])
            if key not in best or h["score"] > best[key][0]:
                best[key] = (h["score"], h["to"])
    per_body: Dict[str, List[float]] = {}
    for score, body in best.values():
        per_body.setdefault(body, []).append(score)
    return {body: sorted(ss, reverse=True) for body, ss in per_body.items()}


def recurring_threshold(all_pair_results: List[List[dict]]) -> Optional[float]:
    """C2: race-level strength at the top RECURRING_TOP_PCT percent, across
    every (subject, pair, body) entry with at least one contact."""
    import numpy as np
    strengths = [sum(ss) for prs in all_pair_results for pr in prs
                 for ss in body_strengths(pr).values()]
    if not strengths:
        return None
    return float(np.percentile(strengths, 100.0 - RECURRING_TOP_PCT))


def write_subject_sheet(wb: Workbook, sheet_name: str, subject_name: str,
                         tt_pairs: List[dict], natal: Dict, tr: Dict,
                         event_label: str = "",
                         pair_results: Optional[List[dict]] = None,
                         recur_threshold: Optional[float] = None):
    ws = wb.create_sheet(sheet_name)
    ws.cell(row=1, column=1, value=subject_name)
    ws.cell(row=2, column=1, value=event_label)

    # Rows 1-3 are reserved for the pinned tally block; body of the sheet
    # starts at row 5.
    r = 5

    qualifying = [p for p in tt_pairs if p["overall_best"] >= TT_THRESHOLD]

    if not qualifying:
        ws.cell(row=r, column=1, value=f"No transit pairs scored >= {TT_THRESHOLD:.0f}")
        return {"sheet": sheet_name, "subject": subject_name, "pairs": [],
                "totals": [[0.0] * len(BODIES) for _ in range(4)], "main_sum_row": None,
                "main_totals": [[0.0] * len(BODIES) for _ in range(4)],
                "core_max_row": None,
                "core_max_values": [[0.0] * len(BODIES) for _ in range(4)]}

    # ── Summary list of qualifying pairs — split core / fast-moving ─────────
    FAST_SET = set(TRANSIT_ONLY_BODIES)
    core_pairs = [p for p in qualifying
                  if p["pair"][0] not in FAST_SET and p["pair"][1] not in FAST_SET]
    fast_pairs_list = [p for p in qualifying
                       if p["pair"][0] in FAST_SET or p["pair"][1] in FAST_SET]

    def _write_pair_list(ws, r, title, pairs, qual_row, add_max_row=False):
        ws.cell(row=r, column=1, value=title)
        r += 1
        ws.cell(row=r, column=1, value="Pair")
        ws.cell(row=r, column=2, value="RA Score")
        ws.cell(row=r, column=3, value="Dec Score")
        ws.cell(row=r, column=4, value="RA Dist")
        ws.cell(row=r, column=5, value="Dec Dist")
        header_row = r
        r += 1
        max_row = None
        if add_max_row:
            ws.cell(row=r, column=1, value="MAX")
            max_row = r
            r += 1
        first_data_row = r
        for p in pairs:
            a, b = p["pair"]
            label = f"{a} / {b}"
            ws.cell(row=r, column=1, value=label)
            ws.cell(row=r, column=2, value=round(p.get("ra_best", 0), 2) if p.get("ra_best", 0) > 0 else None)
            ws.cell(row=r, column=3, value=round(p.get("dec_best", 0), 2) if p.get("dec_best", 0) > 0 else None)
            ws.cell(row=r, column=4, value=round(p["ra_dist"], 6) if p["ra_dist"] is not None else None)
            ws.cell(row=r, column=5, value=round(p["dec_dist"], 6) if p["dec_dist"] is not None else None)
            qual_row[label] = r
            r += 1
        last_data_row = r - 1
        return r, max_row, first_data_row, last_data_row

    qual_row = {}
    r, core_max_row, core_first, core_last = _write_pair_list(
        ws, r, f"QUALIFYING CORE PAIRS (score >= {TT_THRESHOLD:.0f})", core_pairs, qual_row, add_max_row=True)
    r += 1
    r, _, _, _ = _write_pair_list(ws, r, "QUALIFYING FAST-MOVING PAIRS", fast_pairs_list, qual_row)
    r += 2

    # ── NN/TN hits for every qualifying pair (normally precomputed in main) ─
    if pair_results is None:
        pair_results = compute_pair_results(qualifying, natal, tr)

    # ── Highlight summary: MAIN, ADDITIONAL, SOURCE CHAINS ───────────────────
    highlights = build_pair_highlights(pair_results)
    r, main_sum_row, main_totals, hl_pair_ranges = write_highlight_block(ws, r, "MAIN SUMMARY (Type 1 + Type 2, linked)", highlights["main"])
    r, _, _, _ = write_highlight_block(ws, r, "ADDITIONAL SUMMARY (unlinked / secondary)", highlights["additional"])
    r = write_source_chains_block(ws, r, highlights["source_chains"])
    r += 1

    # ── Column layout for the 4 body-indexed score blocks, attached directly
    #    to each hit's own row (starting at column N = 14) ───────────────────
    N = len(BODIES)
    gap = 1
    HIT_COL_START = 14  # column N
    col_t1 = HIT_COL_START                 # SELF/DIRECT/CROSS raw score
    col_t2 = col_t1 + N + gap              # MATCH raw score
    col_t3 = col_t2 + N + gap              # SELF/DIRECT/CROSS + transit pair vibration score
    col_t4 = col_t3 + N + gap              # MATCH + transit pair vibration score
    BODY_COL_INDEX = {b: i for i, b in enumerate(BODIES)}

    def combined_value(h, pr):
        tt_fam_score = pr["p"]["family_best"].get(h["family"], 0.0)
        return tt_fam_score + h["score"]

    def combined_value_mode(h, pr):
        """Combined value using mode-matched transit family score."""
        if h["mode"] == "RA":
            tt_fam_score = pr["p"].get("family_ra", pr["p"]["family_best"]).get(h["family"], 0.0)
        else:
            tt_fam_score = pr["p"].get("family_dec", pr["p"]["family_best"]).get(h["family"], 0.0)
        return tt_fam_score + h["score"]

    # Header + running sum row, pinned to the top of the sheet alongside the
    # subject name (row 1) and event label (row 2)
    header_row = 1
    ws.cell(row=header_row, column=col_t1, value="SELF / DIRECT / CROSS HITS BY BODY")
    ws.cell(row=header_row, column=col_t2, value="MATCH HITS BY BODY")
    ws.cell(row=header_row, column=col_t3, value="SELF / DIRECT / CROSS (+ transit pair vibration score)")
    ws.cell(row=header_row, column=col_t4, value="MATCH (+ transit pair vibration score)")
    body_name_row = header_row + 1
    for ci, body in enumerate(BODIES):
        ws.cell(row=body_name_row, column=col_t1 + ci, value=body)
        ws.cell(row=body_name_row, column=col_t2 + ci, value=body)
        ws.cell(row=body_name_row, column=col_t3 + ci, value=body)
        ws.cell(row=body_name_row, column=col_t4 + ci, value=body)

    all_hits = []
    for pr in pair_results:
        all_hits.extend((h, pr) for h in pr["nn_hits"])
        all_hits.extend((h, pr) for h in pr["tn_hits"])
    scd_all = [(h, pr) for h, pr in all_hits if h["relation"] in ("self", "direct", "cross")]
    match_all = [(h, pr) for h, pr in all_hits if h.get("match") == "MATCH"]

    sum_row = body_name_row + 1
    block_totals = [[], [], [], []]     # per-body totals, one list per block
    for ci, body in enumerate(BODIES):
        v1 = round(sum(h["score"] for h, _ in scd_all if h["to"] == body), 2)
        v2 = round(sum(h["score"] for h, _ in match_all if h["to"] == body), 2)
        v3 = round(sum(combined_value_mode(h, pr) for h, pr in scd_all if h["to"] == body), 2)
        v4 = round(sum(combined_value_mode(h, pr) for h, pr in match_all if h["to"] == body), 2)
        ws.cell(row=sum_row, column=col_t1 + ci, value=v1 or None)
        ws.cell(row=sum_row, column=col_t2 + ci, value=v2 or None)
        ws.cell(row=sum_row, column=col_t3 + ci, value=v3 or None)
        ws.cell(row=sum_row, column=col_t4 + ci, value=v4 or None)
        for k, v in enumerate((v1, v2, v3, v4)):
            block_totals[k].append(v)

    # NOTE: r is NOT reset here. The tally block above is pinned to rows 1-3,
    # so r must carry on from the end of the qualifying-pairs list.

    for pr in pair_results:
        p, a, b = pr["p"], pr["a"], pr["b"]
        pair_label = f"{a} / {b}"

        # ── Repeat body-name headings above this pair's hit rows ─────────
        for ci, body in enumerate(BODIES):
            ws.cell(row=r, column=col_t1 + ci, value=body)
            ws.cell(row=r, column=col_t2 + ci, value=body)
            ws.cell(row=r, column=col_t3 + ci, value=body)
            ws.cell(row=r, column=col_t4 + ci, value=body)

        block_start = r + 1     # first row after the pair header

        # ── Pair header ──────────────────────────────────────────────────
        ws.cell(row=r, column=1, value="TRANSIT PAIR")
        ws.cell(row=r, column=2, value=pair_label)
        ws.cell(row=r, column=3, value="RA Score")
        ws.cell(row=r, column=4, value=round(p["ra_best"], 2) if p["ra_best"] > 0 else None)
        ws.cell(row=r, column=5, value="Dec Score")
        ws.cell(row=r, column=6, value=round(p["dec_best"], 2) if p["dec_best"] > 0 else None)
        ws.cell(row=r, column=7, value="Best Vibration")
        ws.cell(row=r, column=8, value=p["overall_family"])
        # Transit-transit separation distances
        ws.cell(row=r, column=9, value=round(p["ra_dist"], 6) if p["ra_dist"] is not None else None)
        ws.cell(row=r, column=10, value=round(p["dec_dist"], 6) if p["dec_dist"] is not None else None)
        r += 1

        # ── Other vibrations for this transit pair ──────────────────────
        ws.cell(row=r, column=1, value="Other vibrations (transit pair):")
        r += 1
        ws.cell(row=r, column=1, value="Vibration")
        ws.cell(row=r, column=2, value="Score")
        r += 1
        for name, _ in VIBRATION_FAMILIES:
            score = p["family_best"][name]
            ws.cell(row=r, column=1, value=name)
            ws.cell(row=r, column=2, value=round(score, 2) if score > 0 else None)
            r += 1
        r += 1

        # ── NN hits ───────────────────────────────────────────────────────
        nn_hits = pr["nn_hits"]
        ws.cell(row=r, column=1, value="NATAL-TO-NATAL HITS")
        r += 1
        for fam_name, _ in VIBRATION_FAMILIES:
            fam_hits = [h for h in nn_hits if h["family"] == fam_name]
            if not fam_hits:
                continue
            ws.cell(row=r, column=1, value=f"NATAL-TO-NATAL -- {fam_name} --")
            tt_fam_ra = p.get("family_ra", p["family_best"]).get(fam_name, 0.0)
            tt_fam_dec = p.get("family_dec", p["family_best"]).get(fam_name, 0.0)
            # Show both mode scores in the family header
            if tt_fam_ra > 0 or tt_fam_dec > 0:
                ws.cell(row=r, column=6, value=round(max(tt_fam_ra, tt_fam_dec), 2))
            r += 1
            ws.cell(row=r, column=1, value="Relation")
            ws.cell(row=r, column=2, value="From")
            ws.cell(row=r, column=3, value="To")
            ws.cell(row=r, column=4, value="Mode")
            ws.cell(row=r, column=5, value="Distance")
            ws.cell(row=r, column=6, value="Score")
            ws.cell(row=r, column=7, value="Match")
            ws.cell(row=r, column=8, value="Match Partner")
            ws.cell(row=r, column=9, value="Relation (non-convergence)")
            ws.cell(row=r, column=10, value="Transit Score")
            ws.cell(row=r, column=13, value="Transit Dist")
            r += 1
            for h in sorted(fam_hits, key=lambda x: -x["score"]):
                ws.cell(row=r, column=1, value=h["relation"])
                ws.cell(row=r, column=2, value=h["from"])
                ws.cell(row=r, column=3, value=h["to"])
                ws.cell(row=r, column=4, value=h["mode"])
                ws.cell(row=r, column=5, value=round(h["distance"], 4))
                ws.cell(row=r, column=6, value=round(h["score"], 2))
                ws.cell(row=r, column=7, value=h["match"])
                ws.cell(row=r, column=8, value=h["match_partner"])
                ws.cell(row=r, column=9, value=h["relation"].upper() if h["relation"] != "convergence" else None)
                # Transit score matched to this row's mode
                tt_fam_mode = tt_fam_ra if h["mode"] == "RA" else tt_fam_dec
                ws.cell(row=r, column=10, value=round(tt_fam_mode, 2) if tt_fam_mode > 0 else None)
                # Raw transit distance for this pair in the same mode as the hit
                tt_raw = p["ra_dist"] if h["mode"] == "RA" else p["dec_dist"]
                ws.cell(row=r, column=13, value=round(tt_raw, 6) if tt_raw is not None else None)
                cv = combined_value_mode(h, pr)
                # A 'direct' hit is the A-B separation itself and belongs to
                # both bodies, so it is written to both columns - matching how
                # 'self' and 'cross' already mark each end.
                cols = [BODY_COL_INDEX[h["to"]]]
                if h["relation"] == "direct" and h["from"] in BODY_COL_INDEX:
                    fi = BODY_COL_INDEX[h["from"]]
                    if fi not in cols:
                        cols.append(fi)
                for ci in cols:
                    if h["relation"] in ("self", "direct", "cross"):
                        ws.cell(row=r, column=col_t1 + ci, value=round(h["score"], 2))
                        ws.cell(row=r, column=col_t3 + ci, value=round(cv, 2))
                    if h.get("match") == "MATCH":
                        ws.cell(row=r, column=col_t2 + ci, value=round(h["score"], 2))
                        ws.cell(row=r, column=col_t4 + ci, value=round(cv, 2))
                r += 1
            r += 1
        if not nn_hits:
            ws.cell(row=r, column=1, value="(none)")
            r += 1
        r += 1

        # ── TN hits ───────────────────────────────────────────────────────
        tn_hits = pr["tn_hits"]
        ws.cell(row=r, column=1, value="TRANSIT-TO-NATAL HITS")
        r += 1
        for fam_name, _ in VIBRATION_FAMILIES:
            fam_hits = [h for h in tn_hits if h["family"] == fam_name]
            if not fam_hits:
                continue
            ws.cell(row=r, column=1, value=f"TRANSIT-TO-NATAL -- {fam_name} --")
            tt_fam_ra = p.get("family_ra", p["family_best"]).get(fam_name, 0.0)
            tt_fam_dec = p.get("family_dec", p["family_best"]).get(fam_name, 0.0)
            if tt_fam_ra > 0 or tt_fam_dec > 0:
                ws.cell(row=r, column=6, value=round(max(tt_fam_ra, tt_fam_dec), 2))
            r += 1
            ws.cell(row=r, column=1, value="Relation")
            ws.cell(row=r, column=2, value="From")
            ws.cell(row=r, column=3, value="To")
            ws.cell(row=r, column=4, value="Mode")
            ws.cell(row=r, column=5, value="Distance")
            ws.cell(row=r, column=6, value="Score")
            ws.cell(row=r, column=7, value="Match")
            ws.cell(row=r, column=8, value="Match Partner")
            ws.cell(row=r, column=9, value="Relation (non-convergence)")
            ws.cell(row=r, column=10, value="Transit Score")
            ws.cell(row=r, column=13, value="Transit Dist")
            r += 1
            for h in sorted(fam_hits, key=lambda x: -x["score"]):
                ws.cell(row=r, column=1, value=h["relation"])
                ws.cell(row=r, column=2, value=h["from"])
                ws.cell(row=r, column=3, value=h["to"])
                ws.cell(row=r, column=4, value=h["mode"])
                ws.cell(row=r, column=5, value=round(h["distance"], 4))
                ws.cell(row=r, column=6, value=round(h["score"], 2))
                ws.cell(row=r, column=7, value=h["match"])
                ws.cell(row=r, column=8, value=h["match_partner"])
                ws.cell(row=r, column=9, value=h["relation"].upper() if h["relation"] != "convergence" else None)
                # Transit score matched to this row's mode
                tt_fam_mode = tt_fam_ra if h["mode"] == "RA" else tt_fam_dec
                ws.cell(row=r, column=10, value=round(tt_fam_mode, 2) if tt_fam_mode > 0 else None)
                # Raw transit distance for this pair in the same mode as the hit
                tt_raw = p["ra_dist"] if h["mode"] == "RA" else p["dec_dist"]
                ws.cell(row=r, column=13, value=round(tt_raw, 6) if tt_raw is not None else None)
                cv = combined_value_mode(h, pr)
                # A 'direct' hit is the A-B separation itself and belongs to
                # both bodies, so it is written to both columns - matching how
                # 'self' and 'cross' already mark each end.
                cols = [BODY_COL_INDEX[h["to"]]]
                if h["relation"] == "direct" and h["from"] in BODY_COL_INDEX:
                    fi = BODY_COL_INDEX[h["from"]]
                    if fi not in cols:
                        cols.append(fi)
                for ci in cols:
                    if h["relation"] in ("self", "direct", "cross"):
                        ws.cell(row=r, column=col_t1 + ci, value=round(h["score"], 2))
                        ws.cell(row=r, column=col_t3 + ci, value=round(cv, 2))
                    if h.get("match") == "MATCH":
                        ws.cell(row=r, column=col_t2 + ci, value=round(h["score"], 2))
                        ws.cell(row=r, column=col_t4 + ci, value=round(cv, 2))
                r += 1
            r += 1
        if not tn_hits:
            ws.cell(row=r, column=1, value="(none)")
            r += 1
        r += 1

        # ── Recurring bodies (C2: race-level top n% by strength) ─────────
        if recur_threshold is None:
            thr_txt = "no threshold"
            recurring = {}
        else:
            thr_txt = f"threshold {recur_threshold:.2f}"
            recurring = {body: ss for body, ss in body_strengths(pr).items()
                         if len(ss) >= RECURRING_MIN_CONTACTS and sum(ss) >= recur_threshold}
        ws.cell(row=r, column=1,
                value=(f"RECURRING BODIES (race top {RECURRING_TOP_PCT:g}% by strength, "
                       f">= {RECURRING_MIN_CONTACTS} contacts; {thr_txt})"))
        r += 1
        if recurring:
            ws.cell(row=r, column=1, value="Body")
            ws.cell(row=r, column=2, value="Contacts")
            ws.cell(row=r, column=3, value="Strength")
            ws.cell(row=r, column=4, value="Contact scores")
            r += 1
            for body, ss in sorted(recurring.items(), key=lambda x: (-sum(x[1]), x[0])):
                ws.cell(row=r, column=1, value=body)
                ws.cell(row=r, column=2, value=len(ss))
                ws.cell(row=r, column=3, value=round(sum(ss), 2))
                ws.cell(row=r, column=4, value=", ".join(f"{x:.1f}" for x in ss))
                r += 1
        else:
            ws.cell(row=r, column=1, value="(none)")
            r += 1

        # ── Per-pair per-body SUM from MAIN SUMMARY into qualifying-pairs list ──
        # AV-D1: written as VALUES (the sum of the MAIN SUMMARY rows for this
        # pair), so any reader - Excel or Python - sees the number.
        if pair_label in qual_row and pair_label in hl_pair_ranges:
            qr = qual_row[pair_label]
            hl_start, hl_end = hl_pair_ranges[pair_label]
            for base in (col_t1, col_t2, col_t3, col_t4):
                for ci in range(len(BODIES)):
                    ws.cell(row=qr, column=base + ci,
                            value=_sum_cells(ws, base + ci, hl_start, hl_end))
        elif pair_label in qual_row:
            # Pair has no linked content — fill zeros
            qr = qual_row[pair_label]
            for base in (col_t1, col_t2, col_t3, col_t4):
                for ci in range(len(BODIES)):
                    ws.cell(row=qr, column=base + ci, value=0)

        r += 2  # gap before next pair

    # ── MAX row in core pairs section (AV-D1: values, not formulas) ──────────
    core_max_values = [[0.0] * len(BODIES) for _ in range(4)]
    if core_max_row and core_first <= core_last:
        for bi, base in enumerate((col_t1, col_t2, col_t3, col_t4)):
            for ci in range(len(BODIES)):
                vals = [ws.cell(row=rr, column=base + ci).value for rr in range(core_first, core_last + 1)]
                vals = [v for v in vals if isinstance(v, (int, float))]
                mx = round(max(vals), 2) if vals else 0
                ws.cell(row=core_max_row, column=base + ci, value=mx)
                core_max_values[bi][ci] = float(mx)

    ws.freeze_panes = "I3"

    return {
        "sheet": sheet_name,
        "subject": subject_name,
        "_natal": natal,
        "_tr": tr,
        "pairs": [(f'{p["pair"][0]} / {p["pair"][1]}', round(p["overall_best"], 2))
                  for p in qualifying],
        "totals": block_totals,
        "main_sum_row": main_sum_row,
        "main_totals": main_totals,
        "core_max_row": core_max_row,
        "core_max_values": core_max_values,
    }


def _sum_cells(ws, col: int, r1: int, r2: int) -> float:
    """Sum of the numeric cells in one column between two rows (inclusive) -
    the value Excel's =SUM() over the same range would show."""
    tot = 0.0
    for rr in range(r1, r2 + 1):
        v = ws.cell(row=rr, column=col).value
        if isinstance(v, (int, float)):
            tot += v
    return round(tot, 2)


def field_stats(per_subject: List[List[List[float]]]):
    """For per_subject[si][block][col] totals: field max, 2nd-highest distinct
    value, and each subject's rank (1 = highest, ties share, 0/blank = None).
    Works for a single-runner field (no 2nd value: gap and margin blank)."""
    n_blocks = len(per_subject[0]) if per_subject else 0
    n_cols = len(per_subject[0][0]) if per_subject else 0
    field_max = [[0.0] * n_cols for _ in range(n_blocks)]
    field_second = [[None] * n_cols for _ in range(n_blocks)]
    ranks = [[[None] * n_cols for _ in range(n_blocks)] for _ in per_subject]
    for bi in range(n_blocks):
        for ci in range(n_cols):
            vals = [s[bi][ci] for s in per_subject]
            ordered = sorted({v for v in vals if v and v > 0}, reverse=True)
            field_max[bi][ci] = ordered[0] if ordered else 0.0
            field_second[bi][ci] = ordered[1] if len(ordered) >= 2 else None
            pos = {v: i + 1 for i, v in enumerate(ordered)}
            for si, v in enumerate(vals):
                ranks[si][bi][ci] = pos.get(v) if v and v > 0 else None
    return field_max, field_second, ranks


# ── SUMMARY sheet ─────────────────────────────────────────────────────────────

def write_summary_sheet(wb: Workbook, subjects: List[dict], event_label: str):
    """
    Sheet layout (score blocks start at column N = 14, four blocks of
    len(BODIES) columns each: T1 raw, T2 raw, T1 + TT, T2 + TT):

        row 1                event label (col A); body names across all 4 blocks
        row 2      'Field Max (MAIN SUMMARY)'  - highest subject total per body
        row 3      'Gap (1st to 2nd)'          - field max minus 2nd-highest
        then one 5-row block per subject, starting at row 4:
        row R      subject name (col A); block titles at the 4 column bases
        row R+1    'Margin (to leader / 2nd)'  - values
        row R+2    'Rank'                      - values (1 = highest, ties share)
        row R+3    'Total (MAIN SUMMARY only)' - the subject's P-tab MAIN
                                                 SUMMARY sum row, as values (AV-D1)
        row R+4    blank

    Field max, gap, margin and rank are computed in Python from the same
    numbers written in the Total row.
    """
    ws = wb.create_sheet("SUMMARY", 0)
    ws.cell(row=1, column=1, value=event_label)

    N = len(BODIES)
    gap = 1
    col_t1 = 14
    col_t2 = col_t1 + N + gap
    col_t3 = col_t2 + N + gap
    col_t4 = col_t3 + N + gap
    bases = [(col_t1, "TYPE 1 - MAIN"), (col_t2, "TYPE 2 - MAIN"),
             (col_t3, "TYPE 1 - MAIN + TT"), (col_t4, "TYPE 2 - MAIN + TT")]

    # The Total row sources from each subject's own MAIN SUMMARY sum row
    # (not the unfiltered tally pinned at P-tab rows 1-3). Because the
    # qualifying-pair list is identical for every subject, that row is
    # normally the same for all subjects; each subject still carries its
    # own row number defensively.

    block_h = 5          # title(1) margin(1) rank(1) total(1) + 1 blank

    # Rank each subject's MAIN-summary total against the rest of the field,
    # per body per block, using the same numeric totals the Total row's
    # formulas resolve to (computed at write time, not read back from
    # formulas). 1 = highest; ties share a rank; a subject scoring nothing
    # on a body is left blank rather than ranked last.
    field_max = [[0.0] * N for _ in range(4)]
    field_second = [[None] * N for _ in range(4)]  # 2nd-highest distinct value, if any
    ranks = [[[None] * N for _ in range(4)] for _ in subjects]
    for bi in range(4):
        for ci in range(N):
            vals = [s["main_totals"][bi][ci] for s in subjects]
            positive = [v for v in vals if v > 0]
            ordered = sorted(set(positive), reverse=True)
            field_max[bi][ci] = ordered[0] if ordered else 0.0
            field_second[bi][ci] = ordered[1] if len(ordered) >= 2 else None
            pos = {v: i + 1 for i, v in enumerate(ordered)}
            for si, v in enumerate(vals):
                ranks[si][bi][ci] = pos.get(v) if v > 0 else None

    # ── Body names + field max, hoisted once to the top of the sheet (both
    #    are identical for every subject block, so no need to repeat them) ──
    for ci, body in enumerate(BODIES):
        for base, _ in bases:
            ws.cell(row=1, column=base + ci, value=body)
    ws.cell(row=2, column=1, value="Field Max (MAIN SUMMARY)")
    for bi, (base, _) in enumerate(bases):
        for ci in range(N):
            v = field_max[bi][ci]
            ws.cell(row=2, column=base + ci, value=v or None)

    ws.cell(row=3, column=1, value="Gap (1st to 2nd)")
    for bi, (base, _) in enumerate(bases):
        for ci in range(N):
            second = field_second[bi][ci]
            if second is not None and field_max[bi][ci]:
                ws.cell(row=3, column=base + ci, value=round(field_max[bi][ci] - second, 2))

    r = 4
    for si, subj in enumerate(subjects):
        sh = subj["sheet"]
        ws.cell(row=r, column=1, value=subj["subject"])
        for base, title in bases:
            ws.cell(row=r, column=base, value=title)

        # row 1 of the block: this subject's MARGIN for that column - how far
        # behind the field leader they are, or (if they ARE the leader) how
        # far clear of 2nd place they are. Blank if this subject scored
        # nothing on that column, or (for a sole leader) if no one else
        # scored on it either.
        ws.cell(row=r + 1, column=1, value="Margin (to leader / 2nd)")
        for bi, (base, _) in enumerate(bases):
            for ci in range(N):
                own = subj["main_totals"][bi][ci]
                if not own:
                    continue
                if ranks[si][bi][ci] == 1:
                    second = field_second[bi][ci]
                    margin = round(own - second, 2) if second is not None else None
                else:
                    margin = round(own - field_max[bi][ci], 2)
                ws.cell(row=r + 1, column=base + ci, value=margin)

        # row 2: this subject's rank position for that column
        ws.cell(row=r + 2, column=1, value="Rank")
        for bi, (base, _) in enumerate(bases):
            for ci in range(N):
                ws.cell(row=r + 2, column=base + ci, value=ranks[si][bi][ci])

        ws.cell(row=r + 3, column=1, value="Total (MAIN SUMMARY only)")
        if subj["main_sum_row"] is not None:
            for bi, (base, _) in enumerate(bases):
                for ci in range(N):
                    ws.cell(row=r + 3, column=base + ci,
                            value=subj["main_totals"][bi][ci] or None)

        r += block_h

    ws.freeze_panes = "D4"


def write_max_summary_sheet(wb: Workbook, subjects: List[dict], event_label: str):
    """Second SUMMARY sheet showing MAX scores per body (core pairs only),
    with the same field-max / gap / margin / rank structure as SUMMARY.
    v4.0 (AV-D1, AV-D2): every cell is a VALUE computed in Python from each
    subject's core-pairs MAX row, so the sheet reads correctly in Python as
    well as Excel, and a single-runner field no longer produces formula
    errors (gap and the leader's margin are simply left blank)."""
    ws = wb.create_sheet("SUMMARY_MAX", 0)
    ws.cell(row=1, column=1, value=event_label)

    N = len(BODIES)
    gap = 1
    col_t1 = 14
    col_t2 = col_t1 + N + gap
    col_t3 = col_t2 + N + gap
    col_t4 = col_t3 + N + gap
    bases = [(col_t1, "TYPE 1 - MAX"), (col_t2, "TYPE 2 - MAX"),
             (col_t3, "TYPE 1 - MAX + TT"), (col_t4, "TYPE 2 - MAX + TT")]
    block_h = 5

    maxes = [s.get("core_max_values") or [[0.0] * N for _ in range(4)] for s in subjects]
    # Same arithmetic as the v3 formulas: field max = MAX, 2nd = LARGE(...,2)
    # over every runner (zeros and ties included), rank = 1 + number of
    # runners strictly higher. With one runner there is no 2nd value.
    field_max = [[0.0] * N for _ in range(4)]
    field_second = [[None] * N for _ in range(4)]
    ranks = [[[None] * N for _ in range(4)] for _ in subjects]
    for bi in range(4):
        for ci in range(N):
            vals = [m[bi][ci] for m in maxes]
            desc = sorted(vals, reverse=True)
            field_max[bi][ci] = desc[0] if desc else 0.0
            field_second[bi][ci] = desc[1] if len(desc) >= 2 else None
            for si, v in enumerate(vals):
                ranks[si][bi][ci] = (1 + sum(1 for w in vals if w > v)) if v else None

    for ci, body in enumerate(BODIES):
        for base, _ in bases:
            ws.cell(row=1, column=base + ci, value=body)
    ws.cell(row=2, column=1, value="Field Max (MAX core pairs)")
    ws.cell(row=3, column=1, value="Gap (1st to 2nd)")
    for bi, (base, _) in enumerate(bases):
        for ci in range(N):
            fm = field_max[bi][ci]
            ws.cell(row=2, column=base + ci, value=fm or None)
            second = field_second[bi][ci]
            if second is not None and fm:
                ws.cell(row=3, column=base + ci, value=round(fm - second, 2))

    r = 4
    for si, subj in enumerate(subjects):
        ws.cell(row=r, column=1, value=subj["subject"])
        for base, title in bases:
            ws.cell(row=r, column=base, value=title)
        ws.cell(row=r + 1, column=1, value="Margin (to leader / 2nd)")
        ws.cell(row=r + 2, column=1, value="Rank")
        ws.cell(row=r + 3, column=1, value="MAX (core pairs)")
        for bi, (base, _) in enumerate(bases):
            for ci in range(N):
                own = maxes[si][bi][ci]
                if own:
                    if ranks[si][bi][ci] == 1:
                        second = field_second[bi][ci]
                        margin = round(own - second, 2) if second is not None else None
                    else:
                        margin = round(own - field_max[bi][ci], 2)
                    ws.cell(row=r + 1, column=base + ci, value=margin)
                ws.cell(row=r + 2, column=base + ci, value=ranks[si][bi][ci])
                ws.cell(row=r + 3, column=base + ci, value=own if own else 0)
        r += block_h

    ws.freeze_panes = "D4"


# ── Distance matrix tables (bodies × bodies) ─────────────────────────────────

def write_distance_matrix(ws, start_row: int, title: str, row_bodies: list,
                           chart_row: dict, chart_col: dict,
                           sep_fn, mode: str, col_bodies: list = None) -> int:
    """Write a distance matrix of raw angular distances.
    row_bodies = list of body names for the ROW axis
    col_bodies = list of body names for the COLUMN axis (defaults to row_bodies)
    chart_row  = {body: {ra, dec}} for the ROW axis
    chart_col  = {body: {ra, dec}} for the COLUMN axis
    sep_fn     = angular_sep_ra or angular_sep_dec
    mode       = 'ra' or 'dec' (key into chart dicts)
    Returns next available row."""
    if col_bodies is None:
        col_bodies = row_bodies
    r = start_row
    ws.cell(row=r, column=1, value=title)
    r += 1
    # Column headers
    for ci, body in enumerate(col_bodies):
        ws.cell(row=r, column=ci + 2, value=body)
    r += 1
    # Data rows
    for body_a in row_bodies:
        ws.cell(row=r, column=1, value=body_a)
        da = chart_row.get(body_a)
        va = da[mode] if da else None
        # equator has no RA position — skip its RA rows entirely
        if mode == 'ra' and body_a == 'equator':
            r += 1
            continue
        for ci, body_b in enumerate(col_bodies):
            # Skip fixed-star-to-fixed-star — permanent constants, no signal
            if body_a in FIXED_STARS and body_b in FIXED_STARS:
                continue
            # equator has no RA — skip as column body in RA matrices
            if mode == 'ra' and body_b == 'equator':
                continue
            db = chart_col.get(body_b)
            vb = db[mode] if db else None
            if va is not None and vb is not None:
                dist = sep_fn(va, vb)
                ws.cell(row=r, column=ci + 2, value=round(dist, 6))
        r += 1
    return r + 1


def write_subject_distance_tables(wb: Workbook, sheet_name: str,
                                    natal: dict, tr: dict,
                                    natal_fs: dict = None, transit_fs: dict = None):
    """Write 4 distance matrix tables for one subject (Nat×Nat RA, Nat×Nat Dec,
    Tra→Nat RA, Tra→Nat Dec) onto a new sheet.
    All 22 fixed stars are included as rows (they are already members of
    BODIES) so midpoint computation in race_observer.py can find them."""
    ws = wb.create_sheet(f"{sheet_name}_DIST")

    # Build extended row lists: standard BODIES + all 22 fixed stars as extra rows
    # For natal matrices: natal bodies as rows AND cols; fixed stars as extra rows only
    # For transit matrices: transit bodies as rows; natal bodies as cols
    natal_fs = natal_fs or {}
    transit_fs = transit_fs or {}

    # Merge natal chart with natal fixed stars for row lookup
    natal_extended = {**natal, **natal_fs}
    tr_extended = {**tr, **transit_fs}

    # Row bodies for natal matrices: BODIES (48, already includes the 22
    # fixed stars, so the appended list below is empty - kept as a guard)
    nn_row_bodies = BODIES + [fs for fs in FIXED_STARS_EXTENDED if fs not in set(BODIES)]
    # Col bodies stay as standard BODIES only (columns unchanged for compatibility)
    nn_col_bodies = BODIES

    # Row bodies for transit matrices: BODIES_TRANSIT + transit fixed stars
    tn_row_bodies = BODIES_TRANSIT + [fs for fs in FIXED_STARS_EXTENDED if fs not in set(BODIES_TRANSIT)]

    r = 1
    r = write_distance_matrix(ws, r, "NATAL × NATAL — RA distances",
                               nn_row_bodies, natal_extended, natal_extended,
                               angular_sep_ra, "ra", col_bodies=nn_col_bodies)
    r = write_distance_matrix(ws, r, "NATAL × NATAL — DEC distances",
                               nn_row_bodies, natal_extended, natal_extended,
                               angular_sep_dec, "dec", col_bodies=nn_col_bodies)
    r = write_distance_matrix(ws, r, "TRANSIT → NATAL — RA distances (transit on rows, natal on columns)",
                               tn_row_bodies, tr_extended, natal_extended,
                               angular_sep_ra, "ra", col_bodies=nn_col_bodies)
    r = write_distance_matrix(ws, r, "TRANSIT → NATAL — DEC distances (transit on rows, natal on columns)",
                               tn_row_bodies, tr_extended, natal_extended,
                               angular_sep_dec, "dec", col_bodies=nn_col_bodies)


def write_tt_distance_sheet(wb: Workbook, tr: dict, transit_fs: dict = None):
    """Write transit×transit distance tables (RA + Dec) on a single sheet.
    Transit fixed stars are appended as extra rows."""
    transit_fs = transit_fs or {}
    tr_extended = {**tr, **transit_fs}
    tt_row_bodies = BODIES_TRANSIT + [fs for fs in FIXED_STARS_EXTENDED if fs not in set(BODIES_TRANSIT)]

    ws = wb.create_sheet("TT_DIST")
    r = 1
    r = write_distance_matrix(ws, r, "TRANSIT × TRANSIT — RA distances",
                               tt_row_bodies, tr_extended, tr_extended,
                               angular_sep_ra, "ra", col_bodies=BODIES_TRANSIT)
    r = write_distance_matrix(ws, r, "TRANSIT × TRANSIT — DEC distances",
                               tt_row_bodies, tr_extended, tr_extended,
                               angular_sep_dec, "dec", col_bodies=BODIES_TRANSIT)


# ── Event label ───────────────────────────────────────────────────────────────

def build_event_label(trans_df: pd.DataFrame, input_path: str) -> str:
    """
    Combine the TRANS 'name' value (e.g. 'chester 14:40') with the date parsed
    from the input filename (race_batch_YYYYMMDD_...) to give
    'chester 14:40 - 22/08/2026'.

    Falls back to whichever part is available; returns '' if neither is.
    """
    event = ""
    if "name" in trans_df.columns and len(trans_df) > 0:
        val = trans_df["name"].iloc[0]
        if pd.notna(val):
            event = str(val).strip()

    date_str = ""
    m = re.search(r"race_batch_(\d{8})_", os.path.basename(input_path))
    if m:
        ymd = m.group(1)
        date_str = f"{ymd[6:8]}/{ymd[4:6]}/{ymd[0:4]}"

    if event and date_str:
        return f"{event} - {date_str}"
    return event or date_str


# ── Range scoring (H2) ────────────────────────────────────────────────────────
#
# A natal body's birth time is unknown, so its position is a PATH through the
# local birth day (NATAL_HOURLY). A distance is therefore a range [lo, hi],
# and each family is scored three ways:
#   score_mid  at local noon (the value used everywhere else)
#   score_max  the best score reached at any moment of the day
#   score_min  the lowest score across the whole day (holds whatever the time)
# Every family is a set of target windows, each peaking at its centre and
# falling to zero at its edge, so across an interval the best value is at an
# end or at a centre inside it, and the lowest at an end or just outside a
# window edge inside it. Those points are evaluated exactly - no sampling.

def _family_windows(family: str, lo: float, hi: float, mode: str):
    """(centres, edges) of one family's target windows that touch [lo, hi]."""
    centres, edges = [], []

    def periodic(step, hw, kmin=1):
        k0 = max(kmin, int(math.floor((lo - hw) / step)))
        k1 = int(math.ceil((hi + hw) / step))
        for k in range(k0, k1 + 1):
            c = k * step
            centres.append(c)
            edges.extend((c - hw, c + hw))

    def listed(targets):
        for c, hw in targets:
            if c + hw >= lo and c - hw <= hi:
                centres.append(c)
                edges.extend((c - hw, c + hw))

    if family == "Whole Number":
        periodic(1.0, 0.02)
        edges.extend((1.0, 200.0))
    elif family == "Golden Ratio":
        periodic(PHI, 0.03236)
        edges.append(PHI / 2.0)
    elif family == "Phi Powers":
        listed([(t, max(t * 0.005, 0.025)) for t in _PHI_POWER_TARGETS])
    elif family == "Ninths":
        for rlo, rhi, tol, t in _NINTH_RANGES:
            if rhi >= lo and rlo <= hi:
                centres.append(t)
                edges.extend((rlo, rhi, t - tol, t + tol))
    elif family == "Sqrt2":
        periodic(SQRT2, 0.02828)
        listed([(t, max(t * 0.005, 0.025)) for t in (10.0 * SQRT2, 100.0 * SQRT2)])
        edges.append(SQRT2 / 2.0)
    elif family == "Silver Ratio":
        periodic(SILVER, 0.04828)
        t = 10.0 * SILVER
        listed([(t, max(t * 0.005, 0.025))])
        edges.append(SILVER / 2.0)
    elif family == "Conjunction":
        tol = CONJUNCTION_TOL[mode]
        centres.append(0.0)
        edges.append(tol)
    return centres, edges


_FAMILY_FN = dict(VIBRATION_FAMILIES)


def range_scores(family: str, lo: float, hi: float, mode: str) -> Tuple[float, float]:
    """(score_min, score_max) of one family over distances [lo, hi]."""
    fn = _FAMILY_FN[family]
    centres, edges = _family_windows(family, lo, hi, mode)
    eps = 1e-9
    pts = [lo, hi] + [c for c in centres if lo < c < hi]
    for e in edges:
        for x in (e - eps, e, e + eps):
            if lo < x < hi:
                pts.append(x)
    vals = [fn(x, mode) for x in pts]
    return min(vals), max(vals)


def _wrap180(x: float) -> float:
    return ((x + 180.0) % 360.0) - 180.0


def distance_range(mode: str, a_path: List[float], b_path: List[float], err: float = 0.0):
    """Lowest and highest distance between two moving positions.
    a_path / b_path: values at the same moments (a 1-long list is a fixed
    position). err: extra +/- band (Transpluto model error, D3).
    The separation S(t) = a(t) - b(t) moves in straight lines between hourly
    samples, so it covers exactly [min S, max S]; RA is unwrapped so it is
    continuous. Distance is |S| (Dec) or S folded to 0..180 (RA)."""
    n = max(len(a_path), len(b_path))
    a = a_path if len(a_path) == n else a_path * n
    b = b_path if len(b_path) == n else b_path * n
    if mode == "RA":
        seps = [_wrap180(a[0] - b[0])]
        for i in range(1, n):
            seps.append(seps[-1] + _wrap180((a[i] - b[i]) - (a[i - 1] - b[i - 1])))
    else:
        seps = [a[i] - b[i] for i in range(n)]
    s_lo, s_hi = min(seps) - err, max(seps) + err
    if mode == "Dec":
        d_lo = 0.0 if s_lo <= 0.0 <= s_hi else min(abs(s_lo), abs(s_hi))
        return d_lo, max(abs(s_lo), abs(s_hi))

    def fold(x):
        return abs(_wrap180(x))
    has_zero = math.floor(s_hi / 360.0) >= math.ceil(s_lo / 360.0)
    has_180 = math.floor((s_hi - 180.0) / 360.0) >= math.ceil((s_lo - 180.0) / 360.0)
    d_lo = 0.0 if has_zero else min(fold(s_lo), fold(s_hi))
    d_hi = 180.0 if has_180 else max(fold(s_lo), fold(s_hi))
    return d_lo, d_hi


def certainty(score_min: float, score_max: float) -> str:
    """fixed: holds all day, varying by less than 1 point; certain: holds all
    day (score_min > 0); possible: only at some moment of the day."""
    if score_min > 0:
        return "fixed" if score_max - score_min < 1.0 else "certain"
    return "possible"


# ── Natal day paths (NATAL_HOURLY, written by the chart generator v2.2) ────────

def load_natal_paths(hourly_df: Optional[pd.DataFrame]) -> Dict[str, Dict[str, dict]]:
    """{tab: {body: {'ra': [..], 'dec': [..]}}} in hour order. Fixed stars
    keep the name without the _B suffix (as load_fixed_stars does)."""
    if hourly_df is None:
        raise ValueError("NATAL_HOURLY sheet not found - re-run the chart generator "
                         "(racingpost_excel_charts_swiss.py v2.2 or later) for this race")
    out: Dict[str, Dict[str, dict]] = {}
    df = hourly_df.sort_values(["tab", "body", "hour"])
    for (tab, body), g in df.groupby(["tab", "body"], sort=False):
        body = str(body)
        if body.endswith("_B") and body[:-2] in FIXED_STARS:
            body = body[:-2]
        elif body in FIXED_STARS and body in out.get(tab, {}):
            continue                    # the _B row already supplied this star
        ra = [None if pd.isna(v) else float(v) for v in g["ra"]]
        out.setdefault(str(tab), {})[body] = {"ra": ra, "dec": [float(v) for v in g["dec"]]}
    return out


def load_meta_roles(meta_df: Optional[pd.DataFrame]) -> Dict[str, dict]:
    """{tab: {'role', 'cloth'}} from the chart generator's META sheet, if any."""
    out = {}
    if meta_df is None:
        return out
    rows = meta_df.values.tolist()
    cols = [str(c) for c in meta_df.columns]
    hdr = None
    for i, row in enumerate([cols] + rows):
        vals = [str(v) for v in row]
        if hdr is None:
            if vals[:3] == ["tab", "role", "cloth"]:
                hdr = vals
            continue
        rec = dict(zip(hdr, row))
        tab = str(rec.get("tab", ""))
        if re.fullmatch(r"P\d+", tab):
            out[tab] = {"role": rec.get("role"), "cloth": rec.get("cloth")}
    return out


# ── HITS sheet (H1) ───────────────────────────────────────────────────────────

HITS_COLS = [
    "tab", "role", "cloth", "runner", "layer", "from", "to", "mode", "family",
    "relations", "dist_mid", "dist_min", "dist_max",
    "score_mid", "score_min", "score_max", "certainty",
    "families_mid", "families_max", "match",
    "via_pairs_n", "via_pairs", "best_tt_score",
    "summary", "summary_rule", "link_bodies", "note",
]


def _enumerate_pair_distances(a: str, b: str, same_chart: bool):
    """(relation, from, to) exactly as gather_chart_hits records them."""
    if same_chart:
        yield "direct", a, b
    else:
        yield "self", a, a
        yield "self", b, b
        yield "cross", a, b
        yield "cross", b, a
    for x in BODIES:
        if x in (a, b):
            continue
        yield "convergence", a, x
        yield "convergence", b, x


def _nn_key(f: str, t: str) -> Tuple[str, str]:
    """NN distances have no direction: one order per body pair, with a node
    (if exactly one) on the 'to' side so node-axis rules see it as a target."""
    if (f in NODES) != (t in NODES):
        return (t, f) if f in NODES else (f, t)
    return tuple(sorted((f, t)))


def _summary_index(pair_results: List[dict]) -> Dict[tuple, dict]:
    """(layer, from, to, mode, family) -> MATCH/BOTH flag and summary label
    from the noon-based P-tab logic (MAIN beats ADDITIONAL)."""
    layer_of = {}
    for pr in pair_results:
        for h in pr["nn_hits"]:
            layer_of[id(h)] = "NN"
        for h in pr["tn_hits"]:
            layer_of[id(h)] = "TN"
    idx: Dict[tuple, dict] = {}

    def key(h, layer):
        f, t = (h["from"], h["to"]) if layer == "TN" else _nn_key(h["from"], h["to"])
        return (layer, f, t, h["mode"], h["family"])

    for pr in pair_results:
        for layer, hits in (("NN", pr["nn_hits"]), ("TN", pr["tn_hits"])):
            for h in hits:
                if h.get("match"):
                    idx.setdefault(key(h, layer), {}).setdefault("match", set()).add(h["match"])
    hl = build_pair_highlights(pair_results)
    for label, entries in (("MAIN", hl["main"]), ("ADDITIONAL", hl["additional"])):
        for e in entries:
            items = [(h, e.get("t1_rule", ""), e.get("t1_link_bodies", [])) for h, _ in e["t1_rows"]]
            for g in e["t2_groups"]:
                items += [(h, g.get("_rule", ""), g.get("_link_bodies", [])) for h in g["rows"]]
                items += [(h, g.get("_rule", "") + " (bonus row)", g.get("_link_bodies", []))
                          for h in g["bonus"]]
            for h, rule, links in items:
                layer = layer_of.get(id(h))
                if layer is None:
                    continue
                rec = idx.setdefault(key(h, layer), {})
                if rec.get("summary") != "MAIN":
                    rec["summary"] = label
                rec.setdefault("rules", set()).add(rule)
                rec.setdefault("links", set()).update(links)
    return idx


def build_hits(tab: str, runner: str, meta: dict, qualifying: List[dict],
               natal: Dict, tr: Dict, paths: Dict[str, dict],
               pair_results: List[dict]) -> List[dict]:
    """One row per distinct contact for one runner (H1), scored across the
    birth day (H2). Uses the same distances and the same rules as the P tab
    (skip_distance, C1, C5c-B, C5d), applied to the range scores."""
    contacts: Dict[tuple, dict] = {}
    for p in qualifying:
        a, b = p["pair"]
        label = f"{a} / {b}"
        for layer, same in (("NN", True), ("TN", False)):
            c1 = natal if same else tr
            for rel, f, t in _enumerate_pair_distances(a, b, same):
                d1, d2 = c1.get(f), natal.get(t)
                if d1 is None or d2 is None:
                    continue
                if None in (d1["ra"], d2["ra"], d1["dec"], d2["dec"]):
                    continue
                if not same and f in FIXED_STARS:
                    continue
                if f in FIXED_STARS and t in FIXED_STARS:
                    continue
                if same:
                    f, t = _nn_key(f, t)
                for mode in ("RA", "Dec"):
                    if skip_distance(f, t, mode, same):
                        continue
                    c = contacts.setdefault((layer, f, t, mode), {
                        "layer": layer, "from": f, "to": t, "mode": mode,
                        "relations": set(), "pairs": {}})
                    c["relations"].add(rel)
                    c["pairs"][label] = p["overall_best"]

    rows = []
    for (layer, f, t, mode), c in contacts.items():
        key = "ra" if mode == "RA" else "dec"
        tp = paths.get(t)
        if tp is None:
            raise ValueError(f"{tab}: no NATAL_HOURLY path for {t}")
        b_path = tp[key]
        if layer == "NN":
            fp = paths.get(f)
            if fp is None:
                raise ValueError(f"{tab}: no NATAL_HOURLY path for {f}")
            a_path, a_mid = fp[key], natal[f][key]
        else:
            a_mid = tr[f][key]
            a_path = [a_mid]
        err = TRANSPLUTO_ERR * ((f == "Transpluto") + (t == "Transpluto"))
        d_mid = angular_sep_ra(a_mid, natal[t][key]) if mode == "RA" else angular_sep_dec(a_mid, natal[t][key])
        d_lo, d_hi = distance_range(mode, a_path, b_path, err)
        d_lo, d_hi = min(d_lo, d_mid), max(d_hi, d_mid)
        fam_rows = []
        for fam, fn in VIBRATION_FAMILIES:
            s_mid = fn(d_mid, mode)
            s_min, s_max = range_scores(fam, d_lo, d_hi, mode)
            s_max = max(s_max, s_mid)
            s_min = min(s_min, s_mid)
            if s_max <= 0:
                continue
            if layer == "TN" and f == t and f in SLOW_SELF_NO_CONJUNCTION and fam == "Conjunction":
                continue                                             # C1
            fam_rows.append({
                "layer": layer, "from": f, "to": t, "mode": mode, "family": fam,
                "relations": c["relations"], "pairs": c["pairs"],
                "dist_mid": d_mid, "dist_min": d_lo, "dist_max": d_hi,
                "score_mid": s_mid, "score_min": s_min, "score_max": s_max,
                "note": "Transpluto +/-0.01 deg band (D3)" if err else "",
            })
        n_mid = sum(1 for r in fam_rows if r["score_mid"] > 0)
        for r in fam_rows:
            r["families_mid"], r["families_max"] = n_mid, len(fam_rows)
        rows.extend(fam_rows)

    # Node-axis rules on the range scores (C5c-B then C5d), per layer
    out = []
    for layer in ("NN", "TN"):
        lr = [r for r in rows if r["layer"] == layer]
        if layer == "TN":
            lr = _merge_twins(lr)
            lr = collapse_tn_node_axis(lr, lambda r: r["score_max"])
        lr = _dedupe_node_axis_rows(lr)
        out.extend(lr)

    sidx = _summary_index(pair_results)
    for r in out:
        info = sidx.get((r["layer"], r["from"], r["to"], r["mode"], r["family"]), {})
        pairs = r["pairs"]
        r.update({
            "tab": tab, "runner": runner, "role": meta.get("role"), "cloth": meta.get("cloth"),
            "relations": ", ".join(sorted(r["relations"])),
            "certainty": certainty(r["score_min"], r["score_max"]),
            "match": "/".join(sorted(info.get("match", []))) or None,
            "via_pairs_n": len(pairs),
            "via_pairs": "; ".join(sorted(pairs)),
            "best_tt_score": max(pairs.values()),
            "summary": info.get("summary"),
            "summary_rule": " | ".join(sorted(x for x in info.get("rules", []) if x)) or None,
            "link_bodies": ", ".join(sorted(info.get("links", []))) or None,
        })
    fam_order = {n: i for i, (n, _) in enumerate(VIBRATION_FAMILIES)}
    out.sort(key=lambda r: (r["layer"], r["from"], r["to"], r["mode"], fam_order[r["family"]]))
    return out


def _merge_twins(rows: List[dict]) -> List[dict]:
    """TN RA node twins carry the same distance; before C5c-B drops one, pass
    its pairs and relations to the row that is kept."""
    by = {}
    for r in rows:
        if r["mode"] == "RA" and r["from"] in NODES and r["to"] in NODES:
            twin = "self" if r["from"] == r["to"] else "mirror"
            by.setdefault((twin, r["family"]), []).append(r)
    for group in by.values():
        pairs, rels = {}, set()
        for r in group:
            pairs.update(r["pairs"])
            rels |= r["relations"]
        for r in group:
            r["pairs"], r["relations"] = dict(pairs), set(rels)
    return rows


def _dedupe_node_axis_rows(rows: List[dict]) -> List[dict]:
    """C5d on HITS rows: X->Ketu and X->Rahu (or Ketu->X and Rahu->X) in RA
    are one contact seen from both ends; where the same family scores on
    both, keep one (higher score_max, then the Rahu label) and give it the
    other's pairs and relations."""
    drop = set()
    for side, other in (("to", "from"), ("from", "to")):
        groups: Dict[tuple, List[dict]] = {}
        for r in rows:
            if r["mode"] == "RA" and r[side] in NODES and r[other] not in NODES:
                groups.setdefault((r["layer"], r[other], r["family"]), []).append(r)
        for g in groups.values():
            if len({r[side] for r in g}) < 2:
                continue
            keep = max(g, key=lambda r: (r["score_max"], r[side] == "Rahu"))
            for r in g:
                if r is not keep:
                    keep["pairs"] = {**r["pairs"], **keep["pairs"]}
                    keep["relations"] = keep["relations"] | r["relations"]
                    drop.add(id(r))
    return [r for r in rows if id(r) not in drop]


def write_hits_sheet(wb: Workbook, rows: List[dict]):
    ws = wb.create_sheet("HITS")
    for c, h in enumerate(HITS_COLS, 1):
        ws.cell(row=1, column=c, value=h)
    rnd = {"dist_mid": 6, "dist_min": 6, "dist_max": 6,
           "score_mid": 2, "score_min": 2, "score_max": 2, "best_tt_score": 2}
    for i, r in enumerate(rows, 2):
        for c, h in enumerate(HITS_COLS, 1):
            v = r.get(h)
            if h in rnd and v is not None:
                v = round(v, rnd[h])
            if v == "":
                v = None
            ws.cell(row=i, column=c, value=v)
    ws.freeze_panes = "E2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(HITS_COLS))}{max(1, len(rows) + 1)}"


# ── TR_TR sheet: the race-level record of the race sky ────────────────────────

def write_tr_tr_sheet(wb: Workbook, tt_pairs: List[dict]):
    """Every qualifying transit-transit pair (>= TT_THRESHOLD): distances, the
    best score / family / mode, and every family's RA and Dec score. Pairs
    with Transpluto also carry the range over its +/-0.01 deg band (D3):
    best_certain = best family score that holds across the whole band."""
    ws = wb.create_sheet("TR_TR")
    fams = [n for n, _ in VIBRATION_FAMILIES]
    cols = (["rank", "body_A", "body_B", "ra_dist", "dec_dist", "best_score", "best_family",
             "best_mode", "ra_best", "dec_best", "best_certain", "note"]
            + [f"RA {n}" for n in fams] + [f"Dec {n}" for n in fams])
    for c, h in enumerate(cols, 1):
        ws.cell(row=1, column=c, value=h)
    r = 1
    for p in tt_pairs:
        if p["overall_best"] < TT_THRESHOLD:
            continue
        r += 1
        a, b = p["pair"]
        certain = p["overall_best"]
        note = None
        if "Transpluto" in (a, b):
            certain = 0.0
            for mode, d in (("RA", p["ra_dist"]), ("Dec", p["dec_dist"])):
                if mode == "RA" and {a, b} == NODES:
                    continue
                for fam in fams:
                    lo, hi = max(0.0, d - TRANSPLUTO_ERR), min(180.0, d + TRANSPLUTO_ERR)
                    certain = max(certain, range_scores(fam, lo, hi, mode)[0])
            note = "Transpluto +/-0.01 deg band (D3)"
        vals = [r - 1, a, b, round(p["ra_dist"], 6), round(p["dec_dist"], 6),
                round(p["overall_best"], 2), p["overall_family"], p["overall_mode"],
                round(p["ra_best"], 2), round(p["dec_best"], 2), round(certain, 2), note]
        vals += [round(p["family_ra"][n], 2) or None for n in fams]
        vals += [round(p["family_dec"][n], 2) or None for n in fams]
        for c, v in enumerate(vals, 1):
            ws.cell(row=r, column=c, value=v)
    ws.freeze_panes = "D2"


def copy_source_sheets(src_path: str, wb: Workbook, names) -> None:
    """Copy whole sheets (values only) from the input workbook (v4.1)."""
    from openpyxl import load_workbook
    src = load_workbook(src_path, read_only=True, data_only=True)
    for name in names:
        if name not in src.sheetnames:
            raise ValueError(f"{name} sheet not found in {src_path} - re-run the chart generator (v2.2+)")
        ws = wb.create_sheet(name)
        for row in src[name].iter_rows(values_only=True):
            ws.append(list(row))


# ── Main ──────────────────────────────────────────────────────────────────────

SCRIPT_VERSION = "4.1"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input race_batch Excel file")
    args = parser.parse_args()

    print(f"active_vibrations.py v{SCRIPT_VERSION}")
    print()

    base = os.path.basename(args.input)
    if base.startswith("~$"):
        print(f"Skipping Excel lock file: {base}")
        return
    if base.endswith("_active.xlsx"):
        print(f"Skipping previously generated output: {base}")
        return

    sheets = pd.read_excel(args.input, sheet_name=None)
    trans_df = sheets.get("TRANS")
    if trans_df is None:
        raise ValueError("TRANS sheet not found")
    tr = load_chart(trans_df, allowed_bodies=BODIES_TRANSIT)
    transit_fs = load_fixed_stars(trans_df)
    print(f"  Fixed stars loaded from TRANS: {len(transit_fs)} ({', '.join(sorted(transit_fs.keys()))})")
    # Merge fixed stars into transit chart so they participate in TT pair ranking
    # and per-subject NN/TN hit detection. Fixed-star-to-fixed-star pairs are
    # filtered inside rank_tt_pairs and gather_chart_hits.
    tr = {**tr, **transit_fs}

    event_label = build_event_label(trans_df, args.input)
    event_label = f"{event_label}  [v{SCRIPT_VERSION}]"
    print(f"Event: {event_label}")

    print("Ranking transit-to-transit pairs...")
    tt_pairs = rank_tt_pairs(tr)
    qualifying_count = sum(1 for p in tt_pairs if p["overall_best"] >= TT_THRESHOLD)
    print(f"  {len(tt_pairs)} total pairs, {qualifying_count} score >= {TT_THRESHOLD:.0f}")

    p_sheets = sorted([k for k in sheets if k.startswith("P") and k[1:].isdigit()],
                      key=lambda x: int(x[1:]))
    natal_paths = load_natal_paths(sheets.get("NATAL_HOURLY"))
    meta_roles = load_meta_roles(sheets.get("META"))
    qualifying = [p for p in tt_pairs if p["overall_best"] >= TT_THRESHOLD]

    wb = Workbook()
    wb.remove(wb.active)  # remove default sheet

    subject_infos = []
    natal_charts = {}     # keep for distance tables
    natal_fs_charts = {}  # fixed stars per subject natal chart
    subjects = []         # (p_key, subject_name, natal_fs, natal_with_fs, pair_results)

    # Pass 1: load every subject and compute its NN/TN hits (C2 needs the
    # whole race before the recurring-body threshold can be set)
    for p_key in p_sheets:
        df = sheets[p_key]
        if df is None or df.empty:
            continue
        # Subject name: prefer a 'name' column, but P tabs from the football
        # pipeline head this column with the club code (e.g. 'CHE') instead.
        # The name is always the first column's first value, so fall back to
        # position rather than header.
        if len(df) == 0 or len(df.columns) == 0:
            subject_name = p_key
            print(f"  [WARN] {p_key}: sheet is empty - using tab name as subject")
        elif "name" in df.columns:
            subject_name = df["name"].iloc[0]
        else:
            subject_name = df.iloc[0, 0]

        if pd.isna(subject_name) or str(subject_name).strip() == "":
            subject_name = p_key
            print(f"  [WARN] {p_key}: no subject name found - using tab name")

        print(f"{p_key}: {subject_name}")
        natal = load_chart(df)
        natal_fs = load_fixed_stars(df)
        # Merge natal fixed stars into natal chart so they participate in
        # NN hit detection and natal midpoint geometry as targets.
        natal_with_fs = {**natal, **natal_fs}
        natal_charts[p_key] = natal_with_fs
        natal_fs_charts[p_key] = natal_fs
        subjects.append((p_key, subject_name, natal_fs, natal_with_fs,
                         compute_pair_results(tt_pairs, natal_with_fs, tr)))

    recur_thr = recurring_threshold([s[4] for s in subjects])
    print(f"  Recurring-body threshold (race top {RECURRING_TOP_PCT:g}% strength): "
          f"{'n/a' if recur_thr is None else f'{recur_thr:.2f}'}")

    # HITS rows (H1/H2): one row per distinct contact, scored across the day
    print("Scoring contacts across each birth day (HITS)...")
    hits_rows = []
    for p_key, subject_name, natal_fs, natal_with_fs, pair_results in subjects:
        if not natal_with_fs:
            continue                    # placeholder tab (no data)
        if p_key not in natal_paths:
            raise ValueError(f"{p_key}: no NATAL_HOURLY rows - re-run the chart generator")
        hits_rows.extend(build_hits(p_key, str(subject_name), meta_roles.get(p_key, {}),
                                    qualifying, natal_with_fs, tr, natal_paths[p_key],
                                    pair_results))
    print(f"  {len(hits_rows)} HITS rows")

    # Pass 2: write subject sheets
    for p_key, subject_name, natal_fs, natal_with_fs, pair_results in subjects:
        info = write_subject_sheet(wb, p_key, str(subject_name), tt_pairs, natal_with_fs, tr,
                                   event_label, pair_results=pair_results,
                                   recur_threshold=recur_thr)
        if info:
            # Write fixed-star extended section to this subject's sheet
            ws = wb[p_key]
            last_row = ws.max_row + 2
            write_fs_section(ws, last_row, natal_fs, transit_fs, natal_with_fs, tr)
            subject_infos.append(info)

    # ── Distance matrix tables ─────────────────────────────────────────────
    print("Writing distance tables...")

    # Transit×Transit distance sheet (one per race) — includes transit fixed stars
    write_tt_distance_sheet(wb, tr, transit_fs=transit_fs)

    # ── TRANS_POS sheet — raw transit positions for three_way_midpoints.py ──
    ws_tp = wb.create_sheet("TRANS_POS")
    ws_tp.cell(row=1, column=1, value="body")
    ws_tp.cell(row=1, column=2, value="ra")
    ws_tp.cell(row=1, column=3, value="dec")
    # tr already includes transit_fs (merged earlier in main()).
    # Note: bodies lacking RA or Dec (e.g. equator) are skipped but still
    # consume a row index, leaving a blank row - kept as-is for downstream.
    for r_idx, (body, pos) in enumerate(sorted(tr.items()), start=2):
        if pos.get('ra') is None or pos.get('dec') is None:
            continue
        ws_tp.cell(row=r_idx, column=1, value=body)
        ws_tp.cell(row=r_idx, column=2, value=pos['ra'])
        ws_tp.cell(row=r_idx, column=3, value=pos['dec'])

    # ── P_POS sheets — raw natal positions per entity for three_way_midpoints.py ──
    for p_key in p_sheets:
        if p_key not in natal_charts: continue
        ws_pp = wb.create_sheet(f"{p_key}_POS")
        ws_pp.cell(row=1, column=1, value="body")
        ws_pp.cell(row=1, column=2, value="ra")
        ws_pp.cell(row=1, column=3, value="dec")
        natal_full = natal_charts[p_key]
        for r_idx, (body, pos) in enumerate(sorted(natal_full.items()), start=2):
            if not isinstance(pos, dict): continue
            if pos.get('ra') is None or pos.get('dec') is None: continue
            ws_pp.cell(row=r_idx, column=1, value=body)
            ws_pp.cell(row=r_idx, column=2, value=pos['ra'])
            ws_pp.cell(row=r_idx, column=3, value=pos['dec'])

    # Per-subject distance tables (Nat×Nat + Tra→Nat) — includes all 22 fixed stars
    for p_key in p_sheets:
        if p_key in natal_charts:
            p_natal_fs = natal_fs_charts.get(p_key, {})
            write_subject_distance_tables(wb, p_key, natal_charts[p_key], tr,
                                          natal_fs=p_natal_fs, transit_fs=transit_fs)

    base, ext = os.path.splitext(args.input)
    if subject_infos:
        write_summary_sheet(wb, subject_infos, event_label)
        write_max_summary_sheet(wb, subject_infos, event_label)
    write_tr_tr_sheet(wb, tt_pairs)
    write_hits_sheet(wb, hits_rows)
    # Put TR_TR and HITS straight after the two summary sheets
    for name in ("HITS", "TR_TR"):
        ws_ = wb[name]
        wb._sheets.remove(ws_)
        wb._sheets.insert(2 if subject_infos else 0, ws_)

    copy_source_sheets(args.input, wb, ("META", "NATAL_HOURLY"))
    out_path = f"{base}_active{ext}"
    wb.save(out_path)
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
