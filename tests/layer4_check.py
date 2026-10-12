#!/usr/bin/env python3
"""layer4_check.py — field results from the hand reads must come out of Layer 4."""
import json, sys
def F(r): return json.load(open(f'docs/classic/{r}/layer4/field.json'))
def who(r, lvl, k): return sorted(F(r)['table'][lvl].get(k, {}))
C = [
 ('Perth: only the winner (P09) has a strict cross link with 2+ sky bodies on both ends', lambda: who('perth_1610_20220420','strict','1m') == ['P09']),
 ('Nottingham 15:30: only the winner (P01) has a strict cross link with 2+ sky bodies on both ends', lambda: who('nottingham_1530_20220601','strict','1m') == ['P01']),
 ('Wolverhampton 2023: only the winner (P05) has both ends of a cross link moved (strict)', lambda: who('wolverhampton_aw_1725_20231021','strict','4') == ['P05']),
 ('Sandown 2024: only the winner (P13) has a swap', lambda: who('sandown_1430_20240215','broad','6') == ['P13']),
 ('Fontwell 2023: winner (P05) has two swaps, no other runner more than one', lambda: F('fontwell_1530_20231006')['table']['broad']['6'].get('P05') == 2 and all(c <= 1 for p, c in F('fontwell_1530_20231006')['table']['broad']['6'].items() if p != 'P05')),
 ('Venturous (newcastle_aw_1330 P09): only runner with a shared node', lambda: who('newcastle_aw_1330_20220102','broad','9') == ['P09']),
 ('Wholestone (haydock_1405 P09): only runner with a shared node', lambda: who('haydock_1405_20220219','broad','9') == ['P09']),
 ('York 16:15: Venus–Uranus pair together in the sky in winner (P25) and True Promise (P11)', lambda: {'P25','P11'} <= {x['runner'] for s in F('york_1615_20240515')['same_across_field'] if s['shape']==3 and 'Venus' in s['key'] and 'Uranus' in s['key'] for x in s['runners']}),
 ('York 16:15: winner the only runner with both ends moved AND the sky pair together on the same cross link', lambda: sorted({i['runner'] for i in F('york_1615_20240515')['instances'] if i['shape']==3 and any(j['runner']==i['runner'] and j['shape']==4 and j['bodies'][:2]==i['bodies'][:2] for j in F('york_1615_20240515')['instances'])}) == ['P25']),
 ('York 16:15: winner\'s Venus–Uranus tighter than True Promise\'s', lambda: (lambda I: min(i['tight_value'] for i in I if i['runner']=='P25' and i['shape']==3) < min(i['tight_value'] for i in I if i['runner']=='P11' and i['shape']==3 and 'Venus' in i['key']))(F('york_1615_20240515')['instances'])),

 ('Exeter: Forget You Not (P11) top pair Chiron–Juno, the most-lit pair in the field', lambda: F('exeter_1515_20211019')['pair_focus']['P11']['top']=='Chiron–Juno' and F('exeter_1515_20211019')['pair_focus']['P11']['most_lit_alone']),
 ('York 16:15: Venus–Uranus among the winner\'s pairs with 3+ kinds', lambda: any(x['pair']=='Uranus–Venus' for x in json.load(open('docs/classic/york_1615_20240515/layer3/P25.json'))['pair_focus'])),
 ('Newmarket July: Venus–Uranus among the winner\'s pairs with 3+ kinds', lambda: any(x['pair']=='Uranus–Venus' for x in json.load(open('docs/classic/newmarket_july_1745_20240816/layer3/P01.json'))['pair_focus'])),
]
fails = 0
for name, f in C:
    ok = f(); fails += not ok; print(('  ok   ' if ok else '  MISS ') + name)
print(f'{len(C)-fails}/{len(C)}'); sys.exit(1 if fails else 0)
