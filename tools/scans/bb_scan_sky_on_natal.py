"""Every sky body on every natal body (17 Nov 2026, Eddie: 'yes, that is exactly what I am looking for' - the Uranus count for every natal
body; read-only). A runner holds pair (Y, X) when 'S Y → H X' or 'S Y → J X' scores >= CUT in either plane (conj / contraparallel incl.;
horse and jockey charts together). Over the result races (36): holders / won / by chance / favourites holding (27 races with a favourite).
Labels: positive = won >= 2 and won >= 2 × chance; negative = by chance >= 1.5 and won <= chance / 3. Versions: any family >= 90, >= 80,
whole family >= 80. Fair check: leave one race out - labels from the other 35, each runner's net = positive − negative pairs held; is the
winner top or bottom of its field?
  python3 tools/scans/bb_scan_sky_on_natal.py [--race R]   (--race: R's runners with labels from all result races)"""
import sys
ARGS = sys.argv[1:]
RACE = ARGS[ARGS.index('--race') + 1] if '--race' in ARGS else None
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_fieldcheck_outer_uranus as O
import bb_favs_outer_uranus as F
VERS = [('any', 90), ('any', 80), ('whole', 80)]


def pairs(D):
    out = {v: set() for v in VERS}
    for X, d in D.items():
        for r in d['L'] + d['O']:
            ln = r['line']
            if not ln.startswith('S ') or '→' not in ln or r.get('sc') is None:
                continue
            y = ln.split('→')[0][2:].strip(); x = ln.split('→')[1].strip()[2:]
            for fam, c in VERS:
                if r['sc'] >= c and (fam == 'any' or r['fam'] == 'whole'):
                    out[(fam, c)].add((y, x))
    return out


def load(race):
    return {run: pairs(D) for run, D in E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx').items()}


def label(w, c):
    return 'positive' if w >= 2 and w >= 2 * c else 'negative' if c >= 1.5 and w <= c / 3 else ''


def tally(data, v, skip=None):
    st = {}
    for race, win, fav, R in data:
        if race == skip:
            continue
        N = len(R)
        for run, P in R.items():
            for k in P[v]:
                x = st.setdefault(k, [0, 0, 0.0, 0]); x[0] += 1; x[1] += win in run; x[2] += 1 / N; x[3] += run == fav
    return st


def main():
    data = []
    for race, win in O.RACES:
        R = load(race)
        fav = next((r for r in R if race in F.FAV and F.FAV[race] in r), None)
        data.append((race, win, fav, R))
    if RACE:
        R = load(RACE)
        for v in VERS:
            st = tally(data, v)
            print(f'## {RACE}: {v[0]} family >= {v[1]}, labels from {len(data)} result races')
            for run, P in R.items():
                pos = sorted(k for k in P[v] if k in st and label(st[k][1], st[k][2]) == 'positive')
                neg = sorted(k for k in P[v] if k in st and label(st[k][1], st[k][2]) == 'negative')
                print(f'- {run}: +{len(pos)} −{len(neg)} net {len(pos) - len(neg):+d}  + ' + ', '.join(f'S {y} → {x}' for y, x in pos)
                      + '  − ' + ', '.join(f'S {y} → {x}' for y, x in neg))
            print()
        return
    print('# Sky bodies on natal bodies (S Y → H or J X), 36 result races\n')
    for v in VERS:
        st = tally(data, v)
        lab = {k: label(s[1], s[2]) for k, s in st.items()}
        print(f"## {v[0]} family >= {v[1]}: {len(st)} pairs; positive {sum(l == 'positive' for l in lab.values())}, "
              f"negative {sum(l == 'negative' for l in lab.values())}")
        for t in ('positive', 'negative'):
            ks = sorted((k for k in st if lab[k] == t), key=lambda k: (k[1], -st[k][2]))
            print(f'### {t} (by natal body)')
            for k in ks:
                p, w, c, fv = st[k]; print(f'- S {k[0]} → {k[1]}: {p} / {w} / {c:.1f} / fav {fv}')
        fair = [0, 0.0, 0, 0.0, 0, 0, 0.0, 0, 0.0]
        for race, win, fav, R in data:
            s = tally(data, v, skip=race); N = len(R)
            net = {run: sum((label(s[k][1], s[k][2]) == 'positive') - (label(s[k][1], s[k][2]) == 'negative') for k in P[v] if k in s)
                   for run, P in R.items()}
            hi, lo = max(net.values()), min(net.values()); w = next(r for r in R if win in r)
            fair[0] += net[w] == hi; fair[1] += sum(x == hi for x in net.values()) / N
            fair[2] += net[w] == lo; fair[3] += sum(x == lo for x in net.values()) / N
            if fav:
                fair[4] += 1; fair[5] += net[fav] == lo; fair[6] += sum(x == lo for x in net.values()) / N
                fair[7] += net[fav] == hi; fair[8] += sum(x == hi for x in net.values()) / N
        print(f'Fair check (leave one race out): winner top net {fair[0]} of {len(data)} ({fair[1]:.1f} by chance), bottom {fair[2]} '
              f'({fair[3]:.1f} by chance); favourite bottom {fair[5]} of {fair[4]} ({fair[6]:.1f} by chance), top {fair[7]} ({fair[8]:.1f} by chance)\n')


if __name__ == '__main__':
    main()
