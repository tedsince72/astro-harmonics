#!/usr/bin/env python3
"""skysheet.py v1.0 (4 Oct 2026) - the SKY ONLY, read in full detail, no runners (Eddie 10:49-10:54:
"there is something in the sky that allows favs or outsiders or mid prices", "it will likely be in combinations,
bodies, families, distances", "we need to dig the sky only in the same way we have been digging races",
"include sun with moon", "the fast moving points ... may hit transit bodies at the off or in the race,
especially if conjunction or opposite 180 in RA or conjunction or opposite in DEC").

Sections (raw values throughout; no totals used as evidence):
 1. STRUCTURE   top 30 pairs (bodies, coordinate, value, family, score, clean number, applying/separating);
                busiest / next-busiest bodies and every pair they are in; repeated numbers (same value in 2+ of the
                top 30, either coordinate, within 0.005) and decimal-place numbers (x10 / x100) among the top 30.
 2. MOON & SUN  every 80+ pair with the Moon or the Sun; the Moon-Sun distance (RA, Dec, best family); star frames of
                the Moon and the Sun (as starframe.py) with the minute exact; the Moon and the Sun against the busiest
                and top-12 bodies minute by minute (-2..+15): score at the off, peak and minute.
 3. THE MOMENT  sky-sky pairs (no fast points, not star-star) whose best score in -2..+15 is >= 95 and that PEAK at the
                off or in the race window (+1..+15), or are >= 95 at the off; scores at -30/-2/off/+2/peak/+30.
 4. SIGNATURES  the top 30 as body-body + family (+ coordinate); Mars / Mercury / Venus / Sun / Moon in the top 30.
 5. FAST POINTS Ascendant, Midheaven, Vertex, Part of Fortune, Part of Spirit against every sky body (planets, points,
                stars, Sun, Moon): RA conjunction (0) and opposition (180); Dec parallel (same) and contra-parallel
                (equal and opposite) - the minute each becomes exact between -5 and +15 (linear between the minutes
                computed), and how close it is at the off. Also: a fast point completing a top-12 race number with a
                body (distance = the number) inside -2..+15.
Marks: B busiest / next-busiest, T body of a top-12 pair, R a body of a repeated-number pair, (s) star, (R) royal.
Usage: python3 skysheet.py RACE [--out FILE]"""
import sys, csv, itertools, argparse
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, ROYAL, FAST, special, SKYD, PHI
import active_vibrations as av

ap = argparse.ArgumentParser(); ap.add_argument('race'); ap.add_argument('--out', default='')
A = ap.parse_args(); R = A.race
rc = Race(R)
S = {r['race']: r for r in csv.DictReader(open('/home/claude/ledger/surprise_96.csv'))}[R]
M = {}
for r in csv.DictReader(open(f'{SKYD}/{R}__SKYM.csv')):
    M.setdefault(r['body'], {})[int(r['minute'])] = (float(r['ra']), float(r['dec']))
MIN = sorted(next(iter(M.values())))
WIN = [m for m in MIN if -2 <= m <= 15]
OUT = []
P = lambda *a: OUT.append(' '.join(str(x) for x in a))
def nm(b): return b + ('(R)' if b in ROYAL else '(s)' if b in STARS else '')

top30 = rc.byrank[:30]; top12 = rc.byrank[:12]
TOPB = {b for k in top12 for b in k}
BUSYB = set(rc.busiest) | set(rc.busiest_nm) | set(rc.next)
# repeated / decimal-place numbers among the top 30
ent = [(rc.pairs[k]['rank'], k, e[0], e[3], e[1], e[2]) for k in top30 for e in rc.pairs[k]['entries']]
rep = []
for x, y in itertools.combinations(ent, 2):
    if x[1] == y[1]: continue
    for f, lab in ((1, 'same'), (10, 'x10'), (100, 'x100')):
        for a_, b_ in ((x, y), (y, x)):
            if abs(a_[3] * f - b_[3]) <= 0.005 * max(1, f / 10) and not (f == 1 and a_ is y):
                rep.append((lab, a_, b_))
REPB = {b for _, a_, b_ in rep for k in (a_[1], b_[1]) for b in k}
def mark(b): return ('B' if b in BUSYB else '') + ('T' if b in TOPB else '') + ('R' if b in REPB else '')
def bm(b): m = mark(b); return nm(b) + (f'[{m}]' if m else '')

grp = 'FAV WON' if S['fav_finish'] == '1' else f"FAV BEATEN (fav finished {S['fav_finish']})"
P(f"SKY SHEET – {S['label']} {R}  ({rc.mrow.get('race_local_time','')}, {rc.mrow.get('racecourse','')}, lat/lon {rc.mrow.get('racecourse_lat_lon_elev','')})")
P(f"  field {S['field']} | winner {S['winner']} {S['winner_sp']} | favourite {S['fav']} {S['fav_sp']} | {grp} | surprise order #{S['order']} of 96")

P("\n1. STRUCTURE – top 30 pairs")
for k in top30:
    p = rc.pairs[k]
    es = '; '.join(f"{e[0]} {e[3]:.4f} {e[1]} {e[2]:.1f}" + (f" ={special(e[3])}" if special(e[3]) else '') + f" {e[5]}" for e in p['entries'])
    P(f"  #{p['rank']:<3} {bm(k[0])}/{bm(k[1])}  {es}")
P(f"  busiest (Moon kept): {', '.join(f'{b} {rc.count[b]}' for b in rc.busiest)} | without the Moon: {', '.join(f'{b} {rc.count_nm[b]}' for b in rc.busiest_nm)} | next: {', '.join(f'{b} {rc.count[b]}' for b in rc.next) or '-'}")
for b in sorted(BUSYB):
    prs = [(rc.pairs[k]['rank'], k) for k in rc.pairs if b in k]
    P(f"    {b}: " + '; '.join(f"#{r} {nm(k[0] if k[1]==b else k[1])} " + ','.join(f"{e[0]} {e[3]:.3f} {e[1][:6]}" for e in rc.pairs[k]['entries']) for r, k in sorted(prs)))
P("  repeated / decimal-place numbers in the top 30:" + ('' if rep else ' none'))
seen = set()
for lab, a_, b_ in sorted(rep, key=lambda t: (t[1][0], t[2][0])):
    key = (lab, a_[0], b_[0], a_[2], b_[2])
    if key in seen: continue
    seen.add(key)
    P(f"    {lab:4} #{a_[0]} {a_[1][0]}/{a_[1][1]} {a_[2]} {a_[3]:.4f} ({a_[4][:6]})  ~  #{b_[0]} {b_[1][0]}/{b_[1][1]} {b_[2]} {b_[3]:.4f} ({b_[4][:6]})")

def prof(x, y, m, fam=None):
    v0 = sep(M[x][0], M[y][0], m)
    f = fam or max(FAMS, key=lambda q: FN[q](v0, m))
    sc = {t: FN[f](sep(M[x][t], M[y][t], m), m) for t in MIN}
    return v0, f, sc

P("\n2. MOON & SUN")
for b in ('Moon', 'Sun'):
    prs = sorted((rc.pairs[k]['rank'], k) for k in rc.pairs if b in k)
    P(f"  {b} in 80+ pairs: " + ('; '.join(f"#{r} {bm(k[0] if k[1]==b else k[1])} " + ','.join(f"{e[0]} {e[3]:.4f} {e[1][:6]} {e[2]:.0f}" + (f"={special(e[3])}" if special(e[3]) else '') for e in rc.pairs[k]['entries']) for r, k in prs) or '-'))
for m in ('RA', 'Dec'):
    v0, f, sc = prof('Moon', 'Sun', m)
    pk = max(WIN, key=lambda t: sc[t])
    P(f"  Moon–Sun {m}: {v0:.4f} {f} off {sc[0]:.1f}, peak {sc[pk]:.1f} @{pk:+d}" + (f" ={special(v0)}" if special(v0) else ''))
TG = {'1:1': 1.0, 'phi': PHI, 'phi^2': PHI ** 2, 'sqrt2': 2 ** .5, '1+sqrt2': 1 + 2 ** .5, '2': 2.0, '3': 3.0}
stars = sorted(b for b in M if b in STARS)
for X in ('Moon', 'Sun'):
    fr = []
    for a_, b_ in itertools.combinations(stars, 2):
        for m in ('RA', 'Dec'):
            def rat(t):
                d1 = sep(M[X][t], M[a_][t], m); d2 = sep(M[X][t], M[b_][t], m); dab = sep(M[a_][t], M[b_][t], m)
                return d1, d2, dab
            d1, d2, dab = rat(0)
            if abs(d1 + d2 - dab) > 0.01 or min(d1, d2) < 1: continue
            r = max(d1, d2) / min(d1, d2)
            for nme, tv in TG.items():
                if abs(r / tv - 1) <= 0.001:
                    best = min(MIN, key=lambda t: abs(max(rat(t)[0], rat(t)[1]) / max(min(rat(t)[0], rat(t)[1]), 1e-9) / tv - 1))
                    fr.append(f"{a_}–{X}–{b_} {m} {nme} exact @{best:+d}")
    P(f"  {X} star frames: " + ('; '.join(fr) if fr else 'none'))
for X in ('Moon', 'Sun'):
    rows = []
    for Y in sorted((BUSYB | TOPB) - {X}):
        if Y not in M or Y in FAST: continue
        for m in ('RA', 'Dec'):
            v0, f, sc = prof(X, Y, m)
            pk = max(WIN, key=lambda t: sc[t])
            if sc[pk] >= 85 or sc[0] >= 85:
                rows.append(f"{bm(Y)} {m} {v0:.4f} {f[:6]} off {sc[0]:.0f} pk {sc[pk]:.1f}@{pk:+d}" + (f" ={special(v0)}" if special(v0) else ''))
    P(f"  {X} → busiest / top-12 bodies (>=85 at the off or peak, -2..+15): " + ('; '.join(rows) if rows else '-'))

P("\n3. THE MOMENT – sky pairs peaking at the off or in the race window (best in -2..+15 >= 95; star-star and fast points left out)")
mom = []
bodies = sorted(b for b in M if b not in FAST and b != 'equator')
for x, y in itertools.combinations(bodies, 2):
    if x in STARS and y in STARS: continue
    for m in ('RA', 'Dec'):
        v0, f, sc = prof(x, y, m)
        pk = max(WIN, key=lambda t: sc[t])
        if sc[pk] < 95: continue
        i = MIN.index(pk)
        is_peak = (i == 0 or sc[pk] > sc[MIN[i - 1]]) and (i == len(MIN) - 1 or sc[pk] > sc[MIN[i + 1]])
        if not ((is_peak and pk >= 0) or sc[0] >= 95): continue
        lab = 'OFF' if pk == 0 and is_peak else (f'+{pk}' if pk > 0 and is_peak else f'(pk {pk:+d})')
        mom.append((0 if lab == 'OFF' else pk if pk > 0 else 99, f"  {lab:>7} {bm(x)}/{bm(y)} {m} {sep(M[x][pk], M[y][pk], m):.4f} {f[:6]}" + (f" ={special(sep(M[x][pk], M[y][pk], m))}" if special(sep(M[x][pk], M[y][pk], m)) else '') + f"  {sc[-30]:.0f} / {sc[-2]:.1f} / off {sc[0]:.1f} / {sc[2]:.1f} / pk {sc[pk]:.1f} / {sc[30]:.0f}" + ("  [80+ pair #%d]" % rc.pairs[(x, y)]['rank'] if (x, y) in rc.pairs else "  [80+ pair #%d]" % rc.pairs[(y, x)]['rank'] if (y, x) in rc.pairs else '')))
for _, s in sorted(mom, key=lambda t: (t[0], t[1])): P(s)
if not mom: P('  none')

P("\n4. SIGNATURES – top 30 as body–body + family")
P('  ' + '; '.join(f"#{rc.pairs[k]['rank']} {k[0]}–{k[1]} [" + ','.join(f"{e[1]} {e[0]}" for e in rc.pairs[k]['entries']) + ']' for k in top30))
fastin = [f"{b} in #{rc.pairs[k]['rank']}" for k in top30 for b in k if b in ('Mars', 'Mercury', 'Venus', 'Sun', 'Moon')]
P('  Sun / Moon / Mercury / Venus / Mars in the top 30: ' + (', '.join(fastin) or 'none'))

P("\n5. FAST POINTS – conjunction / opposition with sky bodies, exact between -5 and +15 (minute interpolated); and top-12 numbers completed")
def cross(series):
    """series: {minute: signed value}; return list of (minute exact, |value| at off) where it crosses 0 in -5..+15"""
    ms = [m for m in MIN if -5 <= m <= 15]
    out = []
    for a_, b_ in zip(ms, ms[1:]):
        va, vb = series[a_], series[b_]
        if va == 0: out.append(float(a_))
        elif va * vb < 0 and abs(va - vb) < 20:
            out.append(a_ + (b_ - a_) * va / (va - vb))
    return out
def wrap(d): return (d + 180) % 360 - 180
for F in ('Ascendant', 'Midheaven', 'Vertex', 'Part_of_Fortune', 'Part_of_Spirit'):
    if F not in M: continue
    hits = []
    for X in sorted(M):
        if X == F or X in FAST or X == 'equator': continue
        tests = {
            'RA conj': {t: wrap(M[F][t][0] - M[X][t][0]) for t in MIN},
            'RA opp': {t: wrap(M[F][t][0] - M[X][t][0] - 180) for t in MIN},
            'Dec parallel': {t: M[F][t][1] - M[X][t][1] for t in MIN},
            'Dec contra-par': {t: M[F][t][1] + M[X][t][1] for t in MIN},
        }
        for lab, s in tests.items():
            for tx in cross(s):
                hits.append((tx, f"{lab:14} {bm(X)} exact @{tx:+.1f} (off {abs(s[0]):.3f}°)"))
    P(f"  {F}: RA at the off {M[F][0][0]:.3f}, moving {(M[F][1][0]-M[F][0][0]+540)%360-180:+.3f}°/min; Dec {M[F][0][1]:.3f}")
    for tx, s in sorted(hits): P(f"      {s}")
    if not hits: P('      none')
    num = []
    for X in sorted(M):
        if X == F or X in FAST or X == 'equator': continue
        for k in top12:
            for e in rc.pairs[k]['entries']:
                m, val = e[0], e[3]
                s = {t: sep(M[F][t], M[X][t], m) - val for t in MIN}
                ms = [t for t in MIN if -2 <= t <= 15]
                for a_, b_ in zip(ms, ms[1:]):
                    if s[a_] == 0 or (s[a_] * s[b_] < 0 and abs(s[a_] - s[b_]) < 5):
                        tx = a_ if s[a_] == 0 else a_ + (b_ - a_) * s[a_] / (s[a_] - s[b_])
                        num.append(f"{bm(X)} {m} = #{rc.pairs[k]['rank']} {k[0]}/{k[1]} {val:.4f} @{tx:+.1f}")
    if num: P("      completes top-12 numbers: " + '; '.join(num))
txt = '\n'.join(OUT)
if A.out: open(A.out, 'w').write(txt + '\n'); print(len(OUT), 'lines ->', A.out)
else: print(txt)
