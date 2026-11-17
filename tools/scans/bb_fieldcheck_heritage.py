"""Field check (17 Nov 2026, Eddie's lines from Doncaster 14:10 29 Jan 2022 Miss Heritage, winner 10/1):
  S Chiron -> H Jupiter RA 95.4678 59xphi (88.4), Dec 17.7677 ninth 17.7778 (71.6)
  S Jupiter -> H Jupiter Dec 33.2798 ninth 33.3333 (19.7); S Jupiter -> J Jupiter RA 77.7093 ninth 77.7778 (56.0)
  S Jupiter - S Ceres RA 77.7421 ninth 77.7778 (77.1), on S Jupiter -> J Jupiter RA
  S Uranus -> J Saturn RA 177.7964 ninth 177.778 (94.8), Dec 28.0027 whole 28 (86.3)
Read-only; reads each race's _bybody.xlsx (eddie_bybody_rules.load). Versions (picks = runners holding it):
 B70  one sky body Y (not the Moon, not a royal star) on natal X (same chart) in RA and Dec, both in a number family >= 70
 B80  the same, both >= 80
 B2   two or more different B70 cases in the runner
 BN   a B70 case with one of its two lines a ninth
 BJ   a B70 case on natal Jupiter
 BD   two B70 lines (different cases) in the same family with targets in ratio 10 (17.7778 / 177.778)
 JJ   S Jupiter -> H Jupiter and S Jupiter -> J Jupiter both in a number family (any plane, any score)
 JN   JJ with both lines ninths
 JC   JJ and a sky pair S Jupiter - S Y on the same family + target as one of the two lines
 H2   B2 and JJ"""
import sys
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
sys.path.insert(0, 'tools/scans'); sys.argv = sys.argv[:1]
import bb_scan_uranus_pairs as U
RACES = list(U.RACES) + [('20220129_doncaster_1410', 'Miss Heritage')]
ROYAL = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
NUM = lambda r: r.get('fam') and r['fam'] not in ('conj', 'contraparallel', 'opposition') and r.get('sc') is not None
KEYS = ['B70', 'B80', 'B2', 'BN', 'BJ', 'BD', 'JJ', 'JN', 'JC', 'H2']


def tval(t):
    try:
        return float(t)
    except (TypeError, ValueError):
        return None


def runner(D):
    out = {k: [] for k in KEYS}
    cases = {}
    for X, g in D.items():
        for r in g['O']:
            ln = r['line']
            if not ln.startswith('S ') or '→' not in ln or not NUM(r):
                continue
            y, tgt = ln[2:].split(' → ')
            if y == 'Moon' or y in ROYAL:
                continue
            cases.setdefault((y, tgt), {}).setdefault(r['plane'], []).append(r)
    b70 = []
    for (y, tgt), pl in cases.items():
        if 'RA' in pl and 'Dec' in pl:
            ra = max(pl['RA'], key=lambda r: r['sc']); de = max(pl['Dec'], key=lambda r: r['sc'])
            if ra['sc'] >= 70 and de['sc'] >= 70:
                b70.append((y, tgt, ra, de))
    for y, tgt, ra, de in b70:
        t = f"S {y} → {tgt} RA {ra['v']:.4f} {ra['tgt']} {ra['fam']} ({ra['sc']}) / Dec {de['v']:.4f} {de['tgt']} {de['fam']} ({de['sc']})"
        out['B70'].append(t)
        if ra['sc'] >= 80 and de['sc'] >= 80: out['B80'].append(t)
        if 'ninth' in (ra['fam'], de['fam']): out['BN'].append(t)
        if tgt.endswith('Jupiter'): out['BJ'].append(t)
    if len(b70) >= 2:
        out['B2'].append('; '.join(f'S {y} → {tgt}' for y, tgt, _, _ in b70))
        lines = [(y, tgt, r) for y, tgt, ra, de in b70 for r in (ra, de)]
        for i, (y1, t1, r1) in enumerate(lines):
            for y2, t2, r2 in lines[i + 1:]:
                if (y1, t1) == (y2, t2) or r1['fam'] != r2['fam']: continue
                a, b = tval(r1['tgt']), tval(r2['tgt'])
                if a and b and abs(max(a, b) / min(a, b) - 10) < 1e-3:
                    out['BD'].append(f"S {y1} → {t1} {r1['plane']} {r1['tgt']} / S {y2} → {t2} {r2['plane']} {r2['tgt']} {r1['fam']}")
    J = D.get('Jupiter')
    if J:
        sh = [r for r in J['L'] if r['line'] == 'S Jupiter → H Jupiter' and NUM(r)]
        sj = [r for r in J['L'] if r['line'] == 'S Jupiter → J Jupiter' and NUM(r)]
        if sh and sj:
            out['JJ'].append(' / '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} {r['fam']} ({r['sc']})" for r in sh + sj))
            if all(r['fam'] == 'ninth' for r in sh + sj): out['JN'].append('both ninth')
            pairs = [o for o in J['S'] + J['O'] if o['line'].startswith('S Jupiter – S ') or o['line'].endswith('– S Jupiter')]
            pairs = [o for o in pairs if NUM(o) and '→' not in o['line']]
            for r in sh + sj:
                for o in pairs:
                    if o['fam'] == r['fam'] and o['tgt'] == r['tgt']:
                        out['JC'].append(f"{o['line']} {o['plane']} {o['v']:.4f} on {r['line']} {r['plane']} {r['tgt']}")
    if out['B2'] and out['JJ']: out['H2'].append('B2 + JJ')
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
                    if k in ('B70', 'JJ', 'BD', 'JC'):
                        for t in o[k][:3]:
                            print(f"  [{k}] {run}{' *WINNER*' if win in run else ''}: {t}")
        for k in KEYS:
            h = held[k]; w = sum(1 for x in h if win in x)
            tot[k][0] += len(h); tot[k][1] += w; tot[k][2] += len(h) / N
        print('  holders: ' + ', '.join(f'{k} {len(held[k])}' + ('*' if any(win in x for x in held[k]) else '') for k in KEYS))
    print(f'\n## Totals over {len(RACES)} races (picks / won / by chance)')
    for k, (p, w, c) in tot.items():
        print(f'  {k}: {p} / {w} / {c:.1f}')
