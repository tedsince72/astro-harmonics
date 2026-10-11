#!/bin/bash
# run_race.sh RACE OFF(HH:MM:SS) NAME  - per-runner workbooks + every tool + a field overview (Eddie's winner-first reads, 11 Oct 2026)
R=$1; OFF=$2; N=$3; D=reference/classic/$N; O=docs/classic/$N; mkdir -p $O
[ "$4" = "batch" ] || python3.12 tools/race_to_workbooks.py $R $OFF $D > /dev/null
for f in $D/*.xlsx; do b=$(basename $f .xlsx | sed 's/.*__//')
  python3.12 tools/workbook_numbers.py $f > $O/${b}_numbers.txt; python3.12 tools/three_way_wb.py $f 0.02 > $O/${b}_three_way.txt
  python3.12 tools/three_same_body.py $f 0.15 > $O/${b}_same_body.txt; python3.12 tools/winner_detail.py $f Neptune > $O/${b}_detail.txt
  python3.12 tools/soak.py $f 0.02 4 > $O/${b}_soak.txt 2>/dev/null; done
python3.12 tools/field_summary.py $O $D > $O/field_summary.txt; cat $O/field_summary.txt
for f in $D/*.xlsx; do b=$(basename $f .xlsx | sed 's/.*__//'); echo "== $b $(head -1 $O/${b}_detail.txt | cut -d: -f2)"
  grep -E "^-- (NN|TN) .*together: [1-9]" -A4 $O/${b}_numbers.txt | grep "–" | grep -v MOON | sed 's/^/   together /'
  sed -n '/^C\./,/^D\./p' $O/${b}_detail.txt | grep -v -E "^C\.|^D\.|^   sky" | awk '$0 ~ /RA [0-1]\.[0-9]/ || $0 ~ /Dec 0\.[0-1]/' | grep -v '\*:' | sed 's/^/   node/'
  sed -n '/^B\./,/^C\./p' $O/${b}_detail.txt | grep -E "Dec 0\.0|RA 0\.[0-4]" | sed 's/^/   cross/'
  grep "LINK" $O/${b}_three_way.txt | sed 's/^/   3way/'
  sed -n '/ratios):/,/best set/p' $O/${b}_same_body.txt | grep "%" | sed 's/^/   samebody/'
  grep "partners at" $O/${b}_soak.txt | awk '{v=$5; sub("~","",v); if (v+0>=1) print}' | head -3 | sed 's/^/   soak/'; done
