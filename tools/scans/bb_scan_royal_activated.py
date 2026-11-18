"""Scan (18 Nov 2026, Eddie: 'how this may impact the royal stars when they have sky lines versus when they have not'; read-only).
Every natal royal line c R – c X (R a royal star, c = H or J) in a number family (no conj / cp / opposition) scoring >= cut, split by:
  carried   a sky pair S A – S B (A, B not the Moon) on the same family + target (any score)
  royal sky the same royal star on sky X: S R – S X scores (any family incl. conj, any plane)
Groups: both / carried only / royal sky only / neither. Holdings / won / by chance (1 / field size each); and runner-level: runners whose
royal lines >= cut are ALL 'neither' vs runners with at least one sky-linked line. Races = bb_scan_negatives.RACES."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NEG
NO = ('conj', 'contraparallel', 'opposition')
ROY = E.ROY


def lines(D, cut):
    pairs, rsky = {}, set()
    for X, d in D.items():
        for r in d['O']:
            ln = r['line']
            if r.get('sc') is None or not ln.startswith('S ') or ' – ' not in ln:
                continue
            a, b = [s[2:] for s in ln.split(' – ')]
            if 'Moon' in (a, b):
                continue
            if r['fam'] not in NO:
                pairs.setdefault((r['fam'], r['tgt']), []).append(ln)
            for R_, Y in ((a, b), (b, a)):
                if R_ in ROY and r['fam'] not in ('contraparallel', 'opposition'):
                    rsky.add((R_, Y))
    out = []
    for X, d in D.items():
        for r in d['L']:
            ln = r['line']
            if r.get('sc') is None or r['fam'] in NO or r['sc'] < cut or ' – ' not in ln:
                continue
            a, b = [s[2:] for s in ln.split(' – ')]
            if a not in ROY or b != X or ln[0] == 'S':
                continue
            c = bool(pairs.get((r['fam'], r['tgt'])))
            s = (a, X) in rsky
            out.append(('both' if c and s else 'carried only' if c else 'royal sky only' if s else 'neither', f"{ln} {r['plane']} {r['tgt']} ({r['sc']})"))
    return out


def main():
    for cut in (90, 80):
        g, rr = {}, {}
        for race, win in NEG.RACES:
            R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
            N = len(R)
            for run, D in R.items():
                L = lines(D, cut)
                for grp, _ in L:
                    t = g.setdefault(grp, [0, 0, 0.0]); t[0] += 1; t[1] += win in run; t[2] += 1 / N
                if L:
                    k = 'all neither' if all(x == 'neither' for x, _ in L) else 'some sky-linked'
                    t = rr.setdefault(k, [0, 0, 0.0]); t[0] += 1; t[1] += win in run; t[2] += 1 / N
        print(f'## royal lines >= {cut} over {len(NEG.RACES)} result races (holdings / won / by chance)')
        for k in ('both', 'carried only', 'royal sky only', 'neither'):
            h, w, c = g.get(k, [0, 0, 0])
            print(f'  {k:15}: {h} / {w} / {c:.1f}')
        print('  runners:')
        for k in ('some sky-linked', 'all neither'):
            h, w, c = rr.get(k, [0, 0, 0])
            print(f'  {k:15}: {h} / {w} / {c:.1f}')


if __name__ == '__main__':
    main()
