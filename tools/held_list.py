#!/usr/bin/env python3
"""held_list.py RACE [TOL] [TABLE] - what is held through the race, every runner (Eddie, 9 Oct: "show everything for each runner",
"are they applying", "a joint thing between the horse, jockey and transit"; Method 2 added 9 Oct: "start with method 2").

Reads rr/<RACE>/compare/table.csv (tools/race_table.py). An item is HELD when its sky chord is within TOL % (default 0.02) at BOTH the off and
the finish. Kinds: M3 (star strings), M2 (tuned layers L1/Nodes/L2/L3/L4), SB (same body), SBP (pair same body).
A = applying (exact after the finish), S = separating (exact before the off), X = exact in the race; to exact = from the finish (A) / off (S).
Ends with the joint section: per pair, the transit bodies holding both charts; ★ = the same base (and measure) in both.
Output: rr/<RACE>/compare/held-through-the-race.md (in the repo folder this script sits in)."""
import sys, os, re, csv
import pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = sys.argv[1]; TH = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02
TAB = sys.argv[3] if len(sys.argv) > 3 else f'{REPO}/rr/{R}/compare/table.csv'
OUT = f'{REPO}/rr/{R}/compare/held-through-the-race.md'
races = {r['race']: r for r in csv.DictReader(open(f'{REPO}/reference/races.csv'))}
off = races[R]['off']; dur = float(races[R]['dur_s'])
def mi(s): h, m_, x = map(int, s.split(':')); return h * 60 + m_ + x / 60
OFF = mi(off); FIN = OFF + dur / 60
t = pd.read_csv(TAB, dtype=str)
for c in ['dev_off_%', 'dev_finish_%', 'm1_dev_%', 'sky_dev_%', 'natal_dev_%']: t[c] = pd.to_numeric(t[c], errors='coerce')
t['rd'] = t[['dev_off_%', 'dev_finish_%']].max(axis=1)

def clock(s):
    m_ = re.match(r'(\d+):(\d+):(\d+)(?: \(day ([+-]\d+)\))?', s or '')
    return None if not m_ else int(m_[4] or 0) * 1440 + int(m_[1]) * 60 + int(m_[2]) + int(m_[3]) / 60
def rel_text(z):
    """minutes from the off, from 'exact 12.3 min/h after/before the off' or 'in 2.1 d' / '2.1 d ago'"""
    m_ = re.search(r'([\d.]+) (min|h) (after|before) the off', z)
    if m_: v = float(m_[1]) * (60 if m_[2] == 'h' else 1); return v if m_[3] == 'after' else -v
    m_ = re.search(r'in ([\d.]+) d', z)
    if m_: return float(m_[1]) * 1440
    m_ = re.search(r'([\d.]+) d ago', z)
    if m_: return -float(m_[1]) * 1440
    return None
def trend(r): return 'A' if r['dev_finish_%'] < r['dev_off_%'] else 'S'
def state(r):
    z = str(r.exact_zone)
    if r.kind == 'M3':
        if r.zone == 'in the race' or z == 'in the race': return 'X', None
        if 'does not come exact' in z: return trend(r), None
        w = clock(r.exact_time)
        if 'applying' in z or z == 'after the finish': return 'A', None if w is None else w - FIN
        if 'separating' in z or z == 'before the off': return 'S', None if w is None else w - OFF
        return trend(r), None
    if r.kind == 'M2':
        if z.startswith('Moon held') or 'does not come exact' in z: return trend(r), None
        v = rel_text(z)
        if v is None: return trend(r), None
        if 0 <= v <= FIN - OFF: return 'X', None
        return ('A', v - (FIN - OFF)) if v > 0 else ('S', v)
    if 'IN THE RACE' in z: return 'X', None
    w = clock(r.exact_time)
    if 'applying' in z: return 'A', None if w is None else w - FIN
    if 'separating' in z: return 'S', None if w is None else w - OFF
    return trend(r), None
def fmt(d):
    a = abs(d); s = '+' if d > 0 else '−'
    return f"{s}{a / 1440:.1f} d" if a >= 1440 else (f"{s}{a / 60:.1f} h" if a >= 60 else f"{s}{a:.1f} min")

h = t[t.kind.isin(['M3', 'M2', 'SB', 'SBP']) & (t.rd <= TH)].copy()
h = h.drop_duplicates(['kind', 'tab', 'natal_body', 'sky_body', 'layer', 'mm', 'base', 'sky_chord'])
# M2 L1 (star bases) repeats an M3 star-string row when the same sky body, base, measure and natal body are on it: keep the M3 row
_m3 = set(zip(h[h.kind == 'M3'].tab, h[h.kind == 'M3'].sky_body, h[h.kind == 'M3'].mm, h[h.kind == 'M3'].base, h[h.kind == 'M3'].natal_body))
h = h[~((h.kind == 'M2') & (h.layer == 'L1') & pd.Series([k in _m3 for k in zip(h.tab, h.sky_body, h.mm, h.base, h.natal_body)], index=h.index))]
st = h.apply(state, axis=1); h['st'] = [a for a, b in st]; h['dist'] = [b for a, b in st]
order = t[['tab', 'runner', 'role', 'finish', 'sp', 'fav']].drop_duplicates().copy()
order['f'] = pd.to_numeric(order.finish, errors='coerce'); order = order.sort_values(['f', 'tab'])
L = []; P = L.append
P(f"# {R} — what is held through the race, every runner (sky chord within {TH}% at both the off and the finish)\n")
P(f"Off {off}, finish {int(FIN // 60)}:{int(FIN % 60):02d}:{round((FIN * 60) % 60):02d}. From `compare/table.csv`. All 25 sky bodies, all natal bodies. "
  "Kinds: **M3** star strings (Method 3) · **M2** tuned layers (Method 2: L1 star bases, Nodes, L2, L3, L4 — transit chord and natal chord on the "
  "same base; an L1 row that repeats an M3 row is shown once, as M3) · **SB** same body · **SBP** pair same body. A = applying (exact after the finish), S = separating (exact before the off), X = exact "
  "in the race; 'to exact' from the finish (A) or the off (S). Off→fin = sky deviation at the off and at the finish. Natal = the natal string "
  "(M3: Method 1, STRONG ≤0.02%) or the natal chord on the same base (M2). # = rank among all charts on that string / base (M2: 1 = tightest).\n")
def line(r):
    fl = ' '.join(f for f in [r.same_body if isinstance(r.same_body, str) else '', r.unison if isinstance(r.unison, str) else '',
                              r.mirror if isinstance(r.mirror, str) else '', 'PAIR (sky+horse+jockey)' if r.kind == 'SBP' else ''] if f)
    if r.kind == 'M3': nat = f"{r.natal_body} {r.natal_chord}"; nd = f"{r['m1_dev_%']:.3f}{' STRONG' if r.m1_strong == 'STRONG' else ''}"
    elif r.kind == 'M2': nat = f"{r.natal_body} {r.natal_chord}"; nd = f"{r['natal_dev_%']:.3f}"
    else: nat = f"{r.natal_body} ({r.note})"; nd = ''
    rank = f"{r['rank']}/{r.field_bodies}" if isinstance(r['rank'], str) else (f"–/{r.field_bodies}" if r.kind == 'M2' else '')
    d = 'in the race' if r.st == 'X' else ('' if r.dist is None or pd.isna(r.dist) else fmt(r.dist))
    kind = r.kind + (f" {r.layer}" if r.kind == 'M2' else '')
    return f"| {r.st} | {d} | {kind} | {r.sky_body} {r.sky_chord} | {r.mm} {r.base} | {nat} | {nd} | {r['dev_off_%']:.3f}→{r['dev_finish_%']:.3f} | {rank} | {fl} |"
for _, o in order.iterrows():
    x = h[h.tab == o.tab].copy(); x['k'] = x.st.map({'X': 0, 'A': 1, 'S': 2}); x = x.sort_values(['k', 'rd'])
    cnt = lambda k: f"A {((x.kind == k) & (x.st == 'A')).sum()} · S {((x.kind == k) & (x.st == 'S')).sum()} · X {((x.kind == k) & (x.st == 'X')).sum()}"
    P(f"\n## {o.runner} — {o.role}, finished {o.finish}, {o.sp}{' (fav)' if o.fav == 'fav' else ''}   ·   M3 {cnt('M3')}   ·   M2 {cnt('M2')}\n")
    P("| | to exact | kind | sky body + chord | measure, base | natal body + chord | natal dev | off→fin | # | flags |\n|---|---|---|---|---|---|---|---|---|---|")
    for _, r in x.iterrows(): P(line(r))
P("\n# Joint — horse, jockey and the same transit body\n")
P("For each pair: transit bodies that hold BOTH charts through the race (lists above). ★ = the same base and measure in both charts "
  "(M3 string or M2 tuned base). Plus the pair same-body chords.\n")
for _, o in order[order.role == 'horse'].iterrows():
    j = 'P%02d' % (int(o.tab[1:]) + 1)
    if j not in set(order.tab): continue
    jn = order[order.tab == j].runner.iloc[0]
    a = h[(h.tab == o.tab) & h.kind.isin(['M3', 'M2'])]; b = h[(h.tab == j) & h.kind.isin(['M3', 'M2'])]
    common = sorted(set(a.sky_body) & set(b.sky_body))
    P(f"\n## {o.runner} / {jn} — finished {o.finish}{' (fav)' if o.fav == 'fav' else ''}\n")
    if not common: P("- no transit body holds both charts")
    for sb in common:
        A = a[a.sky_body == sb]; B = b[b.sky_body == sb]
        same = set(zip(A.kind, A.mm, A.base)) & set(zip(B.kind, B.mm, B.base))
        f = lambda X: '; '.join(f"{r.st} {r.kind}{(' ' + r.layer) if r.kind == 'M2' else ''} {r.sky_chord} {r.mm} {r.base} → {r.natal_body} {r.natal_chord}"
                                f"{'*' if r.m1_strong == 'STRONG' else ''} [{r.rd:.3f}]" for _, r in X.iterrows())
        P(f"- **{sb}**{' ★ ' + ', '.join(f'{k} {m_} {bs}' for k, m_, bs in sorted(same)) if same else ''} — horse: {f(A)} | jockey: {f(B)}")
    for _, r in t[(t.kind == 'SBP') & (t.tab == o.tab)].iterrows():
        P(f"- pair same-body: {r.sky_body} {r.mm} {r.sky_chord} {r['sky_dev_%']}% · {r.exact_zone}")
open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(OUT, len(L), 'lines', sum(len(l) for l in L), 'chars')
