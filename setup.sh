#!/bin/bash
# setup.sh — recreate the working layout the tools expect (everything lives under /home/claude).
# Run from the repo root:  bash setup.sh
set -e
R=$(cd "$(dirname "$0")" && pwd); H=/home/claude
mkdir -p $H/lattice $H/ledger $H/rebuild_kit $H/tools $H/pinpoint_blind_kit/reference $H/scored $H/reads
cp -n $R/lattice/*.py $H/lattice/
cp -n $R/ledger/*.py $R/ledger/*.csv $H/ledger/ 2>/dev/null || true
cp -n $R/ledger/*.sh $H/ledger/ 2>/dev/null || true
cp -n $R/rebuild_kit/* $H/rebuild_kit/
cp -n $R/tools/* $H/tools/
[ -d $H/ephe ] || cp -r $R/data/ephe $H/ephe
[ -d $H/ledger/allpos ] || cp -r $R/data/allpos $H/ledger/allpos
[ -d $H/ledger/sky ] || cp -r $R/data/sky $H/ledger/sky
[ -d $H/ledger/skygrid ] || cp -r $R/data/skygrid $H/ledger/skygrid
cp -n $R/reference/profiles_blind_kit.csv $H/pinpoint_blind_kit/reference/profiles.csv
cp -n $R/reference/profiles_test_scored.csv $H/scored/profiles_test_scored.csv
cp -n $R/docs/*.md $H/reads/ 2>/dev/null || true
pip install --break-system-packages -q pyswisseph numpy openpyxl 2>/dev/null || true
echo "layout ready under $H"
