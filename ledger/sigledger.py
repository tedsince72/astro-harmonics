#!/usr/bin/env python3
"""sigledger.py v1.0 (3 Oct 2026) - SIGNATURE LEDGER (Eddie 18:00-18:02: every pair has its own nature, and the
family colours it - "Juno-Eris in Golden Ratio is of a different nature to Juno-Eris in Whole Number").
A signature = sky body -> natal body + family (+ coordinate, chart H/J), at the race time.
For every race and every runner: every sky -> natal contact (sky body not a star / fast point; natal body certain over
the birth day - not a star, not Sun/Moon/Mercury/Venus/Mars) whose best score between -2 and +15 min is >= 95,
with its value at the off, score at the off, peak and minute (from SKYM; family = best at the off).
Then, ACROSS races: every signature (sky X -> natal Y, family) that a WINNER has in 2+ races, with EVERY occurrence
in the 13 races - winners and beaten runners - listed one by one (no totals used as evidence).
Outputs: reads_out/siglist.txt (per race, per runner) and reads_out/sigcross.txt (cross-race).
Usage: python3 sigledger.py RACE ..."""
import sys, csv, collections
sys.path.insert(0, '/home/claude/ledger')
from readrace import Race, sep, FN, FAMS, STARS, FAST, FASTNATAL, results, SKYD
races = sys.argv[1:]
occ = collections.defaultdict(list)      # (s, n, fam) -> [(race, runner, finish, sp, chart, coord, value, off, peak, minute)]
win_sig = collections.defaultdict(set)   # sig -> set(races where the winner has it)
L = open('/home/claude/ledger/reads_out/siglist.txt', 'w')
for R in races:
    rc = Race(R); res = results(R)
    M = {}
    for r in csv.DictReader(open(f'{SKYD}/{R}__SKYM.csv')):
        M.setdefault(r['body'], {})[int(r['minute'])] = (float(r['ra']), float(r['dec']))
    order = sorted(rc.charts, key=lambda c: int(res[c]['finish']) if res[c]['finish'].isdigit() else 99)
    print(f"\n######## {R}", file=L)
    for c in order:
        fin, sp, name = res[c]['finish'], res[c]['sp'], rc.names[c][0]
        rows = []
        for sd, tab in rc.charts[c].items():
            P = rc.natal[tab]
            for s in M:
                if s in STARS or s in FAST or s == 'equator': continue
                for n in P:
                    if n in STARS or n in FASTNATAL: continue
                    for m in ('RA', 'Dec'):
                        v0 = sep(M[s][0], P[n], m)
                        f = max(FAMS, key=lambda k: FN[k](v0, m))
                        sc = {t: FN[f](sep(M[s][t], P[n], m), m) for t in M[s]}
                        pk = max(range(-2, 16), key=lambda t: sc[t])
                        if sc[pk] < 95: continue
                        rows.append((s, n, f, sd, m, v0, sc[0], sc[pk], pk))
        rows.sort(key=lambda r: (r[8], -r[7]))
        print(f"\n  {fin:>3} {name:20} {sp:>6}  {len(rows)} contacts >= 95 in the window", file=L)
        for s, n, f, sd, m, v0, s0, spk, pk in rows:
            print(f"      {sd} {s:10}→ {n:10} {f:13} {m:3} {v0:9.4f}  off {s0:5.1f}  peak {spk:5.1f} @{pk:+d}", file=L)
            key = (s, n, f)
            occ[key].append((R, name, fin, sp, sd, m, v0, s0, spk, pk))
            if fin == '1': win_sig[key].add(R)
L.close()
C = open('/home/claude/ledger/reads_out/sigcross.txt', 'w')
print("SIGNATURES (sky X -> natal Y, family) that a WINNER has in 2+ races – every occurrence in the races read\n", file=C)
keys = sorted([k for k in win_sig if len(win_sig[k]) >= 2], key=lambda k: (-len(win_sig[k]), k))
for k in keys:
    o = occ[k]
    beaten = sorted({(x[0], x[1]) for x in o if x[2] != '1'})
    print(f"== {k[0]} → natal {k[1]}  [{k[2]}]   winners in {len(win_sig[k])} races; beaten runners with it: {len(beaten)}", file=C)
    for R, name, fin, sp, sd, m, v0, s0, spk, pk in sorted(o, key=lambda x: (x[0], x[2] != '1', x[2])):
        print(f"     {R:28} {fin:>3} {name:20} {sp:>6} {sd} {m:3} {v0:9.4f} off {s0:5.1f} peak {spk:5.1f} @{pk:+d}" + ('   <- WINNER' if fin == '1' else ''), file=C)
    print(file=C)
C.close()
print('signatures with a winner in 2+ races:', len(keys))
