"""Which families make up the sky triangles (19 Nov 2026, Eddie: 'can you tell me which families are more involved in the triangles';
read-only). Same triangles as bb_scan_sky_triangles.py. Each side's family = its best number family scoring >= cut in that plane
(an across-plane triangle side takes the plane that closes it; a side scoring in both planes is counted once per plane it can use -
Claude's choice: the best-scoring plane). Counted:
  A  across-plane triangles with >= 1 fast body, cut 50: sides by family; families mix of each triangle (sorted);
     races holding >= 1 such triangle with a side in family F: cover hit / miss, fav won / lost.
  B  lines on the busiest fast body (any score inside tolerance): families of those lines, hit vs miss races.
Chosen after the results.
  python3 tools/scans/bb_scan_sky_triangle_families.py [cut]   (default 50; hub part always any score)"""
import sys, os, itertools, io, contextlib
from collections import Counter, defaultdict
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 50
sys.argv = sys.argv[:1]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_regulus_apex as RA
    import bb_scan_sky_triangles as T
FAST, PTS, NUMF = T.FAST, T.PTS, T.NUMF
FAMS = ['whole', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver']


def best(tt, pl, a, b, cut):
    v = EB.pair(tt, 'S', pl, a, b)
    if v is None:
        return None
    h = [(f, s) for f, l, s in EB.hits(v, pl) if f in NUMF and s >= cut]
    return max(h, key=lambda x: x[1]) if h else None


def race_data(tt):
    E = {}
    for pl in ('RA', 'Dec'):
        for a, b in itertools.combinations(PTS, 2):
            h = best(tt, pl, a, b, CUT)
            if h:
                E[(frozenset((a, b)), pl)] = h
    tris = []
    for a, b, c in itertools.combinations(PTS, 3):
        if not any(x in FAST for x in (a, b, c)):
            continue
        sides = [frozenset((a, b)), frozenset((b, c)), frozenset((a, c))]
        pls = [[pl for pl in ('RA', 'Dec') if (x, pl) in E] for x in sides]
        if all(pls) and not any(all(pl in q for q in pls) for pl in ('RA', 'Dec')):
            fams = [max((E[(x, pl)] for pl in q), key=lambda h: h[1])[0] for x, q in zip(sides, pls)]
            tris.append(dict(pts=(a, b, c), fams=fams, fast=sum(x in FAST for x in (a, b, c))))
    # hub: any score
    deg, lines = Counter(), defaultdict(list)
    for pl in ('RA', 'Dec'):
        for a, b in itertools.combinations(PTS, 2):
            h = best(tt, pl, a, b, 0)
            if h:
                for x in (a, b):
                    if x in FAST:
                        deg[x] += 1
                        lines[x].append(h[0])
    top = max(FAST, key=lambda x: deg[x])
    return tris, top, deg[top], lines[top]


def main():
    rows = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        tris, top, n, hl = race_data(tt)
        fav = F.FAV.get(race)
        rows.append(dict(race=race, cover=T.cover_of(race, win), favwon=(RA.key(fav) == RA.key(win)) if fav else None,
                         tris=tris, top=top, n=n, hl=hl))
    G = [('hit', lambda r: r['cover'] is True), ('miss', lambda r: r['cover'] is False),
         ('fav won', lambda r: r['favwon'] is True), ('fav lost', lambda r: r['favwon'] is False)]
    print(f'# Families in the sky triangles (across planes, >= 1 fast body, cut {CUT:g}) and on the busiest fast body\n')
    print(f'{len(rows)} result races; chosen after the results. Cover hit {sum(map(G[0][1], rows))}, miss {sum(map(G[1][1], rows))}; '
          f'fav won {sum(map(G[2][1], rows))}, lost {sum(map(G[3][1], rows))}.\n')
    print('## A. Triangle sides by family (mean sides per race)\n')
    print('| family | ' + ' | '.join(g for g, _ in G) + ' | all |\n|---|' + '---|' * (len(G) + 1))
    for f in FAMS:
        cells = []
        for g, sel in G + [('all', lambda r: True)]:
            xs = [sum(t['fams'].count(f) for t in r['tris']) for r in rows if sel(r)]
            cells.append(f'{sum(xs) / len(xs):.2f}')
        print(f'| {f} | ' + ' | '.join(cells) + ' |')
    print('\n## A. Races with >= 1 such triangle with a side in the family\n')
    print('| family | races | cover hit | cover miss | miss rate | fav won | fav lost |\n|---|---|---|---|---|---|---|')
    for f in FAMS + ['(no triangle at all)']:
        sel = [r for r in rows if (any(f in t['fams'] for t in r['tris']) if f in FAMS else not r['tris'])]
        h = sum(r['cover'] is True for r in sel); m = sum(r['cover'] is False for r in sel)
        w = sum(r['favwon'] is True for r in sel); l = sum(r['favwon'] is False for r in sel)
        print(f'| {f} | {len(sel)} | {h} | {m} | {m / (h + m):.2f} | {w} | {l} |' if h + m else f'| {f} | {len(sel)} | {h} | {m} | - | {w} | {l} |')
    print('\n## A. Family mix of each triangle (all races)\n')
    mix = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        for t in r['tris']:
            k = ' + '.join(sorted(t['fams']))
            mix[k][0] += 1
            mix[k][1] += r['cover'] is True
            mix[k][2] += r['cover'] is False
    print('| mix | triangles | in hit races | in miss races |\n|---|---|---|---|')
    for k, (n, h, m) in sorted(mix.items(), key=lambda x: -x[1][0]):
        print(f'| {k} | {n} | {h} | {m} |')
    print('\n## B. Lines on the busiest fast body (any score): families\n')
    print('| family | ' + ' | '.join(f'{g} (mean / share)' for g, _ in G) + ' |\n|---|' + '---|' * len(G))
    for f in FAMS:
        cells = []
        for g, sel in G:
            xs = [r for r in rows if sel(r)]
            mean = sum(r['hl'].count(f) for r in xs) / len(xs)
            share = sum(r['hl'].count(f) for r in xs) / max(1, sum(len(r['hl']) for r in xs))
            cells.append(f'{mean:.2f} / {share:.0%}')
        print(f'| {f} | ' + ' | '.join(cells) + ' |')
    print('\n## B. Which fast body is busiest\n')
    print('| body | races | cover hit | cover miss | miss rate | fav won | fav lost |\n|---|---|---|---|---|---|---|')
    for b in FAST:
        sel = [r for r in rows if r['top'] == b]
        h = sum(r['cover'] is True for r in sel); m = sum(r['cover'] is False for r in sel)
        w = sum(r['favwon'] is True for r in sel); l = sum(r['favwon'] is False for r in sel)
        print(f'| {b} | {len(sel)} | {h} | {m} | {(m / (h + m)) if h + m else 0:.2f} | {w} | {l} |')


if __name__ == '__main__':
    main()
