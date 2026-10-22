"""check_sel_common.py (independent checker, 22 Oct 2026): own code for the 95 / 100 / 95 columns of the sky STAR TIMELINE / LONG
STAR TIMELINE and for T24 STAR SELECT, written from Eddie's spec only (no import of tools/jupiter_tables.py). families.py for targets and
scores; the engine (rebuild_kit/celestial_bodies_swisseph.py) for positions over time."""
import math, os, re, sys
import numpy as np
import openpyxl

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path[:0] = [os.path.join(REPO, 'tools'), os.path.join(REPO, 'rebuild_kit')]
import families as F
import swisseph as swe
import celestial_bodies_swisseph as E

swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe'))
BEH = dict(E.BEHENIAN_STARS)
SITES = {'asc': (51.4082, -0.6187, 43.0, swe.julday(2012, 6, 19, 13.5)),      # 14:30 BST
         'lin': (51.1826, -0.0028, 132.0, swe.julday(2021, 4, 2, 13 + 35 / 60))}  # 14:35 BST
BODIES24 = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno',
            'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto', 'Rahu', 'Ketu']


def wrap180(x):
    return (x + 180.0) % 360.0 - 180.0


def rawd(a, b, plane):
    if plane == 'RA':
        d = abs(a[0] - b[0]) % 360.0
        return min(d, 360.0 - d)
    if plane == 'Dec':
        return abs(a[1] - b[1])
    return abs(abs(a[1]) - abs(b[1]))


def load_positions(wb):
    sky, ch = {}, {}
    for r in wb['POSITIONS'].iter_rows(values_only=True):
        if not r or len(r) < 7 or not isinstance(r[5], (int, float)):
            continue
        if r[0] == 'SKY':
            sky[r[3]] = (float(r[5]), float(r[6]))
        else:
            ch.setdefault(r[0], {}).setdefault(r[2], {})[r[3]] = (float(r[5]), float(r[6]))
    return sky, ch


class Eng:
    def __init__(self, race):
        self.lat, self.lon, self.elev, self.jd0 = SITES[race]
        swe.set_topo(self.lon, self.lat, self.elev)
        self.c = {}

    def raw(self, name, m):
        k = (name, round(m, 6))
        if k not in self.c:
            jd = self.jd0 + m / 1440.0
            if name == 'Jupiter':
                r = E._calc('Jupiter', swe.JUPITER, jd)
                self.c[k] = (r[0], r[1])
            else:
                self.c[k] = E._star(name, BEH[name], jd)
        return self.c[k]


class Sky:
    def __init__(self, sky, eng):
        self.sky, self.eng = sky, eng

    def at(self, name, m):
        ra, dec = self.sky[name]
        if m == 0:
            return (ra, dec)
        e, e0 = self.eng.raw(name, m), self.eng.raw(name, 0.0)
        return (ra + wrap180(e[0] - e0[0]), dec + (e[1] - e0[1]))


# ---------------------------------------------------------------- scores
def fam_of(lab):
    return lab


def dist_score(v, plane, fam, lab):
    pl = plane if plane in ('RA', 'Dec') else None
    for d in F.evaluate(v, pl, 'deg'):
        if d['family'] == fam and d['target'] == lab:
            return d['score']
    return 0.0


def interval_score(r, lab):
    t = F.INTERVAL_BY_LABEL[lab][1]
    tol = F.TOL[lab]
    dev = abs(r - t) if lab in F.AREA_A else abs(r / t - 1) * 100
    return (10 * (tol - dev) / tol) ** 2 if dev < tol else 0.0


def mid_total(C, A, B, plane, side=None):
    """C the middle point of A, B; side fixed ('near' / 'far') for RA -> (total or 0, side)"""
    d1, d2 = rawd(C, A, plane), rawd(C, B, plane)
    if max(d1, d2) == 0:
        return 0.0, side
    clos = min(d1, d2) / max(d1, d2) * 100
    if plane == 'RA':
        m1 = A[0] + wrap180(B[0] - A[0]) / 2
        o1, o2 = wrap180(C[0] - m1), wrap180(C[0] - (m1 + 180))
        if side is None:
            side = 'near' if abs(o1) <= abs(o2) else 'far'
        off, tol = (o1 if side == 'near' else o2), 0.5
    elif plane == 'Dec':
        off, tol = C[1] - (A[1] + B[1]) / 2, 0.15
    else:
        off, tol = abs(C[1]) - (abs(A[1]) + abs(B[1])) / 2, 0.15
    if clos >= 90 and abs(off) <= tol:
        return 0.5 * (10 * (10 - (100 - clos)) / 10) ** 2 + 0.5 * (10 * (tol - abs(off)) / tol) ** 2, side
    return 0.0, side


# ---------------------------------------------------------------- events from sheet rows
def parse_target(kind, tgt):
    if kind == 'distance':
        m = re.fullmatch(r'(.*?) \((.*?)\)( — outside)?', tgt)
        lab, fam = m[1], m[2]
        if fam.startswith('conj'):
            fam, lab = 'conj', 'conj'
        return fam, lab
    return 'interval', tgt.split(' · ')[0]


def make_scorer(row, sk):
    """row: (rel, plane, kind, target) -> f(m) = score at m minutes from the off; None if not a S Jupiter event"""
    rel, plane, kind, tgt = row
    m1 = re.fullmatch(r'S Jupiter → S (.+)', rel)
    m2 = re.fullmatch(r'S Jupiter: S (.+?) – S (.+)', rel)
    fam, lab = parse_target(kind, tgt)
    if m1 and kind == 'distance':
        X = m1[1]
        return lambda m: dist_score(rawd(sk.at('Jupiter', m), sk.at(X, m), plane), plane, fam, lab)
    if m2:
        A, B = m2[1], m2[2]
        J0, A0, B0 = sk.at('Jupiter', 0), sk.at(A, 0), sk.at(B, 0)
        if kind == 'ratio':
            dA, dB = rawd(J0, A0, plane), rawd(J0, B0, plane)
            N, D = (A, B) if dA >= dB else (B, A)

            def f(m):
                J = sk.at('Jupiter', m)
                return interval_score(rawd(J, sk.at(N, m), plane) / rawd(J, sk.at(D, m), plane), lab)
            return f
        if kind == 'midpoint':
            _, side = mid_total(J0, A0, B0, plane)
            return lambda m: mid_total(sk.at('Jupiter', m), sk.at(A, m), sk.at(B, m), plane, side)[0]
    return None


STEPS = [(1.0, 60.0), (10.0, 1440.0), (60.0, 525600.0)]


def cross(f, m0, direction, thr=95.0):
    """first time from m0 going `direction` where f < thr -> bisected crossing (min) or None within 1 year"""
    prev = m0
    fp = f(prev) - thr
    if fp < 0:
        return 'under'
    m = m0
    for step, lim in STEPS:
        while abs(m - m0) < lim:
            m = m + direction * step
            fm = f(m) - thr
            if fm < 0:
                a, b = prev, m
                for _ in range(40):
                    c = (a + b) / 2
                    if f(c) - thr >= 0:
                        a = c
                    else:
                        b = c
                    if abs(b - a) < 0.005:
                        break
                return (a + b) / 2
            prev = m
    return None


def fmt_rel(m, jd_off_local_str):
    """not used: the sheet text is parsed instead"""
    return None


OFF = {'asc': (2012, 6, 19, 14, 30), 'lin': (2021, 4, 2, 14, 35)}


def clock_min(s, race):
    """minutes from the off of the clock text ('hh:mm' on race day or 'dd Mon yyyy hh:mm'), to the minute"""
    import datetime as dt
    y, mo, d, h, mi = OFF[race]
    off = dt.datetime(y, mo, d, h, mi)
    m = re.match(r'(\d\d \w\w\w \d{4} )?(\d\d):(\d\d)', s)
    if not m:
        return None
    day = dt.datetime.strptime(m[1].strip(), '%d %b %Y') if m[1] else dt.datetime(y, mo, d)
    t = day.replace(hour=int(m[2]), minute=int(m[3]))
    return (t - off).total_seconds() / 60.0


def parse_cell_min(s, off_dt):
    """'hh:mm (±n.n min)' or 'dd Mon yyyy hh:mm (±n.nn days)' -> minutes from the off"""
    m = re.search(r'\(([+-]?[0-9.]+) min\)', s)
    if m:
        return float(m[1])
    m = re.search(r'\(([+-]?[0-9.]+) days\)', s)
    if m:
        return float(m[1]) * 1440.0
    return None
