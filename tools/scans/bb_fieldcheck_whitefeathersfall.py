"""Field check (16 Nov 2026, Eddie: 'is there anything that would test as a new pattern'), from Whitefeathersfall (Carlisle 16:30
7 Jul 2022, won 10/1). Read-only; winners named below, no results file read. 12 result races.
 N1  one sky pair S A - S B (same plane, family, target; not the Moon) carries lines on two different natal bodies of the runner
     ('Sky lines on the same target' of both bodies), each carried line in a real family (conj / cp never)
 N1b N1 with one carried line a royal-star line (c R - c X) and the other a same-body line (S X -> c X)
 N1c N1b with a royal star as one end of the pair
 N2  BB29 held and its sky body Y conjunct (or contraparallel) natal X in that chart, score >= 90
 N3  holds at least 2 of the combos BB3 + BB63, BB3 + BB54, BB59
 N4  holds all 3"""
import sys, json
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
RACES = [('20210402_lingfield_aw_1435', 'Pholas'), ('20200608_haydock_1345', 'Ishvara'), ('20240608_beverley_1405', 'Perfect Part'),
         ('20240515_york_1545', 'Secret Satire'), ('20240515_york_1615', 'Diligent Resdev'), ('20220406_catterick_1440', 'Wotever Next'),
         ('20231006_fontwell_1530', 'Kilcummin'), ('20210802_newcastle_aw_1633', 'Athmad'), ('20220717_newton_abbot_1525', 'On Time'),
         ('20220716_doncaster_1845', 'Novakai'), ('20220712_bath_1530', 'Cafe Sydney'), ('20220707_carlisle_1630', 'Whitefeathersfall')]
CJ = ('conj', 'contraparallel'); ROY = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
ok = lambda r: r.get('fam') and r['fam'] not in CJ and r.get('sc') is not None


def carried(D):
    """(pair line, plane, fam, tgt) -> {(body, matched line text)}"""
    out = {}
    for X, d in D.items():
        lines = {f"{r['line']} {r['plane']}": r for r in d['L'] if ok(r)}
        for p in d['S']:
            if ' – ' not in p['line'] or 'Moon' in p['line'] or not p.get('fam') or p['fam'] in CJ:
                continue
            m = lines.get(p.get('match'))
            if not m:
                continue
            kind = 'same' if m['line'].startswith('S ') else ('royal' if any(f' {R} – ' in m['line'] for R in ROY) else 'other')
            out.setdefault((p['line'], p['plane'], p['fam'], p['tgt']), set()).add((X, kind, p['match']))
    return out


KEYS = ['N1', 'N1b', 'N1c', 'N2', 'N3', 'N4']
tot = {k: [0, 0, 0.0] for k in KEYS}
for r, win in RACES:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
    J = json.load(open(f'docs/eddie_read/bybody_rules/{r}_bbrules.json'))
    hold = {}
    for rid, cs in J['rules'].items():
        for c in cs:
            if not c['watch_only']: hold.setdefault(c['runner'], {}).setdefault(rid, []).append(c)
    held = {k: [] for k in KEYS}; ex = {}
    for run, D in data.items():
        tg = set()
        for key, xs in carried(D).items():
            bodies = {x[0] for x in xs}
            if len(bodies) < 2: continue
            tg.add('N1')
            kinds = {(x[0], x[1]) for x in xs}
            if any(k == 'royal' for _, k in kinds) and any(k == 'same' for _, k in kinds) and \
               any(b1 != b2 for b1, k1 in kinds for b2, k2 in kinds if k1 == 'royal' and k2 == 'same'):
                tg.add('N1b')
                if any(f'S {R}' in key[0] for R in ROY):
                    tg.add('N1c'); ex.setdefault(run, []).append(f"{key[0]} {key[1]} {key[3]} carries {sorted(xs)}")
        h = hold.get(run, {})
        for c in h.get('BB29', []):
            if any(('conj' in x or 'contraparallel' in x) and '→' in x and x.split(' → ')[1].split(' ')[1] == c['body']
                   and float(x.rsplit('(', 1)[1].rstrip(')')) >= 90 for x in c['cells']):
                tg.add('N2')
        n = sum(set(cb) <= set(h) for cb in (('BB3', 'BB63'), ('BB3', 'BB54'), ('BB59',)))
        if n >= 2: tg.add('N3')
        if n == 3: tg.add('N4')
        for k in tg: held[k].append(run)
    for k in KEYS:
        hh = held[k]; w = sum(win in x for x in hh)
        tot[k][0] += len(hh); tot[k][1] += w; tot[k][2] += len(hh) / N
    print(f"\n## {r} ({N} runners, winner {win})")
    for k in KEYS: print(f"  {k} {len(held[k])}: {', '.join(held[k])}")
    for run, e in ex.items():
        if win in run: print(f"  N1c winner: {e[0][:240]}")
print('\n## Totals over 12 result races (picks / won / by chance)')
for k, (p, w, c) in tot.items(): print(f'  {k}: {p} picks, {w} won, {c:.1f} by chance')
