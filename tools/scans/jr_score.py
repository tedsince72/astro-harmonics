#!/usr/bin/env python3
"""jr_score.py RACE WINNER_CLOTH  - after the result: what the winner held in JR v1 and JR v3 (read-only; opens no results itself).
JR v1: every layer-3 item of the winner (docs/jupiter/RACE/layer3/P##.json), with k/n = runners holding the same key.
JR v3: every line of the winner's runner page (strict / exact-in-race / exact-pre-off + combined/chain near through one near part),
from docs/classic/RACE/jupiter/P##.json, with level, t and field count by level.
'ONLY' = no other runner held the same key (JR v1) / the same hit at any level (JR v3). Writes docs/classic/RACE/jupiter/winner_score.txt.
No totals."""
import sys, json, glob, os

STRUCK = ('strict', 'exact-in-race', 'exact-pre-off')


def on_page(h):
    return h['level'] in STRUCK or (h.get('parts') and 'both-near' not in h['flags'])


def main():
    race, cloth = sys.argv[1], str(sys.argv[2])
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
    L.append(f'== {race}: winner cloth {cloth} = {W} {pos[W][1]} / {pos[W][2]}; {n} runners')
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
