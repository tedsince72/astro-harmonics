"""compare_half.py (Eddie, 24 Oct 2026: half family + 4-digit rule in tools/families.py): OLD_FAMILIES_DIR BEFORE.xlsx AFTER.xlsx [--json out]
BEFORE = the tables workbook built with the families.py of OLD_FAMILIES_DIR (commit 83850b1c), AFTER = built now. jupiter_tables.py itself
changed in one line only (NUM_FAMILIES + 'half'), so every difference must come from the family change. Checks:
(1) every distance target cell - '<target> (<family>)' / '... — outside ±tol' with its value 1 or 2 cells left (T1–T9, T23, SKY block,
    T1 / T2 SKY cells), every '→ <target> (<family>, <score>)' / 'no family' leg cell (T17–T22, SKY PAIRS ...), every T24 grid / T24 H / J
    distance cell (comment first line, fill): BEFORE = the old families on the shown value, AFTER = the new ones; tallies how each changed
    (lost digit hit, new half hit, best family changed, nearest target changed);
(2) every row of every sheet: rows aligned in order (difflib); a row that is not identical must hold at least one value whose evaluation
    differs between the old and the new families (numbers in cells, texts and comments); title rows may differ in their digits only.
Prints the tallies, hits per family (T1, T2, T24 SKY / HORSE / JOCKEY natal cells, SKY block), the timeline event counts and THREADS lines."""
import sys, os, re, json, difflib, importlib.util, math
import openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
import families as FN                                                    # noqa: E402  (tools/ on the path via the runner)


def load_old(d):
    spec = importlib.util.spec_from_file_location('families_old', os.path.join(d, 'families.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


FAMS = ('whole', 'half', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver', 'conj')
TGT = re.compile(r'^(.+) \((whole|half|golden|phi power|ninth|sqrt2|silver|conj)\)( — outside ±([0-9.e-]+))?$')
LEG = re.compile(r'^→ (.+) \((whole|half|golden|phi power|ninth|sqrt2|silver|conj), ([0-9.]+)\)')
NUM = re.compile(r'(?<![\w.])-?\d+\.\d+')
PLANES = ('RA', 'Dec', None)


def tlabel(d):
    return f"{d['target']} ({d['family']})"


def out_text(d):
    return f"{tlabel(d)} — outside ±{d['tol']:.3g}"


EPS = 5e-7                                                 # the shown value is rounded to 6 dp


def expect(F, v):
    """the acceptable target texts (any plane: the conjunction depends on it; v and v +- 5e-7: the shown value is rounded) ->
    {text: (family, [scores])}"""
    out = {}
    for x in (v, v - EPS, v + EPS):
        for pl in PLANES:
            ev = F.evaluate(x, pl, 'deg')
            if ev:
                out.setdefault(tlabel(ev[0]), (ev[0]['family'], []))[1].append(ev[0]['score'])
            else:
                o = F.outside(x, pl, 'deg')
                if o:
                    out.setdefault(out_text(o), (None, []))
    return out


def score_ok(shown, scores):
    return min(scores) - 0.006 <= shown <= max(scores) + 0.006


def bests(F, v):
    """[(best or None, outside or None)] over the planes and v +- 5e-7"""
    return [FN_or(F, x, pl) for x in (v, v - EPS, v + EPS) for pl in PLANES]


def sig_eval(F, v):
    r = []
    for pl in ('RA', 'Dec', None):
        r.append(tuple((d['family'], d['target'], round(d['score'], 6)) for d in F.evaluate(v, pl, 'deg')))
        o = F.outside(v, pl, 'deg')
        r.append(o and (o['family'], o['target']))
    return tuple(r)


class Cmp:
    def __init__(self, fo):
        self.fo, self.memo = fo, {}

    def changed(self, v):
        """the old and new families evaluate v (or v +- 5e-7, display rounding) differently"""
        if v is None or v <= 0 or v > 400:
            return False
        if v not in self.memo:
            self.memo[v] = any(sig_eval(self.fo, x) != sig_eval(FN, x) for x in (v, v - 5e-7, v + 5e-7) if x > 0)
        return self.memo[v]


def nums(cells):
    out = []
    for v, com in cells:
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            out.append(float(v))
        for s in (v if isinstance(v, str) else None, com):
            if s:
                out += [abs(float(x)) for x in NUM.findall(s)]
    return out


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def fill(c):
    return c.fill.start_color.rgb if c.fill and c.fill.fill_type else None


def cell_checks(ws, F, tag, tally, hits, bad, sheet):
    """(1): every target / leg / T24 cell of one workbook against the families F; returns {(row, col): (family, score) or ('out', target)}"""
    res = {}
    t24 = None
    for r in ws.iter_rows():
        a = r[0].value
        if a in ('T24', 'T24 H / J') and r[1].value in ('RA', 'table', 'star'):
            pass
        for j, c in enumerate(r):
            v = c.value
            if isinstance(v, str):
                m = TGT.match(v)
                if m and j >= 2:
                    p1, p2 = r[j - 1].value, r[j - 2].value
                    val = p2 if is_num(p2) and (p1 is None or is_num(p1)) else p1
                    if not is_num(val):
                        continue
                    ex = expect(F, float(val))
                    if v not in ex:
                        bad.append((sheet, tag, 'target', c.coordinate, val, v, list(ex)[:2]))
                        continue
                    fam, scs = ex[v]
                    shown = r[j + 3].value if j + 3 < len(r) else None
                    if fam and shown is not None and is_num(shown) and not score_ok(shown, scs):
                        bad.append((sheet, tag, 'score', c.coordinate, val, shown, scs))
                    put(res, (rkey(r), c.column), (fam, round(scs[0], 2)) if fam else ('out', m.group(1)))
                    tbl = a if isinstance(a, str) and len(a) < 12 else None
                    if fam and tbl in ('T1', 'T2') and j in (4, 12):
                        hits.setdefault((tbl, fam), 0); hits[(tbl, fam)] += 1
                    if fam and tbl == 'SKY' and sheet == 'SKY JUPITER':
                        hits.setdefault(('SKY block', fam), 0); hits[('SKY block', fam)] += 1
                    continue
                m = LEG.match(v)
                if (m or v == 'no family') and j >= 1 and is_num(r[j - 1].value):
                    val = float(r[j - 1].value)
                    ev = [F.evaluate(x, pl, 'deg') for x in (val, val - EPS, val + EPS) for pl in PLANES]
                    if v == 'no family':
                        if all(e for e in ev):
                            bad.append((sheet, tag, 'leg none', c.coordinate, val, [e[0]['target'] for e in ev]))
                        put(res, (rkey(r), c.column), ('none', None))
                    else:
                        sc_ = [e[0]['score'] for e in ev if e and e[0]['target'] == m.group(1) and e[0]['family'] == m.group(2)]
                        ok = bool(sc_) and score_ok(float(m.group(3)), sc_)
                        if not ok:
                            bad.append((sheet, tag, 'leg', c.coordinate, val, v, [e and (e[0]['target'], round(e[0]['score'], 2)) for e in ev]))
                        put(res, (rkey(r), c.column), (m.group(2), float(m.group(3))))
            elif is_num(v) and c.comment and a in ('T24', 'T24 H / J') and isinstance(r[1].value, str):
                line = c.comment.text.split('\n')[0]
                pl = None
                val = float(v)
                ev = None
                # the T24 comment: 'target · family · offset · score' / '0 · conjunction (RA < 1.5) · ...' / 'nearest: t · fam — outside ±tol · off'
                parts = line.split(' · ')
                fam0 = line[9:].split(' — ')[0].split(' · ')[-1] if line.startswith('nearest: ') else parts[1] if len(parts) > 1 else ''
                if not (fam0 in FAMS or fam0.startswith('conjunction')):
                    continue                                               # a ratio cell (T24 H / J): not a distance
                if line.startswith('nearest: '):
                    tgt, fam = line[9:].split(' — ')[0].split(' · ')
                    exs = bests(F, val)
                    if not any(e and e[0] is None and e[1]['target'] == tgt and e[1]['family'] == fam for e in exs):
                        bad.append((sheet, tag, 'T24 nearest', c.coordinate, val, line))
                    put(res, (rkey(r), c.column), ('out', tgt))
                    if fill(c) not in (None, 'FFFF8080', '00FF8080'):
                        bad.append((sheet, tag, 'T24 outside fill', c.coordinate, fill(c)))
                else:
                    parts = line.split(' · ')
                    fam = 'conj' if parts[1].startswith('conjunction') else parts[1]
                    tgt, sc = parts[0], float(parts[-1])
                    exs = bests(F, val)
                    sc_ = [e[0]['score'] for e in exs if e and e[0] and e[0]['family'] == fam and (fam == 'conj' or e[0]['target'] == tgt)]
                    if not (sc_ and score_ok(sc, sc_)):
                        bad.append((sheet, tag, 'T24 hit', c.coordinate, val, line))
                    put(res, (rkey(r), c.column), (fam, sc))
                    if a == 'T24':
                        blk = 'T24 SKY' if sheet == 'SKY JUPITER' else 'T24 HORSE' if r[1].value.startswith('H ') else 'T24 JOCKEY'
                        hits.setdefault((blk, fam), 0); hits[(blk, fam)] += 1
    return res


DUP = ('dup', None)


def put(res, k, v):
    """a key seen twice (rows with the same first cells) is ambiguous: left out of the change tally"""
    res[k] = DUP if k in res else v


def rkey(r):
    """a row's key: its first four cells (table id, labels, plane)"""
    return tuple(c.value if isinstance(c.value, str) else None for c in r[:4])


def FN_or(F, v, pl):
    ev = F.evaluate(v, pl, 'deg')
    return (ev[0], None) if ev else (None, F.outside(v, pl, 'deg'))


def rowsig(r):
    return tuple((c.value, fill(c), c.comment.text if c.comment else None) for c in r)


def trim(t):
    while t and t[-1] == (None, None, None):
        t = t[:-1]
    return t


def is_title(t):
    a = t[0][0] if t else None
    return isinstance(a, str) and (len(a) > 40 or a.endswith(':')) and all(x == (None, None, None) for x in t[1:])


TLS = ('TIMELINE', 'LONG TIMELINE', 'STAR TIMELINE', 'LONG STAR TIMELINE', 'TIMELINE H', 'TIMELINE J', 'LONG TIMELINE H', 'LONG TIMELINE J',
       'STAR TIMELINE H', 'STAR TIMELINE J', 'LONG STAR TIMELINE H', 'LONG STAR TIMELINE J')


def digits_only(x, y):
    """two rows that differ only in the digits of their texts (section / count rows), no number cells differing"""
    if len(x) != len(y):
        return False
    for c, d in zip(x, y):
        if c == d:
            continue
        if not (isinstance(c[0], str) and isinstance(d[0], str)) or re.sub(r'\d+', '#', c[0]) != re.sub(r'\d+', '#', d[0]) or c[1:] != d[1:]:
            return False
    return True


def rkey2(sh, t):
    """pairing key of a changed row: T-table rows table id + label; NUMBERS rows family + the digits of the first target form (the forms
    folded x10 / /10 are listed in the label, so a lost form changes it); other sheets the row label"""
    if sh == 'SKY JUPITER' or re.fullmatch(r'P\d\d', sh):
        return tuple(c[0] for c in t[:2])
    a = t[0][0] if t else None
    if sh.endswith('NUMBERS') and isinstance(a, str) and ': ' in a:
        fam, forms = a.split(': ', 1)
        f0 = forms.split(' / ')[0]
        mp = re.fullmatch(r'(?:(\d+)×)?φ\^(-?\d+)', f0)
        if mp:                                                          # a φ power form: the digits of its value
            x = float(mp.group(1) or 1) * FN.PHI ** int(mp.group(2))
            return fam, round(x / 10 ** math.floor(math.log10(x)), 4)
        m = NUM.search(forms)
        if m:
            x = float(m.group())
            return fam, round(x / 10 ** math.floor(math.log10(x)), 4)
        return fam, forms.split(' / ')[0]
    return (a,)


def threads_same(t, u):
    """THREADS: the two rows differ only in their '+ n weaker' lines (hits under 50 are not listed, so their values cannot be shown)"""
    if len(t) != len(u):
        return False
    norm = lambda v: '\n'.join(ln for ln in str(v or 'directions 0').split('\n') if not ln.startswith('+ '))
    return all(c == d or norm(c[0]) == norm(d[0]) and c[2] == d[2] for c, d in zip(t, u))


def row_checks(wb, wa, cmp, bad, counts):
    """(2): rows aligned in order; every row that is not identical holds a changed value (with the rows of the same key on the other
    side), or differs in digits only (titles, section and count rows), or (THREADS) only in its '+ n weaker' line, or is a timeline row
    whose relationship sits in a changed source row of the same sheet (an event that came or went with its source row)"""
    for sh in wa.sheetnames:
        rb = [trim(rowsig(r)) for r in wb[sh].iter_rows()]
        ra = [trim(rowsig(r)) for r in wa[sh].iter_rows()]
        sm = difflib.SequenceMatcher(None, rb, ra, autojunk=False)
        nch = nadd = ndel = 0
        db, da = [], []
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal':
                continue
            db += rb[i1:i2]; da += ra[j1:j2]
            nch += min(i2 - i1, j2 - j1); ndel += max(0, (i2 - i1) - (j2 - j1)); nadd += max(0, (j2 - j1) - (i2 - i1))
        sb, sa = set(rb), set(ra)
        kb, ka = {}, {}
        for t in db:
            kb.setdefault(rkey2(sh, t), []).append(t)
        for t in da:
            ka.setdefault(rkey2(sh, t), []).append(t)
        pend, src = [], set()
        for side, other, osig in ((db, ka, sa), (da, kb, sb)):
            for t in side:
                if t in osig:
                    continue                                            # reordered, unchanged
                peers = other.get(rkey2(sh, t), [])
                if is_title(t) or any(digits_only(t, u) for u in peers) or (len(t) > 3 and isinstance(t[3][0], str) and t[3][0].startswith('———')):
                    continue
                if sh == 'THREADS' and any(threads_same(t, u) for u in peers):
                    continue
                vals = nums([(c[0], c[2]) for u in [t] + peers for c in u])
                if any(cmp.changed(v) for v in vals):
                    if t[0][0] not in TLS:
                        src.update(c[0] for c in t if isinstance(c[0], str))
                    continue
                pend.append(t)
        for t in pend:
            rel = t[4][0] if t[0][0] in TLS and len(t) > 4 else None
            if rel and any(rel in s_ or s_.endswith(rel.split(': ')[-1]) for s_ in src):
                continue
            bad.append((sh, 'row without a changed value', [c[0] for c in t][:8]))
        counts[sh] = (len(rb), len(ra), nch, ndel, nadd)


def tl_counts(wb):
    out = {}
    for sh in wb.sheetnames:
        if sh != 'SKY JUPITER' and not re.fullmatch(r'P\d\d', sh):
            continue
        for r in wb[sh].iter_rows(max_col=1, values_only=True):
            a = r[0]
            if isinstance(a, str):
                m = re.match(r'^((?:LONG )?(?:STAR )?TIMELINE(?: [HJ])?) \(.*?: (\d+) events', a)
                if m:
                    out[f'{sh} {m.group(1)}'] = int(m.group(2))
    return out


def threads(wb):
    if 'THREADS' not in wb.sheetnames:
        return None
    lines = weaker = 0
    for r in wb['THREADS'].iter_rows(min_row=4, values_only=True):
        for v in r[1:]:
            if isinstance(v, str) and '\n' in v or isinstance(v, str) and v.startswith(('directions', 'mutual', 'both')):
                for ln in v.split('\n')[1:]:
                    m = re.match(r'\+ (\d+) weaker', ln)
                    if m:
                        weaker += int(m.group(1))
                    elif ln.strip():
                        lines += 1
    return lines, weaker


verbose = '-v' in sys.argv


def main(old_dir, fb, fa, jout=None):
    fo = load_old(old_dir)
    cmp = Cmp(fo)
    wb, wa = openpyxl.load_workbook(fb), openpyxl.load_workbook(fa)
    bad, hb, ha, tally, ex_ = [], {}, {}, {}, {}
    for sh in wa.sheetnames:
        if sh in ('POSITIONS',):
            continue
        cb = cell_checks(wb[sh], fo, 'before', tally, hb, bad, sh)
        ca = cell_checks(wa[sh], FN, 'after', tally, ha, bad, sh)
        if sh == 'SKY JUPITER' or re.fullmatch(r'P\d\d', sh):
            # how each fixed-layout cell changed (rows that keep their position: T1-T9, T23, T24, SKY block)
            for k in set(cb) & set(ca):
                x, y = cb[k], ca[k]
                if x == y or DUP in (x, y):
                    continue
                if x[0] in FAMS and y[0] in ('out', 'none'):
                    kind = f'lost {x[0]} hit'
                elif y[0] == 'half' and x[0] != 'half':
                    kind = 'new half hit' + (' (was ' + x[0] + ')' if x[0] in FAMS else '')
                elif x[0] in FAMS and y[0] in FAMS and x[0] != y[0]:
                    kind = f'best {x[0]} -> {y[0]}'
                elif x[0] == 'out' and y[0] == 'out':
                    kind = 'nearest target changed' + (' (to half)' if False else '')
                elif x == y:
                    continue
                else:
                    kind = f'other {x[0]} -> {y[0]}'
                tally[kind] = tally.get(kind, 0) + 1
                ex_.setdefault(kind, []).append((sh, k[0][:3], k[1], x, y))
    counts = {}
    row_checks(wb, wa, cmp, bad, counts)
    tb, ta = tl_counts(wb), tl_counts(wa)
    print('cell changes (fixed-layout cells, same position):')
    for k in sorted(tally, key=lambda k: -tally[k]):
        print(f'  {k}: {tally[k]}' + ('   e.g. ' + '; '.join(str(e) for e in ex_[k][:2]) if 'conj' in k or verbose else ''))
    print('hits per family (before -> after):')
    for blk in ('T1', 'T2', 'T24 SKY', 'T24 HORSE', 'T24 JOCKEY', 'SKY block'):
        print(f'  {blk}: ' + ', '.join(f"{f} {hb.get((blk, f), 0)} -> {ha.get((blk, f), 0)}" for f in FAMS))
    print('timeline events (before -> after):')
    for k in tb:
        print(f'  {k}: {tb[k]} -> {ta.get(k)}')
    print('THREADS lines >= 50, + n weaker (before -> after):', threads(wb), '->', threads(wa))
    print('rows per sheet (before, after, changed, removed, added):')
    for sh, c in counts.items():
        if c[2] or c[3] or c[4]:
            print(f'  {sh}: {c}')
    print('mismatches:', len(bad))
    for x in bad[:20]:
        print('  ', x)
    if jout:
        json.dump({'tally': tally, 'hits_before': {f'{k[0]}|{k[1]}': v for k, v in hb.items()},
                   'hits_after': {f'{k[0]}|{k[1]}': v for k, v in ha.items()}, 'tl_before': tb, 'tl_after': ta,
                   'threads': [threads(wb), threads(wa)], 'counts': counts, 'bad': len(bad)}, open(jout, 'w'), indent=1)
    return not bad


if __name__ == '__main__':
    a = sys.argv[1:]
    j = a[a.index('--json') + 1] if '--json' in a else None
    a = [x for x in a if x not in ('--json', j, '-v')]
    sys.exit(0 if main(*a, jout=j) else 1)
