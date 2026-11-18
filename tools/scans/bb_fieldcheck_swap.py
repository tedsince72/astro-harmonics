"""Field check (18 Nov 2026, from Eddie's Sir Chauvelin lines, Newcastle AW 12:20 12 Nov 2021; read-only).
Swap: S Y -> c X and S X -> c Y in the same chart c (H or J), both in a family (no conj / cp / opposition), Y not X, no Moon.
  W80   both >= 80
  W80c  W80 and S X - S Y conjunct in the sky (RA < 1.5 or Dec < 0.3)
  W80s  W80 and S X - S Y in a number family (any plane, any score)
  W80n  W80 and no sky line between X and Y
  W50   both >= 50; W50c, W50s, W50n likewise
Runner-level; races = bb_scan_negatives.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_scan_negatives as NEG
NO = ('conj', 'contraparallel', 'opposition')
KEYS = [f'W{c}{s}' for c in (80, 50) for s in ('', 'c', 's', 'n')]


def cases(D):
    on, sky = {}, {}
    for X, d in D.items():
        for r in d['L'] + d['O']:
            ln, sc = r['line'], r.get('sc')
            if sc is None or not ln.startswith('S '):
                continue
            if ' → ' in ln:
                y, t = ln[2:].split(' → ')
                if r['fam'] in NO or y in ('Moon', X) or t[2:] != X:
                    continue
                k = (y, t[0], X)
                on[k] = max(on.get(k, 0), sc)
            elif ' – ' in ln:
                a, b = [s[2:] for s in ln.split(' – ')]
                k = frozenset((a, b))
                sky.setdefault(k, set()).add('c' if r['fam'] == 'conj' else 's' if r['fam'] not in NO else 'o')
    out = {}
    for (y, c, x), s1 in on.items():
        s2 = on.get((x, c, y))
        if s2 is None or y > x:
            continue
        sk = sky.get(frozenset((x, y)), set())
        tag = f'{c} {x} / {y} ({s2:.1f} / {s1:.1f}) sky {"+".join(sorted(sk)) or "none"}'
        for cut in (80, 50):
            if min(s1, s2) >= cut:
                out.setdefault(f'W{cut}', []).append(tag)
                for s, ok in (('c', 'c' in sk), ('s', 's' in sk), ('n', not sk)):
                    if ok: out.setdefault(f'W{cut}{s}', []).append(tag)
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for race, win in NEG.RACES:
        D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        N = len(D)
        for run, data in D.items():
            cs = cases(data)
            for k in KEYS:
                if k in cs:
                    t = tot[k]; t[0] += 1; t[1] += win in run; t[2] += 1 / N
                    if win in run: t[3].append(f'{race} {run}')
    print(f'## Totals over {len(NEG.RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}' + (f'   {"; ".join(ws)}' if len(ws) <= 4 else ''))


if __name__ == '__main__':
    main()
