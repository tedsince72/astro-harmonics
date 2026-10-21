"""check67_common.py (independent checker, 21 Oct 2026): constant lists for the 67-star check, written out by hand from Eddie's spec
(no import of tools/jupiter_tables.py)."""
import os
S = '/private/tmp/claude-501/-Users-eddieplace-astro-harmonics/3d86481b-e19f-4be4-91e4-da248144d5be/scratchpad'
S67 = S + '/s67'
NEW21 = ['Ankaa', 'Al Rescha', 'Mirfak', 'El Nath', 'Meissa', 'Orion Nebula Cluster', 'Alnilam', 'Murzim', 'Alhena', 'Acubens', 'Alphard',
         'Alkes', 'Zosma', 'Vindemiatrix', 'Diadem', 'Ras Algethi', 'Aculeus', 'Acumen', 'Facies', 'Rukbat', 'Sualocin']
CAT = {'Ankaa': (6.571, -42.306), 'Al Rescha': (30.512, 2.764), 'Mirfak': (51.081, 49.861), 'El Nath': (81.573, 28.607),
       'Meissa': (83.784, 9.934), 'Orion Nebula Cluster': (83.822, -5.391), 'Alnilam': (84.053, -1.202), 'Murzim': (95.675, -17.956),
       'Alhena': (99.428, 16.399), 'Acubens': (134.622, 11.858), 'Alphard': (141.897, -8.659), 'Alkes': (164.944, -18.299),
       'Zosma': (168.527, 20.524), 'Vindemiatrix': (195.544, 10.959), 'Diadem': (197.497, 17.529), 'Ras Algethi': (258.662, 14.390),
       'Aculeus': (265.083, -32.253), 'Acumen': (268.463, -34.793), 'Facies': (279.100, -23.905), 'Rukbat': (290.972, -40.616),
       'Sualocin': (309.910, 15.912)}
STARS67 = ['Alpheratz', 'Algenib', 'Ankaa', 'Difda', 'Mirach', 'Al Rescha', 'Hamal', 'Menkar', 'Algol', 'Mirfak', 'Pleiades', 'Aldebaran',
           'Rigel', 'Capella', 'Bellatrix', 'El Nath', 'Meissa', 'Orion Nebula Cluster', 'Alnilam', 'Phact', 'Betelgeuse', 'Murzim', 'Alhena',
           'Sirius', 'Adhara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Praesepe', 'Acubens', 'Alphard', 'Regulus', 'Alkes', 'Zosma',
           'Denebola', 'Algorab', 'Vindemiatrix', 'Diadem', 'Spica', 'Alkaid', 'Menkent', 'Arcturus', 'Zubenelgenubi', 'Zubeneschamali',
           'Alphecca', 'Unukalhai', 'Antares', 'Ras Algethi', 'Rasalhague', 'Aculeus', 'Galactic Centre', 'Acumen', 'Kaus Australis',
           'Facies', 'Vega', 'Nunki', 'Rukbat', 'Altair', 'Sualocin', 'Deneb', 'Sadalsuud', 'Deneb Algedi', 'Sadalmelik', 'Fomalhaut',
           'Scheat', 'Markab']
STARS46 = [s for s in STARS67 if s not in NEW21]
OLD_STARS = ['Algol', 'Pleiades', 'Aldebaran', 'Capella', 'Sirius', 'Procyon', 'Regulus', 'Alkaid', 'Algorab', 'Spica', 'Arcturus',
             'Alphecca', 'Antares', 'Vega', 'Deneb Algedi', 'Fomalhaut', 'Rigel', 'Betelgeuse', 'Polaris', 'Castor', 'Altair', 'Bellatrix',
             'Galactic Centre']
# SKY STARS orientation: old STARS order without Polaris, then the new stars in RA order
PAIR_ORDER = [s for s in OLD_STARS if s != 'Polaris'] + [s for s in STARS67 if s not in OLD_STARS]
BODIES = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas',
          'Juno', 'Vesta', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto', 'Rahu', 'Ketu']
assert len(STARS67) == 67 and len(set(STARS67)) == 67 and len(STARS46) == 46 and set(NEW21) <= set(STARS67) and len(PAIR_ORDER) == 67
import re
# regex: a name of one of the 21 as a whole word (none of the 21 is a prefix-trap like Deneb / Deneb Algedi)
NEWRX = re.compile(r'(?<![A-Za-z])(' + '|'.join(re.escape(s) for s in sorted(NEW21, key=len, reverse=True)) + r')(?![A-Za-z])')
