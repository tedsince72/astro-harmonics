"""Set up Ascot 14:35 28 Sep 1996 (Diadem Stakes: Diffident / Frankie Dettori) in the same file formats as the other races.
Workbook from Eddie's Mac (charts v2.3, engine v2.2). Non-TNO sky bodies from the local engine every minute;
TNOs: heliocentric position held fixed from the workbook (geocentric RA/Dec + distance at 14:35), re-projected each minute
from the Swiss Earth position (reflex motion only; own motion ~0.002-0.004 deg/day ignored)."""
import sys, csv, numpy as np, openpyxl
sys.path.insert(0, '/home/claude/rebuild_kit')
import celestial_bodies_swisseph as E, swisseph as swe
EPHE = '/home/claude/ephe'; swe.set_ephe_path(EPHE); E.EPHE_PATH = EPHE
TNOS = dict(E._SWE_TNOS); E._SWE_TNOS = {}
WB = sys.argv[1]; P = '/home/claude/ledger/allpos'; SKY = '/home/claude/ledger/sky'
R = '20120619_ascot_1434'; LAT, LON, EL = 51.4062, -0.6756, 77
jd0 = E._to_jd_ut(E._parse_time('2012-06-19 14:34', 'Europe/London'))
wb = openpyxl.load_workbook(WB, read_only=True)
def selfrows(ws):
    out = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[3] == 'transit_self': out[r[1]] = (r[4], r[8], r[12] if len(r) > 12 else None)
    return out
T = selfrows(wb['TRANS'])
def earth(jd):   # heliocentric equatorial xyz of Earth (J2000-ish frame of the engine is of-date apparent; use same flags as tnofit)
    x, _ = swe.calc_ut(jd, swe.EARTH, swe.FLG_HELCTR | swe.FLG_XYZ | swe.FLG_EQUATORIAL | swe.FLG_TRUEPOS | swe.FLG_NOABERR)
    return np.array(x[:3])
def vec(ra, de, d):
    ra, de = np.radians(ra), np.radians(de); return d * np.array([np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)])
E0 = earth(jd0)
HEL = {b: E0 + vec(T[b][0], T[b][1], T[b][2]) for b in TNOS if b in T}
def tno(b, jd):
    g = HEL[b] - earth(jd); d = np.linalg.norm(g)
    return float(np.degrees(np.arctan2(g[1], g[0])) % 360), float(np.degrees(np.arcsin(g[2] / d)))
s0 = E.bodies_at(jd0, LAT, LON, EL, True)
# check the local engine against the workbook at 14:35
worst = 0
for b in T:
    if b in TNOS: continue
    kk = b if b in s0 else b + '_B'
    if kk not in s0 or s0[kk]['ra'] is None or T[b][0] is None: continue
    dd = max(abs((s0[kk]['ra'] - T[b][0] + 180) % 360 - 180), abs(s0[kk]['dec'] - T[b][1])); worst = max(worst, dd)
    if dd > 1e-4: print('MISMATCH', b, dd, file=sys.stderr)
print('engine vs workbook, worst non-TNO diff (deg):', worst, file=sys.stderr)
for b in HEL: print('TNO check', b, tno(b, jd0), T[b][:2], file=sys.stderr)
bodies = list(T.keys())
rows = []; off = {}
for k in range(-60, 151):
    s = E.bodies_at(jd0 + k / 1440, LAT, LON, EL, True)
    for b in bodies:
        if b in HEL: ra, de = tno(b, jd0 + k / 1440); src = 'tno-reflex'
        else:
            kk = b if b in s else b + '_B'
            if kk not in s or s[kk]['ra'] is None: continue
            ra, de = s[kk]['ra'], s[kk]['dec']; src = 'engine'
        rows.append([b, k, ra, de, src])
        if k == 0: off[b] = (ra, de)
with open(f'{SKY}/{R}__SKYM.csv', 'w', newline='') as o:
    w = csv.writer(o); w.writerow(['body', 'minute', 'ra', 'dec', 'source']); w.writerows(rows)
with open(f'{P}/{R}__TRANS_POS.csv', 'w', newline='') as o:
    w = csv.writer(o); w.writerow(['body', 'ra', 'dec']); w.writerows([[b, *off[b]] for b in off])
for tab in ('P01', 'P02'):
    N = selfrows(wb[tab])
    with open(f'{P}/{R}__{tab}_POS.csv', 'w', newline='') as o:
        w = csv.writer(o); w.writerow(['body', 'ra', 'dec']); w.writerows([[b, v[0], v[1]] for b, v in N.items()])
for sh in ('META', 'NATAL_HOURLY'):
    with open(f'{P}/{R}__{sh}.csv', 'w', newline='') as o:
        w = csv.writer(o)
        for r in wb[sh].iter_rows(values_only=True):
            r = ['' if v is None else v for v in r]
            if r and r[0] == 'racecourse': r[1] = 'ascot (Queen Anne Stakes)'
            if r and r[0] == 'race_local_time': r[1] = '2012-06-19 14:34'
            if r and r[0] == 'racecourse_lat_lon_elev': r[1] = '51.4062, -0.6756, 77'
            w.writerow(r)
print('done', R, len(rows), 'sky rows', file=sys.stderr)
# --- 7 Oct fix: plain star names (Algol_B -> Algol), drop duplicate extra-star rows, POS files in the usual layout
def _fix(path, drop=()):
    rows = list(csv.reader(open(path))); hdr = rows[0]; out = [hdr]; seen = set()
    for r in rows[1:]:
        b = r[0]
        if b in drop: continue
        if b.endswith('_B'): b = b[:-2]
        key = (b, r[1]) if 'minute' in hdr else (b,)
        if key in seen: continue
        seen.add(key); out.append([b] + r[1:])
    csv.writer(open(path, 'w', newline='')).writerows(out)
_fix(f'{SKY}/{R}__SKYM.csv'); _fix(f'{P}/{R}__TRANS_POS.csv')
for tab in ('P01', 'P02'): _fix(f'{P}/{R}__{tab}_POS.csv', drop=('equator', 'Part_of_Fortune', 'Part_of_Spirit', 'Ascendant', 'Midheaven', 'Vertex'))
