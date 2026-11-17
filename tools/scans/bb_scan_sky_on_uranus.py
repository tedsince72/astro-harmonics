"""Every sky body on natal Uranus (17 Nov 2026, Eddie: 'I wonder about other bodies to Uranus as well - some positive and some negative?';
read-only). Per sky body Y (Moon and royal stars incl.), a runner holds 'S Y → H / J Uranus' when that line scores >= CUT in either plane
(conj / contraparallel incl.). Over the result races (bb_fieldcheck_outer_uranus.RACES, 36): holders / won / by chance, and favourites holding
it (27 races with a favourite on file, bb_favs_outer_uranus.FAV). Labels as the pair tally: positive = won >= 2 and won >= 2 × chance;
negative = by chance >= 1.5 and won <= chance / 3. Cuts 50, 80, 90; also the whole-number family alone at >= 80."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_fieldcheck_outer_uranus as O
import bb_favs_outer_uranus as F


def label(w, c):
    return 'positive' if w >= 2 and w >= 2 * c else 'negative' if c >= 1.5 and w <= c / 3 else ''


def main():
    keys = [('any', 50), ('any', 80), ('any', 90), ('whole', 80)]
    st = {k: {} for k in keys}
    favn = 0
    for race, win in O.RACES:
        R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'); N = len(R)
        fav = next((r for r in R if race in F.FAV and F.FAV[race] in r), None)
        for run, D in R.items():
            if 'Uranus' not in D:
                continue
            best = {}
            for r in D['Uranus']['L'] + D['Uranus']['O']:
                ln = r['line']
                if not ln.startswith('S ') or '→' not in ln or r.get('sc') is None or 'Uranus' not in ln.split('→')[1]:
                    continue
                y = ln.split('→')[0][2:].strip()
                best.setdefault(y, []).append(r)
            for (fam, c) in keys:
                for y, rs in best.items():
                    if any(r['sc'] >= c and (fam == 'any' or r['fam'] == 'whole') for r in rs):
                        x = st[(fam, c)].setdefault(y, [0, 0, 0.0, 0])
                        x[0] += 1; x[2] += 1 / N; x[1] += win in run; x[3] += run == fav
    print('# Sky bodies on natal Uranus (S Y → H or J Uranus), 36 result races; fav = favourites holding it (27 races with a favourite)\n')
    for k in keys:
        print(f'## {k[0]} family, score >= {k[1]}: holders / won / by chance / favourites holding')
        for y, (p, w, c, fv) in sorted(st[k].items(), key=lambda kv: (kv[1][1] - kv[1][2])):
            print(f'- S {y}: {p} / {w} / {c:.1f} / fav {fv}' + (f'   {label(w, c).upper()}' if label(w, c) else ''))
        print()


if __name__ == '__main__':
    main()
