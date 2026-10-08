#!/bin/bash
# m1d.sh BODY TAB : Method 1 for Doncaster 14:40 18 Mar 2022 (natal 12:00); TAB P03 = Olympe De Gouges, P04 = David Noonan
S=/home/claude/tools; R=20220318_doncaster_1440; T=${2:-P03}
cd /home/claude/lattice
python3 $S/natnums.py $R 14:40:41 248 $T $1 0.002 12 2>&1 | grep -v "^===\|NODES LAYER\|transit Rahu\|transit Ketu" | grep -v "not at midday"
python3 $S/natchords.py $R 14:40:41 248 $T $1 12 2>&1 | grep -v "^===\|NODES LAYER\|transit Rahu\|transit Ketu"
