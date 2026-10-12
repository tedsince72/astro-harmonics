#!/usr/bin/env python3
"""checklist_reader.py RACE [--results] [--step N]   — the checklist reader (design: docs/classic/checklist_reader_design.md,
answers from Eddie 12 Oct 2026).

Each item of docs/classic/winner_checklist.md is one small test, run on every runner of the race. Input: Layer 1 inventories
(docs/classic/<RACE>/layer1/P*.json) and Layer 2 tags (derived / mirror). Layer 3 is not used.
Every instance carries: what (numbers copied from Layer 1), level (strict / near / other / wide), tightness t (each part's offset over
its own tolerance: 0 exact, 1 at the edge; a compound takes its worst part), derived (Layer 2 traced a part to other hits).
Field rarity per item: who has it, each runner's tightest and its rank, the field's tightest. Counts printed as background only.
Joins: per runner, pairs and bodies touched by 2+ different items (strict level).
Blind by default: finishing positions only with --results (separate file).
Output: docs/classic/<RACE>/checklist/field.txt, field.json, P*.txt, P*.json [, field_results.txt]."""
import sys, os, glob, json, csv, re, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layer1_inventory import rd, dd, fl, gc, BOD, WHOLE, NINTH, MOVE_WHOLE, MOVE_NINTH, EQ_WHOLE, EQ_NINTH

VERSION = 'CR v1 (12 Oct 2026)'
SLOW = {'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto'}
MOVING = {'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Rahu', 'Ketu'}  # for returns
PLANES = (('RA', rd), ('Dec', dd), ('Flat', fl), ('GC', gc))
SKY_GC = 5.0                       # item 4: sky pair together
NODE_GC = 3.0                      # item 12
SPLIT_TOL = 0.25                   # item 19, %
MID_OFF, MID_SPAN, MID_WIDE = 0.05, 20.0, 60.0   # item 20
SOAK_SPREAD, SOAK_MIN = 0.04, 4    # item 21 (Eddie: +-0.02 around the centre)
LOOP_MAX = 6                       # item 33
JOIN_SKIP = {14, 18, 30}           # joins of other items / field-relative: not counted again in the join view
TEXT_MAX = 40                      # lines per item in P*.txt (all instances in P*.json)

NAMES = {1: 'cross link struck on both ends by 2+ sky bodies', 2: 'cross link struck on both ends (one body, or one per end)',
         3: 'partner strike', 4: 'cross-link pair together in the sky', 5: 'both ends of a cross link moved', 6: 'movement onto a cross link',
         7: 'swap', 8: 'triangle struck at every corner by one sky body', 9: 'pair in one chart struck on both ends by one sky body',
         10: 'pair in one chart struck on both ends by 2+ sky bodies', 11: 'same number / same ratio in both charts', 12: 'shared node',
         13: 'shared natal pair', 14: 'shared pair also cross-linked', 15: 'pair set H:J:S', 16: 'same-body set', 17: 'same-body Dec 9/4 : 5/4 : 9/5',
         18: 'same-body set joined to the web', 19: 'sky body divides a natal pair (split)', 20: 'natal body at the midpoint of X and sky X',
         21: 'soak', 22: 'sky/natal ratio of a natal pair', 23: 'one body in sky/natal ratios in both charts', 24: 'pair family / horse:jockey ratio',
         25: 'Equator whole/ninth (natal) + chains', 26: 'Equator ratio', 27: 'return / contact', 28: 'one sky body on one natal body in RA and Dec',
         29: 'pair in one chart whole/ninth in RA and Dec', 30: 'tightest cross link in the field', 33: 'node loop'}
STEP = {13: 1, 15: 1, 16: 1, 17: 1, 19: 1, 22: 1, 24: 1, 26: 1, 27: 1,
        1: 2, 2: 2, 3: 2, 5: 2, 6: 2, 7: 2, 9: 2, 10: 2, 11: 2, 14: 2, 18: 2, 23: 2, 25: 2, 28: 2, 29: 2, 30: 2,
        4: 3, 8: 3, 12: 3, 20: 3, 21: 3, 33: 4}
RECUR_PAIRS = ['Neptune–Node', 'Chiron–Transpluto', 'Jupiter–Vesta', 'Haumea–Node', 'Pallas–Juno', 'Neptune–Vesta', 'Saturn–Neptune',
               'Venus–Uranus', 'Makemake–Node', 'Transpluto–Node', 'Chiron–Node', 'Mercury–Saturn']
RECUR_CROSS = [('Sedna', 'Chiron'), ('Pluto', 'Neptune'), ('Makemake', 'Haumea'), ('Venus', 'Uranus'), ('Uranus', 'Venus'), ('Pluto', 'Juno')]

# ---------------------------------------------------------------- helpers
def fold(b): return 'Node' if b in ('Rahu', 'Ketu') else b
def fq(q): c, b = q.split(' ', 1); return f'{c} {fold(b)}'           # 'H Ketu' -> 'H Node'
def pk(a, b): return '–'.join(sorted((fold(a), fold(b))))
def bare(q): return q.split(' ', 1)[1]
def tol(lbl, w, n): return n if '/' in lbl else w
def t_num(off, lbl, w=WHOLE, n=NINTH): return abs(off) / tol(lbl, w, n)
def r4(x): return round(x, 4)

class Runner:
    def __init__(self, P, I, T):
        self.P, self.I, self.T = P, I, T['tags']
        self.name = I['runner']
        self.pos = {f"{p['chart']} {p['body']}": (p['ra'], p['dec']) for p in I['points']}
        self.links = I['links']
        self.cross = [(i, l) for i, l in enumerate(self.links) if l['kind'] == 'cross' and (l['close'] or l['near'])]
        self.st_by = {}
        for i, s in enumerate(I['strikes']): self.st_by.setdefault(s['target'], []).append((i, s))
        self.mv_by = {}
        for i, m in enumerate(I['movement']): self.mv_by.setdefault(f"{m['chart']} {m['body']}", []).append((i, m))
    def tag(self, iid): return self.T.get(iid, {}).get('tag', 'root')
    def der(self, *ids): return any(self.tag(i) in ('derived', 'from_numbers') for i in ids)
    def mirror(self, iid): return self.tag(iid) == 'mirror'

def t_cross(l): return min(l['RA'] / 1.5, l['Dec'] / 0.3)
def t_in_close(l): return min(l['RA'] / 1.5, l['Dec'] / 0.6)
def t_strike(s): return t_num(s['off'], s['num'])
def t_move(m): return t_num(m['off'], m['num'], MOVE_WHOLE, MOVE_NINTH)
def s_str(s): return f"sky {s['sky']} -> {s['target']} {s['plane']} {s['value']:.5f} ({s['num']})"
def m_str(m): return f"{m['chart']} {m['body']} moved {m['plane']} {m['value']:.5f} ({m['num']})"
def x_str(l): return f"{l['a']} – {l['b']} RA {l['RA']:.4f} Dec {l['Dec']:.4f}" + ('' if l['close'] else ' (near band)')
def in_str(l):
    tags = (['close'] if l['close'] else []) + [f"{pl} {l[pl]:.5f} = {n['num']}" for pl, n in l['nums'].items()]
    return f"{l['a']}–{bare(l['b'])} " + ', '.join(tags)
def t_in(l):
    ts = ([t_in_close(l)] if l['close'] else []) + [t_num(n['off'], n['num']) for n in l['nums'].values()]
    return min(ts)
def link_ids(R, li): return [f'links:{li}:{pl}' for pl in R.links[li]['nums']]

def inst(item, level, t, what, bodies=(), pair=None, derived=False, **kw):
    return {'item': item, 'level': level, 't': r4(t), 'what': what, 'bodies': sorted({fq(b) for b in bodies if b[0] in 'HJ'}),
            'pair': pair, 'derived': bool(derived), **kw}

def best_by_sky(R, target, flat=True):
    """sky body (node folded) -> (t, strike index, strike), tightest strike on this natal target (flat=False: Flat strikes left out)"""
    out = {}
    for i, s in R.st_by.get(target, []):
        if not flat and s['plane'] == 'Flat': continue
        k = fold(s['sky']); t = t_strike(s)
        if k not in out or (t, i) < (out[k][0], out[k][1]): out[k] = (t, i, s)
    return out

# ---------------------------------------------------------------- step 1: straight from Layer 1
def it13(R):
    out = []
    for i, x in enumerate(R.I['shared']):
        a, b = x['pair'].split('–')
        age = a in SLOW and b in SLOW   # slow-body pairs are shared by age: listed as 'other', not counted
        out.append(inst(13, 'other' if age else 'strict', x['diff_pct'] / 0.5, f"shared {x['pair']} {x['plane']}" + (' (slow pair: age)' if age else '') + f" H {x['horse']:.4f} J {x['jockey']:.4f} ({x['diff_pct']:.4f}%) "
                        f"sky {x['sky']:.4f} S~H {x['sky_vs_horse']} S~J {x['sky_vs_jockey']}", [f'H {a}', f'H {b}', f'J {a}', f'J {b}'], pk(a, b), R.der(f'shared:{i}')))
    return out

def it15(R):
    return [inst(15, 'strict', x['worst_pct'] / 0.05, f"pair set {x['pair']} {x['plane']} H {x['horse']:.4f} J {x['jockey']:.4f} S {x['sky']:.4f} -> "
                 f"H:J {x['H:J']}, H:S {x['H:S']}, J:S {x['J:S']} (worst {x['worst_pct']:.4f}%)", [f'H {a}', f'H {b}', f'J {a}', f'J {b}'], pk(a, b), R.der(f'pair_sets:{i}'))
            for i, x in enumerate(R.I['pair_sets']) for a, b in [x['pair'].split('–')]]

def sb_str(x): return f"same-body {x['body']} {x['plane']} S–H {x['sky_horse']:.4f} H–J {x['horse_jockey']:.4f} S–J {x['sky_jockey']:.4f} -> {' : '.join(x['ratios'])} (worst {x['worst_pct']:.4f}%)"
def sbs(R): return [(i, x) for i, x in enumerate(R.I['same_body']) if not R.mirror(f'same_body:{i}')]

def it16(R):
    return [inst(16, 'strict', x['worst_pct'] / 0.15, sb_str(x), [f"H {x['body']}", f"J {x['body']}"], pk(x['body'], x['body']), R.der(f'same_body:{i}')) for i, x in sbs(R)]

def it17(R):
    return [inst(17, 'strict', x['worst_pct'] / 0.15, sb_str(x), [f"H {x['body']}", f"J {x['body']}"], pk(x['body'], x['body']), R.der(f'same_body:{i}'))
            for i, x in sbs(R) if x['plane'] == 'Dec' and sorted(x['ratios']) == ['5/4', '9/4', '9/5']]

def it19(R):
    out = []
    for i, x in enumerate(R.I['splits']):
        cands = [(r[1], k, r[0]) for k, r in (('parts', x['parts_ratio']), ('span/other', x['span_ratio'])) if r and r[1] <= SPLIT_TOL]
        if not cands: continue
        e, k, r = min(cands)
        out.append(inst(19, 'strict', e / SPLIT_TOL, f"{x['moved']} moved {x['plane']} ({x['move_num']}) toward {x['to']}: span {x['span']:.5f} = {x['moved_part']:.5f} + "
                        f"{x['other_part']:.5f}" + (f" ({x['other_num']})" if x['other_num'] else '') + f"; {k} {r} ({e:.4f}%)",
                        [x['moved'], x['to']], pk(bare(x['moved']), bare(x['to'])), R.der(f'splits:{i}')))
    return out

def it22(R):
    return [inst(22, 'strict' if x['band'] == 'tight' else 'near', x['err_pct'] / 0.005, f"{x['chart']} {x['pair']} {x['plane']} sky {x['sky']:.4f} / natal {x['natal']:.4f} "
                 f"{x['dir']} {x['ratio']} ({x['err_pct']:.4f}%)", [f"{x['chart']} {a}", f"{x['chart']} {b}"], pk(a, b), R.der(f'ratios:{i}'), chart=x['chart'], plane=x['plane'], ratio=x['ratio'])
            for i, x in enumerate(R.I['ratios']) for a, b in [x['pair'].split('–')]]

def it24(R):
    out = []
    for i, x in enumerate(R.I['pair_family']):
        a, b = x['pair'].split('–')
        out.append(inst(24, 'strict' if x['band'] == 'tight' else 'near', x['err_pct'] / 0.005, f"family {x['chart']} {x['pair']} {x['plane']} {x['tn']} {x['tn_value']:.5f} vs "
                        f"{x['base']} {x['base_value']:.5f} {x['dir']} {x['ratio']} ({x['err_pct']:.4f}%)", [f"{x['chart']} {a}", f"{x['chart']} {b}"], pk(a, b), R.der(f'pair_family:{i}')))
    for i, x in enumerate(R.I['hj_ratios']):
        a, b = x['pair'].split('–')
        out.append(inst(24, 'strict' if x['band'] == 'tight' else 'near', x['err_pct'] / 0.005, f"h:j {x['pair']} {x['plane']} H {x['horse']:.5f} J {x['jockey']:.5f} "
                        f"{x['dir']} {x['ratio']} ({x['err_pct']:.4f}%)", [f'H {a}', f'H {b}', f'J {a}', f'J {b}'], pk(a, b), R.der(f'hj_ratios:{i}')))
    return out

def it26(R):
    out = []
    for i, x in enumerate(R.I['eq_ratios']):
        if R.mirror(f'eq_ratios:{i}'): continue
        ch = [c for c in x['pair'].split('/') if c in 'HJ']
        out.append(inst(26, 'strict' if x['band'] == 'tight' else 'near', x['err_pct'] / 0.01, f"Equator {x['body']} {x['pair']} {x['values'][0]:.4f} / {x['values'][1]:.4f} "
                        f"{x['dir']} {x['ratio']} ({x['err_pct']:.4f}%)", [f"{c} {x['body']}" for c in ch], None, R.der(f'eq_ratios:{i}')))
    return out

def it27(R):
    out = []
    for i, x in enumerate(R.I['contacts']):
        if x['return']:
            if fold(x['sky']) in {fold(b) for b in MOVING} and x['RA'] < 0.3 and x['Dec'] < 1.2:
                out.append(inst(27, 'strict', max(x['RA'] / 0.3, x['Dec'] / 1.2), f"RETURN sky {x['sky']} on {x['target']} RA {x['RA']:.4f} Dec {x['Dec']:.4f}",
                                [x['target']], None, kind='return'))
            continue
        out.append(inst(27, 'strict' if x['band'] == 'close' else 'near', min(x['RA'] / 1.5, x['Dec'] / 0.3),
                        f"contact sky {x['sky']} on {x['target']} RA {x['RA']:.4f} Dec {x['Dec']:.4f} GC {x['GC']:.4f}", [x['target']], None, kind='contact'))
    return out

# ---------------------------------------------------------------- step 2: Layer 1 parts combined
def both_ends(R, a, b, flat=True):
    A, B = best_by_sky(R, a, flat), best_by_sky(R, b, flat)
    both = sorted((max(A[k][0], B[k][0]), k) for k in A if k in B)
    return A, B, both

def ends(R, l): return [[s_str(s) for _, s in R.st_by.get(l['a'], [])], [s_str(s) for _, s in R.st_by.get(l['b'], [])]]   # every strike on each end (json)

def it1_2(R):
    out = []
    for li, l in R.cross:
        A, B, both = both_ends(R, l['a'], l['b'])
        lt, lv = t_cross(l), 'strict' if l['close'] else 'near'
        ids = link_ids(R, li)
        nA, nB, _ = both_ends(R, l['a'], l['b'], flat=False)
        nf = r4(max(lt, min(v[0] for v in nA.values()), min(v[0] for v in nB.values()))) if nA and nB else None   # struck both ends without Flat strikes
        if len(both) >= 2:
            parts = '; '.join(f"{k}: {s_str(A[k][2])} | {s_str(B[k][2])}" for _, k in both)
            out.append(inst(1, lv, max(lt, both[1][0]), f"{x_str(l)} struck by {len(both)} sky bodies — {parts}", [l['a'], l['b']], pk(bare(l['a']), bare(l['b'])),
                            R.der(*ids, *[f'strikes:{A[k][1]}' for _, k in both], *[f'strikes:{B[k][1]}' for _, k in both]), sky=[k for _, k in both], link_t=r4(lt), nf_t=nf, ends=ends(R, l)))
        elif A and B:
            ka, kb = min(A, key=lambda k: (A[k][0], k)), min(B, key=lambda k: (B[k][0], k))
            opts = [(max(lt, A[ka][0], B[kb][0]), 'one per end' if ka != kb else 'one body', ka, kb)]
            if both: opts.append((max(lt, both[0][0]), 'one body', both[0][1], both[0][1]))
            t, how, ka, kb = min(opts)
            bb = f"  [both ends by {both[0][1]}: {s_str(A[both[0][1]][2])} | {s_str(B[both[0][1]][2])}]" if both and how != 'one body' else ''
            out.append(inst(2, lv, t, f"{x_str(l)} ({how}) — {s_str(A[ka][2])} | {s_str(B[kb][2])}{bb}", [l['a'], l['b']], pk(bare(l['a']), bare(l['b'])),
                            R.der(*ids, f'strikes:{A[ka][1]}', f'strikes:{B[kb][1]}'), sky=sorted({ka, kb}), link_t=r4(lt), nf_t=nf, ends=ends(R, l)))
    return out

def it3(R):
    out = []
    for li, l in R.cross:
        x, y = bare(l['a']), bare(l['b'])
        if fold(x) == fold(y): continue
        lt, lv = t_cross(l), 'strict' if l['close'] else 'near'
        for tgt, sky in ((l['a'], y), (l['b'], x)):
            for si, s in R.st_by.get(tgt, []):
                if fold(s['sky']) == fold(sky):
                    out.append(inst(3, lv, max(lt, t_strike(s)), f"{x_str(l)} — partner {s_str(s)}", [l['a'], l['b']], pk(x, y), R.der(*link_ids(R, li), f'strikes:{si}')))
    return out

def it5_6(R):
    out = []
    for li, l in R.cross:
        lt, lv = t_cross(l), 'strict' if l['close'] else 'near'
        ma, mb = R.mv_by.get(l['a'], []), R.mv_by.get(l['b'], [])
        key = pk(bare(l['a']), bare(l['b']))
        if ma and mb:
            (ia, a), (ib, b) = min(ma, key=lambda z: (t_move(z[1]), z[0])), min(mb, key=lambda z: (t_move(z[1]), z[0]))
            out.append(inst(5, lv, max(lt, t_move(a), t_move(b)), f"{x_str(l)} — {m_str(a)} | {m_str(b)}" + (f"  (+{len(ma) + len(mb) - 2} more)" if len(ma) + len(mb) > 2 else ''),
                            [l['a'], l['b']], key, R.der(f'movement:{ia}', f'movement:{ib}'), moves=[m_str(m) for _, m in ma + mb]))
        for mi, m in ma + mb:
            out.append(inst(6, lv, max(lt, t_move(m)), f"{m_str(m)} — on {x_str(l)}", [l['a'], l['b']], key, R.der(f'movement:{mi}')))
    return out

def it7(R):
    """swap on exact bodies; a swap that needs Rahu one way and Ketu the other is listed as 'other' (node: mixed)"""
    best = {}
    for li, l in R.cross:
        k = (bare(l['a']), bare(l['b']))
        if fold(k[0]) != fold(k[1]) and (k not in best or t_cross(l) < t_cross(best[k])): best[k] = l
    out, done = [], set()
    for (x, y), l1 in sorted(best.items()):
        for (x2, y2) in sorted(best):
            if not (fold(x2) == fold(y) and fold(y2) == fold(x)): continue
            exact = (x2, y2) == (y, x)
            key = frozenset([(x, y), (x2, y2)])
            if key in done or (x, y) == (x2, y2): continue
            done.add(key); l2 = best[(x2, y2)]
            lv = ('strict' if l1['close'] and l2['close'] else 'near') if exact else 'other'
            out.append(inst(7, lv, max(t_cross(l1), t_cross(l2)), f"swap {fold(x)}/{fold(y)}: {x_str(l1)}; {x_str(l2)}" + ('' if exact else '  (node: Rahu one way, Ketu the other)'),
                            [l1['a'], l1['b'], l2['a'], l2['b']], pk(x, y)))
    return out

def it9_10(R):
    out = []
    for li, l in enumerate(R.links):
        if l['kind'] not in 'HJ': continue
        A, B, both = both_ends(R, l['a'], l['b'])
        if not both: continue
        lt = t_in(l)
        parts = '; '.join(f"{k}: {s_str(A[k][2])} | {s_str(B[k][2])}" for _, k in both)
        item, t = (10, max(lt, both[1][0])) if len(both) >= 2 else (9, max(lt, both[0][0]))
        out.append(inst(item, 'strict', t, f"{in_str(l)} struck by {len(both)} sky bod{'ies' if len(both) > 1 else 'y'} — {parts}", [l['a'], l['b']], pk(bare(l['a']), bare(l['b'])),
                        R.der(*link_ids(R, li), *[f'strikes:{A[k][1]}' for _, k in both], *[f'strikes:{B[k][1]}' for _, k in both]),
                        label='close' if l['close'] and not l['nums'] else 'number' if not l['close'] else 'close + number', sky=[k for _, k in both]))
    return out

def it11(R):
    nums = {'H': [], 'J': []}   # (family, label, t, text, body list, id)
    for i, p in enumerate(R.I['points']):
        if p['chart'] in 'HJ' and p['eq_num'] and not R.mirror(f'points:{i}'):
            nums[p['chart']].append(('Dec', p['eq_num'], t_num(p['eq_off'], p['eq_num'], EQ_WHOLE, EQ_NINTH), f"{p['chart']} {p['body']} Equator {p['dec']:+.5f}",
                                     [f"{p['chart']} {p['body']}"], f'points:{i}'))
    for li, l in enumerate(R.links):
        if l['kind'] not in 'HJ': continue
        for pl, n in l['nums'].items():
            iid = f'links:{li}:{pl}'
            if R.mirror(iid): continue
            nums[l['kind']].append((pl, n['num'], t_num(n['off'], n['num']), f"{l['a']}–{bare(l['b'])} {pl} {l[pl]:.5f}", [l['a'], l['b']], iid))
    out = []
    byH = {}
    for x in nums['H']: byH.setdefault(x[1], []).append(x)
    for j in nums['J']:
        for h in byH.get(j[1], []):
            lv = 'strict' if h[0] == j[0] else 'other'
            out.append(inst(11, lv, max(h[2], j[2]), f"number {j[1]}: {h[3]} = {j[1]} | {j[3]} = {j[1]}" + ('' if lv == 'strict' else f"  (other plane: {h[0]} / {j[0]})"),
                            h[4] + j[4], None, R.der(h[5], j[5]), kind='number', num=j[1]))
    rH = [(i, x) for i, x in enumerate(R.I['ratios']) if x['chart'] == 'H']
    rJ = [(i, x) for i, x in enumerate(R.I['ratios']) if x['chart'] == 'J']
    for ih, h in rH:
        for ij, j in rJ:
            if h['ratio'] != j['ratio']: continue
            lv = 'other' if h['plane'] != j['plane'] else 'strict' if h['band'] == j['band'] == 'tight' else 'near'
            out.append(inst(11, lv, max(h['err_pct'], j['err_pct']) / 0.005, f"ratio {h['ratio']}: H {h['pair']} {h['plane']} ({h['err_pct']:.4f}%) | J {j['pair']} {j['plane']} ({j['err_pct']:.4f}%)",
                            [f"H {b}" for b in h['pair'].split('–')] + [f"J {b}" for b in j['pair'].split('–')], None, R.der(f'ratios:{ih}', f'ratios:{ij}'), kind='ratio', num=h['ratio']))
    return out

def it14(R):
    out = []
    for i, x in enumerate(R.I['shared']):
        a, b = x['pair'].split('–')
        if a in SLOW and b in SLOW: continue
        for li, l in R.cross:
            if {fold(bare(l['a'])), fold(bare(l['b']))} == {fold(a), fold(b)} and fold(a) != fold(b):
                out.append(inst(14, 'strict' if l['close'] else 'near', max(x['diff_pct'] / 0.5, t_cross(l)), f"shared {x['pair']} {x['plane']} ({x['diff_pct']:.4f}%) + cross {x_str(l)}",
                                [f'H {a}', f'H {b}', f'J {a}', f'J {b}'], pk(a, b), R.der(f'shared:{i}')))
    return out

def it18(R):
    out = []
    for i, x in sbs(R):
        b = fold(x['body']); joins = []
        for li, l in R.cross:
            if b in (fold(bare(l['a'])), fold(bare(l['b']))): joins.append(('strict' if l['close'] else 'near', f"cross {x_str(l)}"))
        for r in R.I['ratios']:
            if b in {fold(y) for y in r['pair'].split('–')}: joins.append(('strict' if r['band'] == 'tight' else 'near', f"ratio {r['chart']} {r['pair']} {r['plane']} {r['ratio']}"))
        if not joins: continue
        lv = 'strict' if any(j[0] == 'strict' for j in joins) else 'near'
        js = [j[1] for j in joins if j[0] == lv]
        out.append(inst(18, lv, x['worst_pct'] / 0.15, f"{sb_str(x)} — joined by {len(js)}: " + '; '.join(js[:4]) + (' ...' if len(js) > 4 else ''),
                        [f"H {x['body']}", f"J {x['body']}"], pk(x['body'], x['body']), R.der(f'same_body:{i}')))
    return out

def it23(R):
    by = {}
    for i, r in enumerate(R.I['ratios']):
        for b in {fold(y) for y in r['pair'].split('–')}: by.setdefault(b, {'H': [], 'J': []})[r['chart']].append(r)
    out = []
    for b, d in sorted(by.items()):
        if not d['H'] or not d['J']: continue
        bh, bj = min(d['H'], key=lambda r: r['err_pct']), min(d['J'], key=lambda r: r['err_pct'])
        lv = 'strict' if any(r['band'] == 'tight' for r in d['H']) and any(r['band'] == 'tight' for r in d['J']) else 'near'
        out.append(inst(23, lv, max(bh['err_pct'], bj['err_pct']) / 0.005, f"{b}: H {len(d['H'])} ({bh['pair']} {bh['plane']} {bh['ratio']} {bh['err_pct']:.4f}%) | "
                        f"J {len(d['J'])} ({bj['pair']} {bj['plane']} {bj['ratio']} {bj['err_pct']:.4f}%)", [f'H {b}', f'J {b}'] if b != 'Node' else ['H Rahu', 'J Rahu'], None))
    return out

def it25(R):
    out = []
    chains = {}
    for iid, v in sorted(R.T.items()):
        if v.get('tag') == 'derived':
            for c in v.get('chain', []):
                if c['id'].startswith('points:'): chains.setdefault(c['id'], []).append((iid, v['chain']))
    for i, p in enumerate(R.I['points']):
        if p['chart'] not in 'HJ' or not p['eq_num'] or R.mirror(f'points:{i}'): continue
        ch = list(chains.get(f'points:{i}', []))
        if fold(p['body']) == 'Node':   # the other node's Equator point is its mirror: its chains belong here too
            other = 'Ketu' if p['body'] == 'Rahu' else 'Rahu'
            j = next(k for k, q in enumerate(R.I['points']) if q['chart'] == p['chart'] and q['body'] == other)
            ch += chains.get(f'points:{j}', [])
        cs = '; '.join(f"{desc(R, iid)} from " + ' & '.join(f"{c['a']}–{c['b']} {c['num']}" for c in chain) for iid, chain in ch[:6])
        out.append(inst(25, 'strict', t_num(p['eq_off'], p['eq_num'], EQ_WHOLE, EQ_NINTH), f"{p['chart']} {p['body']} |Dec| {p['eq']:.5f} = {p['eq_num']} ({p['eq_off']:+.5f})"
                        + (f"; chains: {cs}" if cs else ''), [f"{p['chart']} {p['body']}"], None, R.der(f'points:{i}')))
    return out

def desc(R, iid):
    k = iid.split(':')
    if k[0] == 'strikes': s = R.I['strikes'][int(k[1])]; return f"S {s['sky']}–{s['target']} {s['plane']} {s['num']}"
    if k[0] == 'links': l = R.links[int(k[1])]; return f"{l['a']}–{l['b']} {k[2]} {l['nums'][k[2]]['num']}"
    if k[0] == 'movement': m = R.I['movement'][int(k[1])]; return f"{m['chart']} {m['body']} moved {m['plane']} {m['num']}"
    return iid

def it28(R):
    out = []
    g = {}
    for i, s in enumerate(R.I['strikes']): g.setdefault((s['sky'], s['target']), {}).setdefault(s['plane'], []).append((i, s))
    for (sky, tgt), d in sorted(g.items()):
        if 'RA' in d and 'Dec' in d:
            a, b = min(d['RA'], key=lambda z: t_strike(z[1])), min(d['Dec'], key=lambda z: t_strike(z[1]))
            out.append(inst(28, 'strict', max(t_strike(a[1]), t_strike(b[1])), f"{s_str(a[1])} and Dec {b[1]['value']:.5f} ({b[1]['num']})", [tgt], None, R.der(f'strikes:{a[0]}', f'strikes:{b[0]}')))
    return out

def it29(R):
    return [inst(29, 'strict', max(t_num(l['nums']['RA']['off'], l['nums']['RA']['num']), t_num(l['nums']['Dec']['off'], l['nums']['Dec']['num'])),
                 f"{l['a']}–{bare(l['b'])} RA {l['RA']:.5f} = {l['nums']['RA']['num']}, Dec {l['Dec']:.5f} = {l['nums']['Dec']['num']}", [l['a'], l['b']], pk(bare(l['a']), bare(l['b'])),
                 R.der(f'links:{li}:RA', f'links:{li}:Dec'))
            for li, l in enumerate(R.links) if l['kind'] in 'HJ' and 'RA' in l['nums'] and 'Dec' in l['nums']]

def it30(R):
    cl = [l for _, l in R.cross if l['close']]
    if not cl: return []
    l = min(cl, key=lambda l: (t_cross(l), l['a'], l['b']))
    return [inst(30, 'strict', t_cross(l), f"tightest cross link {x_str(l)}", [l['a'], l['b']], pk(bare(l['a']), bare(l['b'])))]

# ---------------------------------------------------------------- step 3: new measures from positions
def it4(R):
    """strict: the cross link's two bodies within GC 5 in the sky; near: only RA < 1.5 or Dec < 0.3 apart in the sky (far apart on the sphere)"""
    out = []
    S = R.pos
    for li, l in R.cross:
        x, y = bare(l['a']), bare(l['b'])
        if fold(x) == fold(y): continue
        xs = ['Rahu', 'Ketu'] if fold(x) == 'Node' else [x]; ys = ['Rahu', 'Ketu'] if fold(y) == 'Node' else [y]
        pairs = [(S[f'S {p}'], S[f'S {q}'], p, q) for p in xs for q in ys]
        g = min((gc(A, B), p, q, A, B) for A, B, p, q in pairs)
        if g[0] < SKY_GC:
            A, B = g[3], g[4]
            out.append(inst(4, 'strict' if l['close'] else 'near', max(t_cross(l), g[0] / SKY_GC), f"{x_str(l)} — sky {g[1]}–{g[2]} GC {g[0]:.4f} RA {rd(A, B):.4f} Dec {dd(A, B):.4f}",
                            [l['a'], l['b']], pk(x, y)))
            continue
        c = min((min(rd(A, B) / 1.5, dd(A, B) / 0.3), p, q, A, B) for A, B, p, q in pairs)
        if c[0] < 1:
            A, B = c[3], c[4]
            out.append(inst(4, 'near', max(t_cross(l), c[0]), f"{x_str(l)} — sky {c[1]}–{c[2]} close in {'RA' if rd(A, B) < 1.5 else 'Dec'} only: GC {gc(A, B):.4f} RA {rd(A, B):.4f} Dec {dd(A, B):.4f}",
                            [l['a'], l['b']], pk(x, y)))
    return out

def it8(R):
    adj = {}
    for li, l in enumerate(R.links):
        if not l['nums']: continue
        best = min(((t_num(n['off'], n['num']), pl, n['num'], l[pl]) for pl, n in l['nums'].items()))
        e = {'planes': {pl: (t_num(n['off'], n['num']), n['num'], l[pl]) for pl, n in l['nums'].items()}, 'best': best, 'ids': link_ids(R, li)}
        adj.setdefault(l['a'], {})[l['b']] = e; adj.setdefault(l['b'], {})[l['a']] = e
    nodes = sorted(adj)
    out = []
    for a, b, c in itertools.combinations(nodes, 3):
        if b not in adj[a] or c not in adj[a] or c not in adj[b]: continue
        sides = [(a, b, adj[a][b]), (a, c, adj[a][c]), (b, c, adj[b][c])]
        common = set(sides[0][2]['planes']) & set(sides[1][2]['planes']) & set(sides[2][2]['planes'])
        S1, S2, S3 = best_by_sky(R, a), best_by_sky(R, b), best_by_sky(R, c)
        for k in sorted(set(S1) & set(S2) & set(S3)):
            if common:
                pl = min(common, key=lambda p: max(s[2]['planes'][p][0] for s in sides))
                sd = [(u, v, pl, e['planes'][pl]) for u, v, e in sides]; plane_lab = f'one plane ({pl})'
            else:
                sd = [(u, v, e['best'][1], e['planes'][e['best'][1]]) for u, v, e in sides]; plane_lab = 'mixed planes'
            t = max([s[3][0] for s in sd] + [S1[k][0], S2[k][0], S3[k][0]])
            txt = ', '.join(f"{u}–{v} {pl} {val[2]:.5f} ({val[1]})" for u, v, pl, val in sd)
            out.append(inst(8, 'strict', t, f"triangle {a} / {b} / {c} [{plane_lab}]: {txt} — sky {k}: {s_str(S1[k][2])}; {s_str(S2[k][2])}; {s_str(S3[k][2])}",
                            [a, b, c], None, R.der(*[i for _, _, e in sides for i in e['ids']], f'strikes:{S1[k][1]}', f'strikes:{S2[k][1]}', f'strikes:{S3[k][1]}'),
                            planes=plane_lab, sky=[k]))
    return out

def it12(R):
    P = R.pos
    g = sorted([(gc(P['H Rahu'], P['J Rahu']), 'J Rahu'), (gc(P['H Rahu'], P['J Ketu']), 'J Ketu')])[0]
    if g[0] >= NODE_GC: return []
    A, B = P['H Rahu'], P[g[1]]
    return [inst(12, 'strict', g[0] / NODE_GC, f"shared node: H Rahu – {g[1]} GC {g[0]:.4f} RA {rd(A, B):.4f} Dec {dd(A, B):.4f}", ['H Rahu', g[1]], None)]

def it20(R):
    P = R.pos; out = []
    natal = [q for q in P if q[0] in 'HJ']
    for c in 'HJ':
        for x in BOD:
            N, S = P[f'{c} {x}'], P[f'S {x}']
            for pl in ('RA', 'Dec'):
                if pl == 'RA':
                    d = (S[0] - N[0] + 180) % 360 - 180; span = abs(d); mid = (N[0] + d / 2) % 360
                else:
                    span = abs(S[1] - N[1]); mid = (S[1] + N[1]) / 2
                if span < 0.5 or span >= MID_WIDE: continue
                for y in natal:
                    if y == f'{c} {x}': continue
                    off = abs((P[y][0] - mid + 180) % 360 - 180) if pl == 'RA' else abs(P[y][1] - mid)
                    if off < MID_OFF:
                        lv = 'strict' if span < MID_SPAN else 'wide'
                        out.append(inst(20, lv, off / MID_OFF, f"{y} at the {pl} midpoint of {c} {x} and sky {x}: span {span:.4f}, midpoint {mid:.4f}, {y} {P[y][0 if pl == 'RA' else 1]:.4f}, "
                                        f"off {off:.4f} ({'same chart' if y[0] == c else 'other chart'})", [f'{c} {x}', y], pk(x, bare(y)), plane=pl, span=r4(span)))
    return out

def near_num(v):
    w = round(v); q = round(v * 9)
    return f"nearest whole {w} ({v - w:+.4f}), nearest ninth {q}/9 = {q / 9:.4f} ({v - q / 9:+.4f})"

def it21(R):
    P = R.pos; out = []
    for X in sorted({fold(b) for b in BOD}):
        xb = ['Rahu', 'Ketu'] if X == 'Node' else [X]
        vals = []
        for c in 'SHJ':
            for b in xb:
                xi = f'{c} {b}'
                for y in P:
                    if fold(bare(y)) == X: continue
                    for pl, f in PLANES:
                        v = f(P[xi], P[y])
                        if v >= 0.5: vals.append((v, pl, xi, y))
        vals.sort()
        wins = []
        j = 0
        for i in range(len(vals)):
            while j < len(vals) and vals[j][0] - vals[i][0] <= SOAK_SPREAD: j += 1
            W = vals[i:j]
            parts = {w[3] for w in W}
            if len(parts) < SOAK_MIN: continue
            pch = {p[0] for p in parts}; vch = pch | {w[2][0] for w in W}
            if not any(w[2][0] == 'S' or w[3][0] == 'S' for w in W): continue
            if 'H' in pch and 'J' in pch: lv = 'strict'
            elif 'H' in vch and 'J' in vch: lv = 'near'      # partners not from both natal charts, but the values touch both (Catterick Chiron)
            else: continue
            wins.append((-len(parts), W[-1][0] - W[0][0], i, j, lv))
        taken = []
        for np_, sp, i, j, lv in sorted(wins, key=lambda w: (w[4] != 'strict', w[0], w[1], w[2])):
            lo, hi = vals[i][0], vals[j - 1][0]
            if any(not (hi < a or lo > b) for a, b in taken): continue
            taken.append((lo, hi)); W = vals[i:j]
            centre = (lo + hi) / 2
            txt = '; '.join(f"{w[2]} – {w[3]} {w[1]} {w[0]:.4f}" for w in W)
            out.append(inst(21, lv, sp / SOAK_SPREAD, f"soak {X} ~{centre:.4f}: {-np_} partners, spread {sp:.4f}, {near_num(centre)}" + ('' if lv == 'strict' else ' (partners not from both natal charts)') + f" — {txt}",
                            [w[2] for w in W] + [w[3] for w in W], None, centre=r4(centre), partners=-np_))
    return out

# ---------------------------------------------------------------- step 4: node loop
def it33(R):
    """closed loop of close links (in a chart and across), length <= LOOP_MAX, through the horse node and the jockey node.
    strict: close links only. near: the loop also closes through the same body standing in both charts (H X = J X, at most 2 such steps)
    — Eddie's Sedgefield example closes this way (J Mercury = H Mercury, J Ketu = H Ketu)."""
    E = {}
    for l in R.links:
        if not l['close']: continue
        a, b = fq(l['a']), fq(l['b'])
        if a == b: continue
        for u, v in ((a, b), (b, a)):
            if v not in E.setdefault(u, {}) or t_close(l) < t_close(E[u][v]): E[u][v] = l
    for b in sorted({fold(x) for x in BOD}):      # same body in both charts
        E.setdefault(f'H {b}', {}); E.setdefault(f'J {b}', {})
        E[f'H {b}'].setdefault(f'J {b}', None); E[f'J {b}'].setdefault(f'H {b}', None)
    seen, out = set(), []
    def step_txt(p, q):
        l = E[p][q]
        return f"{p} = {q} (same body)" if l is None else f"{l['a']}–{l['b']} RA {l['RA']:.4f} Dec {l['Dec']:.4f}"
    def dfs(path, ids):
        u = path[-1]
        for v in sorted(E[u]):
            same = E[u][v] is None
            if same and ids >= 2: continue
            if v == 'H Node' and len(path) >= 3:
                if 'J Node' in path:
                    steps = list(zip(path, path[1:] + ['H Node']))
                    key = frozenset(frozenset(p) for p in steps)
                    if key not in seen:
                        seen.add(key)
                        ls = [E[p][q] for p, q in steps if E[p][q] is not None]
                        n_same = sum(1 for p, q in steps if E[p][q] is None)
                        sames = sorted({bare(p) for p, q in steps if E[p][q] is None})
                        t = max(t_close(l) for l in ls) if ls else 0
                        out.append(inst(33, 'strict' if n_same == 0 else 'near', t, f"loop of {len(steps)}: " + ' -> '.join(path + ['H Node'])
                                        + (f"  (closed through the same body in both charts: {', '.join(sames)})" if n_same else '') + ' — ' + '; '.join(step_txt(p, q) for p, q in steps),
                                        path, None, length=len(steps), same_steps=n_same))
            elif v not in path and len(path) < LOOP_MAX:
                dfs(path + [v], ids + same)
    dfs(['H Node'], 0)
    return out

def t_close(l): return t_cross(l) if l['kind'] == 'cross' else t_in_close(l)

ITEMS = {13: it13, 15: it15, 16: it16, 17: it17, 19: it19, 22: it22, 24: it24, 26: it26, 27: it27,
         1: it1_2, 3: it3, 5: it5_6, 7: it7, 9: it9_10, 11: it11, 14: it14, 18: it18, 23: it23, 25: it25, 28: it28, 29: it29, 30: it30,
         4: it4, 8: it8, 12: it12, 20: it20, 21: it21, 33: it33}

# ---------------------------------------------------------------- race
def run(race, step=4):
    D1, D2 = f'docs/classic/{race}/layer1', f'docs/classic/{race}/layer2'
    runners = []
    for f in sorted(glob.glob(f'{D1}/P*.json')):
        P = os.path.basename(f)[:-5]
        runners.append(Runner(P, json.load(open(f)), json.load(open(f'{D2}/{P}.json'))))
    res = {}
    for R in runners:
        L = []
        for k, fn in ITEMS.items():
            if STEP[k] <= step: L += fn(R)
        L.sort(key=lambda x: (x['item'], x['level'] != 'strict', x['t'], x['what']))
        joins(L)
        res[R.P] = {'name': R.name, 'instances': L}
    items = sorted({k for k in STEP if STEP[k] <= step} | ({2, 6, 10} if step >= 2 else set()))
    field = {}
    for it in items:
        f = {}
        for lv in ('strict', 'near', 'other', 'wide'):
            have = {}
            for P, r in res.items():
                xs = [x for x in r['instances'] if x['item'] == it and x['level'] == lv]
                if xs: have[P] = {'n': len(xs), 'best': xs[0]['t'], 'what': xs[0]['what']}
            if not have: continue
            order = sorted(have, key=lambda p: (have[p]['best'], p))
            for rank, p in enumerate(order, 1): have[p]['rank'] = rank
            f[lv] = {'k': len(have), 'runners': have, 'tightest': order[0]}
        field[str(it)] = f
    return {'version': VERSION, 'race': race, 'step': step, 'n': len(runners), 'runners': {P: r['name'] for P, r in res.items()},
            'field': field, 'per_runner': res, 'items': items}

def pair_map(S):
    """pair -> {item: tightest t}; a body's same-body items (pair 'X–X') also count on every pair that contains X"""
    byp, selfp = {}, {}
    for x in S:
        if not x['pair'] or x['item'] in JOIN_SKIP: continue
        a, b = x['pair'].split('–')
        if a == b and x['item'] not in (16, 17): continue   # only same-body sets count on a body's pairs
        d = selfp.setdefault(a, {}) if a == b else byp.setdefault(x['pair'], {})
        d[x['item']] = min(d.get(x['item'], 9e9), x['t'])
    for k, d in byp.items():
        for b in set(k.split('–')):
            for it, t in selfp.get(b, {}).items(): d[it] = min(d.get(it, 9e9), t)
    for b, d in selfp.items(): byp.setdefault(f'{b}–{b}', {}).update(d)
    return byp

def joins(L):
    S = [x for x in L if x['level'] == 'strict']
    byp, byb = {k: set(v) for k, v in pair_map(S).items()}, {}
    for x in S:
        if x['item'] in JOIN_SKIP: continue
        for b in x['bodies']: byb.setdefault(b, set()).add(x['item'])
    for x in L:
        j = set(byp.get(x['pair'], set())) if x['pair'] else set()
        for b in x['bodies']: j |= byb.get(b, set())
        j.discard(x['item']); x['joined'] = sorted(j)

def rarity(F, it, lv, P):
    f = F['field'][str(it)].get(lv)
    if not f or P not in f['runners']: return ''
    k, n, rk = f['k'], F['n'], f['runners'][P]['rank']
    return 'ONLY runner' if k == 1 else f"{k} of {n}, rank {rk}" + (' (tightest)' if rk == 1 else '')

def field_text(F):
    L = [f"== {F['race']}  field of {F['n']}   [{F['version']}, step {F['step']}]  (blind: no finishing positions)",
         '-- runners: ' + '; '.join(f"{P} {n}" for P, n in F['runners'].items()),
         '-- t = offset / tolerance (0 exact, 1 at the edge; compound = worst part). Counts are background only.']
    for it in F['items']:
        f = F['field'][str(it)]
        L.append(f"[{it:2d}] {NAMES[it]}")
        if not f: L.append('     none in the field'); continue
        for lv in ('strict', 'near', 'other', 'wide'):
            if lv not in f: continue
            g = f[lv]; rs = g['runners']
            L.append(f"     {lv:6s} {('ONLY ' + g['tightest']) if g['k'] == 1 else str(g['k']) + ' of ' + str(F['n'])}: " +
                     '  '.join(f"{p}(t {rs[p]['best']:.3f}, x{rs[p]['n']})" for p in sorted(rs, key=lambda p: rs[p]['rank'])))
            L.append(f"            tightest {g['tightest']}: {rs[g['tightest']]['what']}")
    L.append('-- field-only (strict) per runner')
    for P in F['runners']:
        o = [str(it) for it in F['items'] if F['field'][str(it)].get('strict', {}).get('k') == 1 and P in F['field'][str(it)]['strict']['runners']]
        L.append(f"   {P} {F['runners'][P]}: {', '.join(o) or '-'}")
    return '\n'.join(L)

def runner_text(F, P):
    r = F['per_runner'][P]; L = [f"== {P} {r['name']}   [{F['race']}, {F['version']}, step {F['step']}]"]
    for it in F['items']:
        xs = [x for x in r['instances'] if x['item'] == it]
        L.append(f"[{it:2d}] {NAMES[it]}: " + (', '.join(f"{lv} {sum(1 for x in xs if x['level'] == lv)} ({rarity(F, it, lv, P)})" for lv in ('strict', 'near', 'other', 'wide')
                                                       if any(x['level'] == lv for x in xs)) or 'none'))
        for x in xs[:TEXT_MAX]:
            L.append(f"     {x['level'][0]} t {x['t']:.3f}{' D' if x['derived'] else '  '} {x['what']}" + (f"   joined: {','.join(map(str, x['joined']))}" if x['joined'] else ''))
        if len(xs) > TEXT_MAX: L.append(f"     (+{len(xs) - TEXT_MAX} more in {P}.json)")
    S = [x for x in r['instances'] if x['level'] == 'strict']
    byp, byb = pair_map(S), {}
    for x in S:
        if x['item'] in JOIN_SKIP: continue
        for b in x['bodies']:
            d = byb.setdefault(b, {}); d[x['item']] = min(d.get(x['item'], 9e9), x['t'])
    L.append('-- joins: pairs touched by 2+ different items (strict; item:t of its tightest; a body\'s same-body items count on its pairs)')
    for k, d in sorted(byp.items(), key=lambda kv: (-len(kv[1]), min(kv[1].values()), kv[0])):
        if len(d) >= 2: L.append(f"   {k:24s} {len(d)} items: " + ' '.join(f"{i}:{t:.3f}" for i, t in sorted(d.items())))
    L.append('-- joins: natal bodies touched by 2+ different items (strict)')
    for k, d in sorted(byb.items(), key=lambda kv: (-len(kv[1]), min(kv[1].values()), kv[0])):
        if len(d) >= 2: L.append(f"   {k:14s} {len(d)} items: " + ' '.join(f"{i}:{t:.3f}" for i, t in sorted(d.items())))
    L.append('-- recurring pairs / cross links (annotation only, not weighed)')
    for rp in RECUR_PAIRS:
        k = '–'.join(sorted(rp.split('–')))
        if k in byp: L.append(f"   pair {rp}: items {','.join(map(str, sorted(byp[k])))}")
    seen = set()
    for x in r['instances']:
        if x['item'] in (2, 1, 3, 4, 5, 6, 14, 30):
            for h, j in RECUR_CROSS:
                if x['what'].startswith(f'H {h} – J {j} ') or f'on H {h} – J {j} ' in x['what'] or f'+ cross H {h} – J {j} ' in x['what'] or f'tightest cross link H {h} – J {j} ' in x['what']:
                    if (h, j, x['item']) not in seen: seen.add((h, j, x['item'])); L.append(f"   cross H {h} – J {j}: item {x['item']}")
    return '\n'.join(L)

def results(race, F):
    m = re.match(r'(.+)_(\d{4})_(\d{8})$', race)
    cands = glob.glob(f'reference/classic/race_batch_{m.group(3)}_{m.group(1)}_{m.group(2)}.csv') if m else []
    if not cands: return None
    rows = list(csv.DictReader(open(cands[0])))
    pos = {r['name']: (r['finish_pos'], r['sp']) for r in rows if r['subject_type'] == 'horse'}
    L = [f"== {race} results (not used by the reader)"]
    for P, n in F['runners'].items():
        p = pos.get(n.split(' / ')[0], ('?', '?'))
        o = [str(it) for it in F['items'] if F['field'][str(it)].get('strict', {}).get('k') == 1 and P in F['field'][str(it)]['strict']['runners']]
        L.append(f"   {P} {n:44s} finish {p[0]:>3s}  SP {p[1]:6s}  field-only strict items {','.join(o) or '-'}")
    return '\n'.join(L)

if __name__ == '__main__':
    race = sys.argv[1].rstrip('/').split('/')[-1]
    step = int(sys.argv[sys.argv.index('--step') + 1]) if '--step' in sys.argv else 4
    F = run(race, step)
    O = f'docs/classic/{race}/checklist'; os.makedirs(O, exist_ok=True)
    json.dump({k: v for k, v in F.items() if k != 'per_runner'}, open(f'{O}/field.json', 'w'), indent=1)
    open(f'{O}/field.txt', 'w').write(field_text(F) + '\n')
    for P, r in F['per_runner'].items():
        json.dump(r, open(f'{O}/{P}.json', 'w'), indent=1)
        open(f'{O}/{P}.txt', 'w').write(runner_text(F, P) + '\n')
    if '--results' in sys.argv:
        r = results(race, F)
        if r: open(f'{O}/field_results.txt', 'w').write(r + '\n')
    print(f"{race}: {F['n']} runners, step {step}, " + ', '.join(f"{it}:{sum(1 for r in F['per_runner'].values() for x in r['instances'] if x['item'] == it and x['level'] == 'strict')}" for it in F['items']))
