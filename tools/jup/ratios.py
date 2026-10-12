#!/usr/bin/env python3
"""ratios.py RACE  - Jupiter-centred read, layer 2: ratios with Jupiter in them (no field view, no judgement).
Reads docs/jupiter/RACE/positions.csv; writes docs/jupiter/RACE/layer2/P##.json + P##.txt.

  26 eq      |Dec| Jupiter S/H, S/J, H/J                      tight <= 0.01%, near <= 0.05%  (p <= 30, q <= 9, not 1)
  16 set     same-body set of Jupiter: S-H, H-J, S-J separations of Jupiter in one plane (or the three |Dec| values,
             plane 'Equator'), all three ratios simple
             (not 1), worst <= 0.15%;  17 = Dec set in proportion 4:5:9 (9/4, 5/4, 9/5)
  22 skynat  pair Jupiter-X: sky value / natal value (per chart)  tight <= 0.005%, near <= 0.01%  (not 1)
  24 hj      pair Jupiter-X: horse value / jockey value          tight <= 0.005%, near <= 0.02%  (not 1)
  13 shared  pair Jupiter-X: horse value ~ jockey value          within 0.5%
  15 pairset pair Jupiter-X: H:J, H:S, J:S all simple (1 allowed), worst <= 0.05%
  24 family  pair Jupiter-X, chart C: S Jupiter - C X  or  C Jupiter - S X  against the natal pair (C) or the sky pair (S)
             tight <= 0.005%, near <= 0.02% (not 1)
Values < 0.5 are not ratioed. X = every body except Jupiter (node = Rahu; no stars; no Moon - no natal Moon)."""
import sys
from jcore import *


def band_of(e, lim):
    return 'tight' if e <= lim[0] else ('near' if e <= lim[1] else '')


def runner_ratios(sky, R):
    H, J = R['H'], R['J']
    out = []
    # 26 Equator ratios
    eq = {'S': abs(sky['Jupiter'][1]), 'H': abs(H['Jupiter'][1]), 'J': abs(J['Jupiter'][1])}
    for a, b in (('S', 'H'), ('S', 'J'), ('H', 'J')):
        f = fit(eq[a], eq[b])
        if f and band_of(f[2], R_EQ):
            out.append({'m': 26, 'kind': 'eq', 'band': band_of(f[2], R_EQ), 'pair': f'{a}/{b}',
                        'values': [eq[a], eq[b]], 'ratio': frac(f), 'dir': f[3], 'err': f[2],
                        'text': f'Jupiter Equator {a}/{b}: {eq[a]:.5f} / {eq[b]:.5f} = {frac(f)} ({f[3]}, {f[2]:.4f}%) [{band_of(f[2], R_EQ)}]'})
    # 16/17 same-body set of Jupiter
    SH = planes(sky['Jupiter'], H['Jupiter']); HJ = planes(H['Jupiter'], J['Jupiter']); SJ = planes(sky['Jupiter'], J['Jupiter'])
    for pl in PLANES + ('Equator',):
        if pl == 'Equator':      # the three |Dec| values themselves: S : H : J
            v = {'S': eq['S'], 'H': eq['H'], 'J': eq['J']}
            fs = [fit(v['S'], v['H']), fit(v['H'], v['J']), fit(v['S'], v['J'])]
            if all(fs) and all(f[0] <= 30 for f in fs) and max(f[2] for f in fs) <= R_SAMEBODY:
                worst = max(f[2] for f in fs)
                out.append({'m': 16, 'kind': 'set', 'plane': pl, 'values': v, 'ratios': [frac(f) for f in fs], 'worst': worst,
                            'text': f"Jupiter same-body set Equator: S {v['S']:.5f}, H {v['H']:.5f}, J {v['J']:.5f}; "
                                    f"S:H {frac(fs[0])}, H:J {frac(fs[1])}, S:J {frac(fs[2])} (worst {worst:.4f}%)"})
            continue
        v = {'S-H': SH[pl], 'H-J': HJ[pl], 'S-J': SJ[pl]}
        fs = [fit(v['S-H'], v['H-J']), fit(v['S-H'], v['S-J']), fit(v['H-J'], v['S-J'])]
        if all(fs) and all(f[0] <= 30 for f in fs):
            worst = max(f[2] for f in fs)
            if worst <= R_SAMEBODY:
                vals = sorted(v.values())
                split = (pl == 'Dec' and
                         abs(vals[1] / vals[0] / 1.25 - 1) * 100 <= R_SAMEBODY and abs(vals[2] / vals[0] / 2.25 - 1) * 100 <= R_SAMEBODY)
                out.append({'m': 17 if split else 16, 'kind': 'set', 'plane': pl, 'values': v,
                            'ratios': [frac(f) for f in fs], 'worst': worst,
                            'text': f"Jupiter same-body set {pl}: S-H {v['S-H']:.5f}, H-J {v['H-J']:.5f}, S-J {v['S-J']:.5f}; "
                                    f"SH:HJ {frac(fs[0])}, SH:SJ {frac(fs[1])}, HJ:SJ {frac(fs[2])} (worst {worst:.4f}%)"
                                    + (' — 4:5:9 split' if split else '')})
    # pairs Jupiter-X
    for x in NATAL_BODIES:
        if x == 'Jupiter':
            continue
        s = planes(sky['Jupiter'], sky[x]); h = planes(H['Jupiter'], H[x]); j = planes(J['Jupiter'], J[x])
        for pl in PLANES:
            # 22 sky/natal
            for c, nat in (('H', h), ('J', j)):
                f = fit(s[pl], nat[pl])
                if f and band_of(f[2], R_SKYNAT):
                    out.append({'m': 22, 'kind': 'skynat', 'chart': c, 'pair': f'Jupiter–{x}', 'x': x, 'plane': pl,
                                'band': band_of(f[2], R_SKYNAT), 'ratio': frac(f), 'err': f[2],
                                'text': f'{c} Jupiter–{x} {pl}: sky {s[pl]:.5f} / {c} {nat[pl]:.5f} = {frac(f)} '
                                        f"({'sky/natal' if f[3] == 'a/b' else 'natal/sky'}, {f[2]:.4f}%) [{band_of(f[2], R_SKYNAT)}]"})
            # 24 h:j and 13 shared
            if h[pl] >= MIN_VALUE and j[pl] >= MIN_VALUE:
                d = abs(h[pl] / j[pl] - 1) * 100
                if d <= R_SHARED:
                    out.append({'m': 13, 'kind': 'shared', 'pair': f'Jupiter–{x}', 'x': x, 'plane': pl, 'err': d,
                                'text': f'shared Jupiter–{x} {pl}: H {h[pl]:.5f} / J {j[pl]:.5f} ({d:.4f}% apart)'})
            f = fit(h[pl], j[pl])
            if f and band_of(f[2], R_HJ):
                out.append({'m': 24, 'kind': 'hj', 'pair': f'Jupiter–{x}', 'x': x, 'plane': pl, 'band': band_of(f[2], R_HJ),
                            'ratio': frac(f), 'err': f[2],
                            'text': f"h:j Jupiter–{x} {pl}: H {h[pl]:.5f} / J {j[pl]:.5f} = {frac(f)} ({'H/J' if f[3] == 'a/b' else 'J/H'}, "
                                    f"{f[2]:.4f}%) [{band_of(f[2], R_HJ)}]"})
            # 15 pair set
            fs = [fit(h[pl], j[pl], True), fit(h[pl], s[pl], True), fit(j[pl], s[pl], True)]
            if all(fs):
                worst = max(f[2] for f in fs)
                if worst <= R_PAIRSET:
                    out.append({'m': 15, 'kind': 'pairset', 'pair': f'Jupiter–{x}', 'x': x, 'plane': pl, 'worst': worst,
                                'ratios': [frac(f) for f in fs],
                                'text': f'pair set Jupiter–{x} {pl}: H {h[pl]:.5f}, J {j[pl]:.5f}, S {s[pl]:.5f}; '
                                        f'H:J {frac(fs[0])}, H:S {frac(fs[1])}, J:S {frac(fs[2])} (worst {worst:.4f}%)'})
        # 24 pair family
        for c, CH, nat in (('H', H, h), ('J', J, j)):
            crossA = planes(sky['Jupiter'], CH[x])   # S Jupiter - C X
            crossB = planes(CH['Jupiter'], sky[x])   # C Jupiter - S X
            for pl in PLANES:
                for cname, cv in ((f'S Jupiter–{c} {x}', crossA[pl]), (f'{c} Jupiter–S {x}', crossB[pl])):
                    for rname, rv in ((f'{c} pair', nat[pl]), ('sky pair', s[pl])):
                        f = fit(cv, rv)
                        if f and band_of(f[2], R_FAMILY):
                            out.append({'m': 24, 'kind': 'family', 'chart': c, 'pair': f'Jupiter–{x}', 'x': x, 'plane': pl,
                                        'band': band_of(f[2], R_FAMILY), 'ratio': frac(f), 'err': f[2],
                                        'text': f'family {cname} {pl} {cv:.5f} vs {rname} {rv:.5f} = {frac(f)} '
                                                f'({f[2]:.4f}%) [{band_of(f[2], R_FAMILY)}]'})
    return out


def main():
    race = sys.argv[1]
    sky, run = load_race(race)
    for P in sorted(run):
        items = runner_ratios(sky, run[P])
        dump(f'docs/jupiter/{race}/layer2/{P}.json', {'runner': run[P]['name'], 'items': items})
        with open(f'docs/jupiter/{race}/layer2/{P}.txt', 'w') as fh:
            fh.write(f'{P} {run[P]["name"]} — layer 2 Jupiter ratios\n')
            for it in sorted(items, key=lambda i: (i['m'], i.get('err', i.get('worst', 0)))):
                fh.write(f"  [{it['m']}] {it['text']}\n")
        print(P, run[P]['name'], len(items), 'items')


if __name__ == '__main__':
    main()
