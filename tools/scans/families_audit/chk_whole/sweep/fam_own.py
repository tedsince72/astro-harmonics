"""Own implementation of Eddie's distance families (written from CLAUDE.md 'Families'; not importing families.py).
Data copied: the 48 ninth ranges (rebuild_kit/active_vibrations.py _NINTH_RANGES, numbers only)."""
import math
from decimal import Decimal, ROUND_FLOOR

PHI = (1 + 5 ** 0.5) / 2
SQ2 = 2 ** 0.5
SILV = 1 + SQ2

NINTHS = [
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
PHIPOW = [('φ^%d' % p, PHI ** p) for p in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] + \
         [('10×φ^%d' % p, 10 * PHI ** p) for p in (-1, 1, 2, 3, 4, 5, 6, 7)] + \
         [('100×φ^%d' % p, 100 * PHI ** p) for p in (-1, 1)]
SQRT2T = [SQ2, 10 * SQ2, 100 * SQ2, SQ2 / 2, 10 * SQ2 / 2, 100 * SQ2 / 2]
# silver forms: 2.414, 24.14, 0.414, 4.14, 41.4  (0.414 = silver - 2 = sqrt2 - 1)
SILVT = [SILV, 10 * SILV, SILV - 2, 10 * (SILV - 2), 100 * (SILV - 2)]


def digits4(x):
    d = Decimal(format(x, '.12g'))
    if d <= 0:
        return None
    k = d.adjusted()  # floor(log10)
    q = (d / (Decimal(10) ** (k - 3))).to_integral_value(rounding=ROUND_FLOOR)
    return k, int(q)


def dmatch(v, t):
    a, b = digits4(v), digits4(t)
    return a is not None and a == b


def sq(tol, dev):
    return (10.0 * (tol - dev) / tol) ** 2


def evaluate(v, plane):
    """Return list of hits (family, target_value, score). plane: 'RA', 'Dec', 'Equator' or None."""
    hits = []
    t = round(v)
    if 1 <= t <= 200 and abs(v - t) < 0.02:
        hits.append(('whole', float(t), sq(0.02, abs(v - t))))
    th = math.floor(v) + 0.5
    if 0.5 <= th <= 199.5 and abs(v - th) < 0.01:
        hits.append(('half', th, sq(0.01, abs(v - th))))
    k = round(v / PHI)
    if k >= 1:
        tg = k * PHI
        if abs(v - tg) < 0.03236 and dmatch(v, tg):
            hits.append(('golden', tg, sq(0.03236, abs(v - tg))))
    for lab, tg in PHIPOW:
        tol = max(0.005 * tg, 0.025)
        if abs(v - tg) <= tol and dmatch(v, tg):
            hits.append(('phi power', tg, sq(tol, abs(v - tg))))
    for lo, hi, tol, tg in NINTHS:
        if lo <= v < hi and dmatch(v, tg):
            hits.append(('ninth', tg, max(0.0, 100.0 * (tol - abs(v - tg)) / tol)))
    for fam, lst in (('sqrt2', SQRT2T), ('silver', SILVT)):
        for tg in lst:
            tol = max(0.005 * tg, 0.025)
            if abs(v - tg) <= tol and dmatch(v, tg):
                hits.append((fam, tg, sq(tol, abs(v - tg))))
    if plane == 'RA' and v < 1.5:
        hits.append(('conj', 0.0, sq(1.5, v)))
    elif plane == 'Dec' and v < 0.3:
        hits.append(('conj', 0.0, sq(0.3, v)))
    return hits


def best(v, plane):
    h = evaluate(v, plane)
    if not h:
        return None, False
    h.sort(key=lambda x: -x[2])
    tie = len(h) > 1 and abs(h[0][2] - h[1][2]) < 1e-9
    return h[0], tie


def ninth_ambiguous(v):
    """ranges whose listed target 0.999999 / 9.999999 / 99.999999 vs exact 1 / 10 / 100 could change the 4-digit match"""
    return any(lo <= v < hi for lo, hi, tol, tg in NINTHS if str(tg).startswith('9'))


def parse_label(lab, fam):
    lab = lab.strip()
    if fam == 'conj':
        return 0.0
    if '×φ^' in lab:
        a, p = lab.split('×φ^')
        return float(a) * PHI ** int(p)
    if lab.startswith('φ^'):
        return PHI ** int(lab[2:])
    if lab.endswith('×φ'):
        return float(lab[:-2]) * PHI
    return float(lab)


def same_target(fam, tv, lab_val):
    if fam == 'conj':
        return True
    return abs(tv - lab_val) <= 1e-3 * max(1.0, abs(tv))


FAMNORM = {'whole': 'whole', 'half': 'half', 'golden': 'golden', 'phi power': 'phi power', 'ninth': 'ninth',
           'sqrt2': 'sqrt2', 'silver': 'silver', 'conj': 'conj', 'conjunction': 'conj'}
