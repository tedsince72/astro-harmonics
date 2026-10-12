#!/usr/bin/env python3
"""layer2_roots.py RACE   — Layer 2 of the layered reader (design: docs/classic/layer2_design.md, approved by Eddie 12 Oct 2026).

Reads docs/classic/<RACE>/layer1/P*.json (+ sky.json, sky_close.json). Removes nothing: tags every Layer 1 item as
  root | derived (with chain) | mirror | duplicate | from_numbers | race_level
Rule 1  numbers on a line add up: in Dec (Equator = point 0) and RA (circle), points joined by whole/ninth items form groups; an item
        that closes a loop is DERIVED from the chain of the others. Roots chosen in priority order
        0 node axis (structural) > 1 Equator value > 2 natal link inside a chart > 3 cross link > 4 movement > 5 sky number > 6 strike,
        ties by smaller |offset|. The derived number must equal the signed sum of the chain (in ninths; RA modulo 360) or it stays root
        and is flagged 'loop_mismatch'. Flat and GC items are always roots.
Rule 2  node mirror: Ketu items that copy a Rahu item (RA via the 180 axis, Equator values, same-body sets, Equator ratios) -> mirror.
Rule 3  a strike of sky X on its own natal X is the movement item -> duplicate.
Rule 4  a ratio whose values are themselves whole/ninth number items -> from_numbers.
Rule 5  sky numbers and close sky pairs are the same for every runner -> race_level (still used as chain links).
Output: docs/classic/<RACE>/layer2/P*.json, P*.txt"""
import sys, os, glob, json, re
VERSION = 'L2 v1.1 (12 Oct 2026)'
PRIO = {'axis': 0, 'equator': 1, 'natal': 2, 'cross': 3, 'movement': 4, 'skynum': 5, 'strike': 6}
FULL = 3240  # 360 degrees in ninths

def ninths(lbl):
    if '/' in lbl: return int(lbl.split('/')[0])
    return int(lbl) * 9

class DSU:
    def __init__(self): self.p = {}
    def f(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def u(self, a, b): self.p[self.f(a)] = self.f(b)

def coords(inv):
    C = {}
    for p in inv['points']:
        C[f"{p['chart']} {p['body']}"] = (p['ra'], p['dec'])
    C['EQ'] = (None, 0.0)
    return C

def wrap(x): return (x + 180) % 360 - 180

def run_runner(inv, skynums, skyclose):
    C = coords(inv)
    tags = {}  # id -> dict
    def tag(i, t, **kw): tags[i] = {'tag': t, **kw}

    # ---------- collect number edges per plane ----------
    edges = {'Dec': [], 'RA': []}
    def add(plane, a, b, lbl, off, kind, iid, value):
        edges[plane].append({'a': a, 'b': b, 'n': ninths(lbl), 'num': lbl, 'off': abs(off), 'kind': kind, 'id': iid, 'value': value})
    for i, p in enumerate(inv['points']):
        if p['eq_num']:
            add('Dec', f"{p['chart']} {p['body']}", 'EQ', p['eq_num'], p['eq_off'], 'equator', f'points:{i}', p['eq'])
    for i, l in enumerate(inv['links']):
        kind = 'cross' if l['kind'] == 'cross' else 'natal'
        for pl in ('Dec', 'RA'):
            if pl in l['nums']:
                add(pl, l['a'], l['b'], l['nums'][pl]['num'], l['nums'][pl]['off'], kind, f'links:{i}:{pl}', l[pl])
    for i, m in enumerate(inv['movement']):
        if m['plane'] in ('Dec', 'RA'):
            add(m['plane'], f"S {m['body']}", f"{m['chart']} {m['body']}", m['num'], m['off'], 'movement', f'movement:{i}', m['value'])
    for i, s in enumerate(skynums):
        if s['plane'] in ('Dec', 'RA'):
            a, b = s['pair'].split('–')
            add(s['plane'], f'S {a}', f'S {b}', s['num'], s['off'], 'skynum', f'sky:{i}', s['value'])
    for i, s in enumerate(inv['strikes']):
        if s['same_body']: continue  # Rule 3
        if s['plane'] in ('Dec', 'RA'):
            add(s['plane'], f"S {s['sky']}", s['target'], s['num'], s['off'], 'strike', f'strikes:{i}', s['value'])
    # node axis (structural, RA only): Rahu–Ketu 180 in each chart
    for c in 'SHJ':
        edges['RA'].append({'a': f'{c} Rahu', 'b': f'{c} Ketu', 'n': 1620, 'num': '180', 'off': 0.0, 'kind': 'axis', 'id': f'axis:{c}', 'value': 180.0})

    groups = {}
    for plane, E in edges.items():
        E.sort(key=lambda e: (PRIO[e['kind']], e['off'], 'Ketu' in e['a'] or 'Ketu' in e['b']))   # Ketu after Rahu on ties (checker)
        dsu = DSU(); tree = {}   # adjacency of accepted root edges: node -> [(nbr, signed ninths, edge)]
        def signed(e, frm):
            to = e['b'] if frm == e['a'] else e['a']
            if plane == 'Dec':
                d = C[to][1] - C[frm][1]
            else:
                d = wrap(C[to][0] - C[frm][0])
            return to, (e['n'] if d >= 0 else -e['n'])
        def path(x, y):
            # BFS in the forest from x to y, returning list of (edge, signed ninths along the path)
            prev = {x: None}; q = [x]
            while q:
                n = q.pop(0)
                if n == y: break
                for nb, sn, e in tree.get(n, []):
                    if nb not in prev: prev[nb] = (n, sn, e); q.append(nb)
            if y not in prev: return None
            out = []; n = y
            while prev[n]: pn, sn, e = prev[n]; out.append((e, sn)); n = pn
            return out[::-1]
        for e in E:
            ra, rb = dsu.f(e['a']), dsu.f(e['b'])
            if ra != rb:
                dsu.u(e['a'], e['b'])
                to, sn = signed(e, e['a'])
                tree.setdefault(e['a'], []).append((e['b'], sn, e)); tree.setdefault(e['b'], []).append((e['a'], -sn, e))
                if e['kind'] != 'axis': tag(e['id'], 'root', plane=plane)
            else:
                ch = path(e['a'], e['b'])
                tot = sum(sn for _, sn in ch)
                implied = abs(tot) if plane == 'Dec' else min(tot % FULL, FULL - tot % FULL)
                if implied == e['n']:
                    chain = [{'id': c['id'], 'kind': c['kind'], 'a': c['a'], 'b': c['b'], 'num': c['num']} for c, _ in ch]
                    t = 'mirror' if (len(ch) == 2 and any(c['kind'] == 'axis' for c, _ in ch)) else 'derived'   # mirror = axis + one Rahu item
                    tag(e['id'], t, plane=plane, chain=chain)
                else:
                    tag(e['id'], 'root', plane=plane, flag='loop_mismatch', implied_ninths=implied, own_ninths=e['n'])
        comp = {}
        for e in E:
            for n in (e['a'], e['b']): comp.setdefault(dsu.f(n), set()).add(n)
        groups[plane] = sorted([sorted(v) for v in comp.values() if len(v) > 2], key=len, reverse=True)

    # ---------- Rule 2 mirrors outside the graph ----------
    for i, p in enumerate(inv['points']):
        if p['body'] == 'Ketu' and p['eq_num']: tags[f'points:{i}'] = {'tag': 'mirror', 'of': f"{p['chart']} Rahu Equator"}
    rahu_sb = {(s['plane'], tuple(s['ratios'])) for s in inv['same_body'] if s['body'] == 'Rahu'}
    for i, s in enumerate(inv['same_body']):
        if s['body'] == 'Ketu' and (s['plane'], tuple(s['ratios'])) in rahu_sb: tag(f'same_body:{i}', 'mirror', of='Rahu same-body set')
    rahu_er = {(e['pair'], e['ratio']) for e in inv['eq_ratios'] if e['body'] == 'Rahu'}
    for i, e in enumerate(inv['eq_ratios']):
        if e['body'] == 'Ketu' and (e['pair'], e['ratio']) in rahu_er: tag(f'eq_ratios:{i}', 'mirror', of='Rahu Equator ratio')

    # ---------- Rule 3 duplicates ----------
    mv = {(m['chart'], m['body'], m['plane']): i for i, m in enumerate(inv['movement'])}
    for i, s in enumerate(inv['strikes']):
        if s['same_body']:
            c = s['target'].split()[0]
            j = mv.get((c, s['sky'], s['plane']))
            tag(f'strikes:{i}', 'duplicate' if j is not None else 'root', of=f'movement:{j}' if j is not None else None)

    # ---------- Rule 4 from numbers ----------
    def nat_num(c, a, b, pl):
        for l in inv['links']:
            if l['kind'] == c and {l['a'], l['b']} == {f'{c} {a}', f'{c} {b}'} and pl in l['nums']: return True
        return False
    def cross_num(a, b, pl):
        for l in inv['links']:
            if l['kind'] == 'cross' and l['a'] == f'H {a}' and l['b'] == f'J {b}' and pl in l['nums']: return True
        return False
    skyset = {(frozenset(s['pair'].split('–')), s['plane']) for s in skynums}
    def sky_num(a, b, pl): return (frozenset((a, b)), pl) in skyset
    def strike_num(sky_, tgt, pl): return any(s['sky'] == sky_ and s['target'] == tgt and s['plane'] == pl for s in inv['strikes'])
    def move_num(c, b, pl): return any(m['chart'] == c and m['body'] == b and m['plane'] == pl for m in inv['movement'])
    eqp = {(p['chart'], p['body']) for p in inv['points'] if p['eq_num']}
    for i, r in enumerate(inv['ratios']):
        a, b = r['pair'].split('–')
        if sky_num(a, b, r['plane']) and nat_num(r['chart'], a, b, r['plane']): tag(f'ratios:{i}', 'from_numbers')
    for i, e in enumerate(inv['eq_ratios']):
        x, y = e['pair'].split('/')
        if f'eq_ratios:{i}' not in tags and (x, e['body']) in eqp and (y, e['body']) in eqp: tag(f'eq_ratios:{i}', 'from_numbers')
    for i, h in enumerate(inv['hj_ratios']):
        a, b = h['pair'].split('–')
        if nat_num('H', a, b, h['plane']) and nat_num('J', a, b, h['plane']): tag(f'hj_ratios:{i}', 'from_numbers')
    for i, f in enumerate(inv['pair_family']):
        a, b = f['pair'].split('–'); c = f['chart']
        tn_is = strike_num(a, f'{c} {b}', f['plane']) if f['tn'].startswith('sky') else strike_num(b, f'{c} {a}', f['plane'])
        base_is = nat_num(c, a, b, f['plane']) if f['base'] == 'NN' else sky_num(a, b, f['plane'])
        if tn_is and base_is: tag(f'pair_family:{i}', 'from_numbers')
    for i, s in enumerate(inv['same_body']):
        if f'same_body:{i}' in tags: continue
        b, pl = s['body'], s['plane']
        if pl == 'EqValue':
            ok = all((c, b) in eqp for c in 'SHJ')
        else:
            ok = move_num('H', b, pl) and move_num('J', b, pl) and cross_num(b, b, pl)
        if ok: tag(f'same_body:{i}', 'from_numbers')
    for i, s in enumerate(inv['splits']):
        if s['other_num']: tag(f'splits:{i}', 'from_numbers')

    # ---------- everything else is a root ----------
    for sec in ('points', 'links', 'strikes', 'ratios', 'movement', 'same_body', 'shared', 'eq_ratios', 'pair_sets', 'pair_family',
                'splits', 'contacts', 'hj_ratios'):
        for i, it in enumerate(inv.get(sec, [])):
            if sec == 'points' and not it['eq_num']: continue
            if sec == 'links':
                ids = [f'links:{i}:{pl}' for pl in it['nums'] if pl in ('Dec', 'RA')]
                for pl in it['nums']:
                    if pl not in ('Dec', 'RA'): tags.setdefault(f'links:{i}:{pl}', {'tag': 'root', 'plane': pl})
                if not it['nums'] or it['close'] or it.get('near'): tags.setdefault(f'links:{i}', {'tag': 'root', 'what': 'close/near'})
                continue
            tags.setdefault(f'{sec}:{i}', {'tag': 'root'})
    tags['node'] = {'tag': 'root'}
    # Rule 5: sky numbers and sky Equator values are the same for every runner -> race_level (graph role kept for reference)
    for i in range(len(skynums)):
        g = tags.get(f'sky:{i}'); tags[f'sky:{i}'] = {'tag': 'race_level', **({'graph': g['tag'], **{k: v for k, v in g.items() if k != 'tag'}} if g else {})}
    for i, p in enumerate(inv['points']):
        if p['chart'] == 'S' and p['eq_num']:
            g = tags.get(f'points:{i}'); tags[f'points:{i}'] = {'tag': 'race_level', **({'graph': g['tag'], **{k: v for k, v in g.items() if k != 'tag'}} if g else {})}
    for i in range(len(skyclose)): tags[f'sky_close:{i}'] = {'tag': 'race_level'}
    counts = {}
    for i, t in tags.items():
        sec = i.split(':')[0]
        counts.setdefault(sec, {}).setdefault(t['tag'], 0); counts[sec][t['tag']] += 1
    return {'version': VERSION, 'runner': inv['runner'], 'workbook': inv['workbook'], 'tags': tags, 'groups': groups, 'counts': counts}

def describe(inv, skynums, iid):
    sec, i, *rest = iid.split(':')
    if sec == 'axis': return f'node axis ({i})'
    if sec == 'sky':
        s = skynums[int(i)]; return f"sky {s['pair']} {s['plane']} {s['value']:.5f} = {s['num']}"
    it = inv[sec][int(i)]
    if sec == 'points': return f"{it['chart']} {it['body']} Equator {it['eq']:.5f} = {it['eq_num']}"
    if sec == 'links': pl = rest[0] if rest else 'close'; return f"{it['kind']} {it['a']}–{it['b']} {pl} " + (f"{it[pl]:.5f} = {it['nums'][pl]['num']}" if rest else '')
    if sec == 'strikes': return f"sky {it['sky']} -> {it['target']} {it['plane']} {it['value']:.5f} = {it['num']}"
    if sec == 'movement': return f"{it['chart']} {it['body']} moved {it['plane']} {it['value']:.5f} = {it['num']}"
    return f"{sec} {it}"

def text(res, inv, skynums):
    L = [f"== {res['runner']}   [{res['workbook']}, {res['version']}]", '-- counts by section: ' +
         '; '.join(f"{s} " + ', '.join(f'{k} {v}' for k, v in sorted(c.items())) for s, c in sorted(res['counts'].items()))]
    for plane in ('Dec', 'RA'):
        L.append(f"-- {plane} groups (3+ points joined by numbers)")
        for g in res['groups'][plane]: L.append('   ' + ', '.join(g))
    L.append('-- derived items (with chain)')
    for iid, t in res['tags'].items():
        if t['tag'] in ('derived', 'mirror') and 'chain' in t:
            L.append(f"   {t['tag'].upper():8s} {describe(inv, skynums, iid)}")
            for c in t['chain']: L.append(f"            <- {c['kind']:9s} {describe(inv, skynums, c['id'])}")
    flagged = [(i, t) for i, t in res['tags'].items() if t.get('flag')]
    if flagged:
        L.append('-- loop mismatches (kept as roots)')
        for i, t in flagged: L.append(f"   {describe(inv, skynums, i)}  implied {t['implied_ninths']}/9 own {t['own_ninths']}/9")
    L.append('-- roots among number items (Dec/RA)')
    for iid, t in res['tags'].items():
        if t['tag'] == 'root' and t.get('plane') in ('Dec', 'RA') and not t.get('flag'):
            L.append(f"   {describe(inv, skynums, iid)}")
    return '\n'.join(L)

if __name__ == '__main__':
    race = sys.argv[1].rstrip('/').split('/')[-1]
    D = f'docs/classic/{race}/layer1'; O = f'docs/classic/{race}/layer2'; os.makedirs(O, exist_ok=True)
    skynums = json.load(open(f'{D}/sky.json'))
    skyclose = json.load(open(f'{D}/sky_close.json')) if os.path.exists(f'{D}/sky_close.json') else []
    for f in sorted(glob.glob(f'{D}/P*.json')):
        t = os.path.basename(f)[:-5]
        inv = json.load(open(f))
        res = run_runner(inv, skynums, skyclose)
        json.dump(res, open(f'{O}/{t}.json', 'w'), indent=1)
        open(f'{O}/{t}.txt', 'w').write(text(res, inv, skynums) + '\n')
        nd = sum(1 for x in res['tags'].values() if x['tag'] == 'derived'); nm = sum(1 for x in res['tags'].values() if x['tag'] == 'mirror')
        nf = sum(1 for x in res['tags'].values() if x['tag'] == 'from_numbers'); nr = sum(1 for x in res['tags'].values() if x['tag'] == 'root')
        mm = sum(1 for x in res['tags'].values() if x.get('flag'))
        print(f"{t} {res['runner']}: roots {nr} derived {nd} mirror {nm} from_numbers {nf} mismatch {mm}")
