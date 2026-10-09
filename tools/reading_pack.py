#!/usr/bin/env python3
"""reading_pack.py RACE [TABLE] - one race laid out for reading, layer by layer (Eddie, 9 Oct: "go through each race, each method / layer
and look at what is going on in detail - bodies / chords ... COMBINATIONS"; "how can we investigate all further races like this").

The machine part of the Doncaster reading (9 Oct), for any race. Reads rr/<RACE>/compare/table.csv (tools/race_table.py). Writes
rr/<RACE>/compare/reading-pack.md with:
  1. each layer - Method 3 (star strings), Method 2 Nodes, L2, L3, L4 - every runner's items LIVE at the race: struck in the race (X) or held
     within 0.02% at both the off and the finish, applying (A) or separating (S); tightest flags; M2 L1 rows that repeat Method 3 left out
  2. the natal Sun, Mars, Neptune and Uranus of every chart, across all layers
  3. joint: transits holding both charts of a pair (★ same base), and same-body crossings (a transit holding its own body in one chart and the
     partner too); 3b. joins by body: every triangle/string holding both charts, per pair, and a field table of which bodies and stars make the joins
  4. triangle corners: the same three points read in different layers (which body moves, who sits on each reading)
  5. same body, pair same body, natal->sky numbers, parallels near the race
  6. the race timeline per pair (non-Moon), off-2 min to finish+2 min, with BEATS = both charts of a pair within 10 s
It does not judge: it lays out what is there. The reading is done on it."""
import sys, os, re, collections
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = sys.argv[1]; TABLE = sys.argv[2] if len(sys.argv) > 2 else f'{REPO}/rr/{R}/compare/table.csv'
_src = open(f'{REPO}/tools/held_list.py', encoding='utf-8').read().split("h = t[t.kind.isin")[0]
_argv = sys.argv; sys.argv = ['held_list.py', R, '0.02', TABLE]; exec(_src); sys.argv = _argv
import pandas as pd
OUT = f'{REPO}/rr/{R}/compare/reading-pack.md'
W = 2.0          # timeline margin, minutes
BEAT = 10 / 60   # both charts within 10 s

def hms(m):
    s = int(round(m * 60)); return f"{s // 3600}:{(s // 60) % 60:02d}:{s % 60:02d}"
order = t[['tab', 'runner', 'role', 'finish', 'sp', 'fav']].drop_duplicates().copy()
order['f'] = pd.to_numeric(order.finish, errors='coerce'); order = order.sort_values(['f', 'tab'])
NAME = dict(zip(order.tab, order.runner)); FINP = dict(zip(order.tab, order.finish)); ROLE = dict(zip(order.tab, order.role))
def partner(tab):
    n = int(tab[1:]); j = 'P%02d' % (n + 1 if ROLE.get(tab) == 'horse' else n - 1)
    return j if j in NAME else None
def who(tab): return f"{NAME[tab]} ({FINP[tab]})"

# ---------------------------------------------------------------- live items (M3, M2)
v = t[t.kind.isin(['M3', 'M2'])].copy()
st_ = v.apply(state, axis=1); v['st'] = [a for a, b in st_]; v['dist'] = [b for a, b in st_]
v = v[(v.rd <= 0.02) | (v.st == 'X')]
v = v.drop_duplicates(['kind', 'tab', 'natal_body', 'sky_body', 'layer', 'mm', 'base', 'sky_chord'])
_m3 = set(zip(v[v.kind == 'M3'].tab, v[v.kind == 'M3'].sky_body, v[v.kind == 'M3'].mm, v[v.kind == 'M3'].base, v[v.kind == 'M3'].natal_body))
v = v[~((v.kind == 'M2') & (v.layer == 'L1') & pd.Series([k in _m3 for k in zip(v.tab, v.sky_body, v.mm, v.base, v.natal_body)], index=v.index))]
v['lay'] = v.apply(lambda r: 'M3' if r.kind == 'M3' else r.layer, axis=1)
v['ndev'] = v.apply(lambda r: r['m1_dev_%'] if r.kind == 'M3' else r['natal_dev_%'], axis=1)
v['tight'] = v.apply(lambda r: (r.m1_strong == 'STRONG') if r.kind == 'M3' else (r['natal_dev_%'] <= 0.02), axis=1)
v['top'] = v['rank'].astype(str) == '1'
v['k'] = v.st.map({'X': 0, 'A': 1, 'S': 2})

def when(r):
    if r.st == 'X': return 'in race'
    if r.dist is None or pd.isna(r.dist): return r.st
    d = r.dist; a = abs(d)
    return f"{r.st} {'+' if d > 0 else '−'}{a / 1440:.1f}d" if a >= 1440 else (f"{r.st} {'+' if d > 0 else '−'}{a / 60:.1f}h" if a >= 60 else f"{r.st} {'+' if d > 0 else '−'}{a:.1f}m")
def item(r, with_lay=False):
    fl = ' '.join(f for f in ['SAME BODY' if r.same_body == 'SAME BODY' else '', 'UNISON' if r.unison == 'UNISON' else '',
                              'MIRROR' if r.mirror == 'MIRROR' else ''] if f)
    nd = f"{r.ndev:.3f}%{' STRONG' if (r.kind == 'M3' and r.m1_strong == 'STRONG') else ''}"
    rk = f"#{r['rank']}/{r.field_bodies}" if isinstance(r['rank'], str) and r['rank'] not in ('', 'nan') else f"–/{r.field_bodies}"
    chk = ' [exact re-checked on the 1-min sky]' if 're-timed' in str(r.exact_zone) else (' [stage said exact; NOT exact on the 1-min sky]' if 'checked on the 1-minute sky' in str(r.exact_zone) else '')
    return (f"{'[' + r.lay + '] ' if with_lay else ''}{when(r)}{chk} · {r.sky_body} {r.sky_chord} on {r.mm} {r.base} → {r.natal_body} {r.natal_chord} {nd}"
            f" · sky {r['dev_off_%']:.3f}→{r['dev_finish_%']:.3f} · {rk}{' ' + fl if fl else ''}")

L = []; P = L.append
fin_s = hms(FIN)
P(f"# Reading pack — {R}\n")
P("Result: " + ' · '.join(f"{o.finish} {o.runner} ({o.role}{', ' + o.sp if isinstance(o.sp, str) else ''}{', fav' if o.fav == 'fav' else ''})" for _, o in order.iterrows()) + "\n")
P(f"Off {off}, finish {fin_s} ({dur:.0f} s). Live at the race = struck in the race (X) or held within 0.02% at both the off and the finish, applying "
  "(A, exact after the finish) or separating (S, exact before the off); +/− time to exact from the finish / the off. Natal dev = Method 1 string (M3, "
  "STRONG ≤0.02%) or the natal chord on the same base (M2). # = rank among all charts on that string/base (M2: #1 = tightest). Moon items are in the "
  "layers but not in the timeline. Made by tools/reading_pack.py; it lays out, it does not judge.\n")
P("| chart | " + ' | '.join(['M3', 'Nodes', 'L2', 'L3', 'L4']) + " |\n|---|---|---|---|---|---|")
for _, o in order.iterrows():
    cells = []
    for lay in ['M3', 'Nodes', 'L2', 'L3', 'L4']:
        x = v[(v.tab == o.tab) & (v.lay == lay)]
        cells.append(f"X{(x.st == 'X').sum()} A{(x.st == 'A').sum()} S{(x.st == 'S').sum()} · tight+top {(x.tight & x.top).sum()}")
    P(f"| {o.finish} {o.runner} | " + ' | '.join(cells) + " |")

# 1. layers
P("\n# 1. Layer by layer\n")
for lay, title in [('M3', 'Method 3 — sky body on a natal star string'), ('Nodes', 'Method 2 — Nodes layer'), ('L2', 'Method 2 — L2 (the slow outer bodies as base ends)'),
                   ('L3', 'Method 2 — L3 (Jupiter, Saturn, Mars, Ceres, Pallas, Juno, Vesta as base ends)'), ('L4', 'Method 2 — L4 (Sun, Mercury, Venus, Moon as base ends)')]:
    P(f"\n## {title}\n")
    for _, o in order.iterrows():
        x = v[(v.tab == o.tab) & (v.lay == lay)].sort_values(['k', 'rd'])
        if not len(x): continue
        P(f"**{o.finish} {o.runner}** ({o.role}{', fav' if o.fav == 'fav' else ''})")
        for _, r in x.iterrows(): P(f"- {'**' if (r.tight and r.top) else ''}{item(r)}{'**' if (r.tight and r.top) else ''}")
        P("")

# 2. focus bodies
P("\n# 2. Natal Sun, Mars, Neptune, Uranus — every chart, all layers\n")
near = lambda m: m is not None and OFF - W <= m <= FIN + W
t['tm_clock'] = t.exact_time.map(lambda s: clock(s) if isinstance(s, str) else None)
for body in ['Sun', 'Mars', 'Neptune', 'Uranus']:
    P(f"\n## natal {body}\n")
    for _, o in order.iterrows():
        x = v[(v.tab == o.tab) & (v.natal_body == body)].sort_values(['k', 'rd'])
        extra = t[(t.tab == o.tab) & (t.natal_body == body) & t.kind.isin(['SB', 'N2T'])]
        extra = extra[extra.tm_clock.map(near) | extra.exact_zone.astype(str).str.contains('IN THE RACE')]
        if not len(x) and not len(extra): continue
        P(f"**{o.finish} {o.runner}**")
        for _, r in x.iterrows(): P(f"- {item(r, True)}")
        for _, r in extra.iterrows():
            P(f"- [{r.kind}] {r.time if isinstance(r.time, str) else r.exact_time} · " + (f"natal {body} → sky {r.sky_body} {r.mm} {r.sky_chord}" if r.kind == 'N2T'
              else f"{body} + {str(r.note).replace('third point ', '')} {r.mm} {r.sky_chord} ({r.exact_zone})"))
        P("")

# 3. joint
P("\n# 3. Joint — horse, jockey and the same transit\n")
for _, o in order[order.role == 'horse'].iterrows():
    j = partner(o.tab)
    if not j: continue
    a = v[v.tab == o.tab]; b = v[v.tab == j]
    P(f"\n## {o.runner} / {NAME[j]} — finished {o.finish}{' (fav)' if o.fav == 'fav' else ''}\n")
    common = sorted(set(a.sky_body) & set(b.sky_body))
    for sb in common:
        A = a[a.sky_body == sb]; B = b[b.sky_body == sb]
        same = set(zip(A.mm, A.base)) & set(zip(B.mm, B.base))
        cross = [f"{NAME[x.tab]}'s own {sb}" for _, x in pd.concat([A, B]).iterrows() if x.natal_body == sb]
        f = lambda X: '; '.join(f"{r.lay} {when(r)} {r.sky_chord} {r.mm} {r.base} → {r.natal_body} {r.ndev:.3f}{'*' if (r.tight and r.top) else ''}" for _, r in X.iterrows())
        P(f"- **{sb}**{' ★ ' + ', '.join(f'{m_} {bs}' for m_, bs in sorted(same)) if same else ''}{' · SAME-BODY CROSSING: ' + ', '.join(sorted(set(cross))) if cross else ''}"
          f" — horse: {f(A)} | jockey: {f(B)}")
    for _, r in t[(t.kind == 'SBP') & (t.tab == o.tab)].iterrows():
        P(f"- pair same-body: {r.sky_body} {r.mm} {r.sky_chord} {r['sky_dev_%']}% · {r.exact_zone}")

# 3b. joins by body (9 Oct, Eddie: "keep building in the parts that would identify the winning reasons" - which bodies make the joins)
P("\n# 3b. Joins by body — every pair, every triangle or string holding BOTH charts (non-Moon)\n")
P("A join = one triangle (three points, one measure: a star string with its sky body, or a tuned base with its moving body) on which both the horse and "
  "the jockey have a live item. Per pair: each join with the tightest natal body of each chart (★ = that chart tightest on it and tight: STRONG / natal "
  "chord ≤0.02%), own bodies (SAME BODY), the stars in the triangle, and whether it is struck in the race. Then the field table: which sky bodies, "
  "natal bodies and stars make each pair's joins — compare the KIND of join across the pairs, not the number.\n")
_STARS = set(REF.keys()) if 'REF' in globals() else set()
def _tri(r):
    x, e = r.base.split('–', 1); return (r.mm, frozenset((r.sky_body, x, e)))
vj = v[v.sky_body != 'Moon'].copy(); vj['tri3'] = vj.apply(_tri, axis=1)
_BODYSET = set(t.sky_body.dropna()) | set(t.natal_body.dropna())
field_rows = []
for _, o in order[order.role == 'horse'].iterrows():
    j = partner(o.tab)
    if not j: continue
    a = vj[vj.tab == o.tab]; b = vj[vj.tab == j]
    common = set(a.tri3) & set(b.tri3)
    P(f"\n## {o.runner} / {NAME[j]} — finished {o.finish}{' (fav)' if o.fav == 'fav' else ''}: {len(common)} joins\n")
    if not common: P("- none"); field_rows.append((o, j, 0, set(), set(), set(), 0, 0)); continue
    P("| measure · points | stars | horse (tightest body) | jockey (tightest body) | own bodies | in the race |\n|---|---|---|---|---|---|")
    jb, js, jn, nown, nrace = set(), set(), set(), 0, 0
    def _key(k):
        A = a[a.tri3 == k]; B = b[b.tri3 == k]; return min(A.ndev.min(), B.ndev.min())
    for k in sorted(common, key=_key):
        A = a[a.tri3 == k].sort_values('ndev'); B = b[b.tri3 == k].sort_values('ndev'); ra, rb = A.iloc[0], B.iloc[0]
        pts_ = sorted(k[1]); stars = [x for x in pts_ if x not in _BODYSET]
        own = [f"H {x}" for x in A[A.same_body == 'SAME BODY'].natal_body] + [f"J {x}" for x in B[B.same_body == 'SAME BODY'].natal_body]
        race = 'X' if ((A.st == 'X').any() or (B.st == 'X').any()) else ''
        movers = sorted(set(A.sky_body) | set(B.sky_body))
        ht = '★ ' if (A.top & A.tight).any() else ''; jt = '★ ' if (B.top & B.tight).any() else ''
        P(f"| {k[0]} {'·'.join(pts_)} (moving: {', '.join(movers)}) | {', '.join(stars) or '—'} | {ht}{ra.natal_body} {ra.natal_chord} {ra.ndev:.3f} {ra.st} "
          f"| {jt}{rb.natal_body} {rb.natal_chord} {rb.ndev:.3f} {rb.st} | {', '.join(own) or '—'} | {race} |")
        jb |= set(movers); js |= set(stars); jn |= {f"H {ra.natal_body}", f"J {rb.natal_body}"}; nown += bool(own); nrace += bool(race)
    field_rows.append((o, j, len(common), jb, js, jn, nown, nrace))
P("\n**The field — which bodies and stars make each pair's joins** (sky bodies that move on the joins · stars in them · the pair's natal bodies on them):\n")
P("| pair (finish) | joins | with own bodies | struck in the race | sky bodies | stars | natal bodies (H / J) |\n|---|---|---|---|---|---|---|")
for o, j, n, jb, js, jn, nown, nrace in field_rows:
    P(f"| {o.runner} / {NAME[j]} ({o.finish}{', fav' if o.fav == 'fav' else ''}) | {n} | {nown} | {nrace} | {', '.join(sorted(jb))} | {', '.join(sorted(js))} | {', '.join(sorted(jn))} |")
P("")

# 4. triangle corners
P("\n# 4. Triangle corners — the same three points read in different layers\n")
P("Each line: one triangle (three points, one measure) with something exact in or within 10 min of the race; under it each reading = which body moves "
  "and on which base, and who is on that reading (tightest first).\n")
def pts(r):
    x, e = r.base.split('–', 1); return frozenset((r.sky_body, x, e))
v['tri'] = v.apply(lambda r: (r.mm, pts(r)), axis=1)
v['near'] = v.apply(lambda r: r.st == 'X' or (r.dist is not None and not pd.isna(r.dist) and abs(r.dist) <= 10), axis=1)
for key, g in v.groupby('tri'):
    if g.sky_body.nunique() < 2 or not g.near.any() or 'Moon' in key[1]: continue
    P(f"\n**{key[0]} {' · '.join(sorted(key[1]))}**")
    for (sb, base), gg in g.groupby(['sky_body', 'base']):
        gg = gg.sort_values('ndev'); r0 = gg.iloc[0]
        P(f"- {sb} moves on {base} ({r0.lay}, {r0.sky_chord}, {when(r0)}): " + '; '.join(f"{NAME[r.tab]} ({FINP[r.tab]}) {r.natal_body} {r.natal_chord} {r.ndev:.3f}" for _, r in gg.iterrows()))

# 5. same body, pair, numbers, parallels
P("\n# 5. Same body, pair same body, natal→sky numbers, parallels near the race\n")
for _, o in order.iterrows():
    sb = t[(t.tab == o.tab) & (t.kind == 'SB') & ((t.rd <= 0.02) | t.exact_zone.astype(str).str.contains('IN THE RACE'))].sort_values('rd')
    n2 = t[(t.tab == o.tab) & (t.kind == 'N2T')]; n2 = n2[n2.tm_clock.map(near)]
    pa = t[(t.tab == o.tab) & (t.kind == 'PAR') & t.note.astype(str).str.contains(r'closest 0\.00\d')]
    pa = pa[pa.time.map(lambda s: OFF - 30 <= (clock(s) or -1e9) <= FIN + 30 if isinstance(s, str) else False)]
    if not (len(sb) or len(n2) or len(pa)): continue
    P(f"**{o.finish} {o.runner}**")
    for _, r in sb.iterrows(): P(f"- SB {r.natal_body} + {str(r.note).replace('third point ', '')} {r.mm} {r.sky_chord} · sky {r['dev_off_%']:.3f}→{r['dev_finish_%']:.3f} · {r.exact_time} {r.exact_zone}")
    for _, r in n2.iterrows(): P(f"- N2T natal {r.natal_body} → sky {r.sky_body} {r.mm} {r.sky_chord} at {r.time} ({'IN THE RACE' if OFF <= clock(r.time) <= FIN else r.zone})")
    for _, r in pa.iterrows(): P(f"- PAR {r.natal_body} ∥ {r.sky_body} {r.mm} {r.note} at {r.time}")
    P("")
P("Pair same-body chords (sky X + horse X + jockey X): " + ('; '.join(f"{NAME[r.tab]} pair {r.sky_body} {r.mm} {r.sky_chord} {r['sky_dev_%']}% ({r.exact_zone})"
                                                            for _, r in t[t.kind == 'SBP'].iterrows()) or 'none') + "\n")

# 6. timeline
P(f"\n# 6. The race timeline — every pair, non-Moon, {hms(OFF - W)} to {hms(FIN + W)} (off {off}, finish {fin_s})\n")
P("M3 with the natal string ≤0.05%, M2 with the natal chord ≤0.03%, same body, natal→sky numbers. ◆ = BEAT: the other chart of the pair has an "
  "event within 10 s.\n")
def m2clock(z):
    m_ = re.search(r'min (?:after|before) the off \((\d+:\d+:\d+)\)', str(z)); return clock(m_[1]) if m_ else None
ev = []
for _, r in t.iterrows():
    if r.sky_body == 'Moon' or 'Moon' in str(r.base) or 'Moon' in str(r.note): continue
    if r.kind == 'M3' and r['m1_dev_%'] <= 0.05 and r.exact_zone in ('before the off', 'in the race', 'after the finish'): tm = clock(r.exact_time)
    elif r.kind == 'M2' and r['natal_dev_%'] <= 0.03: tm = m2clock(r.exact_zone)
    elif r.kind == 'SB' and 'min' in str(r.exact_zone) or (r.kind == 'SB' and 'IN THE RACE' in str(r.exact_zone)): tm = clock(r.exact_time)
    elif r.kind == 'N2T': tm = clock(r.time) if isinstance(r.time, str) else None
    else: continue
    if tm is None or not (OFF - W <= tm <= FIN + W): continue
    if r.kind == 'M2' and r.layer == 'L1': continue
    d = (f"{r.sky_body} {r.sky_chord} on {r.mm} {r.base} → {r.natal_body} {r.natal_chord} {(r['m1_dev_%'] if r.kind == 'M3' else r['natal_dev_%']):.3f}"
         f"{' STRONG' if r.m1_strong == 'STRONG' else ''}" if r.kind in ('M3', 'M2') else
         (f"natal {r.natal_body} → sky {r.sky_body} {r.mm} {r.sky_chord}" if r.kind == 'N2T' else f"{r.natal_body} + {str(r.note).replace('third point ', '')} {r.mm} {r.sky_chord}"))
    ev.append(dict(tab=r.tab, tm=tm, kind=r.kind + (' ' + r.layer if r.kind == 'M2' else ''), d=d))
ev = pd.DataFrame(ev).drop_duplicates(['tab', 'tm', 'kind', 'd']) if ev else pd.DataFrame(columns=['tab', 'tm', 'kind', 'd'])
beats_all = []
for _, o in order[order.role == 'horse'].iterrows():
    j = partner(o.tab)
    if not j: continue
    x = ev[ev.tab.isin([o.tab, j])].sort_values('tm')
    P(f"\n## {o.runner} / {NAME[j]} — finished {o.finish}{' (fav)' if o.fav == 'fav' else ''}\n")
    if not len(x): P("- nothing"); continue
    for _, r in x.iterrows():
        other = x[(x.tab != r.tab) & ((x.tm - r.tm).abs() <= BEAT)]
        zone = 'race' if OFF <= r.tm <= FIN else ('pre' if r.tm < OFF else 'post')
        P(f"- {'◆ ' if len(other) else ''}{hms(r.tm)} ({zone}) {'H' if r.tab == o.tab else 'J'} [{r.kind}] {r.d}")
        if len(other) and r.tab == o.tab: beats_all.append((o.finish, o.runner, hms(r.tm)))
P("\n**Beats (horse event with a jockey event within 10 s):** " + ('; '.join(f"{f} {n} at {tm}" for f, n, tm in beats_all) or 'none') + "\n")
open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(OUT, len(L), 'lines', sum(len(l) for l in L), 'chars')
