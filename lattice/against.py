"""against.py RACE OFF DUR_S - the 'AGAINST' check for every runner (Eddie, 6 Oct 2026: in a small field the others may be
negatively affected). Uses the tuned-pair dumps of every layer (dump/RACE_L1/Nodes/L2/L3/L4.csv).
Each sky chord a runner is tuned to is followed every 5 s from off-10 to finish+2 (same chord type kept).
Only LIVE sky chords count: exact between off-2 and the finish, or coming in / going out in that window
(slow chords that simply hold all through are background and left out). Natal side tuned within 0.05% (UNISON within 0.15%).
 A DISCORD   - the sky chord is the √2 division (discord).
 B SAME NOTE - two or more runners in UNISON with the same sky chord: who holds it tighter.
 C IN / OUT  - the sky chord comes IN during the window, or goes OUT during it (before the finish).
Just say what we see - no scoring."""
import sys, csv, collections, math
src = open('/home/claude/lattice/layer1_tuned.py').read()
exec(src.split('# transit chords')[0])
LAYS = ['L1', 'Nodes', 'L2', 'L3', 'L4']
rows = []
for L in LAYS:
    try: rows += list(csv.DictReader(open(f"/home/claude/lattice/dump/{RACE}_{L}.csv")))
    except FileNotFoundError: print(f"(no dump for {L})", file=sys.stderr)
def P(n, t): return REF[n] if n in REF else pos(n, t)
DISS = [9 / 8, 16 / 9, 9 / 5, 15 / 8, 16 / 15]
def dissonant(typ):
    return '√2' in typ          # discord = the √2 division (Eddie: "root 2 is discord in musical harmony")
def other_diss(typ):
    try: a, b, c = map(int, typ.split(':'))
    except ValueError: return False
    for r in (b / a, c / a, c / b):
        if any(abs(r - d) / d < 0.001 for d in DISS): return True
    return False
TS = np.arange(t0 - 10, t1 + 2 + 1e-9, 5 / 60)
CH = {}
def follow(key):
    if key in CH: return CH[key]
    lay, mm, x, e, tb, ttyp = key
    pres = []; best = (9, None)
    for t in TS:
        r = tri(P(x, t), P(e, t), P(tb, t), mm)
        if r and r[1] <= 0.0015 and ctype(r[0]) == ttyp:
            pres.append(t)
            if r[1] < best[0]: best = (r[1], t)
    CH[key] = (pres, best); return CH[key]
WIN = (t0 - 2, t1)
NAME = {tab: (nm.split(' ', 1)[1], role, fin.get(cloth, ('?', '?'))) for tab, (role, cloth, nm) in order}
items = []
for r in rows:
    key = (r['layer'], r['mm'], r['x'], r['e'], r['transit_body'], r['transit_type'])
    nd = float(r['natal_dev']); un = r['natal_type'] == r['transit_type']
    if nd > (0.0015 if un else 0.0005): continue
    pres, best = follow(key)
    if not any(WIN[0] <= t <= WIN[1] for t in pres): continue
    a, z = min(pres), max(pres)
    edge = best[1] is None or best[1] <= TS[0] + 1e-9 or best[1] >= TS[-1] - 1e-9
    live = (not edge and WIN[0] <= best[1] <= WIN[1]) or (WIN[0] < a <= WIN[1]) or (WIN[0] <= z < WIN[1])
    if not live: continue
    status = []
    if WIN[0] < a <= WIN[1]: status.append(f"IN {hm(a)}")
    if WIN[0] <= z < WIN[1] - 1e-9 and z < TS[-1] - 1e-9: status.append(f"OUT {hm(z)}")
    if not status: status.append("holds")
    items.append(dict(tab=r['tab'], key=key, nb=r['natal_body'], nd=nd, ntyp=r['natal_type'], un=un, a=a, z=z,
                      ex=best[1], st=' '.join(status), dis=dissonant(r['transit_type'])))
def lab(k):
    lay, mm, x, e, tb, ttyp = k; return f"{lay:5s} {mm:4s} {x}–{e} + {tb} {ttyp}"
print('=' * 120); print(f"{RACE}  off {OFF}  finish {hm(t1)}  - THE 'AGAINST' CHECK, every runner (sky chords present off-2 to finish)"); print('=' * 120)
print("\nA  DISCORD - runners tuned to a dissonant sky chord in the window")
for it in sorted([i for i in items if i['dis']], key=lambda i: i['ex']):
    n = NAME[it['tab']]
    print(f"   {hm(it['ex'])} ({it['ex'] - t0:+.2f})  {lab(it['key']):62s}  [{n[2][0]}] {n[0]} ({n[1][0]}) {it['nb']} {it['ntyp']} {it['nd']*100:.3f}%{' UNISON' if it['un'] else ''}  {it['st']}")
print("\nB  SAME NOTE - two or more runners in UNISON with the same sky chord (tighter first)")
by = collections.defaultdict(list)
for it in items:
    if it['un']: by[it['key']].append(it)
for k, lst in sorted(by.items(), key=lambda kv: min(i['ex'] for i in kv[1])):
    if len({i['tab'] for i in lst}) < 2: continue
    lst = sorted(lst, key=lambda i: i['nd'])
    print(f"   {hm(lst[0]['ex'])} {lab(k)}{'  DISCORD' if lst[0]['dis'] else ''}")
    print("        " + '  >  '.join(f"[{NAME[i['tab']][2][0]}] {NAME[i['tab']][0]} ({NAME[i['tab']][1][0]}) {i['nb']} {i['nd']*100:.3f}%" for i in lst))
print("\nC  IN / OUT - per runner: tuned sky chords that come IN or go OUT between off-2 and the finish")
for tab, (role, cloth, nm) in order:
    n = NAME[tab]; mine = [i for i in items if i['tab'] == tab]
    ins = [i for i in mine if 'IN' in i['st']]; outs = [i for i in mine if 'OUT' in i['st']]
    dis = [i for i in mine if i['dis']]
    print(f"\n   [{n[2][0]}] {role.upper():6s} {n[0]:24s} {n[2][1]:>5s}   tuned in window {len(mine):3d}   IN {len(ins):2d}   OUT {len(outs):2d}   discord {len(dis):2d}")
    for i in sorted(ins + outs, key=lambda i: i['ex']):
        print(f"        {i['st']:22s} {lab(i['key']):62s} {i['nb']} {i['ntyp']} {i['nd']*100:.3f}%{' DISCORD' if i['dis'] else ''}")
