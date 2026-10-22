"""compare_sel.py (Eddie, 22 Oct 2026: sky star timelines trimmed + 95 / 100 / 95, T24 STAR SELECT): BEFORE.xlsx AFTER.xlsx
- sky STAR TIMELINE / LONG STAR TIMELINE: after = before minus exactly the star-to-star distance events (relationship 'S A – S B',
  no S Jupiter), every remaining row S Jupiter-centred, its first cells (before the three new ones) identical; section / title counts follow;
- runner sheets: T24 STAR SELECT blocks new (counted, cut out);
- every other row of every sheet identical (values, fills, comments), in order.
Prints the dropped events and the table counts."""
import sys, re, openpyxl

SKYB = ('STAR TIMELINE', 'LONG STAR TIMELINE')


def sig(r):
    return tuple((c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None) for c in r)


def trim(t):
    while t and t[-1] == (None, None, None):
        t = t[:-1]
    return t


def rows(ws):
    return [r for r in ws.iter_rows() if any(c.value is not None for c in r)]


def is_ev(r, tid):
    v = r[0].value
    return v == tid and r[3].value and not str(r[3].value).startswith('———')


def main(fb, fa):
    wb, wa = openpyxl.load_workbook(fb), openpyxl.load_workbook(fa)
    bad = []
    for sh in wa.sheetnames:
        ra, rb = rows(wa[sh]), rows(wb[sh])
        if sh == 'SKY JUPITER':
            for tid in SKYB:
                ncol = 13 if tid == 'STAR TIMELINE' else 15
                eb = [r for r in rb if is_ev(r, tid)]
                ea = [r for r in ra if is_ev(r, tid)]
                drop = [r for r in eb if ' → ' not in str(r[4].value) and not str(r[4].value).startswith('S Jupiter')]
                keepb = [trim(sig(r)[:ncol]) for r in eb if r not in drop]
                got = [trim(sig(r)[:ncol]) for r in ea]
                if keepb != got:
                    bad.append((sh, tid, 'rows', len(keepb), len(got)))
                nonsj = [r[4].value for r in ea if not str(r[4].value).startswith('S Jupiter')]
                if nonsj:
                    bad.append((sh, tid, 'not S Jupiter-centred', nonsj[:3]))
                print(f'{sh} {tid}: before {len(eb)}, after {len(ea)}, dropped {len(drop)}: ' +
                      '; '.join(f'{r[4].value} {r[5].value} {r[7].value} ({r[10].value})' for r in drop))
            other_a = [r for r in ra if not (r[0].value in SKYB or (isinstance(r[0].value, str) and r[0].value.startswith(tuple(f'{t} (' for t in SKYB))))]
            other_b = [r for r in rb if not (r[0].value in SKYB or (isinstance(r[0].value, str) and r[0].value.startswith(tuple(f'{t} (' for t in SKYB))))]
            # the blocks' header rows ('table', 'exact (race-local)'): after has three more header cells; compare trimmed to the before width
            hdr = lambda r: r[0].value == 'table' and r[1].value == 'exact (race-local)'
            sa = [trim(sig(r)) for r in other_a]
            sb = [trim(sig(r)) for r in other_b]
            # the two blocks' header rows carry three more cells: drop those three from the after header rows of these blocks
            ha = [i for i, r in enumerate(ra) if hdr(r) and i and isinstance(ra[i - 1][0].value, str) and ra[i - 1][0].value.startswith(tuple(f'{t} (' for t in SKYB))]
            hb = [i for i, r in enumerate(rb) if hdr(r) and i and isinstance(rb[i - 1][0].value, str) and rb[i - 1][0].value.startswith(tuple(f'{t} (' for t in SKYB))]
            wa_ = [trim(sig(ra[i])) for i in ha]
            wb_ = [trim(sig(rb[i])) for i in hb]
            if [x[:-3] for x in wa_] != wb_ or any([c[0] for c in x[-3:]] != ['> 95 since', '100', '< 95 from'] for x in wa_):
                bad.append((sh, 'STAR block headers'))
            sa = [x for i, x in enumerate(trim(sig(r)) for r in ra) if i not in ha and ra[i] in other_a]
            sb = [x for i, x in enumerate(trim(sig(r)) for r in rb) if i not in hb and rb[i] in other_b]
        else:
            sel = [r for r in ra if r[0].value == 'T24 STAR SELECT']
            nt = sum(1 for r in sel if str(r[1].value or '').startswith('T24 STAR SELECT —'))
            if sel:
                print(f'{sh}: T24 STAR SELECT tables {nt}, rows {len(sel)}')
            ix = [i for i, r in enumerate(ra) if r[0].value == 'T24 STAR SELECT']
            span = set(range(ix[0], ix[-1] + 1)) if ix else set()        # the SELECT region (titles, headers, rows; contiguous)
            sa = [trim(sig(r)) for i, r in enumerate(ra) if i not in span]
            sb = [trim(sig(r)) for r in rb]
        if sa != sb:
            n = sum(1 for x, y in zip(sa, sb) if x != y) + abs(len(sa) - len(sb))
            bad.append((sh, f'{n} other rows differ'))
    print('mismatches:', len(bad))
    for x in bad[:10]:
        print('  ', x)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
