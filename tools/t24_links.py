#!/usr/bin/env python3
"""T24 links and repeats per runner (Eddie, 4 Nov 2026).

For one runner sheet, horse then jockey:
  1. every scoring cell of the T24 top rows (S Jupiter → S body, H/J Jupiter → body, S Jupiter → natal body,
     S body → natal Jupiter, S Sun → S body, S Sun → natal body, S Moon → S body, S Moon → natal body);
  2. every star row whose Jupiter column (natal Jupiter) or S Jupiter column (sky Jupiter → that star) scores,
     RA or Dec, highest Jupiter score first, with every scoring cell of that row (bodies and the S Jupiter /
     S Sun / S Moon columns);
Sky-only cells (S Jupiter / S Sun / S Moon → S body, and the S columns of a star row) are the same on the horse and
jockey blocks: they are listed and counted once, as side S.
then, horse and jockey together:
  CHAINS  - a body or star in two or more rows with a cell that closes it on a natal Jupiter, with its parts
            (Eddie, 4 Nov 2026, from Cuban Cigar's Chiron): A sky centre → sky X (or X a star on a sky line),
            B sky centre → natal X, C a star on a sky line → natal X, D closes on a natal Jupiter (sky X → natal
            Jupiter, natal Jupiter → X, or star X → own Jupiter); most parts first;
  REPEATS - the same target (family and number, not conj) in two or more cells; SKY + NATAL first (a sky line value
            repeated on a natal cell);
  OTHER LINKS - a body or star in two or more rows, not closing on a Jupiter.
Every natal cell is marked ONLY (no other runner has that cell - same chart, row or star, body, plane and target)
or 'also <runner> <score>'; sky cells are marked 'sky' (the same for every runner). The FIELD block at the end lists
the chains of every runner.

Cell values are read from the sheet; each is scored with tools/families.py (the same as the cell comments).
Counted: whole, golden, conj from 50; ninth, phi power, sqrt2, silver at any score.

Usage: python3 tools/t24_links.py <tables.xlsx> [P05 ...]   (no runner = every runner)
"""
import os, sys
from collections import defaultdict
import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import families as F

CUT50 = {'whole', 'golden', 'conj'}


def counts(b):
    if not b or b.get('score') is None:
        return False
    if b['family'] in CUT50:
        return b['score'] >= 50
    return b['score'] > 0


def blocks(rows):
    """yield (side, header row index of body names, first row, last row) for T24 HORSE / T24 JOCKEY."""
    out = []
    for i, r in enumerate(rows):
        if r and r[0] == 'T24' and isinstance(r[1], str) and r[1].startswith(('T24 HORSE', 'T24 JOCKEY')):
            side = 'H' if r[1].startswith('T24 HORSE') else 'J'
            j = i + 3
            while j < len(rows) and rows[j] and rows[j][0] == 'T24':
                j += 1
            out.append((side, i + 2, i + 3, j))
    return out


def cols(head, names):
    """column index -> (plane, body name) from the two header rows."""
    c, plane = {}, None
    for k, v in enumerate(head):
        if v in ('RA', 'Dec'):
            plane = v
        nm = names[k] if k < len(names) else None
        if plane and nm and not str(nm).startswith('star =') and not str(nm).startswith('target'):
            c[k] = (plane, nm)
    return c


def cell(v, plane):
    if not isinstance(v, (int, float)):
        return None
    b = F.best(v, plane)
    return b if counts(b) else None


def fmt(e):
    b = e['b']
    t = 'conj' if b['family'] == 'conj' else f"{b['target']} {b['family']}"
    return f"{e['row']} | {e['body']} {e['plane']} {e['v']:.4f} {t} ({b['score']:.2f})"


def collect(ws_rows):
    """(entries, star rows with a Jupiter score per side) for one runner sheet."""
    entries, jstar = [], {}
    for side, hi, first, last in blocks(ws_rows):
        c = cols(ws_rows[hi - 1], ws_rows[hi])
        top = []
        k = first
        while k < last and ws_rows[k][1] != 'stars':
            top.append(ws_rows[k]); k += 1
        stars = [r for r in ws_rows[k + 1:last] if r[1]]
        for r in top:
            skyrow = r[1].endswith('→ S body')
            if skyrow and side == 'J':
                continue            # sky-only: once, on the horse block
            for ci, (pl, nm) in c.items():
                b = cell(r[ci], pl)
                if b:
                    entries.append(dict(side='S' if skyrow else side, row=r[1], body=nm, plane=pl, v=r[ci], b=b,
                                        kind='top', block=side))
        jr = []
        for r in stars:
            js = [cell(r[ci], pl) for ci, (pl, nm) in c.items() if nm in ('Jupiter', 'S Jupiter')]
            js = [x for x in js if x]
            if js:
                jr.append((max(x['score'] for x in js), r))
        jr.sort(key=lambda x: -x[0])
        jstar[side] = []
        for sc, r in jr:
            st = r[1].split(' ', 1)[1]
            jstar[side].append((sc, r[1]))
            for ci, (pl, nm) in c.items():
                b = cell(r[ci], pl)
                if b:
                    sk = nm.startswith('S ')
                    entries.append(dict(side='S' if sk else side, row=('S ' + st) if sk else r[1], body=nm,
                                        plane=pl, v=r[ci], b=b, kind='star', star=st, block=side))
    # one copy of each cell
    u = {}
    for e in entries:
        u.setdefault((e['side'], e['row'], e['body'], e['plane']), e)
    return list(u.values()), jstar


def tkey(b):
    return 'conj' if b['family'] == 'conj' else (b['family'], b['target'])


def fkey(e):
    """the same cell on another runner: chart, row (star name for star rows), body, plane, target."""
    row = e['row']
    if e['kind'] == 'star' and e['side'] in 'HJ':
        row = 'star ' + e['star']
    return (e['side'], row, e['body'], e['plane'], tkey(e['b']))


def field_mark(e, me, field):
    if e['side'] == 'S':
        return 'sky'
    k = fkey(e)
    also = [f"{r} {x['b']['score']:.2f}" for r, idx in field.items() if r != me for x in idx.get(k, [])]
    return 'ONLY' if not also else 'also ' + ', '.join(also)


def jup_cell(e, x):
    """does cell e close body or star x on a natal Jupiter?"""
    r = e['row']
    if e['kind'] == 'top' and e['side'] in 'HJ' and e['body'] == x:
        return r in ('S body → H Jupiter', 'S body → J Jupiter', 'H Jupiter → H body', 'J Jupiter → J body')
    if e['kind'] == 'star' and e['star'] == x and e['body'] == 'Jupiter':
        return True                                           # star x → own Jupiter
    return False


def parts(nm, es, entries):
    """the four parts of Eddie's chain (4 Nov 2026, Cuban Cigar) found for body or star nm."""
    online = {e['star'] for e in entries if e['kind'] == 'star' and e['side'] == 'S'}
    p = {}
    for e in es:
        if e['kind'] == 'top' and e['side'] == 'S' and e['body'] == nm:
            p.setdefault('A', f"sky {e['row'].split(' →')[0][2:]} → sky {nm}")
        if e['kind'] == 'top' and e['side'] in 'HJ' and e['body'] == nm and e['row'].startswith('S ') \
                and not e['row'].startswith('S body'):
            p.setdefault('B', f"{e['row'].split(' →')[0]} → {e['side']} {nm}")
        if e['kind'] == 'star' and e['side'] in 'HJ' and e['body'] == nm and e['star'] in online:
            p.setdefault('C', f"{e['side']} {e['star']} → {nm} (star on a sky line)")
        if jup_cell(e, nm):
            p.setdefault('D', 'closes on ' + ('own Jupiter' if e['kind'] == 'star' else e['row'].split('→ ')[-1]
                                              if e['row'].startswith('S body') else e['row'].split(' →')[0]))
    if any(e['kind'] == 'star' and e['star'] == nm and e['side'] == 'S' for e in es):
        p.setdefault('A', f'{nm} on a sky line')
    both = {e['side'] for e in es if e['kind'] == 'star' and e['star'] == nm and e['body'] == 'Jupiter'}
    if both == {'H', 'J'}:
        p['D'] = 'star → own Jupiter on both charts'
    return p


def report(label, me, entries, jstar, field):
    out = [f'=== {label} ===']
    sh = lambda e: f"{e['side']} {fmt(e)}   [{field_mark(e, me, field)}]"
    by = defaultdict(list)
    for e in entries:
        nm = e['body']
        if nm != 'Jupiter' and not nm.startswith('S '):   # natal Sun and Moon are bodies; S columns go to the star
            by[nm].append(e)
        if e['kind'] == 'star':
            by[e['star']].append(e)
    links = {nm: es for nm, es in by.items() if len({(e['side'], e['row']) for e in es}) >= 2}
    # CHAINS: a link with a cell closing it on a Jupiter and at least one cell from another row
    chains = []
    for nm, es in links.items():
        js = [e for e in es if jup_cell(e, nm)]
        if js and len({(e['side'], e['row']) for e in es}) >= 2:
            only = sum(1 for e in es if field_mark(e, me, field) == 'ONLY')
            pt = parts(nm, es, entries)
            tags = [f'{k}: {v}' for k, v in sorted(pt.items())]
            sides = ''.join(sorted({e['side'] for e in es}))
            chains.append((nm, es, js, only, tags, sides))
    chains.sort(key=lambda c: (-len(c[4]), -len({(e['side'], e['row']) for e in c[1]}), -c[3], c[0]))
    out.append('\n--- CHAINS: a body or star in two or more rows that also closes on a Jupiter ---')
    out.append('(parts, Eddie 4 Nov 2026: A sky centre → sky X (or X a star on a sky line); B sky centre → natal X; '
               'C a star on a sky line → natal X; D closes on a natal Jupiter (sky X → natal Jupiter, natal Jupiter '
               '→ X, or star X → own Jupiter). Most parts first. [ONLY] = no other runner has that cell on the same '
               'target; sky cells are the same for every runner. →J marks the closing cells.)')
    for nm, es, js, only, tags, sides in chains:
        out.append(f"{nm}: parts {''.join(sorted(pt for pt in 'ABCD' if any(t.startswith(pt + ':') for t in tags)))}"
                   f", {len({(e['side'], e['row']) for e in es})} rows, {sides}, {only} ONLY cells")
        for t in tags:
            out.append('      ' + t)
        for e in sorted(es, key=lambda e: (not jup_cell(e, nm), -e['b']['score'])):
            out.append('   ' + ('→J ' if jup_cell(e, nm) else '   ') + sh(e))
    out.append('\n--- REPEATS: the same target (family and number, not conj) in two or more cells; '
               'SKY + NATAL (a sky line value repeated on a natal cell) first ---')
    bt = defaultdict(list)
    for e in entries:
        if e['b']['family'] != 'conj':
            bt[tkey(e['b'])].append(e)
    skynat = lambda es: any(e['side'] == 'S' for e in es) and any(e['side'] in 'HJ' for e in es)
    for (fam, t), es in sorted(bt.items(), key=lambda x: (not skynat(x[1]), -len(x[1]),
                                                          -max(e['b']['score'] for e in x[1]))):
        if len(es) >= 2:
            out.append(f'{t} {fam}  (x{len(es)})' + ('  SKY + NATAL' if skynat(es) else '') + ':')
            for e in sorted(es, key=lambda e: -e['b']['score']):
                out.append('   ' + sh(e))
    out.append('\n--- OTHER LINKS: in two or more rows, not closing on a Jupiter ---')
    cn = {c[0] for c in chains}
    for nm, es in sorted(links.items(), key=lambda x: (-len(x[1]), x[0])):
        if nm in cn:
            continue
        out.append(f"{nm}  ({len({(e['side'], e['row']) for e in es})} rows):")
        for e in sorted(es, key=lambda e: -e['b']['score']):
            out.append('   ' + sh(e))
    for blk in ('H', 'J'):
        out.append(f"\n--- {'HORSE' if blk == 'H' else 'JOCKEY'}: top rows ---")
        rows = []
        for e in entries:
            if e['kind'] == 'top' and e['block'] == blk:
                rows.append(e)
        cur = None
        for e in sorted(rows, key=lambda e: (e['row'], -e['b']['score'])):
            if e['row'] != cur:
                cur = e['row']; out.append(cur + ':')
            out.append('   ' + sh(e))
        out.append(f"\n--- {'HORSE' if blk == 'H' else 'JOCKEY'}: star rows with a Jupiter or S Jupiter score, "
                   "highest first ---")
        for sc, rl in jstar.get(blk, []):
            st = rl.split(' ', 1)[1]
            out.append(f'{rl} (Jupiter {sc:.2f}):')
            es = [e for e in entries if e['kind'] == 'star' and e['star'] == st and (e['row'] == rl or e['side'] == 'S')]
            for e in sorted(es, key=lambda e: (e['body'] not in ('Jupiter', 'S Jupiter'), -e['b']['score'])):
                out.append('   ' + sh(e))
    return out, chains


def main():
    wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
    want = sys.argv[2:]
    data = {}
    for name in wb.sheetnames:
        if name.startswith('P') and name[1:].isdigit():
            rows = [tuple(r) for r in wb[name].iter_rows(values_only=True)]
            ents, js = collect(rows)
            data[name] = (rows[0][0], ents, js)
    field = {}
    for name, (_, ents, _) in data.items():
        idx = defaultdict(list)
        for e in ents:
            if e['side'] != 'S':
                idx[fkey(e)].append(e)
        field[name] = idx
    summary = []
    for name, (lab, ents, js) in data.items():
        if want and name not in want:
            continue
        out, chains = report(lab, name, ents, js, field)
        print('\n'.join(out)); print()
        summary.append((lab, chains))
    print('=== FIELD: chains per runner, most parts first (A sky centre → sky X / X on a sky line; B sky centre → natal X; '
          'C sky-line star → natal X; D closes on a natal Jupiter) ===')
    for lab, chains in summary:
        print(lab)
        for nm, es, js, only, tags, sides in chains:
            pp = ''.join(t[0] for t in tags)
            print(f"   {nm}: parts {pp}, {len({(e['side'], e['row']) for e in es})} rows, {sides}, {only} ONLY cells; "
                  + '; '.join(t[3:] for t in tags))


if __name__ == '__main__':
    main()
