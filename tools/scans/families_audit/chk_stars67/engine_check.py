"""20 more stars and the Orion Nebula Cluster (Eddie, 21 Oct 2026): engine J2000 RA / Dec at J2000.0 vs the catalogue (within 0.02 deg);
Mirfak |Dec| <= 50; engine RA order of the 67 vs Eddie's list."""
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(REPO, 'rebuild_kit')); sys.path.insert(0, os.path.join(REPO, 'tools'))
import swisseph as swe
import celestial_bodies_swisseph as E
swe.set_ephe_path(os.path.expanduser('~/astronomy-project/ephe')); swe.set_topo(0, 51.5, 0)
CAT = {'Ankaa': (6.571, -42.306), 'Al Rescha': (30.512, 2.764), 'Mirfak': (51.081, 49.861), 'El Nath': (81.573, 28.607),
       'Meissa': (83.784, 9.934), 'Alnilam': (84.053, -1.202), 'Murzim': (95.675, -17.956), 'Alhena': (99.428, 16.399),
       'Acubens': (134.622, 11.858), 'Alphard': (141.897, -8.659), 'Alkes': (164.944, -18.299), 'Zosma': (168.527, 20.524),
       'Vindemiatrix': (195.544, 10.959), 'Diadem': (197.497, 17.529), 'Ras Algethi': (258.662, 14.390), 'Aculeus': (265.083, -32.253),
       'Acumen': (268.463, -34.793), 'Facies': (279.100, -23.905), 'Rukbat': (290.972, -40.616), 'Sualocin': (309.910, 15.912),
       'Orion Nebula Cluster': (83.822, -5.391)}
B = dict(E.BEHENIAN_STARS)
bad = 0
for x, (ra, dec) in CAT.items():
    r, nm, _ = swe.fixstar2_ut(B[x], 2451545.0, E._FLAG)
    d1, d2 = r[0] - ra, r[1] - dec
    ok = abs(d1) < 0.02 and abs(d2) < 0.02
    bad += not ok
    print(f'{x:12s} {nm:28s} {r[0]:11.6f} {r[1]:+10.6f}   cat {ra:8.3f} {dec:+8.3f}   dRA {d1:+.4f} dDec {d2:+.4f}  {"ok" if ok else "OFF"}')
EXPECT = ['Alpheratz', 'Algenib', 'Ankaa', 'Difda', 'Mirach', 'Al Rescha', 'Hamal', 'Menkar', 'Algol', 'Mirfak', 'Pleiades', 'Aldebaran',
          'Rigel', 'Capella', 'Bellatrix', 'El Nath', 'Meissa', 'Orion Nebula Cluster', 'Alnilam', 'Phact', 'Betelgeuse', 'Murzim', 'Alhena', 'Sirius', 'Adhara',
          'Wezen', 'Castor', 'Procyon', 'Pollux', 'Praesepe', 'Acubens', 'Alphard', 'Regulus', 'Alkes', 'Zosma', 'Denebola', 'Algorab',
          'Vindemiatrix', 'Diadem', 'Spica', 'Alkaid', 'Menkent', 'Arcturus', 'Zubenelgenubi', 'Zubeneschamali', 'Alphecca', 'Unukalhai',
          'Antares', 'Ras Algethi', 'Rasalhague', 'Aculeus', 'Galactic Centre', 'Acumen', 'Kaus Australis', 'Facies', 'Vega', 'Nunki',
          'Rukbat', 'Altair', 'Sualocin', 'Deneb', 'Sadalsuud', 'Deneb Algedi', 'Sadalmelik', 'Fomalhaut', 'Scheat', 'Markab']
era = {x: swe.fixstar2_ut(B[x], 2451545.0, E._FLAG)[0] for x in EXPECT}
order = sorted(EXPECT, key=lambda x: era[x][0])
print('engine order = Eddie\'s list:', order == EXPECT, '| all |Dec| <= 50:', all(abs(era[x][1]) <= 50 for x in EXPECT),
      '| Mirfak Dec', f"{era['Mirfak'][1]:+.6f}")
for a, b in zip(order, EXPECT):
    if a != b: print('  differs:', a, b)
for a, b in (('Facies', 'Vega'), ('Meissa', 'Orion Nebula Cluster'), ('Orion Nebula Cluster', 'Alnilam'), ('Bellatrix', 'El Nath')):
    print(f'  closest pair {a} {era[a][0]:.4f} / {b} {era[b][0]:.4f}')
print(', '.join(f'{x} {era[x][0]:.4f}' for x in order))
print('outside 0.02:', bad)
