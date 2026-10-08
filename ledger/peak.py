"""peak.py v1.1 (3 Oct 2026) - sky->natal contacts and WHEN they peak around the off, minute by minute.
v1.1 (Eddie 12:54-12:56): no minimum drop - a peak is simply higher than the minute before and the minute after;
applying at the off and peaking shortly after counts (the race is still being run: ~1 min on the flat, up to
~12 min over jumps); record what we see.
Sky positions every minute from the off to +15 (plus -30..-1 and +20, +30) from sky_minutes.py (SKYM).
Contact: sky body (not a star or a fast point) -> certain natal body (not a star, not Sun/Moon/Mercury/Venus/Mars),
RA or Dec, family = best at the off; listed when its best score between -2 and +15 min is >= 90.
Labels:  OFF      peak at the off (minute 0 higher than -1 and +1)
         +k       applying at the off, peaks k minutes after (1..15)
         >15      still applying at +15 (peaks later)
         -k       peaked k minutes before the off (1..2), separating at the off
◆ = already >= 90 at the off (strong at the off as well as peaking in the race window).
Shown: the minute of the peak and scores at -30 / -2 / off / +2 / peak / +30. * = body of a top-12 sky pair.
Usage: python3 peak.py RACE [--all]   (default: OFF and +k only; --all adds >15 and -k)"""
import sys, csv; sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, FAST, FASTNATAL, results, SKYD
R = sys.argv[1]; ALL = '--all' in sys.argv
rc = Race(R); rc.build(); res = results(R)
M = {}
for r in csv.DictReader(open(f'{SKYD}/{R}__SKYM.csv')):
    M.setdefault(r['body'], {})[int(r['minute'])] = (float(r['ra']), float(r['dec']))
MIN = sorted(next(iter(M.values())))
order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
topb = {b for k in rc.byrank[:12] for b in k}
print('PEAKING AROUND THE OFF –', R, '(minute by minute; peak = higher than the minute either side)')
for c in order:
    rows = []
    for sd, tab in rc.charts[c].items():
        P = rc.natal[tab]
        for s in rc.sky:
            if s in FAST or s in STARS or s == 'equator' or s not in M: continue
            for n in P:
                if n in STARS or n in FASTNATAL: continue
                for m in ('RA', 'Dec'):
                    v0 = sep(M[s][0], P[n], m)
                    f = max(FAMS, key=lambda k: FN[k](v0, m))
                    sc = {t: FN[f](sep(M[s][t], P[n], m), m) for t in MIN}
                    win = [t for t in MIN if -2 <= t <= 15]
                    if max(sc[t] for t in win) < 90: continue
                    # local maxima on the one-minute grid -2..15
                    grid = list(range(-2, 16))
                    peaks = [t for t in grid if t - 1 in sc and t + 1 in sc and sc[t] > sc[t - 1] and sc[t] > sc[t + 1]]
                    if 0 in peaks: lab, p = 'OFF', 0
                    elif sc[1] > sc[0] > sc[-1] or (sc[1] > sc[0] and sc[0] >= sc[-1]):
                        aft = [t for t in peaks if t > 0]
                        if aft: p = aft[0]; lab = f'+{p}'
                        else: p = 15; lab = '>15'
                    elif sc[0] < sc[-1]:
                        bef = [t for t in peaks if t < 0]
                        if not bef: continue
                        p = bef[-1]; lab = f'{p}'
                    else: continue
                    if sc[p] < 90: continue
                    if lab in ('>15',) or lab.startswith('-'):
                        if not ALL: continue
                    rows.append((lab, sd, s, n, m, v0, f, sc, p))
    key = lambda r: (0 if r[0] == 'OFF' else 1 if r[0].startswith('+') else 2 if r[0] == '>15' else 3, int(r[0][1:]) if r[0][0] in '+-' else 0)
    rows.sort(key=key)
    print(f"\n  {res[c]['finish']:>3} {rc.names[c][0]:18} {res[c]['sp']:>5}  at the off {sum(r[0]=='OFF' for r in rows)}, peaking +1..+15 {sum(r[0].startswith('+') for r in rows)} (◆ {sum(r[7][0] >= 90 for r in rows)})"
          + (f", >15 {sum(r[0]=='>15' for r in rows)}, before {sum(r[0].startswith('-') for r in rows)}" if ALL else ''))
    for lab, sd, s, n, m, v0, f, sc, p in rows:
        print(f"    {'◆' if sc[0] >= 90 else ' '} {lab:>4}  {sd} {s}{'*' if s in topb else ''}→{n}{'B' if n in rc.busy else ''} {m} {v0:.4f} {f[:6]:6}  "
              f"{sc[-30]:.1f} / {sc[-2]:.1f} / off {sc[0]:.1f} / {sc[2]:.1f} / peak {sc[p]:.1f} / {sc[30]:.1f}")
