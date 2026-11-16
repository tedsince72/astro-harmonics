"""Field check (16 Nov 2026, Eddie: 'from that Venus is there a new rule or improvement to a current rule'), from Blue Collar Glory
(Sedgefield 15:00 10 May 2022, won 20/1): H Venus – J Venus Dec 11.3263 7xphi (99.94); S Ketu -> H Venus Dec 20 (94.51) (= BB66);
S Ketu – S Fomalhaut Dec 11.3006 on the same 7xphi (20.92): the sky body on H X also carries the H X – J X number with a royal star.
Read-only; winners named below, no results file read. 18 result races (bybody xlsx; BB66 / BB69 holders from the bbrules json).
 B66   BB66 as built
 V4b   BB66 and a sky pair (S A – S B, no Moon) on the family + target of its H X – J X line
 V4    BB66 and the BB66 sky body Y in a sky pair on the H X – J X family + target
 V4r   V4 with the pair's other end a royal star
 V5    BB66 and BB69 (same runner)
 V1    H X – J X in a number family scoring >= 99 (any plane)"""
import sys, json
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_sbcount import RACES
RACES = RACES + [('20220510_sedgefield_1500', 'Blue Collar Glory')]
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
NO = ('conj', 'contraparallel', 'opposition')
KEYS = ['B66', 'V4b', 'V4', 'V4r', 'V5', 'V1']


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        J = json.load(open(f'docs/eddie_read/bybody_rules/{r}_bbrules.json'))['rules']
        b66 = [c for c in J.get('BB66', []) if not c['watch_only']]
        b69 = {c['runner'] for c in J.get('BB69', []) if not c['watch_only']}
        held = {k: set() for k in KEYS}; ex = []
        for c in b66:
            run, X = c['runner'], c['body']
            held['B66'].add(run)
            if run in b69: held['V5'].add(run)
            d = data[run][X]
            hj = [x for x in d['L'] if x['line'] == f'H {X} – J {X}' and x['plane'] == 'Dec' and x['fam'] and x['fam'] not in NO
                  and x['sc'] is not None and x['sc'] >= 90]
            ys = {cl.split(' → ')[0][2:] for cl in c['cells'] if ' → ' in cl}
            for h in hj:
                prs = [s for s in d['S'] if s.get('match') == f"{h['line']} Dec" and ' – ' in s['line'] and '→' not in s['line']
                       and 'Moon' not in s['line']]
                if prs: held['V4b'].add(run)
                for s in prs:
                    ends = [e[2:] for e in s['line'].split(' – ')]
                    if any(y in ends for y in ys):
                        held['V4'].add(run)
                        if any(e in ROY for e in ends): held['V4r'].add(run)
                        ex.append(f"{run} {X}: {h['line']} Dec {h['v']:.4f} {h['tgt']} ({h['sc']}) carried by {s['line']} {s['plane']} "
                                  f"{s['v']:.4f} ({s['sc']}); sky body(s) {sorted(ys)}")
        for run, D in data.items():
            for X, d in D.items():
                if any(x['line'] == f'H {X} – J {X}' and x['fam'] and x['fam'] not in NO and x['sc'] is not None and x['sc'] >= 99
                       for x in d['L']):
                    held['V1'].add(run)
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(sorted(held[k]))}")
        for x in ex: print('   ', x)
    print('\n## Totals (picks, won, by chance)')
    for k in KEYS: print(f"  {k}: {tot[k][0]} picks, {tot[k][1]} won, {tot[k][2]:.1f} by chance")


if __name__ == '__main__':
    main()
