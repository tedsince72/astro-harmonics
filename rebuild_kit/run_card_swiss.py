"""
run_card_swiss.py — Full pipeline for today's UK racecards (Swiss Ephemeris engine).

Scrapes all UK races with <= max_runners, then for each race:
  1. racingpost_card_scraper.py     — scrape racecards, write CSVs
  2. racingpost_excel_charts_swiss.py — generate natal + transit xlsx (Swiss Ephemeris)
  3. active_vibrations.py           — score xlsx, write _active.xlsx
  3b. (with --tables) ~/astro-harmonics/tools/jupiter_tables.py — <race>_jupiter_tables.xlsx (raw Jupiter tables)
  4. run_pipeline.py                — sections 1-6, three-way, summary
  5. full_race_detail.py            — entry-level txt
  6. uk_race_predictor.py           — prediction output

Usage:
    # Scrape today's cards and run full pipeline
    python run_card_swiss.py --lookup jockeys_lookup.csv --max-runners 8 --uk-only

    # Skip scraping (CSVs already exist in a folder)
    python run_card_swiss.py --folder racecards/20260927_uk_all --skip-scrape

Options:
    --lookup jockeys_lookup.csv
    --max-runners 8              (default: no limit)
    --min-runners 3              (default: no limit)
    --uk-only                    (only UK venues)
    --date YYYY-MM-DD            (default: today)
    --folder racecards/...       (use existing folder, skip scrape)
    --output-dir racecards/w48w48
    --ephemeris-path <script_dir>/ephe   (default: ephe/ next to this script)
    --engine celestial_bodies_swisseph.py (default: next to this script)
    --skip-scrape
    --skip-charts
    --skip-vibrations
    --skip-pipeline
    --skip-detail
    --skip-predict
    --tables                     (after step 3: Jupiter tables workbook next to the race xlsx)
    --tables-script <path>       (default: ~/astro-harmonics/tools/jupiter_tables.py)
"""

import argparse
import csv
import os
import subprocess
import sys
from datetime import date, datetime
from glob import glob


def run_step(label, cmd, capture=False):
    print(f"\n  {'─'*55}")
    print(f"  {label}")
    print(f"  {'─'*55}")
    if capture:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='')
    else:
        result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\n  [FAILED] {label} — exit code {result.returncode}")
        return False
    print(f"\n  [OK] {label}")
    return result if capture else True


def find_csvs(folder):
    """Find all race_batch CSVs in folder."""
    return sorted(glob(os.path.join(folder, 'race_batch_*.csv')))


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description="Full card pipeline for UK races (Swiss Ephemeris).")
    parser.add_argument("--lookup", default="jockeys_lookup.csv")
    parser.add_argument("--max-runners", type=int, default=None)
    parser.add_argument("--min-runners", type=int, default=None)
    parser.add_argument("--uk-only", action="store_true")
    parser.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")
    parser.add_argument("--folder", default=None, help="Existing racecards folder (skips scrape)")
    parser.add_argument("--output-dir", default="racecards/w48w48")
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
    results_dir = os.path.join(output_dir, "results")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    target_date = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else date.today()
    date_str = target_date.strftime("%Y%m%d")

    # Determine folder
    if args.folder:
        folder = args.folder
        args.skip_scrape = True
    else:
        folder = os.path.join("racecards", f"{date_str}_uk_all")

    print(f"\n{'━'*60}")
    print(f"  run_card_swiss.py  (Swiss Ephemeris) — {target_date}")
    print(f"  Folder:      {folder}")
    print(f"  Output dir:  {output_dir}")
    print(f"  Max runners: {args.max_runners or 'no limit'}")
    print(f"  Min runners: {args.min_runners or 'no limit'}")
    print(f"  UK only:     {args.uk_only}")
    print(f"  Engine:      {args.engine}")
    print(f"  Ephe:        {args.ephemeris_path}")
    print(f"{'━'*60}")

    # ── Step 1: Scrape all cards ────────────────────────────────────
    if not args.skip_scrape:
        cmd = [
            sys.executable,
            os.path.join(script_dir, "racingpost_card_scraper.py"),
            "--lookup", args.lookup,
            "--outdir", ".",
        ]
        if args.max_runners:
            cmd += ["--max-runners", str(args.max_runners)]
        if args.min_runners:
            cmd += ["--min-runners", str(args.min_runners)]
        if args.uk_only:
            cmd += ["--uk-only"]
        if args.date:
            cmd += ["--date", args.date]
        run_step("Step 1 — Scrape all racecards", cmd)
    else:
        print("\n  [SKIP] Step 1 — scrape")

    # ── Find all CSVs ───────────────────────────────────────────────
    csvs = find_csvs(folder)
    if not csvs:
        print(f"\n[ERROR] No CSVs found in {folder}")
        sys.exit(1)

    print(f"\n  Found {len(csvs)} race(s) to process:")
    for c in csvs:
        print(f"    {os.path.basename(c)}")

    # ── Process each race ───────────────────────────────────────────
    for csv_path in csvs:
        race_id = os.path.splitext(os.path.basename(csv_path))[0]
        race_folder = os.path.dirname(csv_path)

        xlsx_path   = os.path.join(race_folder, f"{race_id}.xlsx")
        active_path = os.path.join(race_folder, f"{race_id}_active.xlsx")
        detail_path = os.path.join(results_dir, f"{race_id}.txt")

        print(f"\n{'━'*60}")
        print(f"  RACE: {race_id}")
        print(f"{'━'*60}")

        # Step 2: Charts (Swiss Ephemeris)
        if not args.skip_charts:
            if not run_step("Step 2 — Charts (Swiss Ephemeris)", [
                sys.executable, os.path.join(script_dir, "racingpost_excel_charts_swiss.py"),
                "--csv", csv_path,
                "--outdir", race_folder,
                "--engine", args.engine,
                "--ephemeris-path", args.ephemeris_path,
            ]):
                print(f"  [SKIP remaining steps for {race_id}]")
                continue
        else:
            print("\n  [SKIP] Step 2 — charts")

        # Step 3: Vibrations
        if not args.skip_vibrations:
            if not os.path.exists(xlsx_path):
                print(f"  [ERROR] xlsx not found: {xlsx_path}")
                continue
            if not run_step("Step 3 — Vibrations", [
                sys.executable, os.path.join(script_dir, "active_vibrations.py"),
                "--input", xlsx_path,
            ]):
                print(f"  [SKIP remaining steps for {race_id}]")
                continue
        else:
            print("\n  [SKIP] Step 3 — vibrations")

        # Step 3b: Jupiter tables (optional; a failure does not stop the race)
        if args.tables:
            if os.path.exists(xlsx_path):
                if not run_step("Step 3b — Jupiter tables", [
                    sys.executable, args.tables_script, xlsx_path,
                ]):
                    print(f"  [WARN] Jupiter tables failed for {race_id} — continuing")
            else:
                print(f"  [WARN] Step 3b — xlsx not found: {xlsx_path}")

        # Step 4: Pipeline (no winner known for racecards — pass TBD)
        if not args.skip_pipeline:
            if not os.path.exists(active_path):
                print(f"  [ERROR] active xlsx not found: {active_path}")
                continue
            if not run_step("Step 4 — Pipeline", [
                sys.executable, os.path.join(script_dir, "run_pipeline.py"),
                active_path, "TBD", "TBD",
                "--output-dir", output_dir,
            ]):
                print(f"  [SKIP remaining steps for {race_id}]")
                continue
        else:
            print("\n  [SKIP] Step 4 — pipeline")

        # Step 5: Full race detail
        if not args.skip_detail:
            if not run_step("Step 5 — Detail", [
                sys.executable, os.path.join(script_dir, "full_race_detail.py"),
                race_id, "TBD", "TBD", output_dir,
                "--out", detail_path,
            ]):
                print(f"  [SKIP remaining steps for {race_id}]")
                continue
        else:
            print("\n  [SKIP] Step 5 — detail")

        # Step 6: Predictor
        if not args.skip_predict:
            if not os.path.exists(detail_path):
                print(f"  [ERROR] detail txt not found: {detail_path}")
                continue
            run_step("Step 6 — Predict", [
                sys.executable, os.path.join(script_dir, "uk_race_predictor.py"),
                detail_path,
            ])
        else:
            print("\n  [SKIP] Step 6 — predict")

    # ── Summary ─────────────────────────────────────────────────────
    print(f"\n{'━'*60}")
    print(f"  COMPLETE — {len(csvs)} race(s) processed  (Swiss Ephemeris)")
    print(f"  Results in: {results_dir}")
    print(f"{'━'*60}\n")


if __name__ == "__main__":
    main()
