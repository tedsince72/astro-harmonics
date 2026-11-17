"""Field check (17 Nov 2026, from Carlisle 13:55 14 Oct 2021 Arvico Bleu; read-only, picks / won / by chance over the result races).
Arvico Bleu Sun: S Sun → H Sun Dec 22.2287 ninth 22.2222 (85.42) carried by the sky pair S Pallas – S Fomalhaut Dec 22.1942 (36.92) - a pair
holding a royal star - and that royal star on the pair's other end in the same chart: H Fomalhaut – H Pallas Dec 33.3254 ninth 33.3333 (88.05).
  Q0  a same-body line S X → c X (c = H or J; number family, not conj / cp / opposition) carried ('Sky lines on the same target') by a sky pair
      S Y – S R (R a royal star, Y not X, not the Moon), and the natal line c R – c Y in a number family (any score)
  Q1  Q0 with the same-body line >= 80 and the natal R – Y line >= 80
  Q2  Q0 with X = the Sun
  Q3  Q1 with X = the Sun
Runner-level; races = bb_fieldcheck_silva.RACES + Doncaster 16:00 23 Feb 2022 + Carlisle 13:55 14 Oct 2021."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_silva as S
RACES = list(dict.fromkeys(list(S.RACES) + [('20211014_carlisle_1355', 'Arvico Bleu')]))
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['Q0', 'Q1', 'Q2', 'Q3']


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        for c in 'HJ':
            for x in d['L']:
                if x['line'] != f'S {X} → {c} {X}' or not ok(x):
                    continue
                tag = f"{x['line']} {x['plane']}"
                for p in d['S']:
                    if p.get('match') != tag or not ok(p) or ' – ' not in p['line'] or '→' in p['line']:
                        continue
                    a, b = [s[2:] for s in p['line'].split(' – ')]
                    for Rr, Y in ((a, b), (b, a)):
                        if Rr not in R.ROY or Y in R.ROY or Y in ('Moon', X):
                            continue
                        nat = [r for r in D.get(Y, {}).get('L', []) if r['line'] == f'{c} {Rr} – {c} {Y}' and ok(r)]
                        for n in nat:
                            t = (f"{X}: {tag} {x['v']:.4f} {x['tgt']} ({x['sc']}) by {p['line']} {p['plane']} {p['v']:.4f} ({p['sc']}); "
                                 f"{n['line']} {n['plane']} {n['v']:.4f} {n['tgt']} ({n['sc']})")
                            out.setdefault('Q0', []).append(t)
                            s1 = x['sc'] >= 80 and n['sc'] >= 80
                            if s1: out.setdefault('Q1', []).append(t)
                            if X == 'Sun':
                                out.setdefault('Q2', []).append(t)
                                if s1: out.setdefault('Q3', []).append(t)
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
            for k in ('Q3', 'Q1', 'Q2'):
                if k in cs:
                    print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}"); break
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
