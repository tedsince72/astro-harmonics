#!/usr/bin/env python3
"""layer1_inventory.py RACEDIR [OUTDIR]   — Layer 1 of the layered reader (see docs/classic/how_it_works.md).

Lists everything, judges nothing. For each runner workbook (sheets TRANS = race sky, P01 = horse natal, P02 = jockey natal):
  points      every body in S/H/J: RA, Dec, Equator (|Dec|); Equator whole/ninth flagged
  links       pairs inside H, inside J, and H x J (cross): close (RA < CLOSE_RA, Dec < CLOSE_DEC_IN / CLOSE_DEC_X)
              or a whole/ninth value in RA, Dec, Flat or GC
  strikes     sky body -> natal body at a whole/ninth in RA, Dec, Flat or GC (sky Ketu included)
  ratios      sky X–Y / natal X–Y simple (p <= 30, q <= 9, not 1, <= RATIO_TOL) in RA, Dec, Flat, GC, per natal chart
  movement    sky X vs natal X (same body), RA/Dec/Flat/GC at whole/ninth (wider window)
  same_body   sky X, horse X, jockey X: three distances in one plane (RA/Dec/Flat/GC), all three ratios simple (p <= 30, q <= 9, not 1),
              worst <= SAME_TOL; skipped when any distance < MIN_V. Plus 'EqValue': the three Equator values S, H, J in simple ratio
              (here equal counts, as 1, but not all three equal — fixed stars are therefore never sets)
  Rahu and Ketu are both listed everywhere (duplicates by symmetry); Layer 2 folds them.
  shared      same pair, horse value vs jockey value within SHARED_TOL (values >= 1), with the sky value and its ratio to each
  eq_ratios   Equator S/H, S/J, H/J simple (p <= 30, q <= 9, not 1) within EQ_NEAR_TOL; band 'tight' (<= EQ_RATIO_TOL) or 'near'
  pair_sets   one pair, horse : jockey : sky values all in simple ratio (p <= 30, q <= 9; 1 allowed, not all three 1), worst <= PAIRSET_TOL
              (as three_way_all.py; Neptune–node sets recur)
  pair_family on one pair, sky-to-natal values vs the natal pair (NN) and sky pair (TT), simple, tight <= FAM_TOL / near <= FAM_NEAR
  splits      a moved body lying between its natal place and another natal body (RA/Dec): span = movement + other part, with ratios
  node        horse node vs jockey node (Rahu–Rahu and Rahu–Ketu) RA offsets
And once per race: sky pair whole/ninth values (sky numbers), the same for every runner.
Every item carries the exact value and its offset. Stars and Moon are not read. Output: OUTDIR/<P>.json, <P>.txt, sky.json, sky.txt."""
import sys, os, glob, re, json, math, itertools, openpyxl

BOD = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno',
       'Vesta', 'Rahu', 'Ketu', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto']
# ---- rules (frozen per version; change only with Eddie) ----
WHOLE, NINTH = 0.005, 0.0005          # links, strikes, sky numbers
MOVE_WHOLE, MOVE_NINTH = 0.01, 0.0011 # movement
EQ_WHOLE, EQ_NINTH = 0.01, 0.0011     # Equator values
RATIO_TOL = 0.00005                   # 0.005 %
SAME_TOL = 0.0015                     # 0.15 %
SHARED_TOL = 0.005                    # 0.5 %
EQ_RATIO_TOL = 0.0001                 # 0.01 %  tight
EQ_NEAR_TOL = 0.0003                  # 0.03 %  near band (Eddie 12 Oct: list, mark, use only when joined)
CLOSE_RA, CLOSE_DEC_IN, CLOSE_DEC_X = 1.5, 0.6, 0.3
MIN_V = 0.5
PAIRSET_TOL = 0.0005                  # 0.05 %
FAM_TOL, FAM_NEAR = 0.00005, 0.0002   # pair-family ratios: tight 0.005 %, near 0.02 % (Eddie 12 Oct, Dettori Sun–Chiron)
PMAX, QMAX = 30, 9
VERSION = 'L1 v1.3 (12 Oct 2026)'

def rd(a, b): return abs((a[0] - b[0] + 180) % 360 - 180)
def dd(a, b): return abs(a[1] - b[1])
def fl(a, b): return math.hypot(rd(a, b), dd(a, b))
def gc(a, b):
    r = math.radians
    c = math.sin(r(a[1])) * math.sin(r(b[1])) + math.cos(r(a[1])) * math.cos(r(b[1])) * math.cos(r(a[0] - b[0]))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))
PLANES = (('RA', rd), ('Dec', dd), ('Flat', fl), ('GC', gc))

def num(v, w=WHOLE, n=NINTH):
    """whole or ninth value -> (label, offset) or None"""
    k = round(v)
    if k > 0 and abs(v - k) <= w: return (str(k), round(v - k, 5))
    q = round(v * 9)
    if q % 9 and q > 0 and abs(v - q / 9) <= n: return (f'{q}/9', round(v - q / 9, 5))
    return None

def frac(x):
    """best simple p/q for x >= 1 (p <= PMAX, q <= QMAX, not 1) -> (label, rel error) or None"""
    best = None
    for q in range(1, QMAX + 1):
        p = round(x * q)
        if p < q or p > PMAX: continue
        g = math.gcd(p, q); pp, qq = p // g, q // g
        if pp == qq: continue
        e = abs(x - p / q) / (p / q)
        if best is None or e < best[1]: best = (f'{pp}/{qq}' if qq > 1 else f'{pp}', e)
    return best

def load(wb, sheet):
    P = {}
    for r in list(wb[sheet].iter_rows(values_only=True))[1:]:
        if r[1] in BOD and isinstance(r[4], (int, float)) and isinstance(r[8], (int, float)):
            assert r[1] not in P, f'{sheet}: duplicate row for {r[1]}'
            P[r[1]] = (float(r[4]), float(r[8]))
    miss = [b for b in BOD if b not in P]
    assert not miss, f'{sheet}: missing bodies {miss}'
    return P

def node_pair(x, y): return {x, y} == {'Rahu', 'Ketu'}

def inventory(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    S, H, J = load(wb, 'TRANS'), load(wb, 'P01'), load(wb, 'P02')
    C = {'S': S, 'H': H, 'J': J}
    name = f"{wb['P01'].cell(2, 1).value} / {wb['P02'].cell(2, 1).value}"
    inv = {'version': VERSION, 'workbook': os.path.basename(path), 'runner': name}

    # points
    pts = []
    for c, N in C.items():
        for b in BOD:
            ra, de = N[b]
            e = num(abs(de), EQ_WHOLE, EQ_NINTH) if abs(de) >= MIN_V else None
            pts.append({'chart': c, 'body': b, 'ra': round(ra, 5), 'dec': round(de, 5), 'eq': round(abs(de), 5),
                        'eq_num': e[0] if e else None, 'eq_off': e[1] if e else None})
    inv['points'] = pts

    # links (inside H, inside J, cross)
    links = []
    def add_link(kind, ca, a, cb, b):
        A, B = C[ca][a], C[cb][b]
        vals = {pl: f(A, B) for pl, f in PLANES}
        close_dec = CLOSE_DEC_X if kind == 'cross' else CLOSE_DEC_IN
        close = vals['RA'] < CLOSE_RA or vals['Dec'] < close_dec
        nums = {pl: num(v) for pl, v in vals.items() if v >= MIN_V and num(v)}
        if close or nums:
            links.append({'kind': kind, 'a': f'{ca} {a}', 'b': f'{cb} {b}', 'close': close,
                          **{pl: round(v, 5) for pl, v in vals.items()},
                          'nums': {pl: {'num': n[0], 'off': n[1]} for pl, n in nums.items()}})
    for c in 'HJ':
        for a, b in itertools.combinations(BOD, 2):
            if not node_pair(a, b): add_link(c, c, a, c, b)
    for a in BOD:
        for b in BOD:
            add_link('cross', 'H', a, 'J', b)
    inv['links'] = links

    # strikes: sky body -> natal body
    st = []
    for c in 'HJ':
        for t in BOD:
            for s in BOD:
                for pl, f in PLANES:
                    v = f(S[s], C[c][t])
                    if v >= MIN_V:
                        n = num(v)
                        if n: st.append({'sky': s, 'target': f'{c} {t}', 'plane': pl, 'value': round(v, 5), 'num': n[0], 'off': n[1],
                                         'same_body': s == t})
    inv['strikes'] = st

    # sky/natal ratios per natal chart
    rt = []
    for c in 'HJ':
        N = C[c]
        for a, b in itertools.combinations(BOD, 2):
            if node_pair(a, b): continue
            for pl, f in PLANES:
                sv, nv = f(S[a], S[b]), f(N[a], N[b])
                if min(sv, nv) < MIN_V: continue
                r = frac(max(sv, nv) / min(sv, nv))
                if r and r[1] <= RATIO_TOL:
                    rt.append({'chart': c, 'pair': f'{a}–{b}', 'plane': pl, 'sky': round(sv, 5), 'natal': round(nv, 5),
                               'ratio': r[0], 'dir': 'sky/natal' if sv >= nv else 'natal/sky', 'err_pct': round(r[1] * 100, 5)})
    inv['ratios'] = rt

    # movement since birth
    mv = []
    for c in 'HJ':
        for b in BOD:
            for pl, f in PLANES:
                v = f(S[b], C[c][b])
                if v >= MIN_V:
                    n = num(v, MOVE_WHOLE, MOVE_NINTH)
                    if n: mv.append({'chart': c, 'body': b, 'plane': pl, 'value': round(v, 5), 'num': n[0], 'off': n[1]})
    inv['movement'] = mv

    # same-body sets
    sb = []
    for b in BOD:
        s, h, j = S[b], H[b], J[b]
        sets = {pl: (f(s, h), f(h, j), f(s, j)) for pl, f in PLANES}
        for pl, v in sets.items():
            if min(v) < MIN_V: continue
            rs = [frac(max(x, y) / min(x, y)) for x, y in itertools.combinations(v, 2)]
            if all(rs) and max(r[1] for r in rs) <= SAME_TOL:
                sb.append({'body': b, 'plane': pl, 'sky_horse': round(v[0], 5), 'horse_jockey': round(v[1], 5), 'sky_jockey': round(v[2], 5),
                           'ratios': [r[0] for r in rs], 'errs_pct': [round(r[1] * 100, 4) for r in rs],
                           'worst_pct': round(max(r[1] for r in rs) * 100, 4)})
        # Equator values (|Dec| of sky, horse, jockey), as in the earlier same_body tool: S:H, H:J, S:J all simple
        ev = (abs(s[1]), abs(h[1]), abs(j[1]))
        if min(ev) >= MIN_V:
            rs = []
            for x, y in ((ev[0], ev[1]), (ev[1], ev[2]), (ev[0], ev[2])):
                q = max(x, y) / min(x, y)
                rs.append(('1', q - 1) if q - 1 <= SAME_TOL else frac(q))
            if all(rs) and max(r[1] for r in rs) <= SAME_TOL and any(r[0] != '1' for r in rs):
                sb.append({'body': b, 'plane': 'EqValue', 'sky_horse': round(ev[0], 5), 'horse_jockey': round(ev[1], 5), 'sky_jockey': round(ev[2], 5),
                           'ratios': [r[0] for r in rs], 'errs_pct': [round(r[1] * 100, 4) for r in rs],
                           'worst_pct': round(max(r[1] for r in rs) * 100, 4)})
    inv['same_body'] = sb

    # shared pairs
    sh = []
    for a, b in itertools.combinations(BOD, 2):
        if node_pair(a, b): continue
        for pl, f in PLANES:
            hv, jv, sv = f(H[a], H[b]), f(J[a], J[b]), f(S[a], S[b])
            if min(hv, jv) < 1: continue
            d = abs(hv - jv) / min(hv, jv)
            if d <= SHARED_TOL:
                def sr(x):
                    if min(x, sv) < MIN_V: return None
                    if abs(max(x, sv) / min(x, sv) - 1) < 1e-12: return ('1', 0.0)
                    r = frac(max(x, sv) / min(x, sv)); return (r[0], round(r[1] * 100, 4)) if r else None
                sh.append({'pair': f'{a}–{b}', 'plane': pl, 'horse': round(hv, 5), 'jockey': round(jv, 5), 'diff_pct': round(d * 100, 4),
                           'sky': round(sv, 5), 'sky_vs_horse': sr(hv), 'sky_vs_jockey': sr(jv),
                           'sky_equal_pct': round(min(abs(sv - hv) / hv, abs(sv - jv) / jv) * 100, 4)})
    inv['shared'] = sh

    # Equator ratios
    er = []
    for b in BOD:
        e = {'S': abs(S[b][1]), 'H': abs(H[b][1]), 'J': abs(J[b][1])}
        for x, y in (('S', 'H'), ('S', 'J'), ('H', 'J')):
            if min(e[x], e[y]) < MIN_V: continue
            r = frac(max(e[x], e[y]) / min(e[x], e[y]))
            if r and r[1] <= EQ_NEAR_TOL:
                er.append({'body': b, 'pair': f'{x}/{y}', 'values': [round(e[x], 5), round(e[y], 5)],
                           'ratio': r[0], 'dir': f'{x}/{y}' if e[x] >= e[y] else f'{y}/{x}', 'err_pct': round(r[1] * 100, 4),
                           'band': 'tight' if r[1] <= EQ_RATIO_TOL else 'near'})
    inv['eq_ratios'] = er

    # pair family: on one pair A–B, sky-to-natal distances (sky A – natal B, natal A – sky B) against the natal pair (NN) and the sky pair (TT)
    pf = []
    for c in 'HJ':
        N = C[c]
        for a, b in itertools.combinations(BOD, 2):
            if node_pair(a, b): continue
            for pl, f in PLANES:
                nn, tt = f(N[a], N[b]), f(S[a], S[b])
                for lab, tn in ((f'sky {a} – {c} {b}', f(S[a], N[b])), (f'{c} {a} – sky {b}', f(N[a], S[b]))):
                    for base, bv in (('NN', nn), ('TT', tt)):
                        if min(tn, bv) < MIN_V: continue
                        r = frac(max(tn, bv) / min(tn, bv))
                        if r and r[1] <= FAM_NEAR:
                            pf.append({'chart': c, 'pair': f'{a}–{b}', 'plane': pl, 'tn': lab, 'tn_value': round(tn, 5), 'base': base,
                                       'base_value': round(bv, 5), 'ratio': r[0], 'dir': 'TN/' + base if tn >= bv else base + '/TN',
                                       'err_pct': round(r[1] * 100, 4), 'band': 'tight' if r[1] <= FAM_TOL else 'near'})
    inv['pair_family'] = pf

    # splits: a moved body (sky X at a whole/ninth from natal X, movement window) lying BETWEEN natal X and natal Y
    # (same chart or the other natal chart), in Dec or RA. Parts: natal X–sky X (the movement) and sky X–natal Y; span natal X–natal Y.
    # No ratio filter: the gate is the movement. Best simple ratio of the parts and of span/part are reported with errors.
    sp = []
    def best(x, y):
        if min(x, y) < 1e-9: return None
        q = max(x, y) / min(x, y)
        if q - 1 <= 1e-9: return ('1', 0.0)
        r = frac(q); return (r[0], round(r[1] * 100, 4)) if r else None
    for m in inv['movement']:
        if m['plane'] not in ('RA', 'Dec'): continue
        x, c = m['body'], m['chart']; f = rd if m['plane'] == 'RA' else dd
        for c2 in 'HJ':
            for y in BOD:
                if c2 == c and (y == x or node_pair(x, y)): continue
                X0, X1, Y = C[c][x], S[x], C[c2][y]
                span, p1, p2 = f(X0, Y), f(X0, X1), f(X1, Y)
                if span < MIN_V or p2 < MIN_V or abs(p1 + p2 - span) > 1e-6: continue
                n2 = num(p2)
                sp.append({'moved': f'{c} {x}', 'to': f'{c2} {y}', 'plane': m['plane'], 'span': round(span, 5), 'moved_part': round(p1, 5),
                           'move_num': m['num'], 'other_part': round(p2, 5), 'other_num': n2[0] if n2 else None,
                           'parts_ratio': best(p1, p2), 'span_ratio': best(span, p2)})
    inv['splits'] = sp

    # pair sets: horse : jockey : sky on one pair
    ps = []
    def frac1(x):
        if x - 1 <= PAIRSET_TOL: return ('1', x - 1)
        return frac(x)
    for a, b in itertools.combinations(BOD, 2):
        if node_pair(a, b): continue
        for pl, f in PLANES:
            hv, jv, sv = f(H[a], H[b]), f(J[a], J[b]), f(S[a], S[b])
            if min(hv, jv, sv) < MIN_V: continue
            rs = [frac1(max(x, y) / min(x, y)) for x, y in ((hv, jv), (hv, sv), (jv, sv))]
            if all(rs) and max(r[1] for r in rs) <= PAIRSET_TOL and any(r[0] != '1' for r in rs):
                ps.append({'pair': f'{a}–{b}', 'plane': pl, 'horse': round(hv, 5), 'jockey': round(jv, 5), 'sky': round(sv, 5),
                           'H:J': rs[0][0], 'H:S': rs[1][0], 'J:S': rs[2][0], 'worst_pct': round(max(r[1] for r in rs) * 100, 4)})
    inv['pair_sets'] = ps

    # node
    inv['node'] = {'rahu_rahu_ra': round(rd(H['Rahu'], J['Rahu']), 4), 'rahu_ketu_ra': round(rd(H['Rahu'], J['Ketu']), 4),
                   'rahu_rahu_dec': round(dd(H['Rahu'], J['Rahu']), 4)}
    return inv, S

def sky_numbers(S):
    out = []
    for a, b in itertools.combinations(BOD, 2):
        if node_pair(a, b): continue
        for pl, f in PLANES:
            v = f(S[a], S[b])
            if v >= MIN_V:
                n = num(v)
                if n: out.append({'pair': f'{a}–{b}', 'plane': pl, 'value': round(v, 5), 'num': n[0], 'off': n[1]})
    return out

def text(inv):
    L = [f"== {inv['runner']}   [{inv['workbook']}, {inv['version']}]"]
    eq = [p for p in inv['points'] if p['eq_num'] and p['chart'] != 'S']
    L.append('-- Equator whole/ninth (natal): ' + ('; '.join(f"{p['chart']} {p['body']} {p['dec']:+.5f} = {p['eq_num']} ({p['eq_off']:+.5f})" for p in eq) or 'none'))
    L.append(f"-- cross links (close: RA < {CLOSE_RA} or Dec < {CLOSE_DEC_X})")
    for l in inv['links']:
        if l['kind'] == 'cross' and l['close']:
            L.append(f"   {l['a']:14s} – {l['b']:14s} RA {l['RA']:9.4f} Dec {l['Dec']:8.4f} GC {l['GC']:9.4f}")
    for c in 'HJ':
        L.append(f"-- {c} close pairs (RA < {CLOSE_RA} or Dec < {CLOSE_DEC_IN})")
        for l in inv['links']:
            if l['kind'] == c and l['close']:
                L.append(f"   {l['a'][2:]}–{l['b'][2:]:12s} RA {l['RA']:9.4f} Dec {l['Dec']:8.4f}" + (' ' + ' '.join(f"{k} {v['num']}" for k, v in l['nums'].items()) if l['nums'] else ''))
    L.append('-- natal numbers (whole/ninth link values, H, J, cross)')
    for l in inv['links']:
        for pl, n in l['nums'].items():
            L.append(f"   {l['kind']:5s} {l['a']}–{l['b']} {pl} {l[pl]:.5f} = {n['num']} ({n['off']:+.5f})")
    L.append('-- sky/natal ratios')
    for r in sorted(inv['ratios'], key=lambda r: r['err_pct']):
        L.append(f"   {r['chart']} {r['pair']:22s} {r['plane']:4s} sky {r['sky']:10.4f} natal {r['natal']:10.4f} {r['dir']} {r['ratio']} ({r['err_pct']:.4f}%)")
    L.append('-- movement since birth')
    for m in inv['movement']:
        L.append(f"   {m['chart']} {m['body']:10s} {m['plane']:4s} {m['value']:10.4f} = {m['num']} ({m['off']:+.5f})")
    L.append('-- same-body sets (sky : horse : jockey)')
    for s in sorted(inv['same_body'], key=lambda s: s['worst_pct']):
        L.append(f"   {s['body']:10s} {s['plane']:7s} S–H {s['sky_horse']:.4f} H–J {s['horse_jockey']:.4f} S–J {s['sky_jockey']:.4f}  {' : '.join(s['ratios'])}  worst {s['worst_pct']:.4f}%")
    L.append('-- shared pairs (horse ~ jockey)')
    for s in sorted(inv['shared'], key=lambda s: s['diff_pct']):
        L.append(f"   {s['pair']:22s} {s['plane']:4s} H {s['horse']:.4f} J {s['jockey']:.4f} ({s['diff_pct']:.3f}%) sky {s['sky']:.4f} S~H {s['sky_vs_horse']} S~J {s['sky_vs_jockey']}")
    L.append('-- Equator ratios')
    for e in inv['eq_ratios']:
        L.append(f"   {e['body']:10s} {e['pair']} {e['values']} {e['dir']} {e['ratio']} ({e['err_pct']:.4f}%) {e['band']}")
    L.append('-- pair family (sky-to-natal vs natal pair NN / sky pair TT, same pair)')
    for s in sorted(inv['pair_family'], key=lambda s: s['err_pct']):
        L.append(f"   {s['chart']} {s['pair']:22s} {s['plane']:4s} {s['tn']:28s} {s['tn_value']:10.5f} vs {s['base']} {s['base_value']:10.5f}  {s['dir']} {s['ratio']} ({s['err_pct']:.4f}%) {s['band']}")
    L.append('-- splits (moved body lying between its natal place and another natal body)')
    for s in inv['splits']:
        L.append(f"   {s['moved']:12s} -> {s['to']:12s} {s['plane']:3s} span {s['span']:9.5f} = moved {s['moved_part']:.5f} ({s['move_num']}) + {s['other_part']:.5f}"
                 + (f" ({s['other_num']})" if s['other_num'] else '') + f"  parts {s['parts_ratio']}  span/other {s['span_ratio']}")
    L.append('-- pair sets (horse : jockey : sky on one pair)')
    for s in sorted(inv['pair_sets'], key=lambda s: s['worst_pct']):
        L.append(f"   {s['pair']:22s} {s['plane']:4s} H {s['horse']:.4f} J {s['jockey']:.4f} S {s['sky']:.4f}  H:J {s['H:J']} H:S {s['H:S']} J:S {s['J:S']}  worst {s['worst_pct']:.4f}%")
    L.append(f"-- node: H Rahu–J Rahu RA {inv['node']['rahu_rahu_ra']}, H Rahu–J Ketu RA {inv['node']['rahu_ketu_ra']}")
    L.append(f"-- sky strikes on natal bodies: {len(inv['strikes'])} (in json; by target below)")
    by = {}
    for s in inv['strikes']: by.setdefault(s['target'], []).append(f"{s['sky']} {s['plane']} {s['num']}")
    for t in sorted(by): L.append(f"   {t:14s} {len(by[t]):2d}: " + '; '.join(by[t]))
    return '\n'.join(L)

if __name__ == '__main__':
    R = sys.argv[1].rstrip('/')
    O = sys.argv[2] if len(sys.argv) > 2 else os.path.join('docs/classic', os.path.basename(R), 'layer1')
    os.makedirs(O, exist_ok=True)
    sky = None
    for f in sorted(glob.glob(f'{R}/*.xlsx')):
        t = re.search(r'__(P\d+)', f).group(1)
        inv, S = inventory(f)
        json.dump(inv, open(f'{O}/{t}.json', 'w'), indent=1)
        open(f'{O}/{t}.txt', 'w').write(text(inv) + '\n')
        if sky is None:
            sky = sky_numbers(S)
            json.dump(sky, open(f'{O}/sky.json', 'w'), indent=1)
            open(f'{O}/sky.txt', 'w').write('\n'.join(f"{s['pair']:22s} {s['plane']:4s} {s['value']:10.5f} = {s['num']} ({s['off']:+.5f})" for s in sky) + '\n')
        print(f"{t} {inv['runner']}: links {len(inv['links'])} strikes {len(inv['strikes'])} ratios {len(inv['ratios'])} moves {len(inv['movement'])} "
              f"same_body {len(inv['same_body'])} shared {len(inv['shared'])} eq_ratios {len(inv['eq_ratios'])} pair_sets {len(inv['pair_sets'])} family {len(inv['pair_family'])} splits {len(inv['splits'])}")
