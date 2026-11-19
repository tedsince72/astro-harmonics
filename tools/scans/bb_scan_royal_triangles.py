"""Triangles with a royal star (19 Nov 2026, Eddie: 'do any of these triangles involve the royal stars?'; read-only). As
bb_scan_sky_triangles.py / bb_scan_runner_triangles.py (number families, >= cut, closing only across planes), with Aldebaran,
Antares, Fomalhaut, Regulus allowed as corners:
  SKY  sky triangles with a fast body (Sun, Moon, Mercury, Venus, Mars) and a royal star among the corners (others bodies);
  SR   runner: sky pair S A - S R (R a royal star, A a fast body), S A -> c X and S R -> c X (X a natal body);
  NR   runner: sky pair S A - S B (A or B fast, both bodies), S A -> c R and S B -> c R (R the runner's natal royal star);
  ANY  runner: SR or NR.
Race level: cover hit / miss, favourite won / lost. Runner level: winner top / holds vs chance, and against the cover picks.
Chosen after the results.
  python3 tools/scans/bb_scan_royal_triangles.py [cut]   (default 80)"""
import sys, os, itertools, io, contextlib
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 80
sys.argv = ['x', str(CUT)]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_runner_triangles as RT
    import bb_scan_runner_triangles_cover as C
    import bb_scan_regulus_apex as RA
    import bb_scan_sky_triangles as T
RT.CUT = CUT
FAST, SKY, NAT, ROY = RT.FAST, RT.SKY, RT.NAT, EB.ROYAL


def sky_edges(tt, pts):
    E = {}
    for pl in ('RA', 'Dec'):
        for a, b in itertools.combinations(pts, 2):
            f = RT.fam(EB.pair(tt, 'S', pl, a, b), pl)
            if f:
                E.setdefault(frozenset((a, b)), {})[pl] = f
    return E


def sky_royal_tris(E):
    n = []
    for a, b, c in itertools.combinations(SKY + ROY, 3):
        t = (a, b, c)
        if sum(x in ROY for x in t) != 1 or not any(x in FAST for x in t):
            continue
        if RT.closes([E.get(frozenset(p), {}) for p in ((a, b), (b, c), (a, c))]):
            n.append(t)
    return n


def runner(r, E):
    sr = nr = 0
    for ch in ('H', 'J'):
        d = r['dist'].get(ch)
        if not d:
            continue
        SX = {}
        for pl in ('RA', 'Dec'):
            for a in SKY + ROY:
                for x in NAT + ROY:
                    f = RT.fam(d.get(('S', pl, a, x)), pl)
                    if f:
                        SX.setdefault((a, x), {})[pl] = f
        for X in NAT:   # SR
            for A in FAST:
                for R in ROY:
                    if (A, X) in SX and (R, X) in SX and RT.closes([E.get(frozenset((A, R)), {}), SX[(A, X)], SX[(R, X)]]):
                        sr += 1
        for R in ROY:   # NR
            on = [a for a in SKY if (a, R) in SX]
            for a, b in itertools.combinations(on, 2):
                if (a in FAST or b in FAST) and RT.closes([E.get(frozenset((a, b)), {}), SX[(a, R)], SX[(b, R)]]):
                    nr += 1
    return dict(SR=sr, NR=nr, ANY=sr + nr)


def main():
    rows = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        E = sky_edges(tt, SKY + ROY)
        st = sky_royal_tris(E)
        cnt = {RA.key(r['name'].get('H') or ''): runner(r, E) for r in runners.values()}
        fav = F.FAV.get(race)
        rows.append(dict(race=race, win=RA.key(win), fav=RA.key(fav) if fav else None, cover=T.cover_of(race, win), picks=C.picks_of(race), st=st, cnt=cnt))
    print(f'# Triangles with a royal star, cut {CUT:g} ({len(rows)} result races; chosen after the results)\n')
    print('## Sky triangles with a fast body and a royal star (across planes)\n')
    print('| group | races | mean per race | races with one |\n|---|---|---|---|')
    for g, sel in (('all', lambda r: True), ('cover hit', lambda r: r['cover'] is True), ('cover miss', lambda r: r['cover'] is False),
                   ('fav won', lambda r: r['fav'] and r['fav'] == r['win']), ('fav lost', lambda r: r['fav'] and r['fav'] != r['win'])):
        xs = [len(r['st']) for r in rows if sel(r)]
        print(f'| {g} | {len(xs)} | {sum(xs) / len(xs):.2f} | {sum(x > 0 for x in xs)} |')
    from collections import Counter
    cs = Counter(x for r in rows for t in r['st'] for x in t if x in ROY)
    print('\nRoyal star in them: ' + ', '.join(f'{k} {v}' for k, v in cs.most_common()) + '\n')
    print('## Runners\n')
    print('| count | runners holding | won | by chance | winner top | chance | holder & cover pick (won / by chance) | holder, not pick (won / by chance) |\n'
          '|---|---|---|---|---|---|---|---|')
    for k, lab in (('SR', 'sky royal star + fast body, both on natal X'), ('NR', 'sky pair with a fast body, both on a natal royal star'),
                   ('ANY', 'either')):
        h = w = 0; ch = 0.0; top = 0; ct = 0.0; hp = [0, 0, 0.0]; hn = [0, 0, 0.0]
        for r in rows:
            vals = {x: v[k] for x, v in r['cnt'].items()}
            n = len(vals); mx = max(vals.values()); mn = min(vals.values())
            hold = {x for x, v in vals.items() if v > 0}
            h += len(hold); w += r['win'] in hold; ch += len(hold) / n
            if mx > mn:
                top += vals.get(r['win'], 0) == mx; ct += sum(v == mx for v in vals.values()) / n
            if r['picks'] is not None:
                for s, a in ((hold & r['picks'], hp), (hold - r['picks'], hn)):
                    a[0] += len(s); a[1] += r['win'] in s; a[2] += len(s) / n
        print(f'| {lab} | {h} | {w} | {ch:.1f} | {top} | {ct:.1f} | {hp[0]}: {hp[1]} / {hp[2]:.1f} | {hn[0]}: {hn[1]} / {hn[2]:.1f} |')


if __name__ == '__main__':
    main()
