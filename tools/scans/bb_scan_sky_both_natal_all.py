import sys,os
sys.path.insert(0,'tools/scans'); sys.argv=sys.argv[:1]
import bb_scan_sky_both_natal as S, bb_scan_negatives as N
top=exp=0; n=0; bot=0; lines=[]
for race,win in N.RACES:
    if not os.path.exists(f'reference/classic/race_batch_{race}_active.xlsx'): continue
    rows=S.race_rows(race); tots=[(h,sum(len(res[c][0])+len(res[c][1]) for c in 'HJ')) for h,j,res,sky in rows]
    w=[t for h,t in tots if win.lower() in str(h).lower()]
    if not w: lines.append(f'{race} winner not found'); continue
    w=w[0]; mx=max(t for h,t in tots); mn=min(t for h,t in tots); k=len(tots)
    ntop=sum(1 for h,t in tots if t==mx); nbot=sum(1 for h,t in tots if t==mn)
    n+=1; exp+=1/k
    if w==mx: top+=1/ntop
    if w==mn: bot+=1/nbot
    rank=1+sum(1 for h,t in tots if t>w)
    lines.append(f'{race} {win}: {w} (max {mx}, min {mn}, rank {rank} of {k})')
print('\n'.join(lines)); print(f'races {n}: winner top {top:.1f} (chance {exp:.1f}), bottom {bot:.1f} (chance {exp:.1f})')
