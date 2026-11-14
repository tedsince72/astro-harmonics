#!/usr/bin/env python3
"""Checks for tools/eddie_bybody_rules.py on Lingfield AW 14:35 2 Apr 2021 (the rules' origin race).

Expected holders per rule = the field checks recorded with each rule (docs/eddie_read/bybody/RULE_CANDIDATES.md, with the
two corrections of 14 Nov 2026: BB2 also Nirodha Quaoar, BB11 also Fizzy Feet Haumea), plus Pholas cells copied from the
bybody sheet by hand. Usage: python3 tests/eddie_bybody_rules_check.py
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import eddie_bybody_rules as R  # noqa: E402

RACE = '20210402_lingfield_aw_1435'
XLSX = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', RACE, f'{RACE}_bybody.xlsx')
ACTIVE = os.path.join(ROOT, 'reference', 'classic', f'race_batch_{RACE}_active.xlsx')

EXPECT = {  # rule: {(runner, body), ...}
    'BB1': {('05 Pholas', 'Mercury')},
    'BB2': {('05 Pholas', 'Mars'), ('04 Nirodha', 'Quaoar')},
    'BB3': {('01 Arafi', 'Pallas'), ('03 Indie Angel', 'Jupiter'), ('05 Pholas', 'Mercury'), ('05 Pholas', 'Jupiter'),
            ('05 Pholas', 'Chiron'), ('06 Shimmering Dawn', 'Pluto'), ('06 Shimmering Dawn', 'Eris')},
    'BB4': {('05 Pholas', 'Saturn')},
    'BB5': {('05 Pholas', 'Uranus')},
    'BB6': {('05 Pholas', 'Uranus'), ('03 Indie Angel', 'Mars')},
    'BB7': {('05 Pholas', 'Neptune'), ('05 Pholas', 'Saturn'), ('05 Pholas', 'Venus'), ('01 Arafi', 'Pluto')},
    'BB8': {('05 Pholas', 'Rahu')},
    'BB9': {('05 Pholas', 'Rahu')},
    'BB10': {('05 Pholas', 'Ketu'), ('04 Nirodha', 'Ketu')},
    'BB11': {('05 Pholas', 'Ceres'), ('02 Fizzy Feet', 'Haumea')},
    'BB12': {('05 Pholas', 'Pallas')},
    'BB13': {('05 Pholas', 'Juno')},
    'BB14': {('05 Pholas', 'Vesta'), ('06 Shimmering Dawn', 'Ketu')},
    'BB15': {('05 Pholas', 'Chiron')},
    'BB16': {('05 Pholas', 'Eris'), ('01 Arafi', 'Pluto'), ('01 Arafi', 'Orcus')},
    'BB17': {('05 Pholas', 'Makemake')},
    'BB18': {('03 Indie Angel', 'Gonggong')},
    'BB19': set(),
}
CELLS = {  # rule: (runner, body, [cell texts that must be in the case])
    'BB1': ('05 Pholas', 'Mercury', ['J Aldebaran – J Mercury Dec 16.193302 10×φ golden (59.99)',
                                     'S Mars – S Sedna Dec 16.192613 10×φ golden (62.12)',
                                     'S Mars – S Mercury RA 77.750019 77.7778 ninth (82.15)',
                                     'S Sedna → J Mercury Dec 7.774191 7.77778 ninth (76.94)']),
    'BB5': ('05 Pholas', 'Uranus', ['H Regulus – H Uranus RA 133.089295 133.333 ninth (8.49)']),
    'BB9': ('05 Pholas', 'Rahu', ['S Transpluto – S Regulus RA 1.996738 2 whole (83.69)',
                                  'S Transpluto → J Rahu RA 33.343278 33.3333 ninth (85.08)']),
    'BB13': ('05 Pholas', 'Juno', ['S Orcus – S Quaoar Dec 4.001963 4 whole (90.19)',
                                   'S Mars – S Jupiter RA 110.018894 68×φ golden (77.11)']),
    'BB17': ('05 Pholas', 'Makemake', ['S Chiron → H Makemake Dec 18.889313 18.8889 ninth (98.88)']),
}
ok = bad = 0


def check(cond, msg):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', msg)


if not os.path.exists(XLSX):
    subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'eddie_bybody.py'), ACTIVE], check=True)
race, runners, res = R.run(XLSX)
check(race == RACE and len(runners) == 6, 'race / runners')
check(sorted(res) == sorted(EXPECT), 'rule set')
for rid, exp in EXPECT.items():
    got = {(c['runner'], c['body']) for c in res[rid]}
    check(got == exp, f'{rid} holders {sorted(got)} != {sorted(exp)}')
for rid, (run, body, want) in CELLS.items():
    cases = [c for c in res[rid] if c['runner'] == run and c['body'] == body]
    allc = [x for c in cases for x in c['cells']]
    for w in want:
        check(any(x.startswith(w.rsplit(' (', 1)[0]) for x in allc), f'{rid} {run} {body} missing cell {w}')
# decade highlight on Pholas Mercury (BB1)
dec = [d for c in res['BB1'] for d in c['decade']]
check(any('77.7778' in d and '7.77778' in d for d in dec), 'BB1 decade highlight 77.7778 / 7.77778')
# lights shown with the case
check(any('S Moon → H Mercury RA 13.329589' in x for c in res['BB1'] for x in c['lights']), 'BB1 Moon light')
# never reads a csv
src = open(os.path.join(ROOT, 'tools', 'eddie_bybody_rules.py')).read()
check('.csv' not in src.replace('Never a csv', ''), 'no csv in the tool')
# Haydock 13:45 8 Jun 2020 (BB18 origin): 07 Ishvara Venus the only holder
HAY = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20200608_haydock_1345', '20200608_haydock_1345_bybody.xlsx')
if os.path.exists(HAY):
    _, _, hres = R.run(HAY)
    check({(c['runner'], c['body']) for c in hres['BB18']} == {('07 Ishvara', 'Venus')}, 'BB18 Haydock holders')
    allc = [x for c in hres['BB18'] for x in c['cells']]
    for w in ('H Venus – J Venus RA 155.302206 155.556 ninth', 'S Juno – S Fomalhaut RA', 'S Fomalhaut – S Venus Dec',
              'J Fomalhaut – J Venus Dec', 'S Juno – S Venus RA'):
        check(any(x.startswith(w) for x in allc), f'BB18 Ishvara cell {w}')
if os.path.exists(HAY):
    check({(c['runner'], c['body']) for c in hres['BB19']} == {('07 Ishvara', 'Venus')}, 'BB19 Haydock holders')
    nts = [n for c in hres['BB19'] for n in c['notes']]
    check(len(nts) == 4 and sum('likely automatic' in n for n in nts) == 2, 'BB19 notes (2 RA unisons automatic)')
    check(any('1.666499 5/3' in n for n in nts), 'BB19 J Dec 5/3')
print(f'{ok}/{ok + bad} checks passed')
sys.exit(1 if bad else 0)
