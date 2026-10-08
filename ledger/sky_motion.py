#!/usr/bin/env python3
"""sky_motion.py v1.1 - race sky at the off, 2 minutes and 30 minutes either side, for applying / separating
(v1.1: +/-2 minutes added - the direction AT the off; +/-30 shows how long a contact lasts).
Every body except the seven TNOs is recalculated with the project engine (celestial_bodies_swisseph.py
v2.2, same frame and settings); the off is checked against TRANS_POS (must match to 1e-6 deg, else stop).
The TNO ephemeris files are not in this workspace, so TNO motion is taken from their TRANS_POS
positions across all 96 race dates (linear rate between the nearest earlier and later race; in 30
minutes a TNO moves ~0.0003 deg, parallax is negligible).
Output: <out>/<race>__SKY3.csv  body, ra_m30, dec_m30, ra_m2, dec_m2, ra_0, dec_0, ra_p2, dec_p2, ra_p30, dec_p30, source
Usage: python3 sky_motion.py --pos DIR --out DIR"""
import argparse, csv, glob, os, sys
from datetime import datetime
sys.path.insert(0, '/home/claude/rebuild_kit')
import celestial_bodies_swisseph as E, swisseph as swe
EPHE = '/home/claude/ephe'; swe.set_ephe_path(EPHE); E.EPHE_PATH = EPHE
TNOS = dict(E._SWE_TNOS); E._SWE_TNOS = {}
ap = argparse.ArgumentParser(); ap.add_argument('--pos', required=True); ap.add_argument('--out', required=True)
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)

def meta(R):
    return {r[0]: r[1] for r in csv.reader(open(f'{a.pos}/{R}__META.csv')) if len(r) > 1}
def tpos(R):
    return {r['body']: (float(r['ra']), float(r['dec'])) for r in csv.DictReader(open(f'{a.pos}/{R}__TRANS_POS.csv')) if r['ra']}
races = sorted(os.path.basename(f)[:-15] for f in glob.glob(f'{a.pos}/*__TRANS_POS.csv'))
jds = {}
for R in races:
    m = meta(R); jds[R] = E._to_jd_ut(E._parse_time(m['race_local_time'], 'Europe/London'))
allT = {R: tpos(R) for R in races}
order = sorted(races, key=lambda R: jds[R])

def tno_rate(R, b):
    i = order.index(R); lo = order[i - 1] if i > 0 else order[i + 1]; hi = order[i + 1] if i < len(order) - 1 else order[i - 1]
    if jds[hi] - jds[lo] < 0.5:  # same day: widen
        lo, hi = order[max(0, i - 3)], order[min(len(order) - 1, i + 3)]
    (r1, d1), (r2, d2) = allT[lo][b], allT[hi][b]; dt = jds[hi] - jds[lo]
    return (((r2 - r1 + 180) % 360) - 180) / dt, (d2 - d1) / dt

H = 30 / 1440
KS = (-30, -2, 0, 2, 30)
for R in races:
    m = meta(R); lat, lon, el = [float(x) for x in m['racecourse_lat_lon_elev'].split(',')]
    jd = jds[R]; T = allT[R]; rows = []
    snaps = [E.bodies_at(jd + k / 1440, lat, lon, el, True) for k in KS]
    for b in T:
        k = b if b in snaps[2] else b + '_B'
        if b in TNOS:
            vr, vd = tno_rate(R, b); ra, dec = T[b]
            rows.append([b] + [v for k in KS for v in ((ra + vr * k / 1440) % 360, dec + vd * k / 1440)] + ['tno-rate'])
            continue
        if k not in snaps[2]:
            sys.exit(f'{R}: {b} not produced by engine')
        s0 = snaps[2][k]
        if abs(((s0['ra'] - T[b][0] + 180) % 360) - 180) > 1e-6 or abs(s0['dec'] - T[b][1]) > 1e-6:
            sys.exit(f'{R}: {b} engine {s0["ra"]:.6f},{s0["dec"]:.6f} != TRANS_POS {T[b]}')
        rows.append([b] + [v for s in snaps for v in (s[k]['ra'], s[k]['dec'])] + ['engine'])
    with open(f'{a.out}/{R}__SKY3.csv', 'w', newline='') as o:
        w = csv.writer(o); w.writerow(['body', 'ra_m30', 'dec_m30', 'ra_m2', 'dec_m2', 'ra_0', 'dec_0', 'ra_p2', 'dec_p2', 'ra_p30', 'dec_p30', 'source']); w.writerows(rows)
print('races', len(races))
