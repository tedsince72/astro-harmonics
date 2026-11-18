"""Scan 1 of 4 on natal pairs (18 Nov 2026, Eddie: 'do one at a time - especially note the families involved'; read-only).
'Sky lands on the natal pair': a natal pair c X – c Y (c = H or J; natal bodies, no Moon, not the chart's own Rahu – Ketu) scoring >= CUT
in a number family (best family + target; conj / opposition / cp out), and the sky copies it: S Y → c X or S X → c Y on the SAME family +
target (any score inside tolerance). Planes RA / Dec for each line, independently. From the _active.xlsx _POS tabs.
Counts holdings (runner × chart × pair; one per pair even if both directions or both planes) / won / by chance (1 / field size), split by
the family of the natal pair's target, natal pair alone vs with the echo; and runner level (runners holding >= 1 echo, >= 2, >= 3).
Races: bb_scan_negatives.RACES with an _active.xlsx.  python3 tools/scans/bb_scan_natal_echo.py [cut]"""
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


def main():
    races = [(r, w) for r, w in NEG.RACES if os.path.exists(f'reference/classic/race_batch_{r}_active.xlsx')]
    fam = {}     # family -> [alone h, w, c, echo h, w, c]
    run = {}     # k echoes -> [runners, won, chance]
    ex = {}      # family -> winners' examples
    who = {}     # sky body that copies -> echoes
    for race, win in races:
        path = f'reference/classic/race_batch_{race}_active.xlsx'
        runners, tt, tp = B.load(path)
        tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
        N = len(runners)
        for cloth, r in runners.items():
            won = win.lower() in str(r['name'].get('H', '')).lower()
            n_echo = 0
            for ch in ('H', 'J'):
                pos, ra = r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {})
                if not pos:
                    continue
                for X, Y in PAIRS:
                    best = None; echo = None
                    for pl in ('RA', 'Dec'):
                        a, b = P(pos, ra, X, pl), P(pos, ra, Y, pl)
                        if a is None or b is None:
                            continue
                        h = nums(dist(a, b, pl), pl)
                        if not h or h[0][2] < CUT:
                            continue
                        k = (h[0][0], h[0][1])
                        if best is None:
                            best = (k, f'{ch} {X} – {ch} {Y} {pl} {dist(a, b, pl):.4f} {B.txt(h[0])}')
                        for s, n in ((Y, X), (X, Y)):          # S s → c n
                            for pl2 in ('RA', 'Dec'):
                                sv, nv = P(tp, tr, s, pl2), P(pos, ra, n, pl2)
                                if sv is None or nv is None:
                                    continue
                                d2 = dist(sv, nv, pl2)
                                if any((x[0], x[1]) == k for x in nums(d2, pl2)):
                                    echo = echo or (k, best[1] if best[0] == k else f'{ch} {X} – {ch} {Y} {pl} {dist(a, b, pl):.4f} {B.txt(h[0])}',
                                                    f'S {s} → {ch} {n} {pl2} {d2:.4f}')
                    if best is None:
                        continue
                    f = (echo or best)[0][0]
                    t = fam.setdefault(f, [0, 0, 0.0, 0, 0, 0.0])
                    t[0] += 1; t[1] += won; t[2] += 1 / N
                    if echo:
                        t[3] += 1; t[4] += won; t[5] += 1 / N; n_echo += 1
                        sb = echo[2].split(' → ')[0][2:]; who[sb] = who.get(sb, 0) + 1
                        if won:
                            ex.setdefault(f, []).append(f'{win}: {echo[1]} = {echo[2]}')
            for k in (1, 2, 3, 5):
                if n_echo >= k:
                    t = run.setdefault(k, [0, 0, 0.0]); t[0] += 1; t[1] += won; t[2] += 1 / N
    print(f'# Natal pair copied by the sky (natal pair >= {CUT:g}, S Y → c X or S X → c Y on the same number; {len(races)} result races)\n')
    print('Holdings / won / by chance (ratio). Family = the natal pair\'s target family.\n')
    print('| family | natal pair alone | with the sky echo |')
    print('|---|---|---|')
    tot = [0, 0, 0.0, 0, 0, 0.0]
    for f, t in sorted(fam.items(), key=lambda kv: -kv[1][0]):
        tot = [a + b for a, b in zip(tot, t)]
        print(f'| {f} | {t[0]} / {t[1]} / {t[2]:.1f} ({t[1] / t[2]:.2f}) | {t[3]} / {t[4]} / {t[5]:.1f} ({t[4] / t[5] if t[5] else 0:.2f}) |')
    print(f'| all | {tot[0]} / {tot[1]} / {tot[2]:.1f} ({tot[1] / tot[2]:.2f}) | {tot[3]} / {tot[4]} / {tot[5]:.1f} ({tot[4] / tot[5]:.2f}) |\n')
    print('Runners by number of echoed natal pairs: ' + '; '.join(f'>= {k}: {v[0]} / {v[1]} / {v[2]:.1f}' for k, v in sorted(run.items())) + '\n')
    print('Sky body doing the copying (echoes): ' + ', '.join(f'{k} {v}' for k, v in sorted(who.items(), key=lambda kv: -kv[1])) + '\n')
    for f, xs in ex.items():
        print(f'### winners, {f} ({len(xs)})')
        for x in xs[:12]:
            print(f'- {x}')


if __name__ == '__main__':
    main()
