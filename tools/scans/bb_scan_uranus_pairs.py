"""Uranus pairs scan (17 Nov 2026, Eddie: 'I often see certain pairs, especially Uranus ones like Venus, Jupiter, Regulus ... if we
measure these in each race what do we see, especially in terms of ratios and splits'; read-only, no rule).

Per race (bb_fieldcheck_nelson.RACES + Newcastle AW 16:40 2022, those with an _active.xlsx), per runner, for X = Venus, Jupiter,
Regulus against Uranus, planes RA (wrapped 0-180) and Dec (|dDec|), from the _POS tabs (eddie_bybody.load):
  lines   S X – S U (sky, the same for every runner), H X – H U, J X – J U, S U → H X, S X → H U, S U → J X, S X → J U
  ratios  the pair line between charts, same plane, larger / smaller: H / S, J / S, H / J (eddie_bybody.ratio_hits: interval list +
          1/10-1/20 cuts); a leg inside the conjunction range is not scored
  splits  a sky body Y (not the Moon, not X, not Uranus) between the two ends of H X – H U / J X – J U (Dec signed; RA on the shorter
          arc) cutting it into two pieces |Y - X|, |Y - U| that both score in a number family (eddie_bybody.hits; conj / opposition out)
Scores: eddie_bybody's linear scoring (its own families). Field check: per pair and measure, runners holding it at a cut,
picks / won / by chance (sum of 1 / field size)."""
import os, sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
import bb_fieldcheck_nelson as Q

RACES = [r for r in list(Q.RACES) + [('20220215_newcastle_aw_1640', 'Sir Chauvelin')]
         if os.path.exists(f'reference/classic/race_batch_{r[0]}_active.xlsx')]
XS = ['Venus', 'Jupiter', 'Regulus']
U = 'Uranus'
NO = ('conj', 'opposition', 'contraparallel')
SKY_Y = [b for b in B.BODIES if b != 'Moon']


def best(v, plane):
    h = [x for x in B.hits(v, plane) if x[0] not in NO]
    return h[0] if h else None


def dist(a, b, plane):
    if plane == 'Dec':
        return abs(a - b)
    d = abs(a - b) % 360
    return 360 - d if d > 180 else d


def between_ra(y, a, b):
    """y on the shorter arc from a to b."""
    d = (b - a) % 360
    if d <= 180:
        return 0 < (y - a) % 360 < d
    return 0 < (a - y) % 360 < 360 - d


def pt(pos, ra, name, plane):
    return (ra if plane == 'RA' else pos).get(name)


def runner(r, tp, tr):
    """-> list of (pair X, measure, plane, score, text)."""
    out = []
    for X in XS:
        for pl in ('RA', 'Dec'):
            sx, su = pt(tp, tr, X, pl), pt(tp, tr, U, pl)
            if sx is None or su is None:
                continue
            ds = dist(sx, su, pl)
            pair = {'S': ds}
            for ch in ('H', 'J'):
                pos, ra = r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {})
                nx, nu = pt(pos, ra, X, pl), pt(pos, ra, U, pl)
                if nx is None or nu is None:
                    continue
                d = dist(nx, nu, pl); pair[ch] = d
                h = best(d, pl)
                if h:
                    out.append((X, f'{ch} pair', pl, h[2], f'{ch} {X} – {ch} {U} {pl} {d:.4f} {B.txt(h)}'))
                for a, b, lab in ((su, nx, f'S {U} → {ch} {X}'), (sx, nu, f'S {X} → {ch} {U}')):
                    dd = dist(a, b, pl); h = best(dd, pl)
                    if h:
                        out.append((X, f'{ch} cross', pl, h[2], f'{lab} {pl} {dd:.4f} {B.txt(h)}'))
                # splits of the natal pair line by a sky body
                for Y in SKY_Y:
                    if Y in (X, U):
                        continue
                    y = pt(tp, tr, Y, pl)
                    if y is None:
                        continue
                    inside = (min(nx, nu) < y < max(nx, nu)) if pl == 'Dec' else between_ra(y, nx, nu)
                    if not inside:
                        continue
                    p1, p2 = dist(y, nx, pl), dist(y, nu, pl)
                    h1, h2 = best(p1, pl), best(p2, pl)
                    if h1 and h2:
                        out.append((X, f'{ch} split', pl, min(h1[2], h2[2]),
                                    f'{ch} {X} – {ch} {U} {pl} {d:.4f} = S {Y} → {ch} {X} {p1:.4f} {B.txt(h1)} + S {Y} → {ch} {U} '
                                    f'{p2:.4f} {B.txt(h2)}'))
            for a, b in (('H', 'S'), ('J', 'S'), ('H', 'J')):
                if a in pair and b in pair:
                    va, vb = pair[a], pair[b]
                    if va < B.CONJ[pl] or vb < B.CONJ[pl]:
                        continue
                    q = max(va, vb) / min(va, vb); h = B.ratio_hits(q)
                    if h:
                        out.append((X, f'ratio {a}/{b}', pl, h[0][2],
                                    f'{a} / {b} {X} – {U} {pl} {va:.4f} / {vb:.4f} = {q:.4f} → {h[0][0]} {h[0][1]} ({h[0][2]:.1f})'))
    return out


MEASURES = ['H pair', 'J pair', 'H cross', 'J cross', 'H split', 'J split', 'ratio H/S', 'ratio J/S', 'ratio H/J']


def main():
    data = []
    for race, win in RACES:
        runners, tt, tp = B.load(f'reference/classic/race_batch_{race}_active.xlsx')
        import openpyxl
        wb = openpyxl.load_workbook(f'reference/classic/race_batch_{race}_active.xlsx', read_only=True)
        tr = B.ra_positions(wb['TRANS_POS'])
        rows = {}
        for cloth, r in runners.items():
            name = r['name'].get('H', str(cloth))
            rows[f'{int(cloth):02d} {name}' if str(cloth).isdigit() else f'{cloth} {name}'] = runner(r, tp, tr)
        sky = {}
        for X in XS:
            for pl in ('RA', 'Dec'):
                sx, su = pt(tp, tr, X, pl), pt(tp, tr, U, pl)
                if sx is not None and su is not None:
                    d = dist(sx, su, pl); h = best(d, pl)
                    sky[(X, pl)] = (d, h)
        data.append((race, win, rows, sky))
    print(f'# Uranus pairs scan ({len(data)} result races with an _active.xlsx)\n')
    print('## Field check: runners holding the measure (best of RA / Dec) at the cut — picks / won / by chance\n')
    print('| pair | measure | >= 50 | >= 80 | >= 90 |')
    print('|---|---|---|---|---|')
    for X in XS:
        for m in MEASURES:
            cells = []
            for cut in (50, 80, 90):
                p = w = 0; c = 0.0; ws = []
                for race, win, rows, sky in data:
                    N = len(rows)
                    for run, items in rows.items():
                        if any(i[0] == X and i[1] == m and i[3] >= cut for i in items):
                            p += 1; c += 1 / N
                            if win.lower() in run.lower():
                                w += 1; ws.append(win)
                cells.append(f'{p} / {w} / {c:.1f}' + (f" ({', '.join(ws)})" if 0 < w <= 4 and cut >= 80 else ''))
            print(f'| {X} – Uranus | {m} | ' + ' | '.join(cells) + ' |')
    print('\n## Per race: sky pair lines, and the winner\'s lines (>= 50)\n')
    for race, win, rows, sky in data:
        print(f'### {race} — winner {win} ({len(rows)} runners)')
        for (X, pl), (d, h) in sky.items():
            print(f"- S {X} – S Uranus {pl} {d:.4f}" + (f' {B.txt(h)}' if h else ''))
        wr = [r for r in rows if win.lower() in r.lower()]
        for run in wr:
            for i in sorted(rows[run], key=lambda i: -i[3]):
                if i[3] >= 50:
                    print(f'  - {i[1]}: {i[4]}')
        print()


if __name__ == '__main__':
    main()
