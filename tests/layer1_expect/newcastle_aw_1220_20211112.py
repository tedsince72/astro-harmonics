from l1helpers import *
RACE = 'newcastle_aw_1220_20211112'
P = 'P03'   # 2 Sir Chauvelin / 2 Paul Mulrennan

_STARS = ('Deneb', 'Alphecca', 'Spica', 'Aldebaran', 'Alkaid', 'Pleiades')
def _nostar(I): return not any(s in json.dumps(I) for s in _STARS)
def _pt(I, c, b): return next(p for p in I['points'] if p['chart'] == c and p['body'] == b)
def _ra(I, a, b): d = abs(_pt(I, *a)['ra'] - _pt(I, *b)['ra']) % 360; return min(d, 360 - d)
def _dec(I, a, b): return abs(_pt(I, *a)['dec'] - _pt(I, *b)['dec'])
def _nostrike(I, s, t, pl): return not any(x['sky'] == s and x['target'] == t and x['plane'] == pl for x in I['strikes'])

CHECKS = [
 ('1 sky Gonggong -> J Uranus RA 94', lambda I: strike(I,'Gonggong','J Uranus','RA','94')),
 ('1 sky Gonggong -> J Uranus Dec 83/9', lambda I: strike(I,'Gonggong','J Uranus','Dec','83/9')),
 ('2 sky Deneb Algedi* -> H Pluto: star (not listed)', lambda I: _nostar(I)),
 ('3 sky Gonggong -> H Chiron RA 0.0674: value < 0.5 (not a strike); points listed',
  lambda I: _nostrike(I,'Gonggong','H Chiron','RA') and abs(_ra(I,('S','Gonggong'),('H','Chiron')) - 0.0674) < 0.001),
 ('3 sky Gonggong -> H Neptune Dec 0.0950: value < 0.5 (not a strike); points listed',
  lambda I: _nostrike(I,'Gonggong','H Neptune','Dec') and abs(_dec(I,('S','Gonggong'),('H','Neptune')) - 0.0950) < 0.001),
 ('4 H Neptune–Gonggong close (RA 1.3220)', lambda I: link(I,'H','H Neptune','H Gonggong',close=True)),
 ('4 J Ketu–Gonggong close (Dec 0.1107)', lambda I: link(I,'J','J Ketu','J Gonggong',close=True)),
 ('4 J Ketu–Gonggong Dec 1/9: value < 0.5 (no number listed; close link is)',
  lambda I: not link(I,'J','J Ketu','J Gonggong','Dec','1/9') and link(I,'J','J Ketu','J Gonggong',close=True)),
 ('4 J Neptune–Gonggong close (Dec 0.1822)', lambda I: link(I,'J','J Neptune','J Gonggong',close=True)),
 ('4 J Neptune–Ketu close (Dec 0.2929)', lambda I: link(I,'J','J Neptune','J Ketu',close=True)),
 ('5 Gonggong same-body RA 6:7:7/6 (worst 0.0849%)', lambda I: same(I,'Gonggong','RA',['6','7','7/6'])),
 ('6 sky Uranus -> H Venus RA 0.2371: value < 0.5 (not a strike); points listed',
  lambda I: _nostrike(I,'Uranus','H Venus','RA') and abs(_ra(I,('S','Uranus'),('H','Venus')) - 0.2371) < 0.001),
 ('7 cross H Pluto–J Juno (close, RA 0.0462)', lambda I: link(I,'cross','H Pluto','J Juno',close=True)),
 ('8 3-way RA Alphecca*–Mars: star partner (not listed)', lambda I: _nostar(I) and not pset(I,'Mars–Alphecca','RA')),
 ('9 (corrected) J Sedna–Eris 14.33731: 129/9 off 0.004, not a ninth; soak is mostly Spica* (not listed)',
  lambda I: not any(l['kind']=='J' and {l['a'],l['b']}=={'J Sedna','J Eris'} and any(n['num']=='129/9' for n in l['nums'].values()) for l in I['links'])),
 ('9 (corrected) sky Ceres–Sedna 8.43336: 76/9 off 0.011, not a sky number; soak is mostly Aldebaran* (not listed)',
  lambda I: not sky(RACE,'Ceres–Sedna','RA','76/9') and not sky(RACE,'Ceres–Sedna','Dec','76/9')),
 ('R J Gonggong–Uranus Dec sky/natal 18', lambda I: ratio(I,'J','Gonggong–Uranus','Dec','18')),
 ('R J Neptune–Rahu GC natal/sky 9/4', lambda I: ratio(I,'J','Neptune–Rahu','GC','9/4')),
 ('R H Sun–Neptune RA 47/9 (0.0053%): p > 30 and outside 0.005% (not listed); best p<=30 is 26/5',
  lambda I: not ratio(I,'H','Sun–Neptune','RA','47/9')),
 ('R H Mercury–Chiron GC 47/9 (0.0040%): p > 30 (not listed)', lambda I: not ratio(I,'H','Mercury–Chiron','GC','47/9')),
 ('R J Gonggong–Orcus RA 7/6 (0.0137%): outside ratio 0.005% (not listed)', lambda I: not ratio(I,'J','Gonggong–Orcus','RA','7/6')),
 ('R Equator S/J Ceres 7/4 tight (0.008%)', lambda I: eqr(I,'Ceres','S/J','7/4','tight')),
 ('R no whole/ninth Equator values in S, H or J', lambda I: not any(p['eq_num'] for p in I['points'])),
]
