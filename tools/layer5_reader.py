#!/usr/bin/env python3
"""layer5_reader.py RACE   — Layer 5 of the layered reader (design: docs/classic/layer5_design.md, approved by Eddie 12 Oct 2026).

Writes a plain reading per runner from Layers 1–4, by fixed rules (every sentence points to an exact item and value). Blind: never reads
finishing positions. No score, no ranking; racecard order.
Sections: 1 only this runner (strict, broad; shared with one other)  2 the web, hub by hub  3 shapes with detail and field standing
          4 what is arithmetic (Layer 2 chains)  5 same pair elsewhere  6 recurring pairs  7 near items that joined
Output: docs/classic/<RACE>/layer5/P*.md and race.md"""
import sys, os, re, glob, json
VERSION = 'L5 v1.1 (12 Oct 2026, pair focus)'
NAMES = {'pair focus': 'the most-lit pair in the field (most different kinds of item on one pair)', 1: 'cross link struck on both ends', 2: 'partner strike (the sky partner lands on the other end)', 3: 'the pair is together in the sky',
         4: 'both ends of the cross link have moved', 5: 'a movement lands on a cross link', 6: 'swap', 7: 'triangle struck at every corner by one sky body',
         8: 'same number / ratio in both charts', 9: 'shared node', 10: 'a sky body divides a natal pair', 11: 'same-body set joined to the web',
         12: 'pair in one chart struck on both ends by 2+ sky bodies', '1m': 'cross link struck on both ends by 2+ different sky bodies',
         '12m': 'pair in one chart struck on both ends by 2+ sky bodies'}
KINDS = {'P': 'a sky body on it', 'M': 'movement', 'R': 'ratio', 'B': 'same-body set', 'E': 'Equator', 'S': 'shared with the other chart', 'X': 'cross link'}
CAP_SHAPES, CAP_HUBS, CAP_ITEMS = 12, 6, 3

def runner_words(name):
    h, j = name.split(' / ')
    h = re.sub(r'^\d+\s+', '', h); j = re.sub(r'^\d+\s+', '', j)
    return h, j.split()[-1]

def words(s, sur):
    s = re.sub(r'(?<![A-Za-z])H (?=[A-Z])', 'horse ', s)
    s = re.sub(r'(?<![A-Za-z])J (?=[A-Z])', f'{sur} ', s)
    s = re.sub(r'(?<![A-Za-z])S (?=[A-Z])', 'sky ', s)
    return s.replace('cross horse', 'horse').replace('horse horse', 'horse').replace(f'{sur} {sur}', sur).replace(f'J {sur}', sur)

def describe(inv, sky, iid, desc3):
    if iid in desc3: return desc3[iid]
    sec, i, *rest = iid.split(':') + ['']
    if sec == 'axis': return f'node axis ({i})'
    if sec == 'sky': s = sky[int(i)]; return f"sky {s['pair']} {s['plane']} {s['value']:.5f} = {s['num']}"
    if sec == 'node': return 'shared node'
    it = inv[sec][int(i)]
    if sec == 'points': return f"{it['chart']} {it['body']} Equator {it['eq']:.5f} = {it['eq_num']}"
    if sec == 'links':
        pl = rest[0]
        return f"{it['a']}–{it['b']} " + (f"{pl} {it[pl]:.5f} = {it['nums'][pl]['num']}" if pl else f"RA {it['RA']:.4f} Dec {it['Dec']:.4f}")
    if sec == 'strikes': return f"sky {it['sky']} -> {it['target']} {it['plane']} {it['value']:.5f} = {it['num']}"
    if sec == 'movement': return f"{it['chart']} {it['body']} moved {it['plane']} {it['value']:.5f} = {it['num']}"
    if sec == 'contacts': return f"sky {it['sky']} on {it['target']} RA {it['RA']:.4f} Dec {it['Dec']:.4f}"
    if sec == 'splits': return f"{it['moved']} -> {it['to']} {it['plane']} span {it['span']:.5f} = {it['moved_part']:.5f} + {it['other_part']:.5f}"
    return f'{sec} {i}'

def simple_key(s, x):
    """ordering inside a shape type: tighter first; for splits (shape 10) the simpler ratio first (p+q), then the error"""
    if s['shape'] == 10:
        m = re.search(r"parts \['?([0-9/]+)'?, ([0-9.]+)\] span/other \['?([0-9/]+)'?, ([0-9.]+)\]", s.get('split', ''))
        if m:
            c = [(sum(int(v) for v in r.split('/')), float(e)) for r, e in ((m.group(1), m.group(2)), (m.group(3), m.group(4))) if r != '1' and float(e) <= 0.25]
            if c: return min(c)
    return (0, x['tight_value'])

def read_runner(P, inv, T, R, F, sky, field_n):
    horse, sur = runner_words(R['runner'])
    W = lambda s: words(s, sur)
    D = lambda i: W(describe(inv, sky, i, R['desc']))
    tags = T['tags']
    mine = [x for x in F['instances'] if x['runner'] == P]   # same order as R['shapes']
    cited = []
    L = [f"# {R['runner']}  ({P})", f"_{VERSION}; blind — no finishing positions; every line points to Layer 1–4 items._", '']
    # 1 only this runner
    L.append('## 1. What only this runner has')
    o = F['only'][P]; any1 = False
    for lvl in ('strict', 'broad'):
        for k in o[lvl]:
            if lvl == 'broad' and k in o['strict']: continue
            kk = int(k) if k.isdigit() else k
            if k == 'pair focus':
                top = R['pair_focus'][0]; any1 = True
                L.append(f"- **Only runner in the field: {NAMES[k]}** — {W(top['pair'])}, {top['n']} kinds: {', '.join(top['kinds'])}" +
                         (f"; the same pair in other runners: {', '.join(f'{p} {n}' for p, n in F['pair_focus'][P]['same_pair_elsewhere'].items())}" if F['pair_focus'][P]['same_pair_elsewhere'] else '; not lit in any other runner'))
                continue
            base = 1 if k == '1m' else 12 if k == '12m' else kk
            if k in ('1m', '12m'):   # 2+ sky bodies: strict level is judged by strict_multi, not by every item being tight
                insts = [(s, x) for s, x in zip(R['shapes'], mine) if s['shape'] == base and (s.get('strict_multi') if lvl == 'strict' else (s.get('multi', True)))]
            else:
                insts = [(s, x) for s, x in zip(R['shapes'], mine) if s['shape'] == base and (lvl == 'broad' or s['strict'])]
            insts.sort(key=lambda sx: simple_key(sx[0], sx[1]))
            for s, x in insts[:3]:
                any1 = True; cited += s['items']
                L.append(f"- **Only runner in the field ({lvl}): {NAMES[kk]}** — " + '; '.join(D(i) for i in s['items'][:4]) + f"  _(rests on {s['roots_behind']} independent facts)_")
    for k in o['with_one_other_strict']:
        kk = int(k) if k.isdigit() else k
        other = [p for p in F['table']['strict'][k] if p != P]
        for s in [s for s in R['shapes'] if s['shape'] == (1 if k == '1m' else 12 if k == '12m' else kk) and s['strict']][:1]:
            any1 = True; cited += s['items']
            L.append(f"- Shared with one other runner ({', '.join(other)}), strict: {NAMES[kk]} — " + '; '.join(D(i) for i in s['items'][:3]))
    if not any1: L.append('- Nothing that no other runner has.')
    L.append('')
    # 2 the web
    L.append('## 2. The web — the most-lit pair first, then hub by hub')
    for x in R.get('pair_focus', [])[:2]:
        L.append(f"- **pair {W(x['pair'])}** — {x['n']} kinds: {', '.join(x['kinds'])}" + (f" (near, not counted: {', '.join(x['near'])})" if x['near'] else ''))
        for k, ids in x['kinds'].items():
            its = [i.split('#')[0] for i in ids[:2]]; cited += its
            L.append(f"    - {k}: " + ('; '.join(D(i) if not i.startswith('sky-gc') else 'together in the sky, great circle ' + i.split()[1] for i in its)))
    hubs = list(R['strong_hubs'])
    for w in R['webs']:
        if any(h in w['bodies'] for h in hubs): hubs += [h for h in w['hubs'] if h not in hubs]
    if not hubs: hubs = R['hubs'][:3]
    for h in hubs[:CAP_HUBS]:
        v = R['bodies'][h]
        L.append(f"- **{W(h)}** — {len(v['kinds'])} kinds ({v['tight_kinds']} tight){' — strong hub' if h in R['strong_hubs'] else ''}: " +
                 ', '.join(KINDS[k] for k in v['kinds']))
        for k in v['kinds']:
            its = v['items'][k][:2]; cited += its
            L.append(f"    - {KINDS[k]}: " + '; '.join(D(i) for i in its))
    paths = [p for w in R['webs'] for p in w['hub_paths'] if p['from'] in hubs[:CAP_HUBS] and p['to'] in hubs[:CAP_HUBS]]
    for p in paths[:4]:
        L.append(f"- {W(p['from'])} joins {W(p['to'])} through: " + ' | '.join(D(i) for i in p['items']))
    L.append('')
    # 3 shapes
    L.append('## Equator values (natal whole / ninth)')
    eqs = [f"{W(p['chart'] + ' ' + p['body'])} {p['dec']:+.5f} = {p['eq_num']}" for p in inv['points'] if p['eq_num'] and p['chart'] in 'HJ' and p['body'] != 'Ketu']
    L.append('- ' + '; '.join(eqs) if eqs else '- none')
    L.append('')
    L.append('## 3. Shapes')
    def field_count(s): return len(F['table']['strict' if s['strict'] else 'broad'].get(str(s['shape']), {}))
    order = sorted(range(len(R['shapes'])), key=lambda i: (not R['shapes'][i]['strict'], field_count(R['shapes'][i])) + simple_key(R['shapes'][i], mine[i]))
    first, rest, seen_t = [], [], set()   # one of each shape type first, then the rest
    for i in order:
        k = (R['shapes'][i]['shape'], R['shapes'][i]['strict'])
        (rest if k in seen_t else first).append(i); seen_t.add(k)
    shown = 0
    for i in first + rest:
        if shown >= CAP_SHAPES: break
        s, x = R['shapes'][i], mine[i]
        lvl = 'strict' if s['strict'] else 'broad'
        same = [y for y in F['instances'] if y['shape'] == s['shape'] and (y['strict'] or lvl == 'broad')]
        rank = sorted({y['tight_value'] for y in same}).index(x['tight_value']) + 1 if s['shape'] not in (7, 8, 12) else None
        fc = field_count(s)
        stand = f"{fc} of {field_n} runners have this shape ({lvl})" + (f"; tightness rank {rank} of {len(set(y['tight_value'] for y in same))} instances" if rank else '')
        extra = ''
        if s['shape'] in (1, 12): extra = f"; sky bodies on both ends: {', '.join(s.get('same_sky_both_ends', s.get('sky', []))) or 'none'}"
        if s['shape'] == 3: extra = f"; sky great circle {s['sky_gc']}"
        if s['shape'] == 8: extra = f"; {'number ' + s['number'] if 'number' in s else 'ratio ' + s.get('ratio', '')}"
        if s['shape'] == 7: extra = f"; sky {s['sky']}"
        L.append(f"- **{NAMES[s['shape']]}** ({lvl}{', hub' if s['hub'] else ''}){extra} — {stand}; rests on {s['roots_behind']} independent facts")
        for it in s['items'][:CAP_ITEMS + 1]: L.append(f"    - {D(it)}"); cited.append(it)
        shown += 1
    if not R['shapes']: L.append('- none')
    L.append('')
    # 4 arithmetic
    L.append('## 4. What is arithmetic (Layer 2)')
    seen, n4 = set(), 0
    fb = lambda x: x.replace('Rahu', 'Node').replace('Ketu', 'Node')
    hubset = {fb(h) for h in hubs[:CAP_HUBS]}
    for l in inv['links']:   # plus the other end of each close cross link on a hub
        if l['kind'] == 'cross' and l['close'] and (fb(l['a']) in hubset or fb(l['b']) in hubset): hubset |= {fb(l['a']), fb(l['b'])}
    def touches_hub(it):
        sec, i = it.split(':')[:2]
        if sec == 'strikes': return fb(inv['strikes'][int(i)]['target']) in hubset
        if sec == 'links': l = inv['links'][int(i)]; return fb(l['a']) in hubset or fb(l['b']) in hubset
        if sec == 'movement': m = inv['movement'][int(i)]; return fb(f"{m['chart']} {m['body']}") in hubset
        return False
    extra = [it for it, t in tags.items() if t.get('tag') == 'derived' and 'chain' in t and it.split(':')[0] in ('strikes', 'links', 'movement') and touches_hub(it)]
    for it in cited + extra:
        t = tags.get(it, {})
        if it in seen or 'chain' not in t or t.get('tag') not in ('derived', 'mirror'): continue
        seen.add(it); n4 += 1
        L.append(f"- {D(it)} = " + ' + '.join(W(describe(inv, sky, c['id'], R['desc'])) for c in t['chain']) + (' (node mirror)' if t['tag'] == 'mirror' else ''))
        if n4 >= 14: break
    if not n4: L.append('- none among the items above')
    L.append('')
    # 5 same pair elsewhere
    L.append('## 5. Same pair / body in other runners')
    n5 = 0
    for s in F['same_across_field']:
        if any(x['runner'] == P for x in s['runners']):
            mine5 = [x for x in s['runners'] if x['runner'] == P][0]
            others = [f"{x['runner']} ({x['tightness']})" for x in s['runners'] if x['runner'] != P]
            L.append(f"- {NAMES[s['shape']]}: {W(s['key'])} — this runner ({mine5['tightness']}); also {', '.join(others)}"); n5 += 1
    if not n5: L.append('- none')
    L.append('')
    # 6 recurring
    L.append('## 6. Recurring pairs from earlier winners (noted, not weighted)')
    def norm(n):
        m = re.match(r'recurring pair (\w+)–(\w+)$', n)
        return f"recurring pair {'–'.join(sorted(m.groups()))}" if m else n
    notes = sorted({norm(a['note']) for a in R['annotations']})
    L += [f"- {W(n)}" for n in notes] or ['- none']
    L.append('')
    # 7 near joined
    L.append('## 7. Near items that joined the web')
    n7 = 0
    for b, v in sorted(R['bodies'].items(), key=lambda x: -x[1]['tight_kinds']):
        for k in v['near_joined']:
            if n7 < 8: L.append(f"- {W(b)} {KINDS[k]}: " + '; '.join(D(i) for i in v['items'][k][:2]))
            n7 += 1
    if n7 > 8: L.append(f"- ... {n7 - 8} more in Layer 3")
    if not n7: L.append('- none')
    return '\n'.join(L), any1

def run(race):
    base = f'docs/classic/{race}'
    F = json.load(open(f'{base}/layer4/field.json')); sky = json.load(open(f'{base}/layer1/sky.json'))
    O = f'{base}/layer5'; os.makedirs(O, exist_ok=True)
    page = [f"# {race} — field reading (blind)  [{VERSION}]", '', '## What only each runner has (racecard order)']
    for r in F['runners']:
        P = r['P']
        inv = json.load(open(f'{base}/layer1/{P}.json')); T = json.load(open(f'{base}/layer2/{P}.json')); R = json.load(open(f'{base}/layer3/{P}.json'))
        txt, _ = read_runner(P, inv, T, R, F, sky, len(F['runners']))
        open(f'{O}/{P}.md', 'w').write(txt + '\n')
        sec1 = txt.split('## 1. What only this runner has')[1].split('## 2.')[0].strip()
        page.append(f"**{P} {r['name']}**\n{sec1}\n")
    page.append('## Tightest instance of each shape in the field')
    for k, v in F['tightest'].items():
        lvl, n = k.split(':'); page.append(f"- {NAMES[int(n)]} ({lvl}): {v['runner']} {v['name']} — {v['key']} ({v['tightness']})")
    open(f'{O}/race.md', 'w').write('\n'.join(page) + '\n')
    print(f'{race}: {len(F["runners"])} readings')

if __name__ == '__main__':
    run(sys.argv[1].rstrip('/').split('/')[-1])
