"""Do the cover-of-eight items carry the fast sky-natal triangle? (19 Nov 2026, Eddie: 'are any of the cover items actually closed
triangles'; read-only). Per cover item: holders over the result races, how many also hold SNf at >= 80 (bb_scan_runner_triangles.py:
sky pair with a fast body, both ends on the same natal body, closing only across planes), winners in each part. BB1b cells: whether the
item's own pair + end lines close across planes and include a fast body. Chosen after the results.
  python3 tools/scans/bb_scan_cover_items_triangles.py"""
import sys, os, json, io, contextlib
sys.argv = ['x', '80']
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_runner_triangles as RT
    import bb_scan_regulus_apex as RA
RT.CUT = 80.0
C8 = RA.C8
out = {c: [0, 0, 0, 0] for c in C8}   # holders, holders won, holders with SNf, those won
for race, win in NG.RACES:
    p = f'reference/classic/race_batch_{race}_active.xlsx'
    rf = f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
    if not (os.path.exists(p) and os.path.exists(rf)):
        continue
    J = json.load(open(rf))
    held = {r: set() for r in J['runners']}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c.get('watch_only'):
                held.setdefault(c['runner'], set()).add(rid)
    runners, tt, tp = EB.load(p)
    SE, co = RT.sky_fast_corners(tt)
    snf = {RA.key(r['name'].get('H') or '') for r in runners.values() if RT.runner_counts(r, SE, co)['SNf'] > 0}
    w = RA.key(win)
    for r, h in held.items():
        k = RA.key(r)
        for c in C8:
            if set(c) <= h:
                o = out[c]; o[0] += 1; o[1] += k == w
                if k in snf:
                    o[2] += 1; o[3] += k == w
print('| item | holders | won | with fast triangle >= 80 | of those won | without | of those won |\n|---|---|---|---|---|---|---|')
for c, (n, wn, s, sw) in out.items():
    print(f"| {' + '.join(c)} | {n} | {wn} | {s} | {sw} | {n - s} | {wn - sw} |")
