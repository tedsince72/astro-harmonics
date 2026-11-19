"""When does the cover of eight work? Race-level measures side by side (19 Nov 2026, Eddie: 'do we need any other measure to see when a
cover would work?'; read-only). Per result race with a cover result:
  v1    sky race score v1 (bb_sky_race_score.score)
  F1    sky triangles with >= 1 fast body closing only across planes, cut 50 (bb_scan_sky_triangles)
  F2    the same with >= 2 fast bodies
  HUB   most sky lines on one fast body, any score inside tolerance
  D     share of the cover picks holding a fast sky-natal triangle at >= 80 (bb_scan_runner_triangles SNf)
  N     cover picks in the race; FIELD runners
Two periods: the 57 races the cover was built on (in-sample) and the races after it was fixed (back-fill + live). Every cut below was
chosen after the results (F1, F2, HUB on all 86 earlier today; D likewise).
  python3 tools/scans/bb_scan_cover_when.py"""
import sys, os, json, io, contextlib
sys.argv = ['x', '80']
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_runner_triangles as RT
    import bb_scan_sky_triangles as T
    import bb_scan_regulus_apex as RA
    import bb_scan_runner_triangles_cover as C
    import bb_sky_race_score as S
RT.CUT = 80.0
FIRST_AFTER = '20261116_wolverhampton_aw_1800'


def main():
    rows, after = [], False
    for race, win in NG.RACES:
        after = after or race == FIRST_AFTER
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        picks = C.picks_of(race)
        if not picks:
            continue
        runners, tt, tp = EB.load(p)
        T.CUT = 50.0
        tr, _ = T.triangles(tt)
        f1 = sum(t['pl'] == 'mixed' and t['fast'] >= 1 for t in tr)
        f2 = sum(t['pl'] == 'mixed' and t['fast'] >= 2 for t in tr)
        T.CUT = 0.0
        _, deg = T.triangles(tt)
        hub = max(deg[b] for b in T.FAST)
        SE, co = RT.sky_fast_corners(tt)
        snf = {RA.key(r['name'].get('H') or '') for r in runners.values() if RT.runner_counts(r, SE, co)['SNf'] > 0}
        d = len(picks & snf) / len(picks)
        try:
            v1 = S.score(race)[0]
        except Exception:
            v1 = None
        rows.append(dict(race=race, hit=RA.key(win) in picks, after=after, v1=v1, F1=f1, F2=f2, HUB=hub, D=d, N=len(picks),
                         FIELD=len(runners)))
    print(f'# When the cover works: race-level measures ({len(rows)} races with cover picks; chosen after the results)\n')
    print('miss rate = races the cover missed / races; in = the 57 build races, out = races after the cover was fixed.\n')
    bands = {'v1': [('<= -2', lambda v: v is not None and v <= -2), ('-1..0', lambda v: v is not None and -1 <= v <= 0),
                    ('>= 1', lambda v: v is not None and v >= 1)],
             'F1': [('0', lambda v: v == 0), ('1-2', lambda v: 1 <= v <= 2), ('>= 3', lambda v: v >= 3)],
             'F2': [('0', lambda v: v == 0), ('>= 1', lambda v: v >= 1)],
             'HUB': [('<= 7', lambda v: v <= 7), ('>= 8', lambda v: v >= 8)],
             'D': [('0', lambda v: v == 0), ('> 0', lambda v: v > 0)],
             'N': [('1', lambda v: v == 1), ('2', lambda v: v == 2), ('>= 3', lambda v: v >= 3)],
             'FIELD': [('<= 5', lambda v: v <= 5), ('6', lambda v: v == 6), ('>= 7', lambda v: v >= 7)]}
    print('| measure | band | all: races / missed / rate | in | out |\n|---|---|---|---|---|')
    for m, bl in bands.items():
        for lab, f in bl:
            cells = []
            for sel in (lambda r: True, lambda r: not r['after'], lambda r: r['after']):
                xs = [r for r in rows if sel(r) and f(r[m])]
                ms = sum(not r['hit'] for r in xs)
                cells.append(f'{len(xs)} / {ms} / {ms / len(xs):.2f}' if xs else '-')
            print(f'| {m} | {lab} | ' + ' | '.join(cells) + ' |')
    # signals pointing to a hit: F1 >= 3 or F2 >= 1; HUB >= 8; D > 0
    print('\n## Signals together (F1 >= 3 or F2 >= 1; HUB >= 8; D > 0)\n')
    print('| signals | all: races / missed / rate | in | out |\n|---|---|---|---|')
    for k in range(4):
        cells = []
        for sel in (lambda r: True, lambda r: not r['after'], lambda r: r['after']):
            xs = [r for r in rows if sel(r) and ((r['F1'] >= 3 or r['F2'] >= 1) + (r['HUB'] >= 8) + (r['D'] > 0)) == k]
            ms = sum(not r['hit'] for r in xs)
            cells.append(f'{len(xs)} / {ms} / {ms / len(xs):.2f}' if xs else '-')
        print(f'| {k} | ' + ' | '.join(cells) + ' |')
    print('\n## Per race\n\n| race | period | hit | v1 | F1 | F2 | HUB | D | N | field |\n|---|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        print(f"| {r['race']} | {'out' if r['after'] else 'in'} | {'hit' if r['hit'] else 'miss'} | {r['v1']} | {r['F1']} | {r['F2']} | "
              f"{r['HUB']} | {r['D']:.2f} | {r['N']} | {r['FIELD']} |")


if __name__ == '__main__':
    main()
