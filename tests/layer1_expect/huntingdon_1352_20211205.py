from l1helpers import *
RACE = 'huntingdon_1352_20211205'
P = 'P05'   # 3 First Flow / 3 David Bass

def _eq(I, c, b): return next(p['eq'] for p in I['points'] if p['chart'] == c and p['body'] == b)

CHECKS = [
 ('1 H Mars–Neptune Dec 7/4', lambda I: ratio(I, 'H', 'Mars–Neptune', 'Dec', '7/4')),
 ('1 H Juno–Ketu Flat 14/3', lambda I: ratio(I, 'H', 'Juno–Ketu', 'Flat', '14/3')),
 ('1 H Juno–Gonggong Dec 3', lambda I: ratio(I, 'H', 'Juno–Gonggong', 'Dec', '3')),
 ('1 J Chiron–Vesta GC 13/6', lambda I: ratio(I, 'J', 'Chiron–Vesta', 'GC', '13/6')),
 ('1 J Pallas–Eris RA 7/4', lambda I: ratio(I, 'J', 'Pallas–Eris', 'RA', '7/4')),
 ('1 J Juno–Haumea GC 7/5', lambda I: ratio(I, 'J', 'Juno–Haumea', 'GC', '7/5')),
 ('1 J Sedna–Gonggong RA 8/7', lambda I: ratio(I, 'J', 'Sedna–Gonggong', 'RA', '8/7')),
 ('2 cross H Orcus–J Vesta close (RA 1.256)', lambda I: link(I, 'cross', 'H Orcus', 'J Vesta', close=True)),
 ('2 sky Juno -> H Orcus Dec 64/9', lambda I: strike(I, 'Juno', 'H Orcus', 'Dec', '64/9')),
 ('2 sky Juno -> J Vesta Dec 32', lambda I: strike(I, 'Juno', 'J Vesta', 'Dec', '32')),
 ('2 J Pluto–Rahu Dec 6', lambda I: link(I, 'J', 'J Pluto', 'J Rahu', 'Dec', '6')),
 ('2 sky Juno -> J Pluto Dec 133/9', lambda I: strike(I, 'Juno', 'J Pluto', 'Dec', '133/9')),
 ('2 sky Juno -> J Rahu Dec 79/9', lambda I: strike(I, 'Juno', 'J Rahu', 'Dec', '79/9')),
 ('3 cross H Pluto–J Neptune close (RA 0.231)', lambda I: link(I, 'cross', 'H Pluto', 'J Neptune', close=True)),
 ('3 sky Haumea -> H Pluto RA 63', lambda I: strike(I, 'Haumea', 'H Pluto', 'RA', '63')),
 ('3 sky Haumea -> J Neptune Dec 37', lambda I: strike(I, 'Haumea', 'J Neptune', 'Dec', '37')),
 ('3 cross H Pallas–J Rahu close (RA 0.1394)', lambda I: link(I, 'cross', 'H Pallas', 'J Rahu', close=True)),
 ('5 sky Orcus Equator 12', lambda I: eqpt(I, 'S', 'Orcus', '12')),
 ('R pair set Neptune–Rahu RA (H:J 4/3, H:S 4/3, J:S 1)', lambda I: any(s['pair'] == 'Neptune–Rahu' and s['plane'] == 'RA' and s['H:J'] == '4/3'
                                                                     and s['H:S'] == '4/3' and s['J:S'] == '1' for s in I['pair_sets'])),
 ('R H Mars–Neptune Dec 7/4 (0.00069%)', lambda I: any(r['chart'] == 'H' and r['pair'] == 'Mars–Neptune' and r['plane'] == 'Dec' and r['ratio'] == '7/4'
                                                     and r['err_pct'] < 0.001 for r in I['ratios'])),
 ('R Neptune Equator H/S 9/4 (0.041% > 0.03% near band) — not listed; both Equator values present',
  lambda I: not any(e['body'] == 'Neptune' and e['pair'] == 'S/H' for e in I['eq_ratios'])
            and abs((_eq(I, 'H', 'Neptune') / _eq(I, 'S', 'Neptune')) / 2.25 - 1) < 0.0005),
 ('R sky Haumea both ends of H Pluto–J Neptune (RA 63 | Dec 37)', lambda I: strike(I, 'Haumea', 'H Pluto', 'RA', '63') and strike(I, 'Haumea', 'J Neptune', 'Dec', '37')),
]
