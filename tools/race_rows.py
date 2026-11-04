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
  9  the rules register (R1-R13, claude/isolation-log.md), computed from POSITIONS with families.py
"""
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


def reg_families():
    """families.py from the astro-harmonics repo (ASTRO_REPO, else ~/astro-harmonics, else /home/claude/astro-harmonics)."""
    for root in (os.environ.get('ASTRO_REPO'), os.path.expanduser('~/astro-harmonics'), '/home/claude/astro-harmonics'):
        if root and os.path.exists(os.path.join(root, 'tools', 'families.py')):
            for sub in ('tools', 'rebuild_kit'):
                if os.path.join(root, sub) not in sys.path: sys.path.insert(0, os.path.join(root, sub))
            import families
            return families
    return None


def rules_register(path):
    """Readings as the records were made (4 Nov 2026): a cell counts on its best family only; R6x leaves out a centre
    on its own natal namesake (S Sun → H Sun); R9 needs conj as the cell's best family; R10's sky bodies are the 24
    natal bodies without Jupiter (no Moon). R13 includes the sky Moon."""
    print("\n" + "=" * 78 + "\n9  RULES REGISTER (rules as worded in claude/isolation-log.md; run on the whole field)")
    F = reg_families()
    if F is None:
        print("  families.py not found (set ASTRO_REPO to the astro-harmonics repo); section skipped"); return
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

    def anysc(a, b):
        return any((F.best(dist(a, b, pl), pl) or {}).get('score', 0) > 0 for pl in ('RA', 'Dec'))

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
    top = max(lines['Jupiter'], key=lambda st: max((F.best(dist(SKY('Jupiter'), SKY(st), pl), pl) or {'score': 0})['score']
                                                   for pl in ('RA', 'Dec'))) if lines['Jupiter'] else None
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

    order = ['R1', 'R2', 'R2a', 'R3', 'R4', 'R5', 'R6', 'R7', 'R6x', 'R8', 'R9', 'R9b', 'R9c', 'R4b', 'R1b', 'R10', 'R11', 'R12', 'R13']
    print(f"  sky star lines: Jupiter {len(lines['Jupiter'])}, Sun {len(lines['Sun'])}, Moon {len(lines['Moon'])}; "
          f"strongest sky Jupiter star line: {top}")
    print("\n  SUMMARY (runners each rule picks out)")
    for r in order:
        p = sorted(picked[r])
        print(f"    {r:4} {len(p)}: " + (', '.join(N(x).strip() for x in p) if p else 'none'))
    for r in order:
        print(f"\n  {r}" + ('' if out[r] else ': none'))
        for line in out[r][:40]: print('  ' + line)
        if len(out[r]) > 40: print(f"    ... {len(out[r]) - 40} more")


if __name__ == '__main__':
    main()
    rules_register(sys.argv[1])
