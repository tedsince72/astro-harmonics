"""moon_tuned.py RACE OFF DUR_S - the Moon's star chords tuned to the runners' natal points, minute by minute (Eddie, 6 Oct 2026).
A: every chart's natal Makemake and how close it is to the three Moon UNISON chords.
B: every Moon star chord from off-30 to off+30 (5 s steps): in / exact / out, and every chart with a natal point on the same base
   (stars at birth): UNISON = same chord type, else tuned. C: per chart, which natal points carry the Moon's chords in the race window."""
import sys
src = open('/home/claude/lattice/layer1_tuned.py').read()
exec(src.split('# transit chords')[0])
NATP = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] in BODIES and r['body'] != 'Moon':
        NATP[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
NAME = {tab: f"{nm.split(' ', 1)[1]} ({role[0]}{fin.get(cloth, ('?',))[0]} {fin.get(cloth, ('', '?'))[1]})" for tab, (role, cloth, nm) in order}
def bpts(tab):
    p = {a: NATB[tab][a] for a in RN if a in STARS and a in NATB[tab]}; p['Equator'] = REF['Equator']; return p
print('=' * 120); print(f"{RACE}  off {OFF}  finish {hm(t1)}  - THE MOON TUNED IN"); print('=' * 120)
print("\nA  NATAL MAKEMAKE OF EVERY CHART against the three Moon UNISON bases (Dec; stars at birth) - dev of each ratio set")
U3 = [('Dec', 'Fomalhaut', 'Polaris'), ('Dec', 'Antares', 'Sirius'), ('Dec', 'Deneb Algedi', 'Polaris')]
for tab, (role, cloth, nm) in order:
    MK = NATP[tab]['Makemake']; P = bpts(tab); out = []
    for mm, a, c in U3:
        d = [dist(MK, P[a], mm), dist(MK, P[c], mm), dist(P[a], P[c], mm)]
        rs = [max(d[0], d[1]) / min(d[0], d[1]), max(d[0], d[2]) / min(d[0], d[2]), max(d[1], d[2]) / min(d[1], d[2])]
        dv = max(iv(x)[1] for x in rs); out.append(f"{a}–{c} {ctype(d) if dv < 0.01 else '-':10s} {dv*100:6.3f}%")
    dob = [r for r in META if r and r[0] == tab][0][5]
    print(f"   {NAME[tab]:34s} born {dob}  Makemake RA {MK[0]:8.3f} Dec {MK[1]:+7.3f}   " + '   '.join(out))
# B
ts = np.arange(t0 - 30, t0 + 30 + 1e-9, 5 / 60)
life = {}
for t in ts:
    X = pos('Moon', t)
    for a, c in PAIRS:
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            r = tri(X, REF[a], REF[c], mm)
            if r and r[1] <= 0.0015:
                L = life.setdefault((mm, a, c), {'ts': [], 'best': (9, None, None)})
                L['ts'].append(t)
                if r[1] < L['best'][0]: L['best'] = (r[1], t, ctype(r[0]))
NATCH = {}
for tab in NATP:
    P = bpts(tab)
    for nb, NP in NATP[tab].items():
        for k in life:
            mm, a, c = k
            if a not in P or c not in P: continue
            r = tri(NP, P[a], P[c], mm)
            if r and r[1] <= 0.0015: NATCH.setdefault(k, []).append((tab, nb, ctype(r[0]), r[1]))
print(f"\nB  EVERY MOON STAR CHORD off-30 to off+30 (5 s): {len(life)} chords; tuned charts (U = UNISON)   race window off-2 {hm(t0-2)} to finish {hm(t1)}")
inrace = collections.defaultdict(list)
for k, L in sorted(life.items(), key=lambda x: x[1]['best'][1]):
    mm, a, c = k; dv, tb, typ = L['best']; a0, z0 = min(L['ts']), max(L['ts'])
    live = a0 <= t1 and z0 >= t0 - 2
    tun = NATCH.get(k, [])
    s_ = '; '.join(f"{'U ' if ty == typ else ''}{NAME[tab].split(' (')[0]}{' J' if tabs[tab][0]=='jockey' else ''}.{nb} {dvv*100:.3f}%" for tab, nb, ty, dvv in sorted(tun, key=lambda x: x[3]))
    print(f"   {'*' if live else ' '} {mm:4s} {typ:14s} {a}–{c:13s} in {a0-t0:+6.2f} exact {hm(tb)} ({tb-t0:+6.2f}) out {z0-t0:+6.2f}  dev {dv*100:.3f}%   {s_ if s_ else '-'}")
    if live:
        for tab, nb, ty, dvv in tun: inrace[tab].append((k, typ, nb, ty, dvv))
print("   (* = held at some moment between off-2 and the finish)")
print("\nC  PER CHART - natal points carrying the Moon's chords held in the race window")
for tab, (role, cloth, nm) in order:
    rows = inrace.get(tab, [])
    print(f"   {NAME[tab]:34s} {len(rows):2d}   UNISON {sum(1 for r in rows if r[1] == r[3]):d}   " +
          ', '.join(f"{nb}{'(U)' if ty == typ else ''} {k[0]} {k[1]}–{k[2]} {dvv*100:.3f}%" for k, typ, nb, ty, dvv in sorted(rows, key=lambda r: r[4])))
