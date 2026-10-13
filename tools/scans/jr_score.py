#!/usr/bin/env python3
"""jr_score.py RACE WINNER_CLOTH  - after the result: what the winner held in JR v1 and JR v3 (read-only; opens no results itself).
JR v1: every layer-3 item of the winner (docs/jupiter/RACE/layer3/P##.json), with k/n = runners holding the same key.
JR v3: every line of the winner's runner page (strict / exact-in-race / exact-pre-off + combined/chain near through one near part),
from docs/classic/RACE/jupiter/P##.json, with level, t and field count by level.
'ONLY' = no other runner held the same key (JR v1) / the same hit at any level (JR v3). Writes docs/classic/RACE/jupiter/winner_score.txt.
Kinds table (fixed 13 Oct 2026, before Musselburgh 14:17; not to be changed): per runner yes/no for each JR v3 kind at strict /
exact-in-race / exact-pre-off level only (C1, C1b, C2, C2b, C3, C4, C5, D1, D2, D3, E1, E2, E3, chain, chain with numbered root
(root itself a number at strict / exact level), any exact-in-race line, any exact-pre-off line), and for each JR v1 item number
(any item of that number); field count k/n per kind, RARE = held by fewer than half the field. Optional 3rd argument = a note. Option --nr C1,C2 (13 Oct, after Worcester 15:07): non-runners' cloths; adds a field count
without them ('w/o NR', RARE judged on the runners that ran) next to the full one.
No totals."""
import sys, json, glob, os

V3_KINDS = ['C1', 'C1b', 'C2', 'C2b', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'chain', 'chain, numbered root',
            'any exact-in-race', 'any exact-pre-off']
V1_KINDS = list(range(1, 36)) + ['ST']

STRUCK = ('strict', 'exact-in-race', 'exact-pre-off')


def on_page(h):
    return h['level'] in STRUCK or (h.get('parts') and 'both-near' not in h['flags'])


def v3_kinds(hits):
    ks = set()
    for h in hits:
        if h['level'] not in STRUCK:
            continue
        if h['m'] in V3_KINDS:
            ks.add(h['m'])
        if h['m'] == 'CH':
            ks.add('chain')
            rn = h.get('root_number')
            if rn and rn['level'] in STRUCK:
                ks.add('chain, numbered root')
        if h['level'] == 'exact-in-race':
            ks.add('any exact-in-race')
        if h['level'] == 'exact-pre-off':
            ks.add('any exact-pre-off')
    return ks


def table(title, kinds, have, order, W, n, nr=()):
    L = [title, '  ' + 'kind'.ljust(22) + ' '.join(P[1:] + ('*' if P == W else ('x' if P in nr else ' ')) for P in order) + '  field'
         + ('   w/o NR' if nr else '')]
    for k in kinds:
        held = [P for P in order if k in have[P]]
        rare = '  RARE' if held and len(held) < n / 2 else ''
        extra = ''
        if nr:
            ran = [P for P in order if P not in nr]
            h2 = [P for P in held if P not in nr]
            extra = f'   {len(h2)}/{len(ran)}' + ('  RARE' if h2 and len(h2) < len(ran) / 2 else '')
        L.append('  ' + str(k).ljust(22) + ' '.join((' Y ' if k in have[P] else ' - ') for P in order) +
                 f'  {len(held)}/{n}{rare}' + extra + ('  winner Y' if k in have[W] else ''))
    return L


def main():
    args = sys.argv[1:]
    nrc = []
    if '--nr' in args:
        i = args.index('--nr'); nrc = args[i + 1].split(','); del args[i:i + 2]
    race, cloth = args[0], str(args[1])
    note = args[2] if len(args) > 2 else ''
    L = []
    # JR v1
    v1 = {os.path.basename(f)[:3]: json.load(open(f)) for f in sorted(glob.glob(f'docs/jupiter/{race}/layer3/P[0-9][0-9].json'))}
    pos = {}
    import csv
    for r in csv.DictReader(open(f'docs/jupiter/{race}/positions.csv')):
        if r['runner'] != 'SKY':
            pos[r['runner']] = (r['cloth'], r['horse'], r['jockey'])
    W = [P for P, c in pos.items() if c[0] == cloth]
    if not W:
        sys.exit(f'cloth {cloth} not in {race}')
    W = W[0]
    n = len(v1)
    hold = {}
    for P, d in v1.items():
        for it in d['items']:
            hold.setdefault(it['key'], set()).add(P)
    L.append(f'== {race}: winner cloth {cloth} = {W} {pos[W][1]} / {pos[W][2]}; {n} runners' + (f'  [{note}]' if note else ''))
    order = sorted(v1)
    nr = [P for P in order if pos[P][0] in nrc]
    L.append('   runners: ' + '; '.join(f'{P} cloth {pos[P][0]} {pos[P][1]}' for P in order) + '   (* = winner'
             + (f'; x = non-runner: {", ".join(nr)}' if nr else '') + ')')
    v3all = {P: json.load(open(f'docs/classic/{race}/jupiter/{P}.json'))['hits'] for P in order}
    L += [''] + table('KINDS — JR v3 (strict / exact-in-race / exact-pre-off only)', V3_KINDS, {P: v3_kinds(v3all[P]) for P in order}, order, W, n, nr)
    L += [''] + table('KINDS — JR v1 item numbers (any item of that number)', V1_KINDS,
                      {P: {it['m'] for it in v1[P]['items']} for P in order}, order, W, n, nr)
    L.append('\nJR v1 (f96f93d) — every layer-3 item of the winner; k/n = runners holding the same key')
    seen = set()
    rows = []
    for it in v1[W]['items']:
        if it['m'] in (30, 32) or (it['m'], it['text']) in seen:
            continue
        seen.add((it['m'], it['text']))
        k = len(hold[it['key']])
        rows.append((k, f"  [{it['m']}] {it['text']}  {{{k}/{n}}}{'  ONLY' if hold[it['key']] == {W} else ''}"))
    L += [r for _, r in sorted(rows, key=lambda x: x[0])]
    # JR v3
    j = json.load(open(f'docs/classic/{race}/jupiter/{W}.json'))
    sys.path.insert(0, 'tools/jup2')
    from report import line
    L.append('\nJR v3 (1e18081) — every line of the winner\'s runner page; field S/I/P/N by level')
    rows = []
    for h in j['hits']:
        if h['m'][0] == 'B' and not h.get('joined_by'):
            continue
        if not on_page(h):
            continue
        f = h['field']
        others = set().union(*map(set, f.values())) - {W}
        fc = f"field S{len(f['strict'])} I{len(f['exact-in-race'])} P{len(f['exact-pre-off'])} N{len(f['near'])} /{n}"
        rows.append((len(others), h['t'], '  ' + line(h, fc) + ('  ONLY' if not others else '')))
    L += [r for *_, r in sorted(rows, key=lambda x: (x[0], x[1]))]
    out = f'docs/classic/{race}/jupiter/winner_score.txt'
    open(out, 'w').write('\n'.join(L) + '\n')
    print(f'-> {out}')


if __name__ == '__main__':
    main()
