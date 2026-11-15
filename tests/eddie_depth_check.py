#!/usr/bin/env python3
"""Checks for tools/eddie_depth.py (Eddie, 15 Nov 2026): hand cases from the bybody sheets + structure on every bybody workbook."""
import glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import eddie_depth as D  # noqa: E402

ok = bad = 0


def check(cond, msg):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', msg)


def bx(race):
    return os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', race, race + '_bybody.xlsx')


def body(res, runner, X):
    r = [q for q in res['runners'] if q['runner'] == runner][0]
    return [b for b in r['bodies'] if b['body'] == X][0]


# Beverley 14:05 2024, Perfect Part Sedna: the BB40 loop, step 5 by the Fomalhaut royal loop (crossed ratio 20 cut)
bev = D.run(bx('20240608_beverley_1405'))
s = body(bev, '15 Perfect Part', 'Sedna')
check(s['depth'] == 5, 'Perfect Part Sedna step 5')
txt = ' | '.join(s['cells'])
for w in ('S Sedna → H Sedna Dec 0.444030', 'pair S Mars – S Eris RA 0.444842', 'Mars on X: S Mars – S Sedna RA 32.995228',
          'Eris on X: S Eris → J Sedna RA 17.923478', 'repeat: S Sun → J Sedna Dec 17.942849', 'royal loop Fomalhaut',
          '19.914709 20 1/20 cut'):
    check(w in txt, f'Perfect Part Sedna cell {w}')
check(bev['race_top'] == 5 and len(bev['at_top']) == 8, 'Beverley: 8 runners at step 5')

# Haydock 13:45 2020, Ishvara Rahu: loop closes on Mercury (sky) and Transpluto (J), Sun repeats 13
hay = D.run(bx('20200608_haydock_1345'))
r = body(hay, '07 Ishvara', 'Rahu')
txt = ' | '.join(r['cells'])
check(r['depth'] >= 4, 'Ishvara Rahu step 4+')
for w in ('S Rahu → H Rahu Dec 13.009928', 'pair S Mercury – S Transpluto Dec 12.996052', 'S Mercury – S Rahu RA 13.317469',
          'S Transpluto → J Rahu Dec 0.989868', 'S Sun → J Rahu Dec 12.984017'):
    check(w in txt, f'Ishvara Rahu cell {w}')

# York 15:45 2024: Francophone Gonggong step 5 by the Aldebaran royal loop; its own pair not shown twice
york = D.run(bx('20240515_york_1545'))
g = body(york, '02 Francophone', 'Gonggong')
check(g['depth'] == 5 and any(c.startswith('royal loop Aldebaran') for c in g['cells']), 'Francophone Gonggong royal loop')
check(not any(c.startswith('second loop') for c in g['cells']), 'Francophone Gonggong: no duplicate second loop')
check(set(york['at_top']) == {'02 Francophone', '04 La Pasionaria'}, 'York at the top step')

# structure on every bybody workbook: ladder, Moon never an end, field counts
for p in sorted(glob.glob(os.path.join(ROOT, 'docs', 'eddie_read', 'bybody', '*', '*_bybody.xlsx'))):
    res = D.run(p)
    n = len(res['runners'])
    check(all(len(res['per_step'][k + 1]) <= len(res['per_step'][k]) for k in range(5)), f'{res["race"]} per-step counts fall')
    check(res['at_top'] == [q['runner'] for q in res['runners'] if q['top'] == res['race_top']], f'{res["race"]} at top')
    for q in res['runners']:
        check(q['n3'] == sum(1 for b in q['bodies'] if b['depth'] >= 3), f'{q["runner"]} n3')
        for b in q['bodies']:
            check(not any(c.startswith('pair S Moon') or ' – S Moon ' in c.split('|')[0] and c.startswith('pair') for c in b['cells']),
                  f'{q["runner"]} {b["body"]} no Moon pair')
    check(n > 0, f'{res["race"]} runners')

print(f'{ok}/{ok + bad} checks passed')
