"""Sky race score v1 (fixed 19 Nov 2026, Eddie: 'yes, cover all the angles and especially the families and pairs involved'; built
in-sample from tools/scans/bb_sky_angles_races.py, docs/eddie_read/bybody/sky_angles_races_20261119.md). The sky is the same for
every runner: the score describes the race. High = the cover of eight's kind of race (a rule-heavy winner), low = a race where it
missed (a quieter winner). Sky lines S X – S Y at the off as bb_sky_angles_races.lines (no Moon, + royal stars):
  A  +1 per golden / phi power / ninth line >= 90 with an end in OUT = Neptune, Sedna, Eris, Regulus, Uranus, Ketu
  B  -1 per whole line >= 90 with an end in WH = Makemake, Ceres, Mercury, Aldebaran
     -1 per golden line >= 90 with Saturn
     -1 per conj / contraparallel / opposition line >= 50 with an end in ASP = Neptune, Regulus, Sedna, Ketu, Pluto
A line counts once in A and once in B at most. Usage: python3 tools/scans/bb_sky_race_score.py [--race <race>]"""
import sys, os
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_sky_angles_races as A

OUT = {'Neptune', 'Sedna', 'Eris', 'Regulus', 'Uranus', 'Ketu'}
WH = {'Makemake', 'Ceres', 'Mercury', 'Aldebaran'}
ASP = {'Neptune', 'Regulus', 'Sedna', 'Ketu', 'Pluto'}


def score(race):
    a = b = 0; why = []
    for x in A.lines(race):
        s, f, ends = x[5], x[3], set(x[:2])
        t = f'S {x[0]} – S {x[1]} {x[2]} {x[4]} {f} ({s:.0f})'
        if f in ('golden', 'phi power', 'ninth') and s >= 90 and ends & OUT:
            a += 1; why.append('+ ' + t)
        if (f == 'whole' and s >= 90 and ends & WH) or (f == 'golden' and s >= 90 and 'Saturn' in ends) or \
           (f in ('conj', 'contraparallel', 'opposition') and s >= 50 and ends & ASP):
            b += 1; why.append('- ' + t)
    return a - b, a, b, why



def score_v2(race):
    """Sky race score v2 (fixed 19 Nov 2026, Eddie: 'yes ... please run alongside'; from Newmarket 14:13 29 Oct 2022, chosen after the
    result): v1, plus -1 per golden line >= 90 between S Venus and S Haumea (5 result races held one, the cover missed all 5). v1 unchanged."""
    s, a, b, why = score(race)
    for x in A.lines(race):
        if x[3] == 'golden' and x[5] >= 90 and set(x[:2]) == {'Venus', 'Haumea'}:
            b += 1; why.append(f'- (v2) S {x[0]} – S {x[1]} {x[2]} {x[4]} golden ({x[5]:.0f})')
    return a - b, a, b, why

def main():
    if '--race' in ARGS:
        r = ARGS[ARGS.index('--race') + 1]
        s, a, b, why = score(r)
        print(f'Sky race score v1: {s:+d} (+{a} / -{b})')
        for w in why:
            print('  ' + w)
        return
    import bb_scan_negatives as NG, bb_cover8_where as W
    from bb_cover8 import C
    rows = []
    for race, win in NG.RACES:
        if not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'):
            continue
        runners, hh = W.holders(race); w = next(r for r in runners if win in r)
        hit = any(set(c) <= hh.get(w, set()) for c in C)
        rows.append((score(race)[0], hit, race in A.ORIG, race))
    print('| score | races | cover hit | without origin races: races / hit |\n|---|---|---|---|')
    for lo, hi in ((-99, -2), (-1, 0), (1, 2), (3, 4), (5, 99)):
        R = [r for r in rows if lo <= r[0] <= hi]; Q = [r for r in R if not r[2]]
        print(f'| {lo}..{hi} | {len(R)} | {sum(r[1] for r in R)} | {len(Q)} / {sum(r[1] for r in Q)} |')
    print('\n' + '\n'.join(f'{r[3]}: {r[0]:+d} {"hit" if r[1] else "other"}' for r in rows if r[3].startswith('2026')))


if __name__ == '__main__':
    main()
