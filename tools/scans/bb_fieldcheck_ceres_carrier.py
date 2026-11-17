"""Field check (17 Nov 2026, Eddie: 'yes take a look at the Ceres and also if it goes further in Peak Time or Wotever Next').
Read-only; winners named below, no results file read.
Peak Time (Newcastle 15:40 11 Mar 2022, won 16/1) Ceres: S Ceres -> H Ceres Dec 6.008907 6 carried by S Makemake -> H Ceres Dec 5.993894 6;
S Ceres -> J Ceres Dec 4.002709 4 carried by S Makemake -> J Ceres Dec 4.017721 4; S Makemake - S Ceres Dec conj 0.015013 (95).
Wotever Next (Catterick 14:40 6 Apr 2022) Ceres: S Ceres -> H Ceres RA 179.9663 opposition carried by S Mercury - S Makemake RA; Dec 41.36 silver
carried by S Ketu - S Makemake Dec; S Makemake also on Ceres (S Makemake - S Ceres Dec 1.7755 ninth 36.3, S Makemake -> J Ceres Dec 3xphi 93.8).
'Carrier' = a 'Sky lines on the same target' row whose Matches is a same-body line S X -> c X (c = H / J, plane RA / Dec). Y = a sky body named in
the carrier row (not X, not the Moon, not a royal star).
 K2   one Y carries two or more different same-body lines of X (any chart / plane)
 K2c  ... the lines in both charts (H X and J X)              K2p  ... the same chart, both planes
 K2s  K2 with Y on sky X as well (S Y - S X scoring, any family, conj / cp incl.)
 K2x  K2 with Y conj / cp sky X (Peak Time)
 K2o  K2 with Y also on natal X outside the carriers (S Y -> c X scoring in a line not already counted)"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
from bb_fieldcheck_riverbray import RACES as R0
RACES = list(R0) + [('20220318_wolverhampton_aw_2030', 'Busby'), ('20220318_doncaster_1440', 'Olympe De Gouges'),
                    ('20220311_newcastle_1540', 'Peak Time')]
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
CJ = ('conj', 'contraparallel')
KEYS = ['K2', 'K2c', 'K2p', 'K2s', 'K2x', 'K2o']


def bodies(line):
    return [p.strip()[2:] for p in line.replace(' → ', '|').replace(' – ', '|').split('|') if p.strip().startswith('S ')]


def cases(X, d):
    same = {}
    for r in d['L']:
        if r['line'] in (f'S {X} → H {X}', f'S {X} → J {X}') and r['plane'] in ('RA', 'Dec') and r['sc'] is not None:
            same[f"{r['line']} {r['plane']}"] = r
    carry = {}
    for r in d['S']:
        m = r.get('match')
        if m not in same:
            continue
        for Y in bodies(r['line']):
            if Y in (X, 'Moon') or Y in ROY:
                continue
            carry.setdefault(Y, {}).setdefault(m, []).append(r)
    out = []
    for Y, ms in carry.items():
        if len(ms) < 2:
            continue
        t = {'K2'}
        charts = {m.split(' → ')[1][0] for m in ms}; planes = {(m.split(' → ')[1][0], m.rsplit(' ', 1)[1]) for m in ms}
        if len(charts) == 2: t.add('K2c')
        if any(sum(1 for c, p in planes if c == ch) == 2 for ch in 'HJ'): t.add('K2p')
        sky = [o for o in d['O'] if o['line'] == f'S {Y} – S {X}' and o['sc'] is not None]
        if sky: t.add('K2s')
        if any(o['fam'] in CJ for o in sky): t.add('K2x')
        used = {(c['line'], c['plane']) for rs in ms.values() for c in rs}
        if any(o['line'] in (f'S {Y} → H {X}', f'S {Y} → J {X}') and o['sc'] is not None and (o['line'], o['plane']) not in used
               for o in d['O']):
            t.add('K2o')
        txt = f"{X} by {Y}: " + '; '.join(
            f"{m} {same[m]['v']:.4f} {same[m]['tgt']} ({same[m]['sc']}) <- " +
            ', '.join(f"{c['line']} {c['plane']} {c['v']:.4f} ({c['sc']})" for c in rs) for m, rs in ms.items())
        if sky: txt += ' | sky: ' + ', '.join(f"{o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})" for o in sky)
        out.append((t, txt))
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = []
        for run, D in data.items():
            tg = set()
            for X, d in D.items():
                if X == 'Moon':
                    continue
                for t, s in cases(X, d):
                    tg |= t; ex.append(f"{run} [{', '.join(sorted(t))}] {s}")
            for k in tg: held[k].append(run)
        for k in KEYS:
            hh = held[k]; w = [x for x in hh if win in x]
            tot[k][0] += len(hh); tot[k][1] += len(w); tot[k][2] += len(hh) / N; tot[k][3] += w
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for x in ex: print('    ', x)
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k, (p, w, c, ws) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance  {ws}')


if __name__ == '__main__':
    main()
