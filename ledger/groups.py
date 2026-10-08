#!/usr/bin/env python3
"""groups.py v1.1 - GROUPS of relationships (Eddie, 3 Oct 08:41-08:42: "where we have multiple relationships there
can be other supporting relationships that are a lower score that may be missed but still contribute as they are
part of a larger group ... try 30 ... any mix but show a shared family").
For each chart a web: every natal-natal relationship scoring >= 30 (any family, RA or Dec, best kept) is a link.
A GROUP = a set of bodies ALL linked to each other (a clique; maximal cliques found with networkx). Shown per group:
members, size, every link with raw value / family / score (weak 30-69 links included), the shared family (the
family most links are in, with its share), total and mean strength; and what the moment does to it: members hit
by the sky at >= 80 from a top-12 sky body, landings of top-12 pairs on members, and links inside the group that
repeat a top-12 sky number (same coordinate, within 0.005). Three webs per partnership: horse natal, jockey natal,
and the partnership (horse + jockey bodies, with horse x jockey links). Natal Moon left out; no star-star links;
fast natal bodies marked *.
v1.1: adds the MOST LIT group per web (most members reached by the moment).
Usage: python3 groups.py --race RACE [--top N]"""
import argparse, collections, itertools, sys
import networkx as nx
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, NODES, FAST, FASTNATAL, results
FLOOR = 30.0

def link(p, q, x, y):
    best = None
    for m in ('RA', 'Dec'):
        if m == 'RA' and {x, y} == NODES:
            continue
        v = sep(p, q, m)
        for f in FAMS:
            s = FN[f](v, m)
            if s >= FLOOR and (best is None or s > best[2]):
                best = (m, f, s, v)
    return best

ap = argparse.ArgumentParser(); ap.add_argument('--race', required=True); ap.add_argument('--top', type=int, default=3)
a = ap.parse_args()
rc = Race(a.race); rc.build(); res = results(a.race)
order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
top12 = rc.byrank[:12]; topb = {b for k in top12 for b in k} - STARS
skyv = []
for k in top12:
    for m in ('RA', 'Dec'):
        v = sep(rc.sky[k[0]], rc.sky[k[1]], m)
        if max(FN[f](v, m) for f in FAMS) >= 80:
            skyv.append((rc.pairs[k]['rank'], m, v))

def sky_hits(tab, b):
    P = rc.natal[tab]; out = []
    for s in topb:
        if s == b or s in FAST:
            continue
        for m in ('RA', 'Dec'):
            v = sep(rc.sky[s], P[b], m)
            f = max(FAMS, key=lambda k: FN[k](v, m))
            if FN[f](v, m) >= 80:
                out.append(f"{s}→{FN[f](v, m):.0f}")
    return out

def lands_on(c, sd, b):
    return [f"#{rc.pairs[k]['rank']}" for k, sides in rc.land[c].items() for ld in sides.get(sd, []) if ld['C'] == b and rc.pairs[k]['rank'] <= 12]

def web(nodes):
    G = nx.Graph()
    for (na, pa), (nb, pb) in itertools.combinations(nodes, 2):
        x, y = na.split(':')[1], nb.split(':')[1]
        if x in STARS and y in STARS:
            continue
        if na.split(':')[0] == nb.split(':')[0] == 'X':
            continue
        L = link(pa, pb, x, y)
        if L:
            G.add_edge(na, nb, m=L[0], f=L[1], s=L[2], v=L[3])
    return G

def describe(G, cl, c):
    E = [(u, v, G[u][v]) for u, v in itertools.combinations(cl, 2)]
    fam = collections.Counter(e['f'] for _, _, e in E)
    f0, n0 = fam.most_common(1)[0]
    tot = sum(e['s'] for _, _, e in E)
    weak = sum(1 for _, _, e in E if e['s'] < 70)
    reps = []
    for u, v, e in E:
        for rk, m, sv in skyv:
            if e['m'] == m and abs(e['v'] - sv) <= 0.005:
                reps.append(f"#{rk} {u.split(':')[1]}–{v.split(':')[1]} {e['v']:.4f}")
    moment = []
    for n in cl:
        sd, b = n.split(':')
        if b in STARS:
            continue
        tab = rc.charts[c][sd]
        h = sky_hits(tab, b); l = lands_on(c, sd, b)
        if h or l:
            moment.append(f"{n}{'*' if b in FASTNATAL else ''}: " + ' '.join(l + h))
    hit90 = 0
    for n in cl:
        sd, b = n.split(':')
        if b in STARS:
            continue
        tab = rc.charts[c][sd]
        if lands_on(c, sd, b) or any(int(h.split('→')[1]) >= 90 for h in sky_hits(tab, b)):
            hit90 += 1
    return dict(size=len(cl), tot=tot, mean=tot / len(E), fam=f"{f0} {n0}/{len(E)}", weak=weak, E=E, reps=reps, moment=moment, hit90=hit90)

print(f"GROUPS (all-linked sets, links >= {FLOOR:.0f}, any family) – {a.race}")
summary = []
for c in order:
    H = {b: v for b, v in rc.natal[rc.charts[c]['H']].items() if b != 'Moon'}
    J = {b: v for b, v in rc.natal[rc.charts[c]['J']].items() if b != 'Moon'}
    print(f"\n=== {res[c]['finish']} {c} {' / '.join(rc.names[c])} {res[c]['sp']}")
    for lab, nodes in (('HORSE', [(f'H:{b}', p) for b, p in H.items()]),
                       ('JOCKEY', [(f'J:{b}', p) for b, p in J.items()]),
                       ('PARTNERSHIP', [(f'H:{b}', p) for b, p in H.items()] + [(f'J:{b}', p) for b, p in J.items()])):
        G = web(nodes)
        if lab == 'PARTNERSHIP':
            # keep only groups that mix horse and jockey bodies
            cls = [cl for cl in nx.find_cliques(G) if len(cl) >= 3 and {n[0] for n in cl} == {'H', 'J'}]
        else:
            cls = [cl for cl in nx.find_cliques(G) if len(cl) >= 3]
        ds = sorted((describe(G, cl, c) | {'cl': sorted(cl)} for cl in cls), key=lambda d: (-d['size'], -d['mean']))
        big = ds[0]['size'] if ds else 0
        nbig = sum(1 for d in ds if d['size'] == big)
        lit = max(ds, key=lambda d: (d['hit90'], d['size'], d['mean'])) if ds else None
        summary.append((c, lab, big, nbig, len(ds), ds[0]['mean'] if ds else 0, lit))
        print(f"  {lab}: {len(ds)} groups; largest size {big} (×{nbig})")
        for d in ds[:a.top]:
            print(f"    size {d['size']} mean {d['mean']:.0f} total {d['tot']:.0f} | shared family {d['fam']} | weak (30-69) links {d['weak']}: {', '.join(n if lab == 'PARTNERSHIP' else n.split(':')[1] for n in d['cl'])}")
            print("        " + '; '.join(f"{u.split(':')[1] if lab != 'PARTNERSHIP' else u}–{v.split(':')[1] if lab != 'PARTNERSHIP' else v} {e['m']} {e['v']:.3f} {e['f'][:6]} {e['s']:.0f}" for u, v, e in d['E']))
            if d['reps']: print("        race numbers inside: " + '; '.join(d['reps']))
            if d['moment']: print("        the moment on it: " + ' | '.join(d['moment']))
print('\nSUMMARY – largest group size (how many of that size), number of groups, mean link score of the best')
for lab in ('HORSE', 'JOCKEY', 'PARTNERSHIP'):
    print(f"  {lab:11} " + ' | '.join(f"{res[c]['finish']} {rc.names[c][0][:14]}: {big} (×{nb}), {n} grp, {mn:.0f}" for c, l, big, nb, n, mn, lit in summary if l == lab))
print('\nMOST LIT GROUP – the group with the most members the moment reaches (a top-12 landing or a top-12 sky body at >= 90)')
for lab in ('HORSE', 'JOCKEY', 'PARTNERSHIP'):
    for c, l, big, nb, n, mn, lit in summary:
        if l == lab and lit:
            print(f"  {lab:11} {res[c]['finish']} {rc.names[c][0][:16]:16} {lit['hit90']} of {lit['size']} lit, mean {lit['mean']:.0f}, {lit['fam']}: {', '.join(lit['cl'])}")
