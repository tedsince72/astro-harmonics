"""check_tl_star.py (independent checker, 22 Oct 2026): (c) STAR TIMELINE (SKY JUPITER) and STAR TIMELINE H / J (runner sheets) = the
TIMELINE / TIMELINE H / J rows whose relationship names only Jupiters and stars (own parser), same cells and order, with the OFF /
OFF + 5 MIN markers. usage: check_tl_star.py tables.xlsx [...]"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from check_tl_common import *
from check67_common import BODIES

NAMES = sorted(set(BODIES) | ALLSTARS, key=len, reverse=True)
RX = re.compile(r'(?:^|(?<=[\s:(,/–=|>]))([SHJ]) (' + '|'.join(re.escape(n) for n in NAMES) + r')(?![A-Za-z])')
APEX = re.compile(r'^(' + '|'.join(re.escape(n) for n in NAMES) + r'): d\(star')


def points(rel):
    pts = [m[2] for m in RX.finditer(rel)]
    m = APEX.match(rel)
    if m:
        pts.append(m[1])
    return pts


def is_star_rel(rel):
    p = points(rel)
    return bool(p) and all(x == 'Jupiter' or x in ALLSTARS for x in p) and any(x in ALLSTARS for x in p)


bad = []
for path in sys.argv[1:]:
    wb = openpyxl.load_workbook(path, read_only=True)
    for sh in wb.sheetnames:
        if sh != 'SKY JUPITER' and not re.fullmatch(r'P\d\d', sh):
            continue
        B = tl_blocks(wb[sh])
        for suf in ([''] if sh == 'SKY JUPITER' else [' H', ' J']):
            src = B.get('TIMELINE' + suf, [])
            dst = B.get('STAR TIMELINE' + suf)
            if dst is None:
                bad.append((path, sh, 'no STAR TIMELINE' + suf))
                continue
            body = lambda rows: [r for r in rows if r[1] != 'exact (race-local)']
            exp = [r for r in body(src) if (r[3] and str(r[3]).startswith('———')) or (r[4] and is_star_rel(str(r[4])))]
            got = body(dst)
            strip = lambda r: tuple(r[1:])
            ok = [strip(a) for a in exp] == [strip(b) for b in got]
            ntl = sum(1 for r in body(src) if r[4])
            nst = sum(1 for r in got if r[4])
            mk = sum(1 for r in got if r[3] and str(r[3]).startswith('———'))
            # unparsed relationships (sanity)
            unp = [r[4] for r in body(src) if r[4] and not points(str(r[4]))]
            print(f'{os.path.basename(path)} {sh} STAR TIMELINE{suf}: TIMELINE events {ntl}, star events {nst}, markers {mk}, '
                  f'= expected {ok}' + (f'; unparsed {unp}' if unp else ''))
            if not ok:
                ea, ga = [strip(a) for a in exp], [strip(b) for b in got]
                bad.append((path, sh, suf, 'expected', len(ea), 'got', len(ga),
                            [x[3] for x in ea if x not in ga][:5], [x[3] for x in ga if x not in ea][:5]))
print('MISMATCHES', len(bad))
for b in bad:
    print('  ', b)
