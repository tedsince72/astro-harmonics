import sys, math, re
from math import gcd
sys.path.insert(0, '/Users/eddieplace/astro-harmonics/rebuild_kit')
import openpyxl
from active_vibrations import (score_whole, score_phi_interval, score_phi_powers,
                               score_ninth, _NINTH_RANGES, _PHI_POWER_TARGETS)

REPO = '/Users/eddieplace/astro-harmonics/'
INP = REPO + 'reference/classic/race_batch_20220102_newcastle_aw_1330.xlsx'
OUT = REPO + 'reference/classic/race_batch_20220102_newcastle_aw_1330_jupiter_tables.xlsx'
SHEET = sys.argv[1] if len(sys.argv) > 1 else 'P09'
HTAB = SHEET
JTAB = 'P%02d' % (int(SHEET[1:]) + 1)
PHI = (1 + 5 ** 0.5) / 2
R2 = 2 ** 0.5

# ---------- positions ----------
wi = openpyxl.load_workbook(INP, data_only=True)
def load(tab):
    d = {}
    for r in wi[tab].iter_rows(min_row=2, values_only=True):
        if r[3] != 'transit_self':
            continue
        d[r[1]] = (r[4], r[8])
    return d
POS = {'S': load('TRANS'), 'H': load(HTAB), 'J': load(JTAB)}
for k in 'SHJ':
    ra, dec = POS[k]['Rahu']
    POS[k]['KetuMirror'] = ((ra + 180) % 360, -dec)

def pt(chart, name):
    """returns (ra or None, dec)"""
    if name == 'equator':
        return (None, 0.0)
    if name == 'Ketu':
        ra, dec = POS[chart]['KetuMirror']
        return (None, dec)        # Dec plane only
    if chart in 'HJ' and name == 'Moon':
        raise KeyError('natal Moon')
    d = POS[chart]
    if name + '_B' in d:
        return d[name + '_B']
    return d[name]

def ra_sep(a, b):
    x = abs(a - b) % 360
    return 360 - x if x > 180 else x

def gc(p, q):
    r1, d1 = map(math.radians, p); r2, d2 = map(math.radians, q)
    h = math.sin((d2 - d1) / 2) ** 2 + math.cos(d1) * math.cos(d2) * math.sin((r2 - r1) / 2) ** 2
    return math.degrees(2 * math.asin(min(1, math.sqrt(h))))

def planes(p, q):
    """dict plane->value; RA-dependent planes absent if either has no RA"""
    out = {'Dec': abs(p[1] - q[1])}
    if p[0] is not None and q[0] is not None:
        ra = ra_sep(p[0], q[0])
        out['RA'] = ra
        out['Flat'] = math.hypot(ra, out['Dec'])
        out['GC'] = gc(p, q)
    return out

# ---------- families ----------
def phi_label(i):
    if i < 11:
        p = (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)[i]; f = ''
    elif i < 19:
        p = (-1, 1, 2, 3, 4, 5, 6, 7)[i - 11]; f = '10×'
    else:
        p = (-1, 1)[i - 19]; f = '100×'
    return '%sφ^%d' % (f, p)

SQ = [('1.414', R2, 'sqrt2'), ('14.14', 10 * R2, 'sqrt2'), ('141.4', 100 * R2, 'sqrt2'),
      ('0.707', R2 / 2, 'sqrt2'), ('7.07', 5 * R2, 'sqrt2'), ('70.7', 50 * R2, 'sqrt2'),
      ('2.414', 1 + R2, 'silver'), ('24.14', 10 * (1 + R2), 'silver'), ('0.414', R2 - 1, 'silver'),
      ('4.14', 10 * (R2 - 1), 'silver'), ('41.4', 100 * (R2 - 1), 'silver')]
PQ = sorted({(p // gcd(p, q), q // gcd(p, q)) for q in range(2, 10) for p in range(q + 1, 31)
             if p % q != 0})

def fams(v, kind, plane, ptol):
    """list of (family, label, offset_str, score, raw_offset). kind 'deg' or 'ratio'."""
    res = []
    s = score_whole(v)
    if s > 0:
        n = round(v); res.append(('whole', str(n), v - n, s))
    s = score_phi_interval(v)
    if s > 0:
        k = round(v / PHI); res.append(('golden', '%d×φ' % k, v - k * PHI, s))
    best = None
    for i, t in enumerate(_PHI_POWER_TARGETS):
        tol = max(t * 0.005, 0.025); dev = abs(v - t)
        if dev <= tol:
            sc = (10 * (tol - dev) / tol) ** 2
            if best is None or sc > best[3]:
                best = ('phi power', phi_label(i), v - t, sc)
    if best and best[3] > 0:
        assert abs(best[3] - score_phi_powers(v)) < 1e-9
        res.append(best)
    s = score_ninth(v)
    if s > 0:
        for lo, hi, tol, t in _NINTH_RANGES:
            if lo <= v < hi:
                res.append(('ninth', '%g' % t, v - t, s)); break
    for fam in ('sqrt2', 'silver'):
        b = None
        for lab, t, f in SQ:
            if f != fam: continue
            tol = max(0.005 * t, 0.025); dev = abs(v - t)
            if dev <= tol:
                sc = (10 * (tol - dev) / tol) ** 2
                if b is None or sc > b[3]:
                    b = (fam, lab, v - t, sc)
        if b and b[3] > 0:
            res.append(b)
    if kind == 'deg' and plane in ('RA', 'Dec', 'Equator'):
        tol = 1.5 if plane == 'RA' else 0.3
        if v < tol:
            sc = (10 * (tol - v) / tol) ** 2
            if sc > 0:
                res.append(('conj', 'conj', v, sc))
    if kind == 'ratio':
        b = None
        for p, q in PQ:
            t = p / q; off = (v - t) / t * 100
            if abs(off) < ptol:
                sc = 100 * (ptol - abs(off)) / ptol
                if b is None or sc > b[3]:
                    b = ('ratio', '%d/%d' % (p, q), off, sc)
        if b and b[3] > 0:
            res.append(b)
    res.sort(key=lambda x: -x[3])
    return res

def offs(fam, off):
    return ('%+.5f%%' % off) if fam == 'ratio' else '%+.5f' % off

def colour(s):
    if s >= 80: return 'C6EFCE'
    if s >= 50: return 'FFEB9C'
    if s > 0: return 'FFF8DC'
    return None

def expected(v, kind, plane, ptol, inverted):
    f = fams(v, kind, plane, ptol)
    exp = {}
    if f:
        b = f[0]
        lab = '%s (%s)' % (b[1], b[0]) + (' (inverted)' if inverted else '')
        exp['target'] = lab
        exp['offset'] = offs(b[0], b[2])
        exp['score'] = round(b[3], 2)
        exp['colour'] = colour(b[3])
        exp['also'] = ['%s (%s) %s [%.1f]' % (x[1], x[0], offs(x[0], x[2]), x[3]) for x in f[1:]]
        exp['ties'] = [x for x in f[1:] if abs(x[3] - b[3]) < 1e-9]
    else:
        exp['target'] = None; exp['colour'] = None; exp['also'] = []
    # scaled
    cands = []
    for tag, sv in (('x10', 10 * v), ('/10', v / 10)):
        ff = [x for x in fams(sv, kind, plane, ptol) if x[0] != 'conj']
        if ff:
            cands.append((tag, ff[0]))
    if cands:
        cands.sort(key=lambda c: -c[1][3])
        tag, b = cands[0]
        s = '%s: %s (%s) %s [%.1f]' % (tag, b[1], b[0], offs(b[0], b[2]), b[3])
        if tag == '/10' and kind == 'deg':
            s += ' (widens 10x in degrees)'
        exp['scaled'] = s; exp['scaled_colour'] = colour(b[3])
        exp['scaled_tie'] = len(cands) == 2 and abs(cands[0][1][3] - cands[1][1][3]) < 1e-9
    else:
        exp['scaled'] = None; exp['scaled_colour'] = None
    return exp

# ---------- label parsing ----------
def parse_point(s):
    s = s.strip()
    ch, name = s[0], s[2:].strip()
    return ch, name

def P(s):
    ch, n = parse_point(s)
    return pt(ch, n)

def mid_offsets(a, b, c):
    out = {}
    out['Dec'] = c[1] - (a[1] + b[1]) / 2
    if a[0] is not None and b[0] is not None and c[0] is not None:
        d = ((b[0] - a[0] + 180) % 360) - 180
        m = (a[0] + d / 2) % 360
        out['RA'] = ((c[0] - m + 180) % 360) - 180
    return out

def ratio_planes(num, den):
    out = {}
    for pl in num:
        if pl in den and den[pl] > 0 and num[pl] > 0:
            n, d = num[pl], den[pl]
            out[pl] = (max(n, d) / min(n, d), n < d)
    return out

def compute(table, label):
    """returns (mode, {plane: value or (value, inverted)}, kind)"""
    t = int(table[1:])
    lab = re.sub(r'\s+\(RA span.*|\s+\(Dec span.*', '', label).strip()
    if t <= 8:
        a, b = lab.split('→')
        return 'deg', {k: (v, False) for k, v in planes(P(a), P(b)).items()}
    if t == 9:
        if lab.endswith('Equator'):
            p = P(lab[:-len('Equator')])
            return 'deg', {'Dec': (abs(p[1]), False)}
        a, b = lab.split(' – ')
        return 'deg', {k: (v, False) for k, v in planes(P(a), P(b)).items()}
    if t in (10, 11):
        ab, c = lab.split('|')
        a, b = ab.split(' / ')
        return 'mid', mid_offsets(P(a), P(b), P(c))
    if t in (12, 13):
        n, d = lab.split(' / ')
        n1, n2 = n.split('–'); d1, d2 = d.split('–')
        return 'ratio', ratio_planes(planes(P(n1), P(n2)), planes(P(d1), P(d2)))
    if t == 14:
        inv = lab.endswith('(inverted)')
        l2 = lab.replace('(inverted)', '').strip()
        a, b = l2.split(' / ')
        va = abs(P(a.replace('|Dec|', ''))[1]); vb = abs(P(b.replace('|Dec|', ''))[1])
        return 'ratio1', {'Equator': (max(va, vb) / min(va, vb), va < vb, inv)}
    if t == 15:
        inv = lab.endswith('(inverted)')
        l2 = lab.replace('(inverted)', '').strip()
        m = re.match(r'\((.*)\) / \((.*)\)$', l2)
        n, d = m.group(1), m.group(2)
        n1, n2 = n.split('–'); d1, d2 = d.split('–')
        if d2.strip() == 'equator':
            pn = planes(P(n1), P(n2)); den = abs(P(d1)[1])
            v = pn['Dec']
            return 'ratio1', {'Dec': (max(v, den) / min(v, den), v < den, inv)}
        return 'ratio', ratio_planes(planes(P(n1), P(n2)), planes(P(d1), P(d2)))
    raise ValueError(table)

# ---------- read sheet ----------
wo = openpyxl.load_workbook(OUT)
ws = wo[SHEET]
PLANE_COL = {}
def fill(c):
    if c.fill and c.fill.fill_type:
        rgb = c.fill.fgColor.rgb
        if rgb and rgb != '00000000':
            return rgb[-6:]
    return None

cells = 0
mism = []
notes = []
rows_done = {}
for r in range(1, ws.max_row + 1):
    a = ws.cell(r, 1).value
    if a == 'table':
        PLANE_COL = {}
        for i in range(4):
            h = ws.cell(r, 3 + 8 * i).value
            if h: PLANE_COL[h] = 3 + 8 * i
        continue
    if not (isinstance(a, str) and re.match(r'^T\d+$', a)):
        continue
    label = ws.cell(r, 2).value
    if ws.cell(r, 3).value is None and all(ws.cell(r, c).value is None for c in range(4, 35)) :
        continue  # title row
    if label is None or (ws.cell(r + 0, 1).value and ws.cell(r, 3).value is None and ws.cell(r, 11).value is None
                         and ws.cell(r, 19).value is None and ws.cell(r, 27).value is None):
        continue
    table = a
    try:
        mode, vals = compute(table, label)
    except Exception as e:
        mism.append((r, table, label, 'PARSE', str(e))); continue
    rows_done[table] = rows_done.get(table, 0) + 1
    for plane, c0 in PLANE_COL.items():
        sv = ws.cell(r, c0).value
        tgt = ws.cell(r, c0 + 2).value; off = ws.cell(r, c0 + 3).value; sc = ws.cell(r, c0 + 4).value
        also = ws.cell(r, c0 + 6).value; scaled = ws.cell(r, c0 + 7).value
        col = fill(ws.cell(r, c0)); scol = fill(ws.cell(r, c0 + 7))
        p5 = ws.cell(r, c0 + 1).value
        def M(what, sheet, mine):
            mism.append((r, table, label[:70], plane, what, sheet, mine))
        cells += 7
        if plane not in vals:
            if any(x is not None for x in (sv, tgt, off, sc, also, scaled)):
                M('cell present but plane n/a for me', sv, None)
            continue
        if mode == 'mid':
            v = vals[plane]
            if sv is None or abs(sv - v) > 2e-6:
                M('value', sv, round(v, 6))
            exp_t = 'midpoint (midpoint)'
            if tgt != exp_t: M('target', tgt, exp_t)
            if off != '%+.5f' % v: M('offset', off, '%+.5f' % v)
            tt = round(abs(v) / 0.05, 2)
            if sc is None or abs(sc - tt) > 0.011: M('score', sc, tt)
            av = abs(v)
            ec = 'C6EFCE' if av <= 0.05 else 'FFEB9C' if av <= 0.15 else 'FFF8DC' if av <= 0.45 else None
            if col != ec: M('colour', col, ec)
            if also or scaled: M('also/scaled present', (also, scaled), None)
            continue
        if mode == 'deg':
            v, inv = vals[plane]; kind = 'deg'; ptol = None; pl = plane
            # equator values in Dec column (T1/T2 'equator', T9 Equator) count as Dec
        elif mode == 'ratio':
            v, inv = vals[plane]; kind = 'ratio'; ptol = 0.005; pl = plane
        else:
            v, inv, labinv = vals[plane]; kind = 'ratio'; ptol = 0.01 if table == 'T14' else 0.005; pl = plane
            if labinv != inv: M('row (inverted) flag', labinv, inv)
            inv = False  # flag lives in the row label
        if sv is None or abs(sv - v) > 2e-6:
            M('value', sv, round(v, 6))
        e = expected(v, kind, pl, ptol, inv)
        if e.get('ties'): notes.append((r, table, label, plane, 'tie', e['ties']))
        if e.get('scaled_tie'): notes.append((r, table, label, plane, 'scaled tie'))
        if tgt != e['target']: M('target', tgt, e['target'])
        if e['target']:
            if off != e['offset']: M('offset', off, e['offset'])
            if sc is None or abs(sc - e['score']) > 0.011: M('score', sc, e['score'])
        else:
            if off is not None or sc is not None: M('offset/score present', (off, sc), None)
        if col != e['colour']: M('colour', col, e['colour'])
        sh_also = [x.strip() for x in re.split(r';\s*|,\s(?=[^\]]*\[)', also)] if also else []
        sh_also = [x for x in sh_also if x]
        if sorted(sh_also) != sorted(e['also']): M('also', also, e['also'])
        if scaled != e['scaled']: M('scaled', scaled, e['scaled'])
        if scol != e['scaled_colour']: M('scaled colour', scol, e['scaled_colour'])

print('sheet', SHEET, 'rows per table', rows_done)
print('cells compared', cells)
print('mismatches', len(mism))
for m in mism: print('  ', m)
print('notes', len(notes))
for n in notes[:40]: print('  ', n)
