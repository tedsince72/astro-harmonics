"""jcore.py - shared pieces for the Jupiter-centred read (tools/jup/). Rules: Eddie, 12 Oct 2026 (see docs/jupiter/README.md)."""
import csv, math, json, os
from math import gcd

NATAL_BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres',
                'Pallas', 'Juno', 'Vesta', 'Rahu', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Orcus', 'Quaoar', 'Gonggong',
                'Transpluto']
SKY_BODIES = NATAL_BODIES + ['Moon']          # sky Moon allowed as a sky body
PLANES = ('RA', 'Dec', 'Flat', 'GC')

# number windows
TOL = {'pair': (0.005, 0.0005), 'move': (0.01, 0.0011), 'equator': (0.01, 0.0011)}
MIN_VALUE = 0.5                               # values below 0.5 are not numbers / not ratioed
# contact
CLOSE = (1.5, 0.3); NEAR = (2.0, 0.6)         # cross link / sky contact: RA < a OR Dec < b
INSIDE_CLOSE = (1.5, 0.6)                     # conjunction inside one chart: RA < 1.5 or Dec < 0.6
# ratio bands (percent)
R_SKYNAT = (0.005, 0.01); R_HJ = (0.005, 0.02); R_FAMILY = (0.005, 0.02); R_EQ = (0.01, 0.05)
R_SAMEBODY = 0.15; R_PAIRSET = 0.05; R_SHARED = 0.5; R_SPLIT = 0.25


def wrap_ra(a, b):
    d = abs(a - b) % 360.0
    return 360.0 - d if d > 180.0 else d


def signed_ra(frm, to):
    d = (to - frm) % 360.0
    return d - 360.0 if d > 180.0 else d


def gc(p, q):
    r1, d1, r2, d2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    dr = r2 - r1
    num = math.hypot(math.cos(d2) * math.sin(dr), math.cos(d1) * math.sin(d2) - math.sin(d1) * math.cos(d2) * math.cos(dr))
    den = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(dr)
    return math.degrees(math.atan2(num, den))


def planes(p, q):
    ra = wrap_ra(p[0], q[0]); de = abs(p[1] - q[1])
    return {'RA': ra, 'Dec': de, 'Flat': math.hypot(ra, de), 'GC': gc(p, q)}


def tag(v, kind='pair'):
    """'W12' / 'N40/9' / '' . whole first; a ninth only when n/9 is not whole."""
    if v is None or v < MIN_VALUE:
        return ''
    tw, tn = TOL[kind]
    w = round(v)
    if abs(v - w) <= tw:
        return f'W{w}'
    n = round(v * 9)
    if n % 9 and abs(v - n / 9) <= tn:
        return f'N{n}/9'
    return ''


def label(t):
    """W12 -> 12, N40/9 -> 40/9"""
    return t[1:] if t else ''


def contact(ra, de, lim=CLOSE):
    return ra < lim[0] or de < lim[1]


def band(ra, de):
    if contact(ra, de, CLOSE):
        return 'close'
    if contact(ra, de, NEAR):
        return 'near'
    return ''


def star_band(ra, de):
    if ra < 1.5 and de < 0.3:
        return 'on'
    if ra < 2.0 and de < 0.6:
        return 'near'
    return ''


FRACS = sorted({(p // gcd(p, q), q // gcd(p, q)) for q in range(1, 10) for p in range(q, 31)}, key=lambda f: f[0] / f[1])


def fit(a, b, allow1=False):
    """ratio of the larger to the smaller value -> (p, q, err_pct, 'a/b' or 'b/a'); None if a value < 0.5."""
    if a < MIN_VALUE or b < MIN_VALUE:
        return None
    big, small, d = (a, b, 'a/b') if a >= b else (b, a, 'b/a')
    r = big / small
    best = None
    for p, q in FRACS:
        if p == q and not allow1:
            continue
        e = abs(r / (p / q) - 1) * 100
        if best is None or e < best[2]:
            best = (p, q, e, d)
    return best


def frac(f):
    return f'{f[0]}' if f[1] == 1 else f'{f[0]}/{f[1]}'


def fmt(v, n=5):
    return f'{v:.{n}f}'


def load_race(race):
    """-> sky {body: (ra, dec, kind)}, runners {P##: {'name':..., 'H': {...}, 'J': {...}}}"""
    sky, run = {}, {}
    with open(f'docs/jupiter/{race}/positions.csv') as fh:
        for r in csv.DictReader(fh):
            v = (float(r['ra']), float(r['dec']), r['kind'])
            if r['runner'] == 'SKY':
                sky[r['body']] = v
            else:
                d = run.setdefault(r['runner'], {'name': f"{r['cloth']} {r['horse']} / {r['jockey']}",
                                                 'horse': r['horse'], 'jockey': r['jockey'], 'H': {}, 'J': {}})
                d[r['chart']][r['body']] = v
    return sky, run


def ketu(p):
    return ((p[0] + 180.0) % 360.0, -p[1], p[2])


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fh:
        json.dump(obj, fh, indent=1)


def tags_all(vals, kind='pair'):
    """{plane: value} -> [(plane, value, tag)] for tagged planes"""
    return [(pl, v, tag(v, kind)) for pl, v in vals.items() if tag(v, kind)]


def tagstr(t):
    return ', '.join(f'{pl} {v:.5f} ({label(tg)})' for pl, v, tg in t)
