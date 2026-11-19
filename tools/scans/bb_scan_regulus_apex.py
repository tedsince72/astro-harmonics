"""Regulus as apex (19 Nov 2026, Eddie: 'what was the old favourite theory that we had that involved regulus?' -> 'yes, run it';
read-only). From the March 2026 chat: races at short odds where the favourite lost ('unexpected') carried more Regulus-as-apex
triplets than races the favourite won. Here, on every result race with an _active.xlsx:
  SKY: an apex = two sky bodies A, B (bodies only, not Regulus, not the Rahu - Ketu pair, Moon allowed) with S A - S Regulus and
       S B - S Regulus both in a number family (no conj / cp / opposition) scoring >= cut, same plane (RA or Dec).
       T0 = that; T1 = T0 and S A - S B also in a number family >= cut (same plane).
  NATAL: the same in each runner's horse and jockey chart (N kind: natal body - natal Regulus), counts H + J.
Groups: favourite won / lost (favourite from bb_favs_outer_uranus.FAV), cover hit / miss (cover of eight picks from the rule files);
natal: winner's rank in its field, favourite's rank. Chosen after the results (the theory is old, the cut and versions are mine).
Usage: python3 tools/scans/bb_scan_regulus_apex.py [cut]"""
import sys, os, json, itertools, statistics as st
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 80
sys.argv = sys.argv[:1]
sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
C8 = [('BB32',), ('BB3', 'BB12', 'BB53'), ('BB79',), ('BB77c',), ('BB54', 'BB82'), ('BB1b',), ('BB69',), ('BB13', 'BB80')]
NUM = lambda h: [x for x in h if x[0] not in ('conj', 'opposition', 'contraparallel')]


def best(v, pl):
    h = NUM(EB.hits(v, pl)) if v is not None else []
    return h[0] if h else None


def apex(d, kind, pts):
    t0 = t1 = 0
    for pl in ('RA', 'Dec'):
        on = [a for a in pts if a != 'Regulus' and (h := best(EB.pair(d, kind, pl, a, 'Regulus'), pl)) and h[2] >= CUT]
        for a, b in itertools.combinations(on, 2):
            if {a, b} == {'Rahu', 'Ketu'}:
                continue
            t0 += 1
            h = best(EB.pair(d, kind, pl, a, b), pl)
            if h and h[2] >= CUT:
                t1 += 1
    return t0, t1


def key(n):
    return n.split(' ', 1)[1].lower() if n[:1].isdigit() else n.lower()


def main():
    rows = []
    for race, win in NG.RACES:
        p = f'reference/classic/race_batch_{race}_active.xlsx'
        rf = f'docs/eddie_read/bybody_rules/{race}_bbrules.json'
        if not os.path.exists(p):
            continue
        runners, tt, tp = EB.load(p)
        s0, s1 = apex(tt, 'S', EB.BODIES)
        nat = {}
        for cloth, r in runners.items():
            n = r['name'].get('H') or ''
            a = [apex(r['dist'][ch], 'N', EB.NATAL_BODIES) for ch in ('H', 'J') if r['dist'].get(ch)]
            nat[n] = (sum(x[0] for x in a), sum(x[1] for x in a))
        cover = None
        if os.path.exists(rf):
            J = json.load(open(rf))
            held = {r: set() for r in J['runners']}
            for rid, cs in J['rules'].items():
                for c in cs:
                    if not c.get('watch_only'):
                        held.setdefault(c['runner'], set()).add(rid)
            picks = {key(r) for r in J['runners'] if any(set(c) <= held[r] for c in C8)}
            cover = key(win) in picks if picks else None
        fav = F.FAV.get(race)
        rows.append(dict(race=race, win=win, fav=fav, favwon=(fav == win) if fav else None, cover=cover, s0=s0, s1=s1, nat=nat))
    print(f'# Regulus as apex, cut {CUT:g} ({len(rows)} result races with an _active.xlsx; chosen after the results)\n')
    print('| race | winner | favourite | fav won | cover | sky T0 | sky T1 |\n|---|---|---|---|---|---|---|')
    for r in rows:
        print(f"| {r['race']} | {r['win']} | {r['fav'] or '-'} | {'-' if r['favwon'] is None else 'yes' if r['favwon'] else 'no'} | "
              f"{'-' if r['cover'] is None else 'hit' if r['cover'] else 'miss'} | {r['s0']} | {r['s1']} |")

    def grp(name, sel):
        print(f'\n## Sky, {name}')
        for lab, f in sel:
            g = [r for r in rows if f(r)]
            if not g:
                continue
            for t in ('s0', 's1'):
                v = [r[t] for r in g]
                print(f'- {lab} ({len(g)} races) {t.upper()}: mean {st.mean(v):.2f}, median {st.median(v)}, races with >= 1: {sum(x > 0 for x in v)}')
    grp('favourite won / lost', [('favourite won', lambda r: r['favwon'] is True), ('favourite lost', lambda r: r['favwon'] is False)])
    grp('cover hit / miss', [('cover hit', lambda r: r['cover'] is True), ('cover miss', lambda r: r['cover'] is False),
                              ('no cover pick', lambda r: r['cover'] is None)])

    print('\n## Natal (H + J), rank in the field (1 = most apexes; ties share the best rank)')
    for t, i in (('T0', 0), ('T1', 1)):
        for who in ('winner', 'favourite'):
            top = bot = n = 0; exp_top = exp_bot = 0.0
            for r in rows:
                name = r['win'] if who == 'winner' else r['fav']
                if not name:
                    continue
                vals = {key(k): v[i] for k, v in r['nat'].items() if k}
                if key(name) not in vals:
                    continue
                n += 1; v = vals[key(name)]; allv = list(vals.values())
                top += v == max(allv); bot += v == min(allv)
                exp_top += sum(x == max(allv) for x in allv) / len(allv); exp_bot += sum(x == min(allv) for x in allv) / len(allv)
            print(f'- {t} {who}: {n} races, top of the field {top} ({exp_top:.1f} by chance), bottom {bot} ({exp_bot:.1f} by chance)')


if __name__ == '__main__':
    main()
