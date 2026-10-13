#!/usr/bin/env python3
"""jr_tally.py - final tally of the 13 blind races of 12 Oct 2026 (JR v1 f96f93d, JR v3 1e18081). Read-only.
Winners and non-runners below are copied from the result lines printed race by race (docs/classic/jr3_blind_20261012.md).

Part 1 (kinds fixed before Musselburgh 14:17; Yarmouth 13:54 was opened before they were fixed): for each kind, in each race where it is
RARE (held by at least one runner and by fewer than half the field), winners holding it vs beaten runners holding it; chance = sum over
those races of holders / field size (= sum of 1/field over holders) = winners expected if holding it made no difference.
Computed with the field as read (non-runners in our files included) and without non-runners (rarity re-judged on the runners that ran).
Part 2 (ADDED AFTER RESULTS, 13 Oct, Eddie): near-level D3, C3, E1, E2, E3 (a hit of that measure at level near), and sky-Moon chains
(CH with S Moon in the root: on the page = not both-near; any = incl. both-near); same tally, plus 'held at all' (rare or not),
plus every holding listed.
Writes docs/classic/jr3_tally_20261012.txt."""
import json, glob, os, csv, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jr_score import V3_KINDS, V1_KINDS, v3_kinds

# race, winner cloth, non-runner cloths that are in our files, note
RACES = [('yarmouth_1354_20261012', '2', [], 'opened before kinds were fixed'),
         ('musselburgh_1417_20261012', '1', [], ''),
         ('worcester_1507_20261012', '2', ['4'], ''),
         ('worcester_1537_20261012', '3', [], ''),
         ('musselburgh_1547_20261012', '5', [], ''),
         ('yarmouth_1554_20261012', '1', [], ''),
         ('worcester_1607_20261012', '1', [], ''),
         ('newcastle_aw_1628_20261012', '6', [], ''),
         ('worcester_1637_20261012', '5', ['7'], ''),
         ('musselburgh_1650_20261012', '5', [], ''),
         ('kempton_aw_1715_20261012', '2', ['3'], 'NR withdrawn at the stalls'),
         ('newcastle_aw_1800_20261012', '1', [], ''),
         ('kempton_aw_1915_20261012', '5', [], '')]
STRUCK = ('strict', 'exact-in-race', 'exact-pre-off')
EXTRA = ['near D3', 'near C3', 'near E1', 'near E2', 'near E3', 'sky-Moon chain (on page)', 'sky-Moon chain (any, incl. both-near)']


def extra_kinds(hits):
    ks, lines = set(), {}
    for h in hits:
        for m in ('D3', 'C3', 'E1', 'E2', 'E3'):
            if h['m'] == m and h['level'] == 'near':
                ks.add(f'near {m}'); lines.setdefault(f'near {m}', []).append(h)
        if h['m'] == 'CH' and 'S Moon' in h.get('root', ''):
            ks.add('sky-Moon chain (any, incl. both-near)'); lines.setdefault('sky-Moon chain (any, incl. both-near)', []).append(h)
            if 'both-near' not in h['flags']:
                ks.add('sky-Moon chain (on page)'); lines.setdefault('sky-Moon chain (on page)', []).append(h)
    return ks, lines


def load(race):
    pos = {}
    for r in csv.DictReader(open(f'docs/jupiter/{race}/positions.csv')):
        if r['runner'] != 'SKY':
            pos[r['runner']] = r['cloth']
    v1 = {os.path.basename(f)[:3]: {it['m'] for it in json.load(open(f))['items']}
          for f in sorted(glob.glob(f'docs/jupiter/{race}/layer3/P[0-9][0-9].json'))}
    v3h = {P: json.load(open(f'docs/classic/{race}/jupiter/{P}.json')) for P in sorted(v1)}
    return pos, v1, v3h


def tally(kinds, have_by_race):
    """have_by_race: [(race, W, order, NR, {P: set(kinds)})] -> rows"""
    rows = []
    for k in kinds:
        acc = {'all': [0, 0.0, 0, 0, 0], 'ran': [0, 0.0, 0, 0, 0]}   # winners, chance, beaten, races rare, winners excl. Yarmouth 13:54
        for race, W, order, NR, have in have_by_race:
            for mode in ('all', 'ran'):
                field = order if mode == 'all' else [P for P in order if P not in NR]
                H = [P for P in field if k in have[P]]
                n = len(field)
                if H and len(H) < n / 2:
                    a = acc[mode]
                    w = int(W in H)
                    a[0] += w; a[1] += len(H) / n; a[2] += len(H) - w; a[3] += 1
                    a[4] += w if race != 'yarmouth_1354_20261012' else 0
        rows.append((k, acc))
    return rows


def tally_any(kinds, have_by_race):
    """held at all (rare or not): winners holding, chance = sum of holders / field, beaten holders, races held"""
    L = ['  kind                                   | with non-runners: winners (chance)  beaten  races held | without non-runners: same']
    for k in kinds:
        out = []
        for mode in ('all', 'ran'):
            w = b = r = 0; ch = 0.0
            for race, W, order, NR, have in have_by_race:
                field = order if mode == 'all' else [P for P in order if P not in NR]
                H = [P for P in field if k in have[P]]
                if H:
                    r += 1; ch += len(H) / len(field); w += int(W in H); b += len(H) - int(W in H)
            out.append(f'{w:>3} ({ch:5.2f})  {b:>6}  {r:>10}')
        L.append(f'  {k:38s} | {out[0]:36s}      | {out[1]}')
    return L


def fmt_rows(rows):
    L = ['  kind                                   | with non-runners in field                      | without non-runners',
         '                                         | winners (chance)  beaten  races rare  [excl. Y13:54] | winners (chance)  beaten  races rare  [excl. Y13:54]']
    for k, acc in rows:
        s = []
        for mode in ('all', 'ran'):
            a = acc[mode]
            s.append(f'{a[0]:>3} ({a[1]:5.2f})  {a[2]:>6}  {a[3]:>10}  [{a[4]}]')
        L.append(f'  {str(k):38s} | {s[0]:44s} | {s[1]}')
    return L


def main():
    data_v3, data_v1, data_x, lines = [], [], [], []
    for race, wc, nrc, note in RACES:
        pos, v1, v3h = load(race)
        order = sorted(v1)
        W = [P for P in order if pos[P] == wc][0]
        NR = [P for P in order if pos[P] in nrc]
        data_v3.append((race, W, order, NR, {P: v3_kinds(v3h[P]['hits']) for P in order}))
        data_v1.append((race, W, order, NR, v1))
        ex = {}
        for P in order:
            ks, ls = extra_kinds(v3h[P]['hits'])
            ex[P] = ks
            for k, hs in ls.items():
                for h in hs:
                    f = h['field']
                    lines.append((k, race, P, P == W, P in NR, len(order), h))
        data_x.append((race, W, order, NR, ex))
    n_runners = sum(len(d[2]) for d in data_v3)
    n_ran = sum(len(d[2]) - len(d[3]) for d in data_v3)
    L = ['JR v1 / JR v3 — final tally, 13 blind races of 12 Oct 2026 (results opened one at a time, 13 Oct). No conclusions drawn here.',
         f'Runners read: {n_runners}; ran: {n_ran} (non-runners in our files: Worcester 15:07 cloth 4, Worcester 16:37 cloth 7, '
         'Kempton 17:15 cloth 3 — withdrawn at the stalls).',
         'Yarmouth 13:54 was opened before the kinds were fixed; [excl. Y13:54] = winners without that race.',
         'Rare = held by at least one runner and by fewer than half the field. chance = sum over the races where the kind is rare of',
         'holders / field size (winners expected by chance). beaten = beaten runners holding it in those races.', '',
         'PART 1a. JR v3 kinds table (strict / exact-in-race / exact-pre-off only)'] + fmt_rows(tally(V3_KINDS, data_v3))
    L += ['', 'PART 1b. JR v1 item numbers (any item of that number)'] + fmt_rows(tally(V1_KINDS, data_v1))
    L += ['', '=' * 100, 'PART 2 — ADDED AFTER RESULTS (13 Oct 2026, Eddie): near-level D3, C3, E and sky-Moon chains. Not part of the fixed kinds.',
          '', 'Rare only (as Part 1):'] + fmt_rows(tally(EXTRA, data_x)) + \
         ['', 'Held at all, rare or not (added with Part 2; chance = sum over races of holders / field size):'] + tally_any(EXTRA, data_x)
    L += ['', 'Every holding (W = winner, NR = non-runner); field = runners holding the same hit, by level, of the field read']
    for k in EXTRA:
        L.append(f'\n  {k}')
        for kk, race, P, w, nr, n, h in sorted([x for x in lines if x[0] == k], key=lambda x: (x[1], x[2])):
            f = h['field']
            desc = h['desc'] if h['m'] != 'CH' else f"{h['root']} {h['root_plane']} {h['root_value']:.5f} -> {h['natal']} [{h['level']}{', both-near' if 'both-near' in h['flags'] else ''}]"
            extra = '' if h['m'] == 'CH' else f" {h['plane']} value {h['value']:.5f} -> {h['target']} off {h['offset']:+.5f}{'%' if h['unit'] == '%' else ''}"
            L.append(f"    {race:28s} {P}{' W' if w else '  '}{' NR' if nr else '   '}  [{h['m']}] {desc}{extra} | "
                     f"field S{len(f['strict'])} I{len(f['exact-in-race'])} P{len(f['exact-pre-off'])} N{len(f['near'])} /{n}")
    open('docs/classic/jr3_tally_20261012.txt', 'w').write('\n'.join(L) + '\n')
    print('-> docs/classic/jr3_tally_20261012.txt')


if __name__ == '__main__':
    main()
