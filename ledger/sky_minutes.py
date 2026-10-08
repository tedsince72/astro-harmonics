#!/usr/bin/env python3
"""sky_minutes.py v1.0 (3 Oct 2026) - the race sky minute by minute through the race.
Eddie 12:54-12:56: applying at the off and peaking shortly after still counts (the race is still being run);
flat races last ~1 minute, jump races up to ~12 minutes - so the sky is computed every minute from the off to
+15, plus -30 -20 -15 -10 -5 -2 -1 and +20 +30 for context.
Same engine and checks as sky_motion.py v1.1 (celestial_bodies_swisseph.py v2.2; the off must match TRANS_POS to
1e-6 deg, else stop; TNOs from their linear rate between neighbouring race dates).
Output: <out>/<race>__SKYM.csv  long format: body, minute, ra, dec, source
Usage: python3 sky_minutes.py --pos DIR --out DIR"""
import argparse, csv, glob, os, sys
sys.path.insert(0, '/home/claude/rebuild_kit')
import celestial_bodies_swisseph as E, swisseph as swe
EPHE = '/home/claude/ephe'; swe.set_ephe_path(EPHE); E.EPHE_PATH = EPHE
TNOS = dict(E._SWE_TNOS); E._SWE_TNOS = {}
ap = argparse.ArgumentParser(); ap.add_argument('--pos', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
MINUTES = [-30, -20, -15, -10, -5, -2, -1] + list(range(0, 16)) + [20, 30]

def meta(R):
    return {r[0]: r[1] for r in csv.reader(open(f'{a.pos}/{R}__META.csv')) if len(r) > 1}
def tpos(R):
    return {r['body']: (float(r['ra']), float(r['dec'])) for r in csv.DictReader(open(f'{a.pos}/{R}__TRANS_POS.csv')) if r['ra']}
races = sorted(os.path.basename(f)[:-15] for f in glob.glob(f'{a.pos}/*__TRANS_POS.csv'))
jds = {R: E._to_jd_ut(E._parse_time(meta(R)['race_local_time'], 'Europe/London')) for R in races}
allT = {R: tpos(R) for R in races}
order = sorted(races, key=lambda R: jds[R])

def tno_rate(R, b):
    i = order.index(R); lo = order[i - 1] if i > 0 else order[i + 1]; hi = order[i + 1] if i < len(order) - 1 else order[i - 1]
    if jds[hi] - jds[lo] < 0.5:
        lo, hi = order[max(0, i - 3)], order[min(len(order) - 1, i + 3)]
    (r1, d1), (r2, d2) = allT[lo][b], allT[hi][b]; dt = jds[hi] - jds[lo]
    return (((r2 - r1 + 180) % 360) - 180) / dt, (d2 - d1) / dt

for R in races:
    m = meta(R); lat, lon, el = [float(x) for x in m['racecourse_lat_lon_elev'].split(',')]
    jd = jds[R]; T = allT[R]; rows = []
    snaps = {k: E.bodies_at(jd + k / 1440, lat, lon, el, True) for k in MINUTES}
    for b in T:
        k = b if b in snaps[0] else b + '_B'
        if b in TNOS:
            vr, vd = tno_rate(R, b); ra, dec = T[b]
            rows += [[b, t, (ra + vr * t / 1440) % 360, dec + vd * t / 1440, 'tno-rate'] for t in MINUTES]
            continue
        if k not in snaps[0]:
            sys.exit(f'{R}: {b} not produced by engine')
        s0 = snaps[0][k]
        if abs(((s0['ra'] - T[b][0] + 180) % 360) - 180) > 1e-6 or abs(s0['dec'] - T[b][1]) > 1e-6:
            sys.exit(f'{R}: {b} engine {s0["ra"]:.6f},{s0["dec"]:.6f} != TRANS_POS {T[b]}')
        rows += [[b, t, snaps[t][k]['ra'], snaps[t][k]['dec'], 'engine'] for t in MINUTES]
    with open(f'{a.out}/{R}__SKYM.csv', 'w', newline='') as o:
        w = csv.writer(o); w.writerow(['body', 'minute', 'ra', 'dec', 'source']); w.writerows(rows)
print('races', len(races))
