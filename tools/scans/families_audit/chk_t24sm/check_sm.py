#!/usr/bin/env python3
"""T24 HORSE / JOCKEY S Sun, S Moon columns and the four Sun / Moon rows (Eddie, 4 Nov 2026): before vs after, cell by cell.
usage: check_sm.py before.xlsx after.xlsx
- every sheet except the runner sheets identical (values)
- runner sheets: every row outside the T24 HORSE / JOCKEY blocks identical (MATCH tables, SUMMARY incl.)
- T24 HORSE / JOCKEY: header and star rows = before with S Sun, S Moon cells after S Jupiter in each plane; old rows identical after the shift;
  the S Sun / S Moon cells = the SKY SUN / SKY MOON SKY block values (S Sun → S star); the four new rows recomputed from POSITIONS (own code);
  every new cell has a T24 comment"""
import sys
import openpyxl

PL = ('RA', 'Dec')


def rows(ws):                                              # trailing blank cells dropped (the sheet is wider after the change)
    out = []
    for r in ws.iter_rows(values_only=True):
        r = list(r)
        while r and r[-1] is None:
            r.pop()
        out.append(r + [None] * 200)
    return out


def d(p, q, pl):
    if pl == 'RA':
        x = abs(p[0] - q[0]) % 360
        return min(x, 360 - x)
    return abs(p[1] - q[1])


def positions(wb):
    out = {}
    for r in wb['POSITIONS'].iter_rows(values_only=True):
        if r and r[0] and len(r) > 6 and isinstance(r[5], (int, float)) and r[2] in ('S', 'H', 'J'):
            out[(r[0], r[2], r[3])] = (r[5], r[6])
    return out


def skyblock(wb, centre):
    ws = wb[f'SKY {centre.upper()}']
    out = {}
    for r in ws.iter_rows(values_only=True):
        if r[0] == 'SKY' and r[1] and str(r[1]).startswith(f'S {centre} → S '):
            x = str(r[1]).split(' → S ', 1)[1]
            out[(x, 'RA')], out[(x, 'Dec')] = r[2], r[11]
    return out


def main(bp, ap):
    B, A = openpyxl.load_workbook(bp, data_only=True), openpyxl.load_workbook(ap, data_only=True)
    bad, n = [], {'other rows': 0, 'old t24 rows': 0, 'new col cells': 0, 'new row cells': 0, 'blank': 0}
    assert B.sheetnames == A.sheetnames, 'sheet list'
    pos = positions(A)
    sky = {c: skyblock(A, c) for c in ('Sun', 'Moon')}
    for s in A.sheetnames:
        rb, ra = rows(B[s]), rows(A[s])
        if not s.startswith('P'):
            if rb != ra:
                bad.append(f'{s}: sheet differs')
            n['other rows'] += len(ra)
            continue
        wsA = A[s]
        i = j = 0
        while i < len(rb) or j < len(ra):
            x = rb[i] if i < len(rb) else None
            y = ra[j] if j < len(ra) else None
            if x and x[0] == 'T24' and x[1] and str(x[1]).startswith(('T24 HORSE', 'T24 JOCKEY')):
                C = 'H' if 'HORSE' in str(x[1]) else 'J'
                if not str(y[1]).startswith(str(x[1])[:10]) or 'S SUN, S MOON columns' not in str(y[1]):
                    bad.append(f'{s} r{j+1}: title')
                hb = rb[i + 2]; ha = ra[j + 2]          # body-name header row
                # positions of S Jupiter in before / after
                sjb = [k for k, v in enumerate(hb) if v == 'S Jupiter']
                sja = [k for k, v in enumerate(ha) if v == 'S Jupiter']
                if [ha[k + 1] for k in sja] != ['S Sun'] * 2 or [ha[k + 2] for k in sja] != ['S Moon'] * 2:
                    bad.append(f'{s} {C}: header S Sun / S Moon')
                def shift(r):                        # before row -> after layout (two blank cells after each S Jupiter column)
                    o = list(r[:sjb[0] + 1]) + [None, None] + list(r[sjb[0] + 1:sjb[1] + 1]) + [None, None] + list(r[sjb[1] + 1:])
                    return o
                bodies = [v for v in ha[2:sja[0]]]
                ib, ja = i + 1, j + 1
                # header rows
                for k in range(2):
                    sb, sa = shift(rb[ib + k]), ra[ja + k]
                    sa2 = list(sa); 
                    for kk in sja:
                        sa2[kk + 1] = sa2[kk + 2] = None
                    if sb[:len(sa2)] + [None] * (len(sa2) - len(sb)) != sa2[:max(len(sb), len(sa2))] and [v for v in sb if v is not None] != [v for v in sa2 if v is not None]:
                        bad.append(f'{s} {C}: header row {k}')
                ib += 2; ja += 2
                # Jupiter rows (4) identical after shift
                while str(rb[ib][1]) != 'stars':
                    sb = shift(rb[ib]); sa = ra[ja]
                    if [v for v in sb] != list(sa)[:len(sb)] + [None] * max(0, len(sb) - len(sa)):
                        if [v for v in sb if v is not None] != [v for v in sa if v is not None]:
                            bad.append(f'{s} {C}: Jupiter row {rb[ib][1]}')
                    ib += 1; ja += 1; n['old t24 rows'] += 1
                # four new rows
                P = s
                for lab in ('S Sun → S body', f'S Sun → {C} body', 'S Moon → S body', f'S Moon → {C} body'):
                    r = ra[ja]
                    if r[1] != lab:
                        bad.append(f'{s} {C}: expected row {lab}, got {r[1]}')
                    cen, tgt = lab[2:].split(' → ')[0], lab.split(' → ')[1][0]
                    for pi, pl in enumerate(PL):
                        c0 = 2 if pl == 'RA' else sja[0] + 4
                        for bi, b in enumerate(bodies):
                            v = r[c0 + bi]
                            key = ('SKY', 'S', b) if tgt == 'S' else (P, C, b)
                            if (tgt == 'S' and b == cen) or key not in pos:
                                if v is not None:
                                    bad.append(f'{s} {lab} {b} {pl}: should be blank')
                                n['blank'] += 1
                                continue
                            exp = d(pos[('SKY', 'S', cen)], pos[key], pl)
                            if v is None or abs(v - exp) > 1.5e-6:
                                bad.append(f'{s} {lab} {b} {pl}: {v} vs {exp}')
                            cell = wsA.cell(row=ja + 1, column=c0 + bi + 1)
                            if not cell.comment:
                                bad.append(f'{s} {lab} {b} {pl}: no comment')
                            n['new row cells'] += 1
                        for k in (n_ := len(bodies), n_ + 1, n_ + 2):
                            if r[c0 + k] is not None:
                                bad.append(f'{s} {lab}: sky column filled')
                    ja += 1
                if ra[ja][1] != 'stars' or rb[ib][1] != 'stars':
                    bad.append(f'{s} {C}: stars row')
                ib += 1; ja += 1
                # star rows
                while ib < len(rb) and rb[ib][0] == 'T24' and str(rb[ib][1])[:2] in ('H ', 'J '):
                    sb, sa = shift(rb[ib]), ra[ja]
                    star = str(sa[1])[2:]
                    if sa[1] != rb[ib][1]:
                        bad.append(f'{s} {C}: star row order')
                    sa2 = list(sa)
                    for pi, (pl, kk) in enumerate(zip(PL, sja)):
                        for k, cen in ((1, 'Sun'), (2, 'Moon')):
                            v = sa2[kk + k]
                            exp = sky[cen].get((star, pl))
                            if exp is None or v is None or abs(v - round(exp, 6)) > 1.5e-6:
                                bad.append(f'{s} {C} {star} {pl} S {cen}: {v} vs {exp}')
                            if not wsA.cell(row=ja + 1, column=kk + k + 1).comment:
                                bad.append(f'{s} {C} {star} {pl} S {cen}: no comment')
                            n['new col cells'] += 1
                            sa2[kk + k] = None
                    L = max(len(sb), len(sa2))
                    if sb + [None] * (L - len(sb)) != sa2 + [None] * (L - len(sa2)):
                        bad.append(f'{s} {C} {star}: old cells differ')
                    n['old t24 rows'] += 1
                    ib += 1; ja += 1
                i, j = ib, ja
                continue
            if x != y:
                bad.append(f'{s} r{j+1} (before r{i+1}): {str(x)[:80]} | {str(y)[:80]}')
                if len(bad) > 40: break
            n['other rows'] += 1
            i += 1; j += 1
    print(bp, '->', ap)
    print('counts:', ', '.join(f'{k} {v}' for k, v in n.items()))
    print('mismatches:', len(bad))
    for b in bad[:40]:
        print('   ', b)
    return not bad


if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
