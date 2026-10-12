"""Layer 1 v1.4 (12 Oct 2026, Eddie approved): items that were 'not listed' under v1.3 and are now listed in the new near bands /
sections. Each entry replaces the check whose label starts with the given prefix."""
from l1helpers import *
NE = lambda b,pair,r: (lambda I: eqr(I,b,pair,r,'near'))
REPLACE = {
 'ascot_1350_20231021': {'3 cross H Jupiter–J Saturn': ('3 cross H Jupiter–J Saturn Dec 0.363 / RA 1.59: near cross link (v1.4)', lambda I: crossnear(I,'H Jupiter','J Saturn'))},
 'carlisle_1630_20220707': {'5x Ketu–Sedna': ('5x Ketu–Sedna Dec H/J 29/8: horse:jockey ratio, tight (v1.4)', lambda I: hjr(I,'Ketu–Sedna','Dec','29/8','tight'))},
 'chelmsford_aw_1320_20240118': {'1 cross H Chiron–J Rahu': ('1 cross H Chiron–J Rahu Dec 0.337: near cross link (v1.4)', lambda I: crossnear(I,'H Chiron','J Rahu'))},
 'fontwell_1530_20231006': {'6 Equator H/J Sun 18/5': ('6 Equator H/J Sun 18/5 (0.035%) near (v1.4)', NE('Sun','H/J','18/5')),
                            '6 Equator S/H Vesta 3/2': ('6 Equator S/H Vesta 3/2 (0.048%) near (v1.4)', NE('Vesta','S/H','3/2'))},
 'haydock_1405_20220219': {'2 Equator S/H Pluto 6/5': ('2 Equator S/H Pluto 6/5 (0.044%) near (v1.4)', NE('Pluto','S/H','6/5'))},
 'haydock_1718_20220507': {'2 cross H Juno–J Venus': ('2 cross H Juno–J Venus Dec 0.437: near cross link (v1.4)', lambda I: crossnear(I,'H Juno','J Venus'))},
 'huntingdon_1352_20211205': {'R Neptune Equator H/S 9/4': ('R Neptune Equator S/H 9/4 (0.041%) near (v1.4)', NE('Neptune','S/H','9/4'))},
 'newbury_1350_20211126': {
   '1 sky Mars on J Mars': ('1 sky Mars on J Mars RA 0.244: contact, RETURN (v1.4)', lambda I: any(x['sky']=='Mars' and x['target']=='J Mars' and x['return'] for x in I['contacts'])),
   '3 sky Vesta on J Mars': ('3 sky Vesta on J Mars Dec 0.0494: contact (v1.4)', lambda I: contact(I,'Vesta','J Mars','close')),
   'R2 Chiron–Transpluto RA': ('R2 Chiron–Transpluto RA J/H 21/8 (0.0114%): horse:jockey ratio, near (v1.4)', lambda I: hjr(I,'Chiron–Transpluto','RA','21/8','near')),
   'R4 H Haumea–Pallas GC 16/7': ('R4 H Haumea–Pallas GC 16/7 (0.0077%): ratio near (v1.4)', lambda I: ratioband(I,'H','Haumea–Pallas','GC','16/7','near')),
   'R6 Equator S/H Sun 7/5': ('R6 Equator S/H Sun 7/5 (0.035%) near (v1.4)', NE('Sun','S/H','7/5'))},
 'newcastle_1540_20220311': {'6 Equator S/H Uranus 13/3': ('6 Equator S/H Uranus 13/3 (0.036%) near (v1.4)', NE('Uranus','S/H','13/3'))},
 'newcastle_aw_1330_20220102': {
   '1 H Rahu – J Rahu': ('1 H Rahu – J Rahu RA 1.87 / Dec 0.52: near cross link (v1.4)', lambda I: crossnear(I,'H Rahu','J Rahu')),
   '4 sky Rahu–Sedna RA 0.2183': ('4 sky Rahu–Sedna RA 0.2183: sky close pair (v1.4)', lambda I: skyclose('newcastle_aw_1330_20220102','Rahu–Sedna')),
   'D3 H Juno–Eris RA 6/5': ('D3 H Juno–Eris RA 6/5 (0.0087%): ratio near (v1.4)', lambda I: ratioband(I,'H','Juno–Eris','RA','6/5','near')),
   'D3 J Juno–Ketu RA 13/4': ('D3 J Juno–Ketu RA 13/4 (0.0056%): ratio near (v1.4)', lambda I: ratioband(I,'J','Juno–Ketu','RA','13/4','near')),
   'D3 J Pallas–Juno Dec 9/7': ('D3 J Pallas–Juno Dec 9/7 (0.0099%): ratio near (v1.4)', lambda I: ratioband(I,'J','Pallas–Juno','Dec','9/7','near')),
   'D4 J Venus–Chiron Flat 23/7': ('D4 J Venus–Chiron Flat 23/7 (0.0057%): ratio near (v1.4)', lambda I: ratioband(I,'J','Venus–Chiron','Flat','23/7','near'))},
 'newcastle_aw_1220_20211112': {
   '3 sky Gonggong -> H Chiron RA 0.0674': ('3 sky Gonggong on H Chiron RA 0.0674: contact (v1.4)', lambda I: contact(I,'Gonggong','H Chiron','close')),
   '3 sky Gonggong -> H Neptune Dec 0.0950': ('3 sky Gonggong on H Neptune Dec 0.0950: contact (v1.4)', lambda I: contact(I,'Gonggong','H Neptune','close')),
   '6 sky Uranus -> H Venus RA 0.2371': ('6 sky Uranus on H Venus RA 0.2371: contact (v1.4)', lambda I: contact(I,'Uranus','H Venus','close'))},
 'newcastle_aw_1540_20211112': {'3 sky Makemake -> J Pluto RA 1.23108': ('3 sky Makemake on J Pluto RA 1.231: contact (v1.4)', lambda I: contact(I,'Makemake','J Pluto','close'))},
 'newcastle_aw_1640_20220215': {
   '3 sky Gonggong – H Chiron RA 0.4812': ('3 sky Gonggong on H Chiron RA 0.4812: contact (v1.4)', lambda I: contact(I,'Gonggong','H Chiron','close')),
   '3 sky Neptune – H Chiron Dec 0.1621': ('3 sky Neptune on H Chiron Dec 0.1621: contact (v1.4)', lambda I: contact(I,'Neptune','H Chiron','close')),
   '3 sky Gonggong – H Neptune Dec 0.1836': ('3 sky Gonggong on H Neptune Dec 0.1836: contact (v1.4)', lambda I: contact(I,'Gonggong','H Neptune','close')),
   '4 sky Uranus – J Sedna RA 0.1349': ('4 sky Uranus on J Sedna RA 0.1349: contact (v1.4)', lambda I: contact(I,'Uranus','J Sedna','close')),
   '4 sky Uranus – H Venus RA 1.0738': ('4 sky Uranus on H Venus RA 1.0738: contact (v1.4)', lambda I: contact(I,'Uranus','H Venus','close')),
   '6 Equator S/J Ceres 11/5': ('6 Equator S/J Ceres 11/5 (0.037%) near (v1.4)', NE('Ceres','S/J','11/5'))},
 'newmarket_1535_20220414': {'2 sky Jupiter–Neptune': ('2 sky Jupiter–Neptune RA 0.31 / Dec 0.24: sky close pair (v1.4)', lambda I: skyclose('newmarket_1535_20220414','Jupiter–Neptune'))},
 'newton_abbot_1525_20220717': {'6 Equator S/J Pallas 5/4': ('6 Equator S/J Pallas 5/4 (0.039%) near (v1.4)', NE('Pallas','S/J','5/4'))},
 'nottingham_1530_20220601': {'6 Equator S/J Pluto 5': ('6 Equator S/J Pluto 5 (0.044%) near (v1.4)', NE('Pluto','S/J','5'))},
 'perth_1610_20220420': {'2 Haumea–Ketu Dec': ('2 Haumea–Ketu Dec J/H 9/5 (0.0094%): horse:jockey ratio near (v1.4); S/H 17/7 0.013% still outside ratio near 0.01%',
                          lambda I: hjr(I,'Haumea–Ketu','Dec','9/5') and not ratio(I,'H','Haumea–Ketu','Dec','17/7'))},
 'sedgefield_1500_20220510': {'6 Equator H/J Saturn 13/7': ('6 Equator H/J Saturn 13/7 (0.034%) near (v1.4)', NE('Saturn','H/J','13/7'))},
 'wincanton_1420_20220321': {'7 Equator S/H Pallas 21/5': ('7 Equator S/H Pallas 21/5 (0.048%) near (v1.4)', NE('Pallas','S/H','21/5'))},
 'york_1545_20240515': {'6 Equator S/J Vesta 2': ('6 Equator S/J Vesta 2 (0.047%) near (v1.4)', NE('Vesta','S/J','2'))},
}
