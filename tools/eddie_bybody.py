#!/usr/bin/env python3
"""Body by body view (Eddie, 8 Nov 2026; built on his Catterick 14:40 6 Apr 2022 Wotever Next read). Data only, no pick.

Usage:  python3 tools/eddie_bybody.py <race>_active.xlsx [--out DIR]     (default DIR docs/eddie_read/bybody)
        -> DIR/<race>/<cloth>_<horse>.md, one file per runner (horse and jockey), DIR/<race>/<race>_bybody.json, and
           DIR/<race>/<race>_bybody.xlsx (one sheet per runner, the same content and order; score cells coloured).

Reads the _active.xlsx only: META (tab, role, cloth, name), P##_DIST (NATAL x NATAL and TRANSIT -> NATAL, RA and DEC blocks),
TT_DIST (TRANSIT x TRANSIT, RA and DEC blocks), P##_POS and TRANS_POS (signed Dec, for contraparallels). Never a csv.

SCORING (Eddie, 8 Nov 2026; this tool only - families.py is not changed). Every family scored linearly, 100 (tol - dev) / tol, hit
when dev < tol; all families that hit are kept (each family's best target), highest score first, the others shown as 'also':
  whole 1..200 tol 0.02; golden k x phi (k 1..124) tol 0.0324; phi powers (rebuild_kit _PHI_POWER_TARGETS) tol 0.15 % of the
  target; ninths (the 48 _NINTH_RANGES targets) tol 0.2 % of the target; sqrt2 and silver (exact values) tol 0.15 % of the target;
  conjunction RA < 1.5 (tol 1.5), Dec < 0.3 (tol 0.3); opposition RA within 0.75 of 180; contraparallel |Dec a + Dec b| < 0.3
  (signed declinations, tol 0.3). No 4-digit rule.

LAYOUT, per runner, one section per body X (the 24 bodies, no Moon), in BODIES order:
  A chart whose META birth date is empty (e.g. an unknown jockey) has no lines; the file says so.
  1. horse lines: S X -> H X RA, Dec; H star - H X for Aldebaran, Antares, Fomalhaut, Regulus in RA, then in Dec; then the
     contraparallels among those pairs (sky X with natal X; natal star with natal X). Then the jockey lines the same way.
  2. 'Sky lines on the same target': every sky distance (S A - S B, A and B sky bodies incl. Moon or royal stars, each pair once,
     no Rahu - Ketu, no star - star; RA, Dec and sky contraparallels) whose family and target equal a hit of any line in 1
     (conjunctions not matched), with the line it matches; highest score first; 'none' when empty.
  3. 'Other scoring sky lines on X': every scoring line on the body (conjunctions incl.): S Y - S X (Y every sky body incl. Moon and
     the royal stars, not X, not the Rahu - Ketu pair), then S Y -> H X, then S Y -> J X (Y sky bodies incl. Moon, not X); each
     group highest score first.
"""
import argparse, json, math, os, re, sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'rebuild_kit'))
from active_vibrations import PHI, _PHI_POWER_TARGETS, _NINTH_RANGES  # noqa: E402

BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Moon', 'Rahu', 'Ketu',
          'Ceres', 'Pallas', 'Juno', 'Vesta', 'Chiron', 'Eris', 'Gonggong', 'Haumea', 'Makemake', 'Orcus', 'Quaoar', 'Sedna',
          'Transpluto']
ROYAL = ['Aldebaran', 'Antares', 'Fomalhaut', 'Regulus']
NATAL_BODIES = [b for b in BODIES if b != 'Moon']
SKY_POINTS = BODIES + ROYAL

R2 = math.sqrt(2.0)
SILVER = 1.0 + R2
_PP = {-1: 'φ^-1', 1: 'φ', 2: 'φ²', 3: 'φ³', 4: 'φ⁴', 5: 'φ⁵', 6: 'φ⁶', 7: 'φ⁷', 8: 'φ⁸', 9: 'φ⁹', 10: 'φ¹⁰'}
_PP_LAB = ([_PP[p] for p in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] + ['10' + _PP[p] for p in (-1, 1, 2, 3, 4, 5, 6, 7)]
           + ['100φ^-1', '100φ'])
TARGETS = [('whole', str(t), float(t), 0.02) for t in range(1, 201)]
TARGETS += [('golden', f'{k}×φ', k * PHI, 0.0324) for k in range(1, 125)]
TARGETS += [('phi power', lab, t, 0.0015 * t) for lab, t in zip(_PP_LAB, _PHI_POWER_TARGETS)]
TARGETS += [('ninth', f'{t:g}', t, 0.002 * t) for *_, t in _NINTH_RANGES]
TARGETS += [('sqrt2', lab, v, 0.0015 * v) for lab, v in (('1.414', R2), ('14.14', 10 * R2), ('141.4', 100 * R2),
                                                          ('0.707', R2 / 2), ('7.07', 10 * R2 / 2), ('70.7', 100 * R2 / 2))]
TARGETS += [('silver', lab, v, 0.0015 * v) for lab, v in (('2.414', SILVER), ('24.14', 10 * SILVER), ('0.414', SILVER - 2),
                                                           ('4.14', 10 * (SILVER - 2)), ('41.4', 100 * (SILVER - 2)))]
CONJ = {'RA': 1.5, 'Dec': 0.3}
OPP = 0.75
CP = 0.3


def hits(v, plane):
    """-> [(family, target, score)], one per family (its best target), highest score first."""
    h = []
    for fam, lab, t, tol in TARGETS:
        d = abs(v - t)
        if d < tol:
            h.append((fam, lab, 100 * (tol - d) / tol))
    c = CONJ[plane]
    if v < c:
        h.append(('conj', '0', 100 * (c - v) / c))
    if plane == 'RA' and 180 - v < OPP:
        h.append(('opposition', '180', 100 * (OPP - (180 - v)) / OPP))
    best = {}
    for x in h:
        if x[0] not in best or x[2] > best[x[0]][2]:
            best[x[0]] = x
    return sorted(best.values(), key=lambda x: -x[2])


def contraparallel(da, db):
    s = abs(da + db)
    return ('contraparallel', 'cp', 100 * (CP - s) / CP) if s < CP else None


def txt(x):
    lab = {'whole': x[1], 'conj': 'conj', 'opposition': '180 opposition', 'contraparallel': 'contraparallel'}
    return lab.get(x[0], f'{x[1]} {x[0]}') + f' ({x[2]:.1f})'


def score_text(h):
    if not h:
        return '—'
    return txt(h[0]) + (' (also: ' + '; '.join(txt(x) for x in h[1:]) + ')' if len(h) > 1 else '')


def blocks(rows):
    """TT_DIST / P##_DIST -> {(kind, plane, row label, column label): value}; kind N (natal x natal), S (transit -> natal or x transit)."""
    out = {}
    for i, row in enumerate(rows):
        t = row[0]
        if not (isinstance(t, str) and '—' in t):
            continue
        kind = 'N' if t.startswith('NATAL') else 'S'
        plane = 'RA' if 'RA distances' in t else 'Dec'
        hdr = rows[i + 1]
        for r2 in rows[i + 2:]:
            a = r2[0]
            if a is None or (isinstance(a, str) and '—' in a):
                break
            for j, b in enumerate(hdr):
                if j and b is not None and isinstance(r2[j], (int, float)):
                    out[(kind, plane, a, b)] = float(r2[j])
    return out


def positions(ws):
    return {r[0]: float(r[2]) for r in list(ws.iter_rows(values_only=True))[1:] if r and r[0] and isinstance(r[2], (int, float))}


def ra_positions(ws):
    return {r[0]: float(r[1]) for r in list(ws.iter_rows(values_only=True))[1:] if r and r[0] and isinstance(r[1], (int, float))}


def load(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    meta = [r for r in wb['META'].iter_rows(values_only=True) if r and isinstance(r[0], str) and r[0][:1] == 'P'
            and r[0][1:].isdigit()]
    runners = {}
    for tab, role, cloth, name, *rest in meta:
        ch = 'H' if role == 'horse' else 'J'
        r = runners.setdefault(cloth, {'name': {}, 'dist': {}, 'pos': {}, 'missing': []})
        r['name'][ch] = name
        if len(rest) >= 2 and rest[0] is None and rest[1] is None:   # no birth date in META: no chart (its tabs are not read)
            r['dist'][ch], r['pos'][ch] = {}, {}
            r.setdefault('ra', {})[ch] = {}
            r['missing'].append(ch)
            continue
        r['dist'][ch] = blocks(list(wb[tab + '_DIST'].iter_rows(values_only=True)))
        r['pos'][ch] = positions(wb[tab + '_POS'])
        r.setdefault('ra', {})[ch] = ra_positions(wb[tab + '_POS'])
    tt = blocks(list(wb['TT_DIST'].iter_rows(values_only=True)))
    tp = positions(wb['TRANS_POS'])
    return runners, tt, tp


def pair(d, kind, plane, a, b):
    v = d.get((kind, plane, a, b))
    return d.get((kind, plane, b, a)) if v is None else v


def sky_lines(tt, tp):
    """Every scoring sky distance between sky points (non-conj family hits only), for matching."""
    out = []
    for i, a in enumerate(SKY_POINTS):
        for b in SKY_POINTS[i + 1:]:
            if {a, b} == {'Rahu', 'Ketu'} or (a in ROYAL and b in ROYAL):
                continue
            for pl in ('RA', 'Dec'):
                v = pair(tt, 'S', pl, a, b)
                if v is None:
                    continue
                for h in hits(v, pl):
                    if h[0] != 'conj':
                        out.append({'line': f'S {a} – S {b}', 'plane': pl, 'value': v, 'hit': h})
            if a in tp and b in tp:
                c = contraparallel(tp[a], tp[b])
                if c:
                    out.append({'line': f'S {a} – S {b}', 'plane': 'Dec contraparallel', 'value': abs(tp[a] + tp[b]), 'hit': c})
    return out


def runner_view(r, tt, tp, sky):
    by_target = {}
    for s in sky:
        by_target.setdefault((s['hit'][0], s['hit'][1]), []).append(s)
    bodies = []
    for X in NATAL_BODIES:
        lines = []
        for ch in ('H', 'J'):
            d, npos = r['dist'][ch], r['pos'][ch]
            ls = [(f'S {X} → {ch} {X}', pl, d.get(('S', pl, X, X))) for pl in ('RA', 'Dec')]
            for pl in ('RA', 'Dec'):
                ls += [(f'{ch} {Y} – {ch} {X}', pl, pair(d, 'N', pl, X, Y)) for Y in ROYAL]
            for lab, pl, v in ls:
                if v is not None:
                    lines.append({'line': lab, 'plane': pl, 'value': v, 'hits': hits(v, pl)})
            cps = [(f'S {X} → {ch} {X}', tp.get(X), npos.get(X))] + [(f'{ch} {Y} – {ch} {X}', npos.get(Y), npos.get(X))
                                                                     for Y in ROYAL]
            for lab, a, b in cps:
                if a is not None and b is not None:
                    c = contraparallel(a, b)
                    if c:
                        lines.append({'line': lab, 'plane': 'Dec contraparallel', 'value': abs(a + b), 'hits': [c]})
        # horse natal X - jockey natal X (Eddie, 8 Nov 2026): RA wrapped 0-180, Dec |dDec|, contraparallel; from the _POS tabs
        hra, jra, hd, jd = r['ra']['H'].get(X), r['ra']['J'].get(X), r['pos']['H'].get(X), r['pos']['J'].get(X)
        if hra is not None and jra is not None:
            v = abs(hra - jra) % 360
            v = 360 - v if v > 180 else v
            lines.append({'line': f'H {X} – J {X}', 'plane': 'RA', 'value': v, 'hits': hits(v, 'RA')})
        if hd is not None and jd is not None:
            v = abs(hd - jd)
            lines.append({'line': f'H {X} – J {X}', 'plane': 'Dec', 'value': v, 'hits': hits(v, 'Dec')})
            c = contraparallel(hd, jd)
            if c:
                lines.append({'line': f'H {X} – J {X}', 'plane': 'Dec contraparallel', 'value': abs(hd + jd), 'hits': [c]})
        matches = []
        for ln in lines:
            for h in ln['hits']:
                if h[0] == 'conj':
                    continue
                for s in by_target.get((h[0], h[1]), []):
                    matches.append({**s, 'matches': f"{ln['line']} {ln['plane']}"})
        matches.sort(key=lambda m: -m['hit'][2])
        other = [[], [], []]
        for Y in SKY_POINTS:
            if Y == X or {X, Y} == {'Rahu', 'Ketu'}:
                continue
            for pl in ('RA', 'Dec'):
                v = pair(tt, 'S', pl, Y, X)
                if v is not None and hits(v, pl):
                    other[0].append({'line': f'S {Y} – S {X}', 'plane': pl, 'value': v, 'hits': hits(v, pl)})
            if Y in tp and X in tp:
                c = contraparallel(tp[X], tp[Y])
                if c:
                    other[0].append({'line': f'S {Y} – S {X}', 'plane': 'Dec contraparallel', 'value': abs(tp[X] + tp[Y]),
                                     'hits': [c]})
        for k, ch in ((1, 'H'), (2, 'J')):
            d, npos = r['dist'][ch], r['pos'][ch]
            for Y in BODIES:
                if Y == X:
                    continue
                for pl in ('RA', 'Dec'):
                    v = d.get(('S', pl, Y, X))
                    if v is not None and hits(v, pl):
                        other[k].append({'line': f'S {Y} → {ch} {X}', 'plane': pl, 'value': v, 'hits': hits(v, pl)})
                if Y in tp and X in npos:
                    c = contraparallel(tp[Y], npos[X])
                    if c:
                        other[k].append({'line': f'S {Y} → {ch} {X}', 'plane': 'Dec contraparallel',
                                         'value': abs(tp[Y] + npos[X]), 'hits': [c]})
        for g in other:
            g.sort(key=lambda o: -o['hits'][0][2])
        # S Y -> H X / J X rows on the same family + target as a line above (Eddie, 8 Nov 2026); S - S rows are already
        # in via sky_lines. Each such row is kept in 'other' too.
        for o in other[1] + other[2]:
            for h in o['hits']:
                if h[0] == 'conj':
                    continue
                for ln in lines:
                    if any(lh[0] == h[0] and lh[1] == h[1] for lh in ln['hits']):
                        matches.append({'line': o['line'], 'plane': o['plane'], 'value': o['value'], 'hit': h,
                                        'matches': f"{ln['line']} {ln['plane']}"})
        matches.sort(key=lambda m: -m['hit'][2])
        bodies.append({'body': X, 'lines': lines, 'matches': matches, 'other': other[0] + other[1] + other[2]})
    return bodies


RULES = ('Rules (Eddie, 8 Nov 2026): all linear. Whole ±0.02; golden ±0.0324; φ powers ±0.15 %; ninths ±0.2 %; √2 and silver '
         '±0.15 %; conjunction RA < 1.5 / Dec < 0.3; opposition RA within 0.75 of 180; contraparallel |Dec a + Dec b| < 0.3. '
         'Highest score first, other families as "also". Last lines: horse X – jockey X (natal to natal, RA wrapped, Dec). Sky lines on the same target = sky body / royal star pairs (Moon '
         'included, no Rahu–Ketu, no star–star) and the S Y → H X / S Y → J X lines on the same family and target as any '
         'scoring line above them (conjunctions not matched; those S Y → natal X rows also stay under "Other"). "Other scoring sky lines": every scoring sky line on the body - S Y – S X, then S Y → H X, then S Y → J X - '
         'conjunctions included, each group highest score first. Data only, no pick (tools/eddie_bybody.py).')


def md(race, r, bodies):
    out = [f"# {race} — {r['name']['H']} / {r['name']['J'].split(' ', 1)[1]}, body by body", '',
           RULES, '']
    for ch in r.get('missing', []):
        out += [f"No birth date for the {'horse' if ch == 'H' else 'jockey'} in the workbook: no {ch} lines.", '']
    for b in bodies:
        out += [f"## {b['body']}", '', '| Line | Plane | Value | Score |', '|---|---|---|---|']
        out += [f"| {ln['line']} | {ln['plane']} | {ln['value']:.4f} | {score_text(ln['hits'])} |" for ln in b['lines']]
        out += ['', 'Sky lines on the same target:', '']
        if b['matches']:
            out += ['| Sky line | Plane | Value | Score | Matches |', '|---|---|---|---|---|']
            out += [f"| {m['line']} | {m['plane']} | {m['value']:.4f} | {txt(m['hit'])} | {m['matches']} |" for m in b['matches']]
        else:
            out.append('none')
        out += ['', f"Other scoring sky lines on {b['body']}:", '']
        if b['other']:
            out += ['| Sky line | Plane | Value | Score |', '|---|---|---|---|']
            out += [f"| {o['line']} | {o['plane']} | {o['value']:.4f} | {score_text(o['hits'])} |" for o in b['other']]
        else:
            out.append('none')
        out.append('')
    return '\n'.join(out) + '\n'


GREEN, YELLOW, LIGHT = 'C6EFCE', 'FFEB9C', 'FFF7D6'
FILL_BODY, FILL_HEAD, FILL_SUB = 'BDD7EE', 'D9D9D9', 'F2F2F2'


def _fill(score):
    return GREEN if score >= 80 else YELLOW if score >= 50 else LIGHT


def _tlab(h):
    return {'whole': h[1], 'conj': 'conj', 'opposition': '180', 'contraparallel': 'cp'}.get(h[0], h[1])


def write_xlsx(path, race, res):
    """One workbook per race, one sheet per runner (same content and order as the .md): per body a band row, then the three tables.
    Columns: Line, Plane, Value, Family, Target, Score, Also (other families), Matches (sky lines on the same target only).
    Score cells filled green >= 80, yellow 50-80, light < 50."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook()
    wb.remove(wb.active)
    bold = Font(bold=True)
    fill = lambda c: PatternFill('solid', fgColor=c)
    for c, (r, bodies) in res.items():
        nm = r['name']['H'].split(' ', 1)[1] if ' ' in r['name']['H'] else r['name']['H']
        ws = wb.create_sheet(re.sub(r'[\\/*?:\[\]]', '', f"{int(c):02d} {nm}")[:31])
        ws.append([f"{race} — {r['name']['H']} / {r['name']['J'].split(' ', 1)[-1]}, body by body"])
        ws['A1'].font = Font(bold=True, size=12)
        ws.append([RULES])
        for ch in r.get('missing', []):
            ws.append([f"No birth date for the {'horse' if ch == 'H' else 'jockey'} in the workbook: no {ch} lines."])
        head = ['Line', 'Plane', 'Value', 'Family', 'Target', 'Score', 'Also', 'Matches']

        def table(title, rows, matches=False):
            ws.append([title])
            ws.cell(ws.max_row, 1).font = bold
            for k in range(1, 9):
                ws.cell(ws.max_row, k).fill = fill(FILL_SUB)
            if not rows:
                ws.append(['none'])
                return
            ws.append(head)
            for k in range(1, 9):
                ws.cell(ws.max_row, k).font = bold
                ws.cell(ws.max_row, k).fill = fill(FILL_HEAD)
            for line, plane, value, hs, m in rows:
                h = hs[0] if hs else None
                also = '; '.join(txt(x) for x in hs[1:]) if hs else ''
                ws.append([line, plane, round(value, 6), h[0] if h else '', _tlab(h) if h else '',
                           round(h[2], 2) if h else None, also, m or ''])
                if h:
                    ws.cell(ws.max_row, 6).fill = fill(_fill(h[2]))
                ws.cell(ws.max_row, 3).number_format = '0.0000'
                ws.cell(ws.max_row, 6).number_format = '0.0'

        for b in bodies:
            ws.append([])
            ws.append([b['body']])
            for k in range(1, 9):
                ws.cell(ws.max_row, k).fill = fill(FILL_BODY)
            ws.cell(ws.max_row, 1).font = Font(bold=True, size=12)
            table('Lines', [(l['line'], l['plane'], l['value'], l['hits'], None) for l in b['lines']])
            table('Sky lines on the same target', [(m['line'], m['plane'], m['value'], [m['hit']], m['matches'])
                                                   for m in b['matches']])
            table(f"Other scoring sky lines on {b['body']}", [(o['line'], o['plane'], o['value'], o['hits'], None) for o in b['other']])
        for col, w in zip('ABCDEFGH', (26, 20, 11, 12, 11, 8, 46, 34)):
            ws.column_dimensions[col].width = w
        ws['A2'].alignment = Alignment(wrap_text=False)
        ws.freeze_panes = 'A3'
    wb.save(path)


def run(path):
    runners, tt, tp = load(path)
    sky = sky_lines(tt, tp)
    return {c: (r, runner_view(r, tt, tp, sky)) for c, r in sorted(runners.items())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('active')
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'docs', 'eddie_read', 'bybody'))
    a = ap.parse_args()
    race = re.sub(r'^race_batch_|_active\.xlsx$', '', os.path.basename(a.active))
    d = os.path.join(a.out, race)
    os.makedirs(d, exist_ok=True)
    res = run(a.active)
    js = {}
    for c, (r, bodies) in res.items():
        nm = r['name']['H'].split(' ', 1)[1] if ' ' in r['name']['H'] else r['name']['H']
        fn = os.path.join(d, f"{int(c):02d}_{re.sub(r'[^A-Za-z0-9]+', '_', nm).strip('_')}.md")
        with open(fn, 'w') as f:
            f.write(md(race, r, bodies))
        js[str(c)] = {'name': r['name'], 'missing': r.get('missing', []), 'bodies': bodies}
    with open(os.path.join(d, f'{race}_bybody.json'), 'w') as f:
        json.dump(js, f, ensure_ascii=False, indent=1)
    write_xlsx(os.path.join(d, f'{race}_bybody.xlsx'), race, res)
    print(f'{race}: {len(res)} runners -> {d}')


if __name__ == '__main__':
    main()
