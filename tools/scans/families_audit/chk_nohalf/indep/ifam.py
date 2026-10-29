"""Independent family scoring (no half), written from the CLAUDE.md rules (29 Oct 2026 change: half removed).
Only data copied: the 48 ninth ranges and the phi-power exponents (as in rebuild_kit/active_vibrations.py).
WITH_HALF=True gives the before rules (half 0.5..199.5, +-0.01 absolute, squared) for classifying before/after diffs."""
import math
from decimal import Decimal

PHI = (1 + 5 ** 0.5) / 2
R2 = 2 ** 0.5

NINTH = [
    (0.1105, 0.112, 0.000611, 0.111111), (0.2215, 0.223, 0.000722, 0.222222), (0.3325, 0.334, 0.000833, 0.333333),
    (0.4435, 0.445, 0.000944, 0.444444), (0.5545, 0.556, 0.001056, 0.555556), (0.6655, 0.667, 0.001167, 0.666667),
    (0.7765, 0.778, 0.001278, 0.777778), (0.8875, 0.889, 0.001389, 0.888889), (0.9985, 1.0, 0.0015, 0.999999),
    (1.105, 1.12, 0.006111, 1.111111), (2.215, 2.23, 0.007222, 2.222222), (3.325, 3.34, 0.008333, 3.333333),
    (4.435, 4.45, 0.009444, 4.444444), (5.545, 5.56, 0.010556, 5.555556), (6.655, 6.67, 0.011667, 6.666667),
    (7.765, 7.78, 0.012778, 7.777778), (8.875, 8.89, 0.013889, 8.888889), (9.985, 10.0, 0.015, 9.999999),
    (11.05, 11.2, 0.061111, 11.111111), (22.15, 22.3, 0.072222, 22.222222), (33.25, 33.4, 0.083333, 33.333333),
    (44.35, 44.5, 0.094444, 44.444444), (55.45, 55.6, 0.105556, 55.555556), (66.55, 66.7, 0.116667, 66.666667),
    (77.65, 77.8, 0.127778, 77.777778), (88.75, 88.9, 0.138889, 88.888889), (99.85, 100.0, 0.15, 99.999999),
    (110.5, 112.0, 0.611111, 111.111111),
    (1.215, 1.23, 0.007222, 1.222222), (1.325, 1.34, 0.008333, 1.333333), (1.435, 1.45, 0.009444, 1.444444),
    (1.545, 1.56, 0.010556, 1.555556), (1.655, 1.67, 0.011667, 1.666667), (1.765, 1.78, 0.012778, 1.777778),
    (1.875, 1.89, 0.013889, 1.888889), (12.15, 12.3, 0.072222, 12.222222), (13.25, 13.4, 0.083333, 13.333333),
    (14.35, 14.5, 0.094444, 14.444444), (15.45, 15.6, 0.105556, 15.555556), (16.55, 16.7, 0.116667, 16.666667),
    (17.65, 17.8, 0.127778, 17.777778), (18.75, 18.9, 0.138889, 18.888889), (121.5, 123.0, 0.722222, 122.222222),
    (132.5, 134.0, 0.833333, 133.333333), (143.5, 145.0, 0.944444, 144.444444), (154.5, 156.0, 1.055556, 155.555556),
    (165.5, 167.0, 1.166667, 166.666667), (176.5, 178.0, 1.277778, 177.777778),
]
PHIP = ([(1, p) for p in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] + [(10, p) for p in (-1, 1, 2, 3, 4, 5, 6, 7)]
        + [(100, -1), (100, 1)])
PHIP = [(m, p, m * PHI ** p) for m, p in PHIP]
SQ = [(1.414, R2), (14.14, 10 * R2), (141.4, 100 * R2), (0.707, R2 / 2), (7.07, 10 * R2 / 2), (70.7, 100 * R2 / 2)]
SI = [(2.414, 1 + R2), (24.14, 10 * (1 + R2)), (0.414, R2 - 1), (4.14, 10 * (R2 - 1)), (41.4, 100 * (R2 - 1))]


def d4(x):
    """first 4 significant digits truncated, and the exponent k (12-significant-digit string, avoids float noise)"""
    s = Decimal(f'{x:.12g}')
    k = math.floor(math.log10(float(s)))
    return k, int((s / Decimal(10) ** (k - 3)).to_integral_value(rounding='ROUND_FLOOR'))


def dmatch(v, t):
    return v > 0 and d4(v) == d4(t)


def sq(tol, dev):
    return (10 * (tol - dev) / tol) ** 2


def cands(v):
    """every candidate target with (family, label-number, exact target, tol, inside_old, score_if_hit)"""
    out = []
    t = round(v)
    out.append(('whole', float(t), float(t), 0.02))
    k = round(v / PHI)
    out.append(('golden', ('g', k), k * PHI, 0.03236))
    for m, p, t in PHIP:
        out.append(('phi power', ('p', m, p), t, max(t * 0.005, 0.025)))
    for lo, hi, tol, t in NINTH:
        out.append(('ninth', t, t, tol))
    for lab, t in SQ:
        out.append(('sqrt2', lab, t, max(t * 0.005, 0.025)))
    for lab, t in SI:
        out.append(('silver', lab, t, max(t * 0.005, 0.025)))
    return out


def hits(v, plane, with_half=False):
    """list of (score, family, label, target) for every family hit"""
    h = []
    t = round(v)
    if 1 <= t <= 200 and abs(v - t) < 0.02:
        h.append((sq(0.02, abs(v - t)), 'whole', float(t), float(t)))
    if with_half:
        th = math.floor(v) + 0.5
        if 0.5 <= th <= 199.5 and abs(v - th) < 0.01:
            h.append((sq(0.01, abs(v - th)), 'half', th, th))
    k = round(v / PHI)
    if k >= 1 and abs(v - k * PHI) < 0.03236 and dmatch(v, k * PHI):
        h.append((sq(0.03236, abs(v - k * PHI)), 'golden', ('g', k), k * PHI))
    best = None
    for m, p, t in PHIP:
        tol = max(t * 0.005, 0.025)
        if abs(v - t) <= tol and dmatch(v, t):
            s = sq(tol, abs(v - t))
            if best is None or s > best[0]:
                best = (s, 'phi power', ('p', m, p), t)
    if best:
        h.append(best)
    for lo, hi, tol, t in NINTH:
        if lo <= v < hi and dmatch(v, t):
            s = max(0.0, 100 * (tol - abs(v - t)) / tol)
            if s > 0:
                h.append((s, 'ninth', t, t))
            break
    for fam, lst in (('sqrt2', SQ), ('silver', SI)):
        best = None
        for lab, t in lst:
            tol = max(t * 0.005, 0.025)
            if abs(v - t) < tol and dmatch(v, t):
                s = sq(tol, abs(v - t))
                if best is None or s > best[0]:
                    best = (s, fam, lab, t)
        if best:
            h.append(best)
    ctol = {'RA': 1.5, 'Dec': 0.3}.get(plane)
    if ctol and v < ctol:
        h.append((sq(ctol, v), 'conj', 0.0, 0.0))
    return h


def inside_old(fam, v, t, tol):
    if fam == 'ninth':
        for lo, hi, tl, tt in NINTH:
            if tt == t:
                return lo <= v < hi and abs(v - t) < tl
    if fam == 'phi power':
        return abs(v - t) <= tol
    return abs(v - t) < tol


def nearest(v, with_half=False):
    cs = cands(v)
    if with_half:
        th = math.floor(v) + 0.5
        if 0.5 <= th <= 199.5:
            cs.append(('half', th, th, 0.01))
    best = min(cs, key=lambda c: abs(v - c[2]) / c[3])
    fam, lab, t, tol = best
    kind = 'digit' if fam in ('golden', 'phi power', 'ninth', 'sqrt2', 'silver') and inside_old(fam, v, t, tol) else 'outside'
    return fam, lab, t, tol, kind


def evaluate(v, plane, with_half=False):
    """-> dict: hit (bool), fam, lab, t, off, score, tol, kind ('hit'/'outside'/'digit'), allhits"""
    h = hits(v, plane, with_half)
    if h:
        s, fam, lab, t = max(h, key=lambda x: x[0])
        return dict(hit=True, fam=fam, lab=lab, t=t, off=v - t, score=s, kind='hit', allhits=h)
    fam, lab, t, tol, kind = nearest(v, with_half)
    return dict(hit=False, fam=fam, lab=lab, t=t, off=v - t, score=None, tol=tol, kind=kind, allhits=[])


def fill_for(score):
    if score is None:
        return '00000000'
    if score >= 80:
        return '00C6EFCE'
    if score >= 50:
        return '00FFEB9C'
    return '00FFF8DC'


# ---- parsing of workbook label numbers -------------------------------------------------------------------------
def parse_label(fam, s):
    s = s.strip()
    if fam == 'conj' or fam.startswith('conjunction'):
        return 0.0
    if fam == 'golden':
        return ('g', int(s.split('×')[0]))
    if fam == 'phi power':
        if s.startswith('φ^'):
            return ('p', 1, int(s[2:]))
        m, p = s.split('×φ^')
        return ('p', int(m), int(p))
    return float(s)


def label_eq(fam, a, b):
    if isinstance(a, tuple) or isinstance(b, tuple):
        return a == b
    if fam in ('sqrt2', 'silver'):
        return abs(a - b) < 1e-9
    return abs(a - b) <= 6e-4 * max(1.0, abs(b)) / 100 + 1e-6 if fam == 'ninth' else abs(a - b) < 1e-9
