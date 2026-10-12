from l1helpers import *
RACE = 'newcastle_aw_1540_20211112'
P = 'P05'   # 3 Heart Throb / 3 Graham Lee

_STARS = ('Regulus', 'Vega', 'Algol', 'Deneb', 'Fomalhaut')
def _nostar(I): return not any(s in json.dumps(I) for s in _STARS)
def _pt(I, c, b): return any(p['chart'] == c and p['body'] == b for p in I['points'])

CHECKS = [
 ('1 Orcus same-body RA 7:8:8/7', lambda I: same(I,'Orcus','RA',['7','8','8/7'])),
 ('2 sky Ketu -> H Orcus RA 87', lambda I: strike(I,'Ketu','H Orcus','RA','87')),
 ('2 sky Rahu -> H Orcus RA 93', lambda I: strike(I,'Rahu','H Orcus','RA','93')),
 ('3 J Pluto–Orcus close (Dec 0.2476)', lambda I: link(I,'J','J Pluto','J Orcus',close=True)),
 ('3 sky Makemake–Vega* RA 80.5813: star, not read by Layer 1 (not listed)', lambda I: _nostar(I) and _pt(I,'S','Makemake')),
 ('3 sky Makemake -> J Orcus Dec 11', lambda I: strike(I,'Makemake','J Orcus','Dec','11')),
 ('3 sky Makemake -> J Pluto RA 1.23108: raw value, not whole/ninth (not listed)',
  lambda I: not any(s['sky']=='Makemake' and s['target']=='J Pluto' and s['plane']=='RA' for s in I['strikes']) and _pt(I,'J','Pluto')),
 ('4 H Orcus–Transpluto close (RA 0.6730)', lambda I: link(I,'H','H Orcus','H Transpluto',close=True)),
 ('4 H Orcus–Regulus* RA 0.2801 and H Orcus–J Regulus* RA 0.2776: star (not listed)', lambda I: _nostar(I) and _pt(I,'H','Orcus')),
 ('4 cross H Transpluto–J Orcus (close, Dec 0.1408)', lambda I: link(I,'cross','H Transpluto','J Orcus',close=True)),
 ('5 H Rahu–Ceres close (RA 0.0897)', lambda I: link(I,'H','H Ceres','H Rahu',close=True)),
 ('6 3-way Dec Deneb Algedi*–Venus: star partner (not listed); Venus points listed',
  lambda I: not pset(I,'Venus–Deneb Algedi','Dec') and _nostar(I) and _pt(I,'H','Venus') and _pt(I,'J','Venus') and _pt(I,'S','Venus')),
 ('7 Jupiter same-body RA 3/2:2:3', lambda I: same(I,'Jupiter','RA',['3/2','2','3'])),
 ('7 Equator S/H Mercury 19 (near, 0.0277%)', lambda I: eqr(I,'Mercury','S/H','19','near')),
 ('8 sky Sedna -> J Algol* (corrected): star (not listed)', lambda I: _nostar(I) and _pt(I,'S','Sedna')),
 ('9 Marquand (P11) J Ketu–Jupiter close (RA 2.7736 Dec 0.1212)',
  lambda I: link(json.load(open(f'docs/classic/{RACE}/layer1/P11.json')),'J','J Jupiter','J Ketu',close=True)),
]
