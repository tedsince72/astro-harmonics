"""core.py - JR v2 (transit-Jupiter reader) shared pieces: points, planes, number families, tolerances, levels.
Design: docs/classic/jupiter_reader_design.md (sections 1-4, 5G). JR v1 (tools/jup/) is not used or changed here,
except that its positions step (tools/jup/positions.py) writes positions.csv."""
import csv, math

PHI = (1 + 5 ** 0.5) / 2
R2 = 2 ** 0.5
SILVER = 1 + R2

NATAL_BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres',
                'Pallas', 'Juno', 'Vesta', 'Rahu', 'Ketu', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Orcus', 'Quaoar',
                'Gonggong', 'Transpluto']
SKY_BODIES = NATAL_BODIES + ['Moon']
ROYAL = ['Aldebaran', 'Regulus', 'Antares', 'Fomalhaut']
SLOW = {'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Rahu', 'Ketu', 'Eris', 'Sedna', 'Haumea', 'Makemake',
        'Orcus', 'Quaoar', 'Gonggong', 'Transpluto'}
STAR_NAMES = {'Algol', 'Pleiades', 'Aldebaran', 'Capella', 'Sirius', 'Procyon', 'Regulus', 'Alkaid', 'Algorab', 'Spica',
              'Arcturus', 'Alphecca', 'Antares', 'Vega', 'Deneb Algedi', 'Fomalhaut', 'Rigel', 'Betelgeuse', 'Polaris',
              'Castor', 'Altair', 'Bellatrix'}
PLANES = ('RA', 'Dec', 'Flat', 'GC')
EQUATOR = 'equator'

# ---- number families (section 3). Exact constants; labels as in the design.
CONSTANTS = []      # (label, value, family)
for lab, v in (('0.382', 1 / PHI ** 2), ('3.82', 10 / PHI ** 2), ('38.20', 100 / PHI ** 2),
               ('0.618', 1 / PHI), ('6.18', 10 / PHI), ('61.80', 100 / PHI),
               ('1.618', PHI), ('16.18', 10 * PHI), ('161.80', 100 * PHI),
               ('2.618', PHI ** 2), ('26.18', 10 * PHI ** 2),
               ('4.236', PHI ** 3), ('42.36', 10 * PHI ** 3),
               ('6.854', PHI ** 4), ('68.54', 10 * PHI ** 4),
               ('11.09', PHI ** 5), ('110.90', 10 * PHI ** 5),
               ('17.94', PHI ** 6), ('179.40', 10 * PHI ** 6),
               ('29.03', PHI ** 7), ('46.98', PHI ** 8), ('76.01', PHI ** 9)):
    CONSTANTS.append((lab, v, 'golden'))
for lab, v in (('1.414', R2), ('14.14', 10 * R2), ('141.4', 100 * R2),
               ('0.707', 1 / R2), ('7.07', 10 / R2), ('70.7', 100 / R2)):
    CONSTANTS.append((lab, v, 'sqrt2'))
for lab, v in (('2.414', SILVER), ('24.14', 10 * SILVER),
               ('0.414', 1 / SILVER), ('4.14', 10 / SILVER), ('41.4', 100 / SILVER)):
    CONSTANTS.append((lab, v, 'silver'))

FRACS = sorted({(p // math.gcd(p, q), q // math.gcd(p, q)) for q in range(1, 10) for p in range(1, 31) if p > q})

# ---- tolerances (section 4): kind -> (strict, near) per family group; 'abs' or 'rel' (percent)
TOL = {
    'dist':    {'mode': 'abs', 'whole': (0.005, 0.02), 'ninth': (0.0005, 0.002), 'const': (0.005, 0.02)},
    'move':    {'mode': 'abs', 'whole': (0.01, 0.03), 'ninth': (0.0011, 0.004), 'const': (0.01, 0.03)},
    'equator': {'mode': 'abs', 'whole': (0.01, 0.03), 'ninth': (0.0011, 0.004), 'const': (0.01, 0.03)},
    'ratio':   {'mode': 'rel', 'all': (0.005, 0.02)},
    'eqratio': {'mode': 'rel', 'all': (0.01, 0.06)},
}
CLOSE = (1.5, 0.3); NEAR_CONTACT = (2.0, 0.6)
MID = (0.05, 0.15)
RATIO_MIN = 0.5            # as built (JR v1 rule kept): values below 0.5 are not ratioed
LEVELS = ('strict', 'exact-in-race', 'exact-pre-off', 'near')
LEVEL_SHORT = {'strict': 'S', 'exact-in-race': 'I', 'exact-pre-off': 'P', 'near': 'N'}
PRE_OFF_MIN = 5.0


def wrap_ra(a, b):
    d = abs(a - b) % 360.0
    return 360.0 - d if d > 180.0 else d


def gc(p, q):
    r1, d1, r2, d2 = map(math.radians, (p[0], p[1], q[0], q[1]))
    dr = r2 - r1
    num = math.hypot(math.cos(d2) * math.sin(dr), math.cos(d1) * math.sin(d2) - math.sin(d1) * math.cos(d2) * math.cos(dr))
    den = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(dr)
    return math.degrees(math.atan2(num, den))


def plane_value(p, q, pl):
    if pl == 'RA':
        return wrap_ra(p[0], q[0])
    if pl == 'Dec':
        return abs(p[1] - q[1])
    if pl == 'Flat':
        return math.hypot(wrap_ra(p[0], q[0]), abs(p[1] - q[1]))
    if pl == 'GC':
        return gc(p, q)
    raise ValueError(pl)


def planes_for(*bodies):
    """Ketu: Dec only (RA duplicates Rahu). Equator: Dec only."""
    if any(b in ('Ketu', EQUATOR) for b in bodies):
        return ('Dec',)
    return PLANES


def targets(kind, lo, hi):
    """targets whose value lies in [lo, hi] -> (label, value, family, group)"""
    out = []
    if kind in ('ratio', 'eqratio'):
        for p, q in FRACS:
            v = p / q
            if lo <= v <= hi:
                out.append((f'{p}' if q == 1 else f'{p}/{q}', v, 'whole' if q == 1 else 'ratio', 'all'))
        for lab, v, fam in CONSTANTS:
            if v > 1 and lo <= v <= hi:
                out.append((lab, v, fam, 'all'))
        return out
    for w in range(max(1, math.ceil(lo)), min(180, math.floor(hi)) + 1):
        out.append((f'{w}', float(w), 'whole', 'whole'))
    for n in range(max(1, math.ceil(lo * 9)), min(1620, math.floor(hi * 9)) + 1):
        if n % 9:
            out.append((f'{n}/9', n / 9, 'ninth', 'ninth'))
    for lab, v, fam in CONSTANTS:
        if lo <= v <= hi:
            out.append((lab, v, fam, 'const'))
    return out


def classify(v0, v5, kind, dur_min):
    """All hits of one measured value. v0 at the off, v5 at off + 5 min (None = no sky leg or rate n/a).
    -> list of dicts: target, value_t, family, level, offset, t, rate, eta, as."""
    T = TOL[kind]
    rate = None if v5 is None else (v5 - v0) / 5.0
    if T['mode'] == 'rel':
        if v0 < RATIO_MIN:
            return []
        snear = T['all'][1]
        lo, hi = v0 * (1 - snear / 100), v0 * (1 + snear / 100)
    else:
        maxnear = max(T['whole'][1], T['ninth'][1], T['const'][1])
        lo, hi = v0 - maxnear, v0 + maxnear
    if rate is not None:
        lo = min(lo, v0 - PRE_OFF_MIN * rate, v0 + dur_min * rate)
        hi = max(hi, v0 - PRE_OFF_MIN * rate, v0 + dur_min * rate)
    hits = []
    for lab, tv, fam, grp in targets(kind, lo, hi):
        s, n = T[grp]
        if T['mode'] == 'rel':
            off = (v0 / tv - 1) * 100            # percent
        else:
            off = v0 - tv
        eta = None if not rate else (tv - v0) / rate   # minutes from the off (negative = before)
        if abs(off) <= s:
            lev = 'strict'
        elif eta is not None and 0 < eta <= dur_min:
            lev = 'exact-in-race'
        elif eta is not None and -PRE_OFF_MIN <= eta < 0:
            lev = 'exact-pre-off'
        elif abs(off) <= n:
            lev = 'near'
        else:
            continue
        a_s = 'n/a' if rate is None else ('applying' if (tv - v0) * rate > 0 else 'separating')
        hits.append({'target': lab, 'target_value': tv, 'family': fam, 'level': lev, 'offset': off,
                     'unit': '%' if T['mode'] == 'rel' else 'deg', 'tol': s, 't': abs(off) / s, 'rate': rate, 'eta': eta, 'as': a_s})
    return hits


def contact_level(ra, de):
    if ra < CLOSE[0] or de < CLOSE[1]:
        return 'strict'
    if ra < NEAR_CONTACT[0] or de < NEAR_CONTACT[1]:
        return 'near'
    return None


def weaker(levels):
    return max(levels, key=LEVELS.index)


def load_positions(path):
    """positions.csv (JR v1 positions step) -> sky {body: (ra, dec, kind)}, runners {P##: {...}}. Adds Ketu as Rahu's mirror
    (positions.py checks the mirror is exact; jupiter_reader.py stops if it is not) and the equator point (Dec 0)."""
    sky, run = {}, {}
    with open(path) as fh:
        for r in csv.DictReader(fh):
            v = (float(r['ra']), float(r['dec']), r['kind'])
            if r['runner'] == 'SKY':
                sky[r['body']] = v
            else:
                d = run.setdefault(r['runner'], {'cloth': r['cloth'], 'horse': r['horse'], 'jockey': r['jockey'], 'H': {}, 'J': {}})
                d[r['chart']][r['body']] = v
    for ch in [sky] + [d[c] for d in run.values() for c in 'HJ']:
        if 'Rahu' in ch:
            ra, de, _ = ch['Rahu']
            ch['Ketu'] = ((ra + 180.0) % 360.0, -de, 'body')
        ch[EQUATOR] = (0.0, 0.0, 'equator')
    return sky, run
