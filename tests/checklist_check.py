#!/usr/bin/env python3
"""checklist_check.py [--step N] [--only ITEM]  — tests for tools/checklist_reader.py, written from docs/classic/winner_checklist.md.
Each check: (item, label, function returning True/False). Labels name the checklist item and race. Field claims ('ONLY runner',
'NOT unique', 'tightest') are checks too; WITHDRAWN claims are negative checks. Where the reader follows the checklist DEFINITION
and a hand read differs, the check says so in its label ('EXPLAINED: ...') and tests the reader's actual behaviour.
Run from the repo root. Exit code 1 if any check fails."""
import sys, os, json, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
import checklist_reader as CR

STEP = int(sys.argv[sys.argv.index('--step') + 1]) if '--step' in sys.argv else 4
ONLY = int(sys.argv[sys.argv.index('--only') + 1]) if '--only' in sys.argv else None
W = {'ascot_1350_20231021': 'P01', 'carlisle_1630_20220707': 'P07', 'catterick_1505_20211119': 'P07', 'chelmsford_aw_1320_20240118': 'P03',
     'ffos_las_1420_20220105': 'P05', 'fontwell_1530_20231006': 'P05', 'haydock_1405_20220219': 'P09', 'haydock_1718_20220507': 'P07',
     'huntingdon_1352_20211205': 'P05', 'lingfield_1500_20220123': 'P11', 'newbury_1350_20211126': 'P09', 'newcastle_1540_20220311': 'P05',
     'newcastle_aw_1220_20211112': 'P03', 'newcastle_aw_1330_20220102': 'P09', 'newcastle_aw_1540_20211112': 'P05', 'newcastle_aw_1640_20220215': 'P01',
     'newmarket_1535_20220414': 'P07', 'newton_abbot_1525_20220717': 'P07', 'nottingham_1530_20220601': 'P01', 'nottingham_1750_20220613': 'P03',
     'perth_1610_20220420': 'P09', 'sandown_1425_20211204': 'P05', 'sandown_1430_20240215': 'P13', 'sedgefield_1500_20220510': 'P01',
     'wincanton_1420_20220321': 'P07', 'wolverhampton_aw_1725_20231021': 'P05', 'york_1545_20240515': 'P11', 'york_1615_20240515': 'P25',
     'newmarket_july_1745_20240816': 'P01', 'dettori_ascot_19960928': 'P01', 'exeter_1515_20211019': 'P11', 'redcar_1515_20211015': 'P05',
     'haydock_1420_20210904': 'P03'}
A = {'asc': 'ascot_1350_20231021', 'car': 'carlisle_1630_20220707', 'cat': 'catterick_1505_20211119', 'che': 'chelmsford_aw_1320_20240118',
     'ffo': 'ffos_las_1420_20220105', 'fon': 'fontwell_1530_20231006', 'hy05': 'haydock_1405_20220219', 'hy18': 'haydock_1718_20220507',
     'hun': 'huntingdon_1352_20211205', 'lin': 'lingfield_1500_20220123', 'nby': 'newbury_1350_20211126', 'nc40': 'newcastle_1540_20220311',
     'aw20': 'newcastle_aw_1220_20211112', 'aw30': 'newcastle_aw_1330_20220102', 'aw15': 'newcastle_aw_1540_20211112', 'aw16': 'newcastle_aw_1640_20220215',
     'nm35': 'newmarket_1535_20220414', 'nab': 'newton_abbot_1525_20220717', 'not30': 'nottingham_1530_20220601', 'not50': 'nottingham_1750_20220613',
     'per': 'perth_1610_20220420', 's21': 'sandown_1425_20211204', 's24': 'sandown_1430_20240215', 'sed': 'sedgefield_1500_20220510',
     'win': 'wincanton_1420_20220321', 'wol': 'wolverhampton_aw_1725_20231021', 'y45': 'york_1545_20240515', 'y15': 'york_1615_20240515',
     'nmj': 'newmarket_july_1745_20240816', 'det': 'dettori_ascot_19960928', 'exe': 'exeter_1515_20211019', 'red': 'redcar_1515_20211015',
     'hy20': 'haydock_1420_20210904'}
_F = {}
def F(r):
    r = A.get(r, r)
    if r not in _F: _F[r] = CR.run(r, STEP)
    return _F[r]
def P_of(r, horse):
    for P, n in F(r)['runners'].items():
        if n.split(' / ')[0].split(' ', 1)[1] == horse: return P
    raise KeyError(f'{horse} not in {r}')
def _m(x, sub):
    if isinstance(sub, tuple): return any(_m(x, s) for s in sub)
    return sub in x['what']
def pr(p):
    """both orders of a pair name, e.g. pr('Chiron–Juno') -> ('Chiron–Juno', 'Juno–Chiron')"""
    a, b = p.split('–'); return (p, f'{b}–{a}')
def find(r, item, *subs, P=None, level='strict'):
    r = A.get(r, r); P = P or W[r]
    return [x for x in F(r)['per_runner'][P]['instances'] if x['item'] == item and (level is None or x['level'] == level) and all(_m(x, s) for s in subs)]
def has(r, item, *subs, P=None, level='strict'): return bool(find(r, item, *subs, P=P, level=level))
def who(r, item, level='strict', *subs):
    r = A.get(r, r)
    return sorted(P for P, x in F(r)['per_runner'].items() if any(i['item'] == item and i['level'] == level and all(_m(i, s) for s in subs) for i in x['instances']))
def only(r, item, level='strict', *subs): return who(r, item, level, *subs) == [W[A.get(r, r)]]
def tightest(r, item, level='strict', *subs):
    r = A.get(r, r); best = None
    for P, x in F(r)['per_runner'].items():
        for i in x['instances']:
            if i['item'] == item and i['level'] == level and all(_m(i, s) for s in subs) and (best is None or (i['t'], P) < best): best = (i['t'], P)
    return best[1] if best else None
def best_t(r, item, P=None, level='strict', *subs):
    xs = find(r, item, *subs, P=P, level=level); return min(x['t'] for x in xs) if xs else None
def sb(r, body, plane, ratios, P=None, level='strict'):
    return any(x['what'].startswith(f'same-body {body} {plane} ') and x['what'].split(' -> ')[1].split(' (')[0] == ' : '.join(ratios) or
               (x['what'].startswith(f'same-body {body} {plane} ') and sorted(x['what'].split(' -> ')[1].split(' (')[0].split(' : ')) == sorted(ratios))
               for x in find(r, 16, P=P, level=level))
def rt(r, chart, pair, plane, ratio, P=None, level='strict'):
    return any(x['chart'] == chart and x['plane'] == plane and x['ratio'] == ratio and _m(x, tuple(f'{chart} {q} {plane} ' for q in pr(pair))) for x in find(r, 22, P=P, level=level))

C = []   # (step, item, label, fn)
def chk(step, item, label, fn): C.append((step, item, label, fn))

# ============================================================== completeness: every Layer 1 item reaches the reader
def complete(item, key, keep=lambda R, i, x: True):
    def f():
        bad = []
        for r in sorted(set(A.values())):
            for P, x in F(r)['per_runner'].items():
                I = json.load(open(f'docs/classic/{r}/layer1/{P}.json')); T = json.load(open(f'docs/classic/{r}/layer2/{P}.json'))
                R = CR.Runner(P, I, T)
                n = sum(1 for i, y in enumerate(I[key]) if keep(R, i, y))
                m = sum(1 for i in x['instances'] if i['item'] == item)
                if n != m: bad.append(f'{r} {P} {n}!={m}')
        if bad: print('      ', bad[:5])
        return not bad
    return f
chk(1, 13, 'every Layer 1 shared pair is an item-13 instance (slow pairs as other)', complete(13, 'shared'))
chk(1, 15, 'every Layer 1 pair set is an item-15 instance', complete(15, 'pair_sets'))
chk(1, 16, 'every Layer 1 same-body set (less node mirrors) is an item-16 instance', complete(16, 'same_body', lambda R, i, x: not R.mirror(f'same_body:{i}')))
chk(1, 22, 'every Layer 1 sky/natal ratio is an item-22 instance', complete(22, 'ratios'))
chk(1, 24, 'every Layer 1 pair family + h:j item is an item-24 instance', lambda: complete(24, 'pair_family')() if False else all(
    sum(1 for i in x['instances'] if i['item'] == 24) == len(json.load(open(f'docs/classic/{r}/layer1/{P}.json'))['pair_family']) + len(json.load(open(f'docs/classic/{r}/layer1/{P}.json'))['hj_ratios'])
    for r in sorted(set(A.values())) for P, x in F(r)['per_runner'].items()))
chk(1, 26, 'every Layer 1 Equator ratio (less node mirrors) is an item-26 instance', complete(26, 'eq_ratios', lambda R, i, x: not R.mirror(f'eq_ratios:{i}')))

# ============================================================== step 1 items
# 13 shared pair
chk(1, 13, 'Exeter: Chiron–Juno GC 0.0035%', lambda: has('exe', 13, pr('Chiron–Juno'), 'GC', '(0.0035%)'))
chk(1, 13, 'Exeter: winner tightest shared pair in field (slow pairs out)', lambda: tightest('exe', 13) == 'P11')
chk(1, 13, 'Exeter: next Caspers Court Saturn–Makemake 0.0227%', lambda: has('exe', 13, pr('Saturn–Makemake'), '(0.0227%)', P='P01'))
chk(1, 13, 'Exeter: Blaze A Trail Gonggong–Transpluto 0.0115% listed as slow pair (age)', lambda: has('exe', 13, pr('Gonggong–Transpluto'), '(0.0115%)', 'age', P='P09', level='other'))
chk(1, 13, 'Venturous: Rahu–Sedna GC 0.006%', lambda: has('aw30', 13, pr('Rahu–Sedna'), 'GC', '(0.006'))
chk(1, 13, 'Venturous: Mars–Rahu GC 0.041%', lambda: has('aw30', 13, pr('Mars–Rahu'), 'GC', '(0.04'))
chk(1, 13, 'DIFFERENCE: Venturous field claim "no other runner has a shared pair with a fast body within 0.1%" — King Of Stars has Neptune–Rahu RA 0.0327% (only if Rahu counts as fast)',
    lambda: [P for P, x in F('aw30')['per_runner'].items() if P != 'P09' and any(i['item'] == 13 and i['level'] == 'strict' and i['t'] < 0.2 for i in x['instances'])] == [P_of('aw30', 'King Of Stars')]
            and has('aw30', 13, pr('Neptune–Rahu'), 'RA', '(0.0327%)', P=P_of('aw30', 'King Of Stars')))
chk(1, 13, 'Wolverhampton: Neptune–Rahu RA 0.0016%', lambda: has('wol', 13, pr('Neptune–Rahu'), 'RA', '(0.0016%)'))
chk(1, 13, 'Newbury: Juno–Pallas RA 138.2873 / 138.8180', lambda: has('nby', 13, pr('Juno–Pallas'), 'RA', '138.2873', '138.8180'))
chk(1, 13, 'Carlisle: Ceres–Transpluto Flat 0.044%', lambda: has('car', 13, pr('Ceres–Transpluto'), 'Flat', '(0.04'))
chk(1, 13, 'Carlisle: Pallas–Vesta GC 154.6004 / 154.4540', lambda: has('car', 13, pr('Pallas–Vesta'), 'GC', '154.6004', ('154.4540', '154.4539')))
chk(1, 13, 'Fontwell: Gonggong–Orcus GC 0.005% (EXPLAINED: slow pair, listed as other/age by the item-13 definition)', lambda: has('fon', 13, pr('Gonggong–Orcus'), 'GC', level='other'))
chk(1, 13, 'Haydock 14:05: Uranus–Pluto Dec 18.6583 / 18.5947', lambda: has('hy05', 13, pr('Uranus–Pluto'), 'Dec', '18.6583', '18.5947'))
chk(1, 13, 'Newton Abbot: Uranus–Juno GC 0.021%', lambda: has('nab', 13, pr('Uranus–Juno'), 'GC', '(0.021'))
chk(1, 13, 'Newton Abbot: Ceres–Makemake GC 0.020%', lambda: has('nab', 13, pr('Ceres–Makemake'), 'GC', '(0.019', ) or has('nab', 13, pr('Ceres–Makemake'), 'GC', '(0.020'))
chk(1, 13, 'Perth: Ketu–Haumea Flat 159.1720 / 158.8583', lambda: has('per', 13, pr('Ketu–Haumea'), 'Flat', '159.1720', '158.8583'))
chk(1, 13, 'Perth: Pallas–Juno RA 141.9906 / 141.5359', lambda: has('per', 13, pr('Pallas–Juno'), 'RA', '141.9906', '141.5359'))
chk(1, 13, 'Perth: Mars–Jupiter GC 0.008%', lambda: has('per', 13, pr('Mars–Jupiter'), 'GC', '(0.007') or has('per', 13, pr('Mars–Jupiter'), 'GC', '(0.008'))
chk(1, 13, 'Sedgefield: Haumea–Makemake RA (EXPLAINED: slow pair -> other/age)', lambda: has('sed', 13, pr('Haumea–Makemake'), 'RA', '18.0078', '18.0197', level='other'))
chk(1, 13, 'Sandown 2024: Mercury–Pluto Dec 34.2213 / 34.2508', lambda: has('s24', 13, pr('Mercury–Pluto'), 'Dec', '34.2213', '34.2508'))
chk(1, 13, 'Ffos Las: Jupiter–Vesta GC 0.41%', lambda: has('ffo', 13, pr('Jupiter–Vesta'), 'GC', ('107.3912', '107.3911'), '107.8361'))
chk(1, 13, 'Newmarket July: Uranus–Ketu Dec, Chiron–Rahu Dec, Chiron–Ketu Flat', lambda: has('nmj', 13, pr('Uranus–Ketu'), 'Dec') and has('nmj', 13, pr('Chiron–Rahu'), 'Dec') and has('nmj', 13, pr('Chiron–Ketu'), 'Flat'))
chk(1, 13, 'York 16:15: Eris–Haumea Flat (age effect -> other)', lambda: has('y15', 13, pr('Eris–Haumea'), 'Flat', '169.9651', '169.4628', level='other'))
# 15 pair sets
chk(1, 15, 'Carlisle: Ceres–Eris Dec 9/8, 7/4, 14/9 (worst 0.0223%)', lambda: has('car', 15, pr('Ceres–Eris'), 'Dec', '0.0223%'))
chk(1, 15, 'Carlisle field: ONLY full three-way set', lambda: only('car', 15))
chk(1, 15, 'Haydock 17:18: Sedna–Haumea RA and Venus–Saturn Dec', lambda: has('hy18', 15, pr('Sedna–Haumea'), 'RA') and has('hy18', 15, pr('Venus–Saturn'), 'Dec'))
chk(1, 15, 'Haydock 17:18 field: ONLY runner with full three-way sets', lambda: only('hy18', 15))
chk(1, 15, 'Newcastle 15:40: Vesta–Sedna Flat 22/7, 11/4, 8/7 (0.0305%)', lambda: has('nc40', 15, pr('Vesta–Sedna'), 'Flat', '0.0305%'))
chk(1, 15, 'Newcastle 15:40 field: ONLY full set', lambda: only('nc40', 15))
chk(1, 15, 'Huntingdon: Neptune–Rahu RA H 90.5696 J 67.9376 S 67.9409', lambda: has('hun', 15, pr('Neptune–Rahu'), 'RA', '90.5696'))
chk(1, 15, 'Huntingdon field: ONLY runner with a Neptune–Rahu set', lambda: only('hun', 15, 'strict', pr('Neptune–Rahu')))
chk(1, 15, 'Chelmsford: Saturn–Neptune Dec 2, 9/5, 18/5 (0.0243%)', lambda: has('che', 15, pr('Saturn–Neptune'), 'Dec', '0.0243%'))
chk(1, 15, 'Chelmsford field: NOT unique (Reset Button, Buford, Duveen have sets)', lambda: {P_of('che', 'Reset Button'), P_of('che', 'Buford'), P_of('che', 'Duveen')} <= set(who('che', 15)))
chk(1, 15, 'Exeter: Jupiter–Vesta RA 7/4, 3/2, 7/6 (0.0159%)', lambda: has('exe', 15, pr('Jupiter–Vesta'), 'RA', '0.0159%'))
chk(1, 15, 'NOT a set: Wolverhampton Jupiter–Sedna RA', lambda: not has('wol', 15, pr('Jupiter–Sedna')))
chk(1, 15, 'WITHDRAWN: Newcastle AW 13:30 Mercury–Orcus Dec not a set', lambda: not has('aw30', 15, pr('Mercury–Orcus')))
for r, losers in (('asc', ['Mill Stream', 'Sandrine', 'Vadream', 'Ocean Quest']), ('aw30', ['Good Effort', 'Regional']), ('not50', ['Miss Britain', 'Baileys Liberty']),
                  ('s24', ['Aston Martini', 'Little Miss Dante', 'Smiling Getaway']), ('sed', ['Wheres Maud Gone']),                   ('y45', ['Classical Song']), ('nmj', ['Double Meaning', 'King Of Cities', 'Knights Gold', 'Big Gypsy King'])):
    chk(1, 15, f'{A[r]}: winner has no pair set, losers {", ".join(losers)} do',
        (lambda r, losers: lambda: not has(r, 15) and all(P_of(r, h) in who(r, 15) for h in losers))(r, losers))
chk(1, 15, 'DIFFERENCE: Wolverhampton — checklist says winner had no full three-way while Gladly Ever After, Come On You Spurs and another did; Layer 1 gives the winner Pallas–Transpluto RA 13/8, 26/7, 16/7 (0.034%), Gladly Ever After none, Come On You Spurs Sun–Ketu Flat',
    lambda: has('wol', 15, pr('Pallas–Transpluto'), 'RA', '0.0340%') and P_of('wol', 'Gladly Ever After') not in who('wol', 15) and P_of('wol', 'Come On You Spurs') in who('wol', 15))
chk(1, 15, 'Newmarket 15:35: winner none, Masekela has one', lambda: not has('nm35', 15) and P_of('nm35', 'Masekela') in who('nm35', 15))
chk(1, 15, 'Nottingham 15:30: winner none, Ballet Steps has one', lambda: not has('not30', 15) and P_of('not30', 'Ballet Steps') in who('not30', 15))
# 16 / 17 same-body sets
SB = [('s24', 'Mercury', 'RA', ['9/8', '17/8', '17/9']), ('aw16', 'Venus', 'RA', ['11/5', '11/6', '6/5']), ('aw16', 'Gonggong', 'Dec', ['7/2', '9/2', '9/7']),
      ('not50', 'Vesta', 'RA', ['8', '9', '9/8']), ('not50', 'Vesta', 'Dec', ['7', '8', '8/7']), ('s21', 'Uranus', 'Flat', ['5/2', '7/2', '7/5']), ('s21', 'Quaoar', 'GC', ['3', '4', '4/3']),
      ('aw15', 'Orcus', 'RA', ['7', '8', '8/7']), ('aw15', 'Jupiter', 'RA', ['3/2', '2', '3']), ('aw20', 'Gonggong', 'RA', ['6', '7', '7/6']), ('car', 'Mercury', 'GC', ['12/7', '7/5', '12/5']),
      ('che', 'Transpluto', 'Dec', ['7', '8', '8/7']), ('che', 'Jupiter', 'Dec', ['6/5', '5', '6']), ('fon', 'Juno', 'Dec', ['3/2', '5/3', '5/2']), ('fon', 'Venus', 'Dec', ['3/2', '5/3', '5/2']),
      ('hy18', 'Vesta', 'GC', ['13/4', '9/4', '13/9']), ('hy18', 'Sun', 'RA', ['3', '2', '3/2']), ('lin', 'Mercury', 'GC', ['5/4', '9/4', '9/5']), ('lin', 'Mercury', 'RA', ['5/4', '9/4', '9/5']),
      ('lin', 'Sedna', 'GC', ['5/2', '7/2', '7/5']), ('lin', 'Mars', 'Dec', ['15/7', '15/8', '8/7']), ('nby', 'Vesta', 'RA', ['7/3', '10/7', '10/3']), ('nby', 'Haumea', 'RA', ['5/2', '7/2', '7/5']),
      ('nc40', 'Ceres', 'Dec', ['5/3', '3/2', '5/2']), ('nc40', 'Chiron', 'Dec', ['7/3', '4/3', '7/4']), ('nm35', 'Mercury', 'RA', ['8/3', '5/3', '8/5']), ('nmj', 'Uranus', 'RA', ['6', '7', '7/6']),
      ('nmj', 'Chiron', 'Dec', ['5/4', '9/4', '9/5']), ('per', 'Uranus', 'RA', ['8/3', '11/3', '11/8']), ('red', 'Pallas', 'Dec', ['11/7', '7/4', '11/4']), ('y15', 'Rahu', 'Dec', ['9/4', '5/4', '9/5']),
      ('y15', 'Chiron', 'GC', ['6', '5', '6/5']), ('exe', 'Chiron', 'Dec', ['9/4', '5/4', '9/5'])]
for r, b, pl, rs in SB: chk(1, 16, f'{A[r]}: same-body {b} {pl} {" : ".join(rs)}', (lambda r, b, pl, rs: lambda: sb(r, b, pl, rs))(r, b, pl, rs))
chk(1, 16, 'Sandown 2024 field: Mercury RA set tightest (next P01 Uranus Dec)', lambda: tightest('s24', 16) == 'P13')
chk(1, 16, 'Newcastle AW 16:40 field: Venus RA set tightest', lambda: tightest('aw16', 16) == 'P01')
chk(1, 16, 'Nottingham 17:50 field: NOT tightest — Baileys Liberty Rahu/Ketu RA slightly tighter', lambda: tightest('not50', 16) == P_of('not50', 'Baileys Liberty'))
chk(1, 16, 'Sandown 2021 field: winner tightest of five', lambda: tightest('s21', 16) == 'P05')
chk(1, 16, 'Carlisle field: winner tightest', lambda: tightest('car', 16) == 'P07')
chk(1, 16, 'Redcar field: Hogan Pallas Dec tightest', lambda: tightest('red', 16) == 'P05')
chk(1, 16, 'Newcastle AW 15:40 field: no other runner has an Orcus RA set closer than 0.18%', lambda: all(not any(i['item'] == 16 and i['what'].startswith('same-body Orcus RA ') for i in x['instances'])
                                                                                                    for P, x in F('aw15')['per_runner'].items() if P != 'P05'))
chk(1, 16, 'EXPLAINED: Carlisle Sun Dec 2, 2, 1 not a set (contains a 1; item 16 says not 1)', lambda: not sb('car', 'Sun', 'Dec', ['2', '2', '1']))
chk(1, 16, 'WITHDRAWN: York 16:15 Quaoar Flat 63/8 : 62/7 : 9/8 (p > 30) not a set', lambda: not any(i['what'].startswith('same-body Quaoar Flat') for i in find('y15', 16)))
chk(1, 16, 'Huntingdon loser Master Tommytucker: Uranus GC 5/4, 9/4, 9/5 and Transpluto GC 4/3, 7/4, 7/3', lambda: sb('hun', 'Uranus', 'GC', ['5/4', '9/4', '9/5'], P=P_of('hun', 'Master Tommytucker'))
                                                                                                         and sb('hun', 'Transpluto', 'GC', ['4/3', '7/4', '7/3'], P=P_of('hun', 'Master Tommytucker')))
chk(1, 16, 'Venturous: no tight same-body set (none under 0.01%)', lambda: (best_t('aw30', 16) or 99) > 0.01 / 0.15)
chk(1, 17, 'York 16:15: node Dec 9/4 : 5/4 : 9/5', lambda: has('y15', 17, ('same-body Rahu Dec', 'same-body Ketu Dec')))
chk(1, 17, 'Newmarket July: Chiron Dec 9/4 : 5/4 : 9/5 (0.034%)', lambda: has('nmj', 17, 'same-body Chiron Dec'))
chk(1, 17, 'Exeter: Chiron Dec (0.0552%)', lambda: has('exe', 17, 'same-body Chiron Dec', '(worst 0.0552%)'))
chk(1, 17, 'Exeter field: ONLY runner', lambda: only('exe', 17))
chk(1, 17, 'Newcastle AW 12:20: Ceres', lambda: has('aw20', 17, 'same-body Ceres Dec'))
chk(1, 17, 'Nottingham 17:50: Juno', lambda: has('not50', 17, 'same-body Juno Dec'))
# 19 split
chk(1, 19, 'Dettori: sky Sun moved Dec 21 toward J Chiron: span 28.01379 = 21 + 7.01412, span/other 4', lambda: has('det', 19, 'J Sun moved Dec (21) toward J Chiron', 'span 28.01379', 'span/other 4'))
# 22 ratios (winners' tightest, checklist item 22)
R22 = [('aw20', 'J', 'Gonggong–Uranus', 'Dec', '18'), ('aw20', 'J', 'Neptune–Rahu', 'GC', '9/4'), ('aw16', 'H', 'Venus–Uranus', 'Dec', '13/7'), ('aw16', 'H', 'Mars–Chiron', 'RA', '13/6'),
       ('aw16', 'J', 'Saturn–Vesta', 'Flat', '23/6'), ('aw16', 'J', 'Chiron–Rahu', 'GC', '7/6'), ('nby', 'H', 'Juno–Pallas', 'RA', '2'), ('nby', 'J', 'Chiron–Transpluto', 'Dec', '5'),
       ('nby', 'H', 'Saturn–Transpluto', 'GC', '5/3'), ('nby', 'J', 'Haumea–Pallas', 'Dec', '23/9'), ('hun', 'H', 'Mars–Neptune', 'Dec', '7/4'), ('hun', 'H', 'Juno–Gonggong', 'Dec', '3'),
       ('s21', 'H', 'Mercury–Uranus', 'Flat', '25/3'), ('s21', 'H', 'Venus–Jupiter', 'Dec', '17/5'), ('s21', 'J', 'Juno–Makemake', 'GC', '11/9'), ('aw30', 'J', 'Jupiter–Uranus', 'Flat', '8/7'),
       ('aw30', 'H', 'Chiron–Makemake', 'Dec', '16/9'), ('aw30', 'H', 'Saturn–Juno', 'Flat', '19/6'), ('aw30', 'J', 'Pallas–Juno', 'GC', '23/9'), ('ffo', 'H', 'Chiron–Transpluto', 'Dec', '21/8'),
       ('ffo', 'H', 'Jupiter–Ketu', 'Dec', '3/2'), ('ffo', 'H', 'Rahu–Eris', 'RA', '11/2'), ('ffo', 'J', 'Neptune–Orcus', 'RA', '8/7'), ('ffo', 'J', 'Neptune–Vesta', 'GC', '14/9'),
       ('lin', 'H', 'Chiron–Transpluto', 'Dec', '14/5'), ('lin', 'H', 'Jupiter–Haumea', 'Dec', '7'), ('lin', 'H', 'Venus–Sedna', 'RA', '17/3'), ('hy05', 'H', 'Pluto–Ceres', 'Flat', '2'),
       ('hy05', 'H', 'Sun–Sedna', 'Dec', '27'), ('nc40', 'J', 'Ceres–Mars', 'RA', '14/9'), ('nc40', 'J', 'Sun–Vesta', 'Dec', '8/3'), ('nm35', 'H', 'Rahu–Makemake', 'RA', '11/6'),
       ('nm35', 'J', 'Neptune–Vesta', 'RA', '21/5'), ('nm35', 'J', 'Sun–Chiron', 'RA', '13'), ('per', 'J', 'Ketu–Haumea', 'RA', '12'), ('per', 'J', 'Sun–Chiron', 'Dec', '27/7'),
       ('win', 'J', 'Neptune–Chiron', 'Dec', '26/7'), ('win', 'J', 'Jupiter–Vesta', 'RA', '4'), ('hy18', 'J', 'Ketu–Transpluto', 'Dec', '11/6'), ('nab', 'J', 'Mars–Neptune', 'RA', '30/7'),
       ('nab', 'J', 'Neptune–Vesta', 'RA', '4/3'), ('nab', 'H', 'Neptune–Vesta', 'Flat', '20/7'), ('not30', 'H', 'Neptune–Rahu', 'GC', '11/5'), ('not30', 'J', 'Vesta–Orcus', 'RA', '11/9'),
       ('not50', 'H', 'Vesta–Rahu', 'RA', '17/9'), ('not50', 'J', 'Neptune–Orcus', 'Dec', '24/7'), ('sed', 'H', 'Sedna–Haumea', 'Dec', '9/7'), ('sed', 'H', 'Sun–Mars', 'Dec', '25/7'),
       ('car', 'H', 'Uranus–Quaoar', 'Dec', '7/6'), ('car', 'J', 'Ketu–Sedna', 'Dec', '16/5'), ('che', 'H', 'Jupiter–Rahu', 'RA', '10'), ('che', 'J', 'Sedna–Orcus', 'Dec', '28/9'),
       ('asc', 'J', 'Mars–Pallas', 'Flat', '5/4'), ('asc', 'H', 'Jupiter–Orcus', 'RA', '25/9'), ('fon', 'J', 'Vesta–Rahu', 'Dec', '15/8'), ('fon', 'J', 'Haumea–Makemake', 'Dec', '7/4'),
       ('wol', 'H', 'Neptune–Quaoar', 'Dec', '6/5'), ('wol', 'J', 'Uranus–Sedna', 'Dec', '23/8'), ('s24', 'J', 'Mercury–Pluto', 'RA', '19/2'), ('s24', 'H', 'Venus–Ceres', 'GC', '11/6'),
       ('y45', 'H', 'Rahu–Makemake', 'Flat', '11/8'), ('y45', 'H', 'Ketu–Sedna', 'Dec', '19/9'), ('y15', 'H', 'Venus–Saturn', 'GC', '12/5'), ('y15', 'J', 'Uranus–Pluto', 'GC', '15/7'),
       ('y15', 'H', 'Chiron–Transpluto', 'Dec', '11/2'), ('nmj', 'H', 'Pluto–Rahu', 'RA', '9/5'), ('nmj', 'J', 'Mercury–Chiron', 'Dec', '28/3'), ('exe', 'J', 'Chiron–Juno', 'Dec', '7/10'),
       ('exe', 'J', 'Mercury–Juno', 'Dec', '7/5'), ('exe', 'J', 'Pallas–Juno', 'Flat', '6/5'), ('exe', 'H', 'Saturn–Pallas', 'GC', '7/5'), ('hy20', 'H', 'Ceres–Orcus', 'Flat', '17/8')]
for r, c, p, pl, ratio in R22:
    ratio2 = '10/7' if ratio == '7/10' else ratio   # Layer 1 writes ratios >= 1 with a direction
    chk(1, 22, f'{A[r]}: {c} {p} {pl} {ratio}', (lambda r, c, p, pl, ratio2: lambda: rt(r, c, p, pl, ratio2))(r, c, p, pl, ratio2))
# 24 pair family / h:j
chk(1, 24, 'Redcar: Hogan Chiron–Sedna pair family 7/2 (0.0009%)', lambda: has('red', 24, 'family J', pr('Chiron–Sedna'), ' 7/2 (0.0009%)'))
chk(1, 24, 'Haydock 14:20: Fanning Ceres–Transpluto family 4/3 (0.0002%)', lambda: has('hy20', 24, 'family J', pr('Ceres–Transpluto'), ' 4/3 (0.0002%)'))
chk(1, 24, 'Haydock 14:20: Fanning Ceres – sky Orcus vs natal 8/5 (GC, 0.0020%)', lambda: has('hy20', 24, 'family J', pr('Ceres–Orcus'), 'GC', ' 8/5 (0.0020%)'))
chk(1, 24, 'Haydock 14:20: horse Rahu – sky Orcus vs sky pair 26/9 (GC, 0.0033%)', lambda: has('hy20', 24, 'family H', pr('Rahu–Orcus'), 'GC', ' 26/9 (0.0033%)'))
chk(1, 24, 'Carlisle: Ketu–Sedna Dec h:j 29/8 (0.00002%)', lambda: has('car', 24, 'h:j', pr('Ketu–Sedna'), 'Dec', ' 29/8 (0.0000%)'))
chk(1, 24, 'Exeter: h:j Ketu–Eris Flat 29/5 (0.0001%)', lambda: has('exe', 24, 'h:j', pr('Ketu–Eris'), 'Flat', ' 29/5 (0.0001%)'))
chk(1, 24, 'Newbury: Chiron–Transpluto RA j/h 21/8 (0.0114%, near)', lambda: has('nby', 24, 'h:j', pr('Chiron–Transpluto'), 'RA', ' 21/8 (0.0114%)', level='near'))
# 26 Equator ratios
E26 = [('aw30', 'Sun', 'S/H', '12', 'strict'), ('aw30', 'Orcus', 'S/J', '13/2', 'near'), ('nmj', 'Uranus', 'H/J', '7/5', 'strict'), ('nmj', 'Ceres', 'H/J', '7/6', 'strict'),
       ('car', 'Gonggong', 'H/J', '9/4', 'strict'), ('hy05', 'Sedna', 'S/J', '15/8', 'strict'), ('hy05', 'Sedna', 'H/J', '11/7', 'strict'), ('hy05', 'Pluto', 'S/H', '6/5', 'near'),
       ('hy18', 'Gonggong', 'H/J', '2', 'strict'), ('hy18', 'Saturn', 'S/H', '3/2', 'strict'), ('asc', 'Haumea', 'S/J', '5/3', 'strict'), ('asc', 'Rahu', 'H/J', '2', 'near'),
       ('che', 'Quaoar', 'S/J', '4/3', 'near'), ('nc40', 'Sedna', 'H/J', '12/7', 'near'), ('nc40', 'Uranus', 'S/H', '13/3', 'near'), ('aw20', 'Ceres', 'S/J', '7/4', 'strict'),
       ('aw16', 'Ceres', 'S/J', '11/5', 'near'), ('nm35', 'Uranus', 'S/H', '11/8', 'near'), ('nm35', 'Vesta', 'S/H', '17/6', 'near'), ('not30', 'Pluto', 'S/J', '5', 'near'),
       ('not50', 'Uranus', 'S/J', '7/5', 'strict'), ('s24', 'Makemake', 'H/J', '5/4', 'strict'), ('s24', 'Orcus', 'S/H', '11/8', 'near'), ('fon', 'Sun', 'H/J', '18/5', 'near'),
       ('fon', 'Vesta', 'S/H', '3/2', 'near'), ('nab', 'Pallas', 'S/J', '5/4', 'near'), ('sed', 'Saturn', 'H/J', '13/7', 'near'), ('win', 'Pallas', 'S/H', '21/5', 'near'),
       ('win', 'Haumea', 'H/J', '6/5', 'near'), ('wol', 'Chiron', 'S/H', '16/9', 'near'), ('hun', 'Neptune', 'S/H', '9/4', 'near'), ('y45', 'Venus', 'H/J', '7/6', 'strict'),
       ('y45', 'Vesta', 'S/J', '2', 'near'), ('aw15', 'Mercury', 'S/H', '19', 'near')]
for r, b, pair, ratio, lv in E26:
    chk(1, 26, f'{A[r]}: Equator {b} {pair} {ratio} ({lv})', (lambda r, b, pair, ratio, lv: lambda: has(r, 26, f'Equator {b} {pair} ', f' {ratio} (', level=lv))(r, b, pair, ratio, lv))
chk(1, 26, 'Venturous field: ONLY sky-involving Equator ratio', lambda: [P for P, x in F('aw30')['per_runner'].items() if any(i['item'] == 26 and i['level'] == 'strict' and ' S/' in i['what'] for i in x['instances'])] == ['P09'])
chk(1, 26, 'Newmarket July field (H/J <= 0.01%): Arabian Poet Rahu 22/7, King Of Cities Venus 11/7', lambda: has('nmj', 26, 'Equator Rahu H/J', ' 22/7 (', P=P_of('nmj', 'Arabian Poet'))
                                                                                                   and has('nmj', 26, 'Equator Venus H/J', ' 11/7 (', P=P_of('nmj', 'King Of Cities')))
# 27 return / contact
chk(1, 27, 'Newbury: RETURN sky Mars on J Mars RA 0.2440 Dec 1.1227', lambda: has('nby', 27, 'RETURN sky Mars on J Mars', 'RA 0.2440', 'Dec 1.1227'))
chk(1, 27, 'Newbury field: ONLY return in the whole field', lambda: [P for P, x in F('nby')['per_runner'].items() if any(i['item'] == 27 and i['what'].startswith('RETURN') for i in x['instances'])] == ['P09'])
chk(1, 27, 'Newbury: sky Vesta on Sheppard Mars Dec 0.0494', lambda: has('nby', 27, 'contact sky Vesta on J Mars', 'Dec 0.0494'))
chk(1, 27, 'Newcastle AW 12:20: sky Gonggong -> H Chiron RA 0.0674, -> H Neptune Dec 0.0950; sky Uranus -> H Venus RA 0.2371',
    lambda: has('aw20', 27, 'sky Gonggong on H Chiron RA 0.0674') and has('aw20', 27, 'sky Gonggong on H Neptune', 'Dec 0.0950') and has('aw20', 27, 'sky Uranus on H Venus RA 0.2371'))
chk(1, 27, 'Newcastle AW 16:40: sky Gonggong -> H Chiron RA 0.4812; sky Neptune -> H Chiron Dec 0.1621; sky Uranus -> J Sedna RA 0.1349',
    lambda: has('aw16', 27, 'sky Gonggong on H Chiron RA 0.4812') and has('aw16', 27, 'sky Neptune on H Chiron', 'Dec 0.1621') and has('aw16', 27, 'sky Uranus on J Sedna RA 0.1349'))
chk(1, 27, 'Haydock 14:20: sky Orcus on J Ketu RA 1.435; sky Transpluto on H Orcus RA 1.147', lambda: has('hy20', 27, 'sky Orcus on J Ketu RA 1.43') and has('hy20', 27, 'sky Transpluto on H Orcus RA 1.14'))


# ============================================================== step 2 items
def xl(x, h, j): return x['what'].startswith(f'H {h} – J {j} ') or f' on H {h} – J {j} ' in x['what']
def xb(r, h, j, sky, P=None, level=None):
    """cross link H h – J j struck on both ends by sky body `sky` (node folded), from the full end lists (items 1/2)"""
    sk = ('Rahu', 'Ketu') if sky == 'Node' else (sky,)
    for x in find(r, 1, P=P, level=level) + find(r, 2, P=P, level=level):
        if xl(x, h, j) and any(e.startswith(f'sky {k} -> H {h} ') for e in x['ends'][0] for k in sk) and any(e.startswith(f'sky {k} -> J {j} ') for e in x['ends'][1] for k in sk): return True
    return False
def xe(r, h, j, sa, sb_, P=None, level=None):
    """cross link struck on its H end by strike text sa and J end by sb_ (substrings of the strike lines)"""
    for x in find(r, 1, P=P, level=level) + find(r, 2, P=P, level=level):
        if xl(x, h, j) and any(sa in e for e in x['ends'][0]) and any(sb_ in e for e in x['ends'][1]): return True
    return False
def p9(r, chart, a, b, sky, P=None):
    """pair in one chart struck on both ends by `sky` (items 9 or 10)"""
    return any((x['what'].startswith(f'{chart} {a}–{b} ') or x['what'].startswith(f'{chart} {b}–{a} ')) and f' {sky}: ' in ' ' + x['what'].split(' — ', 1)[1].replace('; ', ' ')
               for x in find(r, 9) + find(r, 10) if True for _ in [0] if (P is None or True)) if P is None else any(
               (x['what'].startswith(f'{chart} {a}–{b} ') or x['what'].startswith(f'{chart} {b}–{a} ')) and f' {sky}: ' in ' ' + x['what'].split(' — ', 1)[1].replace('; ', ' ')
               for x in find(r, 9, P=P) + find(r, 10, P=P))
def mv6(r, chart, body, plane, n, h, j, P=None, level=None):
    return any(x['what'].startswith(f'{chart} {body} moved {plane} ') and f'({n}) — on H {h} – J {j} ' in x['what'] for x in find(r, 6, P=P, level=level))
def anyl(r, item, h, j, P=None, level=None): return [x for x in find(r, item, P=P, level=level) if xl(x, h, j)]

# 1 cross link struck on both ends by 2+ sky bodies
chk(2, 1, 'Perth: H Ceres – J Uranus RA 0.9991 struck by sky Ceres and sky node', lambda: any(xl(x, 'Ceres', 'Uranus') and 'Ceres:' in x['what'] and 'Node:' in x['what'] for x in find('per', 1)))
chk(2, 1, 'Perth field: ONLY runner', lambda: only('per', 1))
chk(2, 1, 'Nottingham 15:30: H Sedna – J Chiron Dec 0.0055 struck by THREE (Venus, Ceres, Juno)', lambda: any(xl(x, 'Sedna', 'Chiron') and 'struck by 3' in x['what'] and all(k + ':' in x['what'] for k in ('Venus', 'Ceres', 'Juno')) for x in find('not30', 1)))
chk(2, 1, 'Nottingham 15:30 field: ONLY runner', lambda: only('not30', 1))
chk(2, 1, 'Chelmsford: H Chiron – J Rahu Dec 0.337 (near band) by sky Chiron and sky Ceres', lambda: any(xl(x, 'Chiron', 'Rahu') and 'Chiron:' in x['what'] and 'Ceres:' in x['what'] for x in find('che', 1, level='near')))
chk(2, 1, 'DIFFERENCE: Chelmsford field "ONLY runner" — reader also finds P11 H Mercury – J Neptune Dec 0.4792 (near band) struck by node and Makemake, all Flat strikes; ONLY runner when Flat strikes are left out',
    lambda: sorted(set(who('che', 1, 'strict')) | set(who('che', 1, 'near'))) == ['P03', 'P11'] and all(e['what'].count('Flat') >= 4 for e in find('che', 1, P='P11', level='near')))
chk(2, 1, 'Absent in winner: Newmarket July', lambda: not has('nmj', 1))
chk(2, 1, 'York 16:15: none in field (strict)', lambda: who('y15', 1) == [])
chk(2, 1, 'Sandown 2024: none in field (strict)', lambda: who('s24', 1) == [])
chk(2, 1, 'Exeter loser Jarlath: field-only', lambda: who('exe', 1) == [P_of('exe', 'Jarlath')])
# 2 cross link struck on both ends
chk(2, 2, 'Huntingdon: sky Juno on H Orcus – J Vesta (Dec 64/9 | Dec 32)', lambda: xe('hun', 'Orcus', 'Vesta', 'sky Juno -> H Orcus Dec 7.11139 (64/9)', 'sky Juno -> J Vesta Dec 32.00451 (32)'))
chk(2, 2, 'Huntingdon: sky Haumea on H Pluto – J Neptune (RA 63 | Dec 37)', lambda: xe('hun', 'Pluto', 'Neptune', 'sky Haumea -> H Pluto RA', 'sky Haumea -> J Neptune Dec'))
chk(2, 2, 'Catterick: sky Makemake on H Transpluto – J Sun (Dec 10 | RA 435/9)', lambda: xe('cat', 'Transpluto', 'Sun', 'sky Makemake -> H Transpluto Dec 10.00323 (10)', 'sky Makemake -> J Sun RA 48.33347 (435/9)'))
chk(2, 2, 'Lingfield: sky Orcus on H Jupiter – J Venus; sky Saturn on H Haumea – J Pallas', lambda: xb('lin', 'Jupiter', 'Venus', 'Orcus') and xb('lin', 'Haumea', 'Pallas', 'Saturn'))
chk(2, 2, 'Haydock 17:18: sky Venus on H Juno – J Venus (near band); sky Ceres on H Makemake – J Haumea (Dec 2 | Dec 2)', lambda: xb('hy18', 'Juno', 'Venus', 'Venus', level='near') and xe('hy18', 'Makemake', 'Haumea', 'sky Ceres -> H Makemake Dec', 'sky Ceres -> J Haumea Dec'))
chk(2, 2, 'Newmarket July: H Uranus – J Venus by sky Venus GC 123 | sky Pluto Dec 38', lambda: xe('nmj', 'Uranus', 'Venus', 'sky Venus -> H Uranus GC 122.99504 (123)', 'sky Pluto -> J Venus Dec 38.00131 (38)'))
chk(2, 2, 'Exeter: H Juno – J Chiron Dec 0.0555 by sky Gonggong GC 153 | sky Uranus GC 74', lambda: xe('exe', 'Juno', 'Chiron', 'sky Gonggong -> H Juno GC', 'sky Uranus -> J Chiron GC'))
chk(2, 2, 'DIFFERENCE: Exeter "winner tightest strict both-ends cross link" is Layer 4\'s strict shape; by the reader (all strikes, by the link) Pens Man H Sedna – J Rahu Dec 0.0034 (sky Vesta Dec 20 | Dec 20) is tighter; winner\'s Dec 0.0555 is tighter than Pens Man\'s other one',
    lambda: min((x['link_t'], P) for P, r in F('exe')['per_runner'].items() for x in r['instances'] if x['item'] in (1, 2) and x['level'] == 'strict' and x['nf_t'] is not None)[1] == P_of('exe', 'Pens Man')
            and has('exe', 2, 'H Sedna – J Rahu RA 107.3741 Dec 0.0034', P=P_of('exe', 'Pens Man')))
chk(2, 2, 'Exeter field: Pens Man shares the shape', lambda: P_of('exe', 'Pens Man') in who('exe', 2) or P_of('exe', 'Pens Man') in who('exe', 1))
chk(2, 2, 'York 16:15: H Quaoar – J Sun Dec 0.305 (near) by sky Pluto (RA 29.9984 | Dec 62/9)', lambda: xe('y15', 'Quaoar', 'Sun', 'sky Pluto -> H Quaoar RA 29.99837 (30)', 'sky Pluto -> J Sun Dec 6.88901 (62/9)', level='near'))
# 3 partner strike
chk(2, 3, 'Newmarket July: sky Venus -> H Uranus GC 123 on H Uranus – J Venus', lambda: any(xl(x, 'Uranus', 'Venus') and 'partner sky Venus -> H Uranus GC' in x['what'] for x in find('nmj', 3)))
chk(2, 3, 'Newmarket July: sky Neptune -> J Saturn Dec 25/9 on H Neptune – J Saturn', lambda: any(xl(x, 'Neptune', 'Saturn') and 'partner sky Neptune -> J Saturn Dec' in x['what'] and '(25/9)' in x['what'] for x in find('nmj', 3, level=None)))
chk(2, 3, 'Newmarket July field: NOT unique (winner 2, Arabian Poet 2, Vecu 2, Big Gypsy King 2)', lambda: {P_of('nmj', h) for h in ('Arabian Poet', 'Vecu', 'Big Gypsy King')} | {'P01'} <= set(who('nmj', 3)))
chk(2, 3, 'Redcar: H Ceres – J Jupiter Dec 0.1131, sky Jupiter -> H Ceres GC 71.11139 (640/9)', lambda: any(xl(x, 'Ceres', 'Jupiter') and 'sky Jupiter -> H Ceres GC 71.11139 (640/9)' in x['what'] for x in find('red', 3)))
chk(2, 3, 'Redcar field: ONLY partner strike in the field (strict)', lambda: only('red', 3))
chk(2, 3, 'EXPLAINED: Haydock 14:20 H Ceres – J Transpluto RA 0.189 partner strike — sky Transpluto -> H Ceres Flat 26.0062 is outside +-0.005; the reader finds the other direction, sky Ceres -> J Transpluto GC 602/9',
    lambda: any(xl(x, 'Ceres', 'Transpluto') and 'partner sky Ceres -> J Transpluto GC 66.88864 (602/9)' in x['what'] for x in find('hy20', 3)) and not any('sky Transpluto -> H Ceres' in x['what'] for x in find('hy20', 3, level=None)))
chk(2, 3, 'Haydock 17:18: sky Venus -> H Juno RA 671/9 on H Juno – J Venus (near band)', lambda: any(xl(x, 'Juno', 'Venus') and 'sky Venus -> H Juno RA' in x['what'] and '(671/9)' in x['what'] for x in find('hy18', 3, level='near')))
# 5 both ends moved
chk(2, 5, 'Wolverhampton: H Eris – J Jupiter RA 1.1336; H Eris moved RA 8/9; J Jupiter moved GC 122/9', lambda: any(xl(x, 'Eris', 'Jupiter') and 'H Eris moved RA 0.88' in ' '.join(x['moves']) and 'J Jupiter moved GC 13.55' in ' '.join(x['moves']) for x in find('wol', 5)))
chk(2, 5, 'Wolverhampton field: ONLY runner (strict)', lambda: only('wol', 5))
chk(2, 5, 'York 16:15: H Venus moved Dec 40 | J Uranus moved GC 135 on H Venus – J Uranus', lambda: any(xl(x, 'Venus', 'Uranus') and '(40)' in ' '.join(x['moves']) and '(135)' in ' '.join(x['moves']) for x in find('y15', 5)))
chk(2, 5, 'York 16:15 field: NOT unique — Fire Demon, Expensive Queen, Misemerald too', lambda: {P_of('y15', h) for h in ('Fire Demon', 'Expensive Queen', 'Misemerald')} <= set(who('y15', 5)))
chk(2, 5, 'Exeter: H Ketu – J Ceres (Dec 0.280), node moved RA 1163/9, J Ceres moved RA 124', lambda: any(xl(x, 'Ketu', 'Ceres') and '(1163/9)' in ' '.join(x['moves']) and 'J Ceres moved RA 124.00' in ' '.join(x['moves']) for x in find('exe', 5)))
# 6 movement onto a cross link
M6 = [('aw30', 'H', 'Ceres', 'RA', '30', 'Ceres', 'Mars'), ('aw30', 'H', 'Pluto', 'RA', '16', None, None), ('aw16', 'J', 'Juno', 'Dec', '33/9', 'Pluto', 'Juno'),
      ('hy05', 'J', 'Quaoar', 'GC', '39', 'Gonggong', 'Quaoar'), ('lin', 'H', 'Orcus', 'RA', '9', 'Orcus', 'Vesta'), ('win', 'H', 'Mercury', 'Dec', '30', 'Mercury', 'Chiron'),
      ('nab', 'J', 'Jupiter', 'RA', '174', 'Makemake', 'Jupiter'), ('nab', 'J', 'Jupiter', 'RA', '174', 'Juno', 'Jupiter'), ('sed', 'H', 'Neptune', 'GC', '11', 'Neptune', 'Mercury'),
      ('nm35', 'J', 'Haumea', 'RA', '22', 'Makemake', 'Haumea'), ('nm35', 'J', 'Haumea', 'Dec', '53/9', 'Makemake', 'Haumea'), ('not30', 'H', 'Jupiter', 'Dec', '23', 'Jupiter', 'Uranus'),
      ('che', 'J', 'Neptune', 'Dec', '167/9', 'Ceres', 'Neptune'), ('che', 'J', 'Neptune', 'Dec', '167/9', 'Jupiter', 'Neptune'), ('che', 'J', 'Chiron', 'Dec', '5', 'Uranus', 'Chiron'),
      ('che', 'H', 'Pluto', 'GC', '51/9', 'Pluto', 'Sun'), ('asc', 'J', 'Chiron', 'RA', '40', 'Sedna', 'Chiron'), ('fon', 'H', 'Vesta', 'Dec', '57/9', 'Vesta', 'Sedna'),
      ('fon', 'J', 'Gonggong', 'Dec', '69/9', 'Gonggong', 'Juno'), ('fon', 'J', 'Neptune', 'GC', '564/9', 'Saturn', 'Neptune'), ('nc40', 'J', 'Ceres', 'Dec', '4', 'Haumea', 'Ceres'),
      ('nc40', 'H', 'Ceres', 'Dec', '6', 'Ceres', 'Chiron'), ('hy18', 'J', 'Eris', 'GC', '110/9', 'Gonggong', 'Eris'), ('per', 'H', 'Ceres', 'RA', '132', 'Ceres', 'Uranus'),
      ('per', 'H', 'Makemake', 'Dec', '30/9', 'Makemake', 'Haumea'), ('per', 'J', 'Neptune', 'GC', '508/9', 'Pluto', 'Neptune'), ('y45', 'H', 'Pluto', 'RA', '6', 'Pluto', 'Uranus'),
      ('y45', 'J', 'Pallas', 'RA', '92', 'Orcus', 'Pallas'), ('not50', 'H', 'Eris', 'RA', '12/9', 'Eris', 'Vesta'), ('y15', 'H', 'Quaoar', 'RA', '5', 'Quaoar', 'Mars'), ('y15', 'H', 'Quaoar', 'RA', '5', 'Quaoar', 'Rahu')]
for r, c, b, pl, n, h, j in M6:
    if h is None or (r, b) == ('fon', 'Gonggong'): continue
    chk(2, 6, f'{A[r]}: {c} {b} moved {pl} {n} onto H {h} – J {j}', (lambda r, c, b, pl, n, h, j: lambda: mv6(r, c, b, pl, n, h, j))(r, c, b, pl, n, h, j))
chk(2, 6, 'DIFFERENCE: Fontwell J Gonggong moved Dec 69/9 — the cross link is H Gonggong – J Juno, so J Gonggong is not an end (same body, other chart); not item 6 by its definition',
    lambda: not mv6('fon', 'J', 'Gonggong', 'Dec', '69/9', 'Gonggong', 'Juno') and any(m['chart'] == 'J' and m['body'] == 'Gonggong' and m['num'] == '69/9' for m in json.load(open(f"docs/classic/{A['fon']}/layer1/P05.json"))['movement']))
chk(2, 6, 'Haydock 17:18: J Venus moved Dec 11 onto H Juno – J Venus (near band)', lambda: mv6('hy18', 'J', 'Venus', 'Dec', '11', 'Juno', 'Venus', level='near'))
chk(2, 6, 'Wincanton field: winner\'s movement onto a cross link is the tightest', lambda: tightest('win', 6) == 'P07')
chk(2, 6, 'DIFFERENCE: Newmarket 15:35 field "two-plane movement onto a cross link only Eydon and Dawn Of Liberation" — reader also finds Austrian Theory H Gonggong (Flat + Dec)',
    lambda: sorted(P for P, x in F('nm35')['per_runner'].items() if any(len({i['what'].split(' moved ')[1].split(' ')[0] for i in x['instances'] if i['item'] == 6 and i['level'] == 'strict' and i['what'].startswith(b + ' moved ')}) >= 2
                                                                       for b in {i['what'].split(' moved ')[0] for i in x['instances'] if i['item'] == 6 and i['level'] == 'strict'})) == sorted(['P07', P_of('nm35', 'Dawn Of Liberation'), P_of('nm35', 'Austrian Theory')]))
# 7 swap
chk(2, 7, 'Fontwell: TWO swaps — Saturn/Neptune and Sedna/Vesta', lambda: has('fon', 7, ('swap Saturn/Neptune', 'swap Neptune/Saturn')) and has('fon', 7, ('swap Sedna/Vesta', 'swap Vesta/Sedna'), level=None))
chk(2, 7, 'Fontwell field: Vale Dolobo Dancer one (Rahu/Sun), others none', lambda: who('fon', 7) == sorted(['P05', P_of('fon', 'Vale Dolobo Dancer')]))
chk(2, 7, 'Sandown 2024: Ceres/Juno swap', lambda: has('s24', 7, ('swap Ceres/Juno', 'swap Juno/Ceres')))
chk(2, 7, 'Sandown 2024 field: ONLY swap', lambda: who('s24', 7) == ['P13'])
chk(2, 7, 'Newmarket July: no swap in winner; only Vecu (Juno–Quaoar)', lambda: who('nmj', 7) == [P_of('nmj', 'Vecu')])
chk(2, 7, 'York 15:45 and York 16:15: none in field', lambda: not who('y45', 7) and not who('y15', 7))
chk(2, 7, 'Exeter blind: Blaze A Trail field-only swap', lambda: who('exe', 7) == [P_of('exe', 'Blaze A Trail')])
# 9 / 10 pair in one chart struck on both ends
P9 = [('ffo', 'H', 'Mars', 'Orcus', 'Gonggong'), ('ffo', 'J', 'Mars', 'Transpluto', 'Pluto'), ('asc', 'H', 'Saturn', 'Transpluto', 'Quaoar'), ('car', 'H', 'Sun', 'Uranus', 'Vesta'),
      ('car', 'J', 'Pallas', 'Eris', 'Node'), ('fon', 'J', 'Jupiter', 'Gonggong', 'Chiron'), ('hy05', 'H', 'Saturn', 'Pluto', 'Node'), ('hy05', 'J', 'Venus', 'Pluto', 'Saturn'),
      ('hy05', 'H', 'Eris', 'Gonggong', 'Ceres'), ('hy05', 'J', 'Sedna', 'Orcus', 'Pallas'), ('hun', 'J', 'Pluto', 'Rahu', 'Juno'), ('lin', 'J', 'Juno', 'Transpluto', 'Mercury'),
      ('lin', 'J', 'Saturn', 'Pallas', 'Saturn'), ('nc40', 'J', 'Jupiter', 'Ceres', 'Sedna'), ('nm35', 'J', 'Sedna', 'Haumea', 'Haumea'), ('nm35', 'J', 'Uranus', 'Neptune', 'Vesta'),
      ('nab', 'J', 'Uranus', 'Vesta', 'Gonggong'), ('nab', 'H', 'Uranus', 'Sedna', 'Eris'), ('not30', 'J', 'Mars', 'Chiron', 'Juno'), ('not30', 'J', 'Chiron', 'Pallas', 'Makemake'),
      ('not50', 'H', 'Jupiter', 'Pluto', 'Vesta'), ('not50', 'J', 'Pallas', 'Orcus', 'Node'), ('not50', 'H', 'Saturn', 'Uranus', 'Node'), ('not50', 'H', 'Saturn', 'Haumea', 'Node'),
      ('not50', 'H', 'Uranus', 'Pallas', 'Node'), ('s21', 'J', 'Mars', 'Sun', 'Ceres'), ('s24', 'H', 'Juno', 'Orcus', 'Node'), ('win', 'J', 'Ceres', 'Haumea', 'Ceres'),
      ('wol', 'H', 'Neptune', 'Gonggong', 'Sedna'), ('wol', 'H', 'Eris', 'Sedna', 'Transpluto'), ('y45', 'H', 'Pluto', 'Juno', 'Pluto'), ('y45', 'J', 'Mercury', 'Eris', 'Sun'),
      ('aw20', 'J', 'Neptune', 'Rahu', 'Neptune')]
for r, c, a, b, k in P9[:-1]:
    chk(2, 9, f'{A[r]}: {c} {a}–{b} struck on both ends by sky {k}', (lambda r, c, a, b, k: lambda: p9(r, c, a, b, k))(r, c, a, b, k))
chk(2, 10, 'Sandown 2024: J Mars–Jupiter Dec 50 by THREE (Sun, Uranus, Eris)', lambda: any(x['what'].startswith('J Mars–Jupiter ') and all(f' {k}: ' in x['what'].replace('— ', ' ').replace('; ', ' ') for k in ('Sun', 'Uranus', 'Eris')) for x in find('s24', 10)))
chk(2, 10, 'Ffos Las: J Jupiter–Vesta Dec 5 by Ceres and Haumea', lambda: any(x['what'].startswith('J Jupiter–Vesta ') and 'Ceres:' in x['what'] and 'Haumea:' in x['what'] for x in find('ffo', 10)))
chk(2, 10, 'Newcastle AW 13:30: J Gonggong–Transpluto RA 175 by Chiron and Quaoar', lambda: any(x['what'].startswith('J Gonggong–Transpluto ') and 'Chiron:' in x['what'] and 'Quaoar:' in x['what'] for x in find('aw30', 10)))
chk(2, 10, 'York 15:45: H Jupiter–Pluto RA 28 by Pluto and Quaoar', lambda: any(x['what'].startswith('H Jupiter–Pluto ') and 'Pluto:' in x['what'] and 'Quaoar:' in x['what'] for x in find('y45', 10)))
chk(2, 10, 'Haydock 14:20: H Saturn–Pallas by Venus and Pallas; Contact has the shape too', lambda: any(x['what'].startswith('H Saturn–Pallas ') and 'Venus:' in x['what'] and 'Pallas:' in x['what'] for x in find('hy20', 10))
    and P_of('hy20', 'Contact') in who('hy20', 10))
# 11 same number / ratio in both charts
chk(2, 11, 'Nottingham 17:50: 34 — H Jupiter–Pluto RA 34 and J Pallas–Orcus RA 34', lambda: has('not50', 11, 'number 34: ', 'H Jupiter–Pluto RA', 'J Pallas–Orcus RA'))
chk(2, 11, 'Nottingham 17:50: 19/8 — J Saturn–Eris RA and H Uranus–Ceres RA', lambda: has('not50', 11, 'ratio 19/8: ', 'H Uranus–Ceres RA', 'J Saturn–Eris RA'))
chk(2, 11, 'Newmarket July: 21 — H Vesta Equator and J Venus–Pluto Dec (one number family)', lambda: has('nmj', 11, 'number 21: ', 'H Vesta Equator', 'J Venus–Pluto Dec'))
chk(2, 11, 'Redcar: 19 — J Gonggong Equator = H Venus–Gonggong Dec', lambda: has('red', 11, 'number 19: ', 'H Venus–Gonggong Dec', 'J Gonggong Equator'))
chk(2, 11, 'EXPLAINED: Redcar "shared with Oheka" — Oheka\'s same number is 66 in different planes (H GC / J Flat), so it is listed as other plane (answer C)', lambda: has('red', 11, 'number 66: ', P=P_of('red', 'Oheka'), level='other') and not has('red', 11, P=P_of('red', 'Oheka')))
chk(2, 11, 'York 16:15 loser Blue Prince: 19 — H Saturn Equator and J Saturn Equator', lambda: has('y15', 11, 'number 19: ', 'H Saturn Equator', 'J Saturn Equator', P=P_of('y15', 'Blue Prince')))
# 14 shared pair also cross-linked
chk(2, 14, 'Exeter: Chiron–Juno shared GC + cross H Juno – J Chiron', lambda: has('exe', 14, pr('Chiron–Juno'), 'cross H Juno – J Chiron'))
chk(2, 14, 'Exeter field: winner and Caspers Court (Saturn–Ceres)', lambda: who('exe', 14) == sorted(['P11', P_of('exe', 'Caspers Court')]) and has('exe', 14, pr('Saturn–Ceres'), P=P_of('exe', 'Caspers Court')))
chk(2, 14, 'Ffos Las: Jupiter–Vesta shared GC + H Vesta – J Jupiter RA 0.1901', lambda: has('ffo', 14, pr('Jupiter–Vesta'), 'cross H Vesta – J Jupiter RA 0.1901'))
# 18 same-body set joined
chk(2, 18, 'York 16:15: Chiron GC set and node Dec set joined', lambda: has('y15', 18, 'same-body Chiron GC') and has('y15', 18, ('same-body Rahu Dec', 'same-body Ketu Dec')))
chk(2, 18, 'Newmarket July: Uranus set joined (Uranus a cross-link end)', lambda: has('nmj', 18, 'same-body Uranus', 'cross H Uranus – J Venus'))
chk(2, 18, 'Exeter: Chiron set joined; Fontwell Juno and Venus sets; Perth Uranus; Nottingham 17:50 Vesta', lambda: has('exe', 18, 'same-body Chiron Dec') and has('fon', 18, 'same-body Juno Dec')
    and has('fon', 18, 'same-body Venus Dec') and has('per', 18, 'same-body Uranus') and has('not50', 18, 'same-body Vesta'))
# 23 one body in ratios in both charts
chk(2, 23, 'Sandown 2021: Mercury 3 + 3', lambda: has('s21', 23, 'Mercury: H 3 (', '| J 3 ('))
chk(2, 23, 'Huntingdon: Juno and Gonggong in both charts', lambda: has('hun', 23, 'Juno: ') and has('hun', 23, 'Gonggong: '))
chk(2, 23, 'Newcastle AW 13:30: Juno 5 hits in both charts (0.01%)', lambda: has('aw30', 23, 'Juno: H ', level=None) and sum(int(x['what'].split('H ')[1].split(' ')[0]) + int(x['what'].split('| J ')[1].split(' ')[0]) for x in find('aw30', 23, 'Juno: ', level=None)) >= 5)
chk(2, 23, 'Newbury: Transpluto; Newmarket July: Chiron and Vesta; York 16:15: Transpluto and Chiron; Exeter: Juno', lambda: has('nby', 23, 'Transpluto: ') and has('nmj', 23, 'Chiron: ')
    and has('nmj', 23, 'Vesta: ') and has('y15', 23, 'Transpluto: ') and has('y15', 23, 'Chiron: '))
chk(2, 23, 'EXPLAINED: Exeter Juno is in Best\'s ratios only (the horse end is the cross link, not a horse ratio) — not item 23 by its definition', lambda: not has('exe', 23, 'Juno: ', level=None))
# 25 Equator whole/ninth + chains
chk(2, 25, 'York 16:15: H Rahu 23 with chains sky Sun – H Ketu Dec 42 and H Ketu – J Pallas Dec 9', lambda: has('y15', 25, 'H Rahu |Dec| 23.00196 = 23', 'S Sun–H Ketu Dec 42', 'H Ketu–J Pallas Dec 9'))
chk(2, 25, 'York 16:15: J Pallas 14 (off 0.0069) with chain sky Sun – J Pallas Dec 33 = 19 + 14', lambda: has('y15', 25, 'J Pallas |Dec| 14.00695 = 14', 'S Sun–J Pallas Dec 33 from S Sun–EQ 19 & J Pallas–EQ 14'))
chk(2, 25, 'York 16:15 field count does NOT separate: winner 2, Blue Prince 2, Ribble Radiant 3', lambda: [len(find('y15', 25, P=P_of('y15', h))) for h in ('Diligent Resdev', 'Blue Prince', 'Ribble Radiant')] == [2, 2, 3])
chk(2, 25, 'Newmarket July: H Sun 12, H Vesta 21', lambda: has('nmj', 25, 'H Sun |Dec|', '= 12 ') and has('nmj', 25, 'H Vesta |Dec|', '= 21 '))
E25 = [('nby', 'H Sun', '15'), ('hy05', 'H Haumea', '19'), ('hy05', 'H Chiron', '44/9'), ('nc40', 'H Chiron', '2'), ('nm35', 'J Neptune', '19'), ('nab', 'J Orcus', '2'),
       ('s24', 'J Transpluto', '13'), ('sed', 'J Jupiter', '15'), ('sed', 'H Pluto', '191/9'), ('sed', 'J Rahu', '178/9'), ('exe', 'J Neptune', '22'), ('red', 'J Uranus', '22'), ('red', 'J Gonggong', '19')]
for r, b, n in E25: chk(2, 25, f'{A[r]}: {b} Equator {n}', (lambda r, b, n: lambda: has(r, 25, f'{b} |Dec|', f'= {n} '))(r, b, n))
chk(2, 25, 'Newcastle AW 12:20: no whole/ninth Equator values in the natal charts', lambda: not has('aw20', 25))
# 28 one sky body on one natal body in RA and Dec
chk(2, 28, 'Newcastle AW 12:20: sky Gonggong -> J Uranus RA 94, Dec 83/9', lambda: has('aw20', 28, 'sky Gonggong -> J Uranus RA', '(94) and Dec', '(83/9)'))
chk(2, 28, 'Nottingham 15:30: sky Jupiter -> J Vesta RA 18, Dec 137/9', lambda: has('not30', 28, 'sky Jupiter -> J Vesta RA', '(18) and Dec', '(137/9)'))
chk(2, 28, 'Perth: sky Juno -> J Haumea RA 1219/9, Dec 26', lambda: has('per', 28, 'sky Juno -> J Haumea RA', '(1219/9) and Dec', '(26)'))
chk(2, 28, 'York 15:45: sky Sun -> J Mercury RA 136, Dec 25', lambda: has('y45', 28, 'sky Sun -> J Mercury RA', '(136) and Dec', '(25)'))
chk(2, 28, 'Haydock 14:20: winner none, three beaten runners one each', lambda: not has('hy20', 28) and len(who('hy20', 28)) == 3 and all(len(find('hy20', 28, P=P)) == 1 for P in who('hy20', 28)))
# 29 pair in one chart whole/ninth in RA and Dec
chk(2, 29, 'Sandown 2021: J Mars–Sun RA 118, Dec 92/9', lambda: has('s21', 29, ('J Mars–Sun', 'J Sun–Mars'), '= 118, Dec', '= 92/9'))
chk(2, 29, 'Fontwell: J Pluto–Quaoar RA 6/9, Dec 7', lambda: has('fon', 29, ('J Pluto–Quaoar', 'J Quaoar–Pluto'), '= 6/9, Dec', '= 7'))
chk(2, 29, 'Wincanton: J Pallas–Rahu RA 380/9, Dec 3', lambda: has('win', 29, ('J Pallas–Rahu', 'J Rahu–Pallas'), '= 380/9, Dec', '= 3'))
chk(2, 29, 'Perth: H Pallas–Uranus RA 951/9, Dec 112/9', lambda: has('per', 29, ('H Pallas–Uranus', 'H Uranus–Pallas'), '= 951/9, Dec', '= 112/9'))
# 30 tightest cross link
chk(2, 30, 'Catterick: H Sun – J Vesta Dec 0.00010 — tightest cross link in the race', lambda: has('cat', 30, 'H Sun – J Vesta') and tightest('cat', 30) == 'P07')
chk(2, 30, 'Newton Abbot: H Sedna – J Chiron Dec 0.0147 — tightest in the race', lambda: has('nab', 30, 'H Sedna – J Chiron') and tightest('nab', 30) == 'P07')
chk(2, 30, 'Newmarket July: H Uranus – J Venus Dec 0.060 — tightest Venus–Uranus link in field', lambda: min((min(x['RA'] / 1.5, x['Dec'] / 0.3), P) for P in F('nmj')['per_runner']
    for x in json.load(open(f"docs/classic/{A['nmj']}/layer1/{P}.json"))['links'] if x['kind'] == 'cross' and {x['a'][2:], x['b'][2:]} == {'Venus', 'Uranus'})[1] == 'P01')

# ============================================================== run
if __name__ == '__main__':
    ok = bad = nd = 0
    for st, item, label, fn in C:
        if st > STEP or (ONLY and item != ONLY): continue
        try: res = fn()
        except Exception as e: res = False; label += f'  [{type(e).__name__}: {e}]'
        print(f"  {('diff' if label.startswith(('DIFFERENCE', 'EXPLAINED')) else 'ok  ') if res else 'FAIL'} [{item:2d}] {label}")
        ok += bool(res); bad += not res; nd += bool(res) and label.startswith(('DIFFERENCE', 'EXPLAINED'))
    print(f'{ok}/{ok + bad}  (of which {nd} DIFFERENCE / EXPLAINED checks: the reader follows the definition, the hand read differed — for Eddie)')
    sys.exit(1 if bad else 0)
