"""compare_sky35.py (20 Oct 2026): tables workbook with SKY STARS and the sky TIMELINE / LONG TIMELINE on the 35 stars against the build
before. Every sheet but SKY JUPITER identical (values, fills, comments). SKY JUPITER: SKY STARS rows keyed by (pair, plane) with their
area block; TIMELINE / LONG TIMELINE rows keyed by (table, relationship, plane, kind, target) (marker rows by their label); the block
and section titles (counts) printed; every other row identical in order.
usage: compare_sky35.py before.xlsx after.xlsx"""
import sys, re, openpyxl
sys.path.insert(0, 'tools')
from jupiter_tables import NEW_STARS
NEW = re.compile(r'\b(' + '|'.join(x if x != 'Deneb' else r'Deneb(?! Algedi)' for x in NEW_STARS) + r')\b')
TL = ('TIMELINE', 'LONG TIMELINE')


def sig(r):
    return tuple((c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None) for c in r)


def area_of(t):
    return 'A' if 'AREA A' in t else 'φ and √2' if 'AREA φ' in t else 'B' if 'AREA B' in t else 'none'


def split(ws):
    rest, stars, tl, titles, blk = [], {}, {}, [], None
    for r in ws.iter_rows():
        v = [c.value for c in r]
        if not any(x is not None for x in v):
            continue
        a = str(v[0] or '')
        if a.startswith('SKY STARS') and v[1] is None:     # block titles (counts)
            titles.append(a[:120]); blk = area_of(a); continue
        if a == 'SKY STARS':
            stars[(v[2], v[3])] = (blk, sig(r)); continue
        if a.startswith(('TIMELINE (', 'LONG TIMELINE (')) or a in TL and v[1] is None and str(v[3] or '').startswith('———'):
            titles.append((a[:60] + ' ' + str(v[3] or ''))[:200] if a in TL else a[:60]); continue
        if a in TL:
            k = (a, v[4], v[5], v[6], v[7]) if v[4] else (a, v[3])
            tl[k] = (v, sig(r)); continue
        rest.append(sig(r))
    return rest, stars, tl, titles


b, a = openpyxl.load_workbook(sys.argv[1]), openpyxl.load_workbook(sys.argv[2])
bad = []
assert b.sheetnames == a.sheetnames
for sh in b.sheetnames:
    if sh != 'SKY JUPITER':
        if [sig(r) for r in b[sh].iter_rows() if any(c.value is not None for c in r)] != \
           [sig(r) for r in a[sh].iter_rows() if any(c.value is not None for c in r)]:
            bad.append((sh, 'sheet differs'))
        continue
    (rb, sb, tb, hb), (ra, sa, ta, ha) = split(b[sh]), split(a[sh])
    if rb != ra:
        bad.append((sh, 'other rows differ', len(rb), len(ra)))
    gone, new = [k for k in sb if k not in sa], [k for k in sa if k not in sb]
    changed = [k for k in sb if k in sa and sb[k] != sa[k]]
    cnt = lambda d: {ar: sum(1 for x in d.values() if x[0] == ar) for ar in ('A', 'φ and √2', 'B', 'none')}
    print('SKY STARS rows per area before', cnt(sb), '-> after', cnt(sa))
    print('  gone', len(gone), 'all Polaris:', all('Polaris' in k[0] for k in gone), '; new', len(new), 'all with a new star:',
          all(NEW.search(k[0]) for k in new), '; old rows changed:', len(changed), changed[:3])
    print('  new rows per area', {ar: sum(1 for k in new if sa[k][0] == ar) for ar in ('A', 'φ and √2', 'B', 'none')})
    for t in ('TIMELINE', 'LONG TIMELINE'):
        kb = [k for k in tb if k[0] == t]; ka = [k for k in ta if k[0] == t]
        g, n = [k for k in kb if k not in ta], [k for k in ka if k not in tb]
        ch = [k for k in kb if k in ta and tb[k][1] != ta[k][1]]
        print(f'{t}: before {len(kb)} rows, after {len(ka)}; gone {len(g)}, new {len(n)}, changed {len(ch)}')
        for k in g:
            print('   - gone', tb[k][0][1:8], 'Polaris' in str(k))
        for k in n:
            print('   + new ', ta[k][0][1:8], bool(NEW.search(str(k))))
        for k in ch:
            print('   ~ changed', k, [(x, y) for x, y in zip(tb[k][0], ta[k][0]) if x != y][:4])
    print('titles before:', [x for x in hb if 'TIMELINE' in x or '———' in x])
    print('titles after: ', [x for x in ha if 'TIMELINE' in x or '———' in x])
    print('SKY STARS titles after:', [x for x in ha if x.startswith('SKY STARS')])
print('differences outside SKY STARS / TIMELINE / LONG TIMELINE:', len(bad), bad[:4])
