"""Field check (16 Nov 2026, Eddie's Blue Collar Glory Venus lines; Sedgefield 15:00 10 May 2022, won 20/1): H Venus – J Venus Dec
11.3263 7xphi (99.9); S Ketu -> H Venus Dec 20.0011 (94.5); S Ketu -> J Venus RA 111.0947 ninth 111.111 (92.6); S Ketu – S Fomalhaut Dec
11.3006 7xphi (20.9). One sky body on both natal X, and in a sky pair on the H X – J X number. Read-only; winners named below, no results
file read. 18 result races, bybody xlsx.
 K1   H X – J X in a number family >= 90 (any plane); a sky body Y (not X, not the Moon, not a royal star) with S Y -> H X and S Y -> J X both
      in a number family >= 90 (any planes)
 K1d  K1 with H X – J X in Dec
 K2   K1 and Y in a sky pair (S Y – S Z, no Moon) on the H X – J X family + target (any score)
 K2r  K2 with Z a royal star
 K0   (looser) as K1 with the two Y lines >= 80"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_hj_carry import RACES
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
NO = ('conj', 'contraparallel', 'opposition')
KEYS = ['K0', 'K1', 'K1d', 'K2', 'K2r']
num = lambda r, c: r['fam'] and r['fam'] not in NO and r['sc'] is not None and r['sc'] >= c


def cases(X, d):
    out = []
    for h in [x for x in d['L'] if x['line'] == f'H {X} – J {X}' and num(x, 90)]:
        for cut in (80, 90):
            ys = {}
            for o in d['O']:
                if ' → ' not in o['line'] or not num(o, cut): continue
                y, tgt = o['line'].split(' → ')
                y = y[2:]
                if y in (X, 'Moon') or y in ROY or tgt not in (f'H {X}', f'J {X}'): continue
                ys.setdefault(y, {}).setdefault(tgt[0], o)
            for y, v in ys.items():
                if len(v) < 2: continue
                tg = {'K0'} if cut == 80 else {'K1'}
                if cut == 90:
                    if h['plane'] == 'Dec': tg.add('K1d')
                    prs = [s for s in d['S'] if s.get('match') == f"{h['line']} {h['plane']}" and ' – ' in s['line'] and '→' not in s['line']
                           and 'Moon' not in s['line'] and y in [e[2:] for e in s['line'].split(' – ')]]
                    if prs:
                        tg.add('K2')
                        if any(any(e[2:] in ROY for e in s['line'].split(' – ')) for s in prs): tg.add('K2r')
                out.append((tg, f"{h['line']} {h['plane']} {h['v']:.4f} {h['tgt']} ({h['sc']}); S {y} → H {X} {v['H']['plane']} "
                                f"{v['H']['v']:.4f} {v['H']['tgt']} ({v['H']['sc']}), S {y} → J {X} {v['J']['plane']} {v['J']['v']:.4f} "
                                f"{v['J']['tgt']} ({v['J']['sc']})"))
    return out


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: set() for k in KEYS}; ex = []
        for run, D in data.items():
            for X, d in D.items():
                for tg, txt in cases(X, d):
                    for k in tg: held[k].add(run)
                    if 'K1' in tg: ex.append(f"{run} {X} [{' '.join(sorted(tg))}] {txt}")
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(sorted(held[k]))}")
        for x in ex: print('   ', x)
    print('\n## Totals (picks, won, by chance)')
    for k in KEYS: print(f"  {k}: {tot[k][0]} picks, {tot[k][1]} won, {tot[k][2]:.1f} by chance")


if __name__ == '__main__':
    main()
