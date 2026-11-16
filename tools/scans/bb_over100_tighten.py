"""Scan (16 Nov 2026, Eddie: 'it was the accuracy that I meant, not just values over 100 - tightening over 100 might be the idea').
Read-only; no rule or tool changed. The bybody families use percentage tolerances for ninths (0.2 %), φ powers, √2 and silver (0.15 %),
so above 100 the window widens (ninth 155.556 ±0.311, 141.4 ±0.212); whole (±0.02) and golden (±0.0324) stay absolute, opposition ±0.75.
For every row with a value > 100 the best family and the 'also' families are re-evaluated on a tighter tolerance (linear score
100 (tol − dev) / tol, as the bybody tool); the best surviving family is kept, otherwise the row has no family (an S / O row is dropped).
T1 percentage families fixed at their size at 100: ninth ±0.2, φ power / √2 / silver ±0.15 (whole, golden, opposition unchanged).
T2 ninth, φ power, √2, silver ±0.05; opposition ±0.25.
T3 every family at most ±0.0324 (golden's): ninth, φ power, √2, silver, opposition ±0.0324; whole ±0.02.
T4 ninth only ±0.05.
A 'Sky lines on the same target' row is dropped when its anchor line (> 100) no longer holds that family + target under the tighter tolerance (best or 'also'; checker, 16 Nov).
Ratios (same-body / crossed) are not changed. Then every BB rule re-run: picks / winners / chance over the 8 result races."""
import copy, re, sys
sys.path.insert(0, 'tools'); import eddie_bybody_rules as E; import eddie_bybody as BY
RACES = [('Lingfield', '20210402_lingfield_aw_1435', 'Pholas'), ('Haydock', '20200608_haydock_1345', 'Ishvara'),
         ('Beverley', '20240608_beverley_1405', 'Perfect Part'), ('York 15:45', '20240515_york_1545', 'Secret Satire'),
         ('York 16:15', '20240515_york_1615', 'Diligent Resdev'), ('Catterick', '20220406_catterick_1440', 'Wotever Next'),
         ('Fontwell', '20231006_fontwell_1530', 'Kilcummin'), ('Newcastle', '20210802_newcastle_aw_1633', 'Athmad')]


def origin(rid):
    k = int(rid[2:].rstrip('b'))
    for lim, i in ((17, 0), (31, 1), (40, 2), (50, 3), (56, 4), (60, 5), (62, 6), (64, 7)):
        if k <= lim:
            return i
    return 7


big = lambda x: E.num(x) and x > 100


def _strip(data, mode):
    d2 = copy.deepcopy(data)
    cut = (lambda r: big(r['v']) and r.get('fam') != 'opposition') if mode == 'C' else (lambda r: big(r['v']))
    for run, bodies in d2.items():
        for X, d in bodies.items():
            for r in d['L']:
                if cut(r):
                    r['fam'] = r['tgt'] = r['sc'] = None
                if mode == 'B':
                    if big(r['v']) or big(r['sbv']):
                        r['rt'] = r['rs'] = None
                    if big(r['v']) or big(r['xbv']):
                        r['xt'] = r['xs'] = None
            d['S'] = [r for r in d['S'] if not cut(r)]
            d['O'] = [r for r in d['O'] if not cut(r)]
    return d2


def holders(data):
    res = {rid: {} for rid, _, _ in E.RULES}
    for rid, fn, _ in E.RULES:
        if fn is None:  # BB67 is built from the other rules' holders (below)
            continue
        for run, D in data.items():
            for X, d in D.items():
                b = E.Body(X, d); b.all = D
                seen = set()
                for case in fn(b):
                    if case.get('watch_only') or case['key'] in seen:
                        continue
                    seen.add(case['key'])
                    cl = res[rid].setdefault(run, [])
                    for c in case['cells']:
                        if (c['line'], c['plane'], c['tgt']) not in {(x['line'], x['plane'], x['tgt']) for x in cl}:
                            cl.append(c)
    if 'BB67' in res:  # runner-level: at least 2 of BB3 + BB63, BB3 + BB54, BB59
        for run in data:
            h = {rid for rid, rr in res.items() if run in rr}
            if sum(set(cb) <= h for cb in E.BB67_COMBOS) >= 2:
                res['BB67'][run] = []
    return res



TV = {(f, lab): t for f, lab, t, _ in BY.TARGETS}
TV[('opposition', '180')] = 180.0
BASE = {'whole': lambda t: 0.02, 'golden': lambda t: 0.0324, 'phi power': lambda t: 0.0015 * t, 'ninth': lambda t: 0.002 * t,
        'sqrt2': lambda t: 0.0015 * t, 'silver': lambda t: 0.0015 * t, 'opposition': lambda t: 0.75}
V = {'T1': {'ninth': 0.2, 'phi power': 0.15, 'sqrt2': 0.15, 'silver': 0.15},
     'T2': {'ninth': 0.05, 'phi power': 0.05, 'sqrt2': 0.05, 'silver': 0.05, 'opposition': 0.25},
     'T3': {'ninth': 0.0324, 'phi power': 0.0324, 'sqrt2': 0.0324, 'silver': 0.0324, 'opposition': 0.0324},
     'T4': {'ninth': 0.05}}


def cands(r):
    out = [(r['fam'], str(r['tgt']))] if r['fam'] else []
    for part in str(r.get('also') or '').split(';'):
        m = re.match(r'\s*(\S+)\s*(.*?)\s*\(', part)
        if m:
            out.append((m.group(2).strip() or 'whole', m.group(1)))
    return out


def survivors(r, var):
    out = set()
    for fam, lab in cands(r):
        if fam in BASE and (fam, lab) in TV:
            t = TV[(fam, lab)]; tol = min(BASE[fam](t), var.get(fam, BASE[fam](t)))
            if abs(r['v'] - t) < tol:
                out.add((fam, lab))
    return out


def retune(r, var):
    best = None
    for fam, lab in cands(r):
        if fam not in BASE or (fam, lab) not in TV:
            continue
        t = TV[(fam, lab)]; tol = min(BASE[fam](t), var.get(fam, BASE[fam](t)))
        dev = abs(r['v'] - t)
        if dev < tol:
            sc = round(100 * (tol - dev) / tol, 2)
            if not best or sc > best[2]:
                best = (fam, lab, sc)
    return best


def tighten(data, var):
    d2 = copy.deepcopy(data)
    for run, bodies in d2.items():
        for X, d in bodies.items():
            anc = {}
            for sec in 'LSO':
                keep = []
                for r in d[sec]:
                    if sec == 'L' and E.num(r['v']) and r['v'] > 100 and r['fam'] in BASE:
                        anc[f"{r['line']} {r['plane']}"] = (r['v'], survivors(r, var))
                    if sec == 'S' and r.get('match') in anc and anc[r['match']][0] > 100 \
                       and r['fam'] in BASE and (r['fam'], str(r['tgt'])) not in anc[r['match']][1]:
                        continue
                    if E.num(r['v']) and r['v'] > 100 and r['fam'] in BASE:
                        b = retune(r, var)
                        if b:
                            r['fam'], r['tgt'], r['sc'] = b
                        elif sec == 'L':
                            r['fam'] = r['tgt'] = r['sc'] = None
                        else:
                            continue
                    keep.append(r)
                d[sec] = keep
    return d2


if __name__ == '__main__':
    modes = ['0'] + list(V)
    T = {m: {} for m in modes}; lost = {m: 0 for m in modes}
    for i, (n, r, w) in enumerate(RACES):
        data = E.load(f'docs/eddie_read/bybody/{r}/{r}_bybody.xlsx'); N = len(data)
        for m in modes:
            dd = data if m == '0' else tighten(data, V[m])
            for rid, hs in holders(dd).items():
                t = T[m].setdefault(rid, [0, 0, 0.0, 0, 0, 0.0]); won = any(w in x for x in hs)
                t[0] += len(hs); t[1] += won; t[2] += len(hs) / N
                if i > origin(rid):
                    t[3] += len(hs); t[4] += won; t[5] += len(hs) / N
    ids = [rid for rid, _, _ in E.RULES]
    f = lambda t: f"{t[0]} / {t[1]} ({t[2]:.1f})"
    rank = sorted(ids, key=lambda k: -(T['0'][k][1] - T['0'][k][2]))
    print('| Rule | as built | later races | ' + ' | '.join(V) + ' |'); print('|---' * (3 + len(V)) + '|')
    for k in rank:
        print(f"| {k} | {f(T['0'][k])} | {T['0'][k][3]} / {T['0'][k][4]} ({T['0'][k][5]:.1f}) | " + ' | '.join(f(T[m][k]) for m in V) + ' |')
    for m in modes:
        P = sum(T[m][k][0] for k in ids); W = sum(T[m][k][1] for k in ids); C = sum(T[m][k][2] for k in ids)
        Pl = sum(T[m][k][3] for k in ids); Wl = sum(T[m][k][4] for k in ids); Cl = sum(T[m][k][5] for k in ids)
        print(f"{m}: all 8 races {P} picks, {W} winners, {C:.1f} by chance ({W / C:.2f}x); later races {Pl} / {Wl} ({Cl:.1f}, {Wl / Cl:.2f}x)")
