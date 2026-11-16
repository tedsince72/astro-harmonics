"""Field check (16 Nov 2026, Eddie: '2 high scores in these' - Dynamic Force, Nottingham 15:30 1 Jun 2022, won 18/1): Ceres
(S Ceres -> J Ceres Dec 24.2710 15xphi 98.4, S Ceres -> H Ceres RA 155.5900 ninth 155.556 88.9) and Makemake (S Makemake -> H Makemake
Dec 1.4144 sqrt2 90.7, H Makemake - J Makemake RA 24.2711 15xphi 98.1): two bodies, each with two high same-body lines. Read-only; winners
named below, no results file read. 17 result races, bybody xlsx.
Same-body line = S X -> H X, S X -> J X or H X - J X in a number family (no conj / cp / opposition), X not the Moon, Rahu / Ketu one body
(as BB69). A 'double' body = X with 2 or more such lines scoring >= cut (any planes).
 Dk1  at least one double body;  Dk2  two or more double bodies;  Dk2t  Dk2 with a target shared by two of the double bodies' lines
 k = the cut (80, 85, 90)"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_sbcount import RACES
CUTS = (80, 85, 90)
KEYS = [f'D{k}{s}' for k in CUTS for s in ('1', '2', '2t')]


def doubles(D, cut):
    by = {}
    for X, r in E._strong_sb(D, cut):
        by.setdefault(X, []).append(r)
    return {X: rs for X, rs in by.items() if len(rs) >= 2}


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            for k in CUTS:
                db = doubles(D, k)
                if db: held[f'D{k}1'].append(run)
                if len(db) >= 2:
                    held[f'D{k}2'].append(run)
                    tg = {}
                    for X, rs in db.items():
                        for x in rs: tg.setdefault((x['fam'], x['tgt']), set()).add(X)
                    if any(len(v) > 1 for v in tg.values()): held[f'D{k}2t'].append(run)
                    if k == 85:
                        ex.append(f"{run}: " + '; '.join(f"{X}: " + ', '.join(f"{x['line']} {x['plane']} {x['tgt']} ({x['sc']})" for x in rs)
                                                       for X, rs in db.items()))
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex: print('   ', x)
    print('\n## Totals (picks, won, by chance)')
    for k in KEYS: print(f"  {k}: {tot[k][0]} picks, {tot[k][1]} won, {tot[k][2]:.1f} by chance")


if __name__ == '__main__':
    main()
