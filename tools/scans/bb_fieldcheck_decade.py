"""Field check (17 Nov 2026, Eddie: 'and that is 10 * J Aldebaran Sun 4.4'; read-only; picks / won / by chance over the result races).
Arvico Bleu Sun: S Transpluto – S Sun RA 44.4467 ninth 44.4444 (97.51) = 10 x J Aldebaran – J Sun Dec 4.4380 ninth 4.44444 (27.16), and that
royal line is carried by S Rahu – S Ceres Dec 4.4445 (99.65).
  D0  a natal royal line c R – c X (number family) and a sky line naming sky X (S Y – S X, Y not the Moon) in the same family on the same
      digits a decade apart (target x10 or /10; any scores)
  D1  D0 with the sky line >= 90
  D2  D1 with the royal line carried by a sky pair ('Sky lines on the same target', number family)
  D3  D2 with X = the Sun
Runner-level; races = bb_fieldcheck_arvico.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as R
import bb_fieldcheck_arvico as A
RACES = A.RACES
NO = ('conj', 'contraparallel', 'opposition')
ok = lambda r: r.get('fam') and r['fam'] not in NO and r.get('sc') is not None
KEYS = ['D0', 'D1', 'D2', 'D3']


def tnum(r):
    try:
        return float(str(r['tgt']).replace('×φ', ''))
    except ValueError:
        return None


def decade(a, b):
    if a is None or b is None or min(a, b) <= 0:
        return False
    q = max(a, b) / min(a, b)
    return abs(q - 10) < 1e-3


def cases(D):
    out = {}
    for X, d in D.items():
        if X == 'Moon':
            continue
        sky = [o for o in d['O'] if ok(o) and ' – ' in o['line'] and o['line'].startswith('S ') and f'S {X}' in o['line'].split(' – ')
               and 'S Moon' not in o['line']]
        for x in d['L']:
            if ' – ' not in x['line'] or x['line'][0] not in 'HJ' or not ok(x):
                continue
            if x['line'].split(' – ')[0][2:] not in R.ROY:
                continue
            tag = f"{x['line']} {x['plane']}"
            carr = [p for p in d['S'] if p.get('match') == tag and ok(p) and ' – ' in p['line'] and '→' not in p['line']]
            for o in sky:
                if o['fam'] != x['fam'] or str(o['tgt']).endswith('φ') != str(x['tgt']).endswith('φ'):
                    continue
                if not decade(tnum(o), tnum(x)):
                    continue
                t = (f"{X}: {o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']}) / {tag} {x['v']:.4f} {x['tgt']} ({x['sc']})"
                     + (f"; carried by {carr[0]['line']} {carr[0]['plane']} {carr[0]['v']:.4f} ({carr[0]['sc']})" if carr else ''))
                out.setdefault('D0', []).append(t)
                if o['sc'] >= 90:
                    out.setdefault('D1', []).append(t)
                    if carr:
                        out.setdefault('D2', []).append(t)
                        if X == 'Sun': out.setdefault('D3', []).append(t)
    return out


def main():
    tot = {k: [0, 0, 0.0, []] for k in KEYS}
    for race, win in RACES:
        D = R.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        N = len(D)
        for run, data in D.items():
            cs = cases(data)
            for k in KEYS:
                if k in cs:
                    t = tot[k]; t[0] += 1; t[1] += win in run; t[2] += 1 / N
                    if win in run: t[3].append(f'{race} {run}')
            for k in ('D3', 'D2'):
                if k in cs:
                    print(f"  [{k}] {race} {run}{' WON' if win in run else ''}: {cs[k][0]}"); break
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k in KEYS:
        p, w, c, ws = tot[k]
        print(f'  {k}: {p} / {w} / {c:.1f}  {"; ".join(ws)}')


if __name__ == '__main__':
    main()
