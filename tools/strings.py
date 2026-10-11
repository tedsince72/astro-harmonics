#!/usr/bin/env python3
"""strings.py WBDIR [-v]  (Eddie 11 Oct 2026: 'for each runner, find the natal links that sky bodies strike in more than one way'.
Rules fixed BEFORE running on any race; Newcastle AW 12:20 and 15:40 (12 Nov 2021) were the two races that suggested them.)

For every natal body X (non-star, no Moon) in the horse chart (H) and jockey chart (J), four ways it can be struck on the day:
 P  position   : a moving sky body (non-star, no Moon) at a whole number (±0.005) or ninth (±0.0005) to natal X, RA or Dec.
 N  same number: X has a natal link to Y in the same chart (RA < 1.5, or Dec < 0.6, or RA/Dec whole/ninth; Y non-star);
                 a sky pair with at least one moving body (not the pair X–Y itself, not star–star, no Moon) equals that
                 link's RA or Dec value (value >= 0.5) within ±0.002, same plane.
 R  ratio      : sky X–Y / natal X–Y (Y non-star, RA or Dec, both >= 0.5) = p/q, q <= 9, p <= 30, ratio != 1, within 0.005%.
 B  same body  : sky X, horse X, jockey X form a set (RA, Dec or Equator) whose three ratios (p/q, q <= 9) are all within 0.15%;
                 credited to X in both charts.
Rahu and Ketu are one node axis ('Nodes'), on both the natal and the sky side; duplicate items are counted once.
Runner score = the best body: number of ways (0-4), then number of items.   Stars never count."""
import sys, glob, math, itertools, openpyxl
D = sys.argv[1]; V = '-v' in sys.argv
BOD = ['Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','Ceres','Pallas','Juno','Vesta','Rahu','Ketu',
       'Eris','Sedna','Haumea','Makemake','Gonggong','Quaoar','Orcus','Transpluto']
NODE = lambda b: 'Nodes' if b in ('Rahu', 'Ketu') else b
rd = lambda a, b: abs((a[0] - b[0] + 180) % 360 - 180); dd = lambda a, b: abs(a[1] - b[1])
def on(v):
    w = round(v); q = round(v * 9)
    if abs(v - w) <= 0.005 and w > 0: return f'{w}'
    if abs(v - q / 9) <= 0.0005 and q % 9: return f'{q}/9'
    return None
def frac(x, pmax=None):
    best = (9, '')
    for q in range(1, 10):
        p = round(x * q)
        if p >= q and (pmax is None or p <= pmax):
            e = abs(x - p / q) / (p / q); g = math.gcd(p, q)
            if e < best[0]: best = (e, f'{p // g}/{q // g}' if q // g > 1 else f'{p // g}')
    return best
def load(wb, t):
    P, St = {}, {}
    for r in list(wb[t].iter_rows(values_only=True))[1:]:
        b = r[1]
        if not isinstance(r[4], (int, float)): continue
        if b in BOD: P[b] = (float(r[4]), float(r[8]))
        elif isinstance(b, str) and b.endswith('_B'): St[b[:-2] + '*'] = (float(r[4]), float(r[8]))
    return P, St
def score(f):
    wb = openpyxl.load_workbook(f, data_only=True)
    (S, SS), (H, _), (J, _) = load(wb, 'TRANS'), load(wb, 'P01'), load(wb, 'P02')
    nm = f"{wb['P01'].cell(2, 1).value} / {wb['P02'].cell(2, 1).value}"
    hits = {}   # (chart, body) -> {way: set(items)}
    add = lambda c, x, w, it: hits.setdefault((c, NODE(x)), {}).setdefault(w, set()).add(it)
    # sky pair values (at least one moving body, no star-star) for N
    skyall = {**S, **SS}; sp = []
    for a, b in itertools.combinations(skyall, 2):
        if a.endswith('*') and b.endswith('*'): continue
        sp.append((a, b, 'RA', rd(skyall[a], skyall[b]))); sp.append((a, b, 'Dec', dd(skyall[a], skyall[b])))
    for c, N in (('H', H), ('J', J)):
        for x in N:
            # P
            for s in S:
                for pl, v in (('RA', rd(S[s], N[x])), ('Dec', dd(S[s], N[x]))):
                    if pl == 'RA' and 'Nodes' in (NODE(s), NODE(x)): v = min(v, 180 - v)   # node axis: v and 180-v are one strike (checker 11 Oct)
                    if v >= 0.5 and on(v): add(c, x, 'P', f'sky {NODE(s)}->{pl} {on(v)}')
            for y in N:
                if y == x or {x, y} == {'Rahu', 'Ketu'}: continue
                nr, nd = rd(N[x], N[y]), dd(N[x], N[y])
                # N
                if nr < 1.5 or nd < 0.6 or on(nr) or on(nd):
                    for pl, v in (('RA', nr), ('Dec', nd)):
                        if v < 0.5: continue
                        for a, b, spl, sv in sp:
                            if spl == pl and abs(sv - v) <= 0.002 and {a, b} != {x, y}:
                                add(c, x, 'N', f'{x}-{NODE(y)} {pl} {v:.3f} = sky {a}-{b}')
                # R
                for pl, sv, nv in (('RA', rd(S[x], S[y]), nr), ('Dec', dd(S[x], S[y]), nd)):
                    if sv < 0.5 or nv < 0.5: continue
                    e, fr = frac(max(sv, nv) / min(sv, nv), 30)
                    if fr and fr != '1' and e <= 0.00005: add(c, x, 'R', f'{x}-{NODE(y)} {pl} sky/natal {fr}')
    # B
    for x in BOD:
        s, h, j = S[x], H[x], J[x]
        sets = {'RA': (rd(s, h), rd(h, j), rd(s, j)), 'Dec': (dd(s, h), dd(h, j), dd(s, j)), 'Equator': (abs(s[1]), abs(h[1]), abs(j[1]))}
        for pl, v in sets.items():
            if min(v) < 0.5: continue
            rs = [frac(max(a, b) / min(a, b)) for a, b in itertools.combinations(v, 2)]
            if max(e for e, _ in rs) <= 0.0015:
                for c in 'HJ': add(c, x, 'B', f'{pl} ' + ':'.join(f for _, f in rs))
    rows = sorted(((len(w), sum(len(i) for i in w.values()), c, b, w) for (c, b), w in hits.items()), reverse=True)
    return nm, rows
races = sorted(glob.glob(f'{D}/*/')) if not glob.glob(f'{D}/*.xlsx') else [D]
for R in races:
    res = [(score(f), f) for f in sorted(glob.glob(f'{R.rstrip("/")}/*.xlsx'))]
    res.sort(key=lambda t: (t[0][1][0][0], t[0][1][0][1]) if t[0][1] else (0, 0), reverse=True)
    print(f"\n== {R.rstrip('/').split('/')[-1]}")
    print(f"   {'pair':42s} ways items  best body   (bodies with 3+ ways)")
    for (nm, rows), f in res:
        w, n, c, b, ways = rows[0]
        many = [f'{cc} {bb}({ww})' for ww, _, cc, bb, _ in rows if ww >= 3]
        print(f"   {nm:42s} {w:4d} {n:5d}  {c} {b:10s} {''.join(sorted(ways))}   {', '.join(many)}")
        if V:
            for ww, nn, cc, bb, wy in rows[:3]:
                print(f"        {cc} {bb} ({ww} ways, {nn} items)")
                for k in sorted(wy): print(f"           {k}: " + '; '.join(sorted(wy[k])))
