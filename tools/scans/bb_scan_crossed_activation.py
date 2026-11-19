"""Crossed activation (19 Nov 2026, after Impatient, Ffos Las 15:37 8 Nov 2026; read-only, chosen after the result).
A natal pair c X – c Y scoring >= 90 (number family, bodies only, no Moon, not the chart's own Rahu – Ketu) is lit across charts when a
sky line onto the OTHER chart joins the same two bodies: S Y → d X or S X → d Y (d the other chart) scoring >= cut (50 / 80).
Impatient: 5 (H Saturn – Eris by S Saturn → J Eris, H Uranus – Sedna by S Sedna → J Uranus, H Orcus – Sedna by S Sedna → J Orcus,
J Sun – Eris by S Eris → H Sun, J Pluto – Gonggong by S Gonggong → H Pluto); field 0 - 4.
Over every result race with an _active.xlsx: runners with >= k such pairs; the runner(s) with the most in the race.
Usage: python3 tools/scans/bb_scan_crossed_activation.py"""
import sys, os, openpyxl
sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as NG
import bb_scan_eris_hub as EH


def count(r, tp, tr, cut):
    n = 0
    for c, d in (('H', 'J'), ('J', 'H')):
        if not (r['pos'].get(c) and r['pos'].get(d)):
            continue
        for i, X in enumerate(EH.BODIES):
            for Y in EH.BODIES[i + 1:]:
                if {X, Y} == {'Rahu', 'Ketu'}:
                    continue
                if EH.best(r['pos'][c], r['ra'][c], X, r['pos'][c], r['ra'][c], Y) < 90:
                    continue
                if max(EH.best(tp, tr, Y, r['pos'][d], r['ra'][d], X), EH.best(tp, tr, X, r['pos'][d], r['ra'][d], Y)) >= cut:
                    n += 1
    return n


def main():
    for cut in (50, 80):
        K = range(1, 7); t = {k: [0, 0, 0.0] for k in K}; top = [0, 0.0]; nr = 0
        for race, win in NG.RACES:
            p = f'reference/classic/race_batch_{race}_active.xlsx'
            if not os.path.exists(p):
                continue
            rn, tt, tp = EH.B.load(p); tr = EH.B.ra_positions(openpyxl.load_workbook(p, read_only=True)['TRANS_POS'])
            N = len(rn); nr += 1
            cn = {cl: count(r, tp, tr, cut) for cl, r in rn.items()}
            w = next((cl for cl, r in rn.items() if win in (r['name'].get('H') or '')), None)
            for cl, v in cn.items():
                for k in K:
                    if v >= k:
                        t[k][0] += 1; t[k][1] += cl == w; t[k][2] += 1 / N
            hi = max(cn.values())
            if hi > 0:
                ts = [cl for cl in cn if cn[cl] == hi]; top[0] += w in ts; top[1] += len(ts) / N
        print(f'## cross line >= {cut} ({nr} races)')
        for k in K:
            print(f'- >= {k}: {t[k][0]} / {t[k][1]} / {t[k][2]:.1f}')
        print(f'- most in the race: winner among them {top[0]} of {nr} ({top[1]:.1f} by chance)\n')


if __name__ == '__main__':
    main()
