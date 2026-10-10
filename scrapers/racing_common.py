"""
racing_common.py  v1.1
======================
Shared code for racingpost_results_scraper.py and racingpost_card_scraper.py.

Both scrapers must process runners identically, so everything they share
lives here and nowhere else:

  - CSV_FIELDS            the race_batch CSV columns (one format for both)
  - normalise_name()      name cleaning used for the jockey lookup
  - JockeyLookup          jockeys_lookup.csv reader + missing-rider report
  - COUNTRY_CODES         one complete Racing Post country-code table
  - COUNTRY_TZ            birth country -> time zone (v1.1)
  - race_time_*()         ONE race-time rule (24-hour first, 12-hour fallback)
  - is_uk()               UK-only rule (decision D4: UK venues only)
  - parse_sp()            SP text + favourite marker (F / JF / CF)
  - get_next_data()       reads the page's embedded race data (__NEXT_DATA__)
  - fetch_horse_profile() horse DOB + breeding country from its profile page

CSV rules
---------
  - name is always "<cloth> <name>" - never any result tag (no "W", "FAV").
  - Result data lives in its own columns: finish_pos, sp, is_fav. They are
    filled only by the results scraper and only on HORSE rows; they must be
    read only at review time, never by the analysis steps.
  - status is "runner" or "NR". NR rows are kept for the record; the chart
    step skips them.
  - Rows are written in cloth order (horse, then its jockey), never in
    finishing order.

Failures raise ScrapeError with a clear message. A scraper stops that race,
reports why, carries on with the next race, and exits non-zero at the end.
"""

from __future__ import annotations

import csv
import json
import re
import time
import unicodedata
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

COMMON_VERSION = "1.1"


class ScrapeError(Exception):
    """A race could not be scraped cleanly. The message says why."""


# ---------------------------------------------------------------------------
# CSV format (identical for both scrapers)
# ---------------------------------------------------------------------------

CSV_FIELDS = [
    "race_date", "race_time", "racecourse", "subject_type",
    "cloth", "name", "dob", "birth_country",
    "finish_pos", "sp", "is_fav", "status",
]


def race_filename(race_day: date, venue: str, race_time: str) -> str:
    """race_batch_YYYYMMDD_venue_HHMM.csv  (race_time must be 'HH:MM', 24-hour)"""
    return (f"race_batch_{race_day.strftime('%Y%m%d')}_"
            f"{venue.replace(' ', '_')}_{race_time.replace(':', '')}.csv")


def write_race_csv(path: Path, rows: List[Dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in CSV_FIELDS})


def build_rows(race_date_str: str, race_time: str, venue: str,
               runners: List[Dict]) -> List[Dict]:
    """
    Turn parsed runners into CSV rows: horse then jockey, in cloth order,
    non-runners without a cloth number last. Each runner dict carries:
      cloth, horse, horse_dob, horse_country, jockey, jockey_dob,
      jockey_country, finish_pos, sp, is_fav, status
    """
    def key(r):
        return (r.get("cloth") is None, r.get("cloth") or 0, r["horse"])

    rows = []
    for r in sorted(runners, key=key):
        cloth = r.get("cloth")
        prefix = f"{cloth} " if cloth is not None else ""
        base = {"race_date": race_date_str, "race_time": race_time,
                "racecourse": venue, "cloth": cloth if cloth is not None else "",
                "status": r.get("status", "runner")}
        rows.append({**base, "subject_type": "horse",
                     "name": f"{prefix}{r['horse']}",
                     "dob": r.get("horse_dob", ""),
                     "birth_country": r.get("horse_country", ""),
                     "finish_pos": r.get("finish_pos", ""),
                     "sp": r.get("sp", ""),
                     "is_fav": ("1" if r.get("is_fav") else "0") if r.get("sp") else ""})
        if r.get("jockey"):
            rows.append({**base, "subject_type": "jockey",
                         "name": f"{prefix}{r['jockey']}",
                         "dob": r.get("jockey_dob", ""),
                         "birth_country": r.get("jockey_country", "")})
    return rows


# ---------------------------------------------------------------------------
# Names and the jockey lookup
# ---------------------------------------------------------------------------

def normalise_name(name: str) -> str:
    """Lookup key for a person's name. Unchanged from the previous scrapers
    so existing jockeys_lookup.csv keys still match. Note: 'Jr'/'Sr' are
    stripped, so a father and son with the same name share one key."""
    if not isinstance(name, str):
        return ""
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r"\b(Mr|Miss|Mrs|Ms|Dr)\b\.?", "", name, flags=re.I)
    name = name.replace("’", "'").replace("‘", "'").replace("`", "'")
    name = re.sub(r"\s+(jr\.?|sr\.?)$", "", name, flags=re.I)
    name = re.sub(r"^\d+\s+", "", name.strip())
    name = re.sub(r"\b([A-Za-z])\.", r"\1", name)
    result = " ".join(name.lower().split())
    if any("　" <= c <= "鿿" for c in result):
        result = result.replace(" ", "")
    return result


def clean_jockey_name(name: str) -> str:
    """Remove an apprentice claim such as '(3)' or '(7lb)' from a display name."""
    return re.sub(r"\s*\(\s*\d+\s*(lb)?\s*\)\s*$", "", (name or "").strip(), flags=re.I)


class JockeyLookup:
    """jockeys_lookup.csv reader that also records every miss for a report."""

    def __init__(self, path: str):
        self.path = path
        self.entries: Dict[str, Dict[str, str]] = {}
        self.missing: List[Dict[str, str]] = []
        p = Path(path)
        if not p.exists():
            raise ScrapeError(f"Jockey lookup not found: {path}")
        with open(p, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cols = [c.strip().lower() for c in (reader.fieldnames or [])]
            country_col = next((c for c in ("birth_country", "place_of_birth", "country")
                                if c in cols), None)
            for row in reader:
                row = {k.strip().lower(): (v or "").strip() for k, v in row.items()}
                key = normalise_name(row.get("name", ""))
                if key:
                    self.entries[key] = {"dob": row.get("dob", ""),
                                         "birth_country": row.get(country_col, "") if country_col else ""}
        print(f"[INFO] Loaded {len(self.entries)} jockey entries from {path}")

    def get(self, name: str, race_ref: str, cloth) -> Tuple[str, str]:
        entry = self.entries.get(normalise_name(clean_jockey_name(name)))
        if entry is None:
            self.missing.append({"race": race_ref, "cloth": cloth, "jockey": name,
                                 "problem": "not in lookup"})
            return "", ""
        if not entry["dob"]:
            self.missing.append({"race": race_ref, "cloth": cloth, "jockey": name,
                                 "problem": "no DOB in lookup"})
        return entry["dob"], entry["birth_country"]

    def write_report(self, folder: Path) -> Optional[Path]:
        """Append this run's misses to <folder>/missing_riders.csv."""
        if not self.missing:
            print("[INFO] Every rider found in the lookup with a DOB.")
            return None
        path = folder / "missing_riders.csv"
        new = not path.exists()
        with open(path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["race", "cloth", "jockey", "problem"])
            if new:
                w.writeheader()
            w.writerows(self.missing)
        print(f"[WARN] {len(self.missing)} rider(s) missing or without DOB "
              f"- listed in {path}")
        for m in self.missing:
            print(f"         {m['race']}  cloth {m['cloth']}  {m['jockey']}  ({m['problem']})")
        return path


# ---------------------------------------------------------------------------
# Country codes (Racing Post breeding suffixes) - one table for both scrapers
# ---------------------------------------------------------------------------
# code -> (country name as used by the chart generator, IANA time zone)
# The time zone is for the birth-day window (plan item CH-5 / ENG-2); a large
# country uses the zone of its main breeding region.

COUNTRY_CODES: Dict[str, Tuple[str, str]] = {
    "GB":  ("great britain",  "Europe/London"),
    "IRE": ("ireland",        "Europe/Dublin"),
    "FR":  ("france",         "Europe/Paris"),
    "GER": ("germany",        "Europe/Berlin"),
    "ITY": ("italy",          "Europe/Rome"),
    "SPA": ("spain",          "Europe/Madrid"),
    "POR": ("portugal",       "Europe/Lisbon"),
    "HOL": ("netherlands",    "Europe/Amsterdam"),
    "BEL": ("belgium",        "Europe/Brussels"),
    "SWI": ("switzerland",    "Europe/Zurich"),
    "AUT": ("austria",        "Europe/Vienna"),
    "DEN": ("denmark",        "Europe/Copenhagen"),
    "SWE": ("sweden",         "Europe/Stockholm"),
    "NOR": ("norway",         "Europe/Oslo"),
    "CZE": ("czech republic", "Europe/Prague"),
    "SVK": ("slovakia",       "Europe/Bratislava"),
    "HUN": ("hungary",        "Europe/Budapest"),
    "POL": ("poland",         "Europe/Warsaw"),
    "GR":  ("greece",         "Europe/Athens"),
    "TUR": ("turkey",         "Europe/Istanbul"),
    "RUS": ("russia",         "Europe/Moscow"),
    "USA": ("usa",            "America/New_York"),
    "CAN": ("canada",         "America/Toronto"),
    "MEX": ("mexico",         "America/Mexico_City"),
    "BRZ": ("brazil",         "America/Sao_Paulo"),
    "ARG": ("argentina",      "America/Argentina/Buenos_Aires"),
    "CHI": ("chile",          "America/Santiago"),
    "PER": ("peru",           "America/Lima"),
    "URU": ("uruguay",        "America/Montevideo"),
    "AUS": ("australia",      "Australia/Sydney"),
    "NZ":  ("new zealand",    "Pacific/Auckland"),
    "SAF": ("south africa",   "Africa/Johannesburg"),
    "ZIM": ("zimbabwe",       "Africa/Harare"),
    "MOR": ("morocco",        "Africa/Casablanca"),
    "UAE": ("uae",            "Asia/Dubai"),
    "QA":  ("qatar",          "Asia/Qatar"),
    "QAT": ("qatar",          "Asia/Qatar"),
    "KSA": ("saudi arabia",   "Asia/Riyadh"),
    "IND": ("india",          "Asia/Kolkata"),
    "HK":  ("hong kong",      "Asia/Hong_Kong"),
    "JPN": ("japan",          "Asia/Tokyo"),
    "KOR": ("south korea",    "Asia/Seoul"),
}


# Country name -> IANA time zone, for every country name a CSV can carry:
# the breeding-country names above plus the jockey countries used in
# jockeys_lookup.csv. Used for the local calendar day of a birth (CH-5).
COUNTRY_TZ: Dict[str, str] = {name: tz for name, tz in COUNTRY_CODES.values()}
COUNTRY_TZ.update({
    "england":          "Europe/London",
    "scotland":         "Europe/London",
    "wales":            "Europe/London",
    "northern ireland": "Europe/London",
    "china":            "Asia/Shanghai",
    "kazakhstan":       "Asia/Almaty",
    "romania":          "Europe/Bucharest",
    "swaziland":        "Africa/Mbabane",
})


def country_tz(country: str) -> str:
    """'ireland' -> 'Europe/Dublin'. Unknown country -> ScrapeError."""
    key = (country or "").strip().lower()
    if key not in COUNTRY_TZ:
        raise ScrapeError(f"No time zone for birth country '{country}' - add it to "
                          f"COUNTRY_TZ in racing_common.py")
    return COUNTRY_TZ[key]


def country_from_code(code: Optional[str]) -> str:
    """'(IRE)' / 'IRE' -> 'ireland'. A missing code means GB-bred (Racing Post
    shows no suffix for British-bred horses). Unknown code -> ScrapeError."""
    c = (code or "").strip().strip("()").upper()
    if not c:
        c = "GB"
    if c not in COUNTRY_CODES:
        raise ScrapeError(f"Unknown breeding-country code '{c}' - add it to "
                          f"COUNTRY_CODES in racing_common.py")
    return COUNTRY_CODES[c][0]


# ---------------------------------------------------------------------------
# UK only (decision D4)
# ---------------------------------------------------------------------------

UK_VENUES = {
    "aintree", "ascot", "ayr", "bangor on dee", "bath", "beverley", "brighton",
    "carlisle", "cartmel", "catterick", "chelmsford city", "chelmsford aw",
    "cheltenham", "chepstow", "chester", "doncaster", "epsom", "exeter",
    "fakenham", "ffos las", "fontwell", "fontwell park", "goodwood", "hamilton",
    "haydock", "hereford", "hexham", "huntingdon", "kelso", "kempton",
    "kempton aw", "leicester", "lingfield", "lingfield aw", "ludlow",
    "market rasen", "musselburgh", "newbury", "newcastle", "newcastle aw",
    "newmarket", "newmarket july", "newmarket rowley", "newton abbot",
    "nottingham", "perth", "plumpton", "pontefract", "redcar", "ripon",
    "salisbury", "sandown", "sedgefield", "southwell", "southwell aw",
    "stratford", "taunton", "thirsk", "towcester", "uttoxeter", "warwick",
    "wetherby", "wincanton", "windsor", "wolverhampton", "wolverhampton aw",
    "worcester", "yarmouth", "york",
}


def venue_name(course_key: str) -> str:
    """'newcastle-aw' -> 'newcastle aw'"""
    return (course_key or "").strip().lower().replace("-", " ")


def is_uk(country_code: Optional[str], venue: str) -> bool:
    """Racing Post's own country code decides when present ('GB');
    otherwise an EXACT match on the UK venue list (no partial matching)."""
    if country_code:
        return country_code.strip().upper() == "GB"
    return venue_name(venue) in UK_VENUES


# ---------------------------------------------------------------------------
# Race time - one rule for both scrapers
# ---------------------------------------------------------------------------

def race_time_from_iso(value: str) -> Tuple[date, str]:
    """'2026-09-26T16:35:00+01:00' or '2026-09-29 14:45' -> (date, '16:35').
    The clock time is taken as written: Racing Post gives UK local time."""
    m = re.match(r"\s*(\d{4})-(\d{2})-(\d{2})[T ](\d{1,2}):(\d{2})", value or "")
    if not m:
        raise ScrapeError(f"Unreadable race date/time: {value!r}")
    y, mo, d, h, mi = (int(x) for x in m.groups())
    if not (0 <= h <= 23 and 0 <= mi <= 59):
        raise ScrapeError(f"Invalid race time: {value!r}")
    return date(y, mo, d), f"{h:02d}:{mi:02d}"


def race_time_from_12h(text: str) -> str:
    """LAST RESORT for a time shown without am/pm, e.g. '4:35'.
    UK racing runs from about 10:00 to 21:30, so 1-9 o'clock is afternoon or
    evening (+12); 10, 11 and 12 stand as written; 13-23 are already 24-hour."""
    m = re.search(r"(\d{1,2})[:.](\d{2})", text or "")
    if not m:
        raise ScrapeError(f"No race time found in {text!r}")
    h, mi = int(m.group(1)), int(m.group(2))
    if 1 <= h <= 9:
        h += 12
    if not (10 <= h <= 23) or mi > 59:
        raise ScrapeError(f"Race time {text!r} is outside UK racing hours")
    return f"{h:02d}:{mi:02d}"


# ---------------------------------------------------------------------------
# SP and favourite
# ---------------------------------------------------------------------------

def parse_sp(odds: Optional[str]) -> Tuple[str, bool]:
    """'2/1F' -> ('2/1', True); '11/10JF' / '5/2CF' -> joint/co favourite;
    'EvsF' -> ('Evs', True); '7/1' -> ('7/1', False)."""
    s = (odds or "").strip()
    m = re.match(r"^(.*?)(JF|CF|F)$", s, flags=re.I)
    if m and m.group(1):
        return m.group(1).strip(), True
    return s, False


def sp_decimal(sp: str) -> Optional[float]:
    """'9/1' -> 10.0, 'Evs' -> 2.0; None if unreadable."""
    s = (sp or "").strip().lower()
    if s in ("evs", "evens"):
        return 2.0
    m = re.match(r"^(\d+)\s*/\s*(\d+)$", s)
    if m:
        return int(m.group(1)) / int(m.group(2)) + 1.0
    return None


# ---------------------------------------------------------------------------
# Embedded page data
# ---------------------------------------------------------------------------

def get_next_data(html: str) -> Optional[dict]:
    """The race data Racing Post embeds in every page (<script id="__NEXT_DATA__">)."""
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def initial_state(next_data: Optional[dict]) -> dict:
    return ((next_data or {}).get("props", {}) or {}).get("pageProps", {}).get("initialState", {}) or {}


def find_runner_lists(obj) -> List[list]:
    """Every list of dicts in which each dict has saddleClothNo and horseName."""
    found = []
    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            if o and all(isinstance(x, dict) and "saddleClothNo" in x and "horseName" in x for x in o):
                found.append(o)
            for v in o:
                walk(v)
    walk(obj)
    return found


def find_parent_of(obj, target) -> Optional[dict]:
    """The dict that directly holds `target` as one of its values."""
    if isinstance(obj, dict):
        for v in obj.values():
            if v is target:
                return obj
            r = find_parent_of(v, target)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_parent_of(v, target)
            if r is not None:
                return r
    return None


def is_non_runner_record(r: dict) -> bool:
    """True if a runner record carries any non-runner flag set to true."""
    for k, v in r.items():
        if re.search(r"non_?runner|^nr$|^isNr$", k, flags=re.I) and v not in (None, False, 0, "", "N", "n"):
            return True
    return False


# ---------------------------------------------------------------------------
# Horse profile (DOB + breeding country)
# ---------------------------------------------------------------------------

_PROFILE_CACHE: Dict[str, Tuple[str, str]] = {}
_MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"


def _dob_from_iso(v: str) -> Optional[date]:
    try:
        return datetime.fromisoformat(str(v).replace("Z", "+00:00")).date()
    except Exception:
        return None


def parse_profile_html(html: str, race_day: date) -> Tuple[Optional[date], str]:
    """(foaling date, country code) from a horse profile page."""
    dob = None
    code = ""
    nd = get_next_data(html)
    if nd:
        def walk(o):
            nonlocal dob, code
            if isinstance(o, dict):
                for k, v in o.items():
                    if dob is None and k in ("horseDateOfBirth", "dateOfBirth", "foalingDate") and v:
                        dob = _dob_from_iso(v)
                    if not code and k in ("horseCountryOriginCode", "horseCountryCode") and v:
                        code = str(v)
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(nd)
    if dob is None:
        m = re.search(r'"horseDateOfBirth"\s*:\s*"([^"]+)"', html)
        if m:
            dob = _dob_from_iso(m.group(1))
    if dob is None:
        m = re.search(r'"ageDetails"\s*:\s*"(\d{1,2})(' + _MONTHS + r')(\d{2})', html)
        if m:
            yy = int(m.group(3))
            year = 2000 + yy if 2000 + yy <= race_day.year else 1900 + yy
            dob = datetime.strptime(f"{m.group(1)}{m.group(2)}{year}", "%d%b%Y").date()
    if not code:
        m = re.search(r'"horseCountry(?:Origin)?Code"\s*:\s*"([A-Z]{2,3})"', html)
        if m:
            code = m.group(1)
    if dob is not None and dob >= race_day:
        raise ScrapeError(f"Horse foaling date {dob} is not before the race date {race_day}")
    return dob, code


def fetch_horse_profile(page, profile_url: str, race_day: date) -> Tuple[Optional[date], str]:
    """Open the horse's profile page in the shared browser session."""
    if profile_url in _PROFILE_CACHE:
        return _PROFILE_CACHE[profile_url]
    try:
        page.goto(f"https://www.racingpost.com{profile_url}",
                  wait_until="domcontentloaded", timeout=20000)
        time.sleep(1.5)
        result = parse_profile_html(page.content(), race_day)
    except ScrapeError:
        raise
    except Exception as e:
        print(f"  [WARN] Profile error {profile_url}: {e}")
        result = (None, "")
    _PROFILE_CACHE[profile_url] = result
    time.sleep(1.0)
    return result


def fmt_dob(d: Optional[date]) -> str:
    """CSV DOB format read by racingpost_excel_charts_swiss.py: DD-Mon-YY."""
    return d.strftime("%d-%b-%y") if d else ""
