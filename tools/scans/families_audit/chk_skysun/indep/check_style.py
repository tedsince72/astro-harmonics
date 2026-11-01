#!/usr/bin/env python3
"""check_style.py <workbook>: sheet order, freeze, column widths (= SKY JUPITER), score fills by families.colour on the SKY block,
pair tables (ratio score, midpoint total) and timelines (score at the off)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *  # noqa
import check_blocks as CB


def fill(c):
    f = c.fill
    return f.fgColor.rgb if f is not None and f.fill_type else None


def score_cols(ws):
    out = []
    for r in range(1, ws.max_row + 1):
        a = ws.cell(r, 1).value
        if a == 'SKY' and isinstance(ws.cell(r, 2).value, str) and '→' in ws.cell(r, 2).value:
            out += [(r, 8), (r, 17)]
        elif a in ('SKY PAIRS', 'SKY STARS', 'SKY ROYAL') and ws.cell(r, 2).value in ('S–S', 'body – royal', 'royal – royal'):
            out += [(r, 14), (r, 22)]
        elif a in ('TIMELINE', 'LONG TIMELINE', 'STAR TIMELINE', 'LONG STAR TIMELINE') and not str(ws.cell(r, 4).value).startswith('———'):
            out += [(r, 11)]
    return out


def run(path):
    wb = openpyxl.load_workbook(path)
    names = wb.sheetnames
    print('sheets', names[:5])
    errs = []
    if names[1:4] != ['SKY JUPITER', 'SKY SUN', 'SKY MOON'] or not names[4].startswith('P'):
        errs.append(('sheet order', names))
    J = wb['SKY JUPITER']
    # learn colour -> fill on SKY JUPITER
    learn = {}
    for r, c in score_cols(J):
        v = J.cell(r, c).value
        if isinstance(v, (int, float)):
            learn.setdefault(F.colour(v), set()).add(fill(J.cell(r, c)))
    print('fills learned on SKY JUPITER', {k: sorted(map(str, v)) for k, v in learn.items()})
    for sn in ('SKY SUN', 'SKY MOON'):
        ws = wb[sn]
        if ws.freeze_panes not in (None, 'A1'): errs.append((sn, 'freeze', ws.freeze_panes))
        for col, dim in J.column_dimensions.items():
            w2 = ws.column_dimensions[col].width if col in ws.column_dimensions else None
            if dim.width != w2 and (dim.width or w2):
                errs.append((sn, 'width', col, dim.width, w2))
        for col, dim in ws.column_dimensions.items():
            if col not in J.column_dimensions and dim.width: errs.append((sn, 'extra width', col, dim.width))
        n = 0
        for r, c in score_cols(ws):
            v = ws.cell(r, c).value
            if isinstance(v, (int, float)):
                n += 1
                exp = learn.get(F.colour(v))
                if exp is None or fill(ws.cell(r, c)) not in exp:
                    # 2-dp shown scores at a band edge can differ from the unrounded colour: report
                    errs.append((sn, 'fill', r, c, v, fill(ws.cell(r, c)), exp))
        print(sn, 'score cells with fill checked', n)
    print('errors', len(errs))
    print('non-width', [e for e in errs if e[1] != 'width'][:20])
    print('width diffs', len([e for e in errs if e[1] == 'width']))


if __name__ == '__main__':
    run(sys.argv[1])
