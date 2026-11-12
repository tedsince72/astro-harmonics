"""
run_race_swiss.py — Full pipeline for one UK horse racing race (Swiss Ephemeris engine).

Steps:
  1. racingpost_results_scraper.py   — scrape results, write CSV
  2. racingpost_excel_charts_swiss.py — generate natal + transit xlsx (Swiss Ephemeris)
  3. active_vibrations.py            — score xlsx, write _active.xlsx
  3b. (with --tables) ~/astro-harmonics/tools/jupiter_tables.py — <race>_jupiter_tables.xlsx next to the race xlsx
  4. run_pipeline.py                 — sections 1-6, three-way, summary
  5. full_race_detail.py             — entry-level txt file
  6. uk_race_predictor.py            — ranked prediction + _predict.txt

Usage:
    python run_race_swiss.py --url "https://www.racingpost.com/results/1353/newcastle-aw/2026-09-25/927687/"

    # Also write the Jupiter tables workbook (astro-harmonics) next to the race xlsx
    python run_race_swiss.py --url "<racingpost results URL>" --tables

Options:
    --racecards-root racecards                        (default: racecards)
    --output-dir racecards/w48w48                     (default: racecards/w48w48)
    --lookup jockeys_lookup.csv                       (default: jockeys_lookup.csv)
    --ephemeris-path <script_dir>/ephe               (default: ephe/ next to this script)
    --engine celestial_bodies_swisseph.py             (default: next to this script)
    --skip-scrape
    --skip-charts
    --skip-vibrations
    --skip-pipeline
    --skip-detail
    --skip-predict
    --tables                                          (after step 3: Jupiter tables workbook next to the race xlsx)
    --tables-script <path>                            (default: ~/astro-harmonics/tools/jupiter_tables.py)
"""

import argparse
import csv
import os
import re
import subprocess
import sys


def run_step(label, cmd, capture=False):
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"  {' '.join(str(c) for c in cmd)}")
    print(f"{'─'*60}")
    if capture:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='')
    else:
        result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\n[FAILED] {label} — exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"\n[OK] {label}")
    return result


def parse_url(url):
    m = re.search(r'/results/\d+/([^/]+)/(\d{4}-\d{2}-\d{2})/', url)
    if not m:
        print(f"[ERROR] Could not parse venue/date from URL: {url}")
        sys.exit(1)
    venue = m.group(1).replace('-', '_')
    date_str = m.group(2).replace('-', '')
    return venue, date_str


def get_race_time_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print(f"[ERROR] CSV is empty: {csv_path}")
        sys.exit(1)
    return rows[0]['race_time'].strip().replace(':', '')


def get_winner_from_csv(csv_path):
    """
    Winner = the horse row with finish_pos 1 (results scraper v2.0 CSV).
    Non-runners (status NR) are ignored. A dead heat stops the run.
    P-tabs assigned by cloth number sorted numerically:
      lowest cloth = P01/P02, next = P03/P04, etc.
    """
    with open(csv_path, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    if not rows or 'finish_pos' not in rows[0]:
        print(f"[ERROR] {csv_path} has no finish_pos column - re-scrape it with "
              f"racingpost_results_scraper.py v2.0")
        sys.exit(1)

    horses = [r for r in rows if r['subject_type'] == 'horse'
              and r.get('status', 'runner') != 'NR']
    winners = [r for r in horses if r['finish_pos'].strip() == '1']
    if len(winners) != 1:
        found = ', '.join(r['name'] for r in winners) or 'none'
        print(f"[ERROR] Expected exactly one horse with finish_pos 1, found: {found}")
        sys.exit(1)
    winner_horse_row = winners[0]
    winner_cloth = winner_horse_row['cloth'].strip()
    jockey_rows = [r for r in rows if r['subject_type'] == 'jockey'
                   and r['cloth'].strip() == winner_cloth]
    winner_jockey_row = jockey_rows[0] if jockey_rows else {'name': '(no jockey row)'}

    cloths = []
    for row in horses:
        cloth = row['cloth'].strip()
        if cloth not in cloths:
            cloths.append(cloth)
    cloths_sorted = sorted(cloths, key=lambda x: int(x))

    cloth_to_ptab = {}
    for i, cloth in enumerate(cloths_sorted):
        p_num = i + 1
        cloth_to_ptab[cloth] = (
            f"P{str(p_num*2-1).zfill(2)}",
            f"P{str(p_num*2).zfill(2)}"
        )

    if winner_cloth not in cloth_to_ptab:
        print(f"[ERROR] Winner cloth '{winner_cloth}' not found.")
        print(f"  Available cloths: {cloths_sorted}")
        sys.exit(1)

    wh, wj = cloth_to_ptab[winner_cloth]
    print(f"\n  Winner: {winner_horse_row['name']} / {winner_jockey_row['name']}")
    print(f"  Cloth {winner_cloth} -> {wh} / {wj}")
    print(f"  Full cloth mapping: {cloth_to_ptab}")
    return wh, wj


def find_saved_csv(scraper_output, folder):
    """Parse scraper stdout for the saved CSV filename."""
    for line in scraper_output.splitlines():
        m = re.search(r'Saved:\s*(race_batch_\S+\.csv)', line)
        if m:
            path = os.path.join(folder, m.group(1))
            if os.path.exists(path):
                return path
    return None


def find_csv_in_folder(folder):
    """Fallback: find most recently modified CSV in folder."""
    csvs = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.startswith('race_batch_') and f.endswith('.csv')
    ]
    if not csvs:
        return None
    return max(csvs, key=os.path.getmtime)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--racecards-root", default="racecards")
    parser.add_argument("--output-dir", default="racecards/w48w48")
    parser.add_argument("--lookup", default="jockeys_lookup.csv")
    parser.add_argument("--ephemeris-path",
                        default=os.path.join(script_dir, "ephe"))
    parser.add_argument("--engine",
                        default=os.path.join(script_dir, "celestial_bodies_swisseph.py"))
    parser.add_argument("--skip-scrape",      action="store_true")
    parser.add_argument("--skip-charts",      action="store_true")
    parser.add_argument("--skip-vibrations",  action="store_true")
    parser.add_argument("--skip-pipeline",    action="store_true")
    parser.add_argument("--skip-detail",      action="store_true")
    parser.add_argument("--skip-predict",     action="store_true")
    parser.add_argument("--tables",           action="store_true",
                        help="after step 3, write <race>_jupiter_tables.xlsx (astro-harmonics tools/jupiter_tables.py)")
    parser.add_argument("--tables-script",
                        default=os.path.expanduser("~/astro-harmonics/tools/jupiter_tables.py"))
    args = parser.parse_args()

    output_dir = args.output_dir

    venue, date_str = parse_url(args.url)
    folder = os.path.join(args.racecards_root, f"{date_str}_{venue}")
    os.makedirs(folder, exist_ok=True)

    print(f"\n{'━'*60}")
    print(f"  run_race_swiss.py  (Swiss Ephemeris)")
    print(f"  URL:    {args.url}")
    print(f"  Venue:  {venue}  Date: {date_str}")
    print(f"  Folder: {folder}")
    print(f"  Output: {output_dir}")
    print(f"  Engine: {args.engine}")
    print(f"  Ephe:   {args.ephemeris_path}")
    print(f"{'━'*60}")

    # ── Step 1: Scrape ──────────────────────────────────────────────
    csv_path = None
    if not args.skip_scrape:
        result = run_step("Step 1 — Scrape Racing Post results", [
            sys.executable, os.path.join(script_dir, "racingpost_results_scraper.py"),
            "--lookup", args.lookup,
            "--url", args.url,
            "--outdir", ".",
        ], capture=True)
        csv_path = find_saved_csv(result.stdout, folder)
        if csv_path:
            print(f"  [CSV] {csv_path}")
        else:
            print("  [WARN] Could not parse CSV name from scraper output — scanning folder")
    else:
        print("\n  [SKIP] Step 1 — scrape")

    # ── Find CSV ─────────────────────────────────────────────────────
    if csv_path is None:
        csv_path = find_csv_in_folder(folder)
    if not csv_path:
        print(f"[ERROR] No CSV found in {folder}")
        sys.exit(1)

    # Derive race_id from CSV filename
    race_id = os.path.splitext(os.path.basename(csv_path))[0]
    if not re.search(r'_\d{3,4}$', race_id):
        race_time = get_race_time_from_csv(csv_path)
        race_id = f"race_batch_{date_str}_{venue}_{race_time}"
        new_csv = os.path.join(folder, f"{race_id}.csv")
        if csv_path != new_csv:
            os.rename(csv_path, new_csv)
            csv_path = new_csv

    print(f"\n  Race ID: {race_id}")

    xlsx_path   = os.path.join(folder, f"{race_id}.xlsx")
    active_path = os.path.join(folder, f"{race_id}_active.xlsx")
    results_dir = os.path.join(output_dir, "results")
    results_path = os.path.join(results_dir, f"{race_id}.txt")

    # Determine winner
    wh, wj = get_winner_from_csv(csv_path)

    # ── Step 2: Charts (Swiss Ephemeris) ────────────────────────────
    if not args.skip_charts:
        run_step("Step 2 — Generate natal + transit charts (Swiss Ephemeris)", [
            sys.executable, os.path.join(script_dir, "racingpost_excel_charts_swiss.py"),
            "--csv", csv_path,
            "--outdir", folder,
            "--engine", args.engine,
            "--ephemeris-path", args.ephemeris_path,
        ])
    else:
        print("\n  [SKIP] Step 2 — charts")

    # ── Step 3: Vibrations ───────────────────────────────────────────
    if not args.skip_vibrations:
        if not os.path.exists(xlsx_path):
            print(f"[ERROR] xlsx not found: {xlsx_path}")
            sys.exit(1)
        run_step("Step 3 — Score vibrations", [
            sys.executable, os.path.join(script_dir, "active_vibrations.py"),
            "--input", xlsx_path,
        ])
    else:
        print("\n  [SKIP] Step 3 — vibrations")

    # ── Step 3b: Jupiter tables (astro-harmonics, with --tables) ─────
    tables_path = os.path.join(folder, f"{race_id}_jupiter_tables.xlsx")
    if args.tables:
        if os.path.exists(xlsx_path):
            # own subprocess call: run_step exits on a failure, and a tables failure must not stop the race
            print(f"\n  {'─'*55}\n  Step 3b — Jupiter tables\n  {'─'*55}")
            rc = subprocess.run([sys.executable, args.tables_script, xlsx_path]).returncode
            if rc == 0:
                print("\n  [OK] Step 3b — Jupiter tables")
            else:
                print(f"  [WARN] Jupiter tables failed for {race_id} (exit code {rc}) — continuing")
        else:
            print(f"  [WARN] Step 3b — xlsx not found: {xlsx_path}")

    # ── Step 4: Pipeline ─────────────────────────────────────────────
    if not args.skip_pipeline:
        if not os.path.exists(active_path):
            print(f"[ERROR] active xlsx not found: {active_path}")
            sys.exit(1)
        run_step("Step 4 — Run pipeline", [
            sys.executable, os.path.join(script_dir, "run_pipeline.py"),
            active_path, wh, wj,
            "--output-dir", output_dir,
        ])
    else:
        print("\n  [SKIP] Step 4 — pipeline")

    # ── Step 5: Detail ───────────────────────────────────────────────
    if not args.skip_detail:
        os.makedirs(results_dir, exist_ok=True)
        run_step("Step 5 — Full race detail", [
            sys.executable, os.path.join(script_dir, "full_race_detail.py"),
            race_id, wh, wj, output_dir,
            "--out", results_path,
        ])
    else:
        print("\n  [SKIP] Step 5 — detail")

    # ── Step 6: Predict ──────────────────────────────────────────────
    if not args.skip_predict:
        if not os.path.exists(results_path):
            print(f"[ERROR] detail txt not found: {results_path}")
            sys.exit(1)
        run_step("Step 6 — Predict", [
            sys.executable, os.path.join(script_dir, "uk_race_predictor.py"),
            results_path,
        ])
    else:
        print("\n  [SKIP] Step 6 — predict")

    predict_path = os.path.join(results_dir, f"{race_id}_predict.txt")

    print(f"\n{'━'*60}")
    print(f"  COMPLETE — {race_id}  (Swiss Ephemeris)")
    print(f"  Winner:  {wh} / {wj}")
    print(f"  Detail:  {results_path}")
    print(f"  Predict: {predict_path}")
    if args.tables:
        print(f"  Tables:  {tables_path}")
        print(f"  Active:  {active_path}")
    print(f"{'━'*60}\n")


if __name__ == "__main__":
    main()
