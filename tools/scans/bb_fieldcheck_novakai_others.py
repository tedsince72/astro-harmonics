"""Field check (16 Nov 2026, Eddie: 'can you check and see if any are worth pursuing'), Novakai (Doncaster 18:45 16 Jul 2022), read-only.
Over the 10 result races (picks = runners holding it; conj / contraparallel never counted; the Moon never a sky body):
 Q1  one royal star on natal X in both planes in the same chart, both lines >= 90 (Novakai H Fomalhaut – H Quaoar Dec 14.1432 √2 95.0,
     RA 70.0018 70 91.2); X not Rahu / Ketu
 Q2  Q1 + a sky pair (S rows) on the same family + target as one of the two lines (S Makemake – S Sedna Dec 14.1430)
 E1  H X – J X scoring >= 90 + a sky body S Y -> H X or J X scoring >= 90 (Novakai Eris: 10.0012 (94.2), S Pluto -> H Eris 97.5)
 E2  E1 with S Y -> natal X in the same plane as H X – J X
 N1  a royal line c R – c X >= 90 + a sky body S Y -> c X >= 90, same chart (Novakai J Antares – J Neptune 93.4, S Ceres -> J Neptune 98.3)
 N2  N1 with both in the same plane"""
import sys, re
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
sys.path.insert(0, 'tools/scans'); from bb_fieldcheck_royal_decade_echo import RACES
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
CJ = ('conj', 'contraparallel', None)
ok = lambda r, m=90: r['fam'] not in CJ and (r['sc'] or 0) >= m
KEYS = ['Q1', 'Q2', 'E1', 'E2', 'N1', 'N2']


def cases(X, d):
    out = {k: [] for k in KEYS}
    roy = [r for r in d['L'] if re.fullmatch(rf'([HJ]) ({"|".join(ROY)}) – \1 {X}', r['line']) and ok(r)]
    sky = [o for o in d['O'] if re.fullmatch(rf'S (\w+) → [HJ] {X}', o['line']) and not o['line'].startswith('S Moon')
           and not any(o['line'].startswith(f'S {R} ') for R in ROY) and ok(o)]
    if X not in ('Rahu', 'Ketu'):
        for a in roy:
            for b in roy:
                if a['line'] == b['line'] and a['plane'] == 'RA' and b['plane'] == 'Dec':
                    t = f"{a['line']} RA {a['v']:.4f} {a['tgt']} ({a['sc']}) / Dec {b['v']:.4f} {b['tgt']} ({b['sc']})"
                    out['Q1'].append(t)
                    sp = [s for s in d['S'] if ' – ' in s['line'] and s['fam'] not in CJ
                          and any(s['fam'] == r['fam'] and s['tgt'] == r['tgt'] and s['plane'] == r['plane'] for r in (a, b))]
                    if sp:
                        out['Q2'].append(t + f" | {sp[0]['line']} {sp[0]['plane']} {sp[0]['v']:.4f} ({sp[0]['sc']})")
    hj = [r for r in d['L'] if r['line'] == f'H {X} – J {X}' and not r['plane'].endswith('contraparallel') and ok(r)]
    for h in hj:
        for o in sky:
            t = f"{h['line']} {h['plane']} {h['v']:.4f} {h['tgt']} ({h['sc']}) | {o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})"
            out['E1'].append(t)
            if o['plane'] == h['plane']:
                out['E2'].append(t)
    for a in roy:
        c = a['line'][0]
        for o in sky:
            if o['line'].endswith(f'→ {c} {X}'):
                t = f"{a['line']} {a['plane']} {a['v']:.4f} {a['tgt']} ({a['sc']}) | {o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})"
                out['N1'].append(t)
                if o['plane'] == a['plane']:
                    out['N2'].append(t)
    return out


tot = {k: [0, 0, 0.0] for k in KEYS}
for name, r, win in RACES:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
    held = {k: set() for k in KEYS}
    for run, D in data.items():
        for X, d in D.items():
            o = cases(X, d)
            for k in KEYS:
                if o[k]:
                    held[k].add(run)
                    if k in ('Q2', 'E2', 'N2'):
                        print(f'  [{k}] {name} {run}{" *WINNER*" if win in run else ""} {X}: {o[k][0]}')
    for k in KEYS:
        h = held[k]; tot[k][0] += len(h); tot[k][1] += sum(win in x for x in h); tot[k][2] += len(h) / N
    print(f'## {name} (N {N}, winner {win}): ' + ', '.join(f'{k} {len(held[k])}' for k in KEYS))
print('\n## Totals (picks / winners / by chance)')
for k, (p, w, c) in tot.items():
    print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')
