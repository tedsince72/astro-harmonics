#!/bin/bash
# m1f.sh BODY [TAB] : Method 1 for Frankel (P01, born 11 Feb 2008 12:00 GMT, hour 12) — Queally is P02
S=/home/claude/tools; R=20120619_ascot_1434; T=${2:-P01}
cd /home/claude/lattice
python3 $S/natnums.py $R 14:34:00 98 $T $1 0.002 12 2>&1 | grep -v "^===\|NODES LAYER\|transit Rahu\|transit Ketu" | grep -v "not at midday"
python3 $S/natchords.py $R 14:34:00 98 $T $1 12 2>&1 | grep -v "^===\|NODES LAYER\|transit Rahu\|transit Ketu"
