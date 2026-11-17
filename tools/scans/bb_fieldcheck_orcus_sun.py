"""Field check (17 Nov 2026, from Eddie's Arvico Bleu Sun lines; read-only; picks / won / by chance over the result races).
S Orcus – S Sun Dec 3.2413 2×φ (83.8) and RA 42.3835 10φ³ (64.0); S Orcus → H Sun RA 122.0113 122 (43.3); S Orcus → J Sun RA 6.6711 ninth (66.5).
One sky body Y on sky X in both planes and on natal X in both charts (any plane), all in a number family (no conj / cp / opposition).
  O0  as above, any scores; Y not X, not the Moon, not a royal star
  O1  O0 with all four lines >= 40
  O2  O0 with X = the Sun
  O3  O1 with X = the Sun
  O4  O0 with Y also on X's same-body target (Y named in a 'Sky lines on the same target' row on S X -> c X)
Runner-level; races = bb_fieldcheck_arvico.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_arvico as A
RACES = A.RACES
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['O0', 'O1', 'O2', 'O3', 'O4']


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        ys = {}
        for o in d['O']:
            if not ok(o):
                continue
            ln = o['line']
            if ' – ' in ln and ln.startswith('S '):
                a, b = [s[2:] for s in ln.split(' – ')]
                Y = b if a == X else a if b == X else None
                if Y: ys.setdefault(Y, {}).setdefault('S' + o['plane'], []).append(o)
            elif ' → ' in ln:
                a, b = ln.split(' → ')
                if b in (f'H {X}', f'J {X}') and a.startswith('S '):
                    ys.setdefault(a[2:], {}).setdefault(b[0], []).append(o)
        same = {p['line'] for p in d['S']}
        for Y, g in ys.items():
            if Y in ('Moon', X) or Y in R.ROY or not all(k in g for k in ('SRA', 'SDec', 'H', 'J')):
                continue
            b = {k: max(g[k], key=lambda r: r['sc']) for k in ('SRA', 'SDec', 'H', 'J')}
            t = f'{X} by {Y}: ' + '; '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})" for r in b.values())
            s1 = min(r['sc'] for r in b.values()) >= 40
            out.setdefault('O0', []).append(t)
            if s1: out.setdefault('O1', []).append(t)
            if X == 'Sun':
                out.setdefault('O2', []).append(t)
                if s1: out.setdefault('O3', []).append(t)
            if any(f'S {Y}' in ln.split(' – ') or ln.startswith(f'S {Y} →') for ln in same):
                out.setdefault('O4', []).append(t)
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for race, win in RACES:
        D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        N = len(D)
        for run, data in D.items():
            cs = cases(data)
            for k in KEYS:
                if k in cs:
                    t = tot[k]; t[0] += 1; t[1] += win in run; t[2] += 1 / N
                    if win in run: t[3].append(f'{race} {run}')
            for k in ('O3', 'O2'):
                if k in cs:
                    print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}"); break
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
