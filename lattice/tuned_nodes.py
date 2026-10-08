"""tuned_nodes.py RACE OFF DUR_S - TRANSIT AND NATAL TUNED IN, Nodes layer, one race (Eddie, 6 Oct 2026).
Transit side: transit-transit chords = transit Rahu/Ketu + two Layer-1 points (stars on race day, equator, course latitude).
Natal side: natal-natal chords = the chart's own Rahu/Ketu + two Layer-1 points with the stars AT BIRTH (equator kept;
course latitude left out - it is a race-day point). Also the chart's own Rahu + own Ketu + one point.
TUNED IN = a transit chord and a natal chord on the same base (same two Layer-1 points, same measure).
Same base, same chord type = marked UNISON."""
import sys
src = open('/home/claude/lattice/nodes_chords.py').read()
exec(src.split('# A')[0]); exec(src.split('# runners')[1].split('for tab, (role')[0])
# transit-transit chords
TT = {}
for b in TN:
    for a, c in itertools.combinations(RN, 2):
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            r = tri(TN[b], REF[a], REF[c], mm)
            if r and r[1] <= 0.0015:
                ex = exact_days(lambda dd: tri(moved(TN[b], b, dd), REF[a], REF[c], mm), lockT(TN[b], REF[a], REF[c], mm))
                TT.setdefault((mm, a, c), []).append((b, r[0], ctype(r[0]), r[1], ex[1]))
print('=' * 112)
print(f"{RACE}  off {OFF}  - NODES LAYER: TRANSIT AND NATAL TUNED IN (same Layer-1 base, same measure)")
print('=' * 112)
print(f"Transit-transit chords at the off: {sum(len(v) for v in TT.values())} on {len(TT)} bases")
NN = {}
for tab, (role, cloth, nm) in order:
    rows = []
    for nb in ('Rahu', 'Ketu'):
        NP = NAT[tab][nb]
        pts = {a: (NATB[tab][a] if a in STARS else REF[a]) for a in RN if a != 'CourseLat' and (a not in STARS or a in NATB[tab])}
        for a, c in itertools.combinations(sorted(pts), 2):
            for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                r = tri(NP, pts[a], pts[c], mm)
                if r and r[1] <= 0.0015: rows.append(((mm, a, c), nb, r[0], ctype(r[0]), r[1]))
    NN[tab] = rows
print("\nBY RUNNER (finish order, horse then jockey)")
summary = []
for tab, (role, cloth, nm) in order:
    f = fin.get(cloth, ('?', '?', '0')); R = role[0].upper()
    hits = [(k, nb, d, typ, dv) for k, nb, d, typ, dv in NN[tab] if k in TT]
    print(f"\n[{f[0]}] {role.upper():6s} {nm:24s} {f[1]:>5s}{' FAV' if f[2] == '1' else '    '}  natal node chords {len(NN[tab]):2d}   tuned to a transit chord: {len(hits)}")
    for k, nb, d, typ, dv in sorted(hits, key=lambda x: x[4]):
        mm, a, c = k
        for tb, td, ttyp, tdv, ex in TT[k]:
            un = '  UNISON' if ttyp == typ else ''
            print(f"     base {mm:4s} {a}–{c} {td[2]:.3f}")
            print(f"        natal   {R}.{nb:4s} {typ:14s} {R}.{nb}–{a} {d[0]:.3f} | {R}.{nb}–{c} {d[1]:.3f}   dev {dv*100:.3f}%")
            print(f"        transit {tb:6s} {ttyp:14s} {tb}–{a} {td[0]:.3f} | {tb}–{c} {td[1]:.3f}   dev {tdv*100:.3f}%   {fmt_days(ex)}{un}")
    summary.append((f, role, nm, len(NN[tab]), hits))
print('\n' + '=' * 112)
print("BY TRANSIT CHORD - which charts are tuned in to it")
for k in sorted(TT, key=lambda k: min(abs(x[4]) if x[4] is not None else 99 for x in TT[k])):
    mm, a, c = k
    for tb, td, ttyp, tdv, ex in TT[k]:
        who = []
        for tab, (role, cloth, nm) in order:
            for kk, nb, d, typ, dv in NN[tab]:
                if kk == k: who.append(f"{nm.split(' ', 1)[1]} ({role[0]}{fin.get(cloth, ('?',))[0]}) {nb} {typ} {dv*100:.3f}%")
        print(f"   {mm:4s} {tb:5s} {ttyp:14s} on {a}–{c}  {fmt_days(ex)}")
        print(f"        tuned: {'; '.join(who) if who else '-'}")
