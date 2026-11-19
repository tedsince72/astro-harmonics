"""Natal pairs activated by the sky (19 Nov 2026, Eddie: 'natal to natal is always there so it needs activation'; read-only;
from Of Corse I Can, Plumpton 14:45 16 Nov 2026: H Chiron – H Orcus RA 155.5644 ninth 155.556 and S Moon – S Orcus RA 155.5338).
Natal pair c X – c Y (c = H or J; natal bodies + royal stars, no royal – royal, not the chart's own Rahu – Ketu) scoring >= 90 in a
number family (bb_scan_natal_pairs.nums). It is ACTIVATED when a sky line naming S X or S Y scores >= 50 on the same family + target:
a sky pair S X – S Z (Z a sky body or royal star, not sky Rahu – Ketu) or a runner line S X → c' W (W a natal body or royal star,
either chart). Versions: 'm' the Moon may be Z; 's' same plane as the natal pair only.
Per runner (both charts):
  A1   one or more activated natal pairs (no Moon, any plane)
  A1m  the same, Moon allowed
  A2   two or more activated natal pairs (no Moon)
  AB   an activated natal pair that is also >= 90 in the other chart (same pair, any number)
  AB2  two pairs >= 90 in both charts, at least one of them activated
  ABm, AB2m  the same with the Moon allowed as the activating sky end
  R    sky X (X in a natal pair >= 90) carries one number twice: a sky pair S X – S Z and a runner line S X → natal W, both >= 50
       (Of Corse I Can: S Orcus – S Pluto RA 144.444 / S Orcus → J Neptune RA; S Regulus – S Orcus RA 6×φ / S Orcus → J Vesta Dec)
Usage: python3 tools/scans/bb_scan_activation.py [--race <race>] [--cut 50|80|90]  (score of the activating sky line; default 50)"""
import sys, os, openpyxl
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as NG
from bb_scan_natal_pairs import nums, P, NAT
from bb_scan_uranus_pairs import dist
from bb_scan_natal_angle import pairs

CUT = float(ARGS[ARGS.index('--cut') + 1]) if '--cut' in ARGS else 50
KEYS = ['A1', 'A1m', 'A2', 'AB', 'ABm', 'AB2', 'AB2m', 'R']
SKYB = NAT + B.ROYAL


def hits(v, pl):
    return [(f, t, s) for f, t, s in nums(v, pl) if s >= CUT]


def sky_named(tp, tr):
    """sky pair lines: body -> list of (fam, tgt, plane, text, moon)"""
    out = {}
    pts = SKYB + ['Moon']
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            if {a, b} == {'Rahu', 'Ketu'} or (a in B.ROYAL and b in B.ROYAL):
                continue
            for pl in ('RA', 'Dec'):
                x, y = P(tp, tr, a, pl), P(tp, tr, b, pl)
                if x is None or y is None:
                    continue
                v = dist(x, y, pl)
                for f, t, s in hits(v, pl):
                    moon = 'Moon' in (a, b)
                    for n in (a, b):
                        if n != 'Moon':
                            out.setdefault(n, []).append((f, t, pl, f'S {a} – S {b} {pl} {v:.4f} {t} ({s:.0f})', moon, 'pair'))
    return out


def runner(r, tp, tr, skyn):
    nat = {}
    for c in 'HJ':
        if not r['pos'].get(c):
            continue
        for X, Y in pairs(NAT + B.ROYAL):
            for pl in ('RA', 'Dec'):
                a, b = P(r['pos'][c], r['ra'][c], X, pl), P(r['pos'][c], r['ra'][c], Y, pl)
                if a is None or b is None:
                    continue
                v = dist(a, b, pl); h = nums(v, pl)
                if h and h[0][2] >= 90:
                    nat.setdefault(c, []).append((X, Y, pl, h[0][0], h[0][1], v, h[0][2]))
    # runner lines S X -> c W
    rl = {}
    for X in SKYB:
        if X in B.ROYAL:
            continue
        for c in 'HJ':
            if not r['pos'].get(c):
                continue
            for W in NAT + B.ROYAL:
                for pl in ('RA', 'Dec'):
                    x, y = P(tp, tr, X, pl), P(r['pos'][c], r['ra'][c], W, pl)
                    if x is None or y is None:
                        continue
                    v = dist(x, y, pl)
                    for f, t, s in hits(v, pl):
                        rl.setdefault(X, []).append((f, t, pl, f'S {X} → {c} {W} {pl} {v:.4f} {t} ({s:.0f})', False, 'line'))
    act, actm, show = [], [], []
    for c, L in nat.items():
        for X, Y, pl, f, t, v, sc in L:
            lines = [x for n in (X, Y) for x in skyn.get(n, []) + rl.get(n, []) if x[0] == f and x[1] == t]
            nm = [x for x in lines if not x[4]]
            if nm:
                act.append((c, X, Y))
            if lines:
                actm.append((c, X, Y))
                show.append(f'{c} {X} – {Y} {pl} {v:.4f} {t} ({sc:.1f}) <- ' + '; '.join(x[3] for x in lines[:3]))
    pset = {c: {frozenset((X, Y)) for X, Y, *_ in L} for c, L in nat.items()}
    both = pset.get('H', set()) & pset.get('J', set())
    ab = [a for a in act if frozenset(a[1:]) in both]
    abm = [a for a in actm if frozenset(a[1:]) in both]
    bodies = {n for L in nat.values() for X, Y, *_ in L for n in (X, Y)} - set(B.ROYAL)
    rep = []
    for X in bodies:
        sp = {(f, t) for f, t, pl, txt, moon, k in skyn.get(X, []) if not moon}
        for f, t, pl, txt, moon, k in rl.get(X, []):
            if (f, t) in sp:
                rep.append(f'{X} {t}: {txt}')
    h = {'A1': bool(act), 'A1m': bool(actm), 'A2': len(set(act)) >= 2, 'AB': bool(ab),
         'AB2': len(both) >= 2 and bool(ab), 'ABm': bool(abm),
         'AB2m': len(both) >= 2 and bool(abm), 'R': bool(rep)}
    return h, show, rep, sorted(tuple(sorted(p)) for p in both)


def race(rc):
    path = f'reference/classic/race_batch_{rc}_active.xlsx'
    if not os.path.exists(path):
        return None
    runners, tt, tp = B.load(path)
    tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
    skyn = sky_named(tp, tr)
    return [(r['name'].get('H'),) + runner(r, tp, tr, skyn) for cl, r in sorted(runners.items())]


def main():
    if '--race' in ARGS:
        for n, h, show, rep, both in race(ARGS[ARGS.index('--race') + 1]):
            print(f"{n}: {', '.join(k for k in KEYS if h[k]) or '-'} | both charts {both}")
            for s in show: print('   act', s)
            for s in sorted(set(rep))[:8]: print('   rep', s)
        return
    T = {k: [0, 0, 0.0, []] for k in KEYS}; nr = 0
    for rc, win in NG.RACES:
        rows = race(rc)
        if not rows:
            continue
        nr += 1; n = len(rows)
        for name, h, *_ in rows:
            w = bool(name and win in name)
            for k in KEYS:
                if h[k]:
                    T[k][0] += 1; T[k][1] += w; T[k][2] += 1 / n
                    if w: T[k][3].append(win)
    print(f'## Activated natal pairs (activating line >= {CUT:g}) over {nr} result races with an _active.xlsx\n')
    print('| measure | picks | won | by chance |\n|---|---|---|---|')
    for k in KEYS:
        print(f'| {k} | {T[k][0]} | {T[k][1]} | {T[k][2]:.1f} |')
    print()
    for k in KEYS:
        print(f'- {k} winners: ' + (', '.join(T[k][3]) if len(T[k][3]) <= 20 else f'{len(T[k][3])} winners'))


if __name__ == '__main__':
    main()
