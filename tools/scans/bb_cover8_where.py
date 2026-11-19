"""Where the cover of eight works and where it misses (19 Nov 2026, Eddie: 'which races the cover of 8 works in and what is going on
when it misses'; read-only). Every result race in bb_scan_negatives.RACES (in-sample 57 + forward). Holders from /tmp/fresh (today's
rules) with docs/eddie_read/bybody_rules as fallback. Per race: field size, picks, hit / miss with picks / no pick, the winner's SP,
the winner's rule count and its rank in the race (1 = most rules), rules the winner holds alone, the winner's depth step and the race's
top step, whether the favourite (bb_favs_outer_uranus.FAV) was a pick. Then the three groups side by side.
Usage: python3 tools/scans/bb_cover8_where.py [--list]"""
import sys, os, json
LIST = '--list' in sys.argv
sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as NG, bb_fresh_sheet as F, bb_fresh_sheet_profit as SP, bb_favs_outer_uranus as FV
from bb_cover8 import C

FORWARD = ['20261116_wolverhampton_aw_1800', '20261116_plumpton_1445', '20261114_uttoxeter_1242', '20261108_ffos_las_1537',
           '20261104_chepstow_1505']


def holders(race):
    F.D = '/tmp/fresh' if os.path.exists(f'/tmp/fresh/{race}_bbrules.json') else 'docs/eddie_read/bybody_rules'
    return F.holders(race)


def depth(race):
    p = f'docs/eddie_read/depth/{race}_depth.json'
    if not os.path.exists(p):
        return {}, None
    d = json.load(open(p))
    return {r['runner']: r['top'] for r in d['runners']}, d['race_top']


def main():
    rows = []
    for race, win in NG.RACES:
        runners, hh = holders(race)
        w = next(r for r in runners if win in r)
        N = len(runners)
        picks = [r for r in runners if any(set(c) <= hh.get(r, set()) for c in C)]
        cnt = {r: len(hh.get(r, ())) for r in runners}
        rank = 1 + sum(1 for r in runners if cnt[r] > cnt[w])
        alone = sum(1 for rid in hh.get(w, ()) if sum(rid in hh.get(r, ()) for r in runners) == 1)
        dp, top = depth(race)
        try:
            dec, sp = SP.sp(race, win)
        except Exception:
            dec, sp = None, '?'
        fav = FV.FAV.get(race)
        favpick = None if not fav else any(fav in r for r in picks)
        kind = 'hit' if w in picks else ('miss' if picks else 'none')
        rows.append(dict(race=race, w=w, N=N, picks=len(picks), kind=kind, sp=sp, dec=dec, cnt=cnt[w], rank=rank, alone=alone,
                         wd=dp.get(w), top=top, fav=fav, favpick=favpick, fwd=race in FORWARD,
                         pick_names=[p.split(' ', 1)[-1] for p in picks]))
    print(f'# Cover of eight: where it works ({len(rows)} result races; forward races marked *)\n')
    groups = [('hit', 'winner was a pick'), ('miss', 'picks, winner not among them'), ('none', 'no pick')]
    print('| group | races | field size (mean) | picks per race | winner SP (median) | winner rules rank 1 | winner rank (mean) | '
          'winner rules held alone (mean) | winner at the race top depth | favourite was a pick |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for g, txt in groups:
        R = [r for r in rows if r['kind'] == g]
        if not R:
            continue
        m = lambda k: sum(r[k] for r in R) / len(R)
        decs = sorted(r['dec'] for r in R if r['dec'] is not None)
        med = decs[len(decs) // 2] if decs else 0
        top = sum(1 for r in R if r['wd'] is not None and r['wd'] == r['top']); topn = sum(1 for r in R if r['wd'] is not None)
        fp = [r['favpick'] for r in R if r['favpick'] is not None]
        print(f"| {txt} | {len(R)} | {m('N'):.1f} | {m('picks'):.1f} | {med:.0f}/1 | {sum(r['rank'] == 1 for r in R)} | "
              f"{m('rank'):.1f} | {m('alone'):.1f} | {top} of {topn} | {sum(fp)} of {len(fp)} |")
    print('\n## By field size\n\n| runners | races | hit | miss with picks | no pick |\n|---|---|---|---|---|')
    for lo, hi in ((3, 5), (6, 6), (7, 8), (9, 30)):
        R = [r for r in rows if lo <= r['N'] <= hi]
        print(f"| {lo}-{hi} | {len(R)} | {sum(r['kind'] == 'hit' for r in R)} | {sum(r['kind'] == 'miss' for r in R)} | "
              f"{sum(r['kind'] == 'none' for r in R)} |")
    print('\n## By number of picks\n\n| picks | races | hit | chance of a hit (sum of picks / field) |\n|---|---|---|---|')
    for k in sorted({r['picks'] for r in rows}):
        R = [r for r in rows if r['picks'] == k]
        print(f"| {k} | {len(R)} | {sum(r['kind'] == 'hit' for r in R)} | {sum(k / r['N'] for r in R):.1f} |")
    if LIST:
        print('\n## Every race\n\n| race | N | picks | result | winner (SP) | winner rules (rank) | alone | depth / top | picks |')
        print('|---|---|---|---|---|---|---|---|---|')
        for r in rows:
            print(f"| {r['race']}{' *' if r['fwd'] else ''} | {r['N']} | {r['picks']} | {r['kind']} | {r['w'].split(' ', 1)[-1]} ({r['sp']}) | "
                  f"{r['cnt']} ({r['rank']}) | {r['alone']} | {r['wd']} / {r['top']} | {', '.join(r['pick_names'])} |")


if __name__ == '__main__':
    main()
