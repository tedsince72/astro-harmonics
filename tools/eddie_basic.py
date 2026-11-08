#!/usr/bin/env python3
"""eddie_basic.py - the basic view (Eddie, 8 Nov 2026): what a runner's charts hold, read from the race's _active.xlsx only, the
P##_DIST tabs only, natal -> natal and sky (transit) -> natal only, bodies and the four royal stars only (no other stars, no equator,
no Ascendant / Midheaven / Vertex / Part points, no natal Moon; the sky Moon is kept). Data only: no ranking, no pick. Never reads the
csv or any result.

Royal stars (Eddie, 8 Nov 2026: "just include the 4 royal stars Aldebaran, Antares, Fomalhaut & Regulus"): a natal royal star is a natal
point like a body: natal star - natal body cells (no star - star pair: it is the same for everyone) and sky body -> natal star cells. Sky
star rows are left out (a star barely moves, so sky star -> natal X repeats natal star - natal X). A sky body -> natal star cell is about
the same in the horse's and the jockey's chart and for every runner (a sky line), so it is left out of the checks that compare the two
charts on one sky cell (2a, 2b, 4, 5, 7, 13, 15); it takes part everywhere else.

Usage:  python3 tools/eddie_basic.py <race>_active.xlsx [--out DIR]       (default DIR docs/eddie_read/basic)
Writes <race>_basic.md and <race>_basic.json.

A cell = one distance of the _DIST tab: natal A - natal B of one chart (each pair once, the chart's own Rahu - Ketu left out) or
sky A -> natal B (sky body on the row, natal body on the column), plane RA or Dec, scored on tools/families.py (families.best;
the cell's best family, target and score; a cell with no family score is not a cell). Chart H = the horse (odd P sheet), J = the
jockey (even P sheet), runner = cloth. Cell text: 'S A -> H B RA 179.4564 10xphi^6 (96.98)' or 'H A - H B ...'.

Checks (Eddie, 8 Nov 2026, from the Newcastle AW 16:33 2 Aug 2021 read); each item 'only' or 'also: <runners>' (another runner
with the same key):
  1 natal pair, same number, both charts   the same natal pair A - B scores the same family + target in H and in J (any plane,
                                            any score)                                               key: pair, target
  2 sky X on natal Y, both charts           sky X reaches natal Y in H and in J; (a) the same family + target (any score),
                                            (b) any targets, both >= 80                             key: X, Y (+ target)
  3 sky X on both natal Jupiters            sky X reaches H Jupiter and J Jupiter, both >= 80       key: X
  4 sky X, same number, both charts         sky X scores the same family + target on an H body and a J body, both >= 80
                                                                                                     key: X, target
  5 number swap                             targets t1, t2 and natal bodies P, Q: t1 on H P and J Q, t2 on J P and H Q
                                            (P != Q, t1 != t2, every cell >= 80; the natal body = the column of a sky cell,
                                            either end of a natal cell)                             key: {P, Q}, {t1, t2}
  6 centre on a body tied to natal Jupiter  sky Jupiter / Sun / Moon reaches natal X (>= 50) and the same chart's natal
                                            Jupiter - X scores >= 50 (X not Jupiter)               key: centre, chart, X
  7 numbers in both charts (background)     every family + target (not conj) with a cell >= 80 in H and in J; count
                                                                                                     key: target
  8 axis                                    a chart whose natal Jupiter is conj a natal node (Jupiter - Rahu / Ketu best
                                            family conj, any score): sky X conj that chart's other node, or sky X -> that
                                            natal Jupiter RA within 1.5 of 180 (opposite; any value, scored or not)          key: chart, X
  9 natal Jupiter ties                      every natal Jupiter - X cell >= 50, per chart           key: chart, X, target
 10 N and N x phi                           a whole target N (>= 50) and the golden target N x phi (>= 50) in two cells,
                                            either chart                                            key: N
 11 values close together                  three or more cells (any score, both charts, not conj) within WINDOW of one another
                                            (max - min <= WINDOW) holding two or more different targets; each maximal run
                                            once                                                    key: the run's targets
 12 digits across decades                   two cells (any score, either chart) on whole targets N and 10 N (or 100 N)
                                                                                                     key: N
 13 one body pair, every layer              a body pair {A, B}: the cells natal H A - B, natal J A - B, S A -> H B,
                                            S B -> H A, S A -> J B, S B -> J A (any score; not Rahu - Ketu); two or more of them on the same
                                            whole digits (N, 10 N, 100 N) or the same family + target  key: pair, digits / target
 15 sky X on natal Y, crossed planes     sky X reaches natal Y in H and in J, one cell RA and the other Dec, both >= 80 (Eddie,
                                            8 Nov 2026, from Athmad / Pholas / Greaneteen: S Ceres -> H Mars RA 138, -> J Mars
                                            Dec 2)                                                   key: X, Y
 14 sky Jupiter repeats natal Jupiter       same chart: natal Jupiter - X and sky Jupiter -> Y on the same family + target,
                                            both >= 50, not conj (Eddie, 8 Nov 2026, from Pholas: H Jupiter - H Uranus Dec
                                            14.4459 and S Jupiter -> H Chiron Dec 14.4461, 14.4444)  key: chart, target
"""
import argparse, collections, json, os, sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import families as F  # noqa: E402

BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Moon', 'Rahu', 'Ketu',
          'Ceres', 'Pallas', 'Juno', 'Vesta', 'Chiron', 'Eris', 'Gonggong', 'Haumea', 'Makemake', 'Orcus', 'Quaoar', 'Sedna',
          'Transpluto']
ROYAL = ['Aldebaran', 'Antares', 'Fomalhaut', 'Regulus']
POINTS = BODIES + ROYAL
HIGH = 80
MID = 50
WINDOW = 0.3
CENTRES = ('Jupiter', 'Sun', 'Moon')


def load(path):
    """-> {cloth: {'name': {'H': .., 'J': ..}, 'cells': [cell dict]}}"""
    wb = openpyxl.load_workbook(path, read_only=True)
    meta = [r for r in wb['META'].iter_rows(values_only=True) if r and isinstance(r[0], str) and r[0][:1] == 'P'
            and r[0][1:].isdigit()]
    out = {}
    for tab, role, cloth, name, *_ in meta:
        ch = 'H' if role == 'horse' else 'J'
        rows = list(wb[tab + '_DIST'].iter_rows(values_only=True))
        r = out.setdefault(cloth, {'name': {}, 'cells': [], 'opp': []})
        r['name'][ch] = name if ch == 'H' else name.split(' ', 1)[1]
        for i, row in enumerate(rows):
            t = row[0]
            if not (isinstance(t, str) and '—' in t):
                continue
            kind = 'N' if t.startswith('NATAL') else 'S'
            plane = 'RA' if 'RA distances' in t else 'Dec'
            hdr = rows[i + 1]
            cols = {h: j for j, h in enumerate(hdr) if h in POINTS and h != 'Moon'}
            for row2 in rows[i + 2:]:
                a = row2[0]
                if a is None or (isinstance(a, str) and '—' in a):
                    break
                if a not in (POINTS if kind == 'N' else BODIES) or (kind == 'N' and a == 'Moon'):
                    continue
                for b, j in cols.items():
                    if kind == 'N' and (POINTS.index(b) <= POINTS.index(a) or {a, b} == {'Rahu', 'Ketu'}
                                        or (a in ROYAL and b in ROYAL)):
                        continue
                    v = row2[j]
                    if not isinstance(v, (int, float)) or v <= 0:
                        continue
                    bst = F.best(v, plane)
                    if kind == 'S' and plane == 'RA' and b == 'Jupiter' and v > 180 - 1.5:
                        bo = bst or {'family': 'none', 'target': '-', 'score': 0.0}
                        r['opp'].append({'ch': ch, 'kind': kind, 'plane': plane, 'a': a, 'b': b, 'v': float(v),
                                         'family': bo['family'], 'target': bo['target'], 'score': bo['score']})
                    if bst:
                        r['cells'].append({'ch': ch, 'kind': kind, 'plane': plane, 'a': a, 'b': b, 'v': float(v),
                                           'family': bst['family'], 'target': bst['target'], 'score': bst['score'],
                                           'shared': kind == 'S' and b in ROYAL})
    return out


def text(c):
    if c['family'] == 'none':
        return f"S {c['a']} → {c['ch']} {c['b']} {c['plane']} {c['v']:.4f} (no family)"
    src = ('S ' if c['kind'] == 'S' else c['ch'] + ' ') + c['a']
    arrow = '→' if c['kind'] == 'S' else '–'
    return f"{src} {arrow} {c['ch']} {c['b']} {c['plane']} {c['v']:.4f} {c['target']} {c['family']} ({c['score']:.2f})"


def tkey(c):
    return (c['family'], c['target'])


def whole_n(c):
    return int(c['target']) if c['family'] == 'whole' else None


def digits(n):
    while n % 10 == 0 and n > 0:
        n //= 10
    return n


def natal_bodies(c):
    return (c['b'],) if c['kind'] == 'S' else (c['a'], c['b'])


def runner_checks(cells, opp=()):
    """-> list of items {'check', 'key', 'cells': [text], 'note'}"""
    items = []
    add = lambda chk, key, cs, note='': items.append({'check': chk, 'key': key, 'cells': [text(c) for c in cs], 'note': note})
    H = [c for c in cells if c['ch'] == 'H']
    J = [c for c in cells if c['ch'] == 'J']
    Hs = [c for c in H if not c.get('shared')]          # sky -> natal royal star left out of the two-chart comparisons
    Js = [c for c in J if not c.get('shared')]
    # 1
    for h in H:
        if h['kind'] != 'N':
            continue
        for j in J:
            if j['kind'] == 'N' and (j['a'], j['b']) == (h['a'], h['b']) and tkey(j) == tkey(h):
                add(1, (h['a'], h['b'], h['target']), [h, j])
    # 2
    for h in Hs:
        if h['kind'] != 'S':
            continue
        for j in Js:
            if j['kind'] != 'S' or (j['a'], j['b']) != (h['a'], h['b']):
                continue
            if tkey(j) == tkey(h):
                add('2a', (h['a'], h['b'], h['target']), [h, j], 'same number')
            if h['score'] >= HIGH and j['score'] >= HIGH:
                add('2b', (h['a'], h['b']), [h, j], 'both >= 80')
    # 3
    for x in sorted({c['a'] for c in cells if c['kind'] == 'S'}, key=BODIES.index):
        hs = [c for c in H if c['kind'] == 'S' and c['a'] == x and c['b'] == 'Jupiter' and c['score'] >= HIGH]
        js = [c for c in J if c['kind'] == 'S' and c['a'] == x and c['b'] == 'Jupiter' and c['score'] >= HIGH]
        if hs and js:
            add(3, (x,), hs + js)
    # 4
    seen = set()
    for h in Hs:
        if h['kind'] != 'S' or h['score'] < HIGH:
            continue
        js = [j for j in Js if j['kind'] == 'S' and j['a'] == h['a'] and tkey(j) == tkey(h) and j['score'] >= HIGH]
        k = (h['a'], h['target'])
        if js and k not in seen:
            seen.add(k)
            hs = [c for c in Hs if c['kind'] == 'S' and c['a'] == h['a'] and tkey(c) == tkey(h) and c['score'] >= HIGH]
            add(4, k, hs + js)
    # 5
    hi = [c for c in cells if c['score'] >= HIGH and c['family'] != 'conj' and not c.get('shared')]
    on = collections.defaultdict(list)                  # (chart, natal body, target key) -> cells
    for c in hi:
        for b in natal_bodies(c):
            on[(c['ch'], b, tkey(c))].append(c)
    seen = set()
    for (ch1, p, t1), c1 in list(on.items()):
        if ch1 != 'H':
            continue
        for (ch2, q, t1b), c2 in list(on.items()):
            if ch2 != 'J' or t1b != t1 or q == p:
                continue
            for (ch3, p3, t2), c3 in list(on.items()):
                if ch3 != 'J' or p3 != p or t2 == t1:
                    continue
                c4 = on.get(('H', q, t2))
                if not c4:
                    continue
                k = (tuple(sorted((p, q))), tuple(sorted((t1[1], t2[1]))))
                if k in seen:
                    continue
                seen.add(k)
                add(5, k, [c1[0], c2[0], c3[0], c4[0]], f'{t1[1]} on H {p} and J {q}; {t2[1]} on J {p} and H {q}')
    # 6
    for ch, cs in (('H', H), ('J', J)):
        ties = {}
        for c in cs:
            if c['kind'] == 'N' and 'Jupiter' in (c['a'], c['b']) and c['score'] >= MID:
                ties.setdefault(c['b'] if c['a'] == 'Jupiter' else c['a'], []).append(c)
        for c in cs:
            if c['kind'] == 'S' and c['a'] in CENTRES and c['b'] != 'Jupiter' and c['b'] in ties and c['score'] >= MID:
                add(6, (c['a'], ch, c['b']), [c] + ties[c['b']])
    # 7
    hk = {tkey(c) for c in Hs if c['score'] >= HIGH and c['family'] != 'conj'}
    jk = {tkey(c) for c in Js if c['score'] >= HIGH and c['family'] != 'conj'}
    both = sorted(hk & jk)
    items.append({'check': 7, 'key': ('count', len(both)), 'cells': [f'{t} {f}' for f, t in both], 'note': f'{len(both)} numbers'})
    # 8
    for ch, cs in (('H', H), ('J', J)):
        for c in cs:
            if c['kind'] == 'N' and {c['a'], c['b']} in ({'Jupiter', 'Rahu'}, {'Jupiter', 'Ketu'}) and c['family'] == 'conj':
                node = 'Rahu' if 'Rahu' in (c['a'], c['b']) else 'Ketu'
                other = 'Ketu' if node == 'Rahu' else 'Rahu'
                for s in cs:
                    if s['kind'] == 'S' and s['b'] == other and s['family'] == 'conj':
                        add(8, (ch, s['a']), [c, s], f'sky {s["a"]} conj {ch} {other}, {ch} Jupiter conj {ch} {node}')
                for s in opp:
                    if s['ch'] == ch:
                        add(8, (ch, s['a']), [c, s], f'sky {s["a"]} opposite {ch} Jupiter, {ch} Jupiter conj {ch} {node}')
    # 9
    for c in cells:
        if c['kind'] == 'N' and 'Jupiter' in (c['a'], c['b']) and c['score'] >= MID:
            x = c['b'] if c['a'] == 'Jupiter' else c['a']
            add(9, (c['ch'], x, c['target']), [c])
    # 10
    wh = collections.defaultdict(list)
    gd = collections.defaultdict(list)
    for c in cells:
        if c['score'] < MID:
            continue
        if c['family'] == 'whole':
            wh[int(c['target'])].append(c)
        elif c['family'] == 'golden':
            gd[int(c['target'].split('×')[0])].append(c)
    for n in sorted(set(wh) & set(gd)):
        add(10, (n,), wh[n] + gd[n])
    # 11
    srt = sorted([c for c in cells if c['family'] != 'conj'], key=lambda c: c['v'])
    runs, i = [], 0
    for i0 in range(len(srt)):
        j = i0
        while j + 1 < len(srt) and srt[j + 1]['v'] - srt[i0]['v'] <= WINDOW:
            j += 1
        runs.append((i0, j))
    kept = []
    for i0, j in runs:
        if j - i0 + 1 < 3 or len({tkey(c) for c in srt[i0:j + 1]}) < 2:
            continue
        if kept and kept[-1][1] >= j:
            continue                                       # inside the previous run
        kept.append((i0, j))
    for i0, j in kept:
        cs = srt[i0:j + 1]
        add(11, tuple(sorted({c['target'] for c in cs})), cs, f'{cs[0]["v"]:.4f} - {cs[-1]["v"]:.4f}')
    # 12
    ws = [c for c in cells if c['family'] == 'whole']
    seen = set()
    for a in ws:
        for b in ws:
            na, nb = whole_n(a), whole_n(b)
            if nb in (10 * na, 100 * na) and (na, nb) not in seen:
                seen.add((na, nb))
                add(12, (na,), [x for x in ws if whole_n(x) in (na, nb)], f'{na} and {nb}')
    # 13
    for i, A in enumerate(POINTS):
        for B in POINTS[i + 1:]:
            if {A, B} == {'Rahu', 'Ketu'} or (A in ROYAL and B in ROYAL):
                continue                                   # the node axis mirrors itself
            cs = [c for c in cells if not c.get('shared') and (c['kind'] == 'N' and {c['a'], c['b']} == {A, B})
                  or not c.get('shared') and (c['kind'] == 'S' and (c['a'], c['b']) in ((A, B), (B, A)))]
            if len(cs) < 2:
                continue
            groups = collections.defaultdict(list)
            for c in cs:
                if c['family'] == 'whole':
                    groups[('digits', digits(int(c['target'])))].append(c)
                elif c['family'] != 'conj':
                    groups[tkey(c)].append(c)
            for g, gc in groups.items():
                if len(gc) >= 2:
                    lab = f'digits {g[1]}' if g[0] == 'digits' else f'{g[1]} {g[0]}'
                    add(13, (A, B, g), gc, f'{A} – {B}: {lab}')
    # 15
    seen = set()
    for h in Hs:
        if h['kind'] != 'S' or h['score'] < HIGH:
            continue
        for j in Js:
            if (j['kind'] == 'S' and (j['a'], j['b']) == (h['a'], h['b']) and j['plane'] != h['plane']
                    and j['score'] >= HIGH and (h['a'], h['b'], h['plane']) not in seen):
                seen.add((h['a'], h['b'], h['plane']))
                add(15, (h['a'], h['b']), [h, j], f"sky {h['a']} on {h['b']}: H {h['plane']}, J {j['plane']}")
    # 14
    for ch, cs in (('H', H), ('J', J)):
        nat = [c for c in cs if c['kind'] == 'N' and 'Jupiter' in (c['a'], c['b']) and c['score'] >= MID and c['family'] != 'conj']
        sky = [c for c in cs if c['kind'] == 'S' and c['a'] == 'Jupiter' and c['score'] >= MID and c['family'] != 'conj']
        for k in sorted({tkey(c) for c in nat} & {tkey(c) for c in sky}):
            add(14, (ch, k[1]), [c for c in nat if tkey(c) == k] + [c for c in sky if tkey(c) == k], f'{ch} {k[1]} {k[0]}')
    return items


def run(path):
    data = load(path)
    per = {cl: runner_checks(r['cells'], r['opp']) for cl, r in data.items()}
    holders = collections.defaultdict(set)
    for cl, items in per.items():
        for it in items:
            if it['check'] != 7:
                holders[(it['check'], it['key'])].add(cl)
    for cl, items in per.items():
        for it in items:
            if it['check'] == 7:
                it['field'] = ''
                continue
            o = sorted(holders[(it['check'], it['key'])] - {cl})
            it['field'] = 'only' if not o else 'also: ' + ', '.join(f"{c} {data[c]['name']['H'].split(' ', 1)[1]}" for c in o)
    return data, per


NAMES = {1: 'natal pair, same number, both charts', '2a': 'sky X on natal Y, both charts, same number',
         '2b': 'sky X on natal Y, both charts, both >= 80', 3: 'sky X on both natal Jupiters (>= 80)',
         4: 'sky X, same number, both charts (>= 80)', 5: 'number swap (>= 80)', 6: 'centre on a body tied to natal Jupiter (>= 50)',
         7: 'numbers in both charts (>= 80, background)', 8: 'axis (natal Jupiter on a node)', 9: 'natal Jupiter ties (>= 50)',
         10: 'N and N x phi (>= 50)', 11: f'values close together (within {WINDOW})', 12: 'digits across decades (whole N, 10 N)',
         13: 'one body pair, every layer', 14: 'sky Jupiter repeats natal Jupiter (>= 50)',
         15: 'sky X on natal Y, both charts, crossed planes (>= 80)'}
ORDER = [1, '2a', '2b', 15, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('active')
    ap.add_argument('--out', default=os.path.join(HERE, '..', 'docs', 'eddie_read', 'basic'))
    a = ap.parse_args()
    data, per = run(a.active)
    race = os.path.basename(a.active).replace('race_batch_', '').replace('_active.xlsx', '')
    os.makedirs(a.out, exist_ok=True)
    L = [f'# Basic view: {race}', '', 'The _active.xlsx P##_DIST tabs only: natal → natal and sky → natal, bodies and the four royal '
         'stars (no other stars, no equator, no angles, no natal Moon; sky → royal star cells are shared by every runner and left out of '
         'checks 2a, 2b, 4, 5, 7, 13, 15). Data only, no pick (tools/eddie_basic.py). Each item: only / also = the same key in '
         'another runner.', '']
    L.append('## Field')
    L.append('| Runner | ' + ' | '.join(str(k) for k in ORDER) + ' |')
    L.append('|---|' + '---|' * len(ORDER))
    for cl in sorted(per):
        cnt = collections.Counter(it['check'] for it in per[cl])
        row = []
        for k in ORDER:
            if k == 7:
                row.append(str(next(it for it in per[cl] if it['check'] == 7)['key'][1]))
            else:
                n = cnt[k]
                o = sum(1 for it in per[cl] if it['check'] == k and it['field'] == 'only')
                row.append(f'{n} ({o} only)' if n else '-')
        L.append(f"| {cl} {data[cl]['name']['H'].split(' ', 1)[1]} / {data[cl]['name']['J']} | " + ' | '.join(row) + ' |')
    L.append('')
    L.append('Checks: ' + '; '.join(f'{k} {NAMES[k]}' for k in ORDER) + '.')
    for cl in sorted(per):
        L += ['', f"## {data[cl]['name']['H']} / {data[cl]['name']['J']}"]
        for k in ORDER:
            its = [it for it in per[cl] if it['check'] == k]
            L.append(f'### {k} {NAMES[k]}')
            if k == 7:
                it = its[0]
                L.append(f"- {it['note']}: " + (', '.join(it['cells']) or 'none'))
                continue
            if not its:
                L.append('- none')
            for it in its:
                L.append(f"- {it['note'] + ': ' if it['note'] else ''}{' | '.join(it['cells'])} — {it['field']}")
    md = os.path.join(a.out, f'{race}_basic.md')
    open(md, 'w').write('\n'.join(L) + '\n')
    js = {'race': race, 'workbook': os.path.basename(a.active),
          'runners': {str(cl): {'name': data[cl]['name'], 'items': [{**it, 'key': str(it['key'])} for it in per[cl]]}
                      for cl in sorted(per)}}
    json.dump(js, open(os.path.join(a.out, f'{race}_basic.json'), 'w'), indent=1, ensure_ascii=False)
    print(md)


if __name__ == '__main__':
    main()
