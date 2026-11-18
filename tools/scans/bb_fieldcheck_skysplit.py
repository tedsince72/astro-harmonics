"""Sky split by X (Newcastle AW 14:20 11 Dec 2021, Nicholas T 14/1 won; 18 Nov 2026, Eddie: 'this is on the winner'): H Fomalhaut – H Mars RA
174.001471 whole 174 (92.64) carried by S Jupiter – S Transpluto RA 173.99685 174 (84.25), and sky Mars splits that pair: S Jupiter – S Mars RA
93.000533 93 (97.33) + S Transpluto – S Mars RA 80.996318 81 (81.59) = 174 (Mars between Jupiter and Transpluto, so the sum is geometry; the
content is both pieces on targets). Read-only.
Per runner and body X: a line on X with a score (royal R – X, or any line on X), carried by a sky pair S Y – S Z (Y, Z not X; 'S' rows, match =
the line), and S Y – S X and S Z – S X in the same plane both in a number family (no conj / cp / opposition) with |d(Y,X) + d(X,Z) − d(Y,Z)| < 0.1.
Versions: R = royal line carried; A = any line on X carried; cut c = both pieces >= c (0, 50, 80); R80L = R with the royal line and carrier >= 80
too. picks / won / by chance; favourites holding / won (bb_favs_outer_uranus.FAV)."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NG
from bb_favs_outer_uranus import FAV
ROYAL = ('Aldebaran', 'Regulus', 'Antares', 'Fomalhaut')
NONNUM = ('conj', 'contraparallel', 'opposition')


def ends(line):
    return [p.strip()[2:] for p in line.split('–')]


def sky(D, X):
    """S Y – S X rows on X (number families) by (Y, plane) -> row."""
    out = {}
    for g in 'LSO':
        for r in D[X][g]:
            if r.get('sc') is None or r['fam'] in NONNUM or '→' in r['line'] or not r['line'].startswith('S '): continue
            e = ends(r['line'])
            if len(e) == 2 and X in e and all(p.strip().startswith('S ') for p in r['line'].split('–')):
                y = e[0] if e[1] == X else e[1]
                if y != X and ((y, r['plane']) not in out or r['sc'] > out[(y, r['plane'])]['sc']): out[(y, r['plane'])] = r
    return out


def cases(D):
    res = []
    for X, B in D.items():
        sk = sky(D, X)
        lines = {f"{r['line']} {r['plane']}": r for r in B['L'] if r.get('sc') is not None}
        for c in B['S']:
            if c.get('sc') is None or not c.get('match') or c['match'] not in lines or c['fam'] in NONNUM: continue
            e = ends(c['line'])
            if len(e) != 2 or X in e or not all(p.strip().startswith('S ') for p in c['line'].split('–')): continue
            a, b = sk.get((e[0], c['plane'])), sk.get((e[1], c['plane']))
            if not a or not b or abs(a['v'] + b['v'] - c['v']) >= 0.1: continue
            L = lines[c['match']]; royal = any(s in L['line'] for s in ROYAL) and '→' not in L['line']
            res.append(dict(X=X, L=L, c=c, a=a, b=b, royal=royal, lo=min(a['sc'], b['sc'])))
    return res


def main():
    keys = [('R', 0), ('R', 50), ('R', 80), ('A', 0), ('A', 50), ('A', 80), ('R80L', 80)]
    tot = {k: [0, 0, 0.0, [], 0, 0] for k in keys}
    print('# Sky split by X: a carrier pair S Y – S Z split by sky X into two pieces on targets\n')
    for race, win in NG.RACES:
        R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'); N = len(R); fav = FAV.get(race)
        print(f'## {race} ({N} ran, winner {win}, favourite {fav or "?"})'); anyp = False
        for run, D in R.items():
            cs = cases(D)
            for k, cut in keys:
                ok = [x for x in cs if x['lo'] >= cut and (k == 'A' or x['royal'])
                      and (k != 'R80L' or (x['L']['sc'] >= 80 and x['c']['sc'] >= 80))]
                if ok:
                    t = tot[(k, cut)]; t[0] += 1; t[2] += 1 / N
                    if win in run: t[1] += 1; t[3].append(run)
                    if fav and fav in run:
                        t[4] += 1
                        if win in run: t[5] += 1
            if cs:
                anyp = True
                print(f"- {run}{' (won)' if win in run else ''}{' (fav)' if fav and fav in run else ''}")
                for x in cs:
                    f = lambda r: f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})"
                    print(f"  - {'royal ' if x['royal'] else ''}{f(x['L'])} by {f(x['c'])} = {f(x['a'])} + {f(x['b'])}")
        if not anyp: print('- none')
        print()
    print('## Totals (picks / won / by chance; favourites holding / won)')
    for (k, c), (p, w, ch, ws, fh, fw) in tot.items():
        print(f"- {k} pieces >= {c}: {p} / {w} / {ch:.1f}; fav {fh} / {fw}  {', '.join(ws)}")


if __name__ == '__main__':
    main()
