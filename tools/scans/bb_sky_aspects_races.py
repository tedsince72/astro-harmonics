"""Sky - sky conjunctions, oppositions and contraparallels by race (19 Nov 2026, Eddie: 'you sometimes struggle with conjunctions and
contra parallels - how did they fit in?'; read-only). The sky - sky scan (bb_sky_sky_races.py) used number families only; this counts
what it left out: conjunction (RA < 1.5 or Dec < 0.3), opposition (RA within 0.75 of 180) and contraparallel (|Dec a + Dec b| < 0.3),
scored as eddie_bybody (linear). Same points (sky bodies, no Moon, + royal stars, no royal - royal, not S Rahu - S Ketu), same split by
the cover of eight (hit / other), with and without the 9 rule-origin races. Per race: number of each kind; per body: lines per race.
Usage: python3 tools/scans/bb_sky_aspects_races.py"""
import sys, os, openpyxl, collections
sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as NG
import bb_cover8_where as W
from bb_cover8 import C
from bb_scan_natal_pairs import P
from bb_scan_uranus_pairs import dist
from bb_sky_sky_races import PTS

ORIG = {'20210402_lingfield_aw_1435', '20200608_haydock_1345', '20240608_beverley_1405', '20240515_york_1545', '20220406_catterick_1440',
        '20231006_fontwell_1530', '20210802_newcastle_aw_1633', '20240515_york_1615', '20240118_chelmsford_aw_1320'}


def aspects(race):
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
                for f, t, s in B.hits(dist(x, y, pl), pl):
                    if f in ('conj', 'opposition'):
                        out.append((a, b, pl, f, s))
                if pl == 'Dec':
                    c = B.contraparallel(x, y)
                    if c:
                        out.append((a, b, pl, 'contraparallel', c[2]))
    return out


def main():
    for excl in (False, True):
        G = {'hit': [], 'other': []}
        for race, win in NG.RACES:
            if (excl and race in ORIG) or not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
                continue
            runners, hh = W.holders(race)
            w = next(r for r in runners if win in r)
            g = 'hit' if any(set(c) <= hh.get(w, set()) for c in C) else 'other'
            G[g].append(aspects(race))
        nh, no = len(G['hit']), len(G['other'])
        print(f"# {'without' if excl else 'with'} the 9 rule-origin races: hit {nh}, other {no}\n")
        print('| kind | per race, hit | per race, other |\n|---|---|---|')
        for kind in ('conj', 'opposition', 'contraparallel'):
            for cut in (0, 50):
                m = {g: sum(sum(1 for x in R if x[3] == kind and x[4] >= cut) for R in L) / len(L) for g, L in G.items()}
                print(f"| {kind}{' >= 50' if cut else ' (any)'} | {m['hit']:.2f} | {m['other']:.2f} |")
        print('\n| body (any kind, any score) | hit | other | other / hit |\n|---|---|---|---|')
        cnt = {g: collections.Counter() for g in G}
        for g, L in G.items():
            for R in L:
                for a, b, pl, f, s in R:
                    cnt[g][a] += 1; cnt[g][b] += 1
        rows = [((cnt['other'][b] / no) / (cnt['hit'][b] / nh) if cnt['hit'][b] else 9.99, b) for b in PTS]
        for r, b in sorted(rows, reverse=True):
            print(f"| {b} | {cnt['hit'][b] / nh:.2f} | {cnt['other'][b] / no:.2f} | {r:.2f} |")
        print()


if __name__ == '__main__':
    main()
