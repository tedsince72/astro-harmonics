#!/usr/bin/env python3
"""runner_record.py RACE [--off HH:MM:SS --dur SECONDS] [--tabs P03,P04] [--stages ...] [--force] [--jobs N]

The runner record (Eddie, 8 Oct 17:38-17:44): every runner in a race read the same way, horse then jockey, kept in full.
Fixed settings: natal at 12:00 (no natal Moon); window off-30 min to finish+30 min; chords <=0.15% (all three ratios in the
interval list, shortest side >=0.05 deg); numbers +-0.002 deg (kφ, φ^n, k√2, whole, ninths; own RA does not count, own Dec does).

Order of each record:
  0. the chart (positions, daily motion, out of bounds, turning in the day)
  1. body by body, every natal body incl. the natal Sun (no natal Moon):
       Method 1 - what the body is in the chart (numbers, star strings, figures with two bodies, midpoints, links to the partner)
       Method 3 - which sky bodies (not the Sun or Moon) play its strings, and how (texture fields below)
       Method 2 - the tuned layers on it (L1 star bases, Nodes, L2, L3, L4), transit Sun / Moon left to sections 2 and 3
  2. the transit Sun across all the runner's natal bodies     3. the transit Moon the same way, as the clock; Sun and Moon together
  4. the pair together: shared strings, direct links, same-body chords (sky X + horse X + jockey X)
Texture on every item: sky body, natal body, string (measure, base), chord and deviation both sides, time and zone, position on
the string, UNISON / tuned, SAME BODY, how many charts are on the string and who is tightest, the other sky bodies on the same
string (stacks, sequences), the natal string's strength in Method 1, whether the partner is on it.

Stages (each writes under /home/claude/rr/<RACE>/ and is reused unless --force):
  sky    lattice/m3d.py for every sky body, window off-30 to finish+30 (M3WIN=wide, MOONWIN=wide), full JSON dump
  m2     lattice/layer1_tuned.py, nodes_tuned.py, layer_tuned.py L2/L3/L4 with MOONWIN=wide (full dumps)
  sb     lattice/samebody2.py (same-body chords, JSON dump)
  m1     tools/natnums.py + natchords.py for every chart and body; tools/cross.py and lattice/mlist.py for every pair
  extra  tools/rr_extra.py (natal->transit numbers, sky->star numbers, parallels)
  records  writes records/<TAB>_<name>.md and .json for the chosen tabs (default: all)
Race off and duration come from reference/races.csv unless given."""
import argparse, collections, csv, itertools, json, math, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

H = '/home/claude'; LAT_D = f'{H}/lattice'; TOOLS = f'{H}/tools'; POSD = f'{H}/ledger/allpos'
BODIES = ['Rahu', 'Ketu', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Transpluto', 'Eris', 'Sedna', 'Makemake', 'Haumea', 'Gonggong', 'Quaoar', 'Orcus',
          'Jupiter', 'Saturn', 'Mars', 'Ceres', 'Pallas', 'Juno', 'Vesta', 'Sun', 'Mercury', 'Venus', 'Moon']          # sky bodies (as layer1_tuned)
NATAL_ORDER = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron', 'Ceres', 'Pallas', 'Juno', 'Vesta',
               'Eris', 'Sedna', 'Haumea', 'Makemake', 'Quaoar', 'Orcus', 'Gonggong', 'Transpluto', 'Rahu', 'Ketu']
LAYERS = ['L1', 'Nodes', 'L2', 'L3', 'L4']
OBL = 23.437
STRONG = 0.02      # a natal string within 0.02% is 'strong' in Method 1 (as m3compare); Method 1 deviations are kept in percent

# ------------------------------------------------------------------ setup
ap = argparse.ArgumentParser()
ap.add_argument('race'); ap.add_argument('--off'); ap.add_argument('--dur', type=float)
ap.add_argument('--tabs', default=''); ap.add_argument('--stages', default='sky,m2,sb,m1,extra,records')
ap.add_argument('--force', action='store_true'); ap.add_argument('--jobs', type=int, default=6)
A = ap.parse_args()
RACE = A.race
if not (A.off and A.dur):
    for r in csv.DictReader(open(f'{H}/reference/races.csv')):
        if r['race'] == RACE: A.off = A.off or r['off']; A.dur = A.dur or float(r['dur_s'])
if not (A.off and A.dur): sys.exit(f"no off time / duration for {RACE}: add it to {H}/reference/races.csv or pass --off and --dur")
OFF, DUR = A.off, A.dur
h_, m_, s_ = map(int, OFF.split(':')); T0 = h_ * 60 + m_ + s_ / 60; T1 = T0 + DUR / 60; TEND = T1 + 30
OUT = f'{H}/rr/{RACE}'
for d in ('m3', 'm2', 'm1', 'mlist', 'records', 'logs', 'notes'): os.makedirs(f'{OUT}/{d}', exist_ok=True)
META = list(csv.reader(open(f'{POSD}/{RACE}__META.csv')))
TABS = {r[0]: dict(role=r[1], cloth=r[2], name=r[3], dob=r[5] if len(r) > 5 else '') for r in META if r and r[0].startswith('P') and r[0][1:].isdigit()}
PAIR = {}
for t in sorted(TABS):
    if TABS[t]['role'] == 'horse':
        j = 'P%02d' % (int(t[1:]) + 1)
        if j in TABS and TABS[j]['role'] == 'jockey' and TABS[j]['cloth'] == TABS[t]['cloth']: PAIR[t] = j; PAIR[j] = t
FIN = {}
for p in (f'{H}/pinpoint_blind_kit/reference/profiles.csv', f'{H}/scored/profiles_test_scored.csv'):
    if os.path.exists(p):
        for r in csv.DictReader(open(p)):
            if r['race'] == RACE: FIN[r['cloth']] = dict(finish=r['finish'], sp=r['sp'], fav=r['fav'])
def label(t):
    n = TABS[t]['name'].split(' ', 1)[-1]; f = FIN.get(TABS[t]['cloth'], {})
    return n + (f" ({f.get('finish', '?')}, {f.get('sp', '?')})" if f else '')
def short(t): return TABS[t]['name'].split(' ', 1)[-1]
def run(cmd, env=None, out=None, cwd=LAT_D):
    e = dict(os.environ); e.update(env or {})
    with open(out or os.devnull, 'w') as f:
        p = subprocess.run(cmd, cwd=cwd, env=e, stdout=f, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0: raise RuntimeError(f"{' '.join(cmd)} failed:\n{p.stderr[-2000:]}")
    return p
def stage_on(name): return name in A.stages.split(',')
def need(path): return A.force or not os.path.exists(path) or os.path.getsize(path) == 0
ARGS = [RACE, OFF, str(int(DUR) if DUR == int(DUR) else DUR)]
GRIDF = f'{H}/ledger/skygrid/{RACE}__GRID.csv'          # the 1-minute race sky the sky, m2 and sb stages read
if any(stage_on(s) for s in ('sky', 'm2', 'sb')) and (not os.path.exists(GRIDF) or os.path.getsize(GRIDF) == 0):
    print(f"sky grid missing: lattice/skygrid.py {RACE} ...", file=sys.stderr)
    run(['python3', f'{LAT_D}/skygrid.py', RACE])
    print(f"  made {GRIDF} - copy it to the repo's data/skygrid/ with the records", file=sys.stderr)

# ------------------------------------------------------------------ stages
if stage_on('sky'):
    todo = [b for b in BODIES if need(f'{OUT}/m3/{b}.json')]
    if todo: print(f"sky: m3d for {len(todo)} sky bodies ...", file=sys.stderr)
    any_h = next(iter(PAIR), 'P01'); any_j = PAIR.get(any_h, 'P02')
    with ThreadPoolExecutor(A.jobs) as ex:
        list(ex.map(lambda b: run(['python3', f'{LAT_D}/m3d.py', *ARGS, b, any_h, any_j],
                                  env=dict(M3WIN='wide', MOONWIN='wide', M3DUMP=f'{OUT}/m3/{b}.json'), out=f'{OUT}/m3/{b}.txt'), todo))
if stage_on('m2'):
    jobs = [(l, ['python3', f'{LAT_D}/layer1_tuned.py', *ARGS]) if l == 'L1' else
            (l, ['python3', f'{LAT_D}/nodes_tuned.py', *ARGS]) if l == 'Nodes' else (l, ['python3', f'{LAT_D}/layer_tuned.py', *ARGS, l]) for l in LAYERS]
    jobs = [j for j in jobs if need(f'{OUT}/m2/{j[0]}.csv')]
    if jobs: print(f"m2: tuned layers {', '.join(j[0] for j in jobs)} ...", file=sys.stderr)
    os.makedirs(f'{LAT_D}/dump', exist_ok=True)
    def m2job(j):
        run(j[1], env=dict(MOONWIN='wide'), out=f'{OUT}/m2/{j[0]}.txt')
        shutil.copy(f'{LAT_D}/dump/{RACE}_{j[0]}.csv', f'{OUT}/m2/{j[0]}.csv')
    with ThreadPoolExecutor(A.jobs) as ex: list(ex.map(m2job, jobs))
if stage_on('sb') and need(f'{OUT}/sb2.json'):
    print("sb: same-body chords ...", file=sys.stderr)
    run(['python3', f'{LAT_D}/samebody2.py', *ARGS], env=dict(SB2DUMP=f'{OUT}/sb2.json'), out=f'{OUT}/sb2.txt')
if stage_on('m1'):
    DROP = re.compile(r"^===|NODES LAYER|transit Rahu|transit Ketu")
    def m1job(tb):
        tab, b = tb; f = f'{OUT}/m1/{tab}_{b}.txt'
        if not need(f): return
        a = run(['python3', f'{TOOLS}/natnums.py', *ARGS, tab, b, '0.002', '12'], out=f + '.n')
        c = run(['python3', f'{TOOLS}/natchords.py', *ARGS, tab, b, '12'], out=f + '.c')
        with open(f, 'w') as o:
            for part in (f + '.n', f + '.c'):
                for ln in open(part):
                    if DROP.search(ln) or (part.endswith('.n') and 'not at midday' in ln): continue
                    o.write(ln)
                os.remove(part)
    todo = [(t, b) for t in sorted(TABS) for b in NATAL_ORDER if need(f'{OUT}/m1/{t}_{b}.txt')]
    if todo: print(f"m1: natnums + natchords, {len(todo)} chart bodies ...", file=sys.stderr)
    with ThreadPoolExecutor(A.jobs) as ex: list(ex.map(m1job, todo))
    for hh in sorted(t for t in PAIR if TABS[t]['role'] == 'horse'):
        jj = PAIR[hh]; cf = f'{OUT}/cross_{hh}_{jj}.txt'
        if need(cf): run(['python3', f'{TOOLS}/cross.py', RACE, hh, jj], out=cf)
        run(['python3', f'{LAT_D}/mlist.py', RACE, hh, jj, f'{OUT}/m1', cf, f'{OUT}/mlist'], out=f'{OUT}/logs/mlist_{hh}.txt')
if stage_on('extra') and need(f'{OUT}/extra.json'):
    print("extra: natal->transit numbers, sky numbers, parallels ...", file=sys.stderr)
    run(['python3', f'{TOOLS}/rr_extra.py', *ARGS, f'{OUT}/extra.json'], out=f'{OUT}/logs/extra.txt', cwd=TOOLS)
if not stage_on('records'): sys.exit(0)

# ------------------------------------------------------------------ load everything
def hm(t):
    x = int(round(t * 60)); d = x // 86400; x %= 86400
    return f"{x // 3600}:{(x // 60) % 60:02d}:{x % 60:02d}" + (f" (day {d:+d})" if d else '')
def rel(t):
    if t < T0: return f"off−{T0 - t:.1f}m"
    if t <= T1: return f"off+{t - T0:.1f}m, in the race"
    return f"finish+{t - T1:.1f}m"
def zone(t): return 'before the off' if t < T0 else ('in the race' if t <= T1 else 'after the finish')
def pc(v): return '–' if v is None else f"{v * 100:.3f}%"
NATPOS = collections.defaultdict(lambda: collections.defaultdict(dict))     # tab -> body -> hour -> (ra, dec)
for r in csv.DictReader(open(f'{POSD}/{RACE}__NATAL_HOURLY.csv')):
    if r['ra'] and r['tab'] in TABS: NATPOS[r['tab']][r['body']][int(r['hour'])] = (float(r['ra']), float(r['dec']))
# Method 3 (and the Sun's / Moon's star strings)
M3 = {}
for b in BODIES:
    J = json.load(open(f'{OUT}/m3/{b}.json'))
    for r in J['rows']: r['sky'] = b
    M3[b] = J
EXACT_TOL = 0.00005      # 'exact' only when the leftover deviation at that moment is <=0.005% (8 Oct)
def truly_exact(r): return r['x'] is not None and not r['edge'] and (r.get('xdv') is None or r['xdv'] <= EXACT_TOL)
def exact_min(r):
    """the moment the chord is exact (minutes of the race day), None if it does not come exact within the span searched"""
    if not truly_exact(r): return None
    return T0 + r['x'] * 1440
def closest_min(r):
    """the exact moment, or for a chord that never comes exact its closest moment (from the same search)"""
    return None if r['x'] is None or r['edge'] else T0 + r['x'] * 1440
def row_time(r):
    """the time that places the chord: its exact moment when that lies in the window, else the tightest moment in the window"""
    te = exact_min(r)
    return te if te is not None and T0 - 30 <= te <= TEND else r['tbest']
STR = collections.defaultdict(list)        # (mm, frozenset(a, c)) -> every sky row on the string
for b in BODIES:
    for r in M3[b]['rows']: STR[(r['mm'], frozenset((r['a'], r['c'])))].append(r)
# Method 1 (natnums + natchords text, parsed as mlist does)
NUMRE = re.compile(r"^\s+to (.+?)\s{2,}([\d.]+) = (.+?)\s+\(([\d.]+), off ([+-][\d.]+)\)\s+(.+?)\s+\[00:00 ([\d.]+) · 24:00 ([\d.]+)\]")
CHRE = re.compile(r"^\s+(RA|Dec|Flat|Sky)\s+(.+?)–(.+?)\s+base\s+([\d.]+) \| to (.+?)\s+([\d.]+) \| to (.+?)\s+([\d.]+)\s+(.+?)\s+([\d.]+)%\s+\[00:00 (\S+)\s+24:00 (\S+)\]")
def m1parse(tab, b):
    f = f'{OUT}/m1/{tab}_{b}.txt'; nums, stc, boc = [], [], []
    if not os.path.exists(f): return nums, stc, boc
    meas = sect = None
    for ln in open(f, encoding='utf-8'):
        s = ln.strip()
        if s in ('RA:', 'Dec:', 'Flat:', 'Sky:', '|Dec|:'): meas = s[:-1]; sect = 'num'; continue
        if s.startswith('WITH THE STARS'): sect = 'star'; continue
        if s.startswith('WITH TWO OTHER NATAL'): sect = 'body'; continue
        if sect == 'num':
            m = NUMRE.match(ln)
            if m:
                tgt = m.group(1).replace(' ★', '').strip()
                if tgt == 'own' and meas == 'RA': continue            # a body's own RA does not count
                nums.append(dict(meas=meas, to=tgt, star='★' in m.group(1), val=float(m.group(2)), lab=m.group(3).strip(), off=float(m.group(5)),
                                 when=m.group(6).strip()))
        elif sect in ('star', 'body'):
            m = CHRE.match(ln)
            if m:
                g = m.groups(); pf = lambda x: None if '-' == x.strip('%').strip() else float(x.strip('%'))
                (stc if sect == 'star' else boc).append(dict(meas=g[0], A=g[1].strip(), B=g[2].strip(), base=float(g[3]), dA=float(g[5]), dB=float(g[7]),
                                                             ratio=g[8].strip(), dev=float(g[9]), d0=pf(g[10]), d24=pf(g[11])))
    return nums, stc, boc
M1 = {t: {b: m1parse(t, b) for b in NATAL_ORDER} for t in TABS}
NATSTR = {t: collections.defaultdict(list) for t in TABS}     # natal star strings: (mm, frozenset) -> [(body, chord)]
for t in TABS:
    for b in NATAL_ORDER:
        for c in M1[t][b][1]: NATSTR[t][(c['meas'], frozenset((c['A'], c['B'])))].append((b, c))
CROSS = {}
for hh in PAIR:
    if TABS[hh]['role'] != 'horse': continue
    f = f'{OUT}/cross_{hh}_{PAIR[hh]}.txt'
    CROSS[hh] = CROSS[PAIR[hh]] = [ln.rstrip() for ln in open(f)] if os.path.exists(f) else []
# Method 2
M2 = []
for l in LAYERS:
    for r in csv.DictReader(open(f'{OUT}/m2/{l}.csv')):
        for k in ('natal_dev', 'transit_dev', 'natal_dx', 'natal_de', 'transit_dx', 'transit_de', 'transit_t', 'natal_base', 'transit_base'):
            r[k] = float(r[k]) if r.get(k) not in (None, '') else None
        M2.append(r)
def m2key(r):
    """one transit strike: layer, base, transit body, and for the Moon its chord type and minute (several strikes per base)"""
    moon = r['transit_body'] == 'Moon' or 'Moon' in (r['x'], r['e'])
    return (r['layer'], r['mm'], r['x'], r['e'], r['transit_body']) + ((r['transit_type'], round(r['transit_t'], 3)) if moon else ())
M2IDX = collections.defaultdict(list)        # one transit strike -> rows (every chart tuned to it)
for r in M2: M2IDX[m2key(r)].append(r)
M2BASE = collections.defaultdict(set)        # (layer, mm, x, e) -> every transit body that plays the base
for r in M2: M2BASE[(r['layer'], r['mm'], r['x'], r['e'])].add(r['transit_body'])
SB = json.load(open(f'{OUT}/sb2.json'))
EXTRA = json.load(open(f'{OUT}/extra.json'))

# ------------------------------------------------------------------ texture helpers
def place(da, dc, base, a, c):
    """where a point sits on the string a–c, from its two distances and the base"""
    m = max(da, dc, base)
    if m == base:
        if abs(da - dc) <= 0.0015 * base: return 'at the MIDPOINT'
        return f"INSIDE (nearer {a if da < dc else c})"
    return f"beyond the {c} end" if m == da else f"beyond the {a} end"
def side_rel(p1, p2):
    if p1 == p2: return 'same place'
    if 'INSIDE' in p1 and 'INSIDE' in p2: return 'both inside'
    if 'beyond' in p1 and 'beyond' in p2: return 'opposite ends (mirror)'
    return 'one inside, one beyond'
def field(r):
    hold = r['hold']
    if not hold: return 'no natal body on the string'
    tabs_ = {h[1] for h in hold}; tight = min(hold)
    un = sum(1 for h in hold if h[3] == r['typ'])
    return f"{len(hold)} natal bodies in {len(tabs_)} charts (UNISON {un}); tightest {short(tight[1])} {tight[2]} {pc(tight[0])}"
def rank(r, tab, body):
    hold = sorted(r['hold']); i = next((k for k, h in enumerate(hold) if h[1] == tab and h[2] == body), None)
    return None if i is None else i + 1
def pathtxt(at):
    lab = ['off−30', 'off', 'finish', 'off+30', 'finish+30'] if len(at) == 5 else ['off−30', 'off', 'finish', 'finish+30']
    return ' · '.join(f"{l} {pc(v)}" for l, v in zip(lab, at))
def mirror(r, natc, a, c):
    """the sky body and the natal body both inside the string, each nearer a different end (a reflection across the midpoint)"""
    if not natc: return ''
    sa, sc, base = r['d_best']
    na, nc = (natc['dA'], natc['dB']) if natc['A'] == a else (natc['dB'], natc['dA'])
    if max(sa, sc) > base or max(na, nc) > natc['base']: return ''
    if (sa < sc) == (na < nc): return ''
    off = abs(min(sa, sc) - min(na, nc)) / base * 100
    what = 'MIRROR with natal' if off <= 1 else 'inside, nearer opposite ends'
    return f" · {what} (sky {min(sa, sc):.3f} from {a if sa < sc else c}, natal {min(na, nc):.3f} from {a if na < nc else c}; {off:.2f}% of the base apart)"
def exact_any(r):
    """minute of the exact moment wherever it falls (None if beyond the search span or never exact)"""
    return T0 + r['x'] * 1440 if truly_exact(r) else None
def zone_full(r):
    te = exact_any(r)
    if te is None: return 'does not come exact' if (r['x'] is not None and not r['edge']) else 'exact beyond the search span'
    if T0 - 30 <= te <= TEND: return zone(te)
    return 'held, separating' if te < T0 - 30 else 'held, applying'
def exact_txt(r):
    te = exact_any(r)
    if te is not None and T0 - 30 <= te <= TEND: return f"exact {hm(te)} ({rel(te)})"
    return r['when']
def timing(r):
    te = exact_min(r); at = r['at']
    path = pathtxt(at)
    if te is not None and T0 - 30 <= te <= TEND: w = f"exact {hm(te)} ({rel(te)})"
    else: w = f"tightest in the window {hm(r['tbest'])} ({rel(r['tbest'])}); {r['when']}"
    return w, path
def stack(key, but):
    """the other sky bodies on the same string in the window, in time order"""
    o = sorted((x for x in STR.get(key, []) if x['sky'] != but), key=row_time)
    return '; '.join(f"{x['sky']} {x['typ']} {pc(x['dv'])} {hm(row_time(x))}" for x in o)
def partner_on(tab, key):
    p = PAIR.get(tab)
    if not p: return ''
    L = NATSTR[p].get(key, [])
    return '; '.join(f"{b} {c['ratio']} {c['dev']:.3f}%" for b, c in sorted(L, key=lambda x: x[1]['dev']))
def m3_items(tab, body, skies):
    """every sky row (sky body in skies) whose string this natal body holds"""
    out = []
    for b in skies:
        for r in M3[b]['rows']:
            for h in r['hold']:
                if h[1] == tab and h[2] == body: out.append((r, h))
    return out
def m3_block(tab, body, skies, L, indent='  '):
    items = m3_items(tab, body, skies)
    if not items: L.append(f"{indent}- (no sky body plays its strings in the window)"); return 0
    by = collections.defaultdict(list)
    for r, h in items: by[(r['mm'], r['a'], r['c'])].append((r, h))
    keys = sorted(by, key=lambda k: min(row_time(r) for r, h in by[k]))
    for k in keys:
        mm, a, c = k; r0, h0 = by[k][0]
        key = (mm, frozenset((a, c)))
        nat = [x for x in NATSTR[tab].get(key, []) if x[0] == body]
        strength = f"Method 1 {nat[0][1]['ratio']} {nat[0][1]['dev']:.3f}%{' STRONG' if nat[0][1]['dev'] <= STRONG else ''}" if nat else "Method 1: (not in the 12:00 list)"
        L.append(f"{indent}- **{mm} {a}–{c}** — natal {body} {h0[3]} {pc(h0[0])} [natal {body}–{a} {h0[4]:.3f} | –{c} {h0[5]:.3f}]; {strength}; "
                 f"partner on it: {partner_on(tab, key) or 'no'}")
        for r, h in sorted(by[k], key=lambda x: row_time(x[0])):
            w, path = timing(r)
            base = r['d_best'][2]; sp = place(r['d_best'][0], r['d_best'][1], base, a, c)
            natc = nat[0][1] if nat else None
            npl = place(natc['dA'], natc['dB'], natc['base'], natc['A'], natc['B']) if natc else '?'
            tags = ['UNISON' if h[3] == r['typ'] else 'tuned'] + (['SAME BODY'] if r['sky'] == body else [])
            rk = rank(r, tab, body)
            L.append(f"{indent}  - sky **{r['sky']}** {r['typ']} {pc(r['dv'])} — {w}; {' · '.join(tags)}")
            L.append(f"{indent}    path {path} | sky {sp} [{r['sky']}–{a} {r['d_best'][0]:.3f} | –{c} {r['d_best'][1]:.3f} | base {base:.3f}] · "
                     f"natal {npl} → {side_rel(sp, npl)} | field: {field(r)}; this body #{rk}")
        st = stack(key, None)
        L.append(f"{indent}  - all sky bodies on this string in the window: {st}")
    return len(items)
def m2_rows(tab, body=None, transit=None, base_has=None, exclude_sm=False):
    out = []
    for r in M2:
        if r['tab'] != tab: continue
        if body and r['natal_body'] != body: continue
        sm = {'Sun', 'Moon'}
        if exclude_sm and (r['transit_body'] in sm or r['x'] in sm or r['e'] in sm): continue
        if transit and r['transit_body'] != transit: continue
        if base_has and base_has not in (r['x'], r['e']): continue
        out.append(r)
    return out
def m2_line(r, tab):
    flags = (['UNISON'] if r['natal_type'] == r['transit_type'] else ['tuned']) + (['SAME BODY'] if r['natal_body'] == r['transit_body'] else [])
    others = [x for x in M2IDX[m2key(r)] if not (x['tab'] == tab and x['natal_body'] == r['natal_body'])]
    others.sort(key=lambda x: x['natal_dev'])
    me_tight = all(r['natal_dev'] <= x['natal_dev'] for x in others)
    oth = '; '.join(f"{short(x['tab'])} {x['natal_body']} {x['natal_type']}{' U' if x['natal_type'] == x['transit_type'] else ''} {x['natal_dev'] * 100:.3f}%" for x in others[:12])
    more = f" (+{len(others) - 12} more)" if len(others) > 12 else ''
    ln = r.get('lengths') or ''
    lens = f" · base natal {r['natal_base']:.3f} / transit {r['transit_base']:.3f}{(' ' + ln) if ln else ''}" if r['natal_base'] is not None else ''
    third = 'natal ' + r['natal_body']
    return (f"**{r['layer']} {r['mm']} {r['x']}–{r['e']}** — {third} {r['natal_type']} {r['natal_dev'] * 100:.3f}% [{r['natal_dx']:.3f} | {r['natal_de']:.3f}] · "
            f"transit **{r['transit_body']}** {r['transit_type']} {r['transit_dev'] * 100:.3f}% [{r['transit_dx']:.3f} | {r['transit_de']:.3f}] {r['transit_when']}"
            f"{lens} · {' · '.join(flags)} · {'tightest of ' + str(len(others) + 1) if me_tight else 'tuned with it: ' + str(len(others) + 1)}"
            + (f"\n      also tuned: {oth}{more}" if others else ''))
def m2_block(rows, tab, L, indent='  '):
    if not rows: L.append(f"{indent}- (none)"); return
    def tkey(r):
        tt = r['transit_t'] if r['transit_body'] == 'Moon' or 'Moon' in (r['x'], r['e']) else None
        return (LAYERS.index(r['layer']), tt if tt is not None else -1, max(r['natal_dev'], r['transit_dev']))
    for r in sorted(rows, key=tkey): L.append(f"{indent}- {m2_line(r, tab)}")
def sb_lines(tab, pred, L, indent='  '):
    rows = [x for x in SB['part2'].get(tab, []) if pred(x)]
    if not rows: L.append(f"{indent}- (none)"); return
    for x in sorted(rows, key=lambda x: x['t']):
        e = x['edge']; d = x['d']
        tail = f"; followed out: {pc(e['dv'])} at {hm(e['t'])}{' (still closing at ±12 h)' if e['at_limit'] else ''}" if e else ''
        L.append(f"{indent}- natal {x['body']} – sky {x['body']} + {x['third']} **{x['mm']} {x['type']}** {pc(x['dv'])} at {hm(x['t'])} ({rel(x['t'])}) — {x['movement']}{tail}")
        L.append(f"{indent}  path off−30 {pc(x['at'][0])} · off {pc(x['at'][1])} · finish {pc(x['at'][2])} · finish+30 {pc(x['at'][3])} "
                 f"[natal–sky {d[0]:.3f} | natal–{x['third']} {d[1]:.3f} | sky–{x['third']} {d[2]:.3f}]")
def num_lines(L, rows, fmt, indent='  '):
    if not rows: L.append(f"{indent}- (none)"); return
    for x in sorted(rows, key=lambda x: x['t']):
        span = f"{hm(x['start'])}{' (window start)' if x['at_start'] else ''} – {hm(x['end'])}{' (window end)' if x['at_end'] else ''}"
        L.append(f"{indent}- {fmt(x)} = **{x['num']}** ({x['val']:.4f}, off {x['off']:+.4f}) closest {hm(x['t'])} ({rel(x['t'])}); within ±0.002 {span}")
def par_lines(L, rows, indent='  '):
    if not rows: L.append(f"{indent}- (none)"); return
    for x in sorted(rows, key=lambda x: x['min']):
        L.append(f"{indent}- sky {x['sky']} {x['kind']} natal {x['natal']} (natal Dec {x['natal_dec']:+.3f}): closest {x['min']:.3f} at {hm(x['t'])} ({rel(x['t'])})"
                 f"{' — at the window edge' if x['edge'] else ''}; within 0.1 {hm(x['start'])}–{hm(x['end'])}; off {x['at_off']:.3f}, finish {x['at_finish']:.3f}")

# ------------------------------------------------------------------ the record
def chart_table(tab, L):
    L.append("| Body | RA | Dec | RA /day | Dec /day | Out of bounds | In the birth day |")
    L.append("|---|---|---|---|---|---|---|")
    for b in NATAL_ORDER:
        P = NATPOS[tab].get(b)
        if not P or 12 not in P: continue
        ra, de = P[12]; hs = sorted(P); r0, d0 = P[hs[0]]; r24, d24 = P[hs[-1]]
        dra = ((r24 - r0 + 180) % 360) - 180; dde = d24 - d0
        steps = [((P[hs[i + 1]][0] - P[hs[i]][0] + 180) % 360) - 180 for i in range(len(hs) - 1)]
        dsteps = [P[hs[i + 1]][1] - P[hs[i]][1] for i in range(len(hs) - 1)]
        turn = []
        if steps and min(steps) < 0 < max(steps): turn.append('RA turns (station)')
        if dsteps and min(dsteps) < 0 < max(dsteps): turn.append('Dec turns')
        oob = f"YES {abs(de) - OBL:+.2f} out" if abs(de) > OBL else ''
        L.append(f"| {b} | {ra:.3f} | {de:+.3f} | {dra:+.3f} | {dde:+.3f} | {oob} | {', '.join(turn)} |")
def m1_block(tab, b, L):
    nums, stc, boc = M1[tab][b]
    L.append(f"- Numbers ({len(nums)}):")
    for n in sorted(nums, key=lambda n: ('ALL DAY' not in n['when'], '/9' in n['lab'], abs(n['off']))):
        t = 'own |Dec|' if n['to'] == 'own' else ('to ' + n['to'] + (' ★' if n['star'] else ''))
        L.append(f"  - {n['meas']} {t} = **{n['lab']}** ({n['val']:.4f}, off {n['off']:+.4f}; {n['when']})")
    for title, lst in (('Star strings', stc), ('Figures with two other natal bodies', boc)):
        L.append(f"- {title} ({len(lst)}):")
        for c in sorted(lst, key=lambda c: c['dev']):
            allday = c['d0'] is not None and c['d24'] is not None and c['d0'] <= 0.15 and c['d24'] <= 0.15
            pl = place(c['dA'], c['dB'], c['base'], c['A'], c['B'])
            pn = ''
            if title == 'Star strings': pn = partner_on(tab, (c['meas'], frozenset((c['A'], c['B']))))
            L.append(f"  - {c['meas']} {c['A']}–{c['B']} **{c['ratio']}** {c['dev']:.3f}%{' STRONG' if c['dev'] <= STRONG else ''} — {b} {pl}"
                     f" [base {c['base']:.3f} | to {c['A']} {c['dA']:.3f} | to {c['B']} {c['dB']:.3f}]"
                     f"{' — held all day' if allday else f' (00:00 {pc(None if c["d0"] is None else c["d0"] / 100)}, 24:00 {pc(None if c["d24"] is None else c["d24"] / 100)})'}"
                     f"{'; partner on it: ' + pn if pn else ''}")
    mids = [c for c in stc + boc if c['ratio'] == '1:1:2' and 'MIDPOINT' in place(c['dA'], c['dB'], c['base'], c['A'], c['B'])]
    if mids: L.append("- Midpoints: " + '; '.join(f"{c['meas']} {c['A']}–{c['B']} {c['dev']:.3f}%" for c in mids))
    links = [ln.strip() for ln in CROSS.get(tab, []) if re.search(rf"\b{tab} {re.escape(b)}\b", ln)]
    if links:
        L.append("- Direct links to the partner's chart (cross.py, 12:00):")
        for ln in links: L.append(f"  - {ln}")
def sun_moon_block(tab, X, L):
    """section 2 / 3: the transit Sun or Moon across all the runner's natal bodies"""
    L.append(f"\n### {X}'s star strings held by this chart (window off−30 to finish+30)")
    n = 0
    for b in NATAL_ORDER:
        if not m3_items(tab, b, [X]): continue
        L.append(f"\n**natal {b}**"); n += m3_block(tab, b, [X], L)
    if not n: L.append("- (none)")
    L.append(f"\n### Method 2 with the transit {X} (as the third point)")
    m2_block([r for r in m2_rows(tab, transit=X)], tab, L)
    L.append(f"\n### Strings where the {X} is a base end (L4 {X}–X bases; any transit third point)")
    m2_block([r for r in m2_rows(tab, base_has=X) if r['transit_body'] != X], tab, L)
    L.append(f"\n### Same-body chords with the {X}")
    sb_lines(tab, lambda x: x['body'] == X or x['third'] == X, L)
    if PAIR.get(tab):
        hh = tab if TABS[tab]['role'] == 'horse' else PAIR[tab]
        p1 = [x for x in SB['part1'].get(hh, []) if x['body'] == X]
        for x in p1: L.append(f"  - pair: sky {X} + horse {X} + jockey {X} {x['mm']} {x['type']} {pc(x['dv'])} at {hm(x['t'])} — {x['movement']}")
    if X == 'Sun':
        L.append("\n### Natal Sun → sky Sun (numbers)")
        num_lines(L, [x for x in EXTRA['n2t'].get(tab, []) if x['body'] == 'Sun'], lambda x: f"natal Sun – sky Sun {x['mm']}")
    L.append(f"\n### The sky {X}'s own numbers to the stars in the window (the same for every runner)")
    num_lines(L, EXTRA['skynum'].get(X, []), lambda x: f"{X} {x['mm']} to {x['to']}")
    L.append(f"\n### Parallels with the sky {X}")
    par_lines(L, [x for x in EXTRA['par'].get(tab, []) if x['sky'] == X])
def build(tab):
    t = TABS[tab]; f = FIN.get(t['cloth'], {}); p = PAIR.get(tab)
    L = [f"# Runner record — {t['name'].split(' ', 1)[-1]} ({t['role']}, {tab}) — {RACE}"]
    L.append(f"Cloth {t['cloth']} · finish {f.get('finish', '?')} · SP {f.get('sp', '?')}{' · FAVOURITE' if f.get('fav') == '1' else ''} · "
             f"born {t['dob']} · partner: {label(p) + ' (' + p + ')' if p else '—'}")
    L.append(f"Off {hm(T0)}, finish {hm(T1)} ({DUR:.2f} s). Window off−30 ({hm(T0 - 30)}) to finish+30 ({hm(TEND)}). Natal at 12:00, no natal Moon; "
             "chords ≤0.15%; numbers ±0.002°. Built by tools/runner_record.py (stages m3d / tuned layers / samebody2 / natnums+natchords / cross / rr_extra).")
    L.append("Reading the lines: **string** = the two base points and the measure; *path* = the sky chord's deviation at off−30 · off · finish · finish+30; "
             "*position* = where the point sits on the string (inside, beyond an end, midpoint); *field* = every natal body in the race on the string; "
             "UNISON = same chord type both sides; tuned = same base, another type; SAME BODY = sky X on natal X's string.\n")
    L.append("## 0. The chart (12:00)")
    chart_table(tab, L)
    L.append("\n## 1. Body by body")
    sky_other = [b for b in BODIES if b not in ('Sun', 'Moon')]
    for b in NATAL_ORDER:
        P = NATPOS[tab].get(b, {}).get(12)
        if not P: continue
        L.append(f"\n### {b} — RA {P[0]:.3f}, Dec {P[1]:+.3f}")
        L.append("\n#### Method 1 — what it is in the chart")
        m1_block(tab, b, L)
        L.append("\n#### Method 3 — the sky bodies on its strings (not the Sun or Moon), in time order")
        m3_block(tab, b, sky_other, L)
        sm = [r for r in m3_items(tab, b, ['Sun', 'Moon'])]
        if sm: L.append("  - (Sun / Moon on its strings: " + '; '.join(f"{r['sky']} {r['mm']} {r['a']}–{r['c']} {hm(row_time(r))}" for r, h in sorted(sm, key=lambda x: row_time(x[0]))) + " — sections 2 and 3)")
        L.append("\n#### Method 2 — tuned layers on it (transit Sun and Moon in sections 2 and 3)")
        m2_block(m2_rows(tab, body=b, exclude_sm=True), tab, L)
        L.append("\n#### Same body — natal " + b + " – sky " + b + " + a third point")
        sb_lines(tab, lambda x: x['body'] == b and x['third'] not in ('Sun', 'Moon'), L)
        nt = [x for x in EXTRA['n2t'].get(tab, []) if x['body'] == b]
        if nt and b != 'Sun':
            L.append(f"- Natal {b} → sky {b} numbers:")
            num_lines(L, nt, lambda x: f"natal {b} – sky {b} {x['mm']}", indent='  ')
        pr = [x for x in EXTRA['par'].get(tab, []) if x['natal'] == b and x['sky'] not in ('Sun', 'Moon')]
        if pr:
            L.append(f"- Sky bodies parallel / on the RA of natal {b}:"); par_lines(L, pr, indent='  ')
    L.append("\n## 2. The transit Sun")
    sun_moon_block(tab, 'Sun', L)
    L.append("\n## 3. The transit Moon — the clock")
    sun_moon_block(tab, 'Moon', L)
    L.append("\n### The Sun and the Moon on the same string, and on each other's distances")
    both = []
    for key, rows in STR.items():
        sk = {r['sky'] for r in rows}
        if {'Sun', 'Moon'} <= sk:
            mine = [h for r in rows for h in r['hold'] if h[1] == tab]
            both.append((key, rows, mine))
    held = [x for x in both if x[2]]
    L.append(f"- Star strings both play in the window: {len(both)}; held by this chart: {len(held)}")
    for key, rows, mine in sorted(held, key=lambda x: min(row_time(r) for r in x[1] if r['sky'] in ('Sun', 'Moon'))):
        mm, (a, c) = key[0], sorted(key[1])
        sm = '; '.join(f"{r['sky']} {r['typ']} {pc(r['dv'])} {hm(row_time(r))}" for r in sorted(rows, key=row_time) if r['sky'] in ('Sun', 'Moon'))
        L.append(f"  - {mm} {a}–{c}: {sm} — this chart: " + '; '.join(sorted({f"{h[2]} {h[3]} {pc(h[0])}" for h in mine})))
    sm2 = [r for r in m2_rows(tab) if (r['transit_body'] == 'Moon' and 'Sun' in (r['x'], r['e'])) or (r['transit_body'] == 'Sun' and 'Moon' in (r['x'], r['e']))]
    L.append("- The Moon on a Sun base / the Sun on a Moon base (L4), tuned with this chart:")
    m2_block(sm2, tab, L, indent='  ')
    if p:
        L.append(f"\n## 4. The pair together — {label(tab)} and {label(p)}")
        L.append("\n### Shared strings (both charts hold the same star string in the same measure, 12:00)")
        shared = [k for k in NATSTR[tab] if k in NATSTR[p]]
        played = [k for k in shared if k in STR]
        L.append(f"- {len(shared)} shared strings; {len(played)} of them played by a sky body in the window.")
        for k in sorted(played, key=lambda k: min(row_time(r) for r in STR[k])):
            mm, (a, c) = k[0], sorted(k[1])
            me = '; '.join(f"{b} {c_['ratio']} {c_['dev']:.3f}%" for b, c_ in sorted(NATSTR[tab][k], key=lambda x: x[1]['dev']))
            pa = '; '.join(f"{b} {c_['ratio']} {c_['dev']:.3f}%" for b, c_ in sorted(NATSTR[p][k], key=lambda x: x[1]['dev']))
            pl = '; '.join(f"{r['sky']} {r['typ']} {pc(r['dv'])} {hm(row_time(r))} ({zone(row_time(r))})" for r in sorted(STR[k], key=row_time))
            L.append(f"  - **{mm} {a}–{c}** — {short(tab)}: {me} | {short(p)}: {pa}\n    played by: {pl}")
        rest = [k for k in shared if k not in STR]
        if rest:
            L.append("- Shared strings not played in the window: " + '; '.join(
                f"{k[0]} {'–'.join(sorted(k[1]))} ({', '.join(b for b, _ in NATSTR[tab][k])} / {', '.join(b for b, _ in NATSTR[p][k])})" for k in sorted(rest, key=lambda k: (k[0], sorted(k[1])))))
        L.append("\n### Direct links between the two charts (cross.py, 12:00)")
        for ln in CROSS.get(tab, []): L.append(f"    {ln}")
        L.append("\n### Same-body chords — sky X + horse X + jockey X")
        hh = tab if t['role'] == 'horse' else p
        p1 = SB['part1'].get(hh, [])
        if not p1: L.append("- (none)")
        for x in sorted(p1, key=lambda x: x['t']):
            e = x['edge']; d = x['d']
            L.append(f"- **{x['body']} {x['mm']} {x['type']}** {pc(x['dv'])} at {hm(x['t'])} ({rel(x['t'])}) — {x['movement']}"
                     f"{f'; followed out {pc(e["dv"])} at {hm(e["t"])}' if e else ''} "
                     f"[sky–horse {d[0]:.3f} | sky–jockey {d[1]:.3f} | horse–jockey {d[2]:.3f}]")
        c_ = SB['control']
        L.append(f"- control ({c_['n']} other pairings): mean {c_['mean015']:.1f} ≤0.15% / {c_['mean005']:.1f} ≤0.05% / {c_['mean002']:.1f} ≤0.02%; "
                 f"this pair {len(p1)} / {sum(1 for x in p1 if x['dv'] <= 0.0005)} / {sum(1 for x in p1 if x['dv'] <= 0.0002)}")
    return '\n'.join(L) + '\n'
def items_json(tab):
    """flat list of the record's Method 3 items, for side-by-side comparison later"""
    out = []
    for b in NATAL_ORDER:
        for r, h in m3_items(tab, b, BODIES):
            out.append(dict(sky=r['sky'], natal=b, mm=r['mm'], a=r['a'], c=r['c'], sky_type=r['typ'], sky_dev=r['dv'], natal_type=h[3], natal_dev=h[0],
                            t=row_time(r), exact=exact_min(r), zone=zone(row_time(r)), unison=h[3] == r['typ'], same_body=r['sky'] == b,
                            rank=rank(r, tab, b), field=len(r['hold']), charts=len({x[1] for x in r['hold']}),
                            partner=bool(PAIR.get(tab) and NATSTR[PAIR[tab]].get((r['mm'], frozenset((r['a'], r['c'])))))))
    return out
# ------------------------------------------------------------------ the walk-through (the chat / project version)
# Same rule for every runner: everything whose exact moment falls in the window (off-30 to finish+30), body by body;
# then the transit Sun and the transit Moon in full; then the pair. The full record keeps everything else.
WMIN = re.compile(r"exact ([\d.]+) min (before|after) the off")
def m2_time(r):
    """minute the Method 2 transit chord is exact / held, or None if outside the window"""
    if r['transit_body'] == 'Moon' or 'Moon' in (r['x'], r['e']): return r['transit_t']
    m = WMIN.search(r['transit_when'] or '')
    if not m: return None
    t = T0 + float(m.group(1)) * (-1 if m.group(2) == 'before' else 1)
    return t if T0 - 30 <= t <= TEND else None
def in_win(t): return t is not None and T0 - 30 <= t <= TEND
def tz(t): return f"{hm(t)} ({'off' if abs(t - T0) < 0.05 else rel(t)})"
def w_m3(r, h, tab, notime=False):
    a, c = r['a'], r['c']; key = (r['mm'], frozenset((a, c)))
    nat = [x for x in NATSTR[tab].get(key, []) if x[0] == h[2]]; natc = nat[0][1] if nat else None
    sp = place(r['d_best'][0], r['d_best'][1], r['d_best'][2], a, c)
    npl = place(natc['dA'], natc['dB'], natc['base'], natc['A'], natc['B']) if natc else '?'
    tags = ('UNISON' if h[3] == r['typ'] else 'tuned') + (' · SAME BODY' if r['sky'] == h[2] else '')
    hold = r['hold']; others = [x for x in STR.get(key, []) if x is not r]
    also = '; '.join(f"{x['sky']} {hm(row_time(x))}" for x in sorted(others, key=row_time))
    pn = partner_on(tab, key)
    return (f"{'' if notime else tz(row_time(r)) + ' '}**{r['sky']}** {r['mm']} {a}–{c} {r['typ']} {pc(r['dv'])}{' (closest in the window ' + hm(r['tbest']) + ')' if notime else ''} · natal {h[2]} {h[3]} {pc(h[0])}"
            f"{' STRONG' if h[0] * 100 <= STRONG else ''} · {tags} · sky {sp}, natal {npl} · {len(hold)} bodies in {len({x[1] for x in hold})} charts, "
            f"this #{rank(r, tab, h[2])}{' (tightest)' if rank(r, tab, h[2]) == 1 else ', tightest ' + short(min(hold)[1]) + ' ' + min(hold)[2]}"
            f" · partner: {pn or 'no'}{' · also on the string: ' + also if also else ''}")
def w_m2(r, tab):
    others = [x for x in M2IDX[m2key(r)] if not (x['tab'] == tab and x['natal_body'] == r['natal_body'])]
    tight = all(r['natal_dev'] <= x['natal_dev'] for x in others)
    tags = ('UNISON' if r['natal_type'] == r['transit_type'] else 'tuned') + (' · SAME BODY' if r['natal_body'] == r['transit_body'] else '')
    ln = (r.get('lengths') or '')
    tt = m2_time(r)
    return (f"{tz(tt) if tt is not None else 'held at the off (' + (r['transit_when'] or '') + ')'} {r['layer']} **{r['transit_body']}** on {r['mm']} {r['x']}–{r['e']} {r['transit_type']} {r['transit_dev'] * 100:.3f}% · "
            f"natal {r['natal_body']} {r['natal_type']} {r['natal_dev'] * 100:.3f}% · {tags}{' · base ' + ln if ln and not ln.startswith('ratio') else ''} · "
            f"{'tightest of ' + str(len(others) + 1) if tight else str(len(others) + 1) + ' tuned'}")
def w_sb(x):
    return (f"{tz(x['t'])} same body: natal {x['body']} – sky {x['body']} + {x['third']} {x['mm']} {x['type']} {pc(x['dv'])} — {x['movement']}")
def w_num(x, what): return f"{tz(x['t'])} {what} = **{x['num']}** (off {x['off']:+.4f}; within ±0.002 {hm(x['start'])}–{hm(x['end'])})"
def m1_line(tab, b):
    """strongest strings, numbers and figures, out of bounds / turning, partner links — one line per body"""
    nums, stc, boc = M1[tab][b]
    st = sorted(stc, key=lambda c: c['dev']); strong = [c for c in st if c['dev'] <= STRONG]
    sdesc = lambda c: f"{c['meas']} {c['A']}–{c['B']} {c['ratio']} {c['dev']:.3f}%{' (all day)' if c['d0'] is not None and c['d24'] is not None and c['d0'] <= 0.15 and c['d24'] <= 0.15 else ''}"
    parts = []
    parts.append("strongest strings: " + ('; '.join(sdesc(c) for c in strong) if strong else (f"none ≤0.02% (tightest {sdesc(st[0])})" if st else 'none')))
    big = [n for n in nums if '/9' not in n['lab']]; nin = [n for n in nums if '/9' in n['lab']]
    nd = lambda n: f"{n['meas']} {'own |Dec|' if n['to'] == 'own' else n['to'] + (' ★' if n['star'] else '')} {n['lab']}{' (all day)' if 'ALL DAY' in n['when'] else ''}"
    parts.append("numbers: " + ('; '.join(nd(n) for n in big) if big else 'no φ/√2/whole') + f"; ninths {len(nin)}" +
                 (f" ({'; '.join(nd(n) for n in nin if 'ALL DAY' in n['when'])} all day)" if any('ALL DAY' in n['when'] for n in nin) else ''))
    fig = sorted([c for c in boc if c['dev'] <= STRONG], key=lambda c: c['dev'])
    parts.append("figures ≤0.02%: " + ('; '.join(f"{c['meas']} {c['A']}–{c['B']} {c['ratio']} {c['dev']:.3f}%" for c in fig) if fig else 'none'))
    P = NATPOS[tab][b]; hs = sorted(P); ra, de = P[12]
    steps = [((P[hs[i + 1]][0] - P[hs[i]][0] + 180) % 360) - 180 for i in range(len(hs) - 1)]
    dsteps = [P[hs[i + 1]][1] - P[hs[i]][1] for i in range(len(hs) - 1)]
    fl = []
    if abs(de) > OBL: fl.append(f"OUT OF BOUNDS {abs(de) - OBL:+.2f}")
    if steps and min(steps) < 0 < max(steps): fl.append('stationary in RA (turns in the birth day)')
    if dsteps and min(dsteps) < 0 < max(dsteps): fl.append('Dec turns in the birth day')
    if b in ('Mercury', 'Venus', 'Mars', 'Jupiter', 'Ceres', 'Pallas', 'Juno', 'Vesta'):    # near a station (as the §77 out-of-bounds / station check)
        dra = ((P[hs[-1]][0] - P[hs[0]][0] + 180) % 360) - 180; dde = P[hs[-1]][1] - P[hs[0]][1]
        slow = [f"RA {dra:+.3f}°/d" if abs(dra) < 0.05 else '', f"Dec {dde:+.3f}°/d" if abs(dde) < 0.03 else '']
        if any(slow): fl.append('near-stationary (' + ', '.join(x for x in slow if x) + ')')
    if fl: parts.append(', '.join(fl))
    links = [re.sub(r'\s+', ' ', ln.strip()) for ln in CROSS.get(tab, []) if re.search(rf"\b{tab} {re.escape(b)}\b", ln)]
    parts.append("partner links: " + ('; '.join(links) if links else 'none'))
    return ' · '.join(parts)
def walk(tab):
    t = TABS[tab]; f = FIN.get(t['cloth'], {}); p = PAIR.get(tab); nm = re.sub(r'[^a-z0-9]+', '-', short(tab).lower()).strip('-')
    L = [f"# Walk-through — {short(tab)} ({t['role']}, {tab}) — {RACE}",
         f"Finish {f.get('finish', '?')} · SP {f.get('sp', '?')}{' · FAVOURITE' if f.get('fav') == '1' else ''} · born {t['dob']} · partner {label(p) if p else '—'}",
         f"Full record: `rr/{RACE}/records/{tab}_{nm}.md` (repo tedsince72/astro-harmonics). Off {hm(T0)}, finish {hm(T1)}; window {hm(T0 - 30)}–{hm(TEND)}; "
         "natal 12:00, no natal Moon; chords ≤0.15%; numbers ±0.002°.",
         "Here, body by body: its Method 1 line; every sky body (not the Sun or Moon) on its star strings within 0.15% at any point in the window, "
         "with the deviation at off−30 / off / finish / finish+30, the exact time wherever it falls and the zone; then the Method 2 body-to-body "
         "and node layers, same-body chords ≤0.05% and natal→sky numbers that come exact in the window. Then the transit Sun, the transit Moon, the pair. "
         "Method 2's star-base layer (L1) is the same strings as Method 3 seen at the off, so it is not repeated here (it is in the record).",
         "", "## What I see"]
    nf = f'{OUT}/notes/{tab}.md'                      # my notes, kept apart so a rebuild never loses them
    L += ([open(nf).read().rstrip()] if os.path.exists(nf) else ["_(not written yet)_"])
    ch = []
    for b_ in NATAL_ORDER:
        for r, h in m3_items(tab, b_, BODIES):
            if str(r['when']).startswith('closest'): ch.append(f"{b_}: sky {r['sky']} {r['mm']} {r['a']}–{r['c']} {r['typ']} — {r['when']}")
    for r in M2:
        if r['tab'] == tab and str(r['transit_when']).startswith('closest'):
            ch.append(f"{r['natal_body']}: {r['layer']} {r['transit_body']} on {r['mm']} {r['x']}–{r['e']} {r['transit_type']} — {r['transit_when']}")
    L += ["", f"## Exact → closest (8 Oct check: 'exact' only when the deviation at that moment is ≤0.005%) — {len(ch)} items on this chart that earlier builds called exact"]
    L += [f"- {x}" for x in sorted(set(ch))] or ["- (none)"]
    L += ["", "## 1. Body by body — Method 1 line, every sky hold, other items exact in the window"]
    sky_other = [b for b in BODIES if b not in ('Sun', 'Moon')]
    for b in NATAL_ORDER:
        P = NATPOS[tab].get(b, {}).get(12)
        if not P: continue
        items = []; holds = []
        for r, h in m3_items(tab, b, sky_other):
            te = closest_min(r)
            holds.append((te if te is not None else r['tbest'], r, h))
        for r in m2_rows(tab, body=b, exclude_sm=True):
            if r['layer'] == 'L1': continue
            tt = m2_time(r)
            if in_win(tt): items.append((tt, w_m2(r, tab)))
        for x in SB['part2'].get(tab, []):
            if x['body'] == b and x['third'] not in ('Sun', 'Moon') and x['dv'] <= 0.0005 and not x['edge'] and in_win(x['t']): items.append((x['t'], w_sb(x)))
        for x in EXTRA['n2t'].get(tab, []):
            if x['body'] == b and b != 'Sun': items.append((x['t'], w_num(x, f"natal {b} – sky {b} {x['mm']}")))
        hs = sorted(NATPOS[tab][b]); oob = abs(P[1]) > OBL
        flag = f" — OUT OF BOUNDS {abs(P[1]) - OBL:+.2f}" if oob else ''
        L.append(f"\n**{b}** (RA {P[0]:.3f}, Dec {P[1]:+.3f}{flag})")
        L.append(f"- *Method 1:* {m1_line(tab, b)}")
        if holds:
            L.append(f"- *Sky bodies on its star strings within 0.15% in the window ({len(holds)} holds), string by string, in order of the first exact time:*")
            bys = collections.defaultdict(list)
            for tt, r, h in holds: bys[(r['mm'], r['a'], r['c'])].append((tt, r, h))
            for k in sorted(bys, key=lambda k: min(x[0] for x in bys[k])):
                mm, a, c = k; key = (mm, frozenset((a, c))); r0, h0 = bys[k][0][1], bys[k][0][2]
                natc = next((x[1] for x in NATSTR[tab].get(key, []) if x[0] == b), None)
                npl = place(natc['dA'], natc['dB'], natc['base'], natc['A'], natc['B']) if natc else '?'
                hold = r0['hold']; rk = rank(r0, tab, b)
                L.append(f"  - **{mm} {a}–{c}** — natal {b} {h0[3]} {pc(h0[0])}{' STRONG' if h0[0] * 100 <= STRONG else ''}, {npl} · {len(hold)} bodies in "
                         f"{len({x[1] for x in hold})} charts, this #{rk}{' (tightest)' if rk == 1 else ', tightest ' + short(min(hold)[1]) + ' ' + min(hold)[2] + ' ' + pc(min(hold)[0])}"
                         f" · partner: {partner_on(tab, key) or 'no'}")
                for tt, r, h in sorted(bys[k], key=lambda x: x[0]):
                    sp = place(r['d_best'][0], r['d_best'][1], r['d_best'][2], a, c)
                    mir = mirror(r, natc, a, c)
                    # a MIRROR is always the same chord type, so it carries the MIRROR tag in place of UNISON (not counted twice)
                    tags = ('MIRROR' if 'MIRROR' in mir else 'UNISON' if h[3] == r['typ'] else 'tuned') + (' · SAME BODY' if r['sky'] == b else '')
                    mir = mir.replace(' · MIRROR with natal', ' · mirror:')
                    L.append(f"    - {exact_txt(r)} — {zone_full(r)} · **{r['sky']}** {r['typ']} (closest {pc(r['dv'])} at {hm(r['tbest'])}) · {tags} · "
                             f"sky {sp}{mir} · {pathtxt(r['at'])}")
        else: L.append("- *Sky bodies on its star strings:* none within 0.15% in the window")
        if items:
            L.append("- *Other items exact in the window (Method 2 body/node layers, same body, numbers):*")
            for tt, s_ in sorted(items, key=lambda x: x[0]): L.append(f"  - {s_}")

    near = lambda t: t is not None and T0 - 10 <= t <= T1 + 10
    def moon_m3_keep(r, h):
        """outside off-10..finish+10: the textures Eddie listed (8 Oct 20:34)"""
        key = (r['mm'], frozenset((r['a'], r['c']))); why = []
        if h[0] * 100 <= STRONG: why.append('strong Method 1 string')
        oth = sorted({x['sky'] for x in STR.get(key, []) if x['sky'] != 'Moon'})
        if oth: why.append('also played by ' + ', '.join(oth))
        if h[3] == r['typ']: why.append('UNISON')
        if rank(r, tab, h[2]) == 1: why.append('tightest in the field')
        if partner_on(tab, key): why.append('partner on it')
        return why
    def moon_m2_keep(r):
        why = []
        if r['natal_dev'] * 100 <= STRONG: why.append('strong Method 1 figure')
        oth = sorted(b for b in M2BASE[(r['layer'], r['mm'], r['x'], r['e'])] if b != 'Moon')
        if oth: why.append('also played by ' + ', '.join(oth))
        if r['natal_type'] == r['transit_type']: why.append('UNISON')
        if r['natal_body'] == r['transit_body']: why.append('same body')
        others = [x for x in M2IDX[m2key(r)] if not (x['tab'] == tab and x['natal_body'] == r['natal_body'])]
        if all(r['natal_dev'] <= x['natal_dev'] for x in others): why.append('tightest in the field')
        if PAIR.get(tab) and any(x['tab'] == PAIR[tab] for x in M2IDX[m2key(r)]): why.append('partner on it')
        if 'Sun' in (r['x'], r['e']): why.append("on the Sun's distance")
        return why
    for X in ('Sun', 'Moon'):
        L.append(f"\n## {'2. The transit Sun (in full, time order)' if X == 'Sun' else '3. The transit Moon — the clock (time order)'}")
        if X == 'Moon':
            L.append(f"Every Moon strike from off−10 ({hm(T0 - 10)}) to finish+10 ({hm(T1 + 10)}); outside that, only strikes with texture — on the runner's strongest "
                     "Method 1 strings (≤0.02%), on a string another sky body or the Sun also plays, UNISON or same body, the runner tightest in the field, "
                     "the partner on the string, or on the Sun's own distances — each marked with why it is kept. The full Moon list is in the repo record.")
        items = []; dropped = 0
        for b in NATAL_ORDER:
            for r, h in m3_items(tab, b, [X]):
                ln = w_m3(r, h, tab) + ('' if in_win(exact_min(r)) else f" — not exact in the window ({r['when']})")
                if X == 'Moon' and not near(row_time(r)):
                    why = moon_m3_keep(r, h)
                    if not why: dropped += 1; continue
                    ln += f" [kept: {'; '.join(why)}]"
                items.append((row_time(r), ln))
        for r in m2_rows(tab):
            if r['layer'] == 'L1': continue
            if r['transit_body'] == X or X in (r['x'], r['e']):
                tt = m2_time(r); ln = w_m2(r, tab)
                if X == 'Moon' and not near(tt):
                    why = moon_m2_keep(r)
                    if not why: dropped += 1; continue
                    ln += f" [kept: {'; '.join(why)}]"
                items.append((tt if tt is not None else T0, ln))
        for x in SB['part2'].get(tab, []):
            if x['body'] == X or x['third'] == X: items.append((x['t'], w_sb(x) + (f"; followed out {pc(x['edge']['dv'])} at {hm(x['edge']['t'])}" if x['edge'] else '')))
        if X == 'Sun':
            for x in EXTRA['n2t'].get(tab, []):
                if x['body'] == 'Sun': items.append((x['t'], w_num(x, f"natal Sun – sky Sun {x['mm']}")))
        for x in EXTRA['skynum'].get(X, []):
            if X == 'Moon' and not near(x['t']): dropped += 1; continue
            items.append((x['t'], w_num(x, f"sky {X} {x['mm']} to {x['to']}") + " (sky only, every runner)"))
        for x in EXTRA['par'].get(tab, []):
            if x['sky'] == X: items.append((x['t'], f"{tz(x['t'])} sky {X} {x['kind']} natal {x['natal']}, closest {x['min']:.3f}"))
        for tt, s in sorted(items, key=lambda x: x[0]): L.append(f"- {s}")
        if not items: L.append("- (none)")
        if X == 'Moon': L.append(f"- ({dropped} other Moon strikes outside off−10…finish+10 without those textures: in the full record)")
    L.append("\n### The Sun and the Moon on the same string (held by this chart)")
    n = 0
    for key, rows in sorted(STR.items(), key=lambda kv: min(row_time(r) for r in kv[1])):
        if not {'Sun', 'Moon'} <= {r['sky'] for r in rows}: continue
        mine = sorted({f"{h[2]} {h[3]} {pc(h[0])}" for r in rows for h in r['hold'] if h[1] == tab})
        if not mine: continue
        n += 1; a, c = sorted(key[1])
        L.append(f"- {key[0]} {a}–{c}: " + '; '.join(f"{r['sky']} {r['typ']} {hm(row_time(r))}" for r in sorted(rows, key=row_time) if r['sky'] in ('Sun', 'Moon'))
                 + f" — this chart: {'; '.join(mine)}")
    if not n: L.append("- (none)")
    if p:
        L.append(f"\n## 4. The pair — {short(tab)} and {short(p)}")
        shared = [k for k in NATSTR[tab] if k in NATSTR[p] and k in STR]
        hits = []
        for k in shared:
            for r in STR[k]:
                if in_win(exact_min(r)): hits.append((exact_min(r), k, r))
        L.append(f"- Shared strings struck in the window ({len(hits)}):")
        for te, k, r in sorted(hits, key=lambda x: x[0]):
            a, c = sorted(k[1])
            me = ', '.join(f"{b} {x['dev']:.3f}%" for b, x in NATSTR[tab][k]); pa = ', '.join(f"{b} {x['dev']:.3f}%" for b, x in NATSTR[p][k])
            L.append(f"  - {tz(te)} **{r['sky']}** {k[0]} {a}–{c} {r['typ']} — {short(tab)}: {me} | {short(p)}: {pa}")
        hh = tab if t['role'] == 'horse' else p
        p1 = [x for x in SB['part1'].get(hh, []) if in_win(x['t'])]
        def p1s(x):
            e = x.get('edge')
            tail = f" (at the window edge, {x['movement']}; tightest {pc(e['dv'])} at {hm(e['t'])})" if e else f" ({x['movement']})"
            return f"{x['body']} {x['mm']} {x['type']} {pc(x['dv'])} {hm(x['t'])}{tail}"
        L.append("- Same body, sky X + horse X + jockey X, in the window: " + ('; '.join(p1s(x) for x in sorted(p1, key=lambda x: x['t'])) or 'none'))
        par = [ln.strip() for ln in CROSS.get(tab, []) if 'PARALLEL' in ln]
        L.append("- Dec links between the two charts: " + ('; '.join(par) or 'none'))
    return '\n'.join(L) + '\n'
want = [x for x in A.tabs.split(',') if x] or sorted(TABS)
for tab in want:
    md = build(tab)
    nm = re.sub(r'[^a-z0-9]+', '-', short(tab).lower()).strip('-')
    open(f'{OUT}/records/{tab}_{nm}.md', 'w').write(md)
    json.dump(items_json(tab), open(f'{OUT}/records/{tab}_{nm}.json', 'w'))
    print(f"record {tab} {short(tab)}: {len(md.splitlines())} lines -> {OUT}/records/{tab}_{nm}.md", file=sys.stderr)
    if os.environ.get('RR_WALK', '1') != '0':
        wk = walk(tab); open(f'{OUT}/records/{tab}_{nm}_walk.md', 'w').write(wk)
        print(f"walk {tab}: {len(wk.splitlines())} lines", file=sys.stderr)
