"""Dec distances to the racecourse (19 Nov 2026, Eddie: 'does the sky have distances to the racecourse in DEC??? that help with favs
and non favs'; read-only, chosen after the results). The racecourse latitude (META racecourse_lat_lon_elev) is the Dec of the course's
zenith. Lines, Dec only, d = |latitude − Dec point|, scored by eddie_bybody.hits (bybody linear scoring; conj = d < 0.3, the point at
the course zenith):
  sky    S Y → course, Y every sky body (Moon incl.) and the 4 royal stars (race level, the same for every runner)
  natal  H X → course, J X → course, X every natal body (no Moon) and the 4 royal stars (the chart's own positions)
  link   a sky line and a natal line on the same family + target (conj not matched), both >= CUT_LINK
  same   S X → course and N X → course on the same family + target (same body X), both >= CUT_LINK
Groups: winning favourites, losing favourites, other winners, other losers (favourites from bb_favs_outer_uranus.FAV, winners from
bb_scan_negatives.RACES, every race with an _active.xlsx). Usage: python3 tools/scans/bb_scan_course_dec.py [CUT] [CUT_LINK]"""
import sys, os
CUT = float(sys.argv[1]) if len(sys.argv) > 1 else 90
CUT_LINK = float(sys.argv[2]) if len(sys.argv) > 2 else 80
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans']
import openpyxl
import eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
ROYAL = ['Aldebaran', 'Regulus', 'Antares', 'Fomalhaut']


def lat_of(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    for r in wb['META'].iter_rows(values_only=True):
        if r and r[0] == 'racecourse_lat_lon_elev':
            return float(str(r[1]).split(',')[0])


def lines(pos, lat, pts):
    out = {}
    for p in pts:
        if p in pos:
            d = abs(lat - pos[p]); h = EB.hits(d, 'Dec')
            out[p] = (d, h[0] if h else None)
    return out


G = {'WF': [], 'LF': [], 'OW': [], 'OL': []}
RACE = {'fav won': [], 'fav lost': []}
for race, win in NG.RACES:
    p = f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(p):
        continue
    lat = lat_of(p); runners, tt, tp = EB.load(p)
    sky = lines(tp, lat, EB.BODIES + ROYAL)
    favn = F.FAV.get(race)
    favwon = favn is not None and favn == win
    if favn:
        RACE['fav won' if favwon else 'fav lost'].append((race, sky))
    for cloth, r in runners.items():
        nm = r['name'].get('H', '')
        isw = win in nm; isf = favn is not None and favn in nm
        rec = {'race': race, 'name': nm, 'n': {}, 'body': set(), 'link': [], 'same': []}
        for ch in ('H', 'J'):
            nl = lines(r['pos'].get(ch, {}), lat, EB.NATAL_BODIES + ROYAL)
            for X, (d, h) in nl.items():
                if h and h[2] >= CUT:
                    rec['n'][f'{ch} {X}'] = (d, h); rec['body'].add(X)
                if not h or h[0] == 'conj' or h[2] < CUT_LINK:
                    continue
                for Y, (sd, sh) in sky.items():
                    if sh and sh[0] != 'conj' and sh[2] >= CUT_LINK and (sh[0], sh[1]) == (h[0], h[1]):
                        rec['link'].append(f'S {Y} {sd:.4f} / {ch} {X} {d:.4f} {h[1]} {h[0]} ({sh[2]:.1f} / {h[2]:.1f})')
                        if Y == X:
                            rec['same'].append(rec['link'][-1])
        G['WF' if isf and isw else 'LF' if isf else 'OW' if isw else 'OL'].append(rec)

lab = {'WF': 'winning favourites', 'LF': 'losing favourites', 'OW': 'other winners', 'OL': 'other losers'}
print(f'# Dec distances to the racecourse (natal >= {CUT:g}; link / same >= {CUT_LINK:g}; read-only, chosen after the results)\n')
print('| group | runners | natal course lines >= cut (mean) | with any | with a link | with a same-body link |')
print('|---|---|---|---|---|---|')
for k, L in G.items():
    n = len(L) or 1
    print(f"| {lab[k]} | {len(L)} | {sum(len(x['n']) for x in L) / n:.2f} | {sum(1 for x in L if x['n'])} | "
          f"{sum(1 for x in L if x['link'])} | {sum(1 for x in L if x['same'])} |")
print('\n## Natal body on the course >= cut, share of runners per group (bodies held by >= 3 winners or favourites)\n')
print('| body | WF | LF | OW | OL |')
print('|---|---|---|---|---|')
bodies = sorted({b for k in G for x in G[k] for b in x['body']})
for b in bodies:
    c = {k: sum(1 for x in G[k] if b in x['body']) for k in G}
    if c['WF'] + c['LF'] + c['OW'] >= 3:
        print(f"| {b} | {c['WF']} / {len(G['WF'])} | {c['LF']} / {len(G['LF'])} | {c['OW']} / {len(G['OW'])} | {c['OL']} / {len(G['OL'])} |")
print('\n## Sky on the course (race level), >= cut: races whose favourite won vs lost\n')
for k, L in RACE.items():
    cnt = {}
    for race, sky in L:
        for Y, (d, h) in sky.items():
            if h and h[2] >= CUT:
                cnt[Y] = cnt.get(Y, 0) + 1
    print(f"- {k} ({len(L)} races): " + ', '.join(f'{y} {n}' for y, n in sorted(cnt.items(), key=lambda x: -x[1])))
print('\n## Winning favourites, each line\n')
for x in G['WF']:
    print(f"- {x['race']} {x['name']}: natal " + ('; '.join(f"{k} {d:.4f} {h[1]} {h[0]} ({h[2]:.1f})" for k, (d, h) in x['n'].items()) or '-')
          + ' | links: ' + ('; '.join(x['link']) or '-'))
