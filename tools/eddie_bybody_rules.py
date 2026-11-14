#!/usr/bin/env python3
"""Body-by-body rules (Eddie, 14 Nov 2026). BB1-BB17 from Lingfield AW 14:35 2 Apr 2021, 5 Pholas / Hollie Doyle;
BB18-BB24 from Haydock 13:45 8 Jun 2020, 7 Ishvara. Each rule's origin is in rules.json.

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
        f = a['fam']
        for s, A, B in b.pairs_on(a):
            if b.X in (A, B):
                continue
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


RULES = [('BB1', bb1, 'Mercury'), ('BB2', bb2, 'Mars'), ('BB3', bb3, 'Jupiter'), ('BB4', bb4, 'Saturn'),
         ('BB5', bb5, 'Uranus'), ('BB6', bb6, 'Uranus'), ('BB7', bb7, 'Neptune'), ('BB8', bb8, 'Rahu'),
         ('BB9', bb9, 'Rahu'), ('BB10', bb10, 'Ketu'), ('BB11', bb11, 'Ceres'), ('BB12', bb12, 'Pallas'),
         ('BB13', bb13, 'Juno'), ('BB14', bb14, 'Vesta'), ('BB15', bb15, 'Chiron'), ('BB16', bb16, 'Eris'),
         ('BB17', bb17, 'Makemake'), ('BB18', bb18, 'Venus'), ('BB19', bb19, 'Venus'), ('BB20', bb20, 'Jupiter'),
         ('BB21', bb21, 'Saturn'), ('BB22', bb22, 'Saturn'), ('BB23', bb23, 'Neptune'), ('BB24', bb24, 'Rahu')]


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
                                     'additive': additive_steps(cells)})
    return race, list(data), res


def write(race, runners, res, out):
    os.makedirs(out, exist_ok=True)
    rules = {}
    if os.path.exists(RULES_JSON):
        rules = {r['id']: r for r in json.load(open(RULES_JSON))}
    md = [f'# {race} — body-by-body rules BB1-BB{len(RULES)}', '',
          'Data only, no pick. Rules from docs/eddie_read/bybody_rules/rules.json (each with its origin race). '
          'Field: runners holding the rule in this race.', '']
    summ = []
    for rid, _, _ in RULES:
        holders = sorted({c['runner'] for c in res[rid]})
        summ.append(f"| {rid} | {len(res[rid])} | {len(holders)} | {', '.join(holders) or '-'} |")
    md += ['| Rule | Cases | Runners | Holders |', '|---|---|---|---|'] + summ + ['']
    for rid, _, _ in RULES:
        info = rules.get(rid, {})
        md += [f'## {rid} — {info.get("title", "")}', '', f"Rule: {info.get('text', '')}", '',
               f"Origin: {info.get('origin', '')}", '']
        cases = res[rid]
        if not cases:
            md += ['No runner holds it.', '']
            continue
        for c in cases:
            others = sorted({x['runner'] for x in cases if x['runner'] != c['runner']})
            tag = 'only' if not others else 'also: ' + ', '.join(others)
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
        print(rid, len(res[rid]), sorted({c['runner'] for c in res[rid]}))
    print('->', p + '.md')


if __name__ == '__main__':
    main()
