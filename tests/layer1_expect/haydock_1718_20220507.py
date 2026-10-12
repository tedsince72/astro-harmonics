from l1helpers import *
RACE = 'haydock_1718_20220507'
P = 'P07'
def psr(I,pair,pl,rs):
    a,b=pair.split('–')
    return any(s['pair'] in (pair,f'{b}–{a}') and s['plane']==pl and sorted([s['H:J'],s['H:S'],s['J:S']])==sorted(rs) for s in I['pair_sets'])
CHECKS = [
 ('1 pair set Sedna–Haumea RA (8/7, 1, 8/7)', lambda I: psr(I,'Sedna–Haumea','RA',['8/7','1','8/7'])),
 ('1 pair set Venus–Saturn Dec (15/2, 4/3, 10)', lambda I: psr(I,'Venus–Saturn','Dec',['15/2','4/3','10'])),
 ('2 J Venus–Saturn Dec sky/natal 10', lambda I: ratio(I,'J','Venus–Saturn','Dec','10')),
 ('2 J Venus–Saturn GC sky/natal 10', lambda I: ratio(I,'J','Venus–Saturn','GC','10')),
 ('2 J Venus moved Dec 11', lambda I: move(I,'J','Venus','Dec','11')),
 ('2 cross H Juno–J Venus Dec 0.43702 (RA 75.34): outside cross close Dec < 0.3, no whole/ninth (not listed); both ends struck by sky Venus are listed',
  lambda I: not has_link(I,'H Juno','J Venus',close=False) and strike(I,'Venus','H Juno','RA','671/9') and strike(I,'Venus','J Venus','Dec','11')),
 ('2 sky Venus -> H Juno RA 671/9', lambda I: strike(I,'Venus','H Juno','RA','671/9')),
 ('2 sky Venus -> J Venus Dec 11', lambda I: strike(I,'Venus','J Venus','Dec','11')),
 ('3 cross H Makemake–J Haumea close (Dec 0.0058)', lambda I: link(I,'cross','H Makemake','J Haumea',close=True)),
 ('3 sky Ceres -> H Makemake Dec 2', lambda I: strike(I,'Ceres','H Makemake','Dec','2')),
 ('3 sky Ceres -> J Haumea Dec 2', lambda I: strike(I,'Ceres','J Haumea','Dec','2')),
 ('4 J Sun–Sedna GC 23/5', lambda I: ratio(I,'J','Sun–Sedna','GC','23/5')),
 ('4 J Saturn–Sedna GC 6/5', lambda I: ratio(I,'J','Saturn–Sedna','GC','6/5')),
 ('4 J Sedna–Orcus Dec 19/7', lambda I: ratio(I,'J','Sedna–Orcus','Dec','19/7')),
 ('4 H Vesta–Sedna RA 13/8', lambda I: ratio(I,'H','Vesta–Sedna','RA','13/8')),
 ('4 J Chiron–Sedna close (RA 0.1011)', lambda I: link(I,'J','J Chiron','J Sedna',close=True)),
 ('4 H Mars–Sedna close (RA 0.8851)', lambda I: link(I,'H','H Mars','H Sedna',close=True)),
 ('5 sky Gonggong Equator 11', lambda I: eqpt(I,'S','Gonggong','11')),
 ('5 Equator H/J Gonggong 2 tight (corrected)', lambda I: eqr(I,'Gonggong','H/J','2','tight')),
 ('5 Equator S/H Saturn 3/2 tight', lambda I: eqr(I,'Saturn','S/H','3/2','tight')),
 ('6 J Ketu–Transpluto Dec 11/6', lambda I: ratio(I,'J','Ketu–Transpluto','Dec','11/6')),
 ('6 Vesta same-body GC 13/4:9/4:13/9', lambda I: same(I,'Vesta','GC',['13/4','9/4','13/9'])),
 ('6 Sun same-body RA 3:2:3/2', lambda I: same(I,'Sun','RA',['3','2','3/2'])),
 ('6 J Eris moved GC 110/9', lambda I: move(I,'J','Eris','GC','110/9')),
 ('6 cross H Gonggong–J Eris close (Dec 0.239)', lambda I: link(I,'cross','H Gonggong','J Eris',close=True)),
]
