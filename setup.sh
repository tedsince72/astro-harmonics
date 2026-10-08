#!/bin/bash
# setup.sh — recreate the working layout the tools expect (everything lives under /home/claude).
# Run from the repo root:  bash setup.sh
set -e
R=$(cd "$(dirname "$0")" && pwd); H=/home/claude
mkdir -p $H/lattice $H/lattice/dump $H/ledger $H/rebuild_kit $H/tools $H/pinpoint_blind_kit/reference $H/scored $H/reads $H/reference $H/rr
cp -n $R/lattice/*.py $H/lattice/
cp -n $R/ledger/*.py $R/ledger/*.csv $H/ledger/ 2>/dev/null || true
cp -n $R/ledger/*.sh $H/ledger/ 2>/dev/null || true
cp -n $R/rebuild_kit/* $H/rebuild_kit/
[ -e $H/ds ] || ln -s $H/rebuild_kit $H/ds          # ledger/readrace.py loads active_vibrations from /home/claude/ds
cp -n $R/tools/* $H/tools/
[ -d $H/ephe ] || cp -r $R/data/ephe $H/ephe
[ -d $H/ledger/allpos ] || cp -r $R/data/allpos $H/ledger/allpos
[ -d $H/ledger/sky ] || cp -r $R/data/sky $H/ledger/sky
[ -d $H/ledger/skygrid ] || cp -r $R/data/skygrid $H/ledger/skygrid
cp -n $R/reference/profiles_blind_kit.csv $H/pinpoint_blind_kit/reference/profiles.csv
cp -n $R/reference/profiles_test_scored.csv $H/scored/profiles_test_scored.csv
cp $R/reference/races.csv $H/reference/races.csv        # off times and race durations for tools/runner_record.py
cp -n $R/docs/*.md $H/reads/ 2>/dev/null || true
pip install --break-system-packages -q numpy openpyxl
# pyswisseph: the plain build fails against Debian's system setuptools (install_layout error); an isolated PEP 517 build works
python3 -c "import swisseph" 2>/dev/null || pip install --break-system-packages pyswisseph 2>/dev/null || pip install --break-system-packages --use-pep517 pyswisseph || { echo "ERROR: pyswisseph did not install"; exit 1; }
# checks — fail loudly
n=$(find $H/ledger/allpos -type l | wc -l); [ "$n" = 0 ] || { echo "ERROR: $n linked files in ledger/allpos"; exit 1; }
[ -s $H/ledger/allpos/20220318_doncaster_1440__NATAL_HOURLY.csv ] || { echo "ERROR: Doncaster natal file missing"; exit 1; }
[ -e $H/ds/active_vibrations.py ] || { echo "ERROR: $H/ds/active_vibrations.py missing"; exit 1; }
[ -d $H/lattice/dump ] || { echo "ERROR: $H/lattice/dump missing"; exit 1; }
python3 -c "import swisseph; print('swisseph ok')"
echo "layout ready under $H"
