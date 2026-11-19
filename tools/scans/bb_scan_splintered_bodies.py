"""Splintered's bodies (19 Nov 2026, Eddie: 'check the bodies involved not just relationships'; read-only; from the bybody xlsx).
Wolverhampton AW 18:00 16 Nov 2026, 7 Splintered. Per runner, horse and jockey charts:
  V   a royal natal line R – X >= 90 (number family) whose same-body ratio scores >= 90 AND crossed ratio >= 80
      (Splintered H Regulus – H Venus RA 90×φ 99.9, ratio to S Venus → H Venus RA 3/2 92.2, crossed to Dec 13 81.8)
  V8  the same with both ratios >= 80
  C   a same-body line S X → c X >= 90 in a number family and two or more royal lines on X (same chart, any score) whose
      same-body or crossed ratio to that line scores >= 90 (Splintered H Chiron Dec 3 96.7: Aldebaran Dec 9 -> 3 93.8,
      Fomalhaut RA 30 -> crossed 10 91.4)
  U0  the horse's natal Uranus takes no scoring sky line S Y → H Uranus (any score, conj / cp / opposition incl., Moon incl.)
  U0m the same with the Moon left out (a Moon line does not count)
  E0  number of the horse's natal bodies (24, no Moon) that take no scoring sky line (report only)
Per measure: picks / won / by chance (sum 1/field) over every result race with a bybody xlsx; holders in --race.
Usage: python3 tools/scans/bb_scan_splintered_bodies.py [--race <race>]"""
import sys, os, re, openpyxl
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, 'tools'); sys.path.insert(0, 'tools/scans')
import bb_scan_negatives as N

ROYAL = ('Aldebaran', 'Antares', 'Fomalhaut', 'Regulus')
NUMF = {'whole', 'golden', 'phi power', 'ninth', 'sqrt2', 'silver', '√2'}
BODIES = ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Ceres', 'Pallas', 'Juno', 'Vesta',
          'Chiron', 'Eris', 'Haumea', 'Makemake', 'Gonggong', 'Quaoar', 'Orcus', 'Sedna', 'Transpluto', 'Rahu', 'Ketu']
SKYTO = re.compile(r'^S (.+?) → ([HJ]) (.+)$')
ROYROW = re.compile(r'^([HJ]) (Aldebaran|Antares|Fomalhaut|Regulus) – \1 (.+)$')
KEYS = ['V', 'V8', 'C', 'U0', 'U0m']


def runner(ws):
    rows = [r for r in ws.iter_rows(values_only=True) if r and isinstance(r[0], str)]
    same = {}      # (chart, X, plane) -> (value, score) for scoring number-family same-body lines
    taken = {}     # (chart, X) -> set of sky Y with a scoring line onto it
    royal = set()
    for r in rows:
        m = SKYTO.match(r[0])
        if m and r[5] is not None:
            Y, c, X = m.groups()
            taken.setdefault((c, X), set()).add(Y)
            if Y == X and r[3] in NUMF and r[1] in ('RA', 'Dec'):
                same[(c, X, r[1])] = (r[2], r[5])
        m = ROYROW.match(r[0])
        if m and r[1] in ('RA', 'Dec'):
            royal.add(tuple(r[:22]) if len(r) >= 22 else tuple(r) + (None,) * (22 - len(r)))
    hit = {k: [] for k in KEYS}
    cnt = {}
    for r in royal:
        c, R, X = ROYROW.match(r[0]).groups()
        s1, s2 = r[13], r[20]
        if r[3] in NUMF and r[5] is not None and r[5] >= 90 and s1 is not None and s2 is not None:
            if s1 >= 90 and s2 >= 80:
                hit['V'].append(f'{c} {R} – {X} {r[1]} {r[4]} ({r[5]:.1f}) {r[12]} ({s1:.1f}) / {r[19]} ({s2:.1f})')
            if s1 >= 80 and s2 >= 80:
                hit['V8'].append(f'{c} {R} – {X} {r[1]} ({r[5]:.1f}) {s1:.1f} / {s2:.1f}')
        other = 'Dec' if r[1] == 'RA' else 'RA'
        for col, pl in ((13, r[1]), (20, other)):
            sb = same.get((c, X, pl))
            ref = r[9] if col == 13 else r[16]
            if sb and sb[1] >= 90 and r[col] is not None and r[col] >= 90 and ref is not None and abs(ref - sb[0]) < 1e-6:
                cnt.setdefault((c, X, pl), []).append(f'{R} {r[1]} {r[4]} -> {r[col - 1]} ({r[col]:.1f})')
    for (c, X, pl), v in cnt.items():
        if len(v) >= 2:
            hit['C'].append(f'{c} {X} same-body {pl} {same[(c, X, pl)][0]:.4f} ({same[(c, X, pl)][1]:.1f}): ' + '; '.join(v))
    tu = taken.get(('H', 'Uranus'), set())
    if not tu:
        hit['U0'].append('H Uranus: no sky line')
    if not (tu - {'Moon'}):
        hit['U0m'].append('H Uranus: no sky line (Moon aside)' + (f' [Moon only]' if tu else ''))
    e0 = [X for X in BODIES if not taken.get(('H', X))]
    return hit, e0


def race(rc):
    p = f'docs/eddie_read/bybody/{rc}/{rc}_bybody.xlsx'
    if not os.path.exists(p):
        return None
    wb = openpyxl.load_workbook(p, read_only=True)
    out = []
    for sn in wb.sheetnames:
        h, e0 = runner(wb[sn])
        out.append((sn[3:], h, e0))
    return out


def main():
    if '--race' in ARGS:
        for n, h, e0 in race(ARGS[ARGS.index('--race') + 1]):
            print(f'{n}: ' + ', '.join(k for k in KEYS if h[k]) + f'  | horse bodies with no sky line: {e0}')
            for k in KEYS:
                for x in h[k]: print(f'    {k} {x}')
        return
    tot = {k: [0, 0, 0.0] for k in KEYS}; who = {k: [] for k in KEYS}; nr = 0; e0w = e0f = 0.0; e0n = 0
    for rc, win in N.RACES:
        rows = race(rc)
        if not rows or not any(win in n for n, *_ in rows):
            continue
        nr += 1; n = len(rows)
        for name, h, e0 in rows:
            w = win in name
            for k in KEYS:
                if h[k]:
                    tot[k][0] += 1; tot[k][1] += w; tot[k][2] += 1 / n
                    if w: who[k].append(win)
            if w: e0w += len(e0); e0n += 1
            e0f += len(e0) / n
    print(f'## Splintered bodies over {nr} result races with a bybody xlsx\n')
    print('| measure | picks | won | by chance |\n|---|---|---|---|')
    for k in KEYS:
        print(f'| {k} | {tot[k][0]} | {tot[k][1]} | {tot[k][2]:.1f} |')
    print(f'\nE0 (horse bodies with no sky line): winners mean {e0w / e0n:.2f}, field mean {e0f / nr:.2f}\n')
    for k in KEYS:
        print(f'- {k} winners: ' + (', '.join(who[k]) or 'none'))


if __name__ == '__main__':
    main()
