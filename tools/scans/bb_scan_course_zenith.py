"""The racecourse's zenith in the sky's own frame (19 Nov 2026, Eddie: 'what about in RA - the time of the race, the position of the
racecourse on earth relative to the stars'; read-only, chosen after the results).
Zenith at the scheduled off (META race_local_time, Europe/London) = RA of the local meridian (apparent sidereal time + longitude) and Dec =
latitude, on the true equator of date, rotated into J2000 with the engine's own matrix (rebuild_kit date_to_j2000_matrix), so it sits in the
same frame as the workbook positions. (The earlier Dec scan used the plain latitude: about 0.1 deg off in J2000, more than the 0.02 whole
tolerance.) Check: chart_angles at the same jd reproduces the workbook Midheaven.
Lines, scored by eddie_bybody.hits: S Y → zenith (RA wrapped 0-180, Dec |dDec|), Y every sky body (Moon incl.); natal H / J X → zenith.
Groups as bb_scan_course_dec. RA moves 0.25 deg a minute: the real off is usually 1-5 min after the scheduled time, so RA lines at the
whole tolerance (0.02 = 5 s) say little; reported, with that caution. Usage: python3 tools/scans/bb_scan_course_zenith.py"""
import sys, os
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans', 'rebuild_kit']
from datetime import datetime
from zoneinfo import ZoneInfo
import openpyxl, swisseph as swe
import celestial_bodies_swisseph as C, eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe'))


def meta(p):
    m = {}
    for r in openpyxl.load_workbook(p, read_only=True)['META'].iter_rows(values_only=True):
        if r and r[0] in ('racecourse_lat_lon_elev', 'race_local_time'):
            m[r[0]] = str(r[1])
    lat, lon, el = (float(x) for x in m['racecourse_lat_lon_elev'].split(','))
    return lat, lon, el, datetime.strptime(m['race_local_time'][:16], '%Y-%m-%d %H:%M')


def zenith(lat, lon, el, t):
    swe.set_topo(lon, lat, el)
    u = t.replace(tzinfo=ZoneInfo('Europe/London')).astimezone(ZoneInfo('UTC'))
    jd = swe.julday(u.year, u.month, u.day, u.hour + u.minute / 60 + u.second / 3600)
    rot = C.date_to_j2000_matrix(jd)
    ramc = (swe.sidtime(jd) * 15 + lon) % 360
    return C._radec(rot @ C._unit(ramc, lat)), C.chart_angles(jd, lat, lon, rot)['Midheaven']


def ra_d(a, b):
    d = abs(a - b) % 360
    return 360 - d if d > 180 else d


def lines(pos, ra, Z, pts):
    out = []
    for p in pts:
        if p in pos and p in ra:
            for pl, d in (('RA', ra_d(ra[p], Z[0])), ('Dec', abs(pos[p] - Z[1]))):
                h = EB.hits(d, pl)
                if h:
                    out.append((p, pl, round(d, 4), h[0][1], h[0][0], round(h[0][2], 1)))
    return out


def ra_pos(p, tab):
    return {r[0]: float(r[1]) for r in list(openpyxl.load_workbook(p, read_only=True)[tab].iter_rows(values_only=True))[1:]
            if r and r[0] and isinstance(r[1], (int, float))}


RACE = []; G = {'WF': [], 'LF': [], 'OW': [], 'OL': []}; mcchk = []
for race, win in NG.RACES:
    p = f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(p) or race not in F.FAV:
        continue
    lat, lon, el, t = meta(p)
    Z, mc = zenith(lat, lon, el, t)
    runners, tt, tp = EB.load(p)
    tra = ra_pos(p, 'TRANS_POS')
    mcchk.append(ra_d(mc[0], tra.get('Midheaven', mc[0])))
    favwon = F.FAV[race] == win
    RACE.append((race, favwon, Z, lines(tp, tra, Z, EB.BODIES)))
    for cloth, r in runners.items():
        nm = r['name'].get('H', ''); isw = win in nm; isf = F.FAV[race] in nm
        L = []
        for ch in ('H', 'J'):
            L += [(ch,) + x for x in lines(r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {}), Z, EB.NATAL_BODIES)]
        G['WF' if isf and isw else 'LF' if isf else 'OW' if isw else 'OL'].append((race, nm, L))

print('# The racecourse zenith (J2000) against the sky and the natal charts (read-only, chosen after the results)\n')
print(f'Midheaven check: |engine MC − workbook MC| RA max {max(mcchk):.5f} deg over {len(mcchk)} races.\n')
print('## Race level: a sky body on the zenith, races whose favourite won vs lost\n')
print('| plane | cut | favourite won | favourite lost |')
print('|---|---|---|---|')
for pl in ('Dec', 'RA'):
    for cut in (90, 80, 70, 50):
        w = [r for r in RACE if r[1]]; l = [r for r in RACE if not r[1]]
        f = lambda R: sum(1 for r in R if any(x[1] == pl and x[5] >= cut and x[4] != 'conj' for x in r[3]))
        print(f'| {pl} | >= {cut} | {f(w)} / {len(w)} | {f(l)} / {len(l)} |')
print('\n(conjunctions on the zenith counted apart:)')
for pl in ('Dec', 'RA'):
    w = [r for r in RACE if r[1]]; l = [r for r in RACE if not r[1]]
    f = lambda R: sum(1 for r in R if any(x[1] == pl and x[4] == 'conj' for x in r[3]))
    print(f'- {pl} conj: favourite won {f(w)} / {len(w)}, lost {f(l)} / {len(l)}')
print('\n## Runner level: natal H / J X on the zenith >= 90 (number families)\n')
print('| group | runners | Dec mean | RA mean | with any Dec | with any RA |')
print('|---|---|---|---|---|---|')
lab = {'WF': 'winning favourites', 'LF': 'losing favourites', 'OW': 'other winners', 'OL': 'other losers'}
for k, L in G.items():
    n = len(L) or 1
    c = lambda pl: [sum(1 for x in r[2] if x[2] == pl and x[6] >= 90 and x[5] != 'conj') for r in L]
    d, a = c('Dec'), c('RA')
    print(f'| {lab[k]} | {len(L)} | {sum(d)/n:.2f} | {sum(a)/n:.2f} | {sum(1 for x in d if x)} | {sum(1 for x in a if x)} |')
print('\n## Races whose favourite won: every sky body line on the zenith\n')
for race, fw, Z, L in RACE:
    if fw:
        print(f'- {race} zenith RA {Z[0]:.4f} Dec {Z[1]:.4f}: ' + ('; '.join(f'S {y} {pl} {d} {t} {f} ({s})' for y, pl, d, t, f, s in L) or '-'))
