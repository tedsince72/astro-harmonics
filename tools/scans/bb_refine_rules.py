"""Field check (16 Nov 2026, Eddie: 'on any of the rules it hits could they be improved with other winners as well'), Little Girl Blue's rules
BB3, BB4, BB12, BB53, BB63 (and the combination BB3 + BB63). Read-only; winners named below, no results file read. 16 result races, from the
bbrules json (each case's cells as built). Generic tightenings of a case (as BB1b did for BB1):
 G1  every cell in a number family (no conj / contraparallel / opposition, no 'no family')
 G2  G1 and every sky -> natal cell (' → ') >= 50
 G3  G1 and every cell >= 50
 G4  G2 and the royal line (first cell) >= 50
A runner holds a version when one of its cases passes. Combination BB3 + BB63 tested with each version on both rules."""
import sys, json, re
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_hub import RACES
RULES = ['BB3', 'BB4', 'BB12', 'BB53', 'BB63']
NO = ('conj', 'contraparallel', 'opposition')
VERS = ['as built', 'G1', 'G2', 'G3', 'G4']
pat = re.compile(r'^(.*?) (RA|Dec)(?: contraparallel)? (-?[\d.]+) (.*)$')


def parse(c):
    m = pat.match(c)
    if not m: return None
    line, plane, v, rest = m.groups()
    if rest.startswith('(no family)'): return dict(line=line, fam=None, sc=None)
    sc = float(rest.rsplit('(', 1)[1].rstrip(')'))
    fam = rest.rsplit('(', 1)[0].split()[-1]
    return dict(line=line, fam=fam, sc=sc)


def passes(cells, v):
    cs = [parse(c) for c in cells]; cs = [c for c in cs if c]
    if v == 'as built': return True
    if any(c['fam'] is None or c['fam'] in NO for c in cs): return False
    if v == 'G1': return True
    nat = [c for c in cs if ' → ' in c['line']]
    if v in ('G2', 'G4') and any(c['sc'] < 50 for c in nat): return False
    if v == 'G3' and any(c['sc'] < 50 for c in cs): return False
    if v == 'G4' and cs[0]['sc'] < 50: return False
    return True


def main():
    tot = {(r, v): [0, 0, 0.0, []] for r in RULES + ['BB3+BB63'] for v in VERS}
    for race, win in RACES:
        J = json.load(open(f'docs/eddie_read/bybody_rules/{race}_bbrules.json'))
        N = len(E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'))
        hold = {}
        for r in RULES:
            for c in J['rules'][r]:
                if c['watch_only']: continue
                for v in VERS:
                    if passes(c['cells'], v): hold.setdefault((r, v), set()).add(c['runner'])
        for v in VERS:
            hold[('BB3+BB63', v)] = hold.get(('BB3', v), set()) & hold.get(('BB63', v), set())
        for k, t in tot.items():
            hh = hold.get(k, set()); t[0] += len(hh); t[1] += any(win in x for x in hh); t[2] += len(hh) / N
            t[3] += [x for x in hh if win in x]
    print('rule      version   picks  won  by chance  winners')
    for (r, v), (p, w, c, ws) in tot.items():
        print(f'{r:9} {v:9} {p:5} {w:4} {c:9.1f}   {", ".join(ws)}')


if __name__ == '__main__':
    main()
