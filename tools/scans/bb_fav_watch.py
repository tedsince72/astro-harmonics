"""Favourite watch lines, recorded blind on every race (19 Nov 2026, Eddie; chosen after the results, bb_scan_fav_win.py /
bb_scan_fav_tokens.py; graded on the favourite after the result):
  W1 'keep our eye on this': the runner holds BB12 and is not bottom of its field on rule count (favourites with BB12 8 of 34 won,
     without 0 of 34 before Chelmsford AW 15:30 26 Aug 2021).
  W2 'yes, add that': the runner has a bybody line scoring >= 90 on 100φ (161.8; favourites with 8 of 31 won, without 1 of 38 over 79 races);
     also shown: silver 24.14 / 4.14 >= 90 lines (favourites with 7 of 21, without 2 of 48).
Reads only the race's bybody xlsx and bbrules json (no result). Usage: python3 tools/scans/bb_fav_watch.py <race>"""
import sys, json
RACE = sys.argv[1]
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans']
import eddie_bybody_rules as E

R = E.load(f'docs/eddie_read/bybody/{RACE}/{RACE}_bybody.xlsx')
J = json.load(open(f'docs/eddie_read/bybody_rules/{RACE}_bbrules.json'))
held = {r: set() for r in J['runners']}
for rid, cs in J['rules'].items():
    for c in cs:
        if not c.get('watch_only'):
            held.setdefault(c['runner'], set()).add(rid)
lo = min(len(held.get(r, ())) for r in R)
print(f'# Favourite watch: {RACE} (blind)\n')
print('| runner | rules | BB12 | W1 (BB12, not fewest rules) | W2 100φ >= 90 lines | silver 24.14 / 4.14 >= 90 |\n|---|---|---|---|---|---|')
for run, D in R.items():
    n = len(held.get(run, ())); b = 'BB12' in held.get(run, ())
    phi, sil = [], []
    for X, d in D.items():
        for g in 'LSO':
            for r in d[g]:
                if r.get('sc') is None or r['sc'] < 90:
                    continue
                s = f"{r['line']} {r['plane']} {r['v']:.4f} ({r['sc']:.1f})"
                if r['tgt'] == '100φ' and s not in phi:
                    phi.append(s)
                if r['fam'] == 'silver' and r['tgt'] in ('24.14', '4.14') and s not in sil:
                    sil.append(s)
    print(f"| {run} | {n} | {'yes' if b else '-'} | {'yes' if b and n > lo else '-'} | {len(phi)}: {'; '.join(phi) or '-'} | {len(sil)}: {'; '.join(sil) or '-'} |")
