#!/usr/bin/env python3
"""jupiter_reader.py RACE [--batch X.xlsx] [--off "YYYY-MM-DD HH:MM"] [--site lat,lon,elev]
JR v2 - transit-Jupiter reader (design: docs/classic/jupiter_reader_design.md). Output docs/classic/RACE/jupiter/.
RACE = folder in reference/classic made by tools/split_batch.py (<course>_<hhmm>_<yyyymmdd>). No results are opened.
Steps: positions (JR v1's tools/jup/positions.py, unchanged, written to this folder) -> F engine rates (tools/jup2/motion.py)
-> hits A-E (tools/jup2/hits.py) -> field counts, flags, pages (tools/jup2/report.py)."""
import argparse, os, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools', 'jup2'))
from core import load_positions                      # noqa: E402
import motion, hits, report                          # noqa: E402

JR_VERSION = 'JR v2'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('race'); ap.add_argument('--batch'); ap.add_argument('--off'); ap.add_argument('--site')
    a = ap.parse_args()
    os.chdir(REPO)
    race = a.race
    out = f'docs/classic/{race}/jupiter'
    os.makedirs(out, exist_ok=True)
    # 1. positions (JR v1 step, unchanged)
    r = subprocess.run([sys.executable, 'tools/jup/positions.py', f'reference/classic/{race}', f'{out}/positions.csv'],
                       capture_output=True, text=True)
    open(f'{out}/positions_log.txt', 'w').write(r.stdout + r.stderr)
    if r.returncode != 0:
        sys.exit(f'positions step failed:\n{r.stdout}{r.stderr}')
    if 'NOT an exact Rahu mirror' in r.stdout:
        sys.exit('Ketu is not an exact Rahu mirror in some chart (positions_log.txt): Ketu cannot be rebuilt - stopping')
    sky, runners = load_positions(f'{out}/positions.csv')
    # 2. F: engine rates
    course, hhmm, ymd = motion.race_parts(race)
    batch = a.batch or f'reference/classic/race_batch_{ymd}_{course}_{hhmm}.xlsx'
    import openpyxl, glob
    first = sorted(glob.glob(f'reference/classic/{race}/*__P[0-9][0-9].xlsx'))[0]
    label = next(openpyxl.load_workbook(first, read_only=True)['TRANS'].iter_rows(min_row=2, max_row=2, values_only=True))[0]
    off, site, src = motion.off_and_site(race, label, batch, a.off, a.site)
    dur_s, dur_src = motion.race_duration(race)
    rates, elines = motion.engine_rates(sky, off, site)
    elines = [f'{JR_VERSION} engine check — {race}', f'source: {src}; batch {batch if os.path.exists(batch) else "(none)"}'] + elines
    open(f'{out}/engine_check.txt', 'w').write('\n'.join(elines) + '\n')
    durtxt = f'off {off}; race duration {dur_s:g} s = {dur_s / 60:.2f} min ({dur_src}); exact-pre-off window 5 min'
    # 3. hits
    race_ctx = hits.Race(sky, rates, dur_s / 60.0)
    sky_h = hits.sky_hits(race_ctx)
    per = {P: hits.runner_hits(race_ctx, runners[P]) for P in sorted(runners)}
    # 4. pages
    sky_lines = {'SJ': sky['Jupiter']}
    repro = next((l for l in elines if l.startswith('reproduction')), elines[-1])
    report.write_all(out, race, f'{JR_VERSION}; engine check (engine_check.txt): {repro}', sky_lines, sky_h, runners, per, durtxt)
    print(f'{race}: {len(runners)} runners, sky hits {len(sky_h)}, runner hits ' +
          ', '.join(f'{P} {len(h)}' for P, h in per.items()) + f' -> {out}/')
    print('  ' + repro)


if __name__ == '__main__':
    main()
