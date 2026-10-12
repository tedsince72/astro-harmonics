#!/usr/bin/env python3
"""layer5_check.py — readings are blind, and each test winner's reading names its hand-read shapes and items."""
import glob, re, sys
def R(race, P): return open(f'docs/classic/{race}/layer5/{P}.md').read()
C = [
 ('york_1615_20240515','P25',['horse Venus–Mason Uranus','both ends of the cross link have moved','the pair is together in the sky','same-body Chiron','same-body Rahu','Rahu Equator 23.00196 = 23','Mason Pallas -14.00695 = 14']),
 ('newmarket_july_1745_20240816','P01',['horse Uranus–Hornby Venus','sky Venus -> horse Uranus GC 122.99504 = 123','sky Pluto -> Hornby Venus Dec 38.00131 = 38 = Hornby Pluto moved Dec 17.00361 = 17 +','Venus–Hornby Pluto Dec 20.99770 = 21','number 21','same-body Chiron Dec']),
 ('perth_1610_20220420','P09',['cross link struck on both ends by 2+ different sky bodies','horse Ceres–Bowen Uranus']),
 ('nottingham_1530_20220601','P01',['cross link struck on both ends by 2+ different sky bodies','horse Sedna–Dawson Chiron']),
 ('wolverhampton_aw_1725_20231021','P05',["horse Eris–O'Neill Jupiter",'both ends of the cross link have moved']),
 ('fontwell_1530_20231006','P05',['swap']),
 ('sandown_1430_20240215','P13',['Only runner in the field (strict): swap','Brace Mars–Brace Jupiter Dec 50']),
 ('ascot_1350_20231021','P01',['triangle struck at every corner by one sky body','sky Vesta']),
 ('nottingham_1750_20220613','P03',['number 34','ratio 19/8']),
 ('newcastle_aw_1330_20220102','P09',['shared node']),
 ('haydock_1405_20220219','P09',['shared node']),
 ('dettori_ascot_19960928','P01',['a sky body divides a natal pair','Dettori Sun -> Dettori Chiron Dec span 28.01379']),
]
fails = 0
for race, P, phrases in C:
    t = R(race, P)
    for ph in phrases:
        ok = ph in t; fails += not ok
        print(('  ok   ' if ok else '  MISS ') + f'{race} {P}: {ph}')
bad = [f for f in glob.glob('docs/classic/*/layer5/*.md') if re.search(r'finish|\bSP\b|finish_pos', open(f).read().replace('no finishing positions', ''))]
print(('  ok   ' if not bad else '  FAIL ') + f'blind: no finishing positions in any reading ({len(bad)} bad)'); fails += bool(bad)
print('FAILS', fails); sys.exit(1 if fails else 0)
