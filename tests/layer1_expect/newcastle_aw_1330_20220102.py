from l1helpers import *
from l1helpers import _pm
RACE = 'newcastle_aw_1330_20220102'
P = 'P09'   # 5 Venturous / 5 Connor Beasley

def _pt(I, c, b): return next((p['ra'], p['dec']) for p in I['points'] if p['chart'] == c and p['body'] == b)
def _ra(I, x, y):
    a, b = _pt(I, *x.split()), _pt(I, *y.split()); return abs((a[0] - b[0] + 180) % 360 - 180)
def _dec(I, x, y): return abs(_pt(I, *x.split())[1] - _pt(I, *y.split())[1])
def _flat(I, x, y): return (_ra(I, x, y) ** 2 + _dec(I, x, y) ** 2) ** 0.5
def _near(v, p, q, tol): return abs(v - p / q) / (p / q) <= tol

CHECKS = [
 ('1 H Rahu – J Rahu RA 1.8697 (node field)', lambda I: abs(I['node']['rahu_rahu_ra'] - 1.8697) < 0.0002),
 ('1 H Rahu – J Rahu not a close cross link (RA 1.87 >= 1.5, Dec 0.52 >= 0.3; GC 1.8584 is no whole/ninth) — not listed; RA in node field',
  lambda I: not has_link(I, 'H Rahu', 'J Rahu', close=False) and abs(_dec(I, 'H Rahu', 'J Rahu') - 0.5165) < 0.0002),
 ('2 shared Rahu–Sedna GC', lambda I: shared(I, 'Rahu–Sedna', 'GC')),
 ('2 shared Mars–Rahu GC', lambda I: shared(I, 'Mars–Rahu', 'GC')),
 ('3 H Neptune–Rahu RA 111', lambda I: link(I, 'H', 'H Neptune', 'H Rahu', 'RA', '111')),
 ('4 sky Rahu–Sedna RA 0.2183: closeness < 0.5, no sky-pair closeness list in Layer 1 — not listed; reproducible from sky points',
  lambda I: not sky(RACE, 'Rahu–Sedna', 'RA', '0') and abs(_ra(I, 'S Rahu', 'S Sedna') - 0.2183) < 0.0002),
 ('5 J Gonggong–Transpluto RA 175', lambda I: link(I, 'J', 'J Gonggong', 'J Transpluto', 'RA', '175')),
 ('5 sky Chiron -> J Gonggong RA 36', lambda I: strike(I, 'Chiron', 'J Gonggong', 'RA', '36')),
 ('5 sky Chiron -> J Transpluto RA 139', lambda I: strike(I, 'Chiron', 'J Transpluto', 'RA', '139')),
 ('5 sky Quaoar -> J Gonggong RA 55', lambda I: strike(I, 'Quaoar', 'J Gonggong', 'RA', '55')),
 ('5 sky Quaoar -> J Transpluto RA 130', lambda I: strike(I, 'Quaoar', 'J Transpluto', 'RA', '130')),
 ('6 Mercury–Orcus Dec 3-way (S:H 33/5, J:H 32/3, p > 30; S:J not simple) — not listed as pair set or ratio',
  lambda I: not pset(I, 'Mercury–Orcus', 'Dec') and not any(_pm('Mercury–Orcus', r['pair']) and r['plane'] == 'Dec' for r in I['ratios'])
            and _near(_dec(I, 'S Mercury', 'S Orcus') / _dec(I, 'H Mercury', 'H Orcus'), 33, 5, 0.00001)),
 ('7 J Jupiter–Uranus Flat 8/7', lambda I: ratio(I, 'J', 'Jupiter–Uranus', 'Flat', '8/7')),
 ('7 H Chiron–Makemake Dec 16/9', lambda I: ratio(I, 'H', 'Chiron–Makemake', 'Dec', '16/9')),
 ('7 J Uranus–Transpluto GC 4/3', lambda I: ratio(I, 'J', 'Uranus–Transpluto', 'GC', '4/3')),
 ('7 H Pluto–Ceres GC 4/3', lambda I: ratio(I, 'H', 'Pluto–Ceres', 'GC', '4/3')),
 ('8 no fast sky body (Sun..Mars) strike on H Rahu / J Rahu in RA or Dec',
  lambda I: not any(s['target'] in ('H Rahu', 'J Rahu') and s['plane'] in ('RA', 'Dec') and s['sky'] in ('Sun', 'Mercury', 'Venus', 'Mars') for s in I['strikes'])),
 ('D1 Equator S/H Sun 12 tight', lambda I: eqr(I, 'Sun', 'S/H', '12', 'tight')),
 ('D2 cross H Sun–J Orcus close (Dec 0.0383)', lambda I: link(I, 'cross', 'H Sun', 'J Orcus', close=True)),
 ('D2 H Sun–Venus close (RA 0.2027)', lambda I: link(I, 'H', 'H Sun', 'H Venus', close=True)),
 ('D2 J Sun–Mercury close (RA 1.1038)', lambda I: link(I, 'J', 'J Sun', 'J Mercury', close=True)),
 ('D2 Equator S/J Orcus 13/2 near (0.0169%)', lambda I: eqr(I, 'Orcus', 'S/J', '13/2', 'near')),
 ('D3 H Saturn–Juno Flat 19/6', lambda I: ratio(I, 'H', 'Saturn–Juno', 'Flat', '19/6')),
 ('D3 H Juno–Eris RA 6/5 (0.0087% > 0.005% ratio tol) — not listed; value reproducible from points',
  lambda I: not ratio(I, 'H', 'Juno–Eris', 'RA', '6/5') and _near(_ra(I, 'S Juno', 'S Eris') / _ra(I, 'H Juno', 'H Eris'), 6, 5, 0.0001)
            or not ratio(I, 'H', 'Juno–Eris', 'RA', '6/5') and _near(_ra(I, 'H Juno', 'H Eris') / _ra(I, 'S Juno', 'S Eris'), 6, 5, 0.0001)),
 ('D3 J Pallas–Juno GC 23/9', lambda I: ratio(I, 'J', 'Pallas–Juno', 'GC', '23/9')),
 ('D3 J Juno–Ketu RA 13/4 (0.0056% > 0.005% ratio tol) — not listed; value reproducible from points',
  lambda I: not ratio(I, 'J', 'Juno–Ketu', 'RA', '13/4') and (_near(_ra(I, 'S Juno', 'S Ketu') / _ra(I, 'J Juno', 'J Ketu'), 13, 4, 0.0001)
            or _near(_ra(I, 'J Juno', 'J Ketu') / _ra(I, 'S Juno', 'S Ketu'), 13, 4, 0.0001))),
 ('D3 J Pallas–Juno Dec 9/7 (0.0099% > 0.005% ratio tol) — not listed; value reproducible from points',
  lambda I: not ratio(I, 'J', 'Pallas–Juno', 'Dec', '9/7') and (_near(_dec(I, 'S Pallas', 'S Juno') / _dec(I, 'J Pallas', 'J Juno'), 9, 7, 0.00015)
            or _near(_dec(I, 'J Pallas', 'J Juno') / _dec(I, 'S Pallas', 'S Juno'), 9, 7, 0.00015))),
 ('D3 H Mercury–Juno close (Dec 0.0945)', lambda I: link(I, 'H', 'H Mercury', 'H Juno', close=True)),
 ('D4 H Venus–Chiron Flat 16/5', lambda I: ratio(I, 'H', 'Venus–Chiron', 'Flat', '16/5')),
 ('D4 J Venus–Chiron Flat 23/7 (0.0057% > 0.005% ratio tol) — not listed; value reproducible from points',
  lambda I: not ratio(I, 'J', 'Venus–Chiron', 'Flat', '23/7') and _near(_flat(I, 'S Venus', 'S Chiron') / _flat(I, 'J Venus', 'J Chiron'), 23, 7, 0.0001)),
 ('D5 H Pluto moved RA 16', lambda I: move(I, 'H', 'Pluto', 'RA', '16')),
 ('D5 H Ceres moved RA 30', lambda I: move(I, 'H', 'Ceres', 'RA', '30')),
 ('D5 cross H Ceres–J Mars close (RA 0.1439)', lambda I: link(I, 'cross', 'H Ceres', 'J Mars', close=True)),
]
