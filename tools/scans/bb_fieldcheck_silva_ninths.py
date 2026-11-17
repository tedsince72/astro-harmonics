"""Field check (17 Nov 2026, Eddie: 'this is interesting as well'; read-only). Silva Eclipse Makemake, a run of ninths:
H Aldebaran – H Makemake RA 122.2730 122.222 (79.22), J Aldebaran – J Makemake RA 111.1510 111.111 (82.07), H Makemake – J Makemake RA 11.1172
11.1111 (72.61). The H–J line is mostly geometry (natal Aldebaran is nearly the same point in both charts: 122.273 − 111.151 = 11.122).
  N2   the same royal star on natal X in both charts, both lines ninths (any score)
  N2s  N2 with both >= 70
  N3   N2 + H X – J X a ninth (any score)
  N3d  N3 with two of the three targets on the same digits (111.111 / 11.1111)
  N3s  N3 with all three >= 70
Runner-level; races = bb_fieldcheck_silva.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_silva as S
KEYS = ['N2', 'N2s', 'N3', 'N3d', 'N3s']
nin = lambda r: r.get('fam') == 'ninth' and r.get('sc') is not None


def dig(t):
    s = ''.join(c for c in str(t) if c.isdigit()).lstrip('0')
    return s.rstrip('0') or s


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        hj = [r for r in d['L'] if r['line'] == f'H {X} – J {X}' and nin(r)]
        for Rr in R.ROY:
            h = [r for r in d['L'] if r['line'] == f'H {Rr} – H {X}' and nin(r)]
            j = [r for r in d['L'] if r['line'] == f'J {Rr} – J {X}' and nin(r)]
            for a in h:
                for b in j:
                    t = f"{X} {Rr}: H {a['plane']} {a['v']:.4f} {a['tgt']} ({a['sc']}) / J {b['plane']} {b['v']:.4f} {b['tgt']} ({b['sc']})"
                    out.setdefault('N2', []).append(t)
                    if min(a['sc'], b['sc']) >= 70: out.setdefault('N2s', []).append(t)
                    for c in hj:
                        tt = t + f" / H–J {c['plane']} {c['v']:.4f} {c['tgt']} ({c['sc']})"
                        out.setdefault('N3', []).append(tt)
                        if len({dig(a['tgt']), dig(b['tgt']), dig(c['tgt'])}) < 3: out.setdefault('N3d', []).append(tt)
                        if min(a['sc'], b['sc'], c['sc']) >= 70: out.setdefault('N3s', []).append(tt)
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for race, win in S.RACES:
        D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        N = len(D)
        for run, data in D.items():
            cs = cases(data)
            for k in KEYS:
                if k in cs:
                    t = tot[k]; t[0] += 1; t[1] += win in run; t[2] += 1 / N
                    if win in run: t[3].append(f'{race} {run}')
            for k in ('N3s', 'N3'):
                if k in cs:
                    print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}"); break
    print(f'\n## Totals over {len(S.RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
