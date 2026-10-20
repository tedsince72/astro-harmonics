"""11 more stars (Eddie, 20 Oct 2026): engine J2000 RA / Dec at J2000.0 vs the catalogue (within 0.02 deg); engine RA order of the 46."""
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(REPO, 'rebuild_kit')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import swisseph as swe
import celestial_bodies_swisseph as E
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe')); swe.set_topo(0, 51.5, 0)
CAT = {'Alpheratz': (2.097, 29.090), 'Algenib': (3.309, 15.184), 'Difda': (10.897, -17.987), 'Mirach': (17.433, 35.621),
       'Menkar': (45.570, 4.090), 'Phact': (84.912, -34.074), 'Adhara': (104.656, -28.972), 'Wezen': (107.098, -26.393),
       'Menkent': (211.671, -36.370), 'Unukalhai': (236.067, 6.426), 'Rasalhague': (263.734, 12.560)}
B = dict(E.BEHENIAN_STARS)
bad = 0
for x, (ra, dec) in CAT.items():
    r, nm, _ = swe.fixstar2_ut(B[x], 2451545.0, E._FLAG)
    d1, d2 = r[0] - ra, r[1] - dec
    ok = abs(d1) < 0.02 and abs(d2) < 0.02
    bad += not ok
    print(f'{x:12s} {nm:28s} {r[0]:11.6f} {r[1]:+10.6f}   cat {ra:8.3f} {dec:+8.3f}   dRA {d1:+.4f} dDec {d2:+.4f}  {"ok" if ok else "OFF"}')
EXPECT = ['Alpheratz', 'Algenib', 'Difda', 'Mirach', 'Hamal', 'Menkar', 'Algol', 'Pleiades', 'Aldebaran', 'Rigel', 'Capella', 'Bellatrix',
          'Phact', 'Betelgeuse', 'Sirius', 'Adhara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Praesepe', 'Regulus', 'Denebola', 'Algorab',
          'Spica', 'Alkaid', 'Menkent', 'Arcturus', 'Zubenelgenubi', 'Zubeneschamali', 'Alphecca', 'Unukalhai', 'Antares', 'Rasalhague',
          'Galactic Centre', 'Kaus Australis', 'Vega', 'Nunki', 'Altair', 'Deneb', 'Sadalsuud', 'Deneb Algedi', 'Sadalmelik', 'Fomalhaut',
          'Scheat', 'Markab']
era = {x: swe.fixstar2_ut(B[x], 2451545.0, E._FLAG)[0] for x in EXPECT}
order = sorted(EXPECT, key=lambda x: era[x][0])
print('engine order = Eddie\'s list:', order == EXPECT, '| all |Dec| <= 50:', all(abs(era[x][1]) <= 50 for x in EXPECT))
for a, b in zip(order, EXPECT):
    if a != b: print('  differs:', a, b)
print(', '.join(f'{x} {era[x][0]:.4f}' for x in order))
print('outside 0.02:', bad)
