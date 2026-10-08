#!/bin/bash
# fullpass.sh v1.0 - every check on one race, in one sheet, in the same order every time
# (Eddie, 3 Oct 12:10-12:11: "go through all the races again and double check ... one at a time ...
# keep as close to the raw data as possible"). No new measures: it only runs the existing scripts, whose
# lines all carry the raw degrees, the distance from the family target and applying / separating.
# Usage: bash fullpass.sh RACE LABEL   -> reads_out/LABEL_FULL.txt
R=$1; L=$2; cd /home/claude/ledger; O=reads_out/${L}_FULL.txt
{
echo "################ FULL PASS – $L $R"
echo; echo "======== 1. THE RACE, THE SKY, EACH RUNNER (readrace.py)"; python3 readrace.py --race $R
echo; echo "======== 2. REPEATED NUMBERS (repnum.py, across RA and Dec)"; python3 repnum.py --race $R
echo; echo "======== 3. DECIMAL-PLACE NUMBERS (scalenum.py)"; python3 scalenum.py --race $R
echo; echo "======== 4. CARRIER BODIES – where each runner holds race numbers (carrier.py)"; python3 carrier.py --race $R
echo; echo "======== 5. CLOSED LOOP – a pair lands on the body that carries its number (closed.py)"; python3 closed.py $R
echo; echo "======== 6. CONTACTS PEAKING AT THE OFF (peak.py)"; python3 peak.py $R
echo; echo "======== 7. ALL 80+ SKY NUMBERS, CROSS-COORDINATE, SELF CONTACTS (check2.py)"; python3 check2.py $R
echo; echo "======== 8. NATAL STRUCTURE, ROYALS, HORSE-JOCKEY (dig.py)"; python3 dig.py $R
echo; echo "======== 9. GROUPS (groups.py)"; python3 groups.py --race $R
echo; echo "======== 10. HALF NUMBERS (halfnum.py)"; python3 halfnum.py --race $R
echo; echo "======== 11. MIDPOINTS (midpoints.py)"; python3 midpoints.py --race $R
} > $O 2>&1
wc -l $O
