"""Field check (17 Nov 2026, from Doncaster 16:00 23 Feb 2022 Silva Eclipse; read-only, picks / won / by chance over the result races).
Silva Eclipse: one sky pair S Quaoar – S Transpluto RA 122.1915 ninth 122.222 (87.41) carries the SAME royal star's natal line in both charts:
H Aldebaran – H Makemake RA 122.2730 (79.22) and J Aldebaran – J Neptune RA 122.2765 (77.78) (different natal bodies).
  S1   a sky pair (number family, any score) on the target of a natal royal line R – X in the H chart and of R – Z in the J chart, same R,
       royal lines in a number family (not conj / cp / opposition); X, Z any bodies (not the Moon)
  S1s  S1 with all three lines >= 70
  S1x  S1 with X != Z (different natal bodies, as Silva Eclipse)
  S1sx both
  R3   one royal star R on X in the sky (S R – S X), the horse chart and the jockey chart, all in a number family (Silva Eclipse Neptune
       Aldebaran: φ⁹ 70.29 / 93 88.91 / 122.222 77.78); R3s all >= 70; R3+ / R3s+ with a second royal star on sky X and natal X
  T    the same royal star on natal X in both charts and H X – J X, all three in one family (Silva Eclipse Makemake Aldebaran 122.222 /
       111.111 / 11.1111); T50 / T70 all >= 50 / 70. Largely geometry: natal R is nearly the same point in both charts.
Runner-level."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
from bb_fieldcheck_ceres_carrier import RACES as R0
RACES = list(dict.fromkeys(list(R0) + [('20220223_doncaster_1600', 'Silva Eclipse')]))
ROY = R.ROY
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['S1', 'S1s', 'S1x', 'S1sx', 'R3', 'R3s', 'R3+', 'R3s+', 'T', 'T50', 'T70']


def cases(D):
    # pair key -> {(chart, R): [(X, line, v, sc)]}
    hold = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        lines = {f"{x['line']} {x['plane']}": x for x in d['L'] if ' – ' in x['line'] and x['line'][0] in 'HJ' and ok(x)}
        for p in d['S']:
            x = lines.get(p.get('match'))
            if x is None or not ok(p) or ' – ' not in p['line'] or '→' in p['line']:
                continue
            Rr = x['line'].split(' – ')[0][2:]
            if Rr not in ROY:
                continue
            key = (p['line'], p['plane'])
            hold.setdefault(key, {'p': p, 'c': {}})['c'].setdefault((x['line'][0], Rr), []).append((X, x))
    out = {}
    for (pl, pp), h in hold.items():
        p = h['p']
        for Rr in ROY:
            for X, xh in h['c'].get(('H', Rr), []):
                for Z, xj in h['c'].get(('J', Rr), []):
                    t = (f"{pl} {pp} {p['v']:.4f} {p['tgt']} ({p['sc']}) carries {xh['line']} {xh['plane']} {xh['v']:.4f} ({xh['sc']}) and "
                         f"{xj['line']} {xj['plane']} {xj['v']:.4f} ({xj['sc']})")
                    s = min(p['sc'], xh['sc'], xj['sc']) >= 70
                    out.setdefault('S1', []).append(t)
                    if s: out.setdefault('S1s', []).append(t)
                    if X != Z:
                        out.setdefault('S1x', []).append(t)
                        if s: out.setdefault('S1sx', []).append(t)
    for X, d in D.items():
        if X == 'Moon':
            continue
        rows = d['L'] + d['O']
        hj = [r for r in d['L'] if r['line'] == f'H {X} – J {X}' and ok(r)]
        for Rr in ROY:
            g = {c: [r for r in rows if ok(r) and r['line'] in ((f'S {Rr} – S {X}', f'S {X} – S {Rr}') if c == 'S' else (f'{c} {Rr} – {c} {X}',))]
                 for c in 'SHJ'}
            if all(g.values()):
                b = {c: max(v, key=lambda r: r['sc']) for c, v in g.items()}
                t = f'{X} {Rr}: ' + '; '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})" for r in b.values())
                s = min(r['sc'] for r in b.values()) >= 70
                out.setdefault('R3', []).append(t)
                if s: out.setdefault('R3s', []).append(t)
                oth = [R2 for R2 in ROY if R2 != Rr
                       and any(ok(r) and r['line'] in (f'S {R2} – S {X}', f'S {X} – S {R2}') for r in rows)
                       and any(ok(r) and r['line'] in (f'H {R2} – H {X}', f'J {R2} – J {X}') for r in rows)]
                if oth:
                    out.setdefault('R3+', []).append(t)
                    if s: out.setdefault('R3s+', []).append(t)
            for a in g['H']:
                for b2 in g['J']:
                    for c in hj:
                        if a['fam'] == b2['fam'] == c['fam']:
                            t = f"{X} {Rr}: {a['v']:.4f} / {b2['v']:.4f} / H–J {c['v']:.4f} {a['fam']}"
                            m = min(a['sc'], b2['sc'], c['sc'])
                            out.setdefault('T', []).append(t)
                            if m >= 50: out.setdefault('T50', []).append(t)
                            if m >= 70: out.setdefault('T70', []).append(t)
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
            if 'S1s' in cs or 'S1' in cs:
                k = 'S1s' if 'S1s' in cs else 'S1'
                print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}")
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
