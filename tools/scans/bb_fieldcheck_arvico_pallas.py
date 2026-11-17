"""Field check (17 Nov 2026, Arvico Bleu Pallas; read-only; picks / won / by chance over the result races).
Arvico Bleu Pallas: H Regulus – H Pallas RA 160.1673 99×φ (44.22) carried by S Neptune – S Regulus RA 160.1691 99×φ (49.92) - the SAME royal
star in the pair - and the pair's other end on natal Pallas: S Neptune → H Pallas RA 0.0079 conj (99.47); Regulus also on sky Pallas
(S Regulus – S Pallas Dec 19.3973 12×φ (41.13)). Three royal stars on sky Pallas and natal Pallas: Fomalhaut (S Dec 22.2222 36.92 /
H Dec 33.3333 88.05), Antares (S Dec 19 85.09 / J RA 166.667 36.04), Regulus (S Dec 12×φ 41.13 / H RA 99×φ 44.22).
  PA0  a natal royal line c R – c X (number family) carried by a sky pair S Y – S R (the same royal star R; Y not X, not the Moon, not royal),
       and S Y → c X (same chart) scoring in any family, conj / cp included
  PA1  PA0 with S Y → c X a conjunction (or contraparallel)
  PA2  PA0 with R also on sky X (S R – S X in a number family)
  PB2  two or more royal stars each on sky X (S R – S X) and on natal X (c R – c X, either chart), all in a number family
  PB3  three or more
Runner-level; races = bb_fieldcheck_arvico.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_arvico as A
RACES = A.RACES
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
anyf = lambda r: r.get('fam') and r.get('sc') is not None
KEYS = ['PA0', 'PA1', 'PA2', 'PB2', 'PB3']


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        skyR = {Rr for Rr in R.ROY for o in d['O'] if ok(o) and o['line'] in (f'S {Rr} – S {X}', f'S {X} – S {Rr}')}
        natR = {x['line'].split(' – ')[0][2:] for x in d['L'] if ' – ' in x['line'] and x['line'][0] in 'HJ' and ok(x)
                and x['line'].split(' – ')[0][2:] in R.ROY}
        both = skyR & natR
        if len(both) >= 2: out.setdefault('PB2', []).append(f'{X}: royal stars on sky and natal {X}: {", ".join(sorted(both))}')
        if len(both) >= 3: out.setdefault('PB3', []).append(f'{X}: {", ".join(sorted(both))}')
        for x in d['L']:
            if ' – ' not in x['line'] or x['line'][0] not in 'HJ' or not ok(x):
                continue
            c, Rr = x['line'][0], x['line'].split(' – ')[0][2:]
            if Rr not in R.ROY:
                continue
            tag = f"{x['line']} {x['plane']}"
            for p in d['S']:
                if p.get('match') != tag or not ok(p) or ' – ' not in p['line'] or '→' in p['line']:
                    continue
                a, b = [s[2:] for s in p['line'].split(' – ')]
                if Rr not in (a, b):
                    continue
                Y = b if a == Rr else a
                if Y in ('Moon', X) or Y in R.ROY:
                    continue
                on = [o for o in d['O'] if o['line'] == f'S {Y} → {c} {X}' and anyf(o)]
                for o in on:
                    t = (f"{X}: {tag} {x['v']:.4f} {x['tgt']} ({x['sc']}) by {p['line']} {p['plane']} {p['v']:.4f} ({p['sc']}); "
                         f"{o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})")
                    out.setdefault('PA0', []).append(t)
                    if o['fam'] in ('conj', 'contraparallel'): out.setdefault('PA1', []).append(t)
                    if Rr in skyR: out.setdefault('PA2', []).append(t)
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
            for k in ('PA1', 'PB3'):
                if k in cs:
                    print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}")
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
