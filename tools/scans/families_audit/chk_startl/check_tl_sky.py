"""check_tl_sky.py (independent checker, 22 Oct 2026): (e) the sky equivalent cells (relationship, value at the off, target, score,
timing, "same as sky") of every star-source event in TIMELINE H / J and LONG TIMELINE H / J, recomputed from POSITIONS: every natal
point replaced by the same sky point, same plane; "—" where two points become one (star apex) or no Equator straddle.
usage: check_tl_sky.py tables.xlsx [runner]"""
import os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from check_tl_common import *

wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
runner = sys.argv[2] if len(sys.argv) > 2 else 'P01'
sky, ch = load_positions(wb, runner)
W = World(sky, ch)
B = tl_blocks(wb[runner])
S_ = lambda p: ('S', p[1])
bad, n, per = [], 0, collections.Counter()


def tmin(txt):
    m = re.search(r'\(in ([\d.]+) min\)', txt)
    if m:
        return float(m[1])
    m = re.search(r'\(([\d.]+) min ago\)', txt)
    return -float(m[1]) if m else None


def same_target(e_tgt, e_hit, s_tgt, s_hit):
    return bool(e_hit and s_hit and e_tgt == s_tgt)


for blk in ('TIMELINE H', 'TIMELINE J', 'LONG TIMELINE H', 'LONG TIMELINE J'):
    for r in B[blk]:
        if r[3] not in STAR_SRC:
            continue
        n += 1
        p = parse_rel(r[4])
        plane, kind = r[5], r[6]
        prob = []
        if p[0] == 'r' and p[1][0] == 'S' and p[1][1] != 'Jupiter':     # star apex: S Jupiter and C Jupiter become one
            exp = ('—',)
            if r[14] != '—':
                prob.append(('apex not —', r[13:19]))
            per[(r[3], 'apex —')] += 1
        elif p[0] == 'd':
            P, Q = S_(p[1]), S_(p[2])
            pP, pQ = W.lin(P, 0), W.lin(Q, 0)
            rel = f'{pname(P)} → {pname(Q)}'
            if plane == 'Equator' and (pP[1] > 0) == (pQ[1] > 0):
                note = 'equator one side'
            v = rawd(pP, pQ, plane)
            t, hit = dist_target(v, plane)
            v0, v5, tl = lin_t(('d', plane, P, Q), W, t['tv'])
            if r[13] != rel:
                prob.append(('sky rel', r[13], rel))
            if r[14] == '—':
                prob.append(('sky —', plane, pP[1], pQ[1]))
            else:
                if abs(r[14] - round(v, 6)) > 1.5e-6:
                    prob.append(('sky value', r[14], v))
                if r[15] != target_text(t, hit, 'distance'):
                    prob.append(('sky target', r[15], target_text(t, hit, 'distance')))
                sc = round(t['score'], 2) if hit else None
                if (r[16] is None) != (sc is None) or (sc is not None and abs(r[16] - sc) > 0.0051):
                    prob.append(('sky score', r[16], sc))
                tm = tmin(str(r[17]))
                ap = 'applying' if tl > 0 else 'separating'
                if tm is None or abs(tm - tl) > 0.051 or not str(r[17]).startswith(ap):
                    prob.append(('sky timing', r[17], tl))
                e_hit = r[10] is not None
                same = same_target(r[7].replace(' — outside', ''), e_hit, target_text(t, True, 'distance'), hit)
                if (r[18] == 'same as sky') != same:
                    prob.append(('same as sky', r[18], same))
            per[(r[3], 'distance')] += 1
        else:
            X, A, Bp = S_(p[1]), S_(p[2]), S_(p[3])
            pX, pA, pB = W.lin(X, 0), W.lin(A, 0), W.lin(Bp, 0)
            sep = ':' if kind != 'midpoint' else ':'
            if plane == 'Equator' and not straddle([pX, pA, pB]):
                if r[14] != '—':
                    prob.append(('expected — (no straddle)', r[13:19]))
                per[(r[3], 'ratio — no straddle')] += 1
            else:
                dA, dB = rawd(pX, pA, plane), rawd(pX, pB, plane)
                N, D = (A, Bp) if dA >= dB else (Bp, A)
                v = max(dA, dB) / min(dA, dB)
                t, hit = ratio_target(v)
                v0, v5, tl = lin_t(('r', plane, X, N, D), W, t['tv'])
                together = rawd(pA, pB, plane) < (1.5 if plane == 'RA' else 0.3)
                if abs(r[14] - round(v, 6)) > 1.5e-6:
                    prob.append(('sky value', r[14], v))
                if not str(r[13]).startswith(f'S Jupiter: S {A[1]} ') or not str(r[13]).endswith(f' S {Bp[1]}'):
                    prob.append(('sky rel', r[13]))
                if together:
                    per[(r[3], 'ratio together')] += 1
                    if r[15] is not None or r[16] is not None:
                        prob.append(('together sky side not values only', r[13:19]))
                else:
                    if r[15] != target_text(t, hit, 'ratio'):
                        prob.append(('sky target', r[15], target_text(t, hit, 'ratio')))
                    sc = round(t['score'], 2) if hit else None
                    if (r[16] is None) != (sc is None) or (sc is not None and abs(r[16] - sc) > 0.0051):
                        prob.append(('sky score', r[16], sc))
                    tm = tmin(str(r[17]))
                    ap = 'applying' if tl > 0 else 'separating'
                    if tm is None or abs(tm - tl) > 0.051 or not str(r[17]).startswith(ap):
                        prob.append(('sky timing', r[17], tl))
                    e_hit = r[10] is not None and kind == 'ratio'
                    same = same_target(r[7].replace(' — outside', ''), e_hit, target_text(t, True, 'ratio'), hit)
                    if (r[18] == 'same as sky') != same:
                        prob.append(('same as sky', r[18], same))
                    per[(r[3], 'ratio')] += 1
        if prob:
            bad.append((blk, r[4], plane, prob))
print('star events with sky equivalent checked', n, dict(per))
print('MISMATCHES', len(bad))
for b in bad[:40]:
    print('  ', b)
