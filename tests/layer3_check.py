#!/usr/bin/env python3
"""layer3_check.py — every shape and hub named by hand in a winner read must be found by Layer 3 in that winner."""
import json, sys
def L(race, P): return json.load(open(f'docs/classic/{race}/layer3/{P}.json'))
def has(R, n, ends=None, pred=lambda s: True):
    for s in R['shapes']:
        if s['shape'] != n: continue
        if ends and not set(ends) <= set(s['bodies']): continue
        if pred(s): return True
    return False
def hub(R, b): return b in R['hubs']
C = [
 ('york_1615_20240515','P25','3 pair together in sky: H Venus – J Uranus', lambda R: has(R,3,['H Venus','J Uranus'])),
 ('york_1615_20240515','P25','4 both ends moved: H Venus – J Uranus', lambda R: has(R,4,['H Venus','J Uranus'])),
 ('york_1615_20240515','P25','11 joined same-body set: Chiron', lambda R: has(R,11,['H Chiron'])),
 ('york_1615_20240515','P25','11 joined same-body set: node', lambda R: has(R,11,pred=lambda s: any('Rahu' in b or 'Ketu' in b for b in s['bodies']))),
 ('york_1615_20240515','P25','hub H Venus', lambda R: hub(R,'H Venus')),
 ('york_1615_20240515','P25','hub J Uranus', lambda R: hub(R,'J Uranus')),
 ('newmarket_july_1745_20240816','P01','1 cross link struck both ends: H Uranus – J Venus', lambda R: has(R,1,['H Uranus','J Venus'])),
 ('newmarket_july_1745_20240816','P01','2 partner strike: H Uranus – J Venus', lambda R: has(R,2,['H Uranus','J Venus'])),
 ('newmarket_july_1745_20240816','P01','8 same number 21 in both charts', lambda R: has(R,8,pred=lambda s: s.get('number')=='21')),
 ('newmarket_july_1745_20240816','P01','hub H Uranus (strong)', lambda R: 'H Uranus' in R['strong_hubs']),
 ('newmarket_july_1745_20240816','P01','hub J Chiron', lambda R: hub(R,'J Chiron')),
 ('newmarket_july_1745_20240816','P01','hub H Chiron', lambda R: hub(R,'H Chiron')),
 ('perth_1610_20220420','P09','1 H Ceres – J Uranus struck on both ends by 2+ sky bodies (Ceres, Rahu/Ketu)', lambda R: has(R,1,['H Ceres','J Uranus'],lambda s: s['multi'] and 'Ceres' in s['same_sky_both_ends'])),
 ('perth_1610_20220420','P09','hub J Node (Bowen)', lambda R: hub(R,'J Node')),
 ('nottingham_1530_20220601','P01','1 H Sedna – J Chiron struck both ends by Venus, Ceres, Juno', lambda R: has(R,1,['H Sedna','J Chiron'],lambda s: {'Venus','Ceres','Juno'} <= set(s['same_sky_both_ends']))),
 ('nottingham_1530_20220601','P01','hub J Chiron (Dawson)', lambda R: hub(R,'J Chiron')),
 ('wolverhampton_aw_1725_20231021','P05','4 both ends moved: H Eris – J Jupiter', lambda R: has(R,4,['H Eris','J Jupiter'])),
 ('fontwell_1530_20231006','P05','6 swap Saturn/Neptune', lambda R: has(R,6,pred=lambda s: s['pair'] in ('Neptune/Saturn','Saturn/Neptune'))),
 ('fontwell_1530_20231006','P05','6 swap Sedna/Vesta', lambda R: has(R,6,pred=lambda s: s['pair'] in ('Sedna/Vesta','Vesta/Sedna'))),
 ('sandown_1430_20240215','P13','6 swap Ceres/Juno', lambda R: has(R,6,pred=lambda s: s['pair'] in ('Ceres/Juno','Juno/Ceres'))),
 ('sandown_1430_20240215','P13','12 Brace Mars–Jupiter struck both ends by Sun, Uranus, Eris', lambda R: has(R,12,['J Mars','J Jupiter'],lambda s: {'Sun','Uranus','Eris'} <= set(s['sky']))),
 ('ascot_1350_20231021','P01','7 triangle H Ceres/Sedna/Haumea struck by sky Vesta', lambda R: has(R,7,['H Ceres','H Sedna','H Haumea'],lambda s: s['sky']=='Vesta')),
 ('nottingham_1750_20220613','P03','8 same number 34 in both charts', lambda R: has(R,8,pred=lambda s: s.get('number')=='34')),
 ('nottingham_1750_20220613','P03','8 same ratio 19/8 in both charts', lambda R: has(R,8,pred=lambda s: s.get('ratio')=='19/8')),
 ('newcastle_aw_1330_20220102','P09','9 shared node (Venturous)', lambda R: has(R,9)),
 ('haydock_1405_20220219','P09','9 shared node (Wholestone)', lambda R: has(R,9)),
 ('dettori_ascot_19960928','P01','10 sky Sun divides Dettori Sun–Chiron', lambda R: has(R,10,['J Sun','J Chiron'])),
 ('newcastle_aw_1330_20220102','P09','5 movement onto a cross link: horse Ceres (on Beasley Mars)', lambda R: has(R,5,['H Ceres'])),
]
import glob
def only_winner(race, P, pred):
    hits = [f[-8:-5] for f in sorted(glob.glob(f'docs/classic/{race}/layer3/P*.json')) if any(pred(x) for x in json.load(open(f))['shapes'])]
    return hits == [P]
C += [
 ('perth_1610_20220420','P09','field: only runner with a strict cross link struck on both ends by 2+ sky bodies', lambda R: only_winner('perth_1610_20220420','P09',lambda s: s['shape']==1 and s['strict_multi'])),
 ('nottingham_1530_20220601','P01','field: only runner with a strict cross link struck on both ends by 2+ sky bodies', lambda R: only_winner('nottingham_1530_20220601','P01',lambda s: s['shape']==1 and s['strict_multi'])),
 ('wolverhampton_aw_1725_20231021','P05','field: only runner with strict both ends moved', lambda R: only_winner('wolverhampton_aw_1725_20231021','P05',lambda s: s['shape']==4 and s['strict'])),
 ('sandown_1430_20240215','P13','field: only runner with a swap', lambda R: only_winner('sandown_1430_20240215','P13',lambda s: s['shape']==6)),
]
fails = 0
for race, P, name, f in C:
    ok = f(L(race, P)); fails += not ok
    print(('  ok   ' if ok else '  MISS ') + f'{race} {P}: {name}')
print(f'{len(C) - fails}/{len(C)}'); sys.exit(1 if fails else 0)
