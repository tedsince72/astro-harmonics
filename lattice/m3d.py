"""m3d.py RACE OFF DUR_S BODY WIN_H WIN_J [SCFILE]  - METHOD 3, one sky body: who is held, and how (Eddie 8 Oct 08:35 "method 3 now").
1. Every chord the sky BODY makes with two Layer-1 points (22 stars as on race day, Equator, course latitude) that is within 0.15%
   somewhere from off-30 to off+30; its deviation at off-30 / off / finish / off+30; its exact time at the body's rate.
2. For each chord, every natal body in every chart (12:00, stars at birth; Equator yes, course latitude no) on the same base in the
   same measure: UNISON (same chord type) or tuned (another type); the winning pair first with their distances on both sides,
   then every other chart, tightest first. SAME BODY = natal BODY on the string BODY plays.
3. With SCFILE (sunchords.py output): the whole-day list matched to the winning pair's natal strings."""
import sys, re
BODY, WH, WJ = sys.argv[4], sys.argv[5], sys.argv[6]; SC = sys.argv[7] if len(sys.argv) > 7 else None; sys.argv = sys.argv[:4]
exec(open('/home/claude/lattice/layer1_tuned.py').read().split('# transit chords')[0])
NP = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] in BODIES and r['body'] != 'Moon': NP[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
NAME = {t: v[2] for t, v in tabs.items()}
place = {t: fin.get(v[1], ('?',))[0] for t, v in tabs.items()}
def natref(tab, a):
    if a == 'Equator': return (None, 0.0)
    if a == 'CourseLat': return None
    return NATB[tab].get(a)
TS = np.arange(t0 - 30, t0 + 30 + 1e-9, 0.25)
P0 = pos(BODY, t0)
print('=' * 116); print(f"{RACE} off {OFF} finish {hm(t1)} — METHOD 3, sky {BODY}: RA {P0[0]:.3f} Dec {P0[1]:+.3f}  (moving RA {RATE[BODY][0]:+.4f}/d, Dec {RATE[BODY][1]:+.4f}/d)")
print(f"winning pair: {NAME[WH]} ({WH}) / {NAME[WJ]} ({WJ})"); print('=' * 116)
rows = []
for a, c in itertools.combinations(RN, 2):
    for mm in ('RA', 'Dec', 'Flat', 'Sky'):
        if (REF[a][0] is None or REF[c][0] is None) and mm != 'Dec': continue
        best = (9, None)
        for t in TS:
            r = tri(pos(BODY, t), REF[a], REF[c], mm)
            if r and r[1] < best[0]: best = (r[1], t)
        if best[0] > 0.0015: continue
        at = []
        for t in (t0 - 30, t0, t1, t0 + 30):
            r = tri(pos(BODY, t), REF[a], REF[c], mm); at.append(r[1] if r else None)
        r0 = tri(pos(BODY, t0), REF[a], REF[c], mm) or tri(pos(BODY, best[1]), REF[a], REF[c], mm)
        typ = ctype(r0[0]); x, xd, edge = exact_t(BODY, a, c, mm)
        hold = []
        for tab in tabs:
            A, C = natref(tab, a), natref(tab, c)
            if A is None or C is None: continue
            for b, p in NP[tab].items():
                q = tri(p, A, C, mm)
                if q and q[1] <= 0.0015: hold.append((q[1], tab, b, ctype(q[0]), dist(p, A, mm), dist(p, C, mm)))
        rows.append((mm, best[0], a, c, r0[0], typ, at, x, edge, hold, best[1]))
def f(v): return '   –  ' if v is None else f"{v*100:.3f}%"
import os as _os, json as _json
if _os.environ.get('M3DUMP'):
    _json.dump([dict(mm=r[0], dv=r[1], a=r[2], c=r[3], typ=r[5], at=r[6], x=r[7], edge=bool(r[8]), tbest=float(r[10]),
                     hold=[[h[0], h[1], h[2], h[3]] for h in r[9]]) for r in rows], open(_os.environ['M3DUMP'], 'w'))
for mm in ('RA', 'Dec', 'Flat', 'Sky'):
    L = sorted([r for r in rows if r[0] == mm], key=lambda r: r[1])
    print(f"\n{mm}: {len(L)} chords within 0.15% (off−30 to off+30)")
    for mm_, dv, a, c, d, typ, at, x, edge, hold, tb in L:
        win = [h for h in hold if h[1] in (WH, WJ)]
        print(f"\n  {a}–{c}  {typ}  base {d[2]:.3f} | {BODY}–{a} {d[0]:.3f} | {BODY}–{c} {d[1]:.3f}   {when(x, edge, BODY)}")
        print(f"     off−30 {f(at[0])} | off {f(at[1])} | finish {f(at[2])} | off+30 {f(at[3])}")
        if not hold: print("     no natal body on this base"); continue
        un = [h for h in hold if h[3] == typ]
        tightest = min(hold)
        print(f"     on this base: {len(hold)} natal bodies in {len({h[1] for h in hold})} charts; UNISON (same {typ}) {len(un)}; tightest {NAME[tightest[1]]} {tightest[2]} {tightest[0]*100:.3f}%")
        for h in sorted(win):
            tag = 'UNISON' if h[3] == typ else 'tuned'
            sb = '  SAME BODY' if h[2] == BODY else ''
            print(f"     ★ {NAME[h[1]]:22s} {h[2]:10s} {h[3]:16s} {h[0]*100:.3f}% {tag}{sb}   [natal {h[2]}–{a} {h[4]:.3f} | –{c} {h[5]:.3f}]")
        rest = sorted(h for h in hold if h[1] not in (WH, WJ))
        if rest: print("       others: " + '; '.join(f"{NAME[h[1]]} ({place[h[1]]}) {h[2]} {h[3]}{' U' if h[3] == typ else ''}{' SB' if h[2] == BODY else ''} {h[0]*100:.3f}%" for h in rest))
# whole day, matched to the winning pair
if SC:
    WS = {}
    for tab in (WH, WJ):
        for a, c in itertools.combinations(RN, 2):
            for mm in ('RA', 'Dec', 'Flat', 'Sky'):
                A, C = natref(tab, a), natref(tab, c)
                if A is None or C is None: continue
                for b, p in NP[tab].items():
                    q = tri(p, A, C, mm)
                    if q and q[1] <= 0.0015: WS.setdefault((mm, frozenset((a, c))), []).append(f"{NAME[tab]} {b} {ctype(q[0])} {q[1]*100:.3f}%")
    day = re.compile(r"^\s+(\d+:\d+:\d+)\s+(RA|Dec|Flat|Sky)\s+(.+?)–(.+?)\s+base\s+([\d.]+).*?\s(\S+(?: \S+)?)\s+([\d.]+)%$")
    print(f"\nTHE WHOLE RACE DAY — {BODY}'s chords that come exact on the day, on the winning pair's natal strings (≤0.15% at exact):")
    inday = False
    for ln in open(SC):
        if ln.startswith('THE WHOLE DAY'): inday = True; continue
        if not inday: continue
        m = day.match(ln)
        if not m: continue
        t, mm, a, c, base, typ, dv = m.groups()
        if float(dv) > 0.15: continue
        k = (mm, frozenset((a.strip(), c.strip())))
        if k in WS: print(f"  {t} {mm} {a.strip()}–{c.strip()} {typ.strip()} {dv}% | " + '; '.join(WS[k]))
