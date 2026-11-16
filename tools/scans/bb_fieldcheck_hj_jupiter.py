"""Field check (16 Nov 2026, Eddie: 'definitely the Jupiter line ... Juno adds extra ... what are the rule options').
On Time (Newton Abbot 15:25 17 Jul 2022): H Jupiter – J Jupiter Dec 11.3265 7×φ (99.2); S Juno – S Jupiter Dec 0.0059 conj.
Read-only. Versions over the 9 result races (picks = runners holding it):
 A  H Jupiter – J Jupiter scores in a family (conj / contraparallel not counted), any plane
 B  A at score >= 90
 C  A in Dec
 D  A + a sky body (not Moon) conjunct sky Jupiter in the same plane
 E  A + S Jupiter -> H Jupiter and S Jupiter -> J Jupiter both scoring in that plane
 F  A + another sky line (S or O rows of Jupiter, not conj / cp) on the same family + target"""
import sys, re
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
sys.path.insert(0, 'tools/scans'); from bb_over100_tighten import RACES
RACES = RACES + [('Newton Abbot', '20220717_newton_abbot_1525', 'On Time')]
CJ = ('conj', 'contraparallel')
ok = lambda r: r.get('fam') and r['fam'] not in CJ and r.get('sc') is not None


def cases(d):
    L = d['L']
    out = {}
    for r in L:
        if r['line'] != 'H Jupiter – J Jupiter' or not ok(r):
            continue
        pl = r['plane']
        tags = {'A'}
        if r['sc'] >= 90: tags.add('B')
        if pl == 'Dec': tags.add('C')
        sky = [o for o in d['O'] if o['line'].startswith('S ') and '→' not in o['line'] and o['plane'] == pl
               and o.get('fam') == 'conj' and 'Moon' not in o['line']]
        if sky: tags.add('D')
        sh = [x for x in L if x['line'] == 'S Jupiter → H Jupiter' and x['plane'] == pl and ok(x)]
        sj = [x for x in L if x['line'] == 'S Jupiter → J Jupiter' and x['plane'] == pl and ok(x)]
        if sh and sj: tags.add('E')
        rep = [o for o in d['S'] + d['O'] if ok(o) and o['fam'] == r['fam'] and o['tgt'] == r['tgt']]
        if rep: tags.add('F')
        out[pl] = (r, tags, [o['line'] for o in sky], [f"{o['line']} {o['plane']} {o['v']:.4f} ({o['sc']})" for o in rep])
    return out


tot = {k: [0, 0, 0.0] for k in 'ABCDEF'}
for name, r, win in RACES:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
    print(f'\n## {name} ({N} runners, winner {win})')
    held = {k: [] for k in 'ABCDEF'}
    for run, D in data.items():
        if 'Jupiter' not in D: continue
        cs = cases(D['Jupiter'])
        tags = set().union(*[c[1] for c in cs.values()]) if cs else set()
        for k in tags: held[k].append(run)
        for pl, (row, t, sky, rep) in cs.items():
            print(f"  {run}: {pl} {row['v']:.4f} {row['tgt']} {row['fam']} ({row['sc']}) [{''.join(sorted(t))}]"
                  + (f" conj sky Jupiter: {', '.join(sky)}" if sky else '') + (f" repeat: {'; '.join(rep)}" if rep else ''))
    for k in 'ABCDEF':
        h = held[k]; w = sum(1 for x in h if win in x)
        tot[k][0] += len(h); tot[k][1] += w; tot[k][2] += len(h) / N
    print('  holders: ' + ', '.join(f"{k} {len(held[k])}" for k in 'ABCDEF'))
print('\n## Totals (picks / winners / by chance)')
for k, (p, w, c) in tot.items():
    print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')
