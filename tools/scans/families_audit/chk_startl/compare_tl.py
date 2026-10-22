"""compare_tl.py (Eddie, 22 Oct 2026: all 67 stars in every timeline, STAR TIMELINE, LONG >= 90): a tables workbook against the build
before. Timeline blocks (TIMELINE, LONG TIMELINE, STAR TIMELINE; H / J on runner sheets): event counts before -> after, every earlier
event kept with the same cells (only "also" may gain a star source: S Jup→star, star→Jup, S Jup on star pair, star apex); LONG blocks
compared on the events scoring >= 90 (the new threshold); every row outside the timeline blocks identical (values, fills, comments).
usage: compare_tl.py before.xlsx after.xlsx"""
import sys, re, openpyxl

STAR_SRC = ('S Jup→star', 'star→Jup', 'S Jup on star pair', 'star apex')
TL = re.compile(r'^(STAR TIMELINE|LONG TIMELINE|TIMELINE)( [HJ])?$')


def sig(r):
    return tuple((c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None) for c in r)


def blocks(ws):
    """-> {tid: [event rows (cell tuples)]}, {tid: title}, other rows (signatures, in order)"""
    ev, titles, other = {}, {}, []
    for r in ws.iter_rows():
        a = r[0].value
        if isinstance(a, str) and TL.match(a):
            v = [c.value for c in r]
            if v[3] and str(v[3]).startswith('———') or v[1] == 'exact (race-local)':
                continue                                   # markers, section rows, headers
            ev.setdefault(a, []).append(r)
            continue
        if isinstance(a, str) and re.match(r'^(STAR TIMELINE|LONG TIMELINE|TIMELINE)( [HJ])? \(', a):
            titles[a.split(' (')[0]] = a
            continue
        if isinstance(a, str) and a == 'table' and r[1].value == 'exact (race-local)':
            continue
        if any(c.value is not None for c in r):
            other.append(sig(r))
    return ev, titles, other


def key(v):
    return (v[3], v[4], v[5], v[6], v[7])                  # source, relationship, plane, kind, target


def note_ok(nb, na):
    """after note = before note with only star sources added to 'also'"""
    if nb == na:
        return True
    parts = lambda n: [p for p in (n or '').split('; ') if p]
    pb, pa = parts(nb), parts(na)
    alsob = next((p for p in pb if p.startswith('also ')), 'also ')[5:].split(', ')
    alsoa = next((p for p in pa if p.startswith('also ')), 'also ')[5:].split(', ')
    rest = lambda ps: [p for p in ps if not p.startswith('also ')]
    return rest(pb) == rest(pa) and [x for x in alsoa if x not in STAR_SRC] == [x for x in alsob if x] and all(x in STAR_SRC for x in alsoa if x not in alsob)


def main(fb, fa):
    wb, wa = openpyxl.load_workbook(fb), openpyxl.load_workbook(fa)
    bad = []
    for sh in wa.sheetnames:
        if sh not in wb.sheetnames:
            bad.append((sh, 'new sheet')); continue
        eb, tb, ob = blocks(wb[sh]); ea, ta, oa = blocks(wa[sh])
        if ob != oa:
            n = sum(1 for x, y in zip(ob, oa) if x != y) + abs(len(ob) - len(oa))
            bad.append((sh, f'{n} rows outside the timelines differ'))
        for tid in sorted(set(eb) | set(ea)):
            rb = [[c.value for c in r] for r in eb.get(tid, [])]
            ra = [[c.value for c in r] for r in ea.get(tid, [])]
            long_ = tid.startswith('LONG')
            if long_:
                rb = [v for v in rb if v[10] is not None and v[10] >= 90]   # the new threshold
            ka = {}
            for v in ra:
                ka.setdefault(key(v), []).append(v)
            gone, chg, also = [], 0, 0
            for v in rb:
                m = ka.get(key(v))
                if not m:
                    gone.append(v[3:8]); continue
                w = m.pop(0)
                if v[:12] != w[:12] or v[13:] != w[13:] or not note_ok(v[12], w[12]):
                    chg += 1
                    bad.append((sh, tid, 'changed', v[3:13], w[3:13]))
                elif v[12] != w[12]:
                    also += 1
            new = [v for vs in ka.values() for v in vs]
            nsrc = {}
            for v in new:
                nsrc[v[3]] = nsrc.get(v[3], 0) + 1
            if gone:
                bad.append((sh, tid, 'gone', gone[:3]))
            print(f'{sh:12s} {tid:16s} before {len(eb.get(tid, [])):4d}{" (>= 90: " + str(len(rb)) + ")" if long_ else ""} after {len(ra):4d}; '
                  f'new {len(new)} {nsrc}; earlier kept {len(rb) - len(gone)}, note gained a star source {also}, changed {chg}, gone {len(gone)}')
    print('mismatches:', len(bad))
    for x in bad[:15]:
        print('  ', x)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
