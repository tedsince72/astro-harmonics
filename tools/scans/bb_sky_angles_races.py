"""Sky - sky from every angle, by race (19 Nov 2026, Eddie: 'cover all the angles and especially the families and pairs involved';
read-only, in-sample). Every result race with an _active.xlsx, split by the cover of eight (hit = winner a pick, other = miss or no
pick); the 9 rule-origin races left out (bb_sky_aspects_races.ORIG). Every sky line S X – S Y at the off (sky bodies, no Moon, + royal
stars, no royal – royal, not S Rahu – S Ketu), RA and Dec: each number family (its best target) and conj / opposition / contraparallel,
scored as eddie_bybody (linear). Tables (lines per race, hit vs other; cut >= 90 for numbers, >= 50 for conj / cp / opposition):
  1  by kind (family or aspect)
  2  by body x kind group (numbers / aspects) and by body x family
  3  body pairs (any number) and body pairs by kind: races holding them, hit share vs other share, 4+ races
  4  by plane
Usage: python3 tools/scans/bb_sky_angles_races.py"""
import sys, os, openpyxl, collections
sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as NG
import bb_cover8_where as W
from bb_cover8 import C
from bb_scan_natal_pairs import P
from bb_scan_uranus_pairs import dist
from bb_sky_sky_races import PTS
from bb_sky_aspects_races import ORIG

FAMS = ['whole', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver']
ASP = ['conj', 'opposition', 'contraparallel']


def lines(race):
    path = f'reference/classic/race_batch_{race}_active.xlsx'
    runners, tt, tp = B.load(path)
    tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
    out = []
    for i, a in enumerate(PTS):
        for b in PTS[i + 1:]:
            if {a, b} == {'Rahu', 'Ketu'} or (a in B.ROYAL and b in B.ROYAL):
                continue
            for pl in ('RA', 'Dec'):
                x, y = P(tp, tr, a, pl), P(tp, tr, b, pl)
                if x is None or y is None:
                    continue
                for f, t, s in B.hits(dist(x, y, pl), pl):
                    out.append((a, b, pl, f, t, s))
                if pl == 'Dec':
                    c = B.contraparallel(x, y)
                    if c:
                        out.append((a, b, pl, 'contraparallel', 'cp', c[2]))
    return out


def keep(x):
    return x[5] >= (90 if x[3] in FAMS else 50)


def main():
    G = {'hit': [], 'other': []}
    for race, win in NG.RACES:
        if race in ORIG or not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
            continue
        runners, hh = W.holders(race)
        w = next(r for r in runners if win in r)
        g = 'hit' if any(set(c) <= hh.get(w, set()) for c in C) else 'other'
        G[g].append([x for x in lines(race) if keep(x)])
    nh, no = len(G['hit']), len(G['other'])
    per = lambda g, f: sum(sum(1 for x in R if f(x)) for R in G[g]) / len(G[g])
    print(f'# Sky - sky from every angle: hit {nh} races, other {no} (rule-origin races left out); numbers >= 90, aspects >= 50\n')
    print('## 1. By kind\n\n| kind | hit | other | other / hit |\n|---|---|---|---|')
    for k in FAMS + ASP:
        h, o = per('hit', lambda x: x[3] == k), per('other', lambda x: x[3] == k)
        print(f'| {k} | {h:.2f} | {o:.2f} | {o / h if h else 0:.2f} |')
    print('\n## 2. By body\n\n| body | numbers hit | numbers other | aspects hit | aspects other | ' +
          ' | '.join(f'{f} h / o' for f in FAMS) + ' |\n|' + '---|' * (5 + len(FAMS)))
    for b in PTS:
        cells = [per('hit', lambda x: b in x[:2] and x[3] in FAMS), per('other', lambda x: b in x[:2] and x[3] in FAMS),
                 per('hit', lambda x: b in x[:2] and x[3] in ASP), per('other', lambda x: b in x[:2] and x[3] in ASP)]
        fam = [f"{per('hit', lambda x, f=f: b in x[:2] and x[3] == f):.2f} / {per('other', lambda x, f=f: b in x[:2] and x[3] == f):.2f}"
               for f in FAMS]
        print(f'| {b} | ' + ' | '.join(f'{c:.2f}' for c in cells) + ' | ' + ' | '.join(fam) + ' |')
    print('\n## 3. Body pairs (held in 4+ races): races holding the pair, hit share vs other share\n')
    for lab, grp in (('any kind', lambda x: 'any'), ('numbers vs aspects', lambda x: 'numbers' if x[3] in FAMS else 'aspect'),
                     ('by kind', lambda x: x[3])):
        hold = {g: collections.Counter() for g in G}
        for g, L in G.items():
            for R in L:
                for k in {(tuple(sorted(x[:2])), grp(x)) for x in R}:
                    hold[g][k] += 1
        sc = []
        for k in set(hold['hit']) | set(hold['other']):
            h, o = hold['hit'][k], hold['other'][k]
            if h + o >= 4:
                sc.append((h / nh - o / no, k, h, o))
        sc.sort(reverse=True)
        print(f'### {lab} ({len(sc)} pairs held in 4+ races)\n\n| pair | kind | hit races | other races | hit share | other share |\n|---|---|---|---|---|---|')
        for d, k, h, o in sc[:10]:
            print(f'| {k[0][0]} – {k[0][1]} | {k[1]} | {h} | {o} | {h / nh:.2f} | {o / no:.2f} |')
        print('| ... | | | | | |')
        for d, k, h, o in sc[-10:]:
            print(f'| {k[0][0]} – {k[0][1]} | {k[1]} | {h} | {o} | {h / nh:.2f} | {o / no:.2f} |')
        print()
    print('## 4. By plane\n\n| plane | numbers hit | numbers other | aspects hit | aspects other |\n|---|---|---|---|---|')
    for pl in ('RA', 'Dec'):
        print(f"| {pl} | {per('hit', lambda x: x[2] == pl and x[3] in FAMS):.2f} | {per('other', lambda x: x[2] == pl and x[3] in FAMS):.2f} | "
              f"{per('hit', lambda x: x[2] == pl and x[3] in ASP):.2f} | {per('other', lambda x: x[2] == pl and x[3] in ASP):.2f} |")
    print('\nIn-sample, small numbers per body (under one line per race); with 28 bodies x 9 kinds and hundreds of pairs, some differences'
          ' this size come by chance.')


if __name__ == '__main__':
    main()
