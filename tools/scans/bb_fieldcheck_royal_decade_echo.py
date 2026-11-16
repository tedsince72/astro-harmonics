"""Field check (16 Nov 2026, Eddie: 'start with the Sun - any possible rules'). Read-only.
Novakai (Doncaster 18:45 16 Jul 2022) Sun: H Fomalhaut – H Sun Dec 24.1407 silver 24.14 (95.9), only scoring one in the field;
S Neptune → H Sun Dec 2.4171 silver 2.414 (19.9) - the same family and digits a decade apart, on the same natal body and plane.
Versions over the 10 result races (picks = runners holding it; per case cells printed):
 S1   a natal royal line c R – c X (c = H or J) in a family + a sky body S Y -> c X (Y not the Moon) in the same plane, same family,
      target x10 or /10 (the decade echo)
 S1b  S1 with the royal line scoring >= 90
 S2   a natal royal line on natal Sun scoring >= 90 (H or J, RA or Dec)
 S3   a natal royal line on a fast natal body (Sun, Mercury, Venus, Mars) scoring >= 90
 S4   S1b on a fast body"""
import sys, re, math
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
sys.path.insert(0, 'tools/scans'); from bb_over100_tighten import RACES
RACES = RACES + [('Newton Abbot', '20220717_newton_abbot_1525', 'On Time'), ('Doncaster', '20220716_doncaster_1845', 'Novakai')]
PHI = (1 + 5 ** 0.5) / 2
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
FAST = ('Sun', 'Mercury', 'Venus', 'Mars')
CJ = ('conj', 'contraparallel', None)


def tval(fam, t):
    if t is None or fam in CJ or fam == 'golden':
        return None
    t = t.translate(SUP)
    m = re.fullmatch(r'(\d*)φ(-?\d*)', t)
    if m:
        return (int(m.group(1)) if m.group(1) else 1) * PHI ** (int(m.group(2)) if m.group(2) else 1)
    try:
        return float(t)
    except ValueError:
        return None


def decade(a, b):
    if not a or not b:
        return False
    q = max(a, b) / min(a, b)
    return abs(q - 10) < 0.05


def cases(X, d):
    out = {k: [] for k in ('S1', 'S1b', 'S2', 'S3', 'S4')}
    for r in d['L']:
        m = re.fullmatch(rf'([HJ]) ({"|".join(ROY)}) – \1 {X}', r['line'])
        if not m or r['fam'] in CJ or r['sc'] is None:
            continue
        c = m.group(1)
        txt = f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} {r['fam']} ({r['sc']})"
        if r['sc'] >= 90:
            if X == 'Sun': out['S2'].append(txt)
            if X in FAST: out['S3'].append(txt)
        tv = tval(r['fam'], r['tgt'])
        for o in d['O']:
            mo = re.fullmatch(rf'S (\w+) → {c} {X}', o['line'])
            if not mo or mo.group(1) == 'Moon' or o['plane'] != r['plane'] or o['fam'] != r['fam']:
                continue
            if decade(tv, tval(o['fam'], o['tgt'])):
                t2 = txt + f" | {o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})"
                out['S1'].append(t2)
                if r['sc'] >= 90:
                    out['S1b'].append(t2)
                    if X in FAST: out['S4'].append(t2)
    return out


KEYS = ['S1', 'S1b', 'S2', 'S3', 'S4']
tot = {k: [0, 0, 0.0] for k in KEYS}
for name, r, win in RACES:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
    print(f'\n## {name} ({N} runners, winner {win})')
    held = {k: set() for k in KEYS}
    for run, D in data.items():
        for X, d in D.items():
            o = cases(X, d)
            for k in KEYS:
                for t in o[k]:
                    held[k].add(run)
                    if k in ('S1b', 'S2'):
                        print(f'  [{k}] {run}{" *WINNER*" if win in run else ""} {X}: {t}')
    for k in KEYS:
        h = held[k]; w = sum(1 for x in h if win in x)
        tot[k][0] += len(h); tot[k][1] += w; tot[k][2] += len(h) / N
    print('  holders: ' + ', '.join(f'{k} {len(held[k])}' for k in KEYS))
print('\n## Totals (picks / winners / by chance)')
for k, (p, w, c) in tot.items():
    print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')
