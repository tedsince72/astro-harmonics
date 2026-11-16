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
    'BB56': set(),
    'BB57': {('04 Nirodha', 'Pallas')},
    'BB58': {('04 Nirodha', 'Pallas')},
    'BB59': {('05 Pholas', 'Pallas')},
    'BB60': {('05 Pholas', 'Pallas')},
    'BB61': set(),
    'BB62': {('05 Pholas', 'J chart')},
    'BB63': {('05 Pholas', 'Pallas')},
    'BB64': set(),
    'BB65': set(),
    'BB66': set(),
    'BB67': {('05 Pholas', 'runner')},
    'BB1b': {('05 Pholas', 'Mercury')},
    'BB68': {('02 Fizzy Feet', 'Jupiter'), ('05 Pholas', 'Mercury'), ('06 Shimmering Dawn', 'Vesta')},
    'BB55': {('01 Arafi', 'Gonggong'), ('01 Arafi', 'Venus'), ('04 Nirodha', 'Saturn'), ('05 Pholas', 'Pallas')},
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
    check({(c['runner'], c['body']) for c in hres['BB56']} == {('02 Ventura Flame', 'Venus'), ('07 Ishvara', 'Juno')}, 'BB56 Haydock holders')
    ij56 = [x for c in hres['BB56'] if c['runner'] == '07 Ishvara' for x in c['cells']]
    check(any(x.startswith('S Fomalhaut – S Juno RA 155.553196 155.556 ninth') for x in ij56) and any(x.startswith('S Sun → H Juno RA 155.817127') for x in ij56), 'BB56 Ishvara cells')
    check({(c['runner'], c['body']) for c in hres['BB57']} == {('02 Ventura Flame', 'Mars'), ('04 Royal Context', 'Sedna'), ('06 Birkenhead', 'Mars'), ('07 Ishvara', 'Mercury'), ('09 Garsman', 'Chiron')}, 'BB57 Haydock holders')
    check(hres['BB58'] == [], 'BB58 Haydock: no holder')
    check(hres['BB59'] == [], 'BB59 Haydock: no holder')
    check(hres['BB60'] == [], 'BB60 Haydock: no holder')
    check({(c['runner'], c['body']) for c in hres['BB55']} == {('01 Magical Max', 'Jupiter'), ('02 Ventura Flame', 'Vesta'), ('04 Royal Context', 'Gonggong'),
          ('04 Royal Context', 'Makemake'), ('06 Birkenhead', 'Jupiter'), ('07 Ishvara', 'Pallas'), ('11 Mews House', 'Saturn')}, 'BB55 Haydock holders')
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
    check(bres['BB56'] == [], 'BB56 Beverley: no holder')
    check({(c['runner'], c['body']) for c in bres['BB57']} == {('14 Havana White', 'Pallas')}, 'BB57 Beverley holders')
    check({(c['runner'], c['body']) for c in bres['BB58']} == {('15 Perfect Part', 'Mercury')}, 'BB58 Beverley holders')
    check(bres['BB59'] == [], 'BB59 Beverley: no holder')
    check({(c['runner'], c['body']) for c in bres['BB60']} == {('02 Brazilian Belle', 'Quaoar'), ('07 Mademoiselle', 'Gonggong'), ('13 Storm Call', 'Gonggong'), ('14 Havana White', 'Gonggong'), ('15 Perfect Part', 'Gonggong')}, 'BB60 Beverley holders')
    check({(c['runner'], c['body']) for c in bres['BB55']} == {('04 Invincible Annice', 'Pluto'), ('07 Mademoiselle', 'Gonggong'), ('08 Maw Lam', 'Ceres'),
          ('13 Storm Call', 'Gonggong'), ('13 Storm Call', 'Mars'), ('14 Havana White', 'Gonggong'), ('15 Perfect Part', 'Gonggong'), ('15 Perfect Part', 'Orcus')}, 'BB55 Beverley holders')
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
    check({(c['runner'], c['body']) for c in cres['BB56']} == {('02 Beluga Gold', 'Mars')}, 'BB56 Catterick holders')
    check({(c['runner'], c['body']) for c in cres['BB57']} == {('05 Wotever Next', 'Sun')}, 'BB57 Catterick holders')
    w57 = [x for c in cres['BB57'] for x in c['cells']]
    check(any(x.startswith('H Regulus – H Sun Dec 6.000669 6 whole') for x in w57) and any(x.startswith('S Moon – S Rahu Dec 6.006606') for x in w57) and any(x.startswith('J Regulus – J Sun RA 166.917198 166.667 ninth') for x in w57) and any(x.startswith('S Rahu – S Haumea RA 166.802333') for x in w57), 'BB57 Wotever Next cells')
    check({(c['runner'], c['body']) for c in cres['BB58']} == {('05 Wotever Next', 'Neptune')}, 'BB58 Catterick holders')
    w58 = [x for c in cres['BB58'] for x in c['cells']]
    check(any(x.startswith('H Fomalhaut – H Neptune RA 3.992391 4 whole') for x in w58) and any(x.startswith('J Fomalhaut – J Neptune RA 59.894054 37×φ golden') for x in w58), 'BB58 Wotever Next cells')
    check({(c['runner'], c['body']) for c in cres['BB59']} == {('05 Wotever Next', 'Rahu')}, 'BB59 Catterick holders')
    w59 = [x for c in cres['BB59'] for x in c['cells']]
    check(any(x.startswith('J Regulus – J Rahu RA 166.979293') for x in w59) and any(x.startswith('S Regulus – S Rahu Dec 6.466238') for x in w59), 'BB59 Wotever Next cells')
    check({(c['runner'], c['body']) for c in cres['BB60']} == {('05 Wotever Next', 'Chiron')}, 'BB60 Catterick holders')
    w60 = [x for c in cres['BB60'] for x in c['cells']]
    check(any(x.startswith('H Fomalhaut – H Chiron Dec 33.381885') for x in w60) and any(x.startswith('S Chiron – S Gonggong RA 33.346535') for x in w60) and any(x.startswith('S Vesta → J Chiron Dec 33.314388') for x in w60), 'BB60 Wotever Next cells')
    check({(c['runner'], c['body']) for c in cres['BB55']} == {('02 Beluga Gold', 'Chiron')}, 'BB55 Catterick holders')
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
check(yres['BB56'] == [], 'BB56 York: no holder')
check({(c['runner'], c['body']) for c in yres['BB57']} == {('01 Classical Song', 'Sun'), ('03 Friendly Soul', 'Uranus'), ('07 Sinology', 'Mercury')}, 'BB57 York holders')
check(yres['BB58'] == [], 'BB58 York: no holder')
check({(c['runner'], c['body']) for c in yres['BB59']} == {('06 Secret Satire', 'Ceres'), ('06 Secret Satire', 'Jupiter')}, 'BB59 York holders')
check({(c['runner'], c['body']) for c in yres['BB60']} == {('01 Classical Song', 'Gonggong'), ('04 La Pasionaria', 'Gonggong'), ('06 Secret Satire', 'Ceres')}, 'BB60 York holders')
check({(c['runner'], c['body']) for c in yres['BB55']} == {('01 Classical Song', 'Gonggong'), ('01 Classical Song', 'Ketu'), ('04 La Pasionaria', 'Gonggong'),
      ('06 Secret Satire', 'Ceres')}, 'BB55 York holders')
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
    check({c['runner'] for c in y16['BB55']} == {'03 Blue Prince', '05 Respectful', '06 True Promise', "07 Thursday's Child", "08 Ziggy's Condor",
          '12 Quiet Resolve', '13 Diligent Resdev', '14 Misemerald', '15 Ribble Radiant'}, 'BB55 York 16:15 runners')
    d55 = [x for c in y16['BB55'] if c['runner'] == '13 Diligent Resdev' and c['body'] == 'Pallas' for x in c['cells']]
    for w in ('H Aldebaran – H Pallas Dec 16.990885 17 whole', 'S Pallas – S Sedna Dec 16.998976 17 whole',
              'S Sedna → J Pallas Dec 22.655851 14×φ golden', 'S Sedna → J Pallas RA 40.982065 41 whole'):
        check(any(x.startswith(w) for x in d55), f'BB55 Diligent Resdev Pallas cell {w}')
    check({(c['runner'], c['body']) for c in y16['BB56']} == {('06 True Promise', 'Vesta'), ('13 Diligent Resdev', 'Vesta'), ('14 Misemerald', 'Vesta')}, 'BB56 York 16:15 holders')
    d56 = [x for c in y16['BB56'] if c['runner'] == '13 Diligent Resdev' for x in c['cells']]
    check(any(x.startswith('S Fomalhaut – S Vesta RA 122.236525 122.222 ninth') for x in d56) and any(x.startswith('S Sun → H Vesta RA 122.087456 122.222 ninth') for x in d56), 'BB56 Diligent Resdev cells')
    check({(c['runner'], c['body']) for c in y16['BB57']} == {('03 Blue Prince', 'Sun'), ('05 Respectful', 'Transpluto'), ('05 Respectful', 'Vesta'), ("07 Thursday's Child", 'Sun'), ('13 Diligent Resdev', 'Venus')}, 'BB57 York 16:15 holders')
    check({(c['runner'], c['body']) for c in y16['BB58']} == {("08 Ziggy's Condor", 'Uranus')}, 'BB58 York 16:15 holders')
    check({(c['runner'], c['body']) for c in y16['BB59']} == {('03 Blue Prince', 'Vesta'), ("08 Ziggy's Condor", 'Eris'), ('14 Misemerald', 'Vesta')}, 'BB59 York 16:15 holders')
check({(c['runner'], c['body']) for c in y16['BB60']} == {('03 Blue Prince', 'Makemake'), ("07 Thursday's Child", 'Gonggong'), ('12 Quiet Resolve', 'Gonggong')}, 'BB60 York 16:15 holders')
# Fontwell 15:30 6 Oct 2023 (BB61 origin, Kilcummin)
for nm, rr in (('Haydock', hres), ('Beverley', bres), ('York', yres), ('York 16:15', y16)):
    check(rr['BB61'] == [], f'BB61 {nm}: no holder')
check(cres['BB61'] == [], 'BB61 Catterick: no holder')
FW = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20231006_fontwell_1530', '20231006_fontwell_1530_bybody.xlsx')
if os.path.exists(FW):
    fw = R.run(FW)[2]
    check({(c['runner'], c['body']) for c in fw['BB61']} == {('03 Kilcummin', 'Uranus')}, 'BB61 Fontwell holders')
    k = [x for c in fw['BB61'] for x in c['cells']]
    for w in ('J Regulus – J Uranus Dec 33.354156', 'H Uranus – J Uranus Dec 33.347478', 'S Uranus – S Quaoar Dec 33.318289', 'S Quaoar → J Uranus RA 22.187459'):
        check(any(x.startswith(w) for x in k), f'BB61 Kilcummin cell {w}')
    n = [x for c in fw['BB61'] for x in c['notes']]
    check(any('K2: Quaoar on natal Uranus' in x and 'K3: yes' in x for x in n), 'BB61 Kilcummin K2 / K3 notes')
    check({c['runner'] for c in fw['BB59']} == {'03 Kilcummin'}, 'BB59 Fontwell holders')
    check({(c['runner'], c['body']) for c in fw['BB62']} == {('03 Kilcummin', 'J chart'), ('04 Logistical', 'J chart')}, 'BB62 Fontwell holders')
    check(any('Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Nodes, Chiron, Haumea, Transpluto' in x for c in fw['BB62'] if c['runner'] == '03 Kilcummin' for x in c['notes']), 'BB62 Kilcummin bodies')
check({(c['runner'], c['body']) for c in hres['BB62']} == {('11 Mews House', 'J chart')}, 'BB62 Haydock holders')
check({(c['runner'], c['body']) for c in y16['BB62']} == {('13 Diligent Resdev', 'H chart')}, 'BB62 York 16:15 holders')
for nm, rr in (('Beverley', bres), ('York', yres), ('Catterick', cres)):
    check(rr['BB62'] == [], f'BB62 {nm}: no holder')
NC = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20210802_newcastle_aw_1633', '20210802_newcastle_aw_1633_bybody.xlsx')
if os.path.exists(NC):
    nc = R.run(NC)[2]
    check({c['runner'] for c in nc['BB63']} == {'01 Dubai Souq', '02 Athmad', '03 Raise The Roof', '06 Tricolore'}, 'BB63 Newcastle holders')
    k = [x for c in nc['BB63'] if c['runner'] == '02 Athmad' and c['body'] == 'Makemake' for x in c['cells']]
    for w in ('H Regulus – H Makemake RA 42.364', 'S Mars – S Makemake RA 42.397', 'S Mars → H Makemake RA 39.991'):
        check(any(x.startswith(w) for x in k), f'BB63 Athmad cell {w}')
for nm, rr, want in (('Haydock', hres, {'01 Magical Max', '04 Royal Context', '06 Birkenhead'}), ('Beverley', bres, {'02 Brazilian Belle'}),
                     ('York 15:45', yres, {'06 Secret Satire'}), ('Catterick', cres, {'02 Beluga Gold', '03 Capuchinero', '05 Wotever Next'})):
    check({c['runner'] for c in rr['BB63']} == want, f'BB63 {nm} holders')
if os.path.exists(FW):
    check({c['runner'] for c in fw['BB63']} == {'03 Kilcummin', '04 Logistical', '05 Makanao'}, 'BB63 Fontwell holders')
for nm, rr, want in (('Haydock', hres, {('06 Birkenhead', 'Pluto'), ('07 Ishvara', 'Juno'), ('08 Dancin Inthestreet', 'Chiron')}),
                     ('Beverley', bres, {('03 Call Me Harswell', 'Jupiter')}), ('York 15:45', yres, set()), ('Catterick', cres, set()),
                     ('York 16:15', y16, {('10 Lady Pink Rose', 'Ceres'), ('12 Quiet Resolve', 'Jupiter')})):
    check({(c['runner'], c['body']) for c in rr['BB64']} == want, f'BB64 {nm} holders')
k = [x for c in hres['BB64'] if c['runner'] == '07 Ishvara' for x in c['cells']]
for w in ('S Fomalhaut – S Juno RA 155.553', 'S Sun → H Juno RA 155.817', 'S Sun → H Juno Dec 33.367'):
    check(any(x.startswith(w) for x in k), f'BB64 Ishvara cell {w}')
if os.path.exists(NC):
    check({(c['runner'], c['body']) for c in nc['BB64']} == {('01 Dubai Souq', 'Ceres'), ('02 Athmad', 'Venus')}, 'BB64 Newcastle holders')
    k = [x for c in nc['BB64'] if c['runner'] == '02 Athmad' for x in c['cells']]
    for w in ('S Fomalhaut – S Venus Dec 37.229', 'S Uranus → J Venus Dec 37.220', 'S Uranus → J Venus RA 177.449'):
        check(any(x.startswith(w) for x in k), f'BB64 Athmad cell {w}')
if os.path.exists(FW):
    check(fw['BB64'] == [], 'BB64 Fontwell: no holder')
# BB65 (Eddie, 16 Nov 2026): royal line on the horse's natal Sun, Dec, >= 90; RA-only = watch-only note A
hold = lambda rr: {(c['runner'], c['body']) for c in rr['BB65'] if not c['watch_only']}
watch = lambda rr: {c['runner'] for c in rr['BB65'] if c['watch_only']}
check(hold(yres) == {('06 Secret Satire', 'Sun')} and watch(yres) == {'04 La Pasionaria'}, 'BB65 York 15:45')
check(any(x.startswith('H Antares – H Sun Dec 33.3358') for c in yres['BB65'] for x in c['cells']), 'BB65 Secret Satire cell')
if os.path.exists(CAT):
    check(hold(cres) == {('05 Wotever Next', 'Sun')}, 'BB65 Catterick')
check(hold(bres) == {('09 Nad Alshiba Snow', 'Sun')}, 'BB65 Beverley')
check(hold(hres) == set() and hold(lres) == set(), 'BB65 Haydock, Lingfield: no holder')
DON = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20220716_doncaster_1845', '20220716_doncaster_1845_bybody.xlsx')
if os.path.exists(DON):
    dn = R.run(DON)[2]
    check(hold(dn) == {('05 Novakai', 'Sun')}, 'BB65 Doncaster')
    check(any(x.startswith('H Fomalhaut – H Sun Dec 24.140652') for c in dn['BB65'] for x in c['cells']), 'BB65 Novakai cell')
# BB66 (Eddie, 16 Nov 2026): H X – J X Dec >= 90 and a sky body (not Moon, not royal) on natal X Dec >= 90
h66 = lambda rr: {(c['runner'], c['body']) for c in rr['BB66']}
check(h66(yres) == {('06 Secret Satire', 'Ceres')}, 'BB66 York 15:45')
check(h66(hres) == {('02 Ventura Flame', 'Haumea')} and h66(lres) == set(), 'BB66 Haydock, Lingfield')
check(h66(bres) == {('07 Mademoiselle', 'Venus')}, 'BB66 Beverley')
if os.path.exists(CAT):
    check(h66(cres) == {('04 Thakuri', 'Pallas'), ('05 Wotever Next', 'Ceres')}, 'BB66 Catterick')
if os.path.exists(FW):
    check(h66(fw) == {('05 Makanao', 'Mars')}, 'BB66 Fontwell')
if os.path.exists(DON):
    check(h66(dn) == {('04 Mother India', 'Sun'), ('05 Novakai', 'Eris')}, 'BB66 Doncaster')
    k = [x for c in dn['BB66'] if c['runner'] == '05 Novakai' for x in c['cells']]
    check('H Eris – J Eris Dec 10.001156 10 whole (94.22)' in k and 'S Pluto → H Eris Dec 21.033633 13×φ golden (97.5)' in k, 'BB66 Novakai cells')
# BB67 (Eddie, 16 Nov 2026): at least 2 of BB3 + BB63, BB3 + BB54, BB59
h67 = lambda rr: {c['runner'] for c in rr['BB67']}
check(h67(yres) == {'06 Secret Satire'} and h67(hres) == {'06 Birkenhead'} and h67(bres) == set(), 'BB67 York 15:45, Haydock, Beverley')
if os.path.exists(CAT):
    check(h67(cres) == {'05 Wotever Next'}, 'BB67 Catterick')
if os.path.exists(FW):
    check(h67(fw) == {'03 Kilcummin'}, 'BB67 Fontwell')
if os.path.exists(DON):
    check(h67(dn) == set(), 'BB67 Doncaster: no holder')
CAR = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20220707_carlisle_1630', '20220707_carlisle_1630_bybody.xlsx')
if os.path.exists(CAR):
    cr = R.run(CAR)[2]
    check(h67(cr) == {'06 Whitefeathersfall'} and any('3 of 3' in n for c in cr['BB67'] for n in c['notes']), 'BB67 Carlisle Whitefeathersfall 3 of 3')
    hold_all = {}
    for rid, cs in cr.items():
        for c in cs:
            if not c['watch_only']: hold_all.setdefault(c['runner'], set()).add(rid)
    check(all((sum(set(cb) <= hold_all.get(x, set()) for cb in (('BB3', 'BB63'), ('BB3', 'BB54'), ('BB59',))) >= 2) == (x in h67(cr))
              for x in hold_all), 'BB67 Carlisle = the combo count for every runner')
# BB1b (Eddie, 16 Nov 2026): BB1 with royal line, pair and both natal ends on number families (ends >= 50)
h1b = lambda rr: {(c['runner'], c['body']) for c in rr['BB1b']}
check(all(h1b(x) == set() for x in (yres, hres, bres)), 'BB1b York 15:45, Haydock, Beverley: no holder')
NOT = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20220613_nottingham_1750', '20220613_nottingham_1750_bybody.xlsx')
if os.path.exists(NOT):
    nt = R.run(NOT)[2]
    check(h1b(nt) == {('02 The Dunkirk Lads', 'Mars')}, 'BB1b Nottingham: The Dunkirk Lads Mars only')
    k = [x for c in nt['BB1b'] for x in c['cells']]
    check('S Ketu → H Mars RA 161.811042 100φ phi power (96.85)' in k and 'S Chiron → H Mars RA 17.792905 11×φ golden (83.12)' in k, 'BB1b Dunkirk cells')
    check(all(c['runner'] in {x['runner'] for x in nt['BB1']} for c in nt['BB1b']), 'BB1b holders are BB1 holders')
# BB68 (Eddie, 16 Nov 2026): V3d - a sky body splits the same-body line S X -> c X in Dec, pieces >= 90 / >= 50
h68 = lambda rr: {(c['runner'], c['body']) for c in rr['BB68']}
check(h68(yres) == {('03 Friendly Soul', 'Jupiter'), ('04 La Pasionaria', 'Mars'), ('06 Secret Satire', 'Juno')}, 'BB68 York 15:45')
RIP = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '20220616_ripon_1525', '20220616_ripon_1525_bybody.xlsx')
if os.path.exists(RIP):
    rp = R.run(RIP)[2]
    check(h68(rp) == {('04 Society Red', 'Venus'), ('04 Society Red', 'Saturn')}, 'BB68 Ripon: Society Red only')
    k = [x for c in rp['BB68'] if c['body'] == 'Venus' for x in c['cells']]
    check('S Sedna – S Venus Dec 8.090457 5×φ golden (99.11)' in k and 'S Sedna → H Venus Dec 25.005224 25 whole (73.88)' in k
          and 'S Venus → H Venus Dec contraparallel 0.014060 cp contraparallel (95.31)' in k, 'BB68 Society Red Venus cells + mirror')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'scans'))
import bb_fieldcheck_split as SP
for race, _ in SP.RACES:
    pth = os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', race, f'{race}_bybody.xlsx')
    if not os.path.exists(pth):
        continue
    data = R.load(pth)
    v3d = {run for run, D in data.items() for X, d in D.items() for sp in SP.splits(X, d)
           if 'V3d' in SP.tags(sp, set(D) | {'Rahu', 'Ketu'})}
    check({c['runner'] for c in R.run(pth)[2]['BB68']} == v3d, f'BB68 = scan V3d {race}')
print(f'{ok}/{ok + bad} checks passed')
sys.exit(1 if bad else 0)
