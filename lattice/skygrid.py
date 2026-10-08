"""skygrid.py RACE [HOURS]  - the race sky every minute from scheduled-time minus HOURS to plus HOURS (default 12).
Same engine and checks as ledger/sky_minutes.py (celestial_bodies_swisseph; the scheduled minute must match TRANS_POS to 1e-6 deg;
TNOs from their linear rate between neighbouring race dates). Minutes are relative to the scheduled time, as in SKYM.
Output: /home/claude/ledger/skygrid/<RACE>__GRID.csv  (body, minute, ra, dec, source)"""
import csv, glob, os, sys
sys.path.insert(0, '/home/claude/rebuild_kit')
import celestial_bodies_swisseph as E, swisseph as swe
EPHE = '/home/claude/ephe'; swe.set_ephe_path(EPHE); E.EPHE_PATH = EPHE
TNOS = dict(E._SWE_TNOS); E._SWE_TNOS = {}
POS = '/home/claude/ledger/allpos'; OUT = '/home/claude/ledger/skygrid'; os.makedirs(OUT, exist_ok=True)
R = sys.argv[1]; H = int(sys.argv[2]) if len(sys.argv) > 2 else 12
MIN = list(range(-60 * H, 60 * H + 1))
def meta(R): return {r[0]: r[1] for r in csv.reader(open(f'{POS}/{R}__META.csv')) if len(r) > 1}
def tpos(R): return {r['body']: (float(r['ra']), float(r['dec'])) for r in csv.DictReader(open(f'{POS}/{R}__TRANS_POS.csv')) if r['ra']}
races = sorted(os.path.basename(f)[:-15] for f in glob.glob(f'{POS}/*__TRANS_POS.csv'))
jds = {Q: E._to_jd_ut(E._parse_time(meta(Q)['race_local_time'], 'Europe/London')) for Q in races}
allT = {Q: tpos(Q) for Q in races}; order = sorted(races, key=lambda Q: jds[Q])
def tno_rate(R, b):
    i = order.index(R); lo = order[i - 1] if i > 0 else order[i + 1]; hi = order[i + 1] if i < len(order) - 1 else order[i - 1]
    if jds[hi] - jds[lo] < 0.5: lo, hi = order[max(0, i - 3)], order[min(len(order) - 1, i + 3)]
    (r1, d1), (r2, d2) = allT[lo][b], allT[hi][b]; dt = jds[hi] - jds[lo]
    return (((r2 - r1 + 180) % 360) - 180) / dt, (d2 - d1) / dt
m = meta(R); lat, lon, el = [float(x) for x in m['racecourse_lat_lon_elev'].split(',')]
jd = jds[R]; T = allT[R]; rows = []
snaps = {k: E.bodies_at(jd + k / 1440, lat, lon, el, True) for k in MIN}
for b in T:
    k = b if b in snaps[0] else b + '_B'
    if b in TNOS:
        vr, vd = tno_rate(R, b); ra, dec = T[b]
        rows += [[b, t, (ra + vr * t / 1440) % 360, dec + vd * t / 1440, 'tno-rate'] for t in MIN]; continue
    if k not in snaps[0]: sys.exit(f'{R}: {b} not produced by engine')
    s0 = snaps[0][k]
    if abs(((s0['ra'] - T[b][0] + 180) % 360) - 180) > 1e-6 or abs(s0['dec'] - T[b][1]) > 1e-6:
        sys.exit(f'{R}: {b} engine {s0["ra"]:.6f},{s0["dec"]:.6f} != TRANS_POS {T[b]}')
    rows += [[b, t, snaps[t][k]['ra'], snaps[t][k]['dec'], 'engine'] for t in MIN]
with open(f'{OUT}/{R}__GRID.csv', 'w', newline='') as o:
    w = csv.writer(o); w.writerow(['body', 'minute', 'ra', 'dec', 'source']); w.writerows(rows)
print(R, 'minutes', MIN[0], 'to', MIN[-1], 'bodies', len(T))
