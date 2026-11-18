"""Uranus echo (Newcastle AW 14:20 11 Dec 2021, Coltrane 6/4F last; 18 Nov 2026, Eddie: 'this echo with uranus'): S Sun → J Sun Dec 44.458838
ninth 44.4444 (83.81) carried by S Haumea – S Fomalhaut Dec 44.480695 (59.22) and S Uranus – S Fomalhaut Dec 44.393226 (42.38). Read-only.
Per runner, a line with a score carried ('S' rows, match = the line) by:
  SB2  same-body line (S X → H X / J X) with 2+ carriers sharing a royal star
  SBU  same-body line with a carrier S Uranus – S <royal star>
  SB2U both (Coltrane's shape)
  ANY2U any line (royal lines incl.) with 2+ carriers sharing a royal star, one of them S Uranus – S <that star>
--num: number families only. picks / won / by chance over the result races; favourites holding (from bb_favs_outer_uranus.FAV) and won."""
import sys, re
NUM = '--num' in sys.argv  # number families only (read before the imports: one of them resets sys.argv)
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NG
from bb_favs_outer_uranus import FAV
ROYAL = ('Aldebaran', 'Regulus', 'Antares', 'Fomalhaut')
NONNUM = ('conj', 'contraparallel', 'opposition')


def ends(name):
    return [p.strip()[2:] for p in name.split('–')]


def shapes(D):
    got = {k: [] for k in ('SB2', 'SBU', 'SB2U', 'ANY2U')}
    for X, B in D.items():
        car = {}
        for r in B['S']:
            if r.get('sc') is None or not r.get('match'): continue
            car.setdefault(r['match'], []).append(r)
        for m, rs in car.items():
            same = bool(re.match(rf'S {re.escape(X)} → [HJ] {re.escape(X)} ', m))
            seen = {}
            for r in rs: seen.setdefault((r['line'], r['plane']), r)
            rs = list(seen.values())  # one carrier pair counted once (a pair can score in two families)
            if NUM and (any(r['fam'] in NONNUM for r in rs) or 'contraparallel' in m): continue
            stars = {}
            for r in rs:
                for e in ends(r['line']):
                    if e in ROYAL: stars.setdefault(e, []).append(r)
            two = [s for s, v in stars.items() if len(v) >= 2]
            uro = [r for r in rs if 'Uranus' in ends(r['line']) and any(e in ROYAL for e in ends(r['line']))]
            u2 = [s for s in two if any('Uranus' in ends(r['line']) for r in stars[s])]
            txt = f"{m} by " + '; '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})" for r in rs)
            if same and two: got['SB2'].append(txt)
            if same and uro: got['SBU'].append(txt)
            if same and u2: got['SB2U'].append(txt)
            if u2: got['ANY2U'].append(txt)
    return got


def main():
    keys = ('SB2', 'SBU', 'SB2U', 'ANY2U')
    tot = {k: [0, 0, 0.0, [], 0, 0] for k in keys}
    print('# Uranus echo: lines carried by sky pairs sharing a royal star\n')
    for race, win in NG.RACES:
        R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'); N = len(R); fav = FAV.get(race)
        print(f'## {race} ({N} ran, winner {win}, favourite {fav or "?"})')
        any_ = False
        for run, D in R.items():
            g = shapes(D)
            for k in keys:
                if g[k]:
                    x = tot[k]; x[0] += 1; x[2] += 1 / N
                    if win in run: x[1] += 1; x[3].append(run)
                    if fav and fav in run:
                        x[4] += 1
                        if win in run: x[5] += 1
            hk = [k for k in keys if g[k]]
            if hk:
                any_ = True
                tag = (' (won)' if win in run else '') + (' (fav)' if fav and fav in run else '')
                print(f"- {run}{tag}: {', '.join(hk)}")
                for t in dict.fromkeys(g['SB2'] + g['SBU'] + g['ANY2U']): print(f'  - {t}')
        if not any_: print('- none')
        print()
    print('## Totals (picks / won / by chance; favourites holding / favourites won)')
    for k, (p, w, ch, ws, fh, fw) in tot.items():
        print(f"- {k}: {p} / {w} / {ch:.1f}; fav {fh} / {fw}  {', '.join(ws)}")


if __name__ == '__main__':
    main()
