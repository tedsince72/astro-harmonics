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


if __name__ == '__main__':
    main()
