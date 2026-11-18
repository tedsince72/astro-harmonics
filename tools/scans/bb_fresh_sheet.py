"""Fresh sheet (18 Nov 2026, Eddie: 'what do we have from our first round that is the strongest - include all the races, do not
exclude the ones that the rule came from or only after the rule was formed'; read-only). Every result race in
bb_scan_negatives.RACES, holders from a fresh run of today's eddie_bybody_rules.py (BB1-BB84b) into a scratch folder
(argv[1], default /tmp/fresh; watch-only cases left out). Singles, pairs and triples of rules: picks / won / by chance
(sum of 1 / field size) and the chance of that many wins or more if every holder were a random runner (exact, per race).
Ranked by that chance. Everything in-sample: many combinations are tried, so small chances are expected by luck alone."""
import json, sys, itertools
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as N

D = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isdigit() else "/tmp/fresh"


def holders(race):
    J = json.load(open(f'{D}/{race}_bbrules.json'))
    h = {r: set() for r in J['runners']}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                h.setdefault(c['runner'], set()).add(rid)
    return J['runners'], h


def tail(ps, w):
    """P(wins >= w) for independent picks with win chances ps."""
    dist = [1.0]
    for p in ps:
        nd = [0.0] * (len(dist) + 1)
        for k, v in enumerate(dist):
            nd[k] += v * (1 - p); nd[k + 1] += v * p
        dist = nd
    return sum(dist[w:])


def main():
    data = []
    for race, win in N.RACES:
        runners, hh = holders(race)
        w = [r for r in runners if win in r]
        assert len(w) == 1, (race, win, w)
        data.append((race, w[0], runners, hh))
    rules = sorted({x for *_, hh in data for s in hh.values() for x in s})
    out = {}
    for k in (1, 2, 3):
        rows = []
        for combo in itertools.combinations(rules, k):
            cs = set(combo); ps = []; w = 0; races = set(); wins = []
            for race, win, runners, hh in data:
                for r, s in hh.items():
                    if cs <= s:
                        ps.append(1 / len(runners)); races.add(race)
                        if r == win:
                            w += 1; wins.append(win.split(' ', 1)[-1] if ' ' in win else win)
            if len(ps) < 3 or w < 2:
                continue
            rows.append((tail(ps, w), combo, len(ps), w, sum(ps), len(races), wins))
        rows.sort(key=lambda x: (x[0], -x[3]))
        out[k] = rows
    print(f'# Fresh sheet: {len(data)} result races, rules BB1-BB84b, every race counted (in-sample)\n')
    print('picks / won / by chance; p = chance of that many wins or more by luck\n')
    for k, name in ((1, 'Single rules'), (2, 'Pairs'), (3, 'Triples')):
        print(f'## {name} ({len(out[k])} with 2+ wins and 3+ picks), best 25\n')
        for p, combo, n, w, c, nr, wins in out[k][:25]:
            print(f"- {' + '.join(combo)}: {n} / {w} / {c:.1f}  (p {p:.4f}; {nr} races) - {', '.join(wins)}")
        print()
    # all singles too, for reference
    print('## Every single rule, by p\n')
    for k in (1,):
        pass
    allr = []
    for rid in rules:
        ps = []; w = 0
        for race, win, runners, hh in data:
            for r, s in hh.items():
                if rid in s:
                    ps.append(1 / len(runners)); w += r == win
        allr.append((tail(ps, w) if ps else 1, rid, len(ps), w, sum(ps)))
    for p, rid, n, w, c in sorted(allr):
        print(f'- {rid}: {n} / {w} / {c:.1f} (p {p:.3f})')


if __name__ == '__main__':
    main()
