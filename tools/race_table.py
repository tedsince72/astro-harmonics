#!/usr/bin/env python3
"""race_table.py RACE  - the full table of one race (Eddie, 9 Oct 07:15: "it is for all").

Every item in every runner record, one row each, with the same texture columns, so the runners can be read side by side:
  M3    a sky body (Sun and Moon included) on one of the runner's natal star strings (<=0.15% somewhere in the window)
  M2    a tuned layer (L1 star bases, Nodes, L2, L3, L4): transit chord and natal chord on the same base
        (dev_off/dev_finish: the transit chord re-measured at the off and the finish, 9 Oct)
  SB    same body: natal X - sky X + a third point
  SBP   the pair: sky X + horse X + jockey X
  N2T   natal X -> sky X numbers
  PAR   parallels / RA conjunctions of a sky body with a natal body
  ALONE a strong Method 1 star string (<=0.02%) that no sky body plays in the window (what the sky leaves alone)
It reads the same stage outputs as tools/runner_record.py (run that first) and loads them with its own code, so every
value is the record's value. Output: /home/claude/rr/<RACE>/compare/table.csv (+ a copy for the repo).
Chord family (descriptive, from the chord's own numbers): phi (φ forms), fibonacci (1:2:3 2:3:5 3:5:8 5:8:13), sqrt2 (√2 forms),
midpoint (1:1:2), septimal (a 7 in the triple: 1:6:7 2:5:7 3:4:7 1:7:8 ...), ninths (1:8:9 4:5:9), elevenths (5:6:11 3:8:11),
low (1:3:4 1:4:5 1:5:6), other (2-D composites)."""
import sys, os, re, csv
RACE = sys.argv[1]
SRC = open('/home/claude/tools/runner_record.py', encoding='utf-8').read()
cut = SRC.index('# ------------------------------------------------------------------ the record')
sys.argv = ['runner_record.py', RACE, '--stages', 'records']
exec(SRC[:cut])

# M2 deviations at the off and the finish (9 Oct, Eddie: "start with method 2"). The tuned-layer dumps keep one transit deviation (slow
# bodies at the off, the Moon at its best minute); here the same chord is re-measured at the off and at the finish with the stage's own
# geometry (lattice/nodes_chords.py: 1-minute sky grid, stars as on race day, tri() locked to the chord's own interval values).
_G = {'__name__': 'm2geo'}; _argv = sys.argv; _env = os.environ.get('MOONWIN')
sys.argv = ['nodes_chords.py', RACE, OFF, str(DUR)]; os.environ['MOONWIN'] = 'wide'
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()): exec(open(f'{LAT_D}/nodes_chords.py', encoding='utf-8').read().split('# A')[0], _G)
sys.argv = _argv
if _env is None: os.environ.pop('MOONWIN', None)
else: os.environ['MOONWIN'] = _env
def _P(n, t): return _G['REF'][n] if n in _G['REF'] else _G['pos'](n, t)
def m2dev(r, t):
    """the M2 row's transit chord (third point = transit body on base x-e, measure mm) at minute t, deviation from its own chord"""
    x, e, b, mm = r['x'], r['e'], r['transit_body'], r['mm']; tr = float(r['transit_t'])
    try:
        _G['LOCKT'] = _G['lockT'](_P(x, tr), _P(e, tr), _P(b, tr), mm)
        res = _G['tri'](_P(x, t), _P(e, t), _P(b, t), mm)
    except (KeyError, ZeroDivisionError, TypeError): res = None
    finally: _G['LOCKT'] = None
    return '' if res is None else f"{res[1] * 100:.3f}"

WMIN = re.compile(r"exact ([\d.]+) min (before|after) the off")
FIB = {'1:2:3', '2:3:5', '3:5:8', '5:8:13'}
def fam(t):
    if not t: return ''
    if t.startswith('φ'): return 'phi'
    if '√2' in t: return 'sqrt2'
    if t == '1:1:2': return 'midpoint'
    if t in FIB: return 'fibonacci'
    if t.startswith('other'): return 'other'
    try: n = [int(x) for x in t.split(':')]
    except ValueError: return 'other'
    if len(n) != 3 or n[0] + n[1] != n[2]: return 'other'
    if 7 in n: return 'septimal'
    if n[2] == 9: return 'ninths'
    if n[2] == 11: return 'elevenths'
    if n in ([1, 3, 4], [1, 4, 5], [1, 5, 6]): return 'low'
    return 'other'
def strong_tag(tab, body, mm, a, c):
    nat = [x for x in NATSTR[tab].get((mm, frozenset((a, c))), []) if x[0] == body]
    if not nat: return '', ''
    d = nat[0][1]['dev']
    return f"{d:.3f}", 'STRONG' if d <= STRONG else ''
def fin(tab):
    f = FIN.get(TABS[tab]['cloth'], {}); return f.get('finish', '?'), f.get('sp', '?'), 'fav' if f.get('fav') == '1' else ''
def t_or(t): return hm(t) if t is not None else ''
def z_or(t): return zone(t) if t is not None else ''

COLS = ['kind', 'tab', 'runner', 'role', 'finish', 'sp', 'fav', 'natal_body', 'sky_body', 'layer', 'mm', 'base', 'sky_chord', 'sky_family', 'sky_dev_%',
        'natal_chord', 'natal_family', 'natal_dev_%', 'm1_dev_%', 'm1_strong', 'unison', 'mirror', 'same_body', 'time', 'zone', 'exact_time', 'exact_zone',
        'dev_off_%', 'dev_finish_%', 'rank', 'field_bodies', 'field_charts', 'tightest', 'partner_on', 'also_on_string', 'note']
rows = []
for tab in sorted(TABS):
    t_ = TABS[tab]; fi, sp, fv = fin(tab)
    base = dict(tab=tab, runner=t_['name'].split(' ', 1)[-1], role=t_['role'], finish=fi, sp=sp, fav=fv)
    # M3 (Sun and Moon included)
    for b in NATAL_ORDER:
        for r, h in m3_items(tab, b, BODIES):
            a, c = r['a'], r['c']; key = (r['mm'], frozenset((a, c)))
            md, ms = strong_tag(tab, b, r['mm'], a, c)
            nat = [x for x in NATSTR[tab].get(key, []) if x[0] == b]
            mir = mirror(r, nat[0][1] if nat else None, a, c)
            te = exact_any(r); tt = row_time(r)
            hold = r['hold']; tight = min(hold)
            others = sorted((x for x in STR.get(key, []) if x is not r), key=row_time)
            at = r['at']
            rows.append(dict(base, kind='M3', natal_body=b, sky_body=r['sky'], layer='', mm=r['mm'], base=f"{a}–{c}", sky_chord=r['typ'],
                             sky_family=fam(r['typ']), **{'sky_dev_%': f"{r['dv'] * 100:.3f}", 'natal_dev_%': f"{h[0] * 100:.3f}", 'm1_dev_%': md,
                             'dev_off_%': '' if at[1] is None else f"{at[1] * 100:.3f}", 'dev_finish_%': '' if at[2] is None else f"{at[2] * 100:.3f}"},
                             natal_chord=h[3], natal_family=fam(h[3]), m1_strong=ms, unison='UNISON' if h[3] == r['typ'] else '',
                             mirror='MIRROR' if 'MIRROR' in mir else '', same_body='SAME BODY' if r['sky'] == b else '',
                             time=hm(tt), zone=zone(tt), exact_time=t_or(te), exact_zone=zone_full(r), rank=rank(r, tab, b),
                             field_bodies=len(hold), field_charts=len({x[1] for x in hold}), tightest=f"{short(tight[1])} {tight[2]}",
                             partner_on=partner_on(tab, key), also_on_string='; '.join(f"{x['sky']} {x['typ']} {hm(row_time(x))}" for x in others), note=''))
    # M2 (all layers, all transit bodies)
    for r in M2:
        if r['tab'] != tab: continue
        others = [x for x in M2IDX[m2key(r)] if not (x['tab'] == tab and x['natal_body'] == r['natal_body'])]
        tight = all(r['natal_dev'] <= x['natal_dev'] for x in others)
        tt = r['transit_t'] if (r['transit_body'] == 'Moon' or 'Moon' in (r['x'], r['e'])) else None
        m = WMIN.search(r['transit_when'] or '') if tt is None else None
        if m: tt = T0 + float(m.group(1)) * (-1 if m.group(2) == 'before' else 1)
        inwin = tt is not None and T0 - 30 <= tt <= TEND
        rows.append(dict(base, kind='M2', natal_body=r['natal_body'], sky_body=r['transit_body'], layer=r['layer'], mm=r['mm'], base=f"{r['x']}–{r['e']}",
                         sky_chord=r['transit_type'], sky_family=fam(r['transit_type']), natal_chord=r['natal_type'], natal_family=fam(r['natal_type']),
                         **{'sky_dev_%': f"{r['transit_dev'] * 100:.3f}", 'natal_dev_%': f"{r['natal_dev'] * 100:.3f}", 'm1_dev_%': '', 'dev_off_%': m2dev(r, T0), 'dev_finish_%': m2dev(r, T1)},
                         m1_strong='', unison='UNISON' if r['natal_type'] == r['transit_type'] else '', mirror='',
                         same_body='SAME BODY' if r['natal_body'] == r['transit_body'] else '',
                         time=hm(tt) if inwin else '', zone=zone(tt) if inwin else 'held (outside the window)', exact_time=hm(tt) if tt is not None else '',
                         exact_zone=r['transit_when'] or '', rank=1 if tight else '', field_bodies=len(others) + 1, field_charts=len({x['tab'] for x in others} | {tab}),
                         tightest='this chart' if tight else '', partner_on='', also_on_string='; '.join(sorted(M2BASE[(r['layer'], r['mm'], r['x'], r['e'])] - {r['transit_body']})),
                         note=r.get('lengths') or ''))
    # same body
    for x in SB['part2'].get(tab, []):
        rows.append(dict(base, kind='SB', natal_body=x['body'], sky_body=x['body'], layer='', mm=x['mm'], base=f"{x['body']}–{x['third']}", sky_chord=x['type'],
                         sky_family=fam(x['type']), natal_chord='', natal_family='', **{'sky_dev_%': f"{x['dv'] * 100:.3f}", 'natal_dev_%': '', 'm1_dev_%': '',
                         'dev_off_%': '' if x['at'][1] is None else f"{x['at'][1] * 100:.3f}", 'dev_finish_%': '' if x['at'][2] is None else f"{x['at'][2] * 100:.3f}"},
                         m1_strong='', unison='', mirror='', same_body='SAME BODY', time=hm(x['t']), zone=zone(x['t']), exact_time=hm(x['t']), exact_zone=x['movement'],
                         rank='', field_bodies='', field_charts='', tightest='', partner_on='', also_on_string='', note=f"third point {x['third']}"))
    if t_['role'] == 'horse' and PAIR.get(tab):
        for x in SB['part1'].get(tab, []):
            rows.append(dict(base, kind='SBP', natal_body=x['body'], sky_body=x['body'], layer='', mm=x['mm'], base='sky + horse + jockey', sky_chord=x['type'],
                             sky_family=fam(x['type']), natal_chord='', natal_family='', **{'sky_dev_%': f"{x['dv'] * 100:.3f}", 'natal_dev_%': '', 'm1_dev_%': '',
                             'dev_off_%': '' if x['at'][1] is None else f"{x['at'][1] * 100:.3f}", 'dev_finish_%': '' if x['at'][2] is None else f"{x['at'][2] * 100:.3f}"},
                             m1_strong='', unison='', mirror='', same_body='SAME BODY', time=hm(x['t']), zone=zone(x['t']), exact_time=hm(x['t']), exact_zone=x['movement'],
                             rank='', field_bodies='', field_charts='', tightest='', partner_on=PAIR[tab], also_on_string='', note='pair'))
    # numbers and parallels
    for x in EXTRA['n2t'].get(tab, []):
        rows.append(dict(base, kind='N2T', natal_body=x['body'], sky_body=x['body'], layer='', mm=x['mm'], base='natal X – sky X', sky_chord=x['num'],
                         sky_family='number', natal_chord='', natal_family='', **{'sky_dev_%': '', 'natal_dev_%': '', 'm1_dev_%': '', 'dev_off_%': '', 'dev_finish_%': ''},
                         m1_strong='', unison='', mirror='', same_body='SAME BODY', time=hm(x['t']), zone=zone(x['t']), exact_time=hm(x['t']),
                         exact_zone=f"within ±0.002 {hm(x['start'])}–{hm(x['end'])}", rank='', field_bodies='', field_charts='', tightest='', partner_on='',
                         also_on_string='', note=f"value {x['val']:.4f}, off {x['off']:+.4f}"))
    for x in EXTRA['par'].get(tab, []):
        rows.append(dict(base, kind='PAR', natal_body=x['natal'], sky_body=x['sky'], layer='', mm='Dec', base='', sky_chord=x['kind'], sky_family='parallel',
                         natal_chord='', natal_family='', **{'sky_dev_%': '', 'natal_dev_%': '', 'm1_dev_%': '', 'dev_off_%': f"{x['at_off']:.3f}", 'dev_finish_%': f"{x['at_finish']:.3f}"},
                         m1_strong='', unison='', mirror='', same_body='SAME BODY' if x['sky'] == x['natal'] else '', time=hm(x['t']), zone=zone(x['t']),
                         exact_time=hm(x['t']), exact_zone=f"within 0.1 {hm(x['start'])}–{hm(x['end'])}", rank='', field_bodies='', field_charts='', tightest='',
                         partner_on='', also_on_string='', note=f"closest {x['min']:.3f}{' (window edge)' if x['edge'] else ''}"))
    # what the sky leaves alone: strong Method 1 star strings no sky body plays in the window
    for b in NATAL_ORDER:
        for c in M1[tab][b][1]:
            if c['dev'] > STRONG: continue
            key = (c['meas'], frozenset((c['A'], c['B'])))
            played = STR.get(key, [])
            if any(any(h[1] == tab and h[2] == b for h in r['hold']) for r in played): continue
            rows.append(dict(base, kind='ALONE', natal_body=b, sky_body='', layer='', mm=c['meas'], base=f"{c['A']}–{c['B']}", sky_chord='', sky_family='',
                             natal_chord=c['ratio'], natal_family=fam(c['ratio']), **{'sky_dev_%': '', 'natal_dev_%': f"{c['dev']:.3f}", 'm1_dev_%': f"{c['dev']:.3f}",
                             'dev_off_%': '', 'dev_finish_%': ''}, m1_strong='STRONG', unison='', mirror='', same_body='', time='', zone='', exact_time='', exact_zone='',
                             rank='', field_bodies='', field_charts='', tightest='', partner_on=partner_on(tab, key),
                             also_on_string='; '.join(sorted({r['sky'] for r in played})), note='strong string, no sky body holds this body on it in the window'
                             + (' (others are played on it)' if played else '')))
out = f'{OUT}/compare'; os.makedirs(out, exist_ok=True)
with open(f'{out}/table.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
    for r in rows: w.writerow(r)
import collections
print(f"{len(rows)} rows -> {out}/table.csv", file=sys.stderr)
print(collections.Counter((r['kind']) for r in rows), file=sys.stderr)
