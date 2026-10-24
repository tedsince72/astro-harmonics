"""compare_wording.py (Eddie, 24 Oct 2026: '<target> <family> — not a 4-digit match (<offset>)'): OLD_FAMILIES.py BEFORE.xlsx AFTER.xlsx
BEFORE = the build of commit 10b18003 (half + 4-digit rule, old wording), AFTER = now. Every cell compared (value, fill, comment, border,
number format), every sheet, and the pairs workbooks next to them. A cell may differ only in its text / comment, where the nearest-target
text of a value that fails the 4-digit match changed from '... — outside ...' to '<target> <family> — not a 4-digit match (<offset>)', with the
same target, family and offset; and that value must be inside the family's old tolerance (OLD_FAMILIES = families.py of 83850b1c: its score
on that family > 0) and score nothing now. Every '— outside ±' text left must be a value beyond the old tolerance. Prints counts per sheet."""
import sys, re, os, importlib.util
import openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import families as FN                                                    # noqa: E402

NEW = re.compile(r'^(?P<t>\S+) (?P<f>whole|half|golden|phi power|ninth|sqrt2|silver) — not a 4-digit match \((?P<o>[+-]\d+\.\d+)\)$')
OLD_A = re.compile(r'^(?P<t>\S+) \((?P<f>golden|phi power|ninth|sqrt2|silver)\) — outside(?: ±[0-9.]+)?$')          # cells, sky equivalents
OLD_D = re.compile(r'^(?P<t>\S+) (?P<o>[+-]\d+\.\d+) \(outside ±[0-9.]+\)$')                                         # FIELD cells
OLD_B = re.compile(r'^nearest: (?P<t>\S+) · (?P<f>golden|phi power|ninth|sqrt2|silver) — outside ±[0-9.]+ · (?P<o>[+-]\d+\.\d+)$')
ANYOUT = re.compile(r'^(?P<t>\S+) \((?P<f>golden|phi power|ninth|sqrt2|silver)\) — outside ±')
FAMOF = {}


def load_old(p):
    spec = importlib.util.spec_from_file_location('families_old', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def old_inside(FO, v, fam, t):
    """the old families score v on that family's target t (> 0), and the new ones give it nothing"""
    s, lab, tv = FO.score_family(v, fam)
    return s > 0 and lab == t and not FN.evaluate(v, 'Dec', 'deg') or (s > 0 and lab == t and
                                                                        all(d['family'] == 'conj' for d in FN.evaluate(v, 'RA', 'deg')))


def sig(c):
    return (c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.border.left.style, c.border.top.style, c.number_format)


def main(fo_path, fb, fa):
    FO = load_old(fo_path)
    bad, cnt, kept = [], {}, 0
    for b_, a_ in ((fb, fa), (fb.replace('_jupiter_tables', '_pairs'), fa.replace('_jupiter_tables', '_pairs'))):
        wb, wa = openpyxl.load_workbook(b_), openpyxl.load_workbook(a_)
        if wb.sheetnames != wa.sheetnames:
            bad.append(('sheets', b_))
            continue
        for sh in wa.sheetnames:
            rb, ra = list(wb[sh].iter_rows()), list(wa[sh].iter_rows())
            if len(rb) != len(ra):
                bad.append((sh, 'rows', len(rb), len(ra)))
                continue
            for x, y in zip(rb, ra):
                if len(x) != len(y):
                    bad.append((sh, 'cols', x[0].row))
                    continue
                for j, (c, d) in enumerate(zip(x, y)):
                    if sig(c) != sig(d):
                        bad.append((sh, d.coordinate, 'format / fill / border'))
                    cb, ca = (c.comment.text if c.comment else None), (d.comment.text if d.comment else None)
                    if isinstance(d.value, str) and ANYOUT.match(d.value):
                        kept += 1
                    if c.value == d.value and cb == ca:
                        continue
                    if c.value != d.value:
                        m = NEW.match(str(d.value).split('\n')[0]) if isinstance(d.value, str) else None
                        o = (OLD_A.match(c.value) or OLD_D.match(c.value)) if isinstance(c.value, str) else None
                        if not (m and o and m.group('t') == o.group('t') and o.groupdict().get('f', m.group('f')) == m.group('f')):
                            bad.append((sh, d.coordinate, 'text', c.value, d.value))
                            continue
                        off = o.groupdict().get('o')
                        if off is None:                     # cells: the offset cell 2 to the right (T-tables), else not shown before
                            r2 = y[j + 2].value if j + 2 < len(y) else None
                            off = r2 if isinstance(r2, str) and re.fullmatch(r'[+-]\d+\.\d+', r2 or '') else None
                        if off is not None and off != m.group('o'):
                            bad.append((sh, d.coordinate, 'offset', off, m.group('o')))
                        p1, p2 = (y[j - 1].value if j >= 1 else None), (y[j - 2].value if j >= 2 else None)
                        v = p2 if num(p2) and (p1 is None or num(p1)) else p1 if num(p1) else None   # value, +5 min, target (T-tables)
                        if v is None or not old_inside(FO, float(v), m.group('f'), m.group('t')):
                            bad.append((sh, d.coordinate, 'value not inside the old tolerance', v, d.value))
                        cnt[sh] = cnt.get(sh, 0) + 1
                    if cb != ca:
                        lb, la = (cb or '').split('\n'), (ca or '').split('\n')
                        mo, mn = OLD_B.match(lb[0]), NEW.match(la[0][9:]) if la[0].startswith('nearest: ') else None
                        if not (mo and mn and lb[1:] == la[1:] and mo.group('t') == mn.group('t') and mo.group('f') == mn.group('f')
                                and mo.group('o') == mn.group('o') and num(d.value) and old_inside(FO, float(d.value), mn.group('f'), mn.group('t'))):
                            bad.append((sh, d.coordinate, 'comment', cb, ca))
                            continue
                        cnt[sh + ' (comments)'] = cnt.get(sh + ' (comments)', 0) + 1
    for k, v in cnt.items():
        print(f'{k}: {v}')
    print('changed cells:', sum(cnt.values()), '| "— outside ±" digit-family texts left:', kept)
    print('mismatches:', len(bad))
    for z in bad[:15]:
        print('  ', z)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(*sys.argv[1:4]) else 1)
