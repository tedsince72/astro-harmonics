"""Scan (18 Nov 2026, Eddie: 'that may help us understand some of the rules more clearly if they involved activated and non activated
pairs in different races'; read-only). Each BB rule pick (runner holding the rule) is split by its sky-on-natal cells S Y -> H / J X
(Y not X) in the rule's cells: 'activated' = the race's sky pair S Y - S X scores (conj or number family, any plane, any score; pairs
from every runner's bybody rows), 'all activated' / 'none activated' / 'mixed' / 'no S Y -> X cell'. Per rule and pooled:
picks / won / by chance (1 / field size). 45 result races (bb_scan_negatives.RACES). Rules mostly built on some of these races (in-sample).
  python3 tools/scans/bb_scan_rules_activation.py"""
import sys, json, re
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NEG
from bb_scan_negative_activated import skypairs

CELL = re.compile(r'^S (\S+(?: \S+)*?) → [HJ] (\S+(?: \S+)*?) (RA|Dec) ')


def main():
    g = {}  # (rule, cls) -> [picks, won, chance]
    for race, win in NEG.RACES:
        R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        sp = set()
        for D in R.values():
            sp |= skypairs(D)
        N = len(R)
        rules = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))['rules']
        for rule, hs in rules.items():
            byrun = {}
            for h in hs:
                if h.get('watch_only'):
                    continue
                st = byrun.setdefault(h['runner'], set())
                for c in h.get('cells', []):
                    m = CELL.match(c)
                    if m and m.group(1) != m.group(2):
                        st.add(frozenset((m.group(1), m.group(2))) in sp)
            for run, st in byrun.items():
                cls = 'no S Y → X cell' if not st else 'all activated' if st == {True} else 'none activated' if st == {False} else 'mixed'
                for key in ((rule, cls), ('ALL', cls)):
                    t = g.setdefault(key, [0, 0, 0.0]); t[0] += 1; t[1] += win in run; t[2] += 1 / N
    order = ['all activated', 'mixed', 'none activated', 'no S Y → X cell']
    def show(rule):
        parts = []
        for c in order:
            if (rule, c) in g:
                p, w, ch = g[(rule, c)]; parts.append(f'{c} {p} / {w} / {ch:.1f}')
        return '; '.join(parts)
    print(f'# Rule picks by sky activation of their S Y → natal X cells ({len(NEG.RACES)} result races; picks / won / by chance)\n')
    print('ALL rules pooled: ' + show('ALL') + '\n')
    rs = sorted({k[0] for k in g if k[0] != 'ALL'}, key=lambda r: (re.sub(r'\D', '', r).zfill(3), r))
    for r in rs:
        tot = sum(g[(r, c)][0] for c in order if (r, c) in g)
        if tot >= 5:
            print(f'- {r}: {show(r)}')


if __name__ == '__main__':
    main()
