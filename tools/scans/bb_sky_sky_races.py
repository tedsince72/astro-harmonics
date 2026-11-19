"""Sky - sky by race (19 Nov 2026, Eddie: 'what if we look at the sky sky relationships in all the races and compare'; read-only).
Every result race with an _active.xlsx. Sky pairs S X – S Y at the off (natal bodies' sky copies + the four royal stars, no Moon,
no royal – royal, not S Rahu – S Ketu), RA and Dec, best number family (bb_scan_natal_pairs.nums). The sky is the same for every
runner, so this describes the race, not a runner. Races split by the cover of eight: hit (winner a pick) / other (miss or no pick).
Compared: number of scoring pairs (>= 50, 80, 90), the share by family, the bodies most involved, and single pairs (body pair, any
number) found in one group more than the other.
Usage: python3 tools/scans/bb_sky_sky_races.py"""
import sys, os, openpyxl, collections
sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as NG
import bb_cover8_where as W
from bb_cover8 import C
from bb_scan_natal_pairs import nums, P, NAT
from bb_scan_uranus_pairs import dist

PTS = [b for b in NAT if b != 'Moon'] + B.ROYAL


def sky_pairs(race):
    path = f'reference/classic/race_batch_{race}_active.xlsx'
    runners, tt, tp = B.load(path)
    tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
    out = []
    for i, a in enumerate(PTS):
        for b in PTS[i + 1:]:
            if {a, b} == {'Rahu', 'Ketu'} or (a in B.ROYAL and b in B.ROYAL):
                continue
            for pl in ('RA', 'Dec'):
                x, y = P(tp, tr, a, pl), P(tp, tr, b, pl)
                if x is None or y is None:
                    continue
                h = nums(dist(x, y, pl), pl)
                if h:
                    out.append((a, b, pl, h[0][0], h[0][1], h[0][2]))
    return out


def main():
    G = {'hit': [], 'other': []}
    for race, win in NG.RACES:
        if not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
            continue
        runners, hh = W.holders(race)
        w = next(r for r in runners if win in r)
        g = 'hit' if any(set(c) <= hh.get(w, set()) for c in C) else 'other'
        G[g].append((race, sky_pairs(race)))
    print(f"# Sky - sky by race: cover of eight hit ({len(G['hit'])} races) vs other ({len(G['other'])} races)\n")
    print('| | hit | other |\n|---|---|---|')
    for cut in (50, 80, 90):
        m = {g: sum(sum(1 for p in sp if p[5] >= cut) for _, sp in R) / len(R) for g, R in G.items()}
        print(f'| scoring sky pairs >= {cut} per race | {m["hit"]:.1f} | {m["other"]:.1f} |')
    for cut in (90,):
        for fam in ('whole', 'golden', 'phi', 'ninth', 'sqrt2', 'silver'):
            m = {g: sum(sum(1 for p in sp if p[5] >= cut and fam in p[3]) for _, sp in R) / len(R) for g, R in G.items()}
            print(f'| {fam} >= {cut} per race | {m["hit"]:.2f} | {m["other"]:.2f} |')
    for cut in (90,):
        print(f'\n## Bodies in sky pairs >= {cut}: pairs per race\n\n| body | hit | other | other / hit |\n|---|---|---|---|')
        cnt = {g: collections.Counter() for g in G}
        for g, R in G.items():
            for _, sp in R:
                for a, b, pl, f, t, s in sp:
                    if s >= cut:
                        cnt[g][a] += 1; cnt[g][b] += 1
        rows = []
        for body in PTS:
            h, o = cnt['hit'][body] / len(G['hit']), cnt['other'][body] / len(G['other'])
            rows.append((o / h if h else 9.99, body, h, o))
        for r, body, h, o in sorted(rows, reverse=True):
            print(f'| {body} | {h:.2f} | {o:.2f} | {r:.2f} |')
    for cut in (80,):
        print(f'\n## Body pairs (any plane, any number) scoring >= {cut}: share of races holding it\n')
        print('| pair | hit races | other races | hit share | other share |\n|---|---|---|---|---|')
        hold = {g: collections.Counter() for g in G}
        for g, R in G.items():
            for _, sp in R:
                for k in {tuple(sorted((a, b))) for a, b, pl, f, t, s in sp if s >= cut}:
                    hold[g][k] += 1
        keys = set(hold['hit']) | set(hold['other'])
        nh, no = len(G['hit']), len(G['other'])
        sc = []
        for k in keys:
            h, o = hold['hit'][k], hold['other'][k]
            if h + o >= 5:
                sc.append((o / no - h / nh, k, h, o))
        sc.sort()
        for item in sc[:8]:
            d, k, h, o = item
            print(f'| {k[0]} – {k[1]} | {h} | {o} | {h/nh:.2f} | {o/no:.2f} |')
        print('| ... | | | | |')
        for item in sc[-8:]:
            d, k, h, o = item
            print(f'| {k[0]} – {k[1]} | {h} | {o} | {h/nh:.2f} | {o/no:.2f} |')
        print(f'\n({len(sc)} body pairs held in 5+ races; with this many pairs some will differ this much by chance.)')


if __name__ == '__main__':
    main()
