#!/usr/bin/env python3
"""prerace_score.py RACE [RACE ...] - a ROUGH score per pair from the threads seen in the seven known races (10 Oct 2026, Eddie: "a rough score
out of 10"). Not a rule and not a probability: it counts how many of the observed threads a pair shows in / near the race, the same way for
every race. Components (max 8, shown out of 10). Same-body chords held at both ends count as NEAR, and IN the race only when exact in it.
  A Sun-Mars across the pair (0-3): 3 = one chart's natal Sun and the other chart's natal Mars both tight IN the race (or held through it);
    2 = that cross within off-2 / finish+2 min; 1 = Sun and Mars tight near the race but only in one chart; 0 = none.
    "Tight" = M3/M2 natal string/chord <=0.02% (Moon included), a same-body chord held at both ends <=0.02%, or a natal->sky number whose
    +/-0.002 hold window covers the time.
  B tight join in the race (pack 3b, one chart tightest <=0.02%) (0-2): 2 = the other side also <=0.02%, 1 = one side only.
  C receivers: tightest (#1) items <=0.02% exact in the race, both charts, any layer incl. Moon (0-2): 1-2 -> 1, >=3 -> 2.
  D both-sides-tight beat within off-2 / finish+2 (0-1).
STANDOUT flag: the ONLY pair with A = 3 (Sun of one chart and Mars of the other, tight, in the race) AND the top (or joint-top) score.
Backtest on the seven known races: that rule fired twice (Doncaster, Catterick) and both were winners; the plain top score held the
winner outright in 1 of 7 (3 of 7 counting ties). Small sample - read as a rough guide only."""
import sys, re, os, collections
import pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def mi(s): h, m, x = map(int, s.split(':')); return h * 60 + m + x / 60
def score(R):
    P = f'{REPO}/rr/{R}/compare/'; t = pd.read_csv(P + 'table.csv'); L = open(P + 'reading-pack.md').read()
    off, fin = re.search(r'Off (\d+:\d+:\d+), finish (\d+:\d+:\d+)', L).groups(); O, F = mi(off), mi(fin); W = 2.0
    def clk(r):
        z = str(r.exact_zone)
        m = re.search(r'Moon held at (\d+:\d+:\d+)', z) or re.search(r'\((\d+:\d+:\d+)\)', z)
        if m: return mi(m.group(1))
        if r.kind in ('M3', 'SB', 'SBP') and isinstance(r.exact_time, str) and ('race' in z.lower() or 'off' in z or 'finish' in z): return mi(r.exact_time)
        return None
    t['c'] = t.apply(clk, axis=1)
    t['rd'] = t[['dev_off_%', 'dev_finish_%']].max(axis=1)
    def span(z):
        m = re.search(r'within ±0\.002 (\d+:\d+:\d+)\s*[–-]\s*(\d+:\d+:\d+)', str(z)); return (mi(m[1]), mi(m[2])) if m else (None, None)
    names = t[['tab', 'runner', 'role']].drop_duplicates(); NAME = dict(zip(names.tab, names.runner)); ROLE = dict(zip(names.tab, names.role))
    horses = [tb for tb in sorted(NAME) if ROLE[tb] == 'horse' and 'NON-RUNNER' not in str(NAME.get('P%02d' % (int(tb[1:]) + 1), ''))]
    def tight_events(tab, body):
        """list of (kind, in_race:bool, near:bool)"""
        out = []
        x = t[(t.tab == tab) & (t.natal_body == body)]
        for _, r in x.iterrows():
            if r.kind in ('M3', 'M2'):
                nd = r['m1_dev_%'] if r.kind == 'M3' else r['natal_dev_%']
                if pd.isna(nd) or nd > 0.02 or r.c is None or pd.isna(r.c): continue
                out.append((r.kind, O <= r.c <= F, O - W <= r.c <= F + W))
            elif r.kind == 'SB':
                held = r.rd <= 0.02
                c = r.c
                if held: out.append(('SB', c is not None and not pd.isna(c) and O <= c <= F, True))   # held chord: near; in the race only if exact in it
                elif c is not None and not pd.isna(c) and O - W <= c <= F + W and min(r['dev_off_%'], r['dev_finish_%']) <= 0.02: out.append(('SB', O <= c <= F, True))
            elif r.kind == 'N2T':
                a, b = span(r.exact_zone)
                if a is None: continue
                if a <= F and b >= O: out.append(('N2T', True, True))
                elif a <= F + W and b >= O - W: out.append(('N2T', False, True))
        return out
    # 3b tight joins in the race
    tj = collections.defaultdict(list); pair = None
    for l in L.split('\n'):
        m = re.match(r'## (.+) / (.+) — finished (.*): (\d+) joins', l)
        if m: pair = m.group(1); continue
        if l.startswith('## ') or l.startswith('# '): pair = None
        if pair and re.match(r"\| (RA|Dec|Flat|Sky) ", l):
            c = [x.strip() for x in l.strip('|').split('|')]
            def nb(s):
                tt = s.replace('★', '').split(); d = [float(v) for v in tt if re.fullmatch(r'\d\.\d{3}', v)]; return ('★' in s, d[-1] if d else 9)
            h, j = nb(c[2]), nb(c[3]); live = c[5].strip() == 'X' if len(c) > 5 else False
            if live and ((h[0] and h[1] <= 0.02) or (j[0] and j[1] <= 0.02)): tj[pair].append(2 if max(h[1], j[1]) <= 0.02 else 1)
    bl = re.search(r'\*\*Beats, both sides tight[^\n]*?:\*\* ([^\n]*)', L); beats = collections.Counter()
    if bl:
        for nm, tm in re.findall(r'(?:\?|\d+|[A-Z]+) (.+?) at (\d+:\d+:\d+)', bl.group(1)):
            if O - W <= mi(tm) <= F + W: beats[nm] += 1
    rows = []
    for h in horses:
        j = 'P%02d' % (int(h[1:]) + 1)
        if j not in NAME: continue
        ev = {(k, b): tight_events(k, b) for k in (h, j) for b in ('Sun', 'Mars')}
        inr = {k: any(e[1] for e in v) for k, v in ev.items()}; nr = {k: any(e[2] for e in v) for k, v in ev.items()}
        crossI = (inr[(h, 'Sun')] and inr[(j, 'Mars')]) or (inr[(j, 'Sun')] and inr[(h, 'Mars')])
        crossN = (nr[(h, 'Sun')] and nr[(j, 'Mars')]) or (nr[(j, 'Sun')] and nr[(h, 'Mars')])
        one = (nr[(h, 'Sun')] and nr[(h, 'Mars')]) or (nr[(j, 'Sun')] and nr[(j, 'Mars')])
        A = 3 if crossI else (2 if crossN else (1 if one else 0))
        B = max(tj.get(NAME[h], [0]) or [0])
        rec = 0
        for k in (h, j):
            x = t[(t.tab == k) & t.kind.isin(['M3', 'M2'])]
            for _, r in x.iterrows():
                nd = r['m1_dev_%'] if r.kind == 'M3' else r['natal_dev_%']
                if str(r['rank']) in ('1', '1.0') and not pd.isna(nd) and nd <= 0.02 and r.c is not None and not pd.isna(r.c) and O <= r.c <= F: rec += 1
        C = 2 if rec >= 3 else (1 if rec >= 1 else 0)
        D = 1 if beats[NAME[h]] else 0
        raw = A + B + C + D
        flags = ''.join(f for f, on in [('Hs', nr[(h, 'Sun')]), ('Hm', nr[(h, 'Mars')]), ('Js', nr[(j, 'Sun')]), ('Jm', nr[(j, 'Mars')])] if on)
        fin_ = t[t.tab == h].finish.iloc[0]
        rows.append(dict(fin=fin_, pair=f"{NAME[h]} / {NAME[j]}", A=A, B=B, C=C, rec=rec, D=D, score=round(raw * 10 / 8, 1), sunmars=flags))
    df = pd.DataFrame(rows).sort_values('score', ascending=False, kind='mergesort').reset_index(drop=True)
    df['flag'] = ''
    a3 = df[df.A == 3]
    if len(a3) == 1 and a3.score.iloc[0] == df.score.max(): df.loc[a3.index[0], 'flag'] = 'STANDOUT'
    elif len(a3) == 1: df.loc[a3.index[0], 'flag'] = 'only Sun-Mars in race'
    return off, df
if __name__ == '__main__':
    for R in sys.argv[1:]:
        off, df = score(R); print(f"\n## {R} (off {off})"); print(df.to_string(index=False))
