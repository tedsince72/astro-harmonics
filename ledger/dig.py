"""exploratory dig for one race: many raw measures per runner, to see where the winner stands apart."""
import sys, itertools, collections
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, NODES, ROYAL, FASTNATAL, special, results, dev_deg
R = sys.argv[1]
rc = Race(R); rc.build(); res = results(R)
name = {c: rc.names[c][0] for c in rc.charts}
fin = {c: res[c]['finish'] for c in res}
order = sorted(rc.charts, key=lambda c: (not fin[c].isdigit(), int(fin[c]) if fin[c].isdigit() else 99))
def best(v, m):
    f = max(FAMS, key=lambda k: FN[k](v, m)); return f, FN[f](v, m)
def natal_pairs(tab, lv=70):
    P = rc.natal[tab]; out = []
    for x, y in itertools.combinations(sorted(P), 2):
        if (x in STARS and y in STARS) or 'Moon' in (x, y): continue
        for m in ('RA', 'Dec'):
            if m == 'RA' and {x, y} == NODES: continue
            v = sep(P[x], P[y], m); f, s = best(v, m)
            if s >= lv: out.append((x, y, m, v, f, s))
    return out
print('RACE', R, 'order:', ', '.join(f"{fin[c]}:{name[c]} {res[c]['sp']}" for c in order))
# A. hubs >=70 and >=90 per chart
print('\nA. NATAL HUBS (count of relationships >=70; >=90 in brackets) - top 5 per chart')
NP = {}
for c in order:
    for sd, tab in sorted(rc.charts[c].items()):
        prs = natal_pairs(tab); NP[(c, sd)] = prs
        cnt = collections.Counter(); c90 = collections.Counter()
        for x, y, m, v, f, s in prs:
            for b in (x, y):
                if b not in STARS: cnt[b] += 1; c90[b] += s >= 90
        print(f"  {fin[c]} {name[c]:16} {sd}: total>=70 {len(prs):3} >=90 {sum(1 for p in prs if p[5]>=90):3} | " + ', '.join(f"{b} {n}({c90[b]})" for b, n in cnt.most_common(5)))
# B. royal stars in natal-natal >=90
print('\nB. ROYAL STARS in natal-natal (>=90)')
for c in order:
    out = []
    for sd in ('H', 'J'):
        for x, y, m, v, f, s in NP.get((c, sd), []):
            if s >= 90 and {x, y} & ROYAL: out.append(f"{sd} {x}–{y} {m} {v:.4f} {f} {s:.0f}")
    print(f"  {fin[c]} {name[c]:16} {len(out)}: " + '; '.join(out))
# C. pairs exact in BOTH coordinates (>=90 RA and Dec) within one chart
print('\nC. NATAL PAIRS STRONG IN BOTH RA AND DEC (>=80 each)')
for c in order:
    out = []
    for sd, tab in sorted(rc.charts[c].items()):
        P = rc.natal[tab]
        for x, y in itertools.combinations(sorted(P), 2):
            if (x in STARS and y in STARS) or 'Moon' in (x, y) or {x, y} == NODES: continue
            a = best(sep(P[x], P[y], 'RA'), 'RA'); b = best(sep(P[x], P[y], 'Dec'), 'Dec')
            if a[1] >= 80 and b[1] >= 80: out.append(f"{sd} {x}–{y} RA {a[0]} {a[1]:.0f} / Dec {b[0]} {b[1]:.0f}")
    print(f"  {fin[c]} {name[c]:16} {len(out)}: " + '; '.join(out))
# D. horse <-> jockey: same body distance, and cross distances that are clean (>=95)
print('\nD. HORSE <-> JOCKEY (same body in both charts: distance and score; cross pairs >=97)')
for c in order:
    H, J = rc.natal[rc.charts[c]['H']], rc.natal[rc.charts[c]['J']]
    same = []
    for b in H:
        if b in STARS or b == 'Moon' or b not in J: continue
        for m in ('RA', 'Dec'):
            v = sep(H[b], J[b], m); f, s = best(v, m)
            if s >= 90: same.append(f"{b} {m} {v:.4f} {f} {s:.0f}")
    cross = 0
    for x in H:
        for y in J:
            if x in STARS or y in STARS or 'Moon' in (x, y): continue
            for m in ('RA', 'Dec'):
                v = sep(H[x], J[y], m)
                if best(v, m)[1] >= 97: cross += 1
    print(f"  {fin[c]} {name[c]:16} same-body>=90: {len(same)} [{'; '.join(same)}] | cross >=97: {cross}")
# E. numbers held in BOTH horse and jockey natal (>=90, same value within 0.003)
print('\nE. SAME NUMBER IN HORSE AND JOCKEY NATAL (both >=90, within 0.003)')
for c in order:
    h = [p for p in NP[(c, 'H')] if p[5] >= 90]; j = [p for p in NP[(c, 'J')] if p[5] >= 90]
    out = []
    for a in h:
        for b in j:
            if a[2] == b[2] and abs(a[3] - b[3]) <= 0.003:
                out.append(f"{a[3]:.4f}{'='+special(a[3]) if special(a[3]) else ''} H {a[0]}–{a[1]} / J {b[0]}–{b[1]} {a[2]}")
    print(f"  {fin[c]} {name[c]:16} {len(out)}: " + '; '.join(out))
# F. sky -> natal on top-12 pairs' bodies: applying share and exactness
print('\nF. SKY->NATAL contacts from the bodies of the top-12 sky pairs (>=90, not onto stars): count, applying, tightest')
topb = sorted({b for k in rc.byrank[:12] for b in k} - STARS)
for c in order:
    tot = ap = 0; tight = []
    for sd, tab in rc.charts[c].items():
        P = rc.natal[tab]
        for s_ in topb:
            for n in P:
                if n in STARS or n == 'Moon': continue
                for m in ('RA', 'Dec'):
                    v = sep(rc.sky[s_], P[n], m); f, sc = best(v, m)
                    if sc >= 90:
                        tot += 1
                        dm = dev_deg(sep(rc.S3[s_]['m2'], P[n], m), f); dp = dev_deg(sep(rc.S3[s_]['p2'], P[n], m), f)
                        ap += dp < dm
                        tight.append((dev_deg(v, f), f"{sd} {s_}→{n} {m} {v:.4f}"))
    tight.sort()
    print(f"  {fin[c]} {name[c]:16} {tot:3} contacts, applying {ap} ({100*ap/max(tot,1):.0f}%) | tightest: {'; '.join(t for d, t in tight[:3])}")
# G. totals at >=90 and dead-exact natal pairs (dev <= 0.001 deg, >=90), fast bodies flagged
print('\nG. IMPRINT STRENGTH: natal pairs >=90 (both charts) and dead-exact (dev<=0.001)')
for c in order:
    t90 = ex = exf = 0; exl = []
    for sd in ('H', 'J'):
        for x, y, m, v, f, s in NP[(c, sd)]:
            if s >= 90:
                t90 += 1
                if dev_deg(v, f) <= 0.001:
                    if {x, y} & FASTNATAL: exf += 1
                    else: ex += 1; exl.append(f"{sd} {x}–{y} {m} {v:.4f}")
    print(f"  {fin[c]} {name[c]:16} >=90: {t90:3} | dead-exact (slow bodies) {ex:2}, (fast bodies) {exf} | {'; '.join(exl[:12])}")
# H. numbers repeating inside each natal chart (>=90, within 0.002, distinct pairs)
print('\nH. NUMBERS REPEATING INSIDE ONE NATAL CHART (>=90, within 0.002)')
for c in order:
    out = []
    for sd in ('H', 'J'):
        ps = [p for p in NP[(c, sd)] if p[5] >= 90]
        seen = set()
        for a, b in itertools.combinations(ps, 2):
            if a[2] == b[2] and abs(a[3] - b[3]) <= 0.002:
                out.append(f"{sd} {a[3]:.4f}{'='+special(a[3]) if special(a[3]) else ''} ({a[0]}–{a[1]} & {b[0]}–{b[1]}) {a[2]}")
    print(f"  {fin[c]} {name[c]:16} {len(out)}: " + '; '.join(out))
# J. natal hubs on the sky's busy bodies
print('\nJ. THE SKY BUSY BODIES (' + ', '.join(sorted(rc.busy)) + ') AS NATAL HUBS (>=70 count, >=90)')
for c in order:
    out = []
    for sd in ('H', 'J'):
        cnt = collections.Counter(); c90 = collections.Counter()
        for x, y, m, v, f, s in NP[(c, sd)]:
            for b in (x, y): cnt[b] += 1; c90[b] += s >= 90
        out.append(f"{sd} " + ', '.join(f"{b} {cnt[b]}({c90[b]})" for b in sorted(rc.busy) if b != 'Moon'))
    print(f"  {fin[c]} {name[c]:16} " + ' | '.join(out))
# K. horse x jockey cross distances repeating top-12 sky numbers (same coord, 0.005)
print('\nK. HORSE x JOCKEY cross distances repeating a top-12 sky number (same coordinate, within 0.005)')
skyv = []
for k in rc.byrank[:12]:
    for m in ('RA', 'Dec'):
        v = sep(rc.sky[k[0]], rc.sky[k[1]], m)
        if best(v, m)[1] >= 80: skyv.append((rc.pairs[k]['rank'], k, m, v))
for c in order:
    H, J = rc.natal[rc.charts[c]['H']], rc.natal[rc.charts[c]['J']]; out = []
    for x in H:
        for y in J:
            if (x in STARS and y in STARS) or 'Moon' in (x, y): continue
            for m in ('RA', 'Dec'):
                v = sep(H[x], J[y], m)
                for rk, k, sm, sv in skyv:
                    if sm == m and abs(v - sv) <= 0.005: out.append(f"#{rk} H {x}–J {y} {m} {v:.4f} ({v-sv:+.4f})")
    print(f"  {fin[c]} {name[c]:16} {len(out)}: " + '; '.join(out))
