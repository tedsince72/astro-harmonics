# Blank-sheet investigation – surprise ranking of the 96 races

Eddie, 2 Oct 2026 21:16–21:21: start from a clean sheet; begin with the most unexpected winners and work towards the most expected; read each race in full detail to find the COMBINATIONS; compare the top 3 finishers (plus the beaten favourite when it is outside the top 3); keep all insights from the T39–T48 reads (take-stock section in test-race-reads-25-48.md) as a checklist on every read.

## Build (2 Oct 2026, after Eddie's go-ahead 21:21)
- export_positions.py v1.0 (md5 fdae5cac…) – baseline 48 workbooks → same CSV layout as test_positions; all 96 in ledger/allpos.
- sky_motion.py v1.1 (md5 at build in ledger/) – race sky at the off, ±2 min and ±30 min with the project engine v2.2; every non-TNO body reproduces TRANS_POS to < 1e-6° in all 96 races; TNO ephemeris files are not in the workspace, so TNO motion comes from their positions across the 96 race dates (they move ~0.0003° in 30 min).
- ledger.py v1.1 – per race: __SKY.csv (every sky pair scoring > 0, rank among 80+ pairs with fast points aside and the Moon kept, applying/separating at the off, scores ±30 min) and __LEDGER.csv (every natal–natal, sky→natal and self contact on every chart scoring > 0, with raw degrees, deviation from the family target, all family scores, applying/separating, the sky pair's score and rank, body class, day_width = how far the value moves over the unknown birth hour, and SHARED = how many other runners hold the same contact). No only-here / ** / ^ filters – everything kept and labelled. Natal Moon kept (flagged by day_width).
- surprise.py v1.1 (md5 b0bb16dc…) – measure agreed: (winner SP+1)/(favourite SP+1); favourite winners = 1, ordered by price (shortest = most expected, last). v1.1 (3 Oct, Eddie spotted it): odds now read from the SP text – the stored odds column had 0 for joint favourites (15/8J), which put T47 at ×17.0 (4th); correct is ×5.9 (31st). Joint favourites are both shown. Only T47 was affected.

## Ranking (1 = most unexpected)

| # | Race | Field | Winner | SP | Favourite | Fav SP | Fav finish | Ratio |
|---|---|---|---|---|---|---|---|---|
| 1 | T33 20220406_catterick_1440 | 5 | 5 Wotever Next | 33/1 | 2 Beluga Gold | 2/5 | 2 | 24.286 |
| 2 | T32 20220323_ffos_las_1725 | 4 | 4 Ring The Moon | 28/1 | 2 You Say Nothing | 2/5 | 2 | 20.714 |
| 3 | R21 20220102_newcastle_aw_1330 | 5 | 5 Venturous | 25/1 | 1 Good Effort | 2/5 | 3 | 18.571 |
| 4 | R29 20220318_doncaster_1440 | 5 | 2 Olympe De Gouges | 25/1 | 3 Oot Ma Way | 5/6 | 2 | 14.182 |
| 5 | R9 20211014_carlisle_1355 | 5 | 1 Arvico Bleu | 25/1 | 4 Gold Des Bois | Evens | 2 | 13.0 |
| 6 | R30 20220321_wincanton_1420 | 6 | 4 River Bray | 22/1 | 3 Ballyblack | 10/11 | 3 | 12.048 |
| 7 | R12 20211019_exeter_1515 | 6 | 7 Forget You Not | 25/1 | 3 Pens Man | 5/4 | 4 | 11.556 |
| 8 | R39 20220510_sedgefield_1500 | 5 | 1 Blue Collar Glory | 20/1 | 4 Wheres Maud Gone | 5/6 | 5 | 11.455 |
| 9 | R27 20220217_leicester_1445 | 4 | 3 Nelson River | 20/1 | 4 Nickolson | Evens | 2 | 10.5 |
| 10 | T41 20220601_nottingham_1530 | 5 | 2 Dynamic Force | 18/1 | 3 Princess Shabnam | 5/6 | 3 | 10.364 |
| 11 | T30 20220311_newcastle_1540 | 6 | 3 Peak Time | 16/1 | 2 Edmond Dantes | 5/6 | F | 9.273 |
| 12 | R44 20220616_ripon_1525 | 4 | 4 Society Red | 16/1 | 1 Bollin Joan | 10/11 | 4 | 8.905 |
| 13 | T1 20210802_newcastle_aw_1633 | 6 | 2 Athmad | 25/1 | 3 Raise The Roof | 2/1 | 3 | 8.667 |
| 14 | R48 20220716_doncaster_1845 | 6 | 5 Novakai | 12/1 | 1 Crackovia | 8/15 | 2 | 8.478 |
| 15 | T8 20210914_fontwell_1645 | 4 | 3 Pixie Loc | 14/1 | 1 Eye To The Sky | 4/5 | 3 | 8.333 |
| 16 | R38 20220509_musselburgh_1550 | 6 | 3 John Kirkup | 14/1 | 1 The Thin Blue Line | 5/6 | 5 | 8.182 |
| 17 | T28 20220223_doncaster_1600 | 6 | 6 Silva Eclipse | 16/1 | 5 Half Track | 11/10 | 3 | 8.095 |
| 18 | T18 20211204_sandown_1425 | 5 | 3 Greaneteen | 12/1 | 2 Chacun Pour Soi | 8/13 | 5 | 8.048 |
| 19 | T13 20211112_newcastle_aw_1220 | 6 | 2 Sir Chauvelin | 25/1 | 7 Buxted Too | 9/4 | 4 | 8.0 |
| 20 | T46 20220712_bath_1530 | 4 | 3 Cafe Sydney | 11/1 | 5 Overstate | 1/2 | 3 | 8.0 |
| 21 | T9 20211015_redcar_1515 | 5 | 5 Present Moment | 14/1 | 3 Divine Jewel | 10/11 | 3 | 7.857 |
| 22 | T38 20220504_kelso_1450 | 6 | 4 Domandlouis | 12/1 | 6 Spanish Present | 4/6 | 4 | 7.8 |
| 23 | T6 20210904_kempton_aw_1440 | 5 | 3 Hamish | 9/1 | 1 Hukum | 30/100 | 2 | 7.692 |
| 24 | R36 20220414_newmarket_1535 | 6 | 4 Eydon | 22/1 | 5 Masekela | 2/1 | 2 | 7.667 |
| 25 | T4 20210822_worcester_1300 | 5 | 3 Rhythm Is A Dancer | 14/1 | 1 Streets Of Doyen | 6/5 | 3 | 6.818 |
| 26 | T36 20220420_perth_1610 | 5 | 5 Daphne Moon | 10/1 | 2 Zambella | 8/13 | 3 | 6.81 |
| 27 | R16 20211126_newbury_1350 | 5 | 7 Not Available | 14/1 | 2 Mister Coffey | 5/4 | 3 | 6.667 |
| 28 | T21 20220105_ffos_las_1420 | 3 | 6 New Age Dawning | 10/1 | 1 Gustavian | 8/11 | 2 | 6.368 |
| 29 | R17 20211211_newcastle_aw_1420 | 6 | 5 Nicholas T | 14/1 | 2 Coltrane | 6/4 | 6 | 6.0 |
| 30 | T11 20211020_fontwell_1505 | 5 | 3 Native Robin | 16/1 | 2 Dorking Lad | 15/8 | 4 | 5.913 |
| 31 | T47 20220717_newton_abbot_1525 | 4 | 4 On Time | 16/1 | 2 My Lady Grey & 3 Cresswell Queen | 15/8J | 4 & 2 | 5.913 |
| 32 | T19 20211205_huntingdon_1352 | 6 | 3 First Flow | 12/1 | 1 Allmankind | 5/4 | 5 | 5.778 |
| 33 | T26 20220219_haydock_1405 | 6 | 5 Wholestone | 16/1 | 6 Molly Ollys Wishes | 2/1 | PU | 5.667 |
| 34 | R24 20220129_doncaster_1410 | 5 | 5 Miss Heritage | 10/1 | 1 Miranda | Evens | 2 | 5.5 |
| 35 | T40 20220507_haydock_1718 | 5 | 6 Aldhaja | 10/1 | 5 Out From Under | Evens | 3 | 5.5 |
| 36 | T43 20220613_nottingham_1750 | 6 | 2 The Dunkirk Lads | 12/1 | 3 Gidwa | 11/8 | 6 | 5.474 |
| 37 | T14 20211119_catterick_1505 | 6 | 4 Brian Boranha | 14/1 | 1 Reve | 7/4 | 4 | 5.455 |
| 38 | R1 20210825_musselburgh_1345 | 5 | 4 Graces Quest | 11/1 | 5 Natural Value | 11/8 | 3 | 5.053 |
| 39 | R15 20211112_newcastle_aw_1540 | 6 | 3 Heart Throb | 9/1 | 5 Rabat | Evens | 2 | 5.0 |
| 40 | R33 20220406_lingfield_aw_1425 | 6 | 5 Man On A Mission | 12/1 | 1 Judy's Park | 13/8 | 2 | 4.952 |
| 41 | R18 20211216_exeter_1415 | 5 | 1 Deja Vue | 10/1 | 3 Maskada | 11/8 | 3 | 4.632 |
| 42 | T23 20220123_lingfield_1500 | 6 | 7 Two For Gold | 10/1 | 2 Dashel Drasher | 6/4 | 2 | 4.4 |
| 43 | R6 20210904_haydock_1420 | 6 | 2 Golden Flame | 9/1 | 3 Valley Forge | 11/8 | 3 | 4.211 |
| 44 | R26 20220215_newcastle_aw_1640 | 6 | 1 Sir Chauvelin | 10/1 | 4 Onesmoothoperator | 13/8 | 2 | 4.19 |
| 45 | R42 20220603_bath_1750 | 4 | 5 Little Girl Blue | 10/1 | 7 Soi Dao | 13/8 | 2 | 4.19 |
| 46 | R45 20220707_carlisle_1630 | 6 | 6 Whitefeathersfall | 10/1 | 2 Million Thanks | 13/8 | 3 | 4.19 |
| 47 | R8 20210915_yarmouth_1520 | 5 | 4 Ropey Guest | 9/1 | 5 Ajyaall | 6/4 | 3 | 4.0 |
| 48 | R4 20210827_goodwood_1853 | 5 | 5 Madame Tantzy | 12/1 | 1 Stunning Beauty | 5/2 | 3 | 3.714 |
| 49 | R5 20210903_ascot_1645 | 8 | 3 Dark Shift | 100/30 | 3 Dark Shift | 100/30 | 1 | 1.0 |
| 50 | R32 20220325_musselburgh_1605 | 7 | 4 Hold Onto The Line | 100/30 | 4 Hold Onto The Line | 100/30 | 1 | 1.0 |
| 51 | T3 20210820_kempton_aw_1510 | 7 | 6 Exceedingly Regal | 100/30 | 6 Exceedingly Regal | 100/30 | 1 | 1.0 |
| 52 | T12 20211022_doncaster_1300 | 7 | 2 Oh Herberts Reign | 16/5 | 2 Oh Herberts Reign | 16/5 | 1 | 1.0 |
| 53 | R35 20220412_newmarket_1645 | 7 | 5 Educator | 11/4 | 5 Educator | 11/4 | 1 | 1.0 |
| 54 | R40 20220511_bath_1930 | 8 | 4 Mrembo | 11/4 | 4 Mrembo | 11/4 | 1 | 1.0 |
| 55 | R46 20220711_windsor_1905 | 7 | 1 Lequinto | 11/4 | 1 Lequinto | 11/4 | 1 | 1.0 |
| 56 | T25 20220213_southwell_aw_1520 | 7 | 3 Chase The Dollar | 11/4 | 3 Chase The Dollar | 11/4 | 1 | 1.0 |
| 57 | R2 20210825_wolverhampton_aw_2010 | 8 | 3 Cuban Cigar | 5/2 | 3 Cuban Cigar | 5/2 | 1 | 1.0 |
| 58 | R43 20220611_chester_1410 | 8 | 1 Copper Knight | 5/2 | 1 Copper Knight | 5/2 | 1 | 1.0 |
| 59 | R7 20210914_redcar_1310 | 8 | 2 Le Beau Garcon | 9/4 | 2 Le Beau Garcon | 9/4 | 1 | 1.0 |
| 60 | R23 20220121_lingfield_1350 | 7 | 3 Frero Banbou | 9/4 | 3 Frero Banbou | 9/4 | 1 | 1.0 |
| 61 | T17 20211202_chelmsford_aw_1630 | 7 | 6 Trevolli | 9/4 | 6 Trevolli | 9/4 | 1 | 1.0 |
| 62 | T48 20220718_ayr_1645 | 7 | 1 Brazen Bolt | 9/4 | 1 Brazen Bolt | 9/4 | 1 | 1.0 |
| 63 | T34 20220415_chelmsford_aw_1555 | 8 | 3 Trawlerman | 11/5 | 3 Trawlerman | 11/5 | 1 | 1.0 |
| 64 | R14 20211111_chelmsford_aw_1830 | 6 | 6 Bascule | 85/40 | 6 Bascule | 85/40 | 1 | 1.0 |
| 65 | R3 20210826_chelmsford_aw_1530 | 6 | 3 Toussarok | 2/1 | 3 Toussarok | 2/1 | 1 | 1.0 |
| 66 | R22 20220110_ludlow_1515 | 7 | 1 Java Point | 2/1 | 1 Java Point | 2/1 | 1 | 1.0 |
| 67 | R28 20220224_newcastle_aw_1830 | 5 | 3 Gowanlad | 2/1 | 3 Gowanlad | 2/1 | 1 | 1.0 |
| 68 | R37 20220505_chester_1330 | 7 | 7 Look Out Louis | 2/1 | 7 Look Out Louis | 2/1 | 1 | 1.0 |
| 69 | R13 20211109_newcastle_aw_1800 | 8 | 3 Brazen Akoya | 15/8 | 3 Brazen Akoya | 15/8 | 1 | 1.0 |
| 70 | R25 20220214_catterick_1515 | 6 | 3 Omar Maretti | 15/8 | 3 Omar Maretti | 15/8 | 1 | 1.0 |
| 71 | T27 20220222_market_rasen_1630 | 7 | 5 Spanish Present | 15/8 | 5 Spanish Present | 15/8 | 1 | 1.0 |
| 72 | T7 20210913_brighton_1625 | 6 | 6 Discomatic | 7/4 | 6 Discomatic | 7/4 | 1 | 1.0 |
| 73 | T15 20211120_haydock_1535 | 7 | 7 Strictlyadancer | 7/4 | 7 Strictlyadancer | 7/4 | 1 | 1.0 |
| 74 | T42 20220604_lingfield_aw_2045 | 6 | 1 Forge Valley Lad | 7/4 | 1 Forge Valley Lad | 7/4 | 1 | 1.0 |
| 75 | R10 20211017_kempton_1440 | 6 | 1 Mercian Prince | 13/8 | 1 Mercian Prince | 13/8 | 1 | 1.0 |
| 76 | R19 20211217_kempton_aw_1845 | 8 | 4 Mercian Hymn | 13/8 | 4 Mercian Hymn | 13/8 | 1 | 1.0 |
| 77 | R31 20220323_haydock_1335 | 5 | 2 Soldier Of Destiny | 13/8 | 2 Soldier Of Destiny | 13/8 | 1 | 1.0 |
| 78 | T16 20211127_wolverhampton_aw_1830 | 6 | 3 Street Kid | 13/8 | 3 Street Kid | 13/8 | 1 | 1.0 |
| 79 | R41 20220602_chelmsford_aw_1800 | 7 | 3 Tahani | 6/4 | 3 Tahani | 6/4 | 1 | 1.0 |
| 80 | T2 20210803_chelmsford_aw_1545 | 8 | 8 Nibras Gold | 6/4 | 8 Nibras Gold | 6/4 | 1 | 1.0 |
| 81 | T5 20210903_kempton_aw_2045 | 6 | 6 Geremia | 6/4 | 6 Geremia | 6/4 | 1 | 1.0 |
| 82 | T31 20220318_fakenham_1345 | 5 | 5 Coole Well | 6/4 | 5 Coole Well | 6/4 | 1 | 1.0 |
| 83 | R47 20220714_chepstow_1600 | 6 | 4 Beryl Burton | 11/8 | 4 Beryl Burton | 11/8 | 1 | 1.0 |
| 84 | T29 20220309_fontwell_1440 | 7 | 2 Royaume Uni | 11/8 | 2 Royaume Uni | 11/8 | 1 | 1.0 |
| 85 | T35 20220419_wolverhampton_aw_1805 | 6 | 2 Tribal Art | 11/8 | 2 Tribal Art | 11/8 | 1 | 1.0 |
| 86 | T39 20220506_nottingham_1940 | 6 | 1 Percy's Lad | 11/8 | 1 Percy's Lad | 11/8 | 1 | 1.0 |
| 87 | R34 20220408_kempton_aw_1830 | 6 | 1 King Francis | 5/4 | 1 King Francis | 5/4 | 1 | 1.0 |
| 88 | T10 20211017_sedgefield_1640 | 6 | 5 Gordon's Jet | 5/4 | 5 Gordon's Jet | 5/4 | 1 | 1.0 |
| 89 | T22 20220108_lingfield_aw_1345 | 5 | 4 Trevolli | 5/4 | 4 Trevolli | 5/4 | 1 | 1.0 |
| 90 | T24 20220128_doncaster_1315 | 7 | 1 Funambule Sivola | 5/4 | 1 Funambule Sivola | 5/4 | 1 | 1.0 |
| 91 | T37 20220502_bath_1321 | 7 | 4 Symbol Of Hope | 5/4 | 4 Symbol Of Hope | 5/4 | 1 | 1.0 |
| 92 | R11 20211019_exeter_1405 | 6 | 1 An Tailliur | 6/5 | 1 An Tailliur | 6/5 | 1 | 1.0 |
| 93 | R20 20211218_haydock_1330 | 6 | 1 Shakem Up'arry | 6/5 | 1 Shakem Up'arry | 6/5 | 1 | 1.0 |
| 94 | T45 20220708_york_1550 | 6 | 1 Asaassi | 6/5 | 1 Asaassi | 6/5 | 1 | 1.0 |
| 95 | T20 20211214_catterick_1445 | 6 | 3 Out On The Tear | 11/10 | 3 Out On The Tear | 11/10 | 1 | 1.0 |
| 96 | T44 20220617_ascot_1735 | 6 | 1 Changingoftheguard | 11/10 | 1 Changingoftheguard | 11/10 | 1 | 1.0 |

48 races were won by a non-favourite (1–48), 48 by the favourite (49–96).
