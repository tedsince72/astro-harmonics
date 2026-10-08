"""m3compare.py — the same Method 1 / Method 3 measures for every chart in the race (control check, Eddie 8 Oct 14:00)."""
import sys, json, glob, os, collections, itertools
sys.argv = ['x', '20220318_doncaster_1440', '14:40:41', '248']
exec(open('/home/claude/lattice/layer1_tuned.py').read().split('# transit chords')[0])
S = '/home/claude/tools'
NP = collections.defaultdict(dict)
for r in csv.DictReader(open(f"{POSD}/{RACE}__NATAL_HOURLY.csv")):
    if r['hour'] == '12' and r['ra'] and r['body'] in BODIES and r['body'] != 'Moon': NP[r['tab']][r['body']] = (float(r['ra']), float(r['dec']))
NAME = {t: v[2] for t, v in tabs.items()}; ROLE = {t: v[0] for t, v in tabs.items()}
place = {t: fin.get(v[1], ('?',))[0] for t, v in tabs.items()}
def natref(tab, a):
    if a == 'Equator': return (None, 0.0)
    if a == 'CourseLat': return None
    return NATB[tab].get(a)
# Method 1 strong strings (natal body on a star base, <=0.02%, stars at birth)
M1 = collections.defaultdict(set)
for tab in tabs:
    for a, c in itertools.combinations([x for x in RN if x != 'CourseLat'], 2):
        A, C = natref(tab, a), natref(tab, c)
        if A is None or C is None: continue
        for mm in ('RA', 'Dec', 'Flat', 'Sky'):
            if (A[0] is None or C[0] is None) and mm != 'Dec': continue
            for b, p in NP[tab].items():
                q = tri(p, A, C, mm)
                if q and q[1] <= 0.0002: M1[tab].add((mm, frozenset((a, c)), b))
rows = []
for f in glob.glob(f'{S}/m3json/*.json'):
    sb = os.path.basename(f)[:-5]
    for r in json.load(open(f)): r['sky'] = sb; rows.append(r)
win0, win1 = -30, 248 / 60 + 30           # minutes from the off
near0, near1 = -10, 248 / 60 + 10
def tmin(r): return None if r['x'] is None or r['edge'] else r['x'] * 1440
M = collections.defaultdict(collections.Counter)
played = collections.defaultdict(lambda: collections.defaultdict(set))   # tab -> (mm,base,body) -> sky bodies
playedT = collections.defaultdict(set)
for r in rows:
    if not r['hold']: continue
    best = min(r['hold']); t = tmin(r)
    inwin = t is not None and win0 <= t <= win1; near = t is not None and near0 <= t <= near1
    tabs_on = {h[1] for h in r['hold']}
    M[best[1]]['tightest'] += 1
    if inwin: M[best[1]]['tightest_exact_in_window'] += 1
    if near: M[best[1]]['tightest_exact_near_race'] += 1
    if len(tabs_on) == 1: M[best[1]]['only_chart_on_string'] += 1
    for h in r['hold']:
        if near and h[0] <= 0.0005: M[h[1]]['on_string_exact_near_race_<=0.05'] += 1
        if h[2] == r['sky']: M[h[1]]['same_body'] += 1
        k = (r['mm'], frozenset((r['a'], r['c'])), h[2])
        if k in M1[h[1]]:
            played[h[1]][k].add(r['sky'])
            if inwin: playedT[h[1]].add(k)
print(f"{'chart':26s} {'fin':>3s} {'M1 str':>6s} {'played':>6s} {'by 2+':>5s} {'by 3+':>5s} {'exact win':>9s} | {'tightest':>8s} {'tight+win':>9s} {'tight+near':>10s} {'only one':>8s} {'near≤.05':>8s} {'samebody':>8s}")
for tab in sorted(tabs, key=lambda t: (int(place[t]) if str(place[t]).isdigit() else 9, ROLE[t] != 'horse')):
    m = M[tab]; p = played[tab]
    print(f"{NAME[tab]:26s} {place[tab]:>3s} {len(M1[tab]):6d} {len(p):6d} {sum(1 for v in p.values() if len(v) >= 2):5d} {sum(1 for v in p.values() if len(v) >= 3):5d} {len(playedT[tab]):9d} | "
          f"{m['tightest']:8d} {m['tightest_exact_in_window']:9d} {m['tightest_exact_near_race']:10d} {m['only_chart_on_string']:8d} {m['on_string_exact_near_race_<=0.05']:8d} {m['same_body']:8d}")
# natal bodies with most of their strong strings played
print("\nnatal bodies with 3+ strong Method 1 strings and how many are played (by any sky body)")
for tab in sorted(tabs, key=lambda t: (int(place[t]) if str(place[t]).isdigit() else 9, ROLE[t] != 'horse')):
    cnt = collections.Counter(k[2] for k in M1[tab]); pc = collections.Counter(k[2] for k in played[tab])
    full = [f"{b} {pc[b]}/{n}" for b, n in cnt.most_common() if n >= 3 and pc[b] >= 0.75 * n]
    print(f"  {NAME[tab]:26s} " + (', '.join(full) if full else '—'))
# strikes near the race where the chart is tightest
print("\nsky chords exact from off−10 to finish+10 and who is tightest")
for r in sorted(rows, key=lambda r: tmin(r) if tmin(r) is not None else 9e9):
    t = tmin(r)
    if t is None or not (near0 <= t <= near1) or not r['hold']: continue
    best = min(r['hold']); n_on = len({h[1] for h in r['hold']})
    print(f"  {t:+6.1f} min  {r['sky']:10s} {r['mm']:4s} {r['a']}–{r['c']} {r['typ']:14s}  tightest {NAME[best[1]]} {best[2]} {best[0]*100:.3f}%  ({len(r['hold'])} bodies in {n_on} charts)")
