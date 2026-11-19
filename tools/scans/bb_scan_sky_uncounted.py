"""Read-only scan (19 Nov 2026, Eddie after Newmarket 14:13 29 Oct 2022: 'there must have been something less positive or more
negative in the sky than we counted'; chosen after the result). For a race: every sky line S X - S Y at the off (bb_sky_angles_races.lines;
numbers >= 90, conj / cp / opposition >= 50) NOT counted by the sky race score v1; for each, its body x kind and its body pair, over every
result race (origin races left out): races holding it where the cover hit / missed. Usage: python3 tools/scans/bb_scan_sky_uncounted.py <race>"""
import sys, os, collections
race = sys.argv[1]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_sky_angles_races as A, bb_sky_race_score as S, bb_scan_negatives as NG, bb_cover8_where as W
from bb_cover8 import C
ASPK = ('conj', 'contraparallel', 'opposition')
def ok(x): return x[5] >= (50 if x[3] in ASPK else 90)
def counted(x):
    f, s, e = x[3], x[5], set(x[:2])
    return (f in ('golden', 'phi power', 'ninth') and s >= 90 and e & S.OUT) or (f == 'whole' and s >= 90 and e & S.WH) or \
        (f == 'golden' and s >= 90 and 'Saturn' in e) or (f in ASPK and s >= 50 and e & S.ASP)
feat = collections.defaultdict(lambda: [0, 0]); pair = collections.defaultdict(lambda: [0, 0]); nh = nm = 0
for r, win in NG.RACES:
    if r in A.ORIG or r == race or not os.path.exists(f'reference/classic/race_batch_{r}_active.xlsx'): continue
    runners, hh = W.holders(r); w = next((x for x in runners if win in x), None)
    if w is None: continue
    hit = any(set(c) <= hh.get(w, set()) for c in C); nh += hit; nm += not hit
    L = [x for x in A.lines(r) if ok(x)]
    fs = {(b, x[3]) for x in L for b in x[:2]}; ps = {(frozenset(x[:2]), x[3]) for x in L}
    for k in fs: feat[k][0 if hit else 1] += 1
    for k in ps: pair[k][0 if hit else 1] += 1
print(f'other races: cover hit {nh}, missed {nm} (miss share {nm/(nh+nm):.2f})\n')
print('| sky line (not counted by the score) | body x kind: races hit / missed | body pair + kind: hit / missed |\n|---|---|---|')
for x in sorted([x for x in A.lines(race) if ok(x) and not counted(x)], key=lambda x: -x[5]):
    fb = ' ; '.join(f'{b} {x[3]} {feat[(b, x[3])][0]} / {feat[(b, x[3])][1]}' for b in x[:2])
    p = pair[(frozenset(x[:2]), x[3])]
    print(f'| S {x[0]} – S {x[1]} {x[2]} {x[4]} {x[3]} ({x[5]:.1f}) | {fb} | {p[0]} / {p[1]} |')
