"""Neptune and Sedna on natal Uranus (Newcastle AW 13:30 2 Jan 2022, Good Effort 2/5F 3rd; 17 Nov 2026, Eddie: 'fav very short price with
neptune and sedna on uranus': S Neptune → H Uranus Dec cp 0.1094 (63.5), RA 21.0467 13×φ (62.2), S Sedna → J Uranus RA 161.8512 100φ (80.3);
Ffos Las 14:20 Emir Sacree S Sedna → J Uranus Dec 14×φ (96.08)). Read-only. Versions per runner (any plane, conj / cp incl.), at cuts any score,
>= 50, >= 80: N = S Neptune → H or J Uranus; S = S Sedna → H or J Uranus; NS = both; NSany = either. Over the result races + Newcastle 13:30:
picks / won / by chance, and the favourite-free note is left to the reader (no prices held here)."""
import sys
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NG
RACES = NG.RACES + [('20220102_newcastle_aw_1330', 'Venturous')]


def lines(D, y):
    out = []
    for r in D['Uranus']['L'] + D['Uranus']['O']:
        if r['line'] in (f'S {y} → H Uranus', f'S {y} → J Uranus') and r.get('sc') is not None:
            out.append(r)
    return out


def main():
    keys = [(k, c) for c in (0, 50, 80) for k in ('N', 'S', 'NS', 'NSany')]
    tot = {k: [0, 0, 0.0, []] for k in keys}
    print('# Neptune / Sedna on natal Uranus\n')
    for race, win in RACES:
        R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx'); N = len(R)
        held = []
        for run, D in R.items():
            if 'Uranus' not in D: continue
            n, s = lines(D, 'Neptune'), lines(D, 'Sedna')
            for c in (0, 50, 80):
                hn = any(r['sc'] >= c for r in n); hs = any(r['sc'] >= c for r in s)
                for k, v in (('N', hn), ('S', hs), ('NS', hn and hs), ('NSany', hn or hs)):
                    if v:
                        x = tot[(k, c)]; x[0] += 1; x[2] += 1 / N
                        if win in run: x[1] += 1; x[3].append(run)
            if n or s:
                held.append(f"{run}{' (won)' if win in run else ''}: " + '; '.join(f"{r['line']} {r['plane']} {r['v']:.4f} {r['tgt']} ({r['sc']})" for r in n + s))
        print(f'## {race} ({N} ran, winner {win})'); print('\n'.join('- ' + h for h in held) or '- none'); print()
    print('## Totals (picks / won / by chance)')
    for (k, c), (p, w, ch, ws) in tot.items():
        print(f"- {k} >= {c}: {p} / {w} / {ch:.1f}  {', '.join(ws)}")


if __name__ == '__main__':
    main()
