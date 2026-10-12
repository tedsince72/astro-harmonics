#!/bin/bash
# run_all.sh RACE  - Jupiter-centred read, all layers (positions -> measures -> ratios -> shapes -> field). No results used.
set -e
R=$1; cd "$(dirname "$0")/../.."
python3 tools/jup/positions.py reference/classic/$R > docs/jupiter/$R.positions_log.tmp 2>&1 || { cat docs/jupiter/$R.positions_log.tmp; exit 1; }
mkdir -p docs/jupiter/$R && mv docs/jupiter/$R.positions_log.tmp docs/jupiter/$R/positions_log.txt
python3 tools/jup/measures.py $R > /dev/null
PYTHONPATH=tools/jup python3 tools/jup/ratios.py $R > /dev/null
PYTHONPATH=tools/jup python3 tools/jup/shapes.py $R > /dev/null
if [ -f tools/jup/field.py ]; then PYTHONPATH=tools/jup python3 tools/jup/field.py $R; fi
echo "done: docs/jupiter/$R/"
