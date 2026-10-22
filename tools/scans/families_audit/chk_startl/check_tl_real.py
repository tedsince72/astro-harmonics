"""check_tl_real.py (independent checker, 22 Oct 2026): (b) the LONG TIMELINE H / J star events beyond 60 min (linear): own engine
search (sky at m min = POSITIONS value at the off + engine(m) - engine(off), natal fixed; grid 10 min over a day, then 1 h, up to 1 year
each way; nearest crossing, bisection to 0.01 min) against the sheet's real time (index 19); "not within 1 year" confirmed by the same
grid (10 min / 1 h, no sign change). usage: check_tl_real.py tables.xlsx events.pickle"""
import os, pickle, re, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from check_tl_common import *
import swisseph as swe
import celestial_bodies_swisseph as E

wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
D = pickle.load(open(sys.argv[2], 'rb'))
B = tl_blocks(wb['P01'])
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe'))
LAT, LON, ELEV = 51.4082, -0.6187, 43.0
swe.set_topo(LON, LAT, ELEV)
JD0 = swe.julday(2012, 6, 19, 13.5)      # 14:30 BST = 13:30 UT
BEH = dict(E.BEHENIAN_STARS)

GRID = np.array(sorted(set([0.0] + [s * 10.0 * k for k in range(1, 145) for s in (1, -1)] +
                           [s * 60.0 * k for k in range(25, 8761) for s in (1, -1)])))
cache = {}


def eng(name, m):
    jd = JD0 + m / 1440.0
    if name == 'Jupiter':
        r = E._calc('Jupiter', swe.JUPITER, jd)
        return r[0], r[1]
    return E._star(name, BEH.get(name, name), jd)


def series(name):
    if name not in cache:
        arr = np.array([eng(name, m) for m in GRID])
        cache[name] = arr
    return cache[name]


sky, ch = D['sky'], D['ch']


def pos_grid(p):
    if p[0] != 'S':
        ra, dec = ch[p[0]][p[1]]
        return np.full(len(GRID), ra), np.full(len(GRID), dec)
    arr = series(p[1])
    i0 = int(np.where(GRID == 0.0)[0][0])
    ra0, dec0 = sky[p[1]][0], sky[p[1]][1]
    dra = (arr[:, 0] - arr[i0, 0] + 180.0) % 360.0 - 180.0
    return ra0 + dra, dec0 + (arr[:, 1] - arr[i0, 1])


def pos_at(p, m):
    if p[0] != 'S':
        return ch[p[0]][p[1]]
    e, e0 = eng(p[1], m), eng(p[1], 0.0)
    return (sky[p[1]][0] + wrap180(e[0] - e0[0]), sky[p[1]][1] + (e[1] - e0[1]))


def dgrid(a, b, plane):
    if plane == 'RA':
        d = np.abs(a[0] - b[0]) % 360.0
        return np.minimum(d, 360.0 - d)
    if plane == 'Dec':
        return np.abs(a[1] - b[1])
    return np.abs(np.abs(a[1]) - np.abs(b[1]))


def f_grid(form):
    if form[0] == 'd':
        return dgrid(pos_grid(form[2]), pos_grid(form[3]), form[1])
    _, pl, X, N, Dn = form
    x = pos_grid(X)
    return dgrid(x, pos_grid(N), pl) / dgrid(x, pos_grid(Dn), pl)


def f_at(form, m):
    return fval(form, lambda p: pos_at(p, m))


def search(form, target):
    g = f_grid(form) - target
    i0 = int(np.where(GRID == 0.0)[0][0])
    best = None
    # outward on each side: the first bracket
    for step in (1, -1):
        i = i0
        while 0 <= i + step < len(GRID):
            j = i + step
            if g[i] == 0 or np.sign(g[i]) != np.sign(g[j]):
                lo, hi = (GRID[i], GRID[j])
                cand = (abs(lo), lo, hi)
                if best is None or cand[0] < best[0]:
                    best = cand
                break
            i = j
    if best is None:
        return None
    _, a, b = best
    fa = f_at(form, a) - target
    for _ in range(40):
        c = (a + b) / 2
        fc = f_at(form, c) - target
        if np.sign(fc) == np.sign(fa):
            a, fa = c, fc
        else:
            b = c
        if abs(b - a) < 0.01:
            break
    return (a + b) / 2


bad, n = [], 0
for C in 'HJ':
    blk = f'LONG TIMELINE {C}'
    mine = {e['key']: e for e in D['dump'][blk]}
    for r in B[blk]:
        if r[3] not in STAR_SRC:
            continue
        k = row_key(r, World(sky, ch))
        e = mine[k]
        if abs(e['t']) <= 60:
            if r[19] is None or abs(r[19] - e['t']) > 0.051:
                bad.append(('within 60 linear but real differs', r[4], r[5], r[19], e['t']))
            continue
        n += 1
        real = search(e['form'], e['tv'])
        sheet = r[19]
        ap_sheet = r[11]
        if real is None:
            ok = sheet is None and r[1] == 'not within 1 year'
            ap = 'applying' if e['t'] > 0 else 'separating'
        else:
            ok = sheet is not None and abs(sheet - real) <= 1.0
            ap = 'applying' if real > 0 else 'separating'
        ok = ok and ap == ap_sheet
        print(f"{'ok ' if ok else 'BAD'} {blk} {r[3]:18s} {r[4]:45s} {r[5]:7s} target {e['tv']:.6f} linear {e['t']:+.1f} | sheet "
              f"{sheet} ({r[1]}, {ap_sheet}) | mine {None if real is None else round(real, 2)} ({ap})")
        if not ok:
            bad.append((blk, r[4], r[5], sheet, real))
print('events searched', n, 'MISMATCHES', len(bad))
for b in bad:
    print('  ', b)
