#!/bin/bash
# setup.sh — make the working folder the tools run in, from this repo.
#
#   bash setup.sh                      # working folder /home/claude (the cloud sessions)
#   ASTRO_HOME=~/astro-work bash setup.sh   # any other folder, e.g. on a Mac
#
# The repo is the master copy. The scripts have /home/claude written in; when ASTRO_HOME is another folder, the copies made
# here have that path rewritten to ASTRO_HOME (the repo files are not touched). After changing a script in the repo, run
# setup.sh again: scripts are always refreshed from the repo; data folders are only copied when missing.
# Python: 3.12 or newer (the scripts use 3.12 f-strings). Inside a virtual environment pip installs into it; otherwise it
# uses --break-system-packages (the cloud sessions).
set -e
R=$(cd "$(dirname "$0")" && pwd)
H=${ASTRO_HOME:-/home/claude}
H=$(mkdir -p "$H" && cd "$H" && pwd)
echo "repo: $R"; echo "working folder: $H"
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' || { echo "ERROR: python3 is $(python3 --version 2>&1); 3.12 or newer is needed"; exit 1; }
mkdir -p "$H/lattice/dump" "$H/ledger" "$H/rebuild_kit" "$H/tools" "$H/pinpoint_blind_kit/reference" "$H/scored" "$H/reads" "$H/reference" "$H/rr"
# scripts: always refreshed from the repo
cp "$R"/lattice/*.py "$H/lattice/"
cp "$R"/ledger/*.py "$H/ledger/"; cp "$R"/ledger/*.sh "$H/ledger/" 2>/dev/null || true
cp -n "$R"/ledger/*.csv "$H/ledger/" 2>/dev/null || true
cp "$R"/rebuild_kit/* "$H/rebuild_kit/"
cp "$R"/tools/* "$H/tools/"
[ -e "$H/ds" ] || ln -s "$H/rebuild_kit" "$H/ds"          # ledger/readrace.py loads active_vibrations from <working folder>/ds
if [ "$H" != "/home/claude" ]; then
  # point the working copies at this folder (perl works the same on macOS and Linux)
  for f in "$H"/lattice/*.py "$H"/ledger/*.py "$H"/ledger/*.sh "$H"/rebuild_kit/*.py "$H"/tools/*; do
    [ -f "$f" ] && perl -pi -e "s#/home/claude#$H#g" "$f"
  done
fi
# data: copied once
[ -d "$H/ephe" ] || cp -r "$R/data/ephe" "$H/ephe"
[ -d "$H/ledger/allpos" ] || cp -r "$R/data/allpos" "$H/ledger/allpos"
[ -d "$H/ledger/sky" ] || cp -r "$R/data/sky" "$H/ledger/sky"
mkdir -p "$H/ledger/skygrid"; cp -n "$R"/data/skygrid/*.csv "$H/ledger/skygrid/" 2>/dev/null || true   # grids: any new ones added, existing kept
cp -n "$R/reference/profiles_blind_kit.csv" "$H/pinpoint_blind_kit/reference/profiles.csv" 2>/dev/null || true
cp -n "$R/reference/profiles_test_scored.csv" "$H/scored/profiles_test_scored.csv" 2>/dev/null || true
cp "$R/reference/races.csv" "$H/reference/races.csv"        # off times and race durations for tools/runner_record.py
cp -n "$R"/docs/*.md "$H/reads/" 2>/dev/null || true
# python packages
if [ -n "$VIRTUAL_ENV" ]; then PIP="python3 -m pip install -q"; else PIP="python3 -m pip install -q --break-system-packages"; fi
$PIP numpy pandas scipy openpyxl matplotlib pytz
# pyswisseph: on Debian the plain build can fail against the system setuptools; an isolated PEP 517 build works
python3 -c "import swisseph" 2>/dev/null || $PIP pyswisseph 2>/dev/null || $PIP --use-pep517 pyswisseph || { echo "ERROR: pyswisseph did not install"; exit 1; }
# checks — fail loudly
n=$(find "$H/ledger/allpos" -type l | wc -l | tr -d ' '); [ "$n" = 0 ] || { echo "ERROR: $n linked files in ledger/allpos"; exit 1; }
[ -s "$H/ledger/allpos/20220318_doncaster_1440__NATAL_HOURLY.csv" ] || { echo "ERROR: Doncaster natal file missing"; exit 1; }
[ -e "$H/ds/active_vibrations.py" ] || { echo "ERROR: $H/ds/active_vibrations.py missing"; exit 1; }
left=$(grep -h "/home/claude" "$H"/lattice/*.py "$H"/tools/* "$H"/ledger/*.py 2>/dev/null | grep -v "$H" | wc -l | tr -d ' ')
[ "$H" = "/home/claude" ] || [ "$left" = 0 ] || { echo "ERROR: $left lines in the working scripts still point at /home/claude"; exit 1; }
python3 -c "import swisseph, numpy, pandas, pytz; print('python packages ok')"
echo "working folder ready: $H"
