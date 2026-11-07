#!/usr/bin/env python3
"""eddie_backtest.py - stage 3 back-test: the rules' selections against the results. The only script that reads results.

Usage:  python3 tools/eddie_backtest.py [--rules docs/eddie_read/rules.json] [--sel docs/eddie_read/rules]
        [--results docs/eddie_read/results/results.json] [--out docs/eddie_read/backtest]

Reads every <race>_rules.json (tools/eddie_rules.py) whose race is in results.json. Writes backtest.md / .json.
Per rule, split into in-sample races (rules.json 'in_sample': the races a rule was seen on or written from) and test
races (every other race), and all races:
  races      races in the results file
  fired      races where the rule selected at least one runner that ran
  picks      selected runners that ran (non-runners in the workbook left out)
  winners    picks that won;  chance = sum over races of picks / ran
  1st or 2nd picks that finished 1st or 2nd (a dead heat counts both);  chance = sum of picks x placed / ran
  only pick  races where the rule selected exactly one runner (won or not)
  alone      races where the rule selected exactly one runner and it won
  missed     races where it fired and the winner was not selected
Field size 'ran' is from the results (a runner that ran but is not in the workbook still counts in the field).
Every race is listed per rule with its picks and finishing positions.
"""
import argparse
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))


def horse(name):
    """'4 All In You / Sean Bowen' -> 'All In You'."""
    s = name.split(' / ')[0]
    head, _, rest = s.partition(' ')
    return rest if head.isdigit() else s


def pos_of(res, h):
    if h in res['first']:
        return 1
    if h in res['second']:
        return 2
    return res['order'].index(h) + 1 if h in res['order'] else None


def tally(rows):
    t = dict(races=len(rows), fired=0, picks=0, winners=0, top2=0, chance_w=0.0, chance_2=0.0, only=0, alone=0, missed=0)
    for r in rows:
        if not r['picks']:
            continue
        t['fired'] += 1
        t['picks'] += len(r['picks'])
        t['winners'] += sum(1 for _, p in r['picks'] if p == 1)
        t['top2'] += sum(1 for _, p in r['picks'] if p in (1, 2))
        t['chance_w'] += len(r['picks']) / r['ran']
        t['chance_2'] += len(r['picks']) * r['placed'] / r['ran']
        t['only'] += 1 if len(r['picks']) == 1 else 0
        t['alone'] += 1 if len(r['picks']) == 1 and r['picks'][0][1] == 1 else 0
        t['missed'] += 0 if any(p == 1 for _, p in r['picks']) else 1
    return t


def fmt(t):
    return (f"{t['races']} | {t['fired']} | {t['picks']} | {t['winners']} ({t['chance_w']:.1f}) | "
            f"{t['top2']} ({t['chance_2']:.1f}) | {t['only']} | {t['alone']}")


HEAD = '| Rule | Name | races | fired | picks | winners (chance) | 1st or 2nd (chance) | only pick | alone |\n|---|---|---|---|---|---|---|---|---|'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rules', default=os.path.join(ROOT, 'docs', 'eddie_read', 'rules.json'))
    ap.add_argument('--sel', default=os.path.join(ROOT, 'docs', 'eddie_read', 'rules'))
    ap.add_argument('--results', default=os.path.join(ROOT, 'docs', 'eddie_read', 'results', 'results.json'))
    ap.add_argument('--out', default=os.path.join(ROOT, 'docs', 'eddie_read', 'backtest'))
    a = ap.parse_args()
    rules = json.load(open(a.rules))['rules']
    results = {k: v for k, v in json.load(open(a.results)).items() if not k.startswith('_')}
    sel = {}
    for f in sorted(os.listdir(a.sel)):
        if f.endswith('_rules.json'):
            o = json.load(open(os.path.join(a.sel, f)))
            if o['race'] in results:
                sel[o['race']] = o
    missing = sorted(set(results) - set(sel))
    rows = defaultdict(list)
    for race in sorted(sel):
        o, res = sel[race], results[race]
        nr = set(res.get('nonrunners', []))
        placed = len(res['first']) + len(res['second'])
        for r in o['rules']:
            picks = []
            for R in r['selected']:
                h = horse(o['names'][R])
                if h in nr:
                    continue
                p = pos_of(res, h)
                if p is None:
                    raise SystemExit(f"{race}: {h} not in the results order")
                picks.append((h, p))
            rows[r['id']].append(dict(race=race, ran=res['ran'], placed=placed, picks=picks,
                                      winner=res['first'][0], n_sel=len(picks)))
    out, L = {}, ['# Stage 3 back-test', '',
                  f"Races: {len(sel)} (results file {len(results)}" + (f"; no rules output for {', '.join(missing)}" if missing else '') + ').',
                  'fired = races with a pick; only pick = races with exactly one pick; alone = one pick and it won; chance from field sizes.',
                  'In-sample = races the rule was seen on or written from (rules.json); test = every other race. Only the test races are evidence.', '']
    for r in rules:
        ins = set(r.get('in_sample', []))
        rr = rows[r['id']]
        out[r['id']] = dict(name=r['name'], test=tally([x for x in rr if x['race'] not in ins]),
                            in_sample=tally([x for x in rr if x['race'] in ins]), all=tally(rr), races=rr)
    for part, title in (('test', 'Test races'), ('in_sample', 'In-sample races'), ('all', 'All races')):
        L += [f'## {title}', '', HEAD]
        L += [f"| {r['id']} | {r['name']} | {fmt(out[r['id']][part])} |" for r in rules]
        L.append('')
    L += ['', '## Per rule, every race', '']
    for r in rules:
        ins = set(r.get('in_sample', []))
        L.append(f"### {r['id']} {r['name']}")
        for x in out[r['id']]['races']:
            tag = 'in-sample' if x['race'] in ins else 'test'
            pk = ', '.join(f"{h} ({'won' if p == 1 else p})" for h, p in x['picks']) or 'none'
            L.append(f"- {x['race']} ({tag}, {x['ran']} ran): {pk}; winner {x['winner']}")
        L.append('')
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, 'backtest.json'), 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(a.out, 'backtest.md'), 'w').write('\n'.join(L) + '\n')
    print(os.path.join(a.out, 'backtest.md'))


if __name__ == '__main__':
    main()
