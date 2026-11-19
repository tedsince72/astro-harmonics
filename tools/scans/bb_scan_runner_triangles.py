"""Do the winners carry the sky triangle structure? (19 Nov 2026, Eddie: 'ok and do we find the same structure connects with the winner';
read-only). Lines in a number family (whole, golden, phi power, ninth, sqrt2, silver; no conj / cp / opposition) scoring >= cut;
bodies only (Moon in the sky only, Ketu left out). Triangles must close ACROSS planes (a triangle closed in one plane is forced by
geometry; see bb_scan_sky_triangles.py). Per runner, horse and jockey charts summed:
  SN   sky-natal triangle: sky pair S A - S B, S A -> c X and S B -> c X (c = H or J, X a natal body, A or B may equal X);
  SNf  the same with A or B a fast body (Sun, Moon, Mercury, Venus, Mars);
  SNw  SNf with a whole side and a phi-family side (golden or phi power) among the three;
  ON   'on the sky triangles': lines S A -> c X >= cut where A is a corner of one of the race's sky fast triangles (across planes);
  NN   natal triangle in one chart: c X - c Y, c Y - c Z, c X - c Z, across planes.
Winner against its field (top / bottom, ties counted, chance = share tied), favourites, and split by cover hit / miss races.
Chosen after the results.
  python3 tools/scans/bb_scan_runner_triangles.py [cut]   (default 50)"""
import sys, os, itertools, io, contextlib
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 50
sys.argv = sys.argv[:1]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_regulus_apex as RA
    import bb_scan_sky_triangles as T
FAST, NUMF = T.FAST, T.NUMF
SKY = [b for b in EB.BODIES if b != 'Ketu']
NAT = [b for b in EB.NATAL_BODIES if b != 'Ketu']
PHIF = {'golden', 'phi power'}


def fam(v, pl):
    if v is None:
        return None
    h = [(f, s) for f, l, s in EB.hits(v, pl) if f in NUMF and s >= CUT]
    return max(h, key=lambda x: x[1])[0] if h else None


def closes(sides):
    """sides: list of {plane: family}; -> list of families of one across-plane closing, or None."""
    if not all(sides):
        return None
    if any(all(pl in s for s in sides) for pl in ('RA', 'Dec')):
        return None
    return [next(iter(s.values())) if len(s) == 1 else s['RA'] for s in sides]


def edges(d, kind, A, B, same=False):
    E = {}
    for pl in ('RA', 'Dec'):
        it = itertools.combinations(A, 2) if same else itertools.product(A, B)
        for a, b in it:
            v = EB.pair(d, kind, pl, a, b) if kind != 'SN' else d.get(('S', pl, a, b))
            f = fam(v, pl)
            if f:
                E.setdefault((a, b) if not same else frozenset((a, b)), {})[pl] = f
    return E


def sky_fast_corners(tt):
    E = edges(tt, 'S', SKY, None, same=True)
    corners = set()
    for a, b, c in itertools.combinations(SKY, 3):
        if not any(x in FAST for x in (a, b, c)):
            continue
        if closes([E.get(frozenset(p), {}) for p in ((a, b), (b, c), (a, c))]):
            corners |= {a, b, c}
    return E, corners


def runner_counts(r, SE, corners):
    c = dict(SN=0, SNf=0, SNw=0, ON=0, NN=0)
    for ch in ('H', 'J'):
        d = r['dist'].get(ch)
        if not d:
            continue
        SX = edges(d, 'SN', SKY, NAT)                    # (A, X) -> {pl: fam}
        c['ON'] += sum(len(v) for (a, x), v in SX.items() if a in corners)
        for X in NAT:
            on = [a for a in SKY if (a, X) in SX]
            for a, b in itertools.combinations(on, 2):
                fs = closes([SE.get(frozenset((a, b)), {}), SX[(a, X)], SX[(b, X)]])
                if fs:
                    c['SN'] += 1
                    if a in FAST or b in FAST:
                        c['SNf'] += 1
                        if 'whole' in fs and PHIF & set(fs):
                            c['SNw'] += 1
        NE = edges(d, 'N', NAT, None, same=True)
        for x, y, z in itertools.combinations(NAT, 3):
            if closes([NE.get(frozenset(p), {}) for p in ((x, y), (y, z), (x, z))]):
                c['NN'] += 1
    return c


def main():
    rows = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        SE, corners = sky_fast_corners(tt)
        cnt = {RA.key(r['name'].get('H') or ''): runner_counts(r, SE, corners) for r in runners.values()}
        fav = F.FAV.get(race)
        rows.append(dict(race=race, win=RA.key(win), fav=RA.key(fav) if fav else None, cover=T.cover_of(race, win), cnt=cnt))
    keys = [('SN', 'sky pair + both ends on natal X (across planes)'), ('SNf', '... with a fast sky body'),
            ('SNw', '... fast, with a whole side and a phi-family side'), ('ON', 'lines from the sky fast-triangle corners'),
            ('NN', 'natal triangle in one chart (across planes)')]
    print(f'# Does the winner carry the triangle structure? cut {CUT:g}\n')
    print(f'{len(rows)} result races; chosen after the results. Top / bottom = most / fewest in the field, ties counted; chance = share '
          'of the field tied there.\n')

    def table(sel_race, who, title):
        print(f'## {title}\n')
        print('| count | mean (who) | mean (others) | top | chance | bottom | chance | holds >= 1 | chance |\n|---|---|---|---|---|---|---|---|---|')
        for k, lab in keys:
            wm, om, top, ct, bot, cb, hold, ch, n = [], [], 0, 0.0, 0, 0.0, 0, 0.0, 0
            for r in rows:
                if not sel_race(r):
                    continue
                w = who(r)
                if not w or w not in r['cnt']:
                    continue
                vals = {x: v[k] for x, v in r['cnt'].items()}
                n += 1
                wv, mx, mn, kk = vals[w], max(vals.values()), min(vals.values()), len(vals)
                wm.append(wv); om += [v for x, v in vals.items() if x != w]
                top += wv == mx and mx > mn; ct += sum(v == mx for v in vals.values()) / kk if mx > mn else 0
                bot += wv == mn and mx > mn; cb += sum(v == mn for v in vals.values()) / kk if mx > mn else 0
                hold += wv > 0; ch += sum(v > 0 for v in vals.values()) / kk
            if n:
                print(f'| {lab} | {sum(wm) / n:.2f} | {sum(om) / max(1, len(om)):.2f} | {top} / {n} | {ct:.1f} | {bot} / {n} | {cb:.1f} | '
                      f'{hold} / {n} | {ch:.1f} |')
        print()
    table(lambda r: True, lambda r: r['win'], 'Winner, all races')
    table(lambda r: r['cover'] is True, lambda r: r['win'], 'Winner, cover-hit races')
    table(lambda r: r['cover'] is False, lambda r: r['win'], 'Winner, cover-miss races')
    table(lambda r: r['fav'] and r['fav'] == r['win'], lambda r: r['fav'], 'Favourite, races the favourite won')
    table(lambda r: r['fav'] and r['fav'] != r['win'], lambda r: r['fav'], 'Favourite, races the favourite lost')
    print('(Top / bottom count only races where the field is not all level.)')


if __name__ == '__main__':
    main()
