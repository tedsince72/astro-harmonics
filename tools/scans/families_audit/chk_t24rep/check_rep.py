"""check_rep.py (Eddie, 22 Oct 2026: T24 repeats flag): BEFORE.xlsx AFTER.xlsx
- every repeats cell of T24 SKY / HORSE / JOCKEY recomputed from POSITIONS (own code; families.evaluate for the targets): each body cell's
  best target (RA wrapped 0-180, Dec |dDec|; cells inside the conjunction range RA < 1.5 / Dec < 0.3 and conjunction bests left out), every
  target (family + target number, no folding) in >= 2 cells, cells by score (ties RA before Dec, body order), targets by cell count then the
  highest score: text, none missing or extra;
- dotted outline exactly on repeated cells (thick kept where a midpoint outline was), comment = before + one 'repeat: ...' line per target;
- title = before + the counts; header + 'repeats'; every other cell of every sheet identical (values, fills, comments, borders, formats).
Prints per block rows with a repeat / rows, targets, largest xn, and 'mismatches: n'."""
import sys, openpyxl
sys.path.insert(0, 'tools')
import families

CONJ = {'RA': 1.5, 'Dec': 0.3}
NOTE_NEW = ('comment line. REPEATS (22 Oct 2026): the same best target (family and target number, no x10 / /10 folding; conjunction cells '
            'left out) in two or more body cells of a row, any planes - listed in the "repeats" column (most cells first, then by the highest '
            'score), dotted outline and a comment line on each repeated cell (a midpoint thick outline kept). No timing, no +5')


def d(p, q, pl):
    if pl == 'RA':
        x = abs(p[0] - q[0]) % 360
        return 360 - x if x > 180 else x
    return abs(p[1] - q[1])


def sig(c):
    b = c.border
    return (c.value, c.fill.start_color.rgb if c.fill and c.fill.fill_type else None, c.comment.text if c.comment else None,
            tuple(getattr(b, s).style if b and getattr(b, s) else None for s in ('left', 'right', 'top', 'bottom')), c.number_format)


def expect(pos, star, bodies):
    best = {}
    for pl in ('RA', 'Dec'):
        for b in bodies:
            v = d(pos[star], pos[b], pl)
            ev = families.evaluate(v, pl, 'deg')
            if not ev or v < CONJ[pl] or ev[0]['family'] == 'conj':
                continue
            best[(b, pl)] = (f"{ev[0]['target']} {ev[0]['family']}", ev[0]['score'])
    g = {}
    for (b, pl), (k, sc) in best.items():
        g.setdefault(k, []).append((b, pl, sc))
    reps = [(k, sorted(c, key=lambda z: (-z[2], ('RA', 'Dec').index(z[1]), bodies.index(z[0])))) for k, c in g.items() if len(c) >= 2]
    reps.sort(key=lambda kc: (-len(kc[1]), -kc[1][0][2]))
    return reps


def main(fb, fa):
    wb, wa = openpyxl.load_workbook(fb), openpyxl.load_workbook(fa)
    bad, rep = [], []
    pos = {}
    for x in wa['POSITIONS'].iter_rows(min_row=5, values_only=True):
        if x and x[2] in ('S', 'H', 'J') and x[3] and isinstance(x[5], (int, float)):
            pos[(x[0], x[2], x[3])] = (x[5], x[6])
    for sh in wa.sheetnames:
        sb, sa = wb[sh], wa[sh]
        if sb.max_row != sa.max_row:
            bad.append((sh, 'row count', sb.max_row, sa.max_row))
        rb, ra = list(sb.iter_rows()), list(sa.iter_rows())
        allowed = set()                                    # (row, col) cells checked below
        i = 0
        while i < len(ra):
            r = ra[i]
            t = str(r[1].value or '')
            if r[0].value == 'T24' and t.startswith(('T24 SKY', 'T24 HORSE', 'T24 JOCKEY')):
                C = 'S' if t.startswith('T24 SKY') else 'H' if t.startswith('T24 HORSE') else 'J'
                who = 'SKY' if C == 'S' else sh
                h1, h2 = ra[i + 1], ra[i + 2]
                names = [c.value for c in h2]
                cmid = [k for k, c in enumerate(h1) if c.value in ('RA midpoints', 'Dec midpoints')]
                n = cmid[0] - 2
                bodies = names[2:2 + n]
                c0 = {'RA': 2, 'Dec': cmid[0] + 1}
                crep = cmid[1] + 1
                if h1[crep].value != 'repeats' or len([c for c in h1 if c.value is not None]) != len([c for c in rb[i + 1] if c.value is not None]) + 1:
                    bad.append((sh, C, 'header'))
                for hr in (i + 1, i + 2):
                    allowed.add((hr, crep))
                j, nrows, nrep, ntgt, big = i + 3, 0, 0, 0, (0, None)
                while j < len(ra) and ra[j][0].value == 'T24' and str(ra[j][1].value).startswith(f'{C} '):
                    star = ra[j][1].value[2:]
                    P = 'SKY' if C == 'S' else sh
                    pp = {b: pos[(P, C, b)] for b in bodies + [star]}
                    reps = expect(pp, star, bodies)
                    want = '; '.join(f"{k} ×{len(c)} (" + ', '.join(f'{b} {pl} ({sc:.2f})' for b, pl, sc in c) + ')' for k, c in reps) or None
                    if ra[j][crep].value != want:
                        bad.append((sh, C, star, 'repeats', ra[j][crep].value, want))
                    allowed.add((j, crep))
                    lines = {}
                    for k, c in reps:
                        for b, pl, sc in c:
                            lines.setdefault((b, pl), []).append(f"repeat: {k} ×{len(c)} (with " + ', '.join(f'{b2} {p2} ({s2:.2f})' for b2, p2, s2 in c if (b2, p2) != (b, pl)) + ')')
                    for pl in ('RA', 'Dec'):
                        for k, b in enumerate(bodies):
                            col = c0[pl] + k
                            cb_, ca_ = sig(rb[j][col]), sig(ra[j][col])
                            allowed.add((j, col))
                            wc = cb_[2] + ''.join('\n' + l for l in lines.get((b, pl), []))
                            wbd = cb_[3] if (b, pl) not in lines or cb_[3][0] == 'thick' else ('dotted',) * 4
                            if (ca_[0], ca_[1], ca_[2], ca_[3], ca_[4]) != (cb_[0], cb_[1], wc, wbd, cb_[4]):
                                bad.append((sh, C, star, b, pl, 'cell', ca_[2:4], (wc, wbd)))
                    nrows += 1
                    if reps:
                        nrep += 1; ntgt += len(reps)
                        m = max(reps, key=lambda kc: len(kc[1]))
                        if len(m[1]) > big[0]:
                            big = (len(m[1]), f'{star}: {m[0]}')
                    j += 1
                wt = (rb[i][1].value.replace('comment line. No timing, no +5', NOTE_NEW)
                      + f'. REPEATS (22 Oct 2026): {nrep} of {nrows} rows with a repeat, {ntgt} repeated targets')
                if ra[i][1].value != wt:
                    bad.append((sh, C, 'title', ra[i][1].value[-120:], wt[-120:]))
                allowed.add((i, 1))
                rep.append(f'{sh} T24 {"SKY" if C == "S" else "HORSE" if C == "H" else "JOCKEY"}: {nrep} / {nrows} rows, {ntgt} targets, largest ×{big[0]} ({big[1]})')
                i = j
                continue
            i += 1
        for ii, (x, y) in enumerate(zip(rb, ra)):
            for k in range(max(len(x), len(y))):
                if (ii, k) in allowed:
                    continue
                cx = sig(x[k]) if k < len(x) else (None, None, None, (None,) * 4, 'General')
                cy = sig(y[k]) if k < len(y) else (None, None, None, (None,) * 4, 'General')
                if cx != cy:
                    bad.append((sh, ii + 1, k + 1, 'other cell', cx[:3], cy[:3]))
                    break
    for x in rep:
        print(x)
    print('mismatches:', len(bad))
    for x in bad[:10]:
        print('  ', x)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
