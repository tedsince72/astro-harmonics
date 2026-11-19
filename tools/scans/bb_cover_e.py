"""Version E and the cover signal count (fixed 19 Nov 2026, Eddie: 'yes, please fix'; read-only, prints for one race).
VERSION E: the cover of eight with the four royal-line items (BB3 + BB12 + BB53, BB32, BB77c, BB1b) counting only when the runner also
holds a fast sky-natal triangle at >= 80 (bb_scan_runner_triangles SNf: sky pair S A - S B with A or B the Sun, Moon, Mercury, Venus
or Mars, S A -> c X and S B -> c X on the same natal body, number families >= 80, closing only across planes); BB79, BB69,
BB54 + BB82, BB13 + BB80 count as they are. 1 point level stake at SP on each pick.
COVER SIGNALS (0-3), race level: (1) sky fast triangles: >= 3 with one fast body or >= 1 with two, closing only across planes, cut 50;
(2) a fast body with >= 8 sky lines (any score inside tolerance); (3) a cover-of-eight pick holds the fast sky-natal triangle (>= 80).
Graded as a no-bet filter beside the sky race score: bet only at 2-3. Both chosen after the results (bb_scan_cover_when.py,
bb_scan_cover_items_triangles.py); forward count from Newcastle AW 17:40 / 17:10 19 Nov 2026.
  python3 tools/scans/bb_cover_e.py <race>"""
import sys, os, json, io, contextlib
RACE = sys.argv[1]
sys.argv = ['x', '80']
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB
with contextlib.redirect_stdout(io.StringIO()):
    import bb_scan_runner_triangles as RT
    import bb_scan_sky_triangles as T
    import bb_scan_regulus_apex as RA
RT.CUT = 80.0
ROYAL_ITEMS = [('BB3', 'BB12', 'BB53'), ('BB32',), ('BB77c',), ('BB1b',)]
PLAIN_ITEMS = [('BB79',), ('BB69',), ('BB54', 'BB82'), ('BB13', 'BB80')]

J = json.load(open(f'docs/eddie_read/bybody_rules/{RACE}_bbrules.json'))
held = {r: set() for r in J['runners']}
for rid, cs in J['rules'].items():
    for c in cs:
        if not c.get('watch_only'):
            held.setdefault(c['runner'], set()).add(rid)
runners, tt, tp = EB.load(f'reference/classic/race_batch_{RACE}_active.xlsx')
SE, co = RT.sky_fast_corners(tt)
snf = {}
for r in runners.values():
    snf[RA.key(r['name'].get('H') or '')] = RT.runner_counts(r, SE, co)
picks8, picksE = [], []
for r, h in held.items():
    k = RA.key(r)
    roy = [' + '.join(c) for c in ROYAL_ITEMS if set(c) <= h]
    pl = [' + '.join(c) for c in PLAIN_ITEMS if set(c) <= h]
    if roy or pl:
        picks8.append(k)
    s = snf.get(k, {}).get('SNf', 0)
    e = pl + (roy if s else [])
    if e:
        picksE.append((r, e, s, snf[k]['SNw']))
T.CUT = 50.0
tr, _ = T.triangles(tt)
f1 = sum(t['pl'] == 'mixed' and t['fast'] >= 1 for t in tr)
f2 = sum(t['pl'] == 'mixed' and t['fast'] >= 2 for t in tr)
T.CUT = 0.0
_, deg = T.triangles(tt)
hub = max(T.FAST, key=lambda b: deg[b])
sig1 = f1 >= 3 or f2 >= 1
sig2 = deg[hub] >= 8
sig3 = any(snf.get(k, {}).get('SNf', 0) for k in picks8)
n = sig1 + sig2 + sig3
print(f'{RACE}')
print('Version E picks: ' + ('; '.join(f"{r} ({', '.join(e)}; fast triangles {s}, whole + phi {w})" for r, e, s, w in picksE)
                             if picksE else 'none'))
print(f'Cover signals {n} / 3 (filter: {"bet" if n >= 2 else "skip"}): sky fast triangles across planes >= 50 one-fast {f1}, '
      f'two-fast {f2} ({"yes" if sig1 else "no"}); busiest fast body {hub} {deg[hub]} lines ({"yes" if sig2 else "no"}); '
      f'cover pick with a fast sky-natal triangle ({"yes" if sig3 else "no"})')
