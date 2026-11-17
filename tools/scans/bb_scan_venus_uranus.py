"""Venus – Uranus from every angle (17 Nov 2026, Eddie: 'Venus Uranus is one to look at further definitely from all different
angles'; read-only, no rule). Follows bb_scan_uranus_pairs.py (horse natal Venus – Uranus >= 90: 4 picks 3 won, 0.7 by chance).

Per race (bb_scan_uranus_pairs.RACES), per runner, chart c = H (horse) or J (jockey), planes RA (wrapped) and Dec (|dDec|), from the
_active.xlsx _POS tabs, scored with eddie_bybody.hits (its linear scoring; a 'number family' = not conj / opposition / cp):
  base   c Venus – c Uranus in a number family (its best family + target), cut 90 (also 80)
  B  carrier   base + a sky pair S A – S B (A, B sky bodies or royal stars, not the Moon, not Venus / Uranus, not the sky Rahu – Ketu)
               on the same family + target, any plane, any score
  C  sky echo  base + a sky line on Venus or Uranus (S Y – S Venus, S Y – S Uranus, Y incl. each other, not the Moon) on the same
               family + target
  D  cross     base + S Venus → c Uranus or S Uranus → c Venus on the same family + target
  E  same body base + S Venus → c Venus or S Uranus → c Uranus scoring >= 50 in a number family (any target)
  F  royal     base + a natal royal line c R – c Venus or c R – c Uranus on the same family + target
  G  split     a sky body Y (not the Moon, Venus, Uranus) between c Venus and c Uranus cutting the line into two pieces both in a
               number family >= 50 (any base score)
  M  midpoint  a sky body Y (not the Moon) at the midpoint of c Venus and c Uranus (RA within 0.5 of the nearer midpoint, Dec 0.15)
  P  parallel / contraparallel   c Venus and c Uranus within 0.3 in Dec (parallel) or |Dec V + Dec U| < 0.3 (contraparallel)
  X  across charts   H Venus – J Uranus or J Venus – H Uranus >= 90 in a number family
  K  ratio     c V – U / S V – U (same plane, larger / smaller) on an interval / cut >= 80 (eddie_bybody.ratio_hits)
Field check per chart at each cut: picks / won / by chance (sum of 1 / field size); runner-level."""
import os, sys, openpyxl
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody as B
from bb_scan_uranus_pairs import RACES, dist, between_ra

NO = ('conj', 'opposition', 'contraparallel')
V, U = 'Venus', 'Uranus'
SKYP = [b for b in B.BODIES if b != 'Moon'] + B.ROYAL


def nums(v, pl):
    return [x for x in B.hits(v, pl) if x[0] not in NO]


def best(v, pl):
    h = nums(v, pl)
    return h[0] if h else None


def P(pos, ra, n, pl):
    return (ra if pl == 'RA' else pos).get(n)


def items(r, tp, tr):
    out = []   # (key, chart, score, text)
    for ch in ('H', 'J'):
        pos, ra = r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {})
        if not pos:
            continue
        for pl in ('RA', 'Dec'):
            nv, nu = P(pos, ra, V, pl), P(pos, ra, U, pl)
            sv, su = P(tp, tr, V, pl), P(tp, tr, U, pl)
            if None in (nv, nu, sv, su):
                continue
            d = dist(nv, nu, pl)
            line = f'{ch} Venus – {ch} Uranus {pl} {d:.4f}'
            bh = best(d, pl)
            if bh:
                key = (bh[0], bh[1])
                out.append(('base', ch, bh[2], f'{line} {B.txt(bh)}'))
                same = lambda vv, pp: any((x[0], x[1]) == key for x in nums(vv, pp))
                for i, a in enumerate(SKYP):
                    for b in SKYP[i + 1:]:
                        if {a, b} & {V, U} or {a, b} == {'Rahu', 'Ketu'}:
                            continue
                        for p2 in ('RA', 'Dec'):
                            pa, pb = P(tp, tr, a, p2), P(tp, tr, b, p2)
                            if pa is not None and pb is not None and same(dist(pa, pb, p2), p2):
                                out.append(('B', ch, bh[2], f'{line} {B.txt(bh)} carried by S {a} – S {b} {p2} {dist(pa, pb, p2):.4f}'))
                for Y in [b for b in SKYP if b not in (V,)]:
                    for X in (V, U):
                        if Y == X:
                            continue
                        for p2 in ('RA', 'Dec'):
                            py, px = P(tp, tr, Y, p2), P(tp, tr, X, p2)
                            if py is not None and px is not None and same(dist(py, px, p2), p2):
                                out.append(('C', ch, bh[2], f'{line} {B.txt(bh)} = S {Y} – S {X} {p2} {dist(py, px, p2):.4f}'))
                for p2 in ('RA', 'Dec'):
                    for a, b, lab in ((V, U, f'S Venus → {ch} Uranus'), (U, V, f'S Uranus → {ch} Venus')):
                        sa, nb = P(tp, tr, a, p2), P(pos, ra, b, p2)
                        if sa is not None and nb is not None and same(dist(sa, nb, p2), p2):
                            out.append(('D', ch, bh[2], f'{line} {B.txt(bh)} = {lab} {p2} {dist(sa, nb, p2):.4f}'))
                    for R in B.ROYAL:
                        for X in (V, U):
                            pr, px = P(pos, ra, R, p2), P(pos, ra, X, p2)
                            if pr is not None and px is not None and same(dist(pr, px, p2), p2):
                                out.append(('F', ch, bh[2], f'{line} {B.txt(bh)} = {ch} {R} – {ch} {X} {p2} {dist(pr, px, p2):.4f}'))
                for X in (V, U):
                    for p2 in ('RA', 'Dec'):
                        a, b = P(tp, tr, X, p2), P(pos, ra, X, p2)
                        if a is not None and b is not None:
                            h = best(dist(a, b, p2), p2)
                            if h and h[2] >= 50:
                                out.append(('E', ch, bh[2], f'{line} {B.txt(bh)}; S {X} → {ch} {X} {p2} {dist(a, b, p2):.4f} {B.txt(h)}'))
                if d >= B.CONJ[pl] and dist(sv, su, pl) >= B.CONJ[pl]:
                    sd = dist(sv, su, pl); q = max(d, sd) / min(d, sd); rh = B.ratio_hits(q)
                    if rh and rh[0][2] >= 80:
                        out.append(('K', ch, rh[0][2], f'{line} / S Venus – S Uranus {sd:.4f} = {q:.4f} → {rh[0][0]} ({rh[0][2]:.1f})'))
            # split and midpoint (any base)
            for Y in [b for b in B.BODIES if b not in ('Moon', V, U)]:
                y = P(tp, tr, Y, pl)
                if y is None:
                    continue
                inside = (min(nv, nu) < y < max(nv, nu)) if pl == 'Dec' else between_ra(y, nv, nu)
                if inside:
                    p1, p2_ = dist(y, nv, pl), dist(y, nu, pl)
                    h1, h2 = best(p1, pl), best(p2_, pl)
                    if h1 and h2 and min(h1[2], h2[2]) >= 50:
                        out.append(('G', ch, min(h1[2], h2[2]), f'{line} = S {Y} → {ch} Venus {p1:.4f} {B.txt(h1)} + S {Y} → {ch} Uranus {p2_:.4f} {B.txt(h2)}'))
                if pl == 'Dec':
                    off = abs(y - (nv + nu) / 2); tol = 0.15
                else:
                    m1 = ((nv + ((nu - nv + 180) % 360 - 180) / 2)) % 360
                    off = min(dist(y, m1, 'RA'), dist(y, (m1 + 180) % 360, 'RA')); tol = 0.5
                if off < tol and d >= B.CONJ[pl]:
                    out.append(('M', ch, 100 * (tol - off) / tol, f'S {Y} at the midpoint of {ch} Venus and {ch} Uranus {pl} (offset {off:.4f}, line {d:.4f})'))
        dv, du = pos.get(V), pos.get(U)
        if dv is not None and du is not None:
            if abs(dv - du) < 0.3:
                out.append(('P', ch, 100 * (0.3 - abs(dv - du)) / 0.3, f'{ch} Venus parallel {ch} Uranus Dec {abs(dv - du):.4f}'))
            if abs(dv + du) < 0.3:
                out.append(('P', ch, 100 * (0.3 - abs(dv + du)) / 0.3, f'{ch} Venus contraparallel {ch} Uranus {abs(dv + du):.4f}'))
    for a, b in (('H', 'J'), ('J', 'H')):
        pa, pb = r['pos'].get(a, {}), r['pos'].get(b, {})
        ra_, rb = r.get('ra', {}).get(a, {}), r.get('ra', {}).get(b, {})
        for pl in ('RA', 'Dec'):
            x, y = P(pa, ra_, V, pl), P(pb, rb, U, pl)
            if x is not None and y is not None:
                h = best(dist(x, y, pl), pl)
                if h and h[2] >= 90:
                    out.append(('X', 'HJ', h[2], f'{a} Venus – {b} Uranus {pl} {dist(x, y, pl):.4f} {B.txt(h)}'))
    return out


KEYS = [('base', 90), ('base', 80), ('B', 90), ('C', 90), ('D', 90), ('E', 90), ('F', 90), ('B', 80), ('C', 80), ('D', 80),
        ('E', 80), ('F', 80), ('G', 50), ('G', 80), ('M', 0), ('M', 50), ('P', 0), ('X', 90), ('K', 80)]
DESC = {'base': 'natal Venus – Uranus', 'B': 'base + sky pair carrier', 'C': 'base + sky line on Venus / Uranus same number',
        'D': 'base + cross line same number', 'E': 'base + same-body line >= 50', 'F': 'base + royal line same number',
        'G': 'split by a sky body (pieces >= cut)', 'M': 'sky body at the midpoint (score >= cut)', 'P': 'parallel / contraparallel',
        'X': 'H Venus – J Uranus / J Venus – H Uranus >= 90', 'K': 'ratio natal / sky Venus – Uranus >= 80'}


def main():
    data = []
    for race, win in RACES:
        path = f'reference/classic/race_batch_{race}_active.xlsx'
        runners, tt, tp = B.load(path)
        tr = B.ra_positions(openpyxl.load_workbook(path, read_only=True)['TRANS_POS'])
        rows = {f"{c} {r['name'].get('H', '')}": items(r, tp, tr) for c, r in runners.items()}
        data.append((race, win, rows))
    print(f'# Venus – Uranus from every angle ({len(data)} result races)\n')
    print('Base cut: the natal line\'s own score (B-F need the base at the cut). picks / won / by chance; winners named when 1-5.\n')
    print('| measure | cut | horse (H) | jockey (J) |')
    print('|---|---|---|---|')
    for k, cut in KEYS:
        cells = []
        for ch in (('H',), ('J',)) if k != 'X' else (('HJ',), ('-',)):
            p = w = 0; c = 0.0; ws = []
            for race, win, rows in data:
                N = len(rows)
                for run, it in rows.items():
                    if any(i[0] == k and i[1] in ch and i[2] >= cut for i in it):
                        p += 1; c += 1 / N
                        if win.lower() in run.lower():
                            w += 1; ws.append(win)
            cells.append(f'{p} / {w} / {c:.1f}' + (f" ({', '.join(ws)})" if 0 < w <= 5 else ''))
        print(f'| {DESC[k]} | {cut} | ' + ' | '.join(cells) + ' |')
    print('\n## Every runner with horse Venus – Uranus >= 80 (all its items)\n')
    for race, win, rows in data:
        for run, it in rows.items():
            if any(i[0] == 'base' and i[1] == 'H' and i[2] >= 80 for i in it):
                tag = 'WON' if win.lower() in run.lower() else 'lost'
                print(f'### {race} {run} — {tag}')
                for i in it:
                    if i[1] in ('H', 'HJ') and (i[0] != 'base' or i[2] >= 80):
                        print(f'- [{i[0]}] {i[3]}')
                print()
    print('## The winners\' Venus – Uranus items (any score)\n')
    for race, win, rows in data:
        for run, it in rows.items():
            if win.lower() in run.lower() and it:
                print(f'### {race} {run}')
                for i in it:
                    print(f'- [{i[0]} {i[1]}] {i[3]}')
                print()


if __name__ == '__main__':
    main()
