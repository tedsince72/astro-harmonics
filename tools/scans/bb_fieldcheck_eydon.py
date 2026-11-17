"""Field check (17 Nov 2026, from Newmarket 15:35 14 Apr 2022 Eydon Jupiter; read-only, picks / won / by chance over the result races).
Eydon: H Regulus – H Jupiter RA 111.1022 ninth 111.111 (95.99) carried by S Uranus – S Regulus RA 111.1257 (93.4) - the SAME royal star in the
sky pair; S Jupiter → H Uranus Dec 14.5457 9×φ (48.9) (sky X onto the pair's other end, natal); lights on sky Jupiter: S Moon – S Jupiter Dec
7.9996 8 (97.8), S Sun – S Jupiter RA 27.5089 17×φ (92.7).
  G0  a natal royal line R – X (H or J chart, number family, not conj / cp / opposition) carried by a sky pair S Y – S R with the same royal
      star R, on the same family + target ('Sky lines on the same target'), pair in a number family; X, Y not the Moon
  G0s G0 with both lines >= 90
  G1  G0 + sky X onto natal Y (S X → H Y or J Y, number family, any plane, any score)
  G2  G1 + a light on sky X: S Sun – S X or S Moon – S X in a number family (any plane)
  G2s G2 with a light line >= 90
  G3  G0 + a light on sky X (without G1)
Runner-level (a runner holds a version if any body does)."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_daphne as F
RACES = F.RACES + [('20220414_newmarket_1535', 'Eydon')]
ROY = R.ROY
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r, cut=None: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None and (cut is None or r['sc'] >= cut)
KEYS = ['G0', 'G0s', 'G1', 'G2', 'G2s', 'G3']


def cases(D):
    out = {}
    def add(k, t): out.setdefault(k, []).append(t)
    for X, d in D.items():
        if X == 'Moon':
            continue
        lights = [o for o in d['O'] if o['line'] in (f'S Sun – S {X}', f'S {X} – S Sun', f'S Moon – S {X}', f'S {X} – S Moon') and ok(o)]
        for x in d['L']:
            ln = x['line']
            if ' – ' not in ln or ln[0] not in 'HJ' or not ok(x):
                continue
            Rr = ln.split(' – ')[0][2:]
            if Rr not in ROY:
                continue
            tag = f"{ln} {x['plane']}"
            for p in d['S']:
                if p.get('match') != tag or not ok(p) or '→' in p['line'] or ' – ' not in p['line']:
                    continue
                a, b = [s[2:] for s in p['line'].split(' – ')]
                if Rr not in (a, b):
                    continue
                Y = b if a == Rr else a
                if Y in ('Moon', X) or Y in ROY:
                    continue
                t = f"{X}: {tag} {x['v']:.4f} {x['tgt']} ({x['sc']}) by {p['line']} {p['plane']} {p['v']:.4f} ({p['sc']})"
                add('G0', t)
                if x['sc'] >= 90 and p['sc'] >= 90: add('G0s', t)
                back = [o for o in D.get(Y, {}).get('O', []) if o['line'] in (f'S {X} → H {Y}', f'S {X} → J {Y}') and ok(o)]
                if lights and not back: add('G3', t)
                if back:
                    t1 = t + f"; {back[0]['line']} {back[0]['plane']} {back[0]['v']:.4f} ({back[0]['sc']})"
                    add('G1', t1)
                    if lights:
                        add('G2', t1 + '; ' + ', '.join(f"{o['line']} {o['plane']} ({o['sc']})" for o in lights))
                        if any(o['sc'] >= 90 for o in lights): add('G2s', t1)
                    if lights: add('G3', t)
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
                    if win in run: t[3].append(run)
            for k in ('G2s', 'G2', 'G0s'):
                if k in cs:
                    print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}"); break
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {", ".join(ws)}')


if __name__ == '__main__':
    main()
