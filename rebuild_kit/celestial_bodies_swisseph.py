"""
celestial_bodies_swisseph.py  v2.2
==================================
Positions (RA / Dec) of every body used by the project, from the Swiss
Ephemeris, all in ONE reference frame: J2000 equatorial (decision ENG-1).

Bodies
  Planets:    Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus,
              Neptune, Pluto
  Nodes:      Rahu = TRUE lunar node (decision D1); Ketu = exactly opposite
  Asteroids:  Chiron, Ceres, Pallas, Juno, Vesta
  TNOs:       Eris, Haumea, Makemake, Gonggong, Quaoar, Sedna, Orcus
  Transpluto: Hawkins (1978) orbit, geocentric from the Swiss Earth position
  Stars:      Aldebaran, Regulus, Antares, Fomalhaut, plus the 22 stars with
              a _B suffix - taken directly in J2000 coordinates
  Equator:    Dec 0 (no RA)
  Points (race chart only, decision E2):
              Ascendant, Midheaven, Vertex - computed for the moment and
              place, converted exactly into J2000;
              Part_of_Fortune = Asc + Moon - Sun, Part_of_Spirit = Asc + Sun - Moon,
              in J2000 RA and Dec separately (decision D2, option A)

Frame and observer
  - Every position is J2000 equatorial, apparent (light-time, aberration and
    light deflection applied, as Swiss Ephemeris does by default), and
    topocentric at the given location (decision E1: the racecourse for the
    race chart, the birth country's centre for natal charts).

Natal charts (--natal-day, decision ENG-2)
  The birth time is unknown, so each body is calculated at every hour of the
  birth day in the zone's STANDARD time (00:00 to 24:00, no summer time) and
  at standard noon (decision NT-1, Eddie 30/09/2026: clock changes are
  artificial). The standard offset for a birth year is the smaller of the
  zone's mid-January and mid-July UTC offsets, because summer time always
  moves clocks forward: Europe/London and Europe/Dublin = UTC+0 all year,
  Europe/Paris = UTC+1, Australia/Sydney = UTC+10, America/New_York = UTC-5.
  Columns ra_A / dec_A hold standard noon; ra_lo, ra_hi, dec_lo, dec_hi hold the
  lowest and highest values of the day. RA limits are written continuously
  around the noon value, so ra_lo can be below 0 or ra_hi above 360 when the
  day crosses 0 deg (e.g. ra_lo = -1.2 means 358.8).
  Ascendant, Midheaven, Vertex, Part of Fortune and Part of Spirit need an
  exact time: in natal charts their rows are written blank.
  The hourly positions themselves are written to a second file,
  <chart file>_hourly.csv (columns: body, hour, local_time, utc_time, ra, dec),
  so that natal-to-natal distances can be followed hour by hour through the
  same day (decision H3-A).

Failure (ENG-6)
  If any body cannot be calculated, or Swiss Ephemeris falls back to its
  lower-precision built-in model because a data file is missing, the engine
  stops with exit code 2 and names the body. No partial chart is written.

Changes in v2.0: J2000 for stars and points; true node; Part of Spirit
added (night Part of Fortune removed); Campanus half-house cusps removed
(decision E3); birth-day ranges; fail on any missing body or data file.
Changes in v2.1: natal-day mode also writes the hourly positions file.
Changes in v2.2: natal day and noon in standard time, never summer time
(NT-1). Before this, a summer birth in the UK or Ireland was charted at
11:00 UTC; it is now 12:00 UTC, as in the original v2.5 engine.

Output columns
  body_A, body_B, measurement_type, ra_A, ra_B, ra_diff, ra_midpoint,
  dec_A, dec_B, dec_diff, dec_midpoint, topo_dist_AU_A, topo_dist_AU_B,
  dist_AU, mid_x_AU, mid_y_AU, mid_z_AU, moon_involved,
  ra_lo, ra_hi, dec_lo, dec_hi   (ranges for chart A, natal-day mode only)

Usage
  Race chart:
    python celestial_bodies_swisseph.py --lat1 51.3981 --lon1 -2.3308 --elevation1 175 \\
        --time1 "2026-09-29 15:32" --tz1 Europe/London \\
        --lat2 51.3981 --lon2 -2.3308 --elevation2 175 \\
        --time2 "2026-09-29 15:32" --tz2 Europe/London \\
        --ephemeris-path ephe --csv trans
  Natal chart (birth date, standard-time noon, whole-day ranges):
    python celestial_bodies_swisseph.py --natal-day --lat1 53.1424 --lon1 -7.6921 \\
        --time1 "2024-03-27 12:00" --tz1 Europe/Dublin \\
        --lat2 53.1424 --lon2 -7.6921 --time2 "2024-03-27 12:00" --tz2 Europe/Dublin \\
        --ephemeris-path ephe --csv natal
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from datetime import datetime, timedelta

import numpy as np
import pytz
import swisseph as swe

ENGINE_VERSION = "2.2"
KM_PER_AU = 1.495978707e8
EPHE_PATH = "/Users/eddieplace/astronomy-project/ephe"   # overridden by --ephemeris-path


class EngineError(Exception):
    """A body could not be calculated correctly. The message names it."""


# ── Bodies ─────────────────────────────────────────────────────────────────────

_SWE_PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
    "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
    "Rahu": swe.TRUE_NODE,          # decision D1: true node
}
_SWE_ASTEROIDS = {
    "Chiron": swe.CHIRON, "Ceres": swe.CERES, "Pallas": swe.PALLAS,
    "Juno": swe.JUNO, "Vesta": swe.VESTA,
}
_SWE_TNOS = {                        # minor-planet numbers (swe.AST_OFFSET + n)
    "Eris": 136199, "Haumea": 136108, "Makemake": 136472, "Gonggong": 225088,
    "Quaoar": 50000, "Sedna": 90377, "Orcus": 90482,
}
EXTRA_STARS = ["Aldebaran", "Regulus", "Antares", "Fomalhaut"]
# (our name, sefstars.txt name)
BEHENIAN_STARS = [
    ("Algol", "Algol"), ("Pleiades", "Alcyone"), ("Aldebaran", "Aldebaran"),
    ("Capella", "Capella"), ("Sirius", "Sirius"), ("Procyon", "Procyon"),
    ("Regulus", "Regulus"), ("Alkaid", "Alkaid"), ("Algorab", "Algorab"),
    ("Spica", "Spica"), ("Arcturus", "Arcturus"), ("Alphecca", "Alphecca"),
    ("Antares", "Antares"), ("Vega", "Vega"), ("Deneb Algedi", "Denebalgedi"),
    ("Fomalhaut", "Fomalhaut"), ("Rigel", "Rigel"), ("Betelgeuse", "Betelgeuse"),
    ("Polaris", "Polaris"), ("Castor", "Castor"), ("Altair", "Altair"),
    ("Bellatrix", "Bellatrix"),
]
TIMED_POINTS = ["Part_of_Fortune", "Part_of_Spirit", "Ascendant", "Midheaven", "Vertex"]

STANDARD_ORDER = [
    "Aldebaran", "Antares", "Ceres", "Chiron", "Eris", "Fomalhaut",
    "Juno", "Jupiter", "Ketu", "Mars", "Mercury", "Moon", "Neptune",
    "Pallas", "Pluto", "Rahu", "Regulus", "Saturn", "Sun", "Uranus",
    "Venus", "Vesta", "equator",
]
TNO_ORDER = ["Gonggong", "Haumea", "Makemake", "Orcus", "Quaoar", "Sedna", "Transpluto"]
BEHENIAN_ORDER = [n + "_B" for n, _ in BEHENIAN_STARS]
ALL_ORDER = STANDARD_ORDER + TNO_ORDER + TIMED_POINTS + BEHENIAN_ORDER

# Swiss flags: J2000 equatorial, topocentric, apparent
_FLAG = swe.FLG_SWIEPH | swe.FLG_EQUATORIAL | swe.FLG_J2000 | swe.FLG_TOPOCTR
_FLAG_DATE = swe.FLG_SWIEPH | swe.FLG_EQUATORIAL | swe.FLG_TOPOCTR   # true equator of date
_FLAG_HELIO = swe.FLG_SWIEPH | swe.FLG_HELCTR | swe.FLG_XYZ | swe.FLG_J2000


# ── Vector helpers ────────────────────────────────────────────────────────────

def _unit(ra_deg: float, dec_deg: float) -> np.ndarray:
    a, d = math.radians(ra_deg), math.radians(dec_deg)
    return np.array([math.cos(d) * math.cos(a), math.cos(d) * math.sin(a), math.sin(d)])


def _radec(v: np.ndarray):
    v = v / np.linalg.norm(v)
    return math.degrees(math.atan2(v[1], v[0])) % 360.0, math.degrees(math.asin(max(-1.0, min(1.0, v[2]))))


# ── Swiss Ephemeris calls ─────────────────────────────────────────────────────

def _calc(name: str, body_id: int, jd: float):
    """(ra_deg, dec_deg, dist_au) in J2000 topocentric. Stops on any error or
    on a silent fall-back from the Swiss data files to the Moshier model."""
    try:
        res, ret = swe.calc_ut(jd, body_id, _FLAG)
    except swe.Error as e:
        raise EngineError(f"{name}: {e}")
    if not ret & swe.FLG_SWIEPH:
        raise EngineError(f"{name}: Swiss Ephemeris data file not used (fell back to "
                          f"the built-in Moshier model) - check the ephe folder")
    return res[0], res[1], res[2]


def _helio_xyz(name: str, body_id: int, jd: float):
    try:
        res, _ = swe.calc_ut(jd, body_id, _FLAG_HELIO)
        return (res[0], res[1], res[2])
    except swe.Error:
        return None


def _star(our_name: str, swe_name: str, jd: float, flag: int = _FLAG):
    try:
        res, _, _ = swe.fixstar2_ut(swe_name, jd, flag)
    except swe.Error as e:
        raise EngineError(f"Fixed star {our_name}: {e}")
    return res[0], res[1]


_ROT_STARS = [("Aldebaran", "Aldebaran"), ("Polaris", "Polaris"), ("Antares", "Antares"),
              ("Spica", "Spica"), ("Vega", "Vega"), ("Fomalhaut", "Fomalhaut")]


def date_to_j2000_matrix(jd: float) -> np.ndarray:
    """Rotation taking true-equator-of-date vectors into J2000, derived from
    Swiss Ephemeris itself (the same stars in both frames). Residual is
    checked: it must reproduce every reference star to within 1e-5 deg
    (0.04 arcsec); in practice about 1.5e-6 deg."""
    a = np.array([_unit(*_star(n, s, jd, _FLAG_DATE)) for n, s in _ROT_STARS])
    b = np.array([_unit(*_star(n, s, jd, _FLAG)) for n, s in _ROT_STARS])
    u, _, vt = np.linalg.svd(a.T @ b)
    d = np.sign(np.linalg.det(vt.T @ u.T))
    r = vt.T @ np.diag([1.0, 1.0, d]) @ u.T
    worst = max(np.degrees(np.arccos(min(1.0, float(np.dot(r @ x, y))))) for x, y in zip(a, b))
    if worst > 1e-5:
        raise EngineError(f"Frame rotation check failed (residual {worst:.2e} deg)")
    return r


def chart_angles(jd: float, lat: float, lon: float, rot: np.ndarray) -> dict:
    """Ascendant, Midheaven, Vertex for the moment and place, in J2000 RA/Dec.
    Swiss gives their ecliptic longitudes on the true ecliptic of date; they
    are placed on that ecliptic, converted to the true equator of date with
    the true obliquity, then rotated exactly into J2000."""
    _, ascmc = swe.houses_ex(jd, lat, lon, b"E")
    eps_true = swe.calc_ut(jd, swe.ECL_NUT)[0][0]
    out = {}
    for name, lon_ecl in (("Ascendant", ascmc[0]), ("Midheaven", ascmc[1]), ("Vertex", ascmc[3])):
        ra_d, dec_d, _ = swe.cotrans((lon_ecl, 0.0, 1.0), -eps_true)
        out[name] = _radec(rot @ _unit(ra_d, dec_d))
    return out


# Transpluto (Hawkins 1978 elements), heliocentric on the mean ecliptic of date
_J1900 = 2415020.0
_JC = 36525.0


def _solve_kepler(m: float, e: float) -> float:
    E = m
    for _ in range(500):
        dE = (m - E + e * math.sin(E)) / (1.0 - e * math.cos(E))
        E += dE
        if abs(dE) < 1e-12:
            break
    return E


def transpluto(jd: float, rot: np.ndarray):
    """(ra_deg, dec_deg, dist_au), J2000, geocentric using the Swiss Earth
    position. Model accuracy is about 0.01 deg (decision D3)."""
    T = (jd - _J1900) / _JC
    e, a = 0.300, 77.755
    omega = math.radians((0.0438748 + 1.396 * T) % 360.0)
    E = _solve_kepler(math.radians((66.806096 + 52.50492 * T) % 360.0), e)
    nu = 2.0 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2))
    r = a * (1 - e * math.cos(E))
    ecl = np.array([r * math.cos(nu + omega), r * math.sin(nu + omega), 0.0])
    eps_mean = math.radians(swe.calc_ut(jd, swe.ECL_NUT)[0][1])
    ce, se = math.cos(eps_mean), math.sin(eps_mean)
    eq_date = np.array([ecl[0], ecl[1] * ce - ecl[2] * se, ecl[1] * se + ecl[2] * ce])
    helio = rot @ eq_date
    try:
        sun, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL | swe.FLG_J2000 | swe.FLG_XYZ)
    except swe.Error as e2:
        raise EngineError(f"Transpluto (Earth position): {e2}")
    geo = helio + np.array(sun[:3])          # Earth = -Sun(geocentric)
    ra, dec = _radec(geo)
    return ra, dec, float(np.linalg.norm(geo)), tuple(helio)


# ── All bodies at one instant ─────────────────────────────────────────────────

def bodies_at(jd: float, lat: float, lon: float, elev: float, with_points: bool) -> dict:
    """{name: {'ra','dec','dist_au','hxyz'}} for every body at one instant.
    ra/dec in degrees, J2000, topocentric."""
    swe.set_topo(lon, lat, elev)
    out = {}
    for name, bid in _SWE_PLANETS.items():
        ra, dec, dist = _calc(name, bid, jd)
        out[name] = {"ra": ra, "dec": dec, "dist_au": dist,
                     "hxyz": None if name in ("Sun", "Rahu") else _helio_xyz(name, bid, jd)}
    r = out["Rahu"]
    out["Ketu"] = {"ra": (r["ra"] + 180.0) % 360.0, "dec": -r["dec"], "dist_au": None, "hxyz": None}
    for name, bid in _SWE_ASTEROIDS.items():
        ra, dec, dist = _calc(name, bid, jd)
        out[name] = {"ra": ra, "dec": dec, "dist_au": dist, "hxyz": _helio_xyz(name, bid, jd)}
    for name, num in _SWE_TNOS.items():
        ra, dec, dist = _calc(name, swe.AST_OFFSET + num, jd)
        out[name] = {"ra": ra, "dec": dec, "dist_au": dist,
                     "hxyz": _helio_xyz(name, swe.AST_OFFSET + num, jd)}
    rot = date_to_j2000_matrix(jd)
    ra, dec, dist, helio = transpluto(jd, rot)
    out["Transpluto"] = {"ra": ra, "dec": dec, "dist_au": dist, "hxyz": helio}
    for name in EXTRA_STARS:
        ra, dec = _star(name, name, jd)
        out[name] = {"ra": ra, "dec": dec, "dist_au": None, "hxyz": None}
    for name, swe_name in BEHENIAN_STARS:
        ra, dec = _star(name, swe_name, jd)
        out[name + "_B"] = {"ra": ra, "dec": dec, "dist_au": None, "hxyz": None}
    out["equator"] = {"ra": None, "dec": 0.0, "dist_au": None, "hxyz": None}

    if with_points:
        ang = chart_angles(jd, lat, lon, rot)
        for name, (ra, dec) in ang.items():
            out[name] = {"ra": ra, "dec": dec, "dist_au": None, "hxyz": None}
        asc, sun, moon = out["Ascendant"], out["Sun"], out["Moon"]
        for name, sign in (("Part_of_Fortune", 1.0), ("Part_of_Spirit", -1.0)):
            ra = (asc["ra"] + sign * (moon["ra"] - sun["ra"])) % 360.0
            dec = asc["dec"] + sign * (moon["dec"] - sun["dec"])
            if abs(dec) > 90.0:
                raise EngineError(f"{name}: Dec {dec:.3f} outside +/-90")
            out[name] = {"ra": ra, "dec": dec, "dist_au": None, "hxyz": None}
    else:
        for name in TIMED_POINTS:
            out[name] = {"ra": None, "dec": None, "dist_au": None, "hxyz": None}
    return out


def standard_tz(tz, year: int):
    """Fixed-offset zone for the STANDARD time of `tz` in `year` (decision NT-1):
    the smaller of the mid-January and mid-July UTC offsets, since summer time
    always moves clocks forward. Works for both hemispheres and for zones that
    write winter time as a negative DST (Europe/Dublin)."""
    offs = [tz.localize(datetime(year, m, 15, 12)).utcoffset() for m in (1, 7)]
    minutes = int(min(offs).total_seconds() // 60)
    return pytz.FixedOffset(minutes)


def std_label(dt) -> str:
    """'UTC+01:00' style label for a fixed-offset datetime."""
    m = int(dt.utcoffset().total_seconds() // 60)
    sign = "+" if m >= 0 else "-"
    return f"UTC{sign}{abs(m) // 60:02d}:{abs(m) % 60:02d}"


def natal_day_ranges(local_date, tz, lat, lon, elev) -> tuple:
    """(noon_bodies, ranges, hourly) for the birth day in standard time:
    ranges[name] = (ra_lo, ra_hi, dec_lo, dec_hi), RA continuous around the
    noon value; hourly = [(std_dt, samples_dict), ...] for 00:00 .. 24:00
    standard time (always 25 moments - no clock-change days)."""
    stz = standard_tz(tz, local_date.year)
    start = stz.localize(datetime(local_date.year, local_date.month, local_date.day))
    noon = stz.localize(datetime(local_date.year, local_date.month, local_date.day, 12))
    moments = [start + timedelta(hours=h) for h in range(25)]
    noon_b = bodies_at(_to_jd_ut(noon), lat, lon, elev, with_points=False)
    samples = [bodies_at(_to_jd_ut(m), lat, lon, elev, with_points=False) for m in moments]
    ranges = {}
    for name, b in noon_b.items():
        if b["dec"] is None:
            continue
        decs = [s[name]["dec"] for s in samples] + [b["dec"]]
        if b["ra"] is None:
            ranges[name] = (None, None, min(decs), max(decs))
            continue
        offs = [((s[name]["ra"] - b["ra"] + 180.0) % 360.0) - 180.0 for s in samples] + [0.0]
        ranges[name] = (b["ra"] + min(offs), b["ra"] + max(offs), min(decs), max(decs))
    return noon_b, ranges, list(zip(moments, samples))


# ── Time ──────────────────────────────────────────────────────────────────────

TIME_FMTS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M",
             "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"]


def _parse_time(s: str, tz_str: str) -> datetime:
    tz = pytz.timezone(tz_str)
    for fmt in TIME_FMTS:
        try:
            return tz.localize(datetime.strptime(s.strip(), fmt))
        except ValueError:
            continue
    raise EngineError(f"Cannot parse time: {s!r}")


def _to_jd_ut(aware_dt: datetime) -> float:
    u = aware_dt.astimezone(pytz.utc)
    _, jd_ut = swe.utc_to_jd(u.year, u.month, u.day, u.hour, u.minute,
                             u.second + u.microsecond / 1e6, swe.GREG_CAL)
    return jd_ut


# ── Output ────────────────────────────────────────────────────────────────────

OUTPUT_COLS = [
    "body_A", "body_B", "measurement_type",
    "ra_A", "ra_B", "ra_diff", "ra_midpoint",
    "dec_A", "dec_B", "dec_diff", "dec_midpoint",
    "topo_dist_AU_A", "topo_dist_AU_B",
    "dist_AU", "mid_x_AU", "mid_y_AU", "mid_z_AU",
    "moon_involved",
    "ra_lo", "ra_hi", "dec_lo", "dec_hi",
]


HOURLY_COLS = ["body", "hour", "local_time", "utc_time", "ra", "dec"]


def _ra_diff(a, b):
    d = abs(a - b) % 360.0
    return d if d <= 180.0 else 360.0 - d


def _ra_mid(a, b):
    return (a + (((b - a + 180.0) % 360.0) - 180.0) / 2.0) % 360.0


def _row(name: str, b1: dict, b2: dict, rng) -> dict:
    row = {"body_A": name, "body_B": name, "measurement_type": "transit_self",
           "moon_involved": name == "Moon"}
    ra1, ra2, d1, d2 = b1.get("ra"), b2.get("ra"), b1.get("dec"), b2.get("dec")
    if ra1 is not None and ra2 is not None:
        row.update(ra_A=ra1, ra_B=ra2, ra_diff=_ra_diff(ra1, ra2), ra_midpoint=_ra_mid(ra1, ra2))
    if d1 is not None and d2 is not None:
        row.update(dec_A=d1, dec_B=d2, dec_diff=abs(d1 - d2), dec_midpoint=(d1 + d2) / 2.0)
    if b1.get("dist_au") is not None:
        row["topo_dist_AU_A"] = b1["dist_au"]
    if b2.get("dist_au") is not None:
        row["topo_dist_AU_B"] = b2["dist_au"]
    h1, h2 = b1.get("hxyz"), b2.get("hxyz")
    if h1 and h2:
        row["dist_AU"] = math.dist(h1, h2)
        row["mid_x_AU"], row["mid_y_AU"], row["mid_z_AU"] = ((h1[i] + h2[i]) / 2.0 for i in range(3))
    if rng:
        row["ra_lo"], row["ra_hi"], row["dec_lo"], row["dec_hi"] = rng
    return {k: ("" if row.get(k) is None else row.get(k, "")) for k in OUTPUT_COLS}


def _parse_args():
    p = argparse.ArgumentParser(description=f"Celestial bodies (Swiss Ephemeris) v{ENGINE_VERSION}")
    for i in ("1", "2"):
        p.add_argument(f"--lat{i}", type=float, required=True)
        p.add_argument(f"--lon{i}", type=float, required=True)
        p.add_argument(f"--elevation{i}", type=float, default=0.0)
        p.add_argument(f"--time{i}", required=True)
        p.add_argument(f"--tz{i}", default="UTC")
    p.add_argument("--natal-day", action="store_true",
                   help="Natal chart: standard-time noon values plus whole-day ranges "
                        "(no summer time); "
                        "time-dependent points left blank")
    p.add_argument("--ephemeris-path", default=EPHE_PATH)
    p.add_argument("--hip-path", default=".")   # kept for CLI compatibility, unused
    p.add_argument("--csv", default="bodies_")
    p.add_argument("--quiet", action="store_true")
    return p.parse_args()


def run(args) -> str:
    ephe = os.path.abspath(args.ephemeris_path)
    if not os.path.isdir(ephe):
        raise EngineError(f"Ephemeris folder not found: {ephe}")
    swe.set_ephe_path(ephe)
    t1 = _parse_time(args.time1, args.tz1)
    t2 = _parse_time(args.time2, args.tz2)

    def chart(t, lat, lon, elev, tzname):
        if args.natal_day:
            return natal_day_ranges(t.date(), pytz.timezone(tzname), lat, lon, elev)
        return bodies_at(_to_jd_ut(t), lat, lon, elev, with_points=True), {}, None

    b1, r1, hourly = chart(t1, args.lat1, args.lon1, args.elevation1, args.tz1)
    same = (t1 == t2 and (args.lat1, args.lon1, args.elevation1) == (args.lat2, args.lon2, args.elevation2))
    b2 = b1 if same else chart(t2, args.lat2, args.lon2, args.elevation2, args.tz2)[0]

    missing = [n for n in ALL_ORDER if n not in b1]
    if missing:
        raise EngineError(f"Bodies missing from chart: {', '.join(missing)}")
    rows = [_row(n, b1[n], b2[n], r1.get(n)) for n in ALL_ORDER]

    out_path = f"{args.csv.rstrip('_')}_{t1.strftime('%Y%m%d_%H%M')}_vs_{t2.strftime('%Y%m%d_%H%M')}.csv"
    with open(out_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUTPUT_COLS)
        w.writeheader()
        w.writerows(rows)
    if hourly:
        hourly_path = out_path[:-4] + "_hourly.csv"
        with open(hourly_path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(HOURLY_COLS)
            for name in ALL_ORDER:
                if b1[name]["dec"] is None:
                    continue
                for h, (m, smp) in enumerate(hourly):
                    w.writerow([name, h, f"{m.strftime('%Y-%m-%d %H:%M')} {std_label(m)}",
                                m.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M"),
                                "" if smp[name]["ra"] is None else repr(smp[name]["ra"]),
                                repr(smp[name]["dec"])])
    if not args.quiet:
        print(f"celestial_bodies_swisseph.py v{ENGINE_VERSION}: {len(rows)} bodies -> {out_path}")
    return out_path


def main() -> int:
    args = _parse_args()
    try:
        run(args)
    except EngineError as e:
        print(f"[ENGINE ERROR] {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
