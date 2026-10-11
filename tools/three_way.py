#!/usr/bin/env python3
"""three_way.py RACE OFF DUR_S [TOL_PCT] [QMAX]  (Eddie, 11 Oct 2026: 'one pair, in horse, jockey and race sky, at simple ratios' - Pholas Ketu-Deneb Algedi RA 10:36:66.67)
For every pair of points (A,B) - bodies Sun..Transpluto, Rahu, Ketu (no Moon: natal Moon left out) and the 22 stars (no star-star, no Rahu-Ketu) -
and each measure RA (|dRA| wrapped) and Dec (|dDec|): H = distance in the horse's 12:00 chart, J = in the jockey's, S = in the race sky (over the real race).
Three-way link = J:H and S:H both simple ratios: larger/smaller = p/q with q <= QMAX (default 9) and the ratio <= 12, within TOL_PCT (default 0.02%)
(S:H at some moment in the race). Distances under 0.5 deg skipped. Run for each horse with its own jockey, and as a CONTROL each horse with every
other jockey in the race (same horse, wrong partner)."""
import sys, os, csv, collections, itertools, math
import numpy as np
exec(open('/home/claude/lattice/families.py').read().split("N = sorted(S)")[0].split("S = {}")[0]); STARSET = set(STARS)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R, OFF, DUR = sys.argv[1], sys.argv[2], float(sys.argv[3]); TOL = float(sys.argv[4]) / 100 if len(sys.argv) > 4 else 0.0002
QMAX = int(sys.argv[5]) if len(sys.argv) > 5 else 9
SKIP = {'Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit', 'equator', 'body', 'Moon'}
sched = int(R[-4:-2]) * 60 + int(R[-2:]); h, m, s = map(int, OFF.split(':')); t0 = h * 60 + m + s / 60; t1 = t0 + DUR / 60
M = collections.defaultdict(dict)
for r in csv.DictReader(open(f'{REPO}/data/sky/{R}__SKYM.csv')):
    if r['body'] not in SKIP: M[r['body']][sched + int(r['minute'])] = (float(r['ra']), float(r['dec']))
TS = np.arange(t0, t1 + 1e-9, 2 / 60)
def ser(b): ks = sorted(M[b]); return np.interp(TS, ks, np.degrees(np.unwrap(np.radians([M[b][k][0] for k in ks])))) % 360, np.interp(TS, ks, [M[b][k][1] for k in ks])
SKY = {b: ser(b) for b in M}
def hm(t): x = int(round(t * 60)); return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}"
def d(A, B, mm):
    if mm == 'RA': return np.abs((np.asarray(A[0]) - B[0] + 180) % 360 - 180)
    return np.abs(np.asarray(A[1]) - B[1])
def frac(x):
    """x >= 1 -> (rel err, 'p/q') nearest p/q with q <= QMAX"""
    best = (9, '')
    for q in range(1, QMAX + 1):
        p = round(x * q)
        if p >= q:
            e = abs(x - p / q) / (p / q); g = math.gcd(p, q)
            if e < best[0]: best = (e, f'{p // g}/{q // g}' if q // g > 1 else f'{p // g}')
    return best
def ratio(a, b):  # larger/smaller
    return (a / b, 'J>H') if a >= b else (b / a, 'H>J')
meta = list(csv.reader(open(f'{REPO}/data/allpos/{R}__META.csv'))); hdr = next(i for i, r in enumerate(meta) if r[:3] == ['tab', 'role', 'cloth'])
TABS = [dict(zip(meta[hdr], r)) for r in meta[hdr + 1:] if r and r[0].startswith('P')]
NAT = {t['tab']: {q['body']: (float(q['ra']), float(q['dec'])) for q in csv.DictReader(open(f"{REPO}/data/allpos/{R}__{t['tab']}_POS.csv")) if q['ra'] and q['body'] not in SKIP} for t in TABS}
name = {t['tab']: t['name'] for t in TABS}
horses = [t['tab'] for t in TABS if t['role'] == 'horse']; jockeys = [t['tab'] for t in TABS if t['role'] == 'jockey']
def links(hh, jj):
    H, J = NAT[hh], NAT[jj]; out = []
    pts = sorted(set(H) & set(J) & set(SKY))
    for a, b in itertools.combinations(pts, 2):
        if (a in STARSET and b in STARSET) or {a, b} == {'Rahu', 'Ketu'}: continue
        for mm in ('RA', 'Dec'):
            hv = float(d(H[a], H[b], mm)); jv = float(d(J[a], J[b], mm)); sv = d(SKY[a], SKY[b], mm)
            if min(hv, jv, float(sv.min())) < 0.5: continue
            rj = max(hv, jv) / min(hv, jv)
            if rj > 12: continue
            ej, fj = frac(rj)
            if ej > TOL: continue
            best = None
            for i in range(0, len(TS), 5):
                rs = max(sv[i], hv) / min(sv[i], hv)
                if rs > 12: continue
                es, fs = frac(rs)
                if es <= TOL and (best is None or es < best[0]): best = (es, fs, i, float(sv[i]))
            if best: out.append((a, b, mm, hv, jv, best[3], fj, ej, best[1], best[0], hm(TS[best[2]])))
    return out
print(f"== {R}  three-way links (J:H and S:H simple, q<={QMAX}, ratio<=12, ±{TOL*100:.3f}%), RA and Dec, real race {hm(t0)}–{hm(t1)}")
own = {}; ctrl = []
for hh in horses:
    jj = 'P%02d' % (int(hh[1:]) + 1); own[hh] = links(hh, jj)
    for oj in jockeys:
        if oj != jj: ctrl.append(len(links(hh, oj)))
print(f"control (each horse with each OTHER jockey, {len(ctrl)} pairings): mean {np.mean(ctrl):.2f} links, max {max(ctrl)}")
for hh in horses:
    jj = 'P%02d' % (int(hh[1:]) + 1); L = own[hh]
    print(f"\n-- {name[hh]} / {name.get(jj, '?')}: {len(L)} links")
    for a, b, mm, hv, jv, sv, fj, ej, fs, es, t in sorted(L, key=lambda x: x[7] + x[9]):
        print(f"   {mm:3s} {a}–{b:13s} H {hv:9.4f}  J {jv:9.4f}  S {sv:9.4f} ({t})   J:H {fj} ({ej*100:.4f}%)  S:H {fs} ({es*100:.4f}%)")
