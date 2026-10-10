#!/usr/bin/env python3
"""match_lite.py MATCH [MATCH ...] - football LITE summary from compare/table.csv (10 Oct 2026, Eddie: "a lite version today to give a rough idea").

Why: over a 2-hour window every pair reaches the race scorer's ceiling (Arsenal-Leeds: all 22 player/manager pairs 8.8-10), so the race score
cannot separate the sides. This lays the match out by TIME instead - which side's charts are struck, by which bodies, when - and lists the
Sun-Mars combinations, as the threads seen in the races. It lays out; it does not judge.

Event = a live item with an exact clock time from kick-off to kick-off + duration (races.csv):
  M3 struck in the window (natal string = M3 natal chord; lite has no Method 1 stage) · M2 exact in the window (incl. "Moon held at") ·
  same body (SB) exact in the window · natal->sky number (N2T) at its exact time.
TIGHT = M3/M2 natal chord <=0.02% (SB and N2T are exact by definition). RECEIVER = tight AND the chart is #1 (tightest) on that string/base.
VERY TIGHT = natal chord <=0.005% and #1. Moon events are counted apart (the Moon is the clock: it strikes something every couple of minutes).
SUN-MARS = in one player/manager pair, one chart's natal Sun and the other chart's natal Mars both have a TIGHT non-Moon M3/M2 event within
5 min (same-body chords and numbers left out here: over two hours they fire for every chart).
Periods are real clock time from kick-off (first half ~0-47, half-time ~47-62, second half ~62-110 + added time)."""
import sys, os, re, collections
import pandas as pd
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def clk(s):
    m = re.search(r'(\d+):(\d\d):(\d\d)', str(s)); return int(m[1]) * 60 + int(m[2]) + int(m[3]) / 60 if m else None
def hms(m): s = int(round(m * 60)); return f"{s // 3600}:{(s // 60) % 60:02d}:{s % 60:02d}"
PER = [(0, 15), (15, 30), (30, 47), (47, 62), (62, 77), (77, 92), (92, 107), (107, 120)]
PNAME = ['0-15', '15-30', '30-47 (1st half end)', '47-62 (half-time)', '62-77', '77-92', '92-107', '107-120 (added)']

def events(t, O, F):
    ev = []
    for r in t.itertuples(index=False):
        z = str(r.exact_zone); tm = None
        if r.kind == 'M3' and z == 'in the race': tm = clk(r.exact_time)
        elif r.kind == 'M2':
            m = (re.search(r'Moon held at (\d+:\d+:\d+)', z) or re.search(r'min (?:after|before) the off \((\d+:\d+:\d+)\)', z)
                 or re.search(r'h (?:after|before) the off \(\d+ \w+ (\d+:\d+:\d+)\)', z))     # over 60 min: "exact 1.2 h after the off (10 Oct 13:42:00)"
            if m and 'does not come exact' not in z: tm = clk(m[1])
        elif r.kind == 'SB' and 'IN THE RACE' in z: tm = clk(r.exact_time)
        elif r.kind == 'N2T': tm = clk(r.time)
        if tm is None or not (O <= tm <= F): continue
        if r.kind == 'M2' and str(r.layer) == 'L1': continue      # L1 repeats Method 3 (as in the reading views)
        nd = getattr(r, 'm1_dev__') if r.kind == 'M3' else (getattr(r, 'natal_dev__') if r.kind == 'M2' else 0.0)
        try: nd = float(nd)
        except (TypeError, ValueError): nd = 9.0
        top = str(r.rank) in ('1', '1.0')
        moon = r.sky_body == 'Moon' or 'Moon' in str(r.base) or 'Moon' in str(r.note)
        if r.kind in ('M3', 'M2'):
            d = f"{r.sky_body} {r.sky_chord} on {r.mm} {r.base} → {r.natal_body} {r.natal_chord} {nd:.3f}%{' #1' if top else ''}"
        elif r.kind == 'SB': d = f"same body {r.natal_body} + {str(r.note).replace('third point ', '')} {r.mm} {r.sky_chord}"
        else: d = f"number: natal {r.natal_body} → sky {r.sky_body} {r.mm} {r.sky_chord}"
        ev.append(dict(tab=r.tab, tm=tm, kind=r.kind + (' ' + str(r.layer) if r.kind == 'M2' else ''), natal=r.natal_body, sky=r.sky_body,
                       nd=nd, top=top, tight=nd <= 0.02, vt=(nd <= 0.005 and top), moon=moon, d=d))
    return pd.DataFrame(ev)

def run(R):
    P = f'{REPO}/rr/{R}/compare/'
    t = pd.read_csv(P + 'table.csv', low_memory=False)
    t.columns = [c.replace('%', '_') for c in t.columns]
    L = open(P + 'reading-pack.md', encoding='utf-8').read()
    off, fin = re.search(r'Off (\d+:\d+:\d+), finish (\d+:\d+:\d+)', L).groups(); O, F = clk(off), clk(fin)
    names = t[['tab', 'runner', 'role']].drop_duplicates(); NAME = dict(zip(names.tab, names.runner)); ROLE = dict(zip(names.tab, names.role))
    MG = sorted(tb for tb in NAME if ROLE[tb] == 'manager')
    def mgr(tb): return [g for g in MG if int(g[1:]) <= int(tb[1:])][-1]
    side = {tb: mgr(tb) for tb in NAME}
    ev = events(t, O, F); ev['side'] = ev.tab.map(side)
    out = [f"# Football lite — {R}\n", f"Kick-off {off}, window to {fin}. Sides: " + ' v '.join(f"{NAME[g]} (P{int(g[1:]):02d}…)" for g in MG) + ".",
           "Lite build: sky every minute, same-body stage scanned every 5 min then refined to 15 s, Method 1 stage not run (M3 natal string = the "
           "M3 natal chord). Counts are background only - read the bodies and the times.\n"]
    nm = ev[~ev.moon]
    # 1. by period
    out.append("## 1. By period (real minutes from kick-off): tight receivers, non-Moon (very tight ≤0.005% #1 in brackets) · Moon receivers\n")
    out.append("| period | " + ' | '.join(f"{NAME[g]}: receivers (very tight) · Moon" for g in MG) + " |\n|---|" + "---|" * len(MG))
    for (a, b), pn in zip(PER, PNAME):
        cells = []
        for g in MG:
            x = ev[(ev.side == g) & (ev.tm >= O + a) & (ev.tm < O + b) & ev.tight & ev.top]
            cells.append(f"{(~x.moon).sum()} ({(x.vt & ~x.moon).sum()}) · {x.moon.sum()}")
        out.append(f"| {pn} | " + ' | '.join(cells) + " |")
    # 2. Sun-Mars
    out.append("\n## 2. Sun–Mars across a player / manager pair (both tight M3/M2 strings ≤0.02%, non-Moon, within 5 min)\n")
    sm_rows = []
    for g in MG:
        for p in [tb for tb in NAME if side[tb] == g and tb != g]:
            for a_, b_ in ((p, g), (g, p)):
                S = nm[(nm.tab == a_) & (nm.natal == 'Sun') & nm.tight & nm.kind.str.startswith('M')]
                M_ = nm[(nm.tab == b_) & (nm.natal == 'Mars') & nm.tight & nm.kind.str.startswith('M')]
                for _, s_ in S.iterrows():
                    for _, m_ in M_.iterrows():
                        if abs(s_.tm - m_.tm) <= 5:
                            sm_rows.append((g, p, hms(min(s_.tm, m_.tm)), f"{NAME[a_]} Sun [{s_.kind}] {s_.d} @ {hms(s_.tm)}", f"{NAME[b_]} Mars [{m_.kind}] {m_.d} @ {hms(m_.tm)}"))
    sm = pd.DataFrame(sm_rows, columns=['side', 'player', 'at', 'sun', 'mars']).drop_duplicates()
    for g in MG:
        x = sm[sm.side == g]
        out.append(f"**{NAME[g]}'s side** — {len(x)} combination(s), {x.player.nunique()} player(s): " + (', '.join(sorted({NAME[q] for q in x.player})) or 'none'))
        for r in x.sort_values('at').itertuples(): out.append(f"- {r.at} · {r.sun} ‖ {r.mars}")
        out.append("")
    # 3. very tight
    out.append("## 3. Very tight receivers (natal ≤0.005%, #1), non-Moon, in time order\n")
    for g in MG:
        x = nm[(nm.side == g) & nm.vt].sort_values(['tm', 'tab'])
        out.append(f"**{NAME[g]}'s side** ({len(x)})")
        for r in x.itertuples(): out.append(f"- {hms(r.tm)} (+{r.tm - O:.0f}′) {NAME[r.tab]} [{r.kind}] {r.d}")
        out.append("")
    # 4. managers
    out.append("## 4. The managers — every tight receiver, non-Moon\n")
    for g in MG:
        x = nm[(nm.tab == g) & nm.tight & nm.top].sort_values('tm')
        out.append(f"**{NAME[g]}** ({len(x)}; natal bodies: {', '.join(f'{k} {v}' for k, v in collections.Counter(x.natal).most_common())})")
        for r in x.itertuples(): out.append(f"- {hms(r.tm)} (+{r.tm - O:.0f}′) [{r.kind}] {r.d}")
        out.append("")
    # 5. per chart
    out.append("## 5. Every chart — tight receivers non-Moon (very tight) · Sun / Mars receivers · Moon receivers\n")
    out.append("| chart | side | receivers (very tight) | natal Sun | natal Mars | Moon |\n|---|---|---|---|---|---|")
    for tb in sorted(NAME):
        x = ev[(ev.tab == tb) & ev.tight & ev.top]; y = x[~x.moon]
        out.append(f"| {NAME[tb]} ({ROLE[tb]}) | {NAME[side[tb]]} | {len(y)} ({y.vt.sum()}) | {(y.natal == 'Sun').sum()} | {(y.natal == 'Mars').sum()} | {x.moon.sum()} |")
    # 6. patterns (as read in the races): a natal body struck in sequence on one string; one triangle holding two of a chart's own bodies;
    #    Rahu and Ketu together on one natal body
    out.append("\n## 6. Patterns (tight receivers, non-Moon)\n")
    rc_ = nm[nm.tight & nm.top].copy()
    rc_['string'] = rc_.d.str.extract(r' on (\S+ [^→]+?) → ')[0]
    seq = []
    for (tb, nb, st), g in rc_.groupby(['tab', 'natal', 'string']):
        if g.sky.nunique() >= 2:
            g = g.sort_values('tm'); seq.append((g.tm.min(), f"{NAME[tb]} ({NAME[side[tb]]}'s side): natal {nb} on {st} struck by " + ' → '.join(f"{r.sky} {hms(r.tm)}" for r in g.itertuples())))
    out.append("**A natal body struck in sequence on one string (two or more sky bodies):**")
    out += [f"- {x}" for _, x in sorted(seq)] or ['- none']
    dbl = []
    for (tb, tm_), g in rc_[rc_.sky == rc_.natal].groupby(['tab', rc_.tm.round(2)]):
        if g.natal.nunique() >= 2: dbl.append(f"{hms(tm_)} {NAME[tb]} ({NAME[side[tb]]}'s side): " + '; '.join(g.d))
    out.append("\n**One triangle holding two of a chart's own bodies, each by its own sky body (double same-body), at the same moment:**")
    out += [f"- {x}" for x in sorted(dbl)] or ['- none']
    nod = []
    for (tb, nb, tm_), g in rc_[rc_.sky.isin(['Rahu', 'Ketu'])].groupby(['tab', 'natal', rc_.tm.round(2)]):
        if set(g.sky) == {'Rahu', 'Ketu'}: nod.append(f"{hms(tm_)} {NAME[tb]} ({NAME[side[tb]]}'s side): Rahu and Ketu → natal {nb} ({g.d.iloc[0]})")
    out.append("\n**Rahu and Ketu together on one natal body:**")
    out += [f"- {x}" for x in sorted(nod)] or ['- none']
    txt = '\n'.join(out) + '\n'
    open(P + 'match-lite.md', 'w', encoding='utf-8').write(txt)
    return txt, sm, ev

if __name__ == '__main__':
    for R in sys.argv[1:]:
        txt, sm, ev = run(R); print(f"{R}: {len(txt.splitlines())} lines -> rr/{R}/compare/match-lite.md")
