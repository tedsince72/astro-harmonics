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
    'BB20': set(),
    'BB21': set(),
    'BB22': set(),
    'BB23': set(),
    'BB24': set(),
    'BB25': set(),
    'BB26': set(),
    'BB27': set(),
    'BB28': set(),
    'BB29': {('06 Shimmering Dawn', 'Jupiter')},
    'BB30': {('06 Shimmering Dawn', 'Ketu')},
    'BB31': set(),
    'BB32': {('01 Arafi', 'Pluto'), ('05 Pholas', 'Orcus')},
    'BB32b': set(),
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
    got = {(c['runner'], c['body']) for c in res[rid] if not c.get('watch_only')}
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
# WATCH additive steps (14 Nov 2026)
aw = [w for c in res['BB2'] if c['runner'] == '05 Pholas' for w in c['additive']]
check(any('106×φ = 65×φ + 41×φ' in w and 'may be geometry' in w for w in aw), 'additive step Pholas Mars 106 = 65 + 41 (geometry)')
aw = [w for c in res['BB11'] if c['runner'] == '05 Pholas' for w in c['additive']]
check(any('26 = 1 + 25' in w for w in aw), 'additive step Pholas Ceres 26 = 1 + 25')
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
    check({(c['runner'], c['body']) for c in hres['BB20']} ==
          {('07 Ishvara', 'Jupiter'), ('07 Ishvara', 'Gonggong'), ('06 Birkenhead', 'Jupiter')}, 'BB20 Haydock holders')
    ij = [x for c in hres['BB20'] if c['runner'] == '07 Ishvara' and c['body'] == 'Jupiter' for x in c['cells']]
    for w in ('H Fomalhaut – H Jupiter RA 144.676267', 'S Jupiter – S Transpluto RA', 'S Pluto → H Jupiter Dec',
              'S Sedna → H Jupiter RA', 'S Sun → H Jupiter RA'):
        check(any(x.startswith(w) for x in ij), f'BB20 Ishvara Jupiter cell {w}')
    check({(c['runner'], c['body']) for c in hres['BB21']} == {('07 Ishvara', 'Saturn'), ('08 Dancin Inthestreet', 'Gonggong')},
          'BB21 Haydock holders')
    check({(c['runner'], c['body']) for c in hres['BB22']} == {('07 Ishvara', 'Saturn')}, 'BB22 Haydock holders')
    isat = [x for c in hres['BB22'] for x in c['cells']]
    for w in ('S Saturn → H Saturn Dec 2.000397', 'S Uranus – S Regulus Dec', 'S Uranus → H Saturn RA',
              'H Regulus – H Saturn RA', 'S Vesta – S Gonggong RA', 'H Aldebaran – H Saturn RA 161.998378'):
        check(any(x.startswith(w) for x in isat), f'BB22 Ishvara Saturn cell {w}')
    check({(c['runner'], c['body']) for c in hres['BB23']} == {('07 Ishvara', 'Neptune')}, 'BB23 Haydock holders')
    check(all(any(n.startswith('WATCH (b)') for n in c['notes']) for c in hres['BB23']), 'BB23 Ishvara watch (b) note')
    check({(c['runner'], c['body']) for c in hres['BB24']} == {('07 Ishvara', 'Rahu')}, 'BB24 Haydock holders')
    ir = [x for c in hres['BB24'] for x in c['cells']]
    for w in ('S Rahu → H Rahu Dec 13.009928', 'S Mercury – S Transpluto Dec', 'S Makemake – S Transpluto Dec',
              'S Makemake → J Rahu Dec', 'S Transpluto → J Rahu Dec', 'S Mercury → J Rahu Dec'):
        check(any(x.startswith(w) for x in ir), f'BB24 Ishvara Rahu cell {w}')
    aw = [w for c in hres['BB24'] for w in c['additive']]
    check(any('14 = 13 + 1' in w and 'may be geometry' not in w for w in aw) and
          any('14 = 13 + 1' in w and 'may be geometry' in w for w in aw), 'additive steps Ishvara Rahu, with and without geometry')
    check({(c['runner'], c['body']) for c in hres['BB25']} == {('07 Ishvara', 'Ketu'), ('08 Dancin Inthestreet', 'Venus')},
          'BB25 Haydock holders')
    ik = [x for c in hres['BB25'] if c['runner'] == '07 Ishvara' for x in c['cells']]
    for w in ('S Antares – S Ketu Dec', 'H Antares – H Ketu Dec 16.010522', 'S Mercury – S Transpluto Dec', 'S Mercury – S Ketu RA'):
        check(any(x.startswith(w) for x in ik), f'BB25 Ishvara Ketu cell {w}')
    check({(c['runner'], c['body']) for c in hres['BB26']} == {('07 Ishvara', 'Ceres'), ('06 Birkenhead', 'Venus')},
          'BB26 Haydock holders')
    nc = [n for c in hres['BB26'] if c['runner'] == '07 Ishvara' for n in c['notes']]
    check(any('1.00873' in n for n in nc) and any('1.009322' in n for n in nc) and not any('automatic' in n for n in nc),
          'BB26 Ishvara Ceres unisons, none automatic')
    nb = [n for c in hres['BB26'] if c['runner'] == '06 Birkenhead' for n in c['notes']]
    check(any('likely automatic' in n for n in nb), 'BB26 Birkenhead Venus Aldebaran unison marked likely automatic')
    check({(c['runner'], c['body']) for c in hres['BB27']} ==
          {('06 Birkenhead', 'Jupiter'), ('07 Ishvara', 'Jupiter'), ('07 Ishvara', 'Pallas'), ('09 Garsman', 'Pluto')}, 'BB27 Haydock holders')
    w27 = {(c['runner'], c['body']) for c in hres['BB27'] if any(n.startswith('WATCH (b)') for n in c['notes'])}
    check(w27 == {('07 Ishvara', 'Pallas')}, 'BB27 watch (b) only on Ishvara Pallas')
    check({(c['runner'], c['body']) for c in hres['BB28']} == {('07 Ishvara', 'Juno'), ('04 Royal Context', 'Pluto')},
          'BB28 Haydock holders')
    ij = [x for c in hres['BB28'] if c['runner'] == '07 Ishvara' for x in c['cells']]
    for w in ('S Fomalhaut – S Juno RA', 'J Fomalhaut – J Juno RA 101.990237', 'S Jupiter – S Makemake RA', 'S Jupiter → J Juno RA'):
        check(any(x.startswith(w) for x in ij), f'BB28 Ishvara Juno cell {w}')
    check({(c['runner'], c['body']) for c in hres['BB29']} == {('07 Ishvara', 'Vesta')}, 'BB29 Haydock holders')
    iv = [x for c in hres['BB29'] for x in c['cells']]
    for w in ('S Eris – S Antares Dec', 'S Eris – S Aldebaran Dec', 'J Antares – J Vesta Dec', 'S Eris → J Vesta Dec',
              'S Eris – S Vesta Dec', 'S Eris → H Vesta RA'):
        check(any(x.startswith(w) for x in iv), f'BB29 Ishvara Vesta cell {w}')
    h30 = {(c['runner'], c['body']) for c in hres['BB30'] if not c['watch_only']}
    w30 = {(c['runner'], c['body']) for c in hres['BB30'] if c['watch_only']}
    check(h30 == {('07 Ishvara', 'Eris')} and w30 == {('11 Mews House', 'Jupiter')}, 'BB30 Haydock holders / watch only')
    h31 = {(c['runner'], c['body']) for c in hres['BB31'] if not c['watch_only']}
    w31 = {(c['runner'], c['body']) for c in hres['BB31'] if c['watch_only']}
    check(h31 == {('07 Ishvara', 'Gonggong'), ('11 Mews House', 'Uranus')} and w31 == {('09 Garsman', 'Vesta')},
          'BB31 Haydock holders / watch only')
    ig = [x for c in hres['BB31'] if c['runner'] == '07 Ishvara' for x in c['cells']]
    for w in ('S Gonggong → J Gonggong Dec 9.710147', 'S Saturn – S Orcus Dec', 'S Orcus → J Gonggong RA', 'S Jupiter – S Gonggong Dec',
              'S Jupiter → J Gonggong Dec', 'S Pluto → H Gonggong Dec'):
        check(any(x.startswith(w) for x in ig), f'BB31 Ishvara Gonggong cell {w}')
    check({(c['runner'], c['body']) for c in hres['BB32']} == set() and not hres['BB32b'], 'BB32 / BB32b Haydock: none')
BEV = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20240608_beverley_1405', '20240608_beverley_1405_bybody.xlsx')
if os.path.exists(BEV):
    _, _, bres = R.run(BEV)
    check({(c['runner'], c['body']) for c in bres['BB32']} == {('04 Invincible Annice', 'Makemake'), ('15 Perfect Part', 'Sun')},
          'BB32 Beverley holders')
    check({(c['runner'], c['body']) for c in bres['BB32b']} == {('15 Perfect Part', 'Sun')}, 'BB32b Beverley holders')
    pc = [x for c in bres['BB32b'] for x in c['cells']]
    pn = [n for c in bres['BB32b'] for n in c['notes']]
    for w in ('J Regulus – J Sun Dec 5.552598', 'S Venus → J Sun Dec 5.551267', 'S Venus – S Sun Dec 0.187596',
              'S Venus – S Sun RA 1.137027', 'H Antares – H Sun RA 133.224682', 'S Venus – S Pluto RA 133.520006',
              'S Pluto – S Sun Dec contraparallel 0.003798', 'J Aldebaran – J Sun Dec 1.010907', 'S Chiron – S Sedna Dec 0.996865'):
        check(any(x.startswith(w) for x in pc), f'BB32b Perfect Part Sun cell {w}')
    check(any('both planes' in n for n in pn) and any('0.0013' in n for n in pn) and any('third royal star' in n for n in pn),
          'BB32b Perfect Part watch notes (both planes, gap 0.0013, third royal star)')
print(f'{ok}/{ok + bad} checks passed')
sys.exit(1 if bad else 0)
