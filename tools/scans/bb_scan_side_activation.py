"""Scan (18 Nov 2026, Eddie: a sky-on-natal pair S Y -> natal X NOT activated in the sky (S Y - S X does not score), but one end has a sky
activation to another body - does that deepen the pair's effect, or neutralise it, depending on the pair's nature? read-only).
Holdings as bb_scan_negative_activated (S Y -> H / J X, any family >= cut; labels positive / negative / neutral / unseen leave-one-out).
Not-activated holdings split by side links in the race's sky (S A - S B scoring, conj or number family, any plane; pairs from every runner's
bybody rows): 'Y side' = S Y - S Z scores for some Z not X; 'X side' = S X - S Z scores for some Z not Y; 'both', 'neither'. Also: side link
to a royal star only / to a body; and 'shared Z' = one Z linked to both S Y and S X (a sky triangle closed through Z).
Per group: holdings / won / by chance (1 / field size each); ratio won / chance.
  python3 tools/scans/bb_scan_side_activation.py"""
import sys
SIDE = float(sys.argv[1]) if len(sys.argv) > 1 else 0   # side-link score floor (0 = any); activation of S Y - S X stays any score
del sys.argv[1:]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_sky_on_natal as S
import bb_scan_negatives as NEG
from bb_scan_negative_activated import skypairs


def strong(D, cut):
    out = set()
    for X, d in D.items():
        for r in d['O']:
            ln = r['line']
            if r.get('sc') is not None and r['sc'] >= cut and ln.startswith('S ') and ' – ' in ln and r['fam'] not in ('contraparallel', 'opposition'):
                a, b = [t[2:] for t in ln.split(' – ')]
                out.add(frozenset((a, b)))
    return out


def main():
    raw = [(race, win, E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')) for race, win in NEG.RACES]
    data = [(race, win, None, {run: S.pairs(D) for run, D in R.items()}) for race, win, R in raw]
    sky = {}
    for race, win, R in raw:
        s = set(); s2 = set()
        for D in R.values():
            s |= skypairs(D); s2 |= strong(D, SIDE)
        sky[race] = (s, s2)
    for v in [('any', 90), ('any', 80)]:
        g = {}
        def add(key, win_, N):
            t = g.setdefault(key, [0, 0, 0.0]); t[0] += 1; t[1] += win_; t[2] += 1 / N
        for race, win, R in raw:
            st = S.tally(data, v, skip=race)
            N = len(R); sp, sp2 = sky[race]
            part = {}
            for p in sp2:
                a, b = tuple(p)
                part.setdefault(a, set()).add(b); part.setdefault(b, set()).add(a)
            for run, D in R.items():
                w = win in run
                for (y, x) in S.pairs(D)[v]:
                    k = (y, x)
                    lab = (S.label(st[k][1], st[k][2]) or 'neutral') if k in st else 'unseen'
                    if frozenset((y, x)) in sp:
                        add((lab, '0 activated'), w, N); continue
                    zy = part.get(y, set()) - {x}; zx = part.get(x, set()) - {y}
                    side = 'both' if zy and zx else 'Y side' if zy else 'X side' if zx else 'neither'
                    add((lab, '1 ' + side), w, N)
                    if zy & zx:
                        add((lab, '2 shared Z (triangle)'), w, N)
                    zs = zy | zx
                    if zs:
                        roy = all(z in E.ROY for z in zs)
                        add((lab, '3 side link ' + ('royal only' if roy else 'body')), w, N)
        print(f'## {v[0]} >= {v[1]}, side links >= {SIDE} ({len(raw)} races; labels leave-one-out; holdings / won / by chance / ratio)')
        for lab in ('positive', 'negative', 'neutral', 'unseen'):
            for k in sorted(x for x in g if x[0] == lab):
                h, wn, c = g[k]
                print(f'  {lab:8} {k[1][2:]:24}: {h} / {wn} / {c:.1f} / {wn / c if c else 0:.2f}')
        print()


if __name__ == '__main__':
    main()
