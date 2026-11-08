# Stage 3 back-test

Races: 24 (results file 26; no rules output for 20211204_sandown_1425, 20240608_beverley_1405).
fired = races with a pick; only pick = races with exactly one pick; alone = one pick and it won; chance from field sizes.
In-sample = races the rule was seen on or written from (rules.json); test = every other race. Only the test races are evidence.

## Test races

| Rule | Name | races | fired | picks | winners (chance) | 1st or 2nd (chance) | only pick | alone |
|---|---|---|---|---|---|---|---|---|
| R25 | Pallas reached twice | 24 | 7 | 8 | 1 (1.3) | 4 (2.8) | 6 | 1 |
| R28 | Chiron to Jupiter, lit by Sun / Moon | 24 | 6 | 8 | 1 (1.3) | 3 (2.8) | 4 | 0 |
| R1b | Moon to X, sky X to Jupiter | 24 | 13 | 19 | 2 (3.4) | 7 (6.8) | 8 | 1 |
| R7 | Line star on own Jupiter and on one body both charts | 24 | 14 | 22 | 0 (3.6) | 4 (7.7) | 7 | 0 |
| R26 | Royal line star on own Jupiter | 24 | 9 | 13 | 3 (2.1) | 4 (4.2) | 6 | 1 |
| R40 | Node axis | 24 | 7 | 9 | 0 (1.5) | 3 (2.9) | 5 | 0 |
| R42 | Moon on a same body | 24 | 20 | 32 | 3 (5.4) | 10 (11.0) | 9 | 0 |
| R1 | Sun / Moon on one body both charts, sky X to Jupiter | 24 | 3 | 3 | 0 (0.5) | 0 (0.9) | 3 | 0 |
| B1 | Natal body on a strong line star (filter) | 6 | 5 | 11 | 2 (1.7) | 4 (3.3) | 3 | 0 |
| B2 | Top natal body on a strong line star | 9 | 7 | 7 | 2 (1.2) | 4 (2.4) | 7 | 2 |
| B3 | Version 4 | 8 | 6 | 6 | 1 (0.9) | 3 (1.9) | 6 | 1 |
| B4 | Same body, clear lead | 6 | 3 | 3 | 0 (0.5) | 2 (1.0) | 3 | 0 |
| B5 | Same body in both planes | 6 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| B6 | Same body on both charts | 6 | 2 | 2 | 0 (0.3) | 1 (0.7) | 2 | 0 |
| B7 | Most sky bodies onto the jockey's Jupiter | 23 | 22 | 27 | 7 (4.4) | 13 (9.0) | 18 | 5 |
| B8 | One line star on the most natal bodies | 23 | 23 | 47 | 9 (7.9) | 18 (15.9) | 10 | 3 |
| B9 | Jupiter and two of its line stars on one natal body | 23 | 9 | 14 | 3 (2.3) | 5 (4.7) | 6 | 0 |
| B10 | Sun and two of its line stars on one natal body | 23 | 14 | 24 | 9 (3.8) | 14 (8.1) | 10 | 6 |
| B11 | Moon and two of its line stars on one natal body | 23 | 13 | 31 | 8 (5.2) | 12 (10.6) | 4 | 2 |
| B12 | Same body and two line stars on it | 23 | 14 | 24 | 8 (4.2) | 11 (8.4) | 8 | 3 |

## In-sample races

| Rule | Name | races | fired | picks | winners (chance) | 1st or 2nd (chance) | only pick | alone |
|---|---|---|---|---|---|---|---|---|
| R25 | Pallas reached twice | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| R28 | Chiron to Jupiter, lit by Sun / Moon | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| R1b | Moon to X, sky X to Jupiter | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| R7 | Line star on own Jupiter and on one body both charts | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| R26 | Royal line star on own Jupiter | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| R40 | Node axis | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| R42 | Moon on a same body | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| R1 | Sun / Moon on one body both charts, sky X to Jupiter | 0 | 0 | 0 | 0 (0.0) | 0 (0.0) | 0 | 0 |
| B1 | Natal body on a strong line star (filter) | 18 | 14 | 48 | 11 (8.2) | 18 (16.9) | 2 | 0 |
| B2 | Top natal body on a strong line star | 15 | 12 | 12 | 4 (2.1) | 5 (4.3) | 12 | 4 |
| B3 | Version 4 | 16 | 13 | 13 | 6 (2.3) | 7 (4.8) | 13 | 6 |
| B4 | Same body, clear lead | 18 | 6 | 6 | 2 (1.1) | 4 (2.2) | 6 | 2 |
| B5 | Same body in both planes | 18 | 4 | 4 | 1 (0.6) | 2 (1.3) | 4 | 1 |
| B6 | Same body on both charts | 18 | 3 | 4 | 2 (0.7) | 2 (1.4) | 2 | 1 |
| B7 | Most sky bodies onto the jockey's Jupiter | 1 | 1 | 1 | 1 (0.2) | 1 (0.5) | 1 | 1 |
| B8 | One line star on the most natal bodies | 1 | 1 | 1 | 1 (0.2) | 1 (0.4) | 1 | 1 |
| B9 | Jupiter and two of its line stars on one natal body | 1 | 1 | 1 | 1 (0.1) | 1 (0.2) | 1 | 1 |
| B10 | Sun and two of its line stars on one natal body | 1 | 1 | 2 | 0 (0.2) | 0 (0.5) | 0 | 0 |
| B11 | Moon and two of its line stars on one natal body | 1 | 1 | 2 | 0 (0.2) | 0 (0.5) | 0 | 0 |
| B12 | Same body and two line stars on it | 1 | 1 | 1 | 0 (0.1) | 0 (0.2) | 1 | 0 |

## All races

| Rule | Name | races | fired | picks | winners (chance) | 1st or 2nd (chance) | only pick | alone |
|---|---|---|---|---|---|---|---|---|
| R25 | Pallas reached twice | 24 | 7 | 8 | 1 (1.3) | 4 (2.8) | 6 | 1 |
| R28 | Chiron to Jupiter, lit by Sun / Moon | 24 | 6 | 8 | 1 (1.3) | 3 (2.8) | 4 | 0 |
| R1b | Moon to X, sky X to Jupiter | 24 | 13 | 19 | 2 (3.4) | 7 (6.8) | 8 | 1 |
| R7 | Line star on own Jupiter and on one body both charts | 24 | 14 | 22 | 0 (3.6) | 4 (7.7) | 7 | 0 |
| R26 | Royal line star on own Jupiter | 24 | 9 | 13 | 3 (2.1) | 4 (4.2) | 6 | 1 |
| R40 | Node axis | 24 | 7 | 9 | 0 (1.5) | 3 (2.9) | 5 | 0 |
| R42 | Moon on a same body | 24 | 20 | 32 | 3 (5.4) | 10 (11.0) | 9 | 0 |
| R1 | Sun / Moon on one body both charts, sky X to Jupiter | 24 | 3 | 3 | 0 (0.5) | 0 (0.9) | 3 | 0 |
| B1 | Natal body on a strong line star (filter) | 24 | 19 | 59 | 13 (9.9) | 22 (20.3) | 5 | 0 |
| B2 | Top natal body on a strong line star | 24 | 19 | 19 | 6 (3.2) | 9 (6.6) | 19 | 6 |
| B3 | Version 4 | 24 | 19 | 19 | 7 (3.2) | 10 (6.6) | 19 | 7 |
| B4 | Same body, clear lead | 24 | 9 | 9 | 2 (1.6) | 6 (3.2) | 9 | 2 |
| B5 | Same body in both planes | 24 | 4 | 4 | 1 (0.6) | 2 (1.3) | 4 | 1 |
| B6 | Same body on both charts | 24 | 5 | 6 | 2 (1.0) | 3 (2.1) | 4 | 1 |
| B7 | Most sky bodies onto the jockey's Jupiter | 24 | 23 | 28 | 8 (4.7) | 14 (9.5) | 19 | 6 |
| B8 | One line star on the most natal bodies | 24 | 24 | 48 | 10 (8.1) | 19 (16.3) | 11 | 4 |
| B9 | Jupiter and two of its line stars on one natal body | 24 | 10 | 15 | 4 (2.5) | 6 (4.9) | 7 | 1 |
| B10 | Sun and two of its line stars on one natal body | 24 | 15 | 26 | 9 (4.1) | 14 (8.6) | 10 | 6 |
| B11 | Moon and two of its line stars on one natal body | 24 | 14 | 33 | 8 (5.4) | 12 (11.1) | 4 | 2 |
| B12 | Same body and two line stars on it | 24 | 15 | 25 | 8 (4.3) | 11 (8.7) | 9 | 3 |


## Per rule, every race

### R25 Pallas reached twice
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Athmad (won); winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): none; winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): none; winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): Gold Des Bois (4); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Red Tornado (6); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): Boss Man Fred (2); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Hell Red (2); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): Leader Crik (3), Barnpark (5); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Lyssenko (2); winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### R28 Chiron to Jupiter, lit by Sun / Moon
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Pallas Dancer (2); winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Supakalanistic (5), Eleven Eleven (4); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): none; winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): King D'argent (5); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): none; winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): Thomas Darby (5), Wholestone (won); winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Manvers House (6); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): none; winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): Motazzen (2); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### R1b Moon to X, sky X to Jupiter
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Athmad (won); winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Supakalanistic (5); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Eclair D'Ainay (2), Cedar Hill (5); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): none; winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): none; winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Winds Of Fire (5), Brian Boranha (4); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): Wise Eagle (4), Onesmoothoperator (2); winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): Fransham (4), Nelson River (won); winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): Top Ville Ben (2); winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): Blazing Hot (2); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Breaking Waves (7); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): Avide (4); winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Bucephalus (3); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2), Mirabad (3), Daytime Dreaming (5); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Ted The Thief (5); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### R7 Line star on own Jupiter and on one body both charts
- 20210402_lingfield_aw_1435 (test, 6 ran): Shimmering Dawn (2); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Supakalanistic (5), Eleven Eleven (4); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): Une De La Seniere (3), Method Madness (6); winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Financier (7); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Itchy Feet (4); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): The Big Bite (2), Fransham (6), Gold Des Bois (4); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): none; winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Brian Boranha (4); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): Wise Eagle (4), Onesmoothoperator (2); winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): James Watt (4), Tathmeen (3); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): Vocaliser (5), Thundersockssundae (3); winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): Dixie Mafia (4); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Star Of Guiting (5); winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): My Own Lovely Lee (3), Pawpaw (6); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): C'Mon So (2); winner Defence Witness

### R26 Royal line star on own Jupiter
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Protected Guest (2); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): Method Madness (6); winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Financier (7), One True King (4), Beaufort West (6); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Lieutenant Rocco (6), Two For Gold (won); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): none; winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Carn A Chlamain (7); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): Resumption (5); winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): Thomas Darby (5); winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): James Watt (4), Gowanlad (won); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): none; winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): Fire Flyer (won); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### R40 Node axis
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Beating All (5); winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): none; winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Eclair D'Ainay (2), Beaufort West (6); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): none; winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Carn A Chlamain (7); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Almazhar Garde (2), Winds Of Fire (5); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): Nickolson (2); winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Grangeclare Glory (4); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): none; winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): Walk Tall (7); winner Defence Witness

### R42 Moon on a same body
- 20210402_lingfield_aw_1435 (test, 6 ran): Fizzy Feet (4), Pholas (won); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Beating All (5); winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Supakalanistic (5), Trevolli (won); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): Wildfire Warrior (7), Fanamix (4); winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Financier (7), Le Ligerien (3); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Itchy Feet (4); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): The Big Bite (2), Gold Des Bois (4); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): Western Victory (3); winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): none; winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Almazhar Garde (2); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): Boss Man Fred (2), Mr Washington (6); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): Alablaq (5), Tathmeen (3); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Manvers House (6); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): Edmond Dantes (6); winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): Watery Borren (3), Aqua Bleu (2); winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): Leader Crik (3); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Dedicated Hero (6), Lyssenko (2), King Ulanda (7); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2), Brookie (4); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): Motazzen (2); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Pawpaw (6); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): Defence Witness (won), Aill Dubh (3); winner Defence Witness

### R1 Sun / Moon on one body both charts, sky X to Jupiter
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): none; winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Cedar Hill (5); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): none; winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): none; winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Winds Of Fire (5); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Breaking Waves (7); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): none; winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B1 Natal body on a strong line star (filter)
- 20210402_lingfield_aw_1435 (test, 6 ran): Arafi (3), Fizzy Feet (4), Indie Angel (5), Pholas (won); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Pallas Dancer (2); winner Athmad
- 20220108_lingfield_aw_1345 (in-sample, 5 ran): Protected Guest (2), Creationist (3), Eleven Eleven (4); winner Trevolli
- 20220110_ludlow_1515 (in-sample, 7 ran): Method Madness (6); winner Java Point
- 20220121_lingfield_1350 (in-sample, 7 ran): Eclair D'Ainay (2), Financier (7), Frero Banbou (won), One True King (4), Cedar Hill (5), Le Ligerien (3), Beaufort West (6); winner Frero Banbou
- 20220123_lingfield_1500 (in-sample, 6 ran): Bristol De Mai (3), Dashel Drasher (2), Master Tommytucker (5), Itchy Feet (4), Lieutenant Rocco (6), Two For Gold (won); winner Two For Gold
- 20220128_doncaster_1315 (in-sample, 7 ran): Funambule Sivola (won), King D'argent (5), Fransham (6), Gold Des Bois (4); winner Funambule Sivola
- 20220129_doncaster_1410 (in-sample, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (in-sample, 7 ran): Flying Instructor (4), Chase The Dollar (won), Deluxe Music (2), Flamingo Rose (5); winner Chase The Dollar
- 20220214_catterick_1515 (in-sample, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (in-sample, 6 ran): Sir Chauvelin (won), Alba Rose (6), Wise Eagle (4), Onesmoothoperator (2), Aced It (3); winner Sir Chauvelin
- 20220217_leicester_1445 (in-sample, 4 ran): Fransham (4), Nelson River (won); winner Nelson River
- 20220219_haydock_1405 (in-sample, 6 ran): Third Wind (3), Thomas Darby (5), Emitom (4), Wholestone (won), Molly Ollys Wishes (6); winner Wholestone
- 20220223_doncaster_1600 (in-sample, 6 ran): Boss Man Fred (2); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (in-sample, 5 ran): Alablaq (5), Gowanlad (won), Tathmeen (3); winner Gowanlad
- 20220309_fontwell_1440 (in-sample, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (in-sample, 6 ran): Peak Time (won), Thundersockssundae (3); winner Peak Time
- 20261106_aintree_1240 (in-sample, 4 ran): Watery Borren (3), Aqua Bleu (2), Risky Obsession (won); winner Risky Obsession
- 20261106_aintree_1315 (in-sample, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (in-sample, 7 ran): Manuelito (4), All In You (won); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): Fire Flyer (won), Donnie Azoff (7), He's A Latchico (8), So You Know (4); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Pawpaw (6); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B2 Top natal body on a strong line star
- 20210402_lingfield_aw_1435 (test, 6 ran): Pholas (won); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Pallas Dancer (2); winner Athmad
- 20220108_lingfield_aw_1345 (in-sample, 5 ran): Creationist (3); winner Trevolli
- 20220110_ludlow_1515 (in-sample, 7 ran): Method Madness (6); winner Java Point
- 20220121_lingfield_1350 (in-sample, 7 ran): Financier (7); winner Frero Banbou
- 20220123_lingfield_1500 (in-sample, 6 ran): Master Tommytucker (5); winner Two For Gold
- 20220128_doncaster_1315 (in-sample, 7 ran): Funambule Sivola (won); winner Funambule Sivola
- 20220129_doncaster_1410 (in-sample, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (in-sample, 7 ran): Flying Instructor (4); winner Chase The Dollar
- 20220214_catterick_1515 (in-sample, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (in-sample, 6 ran): Wise Eagle (4); winner Sir Chauvelin
- 20220217_leicester_1445 (in-sample, 4 ran): Nelson River (won); winner Nelson River
- 20220219_haydock_1405 (in-sample, 6 ran): Thomas Darby (5); winner Wholestone
- 20220223_doncaster_1600 (in-sample, 6 ran): Boss Man Fred (2); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (in-sample, 5 ran): Gowanlad (won); winner Gowanlad
- 20220309_fontwell_1440 (in-sample, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (in-sample, 6 ran): Peak Time (won); winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): Risky Obsession (won); winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Manuelito (4); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): So You Know (4); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Pawpaw (6); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B3 Version 4
- 20210402_lingfield_aw_1435 (test, 6 ran): Pholas (won); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Pallas Dancer (2); winner Athmad
- 20220108_lingfield_aw_1345 (in-sample, 5 ran): Creationist (3); winner Trevolli
- 20220110_ludlow_1515 (in-sample, 7 ran): Method Madness (6); winner Java Point
- 20220121_lingfield_1350 (in-sample, 7 ran): Financier (7); winner Frero Banbou
- 20220123_lingfield_1500 (in-sample, 6 ran): Two For Gold (won); winner Two For Gold
- 20220128_doncaster_1315 (in-sample, 7 ran): Funambule Sivola (won); winner Funambule Sivola
- 20220129_doncaster_1410 (in-sample, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (in-sample, 7 ran): Flying Instructor (4); winner Chase The Dollar
- 20220214_catterick_1515 (in-sample, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (in-sample, 6 ran): Wise Eagle (4); winner Sir Chauvelin
- 20220217_leicester_1445 (in-sample, 4 ran): Nelson River (won); winner Nelson River
- 20220219_haydock_1405 (in-sample, 6 ran): Thomas Darby (5); winner Wholestone
- 20220223_doncaster_1600 (in-sample, 6 ran): Boss Man Fred (2); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (in-sample, 5 ran): Gowanlad (won); winner Gowanlad
- 20220309_fontwell_1440 (in-sample, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (in-sample, 6 ran): Peak Time (won); winner Peak Time
- 20261106_aintree_1240 (in-sample, 4 ran): Risky Obsession (won); winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Manuelito (4); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): So You Know (4); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Pawpaw (6); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B4 Same body, clear lead
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Pallas Dancer (2); winner Athmad
- 20220108_lingfield_aw_1345 (in-sample, 5 ran): Protected Guest (2); winner Trevolli
- 20220110_ludlow_1515 (in-sample, 7 ran): Jimmy The Digger (5); winner Java Point
- 20220121_lingfield_1350 (in-sample, 7 ran): none; winner Frero Banbou
- 20220123_lingfield_1500 (in-sample, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (in-sample, 7 ran): none; winner Funambule Sivola
- 20220129_doncaster_1410 (in-sample, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (in-sample, 7 ran): Carn A Chlamain (7); winner Chase The Dollar
- 20220214_catterick_1515 (in-sample, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (in-sample, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (in-sample, 4 ran): Nelson River (won); winner Nelson River
- 20220219_haydock_1405 (in-sample, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (in-sample, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (in-sample, 5 ran): Blazing Hot (2); winner Gowanlad
- 20220309_fontwell_1440 (in-sample, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (in-sample, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (in-sample, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (in-sample, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (in-sample, 7 ran): All In You (won); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Sweet Nightingale (4); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B5 Same body in both planes
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (in-sample, 5 ran): none; winner Trevolli
- 20220110_ludlow_1515 (in-sample, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (in-sample, 7 ran): Cedar Hill (5); winner Frero Banbou
- 20220123_lingfield_1500 (in-sample, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (in-sample, 7 ran): Before Midnight (2); winner Funambule Sivola
- 20220129_doncaster_1410 (in-sample, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (in-sample, 7 ran): Carn A Chlamain (7); winner Chase The Dollar
- 20220214_catterick_1515 (in-sample, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (in-sample, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (in-sample, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (in-sample, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (in-sample, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (in-sample, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (in-sample, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (in-sample, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (in-sample, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (in-sample, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (in-sample, 7 ran): All In You (won); winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B6 Same body on both charts
- 20210402_lingfield_aw_1435 (test, 6 ran): Indie Angel (5); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Pallas Dancer (2); winner Athmad
- 20220108_lingfield_aw_1345 (in-sample, 5 ran): none; winner Trevolli
- 20220110_ludlow_1515 (in-sample, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (in-sample, 7 ran): none; winner Frero Banbou
- 20220123_lingfield_1500 (in-sample, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (in-sample, 7 ran): none; winner Funambule Sivola
- 20220129_doncaster_1410 (in-sample, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (in-sample, 7 ran): none; winner Chase The Dollar
- 20220214_catterick_1515 (in-sample, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (in-sample, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (in-sample, 4 ran): Nelson River (won); winner Nelson River
- 20220219_haydock_1405 (in-sample, 6 ran): Molly Ollys Wishes (6); winner Wholestone
- 20220223_doncaster_1600 (in-sample, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (in-sample, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (in-sample, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (in-sample, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (in-sample, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (in-sample, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (in-sample, 7 ran): Dedicated Hero (6), All In You (won); winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): none; winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B7 Most sky bodies onto the jockey's Jupiter
- 20210402_lingfield_aw_1435 (test, 6 ran): Nirodha (6); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Raise The Roof (3), Tricolore (4); winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Protected Guest (2); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): Java Point (won), Method Madness (6); winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Frero Banbou (won); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Master Tommytucker (5); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): Funambule Sivola (won); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): Anna Bunina (4); winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): The Dancing Poet (3); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Brian Boranha (4); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): Onesmoothoperator (2); winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): Nelson River (won); winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): Top Ville Ben (2); winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): Half Track (3); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Royaume Uni (won); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): Thundersockssundae (3); winner Peak Time
- 20261106_aintree_1240 (in-sample, 4 ran): Risky Obsession (won); winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): Barnpark (5); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Bucephalus (3), Lyssenko (2); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2), Mirabad (3), Rubaud (won); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): Motazzen (2); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Steal The Moves (won); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): Walk Tall (7); winner Defence Witness

### B8 One line star on the most natal bodies
- 20210402_lingfield_aw_1435 (test, 6 ran): Indie Angel (5), Pholas (won); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): Beating All (5); winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Protected Guest (2), Supakalanistic (5); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): Isolate (2), Une De La Seniere (3), Wildfire Warrior (7), Jimmy The Digger (5), Method Madness (6); winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Frero Banbou (won); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Itchy Feet (4); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): Funambule Sivola (won); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): Western Victory (3); winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Chase The Dollar (won); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Winds Of Fire (5); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): Onesmoothoperator (2), Resumption (5); winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): Fransham (4), Nelson River (won), Stepney Causeway (3); winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): Thomas Darby (5), Molly Ollys Wishes (6); winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): Boss Man Fred (2); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): Blazing Hot (2), Tathmeen (3); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Royaume Uni (won), Hell Red (2), Dreaming Blue (5); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): Edmond Dantes (6), Peak Time (won), Black Opium (4); winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): Aqua Bleu (2); winner Risky Obsession
- 20261106_aintree_1315 (in-sample, 5 ran): Off The Jury (won); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Dedicated Hero (6), All In You (won), Lyssenko (2), Star Of Guiting (5), King Ulanda (7); winner All In You
- 20261106_aintree_1500 (test, 6 ran): Mirabad (3), Rubaud (won), Daytime Dreaming (5); winner Rubaud
- 20261106_fontwell_1435 (test, 8 ran): Donnie Azoff (7); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Ted The Thief (5), Hard Stare (2), Sweet Nightingale (4); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): Walk Tall (7), Croagh Patrick (5); winner Defence Witness

### B9 Jupiter and two of its line stars on one natal body
- 20210402_lingfield_aw_1435 (test, 6 ran): Indie Angel (5); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): none; winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): Java Point (won), Une De La Seniere (3), Jimmy The Digger (5); winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): none; winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): none; winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): none; winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Red Tornado (6); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): Stepney Causeway (3); winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): none; winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): Vocaliser (5); winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): Barnpark (5); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Bucephalus (3); winner All In You
- 20261106_aintree_1500 (test, 6 ran): JPR One (2), Rubaud (won), Brookie (4); winner Rubaud
- 20261106_fontwell_1435 (in-sample, 8 ran): Fire Flyer (won); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Hard Stare (2), Steal The Moves (won); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

### B10 Sun and two of its line stars on one natal body
- 20210402_lingfield_aw_1435 (test, 6 ran): Nirodha (6); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Trevolli (won); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Eclair D'Ainay (2), Financier (7), Cedar Hill (5), Le Ligerien (3); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Bristol De Mai (3), Dashel Drasher (2), Master Tommytucker (5), Itchy Feet (4), Two For Gold (won); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): Funambule Sivola (won), Before Midnight (2), Fransham (6); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): Miss Heritage (won); winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Flying Instructor (4); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Omar Maretti (won); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): Sir Chauvelin (won); winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): Third Wind (3); winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): Gowanlad (won); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): Royaume Uni (won); winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): none; winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): none; winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Lyssenko (2); winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (in-sample, 8 ran): Lynx De Thaix (3), Donnie Azoff (7); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): none; winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): Defence Witness (won), C'Mon So (2); winner Defence Witness

### B11 Moon and two of its line stars on one natal body
- 20210402_lingfield_aw_1435 (test, 6 ran): none; winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Trevolli (won); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): none; winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Financier (7), Frero Banbou (won), Cedar Hill (5); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Bristol De Mai (3), Dashel Drasher (2), Master Tommytucker (5), Itchy Feet (4), Two For Gold (won); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): Funambule Sivola (won), King D'argent (5); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Deluxe Music (2), Red Tornado (6); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): none; winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): none; winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): Boss Man Fred (2), Mr Washington (6), Half Track (3), Silva Eclipse (won); winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): James Watt (4), Gowanlad (won); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): Edmond Dantes (6), Sir Apollo (2), Thundersockssundae (3); winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): Watery Borren (3), Avide (4); winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): Off The Jury (won); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Dedicated Hero (6), All In You (won), Star Of Guiting (5), King Ulanda (7); winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (in-sample, 8 ran): Donnie Azoff (7), The Bellhop (5); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Ted The Thief (5); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): Croagh Patrick (5); winner Defence Witness

### B12 Same body and two line stars on it
- 20210402_lingfield_aw_1435 (test, 6 ran): Indie Angel (5), Nirodha (6), Pholas (won); winner Pholas
- 20210802_newcastle_aw_1633 (test, 6 ran): none; winner Athmad
- 20220108_lingfield_aw_1345 (test, 5 ran): Protected Guest (2); winner Trevolli
- 20220110_ludlow_1515 (test, 7 ran): Java Point (won); winner Java Point
- 20220121_lingfield_1350 (test, 7 ran): Financier (7), Frero Banbou (won), Cedar Hill (5); winner Frero Banbou
- 20220123_lingfield_1500 (test, 6 ran): Itchy Feet (4), Two For Gold (won); winner Two For Gold
- 20220128_doncaster_1315 (test, 7 ran): Funambule Sivola (won); winner Funambule Sivola
- 20220129_doncaster_1410 (test, 5 ran): none; winner Miss Heritage
- 20220213_southwell_aw_1520 (test, 7 ran): Red Tornado (6); winner Chase The Dollar
- 20220214_catterick_1515 (test, 6 ran): Omar Maretti (won); winner Omar Maretti
- 20220215_newcastle_aw_1640 (test, 6 ran): none; winner Sir Chauvelin
- 20220217_leicester_1445 (test, 4 ran): Stepney Causeway (3); winner Nelson River
- 20220219_haydock_1405 (test, 6 ran): none; winner Wholestone
- 20220223_doncaster_1600 (test, 6 ran): none; winner Silva Eclipse
- 20220224_newcastle_aw_1830 (test, 5 ran): James Watt (4), Blazing Hot (2); winner Gowanlad
- 20220309_fontwell_1440 (test, 7 ran): none; winner Royaume Uni
- 20220311_newcastle_1540 (test, 6 ran): none; winner Peak Time
- 20261106_aintree_1240 (test, 4 ran): Avide (4); winner Risky Obsession
- 20261106_aintree_1315 (test, 5 ran): Off The Jury (won), Leader Crik (3), Dixie Mafia (4); winner Off The Jury
- 20261106_aintree_1350 (test, 7 ran): Bucephalus (3), All In You (won), Star Of Guiting (5); winner All In You
- 20261106_aintree_1500 (test, 6 ran): none; winner Rubaud
- 20261106_fontwell_1435 (in-sample, 8 ran): Donnie Azoff (7); winner Fire Flyer
- 20261106_fontwell_1510 (test, 6 ran): Hard Stare (2); winner Steal The Moves
- 20261106_hexham_1335 (test, 7 ran): none; winner Defence Witness

