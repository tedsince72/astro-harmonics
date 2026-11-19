"""Race level: sky bodies (no stars) on the racecourse in Dec (|latitude − Dec S Y| scored by eddie_bybody.hits), races whose favourite won
vs lost, several cuts (19 Nov 2026, Eddie; read-only, chosen after the results). Usage: python3 tools/scans/bb_scan_course_dec_race.py"""
import sys, os
sys.argv = sys.argv[:1]; sys.path[:0] = ['tools', 'tools/scans']
import openpyxl, eddie_bybody as EB, bb_scan_negatives as NG, bb_favs_outer_uranus as F
def lat_of(p):
    for r in openpyxl.load_workbook(p, read_only=True)['META'].iter_rows(values_only=True):
        if r and r[0] == 'racecourse_lat_lon_elev': return float(str(r[1]).split(',')[0])
rows = []
for race, win in NG.RACES:
    p = f'reference/classic/race_batch_{race}_active.xlsx'
    if not os.path.exists(p) or race not in F.FAV: continue
    lat = lat_of(p); _, _, tp = EB.load(p)
    L = []
    for Y in EB.BODIES:
        if Y in tp:
            d = abs(lat - tp[Y]); h = EB.hits(d, 'Dec')
            if h: L.append((Y, round(d, 4), h[0][1], h[0][0], round(h[0][2], 1)))
    rows.append((race, F.FAV[race] == win, L))
for cut in (90, 80, 70, 50):
    print(f'## cut {cut}')
    for won in (True, False):
        R = [r for r in rows if r[1] == won]
        n = sum(1 for r in R if any(x[4] >= cut for x in r[2]))
        print(f"- favourite {'won' if won else 'lost'}: {len(R)} races, {n} with a sky body on the course >= {cut}, lines {sum(sum(1 for x in r[2] if x[4] >= cut) for r in R)}")
print('\n## favourite won races, every sky body line on the course')
for r in rows:
    if r[1]: print('-', r[0], r[2] or '-')
