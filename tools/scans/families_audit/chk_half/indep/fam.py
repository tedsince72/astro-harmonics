"""Independent family scoring for the half family + 4-digit rule check (Eddie, 24 Oct 2026).
Own code: does NOT import tools/families.py or tools/jupiter_tables.py. Only the raw _NINTH_RANGES data table is read from
rebuild_kit/active_vibrations.py (Eddie's source of the 48 ranges).
new=True: half family + 4-digit rule; new=False: the old rules (no half, no digit rule) for the before workbooks."""
import math, os, re
from decimal import Decimal

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[os.pardir] * 5))
_src = open(os.path.join(ROOT, 'rebuild_kit', 'active_vibrations.py')).read()
_blk = _src[_src.index('_NINTH_RANGES = ['):]
_blk = _blk[:_blk.index('\n]')]
NINTHS = [tuple(float(x) for x in m) for m in re.findall(r'\(\s*([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)', _blk)]
assert len(NINTHS) == 48, len(NINTHS)

PHI = (1 + 5 ** 0.5) / 2
R2 = 2 ** 0.5
SIL = 1 + R2
PP = []                                   # (label, value)
for p in [-1] + list(range(1, 11)):
    PP.append((f'φ^{p}', PHI ** p))
for p in [-1] + list(range(1, 8)):
    PP.append((f'10×φ^{p}', 10 * PHI ** p))
for p in (-1, 1):
    PP.append((f'100×φ^{p}', 100 * PHI ** p))
SQ = [('1.414', R2), ('14.14', 10 * R2), ('141.4', 100 * R2), ('0.707', R2 / 2), ('7.07', 5 * R2), ('70.7', 50 * R2)]
SV = [('2.414', SIL), ('24.14', 10 * SIL), ('0.414', SIL - 2), ('4.14', 10 * (SIL - 2)), ('41.4', 100 * (SIL - 2))]
CONJ = {'RA': 1.5, 'Dec': 0.3}
ORDER = ['whole', 'half', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver', 'conj']
DIGIT = {'golden', 'phi power', 'ninth', 'sqrt2', 'silver'}


def d4(x):
    """(order of magnitude, first 4 significant digits truncated) via a 12-significant-digit decimal string (guards float error)"""
    s = f'{x:.11e}'                       # d.ddddddddddde±XX
    mant, ex = s.split('e')
    digs = mant.replace('.', '')
    return int(ex), int(digs[:4])


def dmatch(v, t):
    return v > 0 and t > 0 and d4(v) == d4(t)


def sq(tol, dev):
    return (10.0 * (tol - dev) / tol) ** 2


def fams(v, plane, new=True):
    """every family scoring > 0: list of (score, family, label, target), best first (ties in ORDER)"""
    out = []
    if v is None:
        return out
    if v > 0:
        # whole
        if 1 <= v <= 200:
            t = round(v)
            if abs(v - t) < 0.02:
                out.append((sq(0.02, abs(v - t)), 'whole', str(int(t)), float(t)))
        if new:
            t = math.floor(v) + 0.5
            if 0.5 <= t <= 199.5 and abs(v - t) < 0.01:
                out.append((sq(0.01, abs(v - t)), 'half', f'{t:g}', t))
        k = round(v / PHI)
        if k >= 1:
            t = k * PHI
            if abs(v - t) < 0.03236 and (not new or dmatch(v, t)):
                out.append((sq(0.03236, abs(v - t)), 'golden', f'{k}×φ', t))
        for fam, lst in (('phi power', PP), ('sqrt2', SQ), ('silver', SV)):
            best = None
            for lab, t in lst:
                tol = max(0.005 * t, 0.025)
                if abs(v - t) <= tol and (not new or dmatch(v, t)):
                    s = sq(tol, abs(v - t))
                    if s > 0 and (best is None or s > best[0]):
                        best = (s, fam, lab, t)
            if best:
                out.append(best)
        for lo, hi, tol, t in NINTHS:
            if lo <= v < hi:
                s = max(0.0, 100.0 * (tol - abs(v - t)) / tol)
                if s > 0 and (not new or dmatch(v, t)):
                    out.append((s, 'ninth', f'{t:g}', t))
                break
    if plane in CONJ and v is not None and v < CONJ[plane]:
        out.append((sq(CONJ[plane], v), 'conj', 'conj', 0.0))
    out = [o for o in out if o[0] > 0]
    out.sort(key=lambda o: (-o[0], ORDER.index(o[1])))
    return out


def outside(v, new=True):
    """nearest target by tightness -> (family, label, target, tol)"""
    if v is None or v <= 0:
        return None
    c = []
    if round(v) > 0:
        c.append(('whole', str(int(round(v))), float(round(v)), 0.02))
    k = round(v / PHI)
    if k >= 1:
        c.append(('golden', f'{k}×φ', k * PHI, 0.03236))
    if new:
        h = math.floor(v) + 0.5
        if 0.5 <= h <= 199.5:
            c.append(('half', f'{h:g}', h, 0.01))
    c += [('phi power', lab, t, max(0.005 * t, 0.025)) for lab, t in PP]
    c += [('ninth', f'{t:g}', t, tol) for lo, hi, tol, t in NINTHS]
    c += [('sqrt2', lab, t, max(0.005 * t, 0.025)) for lab, t in SQ]
    c += [('silver', lab, t, max(0.005 * t, 0.025)) for lab, t in SV]
    return min(c, key=lambda z: abs(v - z[2]) / z[3])


def colour(s):
    return 'green' if s >= 80 else 'yellow' if s >= 50 else 'light' if s > 0 else ''


FILLHEX = {'green': '00C6EFCE', 'yellow': '00FFEB9C', 'light': '00FFF8DC', '': None, 'red': '00FF8080'}


def offs(x):
    return f'{x:+.5f}'


def target_text(v, plane, new=True):
    """the 'nearest target' cell text and offset text and score (None outside) and colour, as the tables write it"""
    f = fams(v, plane, new)
    if f:
        s, fam, lab, t = f[0]
        return f'{lab} ({fam})', offs(v - t), round(s, 2), colour(s), f
    o = outside(v, new)
    if not o:
        return None, None, None, '', f
    fam, lab, t, tol = o
    return f'{lab} ({fam}) — outside ±{tol:.3g}', offs(v - t), None, '', f


def t24_comment(v, plane, new=True):
    f = fams(v, plane, new)
    if f:
        s, fam, lab, t = f[0]
        if fam == 'conj':
            return f'0 · conjunction ({plane} < {CONJ[plane]}) · {offs(v)} · {s:.2f}', colour(s), f
        return f'{lab} · {fam} · {offs(v - t)} · {s:.2f}', colour(s), f
    o = outside(v, new)
    fam, lab, t, tol = o
    return f'nearest: {lab} · {fam} — outside ±{tol:.3g} · {offs(v - t)}', '', f


def ra_d(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)
