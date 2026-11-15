"""Field check (15 Nov 2026, from Fontwell 15:30 2023 Kilcummin's jockey David Noonan): many same-body lines S X → J X score:
Mars Dec 5×φ (95.7), Jupiter RA 152 (58.4), Saturn Dec ninth 6.66667 (30.6), Uranus RA ninth 111.111 (97.3), Neptune RA 100φ^-1 (96.4),
Pluto Dec 10×φ (78.5), Rahu / Ketu RA ninth 177.778 (3.4), Chiron RA 103×φ (98.7), Haumea Dec φ⁴ (61.9), Transpluto RA 9 (20.9);
carried: Mars by S Sedna – S Aldebaran, Saturn by S Haumea – S Makemake and S Jupiter – S Makemake, Rahu by S Eris → J Rahu,
S Saturn – S Transpluto, S Gonggong – S Orcus; lights: Sun on J Jupiter and J Uranus, Moon on J Uranus and J Chiron.
Per runner and chart (H, J): N1 bodies whose S X → c X scores (conj / cp not counted; Rahu and Ketu one body), N1s the same at score >= 50,
N2 of those with a Sun or Moon line on c X, N3 of those carried by a sky pair on its target (not naming X, no Moon). Field rank."""
import sys; sys.path.insert(0, 'tools'); import eddie_bybody_rules as E
races = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell 15:30', '20231006_fontwell_1530', 'Kilcummin'), ('Chelmsford', '20240118_chelmsford_aw_1320', None)]
CJ = ('conj', 'contraparallel'); fam = lambda x: x['fam'] and x['fam'] not in CJ
tops = {}
for n, r, w in races:
    data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); rows = []
    for runner, bodies in data.items():
        res = {}
        for c in 'HJ':
            n1 = set(); n1s = set(); n2 = set(); n3 = set()
            for X, d in bodies.items():
                b = E.Body(X, d); key = 'Nodes' if X in ('Rahu', 'Ketu') else X
                sb = [x for x in b.same_body(c) if fam(x)]
                if not sb: continue
                n1.add(key)
                if any(E.num(x['sc']) and x['sc'] >= 50 for x in sb): n1s.add(key)
                if [o for o in b.lights() if o['line'].endswith(f' → {c} {X}') and o['fam']]: n2.add(key)
                if any(X not in (A, B) and 'Moon' not in (A, B) for x in sb for s, A, B in b.pairs_on(x)): n3.add(key)
            res[c] = (len(n1), len(n1s), len(n2), len(n3))
        rows.append((runner, res))
    print(f'== {n}' + (f' (winner {w})' if w else ''))
    for runner, res in rows:
        print(f"  {runner:26s} H N1 {res['H'][0]:2d} N1s {res['H'][1]:2d} N2 {res['H'][2]:2d} N3 {res['H'][3]:2d} | J N1 {res['J'][0]:2d} N1s {res['J'][1]:2d} N2 {res['J'][2]:2d} N3 {res['J'][3]:2d}{'  W' if w and w in runner else ''}")
    for c in 'HJ':
        for i, nm in enumerate(('N1', 'N1s', 'N2', 'N3')):
            m = max(res[c][i] for _, res in rows); top = [ru for ru, res in rows if res[c][i] == m]
            k = (c, nm); p, wn, ch = tops.get(k, (0, 0, 0.0))
            if w: tops[k] = (p + len(top), wn + any(w in t for t in top), ch + len(top) / len(rows))
for (c, nm), (p, wn, ch) in tops.items(): print(f'top of field on {c} {nm}: {p} picks, {wn} won, {ch:.1f} by chance (7 result races)')

# P1 (15 Nov 2026): the runner's strongest chart, max over H and J of N1 (and of N1s), top of the field.
print('--- P1: max over H / J, top of the field')
for i, nm in ((0, 'N1'), (1, 'N1s')):
    p = wn = 0; ch = 0.0
    for n, r, w in races:
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); val = {}
        for runner, bodies in data.items():
            best = 0
            for c in 'HJ':
                s1, s2 = set(), set()
                for X, d in bodies.items():
                    sb = [x for x in E.Body(X, d).same_body(c) if fam(x)]
                    if sb:
                        k = 'Nodes' if X in ('Rahu', 'Ketu') else X; s1.add(k)
                        if any(E.num(x['sc']) and x['sc'] >= 50 for x in sb): s2.add(k)
                best = max(best, len(s1) if i == 0 else len(s2))
            val[runner] = best
        m = max(val.values()); top = sorted(ru for ru, v in val.items() if v == m)
        print(f'  {n}: top {m} {top}' + (' W' if w and any(w in t for t in top) else ''))
        if w: p += len(top); wn += any(w in t for t in top); ch += len(top) / len(val)
    print(f'P1 {nm}: {p} picks, {wn} won, {ch:.1f} by chance (7 result races)')
