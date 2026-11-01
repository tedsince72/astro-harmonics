"""Independent check of the MATCH JUPITER / SUN / MOON sections. usage: check.py <before.xlsx> <after.xlsx> [--quiet]"""
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib as L  # noqa: E402

TABLES = (('H', 'MATCH HORSE'), ('J', 'MATCH JOCKEY'))


def style(c):
    f = c.font
    b = c.border
    return (L.fillrgb(c), bool(f.b), f.color.rgb if f.color is not None and isinstance(f.color.rgb, str) else None,
            c.number_format, tuple(getattr(b, s).style for s in ('left', 'right', 'top', 'bottom')),
            c.alignment.horizontal, bool(c.alignment.wrap_text))


def full(c):
    return (c.value, style(c), c.comment.text if c.comment else None)


def find_table(rows, name):
    ti = next(i for i, r in enumerate(rows) if r[0].value == name and isinstance(r[1].value, str) and r[1].value.startswith(name + ' ('))
    return ti


def table_body(rows, ti, name, skip):
    """rows of the table body from ti + skip until column A is not the table name"""
    out = []
    i = ti + skip
    while i < len(rows) and rows[i][0].value == name:
        out.append(rows[i])
        i += 1
    return out, i


def cmp_rows(errs, where, exp, act, ncol):
    n = max(len(exp), len(act))
    for k in range(n):
        if k >= len(exp):
            errs.append(f'{where}: extra sheet row {act[k][0].row}: {[c.value for c in act[k][:4]]}')
            continue
        if k >= len(act):
            errs.append(f'{where}: missing row (expected {exp[k]["v"][:3]}...)')
            continue
        e, a = exp[k], act[k]
        for ci in range(ncol):
            c = a[ci] if ci < len(a) else None
            av = c.value if c is not None else None
            ev = e['v'][ci]
            if isinstance(ev, float) and isinstance(av, (int, float)):
                ok = abs(ev - av) < 1e-9
            else:
                ok = ev == av
            if not ok:
                errs.append(f'{where} {c.coordinate if c is not None else ci}: sheet {av!r} vs expected {ev!r}')
                break
            af = L.fillrgb(c) if c is not None else None
            if af != e['f'][ci]:
                errs.append(f'{where} {c.coordinate}: fill {af} vs expected {e["f"][ci]}')
                break
        if e['kind'] in ('section', 'block') and not a[1].font.b:
            errs.append(f'{where} {a[1].coordinate}: band not bold')
        if e['kind'] == 'section' and (a[1].font.color is None or str(a[1].font.color.rgb)[-6:] != 'FFFFFF'):
            errs.append(f'{where} {a[1].coordinate}: section band font not white')


def check(before, after, quiet=False):
    errs = []
    wa = openpyxl.load_workbook(after)
    wb = openpyxl.load_workbook(before)
    pos, kind = L.positions(wa)
    sky_all = {sec: L.sky_cells(wa, pos, kind, centre, sheet, errs) for sec, centre, sheet in L.SECTIONS}
    runners = [s for s in wa.sheetnames if s.startswith('P') and s[1:].isdigit()]
    counts = {}
    hj_models = {}
    hjcount = {}
    for p in runners:
        rows_a = list(wa[p].iter_rows())
        rows_b = list(wb[p].iter_rows())
        models = {}
        first_match = None
        for side, name in TABLES:
            t24 = L.t24_cells(wa, pos, p, side, errs)
            model = {sec: L.build_section(sky_all[sec], t24, side, centre, name) for sec, centre, _ in L.SECTIONS}
            models[side] = model
            ti = find_table(rows_a, name)
            first_match = ti if first_match is None else first_match
            title = rows_a[ti][1].value
            for part in L.title_counts(model, side, len(t24), sky_all):
                if part not in title:
                    errs.append(f'{p} {name} title: missing {part!r}')
            nt = sum(1 for t in t24 if t.fam != 'conj')
            if f'T24 {"HORSE" if side == "H" else "JOCKEY"} {nt} scoring cells' not in title:
                errs.append(f'{p} {name} title: T24 scoring cell count {nt} not found')
            body, _ = table_body(rows_a, ti, name, 2)
            exp = L.render_match(model, name)
            cmp_rows(errs, f'{p} {name}', exp, body, 21)
            # header row = before header row
            tb = find_table(rows_b, name)
            for ca, cb in zip(rows_a[ti + 1][:21], rows_b[tb + 1][:21]):
                if full(ca) != full(cb):
                    errs.append(f'{p} {name} header {ca.coordinate} differs from before')
            # JUPITER section vs before, cell for cell incl. styles
            bbody, _ = table_body(rows_b, tb, name, 2)
            sec_idx = [k for k, r in enumerate(body) if r[1].value in ('JUPITER', 'SUN', 'MOON') and L.fillrgb(r[1]) == L.SEC_FILL]
            jup = body[sec_idx[0] + 1:sec_idx[1]] if len(sec_idx) >= 2 else []
            if len(jup) != len(bbody):
                errs.append(f'{p} {name}: JUPITER section {len(jup)} rows vs before {len(bbody)}')
            for ra, rb in zip(jup, bbody):
                for ca, cb in zip(ra[:21], rb[:21]):
                    if full(ca) != full(cb):
                        errs.append(f'{p} {name} JUPITER {ca.coordinate} vs before {cb.coordinate}: {full(ca)} / {full(cb)}')
                        break
            counts[(p, side)] = {sec: sum(len(g['rows']) for g in model[sec]) for sec in model}
        # HJ
        hj = L.build_hj(models['H'], models['J'])
        hj_models[p] = (hj, rows_a)
        name = 'MATCH HORSE | JOCKEY'
        ti = find_table(rows_a, name)
        body, end = table_body(rows_a, ti, name, 3)
        exp = L.render_hj(hj)
        cmp_rows(errs, f'{p} HJ', exp, body, 29)
        # HJ JUPITER section vs the before HJ table, cell for cell
        tbh = find_table(rows_b, name)
        bbody, _ = table_body(rows_b, tbh, name, 3)
        sec_idx = [k for k, r in enumerate(body) if r[1].value in ('JUPITER', 'SUN', 'MOON') and L.fillrgb(r[1]) == L.SEC_FILL]
        jup = body[sec_idx[0] + 1:sec_idx[1]] if len(sec_idx) >= 2 else []
        if len(jup) != len(bbody):
            errs.append(f'{p} HJ: JUPITER section {len(jup)} rows vs before {len(bbody)}')
        for ra, rb in zip(jup, bbody):
            for ca, cb in zip(ra[:29], rb[:29]):
                if full(ca) != full(cb):
                    errs.append(f'{p} HJ JUPITER {ca.coordinate} vs before {cb.coordinate}')
                    break
        hjcount[p] = (len(jup), len(bbody))
        title = rows_a[ti][1].value
        for sec, _, _ in L.SECTIONS:
            gs = hj[sec]
            lines = [ln for g in gs for ln in g['lines']]
            keys = {}
            for ln in lines:
                d = keys.setdefault(ln['key'], [0, 0])
                d[0] += ln['h'] is not None
                d[1] += ln['j'] is not None
            kk = {k: sum(1 for key in keys if key[3] == k) for k in ('EXACT', 'RATIO', 'BODY', 'CONJ STAR')}
            bl = {b: sum(1 for g in gs if g['block'] == b) for b in L.BLOCKS}
            bc = sum(1 for g in gs if g['block'] == 'OTHER BODIES' and g['part'] == 1)
            txt = (f"{sec}: {len(lines)} lines, {len(keys)} keys: {sum(1 for d in keys.values() if d[0] and d[1])} with both sides, "
                   f"{sum(1 for d in keys.values() if d[0] and not d[1])} horse only, {sum(1 for d in keys.values() if d[1] and not d[0])} "
                   f"jockey only (EXACT {kk['EXACT']}, RATIO {kk['RATIO']}, BODY {kk['BODY']}, CONJ STAR {kk['CONJ STAR']}); groups: "
                   f"FIXED STARS {bl['FIXED STARS']}, CONJUNCTIONS {bl['CONJUNCTIONS']}, OTHER BODIES {bl['OTHER BODIES']} ({bc} of them "
                   f"body conjunctions, at the end); {len(gs)} sky cells (MATCH HORSE {counts[(p, 'H')][sec]} rows, MATCH JOCKEY "
                   f"{counts[(p, 'J')][sec]} rows)")
            if txt not in title:
                errs.append(f'{p} HJ title: missing {txt!r}')
        counts[(p, 'HJ')] = {sec: sum(len(g['lines']) for g in hj[sec]) for sec in hj}
        # outside MATCH: identical before / after
        tb0 = find_table(rows_b, 'MATCH HORSE')
        if first_match != tb0:
            errs.append(f'{p}: MATCH HORSE title row {first_match + 1} vs before {tb0 + 1}')
        for ra, rb in zip(rows_a[:first_match], rows_b[:tb0]):
            for ca, cb in zip(ra, rb):
                if full(ca) != full(cb):
                    errs.append(f'{p} {ca.coordinate}: outside MATCH differs from before')
                    break
        for r in rows_a[end:]:
            if any(c.value is not None for c in r):
                errs.append(f'{p} r{r[0].row}: content after the HJ table')
                break
        if wa[p].freeze_panes != wb[p].freeze_panes:
            errs.append(f'{p}: freeze {wa[p].freeze_panes} vs {wb[p].freeze_panes}')
        for col, d in wb[p].column_dimensions.items():
            if wa[p].column_dimensions[col].width != d.width:
                errs.append(f'{p}: width {col} {wa[p].column_dimensions[col].width} vs {d.width}')
        ma = {str(m) for m in wa[p].merged_cells.ranges if m.min_row <= first_match}
        mb = {str(m) for m in wb[p].merged_cells.ranges if m.min_row <= tb0}
        if ma != mb:
            errs.append(f'{p}: merges outside MATCH differ {ma ^ mb}')
    # other sheets identical
    if wa.sheetnames != wb.sheetnames:
        errs.append(f'sheet names {wa.sheetnames} vs {wb.sheetnames}')
    ncell = 0
    for sn in wb.sheetnames:
        if sn in runners or sn == 'SUMMARY':
            continue
        ra_, rb_ = list(wa[sn].iter_rows()), list(wb[sn].iter_rows())
        if len(ra_) != len(rb_):
            errs.append(f'{sn}: {len(ra_)} rows vs {len(rb_)}')
        for x, y in zip(ra_, rb_):
            for ca, cb in zip(x, y):
                ncell += 1
                if full(ca) != full(cb):
                    errs.append(f'{sn} {ca.coordinate} differs')
                    break
        if {str(m) for m in wa[sn].merged_cells.ranges} != {str(m) for m in wb[sn].merged_cells.ranges}:
            errs.append(f'{sn}: merges differ')
    # SUMMARY
    ws = wa['SUMMARY']
    srows = list(ws.iter_rows())
    exp = []
    nsum = {}
    for p in runners:
        hj, rows_a = hj_models[p]
        exp.append(dict(v=[rows_a[0][0].value] + [None] * 28, f=[None] * 29, kind='a1'))
        ti = find_table(rows_a, 'MATCH HORSE | JOCKEY')
        for r in (rows_a[ti + 1], rows_a[ti + 2]):
            exp.append(dict(v=[c.value for c in r[:29]], f=[L.fillrgb(c) for c in r[:29]], kind='hdr'))
        body = L.render_hj(hj, summary=True)
        nsum[p] = {sec: sum(1 for g in hj[sec] for ln in g['lines'] if L.L_shown(ln)) for sec in hj}
        if not body:
            exp.append(dict(v=['MATCH HORSE | JOCKEY', 'no lines'] + [None] * 27, f=[None] * 29, kind='nolines'))
        exp.extend(body)
        if p != runners[-1]:
            exp += [dict(v=[None] * 29, f=[None] * 29, kind='blank')] * 2
    srows = [r for r in srows]
    while srows and all(c.value is None for c in srows[-1]):
        srows.pop()
    cmp_rows(errs, 'SUMMARY', exp, srows, 29)
    # SUMMARY JUPITER parts vs the before SUMMARY (same runner, lines, headers, block bands; cells and styles)
    def blocks(rows, sections):
        out, cur = {}, None
        for r in rows:
            a = r[0].value
            if isinstance(a, str) and a[:1] == 'P' and a[1:3].isdigit() and r[1].value is None:
                cur = a.split()[0]
                out[cur] = []
                mode = 'JUPITER' if not sections else None
                continue
            if cur is None or a in (None, 'table') or (a == 'MATCH HORSE | JOCKEY' and r[1].value is None):
                continue
            if sections and r[1].value in ('JUPITER', 'SUN', 'MOON') and L.fillrgb(r[1]) == L.SEC_FILL:
                mode = r[1].value
                continue
            if mode == 'JUPITER':
                out[cur].append(r)
        return out
    sb = blocks(list(wb['SUMMARY'].iter_rows()), False)
    sa = blocks(list(wa['SUMMARY'].iter_rows()), True)
    for p in runners:
        x, y = sa.get(p, []), sb.get(p, [])
        if [r[1].value for r in y] == ['no lines']:
            y = []
        if len(x) != len(y):
            errs.append(f'SUMMARY {p}: JUPITER part {len(x)} rows vs before {len(y)}')
        for ra, rb in zip(x, y):
            for ca, cb in zip(ra[:29], rb[:29]):
                if full(ca) != full(cb):
                    errs.append(f'SUMMARY {p} JUPITER {ca.coordinate} vs before {cb.coordinate}')
                    break
        hjcount[p] = hjcount[p] + (len(x),)
    if not quiet:
        print('sky scoring cells:', {s: len(v) for s, v in sky_all.items()}, ' other-sheet cells compared:', ncell)
        print('JUPITER rows compared vs before (HJ after, HJ before, SUMMARY):', hjcount)
        for p in runners:
            print(p, 'H', counts[(p, 'H')], '| J', counts[(p, 'J')], '| HJ lines', counts[(p, 'HJ')], '| SUMMARY lines', nsum[p])
    return errs


if __name__ == '__main__':
    e = check(sys.argv[1], sys.argv[2], '--quiet' in sys.argv)
    for x in e[:60]:
        print('ERR', x)
    print('mismatches:', len(e))
