"""Pair tally: positive, negative and neutral pairs (17 Nov 2026, Eddie: 'it will be in pairs - some pairs are positive and some are
negative with some neutral; we should start counting this in the S - S, S - H and S - J'; read-only, counts only, no rule, no pick).
Per runner, from each race's bybody xlsx (score >= CUT, default 80; conj / contraparallel incl.):
  S–H  'S Y → H X'  (sky body Y onto the horse's natal X; Y may be X)
  S–J  'S Y → J X'
  S–S  'S A – S B'  a sky pair carrying one of the runner's lines (the 'Sky lines on the same target' rows), pair names sorted
A pair counts once per runner (either plane). Over the result races: holders / won / by chance (sum of 1/N). Labels, from the races
counted: positive = won >= 2 and won >= 2 × chance; negative = by chance >= 1.5 and won <= chance / 3; else neutral.
  python3 tools/scans/bb_pair_tally.py [CUT]            -> tally over the result races (+ how many labels random winners give)
  python3 tools/scans/bb_pair_tally.py [CUT] --race R   -> race R's runners: their positive / negative pairs, labels from the other races
Labels are in-sample: the honest test is each new race read blind with labels from the races before it."""
import sys, random
ARGS = [a for a in sys.argv[1:]]
RACE = ARGS[ARGS.index('--race') + 1] if '--race' in ARGS else None
NUMS = [a for a in ARGS if a.replace('.', '').isdigit() and a != RACE]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NG
CUT = float(NUMS[0]) if NUMS else 80


def pairs(D):
    out = set()
    for X, d in D.items():
        for r in d['L'] + d['O']:
            ln = r['line']
            if ln.startswith('S ') and '→' in ln and r.get('sc') is not None and r['sc'] >= CUT:
                y, x = ln.split('→'); ch = x.strip()[0]
                out.add((f'S–{ch}', f"S {y[2:].strip()} → {x.strip()}"))
        for r in d['S']:
            if r.get('sc') is not None and r['sc'] >= CUT and r['line'].startswith('S ') and '–' in r['line']:
                a, b = (s.strip()[2:] for s in r['line'].split('–'))
                out.add(('S–S', 'S ' + ' – S '.join(sorted((a, b)))))
    return out


def load(race):
    return {run: pairs(D) for run, D in E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx').items()}


def tally(data, winners, skip=None):
    st = {}
    for (race, win, R), w in zip(data, winners):
        if race == skip:
            continue
        N = len(R)
        for run, ps in R.items():
            for k in ps:
                x = st.setdefault(k, [0, 0, 0.0]); x[0] += 1; x[1] += run == w; x[2] += 1 / N
    return st


def label(p, w, c):
    if w >= 2 and w >= 2 * c:
        return 'positive'
    if c >= 1.5 and w <= c / 3:
        return 'negative'
    return 'neutral'


def main():
    data = [(race, win, load(race)) for race, win in NG.RACES]
    W = [next(r for r in R if win in r) for race, win, R in data]
    if RACE:
        R = load(RACE) if RACE not in [d[0] for d in data] else next(d[2] for d in data if d[0] == RACE)
        st = tally(data, W, skip=RACE)
        print(f'# {RACE}: pairs >= {CUT}, labels from the other {len([d for d in data if d[0] != RACE])} result races\n')
        for run, ps in R.items():
            pos = sorted((k for k in ps if k in st and label(*st[k]) == 'positive'), key=lambda k: -st[k][1])
            neg = sorted((k for k in ps if k in st and label(*st[k]) == 'negative'), key=lambda k: -st[k][2])
            print(f'## {run}: {len(pos)} positive, {len(neg)} negative (of {len(ps)} pairs)')
            for t, ks in (('+', pos), ('−', neg)):
                for k in ks:
                    p, w, c = st[k]; print(f'  {t} {k[0]} {k[1]}: {p} / {w} / {c:.1f}')
        return
    st = tally(data, W)
    print(f'# Pair tally, score >= {CUT}, {len(data)} result races (in-sample labels)\n')
    for grp in ('S–S', 'S–H', 'S–J'):
        ks = [k for k in st if k[0] == grp]
        lab = {k: label(*st[k]) for k in ks}
        print(f"## {grp}: {len(ks)} pairs; positive {sum(v == 'positive' for v in lab.values())}, "
              f"negative {sum(v == 'negative' for v in lab.values())}, neutral {sum(v == 'neutral' for v in lab.values())}")
        for t in ('positive', 'negative'):
            sel = sorted((k for k in ks if lab[k] == t), key=lambda k: (-st[k][1], -st[k][2]) if t == 'positive' else -st[k][2])
            print(f'### {t}')
            for k in sel[:30]:
                p, w, c = st[k]; print(f'- {k[1]}: {p} / {w} / {c:.1f}')
            if len(sel) > 30:
                print(f'  ... {len(sel) - 30} more')
        print()
    random.seed(1); sims = []
    for _ in range(200):
        Wr = [random.choice(list(R)) for race, win, R in data]
        s = tally(data, Wr); sims.append((sum(label(*v) == 'positive' for v in s.values()), sum(label(*v) == 'negative' for v in s.values())))
    real = (sum(label(*v) == 'positive' for v in st.values()), sum(label(*v) == 'negative' for v in st.values()))
    ps = sorted(x[0] for x in sims); ns = sorted(x[1] for x in sims)
    print(f'Random winners (200 draws): positive median {ps[100]}, 95th {ps[190]}; negative median {ns[100]}, 95th {ns[190]}; real {real[0]} / {real[1]}')
    fair = [0, 0.0, 0, 0.0]
    for (race, win, R), w in zip(data, W):
        s = tally(data, W, skip=race); N = len(R)
        net = {run: sum((label(*s[k]) == 'positive') - (label(*s[k]) == 'negative') for k in ps_ if k in s) for run, ps_ in R.items()}
        hi, lo = max(net.values()), min(net.values())
        fair[0] += net[w] == hi; fair[1] += sum(v == hi for v in net.values()) / N
        fair[2] += net[w] == lo; fair[3] += sum(v == lo for v in net.values()) / N
    print(f'Leave one race out, net = positive − negative pairs held: winner top {fair[0]} of {len(data)} ({fair[1]:.1f} by chance), '
          f'bottom {fair[2]} ({fair[3]:.1f} by chance)')


if __name__ == '__main__':
    main()
