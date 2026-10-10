#!/usr/bin/env python3
"""match_goals.py EVENTS_CSV MATCH [MATCH ...] - after the result (football lite, 11 Oct 2026): each goal / red card at its real clock time
(the events file's wallclock_utc + 1 h, UK summer time - no half-time conversion needed), set against the match's lite events
(tools/match_lite.py definitions). It lays out; it does not judge.
For each event: the scorer's chart (if he is one of the 12 charts of his side) - every TIGHT event of his within +-3 min (Moon too; same body and numbers count as tight);
his manager's within +-3 min; tight non-Moon receivers per side within +-3 min; any natal Sun / Mars receiver of either side within +-5 min."""
import sys, os, re, csv, unicodedata
from datetime import datetime, timedelta
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match_lite as ML
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(s): return unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower().strip()
TEAMS = {'arsenal': 'arsenal', 'leeds united': 'leeds_united', 'aston villa': 'aston_villa', 'brentford': 'brentford', 'chelsea': 'chelsea',
         'afc bournemouth': 'bournemouth', 'bournemouth': 'bournemouth', 'ipswich town': 'ipswich_town', 'fulham': 'fulham', 'sunderland': 'sunderland',
         'brighton & hove albion': 'brighton', 'manchester united': 'manchester_united', 'tottenham hotspur': 'tottenham',
         'hull city': 'hull_city', 'everton': 'everton', 'crystal palace': 'crystal_palace', 'nottingham forest': 'nottingham_forest',
         'liverpool': 'liverpool', 'manchester city': 'manchester_city', 'coventry city': 'coventry', 'newcastle united': 'newcastle_united'}

def run(evf, R):
    P = f'{REPO}/rr/{R}/compare/'
    t = pd.read_csv(P + 'table.csv', low_memory=False); t.columns = [c.replace('%', '_') for c in t.columns]
    L = open(P + 'reading-pack.md', encoding='utf-8').read()
    off, fin = re.search(r'Off (\d+:\d+:\d+), finish (\d+:\d+:\d+)', L).groups(); O, F = ML.clk(off), ML.clk(fin)
    meta = list(csv.reader(open((f'{REPO}/data/allpos/{R}__META.csv' if os.path.exists(f'{REPO}/data/allpos/{R}__META.csv') else f'{REPO}/ledger/allpos/{R}__META.csv'), encoding='utf-8')))
    hdr = next(i for i, r in enumerate(meta) if r[:3] == ['tab', 'role', 'cloth'])
    tabs = [dict(zip(meta[hdr], r)) for r in meta[hdr + 1:] if r and r[0].startswith('P')]
    NAME = {x['tab']: x['name'].split(' ', 1)[1] for x in tabs}; TEAM = {x['tab']: x['team'] for x in tabs}
    MGR = {x['team']: x['tab'] for x in tabs if x['role'] == 'manager'}
    ev = ML.events(t, O, F)
    ev['team'] = ev.tab.map(TEAM)
    home, away = TEAM['P01'], [x['team'] for x in tabs if x['role'] == 'manager'][1]
    E = [r for r in csv.DictReader(open(evf, encoding='utf-8')) if TEAMS.get(norm(r['home'])) == home and TEAMS.get(norm(r['away'])) == away]
    out = [f"\n## {R}: {NAME['P01']}'s {home} v {NAME[MGR[away]]}'s {away} — kick-off {off}"]
    hg = sum(1 for r in E if r['event_type'] == 'GOAL' and TEAMS.get(norm(r['team'])) == home)
    ag = sum(1 for r in E if r['event_type'] == 'GOAL' and TEAMS.get(norm(r['team'])) == away)
    out.append(f"Result: {home} {hg}–{ag} {away}  ({len(E)} events)\n")
    for r in E:
        wc = datetime.strptime(r['wallclock_utc'], '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=1)
        tm = wc.hour * 60 + wc.minute + wc.second / 60; team = TEAMS.get(norm(r['team']))
        who = [tb for tb, n in NAME.items() if norm(n) == norm(r['player'])]
        out.append(f"### {r['event_type']} {r['match_min']} {r['player']} ({team}) — {wc:%H:%M:%S} UK (KO+{tm - O:.1f} min)"
                   + ('' if who else '  [not one of the 12 charts]'))
        for tb in who:
            x = ev[(ev.tab == tb) & ((ev.tm - tm).abs() <= 3) & ev.tight].sort_values('tm')
            out.append(f"- {NAME[tb]} ±3 min: " + ('none' if not len(x) else ''))
            for e in x.itertuples(): out.append(f"  - {ML.hms(e.tm)} ({e.tm - tm:+.1f}′) [{e.kind}] {e.d}{' TIGHT' if e.tight else ''}{' MOON' if e.moon else ''}")
        g = MGR.get(team)
        if g:
            x = ev[(ev.tab == g) & ((ev.tm - tm).abs() <= 3) & ev.tight].sort_values('tm')
            out.append(f"- manager {NAME[g]} ±3 min: " + ('none' if not len(x) else ''))
            for e in x.itertuples(): out.append(f"  - {ML.hms(e.tm)} ({e.tm - tm:+.1f}′) [{e.kind}] {e.d}{' TIGHT' if e.tight else ''}{' MOON' if e.moon else ''}")
        rc = ev[((ev.tm - tm).abs() <= 3) & ev.tight & ev.top & ~ev.moon]
        out.append(f"- tight receivers ±3 min (non-Moon): {home} {(rc.team == home).sum()} ({(rc.vt & (rc.team == home)).sum()} very tight) · "
                   f"{away} {(rc.team == away).sum()} ({(rc.vt & (rc.team == away)).sum()} very tight)")
        sm = ev[((ev.tm - tm).abs() <= 5) & ev.tight & ev.top & ~ev.moon & ev.natal.isin(['Sun', 'Mars']) & ev.kind.str.startswith('M')]
        for e in sm.sort_values('tm').itertuples():
            out.append(f"- Sun/Mars ±5: {ML.hms(e.tm)} ({e.tm - tm:+.1f}′) {NAME[e.tab]} ({TEAM[e.tab]}) [{e.kind}] {e.d}")
        out.append("")
    return '\n'.join(out)

if __name__ == '__main__':
    evf = sys.argv[1]; txt = '\n'.join(run(evf, R) for R in sys.argv[2:])
    print(txt)
