"""Field check (17 Nov 2026, from Wincanton 14:20 21 Mar 2022 River Bray; read-only, picks / won / by chance over the result races).
River Bray: H Jupiter – J Jupiter RA 15.5478 ninth 15.5556 (75.05) with the same target in the sky twice (S Sun – S Quaoar Dec 15.5562 98.02,
S Venus – S Pluto RA 15.5592 88.26), and BB68 on Mars (S Mars → H Mars Dec 40.3566 split at sky Transpluto: 29.0384 φ⁷ 90.9 + 11.3182 7×φ 75.11).
  J0  H Jupiter – J Jupiter in a number family (not conj / cp / opposition) scoring >= 50, a sky pair (not naming Jupiter) on its family + target
  J1  J0 with 2 or more such sky pairs
  J2  J0 with a sky pair scoring >= 90
  J3  J1 and J2 (River Bray's shape)
  J0any J0 at any H–J Jupiter score
  J1any J0any with 2 or more sky pairs on the target (River Bray 2, Society Red 5)
  B68 BB68 as built (any body)
  J0+B68, J1+B68, J2+B68, J3+B68, J0any+B68  held together (runner-level)
Runner-level."""
import sys, json, os
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_ringthemoon as RM
RACES = list(RM.RACES) + [('20220321_wincanton_1420', 'River Bray')]
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['J0', 'J1', 'J2', 'J3', 'J0any', 'J1any', 'B68', 'J0+B68', 'J1+B68', 'J2+B68', 'J3+B68', 'J0any+B68', 'J1any+B68']


def tags(D, b68):
    t, txt = set(), ''
    J = D.get('Jupiter')
    if J:
        for x in J['L']:
            if x['line'] != 'H Jupiter – J Jupiter' or not ok(x):
                continue
            tag = f"{x['line']} {x['plane']}"
            ps = [p for p in J['S'] if p.get('match') == tag and ok(p) and ' – ' in p['line'] and 'Jupiter' not in p['line']]
            if not ps:
                continue
            k = {'J0any'}
            if len(ps) >= 2: k.add('J1any')
            if x['sc'] >= 50:
                k.add('J0')
                if len(ps) >= 2: k.add('J1')
                if any(p['sc'] >= 90 for p in ps): k.add('J2')
                if 'J1' in k and 'J2' in k: k.add('J3')
            t |= k
            txt = f"{tag} {x['v']:.4f} {x['tgt']} ({x['sc']}) / " + '; '.join(f"{p['line']} {p['plane']} {p['v']:.4f} ({p['sc']})" for p in ps)
    if b68:
        t.add('B68')
        for k in ('J0', 'J1', 'J2', 'J3', 'J0any', 'J1any'):
            if k in t: t.add(k + '+B68')
    return t, txt


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    n = 0
    for race, win in RACES:
        p = f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'
        f = f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
        if not (os.path.exists(p) and os.path.exists(f)):
            continue
        n += 1
        data = R.load(p)
        b68 = {c['runner'] for c in json.load(open(f))['rules']['BB68'] if not c['watch_only']}
        N = len(data)
        for run, D in data.items():
            t, txt = tags(D, run in b68)
            for k in t:
                x = tot[k]; x[0] += 1; won = win in run; x[1] += won; x[2] += 1 / N
                x[3].append(('*' if won else '') + f'{race[:20]} {run}: ' + (txt if k != 'B68' else 'BB68'))
    print(f'## {n} result races (picks / won / by chance); * = winner')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}')
        if k != 'B68' and p <= 15:
            for x in ws: print('      ', x)


if __name__ == '__main__':
    main()
