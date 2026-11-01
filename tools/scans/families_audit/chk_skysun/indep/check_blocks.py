#!/usr/bin/env python3
"""check_blocks.py <workbook> [sheet ...]: SKY block, SKY EQ, SKY PAIRS / STARS / ROYAL of each SKY <centre> sheet vs own rebuild."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
from core import *  # noqa

AREA_OF_TITLE = [('AREA A', 'A'), ('AREA φ AND √2', 'P'), ('AREA B', 'B'), ('NO RATIO OR MIDPOINT HIT', None), ('NO HIT', None)]


def num(v):
    return None if v in (None, '') else float(v)


def close(a, b, tol=1.5e-6):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= tol


def sheet_rows(ws):
    return [[ws.cell(r, c).value for c in range(1, ws.max_column + 1)] for r in range(1, ws.max_row + 1)]


def star_order_from_jup(wb):
    ws = wb['SKY JUPITER']
    out = []
    for r in range(5, ws.max_row + 1):
        if ws.cell(r, 1).value != 'SKY': break
        nm = ws.cell(r, 2).value.split('→ S ')[1]
        out.append(nm)
    return out


def run(path, sheets):
    wb = openpyxl.load_workbook(path)
    pos = Pos(wb)
    jorder = star_order_from_jup(wb)
    star_order = [s for s in jorder if pos.p.get(s, (0, 0, 0, 0, ''))[4] == 'star']
    star_pair_order = [s for s in pos.first_stars if s != 'Polaris'] + pos.new_stars
    res = {}
    for sn in sheets:
        centre = sn.split()[-1].capitalize()
        B = build(pos, centre, star_order, star_pair_order)
        res[sn] = (B, check_sheet(wb[sn], pos, B, sn))
    return wb, pos, res


def check_sheet(ws, pos, B, sn):
    rows = sheet_rows(ws)
    c = B['centre']
    errs = []; n = {'sky_cells': 0, 'eq': 0, 'pairs': 0, 'stars': 0, 'royal': 0}
    # ---- SKY block
    sky = [r for r in rows if r[0] == 'SKY' and isinstance(r[1], str) and r[1].startswith(f'S {c} → S ')]
    names = [r[1].split('→ S ')[1] for r in sky]
    exp = [x for x, _ in B['sky']]
    if names != exp:
        errs.append(('SKY order', names, exp))
    for (x, cells), r in zip(B['sky'], sky):
        for pl, base in (('RA', 2), ('Dec', 11)):
            d = cells[pl]
            got = r[base:base + 9]
            if d is None:
                if any(v not in (None, '') for v in got):
                    errs.append(('SKY RA equator not blank', x))
                continue
            n['sky_cells'] += 1
            exp_cells = [round(d['v0'], 6), round(d['v5'], 6), d['txt'], None, f"{d['off']:+.5f}",
                         round(d['score'], 2) if d['score'] is not None else None,
                         d.get('arrow') if d['score'] is not None else None,
                         (d.get('also') or None) if d['score'] is not None else None,
                         d.get('timing') if d['score'] is not None else None]
            for i, (g, e) in enumerate(zip(got, exp_cells)):
                if i in (0, 1, 5):
                    if not close(num(g), e, 1.5e-6 if i < 2 else 0.006):
                        errs.append(('SKY', x, pl, i, g, e))
                else:
                    if (g or None) != (e or None):
                        errs.append(('SKY', x, pl, i, g, e))
    # ---- pair tables
    for tname, key in (('SKY PAIRS', 'pairs'), ('SKY STARS', 'stars'), ('SKY ROYAL', 'royal')):
        area = 'X'; got = []
        for r in rows:
            if isinstance(r[0], str) and r[0].startswith(tname + ' ') and ('AREA' in r[0] or 'NO ' in r[0]):
                for t, a in AREA_OF_TITLE:
                    if t in r[0]:
                        area = a; break
            elif r[0] == tname and r[1] in ('S–S', 'body – royal', 'royal – royal'):
                got.append((area, r))
        expr = B[key]
        n[key] = len(got)
        idx = {}
        for r in expr:
            idx[(r['x'], r['y'], r['plane'])] = r
        gotk = set()
        for area, r in got:
            m = re.match(r'S (.+) – S (.+)$', r[2])
            x, y = m.group(1), m.group(2)
            k = (x, y, r[3])
            if k in gotk:
                errs.append((tname, 'duplicate', k))
            gotk.add(k)
            e = idx.get(k)
            if e is None:
                ek = (y, x, r[3])
                errs.append((tname, 'extra row' if ek not in idx else 'orientation', k)); continue
            if c in (x, y):
                errs.append((tname, 'centre as partner', k))
            if e['block'] != r[1]:
                errs.append((tname, 'block', k, r[1], e['block']))
            if area != e['area']:
                errs.append((tname, 'area', k, area, e['area']))
            L = e['L']
            ce = [round(L[0]['v0'], 6), L[0]['txt'], round(L[1]['v0'], 6), L[1]['txt'], round(L[2]['v0'], 6), L[2]['txt'],
                  round(e['q0'], 6), e['rtxt'] if not e['together'] else None, None,
                  round(e['rscore'], 2) if e['rscore'] is not None else None, e['rtiming'], e['between']]
            g = r[4:16]
            for i, (gv, ev) in enumerate(zip(g, ce)):
                if i in (0, 2, 4, 6):
                    if not close(num(gv), ev): errs.append((tname, k, 'cell', i, gv, ev))
                elif i == 9:
                    if not close(num(gv), ev, 0.006): errs.append((tname, k, 'score', gv, ev))
                elif i in (7, 8):
                    pass
                else:
                    if e['together'] and i in (1, 3, 5):
                        continue
                    if gv != ev: errs.append((tname, k, 'cell', i, gv, ev))
            if not e['together']:
                if r[11] != e['rtxt']: errs.append((tname, k, 'interval', r[11], e['rtxt']))
                rb = e['rb']
                if r[12] != off_text(rb): errs.append((tname, k, 'roff', r[12], off_text(rb)))
            m_ = e['mid']
            if m_['clos'] >= 90:
                if not close(num(r[18]), round(m_['clos'], 4), 6e-5): errs.append((tname, k, 'clos', r[18], m_['clos']))
                offt = f"{m_['off']:+.6f}" + (f" {m_['lab']}" if m_['lab'] else '')
                if not str(r[17]).startswith(offt): errs.append((tname, k, 'midoff', r[17], offt))
                if m_['hit']:
                    if not close(num(r[21]), m_['total'], 0.006): errs.append((tname, k, 'midtotal', r[21], m_['total']))
                elif num(r[21]) is not None and not e['together']:
                    errs.append((tname, k, 'midtotal not expected', r[21]))
            else:
                if r[17] not in (None, '') or (len(r) > 21 and r[21] not in (None, '')):
                    errs.append((tname, k, 'mid cells not expected', r[17:22]))
        expk = {(r['x'], r['y'], r['plane']) for r in expr}
        for k in sorted(expk - gotk):
            errs.append((tname, 'missing row', k, idx[k]['area'], round(idx[k]['key'], 2)))
        # order inside each area block: key non-increasing
        last = {}
        for area, r in got:
            m = re.match(r'S (.+) – S (.+)$', r[2]); k = (m.group(1), m.group(2), r[3])
            e = idx.get(k)
            if not e: continue
            blk = (area, r[1] if tname == 'SKY ROYAL' and area is None else '')
            if tname == 'SKY ROYAL':
                blk = (area,)
            kk = e['key']
            if blk in last and kk > last[blk] + 1e-9:
                errs.append((tname, 'order', k, kk, last[blk]))
            last[blk] = kk
    # ---- SKY EQ
    eqrows = [r for r in rows if r[0] == 'SKY EQ' and isinstance(r[1], str) and r[1].startswith(f'S {c}: ')]
    n['eq'] = len(eqrows)
    exp = {(r['x'], r['y'], r['plane']): r for r in B['eq']}
    gk = []
    for r in eqrows:
        m = re.match(rf'S {c}: S (.+) = S (.+)$', r[1])
        k = (m.group(1), m.group(2), r[2]); gk.append(k)
        e = exp.get(k)
        if not e:
            errs.append(('SKY EQ extra', k)); continue
        mm = e['eqmid']
        ce = [round(e['L'][0]['v0'], 6), round(e['L'][1]['v0'], 6), round(mm['clos'], 4)]
        for gv, ev in zip([r[3], r[4], r[5]], ce):
            if not close(num(gv), ev, 6e-5): errs.append(('SKY EQ', k, gv, ev))
        if not close(num(r[9]), mm['total'], 0.006): errs.append(('SKY EQ total', k, r[9], mm['total']))
        ut = timing_text(pos, e['ut'])
        if r[-1] != ut and r[21] != ut: errs.append(('SKY EQ timing', k, r[21], ut))
    for k in set(exp) - set(gk):
        errs.append(('SKY EQ missing', k))
    # order: non-together by total desc, together at bottom
    tl = [exp[k]['eqtog'] for k in gk if k in exp]
    if tl != sorted(tl): errs.append(('SKY EQ together not at bottom',))
    tots = [exp[k]['eqmid']['total'] for k in gk if k in exp and not exp[k]['eqtog']]
    if any(a < b - 1e-9 for a, b in zip(tots, tots[1:])): errs.append(('SKY EQ order',))
    return n, errs


if __name__ == '__main__':
    wb, pos, res = run(sys.argv[1], sys.argv[2:])
    for sn, (B, (n, errs)) in res.items():
        print(sn, n, 'errors', len(errs))
        for e in errs[:25]:
            print('   ', e)
