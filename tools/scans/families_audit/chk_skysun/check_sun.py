"""SKY SUN and SKY MOON sheets (Eddie, 1 Nov 2026): a build before (commit fce24a12's tools/) against a build after.
usage: python3 check_sun.py <before.xlsx> <after.xlsx>
(a) sheet order: before with SKY SUN, SKY MOON straight after SKY JUPITER; every existing sheet identical (values, styles, comments, merges,
    widths, freeze); new sheets no freeze, column widths = SKY JUPITER's;
(b) blocks in order: SKY SUN = SKY JUPITER's; SKY MOON = SKY JUPITER's minus T24 SKY, LONG TIMELINE, STAR TIMELINE, LONG STAR TIMELINE;
(c) cross-check S Sun → S Jupiter = S Jupiter → S Sun (and Moon), both planes (value, +5, target, group, offset, score); S Sun / S Moon →
    S equator Dec = |Dec| from POSITIONS;
(d) partners: the centre never a partner (SKY block, SKY EQ, pair blocks), S Jupiter a partner, the Moon on SKY SUN / the Sun on SKY MOON,
    no S Rahu – S Ketu pair; titles / headers name the centre, no 'Jupiter' left in a bold cell, SKY MOON 'Sun included', not 'Moon included';
(e) SKY MOON TIMELINE: window -5 / +20 in its title, every event inside it, time order, markers; each event = a timing cell of its source
    row (minutes ±0.15; SKY cells outside at the off recomputed from their value at the off and +5 with families.outside), and every timing
    cell / outside SKY cell inside the window has its event (together rows left out).
Prints counts and 'mismatches: n'."""
import re, sys, os, openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import families

b, a = (openpyxl.load_workbook(p) for p in sys.argv[1:3])
bad = []
memo = {}
NEW = ('SKY SUN', 'SKY MOON')


def sty(wb, c):
    if getattr(c, '_style', None) is None:
        return 'merged'
    k = (id(wb), tuple(c._style))
    if k not in memo:
        memo[k] = (repr(c.font), repr(c.fill), repr(c.border), repr(c.alignment), c.number_format, repr(c.protection))
    return memo[k]


# (a)
want = list(b.sheetnames)
want[want.index('SKY JUPITER') + 1:want.index('SKY JUPITER') + 1] = list(NEW)
if a.sheetnames != want:
    bad.append(('sheet order', a.sheetnames))
ncell = 0
for name in b.sheetnames:
    wb_, wa = b[name], a[name]
    if wb_.freeze_panes != wa.freeze_panes:
        bad.append(('freeze', name))
    if sorted(map(str, wb_.merged_cells.ranges)) != sorted(map(str, wa.merged_cells.ranges)):
        bad.append(('merges', name))
    wd = lambda ws: {k: (d.width, d.customWidth) for k, d in ws.column_dimensions.items() if d.customWidth}
    if wd(wb_) != wd(wa) or (wb_.max_row, wb_.max_column) != (wa.max_row, wa.max_column):
        bad.append(('widths / size', name))
    for rb, ra in zip(wb_.iter_rows(), wa.iter_rows()):
        for cb, ca in zip(rb, ra):
            ncell += 1
            if cb.value != ca.value or sty(b, cb) != sty(a, ca) or (cb.comment.text if cb.comment else None) != (ca.comment.text if ca.comment else None):
                bad.append(('cell', name, ca.coordinate))
wd = lambda ws: {k: (d.width, d.customWidth) for k, d in ws.column_dimensions.items() if d.customWidth}
for n in NEW:
    if wd(a[n]) != wd(a['SKY JUPITER']):
        bad.append(('widths new', n))
    if a[n].freeze_panes is not None:
        bad.append(('freeze new', n, a[n].freeze_panes))
print('existing sheets compared:', len(b.sheetnames), 'sheets,', ncell, 'cells')

# (b)
TIDS = ('SKY', 'SKY EQ', 'SKY PAIRS', 'SKY STARS', 'SKY ROYAL', 'T24 SKY', 'TIMELINE', 'LONG TIMELINE', 'STAR TIMELINE', 'LONG STAR TIMELINE')
rows = {n: [tuple(c.value for c in r) for r in a[n].iter_rows()] for n in ('SKY JUPITER',) + NEW}


def seq(n):
    out = []
    for r in rows[n]:
        if r and r[0] in TIDS and (not out or out[-1] != r[0]):
            out.append(r[0])
    return out


sj = seq('SKY JUPITER')
if seq('SKY SUN') != sj:
    bad.append(('blocks SKY SUN', seq('SKY SUN'), sj))
if seq('SKY MOON') != [t for t in sj if t not in ('T24 SKY', 'LONG TIMELINE', 'STAR TIMELINE', 'LONG STAR TIMELINE')]:
    bad.append(('blocks SKY MOON', seq('SKY MOON')))
print('blocks:', {n: seq(n) for n in rows})

# (c)
pos = {r[3]: r[6] for r in b['POSITIONS'].iter_rows(min_row=5, values_only=True) if r and r[0] == 'SKY' and r[3]}
skyrow = lambda n, lab: next((r for r in rows[n] if r[0] == 'SKY' and r[1] == lab), None)
CELLS = (0, 1, 2, 3, 4, 5)                                 # value, +5, target, group, offset, score
for C in ('Sun', 'Moon'):
    x, y = skyrow(f'SKY {C.upper()}', f'S {C} → S Jupiter'), skyrow('SKY JUPITER', f'S Jupiter → S {C}')
    for c0 in (2, 11):                                     # RA from column C, Dec from column L
        if x is None or y is None or [x[c0 + k] for k in CELLS] != [y[c0 + k] for k in CELLS]:
            bad.append(('cross-check', C, c0, x and x[c0:c0 + 6], y and y[c0:c0 + 6]))
    print(f'cross-check S {C} → S Jupiter:', 'RA', x[2:8], '| Dec', x[11:17])
    e = skyrow(f'SKY {C.upper()}', f'S {C} → S equator')
    if e is None or e[11] != round(abs(pos[C]), 6):
        bad.append(('equator', C, e and e[11], abs(pos[C])))
    print(f'S {C} → S equator Dec', e and e[11], '= |Dec|', round(abs(pos[C]), 6))

# (d)
PT = re.compile(r"S ([A-Za-z' ]+?)(?= → | – | = |: |$)")
for C, other in (('Sun', 'Moon'), ('Moon', 'Sun')):
    n = f'SKY {C.upper()}'
    labs = [r[1] for r in rows[n] if r[0] == 'SKY' and r[1] and r[1].startswith('S ')]
    eq = [r[1] for r in rows[n] if r[0] == 'SKY EQ' and isinstance(r[1], str) and r[1].startswith('S ') and ' = ' in r[1]]
    prs = [r[2] for r in rows[n] if r[0] in ('SKY PAIRS', 'SKY STARS', 'SKY ROYAL') and r[1] != 'block']
    partners = [PT.findall(l.split(' → ', 1)[1]) for l in labs] + [PT.findall(l.split(': ', 1)[1]) for l in eq] + [PT.findall(p) for p in prs]
    flat = [z for p in partners for z in p]
    if any(not l.startswith(f'S {C} → ') for l in labs) or any(not l.startswith(f'S {C}: ') for l in eq):
        bad.append(('centre', n))
    if C in flat:
        bad.append(('centre as partner', n, flat.count(C)))
    if 'Jupiter' not in flat or other not in flat:
        bad.append(('partners', n, 'Jupiter' in flat, other in flat))
    if any(set(p) == {'Rahu', 'Ketu'} for p in partners):
        bad.append(('Rahu – Ketu', n))
    bold = [c.value for r in a[n].iter_rows() for c in r if isinstance(c.value, str) and c.font and c.font.b]
    if any('Jupiter' in t or re.search(r'\bJup\b', t) for t in bold):
        bad.append(('Jupiter in a title', n, [t[:80] for t in bold if 'Jupiter' in t][:3]))
    if C == 'Moon' and (not any('Sun included' in t for t in bold) or any('Moon included' in t for t in bold)):
        bad.append(('Sun included', n))
    print(n, 'SKY rows', len(labs), 'SKY EQ', len(eq), 'pair rows', len(prs), '| Jupiter as partner', flat.count('Jupiter'), f'| {other} as partner', flat.count(other))

# (e) SKY MOON TIMELINE
n = 'SKY MOON'
TM = re.compile(r'\((?:in )?([\d.]+) min( ago)?\)')
tl = [r for r in rows[n] if r[0] == 'TIMELINE']
title = next((r[0] for r in rows[n] if isinstance(r[0], str) and r[0].startswith('TIMELINE (')), '')
if 'window −5 / +20 min (the Moon moves about 0.5° an hour)' not in title:
    bad.append(('Moon TIMELINE title',))
evs = [r for r in tl if r[3] and not str(r[3]).startswith('———')]
marks = [r for r in tl if r[3] and str(r[3]).startswith('———')]
if [m[3] for m in marks] != ['——— OFF ———', '——— OFF + 5 MIN ———']:
    bad.append(('markers', [m[3] for m in marks]))
ts = [r[2] for r in tl]
if ts != sorted(ts):
    bad.append(('order',))
if any(not (-5.0 <= r[2] <= 20.0) for r in evs):
    bad.append(('outside window', [(r[4], r[2]) for r in evs if not (-5.0 <= r[2] <= 20.0)]))
cands = []                                                 # (points, minutes, where)
for r in rows[n]:
    if r[0] not in ('SKY', 'SKY EQ', 'SKY PAIRS', 'SKY STARS', 'SKY ROYAL') or r[1] in ('points', 'block') or r[1] is None:
        continue
    if r[0] in ('SKY PAIRS', 'SKY STARS', 'SKY ROYAL') and r[16] and 'X, Y together' in str(r[16]):
        continue
    pts = set(PT.findall(str(r[2] if r[0] != 'SKY' and r[0] != 'SKY EQ' else r[1]))) | {'Moon'}
    for v in r:
        if isinstance(v, str):
            for m in TM.finditer(v):
                cands.append((pts, -float(m.group(1)) if m.group(2) else float(m.group(1)), r[0]))
    if r[0] == 'SKY':                                      # outside at the off: nearest target recomputed
        for c0, pl in ((2, 'RA'), (11, 'Dec')):
            v0, v5, sc = r[c0], r[c0 + 1], r[c0 + 5]
            if isinstance(v0, float) and isinstance(v5, float) and sc is None and v5 != v0:
                o = families.outside(v0, 'Dec' if r[1].endswith('equator') else pl, 'deg')
                if o:
                    cands.append((pts, (o['tv'] - v0) / ((v5 - v0) / 5.0), 'SKY outside'))
edge = [c for c in cands if round(c[1], 1) in (-5.0, 20.0)]          # shown at the edge (1 dp): may fall either side
win = [c for c in cands if -5.0 <= c[1] <= 20.0 and c not in edge]
evpts = lambda r: set(PT.findall(str(r[4]))) | {'Moon'}
PS = {r[3]: (r[5], r[6], r[7], r[8]) for r in b['POSITIONS'].iter_rows(values_only=True) if r and r[0] == 'SKY' and r[3] and isinstance(r[5], float)}


def dmid(p, q, pl, m):
    (a0, d0, ra, rd), (b0, e0, rb, re_) = PS[p], PS[q]
    ra, rd, rb, re_ = (0.0 if isinstance(x, str) else x for x in (ra, rd, rb, re_))
    A, D, B, E = a0 + ra * m, d0 + rd * m, b0 + rb * m, e0 + re_ * m
    if pl == 'RA':
        x = abs(A - B) % 360.0
        return min(x, 360.0 - x)
    return abs(D - E) if pl == 'Dec' else abs(abs(D) - abs(E))


def mid_t(r):
    """a midpoint event (no timing cell when the nearest interval is not 1): the larger / smaller ratio of the off, linear off -> +5,
    reaching 1, from POSITIONS and its rates"""
    c, xy = r[4].split(': ', 1)
    x, y = (z[2:] for z in re.split(' – | = ', xy))
    c = c[2:]
    q = [(dmid(c, x, r[5], m), dmid(c, y, r[5], m)) for m in (0.0, 5.0)]
    big = q[0][0] >= q[0][1]
    q0, q5 = ((u / v) if big else (v / u) for u, v in q)
    return (1.0 - q0) / ((q5 - q0) / 5.0)


mids = [r for r in evs if str(r[6]).startswith('midpoint')]
for r in mids:
    cands.append((evpts(r), mid_t(r), 'midpoint from POSITIONS'))
miss_src = [r for r in evs if not any(abs(c[1] - r[2]) <= 0.15 and evpts(r) <= c[0] for c in cands)]
miss_ev = [c for c in win if not any(abs(c[1] - r[2]) <= 0.15 and evpts(r) <= c[0] for r in evs)]
if miss_src:
    bad.append(('event without a source cell', [(r[4], r[2]) for r in miss_src]))
if miss_ev:
    bad.append(('timing cell in the window without an event', [(sorted(c[0]), round(c[1], 1), c[2]) for c in miss_ev]))
print('SKY MOON window edge cells (shown -5.0 / 20.0, not required):', [(sorted(c[0]), round(c[1], 3), c[2]) for c in edge])
print(f'SKY MOON TIMELINE midpoint events recomputed from POSITIONS: {len(mids)}')
print(f'SKY MOON TIMELINE: {len(evs)} events (window -5 / +20), timing cells in the window {len(win)}, '
      f'before the off {sum(1 for r in evs if r[2] < 0)}, after {sum(1 for r in evs if r[2] >= 0)}')
for k in ('TIMELINE', 'LONG TIMELINE', 'STAR TIMELINE', 'LONG STAR TIMELINE'):
    t = next((r[0] for r in rows['SKY SUN'] if isinstance(r[0], str) and r[0].startswith(k + ' (')), None)
    print(f'SKY SUN {k}:', t and t.split(': ')[-1])
for x in bad[:20]:
    print('  ', x)
print('mismatches:', len(bad))
