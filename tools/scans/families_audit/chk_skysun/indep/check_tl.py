#!/usr/bin/env python3
"""check_tl.py <workbook> [sheet ...]: TIMELINE / LONG TIMELINE / STAR TIMELINE / LONG STAR TIMELINE of each SKY <centre> sheet
rebuilt from POSITIONS (own events, linear off -> +5 timing) and compared with the sheet. Real engine times (beyond 60 min) and
95 / 100 / 95 cells are checked separately (check_engine.py)."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *  # noqa
import check_blocks as CB

AREA_NAME = {'A': 'area A', 'P': 'area φ and √2', 'B': 'area B'}
SRC_ORDER = ['SKY', 'SKY EQ', 'SKY PAIRS', 'SKY STARS', 'SKY ROYAL']
WINDOW = {'Jupiter': (-30, 60), 'Sun': (-30, 60), 'Moon': (-5, 20)}


def pk(pos, a, b, plane):
    if plane == 'Equator' and b != 'equator' and (pos.p[a][1] >= 0) == (pos.p[b][1] >= 0):
        return 'Dec'
    return plane


def ev_dist(pos, src, c, x, plane, v0, v5, b, score, rel=None):
    t = exact_t(v0, v5, b['tv'])
    if t is None: return None
    pts = frozenset([c, x])
    return {'src': src, 'rel': rel or f'S {c} → S {x}', 'plane': plane, 'kind': 'distance',
            'target': f"{b['target']} ({FAMTXT[b['family']]})", 'tv': b['tv'], 'v0': v0, 'score': score, 't': t,
            'key': ('d', pts, pk(pos, c, x, plane), b['family'], b['target']), 'pts': pts, 'centred': c}


def events(pos, B, sheet_pairs):
    c = B['centre']; out = []
    for x, cells in B['sky']:
        for pl in ('RA', 'Dec'):
            d = cells[pl]
            if d is None or d['b'] is None: continue
            e = ev_dist(pos, 'SKY', c, x, pl, d['v0'], d['v5'], d['b'], d['score'])
            if e: out.append(e)
    for r in B['eq']:
        if r['eqtog']: continue
        if r['ut'] is None: continue
        out.append({'src': 'SKY EQ', 'rel': f"S {c}: S {r['x']} = S {r['y']}", 'plane': r['plane'], 'kind': 'midpoint (equidistance)',
                    'target': '1 · unison · midpoint (area A)', 'tv': 1.0, 'v0': r['q0'], 'score': r['eqmid']['total'], 't': r['ut'],
                    'key': ('r', frozenset([r['x'], r['y']]), r['plane'], '1'), 'pts': frozenset([c, r['x'], r['y']]), 'centred': c,
                    'ratio': True})
    for src in ('SKY PAIRS', 'SKY STARS', 'SKY ROYAL'):
        for r in sheet_pairs[src]:
            if r['together']: continue
            x, y, pl = r['x'], r['y'], r['plane']
            rb = r['rb']
            if r['rt'] is not None:
                lab = rb['target']
                out.append({'src': src, 'rel': f'S {c}: S {x} – S {y}', 'plane': pl, 'kind': 'ratio',
                            'target': f"{lab} · {rb['name']} · {rb['group']} ({AREA_NAME[F.area(lab)]})", 'tv': rb['tv'],
                            'v0': r['q0'], 'score': r['rscore'], 't': r['rt'], 'key': ('r', frozenset([x, y]), pl, lab),
                            'pts': frozenset([c, x, y]), 'centred': c, 'ratio': True})
            if r['mid']['hit'] and r['ut'] is not None:
                out.append({'src': src, 'rel': f'S {c}: S {x} – S {y}', 'plane': pl, 'kind': 'midpoint',
                            'target': '1 · unison · midpoint (area A)', 'tv': 1.0, 'v0': r['q0'], 'score': r['mid']['total'],
                            't': r['ut'], 'key': ('r', frozenset([x, y]), pl, '1'), 'pts': frozenset([c, x, y]), 'centred': c,
                            'ratio': True})
            for (a, b_), L in zip(((c, x), (c, y), (x, y)), r['L']):
                if L['b'] is None: continue
                rel = f'S {a} → S {b_}' if a == c else f'S {a} – S {b_}'
                e = ev_dist(pos, src, a, b_, pl, L['v0'], L['v5'], L['b'], L['b']['score'], rel)
                if e:
                    e['centred'] = c if a == c else None
                    out.append(e)
    return out


def dedupe(evs):
    first = {}; order = []
    for e in evs:
        k = e['key']
        if k not in first:
            first[k] = dict(e, also=[]); order.append(k)
        else:
            f = first[k]
            if e['src'] != f['src'] and e['src'] not in f['also']:
                f['also'].append(e['src'])
    return [first[k] for k in order]


def note(e):
    parts = []
    if e['score'] is None: parts.append('outside at the off')
    if e['also']: parts.append('also ' + ', '.join(e['also']))
    return '; '.join(parts) or None


def sheet_pair_rows(B):
    s = {'SKY PAIRS': B['pairs'], 'SKY STARS': B['stars'], 'SKY ROYAL': B['royal']}
    return s


def star_event(e, pos, c):
    if e.get('centred') != c: return False
    others = [p for p in e['pts'] if p != c]
    return bool(others) and all(pos.p.get(p, (0, 0, 0, 0, ''))[4] == 'star' for p in others)


def read_tl(ws, name):
    rows = []
    for r in range(1, ws.max_row + 1):
        if ws.cell(r, 1).value == name:
            rows.append([ws.cell(r, cc).value for cc in range(1, 20)])
    return rows


def cmp_row(g, e, pos, long=False):
    errs = []
    exp = [clock(pos, e['t']), e['src'], e['rel'], e['plane'], e['kind'], e['target'], e['tv'], round(e['v0'], 6),
           None if e['score'] is None else round(e['score'], 2), 'applying' if e['t'] > 0 else 'separating', note(e)]
    got = [g[1], g[3], g[4], g[5], g[6], g[7], g[8], g[9], g[10], g[11], g[12]]
    for i, (a, b) in enumerate(zip(got, exp)):
        if i in (6, 7):
            if not CB.close(CB.num(a), b, 2e-6): errs.append((i, a, b))
        elif i == 8:
            if not CB.close(CB.num(a), b, 0.006): errs.append((i, a, b))
        elif (a or None) != (b or None):
            errs.append((i, a, b))
    if not long:
        if not CB.close(CB.num(g[2]), round(e['t'], 1), 0.051): errs.append(('min', g[2], round(e['t'], 1)))
    return errs


def check(ws, pos, B):
    c = B['centre']; errs = []; counts = {}
    evs = events(pos, B, sheet_pair_rows(B))
    lo, hi = WINDOW[c]
    D = dedupe(evs)
    tl = sorted([e for e in D if lo <= e['t'] <= hi], key=lambda e: e['t'])
    near = sorted([e for e in D if (lo - 3 <= e['t'] < lo) or (hi < e['t'] <= hi + 3)], key=lambda e: e['t'])
    for name, exp in (('TIMELINE', tl), ('STAR TIMELINE', [e for e in tl if star_event(e, pos, c)])):
        got = [g for g in read_tl(ws, name) if not (isinstance(g[3], str) and g[3].startswith('———'))]
        marks = [g for g in read_tl(ws, name) if isinstance(g[3], str) and g[3].startswith('———')]
        if c == 'Moon' and name != 'TIMELINE':
            if got or marks: errs.append((name, 'present on SKY MOON'))
            continue
        counts[name] = (len(got), len(exp))
        gk = [(g[4], g[5], g[7]) for g in got]
        ek = [(e['rel'], e['plane'], e['target']) for e in exp]
        if sorted(gk, key=str) != sorted(ek, key=str):
            for k in set(gk) - set(ek): errs.append((name, 'extra', k))
            for k in set(ek) - set(gk): errs.append((name, 'missing', k, [round(e['t'], 2) for e in exp if (e['rel'], e['plane'], e['target']) == k]))
        em = {k: e for k, e in zip(ek, exp)}
        for g, k in zip(got, gk):
            if k in em:
                for x in cmp_row(g, em[k], pos): errs.append((name, k, x))
            mm = CB.num(g[2])
            if mm is not None and not (lo <= mm <= hi): errs.append((name, 'outside window', k, mm))
        # order: by the minutes column, markers at 0 and 5
        allr = read_tl(ws, name)
        mins = [CB.num(g[2]) for g in allr]
        if any(a > b for a, b in zip(mins, mins[1:])): errs.append((name, 'not in time order'))
        if [g[3] for g in marks] != ['——— OFF ———', '——— OFF + 5 MIN ———']: errs.append((name, 'markers', [g[3] for g in marks]))
    # LONG (filter >= 90, then dedupe)
    if c != 'Moon':
        DL = dedupe([e for e in evs if e['score'] is not None and e['score'] >= 90])
        for name, exp in (('LONG TIMELINE', DL), ('LONG STAR TIMELINE', [e for e in DL if star_event(e, pos, c)])):
            got = [g for g in read_tl(ws, name) if not (isinstance(g[3], str) and g[3].startswith('———'))]
            counts[name] = (len(got), len(exp))
            gk = [(g[4], g[5], g[7]) for g in got]; ek = [(e['rel'], e['plane'], e['target']) for e in exp]
            for k in set(gk) - set(ek): errs.append((name, 'extra', k))
            for k in set(ek) - set(gk): errs.append((name, 'missing', k))
            em = {k: e for k, e in zip(ek, exp)}
            sec = None
            for g in read_tl(ws, name):
                if isinstance(g[3], str) and g[3].startswith('———'):
                    sec = 'sep' if 'SEPARATING' in g[3] else 'app'; continue
                k = (g[4], g[5], g[7]); e = em.get(k)
                if not e: continue
                if abs(e['t']) <= 60:
                    for x in cmp_row(g, e, pos, long=True): errs.append((name, k, x))
                    if not CB.close(CB.num(g[13]), round(e['t'], 1), 0.051): errs.append((name, k, 'min', g[13], e['t']))
                else:
                    x = [y for y in cmp_row(g, e, pos, long=True) if y[0] not in (0, 9)]
                    for y in x: errs.append((name, k, y))
                    e['real'] = CB.num(g[13])
                lin = f"{clock(pos, e['t'])} ({e['t']:+.1f} min)" if abs(e['t']) < 1440 else None
                if lin and g[14] != lin and abs(e['t']) < 1440: errs.append((name, k, 'linear', g[14], lin))
                if (sec == 'app') != (g[11] == 'applying'): errs.append((name, k, 'section', sec, g[11]))
            # order inside sections: score desc
            for s in ('SEPARATING', 'APPLYING'):
                pass
            ok_order(read_tl(ws, name), em, errs, name)
    return counts, errs, tl, near, evs


def ok_order(rows, em, errs, name):
    sec = []; cur = None
    for g in rows:
        if isinstance(g[3], str) and g[3].startswith('———'):
            cur = []; sec.append(cur); continue
        e = em.get((g[4], g[5], g[7]))
        if e and cur is not None: cur.append((e['score'], CB.num(g[13]), g))
    for i, s in enumerate(sec):
        for a, b in zip(s, s[1:]):
            if a[0] < b[0] - 1e-9: errs.append((name, 'score order', a[2][4], b[2][4]))
            elif abs(a[0] - b[0]) < 1e-9:
                if i == 0 and a[1] < b[1]: errs.append((name, 'tie order', a[2][4]))
                if i == 1 and a[1] > b[1]: errs.append((name, 'tie order', a[2][4]))


if __name__ == '__main__':
    wb, pos, res = CB.run(sys.argv[1], sys.argv[2:])
    for sn, (B, _) in res.items():
        counts, errs, tl, near, evs = check(wb[sn], pos, B)
        print(sn, counts, 'errors', len(errs))
        for e in errs[:30]: print('   ', e)
        lo, hi = WINDOW[B['centre']]
        print('   near the window edges (left out):', [(e['rel'], e['plane'], e['target'], round(e['t'], 2)) for e in near][:12])
        print('   inside edge:', [(e['rel'], e['plane'], round(e['t'], 2)) for e in tl if e['t'] < lo + 0.5 or e['t'] > hi - 0.5])
