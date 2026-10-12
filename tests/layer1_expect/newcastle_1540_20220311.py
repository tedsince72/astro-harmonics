from l1helpers import *
from l1helpers import _pm
RACE = 'newcastle_1540_20220311'
P = 'P05'   # 3 Peak Time / 3 Conor O'Farrell
CHECKS = [
 ('1 pair set Vesta–Sedna Flat H:J 22/7 H:S 11/4 J:S 8/7', lambda I: any(_pm('Vesta–Sedna', s['pair']) and s['plane']=='Flat' and (s['H:J'],s['H:S'],s['J:S'])==('22/7','11/4','8/7') for s in I['pair_sets'])),
 ('2a J Ceres moved Dec 4', lambda I: move(I,'J','Ceres','Dec','4')),
 ('2a cross H Haumea–J Ceres Dec 0.153 (close)', lambda I: link(I,'cross','H Haumea','J Ceres',close=True)),
 ('2b H Ceres moved Dec 6', lambda I: move(I,'H','Ceres','Dec','6')),
 ('2b cross H Ceres–J Chiron RA 0.798 (close)', lambda I: link(I,'cross','H Ceres','J Chiron',close=True)),
 ('2c Ceres same-body Dec 5/3:3/2:5/2', lambda I: same(I,'Ceres','Dec',['5/3','3/2','5/2'])),
 ('2c J Mars–Ceres RA sky/natal 14/9', lambda I: ratio(I,'J','Mars–Ceres','RA','14/9')),
 ('2d J Jupiter–Ceres RA 17', lambda I: linknum(I,'J Jupiter','J Ceres','RA','17')),
 ('2d sky Sedna -> J Jupiter RA 31', lambda I: strike(I,'Sedna','J Jupiter','RA','31')),
 ('2d sky Sedna -> J Ceres RA 14', lambda I: strike(I,'Sedna','J Ceres','RA','14')),
 ('3 H Chiron Equator 2', lambda I: eqpt(I,'H','Chiron','2')),
 ('3 cross H Ketu–J Chiron Dec 0.0957 (close)', lambda I: link(I,'cross','H Ketu','J Chiron',close=True)),
 ('3 Chiron same-body Dec 7/3:4/3:7/4', lambda I: same(I,'Chiron','Dec',['7/3','4/3','7/4'])),
 ('4 J Mars–Ketu RA 0.0159 (close)', lambda I: link(I,'J','J Mars','J Ketu',close=True)),
 ('4 cross H Orcus–J Mars RA 0.3065 (close)', lambda I: link(I,'cross','H Orcus','J Mars',close=True)),
 ('4 cross H Orcus–J Ketu RA 0.3224 (close)', lambda I: link(I,'cross','H Orcus','J Ketu',close=True)),
 ('4 J Mars–Neptune Dec 20/9', lambda I: ratio(I,'J','Mars–Neptune','Dec','20/9')),
 ('4 J Mars–Makemake Flat 4', lambda I: ratio(I,'J','Mars–Makemake','Flat','4')),
 ('5 J Sun–Vesta Dec 8/3', lambda I: ratio(I,'J','Sun–Vesta','Dec','8/3')),
 ('5 J Neptune–Orcus Dec 10/3', lambda I: ratio(I,'J','Neptune–Orcus','Dec','10/3')),
 ('5 H Jupiter–Orcus Dec 16/3', lambda I: ratio(I,'H','Jupiter–Orcus','Dec','16/3')),
 ('5 H Sun–Mars GC 25/2', lambda I: ratio(I,'H','Sun–Mars','GC','25/2')),
 ('5 cross H Pluto–J Neptune RA 0.623 (close)', lambda I: link(I,'cross','H Pluto','J Neptune',close=True)),
 ('6 (corrected) Equator H/J Sedna 12/7 near (0.0145%)', lambda I: eqr(I,'Sedna','H/J','12/7','near')),
 ('6 Equator S/H Uranus 13/3 at 0.036%: outside the 0.03% near band (not listed)', lambda I: not any(e['body']=='Uranus' and e['pair']=='S/H' for e in I['eq_ratios'])),
]
