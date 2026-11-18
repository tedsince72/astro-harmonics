"""Negatives as well as positives (Ffos Las 14:20 5 Jan 2022, New Age Dawning; 17 Nov 2026, Eddie: 'maybe we need to find negatives as well
as positives'; read-only). Over the result races (bb_fieldcheck_twoforgold.RACES + Ffos Las 14:20, + Newcastle AW 13:30 and Exeter 14:15, Newcastle AW 14:20 since 18 Nov 2026: 38), holders from each race's bbrules json
(watch-only left out): (1) the winner's place by rule count (most / middle / fewest); (2) wins by rule count band; (3) each rule
picks / won / by chance, those under chance first; (4) rule pairs held by 6+ runners with no winner (by chance >= 1.5)."""
import json, sys, itertools
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_fieldcheck_twoforgold as TG
RACES = TG.RACES + [('20220105_ffos_las_1420', 'New Age Dawning')]
# every result race from now on (Eddie, 18 Nov 2026: 'include every race from now on'); the pair tally and the sky-on-natal scans read this list
RACES += [('20220102_newcastle_aw_1330', 'Venturous'), ('20211216_exeter_1415', 'Deja Vue'),
          ('20211211_newcastle_aw_1420', 'Nicholas T'), ('20211205_huntingdon_1352', 'First Flow')]


def holders(race):
    J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
    h = {r: set() for r in J['runners']}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                h.setdefault(c['runner'], set()).add(rid)
    return J['runners'], h


def main():
    data = [(race, win, *holders(race)) for race, win in RACES]
    print('## 1. Winner by rule count')
    pos = {'most': [0, 0.0], 'fewest': [0, 0.0], 'middle': [0, 0.0]}
    for race, win, runners, hh in data:
        N = len(runners); cnt = {r: len(hh.get(r, ())) for r in runners}
        w = next(r for r in runners if win in r); hi, lo = max(cnt.values()), min(cnt.values())
        tag = 'most' if cnt[w] == hi else 'fewest' if cnt[w] == lo else 'middle'
        for k, test in (('most', hi), ('fewest', lo)):
            n = sum(1 for v in cnt.values() if v == test); pos[k][1] += n / N
        pos['middle'][1] += sum(1 for v in cnt.values() if lo < v < hi) / N
        pos[tag][0] += 1
        rank = sorted(cnt.values(), reverse=True)
        print(f"- {race} {w}: {cnt[w]} rules ({tag}); field {rank}")
    for k, (w, c) in pos.items():
        print(f"  {k}: {w} winners of {len(data)}, {c:.1f} by chance")
    print('\n## 2. Winners by rule count band')
    bands = {}
    for race, win, runners, hh in data:
        for r in runners:
            n = len(hh.get(r, ())); b = '0-5' if n <= 5 else '6-9' if n <= 9 else '10-14' if n <= 14 else '15+'
            x = bands.setdefault(b, [0, 0, 0.0]); x[0] += 1; x[2] += 1 / len(runners)
            if win in r: x[1] += 1
    for b in ('0-5', '6-9', '10-14', '15+'):
        p, w, c = bands.get(b, [0, 0, 0]); print(f"- {b}: {p} / {w} / {c:.1f}")
    print('\n## 3. Each rule: picks / won / by chance (won / chance lowest first)')
    rules = sorted({rid for _, _, _, hh in data for s in hh.values() for rid in s})
    rows = []
    for rid in rules:
        p = w = 0; c = 0.0
        for race, win, runners, hh in data:
            for r, s in hh.items():
                if rid in s:
                    p += 1; c += 1 / len(runners); w += win in r
        rows.append((rid, p, w, c))
    for rid, p, w, c in sorted(rows, key=lambda x: (x[2] / x[3] if x[3] else 9, -x[3])):
        print(f"- {rid}: {p} / {w} / {c:.1f}" + ('   UNDER' if w < c - 1 else ''))
    print('\n## 4. Rule pairs with no winner (6+ picks, by chance >= 1.5)')
    pr = []
    for a, b in itertools.combinations(rules, 2):
        p = w = 0; c = 0.0; races = set()
        for race, win, runners, hh in data:
            for r, s in hh.items():
                if a in s and b in s:
                    p += 1; c += 1 / len(runners); w += win in r; races.add(race)
        if p >= 6 and w == 0 and c >= 1.5:
            pr.append((c, a, b, p, len(races)))
    for c, a, b, p, nr in sorted(pr, reverse=True)[:40]:
        print(f"- {a} + {b}: {p} / 0 / {c:.1f} ({nr} races)")
    print(f"  ({len(pr)} pairs in all)")


if __name__ == '__main__':
    main()


def neg_set(data, skip=None):
    """Negative items from the races other than skip: single rules won < chance − 1; pairs 6+ picks, 0 won, chance >= 1.5."""
    D = [d for d in data if d[0] != skip]
    rules = sorted({rid for _, _, _, hh in D for s in hh.values() for rid in s})
    st = {}
    for race, win, runners, hh in D:
        for r, s in hh.items():
            for k in [(a,) for a in s] + list(itertools.combinations(sorted(s), 2)):
                x = st.setdefault(k, [0, 0, 0.0]); x[0] += 1; x[1] += win in r; x[2] += 1 / len(runners)
    return {k for k, (p, w, c) in st.items() if (len(k) == 1 and w < c - 1) or (len(k) == 2 and p >= 6 and w == 0 and c >= 1.5)}


def negatives():
    data = [(race, win, *holders(race)) for race, win in RACES]
    for label, loo in (('in-sample (negatives from all 35 races)', False), ('leave one race out (negatives from the other 34)', True)):
        print(f'\n## 5. Negatives held per runner, {label}')
        NEG = None if loo else neg_set(data)
        tally = {'fewest': [0, 0.0], 'most': [0, 0.0], 'zero': [0, 0, 0.0]}
        for race, win, runners, hh in data:
            ns = neg_set(data, race) if loo else NEG
            cnt = {}
            for r in runners:
                s = hh.get(r, set())
                cnt[r] = sorted(k for k in ns if set(k) <= s)
            n = {r: len(v) for r, v in cnt.items()}; lo, hi = min(n.values()), max(n.values()); N = len(runners)
            w = next(r for r in runners if win in r)
            tally['fewest'][1] += sum(v == lo for v in n.values()) / N; tally['most'][1] += sum(v == hi for v in n.values()) / N
            tally['fewest'][0] += n[w] == lo; tally['most'][0] += n[w] == hi
            z = [r for r in runners if n[r] == 0]; tally['zero'][0] += len(z); tally['zero'][1] += w in z; tally['zero'][2] += len(z) / N
            if race == '20220105_ffos_las_1420' or not loo:
                print(f"- {race} {w}: " + '; '.join(f"{r} {n[r]}" + (f" ({', '.join('+'.join(k) for k in cnt[r])})" if cnt[r] else '') for r in runners))
        print(f"  winner with the fewest negatives (ties incl.): {tally['fewest'][0]} of {len(data)}, {tally['fewest'][1]:.1f} by chance; "
              f"with the most: {tally['most'][0]}, {tally['most'][1]:.1f}; runners with none: {tally['zero'][0]} picks / {tally['zero'][1]} won / {tally['zero'][2]:.1f}")


if __name__ == '__main__':
    negatives()
