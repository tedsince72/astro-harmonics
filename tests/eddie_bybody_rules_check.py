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
    'BB33': set(),
    'BB34': {('05 Pholas', 'Mercury')},
    'BB35': set(),
    'BB36': {('05 Pholas', 'Uranus')},
    'BB37': set(),
    'BB38': set(),
    'BB39': {('05 Pholas', 'Juno')},
    'BB40': set(),
    'BB41': set(),
    'BB42': set(),
    'BB43': set(),
    'BB44': set(),
    'BB45': set(),
    'BB46': set(),
    'BB47': set(),
    'BB48': {('04 Nirodha', 'Ketu'), ('05 Pholas', 'Mercury')},
    'BB49': set(),
    'BB50': set(),
    'BB51': set(),
    'BB52': set(),
    'BB54': set(),
    'BB53': {('06 Shimmering Dawn', 'Sun'), ('06 Shimmering Dawn', 'Jupiter'), ('06 Shimmering Dawn', 'Pallas')},
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
    check({(c['runner'], c['body']) for c in hres['BB32']} == set() and not hres['BB32b'] and not hres['BB33'], 'BB32 / BB32b / BB33 Haydock: none')
    check({(c['runner'], c['body']) for c in hres['BB34']} == {('03 Never In Paris', 'Orcus')}, 'BB34 Haydock holders')
    check({(c['runner'], c['body']) for c in hres['BB35']} == {('04 Royal Context', 'Pluto'), ('07 Ishvara', 'Chiron')}, 'BB35 Haydock holders')
    check(not any('Sedna is an end' in n for c in hres['BB34'] for n in c['notes']), 'BB34 Haydock: no Sedna note')
    check(not hres['BB36'], 'BB36 Haydock: none')
    check({(c['runner'], c['body']) for c in hres['BB37']} == {('07 Ishvara', 'Vesta')}, 'BB37 Haydock holders')
    check(not hres['BB38'], 'BB38 Haydock: none')
    check(not hres['BB39'], 'BB39 Haydock: none')
    check({(c['runner'], c['body']) for c in hres['BB40']} == {('07 Ishvara', 'Rahu')}, 'BB40 Haydock holders')
    check({(c['runner'], c['body']) for c in hres['BB41']} == {('07 Ishvara', 'Vesta')}, 'BB41 Haydock holders')
    check(hres['BB42'] == [], 'BB42 Haydock: no holder')
    check(hres['BB44'] == [], 'BB44 Haydock: no holder')
    check(hres['BB45'] == [] and hres['BB46'] == [], 'BB45 / BB46 Haydock: no holder (Ishvara Gonggong holds only version a)')
    check({(c['runner'], c['body']) for c in hres['BB47']} == {('07 Ishvara', 'Gonggong')}, 'BB47 Haydock holders')
    ic7 = [x for c in hres['BB47'] for x in c['cells']]
    for w in ('J Aldebaran – J Gonggong RA 100.174939', 'S Neptune – S Vesta RA 100.112554', 'S Vesta – S Gonggong RA 114.869213',
              'S Neptune → J Gonggong RA 23.000954', 'S Vesta → J Gonggong RA 123.113508', 'S Sun – S Gonggong RA 99.801411'):
        check(any(x.startswith(w) for x in ic7), f'BB47 Ishvara Gonggong cell {w}')
    check(len(ic7) == 6 and any('the same pair' in n for c in hres['BB47'] for n in c['notes']), 'BB47 Ishvara: 6 cells, one pair does both')
    check({(c['runner'], c['body']) for c in hres['BB48']} == {('02 Ventura Flame', 'Quaoar')}, 'BB48 Haydock holders')
    check({(c['runner'], c['body']) for c in hres['BB50']} == {('07 Ishvara', 'Eris')}, 'BB50 Haydock holders')
    ic50 = [x for c in hres['BB50'] for x in c['cells']]
    for w in ('H Eris – J Eris RA 2.990505', 'S Ketu – S Antares Dec 3.001702', 'S Mars – S Orcus Dec 3.014589', 'S Mars – S Eris RA 37.185073'):
        check(any(x.startswith(w) for x in ic50), f'BB50 Ishvara Eris cell {w}')
    check(len(ic50) == 4, 'BB50 Ishvara Eris: 4 cells')
    check({(c['runner'], c['body']) for c in hres['BB51']} == {('07 Ishvara', 'Mercury')}, 'BB51 Haydock holders')
    check(hres['BB52'] == [], 'BB52 Haydock: no holder')
    check({(c['runner'], c['body']) for c in hres['BB54']} == {('02 Ventura Flame', 'Neptune'), ('03 Never In Paris', 'Neptune'),
          ('06 Birkenhead', 'Jupiter'), ('07 Ishvara', 'Jupiter')}, 'BB54 Haydock holders')
    ij54 = [n for c in hres['BB54'] if c['runner'] == '07 Ishvara' for n in c['notes']]
    check(any('H Fomalhaut – H Jupiter RA 144.676267' in n and 'crossed ratio 9.957' in n for n in ij54), 'BB54 Ishvara note')
    check({(c['runner'], c['body']) for c in hres['BB53']} == {('03 Never In Paris', 'Vesta'), ('03 Never In Paris', 'Chiron')}, 'BB53 Haydock holders')
    ic51 = [x for c in hres['BB51'] for x in c['cells']]
    for w in ('H Antares – H Mercury Dec 27.981919', 'S Gonggong – S Aldebaran Dec 27.999417', 'J Antares – J Mercury RA 122.977640',
              'S Gonggong – S Haumea RA 122.826154', 'S Gonggong – S Mercury RA 124.983999'):
        check(any(x.startswith(w) for x in ic51), f'BB51 Ishvara Mercury cell {w}')
    check(len(ic51) == 5, 'BB51 Ishvara Mercury: 5 cells')
    check({(c['runner'], c['body']) for c in hres['BB49']} == {('07 Ishvara', 'Eris')}, 'BB49 Haydock holders')
    ic9 = [x for c in hres['BB49'] for x in c['cells']]
    for w in ('S Aldebaran – S Eris Dec 17.937557', 'S Antares – S Eris Dec 25.002977', 'H Eris – J Eris RA 2.990505',
              'S Ketu – S Antares Dec 3.001702', 'S Ketu → J Eris Dec 13.314408'):
        check(any(x.startswith(w) for x in ic9), f'BB49 Ishvara Eris cell {w}')
    check({(c['runner'], c['body']) for c in hres['BB43']} == {('07 Ishvara', 'Rahu'), ('09 Garsman', 'Transpluto'), ('11 Mews House', 'Sun')}, 'BB43 Haydock holders')
    ic3 = [x for c in hres['BB43'] if c['runner'] == '07 Ishvara' for x in c['cells']]
    in3 = [n for c in hres['BB43'] if c['runner'] == '07 Ishvara' for n in c['notes']]
    for w in ('S Rahu → H Rahu Dec 13.009928', 'S Mercury – S Transpluto Dec 12.996052', 'S Mercury – S Rahu RA 13.317469',
              'S Transpluto → H Rahu RA 1.243682', 'S Transpluto → J Rahu Dec 0.989868'):
        check(any(x.startswith(w) for x in ic3), f'BB43 Ishvara Rahu cell {w}')
    check(any('WATCH an end line is a conj' in n and 'S Transpluto → H Rahu RA' in n for n in in3), 'BB43 Ishvara conj end note')
    iv = [x for c in hres['BB41'] for x in c['cells']]
    ivn = [n for c in hres['BB41'] for n in c['notes']]
    for w in ('H Antares – H Vesta Dec contraparallel 0.153351', 'J Antares – J Vesta Dec 25.012800', 'S Eris – S Antares Dec 25.002977',
              'S Eris → J Vesta Dec 0.010058', 'S Moon – S Vesta Dec 46.936470', 'S Moon → H Vesta RA 177.621190', 'S Moon → J Vesta Dec 22.684496'):
        check(any(x.startswith(w) for x in iv), f'BB41 Ishvara Vesta cell {w}')
    check(any('royal star is a pair end' in n for n in ivn) and any('contraparallel royal line' in n or 'is a contraparallel' in n for n in ivn),
          'BB41 Ishvara notes (royal end, contraparallel line)')
    rc = [x for c in hres['BB40'] for x in c['cells']]
    for w in ('S Rahu → H Rahu Dec 13.009928', 'S Mercury – S Transpluto Dec 12.996052', 'S Mercury – S Rahu RA 13.317469',
              'S Transpluto → J Rahu Dec 0.989868', 'S Sun → J Rahu Dec 12.984017'):
        check(any(x.startswith(w) for x in rc), f'BB40 Ishvara Rahu cell {w}')
    check(any('Sun on the pair' in n for c in hres['BB40'] for n in c['notes']), 'BB40 Ishvara note: Sun on the pair')
    ic = [x for c in hres['BB37'] for x in c['cells']]
    for w in ('S Vesta → J Vesta Dec 24.251973', 'S Vesta – S Eris Dec 24.262031', 'S Eris → J Vesta Dec 0.010058', 'S Sun – S Vesta Dec 0.052556'):
        check(any(x.startswith(w) for x in ic), f'BB37 Ishvara Vesta cell {w}')
BEV = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20240608_beverley_1405', '20240608_beverley_1405_bybody.xlsx')
if os.path.exists(BEV):
    _, _, bres = R.run(BEV)
    check({(c['runner'], c['body']) for c in bres['BB32']} == {('04 Invincible Annice', 'Makemake'), ('15 Perfect Part', 'Sun')},
          'BB32 Beverley holders')
    check({(c['runner'], c['body']) for c in bres['BB33']} == {('15 Perfect Part', 'Mercury')}, 'BB33 Beverley holders')
    mc = [x for c in bres['BB33'] for x in c['cells']]
    mn = [n for c in bres['BB33'] for n in c['notes']]
    for w in ('S Mercury → H Mercury Dec 8.999', 'S Venus – S Aldebaran RA 8.996', 'S Aldebaran – S Mercury RA 0.188',
              'S Venus → J Mercury RA 23.005', 'S Mercury → J Mercury Dec 1.415', 'S Mars – S Sedna Dec 1.416'):
        check(any(x.startswith(w) for x in mc), f'BB33 Perfect Part Mercury cell {w}')
    check(any('likely automatic' in n for n in mn) and any('other chart same-body' in n for n in mn), 'BB33 Perfect Part watch notes')
    check({(c['runner'], c['body']) for c in bres['BB34']} == {('01 Aviation Time', 'Uranus'), ('07 Mademoiselle', 'Ketu'), ('12 Sands Of Dubai', 'Saturn'), ('14 Havana White', 'Pluto'), ('15 Perfect Part', 'Mars')}, 'BB34 Beverley holders')
    check({(c['runner'], c['body']) for c in bres['BB34'] if any('Sedna is an end' in n for n in c['notes'])} == {('15 Perfect Part', 'Mars')}, 'BB34 Beverley Sedna note')
    check({(c['runner'], c['body']) for c in bres['BB34'] if any('tight version' in n for n in c['notes'])} == {('15 Perfect Part', 'Mars')}, 'BB34 Beverley tight-version note only on Perfect Part Mars')
    rc = [x for c in bres['BB34'] if c['runner'] == '15 Perfect Part' for x in c['cells']]
    rnn = [n for c in bres['BB34'] if c['runner'] == '15 Perfect Part' for n in c['notes']]
    for w in ('J Fomalhaut – J Mars RA 48.561', 'S Rahu – S Sedna RA 48.555', 'S Rahu – S Mars RA 15.559', 'S Rahu – S Mars Dec 4.985',
              'S Sedna – S Mars RA 32.995', 'S Sedna – S Mars Dec 1.416', 'S Rahu → J Mars RA 20.997', 'S Sedna → H Mars Dec 22.238'):
        check(any(x.startswith(w) for x in rc), f'BB34 Perfect Part Mars cell {w}')
    check(any('other plane' in n and 'S Ceres – S Haumea' in n and '(Moon)' in n for n in rnn), 'BB34 Perfect Part watch note (Dec pairs)')
    check({(c['runner'], c['body']) for c in bres['BB35']} == {('04 Invincible Annice', 'Venus'), ('15 Perfect Part', 'Saturn')}, 'BB35 Beverley holders')
    sc = [x for c in bres['BB35'] if c['runner'] == '15 Perfect Part' for x in c['cells']]
    sn = [n for c in bres['BB35'] if c['runner'] == '15 Perfect Part' for n in c['notes']]
    for w in ('H Antares – H Saturn RA 78.036', 'H Regulus – H Saturn RA 173.297', 'S Antares – S Saturn RA 103.009', 'S Regulus – S Saturn RA 161.722'):
        check(any(x.startswith(w) for x in sc), f'BB35 Perfect Part Saturn cell {w}')
    check(any('9 9th harmonic (36.4)' in n and '20 1/20 cut (85.17)' in n for n in sn) and any('>= 80' in n for n in sn), 'BB35 Perfect Part notes')
    check({(c['runner'], c['body']) for c in bres['BB36']} == {('15 Perfect Part', 'Uranus')}, 'BB36 Beverley holders')
    uc = [x for c in bres['BB36'] for x in c['cells']]
    un = [n for c in bres['BB36'] for n in c['notes']]
    for w in ('S Uranus → H Uranus RA 11.095305', 'S Venus – S Regulus Dec 11.102830', 'H Regulus – H Uranus RA 111.240410',
              'S Antares – S Uranus Dec 45.011110'):
        check(any(x.startswith(w) for x in uc), f'BB36 Perfect Part Uranus cell {w}')
    check(any('10.025899 10 1/10 cut (48.2)' in n for n in un) and any('Regulus itself on sky Uranus' in n for n in un)
          and any('end Chiron' in n and 'S Chiron → J Uranus RA 73.005085' in n for n in un), 'BB36 Perfect Part notes')
    check({(c['runner'], c['body']) for c in bres['BB37']} == {('15 Perfect Part', 'Pluto')}, 'BB37 Beverley holders')
    pc7 = [x for c in bres['BB37'] for x in c['cells']]
    pn7 = [n for c in bres['BB37'] for n in c['notes']]
    for w in ('S Pluto → J Pluto RA 61.718584', 'S Pluto – S Pallas RA 61.792827', 'S Pallas → J Pluto RA 0.074243', 'S Sun – S Pluto Dec contraparallel 0.003798'):
        check(any(x.startswith(w) for x in pc7), f'BB37 Perfect Part Pluto cell {w}')
    check(any('may be geometry' in n for n in pn7) and any('S Venus – S Pluto Dec contraparallel' in n for n in pn7)
          and any('>= 80 (88.6)' in n for n in pn7), 'BB37 Perfect Part notes')
    check({(c['runner'], c['body']) for c in bres['BB38']} == {('15 Perfect Part', 'Juno')}, 'BB38 Beverley holders')
    jc = [x for c in bres['BB38'] for x in c['cells']]
    jn = [n for c in bres['BB38'] for n in c['notes']]
    for w in ('S Fomalhaut – S Juno RA 179.909', 'H Fomalhaut – H Juno RA 17.971', 'J Fomalhaut – J Juno Dec 29.288', 'H Fomalhaut – H Juno Dec 23.999'):
        check(any(x.startswith(w) for x in jc), f'BB38 Perfect Part Juno cell {w}')
    check(any('7/6 septimal minor third (96)' in n for n in jn) and any('6 6th harmonic (96.8' in n for n in jn)
          and any('opposition / conj' in n for n in jn) and any('S Regulus – S Juno' in n for n in jn), 'BB38 Perfect Part notes')
    check({(c['runner'], c['body']) for c in bres['BB39']} == {('15 Perfect Part', 'Makemake')}, 'BB39 Beverley holders')
    mc9 = [x for c in bres['BB39'] for x in c['cells']]
    mn9 = [n for c in bres['BB39'] for n in c['notes']]
    for w in ('S Makemake → J Makemake Dec 12.210086', 'S Mercury – S Chiron Dec 12.216899', 'S Makemake → H Makemake Dec 1.012089',
              'S Chiron – S Sedna Dec 0.996865', 'S Sun → H Makemake Dec 0.106418'):
        check(any(x.startswith(w) for x in mc9), f'BB39 Perfect Part Makemake cell {w}')
    check(any('both charts' in n and 'Chiron' in n for n in mn9) and any('S Mercury – S Makemake Dec 0.056271' in n for n in mn9)
          and any('J Regulus – J Makemake Dec 22.220684' in n for n in mn9),
          'BB39 Perfect Part notes')
    check({(c['runner'], c['body']) for c in bres['BB40']} == {('15 Perfect Part', 'Sedna')}, 'BB40 Beverley holders')
    sc0 = [x for c in bres['BB40'] for x in c['cells']]
    sn0 = [n for c in bres['BB40'] for n in c['notes']]
    for w in ('S Sedna → H Sedna Dec 0.444030', 'S Mars – S Eris RA 0.444842', 'S Mars – S Sedna RA 32.995228',
              'S Eris → J Sedna RA 17.923478', 'S Sun → J Sedna Dec 17.942849'):
        check(any(x.startswith(w) for x in sc0), f'BB40 Perfect Part Sedna cell {w}')
    check(any("Sun on the end's line" in n for n in sn0) and any('S Regulus – S Sedna' in n and 'S Fomalhaut – S Sedna' in n for n in sn0)
          and any('19.914709 20 1/20 cut' in n for n in sn0), 'BB40 Perfect Part notes')
    check({(c['runner'], c['body']) for c in bres['BB32b']} == {('15 Perfect Part', 'Sun')}, 'BB32b Beverley holders')
    pc = [x for c in bres['BB32b'] for x in c['cells']]
    pn = [n for c in bres['BB32b'] for n in c['notes']]
    for w in ('J Regulus – J Sun Dec 5.552598', 'S Venus → J Sun Dec 5.551267', 'S Venus – S Sun Dec 0.187596',
              'S Venus – S Sun RA 1.137027', 'H Antares – H Sun RA 133.224682', 'S Venus – S Pluto RA 133.520006',
              'S Pluto – S Sun Dec contraparallel 0.003798', 'J Aldebaran – J Sun Dec 1.010907', 'S Chiron – S Sedna Dec 0.996865'):
        check(any(x.startswith(w) for x in pc), f'BB32b Perfect Part Sun cell {w}')
    check(any('both planes' in n for n in pn) and any('0.0013' in n for n in pn) and any('third royal star' in n for n in pn),
          'BB32b Perfect Part watch notes (both planes, gap 0.0013, third royal star)')
    check({(c['runner'], c['body']) for c in bres['BB42']} == {('01 Aviation Time', 'Uranus'), ('15 Perfect Part', 'Sun')}, 'BB42 Beverley holders')
    check(bres['BB44'] == [], 'BB44 Beverley: no holder')
    check(bres['BB45'] == [] and bres['BB46'] == [], 'BB45 / BB46 Beverley: no holder')
    check({(c['runner'], c['body']) for c in bres['BB47']} == {('14 Havana White', 'Rahu')}, 'BB47 Beverley holders')
    check(bres['BB49'] == [], 'BB49 Beverley: no holder')
    check(bres['BB51'] == [], 'BB51 Beverley: no holder')
    check(bres['BB52'] == [], 'BB52 Beverley: no holder')
    check({(c['runner'], c['body']) for c in bres['BB54']} == {('04 Invincible Annice', 'Gonggong'), ('07 Mademoiselle', 'Pallas'),
          ('08 Maw Lam', 'Pluto'), ('14 Havana White', 'Pluto'), ('15 Perfect Part', 'Uranus')}, 'BB54 Beverley holders')
    pp54 = [n for c in bres['BB54'] if c['runner'] == '15 Perfect Part' for n in c['notes']]
    check(any('H Regulus – H Uranus RA 111.240410' in n and 'same-body ratio 10.025899' in n for n in pp54), 'BB54 Perfect Part note')
    check({(c['runner'], c['body']) for c in bres['BB53']} == {('10 Over Spiced', 'Sun'), ('10 Over Spiced', 'Rahu'),
          ('11 Powerful Lady', 'Mercury'), ('11 Powerful Lady', 'Chiron'), ('15 Perfect Part', 'Sun'), ('15 Perfect Part', 'Makemake')}, 'BB53 Beverley holders')
    pp = [x for c in bres['BB53'] if c['runner'] == '15 Perfect Part' and c['body'] == 'Sun' for x in c['cells']]
    for w in ('S Makemake – S Sun RA 122.336114 122.222 ninth', 'J Aldebaran – J Sun RA 22.244169 22.2222 ninth',
              'J Regulus – J Makemake Dec 22.220684 22.2222 ninth'):
        check(any(x.startswith(w) for x in pp), f'BB53 Perfect Part Sun cell {w}')
    check({(c['runner'], c['body']) for c in bres['BB50']} == {('01 Aviation Time', 'Jupiter'), ('08 Maw Lam', 'Saturn')}, 'BB50 Beverley holders')
    check({(c['runner'], c['body']) for c in bres['BB48']} == {('01 Aviation Time', 'Uranus'), ('12 Sands Of Dubai', 'Venus'), ('15 Perfect Part', 'Mars')}, 'BB48 Beverley holders')
    pc8 = [x for c in bres['BB48'] if c['runner'] == '15 Perfect Part' for x in c['cells']]
    for w in ('J Fomalhaut – J Mars RA 48.561123', 'S Rahu – S Sedna RA 48.555037', 'S Rahu – S Mars RA 15.559809',
              'S Sedna – S Mars RA 32.995228', 'S Rahu → J Mars RA 20.997272', 'S Sedna → H Mars Dec 22.238022'):
        check(any(x.startswith(w) for x in pc8), f'BB48 Perfect Part Mars cell {w}')
    check(any('the same pair' in n for c in bres['BB48'] if c['runner'] == '15 Perfect Part' for n in c['notes']), 'BB48 Perfect Part: the same pair reaches H Mars')
    check({(c['runner'], c['body']) for c in bres['BB43']} == {('07 Mademoiselle', 'Pluto'), ('09 Nad Alshiba Snow', 'Pallas'), ('11 Powerful Lady', 'Makemake')}, 'BB43 Beverley holders')
    pc2 = [x for c in bres['BB42'] if c['runner'] == '15 Perfect Part' for x in c['cells']]
    pn2 = [n for c in bres['BB42'] if c['runner'] == '15 Perfect Part' for n in c['notes']]
    for w in ('S Ceres → H Sun RA 88.761547', 'S Ceres → H Sun Dec 35.622637', 'S Ceres → J Sun Dec 44.479694',
              'S Ceres → J Sun RA 114.911447', 'S Ceres – S Sun RA 145.015251'):
        check(any(x.startswith(w) for x in pc2), f'BB42 Perfect Part Sun cell {w}')
    check(len(pc2) == 5 and any('same body does both (Ceres)' in n for n in pn2), 'BB42 Perfect Part cells once, same-body note')
    an2 = [n for c in bres['BB42'] if c['runner'] == '01 Aviation Time' for n in c['notes']]
    check(any('WATCH Haumea: S Haumea → H Uranus Dec is a conj' in n for n in an2), 'BB42 Aviation Time conj watch note')
lres = R.run(XLSX)[2]
YORK = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20240515_york_1545', '20240515_york_1545_bybody.xlsx')
yres = R.run(YORK)[2]
check({(c['runner'], c['body']) for c in yres['BB41']} == {('06 Secret Satire', 'Sun')}, 'BB41 York holders')
yc = [x for c in yres['BB41'] for x in c['cells']]
yn = [n for c in yres['BB41'] for n in c['notes']]
for w in ('H Antares – H Sun Dec 33.335828', 'S Eris – S Sedna RA 33.318658', 'S Eris – S Sun Dec 19.435910', 'S Sedna → H Sun RA 43.994394',
          'J Fomalhaut – J Sun RA 179.631802', 'S Chiron – S Makemake RA 179.671846', 'S Chiron – S Sun Dec 9.683393',
          'S Makemake → J Sun Dec 15.574470', 'S Moon – S Sun Dec 3.214660', 'S Moon → H Sun Dec 8.873957', 'S Moon → J Sun RA 14.437279'):
    check(any(x.startswith(w) for x in yc), f'BB41 Secret Satire Sun cell {w}')
check(any('H Sun – J Sun Dec 0.414204' in n for n in yn) and not any('S Ketu – S Juno' in x for x in yc), 'BB41 Secret Satire notes / open pair left out')
check({(c['runner'], c['body']) for c in lres['BB34'] if any('Sedna is an end' in n for n in c['notes'])} == {('05 Pholas', 'Mercury')}, 'BB34 Lingfield Sedna note on Pholas Mercury')
check({(c['runner'], c['body']) for c in yres['BB42']} == {('06 Secret Satire', 'Mercury')}, 'BB42 York holders')
yc2 = [x for c in yres['BB42'] for x in c['cells']]
yn2 = [n for c in yres['BB42'] for n in c['notes']]
for w in ('S Uranus → H Mercury RA 44.434397', 'S Uranus → H Mercury Dec 17.771076', 'S Uranus → J Mercury RA 137.998721',
          'S Uranus → J Mercury Dec 24.249612', 'S Neptune – S Mercury RA 29.028421', 'S Neptune → H Mercury Dec 2.008908',
          'S Neptune → J Mercury RA 171.002145'):
    check(any(x.startswith(w) for x in yc2), f'BB42 Secret Satire Mercury cell {w}')
check(not any('same body' in n for n in yn2) and not any(x.startswith('S Moon') for x in yc2), 'BB42 Secret Satire: two bodies, no Moon')

check({(c['runner'], c['body']) for c in yres['BB43']} == {('02 Francophone', 'Neptune'), ('06 Secret Satire', 'Venus')}, 'BB43 York holders')
yc3 = [x for c in yres['BB43'] if c['runner'] == '06 Secret Satire' for x in c['cells']]
yn3 = [n for c in yres['BB43'] if c['runner'] == '06 Secret Satire' for n in c['notes']]
for w in ('S Venus → J Venus RA 122.210672', 'S Orcus – S Quaoar RA 122.321615', 'S Orcus – S Venus Dec 29.154476',
          'S Quaoar → H Venus RA 99.840277', 'S Quaoar → J Venus Dec 21.031152'):
    check(any(x.startswith(w) for x in yc3), f'BB43 Secret Satire Venus cell {w}')
check(len(yc3) == 5 and any('1.988915' in n and '7.011677' in n for n in yn3) and not any('S Vesta – S Fomalhaut' in x for x in yc3),
      'BB43 Secret Satire: 5 cells, Regulus both-charts note, open pair left out')
check({(c['runner'], c['body']) for c in yres['BB44']} == {('06 Secret Satire', 'Jupiter')}, 'BB44 York holders')
yc4 = [x for c in yres['BB44'] for x in c['cells']]
yn4 = [n for c in yres['BB44'] for n in c['notes']]
for w in ('H Fomalhaut – H Jupiter Dec 15.529981', 'S Mars – S Jupiter Dec 15.553328', 'S Mars – S Jupiter RA 44.386707',
          'S Mars → H Jupiter RA 44.013073'):
    check(any(x.startswith(w) for x in yc4), f'BB44 Secret Satire Jupiter cell {w}')
check(len(yc4) == 4 and any('same family as the royal line (ninth)' in n for n in yn4)
      and any('WATCH Fomalhaut is also on sky Jupiter' in n and '70.700654' in n for n in yn4), 'BB44 Secret Satire notes')
CAT = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20220406_catterick_1440', '20220406_catterick_1440_bybody.xlsx')
if os.path.exists(CAT):
    cres = R.run(CAT)[2]
    check({(c['runner'], c['body']) for c in cres['BB44']} == {('02 Beluga Gold', 'Gonggong'), ('05 Wotever Next', 'Gonggong')}, 'BB44 Catterick holders')
    wc4 = [x for c in cres['BB44'] if c['runner'] == '05 Wotever Next' for x in c['cells']]
    for w in ('H Fomalhaut – H Gonggong Dec 17.767704', 'S Chiron – S Gonggong Dec 17.747921', 'S Chiron – S Gonggong RA 33.346535',
              'S Chiron → H Gonggong RA 33.963575'):
        check(any(x.startswith(w) for x in wc4), f'BB44 Wotever Next Gonggong cell {w}')
for rid in ('BB45', 'BB46'):
    check({(c['runner'], c['body']) for c in yres[rid]} == {('06 Secret Satire', 'Saturn')}, f'{rid} York holders')
    yc5 = [x for c in yres[rid] for x in c['cells']]
    for w in ('S Saturn → H Saturn RA 34.987581', 'S Mercury → J Saturn RA 34.997610', 'S Mercury → H Saturn Dec 26.177633',
              'S Mercury → H Saturn RA 74.421312'):
        check(any(x.startswith(w) for x in yc5), f'{rid} Secret Satire Saturn cell {w}')
    check((rid == 'BB46') == any(x.startswith('S Fomalhaut – S Saturn Dec 23.011027') for x in yc5), f'{rid} royal cell only in BB46')
if os.path.exists(CAT):
    check(cres['BB45'] == [] and cres['BB46'] == [], 'BB45 / BB46 Catterick: no holder')
    check(cres['BB47'] == [], 'BB47 Catterick: no holder')
    check({(c['runner'], c['body']) for c in cres['BB48']} == {('04 Thakuri', 'Eris')}, 'BB48 Catterick holders')
    check(cres['BB49'] == [], 'BB49 Catterick: no holder')
    check(cres['BB50'] == [], 'BB50 Catterick: no holder')
    check(cres['BB51'] == [], 'BB51 Catterick: no holder')
    check(cres['BB52'] == [], 'BB52 Catterick: no holder')
    check({(c['runner'], c['body']) for c in cres['BB54']} == {('02 Beluga Gold', 'Chiron'), ('02 Beluga Gold', 'Makemake')}, 'BB54 Catterick holders')
    check({(c['runner'], c['body']) for c in cres['BB53']} == {('02 Beluga Gold', 'Chiron'), ('02 Beluga Gold', 'Gonggong'),
          ('03 Capuchinero', 'Mercury'), ('03 Capuchinero', 'Haumea')}, 'BB53 Catterick holders')
check({(c['runner'], c['body']) for c in yres['BB49']} == {('06 Secret Satire', 'Haumea')}, 'BB49 York holders')
yc9 = [x for c in yres['BB49'] for x in c['cells']]
yn9 = [n for c in yres['BB49'] for n in c['notes']]
for w in ('S Antares – S Haumea RA 29.134385', 'S Fomalhaut – S Haumea RA 126.189939', 'S Fomalhaut – S Haumea Dec 44.986331',
          'H Haumea – J Haumea Dec 5.557856', 'S Makemake – S Aldebaran Dec 5.556667', 'S Makemake → H Haumea RA 16.681885'):
    check(any(x.startswith(w) for x in yc9), f'BB49 Secret Satire Haumea cell {w}')
check(len(yc9) == 6 and any('Aldebaran not among them' in n for n in yn9), 'BB49 Secret Satire: 6 cells, Aldebaran not on sky Haumea noted')
check({(c['runner'], c['body']) for c in yres['BB50']} == {('02 Francophone', 'Transpluto'), ('06 Secret Satire', 'Makemake')}, 'BB50 York holders')
yc50 = [x for c in yres['BB50'] if c['runner'] == '06 Secret Satire' for x in c['cells']]
for w in ('H Makemake – J Makemake RA 23.010781', 'S Saturn – S Fomalhaut Dec 23.011027', 'S Juno – S Orcus Dec 23.004886',
          'S Orcus – S Makemake RA 42.044525'):
    check(any(x.startswith(w) for x in yc50), f'BB50 Secret Satire Makemake cell {w}')
check(len(yc50) == 4, 'BB50 Secret Satire Makemake: 4 cells')
check({(c['runner'], c['body']) for c in yres['BB48']} == {('01 Classical Song', 'Ketu'), ('03 Friendly Soul', 'Ketu'), ('04 La Pasionaria', 'Saturn'),
      ('06 Secret Satire', 'Chiron'), ('06 Secret Satire', 'Quaoar'), ('07 Sinology', 'Ketu')}, 'BB48 York holders')
yc8 = [x for c in yres['BB48'] if c['runner'] == '06 Secret Satire' and c['body'] == 'Chiron' for x in c['cells']]
for w in ('H Regulus – H Chiron RA 144.654790', 'S Jupiter – S Makemake RA 144.320722', 'S Jupiter – S Chiron RA 36.007432',
          'S Makemake – S Chiron RA 179.671846', 'S Makemake → H Chiron RA 168.005655', 'S Pluto – S Juno RA 144.681271',
          'S Pluto → J Chiron RA 126.227565'):
    check(any(x.startswith(w) for x in yc8), f'BB48 Secret Satire Chiron cell {w}')
check(len(yc8) == 7 and not any('Ketu' in x for x in yc8), 'BB48 Secret Satire Chiron: 7 cells, the Ketu contraparallel end left out')
check({(c['runner'], c['body']) for c in yres['BB47']} == {('03 Friendly Soul', 'Jupiter'), ('06 Secret Satire', 'Ceres')}, 'BB47 York holders')
yc7 = [x for c in yres['BB47'] if c['runner'] == '06 Secret Satire' for x in c['cells']]
for w in ('H Regulus – H Ceres RA 133.301747', 'S Ketu – S Sedna RA 133.162547', 'S Ketu – S Ceres RA 100.117445',
          'S Sedna → H Ceres RA 41.424683', 'S Juno – S Eris RA 133.132336', 'S Juno → H Ceres RA 141.238361',
          'S Eris → H Ceres RA 8.106026', 'S Ceres – S Juno RA 133.466313'):
    check(any(x.startswith(w) for x in yc7), f'BB47 Secret Satire Ceres cell {w}')
check(not any('contraparallel' in x for x in yc7), 'BB47 Secret Satire: the Eris contraparallel line not used')
check({(c['runner'], c['body']) for c in yres['BB51']} == {('07 Sinology', 'Mercury')}, 'BB51 York holders')
check(yres['BB52'] == [], 'BB52 York: no holder')
check({(c['runner'], c['body']) for c in yres['BB54']} == {('02 Francophone', 'Neptune'), ('06 Secret Satire', 'Rahu')}, 'BB54 York holders')
check(any('crossed ratio 10.017866' in n for c in yres['BB54'] if c['runner'] == '06 Secret Satire' for n in c['notes']), 'BB54 Secret Satire note')
check({(c['runner'], c['body']) for c in yres['BB53']} == {('01 Classical Song', 'Uranus'), ('01 Classical Song', 'Neptune'),
      ('04 La Pasionaria', 'Pluto'), ('04 La Pasionaria', 'Orcus'), ('04 La Pasionaria', 'Quaoar')}, 'BB53 York holders')
Y16 = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20240515_york_1615', '20240515_york_1615_bybody.xlsx')
if os.path.exists(Y16):
    y16 = R.run(Y16)[2]
    check({(c['runner'], c['body']) for c in y16['BB51']} == {('05 Respectful', 'Vesta'), ('13 Diligent Resdev', 'Venus')}, 'BB51 York 16:15 holders')
    dc51 = [x for c in y16['BB51'] if c['runner'] == '13 Diligent Resdev' for x in c['cells']]
    for w in ('H Antares – H Venus Dec 3.265036', 'S Jupiter – S Makemake Dec 3.243443', 'J Antares – J Venus RA 44.418360',
              'S Mars – S Jupiter RA 44.377122', 'S Jupiter – S Venus RA 7.786496', 'S Jupiter – S Venus Dec 1.981299'):
        check(any(x.startswith(w) for x in dc51), f'BB51 Diligent Resdev Venus cell {w}')
    check({(c['runner'], c['body']) for c in y16['BB52']} == {('13 Diligent Resdev', 'Venus'), ('13 Diligent Resdev', 'Uranus')}, 'BB52 York 16:15 holders')
    for c in y16['BB52']:
        for w in ('H Antares – H Venus Dec 3.265036', 'S Venus – S Uranus RA 3.234200', 'H Aldebaran – H Uranus Dec 3.265338'):
            check(any(x.startswith(w) for x in c['cells']), f"BB52 Diligent Resdev {c['body']} cell {w}")
        check(len(c['cells']) == 3, f"BB52 Diligent Resdev {c['body']}: 3 cells")
    check(len(dc51) == 6 and not any('Saturn – S Pluto' in x for x in dc51), 'BB51 Diligent Resdev: 6 cells, the Saturn – Pluto pair (no shared body) left out')
    check({(c['runner'], c['body']) for c in y16['BB53']} == {('01 Mortlake', 'Uranus'), ('01 Mortlake', 'Neptune'), ('05 Respectful', 'Venus'),
          ('05 Respectful', 'Rahu'), ('12 Quiet Resolve', 'Haumea'), ('12 Quiet Resolve', 'Quaoar'), ('13 Diligent Resdev', 'Venus'),
          ('13 Diligent Resdev', 'Rahu'), ('13 Diligent Resdev', 'Uranus')}, 'BB53 York 16:15 holders')
    dr = [x for c in y16['BB53'] if c['runner'] == '13 Diligent Resdev' and c['body'] == 'Rahu' for x in c['cells']]
    for w in ('S Venus – S Rahu RA 33.951817 21×φ golden', 'H Aldebaran – H Rahu Dec 6.493563 4×φ golden',
              'H Fomalhaut – H Venus Dec 6.460070 4×φ golden'):
        check(any(x.startswith(w) for x in dr), f'BB53 Diligent Resdev Rahu cell {w}')
    check({(c['runner'], c['body']) for c in y16['BB54']} == {('04 Elmonjed', 'Ketu'), ('06 True Promise', 'Rahu'), ('11 On Point', 'Mars'),
          ('12 Quiet Resolve', 'Uranus'), ('13 Diligent Resdev', 'Rahu'), ('14 Misemerald', 'Rahu')}, 'BB54 York 16:15 holders')
    d54 = [c for c in y16['BB54'] if c['runner'] == '13 Diligent Resdev']
    check(len(d54) == 1 and d54[0]['cells'] == ['H Aldebaran – H Rahu Dec 6.493563 4×φ golden (33.87)', 'S Rahu → H Rahu RA 64.936805 (no family)']
          and any('crossed ratio 10.000181 on 10 (99.64)' in n for n in d54[0]['notes']), 'BB54 Diligent Resdev cells and note')
print(f'{ok}/{ok + bad} checks passed')
sys.exit(1 if bad else 0)
