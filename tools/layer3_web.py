#!/usr/bin/env python3
"""layer3_web.py RACE   — Layer 3 of the layered reader (design: docs/classic/layer3_design.md, approved by Eddie 12 Oct 2026).

Reads docs/classic/<RACE>/layer1/P*.json and layer2/P*.json. Describes, does not score.
  Step 1  ways each natal body is struck (P position, M movement, R ratio, B same body, E Equator, S shared, X cross link) — ROOT items
          only; derived items listed as 'also'. Near items count only when the body already has a tight kind. HUB = 3+ kinds.
  Step 2  webs: natal bodies joined by cross links, natal links (close or number), ratio pairs, shared / pair-set / horse:jockey pairs,
          same-body sets, Equator ratios, splits. Hubs and the shortest item path between hubs.
  Step 3  shapes 1–12 (see design). Shapes are found on root AND derived items (a loop of numbers is itself a shape); each shape reports
          how many independent root items it rests on (derived items replaced by their chains).
Rahu and Ketu are folded into one 'Node' per chart for hubs and webs (items keep their own names).
Output: docs/classic/<RACE>/layer3/P*.json, P*.txt"""
import sys, os, glob, json, math, itertools
VERSION = 'L3 v1.4 (12 Oct 2026, pair focus A+B+C)'
SPLIT_TOL = 0.25      # % for shape 10
SKY_PAIR_GC = 5.0     # shape 3
NODE_SHARED = 3.0     # shape 9
STRONG = 5            # 'strong hub': 5+ tight kinds (added after first run; see layer3_README)
RECUR_PAIRS = [{'Neptune', 'Node'}, {'Chiron', 'Transpluto'}, {'Haumea', 'Node'}, {'Pallas', 'Juno'}, {'Jupiter', 'Vesta'},
               {'Neptune', 'Vesta'}, {'Saturn', 'Neptune'}, {'Venus', 'Uranus'}]
RECUR_CROSS = [('Sedna', 'Chiron'), ('Pluto', 'Neptune'), ('Makemake', 'Haumea'), ('Venus', 'Uranus'), ('Uranus', 'Venus')]

def fold(b): return 'Node' if b in ('Rahu', 'Ketu') else b
def nb(lbl):  # 'H Rahu' -> 'H Node'
    c, b = lbl.split(' ', 1); return f'{c} {fold(b)}'
def gc(a, b):
    r = math.radians
    c = math.sin(r(a[1])) * math.sin(r(b[1])) + math.cos(r(a[1])) * math.cos(r(b[1])) * math.cos(r(a[0] - b[0]))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))

def run(I, T):
    tags = T['tags']
    def tg(iid): return tags.get(iid, {}).get('tag')
    def usable(iid): return tg(iid) in ('root', 'derived')          # for shapes
    def is_root(iid): return tg(iid) == 'root'
    P = {f"{p['chart']} {p['body']}": (p['ra'], p['dec']) for p in I['points']}
    desc = {}
    # ---------- item index ----------
    links = []   # (iid, a, b, kind, close/near/number, label)
    for i, l in enumerate(I['links']):
        cn = l['close'] or l.get('near')
        if cn and usable(f'links:{i}'):
            links.append((f'links:{i}', l['a'], l['b'], l['kind'], 'close' if l['close'] else 'near',
                          f"{l['kind']} {l['a']}–{l['b']} RA {l['RA']:.4f} Dec {l['Dec']:.4f}" + (' near' if not l['close'] else '')))
        for pl, n in l['nums'].items():
            iid = f'links:{i}:{pl}'
            if usable(iid):
                links.append((iid, l['a'], l['b'], l['kind'], 'number', f"{l['kind']} {l['a']}–{l['b']} {pl} {l[pl]:.5f} = {n['num']}"))
    for x in links: desc[x[0]] = x[5]
    hits = []    # (iid, sky, target, label, near)
    for i, s in enumerate(I['strikes']):
        iid = f'strikes:{i}'
        if usable(iid) or tg(iid) == 'duplicate':   # a sky body on its own natal place (= movement) still lands on that body for shapes
            hits.append((iid, s['sky'], s['target'], f"sky {s['sky']} -> {s['target']} {s['plane']} {s['value']:.5f} = {s['num']}", False))
    for i, c in enumerate(I['contacts']):
        iid = f'contacts:{i}'
        if usable(iid):
            hits.append((iid, c['sky'], c['target'], f"sky {c['sky']} on {c['target']} RA {c['RA']:.4f} Dec {c['Dec']:.4f}" +
                         (' RETURN' if c['return'] else '') + (' near' if c['band'] == 'near' else ''), c['band'] == 'near'))
    for x in hits: desc[x[0]] = x[3]
    moves = []
    for i, m in enumerate(I['movement']):
        iid = f'movement:{i}'
        if usable(iid):
            moves.append((iid, f"{m['chart']} {m['body']}", f"{m['chart']} {m['body']} moved {m['plane']} {m['value']:.5f} = {m['num']}"))
    for x in moves: desc[x[0]] = x[2]

    # ---------- Step 1: kinds per natal body (roots; near only if body already tight) ----------
    kinds = {}   # body -> kind -> list of (iid, near)
    def add(body, k, iid, near=False): kinds.setdefault(nb(body), {}).setdefault(k, []).append((iid, near))
    for iid, s, t, lab, near in hits:
        if is_root(iid): add(t, 'P', iid, near)
    for iid, body, lab in moves:
        if is_root(iid): add(body, 'M', iid)
    for i, r in enumerate(I['ratios']):
        iid = f'ratios:{i}'
        if is_root(iid):
            a, b = r['pair'].split('–'); desc[iid] = f"{r['chart']} {r['pair']} {r['plane']} sky {r['sky']:.4f} natal {r['natal']:.4f} {r['ratio']} ({r['err_pct']:.4f}%)" + (' near' if r['band'] == 'near' else '')
            for x in (a, b): add(f"{r['chart']} {x}", 'R', iid, r['band'] == 'near')
    for i, f in enumerate(I['pair_family']):
        iid = f'pair_family:{i}'
        if is_root(iid):
            a, b = f['pair'].split('–'); desc[iid] = f"{f['chart']} {f['pair']} {f['plane']} {f['tn']} {f['tn_value']:.4f} vs {f['base']} {f['base_value']:.4f} {f['ratio']} ({f['err_pct']:.4f}%)" + (' near' if f['band'] == 'near' else '')
            for x in (a, b): add(f"{f['chart']} {x}", 'R', iid, f['band'] == 'near')
    for i, s in enumerate(I['same_body']):
        iid = f'same_body:{i}'
        if is_root(iid):
            desc[iid] = f"same-body {s['body']} {s['plane']} {' : '.join(s['ratios'])} (worst {s['worst_pct']:.4f}%)"
            for c in 'HJ': add(f"{c} {s['body']}", 'B', iid)
    for i, p in enumerate(I['points']):
        iid = f'points:{i}'
        if p['eq_num'] and p['chart'] in 'HJ' and is_root(iid):
            desc[iid] = f"{p['chart']} {p['body']} Equator {p['eq']:.5f} = {p['eq_num']}"; add(f"{p['chart']} {p['body']}", 'E', iid)
    for i, e in enumerate(I['eq_ratios']):
        iid = f'eq_ratios:{i}'
        if is_root(iid):
            desc[iid] = f"Equator {e['body']} {e['pair']} {e['ratio']} ({e['err_pct']:.4f}%)" + (' near' if e['band'] == 'near' else '')
            for c in e['pair'].split('/'):
                if c in 'HJ': add(f"{c} {e['body']}", 'E', iid, e['band'] == 'near')
    for sec, lab in (('shared', 'shared'), ('pair_sets', 'pair set'), ('hj_ratios', 'horse:jockey')):
        for i, s in enumerate(I[sec]):
            iid = f'{sec}:{i}'
            if is_root(iid):
                near = s.get('band') == 'near'
                desc[iid] = f"{lab} {s['pair']} {s['plane']} H {s['horse']:.4f} J {s['jockey']:.4f}" + (f" {s.get('ratio','')}" if sec == 'hj_ratios' else '') + (' near' if near else '')
                a, b = s['pair'].split('–')
                for c in 'HJ':
                    for x in (a, b): add(f'{c} {x}', 'S', iid, near)
    tight_bodies = {b for b, K in kinds.items() if any(not n for its in K.values() for _, n in its)}
    for iid, a, b, kind, cn, lab in links:
        if kind == 'cross' and cn in ('close', 'near') and is_root(iid):
            if cn == 'near' and not (nb(a) in tight_bodies and nb(b) in tight_bodies): continue   # near link joins only if both ends are already in
            add(a, 'X', iid, cn == 'near'); add(b, 'X', iid, cn == 'near')
    # near admitted only when the body already has a tight kind
    body_kinds = {}
    for body, K in kinds.items():
        tight = {k for k, its in K.items() if any(not n for _, n in its)}
        joined = {k for k, its in K.items() if k not in tight and any(n for _, n in its)} if tight else set()
        body_kinds[body] = {'kinds': sorted(tight | joined), 'near_joined': sorted(joined),
                            'items': {k: [i for i, n in its if (not n) or (k in joined) or (k in tight)] for k, its in K.items() if k in tight | joined},
                            'near_unjoined': sorted({i for k, its in K.items() for i, n in its if n and not tight})}
    for b, v in body_kinds.items(): v['tight_kinds'] = len(v['kinds']) - len(v['near_joined'])
    hubs = sorted([b for b, v in body_kinds.items() if len(v['kinds']) >= 3], key=lambda b: (-body_kinds[b]['tight_kinds'], -len(body_kinds[b]['kinds'])))
    strong = [b for b in hubs if body_kinds[b]['tight_kinds'] >= STRONG]   # reported alongside (design threshold 3+ marks about half the bodies)

    # ---------- Step 2: webs ----------
    adj = {}
    def edge(a, b, iid):
        a, b = nb(a), nb(b)
        if a == b: return
        adj.setdefault(a, []).append((b, iid)); adj.setdefault(b, []).append((a, iid))
    for iid, a, b, kind, cn, lab in links:
        if is_root(iid) and (cn != 'near' or (body_kinds.get(nb(a)) and body_kinds.get(nb(b)))): edge(a, b, iid)
    for i, r in enumerate(I['ratios']):
        if is_root(f'ratios:{i}'): a, b = r['pair'].split('–'); edge(f"{r['chart']} {a}", f"{r['chart']} {b}", f'ratios:{i}')
    for sec in ('shared', 'pair_sets', 'hj_ratios'):
        for i, s in enumerate(I[sec]):
            if is_root(f'{sec}:{i}'):
                a, b = s['pair'].split('–')
                edge(f'H {a}', f'J {a}', f'{sec}:{i}'); edge(f'H {b}', f'J {b}', f'{sec}:{i}'); edge(f'H {a}', f'H {b}', f'{sec}:{i}'); edge(f'J {a}', f'J {b}', f'{sec}:{i}')
    for i, s in enumerate(I['same_body']):
        if is_root(f'same_body:{i}'): edge(f"H {s['body']}", f"J {s['body']}", f'same_body:{i}')
    for i, e in enumerate(I['eq_ratios']):
        if is_root(f'eq_ratios:{i}') and e['pair'] == 'H/J': edge(f"H {e['body']}", f"J {e['body']}", f'eq_ratios:{i}')
    for i, s in enumerate(I['splits']):
        if is_root(f'splits:{i}'): edge(s['moved'], s['to'], f'splits:{i}')
    seen, webs = set(), []
    for n in adj:
        if n in seen: continue
        comp, st = set(), [n]
        while st:
            x = st.pop()
            if x in comp: continue
            comp.add(x); st += [y for y, _ in adj[x]]
        seen |= comp; webs.append(comp)
    def spath(a, b):
        prev = {a: None}; q = [a]
        while q:
            x = q.pop(0)
            if x == b: break
            for y, iid in adj.get(x, []):
                if y not in prev: prev[y] = (x, iid); q.append(y)
        if b not in prev: return None
        out, x = [], b
        while prev[x]: px, iid = prev[x]; out.append(iid); x = px
        return out[::-1]
    web_out = []
    for w in sorted(webs, key=len, reverse=True):
        hw = [h for h in hubs if h in w]
        paths = []
        for a, b in itertools.combinations(hw, 2):
            p = spath(a, b)
            if p and len(p) <= 4: paths.append({'from': a, 'to': b, 'items': p})
        web_out.append({'bodies': sorted(w), 'size': len(w), 'hubs': hw, 'both_charts': len({x[0] for x in w}) == 2, 'hub_paths': paths})

    # ---------- Step 3: shapes ----------
    def roots_of(ids):
        out = set()
        for iid in ids:
            t = tags.get(iid, {})
            if t.get('tag') == 'duplicate' and t.get('of'): out |= roots_of([t['of']]); continue
            if t.get('tag') == 'derived' and 'chain' in t: out |= roots_of([c['id'] for c in t['chain'] if not c['id'].startswith(('axis', 'sky:'))])
            elif t.get('tag') == 'root': out.add(':'.join(iid.split(':')[:2]) if iid.startswith('links:') else iid)   # a link's close fact and its numbers = one root
        return out
    shapes = []
    def strict_item(iid):
        # tight version of an item: close (not near) links, strikes outside the Flat plane, no contacts, no near bands
        sec = iid.split(':')[0]
        if sec == 'links':
            l = I['links'][int(iid.split(':')[1])]; return len(iid.split(':')) == 3 or (l['close'] and not l.get('near'))
        if sec == 'strikes': return I['strikes'][int(iid.split(':')[1])]['plane'] != 'Flat'
        if sec == 'contacts': return False
        if sec in ('node',) or ':' not in iid: return True
        it = I[sec][int(iid.split(':')[1])] if isinstance(I.get(sec), list) else None
        return not (isinstance(it, dict) and it.get('band') == 'near')
    def shape(n, name, ids, **kw):
        bl = kw.pop('bodies', [])
        kw['strict'] = all(strict_item(i) for i in ids)
        shapes.append({'shape': n, 'name': name, 'items': ids, 'roots_behind': len(roots_of(ids)), 'bodies': bl,
                       'hub': any(nb(b) in hubs for b in bl), 'strong_hub': any(nb(b) in strong for b in bl), **kw})
    by_target = {}
    for iid, s, t, lab, near in hits: by_target.setdefault(t, []).append((s, iid))
    mv_by = {}
    for iid, body, lab in moves: mv_by.setdefault(body, []).append(iid)
    cross = [(iid, a, b, cn) for iid, a, b, kind, cn, lab in links if kind == 'cross' and cn in ('close', 'near')]
    for iid, a, b, cn in cross:
        xa, xb = a.split(' ', 1)[1], b.split(' ', 1)[1]
        A, B = by_target.get(a, []), by_target.get(b, [])
        if A and B:
            both = sorted({fold(x) for x, _ in A} & {fold(x) for x, _ in B})
            SA = {fold(s_) for s_, i in A if strict_item(i)}; SB = {fold(s_) for s_, i in B if strict_item(i)}
            sboth = sorted(SA & SB) if strict_item(iid) else []
            shape(1, 'cross link struck on both ends', [iid] + [i for _, i in A + B], bodies=[a, b], link=desc[iid],
                  strict_same_sky_both_ends=sboth, strict_multi=len(sboth) >= 2,
                  strikers_horse_end=sorted({s for s, _ in A}), strikers_jockey_end=sorted({s for s, _ in B}), same_sky_both_ends=both,
                  multi=len(both) >= 2)
        part = [i for s, i in A if s == xb] + [i for s, i in B if s == xa]
        if part: shape(2, 'partner strike', [iid] + part, bodies=[a, b], link=desc[iid])
        if xa != xb and f'S {xa}' in P and f'S {xb}' in P:
            g = gc(P[f'S {xa}'], P[f'S {xb}'])
            if g < SKY_PAIR_GC: shape(3, 'pair together in the sky', [iid], bodies=[a, b], link=desc[iid], sky_gc=round(g, 4))
        if mv_by.get(a) and mv_by.get(b): shape(4, 'both ends moved', [iid] + mv_by[a] + mv_by[b], bodies=[a, b], link=desc[iid])
        for end in (a, b):
            if mv_by.get(end): shape(5, 'movement onto a cross link', [iid] + mv_by[end], bodies=[end], link=desc[iid], moved=end)
    cset = {(a, b): iid for iid, a, b, cn in cross}
    for (a, b), iid in cset.items():
        xa, xb = a.split(' ', 1)[1], b.split(' ', 1)[1]
        if xa < xb and fold(xa) != fold(xb) and (f'H {xb}', f'J {xa}') in cset:
            shape(6, 'swap', [iid, cset[(f'H {xb}', f'J {xa}')]], bodies=[a, b, f'H {xb}', f'J {xa}'], pair=f'{xa}/{xb}')
    # 7 triangle: three natal bodies pairwise linked (close/near or number), one sky body on all three corners
    nbr = {}
    for iid, a, b, kind, cn, lab in links: nbr.setdefault(a, {}).setdefault(b, iid); nbr.setdefault(b, {}).setdefault(a, iid)
    seen_t = set()
    for a in nbr:
        for b in nbr[a]:
            for c in nbr[b]:
                if c != a and c in nbr[a]:
                    tri = tuple(sorted((a, b, c)))
                    if tri in seen_t: continue
                    seen_t.add(tri)
                    sk = set.intersection(*[{s for s, _ in by_target.get(x, [])} for x in tri])
                    for s in sorted(sk):
                        ids = [nbr[tri[0]][tri[1]], nbr[tri[0]][tri[2]], nbr[tri[1]][tri[2]]] + [i for x in tri for ss, i in by_target.get(x, []) if ss == s]
                        shape(7, 'triangle struck at every corner by one sky body', ids, bodies=list(tri), corners=list(tri), sky=s)
    # 8 same number / same ratio in both charts
    numH, numJ = {}, {}
    for i, p in enumerate(I['points']):
        if p['eq_num'] and p['chart'] in 'HJ' and usable(f'points:{i}'):
            (numH if p['chart'] == 'H' else numJ).setdefault(p['eq_num'], []).append(f'points:{i}')
    for iid, a, b, kind, cn, lab in links:
        if cn == 'number' and kind in 'HJ':
            n = lab.split(' = ')[-1]; (numH if kind == 'H' else numJ).setdefault(n, []).append(iid)
    for n in sorted(set(numH) & set(numJ), key=lambda x: (len(x), x)):
        for i, j in itertools.product(numH[n], numJ[n]):
            desc.setdefault(i, i); desc.setdefault(j, j)
            shape(8, 'same number in both charts', [i, j], number=n)
    rH, rJ = {}, {}
    for i, r in enumerate(I['ratios']):
        if usable(f'ratios:{i}'): (rH if r['chart'] == 'H' else rJ).setdefault(r['ratio'], []).append(f'ratios:{i}')
    for n in sorted(set(rH) & set(rJ)):
        for i, j in itertools.product(rH[n], rJ[n]): shape(8, 'same sky/natal ratio in both charts', [i, j], ratio=n)
    # 9 shared node
    nd = I['node']
    if nd['rahu_rahu_ra'] < NODE_SHARED or nd['rahu_ketu_ra'] < NODE_SHARED:
        shape(9, 'shared node', ['node'], rahu_rahu_ra=nd['rahu_rahu_ra'], rahu_ketu_ra=nd['rahu_ketu_ra'])
    # 10 split
    for i, s in enumerate(I['splits']):
        best = [r for r in (s['parts_ratio'], s['span_ratio']) if r and r[0] != '1' and r[1] <= SPLIT_TOL]
        if best and usable(f'splits:{i}'):
            desc[f'splits:{i}'] = (f"{s['moved']} -> {s['to']} {s['plane']} span {s['span']:.5f} = moved {s['moved_part']:.5f} ({s['move_num']}) + {s['other_part']:.5f}"
                                   f"  parts {s['parts_ratio']} span/other {s['span_ratio']}")
            shape(10, 'sky body divides a natal pair', [f'splits:{i}'], bodies=[s['moved'], s['to']], split=desc[f'splits:{i}'])
    # 11 joined same-body set
    for i, s in enumerate(I['same_body']):
        if is_root(f'same_body:{i}'):
            ks = set(body_kinds.get(f"H {fold(s['body'])}", {}).get('kinds', [])) | set(body_kinds.get(f"J {fold(s['body'])}", {}).get('kinds', []))
            if ks & {'X', 'R'}: shape(11, 'joined same-body set', [f'same_body:{i}'], bodies=[f"H {s['body']}", f"J {s['body']}"], joined_by=sorted(ks & {'X', 'R'}))
    # 12 inside-chart pair struck on both ends by 2+ sky bodies
    for iid, a, b, kind, cn, lab in links:
        if kind in 'HJ':
            A, B = by_target.get(a, []), by_target.get(b, [])
            both = sorted({s for s, _ in A} & {s for s, _ in B})
            sboth = sorted({fold(x) for x, i in A if strict_item(i)} & {fold(x) for x, i in B if strict_item(i)}) if strict_item(iid) else []
            if len(both) >= 2:
                shape(12, 'pair in one chart struck on both ends by 2+ sky bodies', [iid] + [i for s, i in A + B if s in both],
                      bodies=[a, b], link=desc[iid], sky=both, strict_sky=sboth, strict_multi=len(sboth) >= 2)
    # annotations
    ann = []
    for iid, a, b, kind, cn, lab in links:
        xa, xb = fold(a.split(' ', 1)[1]), fold(b.split(' ', 1)[1])
        if kind == 'cross' and (xa, xb) in RECUR_CROSS: ann.append({'item': iid, 'note': f'recurring cross link horse {xa} – jockey {xb}', 'what': desc[iid]})
        if {xa, xb} in RECUR_PAIRS: ann.append({'item': iid, 'note': f'recurring pair {xa}–{xb}', 'what': desc[iid]})
    for i, r in enumerate(I['ratios']):
        if usable(f'ratios:{i}') and {fold(x) for x in r['pair'].split('–')} in RECUR_PAIRS:
            ann.append({'item': f'ratios:{i}', 'note': f"recurring pair {r['pair']}", 'what': desc.get(f'ratios:{i}', r['pair'])})
    for i, sb in enumerate(I['same_body']):   # annotation: the Dec 9/4 : 5/4 : 9/5 same-body split (York node, Newmarket July / Exeter Chiron)
        if is_root(f'same_body:{i}') and sb['plane'] == 'Dec' and sorted(sb['ratios']) == ['5/4', '9/4', '9/5']:
            ann.append({'item': f'same_body:{i}', 'note': f"same-body Dec 9/4 : 5/4 : 9/5 on {fold(sb['body'])}", 'what': desc.get(f'same_body:{i}', '')})

    # ---------- pair focus (pair_focus_design.md): kinds of root item landing on one pair {A, B} ----------
    PF = {}
    def pk(a, b): return tuple(sorted((fold(a), fold(b))))
    def put(key, kind, iid, near=False):
        e = PF.setdefault(key, {'kinds': {}, 'near': {}})
        (e['near'] if near else e['kinds']).setdefault(kind, []).append(iid)
    SLOW = {'Eris', 'Sedna', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Transpluto'}
    for i, x in enumerate(I['shared']):
        a_, b_ = x['pair'].split('–')
        if is_root(f'shared:{i}') and not (a_ in SLOW and b_ in SLOW):   # (A) slow-body pairs are shared by age, not counted
            put(pk(a_, b_), 'shared', f'shared:{i}')
    for iid, a, b, kind, cn, lab in links:
        if kind == 'cross' and cn in ('close', 'near') and is_root(iid):
            put(pk(a.split(' ', 1)[1], b.split(' ', 1)[1]), 'cross', iid, cn == 'near')
    for s_ in shapes:
        if s_['shape'] in (1, 2, 4, 5) and len(s_['bodies']) >= 1:
            lk = s_['items'][0]
            l = I['links'][int(lk.split(':')[1])]
            key = pk(l['a'].split(' ', 1)[1], l['b'].split(' ', 1)[1])
            kname = {1: 'struck', 2: 'partner', 4: 'moved', 5: 'moved'}[s_['shape']]
            put(key, kname, lk + f"#shape{s_['shape']}", not s_['strict'])
    for i, r in enumerate(I['ratios']):
        if is_root(f'ratios:{i}'): put(pk(*r['pair'].split('–')), f"ratio {r['chart']}", f'ratios:{i}', r['band'] == 'near')
    for i, x in enumerate(I['pair_sets']):
        if is_root(f'pair_sets:{i}'): put(pk(*x['pair'].split('–')), 'set', f'pair_sets:{i}')
    for i, x in enumerate(I['hj_ratios']):
        if is_root(f'hj_ratios:{i}'): put(pk(*x['pair'].split('–')), 'h:j', f'hj_ratios:{i}', x['band'] == 'near')
    for i, x in enumerate(I['pair_family']):
        if is_root(f'pair_family:{i}'): put(pk(*x['pair'].split('–')), 'family', f'pair_family:{i}', x['band'] == 'near')
    sbody = {}
    for i, x in enumerate(I['same_body']):
        if is_root(f'same_body:{i}'): sbody.setdefault(fold(x['body']), []).append(f'same_body:{i}')
    for key in list(PF):
        for iid in sorted({i for b in set(key) for i in sbody.get(b, [])}, key=lambda s: int(s.split(':')[1])):   # item order, not set order (run-to-run stable)
            put(key, 'same body', iid)
        a, b = key
        if a != b and f'S {a if a != "Node" else "Rahu"}' in P and f'S {b if b != "Node" else "Rahu"}' in P:
            ga = [P[f'S {x}'] for x in (['Rahu', 'Ketu'] if a == 'Node' else [a])]; gb = [P[f'S {x}'] for x in (['Rahu', 'Ketu'] if b == 'Node' else [b])]
            g = min(gc(x, y) for x in ga for y in gb)
            if g < SKY_PAIR_GC: PF[key]['kinds'].setdefault('sky', []).append(f'sky-gc {g:.4f}')
    def ctight(ids):   # (C) tightness of the pair's tightest close cross link: min(RA/1.5, Dec/0.3)
        vals = [min(I['links'][int(i.split(':')[1])]['RA'] / 1.5, I['links'][int(i.split(':')[1])]['Dec'] / 0.3) for i in ids if i.startswith('links:')]
        return round(min(vals), 4) if vals else 9.0
    def stight(ids):
        vals = [I['shared'][int(i.split(':')[1])]['diff_pct'] for i in ids if i.startswith('shared:')]
        return round(min(vals), 4) if vals else None
    focus = [{'pair': '–'.join(k), 'n': len(v['kinds']), 'kinds': v['kinds'], 'near': v['near'],
              'cross_tight': ctight(v['kinds'].get('cross', [])), 'shared_pct': stight(v['kinds'].get('shared', []))}
             for k, v in PF.items() if 'cross' in v['kinds']]          # (B) only pairs joined by a tight cross link
    focus.sort(key=lambda x: (-x['n'], x['cross_tight'], x['pair']))
    for x in focus:
        for k, ids in list(x['kinds'].items()) + list(x['near'].items()):
            for iid in ids:
                base = iid.split('#')[0]
                if base not in desc and base.startswith('same_body:'):
                    sb = I['same_body'][int(base.split(':')[1])]; desc[base] = f"same-body {sb['body']} {sb['plane']} {' : '.join(sb['ratios'])} (worst {sb['worst_pct']:.4f}%)"
    return {'version': VERSION, 'runner': I['runner'], 'workbook': I['workbook'], 'bodies': body_kinds, 'hubs': hubs, 'strong_hubs': strong, 'webs': web_out,
            'shapes': shapes, 'annotations': ann, 'desc': desc, 'pair_focus': [x for x in focus if x['n'] >= 3] or focus[:3]}   # v1.4: A slow-shared out, B cross required, C tightness order

def text(R):
    d = R['desc']; D = lambda i: d.get(i, i)
    L = [f"== {R['runner']}   [{R['workbook']}, {R['version']}]", f"-- strong hubs (5+ tight kinds): {', '.join(R['strong_hubs']) or '-'}",
         '-- hubs (3+ kinds: P position, M movement, R ratio, B same body, E Equator, S shared, X cross), most tight kinds first']
    for h in R['hubs']:
        v = R['bodies'][h]; L.append(f"   {h:14s} {''.join(v['kinds'])}  tight {v['tight_kinds']}" + (f"  (near joined: {''.join(v['near_joined'])})" if v['near_joined'] else ''))
        for k in v['kinds']:
            for i in v['items'][k][:4]: L.append(f"        {k}: {D(i)}")
    L.append('-- webs')
    for w in R['webs'][:3]:
        L.append(f"   size {w['size']} both charts {w['both_charts']} hubs {', '.join(w['hubs']) or '-'}")
        for p in w['hub_paths'][:6]: L.append(f"      {p['from']} .. {p['to']}: " + ' | '.join(D(i) for i in p['items']))
    L.append('-- shapes')
    for s in sorted(R['shapes'], key=lambda s: (s['shape'], -s['hub'])):
        extra = {k: v for k, v in s.items() if k not in ('shape', 'name', 'items', 'roots_behind', 'hub', 'strong_hub')}
        L.append(f"   [{s['shape']:2d}] {s['name']}{' (STRONG HUB)' if s['strong_hub'] else ' (HUB)' if s['hub'] else ''}  roots {s['roots_behind']}  " + '; '.join(f'{k}={v}' for k, v in extra.items()))
        for i in s['items'][:6]: L.append(f"        {D(i)}")
    L.append('-- pair focus (kinds of root item on one pair; near beside, not counted)')
    for x in R['pair_focus'][:8]:
        L.append(f"   {x['pair']:22s} {x['n']} kinds: {', '.join(x['kinds'])}  cross tightness {x['cross_tight']}" + (f", shared {x['shared_pct']}%" if x['shared_pct'] is not None else '') + (f"   near: {', '.join(x['near'])}" if x['near'] else ''))
        for k, ids in x['kinds'].items(): L.append(f"        {k}: " + '; '.join(D(i.split('#')[0]) for i in ids[:2]))
    if R['annotations']:
        L.append('-- annotations (recurring from earlier winners; not weighted)')
        for a in R['annotations']: L.append(f"   {a['note']}: {a['what']}")
    return '\n'.join(L)

if __name__ == '__main__':
    race = sys.argv[1].rstrip('/').split('/')[-1]
    D1, D2, O = f'docs/classic/{race}/layer1', f'docs/classic/{race}/layer2', f'docs/classic/{race}/layer3'
    os.makedirs(O, exist_ok=True)
    for f in sorted(glob.glob(f'{D1}/P*.json')):
        t = os.path.basename(f)[:-5]
        R = run(json.load(open(f)), json.load(open(f'{D2}/{t}.json')))
        json.dump(R, open(f'{O}/{t}.json', 'w'), indent=1)
        open(f'{O}/{t}.txt', 'w').write(text(R) + '\n')
        cnt = {}
        for s in R['shapes']: cnt[s['shape']] = cnt.get(s['shape'], 0) + 1
        print(f"{t} {R['runner']}: hubs {len(R['hubs'])} strong {len(R['strong_hubs'])} shapes " + ' '.join(f'{k}:{v}' for k, v in sorted(cnt.items())))
