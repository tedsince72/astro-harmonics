from l1helpers import *
RACE = 'wolverhampton_aw_1725_20231021'
P = 'P05'
CHECKS = [
 ('1 cross H Eris–J Jupiter RA 1.1336 (close)', lambda I: link(I,'cross','H Eris','J Jupiter',close=True)),
 ('1 H Eris moved RA 8/9', lambda I: move(I,'H','Eris','RA','8/9')),
 ('1 J Jupiter moved GC 122/9', lambda I: move(I,'J','Jupiter','GC','122/9')),
 ('2 shared Neptune–Rahu RA', lambda I: shared(I,'Neptune–Rahu','RA')),
 ('3 cross H Pluto–J Neptune Dec 0.0323 (close)', lambda I: link(I,'cross','H Pluto','J Neptune',close=True)),
 ('3 cross H Quaoar–J Neptune RA 0.6430 (close)', lambda I: link(I,'cross','H Quaoar','J Neptune',close=True)),
 ('3 H Neptune–Quaoar Dec 6/5', lambda I: ratio(I,'H','Neptune–Quaoar','Dec','6/5')),
 ('3 H Neptune–Gonggong RA 14', lambda I: link(I,'H','H Neptune','H Gonggong','RA','14')),
 ('3 sky Sedna -> H Neptune RA 70', lambda I: strike(I,'Sedna','H Neptune','RA','70')),
 ('3 sky Sedna -> H Gonggong RA 84', lambda I: strike(I,'Sedna','H Gonggong','RA','84')),
 ('4 H Rahu–Makemake Dec 0.0113 (close)', lambda I: link(I,'H','H Rahu','H Makemake',close=True)),
 ('4 cross H Makemake–J Haumea Dec 0.1285 (close)', lambda I: link(I,'cross','H Makemake','J Haumea',close=True)),
 ('4 cross H Rahu–J Haumea Dec 0.1172 (close)', lambda I: link(I,'cross','H Rahu','J Haumea',close=True)),
 ('4 J Venus–Haumea RA 0.0009 (close)', lambda I: link(I,'J','J Venus','J Haumea',close=True)),
 ('5 Jupiter–Sedna RA H:J 65/9 (p > 30), H:S 46/9 0.0105% (> 0.005%): not a pair set, not an H sky/natal ratio (not listed)',
  lambda I: not pset(I,'Jupiter–Sedna','RA') and not ratio(I,'H','Jupiter–Sedna','RA','46/9')),
 ('5 J Uranus–Sedna Dec 23/8', lambda I: ratio(I,'J','Uranus–Sedna','Dec','23/8')),
 ('5 H Eris–Sedna RA 32', lambda I: link(I,'H','H Eris','H Sedna','RA','32')),
 ('5 sky Transpluto -> H Eris RA 130', lambda I: strike(I,'Transpluto','H Eris','RA','130')),
 ('5 sky Transpluto -> H Sedna RA 98', lambda I: strike(I,'Transpluto','H Sedna','RA','98')),
 ('6 sky Saturn Equator 13', lambda I: eqpt(I,'S','Saturn','13')),
 ('6 sky Vesta Equator 19', lambda I: eqpt(I,'S','Vesta','19')),
 ('6 Equator S/H Chiron 16/9 near', lambda I: eqr(I,'Chiron','S/H','16/9','near')),
]
