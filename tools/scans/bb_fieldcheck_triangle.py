"""Field check (16 Nov 2026, Eddie: 'yes both of those and eris s-h, s-j, h-j'), from The Dunkirk Lads (Nottingham 17:50 13 Jun 2022,
won 12/1). Read-only; winners named below, no results file read. 14 result races, from the bybody xlsx.
The Dunkirk Lads Eris: S Eris -> H Eris RA 1.3332 ninth 1.33333 (94.52), S Eris -> J Eris RA 4.4367 ninth 4.44444 (13.41),
H Eris - J Eris Dec 8.0762 5xphi (56.73): the three lines of one body all on targets (On Time's Jupiter split 'E' in one plane).
 T1   a body X (not the Moon) with S X -> H X, S X -> J X and H X - J X each scoring in a family (conj / cp never), any planes
 T1s  T1 with all three in one plane
 T1f  T1 with the two sky legs S X -> H X, S X -> J X on the same family in the same plane
 T2   T1 with the best of the three >= 90
 T3   T1 with each >= 50
 C1   T1 and BB68 held;  C2  T1 and BB1 held;  C3  T1, BB68 and BB1 (The Dunkirk Lads' three findings)"""
import sys, json
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_split import RACES
RACES = RACES + [('20220613_nottingham_1750', 'The Dunkirk Lads')]
CJ = ('conj', 'contraparallel')
KEYS = ['T1', 'T1s', 'T1f', 'T2', 'T3', 'C1', 'C2', 'C3']
ok = lambda r: r['fam'] and r['fam'] not in CJ and r['sc'] is not None and r['plane'] in ('RA', 'Dec')


def tri(X, d):
    g = {k: [r for r in d['L'] if r['line'] == k and ok(r)] for k in (f'S {X} → H {X}', f'S {X} → J {X}', f'H {X} – J {X}')}
    if not all(g.values()):
        return set(), ''
    a, b, c = g.values()
    t = {'T1'}
    if any(x['plane'] == y['plane'] == z['plane'] for x in a for y in b for z in c): t.add('T1s')
    if any(x['plane'] == y['plane'] and x['fam'] == y['fam'] for x in a for y in b): t.add('T1f')
    best = [max(r['sc'] for r in g_) for g_ in (a, b, c)]
    if max(best) >= 90: t.add('T2')
    if min(best) >= 50: t.add('T3')
    return t, ' | '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})" for g_ in (a, b, c) for r in g_)


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        J = json.load(open(f'docs/eddie_read/bybody_rules/{r}_bbrules.json'))
        hold = {}
        for rid, cs in J['rules'].items():
            for c in cs:
                if not c['watch_only']: hold.setdefault(c['runner'], set()).add(rid)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            tg = set()
            for X, d in D.items():
                if X == 'Moon': continue
                t, s = tri(X, d)
                if t: tg |= t; ex.append(f'{run} {X} [{",".join(sorted(t))}]: {s}')
            h = hold.get(run, set())
            if 'T1' in tg:
                if 'BB68' in h: tg.add('C1')
                if 'BB1' in h: tg.add('C2')
                if {'BB68', 'BB1'} <= h: tg.add('C3')
            for k in tg: held[k].append(run)
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex: print('    ', x)
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
