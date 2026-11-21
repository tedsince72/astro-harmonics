"""Race-day type calendar from the sky (21 Nov 2026, Eddie's go-ahead; data only, no pick).

Every day of a date range, the sky at 12:00, 14:00, 16:00, 18:00 and 20:00 UK local time (Europe/London, summer time
as on the clock), from the race engine rebuild_kit/celestial_bodies_swisseph.py: J2000 equatorial, apparent, topocentric
- the same frame as the race files' TRANS_POS sheet. One fixed UK site (default 52.5 N, 1.5 W, 100 m; --site);
the Moon's parallax moves it up to about 0.1 deg between UK courses, everything else far less.

Bodies: Sun, Moon, Mercury ... Pluto, Rahu (true node), Ketu, Chiron, Ceres, Pallas, Juno, Vesta, Eris, Haumea, Makemake,
Gonggong, Quaoar, Sedna, Orcus, Transpluto. Royal stars: Aldebaran, Regulus, Antares, Fomalhaut.

Contacts (each body with each royal star, separately; orb 0.50 deg, --orb):
  RA conj    circular RA difference <= orb
  parallel   |Dec body - Dec star| <= orb
  contra     |Dec body + Dec star| <= orb
A body (not the Moon) in contact = a ruling body; its star = a ruling star. Rahu and Ketu count as ONE body (the nodes),
so a node day is one body. The Moon is never a ruling body: it has its own flags (Claude's choice).

Day type, from the 15:00 sky, first that applies (Claude's order, agreed with Eddie 21 Nov 2026):
  5 EMPTY        no ruling body
  6 CROWDED      three or more ruling bodies
  3 TWO STARS    ruling bodies on two or more royal stars
  4 NODE         the only ruling body is the nodes
  7 SUN          the only ruling body is the Sun
  1 FAST         only Mercury, Venus, Mars (with or without the Sun), one star
  2 SLOW         only slow bodies (Jupiter outward, asteroids, TNOs, Transpluto; nodes allowed with them), one star
  8 MIXED        fast and slow bodies on one star (needed: the instruction had no type for it)
Sun ruling = yes/no beside the type (any type).

Moon flags, at each of the five times, against the 15:00 ruling stars: MOON_ON_RULING_STAR = yes when the Moon has a
contact (as above) with a ruling star, or its RA or Dec distance to a ruling star is on a golden or ninth number
(tools/families.py: golden +-0.0324 and the 48 ninth ranges, 4-digit rule) - Eddie's families, not the +-0.015 / +-0.02
of the first instruction. The cell names what it is ('Regulus Dec 33.3333 ninth (71.2)').

Trend: each 15:00 ruling contact's orb at 12:00 and 20:00 -> narrowing / widening (orb measured at every time even
beyond the 0.50).

Check first (--check FILE ..., default the three files of 21 Nov 2026): the engine is run at each file's race time and
site (META) and compared with its TRANS_POS sheet (every body here, RA and Dec, within 0.001 deg), and the contacts
within the orb must be the same with orbs within 0.01. Any difference -> stops before the calendar.

Outputs (default docs/eddie_read/sky_calendar/): sky_calendar_<from>_<to>.csv (one row a day) and
sky_calendar_<from>_<to>_summary.md (days per type per year; runs of 3+ days in a row).

  python3 tools/scans/sky_day_calendar.py [--from 2020-01-01] [--to 2026-12-31] [--ephe DIR] [--site LAT LON ELEV]
         [--orb 0.5] [--check FILE ...] [--check-only] [--skip-tnos] [--out DIR]
(--skip-tnos only for testing where the TNO ephemeris files are missing; the real run needs them.)
"""
import sys, os, csv, argparse
from datetime import date, datetime, timedelta
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [os.path.join(ROOT, 'rebuild_kit'), os.path.join(ROOT, 'tools')]
import pytz
import swisseph as swe
import celestial_bodies_swisseph as E
import families as FAM

UK = pytz.timezone('Europe/London')
TIMES = (12, 14, 16, 18, 20)
TYPE_TIME = 15
ROYAL = ['Aldebaran', 'Regulus', 'Antares', 'Fomalhaut']
FAST = ('Mercury', 'Venus', 'Mars')
NODES = ('Rahu', 'Ketu')
TYPES = {5: 'EMPTY', 6: 'CROWDED', 3: 'TWO STARS', 4: 'NODE', 7: 'SUN', 1: 'FAST', 2: 'SLOW', 8: 'MIXED'}
DEFAULT_CHECKS = [os.path.join(ROOT, 'reference', 'classic', f) for f in (
    'race_batch_20200918_catterick_1455_active.xlsx', 'race_batch_20261023_cheltenham_1500_active.xlsx',
    'race_batch_20261120_ascot_1540_active.xlsx')]


class Sky:
    def __init__(self, lat, lon, elev, skip_tnos=False):
        self.site = (lat, lon, elev)
        self.skip = skip_tnos

    def at(self, jd, site=None):
        lat, lon, elev = site or self.site
        swe.set_topo(lon, lat, elev)
        out = {}
        for n, bid in E._SWE_PLANETS.items():
            ra, dec, _ = E._calc(n, bid, jd)
            out[n] = (ra, dec)
        out['Ketu'] = ((out['Rahu'][0] + 180.0) % 360.0, -out['Rahu'][1])
        for n, bid in E._SWE_ASTEROIDS.items():
            ra, dec, _ = E._calc(n, bid, jd)
            out[n] = (ra, dec)
        if not self.skip:
            for n, num in E._SWE_TNOS.items():
                ra, dec, _ = E._calc(n, swe.AST_OFFSET + num, jd)
                out[n] = (ra, dec)
        ra, dec, _, _ = E.transpluto(jd, E.date_to_j2000_matrix(jd))
        out['Transpluto'] = (ra, dec)
        for s in ROYAL:
            out[s] = E._star(s, s, jd)
        return out


def ra_diff(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def contacts(p, orb, bodies=None):
    """[(body, star, kind, orb)] for every body (not a royal star) with each royal star."""
    out = []
    for b, (ra, dec) in p.items():
        if b in ROYAL or (bodies and b not in bodies):
            continue
        for s in ROYAL:
            sra, sdec = p[s]
            for kind, v in (('RA conj', ra_diff(ra, sra)), ('parallel', abs(dec - sdec)), ('contra', abs(dec + sdec))):
                if v <= orb:
                    out.append((b, s, kind, v))
    return out


def orb_of(p, b, s, kind):
    ra, dec = p[b]
    sra, sdec = p[s]
    return {'RA conj': ra_diff(ra, sra), 'parallel': abs(dec - sdec), 'contra': abs(dec + sdec)}[kind]


def classify(cs):
    rule = [c for c in cs if c[0] != 'Moon']
    bodies = {('Nodes' if b in NODES else b) for b, *_ in rule}
    stars = {s for _, s, *_ in rule}
    sun = 'Sun' in bodies
    if not bodies:
        t = 5
    elif len(bodies) >= 3:
        t = 6
    elif len(stars) >= 2:
        t = 3
    elif bodies == {'Nodes'}:
        t = 4
    elif bodies == {'Sun'}:
        t = 7
    else:
        rest = bodies - {'Sun'}
        fast = rest & set(FAST)
        slow = rest - set(FAST)
        t = 1 if fast and not slow else 2 if slow and not fast else 8
    return t, sorted(bodies), sorted(stars), sun


def moon_flag(p, stars, orb):
    hits = []
    mra, mdec = p['Moon']
    for s in stars:
        sra, sdec = p[s]
        for kind, v in (('RA conj', ra_diff(mra, sra)), ('parallel', abs(mdec - sdec)), ('contra', abs(mdec + sdec))):
            if v <= orb:
                hits.append(f'{s} {kind} {v:.3f}')
        for pl, v in (('RA', ra_diff(mra, sra)), ('Dec', abs(mdec - sdec))):
            for h in FAM.evaluate(v, pl):
                if h['family'] in ('golden', 'ninth') and h['score'] > 0:
                    hits.append(f'{s} {pl} {v:.4f} {h["target"]} {h["family"]} ({h["score"]:.1f})')
    return hits


def jd_local(d, hour, minute=0):
    return E._to_jd_ut(UK.localize(datetime(d.year, d.month, d.day, hour, minute)))


# ── check against race files ──────────────────────────────────────────────────

def check(sky, files, orb):
    import openpyxl
    ok = True
    for f in files:
        if not os.path.exists(f):
            print(f'CHECK  missing file: {f}'); ok = False; continue
        wb = openpyxl.load_workbook(f, read_only=True)
        meta = {r[0]: r[1] for r in wb['META'].iter_rows(values_only=True) if r and isinstance(r[0], str)}
        t = UK.localize(datetime.strptime(meta['race_local_time'], '%Y-%m-%d %H:%M'))
        lat, lon, elev = (float(x) for x in meta['racecourse_lat_lon_elev'].split(','))
        rows = [r for r in list(wb['TRANS_POS'].iter_rows(values_only=True))[1:] if r and r[0]]
        tp = {r[0]: (float(r[1]) if isinstance(r[1], (int, float)) else None, float(r[2])) for r in rows
              if isinstance(r[2], (int, float))}
        p = sky.at(E._to_jd_ut(t), (lat, lon, elev))
        worst = (0.0, '')
        for b, (ra, dec) in p.items():
            if b not in tp:
                print(f'CHECK  {os.path.basename(f)}: {b} not in TRANS_POS'); ok = False; continue
            tra, tdec = tp[b]
            for lab, dv in (('RA', ra_diff(ra, tra) if tra is not None else 0.0), ('Dec', abs(dec - tdec))):
                if dv > worst[0]:
                    worst = (dv, f'{b} {lab}')
        mine = {(b, s, k): v for b, s, k, v in contacts(p, orb)}
        tps = {b: v for b, v in tp.items() if b in p}
        theirs = {(b, s, k): v for b, s, k, v in contacts(tps, orb)}
        same = set(mine) == set(theirs) and all(abs(mine[k] - theirs[k]) <= 0.01 for k in mine)
        good = worst[0] <= 0.001 and same
        ok &= good
        print(f'CHECK  {os.path.basename(f)} ({meta["race_local_time"]}): largest position difference {worst[0]:.6f} '
              f'({worst[1]}); contacts {"same" if same else "DIFFERENT"}: '
              + '; '.join(f'{b} {k} {s} {v:.3f}' for (b, s, k), v in sorted(mine.items(), key=lambda x: x[1]))
              + ('' if same else '  | race file: ' + '; '.join(f'{b} {k} {s} {v:.3f}' for (b, s, k), v in theirs.items()))
              + ('  OK' if good else '  FAILED'))
    return ok


# ── calendar ──────────────────────────────────────────────────────────────────

def run(sky, d0, d1, orb, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    tag = f'{d0:%Y%m%d}_{d1:%Y%m%d}'
    csv_path = os.path.join(out_dir, f'sky_calendar_{tag}.csv')
    head = (['date', 'day_type', 'type_name', 'ruling_contacts_1500', 'n_ruling_bodies', 'n_ruling_stars', 'ruling_stars',
             'sun_ruling'] + [f'moon_{h:02d}' for h in TIMES] + [f'moon_{h:02d}_detail' for h in TIMES] + ['orb_trend_12_20'])
    days = []
    with open(csv_path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(head)
        d = d0
        while d <= d1:
            p15 = sky.at(jd_local(d, TYPE_TIME))
            cs = sorted(contacts(p15, orb), key=lambda c: c[3])
            t, bodies, stars, sun = classify(cs)
            pt = {h: sky.at(jd_local(d, h)) for h in TIMES}
            mflags = {h: moon_flag(pt[h], stars, orb) for h in TIMES}
            trend = []
            for b, s, k, v in cs:
                if b == 'Moon':
                    continue
                a, z = orb_of(pt[12], b, s, k), orb_of(pt[20], b, s, k)
                trend.append(f'{b} {k} {s} {a:.3f}>{z:.3f} {"narrowing" if z < a else "widening"}')
            rc = '; '.join(f'{b} {k} {s} {v:.3f}' for b, s, k, v in cs if b != 'Moon')
            w.writerow([d.isoformat(), t, TYPES[t], rc, len(bodies), len(stars), ', '.join(stars), 'yes' if sun else 'no']
                       + ['yes' if mflags[h] else 'no' for h in TIMES] + ['; '.join(mflags[h]) for h in TIMES]
                       + ['; '.join(trend)])
            days.append((d, t))
            d += timedelta(days=1)
    summary(days, os.path.join(out_dir, f'sky_calendar_{tag}_summary.md'), d0, d1, orb)
    return csv_path


def summary(days, path, d0, d1, orb):
    years = sorted({d.year for d, _ in days})
    cnt = Counter((d.year, t) for d, t in days)
    runs, cur = [], None
    for d, t in days:
        if cur and cur[0] == t and (d - cur[2]).days == 1:
            cur[2] = d
        else:
            if cur:
                runs.append(tuple(cur))
            cur = [t, d, d]
    if cur:
        runs.append(tuple(cur))
    with open(path, 'w') as fh:
        fh.write(f'# Race-day type calendar {d0} to {d1} (sky at 15:00 UK time, orb {orb})\n\n')
        fh.write('Days per type per year.\n\n| type | ' + ' | '.join(map(str, years)) + ' | all |\n|---|'
                 + '---|' * (len(years) + 1) + '\n')
        for t, name in TYPES.items():
            fh.write(f'| {t} {name} | ' + ' | '.join(str(cnt[(y, t)]) for y in years)
                     + f' | {sum(cnt[(y, t)] for y in years)} |\n')
        fh.write('\nRuns of 3 or more days of the same type (start - end, days).\n\n')
        for t, name in TYPES.items():
            rr = [r for r in runs if r[0] == t and (r[2] - r[1]).days >= 2]
            fh.write(f'- {t} {name}: ' + (', '.join(f'{a} - {b} ({(b - a).days + 1})' for _, a, b in rr) or 'none') + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from', dest='d0', default='2020-01-01')
    ap.add_argument('--to', dest='d1', default='2026-12-31')
    ap.add_argument('--ephe', default=E.EPHE_PATH)
    ap.add_argument('--site', nargs=3, type=float, default=(52.5, -1.5, 100.0))
    ap.add_argument('--orb', type=float, default=0.5)
    ap.add_argument('--check', nargs='*', default=DEFAULT_CHECKS)
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--skip-tnos', action='store_true')
    ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'eddie_read', 'sky_calendar'))
    a = ap.parse_args()
    swe.set_ephe_path(os.path.abspath(os.path.expanduser(a.ephe)))
    sky = Sky(*a.site, skip_tnos=a.skip_tnos)
    if a.check:
        if not check(sky, a.check, a.orb):
            print('STOPPED: the check against the race files failed (see above).')
            return 1
    if a.check_only:
        return 0
    path = run(sky, date.fromisoformat(a.d0), date.fromisoformat(a.d1), a.orb, a.out)
    print(f'calendar -> {path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
