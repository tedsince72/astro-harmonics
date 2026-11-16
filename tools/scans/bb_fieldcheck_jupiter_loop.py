"""Field check (16 Nov 2026, Eddie: 'jupiter loop please'). Read-only, never reads results files (winners given below by name).
Cafe Sydney (Bath 15:30 12 Jul 2022, won 11/1): S Jupiter -> J Jupiter RA 55.5859 ninth 55.5556 (72.71), carried by the sky pair
S Venus - S Eris RA 55.5716 (85.6); both ends on J Jupiter: S Venus -> J Jupiter Dec 2.2204 ninth (58.78), S Eris -> J Jupiter Dec
21.0269 13xphi (76.69).
Every line must score in a family (conj / contraparallel never count); pair ends not the Moon, not Jupiter, not a royal star.
 A  same-body line S Jupiter -> c Jupiter, a sky pair S A - S B on its family + target, both ends on Jupiter (S E - S Jupiter, or
    S E -> H / J Jupiter), any plane
 B  both ends on the SAME chart's natal Jupiter as the same-body line (S A -> c Jupiter, S B -> c Jupiter), any plane
 C  B with the same-body line and the pair each scoring >= 50
 D  B with both end lines in the other plane from the same-body line
 X  control: B on any body X (not Jupiter) - S X -> c X, pair on its target, both ends S A -> c X, S B -> c X"""
import sys
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
RACES = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad'),
         ('Newton Abbot', '20220717_newton_abbot_1525', 'On Time'), ('Doncaster', '20220716_doncaster_1845', 'Novakai'),
         ('Bath', '20220712_bath_1530', 'Cafe Sydney')]
CJ = ('conj', 'contraparallel')
ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
ok = lambda r: r.get('fam') and r['fam'] not in CJ and r.get('sc') is not None
base = lambda pl: pl.split(' ')[0]


def loops(X, d):
    out = []
    for s in d['L']:
        ln = s['line']
        if not ok(s) or not ln.startswith(f'S {X} → ') or ln not in (f'S {X} → H {X}', f'S {X} → J {X}'):
            continue
        c = ln.split(' → ')[1][0]
        for p in d['S']:
            if not ok(p) or p.get('match') != f"{ln} {s['plane']}" or ' – ' not in p['line']:
                continue
            A, B = (e[2:] for e in p['line'].split(' – '))
            if {A, B} & ({'Moon', X} | set(ROY)):
                continue
            on = lambda Y, cc: [o for o in d['O'] if ok(o) and o['line'] in ((f'S {Y} → {cc} {X}',) if cc else
                                (f'S {Y} → H {X}', f'S {Y} → J {X}', f'S {Y} – S {X}', f'S {X} – S {Y}'))]
            ea, eb = on(A, None), on(B, None)
            if not (ea and eb):
                continue
            tags = {'A'}
            sa, sb = on(A, c), on(B, c)
            if sa and sb:
                tags.add('B')
                if s['sc'] >= 50 and p['sc'] >= 50: tags.add('C')
                op = [o for o in sa if base(o['plane']) != base(s['plane'])], [o for o in sb if base(o['plane']) != base(s['plane'])]
                if op[0] and op[1]: tags.add('D')
            f = lambda o: f"{o['line']} {o['plane']} {o['v']:.4f} {o['tgt']} ({o['sc']})"
            out.append((tags, f"{f(s)} | pair {f(p)} | ends {'; '.join(f(o) for o in (sa or ea)[:2])} / {'; '.join(f(o) for o in (sb or eb)[:2])}"))
    return out




def main():
    KEYS = 'ABCDX'
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for name, r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        print(f'\n## {name} ({N} runners, winner {win})')
        held = {k: [] for k in KEYS}
        for run, D in data.items():
            tg = set()
            for X, d in D.items():
                for t, txt in loops(X, d):
                    if X == 'Jupiter':
                        tg |= t
                        print(f"  {run} [{''.join(sorted(t))}]: {txt}")
                    elif 'B' in t:
                        tg.add('X')
            for k in tg: held[k].append(run)
        for k in KEYS:
            h = held[k]; w = sum(1 for x in h if win in x)
            tot[k][0] += len(h); tot[k][1] += w; tot[k][2] += len(h) / N
        print('  holders: ' + '; '.join(f"{k} {len(held[k])}" + (f" ({', '.join(held[k])})" if k != 'X' and held[k] else '') for k in KEYS))
    print(f'\n## Totals over {len(RACES)} result races (picks / winners / by chance)')
    for k, (p, w, c) in tot.items():
        print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
