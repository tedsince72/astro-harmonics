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
then the links: every body (or star) named in two or more of those entries, and every target (family and number,
not conj) found in two or more entries, horse and jockey together.

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
CENTRES = {'Jupiter', 'Sun', 'Moon'}


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


def runner(ws_rows, label):
    out = [f'=== {label} ===']
    entries = []          # all entries for the links
    for side, hi, first, last in blocks(ws_rows):
        c = cols(ws_rows[hi - 1], ws_rows[hi])
        top, stars = [], []
        k = first
        while k < last and ws_rows[k][1] != 'stars':
            top.append(ws_rows[k]); k += 1
        stars = [r for r in ws_rows[k + 1:last] if r[1]]
        out.append(f'\n--- {"HORSE" if side == "H" else "JOCKEY"}: top rows (scoring cells) ---')
        for r in top:
            skyrow = r[1].endswith('→ S body')
            if skyrow and side == 'J':
                continue            # listed once, on the horse block
            es = []
            for ci, (pl, nm) in c.items():
                b = cell(r[ci], pl)
                if b:
                    es.append(dict(side='S' if skyrow else side, row=r[1], body=nm, plane=pl, v=r[ci], b=b,
                                   kind='top'))
            es.sort(key=lambda e: -e['b']['score'])
            out.append(f'{r[1]}:')
            for e in es:
                out.append('   ' + fmt(e))
            entries += es
        # star rows with a Jupiter score
        jr = []
        for r in stars:
            js = [(cell(r[ci], pl), pl, ci) for ci, (pl, nm) in c.items() if nm in ('Jupiter', 'S Jupiter')]
            js = [x for x in js if x[0]]
            if js:
                jr.append((max(x[0]['score'] for x in js), r))
        jr.sort(key=lambda x: -x[0])
        out.append(f'\n--- {"HORSE" if side == "H" else "JOCKEY"}: star rows with a Jupiter or S Jupiter score ({len(jr)}), '
                   'highest first ---')
        for sc, r in jr:
            es = []
            for ci, (pl, nm) in c.items():
                b = cell(r[ci], pl)
                if b:
                    st = r[1].split(' ', 1)[1]
                    sk = nm.startswith('S ')
                    es.append(dict(side='S' if sk else side, row=('S ' + st) if sk else r[1], body=nm, plane=pl,
                                   v=r[ci], b=b, kind='star', star=st))
            es.sort(key=lambda e: (e['body'] not in ('Jupiter', 'S Jupiter'), -e['b']['score']))
            out.append(f'{r[1]} (Jupiter {sc:.2f}):')
            for e in es:
                out.append('   ' + fmt(e))
            entries += es
    # links: body / star names in two or more entries (Jupiter, Sun, Moon left out as the centres)
    by = defaultdict(list)
    for e in entries:
        nm = e['body'].replace('S ', '')
        if nm not in CENTRES:
            by[nm].append(e)
        if e['kind'] == 'star' and e['body'].replace('S ', '') not in CENTRES:
            by[e['star']].append(e)
        elif e['kind'] == 'star':
            by[e['star']].append(e)
    out.append('\n--- LINKS: the same body or star in two or more entries (horse and jockey) ---')
    for nm, es in sorted(by.items(), key=lambda x: (-len({(e['row'], e['body'], e['plane']) for e in x[1]}), x[0])):
        uniq = {}
        for e in es:
            uniq[(e['side'], e['row'], e['body'], e['plane'])] = e
        rowset = {(e['side'], e['row']) for e in uniq.values()}
        if len(rowset) < 2:
            continue
        sides = ''.join(sorted({e['side'] for e in uniq.values()}))
        out.append(f'{nm}  ({len(uniq)} cells, {len(rowset)} rows, {sides}):')
        for e in sorted(uniq.values(), key=lambda e: -e['b']['score']):
            out.append(f"   {e['side']} " + fmt(e))
    # repeats: the same target in two or more entries
    bt = defaultdict(dict)
    for e in entries:
        if e['b']['family'] == 'conj':
            continue
        bt[(e['b']['family'], e['b']['target'])][(e['side'], e['row'], e['body'], e['plane'])] = e
    out.append('\n--- REPEATS: the same target (family and number, not conj) in two or more entries ---')
    for (fam, t), es in sorted(bt.items(), key=lambda x: (-len(x[1]), -max(e['b']['score'] for e in x[1].values()))):
        if len(es) < 2:
            continue
        out.append(f'{t} {fam}  (x{len(es)}):')
        for e in sorted(es.values(), key=lambda e: -e['b']['score']):
            out.append(f"   {e['side']} " + fmt(e))
    return out


def main():
    wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
    want = sys.argv[2:]
    for name in wb.sheetnames:
        if not (name.startswith('P') and name[1:].isdigit()):
            continue
        if want and name not in want:
            continue
        rows = [tuple(r) for r in wb[name].iter_rows(values_only=True)]
        print('\n'.join(runner(rows, f'{name} {rows[0][0]}')))
        print()


if __name__ == '__main__':
    main()
