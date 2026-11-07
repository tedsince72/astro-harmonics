#!/usr/bin/env python3
"""eddie_layers.py - stage 2 of Eddie's race read: fixed layers, every runner, no judgement, no ranking, no pick.

Usage:  python3 tools/eddie_layers.py <race>_eddie_read.json [--active <race>_active.xlsx] [--out DIR]

Input: the stage 1 json written by tools/eddie_read.py (every piece: layer, chart, source, body, plane, value, target,
family, score, sky_number, circle, note) and, for layer 0, the race's _active.xlsx (runner names only). Never the csv.
Writes <race>_layers.md and <race>_layers.json.

Built 7 Nov 2026 on Eddie's go-ahead ("everything needs to be scripted"; claude/race-read-instruction.md). The layers:
  L0 field       runners in the tables workbook vs the _active.xlsx (odd P sheets, A1 = '<cloth> <horse>'); cloth gaps
  L1 same bodies every sky X -> natal X cell of the runner, scoring and loose, H and J
  L2 landings    for each same body (chart, body): every other piece of the runner on that natal body (same chart, then
                 the other chart), each tagged with the centre(s) it comes from (see 'centre of a piece'), plus the noted
                 sky lines from a centre to the sky body X (body lines)
  L3 seven cases each a fixed test (race-read-instruction Part 2):
                 1 same body on both charts   (the body has a same-body cell in H and in J; loose counts)
                 2 one body in both planes    (same chart, RA and Dec same-body cells)
                 3 runner number = sky number (a piece the stage 1 report tagged with a sky number)
                 4 circle divisions           (a piece whose target is a whole number dividing 360, scoring >= 50 or a
                                               same-body cell)
                 5 same number, several places (same family and target on two or more different (chart, body, source),
                                               scoring >= 50 or a same-body cell (loose counts); and N with N x phi on one
                                               natal body, scoring >= 50)
                 6 star and sky line on one body (a natal body conj a noted star (star row, conj, >= 50) and a centre's
                                               own line onto that natal body (top rows S centre -> natal body), any score)
                 7 centres meeting            (a natal body reached by 2 or 3 centres, see below; per chart and over both)
  L5 field       every L3 item carries 'only' or 'also: <runners>' by a fixed key (listed per case in KEYS)

Centre of a piece (fixed rules):
  top rows 'S Jupiter / S Sun / S Moon -> natal X'  -> that centre (direct)
  top rows 'S X -> natal Jupiter'                   -> Jupiter (natal Jupiter); and any centre with a noted line to X
  star rows '<chart> star -> natal X'               -> the centre(s) whose noted line or conj point is that star
                                                       (also 'S star -> natal Jupiter'; no Jupiter centre added)
  T1 / T2 'natal Jupiter -> X'                       -> Jupiter (natal Jupiter)
  same body 'S X -> natal X'                         -> any centre with a noted line to X (body line); a same-body cell
                                                       is not itself a centre
  A piece counts for L2 / L7 when it has a score (any score) or is a loose same-body cell.
Nothing here weighs, counts toward a total, ranks or picks. Rules change only with Eddie.
"""
import argparse
import json
import os
import re
from collections import defaultdict

import openpyxl

CENTRES = ('Jupiter', 'Sun', 'Moon')
CASE_NAMES = {
    1: 'same body on both charts',
    2: 'one body in both planes',
    3: 'runner number = sky number',
    4: 'circle divisions',
    5: 'same number in more than one place',
    6: 'star and sky line on one body',
    7: 'centres meeting',
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
    star_centre = d.get('star_centre', {})
    lines = d['lines']
    line_to = defaultdict(set)          # sky point -> centres with a noted line to it
    for l in lines:
        line_to[l['point']].add(l['centre'])

    def centres_of(p):
        src = p['source']
        s = src.split(' ', 1)[1] if ' ' in src else src
        out = set()
        if p['layer'] == 'top rows':
            if src.startswith('S ') and s in CENTRES:
                out.add(s)
            if p['body'] == 'Jupiter':
                out.add('Jupiter')
                out |= line_to.get(s, set())
        elif p['layer'] == 'star rows':
            out |= set(star_centre.get(s, []))
            out |= line_to.get(s, set())
        elif p['layer'] in ('T1', 'T2'):
            out.add('Jupiter')
        elif p['layer'] == 'same body':
            out |= line_to.get(p['body'], set())
        return out

    pieces = [dict(p, centres=sorted(centres_of(p))) for p in d['pieces'] if counts(p)]
    for p in pieces:
        p['text'] = cell(p)
    by_r = defaultdict(list)
    for p in pieces:
        by_r[p['runner']].append(p)

    # ---------------- L0 field
    l0 = {'tables': [names[r] for r in runners], 'missing_in_tables': [], 'cloth_gaps': [], 'active_read': bool(active)}
    cloths = sorted(int(names[r].split()[0]) for r in runners)
    if cloths:
        l0['cloth_gaps'] = [c for c in range(1, max(cloths) + 1) if c not in cloths]
    if active:
        for c, h in sorted(active.items()):
            if c not in cloths:
                l0['missing_in_tables'].append(f'{c} {h}')

    # ---------------- per runner L1, L2, L3 items (keys for the field)
    R = {}
    items = []        # (case, runner, key, text, cells)
    for r in runners:
        mine = by_r[r]
        sb = [p for p in mine if p['layer'] == 'same body']
        sb_bodies = list(dict.fromkeys((p['chart'], p['body']) for p in sb))
        l2 = []
        for ch, b in sb_bodies:
            own = [p for p in sb if p['chart'] == ch and p['body'] == b]
            same = [p for p in mine if p['layer'] != 'same body' and p['chart'] == ch and p['body'] == b]
            other_sb = [p for p in sb if p['chart'] != ch and p['body'] == b]
            other = [p for p in mine if p['layer'] != 'same body' and p['chart'] != ch and p['body'] == b]
            bl = [line_txt(l) for l in lines if l['point'] == b]
            l2.append(dict(chart=ch, body=b, same_body=[p['text'] for p in own],
                           body_lines=bl,
                           on_this_chart=[dict(text=p['text'], layer=p['layer'], centres=p['centres']) for p in same],
                           other_chart_same_body=[p['text'] for p in other_sb],
                           on_other_chart=[dict(text=p['text'], layer=p['layer'], centres=p['centres']) for p in other]))
        # case 1
        for b in dict.fromkeys(b for _, b in sb_bodies):
            hs = [p for p in sb if p['body'] == b and p['chart'] == 'H']
            js = [p for p in sb if p['body'] == b and p['chart'] == 'J']
            if hs and js:
                items.append((1, r, b, f'{b}', [p['text'] for p in hs + js]))
        # case 2
        for ch, b in sb_bodies:
            ps = [p for p in sb if p['chart'] == ch and p['body'] == b]
            if {'RA', 'Dec'} <= {p['plane'] for p in ps}:
                items.append((2, r, (ch, b), f'{ch} {b}', [p['text'] for p in ps]))
        # case 3
        for p in mine:
            if p.get('sky_number'):
                items.append((3, r, (p['target'], p['family']), f"{p['target']} {p['family']}",
                              [p['text'] + ' = ' + p['sky_number']]))
        # case 4
        for p in mine:
            if p['family'] == 'whole' and p['target'].isdigit() and int(p['target']) in DIV360 \
                    and (p['layer'] == 'same body' or (p['score'] or 0) >= 50):
                n = int(p['target'])
                items.append((4, r, n, f'{n} = 360/{360 // n}', [p['text']]))
        # case 5
        grp = defaultdict(list)
        for p in mine:
            if p['family'] != 'conj' and ((p['score'] is not None and p['score'] >= 50) or p['layer'] == 'same body'):
                grp[(p['family'], p['target'])].append(p)
        for (fam, tg), ps in grp.items():
            if len({(p['chart'], p['body'], p['source']) for p in ps}) >= 2:
                items.append((5, r, (fam, tg), f'{tg} {fam}', [p['text'] for p in ps]))
        byb = defaultdict(list)
        for p in mine:
            if p['score'] is not None and p['score'] >= 50:
                byb[(p['chart'], p['body'])].append(p)
        for (ch, b), ps in byb.items():
            wh = {p['target']: p for p in ps if p['family'] == 'whole'}
            for p in ps:
                m = re.fullmatch(r'(\d+)×φ', p['target']) if p['family'] == 'golden' else None
                if m and m.group(1) in wh:
                    items.append((5, r, ('N and N×φ', ch, b), f"{m.group(1)} and {p['target']} on {ch} {b}",
                                  [wh[m.group(1)]['text'], p['text']]))
        # case 6
        for p in mine:
            if p['layer'] == 'star rows' and p['family'] == 'conj' and (p['score'] or 0) >= 50:
                st = p['source'].split(' ', 1)[1]
                if st not in star_centre and st not in line_to:
                    continue
                direct = [q for q in mine if q['layer'] == 'top rows' and q['chart'] == p['chart']
                          and q['body'] == p['body'] and q['source'] in ('S Jupiter', 'S Sun', 'S Moon')]
                if direct:
                    items.append((6, r, (st, p['body']), f"{p['chart']} {p['body']} on {st}",
                                  [p['text']] + [q['text'] for q in direct]))
        # case 7
        bodies = defaultdict(lambda: defaultdict(list))   # body -> centre -> texts (both charts)
        for p in mine:
            for c in p['centres']:
                bodies[p['body']][c].append(p['text'])
        for b, cs in bodies.items():
            if b.startswith('star '):
                continue
            if len(cs) >= 2:
                key = (b, tuple(sorted(cs)))
                items.append((7, r, key, f"{b}: {', '.join(sorted(cs))}",
                              [f'[{c}] ' + t for c in sorted(cs) for t in cs[c]]))
        R[r] = dict(name=names[r], same_bodies=[p['text'] for p in sb], landings=l2)

    # ---------------- L5 field tags
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
    return dict(workbook=d.get('workbook'), l0=l0, runners=runners, report=R,
                sky=dict(top=d.get('top'), hubs=d.get('hubs'), lines=[line_txt(l) for l in lines]))


def write_md(D, path):
    o = []
    o.append(f"# Stage 2 layers: {os.path.basename(D['workbook'] or '')}")
    o.append('Fixed layers for every runner; no judgement, no ranking, no pick (tools/eddie_layers.py).\n')
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
    for r in D['runners']:
        x = D['report'][r]
        o.append(f"\n## {x['name']}")
        o.append('### L1 same bodies')
        o += [f'- {t}' for t in x['same_bodies']] or ['- none']
        o.append('### L2 what lands on each same body')
        for L in x['landings']:
            o.append(f"- **{L['chart']} {L['body']}** (same body: {'; '.join(L['same_body'])})")
            for t in L['body_lines']:
                o.append(f'  - body line: {t}')
            for q in L['on_this_chart']:
                o.append(f"  - {q['layer']}: {q['text']}" + (f" [{', '.join(q['centres'])}]" if q['centres'] else ''))
            for t in L['other_chart_same_body']:
                o.append(f'  - other chart, same body: {t}')
            for q in L['on_other_chart']:
                o.append(f"  - other chart, {q['layer']}: {q['text']}" + (f" [{', '.join(q['centres'])}]" if q['centres'] else ''))
        o.append('### L3 the seven cases (L5 field tag on each)')
        for c, nm in CASE_NAMES.items():
            its = x['cases'][str(c)]
            o.append(f'- **{c}. {nm}**' + ('' if its else ': none'))
            for it in its:
                o.append(f"  - {it['label']} — {it['field']}")
                for t in it['cells']:
                    o.append(f'    - {t}')
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
