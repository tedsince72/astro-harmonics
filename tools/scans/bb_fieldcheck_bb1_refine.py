"""Field check (16 Nov 2026, Eddie: 'Mars (BB1) is there something in common with pholas here that can refine the rule now there are
2 winners'). Read-only; winners named below, no results file read. 14 result races + Chelmsford AW 13:20 2024 (no result, rarity only).
BB1 cases (eddie_bybody_rules.bb1) with: R = the royal line, P = the carrier pair S A - S B, ends = S A / S B - S X and S A / S B -> c X.
 F1  R and P in a number family (conj / contraparallel / opposition never)
 F2  F1 and both natal end lines (S A -> c X, S B -> c X) in a number family scoring >= 50
 F3  F2 and R and P golden (Pholas 10xphi, The Dunkirk Lads 89xphi)
 F4  F2 and every end line (sky and natal) scoring >= 50, conj allowed on a sky leg"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_triangle import RACES
NO = ('conj', 'contraparallel', 'opposition')
KEYS = ['BB1', 'F1', 'F2', 'F3', 'F4']
num = lambda r: r['fam'] and r['fam'] not in NO and r['sc'] is not None


def cases(X, d, D):
    b = E.Body(X, d); b.all = D
    out = []
    for c in b.bb1_cases() if hasattr(b, 'bb1_cases') else E.bb1(b):
        R, P, ends = c['cells'][0], c['cells'][1], c['cells'][2:]
        A, B = P['line'].split(' – ')
        ch = R['line'][0]
        nat = [e for e in ends if ' → ' in e['line']]
        t = {'BB1'}
        if num(R) and num(P):
            t.add('F1')
            if nat and all(num(e) and e['sc'] >= 50 for e in nat):
                t.add('F2')
                if R['fam'] == P['fam'] == 'golden': t.add('F3')
                if all(e['sc'] >= 50 and e['fam'] not in ('contraparallel', 'opposition') for e in ends): t.add('F4')
        out.append((t, f"{R['line']} {R['plane']} {R['v']:.4f} {R['tgt']} ({R['sc']}) by {P['line']} {P['plane']} {P['tgt']} ({P['sc']}); "
                        + '; '.join(f"{e['line']} {e['plane']} {e['v']:.4f} {e['tgt']} ({e['sc']})" for e in ends)))
    return out


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES + [('20240118_chelmsford_aw_1320', None)]:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            tg = set()
            for X, d in D.items():
                for t, s in cases(X, d, D):
                    tg |= t; ex.append(f"{run} {X} [{','.join(k for k in KEYS if k in t)}]: {s}")
            for k in tg: held[k].append(run)
        if win:
            for k in KEYS:
                hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win or 'no result'})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex: print('    ', x)
    print('\n## Totals over the 14 result races (picks / won / by chance; Pholas and The Dunkirk Lads are in-sample)')
    for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
