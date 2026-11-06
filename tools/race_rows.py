#!/usr/bin/env python3
"""race_rows.py - print the rows of a race workbook in the order of the reading procedure.

Usage:  python3 race_rows.py race_batch_..._jupiter_tables.xlsx [minutes]

It prints rows only. No flags, no tallies, no win rates.
A chart row is "in" when its target is not outside and it passes Eddie's cut-offs by family
(whole, golden, conj from 50; ninth, √2, silver, φ power always). Sky Jupiter lines are shown
at any score. Each row shows
its plane, value, family / target and score, which other runners are in on the
same row, and which sit near but off (nearest the same target, outside).

Sections (they follow the reading procedure in claude/handover-new-race-reads.md):
  1  sky Jupiter, Sun and Moon lines (every hit, any score, with timing)
  2  each sky Jupiter / Sun / Moon star line followed onto every runner's T24 star rows (horse and jockey)
  3  each sky Jupiter / Sun / Moon body line followed onto every runner's rows on that body
  3b sky Sun and sky Moon → each runner's natal bodies (T24 rows, from 4 Nov 2026 workbooks)
  4  sky body both ways (a sky body reaching a chart's Jupiter and sky Jupiter reaching the same body)
  5  every runner's Jupiter-table rows (T1-T8), only / shared / near but off
  6  the same body on both charts of a runner
  7  sky lines exact within the window on the rows only that runner is in (any score)
  8  near-but-off pairs between runners, both ways
  9  the rules register (R1-R42, R12c and R41c, claude/isolation-log.md), computed from POSITIONS with families.py, 3-digit rule first, 4-digit marked
"""
import math
import re
import sys
from collections import defaultdict

import openpyxl

TABLES = {'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8'}


def family(t):
    t = t.lower()
    if 'conj' in t: return 'conj'
    if 'ninth' in t: return 'ninth'
    if 'sqrt2' in t or '√2' in t: return '√2'
    if 'silver' in t: return 'silver'
    if 'phi power' in t: return 'φ power'
    if 'golden' in t or '×φ' in t: return 'golden'
    return 'whole'


def counts(fam, score):
    """Eddie's cut-offs by family: whole, golden and conj count from 50; ninth, √2, silver, φ power always."""
    if fam in ('whole', 'golden', 'conj'):
        return score is not None and score >= 50
    return True


def tok(t):
    t = t.replace('nearest:', '').strip()
    return t.split()[0] if t else ''


def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None


def other_body(label):
    a, b = [s.strip() for s in label.split('→')]
    return (a if 'Jupiter' in b and not a.endswith('Jupiter') else b).split(' ', 1)[1]


def load(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    off = None
    for r in wb['POSITIONS'].iter_rows(values_only=True, max_row=1):
        m = re.search(r'off \d{4}-\d\d-\d\d (\d\d:\d\d)', str(r[0]))
        off = m.group(1) if m else None
    runners, jt, t24, smr = [], defaultdict(dict), defaultdict(dict), defaultdict(dict)
    bodies = []
    for sh in wb.sheetnames:
        if not re.match(r'P\d+$', sh): continue
        ws = wb[sh]
        name = jockey = None
        hdr = None
        for row in ws.iter_rows():
            v = ['' if c.value is None else c.value for c in row]
            s0, s1 = str(v[0]), str(v[1]) if len(v) > 1 else ''
            if name is None and s0.startswith('P'):
                head = s0.split(' / ')
                name = ' '.join(head[0].split()[2:]); jockey = head[1].strip() if len(head) > 1 else ''
                runners.append((sh, name, jockey)); continue
            if s0 in TABLES and '→' in s1 and len(v) > 15:
                for pl, i in (('RA', 2), ('Dec', 10)):
                    val, tg = num(v[i]), str(v[i + 2])
                    if val is None or not tg: continue
                    jt[(s0, s1, pl)][sh] = dict(value=val, tgt=tg, tok=tok(tg), fam=family(tg),
                                               score=num(v[i + 5]),
                                               hit='—' not in tg and counts(family(tg), num(v[i + 5])))
            if s0 == '' and len(v) > 30 and v[2] == 'Sun' and hdr is None:
                hdr = [str(x) for x in v]
                mids = [i for i, x in enumerate(hdr) if x.startswith('star = middle')]   # RA midpoints, Dec midpoints
                plane_of = {i: ('RA' if i < mids[0] else 'Dec') for i in range(2, mids[1]) if i != mids[0]}
                if not bodies: bodies = [x for x in hdr[2:mids[0]] if x and not x.startswith('S ')]
            sm_row = s1.startswith(('S Sun → H', 'S Sun → J', 'S Moon → H', 'S Moon → J'))   # Eddie, 4 Nov 2026
            if s0 == 'T24' and hdr and (s1.startswith('H ') or s1.startswith('J ') or sm_row):
                chart, star = (s1.split(' → ')[1][0], s1.split(' → ')[0][2:]) if sm_row else (s1[0], s1[2:])
                for i, c in enumerate(row):
                    if i not in plane_of or not isinstance(c.value, (int, float)): continue
                    body = hdr[i] if i < len(hdr) else ''
                    if not body or body.startswith('S '): continue     # sky columns S Jupiter / S Sun / S Moon
                    com = c.comment.text.split('\n')[0] if c.comment else ''
                    if not com: continue
                    miss = com.startswith('nearest') or '—' in com
                    parts = [p.strip() for p in com.replace('nearest:', '').split('·')]
                    tg = parts[0] + (' ' + parts[1].split('—')[0].strip() if len(parts) > 1 else '')
                    sc = num(parts[3]) if len(parts) > 3 and not miss else None
                    (smr if sm_row else t24)[(chart, star, body, plane_of[i])][sh] = dict(
                        value=c.value, tgt=tg, tok=tok(parts[0]), fam=family(com), score=sc,
                        hit=not miss and counts(family(com), sc))
    sky = []                                     # sky Jupiter, Sun and Moon lines (SKY block of each sky sheet)
    for centre in ('Jupiter', 'Sun', 'Moon'):
        if f'SKY {centre.upper()}' not in wb.sheetnames: continue
        for r in wb[f'SKY {centre.upper()}'].iter_rows(values_only=True):
            if r[0] != 'SKY' or not r[1] or not str(r[1]).startswith(f'S {centre} →'): continue
            for pl, i, si, ti in (('RA', 2, 7, 10), ('Dec', 11, 16, 19)):
                tg = str(r[i + 2] or '')
                if num(r[i]) is None or not tg or '—' in tg: continue
                sky.append(dict(centre=centre, point=str(r[1]).split('→')[1].strip()[2:], plane=pl, value=num(r[i]), tgt=tg,
                                score=num(r[si]), timing=r[ti] if len(r) > ti else None))
    events = []
    for s in ('SKY JUPITER', 'SKY SUN', 'SKY MOON'):
        for r in wb[s].iter_rows(values_only=True):
            if r[0] != 'TIMELINE' or not isinstance(r[2], (int, float)): continue
            rel = str(r[4])
            rest = rel.split(':', 1)[1] if ':' in rel else rel
            bs = set(b.strip()[2:].strip() for b in re.split('[–→]', rest) if b.strip().startswith('S '))
            events.append(dict(time=r[1], mins=float(r[2]), rel=rel, plane=r[5], tgt=r[7], score=r[10],
                               bodies=bs))
    return off, runners, jt, t24, sky, events, set(bodies), smr


def fmt(d):
    sc = '' if d['score'] is None else f", {d['score']:g}"
    return f"{d['value']:.4f} {d['tgt']}{sc}"


def field_note(cells, sh, names):
    me = cells[sh]
    ins = [f"{names[o]} {d['tok']}" + ('' if d['tok'] == me['tok'] else ' (other target)')
           for o, d in cells.items() if o != sh and d['hit']]
    near = [f"{names[o]} {d['value']:.4f}" for o, d in cells.items()
            if o != sh and not d['hit'] and d['tok'] == me['tok']]
    out = 'ONLY' if not ins else 'also in: ' + ', '.join(ins)
    if near: out += ' | near but off: ' + ', '.join(near)
    return out


def main():
    path = sys.argv[1]
    win = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    off, runners, jt, t24, sky, events, bodyset, smr = load(path)
    names = {sh: n for sh, n, j in runners}
    near_ev = sorted([e for e in events if abs(e['mins']) <= win], key=lambda e: e['mins'])
    print(f"{path.split('/')[-1]}  off {off}  runners {len(runners)}  window ±{win:g} min")
    print("Rows only. In = target not outside + cut-offs by family (whole/golden/conj 50+). Sky Jupiter / Sun / Moon lines any score. Read with the procedure in claude/handover-new-race-reads.md.\n")

    sline = lambda s: (f"{s['plane']} {s['value']:.4f} {s['tgt']}" + ('' if s['score'] is None else f", {s['score']:g}"))
    print("=" * 78 + "\n1  SKY JUPITER, SUN AND MOON LINES (every hit, any score)")
    for centre in ('Jupiter', 'Sun', 'Moon'):
        lines = [s for s in sky if s['centre'] == centre]
        print(f"\n  sky {centre}:" + ('' if lines else ' (sheet not in this workbook)'))
        for s in lines:
            print(f"  S {centre} → {s['point']:18} {sline(s)}  {s['timing'] or ''}")

    print("\n" + "=" * 78 + "\n2  SKY JUPITER / SUN / MOON STAR LINES FOLLOWED ONTO EACH RUNNER'S T24 STAR ROWS")
    stars = sorted(set(s['point'] for s in sky if s['point'] not in bodyset and s['point'] not in ('equator', 'Moon')))
    for star in stars:
        line = ' | '.join(f"sky {s['centre']} → {star} {sline(s)}" for s in sky if s['point'] == star)
        print(f"\n  ── {line}")
        for sh, n, j in runners:
            for chart, who in (('H', n), ('J', j)):
                cells = [(k, c) for k, c in t24.items() if k[0] == chart and k[1] == star and sh in c and c[sh]['hit']]
                if not cells:
                    print(f"    {sh} {chart} {star} ({who}): nothing in"); continue
                print(f"    {sh} {chart} {star} ({who}):")
                for k, c in sorted(cells, key=lambda kc: (kc[0][2] != 'Jupiter', kc[0][3], kc[0][2])):
                    mark = '  ← JUPITER' if k[2] == 'Jupiter' else ''
                    print(f"       → {k[2]:10} {k[3]:3} {fmt(c[sh])}  [{field_note(c, sh, names)}]{mark}")
            hb = {k[2] for k, c in t24.items() if k[0] == 'H' and k[1] == star and sh in c and c[sh]['hit']}
            jb = {k[2] for k, c in t24.items() if k[0] == 'J' and k[1] == star and sh in c and c[sh]['hit']}
            if hb & jb: print(f"    {sh} same body on both charts' {star}: {', '.join(sorted(hb & jb))}")

    print("\n" + "=" * 78 + "\n3  SKY JUPITER / SUN / MOON BODY LINES FOLLOWED ONTO EACH RUNNER'S ROWS ON THAT BODY")
    print("   (Jupiter tables T1-T8, and the T24 rows S Sun / S Moon → natal body)")
    for b in sorted(set(s['point'] for s in sky if s['point'] in bodyset or s['point'] in ('Sun', 'Moon'))):
        line = ' | '.join(f"sky {s['centre']} → {b} {sline(s)}" for s in sky if s['point'] == b)
        print(f"\n  ── {line}")
        for sh, n, j in runners:
            hits = [(k, c) for k, c in jt.items() if sh in c and c[sh]['hit'] and other_body(k[1]) == b]
            for k, c in hits:
                print(f"    {sh} {n:20} {k[0]} {k[1]:28} {k[2]:3} {fmt(c[sh])}  [{field_note(c, sh, names)}]")
            for k, c in sorted(smr.items()):
                if k[2] == b and sh in c and c[sh]['hit']:
                    print(f"    {sh} {n:20} T24 S {k[1]} → {k[0]} {b:16} {k[3]:3} {fmt(c[sh])}  [{field_note(c, sh, names)}]")

    print("\n" + "=" * 78 + "\n3b SKY SUN AND SKY MOON → EACH RUNNER'S NATAL BODIES (T24 rows, in)")
    if not smr:
        print("  (no S Sun / S Moon rows in this workbook: built before 4 Nov 2026)")
    for sh, n, j in runners:
        print(f"\n  {sh} {n} / {j}")
        for centre in ('Sun', 'Moon'):
            for chart in ('H', 'J'):
                rows_ = sorted([(k, c) for k, c in smr.items() if k[0] == chart and k[1] == centre and sh in c and c[sh]['hit']],
                               key=lambda kc: (kc[0][2] != 'Jupiter', kc[0][3], kc[0][2]))
                for k, c in rows_:
                    mark = '  ← JUPITER' if k[2] == 'Jupiter' else ''
                    print(f"    S {centre} → {chart} {k[2]:10} {k[3]:3} {fmt(c[sh]):34} [{field_note(c, sh, names)}]{mark}")

    print("\n" + "=" * 78 + "\n4  SKY BODY BOTH WAYS (sky X → chart Jupiter and sky Jupiter → chart X)")
    for sh, n, j in runners:
        found = False
        for b in sorted(bodyset - {'Jupiter'}):
            ways = []
            for t, lab in (('T7', f'S {b} → H Jupiter'), ('T8', f'S {b} → J Jupiter'),
                           ('T5', f'S Jupiter → H {b}'), ('T6', f'S Jupiter → J {b}')):
                for pl in ('RA', 'Dec'):
                    c = jt.get((t, lab, pl), {})
                    if sh in c and c[sh]['hit']:
                        ways.append((lab, pl, c))
            dirs = {('X→' if w[0].startswith(f'S {b}') else 'J→') for w in ways}
            if len(dirs) < 2: continue
            found = True
            print(f"  {sh} {n} / {j}: {b}")
            for lab, pl, c in ways:
                print(f"     {lab:26} {pl:3} {fmt(c[sh])}  [{field_note(c, sh, names)}]")
            for e in near_ev:
                if {'Jupiter', b} <= e['bodies']:
                    print(f"     line: {e['time']} ({e['mins']:+.1f}) {e['rel']} {e['plane']} {e['tgt']}, {e['score']}")
        if not found: print(f"  {sh} {n}: none")

    print("\n" + "=" * 78 + "\n5  EACH RUNNER'S JUPITER-TABLE ROWS (T1-T8, in)")
    side = {'T1': 'HORSE', 'T5': 'HORSE', 'T7': 'HORSE', 'T2': 'JOCKEY', 'T6': 'JOCKEY', 'T8': 'JOCKEY',
            'T3': 'HORSE → JOCKEY', 'T4': 'JOCKEY → HORSE'}
    for sh, n, j in runners:
        print(f"\n  {sh} {n} / {j}")
        for group in ('HORSE', 'JOCKEY', 'HORSE → JOCKEY', 'JOCKEY → HORSE'):
            rows = sorted([(k, c) for k, c in jt.items() if side[k[0]] == group and sh in c and c[sh]['hit']],
                          key=lambda kc: (kc[0][0], kc[0][1]))
            if not rows: continue
            print(f"    {group}")
            for k, c in rows:
                print(f"      {k[0]} {k[1]:30} {k[2]:3} {fmt(c[sh]):34} [{field_note(c, sh, names)}]")

    print("\n" + "=" * 78 + "\n6  THE SAME BODY ON BOTH CHARTS (Jupiter tables, in)")
    for sh, n, j in runners:
        hb, jb = defaultdict(list), defaultdict(list)
        for k, c in jt.items():
            if sh not in c or not c[sh]['hit']: continue
            b = other_body(k[1])
            # the chart the body sits on: T1, T4, T5, T7 horse; T2, T3, T6, T8 jockey
            (hb if k[0] in ('T1', 'T4', 'T5', 'T7') else jb)[b].append(f"{k[1]} {k[2]} {c[sh]['tgt']}" + ('' if c[sh]['score'] is None else f" {c[sh]['score']:g}"))
        both = sorted(set(hb) & set(jb) - {'Jupiter'})
        print(f"  {sh} {n}:" + ('' if both else ' none'))
        for b in both:
            print(f"     {b}:  H: {' / '.join(hb[b])}  ||  J: {' / '.join(jb[b])}")

    print("\n" + "=" * 78 + f"\n7  SKY LINES EXACT WITHIN ±{win:g} MIN ON THE ROWS ONLY THAT RUNNER IS IN (lines at any score)")
    for sh, n, j in runners:
        pts = defaultdict(set)
        only = lambda c: all(not d['hit'] for o, d in c.items() if o != sh)
        for k, c in jt.items():    # rows only this runner is in
            if sh in c and c[sh]['hit'] and only(c):
                pts[other_body(k[1])].add(f"{k[0]} {k[1]} {k[2]}")
        for k, c in smr.items():   # S Sun / S Moon → natal body rows (section 3b) only this runner is in
            if sh in c and c[sh]['hit'] and only(c):
                pts[k[2]].add(f"T24 S {k[1]} → {k[0]} {k[2]} {k[3]}")
        for k, c in t24.items():   # T24 rows of the sky Jupiter / Sun / Moon stars (section 2) only this runner is in
            if k[1] in stars and sh in c and c[sh]['hit'] and only(c):
                pts[k[1]].add(f"T24 {k[0]} {k[1]} → {k[2]} {k[3]}")
        print(f"\n  {sh} {n} / {j}")
        any_ev = False
        for e in near_ev:
            on = sorted(b for b in e['bodies'] if b in pts and b != 'Jupiter')
            if not on: continue
            any_ev = True
            print(f"    {e['time']} ({e['mins']:+.1f}) {e['rel']} {e['plane']} {e['tgt']}, {e['score']}  on {', '.join(on)}")
        if not any_ev: print("    none")

    print("\n" + "=" * 78 + "\n8  NEAR BUT OFF BETWEEN RUNNERS, BOTH WAYS (Jupiter tables and T24)")
    allrows = list(jt.items()) + [(('T24',) + k, c) for k, c in t24.items()]
    for a in range(len(runners)):
        for b in range(a + 1, len(runners)):
            A, B = runners[a][0], runners[b][0]
            ab, ba = [], []
            for k, c in allrows:
                if A in c and B in c and c[A]['tok'] == c[B]['tok']:
                    lab = ' '.join(str(x) for x in k)
                    if c[A]['hit'] and not c[B]['hit']: ab.append(f"{lab}: {fmt(c[A])} (off {c[B]['value']:.4f})")
                    if c[B]['hit'] and not c[A]['hit']: ba.append(f"{lab}: {fmt(c[B])} (off {c[A]['value']:.4f})")
            if not ab and not ba: continue
            print(f"\n  {names[A]} in, {names[B]} near but off:" + ('' if ab else ' none'))
            for x in ab: print(f"     {x}")
            print(f"  {names[B]} in, {names[A]} near but off:" + ('' if ba else ' none'))
            for x in ba: print(f"     {x}")


# ---------------------------------------------------------------------------------------------------
# 9  RULES REGISTER (Eddie, 4 Nov 2026; rules and records in claude/isolation-log.md)
# Computed from POSITIONS with families.py (the astro-harmonics repo). Cut-offs as in the reads.
# ---------------------------------------------------------------------------------------------------
import os

REG_BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres',
              'Pallas', 'Juno', 'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus',
              'Transpluto', 'Rahu', 'Ketu']
REG_CUT = {'whole': 50, 'golden': 50, 'conj': 50}
R39_BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Saturn', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Rahu', 'Ketu']   # bodies that move (no outer / TNO)


def d3_digits(x):
    """First 3 significant digits, truncated, and the order of magnitude (the 3-digit rule)."""
    x = round(x, 10); k = math.floor(math.log10(x)); m = round(x * 10 ** (2 - k), 6)
    if m >= 1000: k, m = k + 1, round(x * 10 ** (1 - k), 6)
    elif m < 100: k, m = k - 1, round(x * 10 ** (3 - k), 6)
    return k, math.floor(m)


def match3(v, t):
    return v > 0 and t > 0 and d3_digits(v) == d3_digits(t)


def reg_families():
    """families.py from the astro-harmonics repo (ASTRO_REPO, else ~/astro-harmonics, else /home/claude/astro-harmonics)."""
    for root in (os.environ.get('ASTRO_REPO'), os.path.expanduser('~/astro-harmonics'), '/home/claude/astro-harmonics'):
        if root and os.path.exists(os.path.join(root, 'tools', 'families.py')):
            for sub in ('tools', 'rebuild_kit'):
                if os.path.join(root, sub) not in sys.path: sys.path.insert(0, os.path.join(root, sub))
            import families
            return families
    return None


def _register(path, digits=3):
    """Readings as the records were made (4 Nov 2026): a cell counts on its best family only; R6x leaves out a centre
    on its own natal namesake (S Sun → H Sun); R9 needs conj as the cell's best family; R10's sky bodies are the 24
    natal bodies without Jupiter (no Moon). R13 includes the sky Moon."""
    F = reg_families()
    if F is None: return None
    F_orig_match = F.digit_match                          # Eddie, 6 Nov 2026: "it should be 3 digit first / that shows all the
    if digits == 3: F.digit_match = match3                # relationships / then you can refine with quality / 4 digits if required"
    wb = openpyxl.load_workbook(path, read_only=True)
    P, names, kind = {}, {}, {}
    for r in wb['POSITIONS'].iter_rows(values_only=True):
        if r and len(r) > 6 and isinstance(r[5], (int, float)) and r[2] in ('S', 'H', 'J'):
            if r[3] == 'Polaris': continue                   # not in the SKY block, T1 / T2 or T24
            P[(r[0], r[2], r[3])] = (r[5], r[6]); kind[r[3]] = r[4]
            if r[1] and r[0] != 'SKY': names[r[0]] = str(r[1])
    runners = sorted({k[0] for k in P if k[0] != 'SKY'})
    SKY = lambda x: P.get(('SKY', 'S', x))

    def dist(a, b, pl):
        if pl == 'RA':
            x = abs(a[0] - b[0]) % 360; return min(x, 360 - x)
        return abs(a[1] - b[1])

    def cells(a, b, conj=True):
        """{plane: (value, target, family, score)} for the cells that count at the cut-offs."""
        out = {}
        if a is None or b is None: return out
        for pl in ('RA', 'Dec'):
            v = dist(a, b, pl); bb = F.best(v, pl)
            if bb and bb['score'] >= REG_CUT.get(bb['family'], 0) and (conj or bb['family'] != 'conj'):
                out[pl] = (v, str(bb['target']), bb['family'], bb['score'])
        return out

    def txt(c):
        return '; '.join(f"{pl} {v:.4f} {t} {f} {s:.2f}" for pl, (v, t, f, s) in c.items())

    def anyc(a, b):
        """{plane: (value, target, family, score)} for any best-family score > 0 (a sky line)."""
        out = {}
        for pl in ('RA', 'Dec'):
            v = dist(a, b, pl); bb = F.best(v, pl)
            if bb and bb['score'] > 0: out[pl] = (v, str(bb['target']), bb['family'], bb['score'])
        return out

    def anysc(a, b):
        return any((F.best(dist(a, b, pl), pl) or {}).get('score', 0) > 0 for pl in ('RA', 'Dec'))

    def d3(x):                                                                    # first 3 significant digits, truncated (R41, R42)
        x = round(x, 10); k = math.floor(math.log10(x)); m = round(x * 10 ** (2 - k), 6)
        if m >= 1000: k, m = k + 1, round(x * 10 ** (1 - k), 6)
        elif m < 100: k, m = k - 1, round(x * 10 ** (3 - k), 6)
        return k, math.floor(m)

    def loose(a, b, pl):
        """Loose same-body target (R41, R42): (value, target, family, offset) or None."""
        if a is None or b is None: return None
        v = dist(a, b, pl)
        if v < 2: return None
        if abs(v - round(v)) < 0.03: return (v, str(round(v)), 'whole', v - round(v))
        orig = F.digit_match
        F.digit_match = lambda x, t: x > 0 and t > 0 and d3(x) == d3(t)
        try: ev = F.evaluate(v, pl)
        finally: F.digit_match = orig
        ev = [e for e in ev if e['family'] not in ('whole', 'conj')]
        return (v, str(ev[0]['target']), ev[0]['family'], ev[0]['off']) if ev else None

    lt = lambda t: f"{t[0]:.4f} {t[1]} {t[2]} ({t[3]:+.4f})"

    skystars = sorted({k[2] for k in P if k[0] == 'SKY' and kind.get(k[2]) == 'star'})
    lines = {c: [st for st in skystars if SKY(c) and anysc(SKY(c), SKY(st))] for c in ('Jupiter', 'Sun', 'Moon')}
    allst = sorted(set(sum(lines.values(), [])))
    onl = lambda st: ','.join(c for c in lines if st in lines[c])
    N = lambda R: f"{R} {names.get(R, '')[:30]}"
    picked = defaultdict(set)
    out = defaultdict(list)

    def add(rule, R, s):
        picked[rule].add(R); out[rule].append(f"  {N(R)}: {s}")

    nat = lambda R, ch, x: P.get((R, ch, x))
    skylines = [(c, pt, pl, val) for c in ('Jupiter', 'Sun', 'Moon') if SKY(c)          # every sky centre line, not conj (R17)
                for pt in sorted({k[2] for k in P if k[0] == 'SKY' and k[2] != c})
                for pl, val in anyc(SKY(c), SKY(pt)).items() if val[2] != 'conj']
    top = max(lines['Jupiter'], key=lambda st: max((F.best(dist(SKY('Jupiter'), SKY(st), pl), pl) or {'score': 0})['score']
                                                   for pl in ('RA', 'Dec'))) if lines['Jupiter'] else None
    bsc = lambda a, b: max((F.best(dist(a, b, pl), pl) or {'score': 0})['score'] for pl in ('RA', 'Dec'))
    jb = [X for X in REG_BODIES if X != 'Jupiter' and SKY(X) and SKY('Jupiter') and bsc(SKY('Jupiter'), SKY(X)) > 0]
    topb = max(jb, key=lambda X: bsc(SKY('Jupiter'), SKY(X))) if jb else None         # R27
    conjpts = [(x, c, kind.get(x) == 'star') for c in ('Jupiter', 'Sun', 'Moon') if SKY(c)                    # R30
               for x in sorted({k[2] for k in P if k[0] == 'SKY'}) if x not in ('Jupiter', 'Sun', 'Moon')
               and kind.get(x) in ('star', 'body') and any(f == 'conj' for (_, _, f, _) in cells(SKY(c), SKY(x)).values())]
    conjcand, sj90 = defaultdict(list), {}
    for R in runners:
        for c in ('Sun', 'Moon'):                                 # R1
            for X in REG_BODIES:
                h, j = cells(SKY(c), nat(R, 'H', X)), cells(SKY(c), nat(R, 'J', X))
                if not (h and j) or X == 'Jupiter': continue
                back = [f"S {X} → {jc} Jupiter [{txt(t)}]" for jc in 'HJ' if (t := cells(SKY(X), nat(R, jc, 'Jupiter')))]
                if back: add('R1', R, f"S {c} → H {X} [{txt(h)}], → J {X} [{txt(j)}]; " + ' | '.join(back))
        for jc, oc in (('H', 'J'), ('J', 'H')):                    # R2, R2a
            for X in REG_BODIES:
                if X == 'Jupiter': continue
                a, b = cells(nat(R, jc, 'Jupiter'), nat(R, jc, X)), cells(nat(R, jc, 'Jupiter'), nat(R, oc, X))
                if a and b:
                    s = f"{jc} Jupiter → {jc} {X} [{txt(a)}] and → {oc} {X} [{txt(b)}]"
                    add('R2', R, s)
                    if jc == 'H': add('R2a', R, s)
        for A, B in (('H Jupiter', 'H Pluto'), ('J Jupiter', 'J Pluto'), ('H Jupiter', 'J Pluto'), ('J Jupiter', 'H Pluto'),
                     ('S Jupiter', 'H Pluto'), ('S Jupiter', 'J Pluto'), ('S Pluto', 'H Jupiter'), ('S Pluto', 'J Jupiter')):   # R3
            ka = SKY(A[2:]) if A[0] == 'S' else nat(R, A[0], A[2:]); kb = SKY(B[2:]) if B[0] == 'S' else nat(R, B[0], B[2:])
            if ka is None or kb is None: continue
            for pl in ('RA', 'Dec'):
                v = dist(ka, kb, pl); s, lab, t = F.score_family(v, 'golden', pl)
                if lab == '12×φ' and s >= 50: add('R3', R, f"{A} → {B} {pl} {v:.4f} 12×φ {s:.2f}")
        for ch in 'HJ':
            oc = 'J' if ch == 'H' else 'H'
            for X in REG_BODIES:
                if X == 'Jupiter' or nat(R, ch, X) is None: continue
                mo = cells(SKY('Moon'), nat(R, ch, X))
                if mo:
                    if (t := cells(nat(R, oc, 'Jupiter'), nat(R, ch, X))):       # R4
                        add('R4', R, f"S Moon → {ch} {X} [{txt(mo)}] + {oc} Jupiter → {ch} {X} [{txt(t)}]")
                    if (t := cells(nat(R, ch, 'Jupiter'), nat(R, ch, X))):       # R4b
                        add('R4b', R, f"S Moon → {ch} {X} [{txt(mo)}] + {ch} Jupiter → {ch} {X} [{txt(t)}]")
                    if (t := cells(SKY(X), nat(R, ch, 'Jupiter'))):              # R1b
                        add('R1b', R, f"S Moon → {ch} {X} [{txt(mo)}] + S {X} → {ch} Jupiter [{txt(t)}]")
                    for pl, (v, tg, fam, sc) in mo.items():                      # R5
                        if fam == 'conj': continue
                        for st in lines['Moon']:
                            for pl2, (v2, tg2, fam2, sc2) in cells(nat(R, ch, st), nat(R, ch, X)).items():
                                if tg2 == tg and fam2 == fam:
                                    add('R5', R, f"S Moon → {ch} {X} {pl} {v:.4f} {tg} {sc:.2f} = {ch} {st} → {X} {pl2} {v2:.4f} {sc2:.2f}")
                got = {c: g for c in ('Jupiter', 'Sun', 'Moon') if c != X and (g := cells(SKY(c), nat(R, ch, X)))}
                if 'Jupiter' in got and 'Moon' in got:                            # R6
                    add('R6', R, f"{ch} {X}: S Jupiter [{txt(got['Jupiter'])}] + S Moon [{txt(got['Moon'])}]")
                if len(got) >= 2:                                                 # R6x
                    add('R6x', R, f"{ch} {X}: " + ' | '.join(f"S {c} [{txt(g)}]" for c, g in got.items()))
        for st in allst:                                                          # R7, R8
            both = [X for X in REG_BODIES if X != 'Jupiter' and all(cells(nat(R, c2, st), nat(R, c2, X)) for c2 in 'HJ')]
            for ch in 'HJ':
                jh = cells(nat(R, ch, st), nat(R, ch, 'Jupiter'))
                if jh and both:
                    add('R7', R, f"{ch} {st} ({onl(st)}) → {ch} Jupiter [{txt(jh)}]; on both charts' {st}: {', '.join(both)}")
            for X in both:
                back = [f"S {X} → {jc} Jupiter [{txt(t)}]" for jc in 'HJ' if (t := cells(SKY(X), nat(R, jc, 'Jupiter')))]
                if back: add('R8', R, f"{X} on both charts' {st} ({onl(st)}); " + ' | '.join(back))
        for ch in 'HJ':                                                           # R9, R9b, R9c
            for st in allst:
                if nat(R, ch, st) is None: continue
                for X in REG_BODIES:
                    if X == 'Jupiter' or nat(R, ch, X) is None: continue
                    a = cells(nat(R, ch, st), nat(R, ch, X)); b = cells(nat(R, ch, 'Jupiter'), nat(R, ch, X))
                    if not (a and b): continue
                    s = f"{ch} {st} ({onl(st)}) → {X} [{txt(a)}] + {ch} Jupiter → {X} [{txt(b)}]"
                    add('R9b', R, s)
                    if any(f == 'conj' for (_, _, f, _) in a.values()): add('R9', R, s)
                    if st == top and set(a) & set(b): add('R9c', R, s)
        for X in REG_BODIES:                                                      # R10
            if X == 'Jupiter': continue
            a, b = cells(SKY(X), nat(R, 'H', 'Jupiter')), cells(SKY(X), nat(R, 'J', 'Jupiter'))
            if a and b: add('R10', R, f"S {X} → H Jupiter [{txt(a)}] + → J Jupiter [{txt(b)}]")
        for ch in 'HJ':
            J = nat(R, ch, 'Jupiter')
            s = [f"{st} [{txt(t)}]" for st in lines['Jupiter'] if (t := cells(nat(R, ch, st), J))]   # R11
            if len(s) >= 2: add('R11', R, f"{ch}: " + ' | '.join(s))
            for X in REG_BODIES:                                                  # R12
                if X == 'Jupiter' or not (sj := cells(SKY('Jupiter'), nat(R, ch, X))): continue
                for st in allst:
                    a = cells(nat(R, ch, st), nat(R, ch, X)); b = cells(nat(R, ch, st), J)
                    if a and b: add('R12', R, f"{ch} {X}: S Jupiter [{txt(sj)}] + {st} ({onl(st)}) → {X} [{txt(a)}] + {st} → {ch} Jupiter [{txt(b)}]")
                    if a and b and any(f == 'conj' for (_, _, f, _) in a.values()):   # R12c (Eddie, 5 Nov 2026): the star–X cell a conj
                        add('R12c', R, f"{ch} {X}: S Jupiter [{txt(sj)}] + {st} ({onl(st)}) conj {X} [{txt(a)}] + {st} → {ch} Jupiter [{txt(b)}]")
            seen = defaultdict(list)                                              # R13
            pts = [(f"{ch} {x}", P[k]) for k in P if k[0] == R and k[1] == ch and (x := k[2]) != 'Jupiter']
            pts += [(f"S {x}", SKY(x)) for x in REG_BODIES + ['Moon'] if x != 'Jupiter' and SKY(x)]
            for lab, p in pts:
                for pl, (v, tg, fam, sc) in cells(p, J, conj=False).items():
                    if pl == 'RA' and lab.endswith('equator'): continue   # the equator is a Dec row only
                    seen[(fam, tg)].append((lab, f"{lab} {pl} {v:.4f} {sc:.2f}"))
            for (fam, tg), v in seen.items():
                labs = {a for a, _ in v}
                if len(labs) >= 2 and any(a.startswith('S ') for a in labs):
                    add('R13', R, f"{ch} Jupiter on {tg} {fam}: " + ' | '.join(t for _, t in v))
        for c in ('Jupiter', 'Sun', 'Moon'):                                      # R14 (Worcester 22 Aug 2021)
            for st in lines[c]:
                for pl, (v, tg, fam, sc) in anyc(SKY(c), SKY(st)).items():
                    if fam == 'conj': continue
                    for ch in 'HJ':
                        if nat(R, ch, st) is None or not (jb := cells(nat(R, ch, st), nat(R, ch, 'Jupiter'))): continue
                        for X in REG_BODIES:
                            if X == 'Jupiter': continue
                            for pl2, (v2, tg2, fam2, sc2) in cells(nat(R, ch, st), nat(R, ch, X)).items():
                                if tg2 == tg and fam2 == fam:
                                    add('R14', R, f"S {c} → S {st} {pl} {v:.4f} {tg} {fam} ({sc:.2f}) = {ch} {st} → {X} {pl2} {v2:.4f} ({sc2:.2f}); "
                                                  f"{st} → {ch} Jupiter [{txt(jb)}]")
        for ch in 'HJ':                                                           # R15 (Worcester 22 Aug 2021)
            oc = 'J' if ch == 'H' else 'H'
            for X in REG_BODIES:
                if X == 'Jupiter' or nat(R, ch, X) is None or nat(R, oc, X) is None: continue
                got = {c: g for c in ('Jupiter', 'Sun', 'Moon') if c != X and (g := cells(SKY(c), nat(R, ch, X)))}
                if len(got) < 2: continue
                js = [f"{jn} Jupiter → {oc} {X} [{txt(t)}]" for jn, Jp in (('H', nat(R, 'H', 'Jupiter')), ('J', nat(R, 'J', 'Jupiter')),
                                                                     ('S', SKY('Jupiter'))) if (t := cells(Jp, nat(R, oc, X)))]
                if js:
                    add('R15', R, f"{ch} {X}: " + ' | '.join(f"S {c} [{txt(g)}]" for c, g in got.items()) + ' ++ ' + ' / '.join(js))
        for X in REG_BODIES:                                                      # R16 (Musselburgh 25 Aug 2021)
            if X == 'Jupiter' or not SKY(X) or not (ml := anyc(SKY('Moon'), SKY(X))): continue
            for jc in 'HJ':
                if (t := cells(SKY(X), nat(R, jc, 'Jupiter'))):
                    add('R16', R, f"S Moon → S {X} [{txt(ml)}] + S {X} → {jc} Jupiter [{txt(t)}]")
        for X in REG_BODIES + ['Moon']:                                           # R17 (Musselburgh 25 Aug 2021)
            if X == 'Jupiter' or not SKY(X): continue
            for jc in 'HJ':
                for pl, (v, tg, fam, sc) in cells(SKY(X), nat(R, jc, 'Jupiter'), conj=False).items():
                    m = [f"S {c} → S {pt} {pl2} {v2:.4f}" for c, pt, pl2, (v2, tg2, fam2, sc2) in skylines if tg2 == tg and fam2 == fam]
                    if m: add('R17', R, f"S {X} → {jc} Jupiter {pl} {v:.4f} {tg} {fam} ({sc:.2f}) = " + ', '.join(m))
        for c in ('Jupiter', 'Sun', 'Moon'):                                      # R18 (Wolverhampton 25 Aug 2021)
            for pl, (v, tg, fam, sc) in cells(SKY(c), nat(R, 'J', 'Pallas')).items():
                if fam == 'conj': add('R18', R, f"S {c} conj J Pallas {pl} {v:.4f} ({sc:.2f})")
        for ch in 'HJ':                                                           # R19 (Haydock 8 Jun 2020)
            for X in REG_BODIES:
                if X in ('Jupiter', 'Moon') or nat(R, ch, X) is None: continue
                a, b = cells(SKY('Jupiter'), nat(R, ch, X)), cells(nat(R, ch, 'Jupiter'), nat(R, ch, X))
                if a and b: add('R19', R, f"{ch} {X}: S Jupiter → {ch} {X} [{txt(a)}] + {ch} Jupiter → {ch} {X} [{txt(b)}]")
        for a_, b_ in (('H', 'J'), ('J', 'H')):                                   # R20 (Chelmsford 26 Aug 2021)
            ra, ke = cells(SKY('Rahu'), nat(R, a_, 'Jupiter')), cells(SKY('Ketu'), nat(R, b_, 'Jupiter'))
            if ra and ke: add('R20', R, f"S Rahu → {a_} Jupiter [{txt(ra)}] + S Ketu → {b_} Jupiter [{txt(ke)}]")
        for ch in 'HJ':                                                           # R21 (Ascot 3 Sep 2021)
            if top is None or nat(R, ch, top) is None: continue
            if not (bj := cells(nat(R, ch, top), nat(R, ch, 'Jupiter'))): continue
            for X in REG_BODIES:
                if X == 'Jupiter' or nat(R, ch, X) is None: continue
                a, b = cells(nat(R, ch, top), nat(R, ch, X)), cells(nat(R, ch, 'Jupiter'), nat(R, ch, X))
                if set(a) & set(b):
                    add('R21', R, f"{ch} {top} → {X} [{txt(a)}] + {ch} Jupiter → {X} [{txt(b)}] + {ch} {top} → {ch} Jupiter [{txt(bj)}]")
        # R22-R31 (Eddie, 5 Nov 2026: shapes seen on winners Kempton 4 Sep - Fontwell 20 Oct 2021, added together and
        # backfilled; every earlier race is in-sample, the record counts from the next race on)
        nodej = [f"S {n} → {jc} Jupiter [{txt(t)}]" for n in ('Rahu', 'Ketu') for jc in 'HJ'
                 if (t := cells(SKY(n), nat(R, jc, 'Jupiter')))]
        if nodej:                                                                 # R24 (N3): a sky node on a natal Jupiter
            add('R24', R, ' | '.join(nodej))
            lit = [f"S {c} → {ch} {n} [{txt(t)}]" for c in ('Sun', 'Moon') for ch in 'HJ' for n in ('Rahu', 'Ketu')
                   if (t := cells(SKY(c), nat(R, ch, n)))]
            if lit: add('R22', R, ' | '.join(nodej) + ' ++ ' + ' | '.join(lit))     # R22 (N1): + Sun / Moon on a natal node
        for X in REG_BODIES:                                                      # R23 (N2): Sun on X one chart, Moon on X the other
            if X == 'Jupiter': continue
            for a_, b_ in (('H', 'J'), ('J', 'H')):
                s_, m_ = cells(SKY('Sun'), nat(R, a_, X)), cells(SKY('Moon'), nat(R, b_, X))
                if s_ and m_: add('R23', R, f"S Sun → {a_} {X} [{txt(s_)}] + S Moon → {b_} {X} [{txt(m_)}]")
        for ch in 'HJ':                                                           # R25 Pallas
            if nat(R, ch, 'Pallas') is None: continue
            got = {f"S {c}": g for c in ('Jupiter', 'Sun', 'Moon') if (g := cells(SKY(c), nat(R, ch, 'Pallas')))}
            if (g := cells(nat(R, ch, 'Jupiter'), nat(R, ch, 'Pallas'))): got[f"{ch} Jupiter"] = g
            conj_ = [k for k, g in got.items() if k.startswith('S ') and any(f == 'conj' for (_, _, f, _) in g.values())]
            if len(got) >= 2 or conj_:
                add('R25', R, f"{ch} Pallas: " + ' | '.join(f"{k} [{txt(g)}]" for k, g in got.items()))
        for ch in 'HJ':                                                           # R26 royal star on a sky line → own Jupiter
            for st in ('Regulus', 'Aldebaran', 'Antares', 'Fomalhaut'):
                if st not in allst or nat(R, ch, st) is None: continue
                if (t := cells(nat(R, ch, st), nat(R, ch, 'Jupiter'))):
                    ln = ' | '.join(f"S {c} → S {st} [{txt(anyc(SKY(c), SKY(st)))}]" for c in lines if st in lines[c])
                    add('R26', R, f"{ch} {st} → {ch} Jupiter [{txt(t)}]; line: {ln}")
        if topb:                                                                  # R27 body of the strongest sky Jupiter body line
            for ch in 'HJ':
                if nat(R, ch, topb) is None: continue
                js = [f"{jc} Jupiter → {ch} {topb} [{txt(t)}]" for jc in 'HJ' if (t := cells(nat(R, jc, 'Jupiter'), nat(R, ch, topb)))]
                cs = [f"S {c} → {ch} {topb} [{txt(t)}]" for c in ('Jupiter', 'Sun', 'Moon') if c != topb
                      and (t := cells(SKY(c), nat(R, ch, topb)))]
                if js and cs: add('R27', R, ' | '.join(js) + ' ++ ' + ' | '.join(cs))
        chj = [f"S Chiron → {jc} Jupiter [{txt(t)}]" for jc in 'HJ' if (t := cells(SKY('Chiron'), nat(R, jc, 'Jupiter')))]
        if chj:                                                                   # R28 Chiron
            lit = [f"S {c} → {ch} Chiron [{txt(t)}]" for c in ('Sun', 'Moon') for ch in 'HJ' if (t := cells(SKY(c), nat(R, ch, 'Chiron')))]
            lit += [f"S {c} → S Chiron [{txt(t)}]" for c in ('Sun', 'Moon') if SKY('Chiron') and (t := anyc(SKY(c), SKY('Chiron')))]
            if lit: add('R28', R, ' | '.join(lit) + ' ++ ' + ' | '.join(chj))
        for jc in 'HJ':                                                           # R29 sky Ceres → natal Jupiter >= 95
            t = {pl: c for pl, c in cells(SKY('Ceres'), nat(R, jc, 'Jupiter')).items() if c[3] >= 95}
            if t: add('R29', R, f"S Ceres → {jc} Jupiter [{txt(t)}]")
        if top:                                                                   # R32 (Eddie, 5 Nov 2026; Brazen Akoya, Newcastle 9 Nov 2021):
            for ch in 'HJ':                                                       # natal X conj the natal star of the strongest sky
                if nat(R, ch, top) is None: continue                              # Jupiter star line, and sky Jupiter reaches X
                for X in REG_BODIES:
                    if X == 'Jupiter' or nat(R, ch, X) is None: continue
                    cj = {pl: c for pl, c in cells(nat(R, ch, top), nat(R, ch, X)).items() if c[2] == 'conj'}
                    if cj and (sj := cells(SKY('Jupiter'), nat(R, ch, X))):
                        add('R32', R, f"{ch} {top} conj {ch} {X} [{txt(cj)}] + S Jupiter → {ch} {X} [{txt(sj)}]; "
                                      f"line S Jupiter → S {top} [{txt(anyc(SKY('Jupiter'), SKY(top)))}]")
        for S_, c_, isstar in conjpts:                                            # R33 (Eddie, 5 Nov 2026; Brian Boranha, Catterick 19 Nov 2021):
            if not isstar: continue                                               # a sky conj star S: natal S reaches that chart's own
            for ch in 'HJ':                                                       # Jupiter and natal S is conj a natal body X (same chart)
                st = nat(R, ch, S_)
                if st is None or not (jj := cells(st, nat(R, ch, 'Jupiter'))): continue
                for X in REG_BODIES:
                    if X == 'Jupiter' or nat(R, ch, X) is None: continue
                    cj = {pl: c for pl, c in cells(st, nat(R, ch, X)).items() if c[2] == 'conj'}
                    if cj:
                        add('R33', R, f"S {c_} conj S {S_} [{txt({pl: c for pl, c in cells(SKY(c_), SKY(S_)).items() if c[2] == 'conj'})}]; "
                                      f"{ch} {S_} → {ch} Jupiter [{txt(jj)}] + {ch} {S_} conj {ch} {X} [{txt(cj)}]")
        for S_, c_, isstar in conjpts:                                            # R34 (Eddie, 5 Nov 2026; Strictlyadancer, Haydock 20 Nov 2021):
            if not isstar: continue                                               # R33 crossed: natal S conj a natal body X on one chart,
            for ch in 'HJ':                                                       # and the other chart's Jupiter reaches that X
                oc = 'J' if ch == 'H' else 'H'
                st = nat(R, ch, S_)
                if st is None: continue
                for X in REG_BODIES:
                    if X == 'Jupiter' or nat(R, ch, X) is None: continue
                    cj = {pl: c for pl, c in cells(st, nat(R, ch, X)).items() if c[2] == 'conj'}
                    if cj and (oj := cells(nat(R, oc, 'Jupiter'), nat(R, ch, X))):
                        add('R34', R, f"S {c_} conj S {S_} [{txt({pl: c for pl, c in cells(SKY(c_), SKY(S_)).items() if c[2] == 'conj'})}]; "
                                      f"{ch} {S_} conj {ch} {X} [{txt(cj)}] + {oc} Jupiter → {ch} {X} [{txt(oj)}]")
        for ch in 'HJ':                                                           # R35 (Eddie, 5 Nov 2026; Not Available, Newbury 26 Nov 2021):
            for x in sorted({k[2] for k in P if k[0] == R and k[1] == ch and kind.get(k[2]) in ('body', 'star')}):   # two sky centres
                if x == 'Moon': continue                                          # each conj the same natal point
                cj = {c: {pl: v for pl, v in cells(SKY(c), nat(R, ch, x)).items() if v[2] == 'conj'} for c in ('Jupiter', 'Sun', 'Moon') if c != x}
                cj = {c: v for c, v in cj.items() if v}
                if len(cj) >= 2:
                    add('R35', R, f"{ch} {x}: " + ' | '.join(f"S {c} conj [{txt(v)}]" for c, v in cj.items()))
        for ch in 'HJ':                                                           # R37 (Eddie, 5 Nov 2026; Greaneteen, Sandown 4 Dec 2021):
            J = nat(R, ch, 'Jupiter')                                             # sky centre → natal X at the target of a sky line to a
            for c1 in ('Jupiter', 'Sun', 'Moon'):                                 # star S; natal S → own Jupiter; sky X → own Jupiter
                for X in REG_BODIES:
                    if X in ('Jupiter', c1) or nat(R, ch, X) is None: continue
                    for pl, (v, tg, fam, sc) in cells(SKY(c1), nat(R, ch, X), conj=False).items():
                        for c2, st, pl2, (v2, tg2, fam2, sc2) in skylines:
                            if kind.get(st) != 'star' or tg2 != tg or fam2 != fam: continue
                            if (sj := cells(nat(R, ch, st), J)) and (xj := cells(SKY(X), J)):
                                add('R37', R, f"S {c1} → {ch} {X} {pl} {v:.4f} {tg} {fam} {sc:.2f} = S {c2} → S {st} {pl2} {v2:.4f} ({sc2:.2f}); "
                                              f"{ch} {st} → {ch} Jupiter [{txt(sj)}]; S {X} → {ch} Jupiter [{txt(xj)}]")
        for S_, c_, isstar in conjpts:                                            # R38 (Eddie, 5 Nov 2026; Nicholas T, Newcastle 11 Dec 2021):
            if not isstar or c_ == 'Jupiter': continue                            # sky Sun / Moon conj star S, S on a sky Jupiter line,
            jl = anyc(SKY('Jupiter'), SKY(S_))                                    # natal S → own Jupiter in that line's plane (any score)
            for ch in 'HJ':
                st = nat(R, ch, S_)
                if st is None or not jl: continue
                for pl, (v, tg, fam, sc) in anyc(st, nat(R, ch, 'Jupiter')).items():
                    if pl in jl:
                        add('R38', R, f"S {c_} conj S {S_} [{txt({p: c for p, c in cells(SKY(c_), SKY(S_)).items() if c[2] == 'conj'})}]; "
                                      f"S Jupiter → S {S_} [{txt({pl: jl[pl]})}]; {ch} {S_} → {ch} Jupiter {pl} {v:.4f} {tg} {fam} {sc:.2f}")
        for ch in 'HJ':                                                           # R39 (Eddie, 5 Nov 2026; Nicholas T, Newcastle 11 Dec 2021):
            for X in R39_BODIES:                                                  # a sky-line star S reaches natal X, sky S reaches the same X
                nx = nat(R, ch, X)                                                # at the same target, and sky X is conj natal X
                if nx is None or not SKY(X): continue
                cj = {pl: c for pl, c in cells(SKY(X), nx).items() if c[2] == 'conj'}
                if not cj: continue
                for st in allst:
                    if nat(R, ch, st) is None: continue
                    b = cells(SKY(st), nx)
                    for pl, (v, tg, fam, sc) in cells(nat(R, ch, st), nx).items():
                        if fam == 'conj': continue
                        for pl2, (v2, tg2, fam2, sc2) in b.items():
                            if tg2 == tg and fam2 == fam:
                                add('R39', R, f"{ch} {st} ({onl(st)}) → {ch} {X} {pl} {v:.4f} {tg} {fam} {sc:.2f}; S {st} → {ch} {X} {pl2} {v2:.4f} {sc2:.2f}; "
                                              f"S {X} conj {ch} {X} [{txt(cj)}]")
        for ch in 'HJ':                                                           # R40 (Eddie, 5 Nov 2026; Shakem Up'arry, Haydock 18 Dec 2021,
            for nd, od in (('Rahu', 'Ketu'), ('Ketu', 'Rahu')):                   # New Age Dawning, Ffos Las 5 Jan 2022): a sky centre conj a
                if nat(R, ch, nd) is None: continue                               # natal node, and the other node of that chart reached by a
                ok = nat(R, ch, od)                                               # Jupiter (S, H or J) or a natal sky-line star of that chart
                for c in ('Jupiter', 'Sun', 'Moon'):
                    cj = {pl: v for pl, v in cells(SKY(c), nat(R, ch, nd)).items() if v[2] == 'conj'}
                    if not cj or ok is None: continue
                    reach = [f"{src} → {ch} {od} [{txt(t)}]" for src, pt in (('S Jupiter', SKY('Jupiter')), ('H Jupiter', nat(R, 'H', 'Jupiter')),
                             ('J Jupiter', nat(R, 'J', 'Jupiter'))) if (t := cells(pt, ok))]
                    reach += [f"{ch} {st} ({onl(st)}) → {ch} {od} [{txt(t)}]" for st in allst if (t := cells(nat(R, ch, st), ok))]
                    if reach:
                        add('R40', R, f"S {c} conj {ch} {nd} [{txt(cj)}]; " + ' | '.join(reach))
        for X in REG_BODIES:                                                      # R41 (Eddie, 6 Nov 2026; Venturous, Secret Satire, Art Power):
            if X == 'Ketu': continue                                              # sky X → H X and sky X → J X both on a loose target in the same
            for pl in ('RA', 'Dec'):                                              # plane (loose: whole ±0.03, other families 3-digit rule, any
                a = loose(SKY(X), nat(R, 'H', X), pl); b = loose(SKY(X), nat(R, 'J', X), pl)   # score; values 2 or more; Ketu = Rahu)
                if a and b: add('R41', R, f"{X} {pl} H {lt(a)} | J {lt(b)}")
            for hp, jp in (('RA', 'Dec'), ('Dec', 'RA')):                         # R41c (Eddie, 6 Nov 2026; Ishvara, Haydock 8 Jun 2020): R41
                a = loose(SKY(X), nat(R, 'H', X), hp); b = loose(SKY(X), nat(R, 'J', X), jp)   # with the planes crossed (horse RA, jockey
                if a and b: add('R41c', R, f"{X} H {hp} {lt(a)} | J {jp} {lt(b)}")       # Dec, or horse Dec, jockey RA)
        for ch in 'HJ':                                                           # R42 (Eddie, 6 Nov 2026; Kilcummin, Art Power, Venturous): a loose
            for X in REG_BODIES:                                                  # same-body cell sky X → natal X (either plane) and the sky Moon
                if X == 'Ketu' or nat(R, ch, X) is None: continue                 # → the same natal X scoring 90 or more ("sky moon is the clock")
                sb = [f"{pl} {lt(t)}" for pl in ('RA', 'Dec') if (t := loose(SKY(X), nat(R, ch, X), pl))]
                mo = {pl: c for pl, c in cells(SKY('Moon'), nat(R, ch, X)).items() if c[3] >= 90}
                if sb and mo: add('R42', R, f"S {X} → {ch} {X} " + '; '.join(sb) + f" | S Moon → {ch} {X} [{txt(mo)}]")
        sj90[R] = [f"{ch} {X} {pl} {v:.4f} {tg} {f} {s:.2f}" for ch in 'HJ' for X in REG_BODIES if X != 'Jupiter'
                   for pl, (v, tg, f, s) in cells(SKY('Jupiter'), nat(R, ch, X)).items() if s >= 90]
        for S_, c_, isstar in conjpts:                                            # R30 closest natal conj to the sky conj point
            for ch in 'HJ':
                if nat(R, ch, S_) is None: continue
                for Y in [k[2] for k in P if k[0] == R and k[1] == ch and k[2] != S_ and kind.get(k[2]) != 'equator' and (isstar or kind.get(k[2]) == 'star')]:
                    for pl, (v, tg, f, s) in cells(nat(R, ch, S_), nat(R, ch, Y)).items():
                        if f == 'conj': conjcand[(S_, c_)].append((v, R, f"S {c_} conj S {S_}; {ch} {S_} conj {ch} {Y} {pl} {v:.4f} ({s:.2f})"))
    for key, lst in conjcand.items():                                             # R30: the smallest distance in the field
        if not lst: continue
        best = min(v for v, _, _ in lst)
        for v, R, s in lst:
            if v == best: add('R30', R, s + ' (closest in the field)')
    mx = max((len(v) for v in sj90.values()), default=0)                          # R31 most sky Jupiter → natal body cells >= 90
    if mx >= 3:
        for R, v in sj90.items():
            if len(v) == mx: add('R31', R, f"{len(v)} cells: " + ' | '.join(v))

    nob = [R for R in runners if R not in picked['R9b']]                         # R36 (Eddie, 5 Nov 2026; Greaneteen, Sandown 4 Dec 2021):
    if len(nob) == 1:                                                             # the only runner in the field without R9b
        add('R36', nob[0], f"the only runner of {len(runners)} without R9b")
    order = ['R1', 'R2', 'R2a', 'R3', 'R4', 'R5', 'R6', 'R7', 'R6x', 'R8', 'R9', 'R9b', 'R9c', 'R4b', 'R1b', 'R10', 'R11', 'R12', 'R12c', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R21',
             'R22', 'R23', 'R24', 'R25', 'R26', 'R27', 'R28', 'R29', 'R30', 'R31', 'R32', 'R33', 'R34', 'R35', 'R36', 'R37', 'R38', 'R39', 'R40', 'R41', 'R41c', 'R42']
    F.digit_match = F_orig_match
    return dict(picked=picked, out=out, order=order, runners=runners, N=N, lines=lines, top=top)


def rules_register(path):
    """The register on the 3-digit rule (default since 6 Nov 2026); each pick marked '4d' when it also stands on the
    4-digit rule (the refinement), '3d only' when it needs the wider rule."""
    print("\n" + "=" * 78 + "\n9  RULES REGISTER (rules as worded in claude/isolation-log.md; run on the whole field)")
    r4 = _register(path, 4)
    r3 = _register(path, 3)
    if r3 is None:
        print("  families.py not found (set ASTRO_REPO to the astro-harmonics repo); section skipped"); return
    picked, out, order, runners, N, lines, top = (r3[k] for k in ('picked', 'out', 'order', 'runners', 'N', 'lines', 'top'))
    p4, o4 = r4['picked'], r4['out']
    print("  Scoring: 3-digit rule first (golden, φ power, ninth, √2, silver: first 3 significant digits); '4d' = the pick also stands"
          " on the 4-digit rule, '3d only' = it needs the wider rule. Lines marked '[3d only]' are not in the 4-digit run.")
    print(f"  sky star lines: Jupiter {len(lines['Jupiter'])}, Sun {len(lines['Sun'])}, Moon {len(lines['Moon'])}; "
          f"strongest sky Jupiter star line: {top}")
    tag = lambda r, x: N(x).strip() + ('' if x in p4[r] else ' [3d only]')
    print("\n  SUMMARY (runners each rule picks out; 3-digit, [3d only] = not picked on the 4-digit rule)")
    for r in order:
        p = sorted(picked[r])
        print(f"    {r:4} {len(p)}: " + (', '.join(tag(r, x) for x in p) if p else 'none') +
              (f"   | 4-digit: {len(p4[r])}" if len(p4[r]) != len(p) else ''))
    print("\n  RULES PER RUNNER (Eddie, 4 Nov 2026: the combinations; 3-digit, rules in brackets only on 3 digits)")
    for R in runners:
        rs = [(r if R in p4[r] else f"({r})") for r in order if R in picked[r]]
        print(f"    {N(R):34} {len(rs):2}: " + (', '.join(rs) if rs else 'none'))
    for r in order:
        print(f"\n  {r}" + ('' if out[r] else ': none'))
        s4 = set(o4[r])
        lst = [l + ('' if l in s4 else '  [3d only]') for l in out[r]]
        for line in lst[:40]: print('  ' + line)
        if len(lst) > 40: print(f"    ... {len(lst) - 40} more")
        gone = [l for l in o4[r] if l not in set(out[r])]
        for line in gone[:10]: print('  ' + line + '  [4d line, changed at 3 digits]')

if __name__ == '__main__':
    main()
    rules_register(sys.argv[1])
