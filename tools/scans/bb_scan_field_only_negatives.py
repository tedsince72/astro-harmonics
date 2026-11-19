"""Field-only negative pairs (19 Nov 2026, Eddie on Spanish Darling, 1/6F, unseated at the start: 'that was the test!!!'; read-only).
Labels from bb_pair_tally (score >= 80, negative = by chance >= 1.5 and won <= chance / 3), each race's labels from the OTHER result races
(leave one race out). A runner's field-only negatives = negative pairs it holds that no other runner in its race holds.
Over every result race: runners with >= k field-only negatives (k = 1..5): picks / won / chance; the same for favourites
(bb_favs_outer_uranus.FAV); the runner(s) with the most field-only negatives in the race; and field-only positives for comparison.
Usage: python3 tools/scans/bb_scan_field_only_negatives.py"""
import sys
sys.argv = sys.argv[:1] + ['80']
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_pair_tally as PT
import bb_scan_negatives as NG
import bb_favs_outer_uranus as FV


def main():
    data = [(race, win, PT.load(race)) for race, win in NG.RACES]
    W = [next(r for r in R if win in r) for race, win, R in data]
    K = range(1, 6)
    allr = {k: [0, 0, 0.0, []] for k in K}; fav = {k: [0, 0, 0.0, []] for k in K}
    pos = {k: [0, 0, 0.0] for k in K}
    top = [0, 0.0, 0]; favs_seen = []
    for (race, win, R), w in zip(data, W):
        st = PT.tally(data, W, skip=race); N = len(R)
        lab = {run: {k for k in ps if k in st and PT.label(*st[k]) == 'negative'} for run, ps in R.items()}
        plab = {run: {k for k in ps if k in st and PT.label(*st[k]) == 'positive'} for run, ps in R.items()}
        fo = {run: len(s - set().union(*(lab[o] for o in R if o != run))) for run, s in lab.items()}
        fp = {run: len(s - set().union(*(plab[o] for o in R if o != run))) for run, s in plab.items()}
        fname = FV.FAV.get(race)
        for run in R:
            for k in K:
                if fo[run] >= k:
                    allr[k][0] += 1; allr[k][1] += run == w; allr[k][2] += 1 / N
                    if fname and fname in run:
                        fav[k][0] += 1; fav[k][1] += run == w; fav[k][2] += 1 / N; fav[k][3].append(f'{fname} ({fo[run]})')
                if fp[run] >= k:
                    pos[k][0] += 1; pos[k][1] += run == w; pos[k][2] += 1 / N
        hi = max(fo.values())
        if hi > 0:
            tops = [r for r in R if fo[r] == hi]; top[0] += w in tops; top[1] += len(tops) / N; top[2] += 1
        if fname:
            fr = next((r for r in R if fname in r), None)
            if fr: favs_seen.append((race, fname, fo[fr], fr == w, hi))
    print(f'## Field-only negative pairs (>= 80, leave one race out) over {len(data)} result races\n')
    print('| field-only negatives | all runners: picks / won / chance | favourites: picks / won / chance | field-only positives: picks / won / chance |')
    print('|---|---|---|---|')
    for k in K:
        a, f, p = allr[k], fav[k], pos[k]
        print(f'| >= {k} | {a[0]} / {a[1]} / {a[2]:.1f} | {f[0]} / {f[1]} / {f[2]:.1f} | {p[0]} / {p[1]} / {p[2]:.1f} |')
    print(f'\nRunner(s) with the most field-only negatives in the race: winner among them {top[0]} of {top[2]} races ({top[1]:.1f} by chance)\n')
    print(f'Favourites on file: {len(favs_seen)}, won {sum(x[3] for x in favs_seen)}')
    for k in K:
        if fav[k][3]: print(f'- favourites with >= {k}: ' + ', '.join(fav[k][3]))


if __name__ == '__main__':
    main()
