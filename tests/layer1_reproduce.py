#!/usr/bin/env python3
"""layer1_reproduce.py RACE — check Layer 1 output contains every item found by hand in that race's winner read.
Expected items per race are listed below (from docs/classic/<race>/winner_read.md, after checker corrections)."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from l1helpers import *
Y='york_1615_20240515'
EXP = {
 'dettori_ascot_19960928': ('P01', [
  ('Dettori: sky Sun moved Dec 21 from J Sun', lambda I: move(I,'J','Sun','Dec','21')),
  ('Dettori: sky Sun splits J Sun–Chiron Dec 28.014 = 21 + 7.014 (span/other 4)', lambda I: any(x['moved']=='J Sun' and x['to']=='J Chiron' and x['plane']=='Dec' and x['move_num']=='21' and x['span_ratio'][0]=='4' for x in I['splits'])),
  ('Diffident: H Sun–Chiron Dec sky/natal 11/2', lambda I: ratio(I,'H','Sun–Chiron','Dec','11/2')),
 ]),
 'newmarket_july_1745_20240816': ('P01', [
  ('cross link H Uranus–J Venus Dec 0.060', lambda I: any(l['kind']=='cross' and l['a']=='H Uranus' and l['b']=='J Venus' and abs(l['Dec']-0.060)<0.001 for l in I['links'])),
  ('sky Venus -> H Uranus GC 123', lambda I: any(s['sky']=='Venus' and s['target']=='H Uranus' and s['plane']=='GC' and s['num']=='123' for s in I['strikes'])),
  ('sky Pluto -> J Venus Dec 38', lambda I: any(s['sky']=='Pluto' and s['target']=='J Venus' and s['plane']=='Dec' and s['num']=='38' for s in I['strikes'])),
  ('sky Neptune -> J Saturn Dec 25/9', lambda I: any(s['sky']=='Neptune' and s['target']=='J Saturn' and s['plane']=='Dec' and s['num']=='25/9' for s in I['strikes'])),
  ('J Venus–Pluto Dec 21', lambda I: any(l['kind']=='J' and l['a']=='J Venus' and l['b']=='J Pluto' and l['nums'].get('Dec',{}).get('num')=='21' for l in I['links'])),
  ('J Pluto moved Dec 17', lambda I: any(m['chart']=='J' and m['body']=='Pluto' and m['plane']=='Dec' and m['num']=='17' for m in I['movement'])),
  ('H Sedna moved GC 26/9', lambda I: any(m['chart']=='H' and m['body']=='Sedna' and m['plane']=='GC' and m['num']=='26/9' for m in I['movement'])),
  ('H Pluto–Rahu RA 9/5', lambda I: any(r['chart']=='H' and r['pair']=='Pluto–Rahu' and r['plane']=='RA' and r['ratio']=='9/5' for r in I['ratios'])),
  ('Uranus same-body RA 6:7:7/6', lambda I: any(s['body']=='Uranus' and s['plane']=='RA' and sorted(s['ratios'])==sorted(['6','7','7/6']) for s in I['same_body'])),
  ('Equator H/J Uranus 7/5', lambda I: any(e['body']=='Uranus' and e['pair']=='H/J' and e['ratio']=='7/5' for e in I['eq_ratios'])),
  ('Equator H/J Ceres 7/6', lambda I: any(e['body']=='Ceres' and e['pair']=='H/J' and e['ratio']=='7/6' for e in I['eq_ratios'])),
  ('shared Uranus–Ketu Dec', lambda I: any(s['pair']=='Uranus–Ketu' and s['plane']=='Dec' for s in I['shared'])),
  ('Chiron same-body Dec 5/4:9/4:9/5', lambda I: any(s['body']=='Chiron' and s['plane']=='Dec' and sorted(s['ratios'])==sorted(['5/4','9/4','9/5']) for s in I['same_body'])),
  ('H Jupiter–Chiron Dec 7/6', lambda I: any(r['chart']=='H' and r['pair']=='Jupiter–Chiron' and r['plane']=='Dec' and r['ratio']=='7/6' for r in I['ratios'])),
  ('J Mercury–Chiron Dec 28/3', lambda I: any(r['chart']=='J' and r['pair']=='Mercury–Chiron' and r['plane']=='Dec' and r['ratio']=='28/3' for r in I['ratios'])),
  ('shared Chiron–Rahu Dec', lambda I: any(s['pair']=='Chiron–Rahu' and s['plane']=='Dec' for s in I['shared'])),
  ('shared Chiron–Ketu Flat', lambda I: any(s['pair']=='Chiron–Ketu' and s['plane']=='Flat' for s in I['shared'])),
  ('H Sun Equator 12', lambda I: any(p['chart']=='H' and p['body']=='Sun' and p['eq_num']=='12' for p in I['points'])),
  ('H Vesta Equator 21', lambda I: any(p['chart']=='H' and p['body']=='Vesta' and p['eq_num']=='21' for p in I['points'])),
  ('H Vesta–Orcus Dec 16/5', lambda I: any(r['chart']=='H' and r['pair']=='Vesta–Orcus' and r['plane']=='Dec' and r['ratio']=='16/5' for r in I['ratios'])),
  ('J Vesta–Gonggong RA 6/5', lambda I: any(r['chart']=='J' and r['pair']=='Vesta–Gonggong' and r['plane']=='RA' and r['ratio']=='6/5' for r in I['ratios'])),
  ('H Sun–Quaoar Flat 5/2', lambda I: any(r['chart']=='H' and r['pair']=='Sun–Quaoar' and r['plane']=='Flat' and r['ratio']=='5/2' for r in I['ratios'])),
  ('H Saturn–Haumea RA 9/7', lambda I: any(r['chart']=='H' and r['pair']=='Saturn–Haumea' and r['plane']=='RA' and r['ratio']=='9/7' for r in I['ratios'])),
  ('J Juno–Makemake Flat 22/5', lambda I: any(r['chart']=='J' and r['pair']=='Juno–Makemake' and r['plane']=='Flat' and r['ratio']=='22/5' for r in I['ratios'])),
  ('J Sedna–Gonggong RA 8/7', lambda I: any(r['chart']=='J' and r['pair']=='Sedna–Gonggong' and r['plane']=='RA' and r['ratio']=='8/7' for r in I['ratios'])),
  ('cross link H Makemake–J Haumea', lambda I: any(l['kind']=='cross' and l['a']=='H Makemake' and l['b']=='J Haumea' and l['close'] for l in I['links'])),
  ('H Mercury–Pluto Dec 3', lambda I: any(l['kind']=='H' and l['a']=='H Mercury' and l['b']=='H Pluto' and l['nums'].get('Dec',{}).get('num')=='3' for l in I['links'])),
  ('Equator S/J Pallas 27/2 near', lambda I: eqr(I,'Pallas','S/J','27/2','near')),
  ('Equator H/J Juno 17/8 near', lambda I: eqr(I,'Juno','H/J','17/8','near')),
  ('Equator H/J Uranus 7/5 tight', lambda I: eqr(I,'Uranus','H/J','7/5','tight')),
 ]),
 Y: ('P25', [
  ('1 cross H Venus–J Uranus (close)', lambda I: link(I,'cross','H Venus','J Uranus',close=True)),
  ('3 H Venus moved Dec 40', lambda I: move(I,'H','Venus','Dec','40')),
  ('3 J Uranus moved GC 135', lambda I: move(I,'J','Uranus','GC','135')),
  ('4 H Venus–Saturn GC 12/5', lambda I: ratio(I,'H','Venus–Saturn','GC','12/5')),
  ('4 J Uranus–Pluto GC 15/7', lambda I: ratio(I,'J','Uranus–Pluto','GC','15/7')),
  ('5 H Mercury–Saturn GC 19/3', lambda I: ratio(I,'H','Mercury–Saturn','GC','19/3')),
  ('5 J Venus–Saturn close', lambda I: link(I,'J','J Venus','J Saturn',close=True)),
  ('6 H Mercury–Saturn close', lambda I: link(I,'H','H Mercury','H Saturn',close=True)),
  ('6 J Mercury–Saturn close', lambda I: link(I,'J','J Mercury','J Saturn',close=True)),
  ('6 H Mars–Uranus close', lambda I: link(I,'H','H Mars','H Uranus',close=True)),
  ('6 J Mars–Uranus close', lambda I: link(I,'J','J Mars','J Uranus',close=True)),
  ('7 sky Neptune–Uranus RA 51', lambda I: sky(Y,'Uranus–Neptune','RA','51')),
  ('8 H Chiron–Transpluto Dec 11/2', lambda I: ratio(I,'H','Chiron–Transpluto','Dec','11/2')),
  ('9 J Makemake–Transpluto RA 7/4', lambda I: ratio(I,'J','Makemake–Transpluto','RA','7/4')),
  ('10 H Chiron–Quaoar GC 9/8', lambda I: ratio(I,'H','Chiron–Quaoar','GC','9/8')),
  ('10 J Chiron–Vesta GC 3/2', lambda I: ratio(I,'J','Chiron–Vesta','GC','3/2')),
  ('11 H Quaoar moved RA 5', lambda I: move(I,'H','Quaoar','RA','5')),
  ('11 cross H Quaoar–J Mars', lambda I: link(I,'cross','H Quaoar','J Mars',close=True)),
  ('11 cross H Quaoar–J Rahu', lambda I: link(I,'cross','H Quaoar','J Rahu',close=True)),
  ('11 J Rahu–Sedna Dec 27/4', lambda I: ratio(I,'J','Rahu–Sedna','Dec','27/4')),
  ('11 sky Pluto -> H Quaoar RA 30', lambda I: strike(I,'Pluto','H Quaoar','RA','30')),
  ('11 sky Pluto -> J Sun Dec 62/9', lambda I: strike(I,'Pluto','J Sun','Dec','62/9')),
  ('12 shared Eris–Haumea Flat', lambda I: shared(I,'Eris–Haumea','Flat')),
  ('12 pair set Eris–Orcus GC', lambda I: pset(I,'Eris–Orcus','GC')),
  ('13 cross H Makemake–J Haumea', lambda I: link(I,'cross','H Makemake','J Haumea',close=True)),
  ('14 H Rahu Equator 23', lambda I: eqpt(I,'H','Rahu','23')),
  ('14 sky Sun Equator 19', lambda I: eqpt(I,'S','Sun','19')),
  ('17 node same-body Dec 9/4:5/4:9/5', lambda I: same(I,'Rahu','Dec',['9/4','5/4','9/5'])),
  ('17 Chiron same-body GC 6:5:6/5', lambda I: same(I,'Chiron','GC',['6','5','6/5'])),
  ('17 Quaoar Flat set NOT listed (p > 30)', lambda I: not any(s['body']=='Quaoar' and s['plane']=='Flat' for s in I['same_body'])),
  ('19 H Mercury–Transpluto Dec 30', lambda I: link(I,'H','H Mercury','H Transpluto','Dec','30')),
  ('20 sky Uranus–Pluto Dec 41', lambda I: sky(Y,'Uranus–Pluto','Dec','41')),
  ('20 sky Chiron–Sedna RA 370/9', lambda I: sky(Y,'Chiron–Sedna','RA','370/9')),
  ('20 sky Venus–Rahu Dec 100/9', lambda I: sky(Y,'Venus–Rahu','Dec','100/9')),
  ('21 Equator S/H Mercury 7/3 tight', lambda I: eqr(I,'Mercury','S/H','7/3','tight')),
  ('22 J Pallas Equator 14', lambda I: eqpt(I,'J','Pallas','14')),
  ('22 sky Quaoar Equator 15', lambda I: eqpt(I,'S','Quaoar','15')),
  ('23 sky Sun -> H Ketu Dec 42', lambda I: strike(I,'Sun','H Ketu','Dec','42')),
  ('23 sky Sun -> J Pallas Dec 33', lambda I: strike(I,'Sun','J Pallas','Dec','33')),
  ('23 sky Sun – H Rahu Dec 4.00502: outside strike ±0.005 (not listed); both Equator roots 19 and 23 are listed for Layer 2',
   lambda I: not strike(I,'Sun','H Rahu','Dec','4') and eqpt(I,'S','Sun','19') and eqpt(I,'H','Rahu','23')),
  ('23 cross H Ketu–J Pallas Dec 9', lambda I: link(I,'cross','H Ketu','J Pallas','Dec','9')),
 ]),
}
import os, importlib.util, glob as _g
for _f in _g.glob(os.path.join(os.path.dirname(__file__), 'layer1_expect', '*.py')):
    _sp = importlib.util.spec_from_file_location('exp', _f); _m = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_m)
    EXP[_m.RACE] = (_m.P, _m.CHECKS)
race = sys.argv[1]; P, checks = EXP[race]
I = json.load(open(f'docs/classic/{race}/layer1/{P}.json'))
miss = 0
for name, f in checks:
    ok = f(I); miss += not ok
    print(('  ok   ' if ok else '  MISS ') + name)
print(f'{race} {P}: {len(checks) - miss}/{len(checks)} reproduced')
sys.exit(1 if miss else 0)
