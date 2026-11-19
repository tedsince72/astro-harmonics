"""The eight cover items (18 Nov 2026, Eddie: 'lets now focus on the eight items cover 38 of the 57 winners with 77 picks';
read-only). Items: BB32; BB3 + BB12 + BB53; BB79; BB77c; BB54 + BB82; BB1b; BB69; BB13 + BB80 (bb_fresh_sheet_cover). Per race the
runners holding any of them; by number of picks in the race; by number of the eight a runner holds; each item alone (its picks
that hold no other of the eight) and overlaps; level stakes at SP (bb_fresh_sheet_profit.sp).
--race <race> (19 Nov 2026, Eddie; the forward test): one new race, blind - reads only its rule file
docs/eddie_read/bybody_rules/<race>_bbrules.json (or --dir), never a result; prints the picks, the items each holds, the
number of picks and the overlap notes. Usage: python3 tools/scans/bb_cover8.py [--race <race> [--dir DIR]]"""
import sys, itertools, json
ARGV = sys.argv[1:]  # read before the imports below (one of them resets sys.argv)
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as N, bb_fresh_sheet as F, bb_fresh_sheet_profit as SP
C = [('BB32',), ('BB3', 'BB12', 'BB53'), ('BB79',), ('BB77c',), ('BB54', 'BB82'), ('BB1b',), ('BB69',), ('BB13', 'BB80')]
L = [' + '.join(c) for c in C]


def fmt(p, w, c, pr):
    return f'{p} / {w} / {c:.1f} | {pr:+.1f} | {100*pr/p:+.0f} %' if p else '0 | | '


NOTES = [({'BB32'}, {'BB1b', 'BB54 + BB82', 'BB13 + BB80'}, 'BB32 with BB1b / BB54 + BB82 / BB13 + BB80: in-sample 3 runners, 3 won'),
         ({'BB13 + BB80'}, {'BB79', 'BB3 + BB12 + BB53'}, 'BB13 + BB80 with BB79 / BB3 + BB12 + BB53: in-sample 4 runners, 4 won'),
         ({'BB32'}, {'BB77c'}, 'BB32 + BB77c: in-sample 2 of 2 lost'),
         ({'BB69'}, set(L) - {'BB69'}, 'BB69 with another of the eight: in-sample 2 of 8 won')]


def one_race(race, d):
    J = json.load(open(f'{d}/{race}_bbrules.json'))
    held = {r: set() for r in J['runners']}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                held.setdefault(c['runner'], set()).add(rid)
    picks = [(r, [L[i] for i, c in enumerate(C) if set(c) <= held[r]]) for r in J['runners']]
    picks = [(r, it) for r, it in picks if it]
    print(f'# Cover of eight: {race} ({len(J["runners"])} runners; rules from {d}; blind, no result read)\n')
    print(f'Picks: {len(picks)}' + ('  -> no bet' if not picks else '  -> single pick' if len(picks) == 1 else ''))
    for r, it in picks:
        print(f'- {r}: {", ".join(it)}')
        for a, b, txt in NOTES:
            s = set(it)
            if s & a and s & b and not (a == {'BB69'} and s == {'BB69'}):
                print(f'    note: {txt}')
    print('\nBet: 1 point level stake at SP on each pick (fixed 18 Nov 2026).')


def main():
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('--race'); ap.add_argument('--dir', default='docs/eddie_read/bybody_rules')
    a = ap.parse_args(ARGV)
    if a.race:
        return one_race(a.race, a.dir)
    rows = []  # (race, runner, n field, held items, won, dec)
    races = []
    for race, win in N.RACES:
        runners, hh = F.holders(race); w = next(r for r in runners if win in r); dec = SP.sp(race, win)[0]
        picks = []
        for r, s in hh.items():
            it = [L[i] for i, c in enumerate(C) if set(c) <= s]
            if it: picks.append((race, r, len(runners), it, r == w, dec))
        rows += picks; races.append((race, win, len(runners), picks))

    def agg(sel):
        p = len(sel); w = sum(x[4] for x in sel); c = sum(1 / x[2] for x in sel)
        return p, w, c, sum(x[5] if x[4] else -1 for x in sel)
    print('## By number of cover picks in the race\n\n| picks in race | races | winner picked | picks / won / chance | profit | ROI |\n|---|---|---|---|---|---|')
    for k in range(0, 6):
        rs = [r for r in races if len(r[3]) == k] if k < 5 else [r for r in races if len(r[3]) >= 5]
        if not rs: continue
        sel = [x for r in rs for x in r[3]]
        print(f"| {k if k < 5 else '5+'} | {len(rs)} | {sum(any(x[4] for x in r[3]) for r in rs)} | {fmt(*agg(sel))} |")
    print('\n## By how many of the eight a runner holds\n\n| items held | picks / won / chance | profit | ROI |\n|---|---|---|---|')
    for k in (1, 2, 3):
        sel = [x for x in rows if (len(x[3]) == k if k < 3 else len(x[3]) >= 3)]
        print(f"| {k if k < 3 else '3+'} | {fmt(*agg(sel))} |")
    print('\n## Each item: all its picks, and its picks holding no other of the eight\n\n| item | all: picks / won / chance | profit | ROI | alone: picks / won / chance | profit | ROI |\n|---|---|---|---|---|---|---|')
    for l in L:
        a = [x for x in rows if l in x[3]]; b = [x for x in a if len(x[3]) == 1]
        print(f'| {l} | {fmt(*agg(a))} | {fmt(*agg(b))} |')
    print('\n## Overlaps between items (runners holding both)\n')
    for a, b in itertools.combinations(L, 2):
        sel = [x for x in rows if a in x[3] and b in x[3]]
        if sel: print(f'- {a} & {b}: {fmt(*agg(sel))} - ' + ', '.join(x[1] + (' WON' if x[4] else '') for x in sel))
    print('\n## Every race\n')
    for race, win, n, picks in races:
        s = '; '.join(f"{x[1]}{' WON' if x[4] else ''} [{', '.join(x[3])}]" for x in picks) or 'no pick'
        print(f'- {race} ({n} ran, winner {win}): {s}')


if __name__ == '__main__':
    main()
