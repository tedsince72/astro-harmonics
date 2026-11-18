"""Field check (18 Nov 2026, from Eddie's Brian Boranha Mars lines, Catterick 15:05 19 Nov 2021; read-only).
O1 on Mars (S Sun on sky Mars RA / Dec, H Mars Dec, J Mars RA), S Mars -> H Mars in RA and Dec, H Mars - J Mars RA 61.
Per body X (number families only, no conj / cp / opposition):
  A  O1 on X (bb_fieldcheck_orcus_sun)
  B  S X -> H X or S X -> J X scoring in both RA and Dec (same chart)
  C  H X - J X scoring (any plane)
  AB, AC, BC, ABC  held on the same X
Runner-level; races = bb_scan_negatives.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_orcus_sun as OS
import bb_scan_negatives as NEG
NO = OS.NO
ok = OS.ok
KEYS = ['A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC']


def cases(D):
    o1 = {t.split(' by ')[0] for t in OS.cases(D).get('O1', [])}
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        L = [r for r in d['L'] if ok(r)]
        b = any({r['plane'] for r in L if r['line'] == f'S {X} → {c} {X}'} >= {'RA', 'Dec'} for c in 'HJ')
        c = any(r['line'] == f'H {X} – J {X}' for r in L)
        f = {'A': X in o1, 'B': b, 'C': c}
        for k in KEYS:
            if all(f[ch] for ch in k):
                out.setdefault(k, []).append(X)
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for race, win in NEG.RACES:
        D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        N = len(D)
        for run, data in D.items():
            cs = cases(data)
            for k in KEYS:
                if k in cs:
                    t = tot[k]; t[0] += 1; t[1] += win in run; t[2] += 1 / N
                    if win in run or k == 'ABC': t[3].append(f"{race} {run}{' WON' if win in run else ''} ({','.join(cs[k])})")
    print(f'## Totals over {len(NEG.RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}')
        if k in ('ABC', 'AB', 'AC'):
            for s in ws: print('     ', s)


if __name__ == '__main__':
    main()
