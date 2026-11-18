"""Level-stake profit on the fresh sheet (18 Nov 2026, Eddie; read-only). 1 point on every holder; a winner returns its SP
(winners' prices from the watch-file Result sections, the rest as below); every other pick -1. Baseline: 1 point on every
runner in every race. Holders from bb_fresh_sheet (today's rules on all 57 result races)."""
import os, re, sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as N, bb_fresh_sheet as F
OTHER = {'20210402_lingfield_aw_1435': '25/1', '20200608_haydock_1345': '40/1', '20240608_beverley_1405': '125/1',
         '20240515_york_1545': '22/1', '20220406_catterick_1440': '33/1', '20231006_fontwell_1530': '50/1',
         '20210802_newcastle_aw_1633': '25/1', '20240118_chelmsford_aw_1320': '18/1', '20240515_york_1615': '40/1'}


def sp(race, win):
    if race in OTHER: s = OTHER[race]
    else:
        t = open(f'docs/eddie_read/bybody_rules/{race}_watch.md').read(); t = t[t.find('## Result'):]
        s = re.search(re.escape(win) + r'[^\n]{0,60}?(\d+/\d+)', t).group(1)
    a, b = s.split('/'); return int(a) / int(b), s


ITEMS = [['BB32'], ['BB3', 'BB12', 'BB53'], ['BB3', 'BB53', 'BB63'], ['BB80'], ['BB3', 'BB80'], ['BB67'], ['BB81'], ['BB79'],
         ['BB72'], ['BB1b'], ['BB62'], ['BB23', 'BB62'], ['BB13', 'BB80'], ['BB54', 'BB82'], ['BB78'], ['BB77'], ['BB77c'],
         ['BB54'], ['BB57'], ['BB23'], ['BB3'], ['BB3', 'BB63'], ['BB3', 'BB54'], ['BB63', 'BB68'], ['BB68'], ['BB69']]


def main():
    data = []
    for race, win in N.RACES:
        runners, hh = F.holders(race); w = next(r for r in runners if win in r)
        data.append((race, w, runners, hh, *sp(race, win)))
    tot = sum(len(d[2]) for d in data); won = sum(d[4] for d in data) + len(data) - tot
    print(f'Baseline, 1 point on every runner: {tot} bets, profit {won:+.1f}, ROI {100*won/tot:+.0f} %\n')
    print('| item | picks / won / by chance | profit (points) | ROI | winners (SP) |\n|---|---|---|---|---|')
    for it in ITEMS:
        s = set(it); n = 0; p = 0.0; c = 0.0; ws = []
        for race, w, runners, hh, dec, txt in data:
            for r, rs in hh.items():
                if s <= rs:
                    n += 1; c += 1 / len(runners)
                    if r == w: p += dec; ws.append(f"{w.split(' ', 1)[-1]} {txt}")
                    else: p -= 1
        nw = len(ws)
        print(f"| {' + '.join(it)} | {n} / {nw} / {c:.1f} | {p:+.1f} | {100*p/n:+.0f} % | {', '.join(ws)} |")


if __name__ == '__main__':
    main()
