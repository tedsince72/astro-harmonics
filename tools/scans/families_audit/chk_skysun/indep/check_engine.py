#!/usr/bin/env python3
"""check_engine.py <workbook> <batch.xlsx> [sheet ...]: LONG / LONG STAR real exact times (beyond 60 min) and the 95 / 100 / 95 cells of
STAR TIMELINE / LONG STAR TIMELINE, re-searched with the race engine (own search; sky at m = workbook value at the off + engine(m) -
engine(off)). Own score code on each event's own target (family / interval tolerance; midpoint total)."""
import sys, os, re, math, functools, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *  # noqa
import check_blocks as CB
sys.path.insert(0, os.path.expanduser('~/astro-harmonics/rebuild_kit'))
import celestial_bodies_swisseph as E  # noqa
import swisseph as swe, pytz  # noqa

swe.set_ephe_path(E.EPHE_PATH)
PHI = (1 + 5 ** 0.5) / 2


class Eng:
    def __init__(self, pos, batch):
        wb = openpyxl.load_workbook(batch, read_only=True)
        meta = {r[0]: r[1] for r in wb['META'].iter_rows(values_only=True) if r and r[0]}
        self.lat, self.lon, self.elev = [float(x) for x in meta['racecourse_lat_lon_elev'].split(',')]
        off = pytz.timezone('Europe/London').localize(pos.off)
        self.jd0 = E._to_jd_ut(off)
        self.pos = pos
        self.base = self.at(0.0)

    @functools.lru_cache(maxsize=200000)
    def at(self, m):
        b = E.bodies_at(self.jd0 + m / 1440.0, self.lat, self.lon, self.elev, False)
        return b

    def pt(self, nm, m):
        if nm == 'equator':
            return (0.0, 0.0)
        k = nm if nm in self.base else nm + '_B'
        b = self.at(round(m, 6)); b0 = self.base
        ra0, dec0 = self.pos.p[nm][0], self.pos.p[nm][1]
        dra = ((b[k]['ra'] - b0[k]['ra'] + 540) % 360) - 180
        return ((ra0 + dra) % 360, dec0 + b[k]['dec'] - b0[k]['dec'])


def d_plane(p1, p2, plane):
    if plane == 'RA':
        x = abs(p1[0] - p2[0]) % 360
        return 360 - x if x > 180 else x
    if plane == 'Dec':
        return abs(p1[1] - p2[1])
    return abs(abs(p1[1]) - abs(p2[1]))


def fam_of(target):
    m = re.search(r'\((whole|golden|phi power|ninth|sqrt2|silver)\)', target)
    return m.group(1) if m else None


def dist_score(v, fam, tv):
    dev = abs(v - tv)
    if fam in F.DIGIT_FAMILIES and not F.digit_match(v, tv):     # the 4-digit rule (families.py)
        return 0.0
    if fam == 'whole': tol = 0.02
    elif fam == 'golden': tol = 0.03236
    elif fam == 'ninth':
        tol = next(t for lo, hi, t, x in F._NINTH_RANGES if abs(x - tv) < 1e-6)
        return max(0.0, 100 * (tol - dev) / tol)
    else: tol = max(tv * 0.005, 0.025)
    return (10 * (tol - dev) / tol) ** 2 if dev < tol else 0.0


def ratio_score(q, lab):
    t = F.INTERVAL_BY_LABEL[lab][1]
    tol = F.TOL[lab]
    dev = abs(q - t) if lab in F.AREA_A else abs(q / t - 1) * 100
    return (10 * (tol - dev) / tol) ** 2 if dev < tol else 0.0


def make_event(eng, row, centre):
    rel, plane, kind, target, tv = row[4], row[5], row[6], row[7], float(row[8])
    m = re.match(r'S (.+) → S (.+)$', rel)
    if m:
        a, b = m.group(1), m.group(2)
        pl = 'Dec' if b == 'equator' else plane
        f = lambda t: d_plane(eng.pt(a, t), eng.pt(b, t), pl)
        fam = fam_of(target)
        return f, tv, (lambda t: dist_score(f(t), fam, tv))
    m = re.match(r'S (.+): S (.+) (?:–|=) S (.+)$', rel)
    if m:
        c, x, y = m.groups()
        d1 = lambda t: d_plane(eng.pt(c, t), eng.pt(x, t), plane)
        d2 = lambda t: d_plane(eng.pt(c, t), eng.pt(y, t), plane)
        big1 = d1(0) >= d2(0)
        q = (lambda t: d1(t) / d2(t)) if big1 else (lambda t: d2(t) / d1(t))
        if kind == 'ratio':
            lab = target.split(' · ')[0]
            return q, tv, (lambda t: ratio_score(q(t), lab))
        # midpoint: RA side fixed at the off
        tol = TOLMID[plane]
        def offset(t, side=[None]):
            pc, px, py = eng.pt(c, t), eng.pt(x, t), eng.pt(y, t)
            if plane == 'RA':
                diff = ((py[0] - px[0] + 540) % 360) - 180
                near = (px[0] + diff / 2) % 360
                o1 = ((pc[0] - near + 540) % 360) - 180
                o2 = ((pc[0] - near - 180 + 540) % 360) - 180
                if side[0] is None:
                    side[0] = 'n' if abs(o1) <= abs(o2) else 'f'
                return o1 if side[0] == 'n' else o2
            if plane == 'Dec':
                return pc[1] - (px[1] + py[1]) / 2
            return abs(pc[1]) - (abs(px[1]) + abs(py[1])) / 2
        offset(0)
        def tot(t):
            a, b = d1(t), d2(t)
            cl = min(a, b) / max(a, b) * 100
            o = offset(t)
            if cl < 90 or abs(o) >= tol: return 0.0
            return (cl - 90) ** 2 * 0.5 + (10 * (tol - abs(o)) / tol) ** 2 * 0.5
        return q, 1.0, tot
    m = re.match(r'S (.+) – S (.+)$', rel)
    a, b = m.groups()
    f = lambda t: d_plane(eng.pt(a, t), eng.pt(b, t), plane)
    fam = fam_of(target)
    return f, tv, (lambda t: dist_score(f(t), fam, tv))


def cross95(sc, ex, sgn):
    """own search: from the exact time step outward (0.5 min for a day, 10 min to 30 days, 1 h to a year), bisect to 0.01 min"""
    if sc(ex) < 95:
        return 'dash'
    t = ex
    while True:
        st = 0.5 if abs(t - ex) < 1440 else 10 if abs(t - ex) < 43200 else 60
        nt = t + sgn * st
        if abs(nt - ex) > 366 * 1440:
            return None
        if sc(nt) < 95:
            a, b = t, nt
            while abs(b - a) > 0.01:
                m = (a + b) / 2
                if sc(m) >= 95: a = m
                else: b = m
            return (a + b) / 2
        t = nt


def parse_m(s):
    if s in (None, '', '—') or 'not within' in str(s):
        return None, None
    m = re.search(r'\(([+-][\d.]+) (min|days)\)', s)
    v = float(m.group(1))
    return (v, 1.0) if m.group(2) == 'min' else (v * 1440, 0.01 * 1440 + 1)


def run(path, batch, sheets):
    wb = openpyxl.load_workbook(path)
    pos = Pos(wb)
    eng = Eng(pos, batch)
    for sn in sheets:
        ws = wb[sn]; centre = sn.split()[-1].capitalize()
        n_real = n_95 = 0; errs = []; nw = 0
        for name, c95 in (('LONG TIMELINE', None), ('LONG STAR TIMELINE', 15), ('STAR TIMELINE', 13)):
            for r in range(1, ws.max_row + 1):
                if ws.cell(r, 1).value != name: continue
                row = [ws.cell(r, k).value for k in range(1, 20)]
                if isinstance(row[3], str) and row[3].startswith('———'): continue
                f, tv, sc = make_event(eng, row, centre)
                if name.startswith('LONG'):
                    mm = CB.num(row[13])
                    if row[1] in (None, '') or 'not within' in str(row[1]) or 'not within' in str(row[2]):
                        nw += 1; continue
                    if abs(mm) > 60:
                        n_real += 1
                        w = 1.0 if abs(mm) < 1440 else 1.0
                        a, b = f(mm - w) - tv, f(mm + w) - tv
                        if a * b > 0:
                            errs.append((name, row[4], row[5], 'real time', mm, a, b))
                if c95 is not None:
                    since, ex, until = row[c95], row[c95 + 1], row[c95 + 2]
                    ex_m = CB.num(row[13]) if name.startswith('LONG') else CB.num(row[2])
                    for kind, cell in (('since', since), ('until', until)):
                        mine = cross95(sc, ex_m, -1 if kind == 'since' else 1)
                        v, w = parse_m(cell)
                        n_95 += 1
                        if v is None:
                            want = '—' if mine == 'dash' else 'not within 1 year' if mine is None else 'time'
                            gotk = '—' if cell == '—' else 'not within 1 year' if 'not within' in str(cell) else cell
                            if want != gotk: errs.append((name, row[4], row[5], kind, cell, mine))
                            continue
                        if not isinstance(mine, float) or abs(mine - v) > (0.6 if w == 1.0 else 16):
                            errs.append((name, row[4], row[5], kind, cell, mine if not isinstance(mine, float) else round(mine, 2)))
        print(sn, f'real times checked {n_real}, not-within-1-year rows {nw}, 95-cells checked {n_95}, errors {len(errs)}')
        for e in errs[:20]: print('   ', e)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3:])
