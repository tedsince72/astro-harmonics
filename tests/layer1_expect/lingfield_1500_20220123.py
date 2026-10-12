from l1helpers import *
from l1helpers import _pm
RACE = 'lingfield_1500_20220123'
P = 'P11'   # 7 Two For Gold / 7 David Bass
CHECKS = [
 ('1 H Chiron–Transpluto Dec natal/sky 14/5', lambda I: ratio(I,'H','Chiron–Transpluto','Dec','14/5')),
 ('2 Haumea–Ketu RA three-way H 164.2962 J 17.0684 S 19.2041: not listed (ratios 77/9, 77/8 have p > 30; S:J 9/8 0.011%)',
  lambda I: not pset(I,'Haumea–Ketu','RA')),
 ('3 cross H Haumea–J Venus Dec 0.0350 (close)', lambda I: link(I,'cross','H Haumea','J Venus',close=True)),
 ('3 cross H Haumea–J Jupiter Dec 0.1132 (close)', lambda I: link(I,'cross','H Haumea','J Jupiter',close=True)),
 ('3 cross H Haumea–J Pallas Dec 0.1474 (close)', lambda I: link(I,'cross','H Haumea','J Pallas',close=True)),
 ('3 H Jupiter–Haumea Dec sky/natal 7', lambda I: ratio(I,'H','Jupiter–Haumea','Dec','7')),
 ('4 cross H Jupiter–J Venus RA 0.447 (close)', lambda I: link(I,'cross','H Jupiter','J Venus',close=True)),
 ('4 sky Orcus -> H Jupiter RA 84', lambda I: strike(I,'Orcus','H Jupiter','RA','84')),
 ('4 sky Orcus -> J Venus Dec 276/9', lambda I: strike(I,'Orcus','J Venus','Dec','276/9')),
 ('4 sky Saturn -> H Haumea Dec 323/9', lambda I: strike(I,'Saturn','H Haumea','Dec','323/9')),
 ('4 sky Saturn -> J Pallas RA 7', lambda I: strike(I,'Saturn','J Pallas','RA','7')),
 ('4 J Juno–Transpluto Dec 0.050 (close)', lambda I: link(I,'J','J Juno','J Transpluto',close=True)),
 ('4 sky Mercury -> J Juno Dec 278/9', lambda I: strike(I,'Mercury','J Juno','Dec','278/9')),
 ('4 sky Mercury -> J Transpluto RA 1450/9', lambda I: strike(I,'Mercury','J Transpluto','RA','1450/9')),
 ('4 sky Saturn -> J Saturn RA 435/9', lambda I: strike(I,'Saturn','J Saturn','RA','435/9')),
 ('5 J Saturn moved RA 435/9', lambda I: move(I,'J','Saturn','RA','435/9')),
 ('5 H Orcus moved RA 9', lambda I: move(I,'H','Orcus','RA','9')),
 ('5 cross H Orcus–J Vesta RA 0.4292 (close)', lambda I: link(I,'cross','H Orcus','J Vesta',close=True)),
 ('5 H Gonggong moved RA 1', lambda I: move(I,'H','Gonggong','RA','1')),
 ('6 Mercury same-body GC 5/4:9/4:9/5', lambda I: same(I,'Mercury','GC',['5/4','9/4','9/5'])),
 ('6 Mercury same-body RA 5/4:9/4:9/5', lambda I: same(I,'Mercury','RA',['5/4','9/4','9/5'])),
 ('6 Sedna same-body GC 5/2:7/2:7/5', lambda I: same(I,'Sedna','GC',['5/2','7/2','7/5'])),
 ('6 Mars same-body Dec 15/7:15/8:8/7', lambda I: same(I,'Mars','Dec',['15/7','15/8','8/7'])),
 ('7 H Venus–Sedna RA 17/3', lambda I: ratio(I,'H','Venus–Sedna','RA','17/3')),
 ('7 J Mercury–Ceres RA 3/2', lambda I: ratio(I,'J','Mercury–Ceres','RA','3/2')),
 ('7 H Chiron–Orcus RA 10/9', lambda I: ratio(I,'H','Chiron–Orcus','RA','10/9')),
 ('8 J Neptune–Rahu RA 67.9376 / sky 64.6638 not simple: not listed (read agrees)', lambda I: not any(x['chart']=='J' and _pm('Neptune–Rahu',x['pair']) and x['plane']=='RA' for x in I['ratios'])),
]
