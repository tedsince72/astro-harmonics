"""check_tl_before.py (independent checker, 22 Oct 2026): (d) a tables workbook before vs after the star-timeline change. Every row
outside the timeline blocks identical (value, fill, comment), sheet by sheet; earlier TIMELINE (sky, H, J) events kept identical apart
from "also"; earlier LONG events scoring >= 90 kept identical apart from "also"; no LONG row under 90; new events listed by source.
usage: check_tl_before.py before.xlsx after.xlsx"""
import os, re, sys, collections
import openpyxl
sys.path.insert(0, os.path.dirname(__file__))
from check_tl_common import STAR_SRC

TLRX = re.compile(r'(STAR TIMELINE|LONG TIMELINE|TIMELINE)( [HJ])?')


def sig(c):
    f = c.fill.start_color.rgb if c.fill is not None and c.fill.fill_type else None
    return (c.value, f, c.comment.text if c.comment else None)


def load(p):
    wb = openpyxl.load_workbook(p)
    out = {}
    for ws in wb.worksheets:
        other, tl = [], collections.defaultdict(list)
        for r in ws.iter_rows():
            a = r[0].value
            if isinstance(a, str) and TLRX.fullmatch(a):
                tl[a].append([sig(c) for c in r])
            elif isinstance(a, str) and TLRX.match(a) and '(' in a[:30] and 'TIMELINE' in a.split('(')[0]:
                tl[a.split(' (')[0] + ' TITLE'].append([sig(c) for c in r])
            else:
                other.append(tuple(sig(c) for c in r))
        out[ws.title] = (other, tl)
    return out


def strip_also(row):
    """row of sigs -> comparable tuple with the note's 'also' part removed"""
    v = list(row)
    if len(v) > 12 and v[12][0]:
        parts = [p for p in str(v[12][0]).split('; ') if not p.startswith('also ')]
        v[12] = ('; '.join(parts) or None, v[12][1], v[12][2])
    while v and v[-1] == (None, None, None):
        v.pop()
    return tuple(v)


def also(row):
    if len(row) > 12 and row[12][0]:
        for p in str(row[12][0]).split('; '):
            if p.startswith('also '):
                return p[5:].split(', ')
    return []


def isevent(row):
    return row[4][0] is not None and row[3][0] not in ('source',) and row[1][0] != 'exact (race-local)'


b, a = load(sys.argv[1]), load(sys.argv[2])
bad = []
print('sheets equal:', list(b) == list(a))
for sh in a:
    if sh not in b:
        bad.append(('sheet added', sh))
        continue
    ob, tb = b[sh]
    oa, ta = a[sh]
    norm = lambda rows: [tuple(x for x in r if x != (None, None, None)) for r in rows]
    nb_, na_ = norm(ob), norm(oa)
    extra_ok = na_[:len(nb_)] == nb_ and all(not r or r[0][0] == 'table' for r in na_[len(nb_):])
    if extra_ok and len(na_) > len(nb_):
        print(f'{sh:12s} other rows identical; {len(na_) - len(nb_)} rows appended (blank / STAR TIMELINE header rows only)')
    if nb_ != na_ and not extra_ok:
        diff = [(i, x, y) for i, (x, y) in enumerate(zip(nb_, na_)) if x != y]
        bad.append(('other rows differ', sh, len(nb_), len(na_), diff[:3]))
    for blk in sorted(set(tb) | set(ta)):
        if blk.endswith('TITLE'):
            continue
        rb = [r for r in tb.get(blk, []) if isevent(r)]
        ra = [r for r in ta.get(blk, []) if isevent(r)]
        if blk.startswith('STAR'):
            if rb:
                bad.append(('STAR block in before', sh, blk))
            continue
        if blk.startswith('LONG'):
            low = [r[4][0] for r in ra if r[10][0] is None or r[10][0] < 90]
            if low:
                bad.append(('LONG row under 90', sh, blk, low[:5]))
            keep = [r for r in rb if r[10][0] is not None and r[10][0] >= 90]
        else:
            keep = rb
        sa = [strip_also(r) for r in ra]
        miss = [r for r in keep if strip_also(r) not in sa]
        for r in miss:
            bad.append(('earlier event lost or changed', sh, blk, r[4][0], r[5][0]))
        # order of the kept events preserved
        pos = [sa.index(strip_also(r)) for r in keep if strip_also(r) in sa]
        if pos != sorted(pos) and not blk.startswith('LONG'):
            bad.append(('order of earlier events changed', sh, blk))
        # also changes on kept events: only star sources added
        for r in keep:
            if strip_also(r) in sa:
                r2 = ra[sa.index(strip_also(r))]
                ab, aa = also(r), also(r2)
                if aa[:len(ab)] != ab or any(x not in STAR_SRC for x in aa[len(ab):]):
                    bad.append(('also changed beyond star sources', sh, blk, r[4][0], ab, aa))
        sk = [strip_also(r) for r in keep]
        new = [r for r in ra if strip_also(r) not in sk]
        cnt = collections.Counter(r[3][0] for r in new)
        nonstar = [(r[3][0], r[4][0], r[5][0], r[10][0], r[2][0]) for r in new if r[3][0] not in STAR_SRC]
        print(f'{sh:12s} {blk:16s} before {len(rb):3d} (kept {len(keep):3d}) after {len(ra):3d}; new by source {dict(cnt)}')
        for x in nonstar:
            print('      new non-star event:', x)
            bad.append(('new non-star event', sh, blk) + x)
print('MISMATCHES / to explain', len(bad))
for x in bad:
    print('  ', str(x)[:400])
