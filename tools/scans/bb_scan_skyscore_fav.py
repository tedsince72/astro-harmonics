"""Read-only scan (19 Nov 2026, Eddie after Musselburgh 13:07 2 Nov 2022: 'something in that SKY must also have suggested that the fav had a
strong chance of winning'; chosen after the result). (1) Sky race score v1 / v2 against the favourite winning, every result race with a
favourite in bb_favs_outer_uranus.FAV. (2) Every runner (not only cover picks) by the sky race score lines inside its rule cells
(bb_scan_skyscore_picks: + only / - only / both / none), won vs chance; and the same for the favourites.
Usage: python3 tools/scans/bb_scan_skyscore_fav.py"""
import sys, os
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans']
import bb_scan_negatives as NG, bb_favs_outer_uranus as F, bb_sky_race_score as S, bb_scan_skyscore_picks as K

rows = []
for race, win in NG.RACES:
    if race not in F.FAV or not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
        continue
    fav = F.FAV[race]
    rows.append((S.score(race)[0], S.score_v2(race)[0], fav == win or fav in win, race, fav))
print(f'# (1) {len(rows)} races with a favourite, favourite won {sum(r[2] for r in rows)}\n')
for lo, hi in ((-99, -2), (-1, 0), (1, 2), (3, 99)):
    R = [r for r in rows if lo <= r[0] <= hi]
    print(f'- v1 {lo}..{hi}: {len(R)} races, favourite won {sum(r[2] for r in R)}')
print('- favourite winners: ' + ', '.join(f'{r[4]} ({r[3]}, v1 {r[0]:+d})' for r in rows if r[2]))
T, FT, n = {}, {}, 0
for race, win in NG.RACES:
    if not os.path.exists(f'docs/eddie_read/bybody_rules/{race}_bbrules.json') or \
       not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
        continue
    try:
        rr = K.race_rows(race)
    except Exception:
        continue
    n += 1; fav = F.FAV.get(race)
    for r, pick, cov, (p, m) in rr:
        lab = '+ only' if p and not m else '- only' if m and not p else 'both' if p and m else 'none'
        T.setdefault(lab, []).append((win in r, 1 / len(rr)))
        if fav and fav in r:
            FT.setdefault(lab, []).append((win in r, race))
print(f'\n# (2) {n} races, every runner by score lines in its rule cells\n')
for k, v in T.items():
    print(f'- {k}: runners {len(v)}, won {sum(a for a, _ in v)}, chance {sum(b for _, b in v):.1f}')
print('\nfavourites:')
for k, v in FT.items():
    print(f'- {k}: {len(v)}, won {sum(a for a, _ in v)} ' + ', '.join(r for a, r in v if a))
