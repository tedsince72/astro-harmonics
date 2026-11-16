"""Field check (16 Nov 2026, Eddie: 'that venus is definitely the one to focus on - does it create a rule - similar to dettori day'),
from Society Red (Ripon 15:25 16 Jun 2022, won 16/1). Read-only; winners named below, no results file read. 13 result races.

Society Red Venus Dec: S Venus -> H Venus 33.095682 (no family) is split by sky Sedna between them:
  S Sedna - S Venus 8.090457 (5xphi, 99.11) + S Sedna -> H Venus 25.005224 (25, 73.88) = 33.095681.
Dettori's day (Ascot 14:35 1996): J Sun - J Chiron Dec 28 split by the sky Sun into 21 (S Sun -> J Sun, 99.34) + 7.

SPLIT = for body X and chart c, a sky body Y (not X, not the Moon) between S X and c X in one plane, so that
d(S Y, S X) + d(S Y, c X) = d(S X, c X) (within 0.0005), both pieces scoring in a family (conj / cp never).
 V1   any plane, any scores
 V1d  Dec only
 V2   both pieces >= 50
 V3   one piece >= 90, the other >= 50
 V3d  V3 in Dec
 V4   V3 and the same-body line itself conj / contraparallel >= 80 in that plane, or the whole line in a family (the mirror)
 V5   V3 and the same-body line conj / contraparallel >= 80 in that plane (Society Red: S Venus cp H Venus 95.31)
 VS   V1 with Y a royal star (V1-V4 take sky bodies only)"""
import sys, json
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
RACES = [('20210402_lingfield_aw_1435', 'Pholas'), ('20200608_haydock_1345', 'Ishvara'), ('20240608_beverley_1405', 'Perfect Part'),
         ('20240515_york_1545', 'Secret Satire'), ('20240515_york_1615', 'Diligent Resdev'), ('20220406_catterick_1440', 'Wotever Next'),
         ('20231006_fontwell_1530', 'Kilcummin'), ('20210802_newcastle_aw_1633', 'Athmad'), ('20220717_newton_abbot_1525', 'On Time'),
         ('20220716_doncaster_1845', 'Novakai'), ('20220712_bath_1530', 'Cafe Sydney'), ('20220707_carlisle_1630', 'Whitefeathersfall'),
         ('20220616_ripon_1525', 'Society Red')]
CJ = ('conj', 'contraparallel')
STARS = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
fam = lambda r: r.get('fam') and r['fam'] not in CJ and r.get('sc') is not None
KEYS = ['V1', 'V1d', 'V2', 'V3', 'V3d', 'V4', 'V5', 'VS']


def splits(X, d):
    out = []
    same = {}
    for r in d['L']:
        if r['line'] in (f'S {X} → H {X}', f'S {X} → J {X}') and r['plane'] in ('RA', 'Dec'):
            same[(r['line'][-len(X) - 2], r['plane'])] = r
    mirror = {}; cpm = {}
    for r in d['L']:
        if r['line'] in (f'S {X} → H {X}', f'S {X} → J {X}') and r.get('fam') and r.get('sc') is not None:
            c = r['line'][-len(X) - 2]; p = r['plane'].split()[0]
            if r['fam'] in CJ and r['sc'] >= 80: cpm[(c, p)] = max(cpm.get((c, p), 0), r['sc'])
            mirror[(c, p)] = max(mirror.get((c, p), 0), r['sc'] if (r['fam'] in CJ and r['sc'] >= 80) or r['fam'] not in CJ else 0)
    ss = {}
    sc = {}
    for r in d['O']:
        if not fam(r): continue
        ln = r['line']
        if ln.endswith(f'– S {X}') and ' – ' in ln:
            Y = ln.split(' – ')[0][2:]; ss.setdefault((Y, r['plane']), []).append(r)
        for c in 'HJ':
            if ln.endswith(f'→ {c} {X}'):
                Y = ln.split(' → ')[0][2:]; sc.setdefault((Y, c, r['plane']), []).append(r)
    for (c, p), base in same.items():
        V = base['v']
        for (Y, c2, p2), bs in sc.items():
            if c2 != c or p2 != p or Y in ('Moon', X): continue
            for a in ss.get((Y, p), []):
                for b in bs:
                    if abs(a['v'] + b['v'] - V) < 5e-4:
                        out.append(dict(X=X, c=c, p=p, Y=Y, V=V, a=a, b=b, base=base, mirror=mirror.get((c, p), 0), cp=cpm.get((c, p), 0)))
    return out


def tags(s, bodies):
    t = set(); lo, hi = sorted((s['a']['sc'], s['b']['sc']))
    if s['Y'] not in bodies:
        return {'VS'}
    t.add('V1')
    if s['p'] == 'Dec': t.add('V1d')
    if lo >= 50: t.add('V2')
    if hi >= 90 and lo >= 50:
        t.add('V3')
        if s['p'] == 'Dec': t.add('V3d')
        if s['mirror'] > 0: t.add('V4')
        if s['cp'] > 0: t.add('V5')
    return t


def txt(s):
    return (f"{s['c']} {s['X']} {s['p']}: S {s['X']} → {s['c']} {s['X']} {s['V']:.4f} = {s['a']['line']} {s['a']['v']:.4f} {s['a']['tgt']} "
            f"({s['a']['sc']}) + {s['b']['line']} {s['b']['v']:.4f} {s['b']['tgt']} ({s['b']['sc']})"
            + (f"; same-body line {s['base']['tgt']} ({s['base']['sc']})" if s['base'].get('fam') else '')
            + (f"; mirror {s['mirror']}" if s['mirror'] else ''))


def main():
    tot = {k: [0, 0, 0.0] for k in KEYS}
    for r, win in RACES:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        held = {k: [] for k in KEYS}; ex = {}
        for run, D in data.items():
            tg = set()
            for X, d in D.items():
                for s in splits(X, d):
                    t = tags(s, set(D) | {'Rahu', 'Ketu'}); tg |= t
                    if 'V3' in t: ex.setdefault(run, []).append(txt(s))
            for k in tg: held[k].append(run)
        for k in KEYS:
            hh = held[k]; w = sum(win in x for x in hh)
            tot[k][0] += len(hh); tot[k][1] += w; tot[k][2] += len(hh) / N
        print(f"\n## {r} ({N} runners, winner {win})")
        for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
        for run, e in ex.items():
            for x in e: print(f"    V3 {run}: {x}")
    print(f'\n## Totals over {len(RACES)} result races (picks / won / by chance)')
    for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')


if __name__ == '__main__':
    main()
