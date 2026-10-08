#!/bin/bash
# m3f.sh BODY : Method 3 for Frankel, Queen Anne 19 Jun 2012 off 14:34:00, 98 s; sky body matched to Frankel natal (P01, 12:00) chords
S=/home/claude/tools; R=20120619_ascot_1434; O=14:34:00; D=98; B=$1
cd /home/claude/lattice
timeout 600 python3 $S/sunchords.py $R $O $D $B 2>/dev/null | grep -v "^===\|NODES LAYER\|transit Rahu\|transit Ketu" | awk '/WHOLE/{p=1} !p || /0\.0[0-9][0-9]%$|0\.1[0-5][0-9]%$|WHOLE/' > $S/f_${B}_sc.txt &
timeout 600 python3 $S/numcheck.py $R $O $D $B 2>&1 | grep -v "^===\|NODES LAYER\|transit" > $S/f_${B}_nc.txt &
timeout 600 python3 $S/parallels.py $R $O $D 0.1 2>&1 | grep -E "^\[|sky $B" | grep -B1 "sky $B" > $S/f_${B}_pa.txt &
wait
sed '/WHOLE DAY/q' $S/f_${B}_sc.txt; echo "---- numbers/parallels"; cat $S/f_${B}_nc.txt $S/f_${B}_pa.txt; echo "---- Frankel natal strings"; python3 $S/fmatch.py $S/f_${B}_sc.txt
