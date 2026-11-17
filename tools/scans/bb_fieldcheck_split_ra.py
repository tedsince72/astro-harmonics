"""Field check (17 Nov 2026, Eddie: 'yes, to both' - BB68b and the RA version of the split), from Doncaster 14:40 18 Mar 2022
Olympe De Gouges Ketu (won 25/1): S Ketu -> J Ketu Dec 28.942585 (no family) = S Jupiter - S Ketu 12.941448 8xphi (91.28)
+ S Jupiter -> J Ketu 16.001137 16 (94.32). Read-only; winners named below, no results file read. Uses splits() of
bb_fieldcheck_split.py (a sky body Y, not X, not the Moon, between S X and c X in one plane; both pieces in a family, conj / cp never).
 RA      any RA split, any scores           RA3   RA, one piece >= 90, the other >= 50 (BB68 in RA)
 RA90    RA, both pieces >= 90              DEC90 Dec, both pieces >= 90 (= BB68b)
 ANY90   either plane, both pieces >= 90    BOTH  the same body split in RA and in Dec (V3 level each)
Royal stars as Y left out (VS in bb_fieldcheck_split)."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
from bb_fieldcheck_split import splits, txt
from bb_fieldcheck_riverbray import RACES as R0
RACES = list(R0) + [('20220318_wolverhampton_aw_2030', 'Busby'), ('20220318_doncaster_1440', 'Olympe De Gouges')]
KEYS = ['RA', 'RA3', 'RA90', 'DEC90', 'ANY90', 'BOTH']


def tags(ss):
    t = set(); v3 = {}
    for s in ss:
        lo, hi = sorted((s['a']['sc'], s['b']['sc']))
        if s['p'] == 'RA': t.add('RA')
        if hi >= 90 and lo >= 50:
            v3.setdefault((s['c'], s['X']), set()).add(s['p'])
            if s['p'] == 'RA': t.add('RA3')
        if lo >= 90:
            t.add('ANY90'); t.add('RA90' if s['p'] == 'RA' else 'DEC90')
    if any(len(p) == 2 for p in v3.values()): t.add('BOTH')
    return t


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            bodies = set(D) | {'Rahu', 'Ketu'}; ss = []
            for X, d in D.items():
                ss += [s for s in splits(X, d) if s['Y'] in bodies]
            tg = tags(ss)
            for s in ss:
                if min(s['a']['sc'], s['b']['sc']) >= 90 or (s['p'] == 'RA' and max(s['a']['sc'], s['b']['sc']) >= 90
                                                             and min(s['a']['sc'], s['b']['sc']) >= 50):
                    ex.append(f'{run} {txt(s)}')
            for k in tg: held[k].append(run)
        for k in KEYS:
            hh = held[k]; w = [x for x in hh if win in x]
            tot[k][0] += len(hh); tot[k][1] += len(w); tot[k][2] += len(hh) / N; tot[k][3] += w
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex: print('    ', x)
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k, (p, w, c, ws) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance  {ws}')


if __name__ == '__main__':
    main()
