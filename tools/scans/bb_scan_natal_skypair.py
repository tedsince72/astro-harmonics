"""Scan 2 of 4 on natal pairs (18 Nov 2026, Eddie; read-only). 'The same pair is live in the sky': a natal pair c X – c Y (c = H or J;
natal bodies, no Moon, not Rahu – Ketu) scoring >= CUT in a number family (best family + target), split by the sky pair S X – S Y (same
two bodies, either plane, number family, any score inside tolerance):
  'same number' = S X – S Y on the natal pair's family + target; 'other number' = S X – S Y scores on another target; 'not live' = no.
'Same number' is further split 'returned' (both bodies within 2 degrees of their natal places in RA and Dec - the sky pair repeats the
natal one by itself) / 'moved'. Holdings / won / by chance (1 / field size), by the natal pair's family.
  python3 tools/scans/bb_scan_natal_skypair.py [cut]"""
import sys, os
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 90
del sys.argv[1:]
import openpyxl
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as NEG
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT

PAIRS = [(X, Y) for i, X in enumerate(NAT) for Y in NAT[i + 1:] if {X, Y} != {'Rahu', 'Ketu'}]
CLS = ['same number, moved', 'same number, returned', 'other number', 'not live']


def main():
    races = [(r, w) for r, w in NEG.RACES if os.path.exists(f'reference/classic/race_batch_{r}_active.xlsx')]
    g = {}; ex = {}; pairs_w = {}
    for race, win in races:
        path = f'reference/classic/race_batch_{race}_active.xlsx'
        runners, tt, tp = B.load(path)
        tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
        N = len(runners)
        sky = {}
        for X, Y in PAIRS:
            ks = set(); txt = {}
            for pl in ('RA', 'Dec'):
                a, b = P(tp, tr, X, pl), P(tp, tr, Y, pl)
                if a is None or b is None:
                    continue
                for h in nums(dist(a, b, pl), pl):
                    ks.add((h[0], h[1])); txt.setdefault((h[0], h[1]), f'S {X} – S {Y} {pl} {dist(a, b, pl):.4f} {B.txt(h)}')
            sky[(X, Y)] = (ks, txt)
        for cloth, r in runners.items():
            won = win.lower() in str(r['name'].get('H', '')).lower()
            for ch in ('H', 'J'):
                pos, ra = r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {})
                if not pos:
                    continue
                def moved(b):
                    m = [dist(P(tp, tr, b, pl), P(pos, ra, b, pl), pl) for pl in ('RA', 'Dec')
                         if P(tp, tr, b, pl) is not None and P(pos, ra, b, pl) is not None]
                    return not m or max(m) > 2
                for X, Y in PAIRS:
                    nat = None
                    for pl in ('RA', 'Dec'):
                        a, b = P(pos, ra, X, pl), P(pos, ra, Y, pl)
                        if a is None or b is None:
                            continue
                        h = nums(dist(a, b, pl), pl)
                        if h and h[0][2] >= CUT:
                            k = (h[0][0], h[0][1]); ks = sky[(X, Y)][0]
                            cand = (k, f'{ch} {X} – {ch} {Y} {pl} {dist(a, b, pl):.4f} {B.txt(h[0])}')
                            if nat is None or (k in ks and nat[0] not in ks):
                                nat = cand
                    if nat is None:
                        continue
                    k = nat[0]; ks, txt = sky[(X, Y)]
                    if k in ks:
                        cls = 'same number, moved' if (moved(X) or moved(Y)) else 'same number, returned'
                    else:
                        cls = 'other number' if ks else 'not live'
                    for key in ((k[0], cls), ('all', cls)):
                        t = g.setdefault(key, [0, 0, 0.0]); t[0] += 1; t[1] += won; t[2] += 1 / N
                    if cls == 'same number, moved':
                        pw = pairs_w.setdefault(f'{X} – {Y}', [0, 0, 0.0]); pw[0] += 1; pw[1] += won; pw[2] += 1 / N
                        if won:
                            ex.setdefault(k[0], []).append(f'{win}: {nat[1]} = {txt[k]}')
    print(f'# Natal pair live in the sky (natal pair >= {CUT:g}; S X – S Y same / other number / not live; {len(races)} result races)\n')
    print('Holdings / won / by chance (ratio), by the natal pair\'s family.\n')
    print('| family | ' + ' | '.join(CLS) + ' |')
    print('|---|' + '---|' * len(CLS))
    fams = sorted({f for f, c in g if f != 'all'}, key=lambda f: -sum(g.get((f, c), [0])[0] for c in CLS)) + ['all']
    for f in fams:
        cells = []
        for c in CLS:
            h, w, ch = g.get((f, c), [0, 0, 0.0])
            cells.append(f'{h} / {w} / {ch:.1f} ({w / ch if ch else 0:.2f})')
        print(f'| {f} | ' + ' | '.join(cells) + ' |')
    print('\nPairs with >= 2 winners on the same number (moved): ' + ', '.join(
        f'{p} {v[0]} / {v[1]} / {v[2]:.1f}' for p, v in sorted(pairs_w.items(), key=lambda kv: -kv[1][1]) if v[1] >= 2) + '\n')
    for f, xs in ex.items():
        print(f'### winners, {f}, same number (moved) ({len(xs)})')
        for x in xs[:15]:
            print(f'- {x}')


if __name__ == '__main__':
    main()
