"""Independent checker (1 Nov 2026) for MATCH sections JUPITER / SUN / MOON. Own matching code; families.py only for scoring a
distance on its family list. Never opens a csv."""
import math
import sys
from itertools import zip_longest
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'tools'))
import families as F  # noqa: E402  (scoring only)

GREEN, YELLOW, LIGHT, UNI = 'C6EFCE', 'FFEB9C', 'FFF8DC', 'BDD7EE'
SEC_FILL, BLOCK_FILL, GRP_FILL = '595959', 'A6A6A6', 'D9D9D9'
SECTIONS = (('JUPITER', 'Jupiter', 'SKY JUPITER'), ('SUN', 'Sun', 'SKY SUN'), ('MOON', 'Moon', 'SKY MOON'))
BLOCKS = ('FIXED STARS', 'CONJUNCTIONS', 'OTHER BODIES')


def fillrgb(c):
    if c.fill is None or c.fill.fill_type is None:
        return None
    rgb = c.fill.fgColor.rgb
    return rgb[-6:] if isinstance(rgb, str) else None


def colour(s):
    return GREEN if s >= 80 else YELLOW if s >= 50 else LIGHT if s > 0 else None


def dra(a, b):
    d = abs(a - b) % 360.0
    return 360.0 - d if d > 180 else d


def best(v, plane):
    """-> (family, label, target value, score) of the best family or None (conj label 'conj')"""
    ev = F.evaluate(v, plane)
    if not ev:
        return None
    e = ev[0]
    return e['family'], e['target'], e['tv'], e['score']


def positions(wb):
    ws = wb['POSITIONS']
    pos, kind = {}, {}
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] is None or r[2] is None or r[5] is None:
            continue
        pos[(r[0], r[2], r[3])] = (float(r[5]), float(r[6]))
        kind[(r[0], r[2], r[3])] = r[4]
    return pos, kind


class Cell:
    __slots__ = ('bi', 'order', 'rel', 'row', 'X', 'plane', 'kind', 'v', 'fam', 'lab', 'tv', 'score', 'body')

    def __init__(self, **k):
        for a in self.__slots__:
            setattr(self, a, k.get(a))


def sky_cells(wb, pos, kind, centre, sheet, errs):
    """every scoring cell of the SKY block of `sheet`, recomputed from POSITIONS and checked against the sheet cells"""
    ws = wb[sheet]
    out, order = [], 0
    pre = f'S {centre} → S '
    cra, cdec = pos[('SKY', 'S', centre)]
    for row in ws.iter_rows(min_row=1):
        if row[0].value != 'SKY' or not isinstance(row[1].value, str) or not row[1].value.startswith(pre):
            continue
        X = row[1].value[len(pre):]
        for plane, (cv, ct, cs) in (('RA', (2, 4, 7)), ('Dec', (11, 13, 16))):
            sv = row[cv].value
            if X == 'equator':
                if plane == 'RA':
                    if sv is not None:
                        errs.append(f'{sheet} r{row[0].row} equator RA not blank')
                    continue
                v, k = abs(cdec), 'equator'
            else:
                xr, xd = pos[('SKY', 'S', X)]
                v = dra(cra, xr) if plane == 'RA' else abs(cdec - xd)
                k = 'body' if kind[('SKY', 'S', X)] == 'body' else 'star'
            order += 1
            if sv is None or abs(sv - round(v, 6)) > 1.5e-6:
                errs.append(f'{sheet} r{row[0].row} {X} {plane}: value {sv} vs POSITIONS {v:.6f}')
            b = best(v, plane)
            shs = row[cs].value
            if b is None:
                if shs is not None:
                    errs.append(f'{sheet} r{row[0].row} {X} {plane}: sheet score {shs}, own none')
                continue
            fam, lab, tv, s = b
            if shs is None or abs(shs - round(s, 2)) > 0.0051:
                errs.append(f'{sheet} r{row[0].row} {X} {plane}: sheet score {shs}, own {s:.4f}')
            want = 'conj (conj)' if fam == 'conj' else f'{lab} ({fam})'
            if row[ct].value != want:
                errs.append(f'{sheet} r{row[0].row} {X} {plane}: target {row[ct].value!r} vs {want!r}')
            out.append(Cell(order=order, rel=row[1].value, X=X, plane=plane, kind=k, v=v, fam=fam, lab=lab, tv=tv, score=s))
    return out


def t24_cells(wb, pos, runner, side, errs):
    """scoring T24 HORSE / JOCKEY cells (star rows x body columns, Jupiter rows except S Jupiter -> S body), recomputed"""
    ws = wb[runner]
    C = side  # 'H' / 'J'
    title = 'T24 HORSE' if side == 'H' else 'T24 JOCKEY'
    rows = list(ws.iter_rows(min_row=1))
    ti = next(i for i, r in enumerate(rows) if r[0].value == 'T24' and isinstance(r[1].value, str) and r[1].value.startswith(title))
    h1, h2 = rows[ti + 1], rows[ti + 2]
    cols = []  # (col index, plane, body)
    v1 = [c.value for c in h1]
    v2 = [c.value for c in h2]
    for plane, mid in (('RA', 'RA midpoints'), ('Dec', 'Dec midpoints')):
        a0, a1 = v1.index(plane), v1.index(mid)
        for ci in range(a0, a1):
            if v2[ci] and v2[ci] != 'S Jupiter':
                cols.append((ci, plane, v2[ci]))
    out, order = [], 0
    sjra, sjdec = pos[('SKY', 'S', 'Jupiter')]
    njra, njdec = pos[(runner, C, 'Jupiter')]
    i = ti + 3
    while i < len(rows) and rows[i][0].value == 'T24':
        r = rows[i]
        lab = r[1].value
        i += 1
        if lab in ('S Jupiter → S body', 'stars'):
            continue
        for ci, plane, X in cols:
            cell = r[ci]
            if lab == f'{C} Jupiter → {C} body':
                a, b = (njra, njdec), pos[(runner, C, X)]
            elif lab == f'S Jupiter → {C} body':
                a, b = (sjra, sjdec), pos[(runner, C, X)]
            elif lab == f'S body → {C} Jupiter':
                a, b = pos[('SKY', 'S', X)], (njra, njdec)
            else:
                star = lab[2:]
                a, b = pos[(runner, C, star)], pos[(runner, C, X)]
            v = dra(a[0], b[0]) if plane == 'RA' else abs(a[1] - b[1])
            order += 1
            if cell.value is None:
                if v > 1e-9:
                    errs.append(f'{runner} {title} {lab} {X} {plane}: blank, own {v:.6f}')
                continue
            if abs(cell.value - round(v, 6)) > 1.5e-6:
                errs.append(f'{runner} {title} {lab} {X} {plane}: {cell.value} vs own {v:.6f}')
            bb = best(v, plane)
            com = cell.comment.text.split('\n')[0] if cell.comment else ''
            if bb is None:
                if not com.startswith('nearest:'):
                    errs.append(f'{runner} {title} {lab} {X} {plane}: comment {com!r}, own no score')
                continue
            fam, tl, tv, s = bb
            parts = com.split(' · ')
            cfam = 'conj' if parts[1].startswith('conjunction') else parts[1]
            if cfam != fam or (fam != 'conj' and parts[0] != tl) or abs(float(parts[3]) - round(s, 2)) > 0.0051:
                errs.append(f'{runner} {title} {lab} {X} {plane}: comment {com!r} vs own {fam} {tl} {s:.4f}')
            out.append(Cell(bi=[c[2] for c in cols].index(X), order=order, row=lab, body=X, plane=plane, v=v, fam=fam, lab=tl, tv=tv, score=s))
    return out


def golden_m(lab):
    return int(lab.split('×')[0])


def r6(x):
    return round(x, 6)


def build_section(sky, t24, side, centre, table):
    """-> list of groups (sky cell, block, part, rows); each row dict with 'cells' (21 values), 'fills' (21), and sort keys"""
    C = side
    groups = []
    for s in sky:
        rows = []
        for t in t24:
            kind = None
            extra = [None] * 5  # C..G
            if s.fam != 'conj' and t.fam != 'conj':
                if (s.fam == t.fam and s.lab == t.lab) or (s.fam != t.fam and F.digits4(r6(s.v)) == F.digits4(r6(t.v))):
                    kind, extra = 'EXACT', ['1', 1, None, None, None]
                    pq = (1, 1)
                elif s.fam == t.fam == 'whole' and s.lab != t.lab:
                    A, B = int(s.lab), int(t.lab)
                    g = gcd(A, B)
                    cf = gcd(g, 360)
                    if cf >= 5:
                        p, q = max(A, B) // g, min(A, B) // g
                        kind, pq = 'RATIO', (p, q)
                        extra = [f'{p}/{q}', r6(p / q), str(g), cf, f'1/{360 // cf}']
                elif s.fam == t.fam == 'golden' and s.lab != t.lab:
                    A, B = golden_m(s.lab), golden_m(t.lab)
                    g = gcd(A, B)
                    p, q = max(A, B) // g, min(A, B) // g
                    if g >= 2 and p <= 6 and q <= 6:
                        kind, pq = 'RATIO', (p, q)
                        extra = [f'{p}/{q}', r6(p / q), f'{g}×φ', None, None]
            if kind is None and s.kind == 'body' and s.X not in ('Moon', centre) and s.score > 50 \
                    and t.row == f'{C} Jupiter → {C} body' and t.body == s.X and t.score > 50:
                kind, pq = 'BODY', None
            if kind is None and s.kind == 'star' and s.fam == 'conj' and s.score > 50 and t.score > 50 \
                    and (t.row == f'{C} {s.X}' or t.row == f'S Jupiter → {C} body'):
                kind, pq = 'CONJ STAR', None
            if kind is None:
                continue
            sf, sl = ('conj', 'conj') if s.fam == 'conj' else (s.fam, s.lab)
            tf, tl = ('conj', 'conj') if t.fam == 'conj' else (t.fam, t.lab)
            low = min(s.score, t.score)
            cells = [table, kind] + extra + [s.rel, s.plane, r6(s.v), sf, sl, round(s.score, 2), t.row, t.body, t.plane, r6(t.v), tf, tl,
                                             round(t.score, 2), round(low, 2)]
            fills = [None] * 21
            if extra[0] == '1':
                fills[2] = UNI
            fills[12], fills[19], fills[20] = colour(s.score), colour(t.score), colour(low)
            # sort keys inside the group
            if kind == 'EXACT':
                key = (0, -t.score, t.order)
            elif kind == 'RATIO':
                key = (1, pq[1], pq[0], -t.score, t.order)
            elif kind == 'BODY':
                key = (2, 0 if t.plane == 'RA' else 1, t.order)
            else:
                body_i = t.order
                key = (3, 0 if t.row != f'S Jupiter → {C} body' else 1, t.bi, 0 if t.plane == 'RA' else 1)
            rows.append(dict(cells=cells, fills=fills, key=key, kind=kind, t=t, s=s, tv=t.tv, pq=pq))
        if not rows:
            continue
        rows.sort(key=lambda r: r['key'])
        if s.kind in ('star', 'equator'):
            block, part = ('CONJUNCTIONS', 0) if s.fam == 'conj' else ('FIXED STARS', 0)
        else:
            block, part = 'OTHER BODIES', (1 if s.fam == 'conj' else 0)
        groups.append(dict(s=s, block=block, part=part, rows=rows))
    groups.sort(key=lambda g: (BLOCKS.index(g['block']), g['part'], -g['s'].score, g['s'].order))
    return groups


def sky_text(s):
    if s.fam == 'conj':
        return f'{s.rel} {s.plane} {s.v:.6f} conjunction ({s.score:.2f})'
    return f'{s.rel} {s.plane} {s.v:.6f} {s.lab} {s.fam} ({s.score:.2f})'


def count(rows, k):
    return sum(1 for r in rows if r['kind'] == k)


def render_match(model, table, ncol=21):
    """expected rows (values, fills) of the table body below the header row: per section band, block bands, groups"""
    out = []
    pad = lambda v: v + [None] * (ncol - len(v))
    for sec, _, _ in SECTIONS:
        groups = model[sec]
        out.append(dict(v=pad([table, sec]), f=[SEC_FILL] * ncol, kind='section', bold=True))
        if not groups:
            out.append(dict(v=pad([table, 'no matches']), f=[None] * ncol, kind='nomatch'))
            continue
        cur = None
        for g in groups:
            if g['block'] != cur:
                cur = g['block']
                out.append(dict(v=pad([table, cur]), f=[BLOCK_FILL] * ncol, kind='block', bold=True))
            rs = g['rows']
            hdr = (f"{sky_text(g['s'])} — EXACT {count(rs, 'EXACT')}, RATIO {count(rs, 'RATIO')}, BODY {count(rs, 'BODY')}, "
                   f"CONJ STAR {count(rs, 'CONJ STAR')}")
            out.append(dict(v=pad([table, hdr]), f=[GRP_FILL] * ncol, kind='group'))
            for r in rs:
                out.append(dict(v=r['cells'], f=r['fills'], kind='row', row=r))
    return out


def title_counts(model, side, n_t24, sky_all):
    """the per-section count sentence expected in the title"""
    parts = []
    for sec, centre, sheet in SECTIONS:
        gs = model[sec]
        rows = [r for g in gs for r in g['rows']]
        ex, ra = count(rows, 'EXACT'), count(rows, 'RATIO')
        wh = sum(1 for r in rows if r['kind'] == 'RATIO' and r['cells'][10] == 'whole')
        go = ra - wh
        bo, cs = count(rows, 'BODY'), count(rows, 'CONJ STAR')
        nconj = sum(1 for g in gs if g['s'].fam == 'conj')
        sk = sky_all[sec]
        sk_nc = sum(1 for s in sk if s.fam != 'conj')
        sk_c = len(sk) - sk_nc
        bl = {b: sum(1 for g in gs if g['block'] == b) for b in BLOCKS}
        bc = sum(1 for g in gs if g['block'] == 'OTHER BODIES' and g['part'] == 1)
        parts.append(f'{sec}: EXACT {ex} rows, RATIO {ra} rows (whole {wh}, golden {go}), BODY {bo} rows, CONJ STAR {cs} rows, '
                     f'{len(gs)} sky cells ({nconj} conjunction) ({sheet} block {sk_nc} scoring cells without conjunction, {sk_c} '
                     f'conjunction); groups: FIXED STARS {bl["FIXED STARS"]}, CONJUNCTIONS {bl["CONJUNCTIONS"]}, OTHER BODIES '
                     f'{bl["OTHER BODIES"]} ({bc} of them body conjunctions, at the end)')
    return parts


# ---------------- HJ ----------------
def hj_key(sec, r):
    c = r['cells']
    s = r['s']
    base = (sec, s.rel, s.plane, r['kind'])
    if r['kind'] in ('EXACT', 'RATIO'):
        return base + (c[2], c[17], c[18])
    if r['kind'] == 'BODY':
        return base + (c[14], c[15])
    return base + ('S' if c[13].startswith('S Jupiter') else 'star', c[14], c[15])


def build_hj(modH, modJ):
    """-> {sec: [groups]} with lines (key, hrow, jrow)"""
    out = {}
    for sec, _, _ in SECTIONS:
        gh = {(g['s'].rel, g['s'].plane): g for g in modH[sec]}
        gj = {(g['s'].rel, g['s'].plane): g for g in modJ[sec]}
        keys = list(dict.fromkeys(list(gh) + list(gj)))
        groups = []
        for k in keys:
            g0 = gh.get(k) or gj.get(k)
            hs, js = (gh[k]['rows'] if k in gh else []), (gj[k]['rows'] if k in gj else [])
            bykey = {}
            for side, rs in (('H', hs), ('J', js)):
                for r in rs:
                    bykey.setdefault(hj_key(sec, r), {'H': [], 'J': []})[side].append(r)
            lines = []
            for key, d in bykey.items():
                for side in 'HJ':
                    d[side].sort(key=lambda r: (-r['t'].score, r['t'].order))
                any_r = (d['H'] or d['J'])[0]
                kind = any_r['kind']
                ko = ('EXACT', 'RATIO', 'BODY', 'CONJ STAR').index(kind)
                if kind == 'RATIO':
                    sk = (ko, any_r['pq'][1], any_r['pq'][0], any_r['tv'])
                elif kind == 'EXACT':
                    sk = (ko, any_r['tv'])
                elif kind == 'CONJ STAR':
                    sk = any_r['key']
                else:
                    sk = (ko,)
                for i, (h, j) in enumerate(zip_longest(d['H'], d['J'])):
                    lines.append(dict(sk=sk, key=key, h=h, j=j, i=i))
            lines.sort(key=lambda L: L['sk'])
            groups.append(dict(s=g0['s'], block=g0['block'], part=g0['part'], lines=lines, nh=hs, nj=js))
        groups.sort(key=lambda g: (BLOCKS.index(g['block']), g['part'], -g['s'].score, g['s'].order))
        out[sec] = groups
    return out


def hj_line_cells(L, table='MATCH HORSE | JOCKEY'):
    h, j = L['h'], L['j']
    src = h or j
    v = [table] + src['cells'][1:13] + (h['cells'][13:21] if h else [None] * 8) + (j['cells'][13:21] if j else [None] * 8)
    f = [None] + src['fills'][1:13] + (h['fills'][13:21] if h else [None] * 8) + (j['fills'][13:21] if j else [None] * 8)
    return v, f


def hj_counts(lines, side):
    return {k: sum(1 for L in lines if L[side] is not None and L[side]['kind'] == k) for k in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR')}


def render_hj(hj, table='MATCH HORSE | JOCKEY', summary=False):
    ncol = 29
    pad = lambda v: v + [None] * (ncol - len(v))
    out = []
    for sec, _, _ in SECTIONS:
        groups = hj[sec]
        sec_rows = []
        cur = None
        for g in groups:
            lines = g['lines']
            if summary:
                lines = [L for L in lines if L_shown(L)]
                if not lines:
                    continue
            if g['block'] != cur:
                cur = g['block']
                sec_rows.append(dict(v=pad([table, cur]), f=[BLOCK_FILL] * ncol, kind='block'))
            ch, cj = hj_counts(lines, 'h'), hj_counts(lines, 'j')
            hdr = sky_text(g['s']) + ' — ' + ', '.join(f'{k} {ch[k]} | {cj[k]}' for k in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR'))
            sec_rows.append(dict(v=pad([table, hdr]), f=[GRP_FILL] * ncol, kind='group'))
            for L in lines:
                v, f = hj_line_cells(L, table)
                sec_rows.append(dict(v=v, f=f, kind='line', line=L))
        if summary and not sec_rows:
            continue
        out.append(dict(v=pad([table, sec]), f=[SEC_FILL] * ncol, kind='section'))
        if not groups:
            out.append(dict(v=pad([table, 'no matches']), f=[None] * ncol, kind='nomatch'))
        out.extend(sec_rows)
    return out


def L_shown(L):
    src = L['h'] or L['j']
    if not src['s'].score > 50:
        return False
    return any(x is not None and x['t'].score > 50 for x in (L['h'], L['j']))
