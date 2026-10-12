#!/usr/bin/env python3
"""layer4_field.py RACE [--results]   — Layer 4 of the layered reader (design: docs/classic/layer4_design.md, approved by Eddie 12 Oct 2026).

Reads docs/classic/<RACE>/layer3/P*.json (+ layer1 for detail) for every runner and reports where each runner stands against the field.
No control, no score, no combined ranking; runners in racecard order. Blind by default: finishing positions only with --results,
written to a separate file.
  1 shape table at two levels: STRICT (Layer 3 'strict' — all items tight) and BROAD (everything): runners with it, counts, field count
  2 detail per instance: tightness, sky bodies (shapes 1, 12), roots_behind, hub / strong hub, strict; tightest instance in the field
  3 field-only findings per runner (only runner; shared with one other)
  4 strong hubs across the field (same body as strong hub in other runners)
  5 same pair / same body across the field
  6 recurring annotations by runner
Output: docs/classic/<RACE>/layer4/field.json, field.txt (blind); field_results.txt with --results."""
import sys, os, glob, json, csv, re
VERSION = 'L4 v1.1 (12 Oct 2026)'
NAMES = {1: 'cross link struck on both ends', 2: 'partner strike', 3: 'pair together in the sky', 4: 'both ends moved',
         5: 'movement onto a cross link', 6: 'swap', 7: 'triangle struck at every corner', 8: 'same number / ratio in both charts',
         9: 'shared node', 10: 'sky body divides a natal pair', 11: 'joined same-body set', 12: 'pair in one chart struck on both ends by 2+'}
def fold(b): return 'Node' if b in ('Rahu', 'Ketu') else b

def tightness(s, I):
    """smaller = tighter; and a short text"""
    n = s['shape']; it = s['items']
    if n in (1, 2, 3, 4, 5, 6, 12):
        l = I['links'][int(it[0].split(':')[1])]
        if l['kind'] == 'cross' or len(it[0].split(':')) == 2:
            v = min(l['RA'] / 1.5, l['Dec'] / 0.3); return v, f"RA {l['RA']:.4f} Dec {l['Dec']:.4f}"
        pl = it[0].split(':')[2]; off = abs(l['nums'][pl]['off']); return off / 0.005, f"{pl} {l[pl]:.5f} = {l['nums'][pl]['num']}"
    if n == 9: v = min(s['rahu_rahu_ra'], s['rahu_ketu_ra']); return v / 3, f"node RA {v:.4f}"
    if n == 10:
        sp = I['splits'][int(it[0].split(':')[1])]
        e = min(r[1] for r in (sp['parts_ratio'], sp['span_ratio']) if r and r[0] != '1'); return e / 0.25, f"split error {e:.4f}%"
    if n == 11:
        sb = I['same_body'][int(it[0].split(':')[1])]; return sb['worst_pct'] / 0.15, f"worst {sb['worst_pct']:.4f}%"
    return 1.0, ''

def key(s):
    """same pair / same body key across runners"""
    n = s['shape']; b = s.get('bodies', [])
    if n == 5 and b: return f"moved {b[0].split(' ',1)[0]} {fold(b[0].split(' ',1)[1])}"
    if n in (1, 2, 3, 4) and len(b) >= 2: return f"horse {fold(b[0].split(' ',1)[1])} – jockey {fold(b[1].split(' ',1)[1])}"
    if n == 6: return f"swap {s['pair']}"
    if n == 8: return f"number {s.get('number')}" if 'number' in s else f"ratio {s.get('ratio')}"
    if n == 11: return f"same body {fold(b[0].split(' ',1)[1])}" if b else ''
    if n == 12 and len(b) >= 2: return f"{b[0].split(' ',1)[0]} {fold(b[0].split(' ',1)[1])}–{fold(b[1].split(' ',1)[1])}"
    if n == 7: return 'triangle ' + '/'.join(sorted(fold(x.split(' ',1)[1]) for x in b))
    if n == 10 and len(b) >= 2: return f"{b[0]} -> {b[1]}"
    return NAMES[n]

def run(race):
    D3 = f'docs/classic/{race}/layer3'; D1 = f'docs/classic/{race}/layer1'
    runners = []
    for f in sorted(glob.glob(f'{D3}/P*.json'), key=lambda x: int(re.search(r'P(\d+)', x).group(1))):
        t = os.path.basename(f)[:-5]; R = json.load(open(f)); I = json.load(open(f'{D1}/{t}.json'))
        runners.append((t, R, I))
    n = len(runners)
    table = {lvl: {k: {} for k in NAMES} for lvl in ('strict', 'broad')}
    inst = []
    for t, R, I in runners:
        for s in R['shapes']:
            tv, tt = tightness(s, I)
            rec = {'runner': t, 'name': R['runner'], 'shape': s['shape'], 'strict': s['strict'], 'tight_value': round(tv, 4), 'tightness': tt,
                   'roots_behind': s['roots_behind'], 'hub': s['hub'], 'strong_hub': s['strong_hub'], 'key': key(s),
                   'sky_bodies': s.get('same_sky_both_ends', s.get('sky')) if s['shape'] in (1, 12) else None,
                   'n_sky_bodies': len({fold(x) for x in (s.get('same_sky_both_ends') or s.get('sky') or [])}) if s['shape'] in (1, 12) else None,
                   'rests_on_near_or_broad': not s['strict'],
                   'strict_multi': s.get('strict_multi'), 'multi': s.get('multi'), 'bodies': s.get('bodies', [])}
            inst.append(rec)
            for lvl in ('strict', 'broad'):
                if lvl == 'broad' or s['strict']:
                    table[lvl][s['shape']].setdefault(t, 0); table[lvl][s['shape']][t] += 1
    # extra sub-shapes that matter in reads: 2+ sky bodies on both ends
    for lvl, fld in (('strict', 'strict_multi'), ('broad', 'multi')):
        for k in ('1m', '12m'):
            table[lvl][k] = {}
        for r in inst:
            if r['shape'] in (1, 12) and (r[fld] or (r['shape'] == 12 and lvl == 'broad')):   # shape 12 is 2+ bodies by definition (broad)
                k = '1m' if r['shape'] == 1 else '12m'; table[lvl][k][r['runner']] = table[lvl][k].get(r['runner'], 0) + 1
    tightest = {}   # per level; shapes 7, 8, 12 have no single tightness measure (checker) and are left out
    for lvl in ('strict', 'broad'):
        for k in NAMES:
            if k in (7, 8, 12): continue
            c = [r for r in inst if r['shape'] == k and (lvl == 'broad' or r['strict'])]
            if c:
                b = min(c, key=lambda r: r['tight_value'])
                tightest[f'{lvl}:{k}'] = {'runner': b['runner'], 'name': b['name'], 'tightness': b['tightness'], 'key': b['key'], 'strict': b['strict']}
    only = {t: {'strict': [], 'broad': [], 'with_one_other_strict': []} for t, _, _ in runners}
    for lvl in ('strict', 'broad'):
        for k, who in table[lvl].items():
            if len(who) == 1: only[next(iter(who))][lvl].append(str(k))
            if lvl == 'strict' and len(who) == 2:
                for w in who: only[w]['with_one_other_strict'].append(str(k))
    hubs = {}
    for t, R, I in runners:
        for h in R['strong_hubs']: hubs.setdefault(h, []).append(t)
    same = {}
    for r in inst:
        if r['shape'] in (1, 3, 4, 6, 11, 12, 7):
            same.setdefault((r['shape'], r['key']), {}).setdefault(r['runner'], r)
    same_out = [{'shape': k[0], 'key': k[1], 'runners': [{'runner': w, 'tightness': v['tightness'], 'strict': v['strict']} for w, v in sorted(rs.items())]}
                for k, rs in same.items() if len(rs) >= 2]
    ann = {}
    for t, R, I in runners:
        for a in R['annotations']: ann.setdefault(a['note'], set()).add(t)
    return {'version': VERSION, 'race': race, 'runners': [{'P': t, 'name': R['runner']} for t, R, I in runners],
            'table': {lvl: {str(k): v for k, v in d.items()} for lvl, d in table.items()}, 'tightest': {str(k): v for k, v in tightest.items()},
            'only': only, 'strong_hubs': hubs, 'same_across_field': same_out, 'annotations': {k: sorted(v) for k, v in ann.items()},
            'instances': inst}

def text(F):
    L = [f"== {F['race']}  field of {len(F['runners'])}   [{F['version']}]  (blind: no finishing positions)"]
    L.append('-- runners: ' + '; '.join(f"{r['P']} {r['name']}" for r in F['runners']))
    L.append('-- shape table (runner: count)          STRICT | BROAD')
    for k in list(map(str, NAMES)) + ['1m', '12m']:
        nm = NAMES.get(int(k), '') if k.isdigit() else ('cross link, 2+ sky bodies on both ends' if k == '1m' else 'pair in one chart, 2+ sky bodies on both ends')
        S, B = F['table']['strict'].get(k, {}), F['table']['broad'].get(k, {})
        L.append(f"   [{k:>3s}] {nm:42s} {len(S):2d}/{len(F['runners'])}: {' '.join(f'{p}:{c}' for p, c in S.items()) or '-'}  |  {len(B):2d}: {' '.join(f'{p}:{c}' for p, c in B.items()) or '-'}")
    L.append('-- tightest instance of each shape')
    for k, v in F['tightest'].items(): L.append(f"   [{k:>9s}] {v['runner']} {v['name']}: {v['key']} ({v['tightness']}){'' if v['strict'] else ' broad/near'}")
    L.append('-- field-only findings (shape numbers)')
    for r in F['runners']:
        o = F['only'][r['P']]
        if o['strict'] or o['broad'] or o['with_one_other_strict']:
            L.append(f"   {r['P']} {r['name']}: only (strict) {','.join(o['strict']) or '-'}; only (broad) {','.join(o['broad']) or '-'}; strict, shared with one other {','.join(o['with_one_other_strict']) or '-'}")
    L.append('-- strong hubs across the field')
    for h, ws in sorted(F['strong_hubs'].items(), key=lambda x: -len(x[1])): L.append(f"   {h:14s} {len(ws)}: {' '.join(ws)}")
    L.append('-- same pair / body across the field (2+ runners)')
    for s in sorted(F['same_across_field'], key=lambda s: (s['shape'], -len(s['runners']))):
        L.append(f"   [{s['shape']:2d}] {s['key']}: " + '; '.join(f"{x['runner']} ({x['tightness']}{'' if x['strict'] else ', broad'})" for x in s['runners']))
    L.append('-- recurring pairs (annotations)')
    for a, ws in sorted(F['annotations'].items()): L.append(f"   {a}: {' '.join(ws)}")
    return '\n'.join(L)

def results(race, F):
    m = re.match(r'(.+)_(\d{4})_(\d{8})$', race)
    cands = glob.glob(f'reference/classic/race_batch_{m.group(3)}_{m.group(1)}_{m.group(2)}.csv') if m else []
    if not cands: return None
    rows = list(csv.DictReader(open(cands[0])))
    pos = {r['name']: (r['finish_pos'], r['sp']) for r in rows if r['subject_type'] == 'horse'}
    L = [f"== {race} results (not used by any layer)"]
    for r in F['runners']:
        h = r['name'].split(' / ')[0]; p = pos.get(h, ('?', '?'))
        o = F['only'][r['P']]
        L.append(f"   {r['P']} {r['name']:44s} finish {p[0]:>3s}  SP {p[1]:6s}  only strict {','.join(o['strict']) or '-'}  only broad {','.join(o['broad']) or '-'}")
    return '\n'.join(L)

if __name__ == '__main__':
    race = sys.argv[1].rstrip('/').split('/')[-1]
    F = run(race); O = f'docs/classic/{race}/layer4'; os.makedirs(O, exist_ok=True)
    json.dump(F, open(f'{O}/field.json', 'w'), indent=1); open(f'{O}/field.txt', 'w').write(text(F) + '\n')
    if '--results' in sys.argv:
        r = results(race, F)
        if r: open(f'{O}/field_results.txt', 'w').write(r + '\n')
    print(f"{race}: {len(F['runners'])} runners, {len(F['instances'])} shape instances")
