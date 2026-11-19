"""Natal / activation features per runner, and as a filter on the cover-of-eight picks (19 Nov 2026, Eddie: 'what did the 2 runners
today have in common with their natal charts and the sky / activations ... maybe this is a filter that we can also use with cover of
eight'; read-only).
Features (both charts summed): nat90, tight, anysky, share1 (bb_scan_natal_angle); act80 / act90 = natal pairs >= 90 activated by a
sky line >= 80 / >= 90 naming one of their bodies (bb_scan_activation, no Moon); both = pairs >= 90 in both charts; co = Chiron – Orcus
>= 90 in either chart; T2 / T3 (bb_scan_echo_threads, tight echoes).
Output: the two 16 Nov 2026 races (each runner); then over every result race the cover picks split by each feature (picks / won /
chance / level-stake profit at SP), and the winner's place in the field on each count (top / bottom, ties shared).
Usage: python3 tools/scans/bb_natal_filter.py [--races-only]"""
import sys, os
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as NG, bb_fresh_sheet as F, bb_fresh_sheet_profit as SP, bb_cover8 as C8
import bb_scan_natal_angle as NA, bb_scan_activation as AC, bb_scan_echo_threads as ET
from bb_scan_natal_pairs import nums

FEATS = ['nat90', 'tight', 'anysky', 'share1', 'act80', 'act90', 'both', 'co', 'T2', 'T3']


def acts(rc, cut):
    AC.hits = lambda v, pl, c=cut: [(f, t, s) for f, t, s in nums(v, pl) if s >= c]
    out = {}
    for name, h, show, rep, both in AC.race(rc) or []:
        # show lists every activated pair (Moon allowed); count those with a non-Moon line
        n = sum(1 for s in show if any('Moon' not in part for part in s.split(' <- ')[1].split('; ')))
        out[name] = (n, len(both), any('Chiron – Orcus' in s or 'Orcus – Chiron' in s for s in show))
    return out


def features(rc):
    na = NA.race(rc)
    if not na:
        return None
    a80, a90 = acts(rc, 80), acts(rc, 90)
    et = {n: h for n, h, b, T in ET.race(rc)}
    co = co_holders(rc)
    out = {}
    for name, t, s in na:
        out[name] = {'nat90': t['nat90'], 'tight': t['tight'], 'anysky': t['anysky'], 'share1': t['share1'],
                     'act80': a80[name][0], 'act90': a90[name][0], 'both': a90[name][1], 'co': int(name in co),
                     'T2': int(et[name]['T2']), 'T3': int(et[name]['T3'])}
    return out


def co_holders(rc):
    import eddie_bybody as B
    from bb_scan_natal_pairs import P
    from bb_scan_uranus_pairs import dist
    runners, tt, tp = B.load(f'reference/classic/race_batch_{rc}_active.xlsx'); s = set()
    for r in runners.values():
        for c in 'HJ':
            if not r['pos'].get(c): continue
            for pl in ('RA', 'Dec'):
                a, b = P(r['pos'][c], r['ra'][c], 'Chiron', pl), P(r['pos'][c], r['ra'][c], 'Orcus', pl)
                if a is None or b is None: continue
                h = nums(dist(a, b, pl), pl)
                if h and h[0][2] >= 90: s.add(r['name'].get('H'))
    return s


def key(n):
    return n.split(' ', 1)[1] if n and n.split(' ', 1)[0].isdigit() else n


def main():
    for rc, win in (('20261116_wolverhampton_aw_1800', 'Splintered'), ('20261116_plumpton_1445', 'Of Corse I Can')):
        f = features(rc)
        print(f'## {rc} (winner {win})\n\n| runner | ' + ' | '.join(FEATS) + ' |\n|---|' + '---|' * len(FEATS))
        for n, v in f.items():
            print(f"| {'*' if win in n else ''}{n} | " + ' | '.join(str(v[k]) for k in FEATS) + ' |')
        print()
    if '--races-only' in ARGS:
        return
    rows = []  # (race, name, field, feats, is_pick, won, dec)
    place = {k: [0.0, 0.0, 0.0] for k in FEATS}; nr = 0
    for rc, win in NG.RACES:
        f = features(rc)
        if not f:
            continue
        try:
            runners, hh = F.holders(rc)
        except Exception:
            hh = {}
        picks = {key(r) for r, s in hh.items() if any(set(c) <= s for c in C8.C)}
        dec = SP.sp(rc, win)[0]; n = len(f); nr += 1
        for name, v in f.items():
            rows.append((rc, name, n, v, key(name) in picks, win in name, dec))
        for k in FEATS:
            vals = [v[k] for v in f.values()]; w = next(v[k] for nm, v in f.items() if win in nm)
            hi, lo = max(vals), min(vals)
            if hi > lo:
                place[k][0] += (w == hi) / vals.count(hi); place[k][1] += (w == lo) / vals.count(lo); place[k][2] += 1 / n
    print(f'## Winner\'s place in the field ({nr} races; ties shared)\n\n| feature | top | bottom | chance each |\n|---|---|---|---|')
    for k in FEATS:
        print(f'| {k} | {place[k][0]:.1f} | {place[k][1]:.1f} | {place[k][2]:.1f} |')
    pk = [r for r in rows if r[4]]
    def agg(sel):
        p = len(sel); w = sum(x[5] for x in sel); c = sum(1 / x[2] for x in sel); pr = sum(x[6] if x[5] else -1 for x in sel)
        return f'{p} / {w} / {c:.1f} | {pr:+.1f}' if p else '0 |'
    print(f'\n## Cover-of-eight picks split by feature (all picks: {agg(pk)})\n\n| feature | value | picks / won / chance | profit |\n|---|---|---|---|')
    for k in FEATS:
        for lab, fn in (('0', lambda x: x == 0), ('>= 1', lambda x: x >= 1), ('>= 2', lambda x: x >= 2)):
            sel = [r for r in pk if fn(r[3][k])]
            print(f'| {k} | {lab} | {agg(sel)} |')


if __name__ == '__main__':
    main()
