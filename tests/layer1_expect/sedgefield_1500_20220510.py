from l1helpers import *
RACE = 'sedgefield_1500_20220510'
P = 'P01'
CHECKS = [
 ('1 cross H Ketu–J Sun close (RA 0.4098 Dec 0.1478)', lambda I: link(I,'cross','H Ketu','J Sun',close=True)),
 ('1 J Sun–Mercury close (RA 0.3394)', lambda I: link(I,'J','J Sun','J Mercury',close=True)),
 ('1 cross H Ketu–J Mercury close (RA 0.7493)', lambda I: link(I,'cross','H Ketu','J Mercury',close=True)),
 ('1 cross H Sedna–J Ketu close (RA 0.0504)', lambda I: link(I,'cross','H Sedna','J Ketu',close=True)),
 ('1 H Mercury–Sedna close (Dec 0.0653)', lambda I: link(I,'H','H Mercury','H Sedna',close=True)),
 ('1 H Rahu–Transpluto close (RA 0.3394 Dec 0.1244)', lambda I: link(I,'H','H Rahu','H Transpluto',close=True)),
 ('2 H Neptune moved GC 11', lambda I: move(I,'H','Neptune','GC','11')),
 ('2 cross H Neptune–J Mercury close (Dec 0.1358)', lambda I: link(I,'cross','H Neptune','J Mercury',close=True)),
 ('3 H Sedna Equator 69/9', lambda I: eqpt(I,'H','Sedna','69/9')),
 ('3 H Saturn moved Dec 69/9', lambda I: move(I,'H','Saturn','Dec','69/9')),
 ('4 H Sedna–Haumea Dec 9/7', lambda I: ratio(I,'H','Sedna–Haumea','Dec','9/7')),
 ('4 cross H Mars–J Haumea close (Dec 0.0177)', lambda I: link(I,'cross','H Mars','J Haumea',close=True)),
 ('4 shared Haumea–Makemake RA', lambda I: shared(I,'Haumea–Makemake','RA')),
 ('5 H Sun–Mars Dec 25/7', lambda I: ratio(I,'H','Sun–Mars','Dec','25/7')),
 ('5 H Ceres–Vesta RA 15/8', lambda I: ratio(I,'H','Ceres–Vesta','RA','15/8')),
 ('5 H Mercury–Gonggong GC 16/9', lambda I: ratio(I,'H','Mercury–Gonggong','GC','16/9')),
 ('5 J Saturn–Juno Flat 25/3', lambda I: ratio(I,'J','Saturn–Juno','Flat','25/3')),
 ('6 J Jupiter Equator 15', lambda I: eqpt(I,'J','Jupiter','15')),
 ('6 H Pluto Equator 191/9', lambda I: eqpt(I,'H','Pluto','191/9')),
 ('6 J Rahu Equator 178/9', lambda I: eqpt(I,'J','Rahu','178/9')),
 ('6 Equator H/J Saturn 13/7 (0.034%): outside near band 0.03% (not listed); both Equator values present',
  lambda I: not eqr(I,'Saturn','H/J','13/7','near') and not eqr(I,'Saturn','H/J','13/7','tight')
            and any(p['chart']=='H' and p['body']=='Saturn' and abs(p['eq']-22.0357)<0.0001 for p in I['points'])
            and any(p['chart']=='J' and p['body']=='Saturn' and abs(p['eq']-11.8613)<0.0001 for p in I['points'])),
]
