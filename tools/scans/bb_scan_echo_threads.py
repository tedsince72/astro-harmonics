"""Echo threads (19 Nov 2026, Eddie 'yes, do both'; read-only; from Splintered, Wolverhampton AW 18:00 16 Nov 2026).
An echo = a natal pair c X – c Y scoring >= 80 in a number family and a sky pair S A – S B scoring >= 80 on the same family + target
within 0.01 of the natal value (bb_scan_natal_angle 'tight'; Moon out, royal stars in, no royal – royal, no own Rahu – Ketu).
Looser 'L' versions: any sky pair >= 80 on the same family + target (no 0.01), natal pair >= 90 ('anysky').
  T2  a natal body in an echo in the horse chart AND in the jockey chart (Splintered: Chiron)
  T3  one sky body in the sky pair of two or more echoes (Splintered: S Juno)
  T23 both T2 and T3
  L2, L3, L23 the same on the looser echoes
Per measure: holders, winners among them, by chance (sum 1/field), over every result race with an _active.xlsx.
Usage: python3 tools/scans/bb_scan_echo_threads.py [--race <race>] [--show]"""
import sys, os, openpyxl
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_scan_negatives as N
from bb_scan_uranus_pairs import dist
from bb_scan_natal_pairs import nums, P, NAT
from bb_scan_natal_angle import pairs, sky_lines

KEYS = ['T2', 'T3', 'T23', 'L2', 'L3', 'L23']


def echoes(pos, ra, sky):
    bykey = {}
    for p, pl, v, s, h in sky:
        for f, t, sc in h:
            if sc >= 80:
                bykey.setdefault((f, t), []).append((p, pl, v, sc))
    tight, loose = [], []
    for X, Y in pairs(NAT + B.ROYAL):
        for pl in ('RA', 'Dec'):
            a, b = P(pos, ra, X, pl), P(pos, ra, Y, pl)
            if a is None or b is None:
                continue
            v = dist(a, b, pl); h = nums(v, pl)
            if not h or h[0][2] < 80:
                continue
            f, t, sc = h[0]; on = bykey.get((f, t), [])
            for q, qpl, qv, qs in on:
                rec = (X, Y, pl, v, sc, q, qpl, qv, qs, t)
                if abs(qv - v) < 0.01:
                    tight.append(rec)
                if sc >= 90:
                    loose.append(rec)
    return tight, loose


def measures(ech):
    """ech: {'H': [...], 'J': [...]} -> (T2 bodies, T3 sky bodies)"""
    nb = {c: set(b for e in ech[c] for b in (e[0], e[1])) for c in ech}
    t2 = (nb.get('H', set()) & nb.get('J', set())) - set(B.ROYAL)
    cnt = {}
    for c in ech:
        for e in ech[c]:
            key = (c, e[0], e[1], e[2])  # one natal echo line counts once per sky body
            for s in e[5]:
                cnt.setdefault(s, set()).add(key)
    t3 = {s for s, k in cnt.items() if len(k) >= 2 and s not in B.ROYAL}
    return t2, t3


def race(rc):
    path = f'reference/classic/race_batch_{rc}_active.xlsx'
    if not os.path.exists(path):
        return None
    runners, tt, tp = B.load(path)
    tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
    sky = sky_lines(tp, tr); rows = []
    for cl, r in sorted(runners.items()):
        T, L = {}, {}
        for ch in 'HJ':
            if r['pos'].get(ch):
                T[ch], L[ch] = echoes(r['pos'][ch], r['ra'][ch], sky)
        t2, t3 = measures(T); l2, l3 = measures(L)
        hold = {'T2': t2, 'T3': t3, 'T23': (t2 and t3) and (t2 | t3), 'L2': l2, 'L3': l3, 'L23': (l2 and l3) and (l2 | l3)}
        rows.append((r['name'].get('H'), {k: bool(v) for k, v in hold.items()}, hold, T))
    return rows


def show(rows):
    for n, h, b, T in rows:
        print(f"{n}: " + ', '.join(f"{k} {sorted(b[k])}" for k in KEYS if h[k]))
        if '--show' in ARGS:
            for c in T:
                for e in T[c]:
                    print(f"    {c} {e[0]} – {e[1]} {e[2]} {e[3]:.4f} ({e[4]:.1f}) = S {' – S '.join(sorted(e[5]))} {e[6]} {e[7]:.4f} ({e[8]:.0f}) {e[9]}")


def main():
    if '--race' in ARGS:
        show(race(ARGS[ARGS.index('--race') + 1])); return
    tot = {k: [0, 0, 0.0] for k in KEYS}; nr = 0; who = {k: [] for k in KEYS}
    for rc, win in N.RACES:
        rows = race(rc)
        if not rows:
            continue
        nr += 1; n = len(rows)
        for name, h, b, T in rows:
            w = bool(name and win in name)
            for k in KEYS:
                if h[k]:
                    tot[k][0] += 1; tot[k][1] += w; tot[k][2] += 1 / n
                    if w: who[k].append(f"{win} {sorted(b[k])}")
    print(f'## Echo threads over {nr} result races with an _active.xlsx\n')
    print('| measure | picks | won | by chance |\n|---|---|---|---|')
    for k in KEYS:
        print(f'| {k} | {tot[k][0]} | {tot[k][1]} | {tot[k][2]:.1f} |')
    print()
    for k in KEYS:
        print(f'- {k} winners: ' + ('; '.join(who[k]) or 'none'))


if __name__ == '__main__':
    main()
