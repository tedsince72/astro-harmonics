from l1helpers import *
RACE = 'newbury_1350_20211126'
P = 'P09'   # 7 Not Available / 7 Stan Sheppard

def _pt(I, c, b): return next((p['ra'], p['dec']) for p in I['points'] if p['chart'] == c and p['body'] == b)
def _ra(I, x, y):
    a, b = _pt(I, *x.split()), _pt(I, *y.split()); return abs((a[0] - b[0] + 180) % 360 - 180)
def _dec(I, x, y): return abs(_pt(I, *x.split())[1] - _pt(I, *y.split())[1])
def _eq(I, c, b): return abs(_pt(I, c, b)[1])

CHECKS = [
 ('1 sky Mars on J Mars RA 0.2440 / Dec 1.1227: RA < 0.5 and Dec no whole/ninth, no return list in Layer 1 — not listed; values reproducible from points',
  lambda I: not any(m['chart'] == 'J' and m['body'] == 'Mars' for m in I['movement'])
            and abs(_ra(I, 'S Mars', 'J Mars') - 0.2440) < 0.0002 and abs(_dec(I, 'S Mars', 'J Mars') - 1.1227) < 0.0002),
 ('2 H Mars – J Mars RA 175.6178: not close, no whole/ninth — not listed (opposition idea dropped by Eddie); value reproducible',
  lambda I: not has_link(I, 'H Mars', 'J Mars', close=False) and abs(_ra(I, 'H Mars', 'J Mars') - 175.6178) < 0.0002),
 ('2 H Mars moved RA 175.8618: no whole/ninth — not listed; value reproducible',
  lambda I: not move(I, 'H', 'Mars', 'RA', '176') and abs(_ra(I, 'S Mars', 'H Mars') - 175.8618) < 0.0002),
 ('3 sky Vesta on J Mars Dec 0.0494: value < 0.5, not a strike — not listed; value reproducible from points',
  lambda I: not any(s['sky'] == 'Vesta' and s['target'] == 'J Mars' and s['plane'] == 'Dec' for s in I['strikes'])
            and abs(_dec(I, 'S Vesta', 'J Mars') - 0.0494) < 0.0002),
 ('4 Vesta same-body RA 7/3:10/7:10/3', lambda I: same(I, 'Vesta', 'RA', ['7/3', '10/7', '10/3'])),
 ('5 J Sun–Rahu close (RA 0.8829, Dec 0.3735)', lambda I: link(I, 'J', 'J Sun', 'J Rahu', close=True)),
 ('5 no sky body strikes both J Sun and J Rahu/Ketu',
  lambda I: not ({s['sky'] for s in I['strikes'] if s['target'] == 'J Sun'} & {s['sky'] for s in I['strikes'] if s['target'] in ('J Rahu', 'J Ketu')})),
 ('6 sky Makemake -> H Mars Dec 31/9', lambda I: strike(I, 'Makemake', 'H Mars', 'Dec', '31/9')),
 ('6 sky Pallas -> J Mars Dec 6', lambda I: strike(I, 'Pallas', 'J Mars', 'Dec', '6')),
 ('6 sky node -> J Mars RA 125/9 (RA folded: listed as sky Ketu 125/9, sky Rahu 1495/9)',
  lambda I: strike(I, 'Ketu', 'J Mars', 'RA', '125/9') and strike(I, 'Rahu', 'J Mars', 'RA', '1495/9')),
 ('7 Haumea same-body RA 5/2:7/2:7/5 (worst 0.125%)', lambda I: same(I, 'Haumea', 'RA', ['5/2', '7/2', '7/5'])),
 ('8 sky Mars–Neptune Dec 12', lambda I: sky(RACE, 'Mars–Neptune', 'Dec', '12')),
 ('R1 H Pallas–Juno RA 2', lambda I: ratio(I, 'H', 'Juno–Pallas', 'RA', '2')),
 ('R1 shared Pallas–Juno RA (H 138.2873 / J 138.8180, 0.38%)', lambda I: shared(I, 'Juno–Pallas', 'RA')),
 ('R2 J Chiron–Transpluto Dec 5', lambda I: ratio(I, 'J', 'Chiron–Transpluto', 'Dec', '5')),
 ('R2 Chiron–Transpluto RA jockey/horse 21/8 (0.0114%): natal H:J ratio without sky is not a Layer 1 item (shared needs <= 0.5% equal) — not listed; values reproducible',
  lambda I: not shared(I, 'Chiron–Transpluto', 'RA') and not pset(I, 'Chiron–Transpluto', 'RA')
            and abs(_ra(I, 'H Chiron', 'H Transpluto') / _ra(I, 'J Chiron', 'J Transpluto') / (21 / 8) - 1) < 0.0002),
 ('R3 H Saturn–Transpluto GC 5/3', lambda I: ratio(I, 'H', 'Saturn–Transpluto', 'GC', '5/3')),
 ('R4 J Haumea–Pallas Dec 23/9', lambda I: ratio(I, 'J', 'Haumea–Pallas', 'Dec', '23/9')),
 ('R4 H Haumea–Pallas GC 16/7 (0.0077% > 0.005% ratio tol) — not listed', lambda I: not ratio(I, 'H', 'Haumea–Pallas', 'GC', '16/7')),
 ('R5 sky Pallas -> J Mars Dec 6', lambda I: strike(I, 'Pallas', 'J Mars', 'Dec', '6')),
 ('R6 H Sun Equator 15', lambda I: eqpt(I, 'H', 'Sun', '15')),
 ('R6 Equator S/H Sun 7/5 (0.035% > 0.03% near band) — not listed; both Equator values present',
  lambda I: not any(e['body'] == 'Sun' and e['pair'] == 'S/H' for e in I['eq_ratios'])
            and abs(_eq(I, 'S', 'Sun') / _eq(I, 'H', 'Sun') / 1.4 - 1) < 0.0005),
]
