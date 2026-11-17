"""Field check (17 Nov 2026, Eddie 'need to investigate!'; Lingfield 15:00 23 Jan 2022, Two For Gold won 10/1, 6 rules, blind lead missed).
Two For Gold: one sky pair S Saturn – S Fomalhaut RA 27.5096 17×φ (90.59) carries two natal lines on two different bodies:
H Regulus – H Quaoar Dec 27.5010 (82.7) and S Juno → J Juno Dec 27.5288 (31.37). Read-only; reads each race's _bybody.xlsx
('Sky lines on the same target' rows: the S group of body X, 'match' = the natal line it carries). Versions (picks = runners):
 DP0  one sky pair (line + plane) carries natal lines on two or more different bodies
 DP1  DP0 with one carried line a same-body line (S X -> c X) and another a royal line (R – Y), X != Y
 DP2  DP1 with the pair >= 90
 DP3  DP1 with the pair naming a royal star
 DP4  DP2 and DP3 (Two For Gold)
 PP   S Pluto -> H Pluto and S Pluto -> J Pluto both in a number family (Two For Gold 16.6667 / 47×φ)"""
import sys
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
sys.path.insert(0, 'tools/scans'); sys.argv = sys.argv[:1]
import bb_fieldcheck_heritage as H
RACES = list(H.RACES) + [('20220123_lingfield_1500', 'Two For Gold')]
ROYAL = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
KEYS = ['DP0', 'DP1', 'DP2', 'DP3', 'DP4', 'PP']


def runner(D):
    out = {k: [] for k in KEYS}
    car = {}
    for X, g in D.items():
        for r in g['S']:
            m = r.get('match')
            if not m or not H.NUM(r):
                continue
            car.setdefault((r['line'], r['plane']), {'sc': r['sc'], 'v': r['v'], 'tgt': r['tgt'], 'lines': set()})['lines'].add((X, m))
    for (pl_line, plane), c in car.items():
        bodies = {x for x, _ in c['lines']}
        if len(bodies) < 2:
            continue
        t = f"{pl_line} {plane} {c['v']:.4f} {c['tgt']} ({c['sc']}) carries " + '; '.join(f'{x}: {m}' for x, m in sorted(c['lines']))
        out['DP0'].append(t)
        same = {x for x, m in c['lines'] if m.startswith('S ') and '→' in m and m.split(' → ')[0][2:] == x}
        roy = {x for x, m in c['lines'] if any(m.startswith(f'{ch} {R} –') for ch in 'HJ' for R in ROYAL)}
        if any(a != b for a in same for b in roy):
            out['DP1'].append(t)
            if c['sc'] >= 90: out['DP2'].append(t)
            if any(R in pl_line for R in ROYAL): out['DP3'].append(t)
            if c['sc'] >= 90 and any(R in pl_line for R in ROYAL): out['DP4'].append(t)
    P = D.get('Pluto')
    if P:
        sh = [r for r in P['L'] if r['line'] == 'S Pluto → H Pluto' and H.NUM(r)]
        sj = [r for r in P['L'] if r['line'] == 'S Pluto → J Pluto' and H.NUM(r)]
        if sh and sj:
            out['PP'].append(' / '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})" for r in sh + sj))
    return out


if __name__ == '__main__':
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        print(f'\n## {r} ({N} runners, winner {win})')
        held = {k: [] for k in KEYS}
        for run, D in data.items():
            o = runner(D)
            for k in KEYS:
                if o[k]:
                    held[k].append(run)
                    if k in ('DP2', 'DP4', 'PP'):
                        print(f"  [{k}] {run}{' *WINNER*' if win in run else ''}: {o[k][0]}")
        for k in KEYS:
            h = held[k]; w = sum(1 for x in h if win in x)
            tot[k][0] += len(h); tot[k][1] += w; tot[k][2] += len(h) / N
        print('  holders: ' + ', '.join(f'{k} {len(held[k])}' + ('*' if any(win in x for x in held[k]) else '') for k in KEYS))
    print(f'\n## Totals over {len(RACES)} races (picks / won / by chance)')
    for k, (p, w, c) in tot.items():
        print(f'  {k}: {p} / {w} / {c:.1f}')
