"""Field check (16 Nov 2026), the Dettori-day form of the split, next to bb_fieldcheck_split.py (Society Red). Read-only.
Dettori (Ascot 14:35 28 Sep 1996, J): sky Sun between J Sun and J Chiron in Dec; S Sun -> J Sun 20.9999 (21) and S Sun -> J Chiron
7.0139 (7), J Sun - J Chiron 28.0138 (28). From the _active.xlsx _POS tabs (signed Dec), scored with eddie_bybody.hits (linear).
 D1  chart c, bodies X != Y (no Moon): sky X strictly between c X and c Y in Dec, S X -> c X in a family >= 90 (conj never), S X -> c Y in a family
 D2  D1 with S X -> c Y >= 50
 D3  D1 with c X - c Y in a family too (any score)"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody as B
from bb_fieldcheck_split import RACES
BOD = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Chiron',
       'Eris', 'Haumea', 'Makemake', 'Sedna', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto', 'Rahu', 'Ketu']
KEYS = ['D1', 'D2', 'D3']


def best(v):
    h = [x for x in B.hits(v, 'Dec') if x[0] not in ('conj', 'opposition')]
    return h[0] if h else None


def runner(r, tp):
    tg, ex = set(), []
    for c in 'HJ':
        P = r['pos'].get(c) or {}
        for X in BOD:
            if X not in P or X not in tp: continue
            a = best(abs(tp[X] - P[X]))
            if not a or a[2] < 90: continue
            for Y in BOD:
                if Y == X or Y not in P: continue
                lo, hi = sorted((P[X], P[Y]))
                if not lo < tp[X] < hi: continue
                b = best(abs(tp[X] - P[Y]))
                if not b: continue
                w = best(abs(P[X] - P[Y]))
                t = {'D1'} | ({'D2'} if b[2] >= 50 else set()) | ({'D3'} if w else set())
                tg |= t
                ex.append(f"{c} {X}-{Y}: S {X} -> {c} {X} {abs(tp[X]-P[X]):.4f} {a[1]} ({a[2]:.1f}) + S {X} -> {c} {Y} {abs(tp[X]-P[Y]):.4f} "
                          f"{b[1]} ({b[2]:.1f}) = {c} {X} - {c} {Y} {abs(P[X]-P[Y]):.4f}" + (f" {w[1]} ({w[2]:.1f})" if w else ''))
    return tg, ex


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    import os
    for race, win in RACES:
        if not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
            print(f'\n## {race}: no _active.xlsx in the repo, skipped'); continue
        rr, tt, tp = B.load(f'reference/classic/race_batch_{race}_active.xlsx'); N = len(rr)
        held = {k: [] for k in KEYS}; wex = []
        for cl, r in rr.items():
            nm = r['name'].get('H', str(cl)); tg, ex = runner(r, tp)
            for k in tg: held[k].append(nm)
            if win in nm: wex = ex
        print(f"\n## {race} ({N} runners, winner {win})")
        for k in KEYS:
            print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
            tot[k][0] += len(held[k]); tot[k][1] += sum(win in x for x in held[k]); tot[k][2] += len(held[k]) / N
        for x in wex: print('    winner:', x)
    print(f'\n## Totals over the races above (picks / won / by chance)')
    for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
