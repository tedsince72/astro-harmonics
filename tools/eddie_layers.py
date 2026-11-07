#!/usr/bin/env python3
"""eddie_layers.py - stage 2 of Eddie's race read: the stage 1 data laid out in fixed layers, every runner. It shows the
data only: no interpretation, no weighing, no score cut-offs, no ranking, no pick (Eddie, 7 Nov 2026: "I just want to show the
data"). Rules come later, beyond stage 2 (stage 3).

Usage:  python3 tools/eddie_layers.py <race>_eddie_read.json [--active <race>_active.xlsx] [--out DIR]

Input: the stage 1 json written by tools/eddie_read.py and, for L0, the race's _active.xlsx (runner names only). Never the csv.
Writes <race>_layers.md and <race>_layers.json.

A cell is every stage 1 piece with a score (any score) and every loose same-body cell (Eddie's underline: its nearest
target is shown with '(loose)' and it takes part in the L3 matches on that target). The same connection carried by two stage 1
layers (e.g. 'same body' and 'top rows' for S Jupiter -> natal Jupiter) is shown once, with both layer names. Beside each cell whose source is a sky
point or a star, its own noted sky lines are copied from the sky notes ('source line: S Moon -> Rigel ...'): the source of
'J Rigel -> J Ketu' is Rigel, of 'S Chiron -> J Jupiter' Chiron, of the same body 'S Ketu -> H Ketu' Ketu; a source that is S
Jupiter / S Sun / S Moon is itself a centre and gets none. Nothing is tagged or grouped by centre.

  L0 field         runners in the tables workbook vs the _active.xlsx (odd P sheets, A1 = '<cloth> <horse>'); cloth gaps
  L1 same bodies   every sky X -> natal X cell of the runner, H and J
  L2 same bodies   for each same body (chart, body): the sky lines to X, every other cell of the runner on that natal body,
     landings      this chart then the other chart, each with its source lines
  L3 matches       plain matches, each with 'only' / 'also: <runners>' (same key in another runner):
                   1 same body on both charts     the body has a same-body cell in H and in J          key: body
                   2 one body in both planes      same chart, RA and Dec same-body cells                key: chart, body
                   3 runner number = sky number   a cell stage 1 tagged with a sky number               key: target, family
                   4 circle divisions             a whole target dividing 360                           key: the number
                   5 same number, several places  same family and target on 2+ different (chart, body,  key: family, target
                                                  source), not conj; N and N x phi on one natal body     key: N, chart, body
  L4 every body    every natal body of the runner (both charts) with every cell on it and the source lines (T1 / T2
                   natal Jupiter -> star cells under Jupiter); each cell
                   'only' / 'also: <runners>' for the same source onto the same body, any chart, plane or number (source:
                   a star with the chart letter dropped; a top-rows sky source as written, e.g. 'S Sun', 'S Chiron';
                   'natal Jupiter' for T1 / T2; 'same body')
"""
import argparse
import json
import os
import re
from collections import defaultdict

import openpyxl

CASE_NAMES = {
    1: 'same body on both charts',
    2: 'one body in both planes',
    3: 'runner number = sky number',
    4: 'circle divisions',
    5: 'same number in more than one place',
}
DIV360 = {n for n in range(1, 361) if 360 % n == 0}


def sc(p):
    return 'loose' if p['score'] is None else f"{p['score']:.2f}"


def cell(p):
    fam = 'conj' if p['family'] == 'conj' else f"{p['target']} {p['family']}"
    return f"{p['source']} → {p['chart']} {p['body']} {p['plane']} {p['value']:.4f} {fam} ({sc(p)})"


def line_txt(l):
    fam = 'conj' if l['family'] == 'conj' else f"{l['target']} {l['family']}"
    return f"S {l['centre']} → {l['point']} {l['plane']} {l['value']:.4f} {fam} ({l['score']:.2f})"


def counts(p):
    return p['score'] is not None or (p['layer'] == 'same body' and p['note'] == 'loose')


def active_names(path):
    """Runner names from the _active.xlsx: odd P sheets, cell A1 '<cloth> <horse>'."""
    wb = openpyxl.load_workbook(path, read_only=True)
    out = {}
    for ws in wb.worksheets:
        m = re.fullmatch(r'P(\d+)', ws.title)
        if not m or int(m.group(1)) % 2 == 0:
            continue
        a1 = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]
        if a1:
            mm = re.match(r'\s*(\d+)\s+(.*)', str(a1))
            if mm:
                out[int(mm.group(1))] = mm.group(2).strip()
    return out


def build(d, active=None):
    names = d['names']
    runners = d['runners']
    lines = d['lines']
    lines_of = defaultdict(list)          # sky point -> its noted lines (text)
    for l in lines:
        lines_of[l['point']].append(line_txt(l))

    def src_name(p):
        s = p['source'].split(' ', 1)[1] if ' ' in p['source'] else p['source']
        return s

    def src_key(p):
        if p['layer'] in ('T1', 'T2'):
            return 'natal Jupiter'
        if p['layer'].startswith('same body'):
            return 'same body'
        if p['source'].startswith('S ') and p['layer'] == 'top rows':
            return p['source']
        return src_name(p)

    def src_lines(p):
        s = src_name(p)
        if p['source'] in ('S Jupiter', 'S Sun', 'S Moon'):
            return []
        if p['layer'] in ('T1', 'T2'):        # natal Jupiter -> X
            return []
        if p['layer'].startswith('same body'):
            return lines_of.get(p['body'], [])
        return lines_of.get(s, [])

    pieces = []
    seen_conn = {}
    for p in d['pieces']:
        if counts(p):
            conn = (p['runner'], p['source'], p['chart'], p['body'], p['plane'], round(p['value'], 6))
            if conn in seen_conn:                   # the same connection carried by two stage 1 layers: shown once
                seen_conn[conn]['layer'] += ' + ' + p['layer']
                continue
            q = dict(p)
            q['text'] = cell(p)
            q['source_lines'] = src_lines(p)
            seen_conn[conn] = q
            pieces.append(q)
    by_r = defaultdict(list)
    for p in pieces:
        by_r[p['runner']].append(p)

    def cj(p):
        return dict(text=p['text'], layer=p['layer'], source_lines=p['source_lines'])

    # ---------------- L0 field
    l0 = {'tables': [names[r] for r in runners], 'missing_in_tables': [], 'cloth_gaps': [], 'active_read': bool(active)}
    cloths = sorted(int(names[r].split()[0]) for r in runners)
    if cloths:
        l0['cloth_gaps'] = [c for c in range(1, max(cloths) + 1) if c not in cloths]
    if active:
        for c, h in sorted(active.items()):
            if c not in cloths:
                l0['missing_in_tables'].append(f'{c} {h}')

    R = {}
    items = []        # (case, runner, key, label, cells)
    l4keys = defaultdict(set)
    for r in runners:
        mine = by_r[r]
        sb = [p for p in mine if p['layer'].startswith('same body')]
        sb_bodies = list(dict.fromkeys((p['chart'], p['body']) for p in sb))
        l2 = []
        for ch, b in sb_bodies:
            own = [p for p in sb if p['chart'] == ch and p['body'] == b]
            l2.append(dict(chart=ch, body=b, same_body=[p['text'] for p in own], body_lines=lines_of.get(b, []),
                           on_this_chart=[cj(p) for p in mine if not p['layer'].startswith('same body') and p['chart'] == ch and p['body'] == b],
                           other_chart_same_body=[p['text'] for p in sb if p['chart'] != ch and p['body'] == b],
                           on_other_chart=[cj(p) for p in mine if not p['layer'].startswith('same body') and p['chart'] != ch and p['body'] == b]))
        # 1
        for b in dict.fromkeys(b for _, b in sb_bodies):
            hs = [p for p in sb if p['body'] == b and p['chart'] == 'H']
            js = [p for p in sb if p['body'] == b and p['chart'] == 'J']
            if hs and js:
                items.append((1, r, b, b, [p['text'] for p in hs + js]))
        # 2
        for ch, b in sb_bodies:
            ps = [p for p in sb if p['chart'] == ch and p['body'] == b]
            if {'RA', 'Dec'} <= {p['plane'] for p in ps}:
                items.append((2, r, (ch, b), f'{ch} {b}', [p['text'] for p in ps]))
        # 3
        for p in mine:
            if p.get('sky_number'):
                items.append((3, r, (p['target'], p['family']), f"{p['target']} {p['family']}",
                              [p['text'] + ' = ' + p['sky_number']]))
        # 4
        for p in mine:
            if p['family'] == 'whole' and p['target'].isdigit() and int(p['target']) in DIV360:
                n = int(p['target'])
                items.append((4, r, n, f'{n} = 360/{360 // n}', [p['text']]))
        # 5
        grp = defaultdict(list)
        for p in mine:
            if p['family'] != 'conj':
                grp[(p['family'], p['target'])].append(p)
        for (fam, tg), ps in grp.items():
            if len({(p['chart'], p['body'], p['source']) for p in ps}) >= 2:
                items.append((5, r, (fam, tg), f'{tg} {fam}', [p['text'] for p in ps]))
        byb = defaultdict(list)
        for p in mine:
            byb[(p['chart'], p['body'])].append(p)
        for (ch, b), ps in byb.items():
            wh = defaultdict(list)
            for p in ps:
                if p['family'] == 'whole':
                    wh[p['target']].append(p)
            for p in ps:
                m = re.fullmatch(r'(\d+)×φ', p['target']) if p['family'] == 'golden' else None
                if m and m.group(1) in wh:
                    items.append((5, r, ('N and N×φ', m.group(1), ch, b), f"{m.group(1)} and {p['target']} on {ch} {b}",
                                  [q['text'] for q in wh[m.group(1)]] + [p['text']]))
        # L4
        def l4body(p):                          # natal Jupiter -> star (T1 / T2) sits on natal Jupiter
            return 'Jupiter' if p['body'].startswith('star ') else p['body']
        bodies = list(dict.fromkeys(l4body(p) for p in mine))
        l4 = []
        for b in bodies:
            cs = [p for p in mine if l4body(p) == b]
            for p in cs:
                l4keys[(src_key(p), b)].add(r)
            l4.append(dict(body=b, cells=[dict(cj(p), key=(src_key(p), b)) for p in cs]))
        R[r] = dict(name=names[r], same_bodies=[p['text'] for p in sb], landings=l2, bodies=l4)

    # ---------------- field tags
    held = defaultdict(set)
    for case, r, key, _, _ in items:
        held[(case, key)].add(r)
    out_items = defaultdict(lambda: defaultdict(list))
    seen = set()
    for case, r, key, label, cells_ in items:
        k = (case, r, key, label, tuple(cells_))
        if k in seen:
            continue
        seen.add(k)
        others = sorted(held[(case, key)] - {r})
        field = 'only' if not others else 'also: ' + ', '.join(names[o] for o in others)
        out_items[r][case].append(dict(label=label, cells=list(cells_), field=field))
    for r in runners:
        R[r]['cases'] = {str(c): out_items[r].get(c, []) for c in CASE_NAMES}
        for B in R[r]['bodies']:
            for c in B['cells']:
                others = sorted(l4keys[c['key']] - {r})
                c['field'] = 'only' if not others else 'also: ' + ', '.join(names[o] for o in others)
                c['key'] = list(c['key'])
    return dict(workbook=d.get('workbook'), l0=l0, runners=runners, report=R,
                sky=dict(hubs=d.get('hubs'), lines=[line_txt(l) for l in lines]))


def write_md(D, path):
    o = []
    o.append(f"# Stage 2 layers: {os.path.basename(D['workbook'] or '')}")
    o.append('The stage 1 data laid out in fixed layers for every runner; data only, no interpretation, no ranking, no pick '
             '(tools/eddie_layers.py).\n')
    l0 = D['l0']
    o.append('## L0 field')
    o.append(f"- In the tables workbook ({len(l0['tables'])}): " + '; '.join(l0['tables']))
    if l0.get('active_read'):
        o.append('- Missing from the tables workbook (in the _active.xlsx): ' + ('; '.join(l0['missing_in_tables']) or 'none'))
    else:
        o.append('- _active.xlsx not found: runners not checked against it')
    o.append('- Cloth numbers not in the tables workbook: ' + (', '.join(map(str, l0['cloth_gaps'])) or 'none'))
    o.append('\n## Sky (noted lines)')
    for t in D['sky']['lines']:
        o.append(f'- {t}')
    o.append('- Hubs: ' + (', '.join(D['sky']['hubs']) or 'none'))

    def cl(q, pre=''):
        s = f"  - {pre}{q['layer']}: {q['text']}"
        if q.get('field'):
            s += f" — {q['field']}"
        out = [s]
        for t in q['source_lines']:
            out.append(f'    - source line: {t}')
        return out
    for r in D['runners']:
        x = D['report'][r]
        o.append(f"\n## {x['name']}")
        o.append('### L1 same bodies')
        o += [f'- {t}' for t in x['same_bodies']] or ['- none']
        o.append('### L2 what lands on each same body')
        for L in x['landings']:
            o.append(f"- **{L['chart']} {L['body']}** (same body: {'; '.join(L['same_body'])})")
            for t in L['body_lines']:
                o.append(f'  - sky line to {L["body"]}: {t}')
            for q in L['on_this_chart']:
                o += cl(q)
            for t in L['other_chart_same_body']:
                o.append(f'  - other chart, same body: {t}')
            for q in L['on_other_chart']:
                o += cl(q, 'other chart, ')
        o.append('### L3 matches')
        for c, nm in CASE_NAMES.items():
            its = x['cases'][str(c)]
            o.append(f'- **{c}. {nm}**' + ('' if its else ': none'))
            for it in its:
                o.append(f"  - {it['label']} — {it['field']}")
                for t in it['cells']:
                    o.append(f'    - {t}')
        o.append('### L4 every natal body')
        for B in x['bodies']:
            o.append(f"- **{B['body']}**")
            for q in B['cells']:
                o += cl(q)
    with open(path, 'w') as f:
        f.write('\n'.join(o) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('json')
    ap.add_argument('--active')
    ap.add_argument('--out')
    a = ap.parse_args()
    d = json.load(open(a.json))
    act = None
    if a.active:
        act = active_names(a.active)
    else:
        nm = re.sub(r'_jupiter_tables\.xlsx$', '_active.xlsx', os.path.basename(d.get('workbook') or ''))
        repo = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
        for guess in (os.path.join(os.path.dirname(os.path.abspath(a.json)), nm),
                      os.path.join(repo, 'reference', 'classic', nm)):
            if nm and os.path.exists(guess):
                act = active_names(guess)
                break
    D = build(d, act)
    base = os.path.basename(a.json).replace('_eddie_read.json', '')
    out = a.out or os.path.dirname(a.json)
    write_md(D, os.path.join(out, base + '_layers.md'))
    with open(os.path.join(out, base + '_layers.json'), 'w') as f:
        json.dump(D, f, indent=1, ensure_ascii=False)
    print(os.path.join(out, base + '_layers.md'))


if __name__ == '__main__':
    main()
