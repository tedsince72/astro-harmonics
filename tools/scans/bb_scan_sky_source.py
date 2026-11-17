"""Sky body as a source on the natal charts (Ffos Las 14:20 5 Jan 2022, Gustavian 8/11F beaten; 17 Nov 2026, Eddie: 'Sedna and Neptune seem to
feature quite strongly in S - H, S - J and some Saturn ... needs further investigation'; read-only). Per runner, the number of lines
S Y → H X and S Y → J X (any X, conj / contraparallel incl.) scoring >= CUT, for each sky body Y. Over the result races: is the winner the
runner with the most such lines (ties incl.), the fewest, and picks / won / by chance for 'most in the field'. Ffos Las 14:20 is shown, and the
totals are given with and without it (it is where the idea came from)."""
import sys
ARGS = sys.argv[1:]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import eddie_bybody_rules as E
import bb_scan_negatives as NG
CUT = float(ARGS[0]) if ARGS else 80
SRC = ['Sedna', 'Neptune', 'Saturn', 'Sedna+Neptune', 'Sedna+Neptune+Saturn']
ORIGIN = '20220105_ffos_las_1420'


def counts(D):
    c = {}
    seen = set()
    for X, d in D.items():
        for r in d['L'] + d['O']:
            ln = r['line']
            if not ln.startswith('S ') or '→' not in ln or r.get('sc') is None or r['sc'] < CUT:
                continue
            key = (ln, r['plane'])
            if key in seen:
                continue
            seen.add(key)
            y = ln.split('→')[0][2:].strip()
            c[y] = c.get(y, 0) + 1
    out = {y: c.get(y, 0) for y in SRC[:3]}
    out['Sedna+Neptune'] = out['Sedna'] + out['Neptune']
    out['Sedna+Neptune+Saturn'] = out['Sedna+Neptune'] + out['Saturn']
    return out


def main():
    data = []
    for race, win in NG.RACES:
        R = E.load(f'docs/eddie_read/bybody/{race}/{race}_bybody.xlsx')
        data.append((race, win, {run: counts(D) for run, D in R.items()}))
    print(f'# Sky body as source, lines S Y → H / J X scoring >= {CUT}, {len(data)} result races\n')
    for race, win, C in data:
        if race == ORIGIN:
            print(f'{race} (origin):')
            for run, c in C.items():
                print(f'  {run}: ' + ', '.join(f'{k} {v}' for k, v in c.items()))
    for label, skip in (('all races', None), ('without Ffos Las 14:20', ORIGIN)):
        print(f'\n## {label}')
        for k in SRC:
            most = [0, 0, 0.0]; few = [0, 0.0]; nr = 0
            for race, win, C in data:
                if race == skip:
                    continue
                nr += 1; N = len(C); v = {r: c[k] for r, c in C.items()}; hi, lo = max(v.values()), min(v.values())
                w = next(r for r in C if win in r)
                if hi > lo:
                    hold = [r for r in v if v[r] == hi]
                    most[0] += len(hold); most[1] += w in hold; most[2] += len(hold) / N
                    few[0] += v[w] == lo; few[1] += sum(x == lo for x in v.values()) / N
            print(f'- {k}: most in the field {most[0]} picks / {most[1]} won / {most[2]:.1f} by chance; '
                  f'winner among the fewest {few[0]} ({few[1]:.1f} by chance); {nr} races')


if __name__ == '__main__':
    main()
