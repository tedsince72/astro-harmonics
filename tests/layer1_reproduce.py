#!/usr/bin/env python3
"""layer1_reproduce.py RACE — check Layer 1 output contains every item found by hand in that race's winner read.
Expected items per race are listed below (from docs/classic/<race>/winner_read.md, after checker corrections)."""
import sys, json
EXP = {
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
 ]),
}
race = sys.argv[1]; P, checks = EXP[race]
I = json.load(open(f'docs/classic/{race}/layer1/{P}.json'))
miss = 0
for name, f in checks:
    ok = f(I); miss += not ok
    print(('  ok   ' if ok else '  MISS ') + name)
print(f'{race} {P}: {len(checks) - miss}/{len(checks)} reproduced')
sys.exit(1 if miss else 0)
