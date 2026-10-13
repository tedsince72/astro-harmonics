#!/usr/bin/env python3
"""jr2_check.py - JR v2/v3 acceptance tests (docs/classic/jupiter_reader_design.md section 7; + JR v3 chain test, section 11). Runs tools/jupiter_reader.py on the
six races, then checks each expected item in the runner's P##.json (found by horse name; no results opened).
Exit 1 if any check fails."""
import json, glob, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
RES = []


def check(name, ok, detail):
    RES.append(ok)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")


def runner(race, horse):
    for f in sorted(glob.glob(f'docs/classic/{race}/jupiter/P[0-9][0-9].json')):
        d = json.load(open(f))
        if d['horse'] == horse:
            return d
    raise SystemExit(f'{horse} not found in {race}')


def find(hs, **kw):
    return [h for h in hs if all(h.get(k) == v for k, v in kw.items())]


def r5(x):
    return round(x, 5)


RACES = [('lingfield_aw_1435_20210402', 'Pholas'), ('fontwell_1645_20210914', 'Pixie Loc'), ('kempton_aw_1440_20210904', 'Hamish'),
         ('goodwood_1853_20210827', 'Madame Tantzy'), ('nottingham_1530_20220601', 'Dynamic Force'), ('redcar_1515_20211015', 'Present Moment'),
         ('newcastle_aw_1330_20220102', 'Venturous')]

for race, horse in RACES:
    r = subprocess.run([sys.executable, 'tools/jupiter_reader.py', race], capture_output=True, text=True)
    print(f'run {race}: ' + (r.stdout.strip().splitlines()[-1] if r.returncode == 0 else 'FAILED\n' + r.stdout + r.stderr))
    if r.returncode:
        RES.append(False)

print('\nLingfield 14:35 2 Apr 2021 (Pholas / Holly Doyle)')
d = runner('lingfield_aw_1435_20210402', 'Pholas'); hs = d['hits']
h = find(hs, m='D3', pts=['S Jupiter', 'J Jupiter'], target='1.618')
ok = len(h) == 1 and r5(h[0]['value']) == 1.61887 and round(abs(h[0]['offset']), 4) == 0.0515 and h[0]['level'] == 'near' \
    and r5(max(h[0]['num'], h[0]['den'])) == 23.29537 and r5(min(h[0]['num'], h[0]['den'])) == 14.38992 and 'golden section' in h[0]['desc']
check('D3 J/S Jupiter Equator phi, near', ok, (f"{max(h[0]['num'], h[0]['den']):.5f} / {min(h[0]['num'], h[0]['den']):.5f} = {h[0]['value']:.5f}, off {h[0]['offset']:+.4f}%, "
                                              f"{h[0]['level']}; {h[0]['desc']}") if h else 'missing')
import csv
pos = {(r['chart'], r['body']): float(r['dec']) for r in csv.DictReader(open('docs/classic/lingfield_aw_1435_20210402/jupiter/positions.csv'))
       if r['body'] == 'Jupiter'}
ok = r5(pos[('S', 'Jupiter')]) == -14.38992 and r5(pos[('H', 'Jupiter')]) == -7.06006 and r5(pos[('J', 'Jupiter')]) == -23.29537
check('Jupiter Decs S / H / J', ok, f"{pos[('S', 'Jupiter')]:.5f} / {pos[('H', 'Jupiter')]:.5f} / {pos[('J', 'Jupiter')]:.5f}")

print('\nFontwell 16:45 2021 (Pixie Loc / Ben Jones)')
hs = runner('fontwell_1645_20210914', 'Pixie Loc')['hits']
h = find(hs, m='C3', pts=['S Jupiter', 'J Jupiter'], plane='RA', target='59')
check('C3 J Jupiter moved RA 59', len(h) == 1 and r5(h[0]['value']) == 58.99549 and h[0]['level'] == 'strict',
      f"{h[0]['value']:.5f} -> 59, {h[0]['level']}" if h else 'missing')

print('\nKempton 14:40 2021 (Hamish)')
hs = runner('kempton_aw_1440_20210904', 'Hamish')['hits']
h = find(hs, m='D3', pts=['S Jupiter', 'H Jupiter'], target='16/5')
check('D3 Equator S/H 16/5 (0.0019%)', len(h) == 1 and round(abs(h[0]['offset']), 4) == 0.0019 and h[0]['level'] == 'strict',
      f"{h[0]['value']:.5f}, off {h[0]['offset']:+.4f}%, {h[0]['level']}" if h else 'missing')

print('\nGoodwood 18:53 2021 (Madame Tantzy / Dobie)')
hs = runner('goodwood_1853_20210827', 'Madame Tantzy')['hits']
h = find(hs, m='D3', pts=['H Jupiter', 'J Jupiter'], target='11/9')
check('D3 Equator H/J 11/9 (0.0038%)', len(h) == 1 and round(abs(h[0]['offset']), 4) == 0.0038 and h[0]['level'] == 'strict',
      f"{h[0]['value']:.5f}, off {h[0]['offset']:+.4f}%, {h[0]['level']}" if h else 'missing')

print('\nNottingham 15:30 2022 (Dynamic Force / Dawson)')
hs = runner('nottingham_1530_20220601', 'Dynamic Force')['hits']
h = [x for x in find(hs, m='C4') if x['pts'] == ['S Jupiter', 'J Vesta']
     and [p['target'] for p in x['parts']] == ['18', '137/9']]
ok = len(h) == 1 and round(abs(h[0]['parts'][0]['offset']), 5) == 0.00414 and round(abs(h[0]['parts'][1]['offset']), 5) == 0.00046 \
    and h[0]['level'] == 'strict'
check('C4 S Jupiter -> J Vesta RA 18 + Dec 137/9', ok,
      (f"RA off {h[0]['parts'][0]['offset']:+.5f}, Dec off {h[0]['parts'][1]['offset']:+.5f}, {h[0]['level']}") if h else 'missing')

print('\nRedcar 15:15 2021 (Present Moment / Hogan)')
hs = runner('redcar_1515_20211015', 'Present Moment')['hits']
h = [x for x in find(hs, m='C5') if x['parts'][0]['pts'] == ['H Ceres', 'J Jupiter'] and x['parts'][1]['plane'] == 'GC'
     and x['parts'][1]['target'] == '640/9']
ok = len(h) == 1 and round(h[0]['parts'][0]['Dec'], 4) == 0.1131 and r5(h[0]['parts'][1]['value']) == 71.11139 and h[0]['level'] == 'strict'
check('C5 H Ceres – J Jupiter Dec 0.1131; S Jupiter -> H Ceres GC 640/9', ok,
      (f"link Dec {h[0]['parts'][0]['Dec']:.4f}; GC {h[0]['parts'][1]['value']:.5f}, {h[0]['level']}") if h else 'missing')

print('\nNewcastle AW 13:30 2022 (Venturous; King Of Stars) — JR v3 chain')
V = runner('newcastle_aw_1330_20220102', 'Venturous')
K = runner('newcastle_aw_1330_20220102', 'King Of Stars')
cv = [h for h in V['hits'] if h['m'] == 'CH' and h['root'] == 'S Uranus–S Venus' and h['root_plane'] == 'Dec' and h['natal'] == 'H Jupiter']
ck = [h for h in K['hits'] if h['m'] == 'CH' and h['root'] == 'S Uranus–S Venus' and h['root_plane'] == 'Dec' and h['natal'] == 'J Jupiter']
ok = len(cv) == 1 and r5(cv[0]['root_value']) == 32.9937 and cv[0]['level'] == 'near' and 'both-near' not in cv[0]['flags'] and \
    sorted((r5(p['value']), p['level']) for p in cv[0]['parts']) == [(7.00821, 'near'), (40.00191, 'strict')]
check('CH Venturous: sky Uranus–Venus Dec 32.9937 -> H Jupiter at 7 / 40 (near + strict = near)', ok,
      (f"root {cv[0]['root_value']:.5f} ({cv[0]['root_relation']}), parts " +
       ', '.join(f"{p['value']:.5f} {p['level']}" for p in cv[0]['parts']) + f", {cv[0]['level']}") if cv else 'missing')
ok = len(ck) == 1 and sorted(r5(p['value']) for p in ck[0]['parts']) == [1.99424, 34.98795] and 'both-near' in ck[0]['flags']
check('CH King Of Stars: same root on J Jupiter, 1.99424 / 34.98795, both near (full file only)', ok,
      (', '.join(f"{p['value']:.5f} {p['level']}" for p in ck[0]['parts']) + f", flags {ck[0]['flags']}") if ck else 'missing')
fld = cv[0]['field'] if cv else {}
both = cv and V['runner'] in fld.get('near', []) and K['runner'] in fld.get('near', [])
check('CH root field count includes both runners (near)', bool(both), f"field {fld}")
pv = open(f"docs/classic/newcastle_aw_1330_20220102/jupiter/{V['runner']}.txt").read()
pk = open(f"docs/classic/newcastle_aw_1330_20220102/jupiter/{K['runner']}.txt").read()
check('runner pages: Venturous shows the chain, King Of Stars does not', 'sky Uranus–Venus Dec' in pv and 'sky Uranus–Venus Dec' not in pk, '')

print(f'\n{sum(RES)}/{len(RES)} passed')
sys.exit(0 if all(RES) else 1)
