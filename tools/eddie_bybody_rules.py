#!/usr/bin/env python3
"""Body-by-body rules (Eddie, 14 Nov 2026). BB1-BB17 from Lingfield AW 14:35 2 Apr 2021, 5 Pholas / Hollie Doyle;
BB18-BB31 from Haydock 13:45 8 Jun 2020, 7 Ishvara. Each rule's origin is in rules.json.

Usage:  python3 tools/eddie_bybody_rules.py <race>_bybody.xlsx [--out DIR]   (default DIR docs/eddie_read/bybody_rules)
        -> DIR/<race>_bbrules.md and DIR/<race>_bbrules.json

Reads the bybody workbook only (tools/eddie_bybody.py output; one sheet per runner). Never a csv, never a result.
For every rule: every runner and body holding it, with the cells; a field line ('only' / 'also: ...'); highlights.
Rule texts and origins: docs/eddie_read/bybody_rules/rules.json (and docs/eddie_read/bybody/RULE_CANDIDATES.md).

Definitions used by the rules (all from the bybody sheet, per runner and body X):
  Lines      the table 'Lines' (S X -> H/J X, natal royal star - X, H X - J X, contraparallels), with the same-body ratio
             (columns I-O) and crossed same-body ratio (P-V) on the royal-star rows.
  Same       the table 'Sky lines on the same target' (column H = the line it matches).
  Other      the table 'Other scoring sky lines on X'.
  'scores' = the row has a family (column D). A pair = a 'Same' row 'S A – S B'. A royal star = Aldebaran, Antares, Fomalhaut,
  Regulus. Lights = the Sun and the Moon.
Highlights (never rules): lights (every Sun / Moon line in Other on X); same digits a decade apart among the case's targets;
WATCH additive steps (Eddie, 14 Nov 2026): three of the case's cells, same plane (RA / Dec) and family (whole, or golden k×φ),
one multiplier = the sum of the other two; '(may be geometry)' when the three lines join the same three points (a royal star
counted as one point in sky and natal charts).
"""
import argparse, json, os, re, sys

import openpyxl

ROY = ['Aldebaran', 'Antares', 'Fomalhaut', 'Regulus']
LIGHTS = ('Sun', 'Moon')
BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Rahu', 'Ketu', 'Ceres',
          'Pallas', 'Juno', 'Vesta', 'Chiron', 'Eris', 'Gonggong', 'Haumea', 'Makemake', 'Orcus', 'Quaoar', 'Sedna',
          'Transpluto']
ORIGIN = 'Lingfield AW 14:35 2 Apr 2021, 5 Pholas / Hollie Doyle'
HERE = os.path.dirname(os.path.abspath(__file__))
RULES_JSON = os.path.join(os.path.dirname(HERE), 'docs', 'eddie_read', 'bybody_rules', 'rules.json')
KEYS = ['line', 'plane', 'v', 'fam', 'tgt', 'sc', 'also', 'match', 'sb', 'sbv', 'r', 'rpct', 'rt', 'rs', 'ralso',
        'xb', 'xbv', 'xr', 'xpct', 'xt', 'xs', 'xalso']


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def load(path):
    """{runner sheet: {body: {'L': [...], 'S': [...], 'O': [...]}}}; rows as dicts (KEYS)."""
    wb = openpyxl.load_workbook(path, read_only=True)
    out = {}
    for ws in wb:
        body, sec, D = None, None, {}
        for r in ws.iter_rows(values_only=True):
            r = list(r) + [None] * (22 - len(r))
            a = r[0]
            if a in BODIES and r[1] is None:
                body, sec = a, None
                D[body] = {'L': [], 'S': [], 'O': []}
                continue
            if body is None:
                continue
            if a == 'Lines':
                sec = 'L'; continue
            if a == 'Sky lines on the same target':
                sec = 'S'; continue
            if isinstance(a, str) and a.startswith('Other scoring sky lines on'):
                sec = 'O'; continue
            if a in (None, 'Line') or sec is None or isinstance(a, str) and a.startswith('none'):
                continue
            row = dict(zip(KEYS, r[:22]))
            if sec != 'L' and not row['fam']:
                continue
            D[body][sec].append(row)
        out[ws.title] = D
    return out


def cell(r):
    """'line plane value target family (score)'."""
    if r is None:
        return ''
    v = f"{r['v']:.6f}" if num(r['v']) else str(r['v'])
    t = f" {r['tgt']} {r['fam']} ({r['sc']})" if r['fam'] else ' (no family)'
    return f"{r['line']} {r['plane']} {v}{t}"


def ratio_txt(r, kind):
    if kind == 'same':
        return f"same-body ratio vs {r['sb']} {r['sbv']:.6f} = {r['r']:.6f} {r['rt']} ({r['rs']})"
    return f"crossed ratio vs {r['xb']} {r['xbv']:.6f} = {r['xr']:.6f} {r['xt']} ({r['xs']})"


class Body:
    def __init__(self, name, d):
        self.X, self.L, self.S, self.O = name, d['L'], d['S'], d['O']

    def lines(self, name, plane=None, scoring=False):
        return [r for r in self.L if r['line'] == name and (plane is None or r['plane'] == plane)
                and (not scoring or r['fam'])]

    def other(self, name, plane=None):
        return [r for r in self.O if r['line'] == name and (plane is None or r['plane'] == plane)]

    def same_on(self, anchor):
        """Same-target rows matching the Lines row `anchor` (column H = 'line plane')."""
        key = f"{anchor['line']} {anchor['plane']}"
        return [s for s in self.S if s['match'] == key]

    def pairs_on(self, anchor):
        out = []
        for s in self.same_on(anchor):
            m = re.match(r'S (.+) – S (.+)$', s['line'])
            if m:
                out.append((s, m.group(1), m.group(2)))
        return out

    def star_rows(self, c=None, scoring=False):
        out = []
        for r in self.L:
            m = re.match(rf'([HJ]) (\w+) – \1 {re.escape(self.X)}$', r['line'] or '')
            if m and m.group(2) in ROY and (c is None or m.group(1) == c) and (not scoring or r['fam']):
                out.append((m.group(1), m.group(2), r))
        return out

    def same_body(self, c, plane=None, scoring=True):
        return self.lines(f'S {self.X} → {c} {self.X}', plane, scoring)

    def sky_y(self, Y):
        return self.other(f'S {Y} – S {self.X}')

    def to_natal(self, Y, c):
        return self.other(f'S {Y} → {c} {self.X}')

    def lights(self):
        return [o for o in self.O if re.match(r'S (Sun|Moon) ', o['line'])]


def other_chart(c):
    return 'J' if c == 'H' else 'H'


def mult(r):
    if r['fam'] == 'whole':
        return int(r['tgt'])
    if r['fam'] == 'golden':
        return int(r['tgt'].split('×')[0])
    return None


# ---------------------------------------------------------------- rules: each returns a list of cases {key, cells}
def bb1(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                continue
            ends = []
            for E in (A, B):
                sk, nt = b.sky_y(E), b.to_natal(E, c)
                if not (sk and nt):
                    break
                ends += sk + nt
            else:
                out.append({'key': (a['line'], a['plane'], s['line'], s['plane'], s['tgt']), 'cells': [a, s] + ends})
    return out


def bb2(b):
    out = []
    for c in 'HJ':
        hold = []
        for R in ROY:
            for p in ('RA', 'Dec'):
                sk = b.other(f'S {R} – S {b.X}', p)
                nt = b.lines(f'{c} {R} – {c} {b.X}', p, scoring=True)
                if sk and nt:
                    hold.append((R, sk[0], nt[0]))
        if len({h[0] for h in hold}) >= 2:
            cells = [x for h in hold for x in h[1:]]
            cells += b.same_body(c)
            out.append({'key': (c,) + tuple(h[0] for h in hold), 'cells': cells})
    return out


def bb3(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                continue
            ends = [o for E in (A, B) for o in b.to_natal(E, c) if o['fam'] == s['fam']]
            if ends:
                out.append({'key': (a['line'], a['plane'], s['line'], s['plane'], s['tgt']), 'cells': [a, s] + ends})
    return out


def _paired_same_body(b, c):
    return [x for x in b.same_body(c) if any(True for _ in b.same_on(x))]


def bb4(b):
    out = []
    for c in 'HJ':
        for sb in _paired_same_body(b, c):
            for _, R, r in b.star_rows(c, scoring=True):
                if r['plane'] == sb['plane'] and b.same_on(r) and num(r['rs']):
                    out.append({'key': (c, R, sb['plane']), 'cells': [sb] + b.same_on(sb) + [r] + b.same_on(r),
                                'notes': [ratio_txt(r, 'same')]})
    return out


def bb5(b):
    hold = {}
    for c, R, r in b.star_rows():
        if num(r['xs']) and 'cut' in str(r['xt']) and r['xs'] >= 80:
            hold.setdefault(c, []).append(r)
    if 'H' in hold and 'J' in hold:
        rows = hold['H'] + hold['J']
        return [{'key': tuple(r['line'] for r in rows), 'cells': rows, 'notes': [ratio_txt(r, 'crossed') for r in rows]}]
    return []


def bb6(b):
    out = []
    for c in 'HJ':
        for sb in b.same_body(c):
            for s in b.same_on(sb):
                m = re.match(r'S (.+) – S (.+)$', s['line'])
                if not m:
                    continue
                for R in set(m.groups()) & set(ROY):
                    for r in b.lines(f'{c} {R} – {c} {b.X}'):
                        kind = 'same' if r['plane'] == sb['plane'] and num(r['rs']) else \
                               'crossed' if r['plane'] != sb['plane'] and num(r['xs']) else None
                        if kind:
                            A = [x for x in m.groups() if x != R][0]
                            ends = b.sky_y(A) + b.to_natal(A, c)
                            out.append({'key': (c, sb['plane'], s['line'], s['plane'], s['tgt'], r['line'], r['plane']),
                                        'cells': [sb, s, r] + ends, 'notes': [ratio_txt(r, kind)]})
    return out


def bb7(b):
    out = []
    for c in 'HJ':
        for sb in _paired_same_body(b, c):
            for _, R, r in b.star_rows(c):
                if r['plane'] != sb['plane'] or not num(r['rs']):
                    continue
                second = [q for _, R2, q in b.star_rows(c, scoring=True) if R2 != R and b.same_on(q)]
                if second:
                    cells = [sb] + b.same_on(sb) + [r] + [x for q in second for x in [q] + b.same_on(q)]
                    out.append({'key': (c, sb['plane'], R), 'cells': cells, 'notes': [ratio_txt(r, 'same')]})
    return out


def bb8(b):
    out = []
    for c in 'HJ':
        dbl = [(R, r) for _, R, r in b.star_rows(c) if num(r['rs']) and num(r['xs'])]
        if len({R for R, _ in dbl}) >= 2:
            out.append({'key': (c,) + tuple(R for R, _ in dbl), 'cells': [r for _, r in dbl],
                        'notes': [ratio_txt(r, k) for _, r in dbl for k in ('same', 'crossed')]})
    return out


def bb9(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        for s, A0, B0 in b.pairs_on(a):
            if R not in (A0, B0):
                continue
            A = B0 if A0 == R else A0
            h, j = b.to_natal(A, 'H'), b.to_natal(A, 'J')
            if h and j:
                out.append({'key': (a['line'], a['plane'], s['line'], s['plane'], s['tgt']), 'cells': [a, s] + h + j})
    return out


def bb10(b):
    out = []
    for R in ROY:
        sky = b.sky_y(R)
        if not sky:
            continue
        nat = {c: [r for _, R2, r in b.star_rows(c) if R2 == R and (r['fam'] or num(r['rs']) or num(r['xs']))]
               for c in 'HJ'}
        if not (nat['H'] and nat['J']):
            continue
        for c in 'HJ':
            for r in nat[c]:
                if not r['fam']:
                    continue
                for s, A, B in b.pairs_on(r):
                    sa, sbb = b.sky_y(A), b.sky_y(B)
                    if sa and sbb:
                        out.append({'key': (R, r['line'], r['plane'], s['line'], s['plane'], s['tgt']),
                                    'cells': sky + nat['H'] + nat['J'] + [s] + sa + sbb})
    return out


def bb11(b):
    out = []
    for c in 'HJ':
        a_cases, b_cases = [], []
        for p in ('RA', 'Dec'):
            for sb in b.same_body(c, p):
                if sb['fam'] not in ('whole', 'golden'):
                    continue
                for R in ROY:
                    for sk in b.other(f'S {R} – S {b.X}', p):
                        for nt in b.lines(f'{c} {R} – {c} {b.X}', p, scoring=True):
                            if sk['fam'] == nt['fam'] == sb['fam']:
                                ma, ms, mn = mult(sb), mult(sk), mult(nt)
                                if ms in (ma + mn, abs(ma - mn)) or ma in (ms + mn, abs(ms - mn)):
                                    a_cases.append([sk, nt, sb])
        for _, R, r in b.star_rows(c, scoring=True):
            if not b.same_on(r):
                continue
            op = 'Dec' if r['plane'] == 'RA' else 'RA'
            for q in b.lines(r['line'], op):
                if num(q['rs']) and b.same_body(c, op):
                    b_cases.append(([r] + b.same_on(r) + [q] + b.same_body(c, op), ratio_txt(q, 'same')))
        for ac in a_cases:
            for bc, note in b_cases:
                out.append({'key': (c, ac[0]['line'], bc[0]['line']), 'cells': ac + bc, 'notes': [note]})
    return out


def bb12(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        for s, A, B in b.pairs_on(a):
            if b.X not in (A, B):
                continue
            Y = B if A == b.X else A
            nt = b.to_natal(Y, c)
            if nt:
                out.append({'key': (a['line'], a['plane'], s['line'], s['plane'], s['tgt']),
                            'cells': [a, s] + nt + b.to_natal(Y, other_chart(c))})
    return out


def bb13(b):
    got = {}
    for c in 'HJ':
        for sb in b.same_body(c):
            ps = [s for s, A, B in b.pairs_on(sb) if b.X not in (A, B)]
            if ps:
                got.setdefault(c, []).extend([sb] + ps)
    if 'H' in got and 'J' in got:
        return [{'key': ('H+J',), 'cells': got['H'] + got['J']}]
    return []


def bb14(b):
    out = []
    for a in b.lines(f'H {b.X} – J {b.X}', scoring=True):
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                continue
            for c in 'HJ':
                ea, eb = b.to_natal(A, c), b.to_natal(B, c)
                if ea and eb:
                    out.append({'key': (a['plane'], s['line'], s['plane'], s['tgt'], c), 'cells': [a, s] + ea + eb})
    return out


def bb15(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        if a['fam'] == 'conj':
            continue
        pr = [s for s, A, B in b.pairs_on(a) if R in (A, B)]
        if not pr:
            continue
        oc = other_chart(c)
        for o in b.O:
            m = re.match(rf'S (.+) → {oc} {re.escape(b.X)}$', o['line'])
            if m and o['fam'] == a['fam'] and o['tgt'] == a['tgt']:
                back = b.to_natal(m.group(1), c)
                if back:
                    out.append({'key': (a['line'], a['plane'], m.group(1)), 'cells': [a] + pr + [o] + back})
    return out


def bb16(b):
    out = []
    for c in 'HJ':
        for sb in b.same_body(c):
            if sb['fam'] in ('conj', 'contraparallel'):
                continue
            for o in b.O:
                m = re.match(rf'S (.+) → {c} {re.escape(b.X)}$', o['line'])
                if not m or m.group(1) in LIGHTS or o['fam'] != sb['fam'] or o['tgt'] != sb['tgt']:
                    continue
                sky = b.sky_y(m.group(1))
                if sky:
                    out.append({'key': (c, sb['plane'], m.group(1), o['plane']), 'cells': [sb, o] + sky})
    return out


def bb17(b):
    out = []
    for a in b.lines(f'H {b.X} – J {b.X}', scoring=True):
        for o in b.O:
            m = re.match(rf'S (.+) → ([HJ]) {re.escape(b.X)}$', o['line'])
            if not m or m.group(1) in LIGHTS or o['fam'] != a['fam'] or o['tgt'] != a['tgt']:
                continue
            sky = [q for q in b.sky_y(m.group(1)) if q['fam'] == a['fam']]
            if sky:
                out.append({'key': (a['plane'], o['line'], o['plane']), 'cells': [a, o] + sky + b.same_on(a)})
    return out


def bb18(b):
    out = []
    for a in b.lines(f'H {b.X} – J {b.X}', scoring=True):
        for s, A0, B0 in b.pairs_on(a):
            for R in set((A0, B0)) & set(ROY):
                A = B0 if A0 == R else A0
                legs = []
                for p in ('RA', 'Dec'):
                    sk = b.other(f'S {R} – S {b.X}', p)
                    nt = [r for c in 'HJ' for r in b.lines(f'{c} {R} – {c} {b.X}', p, scoring=True)]
                    if sk and nt:
                        legs += sk + nt
                ends = b.sky_y(A) + b.to_natal(A, 'H') + b.to_natal(A, 'J')
                if legs and ends:
                    out.append({'key': (a['plane'], s['line'], s['plane'], s['tgt']),
                                'cells': [a, s] + legs + ends + b.same_on(a)})
    return out


def bb19(b):
    out = []
    for R in ROY:
        sky = b.sky_y(R)
        if not sky:
            continue
        rows = [r for c in 'HJ' for p in ('RA', 'Dec') for r in b.lines(f'{c} {R} – {c} {b.X}', p)]
        if len(rows) == 4 and all(num(r['rs']) for r in rows):
            conj = {o['plane'] for o in sky if o['fam'] == 'conj'}
            notes = [ratio_txt(r, 'same') + (' [likely automatic: S %s – S %s %s conjunction]' % (R, b.X, r['plane'])
                                             if r['plane'] in conj else '') for r in rows]
            out.append({'key': (R,), 'cells': sky + rows, 'notes': notes})
    return out


def bb20(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        good, selfp = [], []
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                selfp.append(s)
                continue
            ends = [x for E in (A, B) for x in b.sky_y(E) + b.to_natal(E, 'H') + b.to_natal(E, 'J')]
            if ends:
                good.append((s, ends))
        if len({s['line'] for s, _ in good}) >= 3 and selfp:
            cells = [a] + selfp + [x for s, e in good for x in [s] + e]
            out.append({'key': (a['line'], a['plane']), 'cells': cells,
                        'notes': [f"{len({s['line'] for s, _ in good})} pairs with an end on {b.X}"]})
    return out


def _bb21_cases(b):
    out = []
    for c in 'HJ':
        for sb in b.same_body(c):
            for s in b.same_on(sb):
                m = re.match(r'S (.+) – S (.+)$', s['line'])
                if not m:
                    continue
                for R in set(m.groups()) & set(ROY):
                    A = [x for x in m.groups() if x != R][0]
                    ends = b.to_natal(A, c)
                    nl = [r for r in b.lines(f'{c} {R} – {c} {b.X}', scoring=True) if b.same_on(r)]
                    if ends and nl:
                        out.append((c, sb, s, ends, nl))
    return out


def bb21(b):
    return [{'key': (c, sb['plane'], s['line'], s['plane'], s['tgt']),
             'cells': [sb, s] + ends + [x for r in nl for x in [r] + b.same_on(r)]}
            for c, sb, s, ends, nl in _bb21_cases(b)]


def bb22(b):
    out = []
    for c, sb, s, ends, nl in _bb21_cases(b):
        matched = [(R, r) for _, R, r in b.star_rows(c, scoring=True) if b.same_on(r)]
        if len({R for R, _ in matched}) >= 2:
            cells = [sb, s] + ends + [x for _, r in matched for x in [r] + b.same_on(r)]
            out.append({'key': (c, sb['plane'], s['line'], s['plane'], s['tgt']), 'cells': cells,
                        'notes': ['royal-star lines matched in this chart: ' + ', '.join(sorted({R for R, _ in matched}))]})
    return out


def bb23(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                continue
            f = s['fam']  # the family the pair sits on (Eddie, 14 Nov 2026), not the anchor's best family
            for E in (A, B):
                nt = [o for o in b.to_natal(E, c) if o['fam'] == f]
                sk = [o for o in b.sky_y(E) if o['fam'] == f]
                if nt and sk:
                    star = [o for o in b.sky_y(R) if o['fam'] == f]
                    notes = ([f'WATCH (b): the same star on sky {b.X} on the same family ({star[0]["tgt"]} {f})']
                             if star else [])
                    out.append({'key': (a['line'], a['plane'], s['line'], s['plane'], s['tgt'], E),
                                'cells': [a, s] + nt + sk + star, 'notes': notes})
    return out


def bb24(b):
    out = []
    for c in 'HJ':
        for sb in b.same_body(c):
            full = {}
            for s, A, B in b.pairs_on(sb):
                if b.X in (A, B):
                    continue
                ends = [b.to_natal(E, 'H') + b.to_natal(E, 'J') for E in (A, B)]
                if all(ends):
                    full.setdefault(frozenset((A, B)), (s, ends[0] + ends[1]))
            if len(full) >= 2:
                cells = [sb] + [x for s, e in full.values() for x in [s] + e]
                out.append({'key': (c, sb['plane']), 'cells': cells,
                            'notes': [f'{len(full)} different pairs, both ends on natal {b.X}']})
    return out


def _points(line):
    """The two points of a line ('S Mars', 'J Mars'); a royal star counts as one point in every chart (it barely moves)."""
    parts = re.split(r' – | → ', line or '')
    pts = set()
    for p in parts:
        w = p.split()
        pts.add(w[-1] if w and w[-1] in ROY else p.strip())
    return pts


def additive_steps(cells):
    """WATCH lines: three cells of the case, same plane (RA / Dec) and family (whole or golden), one multiplier = sum of the other two."""
    rows = [r for r in cells if r and r['fam'] in ('whole', 'golden') and r['plane'] in ('RA', 'Dec')]
    out, seen = [], set()
    for i, a in enumerate(rows):
        for j, b in enumerate(rows):
            if j <= i:
                continue
            for k, c in enumerate(rows):
                if k in (i, j) or not (a['plane'] == b['plane'] == c['plane'] and a['fam'] == b['fam'] == c['fam']):
                    continue
                ma, mb, mc = mult(a), mult(b), mult(c)
                if mc == ma + mb:
                    key = frozenset((i, j, k))
                    if key in seen:
                        continue
                    seen.add(key)
                    u = '×φ' if c['fam'] == 'golden' else ''
                    pts = _points(a['line']) | _points(b['line']) | _points(c['line'])
                    geo = ' (may be geometry: three distances between the same three points)' if len(pts) == 3 else ''
                    out.append(f"WATCH additive step ({c['plane']}): {mc}{u} = {ma}{u} + {mb}{u} "
                               f"({c['line']}; {a['line']}; {b['line']}){geo}")
    return out


def bb25(b):
    out = []
    for c in 'HJ':
        for p in ('RA', 'Dec'):
            for sb in b.same_body(c, p):
                if sb['fam'] not in ('whole', 'golden'):
                    continue
                for R in ROY:
                    for sk in b.other(f'S {R} – S {b.X}', p):
                        for nt in b.lines(f'{c} {R} – {c} {b.X}', p, scoring=True):
                            if not (sk['fam'] == nt['fam'] == sb['fam']):
                                continue
                            ma, ms, mn = mult(sb), mult(sk), mult(nt)
                            if not (ms in (ma + mn, abs(ma - mn)) or ma in (ms + mn, abs(ms - mn)) or mn == ma + ms):
                                continue
                            pr = [(s, A, B) for s, A, B in b.pairs_on(sb) if b.X not in (A, B)]
                            ends = [o for s, A, B in pr for E in (A, B) for o in b.sky_y(E)]
                            if pr and ends:
                                out.append({'key': (c, p, R), 'cells': [sk, nt, sb] + [s for s, _, _ in pr] + ends})
    return out


def bb26(b):
    out = []
    for c in 'HJ':
        uni = {}
        for _, R, r in b.star_rows(c):
            for kind, t, sc in (('same', r['rt'], r['rs']), ('crossed', r['xt'], r['xs'])):
                if num(sc) and str(t).startswith('1 unison'):
                    uni.setdefault(R, []).append((r, kind))
        uni = {R: v for R, v in uni.items() if b.sky_y(R)}
        if len(uni) >= 2:
            cells, notes = [], []
            for R, v in sorted(uni.items()):
                sky = b.sky_y(R)
                conj = {o['plane'] for o in sky if o['fam'] == 'conj'}
                cells += sky
                for r, kind in v:
                    cells.append(r)
                    pl = r['plane'] if kind == 'same' else ('Dec' if r['plane'] == 'RA' else 'RA')
                    auto = (f' [likely automatic: S {R} – S {b.X} {r["plane"]} conjunction]'
                            if kind == 'same' and r['plane'] in conj else '')
                    notes.append(ratio_txt(r, kind) + auto)
            out.append({'key': (c,) + tuple(sorted(uni)), 'cells': cells, 'notes': notes})
    return out


def bb27(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        prs = b.pairs_on(a)
        selfp = [s for s, A, B in prs if b.X in (A, B)]
        if not selfp:
            continue
        for s, A, B in prs:
            if b.X in (A, B):
                continue
            r2 = (set((A, B)) & set(ROY)) - {R}
            if not r2:
                continue
            R2 = r2.pop()
            E = B if A == R2 else A
            sky = b.sky_y(E)
            if sky:
                notes = ([f'WATCH (b): {E} in conjunction with sky {b.X}'] if any(o['fam'] == 'conj' for o in sky) else [])
                out.append({'key': (a['line'], a['plane'], s['line'], s['plane'], s['tgt']),
                            'cells': [a] + selfp + [s] + sky, 'notes': notes})
    return out


def bb28(b):
    out = []
    for c, R, a in b.star_rows(scoring=True):
        sky = b.other(f'S {R} – S {b.X}', a['plane'])
        if not sky:
            continue
        fams = {o['fam'] for o in sky}
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                continue
            for E in (A, B):
                ends = [o for o in b.to_natal(E, c) if o['fam'] in fams]
                if ends:
                    out.append({'key': (a['line'], a['plane'], s['line'], s['plane'], s['tgt'], E),
                                'cells': sky + [a, s] + ends})
    return out


def bb29(b):
    out = []
    for c in 'HJ':
        byY = {}
        for _, R, a in b.star_rows(c, scoring=True):
            for s, A, B in b.pairs_on(a):
                if R in (A, B):
                    Y = B if A == R else A
                    if Y != b.X:
                        byY.setdefault(Y, []).append((R, a, s))
        for Y, hits in byY.items():
            if len({R for R, _, _ in hits}) < 2:
                continue
            nat, sky = b.to_natal(Y, c), b.sky_y(Y)
            if nat and sky:
                cells = [x for _, a, s in hits for x in (a, s)] + nat + sky + b.to_natal(Y, other_chart(c))
                out.append({'key': (c, Y), 'cells': cells,
                            'notes': [f"{Y} paired with {', '.join(sorted({R for R, _, _ in hits}))} on their own natal lines"]})
    return out


def bb30(b):
    out = []
    for a in b.lines(f'H {b.X} – J {b.X}', scoring=True):
        full, light = {}, {}
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                continue
            ends = [b.sky_y(E) + b.to_natal(E, 'H') + b.to_natal(E, 'J') for E in (A, B)]
            if all(ends):
                (light if 'Moon' in (A, B) else full).setdefault(frozenset((A, B)), (s, ends[0] + ends[1]))
        cells = lambda d: [a] + [x for s, e in d.values() for x in [s] + e]
        if len(full) >= 2:
            notes = [f'{len(full)} pairs, every end on {b.X}']
            if light:
                notes.append('WATCH Moon pairs also on the number: ' + '; '.join(s['line'] for s, _ in light.values()))
            out.append({'key': (a['plane'],), 'cells': cells(full) + cells(light)[1:], 'notes': notes})
        elif len(full) + len(light) >= 2:
            out.append({'key': (a['plane'], 'watch'), 'cells': cells({**full, **light}), 'watch_only': True,
                        'notes': ['WATCH (Moon as an end): holds only when a Moon pair counts; not a holder']})
    return out


def bb31(b):
    out = []
    for c in 'HJ':
        for sb in b.same_body(c):
            prs = b.pairs_on(sb)
            tri = [(s, E) for s, A, B in prs if b.X not in (A, B) for E in (A, B)
                   if b.sky_y(E) and b.to_natal(E, 'H') and b.to_natal(E, 'J')]
            if not tri:
                continue
            selfp = [(s, [p for p in (A, B) if p != b.X][0]) for s, A, B in prs if b.X in (A, B)]
            good = [(s, Y) for s, Y in selfp if b.to_natal(Y, 'H') + b.to_natal(Y, 'J')]
            if not good:
                continue
            real = [(s, Y) for s, Y in good if Y != 'Moon']
            cells = [sb] + [x for s, E in tri for x in [s] + b.sky_y(E) + b.to_natal(E, 'H') + b.to_natal(E, 'J')]
            cells += [x for s, Y in good for x in [s] + b.to_natal(Y, 'H') + b.to_natal(Y, 'J')]
            cells += [o for o in b.O if o['line'].startswith('S ') and '→' in o['line'] and o['fam'] == sb['fam']
                      and o['tgt'] == sb['tgt'] and o['line'] != sb['line']]
            case = {'key': (c, sb['plane']), 'cells': cells}
            if not real:
                case['watch_only'] = True
                case['notes'] = ['WATCH (Moon): holds only through the Moon pair; not a holder']
            out.append(case)
    return out


CJ = ('conj', 'contraparallel')


def _cj_sky(b, E):
    """E in conjunction or contraparallel with sky X (S E – S X rows)."""
    return [o for o in b.sky_y(E) if o['fam'] in CJ]


def _bb32_cases(b):
    """(star line, S E -> c X row, E, its conj / contraparallel rows on sky X)."""
    out = []
    for c, R, a in b.star_rows(scoring=True):
        for s in b.same_on(a):
            m = re.match(rf'S (\w+) → {c} {re.escape(b.X)}$', s['line'])
            if m and m.group(1) not in ('Moon', b.X):
                t = _cj_sky(b, m.group(1))
                if t:
                    out.append((c, R, a, s, m.group(1), t))
    return out


def bb32(b):
    out = []
    for c, R, a, s, E, t in _bb32_cases(b):
        notes = [f'S {E} on sky {b.X} by ' + ', '.join(o['plane'] if o['fam'] in o['plane'] else f"{o['plane']} {o['fam']}" for o in t),
                 f"gap |star line - S {E} line| {abs(a['v'] - s['v']):.4f}"]
        out.append({'key': (c, R, a['plane'], E, s['plane']), 'cells': [a, s] + t, 'notes': notes})
    return out


def bb32b(b):
    out = []
    for c, R, a, s, E, t in _bb32_cases(b):
        for c2, R2, a2 in b.star_rows(scoring=True):
            if R2 == R:
                continue
            for s2, A, B in b.pairs_on(a2):
                if E not in (A, B) or b.X in (A, B):
                    continue
                O = B if A == E else A
                t2 = _cj_sky(b, O)
                if O == 'Moon' or not t2:
                    continue
                notes = [f'S {E} on sky {b.X} carries {c} {R} (number) and {c2} {R2} (pair S {A} – S {B})']
                if len({o['plane'] for o in t}) == 2:
                    notes.append(f'WATCH: S {E} on sky {b.X} in both planes')
                notes.append(f"WATCH gap |star line - S {E} line| {abs(a['v'] - s['v']):.4f}")
                cj_any = lambda e: [o for o in b.sky_y(e) + b.to_natal(e, 'H') + b.to_natal(e, 'J') if o['fam'] in CJ]
                third = [(c3, R3, a3, s3) for c3, R3, a3 in b.star_rows(scoring=True) if R3 not in (R, R2)
                         for s3, P, Q in b.pairs_on(a3) if b.X not in (P, Q) and 'Moon' not in (P, Q)
                         and cj_any(P) and cj_any(Q)]
                for c3, R3, a3, s3 in third:
                    P, Q = re.match(r'S (.+) – S (.+)$', s3['line']).groups()
                    how = '; '.join(f"{o['line']} {o['plane']} {o['v']:.6f}" for e in (P, Q) for o in cj_any(e))
                    notes.append(f"WATCH third royal star: {a3['line']} {a3['plane']} paired by {s3['line']} "
                                 f"{s3['plane']}, both ends conj / contraparallel {b.X} ({how})")
                out.append({'key': (c, R, a['plane'], E, c2, R2, a2['plane']),
                            'cells': [a, s] + t + [a2, s2] + t2 + [x for _, _, a3, s3 in third for x in (a3, s3)],
                            'notes': notes})
    return out


def bb33(b):
    out = []
    conjR = {R: [o for o in b.sky_y(R) if o['fam'] in CJ] for R in ROY}
    conjR = {R: v for R, v in conjR.items() if v}
    for c in 'HJ':
        for sb in b.same_body(c):
            for s, P, Q in b.pairs_on(sb):
                for R, Y in ((P, Q), (Q, P)):
                    if R not in conjR or Y in (b.X, 'Moon', R) or Y in ROY:
                        continue
                    yn = b.to_natal(Y, 'H') + b.to_natal(Y, 'J')
                    if not yn:
                        continue
                    notes = [f"S {R} on sky {b.X} ({', '.join(o['plane'] + ' ' + str(round(o['v'], 4)) for o in conjR[R])}); "
                             f"pair S {Y} – S {R} on {sb['line']} {sb['plane']}; S {Y} on natal {b.X}"]
                    auto = []
                    for cc in 'HJ':
                        for r in b.lines(f'{cc} {R} – {cc} {b.X}'):
                            if r.get('r') and str(r.get('rt') or '').startswith('1 '):
                                auto.append(f"{cc} {r['plane']} {r['r']:.4f}")
                    if auto:
                        notes.append(f'WATCH likely automatic ({R} conj sky {b.X}): same-body unisons ' + ', '.join(auto))
                    other = [(c2, sb2, s2) for c2 in 'HJ' if c2 != c for sb2 in b.same_body(c2)
                             for s2, A2, B2 in b.pairs_on(sb2) if b.X not in (A2, B2)]
                    if other:
                        notes.append('WATCH other chart same-body line also paired: ' + '; '.join(
                            f"{sb2['line']} {sb2['plane']} by {s2['line']} {s2['plane']}" for _, sb2, s2 in other))
                    out.append({'key': (c, sb['plane'], R, Y, s['plane']),
                                'cells': [sb, s] + conjR[R] + yn + [x for _, sb2, s2 in other for x in (sb2, s2)],
                                'notes': notes})
    return out


def bb34(b):
    out = []
    planes = lambda e: {o['plane'].split()[0] for o in b.sky_y(e)}
    for c, R, a in b.star_rows(scoring=True):
        for s, P, Q in b.pairs_on(a):
            if b.X in (P, Q) or 'Moon' in (P, Q):
                continue
            if not all(planes(e) for e in (P, Q)):
                continue
            nat = {e: b.to_natal(e, 'H') + b.to_natal(e, 'J') for e in (P, Q)}
            if not all(nat.values()):
                continue
            notes = [f"S {P} on sky {b.X} ({'/'.join(sorted(planes(P)))}), S {Q} on sky {b.X} ({'/'.join(sorted(planes(Q)))}); "
                     f'both on natal {b.X}']
            if all(planes(e) >= {'RA', 'Dec'} for e in (P, Q)):
                notes.append(f'WATCH (tight version): both ends on sky {b.X} in RA and Dec')
            if 'Sedna' in (P, Q):
                notes.append(f'WATCH Sedna is an end of the pair (S {P} – S {Q})')
            other = [(a2, s2) for a2 in b.lines(f'{c} {R} – {c} {b.X}', scoring=True) if a2['plane'] != a['plane']
                     for s2 in b.same_on(a2)]
            if other:
                notes.append(f"WATCH {a['line']} also paired in the other plane: " + '; '.join(
                    f"{s2['line']} {s2['plane']}" + (' (Moon)' if 'Moon' in s2['line'] else '') for _, s2 in other))
            cells = [a, s] + b.sky_y(P) + b.sky_y(Q) + nat[P] + nat[Q] + [x for a2, s2 in other for x in (a2, s2)]
            out.append({'key': (c, R, a['plane'], frozenset((P, Q))), 'cells': cells, 'notes': notes})
    return out


def bb35(b):
    out = []
    onsky = {R: b.sky_y(R) for R in ROY if b.sky_y(R)}
    for c in 'HJ':
        cx = {}
        for R in onsky:
            for r in b.lines(f'{c} {R} – {c} {b.X}'):
                if r.get('xs'):
                    cx.setdefault((R, r['plane']), []).append(r)
        for pl in ('RA', 'Dec'):
            stars = sorted({R for R, p in cx if p == pl})
            for i in range(len(stars)):
                for j in range(i + 1, len(stars)):
                    R1, R2 = stars[i], stars[j]
                    rows = cx[(R1, pl)] + cx[(R2, pl)]
                    notes = [f"{c} {R1} and {c} {R2} – {b.X} {pl}: crossed same-body ratios "
                             + '; '.join(f"{r['xt']} ({r['xs']})" for r in rows) + f"; both stars on sky {b.X}"]
                    if any((r.get('xs') or 0) >= 80 for r in rows):
                        notes.append('WATCH a crossed ratio scores >= 80')
                    out.append({'key': (c, pl, R1, R2), 'cells': rows + onsky[R1] + onsky[R2], 'notes': notes})
    return out


def bb36(b):
    """BB6 + the ratio on a cut + R's natal line scores + a second royal star on sky X."""
    out = []
    for c in 'HJ':
        for sb in b.same_body(c):
            for s in b.same_on(sb):
                m = re.match(r'S (.+) – S (.+)$', s['line'])
                if not m:
                    continue
                for R in set(m.groups()) & set(ROY):
                    for r in b.lines(f'{c} {R} – {c} {b.X}', scoring=True):
                        kind = 'same' if r['plane'] == sb['plane'] and num(r['rs']) else \
                               'crossed' if r['plane'] != sb['plane'] and num(r['xs']) else None
                        if not kind or 'cut' not in str(r['rt'] if kind == 'same' else r['xt']):
                            continue
                        R2 = [o for q in ROY if q != R for o in b.sky_y(q)]
                        if not R2:
                            continue
                        notes = [ratio_txt(r, kind)]
                        if b.sky_y(R):
                            notes.append(f'WATCH {R} itself on sky {b.X}: ' + '; '.join(cell(o) for o in b.sky_y(R)))
                        extra = []
                        for s2 in b.same_on(sb):
                            m2 = re.match(r'S (.+) – S (.+)$', s2['line'])
                            if not m2 or s2['line'] == s['line']:
                                continue
                            for e in m2.groups():
                                if e in ROY or e == 'Moon' or e == b.X:
                                    continue
                                nt = b.to_natal(e, 'H') + b.to_natal(e, 'J')
                                if b.sky_y(e) and nt:
                                    extra += [s2] + b.sky_y(e) + nt
                                    notes.append(f"WATCH second pair {s2['line']} {s2['plane']} on the same-body line, end {e} "
                                                 f"on sky {b.X} and natal {b.X}: " + '; '.join(cell(o) for o in b.sky_y(e) + nt))
                        out.append({'key': (c, sb['plane'], s['line'], s['plane'], s['tgt'], r['line'], r['plane']),
                                    'cells': [sb, s, r] + R2, 'notes': notes})
    return out


def bb37(b):
    """Same-body line paired by S X – S Y, Y conj natal X (same chart), and the Sun conj / contraparallel sky X."""
    out = []
    sun = [o for o in b.sky_y('Sun') if o['fam'] in CJ]
    if not sun:
        return out
    for c in 'HJ':
        for sb in b.same_body(c, scoring=False):
            for s in b.same_on(sb):
                m = re.match(r'S (.+) – S (.+)$', s['line'])
                if not m or b.X not in m.groups():
                    continue
                Y = [g for g in m.groups() if g != b.X][0]
                if Y == 'Moon':
                    continue
                cj = [o for o in b.to_natal(Y, c) if o['fam'] == 'conj']
                if not cj:
                    continue
                notes = [f"S {Y} on natal {c} {b.X} ({'; '.join(cell(o) for o in cj)}): the pair S {b.X} – S {Y} repeats "
                         f"S {b.X} → {c} {b.X} (may be geometry)",
                         'Sun on sky ' + b.X + ': ' + '; '.join(cell(o) for o in sun)]
                oth = [o for o in b.O if re.match(rf'S (.+) – S {re.escape(b.X)}$', o['line']) and o['fam'] in CJ
                       and not o['line'].startswith(('S Sun ', 'S Moon '))]
                if oth:
                    notes.append(f'WATCH another body conj / contraparallel sky {b.X}: ' + '; '.join(cell(o) for o in oth))
                if (s['sc'] or 0) >= 80:
                    notes.append(f"WATCH the pair scores >= 80 ({s['sc']})")
                out.append({'key': (c, sb['plane'], s['line'], s['plane'], s['tgt']),
                            'cells': [sb, s] + cj + sun, 'notes': notes})
    return out


def bb38(b):
    """A royal star on sky X; its natal line on X has a crossed same-body ratio >= 80 in the horse chart and in the jockey chart."""
    out = []
    for R in ROY:
        sk = b.sky_y(R)
        if not sk:
            continue
        side = {c: [r for r in b.lines(f'{c} {R} – {c} {b.X}') if num(r['xs']) and r['xs'] >= 80] for c in 'HJ'}
        if not (side['H'] and side['J']):
            continue
        rows = side['H'] + side['J']
        notes = [f"{r['line']} {r['plane']}: " + ratio_txt(r, 'crossed') for r in rows]
        if any(o['fam'] in ('opposition', 'conj') for o in sk):
            notes.append(f'WATCH {R} opposition / conj sky {b.X}')
        if any((o['sc'] or 0) >= 80 for o in sk):
            notes.append(f'WATCH the sky line S {R} – S {b.X} scores >= 80')
        nat = [r for c in 'HJ' for r in b.lines(f'{c} {R} – {c} {b.X}') if r['fam'] and (r['sc'] or 0) >= 90]
        if nat:
            notes.append('WATCH a natal star line scores >= 90: ' + '; '.join(cell(r) for r in nat))
        r2 = [o for q in ROY if q != R for o in b.sky_y(q)]
        if r2:
            notes.append(f'WATCH another royal star on sky {b.X}: ' + '; '.join(cell(o) for o in r2))
        out.append({'key': (R,), 'cells': sk + rows + nat, 'notes': notes})
    return out


def bb39(b):
    """BB13 (same-body line paired in both charts) + the Sun conj / contraparallel natal X."""
    base = bb13(b)
    if not base:
        return []
    sun = [o for c in 'HJ' for o in b.to_natal('Sun', c) if o['fam'] in CJ]
    if not sun:
        return []
    P = {c: [(sb, s, {A, B}) for sb in b.same_body(c) for s, A, B in b.pairs_on(sb) if b.X not in (A, B)] for c in 'HJ'}
    notes = ['Sun on natal ' + b.X + ': ' + '; '.join(cell(o) for o in sun)]
    ends = {c: set().union(*[g for _, _, g in P[c]]) - {'Moon'} for c in 'HJ'}
    both = sorted((ends['H'] & ends['J']) - set(ROY))
    if both:
        notes.append('WATCH a body in a pair on both charts\' lines: ' + ', '.join(both))
    ec = [o for c in 'HJ' for Y in sorted(ends[c] - set(ROY)) for o in b.sky_y(Y) if o['fam'] in CJ]
    if ec:
        notes.append(f'WATCH a pair end conj / contraparallel sky {b.X}: ' + '; '.join(cell(o) for o in ec))
    rr = []
    for c in 'HJ':
        for _, s, g in P[c]:
            for R in sorted(g & set(ROY)):
                nat = [r for r in b.lines(f'{c} {R} – {c} {b.X}') if r['fam'] and (r['sc'] or 0) >= 90]
                if b.sky_y(R) and nat:
                    rr.append(f"{s['line']} {s['plane']} with {R} on sky {b.X} and " + '; '.join(cell(r) for r in nat))
    if rr:
        notes.append('WATCH a royal pair, the star on sky X and its natal line >= 90: ' + ' | '.join(rr))
    for c in 'HJ':
        for sb in b.same_body(c):
            n = sum(1 for x in P[c] if x[0] is sb)
            if n >= 3:
                notes.append(f"WATCH {n} pairs on {sb['line']} {sb['plane']}")
    return [{'key': base[0]['key'], 'cells': base[0]['cells'] + sun, 'notes': notes}]


def bb40(b):
    """A sky pair on a same-body line: one end on sky X, the other on natal X in the other chart; the Sun on that natal X
    on the same target as the end's line or the pair (the Sun not a pair end)."""
    out = []
    for c in 'HJ':
        oc = other_chart(c)
        for sb in b.same_body(c):
            for s, A, B in b.pairs_on(sb):
                if b.X in (A, B) or 'Moon' in (A, B) or 'Sun' in (A, B):
                    continue
                for a, e in ((A, B), (B, A)):
                    sky, nat = b.sky_y(a), b.to_natal(e, oc)
                    if not sky or not nat:
                        continue
                    tg = {(n['fam'], n['tgt']) for n in nat} | {(s['fam'], s['tgt'])}
                    sun = [o for o in b.to_natal('Sun', oc) if (o['fam'], o['tgt']) in tg]
                    if not sun:
                        continue
                    notes = [f'{a} on sky {b.X}, {e} on {oc} {b.X}; Sun on ' +
                             ' and '.join(w for w, ok in (("the end's line", any((o['fam'], o['tgt']) in {(n['fam'], n['tgt']) for n in nat} for o in sun)),
                                                          ('the pair', any((o['fam'], o['tgt']) == (s['fam'], s['tgt']) for o in sun))) if ok)]
                    roy = [o for q in ROY for o in b.sky_y(q)]
                    if len({o['line'] for o in roy}) >= 2:
                        notes.append(f'WATCH two or more royal stars on sky {b.X}: ' + '; '.join(cell(o) for o in roy))
                    cut = [r for _, _, r in b.star_rows() if 'cut' in str(r.get('rt')) or 'cut' in str(r.get('xt'))]
                    for r in cut:
                        k = 'same' if 'cut' in str(r.get('rt')) else 'crossed'
                        notes.append(f'WATCH a royal natal line with a ratio on a cut: {cell(r)} ' + ratio_txt(r, k))
                    out.append({'key': (c, sb['plane'], s['line'], s['plane'], s['tgt'], a, e),
                                'cells': [sb, s] + sky + nat + sun, 'notes': notes})
    return out


def bb41(b):
    """A royal-star line on X closed by a sky pair in BOTH charts (one end on sky X, the other on natal X in the line's own chart),
    and the Moon on sky X and on both natal X."""
    moon = (b.sky_y('Moon'), b.to_natal('Moon', 'H'), b.to_natal('Moon', 'J'))
    if not all(moon):
        return []
    loops = {'H': [], 'J': []}
    for c, R, r in b.star_rows(scoring=True):
        for s, A, B in b.pairs_on(r):
            if b.X in (A, B) or 'Moon' in (A, B):
                continue
            for a, e in ((A, B), (B, A)):
                sky, nat = b.sky_y(a), b.to_natal(e, c)
                if sky and nat:
                    loops[c].append((R, r, s, a, e, sky, nat))
    if not (loops['H'] and loops['J']):
        return []
    cells, notes, seen = [], [], set()
    for c in 'HJ':
        for R, r, s, a, e, sky, nat in loops[c]:
            k = (r['line'], r['plane'], s['line'], s['plane'], a)
            if k in seen:
                continue
            seen.add(k)
            cells += [r, s] + sky + nat
            notes.append(f"{c} {R} line closed by {s['line']} {s['plane']}: {a} on sky {b.X}, {e} on {c} {b.X}")
            if a in ROY or e in ROY:
                notes.append(f"WATCH a royal star is a pair end ({s['line']} {s['plane']})")
            if r['fam'] in CJ:
                notes.append(f"WATCH the royal line is a {r['fam']} ({r['line']} {r['plane']})")
    cells += [o for m in moon for o in m]
    notes.append(f'Moon on sky {b.X}, H {b.X} and J {b.X}: ' + '; '.join(cell(o) for m in moon for o in m))
    hj = [r for r in b.L if r['line'] == f'H {b.X} – J {b.X}' and r['fam']]
    if hj:
        notes.append(f'WATCH H {b.X} – J {b.X} scores: ' + '; '.join(cell(r) for r in hj))
    return [{'key': ('BB41', b.X), 'cells': cells, 'notes': notes}]


def bb42(b):
    """A sky body on both natal X in both planes (not the Sun or the Moon; no conj / contraparallel lines), and a sky body
    (not the Sun) on sky X and on both natal X."""
    def ys(pat):
        return {re.match(pat, o['line']).group(1) for o in b.O if re.match(pat, o['line'] or '')}
    four = []
    for Y in sorted(ys(rf'S (.+) → [HJ] {re.escape(b.X)}$') - {b.X, 'Sun', 'Moon'}):
        lines = [o for c in 'HJ' for o in b.to_natal(Y, c) if o['fam'] not in CJ]
        got = {(c, o['plane']) for c in 'HJ' for o in b.to_natal(Y, c) if o['fam'] not in CJ}
        if {('H', 'RA'), ('H', 'Dec'), ('J', 'RA'), ('J', 'Dec')} <= got:
            four.append((Y, lines))
    three = []
    for Y in sorted(ys(rf'S (.+) – S {re.escape(b.X)}$') - {b.X, 'Sun'}):
        sky, h, j = b.sky_y(Y), b.to_natal(Y, 'H'), b.to_natal(Y, 'J')
        if sky and h and j:
            three.append((Y, sky + h + j))
    if not (four and three):
        return []
    cells, notes = [], []
    for Y, lines in four:
        cells += lines
        notes.append(f'{Y} on H {b.X} and J {b.X} in RA and Dec ({len(lines)} lines)')
    for Y, lines in three:
        cells += [o for o in lines if o not in cells]
        notes.append(f'{Y} on sky {b.X}, H {b.X} and J {b.X}')
        cj = [o for o in lines if o['fam'] in CJ]
        if cj:
            notes.append(f'WATCH {Y}: ' + '; '.join(f"{o['line']} {o['plane']} is a {o['fam']}" for o in cj))
        if Y == 'Moon':
            notes.append('WATCH the sky-X body is the Moon')
    if {Y for Y, _ in four} & {Y for Y, _ in three}:
        notes.append('the same body does both (' + ', '.join(sorted({Y for Y, _ in four} & {Y for Y, _ in three})) + ')')
    return [{'key': ('BB42', b.X), 'cells': cells, 'notes': notes}]


def bb43(b):
    """A same-body line S X -> H X / J X (no conj / contraparallel) with a sky pair S A - S B on its target (not naming X or the Moon):
    one end on sky X (S A - S X) and the other on BOTH natal X (S B -> H X and S B -> J X); any plane, any score."""
    loops, seen = [], set()
    for c in 'HJ':
        for r in b.same_body(c):
            if r['fam'] in CJ:
                continue
            for s, A, B in b.pairs_on(r):
                if b.X in (A, B) or 'Moon' in (A, B):
                    continue
                for a, e in ((A, B), (B, A)):
                    sky, h, j = b.sky_y(a), b.to_natal(e, 'H'), b.to_natal(e, 'J')
                    k = (r['line'], r['plane'], s['line'], s['plane'], a)
                    if sky and h and j and k not in seen:
                        seen.add(k)
                        loops.append((r, s, a, e, sky, h + j))
    if not loops:
        return []
    cells, notes = [], []
    for r, s, a, e, sky, nat in loops:
        cells += [o for o in [r, s] + sky + nat if o not in cells]
        notes.append(f"{r['line']} {r['plane']} closed by {s['line']} {s['plane']}: {a} on sky {b.X}, {e} on H {b.X} and J {b.X}")
        if a in ROY or e in ROY:
            notes.append(f"WATCH a royal star is a pair end ({s['line']} {s['plane']})")
        cj = [o for o in sky + nat if o['fam'] in CJ]
        if cj:
            notes.append('WATCH an end line is a conj / contraparallel: ' + '; '.join(f"{o['line']} {o['plane']}" for o in cj))
    rr = {}
    for c, R, r in b.star_rows():
        if r.get('rs') is not None:
            rr.setdefault(R, []).append((c, r))
    for R, lst in rr.items():
        if {c for c, _ in lst} == {'H', 'J'}:
            notes.append(f'WATCH {R} has a same-body ratio on a target in both charts: ' +
                         '; '.join(f"{r['line']} {r['plane']} {ratio_txt(r, 'same')}" for c, r in lst))
    return [{'key': ('BB43', b.X), 'cells': cells, 'notes': notes}]


def bb44(b):
    """A natal royal-star line c R - c X (no conj / contraparallel) with a sky line S Y - S X on its target in the same plane (Y a sky
    body, not a royal star, the Sun or the Moon); Y is also on sky X in the other plane (no conj / cp) and on natal X in chart c."""
    out = []
    for c, R, r in b.star_rows(scoring=True):
        if r['fam'] in CJ:
            continue
        for s in b.same_on(r):
            m = re.match(rf'S (.+) – S {re.escape(b.X)}$', s['line'] or '')
            if not m or s['plane'] != r['plane']:
                continue
            Y = m.group(1)
            if Y in ROY or Y in ('Sun', 'Moon') or Y == b.X:
                continue
            oth = [o for o in b.sky_y(Y) if o['plane'] != r['plane'] and o['fam'] not in CJ]
            nat = b.to_natal(Y, c)
            if oth and nat:
                out.append((c, R, r, Y, s, oth, nat))
    if not out:
        return []
    cells, notes = [], []
    for c, R, r, Y, s, oth, nat in out:
        cells += [o for o in [r, s] + oth + nat if o not in cells]
        notes.append(f"{r['line']} {r['plane']} carried by {s['line']} {s['plane']}; {Y} also on sky {b.X} "
                     f"{', '.join(o['plane'] for o in oth)} and on {c} {b.X}")
        if any(o['fam'] == r['fam'] for o in oth):
            notes.append(f"{Y}'s other-plane line is the same family as the royal line ({r['fam']})")
        rs = [o for o in b.sky_y(R)]
        if rs:
            notes.append(f'WATCH {R} is also on sky {b.X}: ' + '; '.join(cell(o) for o in rs))
    return [{'key': ('BB44', b.X), 'cells': cells, 'notes': notes}]


def _bb45_cases(b):
    """Same-body line S X -> c X (no conj / cp) with S Y -> the other chart's X on its target (Y not X, the Sun or the Moon), and Y on
    natal X in chart c in both planes (no conj / cp)."""
    out = []
    for c in 'HJ':
        oc = other_chart(c)
        for r in b.same_body(c):
            if r['fam'] in CJ:
                continue
            for s in b.same_on(r):
                m = re.match(rf'S (.+) → {oc} {re.escape(b.X)}$', s['line'] or '')
                if not m or m.group(1) in (b.X, 'Sun', 'Moon'):
                    continue
                Y = m.group(1)
                nat = [o for o in b.to_natal(Y, c) if o['fam'] not in CJ]
                if {o['plane'] for o in nat} >= {'RA', 'Dec'}:
                    out.append((c, oc, r, Y, s, nat))
    return out


def _bb45_build(b, rid, cases, royal):
    cells, notes = [], []
    for c, oc, r, Y, s, nat in cases:
        cells += [o for o in [r, s] + nat if o not in cells]
        notes.append(f"{r['line']} {r['plane']} on {r['tgt']} carried in the other chart by {s['line']} {s['plane']}; {Y} also on "
                     f"{c} {b.X} in RA and Dec")
        sky = b.sky_y(Y)
        if sky:
            notes.append(f'{Y} is also on sky {b.X}: ' + '; '.join(cell(o) for o in sky))
    for o in royal:
        if o not in cells:
            cells.append(o)
    if royal:
        notes.append(f'royal star on sky {b.X}: ' + '; '.join(cell(o) for o in royal))
    return [{'key': (rid, b.X), 'cells': cells, 'notes': notes}]


def bb45(b):
    """A same-body line carried in the other chart by a sky body Y on the same target; Y also on the same-body chart's X in RA and Dec."""
    cases = _bb45_cases(b)
    return _bb45_build(b, 'BB45', cases, []) if cases else []


def bb46(b):
    """BB45 and a royal star on sky X (S R – S X, any plane, any score)."""
    cases = _bb45_cases(b)
    royal = [o for R in ROY for o in b.sky_y(R)]
    return _bb45_build(b, 'BB46', cases, royal) if cases and royal else []


def bb47(b):
    """A natal royal-star line c R - c X (no conj / contraparallel) carrying on its target: a sky pair S A - S B (not naming X or the
    Moon) with one end on sky X (S A - S X) and the other on natal X in chart c (S B -> c X); a pair S C - S D on the target (the same
    pair or another; Eddie, 15 Nov 2026) with both ends on natal X in chart c; and a sky line naming X (S X - S Y or S Y - S X). End
    lines no conj / cp; any plane, any score."""
    ok = lambda rs: [o for o in rs if o['fam'] and o['fam'] not in CJ]
    xs = re.escape(b.X)
    out = []
    for c, R, r in b.star_rows(scoring=True):
        if r['fam'] in CJ:
            continue
        prs = [(s, A, B) for s, A, B in b.pairs_on(r) if b.X not in (A, B) and 'Moon' not in (A, B)]
        split, both = [], []
        for s, A, B in prs:
            for P, Q in ((A, B), (B, A)):
                sk, nt = ok(b.sky_y(P)), ok(b.to_natal(Q, c))
                if sk and nt:
                    split.append((s, P, Q, sk, nt))
            na, nb = ok(b.to_natal(A, c)), ok(b.to_natal(B, c))
            if na and nb:
                both.append((s, A, B, na + nb))
        xl = [s for s in b.same_on(r) if re.match(rf'S {xs} – S |S .+ – S {xs}$', s['line'] or '')]
        if not xl:
            continue
        for s1, P, Q, sk, nt in split:
            for s2, A, B, nn in both:
                out.append((c, R, r, s1, P, Q, sk, nt, s2, A, B, nn, xl))
    if not out:
        return []
    cells, notes = [], []
    for c, R, r, s1, P, Q, sk, nt, s2, A, B, nn, xl in out:
        for o in [r, s1] + sk + nt + [s2] + nn + xl:
            if o not in cells:
                cells.append(o)
        notes.append(f"{r['line']} {r['plane']}: {s1['line']} {s1['plane']} ({P} on sky {b.X}, {Q} on {c} {b.X}); "
                     f"{s2['line']} {s2['plane']} ({A} and {B} on {c} {b.X}"
                     + ('; the same pair' if s2 is s1 else '') + '); '
                     + '; '.join(f"{x['line']} {x['plane']}" for x in xl))
    return [{'key': ('BB47', b.X), 'cells': cells, 'notes': notes}]


def bb48(b):
    """A natal royal-star line c R - c X (no conj / contraparallel) with a sky pair S A - S B on its target (not naming X or the Moon)
    whose two ends are both on sky X (S A - S X and S B - S X) and one of them on natal X in chart c (S A / S B -> c X); and an end of a
    pair on the target (the same pair or another; Eddie, 15 Nov 2026) on natal X in the other chart. End lines no conj / cp; any plane,
    any score."""
    ok = lambda rs: [o for o in rs if o['fam'] and o['fam'] not in CJ]
    out = []
    for c, R, r in b.star_rows(scoring=True):
        if r['fam'] in CJ:
            continue
        oc = other_chart(c)
        prs = [(s, A, B) for s, A, B in b.pairs_on(r) if b.X not in (A, B) and 'Moon' not in (A, B)]
        far = [(s, E, ok(b.to_natal(E, oc))) for s, A, B in prs for E in (A, B)]
        far = [f for f in far if f[2]]
        if not far:
            continue
        for s, A, B in prs:
            sa, sb_ = ok(b.sky_y(A)), ok(b.sky_y(B))
            na, nb = ok(b.to_natal(A, c)), ok(b.to_natal(B, c))
            if sa and sb_ and (na or nb):
                out.append((c, R, r, s, A, B, sa + sb_, na + nb, far))
    if not out:
        return []
    cells, notes = [], []
    for c, R, r, s, A, B, sky, nat, far in out:
        oc = other_chart(c)
        for o in [r, s] + sky + nat + [x for f in far for x in [f[0]] + f[2]]:
            if o not in cells:
                cells.append(o)
        ends = ', '.join(sorted({ln['line'].split(' → ')[0][2:] for ln in nat}))
        fr = '; '.join(f"{E} ({f['line']} {f['plane']}{', the same pair' if f is s else ''})" for f, E, _ in far)
        notes.append(f"{r['line']} {r['plane']}: {s['line']} {s['plane']} ({A} and {B} on sky {b.X}; {ends} on {c} {b.X}); "
                     f"on {oc} {b.X}: {fr}")
    return [{'key': ('BB48', b.X), 'cells': cells, 'notes': notes}]


def bb49(b):
    """The H X - J X line scores (no conj / contraparallel) and a sky pair S R - S Y on its target (not naming X or the Moon) has a royal
    star R at one end and at the other a body Y on natal X (S Y -> H X or S Y -> J X, no conj / cp); and two or more royal stars are on
    sky X (S R - S X, no conj / cp). X not Rahu or Ketu (their H - J lines pair up automatically). Any plane, any score."""
    if b.X in ('Rahu', 'Ketu'):
        return []
    ok = lambda rs: [o for o in rs if o['fam'] and o['fam'] not in CJ]
    sky = {R: ok(b.sky_y(R)) for R in ROY}
    sky = {R: v for R, v in sky.items() if v}
    if len(sky) < 2:
        return []
    out = []
    for r in ok(b.lines(f'H {b.X} – J {b.X}', scoring=True)):
        for s, A, B in b.pairs_on(r):
            if b.X in (A, B) or 'Moon' in (A, B):
                continue
            for R, Y in ((A, B), (B, A)):
                if R in ROY and Y not in ROY:
                    nat = ok(b.to_natal(Y, 'H')) + ok(b.to_natal(Y, 'J'))
                    if nat:
                        out.append((r, s, R, Y, nat))
    if not out:
        return []
    cells, notes = [], []
    for o in [x for R in ROY if R in sky for x in sky[R]]:
        cells.append(o)
    for r, s, R, Y, nat in out:
        for o in [r, s] + nat:
            if o not in cells:
                cells.append(o)
        notes.append(f"{r['line']} {r['plane']} carried by {s['line']} {s['plane']} ({R} with {Y}; {Y} on "
                     f"{', '.join(sorted({n['line'].split(' → ')[1][0] for n in nat}))} {b.X}); royal stars on sky {b.X}: "
                     f"{', '.join(R2 for R2 in ROY if R2 in sky)}" + ('' if R in sky else f' ({R} not among them)'))
    return [{'key': ('BB49', b.X), 'cells': cells, 'notes': notes}]


def bb50(b):
    """The H X - J X line scores (no conj / contraparallel) and two sky pairs on its target (pairs not naming X or the Moon) carry it:
    one with a royal star at an end (S R - S Y), and one with no royal star whose end Y is on sky X (S Y - S X, no conj / cp). X not
    Rahu or Ketu (their H - J lines pair up automatically). Any plane, any score."""
    if b.X in ('Rahu', 'Ketu'):
        return []
    ok = lambda rs: [o for o in rs if o['fam'] and o['fam'] not in CJ]
    cells, notes = [], []
    for r in ok(b.lines(f'H {b.X} – J {b.X}', scoring=True)):
        ps = [(s, A, B) for s, A, B in b.pairs_on(r) if b.X not in (A, B) and 'Moon' not in (A, B)]
        roy = [s for s, A, B in ps if A in ROY or B in ROY]
        sky = [(s, Y, ok(b.sky_y(Y))) for s, A, B in ps if A not in ROY and B not in ROY for Y in (A, B) if ok(b.sky_y(Y))]
        if not roy or not sky:
            continue
        for o in [r] + roy + [x for s, Y, on in sky for x in [s] + on]:
            if o not in cells:
                cells.append(o)
        notes.append(f"{r['line']} {r['plane']} carried by the royal pair{'s' if len(roy) > 1 else ''} "
                     f"{'; '.join(s['line'] + ' ' + s['plane'] for s in roy)} and by "
                     f"{'; '.join(s['line'] + ' ' + s['plane'] + ' (' + Y + ' on sky ' + b.X + ')' for s, Y, _ in sky)}")
    return [{'key': ('BB50', b.X), 'cells': cells, 'notes': notes}] if cells else []


def bb51(b):
    """The same royal star R has a scoring natal line to X in both charts (H R - H X and J R - J X, no conj / contraparallel, any plane),
    each carried by a sky pair on its target (pairs not naming X or the Moon); a horse pair and a jockey pair share a body Y (not a royal
    star), and Y is on sky X (S Y - S X scores, no conj / cp). Any plane, any score."""
    ok = lambda rs: [o for o in rs if o['fam'] and o['fam'] not in CJ]
    def carried(c, R):
        out = []
        for _, R2, r in b.star_rows(c, scoring=True):
            if R2 != R or r['fam'] in CJ:
                continue
            for s, A, B in b.pairs_on(r):
                if b.X not in (A, B) and 'Moon' not in (A, B):
                    out.append((r, s, {A, B}))
        return out
    cells, notes = [], []
    for R in ROY:
        hc, jc = carried('H', R), carried('J', R)
        for Y in sorted({y for _, _, e in hc for y in e} & {y for _, _, e in jc for y in e}):
            if Y in ROY:
                continue
            sky = ok(b.sky_y(Y))
            if not sky:
                continue
            hs = [(r, s) for r, s, e in hc if Y in e]
            js = [(r, s) for r, s, e in jc if Y in e]
            for o in [x for r, s in hs + js for x in (r, s)] + sky:
                if o not in cells:
                    cells.append(o)
            notes.append(f"{R} in both charts: {'; '.join(r['line'] + ' ' + r['plane'] + ' carried by ' + s['line'] + ' ' + s['plane'] for r, s in hs)}"
                         f" | {'; '.join(r['line'] + ' ' + r['plane'] + ' carried by ' + s['line'] + ' ' + s['plane'] for r, s in js)}"
                         f"; {Y} in both, on sky {b.X}")
    return [{'key': ('BB51', b.X), 'cells': cells, 'notes': notes}] if cells else []


def bb52(b):
    """A scoring royal natal line to X (c R - c X, no conj / contraparallel, any chart and plane) is carried by the sky line S X - S Y
    itself (a 'Sky lines on the same target' row naming X; Y not a royal star, not the Moon; the line not conj / cp), and in Y's own sheet
    the same sky line S X - S Y (same plane) carries a royal natal line to Y (c' R' - c' Y, no conj / cp). One sky line between X and Y on
    a royal line of each end. Any score."""
    D = getattr(b, 'all', None) or {}
    def selfpairs(bb):
        out = []
        for c, R, r in bb.star_rows(scoring=True):
            if r['fam'] in CJ:
                continue
            for s in bb.same_on(r):
                m = re.match(r'S (.+) – S (.+)$', s['line'] or '')
                if m and bb.X in m.groups() and s['fam'] not in CJ:
                    Y = [g for g in m.groups() if g != bb.X][0]
                    if Y not in ROY and Y != 'Moon':
                        out.append((r, s, Y))
        return out
    cells, notes = [], []
    for r, s, Y in selfpairs(b):
        if Y not in D:
            continue
        other = [(r2, s2) for r2, s2, X2 in selfpairs(Body(Y, D[Y]))
                 if X2 == b.X and s2['line'] == s['line'] and s2['plane'] == s['plane']]
        if not other:
            continue
        for o in [r, s] + [r2 for r2, _ in other]:
            if o not in cells:
                cells.append(o)
        notes.append(f"{s['line']} {s['plane']} carries {r['line']} {r['plane']} and, on {Y}, "
                     + '; '.join(f"{r2['line']} {r2['plane']}" for r2, _ in other))
    return [{'key': ('BB52', b.X), 'cells': cells, 'notes': notes}] if cells else []


RULES = [('BB1', bb1, 'Mercury'), ('BB2', bb2, 'Mars'), ('BB3', bb3, 'Jupiter'), ('BB4', bb4, 'Saturn'),
         ('BB5', bb5, 'Uranus'), ('BB6', bb6, 'Uranus'), ('BB7', bb7, 'Neptune'), ('BB8', bb8, 'Rahu'),
         ('BB9', bb9, 'Rahu'), ('BB10', bb10, 'Ketu'), ('BB11', bb11, 'Ceres'), ('BB12', bb12, 'Pallas'),
         ('BB13', bb13, 'Juno'), ('BB14', bb14, 'Vesta'), ('BB15', bb15, 'Chiron'), ('BB16', bb16, 'Eris'),
         ('BB17', bb17, 'Makemake'), ('BB18', bb18, 'Venus'), ('BB19', bb19, 'Venus'), ('BB20', bb20, 'Jupiter'),
         ('BB21', bb21, 'Saturn'), ('BB22', bb22, 'Saturn'), ('BB23', bb23, 'Neptune'), ('BB24', bb24, 'Rahu'), ('BB25', bb25, 'Ketu'), ('BB26', bb26, 'Ceres'), ('BB27', bb27, 'Pallas'), ('BB28', bb28, 'Juno'), ('BB29', bb29, 'Vesta'), ('BB30', bb30, 'Eris'), ('BB31', bb31, 'Gonggong'),
         ('BB32', bb32, 'Sun'), ('BB32b', bb32b, 'Sun'), ('BB33', bb33, 'Mercury'), ('BB34', bb34, 'Mars'), ('BB35', bb35, 'Saturn'),
         ('BB36', bb36, 'Uranus'), ('BB37', bb37, 'Pluto'), ('BB38', bb38, 'Juno'), ('BB39', bb39, 'Makemake'),
         ('BB40', bb40, 'Sedna'), ('BB41', bb41, 'Sun'), ('BB42', bb42, 'Mercury'), ('BB43', bb43, 'Venus'), ('BB44', bb44, 'Jupiter'), ('BB45', bb45, 'Saturn'), ('BB46', bb46, 'Saturn'), ('BB47', bb47, 'Ceres'), ('BB48', bb48, 'Chiron'), ('BB49', bb49, 'Haumea'), ('BB50', bb50, 'Makemake'), ('BB51', bb51, 'Venus'), ('BB52', bb52, 'Uranus')]


def decade_pairs(cells):
    """Targets with the same digits a decade apart (e.g. ninth 7.77778 / 77.7778)."""
    seen = {}
    for r in cells:
        if r and r['fam'] in ('whole', 'ninth') and r['tgt']:
            try:
                t = float(r['tgt'])
            except ValueError:
                continue
            seen.setdefault((r['fam'], r['tgt']), (t, r))
    out = []
    ks = list(seen)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            (ta, ra), (tb, rb) = seen[ks[i]], seen[ks[j]]
            lo, hi = sorted((ta, tb))
            k = hi / lo if lo else 0
            if any(abs(k - 10 ** n) < 1e-3 * 10 ** n for n in (1, 2)):
                out.append(f"{ra['tgt']} ({ra['line']}) / {rb['tgt']} ({rb['line']})")
    return out


def run(path):
    data = load(path)
    race = os.path.basename(path).replace('_bybody.xlsx', '')
    res = {}
    for rid, fn, _ in RULES:
        res[rid] = []
        for runner, D in data.items():
            for X, d in D.items():
                b = Body(X, d)
                b.all = D  # the runner's other bodies (BB52 reads the partner body's sheet)
                seen = set()
                for case in fn(b):
                    if case['key'] in seen:
                        continue
                    seen.add(case['key'])
                    cells, uniq = [], set()
                    for r in case['cells']:
                        k = (r['line'], r['plane'], r['tgt'])
                        if k not in uniq:
                            uniq.add(k); cells.append(r)
                    res[rid].append({'runner': runner, 'body': X, 'cells': [cell(r) for r in cells],
                                     'notes': case.get('notes', []),
                                     'lights': [cell(r) for r in b.lights()],
                                     'decade': decade_pairs(cells),
                                     'additive': additive_steps(cells),
                                     'watch_only': bool(case.get('watch_only'))})
    return race, list(data), res


def write(race, runners, res, out):
    os.makedirs(out, exist_ok=True)
    rules = {}
    if os.path.exists(RULES_JSON):
        rules = {r['id']: r for r in json.load(open(RULES_JSON))}
    md = [f'# {race} — body-by-body rules BB1-{RULES[-1][0]}', '',
          'Data only, no pick. Rules from docs/eddie_read/bybody_rules/rules.json (each with its origin race). '
          'Field: runners holding the rule in this race.', '']
    summ = []
    for rid, _, _ in RULES:
        hc = [c for c in res[rid] if not c['watch_only']]
        holders = sorted({c['runner'] for c in hc})
        wo = sorted({c['runner'] for c in res[rid] if c['watch_only']})
        summ.append(f"| {rid} | {len(hc)} | {len(holders)} | {', '.join(holders) or '-'} | {', '.join(wo)} |")
    md += ['| Rule | Cases | Runners | Holders | Watch only |', '|---|---|---|---|---|'] + summ + ['']
    for rid, _, _ in RULES:
        info = rules.get(rid, {})
        md += [f'## {rid} — {info.get("title", "")}', '', f"Rule: {info.get('text', '')}", '',
               f"Origin: {info.get('origin', '')}", '']
        cases = res[rid]
        if not [c for c in cases if not c['watch_only']]:
            md += ['No runner holds it.', '']
        for c in cases:
            others = sorted({x['runner'] for x in cases if x['runner'] != c['runner'] and not x['watch_only']})
            tag = 'WATCH only, not a holder' if c['watch_only'] else ('only' if not others else 'also: ' + ', '.join(others))
            md.append(f"### {c['runner']} — {c['body']} ({tag})")
            md += [f'- {x}' for x in c['cells']]
            md += [f'- {n}' for n in c['notes']]
            md += [f'- {w}' for w in c.get('additive', [])]
            if c['decade']:
                md.append('- HIGHLIGHT same digits a decade apart: ' + '; '.join(c['decade']))
            if c['lights']:
                md.append('- lights on ' + c['body'] + ': ' + '; '.join(c['lights']))
            md.append('')
    p = os.path.join(out, f'{race}_bbrules')
    open(p + '.md', 'w').write('\n'.join(md) + '\n')
    json.dump({'race': race, 'runners': runners, 'rules': res}, open(p + '.json', 'w'), indent=1, ensure_ascii=False)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('bybody_xlsx')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(HERE), 'docs', 'eddie_read', 'bybody_rules'))
    a = ap.parse_args()
    race, runners, res = run(a.bybody_xlsx)
    p = write(race, runners, res, a.out)
    for rid, _, _ in RULES:
        print(rid, len([c for c in res[rid] if not c['watch_only']]),
              sorted({c['runner'] for c in res[rid] if not c['watch_only']}),
              ('watch only: ' + ', '.join(sorted({c['runner'] for c in res[rid] if c['watch_only']}))) if any(c['watch_only'] for c in res[rid]) else '')
    print('->', p + '.md')


if __name__ == '__main__':
    main()
