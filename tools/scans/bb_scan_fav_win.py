"""Why does a favourite win? (19 Nov 2026, Eddie after Wolverhampton AW 20:10 25 Aug 2021, Cuban Cigar the second favourite in a row to win
outside the cover: 'what gives the fav the opportunity to win, and why does the fav accept that opportunity and win'; read-only,
chosen after the results). Every result race with a known favourite (bb_favs_outer_uranus.FAV): winning favourites against losing
favourites.
 (A) the favourite itself ('accepts'): rules held / alone / rank in field, depth, cover pick, nets (sky-on-natal >= 90, >= 80, whole >= 80;
     pair tally >= 80), field-only negatives; nets use labels from the other races (leave one race out).
 (B) the field around it ('opportunity'): field size, sky race score v1, cover picks among the others, best rival rule count, rivals at
     depth 5, rivals with a positive net, whether the favourite is top / bottom of its field on each measure.
 (C) rules: each rule held by favourites - held / won; and rules held by winning favourites.
Usage: python3 tools/scans/bb_scan_fav_win.py"""
import sys, os, json
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans']
import bb_scan_negatives as NG, bb_favs_outer_uranus as F, bb_sky_race_score as S
import bb_pair_tally as PT, bb_scan_sky_on_natal as SN

C8 = [('BB32',), ('BB3', 'BB12', 'BB53'), ('BB79',), ('BB77c',), ('BB54', 'BB82'), ('BB1b',), ('BB69',), ('BB13', 'BB80')]
races = [(r, w) for r, w in NG.RACES if os.path.exists(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx')]
print('loading ...', file=sys.stderr)
SNd = []; PTd = []
for race, win in races:
    sn = SN.load(race); pt = PT.load(race)
    fav = next((r for r in sn if race in F.FAV and F.FAV[race] in r), None)
    SNd.append((race, win, fav, sn)); PTd.append((race, win, pt))
PW = [next(r for r in R if win in r) for race, win, R in PTd]

rows = []
for i, (race, win) in enumerate(races):
    fav = SNd[i][2]
    if not fav:
        continue
    runners, held = NG.holders(race)
    runners = list(SNd[i][3])
    cnt = {r: len(held.get(r, ())) for r in runners}
    from collections import Counter
    rc = Counter(x for r in runners for x in held.get(r, ()))
    alone = {r: sum(rc[x] == 1 for x in held.get(r, ())) for r in runners}
    cover = {r: any(set(c) <= held.get(r, set()) for c in C8) for r in runners}
    dp = {}
    if os.path.exists(f'docs/eddie_read/depth/{race}_depth.json'):
        dp = {d['runner']: d['top'] for d in json.load(open(f'docs/eddie_read/depth/{race}_depth.json'))['runners']}
    nets = {}
    for v in SN.VERS:
        st = SN.tally(SNd, v, skip=race)
        nets[v] = {r: sum((SN.label(st[k][1], st[k][2]) == 'positive') - (SN.label(st[k][1], st[k][2]) == 'negative')
                          for k in P[v] if k in st) for r, P in SNd[i][3].items()}
    st = PT.tally(PTd, PW, skip=race); R = PTd[i][2]
    lab = lambda k: PT.label(*st[k]) if k in st else ''
    pnet = {r: sum((lab(k) == 'positive') - (lab(k) == 'negative') for k in ps) for r, ps in R.items()}
    negs = {r: {k for k in ps if lab(k) == 'negative'} for r, ps in R.items()}
    fon = {r: len([k for k in negs[r] if not any(k in negs[o] for o in R if o != r)]) for r in R}
    won = win in fav
    m = dict(rules=cnt, alone=alone, depth=dp, net90=nets[('any', 90)], net80=nets[('any', 80)], whole80=nets[('whole', 80)],
             pair=pnet, fon=fon)
    pos = {}
    for k, d in m.items():
        if fav not in d:
            continue
        vals = list(d.values()); pos[k] = ('top' if d[fav] == max(vals) else '') + ('bottom' if d[fav] == min(vals) else '')
    others = [r for r in runners if r != fav]
    rows.append(dict(race=race, fav=fav, won=won, n=len(runners), v1=S.score(race)[0], cover=cover[fav],
                     cov_oth=sum(cover[r] for r in others), best_rival=max(cnt[r] for r in others),
                     d5_oth=sum(dp.get(r) == 5 for r in others), pos_oth=sum(nets[('any', 90)][r] > 0 for r in others),
                     held=held.get(fav, set()), pos=pos, **{k: d.get(fav) for k, d in m.items()}))

W = [r for r in rows if r['won']]; L = [r for r in rows if not r['won']]
avg = lambda xs, k: sum(x[k] for x in xs if x[k] is not None) / max(1, sum(x[k] is not None for x in xs))
print(f'# Winning favourites vs losing favourites: {len(rows)} races with a favourite, favourite won {len(W)}\n')
print('Note: races were chosen by the winner (mostly outsiders before 19 Nov), so favourites win far less here than on the track.\n')
print('## A. The favourite itself (averages; winners | losers)\n')
print('| measure | winning favs | losing favs |\n|---|---|---|')
for k in ('rules', 'alone', 'depth', 'net90', 'net80', 'whole80', 'pair', 'fon'):
    print(f'| {k} | {avg(W, k):.2f} | {avg(L, k):.2f} |')
print(f"| cover pick | {sum(r['cover'] for r in W)} of {len(W)} | {sum(r['cover'] for r in L)} of {len(L)} |")
print('\n### Favourite top / bottom of its field (winners | losers)\n')
print('| measure | top: W | top: L | bottom: W | bottom: L |\n|---|---|---|---|---|')
for k in ('rules', 'alone', 'depth', 'net90', 'net80', 'whole80', 'pair', 'fon'):
    f = lambda xs, t: sum(t in x['pos'].get(k, '') for x in xs)
    print(f"| {k} | {f(W, 'top')} | {f(L, 'top')} | {f(W, 'bottom')} | {f(L, 'bottom')} |")
print('\n## B. The field around the favourite (averages; winners | losers)\n')
print('| measure | fav won | fav lost |\n|---|---|---|')
for k in ('n', 'v1', 'cov_oth', 'best_rival', 'd5_oth', 'pos_oth'):
    print(f'| {k} | {avg(W, k):.2f} | {avg(L, k):.2f} |')
print('\n## Winning favourites one by one\n')
print('| race | favourite | rules (alone) | depth | net 90 / 80 / whole | pair | field-only neg | cover | v1 | rivals: cover / best rules / depth 5 |\n|---|---|---|---|---|---|---|---|---|---|')
for r in W:
    print(f"| {r['race']} | {r['fav']} | {r['rules']} ({r['alone']}) | {r['depth']} | {r['net90']:+d} / {r['net80']:+d} / {r['whole80']:+d} | "
          f"{r['pair']:+d} | {r['fon']} | {'yes' if r['cover'] else 'no'} | {r['v1']:+d} | {r['cov_oth']} / {r['best_rival']} / {r['d5_oth']} |")
print('\n## C. Rules held by favourites: held / won (rules held by at least 2 winning favourites)\n')
from collections import Counter
hw = Counter(x for r in W for x in r['held']); hl = Counter(x for r in L for x in r['held'])
for x, w in sorted(hw.items(), key=lambda t: (-t[1], t[0])):
    if w >= 2:
        print(f'- {x}: winning favs {w} of {len(W)}, losing favs {hl[x]} of {len(L)}')
