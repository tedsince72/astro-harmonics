#!/usr/bin/env python3
"""positions.py RACE_DIR [OUT_CSV]

Jupiter-centred read, layer 0: positions only (no measuring).
Reads every runner workbook in RACE_DIR (*__P##.xlsx: TRANS = sky, P01 = horse natal, P02 = jockey natal;
column B body, E RA deg, I Dec signed) and writes one table for the race:

  runner, cloth, horse, jockey, chart (S/H/J), body, kind (body/star), ra, dec

Rules (Eddie, 12 Oct 2026):
- bodies: Sun, Moon (sky only), Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Chiron, Ceres, Pallas,
  Juno, Vesta, Rahu, Eris, Sedna, Haumea, Makemake, Orcus, Quaoar, Gonggong, Transpluto
- Ketu folded into Rahu (its mirror): Ketu row dropped, mirror checked and reported
- dropped: natal Moon, Part_of_Fortune, Part_of_Spirit, Ascendant, Midheaven, Vertex
- stars: the 22 rows ending _B, each chart's own values as they stand
- numbers copied exactly as stored in the workbook (repr of the float), no rounding
- sky (S) written once per race, after checking every runner's TRANS sheet is identical
"""
import sys, os, glob, csv, re
import openpyxl

BODIES = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron',
          'Ceres', 'Pallas', 'Juno', 'Vesta', 'Rahu', 'Eris', 'Sedna', 'Haumea', 'Makemake', 'Orcus', 'Quaoar',
          'Gonggong', 'Transpluto']
STARS = ['Algol', 'Pleiades', 'Aldebaran', 'Capella', 'Sirius', 'Procyon', 'Regulus', 'Alkaid', 'Algorab', 'Spica',
         'Arcturus', 'Alphecca', 'Antares', 'Vega', 'Deneb Algedi', 'Fomalhaut', 'Rigel', 'Betelgeuse', 'Polaris',
         'Castor', 'Altair', 'Bellatrix']
DROP = {'Part_of_Fortune', 'Part_of_Spirit', 'Ascendant', 'Midheaven', 'Vertex', 'Ketu'}
COL_BODY, COL_RA, COL_DEC = 1, 4, 8   # B, E, I


def read_sheet(ws):
    out, label = {}, None
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[COL_BODY] is None:
            continue
        label = label or r[0]
        out[str(r[COL_BODY]).strip()] = (r[COL_RA], r[COL_DEC])
    return label, out


def keep(chart, sheet):
    rows, notes = [], []
    want = [b for b in BODIES if not (b == 'Moon' and chart != 'S')]
    for b in want:
        if b in sheet:
            rows.append((b, 'body') + sheet[b])
        else:
            notes.append(f'{chart}: missing body {b}')
    for s in STARS:
        k = s + '_B'
        if k in sheet:
            rows.append((s, 'star') + sheet[k])
        else:
            notes.append(f'{chart}: missing star {s}')
    known = set(want) | {s + '_B' for s in STARS} | DROP | {'Moon'}
    for k in sheet:
        if k not in known:
            notes.append(f'{chart}: unexpected row {k} (not kept)')
    # Ketu fold check: Ketu should be Rahu's mirror (RA + 180, Dec negated)
    if 'Rahu' in sheet and 'Ketu' in sheet:
        (ra_r, de_r), (ra_k, de_k) = sheet['Rahu'], sheet['Ketu']
        dra = abs(((ra_k - ra_r) % 360) - 180)
        dde = abs(de_k + de_r)
        if dra > 1e-6 or dde > 1e-6:
            notes.append(f'{chart}: Ketu is NOT an exact Rahu mirror (RA off {dra!r}, Dec off {dde!r})')
    return rows, notes


def main():
    race_dir = sys.argv[1].rstrip('/')
    race = os.path.basename(race_dir)
    out = sys.argv[2] if len(sys.argv) > 2 else f'docs/jupiter/{race}/positions.csv'
    files = sorted(glob.glob(f'{race_dir}/*__P[0-9][0-9].xlsx'))
    if not files:
        sys.exit(f'no runner workbooks in {race_dir}')
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)

    table, notes, sky, sky_from = [], [], None, None
    for f in files:
        runner = re.search(r'__(P\d\d)\.xlsx$', f).group(1)
        wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
        _, trans = read_sheet(wb['TRANS'])
        hlab, horse = read_sheet(wb['P01'])
        jlab, jock = read_sheet(wb['P02'])
        cloth = str(hlab).split(' ', 1)[0] if hlab else ''
        hname = str(hlab).split(' ', 1)[1] if hlab and ' ' in str(hlab) else str(hlab)
        jname = str(jlab).split(' ', 1)[1] if jlab and ' ' in str(jlab) else str(jlab)
        if sky is None:
            sky, sky_from = trans, runner
            srows, sn = keep('S', trans)
            notes += sn
            for b, kind, ra, dec in srows:
                table.append(['SKY', '', '', '', 'S', b, kind, repr(ra), repr(dec)])
        elif trans != sky:
            diff = [k for k in set(trans) | set(sky) if trans.get(k) != sky.get(k)]
            notes.append(f'{runner}: TRANS differs from {sky_from} in {len(diff)} rows: {sorted(diff)[:6]}')
        for chart, sheet in (('H', horse), ('J', jock)):
            rows, rn = keep(chart, sheet)
            notes += [f'{runner} {n}' for n in rn]
            for b, kind, ra, dec in rows:
                table.append([runner, cloth, hname, jname, chart, b, kind, repr(ra), repr(dec)])

    with open(out, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['runner', 'cloth', 'horse', 'jockey', 'chart', 'body', 'kind', 'ra', 'dec'])
        w.writerows(table)

    n_run = len(files)
    print(f'{race}: {n_run} runners, {len(table)} rows -> {out}')
    print(f'  sky rows {sum(1 for r in table if r[4] == "S")}, per natal chart {len(BODIES) - 1} bodies + {len(STARS)} stars expected')
    for f in files:
        r = re.search(r'__(P\d\d)\.xlsx$', f).group(1)
        rr = [x for x in table if x[0] == r]
        print(f'  {r} cloth {rr[0][1]:>2} {rr[0][2]} / {rr[0][3]}: H {sum(1 for x in rr if x[4]=="H")}, J {sum(1 for x in rr if x[4]=="J")}')
    print('notes:' if notes else 'notes: none')
    for n in notes:
        print('  ' + n)


if __name__ == '__main__':
    main()
