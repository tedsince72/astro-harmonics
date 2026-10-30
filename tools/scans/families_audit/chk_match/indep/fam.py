"""Independent family scoring for the MATCH check (own code; only the ninth ranges and phi-power targets copied as data)."""
import math
from decimal import Decimal
PHI = (1 + 5 ** 0.5) / 2
PHI_POW = ([PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] +
           [10.0 * PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7)] +
           [100.0 * PHI ** p for p in (-1, 1)])
PHI_POW_LAB = (['φ^-1'] + ['φ^%d' % p for p in range(1, 11)] +
               ['10×φ^%d' % p for p in (-1, 1, 2, 3, 4, 5, 6, 7)] + ['100×φ^-1', '100×φ^1'])
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
R2 = 2 ** 0.5
SQRT2 = [(R2 * 10 ** k, None) for k in (0, 1, 2)] + [(R2 / 2 * 10 ** k, None) for k in (0, 1, 2)]
SILVER = [((1 + R2) * 10 ** k, None) for k in (0, 1)] + [((R2 - 1) * 10 ** k, None) for k in (0, 1, 2)]


def d4(x):
    """(order of magnitude, first 4 significant digits truncated) using a 12-sig-digit decimal string."""
    x = abs(x)
    if x == 0:
        return None
    d = Decimal(repr(float(x)))
    k = d.adjusted()
    s = d.scaleb(3 - k)
    return k, int(s)


def d4s(x):  # on a value as shown at 6 dp
    d = Decimal('%.6f' % x)
    if d == 0:
        return None
    k = d.adjusted()
    return k, int(d.scaleb(3 - k))


def sq(tol, dev):
    return (10.0 * (tol - dev) / tol) ** 2


def evaluate(v, plane):
    """list of (family, target_id, label, score) inside tolerance with a score > 0 (incl. conjunction)."""
    out = []
    t = round(v)
    if 1 <= t <= 200 and abs(v - t) < 0.02:
        out.append(('whole', t, str(t), sq(0.02, abs(v - t))))
    k = round(v / PHI)
    if k >= 1 and abs(v - k * PHI) < 0.03236 and d4(v) == d4(k * PHI):
        out.append(('golden', k, '%d×φ' % k, sq(0.03236, abs(v - k * PHI))))
    for tg, lab in zip(PHI_POW, PHI_POW_LAB):
        tol = max(0.005 * tg, 0.025)
        if abs(v - tg) < tol and d4(v) == d4(tg):
            out.append(('phi power', lab, lab, sq(tol, abs(v - tg))))
    for lo, hi, tol, tg in NINTH:
        if lo <= v < hi:
            dev = abs(v - tg)
            if dev < tol and d4(v) == d4(tg):
                out.append(('ninth', tg, '%g' % tg, 100.0 * (tol - dev) / tol))
    for fam, lst in (('sqrt2', SQRT2), ('silver', SILVER)):
        for tg, _ in lst:
            tol = max(0.005 * tg, 0.025)
            if abs(v - tg) < tol and d4(v) == d4(tg):
                out.append((fam, round(tg, 6), '%g' % tg, sq(tol, abs(v - tg))))
    ct = 1.5 if plane == 'RA' else 0.3
    if v < ct:
        out.append(('conjunction', 0, '0', sq(ct, v)))
    return out


def best(v, plane):
    ev = [e for e in evaluate(v, plane) if e[3] > 0]
    if not ev:
        return None
    return max(ev, key=lambda e: e[3])
