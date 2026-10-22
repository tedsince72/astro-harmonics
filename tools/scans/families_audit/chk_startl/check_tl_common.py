"""check_tl_common.py (independent checker, 22 Oct 2026): own code for the star sources of the runner timelines (S Jup→star,
star→Jup, S Jup on star pair, star apex), written from Eddie's spec only (no import of tools/jupiter_tables.py). families.py for the
targets and scores; the engine (rebuild_kit/celestial_bodies_swisseph.py) for the real exact times."""
import math, os, re, sys
import openpyxl

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path[:0] = [os.path.join(REPO, 'tools'), os.path.join(REPO, 'rebuild_kit'),
                os.path.join(REPO, 'tools', 'scans', 'families_audit', 'chk_stars67')]
import families as F
from check67_common import STARS67

STAR_SRC = ('S Jup→star', 'star→Jup', 'S Jup on star pair', 'star apex')
ALLSTARS = set(STARS67) | {'Polaris'}
FAMNAME = {'whole': 'whole', 'golden': 'golden', 'phi power': 'phi power', 'ninth': 'ninth', 'sqrt2': 'sqrt2', 'silver': 'silver'}
AREANAME = {'A': 'area A', 'P': 'area φ and √2', 'B': 'area B'}


# ---------------------------------------------------------------- positions
def load_positions(wb, runner='P01'):
    sky, ch = {}, {'H': {}, 'J': {}}
    for r in wb['POSITIONS'].iter_rows(values_only=True):
        if not r or r[0] is None or len(r) < 7:
            continue
        if r[0] == 'SKY' and r[2] == 'S' and isinstance(r[5], (int, float)):
            sky[r[3]] = (float(r[5]), float(r[6]), float(r[7] or 0.0), float(r[8] or 0.0))
        elif r[0] == runner and r[2] in ('H', 'J') and isinstance(r[5], (int, float)):
            ch[r[2]][r[3]] = (float(r[5]), float(r[6]))
    return sky, ch


# ---------------------------------------------------------------- geometry
def rawd(a, b, plane):
    """a, b = (ra, dec)"""
    if plane == 'RA':
        d = abs(a[0] - b[0]) % 360.0
        return min(d, 360.0 - d)
    if plane == 'Dec':
        return abs(a[1] - b[1])
    return abs(abs(a[1]) - abs(b[1]))


def wrap180(x):
    return (x + 180.0) % 360.0 - 180.0


def midpoint(C, A, B, plane):
    """C the middle point of A and B -> (hit, total, closeness, offset)"""
    d1, d2 = rawd(C, A, plane), rawd(C, B, plane)
    if max(d1, d2) == 0:
        return False, None, None, None
    clos = min(d1, d2) / max(d1, d2) * 100.0
    if plane == 'RA':
        m1 = A[0] + wrap180(B[0] - A[0]) / 2.0
        o1, o2 = wrap180(C[0] - m1), wrap180(C[0] - (m1 + 180.0))
        off = o1 if abs(o1) <= abs(o2) else o2
        tol = 0.5
    elif plane == 'Dec':
        off, tol = C[1] - (A[1] + B[1]) / 2.0, 0.15
    else:
        off, tol = abs(C[1]) - (abs(A[1]) + abs(B[1])) / 2.0, 0.15
    if clos >= 90.0 and abs(off) <= tol:
        tot = 0.5 * (10 * (10 - (100 - clos)) / 10) ** 2 + 0.5 * (10 * (tol - abs(off)) / tol) ** 2
        return True, tot, clos, off
    return False, None, clos, off


def straddle(pts):
    s = [p[1] > 0 for p in pts]
    return not (all(s) or not any(s))


def fam_plane(plane):
    return plane if plane in ('RA', 'Dec') else None


def digits(lab):
    if re.fullmatch(r'[0-9.]+', lab):
        s = lab.replace('.', '').lstrip('0').rstrip('0')
        return s
    return lab


def dist_target(v, plane):
    b = F.best(v, fam_plane(plane), 'deg')
    if b:
        return b, True
    return F.outside(v, fam_plane(plane), 'deg'), False


def ratio_target(r):
    b = F.best(r, None, 'ratio')
    if b:
        return b, True
    return F.outside(r, None, 'ratio'), False


def target_text(t, hit, kind):
    if kind == 'ratio':
        s = f"{t['target']} · {t['name']} · {t['group']} ({AREANAME[F.area(t['target'])]})"
    else:
        s = f"{t['target']} ({t['family']})"
    return s + ('' if hit else ' — outside')


# ---------------------------------------------------------------- the world: points and motion
class World:
    """points: ('S', name) sky (moving), ('H', name) / ('J', name) natal (fixed)"""

    def __init__(self, sky, ch):
        self.sky, self.ch = sky, ch
        self.eng = None

    def lin(self, p, t):
        if p[0] == 'S':
            ra, dec, rr, rd = self.sky[p[1]]
            return (ra + rr * t, dec + rd * t)
        return self.ch[p[0]][p[1]]

    def realpos(self, p, m):
        if p[0] != 'S':
            return self.ch[p[0]][p[1]]
        ra, dec, _, _ = self.sky[p[1]]
        e = self.eng.at(p[1], m)
        e0 = self.eng.at(p[1], 0.0)
        return (ra + wrap180(e[0] - e0[0]), dec + (e[1] - e0[1]))


def fval(form, get):
    """form: ('d', plane, P, Q) or ('r', plane, apex, num, den)"""
    if form[0] == 'd':
        return rawd(get(form[2]), get(form[3]), form[1])
    _, plane, X, N, D = form
    dn, dd = rawd(get(X), get(N), plane), rawd(get(X), get(D), plane)
    return dn / dd if dd else float('inf')


def lin_t(form, W, target):
    v0 = fval(form, lambda p: W.lin(p, 0.0))
    v5 = fval(form, lambda p: W.lin(p, 5.0))
    rate = (v5 - v0) / 5.0
    if rate == 0:
        return v0, v5, None
    return v0, v5, (target - v0) / rate


def pname(p):
    return f'{p[0]} {p[1]}'


# ---------------------------------------------------------------- events of the four star sources
def key_dist(P, Q, plane, t, W):
    pl = plane
    if plane == 'Equator':
        a, b = W.lin(P, 0), W.lin(Q, 0)
        if (a[1] > 0) == (b[1] > 0):
            pl = 'Dec'
    fam = t['family']
    return ('d', frozenset([P, Q]), pl, fam, 'conj' if fam == 'conj' else digits(t['target']))


def key_ratio(X, A, B, plane, lab):
    return ('r', X, frozenset([A, B]), plane, lab)


def dist_event(src, P, Q, plane, W, only_hit=False):
    v = rawd(W.lin(P, 0), W.lin(Q, 0), plane)
    t, hit = dist_target(v, plane)
    if only_hit and not hit:
        return None
    if t is None:
        return None
    form = ('d', plane, P, Q)
    v0, v5, tl = lin_t(form, W, t['tv'])
    return dict(src=src, rel=f'{pname(P)} → {pname(Q)}', plane=plane, kind='distance', tv=t['tv'], tgt=t, hit=hit, v0=v0,
                score=t['score'] if hit else None, t=tl, form=form, key=key_dist(P, Q, plane, t, W), pts=(P, Q))


def ratio_events(src, X, A, B, plane, W, rel):
    """ratio d(X, A) / d(X, B) larger / smaller, and the midpoint (X the middle point) when a hit"""
    dA, dB = rawd(W.lin(X, 0), W.lin(A, 0), plane), rawd(W.lin(X, 0), W.lin(B, 0), plane)
    out = []
    if min(dA, dB) == 0:
        return out, None, None
    N, D = (A, B) if dA >= dB else (B, A)
    r = max(dA, dB) / min(dA, dB)
    t, hit = ratio_target(r)
    form = ('r', plane, X, N, D)
    v0, v5, tl = lin_t(form, W, t['tv'])
    out.append(dict(src=src, rel=rel, plane=plane, kind='ratio', tv=t['tv'], tgt=t, hit=hit, v0=v0, score=t['score'] if hit else None,
                    t=tl, form=form, key=key_ratio(X, A, B, plane, t['target']), pts=(X, A, B)))
    mh, tot, clos, off = midpoint(W.lin(X, 0), W.lin(A, 0), W.lin(B, 0), plane)
    if mh:
        v0, v5, tl = lin_t(form, W, 1.0)
        out.append(dict(src=src, rel=rel, plane=plane, kind='midpoint', tv=1.0, tgt=None, hit=True, v0=v0, score=tot, t=tl, form=form,
                        key=key_ratio(X, A, B, plane, '1'), pts=(X, A, B), clos=clos, off=off))
    return out, hit, mh


def star_events(W, C, stars):
    """all events of the four star sources for chart C ('H' / 'J'), in source order"""
    SJ, CJ = ('S', 'Jupiter'), (C, 'Jupiter')
    ev = {s: [] for s in STAR_SRC}
    for s in stars:
        for pl in ('RA', 'Dec'):
            e = dist_event('S Jup→star', SJ, (C, s), pl, W)
            if e:
                ev['S Jup→star'].append(e)
    for s in stars:
        for pl in ('RA', 'Dec'):
            e = dist_event('star→Jup', ('S', s), CJ, pl, W)
            if e:
                ev['star→Jup'].append(e)
    kept = 0
    for i, x in enumerate(stars):
        for y in stars[i + 1:]:
            X, Y = (C, x), (C, y)
            for pl in ('RA', 'Dec', 'Equator'):
                pS, pX, pY = W.lin(SJ, 0), W.lin(X, 0), W.lin(Y, 0)
                if pl == 'Equator' and not straddle([pS, pX, pY]):
                    continue
                dxy = rawd(pX, pY, pl)
                if dxy < (1.5 if pl == 'RA' else 0.3):
                    continue
                rel = f'S Jupiter: {pname(X)} – {pname(Y)}'
                rev, rhit, mh = ratio_events('S Jup on star pair', SJ, X, Y, pl, W, rel)
                if not rev:
                    continue
                d1, d2 = rawd(pS, pX, pl), rawd(pS, pY, pl)
                fp = fam_plane(pl)
                three = all(F.best(v, fp, 'deg') for v in (d1, d2, dxy))
                if not (rhit or mh or three):
                    continue
                kept += 1
                ev['S Jup on star pair'] += rev
                for Z in (X, Y):
                    e = dist_event('S Jup on star pair', SJ, Z, pl, W, only_hit=True)
                    if e:
                        ev['S Jup on star pair'].append(e)
    for s in stars:
        ST = ('S', s)
        for pl in ('RA', 'Dec', 'Equator'):
            if pl == 'Equator' and not straddle([W.lin(ST, 0), W.lin(SJ, 0), W.lin(CJ, 0)]):
                continue
            rel = f'{s}: d(star, S Jupiter) / d(star, {C} Jupiter)'
            rev, _, _ = ratio_events('star apex', ST, SJ, CJ, pl, W, rel)
            ev['star apex'] += rev
            e = dist_event('star apex', ST, CJ, pl, W, only_hit=True)
            if e:
                ev['star apex'].append(e)
    return ev, kept


# ---------------------------------------------------------------- reading the sheets
def tl_blocks(ws):
    """-> {block id: [row tuples (values)]} for every timeline block (rows whose col A is the block id)"""
    out = {}
    for r in ws.iter_rows(values_only=True):
        a = r[0] if r else None
        if isinstance(a, str) and re.fullmatch(r'(STAR TIMELINE|LONG TIMELINE|TIMELINE)( [HJ])?', a):
            out.setdefault(a, []).append(tuple(r))
    return out


PT = r'([SHJ]) ([A-Z][A-Za-z ]*?)'


def parse_rel(rel):
    """relationship text -> ('d', P, Q) / ('r', X, A, B) / None; points (chart, name)"""
    m = re.fullmatch(PT + r' → ' + PT, rel)
    if m:
        return ('d', (m[1], m[2]), (m[3], m[4]))
    m = re.fullmatch(PT + r': ' + PT + ' – ' + PT, rel)
    if m:
        return ('r', (m[1], m[2]), (m[3], m[4]), (m[5], m[6]))
    m = re.fullmatch(r'([A-Z][A-Za-z ]*?): d\(star, S Jupiter\) / d\(star, ([HJ]) Jupiter\)', rel)
    if m:
        return ('r', ('S', m[1]), ('S', 'Jupiter'), (m[2], 'Jupiter'))
    return None


def all_points(rel):
    """every point named in a relationship (for the Jupiter-star test); None when not parseable"""
    p = parse_rel(rel)
    if p:
        return [x for x in p[1:]]
    m = re.fullmatch(r'S (\w[\w ]*)–(\w) (\w[\w ]*) / (\w) Jupiter–(\w) (\w[\w ]*)', rel)   # T12 / T13 style
    if m:
        return [('S', m[1]), (m[2], m[3]), (m[4], 'Jupiter'), (m[5], m[6])]
    return None


def row_key(row, W):
    """key of a sheet event row (cols as on the sheet, index 0 = block id)"""
    rel, plane, kind, tgt, tv = row[4], row[5], row[6], row[7], row[8]
    p = parse_rel(rel)
    if p is None:
        return None
    if p[0] == 'd':
        lab, fam = re.fullmatch(r'(.*?) \((.*?)\)( — outside)?', tgt).group(1, 2)
        pl = plane
        if plane == 'Equator':
            a, b = W.lin(p[1], 0), W.lin(p[2], 0)
            if (a[1] > 0) == (b[1] > 0):
                pl = 'Dec'
        fam = {'whole': 'whole'}.get(fam, fam)
        return ('d', frozenset([p[1], p[2]]), pl, fam, 'conj' if fam.startswith('conj') else digits(lab))
    lab = tgt.split(' · ')[0]
    return key_ratio(p[1], p[2], p[3], plane, lab)
