#!/usr/bin/env python3
"""
ledger.py v1.1 - the raw ledger (Eddie, 2 Oct 2026: "start from a blank sheet ... read the raw data or as
close as you can get without many filters ... go in detail through each one to find the combinations").

For every race it writes two CSV files, built straight from the positions (no detail sheet, no grid,
no "only here", no ** or ^ filters - everything is kept and LABELLED):

  <race>__SKY.csv     every sky pair (both coordinates) scoring > 0 in any family
      a, b, mode, value, best_family, best_score, dev_deg, families, score_m30, score_p30, motion
      (A applying / S separating: the distance from the family target shrinking / growing AT the off,
      measured 2 minutes either side; score_m30 / score_p30 show the score half an hour before / after),
      pair_best (the pair's best over RA/Dec, as the sheet ranks), rank80 (rank among 80+ pairs,
      fast points set aside, Moon kept; blank if below 80), count80_a, count80_b (80+ pairs per body)
  <race>__LEDGER.csv  every contact on every chart (horse and jockey) scoring > 0 in any family
      tab, role, cloth, partnership, kind (N natal-natal / X sky->natal / S sky->same natal body),
      a (natal or sky body), b (natal body), mode, value, best_family, best_score, dev_deg, families,
      score_m30, score_p30, motion (X/S only, as for the sky; N is natal and does not move), sky_pair_score (the sky pair a/b in the same coordinate, best family),
      sky_pair_rank80, class_a, class_b, day_width (how far the value moves across the birth day -
      0 for slow bodies; the natal time is unknown, so contacts on fast natal bodies are not exact),
      shared (number of OTHER runners - partnerships - whose charts hold the same kind/a/b/mode with
      the same best family at score >= 50)

Rules kept from the engine (active_vibrations.py, unchanged): the family scoring functions; RA
separations on the circle; star-star pairs skipped; Ketu/Rahu RA axis skipped. Differences, on
purpose: natal Moon KEPT (flagged by day_width); fast points (Asc, MC, Vertex, PoF, PoS) set aside
(Eddie 2 Oct); sky star -> natal star skipped (the same star for everyone).
Motion comes from sky_motion.py v1.1 (engine at the off, +/-2 and +/-30 minutes).

Usage: python3 ledger.py --pos DIR --sky DIR --out DIR [--races R1,R2]
"""
import argparse
import collections
import csv
import glob
import itertools
import os
import sys

sys.path.insert(0, '/home/claude/ds')
import active_vibrations as av

FAST = {'Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit'}
STARS = av.FIXED_STARS
NODES = {'Ketu', 'Rahu'}
PERSONAL = {'Sun', 'Moon', 'Mercury', 'Venus', 'Mars'}
SOCIAL = {'Jupiter', 'Saturn', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Rahu', 'Ketu'}
FAMS = [n for n, _ in av.VIBRATION_FAMILIES]
PHI = (1 + 5 ** 0.5) / 2
SQ2 = 2 ** 0.5
SIL = 1 + SQ2
PP = [PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] + [10 * PHI ** p for p in (-1, 1, 2, 3, 4, 5, 6, 7)] + [100 * PHI ** p for p in (-1, 1)]


def cls(b):
    if b in STARS:
        return 'star'
    if b in PERSONAL:
        return 'personal'
    if b in SOCIAL:
        return 'social'
    return 'slow'


def sep(p, q, mode):
    return av.angular_sep_ra(p[0], q[0]) if mode == 'RA' else av.angular_sep_dec(p[1], q[1])


def scores(v, mode):
    return av.all_vibrations(v, mode)


def best(sc):
    f = max(FAMS, key=lambda k: sc[k])
    return f, sc[f]


def dev_deg(v, family):
    if family == 'Whole Number':
        return abs(v - round(v))
    if family == 'Golden Ratio':
        m = v % PHI
        return min(m, PHI - m)
    if family == 'Phi Powers':
        return min(abs(v - t) for t in PP)
    if family == 'Ninths':
        return min(abs(v - t) for lo, hi, tol, t in av._NINTH_RANGES)
    if family == 'Sqrt2':
        m = v % SQ2
        return min(min(m, SQ2 - m), abs(v - 10 * SQ2), abs(v - 100 * SQ2))
    if family == 'Silver Ratio':
        m = v % SIL
        return min(min(m, SIL - m), abs(v - 10 * SIL))
    if family == 'Conjunction':
        return v
    return None


def fam_str(sc):
    return ';'.join(f'{k}={sc[k]:.1f}' for k in FAMS if sc[k] > 0)


def motion(d_m, d_p):
    if d_p < d_m - 1e-9:
        return 'A'
    if d_p > d_m + 1e-9:
        return 'S'
    return ''


def read_pos(f):
    return {r['body']: (float(r['ra']), float(r['dec'])) for r in csv.DictReader(open(f)) if r.get('ra')}


def read_meta(pos, R):
    out = []
    for r in csv.reader(open(f'{pos}/{R}__META.csv')):
        if r and len(r) > 3 and r[0].startswith('P') and r[0][1:].isdigit():
            out.append({'tab': r[0], 'role': r[1], 'cloth': r[2], 'name': r[3]})
    return out


def read_hourly(pos, R):
    h = collections.defaultdict(lambda: collections.defaultdict(list))
    f = f'{pos}/{R}__NATAL_HOURLY.csv'
    if os.path.exists(f):
        for r in csv.DictReader(open(f)):
            if r['ra'] and r['dec']:
                h[r['tab']][r['body']].append((float(r['ra']), float(r['dec'])))
    return h


def day_width(hr, a, b, mode, kind, skyp=None):
    """range of the value over the birth day (natal side moves; sky side fixed for X/S)."""
    if kind == 'N':
        A, B = hr.get(a), hr.get(b)
        if not A or not B or len(A) != len(B):
            return ''
        vals = [sep(p, q, mode) for p, q in zip(A, B)]
    else:
        B = hr.get(b)
        if not B:
            return ''
        vals = [sep(skyp, q, mode) for q in B]
    return round(max(vals) - min(vals), 4)


def build(R, pos, skydir, out):
    S3 = {}
    for r in csv.DictReader(open(f'{skydir}/{R}__SKY3.csv')):
        S3[r['body']] = [(float(r[f'ra_{k}']), float(r[f'dec_{k}'])) for k in ('m30', '0', 'p30', 'm2', 'p2')]
    sky_bodies = [b for b in S3 if b not in FAST and b != 'equator']
    # ---- sky pairs
    sky = {}
    pair_best = {}
    for a, b in itertools.combinations(sorted(sky_bodies), 2):
        if a in STARS and b in STARS:
            continue
        for mode in ('RA', 'Dec'):
            if mode == 'RA' and {a, b} == NODES:
                continue
            v = sep(S3[a][1], S3[b][1], mode)
            sc = scores(v, mode)
            f, s = best(sc)
            if s <= 0:
                continue
            sm = scores(sep(S3[a][0], S3[b][0], mode), mode)[f]
            sp = scores(sep(S3[a][2], S3[b][2], mode), mode)[f]
            mv = motion(dev_deg(sep(S3[a][3], S3[b][3], mode), f), dev_deg(sep(S3[a][4], S3[b][4], mode), f))
            sky[(a, b, mode)] = dict(value=v, f=f, s=s, sc=sc, sm=sm, sp=sp, mv=mv)
            pair_best[(a, b)] = max(pair_best.get((a, b), 0), s)
    p80 = sorted([p for p, s in pair_best.items() if s >= 80], key=lambda p: -pair_best[p])
    rank = {p: i + 1 for i, p in enumerate(p80)}
    cnt = collections.Counter()
    for a, b in p80:
        cnt[a] += 1
        cnt[b] += 1
    with open(f'{out}/{R}__SKY.csv', 'w', newline='') as o:
        w = csv.writer(o)
        w.writerow(['a', 'b', 'mode', 'value', 'best_family', 'best_score', 'dev_deg', 'families', 'score_m30',
                    'score_p30', 'motion', 'pair_best', 'rank80', 'count80_a', 'count80_b'])
        for (a, b, mode), d in sorted(sky.items(), key=lambda kv: (-pair_best[kv[0][:2]], kv[0])):
            w.writerow([a, b, mode, round(d['value'], 6), d['f'], round(d['s'], 2), round(dev_deg(d['value'], d['f']), 6),
                        fam_str(d['sc']), round(d['sm'], 2), round(d['sp'], 2), d['mv'],
                        round(pair_best[(a, b)], 2), rank.get((a, b), ''), cnt[a], cnt[b]])

    def skyinfo(a, b, mode):
        k = (a, b, mode) if (a, b, mode) in sky else (b, a, mode)
        d = sky.get(k)
        p = (a, b) if (a, b) in rank else (b, a)
        return (round(d['s'], 2) if d else 0), rank.get(p, '')

    # ---- charts
    meta = read_meta(pos, R)
    hourly = read_hourly(pos, R)
    part = {m['cloth']: '' for m in meta}
    for m in meta:
        part[m['cloth']] = (part[m['cloth']] + '  /  ' if part[m['cloth']] else '') + m['name']
    rows = []
    for m in meta:
        P = read_pos(f'{pos}/{R}__{m["tab"]}_POS.csv')
        hr = hourly.get(m['tab'], {})
        nb = [b for b in P if b != 'equator']
        # natal-natal
        for a, b in itertools.combinations(sorted(nb), 2):
            if a in STARS and b in STARS:
                continue
            for mode in ('RA', 'Dec'):
                if mode == 'RA' and {a, b} == NODES:
                    continue
                v = sep(P[a], P[b], mode)
                sc = scores(v, mode)
                f, s = best(sc)
                if s <= 0:
                    continue
                ss, rk = skyinfo(a, b, mode)
                rows.append([m['tab'], m['role'], m['cloth'], part[m['cloth']], 'N', a, b, mode, round(v, 6), f, round(s, 2),
                             round(dev_deg(v, f), 6), fam_str(sc), '', '', '', ss, rk, cls(a), cls(b),
                             day_width(hr, a, b, mode, 'N') if (a in PERSONAL or b in PERSONAL) else 0])
        # sky -> natal
        for a in sky_bodies:
            for b in nb:
                if a in STARS and b in STARS:
                    continue
                for mode in ('RA', 'Dec'):
                    v = sep(S3[a][1], P[b], mode)
                    sc = scores(v, mode)
                    f, s = best(sc)
                    if s <= 0:
                        continue
                    sm = scores(sep(S3[a][0], P[b], mode), mode)[f]
                    sp = scores(sep(S3[a][2], P[b], mode), mode)[f]
                    kind = 'S' if a == b else 'X'
                    mv = motion(dev_deg(sep(S3[a][3], P[b], mode), f), dev_deg(sep(S3[a][4], P[b], mode), f))
                    ss, rk = skyinfo(a, b, mode) if kind == 'X' else (0, '')
                    rows.append([m['tab'], m['role'], m['cloth'], part[m['cloth']], kind, a, b, mode, round(v, 6), f, round(s, 2),
                                 round(dev_deg(v, f), 6), fam_str(sc), round(sm, 2), round(sp, 2), mv, ss, rk,
                                 cls(a), cls(b), day_width(hr, a, b, mode, kind, S3[a][1]) if b in PERSONAL else 0])
    # shared: other partnerships holding the same kind/a/b/mode/family at >= 50
    holders = collections.defaultdict(set)
    for r in rows:
        if r[10] >= 50:
            holders[(r[4], r[5], r[6], r[7], r[9])].add(r[2])
    with open(f'{out}/{R}__LEDGER.csv', 'w', newline='') as o:
        w = csv.writer(o)
        w.writerow(['tab', 'role', 'cloth', 'partnership', 'kind', 'a', 'b', 'mode', 'value', 'best_family', 'best_score',
                    'dev_deg', 'families', 'score_m30', 'score_p30', 'motion', 'sky_pair_score', 'sky_pair_rank80',
                    'class_a', 'class_b', 'day_width', 'shared'])
        for r in rows:
            h = holders.get((r[4], r[5], r[6], r[7], r[9]), set())
            w.writerow(r + [len(h - {r[2]})])
    return len(sky), len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pos', required=True)
    ap.add_argument('--sky', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--races', default='')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    races = a.races.split(',') if a.races else sorted(os.path.basename(f)[:-15] for f in glob.glob(f'{a.pos}/*__TRANS_POS.csv'))
    for R in races:
        n1, n2 = build(R, a.pos, a.sky, a.out)
        print(R, n1, n2, flush=True)


if __name__ == '__main__':
    main()
