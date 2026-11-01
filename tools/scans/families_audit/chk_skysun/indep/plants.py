#!/usr/bin/env python3
"""plants.py <built workbook> <outdir>: planted errors on copies, each must be caught by check_blocks / check_tl."""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import check_blocks as CB, check_tl as T


def rows_of(ws, a, b_pred=lambda v: True):
    return [r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value == a and b_pred(ws.cell(r, 2).value)]


def find(ws, a, col, text):
    for r in range(1, ws.max_row + 1):
        if ws.cell(r, 1).value == a and ws.cell(r, col).value == text:
            return r
    raise KeyError(text)


def setrow(ws, r, vals):
    for k, v in enumerate(vals):
        ws.cell(r, 1 + k).value = v


def getrow(ws, r, n=25):
    return [ws.cell(r, k).value for k in range(1, n + 1)]


def plant_wrong_centre(wb):         # SKY SUN row 'S Sun → S Mars' filled with the S Jupiter → S Mars cells (label kept)
    s, j = wb['SKY SUN'], wb['SKY JUPITER']
    r = find(s, 'SKY', 2, 'S Sun → S Mars'); rj = find(j, 'SKY', 2, 'S Jupiter → S Mars')
    v = getrow(j, rj); v[1] = 'S Sun → S Mars'; setrow(s, r, v)


def plant_relabel(wb):              # SKY SUN row relabelled 'S Jupiter → S Mars'
    s = wb['SKY SUN']; r = find(s, 'SKY', 2, 'S Sun → S Mars'); s.cell(r, 2).value = 'S Jupiter → S Mars'


def plant_missing_pair(wb):         # one SKY PAIRS row deleted on SKY SUN
    s = wb['SKY SUN']; r = rows_of(s, 'SKY PAIRS', lambda v: v in ('S–S', 'body – royal'))[5]
    s.delete_rows(r)


def plant_centre_partner(wb):       # a SKY MOON pair row relabelled with the Moon as a partner
    s = wb['SKY MOON']; r = rows_of(s, 'SKY PAIRS', lambda v: v == 'S–S')[3]
    lab = s.cell(r, 3).value; x = lab.split(' – ')[0]
    s.cell(r, 3).value = lab.replace(x, 'S Moon', 1)


def plant_moon_outside(wb, pos, B):  # a real event just outside +20 inserted at the end of SKY MOON TIMELINE
    s = wb['SKY MOON']
    evs = T.dedupe(T.events(pos, B, T.sheet_pair_rows(B)))
    e = min((e for e in evs if 20 < e['t'] < 22), key=lambda e: e['t'])
    last = rows_of(s, 'TIMELINE')[-1]
    s.insert_rows(last + 1)
    setrow(s, last + 1, ['TIMELINE', T.clock(pos, e['t']), round(e['t'], 1), e['src'], e['rel'], e['plane'], e['kind'], e['target'],
                         e['tv'], round(e['v0'], 6), None if e['score'] is None else round(e['score'], 2),
                         'applying', T.note(e)])
    return f"{e['rel']} {e['plane']} at {e['t']:+.2f} min"


def plant_order(wb):                # two SKY SUN TIMELINE events swapped
    s = wb['SKY SUN']; rr = [r for r in rows_of(s, 'TIMELINE') if not str(s.cell(r, 4).value).startswith('———')]
    a, b = rr[2], rr[10]
    va, vb = getrow(s, a, 14), getrow(s, b, 14)
    setrow(s, a, vb); setrow(s, b, va)


def plant_moon_star_tl(wb):         # a STAR TIMELINE block on SKY MOON (spec: TIMELINE only)
    s = wb['SKY MOON']; r = s.max_row + 2
    setrow(s, r, ['STAR TIMELINE', '14:40', 5.0, 'SKY', 'S Moon → S Regulus', 'RA', 'distance'])


def detect(path, sheets):
    wb, pos, res = CB.run(path, sheets)
    out = []
    for sn, (B, (n, errs)) in res.items():
        out += [(sn,) + tuple(e) for e in errs]
        c, e2, *_ = T.check(wb[sn], pos, B)
        out += [(sn,) + tuple(e) for e in e2]
    return out


if __name__ == '__main__':
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    base = detect(src, ['SKY SUN', 'SKY MOON'])
    print('clean build errors:', len(base))
    wb0, pos, res = CB.run(src, ['SKY MOON'])
    Bm = res['SKY MOON'][0]
    plants = [('wrong centre (S Jupiter cells under S Sun → S Mars)', plant_wrong_centre, False),
              ('SKY row relabelled S Jupiter → S Mars', plant_relabel, False),
              ('missing SKY PAIRS row', plant_missing_pair, False),
              ('centre (Moon) as partner in SKY MOON SKY PAIRS', plant_centre_partner, False),
              ('Moon event outside −5 / +20', plant_moon_outside, True),
              ('out-of-order SKY SUN TIMELINE event', plant_order, False),
              ('STAR TIMELINE on SKY MOON', plant_moon_star_tl, False)]
    for i, (name, fn, needs) in enumerate(plants):
        wb = openpyxl.load_workbook(src)
        info = fn(wb, pos, Bm) if needs else fn(wb)
        p = os.path.join(outdir, f'plant{i + 1}.xlsx'); wb.save(p)
        found = detect(p, ['SKY SUN', 'SKY MOON'])
        print(f'plant {i + 1}: {name}{" (" + info + ")" if info else ""}: caught {"yes" if found else "NO"} ({len(found)} findings)',
              '| first:', str(found[:2])[:300])
