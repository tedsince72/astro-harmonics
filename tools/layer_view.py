#!/usr/bin/env python3
"""layer_view.py RACE KIND [LAYER] - one layer of one race, every runner, everything LIVE at the race (the view used for the full reads of
Doncaster and Catterick, 9 Oct 2026; see docs/reading_method.md).

KIND = M3 (sky body on a natal star string) or M2 (tuned layers) with LAYER = Nodes | L2 | L3 | L4.
Live = struck in the race (X) or the sky chord within 0.02% at BOTH the off and the finish, applying (A) or separating (S).
One line per item: state and time to exact (A from the finish, S from the off) · sky body + chord · measure + base · natal body + chord ·
natal deviation (M3: Method 1 string, * = STRONG <=0.02%; M2: natal chord on the same base) · [sky deviation at the off -> at the finish] ·
#rank/bodies on the string (M2: #1 = tightest, '-' otherwise) · SAME (same body) UNI (unison) MIR (mirror).
Runners in finishing order; within a runner X first, then A, then S, tightest at the race first."""
import sys, os
import pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R, KIND, LAY = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else '')
src = open(f'{REPO}/tools/held_list.py', encoding='utf-8').read().split("h = t[t.kind.isin")[0]
sys.argv = ['held_list.py', R, '0.02']; g = {'__file__': f'{REPO}/tools/held_list.py'}; exec(src, g); t = g['t']; state = g['state']
x = t[t.kind == KIND].copy()
if LAY: x = x[x.layer == LAY]
st = x.apply(state, axis=1); x['st'] = [a for a, b in st]; x['dist'] = [b for a, b in st]
x = x[(x.rd <= 0.02) | (x.st == 'X')].drop_duplicates(['tab', 'natal_body', 'sky_body', 'mm', 'base', 'sky_chord'])
od = t[['tab', 'runner', 'role', 'finish', 'fav']].drop_duplicates(); od['f'] = pd.to_numeric(od.finish, errors='coerce'); od = od.sort_values(['f', 'tab'])
for _, o in od.iterrows():
    y = x[x.tab == o.tab].copy(); y['k'] = y.st.map({'X': 0, 'A': 1, 'S': 2}); y = y.sort_values(['k', 'rd', 'natal_body', 'sky_body', 'mm', 'base', 'sky_chord'], kind='mergesort')
    print(f"\n{o.finish} {o.runner} ({o.role}{', fav' if o.fav == 'fav' else ''}) — X{(y.st == 'X').sum()} A{(y.st == 'A').sum()} S{(y.st == 'S').sum()}")
    for _, r in y.iterrows():
        nd = (f"{r['m1_dev_%']:.3f}{'*' if r.m1_strong == 'STRONG' else ''}" if KIND == 'M3' else f"{r['natal_dev_%']:.3f}")
        d = '' if r.st == 'X' else ('' if r.dist is None or pd.isna(r.dist) else (f"{r.dist / 60:+.1f}h" if abs(r.dist) < 1440 else f"{r.dist / 1440:+.1f}d"))
        fl = ' '.join(f for f in [('SAME' if r.same_body == 'SAME BODY' else ''), ('UNI' if r.unison == 'UNISON' else ''), ('MIR' if r.mirror == 'MIRROR' else '')] if f)
        print(f"  {r.st}{d:>7} {r.sky_body:10} {r.sky_chord:16} {r.mm:4} {r.base:22} → {r.natal_body:10} {r.natal_chord:16} {nd:7} "
              f"[{r['dev_off_%']:.3f}→{r['dev_finish_%']:.3f}] #{r['rank'] if isinstance(r['rank'], str) else '-'}/{r.field_bodies} {fl}")
