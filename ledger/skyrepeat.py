#!/usr/bin/env python3
"""skyrepeat.py v1.0 (3 Oct 2026) - sky pairs / distances / families that REPEAT between races (Eddie 18:16-18:18):
"sky pairs, distances, families that repeat between races in the outsiders and how that may look in the fav races".
Sky only, no runners. For all 96 races: the top-12 sky pairs plus every pair on the busiest body (Moon kept),
each with bodies, family, coordinate, value, score, rank. Race groups from surprise_96.csv: FAV = the favourite won
(fav_finish 1), OUT = the favourite was beaten (incl. F / PU / joint-favourite cases).
Three kinds of repeat, each listed race by race with date and group:
 A. the same PAIR (two bodies) in the same FAMILY (any value, any coordinate);
 B. the same pair, family, coordinate and the SAME number (within 0.005);
 C. the same NUMBER in the same family on ANY pair - also with the decimal moved (x10 / x100) and across RA/Dec.
Output: reads_out/skyrepeat.txt (full) - the date span of each repeat is shown, because slow bodies give the same
sky for races a few days apart.
Usage: python3 skyrepeat.py"""
import sys, csv, collections, datetime
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race
S = {r['race']: r for r in csv.DictReader(open('/home/claude/ledger/surprise_96.csv'))}
def grp(r): return 'FAV' if S[r]['fav_finish'] == '1' else 'OUT'
def date(r): return datetime.date(int(r[:4]), int(r[4:6]), int(r[6:8]))
E = []   # (race, label, group, rank, a, b, family, coord, value, score, busy)
for R in S:
    rc = Race(R); rc.build()
    keys = list(rc.byrank[:12]) + [k for k in rc.byrank if (k[0] in rc.busiest or k[1] in rc.busiest) and k not in rc.byrank[:12]]
    for k in keys:
        busy = k[0] in rc.busiest or k[1] in rc.busiest
        for e in rc.pairs[k]['entries']:
            E.append((R, S[R]['label'], grp(R), rc.pairs[k]['rank'], *sorted(k), e[1], e[0], e[3], e[2], busy))
O = open('/home/claude/ledger/reads_out/skyrepeat.txt', 'w')
P = lambda *a: print(*a, file=O)
nfav = sum(1 for r in S if grp(r) == 'FAV'); nout = len(S) - nfav
P(f"SKY REPEATS – 96 races: {nout} OUT (favourite beaten), {nfav} FAV (favourite won). Entries: {len(E)} (top 12 + busiest-body pairs)\n")
def show(rows):
    rows = sorted(rows, key=lambda x: x[0])
    for x in rows:
        P(f"      {x[0]:28} {x[1]:4} {x[2]:3} #{x[3]:<3} {x[4]}/{x[5]} {x[6]:13} {x[7]:3} {x[8]:9.4f} ({x[9]:.1f}){' busy' if x[10] else ''}")
def span(rows):
    ds = sorted({date(x[0]) for x in rows}); return (ds[-1] - ds[0]).days
def head(rows):
    races = {x[0] for x in rows}; o = sum(1 for r in races if grp(r) == 'OUT'); f = len(races) - o
    return o, f, len(races)
# A
A = collections.defaultdict(list)
for x in E: A[(x[4], x[5], x[6])].append(x)
P("=" * 100 + "\nA. SAME PAIR, SAME FAMILY (3+ races), sorted by how lopsided OUT vs FAV – every race listed\n")
rowsA = [(k, v) for k, v in A.items() if len({x[0] for x in v}) >= 3]
rowsA.sort(key=lambda kv: (-abs(head(kv[1])[0] / nout - head(kv[1])[1] / nfav), -head(kv[1])[2]))
for k, v in rowsA:
    o, f, n = head(v)
    P(f"  {k[0]}/{k[1]} [{k[2]}]  races {n}: OUT {o}, FAV {f}   date span {span(v)} days")
    show(v)
# B
P("\n" + "=" * 100 + "\nB. SAME PAIR, FAMILY, COORDINATE AND NUMBER (within 0.005), 2+ races\n")
B = []
for k, v in A.items():
    for crd in ('RA', 'Dec'):
        vv = sorted([x for x in v if x[7] == crd], key=lambda x: x[8])
        cl = []
        for x in vv:
            if cl and abs(x[8] - cl[-1][-1][8]) <= 0.005: cl[-1].append(x)
            else: cl.append([x])
        B += [c for c in cl if len({x[0] for x in c}) >= 2]
for c in sorted(B, key=lambda c: -len(c)):
    o, f, n = head(c)
    P(f"  {c[0][4]}/{c[0][5]} [{c[0][6]}] {c[0][7]} ≈ {c[0][8]:.4f}  races {n}: OUT {o}, FAV {f}   date span {span(c)} days")
    show(c)
# C
P("\n" + "=" * 100 + "\nC. SAME NUMBER, SAME FAMILY, ANY PAIR (x10 / x100, RA or Dec), 4+ races, spanning 60+ days\n")
def norm(v):
    if v < 0.05: return None
    while v >= 10: v /= 10
    while v < 1: v *= 10
    return v
C = collections.defaultdict(list)
for x in E:
    nv = norm(x[8])
    if nv is not None: C[x[6]].append((nv, x))
rowsC = []
for fam, lst in C.items():
    lst.sort(key=lambda t: t[0]); cl = []
    for t in lst:
        if cl and abs(t[0] - cl[-1][-1][0]) <= 0.0005 * max(1, t[0]): cl[-1].append(t)
        else: cl.append([t])
    for c in cl:
        rows = [t[1] for t in c]
        if len({x[0] for x in rows}) >= 4 and span(rows) >= 60: rowsC.append((fam, c[0][0], rows))
rowsC.sort(key=lambda t: -abs(head(t[2])[0] / nout - head(t[2])[1] / nfav))
for fam, nv, rows in rowsC:
    o, f, n = head(rows)
    P(f"  [{fam}] {nv:.4f} (any decimal place)  races {n}: OUT {o}, FAV {f}   date span {span(rows)} days")
    show(rows)
O.close()
print('A', len(rowsA), 'B', len(B), 'C', len(rowsC))
