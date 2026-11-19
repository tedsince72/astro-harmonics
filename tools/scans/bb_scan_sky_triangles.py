"""Sky structure: closed triangles (19 Nov 2026, Eddie: 'yes, lets look at that next / I agree that structure and closed triangles
etc... especially with the faster bodies involved'; read-only).
Sky lines S A - S B at the off, bodies only (Moon incl.; Ketu left out, it mirrors Rahu), RA or Dec, in a number family (eddie_bybody
families: whole, golden, phi power, ninth, sqrt2, silver; no conj / cp / opposition) scoring >= cut. A triangle = three bodies A, B, C
with all three sides scoring in the same plane; 'across planes' = all three sides score but only with RA and Dec sides mixed
(not forced by geometry). Hubs: lines ending on each fast body.
Geometry: in Dec (and in RA up to the wrap) one side is always the sum or difference of the other two, so two sides on targets force
the third onto target sum / difference (whole + whole -> whole, k x phi + m x phi -> golden). Such a triangle is 'additive' (may be
geometry); 'independent' = no choice of the three sides' targets has t3 = t1 + t2, |t1 - t2| or 360 - (t1 + t2) (RA).
Fast bodies: Sun, Moon, Mercury, Venus, Mars. Per race: triangles all / independent, with >= 1 and >= 2 fast bodies; by fast body.
Groups: cover hit / miss (cover of eight from the rule files), favourite won / lost (bb_favs_outer_uranus.FAV). Chosen after the results.
  python3 tools/scans/bb_scan_sky_triangles.py [cut] [--race R ...]"""
import sys, os, json, itertools, io, contextlib
ARGS = sys.argv[1:]
EXTRA = ARGS[ARGS.index('--race') + 1:] if '--race' in ARGS else []
ARGS = ARGS[:ARGS.index('--race')] if '--race' in ARGS else ARGS
CUT = float(ARGS[0]) if ARGS else 80
sys.argv = sys.argv[:1]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_regulus_apex as RA
TV = {(f, l): t for f, l, t, _tol in EB.TARGETS}
FAST = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars']
PTS = [b for b in EB.BODIES if b != 'Ketu']
NUMF = {'whole', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver'}


def edge(tt, pl, a, b):
    v = EB.pair(tt, 'S', pl, a, b)
    if v is None:
        return None
    h = [TV[(f, l)] for f, l, s in EB.hits(v, pl) if f in NUMF and s >= CUT]
    return h or None


def additive(t1s, t2s, t3s, pl):
    for t1, t2, t3 in itertools.product(t1s, t2s, t3s):
        cands = [t1 + t2, abs(t1 - t2)] + ([360 - (t1 + t2)] if pl == 'RA' else [])
        if any(abs(t3 - c) < 1e-3 for c in cands):
            return True
    return False


def triangles(tt):
    out, E = [], {}
    for pl in ('RA', 'Dec'):
        for a, b in itertools.combinations(PTS, 2):
            h = edge(tt, pl, a, b)
            if h:
                E[(frozenset((a, b)), pl)] = h
    for a, b, c in itertools.combinations(PTS, 3):
        sides = [frozenset((a, b)), frozenset((b, c)), frozenset((a, c))]
        for pl in ('RA', 'Dec'):
            ab, bc, ac = (E.get((x, pl)) for x in sides)
            if ab and bc and ac:
                add = additive(ab, bc, ac, pl) or additive(ab, ac, bc, pl) or additive(bc, ac, ab, pl)
                out.append(dict(pts=(a, b, c), pl=pl, add=add, fast=sum(x in FAST for x in (a, b, c))))
        pls = [[pl for pl in ('RA', 'Dec') if (x, pl) in E] for x in sides]
        if all(pls) and not any(all(pl in q for q in pls) for pl in ('RA', 'Dec')):
            # closed only across planes (no single plane closes it): not forced by geometry
            out.append(dict(pts=(a, b, c), pl='mixed', add=False, fast=sum(x in FAST for x in (a, b, c))))
    deg = {b: sum(b in k for k, _pl in E) for b in PTS}
    return out, deg


def cover_of(race, win):
    rf = f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
    if not os.path.exists(rf) or win is None:
        return None
    J = json.load(open(rf))
    held = {r: set() for r in J['runners']}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                held.setdefault(c['runner'], set()).add(rid)
    picks = {RA.key(r) for r in J['runners'] if any(set(c) <= held[r] for c in RA.C8)}
    return RA.key(win) in picks if picks else None


def summary(trd):
    tr, deg = trd
    ind = [t for t in tr if not t['add']]
    d = dict(all=len(tr), add=len(tr) - len(ind), ind=len(ind), ind_f1=sum(t['fast'] >= 1 for t in ind),
             ind_f2=sum(t['fast'] >= 2 for t in ind), all_f1=sum(t['fast'] >= 1 for t in tr), all_f2=sum(t['fast'] >= 2 for t in tr))
    d['mixed'] = sum(t['pl'] == 'mixed' for t in tr)
    d['mixed_f1'] = sum(t['pl'] == 'mixed' and t['fast'] >= 1 for t in tr)
    d['mixed_f2'] = sum(t['pl'] == 'mixed' and t['fast'] >= 2 for t in tr)
    for b in FAST:
        d['ind ' + b] = sum(b in t['pts'] for t in ind)
    d['fast lines'] = sum(deg[b] for b in FAST)
    d['all lines'] = sum(deg.values()) // 2
    d['top fast hub'] = max(deg[b] for b in FAST)
    return d


def main():
    rows = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        trd = triangles(tt); tr = trd[0]
        fav = F.FAV.get(race)
        rows.append(dict(race=race, cover=cover_of(race, win), favwon=(RA.key(fav) == RA.key(win)) if fav else None,
                         s=summary(trd), tr=tr))
    keys = ['all lines', 'fast lines', 'top fast hub', 'all', 'add', 'ind', 'mixed', 'mixed_f1', 'mixed_f2', 'ind_f1', 'ind_f2'] + ['ind ' + b for b in FAST]
    lab = {'all': 'all triangles', 'add': 'additive (may be geometry)', 'ind': 'independent', 'all_f1': 'all, >= 1 fast',
           'all_f2': 'all, >= 2 fast', 'ind_f1': 'independent, >= 1 fast', 'ind_f2': 'independent, >= 2 fast', 'mixed': 'closed only across planes', 'mixed_f1': 'across planes, >= 1 fast', 'mixed_f2': 'across planes, >= 2 fast', 'all lines': 'sky lines', 'fast lines': 'line ends on a fast body', 'top fast hub': 'most lines on one fast body'}
    print(f'# Sky closed triangles, cut {CUT:g} ({len(rows)} result races with an _active.xlsx; chosen after the results)\n')
    print('Fast bodies: Sun, Moon, Mercury, Venus, Mars. Mean per race; in brackets the share of races with at least one.\n')
    G = [('all', lambda r: True), ('cover hit', lambda r: r['cover'] is True), ('cover miss', lambda r: r['cover'] is False),
         ('fav won', lambda r: r['favwon'] is True), ('fav lost', lambda r: r['favwon'] is False)]
    print('| count | ' + ' | '.join(f'{g} ({sum(map(f, rows))})' for g, f in G) + ' |\n|---|' + '---|' * len(G))
    for k in keys:
        cells = []
        for g, f in G:
            xs = [r['s'][k] for r in rows if f(r)]
            cells.append(f'{sum(xs) / len(xs):.2f} ({sum(x > 0 for x in xs) / len(xs):.0%})' if xs else '-')
        print(f'| {lab.get(k, k)} | ' + ' | '.join(cells) + ' |')
    for k in ('ind', 'mixed', 'mixed_f1', 'mixed_f2', 'top fast hub'):
        print(f'\n## Races by {lab[k]} count\n')
        print('| count | races | cover hit | cover miss | miss rate | fav won | fav lost |\n|---|---|---|---|---|---|---|')
        mx = max(r['s'][k] for r in rows)
        bands = [(0, 0), (1, 1), (2, 2), (3, 4), (5, 7), (8, 10 ** 6)]
        for lo, hi in bands:
            sel = [r for r in rows if lo <= r['s'][k] <= hi]
            if not sel or lo > mx:
                continue
            h = sum(r['cover'] is True for r in sel); m = sum(r['cover'] is False for r in sel)
            w = sum(r['favwon'] is True for r in sel); l = sum(r['favwon'] is False for r in sel)
            band = f'{lo}' if lo == hi else (f'{lo}+' if hi > 10 ** 5 else f'{lo}-{hi}')
            print(f'| {band} | {len(sel)} | {h} | {m} | {m / (h + m):.2f} | {w} | {l} |' if h + m else
                  f'| {band} | {len(sel)} | {h} | {m} | - | {w} | {l} |')
    print('\n## Per race\n')
    print('| race | cover | fav won | all | independent | ind >= 1 fast | ind >= 2 fast | independent / across-plane triangles with >= 2 fast |\n'
          '|---|---|---|---|---|---|---|---|')
    for r in rows:
        ft = '; '.join(f"{'-'.join(t['pts'])} {t['pl']}" for t in r['tr'] if not t['add'] and t['fast'] >= 2)
        c = '-' if r['cover'] is None else 'hit' if r['cover'] else 'miss'
        fw = '-' if r['favwon'] is None else 'yes' if r['favwon'] else 'no'
        s = r['s']
        print(f"| {r['race']} | {c} | {fw} | {s['all']} | {s['ind']} | {s['ind_f1']} | {s['ind_f2']} | {ft} |")
    for race in EXTRA:
        runners, tt, tp = EB.load(f'reference/classic/race_batch_{race}_active.xlsx')
        trd = triangles(tt); tr = trd[0]; s = summary(trd)
        ft = '; '.join(f"{'-'.join(t['pts'])} {t['pl']}" for t in tr if not t['add'] and t['fast'] >= 2)
        print(f"\n{race}: " + ', '.join(f"{lab.get(k, k)} {s[k]}" for k in keys[:11]) + f" | >= 2 fast: {ft}")


if __name__ == '__main__':
    main()
