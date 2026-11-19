"""Hub body lit with its partners (19 Nov 2026, Eddie on Impatient, Ffos Las 15:37 8 Nov 2026: 'this seems pretty obvious to me that
this is the winning connection / combination for this race - test this and looser versions'; read-only, chosen after the result).
Impatient: Eris with Sun and with Saturn - for each pair X – Y (X = Eris)
  sky    S X – S Y scores (Sun – Eris RA 101×φ 86.1, Saturn – Eris RA 18 71.6)
  natal  c X – c Y scores in one chart (J Sun – Eris Dec 11.1111 99.1; H Saturn – Eris RA 70×φ 99.2 / Dec 20 84.8)
  cross  a sky line joins the two bodies across sky and natal: S Y → c X or S X → c Y (S Eris → H Sun Dec 22.2222 90.0,
         S Sun → H Eris RA 100φ 55.4, S Saturn → J Eris RA 14 57.4)
Bodies only (no Moon, no royal stars), the chart's own Rahu – Ketu never paired; number families (bb_scan_natal_pairs.nums), best score
over RA and Dec; numbers need not match. A partner Y of X 'holds' when sky >= s, natal >= n (either chart) and cross >= x.
Versions (runner holds when some hub X has >= k partners):
  H1 strict   k 2, natal 90, sky 50, cross 50   (Impatient: Sun, Saturn)
  H2          k 1, natal 90, sky 50, cross 50
  H3          k 2, natal 80, sky any, cross any
  H4          k 1, natal 80, sky any, cross any
  H5          k 2, natal 90, sky 50, cross any
  H6          k 2, natal 90, sky any, cross 50
  H7          k 2, no natal, sky 50, cross 50
  H8          k 2, natal 90, no sky, cross 50
  H9          k 3, natal 80, sky any, cross any
  H1b / H1c / H1d / H1e  H1 with natal 80 / sky and cross 40 / natal 85 / sky 60
Usage: python3 tools/scans/bb_scan_eris_hub.py [--show]  (--show lists every holder with its hub and partners)"""
import sys, os, openpyxl
SHOW = '--show' in sys.argv
sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as NG
from bb_scan_natal_pairs import nums, P, NAT
from bb_scan_uranus_pairs import dist

BODIES = [b for b in NAT if b != 'Moon']
NONE = -1.0
V = [('H1', 2, 90, 50, 50), ('H2', 1, 90, 50, 50), ('H3', 2, 80, 0, 0), ('H4', 1, 80, 0, 0), ('H5', 2, 90, 50, 0),
     ('H6', 2, 90, 0, 50), ('H7', 2, None, 50, 50), ('H8', 2, 90, None, 50), ('H9', 3, 80, 0, 0),
     ('H1b', 2, 80, 50, 50), ('H1c', 2, 90, 40, 40), ('H1d', 2, 85, 50, 50), ('H1e', 2, 90, 60, 50)]


def best(pa, ra_a, a, pb, ra_b, b):
    s = NONE
    for pl in ('RA', 'Dec'):
        x, y = P(pa, ra_a, a, pl), P(pb, ra_b, b, pl)
        if x is None or y is None:
            continue
        h = nums(dist(x, y, pl), pl)
        if h:
            s = max(s, h[0][2])
    return s


def runner_pairs(r, tp, tr):
    out = {}
    ch = [c for c in 'HJ' if r['pos'].get(c)]
    for i, X in enumerate(BODIES):
        for Y in BODIES[i + 1:]:
            if {X, Y} == {'Rahu', 'Ketu'}:
                continue
            sky = best(tp, tr, X, tp, tr, Y)
            nat = max([best(r['pos'][c], r['ra'][c], X, r['pos'][c], r['ra'][c], Y) for c in ch] or [NONE])
            cr = max([best(tp, tr, Y, r['pos'][c], r['ra'][c], X) for c in ch] +
                     [best(tp, tr, X, r['pos'][c], r['ra'][c], Y) for c in ch] or [NONE])
            out[(X, Y)] = (sky, nat, cr)
    return out


def ok(v, cut):
    return True if cut is None else (v >= cut if cut > 0 else v > NONE)


def holds(pairs, k, n, s, x):
    hub = {}
    for (X, Y), (sky, nat, cr) in pairs.items():
        if ok(nat, n) and ok(sky, s) and ok(cr, x):
            hub.setdefault(X, []).append(Y); hub.setdefault(Y, []).append(X)
    return {h: p for h, p in hub.items() if len(p) >= k}


def main():
    tot = {v[0]: [0, 0, 0.0, 0, 0, 0.0] for v in V}  # picks won chance | without Ffos Las
    nr = 0; lines = []
    for race, win in NG.RACES:
        path = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(path):
            continue
        runners, tt, tp = B.load(path)
        tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
        N = len(runners); nr += 1
        rp = {cl: runner_pairs(r, tp, tr) for cl, r in runners.items()}
        for name, k, n, s, x in V:
            for cl, r in runners.items():
                hb = holds(rp[cl], k, n, s, x)
                if not hb:
                    continue
                w = win in (r['name'].get('H') or '')
                t = tot[name]; t[0] += 1; t[1] += w; t[2] += 1 / N
                if race != '20261108_ffos_las_1537':
                    t[3] += 1; t[4] += w; t[5] += 1 / N
                if SHOW:
                    lines.append(f"{name} {race} {r['name'].get('H')}{' WON' if w else ''}: " +
                                 '; '.join(f"{h} ({', '.join(p)})" for h, p in sorted(hb.items())))
    print(f'# Hub body lit with its partners over {nr} result races with _active.xlsx (picks / won / chance; then without Ffos Las 15:37)\n')
    print('| version | k | natal | sky | cross | all | without Impatient\'s race |\n|---|---|---|---|---|---|---|')
    for name, k, n, s, x in V:
        t = tot[name]
        f = lambda c: '-' if c is None else ('any' if c == 0 else f'>= {c}')
        print(f'| {name} | {k} | {f(n)} | {f(s)} | {f(x)} | {t[0]} / {t[1]} / {t[2]:.1f} | {t[3]} / {t[4]} / {t[5]:.1f} |')
    if SHOW:
        print('\n' + '\n'.join(lines))


if __name__ == '__main__':
    main()
