#!/usr/bin/env python3
"""Checks for tools/eddie_basic.py (Eddie, 8 Nov 2026). Known cases from the Newcastle AW 16:33 2 Aug 2021 read, every value
checked by an independent checker from the P##_DIST tabs; then the cell set recomputed with its own reader (no shared code but
families.py) on every _active.xlsx in reference/classic."""
import glob, os, sys
import openpyxl
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import eddie_basic as EB  # noqa: E402
import families as F  # noqa: E402

ok = bad = 0
def check(cond, what):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        print('FAIL', what)

NEW = os.path.join(ROOT, 'reference/classic/race_batch_20210802_newcastle_aw_1633_active.xlsx')
data, per = EB.run(NEW)
ath = {(it['check'], it['note'] + ' ' + ' | '.join(it['cells'])): it for it in per[2]}
def has(chk, *parts, field=None):
    for (c, t), it in ath.items():
        if c == chk and all(p in t for p in parts):
            return field is None or it['field'] == field
    return False
check(has(1, 'H Jupiter – H Rahu RA 0.2100 conj', 'J Jupiter – J Rahu RA 0.9090 conj', field='only'), 'T1 Jupiter-Rahu both charts')
c1 = sorted(c for c in per for it in per[c] if it['check'] == 1)
check(c1 == [2, 3], f'T1 Athmad and Raise The Roof (Mars - Vesta conj, RA | Dec) only: {c1}')
check(has('2a', 'S Jupiter → H Saturn Dec 8.0020 8 whole (80.83)', 'S Jupiter → J Saturn RA 8.0193 8 whole (0.11)', field='only'), '2a Saturn 8')
check(has('2a', 'S Jupiter → H Gonggong Dec 0.0512', 'S Jupiter → J Gonggong RA 1.4607', field='also: 1 Dubai Souq'), '2a Gonggong')
check(has(3, 'S Neptune → H Jupiter RA 179.4564 10×φ^6', 'S Neptune → J Jupiter Dec 11.3247 7×φ', field='only'), '3 Neptune')
check(any(it['check'] == 3 and 'S Pallas → H Jupiter RA 122.9565' in ' '.join(it['cells']) for it in per[6]), '3 Tricolore Pallas')
check(sum(1 for c in per for it in per[c] if it['check'] == 3) == 2, '3 two runners only')
check(has(4, 'S Neptune → J Makemake RA 179.4320 10×φ^6', field='only'), '4 Neptune 10phi^6')
check(any(it['check'] == 4 and 'S Quaoar → J Jupiter RA 111.1493' in ' '.join(it['cells']) for it in per[1]), '4 Dubai Souq Quaoar')
check(has(5, 'S Ceres → H Makemake Dec 11.3245 7×φ', 'S Neptune → J Makemake', field='only'), '5 swap Jupiter / Makemake')
check(has(6, 'S Moon → J Pallas RA 0.2075 conj', 'J Jupiter – J Pallas RA 161.8502', field='only'), '6 Moon on J Pallas')
n7 = {c: next(it for it in per[c] if it['check'] == 7)['key'][1] for c in per}
check(n7 == {1: 2, 2: 6, 3: 3, 4: 3, 5: 4, 6: 3}, f'7 counts {n7}')
check(has(8, 'S Neptune → H Ketu RA 0.7536 conj'), '8 Neptune on H Ketu')
check(has(8, 'S Pallas → H Jupiter RA 179.9597 (no family)'), '8 Pallas opposite H Jupiter, unscored')
check(has(8, 'S Uranus → J Jupiter RA 179.7674 (no family)'), '8 Uranus opposite J Jupiter, unscored')
check(has(9, 'J Jupiter – J Vesta RA 125.9982 126'), '9 J Jupiter - Vesta')
check(has(10, 'J Jupiter – J Eris Dec 6.9987 7', 'S Neptune → J Jupiter Dec 11.3247 7×φ'), '10 7 and 7xphi')
check(has(11, 'H Mars – H Gonggong RA 110.9048', 'S Transpluto → J Ketu RA 111.1705'), '11 110.9-111.17')
check(has(12, 'H Jupiter – H Saturn RA 79.9872 80', 'S Jupiter → H Saturn Dec 8.0020'), '12 8 and 80')
check(has(13, 'Jupiter – Saturn: digits 8', 'H Jupiter – H Saturn RA 79.9872', 'S Jupiter → J Saturn RA 8.0193', field='only'), '13 Jupiter-Saturn 8')

check(not any(it['check'] == 14 for c in per for it in per[c]), '14 none in Newcastle at >= 50')
_, pl = EB.run(os.path.join(ROOT, 'reference/classic/race_batch_20210402_lingfield_aw_1435_active.xlsx'))
c14 = [(c, ' | '.join(it['cells']), it['field']) for c in pl for it in pl[c] if it['check'] == 14]
check(len(c14) == 1 and c14[0][0] == 5 and 'H Jupiter – H Uranus Dec 14.4459 14.4444 ninth (98.46)' in c14[0][1]
      and 'S Jupiter → H Chiron Dec 14.4461 14.4444 ninth (98.21)' in c14[0][1] and c14[0][2] == 'only', f'14 Pholas only {c14}')
c5 = sorted(c for c in pl for it in pl[c] if it['check'] == 5)
check(c5 == [1, 5], f'5 Lingfield swaps Arafi, Pholas {c5}')

check(has(15, 'S Neptune → H Jupiter RA 179.4564', 'S Neptune → J Jupiter Dec 11.3247', field='only'), '15 Athmad Neptune crossed')
_, ps = EB.run(os.path.join(ROOT, 'reference/classic/race_batch_20211204_sandown_1425_active.xlsx'))
c15 = [(c, ' | '.join(it['cells'])) for c in ps for it in ps[c] if it['check'] == 15]
check(len(c15) == 1 and c15[0][0] == 3 and 'S Ceres → H Mars RA 138.0017 138 whole (83.98)' in c15[0][1]
      and 'S Ceres → J Mars Dec 2.0001 2 whole (99.38)' in c15[0][1], f'15 Sandown Greaneteen only {c15}')
check(any(it['check'] == 15 and 'S Quaoar → H Vesta Dec 37.2167' in ' '.join(it['cells']) for it in pl[5]), '15 Pholas Quaoar crossed')

# own reader: every body cell of every _active.xlsx = the tool's cell set
BOD = set(EB.BODIES)
for path in sorted(glob.glob(os.path.join(ROOT, 'reference/classic/*_active.xlsx'))):
    wb = openpyxl.load_workbook(path, read_only=True)
    mine = set()
    for r in wb['META'].iter_rows(values_only=True):
        if not (r and isinstance(r[0], str) and r[0][:1] == 'P' and r[0][1:].isdigit()):
            continue
        tab, role, cloth = r[0], r[1], r[2]
        ch = 'H' if role == 'horse' else 'J'
        rows = list(wb[tab + '_DIST'].iter_rows(values_only=True))
        starts = [i for i, x in enumerate(rows) if isinstance(x[0], str) and '—' in x[0]]
        for s in starts:
            kind = 'N' if rows[s][0].startswith('NATAL') else 'S'
            plane = 'RA' if 'RA' in rows[s][0].split('—')[1] else 'Dec'
            hdr = rows[s + 1]
            i = s + 2
            while i < len(rows) and rows[i][0] is not None and i not in starts:
                a = rows[i][0]
                for j, b in enumerate(hdr):
                    if a in BOD and b in BOD and b != 'Moon' and not (kind == 'N' and a == 'Moon') and (kind == 'S' or a != b):
                        if kind == 'N' and ({a, b} == {'Rahu', 'Ketu'} or EB.BODIES.index(b) < EB.BODIES.index(a)):
                            continue
                        v = rows[i][j]
                        if isinstance(v, (int, float)) and v > 0:
                            bst = F.best(v, plane)
                            if bst:
                                mine.add((cloth, ch, kind, plane, a, b, round(v, 6), bst['target']))
                i += 1
    tool = {(cl, c['ch'], c['kind'], c['plane'], c['a'], c['b'], round(c['v'], 6), c['target'])
            for cl, r in EB.load(path).items() for c in r['cells']}
    check(mine == tool, f'cell set {os.path.basename(path)} ({len(mine)} / {len(tool)})')
print(f'{ok}/{ok + bad}')
sys.exit(1 if bad else 0)
