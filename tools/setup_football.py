#!/usr/bin/env python3
"""setup_football.py MATCH_BATCH_CSV TEAM_XLSX_DIR [STEP_MIN]  (10 Oct 2026, football LITE build in the cloud session)

One match -> the race file set the tools read (ledger/allpos/<M>__META, __NATAL_HOURLY, __Pxx_POS, __TRANS_POS and
ledger/skygrid/<M>__GRID.csv), without the chart workbook. Why: the cloud session has no TNO ephemeris files, so the
chart builder cannot run here (the Mac can: rebuild_kit/charts_football.py).
  - natal: the engine (celestial_bodies_swisseph v2.2, as the chart builder) at every hour of the birth day in the birth
    zone's STANDARD time, country centroid, elevation 0 (identical to the builder's NATAL_HOURLY - checked on a race file);
    the seven TNOs (Eris, Haumea, Makemake, Gonggong, Quaoar, Sedna, Orcus) are not in the cloud engine: taken from
    Eddie's team workbook (12:00 UTC chart) and held for the day (they move <0.005 deg/day).
  - sky: the engine at the ground every STEP_MIN minutes (default 1) from kick-off -60 min to +180 min; TNOs from
    their linear rate between two race-day TRANS_POS files already in ledger/allpos (as skygrid.py does).
  - roles: manager / player; cloth 1 = home, 2 = away; names carry the side number first ('1 Mikel Arteta') as race names do.
The batch CSV is written by rebuild_kit/charts_football.py --batch-only."""
import csv, glob, os, sys, re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
H = os.environ.get('ASTRO_HOME', '/home/claude')
sys.path.insert(0, f'{H}/rebuild_kit'); sys.path.insert(0, f'{H}/scrapers')
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f'{REPO}/rebuild_kit'); sys.path.insert(0, f'{REPO}/scrapers')
import celestial_bodies_swisseph as E, swisseph as swe, openpyxl
import racing_common as rc
import charts_football as CF          # stadiums, extra countries (patches the tables)
import racingpost_excel_charts_swiss as CH
EPHE = f'{H}/ephe'; swe.set_ephe_path(EPHE); E.EPHE_PATH = EPHE
TNOS = list(E._SWE_TNOS); E._SWE_TNOS = {}
POS = f'{H}/ledger/allpos'; GRIDD = f'{H}/ledger/skygrid'; os.makedirs(GRIDD, exist_ok=True)
BATCH, XDIR = sys.argv[1], sys.argv[2]; STEP = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rows = list(csv.DictReader(open(BATCH, encoding='utf-8')))
M = os.path.basename(BATCH)[len('match_'):-4]
ko = datetime.strptime(f"{rows[0]['race_date']} {rows[0]['race_time']}", '%d-%b-%y %H:%M')
ground = rows[0]['racecourse']; lat, lon, el = CF.STADIUMS[ground]
plan = CF.plan_tabs(rows)

def team_xlsx(team):
    f = [p for p in glob.glob(f'{XDIR}/*{team}.xlsx')]
    if len(f) != 1: sys.exit(f'team workbook for {team}: {f}')
    return openpyxl.load_workbook(f[0], read_only=True)
WB = {}
def tno_natal(team, name):
    if team not in WB: WB[team] = team_xlsx(team)
    wb = WB[team]
    for s in wb.sheetnames:
        if not s.startswith('P'): continue
        rr = [r for r in wb[s].iter_rows(min_row=2, values_only=True) if r and len(r) > 8 and r[3] == 'transit_self']
        if rr and rr[0][0] and rr[0][0].strip() == name:
            return {r[1]: (r[4], r[8]) for r in rr if r[1] in TNOS}
    sys.exit(f'{name} not found in the {team} workbook')

# ---- natal: hourly through the birth day in standard time
hourly, natpos, meta_rows = [], {}, []
for tab, role, side, r in plan:
    nm = f"{side} {r['name']}"
    dob, corr = CH.parse_dob(r['dob'], ko.date())
    tzn = rc.country_tz(r['birth_country']); blat, blon = CH.get_birth_coords(r['birth_country'])
    z = ZoneInfo(tzn); noon = datetime(dob.year, dob.month, dob.day, 12, tzinfo=z)
    std = noon.utcoffset() - (noon.dst() or timedelta(0))
    tn = tno_natal(r['team'], r['name'])
    for hr in range(0, 25):
        utc = datetime(dob.year, dob.month, dob.day) + timedelta(hours=hr) - std
        jd = E._to_jd_ut(E._parse_time(utc.strftime('%Y-%m-%d %H:%M'), 'UTC'))
        s = E.bodies_at(jd, blat, blon, 0, True)
        loc = f"{(datetime(dob.year, dob.month, dob.day) + timedelta(hours=hr)).strftime('%Y-%m-%d %H:%M')} UTC{'+' if std >= timedelta(0) else '-'}{abs(int(std.total_seconds()))//3600:02d}:{(abs(int(std.total_seconds()))%3600)//60:02d}"
        pts = {b: (v['ra'], v['dec']) for b, v in s.items() if v.get('ra') is not None and v.get('dec') is not None}
        pts.update(tn)
        for b in sorted(pts, key=str):
            hourly.append([tab, nm, b, hr, loc, utc.strftime('%Y-%m-%d %H:%M'), pts[b][0], pts[b][1]])
        if hr == 12: natpos[tab] = pts
    meta_rows.append([tab, role, side, nm, r['dob'], dob.isoformat(), 'yes' if corr else '', r['birth_country'], tzn,
                      CH.NATAL_TIME, 'OK', '', r['team']])
    print(f'  {tab} {role:7s} {nm}  {dob}  {r["birth_country"]} ({tzn})', file=sys.stderr)

# ---- sky: TNO rates from two race-day TRANS_POS files
def tpos(f): return {q['body']: (float(q['ra']), float(q['dec'])) for q in csv.DictReader(open(f)) if q['ra']}
def rmeta(f): return {q[0]: q[1] for q in csv.reader(open(f)) if len(q) > 1}
cands = []
for f in glob.glob(f'{POS}/*__TRANS_POS.csv'):
    R = os.path.basename(f)[:-15]
    if R.startswith(M): continue
    mf = f'{POS}/{R}__META.csv'
    if not os.path.exists(mf): continue
    tz = 'Asia/Kuala_Lumpur' if 'selangor' in R or 'perak' in R else 'Europe/London'
    try: jd = E._to_jd_ut(E._parse_time(rmeta(mf)['race_local_time'], tz))
    except Exception: continue
    cands.append((jd, R, f))
jd0 = E._to_jd_ut(E._parse_time(ko.strftime('%Y-%m-%d %H:%M'), 'Europe/London'))
cands.sort(key=lambda x: abs(x[0] - jd0))
a = cands[0]; b = next(c for c in cands if abs(c[0] - a[0]) > 3)
TA, TB = tpos(a[2]), tpos(b[2])
def tno(bd, jd):
    (r1, d1), (r2, d2) = TA[bd], TB[bd]; dt = b[0] - a[0]
    vr, vd = (((r2 - r1 + 180) % 360) - 180) / dt, (d2 - d1) / dt
    return (r1 + vr * (jd - a[0])) % 360, d1 + vd * (jd - a[0])
print(f'TNO sky from {a[1]} and {b[1]} ({abs(b[0]-a[0]):.2f} d apart)', file=sys.stderr)
MIN = list(range(-60, 181, STEP))
sched = int(M[-4:-2]) * 60 + int(M[-2:]); kom = ko.hour * 60 + ko.minute
grid, trans = [], {}
for k in MIN:
    s = E.bodies_at(jd0 + k / 1440, lat, lon, el, True)
    pts = {}
    for bd, v in s.items():
        if v.get('ra') is None or v.get('dec') is None: continue
        pts[bd[:-2] if bd.endswith('_B') else bd] = (v['ra'], v['dec'])   # race-day stars: plain names (as skygrid / setup_messi)
    for bd in TNOS: pts[bd] = tno(bd, jd0 + k / 1440)
    for bd in sorted(pts): grid.append([bd, k + (kom - sched), pts[bd][0], pts[bd][1], 'tno-rate' if bd in TNOS else 'engine'])
    if k == 0: trans = pts
DROPN = {'equator', 'Part_of_Fortune', 'Part_of_Spirit', 'Ascendant', 'Midheaven', 'Vertex'}
w = lambda p: csv.writer(open(p, 'w', newline='', encoding='utf-8'))
o = w(f'{GRIDD}/{M}__GRID.csv'); o.writerow(['body', 'minute', 'ra', 'dec', 'source']); o.writerows(grid)
o = w(f'{POS}/{M}__TRANS_POS.csv'); o.writerow(['body', 'ra', 'dec']); o.writerows([[k, *v] for k, v in sorted(trans.items())])
for tab, pts in natpos.items():
    o = w(f'{POS}/{M}__{tab}_POS.csv'); o.writerow(['body', 'ra', 'dec'])
    out = {}
    for k, v in pts.items():
        if k in DROPN: continue
        if k.endswith('_B'): out[k[:-2]] = v                 # stars at birth win over the plain star rows
        elif k not in out: out[k] = v
    o.writerows([[k, *v] for k, v in sorted(out.items())])
o = w(f'{POS}/{M}__NATAL_HOURLY.csv'); o.writerow(['tab', 'name', 'body', 'hour', 'local_time', 'utc_time', 'ra', 'dec']); o.writerows(hourly)
o = w(f'{POS}/{M}__META.csv')
for k, v in [('charts_version', 'football-lite 1.0 (setup_football.py)'), ('engine_file', 'celestial_bodies_swisseph.py'),
             ('engine_version', E.ENGINE_VERSION if hasattr(E, 'ENGINE_VERSION') else '2.2'), ('source_csv', os.path.basename(BATCH)),
             ('racecourse', ground), ('race_local_time', ko.strftime('%Y-%m-%d %H:%M')), ('racecourse_lat_lon_elev', f'{lat}, {lon}, {el}'),
             ('sky_step_min', STEP), ('tno_note', 'natal TNOs from the team workbook (12:00 UTC); sky TNOs by rate')]:
    o.writerow([k, v])
o.writerow([])
o.writerow(['tab', 'role', 'cloth', 'name', 'dob_csv', 'dob_used', 'dob_century_corrected', 'birth_country', 'birth_tz', 'natal_time', 'status', 'cache', 'team'])
o.writerows(meta_rows)
print(f'{M}: {len(plan)} charts, sky {MIN[0]}..{MIN[-1]} min step {STEP} at {ground} ({lat}, {lon}, {el} m)', file=sys.stderr)
