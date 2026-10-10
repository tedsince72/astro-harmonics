#!/usr/bin/env python3
"""charts_football.py v1.0 (10 Oct 2026) - one football match -> one chart workbook in the race layout.

Wraps racingpost_excel_charts_swiss.py v2.3 (same engine, same natal rule: 12:00 standard time in the birth country,
country centroid, NATAL_HOURLY through the birth day). Only three things change for football:
  - the plan of tabs: home manager P01, home players P02.., away manager, away players (role manager / player,
    cloth 1 = home, 2 = away) instead of horse / jockey by cloth;
  - the ground's coordinates (home club's stadium, same list as epl_transit_charts.py);
  - birth countries the racing tables lack (centroid + time zone).
TRANS is the sky at kick-off at the ground.

Usage:
  python3 charts_football.py --fixtures reference/football/epl_fixtures_GW06.csv --squads reference/football/squads \
      --match arsenal --outdir DIR --ephemeris-path /home/claude/ephe --engine celestial_bodies_swisseph.py
The fixtures CSV is the scraper's: race_time there is kick-off + 60 min, so kick-off = race_time - 60 min.
Writes DIR/match_<YYYYMMDD>_<home>_<HHMM>.csv (the batch) and .xlsx (the workbook)."""
import argparse, csv, os, re, sys
from datetime import datetime, timedelta
from pathlib import Path
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'scrapers'))
import racing_common as rc
import racingpost_excel_charts_swiss as CH

FOOTBALL_VERSION = "1.0"

# stadium coordinates (lat, lon, elev m) - as epl_transit_charts.py (Eddie's list); keys are the batch 'racecourse'
STADIUMS = {
    "arsenal": (51.5549, -0.1084, 29), "aston villa": (52.5090, -1.8847, 99), "bournemouth": (50.7352, -1.8381, 10),
    "brentford": (51.4915, -0.2889, 10), "brighton": (50.8618, -0.0839, 25), "chelsea": (51.4816, -0.1910, 8),
    "coventry": (52.4521, -1.5217, 87), "crystal palace": (51.3983, -0.0856, 73), "everton": (53.4388, -2.9611, 6),
    "fulham": (51.4749, -0.2217, 6), "hull city": (53.7463, -0.3674, 4), "ipswich town": (52.0550, 1.1449, 9),
    "leeds united": (53.7774, -1.5724, 57), "liverpool": (53.4308, -2.9608, 22), "manchester city": (53.4831, -2.2004, 51),
    "manchester united": (53.4631, -2.2913, 49), "newcastle united": (54.9756, -1.6218, 27),
    "nottingham forest": (52.9399, -1.1327, 34), "sunderland": (54.9146, -1.3876, 20), "tottenham": (51.6043, -0.0665, 34),
    "west ham": (51.5386, 0.0164, 19), "wolverhampton": (52.5900, -2.1302, 149),
}
# the scraper's clipped names (and the full names) -> squad file stem
TEAM = {
    "arsenal": "arsenal", "leeds": "leeds_united", "sunderland": "sunderland", "brighton": "brighton", "chelsea": "chelsea",
    "bournemouth": "bournemouth", "ipswich": "ipswich_town", "fulham": "fulham", "aston": "aston_villa", "aston villa": "aston_villa",
    "brentford": "brentford", "tottenham": "tottenham", "hull city": "hull_city", "everton": "everton", "crystal": "crystal_palace",
    "crystal palace": "crystal_palace", "nottingham": "nottingham_forest", "nottingham forest": "nottingham_forest",
    "liverpool": "liverpool", "coventry": "coventry", "newcastle": "newcastle_united",
    "manchester united": "manchester_united", "manchester city": "manchester_city",
}
# GW06 (10-12 Oct 2026): the scraper writes both Manchester clubs as 'Manchester' - which is which, by match id
# (fifplay Matchday 6: Man United v Tottenham Sat 17:30 at Old Trafford; Liverpool v Man City Sun 16:30 at Anfield)
MANCHESTER = {"560600": "manchester_united", "560598": "manchester_city"}

# birth countries the racing tables lack: centroid (lat, lon) and the zone of the capital
EXTRA = {
    "algeria": ((28.0339, 1.6596), "Africa/Algiers"), "bosnia and herzegovina": ((43.9159, 17.6791), "Europe/Sarajevo"),
    "burkina faso": ((12.2383, -1.5616), "Africa/Ouagadougou"), "cameroon": ((7.3697, 12.3547), "Africa/Douala"),
    "colombia": ((4.5709, -74.2973), "America/Bogota"), "croatia": ((45.1000, 15.2000), "Europe/Zagreb"),
    "ecuador": ((-1.8312, -78.1834), "America/Guayaquil"), "gambia": ((13.4432, -15.3101), "Africa/Banjul"),
    "georgia": ((42.3154, 43.3569), "Asia/Tbilisi"), "ghana": ((7.9465, -1.0232), "Africa/Accra"),
    "ivory coast": ((7.5400, -5.5471), "Africa/Abidjan"), "jamaica": ((18.1096, -77.2975), "America/Jamaica"),
    "mozambique": ((-18.6657, 35.5296), "Africa/Maputo"), "nigeria": ((9.0820, 8.6753), "Africa/Lagos"),
    "paraguay": ((-23.4425, -58.4438), "America/Asuncion"), "senegal": ((14.4974, -14.4524), "Africa/Dakar"),
    "serbia": ((44.0165, 21.0059), "Europe/Belgrade"), "slovenia": ((46.1512, 14.9955), "Europe/Ljubljana"),
    "ukraine": ((48.3794, 31.1656), "Europe/Kyiv"),
}
for k, (cen, tz) in EXTRA.items():
    CH.COUNTRY_CENTROIDS.setdefault(k, cen); rc.COUNTRY_TZ.setdefault(k, tz)
CH.RACECOURSE_COORDS.update(STADIUMS)
CH.CHARTS_VERSION = f"{CH.CHARTS_VERSION}+football{FOOTBALL_VERSION}"


def plan_tabs(subjects):
    """home manager, home players, away manager, away players - in the squad file's order (manager first)."""
    plan, k = [], 0
    for side in ("1", "2"):
        rows = [s for s in subjects if s.get("cloth") == side]
        mg = [s for s in rows if s["subject_type"] == "manager"]
        if len(mg) != 1: raise CH.ChartError(f"side {side}: {len(mg)} manager rows (need 1)")
        for s in mg + [s for s in rows if s["subject_type"] == "player"]:
            k += 1; plan.append((f"P{k:02d}", s["subject_type"], int(side), s))
    return plan
CH.plan_tabs = plan_tabs


def squad(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    return rows[0], rows[1:]      # the squad files list the manager first


def batch(fix, squads_dir, out_dir):
    ko = datetime.strptime(f"{fix['race_date']} {fix['race_time']}", "%Y-%m-%d %H:%M") - timedelta(minutes=60)
    h = MANCHESTER.get(fix["match_id"]) if fix["home_team"].lower() == "manchester" else TEAM[fix["home_team"].lower()]
    a = MANCHESTER.get(fix["match_id"]) if fix["away_team"].lower() == "manchester" else TEAM[fix["away_team"].lower()]
    ground = h.replace("_", " ")
    mid = f"{ko:%Y%m%d}_{h}_{ko:%H%M}"
    rows = []
    for side, team in (("1", h), ("2", a)):
        m, ps = squad(f"{squads_dir}/{team}.csv")
        for i, r in enumerate([m] + ps):
            rows.append(dict(race_date=f"{ko:%d-%b-%y}", race_time=f"{ko:%H:%M}", racecourse=ground,
                             subject_type="manager" if i == 0 else "player", cloth=side, name=r["name"].strip(),
                             dob=r["dob"], birth_country=r["birth_country"], finish_pos="", sp="", is_fav="", status="runner", team=team))
    os.makedirs(out_dir, exist_ok=True)
    p = Path(out_dir) / f"match_{mid}.csv"
    with open(p, "w", newline="", encoding="utf-8") as o:
        w = csv.DictWriter(o, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return p, mid, ko, h, a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", required=True); ap.add_argument("--squads", required=True)
    ap.add_argument("--match", required=True, help="home squad stem (e.g. arsenal) or match_id, or 'all'")
    ap.add_argument("--outdir", required=True); ap.add_argument("--ephemeris-path", default=".")
    ap.add_argument("--engine", default=os.path.join(HERE, "celestial_bodies_swisseph.py")); ap.add_argument("--hip-path", default=".")
    ap.add_argument("--batch-only", action="store_true")
    a = ap.parse_args()
    fx = list(csv.DictReader(open(a.fixtures, encoding="utf-8")))
    done = 0
    for f in fx:
        p, mid, ko, h, aw = batch(f, a.squads, a.outdir)
        if a.match not in ("all", h, f["match_id"], mid): os.remove(p); continue
        print(f"[MATCH] {mid}: {h} v {aw}, kick-off {ko:%Y-%m-%d %H:%M} UK")
        done += 1
        if a.batch_only: continue
        args = argparse.Namespace(csv=str(p), outdir=a.outdir, ephemeris_path=a.ephemeris_path, hip_path=a.hip_path, engine=a.engine)
        try: CH.build(args)
        except CH.ChartError as e: print(f"[FAILED] {mid}: {e}"); return 1
    if not done: print("no match selected"); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
