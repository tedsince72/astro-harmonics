"""Every natal pair, Venus – Uranus shape (17 Nov 2026, Eddie: 'what other pairs does it work on?'; read-only, no rule).
Shape (from bb_scan_venus_uranus.py): a natal pair c X – c Y (c = H or J, X and Y natal bodies, no Moon, not the chart's own Rahu –
Ketu) scoring >= CUT in a number family (its best family + target; eddie_bybody.hits, conj / opposition / cp out), and a sky line on
the same family + target: any sky pair S A – S B (sky bodies and royal stars, not the Moon, not the sky Rahu – Ketu; A, B may be X or
Y), any plane, any score. Planes RA (wrapped) and Dec (|dDec|), from the _active.xlsx _POS tabs.
Per pair and chart: runners holding it, picks / won / by chance over bb_scan_uranus_pairs.RACES; and the natal line alone."""
import sys, openpyxl
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
from bb_scan_uranus_pairs import RACES, dist

NO = ('conj', 'opposition', 'contraparallel')
NAT = [b for b in B.BODIES if b != 'Moon']
SKYP = NAT + B.ROYAL
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 90


def nums(v, pl):
    return [x for x in B.hits(v, pl) if x[0] not in NO]


def P(pos, ra, n, pl):
    return (ra if pl == 'RA' else pos).get(n)


def sky_keys(tp, tr):
    keys = {}
    for i, a in enumerate(SKYP):
        for b in SKYP[i + 1:]:
            if {a, b} == {'Rahu', 'Ketu'}:
                continue
            for pl in ('RA', 'Dec'):
                pa, pb = P(tp, tr, a, pl), P(tp, tr, b, pl)
                if pa is None or pb is None:
                    continue
                for h in nums(dist(pa, pb, pl), pl):
                    keys.setdefault((h[0], h[1]), []).append(f'S {a} – S {b} {pl} {dist(pa, pb, pl):.4f}')
    return keys


def main():
    stats = {}   # (X, Y, ch) -> [alone p, w, c, with-sky p, w, c, winners]
    for race, win in RACES:
        path = f'reference/classic/race_batch_{race}_active.xlsx'
        runners, tt, tp = B.load(path)
        tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
        keys = sky_keys(tp, tr)
        N = len(runners)
        for cloth, r in runners.items():
            won = win.lower() in str(r['name'].get('H', '')).lower()
            for ch in ('H', 'J'):
                pos, ra = r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {})
                if not pos:
                    continue
                for i, X in enumerate(NAT):
                    for Y in NAT[i + 1:]:
                        if {X, Y} == {'Rahu', 'Ketu'}:
                            continue
                        alone = sky = False
                        for pl in ('RA', 'Dec'):
                            a, b = P(pos, ra, X, pl), P(pos, ra, Y, pl)
                            if a is None or b is None:
                                continue
                            h = nums(dist(a, b, pl), pl)
                            if h and h[0][2] >= CUT:
                                alone = True
                                if (h[0][0], h[0][1]) in keys:
                                    sky = True
                        s = stats.setdefault((X, Y, ch), [0, 0, 0.0, 0, 0, 0.0, []])
                        if alone:
                            s[0] += 1; s[2] += 1 / N; s[1] += won
                        if sky:
                            s[3] += 1; s[5] += 1 / N; s[4] += won
                            if won:
                                s[6].append(win)
    print(f'# Natal pairs, Venus – Uranus shape (natal line >= {CUT:g} + a sky line on the same number; {len(RACES)} result races)\n')
    for ch in ('H', 'J'):
        tot = [sum(v[k] for (x, y, c), v in stats.items() if c == ch) for k in range(6)]
        print(f'## {ch} chart — all pairs pooled: line alone {tot[0]} / {tot[1]} / {tot[2]:.1f}; with sky {tot[3]} / {tot[4]} / {tot[5]:.1f}\n')
        print('| pair | line alone | with a sky line on the number | winners |')
        print('|---|---|---|---|')
        rows = [(k, v) for k, v in stats.items() if k[2] == ch and v[4] >= 2]
        for (X, Y, c), v in sorted(rows, key=lambda kv: (-(kv[1][4] - kv[1][5]), -kv[1][4])):
            print(f'| {X} – {Y} | {v[0]} / {v[1]} / {v[2]:.1f} | {v[3]} / {v[4]} / {v[5]:.1f} | {", ".join(v[6])} |')
        print()


if __name__ == '__main__':
    main()
