"""Scan (18 Nov 2026, Eddie: 'sky activation may override the negative aspect'; read-only).
Sky-on-natal pairs S Y -> natal X (bb_scan_sky_on_natal: any family >= cut), labelled positive / negative / neutral (held elsewhere, neither) / unseen (held in no other race) from the OTHER result races
(leave one out). Each holding is split by whether the sky pair S Y - S X scores (conj, or a number family; any plane, any score) - 'activated'
- or not. Per group: holdings / won / by chance (1 / field size each). Races = bb_scan_negatives.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_sky_on_natal as S
import bb_scan_negatives as NEG


def skypairs(D):
    out = set()
    for X, d in D.items():
        for r in d['O']:
            ln = r['line']
            if r.get('sc') is not None and ln.startswith('S ') and ' – ' in ln and r['fam'] not in ('contraparallel', 'opposition'):
                a, b = [s[2:] for s in ln.split(' – ')]
                out.add(frozenset((a, b)))
    return out


def main():
    raw = [(race, win, E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')) for race, win in NEG.RACES]
    data = [(race, win, None, {run: S.pairs(D) for run, D in R.items()}) for race, win, R in raw]
    act = {(race, run): skypairs(D) for race, win, R in raw for run, D in R.items()}
    for v in [('any', 90), ('any', 80)]:
        g = {}
        for race, win, R in raw:
            st = S.tally(data, v, skip=race)
            N = len(R)
            for run, D in R.items():
                for k in S.pairs(D)[v]:
                    lab = (S.label(st[k][1], st[k][2]) or 'neutral') if k in st else 'unseen'
                    a = 'activated' if frozenset(k) in act[(race, run)] else 'not activated'
                    t = g.setdefault((lab, a), [0, 0, 0.0]); t[0] += 1; t[1] += win in run; t[2] += 1 / N
        print(f'## {v[0]} >= {v[1]} (labels leave-one-out; holdings / won / by chance)')
        for k in sorted(g):
            h, w, c = g[k]
            print(f'  {k[0]:8} {k[1]:13}: {h} / {w} / {c:.1f}')


if __name__ == '__main__':
    main()
