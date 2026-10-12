#!/usr/bin/env python3
"""measures.py RACE   (reads docs/jupiter/RACE/positions.csv, made by positions.py)

Jupiter-centred read, layer 1: every raw measurement with a Jupiter in it, plus number tags. No filtering, no ratios,
no field view. Output docs/jupiter/RACE/measures/:
  sky.csv     S Jupiter vs every other sky point (same for every runner, written once)
  P##.csv     per runner:
              pair  - H Jupiter vs every H, J, S point; J Jupiter vs every H, J, S point;
                      S Jupiter vs every H, J point (so every H-J-S Jupiter-Jupiter pair appears)
              move  - every body: sky X vs H X, sky X vs J X (Moon excluded: no natal Moon)
              equator - |Dec| of every body (S, H, J)
Planes: RA = |dRA| wrapped to 0-180; Dec = |dDec|; Flat = sqrt(RA^2 + Dec^2); GC = true angular distance.
Tags (Eddie, 12 Oct 2026):
  pair      whole +-0.005, ninth +-0.0005
  move      whole +-0.01,  ninth +-0.0011
  equator   whole +-0.01,  ninth +-0.0011
  whole first; ninth only when n/9 is not a whole number. Values below 0.5 are not tagged as numbers.
  contact (pairs): close = RA < 1.5 or Dec < 0.3; near = RA < 2 or Dec < 0.6 (else blank)
  star   (pair with a star): on = RA < 1.5 and Dec < 0.3; near = RA < 2 and Dec < 0.6
Rahu stands for the node (Ketu folded, positions.py). Numbers are full precision (repr), never rounded.
"""
import sys, os, csv, math
from collections import defaultdict

TOL = {'pair': (0.005, 0.0005), 'move': (0.01, 0.0011), 'equator': (0.01, 0.0011)}


def ra_sep(a, b):
    d = abs(a - b) % 360.0
    return 360.0 - d if d > 180.0 else d


def gc(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(math.radians, (ra1, de1, ra2, de2))
    dr = r2 - r1
    num = math.hypot(math.cos(d2) * math.sin(dr),
                     math.cos(d1) * math.sin(d2) - math.sin(d1) * math.cos(d2) * math.cos(dr))
    den = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(dr)
    return math.degrees(math.atan2(num, den))


def tag(v, kind):
    if v is None or v < 0.5:
        return ''
    tw, tn = TOL[kind]
    w = round(v)
    if abs(v - w) <= tw:
        return f'W{w}'
    n = round(v * 9)
    if n % 9 and abs(v - n / 9) <= tn:
        return f'N{n}/9'
    return ''


def planes(p, q):
    ra = ra_sep(p[0], q[0])
    de = abs(p[1] - q[1])
    return ra, de, math.hypot(ra, de), gc(p[0], p[1], q[0], q[1])


def contact(ra, de, star):
    if star:
        if ra < 1.5 and de < 0.3:
            return 'on'
        if ra < 2 and de < 0.6:
            return 'near'
        return ''
    if ra < 1.5 or de < 0.3:
        return 'close'
    if ra < 2 or de < 0.6:
        return 'near'
    return ''


HEAD = ['type', 'a', 'b', 'b_kind', 'RA', 'Dec', 'Flat', 'GC', 'RA_tag', 'Dec_tag', 'Flat_tag', 'GC_tag', 'contact']


def pair_row(an, ap, bn, bp, bkind):
    ra, de, fl, g = planes(ap, bp)
    return ['pair', an, bn, bkind, repr(ra), repr(de), repr(fl), repr(g),
            tag(ra, 'pair'), tag(de, 'pair'), tag(fl, 'pair'), tag(g, 'pair'), contact(ra, de, bkind == 'star')]


def main():
    race = sys.argv[1]
    base = f'docs/jupiter/{race}'
    charts = defaultdict(dict)      # (runner, chart) -> body -> (ra, dec, kind)
    names = {}
    with open(f'{base}/positions.csv') as fh:
        for r in csv.DictReader(fh):
            charts[(r['runner'], r['chart'])][r['body']] = (float(r['ra']), float(r['dec']), r['kind'])
            if r['runner'] != 'SKY':
                names[r['runner']] = f"{r['cloth']} {r['horse']} / {r['jockey']}"
    sky = charts[('SKY', 'S')]
    out = f'{base}/measures'
    os.makedirs(out, exist_ok=True)

    sj = sky['Jupiter']
    with open(f'{out}/sky.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(HEAD)
        for b, p in sky.items():
            if b != 'Jupiter':
                w.writerow(pair_row('S Jupiter', sj, f'S {b}', p, p[2]))
        w.writerow(['equator', 'S Jupiter', '', 'body', '', repr(abs(sj[1])), '', '', '', tag(abs(sj[1]), 'equator'), '', '', ''])

    runners = sorted(names)
    for run in runners:
        H, J = charts[(run, 'H')], charts[(run, 'J')]
        rows = []
        for jn, jp in (('H Jupiter', H['Jupiter']), ('J Jupiter', J['Jupiter'])):
            for cn, ch in (('H', H), ('J', J), ('S', sky)):
                for b, p in ch.items():
                    label = f'{cn} {b}'
                    if label == jn:
                        continue
                    if jn == 'J Jupiter' and label == 'H Jupiter':
                        continue          # already written as H Jupiter - J Jupiter
                    rows.append(pair_row(jn, jp, label, p, p[2]))
        for cn, ch in (('H', H), ('J', J)):
            for b, p in ch.items():
                if b != 'Jupiter':        # S Jupiter vs natal Jupiter already above
                    rows.append(pair_row('S Jupiter', sj, f'{cn} {b}', p, p[2]))
        for cn, ch in (('H', H), ('J', J)):
            for b, p in ch.items():
                if p[2] != 'body' or b not in sky:
                    continue
                ra, de, fl, g = planes(sky[b], p)
                rows.append(['move', f'S {b}', f'{cn} {b}', 'body', repr(ra), repr(de), repr(fl), repr(g),
                             tag(ra, 'move'), tag(de, 'move'), tag(fl, 'move'), tag(g, 'move'), ''])
        for cn, ch in (('S', sky), ('H', H), ('J', J)):
            for b, p in ch.items():
                if p[2] == 'body':
                    e = abs(p[1])
                    rows.append(['equator', f'{cn} {b}', '', 'body', '', repr(e), '', '', '', tag(e, 'equator'), '', '', ''])
        with open(f'{out}/{run}.csv', 'w', newline='') as fh:
            w = csv.writer(fh); w.writerow(['runner', names[run]]); w.writerow(HEAD); w.writerows(rows)
        print(f'{run} {names[run]}: {len(rows)} rows')
    print(f'-> {out}/')


if __name__ == '__main__':
    main()
