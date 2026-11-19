"""Was the latitude-only Dec result luck? (19 Nov 2026, Eddie: 'seems funny that it worked at your previous calculation'; read-only).
(a) Race level: a sky body (no stars) on a point at Dec = latitude + k, k from -0.30 to +0.30 deg in 0.01 steps (k = 0: the old scan;
k ~ +0.1: about where the J2000 zenith sits), cut 80, favourite-won vs lost races. (b) Runner level on the J2000 zenith (bb_scan_course_zenith):
natal H / J X -> zenith and a sky line S Y -> zenith on the same family + target, both >= CUT (no conj), RA and Dec; and the same body
(S X and natal X). Usage: python3 tools/scans/bb_scan_zenith_offsets.py [CUT]"""
import sys, os
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 80
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans', 'rebuild_kit']
import bb_scan_course_zenith as Z, eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
D = []
for race, win in NG.RACES:
    p = f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(p) or race not in F.FAV:
        continue
    lat, lon, el, t = Z.meta(p); zz, _ = Z.zenith(lat, lon, el, t)
    runners, tt, tp = EB.load(p); tra = Z.ra_pos(p, 'TRANS_POS')
    D.append((race, win, lat, zz, runners, tp, tra))
print(f'# Was the latitude-only result luck? (cut {CUT:g}; read-only)\n')
print('## (a) offset sweep: a sky body on Dec = latitude + k, races with a line >= cut (favourite won / lost)\n')
print('| k | fav won (10) | fav lost (60) | J2000 zenith - latitude |'); print('|---|---|---|---|')
for i in range(-30, 31, 2):
    k = i / 100; w = l = 0
    for race, win, lat, zz, R, tp, tra in D:
        hit = any((h := EB.hits(abs(lat + k - tp[y]), 'Dec')) and h[0][0] != 'conj' and h[0][2] >= CUT for y in EB.BODIES if y in tp)
        if F.FAV[race] == win: w += hit
        else: l += hit
    print(f'| {k:+.2f} | {w} | {l} | |')
print('\nJ2000 zenith minus latitude (Dec), per race: min %.3f, max %.3f' % (min(d[3][1] - d[2] for d in D), max(d[3][1] - d[2] for d in D)))
print(f'\n## (b) runner level on the J2000 zenith: natal X and a sky line on the same number, both >= {CUT:g}\n')
G = {}
for race, win, lat, zz, R, tp, tra in D:
    sky = Z.lines(tp, tra, zz, EB.BODIES)
    for c, r in R.items():
        nm = r['name'].get('H', ''); k = ('WF' if F.FAV[race] in nm and win in nm else 'LF' if F.FAV[race] in nm else 'OW' if win in nm else 'OL')
        link = same = 0
        for ch in ('H', 'J'):
            for x in Z.lines(r['pos'].get(ch, {}), r.get('ra', {}).get(ch, {}), zz, EB.NATAL_BODIES):
                if x[4] == 'conj' or x[5] < CUT: continue
                for y in sky:
                    if y[4] != 'conj' and y[5] >= CUT and y[1] == x[1] and (y[3], y[4]) == (x[3], x[4]):
                        link = 1; same |= (y[0] == x[0])
        G.setdefault(k, []).append((link, same))
lab = {'WF': 'winning favourites', 'LF': 'losing favourites', 'OW': 'other winners', 'OL': 'other losers'}
print('| group | runners | with a link | with a same-body link |'); print('|---|---|---|---|')
for k in ('WF', 'LF', 'OW', 'OL'):
    L = G.get(k, []); print(f'| {lab[k]} | {len(L)} | {sum(a for a, b in L)} | {sum(b for a, b in L)} |')
