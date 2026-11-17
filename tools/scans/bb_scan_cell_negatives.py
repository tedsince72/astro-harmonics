"""Cell-level negatives (17 Nov 2026, Eddie: 'this is what we need to be looking at' - negatives from the losers, at cell level; read-only).
Features per runner from each race's bybody xlsx: one per runner-specific line kind that scores (best family incl. conj / contraparallel) at
>= CUT in either plane: 'S Y → H X', 'S Y → J X' (Y may be X), 'H R – H X', 'J R – J X' (royal), 'H X – J X'. Sky-only lines (S Y – S X)
are the same for every runner and are left out. Over the result races: per feature picks / won / by chance.
Negatives = features with 0 winners, picks >= MINP, by chance >= MINC. Checks:
 (a) how many such features a random choice of winner would give (1,000 draws: each race's winner drawn from its runners),
 (b) leave one race out: negatives from the other races, per race the runner(s) holding the fewest; winner among them vs chance;
     also holders of no negative: picks / won / by chance; and the winner among the runners holding the most."""
import sys, random, json
ARGS = sys.argv[1:]  # read before imports (bb_fieldcheck_twoforgold resets sys.argv)
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NG
RACES = NG.RACES
CUT, MINP, MINC = float(ARGS[0]) if ARGS else 80, 8, 1.5
KINDS = ('S ', 'H ', 'J ')


def feats(D):
    f = set()
    for X, d in D.items():
        for r in d['L'] + d['O']:
            ln = r['line']
            if ln.startswith('S ') and '→' not in ln:
                continue
            if r.get('sc') is None or r['sc'] < CUT:
                continue
            f.add(ln)
    return f


def load():
    out = []
    for race, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        out.append((race, win, {run: feats(D) for run, D in data.items()}))
    return out


def stats(data, winners, skip=None):
    st = {}
    for (race, win, R), w in zip(data, winners):
        if race == skip:
            continue
        N = len(R)
        for run, fs in R.items():
            for k in fs:
                x = st.setdefault(k, [0, 0, 0.0]); x[0] += 1; x[1] += run == w; x[2] += 1 / N
    return st


def negs(st):
    return {k for k, (p, w, c) in st.items() if w == 0 and p >= MINP and c >= MINC}


def main():
    data = load()
    W = [next(r for r in R if win in r) for race, win, R in data]
    st = stats(data, W)
    NEG = negs(st)
    print(f'# Cell-level negatives, score >= {CUT}, {len(data)} result races\n')
    print(f'## Features with no winner (picks >= {MINP}, by chance >= {MINC}): {len(NEG)}')
    for k in sorted(NEG, key=lambda k: -st[k][2])[:40]:
        p, w, c = st[k]; print(f'- {k}: {p} / 0 / {c:.1f}')
    random.seed(1)
    sims = []
    for _ in range(1000):
        Wr = [random.choice(list(R)) for race, win, R in data]
        sims.append(len(negs(stats(data, Wr))))
    sims.sort()
    print(f'\n(a) random winners: median {sims[500]}, 95th percentile {sims[950]}, max {sims[-1]}; real {len(NEG)}')
    few = [0, 0.0]; most = [0, 0.0]; zero = [0, 0, 0.0]
    print('\n(b) leave one race out')
    for (race, win, R), w in zip(data, W):
        ng = negs(stats(data, W, skip=race)); N = len(R)
        n = {run: len(fs & ng) for run, fs in R.items()}
        lo, hi = min(n.values()), max(n.values())
        few[0] += n[w] == lo; few[1] += sum(v == lo for v in n.values()) / N
        most[0] += n[w] == hi; most[1] += sum(v == hi for v in n.values()) / N
        for run, v in n.items():
            if v == 0:
                zero[0] += 1; zero[1] += run == w; zero[2] += 1 / N
        print(f'- {race} {w}: ' + '; '.join(f'{run} {v}' for run, v in n.items()))
    print(f'  winner among the fewest: {few[0]} of {len(data)}, {few[1]:.1f} by chance; among the most: {most[0]}, {most[1]:.1f}; '
          f'no negative: {zero[0]} picks / {zero[1]} won / {zero[2]:.1f}')


if __name__ == '__main__':
    main()
