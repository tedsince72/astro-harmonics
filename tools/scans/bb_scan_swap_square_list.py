import sys, subprocess, os, re
sys.path.insert(0,'tools/scans'); sys.argv=sys.argv[:1]
from bb_scan_negatives import RACES
for race,win in RACES:
    if not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'): continue
    o=subprocess.run(['python3','tools/scans/bb_scan_swap_square.py',race,'90','80'],capture_output=True,text=True).stdout
    cur=None; hold={}
    for l in o.splitlines():
        m=re.match(r'^\d+ (.+) (\d+)$',l)
        if m: cur=m.group(1); continue
        if cur and l.startswith('    H ') and '×φ' in l.split('|')[1]: hold.setdefault(cur,l.strip())
    for h,l in hold.items(): print(race, h, 'WON' if h==win else '', '|', l)
