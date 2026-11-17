"""Field check (17 Nov 2026, from Ffos Las 17:25 23 Mar 2022 Ring The Moon Mercury; read-only, picks / won / by chance over the result races).
Ring The Moon: H Regulus – H Mercury RA 122.2550 ninth 122.222 (86.6) with S Uranus → J Mercury RA 122.4221 on the same target (18.2), and
S Uranus → H Mercury RA 10.0116 10 (42.2); Mercury back on both natal Uranus: S Mercury → H Uranus Dec 8.1095 5×φ (40.2), S Mercury → J Uranus
Dec 19.0078 19 (61.0). Eydon (Newmarket 15:35 2022): H Regulus – H Jupiter RA 111.1022 carried by S Uranus – S Regulus RA 111.1257.
  U0  a natal royal line R – X (number family, not conj / cp / opposition) with a sky body Y → natal X (either chart) on the same family +
      target ('Sky lines on the same target'), Y not X, not the Moon, not a royal star
  U1  a natal REGULUS line on X whose same-target list holds a line naming Uranus (S Uranus → c X, or a pair S Uranus – S Z / S Z – S Uranus)
  U2  mutual both charts: S Y → H X and S Y → J X, and S X → H Y and S X → J Y, all four in a number family (any score)
  U3  U0 and U2 with the same Y
  U4  U3 with R = Regulus and Y = Uranus (Ring The Moon's exact shape)
  U5  a natal Regulus line on X scoring >= 80 with S Uranus → natal X (either chart) on the same family + target
  U6  a natal Regulus line on X scoring >= 80 with any Uranus line on its target (S Uranus → c X or a pair with S Uranus; Eydon's pair form)
  U7  U5 at any Regulus score
  U8  U1 (Regulus line on X, a Uranus line on its target) and S X → H Uranus or J Uranus in a number family (the back-link; Eydon, Ring
      The Moon); U8a any Regulus score, U8 Regulus line >= 80
Runner-level."""
import sys, re
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_ringthemoon as RM
ROY = R.ROY
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['U0', 'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7', 'U8a', 'U8']


def mutual(D, X, Y):
    if Y not in D:
        return False
    a = [o for o in D[X]['O'] if o['line'] in (f'S {Y} → H {X}', f'S {Y} → J {X}') and ok(o)]
    b = [o for o in D[Y]['O'] if o['line'] in (f'S {X} → H {Y}', f'S {X} → J {Y}') and ok(o)]
    return {o['line'][-len(X) - 2] for o in a} == {'H', 'J'} and {o['line'][-len(Y) - 2] for o in b} == {'H', 'J'}


def cases(D):
    out = {}
    def add(k, t): out.setdefault(k, []).append(t)
    for X, d in D.items():
        if X == 'Moon':
            continue
        for x in d['L']:
            ln = x['line']
            if ' – ' not in ln or ln[0] not in 'HJ' or not ok(x):
                continue
            Rr = ln.split(' – ')[0][2:]
            if Rr not in ROY:
                continue
            tag = f"{ln} {x['plane']}"
            same = [p for p in d['S'] if p.get('match') == tag and ok(p)]
            if Rr == 'Regulus' and any('S Uranus' in p['line'] for p in same):
                add('U1', f'{X}: {tag} {x["tgt"]} ({x["sc"]})')
                us = [p for p in same if 'S Uranus' in p['line']]
                un = [p for p in us if '→' in p['line']]
                t = f"{X}: {tag} {x['v']:.4f} {x['tgt']} ({x['sc']}) / " + '; '.join(f"{p['line']} {p['plane']} {p['v']:.4f} ({p['sc']})" for p in us)
                if un:
                    add('U7', t)
                back = [o for o in D.get('Uranus', {}).get('O', []) if o['line'] in (f'S {X} → H Uranus', f'S {X} → J Uranus') and ok(o)]
                if back:
                    tb = f"{X}: {tag} {x['v']:.4f} {x['tgt']} ({x['sc']}) / back " + '; '.join(f"{o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})" for o in back)
                    add('U8a', tb)
                    if x['sc'] >= 80:
                        add('U8', tb)
                if x['sc'] >= 80:
                    add('U6', t)
                    if un:
                        add('U5', t)
            for p in same:
                m = re.match(r'S (\S+) → [HJ] (\S+)$', p['line'])
                if not m or m.group(2) != X:
                    continue
                Y = m.group(1)
                if Y in ('Moon', X) or Y in ROY:
                    continue
                t = f"{X}: {tag} {x['v']:.4f} {x['tgt']} ({x['sc']}) / {p['line']} {p['plane']} {p['v']:.4f} ({p['sc']})"
                add('U0', t)
                if mutual(D, X, Y):
                    add('U3', t)
                    if Rr == 'Regulus' and Y == 'Uranus':
                        add('U4', t)
        for Y in D:
            if Y not in (X, 'Moon') and Y not in ROY and X < Y and mutual(D, X, Y):
                add('U2', f'{X} <-> {Y}')
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}; n = 0
    for race, win in RM.RACES:
        try:
            D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        except FileNotFoundError:
            continue
        n += 1; N = len(D)
        for run, data in D.items():
            cs = cases(data)
            for k in KEYS:
                if k in cs:
                    t = tot[k]; t[0] += 1; t[1] += win in run; t[2] += 1 / N
                    t[3].append(('*' if win in run else '') + race[:16] + ' ' + run + ': ' + cs[k][0])
    print(f'## {n} result races (picks / won / by chance); * = winner')
    for k, (p, w, c, ws) in tot.items():
        print(f'  {k}: {p} / {w} / {c:.1f}')
        if p <= 12:
            for x in ws: print('      ', x)


if __name__ == '__main__':
    main()
