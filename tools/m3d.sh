#!/bin/bash
# m3d.sh BODY : Method 3 for Doncaster 14:40 18 Mar 2022 (off 14:40:41, 248 s); winning pair P03 Olympe De Gouges / P04 David Noonan
S=/home/claude/tools; R=20220318_doncaster_1440; O=14:40:41; D=248; B=$1
mkdir -p $S/m3d; cd /home/claude/lattice
timeout 900 python3 $S/sunchords.py $R $O $D $B 2>/dev/null > $S/m3d/${B}_sc.txt &
timeout 600 python3 $S/numcheck.py $R $O $D $B 2>&1 | grep -v "^===\|NODES LAYER\|transit" > $S/m3d/${B}_nc.txt &
timeout 600 python3 $S/parallels.py $R $O $D 0.1 2>&1 | grep -E "^\[|sky $B" | grep -B1 "sky $B" > $S/m3d/${B}_pa.txt &
wait
python3 m3d.py $R $O $D $B P03 P04 $S/m3d/${B}_sc.txt 2>&1 | grep -v "^===\|NODES LAYER\|transit Rahu\|transit Ketu" > $S/m3d/${B}_m3.txt
cat $S/m3d/${B}_m3.txt; echo "---- numbers"; cat $S/m3d/${B}_nc.txt; echo "---- parallels"; cat $S/m3d/${B}_pa.txt
