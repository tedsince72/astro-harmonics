"""Field check (17 Nov 2026, from Kelso 14:50 4 May 2022 Domandlouis; read-only, prints picks / winners / by chance over the result races).
Items:
  F1   the same royal star on X in the sky and in a natal chart, same plane: S R – S X and c R – c X both in a number family >= 90
       (Domandlouis Mercury Fomalhaut RA 47×φ 95.8 / 16×φ 98.12; Jupiter Fomalhaut Dec 28 91.36 / 25×φ 93.18)
  F1x2 F1 on two or more bodies
  F2   a royal sky line S R – S X >= 90 in a family and a sky body line S Y -> c Z >= 90 on the same family + target (Domandlouis S Fomalhaut –
       S Mercury RA 76.046236 47×φ / S Mars -> H Quaoar RA 76.047737 47×φ 99.57)
  R11w a Regulus natal line with a same-body or crossed ratio on 11 >= 50 (R11 >= 90 is the watch item)
and each of Domandlouis's rules (BB2, BB3, BB6, BB14, BB23, BB28, BB35), then every pair and triple of the items and rules held by
Domandlouis, listing those with 2+ winners. Rule holders from bbrules json (watch-only left out) written to /tmp/mus/out by the caller."""
import json, sys, itertools, re, os
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_royal_cut as C
RACES = C.RACES + [('20220504_kelso_1450', 'Domandlouis')]
NO = ('conj', 'contraparallel', 'opposition')
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/mus/out'
RULES = ['BB2', 'BB3', 'BB6', 'BB14', 'BB23', 'BB28', 'BB35']


def star(line):
    return line.split(' – ')[0].split(' ', 1)[1]


def items(D):
    f1, f2, r11 = set(), False, False
    sky_tgts = []  # (fam, tgt) of S Y -> c Z >= 90, Y not a royal star
    for X, d in D.items():
        for s in d['O'] + d['S']:
            if '→' in s['line'] and s['fam'] and s['fam'] not in NO and (s['sc'] or 0) >= 90:
                sky_tgts.append((s['fam'], s['tgt'], s['plane'], s['line']))
    for X, d in D.items():
        for x in d['L']:
            if ' – ' not in x['line'] or x['line'][0] not in 'HJ':
                continue
            st = star(x['line'])
            if st not in C.ROY:
                continue
            if st == 'Regulus':
                for t, sc in ((x['rt'], x['rs']), (x['xt'], x['xs'])):
                    m = C.CUT.match(str(t or ''))
                    if m and m.group(1) == '11' and sc is not None and sc >= 50:
                        r11 = True
            if not x['fam'] or x['fam'] in NO or (x['sc'] or 0) < 90:
                continue
            for s in d['S'] + d['O']:
                if s['line'] == f'S {st} – S {X}' and s['plane'] == x['plane'] and s['fam'] and s['fam'] not in NO and (s['sc'] or 0) >= 90:
                    f1.add(X)
        for s in d['S'] + d['O']:
            if s['line'].startswith('S ') and ' – S ' in s['line'] and s['line'].split(' – ')[0][2:] in C.ROY and s['fam'] \
                    and s['fam'] not in NO and (s['sc'] or 0) >= 90:
                if any(f == s['fam'] and t == s['tgt'] and p == s['plane'] for f, t, p, _ in sky_tgts):
                    f2 = True
    out = set()
    if f1: out.add('F1')
    if len(f1) >= 2: out.add('F1x2')
    if f2: out.add('F2')
    if r11: out.add('R11w')
    return out


def main():
    rows = []
    for race, win in RACES:
        data = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        J = json.load(open(f'{OUT}/{race}_bbrules.json'))['rules']
        N = len(data)
        for run, D in data.items():
            held = items(D) | {k for k in RULES if any(c['runner'] == run and not c['watch_only'] for c in J.get(k, []))}
            rows.append((race, run, win in run, N, held))
    keys = ['F1', 'F1x2', 'F2', 'R11w'] + RULES
    def tally(cmb):
        h = [r for r in rows if set(cmb) <= r[4]]
        return len(h), sum(r[2] for r in h), sum(1 / r[3] for r in h), [r[1] for r in h if r[2]]
    print('## Single items (picks / won / by chance)')
    for k in keys:
        p, w, c, ws = tally((k,))
        print(f'  {k}: {p} / {w} / {c:.1f}  {", ".join(ws)}')
    dl = next(r[4] for r in rows if 'Domandlouis' in r[1])
    print('\n## Domandlouis holds:', ', '.join(k for k in keys if k in dl))
    print('\n## Pairs and triples of his items with 2+ winners (by winners / chance)')
    res = []
    for n in (2, 3):
        for cmb in itertools.combinations([k for k in keys if k in dl], n):
            p, w, c, ws = tally(cmb)
            if w >= 2:
                res.append((w / c, cmb, p, w, c, ws))
    for _, cmb, p, w, c, ws in sorted(res, reverse=True):
        print(f'  {" + ".join(cmb)}: {p} / {w} / {c:.1f}  {", ".join(ws)}')


if __name__ == '__main__':
    main()
