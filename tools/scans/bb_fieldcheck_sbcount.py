"""Field check (16 Nov 2026, Eddie: '1. The most strong same-body lines ... is there any rule that this could make'), from Dynamic Force
(Nottingham 15:30 1 Jun 2022, won 18/1): 6 same-body / H-J lines in a number family scoring >= 90 (field 0-3). Read-only; winners named
below, no results file read. 17 result races, bybody xlsx.
A strong same-body line = S X -> H X, S X -> J X or H X - J X in a number family (not conj / cp / opposition), score >= 90, X any body
(no Moon), Rahu / Ketu counted as one body (Ketu lines dropped when Rahu has the same line).
 Nk    runners with N >= k strong lines (k = 3..7)
 TOP   runners with the most strong lines in the race (ties included)
 TOP1  TOP alone (no tie)
 TOP2  TOP alone and at least 2 more than the next runner
 REP   two different bodies' same-body lines (>= 80) on the same family + target"""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans'); import eddie_bybody_rules as E
from bb_fieldcheck_hub import RACES
RACES = RACES + [('20220601_nottingham_1530', 'Dynamic Force')]
NO = ('conj', 'contraparallel', 'opposition')
num = lambda r: r['fam'] and r['fam'] not in NO and r['sc'] is not None


def strong(D, cut=90):
    out = []; seen = set()
    for X, d in D.items():
        if X == 'Moon': continue
        for r in d['L']:
            if r['line'] in (f'S {X} → H {X}', f'S {X} → J {X}', f'H {X} – J {X}') and num(r) and r['sc'] >= cut:
                k = (r['line'].replace('Ketu', 'Rahu'), r['plane'], round(r['v'], 4))
                if X == 'Ketu' and k in seen: continue
                seen.add(k); out.append((X, f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})", r['fam'], r['tgt']))
    return out


def main():
    keys = [f'N{k}' for k in range(3, 8)] + ['TOP', 'TOP1', 'TOP2', 'REP']
    tot = {k: [0, 0, 0.0] for k in keys}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        cnt = {run: strong(D) for run, D in data.items()}
        n = {run: len(v) for run, v in cnt.items()}
        mx = max(n.values()); srt = sorted(n.values(), reverse=True); nxt = srt[1] if len(srt) > 1 else 0
        held = {k: [] for k in keys}
        for run in data:
            for k in range(3, 8):
                if n[run] >= k: held[f'N{k}'].append(run)
            if n[run] == mx and mx > 0:
                held['TOP'].append(run)
                if srt.count(mx) == 1:
                    held['TOP1'].append(run)
                    if mx - nxt >= 2: held['TOP2'].append(run)
            t = {}
            for X, _, f, g in strong(data[run], 80): t.setdefault((f, g), set()).add('Rahu' if X == 'Ketu' else X)
            if any(len(v) > 1 for v in t.values()): held['REP'].append(run)
        for k in keys:
            hh = held[k]; tot[k][0] += len(hh); tot[k][1] += sum(win in x for x in hh); tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        print('  counts: ' + ', '.join(f"{run} {n[run]}" for run in data))
        for k in keys: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
    print('\n## Totals (picks, won, by chance)')
    for k in keys: print(f"  {k}: {tot[k][0]} picks, {tot[k][1]} won, {tot[k][2]:.1f} by chance")


if __name__ == '__main__':
    main()
