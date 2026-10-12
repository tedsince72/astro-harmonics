#!/usr/bin/env python3
"""sky_anchored_compare.py [--min N]  — runs sky_anchored_soak over every race already read (winner known; blind races left out)
and compares winners with the other runners: by body name, and for same-afternoon race pairs, anchor by anchor.
The read races are where the checklist came from: what this prints is description, not evidence."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sky_anchored_soak as S

WIN = {'ascot_1350_20231021': 'P01', 'carlisle_1630_20220707': 'P07', 'catterick_1505_20211119': 'P07', 'chelmsford_aw_1320_20240118': 'P03',
       'ffos_las_1420_20220105': 'P05', 'fontwell_1530_20231006': 'P05', 'haydock_1405_20220219': 'P09', 'haydock_1718_20220507': 'P07',
       'huntingdon_1352_20211205': 'P05', 'lingfield_1500_20220123': 'P11', 'newbury_1350_20211126': 'P09', 'newcastle_1540_20220311': 'P05',
       'newcastle_aw_1220_20211112': 'P03', 'newcastle_aw_1330_20220102': 'P09', 'newcastle_aw_1540_20211112': 'P05', 'newcastle_aw_1640_20220215': 'P01',
       'newmarket_1535_20220414': 'P07', 'newton_abbot_1525_20220717': 'P07', 'nottingham_1530_20220601': 'P01', 'nottingham_1750_20220613': 'P03',
       'perth_1610_20220420': 'P09', 'sandown_1425_20211204': 'P05', 'sandown_1430_20240215': 'P13', 'sedgefield_1500_20220510': 'P01',
       'wincanton_1420_20220321': 'P07', 'wolverhampton_aw_1725_20231021': 'P05', 'york_1545_20240515': 'P11', 'york_1615_20240515': 'P25',
       'newmarket_july_1745_20240816': 'P01', 'exeter_1515_20211019': 'P11', 'redcar_1515_20211015': 'P05', 'haydock_1420_20210904': 'P03',
       'kempton_aw_1440_20210904': 'P05'}
PAIRS = [('newcastle_aw_1220_20211112', 'newcastle_aw_1540_20211112'), ('york_1545_20240515', 'york_1615_20240515'),
         ('haydock_1420_20210904', 'kempton_aw_1440_20210904')]

def main(nmin):
    data = {r: S.scan(r, nmin) for r in sorted(WIN)}
    print(f"Sky-anchored soak (>= {nmin} natal partners incl. a horse and a jockey body, +-{S.TOL}); {len(WIN)} read races. NOT evidence: these are the races the checklist came from.")
    # per runner: number of anchors with the soak
    nw = nl = 0; aw = al = 0; byb = {}
    for r, (R, res) in data.items():
        for P in R:
            k = [key for key, (v, row) in res.items() if row[P][1]]
            win = P == WIN[r]; nw += win; nl += not win
            if win: aw += len(k)
            else: al += len(k)
            for b in sorted({fold for key in k for fold in (S.fold(key[0]), S.fold(key[1]))}):
                d = byb.setdefault(b, [0, 0]); d[0 if win else 1] += 1
    print(f"-- anchors per runner (background): winners {aw / nw:.1f} on average ({nw} winners), other runners {al / nl:.1f} ({nl})")
    print("-- by body name: runners with >= 1 sky-anchored soak on an anchor containing that body")
    print(f"   {'body':11s} {'winners':>12s} {'others':>12s}")
    for b, (w, l) in sorted(byb.items(), key=lambda kv: (-(kv[1][0] / nw - kv[1][1] / nl), kv[0])):
        print(f"   {b:11s} {w:3d}/{nw} {100 * w / nw:3.0f}%   {l:3d}/{nl} {100 * l / nl:3.0f}%")
    print("-- same-afternoon pairs: anchors (same sky pair and plane) that BOTH winners have")
    for r1, r2 in PAIRS:
        (R1, s1), (R2, s2) = data[r1], data[r2]; w1, w2 = WIN[r1], WIN[r2]
        both = [k for k in s1 if k in s2 and s1[k][1][w1][1] and s2[k][1][w2][1]]
        print(f"   {r1} (winner {R1[w1][0]}) + {r2} (winner {R2[w2][0]}): {len(both)} anchors shared by both winners")
        for k in sorted(both, key=lambda k: s1[k][0]):
            l1 = [P for P in R1 if P != w1 and s1[k][1][P][1]]; l2 = [P for P in R2 if P != w2 and s2[k][1][P][1]]
            print(f"      sky {k[0]}–{k[1]} {k[2]} {s1[k][0]:.4f} / {s2[k][0]:.4f}: winners {s1[k][1][w1][0]} / {s2[k][1][w2][0]} partners; "
                  f"losers with it {len(l1)}/{len(R1) - 1} and {len(l2)}/{len(R2) - 1}" + ('   <- no loser in either race' if not l1 and not l2 else ''))
            print(f"         {r1[:12]} winner: {', '.join(s1[k][1][w1][2])}")
            print(f"         {r2[:12]} winner: {', '.join(s2[k][1][w2][2])}")
        # control: every pairing of one runner from each race — anchors both have, and anchors both have that nobody else in either race has
        def shared(p1, p2):
            ks = [k for k in s1 if k in s2 and s1[k][1][p1][1] and s2[k][1][p2][1]]
            excl = [k for k in ks if not any(s1[k][1][P][1] for P in R1 if P != p1) and not any(s2[k][1][P][1] for P in R2 if P != p2)]
            return len(ks), len(excl)
        ctl = {(p1, p2): shared(p1, p2) for p1 in R1 for p2 in R2}
        wv = ctl[(w1, w2)]
        rk_all = 1 + sum(1 for v in ctl.values() if v[0] > wv[0]); rk_ex = 1 + sum(1 for v in ctl.values() if v[1] > wv[1])
        print(f"      control: all {len(ctl)} pairings of one runner from each race — shared anchors: winners {wv[0]}, others mean {sum(v[0] for k, v in ctl.items() if k != (w1, w2)) / (len(ctl) - 1):.2f}, "
              f"max {max(v[0] for k, v in ctl.items() if k != (w1, w2))} (winners' rank {rk_all} of {len(ctl)}); "
              f"shared by that pairing only: winners {wv[1]}, others mean {sum(v[1] for k, v in ctl.items() if k != (w1, w2)) / (len(ctl) - 1):.2f}, "
              f"pairings with >= 1: {sum(1 for k, v in ctl.items() if k != (w1, w2) and v[1] >= 1)} of {len(ctl) - 1} (winners' rank {rk_ex})")

if __name__ == '__main__':
    main(int(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 4)
