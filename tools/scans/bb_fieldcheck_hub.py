"""Field check (16 Nov 2026, Eddie: 'so does it make a potential rule'), from Little Girl Blue (Bath 17:50 3 Jun 2022, won 10/1):
sky Makemake carries royal lines on several natal bodies (J Venus 4xphi with Aldebaran, H Mars 9xphi with Sedna, H Jupiter ninth 166.667
with Jupiter, H Pallas / H Makemake 32xphi BB53). Read-only; winners named below, no results file read. 15 result races, bybody xlsx.
A 'carry' = a sky pair S Y - S Z (no Moon; royal stars allowed as the other end) on the same family and target as a scoring royal line
c R - c X (family, not conj / cp / opposition); Y is a hub of natal X.
 H3   one sky body Y (not a royal star) carries royal lines on 3 or more different natal bodies of the runner (either chart)
 H4   the same with 4 or more
 H3r  H3 with one royal star on at least two of those royal lines
 H3n  H3 and Y also scores onto one of those natal bodies (S Y -> c X in a family)
 H3s  H3 with every carrying pair scoring >= 50"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_triangle import RACES
RACES = RACES + [('20240118_chelmsford_aw_1320', 'Sullivan Bay'), ('20220603_bath_1750', 'Little Girl Blue')]
NO = ('conj', 'contraparallel', 'opposition')
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
KEYS = ['H3', 'H4', 'H3r', 'H3n', 'H3s']
num = lambda r: r['fam'] and r['fam'] not in NO and r['sc'] is not None


def hubs(D):
    hub = {}
    for X, d in D.items():
        roy = {f"{r['line']} {r['plane']}": r for r in d['L'] if num(r) and any(f' {R} – ' in r['line'] for R in ROY)}
        nat = {r['line'] for r in d['O'] if ' → ' in r['line'] and num(r)}
        for p in d['S']:
            if ' – ' not in p['line'] or 'Moon' in p['line'] or not num(p): continue
            m = roy.get(p.get('match'))
            if not m: continue
            R = [R for R in ROY if f' {R} – ' in m['line']][0]
            for Y in (p['line'].split(' – ')[0][2:], p['line'].split(' – ')[1][2:]):
                if Y in ROY: continue
                h = hub.setdefault(Y, {})
                h.setdefault(X, []).append((R, p['sc'], f"{m['line']} {m['plane']} {m['tgt']} ({m['sc']}) by {p['line']} {p['plane']} ({p['sc']})",
                                            any(n.startswith(f'S {Y} → ') for n in nat)))
    return hub


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            tg = set()
            for Y, xs in hubs(D).items():
                if len(xs) < 3: continue
                tg.add('H3')
                if len(xs) >= 4: tg.add('H4')
                Rs = [R for v in xs.values() for R in {c[0] for c in v}]
                if any(Rs.count(R) >= 2 for R in set(Rs)): tg.add('H3r')
                if any(c[3] for v in xs.values() for c in v): tg.add('H3n')
                if sum(any(c[1] >= 50 for c in v) for v in xs.values()) >= 3: tg.add('H3s')
                ex.append(f"{run} hub S {Y} -> {len(xs)} bodies: " + '; '.join(f"{X}: {v[0][2]}" for X, v in xs.items()))
            for k in tg: held[k].append(run)
        for k in KEYS:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex:
            if win in x: print('    winner', x[:400])
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
