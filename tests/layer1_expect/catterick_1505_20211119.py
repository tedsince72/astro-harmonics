from l1helpers import *
RACE = 'catterick_1505_20211119'
P = 'P07'   # 4 Brian Boranha / 4 Callum Bewley

def _pt(I, c, b): return next(p for p in I['points'] if p['chart'] == c and p['body'] == b)
def _ddec(I, a, b): return abs(_pt(I, *a)['dec'] - _pt(I, *b)['dec'])

CHECKS = [
 ('1 cross H Sun–J Vesta (close, Dec 0.0001)', lambda I: link(I,'cross','H Sun','J Vesta',close=True)),
 ('1 cross H Transpluto–J Sun (close, RA 0.2949 Dec 0.1060)', lambda I: link(I,'cross','H Transpluto','J Sun',close=True)),
 ('2/3 sky Makemake -> H Transpluto Dec 10', lambda I: strike(I,'Makemake','H Transpluto','Dec','10')),
 ('2/3 sky Makemake -> J Sun RA 435/9', lambda I: strike(I,'Makemake','J Sun','RA','435/9')),
 ('3 sky Makemake -> H Sun RA 145', lambda I: strike(I,'Makemake','H Sun','RA','145')),
 ('3 sky Makemake -> H Pallas RA 980/9', lambda I: strike(I,'Makemake','H Pallas','RA','980/9')),
 ('3 sky Makemake -> J Haumea RA 8', lambda I: strike(I,'Makemake','J Haumea','RA','8')),
 ('3 sky Makemake -> J Ketu Dec 42/9', lambda I: strike(I,'Makemake','J Ketu','Dec','42/9')),
 ('4 H Transpluto–Regulus conj: star, not read by Layer 1 (not listed)',
  lambda I: 'Regulus' not in json.dumps(I) and any(p['chart']=='H' and p['body']=='Transpluto' for p in I['points'])),
 ('5 cross H Gonggong–J Quaoar (close, Dec 0.0247)', lambda I: link(I,'cross','H Gonggong','J Quaoar',close=True)),
 ('5 H Rahu–Quaoar close (RA 0.8255)', lambda I: link(I,'H','H Rahu','H Quaoar',close=True)),
 ('5 cross H Saturn–J Haumea (close, RA 0.2557)', lambda I: link(I,'cross','H Saturn','J Haumea',close=True)),
 ('6 sky Mars–Quaoar Dec 0.0014: sky-only conjunction < 0.5 (not a sky number); both sky points listed',
  lambda I: not sky(RACE,'Mars–Quaoar','Dec','0') and _ddec(I,('S','Mars'),('S','Quaoar')) < 0.002),
 ('6 sky Mars / sky Quaoar Dec ~0.11 from H Quaoar: < 0.5 (not a strike / movement); points listed',
  lambda I: not any(s['sky'] in ('Mars','Quaoar') and s['target']=='H Quaoar' and s['plane']=='Dec' for s in I['strikes'])
            and abs(_ddec(I,('S','Mars'),('H','Quaoar')) - 0.11) < 0.01 and abs(_ddec(I,('S','Quaoar'),('H','Quaoar')) - 0.11) < 0.01),
 ('7 soak Chiron ~18.3438: 165/9 off ~0.01, not a ninth (not listed); the four distances are present in points',
  lambda I: not any(s['num']=='165/9' and (s['target']=='J Chiron' or s['sky']=='Chiron') for s in I['strikes'])
            and abs(_ddec(I,('S','Mars'),('J','Chiron')) - 18.3438) < 0.002
            and abs(_ddec(I,('S','Quaoar'),('J','Chiron')) - 18.3438) < 0.002
            and abs(_ddec(I,('S','Chiron'),('H','Ceres')) - 18.3438) < 0.002
            and abs(abs(_pt(I,'S','Chiron')['ra'] - _pt(I,'H','Eris')['ra']) - 18.3438) < 0.002),
]
