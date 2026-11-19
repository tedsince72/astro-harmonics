"""Fast sky-natal triangle (bb_scan_runner_triangles.py SNf / SNw, cut 80) against the cover of eight picks (19 Nov 2026, Eddie:
'yes, please do that'; read-only). Per race: holders, cover picks, overlap; winners in each group; by chance = sum of group size /
field. Chosen after the results.
  python3 tools/scans/bb_scan_runner_triangles_cover.py [cut]   (default 80)"""
import sys, os, json, io, contextlib
CUT = sys.argv[1] if len(sys.argv) > 1 else '80'
sys.argv = ['x', CUT]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_regulus_apex as RA
    import bb_scan_runner_triangles as RT
RT.CUT = float(CUT)


def picks_of(race):
    rf = f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
    if not os.path.exists(rf):
        return None
    J = json.load(open(rf))
    held = {r: set() for r in J['runners']}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                held.setdefault(c['runner'], set()).add(rid)
    return {RA.key(r) for r in J['runners'] if any(set(c) <= held[r] for c in RA.C8)}


def main():
    G = {}
    out = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        if not os.path.exists(p):
            continue
        picks = picks_of(race)
        if picks is None:
            continue
        runners, tt, tp = EB.load(p)
        SE, corners = RT.sky_fast_corners(tt)
        cnt = {RA.key(r['name'].get('H') or ''): RT.runner_counts(r, SE, corners) for r in runners.values()}
        n = len(cnt); w = RA.key(win); fav = F.FAV.get(race); fav = RA.key(fav) if fav else None
        for k in ('SNf', 'SNw'):
            hold = {x for x, c in cnt.items() if c[k] > 0}
            groups = {'holder': hold, 'holder & pick': hold & picks, 'holder, not pick': hold - picks,
                      'pick, not holder': picks - hold, 'pick or holder': hold | picks,
                      'holder, not pick, not favourite': hold - picks - {fav}}
            for g, s in groups.items():
                a = G.setdefault((k, g), [0, 0, 0.0, 0, 0])   # picks, won, chance, races with >= 1, races won
                a[0] += len(s); a[1] += w in s; a[2] += len(s) / n; a[3] += bool(s); a[4] += w in s
            if k == 'SNf':
                out.append((race, win, w in picks, sorted(hold - picks), w in hold, bool(picks)))
    print(f'# Fast sky-natal triangle (cut {CUT}) against the cover of eight picks\n')
    print(f'{len(out)} result races with a rule file; chosen after the results. SNf = sky pair with a fast body, both ends on the same '
          'natal body, closing across planes; SNw = SNf with a whole side and a phi-family side.\n')
    print('| count | group | runners | won | by chance | races with one | races won |\n|---|---|---|---|---|---|---|')
    for (k, g), (np_, won, ch, rr, rw) in G.items():
        print(f'| {k} | {g} | {np_} | {won} | {ch:.1f} | {rr} | {rw} |')
    print('\n## Cover-miss races: did a holder outside the cover win?\n')
    print('| race | winner | winner holds SNf | holders outside the cover |\n|---|---|---|---|')
    for race, win, hit, extra, wh, hp in out:
        if hp and not hit:
            print(f"| {race} | {win} | {'yes' if wh else 'no'} | {', '.join(extra) or '-'} |")


if __name__ == '__main__':
    main()
