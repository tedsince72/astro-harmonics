from l1helpers import *
RACE = 'newcastle_aw_1640_20220215'
P = 'P01'   # 1 Sir Chauvelin / 1 Paul Mulrennan
_NOSKY = 'sky-to-natal closeness is not a Layer 1 section (strikes are whole/ninth only, values < 0.5 skipped)'
CHECKS = [
 ('1 Venus same-body RA 11/5:11/6:6/5', lambda I: same(I,'Venus','RA',['11/5','11/6','6/5'])),
 ('1 Gonggong same-body Dec 7/2:9/2:9/7', lambda I: same(I,'Gonggong','Dec',['7/2','9/2','9/7'])),
 ('3 sky Gonggong – H Chiron RA 0.4812: not listed (' + _NOSKY + ')', lambda I: not any(s['sky']=='Gonggong' and s['target']=='H Chiron' and s['plane']=='RA' for s in I['strikes'])),
 ('3 sky Neptune – H Chiron Dec 0.1621: not listed (' + _NOSKY + ')', lambda I: not any(s['sky']=='Neptune' and s['target']=='H Chiron' and s['plane']=='Dec' for s in I['strikes'])),
 ('3 sky Gonggong – H Neptune Dec 0.1836: not listed (' + _NOSKY + ')', lambda I: not any(s['sky']=='Gonggong' and s['target']=='H Neptune' and s['plane']=='Dec' for s in I['strikes'])),
 ('4 H Venus–Uranus Dec sky/natal 13/7', lambda I: ratio(I,'H','Venus–Uranus','Dec','13/7')),
 ('4 sky Uranus – J Sedna RA 0.1349: not listed (' + _NOSKY + ')', lambda I: not any(s['sky']=='Uranus' and s['target']=='J Sedna' and s['plane']=='RA' for s in I['strikes'])),
 ('4 cross H Venus–J Sedna RA 1.2088 (close)', lambda I: link(I,'cross','H Venus','J Sedna',close=True)),
 ('4 sky Uranus – H Venus RA 1.0738: not listed (' + _NOSKY + ')', lambda I: not any(s['sky']=='Uranus' and s['target']=='H Venus' and s['plane']=='RA' for s in I['strikes'])),
 ('5 J Juno moved Dec 33/9', lambda I: move(I,'J','Juno','Dec','33/9')),
 ('5 cross H Pluto–J Juno RA 0.046 (close)', lambda I: link(I,'cross','H Pluto','J Juno',close=True)),
 ('6 Equator S/J Ceres 11/5 at 0.037%: outside the 0.03% near band (not listed)', lambda I: not any(e['body']=='Ceres' and e['pair']=='S/J' for e in I['eq_ratios'])),
 ('7 H Mars–Chiron RA 13/6', lambda I: ratio(I,'H','Mars–Chiron','RA','13/6')),
 ('7 J Saturn–Vesta Flat 23/6', lambda I: ratio(I,'J','Saturn–Vesta','Flat','23/6')),
 ('7 J Chiron–Rahu GC 7/6', lambda I: ratio(I,'J','Chiron–Rahu','GC','7/6')),
]
