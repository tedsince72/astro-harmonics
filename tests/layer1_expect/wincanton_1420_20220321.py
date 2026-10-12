from l1helpers import *
RACE = 'wincanton_1420_20220321'
P = 'P07'
def eqv(I, c, b, v): return any(p['chart']==c and p['body']==b and abs(p['eq']-v) < 0.0001 for p in I['points'])
CHECKS = [
 ('1 H Mercury moved Dec 30', lambda I: move(I,'H','Mercury','Dec','30')),
 ('1 cross H Mercury–J Chiron close (RA 0.0255)', lambda I: link(I,'cross','H Mercury','J Chiron',close=True)),
 ('2 J Neptune–Chiron Dec 26/7', lambda I: ratio(I,'J','Neptune–Chiron','Dec','26/7')),
 ('2 J Neptune–Orcus Dec 29/9', lambda I: ratio(I,'J','Neptune–Orcus','Dec','29/9')),
 ('2 J Neptune–Vesta RA 23/5', lambda I: ratio(I,'J','Neptune–Vesta','RA','23/5')),
 ('2 J Neptune–Makemake GC 5/4', lambda I: ratio(I,'J','Neptune–Makemake','GC','5/4')),
 ('2 cross H Pluto–J Neptune close (RA 0.2450)', lambda I: link(I,'cross','H Pluto','J Neptune',close=True)),
 ('2 J Saturn–Neptune close (RA 0.8433)', lambda I: link(I,'J','J Saturn','J Neptune',close=True)),
 ('3 J Chiron–Rahu Dec 12/5', lambda I: ratio(I,'J','Chiron–Rahu','Dec','12/5')),
 ('4 J Sun–Rahu close (Dec 0.0001)', lambda I: link(I,'J','J Sun','J Rahu',close=True)),
 ('4 J Ketu–Transpluto close (RA 0.4752 Dec 0.1574)', lambda I: link(I,'J','J Ketu','J Transpluto',close=True)),
 ('4 J Pallas–Rahu RA 380/9', lambda I: link(I,'J','J Pallas','J Rahu','RA','380/9')),
 ('4 J Pallas–Rahu Dec 3', lambda I: link(I,'J','J Pallas','J Rahu','Dec','3')),
 ('5 J Jupiter–Vesta RA 4', lambda I: ratio(I,'J','Jupiter–Vesta','RA','4')),
 ('6 J Ceres moved Dec 10/9', lambda I: move(I,'J','Ceres','Dec','10/9')),
 ('6 J Ceres–Haumea close (Dec 0.174)', lambda I: link(I,'J','J Ceres','J Haumea',close=True)),
 ('6 sky Ceres -> J Ceres Dec 10/9', lambda I: strike(I,'Ceres','J Ceres','Dec','10/9')),
 ('6 sky Ceres -> J Haumea RA 120', lambda I: strike(I,'Ceres','J Haumea','RA','120')),
 ('7 sky Pallas Equator 6', lambda I: eqpt(I,'S','Pallas','6')),
 ('7 Equator S/H Pallas 21/5 (0.048%): outside near band 0.03% (not listed); both Equator values present',
  lambda I: not any(e['body']=='Pallas' and e['pair']=='S/H' for e in I['eq_ratios']) and eqv(I,'S','Pallas',6.0022) and eqv(I,'H','Pallas',1.4298)),
 ('7 Equator H/J Haumea 6/5 near', lambda I: eqr(I,'Haumea','H/J','6/5','near')),
 ('7 H Sun–Jupiter close (Dec 0.0064)', lambda I: link(I,'H','H Sun','H Jupiter',close=True)),
]
