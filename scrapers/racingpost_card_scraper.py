#!/usr/bin/env python3
"""
racingpost_card_scraper.py  v2.0
--------------------------------
Scrapes UK race cards from Racing Post into the race_batch CSV format shared
with racingpost_results_scraper.py (see racing_common.py).

Output: one CSV per race, e.g.
  racecards/20260929_uk_all/race_batch_20260929_ayr_1438.csv

Rules (plan items CARD-1, CARD-2, CARD-3, CARD-5, CARD-6, D4):
  - Same CSV columns as the results scraper. finish_pos / sp / is_fav stay
    blank on racecards (no result information).
  - Race time: the 24-hour time in the page data first; the 12-hour
    fallback is the one shared rule in racing_common.
  - Non-runners are kept with status NR (the chart step skips them), and are
    not counted for --min-runners / --max-runners.
  - UK venues only (Racing Post country code GB, or an exact venue match).
  - Any problem stops that race with a clear message; the run carries on
    and exits with code 1 if any race failed.
  - Riders missing from the lookup are listed in missing_riders.csv.
  - Scrape as close to the off as practical, so late non-runners and jockey
    changes are picked up.

Usage:
  python racingpost_card_scraper.py --lookup jockeys_lookup.csv --max-runners 8
  python racingpost_card_scraper.py --lookup jockeys_lookup.csv --course ayr
  python racingpost_card_scraper.py --lookup jockeys_lookup.csv --date 2026-09-30
  # Offline check of a saved racecard page (no browser, no profile pages)
  python racingpost_card_scraper.py --lookup jockeys_lookup.csv --html "Ayr 14.38.html"
"""

import argparse
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import racing_common as rc

SCRIPT_VERSION = "2.0"

_TIME_KEYS = ("localRaceDatetime", "raceDatetime", "raceDateTime", "startDateTime",
              "localStartDateTime")


def _first(d: Dict, keys, default=None):
    for k in keys:
        v = d.get(k)
        if v not in (None, ""):
            return v
    return default


def _name_of(v) -> str:
    """A name field may be a string or a small dict holding the name."""
    if isinstance(v, dict):
        v = _first(v, ("name", "jockeyName", "displayName"), "")
    return (v or "").strip()


# ---------------------------------------------------------------------------
# Parsing the embedded race data (pure - testable on a saved page)
# ---------------------------------------------------------------------------

def _profile_url(url: str) -> str:
    """'/profile/horse/9777142/divide-and-conquer/form#race-id=…' -> '/profile/horse/9777142/divide-and-conquer/'"""
    url = (url or "").split("#")[0]
    return re.sub(r"/form/?$", "/", url)


def parse_racepage_data(state: Dict) -> Optional[Dict]:
    """Racecard page layout confirmed on Bath 15:32, 29/09/2026:
    initialState.racePage.data = {race: {...}, runners: [...]}"""
    data = (state.get("racePage") or {}).get("data")
    if not isinstance(data, dict) or not isinstance(data.get("runners"), list):
        return None
    race = data.get("race") or {}
    iso = _first(race, ("raceTime", "startDateTime", "localMeetingRaceDateTime"))
    if not iso:
        raise rc.ScrapeError("Racecard data has no race time")
    race_day, race_time = rc.race_time_from_iso(str(iso))
    runners = []
    for r in data["runners"]:
        status = "NR" if r.get("nonRunner") else "runner"
        cloth = r.get("startNumber")
        if cloth in (None, "") and status == "runner":
            raise rc.ScrapeError(f"Runner {r.get('horseName')!r} has no cloth number")
        if r.get("irishReserve") and status == "runner":
            print(f"  [NOTE] {r.get('horseName')} is listed as a reserve")
        runners.append({
            "cloth": int(cloth) if cloth not in (None, "") else None,
            "horse": (r.get("horseName") or "").strip(),
            "horse_url": _profile_url(r.get("horseUrl")),
            "horse_code": r.get("countryOrigin") or "",
            "jockey": rc.clean_jockey_name(r.get("jockeyName") or ""),
            "status": status,
        })
    declared = race.get("numberOfRunners")
    running = sum(1 for r in runners if r["status"] == "runner")
    if declared and declared != running:
        print(f"  [NOTE] Card states {declared} runners, {running} found after non-runners")
    return {"race_day": race_day, "race_time": race_time,
            "venue": rc.venue_name(race.get("courseKey") or race.get("courseName") or ""),
            "country_code": race.get("countryCode") or "", "runners": runners}


def parse_card_html(html: str) -> Optional[Dict]:
    """
    Read one racecard page from its embedded data. Returns None if the page
    has no runner data (the caller then reads the page itself).
    Returns {race_day, race_time, venue, country_code, runners:[...]}.
    """
    nd = rc.get_next_data(html)
    state = rc.initial_state(nd)
    known = parse_racepage_data(state)
    if known is not None:
        return known
    # Generic search (e.g. a results-style runner list) if the layout changes
    lists = rc.find_runner_lists(state)
    if not lists:
        return None
    runner_list = max(lists, key=len)
    parent = rc.find_parent_of(state, runner_list) or {}

    # Race time/venue: only from the dict that holds THIS race's runners (the
    # page also carries other races' times in its meeting index).
    iso = _first(parent, _TIME_KEYS)
    header = parent.get("header") or parent.get("raceInfo") or {}
    if not iso and isinstance(header, dict):
        iso = _first(header, _TIME_KEYS)
    if iso:
        race_day, race_time = rc.race_time_from_iso(str(iso))
    else:
        t12 = _first(parent, ("raceTime", "time")) or (header.get("raceTime") if isinstance(header, dict) else "")
        if not t12:
            raise rc.ScrapeError("Runner data found but no race time next to it")
        race_time = rc.race_time_from_12h(str(t12))
        race_day = None
        print(f"  [WARN] No 24-hour time in page data - used 12-hour fallback: {race_time}")

    venue = rc.venue_name(_first(parent, ("courseKey", "courseName", "venueName"), "")
                          or (header.get("courseDisplayName", "") if isinstance(header, dict) else ""))
    country_code = _first(parent, ("countryCode",), "")

    runners = []
    for r in runner_list:
        cloth = r.get("saddleClothNo")
        status = "NR" if rc.is_non_runner_record(r) else "runner"
        if cloth in (None, "") and status == "runner":
            raise rc.ScrapeError(f"Runner {r.get('horseName')!r} has no cloth number")
        runners.append({
            "cloth": int(cloth) if cloth not in (None, "") else None,
            "horse": (r.get("horseName") or "").strip(),
            "horse_url": (_first(r, ("horseUrl", "horseProfileUrl"), "") or "").split("#")[0],
            "horse_code": _first(r, ("horseSuffix", "horseCountryOriginCode", "horseCountryCode",
                                     "countryOriginCode"), ""),
            "jockey": rc.clean_jockey_name(_name_of(_first(r, ("jockeyName", "jockey"), ""))),
            "status": status,
        })
    return {"race_day": race_day, "race_time": race_time, "venue": venue,
            "country_code": country_code, "runners": runners}


# ---------------------------------------------------------------------------
# Fallback: read the page itself (previous scraper's method)
# ---------------------------------------------------------------------------

def read_card_from_page(page) -> Dict:
    title_time = rc.race_time_from_12h(page.title())
    blocks = page.locator("[data-testid='Container__RunnerRowDesktop']").all()
    if not blocks:
        raise rc.ScrapeError("No runner data in page data and no runner rows on page "
                             "- Racing Post layout may have changed")
    runners = []
    for block in blocks:
        cloth = horse = jockey = horse_url = code = ""
        try:
            spans = block.locator("[data-testid='Container__RunnerNumber'] span").all()
            if spans:
                cloth = spans[0].inner_text().strip().rstrip(".")
        except Exception:
            pass
        try:
            link = block.locator("[data-testid='Link__Horse']").first
            if link.count() > 0:
                horse_url = (link.get_attribute("href") or "").split("#")[0]
                for span in link.locator("span").all():
                    t = span.inner_text().strip().strip("()")
                    if t.upper() in rc.COUNTRY_CODES:
                        code = t.upper()
                    elif t and not horse:
                        horse = t
        except Exception:
            pass
        try:
            jl = block.locator("[data-testid='Link__Jockey']").first
            if jl.count() > 0:
                jockey = rc.clean_jockey_name(jl.inner_text().strip())
        except Exception:
            pass
        text = ""
        try:
            text = block.inner_text()
        except Exception:
            pass
        status = "NR" if re.search(r"\bNR\b|Non[- ]?runner", text, flags=re.I) else "runner"
        if not horse:
            continue
        if not cloth.isdigit() and status == "runner":
            raise rc.ScrapeError(f"Runner {horse!r} has no readable cloth number")
        runners.append({"cloth": int(cloth) if cloth.isdigit() else None, "horse": horse,
                        "horse_url": horse_url, "horse_code": code, "jockey": jockey,
                        "status": status})
    print("  [WARN] Read from the page layout (fallback) - please check this race's CSV")
    return {"race_day": None, "race_time": title_time, "venue": "",
            "country_code": "", "runners": runners}


# ---------------------------------------------------------------------------
# One race
# ---------------------------------------------------------------------------

def process_race(race: Dict, target_date: date, index_venue: str,
                 lookup: rc.JockeyLookup, folder: Path, page=None,
                 min_runners=None, max_runners=None) -> Optional[Path]:
    race_day = race["race_day"] or target_date
    venue = race["venue"] or index_venue
    if race_day != target_date:
        raise rc.ScrapeError(f"Page date {race_day} differs from target date {target_date}")
    if not rc.is_uk(race["country_code"], venue):
        print(f"  [SKIP] {venue} ({race['country_code'] or 'no code'}) - not a UK race")
        return None

    running = [r for r in race["runners"] if r["status"] == "runner"]
    cloths = [r["cloth"] for r in running]
    if len(set(cloths)) != len(cloths):
        raise rc.ScrapeError(f"Duplicate cloth numbers: {sorted(cloths)}")
    if max_runners and len(running) > max_runners:
        print(f"  [SKIP] {len(running)} runners > max {max_runners}")
        return None
    if min_runners and len(running) < min_runners:
        print(f"  [SKIP] {len(running)} runners < min {min_runners}")
        return None

    fname = rc.race_filename(race_day, venue, race["race_time"])
    race_ref = fname[:-4]
    for r in race["runners"]:
        r["horse_dob"] = ""
        r["horse_country"] = ""
        if r["status"] == "NR":
            continue
        r["horse_country"] = rc.country_from_code(r["horse_code"])
        if page is not None and r["horse_url"]:
            dob, profile_code = rc.fetch_horse_profile(page, r["horse_url"], race_day)
            r["horse_dob"] = rc.fmt_dob(dob)
            if profile_code:
                prof_country = rc.country_from_code(profile_code)
                if prof_country != r["horse_country"]:
                    print(f"  [WARN] {r['horse']}: page says {r['horse_country']}, "
                          f"profile says {prof_country} - using profile")
                    r["horse_country"] = prof_country
            if not r["horse_dob"]:
                lookup.missing.append({"race": race_ref, "cloth": r["cloth"],
                                       "jockey": f"(horse) {r['horse']}",
                                       "problem": "horse DOB not found on profile"})
        if r["jockey"]:
            r["jockey_dob"], r["jockey_country"] = lookup.get(r["jockey"], race_ref, r["cloth"])
        else:
            lookup.missing.append({"race": race_ref, "cloth": r["cloth"],
                                   "jockey": "(none declared)", "problem": "no jockey on card"})

    rows = rc.build_rows(race_day.strftime("%d-%b-%y"), race["race_time"], venue, race["runners"])
    path = folder / fname
    rc.write_race_csv(path, rows)
    nr = len(race["runners"]) - len(running)
    print(f"  {venue} {race['race_time']}  {len(running)} runners" + (f", {nr} NR" if nr else ""))
    print(f"  → Saved: {fname}")
    return path


# ---------------------------------------------------------------------------
# Race discovery
# ---------------------------------------------------------------------------

def discover_race_urls(page, target_date: date, course_filter: Optional[str],
                       direct_url: Optional[str]) -> List[Tuple[str, str]]:
    """[(venue, race_url)] for UK races on target_date."""
    pattern = re.compile(r"/racecards/(\d+)/([a-z\-]+)/" + re.escape(target_date.isoformat())
                         + r"/(\d+)/?")
    races, seen = [], set()

    if direct_url:
        m = re.search(r"/racecards/\d+/([a-z\-]+)/", direct_url)
        url_venue = rc.venue_name(m.group(1)) if m else ""
        page.goto(direct_url, wait_until="networkidle", timeout=40000)
        time.sleep(4)
        for link in page.locator("a").all():
            href = link.get_attribute("href") or ""
            m2 = pattern.match(href)
            if m2 and rc.venue_name(m2.group(2)) == url_venue and m2.group(3) not in seen:
                seen.add(m2.group(3))
                races.append((url_venue, f"https://www.racingpost.com{href}"))
        return races

    index_url = f"https://www.racingpost.com/racecards/{target_date.isoformat()}"
    print(f"[INFO] Loading index: {index_url}")
    page.goto(index_url, wait_until="networkidle", timeout=40000)
    time.sleep(4)
    state = rc.initial_state(rc.get_next_data(page.content()))
    for meeting in (state.get("raceCards") or {}).get("meetings", []) or []:
        venue = rc.venue_name(meeting.get("courseKey", ""))
        if not rc.is_uk(meeting.get("countryCode"), venue):
            print(f"  [SKIP] {venue} ({meeting.get('countryCode') or 'no code'}) - not UK")
            continue
        for race in meeting.get("races", []) or []:
            url = race.get("raceUrl", "")
            rid = url.strip("/").split("/")[-1] if url else ""
            if url and rid not in seen:
                seen.add(rid)
                races.append((venue, f"https://www.racingpost.com{url}"))
    if not races:
        raise rc.ScrapeError("No races found in the racecard index page data")
    if course_filter:
        cf = rc.venue_name(course_filter)
        races = [(v, u) for v, u in races if v == cf or v.startswith(cf + " ")]
        if not races:
            raise rc.ScrapeError(f"No UK races matched course '{course_filter}'")
    print(f"[INFO] {len(races)} UK race(s) found")
    return races


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description=f"Racing Post UK racecard scraper v{SCRIPT_VERSION}")
    p.add_argument("--lookup", required=True)
    p.add_argument("--course", default=None, help="One course, e.g. 'ayr' or 'newcastle-aw'")
    p.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    p.add_argument("--outdir", default=".")
    p.add_argument("--url", default=None, help="Direct meeting URL")
    p.add_argument("--html", default=None, help="Saved racecard page (.html) - offline, no profiles")
    p.add_argument("--min-runners", type=int, default=None, help="Declared runners, NRs excluded")
    p.add_argument("--max-runners", type=int, default=None, help="Declared runners, NRs excluded")
    p.add_argument("--uk-only", action="store_true",
                   help="Kept for compatibility: UK-only is now always on (decision D4)")
    p.add_argument("--skip-races", type=int, default=0, help="Skip the first N races (resume)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    print(f"racingpost_card_scraper.py v{SCRIPT_VERSION} (racing_common v{rc.COMMON_VERSION})")
    target_date = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
    lookup = rc.JockeyLookup(args.lookup)
    suffix = rc.venue_name(args.course).replace(" ", "_") if args.course else "uk_all"
    folder = Path(args.outdir) / "racecards" / f"{target_date.strftime('%Y%m%d')}_{suffix}"
    folder.mkdir(parents=True, exist_ok=True)
    failures: List[Tuple[str, str]] = []
    written: List[Path] = []

    if args.html:
        html = Path(args.html).read_text(encoding="utf-8", errors="replace")
        try:
            race = parse_card_html(html)
            if race is None:
                raise rc.ScrapeError("No runner list in the saved page's data - send this "
                                     "page so the reader can be matched to it")
            if race["race_day"] and not args.date:
                target_date = race["race_day"]
                folder = Path(args.outdir) / "racecards" / f"{target_date.strftime('%Y%m%d')}_{suffix}"
                folder.mkdir(parents=True, exist_ok=True)
            p = process_race(race, target_date, "", lookup, folder, None,
                             args.min_runners, args.max_runners)
            if p:
                written.append(p)
                print("  [INFO] Offline mode: horse DOBs not fetched (profile pages need the browser)")
        except rc.ScrapeError as e:
            failures.append((args.html, str(e)))
    else:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
                viewport={"width": 1280, "height": 800},
                locale="en-GB", timezone_id="Europe/London",
            )
            page = context.new_page()
            try:
                races = discover_race_urls(page, target_date, args.course, args.url)
            except rc.ScrapeError as e:
                print(f"[ERROR] {e}")
                browser.close()
                return 1
            for i, (venue, url) in enumerate(races, 1):
                if i <= args.skip_races:
                    continue
                print(f"[INFO] Race {i}/{len(races)}: {url}")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    time.sleep(3)
                    race = parse_card_html(page.content()) or read_card_from_page(page)
                    p = process_race(race, target_date, venue, lookup, folder, page,
                                     args.min_runners, args.max_runners)
                    if p:
                        written.append(p)
                except rc.ScrapeError as e:
                    print(f"  [FAILED] {e}")
                    failures.append((url, str(e)))
                except Exception as e:
                    print(f"  [FAILED] {type(e).__name__}: {e}")
                    failures.append((url, f"{type(e).__name__}: {e}"))
                time.sleep(2.5)
            browser.close()

    lookup.write_report(folder)
    print(f"\n[RESULT] {len(written)} race file(s) written to {folder}")
    if failures:
        print(f"[RESULT] {len(failures)} race(s) FAILED:")
        for where, why in failures:
            print(f"         {where}\n           {why}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
