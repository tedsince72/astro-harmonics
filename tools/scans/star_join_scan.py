#!/usr/bin/env python3
"""star_join_scan.py  — read-only star scan (design agreed with Eddie 12 Oct 2026). Not part of the frozen reader or layers.

Stars are read from the runner workbooks (rows '<Star>_B' in TRANS = sky, P01 = horse, P02 = jockey; column B name, E RA, I Dec); each chart's
bodies are measured against that chart's own star positions. A body is ON a star when RA < 1.5 AND Dec < 0.3; NEAR when RA < 2 AND Dec < 0.6
(and not on). Only stars that JOIN charts count:
  (a) a sky body and a natal body (horse or jockey) on the same star — left out when both are the same slow body (Uranus outward: age effect);
  (b) a horse body and a jockey body on the same star;
  (c) a star on either end of a checklist link — the cross link of a strict item 1–7 or 14 in the frozen reader's output (CR v1.1).
A natal body on a star alone is not counted. A join is 'close' when every contact in it is on the star, 'near' when all are within the near
band and at least one is only near. For each join: how many runners in the race hold the same join (same star, same bodies, same charts); joins
held by fewer than half the field are marked RARE. Winners vs beaten per kind, chance = sum of 1/field size over the runners with it.
Read races are NOT evidence; Kempton 14:40, Fontwell 16:45, Goodwood 18:53 (blind for the reader) are shown separately."""
import sys, os, glob, re, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import openpyxl
import checklist_reader as CR
from layer1_inventory import rd, dd, BOD

ON_RA, ON_DEC, NEAR_RA, NEAR_DEC = 1.5, 0.3, 2.0, 0.6
SLOWISH = {'Uranus', 'Neptune', 'Pluto', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto'}
LINK_ITEMS = (1, 2, 3, 4, 5, 6, 7, 14)
READ = {'ascot_1350_20231021': 'P01', 'carlisle_1630_20220707': 'P07', 'catterick_1505_20211119': 'P07', 'chelmsford_aw_1320_20240118': 'P03',
        'ffos_las_1420_20220105': 'P05', 'fontwell_1530_20231006': 'P05', 'haydock_1405_20220219': 'P09', 'haydock_1718_20220507': 'P07',
        'huntingdon_1352_20211205': 'P05', 'lingfield_1500_20220123': 'P11', 'newbury_1350_20211126': 'P09', 'newcastle_1540_20220311': 'P05',
        'newcastle_aw_1220_20211112': 'P03', 'newcastle_aw_1330_20220102': 'P09', 'newcastle_aw_1540_20211112': 'P05', 'newcastle_aw_1640_20220215': 'P01',
        'newmarket_1535_20220414': 'P07', 'newton_abbot_1525_20220717': 'P07', 'nottingham_1530_20220601': 'P01', 'nottingham_1750_20220613': 'P03',
        'perth_1610_20220420': 'P09', 'sandown_1425_20211204': 'P05', 'sandown_1430_20240215': 'P13', 'sedgefield_1500_20220510': 'P01',
        'wincanton_1420_20220321': 'P07', 'wolverhampton_aw_1725_20231021': 'P05', 'york_1545_20240515': 'P11', 'york_1615_20240515': 'P25',
        'newmarket_july_1745_20240816': 'P01', 'exeter_1515_20211019': 'P11', 'redcar_1515_20211015': 'P05', 'haydock_1420_20210904': 'P03'}
BLIND = {'kempton_aw_1440_20210904': 'P05', 'fontwell_1645_20210914': 'P05', 'goodwood_1853_20210827': 'P09'}

def load(path):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    out = {}
    for c, sh in (('S', 'TRANS'), ('H', 'P01'), ('J', 'P02')):
        bodies, stars = {}, {}
        for r in list(wb[sh].iter_rows(values_only=True))[1:]:
            if not isinstance(r[4], (int, float)) or not isinstance(r[8], (int, float)): continue
            if r[1] in BOD: bodies[r[1]] = (float(r[4]), float(r[8]))
            elif isinstance(r[1], str) and r[1].endswith('_B'): stars[r[1][:-2]] = (float(r[4]), float(r[8]))
        out[c] = (bodies, stars)
    return out

def contacts(C):
    """(chart, body) -> {star: 'on' | 'near'} against that chart's own star positions"""
    ct = {}
    for c, (bodies, stars) in C.items():
        for b, p in bodies.items():
            for s, q in stars.items():
                r_, d_ = rd(p, q), dd(p, q)
                lv = 'on' if r_ < ON_RA and d_ < ON_DEC else 'near' if r_ < NEAR_RA and d_ < NEAR_DEC else None
                if lv: ct.setdefault((c, b), {})[s] = (lv, round(r_, 4), round(d_, 4))
    return ct

def joins(C, inst):
    ct = contacts(C); out = []
    def lv(*xs): return 'close' if all(x[0] == 'on' for x in xs) else 'near'
    by_star = {}
    for (c, b), d in ct.items():
        for s, v in d.items(): by_star.setdefault(s, []).append((c, b, v))
    for s, xs in sorted(by_star.items()):
        sky = [x for x in xs if x[0] == 'S']; H = [x for x in xs if x[0] == 'H']; J = [x for x in xs if x[0] == 'J']
        for a in sky:
            for n in H + J:
                if a[1] == n[1] and a[1] in SLOWISH: continue
                out.append(('a', f"{s}: sky {a[1]} + {n[0]} {n[1]}", lv(a[2], n[2]), f"sky {a[1]} RA {a[2][1]} Dec {a[2][2]} | {n[0]} {n[1]} RA {n[2][1]} Dec {n[2][2]}"))
        for h in H:
            for j in J:
                out.append(('b', f"{s}: H {h[1]} + J {j[1]}", lv(h[2], j[2]), f"H {h[1]} RA {h[2][1]} Dec {h[2][2]} | J {j[1]} RA {j[2][1]} Dec {j[2][2]}"))
    seen = set()
    for x in inst:
        if x['item'] not in LINK_ITEMS or x['level'] != 'strict': continue
        for h, j in re.findall(r'H (\w+) – J (\w+) ', x['what']):
            for end in (('H', h), ('J', j)):
                for s, v in sorted(ct.get(end, {}).items()):
                    key = ('c', f"{s}: {end[0]} {end[1]} on link H {h} – J {j}", 'close' if v[0] == 'on' else 'near', f"{end[0]} {end[1]} RA {v[1]} Dec {v[2]} (item {x['item']})")
                    if key[:3] not in seen: seen.add(key[:3]); out.append(key)
    return out

def race(r):
    F = CR.run(r); res = {}
    for P in F['runners']:
        C = load(glob.glob(f'reference/classic/{r}/*__{P}.xlsx')[0])
        res[P] = joins(C, F['per_runner'][P]['instances'])
    held = {}
    for P, js in res.items():
        for k, key, lv, _ in js: held.setdefault((k, key, lv), set()).add(P)
    return F, res, held

def summary(races, label, out):
    T = {}
    for r, W in races.items():
        F, res, held = race(r); n = F['n']
        for P, js in res.items():
            for k in 'abc':
                for lv in ('close', 'near'):
                    mine = [j for j in js if j[0] == k and j[2] == lv]
                    for tag, sel in (('any', mine), ('rare', [j for j in mine if len(held[(j[0], j[1], j[2])]) * 2 < n])):
                        d = T.setdefault((k, lv, tag), [0, 0, 0, 0, 0.0])   # winners with, winners, beaten with, beaten, chance
                        if P == W: d[1] += 1; d[0] += bool(sel)
                        else: d[3] += 1; d[2] += bool(sel)
                        if sel: d[4] += 1 / n
    out.append(f"-- {label}")
    out.append(f"   {'kind':6s} {'band':6s} {'joins':5s} {'winners with':>14s} {'beaten with':>14s}   wins (chance)")
    names = {'a': 'a sky+natal', 'b': 'b H+J', 'c': 'c on link'}
    for k in 'abc':
        for lv in ('close', 'near'):
            for tag in ('any', 'rare'):
                d = T.get((k, lv, tag), [0, 0, 0, 0, 0.0])
                out.append(f"   {names[k]:12s} {lv:6s} {tag:5s} {d[0]:4d}/{d[1]:<4d} {100 * d[0] / max(d[1], 1):3.0f}%  {d[2]:4d}/{d[3]:<4d} {100 * d[2] / max(d[3], 1):3.0f}%   {d[0]} ({d[4]:.2f})")

def detail(r, W, out):
    F, res, held = race(r); n = F['n']
    out.append(f"== {r}  (field {n}; winner {W} {F['runners'][W]})")
    for P, js in res.items():
        out.append(f"   {P} {F['runners'][P]}{'   <- WINNER' if P == W else ''}")
        for k, key, lv, txt in sorted(js):
            h = len(held[(k, key, lv)])
            out.append(f"      ({k}) {lv:5s} {key:46s} held by {h} of {n}{'  RARE' if h * 2 < n else ''}   {txt}")

if __name__ == '__main__':
    out = ['Star joins (read-only scan; ON = RA < 1.5 AND Dec < 0.3, NEAR = RA < 2 AND Dec < 0.6). RARE = held by fewer than half the field.',
           'Chance = expected winners if every runner had 1/field-size; a runner counts once per row however many joins it has.']
    summary(BLIND, 'BLIND for the reader: Kempton 14:40, Fontwell 16:45, Goodwood 18:53', out)
    summary(READ, f'{len(READ)} read races — NOT evidence', out)
    out.append('')
    for r, W in BLIND.items(): detail(r, W, out)
    out.append('')
    out.append('-- every join in the read races (NOT evidence)')
    for r, W in READ.items():
        F, res, held = race(r); n = F['n']
        for P, js in res.items():
            for k, key, lv, txt in sorted(js):
                h = len(held[(k, key, lv)])
                out.append(f"   {r:30s} {P} {F['runners'][P][:34]:34s}{' WIN' if P == W else '    '} ({k}) {lv:5s} {key:44s} held {h}/{n}{' RARE' if h * 2 < n else ''}   {txt}")
    txt = '\n'.join(out); print(txt)
    open('docs/classic/star_join_scan.txt', 'w').write(txt + '\n')
