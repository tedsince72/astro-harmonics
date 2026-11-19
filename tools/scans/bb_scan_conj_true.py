"""Conjunctions in the sky race score: plane-only or a real meeting in the sky? (19 Nov 2026, Eddie after Musselburgh 13:07 2 Nov 2022:
'are you sure you are looking at the conjunctions etc. correctly'; read-only, chosen after the result).
The sky lines (bb_sky_angles_races.lines) take each plane alone: an RA 'conj' (dRA < 1.5) can be far apart in Dec, a Dec 'conj'
(|dDec| < 0.3, a parallel) can be on the other side of the sky. Each conj / contraparallel / opposition line >= 50 gets its great-circle
separation (true angle between the two points; for an opposition / contraparallel the angle from the exact mirror point).
'real' = great-circle separation < 3 deg (conj: the two points; opposition: one point vs the other's antipode; contraparallel: one
point vs the other's mirror across the equator at the same RA). Per result race: the v1 score, the v1 B-part aspect lines split real /
plane-only, and the score with only real aspect lines counted, against the cover of eight hit / miss.
Usage: python3 tools/scans/bb_scan_conj_true.py [--race <race>]"""
import sys, os, math
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import openpyxl
import bb_sky_angles_races as A
import bb_sky_race_score as S
B = A.B
REAL = 3.0


def gc(ra1, d1, ra2, d2):
    r = math.radians
    c = math.sin(r(d1)) * math.sin(r(d2)) + math.cos(r(d1)) * math.cos(r(d2)) * math.cos(r(ra1 - ra2))
    return math.degrees(math.acos(max(-1, min(1, c))))


def pos(race):
    p = f'reference/classic/race_batch_{race}_active.xlsx'
    _, _, tp = B.load(p)
    tr = B.ra_positions(openpyxl.load_workbook(p, read_only=True)['TRANS_POS'])
    return lambda b: (A.P(tp, tr, b, 'RA'), A.P(tp, tr, b, 'Dec'))


def aspects(race):
    P = pos(race); out = []
    for x in A.lines(race):
        if x[3] not in ('conj', 'contraparallel', 'opposition') or x[5] < 50:
            continue
        (r1, d1), (r2, d2) = P(x[0]), P(x[1])
        if x[3] == 'conj':
            sep = gc(r1, d1, r2, d2)
        elif x[3] == 'opposition':
            sep = gc(r1, d1, (r2 + 180) % 360, -d2)
        else:
            sep = gc(r1, d1, r2, -d2)
        asp = bool(set(x[:2]) & S.ASP)
        out.append((x, sep, asp))
    return out


def show(race):
    s, a, b, _ = S.score(race)
    print(f'{race}: v1 {s:+d}')
    for x, sep, asp in aspects(race):
        print(f'  S {x[0]} – S {x[1]} {x[2]} {x[3]} ({x[5]:.0f})  true separation {sep:.2f} deg'
              f'{"  [counted in v1]" if asp else ""}{"  real" if sep < REAL else "  plane only"}')


def main():
    if '--race' in ARGS:
        show(ARGS[ARGS.index('--race') + 1]); return
    import bb_scan_negatives as NG, bb_cover8_where as W
    from bb_cover8 import C
    rows = []
    for race, win in NG.RACES:
        if not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
            continue
        runners, hh = W.holders(race); w = next(r for r in runners if win in r)
        hit = any(set(c) <= hh.get(w, set()) for c in C)
        s = S.score(race)[0]
        asp = [(sep, a) for x, sep, a in aspects(race)]
        cnt = [y for y in asp if y[1]]
        plane = sum(1 for sep, a in cnt if sep >= REAL)
        rows.append((race, hit, s, s + plane, len(cnt) - plane, plane, race in A.ORIG,
                     sum(1 for sep, a in asp if sep < REAL), sum(1 for sep, a in asp if sep >= REAL)))
    print(f'# Sky aspect lines >= 50: real (< {REAL} deg in the sky) or plane only, {len(rows)} result races\n')
    for lab, f in (('all races', lambda r: True), ('without the 9 origin races', lambda r: not r[6])):
        R = [r for r in rows if f(r)]; H = [r for r in R if r[1]]; M = [r for r in R if not r[1]]
        m = lambda G, i: sum(r[i] for r in G) / len(G) if G else 0
        print(f'## {lab}: cover hit {len(H)}, miss {len(M)}\n')
        print('| per race | hit | miss |\n|---|---|---|')
        for nm, i in (('counted aspect lines, real', 4), ('counted aspect lines, plane only', 5),
                      ('all aspect lines, real', 7), ('all aspect lines, plane only', 8)):
            print(f'| {nm} | {m(H, i):.2f} | {m(M, i):.2f} |')
        print('\n| score | v1 races / hit | real-only races / hit |\n|---|---|---|')
        for lo, hi in ((-99, -2), (-1, 0), (1, 2), (3, 99)):
            a = [r for r in R if lo <= r[2] <= hi]; b = [r for r in R if lo <= r[3] <= hi]
            print(f'| {lo}..{hi} | {len(a)} / {sum(r[1] for r in a)} | {len(b)} / {sum(r[1] for r in b)} |')
        print()


if __name__ == '__main__':
    main()
