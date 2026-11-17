"""Field check (17 Nov 2026, from Perth 16:10 20 Apr 2022 Daphne Moon; read-only, picks / won / by chance over the result races).
Haumea (H): H Haumea – J Haumea RA 16.6664 ninth (99.31) carried by S Juno – S Regulus Dec 16.6500 (50.08); H Regulus – H Haumea Dec 5.9999 6
(99.65); S Regulus – S Haumea RA 40×φ (76.66); Juno on both natal Haumeas (S Juno → H Haumea Dec 14×φ 91.99, → J Haumea Dec 26 83.71).
  H0  H X – J X in a number family (no conj / contraparallel / opposition) >= 90 carried by a sky pair S A – S R (R a royal star) on its target
  H1  H0 + a natal line R – X (the same royal star, H or J chart) in a number family
  H1s H1 with that natal R line >= 90
  H2  H1 + S R – S X in a number family (royal star on sky X)
  H3  H1 + the pair's other end A on natal X (S A → H X or J X in a number family)
  H4  H2 + H3 (Daphne Moon's whole picture)
  P0  reference: H X – J X >= 90 carried by any sky pair (royal star or not)
Sun (S): S Sun → J Sun Dec 4.8629 3×φ (72.88); S Uranus → H Sun Dec 4.8536 3×φ (98.3) on the same target; S Uranus → J Sun RA φ¹⁰ (83.82).
  S0  a same-body line S X → cA X in a number family and a sky body Y (not X, not the Moon) onto the other chart's X, S Y → cB X, on the same
      family + target and plane (the 'Sky lines on the same target' row)
  S1  S0 with the S Y → cB X line >= 90
  S2  S1 + Y on cA X too (S Y → cA X in a number family, any plane)
  S3  S2 with the S Y → cA X line in the other plane
Rows from eddie_bybody_rules.load (the bybody xlsx); runner-level (a runner holds a version if any body does)."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_royal_cut as C
RACES = C.RACES + [('20220504_kelso_1450', 'Domandlouis'), ('20220420_perth_1610', 'Daphne Moon')]
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r, cut=None: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None and (cut is None or r['sc'] >= cut)
KEYS = ['P0', 'H0', 'H1', 'H1s', 'H2', 'H3', 'H4', 'S0', 'S1', 'S2', 'S3']


def cases(D):
    out = {}
    def add(k, txt): out.setdefault(k, []).append(txt)
    for X, d in D.items():
        if X == 'Moon':
            continue
        # Haumea shape
        for hj in d['L']:
            if hj['line'] != f'H {X} – J {X}' or not ok(hj, 90):
                continue
            tag = f"{hj['line']} {hj['plane']}"
            for p in d['S']:
                if p.get('match') != tag or not ok(p) or ' – ' not in p['line'] or '→' in p['line']:
                    continue
                a, b = [s[2:] for s in p['line'].split(' – ')]
                add('P0', f"{X}: {tag} {hj['v']:.4f} {hj['tgt']} ({hj['sc']}) by {p['line']} {p['plane']} ({p['sc']})")
                for R_, A in ((a, b), (b, a)):
                    if R_ not in C.ROY:
                        continue
                    base = f"{X}: {tag} {hj['v']:.4f} {hj['tgt']} ({hj['sc']}) by {p['line']} {p['plane']} ({p['sc']})"
                    add('H0', base)
                    nat = [x for x in d['L'] if x['line'] in (f'H {R_} – H {X}', f'J {R_} – J {X}') and ok(x)]
                    if not nat:
                        continue
                    nb = max(nat, key=lambda x: x['sc'])
                    t1 = base + f"; {nb['line']} {nb['plane']} {nb['v']:.4f} {nb['tgt']} ({nb['sc']})"
                    add('H1', t1)
                    if nb['sc'] >= 90: add('H1s', t1)
                    sky = [o for o in d['O'] if o['line'] in (f'S {R_} – S {X}', f'S {X} – S {R_}') and ok(o)]
                    end = [o for o in d['O'] if o['line'] in (f'S {A} → H {X}', f'S {A} → J {X}') and ok(o)]
                    if sky: add('H2', t1 + f"; {sky[0]['line']} {sky[0]['plane']} ({sky[0]['sc']})")
                    if end: add('H3', t1 + f"; {', '.join(o['line'] + ' ' + o['plane'] + ' (' + str(o['sc']) + ')' for o in end)}")
                    if sky and end: add('H4', t1)
        # Sun shape
        for sb in d['L']:
            for ca, cb in (('H', 'J'), ('J', 'H')):
                if sb['line'] != f'S {X} → {ca} {X}' or not ok(sb):
                    continue
                tag = f"{sb['line']} {sb['plane']}"
                for y in d['S']:
                    if y.get('match') != tag or not ok(y) or '→' not in y['line'] or not y['line'].endswith(f'→ {cb} {X}'):
                        continue
                    Y = y['line'].split(' → ')[0][2:]
                    if Y in (X, 'Moon') or Y in C.ROY:
                        continue
                    t = f"{X}: {tag} {sb['v']:.4f} {sb['tgt']} ({sb['sc']}); {y['line']} {y['plane']} {y['v']:.4f} ({y['sc']})"
                    add('S0', t)
                    if y['sc'] < 90:
                        continue
                    add('S1', t)
                    both = [o for o in d['O'] if o['line'] == f'S {Y} → {ca} {X}' and ok(o)]
                    if both:
                        add('S2', t + f"; {both[0]['line']} {both[0]['plane']} {both[0]['tgt']} ({both[0]['sc']})")
                        if any(o['plane'] != sb['plane'] for o in both): add('S3', t)
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
                    if k in ('H4', 'H2', 'H1s', 'S3', 'S2'):
                        print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}")
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {", ".join(ws)}')


if __name__ == '__main__':
    main()
