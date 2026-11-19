"""Powers of sqrt 2 and of silver as distance families (19 Nov 2026, Eddie: 'try both and the powers but do one at a time' ->
'yes do that'; read-only, no scoring changed). Follows bb_scan_sqrt2_multiples.py (same lines, groups and tables).
Targets m x b^n, m = 1, 10, 100, n any integer, 0.3 <= value <= 180, n = 0 left out (1, 10, 100), tolerance 0.15 % of the target (as bybody's
phi powers):
  sqrt 2 powers  b = 1.41421 (even n are powers of 2: 2, 4, 8 ... and 20, 40 ... are already whole numbers);
  silver powers  b = 2.41421 (0.414, 2.414, 5.828, 14.07, 33.97, 82.01; x10 4.14, 24.14, 58.28, 140.7; x100 41.4).
'new' = a target the bybody scoring does not have today (no whole, golden, phi power, ninth, sqrt2 or silver target within 1e-6).
Baselines: bybody's phi powers and golden k x phi, counted the same way. Chosen after the results.
  python3 tools/scans/bb_scan_sqrt2_powers.py [cut]   (default 90)"""
import sys, os, json, math, itertools, io, contextlib
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 90
sys.argv = sys.argv[:1]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_regulus_apex as RA
R2, PHI = math.sqrt(2), (1 + 5 ** 0.5) / 2
SIL = 1 + R2


def powers(b):
    out = set()
    for m in (1, 10, 100):
        for n in range(-20, 20):
            v = m * b ** n
            if n and 0.3 <= v <= 180:
                out.add(round(v, 9))
    return sorted(out)


OLDT = [t for _f, _l, t, _tol in EB.TARGETS]
isnew = lambda t: all(abs(t - o) > 1e-6 for o in OLDT)
FAMS = {'sqrt 2 powers': [(t, 0.0015 * t, isnew(t)) for t in powers(R2)],
        'silver powers': [(t, 0.0015 * t, isnew(t)) for t in powers(SIL)],
        'phi powers': [(t, tol, True) for f, _l, t, tol in EB.TARGETS if f == 'phi power'],
        'golden': [(k * PHI, 0.0324, True) for k in range(1, 125)]}
TESTS = ('sqrt 2 powers', 'silver powers')


def fam_hit(v, fam):
    """-> (new, score) for the best target inside tolerance, else None."""
    if v is None:
        return None
    best = None
    for t, tol, nw in FAMS[fam]:
        d = abs(v - t)
        if d < tol:
            sc = 100 * (tol - d) / tol
            if best is None or sc > best[1]:
                best = (nw, sc)
    return best


def count(vals, fam):
    n = new = 0
    for v in vals:
        h = fam_hit(v, fam)
        if h and h[1] >= CUT:
            n += 1
            if h[0]:
                new += 1
    return n, new


def sky_vals(tt):
    out = []
    for pl in ('RA', 'Dec'):
        for a, b in itertools.combinations(EB.BODIES, 2):
            if {a, b} != {'Rahu', 'Ketu'}:
                out.append(EB.pair(tt, 'S', pl, a, b))
    return out


def runner_vals(r):
    nat, son, same = [], [], []
    for ch in ('H', 'J'):
        d = r['dist'].get(ch)
        if not d:
            continue
        for pl in ('RA', 'Dec'):
            for a, b in itertools.combinations(EB.NATAL_BODIES, 2):
                if {a, b} != {'Rahu', 'Ketu'}:
                    nat.append(EB.pair(d, 'N', pl, a, b))
            for X in EB.NATAL_BODIES:
                same.append(d.get(('S', pl, X, X)))
                for Y in EB.BODIES:
                    if Y != X:
                        son.append(d.get(('S', pl, Y, X)))
    return {'natal': nat, 'sky on natal': son, 'same-body': same}


def main():
    races = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        rf = f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
        cover = None
        if os.path.exists(rf):
            J = json.load(open(rf))
            held = {r: set() for r in J['runners']}
            for rid, cs in J['rules'].items():
                for c in cs:
                    if not c.get('watch_only'):
                        held.setdefault(c['runner'], set()).add(rid)
            picks = {RA.key(r) for r in J['runners'] if any(set(c) <= held[r] for c in RA.C8)}
            cover = RA.key(win) in picks if picks else None
        sv = sky_vals(tt)
        sky = {f: count(sv, f) for f in FAMS}
        run = {}
        for cloth, r in runners.items():
            vals = runner_vals(r)
            run[RA.key(r['name'].get('H') or '')] = {(t, f): count(v, f) for t, v in vals.items() for f in FAMS}
        fav = F.FAV.get(race)
        races.append(dict(race=race, win=RA.key(win), fav=RA.key(fav) if fav else None, cover=cover, sky=sky, run=run))
    print(f'# Powers of sqrt 2 and of silver (m x b^n, m 1 / 10 / 100, ±0.15 %), cut {CUT:g}; phi powers and golden as baselines\n')
    for f in TESTS:
        print(f"{f}: " + ', '.join(f"{t:.4g}{'' if nw else '*'}" for t, _tol, nw in FAMS[f]) + '  (* = already a bybody target)\n')
    print(f'{len(races)} result races with an _active.xlsx. Chosen after the results; read-only. '
          "'new' = lines on a target the bybody scoring does not have today.\n")

    # sky
    print('## Sky lines S A - S B per race (mean)\n')
    print('| family | all races | cover hit | cover miss | fav won | fav lost |\n|---|---|---|---|---|---|')
    for f, i, lab in tuple((f, i, f + (' new' if i else ' all')) for f in TESTS for i in (0, 1)) + (('phi powers', 0, 'phi powers'), ('golden', 0, 'golden')):
        def m(sel):
            xs = [r['sky'][f][i] for r in races if sel(r)]
            return f'{sum(xs) / len(xs):.2f} ({len(xs)})' if xs else '-'
        print(f"| {lab} | {m(lambda r: True)} | {m(lambda r: r['cover'] is True)} | {m(lambda r: r['cover'] is False)} | "
              f"{m(lambda r: r['fav'] and r['fav'] == r['win'])} | {m(lambda r: r['fav'] and r['fav'] != r['win'])} |")

    # runners
    print('\n## Per runner: winner against its field\n')
    print('Top = winner has the most lines in its field (ties count; chance = share of the field tied at the top). '
          'Bottom the same at the fewest. Mean = lines per runner.\n')
    print('| lines | family | winner mean | others mean | winner top | chance | winner bottom | chance |\n|---|---|---|---|---|---|---|---|')
    for t in ('natal', 'sky on natal', 'same-body'):
        for f, i, lab in tuple((f, i, f + (' new' if i else ' all')) for f in TESTS for i in (0, 1)) + (('phi powers', 0, 'phi powers'), ('golden', 0, 'golden')):
            wm, om, top, ctop, bot, cbot, nr = [], [], 0, 0.0, 0, 0.0, 0
            for r in races:
                vals = {n: v[(t, f)][i] for n, v in r['run'].items()}
                if r['win'] not in vals:
                    continue
                nr += 1
                w = vals[r['win']]
                wm.append(w)
                om += [v for n, v in vals.items() if n != r['win']]
                mx, mn, k = max(vals.values()), min(vals.values()), len(vals)
                top += w == mx
                ctop += sum(v == mx for v in vals.values()) / k
                bot += w == mn
                cbot += sum(v == mn for v in vals.values()) / k
            print(f'| {t} | {lab} | {sum(wm) / len(wm):.2f} | {sum(om) / len(om):.2f} | {top} / {nr} | {ctop:.1f} | '
                  f'{bot} / {nr} | {cbot:.1f} |')

    # favourites
    print('\n## Favourite against its field (races with a favourite)\n')
    print('| lines | family | fav won: fav top / chance | fav lost: fav top / chance | fav lost: fav bottom / chance |\n'
          '|---|---|---|---|---|')
    for t in ('natal', 'sky on natal', 'same-body'):
        for f, i, lab in tuple((f, i, f + (' new' if i else ' all')) for f in TESTS for i in (0, 1)) + (('phi powers', 0, 'phi powers'), ('golden', 0, 'golden')):
            acc = {'w': [0, 0.0, 0], 'l': [0, 0.0, 0, 0, 0.0]}
            for r in races:
                vals = {n: v[(t, f)][i] for n, v in r['run'].items()}
                if not r['fav'] or r['fav'] not in vals:
                    continue
                fv, mx, mn, k = vals[r['fav']], max(vals.values()), min(vals.values()), len(vals)
                g = 'w' if r['fav'] == r['win'] else 'l'
                a = acc[g]
                a[0] += fv == mx
                a[1] += sum(v == mx for v in vals.values()) / k
                a[2] += 1
                if g == 'l':
                    a[3] += fv == mn
                    a[4] += sum(v == mn for v in vals.values()) / k
            w, l = acc['w'], acc['l']
            print(f'| {t} | {lab} | {w[0]} / {w[2]} ({w[1]:.1f}) | {l[0]} / {l[2]} ({l[1]:.1f}) | {l[3]} / {l[2]} ({l[4]:.1f}) |')


if __name__ == '__main__':
    main()
