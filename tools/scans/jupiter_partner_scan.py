#!/usr/bin/env python3
"""jupiter_partner_scan.py  — read-only: does Jupiter's partner matter? (Eddie 12 Oct 2026). Reads only the frozen checklist reader's saved
outputs (docs/classic/<race>/checklist/P*.json and field.json), strict level. Node folded. Nothing is recomputed.

Each strict instance is parsed into Jupiter roles (Jupiter side, partner side, partner, plane, kind):
  natal Jupiter in a pair (cross link, pair in one chart, shared, pair set, ratio, family, h:j, split, midpoint, contact);
  sky Jupiter striking a natal body, or a sky body striking natal Jupiter; Jupiter–Jupiter across charts (same-body set, Equator ratio,
  movement, ratios in both charts, return) as its own partner; 'Jupiter alone' only for single-chart items (Equator value).
Chart sides kept for both ends (H Eris – J Jupiter apart from J Eris – H Jupiter), with a total per partner.
Multi-body items (8 triangle, 11 same number, 21 soak, 33 node loop) are in their own section. RARE = the item is held by fewer than half
the field (strict). Per row: runners with it (each once), winners vs beaten, wins (chance = sum of 1/field size over those runners).
The read races are NOT evidence; Kempton 14:40, Fontwell 16:45, Goodwood 18:53 (blind for the reader) are shown separately."""
import os, re, json
from collections import defaultdict

J = 'Jupiter'
FOCUS = ['Vesta', 'Eris', 'Pluto', 'Sun']
MULTI = {8: 'triangle', 11: 'same number / ratio in both charts', 21: 'soak', 33: 'node loop'}
READ = {'ascot_1350_20231021': 'P01', 'carlisle_1630_20220707': 'P07', 'catterick_1505_20211119': 'P07', 'chelmsford_aw_1320_20240118': 'P03',
        'ffos_las_1420_20220105': 'P05', 'fontwell_1530_20231006': 'P05', 'haydock_1405_20220219': 'P09', 'haydock_1718_20220507': 'P07',
        'huntingdon_1352_20211205': 'P05', 'lingfield_1500_20220123': 'P11', 'newbury_1350_20211126': 'P09', 'newcastle_1540_20220311': 'P05',
        'newcastle_aw_1220_20211112': 'P03', 'newcastle_aw_1330_20220102': 'P09', 'newcastle_aw_1540_20211112': 'P05', 'newcastle_aw_1640_20220215': 'P01',
        'newmarket_1535_20220414': 'P07', 'newton_abbot_1525_20220717': 'P07', 'nottingham_1530_20220601': 'P01', 'nottingham_1750_20220613': 'P03',
        'perth_1610_20220420': 'P09', 'sandown_1425_20211204': 'P05', 'sandown_1430_20240215': 'P13', 'sedgefield_1500_20220510': 'P01',
        'wincanton_1420_20220321': 'P07', 'wolverhampton_aw_1725_20231021': 'P05', 'york_1545_20240515': 'P11', 'york_1615_20240515': 'P25',
        'newmarket_july_1745_20240816': 'P01', 'exeter_1515_20211019': 'P11', 'redcar_1515_20211015': 'P05', 'haydock_1420_20210904': 'P03'}
BLIND = {'kempton_aw_1440_20210904': 'P05', 'fontwell_1645_20210914': 'P05', 'goodwood_1853_20210827': 'P09'}
NAMES = {1: 'cross struck 2+', 2: 'cross struck both ends', 3: 'partner strike', 4: 'pair together in sky', 5: 'both ends moved', 6: 'moved onto cross',
         7: 'swap', 9: 'in-chart pair struck', 10: 'in-chart pair struck 2+', 12: 'shared node', 13: 'shared pair', 14: 'shared + cross', 15: 'pair set',
         16: 'same-body set', 17: 'same-body 4:5:9', 18: 'same-body joined', 19: 'split', 20: 'midpoint', 22: 'sky/natal ratio', 23: 'ratios both charts',
         24: 'family / h:j', 25: 'Equator value', 26: 'Equator ratio', 27: 'return / contact', 28: 'RA+Dec on one body', 29: 'in-chart RA+Dec', 30: 'tightest cross'}
W_ = r'(\w+)'

def fold(b): return 'Node' if b in ('Rahu', 'Ketu') else b

def roles(x):
    """-> list of (jupiter side, partner side, partner, plane, kind)"""
    it, w = x['item'], x['what']; out = []
    def pair(ca, a, cb, b, pl, kind):
        a, b = fold(a), fold(b)
        if a == J and b == J: out.append((ca, cb, J, pl, kind))
        elif a == J: out.append((ca, cb, b, pl, kind))
        elif b == J: out.append((cb, ca, a, pl, kind))
    head, _, tail = w.partition(' — ')
    if it in (1, 2, 3, 9, 10, 28):
        for s, c, t, pl in re.findall(r'sky (\w+) -> ([HJ]) (\w+) (RA|Dec|Flat|GC)', w):
            pair('S', s, c, t, pl, f'{it} {NAMES[it]} (sky strike)')
    if it in (1, 2, 3, 4, 5, 6, 7, 14, 30):
        for h, j in re.findall(r'H (\w+) – J (\w+) RA', head if it not in (6, 14) else w):
            pair('H', h, 'J', j, 'link', f'{it} {NAMES[it]}')
    if it == 4:
        for a, b in re.findall(r'sky (\w+)–(\w+) (?:GC|close)', tail): pair('S', a, 'S', b, 'sky pair', f'4 {NAMES[4]} (sky pair)')
    if it in (5, 6):
        for c, b, pl in re.findall(r'([HJ]) (\w+) moved (RA|Dec|Flat|GC)', w):
            if b == J: out.append(('S', c, J, pl, f'{it} {NAMES[it]} (Jupiter moved)'))
    if it in (9, 10, 29):
        m = re.match(r'([HJ]) (\w+)–(\w+) ', w)
        if m: pair(m[1], m[2], m[1], m[3], 'pair', f'{it} {NAMES[it]}')
    if it == 13:
        m = re.match(r'shared (\w+)–(\w+) (\w+)', w)
        if m: pair('H+J', m[1], 'H+J', m[2], m[3], f'13 {NAMES[13]}')
    if it == 15:
        m = re.match(r'pair set (\w+)–(\w+) (\w+)', w)
        if m: pair('H+J+S', m[1], 'H+J+S', m[2], m[3], f'15 {NAMES[15]}')
    if it in (16, 17, 18):
        m = re.match(r'same-body (\w+) (\w+)', w)
        if m and fold(m[1]) == J: out.append(('S/H/J', 'S/H/J', J, m[2], f'{it} {NAMES[it]}'))
    if it == 19:
        m = re.match(r'([HJ]) (\w+) moved (RA|Dec) \(.*?\) toward ([HJ]) (\w+)', w)
        if m: pair(f'{m[1]}+S', m[2], m[4], m[5], m[3], f'19 {NAMES[19]}')
    if it == 20:
        m = re.match(r'([HJ]) (\w+) at the (RA|Dec) midpoint of ([HJ]) (\w+) and sky', w)
        if m: pair(m[1], m[2], f'{m[4]}+S', m[5], m[3], f'20 {NAMES[20]}')
    if it == 22:
        m = re.match(r'([HJ]) (\w+)–(\w+) (RA|Dec|Flat|GC) sky', w)
        if m: pair(f'{m[1]}+S', m[2], f'{m[1]}+S', m[3], m[4], f'22 {NAMES[22]}')
    if it == 23:
        m = re.match(r'(\w+): H', w)
        if m and fold(m[1]) == J: out.append(('H', 'J', J, 'ratios', f'23 {NAMES[23]}'))
    if it == 24:
        m = re.match(r'family ([HJ]) (\w+)–(\w+) (\w+) (?:sky (\w+) – ([HJ]) (\w+)|([HJ]) (\w+) – sky (\w+))', w)
        if m:
            if m[5]: pair('S', m[5], m[6], m[7], m[4], f'24 family (sky–natal leg)')
            else: pair(m[8], m[9], 'S', m[10], m[4], f'24 family (natal–sky leg)')
        m = re.match(r'h:j (\w+)–(\w+) (\w+)', w)
        if m: pair('H/J', m[1], 'H/J', m[2], m[3], '24 h:j')
    if it == 25:
        m = re.match(r'([HJ]) (\w+) \|Dec\|', w)
        if m and fold(m[2]) == J: out.append((m[1], '-', 'Jupiter alone', 'Equator', f'25 {NAMES[25]}'))
    if it == 26:
        m = re.match(r'Equator (\w+) (\w)/(\w) ', w)
        if m and fold(m[1]) == J: out.append((m[2], m[3], J, 'Equator', f'26 {NAMES[26]}'))
    if it == 27:
        m = re.match(r'(RETURN|contact) sky (\w+) on ([HJ]) (\w+)', w)
        if m: pair('S', m[2], m[3], m[4], 'contact', f"27 {'return' if m[1] == 'RETURN' else 'contact'}")
    return out

def multi_has(x):
    if x['item'] not in MULTI: return False
    return any(b.endswith(' Jupiter') for b in x['bodies']) or bool(re.search(r'\bS Jupiter\b|sky Jupiter|soak Jupiter', x['what']))

def collect(races):
    rows = defaultdict(lambda: {'r': set(), 'kinds': defaultdict(int)})
    tot = defaultdict(lambda: {'r': set(), 'kinds': defaultdict(int)})
    multi = defaultdict(lambda: {'r': set(), 'other': defaultdict(int)})
    field = {}
    for r, W in races.items():
        F = json.load(open(f'docs/classic/{r}/checklist/field.json')); n = F['n']; field[r] = (n, W)
        for P in F['runners']:
            inst = json.load(open(f'docs/classic/{r}/checklist/{P}.json'))['instances']
            for x in inst:
                if x['level'] != 'strict': continue
                rare = F['field'][str(x['item'])]['strict']['k'] * 2 < n
                for tag in ('rare', 'all') if rare else ('all',):
                    if x['item'] in MULTI:
                        if multi_has(x):
                            d = multi[(tag, x['item'])]; d['r'].add((r, P))
                            for b in x['bodies']:
                                if not b.endswith(' Jupiter'): d['other'][fold(b.split(' ', 1)[1])] += 1
                        continue
                    for js, ps, partner, pl, kind in roles(x):
                        key = (tag, partner, f'{js} Jupiter – {ps} {partner}')
                        rows[key]['r'].add((r, P)); rows[key]['kinds'][f'{kind} [{pl}]'] += 1
                        tot[(tag, partner)]['r'].add((r, P)); tot[(tag, partner)]['kinds'][f'{kind} [{pl}]'] += 1
    return rows, tot, multi, field

def stat(rs, field):
    nw = sum(1 for r in field); nb = sum(n - 1 for n, W in field.values())
    w = sum(1 for r, P in rs if field[r][1] == P); b = len(rs) - w
    ch = sum(1 / field[r][0] for r, P in rs)
    return f"W {w:2d}/{nw} {100 * w / nw:3.0f}%  B {b:3d}/{nb} {100 * b / nb:3.0f}%  wins {w} ({ch:.2f})"

def section(races, label, tag, out):
    rows, tot, multi, field = collect(races)
    out.append(f"-- {label} — {'RARE items only (held by < half the field)' if tag == 'rare' else 'all strict items'}")
    partners = sorted({k[1] for k in tot if k[0] == tag})
    order = [p for p in FOCUS if p in partners] + [J] * (J in partners) + sorted((p for p in partners if p not in FOCUS + [J]),
                                                                              key=lambda p: (-len(tot[(tag, p)]['r']), p))
    for p in order:
        t = tot[(tag, p)]
        out.append(f"   {('Jupiter–' + p) if p not in (J, 'Jupiter alone') else ('Jupiter–Jupiter (across charts)' if p == J else 'Jupiter alone'):34s} total  {stat(t['r'], field)}")
        for key in sorted(k for k in rows if k[0] == tag and k[1] == p):
            d = rows[key]
            kinds = ', '.join(f"{k} x{v}" for k, v in sorted(d['kinds'].items(), key=lambda kv: (-kv[1], kv[0]))[:5])
            out.append(f"      {key[2]:40s} {stat(d['r'], field)}   {kinds}")
    out.append(f"   multi-body items with Jupiter in them ({'rare' if tag == 'rare' else 'all strict'}):")
    for it in sorted(MULTI):
        d = multi.get((tag, it))
        if not d: out.append(f"      [{it}] {MULTI[it]}: none"); continue
        other = ', '.join(f"{b} {c}" for b, c in sorted(d['other'].items(), key=lambda kv: (-kv[1], kv[0]))[:8])
        out.append(f"      [{it}] {MULTI[it]:34s} {stat(d['r'], field)}   other bodies (instances): {other}")

if __name__ == '__main__':
    out = ["Jupiter's partner (read-only; frozen checklist reader CR v1.1 outputs, strict). W = winners with it / all winners; B = beaten with it /",
           "all beaten; chance = sum of 1/field size over the runners with it. Each runner counted once per row. Read races are NOT evidence."]
    for tag in ('rare', 'all'):
        section(BLIND, 'BLIND for the reader: Kempton 14:40, Fontwell 16:45, Goodwood 18:53', tag, out)
        section(READ, f'{len(READ)} read races — NOT evidence', tag, out)
        out.append('')
    # control (added after the first run): the same 'X–X across charts, rare' row with every body in Jupiter's place
    out.append('-- control: body X with itself across charts (H/J/S), RARE items — blind 3 races | 32 read races (NOT evidence)')
    for b in ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Node',
              'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto']:
        J = b; cells = []
        for races in (BLIND, READ):
            rows, tot, multi, field = collect(races)
            cells.append(stat(tot.get(('rare', b), {'r': set()})['r'], field))
        out.append(f"   {b:11s} {cells[0]}  |  {cells[1]}")
    J = 'Jupiter'
    txt = '\n'.join(out); print(txt)
    open('docs/classic/jupiter_partner_scan.txt', 'w').write(txt + '\n')
