"""Scan 4 of 4 on natal pairs (18 Nov 2026, Eddie; read-only). 'Natal X's partner sits where sky X lands': a natal pair c X – c Y (c = H or
J; natal bodies, no Moon, not Rahu – Ketu) scoring >= CUT in a number family, and the same-body line S X → c X (sky X to natal X) on the SAME
family + target (any score inside tolerance), either plane each. Checked both ways (X's same-body line, and Y's: S Y → c Y).
Split: 'geometry' = sky X conjunct natal Y in the matching plane (RA < 1.5 / Dec < 0.3 - then S X → c X equals c Y – c X by itself) /
'real'; and sky pair S X – S Y scores (any number family) 'sky live' / 'sky quiet'. Holdings (runner × chart × pair) / won / by chance,
by the shared family.   python3 tools/scans/bb_scan_natal_samebody.py [cut]"""
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
CONJ = {'RA': 1.5, 'Dec': 0.3}


def main():
    races = [(r, w) for r, w in NEG.RACES if os.path.exists(f'reference/classic/race_batch_{r}_active.xlsx')]
    g = {}; ex = []; run = {}; bod = {}
    for race, win in races:
        path = f'reference/classic/race_batch_{race}_active.xlsx'
        runners, tt, tp = B.load(path)
        tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
        N = len(runners)
        live = {}
        for X, Y in PAIRS:
            live[(X, Y)] = any(nums(dist(P(tp, tr, X, pl), P(tp, tr, Y, pl), pl), pl) for pl in ('RA', 'Dec')
                               if P(tp, tr, X, pl) is not None and P(tp, tr, Y, pl) is not None)
        for cloth, r in runners.items():
            won = win.lower() in str(r['name'].get('H', '')).lower()
            nreal = 0
            for ch in ('H', 'J'):
                pos, ra = r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {})
                if not pos:
                    continue
                for X, Y in PAIRS:
                    nat = {}
                    for pl in ('RA', 'Dec'):
                        a, b = P(pos, ra, X, pl), P(pos, ra, Y, pl)
                        if a is None or b is None:
                            continue
                        d = dist(a, b, pl); h = nums(d, pl)
                        if h and h[0][2] >= CUT:
                            nat[(h[0][0], h[0][1])] = f'{ch} {X} – {ch} {Y} {pl} {d:.4f} {B.txt(h[0])}'
                    if not nat:
                        continue
                    hit = None
                    for s, o in ((X, Y), (Y, X)):           # S s → c s on the natal pair's number
                        for pl in ('RA', 'Dec'):
                            sv, nv, ov = P(tp, tr, s, pl), P(pos, ra, s, pl), P(pos, ra, o, pl)
                            if sv is None or nv is None:
                                continue
                            d2 = dist(sv, nv, pl)
                            for x in nums(d2, pl):
                                k = (x[0], x[1])
                                if k in nat:
                                    geo = ov is not None and dist(sv, ov, pl) < CONJ[pl]
                                    cand = (geo, k, s, f'{nat[k]} = S {s} → {ch} {s} {pl} {d2:.4f} {B.txt(x)}')
                                    if hit is None or (hit[0] and not geo):
                                        hit = cand
                    if hit is None:
                        continue
                    geo, k, s, txt = hit
                    gc = 'geometry' if geo else 'real'
                    sk = 'sky live' if live[(X, Y)] else 'sky quiet'
                    for key in ((k[0], gc), ('all', gc), (k[0], gc + ', ' + sk), ('all', gc + ', ' + sk)):
                        t = g.setdefault(key, [0, 0, 0.0]); t[0] += 1; t[1] += won; t[2] += 1 / N
                    if not geo:
                        nreal += 1
                        b_ = bod.setdefault(s, [0, 0, 0.0]); b_[0] += 1; b_[1] += won; b_[2] += 1 / N
                        if won:
                            ex.append(f'{win}: {txt} ({sk})')
            for kk in (1, 2, 3):
                if nreal >= kk:
                    t = run.setdefault(kk, [0, 0, 0.0]); t[0] += 1; t[1] += won; t[2] += 1 / N
    cols = ['real', 'real, sky live', 'real, sky quiet', 'geometry']
    print(f'# Same-body line S X → c X on the number of a natal pair c X – c Y (natal pair >= {CUT:g}; {len(races)} result races)\n')
    print('Holdings / won / by chance (ratio), by the shared family. geometry = sky X conjunct natal Y in that plane.\n')
    print('| family | ' + ' | '.join(cols) + ' |')
    print('|---|' + '---|' * len(cols))
    fams = sorted({f for f, c in g if f != 'all'}, key=lambda f: -g.get((f, 'real'), [0])[0]) + ['all']
    for f in fams:
        cells = []
        for c in cols:
            h, w, ch = g.get((f, c), [0, 0, 0.0])
            cells.append(f'{h} / {w} / {ch:.1f} ({w / ch if ch else 0:.2f})')
        print(f'| {f} | ' + ' | '.join(cells) + ' |')
    print('\nRunners by number of real cases: ' + '; '.join(f'>= {k}: {v[0]} / {v[1]} / {v[2]:.1f}' for k, v in sorted(run.items())))
    print('\nBy the body whose same-body line carries it (real, >= 5 holdings): ' + ', '.join(
        f'{b} {v[0]} / {v[1]} / {v[2]:.1f}' for b, v in sorted(bod.items(), key=lambda kv: -kv[1][0]) if v[0] >= 5) + '\n')
    print(f'### winners (real, {len(ex)})')
    for x in ex[:60]:
        print(f'- {x}')


if __name__ == '__main__':
    main()
