#!/usr/bin/env python3
"""T24 links and repeats per runner (Eddie, 4 Nov 2026).

For one runner sheet, horse then jockey:
  1. every scoring cell of the T24 top rows (S Jupiter → S body, H/J Jupiter → body, S Jupiter → natal body,
     S body → natal Jupiter, S Sun → S body, S Sun → natal body, S Moon → S body, S Moon → natal body);
  2. every star row whose S Jupiter column scores (sky Jupiter on the star; Eddie, 4 Nov 2026), RA or Dec,
     highest sky Jupiter score first, with every scoring cell of that row (bodies and the S Jupiter / S Sun /
     S Moon columns);
  3. then the star rows on a sky Sun or sky Moon line only (S Sun / S Moon column scores, no S Jupiter): their
     cells on a body join a chain built from 1 and 2 as part C (with their own centre named); they never start a
     chain of their own (Eddie, 4 Nov 2026: Jupiter first, Sun and Moon joining);
Sky-only cells (S Jupiter / S Sun / S Moon → S body, and the S columns of a star row) are the same on the horse and
jockey blocks: they are listed and counted once, as side S.
then, horse and jockey together:
  CHAINS  - a body or star in two or more rows with a cell that closes it on a natal Jupiter, with its parts
            (Eddie, 4 Nov 2026, from Cuban Cigar's Chiron): A sky centre → sky X (or X a star on a sky line),
            B sky centre → natal X, C a star on a sky line → natal X (with the star's strongest sky line and its
            score), D closes on a natal Jupiter (sky X → natal Jupiter, natal Jupiter → X, or star X → own Jupiter);
            each part shows its best cell with value and score, and the sky centre of A, B, C ('one centre: Sun', or
            each centre: Sun and Moon are different, Eddie 4 Nov 2026); most parts first. No natal Moon (the
            natal T24 columns have none; the S Moon column is the sky).
  REPEATS - the same target (family and number, not conj) in two or more cells; SKY + NATAL first (a sky line value
            repeated on a natal cell);
  OTHER LINKS - a body or star in two or more rows, not closing on a Jupiter.
Every natal cell is marked ONLY (no other runner has that cell - same chart, row or star, body, plane and target)
or 'also <runner> <score> (lower / higher / same)'; sky cells are marked 'sky' (the same for every runner). The FIELD block at the end lists
the chains of every runner.

Cell values are read from the sheet; each is scored with tools/families.py (the same as the cell comments).
Counted: whole, golden, conj from 50; ninth, phi power, sqrt2, silver at any score.

Usage: python3 tools/t24_links.py <tables.xlsx> [P05 ...]   (no runner = every runner)
"""
import os, sys
from collections import defaultdict
import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import families as F

CUT50 = {'whole', 'golden', 'conj'}


def counts(b):
    if not b or b.get('score') is None:
        return False
    if b['family'] in CUT50:
        return b['score'] >= 50
    return b['score'] > 0


def blocks(rows):
    """yield (side, header row index of body names, first row, last row) for T24 HORSE / T24 JOCKEY."""
    out = []
    for i, r in enumerate(rows):
        if r and r[0] == 'T24' and isinstance(r[1], str) and r[1].startswith(('T24 HORSE', 'T24 JOCKEY')):
            side = 'H' if r[1].startswith('T24 HORSE') else 'J'
            j = i + 3
            while j < len(rows) and rows[j] and rows[j][0] == 'T24':
                j += 1
            out.append((side, i + 2, i + 3, j))
    return out


def cols(head, names):
    """column index -> (plane, body name) from the two header rows."""
    c, plane = {}, None
    for k, v in enumerate(head):
        if v in ('RA', 'Dec'):
            plane = v
        nm = names[k] if k < len(names) else None
        if plane and nm and not str(nm).startswith('star =') and not str(nm).startswith('target'):
            c[k] = (plane, nm)
    return c


def cell(v, plane):
    if not isinstance(v, (int, float)):
        return None
    b = F.best(v, plane)
    return b if counts(b) else None


def fmt(e):
    b = e['b']
    t = 'conj' if b['family'] == 'conj' else f"{b['target']} {b['family']}"
    return f"{e['row']} | {e['body']} {e['plane']} {e['v']:.4f} {t} ({b['score']:.2f})"


def collect(ws_rows):
    """(entries, star rows on the sky Jupiter line per side, Sun / Moon star-row entries) for one runner sheet."""
    entries, jstar, extra = [], {}, []
    for side, hi, first, last in blocks(ws_rows):
        c = cols(ws_rows[hi - 1], ws_rows[hi])
        top = []
        k = first
        while k < last and ws_rows[k][1] != 'stars':
            top.append(ws_rows[k]); k += 1
        stars = [r for r in ws_rows[k + 1:last] if r[1]]
        for r in top:
            skyrow = r[1].endswith('→ S body')
            if skyrow and side == 'J':
                continue            # sky-only: once, on the horse block
            for ci, (pl, nm) in c.items():
                b = cell(r[ci], pl)
                if b:
                    entries.append(dict(side='S' if skyrow else side, row=r[1], body=nm, plane=pl, v=r[ci], b=b,
                                        kind='top', block=side))
        jr = []
        for r in stars:
            js = [cell(r[ci], pl) for ci, (pl, nm) in c.items() if nm == 'S Jupiter']
            js = [x for x in js if x]
            if js:
                jr.append((max(x['score'] for x in js), r))
            elif any(cell(r[ci], pl) for ci, (pl, nm) in c.items() if nm in ('S Sun', 'S Moon')):
                st = r[1].split(' ', 1)[1]
                for ci, (pl, nm) in c.items():
                    b = cell(r[ci], pl)
                    if b:
                        sk = nm.startswith('S ')
                        extra.append(dict(side='S' if sk else side, row=('S ' + st) if sk else r[1], body=nm,
                                          plane=pl, v=r[ci], b=b, kind='sm', star=st, block=side))
        jr.sort(key=lambda x: -x[0])
        jstar[side] = []
        for sc, r in jr:
            st = r[1].split(' ', 1)[1]
            jstar[side].append((sc, r[1]))
            for ci, (pl, nm) in c.items():
                b = cell(r[ci], pl)
                if b:
                    sk = nm.startswith('S ')
                    entries.append(dict(side='S' if sk else side, row=('S ' + st) if sk else r[1], body=nm,
                                        plane=pl, v=r[ci], b=b, kind='star', star=st, block=side))
    # one copy of each cell
    u, x = {}, {}
    for e in entries:
        u.setdefault((e['side'], e['row'], e['body'], e['plane']), e)
    for e in extra:
        x.setdefault((e['side'], e['row'], e['body'], e['plane']), e)
    return list(u.values()), jstar, list(x.values())


def tkey(b):
    return 'conj' if b['family'] == 'conj' else (b['family'], b['target'])


def fkey(e):
    """the same cell on another runner: chart, row (star name for star rows), body, plane, target."""
    row = e['row']
    if e['kind'] in ('star', 'sm') and e['side'] in 'HJ':
        row = 'star ' + e['star']
    return (e['side'], row, e['body'], e['plane'], tkey(e['b']))


def field_mark(e, me, field):
    if e['side'] == 'S':
        return 'sky'
    k = fkey(e)
    hl = lambda x: 'lower' if x < e['b']['score'] else ('higher' if x > e['b']['score'] else 'same')
    also = [f"{r} {x['b']['score']:.2f} ({hl(x['b']['score'])})" for r, idx in field.items() if r != me
            for x in idx.get(k, [])]
    return 'ONLY' if not also else 'also ' + ', '.join(also)


def jup_cell(e, x):
    """does cell e close body or star x on a natal Jupiter?"""
    r = e['row']
    if e['kind'] == 'top' and e['side'] in 'HJ' and e['body'] == x:
        return r in ('S body → H Jupiter', 'S body → J Jupiter', 'H Jupiter → H body', 'J Jupiter → J body')
    if e['kind'] == 'star' and e['star'] == x and e['body'] == 'Jupiter':
        return True                                           # star x → own Jupiter
    return False


def skyline(star, entries):
    """the strongest sky line onto a star: 'sky Jupiter 26×φ golden 93.94'."""
    ls = [e for e in entries if e['kind'] in ('star', 'sm') and e['side'] == 'S' and e['star'] == star]
    if not ls:
        return None
    e = max(ls, key=lambda e: e['b']['score'])
    return f"sky {e['body'][2:]} {sc(e)}", e['body'][2:]


def skylines(star, entries):
    """every sky line onto a star: ('sky Sun RA 65×φ golden 92.31, sky Moon ...', 'Sun / Moon')."""
    ls = sorted((e for e in entries if e['kind'] in ('star', 'sm') and e['side'] == 'S' and e['star'] == star),
                key=lambda e: -e['b']['score'])
    txt = ', '.join(f"sky {e['body'][2:]} {sc(e)}" for e in ls)
    cs = []
    for e in ls:
        if e['body'][2:] not in cs:
            cs.append(e['body'][2:])
    return txt, ' / '.join(sorted(cs, key=['Jupiter', 'Sun', 'Moon'].index))


def sc(e):
    t = 'conj' if e['b']['family'] == 'conj' else f"{e['b']['target']} {e['b']['family']}"
    return f"{e['plane']} {e['v']:.4f} {t} {e['b']['score']:.2f}"


def parts(nm, es, entries):
    """the four parts of Eddie's chain (4 Nov 2026, Cuban Cigar) for body or star nm, best cell of each part,
    with the sky centre of A, B and the star's sky line (Eddie: Sun and Moon are different)."""
    p, cen = {}, {}
    best = lambda k, txt, e, c=None: (k not in p or e['b']['score'] > p[k][1]) and \
        (p.__setitem__(k, (txt, e['b']['score'])), cen.__setitem__(k, c))
    for e in es:
        if e['kind'] == 'top' and e['side'] == 'S' and e['body'] == nm:
            c = e['row'].split(' →')[0][2:]
            best('A', f"sky {c} → sky {nm} {sc(e)}", e, c)
        if e['kind'] == 'top' and e['side'] in 'HJ' and e['body'] == nm and e['row'].startswith('S ') \
                and not e['row'].startswith('S body'):
            c = e['row'].split(' →')[0][2:]
            best('B', f"sky {c} → {e['side']} {nm} {sc(e)}", e, c)
        if e['kind'] == 'star' and e['side'] in 'HJ' and e['body'] == nm:
            sl = skyline(e['star'], entries)
            if sl:
                best('C', f"{e['side']} {e['star']} → {nm} {sc(e)}; {e['star']} on {sl[0]}", e, sl[1])
        if jup_cell(e, nm):
            to = e['row'].split('→ ')[-1] if e['row'].startswith('S body') else \
                (e['row'].split(' →')[0] if e['kind'] == 'top' else f"{e['side']} {nm} → own Jupiter")
            best('D', f"{to} {sc(e)}" if e['kind'] == 'star' else
                 (f"sky {nm} → {to} {sc(e)}" if e['row'].startswith('S body') else f"{to} → {e['side']} {nm} {sc(e)}"), e)
    if nm in {e['star'] for e in es if e['kind'] == 'star'}:
        sl = skyline(nm, entries)
        if sl and 'A' not in p:
            p['A'], cen['A'] = (f'{nm} on {sl[0]}', 0), sl[1]
    both = {e['side'] for e in es if e['kind'] == 'star' and e['star'] == nm and e['body'] == 'Jupiter'}
    if both == {'H', 'J'}:
        p['D'] = (p['D'][0] + '; on both charts', p['D'][1])
    out = {k: v[0] for k, v in p.items()}
    cs = [cen[k] for k in 'ABC' if cen.get(k)]
    if cs:
        out['centres'] = ('one centre: ' + cs[0]) if len(set(cs)) == 1 else \
            'centres: ' + ', '.join(f'{k} {cen[k]}' for k in 'ABC' if cen.get(k))
    return out


def report(label, me, entries, jstar, extra, field):
    out = [f'=== {label} ===']
    sh = lambda e: f"{e['side']} {fmt(e)}   [{field_mark(e, me, field)}]"
    by = defaultdict(list)
    for e in entries:
        nm = e['body']
        if nm != 'Jupiter' and not nm.startswith('S '):   # natal Sun and Moon are bodies; S columns go to the star
            by[nm].append(e)
        if e['kind'] == 'star':
            by[e['star']].append(e)
    links = {nm: es for nm, es in by.items() if len({(e['side'], e['row']) for e in es}) >= 2}
    # CHAINS: a link with a cell closing it on a Jupiter and at least one cell from another row
    chains = []
    for nm, es in links.items():
        js = [e for e in es if jup_cell(e, nm)]
        if js and len({(e['side'], e['row']) for e in es}) >= 2:
            only = sum(1 for e in es if field_mark(e, me, field) == 'ONLY')
            pt = parts(nm, es, entries)
            tags = [f'{k}: {pt[k]}' for k in 'ABCD' if k in pt]
            letters = {k for k in 'ABCD' if k in pt}
            # Sun / Moon star rows join the chain (body chains only), as part C with their own centre
            joined = [e for e in extra if e['side'] in 'HJ' and e['body'] == nm]
            cen = pt.get('centres', '')
            for e in sorted(joined, key=lambda e: -e['b']['score']):
                txt, cs = skylines(e['star'], extra)
                tags.append(f"C {cs}: {e['side']} {e['star']} → {nm} {sc(e)}; {e['star']} on {txt}")
                letters.add('C')
            if joined:
                es = es + joined
                only = sum(1 for e in es if field_mark(e, me, field) == 'ONLY')
                jc = sorted({c for e in joined for c in skylines(e['star'], extra)[1].split(' / ')},
                            key=['Jupiter', 'Sun', 'Moon'].index)
                cen = (cen + '; ' if cen else '') + 'joined C: ' + ' / '.join(jc)
            if cen:
                tags.append(cen)
            sides = ''.join(sorted({e['side'] for e in es}))
            chains.append((nm, es, js, only, tags, sides, ''.join(sorted(letters))))
    chains.sort(key=lambda c: (-len(c[6]), -len({(e['side'], e['row']) for e in c[1]}), -c[3], c[0]))
    out.append('\n--- CHAINS: a body or star in two or more rows that also closes on a Jupiter ---')
    out.append('(parts, Eddie 4 Nov 2026: A sky centre → sky X (or X a star on a sky line); B sky centre → natal X; '
               'C a star on a sky line → natal X; D closes on a natal Jupiter (sky X → natal Jupiter, natal Jupiter '
               '→ X, or star X → own Jupiter). Most parts first. [ONLY] = no other runner has that cell on the same '
               'target; sky cells are the same for every runner. →J marks the closing cells. "C Sun / Moon": a star on '
               'a sky Sun or Moon line only, joining the chain.)')
    for nm, es, js, only, tags, sides, letters in chains:
        out.append(f"{nm}: parts {letters}, {len({(e['side'], e['row']) for e in es})} rows, {sides}, {only} ONLY cells")
        for t in tags:
            out.append('      ' + t)
        for e in sorted(es, key=lambda e: (not jup_cell(e, nm), e['kind'] == 'sm', -e['b']['score'])):
            out.append('   ' + ('→J ' if jup_cell(e, nm) else ('+C ' if e['kind'] == 'sm' else '   ')) + sh(e))
    out.append('\n--- REPEATS: the same target (family and number, not conj) in two or more cells; '
               'SKY + NATAL (a sky line value repeated on a natal cell) first ---')
    bt = defaultdict(list)
    joinedall = [e for c in chains for e in c[1] if e['kind'] == 'sm']
    for e in entries + joinedall:
        if e['b']['family'] != 'conj':
            bt[tkey(e['b'])].append(e)
    skynat = lambda es: any(e['side'] == 'S' for e in es) and any(e['side'] in 'HJ' for e in es)
    for (fam, t), es in sorted(bt.items(), key=lambda x: (not skynat(x[1]), -len(x[1]),
                                                          -max(e['b']['score'] for e in x[1]))):
        if len(es) >= 2:
            out.append(f'{t} {fam}  (x{len(es)})' + ('  SKY + NATAL' if skynat(es) else '') + ':')
            for e in sorted(es, key=lambda e: -e['b']['score']):
                out.append('   ' + sh(e))
    out.append('\n--- OTHER LINKS: in two or more rows, not closing on a Jupiter ---')
    cn = {c[0] for c in chains}
    for nm, es in sorted(links.items(), key=lambda x: (-len(x[1]), x[0])):
        if nm in cn:
            continue
        out.append(f"{nm}  ({len({(e['side'], e['row']) for e in es})} rows):")
        for e in sorted(es, key=lambda e: -e['b']['score']):
            out.append('   ' + sh(e))
    for blk in ('H', 'J'):
        out.append(f"\n--- {'HORSE' if blk == 'H' else 'JOCKEY'}: top rows ---")
        rows = []
        for e in entries:
            if e['kind'] == 'top' and e['block'] == blk:
                rows.append(e)
        cur = None
        for e in sorted(rows, key=lambda e: (e['row'], -e['b']['score'])):
            if e['row'] != cur:
                cur = e['row']; out.append(cur + ':')
            out.append('   ' + sh(e))
        out.append(f"\n--- {'HORSE' if blk == 'H' else 'JOCKEY'}: star rows on the sky Jupiter line, "
                   "highest sky Jupiter score first ---")
        for scr, rl in jstar.get(blk, []):
            st = rl.split(' ', 1)[1]
            out.append(f'{rl} (sky Jupiter {scr:.2f}):')
            es = [e for e in entries if e['kind'] == 'star' and e['star'] == st and (e['row'] == rl or e['side'] == 'S')]
            for e in sorted(es, key=lambda e: (e['body'] not in ('Jupiter', 'S Jupiter'), -e['b']['score'])):
                out.append('   ' + sh(e))
        js_ = [e for e in joinedall if e['block'] == blk]
        out.append(f"\n--- {'HORSE' if blk == 'H' else 'JOCKEY'}: star rows on a sky Sun / Moon line joining a chain ---")
        for e in sorted(js_, key=lambda e: -e['b']['score']):
            out.append(f"   {sh(e)}; {e['star']} on {skylines(e['star'], extra)[0]}")
    return out, chains


def main():
    wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
    want = sys.argv[2:]
    data = {}
    for name in wb.sheetnames:
        if name.startswith('P') and name[1:].isdigit():
            rows = [tuple(r) for r in wb[name].iter_rows(values_only=True)]
            ents, js, ex = collect(rows)
            data[name] = (rows[0][0], ents, js, ex)
    field = {}
    for name, (_, ents, _, ex) in data.items():
        idx = defaultdict(list)
        for e in ents + ex:
            if e['side'] != 'S':
                idx[fkey(e)].append(e)
        field[name] = idx
    summary = []
    for name, (lab, ents, js, ex) in data.items():
        if want and name not in want:
            continue
        out, chains = report(lab, name, ents, js, ex, field)
        print('\n'.join(out)); print()
        summary.append((lab, chains))
    print('=== FIELD: chains per runner, most parts first (A sky centre → sky X / X on a sky line; B sky centre → natal X; '
          'C sky-line star → natal X (C Sun / Moon: joining); D closes on a natal Jupiter) ===')
    for lab, chains in summary:
        print(lab)
        for nm, es, js, only, tags, sides, letters in chains:
            print(f"   {nm}: parts {letters}, {len({(e['side'], e['row']) for e in es})} rows, {sides}, {only} ONLY cells")
            for t in tags:
                print('        ' + t)


if __name__ == '__main__':
    main()
