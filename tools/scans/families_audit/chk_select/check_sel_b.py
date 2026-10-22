"""check_sel_b.py: (b) every '> 95 since' / '100' / '< 95 from' cell of the sky STAR TIMELINE and LONG STAR TIMELINE re-searched with
own engine code. usage: check_sel_b.py tables.xlsx asc|lin"""
import sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from check_sel_common import *

wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
race = sys.argv[2]
sky, ch = load_positions(wb)
sk = Sky(sky, Eng(race))
rows = [r for r in wb['SKY JUPITER'].iter_rows(values_only=True) if r and r[0] in ('STAR TIMELINE', 'LONG STAR TIMELINE')]
n = bad = 0
stats = {}
for r in rows:
    blk = r[0]
    if r[4] is None or r[1] is None:      # markers / section rows
        continue
    if blk == 'STAR TIMELINE':
        m0, c = r[2], r[13:16]
    else:
        m0, c = r[13], r[15:18]
    f = make_scorer((r[4], r[5], r[6], r[7]), sk)
    n += 1
    msgs = []
    if f is None:
        msgs.append('not a S Jupiter event')
    elif m0 is None:      # not within 1 year exact
        ok = all(x == 'not within 1 year' or x == '—' for x in c)
        if not ok:
            msgs.append(f'exact not within 1 year but cells {c}')
        stats['exact not within'] = stats.get('exact not within', 0) + 1
    else:
        s0 = f(m0)
        if s0 < 95:
            # refine: peak within +-1 min
            pk = max(f(m0 + d / 10) for d in range(-10, 11))
            if c != ('—', '—', '—') and not (c[0] == '—' and c[2] == '—'):
                msgs.append(f'score at exact {s0:.2f} (peak +-1 min {pk:.2f}) < 95 but cells {c}')
            stats['dash'] = stats.get('dash', 0) + 1
            if c[0] != '—':
                msgs.append(f'expected — got {c}')
            line = f"{'BAD' if msgs else 'ok '} {blk:18s} {r[4]:50s} {r[5]:7s} {r[6]:8s} m0 {m0:+.1f} score@exact {s0:.2f} peak {pk:.2f} | {c}"
            print(line, *msgs)
            bad += bool(msgs)
            continue
        hit100 = parse_cell_min(c[1], None)
        tolm = 0.051 if 'min)' in c[1] else 7.3
        if hit100 is None or abs(hit100 - m0) > tolm or c[1].split(' (')[0] != r[1]:
            msgs.append(f'100 cell {c[1]} vs exact {r[1]} {m0}')
        mine = []
        for i, d in ((0, -1), (2, 1)):
            x = cross(f, m0, d)
            mine.append(x)
            if x is None:
                if c[i] != 'not within 1 year':
                    msgs.append(f'col {i}: mine not within 1 year, sheet {c[i]}')
                stats['nw'] = stats.get('nw', 0) + 1
            else:
                sv = parse_cell_min(c[i], None)
                cm = clock_min(c[i], race)
                tolm = 1.0 if 'min)' in c[i] else 7.3
                if sv is None or abs(sv - x) > tolm or cm is None or not (-2.0 <= cm - x <= 1.0) or ('min)' in c[i] and not (cm - 0.06 <= sv <= cm + 1.05)):
                    msgs.append(f'col {i}: mine {x:+.2f}, sheet {c[i]} (clock {cm})')
                if 'min)' in c[i] and abs(x) >= 1440 or 'days)' in c[i] and abs(x) < 1440:
                    msgs.append(f'col {i}: format {c[i]}')
                # format: days beyond a day
                stats['found'] = stats.get('found', 0) + 1
    bad += bool(msgs)
    print(f"{'BAD' if msgs else 'ok '} {blk:18s} {r[4]:50s} {r[5]:7s} {r[6]:8s} m0 {m0} | {c} | mine "
          f"{[None if not isinstance(x, float) else round(x, 2) for x in (mine if f and m0 is not None else [])]}", *msgs)
print(f'rows {n}, bad {bad}, {stats}')
