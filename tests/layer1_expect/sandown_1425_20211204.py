from l1helpers import *
RACE = 'sandown_1425_20211204'
P = 'P05'   # 3 Greaneteen / 3 Bryony Le Clerc (Frost)

CHECKS = [
 ('1 Uranus same-body Flat 5/2:7/2:7/5', lambda I: same(I, 'Uranus', 'Flat', ['5/2', '7/2', '7/5'])),
 ('1 Quaoar same-body GC 3:4:4/3', lambda I: same(I, 'Quaoar', 'GC', ['3', '4', '4/3'])),
 ('2 H Mercury–Uranus Flat 25/3', lambda I: ratio(I, 'H', 'Mercury–Uranus', 'Flat', '25/3')),
 ('2 H Mercury–Rahu Flat 8/7', lambda I: ratio(I, 'H', 'Mercury–Rahu', 'Flat', '8/7')),
 ('2 H Mercury–Sedna Flat 17/6', lambda I: ratio(I, 'H', 'Mercury–Sedna', 'Flat', '17/6')),
 ('2 J Mercury–Vesta Dec 15/4', lambda I: ratio(I, 'J', 'Mercury–Vesta', 'Dec', '15/4')),
 ('2 J Mercury–Pluto GC 7/2', lambda I: ratio(I, 'J', 'Mercury–Pluto', 'GC', '7/2')),
 ('2 J Mercury–Orcus GC 5/4', lambda I: ratio(I, 'J', 'Mercury–Orcus', 'GC', '5/4')),
 ('3 J Sun–Mars RA 118', lambda I: link(I, 'J', 'J Sun', 'J Mars', 'RA', '118')),
 ('3 J Sun–Mars Dec 92/9', lambda I: link(I, 'J', 'J Sun', 'J Mars', 'Dec', '92/9')),
 ('3 sky Ceres -> J Mars Dec 2', lambda I: strike(I, 'Ceres', 'J Mars', 'Dec', '2')),
 ('3 sky Ceres -> J Sun Dec 74/9', lambda I: strike(I, 'Ceres', 'J Sun', 'Dec', '74/9')),
 ('4 J Sun–Jupiter Dec 11/3 (natal/sky)', lambda I: any(r['chart'] == 'J' and r['pair'] == 'Sun–Jupiter' and r['plane'] == 'Dec' and r['ratio'] == '11/3'
                                                      and r['dir'] == 'natal/sky' for r in I['ratios'])),
 ('4 J Sun–Saturn Dec 25/6 (natal/sky)', lambda I: any(r['chart'] == 'J' and r['pair'] == 'Sun–Saturn' and r['plane'] == 'Dec' and r['ratio'] == '25/6'
                                                     and r['dir'] == 'natal/sky' for r in I['ratios'])),
 ('5 H Venus–Jupiter Dec 17/5 (natal/sky)', lambda I: any(r['chart'] == 'H' and r['pair'] == 'Venus–Jupiter' and r['plane'] == 'Dec' and r['ratio'] == '17/5'
                                                        and r['dir'] == 'natal/sky' for r in I['ratios'])),
 ('6 cross H Makemake–J Haumea close (RA 0.0159)', lambda I: link(I, 'cross', 'H Makemake', 'J Haumea', close=True)),
 ('6 J Juno–Makemake GC 11/9', lambda I: ratio(I, 'J', 'Juno–Makemake', 'GC', '11/9')),
 ('7 sky Regulus* -> H Uranus RA 1264/9, Dec 69/9: fixed star (Layer 1 reads no stars) — not listed; H Uranus point present',
  lambda I: not any(s['sky'] == 'Regulus' for s in I['strikes']) and any(p['chart'] == 'H' and p['body'] == 'Uranus' for p in I['points'])),
]
