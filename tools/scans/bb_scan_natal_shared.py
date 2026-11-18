"""Scan 3 of 4 on natal pairs (18 Nov 2026, Eddie; read-only). 'Horse and jockey share it': the same natal pair X – Y (natal bodies, no
Moon, not Rahu – Ketu) scores in a number family on the SAME family + target in the horse chart and in the jockey chart (each plane on
its own: H X – H Y in RA or Dec, J X – J Y in RA or Dec), at least one of the two >= CUT, the other any score.
Split: 'fixed' = both bodies within 2 degrees of each other's place in the two charts (H X ~ J X and H Y ~ J Y in RA and Dec: slow bodies,
the pair is the same by itself) / 'moved'; and by whether the sky pair S X – S Y scores (any number family) - 'sky live' / 'sky quiet'.
Holdings (runner × pair) / won / by chance (1 / field size), by the shared family. Runner level: runners holding >= 1, 2, 3 moved shares.
  python3 tools/scans/bb_scan_natal_shared.py [cut]"""
import sys, os
ANY = '--any' in sys.argv   # looser (Eddie, 18 Nov 2026): the pair scores >= CUT in BOTH charts, any targets; family 'X' = both on X, 'X / Y' mixed
_a = [a for a in sys.argv[1:] if not a.startswith('--')]
CUT = float(_a[0]) if _a else 90
del sys.argv[1:]
import openpyxl
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as NEG
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT

PAIRS = [(X, Y) for i, X in enumerate(NAT) for Y in NAT[i + 1:] if {X, Y} != {'Rahu', 'Ketu'}]


def lines(pos, ra, X, Y):
    out = {}
    for pl in ('RA', 'Dec'):
        a, b = P(pos, ra, X, pl), P(pos, ra, Y, pl)
        if a is None or b is None:
            continue
        d = dist(a, b, pl)
        for h in nums(d, pl):
            k = (h[0], h[1])
            if k not in out or h[2] > out[k][0]:
                out[k] = (h[2], f'{pl} {d:.4f} {B.txt(h)}')
    return out


def main():
    races = [(r, w) for r, w in NEG.RACES if os.path.exists(f'reference/classic/race_batch_{r}_active.xlsx')]
    g = {}; run = {}; ex = []; pw = {}
    for race, win in races:
        path = f'reference/classic/race_batch_{race}_active.xlsx'
        runners, tt, tp = B.load(path)
        tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
        N = len(runners)
        skylive = {}
        for X, Y in PAIRS:
            skylive[(X, Y)] = bool(lines(tp, tr, X, Y))
        for cloth, r in runners.items():
            won = win.lower() in str(r['name'].get('H', '')).lower()
            ph, rh = r['pos'].get('H', {}), r.get('ra', {}).get('H', {})
            pj, rj = r['pos'].get('J', {}), r.get('ra', {}).get('J', {})
            if not ph or not pj:
                continue
            def near(b):
                m = [dist(P(ph, rh, b, pl), P(pj, rj, b, pl), pl) for pl in ('RA', 'Dec')
                     if P(ph, rh, b, pl) is not None and P(pj, rj, b, pl) is not None]
                return bool(m) and max(m) <= 2
            nm = 0
            for X, Y in PAIRS:
                lh, lj = lines(ph, rh, X, Y), lines(pj, rj, X, Y)
                if ANY:
                    bh = [(v[0], kk) for kk, v in lh.items() if v[0] >= CUT]; bj = [(v[0], kk) for kk, v in lj.items() if v[0] >= CUT]
                    if not bh or not bj:
                        continue
                    kh, kj = max(bh)[1], max(bj)[1]
                    fam = kh[0] if kh[0] == kj[0] else ' / '.join(sorted((kh[0], kj[0])))
                    k = (fam, kh[1]); lh = {k: lh[kh]}; lj = {k: lj[kj]}
                else:
                    sh = [(max(lh[k][0], lj[k][0]), k) for k in lh.keys() & lj.keys() if max(lh[k][0], lj[k][0]) >= CUT]
                    if not sh:
                        continue
                    sc, k = max(sh)
                fx = 'fixed' if near(X) and near(Y) else 'moved'
                sk = 'sky live' if skylive[(X, Y)] else 'sky quiet'
                for key in ((k[0], fx), ('all', fx), (k[0], fx + ', ' + sk), ('all', fx + ', ' + sk)):
                    t = g.setdefault(key, [0, 0, 0.0]); t[0] += 1; t[1] += won; t[2] += 1 / N
                if fx == 'moved':
                    nm += 1
                    p = pw.setdefault(f'{X} – {Y}', [0, 0, 0.0]); p[0] += 1; p[1] += won; p[2] += 1 / N
                    if won:
                        ex.append(f'{win}: H {X} – H {Y} {lh[k][1]} | J {X} – J {Y} {lj[k][1]} ({sk})')
            for kk in (1, 2, 3):
                if nm >= kk:
                    t = run.setdefault(kk, [0, 0, 0.0]); t[0] += 1; t[1] += won; t[2] += 1 / N
    cols = ['moved', 'moved, sky live', 'moved, sky quiet', 'fixed']
    print(f'# Same natal pair in horse and jockey, ' + (f'both charts >= {CUT:g}, any targets' if ANY else f'same number, one side >= {CUT:g}') + f' ({len(races)} result races)\n')
    print('Holdings / won / by chance (ratio), by the shared family. fixed = both bodies within 2 degrees between the two charts.\n')
    print('| family | ' + ' | '.join(cols) + ' |')
    print('|---|' + '---|' * len(cols))
    fams = sorted({f for f, c in g if f != 'all'}, key=lambda f: -g.get((f, 'moved'), [0])[0]) + ['all']
    for f in fams:
        cells = []
        for c in cols:
            h, w, ch = g.get((f, c), [0, 0, 0.0])
            cells.append(f'{h} / {w} / {ch:.1f} ({w / ch if ch else 0:.2f})')
        print(f'| {f} | ' + ' | '.join(cells) + ' |')
    print('\nRunners by number of moved shared pairs: ' + '; '.join(f'>= {k}: {v[0]} / {v[1]} / {v[2]:.1f}' for k, v in sorted(run.items())))
    print('\nPairs (moved) with >= 2 winners: ' + ', '.join(f'{p} {v[0]} / {v[1]} / {v[2]:.1f}' for p, v in
                                                       sorted(pw.items(), key=lambda kv: -kv[1][1]) if v[1] >= 2) + '\n')
    print(f'### winners (moved, {len(ex)})')
    for x in ex[:60]:
        print(f'- {x}')


if __name__ == '__main__':
    main()
